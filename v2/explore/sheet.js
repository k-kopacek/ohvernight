(function(scope){
  'use strict';
  const states=['collapsed','half','expanded'];
  function nextState(state,direction){return states[Math.max(0,Math.min(2,states.indexOf(state)+direction))];}
  function createSheet(element,toggle,body){
    let state='collapsed',gesture,suppressClick=false;
    const header=element.querySelector('.explore-sheet-header'),phone=()=>!scope.matchMedia?.('(min-width:768px)').matches;
    function setState(value){
      if(!states.includes(value))return;
      state=value;element.dataset.state=value;element.classList.toggle('expanded',value!=='collapsed');body.inert=value==='collapsed';
      toggle.setAttribute('aria-expanded',String(value!=='collapsed'));
      toggle.textContent=value==='collapsed'?'Results · Expand':'Results · '+(value==='half'?'Expand':'Collapse');
      element.dispatchEvent(new CustomEvent('sheetstatechange',{detail:{state:value}}));
    }
    const cycle=()=>setState(states[(states.indexOf(state)+1)%states.length]);
    const click=()=>{if(suppressClick){suppressClick=false;return;}cycle();};
    const key=event=>{if(event.key==='Escape'&&state!=='collapsed'&&!document.querySelector('dialog[open],.explore-drawer:not([hidden])')){setState('collapsed');toggle.focus();}};
    function down(event){
      if(!phone()||event.button>0)return;
      const onHeader=header.contains(event.target);
      if(!onHeader&&(state!=='expanded'||body.scrollTop>0||event.target.closest('button,a,input,select,textarea')))return;
      gesture={id:event.pointerId,x:event.clientX,y:event.clientY,onHeader};
      if(onHeader)header.setPointerCapture?.(event.pointerId);
    }
    function move(event){
      if(!gesture||gesture.id!==event.pointerId)return;
      if(gesture.onHeader)event.preventDefault();
    }
    function up(event){
      if(!gesture||gesture.id!==event.pointerId)return;
      const {x,y,onHeader}=gesture;gesture=null;
      const delta=event.clientY-y;
      if(Math.abs(delta)<32||Math.abs(delta)<Math.abs(event.clientX-x)||(!onHeader&&delta<0))return;
      event.preventDefault();suppressClick=onHeader;setState(nextState(state,delta<0?1:-1));
    }
    const cancel=()=>{gesture=null;};
    toggle.addEventListener('click',click);document.addEventListener('keydown',key);
    element.addEventListener('pointerdown',down);element.addEventListener('pointermove',move);element.addEventListener('pointerup',up);element.addEventListener('pointercancel',cancel);
    const stop=event=>event.stopPropagation();
    for(const name of ['pointerdown','touchstart','wheel'])element.addEventListener(name,stop,{passive:true});
    setState(scope.matchMedia?.('(min-width:1200px)').matches===true?'expanded':'collapsed');
    return {setState,setExpanded(value){setState(value?'expanded':'collapsed');},get state(){return state;},get expanded(){return state!=='collapsed';},destroy(){toggle.removeEventListener('click',click);document.removeEventListener('keydown',key);element.removeEventListener('pointerdown',down);element.removeEventListener('pointermove',move);element.removeEventListener('pointerup',up);element.removeEventListener('pointercancel',cancel);for(const name of ['pointerdown','touchstart','wheel'])element.removeEventListener(name,stop);}};
  }
  const api={createSheet,nextState};if(typeof module!=='undefined')module.exports=api;scope.ExploreSheet=api;
})(typeof globalThis!=='undefined'?globalThis:this);
