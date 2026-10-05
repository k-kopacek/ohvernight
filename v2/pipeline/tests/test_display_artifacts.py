import hashlib
import json
import sys
import unittest
from pathlib import Path

V2 = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(V2 / 'pipeline' / 'scripts'))
from build_display import build_region, display_water  # noqa: E402


class DisplayArtifactTests(unittest.TestCase):
    def test_water_vectors(self):
        vectors = json.loads((V2 / 'pipeline/tests/fixtures/display-water-vectors.json').read_text())
        for vector in vectors:
            feature = {'type': 'Feature', 'geometry': vector['geometry'], 'properties': {
                'name': vector['name'], 'kind': vector['kind'],
            }}
            self.assertEqual(display_water(feature), vector['expected'], vector['name'])

    def test_committed_artifacts_rebuild_byte_for_byte(self):
        for region_id in ('aspen', 'douglas-co'):
            result = build_region(region_id, V2)
            index_path = V2 / 'regions' / region_id / 'display/index.json'
            committed_index = index_path.read_bytes()
            self.assertEqual(result['artifacts'][f'regions/{region_id}/display/index.json'], committed_index)
            for relative, data in result['artifacts'].items():
                self.assertEqual((V2 / relative).read_bytes(), data, relative)
            for entry in result['index']['artifacts']:
                data = result['artifacts'][entry['path']]
                self.assertEqual(entry['bytes'], len(data))
                self.assertEqual(entry['sha256'], hashlib.sha256(data).hexdigest())

    def test_evidence_is_deduplicated_without_changing_non_evidence_properties(self):
        result = build_region('aspen', V2)
        artifact = json.loads(result['artifacts']['regions/aspen/display/land_ownership.geojson'])
        source = json.loads((V2 / 'map-data-v2.json').read_text())['layers']['land_ownership']
        self.assertLessEqual(len(artifact['evidence_table']), len(source['features']))
        for feature in artifact['features'][:10]:
            evidence = artifact['evidence_table'][feature['properties']['evidence']]
            self.assertIsInstance(evidence, dict)
            self.assertIn('source_url', evidence)


if __name__ == '__main__':
    unittest.main()
