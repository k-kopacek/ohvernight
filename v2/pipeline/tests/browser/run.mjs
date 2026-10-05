import {createServer} from 'node:http';
import {mkdtemp,readFile,rm,stat} from 'node:fs/promises';
import {spawn} from 'node:child_process';
import {createServer as createTcpServer} from 'node:net';
import {extname,join,normalize,resolve} from 'node:path';
import {tmpdir} from 'node:os';
import {fileURLToPath} from 'node:url';

const root=resolve(fileURLToPath(new URL('../../../../',import.meta.url)));
const chromeCandidates=[process.env.CHROME,'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome','google-chrome','chromium'].filter(Boolean);
const mime={'.html':'text/html','.js':'text/javascript','.json':'application/json','.css':'text/css','.geojson':'application/geo+json','.svg':'image/svg+xml','.png':'image/png','.ico':'image/x-icon'};
const wait=ms=>new Promise(resolvePromise=>setTimeout(resolvePromise,ms));

async function freePort(){
  const server=createTcpServer();
  await new Promise((resolvePromise,reject)=>{server.once('error',reject);server.listen(0,'127.0.0.1',resolvePromise);});
  const port=server.address().port;server.close();return port;
}
async function waitFor(url){
  for(let attempt=0;attempt<100;attempt++){
    try{const response=await fetch(url);if(response.ok)return; }catch{}
    await wait(50);
  }
  throw new Error('Timed out waiting for '+url);
}
function cdpClient(url){
  const socket=new WebSocket(url);let nextId=0;const pending=new Map();const events=[];
  const ready=new Promise((resolvePromise,reject)=>{socket.addEventListener('open',()=>resolvePromise());socket.addEventListener('error',reject);});
  socket.addEventListener('message',event=>{
    const message=JSON.parse(event.data);
    if(message.id&&pending.has(message.id)){const {resolve:resolvePromise,reject}=pending.get(message.id);pending.delete(message.id);message.error?reject(new Error(message.error.message)):resolvePromise(message.result);}
    else events.push(message);
  });
  const command=async(method,params={})=>{await ready;const id=++nextId;return new Promise((resolvePromise,reject)=>{pending.set(id,{resolve:resolvePromise,reject});socket.send(JSON.stringify({id,method,params}));});};
  return {command,events,socket};
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
      const file=resolve(root,relative);
      if(file!==root&&!file.startsWith(root+'/')) throw new Error('path outside checkout');
      const info=await stat(file);if(!info.isFile()) throw new Error('not a file');
      response.writeHead(200,{'content-type':mime[extname(file)]||'application/octet-stream','cache-control':'no-store'});
      response.end(await readFile(file));
    }catch(error){response.writeHead(error.message==='not a file'?404:400);response.end(error.message);}
  });
  await new Promise(resolvePromise=>server.listen(0,'127.0.0.1',resolvePromise));
  return {server,port:server.address().port};
}
async function inspectPage(client,url,localOrigin){
  const state={url,sameOriginRequests:[],failedSameOrigin:[],externalUrls:[],externalBlocked:0,exceptions:[],consoleErrors:[]};
  await client.command('Network.enable');
  await client.command('Runtime.enable');
  await client.command('Page.enable');
  await client.command('Log.enable');
  await client.command('Fetch.enable',{patterns:[{urlPattern:'*',requestStage:'Request'}]});
  const finishAt=Date.now()+12000;
  const navigation=client.command('Page.navigate',{url});
  while(Date.now()<finishAt){
    const message=client.events.shift();
    if(!message){await wait(20);continue;}
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
  const chrome=await findChrome();
  const site=await staticServer();
  const debugPort=await freePort();
  const profile=await mkdtemp(join(tmpdir(),'ohvernight-browser-'));
  const browser=spawn(chrome.candidate,[`--headless=new`,`--no-sandbox`,`--disable-gpu`,`--disable-dev-shm-usage`,`--remote-debugging-port=${debugPort}`,`--user-data-dir=${profile}`,'about:blank'],{stdio:['ignore','ignore','ignore']});
  try{
    await waitFor(`http://127.0.0.1:${debugPort}/json/version`);
    const targets=await (await fetch(`http://127.0.0.1:${debugPort}/json/list`)).json();
    const target=targets.find(item=>item.type==='page');
    if(!target) throw new Error('Chrome page target missing');
    const client=cdpClient(target.webSocketDebuggerUrl);
    const origin=`http://127.0.0.1:${site.port}`;
    const pages=[await inspectPage(client,`${origin}/v2/index.html`,origin),await inspectPage(client,`${origin}/v2/regions/douglas-co/index.html`,origin)];
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
    client.socket.close();
  }finally{
    browser.kill('SIGTERM');
    if(browser.exitCode===null) await new Promise(resolvePromise=>browser.once('close',resolvePromise));
    site.server.close();
    await rm(profile,{recursive:true,force:true,maxRetries:5,retryDelay:100});
  }
}
main().catch(error=>{console.error(error.stack||error);process.exitCode=1;});
