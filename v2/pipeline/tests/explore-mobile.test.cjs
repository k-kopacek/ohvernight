const {test}=require('node:test'),assert=require('node:assert/strict');
const Sheet=require('../../explore/sheet.js');
test('A11 sheet snaps through three states and clamps swipe endpoints',()=>{
 assert.equal(Sheet.nextState('collapsed',1),'half');
 assert.equal(Sheet.nextState('half',1),'expanded');
 assert.equal(Sheet.nextState('expanded',1),'expanded');
 assert.equal(Sheet.nextState('expanded',-1),'half');
 assert.equal(Sheet.nextState('half',-1),'collapsed');
 assert.equal(Sheet.nextState('collapsed',-1),'collapsed');
});
test('A11 sheet gestures, handle activation and Escape preserve inertness and map isolation',()=>{
 const fs=require('node:fs'),vm=require('node:vm');
 class Node extends EventTarget{
  constructor(){super();this.dataset={};this.attrs={};this.style={};this.classList={toggle(){},add(){},remove(){}};}
  setAttribute(k,v){this.attrs[k]=v;}focus(){this.focused=true;}
  contains(e){return e===this;}querySelector(){return header;}getBoundingClientRect(){return {height:this.style.height?parseFloat(this.style.height):this.dataset.state==='expanded'?450:this.dataset.state==='half'?240:64};}
 }
 const element=new Node(),toggle=new Node(),body=new Node(),header=new Node(),doc=new Node();
 body.scrollTop=0;doc.querySelector=()=>null;
 const context={module:{exports:{}},document:doc,CustomEvent,innerHeight:600,matchMedia:()=>({matches:false})};
 vm.runInNewContext(fs.readFileSync(require.resolve('../../explore/sheet.js'),'utf8'),context);
 const sheet=context.module.exports.createSheet(element,toggle,body);
 const pointer=(type,y)=>{const e=new Event(type,{cancelable:true});Object.assign(e,{pointerId:1,clientX:10,clientY:y,button:0});Object.defineProperty(e,'target',{value:header});element.dispatchEvent(e);return e;};
 assert.equal(sheet.state,'collapsed');assert.equal(body.inert,true);
 pointer('pointerdown',100);pointer('pointermove',40);const end=pointer('pointerup',40);
 assert.equal(sheet.state,'half');assert.equal(end.defaultPrevented,true);assert.equal(body.inert,false);
 toggle.dispatchEvent(new Event('click'));assert.equal(sheet.state,'half','swipe suppresses its click');
 toggle.dispatchEvent(new Event('click'));assert.equal(sheet.state,'expanded');
 const escape=new Event('keydown');escape.key='Escape';doc.dispatchEvent(escape);
 assert.equal(sheet.state,'collapsed');assert.equal(body.inert,true);assert.equal(toggle.focused,true);
 sheet.destroy();toggle.dispatchEvent(new Event('click'));assert.equal(sheet.state,'collapsed');
});
test('A11 drawer swipe and Escape dismiss non-modally and return focus',()=>{
 const fs=require('node:fs'),vm=require('node:vm');
 class Node extends EventTarget{constructor(){super();this.dataset={};this.attrs={};this.style={};this.classList={add(){},remove(){}};}contains(e){return e===this;}closest(){return null;}getBoundingClientRect(){return {height:250};}setAttribute(k,v){this.attrs[k]=v;}focus(){this.focused=true;}}
 const element=new Node(),opener=new Node(),closeButton=new Node(),header=new Node(),doc=new Node();element.querySelector=()=>header;doc.querySelector=()=>null;
 const context={module:{exports:{}},document:doc,CustomEvent,innerHeight:600,matchMedia:()=>({matches:false})};vm.runInNewContext(fs.readFileSync(require.resolve('../../explore/sheet.js'),'utf8'),context);vm.runInNewContext(fs.readFileSync(require.resolve('../../explore/drawer.js'),'utf8'),context);
 const drawer=context.module.exports.createDrawer(element,opener,closeButton);assert.equal(element.hidden,true);
 drawer.open();assert.equal(element.hidden,false);assert.equal(closeButton.focused,true);assert.equal(opener.attrs['aria-expanded'],'true');
 const pointer=(type,y)=>{const e=new Event(type,{cancelable:true});Object.assign(e,{pointerId:1,clientX:10,clientY:y});Object.defineProperty(e,'target',{value:header});element.dispatchEvent(e);};
 pointer('pointerdown',20);pointer('pointermove',80);pointer('pointerup',80);assert.equal(element.hidden,true);assert.equal(opener.focused,true);
 opener.focused=false;drawer.open();drawer.close(false);assert.equal(opener.focused,false,'sheet opening does not steal handle focus');
 drawer.open();const escape=new Event('keydown');escape.key='Escape';doc.dispatchEvent(escape);assert.equal(element.hidden,true);assert.equal(opener.focused,true);
 drawer.destroy();opener.dispatchEvent(new Event('click'));assert.equal(element.hidden,true);
});

test('A11 slow drags choose nearest state; short flicks advance one; long drags can skip half',()=>{
 assert.equal(Sheet.snapState(250,'collapsed',-186,-.2,600),'half');
 assert.equal(Sheet.snapState(420,'collapsed',-356,-1,600),'expanded');
 assert.equal(Sheet.snapState(100,'collapsed',-36,-1,600),'half');
 assert.equal(Sheet.snapState(210,'half',30,1,600),'collapsed');
 assert.equal(Sheet.snapState(430,'expanded',20,.1,600),'expanded');
});

test('review fix 1: shared gestures use controlled 160/100 ms and velocity boundaries',()=>{
 const fs=require('node:fs'),vm=require('node:vm');
 function stateAfterRelease(time){
  let header;class Node extends EventTarget{constructor(){super();this.dataset={};this.attrs={};this.style={};this.classList={toggle(){},add(){},remove(){}};}contains(e){return e===this;}closest(){return null;}setAttribute(k,v){this.attrs[k]=v;}querySelector(){return header;}getBoundingClientRect(){return {height:this.style.height?parseFloat(this.style.height):64};}}
  const element=new Node(),toggle=new Node(),body=new Node(),doc=new Node();header=new Node();body.scrollTop=0;doc.querySelector=()=>null;
  const context={module:{exports:{}},document:doc,CustomEvent,innerHeight:600,matchMedia:()=>({matches:false})};vm.runInNewContext(fs.readFileSync(require.resolve('../../explore/sheet.js'),'utf8'),context);const sheet=context.module.exports.createSheet(element,toggle,body);
  for(const [type,y,timestamp] of [['touchstart',400,0],['touchmove',364,70],['touchend',364,time]]){const e=new Event(type,{cancelable:true});Object.defineProperty(e,'target',{value:header});Object.defineProperty(e,'timeStamp',{value:timestamp});e.touches=type==='touchend'?[]:[{clientX:30,clientY:y}];e.changedTouches=[{clientX:30,clientY:y}];element.dispatchEvent(e);}
  const state=sheet.state;sheet.destroy();return state;
 }
 assert.equal(stateAfterRelease(159),'collapsed','under 160 ms uses whole-gesture velocity');
 assert.equal(stateAfterRelease(160),'half','at 160 ms uses recent segment velocity');
 assert.equal(stateAfterRelease(170),'half','recent segment remains eligible at exactly 100 ms');
 assert.equal(stateAfterRelease(171),'collapsed','after 100 ms the segment velocity expires');
 assert.equal(Sheet.snapState(100,'collapsed',-36,-.45,600),'collapsed');assert.equal(Sheet.snapState(100,'collapsed',-36,-.4501,600),'half');
});

test('A12 tablet touch drag follows the finger and snaps half; mouse title toggle stays available',()=>{
 const fs=require('node:fs'),vm=require('node:vm');let header;
 class Node extends EventTarget{
  constructor(){super();this.dataset={};this.attrs={};this.style={};this.classList={toggle(){},add(){},remove(){}};}
  setAttribute(k,v){this.attrs[k]=v;}focus(){}contains(e){return e===this;}querySelector(){return header;}
  getBoundingClientRect(){return {height:this.style.height?parseFloat(this.style.height):this.dataset.state==='half'?409.6:this.dataset.state==='expanded'?768:64};}
 }
 const element=new Node(),toggle=new Node(),body=new Node(),doc=new Node();header=new Node();body.scrollTop=0;doc.querySelector=()=>null;
 const context={module:{exports:{}},document:doc,CustomEvent,innerHeight:1024,matchMedia:q=>({matches:q==='(min-width:768px)'})};
 vm.runInNewContext(fs.readFileSync(require.resolve('../../explore/sheet.js'),'utf8'),context);
 const sheet=context.module.exports.createSheet(element,toggle,body);
 function touch(type,y,time){const e=new Event(type,{cancelable:true});Object.defineProperty(e,'target',{value:header});Object.defineProperty(e,'timeStamp',{value:time});e.touches=type==='touchend'?[]:[{clientX:30,clientY:y}];e.changedTouches=[{clientX:30,clientY:y}];element.dispatchEvent(e);return e;}
 touch('touchstart',900,0);const cancel=new Event('pointercancel');cancel.pointerType='touch';element.dispatchEvent(cancel);touch('touchmove',700,200);assert.equal(parseFloat(element.style.height),264,'intermediate follows finger');touch('touchmove',550,400);touch('touchend',550,420);
 assert.equal(sheet.state,'half');assert.equal(body.inert,false);assert.equal(element.style.height,'');
 const click=new Event('click');Object.defineProperty(click,'timeStamp',{value:1000});Object.defineProperty(click,'detail',{value:1});toggle.dispatchEvent(click);assert.equal(sheet.state,'collapsed','mouse click toggle remains');sheet.destroy();
});

 test('A12 shared drawer levels snap expanded to peek, peek to dismissal, and slow drag to the nearest height',()=>{
 const levels=[{state:'dismissed',height:0},{state:'peek',height:252},{state:'expanded',height:450}];
 assert.equal(Sheet.snapPanelState(312,'peek',-60,-1,levels),'expanded');
 assert.equal(Sheet.snapPanelState(390,'expanded',60,1,levels),'peek');
 assert.equal(Sheet.snapPanelState(192,'peek',60,1,levels),'dismissed');
 assert.equal(Sheet.snapPanelState(390,'peek',-138,-.2,levels),'expanded');
 assert.equal(Sheet.snapPanelState(260,'expanded',190,.2,levels),'peek');
 });

test('A12 panel heights use the visible viewport and top/bottom safe areas',()=>{
 const fs=require('node:fs'),vm=require('node:vm'),context={module:{exports:{}},innerHeight:900,visualViewport:{height:820},getComputedStyle:()=>({getPropertyValue:name=>name==='--safe-top'?'30px':'10px'})};
 vm.runInNewContext(fs.readFileSync(require.resolve('../../explore/sheet.js'),'utf8'),context);
 assert.equal(context.module.exports.panelViewport({}),780);
 context.visualViewport.height=700;assert.equal(context.module.exports.panelViewport({}),660);
});

test('A12 short landscape disables height dragging and keeps an open/collapse title action',()=>{
 const fs=require('node:fs'),vm=require('node:vm');let header;
 class Node extends EventTarget{constructor(){super();this.dataset={};this.attrs={};this.style={};this.classList={toggle(){},add(){},remove(){}};}setAttribute(k,v){this.attrs[k]=v;}focus(){}contains(e){return e===this;}querySelector(){return header;}getBoundingClientRect(){return {height:64};}}
 const element=new Node(),toggle=new Node(),body=new Node(),doc=new Node();header=new Node();body.scrollTop=0;doc.querySelector=()=>null;
 const context={module:{exports:{}},document:doc,CustomEvent,innerHeight:375,matchMedia:q=>({matches:q==='(orientation:landscape) and (max-height:500px)'})};vm.runInNewContext(fs.readFileSync(require.resolve('../../explore/sheet.js'),'utf8'),context);const sheet=context.module.exports.createSheet(element,toggle,body);
 for(const [type,y] of [['touchstart',300],['touchmove',200],['touchend',200]]){const e=new Event(type,{cancelable:true});Object.defineProperty(e,'target',{value:header});e.touches=type==='touchend'?[]:[{clientX:30,clientY:y}];e.changedTouches=[{clientX:30,clientY:y}];element.dispatchEvent(e);}
 assert.equal(sheet.state,'collapsed');assert.equal(element.style.height,undefined);const click=new Event('click');click.detail=0;toggle.dispatchEvent(click);assert.equal(sheet.state,'expanded');toggle.dispatchEvent(click);assert.equal(sheet.state,'collapsed');sheet.destroy();
});
