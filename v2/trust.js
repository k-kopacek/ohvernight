(function(scope){
  'use strict';
  function freshness(record, now=Date.now()){
    const timestamp=Date.parse(record?.last_confirmed_at||'');
    const hours=record?.max_age_hours;
    if(!Number.isFinite(timestamp)||!Number.isFinite(hours)||hours<=0||timestamp>now)return 'unavailable';
    return now-timestamp>hours*3600000?'stale':'current';
  }
  function sameTrip(a,b){return !!a&&!!b&&['arrive','depart','vehicle'].every(k=>a[k]===b[k]);}
  function applyRules(place,registry,now=Date.now()){
    const matches=(registry?.rules||[]).filter(r=>r.place_ids?.includes(place.id));
    if(matches.length!==1)return {...place,ruleReview:matches.length?'Conflicting rule records need review':null};
    const rule=matches[0], current=freshness(rule,now)==='current';
    return {...place,
      ...(current?{stay_limit_days:rule.stay_limit_days,requires_high_clearance:rule.requires_high_clearance}:{}),
      ruleReview:current?null:'The published site rule needs a fresh source review.',
      ruleSource:rule.source_url};
  }
  function sourceSummary(bundle,ridb,now=Date.now()){
    const records=bundle?.layers?.fire_restriction_stage?.features||[];
    const fire=records.find(f=>f.properties?.id==='pitkin-fire-monitor')?.properties;
    const fireAge=freshness(fire,now);
    const interpreted=fire?.status==='confirmed' && fireAge==='current';
    return {
      fire:interpreted?'Fire notice reviewed; check its jurisdiction and effective dates.':
        fireAge==='stale'?'Fire restriction information is outdated. Verify with the agency before travel.':
        'Current fire restrictions have not been confirmed. Check official notices.',
      closures:'Wildlife closures and special orders are not fully verified for this trip.',
      inventory:!ridb?'RIDB inventory is not connected yet.':
        freshness(ridb.source_status,now)==='current'?'RIDB facility inventory fetched recently; availability is not checked.':
        'RIDB inventory may be outdated. Open the official listing to confirm.',
      fireState:interpreted?'current':fireAge==='stale'?'stale':'unavailable'
    };
  }
  const api={freshness,sameTrip,applyRules,sourceSummary};
  if(typeof module!=='undefined')module.exports=api;
  scope.Trust=api;
})(typeof globalThis!=='undefined'?globalThis:this);
