const assert=require('node:assert/strict');
const {test}=require('node:test');
const fs=require('node:fs');
const path=require('node:path');
const {createRegionLoader,resolveRegionId,RegionLoaderError}=require('../../explore/region-loader.js');
const root=path.resolve(__dirname,'../..');
const readJson=relative=>JSON.parse(fs.readFileSync(path.join(root,relative),'utf8'));

function fixtureConfig(manifest,defaults=[]){
  return {explore_version:1,layers:manifest.layers.map((layer,index)=>({
    layer_id:layer.id,title:'Layer '+layer.id,order:index,default_on:defaults.includes(layer.id),min_zoom:null
  }))};
}

function fixtureFetch(manifest,config,index,regionId='aspen',missing=new Set()){
  const docs=new Map();
  docs.set(`regions/${regionId}/region.json`,manifest);
  docs.set(`regions/${regionId}/explore.json`,config);
  docs.set(`regions/${regionId}/display/index.json`,index);
  docs.set(manifest.coverage.display.path,readJson(manifest.coverage.display.path));
  for(const layer of manifest.layers){
    if(layer.format==='place_list') docs.set(layer.path,readJson(layer.path));
  }
  for(const artifact of index.artifacts){
    if(!missing.has(artifact.layer_id)) docs.set(artifact.path,readJson(artifact.path));
  }
  const calls=[];
  const fetch=async url=>{
    const clean=url.replace(/^.*?:\/\/[^/]+\//,'').split('?')[0];
    calls.push(url);
    if(!docs.has(clean)) throw new Error('missing fixture '+clean);
    return docs.get(clean);
  };
  return {fetch,calls};
}

test('T1: region loader resolves an active region, restores evidence and isolates lazy layers',async()=>{
  const manifest=readJson('regions/aspen/region.json');
  const index=readJson('regions/aspen/display/index.json');
  const first=manifest.layers.find(layer=>layer.display);
  const second=manifest.layers.find(layer=>layer.display&&layer.id!==first.id);
  const {fetch,calls}=fixtureFetch(manifest,fixtureConfig(manifest,[first.id,second.id]),index,'aspen',new Set([second.id]));
  const loader=createRegionLoader({fetch});
  const loaded=await loader.loadRegion('?region=aspen');
  assert.equal(loaded.regionId,'aspen');
  assert.equal(loaded.coverage.type,'FeatureCollection');
  assert.ok(loaded.places.overnight_options);
  assert.equal(calls.some(url=>url.includes(first.display.path)),false);
  const results=await loaded.loadDefaultLayers();
  assert.deepEqual(results.map(result=>result.state).slice(0,2),['loaded','failed']);
  assert.equal(loaded.layers.get(first.id).data.features[0].properties.evidence.constructor,Object);
  assert.equal(calls.some(url=>url.includes('v='+index.artifacts.find(item=>item.layer_id===first.id).sha256.slice(0,12))),true);
  const off=manifest.layers.find(layer=>layer.display&&layer.id!==first.id&&layer.id!==second.id);
  assert.equal(calls.some(url=>url.includes(off.display.path)),false);
  await loaded.loadLayer(off.id);
  assert.equal(calls.some(url=>url.includes(off.display.path)),true);
});

test('T2: region loader rejects malformed or unavailable regions without fallback',async()=>{
  const manifest=readJson('regions/aspen/region.json');
  const index=readJson('regions/aspen/display/index.json');
  const config=fixtureConfig(manifest);
  const {fetch}=fixtureFetch(manifest,config,index);
  const loader=createRegionLoader({fetch});
  assert.throws(()=>resolveRegionId('?region=bad_id'),error=>error.code==='REGION_NOT_FOUND');
  await assert.rejects(loader.loadRegion('?region=missing'),error=>error instanceof RegionLoaderError&&error.code==='REGION_NOT_FOUND');
  const available=await loader.loadRegion('?region=aspen');
  assert.equal(available.regionId,'aspen');
});
