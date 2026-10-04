import json
import sys
import unittest
import importlib.util
from pathlib import Path
from shapely.geometry import mapping, Polygon
from lib.validation import validate_bundle
from lib.region_contract import ContractError, validate_region_data

V2 = Path(__file__).resolve().parents[2]
SCRIPTS = V2 / "pipeline" / "scripts"
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(0, str(SCRIPTS / "lib"))

_spec = importlib.util.spec_from_file_location("ingest_leads", SCRIPTS / "08_ingest_leads.py")
_module = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_module)
normalize = _module.normalize


class CommunityLeadTests(unittest.TestCase):
    def setUp(self):
        self.lead = {"lon": 0, "lat": 0, "name": "reported", "notes": "A report", "source_url": "https://example.org/report", "reported_by": "Reporter", "reported_at": "2026-01-01T00:00:00Z"}
        self.corridor = {"type": "Feature", "geometry": mapping(Polygon([[-1, -1], [1, -1], [1, 1], [-1, 1], [-1, -1]])), "properties": {"id": "corridor-1"}}

    def test_normalized_lead_is_unverified(self):
        feature = normalize([self.lead], [self.corridor])[0]
        props = feature["properties"]
        self.assertTrue(props["matched_candidate_ids"])
        self.assertIsNone(props["evidence"]["verification_method"])
        self.assertTrue(props["needs_review"])
        self.assertEqual(props["camping_permission"], "unknown")
        self.assertEqual(props["site_type"], "dispersed_lead_unverified")
        self.assertIsNone(props["evidence"]["last_verified"])
        self.assertEqual(props["evidence"]["confidence"], "unverified")

    def test_intersection_does_not_change_lead_semantics(self):
        inside = normalize([self.lead], [self.corridor])[0]["properties"]
        outside = normalize([self.lead], [])[0]["properties"]
        for key in ("needs_review", "camping_permission", "site_type"):
            self.assertEqual(inside[key], outside[key])
        for key in set(inside["evidence"]) - {"retrieved_at"}:
            self.assertEqual(inside["evidence"][key], outside["evidence"][key])
        self.assertEqual(inside["evidence"]["confidence"], outside["evidence"]["confidence"])
        self.assertEqual(inside["evidence"]["last_verified"], outside["evidence"]["last_verified"])
        self.assertNotEqual(inside["matched_candidate_ids"], outside["matched_candidate_ids"])

    def test_origin_is_preserved_without_new_evidence_field(self):
        props = normalize([self.lead], [])[0]["properties"]
        evidence = props["evidence"]
        self.assertEqual(evidence["source_url"], self.lead["source_url"])
        self.assertEqual(evidence["agency"], self.lead["reported_by"])
        self.assertEqual(evidence["reported_at"], self.lead["reported_at"])
        self.assertEqual(set(evidence), {"source_url", "agency", "retrieved_at", "last_verified", "confidence", "verification_method", "notes", "reported_at"})

    def test_bundle_schema_accepts_null_lead_without_site_feed_entry(self):
        feature = normalize([self.lead], [])[0]
        bundle = json.loads((V2 / "map-data-v2.json").read_text())
        bundle["layers"]["leads"]["features"].append(feature)
        validate_bundle(bundle)
        self.assertNotIn(feature["properties"]["id"], {place["id"] for place in bundle["site_feed"]["places"]})

    def test_contract_accepts_null_and_rejects_community_report(self):
        from test_region_contract import RegionContractTests
        helper = RegionContractTests()
        manifest, docs = helper.base()
        manifest["layers"][0]["kind"] = "community_leads"
        manifest["layers"][0]["fields"] = {"source": ["notes"], "derived": ["site_type", "matched_candidate_ids"]}
        manifest["sources"]["agency"]["source_urls"] = ["https://example.org/report"]
        manifest["fact_coverage"]["recreation_permission"]["layer_ids"] = ["water"]
        feature = normalize([self.lead], [self.corridor])[0]
        docs["data.json"]["layers"]["water"]["features"] = [feature]
        properties = feature["properties"]
        validate_region_data(manifest, lambda path: docs[path])
        properties["evidence"]["verification_method"] = "community_report"
        with self.assertRaises(ContractError) as raised:
            validate_region_data(manifest, lambda path: docs[path])
        self.assertEqual(raised.exception.rule, "R23")

    def test_literal_community_report_is_gone(self):
        self.assertNotIn("community_report", (SCRIPTS / "08_ingest_leads.py").read_text())


if __name__ == "__main__":
    unittest.main()
