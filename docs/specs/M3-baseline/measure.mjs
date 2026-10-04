// Baseline measurement of the current Ohvernight apps via headless Chrome (CDP).
import { spawn } from 'node:child_process';
import { existsSync, mkdtempSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

const BASE = process.env.BASE || 'http://127.0.0.1:8765';
// Set CHROME to the browser binary if it is not at one of these paths.
const CHROME = process.env.CHROME || ['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', '/usr/bin/google-chrome', '/usr/bin/chromium-browser', '/usr/bin/chromium'].find(p => existsSync(p));
if (!CHROME) throw new Error('Chrome not found; set CHROME=/path/to/chrome');
const PORT = 9333;
const sleep = ms => new Promise(r => setTimeout(r, ms));
const dir = mkdtempSync(join(tmpdir(), 'ohvernight-chrome-'));
const chrome = spawn(CHROME, ['--headless=new', `--remote-debugging-port=${PORT}`, `--user-data-dir=${dir}`, '--no-first-run', '--disable-extensions', '--enable-precise-memory-info', 'about:blank'], { stdio: 'ignore' });

async function connect() {
  for (let i = 0; i < 300; i++) {
    try {
      const list = await (await fetch(`http://127.0.0.1:${PORT}/json/list`)).json();
      const page = list.find(t => t.type === 'page');
      if (page) return page.webSocketDebuggerUrl;
    } catch {}
    await sleep(200);
  }
  throw new Error('chrome did not start');
}

const ws = new WebSocket(await connect());
await new Promise(r => (ws.onopen = r));
let seq = 0; const pending = new Map(); const listeners = [];
ws.onmessage = e => { const m = JSON.parse(e.data); if (m.id) { const p = pending.get(m.id); pending.delete(m.id); m.error ? p.reject(new Error(m.error.message)) : p.resolve(m.result); } else listeners.forEach(f => f(m)); };
const send = (method, params = {}) => new Promise((resolve, reject) => { const id = ++seq; pending.set(id, { resolve, reject }); ws.send(JSON.stringify({ id, method, params })); });
const evaluate = async expression => { const r = await send('Runtime.evaluate', { expression, awaitPromise: true, returnByValue: true }); if (r.exceptionDetails) throw new Error(JSON.stringify(r.exceptionDetails).slice(0, 400)); return r.result.value; };

await send('Page.enable'); await send('Network.enable'); await send('Runtime.enable'); await send('Performance.enable');

const INIT = `window.__lt=[];try{new PerformanceObserver(l=>{for(const e of l.getEntries())window.__lt.push(e.duration)}).observe({type:'longtask',buffered:true})}catch(e){}`;
await send('Page.addScriptToEvaluateOnNewDocument', { source: INIT });

const AREA = `(()=>{const W=innerWidth,H=innerHeight,step=4;let total=0,free=0;const m=document.getElementById('map');
for(let y=step/2;y<H;y+=step)for(let x=step/2;x<W;x+=step){total++;const e=document.elementFromPoint(x,y);if(e&&m.contains(e)&&!e.closest('.leaflet-control'))free++;}
const small=[...document.querySelectorAll('button,a,input[type=checkbox],select,summary')].filter(e=>{const r=e.getBoundingClientRect();const s=getComputedStyle(e);return r.width>0&&r.height>0&&s.visibility!=='hidden'&&r.bottom>0&&r.top<H&&!e.closest('dialog:not([open])')&&!e.closest('[inert]')&&(r.width<44||r.height<44);}).map(e=>(e.id||e.textContent.trim().slice(0,18)||e.className)+' '+Math.round(e.getBoundingClientRect().width)+'x'+Math.round(e.getBoundingClientRect().height));
const rect=s=>{const e=document.querySelector(s);if(!e)return null;const r=e.getBoundingClientRect();return [Math.round(r.left),Math.round(r.top),Math.round(r.width),Math.round(r.height)];};
return {viewport:[W,H],freeMapPct:+(100*free/total).toFixed(1),small,sheet:rect('#sheet')||rect('.peek'),topbar:rect('.topbar')||rect('header'),tools:rect('.map-tools')||rect('.tools'),hscroll:document.documentElement.scrollWidth>W};})()`;

const pages = {
  aspen: {
    url: '/v2/',
    ready: `!!document.getElementById('results-summary')&&!/Loading/.test(document.getElementById('results-summary').textContent)&&document.getElementById('landing-explore').disabled===false`,
    enter: `document.getElementById('landing-explore').click()`,
    toggle: `(async()=>{const c=document.getElementById('layer-water');const raf=()=>new Promise(r=>requestAnimationFrame(()=>setTimeout(r,0)));let t=performance.now();c.click();await raf();const off=performance.now()-t;t=performance.now();c.click();await raf();const on=performance.now()-t;return {off:+off.toFixed(1),on:+on.toFixed(1)};})()`,
    openLayers: `document.getElementById('open-layers').click()`,
  },
  douglas: {
    url: '/v2/regions/douglas-co/',
    ready: `!!document.getElementById('status')&&!/Loading/.test(document.getElementById('status').textContent)`,
    enter: `0`,
    toggle: `(async()=>{const c=document.querySelector('#layer-controls input[aria-label="Named streams"]');const raf=()=>new Promise(r=>requestAnimationFrame(()=>setTimeout(r,0)));let t=performance.now();c.click();await raf();const off=performance.now()-t;t=performance.now();c.click();await raf();const on=performance.now()-t;return {off:+off.toFixed(1),on:+on.toFixed(1)};})()`,
    openLayers: `document.getElementById('layers').click()`,
  },
};
const viewports = [[320, 568, true], [390, 844, true], [768, 1024, true], [1440, 900, false]];

async function run(name, [w, h, mobile], throttle) {
  const p = pages[name];
  await send('Emulation.setDeviceMetricsOverride', { width: w, height: h, deviceScaleFactor: mobile ? 2 : 1, mobile });
  await send('Emulation.setTouchEmulationEnabled', { enabled: mobile });
  await send('Emulation.setCPUThrottlingRate', { rate: throttle });
  await send('Network.clearBrowserCache');
  const sizes = new Map(), urls = new Map();
  const onEvent = m => {
    if (m.method === 'Network.requestWillBeSent') urls.set(m.params.requestId, m.params.request.url);
    if (m.method === 'Network.loadingFinished') sizes.set(m.params.requestId, m.params.encodedDataLength);
  };
  listeners.push(onEvent);
  await send('Page.navigate', { url: 'about:blank' }); await sleep(200);
  const t0 = Date.now();
  await send('Page.navigate', { url: BASE + p.url });
  let readyMs = null;
  for (let i = 0; i < 1200; i++) { try { if (await evaluate(p.ready)) { readyMs = await evaluate('performance.now()'); break; } } catch {} await sleep(50); }
  await evaluate(p.enter); await sleep(1500);
  const lt = await evaluate('({n:window.__lt.length,total:Math.round(window.__lt.reduce((a,b)=>a+b,0)),max:Math.round(Math.max(0,...window.__lt))})');
  const collapsed = await evaluate(AREA);
  const toggle = await evaluate(p.toggle);
  await send('HeapProfiler.collectGarbage');
  const metrics = Object.fromEntries((await send('Performance.getMetrics')).metrics.map(m => [m.name, m.value]));
  const dom = await evaluate('document.getElementsByTagName("*").length');
  await evaluate(p.openLayers); await sleep(400);
  const drawer = await evaluate(`(()=>{const d=document.querySelector('dialog[open]');if(!d)return null;const r=d.getBoundingClientRect();return {rect:[Math.round(r.left),Math.round(r.top),Math.round(r.width),Math.round(r.height)],coverPct:+(100*r.width*r.height/(innerWidth*innerHeight)).toFixed(1),modal:d.matches(':modal')};})()`);
  listeners.splice(listeners.indexOf(onEvent), 1);
  let own = 0, ownN = 0, tiles = 0;
  for (const [id, size] of sizes) { const u = urls.get(id) || ''; if (u.startsWith(BASE)) { own += size; ownN++; } else tiles += size; }
  return { page: name, viewport: `${w}x${h}`, cpuThrottle: throttle, readyMs: Math.round(readyMs), wallMs: Date.now() - t0, longTasks: lt, sameOriginRequests: ownN, sameOriginBytes: own, heapUsedMB: +(metrics.JSHeapUsedSize / 1e6).toFixed(1), domNodes: dom, layoutCount: metrics.LayoutCount, toggleHeavyLayerMs: toggle, freeMapPct: collapsed.freeMapPct, sheet: collapsed.sheet, topbar: collapsed.topbar, tools: collapsed.tools, hscroll: collapsed.hscroll, smallTargets: collapsed.small, layerDrawer: drawer };
}

const out = [];
try {
  for (const name of Object.keys(pages)) for (const vp of viewports) out.push(await run(name, vp, vp[2] ? 4 : 1));
  for (const name of Object.keys(pages)) out.push(await run(name, [390, 844, true], 1));
} finally { console.log(JSON.stringify(out, null, 1)); ws.close(); chrome.kill(); }
