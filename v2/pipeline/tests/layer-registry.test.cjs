const assert=require('node:assert/strict');
const {test}=require('node:test');
const fs=require('node:fs');
const path=require('node:path');
const {buildLayerRegistry,LayerRegistryError}=require('../../explore/layer-registry.js');
const {normalizeTransport}=require('../../explore/transport.js');
const root=path.resolve(__dirname,'../..');
const readJson=relative=>JSON.parse(fs.readFileSync(path.join(root,relative),'utf8'));

test('T2: registry joins every displayed manifest layer to presentation metadata',()=>{
  for(const id of ['aspen','douglas-co']){
    const manifest=readJson(`regions/${id}/region.json`);
    const config=readJson(`regions/${id}/explore.json`);
    const registry=buildLayerRegistry(manifest,config);
    assert.equal(registry.length,manifest.layers.length);
    assert.equal(new Set(registry.map(layer=>layer.id)).size,registry.length);
    for(const layer of registry){
      const source=manifest.layers.find(item=>item.id===layer.id);
      assert.equal(layer.description,source.limitations);
      assert.equal(layer.kind,source.kind);
      assert.equal(layer.spatialPrecision,source.spatial_precision);
      assert.equal(layer.classificationSourceField,source.classification_source_field||null);
      assert.deepEqual(layer.statusRef,source.status_ref||null);
      assert.equal(layer.maxAgeHours,source.max_age_hours);
      assert.equal(layer.canonicalPath,source.path);
    }
  }
});

test('layer registry refuses a presentation layer that is not in the manifest',()=>{
  const manifest={layers:[{id:'known',format:'feature_collection',limitations:'Context',path:'data.json'}]};
  assert.throws(()=>buildLayerRegistry(manifest,{layers:[{layer_id:'unknown',title:'x'}]}),LayerRegistryError);
});

test('water stream fit policy defaults are registry metadata and other line layers have none',()=>{
  const manifest=readJson('regions/aspen/region.json'),config=readJson('regions/aspen/explore.json');
  const registry=buildLayerRegistry(manifest,config);
  assert.deepEqual(registry.find(layer=>layer.id==='water_streams').fitPolicy,
    {tap:{max_zoom_out:2},list:{min_zoom:11}});
  assert.equal(registry.find(layer=>layer.id==='water_bodies').fitPolicy,null);
  assert.equal(registry.find(layer=>layer.id==='trails').fitPolicy,null);
  const douglas=buildLayerRegistry(readJson('regions/douglas-co/region.json'),readJson('regions/douglas-co/explore.json'));
  assert.deepEqual(douglas.find(layer=>layer.id==='waterways').fitPolicy,
    {tap:{max_zoom_out:2},list:{min_zoom:11}});
});

test('layer registry rejects malformed per-layer fit policy values',()=>{
  const manifest=readJson('regions/aspen/region.json'),config=readJson('regions/aspen/explore.json');
  config.layers.find(layer=>layer.layer_id==='water_streams').fit_policy={tap:{max_zoom_out:'2'}};
  assert.throws(()=>buildLayerRegistry(manifest,config),LayerRegistryError);
  config.layers.find(layer=>layer.layer_id==='water_streams').fit_policy={list:{min_zoom:4}};
  assert.throws(()=>buildLayerRegistry(manifest,config),LayerRegistryError);
  config.layers.find(layer=>layer.layer_id==='water_streams').fit_policy={tap:{max_zoom_out:2},list:{min_zoom:11}};
  config.layers.find(layer=>layer.layer_id==='trails').fit_policy={tap:{max_zoom_out:2},list:{min_zoom:11}};
  assert.throws(()=>buildLayerRegistry(manifest,config),LayerRegistryError);
});

test('shared transport vectors match the Python normalizer contract',()=>{
  const vectors=readJson('pipeline/tests/fixtures/transport-vectors.json');
  for(const vector of vectors) assert.deepEqual(normalizeTransport(vector.input),{record:vector.record,used:vector.used});
});
