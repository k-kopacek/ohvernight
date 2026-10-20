const {test}=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const {createRegionLoader}=require('../../explore/region-loader.js');
const C=require('../../explore/capabilities.js'),T=require('../../trail-discovery.js');
const root=path.resolve(__dirname,'../..'),read=p=>JSON.parse(fs.readFileSync(path.join(root,p.split('?')[0])));
const hidden=['dispersed_corridors','dispersed_corridor_points'];
const bundle=read('map-data-v2.json');
const researchIds=new Set(hidden.flatMap(id=>bundle.layers[id].features.map(f=>f.properties.id)));
const load=()=>createRegionLoader({defaultRegion:'aspen',fetch:async p=>read(p)}).loadRegion('');

test('Aspen has no research-area display declaration, artifact or registry entry',async()=>{
 const region=await load();
 assert.ok(researchIds.size>0,'canonical research evidence remains available for later retirement');
 assert.equal(region.manifest.layers.some(x=>x.kind==='research_areas'),false);
 assert.equal(region.registry.some(x=>x.kind==='research_areas'||hidden.includes(x.id)),false);
 for(const id of hidden){
  assert.equal(region.config.layers.some(x=>x.layer_id===id),false);
  assert.equal(region.index.artifacts.some(x=>x.layer_id===id),false);
  assert.equal(Object.hasOwn(region.index.transport,id),false);
  assert.equal(fs.existsSync(path.join(root,'regions/aspen/display',id+'.geojson')),false);
  await assert.rejects(region.loadLayer(id),/Unknown layer/);
 }
 await region.loadDefaultLayers({zoom:12});
 const features=[...region.layers.values()].flatMap(x=>x.data?.features||[]);
 assert.equal(features.some(f=>researchIds.has(f.properties.id)),false);
});

test('Aspen search, trip candidates, saved-plan IDs and nearby pairings exclude research areas',async()=>{
 const region=await load();
 await region.loadDefaultLayers({zoom:12});
 const trip={arrive:'2026-07-10',depart:'2026-07-12',vehicle:'passenger_car'};
 const inventory=C.inventory(region).map(x=>x.place),candidates=C.evaluate(region,trip,'2026-07-10',Date.parse('2026-07-10'));
 const trails=region.registry.filter(x=>x.kind==='trails').flatMap(x=>region.layers.get(x.id).data.features);
 const search=trails.filter(f=>T.matches(f,'',''));
 for(const list of [inventory,candidates,search])assert.equal(list.some(x=>researchIds.has(x.id||x.properties.id)),false);
 // Plan A / backup restoration accepts only IDs in this same inventory.
 const saveableIds=new Set(inventory.map(x=>x.id));
 for(const id of researchIds)assert.equal(saveableIds.has(id),false);
 assert.equal(region.config.capabilities.saved_list,false,'Aspen does not attach the Douglas saved/Finder capability');
 for(const trail of trails)assert.equal(T.nearby(trail,inventory).some(x=>researchIds.has(x.place.id)),false);
 for(const activity of Object.keys(T.activities))assert.equal(T.adventureOptions(candidates,trails,activity).some(x=>researchIds.has(x.place.id)),false);
 assert.ok(inventory.some(p=>p.kind==='campground'),'developed campground inventory remains present');
 assert.ok(inventory.some(p=>p.kind==='dispersed'),'independent dispersed listings remain present');
});
