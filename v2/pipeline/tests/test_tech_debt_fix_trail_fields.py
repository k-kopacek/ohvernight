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
