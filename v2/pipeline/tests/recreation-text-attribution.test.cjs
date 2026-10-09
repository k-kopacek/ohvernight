const {test}=require('node:test'),a=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
globalThis.ExploreEvidence={safeUrl:url=>url};
const B=require('../../explore/browse.js');
const sites=JSON.parse(fs.readFileSync(path.join(__dirname,'../../regions/douglas-co/research.json'),'utf8')).layers.recreation.features;
function node(tag,text,className){
 const n={tag,textContent:text||'',className,children:[],dataset:{},append(...xs){n.children.push(...xs);},replaceChildren(...xs){n.children=xs;},setAttribute(){},addEventListener(){}};return n;
}
const flat=n=>[n,...n.children.flatMap(flat)];
function render(feature){
 const shell={element:node,button:(text)=>node('button',text),$:()=>node('div'),extras:undefined,showList(){},showSources(){},showDetail(){},isListActive:()=>false,openDialog(){},
  region:{config:{capabilities:{saved_list:false,gpx_export:false},storage_keys:{plan:'p',notes:'n',trip:'t'},trip_defaults:{activity:'motorcycling',vehicle:'Car / SUV'},export_names:{}},
   registry:[{kind:'trails',id:'trails'},{kind:'recreation_sites',id:'recreation'}],layers:new Map([['trails',{state:'loaded',data:{features:[]}}],['recreation',{state:'loaded',data:{features:sites}}]])}};
 const box=node('div');B.attach(shell).detail({id:'recreation'},feature,box);return flat(box).slice(1);
}
const texts=nodes=>nodes.map(n=>n.textContent);
const byName=name=>sites.find(f=>f.properties.name===name);
test('a record with no agency page shows no descriptive source text and says it is withheld',()=>{
 const f=byName('RAMPART ENTRANCE'),p=f.properties,out=texts(render(f));
 a.ok(p.directions&&p.important_info&&p.activity_type_list&&!p.usda_portal_url&&!p.rec1stop_url,'fixture record still has text and no agency page');
 for(const key of ['directions','important_info','activity_type_list'])a.ok(!out.includes(p[key]),key+' is not rendered');
 for(const heading of ['Agency directions','Important information','Listed activities'])a.ok(!out.includes(heading),heading);
 a.equal(out.filter(x=>x===B.WITHHELD).length,1);
 a.ok(out.includes('Source ↗')&&!out.includes('Publisher page ↗'),'the data service is not labelled an official listing');
});
test('a record with an agency page renders its text as before, with no notice',()=>{
 const f=sites.find(x=>x.properties.usda_portal_url&&x.properties.directions&&x.properties.site_type==='TRAILHEAD'),out=texts(render(f));
 a.ok(out.includes('Agency directions')&&out.includes(f.properties.directions));
 a.ok(!out.includes(B.WITHHELD)&&out.includes('Publisher page ↗'));
 const rec={...f,properties:{...f.properties,usda_portal_url:null,rec1stop_url:'https://www.recreation.gov/camping/campgrounds/1'}};
 a.ok(texts(render(rec)).includes(f.properties.directions),'either agency page field is enough');
});
test('the rule is general: it withholds by missing agency page, and never withholds a restriction',()=>{
 a.deepEqual(sites.filter(B.withheld).map(f=>f.properties.name).sort(),['DEVILS HEAD TH','RAMPART ENTRANCE','TURKEY']);
 const synthetic={type:'Feature',geometry:null,properties:{id:'x',name:'X',site_type:'TRAILHEAD',directions:'Go north.',restrictions:'No fires.',evidence:{source_url:'https://example.test/rest'}}};
 const out=texts(render(synthetic));a.ok(out.includes('No fires.')&&out.includes('Published restrictions')&&!out.includes('Go north.')&&out.includes(B.WITHHELD));
 a.ok(!B.withheld({properties:{id:'y',site_type:'TRAILHEAD',evidence:{}}}),'nothing to withhold means no notice');
 a.doesNotMatch(fs.readFileSync(path.join(__dirname,'../../explore/browse.js'),'utf8'),/RAMPART ENTRANCE|TURKEY|DEVILS HEAD|recreation-33/);
});
test('the withheld notice makes no positive claim',()=>{
 for(const text of [B.WITHHELD,'Source data service ↗'])a.doesNotMatch(text,/\b(allowed|open|legal|permitted|verified|in season)\b/i);
});

test('publisher labels require a record field that identifies an agency page',()=>{
 a.equal(B.sourceLinkLabel({properties:{evidence:{source_url:'https://example.test/rest'}}}),'Source ↗');
 a.equal(B.sourceLinkLabel({properties:{rec1stop_url:'https://www.recreation.gov/facility/1',evidence:{source_url:'https://example.test/rest'}}}),'Publisher page ↗');
 a.equal(B.sourceLinkLabel({properties:{usda_portal_url:'https://www.fs.usda.gov/page'}}),'Publisher page ↗');
});
test('missing recreation values are stated without broadening rendered record types',()=>{
 const f={type:'Feature',geometry:null,properties:{id:'missing',name:'Missing fields',site_type:'CAMPGROUND',evidence:{source_url:'https://example.test/rest'}}};
 const out=texts(render(f));
 for(const heading of ['Published restrictions','Fees (verify current price)','Published season (may be historical)','Water','Restrooms'])a.ok(out.includes(heading),heading+' field remains visible');
 a.equal(out.filter(x=>x==='Not stated in this source record').length,5);
 const unsupported={type:'Feature',geometry:null,properties:{id:'other',name:'Other',site_type:'PICNIC SITE',restrictions:'X'}};
 a.deepEqual(texts(render(unsupported)),[]);
});
test('Douglas source site types do not fall through to campground',()=>{
 const record={properties:{id:'x',name:'Picnic Site',site_type:'PICNIC SITE'}};
 const plan=B.buildPlan(new Map([['x',record]]),['x'],{},'', '2026-10-09T00:00:00Z');
 a.equal(plan.saved[0].type,'Picnic Site');
});
