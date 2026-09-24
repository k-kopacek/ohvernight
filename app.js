(async()=>{
'use strict';
const $=id=>document.getElementById(id),esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const mobile=()=>matchMedia('(max-width:760px)').matches;
let map,markers,baseLayer,data,inventory,places=[],kind='all',selected=null;
let trip={resort:'aspen',arrive:'2027-01-15',depart:'2027-01-17',vehicle:'passenger_car'},plan={a:null,b:null};
const storageKey='ohvernight-trip-v1';
function controlsReady(ready){document.querySelectorAll('button').forEach(b=>{if(b.id!=='sheet-toggle')b.disabled=!ready;});}
controlsReady(false);
try{const saved=JSON.parse(localStorage.getItem(storageKey)||'null');if(saved){trip={...trip,...saved.trip};plan={...plan,...saved.plan};}}catch{}
function persist(){try{localStorage.setItem(storageKey,JSON.stringify({trip,plan}));}catch{}}
const ll=p=>[p.coordinates[1],p.coordinates[0]];
const resort=()=>data.resorts.find(r=>r.id===trip.resort);
const distance=p=>map?map.distance(ll(p),ll(resort()))/1609.344:null;
const distanceText=p=>distance(p)===null?'Distance unavailable':distance(p).toFixed(1)+' mi direct';
const type=p=>({campground:'CAMPGROUND',dispersed:'DISPERSED AREA',lodging:'ROOM BACKUP'}[p.kind]||'LOCATION');
const visible=()=>places.filter(p=>(kind==='all'||p.kind===kind)&&($('show-conflicts').checked||p.status!=='excluded'));
function expand(value){$('sheet').classList.toggle('expanded',value);document.body.classList.toggle('sheet-open',value);$('sheet-toggle').setAttribute('aria-expanded',String(value));$('sheet-action').textContent=value?'More map ↓':'Expand ↑';}
$('sheet-toggle').addEventListener('click',()=>expand(!$('sheet').classList.contains('expanded')));
function fillTrip(){for(const key of ['resort','arrive','depart','vehicle'])$(key).value=trip[key];}
$('edit-trip').onclick=()=>{fillTrip();$('trip-error').hidden=true;$('trip-dialog').showModal();};
$('close-trip').onclick=()=>$('trip-dialog').close();
$('trip-form').onsubmit=event=>{event.preventDefault();const next=Object.fromEntries(['resort','arrive','depart','vehicle'].map(k=>[k,$(k).value]));if(!TripRules.tripDays(next.arrive,next.depart)){$('trip-error').textContent='Choose a departure after arrival, within 366 nights.';$('trip-error').hidden=false;return;}trip=next;persist();$('trip-dialog').close();render();fit();};
function setKind(value){kind=value;document.querySelectorAll('[data-kind]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.kind===value)));render();}
document.querySelectorAll('[data-kind]').forEach(b=>b.onclick=()=>setKind(b.dataset.kind));
$('show-conflicts').onchange=()=>render();
function selectedDetails(){
 const p=places.find(p=>p.id===selected);
 if(!p){$('detail').innerHTML='';return;}
 const directions='https://www.google.com/maps/dir/?api=1&destination='+encodeURIComponent(p.coordinates[1]+','+p.coordinates[0]);
 const listingLabel=p.kind==='lodging'?'Official site & booking ↗':'Official listing & camping details ↗';
 $('detail').innerHTML='<span class="eyebrow">'+esc(type(p))+'</span><h2>'+esc(p.name)+'</h2><a class="official-link" href="'+esc(p.source)+'" target="_blank" rel="noopener noreferrer">'+listingLabel+'</a><span class="status '+(p.status==='excluded'?'conflict':'')+'">'+esc(p.label)+'</span><p class="why">'+esc(p.tripNote)+'</p><p>'+esc(p.note)+'</p><h3>Before you commit</h3><ul>'+p.unknowns.map(n=>'<li>'+esc(n)+'</li>').join('')+'</ul><div class="actions"><button data-save="a" aria-pressed="'+(plan.a===p.id)+'">'+(plan.a===p.id?'Saved as Plan A':'Save as Plan A')+'</button><button data-save="b" aria-pressed="'+(plan.b===p.id)+'">'+(plan.b===p.id?'Saved as backup':'Save as backup')+'</button></div><p class="muted">Saving a place does not confirm it is suitable or available.</p><div class="links"><a href="'+directions+'" target="_blank" rel="noopener noreferrer">Open directions ↗</a><span>'+esc(distanceText(p))+' to '+esc(resort().name)+'</span></div><details><summary>Evidence, location accuracy & review date</summary><p>Listing reviewed '+esc(p.checked_on)+'. '+esc(p.locationBasis)+'.</p><p><a href="'+esc(p.mapSource)+'" target="_blank" rel="noopener noreferrer">Location source ↗</a></p>'+(p.access?'<p><a href="'+esc(p.access.evidence.source_url)+'" target="_blank" rel="noopener noreferrer">USFS vehicle designation ↗</a> · '+esc(p.access.id)+' · retrieved '+esc(p.access.evidence.retrieved_at.slice(0,10))+'</p>':'')+'<p>Distances are straight-line, not driving distances. Directions may not reflect closures or permission to use the approach.</p></details>';
 $('detail').querySelectorAll('[data-save]').forEach(b=>b.onclick=()=>{const slot=b.dataset.save,other=slot==='a'?'b':'a';plan[slot]=plan[slot]===p.id?null:p.id;if(plan[other]===p.id)plan[other]=null;persist();renderPlan();selectedDetails();});
}
function renderPlan(){
 const rows=['a','b'].map(slot=>{const p=places.find(p=>p.id===plan[slot]);return p?'<div class="plan-row"><span><strong>'+ (slot==='a'?'PLAN A':'BACKUP')+'</strong> · '+esc(p.name)+'<small>'+esc(p.label)+'</small></span><button data-open-plan="'+p.id+'" aria-label="View '+esc(p.name)+'">View</button><button data-clear="'+slot+'" aria-label="Remove '+(slot==='a'?'Plan A':'backup')+'">×</button></div>':'';}).join('');
 $('saved-plan').innerHTML=rows?'<h2>Your overnight plan</h2>'+rows+'<p class="plan-note">Saved on this device · still needs confirmation</p>':'';
 $('saved-plan').querySelectorAll('[data-open-plan]').forEach(b=>b.onclick=()=>{setKind('all');$('show-conflicts').checked=true;choose(b.dataset.openPlan);});
 $('saved-plan').querySelectorAll('[data-clear]').forEach(b=>b.onclick=()=>{plan[b.dataset.clear]=null;persist();renderPlan();selectedDetails();});
}
function render(){
 places=inventory.places.map(p=>TripRules.evaluate(p,trip));
 const shown=visible().sort((a,b)=>(a.status==='excluded')-(b.status==='excluded') || (distance(a)||0)-(distance(b)||0));
 if(!shown.some(p=>p.id===selected))selected=shown[0]?.id||null;
 const conflicts=places.filter(p=>p.status==='excluded').length;
 $('results-summary').textContent=places.length+' sourced places · '+conflicts+' date / vehicle conflicts';
 const fmt=s=>new Date(s+'T12:00:00Z').toLocaleDateString('en-US',{month:'short',day:'numeric',timeZone:'UTC'});
 $('trip-caption').textContent=resort().name+' · '+fmt(trip.arrive)+'–'+fmt(trip.depart);
 $('trip-insight').innerHTML='<strong>No confirmed vehicle overnights yet.</strong><span>'+conflicts+(conflicts===1?' place conflicts':' places conflict')+' with this trip. Other camping options still need access and permission checks.</span><br><button class="text-button" id="room-backups">Explore a room backup →</button>';
 $('room-backups').onclick=()=>{setKind('lodging');expand(true);};
 $('list').innerHTML=shown.length?shown.map(p=>'<button class="place-card" data-place="'+p.id+'" aria-pressed="'+(p.id===selected)+'"><span class="card-top"><span>'+esc(type(p))+'</span><span class="distance">'+esc(distanceText(p))+'</span></span><h3>'+esc(p.name)+'</h3><span class="status '+(p.status==='excluded'?'conflict':'')+'">'+esc(p.label)+'</span></button>').join(''):'<p class="empty">No places match. Try another stay type or include conflicts.</p>';
 $('list').querySelectorAll('[data-place]').forEach(b=>b.onclick=()=>choose(b.dataset.place));
 renderPlan();selectedDetails();renderMarkers();
}
function choose(id){selected=id;render();const p=places.find(p=>p.id===selected);if(p&&map){expand(false);map.panTo(ll(p),{animate:!matchMedia('(prefers-reduced-motion:reduce)').matches});}if(mobile())expand(true);$('detail').scrollIntoView({block:'start',behavior:'instant'});}
function renderMarkers(){
 if(!map)return;markers.clearLayers();
 for(const r of data.resorts){const marker=L.marker(ll(r),{icon:L.divIcon({className:'pin resort',html:'<span class="pin-badge">'+esc(r.symbol)+'</span>',iconSize:[44,44],iconAnchor:[18,18]}),title:r.name,keyboard:true}).addTo(markers);marker.bindTooltip(esc(r.name),{permanent:r.id===trip.resort,direction:'right',offset:[14,0],className:'map-label'});marker.on('click',()=>{trip.resort=r.id;persist();render();});}
 for(const p of visible()){const marker=L.marker(ll(p),{icon:L.divIcon({className:'pin '+(p.status==='excluded'?'conflict ':'')+(p.id===selected?'active':''),html:'<span class="pin-badge">'+(p.kind==='lodging'?'R':p.number)+'</span>',iconSize:[44,44],iconAnchor:[18,18]}),title:p.name+': '+p.label,keyboard:true,zIndexOffset:p.id===selected?1000:0}).addTo(markers);marker.bindTooltip(esc(p.name),{direction:'top',offset:[0,-20],className:'map-label'});marker.on('click',()=>choose(p.id));}
}
function fit(){if(!map||!data)return;expand(false);map.invalidateSize();map.fitBounds(data.resorts.concat(inventory.places).map(ll),{paddingTopLeft:mobile()?[38,135]:[440,110],paddingBottomRight:mobile()?[40,Math.max(innerHeight*.30,205)+80]:[70,80],maxZoom:13,animate:false});}
function switchMap(mode){
 if(!map)return;if(baseLayer)map.removeLayer(baseLayer);
 const service=mode==='satellite'?'USGSImageryOnly':'USGSTopo';
 let failures=0;
 baseLayer=L.tileLayer('https://basemap.nationalmap.gov/arcgis/rest/services/'+service+'/MapServer/tile/{z}/{y}/{x}',{maxNativeZoom:16,maxZoom:19,minZoom:5,attribution:'Imagery / map: <a href="https://www.usgs.gov/programs/national-geospatial-program/national-map" target="_blank" rel="noopener noreferrer">USGS The National Map</a>',keepBuffer:1});
 baseLayer.on('tileerror',()=>{failures++;if(failures>=3){$('map-status').textContent='Some map tiles could not load. Try the other map style or check your connection. Place details remain available.';$('map-status').hidden=false;}});
 baseLayer.on('tileload',()=>{if(failures<3)$('map-status').hidden=true;});baseLayer.addTo(map);
 for(const id of ['satellite','terrain'])$(id).setAttribute('aria-pressed',String((mode==='satellite')===(id==='satellite')));
}
try{
 const load=async path=>{const r=await fetch(path,{cache:'no-store'});if(!r.ok)throw Error('Location data unavailable');return r.json();};
 [data,inventory]=await Promise.all([load('./destinations.json'),load('./overnight-options.json')]);
 if(inventory.schema_version!==1||!Array.isArray(inventory.places)||!Array.isArray(data.resorts))throw Error('Invalid location data');
 const ids=new Set();for(const p of inventory.places){if(!/^[a-z0-9_-]+$/.test(p.id)||ids.has(p.id)||!Array.isArray(p.coordinates)||p.coordinates.length!==2||!p.coordinates.every(Number.isFinite)||Math.abs(p.coordinates[0])>180||Math.abs(p.coordinates[1])>90)throw Error('Invalid location');ids.add(p.id);for(const url of [p.source,p.mapSource,p.access?.evidence?.source_url].filter(Boolean))if(!['https:','http:'].includes(new URL(url).protocol))throw Error('Invalid source');}
 if(!data.resorts.some(r=>r.id===trip.resort))trip.resort='aspen';
 if(!TripRules.tripDays(trip.arrive,trip.depart)){trip.arrive='2027-01-15';trip.depart='2027-01-17';}
 if(!['passenger_car','high_clearance','motorhome'].includes(trip.vehicle))trip.vehicle='passenger_car';
 for(const slot of ['a','b'])if(!ids.has(plan[slot]))plan[slot]=null;
 if(typeof L!=='undefined'){
 map=L.map('map',{zoomControl:false,minZoom:5,maxZoom:19,preferCanvas:true}).setView([39.18,-106.83],12);markers=L.layerGroup().addTo(map);L.control.scale({position:'bottomleft',imperial:true,metric:false}).addTo(map);switchMap('satellite');
 }else{$('map-status').textContent='Map library unavailable. You can still compare places below.';$('map-status').hidden=false;}
 $('satellite').onclick=()=>switchMap('satellite');$('terrain').onclick=()=>switchMap('terrain');$('fit').onclick=fit;$('zoom-in').onclick=()=>map?.zoomIn();$('zoom-out').onclick=()=>map?.zoomOut();
 render();fit();fillTrip();controlsReady(true);if(!map)for(const id of ['satellite','terrain','fit','zoom-in','zoom-out'])$(id).disabled=true;window.addEventListener('resize',()=>{map?.invalidateSize();});
}catch(error){controlsReady(false);$('results-summary').textContent='Location data could not load.';$('list').innerHTML='<p class="empty">Refresh to retry. No places can be evaluated until the location data loads.</p>';$('map-status').textContent='Location data unavailable. Refresh to retry.';$('map-status').hidden=false;}
})();
