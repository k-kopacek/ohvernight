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
  return {fetch,calls,docs};
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
  await assert.rejects(loader.loadRegion('?region=missing'),error=>error instanceof RegionLoaderError&&error.code==='REGION_NOT_AVAILABLE');
  const available=await loader.loadRegion('?region=aspen');
  assert.equal(available.regionId,'aspen');
});

test('T1: loader rejects malformed IDs, requires an injected default, and scopes real regions',async()=>{
  assert.throws(()=>resolveRegionId(''),error=>error.code==='REGION_NOT_FOUND');
  for(const malformed of ['ASPEN','bad_id','bad/id','..',''])
    assert.throws(()=>resolveRegionId(`?region=${encodeURIComponent(malformed)}`),error=>error.code==='REGION_NOT_FOUND');
  const aspen=readJson('regions/aspen/region.json');
  const aspenIndex=readJson('regions/aspen/display/index.json');
  const injected=fixtureFetch(aspen,fixtureConfig(aspen),aspenIndex,'aspen');
  const defaulted=createRegionLoader({fetch:injected.fetch,defaultRegion:'aspen'});
  assert.equal((await defaulted.loadRegion('')).regionId,'aspen');
  for(const regionId of ['aspen','douglas-co']){
    const manifest=readJson(`regions/${regionId}/region.json`);
    const index=readJson(`regions/${regionId}/display/index.json`);
    const fixture=fixtureFetch(manifest,fixtureConfig(manifest),index,regionId);
    await createRegionLoader({fetch:fixture.fetch,defaultRegion:regionId}).loadRegion(`?region=${regionId}`);
    assert.equal(fixture.calls.some(url=>url.includes(`regions/${regionId==='aspen'?'douglas-co':'aspen'}/`)),false);
    assert.equal(fixture.calls.filter(url=>/display\/[^/]+\.geojson/.test(url)).every(url=>/[?]v=[0-9a-f]{12}$/.test(url)),true);
  }
});

test('T1: manifest/config/index and display failures stay isolated while place-list failures are marked',async()=>{
  const manifest=readJson('regions/aspen/region.json');
  const index=readJson('regions/aspen/display/index.json');
  const first=manifest.layers.find(layer=>layer.display);
  const base=fixtureFetch(manifest,fixtureConfig(manifest,[first.id]),index);
  const pathOf=url=>url.replace(/^.*?:\/\/[^/]+\//,'').split('?')[0];
  const expectUnavailable=async(mutator)=>{
    const calls=[]; const fetch=async url=>{calls.push(url); return mutator(pathOf(url),base.docs.get(pathOf(url)));};
    await assert.rejects(createRegionLoader({fetch}).loadRegion('?region=aspen'),error=>error.code==='REGION_NOT_AVAILABLE');
  };
  await expectUnavailable((path,value)=>path.endsWith('/region.json')?Promise.reject(new Error('missing')):value);
  await expectUnavailable((path,value)=>path.endsWith('/region.json')?Promise.reject(new SyntaxError('bad json')):value);
  await expectUnavailable((path,value)=>path.endsWith('/region.json')?{...value,contract_version:2}:value);
  await expectUnavailable((path,value)=>path.endsWith('/region.json')?{...value,region:{...value.region,id:'other'}}:value);
  await expectUnavailable((path,value)=>path.endsWith('/explore.json')?Promise.reject(new Error('missing')):value);
  await expectUnavailable((path,value)=>path.endsWith('/display/index.json')?Promise.reject(new Error('missing')):value);
  const oneMissing=fixtureFetch(manifest,fixtureConfig(manifest,[first.id]),index,'aspen');
  const missingDoc=oneMissing.docs.get(first.display.path);
  oneMissing.docs.delete(first.display.path);
  const loaded=await createRegionLoader({fetch:oneMissing.fetch}).loadRegion('?region=aspen');
  const result=await loaded.loadLayer(first.id);
  assert.equal(result.state,'failed');
  oneMissing.docs.set(first.display.path,{...missingDoc,type:'FeatureCollection',layer_id:'wrong'});
  assert.equal((await loaded.loadLayer(first.id)).state,'failed');
  oneMissing.docs.set(first.display.path,{...missingDoc,type:'NotAFeatureCollection'});
  assert.equal((await loaded.loadLayer(first.id)).state,'failed');
  const place=fixtureFetch(manifest,fixtureConfig(manifest),index);
  place.docs.get('destinations.json').resorts=null;
  const withFailedPlaces=await createRegionLoader({fetch:place.fetch}).loadRegion('?region=aspen');
  assert.equal(withFailedPlaces.places.destinations.state,'failed');
  assert.equal((await withFailedPlaces.loadLayer(first.id)).state,'loaded');
  const badEvidence=fixtureFetch(manifest,fixtureConfig(manifest),index);
  const artifact=badEvidence.docs.get(first.display.path);
  artifact.features[0].properties.evidence=999;
  const bad=await createRegionLoader({fetch:badEvidence.fetch}).loadRegion('?region=aspen');
  assert.equal((await bad.loadLayer(first.id)).state,'failed');
});

test('I1: a manifest cannot make the loader request another region path',async()=>{
  const manifest=readJson('regions/aspen/region.json');
  const index=readJson('regions/aspen/display/index.json');
  const layer=manifest.layers.find(item=>item.format==='place_list');
  layer.path='regions/douglas-co/research.json';
  const fixture=fixtureFetch(manifest,fixtureConfig(manifest),index);
  const loaded=await createRegionLoader({fetch:fixture.fetch}).loadRegion('?region=aspen');
  assert.equal(loaded.places[layer.id].state,'failed');
  assert.equal(fixture.calls.some(url=>url.includes('regions/douglas-co/')),false);
});

test('criterion 10: explore modules contain no region IDs, literal region paths, or char-code defaults',()=>{
  for(const name of fs.readdirSync(path.join(root,'explore'))){
    const source=fs.readFileSync(path.join(root,'explore',name),'utf8');
    assert.doesNotMatch(source,/aspen|douglas/i,name);
    assert.doesNotMatch(source,/regions\/[a-z0-9-]+\//i,name);
    assert.doesNotMatch(source,/fromCharCode|\[\s*\d+(?:\s*,\s*\d+)+\s*\]\s*\.map/,name);
  }
});
