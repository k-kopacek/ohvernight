(function(scope){
  'use strict';
  function createDrawer(element,opener,closeButton){
    const header=element.querySelector('.explore-heading'),body=element.querySelector('.explore-drawer-body');let state='dismissed',gestures;
    function close(restoreFocus=true){
      if(element.hidden)return;gestures?.reset();state='dismissed';element.dataset.state=state;element.hidden=true;opener.setAttribute('aria-expanded','false');
      element.dispatchEvent(new CustomEvent('drawerstatechange',{detail:{open:false,state}}));if(restoreFocus)opener.focus();
    }
    function setState(value){
      if(value==='dismissed'){close();return;}if(!['peek','expanded'].includes(value))return;
      state=value;element.dataset.state=value;element.hidden=false;opener.setAttribute('aria-expanded','true');
      element.dispatchEvent(new CustomEvent('drawerstatechange',{detail:{open:true,state}}));
    }
    function open(){gestures.reset();setState('peek');closeButton.focus();}
    const key=event=>{if(event.key==='Escape'&&!element.hidden&&!document.querySelector('dialog[open]')){event.stopPropagation();close();}};
    const toggle=()=>element.hidden?open():close(),headerClick=event=>{if(!event.target.closest('button,a'))gestures.activate(event,()=>setState(state==='peek'?'expanded':'peek'));};
    gestures=scope.ExploreSheet.createPanelGesture(element,header,body,{state:()=>state,setState,
      levels:()=>[{state:'dismissed',height:0},{state:'peek',height:scope.ExploreSheet.panelViewport(element)*.42},{state:'expanded',height:scope.ExploreSheet.panelViewport(element)*.75}],
      enabled:event=>!scope.ExploreSheet.shortLandscape()&&(!scope.matchMedia?.('(min-width:768px)').matches||event.type.startsWith('touch')),ignore:target=>target===closeButton});
    opener.addEventListener('click',toggle);closeButton.addEventListener('click',close);header.addEventListener('click',headerClick);document.addEventListener('keydown',key);element.hidden=true;
    return {open,close,setState,get state(){return state;},destroy(){opener.removeEventListener('click',toggle);closeButton.removeEventListener('click',close);header.removeEventListener('click',headerClick);document.removeEventListener('keydown',key);gestures.destroy();}};
  }
  const api={createDrawer};if(typeof module!=='undefined')module.exports=api;scope.ExploreDrawer=api;
})(typeof globalThis!=='undefined'?globalThis:this);
