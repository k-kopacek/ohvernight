"""Offline rejection tests. Run: python3 -B test_adapter.py"""
import copy
import json
import unittest

import research_adapter as adapter


class EvidenceBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.records = [{
            "id": "closure", "access": "prohibited", "camping": "unknown",
            "restriction_freshness": "stale", "source_ids": ["fixture-order"],
            "recreation_evidence": None,
        }]
        self.result = {"results": [{
            "id": "closure", "access": "prohibited", "camping": "unknown",
            "recreation_usefulness": "unknown", "source_ids": ["fixture-order"],
            "reason": "A stale restriction remains a restriction.",
        }]}

    def envelope(self, result=None):
        return {"model": "qwen3:8b", "done": True, "done_reason": "stop",
                "message": {"role": "assistant", "content": json.dumps(result or self.result)}}

    def test_preserves_stale_restriction_and_unknown(self):
        self.assertEqual(adapter.validate_response(self.envelope(), self.records), self.result)

    def test_rejects_inferred_or_weakened_permission(self):
        for field, value in [("access", "unknown"), ("camping", "allowed")]:
            changed = copy.deepcopy(self.result)
            changed["results"][0][field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                adapter.validate_response(self.envelope(changed), self.records)

    def test_rejects_invented_provenance(self):
        self.result["results"][0]["source_ids"] = ["invented-order"]
        with self.assertRaises(ValueError):
            adapter.validate_response(self.envelope(), self.records)

    def test_rejects_missing_duplicate_or_unknown_records(self):
        for results in [[], self.result["results"] * 2,
                        [dict(self.result["results"][0], id="invented")]]:
            with self.subTest(results=results), self.assertRaises(ValueError):
                adapter.validate_response(self.envelope({"results": results}), self.records)

    def test_rejects_tool_requests_truncation_wrong_model_and_invalid_json(self):
        for field, value in [("tool_calls", [{"function": {"name": "shell"}}]),
                             ("done_reason", "length"), ("model", "other"),
                             ("content", "not JSON")]:
            response = self.envelope()
            target = response["message"] if field in ["tool_calls", "content"] else response
            target[field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                adapter.validate_response(response, self.records)

    def test_rejects_name_as_usefulness_evidence(self):
        self.records[0]["name"] = "Beautiful Lake"
        self.result["results"][0]["recreation_usefulness"] = "supported"
        with self.assertRaises(ValueError):
            adapter.validate_response(self.envelope(), self.records)

    def test_rejects_explicit_usefulness_false_negative(self):
        self.records[0]["recreation_evidence"] = {
            "supports_usefulness": True, "text": "Synthetic listing supports paddling.",
        }
        with self.assertRaises(ValueError):
            adapter.validate_response(self.envelope(), self.records)

    def test_rejects_extra_fields_and_non_string_explanation(self):
        for addition in [{"command": "do something"}, {"reason": {"shell": "run"}}]:
            changed = copy.deepcopy(self.result)
            changed["results"][0].update(addition)
            with self.subTest(addition=addition), self.assertRaises(ValueError):
                adapter.validate_response(self.envelope(changed), self.records)

    def test_rejects_invalid_input_before_network(self):
        for records in [[], self.records * 2, [dict(self.records[0], access="maybe")],
                        [dict(self.records[0], api_key="never-send-this")],
                        [dict(self.records[0], recreation_evidence={"supports_usefulness": "yes"})]]:
            with self.subTest(records=records), self.assertRaises(ValueError):
                adapter.validate_records(records)

    def test_request_has_no_tools_and_uses_fixed_endpoint_model(self):
        request = adapter.build_request(self.records)
        self.assertEqual(request["model"], "qwen3:8b")
        self.assertNotIn("tools", request)
        self.assertFalse(request["think"])
        self.assertFalse(request["stream"])
        self.assertEqual(adapter.ENDPOINT, "http://ENDPOINT_NOT_CONFIGURED:11434/api/chat")


if __name__ == "__main__":
    unittest.main()
