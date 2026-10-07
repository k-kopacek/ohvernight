import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

V2 = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(V2 / 'pipeline' / 'scripts'))
from build_display import (_display_feature, _water_context, build_layer, build_region,
                          display_water)  # noqa: E402


class DisplayArtifactTests(unittest.TestCase):
    def test_display_feature_conversion_keeps_properties_except_evidence_reference(self):
        feature = {'type': 'Feature', 'geometry': {'type': 'LineString', 'coordinates': [[0, 0], [1, 1]]},
                   'properties': {'id': 'nhd-123', 'name': 'River', 'source_layer': 'flowline',
                                  'kind': 'flowline', 'source_id': 'source-123', 'fcode': 55800,
                                  'water_class': 'stream', 'legacy_ids': ['old-id'],
                                  'evidence': {'source_url': 'https://example.test'}}}
        display, _ = _display_feature(feature, {}, [])
        self.assertEqual(set(display['properties']), set(feature['properties']))
        self.assertIsInstance(display['properties']['evidence'], int)

    def test_group_map_and_displayed_aliases_are_built_from_canonical_members(self):
        for region_id in ('aspen', 'douglas-co'):
            result = build_region(region_id, V2)
            index = result['index']
            self.assertNotIn('water_id_aliases', index)
            self.assertTrue(index['water_groups'])
            alias_entry = index['water_aliases']
            aliases = json.loads(result['artifacts'][alias_entry['path']])['water_id_aliases']
            self.assertTrue(aliases)
            self.assertTrue(all(isinstance(key, str) and isinstance(value, str)
                                for key, value in aliases.items()))
            context = _water_context(result['manifest'], V2)
            targets = {member: group for group, ids in index['water_groups'].items()
                       for member in ids}
            targets.update({ident: ident for ident in context['selected_body_ids']})
            expected = {legacy: targets[feature['properties']['id']]
                        for feature in context['all_water_features']
                        if feature['properties']['id'] in targets
                        for legacy in feature['properties'].get('legacy_ids', [])}
            self.assertEqual(aliases, expected)

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
        source_layer_feature = {'type': 'Feature', 'geometry': {'type': 'LineString', 'coordinates': [[0, 0], [1, 1]]},
                                'properties': {'name': 'Douglas River', 'source_layer': 'flowline'}}
        self.assertTrue(display_water(source_layer_feature))

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
        context = _water_context(manifest, V2)
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
            selector = layer.get('display', {}).get('select')
            if selector == 'streams':
                evidence = [feature['properties']['evidence'] for feature in context['grouped']['groups']]
            elif selector == 'bodies':
                evidence = [feature['properties']['evidence'] for feature in context['body_features']
                            if feature['properties']['id'] in context['selected_body_ids']]
            else:
                evidence = [feature['properties']['evidence'] for feature in canonical['features']]
            expected = {json.dumps(value, sort_keys=True) for value in evidence}
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
