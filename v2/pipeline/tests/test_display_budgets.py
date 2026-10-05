import gzip
import json
import unittest
from pathlib import Path


V2 = Path(__file__).resolve().parents[2]


class DisplayBudgetTests(unittest.TestCase):
    def test_T13_display_files_stay_within_feature_and_byte_budgets(self):
        for region_dir in (V2 / "regions").glob("*/display"):
            index = json.loads((region_dir / "index.json").read_text())
            total_features = 0
            total_gzip = 0
            for artifact in index["artifacts"]:
                raw = (V2 / artifact["path"]).read_bytes()
                compressed = gzip.compress(raw, mtime=0)
                self.assertEqual(len(raw), artifact["bytes"])
                self.assertLessEqual(artifact["feature_count"], 5000, artifact["layer_id"])
                self.assertLessEqual(len(compressed), 450000, artifact["layer_id"])
                total_features += artifact["feature_count"]
                total_gzip += len(compressed)
            self.assertLessEqual(total_features, 15000, region_dir.parent.name)
            self.assertLessEqual(total_gzip, 1000000, region_dir.parent.name)
