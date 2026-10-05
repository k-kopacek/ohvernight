(function(scope){
  'use strict';
  const states=['collapsed','half','expanded'];
  const shortLandscape=()=>scope.matchMedia?.('(orientation:landscape) and (max-height:500px)').matches===true;
  function panelViewport(element){const style=scope.getComputedStyle?.(element);return Math.max(0,(scope.visualViewport?.height||scope.innerHeight)-(parseFloat(style?.getPropertyValue('--safe-top'))||0)-(parseFloat(style?.getPropertyValue('--safe-bottom'))||0));}
  function nextState(state,direction){return states[Math.max(0,Math.min(2,states.indexOf(state)+direction))];}
  function snapPanelState(height,start,delta,velocity,levels){
    const index=levels.findIndex(level=>level.state===start),range=levels.at(-1).height-levels[0].height;
    if(Math.abs(velocity)>.45&&Math.abs(delta)<range*.5)return levels[Math.max(0,Math.min(levels.length-1,index+(delta<0?1:-1)))].state;
    return levels[levels.reduce((best,value,i)=>Math.abs(value.height-height)<Math.abs(levels[best].height-height)?i:best,0)].state;
  }
  function snapState(height,start,delta,velocity,viewport){
    return snapPanelState(height,start,delta,velocity,states.map((state,i)=>({state,height:[64,viewport*.4,viewport*.75][i]})));
  }
  // One TouchEvent path preserves Safari scroll/drag arbitration for both panels.
  function createPanelGesture(element,header,body,options){
    let gesture,suppressClick=0;
    function begin(event,point){
      if(!options.enabled(event)||event.button>0||options.ignore?.(event.target))return;
      const onHeader=header.contains(event.target),start=options.state();
      if(!onHeader&&(start===options.levels()[0].state||body.scrollTop>0||event.target.closest('button,a,input,select,textarea,summary')))return;
      suppressClick=0;gesture={x:point.clientX,y:point.clientY,height:element.getBoundingClientRect().height,start,onHeader,time:event.timeStamp,lastY:point.clientY,lastTime:event.timeStamp,velocity:0,dragging:false};
    }
    function move(event,point){
      if(!gesture)return;const delta=point.clientY-gesture.y;
      if(!gesture.onHeader&&!gesture.dragging&&(delta<=0||body.scrollTop>0))return;
      if(Math.abs(delta)<4&&!gesture.dragging)return;
      if(Math.abs(delta)<Math.abs(point.clientX-gesture.x)&&!gesture.dragging){gesture=null;return;}
      event.preventDefault();gesture.dragging=true;
      const dt=event.timeStamp-gesture.lastTime;if(dt>0)gesture.velocity=(point.clientY-gesture.lastY)/dt;
      gesture.lastY=point.clientY;gesture.lastTime=event.timeStamp;
      const levels=options.levels();element.classList.add('is-dragging');element.style.height=Math.max(levels[0].height,Math.min(levels.at(-1).height,gesture.height-delta))+'px';
    }
    function end(event,point){
      if(!gesture)return;const g=gesture;gesture=null;if(!g.dragging)return;
      const delta=point.clientY-g.y,dt=event.timeStamp-g.time,velocity=dt>0&&dt<160?delta/dt:event.timeStamp-g.lastTime<=100?g.velocity:0;
      event.preventDefault();suppressClick=g.onHeader?event.timeStamp+350:0;
      options.setState(snapPanelState(parseFloat(element.style.height),g.start,delta,velocity,options.levels()));reset();
    }
    function reset(){gesture=null;element.classList.remove('is-dragging');element.style.height='';}
    const pd=event=>{if(event.pointerType==='touch')return;begin(event,event);if(gesture)header.setPointerCapture?.(event.pointerId);};
    const pm=event=>{if(event.pointerType!=='touch')move(event,event);},pu=event=>{if(event.pointerType!=='touch')end(event,event);},pc=event=>{if(event.pointerType!=='touch')reset();};
    const td=event=>{if(event.touches.length===1)begin(event,event.touches[0]);else reset();};
    const tm=event=>{if(event.touches.length===1)move(event,event.touches[0]);else reset();},tu=event=>{if(event.changedTouches.length)end(event,event.changedTouches[0]);};
    const bindings=[['pointerdown',pd],['pointermove',pm],['pointerup',pu],['pointercancel',pc],['touchstart',td],['touchmove',tm],['touchend',tu],['touchcancel',reset]];
    for(const [name,handler] of bindings)element.addEventListener(name,handler,{passive:name==='touchstart'});
    scope.addEventListener?.('resize',reset);scope.addEventListener?.('orientationchange',reset);
    const stop=event=>event.stopPropagation();for(const name of ['pointerdown','touchstart','wheel'])element.addEventListener(name,stop,{passive:true});
    return {reset,activate(event,fn){if(event.detail!==0&&event.timeStamp<=suppressClick){suppressClick=0;return;}fn();},destroy(){reset();scope.removeEventListener?.('resize',reset);scope.removeEventListener?.('orientationchange',reset);for(const [name,handler] of bindings)element.removeEventListener(name,handler);for(const name of ['pointerdown','touchstart','wheel'])element.removeEventListener(name,stop);}};
  }
  function createSheet(element,toggle,body){
    let state='collapsed';
    const header=element.querySelector('.explore-sheet-header'),phone=()=>!scope.matchMedia?.('(min-width:768px)').matches;
    function setState(value){
      if(!states.includes(value))return;
      state=value;element.dataset.state=value;element.classList.toggle('expanded',value!=='collapsed');body.inert=value==='collapsed';
      toggle.setAttribute('aria-expanded',String(value!=='collapsed'));
      toggle.textContent=value==='collapsed'?'Results · Expand':'Results · '+(value==='half'&&phone()&&!shortLandscape()?'Expand':'Collapse');
      element.dispatchEvent(new CustomEvent('sheetstatechange',{detail:{state:value}}));
    }
    const cycle=()=>setState(phone()&&!shortLandscape()?states[(states.indexOf(state)+1)%states.length]:state==='collapsed'?'expanded':'collapsed');
    const click=event=>gestures.activate(event,cycle);
    const key=event=>{if(event.key==='Escape'&&state!=='collapsed'&&!document.querySelector('dialog[open],.explore-drawer:not([hidden])')){setState('collapsed');toggle.focus();}};
    const gestures=createPanelGesture(element,header,body,{state:()=>state,setState,
      levels:()=>states.map((state,i)=>({state,height:[64,panelViewport(element)*.4,panelViewport(element)*.75][i]})),
      enabled:event=>!shortLandscape()&&(phone()||event.type.startsWith('touch'))});
    toggle.addEventListener('click',click);document.addEventListener('keydown',key);
    setState(scope.matchMedia?.('(min-width:1200px)').matches===true?'expanded':'collapsed');
    return {setState,setExpanded(value){setState(value?'expanded':'collapsed');},get state(){return state;},get expanded(){return state!=='collapsed';},destroy(){toggle.removeEventListener('click',click);document.removeEventListener('keydown',key);gestures.destroy();}};
  }
  const api={createSheet,nextState,snapState,createPanelGesture,snapPanelState,panelViewport,shortLandscape};if(typeof module!=='undefined')module.exports=api;scope.ExploreSheet=api;
})(typeof globalThis!=='undefined'?globalThis:this);
