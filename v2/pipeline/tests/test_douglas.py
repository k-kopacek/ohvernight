import sys
import unittest
from pathlib import Path
from unittest.mock import patch
from shapely.geometry import box, shape
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from fetch_douglas import county_boundary, normalize_road
from fetch_trails import normalize

class DouglasTests(unittest.TestCase):
    def test_region_clipping_does_not_use_aspen_default(self):
        bounds=box(-105.3,39,-105,39.6)
        row={'geometry':{'type':'LineString','coordinates':[[-105.5,39.2],[-105.1,39.2]]},'properties':{'objectid':1,'name':'Road','trail_name':'Trail'}}
        for feature in [normalize_road(row,bounds,{}),normalize(row,{},bounds)]:
            self.assertIsNotNone(feature)
            self.assertTrue(bounds.covers(shape(feature['geometry'])))
    @patch('fetch_douglas.get_json',return_value={'features':[{'properties':{'GEOID':'41019'}}]})
    def test_rejects_wrong_douglas_county(self,mock):
        with self.assertRaises(ValueError):county_boundary(None)
