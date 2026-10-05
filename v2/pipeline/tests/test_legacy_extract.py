import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]


class LegacyExtractTests(unittest.TestCase):
    def test_T14_unmanifested_v2_extract_is_absent(self):
        self.assertFalse((ROOT / "v2" / "map-data.json").exists())
