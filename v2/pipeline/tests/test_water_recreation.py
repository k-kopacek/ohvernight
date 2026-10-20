"""Fixture-only R74/R76 mutation proofs; no claim content for real waters."""
import copy
import json
import sys
import unittest
from pathlib import Path

V2 = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(V2 / 'pipeline/scripts'))
from lib.region_contract import ContractError, validate_water_recreation_data


class WaterRecreationTests(unittest.TestCase):
    def fixture(self):
        registry = json.loads((Path(__file__).parent / 'fixtures/water-recreation.json').read_text())
        manifest = {'region': {'id': 'synthetic'}, 'layers': [
            {'id': 'bodies', 'kind': 'water'}, {'id': 'streams', 'kind': 'water'},
            {'id': 'roads', 'kind': 'roads'}], 'fact_coverage': {'recreation_permission': {
                'state': 'reviewed_partial', 'layer_ids': ['bodies', 'streams']}}}
        return manifest, registry

    def validate(self, manifest, registry):
        return validate_water_recreation_data(manifest, registry, {'fixture-lake', 'fixture-stream-group'})

    def test_valid_registry_and_independent_same_page_evidence(self):
        manifest, registry = self.fixture()
        original = copy.deepcopy(registry)
        self.assertTrue(self.validate(manifest, registry))
        self.assertEqual(registry, original)
        # Equal evidence values in independent JSON objects are explicitly valid.
        self.assertEqual(registry['records'][0]['claims']['fishing']['evidence'],
                         registry['records'][0]['claims']['boating']['evidence'])

    def assert_mutation(self, rule, mutate):
        manifest, registry = self.fixture()
        self.assertTrue(self.validate(manifest, registry))
        mutate(manifest, registry)
        with self.assertRaises(ContractError) as error:
            self.validate(manifest, registry)
        self.assertEqual(error.exception.rule, rule)

    def test_R74_single_mutations(self):
        def record(registry): return registry['records'][0]
        def claim(registry): return record(registry)['claims']['fishing']
        mutations = {
            'unresolved water ID': lambda m,r: record(r).update(water_id='absent'),
            'duplicate water ID': lambda m,r: r['records'].append(copy.deepcopy(record(r))),
            'missing activity': lambda m,r: record(r)['claims'].pop('swimming'),
            'extra activity': lambda m,r: record(r)['claims'].update(camping={'status':'unknown'}),
            'bad status': lambda m,r: claim(r).update(status='supported'),
            'missing summary': lambda m,r: claim(r).pop('summary'),
            'missing evidence': lambda m,r: claim(r).pop('evidence'),
            'empty summary': lambda m,r: claim(r).update(summary=''),
            'blank summary': lambda m,r: claim(r).update(summary='   '),
            'long summary': lambda m,r: claim(r).update(summary='x'*161),
            'unknown summary': lambda m,r: record(r)['claims']['swimming'].update(summary='x'),
            'unknown evidence': lambda m,r: record(r)['claims']['swimming'].update(evidence={}),
            'shared evidence reference': lambda m,r: record(r)['claims']['boating'].update(evidence=claim(r)['evidence']),
            'access allowed': lambda m,r: record(r).update(access=copy.deepcopy(claim(r))),
            'access prohibited': lambda m,r: record(r).update(access={'status':'prohibited'}),
            'access restricted without evidence': lambda m,r: record(r).update(access={'status':'restricted','summary':'Foot only.'}),
            'schema version': lambda m,r: r.update(schema_version=2),
            'extra registry field': lambda m,r: r.update(community=[]),
            'empty operator': lambda m,r: record(r).update(operator=''),
            'missing access': lambda m,r: record(r).pop('access'),
        }
        for field in ('source_url','agency','basis','last_checked_at','last_confirmed_at','max_age_hours'):
            mutations['missing evidence '+field] = lambda m,r,f=field: claim(r)['evidence'].pop(f)
        for field,value in [('source_url','ftp://operator.example/a'),('source_url','https:///missing-host'),
                            ('agency',''),('basis','source_fetch'),('last_checked_at','bad'),
                            ('last_confirmed_at','2026-02-30'),('max_age_hours',0),
                            ('max_age_hours',True),('max_age_hours',-1),('effective_to','bad')]:
            mutations['invalid '+field+' '+str(value)] = lambda m,r,f=field,v=value: claim(r)['evidence'].update({f:v})
        for name, mutate in mutations.items():
            with self.subTest(mutation=name): self.assert_mutation('R74', mutate)

    def test_R74_every_non_claim_host_and_subdomain(self):
        config = json.loads((V2 / 'pipeline/config/water_display.json').read_text())
        for host in config['non_claim_hosts']:
            for hostname in (host, 'nested.'+host):
                with self.subTest(host=hostname):
                    self.assert_mutation('R74', lambda m,r: r['records'][0]['claims']['fishing']['evidence'].update(
                        source_url='https://'+hostname+'/statement'))
        manifest, registry = self.fixture()
        registry['records'][0]['claims']['fishing']['evidence']['source_url']='https://notreddit.com/statement'
        self.assertTrue(self.validate(manifest, registry))

    def test_R74_stream_group_resolves_and_access_restriction_has_own_evidence(self):
        manifest, registry = self.fixture()
        registry['records'][0]['water_id']='fixture-stream-group'
        registry['records'][0]['access']=copy.deepcopy(registry['records'][0]['claims']['paddling'])
        self.assertTrue(self.validate(manifest, registry))

    def test_R76_both_directions_and_water_layers(self):
        for state in ('none','context'):
            with self.subTest(state=state):
                self.assert_mutation('R76', lambda m,r: m['fact_coverage']['recreation_permission'].update(state=state))
        for ids in ([], ['bodies'], ['bodies','streams','roads'], ['roads'], ['bodies','streams','streams']):
            with self.subTest(ids=ids):
                self.assert_mutation('R76', lambda m,r: m['fact_coverage']['recreation_permission'].update(layer_ids=ids))
        self.assert_mutation('R76', lambda m,r: r.update(records=[]))
        manifest, registry = self.fixture()
        manifest['fact_coverage']['recreation_permission']['state']='context'
        self.assertFalse(self.validate(manifest, None))
        self.assertFalse(self.validate(manifest, {'schema_version':1,'records':[]}))

class WaterRecreationIntegrationTests(unittest.TestCase):
    def fixture(self):
        import test_region_contract
        manifest, docs = test_region_contract.RegionContractTests().display_base(
            {'type':'Polygon','coordinates':[[[0,0],[0.1,0],[0.1,0.1],[0,0.1],[0,0]]]})
        registry = WaterRecreationTests().fixture()[1]
        registry['records'][0]['water_id']='water-1'
        manifest['water_recreation']={'path':'regions/synthetic/water-recreation.json'}
        manifest['fact_coverage']['recreation_permission']['state']='reviewed_partial'
        docs[manifest['water_recreation']['path']]=registry
        return manifest, docs

    def test_registry_resolves_in_full_contract_without_rules_or_reviewed_sites(self):
        from lib.region_contract import validate_region_data
        manifest, docs = self.fixture()
        validate_region_data(manifest, docs.__getitem__)
        # Only recreation_permission gets the extension; other dimensions keep R05.
        manifest['fact_coverage']['camping_permission'].update(state='reviewed_partial')
        with self.assertRaises(ContractError) as error: validate_region_data(manifest, docs.__getitem__)
        self.assertEqual(error.exception.rule, 'R05')

    def test_registry_missing_or_other_region_path_fails_R74(self):
        from lib.region_contract import validate_region_data
        for path in ('regions/other/water-recreation.json', 'regions/synthetic/water-recreation.json'):
            manifest, docs = self.fixture()
            docs.pop(manifest['water_recreation']['path'])
            manifest['water_recreation']['path']=path
            with self.assertRaises(ContractError) as error: validate_region_data(manifest, docs.__getitem__)
            self.assertEqual(error.exception.rule, 'R74')

    def test_all_unknown_rejected_but_access_only_restriction_passes(self):
        manifest, registry = WaterRecreationTests().fixture()
        record=registry['records'][0]
        access=copy.deepcopy(record['claims']['paddling'])
        record['claims']={name:{'status':'unknown'} for name in record['claims']}
        with self.assertRaises(ContractError) as error:
            validate_water_recreation_data(manifest, registry, {'fixture-lake'})
        self.assertEqual(error.exception.rule, 'R74')
        record['access']=access
        self.assertTrue(validate_water_recreation_data(manifest, registry, {'fixture-lake'}))

    def test_non_claim_host_list_is_exact_and_every_entry_has_local_provenance(self):
        config=json.loads((V2/'pipeline/config/water_display.json').read_text())
        provenance=json.loads((Path(__file__).parent/'fixtures/non-claim-hosts-provenance.json').read_text())
        self.assertEqual(config['non_claim_hosts'], sorted(provenance))
        for host,ref in provenance.items():
            line=(V2.parent/ref['file']).read_text().splitlines()[ref['line']-1]
            self.assertIn(host, line, host)


if __name__ == '__main__': unittest.main()
