
(async()=>{
const root=document.getElementById('aspen-overnight');
const el=id=>root.querySelector('#'+id);
let data, inventory;
try {
 const load=async path=>{const r=await fetch(path,{cache:'no-store'});if(!r.ok)throw new Error(path);return r.json();};
 [data,inventory]=await Promise.all([load('./map-data.json'),load('./overnight-options.json')]);
 if(inventory.schema_version!==1 || !Array.isArray(inventory.places))throw new Error('Inventory format');
 const ids=new Set();
 for(const p of inventory.places){
  if(!/^[a-z0-9_-]+$/.test(p.id)||ids.has(p.id)||!Array.isArray(p.coordinates)||p.coordinates.length!==2||!p.coordinates.every(Number.isFinite)||Math.abs(p.coordinates[0])>180||Math.abs(p.coordinates[1])>90)throw new Error('Invalid location');
  ids.add(p.id);
  for(const url of [p.source,p.mapSource,p.access?.evidence?.source_url].filter(Boolean))if(!['https:','http:'].includes(new URL(url).protocol))throw new Error('Invalid source');
 }
 data.places=inventory.places;
 el('ap-source-status').textContent=inventory.notice;
} catch(error) {
 el('ap-loading').textContent='Location data could not load. Refresh to retry.';
 el('ap-source-status').textContent='Data unavailable. No locations or permissions can be evaluated.';
 return;
}
const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
let destination='aspen',selected='difficult',projection,zoom,camera,width=0,height=0,validDates=true;
const design={panel:'side',minorRoads:true};
const currentResort=()=>data.resorts.find(r=>r.id===destination);
const currentPlace=()=>data.places.find(p=>p.id===selected);
const visiblePlaces=()=>data.places.filter(p=>(el('ap-kind').value==='all'||p.kind===el('ap-kind').value)&&(p.status!=='excluded'||el('ap-show-excluded').checked));
const distance=p=>typeof d3==='undefined'?null:d3.geoDistance(p.coordinates,currentResort().coordinates)*3958.7613;
const distanceText=p=>distance(p)===null?'Map distance unavailable':distance(p).toFixed(1)+' mi straight line';
function dates(){
 const start=el('ap-arrive').value,end=el('ap-depart').value;
 validDates=Boolean(TripRules.tripDays(start,end));
 el('ap-error').hidden=validDates;
 el('ap-error').textContent='Choose a departure after arrival, within 366 nights.';
 const fmt=s=>new Date(s+'T12:00:00Z').toLocaleDateString('en-US',{month:'short',day:'numeric',year:'numeric',timeZone:'UTC'});
 el('ap-trip-summary').textContent=validDates?fmt(start)+' – '+fmt(end):'Check your dates';
}
function details(){
 const p=currentPlace(),r=currentResort();
 if(!p){el('ap-detail').innerHTML='<p>No locations match these filters. Try another category or show mismatches.</p>';return;}
 el('ap-detail').innerHTML='<h3>'+esc(p.name)+'</h3><span class="ap-status '+(p.status==='excluded'?'blocked':'')+'">'+esc(p.label)+'</span><dl><dt>Relative to '+esc(r.name)+'</dt><dd>'+esc(distanceText(p))+'</dd><dt>Road distance / drive time</dt><dd>Not calculated</dd><dt>For your dates and vehicle</dt><dd>'+esc(p.tripNote)+'</dd></dl><p>'+esc(p.note)+'</p><p><strong>Still to confirm:</strong> '+esc(p.unknowns.join(' · '))+'</p><details><summary>Sources and last review</summary><p><a target="_blank" rel="noopener noreferrer" href="'+esc(p.source)+'">Official listing / booking information</a></p><p>Listing reviewed '+esc(p.checked_on)+'. This does not confirm availability or current conditions.</p>'+(p.access?'<p><a target="_blank" rel="noopener noreferrer" href="'+esc(p.access.evidence.source_url)+'">USFS vehicle designation</a> · '+esc(p.access.id)+' · retrieved '+esc(p.access.evidence.retrieved_at.slice(0,10))+'</p>':'')+'<p><a target="_blank" rel="noopener noreferrer" href="'+esc(p.mapSource)+'">Location source</a> · '+esc(p.locationBasis)+'.</p></details>';
}
function list(){
 el('ap-list').innerHTML=visiblePlaces().map(p=>'<button class="ap-choice" type="button" data-place="'+p.id+'" aria-pressed="'+(selected===p.id)+'"><strong>'+p.number+'. '+esc(p.name)+'</strong><span>'+esc(p.label)+' · '+esc(distanceText(p))+'</span></button>').join('');
}
function pinMarkup(){
 el('ap-pins').innerHTML=data.resorts.map(r=>'<button class="ap-pin ap-resort" type="button" data-resort="'+r.id+'" aria-label="Select '+esc(r.name)+'" aria-pressed="'+(destination===r.id)+'"><span class="ap-marker">'+r.symbol+'</span><span class="ap-pinlabel">'+esc(r.name)+'</span></button>').join('')+visiblePlaces().map(p=>'<button class="ap-pin ap-place '+(p.status==='excluded'?'ap-excluded':'')+'" type="button" data-place="'+p.id+'" aria-label="Select '+esc(p.name)+': '+esc(p.label)+'" aria-pressed="'+(selected===p.id)+'"><span class="ap-marker">'+p.number+'</span>'+(selected===p.id?'<span class="ap-pinlabel">'+esc(p.name)+'</span>':'')+'</button>').join('');
 positionPins();
}
function positionPins(){
 if(!projection||!camera)return;
 for(const button of el('ap-pins').querySelectorAll('button')){
  const record=button.dataset.resort?data.resorts.find(p=>p.id===button.dataset.resort):data.places.find(p=>p.id===button.dataset.place);
  const point=camera.apply(projection(record.coordinates));
  button.style.transform='translate('+(point[0]-22)+'px,'+(point[1]-22)+'px)';
  button.hidden=point[0]<0||point[1]<0||point[0]>width||point[1]>height;
  const label=button.querySelector('.ap-pinlabel');
  if(label){label.style.left=point[0]<100?'0':point[0]>width-100?'100%':'50%';label.style.transform=point[0]<100?'none':point[0]>width-100?'translateX(-100%)':'translateX(-50%)';}
 }
 const a=projection.invert(camera.invert([30,height-25])),b=projection.invert(camera.invert([130,height-25]));
 const miles=d3.geoDistance(a,b)*3958.7613;
 const step=[.1,.25,.5,1,2,5,10].filter(n=>n<=miles).pop()||.1;
 el('ap-scale').innerHTML='<span style="width:'+(100*step/miles).toFixed(1)+'px"></span>'+step+' mi';
}
function draw(){
 if(typeof d3==='undefined')return;
 width=el('ap-map').clientWidth;height=el('ap-map').clientHeight;
 if(!width||!height)return;
 const fitCoordinates=data.resorts.concat(data.places).map(p=>p.coordinates);
 const horizontalPadding=width<480?20:35;
 projection=d3.geoMercator().fitExtent([[horizontalPadding,65],[width-horizontalPadding,height-45]],{type:'MultiPoint',coordinates:fitCoordinates});
 const path=d3.geoPath(projection);
 const svg=d3.select(el('ap-svg')).attr('viewBox','0 0 '+width+' '+height);
 const base=d3.select(el('ap-geography'));base.selectAll('*').remove();
 base.append('g').selectAll('path').data(data.waterways.features).join('path').attr('d',path).attr('fill','none').attr('stroke','var(--ap-river)').attr('stroke-width',1.4).attr('vector-effect','non-scaling-stroke');
 const main=data.roads.features.filter(f=>f.properties.kind==='major');
 if(design.minorRoads)base.append('g').selectAll('path').data(data.roads.features.filter(f=>f.properties.kind==='minor')).join('path').attr('d',path).attr('fill','none').attr('stroke','var(--ap-road)').attr('stroke-width',.8).attr('vector-effect','non-scaling-stroke');
 base.append('g').selectAll('path').data(main).join('path').attr('d',path).attr('fill','none').attr('stroke','var(--ap-casing)').attr('stroke-width',6).attr('vector-effect','non-scaling-stroke');
 base.append('g').selectAll('path').data(main).join('path').attr('d',path).attr('fill','none').attr('stroke','var(--ap-major)').attr('stroke-width',2.5).attr('vector-effect','non-scaling-stroke');
 if(!zoom){
  camera=d3.zoomIdentity;
  zoom=d3.zoom().scaleExtent([1,6]).filter(event=>event.type==='wheel'?event.ctrlKey:(!event.button)).on('zoom',event=>{camera=event.transform;base.attr('transform',camera);positionPins();});
  svg.call(zoom).on('dblclick.zoom',null);
 }
 zoom.extent([[0,0],[width,height]]).translateExtent([[-width*.4,-height*.4],[width*1.4,height*1.4]]);
 svg.call(zoom.transform,camera);
 el('ap-loading').hidden=true;
 positionPins();
}
function refresh(){
 dates();
 const trip={arrive:el('ap-arrive').value,depart:el('ap-depart').value,vehicle:el('ap-vehicle').value};
 data.places=inventory.places.map(p=>TripRules.evaluate(p,trip));
 if(!visiblePlaces().some(p=>p.id===selected))selected=visiblePlaces()[0]?.id||null;
 list();details();pinMarkup();
}
function chooseResort(id){destination=id;el('ap-resort').value=id;refresh();if(zoom)d3.select(el('ap-svg')).call(zoom.transform,d3.zoomIdentity);}
function choosePlace(id){selected=id;refresh();if(zoom){const point=camera.apply(projection(currentPlace().coordinates));if(point[0]<24||point[1]<24||point[0]>width-24||point[1]>height-24)d3.select(el('ap-svg')).call(zoom.transform,d3.zoomIdentity);}}
root.addEventListener('click',event=>{const button=event.target.closest('button');if(!button)return;const scope=button.classList.contains('ap-pin')?'#ap-pins':'#ap-list';if(button.dataset.resort){const id=button.dataset.resort;chooseResort(id);root.querySelector('#ap-pins [data-resort="'+id+'"]').focus({preventScroll:true});}else if(button.dataset.place){const id=button.dataset.place;choosePlace(id);root.querySelector(scope+' [data-place="'+id+'"]').focus({preventScroll:true});}});
el('ap-resort').addEventListener('change',()=>chooseResort(el('ap-resort').value));
el('ap-arrive').addEventListener('change',refresh);el('ap-depart').addEventListener('change',refresh);
for(const id of ['ap-show-excluded','ap-vehicle','ap-kind'])el(id).addEventListener('change',refresh);
el('ap-in').addEventListener('click',()=>{if(zoom)d3.select(el('ap-svg')).call(zoom.scaleBy,1.6);});
el('ap-out').addEventListener('click',()=>{if(zoom)d3.select(el('ap-svg')).call(zoom.scaleBy,1/1.6);});
el('ap-fit').addEventListener('click',()=>{if(zoom)d3.select(el('ap-svg')).call(zoom.transform,d3.zoomIdentity);});
refresh();
if(typeof d3==='undefined'){el('ap-loading').textContent='Map library unavailable. The place list and source links remain available.';for(const id of ['ap-in','ap-out','ap-fit'])el(id).disabled=true;}
else{draw();new ResizeObserver(draw).observe(el('ap-map'));}
})();
