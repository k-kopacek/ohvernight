"""Exercise CLI events and transport limits using only a fake opener."""
import contextlib
import hashlib
import http.client
import io
import ipaddress
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import research_adapter as adapter


class FakeResponse:
    def __init__(self, body):
        self.body = body
        self.read_sizes = []

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def read(self, size):
        self.read_sizes.append(size)
        return self.body[:size]


class FakeOpener:
    def __init__(self, body, error=None):
        self.response = FakeResponse(body)
        self.error = error
        self.calls = []

    def open(self, request, *, timeout):
        self.calls.append((request, timeout))
        if self.error:
            raise self.error
        return self.response


class AdapterCliTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="qwen-cli-offline-")
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "input.json"
        self.raw = b'[{"id":"cli_record","access":"unknown","camping":"unknown","source_ids":["fixture-main"]}]\n'
        self.path.write_bytes(self.raw)
        self.expected = {"results": [{"id": "cli_record", "access": "unknown", "camping": "unknown",
                                      "source_ids": ["fixture-main"], "recreation_usefulness": "unknown",
                                      "reason": "No evidence establishes permission or usefulness."}]}
        self.envelope = {"model": "qwen3:8b", "done": True, "done_reason": "stop",
                         "message": {"role": "assistant", "content": json.dumps(self.expected)}}
        self.endpoint = f"http://{ipaddress.IPv4Address(2130706433)}:11434/api/chat"

    def invoke(self, body=None, error=None):
        opener = FakeOpener(json.dumps(self.envelope).encode() if body is None else body, error)
        output = io.StringIO()
        with patch("sys.argv", ["adapter", "--input", str(self.path), "--run-id", "offline-cli"]), \
                patch.object(adapter, "require_owner_exposure_review", return_value="synthetic-review"), \
                patch.object(adapter, "configured_endpoint", return_value=self.endpoint), \
                patch.object(adapter.urllib.request, "build_opener", return_value=opener) as builder, \
                contextlib.redirect_stdout(output):
            code = adapter.main()
        return code, [json.loads(line) for line in output.getvalue().splitlines()], opener, builder

    def test_request_timeout_read_bound_and_completed_event(self):
        code, events, opener, builder = self.invoke()
        self.assertEqual(code, 0)
        self.assertEqual([event["event"] for event in events], ["started", "completed"])
        self.assertEqual(len(opener.calls), 1)
        request, timeout = opener.calls[0]
        self.assertEqual(timeout, 120)
        self.assertEqual(request.get_method(), "POST")
        self.assertEqual(request.full_url, self.endpoint)
        self.assertEqual(dict(request.header_items()), {"Content-type": "application/json"})
        payload = json.loads(request.data)
        self.assertEqual(payload["model"], "qwen3:8b")
        self.assertIs(payload["stream"], False)
        self.assertIs(payload["think"], False)
        self.assertEqual(payload["options"], {"temperature": 0, "num_ctx": 4096, "num_predict": 1600})
        self.assertEqual(payload["messages"][1], {"role": "user", "content": json.dumps(json.loads(self.raw))})
        self.assertEqual(payload["messages"][0], {"role": "system", "content": adapter.SYSTEM_PROMPT})
        self.assertFalse(payload["format"]["additionalProperties"])
        self.assertEqual(opener.response.read_sizes, [131073])
        self.assertEqual(events[1]["result"], self.expected)
        self.assertEqual(events[1]["input_sha256"], hashlib.sha256(self.raw).hexdigest())
        self.assertIs(events[1]["accepted"], True)
        self.assertEqual(events[1]["model"], "qwen3:8b")
        self.assertEqual(events[1]["run_id"], "offline-cli")
        self.assertEqual(builder.call_count, 1)
        self.assertEqual(builder.call_args.args[0].proxies, {})
        self.assertIsInstance(builder.call_args.args[1], adapter.NoRedirect)

    def test_raw_input_limit_precedes_request(self):
        self.path.write_bytes(b" " * 8001)
        code, events, opener, builder = self.invoke()
        self.assertEqual(code, 1)
        self.assertEqual(events, [{"event": "rejected", "run_id": "offline-cli", "reason": "input file exceeds limit"}])
        self.assertEqual(opener.calls, [])
        builder.assert_not_called()

    def test_missing_input_emits_failed_before_request(self):
        self.path.unlink()
        code, events, opener, builder = self.invoke()
        self.assertEqual(code, 1)
        self.assertEqual(events[0]["event"], "failed")
        self.assertEqual(opener.calls, [])
        builder.assert_not_called()

    def test_response_limit_malformed_and_truncated_reject(self):
        truncated = dict(self.envelope, done_reason="length")
        for body, reason in [(b" " * 131073, "response exceeds limit"),
                             (b"{", "invalid JSON"),
                             (json.dumps(truncated).encode(), "wrong model or incomplete generation")]:
            with self.subTest(reason=reason):
                code, events, opener, _ = self.invoke(body)
                self.assertEqual(code, 1)
                self.assertEqual([event["event"] for event in events], ["started", "rejected"])
                self.assertEqual(events[1]["reason"], reason)
                self.assertEqual(len(opener.calls), 1)

    def test_io_and_protocol_failures_emit_failed_without_retry(self):
        for error in [OSError(), adapter.urllib.error.URLError("synthetic"), TimeoutError(),
                      http.client.BadStatusLine("synthetic"), http.client.IncompleteRead(b"partial")]:
            with self.subTest(error=type(error).__name__):
                code, events, opener, _ = self.invoke(error=error)
                self.assertEqual(code, 1)
                self.assertEqual([event["event"] for event in events], ["started", "failed"])
                if isinstance(error, http.client.HTTPException):
                    self.assertEqual(events[1]["failure_code"], "HTTP_PROTOCOL_ERROR")
                self.assertEqual(len(opener.calls), 1)

    def test_deep_json_emits_terminal_rejection(self):
        code, events, opener, _ = self.invoke(b"[" * 100000)
        self.assertEqual(code, 1)
        self.assertEqual([event["event"] for event in events], ["started", "rejected"])
        self.assertEqual(events[-1]["failure_code"], "JSON_RECURSION_LIMIT")
        self.assertEqual(len(opener.calls), 1)

    def test_unexpected_opener_error_emits_terminal_failure(self):
        code, events, opener, _ = self.invoke(error=RuntimeError("private exception detail"))
        self.assertEqual(code, 1)
        self.assertEqual(events, [{"event": "started", "run_id": "offline-cli"},
                                 {"event": "failed", "run_id": "offline-cli",
                                  "failure_code": "UNEXPECTED_ADAPTER_ERROR"}])
        self.assertEqual(len(opener.calls), 1)

    def test_control_flow_exceptions_are_not_swallowed(self):
        from orca_runner import DeadlineExpired
        for error in [KeyboardInterrupt(), SystemExit(), DeadlineExpired()]:
            with self.subTest(error=type(error).__name__), self.assertRaises(type(error)):
                self.invoke(error=error)
