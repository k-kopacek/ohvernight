"""Synthetic local acknowledgement files only; no real owner setting needed."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import orca_runner as runner


class ExposureReviewTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="qwen-review-offline-")
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "synthetic-review.json"
        setting_patch = patch.object(runner, "exposure_review_setting_path", return_value=self.path)
        setting_patch.start()
        self.addCleanup(setting_patch.stop)
        self.valid = {"owner_exposure_review_acknowledged": True, "reviewed_at": "2026-10-12"}

    def test_dated_explicit_acknowledgement(self):
        self.path.write_text(json.dumps(self.valid), encoding="utf-8")
        before = self.path.read_bytes()
        self.assertEqual(runner.require_owner_exposure_review(), "2026-10-12")
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
                with self.assertRaises(runner.RunFailure) as caught:
                    runner.require_owner_exposure_review()
                self.assertEqual(caught.exception.code, "EXPOSURE_REVIEW_REQUIRED")
        with patch.object(Path, "open", side_effect=PermissionError()):
            with self.assertRaises(runner.RunFailure) as caught:
                runner.require_owner_exposure_review()
        self.assertEqual(caught.exception.code, "EXPOSURE_REVIEW_REQUIRED")

    def test_in_repository_setting_and_symlink_rejected(self):
        target = Path(runner.__file__).resolve()
        with patch.object(runner, "exposure_review_setting_path", return_value=target):
            with self.assertRaises(runner.RunFailure):
                runner.require_owner_exposure_review()
        self.path.symlink_to(target)
        with self.assertRaises(runner.RunFailure) as caught:
            runner.require_owner_exposure_review()
        self.assertEqual(caught.exception.code, "EXPOSURE_REVIEW_REQUIRED")
