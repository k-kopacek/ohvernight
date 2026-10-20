// DIAGNOSTIC ONLY. Never merge. Outcomes are observations, not pass assertions.
import {setTimeout as delay} from 'node:timers/promises';

export async function runLinuxTapDiagnostics(client,origin,evaluate,navigate){
 console.log('TAP_DIAG_ENV '+JSON.stringify(await client.command('Browser.getVersion')));
 const cases=['immediate','slow30','wait350','noPrior'];
 for(let round=0;round<2;round++)for(const region of ['aspen','douglas-co'])for(const variant of cases){
  await client.command('Emulation.setDeviceMetricsOverride',{width:390,height:844,deviceScaleFactor:2,mobile:true});
  await client.command('Emulation.setTouchEmulationEnabled',{enabled:true});
  await navigate(origin+'/v2/?region='+region+'&view=map');
  await evaluate(`(()=>{
   explore.$('map').parentElement.style.setProperty('--test-safe-top','59px');
   explore.$('map').parentElement.style.setProperty('--test-safe-bottom','34px');explore.sheet.setState('half');
  })()`);
  for(const state of ['collapsed','half','expanded','half'])await evaluate(`explore.sheet.setState(${JSON.stringify(state)})`);
  const feature=await evaluate(`(()=>{
   const entry=explore.region.registry.find(e=>e.kind===${JSON.stringify(region==='aspen'?'water':'recreation_sites')}),features=explore.region.layers.get(entry.id).data.features;
   const feature=features.find(f=>/American Lake|Roaring Fork River/.test(f.properties.name))||[...features].sort((a,b)=>JSON.stringify(b.properties).length-JSON.stringify(a.properties).length)[0];
   explore.showDetail(entry,feature);return {id:feature.properties.id,title:feature.properties.name};
  })()`);
  await evaluate(`explore.$('sheet-body').scrollTop=0`);
  await evaluate(`(()=>{const b=explore.$('sheet-body');b.scrollTop=Math.min(200,b.scrollHeight-b.clientHeight)})()`);
  for(const state of ['collapsed','half','expanded','half'])await evaluate(`explore.sheet.setState(${JSON.stringify(state)})`);
  await evaluate(`explore.$('sheet-body').scrollTop=0`);
  await evaluate(`(()=>{const b=explore.$('sheet-body');b.scrollTop=Math.min(200,b.scrollHeight-b.clientHeight)})()`);
  const setup=await evaluate(`(()=>{
   const b=explore.$('sheet-body'),button=explore.$('detail-back'),header=explore.$('sheet-header');b.scrollTop=0;
   ${variant==='touchActionAuto'?"header.style.touchAction='auto';":''}
   const r=button.getBoundingClientRect(),p={x:r.x+r.width/2,y:r.y+r.height/2};
   const name=e=>e?.id||e?.tagName;
   const chain=[];for(let e=button;e;e=e.parentElement){const s=getComputedStyle(e);chain.push({id:name(e),touchAction:s.touchAction,overflowY:s.overflowY,scrollTop:e.scrollTop,scrollHeight:e.scrollHeight,clientHeight:e.clientHeight});}
   const trace=window.__tapDiag={events:[],marks:[],samples:[],longTasks:[],lastScroll:performance.now(),scrollCount:0};
   const types=['touchstart','touchmove','touchend','touchcancel','pointerdown','pointermove','pointerup','pointercancel','mousedown','mouseup','click','scroll','scrollend','gesturetap','gesturetapdown','gesturetapcancel','gesturestart','gestureend','gotpointercapture','lostpointercapture'];
   const record=e=>{if(e.type==='scroll'){trace.lastScroll=performance.now();trace.scrollCount++;}const q=e.changedTouches?.[0]||e;trace.events.push({event:e,at:performance.now(),wall:Date.now(),bodyTop:b.scrollTop,x:q.clientX,y:q.clientY,hit:name(document.elementFromPoint(q.clientX??p.x,q.clientY??p.y))});};
   for(const t of types)document.addEventListener(t,record,{capture:true,passive:true});
   let frame;const sample=()=>{const top=b.scrollTop,last=trace.samples.at(-1);if(!last||top!==last.top)trace.samples.push({at:performance.now(),top});frame=requestAnimationFrame(sample);};sample();
   let observer;try{observer=new PerformanceObserver(list=>trace.longTasks.push(...list.getEntries().map(e=>({start:e.startTime,duration:e.duration}))));observer.observe({type:'longtask',buffered:false});}catch{}
   trace.mark=label=>trace.marks.push({label,at:performance.now(),wall:Date.now(),bodyTop:b.scrollTop,scrollCount:trace.scrollCount,sinceScroll:performance.now()-trace.lastScroll,hit:name(document.elementFromPoint(p.x,p.y)),hidden:explore.$('detail-view').hidden,dragging:explore.$('sheet').classList.contains('is-dragging'),inlineHeight:explore.$('sheet').style.height});
   trace.stop=()=>{cancelAnimationFrame(frame);observer?.disconnect();for(const t of types)document.removeEventListener(t,record,true);};
   trace.mark('setup');return {point:p,chain,body:{top:b.scrollTop,max:b.scrollHeight-b.clientHeight},header:header.getBoundingClientRect().toJSON()};
  })()`);
  const p=setup.point;
  const mark=label=>evaluate(`window.__tapDiag.mark(${JSON.stringify(label)})`);
  const touch=async dy=>{
   await client.command('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:[p]});
   if(dy===30&&variant==='slow30'){
    for(let i=1;i<=5;i++){await delay(80);await client.command('Input.dispatchTouchEvent',{type:'touchMove',touchPoints:[{x:p.x,y:p.y+dy*i/5}]});}
    await mark('slow-move-held');await delay(150);
   }else if(dy!==null)await client.command('Input.dispatchTouchEvent',{type:'touchMove',touchPoints:[{x:p.x,y:p.y+dy}]});
   await client.command('Input.dispatchTouchEvent',{type:'touchEnd',touchPoints:[]});
  };
  const tracing=round===0&&region==='douglas-co'&&['immediate','slow30'].includes(variant);
  if(tracing){client.__tapTrace=[];client.__tapTraceComplete=false;await client.command('Tracing.start',{categories:'input,latencyInfo,benchmark',transferMode:'ReportEvents'});}
  await mark('prior-start');
  if(variant!=='noPrior')await touch(variant==='priorNoMove'?null:30);
  await mark('prior-end');
  if(variant==='idle300')await evaluate(`(async()=>{const t=window.__tapDiag,start=performance.now();while(performance.now()-t.lastScroll<300&&performance.now()-start<2000)await new Promise(r=>setTimeout(r,20));t.mark('idle-complete')})()`);
  if(variant==='wait350')await delay(350);
  if(variant==='wait1500')await delay(1500);
  if(variant==='autoAfterPrior'||variant==='noneAfterAutoPrior')await evaluate(`explore.$('sheet-header').style.touchAction=${JSON.stringify(variant==='autoAfterPrior'?'auto':'none')}`);
  // A prior no-move tap may activate Back; record that outcome and restore detail
  // only for this negative control, without hiding the event from the trace.
  if(variant==='priorNoMove')await evaluate(`(()=>{const t=window.__tapDiag;t.mark('before-restore');const entry=explore.region.registry.find(e=>e.kind===${JSON.stringify(region==='aspen'?'water':'recreation_sites')});explore.showDetail(entry,explore.region.layers.get(entry.id).data.features.find(f=>f.properties.id===${JSON.stringify(feature.id)}));explore.sheet.setState('half');})()`);
  await mark('tap-start');await touch(6);await mark('tap-end-resolved');
  const observed=await evaluate(`(async()=>{
   const t=window.__tapDiag,start=performance.now(),tap=t.marks.find(m=>m.label==='tap-start').at;
   while(!t.events.some(x=>x.at>=tap&&x.event.type==='click')&&performance.now()-start<2000)await new Promise(r=>setTimeout(r,20));
   t.mark('done');t.stop();return {waitedMs:performance.now()-start,hidden:explore.$('detail-view').hidden,state:explore.sheet.state,view:explore.$('sheet').dataset.view,classes:explore.$('sheet').className,active:document.activeElement?.id||document.activeElement?.tagName,
    marks:t.marks,samples:t.samples,longTasks:t.longTasks,events:t.events.map(({event:e,...x})=>({...x,type:e.type,target:e.target.id||e.target.tagName,timeStamp:e.timeStamp,prevented:e.defaultPrevented,cancelable:e.cancelable,pointerType:e.pointerType,detail:e.detail}))};
  })()`);
  console.log('TAP_DIAG '+JSON.stringify({round,region,variant,feature,setup,...observed}));
  if(tracing){
   await client.command('Tracing.end');for(let i=0;i<100&&!client.__tapTraceComplete;i++)await delay(20);
   const events=client.__tapTrace.filter(e=>/Fling|Gesture|TouchAction|TouchEmulator|InputHandler/i.test(e.name));
   console.log('TAP_DIAG_TRACE '+JSON.stringify({region,variant,complete:client.__tapTraceComplete,total:client.__tapTrace.length,events}));
   delete client.__tapTrace;
  }
  if(variant==='thirdTap'){
   await mark('third-tap-start');await touch(6);
   const third=await evaluate(`(async()=>{const start=performance.now();while(!explore.$('detail-view').hidden&&performance.now()-start<2000)await new Promise(r=>setTimeout(r,20));return {hidden:explore.$('detail-view').hidden,waitedMs:performance.now()-start}})()`);
   console.log('TAP_DIAG_THIRD '+JSON.stringify({round,region,...third}));
  }
 }
}
