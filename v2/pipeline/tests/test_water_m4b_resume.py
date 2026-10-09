"""Offline fixtures for the single explicitly authorized blocked-tile resume."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import requests
from shapely.geometry import box

import test_water_m4b_tiled as fixture

refresh = fixture.refresh


class BlockedResumeTests(unittest.TestCase):
    def blocked(self, root):
        tiles = refresh.split_tiles(fixture.EXTENT)
        northeast = tiles[3]
        children = refresh.split_tiles(northeast["extent"], northeast["id"])
        failed = {tuple(northeast["extent"]), tuple(children[0]["extent"]),
                  tuple(children[1]["extent"]),
                  tuple(refresh.split_tiles(children[1]["extent"], children[1]["id"])[1]["extent"])}

        def fail(url, params, calls):
            if params.get("returnCountOnly") and tuple(map(float, params["geometry"].split(","))) in failed:
                raise requests.Timeout("original fixture timeout")

        clock = fixture.Clock()
        client = fixture.Client(clock, hook=fail)
        transport = refresh.SavedTransport(client, root, now=clock.now, sleep=clock.sleep)
        with self.assertRaisesRegex(refresh.ExternalBlocked, "3.1.1") as error:
            refresh.discover_tiles(transport, 6, fixture.EXTENT, fixture.INFO)
        refresh.write_json(root / "session.json", {"retrieved_at_utc": "2026-10-08T00:00:00Z",
                                                 "blocked": str(error.exception)})
        refresh.write_json(root / "attempt-0001.json", {"outcome": "failed", "error": str(error.exception)})
        state = json.loads((root / "layer-6-tiles.json").read_text())
        self.assertEqual(len(state["unresolved_tiles"]), 5)
        self.assertEqual(sum(t["status"] == "complete" for t in state["tiles"].values()), 8)
        return clock, state

    def prepare(self, root, flag=True):
        with patch.object(refresh, "RAW_ROOT", root), patch.object(refresh, "STAGING", root / "stage"):
            return refresh.prepare_session(resume_blocked=flag)

    def resumed(self, root, clock, hook=None):
        session = self.prepare(root)
        client = fixture.Client(clock, hook=hook)
        transport = refresh.SavedTransport(client, root, now=clock.now, sleep=clock.sleep,
                                          resume_number=session["resume_number"])
        return transport, client

    def immutable_files(self, root):
        mutable = {"session.json", "request-ledger.json", "layer-6-tiles.json"}
        return {p.relative_to(root): p.read_bytes() for p in root.rglob("*.json")
                if p.name not in mutable}

    def test_without_flag_blocked_snapshot_refuses_without_any_mutation_or_request(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.blocked(root)
            before = {p: p.read_bytes() for p in root.rglob("*.json")}
            with self.assertRaises(refresh.ExternalBlocked):
                self.prepare(root, False)
            self.assertEqual(before, {p: p.read_bytes() for p in root.rglob("*.json")})

    def test_resume_skips_completed_discovery_and_preserves_every_old_request_and_attempt(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            clock, old = self.blocked(root)
            before = self.immutable_files(root)
            transport, client = self.resumed(root, clock)
            _, state = refresh.discover_tiles(transport, 6, fixture.EXTENT, fixture.INFO)
            reused = {','.join(map(str,t['extent'])) for t in old['tiles'].values() if t['status']=='complete'}
            self.assertTrue(client.calls)
            self.assertFalse(any(call[2].get('geometry') in reused for call in client.calls))
            self.assertEqual(before, {p: (root / p).read_bytes() for p in before})
            self.assertEqual(sum(t.get('completed_in')=='original' for t in state['tiles'].values()), 8)
            self.assertEqual(sum(t.get('completed_in')=='resume-1' for t in state['tiles'].values()), 5)
            self.assertTrue(state['coverage_complete'])
            session = json.loads((root/'session.json').read_text())
            self.assertEqual(session['resume_number'], 1)
            self.assertTrue(session['resume_started_at_utc'].endswith('Z'))
            self.assertTrue(list(root.rglob('resume-1-attempt-1-count.json')))

    def test_second_resume_is_refused_even_if_active_or_reblocked(self):
        for reblocked in (False, True):
            with self.subTest(reblocked=reblocked), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                self.blocked(root)
                self.prepare(root)
                session = json.loads((root/'session.json').read_text())
                if reblocked:
                    session['blocked'] = 'resume failed'
                    refresh.write_json(root/'session.json', session)
                before = {p: p.read_bytes() for p in root.rglob('*.json')}
                with self.assertRaisesRegex(RuntimeError, 'already been consumed'):
                    self.prepare(root)
                self.assertEqual(before, {p: p.read_bytes() for p in root.rglob('*.json')})

    def test_unresolved_tiles_have_fresh_two_attempt_policy_and_only_level1_subdivides(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            clock, old = self.blocked(root)
            envelopes = {k: ','.join(map(str,v['extent'])) for k,v in old['tiles'].items()}

            def fail(url, params, calls):
                if params.get('returnCountOnly') and params.get('geometry') == envelopes['3.2']:
                    raise requests.Timeout('resumed level1 timeout')
                if params.get('returnCountOnly') and params.get('geometry') == envelopes['3.1.1']:
                    count = sum(bool(c[2].get('returnCountOnly')) and c[2].get('geometry') == envelopes['3.1.1'] for c in calls)
                    if count == 1:
                        return fixture.Response({}, 503)

            transport, client = self.resumed(root, clock, fail)
            _, state = refresh.discover_tiles(transport, 6, fixture.EXTENT, fixture.INFO)
            self.assertEqual(len(state['tiles']['3.1.1']['attempts']), 2)
            self.assertEqual(len(state['tiles']['3.1.1']['resume_attempts']), 2)
            self.assertEqual([a['outcome'] for a in state['tiles']['3.1.1']['resume_attempts']], ['service_failure','complete'])
            self.assertEqual(len(state['tiles']['3.2']['resume_attempts']), 2)
            self.assertEqual(state['tiles']['3.2']['status'], 'subdivided')
            self.assertEqual(len(state['tiles']['3.2']['children']), 4)
            self.assertTrue(all(state['tiles'][k]['depth']==2 for k in state['tiles']['3.2']['children']))
            for tile in state['tiles'].values():
                tries = tile.get('resume_attempts', [])
                self.assertLessEqual(len(tries), 2)
                if len(tries)==2:
                    from datetime import datetime
                    self.assertGreaterEqual(datetime.fromisoformat(tries[1]['timestamp_utc']).timestamp()-tries[0]['finished_epoch'],60)
            self.assertTrue(all(b[0]-a[0]>=2 for a,b in zip(client.calls,client.calls[1:])))

    def test_level2_resume_failure_stops_with_remaining_envelopes_and_old_files_intact(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            clock, old = self.blocked(root)
            before = self.immutable_files(root)
            envelope = ','.join(map(str,old['tiles']['3.1.1']['extent']))
            def fail(url, params, calls):
                if params.get('geometry')==envelope:
                    raise requests.Timeout('second session timeout')
            transport, client = self.resumed(root, clock, fail)
            with self.assertRaisesRegex(refresh.ExternalBlocked,'level-2 tile 3.1.1 failed twice'):
                refresh.discover_tiles(transport,6,fixture.EXTENT,fixture.INFO)
            state=json.loads((root/'layer-6-tiles.json').read_text())
            self.assertFalse(state['coverage_complete'])
            self.assertEqual({x['id'] for x in state['unresolved_tiles']}, {'3.1.1','3.1.2','3.1.3','3.2','3.3'})
            self.assertEqual(len(client.calls),2)
            self.assertEqual(len(state['tiles']['3.1.1']['resume_attempts']),2)
            self.assertEqual(before,{p:(root/p).read_bytes() for p in before})
            self.assertFalse(list((root/'stage').glob('*.geojson')))

    def test_discovery_cap_is_cumulative_and_not_reset_by_resume(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            clock,_=self.blocked(root)
            ledger=json.loads((root/'request-ledger.json').read_text())
            ledger['discovery_requests']['6']=149
            refresh.write_json(root/'request-ledger.json',ledger)
            transport,client=self.resumed(root,clock)
            self.assertEqual(transport.ledger['discovery_requests']['6'],149)
            with self.assertRaisesRegex(refresh.ExternalBlocked,'150 discovery requests'):
                refresh.discover_tiles(transport,6,fixture.EXTENT,fixture.INFO)
            self.assertEqual(len(client.calls),1)
            self.assertEqual(transport.ledger['discovery_requests']['6'],150)

    def test_resumed_result_equals_unblocked_single_session_and_verifies_every_leaf(self):
        outputs=[]
        for blocked in (False,True):
            with tempfile.TemporaryDirectory() as directory:
                root=Path(directory)
                if blocked:
                    clock,old=self.blocked(root)
                    before=self.immutable_files(root)
                    transport,client=self.resumed(root,clock)
                else:
                    clock=fixture.Clock()
                    client=fixture.Client(clock)
                    transport=refresh.SavedTransport(client,root,now=clock.now,sleep=clock.sleep)
                fc,record=refresh.tiled_layer_query(transport,'flowline',6,fixture.EXTENT,refresh.m4a.OUT_FIELDS['flowline'])
                features,_=refresh._derive_flowlines(fc['features'],box(*fixture.EXTENT),fixture.EVIDENCE)
                outputs.append(json.dumps(features,sort_keys=True,separators=(',',':')))
                if blocked:
                    leaves=[t for t in record['tiles']['tiles'].values() if t['status']=='complete']
                    self.assertEqual(len(list(root.rglob('resume-1-verify.json'))),len(leaves))
                    self.assertEqual(before,{p:(root/p).read_bytes() for p in before})
        self.assertEqual(outputs[0],outputs[1])

    def test_changed_ids_in_reused_tile_stop_in_final_verification(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            clock,old=self.blocked(root)
            envelope=','.join(map(str,old['tiles']['0']['extent']))
            def change(url,params,calls):
                if params.get('returnIdsOnly') and params.get('geometry')==envelope:
                    return fixture.Response({'objectIds':[999]})
            transport,client=self.resumed(root,clock,change)
            with self.assertRaisesRegex(RuntimeError,'tile 0 IDs changed during session'):
                refresh.tiled_layer_query(transport,'flowline',6,fixture.EXTENT,refresh.m4a.OUT_FIELDS['flowline'])
            self.assertEqual(sum(c[2].get('geometry')==envelope for c in client.calls),1)

    def test_record_page_continuation_does_not_consume_another_resume(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            clock,_=self.blocked(root)
            def fail(url,params,calls):
                if 'objectIds' in params and sum('objectIds' in c[2] for c in calls)==1:
                    raise requests.Timeout('page fixture timeout')
            transport,client=self.resumed(root,clock,fail)
            refresh.tiled_layer_query(transport,'flowline',6,fixture.EXTENT,refresh.m4a.OUT_FIELDS['flowline'])
            pages=[c for c in client.calls if 'objectIds' in c[2]]
            self.assertEqual(len(pages),2)
            self.assertGreaterEqual(pages[1][0]-pages[0][0],900)
            session_before=(root/'session.json').read_bytes()
            self.assertEqual(self.prepare(root,False)['resume_number'],1)
            before=len(client.calls)
            refresh.tiled_layer_query(transport,'flowline',6,fixture.EXTENT,refresh.m4a.OUT_FIELDS['flowline'])
            self.assertEqual(len(client.calls),before)
            self.assertEqual((root/'session.json').read_bytes(),session_before)

    def test_new_layer_completion_origin_survives_active_session_continuation(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            clock,_=self.blocked(root)
            transport,_=self.resumed(root,clock)
            refresh.discover_tiles(transport,12,fixture.EXTENT,fixture.INFO)
            before=(root/'layer-12-tiles.json').read_bytes()
            self.prepare(root,False)
            self.assertEqual((root/'layer-12-tiles.json').read_bytes(),before)
            state=json.loads(before)
            self.assertEqual(state['resume_number'],1)
            self.assertTrue(all(t['completed_in']=='resume-1' for t in state['tiles'].values()))


if __name__=='__main__':
    unittest.main()
