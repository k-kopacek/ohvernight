const {test}=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const S=require('../../explore/land-style.js');const root=path.resolve(__dirname,'../..');
const read=p=>JSON.parse(fs.readFileSync(path.join(root,p),'utf8'));
const literal={
 W1:'Generalized land management context — not parcels',
 W2:'Broad areas drawn at limited scale from a national agency dataset. They show which agency the source lists as managing an area. They are not property lines and do not show who owns a specific spot.',
 W3:'Ownership or management does not establish public access. This map does not show whether you may enter, cross, park or stay.',
 W4:"PVT — the source's generalized private class; not a parcel-level finding",
 W5:'Unshaded land is unknown — not private, not public, not open',
 W6:'<code> — unrecognised source code; unknown',
 W7:'Limited-scale boundary. It cannot locate a property line or tell you whether a specific spot is inside this area.',
 W8:{USFS:'USFS — Forest Service; generalized source class',BLM:'BLM — Bureau of Land Management; generalized source class',OTHFE:'OTHFE — Other Federal; generalized source class',ST:'ST — State; generalized source class',LG:'LG — Local; generalized source class'},
 W9:'<layer title> — boundary as published by <agency>',W10:'Computer-screened research areas — not campsites',W11:'Source classification: <code>'
};
test('T4: W1-W11 are the owner-approved byte-identical literals',()=>{assert.deepEqual(S.wording,literal);assert.doesNotMatch(fs.readFileSync(path.join(root,'explore/land-style.js'),'utf8'),/verified|legal|permitted|open to/i);});
test('T4: every current layer has the specified tier, with no tier A and conservative outlines',()=>{
 for(const rid of ['aspen','douglas-co'])for(const layer of read(`regions/${rid}/region.json`).layers){
  const tier=S.tier(layer);assert.notEqual(tier,'A');
  if(layer.kind==='land_management')assert.equal(tier,'G');
  if(layer.spatial_precision==='computed')assert.equal(tier,'C');
  if(layer.kind==='wilderness')assert.equal(tier,'P');
  const style=S.style(layer,13,{properties:{[layer.classification_source_field]:'PVT'}});
  if(tier==='G'){assert.ok(style.fillOpacity<=.12);assert.ok(style.opacity<=.5);assert.equal(style.weight,1);assert.ok(style.dashArray);const high=S.style(layer,14);assert.equal(high.weight,0);assert.equal(high.stroke,false);assert.equal(high.fillOpacity,style.fillOpacity);}
  if(tier==='P'){assert.ok(style.fillOpacity<=.15);assert.ok(style.weight<=1.5);assert.equal(style.dashArray,null);}
  if(tier==='C'){assert.ok(style.fillOpacity<=.10);assert.ok(style.dashArray);}
 }
});
test('T4: class order follows data, Unknown is last even when unloaded, and palette is shared',()=>{
 const colors=[];
 for(const rid of ['aspen','douglas-co']){
  const m=read(`regions/${rid}/region.json`),layer=m.layers.find(l=>l.kind==='land_management');
  const features=read(layer.display.path).features;const codes=[...new Set(features.map(f=>f.properties[layer.classification_source_field]))];
  const legend=S.legend(layer,features);
  assert.deepEqual(legend.slice(0,3).map(x=>x.text),[literal.W1,literal.W2,literal.W3]);
  assert.deepEqual(legend.slice(3,-1).map(x=>x.text),codes.map(S.label));assert.equal(legend.at(-1).text,literal.W5);
  assert.equal(S.legend(layer,[]).at(-1).text,literal.W5);assert.ok(legend.every(x=>!['Private','Public'].includes(x.text)));
  colors.push(S.style(layer,13,{properties:{[layer.classification_source_field]:'PVT'}}).fillColor);
 }
 assert.equal(colors[0],colors[1]);assert.equal(S.label('NEW'),'NEW — unrecognised source code; unknown');
 assert.ok(!S.palette.includes(S.color('NEW')));assert.notEqual(S.color('NEW'),S.color('PVT'));
 assert.equal(S.legend({kind:'wilderness',spatial_precision:'source_published',geometry_types:['Polygon']},[],'Wilderness','USFS')[0].text,'Wilderness — boundary as published by USFS');
 assert.equal(S.legend({spatial_precision:'computed'})[0].text,literal.W10);
});
test('T4: generalized detail preserves the exact content order and verbatim fact coverage',()=>{
 const m=read('regions/douglas-co/region.json'),layer=m.layers.find(x=>x.kind==='land_management');
 const feature={properties:{manager:'PVT',evidence:{agency:'Agency',source_url:'https://agency.example',retrieved_at:'2026-09-27T00:00:00Z'}}};
 const output=S.detail(m,layer,feature);
 assert.equal(output.title,literal.W4);
 assert.deepEqual(output.items.map(x=>x.text),['Source classification: PVT',literal.W4,'Agency','View source ↗','Source fetched 2026-09-27',literal.W7,literal.W3,m.fact_coverage.ownership.statement,m.fact_coverage.public_access.statement,layer.limitations]);
 assert.equal(output.items[3].url,'https://agency.example/');
});
test('checkpoint C1: source strings avoid the access word except the literal Unknown legend',()=>{
 for(const name of ['evidence.js','land-style.js']){
  const source=fs.readFileSync(path.join(root,'explore',name),'utf8').replace(literal.W5,'');
  assert.doesNotMatch(source,/\bopen\b/i,name);
 }
});
