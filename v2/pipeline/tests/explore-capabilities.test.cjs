const {test}=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const C=require('../../explore/capabilities.js'),R=require('../../trip-rules.js'),Trust=require('../../trust.js');
const root=path.resolve(__dirname,'../..'),read=p=>JSON.parse(fs.readFileSync(path.join(root,p)));
test('T6/17.3: inventory de-duplicates RIDB and evaluates with each originating manifest policy',()=>{
 const manifest=read('regions/aspen/region.json'),curated=read('overnight-options.json').places,imported=read('ridb-options.json').places;
 const region={registry:manifest.layers.filter(x=>x.format==='place_list').map(x=>({id:x.id,kind:x.kind,format:x.format,maxAgeHours:x.max_age_hours})),places:{overnight_options:curated,ridb_options:imported},rules:read('pipeline/config/rules-registry.json')};
 const existing=new Set(curated.map(p=>p.ridb_facility_id).filter(Boolean)),merged=[...curated,...imported.filter(p=>!existing.has(p.ridb_facility_id))];
 assert.deepEqual(C.inventory(region).map(x=>x.place),merged);
 const trip={arrive:'2026-09-25',depart:'2026-09-26',vehicle:'passenger_car'};
 assert.deepEqual(C.evaluate(region,trip,'2026-09-26',Date.parse('2026-09-26')),merged.map(p=>R.evaluate(Trust.applyRules(p,region.rules,Date.parse('2026-09-26')),trip,'2026-09-26',{max_age_hours:p.source_is_search?168:720})));
});
