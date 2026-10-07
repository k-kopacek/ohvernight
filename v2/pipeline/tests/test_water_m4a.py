import copy
import tempfile
import sys
import unittest
from pathlib import Path

V2 = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(V2 / "pipeline" / "scripts"))

from lib.water import (  # noqa: E402
    SOURCE_FIELDS, attach_legacy_ids, classify, ensure_supported_ftype, ensure_unique_feature_ids, enrich_properties, feature_id, legacy_geometry_matches,
    normalize_source_fields, splice_layer, support_bridges, support_gap_boxes,
    water_display_config,
)
from apply_m4a_water import write_region_manifest  # noqa: E402


class WaterM4ATests(unittest.TestCase):
    def test_waterbody_elevation_mapping_preserves_the_source_value_in_metres(self):
        self.assertEqual(SOURCE_FIELDS["waterbody"]["elevation_m"], "elevation")
        values = normalize_source_fields("waterbody", {
            "permanent_identifier": "water-1", "ftype": 390, "fcode": 39004,
            "elevation": 3071.1648,
        })
        self.assertEqual(values["elevation_m"], 3071.1648)
        self.assertNotIn("elevation_ft", values)

    def test_manifest_update_preserves_every_non_water_line(self):
        text = ('{\n  "sources": {\n    "usgs_nhd": {"scope": "old"},\n'
                '    "other": {"scope": "untouched"}\n  },\n  "layers": [\n'
                '    {"id": "other", "fields": {"source": ["keep"]}},\n'
                '    {"id": "water", "fields": {"source": [], "derived": []}}\n  ]\n}\n')
        manifest = {
            "sources": {"usgs_nhd": {"scope": "new"}},
            "layers": [{"id": "other", "fields": {"source": ["keep"]}},
                       {"id": "water", "fields": {"source": ["source_id"], "derived": ["source_layer"]}}],
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "region.json"
            path.write_text(text)
            write_region_manifest(path, manifest, {"water"})
            updated = path.read_text()
        self.assertIn('    "other": {"scope": "untouched"}', updated)
        self.assertIn('    {"id": "other", "fields": {"source": ["keep"]}},', updated)
        self.assertIn('"source": ["source_id"]', updated)

    def test_feature_id_sanitizes_but_source_id_is_preserved(self):
        self.assertEqual(feature_id("{A0-b_C}"), "nhd-A0-bC")
        values = normalize_source_fields("flowline", {
            "permanent_identifier": "{A0-b_C}", "gnis_id": "0012", "ftype": 460, "fcode": 46006,
        })
        self.assertEqual(values["source_id"], "{A0-b_C}")
        self.assertEqual(values["gnis_id"], "0012")
        self.assertNotIn("area_sqkm", values)
        self.assertNotIn("elevation_m", values)

    def test_missing_source_id_stops_normalization(self):
        with self.assertRaisesRegex(ValueError, "no permanent source_id"):
            normalize_source_fields("flowline", {"ftype": 460, "fcode": 46006})

    def test_normalized_water_feature_keeps_source_fields_and_omits_grouping(self):
        source = {"permanent_identifier": "{A0-b_C}", "gnis_id": "0012", "gnis_name": "River",
                  "ftype": 460, "fcode": 46006, "reachcode": "123456", "lengthkm": 2.5,
                  "visibilityfilter": 3, "wbarea_permanent_identifier": "wb-1", "fdate": "2023-01-01T00:00:00Z"}
        result = enrich_properties("flowline", source, {"source_url": "https://agency.example"},
                                   ["old-id"], support_for="0012")
        self.assertEqual(result["id"], "nhd-A0-bC")
        self.assertEqual(result["source_id"], "{A0-b_C}")
        self.assertEqual(result["name"], "River")
        self.assertEqual(result["source_namespace"], "usgs_nhd")
        self.assertEqual(result["source_layer"], "flowline")
        self.assertEqual(result["legacy_ids"], ["old-id"])
        self.assertEqual(result["support_for"], "0012")
        self.assertEqual(result["support_reason"], "bridges_named_parts")
        self.assertNotIn("group_id", result)
        self.assertNotIn("manager", result)

    def test_sanitization_collision_stops_build(self):
        features = [{"properties": {"id": feature_id(value)}} for value in ("A{B}", "AB")]
        with self.assertRaisesRegex(ValueError, "duplicate water feature ID"):
            ensure_unique_feature_ids(features)

    def test_fixed_water_class_and_hydro_category_tables(self):
        vectors = {
            460: "stream", 558: "artificial_path", 336: "canal_ditch", 428: "pipeline",
            334: "connector", 390: "lake_pond", 436: "reservoir", 466: "swamp_marsh", 999: "other",
        }
        for ftype, expected in vectors.items():
            self.assertEqual(classify(ftype, 39004)[0], expected)
        for fcode in (39004, 39009, 39010, 39011, 39012, 43615, 43621):
            self.assertEqual(classify(436, fcode)[1], "perennial")
        for fcode in (46003, 39001, 39005, 39006, 43614):
            self.assertEqual(classify(436, fcode)[1], "intermittent")
        self.assertEqual(classify(460, 46007)[1], "ephemeral")
        self.assertEqual(classify(460, 43619)[1], "unknown")

    def test_known_unknown_hydro_codes_are_valid_but_unknown_ftype_stops(self):
        for ftype, fcode, expected_class in (
                (558, 55800, "artificial_path"), (336, 33600, "canal_ditch"),
                (436, 43619, "reservoir")):
            self.assertEqual(classify(ftype, fcode), (expected_class, "unknown"))
            self.assertEqual(ensure_supported_ftype(ftype), expected_class)
        with self.assertRaisesRegex(ValueError, "unsupported water ftype 999"):
            ensure_supported_ftype(999)

    def test_water_display_config_contains_fixed_reservoir_tables_and_m4b_placeholders(self):
        config = water_display_config()
        self.assertEqual(config["reservoir_eligible_fcodes"], [43600, 43613, 43615, 43617, 43618, 43619, 43621])
        self.assertEqual(config["reservoir_ineligible_fcodes"], [43601, 43603, 43604, 43605, 43606, 43607, 43608,
                                                                  43609, 43610, 43611, 43612, 43614, 43623, 43624,
                                                                  43625, 43626])
        self.assertFalse(set(config["reservoir_eligible_fcodes"]) & set(config["reservoir_ineligible_fcodes"]))
        self.assertEqual(config["unnamed_waterbody_min_area_sqkm"], 0.02)
        self.assertEqual(set(config["non_claim_hosts"]),
                         {"facebook.com", "reddit.com", "youtube.com", "instagram.com",
                          "alltrails.com", "wikiloc.com", "tripadvisor.com"})
        self.assertEqual({region: [row["gnis_id"] for row in rows]
                          for region, rows in config["expected_major_rivers"].items()},
                         {"aspen": ["00174812", "00180078", "00180007", "00175217", "00180061"],
                          "douglas-co": ["00201759", "00183363", "00185069", "00185068", "00181657"]})
        self.assertEqual(config["pending_external_source_refresh"]["state"],
                         "PENDING_EXTERNAL_SOURCE_REFRESH")
        self.assertEqual(config["pending_external_source_refresh"]["gnis_id"], "00201759")
        self.assertEqual([row["fcode"] for row in config["snapshot_unknown_fcodes"]],
                         [33400, 33600, 39000, 42800, 42802, 42803, 42807, 42813,
                          43601, 43612, 43613, 43619, 43624, 46600, 55800])
        ftype_by_fcode = {33400: 334, 33600: 336, 39000: 390, 42800: 428, 42802: 428,
                          42803: 428, 42807: 428, 42813: 428, 43601: 436, 43612: 436,
                          43613: 436, 43619: 436, 43624: 436, 46600: 466, 55800: 558}
        for row in config["snapshot_unknown_fcodes"]:
            self.assertEqual(classify(ftype_by_fcode[row["fcode"]], row["fcode"])[1], "unknown")

    def test_legacy_matching_uses_exact_geometry_not_row_position(self):
        def feature(ident, geometry):
            return {"type": "Feature", "geometry": geometry, "properties": {"id": ident}}
        old = [feature("old-first", {"type": "LineString", "coordinates": [[0, 0], [1, 1]]}),
               feature("old-second", {"type": "LineString", "coordinates": [[2, 2], [3, 3]]})]
        new = [feature("new-first", {"type": "LineString", "coordinates": [[9, 9], [10, 10]]}),
               feature("new-second", {"type": "LineString", "coordinates": [[2, 2], [3, 3]]})]
        matches, unmatched_old, unmatched_new = legacy_geometry_matches(old, new)
        self.assertEqual(matches, {"new-second": ["old-second"]})
        self.assertEqual(unmatched_old, ["old-first"])
        self.assertEqual(unmatched_new, ["new-first"])

    def test_legacy_matching_rejects_ambiguous_duplicate_geometry(self):
        geom = {"type": "Point", "coordinates": [1, 1]}
        old = [{"geometry": geom, "properties": {"id": "old-1"}},
               {"geometry": geom, "properties": {"id": "old-2"}}]
        new = [{"geometry": geom, "properties": {"id": "new-1"}}]
        matches, unmatched_old, unmatched_new = legacy_geometry_matches(old, new)
        self.assertEqual(matches, {})
        self.assertEqual(unmatched_old, ["old-1", "old-2"])
        self.assertEqual(unmatched_new, ["new-1"])

    def test_legacy_ids_survive_a_second_fetch(self):
        geometry = {"type": "LineString", "coordinates": [[0, 0], [1, 1]]}
        old = [{"type": "Feature", "geometry": geometry,
                "properties": {"id": "pre-m4-row"}}]
        first = [{"type": "Feature", "geometry": copy.deepcopy(geometry),
                  "properties": {"id": "nhd-current", "legacy_ids": []}}]
        attach_legacy_ids(old, first)
        self.assertEqual(first[0]["properties"]["legacy_ids"], ["pre-m4-row"])
        second = copy.deepcopy(first)
        attach_legacy_ids(first, second)
        self.assertEqual(second[0]["properties"]["legacy_ids"], first[0]["properties"]["legacy_ids"])

    def test_legacy_ids_survive_geometry_change_when_id_is_stable(self):
        old = [{"type": "Feature", "geometry": {"type": "LineString", "coordinates": [[0, 0], [1, 1]]},
                "properties": {"id": "nhd-current", "legacy_ids": ["pre-m4-row"]}}]
        new = [{"type": "Feature", "geometry": {"type": "LineString", "coordinates": [[0, 0], [2, 2]]},
                "properties": {"id": "nhd-current", "legacy_ids": []}}]
        attach_legacy_ids(old, new)
        self.assertEqual(new[0]["properties"]["legacy_ids"], ["pre-m4-row"])

    def test_legacy_ids_never_include_their_own_feature_id(self):
        geometry = {"type": "LineString", "coordinates": [[0, 0], [1, 1]]}
        old = [{"type": "Feature", "geometry": geometry,
                "properties": {"id": "nhd-current", "legacy_ids": ["pre-m4-row", "nhd-current"]}}]
        new = [{"type": "Feature", "geometry": copy.deepcopy(geometry),
                "properties": {"id": "nhd-current", "legacy_ids": []}}]
        attach_legacy_ids(old, new)
        self.assertEqual(new[0]["properties"]["legacy_ids"], ["pre-m4-row"])

    def test_legacy_id_cannot_be_assigned_to_two_new_features(self):
        old = [{"type": "Feature", "geometry": {"type": "LineString", "coordinates": [[0, 0], [1, 1]]},
                "properties": {"id": "nhd-old-a", "legacy_ids": ["pre-m4-row"]}},
               {"type": "Feature", "geometry": {"type": "LineString", "coordinates": [[2, 2], [3, 3]]},
                "properties": {"id": "nhd-old-b", "legacy_ids": ["pre-m4-row"]}}]
        new = [{"type": "Feature", "geometry": {"type": "LineString", "coordinates": [[0, 0], [1, 1]]},
                "properties": {"id": "nhd-new-a", "legacy_ids": []}},
               {"type": "Feature", "geometry": {"type": "LineString", "coordinates": [[2, 2], [3, 3]]},
                "properties": {"id": "nhd-new-b", "legacy_ids": []}}]
        with self.assertRaisesRegex(ValueError, "legacy water ID pre-m4-row would be assigned to multiple features"):
            attach_legacy_ids(old, new)

    def test_support_bridge_is_kept_but_non_bridge_is_not(self):
        def line(ident, coords, name, gnis_id="42", water_class="stream"):
            return {"type": "Feature", "geometry": {"type": "LineString", "coordinates": coords},
                    "properties": {"id": ident, "name": name, "gnis_id": gnis_id, "water_class": water_class}}
        named = [line("left", [[-0.001, 39], [0, 39]], "River"),
                 line("right", [[0.001, 39], [0.002, 39]], "River")]
        bridge = line("bridge", [[0, 39], [0.001, 39]], None, gnis_id=None)
        stray = line("stray", [[20, 20], [21, 20]], None, gnis_id=None)
        result = support_bridges(named, [bridge, stray], max_gap_m=250, tolerance_m=0.01)
        self.assertEqual([(feature["properties"]["id"], gnis_id) for feature, gnis_id in result], [("bridge", "42")])

    def test_support_gap_uses_six_decimal_endpoints_and_300m_box(self):
        named = [
            {"type": "Feature", "geometry": {"type": "LineString", "coordinates": [[-0.001, 39], [0, 39]]},
             "properties": {"id": "left", "gnis_id": "42"}},
            {"type": "Feature", "geometry": {"type": "LineString", "coordinates": [[0.001, 39], [0.002, 39]]},
             "properties": {"id": "right", "gnis_id": "42"}},
        ]
        gaps = support_gap_boxes(named)
        self.assertEqual(len(gaps), 1)
        self.assertEqual(gaps[0][0], "42")
        west, south, east, north = gaps[0][1]
        self.assertLess(east - west, 0.004)
        self.assertGreater(east - west, 0.002)
        self.assertLess(north - south, 0.004)
        self.assertGreater(north - south, 0.002)

    def test_splicing_replaces_only_selected_layer(self):
        original = {"layers": {"hydrology": {"features": [1]}, "roads": {"features": [2]},
                                "land": {"features": [3]}}}
        before = copy.deepcopy(original)
        updated = splice_layer(original, "hydrology", {"features": [9]})
        self.assertEqual(updated["layers"]["hydrology"], {"features": [9]})
        self.assertEqual(updated["layers"]["roads"], before["layers"]["roads"])
        self.assertEqual(updated["layers"]["land"], before["layers"]["land"])


if __name__ == "__main__":
    unittest.main()
