const {test}=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const T=require('../../trail-discovery.js'),D=require('../../regions/douglas-co/discovery.js');
const root=path.resolve(__dirname,'../..'),read=p=>JSON.parse(fs.readFileSync(path.join(root,p),'utf8'));
const base=read('pipeline/tests/fixtures/explore-compatibility.json');
test('T8: trail seasons, windows, days and GPX equal pinned base-commit outputs',()=>{
 for(const x of base.seasonCases)assert.equal(D.season({properties:{activities:{motorcycling:x.r}}},'motorcycling',x.start,x.end),x.expected);
 for(const x of base.windows)assert.deepEqual(D.windows(x.input),x.expected);
 for(const x of base.days)assert.deepEqual(D.days(x.start,x.end),x.expected);
 assert.equal(D.gpx(base.feature),base.gpx);
});
test('T9: adventure ordering, trail search and both nearby lists equal base-commit outputs',()=>{
 assert.deepEqual(T.nearby(base.feature,base.places),base.nearby);
 assert.deepEqual(T.nearbyTrails(base.places[0],[base.feature,base.feature]),base.nearbyTrails);
 assert.deepEqual(T.adventureOptions(base.places,[base.feature],'hiking'),base.adventure);
 for(const x of base.matches)assert.equal(T.matches(base.feature,x.query,x.activity),x.expected);
});
test('T9: Douglas browse mode counts, Rampart literal and coverage note are pinned before migration',()=>{
 const data=read('regions/douglas-co/research.json');
 assert.deepEqual({trails:data.layers.trails.features.length,camping:1+D.camping(data.layers.recreation.features).length,
  trailheads:data.layers.recreation.features.filter(f=>f.properties.site_type==='TRAILHEAD').length},base.browseCounts);
 assert.ok(fs.readFileSync(path.join(root,'regions/douglas-co/preview.js'),'utf8').includes('const area='+base.rampartText+';'));
 assert.ok(fs.readFileSync(path.join(root,'regions/douglas-co/index.html'),'utf8').includes(base.coverage));
});
