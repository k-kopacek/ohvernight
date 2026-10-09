import json, sys, tempfile, unittest
from pathlib import Path
from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import patch
SCRIPTS=Path(__file__).resolve().parents[1]/"scripts"; sys.path.insert(0,str(SCRIPTS))
import fetch_trails
class AttributeDriftTest(unittest.TestCase):
 def test_real_publish_reports_changed_name_under_stable_id(self):
  def row(name): return {"type":"Feature","id":7,"properties":{"OBJECTID":7,"TRAIL_NAME":name,"TRAIL_NO":"007"},"geometry":{"type":"LineString","coordinates":[[-106.8,39.1],[-106.7,39.2]]}}
  with tempfile.TemporaryDirectory() as d:
   root=Path(d)/"v2"; (root/"pipeline/scripts").mkdir(parents=True); target=root/"trails.geojson"; target.write_text('{"features":[]}')
   logs=[]
   with patch.object(fetch_trails,"__file__",str(root/"pipeline/scripts/fetch_trails.py")), patch.object(fetch_trails,"query_layer_geojson") as query:
    for name in ("ORIGINAL NAME","RENAMED UNDER SAME ID"):
     query.return_value={"features":[row(name)]}; out=StringIO()
     with redirect_stdout(out): fetch_trails.main()
     logs.append(out.getvalue())
   self.assertIn("Attribute drift detected",logs[1]); self.assertIn("name",logs[1])
   saved=json.loads(target.read_text()); self.assertEqual(saved["features"][0]["properties"]["name"],"RENAMED UNDER SAME ID")
