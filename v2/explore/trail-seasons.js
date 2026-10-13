(function(scope){
 const activities={motorcycling:'Dirt biking',atv:'ATV',mountain_biking:'Mountain biking',hiking:'Hiking',horseback_riding:'Horseback riding',four_wheel_drive:'4WD',snowshoeing:'Snowshoeing',cross_country_skiing:'Cross-country skiing',snowmobiling:'Snowmobiling'};
 function windows(text){
  if(!text)return null;
  const parts=String(text).split(/[;,]/),result=[];
  for(const p of parts){const m=p.trim().match(/^(\d{1,2})\/(\d{1,2})\s*[-–]\s*(\d{1,2})\/(\d{1,2})$/);if(!m)return null;const n=m.slice(1).map(Number);
   for(const [month,day] of [[n[0],n[1]],[n[2],n[3]]]){const d=new Date(Date.UTC(2000,month-1,day));if(d.getUTCMonth()!==month-1||d.getUTCDate()!==day)return null;}
   result.push([n[0]*100+n[1],n[2]*100+n[3]]);
  }return result;
 }
 const covers=(ranges,day)=>ranges.some(([a,b])=>a<=b?day>=a&&day<=b:day>=a||day<=b);
 function days(start,end){
  const parse=s=>{if(!/^\d{4}-\d{2}-\d{2}$/.test(s))return NaN;const t=Date.parse(s+'T00:00:00Z');return Number.isFinite(t)&&new Date(t).toISOString().slice(0,10)===s?t:NaN;};
  const a=parse(start),b=parse(end);if(!Number.isFinite(a+b)||b<a||b-a>366*86400000)return null;
  const result=[];for(let t=a;t<=b;t+=86400000){const d=new Date(t);result.push((d.getUTCMonth()+1)*100+d.getUTCDate());}return result;
 }
 const NOT_INTERPRETED='Source dates not interpreted — see details';
 function season(feature,activity,start,end){
  const dates=days(start,end),r=feature.properties.activities?.[activity]||{};if(!dates)return 'Choose valid trip dates';
  const restricted=windows(r.restricted);if(restricted&&dates.some(d=>covers(restricted,d)))return 'Published restriction overlaps trip';
  if(r.restricted&&!restricted)return 'Restriction needs review';
  const values=[r.managed,r.accpt].filter(Boolean);if(!values.length)return 'Use permission unknown';
  // The publisher does not define managed or accepted dates as a season of use, and dates it does not
  // list are unknown, so no trip verdict is derived from them. Only restricted dates are compared.
  return r.disc?'Published use discouraged — review':NOT_INTERPRETED;
 }
 function camping(features){return features.filter(f=>f.properties.site_type==='CAMPGROUND');}
 function gpx(feature){
  const escape=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&apos;'}[c]));
  const lines=feature.geometry.type==='LineString'?[feature.geometry.coordinates]:feature.geometry.type==='MultiLineString'?feature.geometry.coordinates:[];
  return '<?xml version="1.0" encoding="UTF-8"?><gpx version="1.1" creator="ohvernight" xmlns="http://www.topografix.com/GPX/1/1"><trk><name>'+escape(feature.properties.name||'Trail segment')+'</name><desc>County-clipped source geometry, not a navigable route or access approval.</desc>'+lines.map(line=>'<trkseg>'+line.map(p=>'<trkpt lat="'+Number(p[1])+'" lon="'+Number(p[0])+'"/>').join('')+'</trkseg>').join('')+'</trk></gpx>';
 }
 const api={activities,windows,days,season,camping,gpx,NOT_INTERPRETED};if(typeof module!=='undefined')module.exports=api;scope.ExploreSeasons=api;
})(typeof globalThis!=='undefined'?globalThis:this);
