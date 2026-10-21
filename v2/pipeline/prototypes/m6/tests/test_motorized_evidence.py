from datetime import date
import json
from pathlib import Path
import unittest

from motorized_evidence import date_window_status, join_candidate, normalize_record, parse_date_windows, route_number_key

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = json.loads((ROOT / "fixtures" / "mvum-sample.json").read_text())


def mvum_record(raw_dates):
    return {"source_layer": "EDW_MVUM_01/MapServer/1", "attributes": {
        "objectid": 7, "globalid": "{fixture-id}", "rte_cn": "route-canonical-number",
        "id": "000674", "name": "Fixture road", "symbol": "2",
        "motorcycle": "open", "motorcycle_datesopen": raw_dates,
    }}


class MotorizedEvidenceTests(unittest.TestCase):
    def test_fixture_covers_every_distinct_sample_date_value_and_shape(self):
        actual = {r["attributes"]["motorcycle_datesopen"] for r in FIXTURE["records"]}
        expected = {
            "01/01-03/14,04/02-12/31", "01/01-03/14,05/16-12/31",
            "01/01-12/31", "04/02-11/30", "05/16-11/30",
            "06/01-11/30", "12/01-03/14",
        }
        self.assertEqual(actual, expected)
        for raw in actual:
            parsed = parse_date_windows(raw)
            self.assertEqual(parsed["state"], "PARSED")
            self.assertEqual(parsed["raw"], raw)

    def test_year_wrap_and_inclusive_boundaries(self):
        record = normalize_record(mvum_record("12/01-03/14"))
        for day in (date(2026, 12, 1), date(2027, 3, 14)):
            self.assertEqual(date_window_status(record, "motorcycle", day), "INSIDE_WINDOW")
        self.assertEqual(date_window_status(record, "motorcycle", date(2027, 3, 15)), "OUTSIDE_WINDOW")
        self.assertEqual(date_window_status(record, "motorcycle", date(2027, 6, 1)), "OUTSIDE_WINDOW")

    def test_two_windows_are_lossless_and_keep_gap_outside(self):
        raw = "01/01-03/14,05/16-12/31"
        parsed = parse_date_windows(raw)
        self.assertEqual(parsed["raw"], raw)
        self.assertEqual([x["raw"] for x in parsed["windows"]], ["01/01-03/14", "05/16-12/31"])
        record = normalize_record(mvum_record(raw))
        self.assertEqual(date_window_status(record, "motorcycle", date(2026, 3, 14)), "INSIDE_WINDOW")
        self.assertEqual(date_window_status(record, "motorcycle", date(2026, 4, 15)), "OUTSIDE_WINDOW")
        self.assertEqual(date_window_status(record, "motorcycle", date(2026, 5, 16)), "INSIDE_WINDOW")

    def test_single_window_boundary_days(self):
        record = normalize_record(mvum_record("04/02-11/30"))
        self.assertEqual(date_window_status(record, "motorcycle", date(2026, 4, 1)), "OUTSIDE_WINDOW")
        self.assertEqual(date_window_status(record, "motorcycle", date(2026, 4, 2)), "INSIDE_WINDOW")
        self.assertEqual(date_window_status(record, "motorcycle", date(2026, 11, 30)), "INSIDE_WINDOW")
        self.assertEqual(date_window_status(record, "motorcycle", date(2026, 12, 1)), "OUTSIDE_WINDOW")

    def test_unparseable_and_missing_windows(self):
        raw = "spring through fall"
        self.assertEqual(parse_date_windows(raw), {"raw": raw, "state": "UNPARSEABLE", "windows": []})
        self.assertEqual(date_window_status(normalize_record(mvum_record(raw)), "motorcycle", date(2026, 6, 1)), "UNPARSEABLE")
        self.assertEqual(date_window_status(normalize_record(mvum_record(None)), "motorcycle", date(2026, 6, 1)), "NO_WINDOW_STATED")
        self.assertEqual(date_window_status(normalize_record(mvum_record(None)), "other", date(2026, 6, 1)), "NO_WINDOW_STATED")

    def test_zero_padded_and_unpadded_route_number_join_candidate(self):
        management = {"source_layer": "EDW_TrailNFSPublishWithDataStatus_01/MapServer/0", "id": "trail-1",
                      "trail_number": "674", "activities": {"motorcycle": {"managed": "", "accpt": "", "disc": "", "restricted": ""}}}
        self.assertEqual(route_number_key("000674"), route_number_key("674"))
        candidate = join_candidate(mvum_record("05/16-11/30"), management)
        self.assertEqual(candidate["match_basis"], "normalized_route_number_candidate")
        self.assertEqual(candidate["mvum_route_number_raw"], "000674")
        self.assertEqual(candidate["trail_route_number_raw"], "674")
        self.assertEqual(candidate["source_claims"][0]["source_feature"]["objectid"], 7)
        self.assertEqual(candidate["source_claims"][1]["source_feature"]["id"], "trail-1")

    def test_conflicting_source_claims_are_preserved_without_resolution(self):
        management = {"source_layer": "EDW_TrailNFSPublishWithDataStatus_01/MapServer/0", "id": "trail-1",
                      "trail_number": "674", "activities": {"motorcycle": {"managed": "08/01-08/31", "accpt": None, "disc": None, "restricted": None}}}
        candidate = join_candidate(mvum_record("12/01-03/14"), management)
        claims = candidate["source_claims"]
        self.assertEqual(claims[0]["vehicle_designations"]["motorcycle"]["designation_raw"], "open")
        self.assertEqual(claims[0]["vehicle_designations"]["motorcycle"]["dates_open"]["raw"], "12/01-03/14")
        self.assertEqual(claims[1]["activities"]["motorcycle"]["managed"], "08/01-08/31")
        self.assertIsNone(claims[1]["activities"]["motorcycle"]["restricted"])
        self.assertEqual(candidate["current_condition"], "unknown")

    def test_sources_and_unknown_current_condition_stay_separate(self):
        normalized = normalize_record(mvum_record("06/01-11/30"))
        self.assertEqual(len(normalized["source_claims"]), 1)
        self.assertEqual(normalized["current_condition"], "unknown")
        self.assertIsNone(join_candidate(mvum_record("06/01-11/30"), {"trail_number": "999"}))

    def test_serialized_evidence_has_no_boolean_verdicts(self):
        normalized = normalize_record(mvum_record("01/01-12/31"), {"trail_number": "674", "activities": {}})

        def inspect(value):
            if isinstance(value, bool):
                self.fail("payload contains a boolean verdict")
            if isinstance(value, dict):
                for child in value.values():
                    inspect(child)
            elif isinstance(value, list):
                for child in value:
                    inspect(child)

        inspect(normalized)
        self.assertEqual(normalized["current_condition"], "unknown")


if __name__ == "__main__":
    unittest.main()
