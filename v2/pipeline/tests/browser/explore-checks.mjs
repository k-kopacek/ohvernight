import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {resolve} from 'node:path';
import {setTimeout as delay} from 'node:timers/promises';

const INIT=`(()=>{
 let app,renderer;window.__rendered=[];window.__handed={};window.__visible={};
 window.__frameLine=(f,zoom=15)=>{
  let best;
  for(const line of f.geometry.type==='LineString'?[f.geometry.coordinates]:f.geometry.coordinates)for(let i=1;i<line.length;i++){
   const a=line[i-1],b=line[i],length=Math.hypot(b[0]-a[0],b[1]-a[1]);if(!best||length>best.length)best={length,a,b};
  }
  const item=window.__rendered.flatMap(g=>Object.values(g._layers)).find(l=>l.feature?.properties?.id===f.properties.id);
  item._map.setView([(best.a[1]+best.b[1])/2,(best.a[0]+best.b[0])/2],zoom,{animate:false});
 };
 window.__framePolygon=(f,zoom=15)=>{
  const item=window.__rendered.flatMap(g=>Object.values(g._layers)).find(l=>l.feature?.properties?.id===f.properties.id),map=item._map;
  const area=l=>{const b=l.getBounds(),a=map.latLngToContainerPoint(b.getNorthWest()),z=map.latLngToContainerPoint(b.getSouthEast());return Math.abs((a.x-z.x)*(a.y-z.y));};
  const others=window.__rendered.flatMap(g=>Object.values(g._layers)).filter(l=>l!==item&&l._map===map&&/Polygon$/.test(l.feature?.geometry?.type)&&area(l)<=area(item)&&app.region.registry.some(e=>window.__handed[e.id]?.includes(l.feature)));
  const contains=(p,g)=>{
   const inside=ring=>{let hit=false;for(let i=0,j=ring.length-1;i<ring.length;j=i++){const a=ring[j],b=ring[i];if((a[1]>p[1])!==(b[1]>p[1])&&p[0]<(b[0]-a[0])*(p[1]-a[1])/(b[1]-a[1])+a[0])hit=!hit;}return hit;};
   return (g.type==='Polygon'?[g.coordinates]:g.coordinates).some(rings=>inside(rings[0])&&!rings.slice(1).some(inside));
  };
  const polygons=f.geometry.type==='Polygon'?[f.geometry.coordinates]:f.geometry.coordinates;
  let best;
  for(const polygon of polygons){const ys=polygon[0].map(p=>p[1]),min=Math.min(...ys),max=Math.max(...ys);
   for(const fraction of [.125,.25,.375,.5,.625,.75,.875]){const y=min+(max-min)*fraction,xs=[];
    for(const ring of polygon)for(let i=0,j=ring.length-1;i<ring.length;j=i++){const a=ring[j],b=ring[i];if((a[1]>y)!==(b[1]>y))xs.push(a[0]+(y-a[1])*(b[0]-a[0])/(b[1]-a[1]));}
    xs.sort((a,b)=>a-b);for(let i=0;i+1<xs.length;i+=2)for(const t of [.5,.2,.8]){
     const x=xs[i]+t*(xs[i+1]-xs[i]),width=xs[i+1]-xs[i];
     if((!best||width>best.width)&&!others.some(l=>l.getBounds().contains([y,x])&&contains([x,y],l.feature.geometry)))best={width,x,y};
    }
   }
  }
  if(!best)throw Error('No unobscured polygon interior '+f.properties.id);
  map.setView([best.y,best.x],zoom,{animate:false});
 };
 window.__pointForFeature=(f,offset=0)=>{
  const item=window.__rendered.flatMap(g=>Object.values(g._layers)).find(l=>l.feature?.properties?.id===f.properties.id),map=item?._map;
  if(!map)throw Error('Feature not rendered '+f.properties.id);
  const project=p=>map.latLngToContainerPoint([p[1],p[0]]),g=f.geometry,c=g.coordinates,points=[];
  if(/LineString$/.test(g.type))for(const line of g.type==='LineString'?[c]:c)for(let i=1;i<line.length;i++)for(const t of [.25,.5,.75])for(const side of offset?[offset,-offset]:[0]){
   const a=project(line[i-1]),b=project(line[i]),d=Math.hypot(b.x-a.x,b.y-a.y)||1;
   points.push({x:a.x+(b.x-a.x)*t-(b.y-a.y)*side/d,y:a.y+(b.y-a.y)*t+(b.x-a.x)*side/d});
  }
  else if(/Polygon$/.test(g.type)){
   const rings=(g.type==='Polygon'?c:c.flat()).map(r=>r.map(project));
   const inside=(p,ring)=>{let hit=false;for(let i=0,j=ring.length-1;i<ring.length;j=i++){const a=ring[i],b=ring[j];if((a.y>p.y)!==(b.y>p.y)&&p.x<(b.x-a.x)*(p.y-a.y)/(b.y-a.y)+a.x)hit=!hit;}return hit;};
   for(let y=130;y<innerHeight-70;y+=24)for(let x=12;x<innerWidth-12;x+=24){const p={x,y};if(rings.reduce((hit,r)=>inside(p,r)?!hit:hit,false))points.push(p);}
  }else if(g.type==='Point')points.push(project(c));
  const area=l=>{const b=l.getBounds?.();if(!b)return 0;const a=map.latLngToContainerPoint(b.getNorthWest()),c=map.latLngToContainerPoint(b.getSouthEast());return Math.abs((c.x-a.x)*(c.y-a.y));};
  const others=window.__rendered.flatMap(g=>Object.values(g._layers)).filter(l=>l._map===map&&l.feature?.geometry&&l!==item&&app.region.registry.some(e=>window.__handed[e.id]?.includes(l.feature))).map(l=>{
   const h=l.feature.geometry,lc=h.coordinates,b=l.getBounds?.(),a=b?map.latLngToContainerPoint(b.getNorthWest()):project(lc),z=b?map.latLngToContainerPoint(b.getSouthEast()):a;
   const segments=[];if(/LineString$/.test(h.type))for(const line of h.type==='LineString'?[lc]:lc){let last;for(const coord of line){const p=project(coord);if(last)segments.push([last,p]);last=p;}}
   return {l,type:h.type,a,z,segments,area:area(l)};
  });
  const step=Math.max(1,Math.floor(points.length/256)),reasons=[];
  const labelBoxes=Object.values(map._layers).filter(l=>(l.feature?.properties?.id||l.featureId)!==f.properties.id).map(l=>l.getTooltip?.()?.getElement()?.getBoundingClientRect()).filter(r=>r?.width);
  for(let i=0;i<points.length;i+=step){const p=points[i];
   const e=document.elementFromPoint(p.x,p.y);if(p.y<120||!map.getContainer().contains(e)||e?.closest('.leaflet-control'))continue;
   if(labelBoxes.some(r=>p.x>=r.left&&p.x<=r.right&&p.y>=r.top&&p.y<=r.bottom)||e.closest('.leaflet-marker-icon'))continue;
   let obscured=false;
   for(const {l,type,a,z,segments,area:otherArea} of others){
    if(p.x<Math.min(a.x,z.x)-14||p.x>Math.max(a.x,z.x)+14||p.y<Math.min(a.y,z.y)-14||p.y>Math.max(a.y,z.y)+14)continue;
    if(/Polygon$/.test(type)){if(/Polygon$/.test(g.type)&&otherArea<=area(item)&&l._containsPoint(map.containerPointToLayerPoint(p))){obscured=true;break;}continue;}
    let distance=type==='Point'?Math.hypot(a.x-p.x,a.y-p.y):Infinity;
    for(const [a,z] of segments){const dx=z.x-a.x,dy=z.y-a.y,t=Math.max(0,Math.min(1,((p.x-a.x)*dx+(p.y-a.y)*dy)/(dx*dx+dy*dy||1)));distance=Math.min(distance,Math.hypot(p.x-a.x-t*dx,p.y-a.y-t*dy));}
    if(distance<=(/Polygon$/.test(g.type)||type==='Point'?14:Math.abs(offset)+1e-6)){obscured=true;reasons.push({id:l.feature.properties.id,distance});break;}
   }
   if(!obscured)return {x:p.x,y:p.y};
  }
  throw Error('No exposed geometry point '+f.properties.id+' '+JSON.stringify({points:points.slice(0,3),zoom:map.getZoom(),reasons:reasons.slice(0,3)}));
 };
 Object.defineProperty(window,'L',{configurable:true,get(){return renderer},set(value){renderer=value;const original=value.geoJSON;value.geoJSON=function(data,options){const result=original.call(this,data,options);window.__rendered.push(result);return result;}}});
 let adapter;Object.defineProperty(window,'ExploreMap',{configurable:true,get(){return adapter},set(value){adapter=value;for(const method of ['addLayer','setPins']){const original=value[method];value[method]=function(id,data,...args){window.__handed[id]=method==='addLayer'?data.features:data;window.__visible[id]=true;return original.call(this,id,data,...args);};}const original=value.setVisible;value.setVisible=function(id,value){window.__visible[id]=value;return original.call(this,id,value);};}});
 Object.defineProperty(window,'explore',{configurable:true,get(){return app},set(value){app=value;for(const name of ['mapUsable','defaultLayersLoaded']){let state=value.state[name];Object.defineProperty(value.state,name,{get(){return state},set(next){state=next;if(next)window['__'+name+'Resources']=performance.getEntriesByType('resource').map(x=>x.name);}});}}});
 try{localStorage.setItem('ohvernight-trip-v1',JSON.stringify({trip:{resort:'aspen',arrive:'2026-07-10',depart:'2026-07-12',vehicle:'passenger_car'},plan:{a:'difficult',b:'silverbar'}}));localStorage.setItem('ohvernight-douglas-plan-v1',JSON.stringify(['usfs-trail-8939494']));localStorage.setItem('ohvernight-douglas-plan-v1-notes','compatibility notes');localStorage.setItem('ohvernight-douglas-plan-v1-trip',JSON.stringify({start:'2026-09-25',end:'2026-09-26',activity:'hiking',vehicle:'Truck with trailer'}));}catch{}
})()`;
const AREA=`(()=>{let n=0,free=0;const m=explore.$('map');for(let y=2;y<innerHeight;y+=4)for(let x=2;x<innerWidth;x+=4){n++;const e=document.elementFromPoint(x,y);if(e&&m.contains(e)&&!e.closest('.leaflet-control'))free++;}return 100*free/n})()`;
const RECT=`e=>{const r=e.getBoundingClientRect();return {x:r.x,y:r.y,width:r.width,height:r.height}}`;
const visible=`e=>{const r=e.getBoundingClientRect();return r.width>0&&r.height>0&&getComputedStyle(e).visibility!=='hidden'&&!e.closest('dialog:not([open]),[hidden],[inert]')}`;
// Fixture lengths are used only to choose regression samples, never in the UI.
export function trailSamples(features,crossingIds){
 const length=f=>(f.geometry.type==='LineString'?[f.geometry.coordinates]:f.geometry.coordinates).reduce((sum,line)=>sum+line.slice(1).reduce((n,p,i)=>n+Math.hypot(p[0]-line[i][0],p[1]-line[i][1]),0),0);
 const ordered=[...features].sort((a,b)=>length(a)-length(b)||a.properties.id.localeCompare(b.properties.id));
 const ids=new Set([ordered[0].properties.id,ordered.at(-1).properties.id,...crossingIds]);
 const byId=[...features].sort((a,b)=>a.properties.id.localeCompare(b.properties.id));
 for(let i=0;ids.size<8&&i<8;i++)ids.add(byId[Math.floor(i*(byId.length-1)/7)].properties.id);
 for(const f of byId){if(ids.size>=8)break;ids.add(f.properties.id);}
 return [...ids].map(id=>features.find(f=>f.properties.id===id));
}
// Readiness must belong to the loaded destination document, not its forwarding page.
export function destinationLoaded(frame,url,loaded){return frame.url===url&&loaded.has(frame.loaderId);}
export async function runExploreChecks(client,origin,signal,root){
 let running=true,current={externalBlocked:0,responses:[],escaped:[],errors:[],consoleErrors:[]},pumpError;const loaded=new Set();
 const interception=async(method,params)=>{try{return await client.command(method,params);}catch(error){if(!error.message.includes('Invalid InterceptionId'))throw error;}};
 const evaluate=async expression=>{signal.throwIfAborted();if(pumpError)throw pumpError;const r=await client.command('Runtime.evaluate',{expression,awaitPromise:true,returnByValue:true});if(r.exceptionDetails)throw new Error(expression+' '+JSON.stringify(r.exceptionDetails));return r.result.value;};
 const pump=(async()=>{while(running){const e=client.events.shift();if(!e){await delay(5,undefined,{signal});continue;}
  if(e.method==='Fetch.requestPaused'){
   const {requestId,request}=e.params,url=new URL(request.url);
   if(url.origin!==origin){current.externalBlocked++;await interception('Fetch.failRequest',{requestId,errorReason:'BlockedByClient'});continue;}
   const replacement=await current.intercept?.(url);
   if(replacement)await interception('Fetch.fulfillRequest',{requestId,responseCode:replacement.status||200,responseHeaders:[{name:'Content-Type',value:'application/json'}],body:Buffer.from(replacement.body||'').toString('base64')});
   else await interception('Fetch.continueRequest',{requestId});
  }else if(e.method==='Page.lifecycleEvent'&&e.params.name==='load')loaded.add(e.params.loaderId);
  else if(e.method==='Network.responseReceived'&&current){const response=e.params.response;if(new URL(response.url).origin===origin)current.responses.push({url:response.url,status:response.status});else if(!response.url.startsWith('data:'))current.escaped.push(response.url);}
  else if(e.method==='Runtime.exceptionThrown'&&current)current.errors.push(e.params.exceptionDetails);
  else if(e.method==='Log.entryAdded'&&current&&e.params.entry.level==='error'&&!e.params.entry.text.includes('ERR_BLOCKED_BY_CLIENT'))current.consoleErrors.push(e.params.entry.text);
 }} )().catch(error=>{pumpError=error;});
 await client.command('Network.enable');await client.command('Network.setCacheDisabled',{cacheDisabled:true});await client.command('Runtime.enable');await client.command('Log.enable');await client.command('Page.enable');
 await client.command('Page.setLifecycleEventsEnabled',{enabled:true});
 await client.command('Fetch.enable',{patterns:[{urlPattern:'*',requestStage:'Request'}]});
 await client.command('Page.addScriptToEvaluateOnNewDocument',{source:INIT});
 await client.command('Emulation.setEmulatedMedia',{features:[{name:'prefers-reduced-motion',value:'reduce'}]});
 const poll=async(expression,label)=>{for(let i=0;i<600;i++){signal.throwIfAborted();if(await evaluate(expression))return;await delay(20,undefined,{signal});}throw new Error('Browser state did not settle: '+label+' '+JSON.stringify(await evaluate('window.explore?.state')));};
 const key=async key=>{const code=key===' '?'Space':key,windowsVirtualKeyCode={Escape:27,Tab:9,Enter:13,' ':32}[key],text=key==='Enter'?'\r':key===' '?' ':undefined;await client.command('Input.dispatchKeyEvent',{type:'keyDown',key,code,windowsVirtualKeyCode,...(text?{text}: {})});await client.command('Input.dispatchKeyEvent',{type:'keyUp',key,code,windowsVirtualKeyCode});};
 async function navigate(url,intercept){
  async function documentAt(destination){for(let i=0;i<600;i++){signal.throwIfAborted();if(pumpError)throw pumpError;const {frameTree}=await client.command('Page.getFrameTree');if(destinationLoaded(frameTree.frame,destination,loaded))return;await delay(20,undefined,{signal});}throw new Error('Destination document did not load: '+destination);}
  await client.command('Page.navigate',{url:'about:blank'});await documentAt('about:blank');current={url,responses:[],errors:[],consoleErrors:[],escaped:[],externalBlocked:0,intercept};
  await client.command('Page.navigate',{url});await documentAt(url.endsWith('/v2/regions/douglas-co/')?origin+'/v2/?region=douglas-co&view=map':url);
  await poll('!!window.explore&&(explore.state.defaultLayersLoaded||explore.state.error)','load');assert.deepEqual(current.errors,[],'uncaught browser errors');if(!intercept){assert.deepEqual(current.consoleErrors,[],'browser console errors');assert.ok(current.responses.every(x=>x.status<400),'same-origin request failed');}assert.deepEqual(current.escaped,[],'non-local request escaped blocking');return current;
 }
 const bytes=async urls=>{let count=0;const paths=new Set();for(const url of new Set(urls)){const u=new URL(url);if(u.origin!==origin)continue;let p=resolve(root,'.'+u.pathname);if(u.pathname.endsWith('/'))p=resolve(p,'index.html');if(!paths.has(p)){paths.add(p);count+=(await readFile(p)).length;}}return count;};
 async function drag(point,dx,dy){await client.command('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:[{x:point.x,y:point.y}]});for(let i=1;i<=5;i++)await client.command('Input.dispatchTouchEvent',{type:'touchMove',touchPoints:[{x:point.x+dx*i/5,y:point.y+dy*i/5}]});await client.command('Input.dispatchTouchEvent',{type:'touchEnd',touchPoints:[]});}
 async function mouseTap(point){await client.command('Input.dispatchMouseEvent',{type:'mousePressed',...point,button:'left',clickCount:1});await client.command('Input.dispatchMouseEvent',{type:'mouseReleased',...point,button:'left',clickCount:1});}
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
  await evaluate('explore.$("sheet-toggle").focus()');await key('Enter');assert.equal(await evaluate('explore.sheet.state'),width<768?'half':'expanded','A11 Enter opens sheet');
  await key(' ');assert.equal(await evaluate('explore.sheet.state'),width<768?'expanded':'collapsed','A11 Space cycles sheet');
  await evaluate('explore.sheet.setState("expanded")');await key('Escape');assert.equal(await evaluate('explore.sheet.state'), 'collapsed','A11 Escape collapses sheet');assert.equal(await evaluate('document.activeElement===explore.$("sheet-toggle")'),true,'A11 Escape restores handle focus');
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
   await evaluate('explore.drawer.open()');const drawerHandle=()=>evaluate('(()=>{const r=explore.$("drawer").querySelector(".explore-heading h1").getBoundingClientRect();return {x:r.x+20,y:r.y+12}})()');
   const hp=await drawerHandle(),peek=await evaluate('explore.$("drawer").getBoundingClientRect().height');
   await client.command('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:[hp]});
   for(let i=1;i<=3;i++){await delay(110,undefined,{signal});await client.command('Input.dispatchTouchEvent',{type:'touchMove',touchPoints:[{x:hp.x,y:hp.y-height*.24*i/3}]});const h=await evaluate('explore.$("drawer").getBoundingClientRect().height');assert.ok(h>peek&&h<height*.75,'A12 drawer slow drag follows finger before release');}
   await client.command('Input.dispatchTouchEvent',{type:'touchEnd',touchPoints:[]});assert.equal(await evaluate('explore.drawer.state'),'expanded','A12 drawer slow drag snaps expanded');
   await evaluate('explore.$("drawer").querySelector(".explore-drawer-body").scrollTop=120');const before=await evaluate('explore.$("drawer").querySelector(".explore-drawer-body").scrollTop');assert.ok(before>0,'A12 scrollable layer list fixture');
   const lp=await evaluate('(()=>{const r=explore.$("drawer").querySelector(".explore-drawer-body").getBoundingClientRect();return {x:r.x+2,y:r.y+40}})()');await drag(lp,0,35);assert.equal(await evaluate('explore.drawer.state'),'expanded','A12 layer list scroll does not drag drawer');assert.ok(await evaluate('explore.$("drawer").querySelector(".explore-drawer-body").scrollTop')<before,'A12 layer list scrolls independently');
   await flick(await drawerHandle(),60);assert.equal(await evaluate('explore.drawer.state'),'peek','A12 drawer downward flick collapses expanded to peek');
   await flick(await drawerHandle(),-60);assert.equal(await evaluate('explore.drawer.state'),'expanded','A12 drawer upward flick expands');
   await flick(await drawerHandle(),60);await flick(await drawerHandle(),60);assert.equal(await evaluate('explore.$("drawer").hidden'),true,'A11/A12 drawer downward swipe dismisses after collapse');
   assert.equal(await evaluate('document.activeElement===explore.$("layers")'),true,'A12 drawer swipe focus returns');

  }
  if(width>=768){
   await evaluate('explore.sheet.setState("collapsed")');const center=await evaluate('explore.state.view.center');
   const handle=()=>evaluate('(()=>{const r=explore.$("sheet-toggle").getBoundingClientRect();return {x:r.x+r.width/2,y:r.y+24}})()');
   for(const [dy,state] of [[-60,'half'],[-60,'expanded'],[60,'half'],[60,'collapsed']]){await flick(await handle(),dy);assert.equal(await evaluate('explore.sheet.state'),state,'A12 tablet native flick snap');}
   const p=await handle();await client.command('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:[p]});
   await delay(110,undefined,{signal});await client.command('Input.dispatchTouchEvent',{type:'touchMove',touchPoints:[{x:p.x,y:p.y-height*.15}]});
   const intermediate=await evaluate('explore.$("sheet").getBoundingClientRect().height');assert.ok(intermediate>64&&intermediate<height*.4,'A12 tablet follows finger before release');
   await delay(110,undefined,{signal});await client.command('Input.dispatchTouchEvent',{type:'touchMove',touchPoints:[{x:p.x,y:p.y-height*.3}]});
   await client.command('Input.dispatchTouchEvent',{type:'touchEnd',touchPoints:[]});assert.equal(await evaluate('explore.sheet.state'),'half','A12 tablet slow drag snaps partial');
   assert.deepEqual(await evaluate('explore.state.view.center'),center,'A12 tablet sheet never pans map');await evaluate('explore.sheet.setState("collapsed")');
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
   if(!filtered.length)throw Error('A11 filtered list disappeared');window.__a11Count=filtered.length;const trail=explore.region.registry.find(e=>e.kind==='trails');document.getElementById('layer-'+trail.id).click();if(window.__visible[trail.id]!==false)throw Error('A12 hidden trail fixture');filtered[0].click();
  })()`);
  await assertSelection('A11 selected search result');assert.equal(await evaluate(`(()=>{const id=explore.state.selection.layerId,row=document.getElementById('layer-'+id).closest('[data-layer-id]');return window.__visible[id]&&row.querySelector('input').checked&&row.querySelector('.explore-layer-mode').textContent==='On'})()`),true,'A12 selection restores map, checkbox and On label');
  assert.equal(await evaluate('!explore.$("detail-view").hidden&&explore.$("list-view").hidden&&!document.querySelector("dialog[open]")'),true,'A11 selection opens sheet detail');
  await evaluate('explore.$("detail-back").click()');await assertSelection('A11 Back clears result',true);
  assert.equal(await evaluate('window.__a11List.parentElement===explore.$("list-view")&&!window.__a11List.hidden&&window.__a11Query.value===window.__a11Value'),true,'A11 Back preserves list and filter');
  assert.equal(await evaluate('[...window.__a11List.querySelectorAll("button")].filter(e=>e.classList.contains("explore-result")||e.parentElement===explore.$("search-results")).length'),await evaluate('window.__a11Count'),'A11 filtered results persist');
  await evaluate(`(()=>{window.__a11Query.value='';window.__a11Query.dispatchEvent(new Event('input',{bubbles:true}));explore.$('sheet-body').scrollTop=120;window.__a11Scroll=explore.$('sheet-body').scrollTop;const result=[...window.__a11List.querySelectorAll('button')].find(e=>e.classList.contains('explore-result')||e.parentElement===explore.$('search-results'));result.click();explore.$('detail-back').click()})()`);
  assert.ok(await evaluate('window.__a11Scroll')>0,'A11 scrolling list fixture');assert.equal(await evaluate('explore.$("sheet-body").scrollTop'),await evaluate('window.__a11Scroll'),'A11 Back restores practical list scroll');
  if(id==='aspen'){
   await evaluate(`(()=>{explore.$('search-back').click();explore.sheet.setState('expanded');const panel=explore.$('list-body').querySelector('.explore-filters');panel.open=true;[...panel.querySelectorAll('button')].find(e=>e.textContent==='Campgrounds').click();window.__a11Planner=explore.$('list-body');window.__a11PlannerCount=window.__a11Planner.querySelectorAll('.explore-result').length;window.__a11Planner.querySelector('.explore-result').click();explore.$('detail-back').click()})()`);
   assert.equal(await evaluate('!window.__a11Planner.hidden&&window.__a11Planner.querySelector(".explore-filters").open'),true,'A11 planner list and filter panel persist');
   assert.equal(await evaluate('[...window.__a11Planner.querySelectorAll("button")].find(e=>e.textContent==="Campgrounds").getAttribute("aria-pressed")'),'true','A11 planner filter stays selected');assert.equal(await evaluate('window.__a11Planner.querySelectorAll(".explore-result").length'),await evaluate('window.__a11PlannerCount'),'A11 planner filtered list persists');
  }
  await key('Escape');
  async function checkTargets(){const small=await evaluate(`[...document.querySelectorAll('button,input,select,textarea,summary,[role=button],a')].filter(${visible}).filter(e=>!e.closest('.leaflet-control-attribution')&&!(e.tagName==='A'&&e.closest('p')&&e.parentElement.childNodes.length>1)).filter(e=>{const r=e.getBoundingClientRect();return r.width<44||r.height<44}).map(e=>e.id||e.textContent)`);assert.deepEqual(small,[],'B2 overlay target size');}
  const overlays=await evaluate('[...document.querySelectorAll("dialog")].length');for(let i=0;i<overlays;i++){await evaluate(`(()=>{const d=document.querySelectorAll('dialog')[${i}];explore.openDialog(d);return d.open})()`);await checkTargets();await key('Escape');}
  await evaluate('explore.drawer.close();explore.sheet.setExpanded(false)');assert.ok(await evaluate(AREA)>=(width===1440?90:minimum),'B6 restored map '+JSON.stringify(await evaluate('({free:'+AREA+',open:[...document.querySelectorAll("dialog[open]")].map(x=>x.id),drawer:explore.$("drawer").hidden})') ));result.checks.push('B6');
  const manifest=JSON.parse(await readFile(resolve(root,'v2/regions',id,'region.json'))),index=JSON.parse(await readFile(resolve(root,'v2/regions',id,'display/index.json')));
  const rowRecords=await evaluate(`[...explore.$('layer-list').children].map(row=>({id:row.dataset.layerId,title:row.querySelector('label span').textContent,source:row.querySelector('.explore-layer-source').textContent,limitation:row.querySelector('.explore-layer-limitation').textContent,state:row.querySelector('.explore-layer-mode').textContent,checked:row.querySelector('input').checked,status:row.querySelector('.explore-layer-state').textContent}))`);
  for(const row of rowRecords){const declaration=manifest.layers.find(e=>e.id===row.id),config=await evaluate('explore.region.registry.find(e=>e.id==='+JSON.stringify(row.id)+').title');assert.equal(row.title,config,'A12 approved layer title');assert.equal(row.limitation,declaration.limitations,'A12 verbatim row limitation');assert.equal(row.source,'Source: '+[...new Set(declaration.source_ids.map(id=>manifest.sources[id].agency))].join(' · '),'A12 approved source agencies');assert.equal(row.state,row.checked?'On':'Off','A12 explicit on/off state');assert.match(row.status,/loaded|Could not load|No features|Loading/,'A12 current load status');}
  const rowToggle=rowRecords.find(e=>e.checked),stateSelector='[data-layer-id="'+rowToggle.id+'"] .explore-layer-mode';
  await evaluate('document.getElementById('+JSON.stringify('layer-'+rowToggle.id)+').click()');assert.equal(await evaluate('document.querySelector('+JSON.stringify(stateSelector)+').textContent'),'Off','A12 row state updates immediately');await evaluate('document.getElementById('+JSON.stringify('layer-'+rowToggle.id)+').click()');assert.equal(await evaluate('document.querySelector('+JSON.stringify(stateSelector)+').textContent'),'On','A12 row state restores');result.a12LayerRows=rowRecords;
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
   if(!item)throw Error('A11 trail renderer item absent');explore.select(entry,f);explore.$('detail-back').click();explore.sheet.setState('collapsed');
  })()`);
  await evaluate('__frameLine(window.__a11Trail)');await mouseTap(await evaluate('__pointForFeature(window.__a11Trail)'));
  assert.equal(await evaluate('explore.state.selection.featureId===window.__a11Trail.properties.id&&!explore.$("detail-view").hidden'),true,'A11 trail tap selects and opens detail');await assertSelection('A11 exact trail tap');
  assert.equal(await evaluate(`(()=>{const b=ExploreShell.bounds({features:[window.__a11Trail]}),v=explore.state.view.bounds;return v[0][0]<=b[0][0]&&v[0][1]<=b[0][1]&&v[1][0]>=b[1][0]&&v[1][1]>=b[1][1]})()`),true,'A11 full trail bounds fitted');
  const trailText=await evaluate('explore.$("detail-view").textContent'),trailFields=await evaluate('window.__a11Trail.properties');
  for(const value of [trailFields.name,trailFields.trail_number,trailFields.surface,trailFields.allowed_terra_use].filter(Boolean))assert.ok(trailText.includes(value),'A11 carried trail field');
  assert.ok(trailText.includes('Source fetched '+trailFields.evidence.retrieved_at.slice(0,10)));
  assert.ok(trailText.includes(manifest.layers.find(e=>e.kind==='trails').limitations),'A11 trail limitation');assert.doesNotMatch(trailText,/\blength\b|elevation gain/i,'A11 no fabricated trail measures');
  await evaluate('explore.$("detail-back").click()');
  const landTexts=await evaluate(`(()=>{const entry=explore.region.registry.find(e=>e.kind==='land_management'),f=explore.region.layers.get(entry.id).data.features[0];window.__a11Land=f;window.__a11LandId=f.properties.id;explore.select(entry,f);explore.$('detail-back').click();explore.sheet.setState('collapsed');__framePolygon(f);return ExploreLand.detail(explore.manifest,explore.manifest.layers.find(e=>e.id===entry.id),f).items.map(x=>x.text)})()`);
  await mouseTap(await evaluate('__pointForFeature(window.__a11Land)'));
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
  if(width<768){assert.equal(await evaluate(`(()=>{const button=[...explore.$('detail-body').firstElementChild.querySelectorAll('button')].find(e=>e.dataset.save||e.textContent==='Save to plan'||e.textContent==='Remove from saved'),r=button.getBoundingClientRect();return r.top>=explore.$('sheet').getBoundingClientRect().top&&r.bottom<=innerHeight})()`),true,'A11 save control visible in half sheet');}
  assert.equal(await evaluate('document.querySelector(".leaflet-marker-icon.is-selected").getBoundingClientRect().width'),44,'A11 lighter pin retains 44px target');assert.equal(await evaluate('document.querySelector(".leaflet-marker-icon.is-selected .pin-badge").getBoundingClientRect().width'),28,'A11 lighter pin badge');
  await evaluate('window.__assistivePin=document.querySelector(".leaflet-marker-icon.is-selected");explore.$("detail-back").click();window.__assistivePin.click()');
  assert.equal(await evaluate('explore.state.selection?.featureId'),await evaluate('window.__a11PinId'),'R3 programmatic zero-coordinate pin activation');await assertSelection('R3 assistive pin highlight');

  await evaluate('explore.$("detail-back").click()');const pinPoint=await evaluate('(()=>{const e=window.__assistivePin,r=e.getBoundingClientRect();return {x:r.x+r.width/2,y:r.y+r.height/2}})()');await tap(pinPoint);await poll('explore.state.selection?.featureId===window.__a11PinId','A12 native pin selection');await assertSelection('A12 native pin same ID');
  if(width>=768){assert.equal(await evaluate('explore.sheet.state'),'half','A12 selection opens tablet partial state (supersedes K3)');assert.ok(Math.abs(await evaluate('explore.$("sheet").getBoundingClientRect().height')-height*.4)<=1/64,'A12 partial side panel uses 40% height, within CSS pixel quantization');}
  await evaluate('explore.$("detail-back").click()');await assertSelection('A11 Back clears pin',true);await evaluate('explore.sheet.setExpanded(false)');
  await evaluate(`(()=>{const entry=explore.region.registry.find(e=>e.kind==='trails'),f=explore.region.layers.get(entry.id).data.features.filter(f=>f.properties.name&&f.geometry).sort((a,b)=>{const size=f=>{const b=ExploreShell.bounds({features:[f]});return (b[1][0]-b[0][0])*(b[1][1]-b[0][1])};return size(a)-size(b)})[0];window.__a11LabelFeature=f;window.__a11LabelEntry=entry;explore.select(entry,f);explore.$('detail-back').click();explore.sheet.setExpanded(false);while(explore.state.view.zoom>13)explore.$('zoom-out').click()})()`);
  assert.equal(await evaluate('document.querySelectorAll(".explore-map-label").length'),0,'A11 no names below label zoom');
  await evaluate('explore.$("zoom-in").click()');
  const labels=await evaluate('[...document.querySelectorAll(".explore-map-label")].map(e=>({text:e.textContent,interactive:getComputedStyle(e).pointerEvents,box:((r)=>[r.left,r.top,r.right,r.bottom])(e.getBoundingClientRect())}))');
  assert.ok(labels.length>0&&labels.length<=32,'A11 capped names at zoom 14');
  const names=await evaluate('[...Object.values(window.__handed)].flat().map(f=>f.properties?.name||f.name).filter(Boolean)');
  for(const label of labels){assert.ok(names.includes(label.text),'A11 only carried names');assert.equal(label.interactive,'none','A11 labels never block taps');}
  for(let a=0;a<labels.length;a++)for(let b=a+1;b<labels.length;b++){const x=labels[a].box,y=labels[b].box;assert.ok(x[2]<=y[0]||y[2]<=x[0]||x[3]<=y[1]||y[3]<=x[1],'A11 names do not crowd each other');}result.labelsAt14=labels.map(l=>l.text);
  await evaluate('__frameLine(window.__a11LabelFeature,18)');
  const labelFixture=await evaluate(`(()=>{
   const item=window.__rendered.flatMap(g=>Object.values(g._layers)).find(l=>{
    const r=l.getTooltip?.()?.getElement()?.getBoundingClientRect();if(!r?.width||!l.feature?.geometry||!window.__handed[explore.region.registry.find(e=>e.kind==='trails').id].includes(l.feature))return false;
    const e=document.elementFromPoint(r.x+r.width/2,r.y+r.height/2);return l._map.getContainer().contains(e)&&!e.closest('.leaflet-control');
   });
   if(!item)throw Error('A12 no visible trail label');window.__a12LabelFeature=item.feature;window.__a12LabelMap=item._map;window.__a12LabelView={center:item._map.getCenter(),zoom:item._map.getZoom()};
   const r=item.getTooltip().getElement().getBoundingClientRect();return {id:item.feature.properties.id,point:{x:r.x+r.width/2,y:r.y+r.height/2}};
  })()`);
  await mouseTap(labelFixture.point);assert.equal(await evaluate('explore.state.selection.featureId'),labelFixture.id,'A12 visible label selects its feature');await assertSelection('A12 label highlight');
  await evaluate('explore.$("detail-back").click();explore.sheet.setState("collapsed");window.__a12LabelMap.setView(window.__a12LabelView.center,window.__a12LabelView.zoom,{animate:false});void 0');
  await mouseTap(await evaluate('__pointForFeature(window.__a12LabelFeature)'));assert.equal(await evaluate('explore.state.selection.featureId'),labelFixture.id,'A12 geometry and label resolve to the same ID');
  await evaluate('explore.$("detail-back").click();explore.sheet.setState("collapsed")');
  async function tap(point){await client.command('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:[point]});await client.command('Input.dispatchTouchEvent',{type:'touchEnd',touchPoints:[]});}
  await evaluate('window.__a12LabelMap.setView(window.__a12LabelView.center,window.__a12LabelView.zoom,{animate:false});void 0');
  const nativeLabelPoint=await evaluate(`(()=>{const item=window.__rendered.flatMap(g=>Object.values(g._layers)).find(l=>l.feature===window.__a12LabelFeature),r=item.getTooltip().getElement().getBoundingClientRect();return {x:r.x+r.width/2,y:r.y+r.height/2}})()`);await tap(nativeLabelPoint);await poll('explore.state.selection?.featureId==='+JSON.stringify(labelFixture.id),'A12 native label ID');await assertSelection('A12 native label same feature');await evaluate('explore.$("detail-back").click();explore.sheet.setState("collapsed")');
  const trailArtifact=index.artifacts.find(a=>a.layer_id===manifest.layers.find(e=>e.kind==='trails').id),trailDoc=JSON.parse(await readFile(resolve(root,'v2',trailArtifact.path)));
  const sampleIds=trailSamples(trailDoc.features,id==='aspen'?['usfs-trail-8919662','usfs-trail-8928063']:['usfs-trail-8913499','usfs-trail-8964041']).map(f=>f.properties.id);
  result.a12Trails=[];
  for(const featureId of sampleIds){
   for(const offset of [0,6]){
    await evaluate(`(()=>{const entry=explore.region.registry.find(e=>e.kind==='trails');window.__a12Trail=explore.region.layers.get(entry.id).data.features.find(f=>f.properties.id===${JSON.stringify(featureId)});explore.sheet.setState('collapsed');__frameLine(window.__a12Trail,18)})()`);
    await tap(await evaluate('__pointForFeature(window.__a12Trail,'+offset+')'));
    await poll('explore.state.selection?.featureId==='+JSON.stringify(featureId),'A12 real trail '+featureId+' offset '+offset);
    await assertSelection('A12 real trail '+featureId+' offset '+offset);assert.equal(await evaluate('!explore.$("detail-view").hidden'),true,'A12 trail opens detail');
    await evaluate('explore.$("detail-back").click();explore.sheet.setState("collapsed")');
   }
   result.a12Trails.push({featureId,onLine:true,besideLinePx:6});
  }
  await evaluate(`(()=>{const e=explore.region.registry.find(e=>e.kind==='trails');window.__safariFeature=explore.region.layers.get(e.id).data.features.find(f=>f.properties.id===${JSON.stringify(sampleIds[0])});__frameLine(window.__safariFeature,18)})()`);
  const safariPoint=await evaluate('__pointForFeature(window.__safariFeature)');await tap(safariPoint);
  await evaluate(`(()=>{const e=document.elementFromPoint(${safariPoint.x},${safariPoint.y});e.dispatchEvent(new MouseEvent('click',{bubbles:true,clientX:${Math.round(safariPoint.x)},clientY:${Math.round(safariPoint.y)}}))})()`);
  assert.equal(await evaluate('explore.state.selection'),null,'R2 Safari plain compatibility click remains deferred');
  await poll('explore.state.selection?.featureId==='+JSON.stringify(sampleIds[0]),'R2 plain click uses fractional touch position');await assertSelection('R2 Safari-compatible touch selection');
  await evaluate('explore.$("detail-back").click();explore.sheet.setState("collapsed")');
  if(id==='douglas-co'){
   for(const featureId of ['usfs-trail-8925194','usfs-trail-8952194']){
    await evaluate(`(()=>{explore.$('search').click();const activity=document.getElementById('activity'),query=document.getElementById('query');activity.value='';activity.dispatchEvent(new Event('input'));const e=explore.region.registry.find(e=>e.kind==='trails'),f=explore.region.layers.get(e.id).data.features.find(f=>f.properties.id===${JSON.stringify(featureId)});window.__overlapFeature=f;query.value=f.properties.name;query.dispatchEvent(new Event('input'));document.querySelector('[data-feature="'+f.properties.id+'"]').click()})()`);
    assert.equal(await evaluate('explore.state.selection?.featureId'),featureId,'A12 coincident source trail reachable through search');await assertSelection('A12 shadowed own ID');
    assert.equal(await evaluate('explore.$("detail-title").textContent'),await evaluate('window.__overlapFeature.properties.name'),'A12 shadowed own detail');
    assert.equal(await evaluate(`(()=>{const b=ExploreShell.bounds({features:[window.__overlapFeature]}),v=explore.state.view.bounds;return v[0][0]<=b[0][0]&&v[0][1]<=b[0][1]&&v[1][0]>=b[1][0]&&v[1][1]>=b[1][1]})()`),true,'A12 shadowed own geometry fit');
    await evaluate('explore.$("detail-back").click();explore.sheet.setState("collapsed")');
   }
   let previous;
   for(let i=0;i<2;i++){
    const p=await evaluate(`(()=>{const e=explore.region.registry.find(e=>e.kind==='trails'),f=explore.region.layers.get(e.id).data.features.find(f=>f.properties.id==='usfs-trail-8925194');__frameLine(f,18);const item=window.__rendered.flatMap(g=>Object.values(g._layers)).find(l=>l.feature===f);const r=item._map.getContainer().getBoundingClientRect();return {x:r.x+r.width/2,y:r.y+r.height/2}})()`);
    await tap(p);await poll('!!explore.state.selection','A12 coincident geometry tap');const selected=await evaluate('explore.state.selection.featureId');if(previous)assert.equal(selected,previous,'A12 coincident geometry deterministic single hit');previous=selected;await assertSelection('A12 coincident single highlight');await evaluate('explore.$("detail-back").click();explore.sheet.setState("collapsed")');
   }
  }
  result.a12LandModes=[];
  for(const mode of ['plain','search','trail detail','after drawer']){
   await evaluate(`(()=>{if(!explore.$('detail-view').hidden)explore.$('detail-back').click();if(${JSON.stringify(mode)}==='plain')explore.sheet.setState('collapsed');if(${JSON.stringify(mode)}==='search')explore.$('search').click();if(${JSON.stringify(mode)}==='trail detail')explore.select(window.__a11TrailEntry,window.__a11Trail);if(${JSON.stringify(mode)}==='after drawer'){explore.drawer.open();explore.drawer.close();}__framePolygon(window.__a11Land)})()`);
   const list=await evaluate('(()=>{const n=[...explore.$("list-view").children].find(n=>!n.hidden);return {index:[...explore.$("list-view").children].indexOf(n),query:n.querySelector("#query,#explore-query")?.value}})()');
   await tap(await evaluate('__pointForFeature(window.__a11Land)'));await poll('explore.state.selection?.featureId===window.__a11LandId','A12 land '+mode);
   await assertSelection('A12 land '+mode);assert.equal(await evaluate('explore.sheet.state'),'half','A12 land partial state on phones and tablets');
   assert.deepEqual(await evaluate('[...explore.$("detail-body").querySelectorAll("p,a")].slice(0,'+landTexts.length+').map(e=>e.textContent)'),landTexts,'A12 land exact wording '+mode);
   await evaluate('explore.$("detail-back").click()');assert.equal(await evaluate('explore.$("list-view").children['+list.index+'].hidden'),false,'A12 Back restores list '+mode);
   if(list.query!==undefined)assert.equal(await evaluate('explore.$("list-view").children['+list.index+'].querySelector("#query,#explore-query").value'),list.query,'A12 Back keeps filters '+mode);
   result.a12LandModes.push({mode,featureId:await evaluate('window.__a11LandId')});
  }
  await evaluate('explore.sheet.setState("collapsed")');
  const water=await evaluate(`(()=>{const entry=explore.region.registry.find(e=>e.kind==='water'&&explore.region.layers.get(e.id).data?.features.some(f=>f.properties.name&&f.geometry)),f=explore.region.layers.get(entry.id).data.features.find(f=>f.properties.name&&f.geometry);window.__a12Water=f;window.__a12WaterEntry=entry;if(/Polygon$/.test(f.geometry.type))__framePolygon(f);else __frameLine(f,18);return {id:f.properties.id,output:ExploreEvidence.feature(explore.manifest,explore.manifest.layers.find(e=>e.id===entry.id),f,entry.title,Date.now())}})()`);
  await tap(await evaluate('__pointForFeature(window.__a12Water)'));await poll('explore.state.selection?.featureId==='+JSON.stringify(water.id),'A12 named water');
  assert.equal(await evaluate('explore.$("detail-title").textContent'),water.output.title,'A12 water source name');
  assert.deepEqual(await evaluate('[...explore.$("detail-body").querySelectorAll("p")].map(e=>e.textContent)'),water.output.lines,'A12 water generic source-backed lines only');
  assert.deepEqual(await evaluate('[...explore.$("detail-body").querySelectorAll("a")].map(e=>({label:e.textContent,url:e.href}))'),water.output.links,'A12 water source links only');
  result.a12Water=water.id;await evaluate('explore.$("detail-back").click();explore.sheet.setState("collapsed")');
  result.a12LandFeatures=[];
  const landIds=await evaluate('explore.region.layers.get(explore.region.registry.find(e=>e.kind==="land_management").id).data.features.filter(f=>f.geometry).map(f=>f.properties.id)');
  for(const featureId of landIds){
   const wording=await evaluate(`(()=>{const e=explore.region.registry.find(e=>e.kind==='land_management'),f=explore.region.layers.get(e.id).data.features.find(f=>f.properties.id===${JSON.stringify(featureId)});window.__a12Land=f;__framePolygon(f,18);return ExploreLand.detail(explore.manifest,explore.manifest.layers.find(d=>d.id===e.id),f).items.map(x=>x.text)})()`);
   await tap(await evaluate('__pointForFeature(window.__a12Land)'));await poll('explore.state.selection?.featureId==='+JSON.stringify(featureId),'A12 land feature '+featureId);await assertSelection('A12 land feature '+featureId);
   assert.deepEqual(await evaluate('[...explore.$("detail-body").querySelectorAll("p,a")].slice(0,'+wording.length+').map(e=>e.textContent)'),wording,'A12 every land feature exact wording');
   await evaluate('explore.$("detail-back").click();explore.sheet.setState("collapsed")');result.a12LandFeatures.push(featureId);
  }
  result.checks.push('A12 real trails, land mode independence, Back, label identity and generic water');
  if(width<768){
   const nativeFeaturePoint=await evaluate(`(()=>{explore.select(window.__a11LabelEntry,window.__a11LabelFeature);explore.$('detail-back').click();explore.drawer.open();return __pointForFeature(window.__a11LabelFeature)})()`);
   await tap(nativeFeaturePoint);await poll('explore.state.selection?.featureId===window.__a11LabelFeature.properties.id','A11 native feature with drawer');assert.equal(await evaluate('explore.$("drawer").hidden'),true,'A11 feature tap dismisses drawer without swallowing selection');await assertSelection('A11 native feature with drawer');await evaluate('explore.$("detail-back").click()');
  }
  await evaluate('explore.sheet.setExpanded(false)');
  const doublePoint={x:Math.round(width*.65),y:Math.round(height*.25)},beforeDouble=await evaluate('explore.state.view.zoom');
  await tap(doublePoint);await tap(doublePoint);await poll('explore.state.view.zoom>'+beforeDouble,'A11 native double-tap zoom');assert.equal(await evaluate('visualViewport.scale'),1,'A11 native double-tap preserves page scale');
  await evaluate('explore.sheet.setExpanded(false)');const mouseZoom=await evaluate('explore.state.view.zoom');for(const [type,count] of [['mousePressed',1],['mouseReleased',1],['mousePressed',2],['mouseReleased',2]])await client.command('Input.dispatchMouseEvent',{type,x:doublePoint.x,y:doublePoint.y,button:'left',clickCount:count});await poll('explore.state.view.zoom>'+mouseZoom,'A11 double-click zoom');
  await evaluate(`(()=>{if(!explore.$('detail-view').hidden)explore.$('detail-back').click();explore.sheet.setState('collapsed');__framePolygon(window.__a11Land);window.__blockCompatibilityClicks=true;window.addEventListener('click',e=>{if(window.__blockCompatibilityClicks&&explore.$('map').contains(e.target))e.stopImmediatePropagation();},true);void 0})()`);
  const sourcePoint=await evaluate('__pointForFeature(window.__a11Land)'),sourceZoom=await evaluate('explore.state.view.zoom');
  await tap(sourcePoint);await delay(220,undefined,{signal});await tap(sourcePoint);await poll('explore.state.view.zoom==='+Math.min(19,sourceZoom+1),'A12 touchend double-tap beyond Leaflet click window');
  await delay(330,undefined,{signal});assert.equal(await evaluate('explore.state.selection'),null,'A12 double-tap over a selectable polygon never selects');assert.equal(await evaluate('explore.$("detail-view").hidden'),true,'A12 double-tap does not open detail');assert.equal(await evaluate('visualViewport.scale'),1,'A12 click-free touch double-tap preserves page scale');
  for(let i=0;i<2;i++){
   await evaluate('__framePolygon(window.__a11Land)');await tap(await evaluate('__pointForFeature(window.__a11Land)'));await poll('explore.state.selection?.featureId===window.__a11LandId','A12 slow single tap without compatibility click');await assertSelection('A12 click-free single tap');await evaluate('explore.$("detail-back").click();explore.sheet.setState("collapsed")');await delay(330,undefined,{signal});
  }
  await evaluate('__framePolygon(window.__a11Land)');const panPoint=await evaluate('__pointForFeature(window.__a11Land)');const beforePan=await evaluate('explore.state.view.center');await drag(panPoint,35,25);await poll('JSON.stringify(explore.state.view.center)!=='+JSON.stringify(JSON.stringify(beforePan)),'A12 pan still works after double-tap');await delay(330,undefined,{signal});assert.equal(await evaluate('explore.state.selection'),null,'A12 native pan never selects');
  const pinchCenter={x:Math.round(width*.65),y:Math.round(height*.35)},pinchZoom=await evaluate('explore.state.view.zoom'),pinch=[{x:pinchCenter.x-20,y:pinchCenter.y},{x:pinchCenter.x+20,y:pinchCenter.y}];await client.command('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:pinch});await client.command('Input.dispatchTouchEvent',{type:'touchMove',touchPoints:pinch.map((p,i)=>({...p,x:p.x+(i?30:-30)}))});await client.command('Input.dispatchTouchEvent',{type:'touchEnd',touchPoints:[]});await delay(330,undefined,{signal});await poll('explore.state.view.zoom>'+pinchZoom,'A12 native pinch changes map zoom');assert.equal(await evaluate('explore.state.selection'),null,'A12 native pinch never selects');assert.equal(await evaluate('visualViewport.scale'),1,'A12 native pinch zooms map, not page');
  await evaluate('window.__blockCompatibilityClicks=false');result.checks.push('A12 touchend double-tap, click-free single selection, pan/pinch without selection');
  const zoomBefore=await evaluate('explore.state.view.zoom');
  const zoomPoint=async name=>evaluate('(()=>{const r=explore.$('+JSON.stringify(name)+').getBoundingClientRect();return {x:r.x+r.width/2,y:r.y+r.height/2}})()');
  for(let i=0;i<3;i++)await tap(await zoomPoint('zoom-in'));const afterPlus=await evaluate('explore.state.view.zoom');assert.ok(afterPlus>zoomBefore,'A11 native rapid plus zooms map');assert.equal(afterPlus,Math.min(19,zoomBefore+3),'A11 every rapid plus activation applies');assert.equal(await evaluate('visualViewport.scale'),1,'A11 rapid plus never zooms page');
  for(let i=0;i<3;i++)await tap(await zoomPoint('zoom-out'));const afterMinus=await evaluate('explore.state.view.zoom');assert.ok(afterMinus<=zoomBefore,'A11 native rapid minus zooms map');assert.equal(afterMinus,Math.max(5,afterPlus-3),'A11 every rapid minus activation applies');assert.equal(await evaluate('visualViewport.scale'),1,'A11 rapid minus never zooms page');
  if(width<768){
   await client.command('Emulation.setDeviceMetricsOverride',{width:height,height:width,deviceScaleFactor:2,mobile:true});
   await poll('innerWidth==='+height+'&&innerHeight==='+width,'A11 landscape viewport');await evaluate('new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve)))');
   assert.equal(await evaluate('document.documentElement.scrollWidth>innerWidth'),false,'A11 landscape no horizontal scroll');assert.ok(await evaluate(AREA)>=35,'A11 landscape map remains usable');
   await evaluate('explore.select(window.__a11TrailEntry,window.__a11Trail);explore.sheet.setState("expanded")');
   assert.equal(await evaluate('!explore.$("detail-view").hidden&&!document.querySelector("dialog[open]")'),true,'A11 landscape detail stays in sheet');
   assert.ok(await evaluate('explore.$("sheet").getBoundingClientRect().height')<=width*.75,'A11 landscape sheet stays inside viewport');
   assert.equal(await evaluate(`(()=>{const r=explore.$('detail-back').getBoundingClientRect();return r.left>=0&&r.right<=innerWidth&&r.top>=0&&r.bottom<=innerHeight})()`),true,'A11 landscape Back remains exposed');
   await evaluate('explore.$("detail-back").click();explore.sheet.setState("collapsed")');await assertSelection('A11 landscape Back clears',true);
   await client.command('Emulation.setDeviceMetricsOverride',{width,height,deviceScaleFactor:2,mobile:true});await poll('innerWidth==='+width+'&&innerHeight==='+height,'A11 return to portrait');
  }
  if(width===390){
   result.a12Landscape=[];
   for(const [w,h,scale,screenHeight] of [[844,390,3],[932,430,3],[667,375,2],[844,320,3,390]])for(const notch of ['left','right']){
    await evaluate(`(()=>{explore.sheet.setState('collapsed');explore.drawer.close();const host=explore.$('map').parentElement;for(const edge of ['left','right','top','bottom'])host.style.setProperty('--test-safe-'+edge,((edge===${JSON.stringify(notch)}?47:edge==='bottom'?21:0))+'px')})()`);
    await client.command('Emulation.setDeviceMetricsOverride',{width:w,height:h,deviceScaleFactor:scale,mobile:true,...(screenHeight?{screenWidth:w,screenHeight}: {})});await poll('innerWidth==='+w+'&&innerHeight==='+h,'A12 short landscape');
    await evaluate('new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve)))');
    const size=await evaluate(`(()=>{const map=window.__rendered.find(g=>g._map)._map,r=explore.$('map').getBoundingClientRect(),n=map.getSize();return {render:[n.x,n.y],rect:[r.width,r.height],viewport:visualViewport.height}})()`);assert.ok(Math.abs(size.render[0]-size.rect[0])<=1&&Math.abs(size.render[1]-size.rect[1])<=1,'A12 no stale map dimensions');assert.ok(Math.abs(size.rect[1]-size.viewport)<=1,'A12 visible viewport height used');
    assert.equal(await evaluate('document.documentElement.scrollWidth>innerWidth'),false,'A12 landscape no horizontal overflow');
    const safe=async name=>{assert.equal(await evaluate(`(()=>{const e=explore.$(${JSON.stringify(name)}),r=e.getBoundingClientRect();return r.left>=${notch==='left'?47:0}&&r.right<=innerWidth-${notch==='right'?47:0}&&r.top>=0&&r.bottom<=innerHeight-21&&r.width>=44&&r.height>=44})()`),true,'A12 safe-area target '+name);};
    for(const name of ['layers','search','zoom-in','zoom-out','sheet-toggle'])await safe(name);
    const collapsed=await evaluate(AREA);assert.ok(collapsed>=80,'A12 landscape collapsed free map '+collapsed);
    await evaluate(`(()=>{explore.$('search').click();const list=[...explore.$('list-view').children].find(e=>!e.hidden),filters=list.querySelector('.explore-filters');filters.open=true;const query=list.querySelector('#query,#explore-query'),activity=list.querySelector('#activity,#explore-activity');if(activity){activity.value='';activity.dispatchEvent(new Event('input',{bubbles:true}));activity.dispatchEvent(new Event('change',{bubbles:true}));}query.value=window.__a11Trail.properties.name;query.dispatchEvent(new Event('input',{bubbles:true}));query.scrollIntoView({block:'center'});window.__landscapeList=list;window.__landscapeQuery=query})()`);
    const queryReachable=await evaluate(`(()=>{const r=window.__landscapeQuery.getBoundingClientRect(),e=document.elementFromPoint(r.x+r.width/2,r.y+r.height/2);return e===window.__landscapeQuery&&r.top>=0&&r.bottom<=innerHeight-21})()`);assert.equal(queryReachable,true,'A12 landscape search query reachable');
    await evaluate(`(()=>{const b=[...window.__landscapeList.querySelectorAll('button')].find(e=>e.classList.contains('explore-result')||e.parentElement===explore.$('search-results'));if(!b)throw Error('No landscape search result');b.scrollIntoView({block:'center'});window.__landscapeResult=b})()`);
    const buttonReachable=await evaluate(`(()=>{const b=window.__landscapeResult,r=b.getBoundingClientRect();return b.contains(document.elementFromPoint(r.x+r.width/2,r.y+r.height/2))})()`);assert.equal(buttonReachable,true,'A12 landscape result reachable');await evaluate('window.__landscapeResult.click()');await safe('detail-back');await assertSelection('A12 landscape result selection');
    const opened=await evaluate(AREA);assert.ok(opened>=50,'A12 landscape open detail free map '+opened);await evaluate('explore.$("detail-back").click()');assert.equal(await evaluate('!window.__landscapeList.hidden&&window.__landscapeQuery.value===window.__a11Trail.properties.name'),true,'A12 landscape Back preserves list and query');
    await evaluate('explore.drawer.open()');assert.equal(await evaluate('explore.sheet.state'),'collapsed','A12 short landscape panels mutually exclusive');await safe('drawer-close');
    await evaluate(`(()=>{const body=explore.$('drawer').querySelector('.explore-drawer-body');body.scrollTop=body.scrollHeight;window.__lastLayer=explore.$('layer-list').lastElementChild;window.__lastToggle=window.__lastLayer.querySelector('input');window.__lastToggle.scrollIntoView({block:'center'})})()`);
    assert.equal(await evaluate(`(()=>{const e=window.__lastToggle,r=e.getBoundingClientRect();return document.elementFromPoint(r.x+r.width/2,r.y+r.height/2)===e&&r.top>=0&&r.bottom<=innerHeight-21})()`),true,'A12 landscape final layer toggle reachable');const lastId=await evaluate('window.__lastLayer.dataset.layerId');await evaluate('window.__lastToggle.click()');assert.equal(await evaluate('window.__visible['+JSON.stringify(lastId)+']'),false,'A12 landscape layer toggle changes map');await evaluate('window.__lastToggle.click()');assert.equal(await evaluate('window.__visible['+JSON.stringify(lastId)+']'),true,'A12 landscape layer restored');
    const drawerFree=await evaluate(AREA);assert.ok(drawerFree>=50,'A12 landscape drawer free map '+drawerFree);await evaluate('explore.$("drawer-close").click()');assert.equal(await evaluate('explore.$("drawer").hidden'),true,'A12 landscape drawer close reachable');result.a12Landscape.push({viewport:[w,h],deviceScaleFactor:scale,...(screenHeight?{screenHeight}: {}),notch,collapsedFreeMapPct:collapsed,detailFreeMapPct:opened,drawerFreeMapPct:drawerFree,mapSize:size});
   }
   await evaluate(`(()=>{const host=explore.$('map').parentElement;for(const edge of ['left','right','top','bottom'])host.style.removeProperty('--test-safe-'+edge);explore.sheet.setState('half')})()`);
   await client.command('Emulation.setDeviceMetricsOverride',{width:390,height:844,deviceScaleFactor:3,mobile:true});await poll('innerWidth===390&&innerHeight===844','A12 return portrait');await evaluate('new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve)))');assert.equal(await evaluate('explore.sheet.state'),'half','A12 rotation keeps valid state');assert.equal(await evaluate('document.documentElement.scrollWidth>innerWidth'),false,'A12 portrait restored without overflow');await evaluate('explore.sheet.setState("collapsed")');
  }
  if(width===768){
   await client.command('Emulation.setDeviceMetricsOverride',{width:1024,height:768,deviceScaleFactor:2,mobile:true});await poll('innerWidth===1024&&innerHeight===768','A12 tablet landscape');await evaluate('new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve)))');await evaluate('explore.sheet.setState("collapsed")');const p=await evaluate('(()=>{const r=explore.$("sheet-toggle").getBoundingClientRect();return {x:r.x+40,y:r.y+24}})()');await flick(p,-60);assert.equal(await evaluate('explore.sheet.state'),'half','A12 tablet landscape native drag snap');assert.ok(await evaluate('explore.$("sheet").getBoundingClientRect().width')<=360,'A12 tablet landscape panel width');
   await evaluate('explore.sheet.setState("collapsed")');const handle=await evaluate('(()=>{const r=explore.$("sheet-toggle").getBoundingClientRect();return {x:r.x+40,y:r.y+24}})()'),tabletCenter=await evaluate('explore.state.view.center');
   await client.command('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:[handle]});await delay(110,undefined,{signal});await client.command('Input.dispatchTouchEvent',{type:'touchMove',touchPoints:[{x:handle.x,y:handle.y-100}]});const intermediate=await evaluate('explore.$("sheet").getBoundingClientRect().height');assert.ok(intermediate>64&&intermediate<768*.4,'A12 landscape tablet follows finger');await delay(110,undefined,{signal});await client.command('Input.dispatchTouchEvent',{type:'touchMove',touchPoints:[{x:handle.x,y:handle.y-220}]});await client.command('Input.dispatchTouchEvent',{type:'touchEnd',touchPoints:[]});assert.equal(await evaluate('explore.sheet.state'),'half','A12 landscape tablet slow snap');assert.deepEqual(await evaluate('explore.state.view.center'),tabletCenter,'A12 landscape tablet drag does not pan');
   await client.command('Emulation.setDeviceMetricsOverride',{width:768,height:1024,deviceScaleFactor:2,mobile:true});await poll('innerWidth===768&&innerHeight===1024','A12 tablet portrait restored');await evaluate('new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve)))');assert.equal(await evaluate('explore.sheet.state'),'half','A12 tablet rotation keeps state');await evaluate('explore.sheet.setState("collapsed")');
  }
  result.checks.push('A11 gestures, keyboard, retained filters/scroll, exact selection, carried details, drawer, labels and native zoom'+(width<768?', landscape':''));
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
