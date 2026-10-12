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
   self.assertIn("trails drift usfs-trail-7",logs[1]); self.assertIn("name",logs[1])
   saved=json.loads(target.read_text()); self.assertEqual(saved["features"][0]["properties"]["name"],"RENAMED UNDER SAME ID")

 def test_bad_previous_snapshots_never_stop_publication(self):
  cases={'corrupt':'{not-json','list':'[]','feature-without-id':json.dumps({'features':[{'properties':{},'geometry':None}]})}
  row={'type':'Feature','geometry':{'type':'LineString','coordinates':[[-106.8,39.1],[-106.7,39.2]]},'properties':{'OBJECTID':8,'TRAIL_NAME':'CURRENT','TRAIL_NO':'008'}}
  for label,prior in cases.items():
   with self.subTest(label=label), tempfile.TemporaryDirectory() as d:
    root=Path(d)/'v2'; (root/'pipeline/scripts').mkdir(parents=True); target=root/'trails.geojson'; target.write_text(prior)
    with patch.object(fetch_trails,'__file__',str(root/'pipeline/scripts/fetch_trails.py')), patch.object(fetch_trails,'query_layer_geojson',return_value={'features':[row]}):
     with redirect_stdout(StringIO()) as out: fetch_trails.main()
    self.assertEqual(json.loads(target.read_text())['features'][0]['properties']['name'],'CURRENT')
    self.assertIn('drift comparison skipped:',out.getvalue())

 def test_missing_previous_snapshot_publishes(self):
  row={'type':'Feature','geometry':{'type':'LineString','coordinates':[[-106.8,39.1],[-106.7,39.2]]},'properties':{'OBJECTID':9,'TRAIL_NAME':'NEW','TRAIL_NO':'009'}}
  with tempfile.TemporaryDirectory() as d:
   root=Path(d)/'v2'; (root/'pipeline/scripts').mkdir(parents=True); target=root/'trails.geojson'
   with patch.object(fetch_trails,'__file__',str(root/'pipeline/scripts/fetch_trails.py')), patch.object(fetch_trails,'query_layer_geojson',return_value={'features':[row]}): fetch_trails.main()
   self.assertTrue(target.exists())

 def test_identical_data_publishes_without_drift_and_report_is_read_only(self):
  row={'type':'Feature','geometry':{'type':'LineString','coordinates':[[-106.8,39.1],[-106.7,39.2]]},'properties':{'OBJECTID':10,'TRAIL_NAME':'SAME','TRAIL_NO':'010'}}
  with tempfile.TemporaryDirectory() as d:
   root=Path(d)/'v2'; (root/'pipeline/scripts').mkdir(parents=True); target=root/'trails.geojson'
   with patch.object(fetch_trails,'__file__',str(root/'pipeline/scripts/fetch_trails.py')), patch.object(fetch_trails,'query_layer_geojson',return_value={'features':[row]}), patch.object(fetch_trails,'now',return_value='2026-10-09T00:00:00Z'), patch('lib.evidence.now',return_value='2026-10-09T00:00:00Z'): fetch_trails.main()
   before=target.read_bytes(); digest=__import__('hashlib').sha256(before).hexdigest()
   with patch.object(fetch_trails,'__file__',str(root/'pipeline/scripts/fetch_trails.py')), patch.object(fetch_trails,'query_layer_geojson',return_value={'features':[row]}), patch.object(fetch_trails,'now',return_value='2026-10-09T00:00:00Z'), patch('lib.evidence.now',return_value='2026-10-09T00:00:00Z'):
    with redirect_stdout(StringIO()) as out: fetch_trails.main()
   self.assertEqual(__import__('hashlib').sha256(target.read_bytes()).hexdigest(),digest)
   self.assertNotIn('drift',out.getvalue().lower())

 def test_activity_drift_is_itemized_by_activity_and_field(self):
  from lib.trail_drift import report_trail_drift
  import hashlib
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'prior.json'; old={'id':'x','activities':{'motorcycling':{'restricted':''}}}; current={'id':'x','activities':{'motorcycling':{'restricted':'12/01-04/30'}}}
   p.write_text(json.dumps({'features':[{'properties':old,'geometry':None}]})); before=hashlib.sha256(p.read_bytes()).hexdigest()
   with redirect_stdout(StringIO()) as out: report_trail_drift(p,[{'properties':current,'geometry':None}])
   self.assertIn("activities.motorcycling.restricted: '' -> '12/01-04/30'",out.getvalue())
   self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),before)

 def test_douglas_publication_uses_shared_drift_reporter(self):
  import fetch_douglas
  from shapely.geometry import box
  with tempfile.TemporaryDirectory() as d:
   root=Path(d)/'v2'; target=root/'regions/douglas-co/research.json'; target.parent.mkdir(parents=True)
   target.write_text(json.dumps({'region':'douglas-co','layers':{}}))
   features=[{'type':'Feature','geometry':{'type':'LineString','coordinates':[[0,0],[1,1]]},'properties':{'id':'x'}}]
   county={'type':'FeatureCollection','features':[]}
   boundary=box(-1,-1,2,2)
   raw={'features':[{'geometry':{'type':'LineString','coordinates':[[0,0],[1,1]]},'properties':{'OBJECTID':1,'TRAIL_NAME':'N'}}]}
   with patch.object(fetch_douglas,'__file__',str(root/'pipeline/scripts/fetch_douglas.py')), patch.object(fetch_douglas,'new_session'), patch.object(fetch_douglas,'county_boundary',return_value=(county,boundary)), patch.object(fetch_douglas,'query_layer_geojson',return_value=raw), patch.object(fetch_douglas,'report_trail_drift') as report:
    fetch_douglas.main()
   self.assertTrue(any(call.kwargs.get('douglas') for call in report.call_args_list))
