import logging, sys, unittest
from pathlib import Path
from shapely.geometry import box, shape
SCRIPTS=Path(__file__).resolve().parents[1]/"scripts"; sys.path.insert(0,str(SCRIPTS))
from lib.common import clip_geometry
class GeometryRepairVisibilityTest(unittest.TestCase):
 def test_repair_of_invalid_bowtie_emits_diagnostic(self):
  invalid={"type":"Polygon","coordinates":[[[0,0],[2,2],[0,2],[2,0],[0,0]]]}; original=shape(invalid)
  with self.assertLogs("lib.common",level="WARNING") as captured: result=clip_geometry(invalid,box(-1,-1,3,3))
  repaired=shape(result); self.assertNotEqual(original.area,repaired.area); self.assertIn("Invalid geometry repaired",captured.output[0])
