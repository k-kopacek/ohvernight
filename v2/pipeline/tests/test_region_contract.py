import copy
import csv
import hashlib
import json
import re
import shutil
import sys
import tempfile
import unittest
from collections import Counter
from pathlib import Path

V2 = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(V2 / "pipeline" / "scripts"))

from lib.region_contract import (ContractError, _display_transform_geometry,
                                 normalize_transport, validate_region, validate_region_data,
                                 validate_water_alias_file, validate_water_contract_data)


class RegionContractTests(unittest.TestCase):
    def load(self, relative):
        return json.loads((V2 / relative).read_text())

    def test_usgs_nhd_scope_strings_match_origin_main(self):
        expected = {
            "aspen": "Hydrography retained for setback screening. Feature type, flow permanence and size are not carried. A name does not indicate recreational usefulness, public access or seasonal flow.",
            "douglas-co": "Named waterbodies and flowlines only, selected by name. A display subset, not complete hydrology. A name does not indicate recreational usefulness, public access, fishing or paddling permission.",
        }
        for region_id, scope in expected.items():
            with self.subTest(region=region_id):
                manifest = self.load(f"regions/{region_id}/region.json")
                self.assertEqual(manifest["sources"]["usgs_nhd"]["scope"], scope)

    def test_real_water_features_do_not_carry_mislabeled_elevation(self):
        for manifest_path in (V2 / "regions").glob("*/region.json"):
            manifest = json.loads(manifest_path.read_text())
            for layer in manifest["layers"]:
                if layer.get("kind") != "water":
                    continue
                document = self.load(layer["path"])
                features = document["layers"][layer["id"]]["features"]
                mislabeled = [feature.get("properties", {}).get("id") for feature in features
                              if "elevation_ft" in feature.get("properties", {})]
                self.assertEqual(mislabeled, [], f"{manifest['region']['id']}/{layer['id']}")

    def test_committed_pre_m4_water_ids_are_pinned_once_in_canonical_data(self):
        with (V2.parent / "docs/research/m4-water/nhd-snapshot-id-map.csv").open() as handle:
            pins = list(csv.DictReader(handle))
        pinned_by_region = {}
        for row in pins:
            if row["legacy_id"]:
                pinned_by_region.setdefault(row["region"], Counter())[row["legacy_id"]] += 1
        manifests = sorted((V2 / "regions").glob("*/region.json"))
        for manifest_path in manifests:
            manifest = json.loads(manifest_path.read_text())
            region = manifest["region"]["id"]
            actual = Counter()
            for layer in manifest["layers"]:
                if layer.get("kind") != "water":
                    continue
                document = self.load(layer["path"])
                features = document["layers"][layer["id"]]["features"]
                for feature in features:
                    actual.update(feature["properties"].get("legacy_ids", []))
            expected = pinned_by_region.get(region, Counter())
            self.assertTrue(all(count == 1 for count in expected.values()), region)
            self.assertEqual(actual, expected, region)

    def test_real_regions_validate_and_pin_status_gaps(self):
        manifests = sorted((V2 / "regions").glob("*/region.json"))
        self.assertEqual({p.parent.name for p in manifests}, {"aspen", "douglas-co"})
        reports = {p.parent.name: validate_region(p, V2) for p in manifests}
        self.assertEqual(reports["aspen"]["unrecorded_status_layers"], ["trails"])
        self.assertEqual(reports["douglas-co"]["unrecorded_status_layers"], ["roads", "trails"])
        self.assertEqual(set(reports["aspen"]["legacy_transport"]), {"land_ownership", "wilderness", "mvum_roads", "hydrology", "fire_restriction_stage", "dispersed_corridors", "dispersed_corridor_points", "leads", "reviewed_sites", "ridb_options"})

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
            if path.parent.name == "aspen":
                data = self.load("map-data-v2.json")
                self.assertTrue(set(data["layers"]) <= {layer["id"] for layer in manifest["layers"]})
            else:
                data = self.load("regions/douglas-co/research.json")
                self.assertTrue(set(data["layers"]) - {"coverage"} <= {layer["id"] for layer in manifest["layers"]})

    def test_fact_coverage_statements_are_normative_literals(self):
        expected = {
            "aspen": {
                "ownership": "Limited-scale managing-agency polygons only. They are not parcels or surveyed boundaries. A Private label repeats the source's generalized classification and is not a parcel-level finding. Land outside a federal polygon is not thereby private, and unshaded land is unknown.",
                "public_access": "No public-access evidence is loaded. Ownership and access are separate questions: managing-agency context, a mapped road or trail, or nearby public land does not establish that the public may enter or cross land.",
                "camping_permission": "No camping permission is confirmed anywhere in this region. No listed facility, research area or rule record asserts it; wherever the field is present its value is unknown. A listing shows that a facility exists, not that a given setup may stay.",
                "closures": "No closure or fire-restriction status is confirmed. The county page monitor detects page changes only and the wildlife source is unavailable. No mapped closure does not mean no closure.",
                "restrictions": "One reviewed rule record exists, for the agency-listed Lincoln Creek dispersed sites. All other stay limits, seasons, permits and orders are unknown.",
                "road_access": "USFS motor-vehicle designations, evaluated for the trip recorded on each feature and not for the visitor's trip. Current conditions, snow, passability and the full approach are unknown.",
                "trail_access": "USFS published trail-use strings, kept verbatim. Not evaluated against dates, closures or current conditions.",
                "recreation_permission": "No recreational-use permission is loaded. A mapped or named water feature does not establish public access, fishing, paddling or swimming permission, or that the water is usable for recreation. Distances to trails, roads and water are straight-line and are not connections.",
            },
            "douglas-co": {
                "ownership": "Five limited-scale management polygons only. They are not parcels or surveyed boundaries. The PVT code repeats the source's generalized classification and is not a parcel-level finding. Land outside a federal polygon is not thereby private, and unshaded land is unknown.",
                "public_access": "No public-access evidence is loaded. Ownership and access are separate questions: managing-agency context, a mapped road or trail, or nearby public land does not establish that the public may enter or cross land.",
                "camping_permission": "No camping permission is confirmed. A recreation-site record shows that a facility is listed, not that it is open or that a given setup may stay.",
                "closures": "No closure or fire-restriction status is loaded. The linked county page covers county jurisdiction only; federal orders must be checked separately.",
                "restrictions": "No reviewed stay limits, seasons, permits or orders are loaded.",
                "road_access": "USFS road geometry only. Vehicle and season designations are not evaluated; access status is unknown on every feature.",
                "trail_access": "USFS published trail-use strings, kept verbatim. Segments are clipped at the county boundary and are not complete routes. Not evaluated against closures or current conditions.",
                "recreation_permission": "No recreational-use permission is loaded. A mapped or named water feature does not establish public access, fishing, paddling or swimming permission, or that the water is usable for recreation. Distances to campgrounds, trailheads and trails are straight-line and are not connections.",
            },
        }
        for path in (V2 / "regions").glob("*/region.json"):
            manifest = self.load(path.relative_to(V2))
            self.assertEqual({key: value["statement"] for key, value in manifest["fact_coverage"].items()}, expected[path.parent.name])

    def test_normalize_transport_aliases(self):
        vectors = self.load("pipeline/tests/fixtures/transport-vectors.json")
        for vector in vectors:
            normalized, used = normalize_transport(vector["input"])
            self.assertEqual(normalized, vector["record"])
            self.assertEqual(used, vector["used"])

    def test_pinned_real_transport_alias_sets(self):
        aspen = validate_region(V2 / "regions/aspen/region.json", V2)
        douglas = validate_region(V2 / "regions/douglas-co/region.json", V2)
        self.assertEqual({alias for layer, aliases in aspen["legacy_transport"].items() if layer != "ridb_options" for alias in aliases}, {"completed_at"})
        self.assertEqual({alias for aliases in douglas["legacy_transport"].values() for alias in aliases}, {"retrieved_at"})
        self.assertEqual(set(aspen["legacy_transport"]["ridb_options"]), {"inferred_retrieval", "last_confirmed_at"})
        ridb = self.load("ridb-options.json")["source_status"]
        self.assertEqual(set(normalize_transport(ridb)[1]), {"inferred_retrieval", "last_confirmed_at"})

    def test_confidence_is_not_consumed_by_browser_code(self):
        pattern = re.compile(r"\.confidence(?![-\w])|\[['\"]confidence['\"]\]")
        for path in list((V2).glob("*.js")) + list((V2 / "regions").glob("*/*.js")) + list((V2 / "explore").glob("*.js")):
            self.assertIsNone(pattern.search(path.read_text()), str(path))

    def test_validator_is_clock_independent(self):
        source = (V2 / "pipeline" / "scripts" / "lib" / "region_contract.py").read_text()
        for forbidden in ("datetime.now", "utcnow", "date.today", "import time"):
            self.assertNotIn(forbidden, source)

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

    def display_base(self, geometry=None, geometry_types=None):
        manifest, docs = self.base()
        if geometry is not None:
            docs["data.json"]["layers"]["water"]["features"][0]["geometry"] = copy.deepcopy(geometry)
            manifest["layers"][0]["geometry_types"] = geometry_types or [geometry["type"]]
        manifest["coverage"]["display"] = {"path": "regions/synthetic/display/coverage.geojson"}
        manifest["layers"][0]["display"] = {"path": "regions/synthetic/display/water.geojson"}
        canonical = docs["data.json"]["layers"]["water"]
        evidence = copy.deepcopy(canonical["features"][0]["properties"]["evidence"])
        display_geometry, dropped = _display_transform_geometry(canonical["features"][0]["geometry"])
        display = {"type": "FeatureCollection", "layer_id": "water", "evidence_table": [evidence], "features": [{
            "type": "Feature", "geometry": display_geometry,
            "properties": {"id": "water-1", "evidence": 0},
        }]}
        coverage = docs["coverage.json"]
        coverage_display = {"type": "FeatureCollection", "layer_id": "coverage", "evidence_table": [], "features": [{
            "type": "Feature", "geometry": copy.deepcopy(coverage["geometry"]), "properties": copy.deepcopy(coverage["properties"]),
        }]}
        def encoded(value):
            return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode()
        entries = []
        for layer_id, path, value, canonical_path in (("water", "regions/synthetic/display/water.geojson", display, "data.json"), ("coverage", "regions/synthetic/display/coverage.geojson", coverage_display, "coverage.json")):
            data = encoded(value)
            entries.append({"layer_id": layer_id, "path": path, "feature_count": 1, "source_feature_count": 1,
                            "dropped_degenerate_parts": dropped if layer_id == "water" else 0,
                            "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(),
                            "canonical_sha256": hashlib.sha256(encoded(docs[canonical_path])).hexdigest()})
        docs["regions/synthetic/display/water.geojson"] = display
        docs["regions/synthetic/display/coverage.geojson"] = coverage_display
        docs["regions/synthetic/display/index.json"] = {"region_id": "synthetic", "artifacts": entries,
                                                       "transport": {"water": copy.deepcopy(docs["data.json"]["status"])}}
        return manifest, docs

    def test_display_transport_R65_changed_value(self):
        manifest, docs = self.display_base()
        self.valid(manifest, docs)
        docs["regions/synthetic/display/index.json"]["transport"]["water"]["count"] = 2
        with self.assertRaises(ContractError) as raised:
            self.valid(manifest, docs)
        self.assertEqual(raised.exception.rule, "R65")

    def test_display_transport_R65_missing_key(self):
        manifest, docs = self.display_base()
        docs["regions/synthetic/display/index.json"]["transport"].pop("water")
        with self.assertRaises(ContractError) as raised:
            self.valid(manifest, docs)
        self.assertEqual(raised.exception.rule, "R65")

    def test_display_transport_R65_scalar_type_change(self):
        for value in (True, 1.0):
            with self.subTest(value=value):
                manifest, docs = self.display_base()
                docs["regions/synthetic/display/index.json"]["transport"]["water"]["count"] = value
                with self.assertRaises(ContractError) as raised:
                    self.valid(manifest, docs)
                self.assertEqual(raised.exception.rule, "R65")

    def test_display_properties_R62_scalar_type_change(self):
        manifest, docs = self.display_base()
        docs["data.json"]["layers"]["water"]["features"][0]["properties"]["numeric_property"] = 1
        docs["regions/synthetic/display/water.geojson"]["features"][0]["properties"]["numeric_property"] = True
        entry = docs["regions/synthetic/display/index.json"]["artifacts"][0]
        entry["canonical_sha256"] = hashlib.sha256((json.dumps(docs["data.json"], ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode()).hexdigest()
        self.refresh_display_hash(docs, "water")
        with self.assertRaises(ContractError) as raised:
            self.valid(manifest, docs)
        self.assertEqual(raised.exception.rule, "R62")

    def test_display_transport_R65_extra_null_status_key(self):
        manifest, docs = self.display_base()
        manifest["layers"][0]["status_ref"] = None
        with self.assertRaises(ContractError) as raised:
            self.valid(manifest, docs)
        self.assertEqual(raised.exception.rule, "R65")

    def refresh_display_hash(self, docs, layer_id):
        value = docs[f"regions/synthetic/display/{layer_id}.geojson"]
        data = (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode()
        entry = next(item for item in docs["regions/synthetic/display/index.json"]["artifacts"] if item["layer_id"] == layer_id)
        entry["bytes"] = len(data)
        entry["sha256"] = hashlib.sha256(data).hexdigest()

    def water_contract_base(self):
        manifest = {"region": {"id": "synthetic"}}
        def water_feature(ident, source_id, legacy_ids):
            return {"type": "Feature", "geometry": {"type": "LineString", "coordinates": [[0, 0], [1, 1]]},
                    "properties": {"id": ident, "name": "River", "evidence": {}, "source_id": source_id,
                                   "source_namespace": "usgs_nhd", "ftype": 460, "fcode": 46006,
                                   "source_layer": "flowline", "water_class": "stream",
                                   "hydro_category": "perennial", "legacy_ids": legacy_ids}}
        canonical = [("waterways", water_feature("nhd-A", "{A}", ["old-a"])),
                     ("waterways", water_feature("nhd-B", "{B}", []))]
        display = [("waterways", copy.deepcopy(canonical[0][1]))]
        config = self.load("pipeline/config/water_display.json")
        aliases = {"old-a": "nhd-A"}
        return manifest, canonical, config, aliases, display

    def assert_water_rule(self, rule, mutate):
        manifest, canonical, config, aliases, display = self.water_contract_base()
        validate_water_contract_data(manifest, canonical, config, aliases, display)
        mutate(manifest, canonical, config, aliases, display)
        with self.assertRaises(ContractError) as raised:
            validate_water_contract_data(manifest, canonical, config, aliases, display)
        self.assertEqual(raised.exception.rule, rule)

    def test_water_R66_rejects_id_not_derived_from_source(self):
        self.assert_water_rule("R66", lambda m, c, cfg, a, d: c[0][1]["properties"].update(id="row-1"))

    def test_water_R67_rejects_wrong_fixed_table_classification(self):
        self.assert_water_rule("R67", lambda m, c, cfg, a, d: c[0][1]["properties"].update(water_class="canal_ditch"))

    def test_water_R68_rejects_missing_display_alias(self):
        self.assert_water_rule("R68", lambda m, c, cfg, a, d: a.clear())

    def test_water_R68_rejects_alias_for_undisplayed_feature(self):
        self.assert_water_rule("R68", lambda m, c, cfg, a, d: a.update({"old-hidden": "nhd-B"}))

    def test_water_R68_rejects_alias_to_wrong_display_id(self):
        self.assert_water_rule("R68", lambda m, c, cfg, a, d: a.update({"old-a": "nhd-B"}))

    def test_water_R68_rejects_legacy_id_on_two_canonical_features(self):
        self.assert_water_rule("R68", lambda m, c, cfg, a, d: c[1][1]["properties"].update(legacy_ids=["old-a"]))

    def test_water_R68_rejects_legacy_id_equal_to_current_water_id(self):
        manifest, canonical, config, aliases, display = self.water_contract_base()
        canonical[0][1]["properties"]["legacy_ids"] = ["nhd-B"]
        with self.assertRaisesRegex(ContractError, "legacy ID nhd-B equals the ID of a current water feature") as raised:
            validate_water_contract_data(manifest, canonical, config, aliases, display)
        self.assertEqual(raised.exception.rule, "R68")

    def test_water_R68_rejects_stale_alias_file_hash(self):
        document = {"region_id": "synthetic", "water_id_aliases": {"old-a": "nhd-A"}}
        raw = (json.dumps(document, sort_keys=True, separators=(",", ":")) + "\n").encode()
        index = {"water_aliases": {"path": "regions/synthetic/display/water-aliases.json",
                                   "bytes": len(raw), "sha256": "0" * 64}}
        with self.assertRaises(ContractError) as raised:
            validate_water_alias_file(index, document, raw, "synthetic")
        self.assertEqual(raised.exception.rule, "R68")

    def test_water_R68_rejects_alias_map_left_in_index(self):
        index = {"water_id_aliases": {"old-a": "nhd-A"}}
        with self.assertRaises(ContractError) as raised:
            validate_water_alias_file(index, {}, b"", "synthetic")
        self.assertEqual(raised.exception.rule, "R68")

    def test_water_R75_rejects_activity_property(self):
        self.assert_water_rule("R75", lambda m, c, cfg, a, d: c[0][1]["properties"].update(fishing="allowed"))

    def test_display_contract_rules_R60_to_R64(self):
        def assert_display_rule(rule, mutate):
            manifest, docs = self.display_base()
            self.valid(manifest, docs)
            mutate(manifest, docs)
            with self.assertRaises(ContractError) as raised:
                self.valid(manifest, docs)
            self.assertEqual(raised.exception.rule, rule)
        assert_display_rule("R60", lambda m, d: m["layers"][0]["display"].update(path="regions/synthetic/other/water.geojson"))
        def missing_feature(m, d):
            d["regions/synthetic/display/water.geojson"]["features"] = []
            d["regions/synthetic/display/index.json"]["artifacts"][0]["feature_count"] = 0
            self.refresh_display_hash(d, "water")
        assert_display_rule("R61", missing_feature)
        def changed_evidence(m, d):
            d["regions/synthetic/display/water.geojson"]["evidence_table"][0]["agency"] = "Different"
            self.refresh_display_hash(d, "water")
        assert_display_rule("R62", changed_evidence)
        def changed_coordinate(m, d):
            d["regions/synthetic/display/water.geojson"]["features"][0]["geometry"]["coordinates"] = [0.5, 0.5]
            self.refresh_display_hash(d, "water")
        assert_display_rule("R63", changed_coordinate)
        def malformed_ring(m, d):
            m["layers"][0]["geometry_types"] = ["Polygon"]
            d["data.json"]["layers"]["water"]["features"][0]["geometry"] = {"type": "Polygon", "coordinates": [[[0, 0], [1, 0], [0, 0]]]}
            d["regions/synthetic/display/water.geojson"]["features"][0]["geometry"] = copy.deepcopy(d["data.json"]["layers"]["water"]["features"][0]["geometry"])
            entry = d["regions/synthetic/display/index.json"]["artifacts"][0]
            entry["canonical_sha256"] = hashlib.sha256((json.dumps(d["data.json"], ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode()).hexdigest()
            self.refresh_display_hash(d, "water")
        assert_display_rule("R63", malformed_ring)
        def malformed_line(m, d):
            m["layers"][0]["geometry_types"] = ["LineString"]
            d["data.json"]["layers"]["water"]["features"][0]["geometry"] = {"type": "LineString", "coordinates": [[0, 0]]}
            d["regions/synthetic/display/water.geojson"]["features"][0]["geometry"] = {"type": "LineString", "coordinates": [[0, 0]]}
            entry = d["regions/synthetic/display/index.json"]["artifacts"][0]
            entry["canonical_sha256"] = hashlib.sha256((json.dumps(d["data.json"], ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode()).hexdigest()
            self.refresh_display_hash(d, "water")
        assert_display_rule("R63", malformed_line)
        assert_display_rule("R63", lambda m, d: d["regions/synthetic/display/index.json"]["artifacts"][0].update(dropped_degenerate_parts=1))
        manifest, docs = self.display_base(
            {"type": "MultiLineString", "coordinates": [[[0, 0], [0.0000001, 0.0000001]], [[0, 0], [1, 1]]]},
            ["MultiLineString"],
        )
        self.assertEqual(docs["regions/synthetic/display/index.json"]["artifacts"][0]["dropped_degenerate_parts"], 1)
        self.valid(manifest, docs)
        assert_display_rule("R64", lambda m, d: d["data.json"]["layers"]["water"]["features"][0]["properties"].update(name="changed"))

    def test_validate_region_without_display_artifacts(self):
        manifest, docs = self.base()
        self.valid(manifest, docs)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            region_dir = root / "regions" / "synthetic"
            region_dir.mkdir(parents=True)
            (region_dir / "region.json").write_text(json.dumps(manifest))
            (root / "coverage.json").write_text(json.dumps(docs["coverage.json"]))
            (root / "data.json").write_text(json.dumps(docs["data.json"]))
            validate_region(region_dir / "region.json", root)
        with tempfile.TemporaryDirectory() as tmp:
            manifest = self.load("regions/aspen/region.json")
            manifest["coverage"].pop("display", None)
            for layer in manifest["layers"]:
                layer.pop("display", None)
            path = Path(tmp) / "aspen" / "region.json"
            path.parent.mkdir()
            path.write_text(json.dumps(manifest))
            validate_region(path, V2)
    def test_R01_manifest_enum_and_shape(self):
        self.assert_rule("R01", lambda m, d: m["region"].update(status="verified"))
        self.assert_rule("R01", lambda m, d: m["fact_coverage"]["ownership"].update(state="complete"))
        self.assert_rule("R01", lambda m, d: m["fact_coverage"].update(extra={"state": "none", "layer_ids": [], "official_urls": [], "statement": "x"}))
        self.assert_rule("R01", lambda m, d: m["sources"]["agency"].update(source_urls=[]))
        def missing_dimension(m, d):
            del m["fact_coverage"]["ownership"]
        self.assert_rule("R01", missing_dimension)

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

    def test_R03_status_ref_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            good = root / "aspen" / "region.json"
            good.parent.mkdir()
            manifest = self.load("regions/aspen/region.json")
            manifest["layers"][0]["status_ref"]["path"] = "missing-status.json"
            good.write_text(json.dumps(manifest))
            with self.assertRaises(ContractError) as raised:
                validate_region(good, V2)
            self.assertEqual(raised.exception.rule, "R03")

    def test_R04_source_and_layer_ids(self):
        self.assert_rule("R04", lambda m, d: m["layers"].append(copy.deepcopy(m["layers"][0])))

    def test_R04_undeclared_source(self):
        self.assert_rule("R04", lambda m, d: m["layers"][0]["source_ids"].append("missing"))

    def test_R05_fact_coverage(self):
        self.assert_rule("R05", lambda m, d: m["fact_coverage"]["recreation_permission"].update(layer_ids=[]))

    def test_R05_reviewed_partial_requires_reviewed_feature(self):
        manifest, docs = self.base()
        reviewed = copy.deepcopy(manifest["layers"][0])
        reviewed.update(id="reviewed_sites", kind="reviewed_sites", pointer="/layers/reviewed_sites")
        manifest["layers"].append(reviewed)
        docs["data.json"]["layers"]["reviewed_sites"] = {"type": "FeatureCollection", "features": []}
        manifest["fact_coverage"]["restrictions"].update(state="reviewed_partial", layer_ids=["reviewed_sites"])
        with self.assertRaises(ContractError) as raised:
            self.valid(manifest, docs)
        self.assertEqual(raised.exception.rule, "R05")

        feature = copy.deepcopy(docs["data.json"]["layers"]["water"]["features"][0])
        feature["properties"]["id"] = "reviewed-1"
        docs["data.json"]["layers"]["reviewed_sites"]["features"].append(feature)
        manifest["fact_coverage"]["restrictions"]["layer_ids"] = ["water"]
        self.valid(manifest, docs)

    def test_R10_coverage_geometry(self):
        self.assert_rule("R10", lambda m, d: d["coverage.json"].update(geometry=None))

    def test_R20_feature_collection(self):
        self.assert_rule("R20", lambda m, d: d["data.json"]["layers"]["water"].update(type="NotACollection"))

    def test_R21_duplicate_ids(self):
        self.assert_rule("R21", lambda m, d: d["data.json"]["layers"]["water"]["features"].append(copy.deepcopy(d["data.json"]["layers"]["water"]["features"][0])))

    def test_R22_geometry_constraints(self):
        for mutate in (lambda m, d: d["data.json"]["layers"]["water"]["features"][0].update(geometry=None), lambda m, d: d["data.json"]["layers"]["water"]["features"][0]["geometry"].update(coordinates=[2, 2]), lambda m, d: d["data.json"]["layers"]["water"]["features"][0]["geometry"].update(type="LineString")):
            self.assert_rule("R22", mutate)

    def test_R22_empty_geometry_types_reject_non_null_geometry(self):
        def mutate(m, d):
            m["layers"][0].update(geometry_types=[], allow_null_geometry=True)
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

    def test_R23_requires_valid_full_rfc3339_timestamp(self):
        for value in ("2026-01-01", "2026-13-45T99:99:99Z"):
            self.assert_rule("R23", lambda m, d, value=value: d["data.json"]["layers"]["water"]["features"][0]["properties"]["evidence"].update(retrieved_at=value))

    def test_R24_declared_url_boundary(self):
        self.assert_rule("R24", lambda m, d: d["data.json"]["layers"]["water"]["features"][0]["properties"]["evidence"].update(source_url="https://agency.example/source-extra"))

    def test_R24_undeclared_host_and_prefix_boundary(self):
        self.assert_rule("R24", lambda m, d: d["data.json"]["layers"]["water"]["features"][0]["properties"]["evidence"].update(source_url="https://other.example/source"))
        def prefix(m, d):
            m["sources"]["agency"]["source_urls"] = ["https://agency.example/MapServer/1"]
            d["data.json"]["layers"]["water"]["features"][0]["properties"]["evidence"]["source_url"] = "https://agency.example/MapServer/12"
        self.assert_rule("R24", prefix)

    def test_R25_last_verified(self):
        self.assert_rule("R25", lambda m, d: d["data.json"]["layers"]["water"]["features"][0]["properties"]["evidence"].update(last_verified="2026-01-01"))

    def test_R26_declared_properties(self):
        self.assert_rule("R26", lambda m, d: d["data.json"]["layers"]["water"]["features"][0]["properties"].update(unlisted="x"))
        self.assert_rule("R26", lambda m, d: m["layers"][0]["fields"]["source"].append("name"))

    def test_R27_positive_values_fail_closed(self):
        self.assert_rule("R27", lambda m, d: d["data.json"]["layers"]["water"]["features"][0]["properties"].update(camping_permission="allowed"))

    def test_R27_reserved_values_and_types(self):
        mutations = [
            lambda m, d: d["data.json"]["layers"]["water"]["features"][0]["properties"].update(camping_permission="supported_for_trip"),
            lambda m, d: d["data.json"]["layers"]["water"]["features"][0]["properties"].update(access_status="designated_open"),
            lambda m, d: d["data.json"]["layers"]["water"]["features"][0]["properties"].update(land_class="public"),
            lambda m, d: d["data.json"]["layers"]["water"]["features"][0]["properties"].update(road_conditions="open"),
            lambda m, d: d["data.json"]["layers"]["water"]["features"][0]["properties"].update(name=5),
            lambda m, d: d["data.json"]["layers"]["water"]["features"][0]["properties"].update(needs_review="yes"),
            lambda m, d: d["data.json"]["layers"]["water"]["features"][0]["properties"].update(access_reason=5),
            lambda m, d: d["data.json"]["layers"]["water"]["features"][0]["properties"].update(actual_site_confirmed="no"),
            lambda m, d: d["data.json"]["layers"]["water"]["features"][0]["properties"].update(evaluated_trip={"x": 1}),
        ]
        for mutate in mutations:
            self.assert_rule("R27", mutate)

    def test_R28_kind_rules(self):
        manifest, docs = self.base()
        manifest["layers"][0]["kind"] = "community_leads"
        docs["data.json"]["layers"]["water"]["features"][0]["properties"].update(needs_review=True, camping_permission="unknown")
        docs["data.json"]["layers"]["water"]["features"][0]["properties"]["evidence"]["verification_method"] = "source_fetch"
        with self.assertRaises(ContractError) as raised:
            self.valid(manifest, docs)
        self.assertEqual(raised.exception.rule, "R28")

    def test_R28_kind_mutations(self):
        def research(m, d):
            m["layers"][0]["kind"] = "research_areas"
            d["data.json"]["layers"]["water"]["features"][0]["properties"].update(needs_review=False, camping_permission="unknown", actual_site_confirmed=False, evaluated_trip={"arrive": "2026-01-01", "depart": "2026-01-02", "vehicle": "passenger_car"})
        self.assert_rule("R28", research)
        def monitor(m, d):
            m["layers"][0]["kind"] = "restriction_monitor"
            m["layers"][0]["fields"]["source"] = ["type", "status", "stage", "last_confirmed_at", "max_age_hours"]
            props = d["data.json"]["layers"]["water"]["features"][0]["properties"]
            props.update(needs_review=True, status="confirmed", stage="2", last_confirmed_at="2026-01-01T00:00:00Z", max_age_hours=24)
            props["evidence"]["verification_method"] = "html_change_monitor"
        self.assert_rule("R28", monitor)
        # must_be_empty must fail with a feature, not after deleting it.
        self.assert_rule("R28", lambda m, d: m["layers"][0].update(must_be_empty=True))
        def lead(m, d):
            m["layers"][0]["kind"] = "community_leads"
            d["data.json"]["layers"]["water"]["features"][0]["properties"].update(needs_review=False, camping_permission="unknown")
            d["data.json"]["layers"]["water"]["features"][0]["properties"]["evidence"]["verification_method"] = None
        self.assert_rule("R28", lead)
        def empty_classification(m, d):
            m["layers"][0].update(kind="land_management", classification_source_field="manager")
            m["layers"][0]["fields"]["source"] = ["manager"]
            d["data.json"]["layers"]["water"]["features"][0]["properties"]["manager"] = ""
        self.assert_rule("R28", empty_classification)
        def private_mismatch(m, d):
            m["layers"][0].update(kind="land_management", classification_source_field="raw_code")
            m["layers"][0]["fields"] = {"source": ["raw_code"], "derived": ["manager"]}
            props = d["data.json"]["layers"]["water"]["features"][0]["properties"]
            props["raw_code"] = "LG"
            props["manager"] = "Private"
        self.assert_rule("R28", private_mismatch)

    def test_R29_trail_activity_shape(self):
        def mutate(m, d):
            m["layers"][0].update(id="trails", kind="trails")
            m["fact_coverage"]["recreation_permission"]["layer_ids"] = ["trails"]
            m["layers"][0]["fields"]["source"] = ["activities"]
            d["data.json"]["layers"]["water"]["features"][0]["properties"]["activities"] = {}
        self.assert_rule("R29", mutate)

        def kind_not_id(m, d):
            m["layers"][0].update(id="trail-context", kind="trails")
            m["fact_coverage"]["recreation_permission"]["layer_ids"] = ["trail-context"]
            m["layers"][0]["fields"]["source"] = ["activities"]
            d["data.json"]["layers"]["water"]["features"][0]["properties"]["activities"] = {}
        self.assert_rule("R29", kind_not_id)

    def test_R30_transport_shape(self):
        self.assert_rule("R30", lambda m, d: d["data.json"]["status"].update(status="ok"))
        self.assert_rule("R30", lambda m, d: d["data.json"]["status"].update(status="available", last_retrieved_at=None))
        self.assert_rule("R30", lambda m, d: d["data.json"]["status"].update(status="unavailable", reason=None))
        self.assert_rule("R30", lambda m, d: d["data.json"].update(status=[]))

    def test_R31_reports_non_curated_layer_without_status_reference(self):
        manifest, docs = self.base()
        manifest["layers"][0]["status_ref"] = None

        report = self.valid(manifest, docs)

        self.assertEqual(report["unrecorded_status_layers"], ["water"])

    def test_R32_transport_count(self):
        self.assert_rule("R32", lambda m, d: d["data.json"]["status"].update(count=2))

    def test_R33_unavailable_retention(self):
        self.assert_rule("R33", lambda m, d: d["data.json"]["status"].update(status="unavailable", reason="offline"))

    def test_place_list_transport_rules_and_alias_report(self):
        manifest, docs = self.base()
        layer = manifest["layers"][0]
        layer.update(format="place_list", list_key="places", pointer="")
        for key in ("geometry_types", "allow_null_geometry", "extent_padding_deg", "fields", "spatial_precision"):
            layer.pop(key, None)
        docs["data.json"] = {"places": [{"id": "place-1", "coordinates": [0, 0]}], "status": {"status": "available", "last_checked_at": "2026-01-01T00:00:00Z", "last_confirmed_at": "2026-01-01T00:00:00Z", "count": 1}}
        report = self.valid(manifest, docs)
        self.assertEqual(report["legacy_transport"]["water"], ["inferred_retrieval", "last_confirmed_at"])
        for mutate, rule in ((lambda: docs["data.json"]["status"].update(status="ok"), "R30"), (lambda: docs["data.json"]["status"].update(count=2), "R32")):
            mutate()
            with self.assertRaises(ContractError) as raised:
                self.valid(manifest, docs)
            self.assertEqual(raised.exception.rule, rule)
            docs["data.json"]["status"].update(status="available", count=1)

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
        manifest, docs = self.base()
        manifest["rules"] = {"path": "rules.json"}
        docs["rules.json"] = {"rules": [{"id": "rule", "scope": "x", "source_url": "https://example.org", "last_confirmed_at": "2026-01-01T00:00:00Z", "max_age_hours": 24, "camping_permission": "unknown", "place_ids": ["no-such-place"]}]}
        with self.assertRaises(ContractError) as raised:
            self.valid(manifest, docs)
        self.assertEqual(raised.exception.rule, "R50")


if __name__ == "__main__":
    unittest.main()
