// One offline session: base 3dc0fef and working head, five runs each, 390×844, CPU 4×.
import {spawn,execFileSync} from 'node:child_process';
import {createServer} from 'node:http';
import {readFile,mkdtemp,rm} from 'node:fs/promises';
import {resolve,join,extname} from 'node:path';
import {tmpdir} from 'node:os';
import {fileURLToPath} from 'node:url';
import {setTimeout as delay} from 'node:timers/promises';
import {cdpClient,waitFor,findChrome,freePort,trackProcess,closeSocket,stopChrome,closeServer} from './run.mjs';
const root=resolve(fileURLToPath(new URL('../../../../',import.meta.url))),cache=new Map();
const types={'.html':'text/html','.js':'text/javascript','.json':'application/json','.geojson':'application/json','.css':'text/css','.svg':'image/svg+xml','.png':'image/png'};
async function content(version,path){
 if(path.includes('..'))throw Error('invalid path');if(path.endsWith('/'))path+='index.html';
 if(version==='head')return readFile(resolve(root,path));
 if(!cache.has(path))cache.set(path,execFileSync('git',['show','3dc0fef:'+path],{cwd:root,maxBuffer:32*1024*1024}));return cache.get(path);
}
let server,browser,lifecycle,profile,client,pump,running=true,pumpError;
const rows=[];
try{
 const chrome=await findChrome();server=createServer(async(req,res)=>{try{const u=new URL(req.url,'http://local'),parts=u.pathname.slice(1).split('/'),version=parts.shift(),path=parts.join('/');if(!['base','head'].includes(version))throw Error('version');const body=await content(version,path);res.writeHead(200,{'Content-Type':types[extname(path.endsWith('/')?path+'index.html':path)]||'application/octet-stream','Content-Length':body.length,'Cache-Control':'no-store'});res.end(body);}catch{res.writeHead(404);res.end();}});
 await new Promise(r=>server.listen(0,'127.0.0.1',r));const origin='http://127.0.0.1:'+server.address().port,port=await freePort();
 profile=await mkdtemp(join(tmpdir(),'ohvernight-measure-'));browser=spawn(chrome.candidate,['--headless=new','--no-sandbox','--disable-gpu','--enable-precise-memory-info','--remote-debugging-port='+port,'--user-data-dir='+profile,'about:blank'],{stdio:'ignore'});lifecycle=trackProcess(browser);
 await waitFor('http://127.0.0.1:'+port+'/json/version',{chrome,processState:()=>lifecycle.state,exitSignal:lifecycle.signal});const targets=await(await fetch('http://127.0.0.1:'+port+'/json/list')).json();client=cdpClient(targets.find(x=>x.type==='page').webSocketDebuggerUrl);
 const evaluate=async expression=>{if(pumpError)throw pumpError;const r=await client.command('Runtime.evaluate',{expression,awaitPromise:true,returnByValue:true});if(r.exceptionDetails)throw Error(expression+' '+JSON.stringify(r.exceptionDetails));return r.result.value;};
 pump=(async()=>{while(running){const e=client.events.shift();if(!e){await delay(5);continue;}if(e.method==='Fetch.requestPaused'){const local=new URL(e.params.request.url).origin===origin;try{await client.command(local?'Fetch.continueRequest':'Fetch.failRequest',{requestId:e.params.requestId,...(local?{}:{errorReason:'BlockedByClient'})});}catch(error){if(!error.message.includes('Invalid InterceptionId'))throw error;}}}})().catch(error=>{pumpError=error;});
 for(const name of ['Page','Runtime','Network','Performance'])await client.command(name+'.enable');await client.command('Network.setCacheDisabled',{cacheDisabled:true});await client.command('Fetch.enable',{patterns:[{urlPattern:'*',requestStage:'Request'}]});
 await client.command('Page.addScriptToEvaluateOnNewDocument',{source:"window.__lt=[];new PerformanceObserver(list=>{for(const e of list.getEntries())__lt.push(e.duration)}).observe({type:'longtask',buffered:true});"});
 await client.command('Emulation.setDeviceMetricsOverride',{width:390,height:844,deviceScaleFactor:2,mobile:true});await client.command('Emulation.setTouchEmulationEnabled',{enabled:true});await client.command('Emulation.setCPUThrottlingRate',{rate:4});
 async function ready(expression){for(let i=0;i<1200;i++){try{if(await evaluate(expression))return await evaluate('performance.now()');}catch(error){if(client.signal.aborted||lifecycle.signal.aborted)throw error;}await delay(50);}throw Error('measurement readiness timeout '+expression);}
 const frame='new Promise(r=>requestAnimationFrame(()=>setTimeout(r,0)))';
 for(const version of ['base','head'])for(const region of ['aspen','douglas-co'])for(let run=1;run<=5;run++){
  await client.command('Page.navigate',{url:'about:blank'});await client.command('Network.clearBrowserCache');
  const url=origin+'/'+version+(version==='head'?'/v2/?region='+region+'&view=map':region==='aspen'?'/v2/':'/v2/regions/douglas-co/');await client.command('Page.navigate',{url});
  const usable=await ready(version==='head'?'!!window.explore?.state.mapUsable':region==='aspen'?'!!document.getElementById("landing-explore")&&!document.getElementById("landing-explore").disabled&&!/Loading/.test(document.getElementById("results-summary").textContent)':'!!document.getElementById("status")&&!/Loading/.test(document.getElementById("status").textContent)');
  const complete=version==='head'?await ready('!!window.explore?.state.defaultLayersLoaded'):usable;
  if(version==='base'&&region==='aspen')await evaluate('document.getElementById("landing-explore").click()');await delay(1500);
  const longest=await evaluate('Math.max(0,...window.__lt)');
  await client.command('HeapProfiler.collectGarbage');const metrics=Object.fromEntries((await client.command('Performance.getMetrics')).metrics.map(x=>[x.name,x.value]));
  const select=version==='head'?`document.getElementById('layer-'+explore.region.index.artifacts.filter(x=>x.layer_id!=='coverage').sort((a,b)=>b.bytes-a.bytes)[0].layer_id)`:region==='aspen'?'document.getElementById("layer-water")':'document.querySelector("#layer-controls input[aria-label=\"Named streams\"]")';
  const toggle=await evaluate(`(async()=>{const control=${select};let start=performance.now();control.click();await ${frame};const off=performance.now()-start;start=performance.now();control.click();await ${frame};return {off,on:performance.now()-start}})()`);
  const row={version,region,run,mapUsableMs:usable,allDefaultLayersMs:complete,longestLongTaskMs:longest,heavyLayerOnMs:toggle.on,heavyLayerOffMs:toggle.off,heapMB:metrics.JSHeapUsedSize/1e6};rows.push(row);console.error(JSON.stringify(row));
 }
 const median=values=>[...values].sort((a,b)=>a-b)[2],medians={};for(const version of ['base','head']){medians[version]={};for(const region of ['aspen','douglas-co'])medians[version][region]=Object.fromEntries(['mapUsableMs','allDefaultLayersMs','longestLongTaskMs','heavyLayerOnMs','heapMB'].map(key=>[key,median(rows.filter(x=>x.version===version&&x.region===region).map(x=>x[key]))]));}
 const thresholds={};for(const region of ['aspen','douglas-co']){const base=medians.base[region],head=medians.head[region];thresholds[region]={mapUsableMs:base.allDefaultLayersMs*.5,allDefaultLayersMs:base.allDefaultLayersMs,longestLongTaskMs:medians.base.aspen.longestLongTaskMs*.5,heavyLayerOnMs:base.heavyLayerOnMs*1.25,heapMB:region==='aspen'?33.4:30.4};thresholds[region]=Object.fromEntries(Object.entries(thresholds[region]).map(([key,limit])=>[key,{limit,actual:head[key],pass:head[key]<=limit}]));}
 const baseline=JSON.parse(await readFile(join(root,'docs/specs/M3-baseline/baseline.json')));
 const output={baseCommit:'3dc0fef',headCommit:execFileSync('git',['rev-parse','HEAD'],{cwd:root,encoding:'utf8'}).trim(),chrome:chrome.version,node:process.version,viewport:[390,844],cpuThrottle:4,runs:5,method:'One offline Chrome session; non-local requests blocked; cold cache; readiness observed consistently through CDP; 1500ms settle before long-task and GC measures; heaviest loaded layer selected by display bytes. Base selectors match the committed baseline script.',rows,medians,thresholds,committedBaseline:baseline.filter(x=>x.viewport==='390x844'&&x.cpuThrottle===4)};
 console.log(JSON.stringify(output,null,2));
}finally{
 running=false;if(pump)await pump;const errors=[];const cleanup=async fn=>{try{await fn();}catch(error){errors.push(String(error));}};
 if(client)await cleanup(()=>closeSocket(client.socket));if(browser)await cleanup(()=>stopChrome(browser,lifecycle));if(server)await cleanup(()=>closeServer(server));if(profile)await cleanup(()=>rm(profile,{recursive:true,force:true,maxRetries:5,retryDelay:100}));if(errors.length)throw Error('measurement cleanup '+errors.join('; '));
}
