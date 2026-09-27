import importlib
import sys
import unittest
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
ridb=importlib.import_module('04_fetch_campgrounds_ridb')

class InventoryTests(unittest.TestCase):
    def test_day_use_results_are_not_overnight_options(self):
        def row(name):
            return {'FacilityName':name,'FacilityID':'1','FacilityLatitude':39.15,'FacilityLongitude':-106.85}
        for name in ['Maroon Bells Amphitheatre','EAST MAROON PORTAL PICNIC SITE','Campground Picnic Area','Unknown facility']:
            self.assertEqual(ridb.normalize([row(name)]),[])
        self.assertEqual(len(ridb.normalize([row('Silver Queen Campground')])),1)
