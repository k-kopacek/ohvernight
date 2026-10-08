const {test}=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const root=path.resolve(__dirname,'../..');
const read=file=>fs.readFileSync(path.join(root,file),'utf8');
const capabilities=read('explore/capabilities.js'),browse=read('explore/browse.js');
const landing=JSON.parse(read('regions/aspen/explore.json')).landing;

test('proximity listings state straight-line distance in the heading itself',()=>{
 for(const heading of ['Camping and trails by straight-line distance','Camping nearby by straight-line distance','Trails nearby by straight-line distance'])
  assert.ok(capabilities.includes("'"+heading+"'"),'Aspen heading: '+heading);
 for(const heading of ['Campgrounds nearby by straight-line distance','Trailheads nearby by straight-line distance','Trails for selected activity nearby by straight-line distance'])
  assert.ok(browse.includes("'"+heading+"'"),'Douglas heading: '+heading);
 assert.match(landing.lead,/straight-line distance/);
 // A bare "nearby" heading carries no distance basis.
 for(const bare of ["'Camping nearby'","'Trails nearby'","'Campgrounds nearby'","'Trailheads nearby'","'Nearby trails for selected activity'","'Camping near your activity'"])
  assert.ok(!capabilities.includes(bare)&&!browse.includes(bare),'bare proximity heading: '+bare);
});

test('proximity distances are never called direct',()=>{
 assert.doesNotMatch(capabilities,/mi direct/);
 assert.equal(capabilities.split(' mi straight-line').length-1,4);
 assert.match(capabilities,/straight-line pairings in this pilot/);
 assert.match(capabilities,/then straight-line distance to the nearest matching trail segment\./);
 assert.match(capabilities,/No camping listing within five straight-line miles of a matching trail segment in this small pilot\./);
 assert.match(capabilities,/No mapped trails within five straight-line miles in this pilot\./);
 assert.equal(browse.split('straight-line miles · connection unverified').length-1,2);
});

test('proximity copy implies no connection, access, recommendation or trip relevance',()=>{
 const denied=/\b(connected|accessible|recommended for|serves|nearby trip)\b/i;
 assert.doesNotMatch(capabilities,denied,'explore/capabilities.js');
 assert.doesNotMatch(browse,denied,'explore/browse.js');
 for(const [key,value] of Object.entries(landing))if(typeof value==='string')assert.doesNotMatch(value,denied,'aspen landing.'+key);
});
