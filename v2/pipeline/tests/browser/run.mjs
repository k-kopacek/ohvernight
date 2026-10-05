import {createServer} from 'node:http';
import {mkdtemp,readFile,rm,stat} from 'node:fs/promises';
import {spawn} from 'node:child_process';
import {createServer as createTcpServer} from 'node:net';
import {extname,join,normalize,resolve} from 'node:path';
import {tmpdir} from 'node:os';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {setTimeout as delay} from 'node:timers/promises';

const root=resolve(fileURLToPath(new URL('../../../../',import.meta.url)));
const chromeCandidates=[process.env.CHROME,'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome','google-chrome','chromium'].filter(Boolean);
const mime={'.html':'text/html','.js':'text/javascript','.json':'application/json','.css':'text/css','.geojson':'application/geo+json','.svg':'image/svg+xml','.png':'image/png','.ico':'image/x-icon'};
export const CHROME_STARTUP_TIMEOUT_MS=60000;
export const CDP_COMMAND_TIMEOUT_MS=20000;
const CHROME_STOP_GRACE_MS=1500;
const CHROME_EXIT_DIAGNOSTIC_GRACE_MS=250;

async function freePort(){
  const server=createTcpServer();
  await new Promise((resolvePromise,reject)=>{server.once('error',reject);server.listen(0,'127.0.0.1',resolvePromise);});
  const port=server.address().port;
  await new Promise((resolvePromise,reject)=>server.close(error=>error?reject(error):resolvePromise()));
  return port;
}
export async function waitFor(url,{
  timeoutMs=CHROME_STARTUP_TIMEOUT_MS,retryIntervalMs=150,attemptTimeoutMs=1000,
  chrome={candidate:'unknown',version:'unknown'},
  processState=()=>({exited:false,exitCode:null,signal:null}),exitSignal,
}={}){
  const started=performance.now();
  const deadline=started+timeoutMs;
  let attempts=0,lastError='none';
  const diagnostic=reason=>{
    const state=processState();
    return new Error(`${reason} waiting for ${url}; elapsed=${Math.round(performance.now()-started)} ms; attempts=${attempts}; last error/status=${lastError}; Chrome executable=${chrome.candidate}; Chrome version=${chrome.version}; Chrome exited=${state.exited}; exit code=${state.exitCode}; signal=${state.signal}${state.error?`; process error=${state.error.message}`:''}`);
  };
  while(performance.now()<deadline){
    if(processState().exited||exitSignal?.aborted) throw diagnostic('Chrome exited before readiness');
    attempts++;
    let ready=false;
    try{
      const timeout=AbortSignal.timeout(Math.max(1,Math.ceil(Math.min(attemptTimeoutMs,deadline-performance.now()))));
      const response=await fetch(url,{signal:exitSignal?AbortSignal.any([timeout,exitSignal]):timeout});
      lastError=`HTTP ${response.status}`;
      await response.body?.cancel();
      ready=response.ok;
    }catch(error){lastError=`${error.name}: ${error.message}${error.cause?` (${error.cause.message})`:''}`;}
    if(processState().exited||exitSignal?.aborted) throw diagnostic('Chrome exited before readiness');
    if(ready) return;
    const remaining=deadline-performance.now();
    if(remaining>0) await delay(Math.min(retryIntervalMs,remaining),undefined,{signal:exitSignal}).catch(error=>{
      if(error.name!=='AbortError') throw error;
    });
  }
  throw diagnostic(processState().exited?'Chrome exited before readiness':'Timed out');
}
function trackProcess(child){
  const state={exited:false,exitCode:null,signal:null,error:null,closed:false};
  const controller=new AbortController();
  child.once('exit',(code,signal)=>{Object.assign(state,{exited:true,exitCode:code,signal});controller.abort();});
  child.once('error',error=>{Object.assign(state,{exited:true,error});controller.abort();});
  const closed=new Promise(resolvePromise=>child.once('close',()=>{state.closed=true;resolvePromise();}));
  return {state,closed,signal:controller.signal};
}
async function settlesWithin(promise,timeoutMs){
  let timer;
  try{return await Promise.race([promise.then(()=>true),new Promise(resolvePromise=>{timer=setTimeout(()=>resolvePromise(false),timeoutMs);})]);}
  finally{clearTimeout(timer);}
}
async function closeSocket(socket){
  if(socket.readyState===WebSocket.CLOSED) return;
  const closed=new Promise(resolvePromise=>socket.addEventListener('close',resolvePromise,{once:true}));
  socket.close();
  await settlesWithin(closed,CHROME_STOP_GRACE_MS);
}
async function stopChrome(browser,lifecycle){
  if(!lifecycle.state.exited) browser.kill('SIGTERM');
  if(!await settlesWithin(lifecycle.closed,CHROME_STOP_GRACE_MS)) browser.kill('SIGKILL');
  await lifecycle.closed;
}
async function closeServer(server){
  const closed=new Promise((resolvePromise,reject)=>server.close(error=>error?reject(error):resolvePromise()));
  server.closeAllConnections?.();
  await closed;
}
export function cdpClient(url,{commandTimeoutMs=CDP_COMMAND_TIMEOUT_MS}={}){
  const socket=new WebSocket(url);let nextId=0;const pending=new Map();const events=[];
  const connection=new AbortController();
  let disconnected,resolveReady,rejectReady;
  const ready=new Promise((resolvePromise,reject)=>{resolveReady=resolvePromise;rejectReady=reject;});
  ready.catch(()=>{}); // A disconnect before the first command must not be unhandled.
  const settle=(id,error,result)=>{
    const entry=pending.get(id);if(!entry) return;
    pending.delete(id);clearTimeout(entry.timer);
    error?entry.reject(new Error(`${entry.method}: ${error.message}`,{cause:error})):entry.resolve(result);
  };
  const disconnect=detail=>{
    if(disconnected) return;
    disconnected=new Error(`DevTools connection closed (${detail})`);
    rejectReady(disconnected);
    for(const id of pending.keys()) settle(id,disconnected);
    connection.abort(disconnected);
  };
  socket.addEventListener('open',()=>{if(!disconnected) resolveReady();});
  socket.addEventListener('close',event=>disconnect(`code=${event.code}${event.reason?`; ${event.reason}`:''}`));
  socket.addEventListener('error',event=>disconnect(`WebSocket error${event.message?`: ${event.message}`:''}`));
  socket.addEventListener('message',event=>{
    const message=JSON.parse(event.data);
    if(message.id&&pending.has(message.id)) settle(message.id,message.error?new Error(message.error.message):null,message.result);
    else events.push(message);
  });
  const command=(method,params={})=>{
    if(disconnected) return Promise.reject(new Error(`${method}: ${disconnected.message}`,{cause:disconnected}));
    const id=++nextId;
    return new Promise((resolvePromise,reject)=>{
      const timer=setTimeout(()=>settle(id,new Error(`CDP command timed out after ${commandTimeoutMs} ms`)),commandTimeoutMs);
      pending.set(id,{method,resolve:resolvePromise,reject,timer});
      ready.then(()=>{
        if(!pending.has(id)) return;
        try{socket.send(JSON.stringify({id,method,params}));}
        catch(error){disconnect(`send failed: ${error.message}`);}
      },error=>settle(id,error));
    });
  };
  return {command,events,socket,signal:connection.signal};
}
async function findChrome(){
  for(const candidate of chromeCandidates){
    const child=spawn(candidate,['--version'],{stdio:['ignore','pipe','ignore']});
    const output=await new Promise(resolvePromise=>{let text='';child.stdout.on('data',chunk=>text+=chunk);child.on('close',()=>resolvePromise(text));child.on('error',()=>resolvePromise(''));});
    if(output.trim()) return {candidate,version:output.trim()};
  }
  throw new Error('Chrome not found; set CHROME to a Chrome or Chromium executable');
}
async function staticServer(){
  const server=createServer(async(request,response)=>{
    try{
      const requestPath=decodeURIComponent((request.url||'/').split('?')[0]);
      const relative=normalize(requestPath).replace(/^([.][.][/\\])+/, '').replace(/^[/\\]+/,'')||'index.html';
      let file=resolve(root,relative);
      if(file!==root&&!file.startsWith(root+'/')) throw new Error('path outside checkout');
      let info=await stat(file);if(info.isDirectory()){file=join(file,'index.html');info=await stat(file);}if(!info.isFile()) throw new Error('not a file');
      response.writeHead(200,{'content-type':mime[extname(file)]||'application/octet-stream','cache-control':'no-store'});
      response.end(await readFile(file));
    }catch(error){response.writeHead(error.message==='not a file'?404:400);response.end(error.message);}
  });
  await new Promise(resolvePromise=>server.listen(0,'127.0.0.1',resolvePromise));
  return {server,port:server.address().port};
}
async function inspectPage(client,url,localOrigin,signal){
  signal.throwIfAborted();
  const state={url,sameOriginRequests:[],failedSameOrigin:[],externalUrls:[],externalBlocked:0,exceptions:[],consoleErrors:[]};
  await client.command('Network.enable');
  await client.command('Runtime.enable');
  await client.command('Page.enable');
  await client.command('Log.enable');
  await client.command('Fetch.enable',{patterns:[{urlPattern:'*',requestStage:'Request'}]});
  const finishAt=Date.now()+12000;
  const navigation=client.command('Page.navigate',{url});
  navigation.catch(()=>{}); // Navigation is awaited after processing intercepted requests.
  while(Date.now()<finishAt){
    signal.throwIfAborted();
    const message=client.events.shift();
    if(!message){await delay(20,undefined,{signal});continue;}
    if(message.method==='Fetch.requestPaused'){
      const requestUrl=message.params.request.url;
      if(requestUrl.startsWith(localOrigin)) await client.command('Fetch.continueRequest',{requestId:message.params.requestId});
      else {state.externalBlocked++;await client.command('Fetch.failRequest',{requestId:message.params.requestId,errorReason:'BlockedByClient'});}
    }else if(message.method==='Network.responseReceived'){
      const response=message.params.response;
      if(response.url.startsWith(localOrigin)){state.sameOriginRequests.push({url:response.url,status:response.status});if(response.status>=400)state.failedSameOrigin.push(response.url);}
      else if(!response.url.startsWith('data:')) state.externalUrls.push(response.url);
    }else if(message.method==='Network.loadingFailed'&&message.params.type!=='Other'&&message.params.errorText){
      if((message.params.errorText||'').includes('net::ERR_FAILED')) state.externalBlocked++;
    }else if(message.method==='Runtime.exceptionThrown') state.exceptions.push(message.params.exceptionDetails.text||'uncaught exception');
    else if(message.method==='Log.entryAdded'&&message.params.entry.level==='error'&&!message.params.entry.text.includes('ERR_BLOCKED_BY_CLIENT')) state.consoleErrors.push(message.params.entry.text);
    if(message.method==='Page.loadEventFired') state.loaded=true;
    if(state.loaded&&Date.now()>finishAt-2500) break;
  }
  state.dom=await client.command('Runtime.evaluate',{expression:`JSON.stringify({scrollWidth:document.documentElement.scrollWidth,innerWidth:innerWidth,hasLegacyLink:!!document.querySelector('a[href="./map-data.json"]'),title:document.title})`,returnByValue:true});
  await navigation;
  state.dom=JSON.parse(state.dom.result.value);
  return state;
}
async function main(){
  let site,profile,browser,lifecycle,client;
  try{
    const chrome=await findChrome();
    site=await staticServer();
    const debugPort=await freePort();
    profile=await mkdtemp(join(tmpdir(),'ohvernight-browser-'));
    browser=spawn(chrome.candidate,[`--headless=new`,`--no-sandbox`,`--disable-gpu`,`--disable-dev-shm-usage`,`--remote-debugging-port=${debugPort}`,`--user-data-dir=${profile}`,'about:blank'],{stdio:['ignore','ignore','ignore']});
    lifecycle=trackProcess(browser);
    await waitFor(`http://127.0.0.1:${debugPort}/json/version`,{chrome,processState:()=>lifecycle.state,exitSignal:lifecycle.signal});
    const targets=await (await fetch(`http://127.0.0.1:${debugPort}/json/list`)).json();
    const target=targets.find(item=>item.type==='page');
    if(!target) throw new Error('Chrome page target missing');
    client=cdpClient(target.webSocketDebuggerUrl);
    const origin=`http://127.0.0.1:${site.port}`;
    const inspectionSignal=AbortSignal.any([lifecycle.signal,client.signal]);
    const chromeExited=()=>new Error(`Chrome exited during page inspection; exit code=${lifecycle.state.exitCode}; signal=${lifecycle.state.signal}`);
    let pages;
    let onExit;
    try{
      const exited=new Promise((_,reject)=>{
        onExit=()=>reject(chromeExited());
        if(lifecycle.signal.aborted) onExit();
        else lifecycle.signal.addEventListener('abort',onExit,{once:true});
      });
      const inspect=async()=>[await inspectPage(client,`${origin}/v2/index.html`,origin,inspectionSignal),await inspectPage(client,`${origin}/v2/regions/douglas-co/index.html`,origin,inspectionSignal)];
      pages=await Promise.race([inspect(),exited]);
    }catch(error){
      // Socket closure can precede the child exit event; observe it before cleanup sends SIGTERM.
      if(client.signal.aborted&&!lifecycle.state.exited) await settlesWithin(lifecycle.closed,CHROME_EXIT_DIAGNOSTIC_GRACE_MS);
      if(lifecycle.state.exited) throw chromeExited();
      if(inspectionSignal.aborted&&error.name==='AbortError') throw inspectionSignal.reason;
      throw error;
    }finally{lifecycle.signal.removeEventListener('abort',onExit);}
    for(const page of pages){
      if(!page.loaded) throw new Error(`page did not load: ${page.url}`);
      if(page.exceptions.length||page.consoleErrors.length) throw new Error(`browser errors on ${page.url}: ${JSON.stringify({exceptions:page.exceptions,consoleErrors:page.consoleErrors})}`);
      if(page.failedSameOrigin.length) throw new Error(`same-origin request failed on ${page.url}: ${page.failedSameOrigin.join(',')}`);
      if(page.externalUrls.length) throw new Error(`non-local request escaped blocking on ${page.url}: ${page.externalUrls.join(',')}`);
      if(page.dom.scrollWidth>page.dom.innerWidth) throw new Error(`horizontal overflow on ${page.url}`);
    }
    if(pages[0].dom.hasLegacyLink) throw new Error('removed legacy download link is still present');
    if(!pages[0].sameOriginRequests.some(request=>request.url.endsWith('/regions/aspen/region.json'))){
      throw new Error('Aspen page did not load its manifest policy');
    }
    console.log(JSON.stringify({chrome:chrome.version,server:`127.0.0.1:${site.port}`,pages},null,2));
  }finally{
    const cleanupErrors=[];
    const cleanup=async action=>{try{await action();}catch(error){cleanupErrors.push(error);}};
    if(client) await cleanup(()=>closeSocket(client.socket));
    if(browser) await cleanup(()=>stopChrome(browser,lifecycle));
    if(site) await cleanup(()=>closeServer(site.server));
    if(profile) await cleanup(()=>rm(profile,{recursive:true,force:true,maxRetries:5,retryDelay:100}));
    if(cleanupErrors.length){console.error('Browser cleanup failed:',cleanupErrors);process.exitCode=1;}
  }
}
if(process.argv[1]&&import.meta.url===pathToFileURL(process.argv[1]).href){
  main().catch(error=>{console.error(error.stack||error);process.exitCode=1;});
}
