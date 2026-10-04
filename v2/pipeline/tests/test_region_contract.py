import copy
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

V2 = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(V2 / "pipeline" / "scripts"))

from lib.region_contract import ContractError, normalize_transport, validate_region, validate_region_data


class RegionContractTests(unittest.TestCase):
    def load(self, relative):
        return json.loads((V2 / relative).read_text())

    def test_real_regions_validate_and_pin_status_gaps(self):
        manifests = sorted((V2 / "regions").glob("*/region.json"))
        self.assertEqual({p.parent.name for p in manifests}, {"aspen", "douglas-co"})
        reports = {p.parent.name: validate_region(p, V2) for p in manifests}
        self.assertEqual(reports["aspen"]["unrecorded_status_layers"], ["trails"])
        self.assertEqual(reports["douglas-co"]["unrecorded_status_layers"], ["trails", "roads"])
        self.assertEqual(set(reports["aspen"]["legacy_transport"]), {"land_ownership", "wilderness", "mvum_roads", "hydrology", "fire_restriction_stage", "dispersed_corridors", "dispersed_corridor_points", "leads", "reviewed_sites"})

    def test_declared_surface_and_fact_dimensions(self):
        expected = {
            "aspen": {"map-data-v2.json", "trails.geojson", "overnight-options.json", "ridb-options.json", "destinations.json", "pipeline/config/aoi.geojson", "pipeline/config/rules-registry.json"},
            "douglas-co": {"regions/douglas-co/research.json"},
        }
        dimensions = {"ownership", "public_access", "camping_permission", "closures", "restrictions", "road_access", "trail_access", "recreation_permission"}
        for path in (V2 / "regions").glob("*/region.json"):
            manifest = self.load(path.relative_to(V2))
            self.assertEqual({layer["path"] for layer in manifest["layers"]} | {manifest["coverage"]["path"]} | ({manifest["rules"]["path"]} if manifest["rules"] else set()), expected[path.parent.name])
            self.assertEqual(set(manifest["fact_coverage"]), dimensions)

    def test_normalize_transport_aliases(self):
        rows = [
            ({"status": "available", "completed_at": "2026-01-01T00:00:00Z"}, {"status": "available", "last_checked_at": "2026-01-01T00:00:00Z", "last_retrieved_at": "2026-01-01T00:00:00Z"}, ["completed_at"]),
            ({"status": "available", "retrieved_at": "2026-01-01T00:00:00Z"}, {"status": "available", "last_checked_at": "2026-01-01T00:00:00Z", "last_retrieved_at": "2026-01-01T00:00:00Z"}, ["retrieved_at"]),
            ({"status": "failed", "checked_at": "2026-01-01T00:00:00Z", "error": "nope"}, {"status": "unavailable", "last_checked_at": "2026-01-01T00:00:00Z", "reason": "nope"}, ["checked_at", "failed", "error"]),
            ({"status": "available", "last_checked_at": "2026-01-01T00:00:00Z", "last_confirmed_at": "2026-01-01T00:00:00Z"}, {"status": "available", "last_retrieved_at": "2026-01-01T00:00:00Z"}, ["inferred_retrieval", "last_confirmed_at"]),
        ]
        for record, expected, aliases in rows:
            normalized, used = normalize_transport(record)
            for key, value in expected.items():
                self.assertEqual(normalized[key], value)
            self.assertEqual(used, aliases)

    def test_pinned_real_transport_alias_sets(self):
        aspen = validate_region(V2 / "regions/aspen/region.json", V2)
        douglas = validate_region(V2 / "regions/douglas-co/region.json", V2)
        self.assertEqual({alias for aliases in aspen["legacy_transport"].values() for alias in aliases}, {"completed_at"})
        self.assertEqual({alias for aliases in douglas["legacy_transport"].values() for alias in aliases}, {"retrieved_at"})
        ridb = self.load("ridb-options.json")["source_status"]
        self.assertEqual(set(normalize_transport(ridb)[1]), {"inferred_retrieval", "last_confirmed_at"})

    def base(self):
        feature = {"type": "Feature", "geometry": {"type": "Point", "coordinates": [0, 0]}, "properties": {"id": "water-1", "evidence": {"source_url": "https://agency.example/source", "agency": "Agency", "retrieved_at": "2026-01-01T00:00:00Z", "last_verified": None, "confidence": "unverified", "verification_method": "source_fetch"}}}
        manifest = {
            "contract_version": 1,
            "region": {"id": "synthetic", "name": "Synthetic", "state": "CO", "status": "research_only"},
            "coverage": {"path": "coverage.json", "pointer": "", "kind": "project_defined_extent", "source_id": None, "statement": "Synthetic extent. It is not a land-ownership or access boundary."},
            "sources": {"agency": {"type": "agency", "agency": "Agency", "source_urls": ["https://agency.example/source"], "scope": "Context only; does not establish permission."}},
            "layers": [{"id": "water", "kind": "water", "format": "feature_collection", "path": "data.json", "pointer": "/layers/water", "source_ids": ["agency"], "status_ref": {"path": "data.json", "pointer": "/status"}, "max_age_hours": 24, "geometry_types": ["Point"], "allow_null_geometry": False, "must_be_empty": False, "extent_padding_deg": 0, "spatial_precision": "source_published", "fields": {"source": [], "derived": []}, "limitations": "Context only."}],
            "rules": None,
            "fact_coverage": {"ownership": {"state": "none", "layer_ids": [], "official_urls": [], "statement": "Unknown."}, "public_access": {"state": "none", "layer_ids": [], "official_urls": [], "statement": "Unknown."}, "camping_permission": {"state": "none", "layer_ids": [], "official_urls": [], "statement": "Unknown."}, "closures": {"state": "none", "layer_ids": [], "official_urls": [], "statement": "Unknown."}, "restrictions": {"state": "none", "layer_ids": [], "official_urls": [], "statement": "Unknown."}, "road_access": {"state": "none", "layer_ids": [], "official_urls": [], "statement": "Unknown."}, "trail_access": {"state": "none", "layer_ids": [], "official_urls": [], "statement": "Unknown."}, "recreation_permission": {"state": "context", "layer_ids": ["water"], "official_urls": [], "statement": "Unknown."}},
            "known_gaps": ["Synthetic data."],
        }
        docs = {"coverage.json": {"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [[[-1, -1], [1, -1], [1, 1], [-1, 1], [-1, -1]]]}, "properties": {}}, "data.json": {"layers": {"water": {"type": "FeatureCollection", "features": [feature]}}, "status": {"status": "available", "last_retrieved_at": "2026-01-01T00:00:00Z", "count": 1}}}
        return manifest, docs

    def valid(self, manifest=None, docs=None):
        manifest, docs = manifest or self.base()[0], docs or self.base()[1]
        return validate_region_data(manifest, lambda path: docs[path])

    def assert_rule(self, rule, mutate):
        manifest, docs = self.base()
        self.valid(manifest, docs)
        mutate(manifest, docs)
        with self.assertRaises(ContractError) as raised:
            self.valid(manifest, docs)
        self.assertEqual(raised.exception.rule, rule)

    def test_R01_manifest_enum_and_shape(self):
        self.assert_rule("R01", lambda m, d: m["region"].update(status="verified"))

    def test_R02_manifest_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bad = root / "wrong" / "region.json"
            bad.parent.mkdir()
            shutil.copy(V2 / "regions/aspen/region.json", bad)
            with self.assertRaises(ContractError) as raised:
                validate_region(bad, V2)
            self.assertEqual(raised.exception.rule, "R02")

    def test_R03_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            good = root / "aspen" / "region.json"
            good.parent.mkdir()
            manifest = self.load("regions/aspen/region.json")
            manifest["coverage"]["path"] = "../outside.json"
            good.write_text(json.dumps(manifest))
            with self.assertRaises(ContractError) as raised:
                validate_region(good, V2)
            self.assertEqual(raised.exception.rule, "R03")

    def test_R04_source_and_layer_ids(self):
        self.assert_rule("R04", lambda m, d: m["layers"].append(copy.deepcopy(m["layers"][0])))

    def test_R05_fact_coverage(self):
        self.assert_rule("R05", lambda m, d: m["fact_coverage"]["recreation_permission"].update(layer_ids=[]))

    def test_R10_coverage_geometry(self):
        self.assert_rule("R10", lambda m, d: d["coverage.json"].update(geometry=None))

    def test_R20_feature_collection(self):
        self.assert_rule("R20", lambda m, d: d["data.json"]["layers"]["water"].update(type="NotACollection"))

    def test_R21_duplicate_ids(self):
        self.assert_rule("R21", lambda m, d: d["data.json"]["layers"]["water"]["features"].append(copy.deepcopy(d["data.json"]["layers"]["water"]["features"][0])))

    def test_R22_geometry_constraints(self):
        for mutate in (lambda m, d: d["data.json"]["layers"]["water"]["features"][0].update(geometry=None), lambda m, d: d["data.json"]["layers"]["water"]["features"][0]["geometry"].update(coordinates=[2, 2]), lambda m, d: d["data.json"]["layers"]["water"]["features"][0]["geometry"].update(type="LineString")):
            self.assert_rule("R22", mutate)

    def test_R23_verification_method(self):
        for value in ("community_report", ""):
            self.assert_rule("R23", lambda m, d, value=value: d["data.json"]["layers"]["water"]["features"][0]["properties"]["evidence"].update(verification_method=value))
        def missing(m, d):
            del d["data.json"]["layers"]["water"]["features"][0]["properties"]["evidence"]["verification_method"]
        self.assert_rule("R23", missing)
        manifest, docs = self.base()
        docs["data.json"]["layers"]["water"]["features"][0]["properties"]["evidence"]["verification_method"] = None
        self.valid(manifest, docs)

    def test_R24_declared_url_boundary(self):
        self.assert_rule("R24", lambda m, d: d["data.json"]["layers"]["water"]["features"][0]["properties"]["evidence"].update(source_url="https://agency.example/source-extra"))

    def test_R25_last_verified(self):
        self.assert_rule("R25", lambda m, d: d["data.json"]["layers"]["water"]["features"][0]["properties"]["evidence"].update(last_verified="2026-01-01"))

    def test_R26_declared_properties(self):
        self.assert_rule("R26", lambda m, d: d["data.json"]["layers"]["water"]["features"][0]["properties"].update(unlisted="x"))

    def test_R27_positive_values_fail_closed(self):
        self.assert_rule("R27", lambda m, d: d["data.json"]["layers"]["water"]["features"][0]["properties"].update(camping_permission="allowed"))

    def test_R28_kind_rules(self):
        manifest, docs = self.base()
        manifest["layers"][0]["kind"] = "community_leads"
        docs["data.json"]["layers"]["water"]["features"][0]["properties"].update(needs_review=True, camping_permission="unknown")
        docs["data.json"]["layers"]["water"]["features"][0]["properties"]["evidence"]["verification_method"] = "source_fetch"
        with self.assertRaises(ContractError) as raised:
            self.valid(manifest, docs)
        self.assertEqual(raised.exception.rule, "R28")

    def test_R29_trail_activity_shape(self):
        def mutate(m, d):
            m["layers"][0].update(id="trails", kind="trails")
            m["fact_coverage"]["recreation_permission"]["layer_ids"] = ["trails"]
            m["layers"][0]["fields"]["source"] = ["activities"]
            d["data.json"]["layers"]["water"]["features"][0]["properties"]["activities"] = {}
        self.assert_rule("R29", mutate)

    def test_R30_transport_shape(self):
        self.assert_rule("R30", lambda m, d: d["data.json"]["status"].update(status="ok"))

    def test_R32_transport_count(self):
        self.assert_rule("R32", lambda m, d: d["data.json"]["status"].update(count=2))

    def test_R33_unavailable_retention(self):
        self.assert_rule("R33", lambda m, d: d["data.json"]["status"].update(status="unavailable", reason="offline"))

    def test_R40_place_list(self):
        manifest, docs = self.base()
        layer = manifest["layers"][0]
        layer.update(format="place_list", list_key="places", pointer="")
        for key in ("geometry_types", "allow_null_geometry", "extent_padding_deg", "fields", "spatial_precision"):
            layer.pop(key, None)
        docs["data.json"] = {"places": [{"id": "Bad ID", "coordinates": [0, 0]}], "status": {"status": "available", "last_retrieved_at": "2026-01-01T00:00:00Z", "count": 1}}
        with self.assertRaises(ContractError) as raised:
            self.valid(manifest, docs)
        self.assertEqual(raised.exception.rule, "R40")

    def test_R41_place_claim(self):
        manifest, docs = self.base()
        layer = manifest["layers"][0]
        layer.update(format="place_list", list_key="places", pointer="")
        for key in ("geometry_types", "allow_null_geometry", "extent_padding_deg", "fields", "spatial_precision"):
            layer.pop(key, None)
        docs["data.json"] = {"places": [{"id": "place-1", "coordinates": [0, 0], "facts": {"access": {"status": "supported"}}}], "status": {"status": "available", "last_retrieved_at": "2026-01-01T00:00:00Z", "count": 1}}
        with self.assertRaises(ContractError) as raised:
            self.valid(manifest, docs)
        self.assertEqual(raised.exception.rule, "R41")

    def test_R50_rules_registry(self):
        manifest, docs = self.base()
        manifest["rules"] = {"path": "rules.json"}
        docs["rules.json"] = {"rules": [{"id": "bad"}]}
        with self.assertRaises(ContractError) as raised:
            self.valid(manifest, docs)
        self.assertEqual(raised.exception.rule, "R50")


if __name__ == "__main__":
    unittest.main()
