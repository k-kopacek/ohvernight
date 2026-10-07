"""Synthetic offline fixtures for M4-B water selection, groups and validators."""
import copy
import json
import random
import subprocess
import sys
import unittest
from pathlib import Path

V2 = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(V2 / "pipeline" / "scripts"))

from lib.water import (  # noqa: E402
    classify, group_flowlines, geodesic_length_km, select_water_features,
    validate_expected_major_rivers, water_display_config,
)
from lib.region_contract import (ContractError, _json_pointer,
                                 _validate_water_review,
                                 REGION_MANIFEST_SCHEMA,
                                 _validate_water_group_index,
                                 validate_m4b_water_layer)  # noqa: E402
from jsonschema import Draft202012Validator  # noqa: E402
from build_display import build_selection_report, build_water_report  # noqa: E402


CONFIG = water_display_config()


def water_feature(ident="water-1", *, layer="waterbody", ftype=390, fcode=39004,
                  name=None, gnis="", area=None, coords=None, **extra):
    if coords is None:
        coords = [[0, 0], [1, 0]] if layer == "flowline" else [
            [[0, 0], [1, 0], [1, 1], [0, 0]]]
    geometry_type = "LineString" if layer == "flowline" else "Polygon"
    props = {"id": ident, "source_id": ident, "source_namespace": "usgs_nhd",
             "source_layer": layer, "ftype": ftype, "fcode": fcode,
             "name": name, "gnis_id": gnis, "area_sqkm": area,
             "length_km": 1.0, "water_class": "", "hydro_category": "",
             "legacy_ids": [], "evidence": {"source_url": "https://example.test"}}
    props["water_class"], props["hydro_category"] = classify(ftype, fcode, CONFIG)
    props.update(extra)
    return {"type": "Feature", "geometry": {"type": geometry_type, "coordinates": coords},
            "properties": props}


def decisions(features, *, inclusions=(), exclusions=(), config=None):
    result = select_water_features(features, config or CONFIG,
                                   {"inclusions": list(inclusions), "exclusions": list(exclusions)})
    return {row["feature"]["properties"]["id"]: row for row in result}


class WaterSelectionFixtures(unittest.TestCase):
    def test_stream_eligibility_rows_require_named_perennial_and_gnis(self):
        features = [
            water_feature("perennial", layer="flowline", ftype=460, fcode=46006,
                          name="River", gnis="001"),
            water_feature("unnamed", layer="flowline", ftype=460, fcode=46006, gnis="001"),
            water_feature("empty-gnis", layer="flowline", ftype=460, fcode=46006, name="River"),
            water_feature("intermittent", layer="flowline", ftype=460, fcode=46003,
                          name="River", gnis="001"),
            water_feature("ephemeral", layer="flowline", ftype=460, fcode=46007,
                          name="River", gnis="001"),
            water_feature("unknown", layer="flowline", ftype=460, fcode=46000,
                          name="River", gnis="001"),
            water_feature("canal", layer="flowline", ftype=336, fcode=33600,
                          name="River", gnis="001"),
            water_feature("pipeline", layer="flowline", ftype=428, fcode=42803,
                          name="River", gnis="001"),
            water_feature("connector", layer="flowline", ftype=334, fcode=33400,
                          name="River", gnis="001"),
            water_feature("artificial", layer="flowline", ftype=558, fcode=55800,
                          name="River", gnis="001"),
            water_feature("area", layer="area", ftype=460, fcode=46006,
                          name="River", gnis="001"),
            water_feature("swamp", ftype=466, fcode=46600, name="River", area=1),
            water_feature("other", ftype=999, fcode=99900, name="River", area=1),
        ]
        got = decisions(features)
        self.assertTrue(got["perennial"]["eligible"])
        for ident in ("unnamed", "empty-gnis", "intermittent", "ephemeral", "unknown", "canal",
                      "pipeline", "connector", "artificial", "area", "swamp", "other"):
            with self.subTest(ident=ident):
                self.assertFalse(got[ident]["eligible"])

    def test_named_perennial_lakes_and_unnamed_threshold_edges(self):
        features = [
            water_feature("named-tiny", name="Pond", area=0.0001),
            water_feature("unnamed-below", area=0.019999999),
            water_feature("unnamed-at", area=0.02),
            water_feature("unnamed-above", area=0.020000001),
            water_feature("unnamed-null", area=None),
        ]
        got = decisions(features)
        self.assertTrue(got["named-tiny"]["eligible"])
        self.assertFalse(got["unnamed-below"]["eligible"])
        self.assertTrue(got["unnamed-at"]["eligible"])
        self.assertTrue(got["unnamed-above"]["eligible"])
        self.assertFalse(got["unnamed-null"]["eligible"])

    def test_intermediate_and_unknown_lakes_are_not_selected_without_review(self):
        got = decisions([
            water_feature("intermittent", fcode=39001, name="Lake", area=2),
            water_feature("not-stated", fcode=39000, name="Lake", area=2),
        ])
        self.assertFalse(got["intermittent"]["eligible"])
        self.assertFalse(got["not-stated"]["eligible"])

    def test_reservoir_codes_follow_the_fixed_eligible_and_ineligible_tables(self):
        eligible = CONFIG["reservoir_eligible_fcodes"]
        ineligible = CONFIG["reservoir_ineligible_fcodes"]
        features = [water_feature(f"e-{code}", ftype=436, fcode=code, name="Reservoir")
                    for code in eligible]
        features += [water_feature(f"i-{code}", ftype=436, fcode=code, name="Reservoir")
                     for code in ineligible]
        got = decisions(features)
        self.assertTrue(all(got[f"e-{code}"]["eligible"] for code in eligible))
        self.assertTrue(all(not got[f"i-{code}"]["eligible"] for code in ineligible))

    def test_unknown_category_eligible_reservoir_is_not_promoted_to_perennial(self):
        feature = water_feature("reservoir", ftype=436, fcode=43619, name="Reservoir")
        result = decisions([feature])["reservoir"]
        self.assertTrue(result["eligible"])
        self.assertEqual(result["hydro_category"], "unknown")

    def test_unknown_category_unnamed_reservoir_uses_exact_threshold(self):
        features = [water_feature(f"r-{area}", ftype=436, fcode=43619, area=area)
                    for area in (0.019999999, 0.02, 0.020000001)]
        got = decisions(features)
        self.assertEqual([got[f"r-{area}"]["eligible"] for area in (0.019999999, 0.02, 0.020000001)],
                         [False, True, True])

    def test_reviewed_inclusion_overrides_only_allowed_waterbody_categories(self):
        features = [water_feature("intermittent", fcode=39001, name="Lake"),
                    water_feature("not-stated", fcode=39000, name="Pond"),
                    water_feature("stream", layer="flowline", ftype=460, fcode=46003,
                                  name="River", gnis="001")]
        inclusion = {"feature_id": "intermittent", "reason_code": "reviewed_intermittent_waterbody"}
        got = decisions(features, inclusions=[inclusion])
        self.assertTrue(got["intermittent"]["eligible"])
        self.assertFalse(got["not-stated"]["eligible"])
        self.assertFalse(got["stream"]["eligible"])
        unknown = decisions([features[1]], inclusions=[
            {"feature_id": "not-stated", "reason_code": "reviewed_intermittent_waterbody"}])
        self.assertTrue(unknown["not-stated"]["eligible"])

    def test_reviewed_inclusion_is_limited_to_the_three_specified_waterbody_cases(self):
        allowed = [water_feature("lake-intermittent", fcode=39001, name="Lake"),
                   water_feature("lake-unstated", fcode=39000, name="Pond"),
                   water_feature("reservoir-intermittent", ftype=436, fcode=43614,
                                 name="Reservoir")]
        decisions_by_id = decisions(allowed, inclusions=[
            {"feature_id": feature["properties"]["id"],
             "reason_code": "reviewed_intermittent_waterbody"} for feature in allowed])
        self.assertTrue(all(decisions_by_id[feature["properties"]["id"]]["eligible"]
                            for feature in allowed))

        invalid = [water_feature("ineligible-code", ftype=436, fcode=43624, area=2),
                   water_feature("eligible-unknown", ftype=436, fcode=43619,
                                 name="Reservoir", area=0.01),
                   water_feature("perennial-lake", fcode=39004, area=0.01),
                   water_feature("swamp", ftype=466, fcode=46600, area=2),
                   water_feature("flowline", layer="flowline", ftype=460, fcode=46003,
                                 name="Intermittent Creek", gnis="001")]
        baseline = decisions(invalid)
        with_inclusions = decisions(invalid, inclusions=[
            {"feature_id": feature["properties"]["id"],
             "reason_code": "reviewed_intermittent_waterbody"} for feature in invalid])
        for feature in invalid:
            ident = feature["properties"]["id"]
            with self.subTest(ident=ident):
                self.assertEqual(with_inclusions[ident]["eligible"], baseline[ident]["eligible"])
                self.assertEqual(with_inclusions[ident]["reason"], baseline[ident]["reason"])
        self.assertTrue(baseline["eligible-unknown"]["eligible"])
        self.assertEqual(baseline["eligible-unknown"]["reason"], "eligible_named_waterbody")

    def test_reviewed_exclusion_removes_only_its_exact_target(self):
        features = [water_feature("target", name="Lake", area=0.001),
                    water_feature("other", name="Pond", area=0.001)]
        exclusion = {"feature_id": "target", "reason_code": "duplicate_of"}
        got = decisions(features, exclusions=[exclusion])
        self.assertFalse(got["target"]["eligible"])
        self.assertTrue(got["other"]["eligible"])

    def test_name_keywords_never_change_eligibility(self):
        names = ["Detention Pond", "Treatment Reservoir", "Private Lake", "Ditch Lake"]
        got = decisions([water_feature(f"n-{index}", name=name, area=0.001)
                         for index, name in enumerate(names)])
        self.assertTrue(all(row["eligible"] for row in got.values()))


def flow(ident, coords, *, gnis="00000001", name="River", ftype=460, fcode=46006,
         length_km=999.0, source_layer="flowline", **extra):
    feature = water_feature(ident, layer=source_layer, ftype=ftype, fcode=fcode,
                            name=name, gnis=gnis, coords=coords,
                            length_km=length_km, group_id=None, **extra)
    feature["geometry"] = {"type": "MultiLineString" if coords and isinstance(coords[0][0], list)
                           else "LineString", "coordinates": coords}
    return feature


def group(features, *, config=None, region_id="fixture", review=None, coverage=None):
    return group_flowlines(features, config or CONFIG, region_id=region_id,
                           review=review or {"inclusions": [], "exclusions": []},
                           coverage=coverage, enforce_major=False)


class WaterGroupingFixtures(unittest.TestCase):
    def test_offline_dry_run_report_matches_approved_current_counts(self):
        report = build_water_report(V2)
        self.assertEqual(report["aspen"]["group_count"], 69)
        self.assertEqual(report["aspen"]["members_per_expected_river"]["00174812"]["member_counts"], [111])
        self.assertEqual(report["aspen"]["waterbodies_displayed_at_0_02_sqkm"], 46)
        self.assertEqual(report["douglas-co"]["group_count"], 35)
        self.assertEqual(report["douglas-co"]["members_per_expected_river"]["00201759"]["state"],
                         "PENDING_EXTERNAL_SOURCE_REFRESH")
        self.assertEqual(report["douglas-co"]["waterbodies_displayed_at_0_02_sqkm"], 32)

    def test_section_8_6_report_is_deterministic_and_marks_pending_source(self):
        report = build_selection_report(V2)
        self.assertEqual(report, build_selection_report(V2))
        for section in ('## aspen', '## douglas-co', 'Members per group distribution',
                        'Extent-edge splits', '0.5 ha (0.005 km²)',
                        'PENDING_EXTERNAL_SOURCE_REFRESH',
                        'To be written by Codex after the padded refresh and checked by the coordinator.'):
            self.assertIn(section, report)


class WaterContractFixtures(unittest.TestCase):
    def setUp(self):
        self.manifest = {"region": {"id": "fixture"}}
        self.layer = {"id": "waterways", "kind": "water",
                      "display": {"path": "regions/fixture/display/waterways.json",
                                  "select": "streams"}}

    def _connected(self):
        features = [flow("a", [[0, 0], [0.5, 0]], length_km=20),
                    flow("b", [[0.5, 0], [1, 0]], length_km=20)]
        expected = group(features)
        for feature in features:
            feature["properties"]["group_id"] = expected["group_assignments"][feature["properties"]["id"]]
        return features, expected["groups"]

    def test_grouped_R69_to_R73_and_grouped_R61_to_R63_accept_fixture(self):
        features, display = self._connected()
        result = validate_m4b_water_layer(self.manifest, self.layer, features, display, CONFIG)
        self.assertEqual(result["water_groups"], {"nhd-gnis-00000001": ["a", "b"]})

    def test_R70_detects_mutated_member_assignment(self):
        features, display = self._connected()
        features[1]["properties"]["group_id"] = "nhd-gnis-foreign"
        with self.assertRaisesRegex(ContractError, "R70"):
            validate_m4b_water_layer(self.manifest, self.layer, features, display, CONFIG)

    def test_R70_rejects_a_segment_moved_to_another_index_group(self):
        features = [flow("a", [[0, 0], [1, 0]]), flow("b", [[3, 0], [4, 0]])]
        computed = group(features)["water_groups"]
        declared = copy.deepcopy(computed)
        first, second = sorted(declared)
        moved = declared[first].pop()
        declared[second].append(moved)
        with self.assertRaisesRegex(ContractError, "R70"):
            _validate_water_group_index(self.manifest, "waterways", declared, computed)

    def test_R71_detects_dropped_group_geometry_line(self):
        features, display = self._connected()
        display[0]["geometry"]["coordinates"].pop()
        with self.assertRaisesRegex(ContractError, "R71"):
            validate_m4b_water_layer(self.manifest, self.layer, features, display, CONFIG)

    def test_R62_detects_group_evidence_changed_from_canonical_members(self):
        features, display = self._connected()
        display[0]["properties"]["evidence"] = {"source_url": "https://wrong.example/"}
        with self.assertRaisesRegex(ContractError, "R62"):
            validate_m4b_water_layer(self.manifest, self.layer, features, display, CONFIG)

    def test_R69_detects_unexpected_canal_in_stream_display(self):
        features, display = self._connected()
        display.append(copy.deepcopy(display[0]))
        display[-1]["properties"]["id"] = "canal-display"
        with self.assertRaisesRegex(ContractError, "R69"):
            validate_m4b_water_layer(self.manifest, self.layer, features, display, CONFIG)

    def test_R69_detects_fcode_change_that_removes_expected_stream(self):
        features, display = self._connected()
        features[0]["properties"]["fcode"] = 46003
        with self.assertRaisesRegex(ContractError, "R71"):
            validate_m4b_water_layer(self.manifest, self.layer, features, display, CONFIG)

    def test_R69_body_threshold_is_taken_from_config_not_artifact_metadata(self):
        layer = {"id": "waterbodies", "kind": "water",
                 "display": {"path": "regions/fixture/display/waterbodies.json", "select": "bodies"}}
        below = water_feature("below", area=0.019)
        at = water_feature("at", area=0.02)
        # Simulate a stale display generated with a lowered 0.01 km2 threshold.
        with self.assertRaisesRegex(ContractError, "R69"):
            validate_m4b_water_layer(self.manifest, layer, [below, at], [below, at], CONFIG)

    def test_R72_rejects_a_reservoir_promoted_from_unknown_to_perennial(self):
        layer = {"id": "waterbodies", "kind": "water",
                 "display": {"path": "regions/fixture/display/waterbodies.json", "select": "bodies"}}
        body = water_feature("reservoir", ftype=436, fcode=43619, name="Reservoir")
        body["properties"]["hydro_category"] = "perennial"
        with self.assertRaisesRegex(ContractError, "R72"):
            validate_m4b_water_layer(self.manifest, layer, [body], [body], CONFIG)

    def test_R72_accepts_eligible_unknown_reservoir_and_rejects_other_displayed_categories(self):
        layer = {"id": "waterbodies", "kind": "water",
                 "display": {"path": "regions/fixture/display/waterbodies.json", "select": "bodies"}}
        eligible_unknown_reservoir = water_feature(
            "eligible-unknown", ftype=436, fcode=43619, name="Reservoir")
        result = validate_m4b_water_layer(self.manifest, layer,
                    [eligible_unknown_reservoir], [eligible_unknown_reservoir], CONFIG)
        self.assertEqual(result["water_groups"], {})
        invalid_display_features = [
            water_feature("ineligible-code", ftype=436, fcode=43624, name="Treatment Pond"),
            water_feature("intermittent-reservoir", ftype=436, fcode=43614, name="Reservoir"),
            water_feature("unstated-lake", ftype=390, fcode=39000, name="Lake"),
        ]
        for feature in invalid_display_features:
            with self.subTest(feature=feature["properties"]["id"]):
                with self.assertRaisesRegex(ContractError, "R72"):
                    validate_m4b_water_layer(self.manifest, layer, [feature], [feature], CONFIG)

    def test_R73_accepts_only_specified_reviewed_inclusion_targets(self):
        allowed = [water_feature("lake-intermittent", ftype=390, fcode=39001, name="Lake"),
                   water_feature("lake-unstated", ftype=390, fcode=39000, name="Pond"),
                   water_feature("reservoir-intermittent", ftype=436, fcode=43614,
                                 name="Reservoir")]
        review = {"exclusions": [], "inclusions": [
            {"feature_id": feature["properties"]["id"],
             "reason_code": "reviewed_intermittent_waterbody",
             "evidence": {"source_url": "https://agency.example/water",
                          "agency": "Agency", "statement": "Official record identifies this water's hydrographic classification."},
             "reviewed_at": "2026-10-07T00:00:00Z"} for feature in allowed]}
        self.assertEqual(len(_validate_water_review(review, [("waterbodies", feature) for feature in allowed],
                                                    "fixture", CONFIG)["inclusions"]), 3)
        invalid = [water_feature("ineligible-code", ftype=436, fcode=43624, area=2),
                   water_feature("eligible-unknown", ftype=436, fcode=43619,
                                 name="Reservoir", area=0.01),
                   water_feature("perennial-lake", ftype=390, fcode=39004, area=0.01),
                   water_feature("swamp", ftype=466, fcode=46600, area=2),
                   water_feature("flowline", layer="flowline", ftype=460, fcode=46003,
                                 name="Creek", gnis="001")]
        for feature in invalid:
            candidate_review = {"exclusions": [], "inclusions": [{
                "feature_id": feature["properties"]["id"],
                "reason_code": "reviewed_intermittent_waterbody",
                "evidence": {"source_url": "https://agency.example/water", "agency": "Agency",
                             "statement": "Official record identifies this water's hydrographic classification."},
                "reviewed_at": "2026-10-07T00:00:00Z"}]}
            with self.subTest(feature=feature["properties"]["id"]):
                with self.assertRaisesRegex(ContractError, "R73"):
                    _validate_water_review(candidate_review, [("water", feature)], "fixture", CONFIG)
        grouped = group([flow("seed", [[0, 0], [1, 0]])])
        group_id = grouped["groups"][0]["properties"]["id"]
        candidate_review["inclusions"][0]["feature_id"] = group_id
        with self.assertRaisesRegex(ContractError, "R73"):
            _validate_water_review(candidate_review, [("water", flow("seed", [[0, 0], [1, 0]]))],
                                   "fixture", CONFIG, [group_id])

    def test_review_host_blocklist_is_read_only_from_config(self):
        feature = water_feature("pond", name="Pond", area=0.01)
        review = {"exclusions": [{"feature_id": "pond", "reason_code": "duplicate_of",
                    "evidence": {"source_url": "https://reddit.com/water", "agency": "Agency",
                                 "statement": "An agency record describes this as a duplicate inventory feature."},
                    "reviewed_at": "2026-10-07T00:00:00Z"}], "inclusions": []}
        self.assertIn("reddit.com", CONFIG["non_claim_hosts"])
        with self.assertRaisesRegex(ContractError, "non-community"):
            _validate_water_review(review, [("waterbodies", feature)], "fixture", CONFIG)
        without_reddit = copy.deepcopy(CONFIG)
        without_reddit["non_claim_hosts"].remove("reddit.com")
        _validate_water_review(review, [("waterbodies", feature)], "fixture", without_reddit)

    def test_R73_rejects_name_only_exclusion_and_accepts_empty_review(self):
        body = water_feature("pond", name="Pond", area=0.001)
        review = {"exclusions": [{"feature_id": "pond", "reason_code": "duplicate_of",
                                  "evidence": {"source_url": "https://agency.example/pond",
                                               "agency": "Agency", "statement": "Pond"},
                                  "reviewed_at": "2026-10-07T00:00:00Z"}],
                  "inclusions": []}
        with self.assertRaisesRegex(ContractError, "R73"):
            validate_m4b_water_layer(self.manifest, {"id": "waterbodies", "display": {"select": "bodies"}},
                                     [body], [], CONFIG, review)
        intermittent = water_feature("intermittent", fcode=39001, name="Pond", area=0.01)
        inclusion = {"exclusions": [], "inclusions": [{"feature_id": "intermittent",
                      "reason_code": "reviewed_intermittent_waterbody",
                      "evidence": {"source_url": "https://agency.example/pond", "agency": "Agency",
                                   "statement": "Pond is named Pond"},
                      "reviewed_at": "2026-10-07T00:00:00Z"}]}
        with self.assertRaisesRegex(ContractError, "R73"):
            validate_m4b_water_layer(self.manifest, {"id": "waterbodies", "display": {"select": "bodies"}},
                                     [intermittent], [], CONFIG, inclusion)
        valid = validate_m4b_water_layer(self.manifest,
                {"id": "waterbodies", "display": {"select": "bodies"}}, [body], [body], CONFIG,
                {"exclusions": [], "inclusions": []})
        self.assertEqual(valid["water_groups"], {})

    def test_manifest_schema_accepts_optional_review_and_water_selector(self):
        manifest = json.loads((V2 / "regions/aspen/region.json").read_text())
        water_layer = next(layer for layer in manifest["layers"] if layer["kind"] == "water")
        water_layer["display"]["select"] = "streams"
        manifest["water_review"] = {"path": "regions/aspen/water-review.json"}
        validator = Draft202012Validator(REGION_MANIFEST_SCHEMA)
        self.assertTrue(validator.is_valid(manifest))
        water_layer["display"]["select"] = "other"
        self.assertFalse(validator.is_valid(manifest))

    def test_same_gnis_endpoints_form_one_group_and_member_order_is_by_id(self):
        result = group([flow("nhd-b", [[1, 0], [2, 0]]), flow("nhd-a", [[0, 0], [1, 0]])])
        self.assertEqual(len(result["groups"]), 1)
        self.assertEqual(result["groups"][0]["properties"]["id"], "nhd-gnis-00000001")
        self.assertEqual(result["water_groups"]["nhd-gnis-00000001"], ["nhd-a", "nhd-b"])
        self.assertEqual(result["groups"][0]["properties"]["member_count"], 2)

    def test_same_gnis_disconnected_parts_get_stable_suffixes_and_length_order(self):
        result = group([flow("long", [[0, 0], [3, 0]]), flow("short", [[5, 0], [6, 0]])])
        self.assertEqual([f["properties"]["id"] for f in result["groups"]],
                         ["nhd-gnis-00000001", "nhd-gnis-00000001-p2"])
        self.assertEqual(result["water_groups"]["nhd-gnis-00000001"], ["long"])
        self.assertEqual(result["water_groups"]["nhd-gnis-00000001-p2"], ["short"])
        self.assertEqual(result["multi_part_gnis_ids"], ["00000001"])

    def test_touching_different_gnis_and_same_name_never_merge(self):
        result = group([flow("one", [[0, 0], [1, 0]], name="Creek"),
                        flow("two", [[1, 0], [2, 0]], gnis="00000002", name="Creek")])
        self.assertEqual(len(result["groups"]), 2)
        self.assertEqual({g["properties"]["gnis_id"] for g in result["groups"]},
                         {"00000001", "00000002"})

    def test_two_names_under_one_gnis_fail_with_both_members_and_names(self):
        with self.assertRaisesRegex(ValueError, "multiple names under GNIS 00000001") as raised:
            group([flow("member-a", [[0, 0], [1, 0]]),
                   flow("member-b", [[1, 0], [2, 0]], name="Different")])
        for value in ("member-a", "member-b", "River", "Different"):
            self.assertIn(value, str(raised.exception))

    def test_empty_gnis_stream_joins_nothing(self):
        result = group([flow("named", [[0, 0], [1, 0]]),
                        flow("empty", [[1, 0], [2, 0]], gnis="")])
        self.assertEqual(len(result["groups"]), 1)
        self.assertEqual(result["water_groups"]["nhd-gnis-00000001"], ["named"])
        self.assertIsNone(result["group_assignments"]["empty"])

    def test_intermittent_reach_connects_two_drawn_lines_without_inventing_geometry(self):
        result = group([flow("seed-a", [[0, 0], [1, 0]]),
                        flow("hidden", [[1, 0], [2, 0]], fcode=46003),
                        flow("seed-b", [[2, 0], [3, 0]])])
        self.assertEqual(len(result["groups"]), 1)
        self.assertEqual(result["water_groups"]["nhd-gnis-00000001"], ["seed-a", "seed-b"])
        self.assertIsNone(result["group_assignments"]["hidden"])
        self.assertEqual(result["groups"][0]["geometry"]["coordinates"],
                         [[[0.0, 0.0], [1.0, 0.0]], [[2.0, 0.0], [3.0, 0.0]]])

    def test_same_gnis_connector_connects_but_is_not_drawn_counted_or_assigned(self):
        result = group([flow("seed-a", [[0, 0], [1, 0]]),
                        flow("connector", [[1, 0], [2, 0]], ftype=334, fcode=33400),
                        flow("seed-b", [[2, 0], [3, 0]])])
        self.assertEqual(len(result["groups"]), 1)
        self.assertEqual(result["water_groups"]["nhd-gnis-00000001"], ["seed-a", "seed-b"])
        self.assertEqual(result["groups"][0]["properties"]["member_count"], 2)
        self.assertIsNone(result["group_assignments"]["connector"])
        self.assertEqual(result["connectors_used"][0]["id"], "connector")
        self.assertGreater(result["connectors_used"][0]["length_km"], 0)

    def test_empty_or_foreign_connector_canal_and_pipeline_do_not_connect(self):
        cases = [
            flow("connector-empty", [[1, 0], [2, 0]], gnis="", ftype=334, fcode=33400),
            flow("connector-foreign", [[1, 0], [2, 0]], gnis="00000002", ftype=334, fcode=33400),
            flow("canal", [[1, 0], [2, 0]], ftype=336, fcode=33600),
            flow("pipeline", [[1, 0], [2, 0]], ftype=428, fcode=42803),
        ]
        for middle in cases:
            with self.subTest(middle=middle["properties"]["id"]):
                result = group([flow("seed-a", [[0, 0], [1, 0]]), middle,
                                flow("seed-b", [[2, 0], [3, 0]])])
                self.assertEqual(len(result["groups"]), 2)
                self.assertIsNone(result["group_assignments"][middle["properties"]["id"]])

    def test_drawn_status_does_not_pass_through_connector_to_artificial_path(self):
        result = group([flow("seed", [[0, 0], [1, 0]]),
                        flow("connector", [[1, 0], [2, 0]], ftype=334, fcode=33400),
                        flow("artificial", [[2, 0], [3, 0]], ftype=558, fcode=55800)])
        self.assertEqual(result["water_groups"]["nhd-gnis-00000001"], ["seed"])
        self.assertIsNone(result["group_assignments"]["artificial"])

    def test_artificial_paths_draw_to_fixed_point_but_not_through_hidden_stream(self):
        result = group([flow("seed", [[0, 0], [1, 0]]),
                        flow("art-a", [[1, 0], [2, 0]], ftype=558, fcode=55800),
                        flow("art-b", [[2, 0], [3, 0]], ftype=558, fcode=55800),
                        flow("hidden", [[3, 0], [4, 0]], fcode=46003),
                        flow("art-c", [[4, 0], [5, 0]], ftype=558, fcode=55800)])
        self.assertEqual(result["water_groups"]["nhd-gnis-00000001"], ["art-a", "art-b", "seed"])
        only_artificial = group([flow("art-only", [[0, 0], [1, 0]], ftype=558, fcode=55800)])
        self.assertEqual(only_artificial["groups"], [])

    def test_connectivity_name_conflict_and_connector_name_are_strict(self):
        with self.assertRaisesRegex(ValueError, "multiple names under GNIS"):
            group([flow("seed-a", [[0, 0], [1, 0]]),
                   flow("connector", [[1, 0], [2, 0]], ftype=334, fcode=33400,
                        name="Other River"),
                   flow("seed-b", [[2, 0], [3, 0]])])

    def test_multipart_source_is_one_member_and_no_intersection_connects(self):
        multipart = flow("multipart", [[[0, 0], [1, 0]], [[5, 0], [6, 0]]])
        result = group([multipart])
        self.assertEqual(result["groups"][0]["properties"]["member_count"], 1)
        self.assertEqual(len(result["groups"][0]["geometry"]["coordinates"]), 2)
        crossing = flow("crossing", [[0.5, -1], [0.5, 1]], gnis="00000002")
        split = group([flow("horizontal", [[0, 0], [1, 0]]), crossing])
        self.assertEqual(len(split["groups"]), 2)

    def test_same_gnis_interior_crossing_does_not_join_components(self):
        crossing = flow("vertical", [[0.5, -1], [0.5, 1]])
        horizontal = flow("horizontal", [[0, 0], [1, 0]])
        self.assertEqual(len(group([horizontal, crossing])["groups"]), 2)

    def test_supporting_bridge_joins_connectivity_but_is_never_a_member(self):
        support = flow("support", [[1, 0], [2, 0]], gnis="", name=None,
                       support_for="00000001", support_reason="bridges_named_parts")
        result = group([flow("seed-a", [[0, 0], [1, 0]]), support,
                        flow("seed-b", [[2, 0], [3, 0]])])
        self.assertEqual(result["water_groups"]["nhd-gnis-00000001"], ["seed-a", "seed-b"])
        self.assertIsNone(result["group_assignments"]["support"])
        self.assertNotIn("support", result["water_groups"]["nhd-gnis-00000001"])

    def test_real_canonical_regions_reproduce_expected_groups_connectors_and_bodies(self):
        config = water_display_config()
        for region_id in ("aspen", "douglas-co"):
            manifest = json.loads((V2 / f"regions/{region_id}/region.json").read_text())
            bundle_path = V2 / ("map-data-v2.json" if region_id == "aspen"
                                else "regions/douglas-co/research.json")
            bundle = json.loads(bundle_path.read_text())
            coverage_doc = json.loads((V2 / manifest["coverage"]["path"]).read_text())
            coverage_feature = _json_pointer(coverage_doc, manifest["coverage"].get("pointer", ""))
            from shapely.geometry import shape
            coverage = shape(coverage_feature["geometry"]).buffer(
                next((layer.get("extent_padding_deg", 0.0) for layer in manifest["layers"]
                      if layer.get("kind") == "water"), 0.0))
            flowline_layer = next(layer for layer in manifest["layers"]
                                  if layer.get("kind") == "water" and
                                  layer.get("display", {}).get("select") == "streams")
            flowlines = _json_pointer(bundle, flowline_layer["pointer"])["features"]
            grouped = group_flowlines(flowlines, config, region_id=region_id,
                                      coverage=coverage)
            body_features = ([feature for feature in bundle["layers"]["hydrology"]["features"]
                              if feature["properties"].get("source_layer") == "waterbody"]
                             if region_id == "aspen" else
                             bundle["layers"]["waterbodies"]["features"])
            bodies = [row for row in select_water_features(body_features, config) if row["eligible"]]
            body_layer = {"id": "waterbodies", "kind": "water",
                          "display": {"select": "bodies"}}
            validate_m4b_water_layer({"region": {"id": region_id}}, body_layer,
                                     body_features, [row["feature"] for row in bodies], config)
            expected_groups = 69 if region_id == "aspen" else 35
            expected_bodies = 46 if region_id == "aspen" else 32
            with self.subTest(region=region_id):
                self.assertEqual(len(grouped["groups"]), expected_groups)
                self.assertEqual(len(bodies), expected_bodies)
                self.assertTrue(all(set(feature["properties"]["gnis_id"]
                                        for feature in flowlines if feature["properties"]["id"] in members)
                                    == {group_id.removeprefix("nhd-gnis-").split("-p")[0]}
                                    for group_id, members in grouped["water_groups"].items()))
        aspen_manifest = json.loads((V2 / "regions/aspen/region.json").read_text())
        aspen_bundle = json.loads((V2 / "map-data-v2.json").read_text())
        aspen_flowlines = aspen_bundle["layers"]["hydrology"]["features"]
        coverage_doc = json.loads((V2 / aspen_manifest["coverage"]["path"]).read_text())
        from shapely.geometry import shape
        coverage = shape(_json_pointer(coverage_doc, aspen_manifest["coverage"].get("pointer", ""))
                         ["geometry"]).buffer(0.005)
        aspen = group_flowlines(aspen_flowlines, config, region_id="aspen", coverage=coverage)
        members = {row["gnis_id"]: row["member_count"] for row in aspen["group_summaries"]}
        counts = {}
        for row in aspen["group_summaries"]:
            counts[row["gnis_id"]] = counts.get(row["gnis_id"], 0) + 1
        self.assertEqual(counts["00180061"], 1)
        self.assertEqual(counts["00180317"], 1)
        self.assertEqual(counts["00179785"], 3)
        self.assertEqual(members["00174812"], 111)
        self.assertEqual({row["gnis_id"] for row in aspen["extent_edge_splits"]}, {"00179785"})
        self.assertEqual({row["gnis_id"] for row in aspen["connectors_used"]},
                         {"00180061", "00180317"})

    def test_geodesic_length_uses_canonical_coordinates_not_source_sum(self):
        feature = flow("long-degree", [[0, 0], [1, 0]], length_km=999.0)
        result = group([feature])
        exact = geodesic_length_km([feature])
        self.assertAlmostEqual(exact, 111.3194908, places=5)
        self.assertEqual(result["groups"][0]["properties"]["length_km"], round(exact, 3))
        self.assertNotEqual(result["groups"][0]["properties"]["length_km"], 999.0)

    def test_group_and_member_order_are_input_and_hash_seed_independent(self):
        features = [flow("z", [[0, 0], [1, 0]]), flow("a", [[1, 0], [2, 0]]),
                    flow("b", [[5, 0], [6, 0]])]
        baseline = group(features)
        shuffled = group(list(reversed(features)))
        self.assertEqual(baseline, shuffled)
        script = """import sys; sys.path.insert(0,'v2/pipeline/scripts')
from lib.water import group_flowlines,water_display_config
def f(i,a,b):
 return {'type':'Feature','geometry':{'type':'LineString','coordinates':[[a,0],[b,0]]},'properties':{'id':i,'source_id':i,'source_layer':'flowline','gnis_id':'00000001','name':'River','ftype':460,'fcode':46006,'water_class':'stream','hydro_category':'perennial','evidence':{},'length_km':1}}
r=group_flowlines([f('z',0,1),f('a',1,2),f('b',5,6)],water_display_config(),region_id='fixture',enforce_major=False)
import json; print(json.dumps(r['water_groups'],sort_keys=True))"""
        outputs = []
        for seed in ("0", "1"):
            env = dict(__import__("os").environ, PYTHONHASHSEED=seed)
            run = subprocess.run([sys.executable, "-c", script], cwd=V2.parent,
                                 env=env, check=True, text=True, capture_output=True)
            outputs.append(run.stdout.strip())
        self.assertEqual(outputs[0], outputs[1])

    def test_expected_major_river_missing_short_foreign_and_pending_are_distinct(self):
        row = {"gnis_id": "123", "minimum_drawn_fraction": 0.8}
        config = copy.deepcopy(CONFIG)
        config["expected_major_rivers"] = {"fixture": [row]}
        missing = group([], config=config)
        with self.assertRaisesRegex(ValueError, "major river 123.*missing"):
            validate_expected_major_rivers(missing, config, "fixture")
        short = group([flow("short", [[0, 0], [0.5, 0]], gnis="123"),
                       flow("undrawn-long", [[10, 0], [110, 0]], gnis="123",
                            ftype=558, fcode=55800)], config=config)
        with self.assertRaisesRegex(ValueError, "major river 123.*fraction"):
            validate_expected_major_rivers(short, config, "fixture")
        foreign_group = copy.deepcopy(short)
        foreign_group["groups"][0]["properties"]["gnis_id"] = "other"
        with self.assertRaisesRegex(ValueError, "major river 123.*foreign"):
            validate_expected_major_rivers(foreign_group, config, "fixture")

    def test_pending_marker_only_downgrades_absent_south_platte(self):
        config = copy.deepcopy(CONFIG)
        config["expected_major_rivers"] = {"douglas-co": [
            {"gnis_id": "00201759", "minimum_drawn_fraction": 0.8}]}
        config["pending_external_source_refresh"] = {
            "region_id": "douglas-co", "gnis_id": "00201759",
            "state": "PENDING_EXTERNAL_SOURCE_REFRESH", "reason": "fixture pending source"}
        result = group([], config=config, region_id="douglas-co")
        self.assertEqual(validate_expected_major_rivers(result, config, "douglas-co")[0]["state"],
                         "PENDING_EXTERNAL_SOURCE_REFRESH")
        config["expected_major_rivers"]["douglas-co"].append(
            {"gnis_id": "other", "minimum_drawn_fraction": 0.8})
        result["major_river_checks"].append({"gnis_id": "other", "group_present": False,
            "seed_present": False, "member_gnis_ids": [], "drawn_fraction": 0,
            "minimum_drawn_fraction": 0.8})
        with self.assertRaisesRegex(ValueError, "major river other.*missing"):
            validate_expected_major_rivers(result, config, "douglas-co")
        config.pop("pending_external_source_refresh")
        with self.assertRaisesRegex(ValueError, "major river 00201759.*missing"):
            validate_expected_major_rivers(result, config, "douglas-co")

    def test_pending_marker_does_not_hide_a_short_river_or_another_identity(self):
        config = copy.deepcopy(CONFIG)
        config["expected_major_rivers"] = {"douglas-co": [
            {"gnis_id": "00201759", "minimum_drawn_fraction": 0.8}]}
        pending = config["pending_external_source_refresh"]
        short = group([flow("seed", [[0, 0], [0.5, 0]], gnis="00201759"),
                       flow("undrawn", [[10, 0], [110, 0]], gnis="00201759",
                            ftype=558, fcode=55800)], config=config, region_id="douglas-co")
        config.pop("pending_external_source_refresh")
        with self.assertRaisesRegex(ValueError, "00201759.*fraction"):
            validate_expected_major_rivers(short, config, "douglas-co")
        config["pending_external_source_refresh"] = pending
        with self.assertRaisesRegex(ValueError, "PENDING_EXTERNAL_SOURCE_REFRESH marker must be removed"):
            validate_expected_major_rivers(short, config, "douglas-co")
        config["pending_external_source_refresh"] = {**pending, "gnis_id": "other"}
        with self.assertRaisesRegex(ValueError, "invalid pending"):
            validate_expected_major_rivers(short, config, "douglas-co")

    def test_present_seed_requires_pending_marker_removal(self):
        config = copy.deepcopy(CONFIG)
        config["expected_major_rivers"] = {"douglas-co": [
            {"gnis_id": "00201759", "minimum_drawn_fraction": 0.8}]}
        seed = flow("south-seed", [[0, 0], [1, 0]], gnis="00201759",
                    name="South Platte River")
        result = group_flowlines([seed], config, region_id="douglas-co", enforce_major=False)
        with self.assertRaisesRegex(ValueError,
                                    "PENDING_EXTERNAL_SOURCE_REFRESH marker must be removed"):
            validate_expected_major_rivers(result, config, "douglas-co")

    def test_padded_south_platte_fixture_groups_only_when_seed_is_present(self):
        cfg = copy.deepcopy(CONFIG)
        cfg["expected_major_rivers"] = {"fixture": []}
        fixture = [flow("south-seed", [[0, 0], [1, 0]], gnis="00201759",
                         name="South Platte River"),
                   flow("south-path", [[1, 0], [2, 0]], gnis="00201759",
                         name="South Platte River", ftype=558, fcode=55800)]
        self.assertEqual(len(group(fixture, config=cfg)["groups"]), 1)
        self.assertEqual(group(fixture[1:], config=cfg)["groups"], [])


if __name__ == "__main__":
    unittest.main()
