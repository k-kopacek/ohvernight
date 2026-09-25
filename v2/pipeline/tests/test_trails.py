import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from fetch_trails import normalize, main

class TrailTests(unittest.TestCase):
    def test_preserves_dates_and_unknown_activity(self):
        row = {'type': 'Feature', 'geometry': {'type': 'LineString',
               'coordinates': [[-106.9, 39.1], [-106.8, 39.15]]},
               'properties': {'OBJECTID': 42, 'TRAIL_NAME': 'Example',
                              'BICYCLE_RESTRICTED': '05/01-06/30'}}
        result = normalize(row, {'retrieved_at': '2026-09-25'})
        self.assertEqual(result['properties']['activities']['mountain_biking']['restricted'], '05/01-06/30')
        self.assertIsNone(result['properties']['activities']['hiking']['accpt'])
        self.assertEqual(result['properties']['id'], 'usfs-trail-42')

    def test_excludes_geometry_outside_pilot(self):
        row = {'geometry': {'type': 'LineString', 'coordinates': [[0, 0], [1, 1]]},
               'properties': {'objectid': 1}}
        self.assertIsNone(normalize(row, {}))

    @patch('fetch_trails.query_layer_geojson', return_value={'features': []})
    def test_empty_refresh_does_not_replace_snapshot(self, query):
        target = Path(__file__).resolve().parents[2] / 'trails.geojson'
        before = target.read_bytes()
        with self.assertRaises(ValueError):
            main()
        self.assertEqual(target.read_bytes(), before)
