import sys, tempfile, unittest
from pathlib import Path
from unittest.mock import patch
SCRIPTS=Path(__file__).resolve().parents[1]/"scripts"; sys.path.insert(0,str(SCRIPTS))
import fetch_trails
from lib.arcgis_client import ArcGISQueryError
class RequiredTrailFieldsTest(unittest.TestCase):
 def test_missing_activity_field_stops_before_normalization_and_publication(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d)/"v2"; (root/"pipeline/scripts").mkdir(parents=True); target=root/"trails.geojson"; target.write_bytes(b"previous published bytes")
   seen={}
   def query(*args,**kwargs):
    seen.update(kwargs); raise ArcGISQueryError("Layer missing ['atv_accpt']")
   with patch.object(fetch_trails,"__file__",str(root/"pipeline/scripts/fetch_trails.py")), patch.object(fetch_trails,"query_layer_geojson",side_effect=query), patch.object(fetch_trails,"normalize") as normalize:
    with self.assertRaisesRegex(ArcGISQueryError,"atv_accpt"): fetch_trails.main()
   self.assertIn("atv_accpt",seen["required_fields"]); normalize.assert_not_called(); self.assertEqual(target.read_bytes(),b"previous published bytes")

 def test_required_fields_are_the_full_activity_schema(self):
  expected={'objectid','trail_name','trail_no'} | {f'{prefix}_{suffix}' for prefix in fetch_trails.ACTIVITIES.values() for suffix in ('managed','accpt','disc','restricted')}
  self.assertEqual(set(fetch_trails.REQUIRED_FIELDS),expected)
  self.assertEqual(len(fetch_trails.REQUIRED_FIELDS),39)

 def test_real_describe_layer_rejects_missing_field_before_query_or_write(self):
  from lib.arcgis_client import query_layer_geojson
  class Response:
   def raise_for_status(self): pass
   def json(self): return {'type':'Feature Layer','fields':[{'name':'OBJECTID','type':'esriFieldTypeOID'}]}
  class Session:
   headers={}
   def __init__(self): self.urls=[]
   def get(self,url,params,timeout): self.urls.append((url,params)); return Response()
  session=Session()
  with self.assertRaisesRegex(ArcGISQueryError,'missing'):
   query_layer_geojson('https://example.invalid/MapServer',0,(-1,-1,1,1),session=session,required_fields=fetch_trails.REQUIRED_FIELDS)
  self.assertEqual(len(session.urls),1)
  self.assertFalse(session.urls[0][0].endswith('/query'))

 def test_douglas_trail_layer_uses_exported_required_fields(self):
  import fetch_douglas
  self.assertIs(fetch_douglas.TRAIL_REQUIRED_FIELDS,fetch_trails.REQUIRED_FIELDS)
