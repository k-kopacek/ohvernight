import gzip
import json
import unittest
from pathlib import Path


V2 = Path(__file__).resolve().parents[2]


class DisplayBudgetTests(unittest.TestCase):
    def test_T13_display_files_stay_within_feature_and_byte_budgets(self):
        for region_dir in (V2 / "regions").glob("*/display"):
            manifest = json.loads((region_dir.parent / "region.json").read_text())
            index = json.loads((region_dir / "index.json").read_text())
            total_features = 0
            total_gzip = 0
            map_usable = sum((V2 / relative).stat().st_size for relative in [
                str((region_dir.parent / "region.json").relative_to(V2)),
                str((region_dir / "index.json").relative_to(V2)),
            ])
            # explore.json is not present in PR A; PR B will add it to this measure.
            place_paths = [layer["path"] for layer in manifest["layers"] if layer["format"] == "place_list"]
            map_usable += sum((V2 / relative).stat().st_size for relative in place_paths)
            coverage_entry = next(item for item in index["artifacts"] if item["layer_id"] == "coverage")
            map_usable += (V2 / coverage_entry["path"]).stat().st_size
            self.assertLessEqual(map_usable, 500000, f"{region_dir.parent.name} map usable")
            for artifact in index["artifacts"]:
                raw = (V2 / artifact["path"]).read_bytes()
                compressed = gzip.compress(raw, mtime=0)
                document = json.loads(raw)
                self.assertEqual(len(raw), artifact["bytes"])
                self.assertEqual(artifact["feature_count"], len(document["features"]), artifact["layer_id"])
                self.assertLessEqual(artifact["feature_count"], 5000, artifact["layer_id"])
                self.assertLessEqual(len(compressed), 450000, artifact["layer_id"])
                total_features += artifact["feature_count"]
                total_gzip += len(compressed)
            self.assertLessEqual(total_features, 15000, region_dir.parent.name)
            self.assertLessEqual(total_gzip, 1000000, region_dir.parent.name)
            self.assertLessEqual(total_gzip, 1500000, f"{region_dir.parent.name} default-on gzip growth budget")
            all_loaded = map_usable + sum((V2 / artifact["path"]).stat().st_size for artifact in index["artifacts"] if artifact["layer_id"] != "coverage")
            self.assertLessEqual(all_loaded, 4500000, f"{region_dir.parent.name} all display bytes")
