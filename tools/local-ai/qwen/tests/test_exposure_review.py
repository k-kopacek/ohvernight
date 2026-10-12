"""Synthetic local acknowledgement files only; no real owner setting needed."""
import json
import contextlib
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import research_adapter as adapter
from datetime import date


class ExposureReviewTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="qwen-review-offline-")
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "synthetic-review.json"
        setting_patch = patch.object(adapter, "exposure_review_setting_path", return_value=self.path)
        setting_patch.start()
        self.addCleanup(setting_patch.stop)
        self.valid = {"owner_exposure_review_acknowledged": True, "reviewed_at": "2026-10-12"}

    def test_dated_explicit_acknowledgement(self):
        self.path.write_text(json.dumps(self.valid), encoding="utf-8")
        before = self.path.read_bytes()
        self.assertEqual(adapter.require_owner_exposure_review(today=date(2026, 10, 12)), "2026-10-12")
        self.assertEqual(self.path.read_bytes(), before)

    def test_missing_unreadable_and_invalid_fail_closed(self):
        samples = [None, b"", b"\xff", b"{" , b"x" * 1025,
                   b'{"owner_exposure_review_acknowledged":true,"reviewed_at":"2026-10-12","reviewed_at":"2026-10-12"}']
        for change in [{"owner_exposure_review_acknowledged": False},
                       {"owner_exposure_review_acknowledged": "true"},
                       {"reviewed_at": None}, {"reviewed_at": "2026-02-30"},
                       {"reviewed_at": "2026-1-2"}, {"reviewed_at": "2026-10-12T00:00:00Z"},
                       {"extra": "not allowed"}]:
            samples.append(json.dumps(dict(self.valid, **change)).encode())
        samples.extend(json.dumps({key: value}).encode() for key, value in self.valid.items())
        for raw in samples:
            with self.subTest(raw=raw):
                if self.path.exists():
                    self.path.unlink()
                if raw is not None:
                    self.path.write_bytes(raw)
                with self.assertRaises(adapter.ExposureReviewError) as caught:
                    adapter.require_owner_exposure_review()
                self.assertEqual(caught.exception.code, "EXPOSURE_REVIEW_REQUIRED")
        with patch.object(Path, "open", side_effect=PermissionError()):
            with self.assertRaises(adapter.ExposureReviewError) as caught:
                adapter.require_owner_exposure_review()
        self.assertEqual(caught.exception.code, "EXPOSURE_REVIEW_REQUIRED")

    def test_future_dates_rejected_old_dates_not_silently_expired(self):
        for value, accepted in [("2026-10-13", False), ("2026-10-12", True), ("2000-01-01", True)]:
            self.path.write_text(json.dumps(dict(self.valid, reviewed_at=value)))
            if accepted:
                self.assertEqual(adapter.require_owner_exposure_review(today=date(2026, 10, 12)), value)
            else:
                with self.assertRaises(adapter.ExposureReviewError):
                    adapter.require_owner_exposure_review(today=date(2026, 10, 12))

    def test_adapter_cli_missing_or_invalid_review_precedes_endpoint_and_request(self):
        for value in [None, "invalid"]:
            if value is not None:
                self.path.write_text(value)
            output = io.StringIO()
            with patch("sys.argv", ["adapter", "--input", "unused", "--run-id", "offline"]), \
                    patch.object(adapter, "configured_endpoint", side_effect=AssertionError("Must not read endpoint")) as endpoint, \
                    patch.object(adapter.urllib.request, "Request", side_effect=AssertionError("Must not build request")) as request, \
                    contextlib.redirect_stdout(output):
                self.assertEqual(adapter.main(), 1)
            event = json.loads(output.getvalue())
            self.assertEqual(event, {"event": "rejected", "run_id": "offline", "failure_code": "EXPOSURE_REVIEW_REQUIRED"})
            endpoint.assert_not_called()
            request.assert_not_called()

    def test_adapter_cli_never_reaches_opener_without_owner_review(self):
        output = io.StringIO()
        with patch("sys.argv", ["adapter", "--input", "unused", "--run-id", "offline"]), \
                patch.object(adapter.urllib.request, "build_opener", side_effect=AssertionError("Must not open")) as opener, \
                contextlib.redirect_stdout(output):
            self.assertEqual(adapter.main(), 1)
        opener.assert_not_called()
        self.assertEqual(json.loads(output.getvalue())["failure_code"], "EXPOSURE_REVIEW_REQUIRED")

    def test_in_repository_setting_and_symlink_rejected(self):
        target = Path(self.temp.name) / "repo" / "ack.json"
        target.parent.mkdir()
        (target.parent / ".git").mkdir()
        target.write_text(json.dumps(self.valid))
        with patch.object(adapter, "exposure_review_setting_path", return_value=target):
            with self.assertRaises(adapter.ExposureReviewError):
                adapter.require_owner_exposure_review()
        self.path.symlink_to(target)
        with self.assertRaises(adapter.ExposureReviewError) as caught:
            adapter.require_owner_exposure_review()
        self.assertEqual(caught.exception.code, "EXPOSURE_REVIEW_REQUIRED")
