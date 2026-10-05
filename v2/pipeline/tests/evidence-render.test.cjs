const {test}=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const E=require('../../explore/evidence.js');
const root=path.resolve(__dirname,'../..');
const read=p=>JSON.parse(fs.readFileSync(path.join(root,p),'utf8'));
const now=Date.parse('2026-10-04T00:00:00Z');
test('T3: index transport alone supplies every real layer retrieval line and verbatim manifest statements',()=>{
 for(const id of ['aspen','douglas-co']){
  const m=read(`regions/${id}/region.json`),index=read(`regions/${id}/display/index.json`);
  assert.deepEqual(E.region(m).lines,[m.coverage.statement,...Object.values(m.fact_coverage).map(f=>f.statement),...m.known_gaps]);
  for(const layer of m.layers){
   const output=E.layer(m,layer,index,0,now);assert.equal(output.lines[0],layer.limitations);
   if(!layer.status_ref)assert.ok(output.lines.includes('No retrieval status is recorded for this layer'));
   else{
    const record=require('../../explore/transport.js').normalizeTransport(index.transport[layer.id]).record;
    if(record.status!=='available')assert.ok(output.lines.includes('Source unavailable'));
    if(record.last_retrieved_at)assert.ok(output.lines.some(line=>line.startsWith('Fetched '+record.last_retrieved_at.slice(0,10))));
   }
   assert.doesNotMatch(JSON.stringify(output.lines.slice(1)),/verified|legal|permitted|open to/i);
  }
 }
});
test('T3: provenance yields safe URLs and text without interpreting absent review or rendering data as HTML',()=>{
 const layer={limitations:'Context only.'},m={};
 const f={properties:{name:'<script>bad()</script>',evidence:{agency:'A',source_url:'javascript:bad()',retrieved_at:'2026-01-01T00:00:00Z',verification_method:null,confidence:'secret-value'}}};
 const output=E.feature(m,layer,f,'Layer');assert.equal(output.title,f.properties.name);assert.equal(output.links.length,0);
 assert.doesNotMatch(JSON.stringify(output),/secret-value|review|verified|legal|permitted|open to/i);
 assert.equal(E.safeUrl('https://agency.example/x'),'https://agency.example/x');
 assert.equal(E.safeUrl('data:text/html,bad'),null);assert.equal(E.safeUrl('/relative'),null);
 assert.deepEqual(output.lines,['A','Source fetched 2026-01-01','Context only.']);
});
test('T3: retrieval age uses the supplied policy and ignores transport confirmation',()=>{
 assert.equal(E.retrievalLine({last_retrieved_at:'2026-10-01T00:00:00Z',last_confirmed_at:'2026-10-04T00:00:00Z'},24,now),'Fetched 2026-10-01 · older than the refresh policy; refresh needed');
 assert.equal(E.retrievalLine({last_retrieved_at:'2026-10-01T00:00:00Z'},null,now),'Fetched 2026-10-01');
 assert.equal(E.retrievalLine({last_confirmed_at:'2026-10-04T00:00:00Z'},24,now),'');
});
test('T3 and criterion 11: all Explore source files avoid consuming the deprecated evidence field',()=>{
 for(const name of fs.readdirSync(path.join(root,'explore')).filter(name=>name.endsWith('.js')))
  assert.doesNotMatch(fs.readFileSync(path.join(root,'explore',name),'utf8'),/\.confidence(?![-\w])|\[['"]confidence['"]\]/,name);
 assert.doesNotMatch(fs.readFileSync(path.join(root,'explore/evidence.js'),'utf8'),/verified|legal|permitted|open to/i);
});
