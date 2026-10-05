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
  constructor(){super();this.dataset={};this.attrs={};this.classList={toggle(){}};}
  setAttribute(k,v){this.attrs[k]=v;}focus(){this.focused=true;}
  contains(e){return e===this;}querySelector(){return header;}
 }
 const element=new Node(),toggle=new Node(),body=new Node(),header=new Node(),doc=new Node();
 body.scrollTop=0;doc.querySelector=()=>null;
 const context={module:{exports:{}},document:doc,CustomEvent,matchMedia:()=>({matches:false})};
 vm.runInNewContext(fs.readFileSync(require.resolve('../../explore/sheet.js'),'utf8'),context);
 const sheet=context.module.exports.createSheet(element,toggle,body);
 const pointer=(type,y)=>{const e=new Event(type,{cancelable:true});Object.assign(e,{pointerId:1,clientX:10,clientY:y,button:0});Object.defineProperty(e,'target',{value:header});element.dispatchEvent(e);return e;};
 assert.equal(sheet.state,'collapsed');assert.equal(body.inert,true);
 pointer('pointerdown',100);const end=pointer('pointerup',40);
 assert.equal(sheet.state,'half');assert.equal(end.defaultPrevented,true);assert.equal(body.inert,false);
 toggle.dispatchEvent(new Event('click'));assert.equal(sheet.state,'half','swipe suppresses its click');
 toggle.dispatchEvent(new Event('click'));assert.equal(sheet.state,'expanded');
 const escape=new Event('keydown');escape.key='Escape';doc.dispatchEvent(escape);
 assert.equal(sheet.state,'collapsed');assert.equal(body.inert,true);assert.equal(toggle.focused,true);
 sheet.destroy();toggle.dispatchEvent(new Event('click'));assert.equal(sheet.state,'collapsed');
});
