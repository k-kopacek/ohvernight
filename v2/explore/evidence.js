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
      links:facts.flatMap(fact=>(fact.official_urls||[]).map(url=>({label:'Open source ↗',url:safeUrl(url)}))).filter(item=>item.url)};
  }
  function feature(manifest,declaration,record,title){
    const properties=record.properties||record;
    const provenance=properties.evidence||{};
    const lines=[];
    if(provenance.agency)lines.push(provenance.agency);
    if(provenance.retrieved_at)lines.push('Source fetched '+date(provenance.retrieved_at));
    lines.push(declaration.limitations);
    return {title:properties.name||title,lines,links:[{label:'Open source ↗',url:safeUrl(provenance.source_url)}].filter(item=>item.url)};
  }
  const api={safeUrl,retrievalLine,layer,region,feature};
  if(typeof module!=='undefined')module.exports=api;
  scope.ExploreEvidence=api;
})(typeof globalThis!=='undefined'?globalThis:this);
