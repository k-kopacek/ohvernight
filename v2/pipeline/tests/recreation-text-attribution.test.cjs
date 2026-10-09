const {test}=require('node:test'),a=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
globalThis.ExploreEvidence={safeUrl:url=>url};
const B=require('../../explore/browse.js');
const sites=JSON.parse(fs.readFileSync(path.join(__dirname,'../../regions/douglas-co/research.json'),'utf8')).layers.recreation.features,extras=require('../../regions/douglas-co/extras.js'),D=require('../../explore/trail-seasons.js');
function node(tag,text,className){
 const n={tag,textContent:text||'',className,children:[],dataset:{},append(...xs){n.children.push(...xs);},replaceChildren(...xs){n.children=xs;},setAttribute(){},addEventListener(){}};return n;
}
const flat=n=>[n,...n.children.flatMap(flat)];
function render(feature,savedList=false){
 const map=node('div');map.parentNode={append(){}};
 const shell={element:node,button:(text)=>node('button',text),$:()=>map,extras:undefined,showList(){},showSources(){},showDetail(){},isListActive:()=>false,openDialog(){},
  region:{config:{capabilities:{saved_list:savedList,gpx_export:false},storage_keys:{plan:'p',notes:'n',trip:'t'},trip_defaults:{activity:'motorcycling',vehicle:'Car / SUV'},export_names:{}},
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
 a.ok(out.includes('Source data service ↗')&&!out.includes('Official listing / source ↗'),'the data service is not labelled an official listing');
});
test('a record with an agency page renders its text as before, with no notice',()=>{
 const f=sites.find(x=>x.properties.usda_portal_url&&x.properties.directions&&x.properties.site_type==='TRAILHEAD'),out=texts(render(f));
 a.ok(out.includes('Agency directions')&&out.includes(f.properties.directions));
 a.ok(!out.includes(B.WITHHELD)&&out.includes('Official listing / source ↗'));
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
test('Other listed sites keeps exactly the 14 non-campground, non-trailhead records out of other modes',()=>{
 const expected=['recreation-3300079','recreation-3301118','recreation-3301271','recreation-3304676','recreation-3305503','recreation-3305648','recreation-3307252','recreation-3308608','recreation-3310872','recreation-3311222','recreation-3313457','recreation-3316544','recreation-3319912','recreation-3322652'];
 const all=sites.filter(f=>!['CAMPGROUND','TRAILHEAD','DISPERSED_AREA'].includes(f.properties.site_type));
 a.deepEqual(B.rows([],sites,null,'other-sites','','').map(f=>f.properties.id),expected);
 a.equal(B.rows([],sites,null,'other-sites','Cabin Ridge','').length,1);
 a.deepEqual(B.rows([],sites,null,'trailheads','').map(f=>f.properties.id),sites.filter(f=>f.properties.site_type==='TRAILHEAD').map(f=>f.properties.id));
 a.deepEqual(B.rows([],sites,null,'camping','').map(f=>f.properties.id),require('../../explore/trail-seasons.js').camping(sites).map(f=>f.properties.id));
 a.deepEqual(B.rows([],sites,extras.area,'camping','').map(f=>f.properties.id),[extras.area.properties.id,...D.camping(sites).map(f=>f.properties.id)]);
 a.equal(all.length,14);a.equal(B.rows([],sites,null,'camping','').length,5);
 for(const f of all){a.equal(B.kind(f),f.properties.site_type.toLowerCase().replace(/^./,c=>c.toUpperCase()));a.notEqual(B.kind(f),'Campground');}
 const cabin=byName('CABIN RIDGE PS'),plan=B.buildPlan(new Map([[cabin.properties.id,cabin]]),[cabin.properties.id],{start:'2026-10-10',end:'2026-10-11'},'','2026-10-09');a.equal(plan.saved[0].type,'Picnic site','saved details keep the source type');
});
test('other-site detail displays attributed source fields and suppresses absent, placeholder and status values',()=>{
 const cabin=byName('CABIN RIDGE PS'),topaz=byName('TOPAZ POINT'),cabinText=texts(render(cabin)).join('\n'),topazText=texts(render(topaz)).join('\n');
 const cabinNodes=texts(render(cabin)),credit=cabinNodes.indexOf('Published by the Forest Service — not reviewed by Ohvernight');a.ok(credit>=0);
 a.ok(credit<cabinNodes.indexOf('Source site type')&&credit<cabinNodes.indexOf('Published restrictions (source text)'),'attribution precedes source facts');
 for(const key of ['fee_description','restrictions','restroom_availability','water_availability'])a.ok(cabinText.includes(cabin.properties[key]),key+' is byte-for-byte source text');
 a.ok(cabinText.includes('Source site type')&&cabinText.includes('Picnic site'));
 for(const key of ['open_season','water_availability','restroom_availability'])a.ok(topazText.includes(topaz.properties[key]),'Topaz shows '+key);
 a.ok(topazText.includes('May 15')&&!topazText.includes('Day Use')&&!topazText.includes('Overnight use prohibited'));
 a.deepEqual(texts(render(topaz)).filter(x=>['Source site type','Published restrictions (source text)','Listed activities (source text)','Fee information (source text; may be historical)','Season text (source; may be historical)','Water details (source text)','Restroom details (source text)','Important information (source text)','Directions (source text; route and conditions not reviewed)'].includes(x)),['Source site type','Season text (source; may be historical)','Water details (source text)','Restroom details (source text)']);
 const dakan=byName('DAKAN'),dakanText=texts(render(dakan)).join('\n');
 a.ok(dakanText.includes(dakan.properties.restroom_availability));a.ok(!dakanText.includes('N/A')&&!dakanText.includes('No Data'));
 for(const f of sites.filter(x=>!['CAMPGROUND','TRAILHEAD','DISPERSED_AREA'].includes(x.properties.site_type))){
  const rendered=texts(render(f)),full=rendered.join('\n');
  a.ok(!full.includes(f.properties.seasonal_operational_status),'operational status stays hidden for '+f.properties.name);
  a.ok(!rendered.includes('Campground')||f.properties.site_type==='CAMPGROUND','other source types are not labelled Campground: '+f.properties.name);
  a.ok(!full.includes('No Data')&&!full.includes('N/A'),'placeholders stay hidden for '+f.properties.name);
  a.equal(rendered.filter(x=>x==='Published by the Forest Service — not reviewed by Ohvernight').length,1,'one source attribution for '+f.properties.name);
  const page=Boolean(B.agencyPage(f)),nodes=render(f),fields=[['site_type','Source site type',false],['restrictions','Published restrictions (source text)',false],['activity_type_list','Listed activities (source text)',true],['fee_description','Fee information (source text; may be historical)',false],['open_season','Season text (source; may be historical)',false],['water_availability','Water details (source text)',false],['restroom_availability','Restroom details (source text)',false],['important_info','Important information (source text)',true],['directions','Directions (source text; route and conditions not reviewed)',true]];
  for(const [key,label,descriptive] of fields){const value=f.properties[key],present=typeof value==='string'&&value.trim()&&!['no data','n/a'].includes(value.trim().toLowerCase()),shown=present&&(!descriptive||page);if(shown)a.ok(rendered.includes(key==='site_type'?B.kind(f):value),key+' source text rendered for '+f.properties.name);a.equal(rendered.includes(label),Boolean(shown),key+' field label presence for '+f.properties.name);}
  a.ok(nodes.some(node=>node.tag==='a'&&node.href===(B.agencyPage(f)||f.properties.evidence?.source_url)),'agency listing or source-data link present for '+f.properties.name);
  if(!page&&B.withheld(f))a.ok(rendered.includes(B.WITHHELD),'unattributed descriptive text stays withheld for '+f.properties.name);
  // Raw publisher values are checked above and intentionally excluded from the app-copy scan: this source snapshot itself includes "DAY USE AREA", "Day Use", and "NOT ALLOWED".
  const raw=['site_type','restrictions','activity_type_list','fee_description','open_season','water_availability','restroom_availability','important_info','directions'].map(key=>f.properties[key]).filter(value=>typeof value==='string'&&value);raw.push(B.kind(f));
  const appCopy=raw.reduce((text,value)=>text.split(value).join(''),full);
  a.doesNotMatch(appCopy,/\b(open|closed|allowed|permitted|legal|free|suitable|good for|recommended|verified|day use)\b/i,'Ohvernight-added wording carries no status or suitability claim for '+f.properties.name);
 }
 const saved=texts(render(byName('CABIN RIDGE PS'),true));a.ok(saved.includes('Save to plan')&&saved.includes('Saving stores this source record in your saved list.'));
});
test('a non-page record still withholds descriptive text while showing structured fields',()=>{
 const f={type:'Feature',geometry:null,properties:{id:'synthetic-other',name:'Synthetic',site_type:'PICNIC SITE',water_availability:'No',directions:'Unattributed directions',important_info:'Unattributed details',activity_type_list:'HIKING',evidence:{source_url:'https://example.test/layer'}}};
 const out=texts(render(f));a.ok(out.includes('No'));a.ok(out.includes('Source site type'));a.ok(!out.includes('Unattributed directions')&&!out.includes('Unattributed details')&&!out.includes('HIKING'));a.ok(out.includes(B.WITHHELD));
});
