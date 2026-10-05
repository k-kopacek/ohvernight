const assert=require('node:assert/strict');
const {test}=require('node:test');
const {createServer}=require('node:http');

const harness=import('./browser/run.mjs');
const chrome={candidate:'/offline/test-chrome',version:'Test Chrome 123'};

async function localServer(t,handler){
  const server=createServer(handler);
  t.after(async()=>{
    const closed=new Promise((resolve,reject)=>server.close(error=>error?reject(error):resolve()));
    server.closeAllConnections();
    await closed;
  });
  await new Promise((resolve,reject)=>{server.once('error',reject);server.listen(0,'127.0.0.1',resolve);});
  return {server,url:`http://127.0.0.1:${server.address().port}/json/version`};
}

function checkDiagnostic(error,url){
  assert.ok(error.message.includes(url));
  for(const field of [/elapsed=\d+ ms/,/attempts=\d+/,/last error\/status=/,
    /Chrome executable=\/offline\/test-chrome/,/Chrome version=Test Chrome 123/,
    /Chrome exited=/,/exit code=/,/signal=/]) assert.match(error.message,field);
  return true;
}

test('browser startup resolves promptly after delayed readiness',{timeout:3000},async t=>{
  const {waitFor}=await harness;
  let polls=0;
  const {url}=await localServer(t,(_request,response)=>{
    response.writeHead(++polls<=3?503:200);
    response.end('{}');
  });
  const started=performance.now();
  await waitFor(url,{timeoutMs:2500,retryIntervalMs:20,attemptTimeoutMs:500,chrome});
  assert.equal(polls,4);
  assert.ok(performance.now()-started<2000,'readiness should resolve before the overall deadline');
});

test('browser startup closed-port timeout has complete diagnostics',{timeout:3000},async()=>{
  const {waitFor}=await harness;
  const server=createServer();
  await new Promise((resolve,reject)=>{server.once('error',reject);server.listen(0,'127.0.0.1',resolve);});
  const url=`http://127.0.0.1:${server.address().port}/json/version`;
  await new Promise((resolve,reject)=>server.close(error=>error?reject(error):resolve()));
  const started=performance.now();
  await assert.rejects(waitFor(url,{timeoutMs:150,retryIntervalMs:20,attemptTimeoutMs:50,chrome}),error=>{
    checkDiagnostic(error,url);
    assert.match(error.message,/Timed out/);
    assert.match(error.message,/last error\/status=TypeError: fetch failed/);
    assert.match(error.message,/Chrome exited=false; exit code=null; signal=null/);
    return true;
  });
  assert.ok(performance.now()-started<2000,'a closed port must not hang the helper');
});

test('browser startup rejects an already exited child before polling',{timeout:3000},async()=>{
  const {waitFor}=await harness;
  const url='http://127.0.0.1:1/json/version';
  const started=performance.now();
  await assert.rejects(waitFor(url,{timeoutMs:2500,chrome,
    processState:()=>({exited:true,exitCode:17,signal:null})}),error=>{
    checkDiagnostic(error,url);
    assert.match(error.message,/Chrome exited before readiness/);
    assert.match(error.message,/attempts=0/);
    assert.match(error.message,/Chrome exited=true; exit code=17; signal=null/);
    return true;
  });
  assert.ok(performance.now()-started<2000,'an exited child must not wait for the deadline');
});

test('browser startup bounds hung HTTP requests by the overall deadline',{timeout:3000},async t=>{
  const {waitFor}=await harness;
  const {url}=await localServer(t,()=>{});
  const started=performance.now();
  await assert.rejects(waitFor(url,{timeoutMs:150,retryIntervalMs:20,attemptTimeoutMs:1000,chrome}),error=>{
    checkDiagnostic(error,url);
    assert.match(error.message,/Timed out/);
    assert.match(error.message,/TimeoutError/);
    return true;
  });
  assert.ok(performance.now()-started<2000,'a hung request must not exceed the deadline indefinitely');
});

test('browser exit interrupts an in-flight readiness request',{timeout:3000},async t=>{
  const {waitFor}=await harness;
  const controller=new AbortController();
  const state={exited:false,exitCode:null,signal:null};
  const {url}=await localServer(t,()=>{
    Object.assign(state,{exited:true,signal:'SIGTERM'});
    controller.abort();
  });
  const started=performance.now();
  await assert.rejects(waitFor(url,{timeoutMs:2500,attemptTimeoutMs:2500,chrome,
    processState:()=>state,exitSignal:controller.signal}),error=>{
    checkDiagnostic(error,url);
    assert.match(error.message,/Chrome exited before readiness/);
    assert.match(error.message,/Chrome exited=true; exit code=null; signal=SIGTERM/);
    return true;
  });
  assert.ok(performance.now()-started<2000,'child exit should interrupt the fetch timeout');
});
