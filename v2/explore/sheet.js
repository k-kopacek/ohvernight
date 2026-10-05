(function(scope){
  'use strict';
  const states=['collapsed','half','expanded'];
  function nextState(state,direction){return states[Math.max(0,Math.min(2,states.indexOf(state)+direction))];}
  function snapState(height,start,delta,velocity,viewport){
    const heights=[64,viewport*.4,viewport*.75];
    if(Math.abs(velocity)>.45&&Math.abs(delta)<(heights[2]-heights[0])*.5)return nextState(start,delta<0?1:-1);
    return states[heights.reduce((best,value,i)=>Math.abs(value-height)<Math.abs(heights[best]-height)?i:best,0)];
  }
  function createSheet(element,toggle,body){
    let state='collapsed',gesture,suppressClick=0;
    const header=element.querySelector('.explore-sheet-header'),phone=()=>!scope.matchMedia?.('(min-width:768px)').matches;
    function setState(value){
      if(!states.includes(value))return;
      state=value;element.dataset.state=value;element.classList.toggle('expanded',value!=='collapsed');body.inert=value==='collapsed';
      toggle.setAttribute('aria-expanded',String(value!=='collapsed'));
      toggle.textContent=value==='collapsed'?'Results · Expand':'Results · '+(value==='half'?'Expand':'Collapse');
      element.dispatchEvent(new CustomEvent('sheetstatechange',{detail:{state:value}}));
    }
    const cycle=()=>setState(phone()?states[(states.indexOf(state)+1)%states.length]:state==='collapsed'?'expanded':'collapsed');
    const click=event=>{if(event.detail!==0&&event.timeStamp<=suppressClick){suppressClick=0;return;}cycle();};
    const key=event=>{if(event.key==='Escape'&&state!=='collapsed'&&!document.querySelector('dialog[open],.explore-drawer:not([hidden])')){setState('collapsed');toggle.focus();}};
    function begin(event,point){
      if((!phone()&&!event.type.startsWith('touch'))||event.button>0)return;
      const onHeader=header.contains(event.target);
      if(!onHeader&&(state==='collapsed'||body.scrollTop>0||event.target.closest('button,a,input,select,textarea')))return;
      suppressClick=0;gesture={x:point.clientX,y:point.clientY,height:element.getBoundingClientRect().height,start:state,onHeader,time:event.timeStamp,lastY:point.clientY,lastTime:event.timeStamp,velocity:0,dragging:false};
    }
    function move(event,point){
      if(!gesture)return;
      const delta=point.clientY-gesture.y;
      if(!gesture.onHeader&&!gesture.dragging&&(delta<=0||body.scrollTop>0))return;
      if(Math.abs(delta)<4&&!gesture.dragging)return;
      if(Math.abs(delta)<Math.abs(point.clientX-gesture.x)&&!gesture.dragging){gesture=null;return;}
      event.preventDefault();gesture.dragging=true;
      const dt=event.timeStamp-gesture.lastTime;if(dt>0)gesture.velocity=(point.clientY-gesture.lastY)/dt;
      gesture.lastY=point.clientY;gesture.lastTime=event.timeStamp;
      element.classList.add('is-dragging');element.style.height=Math.max(64,Math.min(scope.innerHeight*.75,gesture.height-delta))+'px';
    }
    function end(event,point){
      if(!gesture)return;const g=gesture;gesture=null;
      if(!g.dragging)return;
      const delta=point.clientY-g.y,dt=event.timeStamp-g.time;
      const velocity=dt>0&&dt<160?delta/dt:event.timeStamp-g.lastTime<=100?g.velocity:0;
      event.preventDefault();suppressClick=g.onHeader?event.timeStamp+350:0;
      const height=parseFloat(element.style.height);
      setState(snapState(height,g.start,delta,velocity,scope.innerHeight));
      element.classList.remove('is-dragging');element.style.height='';
    }
    const cancel=()=>{gesture=null;element.classList.remove('is-dragging');element.style.height='';};
    const pointerDown=event=>{if(event.pointerType==='touch')return;begin(event,event);if(gesture)header.setPointerCapture?.(event.pointerId);};
    const pointerMove=event=>{if(event.pointerType!=='touch')move(event,event);};
    const pointerUp=event=>{if(event.pointerType!=='touch')end(event,event);};
    const touchDown=event=>{if(event.touches.length===1)begin(event,event.touches[0]);else cancel();};
    const touchMove=event=>{if(event.touches.length===1)move(event,event.touches[0]);};
    const touchUp=event=>{if(event.changedTouches.length)end(event,event.changedTouches[0]);};
    toggle.addEventListener('click',click);document.addEventListener('keydown',key);
    const bindings=[['pointerdown',pointerDown],['pointermove',pointerMove],['pointerup',pointerUp],['touchstart',touchDown],['touchmove',touchMove],['touchend',touchUp],['touchcancel',cancel]];
    for(const [name,handler] of bindings)element.addEventListener(name,handler,{passive:name==='touchstart'});
    const stop=event=>event.stopPropagation();for(const name of ['pointerdown','touchstart','wheel'])element.addEventListener(name,stop,{passive:true});
    setState(scope.matchMedia?.('(min-width:1200px)').matches===true?'expanded':'collapsed');
    return {setState,setExpanded(value){setState(value?'expanded':'collapsed');},get state(){return state;},get expanded(){return state!=='collapsed';},destroy(){toggle.removeEventListener('click',click);document.removeEventListener('keydown',key);for(const [name,handler] of bindings)element.removeEventListener(name,handler);for(const name of ['pointerdown','touchstart','wheel'])element.removeEventListener(name,stop);}};
  }
  const api={createSheet,nextState,snapState};if(typeof module!=='undefined')module.exports=api;scope.ExploreSheet=api;
})(typeof globalThis!=='undefined'?globalThis:this);
