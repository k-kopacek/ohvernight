import json
import csv
import sys
import unittest
from pathlib import Path

from shapely.geometry import LineString, box, mapping, shape

V2 = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(V2 / "pipeline" / "scripts"))

from refresh_m4b_douglas_water import (PAD_DEG, compare_layer, padded_water_geometry)  # noqa: E402


class WaterM4BExtentTests(unittest.TestCase):
    def setUp(self):
        self.bundle = json.loads((V2 / "regions/douglas-co/research.json").read_text())
        self.county = shape(self.bundle["layers"]["coverage"]["features"][0]["geometry"])
        self.padded = padded_water_geometry(self.county)

    def test_padding_is_deterministic_and_uses_the_approved_degrees(self):
        first = padded_water_geometry(self.county)
        second = padded_water_geometry(self.county)
        self.assertEqual(PAD_DEG, 0.005)
        self.assertEqual(first.wkb, second.wkb)
        self.assertEqual(first, self.county.buffer(0.005))

    def test_every_douglas_water_geometry_is_covered_by_the_padded_polygon(self):
        tolerated = self.padded.buffer(1e-9)
        for layer_id in ("waterways", "waterbodies"):
            with self.subTest(layer=layer_id):
                for feature in self.bundle["layers"][layer_id]["features"]:
                    self.assertTrue(tolerated.covers(shape(feature["geometry"])),
                                    feature["properties"].get("id"))

    def test_every_preexisting_douglas_water_id_remains_present(self):
        baseline_by_layer = {"waterways": set(), "waterbodies": set()}
        with (V2.parent / "docs/research/m4-water/nhd-snapshot-id-map.csv").open(newline="") as handle:
            for row in csv.DictReader(handle):
                if row["region"] != "douglas-co":
                    continue
                layer_id = {"flowline": "waterways", "waterbody": "waterbodies"}.get(row["layer"])
                if layer_id:
                    baseline_by_layer[layer_id].add(row["new_id"])
        current_ids = {layer: {feature["properties"]["id"] for feature in
                               self.bundle["layers"][layer]["features"]}
                       for layer in ("waterways", "waterbodies")}
        for layer in ("waterways", "waterbodies"):
            old_ids = baseline_by_layer[layer]
            with self.subTest(layer=layer):
                self.assertTrue(old_ids, f"snapshot CSV has no baseline IDs for {layer}")
                self.assertTrue(old_ids.issubset(current_ids[layer]))

    def test_difference_guard_explains_only_geometry_growth_into_padding(self):
        county = box(0, 0, 1, 1)
        padded = county.buffer(0.005)
        def feature(geometry):
            return {"type": "Feature", "geometry": mapping(geometry),
                    "properties": {"id": "nhd-one", "source_id": "one", "name": "River",
                                   "ftype": 460, "fcode": 46006}}
        before = [feature(LineString([(0.5, 0.5), (1, 0.5)]))]
        extended = [feature(LineString([(0.5, 0.5), (1, 0.5), (1.004, 0.5)]))]
        report = compare_layer("waterways", before, extended, county, padded)
        self.assertTrue(report["explained"])
        self.assertEqual(report["geometry_grew_ids"], ["nhd-one"])

    def test_difference_guard_rejects_non_padding_geometry_changes(self):
        county = box(0, 0, 1, 1)
        padded = county.buffer(0.005)
        def feature(geometry):
            return {"type": "Feature", "geometry": mapping(geometry),
                    "properties": {"id": "nhd-one", "source_id": "one", "name": "River",
                                   "ftype": 460, "fcode": 46006}}
        before = [feature(LineString([(0.5, 0.5), (0.9, 0.5)]))]
        moved = [feature(LineString([(0.6, 0.5), (0.9, 0.5)]))]
        report = compare_layer("waterways", before, moved, county, padded)
        self.assertFalse(report["explained"])
        self.assertEqual(report["other_existing_changes"], ["nhd-one"])

    def test_difference_guard_uses_exact_county_reclip_for_interpolated_endpoints(self):
        county = box(0, 0, 1, 1)
        padded = county.buffer(0.005)
        source = LineString([(0.3333333333333333, 0.12121212121212),
                             (1.004, 0.923456789)])
        def feature(geometry):
            return {"type": "Feature", "geometry": mapping(geometry),
                    "properties": {"id": "nhd-one", "source_id": "one", "name": "River",
                                   "ftype": 460, "fcode": 46006}}
        old = source.intersection(county)
        new = source.intersection(padded)
        self.assertTrue(old.equals_exact(new.intersection(county), 0))
        report = compare_layer("waterways", [feature(old)], [feature(new)], county, padded)
        self.assertTrue(report["explained"])
        self.assertEqual(report["geometry_grew_ids"], ["nhd-one"])

    def test_difference_guard_rejects_every_unapproved_existing_feature_change(self):
        county = box(0, 0, 1, 1)
        padded = county.buffer(0.005)
        def feature(points, **overrides):
            props = {"id": "nhd-one", "source_id": "one", "name": "River",
                     "ftype": 460, "fcode": 46006}
            props.update(overrides)
            return {"type": "Feature", "geometry": mapping(LineString(points)),
                    "properties": props}
        old = feature([(0.5, 0.5), (1, 0.5)])
        extended = [(0.5, 0.5), (1, 0.5), (1.004, 0.5)]
        cases = {
            "inside_county_change": feature([(0.5, 0.5001), (1, 0.5), (1.004, 0.5)]),
            "inside_change_below_old_tolerance": feature([(0.5, 0.5 + 1e-11), (1, 0.5)]),
            "shrinkage": feature([(0.6, 0.5), (1, 0.5)]),
            "beyond_padding": feature([(0.5, 0.5), (1, 0.5), (1.006, 0.5)]),
            "padding_overflow_below_old_tolerance": feature([(0.5, 0.5), (1, 0.5), (1.005 + 1e-11, 0.5)]),
            "renamed": feature(extended, name="Other"),
            "source_id_changed": feature(extended, source_id="other"),
            "type_changed": feature(extended, ftype=336),
            "code_changed": feature(extended, fcode=46003),
        }
        for label, new in cases.items():
            with self.subTest(change=label):
                report = compare_layer("waterways", [old], [new], county, padded)
                self.assertFalse(report["explained"])
                self.assertTrue(report["other_existing_changes"] or report["name_changed_ids"])
        missing = compare_layer("waterways", [old], [], county, padded)
        self.assertFalse(missing["explained"])
        self.assertEqual(missing["removed_ids"], ["nhd-one"])


if __name__ == "__main__":
    unittest.main()
