import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]


class LegacyExtractTests(unittest.TestCase):
    def test_T14_every_v2_json_surface_is_manifest_declared(self):
        self.assertFalse((ROOT / "v2" / "map-data.json").exists())
        allowed = set()
        for manifest_path in (ROOT / "v2" / "regions").glob("*/region.json"):
            allowed.add(manifest_path.relative_to(ROOT).as_posix())
            allowed.add((manifest_path.parent / 'explore.json').relative_to(ROOT).as_posix())
            manifest = json.loads(manifest_path.read_text())
            def add_paths(value):
                if isinstance(value, dict):
                    for key, child in value.items():
                        if key == "path" and isinstance(child, str):
                            allowed.add((Path("v2") / child).as_posix())
                        add_paths(child)
                elif isinstance(value, list):
                    for child in value:
                        add_paths(child)
            add_paths(manifest)
            display_dir = manifest_path.parent / "display"
            index_path = display_dir / "index.json"
            if index_path.is_file():
                allowed.add(index_path.relative_to(ROOT).as_posix())
                index = json.loads(index_path.read_text())
                for artifact in index.get("artifacts", []):
                    if isinstance(artifact, dict) and isinstance(artifact.get("path"), str):
                        allowed.add((Path("v2") / artifact["path"]).as_posix())
                water_aliases = index.get("water_aliases")
                if isinstance(water_aliases, dict) and isinstance(water_aliases.get("path"), str):
                    allowed.add((Path("v2") / water_aliases["path"]).as_posix())
        candidates = []
        for path in (ROOT / "v2").rglob("*"):
            if "pipeline" in path.relative_to(ROOT / "v2").parts:
                continue
            if path.is_file() and path.suffix in {".json", ".geojson"}:
                candidates.append(path.relative_to(ROOT).as_posix())
        self.assertEqual(set(candidates) - allowed, set())

    def test_T14_unmanifested_v2_extract_is_absent(self):
        self.assertFalse((ROOT / "v2" / "map-data.json").exists())
