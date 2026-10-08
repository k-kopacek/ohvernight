"""Offline policy and completeness tests for the approved tiled transport."""
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import requests
from shapely.geometry import LineString, box, mapping, shape
from shapely.ops import unary_union

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
import refresh_m4b_douglas_water as refresh
from lib.evidence import make_evidence
from lib.water import normalize_feature

EXTENT = (-105.2, 39.1, -104.8, 39.5)
INFO = {"type": "Feature Layer", "maxRecordCount": 2000,
        "fields": [{"name": "OBJECTID", "type": "esriFieldTypeOID"},
                   *[{"name": name, "type": "esriFieldTypeString"}
                     for name in ("permanent_identifier", "ftype", "fcode")]]}
EVIDENCE = make_evidence("https://fixture/6", "USGS")
EVIDENCE["retrieved_at"] = "2026-10-08T00:00:00Z"


def row(oid, coords, name="River"):
    return {"type": "Feature", "geometry": mapping(LineString(coords)),
            "properties": {"OBJECTID": oid, "permanent_identifier": f"source-{oid}",
                           "gnis_id": "0001", "gnis_name": name, "ftype": 460,
                           "fcode": 46006, "lengthkm": 1.0}}


ROWS = [row(3, [(-105.1, 39.2), (-104.9, 39.2)]),
        row(1, [(-105.1, 39.3), (-104.9, 39.3)]),
        row(2, [(-105.1, 39.4), (-104.9, 39.4)])]


class Clock:
    def __init__(self):
        self.value = 1000
        self.sleeps = []

    def now(self):
        return self.value

    def sleep(self, seconds):
        self.sleeps.append(seconds)
        self.value += seconds


class Response:
    def __init__(self, payload, status=200):
        self.status_code = status
        self.text = json.dumps(payload)


class Client:
    def __init__(self, clock, rows=None, hook=None):
        self.clock, self.rows = clock, ROWS if rows is None else rows
        self.hook, self.calls = hook, []

    def get(self, url, params, timeout, allow_redirects=False):
        if allow_redirects:
            raise AssertionError("transport must not follow redirects to another host")
        self.calls.append((self.clock.now(), url, dict(params), timeout))
        if self.hook:
            response = self.hook(url, params, self.calls)
            if response is not None:
                return response
        if not url.endswith("/query"):
            return Response(INFO if url.rsplit("/", 1)[-1] in {"6", "12"}
                            else {"currentVersion": 11.3})
        if "objectIds" in params:
            ids = set(map(int, params["objectIds"].split(",")))
            return Response({"type": "FeatureCollection",
                             "features": [item for item in reversed(self.rows)
                                          if item["properties"]["OBJECTID"] in ids]})
        extent = tuple(map(float, params["geometry"].split(",")))
        ids = [item["properties"]["OBJECTID"] for item in reversed(self.rows)
               if box(*extent).intersects(shape(item["geometry"]))]
        return Response({"count": len(ids)} if "returnCountOnly" in params else {"objectIds": ids})


class TiledTests(unittest.TestCase):
    def transport(self, root, hook=None, rows=None):
        clock = Clock()
        client = Client(clock, hook=hook, rows=rows)
        return refresh.SavedTransport(client, root, now=clock.now, sleep=clock.sleep), client, clock

    def discover(self, transport, **kwargs):
        return refresh.discover_tiles(transport, 6, EXTENT, INFO, **kwargs)

    def test_exact_area_and_edge_coverage_at_every_depth(self):
        tiles = refresh.split_tiles(EXTENT)
        for depth in range(3):
            geometries = [box(*tile["extent"]) for tile in tiles]
            self.assertTrue(unary_union(geometries).equals(box(*EXTENT)))
            self.assertAlmostEqual(sum(part.area for part in geometries), box(*EXTENT).area, places=14)
            if depth == 0:
                self.assertEqual(tiles[0]["extent"][2], tiles[1]["extent"][0])
                self.assertEqual(tiles[0]["extent"][3], tiles[2]["extent"][1])
            # Mixed depths prove subdividing only one tile leaves no gap or overlap.
            leaf = tiles.pop(0)
            tiles.extend(refresh.split_tiles(leaf["extent"], leaf["id"]))

    def test_full_uniform_level2_grid_is_exactly_64_tiles(self):
        tiles = refresh.split_tiles(EXTENT)
        for _ in range(2):
            tiles = [child for tile in tiles for child in refresh.split_tiles(tile["extent"], tile["id"])]
        self.assertEqual(len(tiles), 64)
        self.assertTrue(unary_union([box(*tile["extent"]) for tile in tiles]).equals(box(*EXTENT)))
        self.assertAlmostEqual(sum(box(*tile["extent"]).area for tile in tiles),
                               box(*EXTENT).area, places=14)

    def test_boundary_feature_is_paged_once_and_ids_sorted(self):
        with tempfile.TemporaryDirectory() as directory:
            transport, client, _ = self.transport(Path(directory))
            fc, record = refresh.tiled_layer_query(transport, "flowline", 6, EXTENT,
                                                   refresh.m4a.OUT_FIELDS["flowline"])
            self.assertEqual([item["properties"]["permanent_identifier"] for item in fc["features"]],
                             ["source-1", "source-2", "source-3"])
            pages = [call for call in client.calls if "objectIds" in call[2]]
            self.assertEqual(len(pages), 1)
            self.assertEqual(pages[0][2]["objectIds"], "1,2,3")
            self.assertGreater(record["tiles"]["duplicates_removed"], 0)
            self.assertEqual(record["discovery_requests"], 12)
            self.assertTrue(all(b[0] - a[0] >= 2 for a, b in zip(client.calls, client.calls[1:])))

    def test_stage_bytes_independent_of_order_and_subdivision(self):
        outputs = []
        first = refresh.split_tiles(EXTENT)[0]["extent"]
        for order, subdivide in ((["0", "1", "2", "3"], False),
                                 (["3", "1", "0", "2"], False),
                                 (["2", "1", "3", "0"], True)):
            def hook(url, params, calls):
                if subdivide and params.get("geometry") == ",".join(map(str, first)):
                    return Response({}, 504)
            with tempfile.TemporaryDirectory() as directory:
                transport, _, _ = self.transport(Path(directory), hook=hook)
                self.discover(transport, tile_order=order)
                fc, _ = refresh.tiled_layer_query(transport, "flowline", 6, EXTENT,
                                                  refresh.m4a.OUT_FIELDS["flowline"])
                features, _ = refresh._derive_flowlines(fc["features"], box(*EXTENT), EVIDENCE)
                out = Path(directory) / "stage.geojson"
                refresh.write_json(out, {"type": "FeatureCollection", "features": features})
                outputs.append(out.read_bytes())
        self.assertEqual(outputs[0], outputs[1])
        self.assertEqual(outputs[0], outputs[2])

    def test_two_service_failures_subdivide_only_the_failed_tile(self):
        first = refresh.split_tiles(EXTENT)[0]["extent"]
        def hook(url, params, calls):
            if params.get("geometry") == ",".join(map(str, first)):
                raise requests.Timeout("fixture timeout")
        with tempfile.TemporaryDirectory() as directory:
            transport, client, _ = self.transport(Path(directory), hook)
            ids, state = self.discover(transport)
            self.assertEqual(ids, [1, 2, 3])
            self.assertEqual([key for key, tile in state["tiles"].items()
                              if tile["status"] == "subdivided"], ["0"])
            attempts = [call for call in client.calls
                        if call[2].get("geometry") == ",".join(map(str, first))]
            self.assertEqual(len(attempts), 2)
            self.assertGreaterEqual(attempts[1][0] - attempts[0][0], 60)

    def test_level2_failure_saves_partial_coverage_and_run_writes_no_stage(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            raw_root, stage, v2 = root / "raw", root / "stage", root / "v2"
            bundle_path = v2 / "regions/douglas-co/research.json"
            refresh.write_json(bundle_path, {"layers": {
                "coverage": {"features": [{"geometry": mapping(box(*EXTENT))}]},
                "waterways": {"features": []}, "waterbodies": {"features": []}}})
            clock = Clock()
            def hook(url, params, calls):
                if params.get("returnCountOnly"):
                    return Response({}, 503)
            client = Client(clock, hook=hook)
            transport = refresh.SavedTransport(client, raw_root, now=clock.now, sleep=clock.sleep)
            with patch.object(refresh, "RAW_ROOT", raw_root), patch.object(refresh, "STAGING", stage), \
                 patch.object(refresh, "V2", v2), patch.object(refresh, "preservation_hashes", return_value={}), \
                 patch.object(refresh, "SavedTransport", return_value=transport):
                with self.assertRaisesRegex(refresh.ExternalBlocked, "level-2"):
                    refresh.run()
            state = json.loads((raw_root / "layer-6-tiles.json").read_text())
            self.assertFalse(state["coverage_complete"])
            self.assertTrue(state["unresolved_tiles"])
            self.assertFalse(list(stage.glob("*.geojson")))
            count = len(client.calls)
            with self.assertRaises(refresh.ExternalBlocked):
                refresh.discover_tiles(transport, 6, state["extent"], INFO)
            self.assertEqual(len(client.calls), count)

    def test_discovery_cap_includes_retries_and_stops_without_skipping(self):
        with tempfile.TemporaryDirectory() as directory:
            transport, client, _ = self.transport(Path(directory))
            with patch.object(refresh, "DISCOVERY_CAP", 3):
                with self.assertRaisesRegex(refresh.ExternalBlocked, "3 discovery requests"):
                    self.discover(transport)
            self.assertEqual(len(client.calls), 3)
            state = json.loads((Path(directory) / "layer-6-tiles.json").read_text())
            self.assertFalse(state["coverage_complete"])
            self.assertTrue(state["unresolved_tiles"])

    def test_truncated_and_count_mismatched_responses_are_not_accepted(self):
        first = refresh.split_tiles(EXTENT)[0]["extent"]
        for payload in ({"objectIds": [1, 2, 3], "exceededTransferLimit": True},
                        {"objectIds": [1]}):
            def hook(url, params, calls):
                if params.get("geometry") == ",".join(map(str, first)) and params.get("returnIdsOnly"):
                    return Response(payload)
            with self.subTest(payload_size=len(payload["objectIds"])), tempfile.TemporaryDirectory() as directory:
                transport, _, _ = self.transport(Path(directory), hook)
                _, state = self.discover(transport)
                self.assertEqual(state["tiles"]["0"]["status"], "subdivided")
                self.assertTrue(all(attempt["outcome"] == "overflow"
                                    for attempt in state["tiles"]["0"]["attempts"]))

    def test_invalid_and_duplicate_ids_are_fatal(self):
        for payload in ({"objectIds": [1, 1]}, {"objectIds": [1, "2"]}):
            def hook(url, params, calls):
                if params.get("returnIdsOnly"):
                    return Response(payload)
            with tempfile.TemporaryDirectory() as directory:
                transport, client, _ = self.transport(Path(directory), hook)
                with self.assertRaises(RuntimeError):
                    self.discover(transport)
                self.assertEqual(len(client.calls), 2)

    def test_resumed_discovery_never_requests_completed_tiles(self):
        with tempfile.TemporaryDirectory() as directory:
            transport, client, clock = self.transport(Path(directory))
            self.discover(transport)
            count = len(client.calls)
            resumed = refresh.SavedTransport(client, Path(directory), now=clock.now, sleep=clock.sleep)
            ids, _ = self.discover(resumed, tile_order=["3", "2", "1", "0"])
            self.assertEqual(ids, [1, 2, 3])
            self.assertEqual(len(client.calls), count)

    def test_response_is_saved_before_validation_and_has_exact_parameters(self):
        with tempfile.TemporaryDirectory() as directory:
            transport, client, _ = self.transport(Path(directory))
            self.discover(transport)
            tile_dir = Path(directory) / "layer-6-tiles/0"
            record = json.loads((tile_dir / "attempt-1-ids.json").read_text())
            self.assertEqual(record["params"], client.calls[1][2])
            self.assertEqual(record["timeout"], 180)
            self.assertEqual(record["context"]["tile_id"], "0")
            attempt = json.loads((tile_dir / "attempt-1.json").read_text())
            self.assertEqual(attempt["outcome"], "complete")
            self.assertEqual(attempt["count"], len(attempt["object_ids"]))
            self.assertIn("timestamp_utc", attempt)

    def test_page_resume_reuses_discovery_waits_15_minutes_and_never_overwrites(self):
        for fail_twice in (False, True):
            failures = []
            def hook(url, params, calls):
                if "objectIds" in params and (not failures or fail_twice):
                    failures.append(True)
                    return Response({}, 504)
            with self.subTest(fail_twice=fail_twice), tempfile.TemporaryDirectory() as directory:
                transport, client, clock = self.transport(Path(directory), hook)
                args = (transport, "flowline", 6, EXTENT, refresh.m4a.OUT_FIELDS["flowline"])
                with self.assertRaises(refresh.ResumeLater):
                    refresh.tiled_layer_query(*args)
                before = len(client.calls)
                with self.assertRaises(refresh.ResumeLater):
                    refresh.tiled_layer_query(*args)
                self.assertEqual(len(client.calls), before)
                clock.value += 900
                if fail_twice:
                    with self.assertRaises(refresh.ExternalBlocked):
                        refresh.tiled_layer_query(*args)
                    before = len(client.calls)
                    with self.assertRaises(refresh.ExternalBlocked):
                        refresh.tiled_layer_query(*args)
                    self.assertEqual(len(client.calls), before)
                else:
                    fc, _ = refresh.tiled_layer_query(*args)
                    self.assertEqual(len(fc["features"]), 3)
                    page = Path(directory) / "douglas-co-flowline-pages/page-0001.json"
                    saved = page.read_bytes(), page.stat().st_mtime_ns
                    refresh.tiled_layer_query(*args)
                    self.assertEqual(saved, (page.read_bytes(), page.stat().st_mtime_ns))
                    # Only retry page and final leaf verification were new network requests.
                    self.assertEqual(len(client.calls) - before, 5)

    def test_permanent_identifier_conflict_stops_before_staging(self):
        rows = json.loads(json.dumps(ROWS))
        rows[0]["properties"]["permanent_identifier"] = rows[1]["properties"]["permanent_identifier"]
        with tempfile.TemporaryDirectory() as directory:
            transport, _, _ = self.transport(Path(directory), rows=rows)
            with self.assertRaisesRegex(RuntimeError, "permanent_identifier conflict"):
                refresh.tiled_layer_query(transport, "flowline", 6, EXTENT,
                                           refresh.m4a.OUT_FIELDS["flowline"])

    def test_ids_changing_after_pages_is_fatal(self):
        seen = {}
        def hook(url, params, calls):
            if params.get("returnIdsOnly"):
                key = params["geometry"]
                seen[key] = seen.get(key, 0) + 1
                if seen[key] == 2:
                    return Response({"objectIds": [900]})
        with tempfile.TemporaryDirectory() as directory:
            transport, _, _ = self.transport(Path(directory), hook)
            with self.assertRaisesRegex(RuntimeError, "disagree|changed"):
                refresh.tiled_layer_query(transport, "flowline", 6, EXTENT,
                                           refresh.m4a.OUT_FIELDS["flowline"])



    def test_empty_tile_accepts_explicit_null_ids_but_not_missing_ids(self):
        self.assertEqual(refresh._validated_ids({"objectIds": None}, 0), [])
        with self.assertRaises(RuntimeError):
            refresh._validated_ids({}, 0)

    def test_count_larger_than_ids_is_truncation_not_accepted(self):
        with self.assertRaises(refresh.TileOverflow):
            refresh._validated_ids({"objectIds": [1]}, 2)

    def test_partial_resume_skips_completed_tile_after_interruption(self):
        with tempfile.TemporaryDirectory() as directory:
            transport, client, _ = self.transport(Path(directory))
            original = transport.request
            second = ",".join(map(str, refresh.split_tiles(EXTENT)[1]["extent"]))
            def interrupted(path, url, params, timeout, **kwargs):
                if params.get("geometry") == second:
                    raise KeyboardInterrupt()
                return original(path, url, params, timeout, **kwargs)
            with patch.object(transport, "request", side_effect=interrupted):
                with self.assertRaises(KeyboardInterrupt):
                    self.discover(transport)
            before = len(client.calls)
            ids, _ = self.discover(transport)
            self.assertEqual(ids, [1, 2, 3])
            first = ",".join(map(str, refresh.split_tiles(EXTENT)[0]["extent"]))
            self.assertFalse(any(call[2].get("geometry") == first for call in client.calls[before:]))

    def test_saved_request_makes_no_network_call_even_after_new_transport(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            transport, client, clock = self.transport(root)
            path = root / "response.json"
            value = transport.request(path, refresh.SERVICE, {"f": "json"}, 180)
            resumed = refresh.SavedTransport(client, root, now=clock.now, sleep=clock.sleep)
            self.assertEqual(resumed.request(path, refresh.SERVICE, {"f": "json"}, 180), value)
            self.assertEqual(len(client.calls), 1)
            with self.assertRaisesRegex(RuntimeError, "parameters changed"):
                resumed.request(path, refresh.SERVICE, {"f": "pjson"}, 180)

    def test_http200_server_error_uses_service_policy_and_400_does_not(self):
        for code, error_type in ((504, refresh.ServiceFailure), (400, RuntimeError)):
            def hook(url, params, calls):
                return Response({"error": {"code": code, "message": "fixture"}})
            with tempfile.TemporaryDirectory() as directory:
                transport, client, _ = self.transport(Path(directory), hook)
                with self.assertRaises(error_type):
                    transport.request(Path(directory) / "response.json", refresh.SERVICE, {"f": "json"}, 180)
                self.assertEqual(len(client.calls), 1)

    def test_unsupported_ftype_in_unnamed_raw_row_is_fatal(self):
        rows = json.loads(json.dumps(ROWS))
        rows[0]["properties"].update(gnis_name=None, ftype=999)
        with tempfile.TemporaryDirectory() as directory:
            transport, _, _ = self.transport(Path(directory), rows=rows)
            with self.assertRaisesRegex(ValueError, "ftype"):
                refresh.tiled_layer_query(transport, "flowline", 6, EXTENT,
                                           refresh.m4a.OUT_FIELDS["flowline"])

    def test_changed_discovery_extent_and_cap_are_rejected_on_resume(self):
        with tempfile.TemporaryDirectory() as directory:
            transport, _, _ = self.transport(Path(directory))
            self.discover(transport)
            with self.assertRaisesRegex(RuntimeError, "plan changed"):
                refresh.discover_tiles(transport, 6, (-105, 39, -104, 40), INFO)


    def test_matching_id_lists_above_record_limit_are_accepted_without_subdivision(self):
        ids = list(range(INFO["maxRecordCount"] + 1))
        def hook(url, params, calls):
            if params.get("returnCountOnly"):
                return Response({"count": len(ids)})
            if params.get("returnIdsOnly"):
                return Response({"objectIds": list(reversed(ids))})
        with tempfile.TemporaryDirectory() as directory:
            transport, client, _ = self.transport(Path(directory), hook)
            actual, state = self.discover(transport)
            self.assertEqual(actual, ids)
            self.assertEqual(len(state["tiles"]), 4)
            self.assertTrue(all(tile["status"] == "complete" for tile in state["tiles"].values()))
            self.assertEqual(state["duplicates_removed"], 3 * len(ids))
            self.assertEqual(len(client.calls), 8)
            self.assertEqual(state["raw_leaf_id_count"], 4 * len(ids))

if __name__ == "__main__":
    unittest.main()
