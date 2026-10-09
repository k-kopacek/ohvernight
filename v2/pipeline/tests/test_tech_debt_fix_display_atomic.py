import sys, tempfile, unittest
from pathlib import Path
from unittest.mock import patch
SCRIPTS=Path(__file__).resolve().parents[1]/"scripts"; sys.path.insert(0,str(SCRIPTS))
import build_display
class AtomicDisplayPublicationTest(unittest.TestCase):
 def setup_fixture(self,root):
  output=root/"regions/fixture/display"; output.mkdir(parents=True); (output/"first.geojson").write_bytes(b"old-first"); (output/"coverage.geojson").write_bytes(b"old-coverage"); return output
 def patches(self,root):
  manifest={"layers":[{"id":"first","format":"feature_collection","kind":"land","status_ref":None}]}
  first=({"type":"FeatureCollection","features":[]},{"path":"regions/fixture/display/first.geojson","layer_id":"first","feature_count":0})
  coverage=({"type":"FeatureCollection","features":[]},{"path":"regions/fixture/display/coverage.geojson","layer_id":"coverage","feature_count":0})
  return (patch.object(build_display,"_read_json",return_value=manifest),patch.object(build_display,"build_layer",return_value=first),patch.object(build_display,"build_coverage",return_value=coverage))
 def test_failure_preserves_old_directory_and_cleans_stage(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d); output=self.setup_fixture(root); before={p.name:p.read_bytes() for p in output.iterdir()}; writes=0; orig=Path.write_bytes
   def fail(path,data):
    nonlocal writes; writes+=1
    if writes==2: raise OSError("synthetic interrupted publication")
    return orig(path,data)
   with self.patches(root)[0],self.patches(root)[1],self.patches(root)[2],patch.object(Path,"write_bytes",fail):
    with self.assertRaisesRegex(OSError,"synthetic interrupted"): build_display.build_region("fixture",root=root,write=True)
   self.assertEqual({p.name:p.read_bytes() for p in output.iterdir()},before); self.assertEqual(list(output.parent.glob(".fixture-display-*")),[])
 def test_success_replaces_complete_directory_and_cleans_stage(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d); output=self.setup_fixture(root)
   with self.patches(root)[0],self.patches(root)[1],self.patches(root)[2]: build_display.build_region("fixture",root=root,write=True)
   self.assertEqual({p.name for p in output.iterdir()},{"first.geojson","coverage.geojson","index.json"}); self.assertEqual(list(output.parent.glob(".fixture-display-*")),[])
