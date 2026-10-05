(function(scope){
  'use strict';
  function createSheet(element,toggle,body){
    let expanded=false;
    function setExpanded(value){
      expanded=value;element.classList.toggle('expanded',value);body.inert=!value;
      toggle.setAttribute('aria-expanded',String(value));toggle.textContent=value?'Collapse':'Results · Expand';
    }
    const click=()=>setExpanded(!expanded);
    const key=event=>{if(event.key==='Escape'&&expanded&&!document.querySelector('dialog[open],.explore-drawer:not([hidden])')){setExpanded(false);toggle.focus();}};
    toggle.addEventListener('click',click);document.addEventListener('keydown',key);
    const stop=event=>event.stopPropagation();
    for(const name of ['pointerdown','touchstart','wheel'])element.addEventListener(name,stop,{passive:true});
    setExpanded(scope.matchMedia?.('(min-width:1200px)').matches===true);
    return {setExpanded,get expanded(){return expanded;},destroy(){toggle.removeEventListener('click',click);document.removeEventListener('keydown',key);for(const name of ['pointerdown','touchstart','wheel'])element.removeEventListener(name,stop);}};
  }
  const api={createSheet};if(typeof module!=='undefined')module.exports=api;scope.ExploreSheet=api;
})(typeof globalThis!=='undefined'?globalThis:this);
