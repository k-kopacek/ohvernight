const {test}=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const root=path.resolve(__dirname,'../..'),source=fs.readFileSync(path.join(root,'explore/map-adapter.js'),'utf8');
const names=['init','addLayer','removeLayer','setVisible','setStyle','setPins','onFeature','fit','setBasemap','destroy'];
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
