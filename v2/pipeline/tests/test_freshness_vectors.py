"""Python side of the cross-language freshness contract."""
import json
import sys
import unittest
from datetime import datetime
from pathlib import Path

V2 = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(V2 / "pipeline" / "scripts"))

from lib.evidence import freshness


class FreshnessVectorTests(unittest.TestCase):
    def test_every_fixture_vector(self):
        vectors = json.loads((V2 / "pipeline/tests/fixtures/freshness-vectors.json").read_text())
        for vector in vectors:
            raw = vector["now"]
            current = datetime.fromisoformat((raw + "T00:00:00Z") if len(raw) == 10 else raw.replace("Z", "+00:00"))
            self.assertEqual(freshness(vector["record"], current), vector["expected"], vector["name"])


if __name__ == "__main__":
    unittest.main()
