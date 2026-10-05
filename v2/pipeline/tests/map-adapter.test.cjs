const {test}=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const root=path.resolve(__dirname,'../..'),source=fs.readFileSync(path.join(root,'explore/map-adapter.js'),'utf8');
const names=['init','addLayer','removeLayer','setVisible','setStyle','setPins','onFeature','fit','setBasemap','destroy','setSelected','setLabels'];
function predicates(){const context={};vm.runInNewContext(source.replace('const api={init,','scope.testPredicates={hitGeometry,chooseHit,resolveTap,HIT_TOLERANCE,layers,handlers,labelled,matchingTouch,pinActivation,isDoubleTap,setMap:value=>{map=value;}}; const api={init,'),context);return context.testPredicates;}
const project=([x,y])=>({x,y});
test('A12 hit tolerance includes the boundary for lines and points, including multipart lines',()=>{
 const H=predicates(),line={type:'LineString',coordinates:[[0,0],[100,0]]};
 assert.equal(H.HIT_TOLERANCE,14);assert.equal(H.hitGeometry({x:50,y:14},line,project).priority,1);assert.equal(H.hitGeometry({x:50,y:14.01},line,project),null);
 assert.equal(H.hitGeometry({x:0,y:14},{type:'Point',coordinates:[0,0]},project).priority,0);
 assert.equal(H.hitGeometry({x:0,y:14.01},{type:'Point',coordinates:[0,0]},project),null);
 assert.equal(H.hitGeometry({x:50,y:114},{type:'MultiLineString',coordinates:[line.coordinates,[[0,100],[100,100]]]},project).priority,1);
});
test('A12 polygons include their exterior and exclude holes',()=>{
 const H=predicates(),g={type:'Polygon',coordinates:[[[0,0],[100,0],[100,100],[0,100],[0,0]],[[30,30],[70,30],[70,70],[30,70],[30,30]]]};
 assert.equal(H.hitGeometry({x:15,y:50},g,project).priority,2);assert.equal(H.hitGeometry({x:50,y:50},g,project),null);
 assert.equal(H.hitGeometry({x:101,y:50},g,project),null);assert.equal(H.hitGeometry({x:0,y:50},g,project).priority,2);
});
test('A12 resolver prioritizes point, closest line, most specific polygon and topmost ties; ignores hidden layers',()=>{
 const H=predicates(),c=(id,priority,distance=0,area=100,order=1)=>({featureId:id,priority,distance,area,order});
 assert.equal(H.chooseHit([c('polygon',2),c('line',1),c('pin',0)]).featureId,'pin');
 assert.equal(H.chooseHit([c('far',1,12),c('near',1,2)]).featureId,'near');
 assert.equal(H.chooseHit([c('large',2,0,100),c('specific',2,0,10)]).featureId,'specific');
 assert.equal(H.chooseHit([c('lower',1,2,100,1),c('upper',1,2,100,2)]).featureId,'upper');
 const feature={properties:{id:'hidden'},geometry:{type:'Point',coordinates:[50,50]}};
 const group={eachLayer(fn){fn({feature,getLatLng:()=>[50,50]});}};H.layers.set('layer',group);H.handlers.set('layer',()=>{});
 let visible=false,projections=0;H.setMap({hasLayer:()=>visible,latLngToContainerPoint(p){projections++;return {x:p[1],y:p[0]};}});
 assert.equal(H.resolveTap({x:50,y:50}),null);assert.equal(projections,0);visible=true;
 assert.equal(H.resolveTap({x:50,y:50}).featureId,'hidden');assert.equal(H.resolveTap({x:500,y:500}),null);
});
test('criterion 17: exact adapter surface; all renderer references stay in the adapter',()=>{
 assert.deepEqual(Object.keys(require('../../explore/map-adapter.js')),names);
 for(const name of fs.readdirSync(path.join(root,'explore')).filter(name=>name.endsWith('.js')&&name!=='map-adapter.js'))
  assert.doesNotMatch(fs.readFileSync(path.join(root,'explore',name),'utf8'),/\bL\./,name);
});
test('adapter absence returns false; plain view payload, control lifecycle and reinitialization work',()=>{
 const context={module:{exports:{}}};vm.runInNewContext(source,context);const A=context.module.exports;
 assert.equal(A.init('map',{center:[1,2],zoom:10}),false);
 let removed=0,zoom=10,center={lng:1,lat:2},callbacks=[];
 const map={createPane(){},getPane(){return {style:{}};},on(){},off(){},setView(ll,z){center={lng:ll[1],lat:ll[0]};zoom=z;},
  getZoom:()=>zoom,getCenter:()=>center,getBounds:()=>({getWest:()=>0,getSouth:()=>1,getEast:()=>2,getNorth:()=>3}),
  setZoom(z){zoom=z;},remove(){removed++;},removeLayer(){},invalidateSize(){},fitBounds(){center={lng:3,lat:4};}};
 context.L={map:()=>map,control:{scale:()=>({addTo(){}})},tileLayer:()=>({addTo(){return this;}})};
 const listeners=new Set(),button={addEventListener(_,fn){listeners.add(fn);},removeEventListener(_,fn){listeners.delete(fn);}};
 assert.equal(A.init('map',{center:[1,2],zoom:10,controls:{zoomIn:button},onViewChange:payload=>callbacks.push(JSON.parse(JSON.stringify(payload)))}),true);
 assert.deepEqual(callbacks.at(-1),{zoom:10,center:[1,2],bounds:[[0,1],[2,3]]});assert.equal(listeners.size,1);
 [...listeners][0]();assert.equal(zoom,11);A.fit([[0,1],[2,3]]);assert.deepEqual(callbacks.at(-1).center,[3,4]);
 A.destroy();assert.equal(listeners.size,0);assert.equal(removed,1);
 assert.equal(A.init('map',{center:[2,3],zoom:12}),true);A.destroy();assert.equal(removed,2);
});
test('A11 selection emphasizes one feature, clears it, and preserves generalized polygon limits',()=>{
 const context={module:{exports:{}}},groups=[];let fitted;
 const map={createPane(){},getPane:()=>({style:{}}),on(){},off(){},setView(){},getZoom:()=>14,getCenter:()=>({lng:0,lat:0}),getBounds:()=>({getWest:()=>0,getSouth:()=>0,getEast:()=>1,getNorth:()=>1}),remove(){},removeLayer(){},invalidateSize(){},fitBounds(bounds,options){fitted={bounds,options};}};
 context.L={map:()=>map,control:{scale:()=>({addTo(){}})},tileLayer:()=>({addTo(){return this;}}),geoJSON(data){
  const items=data.features.map(feature=>({feature,options:{},setStyle(value){Object.assign(this.options,value);},on(){return this;}}));
  const group={items,eachLayer(fn){items.forEach(fn);},addTo(){return this;},setStyle(style){items.forEach(item=>item.setStyle(typeof style==='function'?style(item.feature):style));}};groups.push(group);return group;
 }};
 vm.runInNewContext(source,context);const A=context.module.exports;A.init('map',{center:[0,0],zoom:14});
 const features=['one','two'].map(id=>({properties:{id},geometry:{type:'Polygon'}}));
 A.addLayer('context',{features},{fillOpacity:.12,weight:0,opacity:0,stroke:false,dashArray:'5 5'});A.setSelected('context','one');
 assert.equal(groups[0].items[0].options.selected,true);assert.equal(groups[0].items[0].options.fillOpacity,.12);
 assert.equal(groups[0].items[1].options.fillOpacity,.04);assert.equal(groups[0].items[0].options.stroke,false);
 A.setSelected('context',null);assert.equal(groups[0].items[1].options.fillOpacity,.12);assert.equal(groups[0].items[0].options.selected,false);
 A.addLayer('line',{features:[{properties:{id:'trail'},geometry:{type:'LineString'}}]},{weight:3,opacity:.85});A.setSelected('line','trail');assert.equal(groups[1].items[0].options.weight,5);
 A.setSelected('line',null);assert.equal(groups[1].items[0].options.weight,3);
 A.fit([[0,0],[1,1]],{topLeft:[24,108],bottomRight:[24,360]});assert.deepEqual(JSON.parse(JSON.stringify(fitted.options.paddingBottomRight)),[24,360]);assert.equal(fitted.options.maxZoom,15);A.destroy();
});
test('A11 labels use carried names only, respect zoom, clear, and share a global cap',()=>{
 const context={module:{exports:{}},document:{createElement:()=>({})}},active=new Set();let zoom=13,publish,scanned=0,bound=0;
 const map={createPane(){},getPane:()=>({style:{}}),on(name,fn){if(name.includes('moveend'))publish=fn;},off(){},setView(){},getZoom:()=>zoom,getCenter:()=>({lng:0,lat:0}),getBounds:()=>({getWest:()=>0,getSouth:()=>0,getEast:()=>1,getNorth:()=>1,contains:()=>true}),latLngToContainerPoint:ll=>({x:ll.lng*220+120,y:ll.lat*60+140}),hasLayer:()=>true,remove(){},removeLayer(){}};
 context.L={map:()=>map,control:{scale:()=>({addTo(){}})},tileLayer:()=>({addTo(){return this;}}),geoJSON(data){
  const items=data.features.map(feature=>({feature,on(){return this;},getLatLng:()=>feature.geometry.coordinates,bindTooltip(node,options){bound++;this.label=node.textContent;assert.equal(options.interactive,false);assert.equal(options.permanent,true);return this;},openTooltip(){active.add(this);return this;},unbindTooltip(){active.delete(this);}}));return {eachLayer(fn){scanned++;items.forEach(fn);},addTo(){return this;}};
 }};
 vm.runInNewContext(source,context);const A=context.module.exports;A.init('map',{center:[0,0],zoom:13});
 const features=Array.from({length:40},(_,i)=>({properties:{id:String(i),name:i===0?null:'Carried '+i},geometry:{type:'Point',coordinates:{lng:i%10,lat:Math.floor(i/10)}}}));
 A.addLayer('names',{features},{});A.setLabels('names',{property:'name',minZoom:14,max:40});assert.equal(active.size,0);assert.equal(scanned,0,'no feature scan below label zoom');assert.equal(bound,0,'no tooltip allocation below label zoom');zoom=14;publish();assert.equal(active.size,32);assert.equal(bound,32,'only capped visible labels allocated');assert.ok([...active].every(item=>item.label===item.feature.properties.name));
 zoom=13;publish();assert.equal(active.size,0);zoom=14;publish();assert.equal(active.size,32);A.setLabels('names',null);assert.equal(active.size,0);A.destroy();
});

test('A12 label boxes select the same feature and do not intercept outside their own bounds',()=>{
 const H=predicates(),feature={properties:{id:'labelled'},geometry:{type:'LineString',coordinates:[[0,100],[100,100]]}},group={eachLayer(){}};
 H.layers.set('line',group);H.handlers.set('line',()=>{});
 H.labelled.add({feature,labelLayerId:'line',getTooltip:()=>({getElement:()=>({getBoundingClientRect:()=>({left:20,right:80,top:10,bottom:30,width:60})})})});
 H.setMap({getContainer:()=>({getBoundingClientRect:()=>({left:0,top:0})}),hasLayer:()=>true});
 assert.equal(H.resolveTap({x:40,y:20}).featureId,feature.properties.id);assert.equal(H.resolveTap({x:81,y:20}),null);
 H.setMap({getContainer:()=>({getBoundingClientRect:()=>({left:0,top:0})}),hasLayer:()=>false});assert.equal(H.resolveTap({x:40,y:20}),null);
});

test('A12 regression samples include shortest, longest, real crossings and eight distinct trails per region',async()=>{
 const {trailSamples}=await import('./browser/explore-checks.mjs');
 const crosses=(a,b)=>{
  const lines=f=>f.geometry.type==='LineString'?[f.geometry.coordinates]:f.geometry.coordinates;
  const side=(a,b,p)=>(b[0]-a[0])*(p[1]-a[1])-(b[1]-a[1])*(p[0]-a[0]);
  for(const x of lines(a))for(const y of lines(b))for(let i=1;i<x.length;i++)for(let j=1;j<y.length;j++)
   if(side(x[i-1],x[i],y[j-1])*side(x[i-1],x[i],y[j])<0&&side(y[j-1],y[j],x[i-1])*side(y[j-1],y[j],x[i])<0)return true;
  return false;
 };
 for(const [region,pair,shortest,longest] of [['aspen',['usfs-trail-8919662','usfs-trail-8928063'],'usfs-trail-8932151','usfs-trail-8922773'],['douglas-co',['usfs-trail-8913499','usfs-trail-8964041'],'usfs-trail-8925547','usfs-trail-8913499']]){
  const index=JSON.parse(fs.readFileSync(path.join(root,'regions',region,'display/index.json'))),artifact=index.artifacts.find(a=>a.layer_id==='trails');
  const features=JSON.parse(fs.readFileSync(path.join(root,artifact.path))).features,samples=trailSamples(features,pair),ids=samples.map(f=>f.properties.id);
  assert.equal(samples.length,8);assert.equal(new Set(ids).size,8);for(const id of [shortest,longest,...pair])assert.ok(ids.includes(id));
  assert.equal(crosses(features.find(f=>f.properties.id===pair[0]),features.find(f=>f.properties.id===pair[1])),true,'real source crossing');
 }
});
test('A12 touch selection uses fractional touch coordinates rather than the rounded compatibility click',()=>{
 const surface=new EventTarget();surface.getBoundingClientRect=()=>({left:0,top:0});surface.closest=()=>null;
 const active=new Set();let scheduled,chosen;
 const map={getContainer:()=>surface,createPane(){},getPane:()=>({style:{}}),on(){},off(){},setView(){},getZoom:()=>18,getCenter:()=>({lng:0,lat:0}),getBounds:()=>({getWest:()=>0,getSouth:()=>0,getEast:()=>1,getNorth:()=>1}),hasLayer:g=>active.has(g),latLngToContainerPoint:p=>({x:p[1],y:p[0]}),containerPointToLatLng:p=>({lng:p.x,lat:p.y}),remove(){},removeLayer:g=>active.delete(g)};
 const context={module:{exports:{}},setTimeout(fn){scheduled=fn;return 1;},clearTimeout(){scheduled=null;}};
 context.L={map:()=>map,control:{scale:()=>({addTo(){}})},tileLayer:()=>({addTo(){return this;}}),geoJSON(data){const group={addTo(){active.add(this);return this;},eachLayer(fn){data.features.forEach(feature=>fn({feature,getBounds:()=>({getNorthWest:()=>[feature.geometry.coordinates[0][1],10],getSouthEast:()=>[feature.geometry.coordinates[0][1],20]})}));}};return group;}};
 vm.runInNewContext(source,context);const A=context.module.exports;A.init('map',{center:[0,0],zoom:18});
 A.addLayer('lines',{features:[['target',100.6],['neighbor',101]].map(([id,y])=>({properties:{id},geometry:{type:'LineString',coordinates:[[10,y],[20,y]]}}))},{});
 A.onFeature('lines',f=>{chosen=f.properties.id;});
 const start=new Event('touchstart');start.touches=[{clientX:15.5,clientY:100.6}];surface.dispatchEvent(start);
 const end=new Event('touchend');end.changedTouches=[{clientX:15.5,clientY:100.6}];end.touches=[];surface.dispatchEvent(end);
 const click=new Event('click');Object.assign(click,{clientX:16,clientY:101,pointerType:'touch',detail:1});surface.dispatchEvent(click);
 assert.equal(chosen,undefined,'touch selection is deferred');scheduled();assert.equal(chosen,'target','fractional touch wins over rounded click neighbor');A.destroy();
});

test('R2: touch records match Safari plain clicks, expire, and reject another location or backwards timestamp',()=>{
 const H=predicates(),record={time:100,clientX:20.5,clientY:50.5,point:{x:20.5,y:50.5}};
 assert.equal(H.matchingTouch({timeStamp:150,clientX:21,clientY:51},record),record);
 assert.equal(H.matchingTouch({timeStamp:800,clientX:21,clientY:51},record),record);
 assert.equal(H.matchingTouch({timeStamp:801,clientX:21,clientY:51},record),null);
 assert.equal(H.matchingTouch({timeStamp:150,clientX:100,clientY:51},record),null);
 assert.equal(H.matchingTouch({timeStamp:99,clientX:21,clientY:51},record),null);
 assert.equal(H.matchingTouch({timeStamp:150,clientX:21,clientY:51,pointerType:'mouse'},record),null,'hybrid mouse remains immediate');
});
test('R3: keyboard and assistive pin activation select directly, physical clicks stay with the resolver',()=>{
 const H=predicates();assert.equal(H.pinActivation({originalEvent:{type:'keypress'}}),true);
 assert.equal(H.pinActivation({originalEvent:{type:'click',clientX:0,clientY:0}}),true);
 assert.equal(H.pinActivation({originalEvent:{type:'click',clientX:40,clientY:80}}),false);
});
test('R4: direct points win over another feature label; labels win over lines and polygons',()=>{
 const H=predicates(),label={priority:.5,distance:0,order:1,featureId:'label'};
 assert.equal(H.chooseHit([label,{priority:0,distance:12,order:1,featureId:'pin'}]).featureId,'pin');
 assert.equal(H.chooseHit([label,{priority:1,distance:0,order:2,featureId:'line'},{priority:2,distance:0,order:3,area:2,featureId:'land'}]).featureId,'label');
});
test('R4: resolver selects a point beneath another feature label box',()=>{
 const H=predicates(),line={properties:{id:'label'},geometry:{type:'LineString',coordinates:[[0,0],[100,0]]}},pin={properties:{id:'pin'},geometry:{type:'Point',coordinates:[40,20]}};
 H.layers.set('labels',{eachLayer(){}});H.handlers.set('labels',()=>{});
 H.labelled.add({feature:line,labelLayerId:'labels',getTooltip:()=>({getElement:()=>({getBoundingClientRect:()=>({left:20,right:80,top:10,bottom:30,width:60})})})});
 H.layers.set('points',{eachLayer(fn){fn({feature:pin,getLatLng:()=>[20,40]});}});H.handlers.set('points',()=>{});
 H.setMap({getContainer:()=>({getBoundingClientRect:()=>({left:0,top:0})}),hasLayer:()=>true,latLngToContainerPoint:p=>({x:p[1],y:p[0]})});
 assert.equal(H.resolveTap({x:40,y:20}).featureId,'pin');
});

test('A12 double-tap uses touch time and distance, beyond Leaflet 200 ms, with deterministic boundaries',()=>{
 const H=predicates(),first={time:100,clientX:20,clientY:30};
 assert.equal(H.isDoubleTap(first,{time:340,clientX:20,clientY:30}),true);
 assert.equal(H.isDoubleTap(first,{time:380,clientX:50,clientY:30}),true);
 assert.equal(H.isDoubleTap(first,{time:381,clientX:20,clientY:30}),false);
 assert.equal(H.isDoubleTap(first,{time:300,clientX:50.01,clientY:30}),false);
 assert.equal(H.isDoubleTap(first,{time:99,clientX:20,clientY:30}),false);
 assert.equal(H.isDoubleTap(null,{time:200,clientX:20,clientY:30}),false);
});

test('A12 viewport and orientation changes coalesce renderer resize and clean up listeners/frame',()=>{
 const listeners=new Map();let frame,scheduled=0,invalidations=0,cancelled;
 const context={module:{exports:{}},addEventListener:(name,fn)=>listeners.set('window.'+name,fn),removeEventListener:name=>listeners.delete('window.'+name),visualViewport:{addEventListener:(name,fn)=>listeners.set('viewport.'+name,fn),removeEventListener:name=>listeners.delete('viewport.'+name)},requestAnimationFrame(fn){frame=fn;scheduled++;return 7;},cancelAnimationFrame(id){cancelled=id;}};
 const map={createPane(){},getPane:()=>({style:{}}),on(){},off(){},setView(){},getZoom:()=>10,getCenter:()=>({lng:0,lat:0}),getBounds:()=>({getWest:()=>0,getSouth:()=>0,getEast:()=>1,getNorth:()=>1}),invalidateSize(options){invalidations++;assert.equal(options.pan,false);},remove(){},removeLayer(){}};
 context.L={map:()=>map,control:{scale:()=>({addTo(){}})},tileLayer:()=>({addTo(){return this;}})};
 vm.runInNewContext(source,context);const A=context.module.exports;A.init('map',{center:[0,0],zoom:10});
 assert.equal(listeners.size,3);listeners.get('window.resize')();listeners.get('viewport.resize')();listeners.get('window.orientationchange')();assert.equal(scheduled,1);frame();assert.equal(invalidations,1);
 listeners.get('viewport.resize')();A.destroy();assert.equal(cancelled,7);assert.equal(listeners.size,0);
});
