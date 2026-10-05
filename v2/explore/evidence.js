(function(scope){
  'use strict';
  const transport=typeof require==='function'?require('./transport.js'):scope.ExploreTransport;
  const trust=typeof require==='function'?require('../trust.js'):scope.Trust;
  function safeUrl(value){
    try{const url=new URL(value);return ['http:','https:'].includes(url.protocol)?url.href:null;}catch{return null;}
  }
  const date=value=>typeof value==='string'?value.slice(0,10):'';
  function retrievalLine(record,maxAgeHours,now){
    if(!record?.last_retrieved_at)return '';
    let text='Fetched '+date(record.last_retrieved_at);
    if(maxAgeHours!==null&&trust.freshness({last_confirmed_at:record.last_retrieved_at,max_age_hours:maxAgeHours},Number.isFinite(now)?now:NaN)==='stale')
      text+=' · older than the refresh policy; refresh needed';
    return text;
  }
  function layer(manifest,declaration,index,count,now){
    const raw=index?.transport?.[declaration.id];
    const record=raw?transport.normalizeTransport(raw).record:null;
    const lines=[declaration.limitations];
    if(!record)lines.push('No retrieval status is recorded for this layer');
    else{
      if(record.status!=='available')lines.push(count?'latest fetch failed':'Source unavailable');
      if(record.last_checked_at&&(record.last_checked_at!==record.last_retrieved_at||record.status!=='available'))
        lines.push('Last retrieval attempt '+date(record.last_checked_at));
      const fetched=retrievalLine(record,declaration.max_age_hours,now);if(fetched)lines.push(fetched);
      if(record.reason)lines.push(record.reason);
    }
    const links=declaration.source_ids.flatMap(id=>{
      const source=manifest.sources[id];
      return source.source_urls.map(url=>({label:source.agency,url:safeUrl(url)})).filter(item=>item.url);
    });
    return {lines,links,count};
  }
  function region(manifest){
    const facts=Object.values(manifest.fact_coverage||{});
    return {lines:[manifest.coverage?.statement,...facts.map(fact=>fact.statement),...(manifest.known_gaps||[])].filter(value=>typeof value==='string'),
      links:facts.flatMap(fact=>(fact.official_urls||[]).map(url=>({label:'View source ↗',url:safeUrl(url)}))).filter(item=>item.url)};
  }
  function feature(manifest,declaration,record,title){
    const properties=record.properties||record;
    const provenance=properties.evidence||{};
    const lines=[];
    if(provenance.agency)lines.push(provenance.agency);
    if(provenance.retrieved_at)lines.push('Source fetched '+date(provenance.retrieved_at));
    lines.push(declaration.limitations);
    if(declaration.kind==='trails'){
      lines.push('Trail '+(properties.trail_number||'number unavailable')+' · '+(properties.surface||'Surface unknown'),
        'Only the portion inside our research boundary is shown. Check current agency notices before travel.',
        'Published activity dates','These are source records, not a check for your trip dates. Blank records mean unknown.');
      const discovery=typeof require==='function'?require('../trail-discovery.js'):scope.TrailDiscovery;
      for(const [key,label] of Object.entries(discovery.activities)){
        const rules=properties.activities?.[key]||{};
        const parts=Object.entries({managed:'Managed use',accpt:'Accepted use',disc:'Discouraged',restricted:'Restricted'}).filter(([field])=>rules[field]).map(([field,text])=>text+': '+rules[field]);
        lines.push(label,parts.join(' · ')||'Unknown — no published use record');
      }
    }
    if(declaration.kind==='roads'){
      lines.push('Current road conditions and vehicle suitability are unconfirmed.');
      if(properties.operational_maintenance_level)lines.push('Agency maintenance classification: '+properties.operational_maintenance_level);
      if(properties.designations){lines.push('Published vehicle seasons');for(const [vehicle,r] of Object.entries(properties.designations))
        lines.push(({passenger_car:'Passenger car / SUV',high_clearance:'High-clearance vehicle',motorhome:'Motorhome / RV'})[vehicle]+': '+(r.dates_open||'Dates not provided')+' · '+r.designation);}
    }
    if(declaration.kind==='research_areas'&&properties.evaluated_trip){const trip=properties.evaluated_trip;
      lines.push('No campsite or camping permission has been confirmed. Screening snapshot: '+trip.arrive+'–'+trip.depart+' ('+trip.vehicle.replaceAll('_',' ')+'). This is not an assessment of your selected trip.');}
    return {title:properties.name||title,lines,links:[{label:'View source ↗',url:safeUrl(provenance.source_url)}].filter(item=>item.url)};
  }
  const api={safeUrl,retrievalLine,layer,region,feature};
  if(typeof module!=='undefined')module.exports=api;
  scope.ExploreEvidence=api;
})(typeof globalThis!=='undefined'?globalThis:this);
