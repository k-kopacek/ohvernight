import datetime as dt
import json
import math
import re
import sys
import unittest
from pathlib import Path
from urllib.parse import urlparse

from shapely.geometry import shape

V2 = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(V2 / "pipeline" / "scripts"))

from lib.validation import validate_bundle
from fetch_trails import ACTIVITIES


class PublishedDataTests(unittest.TestCase):
    @staticmethod
    def load(relative_path):
        return json.loads((V2 / relative_path).read_text())

    def assert_geometry(self, geometry):
        self.assertIsNotNone(geometry)
        parsed = shape(geometry)
        self.assertFalse(parsed.is_empty)
        self.assertTrue(parsed.is_valid)
        west, south, east, north = parsed.bounds
        self.assertGreaterEqual(west, -180)
        self.assertGreaterEqual(south, -90)
        self.assertLessEqual(east, 180)
        self.assertLessEqual(north, 90)
        return parsed

    def assert_coordinates(self, coordinates):
        self.assertIsInstance(coordinates, list)
        self.assertEqual(len(coordinates), 2)
        self.assertTrue(all(isinstance(value, (int, float)) and math.isfinite(value)
                            for value in coordinates))
        self.assertGreaterEqual(coordinates[0], -180)
        self.assertLessEqual(coordinates[0], 180)
        self.assertGreaterEqual(coordinates[1], -90)
        self.assertLessEqual(coordinates[1], 90)

    def assert_http_url(self, value):
        self.assertIn(urlparse(value).scheme, {"http", "https"})

    def assert_activity_records(self, feature):
        self.assertEqual(set(feature["properties"]["activities"]), set(ACTIVITIES))
        expected_fields = {"managed", "accpt", "disc", "restricted"}
        for record in feature["properties"]["activities"].values():
            self.assertEqual(set(record), expected_fields)
            self.assertTrue(all(value is None or isinstance(value, str)
                                for value in record.values()))

    def test_aspen_bundle_validates(self):
        validate_bundle(self.load("map-data-v2.json"))

    def test_aspen_trails_have_valid_geometry_and_activity_records(self):
        trails = self.load("trails.geojson")
        self.assertEqual(trails["type"], "FeatureCollection")
        self.assertIsInstance(trails["features"], list)
        self.assertTrue(trails["features"])

        aoi = shape(self.load("pipeline/config/aoi.geojson")["geometry"])
        west, south, east, north = aoi.bounds
        ids = set()
        for feature in trails["features"]:
            properties = feature["properties"]
            identifier = properties.get("id")
            self.assertIsInstance(identifier, str)
            self.assertTrue(identifier)
            self.assertNotIn(identifier, ids, f"duplicate trail id: {identifier}")
            ids.add(identifier)

            self.assertIn(feature["geometry"]["type"], {"LineString", "MultiLineString"})
            geometry = self.assert_geometry(feature["geometry"])
            feature_west, feature_south, feature_east, feature_north = geometry.bounds
            self.assertGreaterEqual(feature_west, west - 1e-6)
            self.assertGreaterEqual(feature_south, south - 1e-6)
            self.assertLessEqual(feature_east, east + 1e-6)
            self.assertLessEqual(feature_north, north + 1e-6)
            self.assert_activity_records(feature)

            evidence = properties["evidence"]
            self.assertTrue(evidence["source_url"].startswith(("http://", "https://")))
            self.assertTrue(evidence["agency"])
            self.assertIsInstance(evidence["retrieved_at"], str)

    def test_douglas_snapshot_has_valid_layers_and_geometry(self):
        snapshot = self.load("regions/douglas-co/research.json")
        self.assertEqual(snapshot["region"], "douglas-co")
        self.assertEqual(snapshot["schema_version"], 1)

        expected_layers = {"coverage", "trails", "roads", "recreation", "land",
                           "wilderness", "waterbodies", "waterways"}
        self.assertEqual(set(snapshot["layers"]), expected_layers)
        self.assertTrue(all(isinstance(layer.get("features"), list)
                            for layer in snapshot["layers"].values()))

        coverage = snapshot["layers"]["coverage"]["features"]
        self.assertEqual(len(coverage), 1)
        self.assertEqual(coverage[0]["properties"].get("GEOID"), "08035")
        coverage_geometry = self.assert_geometry(coverage[0]["geometry"])
        west, south, east, north = coverage_geometry.bounds

        geometry_types = {
            "trails": {"LineString", "MultiLineString"},
            "roads": {"LineString", "MultiLineString"},
            "waterways": {"LineString", "MultiLineString"},
            "land": {"Polygon", "MultiPolygon"},
            "wilderness": {"Polygon", "MultiPolygon"},
            "waterbodies": {"Polygon", "MultiPolygon"},
            "recreation": {"Point"},
        }
        ids = set()
        for layer_name, layer in snapshot["layers"].items():
            if layer_name == "coverage":
                continue
            for feature in layer["features"]:
                properties = feature["properties"]
                identifier = properties.get("id")
                self.assertIsInstance(identifier, str)
                self.assertTrue(identifier)
                self.assertNotIn(identifier, ids, f"duplicate Douglas feature id: {identifier}")
                ids.add(identifier)

                geometry = self.assert_geometry(feature["geometry"])
                self.assertIn(geometry.geom_type, geometry_types[layer_name])
                feature_west, feature_south, feature_east, feature_north = geometry.bounds
                self.assertGreaterEqual(feature_west, west - 1e-6)
                self.assertGreaterEqual(feature_south, south - 1e-6)
                self.assertLessEqual(feature_east, east + 1e-6)
                self.assertLessEqual(feature_north, north + 1e-6)

                evidence = properties["evidence"]
                self.assertTrue(evidence["source_url"].startswith("http"))
                if layer_name == "land":
                    self.assertIsInstance(properties.get("manager"), str)
                    self.assertTrue(properties["manager"])
                if layer_name == "trails":
                    self.assert_activity_records(feature)

    def test_place_inventories_have_safe_records(self):
        for relative_path in ("overnight-options.json", "ridb-options.json"):
            inventory = self.load(relative_path)
            self.assertEqual(inventory["schema_version"], 1)
            self.assertIsInstance(inventory["places"], list)
            ids = set()
            for place in inventory["places"]:
                identifier = place["id"]
                self.assertRegex(identifier, r"^[a-z0-9_-]+$")
                self.assertNotIn(identifier, ids)
                ids.add(identifier)
                self.assert_coordinates(place["coordinates"])
                self.assertIn(place["kind"], {"campground", "dispersed", "lodging"})
                self.assert_http_url(place["source"])
                self.assert_http_url(place["mapSource"])
                self.assertRegex(place["checked_on"], r"^\d{4}-\d{2}-\d{2}$")
                dt.date.fromisoformat(place["checked_on"])

                if relative_path == "ridb-options.json":
                    self.assertEqual(place["camping_permission"], "unknown")
                    self.assertIs(place["needs_review"], True)
                    self.assertTrue(place["ridb_facility_id"])

    def test_rules_registry_only_matches_unknown_permission_places(self):
        place_ids = set()
        ridb_facility_ids = set()
        for relative_path in ("overnight-options.json", "ridb-options.json"):
            for place in self.load(relative_path)["places"]:
                place_ids.add(place["id"])
                if place.get("ridb_facility_id"):
                    ridb_facility_ids.add(str(place["ridb_facility_id"]))
        registry = self.load("pipeline/config/rules-registry.json")
        for rule in registry["rules"]:
            for identifier in rule.get("place_ids", []):
                if identifier in place_ids:
                    continue
                match = re.fullmatch(r"ridb-(.+)", identifier)
                self.assertIsNotNone(match, f"unknown registry place id: {identifier}")
                self.assertIn(match.group(1), ridb_facility_ids,
                              f"unknown RIDB facility reference: {identifier}")
            self.assertEqual(rule["camping_permission"], "unknown")

    def test_destinations_have_unique_valid_coordinates(self):
        destinations = self.load("destinations.json")["resorts"]
        self.assertTrue(destinations)
        ids = [resort["id"] for resort in destinations]
        self.assertEqual(len(ids), len(set(ids)))
        for resort in destinations:
            self.assert_coordinates(resort["coordinates"])


if __name__ == "__main__":
    unittest.main()
