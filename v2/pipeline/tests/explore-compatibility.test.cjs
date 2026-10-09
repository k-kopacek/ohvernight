const {test}=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const T=require('../../trail-discovery.js'),D=require('../../explore/trail-seasons.js');
const root=path.resolve(__dirname,'../..'),read=p=>JSON.parse(fs.readFileSync(path.join(root,p),'utf8'));
const base=read('pipeline/tests/fixtures/explore-compatibility.json');
const real=read('pipeline/tests/fixtures/explore-real-compatibility.json');
test('17.3: saved plan export shape is pinned before moving the writer',()=>{
 const fixture=read('pipeline/tests/fixtures/explore-plan-export.json'),f=fixture.feature;
 const B=require('../../explore/browse.js');
 assert.deepEqual(B.buildPlan(new Map([[f.properties.id,f]]),[f.properties.id],{start:'2026-10-01',end:'2026-10-02',activity:'hiking',vehicle:'Car / SUV'},'fixed notes','2026-10-01T00:00:00.000Z'),fixture.expected);
});
test('T9/A6: every real nearby list keeps base IDs, ordering and displayed distances',()=>{
 const a=read('regions/aspen/display/trails.geojson').features,places=read('overnight-options.json').places,
  d=read('regions/douglas-co/display/trails.geojson').features,points=read('regions/douglas-co/display/recreation.geojson').features;
 const near=(f,list,n)=>list.map(x=>({id:x.properties.id,miles:T.distanceMiles(x.geometry.coordinates,f.geometry)})).filter(x=>x.miles<=5).sort((x,y)=>x.miles-y.miles).slice(0,n).map(x=>({id:x.id,distance:x.miles.toFixed(1)}));
 for(const x of real.aspenTrails)assert.deepEqual(T.nearby(a.find(f=>f.properties.id===x.id),places).map(y=>({id:y.place.id,distance:y.miles.toFixed(1)})),x.rows,x.id);
 for(const x of real.aspenPlaces)assert.deepEqual(T.nearbyTrails(places.find(p=>p.id===x.id),a).map(y=>({id:y.feature.properties.id,distance:y.miles.toFixed(1)})),x.rows,x.id);
 for(const x of real.douglasTrails){const f=d.find(f=>f.properties.id===x.id);assert.deepEqual(near(f,D.camping(points),3),x.camps,x.id);assert.deepEqual(near(f,points.filter(p=>p.properties.site_type==='TRAILHEAD'),3),x.heads,x.id);}
 for(const x of real.douglasPoints)for(const {activity,rows} of x.activities){const p=points.find(p=>p.properties.id===x.id);assert.deepEqual(d.filter(f=>T.matches(f,'',activity)).map(f=>({id:f.properties.id,miles:T.distanceMiles(p.geometry.coordinates,f.geometry)})).filter(y=>y.miles<=5).sort((a,b)=>a.miles-b.miles).slice(0,5).map(y=>({id:y.id,distance:y.miles.toFixed(1)})),rows,x.id+' '+activity);}
});
test('T8/A6: real GPX uses approved rounded geometry including a pinned dropped part',()=>{
 const features=read('regions/douglas-co/display/trails.geojson').features;
 for(const row of Object.values(real.gpx))assert.equal(D.gpx(features.find(f=>f.properties.id===row.id)),row.text,row.id);
});
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
  trailheads:data.layers.recreation.features.filter(f=>f.properties.site_type==='TRAILHEAD').length,
  otherSites:data.layers.recreation.features.filter(f=>!['CAMPGROUND','TRAILHEAD','DISPERSED_AREA'].includes(f.properties.site_type)).length},base.browseCounts);
 assert.ok(fs.readFileSync(path.join(root,'regions/douglas-co/extras.js'),'utf8').includes('const area='+base.rampartText+';'));
 assert.ok(fs.readFileSync(path.join(root,'regions/douglas-co/extras.js'),'utf8').includes(base.coverage));
 const B=require('../../explore/browse.js'),extras=require('../../regions/douglas-co/extras.js');
 for(const mode of ['trails','camping','trailheads','other-sites'])assert.equal(B.rows(data.layers.trails.features,data.layers.recreation.features,extras.area,mode,'','').length,base.browseCounts[mode==='other-sites'?'otherSites':mode]);
 assert.equal(B.rows(data.layers.trails.features,data.layers.recreation.features,extras.area,'other-sites','Cabin Ridge','').length,1,'other sites are searchable by name');
});
