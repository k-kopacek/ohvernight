import copy
import json
import re
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

V2 = Path(__file__).resolve().parents[2]
SCHEMA = json.loads((V2 / 'pipeline/schema/explore-config.schema.json').read_text())
LEGACY = {entry['text'] for entry in json.loads((V2 / 'pipeline/tests/fixtures/legacy-negated-wording.json').read_text())['strings']}


def validate_config(manifest, config):
    Draft202012Validator(SCHEMA, format_checker=FormatChecker()).validate(config)
    if config['region_id'] != manifest['region']['id']:
        raise ValueError('region mismatch')
    ids = [layer['layer_id'] for layer in config['layers']]
    declared = {layer['id'] for layer in manifest['layers']}
    displayed = {layer['id'] for layer in manifest['layers'] if layer.get('display')}
    if len(ids) != len(set(ids)) or not set(ids) <= declared or not displayed <= set(ids):
        raise ValueError('layer membership or duplicates')
    def strings(value):
        if isinstance(value, str):
            yield value
        elif isinstance(value, dict):
            for child in value.values():
                yield from strings(child)
        elif isinstance(value, list):
            for child in value:
                yield from strings(child)
    for value in strings(config):
        if value not in LEGACY and re.search(r'\b(verified|legal|permitted|open|allowed|private|public)\b', value, re.I):
            raise ValueError('presentation word rule')
    return config


class ExploreConfigTests(unittest.TestCase):
    def setUp(self):
        self.manifest = json.loads((V2 / 'regions/aspen/region.json').read_text())
        self.config = json.loads((V2 / 'regions/aspen/explore.json').read_text())

    def negative(self, mutate):
        config = copy.deepcopy(self.config)
        mutate(config)
        with self.assertRaises(Exception):
            validate_config(self.manifest, config)

    def test_T11_real_config_and_capabilities(self):
        for rid in ('aspen', 'douglas-co'):
            manifest = json.loads((V2 / f'regions/{rid}/region.json').read_text())
            config = json.loads((V2 / f'regions/{rid}/explore.json').read_text())
            validate_config(manifest, config)
            self.assertTrue(all(layer['default_on'] for layer in config['layers']))
            self.assertEqual(config['capabilities']['trail_season_check'], rid != 'aspen')
        self.assertEqual(self.config['storage_keys'], {'trip': 'ohvernight-trip-v1'})
        other = json.loads((V2 / 'regions/douglas-co/explore.json').read_text())
        self.assertEqual(other['storage_keys'], {'plan': 'ohvernight-douglas-plan-v1', 'notes': 'ohvernight-douglas-plan-v1-notes', 'trip': 'ohvernight-douglas-plan-v1-trip'})

    def test_T11_aspen_season_check_remains_off(self):
        self.assertIs(self.config['capabilities']['trail_season_check'], False)

    def test_T11_unknown_layer(self):
        self.negative(lambda c: c['layers'][0].update(layer_id='missing'))

    def test_T11_missing_display_layer(self):
        self.negative(lambda c: c['layers'].pop(0))

    def test_T11_duplicate_layer(self):
        self.negative(lambda c: c['layers'].append(c['layers'][0]))

    def test_T11_region_mismatch(self):
        self.negative(lambda c: c.update(region_id='other'))

    def test_T11_word_rule_every_forbidden_title(self):
        for word in ('verified', 'legal', 'permitted', 'open', 'allowed', 'private', 'public'):
            with self.subTest(word=word):
                self.negative(lambda c: c['layers'][0].update(title=word))

    def test_T11_non_http_url(self):
        self.negative(lambda c: c['official_links'][0].update(url='javascript:bad()'))

    def test_T11_version(self):
        self.negative(lambda c: c.update(explore_version=2))

    def test_T11_view(self):
        self.negative(lambda c: c['initial_view'].update(center=[181, 91]))

    def test_T11_layer_types(self):
        for key, value in (('order', 'first'), ('default_on', 1), ('min_zoom', 'zoom')):
            self.negative(lambda c: c['layers'][0].update({key: value}))

    def test_T11_capabilities(self):
        self.negative(lambda c: c['capabilities'].update(region_extras='yes'))

    def test_T11_storage_keys(self):
        self.negative(lambda c: c['storage_keys'].update(trip='../key'))

    def test_T11_trip_defaults(self):
        self.negative(lambda c: c['trip_defaults'].update(arrive='2026-02-30'))

    def test_T11_landing(self):
        self.negative(lambda c: c.update(landing='html'))

    def test_T11_export_names(self):
        self.negative(lambda c: c.update(export_names={'plan': '../plan.json'}))

    def test_T11_no_script_path(self):
        self.negative(lambda c: c.update(extras_path='regions/aspen/extras.js'))

    def test_T11_no_limitation_in_config(self):
        self.negative(lambda c: c['layers'][0].update(limitations='Anything'))

    def test_T11_word_rule_other_strings(self):
        self.negative(lambda c: c['official_links'][0].update(label='Verified agency'))

    def test_T11_region_link_id(self):
        self.negative(lambda c: c['landing']['region_links'][0].update(region_id='../other'))

    def test_T11_region_link_no_url_or_path(self):
        for key in ('url', 'path'):
            self.negative(lambda c: c['landing']['region_links'][0].update({key: 'other'}))


if __name__ == '__main__':
    unittest.main()
