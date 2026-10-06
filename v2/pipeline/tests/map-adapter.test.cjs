const {test}=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const root=path.resolve(__dirname,'../..'),source=fs.readFileSync(path.join(root,'explore/map-adapter.js'),'utf8');
const names=['init','addLayer','removeLayer','setVisible','setStyle','setPins','onFeature','fit','setBasemap','destroy','setSelected','setLabels'];
function predicates(){const context={};vm.runInNewContext(source.replace('const api={init,','scope.testPredicates={hitGeometry,chooseHit,resolveTap,HIT_TOLERANCE,layers,handlers,labelled,matchingTouch,pinActivation,isDoubleTap,withinTapSlop,TAP_MOVEMENT_SLOP,setMap:value=>{map=value;}}; const api={init,'),context);return context.testPredicates;}
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
 A.addLayer('line',{features:[{properties:{id:'trail'},geometry:{type:'LineString'}}]},{weight:3,opacity:.85});A.setSelected('line','trail');assert.equal(groups[1].items[0].options.weight,6);
 A.setSelected('line',null);assert.equal(groups[1].items[0].options.weight,3);
 A.fit([[0,0],[1,1]],{topLeft:[24,108],bottomRight:[24,360]});assert.deepEqual(JSON.parse(JSON.stringify(fitted.options.paddingBottomRight)),[24,360]);assert.equal(fitted.options.maxZoom,15);A.destroy();
});
test('A13 selected line uses a two-tone casing and every lifecycle path restores normal styles',()=>{
 const surface=new EventTarget();surface.getBoundingClientRect=()=>({left:0,top:0});surface.closest=()=>null;
 const context={module:{exports:{}},document:{createElement:()=>({className:'',classList:{toggle(){}}})}},groups=[],mapLayers=new Set(),front=[];
 const map={createPane(){},getPane:()=>({style:{}}),on(){},off(){},setView(){},getZoom:()=>14,getCenter:()=>({lng:0,lat:0}),getBounds:()=>({getWest:()=>0,getSouth:()=>0,getEast:()=>1,getNorth:()=>1}),getContainer:()=>surface,latLngToContainerPoint:ll=>({x:Array.isArray(ll)?ll[1]:ll.lng,y:Array.isArray(ll)?ll[0]:ll.lat}),containerPointToLatLng:p=>({lng:p.x,lat:p.y}),remove(){mapLayers.clear();},addLayer(group){mapLayers.add(group);},removeLayer(group){mapLayers.delete(group);},hasLayer(group){return mapLayers.has(group);},invalidateSize(){},fitBounds(){}};
 context.L={map:()=>map,control:{scale:()=>({addTo(){}})},tileLayer:()=>({addTo(){return this;}}),geoJSON(data,options={}){
  const items=data.features.map(feature=>{const base=typeof options.style==='function'?options.style(feature):options.style||{};return {feature,options:{...base},setStyle(value){Object.assign(this.options,value);},bringToFront(){front.push(this);},getBounds(){return {getNorthWest:()=>[0,0],getSouthEast:()=>[1,1]};}};});
  const group={items,options,eachLayer(fn){if(String(options.style?.className||'').startsWith('explore-selection-casing-'))this.eachCalls=(this.eachCalls||0)+1;items.forEach(fn);},addTo(target){target.addLayer(this);return this;},setStyle(style){items.forEach(item=>item.setStyle(typeof style==='function'?style(item.feature):style));}};groups.push(group);return group;
 }};
 vm.runInNewContext(source.replace('const api={init,','scope.__a13Test={layers,casings,resolveTap,setMap:value=>{map=value;}};const api={init,'),context);const A=context.module.exports;A.init('map',{center:[0,0],zoom:14});
 const features=['one','two','three'].map(id=>({type:'Feature',properties:{id},geometry:{type:'LineString',coordinates:[[0,0],[1,1]]}}));
 const normal=feature=>({color:feature.properties.id==='two'?'#b4a4ad':'#73c5dc',weight:feature.properties.id==='two'?2.25:3,opacity:.85,dashArray:'5 2'});
 A.addLayer('lines',{type:'FeatureCollection',features},normal);const lines=groups[0],base=lines.items.map(item=>({...normal(item.feature)}));
 const casingGroups=()=>groups.filter(group=>mapLayers.has(group)&&String(group.options.style?.className||'').startsWith('explore-selection-casing-'));
 const assertNormal=()=>lines.items.forEach((item,index)=>{for(const key of Object.keys(base[index]))assert.equal(item.options[key],base[index][key]);assert.equal(item.options.selected,false);});
 A.setSelected('lines','one');
 const selected=lines.items[0];assert.equal(selected.options.weight,6);assert.equal(selected.options.opacity,1);assert.equal(selected.options.color,base[0].color);assert.equal(selected.options.dashArray,base[0].dashArray);
 for(const item of lines.items.slice(1)){assert.equal(item.options.opacity,Math.max(.5,base[lines.items.indexOf(item)].opacity*.7));assert.ok(item.options.opacity>=.5);assert.equal(item.options.color,base[lines.items.indexOf(item)].color);assert.equal(item.options.weight,base[lines.items.indexOf(item)].weight);assert.equal(item.options.dashArray,base[lines.items.indexOf(item)].dashArray);assert.ok(mapLayers.has(lines));}
 let cases=casingGroups();assert.equal(cases.length,2);assert.ok(cases.every(group=>group.items.length===1&&group.items[0].feature===features[0]&&group.options.interactive===false));
 const halo=cases.find(group=>group.options.style.className==='explore-selection-casing-halo'),edge=cases.find(group=>group.options.style.className==='explore-selection-casing-edge');
 assert.equal(halo.options.style.weight,selected.options.weight+4);assert.equal(edge.options.style.weight,selected.options.weight+6);assert.notEqual(halo.options.style.color,selected.options.color);assert.notEqual(edge.options.style.color,selected.options.color);
 assert.deepEqual(front.slice(-3),[edge.items[0],halo.items[0],selected],'casing is above other lines and selected line sits directly above both casing tones');
 assert.deepEqual([...context.__a13Test.layers.keys()],['lines'],'casing stays outside the selectable layer registry');A.onFeature('lines',()=>{});context.__a13Test.setMap(map);const resolverScanCounts=cases.map(group=>group.eachCalls);assert.equal(context.__a13Test.resolveTap({x:.5,y:.5})?.featureId,'one','resolver returns the source feature, never a casing path');assert.deepEqual(cases.map(group=>group.eachCalls),resolverScanCounts,'tap resolver does not inspect adapter-owned casing paths');
 A.setSelected('lines','two');cases=casingGroups();assert.equal(cases.length,2);assert.ok(cases.every(group=>group.items[0].feature===features[1]));assert.equal(lines.items[1].options.weight,5.25);assert.ok(lines.items[1].options.weight>=5);assert.equal(lines.items[0].options.weight,base[0].weight);assert.equal(lines.items[0].options.opacity,Math.max(.5,base[0].opacity*.7));
 A.setSelected('lines',null);assert.equal(casingGroups().length,0);assertNormal();
 A.setSelected('lines','one');A.setVisible('lines',false);assert.equal(casingGroups().length,0);assertNormal();
 const restyled=feature=>({...normal(feature),weight:feature.properties.id==='one'?4:2.5,opacity:.8});A.setStyle('lines',restyled);assert.equal(casingGroups().length,0);assert.equal(lines.items[0].options.weight,4);assert.equal(lines.items[0].options.opacity,.8);assert.equal(lines.items[0].options.selected,false);
 A.setVisible('lines',true);assert.equal(casingGroups().length,2);assert.equal(lines.items[0].options.weight,7);
 A.setStyle('lines',restyled);assert.equal(casingGroups().length,2);assert.equal(lines.items[0].options.weight,7);assert.equal(casingGroups().find(g=>g.options.style.className==='explore-selection-casing-halo').options.style.weight,11);
 A.removeLayer('lines');assert.equal(casingGroups().length,0);assert.equal(mapLayers.size,0);
 const polygons=[{type:'Feature',properties:{id:'land-one'},geometry:{type:'Polygon',coordinates:[]}}];A.addLayer('land',{type:'FeatureCollection',features:polygons},{color:'#8f9f89',fillColor:'#8f9f89',fillOpacity:.12,weight:0,opacity:0,stroke:false,dashArray:'5 5'});A.setSelected('land','land-one');assert.equal(casingGroups().length,0,'polygon selection never creates line casing');assert.equal(groups.at(-1).items[0].options.fillOpacity,.12);A.setSelected('land',null);
 A.addLayer('again',{type:'FeatureCollection',features},normal);A.setSelected('again','one');assert.equal(casingGroups().length,2);A.destroy();assert.equal(casingGroups().length,0);assert.equal(mapLayers.size,0);
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
 const map={getContainer:()=>surface,createPane(){},getPane:()=>({style:{}}),on(){},off(){},setView(){},getZoom:()=>18,getCenter:()=>({lng:0,lat:0}),getBounds:()=>({getWest:()=>0,getSouth:()=>0,getEast:()=>1,getNorth:()=>1}),hasLayer:g=>active.has(g),latLngToContainerPoint:p=>p.lng===undefined?({x:p[1],y:p[0]}):({x:Math.round(p.lng),y:Math.round(p.lat)}),containerPointToLatLng:p=>({lng:p.x,lat:p.y}),remove(){},removeLayer:g=>active.delete(g)};
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

test('review fix 1: controlled release cadence at 279/280 ms zooms once; 281 ms and later select twice',()=>{
 for(const gap of [279,280,281,500])for(const jitter of [0,3]){
  const surface=new EventTarget();surface.getBoundingClientRect=()=>({left:0,top:0});surface.closest=()=>null;
  const active=new Set(),timers=new Map(),selections=[];let clock=0,nextTimer=0,zoom=18,zoomCalls=0;
  const map={getContainer:()=>surface,createPane(){},getPane:()=>({style:{}}),on(){},off(){},setView(){},getZoom:()=>zoom,setZoomAround(point,value){zoom=value;zoomCalls++;},getCenter:()=>({lng:0,lat:0}),getBounds:()=>({getWest:()=>0,getSouth:()=>0,getEast:()=>1,getNorth:()=>1}),hasLayer:g=>active.has(g),latLngToContainerPoint:p=>({x:p.lng??p[1],y:p.lat??p[0]}),containerPointToLatLng:p=>({lng:p.x,lat:p.y}),remove(){},removeLayer:g=>active.delete(g)};
  const context={module:{exports:{}},setTimeout(fn,ms){const id=++nextTimer;timers.set(id,{fn,due:clock+ms});return id;},clearTimeout(id){timers.delete(id);}};
  context.L={map:()=>map,control:{scale:()=>({addTo(){}})},tileLayer:()=>({addTo(){return this;}}),geoJSON(data){return {addTo(){active.add(this);return this;},eachLayer(fn){data.features.forEach(feature=>fn({feature,getBounds:()=>({getNorthWest:()=>[100,10],getSouthEast:()=>[100,40]})}));}};}};
  vm.runInNewContext(source,context);const A=context.module.exports;A.init('map',{center:[0,0],zoom:18});A.addLayer('lines',{features:[{properties:{id:'target'},geometry:{type:'LineString',coordinates:[[10,100],[40,100]]}}]},{});A.onFeature('lines',f=>selections.push(f.properties.id));
  function advance(time){let next;while((next=[...timers].sort((a,b)=>a[1].due-b[1].due)[0])&&next[1].due<=time){clock=next[1].due;timers.delete(next[0]);next[1].fn();}clock=time;}
  function touch(type,time,dx=0){advance(time);const e=new Event(type,{cancelable:true});Object.defineProperty(e,'timeStamp',{value:time});const p={clientX:15.5+dx,clientY:100};e.touches=type==='touchend'?[]:[p];e.changedTouches=[p];surface.dispatchEvent(e);}
  touch('touchstart',0);if(jitter)touch('touchmove',5,jitter);touch('touchend',10,jitter);
  assert.equal(selections.length,0);assert.equal(timers.size,1);
  const release=10+gap;
  // Inside the window, contact starts before the pending selection deadline.
  // Outside it, let the first single-tap timer run before the second contact.
  touch('touchstart',gap<=280?release-10:release);if(jitter)touch('touchmove',release,jitter);touch('touchend',release,jitter);
  if(gap<=280){assert.equal(zoom,19);assert.equal(zoomCalls,1);assert.deepEqual(selections,[]);assert.equal(timers.size,0);}
  else{assert.equal(zoom,18);assert.equal(zoomCalls,0);assert.deepEqual(selections,['target']);assert.equal(timers.size,1);}
  advance(release+1000);assert.deepEqual(selections,gap<=280?[]:['target','target']);assert.equal(zoomCalls,gap<=280?1:0);assert.equal(timers.size,0);A.destroy();
 }
});

test('D1: tap slop uses total displacement from the start, including its exact boundary',()=>{
 const H=predicates(),start={clientX:20,clientY:30};assert.equal(H.TAP_MOVEMENT_SLOP,10);
 for(const [dx,dy] of [[3,0],[6,0],[10,0],[6,8]])assert.equal(H.withinTapSlop(start,{clientX:20+dx,clientY:30+dy}),true);
 assert.equal(H.withinTapSlop(start,{clientX:30.01,clientY:30}),false);assert.equal(H.withinTapSlop(start,{clientX:20,clientY:55}),false);
});

test('D1: jitter schedules one fractional selection; unhandled click falls back; pans and pinch stay consumed',()=>{
 const surface=new EventTarget();surface.getBoundingClientRect=()=>({left:0,top:0});surface.closest=()=>null;
 const active=new Set();let scheduled,chosen,zoom=18;
 const map={getContainer:()=>surface,createPane(){},getPane:()=>({style:{}}),on(){},off(){},setView(){},getZoom:()=>zoom,setZoomAround(point,value){zoom=value;},getCenter:()=>({lng:0,lat:0}),getBounds:()=>({getWest:()=>0,getSouth:()=>0,getEast:()=>1,getNorth:()=>1}),hasLayer:g=>active.has(g),latLngToContainerPoint:p=>p.lng===undefined?({x:p[1],y:p[0]}):({x:Math.round(p.lng),y:Math.round(p.lat)}),containerPointToLatLng:p=>({lng:p.x,lat:p.y}),remove(){},removeLayer:g=>active.delete(g)};
 const context={module:{exports:{}},setTimeout(fn){scheduled=fn;return 1;},clearTimeout(){scheduled=null;}};
 context.L={map:()=>map,control:{scale:()=>({addTo(){}})},tileLayer:()=>({addTo(){return this;}}),geoJSON(data){return {addTo(){active.add(this);return this;},eachLayer(fn){data.features.forEach(feature=>fn({feature,getBounds:()=>({getNorthWest:()=>[feature.geometry.coordinates[0][1],10],getSouthEast:()=>[feature.geometry.coordinates[0][1],40]})}));}};}};
 vm.runInNewContext(source,context);const A=context.module.exports;A.init('map',{center:[0,0],zoom:18});
 A.addLayer('lines',{features:[['target',100.6],['neighbor',101]].map(([id,y])=>({properties:{id},geometry:{type:'LineString',coordinates:[[10,y],[40,y]]}}))},{});A.onFeature('lines',f=>{chosen=f.properties.id;});
 const point={clientX:15.5,clientY:100.6};
 function event(type,time,p=point,multiple=false,remaining=[]){const e=new Event(type,{cancelable:true});Object.defineProperty(e,'timeStamp',{value:time});if(type==='click')Object.assign(e,{clientX:Math.round(p.clientX),clientY:Math.round(p.clientY),detail:1});else{e.touches=type==='touchend'?remaining:multiple?[p,{clientX:40,clientY:100}]:[p];e.changedTouches=[p];}surface.dispatchEvent(e);}
 for(const [i,dx] of [3,6,10].entries()){
  chosen=undefined;scheduled=null;const time=1000+i*1000,p={...point,clientX:point.clientX+dx};event('touchstart',time);event('touchmove',time+5,p);event('touchend',time+10,p);event('click',time+15,p);
  assert.equal(chosen,undefined,'handled native tap skips the compatibility click');assert.equal(typeof scheduled,'function');scheduled();assert.equal(chosen,'target');
 }
 chosen=undefined;scheduled=null;event('touchstart',5000);event('touchmove',5005,{...point,clientX:point.clientX+25});event('touchmove',5010);event('touchend',5015);event('click',5020);assert.equal(scheduled,null);assert.equal(chosen,undefined,'a pan cannot become a tap by returning to the start');
 event('touchend',6000);event('click',6010);assert.equal(chosen,'target','unhandled release falls back with fractional coordinates, not rounded neighbor');
 chosen=undefined;scheduled=null;event('touchstart',7000);event('touchmove',7005,point,true);event('touchend',7010);event('click',7015);assert.equal(scheduled,null);assert.equal(chosen,undefined,'multi-touch remains consumed without selection');
 event('touchstart',7500,point,true);event('touchend',7505,point,false,[point]);event('touchend',7510);event('click',7515);assert.equal(scheduled,null);assert.equal(chosen,undefined,'sequential finger releases remain consumed through the last release');
 event('touchstart',8000);event('touchmove',8005,{...point,clientX:point.clientX+3});event('touchend',8010,{...point,clientX:point.clientX+3});assert.equal(typeof scheduled,'function');event('touchstart',8240);event('touchmove',8245,{...point,clientX:point.clientX+3});event('touchend',8250,{...point,clientX:point.clientX+3});event('click',8260);assert.equal(scheduled,null);assert.equal(chosen,undefined);assert.equal(zoom,19,'jittery double-tap zooms once');A.destroy();
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
