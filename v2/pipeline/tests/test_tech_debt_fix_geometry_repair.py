import hashlib, logging, sys, unittest
from pathlib import Path
from shapely.geometry import box, shape
SCRIPTS=Path(__file__).resolve().parents[1]/"scripts"; sys.path.insert(0,str(SCRIPTS))
from lib.common import clip_geometry
class GeometryRepairVisibilityTest(unittest.TestCase):
 def setUp(self):
  from lib import common
  common._REPORTED_REPAIRS.clear()
 def test_repair_of_invalid_bowtie_emits_diagnostic(self):
  invalid={"type":"Polygon","coordinates":[[[0,0],[2,2],[0,2],[2,0],[0,0]]]}; original=shape(invalid)
  with self.assertLogs("lib.common",level="WARNING") as captured: result=clip_geometry(invalid,box(-1,-1,3,3))
  repaired=shape(result); self.assertNotEqual(original.area,repaired.area); self.assertIn("Invalid Polygon geometry",captured.output[0]); self.assertIn("Self-intersection",captured.output[0])
 def test_identical_repairs_are_summarized_once(self):
  invalid={"type":"Polygon","coordinates":[[[0,0],[2,2],[0,2],[2,0],[0,0]]]}
  with self.assertLogs("lib.common",level="WARNING") as captured:
   clip_geometry(invalid,box(-1,-1,3,3)); clip_geometry(invalid,box(-1,-1,3,3))
  self.assertEqual(len(captured.records),1)
 def test_output_hashes_match_pre_change_results(self):
  geometries=[
   {"type":"Polygon","coordinates":[[[0,0],[2,2],[0,2],[2,0],[0,0]]]},
   {"type":"LineString","coordinates":[[0,0],[2,2]]},
   {"type":"Polygon","coordinates":[[[0,0],[2,0],[2,2],[0,2],[0,0]]]},
  ]
  actual=[hashlib.sha256(str(clip_geometry(g,box(-1,-1,3,3))).encode()).hexdigest() for g in geometries]
  self.assertEqual(actual,["2ca62b0e398cd4997e56666cbebb2fe05c6c8f6419278879eb310b1405c8f586","02c5149a6c2c3d75a298c51db246c20d193dacf9518ff25cd3a7c56e989f62fd","d042b2fc987b000ef5f96782ae73d101bf09db4082aaeff5e3e314b1ad715c71"])
