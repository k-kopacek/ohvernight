const assert=require('node:assert/strict');
const {test}=require('node:test');
const fs=require('node:fs'),path=require('node:path');
const {displayWater}=require('../../map-layers.js');
const root=path.resolve(__dirname,'../..');
const bundle=JSON.parse(fs.readFileSync(path.join(root,'map-data-v2.json')));
const {createRegionLoader}=require('../../explore/region-loader.js');
const E=require('../../explore/evidence.js');
const manifest=JSON.parse(fs.readFileSync(path.join(root,'regions/aspen/region.json')));
const read=p=>JSON.parse(fs.readFileSync(path.join(root,p.split('?')[0])));
const load=()=>createRegionLoader({fetch:async p=>read(p),defaultRegion:'aspen'}).loadRegion('');
const vectors=JSON.parse(fs.readFileSync(path.join(root,'pipeline/tests/fixtures/display-water-vectors.json')));
test('trail pilot is independently loaded and missing trail data is explicit',async()=>{
  const trails=read('trails.geojson'),region=await load();
  assert.equal(region.layers.get('trails').state,'idle');
  const result=await region.loadLayer('trails');
  assert.equal(result.count,trails.features.length);assert.ok(result.count>0);
  const missing=await createRegionLoader({fetch:async p=>{if(p.startsWith('regions/aspen/display/trails.geojson'))throw Error('missing');return read(p);},defaultRegion:'aspen'}).loadRegion('');
  assert.equal((await missing.loadLayer('trails')).state,'failed');
});
test('real map data is represented independently of the trip, including wilderness and research areas',async()=>{
  const region=await load();
  for(const key of ['mvum_roads','dispersed_corridors','wilderness']){
    const result=await region.loadLayer(key);assert.equal(result.count,bundle.layers[key].features.length);assert.ok(result.count>0);
  }
  assert.equal(region.coverage.features.length,1);
});
test('grouped water display preserves canonical hydrology for setback screening',()=>{
  const before=JSON.stringify(bundle.layers.hydrology);
  assert.equal(bundle.layers.hydrology.features.length,6926);
  assert.equal(JSON.stringify(bundle.layers.hydrology),before);
  const waterArtifacts=read('regions/aspen/display/index.json').artifacts;
  assert.equal(waterArtifacts.find(x=>x.layer_id==='water_streams').feature_count,69);
  assert.equal(waterArtifacts.find(x=>x.layer_id==='water_bodies').feature_count,46);
  const feature=(name,kind='flowline',type='LineString')=>({properties:{name,kind},geometry:{type,coordinates:[]}});
  assert.equal(displayWater(feature('River')),true);
  assert.equal(displayWater(feature('Lake','waterbody','Polygon')),true);
  assert.equal(displayWater({properties:{name:'Douglas River',source_layer:'flowline'},geometry:{type:'MultiLineString',coordinates:[]}}),true);
  assert.equal(displayWater({properties:{name:'Douglas Lake',source_layer:'waterbody'},geometry:{type:'MultiPolygon',coordinates:[]}}),true);
  for(const name of [null,undefined,'','   '])assert.equal(displayWater(feature(name)),false);
  assert.equal(displayWater(feature('Wetland','area','Polygon')),false);
  assert.equal(displayWater(feature('River','flowline','Polygon')),false);
  assert.equal(displayWater({properties:{name:'Lake',kind:'waterbody'},geometry:null}),false);
});

test('display-water vectors remain in parity with the Python artifact builder',()=>{
 for(const vector of vectors){
   assert.equal(displayWater({properties:{name:vector.name,kind:vector.kind},geometry:vector.geometry}),vector.expected,vector.name);
 }
});
test('missing, empty, and failed sources produce different explanations',()=>{
  const roads=manifest.layers.find(x=>x.id==='mvum_roads');
  const get=(transport,count=0)=>E.layer(manifest,roads,{transport:{mvum_roads:transport}},count,Date.parse('2026-10-04T00:00:00Z'));
  assert.ok(get(null).lines.includes('No retrieval status is recorded for this layer'));
  assert.deepEqual(get({status:'available'}).lines,[roads.limitations]);
  assert.ok(get({status:'unavailable'}).lines.includes('Source unavailable'));
  assert.ok(get({status:'unavailable'},1).lines.includes('latest fetch failed'));
});
test('an unconfirmed fire monitor without geometry does not count as a mapped restriction',async()=>{
  const region=await load(),result=await region.loadLayer('fire_restriction_stage');
  assert.equal(result.data.features.filter(f=>f.geometry).length,0);
  assert.ok(E.region(manifest).lines.includes(manifest.fact_coverage.closures.statement));
  assert.match(manifest.fact_coverage.closures.statement,/No mapped closure does not mean no closure/);
});
