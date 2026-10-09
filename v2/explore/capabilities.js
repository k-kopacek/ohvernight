(function(scope){
 'use strict';
 const T=typeof require==='function'?require('../trail-discovery.js'):scope.TrailDiscovery;
 const R=typeof require==='function'?require('../trip-rules.js'):scope.TripRules;
 const Trust=typeof require==='function'?require('../trust.js'):scope.Trust;
 function inventory(region){
  const entries=region.registry.filter(x=>x.format==='place_list'&&x.kind==='overnight_inventory');
  const output=[],facilities=new Set();
  for(const entry of entries)for(const place of Array.isArray(region.places[entry.id])?region.places[entry.id]:[]){
   if(place.ridb_facility_id&&facilities.has(place.ridb_facility_id))continue;
   if(place.ridb_facility_id)facilities.add(place.ridb_facility_id);
   output.push({place,entry});
  }
  return output;
 }
 function evaluate(region,trip,today,now){return inventory(region).map(({place,entry})=>R.evaluate(Trust.applyRules(place,region.rules,now),trip,today,{max_age_hours:entry.maxAgeHours}));}
 function sourceSummary(region,now){
  const entry=region.registry.find(x=>x.kind==='restriction_monitor');
  const ridb=region.registry.find(x=>x.format==='place_list'&&x.statusRef);
  return Trust.sourceSummary({layers:{fire_restriction_stage:region.layers.get(entry?.id)?.data}},region.placeDocuments?.[ridb?.id],now);
 }
 function sourceLinkLabel(place){return place.source_is_search?'Source search ↗':'Source ↗';}
 function attach(shell){
  const region=shell.region,config=region.config,caps=config.capabilities;
  if(!caps.trip_planner)return caps.trail_season_check?scope.ExploreBrowse.attach(shell):null;
  const {element:el,button,$}=shell,M=scope.ExploreMap,E=scope.ExploreEvidence;
  const read=(key,fallback)=>{try{return JSON.parse(localStorage.getItem(key))||fallback;}catch{return fallback;}};
  const stored=read(config.storage_keys.trip,{});
  let trip={...config.trip_defaults,...stored.trip},plan={a:null,b:null,...stored.plan},places=[],kind='all',conflicts=true,lastAdventure='',filterOpen=false,healthOpen=false;
  const destinationEntry=region.registry.find(x=>x.kind==='destinations'),resorts=region.places[destinationEntry?.id]||[];
  if(!resorts.some(r=>r.id===trip.resort))trip.resort=config.trip_defaults.resort;
  if(!R.tripDays(trip.arrive,trip.depart)){trip.arrive=config.trip_defaults.arrive;trip.depart=config.trip_defaults.depart;}
  if(!['passenger_car','high_clearance','motorhome'].includes(trip.vehicle))trip.vehicle=config.trip_defaults.vehicle;
  const ids=new Set(inventory(region).map(x=>x.place.id));for(const slot of ['a','b'])if(!ids.has(plan[slot]))plan[slot]=null;
  const persist=()=>{try{localStorage.setItem(config.storage_keys.trip,JSON.stringify({trip,plan}));}catch{}};
  const trailEntry=()=>region.registry.find(x=>x.kind==='trails'),trails=()=>region.layers.get(trailEntry()?.id)?.data?.features||[];
  const link=(label,url)=>{const node=el('a',label),safe=E.safeUrl(url);if(!safe)return el('p','Source link unavailable');node.href=safe;node.target='_blank';node.rel='noopener noreferrer';return node;};
  const paragraph=(box,text)=>box.append(el('p',text));
  function dialog(title){
   const node=el('dialog',undefined,'explore-dialog'),heading=el('div',undefined,'explore-heading'),body=el('div');
   const close=button('×',()=>node.close());close.setAttribute('aria-label','Close '+title);heading.append(el('h1',title),close);node.append(heading,body);shell.$('map').parentNode.append(node);node.addEventListener('close',()=>node.opener?.focus());
   return {node,body,show(){node.opener=document.activeElement;shell.openDialog(node);}};
  }
  const settings=dialog('Where are you headed?'),adventure=dialog('Camping and trails by straight-line distance');
  const landing=el('section',undefined,'explore-landing');landing.id='landing';shell.$('map').parentNode.append(landing);
  const card=el('div',undefined,'explore-landing-card');landing.append(card);
  card.append(el('span',config.landing.eyebrow),el('h1',config.landing.title),el('p',config.landing.lead),el('p',config.landing.note));
  function field(form,label,id,type,options,value){
   const row=el('label',label),control=el(type==='select'?'select':'input');control.id=id;
   if(type==='select')for(const [key,text] of options){const option=el('option',text);option.value=key;control.append(option);}
   else{control.type=type;control.required=true;}
   control.value=value;row.append(control);form.append(row);return control;
  }
  function tripForm(box,prefix,withActivity){
   const form=el('form'),fields={},error=el('p');error.hidden=true;error.setAttribute('role','alert');box.append(form);
   fields.resort=field(form,'Mountain',prefix+'resort','select',config.landing.mountains.map(x=>[x.value,x.label]),trip.resort);
   fields.arrive=field(form,'Arrive',prefix+'arrive','date',[],trip.arrive);fields.depart=field(form,'Depart',prefix+'depart','date',[],trip.depart);
   fields.vehicle=field(form,'Your vehicle',prefix+'vehicle','select',[['passenger_car','Passenger car / SUV'],['high_clearance','High-clearance vehicle'],['motorhome','Motorhome / RV']],trip.vehicle);
   if(withActivity)fields.activity=field(form,'What would you like to do?',prefix+'activity','select',[['','Just find an overnight stay'],...Object.entries(T.activities)],'');
   const submit=el('button',withActivity?'Find my adventure →':'Update my trip →');submit.type='submit';form.append(error,submit);
   form.onsubmit=event=>{event.preventDefault();const next=Object.fromEntries(['resort','arrive','depart','vehicle'].map(k=>[k,fields[k].value]));
    if(!R.tripDays(next.arrive,next.depart)){error.textContent='Choose a departure after arrival, within 366 nights.';error.hidden=false;return;}
    trip=next;persist();error.hidden=true;landing.hidden=true;settings.node.close();render();if(fields.activity?.value)showAdventure(fields.activity.value);};
   return fields;
  }
  const landingFields=tripForm(card,'landing-',true),settingsFields=tripForm(settings.body,'trip-',false);
  const explore=button(config.landing.explore_label,()=>{landing.hidden=true;M.fit(scope.ExploreShell.bounds(region.coverage));});explore.id='landing-explore';card.append(explore);
  for(const item of config.landing.region_links||[]){const node=el('a',item.label);node.href='?region='+encodeURIComponent(item.region_id)+'&view=map';card.append(node);}
  paragraph(card,'The map helps you research. It does not replace the official source, current conditions, or local confirmation.');
  landing.hidden=new URLSearchParams(scope.location.search).get('view')==='map';
  document.addEventListener('keydown',event=>{if(event.key==='Escape'&&!landing.hidden&&!document.querySelector('dialog[open]')){landing.hidden=true;$('sheet-toggle').focus();}});
  const tools=el('div',undefined,'explore-planner-tools');shell.$('sheet-header')?.append(tools);
  const toolbar=el('div');toolbar.append(button('Plan a trip',()=>{for(const k of Object.keys(settingsFields))settingsFields[k].value=trip[k];settings.show();}),button('Change my adventure',()=>{landing.hidden=false;for(const k of ['resort','arrive','depart','vehicle'])landingFields[k].value=trip[k];}));
  function entryFor(place){return inventory(region).find(x=>x.place.id===place.id)?.entry;}
  function showPlace(place){shell.showDetail(entryFor(place),place);}
  const resort=()=>resorts.find(x=>x.id===trip.resort);
  function miles(place){const a=place.coordinates,b=resort()?.coordinates;if(!b)return Infinity;const rad=Math.PI/180,dlat=(a[1]-b[1])*rad,dlon=(a[0]-b[0])*rad,h=Math.sin(dlat/2)**2+Math.cos(a[1]*rad)*Math.cos(b[1]*rad)*Math.sin(dlon/2)**2;return 6371000*2*Math.atan2(Math.sqrt(h),Math.sqrt(1-h))/1609.344;}
  function result(place){const node=button('',()=>showPlace(place));node.className='explore-result';node.dataset.place=place.id;node.append(el('strong',place.name),el('small',place.label),el('small',miles(place).toFixed(1)+' mi straight-line'),el('small','Sourced listing · trip needs confirmation'));return node;}
  function render(){
   places=evaluate(region,trip);const box=$('list-body');box.replaceChildren(toolbar);
   const failed=region.registry.filter(x=>x.format==='place_list'&&x.kind==='overnight_inventory').some(x=>!Array.isArray(region.places[x.id]));
   const count=places.filter(p=>p.status==='excluded').length;$('summary').textContent=failed?'Listings could not load':places.length+' sourced places · '+count+' trip conflicts';
   if(failed)paragraph(box,'Listings could not load');
   const health=el('details'),summary=el('summary','What has been checked?');health.open=healthOpen;health.ontoggle=()=>{healthOpen=health.open;};health.append(summary);
   paragraph(health,'No confirmed vehicle overnights yet.');paragraph(health,count+(count===1?' place conflicts':' places conflict')+' with this trip. Other camping options still need access and permission checks.');
   box.append(button('Explore a room backup →',()=>{kind='lodging';render();}));
   for(const key of ['fire','closures','inventory'])paragraph(health,sourceSummary(region)[key]);box.append(health);
   const panel=el('details',undefined,'explore-filters');panel.open=filterOpen;panel.ontoggle=()=>{filterOpen=panel.open;};panel.append(el('summary','Filters'));const filters=el('nav');filters.setAttribute('aria-label','Stay type');for(const [value,label] of [['all','All'],['campground','Campgrounds'],['dispersed','Dispersed'],['lodging','Rooms']]){const node=button(label,()=>{kind=value;filterOpen=panel.open;render();});node.setAttribute('aria-pressed',String(kind===value));filters.append(node);}panel.append(filters);box.append(panel);
   const label=el('label'),check=el('input');check.type='checkbox';check.checked=conflicts;check.onchange=()=>{conflicts=check.checked;filterOpen=panel.open;render();};label.append(check,el('span','Include date / vehicle / stay-limit conflicts'));panel.append(label);
   for(const slot of ['a','b']){const place=places.find(p=>p.id===plan[slot]);if(place){box.append(el('h2',slot==='a'?'PLAN A':'BACKUP'),result(place),button('Remove',()=>{plan[slot]=null;persist();render();}));}}
   const shown=places.filter(p=>(kind==='all'||p.kind===kind)&&(conflicts||p.status!=='excluded')).sort((a,b)=>(a.status==='excluded')-(b.status==='excluded')||miles(a)-miles(b));
   for(const place of shown)box.append(result(place));if(!shown.length&&!failed)paragraph(box,'No places match. Try another stay type or include conflicts.');
   paragraph(box,'Availability is not checked. Satellite imagery does not show current snow or road conditions. List filters affect the list only; map layers have their own switches.');
   if(adventure.node.open)showAdventure(lastAdventure);
  }
  function showAdventure(activity){
   lastAdventure=activity;
   const box=adventure.body;box.replaceChildren();const options=T.adventureOptions(places,trails(),activity);
   paragraph(box,T.activities[activity]+' + camping · '+trip.arrive+' to '+trip.depart+' · '+options.length+' straight-line pairings in this pilot');
   paragraph(box,'Research suggestions, not verified itineraries. Camping date and vehicle conflicts are shown. Trail use dates, closures and connecting access still need review. Distances are straight-line to mapped segments, not trailheads.');
   for(const {place,trails:nearby} of options){box.append(el('h2',place.name));paragraph(box,place.label);paragraph(box,place.tripNote);paragraph(box,'Ordered by camping conflicts, then straight-line distance to the nearest matching trail segment.');
    for(const {feature,miles} of nearby){paragraph(box,(feature.properties.name||'Unnamed trail')+' · about '+miles.toFixed(1)+' mi straight-line');const r=feature.properties.activities[activity];paragraph(box,[r.managed?'Managed: '+r.managed:'',r.accpt?'Accepted: '+r.accpt:'',r.restricted?'Restricted: '+r.restricted:'',r.disc?'Discouraged: '+r.disc:''].filter(Boolean).join(' · '));}
    box.append(button('View camping & nearby trails',()=>{adventure.node.close();showPlace(place);}));}
   if(!options.length)paragraph(box,region.layers.get(trailEntry()?.id)?.state==='loaded'?'No camping listing within five straight-line miles of a matching trail segment in this small pilot. Try a different activity or explore the map. This does not mean the activity is unavailable in the area.':'Trail data could not load. You can still explore the camping listings on the map.');if(!adventure.node.open)adventure.show();
  }
  function detail(entry,feature,box,actions=box){
   if(entry.kind==='trails'){
    box.append(el('h3','Camping nearby by straight-line distance'));paragraph(box,'Within about 5 miles of this mapped segment, in a straight line. These are not trailhead distances or connecting routes. Access and camping permission need checking.');
    const nearby=T.nearby(feature,inventory(region).map(x=>x.place));for(const {place,miles} of nearby)box.append(button(place.name+' · About '+miles.toFixed(1)+' mi straight-line · View camping details',()=>showPlace(place)));
    if(!nearby.length)paragraph(box,'No camping listings in our current inventory within this distance.');
   }
   if(entry.kind==='destinations'){trip.resort=feature.id;persist();render();return;}
   if(entry.format==='place_list'&&entry.kind==='overnight_inventory'){
    const p=places.find(p=>p.id===feature.id);if(!p)return;
    box.append(link(sourceLinkLabel(p),p.source));
    paragraph(actions,p.label);for(const text of [p.tripNote,p.note])paragraph(box,text);box.append(el('h3','Before you commit'));for(const text of p.unknowns||[])paragraph(box,text);
    for(const slot of ['a','b']){const node=button(slot==='a'?(plan.a===p.id?'Saved as Plan A':'Save as Plan A'):(plan.b===p.id?'Saved as backup':'Save as backup'),()=>{const other=slot==='a'?'b':'a';plan[slot]=plan[slot]===p.id?null:p.id;if(plan[other]===p.id)plan[other]=null;persist();render();showPlace(p);});node.dataset.save=slot;node.setAttribute('aria-pressed',String(plan[slot]===p.id));actions.append(node);}
    paragraph(actions,'Saving a place does not confirm it is suitable or available.');box.append(link('Open directions ↗','https://www.google.com/maps/dir/?api=1&destination='+encodeURIComponent(p.coordinates[1]+','+p.coordinates[0])));
    paragraph(box,'Listing reviewed '+p.checked_on+'. '+p.locationBasis+'.');box.append(link('Location source ↗',p.mapSource));
    if(p.access)box.append(link('USFS vehicle designation ↗',p.access.evidence.source_url));
    paragraph(box,'Distances are straight-line, not driving distances. Directions may not reflect closures or permission to use the approach.');
    if(p.ruleReview)paragraph(box,p.ruleReview);box.append(el('h3','Trails nearby by straight-line distance'));paragraph(box,'Approximate straight-line distance to mapped trail segments, not trailheads or routes. Check published uses and access.');
    const nearby=T.nearbyTrails(p,trails());for(const {feature,miles} of nearby)box.append(button((feature.properties.name||'Unnamed trail')+' · About '+miles.toFixed(1)+' mi straight-line · View trail',()=>shell.showDetail(trailEntry(),feature)));
    if(!nearby.length)paragraph(box,region.layers.get(trailEntry()?.id)?.state==='loaded'?'No mapped trails within five straight-line miles in this pilot.':'Trail data is not loaded.');
   }
  }
  return {render,detail,pins(entry){return entry.kind==='overnight_inventory'?inventory(region).filter(x=>x.entry.id===entry.id).map(x=>x.place):region.places[entry.id];},get trip(){return trip;},get plan(){return plan;}};
 }
 const api={inventory,evaluate,sourceSummary,sourceLinkLabel,attach};if(typeof module!=='undefined')module.exports=api;scope.ExploreCapabilities=api;
})(typeof globalThis!=='undefined'?globalThis:this);
