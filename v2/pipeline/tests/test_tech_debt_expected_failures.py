"""Offline tests pin five confirmed pipeline risks without changing production code.

Each expected failure expresses the smallest desirable safety property; the test
runner's expected-failure result documents that main does not yet satisfy it.
"""
import json
import logging
from pathlib import Path
import sys
import tempfile
import unittest
import warnings
from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import build_display
import fetch_trails
from lib.arcgis_client import get_json, new_session
from lib.common import clip_geometry
from shapely.geometry import box
from shapely.geometry import shape
import requests
from requests.adapters import HTTPAdapter
from urllib3 import HTTPSConnectionPool, HTTPResponse
from urllib3.exceptions import NewConnectionError


class JsonResponse:
    def __init__(self, payload):
        self.payload = payload

    def raise_for_status(self):
        pass

    def json(self):
        return self.payload


class ArcGISErrorSession:
    """Synthetic HTTP-200 ArcGIS errors; no adapter or network is invoked."""
    def __init__(self):
        self.calls = 0

    def get(self, url, params, timeout):
        self.calls += 1
        return JsonResponse({"error": {"code": 503, "message": "synthetic service error"}})


class SnapshotDriftSession:
    """Stable IDs with a changed attribute in the synthetic current snapshot."""
    def __init__(self):
        self.feature = {
            "type": "Feature",
            "id": 7,
            "properties": {"OBJECTID": 7, "TRAIL_NAME": "RENAMED UNDER SAME ID"},
            "geometry": {"type": "LineString", "coordinates": [[0.1, 0.1], [0.2, 0.2]]},
        }

    def get(self, url, params, timeout):
        if not url.endswith("/query"):
            return JsonResponse({
                "type": "Feature Layer",
                "maxRecordCount": 10,
                "fields": [
                    {"name": "OBJECTID", "type": "esriFieldTypeOID"},
                    {"name": "TRAIL_NAME", "type": "esriFieldTypeString"},
                ],
            })
        if params.get("returnCountOnly"):
            return JsonResponse({"count": 1})
        if params.get("returnIdsOnly"):
            return JsonResponse({"objectIds": [7]})
        return JsonResponse({"type": "FeatureCollection", "features": [self.feature]})


class CountingTransportPool(HTTPSConnectionPool):
    """In-memory urllib3 pool that counts each transport attempt."""
    def __init__(self, failure):
        super().__init__("example.invalid")
        self.failure = failure
        self.transport_sends = 0

    def _validate_conn(self, conn):
        # The pool never opens a socket; _make_request supplies the response.
        pass

    def _make_request(self, conn, method, url, **kwargs):
        self.transport_sends += 1
        if self.failure == "connection":
            raise NewConnectionError(conn, "synthetic connection failure")
        return HTTPResponse(
            body=b'{"error":{"code":503,"message":"synthetic unavailable"}}',
            status=503,
            headers={"Content-Type": "application/json"},
            preload_content=False,
            reason="Synthetic Service Unavailable",
        )


class CountingHTTPAdapter(HTTPAdapter):
    """Real HTTPAdapter retry logic over a counting, socket-free pool."""
    def __init__(self, failure, max_retries):
        super().__init__(max_retries=max_retries)
        self.pool = CountingTransportPool(failure)
        self.adapter_send_calls = 0

    def get_connection_with_tls_context(self, request, verify, proxies=None, cert=None):
        return self.pool

    def send(self, request, **kwargs):
        self.adapter_send_calls += 1
        return super().send(request, **kwargs)


class PipelineTechnicalDebtExpectedFailures(unittest.TestCase):
    def test_transport_failures_use_one_adapter_budget_without_json_retry_fanout(self):
        """Pin actual transport attempts for status and connection failures."""
        measurements = {}
        for failure, expected_exception in (
            ("status", requests.exceptions.RetryError),
            ("connection", requests.exceptions.ConnectionError),
        ):
            session = new_session()
            configured_retries = session.get_adapter("https://").max_retries
            adapter = CountingHTTPAdapter(failure, configured_retries)
            session.mount("https://", adapter)
            with patch("lib.arcgis_client.time.sleep"):
                with self.assertRaises(expected_exception):
                    get_json(session, "https://example.invalid/layer", {})
            measurements[failure] = adapter.pool.transport_sends
            self.assertEqual(adapter.pool.transport_sends, configured_retries.total + 1)
            self.assertEqual(adapter.adapter_send_calls, 1,
                             "get_json must not multiply a transport exception")
        self.assertEqual(measurements, {"status": 3, "connection": 3})

    @unittest.expectedFailure
    def test_real_trail_publish_reports_attribute_change_under_stable_id(self):
        """EXPECTED FAILURE: real refresh replaces a renamed ID without a drift signal."""
        row = lambda name: {
            "type": "Feature", "id": 7,
            "properties": {"OBJECTID": 7, "TRAIL_NAME": name, "TRAIL_NO": "007"},
            "geometry": {"type": "LineString", "coordinates": [[-106.2, 39.2], [-106.1, 39.3]]},
        }
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "v2"
            (root / "pipeline" / "scripts").mkdir(parents=True)
            (root / "trails.geojson").write_text('{"old":"snapshot"}')
            published_path = root / "trails.geojson"
            outputs = []
            logs = []
            with patch.object(fetch_trails, "__file__", str(root / "pipeline" / "scripts" / "fetch_trails.py")), \
                 patch.object(fetch_trails, "query_layer_geojson") as query:
                for name in ("ORIGINAL NAME", "RENAMED UNDER SAME ID"):
                    query.return_value = {"features": [row(name)]}
                    output = StringIO()
                    with redirect_stdout(output):
                        result = fetch_trails.main()
                    outputs.append(json.loads(published_path.read_text()))
                    logs.append(output.getvalue())
                    self.assertIsNone(result)
            before, after = outputs
            self.assertEqual(before["features"][0]["properties"]["id"],
                             after["features"][0]["properties"]["id"])
            self.assertEqual(before["features"][0]["properties"]["name"], "ORIGINAL NAME")
            self.assertEqual(after["features"][0]["properties"]["name"], "RENAMED UNDER SAME ID")
            drift_signal = any(
                term in logs[1].lower()
                for term in ("attribute changed", "attribute drift", "changed record", "snapshot diff")
            )
            self.assertTrue(drift_signal,
                            "second real publish overwrote the changed name without a drift report, log, or return signal")

    @unittest.expectedFailure
    def test_geometry_repair_change_has_no_warning_log_or_exception_signal(self):
        """EXPECTED FAILURE: clip_geometry changes invalid geometry without a diagnostic."""
        invalid_bowtie = {
            "type": "Polygon",
            "coordinates": [[[0, 0], [2, 2], [0, 2], [2, 0], [0, 0]]],
        }
        original = shape(invalid_bowtie)
        emitted_logs = []
        handler = logging.Handler()
        handler.emit = lambda record: emitted_logs.append(record)
        root_logger = logging.getLogger()
        root_logger.addHandler(handler)
        try:
            with warnings.catch_warnings(record=True) as emitted_warnings:
                warnings.simplefilter("always")
                result = clip_geometry(invalid_bowtie, box(-1, -1, 3, 3))
        finally:
            root_logger.removeHandler(handler)
        repaired = shape(result)
        coordinate_count = lambda geom: sum(
            len(poly.exterior.coords) + sum(len(ring.coords) for ring in poly.interiors)
            for poly in ([geom] if geom.geom_type == "Polygon" else geom.geoms)
            if poly.geom_type == "Polygon"
        )
        changed = original.area != repaired.area or coordinate_count(original) != coordinate_count(repaired)
        self.assertTrue(changed, "synthetic bow-tie must change after the real clip/repair path")
        self.assertEqual(emitted_warnings, [], "repair must not warn in this code path")
        self.assertEqual(emitted_logs, [], "repair must not log in this code path")
        self.assertTrue(emitted_warnings or emitted_logs,
                        "make_valid changed the output but produced no warning or log diagnostic")

    @unittest.expectedFailure
    def test_failed_display_build_preserves_the_previous_directory(self):
        """EXPECTED FAILURE: a second artifact write can leave a mixed display set."""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            output = root / "regions" / "fixture" / "display"
            output.mkdir(parents=True)
            (output / "first.geojson").write_bytes(b"old-first")
            (output / "coverage.geojson").write_bytes(b"old-coverage")
            before = {p.name: p.read_bytes() for p in output.iterdir()}
            manifest = {"layers": [{"id": "first", "format": "feature_collection", "status_ref": None}]}
            first = ({"type": "FeatureCollection", "features": []}, {
                "path": "regions/fixture/display/first.geojson", "layer_id": "first", "feature_count": 0,
            })
            coverage = ({"type": "FeatureCollection", "features": []}, {
                "path": "regions/fixture/display/coverage.geojson", "layer_id": "coverage", "feature_count": 0,
            })
            original_write = Path.write_bytes
            writes = 0

            def fail_on_second_write(path, value):
                nonlocal writes
                writes += 1
                if writes == 2:
                    raise OSError("synthetic interrupted publication")
                return original_write(path, value)

            with patch.object(build_display, "_read_json", return_value=manifest), \
                 patch.object(build_display, "build_layer", return_value=first), \
                 patch.object(build_display, "build_coverage", return_value=coverage), \
                 patch.object(Path, "write_bytes", fail_on_second_write):
                with self.assertRaisesRegex(OSError, "synthetic interrupted"):
                    build_display.build_region("fixture", root=root, write=True)
            after = {p.name: p.read_bytes() for p in output.iterdir()}
            self.assertEqual(after, before,
                             "publication should stage all artifacts before replacing the current set")

    @unittest.expectedFailure
    def test_trail_fetch_requires_each_per_activity_use_attribute(self):
        """EXPECTED FAILURE: renamed/missing use attributes currently normalize to null."""
        expected_fields = {"objectid", "trail_name", "trail_no"}
        expected_fields.update(
            f"{prefix}_{suffix}"
            for prefix in fetch_trails.ACTIVITIES.values()
            for suffix in ("managed", "accpt", "disc", "restricted")
        )
        with patch.object(fetch_trails, "query_layer_geojson", return_value={"features": []}) as query:
            with self.assertRaisesRegex(ValueError, "Empty trail pilot"):
                fetch_trails.main()
        requested = {value.lower() for value in query.call_args.kwargs["required_fields"]}
        self.assertTrue(expected_fields.issubset(requested),
                        "query must reject any missing activity field before normalization can turn it into null")


if __name__ == "__main__":
    unittest.main()
