const {test}=require('node:test'),assert=require('node:assert/strict');
const Water=require('../../explore/water-detail.js');

const LIMITATION='Rivers, streams, lakes and reservoirs selected from source type codes. Displayed streams and lakes are coded perennial; some reservoirs have no hydrographic category stated by the source. Unnamed streams and intermittent water are not shown. A mapped water feature is not evidence of access or of any allowed activity.';
const SOURCE='https://www.usgs.gov/example';
const manifest={sources:{usgs_nhd:{agency:'USGS'}},layers:[]};
function declaration(id='water_streams'){
  return {id,kind:'water',limitations:LIMITATION,max_age_hours:null,source_ids:['usgs_nhd']};
}
function feature(id,name,water_class,hydro_category,extra={}){
  return {type:'Feature',geometry:{type:'MultiLineString',coordinates:[[[-106,39],[-105.9,39.1]]]},properties:{
    id,name,water_class,hydro_category,evidence:{agency:'USGS',source_url:SOURCE,retrieved_at:'2026-10-07T00:00:00Z'},...extra
  }};
}
const texts=output=>output.items.map(item=>item.text);

test('M4-B grouped stream detail uses source facts and one computed length',()=>{
  const f=feature('nhd-gnis-00174812','Roaring Fork River','stream','perennial',
    {member_count:111,length_km:48.765,water_recreation:{fishing:'allowed'}});
  const out=Water.feature(manifest,declaration(),f);
  assert.equal(out.title,'Roaring Fork River');
  assert.deepEqual(texts(out),['From the source','River or stream','Perennial','111 source segments','USGS',
    'View source ↗','Source fetched 2026-10-07',LIMITATION,'Computed by Ohvernight','48.8 km',
    'Mapped water. Access and allowed activities are not established.',
    'A mapped water feature is not permission to enter, fish, boat, paddle, swim, park or camp.']);
  assert.equal(out.items[5].url,SOURCE);
});

test('M4-B named and unnamed lake details use approved titles and hectares',()=>{
  const named=Water.feature(manifest,declaration('water_bodies'),feature('lake-1','Blue Lake','lake_pond','perennial',{area_sqkm:0.072}));
  assert.equal(named.title,'Blue Lake');
  assert.deepEqual(texts(named).slice(0,4),['From the source','Lake or pond','Perennial','USGS']);
  assert.deepEqual(texts(named).slice(7,9),['Computed by Ohvernight','7.2 ha']);
  const unnamed=Water.feature(manifest,declaration('water_bodies'),feature('lake-2',null,'lake_pond','perennial',{area_sqkm:0.02}));
  assert.equal(unnamed.title,'Unnamed lake');
});

test('M4-B reservoir with unknown category renders WW16 and never WW12',()=>{
  const named=Water.feature(manifest,declaration('water_bodies'),feature('reservoir-1','Rueter-Hess Reservoir','reservoir','unknown',{area_sqkm:5}));
  assert.equal(named.title,'Rueter-Hess Reservoir');
  assert.ok(texts(named).includes('Hydrographic category not stated by the source'));
  assert.ok(!texts(named).includes('Perennial'));
  const unnamed=Water.feature(manifest,declaration('water_bodies'),feature('reservoir-2',null,'reservoir','unknown',{area_sqkm:0.05}));
  assert.equal(unnamed.title,'Unnamed reservoir');
});

test('every M4-B water wording and type label matches its approved literal',()=>{
  assert.deepEqual(Water.wording,{
    WW1:'Mapped water. Access and allowed activities are not established.',
    WW2:'A mapped water feature is not permission to enter, fish, boat, paddle, swim, park or camp.',
    WW9:'From the source',WW10:'Computed by Ohvernight',WW12:'Perennial',WW13:'source segments',
    WW14:'Unnamed lake',WW15:'Unnamed reservoir',WW16:'Hydrographic category not stated by the source',
    river:'River or stream',lake:'Lake or pond',reservoir:'Reservoir'
  });
});

test('M4-B water details cannot render M4-C status or operator-statement strings',()=>{
  const f=feature('lake-1','Blue Lake','lake_pond','perennial',{
    water_recreation:{fishing:'Allowed',boating:'Prohibited',review:'Reviewed',access:'Not established'},
    status:'Review overdue',operator:'Agency or operator statement'
  });
  const rendered=texts(Water.feature(manifest,declaration('water_bodies'),f));
  for(const forbidden of ['Allowed','Restricted','Prohibited','Not established','Review overdue','Reviewed','Agency or operator statement'])
    assert.ok(!rendered.includes(forbidden),forbidden);
});

test('water search returns each named stream group and waterbody once and omits unnamed bodies',()=>{
  const streams=declaration('water_streams'),bodies=declaration('water_bodies');
  const region={registry:[streams,bodies],layers:new Map([
    [streams.id,{data:{features:[feature('group-1','East Plum Creek','stream','perennial'),feature('group-2','Other River','stream','perennial')]} }],
    [bodies.id,{data:{features:[feature('body-1','East Lake','lake_pond','perennial'),feature('body-2',null,'lake_pond','perennial')]}}]
  ])};
  const rows=Water.searchRows(region,'east');
  assert.deepEqual(rows.map(row=>[row.entry.id,row.feature.properties.id,row.title]),[
    ['water_streams','group-1','East Plum Creek'],['water_bodies','body-1','East Lake']
  ]);
});

const recreation=JSON.parse(require('node:fs').readFileSync(require('node:path').join(__dirname,'fixtures/water-recreation.json'),'utf8'));
const claimTexts=output=>output.items.map(item=>item.parts?item.parts.map(part=>part.text).join(''):item.text);
const claimDetail=(registry=recreation,now='2026-10-20')=>Water.feature(manifest,declaration('water_bodies'),
  feature('fixture-lake','Fixture Lake','lake_pond','perennial',{area_sqkm:0.03}),{registry,now:Date.parse(now)});

test('M4-C fixed statement strings and activity labels match byte-exact literals',()=>{
  assert.deepEqual(Water.claimWording,{
    WW3:'Not established',WW4:'Allowed',WW5:'Restricted',WW6:'Prohibited',WW7:'Review overdue',
    WW8:'Agency or operator statement',WW11:'Reviewed',
    fishing:'Fishing',boating:'Boating (motorized or trailered)',paddling:'Paddling',swimming:'Swimming',access:'Access'
  });
});

test('M4-C fixture detail orders prohibitions/restrictions before allowances, with access last and WW2 final',()=>{
  const output=claimDetail(),lines=claimTexts(output);
  assert.deepEqual(lines.slice(-8),[
    'Agency or operator statement','Fixture Operator',
    'Boating (motorized or trailered): Prohibited. Synthetic boating statement. Fixture Operator. Reviewed 2026-10-01.',
    'Paddling: Restricted. Synthetic paddling statement. Fixture Operator. Reviewed 2026-10-01.',
    'Fishing: Allowed. Synthetic fishing statement. Fixture Operator. Reviewed 2026-10-01.',
    'Swimming: Not established.', 'Access: Not established.',
    'A mapped water feature is not permission to enter, fish, boat, paddle, swim, park or camp.'
  ]);
  assert.equal(lines.includes(Water.wording.WW1),false);
  const link=output.items.find(item=>item.parts)?.parts.find(part=>part.url);
  assert.deepEqual(link,{text:'Fixture Operator',url:'https://operator.example/water/fixture'});
});

test('M4-C overdue fixture preserves restrictive words and flags while allowed becomes not established',()=>{
  const lines=claimTexts(claimDetail(recreation,'2026-12-30T00:00:01Z'));
  assert.ok(lines.includes('Boating (motorized or trailered): Prohibited. Synthetic boating statement. Fixture Operator. Reviewed 2026-10-01. Review overdue.'));
  assert.ok(lines.includes('Paddling: Restricted. Synthetic paddling statement. Fixture Operator. Reviewed 2026-10-01. Review overdue.'));
  assert.ok(lines.includes('Fishing: Not established. Fixture Operator. Reviewed 2026-10-01.'));
  assert.ok(!lines.some(line=>line.includes('Allowed')));
});

test('M4-C access restriction has its own summary, source and overdue date after all activities',()=>{
  const registry=structuredClone(recreation);
  registry.records[0].access=structuredClone(registry.records[0].claims.paddling);
  registry.records[0].access.summary='Synthetic foot-only access.';
  assert.equal(claimTexts(claimDetail(registry,'2027-01-01')).at(-2),
    'Access: Restricted. Synthetic foot-only access. Fixture Operator. Reviewed 2026-10-01. Review overdue.');
});

test('M4-C missing records preserve WW1 and WW2 without any activity wording',()=>{
  for(const registry of [null,{schema_version:1,records:[]},{schema_version:1,records:[{...recreation.records[0],water_id:'different-water'}]}]){
    const output=claimDetail(registry);
    assert.deepEqual(claimTexts(output).slice(-2),[Water.wording.WW1,Water.wording.WW2]);
    assert.ok(!claimTexts(output).some(line=>/Fishing|Boating|Paddling|Swimming|Agency or operator statement/.test(line)));
  }
});

test('M4-C malformed claims never display a status without complete evidence or an unsafe link',()=>{
  for(const field of ['source_url','agency','basis','last_checked_at','last_confirmed_at','max_age_hours']){
    const registry=structuredClone(recreation);delete registry.records[0].claims.fishing.evidence[field];
    assert.ok(claimTexts(claimDetail(registry)).includes('Fishing: Not established.'),field);
  }
  const registry=structuredClone(recreation);registry.records[0].claims.fishing.evidence.source_url='javascript:alert(1)';
  const output=claimDetail(registry);
  assert.ok(claimTexts(output).includes('Fishing: Not established.'));
  assert.ok(!output.items.some(item=>item.parts?.some(part=>part.url?.startsWith('javascript:'))));
});
