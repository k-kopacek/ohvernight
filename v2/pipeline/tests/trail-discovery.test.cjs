const {test}=require('node:test'),assert=require('node:assert/strict');
const D=require('../../trail-discovery.js');
const feature={properties:{name:'Snowmass',trail_number:'42',activities:{hiking:{accpt:'06/01-09/30'},mountain_biking:{restricted:'01/01-12/31'}}},geometry:{type:'LineString',coordinates:[[-107,39],[-106,39]]}};
test('activity discovery requires positive source evidence; search supports names and numbers',()=>{
 assert.equal(D.matches(feature,'SNOW','hiking'),true);
 assert.equal(D.matches(feature,'42',''),true);
 assert.equal(D.matches(feature,'snow','mountain_biking'),false);
 assert.equal(D.matches(feature,'','snowmobiling'),false);
 assert.equal(D.matches(feature,'missing',''),false);
});
test('proximity uses segment interiors, not just endpoints',()=>{
 assert.equal(D.distanceMiles([-106.5,39],feature.geometry),0);
 assert.ok(Math.abs(D.distanceMiles([-106.5,39.01],feature.geometry)-0.691)<0.01);
 assert.equal(D.distanceMiles([-106.5,39],{type:'MultiLineString',coordinates:[feature.geometry.coordinates]}),0);
 assert.equal(D.distanceMiles([-106.5,39],null),Infinity);
});
test('nearby camping excludes distant records and rooms; retains conflicts for review',()=>{
 const places=[{id:'camp',kind:'campground',coordinates:[-106.5,39.01],status:'excluded'},
 {id:'room',kind:'lodging',coordinates:[-106.5,39]},
 {id:'far',kind:'dispersed',coordinates:[-106.5,40]}];
 assert.deepEqual(D.nearby(feature,places).map(x=>x.place.id),['camp']);
});
