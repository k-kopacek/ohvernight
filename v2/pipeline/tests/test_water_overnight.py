"""Bounded offline M4-B grouping, identity, mutation and build stress coverage."""
import copy
import hashlib
import json
import os
import random
import subprocess
import sys
import unittest
from pathlib import Path

from shapely.geometry import shape

V2 = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(V2 / "pipeline/scripts"))

import test_water_m4b as fixtures
import test_region_contract as contract_fixtures
from lib.region_contract import (ContractError, validate_water_alias_file,
                                 validate_water_contract_data, validate_m4b_water_layer)
from lib.water import attach_legacy_ids, group_flowlines, normalize_feature


def canonical(ident, coordinates):
    return normalize_feature("flowline", {"properties": {
        "permanent_identifier": ident, "gnis_name": "Stress River", "gnis_id": "stress",
        "ftype": 460, "fcode": 46006, "lengthkm": 999},
        "geometry": {"type": "LineString", "coordinates": coordinates}},
        {"type": "LineString", "coordinates": coordinates},
        {"source_url": "https://fixture.example/6", "retrieved_at": "2026-10-08T00:00:00Z",
         "agency": "USGS", "confidence": "high", "last_verified": None,
         "verification_method": "arcgis_rest_query", "notes": ""})


class OvernightWaterTests(unittest.TestCase):
    def stress_features(self):
        return [canonical(f"part-{part:02d}-segment-{segment:02d}",
                          [[part * 2 + segment / 10, 0], [part * 2 + (segment + 1) / 10, 0]])
                for part in range(20) for segment in range(4)]

    def grouped(self, features):
        return group_flowlines(features, region_id="fixture", enforce_major=False)

    def test_many_parts_member_shuffles_are_byte_identical_and_input_is_immutable(self):
        features = self.stress_features()
        before = copy.deepcopy(features)
        expected = self.grouped(features)
        self.assertEqual(len(expected["groups"]), 20)
        self.assertEqual(sum(map(len, expected["water_groups"].values())), 80)
        encoded = json.dumps(expected, sort_keys=True, separators=(",", ":"))
        for seed in range(30):
            with self.subTest(seed=seed):
                shuffled = copy.deepcopy(features)
                random.Random(seed).shuffle(shuffled)
                self.assertEqual(json.dumps(self.grouped(shuffled), sort_keys=True, separators=(",", ":")), encoded)
                self.assertEqual(features, before)

    def test_reversed_lines_and_repeated_endpoints_keep_ids_members_and_geometry(self):
        features = self.stress_features()
        expected = self.grouped(features)
        expected_groups = {f["properties"]["id"]: f for f in expected["groups"]}
        for variant in ("reversed", "duplicate_endpoints", "both"):
            modified = copy.deepcopy(features)
            for feature in modified:
                coords = feature["geometry"]["coordinates"]
                if variant in {"reversed", "both"}:
                    coords.reverse()
                if variant in {"duplicate_endpoints", "both"}:
                    coords.insert(0, copy.deepcopy(coords[0]))
                    coords.append(copy.deepcopy(coords[-1]))
            random.Random(1907).shuffle(modified)
            before = copy.deepcopy(modified)
            result = self.grouped(modified)
            with self.subTest(variant=variant):
                self.assertEqual(result["water_groups"], expected["water_groups"])
                self.assertEqual(result["group_assignments"], expected["group_assignments"])
                for group in result["groups"]:
                    baseline = expected_groups[group["properties"]["id"]]
                    self.assertTrue(shape(group["geometry"]).equals(shape(baseline["geometry"])))
                    self.assertEqual(group["properties"]["length_km"], baseline["properties"]["length_km"])
                self.assertEqual(modified, before)

    def test_legacy_alias_round_trip_survives_refresh_and_geometry_growth(self):
        old = [canonical("a", [[0, 0], [1, 0]]), canonical("b", [[1, 0], [2, 0]])]
        for index, feature in enumerate(old):
            feature["properties"]["legacy_ids"] = [f"old-{index}"]
        new = copy.deepcopy(list(reversed(old)))
        new[0]["geometry"]["coordinates"].append([2.005, 0])
        new, _, _ = attach_legacy_ids(old, new)
        grouped = self.grouped(new)
        targets = {member: group for group, members in grouped["water_groups"].items() for member in members}
        aliases = {legacy: targets[f["properties"]["id"]] for f in new
                   for legacy in f["properties"]["legacy_ids"]}
        document = {"region_id": "fixture", "water_id_aliases": aliases}
        raw = (json.dumps(document, sort_keys=True, separators=(",", ":")) + "\n").encode()
        entry = {"water_aliases": {"path": "regions/fixture/display/water-aliases.json",
                                  "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}}
        decoded = json.loads(raw)
        resolved = validate_water_alias_file(entry, decoded, raw, "fixture")
        self.assertEqual(resolved, {"old-0": "nhd-gnis-stress", "old-1": "nhd-gnis-stress"})
        second, _, _ = attach_legacy_ids(new, copy.deepcopy(new))
        self.assertEqual({f["properties"]["id"]: f["properties"]["legacy_ids"] for f in second},
                         {f["properties"]["id"]: f["properties"]["legacy_ids"] for f in new})
        for ident in resolved.values():
            self.assertIn(ident, grouped["water_groups"])

    def test_R66_R67_R68_R75_mutations_fail_with_the_specific_rule(self):
        factory = contract_fixtures.RegionContractTests()
        cases = {
            "R66": lambda c, a: c[1][1]["properties"].update(source_id=c[0][1]["properties"]["source_id"]),
            "R67": lambda c, a: c[0][1]["properties"].update(hydro_category="unknown"),
            "R68": lambda c, a: c[0][1]["properties"].update(legacy_ids=["old-a", "old-a"]),
            "R75": lambda c, a: c[0][1]["properties"].update(access="allowed"),
        }
        for rule, mutate in cases.items():
            manifest, canonical_rows, config, aliases, displayed = factory.water_contract_base()
            validate_water_contract_data(manifest, canonical_rows, config, aliases, displayed)
            mutate(canonical_rows, aliases)
            with self.subTest(rule=rule), self.assertRaises(ContractError) as raised:
                validate_water_contract_data(manifest, canonical_rows, config, aliases, displayed)
            self.assertEqual(raised.exception.rule, rule)

    def test_R69_R70_R71_R72_R73_mutations_fail_with_the_specific_rule(self):
        factory = fixtures.WaterContractFixtures()
        factory.setUp()
        for rule in ("R69", "R70", "R71", "R72", "R73"):
            rows, displayed = factory._connected()
            layer = copy.deepcopy(factory.layer)
            manifest = copy.deepcopy(factory.manifest)
            kwargs = {}
            validate_m4b_water_layer(manifest, layer, rows, displayed, fixtures.CONFIG)
            if rule == "R69":
                displayed.append(copy.deepcopy(displayed[0]))
                displayed[-1]["properties"]["id"] = "unexpected-display-group"
            elif rule == "R70":
                rows[0]["properties"]["group_id"] = "nhd-gnis-foreign"
            elif rule == "R71":
                displayed[0]["geometry"]["coordinates"].pop()
            elif rule == "R72":
                displayed[0]["properties"]["hydro_category"] = "intermittent"
            elif rule == "R73":
                kwargs["review"] = {"inclusions": [], "exclusions": [{"name": "Stress River"}]}
            with self.subTest(rule=rule), self.assertRaises(ContractError) as raised:
                validate_m4b_water_layer(manifest, layer, rows, displayed, fixtures.CONFIG, **kwargs)
            self.assertEqual(raised.exception.rule, rule)

    def test_display_artifacts_reproduce_across_two_builds_and_two_hash_seeds(self):
        script = """import hashlib,json,sys
from pathlib import Path
sys.path.insert(0,str(Path('v2/pipeline/scripts').resolve()))
from build_display import build_region
runs=[]
for repeat in range(2):
 result={}
 for region in ('aspen','douglas-co'):
  built=build_region(region,Path('v2').resolve(),write=False)
  result.update({path:hashlib.sha256(raw).hexdigest() for path,raw in built['artifacts'].items()})
 runs.append(result)
assert runs[0]==runs[1]
print(json.dumps(runs[0],sort_keys=True))"""
        outputs = []
        for seed in ("7", "1907"):
            env = dict(os.environ, PYTHONHASHSEED=seed)
            run = subprocess.run([sys.executable, "-c", script], cwd=V2.parent,
                                 env=env, capture_output=True, text=True, check=True, timeout=180)
            outputs.append(run.stdout)
        self.assertEqual(outputs[0], outputs[1])
        self.assertGreater(len(json.loads(outputs[0])), 10)


if __name__ == "__main__":
    unittest.main()
