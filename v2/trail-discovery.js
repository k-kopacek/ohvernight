(function(scope){
 'use strict';
 const activities={hiking:'Hiking',horseback_riding:'Horseback riding',mountain_biking:'Mountain biking',motorcycling:'Motorcycling',atv:'ATV',four_wheel_drive:'4WD',snowshoeing:'Snowshoeing',cross_country_skiing:'Cross-country skiing',snowmobiling:'Snowmobiling'};
 function matches(feature,query,activity){
   const p=feature.properties||{},r=p.activities?.[activity]||{};
   return `${p.name||''} ${p.trail_number||''}`.toLowerCase().includes(query.trim().toLowerCase())&&
     (!activity||Boolean(r.managed||r.accpt));
 }
 // Local equirectangular projection: approximate proximity, never route distance.
 function distanceMiles(coordinates,geometry){
   const lines=geometry?.type==='LineString'?[geometry.coordinates]:geometry?.type==='MultiLineString'?geometry.coordinates:[];
   const [lon,lat]=coordinates,scale=Math.cos(lat*Math.PI/180),km=111.195;
   const project=p=>[(p[0]-lon)*scale*km,(p[1]-lat)*km];
   let best=Infinity;
   for(const line of lines)for(let i=1;i<line.length;i++){
     const a=project(line[i-1]),b=project(line[i]),dx=b[0]-a[0],dy=b[1]-a[1],den=dx*dx+dy*dy;
     const t=den?Math.max(0,Math.min(1,-(a[0]*dx+a[1]*dy)/den)):0;
     best=Math.min(best,Math.hypot(a[0]+t*dx,a[1]+t*dy));
   }
   return best/1.609344;
 }
 function nearby(feature,places){
   return places.filter(p=>['campground','dispersed'].includes(p.kind))
     .map(place=>({place,miles:distanceMiles(place.coordinates,feature.geometry)}))
     .filter(p=>p.miles<=5).sort((a,b)=>a.miles-b.miles).slice(0,3);
 }
 function nearbyTrails(place,features){
   const seen=new Set();
   return features.map(feature=>({feature,miles:distanceMiles(place.coordinates,feature.geometry)}))
     .filter(x=>x.miles<=5).sort((a,b)=>a.miles-b.miles)
     .filter(({feature})=>{const p=feature.properties,key=(p.trail_number||p.id)+'|'+(p.name||'');if(seen.has(key))return false;seen.add(key);return true;}).slice(0,3);
 }
 function adventureOptions(places,features,activity){
   if(!Object.hasOwn(activities,activity))return [];
   const candidates=features.filter(f=>matches(f,'',activity));
   return places.filter(p=>['campground','dispersed'].includes(p.kind))
     .map(place=>({place,trails:nearbyTrails(place,candidates)})).filter(x=>x.trails.length)
     .sort((a,b)=>(a.place.status==='excluded')-(b.place.status==='excluded')||a.trails[0].miles-b.trails[0].miles);
 }
 const api={activities,matches,distanceMiles,nearby,nearbyTrails,adventureOptions};
 if(typeof module!=='undefined')module.exports=api;
 scope.TrailDiscovery=api;
})(typeof globalThis!=='undefined'?globalThis:this);
