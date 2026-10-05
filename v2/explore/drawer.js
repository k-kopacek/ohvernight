(function(scope){
  'use strict';
  function createDrawer(element,opener,closeButton){
    function close(){element.hidden=true;opener.setAttribute('aria-expanded','false');opener.focus();}
    function open(){element.hidden=false;opener.setAttribute('aria-expanded','true');closeButton.focus();}
    const key=event=>{if(event.key==='Escape'&&!element.hidden&&!document.querySelector('dialog[open]')){event.stopPropagation();close();}};
    const toggle=()=>element.hidden?open():close();
    const stop=event=>event.stopPropagation();
    opener.addEventListener('click',toggle);closeButton.addEventListener('click',close);document.addEventListener('keydown',key);
    for(const name of ['pointerdown','touchstart','wheel'])element.addEventListener(name,stop,{passive:true});
    element.hidden=true;
    return {open,close,destroy(){opener.removeEventListener('click',toggle);closeButton.removeEventListener('click',close);document.removeEventListener('keydown',key);for(const name of ['pointerdown','touchstart','wheel'])element.removeEventListener(name,stop);}};
  }
  const api={createDrawer};if(typeof module!=='undefined')module.exports=api;scope.ExploreDrawer=api;
})(typeof globalThis!=='undefined'?globalThis:this);
