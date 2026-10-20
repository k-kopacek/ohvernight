(function(scope){
 'use strict';
 const area={type:'Feature',geometry:null,properties:{id:'rampart-designated-area',name:'Rampart Range designated dispersed camping',site_type:'DISPERSED_AREA',rec1stop_url:'https://www.recreation.gov/camping/campgrounds/10132201',restrictions:'Numbered designated sites only; fee required. The official listing describes a December 1–April 1 camping closure, with weather-dependent reopening. Check the listing for current rules and availability.',evidence:{retrieved_at:'2026-09-27',source_url:'https://www.recreation.gov/camping/campgrounds/10132201'}}};
 const coverage={text:"County/state trails, complete cross-county routes, precise parcels, live availability, verified difficulty and turn-by-turn navigation are not included. Named water does not confirm recreation access or perennial flow. GPX exports contain clipped source segments, not verified routes. Facility “open” fields may be old and are not treated as current status."};
 const api={area,coverage};if(typeof module!=='undefined')module.exports=api;scope.RegionExtras=api;
})(typeof globalThis!=='undefined'?globalThis:this);
