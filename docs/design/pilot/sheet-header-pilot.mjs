// Design-tooling pilot: mobile sheet header, before (main) vs after (PR #39 structure) vs a pilot-only proposal.
// NOT part of run.mjs or CI. Reuses the existing harness's Chrome/CDP helpers.
//
//   node docs/design/pilot/sheet-header-pilot.mjs            # writes screenshots + report here
//   node docs/design/pilot/sheet-header-pilot.mjs --out DIR  # writes to DIR instead (for run-to-run comparison)
//
// Same rules as the harness: local Chrome, a local static server, every
// non-local request blocked. Exit code 1 if a protected-wording check fails.
import {createServer} from 'node:http';
import {createHash} from 'node:crypto';
import {mkdir,mkdtemp,readFile,rm,stat,writeFile} from 'node:fs/promises';
import {spawn} from 'node:child_process';
import {extname,join,normalize,resolve} from 'node:path';
import {tmpdir} from 'node:os';
import {fileURLToPath} from 'node:url';
import {setTimeout as delay} from 'node:timers/promises';
import {cdpClient,waitFor,findChrome,freePort,trackProcess,closeSocket,stopChrome,closeServer} from '../../../v2/pipeline/tests/browser/run.mjs';

const here=fileURLToPath(new URL('.',import.meta.url));
const root=resolve(here,'../../..');
const outFlag=process.argv.indexOf('--out');
const out=resolve(outFlag>0?process.argv[outFlag+1]:here);
const shots=join(out,'screenshots');
const VIEWPORTS=[[390,844],[430,932]],VARIANTS=['before','after','proposal'],STATES={top:0,scrolled:160};
const mime={'.html':'text/html','.js':'text/javascript','.json':'application/json','.css':'text/css','.geojson':'application/geo+json'};

// Runs in the page. Returns geometry, accessibility and wording measurements for the sheet.
const MEASURE=`(()=>{
 const $=id=>document.getElementById('explore-'+id),sheet=$('sheet'),body=$('sheet-body');
 const rect=e=>{const r=e.getBoundingClientRect();return {x:Math.round(r.left),y:Math.round(r.top),w:Math.round(r.width),h:Math.round(r.height)};};
 const parse=c=>{const m=c.match(/[\\d.]+/g).map(Number);return {r:m[0],g:m[1],b:m[2],a:m.length>3?m[3]:1};};
 const lum=({r,g,b})=>{const f=v=>{v/=255;return v<=.03928?v/12.92:((v+.055)/1.055)**2.4;};return .2126*f(r)+.7152*f(g)+.0722*f(b);};
 const background=e=>{for(let n=e;n;n=n.parentElement){const c=parse(getComputedStyle(n).backgroundColor);if(c.a>0)return c;}return {r:255,g:255,b:255,a:1};};
 const ratio=(a,b)=>{const x=lum(a),y=lum(b);return (Math.max(x,y)+.05)/(Math.min(x,y)+.05);};
 // Header rows: what must stay readable and on top.
 const rows=['sheet-toggle','summary','detail-back','detail-title'].map(id=>({id,el:$(id)}));
 const ownership=rows.map(({id,el})=>{const r=el.getBoundingClientRect(),hit=document.elementFromPoint(r.left+r.width/2,r.top+r.height/2);return {id,ownsCentre:!!hit&&(hit===el||el.contains(hit))};});
 // Body content that is painted inside the body's scrollport AND geometrically under a header row.
 const clip=body.getBoundingClientRect(),under=[];
 for(const p of $('detail-body').children){const r=p.getBoundingClientRect(),top=Math.max(r.top,clip.top),bottom=Math.min(r.bottom,clip.bottom);if(bottom<=top)continue;
  for(const {id,el} of rows){const h=el.getBoundingClientRect();if(top<h.bottom-0.5&&bottom>h.top+0.5&&r.left<h.right&&r.right>h.left)under.push({text:p.textContent.slice(0,40),row:id});}}
 const header=document.querySelector('.explore-sheet-head')||document.querySelector('.explore-sheet-header');
 // The summary is trust-bearing ("Closures unconfirmed."); clipping it hides part of the statement.
 const summary=$('summary'),summaryClipped=summary.scrollWidth>summary.clientWidth+1;
 // A visible boundary between the lowest header row and the scrolling body.
 const lowest=document.querySelector('.explore-detail-heading'),separator=parseFloat(getComputedStyle(lowest).borderBottomWidth)>0||parseFloat(getComputedStyle(body).borderTopWidth)>0;
 const headerBottom=Math.max(...rows.map(({el})=>el.getBoundingClientRect().bottom));
 // Contrast of every visible text-bearing element in the sheet.
 const contrast=[];
 for(const e of sheet.querySelectorAll('*')){
  if(![...e.childNodes].some(n=>n.nodeType===3&&n.textContent.trim()))continue;
  const r=e.getBoundingClientRect();if(!r.width||!r.height||r.bottom<=clip.top&&!header.contains(e))continue;
  const s=getComputedStyle(e),size=parseFloat(s.fontSize),bold=Number(s.fontWeight)>=700,large=size>=24||(bold&&size>=18.66);
  const value=Math.round(ratio(parse(s.color),background(e))*100)/100;
  contrast.push({el:e.id||e.tagName.toLowerCase(),text:e.textContent.trim().slice(0,32),fontPx:size,ratio:value,required:large?3:4.5,pass:value>=(large?3:4.5)});
 }
 // Target size (M3 section 11: 44x44 CSS px; inline links in a sentence are exempt).
 const targets=[...sheet.querySelectorAll('button,a,[tabindex]')].filter(e=>e.getBoundingClientRect().width).map(e=>{const r=rect(e);return {el:e.id||e.textContent.trim().slice(0,24),w:r.w,h:r.h,pass:r.w>=44&&r.h>=44};});
 // Protected wording, compared byte-for-byte with the production wording object.
 const W=globalThis.ExploreLand.wording,texts=[...$('detail-body').children].map(n=>n.textContent);
 const wording={W3:texts.includes(W.W3),W7:texts.includes(W.W7),W11:texts.some(t=>/^Source classification: /.test(t)&&W.W11.replace('<code>',t.slice('Source classification: '.length))===t),
  label:$('detail-title').textContent===window.__pilot.detail.title&&texts.includes(window.__pilot.detail.title),closures:$('summary').textContent.endsWith('Closures unconfirmed.')};
 return {variant:window.__pilot.variant,scrollTop:body.scrollTop,bodyTop:Math.round(clip.top),headerBottom:Math.round(headerBottom),bodyStartsBelowHeader:clip.top>=headerBottom-0.5,summaryClipped,separator,
  rows:Object.fromEntries(rows.map(({id,el})=>[id,rect(el)])),ownership,underHeader:under,contrast,targets,wording,detailText:texts.join('\\n')};
})()`;

async function staticServer(){
  const server=createServer(async(request,response)=>{
    try{
      const path=normalize(decodeURIComponent((request.url||'/').split('?')[0])).replace(/^([.][.][/\\])+/,'').replace(/^[/\\]+/,'');
      const file=resolve(root,path);if(!file.startsWith(root+'/'))throw new Error('path outside checkout');
      if(!(await stat(file)).isFile())throw new Error('not a file');
      response.writeHead(200,{'content-type':mime[extname(file)]||'application/octet-stream','cache-control':'no-store'});response.end(await readFile(file));
    }catch(error){response.writeHead(404);response.end(error.message);}
  });
  await new Promise(done=>server.listen(0,'127.0.0.1',done));
  return server;
}

let server,browser,lifecycle,profile,client,pump,running=true,pumpError;
const report={pilot:'sheet-header',note:'Static mockup in headless Chrome. Chrome rendering is not iPhone Safari; real-device validation remains a human gate.',runs:[]};
let failed=false;
try{
  const chrome=await findChrome();report.chrome=chrome.version;
  server=await staticServer();const origin='http://127.0.0.1:'+server.address().port,port=await freePort();
  profile=await mkdtemp(join(tmpdir(),'ohvernight-pilot-'));
  browser=spawn(chrome.candidate,['--headless=new','--no-sandbox','--disable-gpu','--disable-dev-shm-usage','--hide-scrollbars','--remote-debugging-port='+port,'--user-data-dir='+profile,'about:blank'],{stdio:'ignore'});
  lifecycle=trackProcess(browser);
  await waitFor('http://127.0.0.1:'+port+'/json/version',{chrome,processState:()=>lifecycle.state,exitSignal:lifecycle.signal});
  client=cdpClient((await(await fetch('http://127.0.0.1:'+port+'/json/list')).json()).find(target=>target.type==='page').webSocketDebuggerUrl);
  let blocked=0;
  pump=(async()=>{while(running){const event=client.events.shift();if(!event){await delay(5);continue;}
    if(event.method==='Fetch.requestPaused'){const local=new URL(event.params.request.url).origin===origin;if(!local)blocked++;
      try{await client.command(local?'Fetch.continueRequest':'Fetch.failRequest',{requestId:event.params.requestId,...(local?{}:{errorReason:'BlockedByClient'})});}
      catch(error){if(!error.message.includes('Invalid InterceptionId'))throw error;}}}})().catch(error=>{pumpError=error;});
  const evaluate=async expression=>{if(pumpError)throw pumpError;const r=await client.command('Runtime.evaluate',{expression,awaitPromise:true,returnByValue:true});if(r.exceptionDetails)throw new Error(JSON.stringify(r.exceptionDetails));return r.result.value;};
  for(const name of ['Page','Runtime'])await client.command(name+'.enable');
  await client.command('Fetch.enable',{patterns:[{urlPattern:'*',requestStage:'Request'}]});
  await client.command('Emulation.setEmulatedMedia',{features:[{name:'prefers-reduced-motion',value:'reduce'}]});
  await client.command('Emulation.setTouchEmulationEnabled',{enabled:true});
  await mkdir(shots,{recursive:true});
  for(const [width,height] of VIEWPORTS)for(const variant of VARIANTS){
    await client.command('Emulation.setDeviceMetricsOverride',{width,height,deviceScaleFactor:1,mobile:true});
    await client.command('Page.navigate',{url:origin+'/docs/design/pilot/sheet-header-mockup.html?variant='+variant});
    let ready;for(let i=0;i<300&&!(ready=await evaluate('window.__pilot||null').catch(()=>null));i++)await delay(20);
    if(!ready?.ready)throw new Error('mockup did not load: '+JSON.stringify(ready));
    // Focus order: Tab from the document start, recording each focused control and its position.
    await evaluate('document.activeElement?.blur(),window.scrollTo(0,0),true');
    const tabs=[];
    for(let i=0;i<14;i++){
      await client.command('Input.dispatchKeyEvent',{type:'keyDown',key:'Tab',code:'Tab',windowsVirtualKeyCode:9});
      await client.command('Input.dispatchKeyEvent',{type:'keyUp',key:'Tab',code:'Tab',windowsVirtualKeyCode:9});
      tabs.push(await evaluate(`(()=>{const e=document.activeElement,r=e.getBoundingClientRect();return {el:e.id||e.textContent.trim().slice(0,24),y:Math.round(r.top),x:Math.round(r.left),visibleFocus:getComputedStyle(e).outlineStyle!=='none'};})()`));
    }
    await evaluate(`document.getElementById('explore-sheet-body').scrollTop=0,document.activeElement?.blur(),true`);
    const sheetTabs=tabs.filter(t=>['explore-sheet-toggle','explore-detail-back'].includes(t.el)||t.y>=height*.55);
    const visualOrder=sheetTabs.every((t,i)=>i===0||t.y>sheetTabs[i-1].y||(t.y===sheetTabs[i-1].y&&t.x>=sheetTabs[i-1].x)||t.el===sheetTabs[0].el);
    for(const [state,scrollTop] of Object.entries(STATES)){
      await evaluate(`document.getElementById('explore-sheet-body').scrollTop=${scrollTop},new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))`);
      const measured=await evaluate(MEASURE);
      // Screenshot only the defect-relevant state (body scrolled) to keep committed PNGs small.
      // PNG bytes vary slightly run to run (headless rasterisation); the measurements do not.
      const file=state==='scrolled'?`${variant}-${width}x${height}.png`:null;
      if(file)await writeFile(join(shots,file),Buffer.from((await client.command('Page.captureScreenshot',{format:'png'})).data,'base64'));
      const {detailText,...rest}=measured;
      report.runs.push({viewport:`${width}x${height}`,state,...rest,detailTextSha256:createHash('sha256').update(detailText).digest('hex'),
        focusOrder:state==='top'?{sequence:tabs.map(t=>t.el),sheetSequence:sheetTabs.map(t=>t.el),sheetFollowsVisualOrder:visualOrder,allVisible:tabs.every(t=>t.visibleFocus)}:undefined,
        screenshot:file?'screenshots/'+file:undefined});
      if(!Object.values(measured.wording).every(Boolean))failed=true;
    }
  }
  report.blockedNonLocalRequests=blocked;
  const texts=new Set(report.runs.map(run=>run.detailTextSha256));
  report.detailTextIdenticalAcrossVariants=texts.size===1;if(texts.size!==1)failed=true;
  report.summary=Object.fromEntries(VARIANTS.map(variant=>{const runs=report.runs.filter(run=>run.variant===variant);return [variant,{
    bodyStartsBelowHeader:runs.every(r=>r.bodyStartsBelowHeader),headerRowsOwnTheirCentres:runs.every(r=>r.ownership.every(o=>o.ownsCentre)),
    bodyElementsUnderHeaderRows:runs.reduce((n,r)=>n+r.underHeader.length,0),
    summaryClipped:runs.some(r=>r.summaryClipped),headerBodySeparator:runs.every(r=>r.separator),
    minContrast:Math.min(...runs.flatMap(r=>r.contrast.map(c=>c.ratio))),contrastFailures:[...new Set(runs.flatMap(r=>r.contrast.filter(c=>!c.pass).map(c=>`${c.el} "${c.text}" ${c.ratio}:1 @${c.fontPx}px`)))],
    targetFailures:[...new Set(runs.flatMap(r=>r.targets.filter(t=>!t.pass).map(t=>`${t.el} ${t.w}x${t.h}`)))],
    focusFollowsVisualOrder:runs.filter(r=>r.focusOrder).every(r=>r.focusOrder.sheetFollowsVisualOrder),
    protectedWordingIntact:runs.every(r=>Object.values(r.wording).every(Boolean))}];}));
  await writeFile(join(out,'pilot-report.json'),JSON.stringify(report,null,1)+'\n');
  console.log(JSON.stringify({chrome:report.chrome,out,summary:report.summary,detailTextIdenticalAcrossVariants:report.detailTextIdenticalAcrossVariants,blockedNonLocalRequests:blocked},null,1));
  if(failed){console.error('Protected wording check failed');process.exitCode=1;}
}finally{
  running=false;await pump?.catch(()=>{});
  if(client)await closeSocket(client.socket).catch(()=>{});
  if(browser)await stopChrome(browser,lifecycle).catch(()=>{});
  if(server)await closeServer(server).catch(()=>{});
  if(profile)await rm(profile,{recursive:true,force:true,maxRetries:5,retryDelay:100});
}
