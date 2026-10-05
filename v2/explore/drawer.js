(function(scope){
  'use strict';
  function createDrawer(element,opener,closeButton){
    const header=element.querySelector('.explore-heading');let gesture;
    const reset=()=>{gesture=null;element.classList.remove('is-dragging');element.style.transform='';};
    function close(restoreFocus=true){
      if(element.hidden)return;reset();element.hidden=true;opener.setAttribute('aria-expanded','false');
      element.dispatchEvent(new CustomEvent('drawerstatechange',{detail:{open:false}}));if(restoreFocus)opener.focus();
    }
    function open(){reset();element.hidden=false;opener.setAttribute('aria-expanded','true');element.dispatchEvent(new CustomEvent('drawerstatechange',{detail:{open:true}}));closeButton.focus();}
    const key=event=>{if(event.key==='Escape'&&!element.hidden&&!document.querySelector('dialog[open]')){event.stopPropagation();close();}};
    const toggle=()=>element.hidden?open():close(),stop=event=>event.stopPropagation();
    function begin(event,point){if(scope.matchMedia?.('(min-width:768px)').matches||event.target.closest('button'))return;gesture={x:point.clientX,y:point.clientY};}
    function move(event,point){if(!gesture)return;const dy=point.clientY-gesture.y;if(dy>0&&dy>Math.abs(point.clientX-gesture.x)){event.preventDefault();element.classList.add('is-dragging');element.style.transform='translateY('+Math.min(dy,element.getBoundingClientRect().height)+'px)';}}
    function end(event,point){if(!gesture)return;const {x,y}=gesture;if(point.clientY-y>=32&&point.clientY-y>Math.abs(point.clientX-x)){event.preventDefault();close();}else reset();}
    const pd=event=>{if(event.pointerType!=='touch'){begin(event,event);if(gesture)header.setPointerCapture?.(event.pointerId);}},pm=event=>{if(event.pointerType!=='touch')move(event,event);},pu=event=>{if(event.pointerType!=='touch')end(event,event);};
    const td=event=>{if(event.touches.length===1)begin(event,event.touches[0]);},tm=event=>{if(event.touches.length===1)move(event,event.touches[0]);},tu=event=>{if(event.changedTouches.length)end(event,event.changedTouches[0]);};
    const bindings=[['pointerdown',pd],['pointermove',pm],['pointerup',pu],['touchstart',td],['touchmove',tm],['touchend',tu],['touchcancel',reset]];
    opener.addEventListener('click',toggle);closeButton.addEventListener('click',close);document.addEventListener('keydown',key);
    for(const [name,handler] of bindings)header.addEventListener(name,handler,{passive:name==='touchstart'});
    for(const name of ['pointerdown','touchstart','wheel'])element.addEventListener(name,stop,{passive:true});element.hidden=true;
    return {open,close,destroy(){opener.removeEventListener('click',toggle);closeButton.removeEventListener('click',close);document.removeEventListener('keydown',key);for(const [name,handler] of bindings)header.removeEventListener(name,handler);for(const name of ['pointerdown','touchstart','wheel'])element.removeEventListener(name,stop);}};
  }
  const api={createDrawer};if(typeof module!=='undefined')module.exports=api;scope.ExploreDrawer=api;
})(typeof globalThis!=='undefined'?globalThis:this);
