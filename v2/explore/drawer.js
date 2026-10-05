(function(scope){
  'use strict';
  function createDrawer(element,opener,closeButton){
    const header=element.querySelector('.explore-heading');let gesture;
    function close(restoreFocus=true){
      if(element.hidden)return;
      element.hidden=true;opener.setAttribute('aria-expanded','false');
      element.dispatchEvent(new CustomEvent('drawerstatechange',{detail:{open:false}}));
      if(restoreFocus)opener.focus();
    }
    function open(){element.hidden=false;opener.setAttribute('aria-expanded','true');element.dispatchEvent(new CustomEvent('drawerstatechange',{detail:{open:true}}));closeButton.focus();}
    const key=event=>{if(event.key==='Escape'&&!element.hidden&&!document.querySelector('dialog[open]')){event.stopPropagation();close();}};
    const toggle=()=>element.hidden?open():close();
    const stop=event=>event.stopPropagation();
    function down(event){if(scope.matchMedia?.('(min-width:768px)').matches||event.target.closest('button'))return;gesture={id:event.pointerId,x:event.clientX,y:event.clientY};header.setPointerCapture?.(event.pointerId);}
    function up(event){if(!gesture||gesture.id!==event.pointerId)return;const {x,y}=gesture;gesture=null;if(event.clientY-y>=32&&event.clientY-y>Math.abs(event.clientX-x)){event.preventDefault();close();}}
    const cancel=()=>{gesture=null;};
    opener.addEventListener('click',toggle);closeButton.addEventListener('click',close);document.addEventListener('keydown',key);
    header.addEventListener('pointerdown',down);header.addEventListener('pointerup',up);header.addEventListener('pointercancel',cancel);
    for(const name of ['pointerdown','touchstart','wheel'])element.addEventListener(name,stop,{passive:true});
    element.hidden=true;
    return {open,close,destroy(){opener.removeEventListener('click',toggle);closeButton.removeEventListener('click',close);document.removeEventListener('keydown',key);header.removeEventListener('pointerdown',down);header.removeEventListener('pointerup',up);header.removeEventListener('pointercancel',cancel);for(const name of ['pointerdown','touchstart','wheel'])element.removeEventListener(name,stop);}};
  }
  const api={createDrawer};if(typeof module!=='undefined')module.exports=api;scope.ExploreDrawer=api;
})(typeof globalThis!=='undefined'?globalThis:this);
