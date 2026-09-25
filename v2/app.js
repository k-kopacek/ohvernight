(async()=>{
'use strict';
const $=id=>document.getElementById(id),esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const mobile=()=>matchMedia('(max-width:760px)').matches;
let map,markers,baseLayer,data,inventory,bundle=null,ridb=null,registry=null,coverage=null,places=[],kind='all',selected=null;
let pipelineLayers=new Map(),layerRecords=null,view='planner';
const enabledLayers=new Set(MapLayers.definitions.map(d=>d.id));
let trip={resort:'aspen',arrive:'2027-01-15',depart:'2027-01-17',vehicle:'passenger_car'},plan={a:null,b:null};
const storageKey='ohvernight-trip-v1';
function controlsReady(ready){document.querySelectorAll('button').forEach(b=>{if(b.id!=='sheet-toggle')b.disabled=!ready;});}
controlsReady(false);
try{const saved=JSON.parse(localStorage.getItem(storageKey)||'null');if(saved){trip={...trip,...saved.trip};plan={...plan,...saved.plan};}}catch{}
function persist(){try{localStorage.setItem(storageKey,JSON.stringify({trip,plan}));}catch{}}
function setView(next){view=next;document.body.dataset.view=next;$('landing').hidden=next!=='planner';if(next==='map')setTimeout(()=>{map?.invalidateSize();fit();},30);}
function fillLandingTrip(){for(const key of ['resort','arrive','depart','vehicle'])$('landing-'+key).value=trip[key];}
function applyTrip(next,errorId='landing-error'){if(!TripRules.tripDays(next.arrive,next.depart)){$(errorId).textContent='Choose a departure after arrival, within 366 nights.';$(errorId).hidden=false;return false;}trip=next;persist();$('trip-error').hidden=true;$('landing-error').hidden=true;setView('map');render();fit();return true;}
const ll=p=>[p.coordinates[1],p.coordinates[0]];
const resort=()=>data.resorts.find(r=>r.id===trip.resort);
const distance=p=>map?map.distance(ll(p),ll(resort()))/1609.344:null;
const distanceText=p=>distance(p)===null?'Distance unavailable':distance(p).toFixed(1)+' mi direct';
const type=p=>({campground:'CAMPGROUND',dispersed:'DISPERSED AREA',lodging:'ROOM BACKUP'}[p.kind]||'LOCATION');
const visible=()=>places.filter(p=>(kind==='all'||p.kind===kind)&&($('show-conflicts').checked||p.status!=='excluded'));
function expand(value){$('sheet').classList.toggle('expanded',value);document.body.classList.toggle('sheet-open',value);$('sheet-toggle').setAttribute('aria-expanded',String(value));$('sheet-action').textContent=value?'More map ↓':'Explore stays ↑';document.querySelector('.sheet-body').inert=mobile()&&!value;}
$('sheet-toggle').addEventListener('click',()=>expand(!$('sheet').classList.contains('expanded')));
fillLandingTrip();
document.body.dataset.view=view;
$('landing-trip-form').onsubmit=event=>{event.preventDefault();const next=Object.fromEntries(['resort','arrive','depart','vehicle'].map(k=>[k,$('landing-'+k).value]));applyTrip(next);};
$('landing-explore').onclick=()=>{setView('map');render();fit();};
$('back-planner').onclick=()=>{fillLandingTrip();setView('planner');};
function fillTrip(){for(const key of ['resort','arrive','depart','vehicle'])$(key).value=trip[key];}
$('edit-trip').onclick=()=>{fillTrip();$('trip-error').hidden=true;$('trip-dialog').showModal();};
$('close-trip').onclick=()=>$('trip-dialog').close();
$('trip-form').onsubmit=event=>{event.preventDefault();const next=Object.fromEntries(['resort','arrive','depart','vehicle'].map(k=>[k,$(k).value]));if(applyTrip(next,'trip-error'))$('trip-dialog').close();};
function setKind(value){kind=value;document.querySelectorAll('[data-kind]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.kind===value)));render();}
document.querySelectorAll('[data-kind]').forEach(b=>b.onclick=()=>setKind(b.dataset.kind));
$('show-conflicts').onchange=()=>render();
function selectedDetails(){
 const p=places.find(p=>p.id===selected);
 if(!p){$('detail').innerHTML='';return;}
 const directions='https://www.google.com/maps/dir/?api=1&destination='+encodeURIComponent(p.coordinates[1]+','+p.coordinates[0]);
 const listingLabel=p.kind==='lodging'?'Official site & booking ↗':p.source_is_search?'Find official listing on Recreation.gov ↗':'Official listing & camping details ↗';
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
 places=inventory.places.map(p=>TripRules.evaluate(Trust.applyRules(p,registry),trip));
 const shown=visible().sort((a,b)=>(a.status==='excluded')-(b.status==='excluded') || (distance(a)||0)-(distance(b)||0));
 if(!shown.some(p=>p.id===selected))selected=shown[0]?.id||null;
 const conflicts=places.filter(p=>p.status==='excluded').length;
 $('results-summary').textContent=places.length+' sourced places · '+conflicts+' trip conflicts';
 const fmt=s=>new Date(s+'T12:00:00Z').toLocaleDateString('en-US',{month:'short',day:'numeric',timeZone:'UTC'});
 $('trip-caption').textContent=resort().name+' · '+fmt(trip.arrive)+'–'+fmt(trip.depart);
 $('trip-insight').innerHTML='<strong>No confirmed vehicle overnights yet.</strong><span>'+conflicts+(conflicts===1?' place conflicts':' places conflict')+' with this trip. Other camping options still need access and permission checks.</span><br><button class="text-button" id="room-backups">Explore a room backup →</button>';
 $('room-backups').onclick=()=>{setKind('lodging');expand(true);};
 $('list').innerHTML=shown.length?shown.map(p=>'<button class="place-card" data-place="'+p.id+'" aria-pressed="'+(p.id===selected)+'"><span class="card-top"><span>'+esc(type(p))+'</span><span class="distance">'+esc(distanceText(p))+'</span></span><h3>'+esc(p.name)+'</h3><span class="status '+(p.status==='excluded'?'conflict':'')+'">'+esc(p.label)+'</span></button>').join(''):'<p class="empty">No places match. Try another stay type or include conflicts.</p>';
 $('list').querySelectorAll('[data-place]').forEach(b=>b.onclick=()=>choose(b.dataset.place));
 renderPlan();selectedDetails();renderMarkers();renderSourceHealth();renderPipelineLayers();
}
function renderSourceHealth(){
 const summary=Trust.sourceSummary(bundle,ridb);
 $('source-health-content').innerHTML='<p class="trust-warning">'+esc(summary.fire)+'</p><p>'+esc(summary.closures)+'</p><p>'+esc(summary.inventory)+'</p><a href="https://www.fs.usda.gov/r02/whiteriver/alerts" target="_blank" rel="noopener noreferrer">Forest Service alerts ↗</a> · <a href="https://pitkincounty.com/CivicAlerts.asp" target="_blank" rel="noopener noreferrer">Pitkin County notices ↗</a>';
 $('source-health').dataset.state=summary.fireState;
 document.querySelectorAll('.place-card').forEach(card=>{const badge=document.createElement('span');badge.className='confidence-badge';badge.textContent='Official listing · trip needs confirmation';card.appendChild(badge);});
 const p=places.find(p=>p.id===selected);
 if(p?.ruleReview){const warning=document.createElement('p');warning.className='trust-warning';warning.textContent=p.ruleReview;$('detail').appendChild(warning);}
}
function choose(id){kind='all';$('show-conflicts').checked=true;document.querySelectorAll('[data-kind]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.kind==='all')));selected=id;render();const p=places.find(p=>p.id===selected);if(p&&map){expand(false);map.panTo(ll(p),{animate:!matchMedia('(prefers-reduced-motion:reduce)').matches});}if(mobile())expand(true);$('detail').scrollIntoView({block:'start',behavior:'instant'});}
function renderMarkers(){
 if(!map)return;markers.clearLayers();
 if(enabledLayers.has('resorts'))for(const r of data.resorts){const marker=L.marker(ll(r),{icon:L.divIcon({className:'pin resort',html:'<span class="pin-badge">'+esc(r.symbol)+'</span>',iconSize:[44,44],iconAnchor:[18,18]}),title:r.name,keyboard:true}).addTo(markers);marker.on('click',()=>{trip.resort=r.id;persist();render();});}
 if(enabledLayers.has('places'))for(const p of places){const marker=L.marker(ll(p),{icon:L.divIcon({className:'pin '+(p.status==='excluded'?'conflict ':'')+(p.id===selected?'active':''),html:'<span class="pin-badge">'+esc(p.kind==='lodging'?'R':p.number)+'</span>',iconSize:[44,44],iconAnchor:[18,18]}),title:p.name+': '+p.label,keyboard:true,zIndexOffset:p.id===selected?1000:0}).addTo(markers);marker.on('click',()=>choose(p.id));}
}
function layerPopup(feature,definition){
 const p=feature.properties||{}, evidence=p.evidence||{};
 let extra='';
 if(definition.id==='roads'){
   extra='<p>Current road conditions and vehicle suitability are unconfirmed.</p>';
   if(p.operational_maintenance_level)extra+='<p>Agency maintenance classification: '+esc(p.operational_maintenance_level)+'</p>';
   if(p.designations)extra+='<details><summary>Published vehicle seasons</summary>'+Object.entries(p.designations).map(([vehicle,r])=>'<p>'+esc(({passenger_car:'Passenger car / SUV',high_clearance:'High-clearance vehicle',motorhome:'Motorhome / RV'})[vehicle]||vehicle)+': '+esc(r.dates_open||'Dates not provided')+' · '+esc(r.designation)+'</p>').join('')+'</details>';
 }
 if(definition.id==='candidates')extra='<p>No campsite or camping permission has been confirmed. Screening snapshot: '+esc(bundle?.trip?.arrive)+'–'+esc(bundle?.trip?.depart)+' ('+esc(bundle?.trip?.vehicle?.replaceAll('_',' '))+'). This is not an assessment of your selected trip.</p>';
 let source='';try{const u=new URL(evidence.source_url);if(['https:','http:'].includes(u.protocol))source='<a href="'+esc(u.href)+'" target="_blank" rel="noopener noreferrer">Open source ↗</a>';}catch{}
 return '<div class="layer-popup"><strong>'+esc(p.name||p.manager||definition.title)+'</strong><p>'+esc(definition.description)+'</p>'+extra+(evidence.retrieved_at?'<p>Source fetched '+esc(evidence.retrieved_at.slice(0,10))+'.</p>':'')+source+'</div>';
}
function renderPipelineLayers(){
 if(!layerRecords){
   layerRecords=MapLayers.describe(bundle,coverage,inventory.places.length,data.resorts.length);
   $('legend-layers').innerHTML=layerRecords.map(d=>'<div class="legend-toggle"><input type="checkbox" id="layer-'+d.id+'" checked><span aria-hidden="true" class="swatch '+(d.kind||'area')+'" style="--swatch:'+d.color+'"></span><label for="layer-'+d.id+'"><strong>'+d.title+'</strong><small>'+d.description+'</small><small class="layer-count">'+esc(d.status)+'</small>'+(d.fetched?'<small>Fetched '+esc(d.fetched.slice(0,10))+'</small>':'')+'</label><button type="button" data-fit-layer="'+d.id+'" aria-label="Show '+d.title+' on map" '+(!d.count||!map?'disabled':'')+'>View</button></div>').join('');
   for(const d of layerRecords){
     $('layer-'+d.id).onchange=()=>{if($('layer-'+d.id).checked)enabledLayers.add(d.id);else enabledLayers.delete(d.id);renderMarkers();renderPipelineLayers();};
     if(!map||d.kind==='pins'||!d.records.length)continue;
     const style={color:d.color,weight:d.id==='roads'?3:d.id==='water'?1.3:2,opacity:.9,fill:d.id!=='coverage',fillColor:d.color,fillOpacity:d.id==='water'?.12:.10,...(d.kind==='dashed'?{dashArray:'7 5'}:{})};
     const layer=L.geoJSON({type:'FeatureCollection',features:d.records},{style,interactive:d.id!=='coverage',pointToLayer:(f,latlng)=>L.circleMarker(latlng,{...style,radius:7,fillOpacity:.7}),onEachFeature:(f,l)=>{if(d.id!=='coverage')l.bindPopup(layerPopup(f,d),{maxWidth:280});}});
     pipelineLayers.set(d.id,layer);
   }
   document.querySelectorAll('[data-fit-layer]').forEach(b=>b.onclick=()=>{
     const id=b.dataset.fitLayer;enabledLayers.add(id);$('layer-'+id).checked=true;renderMarkers();renderPipelineLayers();expand(false);
     $('map-legend').close();
     const bounds=id==='places'?L.latLngBounds(inventory.places.map(ll)):id==='resorts'?L.latLngBounds(data.resorts.map(ll)):pipelineLayers.get(id)?.getBounds();
     if(bounds?.isValid())map.fitBounds(bounds,{paddingTopLeft:mobile()?[25,155]:[425,95],paddingBottomRight:mobile()?[25,190]:[45,85],maxZoom:14});
   });
 }
 if(map)for(const [id,layer] of pipelineLayers){if(enabledLayers.has(id)){if(!map.hasLayer(layer))layer.addTo(map);}else if(map.hasLayer(layer))map.removeLayer(layer);}
 if(map&&enabledLayers.has('roads'))pipelineLayers.get('roads')?.bringToFront();
 $('layer-trip-status').textContent=bundle?'Research snapshot: '+(bundle.generated_at||'Unknown date').slice(0,10)+'. Roads and research areas stay visible for every trip. Research areas were screened for '+bundle.trip.arrive+'–'+bundle.trip.depart+' ('+bundle.trip.vehicle.replaceAll('_',' ')+'); camping permission remains unknown.':'Research map data is not loaded. Overnight listings are still available.';
 $('inventory-status').textContent=ridb?'RIDB: '+ridb.places.length+' imported facility records. '+Trust.sourceSummary(bundle,ridb).inventory:'RIDB: no campground import loaded yet. Only the manually researched listings are shown.';
}
function fit(){if(!map||!data)return;expand(false);map.invalidateSize();map.fitBounds(data.resorts.concat(inventory.places).map(ll),{paddingTopLeft:mobile()?[38,155]:[440,110],paddingBottomRight:mobile()?[40,190]:[70,80],maxZoom:13,animate:false});}
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
 const optional=async path=>{try{return await load(path);}catch{return null;}};
 [data,inventory,bundle,ridb,registry,coverage]=await Promise.all([load('./destinations.json'),load('./overnight-options.json'),optional('./map-data-v2.json'),optional('./ridb-options.json'),optional('./pipeline/config/rules-registry.json'),optional('./pipeline/config/aoi.geojson')]);
 if(inventory.schema_version!==1||!Array.isArray(inventory.places)||!Array.isArray(data.resorts))throw Error('Invalid location data');
 if(bundle?.schema_version!==2||!bundle.trip||!bundle.layers)bundle=null;
 if(ridb?.schema_version===1&&Array.isArray(ridb.places)){
   const existing=new Set(inventory.places.map(p=>p.ridb_facility_id).filter(Boolean));
   inventory.places.push(...ridb.places.filter(p=>!existing.has(p.ridb_facility_id)));
 }else ridb=null;
 const ids=new Set();for(const p of inventory.places){if(!/^[a-z0-9_-]+$/.test(p.id)||ids.has(p.id)||!Array.isArray(p.coordinates)||p.coordinates.length!==2||!p.coordinates.every(Number.isFinite)||Math.abs(p.coordinates[0])>180||Math.abs(p.coordinates[1])>90)throw Error('Invalid location');ids.add(p.id);for(const url of [p.source,p.mapSource,p.access?.evidence?.source_url].filter(Boolean))if(!['https:','http:'].includes(new URL(url).protocol))throw Error('Invalid source');}
 if(!data.resorts.some(r=>r.id===trip.resort))trip.resort='aspen';
 if(!TripRules.tripDays(trip.arrive,trip.depart)){trip.arrive='2027-01-15';trip.depart='2027-01-17';}
 if(!['passenger_car','high_clearance','motorhome'].includes(trip.vehicle))trip.vehicle='passenger_car';
 for(const slot of ['a','b'])if(!ids.has(plan[slot]))plan[slot]=null;
 if(typeof L!=='undefined'){
 map=L.map('map',{zoomControl:false,minZoom:5,maxZoom:19,preferCanvas:true}).setView([39.18,-106.83],12);markers=L.layerGroup().addTo(map);L.control.scale({position:'bottomleft',imperial:true,metric:false}).addTo(map);switchMap('satellite');
 }else{$('map-status').textContent='Map library unavailable. You can still compare places below.';$('map-status').hidden=false;}
 $('satellite').onclick=()=>switchMap('satellite');$('terrain').onclick=()=>switchMap('terrain');$('fit').onclick=fit;$('zoom-in').onclick=()=>map?.zoomIn();$('zoom-out').onclick=()=>map?.zoomOut();
 $('open-layers').onclick=()=>$('map-legend').showModal();
 $('legend-close').onclick=()=>$('map-legend').close();
 matchMedia('(max-width:760px)').addEventListener('change',()=>expand($('sheet').classList.contains('expanded')));
 render();fit();fillTrip();fillLandingTrip();controlsReady(true);document.querySelectorAll('[data-fit-layer]').forEach(b=>b.disabled=!map||!layerRecords.find(d=>d.id===b.dataset.fitLayer)?.count);if(!map)for(const id of ['satellite','terrain','fit','zoom-in','zoom-out'])$(id).disabled=true;window.addEventListener('resize',()=>{map?.invalidateSize();});
 setInterval(()=>render(),60000);
}catch(error){controlsReady(false);$('landing-error').textContent='Location data could not load. Refresh to retry.';$('landing-error').hidden=false;$('results-summary').textContent='Location data could not load.';$('list').innerHTML='<p class="empty">Refresh to retry. No places can be evaluated until the location data loads.</p>';$('map-status').textContent='Location data unavailable. Refresh to retry.';$('map-status').hidden=false;}
})();
