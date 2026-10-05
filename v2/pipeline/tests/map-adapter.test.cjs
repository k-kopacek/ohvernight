const {test}=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const root=path.resolve(__dirname,'../..'),source=fs.readFileSync(path.join(root,'explore/map-adapter.js'),'utf8');
const names=['init','addLayer','removeLayer','setVisible','setStyle','setPins','onFeature','fit','setBasemap','destroy','setSelected','setLabels'];
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
 const map={createPane(){},getPane:()=>({style:{}}),on(_,fn){publish=fn;},off(){},setView(){},getZoom:()=>zoom,getCenter:()=>({lng:0,lat:0}),getBounds:()=>({getWest:()=>0,getSouth:()=>0,getEast:()=>1,getNorth:()=>1,contains:()=>true}),latLngToContainerPoint:ll=>({x:ll.lng*220+120,y:ll.lat*60+140}),hasLayer:()=>true,remove(){},removeLayer(){}};
 context.L={map:()=>map,control:{scale:()=>({addTo(){}})},tileLayer:()=>({addTo(){return this;}}),geoJSON(data){
  const items=data.features.map(feature=>({feature,on(){return this;},getLatLng:()=>feature.geometry.coordinates,bindTooltip(node,options){bound++;this.label=node.textContent;assert.equal(options.interactive,false);assert.equal(options.permanent,true);return this;},openTooltip(){active.add(this);return this;},unbindTooltip(){active.delete(this);}}));return {eachLayer(fn){scanned++;items.forEach(fn);},addTo(){return this;}};
 }};
 vm.runInNewContext(source,context);const A=context.module.exports;A.init('map',{center:[0,0],zoom:13});
 const features=Array.from({length:40},(_,i)=>({properties:{id:String(i),name:i===0?null:'Carried '+i},geometry:{type:'Point',coordinates:{lng:i%10,lat:Math.floor(i/10)}}}));
 A.addLayer('names',{features},{});A.setLabels('names',{property:'name',minZoom:14,max:40});assert.equal(active.size,0);assert.equal(scanned,0,'no feature scan below label zoom');assert.equal(bound,0,'no tooltip allocation below label zoom');zoom=14;publish();assert.equal(active.size,32);assert.equal(bound,32,'only capped visible labels allocated');assert.ok([...active].every(item=>item.label===item.feature.properties.name));
 zoom=13;publish();assert.equal(active.size,0);zoom=14;publish();assert.equal(active.size,32);A.setLabels('names',null);assert.equal(active.size,0);A.destroy();
});
