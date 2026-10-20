const {test}=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const root=path.resolve(__dirname,'../..'),fixture=require('./fixtures/legacy-negated-wording.json');
function files(dir){return fs.readdirSync(dir,{withFileTypes:true}).flatMap(x=>x.isDirectory()?(['pipeline','vendor'].includes(x.name)?[]:files(path.join(dir,x.name))):/\.(js|html)$/.test(x.name)?[path.join(dir,x.name)]:[]);}
test('criterion 11/A4: every denied wording occurrence is inventoried; pattern exception is exact',()=>{
 const documents=files(root).map(file=>({file:'v2/'+path.relative(root,file),text:fs.readFileSync(file,'utf8')}));
 const all=documents.map(x=>x.text).join('\n')+['aspen','douglas-co'].map(id=>fs.readFileSync(path.join(root,'regions',id,'explore.json'),'utf8')).join('\n');
 for(const item of fixture.strings)assert.ok(all.includes(item.text),'missing carried wording: '+item.text);
 for(const item of fixture.non_display_patterns){const doc=documents.find(x=>x.file===item.file);assert.equal(doc.text.split(item.text).length-1,1,'pattern must appear exactly once');}
 for(const doc of documents){
  let source=doc.text;
  for(const item of fixture.non_display_patterns)if(doc.file===item.file)source=source.replace(item.text,'');
  for(const item of fixture.strings)source=source.split(item.text).join('');
  assert.doesNotMatch(source,/verified|legal|permitted|open to/i,doc.file);
 }
});
