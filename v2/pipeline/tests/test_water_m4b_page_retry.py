"""Network-free four-attempt record-page queue, recovery and migration tests."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import requests
from shapely.geometry import box, mapping
import test_water_m4b_tiled as fixture

refresh = fixture.refresh


class PageRetryTests(unittest.TestCase):
    def setup_transport(self, root, hook=None, clock=None, layer=6):
        clock = clock or fixture.Clock()
        rows = [fixture.row(i, [(-105.1, 39.2), (-104.9, 39.2)]) for i in range(1, 502)]
        client = fixture.Client(clock, rows=rows, hook=hook)
        transport = refresh.SavedTransport(client, root, now=clock.now, sleep=clock.sleep)
        return transport, client, clock

    def query(self, transport, layer=6):
        name = 'flowline' if layer == 6 else 'waterbody'
        return refresh.tiled_layer_query(transport, name, layer, fixture.EXTENT,
                                         refresh.m4a.OUT_FIELDS[name])

    def calls(self, client):
        return [c for c in client.calls if 'objectIds' in c[2]]

    def plan(self, root):
        return json.loads((root/'douglas-co-flowline-plan.json').read_text())

    def test_failure_is_queued_later_pages_fetched_and_spacing_enforced(self):
        def fail(url, params, calls):
            if params.get('objectIds', '').startswith('1,') and sum('objectIds' in c[2] for c in calls) == 1:
                return fixture.Response({}, 504)
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            t, client, clock = self.setup_transport(root, fail)
            fc, _ = self.query(t)
            calls = self.calls(client)
            self.assertEqual([int(c[2]['objectIds'].split(',')[0]) for c in calls], [1,251,501,1])
            self.assertGreaterEqual(calls[-1][0]-calls[0][0],900)
            self.assertTrue(all(b[0]-a[0]>=2 for a,b in zip(client.calls, client.calls[1:])))
            self.assertEqual(len(fc['features']),501)
            self.assertEqual(len({f['properties']['permanent_identifier'] for f in fc['features']}),501)
            self.assertEqual(self.plan(root)['failed_pages'],{})
            saved = {p:p.read_bytes() for p in root.rglob('*.json') if p.name.startswith(('page-', 'request-'))}
            client.calls.clear()
            self.query(refresh.SavedTransport(client,root,now=clock.now,sleep=clock.sleep))
            self.assertEqual(client.calls,[])
            self.assertEqual(saved,{p:p.read_bytes() for p in saved})

    def test_interleaved_failures_have_deterministic_collection_bytes(self):
        outputs=[]
        for failed in ((),(1,251),(251,501)):
            seen={}
            def fail(url,params,calls):
                if 'objectIds' in params:
                    first=int(params['objectIds'].split(',')[0]);seen[first]=seen.get(first,0)+1
                    if first in failed and seen[first]==1:
                        raise requests.ConnectionError('transient fixture')
            with tempfile.TemporaryDirectory() as d:
                t,client,_=self.setup_transport(Path(d),fail)
                fc,_=self.query(t);outputs.append(json.dumps(fc,separators=(',',':')).encode())
                for first in failed:
                    times=[c[0] for c in self.calls(client) if int(c[2]['objectIds'].split(',')[0])==first]
                    self.assertGreaterEqual(times[1]-times[0],900)
        self.assertEqual(outputs[0],outputs[1]);self.assertEqual(outputs[0],outputs[2])

    def test_exhaustion_exactly_four_attempts_finishes_other_pages_before_verification(self):
        def fail(url,params,calls):
            if params.get('objectIds','').startswith('1,'):
                return fixture.Response({'error':{'code':503,'message':'busy'}})
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);t,client,_=self.setup_transport(root,fail)
            with self.assertRaisesRegex(refresh.ExternalBlocked,'exhausted.*1'):
                self.query(t)
            calls=self.calls(client)
            first=[c for c in calls if c[2]['objectIds'].startswith('1,')]
            self.assertEqual(len(first),4)
            self.assertTrue(all(b[0]-a[0]>=900 for a,b in zip(first,first[1:])))
            self.assertTrue((root/'douglas-co-flowline-pages/page-0002.json').exists())
            self.assertTrue((root/'douglas-co-flowline-pages/page-0003.json').exists())
            self.assertFalse(list(root.rglob('*verify.json')))
            self.assertEqual(self.plan(root)['exhausted_pages'],[1])
            self.assertFalse(list((root/'stage').glob('*.geojson')))
            count=len(client.calls)
            with self.assertRaises(refresh.ExternalBlocked):self.query(t)
            self.assertEqual(count,len(client.calls))

    def test_restart_keeps_queue_attempts_and_deadline(self):
        failures=[]
        def fail(url,params,calls):
            if params.get('objectIds','').startswith('1,') and not failures:
                failures.append(True);raise requests.Timeout('first failure')
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);t,client,clock=self.setup_transport(root,fail)
            original_sleep=clock.sleep
            def die(seconds):
                if seconds>2:raise KeyboardInterrupt()
                original_sleep(seconds)
            t.sleep=die
            with self.assertRaises(KeyboardInterrupt):self.query(t)
            plan=self.plan(root);entry=plan['failed_pages']['1']
            self.assertEqual(entry['attempts'],1)
            self.assertGreater(entry['next_eligible_epoch'],clock.now())
            immutable=(root/'douglas-co-flowline-pages/request-0001-1.json').read_bytes()
            new=refresh.SavedTransport(client,root,now=clock.now,sleep=clock.sleep)
            fc,_=self.query(new)
            first=[c for c in self.calls(client) if c[2]['objectIds'].startswith('1,')]
            self.assertEqual(len(first),2);self.assertGreaterEqual(first[1][0]-first[0][0],900)
            self.assertEqual(len(fc['features']),501)
            self.assertEqual(immutable,(root/'douglas-co-flowline-pages/request-0001-1.json').read_bytes())

    def test_interrupted_request_counts_and_success_response_recovers_without_reissue(self):
        for interrupted in (True,False):
            with self.subTest(interrupted=interrupted),tempfile.TemporaryDirectory() as d:
                root=Path(d);t,client,clock=self.setup_transport(root)
                original=t.request
                def die(path,*args,**kwargs):
                    if Path(path).name=='request-0001-1.json':
                        if interrupted:
                            with patch.object(client,'get',side_effect=KeyboardInterrupt):original(path,*args,**kwargs)
                        else:original(path,*args,**kwargs)
                        raise KeyboardInterrupt()
                    return original(path,*args,**kwargs)
                with patch.object(t,'request',side_effect=die):
                    with self.assertRaises(KeyboardInterrupt):self.query(t)
                file=root/'douglas-co-flowline-pages/request-0001-1.json';before=file.read_bytes()
                requests_before=len(self.calls(client))
                self.query(refresh.SavedTransport(client,root,now=clock.now,sleep=clock.sleep))
                self.assertEqual(before,file.read_bytes())
                records=list((root/'douglas-co-flowline-pages').glob('request-0001-*.json'))
                self.assertEqual(len(records),2 if interrupted else 1)
                self.assertEqual(len(self.calls(client))-requests_before,3 if interrupted else 2)
                if interrupted:
                    first=json.loads(before);retry=json.loads(records[-1].read_text())
                    self.assertGreaterEqual(retry['finished_epoch']-first['finished_epoch'],900)

    def test_real_shaped_blocked_migration_preserves_all_requests_pages_and_two_tries_left(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);clock=fixture.Clock()
            page_dir=root/'douglas-co-flowline-pages'
            ids=list(range(1,14001))
            plan={'layer_id':6,'extent':list(fixture.EXTENT),'out_fields':refresh.m4a.OUT_FIELDS['flowline'],
                  'page_size':250,'object_id_field':'OBJECTID','object_ids':ids,'completed_pages':list(range(1,56)),
                  'failed_pages':{'56':{'failures':2,'finished_epoch':1000,'error':'timeout'}}}
            for n in range(1,57):
                batch=ids[(n-1)*250:n*250]
                params={'f':'geojson','objectIds':','.join(map(str,batch)),'outFields':plan['out_fields']+',OBJECTID',
                        'outSR':4326,'returnGeometry':'true','returnZ':'false','returnM':'false'}
                page={'type':'FeatureCollection','features':[fixture.row(i,[(-105.1,39.2),(-104.9,39.2)]) for i in batch]}
                if n<56:refresh.write_json(page_dir/f'page-{n:04d}.json',page)
                for a in range(1,3 if n==56 else 2):
                    record={'url':refresh.SERVICE+'/6/query','params':params,'timeout':120,
                            'context':{'page':n,'attempt':a},'timestamp_utc':'2026-10-08T00:00:00Z',
                            'finished_epoch':1000,'outcome':'service_failure' if n==56 else 'received'}
                    if n==56:record['error']='timeout'
                    else:record.update(status_code=200,response_text=json.dumps(page))
                    refresh.write_json(page_dir/f'request-{n:04d}-{a}.json',record)
            refresh.write_json(root/'douglas-co-flowline-plan.json',plan)
            refresh.write_json(root/'session.json',{'retrieved_at_utc':'2026-10-08T00:00:00Z',
                       'resume_number':1,'blocked':'layer 6 page 56 failed twice'})
            before={p:p.read_bytes() for p in page_dir.glob('*.json')}
            with patch.object(refresh,'RAW_ROOT',root),patch.object(refresh,'STAGING',root/'stage'):
                session=refresh.prepare_session(now=clock.now)
                migrated=self.plan(root)
                self.assertNotIn('blocked',session)
                self.assertEqual(session['resume_number'],1)
                self.assertEqual(migrated['failed_pages']['56']['attempts'],2)
                self.assertEqual(migrated['failed_pages']['56']['next_eligible_epoch'],1900)
                self.assertEqual(migrated['page_retry_policy']['max_attempts'],4)
                self.assertEqual(migrated['page_retry_policy']['min_retry_seconds'],900)
                self.assertIn('page_policy_migrated_at_utc',session)
                self.assertEqual(before,{p:p.read_bytes() for p in before})
                self.assertEqual(session,refresh.prepare_session(now=clock.now))

    def test_layer12_uses_same_queue_policy(self):
        failed=[]
        def fail(url,params,calls):
            if 'objectIds' in params and not failed:
                failed.append(True);return fixture.Response({},503)
        with tempfile.TemporaryDirectory() as d:
            t,client,_=self.setup_transport(Path(d),fail)
            fc,_=self.query(t,12)
            self.assertEqual(len(fc['features']),501)
            calls=self.calls(client);self.assertGreaterEqual(calls[-1][0]-calls[0][0],900)
            self.assertTrue(all('/12/query' in c[1] for c in calls))

    def test_exhausted_session_blocks_and_partial_run_never_changes_canonical_or_stages(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);raw=root/'raw';stage=root/'stage';v2=root/'v2'
            canonical=v2/'regions/douglas-co/research.json'
            refresh.write_json(canonical,{'layers':{
                'coverage':{'features':[{'geometry':mapping(box(*fixture.EXTENT))}]},
                'waterways':{'features':[]},'waterbodies':{'features':[]}}})
            before=canonical.read_bytes()
            def fail(url,params,calls):
                if params.get('objectIds','').startswith('1,'):
                    raise requests.Timeout('service fixture timeout')
            transport,client,_=self.setup_transport(raw,fail)
            with patch.object(refresh,'RAW_ROOT',raw),patch.object(refresh,'STAGING',stage), \
                 patch.object(refresh,'V2',v2),patch.object(refresh,'preservation_hashes',return_value={}), \
                 patch.object(refresh,'SavedTransport',return_value=transport), \
                 patch.object(refresh.sys,'argv',['refresh','--run']):
                with self.assertRaises(refresh.ExternalBlocked):refresh.main()
                self.assertIn('exhausted',json.loads((raw/'session.json').read_text())['blocked'])
                count=len(client.calls)
                with self.assertRaises(refresh.ExternalBlocked):refresh.prepare_session()
                self.assertEqual(len(client.calls),count)
            self.assertEqual(before,canonical.read_bytes())
            self.assertFalse(list(stage.glob('*.geojson')))
            self.assertFalse((stage/'refresh-report.json').exists())
            self.assertFalse((raw/'layer-12-metadata-response.json').exists())
            files=list((raw/'douglas-co-flowline-pages').glob('request-0001-*.json'))
            self.assertEqual(len(files),4)
            for file in files:
                record=json.loads(file.read_text())
                self.assertEqual(record['outcome'],'service_failure')
                self.assertIn('timestamp_utc',record)
                self.assertIn('error',record)

    def test_non_service_page_failures_stop_immediately_without_later_page_or_retry(self):
        for failure in ('wrong_ids','missing_identity','unsupported_type','conflict'):
            with self.subTest(failure=failure),tempfile.TemporaryDirectory() as d:
                def bad(url,params,calls):
                    if 'objectIds' not in params:return
                    ids=list(map(int,params['objectIds'].split(',')))
                    rows=[fixture.row(i,[(-105.1,39.2),(-104.9,39.2)]) for i in ids]
                    if failure=='wrong_ids':rows.pop()
                    if failure=='missing_identity':rows[0]['properties'].pop('permanent_identifier')
                    if failure=='unsupported_type':rows[0]['properties']['ftype']=999
                    if failure=='conflict':rows[1]['properties']['permanent_identifier']=rows[0]['properties']['permanent_identifier']
                    return fixture.Response({'type':'FeatureCollection','features':rows})
                t,client,_=self.setup_transport(Path(d),bad)
                with self.assertRaises((RuntimeError,ValueError)):self.query(t)
                self.assertEqual(len(self.calls(client)),1)
                self.assertFalse(list(Path(d).rglob('*verify.json')))

    def test_migration_restarts_after_plan_written_before_session_activation(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);t,client,clock=self.setup_transport(root)
            self.query(t)
            plan=self.plan(root)
            page_dir=root/'douglas-co-flowline-pages'
            (page_dir/'page-0001.json').unlink()
            record=json.loads((page_dir/'request-0001-1.json').read_text())
            record.update(outcome='service_failure',error='legacy timeout')
            refresh.write_json(page_dir/'request-0001-1.json',record)
            plan['failed_pages']={'1':{'failures':2,'finished_epoch':clock.now(),'error':'legacy timeout'}}
            plan.pop('page_retry_policy');plan.pop('page_policy_migrated_at_utc')
            second=dict(record);second['context']={'page':1,'attempt':2}
            refresh.write_json(page_dir/'request-0001-2.json',second)
            refresh.write_json(root/'douglas-co-flowline-plan.json',plan)
            refresh.write_json(root/'session.json',{'retrieved_at_utc':'2026-10-08T00:00:00Z','resume_number':1,
                                                 'blocked':'layer 6 page 1 failed twice'})
            # Simulate death after the migrated plan was durable but before session activation.
            refresh.reconcile_page_policy(plan,root/'douglas-co-flowline-plan.json',clock.now())
            before={p:p.read_bytes() for p in page_dir.glob('*.json')}
            with patch.object(refresh,'RAW_ROOT',root),patch.object(refresh,'STAGING',root/'stage'):
                session=refresh.prepare_session(now=clock.now)
            self.assertNotIn('blocked',session)
            self.assertEqual(self.plan(root)['failed_pages']['1']['attempts'],2)
            self.assertEqual(before,{p:p.read_bytes() for p in before})


if __name__=='__main__':unittest.main()
