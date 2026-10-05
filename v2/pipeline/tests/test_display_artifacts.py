import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

V2 = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(V2 / 'pipeline' / 'scripts'))
from build_display import build_layer, build_region, display_water  # noqa: E402


class DisplayArtifactTests(unittest.TestCase):
    def test_transport_copies_every_status_reference_verbatim_including_place_lists(self):
        for region_id in ('aspen', 'douglas-co'):
            result = build_region(region_id, V2)
            transport = result['index']['transport']
            expected = {}
            for layer in result['manifest']['layers']:
                ref = layer['status_ref']
                if ref is None:
                    continue
                record = json.loads((V2 / ref['path']).read_text())
                for token in ref['pointer'].lstrip('/').split('/') if ref['pointer'] else []:
                    token = token.replace('~1', '/').replace('~0', '~')
                    record = record[int(token)] if isinstance(record, list) else record[token]
                expected[layer['id']] = record
            self.assertEqual(transport, expected)
        self.assertIn('ridb_options', build_region('aspen', V2)['index']['transport'])

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
        manifest = result['manifest']
        for entry in result['index']['artifacts']:
            if entry['layer_id'] == 'coverage':
                continue
            artifact = json.loads(result['artifacts'][entry['path']])
            self.assertEqual(len({json.dumps(value, sort_keys=True) for value in artifact['evidence_table']}), len(artifact['evidence_table']))
            layer = next(layer for layer in manifest['layers'] if layer['id'] == entry['layer_id'])
            source = json.loads((V2 / layer['path']).read_text())
            canonical = source
            for token in layer.get('pointer', '').lstrip('/').split('/') if layer.get('pointer') else []:
                canonical = canonical[token]
            if layer['kind'] == 'water' and any('kind' in (feature.get('properties') or {}) for feature in canonical['features']):
                canonical = {**canonical, 'features': [feature for feature in canonical['features'] if display_water(feature)]}
            expected = {json.dumps(feature['properties']['evidence'], sort_keys=True) for feature in canonical['features']}
            self.assertEqual({json.dumps(value, sort_keys=True) for value in artifact['evidence_table']}, expected)

    def test_build_fails_when_every_part_of_a_feature_collapses(self):
        manifest = {'region': {'id': 'synthetic'}}
        layer = {'id': 'lines', 'kind': 'trails', 'format': 'feature_collection', 'path': 'data.json', 'pointer': ''}
        feature = {'type': 'Feature', 'geometry': {'type': 'MultiLineString', 'coordinates': [[[0, 0], [0.0000001, 0.0000001]]]}, 'properties': {'id': 'all-degenerate', 'evidence': {}}}
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'data.json').write_text(json.dumps({'type': 'FeatureCollection', 'features': [feature]}))
            with self.assertRaises(ValueError):
                build_layer(manifest, layer, root)


if __name__ == '__main__':
    unittest.main()
