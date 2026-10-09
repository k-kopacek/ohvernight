"""Offline tests pin five confirmed pipeline risks without changing production code.

Each expected failure expresses the smallest desirable safety property; the test
runner's expected-failure result documents that main does not yet satisfy it.
"""
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import build_display
import fetch_trails
from lib.arcgis_client import ArcGISQueryError, get_json, new_session, query_layer_geojson
from lib.common import clip_geometry
from shapely.geometry import box


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


class PipelineTechnicalDebtExpectedFailures(unittest.TestCase):
    @unittest.expectedFailure
    def test_retry_fanout_has_one_bounded_attempt_budget(self):
        """EXPECTED FAILURE: adapter and JSON layers compound one logical request."""
        adapter_attempts = new_session().get_adapter("https://").max_retries.total + 1
        fake = ArcGISErrorSession()
        with patch("lib.arcgis_client.time.sleep"):
            with self.assertRaises(ArcGISQueryError):
                get_json(fake, "https://example.invalid/layer", {})
        # HTTPAdapter permits 3 attempts and get_json makes 3 calls on its own:
        # a single logical request can therefore reach the transport up to 9 times.
        self.assertLessEqual(adapter_attempts * fake.calls, 3,
                             "retry layers multiply a request beyond the single run budget")

    @unittest.expectedFailure
    def test_stable_object_ids_detect_changed_attributes(self):
        """EXPECTED FAILURE: identical ID sets do not flag a renamed source row."""
        saved_snapshot = {"objectid": 7, "trail_name": "ORIGINAL NAME"}
        result = query_layer_geojson(
            "https://example.invalid/MapServer", 0, (0, 0, 1, 1),
            session=SnapshotDriftSession(), page_size=10,
        )
        current = result["features"][0]["properties"]
        self.assertEqual(current.get("trail_name"), saved_snapshot["trail_name"],
                         "changed name under a stable object ID needs a drift report")

    @unittest.expectedFailure
    def test_geometry_repair_reports_when_make_valid_changes_topology(self):
        """EXPECTED FAILURE: clip_geometry repairs invalid input with no audit result."""
        invalid_bowtie = {
            "type": "Polygon",
            "coordinates": [[[0, 0], [2, 2], [0, 2], [2, 0], [0, 0]]],
        }
        result = clip_geometry(invalid_bowtie, box(-1, -1, 3, 3))
        self.assertIn("repair_report", result,
                      "geometry repair needs a caller-visible changed/unchanged diagnostic")

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
