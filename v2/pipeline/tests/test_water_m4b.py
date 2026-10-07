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
    select_water_features, water_display_config,
)


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


if __name__ == "__main__":
    unittest.main()
