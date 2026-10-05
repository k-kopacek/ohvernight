import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {resolve} from 'node:path';
import {setTimeout as delay} from 'node:timers/promises';

const INIT=`(()=>{
 let app,renderer;window.__rendered=[];window.__handed={};window.__visible={};
 Object.defineProperty(window,'L',{configurable:true,get(){return renderer},set(value){renderer=value;const original=value.geoJSON;value.geoJSON=function(data,options){const result=original.call(this,data,options);window.__rendered.push(result);return result;}}});
 let adapter;Object.defineProperty(window,'ExploreMap',{configurable:true,get(){return adapter},set(value){adapter=value;for(const method of ['addLayer','setPins']){const original=value[method];value[method]=function(id,data,...args){window.__handed[id]=method==='addLayer'?data.features:data;window.__visible[id]=true;return original.call(this,id,data,...args);};}const original=value.setVisible;value.setVisible=function(id,value){window.__visible[id]=value;return original.call(this,id,value);};}});
 Object.defineProperty(window,'explore',{configurable:true,get(){return app},set(value){app=value;for(const name of ['mapUsable','defaultLayersLoaded']){let state=value.state[name];Object.defineProperty(value.state,name,{get(){return state},set(next){state=next;if(next)window['__'+name+'Resources']=performance.getEntriesByType('resource').map(x=>x.name);}});}}});
 try{localStorage.setItem('ohvernight-trip-v1',JSON.stringify({trip:{resort:'aspen',arrive:'2026-07-10',depart:'2026-07-12',vehicle:'passenger_car'},plan:{a:'difficult',b:'silverbar'}}));localStorage.setItem('ohvernight-douglas-plan-v1',JSON.stringify(['usfs-trail-8939494']));localStorage.setItem('ohvernight-douglas-plan-v1-notes','compatibility notes');localStorage.setItem('ohvernight-douglas-plan-v1-trip',JSON.stringify({start:'2026-09-25',end:'2026-09-26',activity:'hiking',vehicle:'Truck with trailer'}));}catch{}
})()`;
const AREA=`(()=>{let n=0,free=0;const m=explore.$('map');for(let y=2;y<innerHeight;y+=4)for(let x=2;x<innerWidth;x+=4){n++;const e=document.elementFromPoint(x,y);if(e&&m.contains(e)&&!e.closest('.leaflet-control'))free++;}return 100*free/n})()`;
const RECT=`e=>{const r=e.getBoundingClientRect();return {x:r.x,y:r.y,width:r.width,height:r.height}}`;
const visible=`e=>{const r=e.getBoundingClientRect();return r.width>0&&r.height>0&&getComputedStyle(e).visibility!=='hidden'&&!e.closest('dialog:not([open]),[hidden],[inert]')}`;
export async function runExploreChecks(client,origin,signal,root){
 let running=true,current={externalBlocked:0,responses:[],escaped:[],errors:[],consoleErrors:[]},pumpError;
 const interception=async(method,params)=>{try{return await client.command(method,params);}catch(error){if(!error.message.includes('Invalid InterceptionId'))throw error;}};
 const evaluate=async expression=>{signal.throwIfAborted();if(pumpError)throw pumpError;const r=await client.command('Runtime.evaluate',{expression,awaitPromise:true,returnByValue:true});if(r.exceptionDetails)throw new Error(expression+' '+JSON.stringify(r.exceptionDetails));return r.result.value;};
 const pump=(async()=>{while(running){const e=client.events.shift();if(!e){await delay(5,undefined,{signal});continue;}
  if(e.method==='Fetch.requestPaused'){
   const {requestId,request}=e.params,url=new URL(request.url);
   if(url.origin!==origin){current.externalBlocked++;await interception('Fetch.failRequest',{requestId,errorReason:'BlockedByClient'});continue;}
   const replacement=await current.intercept?.(url);
   if(replacement)await interception('Fetch.fulfillRequest',{requestId,responseCode:replacement.status||200,responseHeaders:[{name:'Content-Type',value:'application/json'}],body:Buffer.from(replacement.body||'').toString('base64')});
   else await interception('Fetch.continueRequest',{requestId});
  }else if(e.method==='Network.responseReceived'&&current){const response=e.params.response;if(new URL(response.url).origin===origin)current.responses.push({url:response.url,status:response.status});else if(!response.url.startsWith('data:'))current.escaped.push(response.url);}
  else if(e.method==='Runtime.exceptionThrown'&&current)current.errors.push(e.params.exceptionDetails);
  else if(e.method==='Log.entryAdded'&&current&&e.params.entry.level==='error'&&!e.params.entry.text.includes('ERR_BLOCKED_BY_CLIENT'))current.consoleErrors.push(e.params.entry.text);
 }} )().catch(error=>{pumpError=error;});
 await client.command('Network.enable');await client.command('Network.setCacheDisabled',{cacheDisabled:true});await client.command('Runtime.enable');await client.command('Log.enable');await client.command('Page.enable');
 await client.command('Fetch.enable',{patterns:[{urlPattern:'*',requestStage:'Request'}]});
 await client.command('Page.addScriptToEvaluateOnNewDocument',{source:INIT});
 await client.command('Emulation.setEmulatedMedia',{features:[{name:'prefers-reduced-motion',value:'reduce'}]});
 const poll=async(expression,label)=>{for(let i=0;i<600;i++){signal.throwIfAborted();if(await evaluate(expression))return;await delay(20,undefined,{signal});}throw new Error('Browser state did not settle: '+label+' '+JSON.stringify(await evaluate('window.explore?.state')));};
 const key=async key=>{await client.command('Input.dispatchKeyEvent',{type:'keyDown',key,code:key,windowsVirtualKeyCode:key==='Escape'?27:9});await client.command('Input.dispatchKeyEvent',{type:'keyUp',key,code:key,windowsVirtualKeyCode:key==='Escape'?27:9});};
 async function navigate(url,intercept){
  await client.command('Page.navigate',{url:'about:blank'});current={url,responses:[],errors:[],consoleErrors:[],escaped:[],externalBlocked:0,intercept};
  await client.command('Page.navigate',{url});await poll('!!window.explore&&(explore.state.defaultLayersLoaded||explore.state.error)','load');assert.deepEqual(current.errors,[],'uncaught browser errors');if(!intercept){assert.deepEqual(current.consoleErrors,[],'browser console errors');assert.ok(current.responses.every(x=>x.status<400),'same-origin request failed');}assert.deepEqual(current.escaped,[],'non-local request escaped blocking');return current;
 }
 const bytes=async urls=>{let count=0;const paths=new Set();for(const url of new Set(urls)){const u=new URL(url);if(u.origin!==origin)continue;let p=resolve(root,'.'+u.pathname);if(u.pathname.endsWith('/'))p=resolve(p,'index.html');if(!paths.has(p)){paths.add(p);count+=(await readFile(p)).length;}}return count;};
 async function drag(point,dx,dy){await client.command('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:[{x:point.x,y:point.y}]});for(let i=1;i<=5;i++)await client.command('Input.dispatchTouchEvent',{type:'touchMove',touchPoints:[{x:point.x+dx*i/5,y:point.y+dy*i/5}]});await client.command('Input.dispatchTouchEvent',{type:'touchEnd',touchPoints:[]});}
 async function assertSelection(label,cleared=false){
  const selection=await evaluate(`(()=>{
   const paths=window.__rendered.flatMap(g=>Object.values(g._layers)).filter(l=>l.options.selected).map(l=>l.feature.properties.id);
   const pins=[...document.querySelectorAll('.leaflet-marker-icon.is-selected')].map(e=>({id:e.dataset.featureId,pressed:e.getAttribute('aria-pressed')}));
   return {id:explore.state.selection?.featureId,paths,pins};
  })()`);
  const ids=[...new Set([...selection.paths,...selection.pins.map(p=>p.id)])];
  assert.deepEqual(ids,cleared?[]:[selection.id],label+' exact selected id and no others');
  for(const pin of selection.pins)assert.equal(pin.pressed,'true',label+' pin pressed');
  if(cleared)assert.equal(selection.id,undefined,label+' shell cleared');
 }
 let gestureSequence=0;
 async function flick(point,dy){
  const timestamp=4102444800+(gestureSequence++);
  await client.command('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:[point],timestamp});
  await client.command('Input.dispatchTouchEvent',{type:'touchMove',touchPoints:[{x:point.x,y:point.y+dy}],timestamp:timestamp+.04});
  await client.command('Input.dispatchTouchEvent',{type:'touchEnd',touchPoints:[],timestamp:timestamp+.08});
 }
 const results=[];
 try{
 for(const id of ['aspen','douglas-co'])for(const [width,height,minimum] of [[320,568,72],[390,844,80],[768,1024,80],[1440,900,75]]){
  console.log('B1–B10 '+id+' '+width+'×'+height);
  await client.command('Emulation.setDeviceMetricsOverride',{width,height,deviceScaleFactor:width<1200?2:1,mobile:width<1200});await client.command('Emulation.setTouchEmulationEnabled',{enabled:true});
  const url=id==='douglas-co'?origin+'/v2/regions/douglas-co/':origin+'/v2/?region='+id+'&view=map';await navigate(url);
  assert.equal(await evaluate('explore.state.error'),undefined,'B7 isolated region load');
  const result={region:id,viewport:[width,height],checks:[]};
  const free=await evaluate(AREA),sheet=await evaluate('('+RECT+')(explore.$("sheet"))');assert.ok(free>=minimum,'B1 free map '+free);if(width<768)assert.ok(sheet.height<=(width===320?88:96));else assert.ok(sheet.width<=(width===768?360:380));result.freeMapPct=free;result.checks.push('B1');
  assert.equal(await evaluate('document.documentElement.scrollWidth>innerWidth'),false,'B2 horizontal scroll');
  const small=await evaluate(`[...document.querySelectorAll('button,input,select,textarea,summary,[role=button],a')].filter(${visible}).filter(e=>!e.closest('.leaflet-control-attribution')&&!(e.tagName==='A'&&e.closest('p')&&e.parentElement.childNodes.length>1)).filter(e=>{const r=e.getBoundingClientRect();return r.width<44||r.height<44}).map(e=>e.id||e.textContent)`);assert.deepEqual(small,[],'B2 target size');result.checks.push('B2');
  assert.equal(await evaluate('[...document.querySelectorAll(".leaflet-marker-icon")].every(e=>e.tabIndex===0&&!!e.title&&e.getBoundingClientRect().width>=44&&e.getBoundingClientRect().height>=44)'),true,'B2 pins focusable, named and 44px');
  await evaluate('explore.$("layers").click()');const drawer=await evaluate('('+RECT+')(explore.$("drawer"))');if(width<768){assert.ok(drawer.height<=height*.6);assert.ok(await evaluate(AREA)>=35,'B3 map visible');result.drawerFreeMapPct=await evaluate(AREA);assert.ok(result.drawerFreeMapPct>=45,'A11 meaningful map above drawer');assert.equal(await evaluate('explore.sheet.state'),'collapsed','A11 drawer collapses sheet');}else assert.ok(drawer.width<=360);
  const toggle=await evaluate('explore.region.registry.find(x=>x.format==="feature_collection"&&explore.region.layers.get(x.id).count>0).id');
  await evaluate(`document.getElementById(${JSON.stringify('layer-')}+${JSON.stringify(toggle)}).click()`);assert.equal(await evaluate(`window.__visible[${JSON.stringify(toggle)}]`),false,'B3 map toggle off');assert.equal(await evaluate('explore.$("drawer").hidden'),false);await evaluate(`document.getElementById('layer-'+${JSON.stringify(toggle)}).click()`);assert.equal(await evaluate(`window.__visible[${JSON.stringify(toggle)}]`),true);await key('Escape');assert.equal(await evaluate('explore.$("drawer").hidden&&document.activeElement===explore.$("layers")'),true,'B3 closes and restores focus');result.checks.push('B3');
  await evaluate('explore.sheet.setExpanded(false)');
  if(width<768){
   result.sheetFreeMapPct={};
   for(const state of ['collapsed','half','expanded']){await evaluate('explore.sheet.setState('+JSON.stringify(state)+')');result.sheetFreeMapPct[state]=await evaluate(AREA);}
   await evaluate('explore.sheet.setState("collapsed")');const unchanged=await evaluate('explore.state.view.center');
   const headerPoint=()=>evaluate('(()=>{const r=explore.$("sheet-toggle").getBoundingClientRect();return {x:r.x+r.width/2,y:r.y+24}})()');
   for(const [dy,state] of [[-60,'half'],[-60,'expanded'],[60,'half'],[60,'collapsed']]){await flick(await headerPoint(),dy);assert.equal(await evaluate('explore.sheet.state'),state,'A11 synthetic sheet swipe');}
   assert.deepEqual(await evaluate('explore.state.view.center'),unchanged,'A11 sheet swipe never pans map');
   async function slowSheetDrag(start,dy,content=false){
    const pt=content?await evaluate('(()=>{const r=explore.$("sheet-body").getBoundingClientRect();return {x:r.x+3,y:r.y+36}})()'):await headerPoint();
    const initial=await evaluate('explore.$("sheet").getBoundingClientRect().height');
    await client.command('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:[pt]});
    for(let i=1;i<=3;i++){await delay(110,undefined,{signal});await client.command('Input.dispatchTouchEvent',{type:'touchMove',touchPoints:[{x:pt.x,y:pt.y+dy*i/3}]});
     const h=await evaluate('explore.$("sheet").getBoundingClientRect().height');if(i<3){assert.ok(dy<0?h>initial:h<initial,'A11 sheet follows finger before release');assert.ok(h>64&&h<height*.75,'A11 intermediate height between endpoints');}}
    await client.command('Input.dispatchTouchEvent',{type:'touchEnd',touchPoints:[]});
   }
   await slowSheetDrag('collapsed',-height*.65);await evaluate('explore.$("search").click()');assert.equal(await evaluate('explore.sheet.state'),'expanded','A11 long swipe skips half');
   await evaluate('explore.$("sheet-body").scrollTop=0');await slowSheetDrag('expanded',height*.35,true);assert.equal(await evaluate('explore.sheet.state'),'half','A11 content at top drags sheet');
   await evaluate('explore.$("sheet-body").scrollTop=0');await slowSheetDrag('half',height*.2,true);assert.equal(await evaluate('explore.sheet.state'),'collapsed','A11 half content at top collapses');
   await evaluate('explore.sheet.setState("expanded");explore.$("sheet-body").scrollTop=120');const scrolled=await evaluate('explore.$("sheet-body").scrollTop');assert.ok(scrolled>0,'A11 scrollable content fixture');
   const cp=await evaluate('(()=>{const r=explore.$("sheet-body").getBoundingClientRect();return {x:r.x+20,y:r.y+50}})()');await drag(cp,0,35);assert.equal(await evaluate('explore.sheet.state'),'expanded','A11 scrolled content keeps sheet state');assert.ok(await evaluate('explore.$("sheet-body").scrollTop')<scrolled,'A11 scrolled content scrolls independently');
   assert.deepEqual(await evaluate('explore.state.view.center'),unchanged,'A11 content drags never pan map');await evaluate('explore.sheet.setState("collapsed")');

   await evaluate('explore.drawer.open();explore.sheet.setState("half")');assert.equal(await evaluate('explore.$("drawer").hidden'),true,'A11 sheet opening closes drawer');
   await evaluate('explore.drawer.open();explore.$("map").dispatchEvent(new MouseEvent("click",{bubbles:true}))');assert.equal(await evaluate('explore.$("drawer").hidden'),true,'A11 exposed map tap dismisses drawer');
   await evaluate('explore.drawer.open()');const hp=await evaluate('(()=>{const r=explore.$("drawer").querySelector(".explore-heading h1").getBoundingClientRect();return {x:r.x+20,y:r.y+12}})()');await client.command('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:[hp]});await client.command('Input.dispatchTouchEvent',{type:'touchMove',touchPoints:[{x:hp.x,y:hp.y+40}]});assert.ok(await evaluate('explore.$("drawer").getBoundingClientRect().bottom>innerHeight'),'A11 drawer follows finger before release');await client.command('Input.dispatchTouchEvent',{type:'touchEnd',touchPoints:[]});assert.equal(await evaluate('explore.$("drawer").hidden'),true,'A11 drawer swipe dismisses');
  }
  const point=await evaluate(`(()=>{const m=explore.$('map');for(let y=150;y<innerHeight-120;y+=20)for(let x=80;x<innerWidth-80;x+=20){const e=document.elementFromPoint(x,y);if(m.contains(e)&&!e.closest('.leaflet-control'))return {x,y};}throw Error('no free map point')})()`);
  const center=await evaluate('explore.state.view.center');await drag(point,35,25);await poll('JSON.stringify(explore.state.view.center)!=='+JSON.stringify(JSON.stringify(center)),'map drag');
  await evaluate('explore.sheet.setExpanded(true)');const after=await evaluate('explore.state.view.center'),inside=await evaluate('(()=>{const r=explore.$("sheet-body").getBoundingClientRect();return {x:r.x+r.width/2,y:r.y+80}})()');await drag(inside,0,-40);await evaluate('new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve)))');assert.deepEqual(await evaluate('explore.state.view.center'),after,'B4 sheet drag does not pan');result.checks.push('B4');
  const expanded=await evaluate('('+RECT+')(explore.$("sheet"))');if(width<768)assert.ok(expanded.height<=height*.75);else assert.ok(expanded.width<=(width===768?360:380));await evaluate('explore.sheet.setExpanded(false)');
  const controls=await evaluate(`(()=>{const a=[...document.querySelectorAll('button,a,input,select,textarea,summary,[tabindex="0"]')].filter(${visible});a.forEach((e,i)=>e.dataset.focusCheck=String(i));return a.map(e=>e.dataset.focusCheck)})()`),seen=new Set();await evaluate('document.activeElement.blur()');
  for(let i=0;i<controls.length*2+6;i++){await key('Tab');const focus=await evaluate('({id:document.activeElement.dataset.focusCheck,inBody:!!document.activeElement.closest("#explore-sheet-body")})');if(focus.id)seen.add(focus.id);assert.equal(focus.inBody,false,'B5 collapsed body inert');}
  for(const control of controls)assert.ok(seen.has(control),'B5 unreachable control '+control);assert.equal(await evaluate(`[...document.querySelectorAll('[tabindex]')].some(e=>Number(e.getAttribute('tabindex'))>0)`),false);result.checks.push('B5');
  await evaluate('explore.$("layers").click();explore.$("sources").click()');assert.equal(await evaluate('explore.$("source-dialog").open'),true);await key('Escape');await key('Escape');
  await evaluate('explore.$("search").click()');assert.equal(await evaluate('!explore.$("list-view").hidden&&explore.sheet.expanded&&!document.querySelector("dialog[open]")'),true,'B6 search opens persistent sheet list with map exposed');await evaluate(`(()=>{
   const list=[...explore.$('list-view').children].find(e=>!e.hidden),query=list.querySelector('#query')||explore.$('query');
   const result=[...list.querySelectorAll('button')].find(e=>e.classList.contains('explore-result')||e.parentElement===explore.$('search-results'));
   if(!result)throw Error('A11 no search result');
   const title=result.querySelector('strong')?.textContent||result.textContent;
   query.value=title.split(' · #')[0];query.dispatchEvent(new Event('input',{bubbles:true}));
   window.__a11Query=query;window.__a11Value=query.value;window.__a11List=list;
   const filtered=[...list.querySelectorAll('button')].filter(e=>e.classList.contains('explore-result')||e.parentElement===explore.$('search-results'));
   if(!filtered.length)throw Error('A11 filtered list disappeared');window.__a11Count=filtered.length;filtered[0].click();
  })()`);
  await assertSelection('A11 selected search result');
  assert.equal(await evaluate('!explore.$("detail-view").hidden&&explore.$("list-view").hidden&&!document.querySelector("dialog[open]")'),true,'A11 selection opens sheet detail');
  await evaluate('explore.$("detail-back").click()');await assertSelection('A11 Back clears result',true);
  assert.equal(await evaluate('window.__a11List.parentElement===explore.$("list-view")&&!window.__a11List.hidden&&window.__a11Query.value===window.__a11Value'),true,'A11 Back preserves list and filter');
  assert.equal(await evaluate('[...window.__a11List.querySelectorAll("button")].filter(e=>e.classList.contains("explore-result")||e.parentElement===explore.$("search-results")).length'),await evaluate('window.__a11Count'),'A11 filtered results persist');
  await key('Escape');
  async function checkTargets(){const small=await evaluate(`[...document.querySelectorAll('button,input,select,textarea,summary,[role=button],a')].filter(${visible}).filter(e=>!e.closest('.leaflet-control-attribution')&&!(e.tagName==='A'&&e.closest('p')&&e.parentElement.childNodes.length>1)).filter(e=>{const r=e.getBoundingClientRect();return r.width<44||r.height<44}).map(e=>e.id||e.textContent)`);assert.deepEqual(small,[],'B2 overlay target size');}
  const overlays=await evaluate('[...document.querySelectorAll("dialog")].length');for(let i=0;i<overlays;i++){await evaluate(`(()=>{const d=document.querySelectorAll('dialog')[${i}];explore.openDialog(d);return d.open})()`);await checkTargets();await key('Escape');}
  await evaluate('explore.drawer.close();explore.sheet.setExpanded(false)');assert.ok(await evaluate(AREA)>=(width===1440?90:minimum),'B6 restored map '+JSON.stringify(await evaluate('({free:'+AREA+',open:[...document.querySelectorAll("dialog[open]")].map(x=>x.id),drawer:explore.$("drawer").hidden})') ));result.checks.push('B6');
  const manifest=JSON.parse(await readFile(resolve(root,'v2/regions',id,'region.json'))),index=JSON.parse(await readFile(resolve(root,'v2/regions',id,'display/index.json')));
  const mapResources=await evaluate('window.__mapUsableResources'),allResources=await evaluate('window.__defaultLayersLoadedResources');
  result.mapUsableBytes=await bytes([url,origin+'/v2/index.html',...mapResources]);result.defaultOnBytes=await bytes([url,origin+'/v2/index.html',...allResources]);assert.ok(result.mapUsableBytes<=500000,'B7 map usable bytes '+result.mapUsableBytes);assert.ok(result.defaultOnBytes<=4500000,'B7 default bytes '+result.defaultOnBytes);
  assert.equal(current.responses.some(x=>x.url.includes('/regions/'+(id==='aspen'?'douglas-co':'aspen')+'/')),false,'B7 cross-region request');assert.equal(current.responses.some(x=>/\/map-data-v2.json|\/research.json/.test(x.url)),false,'B7 canonical geometry fetch');
  await evaluate('explore.showSources()');const delivered=await evaluate('Object.fromEntries(Object.entries(window.__handed).map(([id,features])=>[id,features.length]))'),nonSpatial=[];
  for(const artifact of index.artifacts){const doc=JSON.parse(await readFile(resolve(root,'v2',artifact.path)));assert.equal(delivered[artifact.layer_id],doc.features.length,'B7 every feature handed to renderer '+artifact.layer_id);for(const f of doc.features.filter(x=>x.geometry===null)){const declaration=manifest.layers.find(x=>x.id===artifact.layer_id);assert.equal(declaration.allow_null_geometry,true);assert.ok(await evaluate(`!!document.querySelector('[data-nonspatial="'+${JSON.stringify(artifact.layer_id)}+'"]')`));nonSpatial.push({layer:artifact.layer_id,id:f.properties.id,consumer:'source panel and Trust.sourceSummary'});}}
  assert.equal(current.responses.some(x=>/\/map-data-v2.json|\/research.json/.test(x.url)),false,'B7 source panel canonical geometry fetch');assert.equal(current.responses.some(x=>x.url.includes('/regions/'+(id==='aspen'?'douglas-co':'aspen')+'/')),false,'B7 source panel region isolation');
  result.nonSpatialRecords=nonSpatial;await key('Escape');result.checks.push('B7');
  assert.equal(await evaluate('explore.region.regionId'),id,'B9 active region');
  const stored=await evaluate('explore.capabilities.trip');if(id==='aspen'){assert.equal(stored.arrive,'2026-07-10');assert.equal(stored.depart,'2026-07-12');assert.deepEqual(await evaluate('explore.capabilities.plan'),{a:'difficult',b:'silverbar'});}else{assert.equal(await evaluate('location.search'),'?region=douglas-co&view=map');assert.equal(stored.vehicle,'Truck with trailer');assert.equal(stored.activity,'hiking');assert.ok((await evaluate('explore.capabilities.saved')).includes('usfs-trail-8939494'));await evaluate('explore.sheet.setExpanded(true);[...explore.$("sheet-body").querySelectorAll("button")].find(x=>x.textContent==="Saved plan").click()');assert.equal(await evaluate('document.getElementById("feedback").value'),'compatibility notes');await key('Escape');await evaluate('explore.sheet.setExpanded(false)');}result.checks.push('B9');
  const land=manifest.layers.find(x=>x.kind==='land_management');await evaluate('explore.$("fit").click()');await evaluate('explore.$("layers").click()');assert.ok((await evaluate('explore.$("drawer").textContent')).includes('Turn layers on or off. Colors explain what the map can tell you; they do not prove a place is legal to camp.'),'B10 carried disclaimer');assert.ok((await evaluate('explore.$("drawer").textContent')).includes('All layers start on. Dates and vehicle choices do not hide map features. Tap a road or shaded area to learn more.'),'B10 carried instructions');assert.ok((await evaluate('explore.$("drawer").textContent')).includes('Unshaded land is unknown — not private, not public, not open'),'B10 Unknown legend');
  const styles=await evaluate(`window.__rendered.flatMap(group=>{const out=[];group.eachLayer(layer=>{if(window.__handed[${JSON.stringify(land.id)}].some(f=>f.properties.id===layer.feature?.properties?.id))out.push({weight:layer.options.weight,opacity:layer.options.opacity,fillOpacity:layer.options.fillOpacity,dashArray:layer.options.dashArray});});return out;})`);assert.ok(styles.length);for(const style of styles){assert.equal(style.fillOpacity,.12);assert.equal(style.weight,1);assert.equal(style.opacity,.5);assert.equal(style.dashArray,'5 5');}
  await evaluate('explore.drawer.close();for(let i=0;i<8&&explore.state.view.zoom<14;i++)explore.$("zoom-in").click()');assert.ok(await evaluate('explore.state.view.zoom')>=14);const strokes=await evaluate(`window.__rendered.flatMap(group=>{const out=[];group.eachLayer(layer=>{if(window.__handed[${JSON.stringify(land.id)}].some(f=>f.properties.id===layer.feature?.properties?.id))out.push(layer.options.stroke);});return out;})`);assert.ok(strokes.every(x=>x===false),'B10 outline removed at zoom14');result.checks.push('B10');
  await evaluate(`(()=>{
   const entry=explore.region.registry.find(e=>e.kind==='trails'),f=explore.region.layers.get(entry.id).data.features.find(f=>f.properties.name&&f.geometry);
   window.__a11Trail=f;window.__a11TrailEntry=entry;
   const item=window.__rendered.flatMap(g=>Object.values(g._layers)).find(l=>l.feature?.properties?.id===f.properties.id);
   if(!item)throw Error('A11 trail renderer item absent');item.fire('click',{latlng:item.getBounds().getCenter()});
  })()`);
  assert.equal(await evaluate('explore.state.selection.featureId===window.__a11Trail.properties.id&&!explore.$("detail-view").hidden'),true,'A11 trail tap selects and opens detail');await assertSelection('A11 exact trail tap');
  assert.equal(await evaluate(`(()=>{const b=ExploreShell.bounds({features:[window.__a11Trail]}),v=explore.state.view.bounds;return v[0][0]<=b[0][0]&&v[0][1]<=b[0][1]&&v[1][0]>=b[1][0]&&v[1][1]>=b[1][1]})()`),true,'A11 full trail bounds fitted');
  const trailText=await evaluate('explore.$("detail-view").textContent'),trailFields=await evaluate('window.__a11Trail.properties');
  for(const value of [trailFields.name,trailFields.trail_number,trailFields.surface,trailFields.allowed_terra_use].filter(Boolean))assert.ok(trailText.includes(value),'A11 carried trail field');
  assert.ok(trailText.includes('Source fetched '+trailFields.evidence.retrieved_at.slice(0,10)));
  assert.ok(trailText.includes(manifest.layers.find(e=>e.kind==='trails').limitations),'A11 trail limitation');assert.doesNotMatch(trailText,/\blength\b|elevation gain/i,'A11 no fabricated trail measures');
  await evaluate('explore.$("detail-back").click()');
  const landTexts=await evaluate(`(()=>{const entry=explore.region.registry.find(e=>e.kind==='land_management'),f=explore.region.layers.get(entry.id).data.features[0];window.__a11LandId=f.properties.id;const item=window.__rendered.flatMap(g=>Object.values(g._layers)).find(l=>l.feature?.properties?.id===f.properties.id);item.fire('click',{latlng:item.getBounds().getCenter()});return ExploreLand.detail(explore.manifest,explore.manifest.layers.find(e=>e.id===entry.id),f).items.map(x=>x.text)})()`);
  assert.deepEqual(await evaluate('[...explore.$("detail-body").querySelectorAll("p,a")].slice(0,'+landTexts.length+').map(e=>e.textContent)'),landTexts,'A11 land detail exact wording and order');
  assert.equal(await evaluate('!explore.$("detail-view").hidden&&explore.state.selection?.featureId===window.__a11LandId'),true,'A11 land tap selects');await assertSelection('A11 exact land tap');assert.ok(!['Private','Public'].includes(await evaluate('explore.$("detail-title").textContent')));
  await evaluate('explore.$("detail-back").click();explore.sheet.setExpanded(false)');
  await evaluate(`(()=>{
   const entry=explore.region.registry.find(e=>e.format==='place_list'&&e.kind==='overnight_inventory')||explore.region.registry.find(e=>e.kind==='recreation_sites');
   const f=entry.format==='place_list'?explore.region.places[entry.id][0]:explore.region.layers.get(entry.id).data.features.find(f=>f.geometry?.type==='Point'&&f.properties.site_type==='CAMPGROUND');
   explore.showDetail(entry,f);window.__a11PinId=f.id||f.properties.id;
  })()`);await assertSelection('A11 exact place/site pin');
  assert.equal(await evaluate('(()=>{const e=document.querySelector(".leaflet-marker-icon.is-selected");return e?.dataset.featureId===window.__a11PinId&&e.getAttribute("aria-pressed")==="true"})()'),true,'A11 pin selected class and aria');
  assert.ok(await evaluate('[...explore.$("detail-body").firstElementChild.querySelectorAll("button")].some(e=>e.dataset.save||e.textContent==="Save to plan"||e.textContent==="Remove from saved")'),'A11 save action immediately under title/status');
  assert.ok((await evaluate('explore.$("detail-body").firstElementChild.textContent')).includes('Saving a place does not confirm it is suitable or available.'));
  if(width>=768)assert.equal(await evaluate('explore.$("sheet").getBoundingClientRect().height'),height*.75,'A11 selection keeps full side panel');
  await evaluate('explore.$("detail-back").click()');await assertSelection('A11 Back clears pin',true);await evaluate('explore.sheet.setExpanded(false)');
  const prefix='/v2/regions/'+id+'/',json=async name=>JSON.parse(await readFile(resolve(root,'v2/regions',id,name)));
  const cases=[['manifest missing',u=>u.pathname===prefix+'region.json'?{status:404}:null,false],['manifest unparseable',u=>u.pathname===prefix+'region.json'?{body:'{'}:null,false],['contract version',async u=>u.pathname===prefix+'region.json'?{body:JSON.stringify({...await json('region.json'),contract_version:2})}:null,true],['region mismatch',async u=>{if(u.pathname!==prefix+'region.json')return null;const m=await json('region.json');m.region.id='other';return {body:JSON.stringify(m)};},true],['config missing',u=>u.pathname===prefix+'explore.json'?{status:404}:null,true],['config invalid',async u=>u.pathname===prefix+'explore.json'?{body:JSON.stringify({...await json('explore.json'),explore_version:2})}:null,true],['index missing',u=>u.pathname===prefix+'display/index.json'?{status:404}:null,true]];
  for(const [label,intercept,hasManifest] of cases){await navigate(origin+'/v2/?region='+id+'&view=map',intercept);assert.equal(await evaluate('explore.$("summary").textContent'),'Region not available','B8 '+label);assert.deepEqual(await evaluate('Object.keys(window.__handed)'),[],'B8 no data layers');if(hasManifest){await evaluate('explore.showSources()');assert.ok((await evaluate('explore.$("source-body").textContent')).includes(manifest.fact_coverage.public_access.statement));await key('Escape');}}
  const first=manifest.layers.find(x=>x.format==='feature_collection'&&index.artifacts.find(a=>a.layer_id===x.id).feature_count>0);
  for(const failure of ['missing','unparseable','wrong layer']){await navigate(origin+'/v2/?region='+id+'&view=map',u=>u.pathname==='/v2/'+first.display.path?failure==='missing'?{status:404}:failure==='unparseable'?{body:'{'}:{body:JSON.stringify({type:'FeatureCollection',layer_id:'other',features:[]})}:null);assert.equal(await evaluate(`explore.region.layers.get(${JSON.stringify(first.id)}).state`),'failed');assert.ok(await evaluate('explore.region.registry.some(x=>x.id!=='+JSON.stringify(first.id)+'&&explore.region.layers.get(x.id).state==="loaded")'));assert.ok((await evaluate('explore.$("drawer").textContent')).includes('Could not load'));
   current.intercept=undefined;await evaluate(`(()=>{const row=document.getElementById('layer-'+${JSON.stringify(first.id)}).closest('section');[...row.querySelectorAll('button')].find(x=>x.textContent==='Retry').click()})()`);await poll(`explore.region.layers.get(${JSON.stringify(first.id)}).state==='loaded'`,'B8 retry');}
  if(manifest.layers.some(x=>x.format==='place_list')){const list=manifest.layers.find(x=>x.format==='place_list');await navigate(origin+'/v2/?region='+id+'&view=map',u=>u.pathname==='/v2/'+list.path?{status:404}:null);assert.equal(await evaluate('explore.$("summary").textContent'),'Listings could not load');assert.equal(await evaluate('explore.state.defaultLayersLoaded'),true);}
  else{await navigate(origin+'/v2/?region='+id+'&view=map',async u=>{
   if(u.pathname===prefix+'region.json'){const m=await json('region.json');m.layers.push({id:'test_places',kind:'overnight_inventory',format:'place_list',path:'regions/'+id+'/missing-places.json',pointer:'',list_key:'places',source_ids:[],status_ref:null,max_age_hours:720,limitations:'Research only.'});return {body:JSON.stringify(m)};}
   if(u.pathname===prefix+'explore.json'){const c=await json('explore.json');c.layers.push({layer_id:'test_places',title:'Listings',order:999,default_on:true,min_zoom:null});return {body:JSON.stringify(c)};}
   if(u.pathname===prefix+'missing-places.json')return {status:404};return null;
  });assert.equal(await evaluate('explore.$("summary").textContent'),'Listings could not load');assert.equal(await evaluate('explore.state.defaultLayersLoaded'),true);}
  if(id==='douglas-co'){await navigate(origin+'/v2/?region='+id+'&view=map',async u=>{if(u.pathname!==prefix+'explore.json')return null;const c=await json('explore.json');c.capabilities.saved_list=false;return {body:JSON.stringify(c)};});assert.deepEqual(await evaluate('explore.capabilities.saved'),[],'B9 saved_list off');assert.equal(await evaluate('[...document.querySelectorAll("button")].some(x=>x.textContent==="Saved plan")'),false);await evaluate('(()=>{const e=explore.region.registry.find(x=>x.kind==="trails");explore.showDetail(e,explore.region.layers.get(e.id).data.features[0])})()');assert.equal(await evaluate('[...document.querySelectorAll("button")].some(x=>x.textContent==="Save to plan"||x.textContent==="Remove from saved")'),false);await key('Escape');}
  await navigate(origin+'/v2/?region='+id+'&view=map',u=>u.pathname==='/v2/vendor/leaflet.js'?{status:404}:null);assert.equal(await evaluate('explore.$("map").textContent'),'Map could not load');await evaluate('explore.showSources()');assert.ok((await evaluate('explore.$("source-body").textContent')).includes(manifest.fact_coverage.public_access.statement));await key('Escape');result.checks.push('B8');results.push(result);
 }
 return results;
 }finally{running=false;await pump;if(pumpError&&!signal.aborted)throw pumpError;}
}
