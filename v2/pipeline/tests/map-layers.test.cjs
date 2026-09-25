const assert=require('node:assert/strict');
const {test}=require('node:test');
const fs=require('node:fs'),path=require('node:path');
const {describe,displayWater}=require('../../map-layers.js');
const root=path.resolve(__dirname,'../..');
const bundle=JSON.parse(fs.readFileSync(path.join(root,'map-data-v2.json')));
const coverage=JSON.parse(fs.readFileSync(path.join(root,'pipeline/config/aoi.geojson')));
test('real map data is represented independently of the trip, including wilderness and research areas',()=>{
  const records=describe(bundle,coverage,5,4);
  for(const [id,key] of [['roads','mvum_roads'],['candidates','dispersed_corridors'],['wilderness','wilderness']]){
    assert.equal(records.find(d=>d.id===id).count,bundle.layers[key].features.length);
    assert.ok(records.find(d=>d.id===id).count>0);
  }
  assert.equal(records.find(d=>d.id==='coverage').count,1);
});
test('water display removes unnamed clutter without changing screening geometry',()=>{
  const before=JSON.stringify(bundle.layers.hydrology);
  const water=describe(bundle,coverage,5,4).find(d=>d.id==='water');
  assert.ok(water.count>0&&water.count<water.sourceCount);
  assert.equal(water.sourceCount,bundle.layers.hydrology.features.length);
  assert.equal(JSON.stringify(bundle.layers.hydrology),before);
  const feature=(name,kind='flowline',type='LineString')=>({properties:{name,kind},geometry:{type,coordinates:[]}});
  assert.equal(displayWater(feature('River')),true);
  assert.equal(displayWater(feature('Lake','waterbody','Polygon')),true);
  for(const name of [null,undefined,'','   '])assert.equal(displayWater(feature(name)),false);
  assert.equal(displayWater(feature('Wetland','area','Polygon')),false);
  assert.equal(displayWater(feature('River','flowline','Polygon')),false);
  assert.equal(displayWater({properties:{name:'Lake',kind:'waterbody'},geometry:null}),false);
});
test('missing, empty, and failed sources produce different explanations',()=>{
  const get=b=>describe(b,null,0,0).find(d=>d.id==='roads');
  assert.equal(get(null).status,'Data not loaded');
  const empty={layers:{mvum_roads:{features:[]}},source_status:{'02_fetch_mvum_roads':{status:'available'}}};
  assert.equal(get(empty).status,'No features in this dataset');
  empty.source_status['02_fetch_mvum_roads'].status='unavailable';
  assert.equal(get(empty).status,'Source unavailable');
});
test('an unconfirmed fire monitor without geometry does not count as a mapped restriction',()=>{
  const records=describe({layers:{fire_restriction_stage:{features:[{geometry:null,properties:{status:'unknown'}}]}}},null,0,0);
  const restrictions=records.find(d=>d.id==='restrictions');
  assert.equal(restrictions.count,0);
  assert.match(restrictions.status,/coverage incomplete/);
});
