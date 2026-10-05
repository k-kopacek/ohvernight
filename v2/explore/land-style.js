(function(scope){
  'use strict';
  const E=typeof require==='function'?require('./evidence.js'):scope.ExploreEvidence;
  const wording={
    W1:'Generalized land management context — not parcels',
    W2:'Broad areas drawn at limited scale from a national agency dataset. They show which agency the source lists as managing an area. They are not property lines and do not show who owns a specific spot.',
    W3:'Ownership or management does not establish public access. This map does not show whether you may enter, cross, park or stay.',
    W4:"PVT — the source's generalized private class; not a parcel-level finding",
    W5:'Unshaded land is unknown — not private, not public, not open',
    W6:'<code> — unrecognised source code; unknown',
    W7:'Limited-scale boundary. It cannot locate a property line or tell you whether a specific spot is inside this area.',
    W8:{USFS:'USFS — Forest Service; generalized source class',BLM:'BLM — Bureau of Land Management; generalized source class',
      OTHFE:'OTHFE — Other Federal; generalized source class',ST:'ST — State; generalized source class',LG:'LG — Local; generalized source class'},
    W9:'<layer title> — boundary as published by <agency>',
    W10:'Computer-screened research areas — not campsites',
    W11:'Source classification: <code>'
  };
  const palette=['#8f9f89','#8d9da7','#a59e88','#a49ba9','#91a6a0','#9ea3a6'];
  const codes=['USFS','BLM','OTHFE','ST','LG','PVT'];
  function color(code){const index=codes.indexOf(code);return index<0?'#b8b9b6':palette[index];}
  const precision=layer=>layer.spatial_precision||layer.spatialPrecision;
  const field=layer=>layer.classification_source_field||layer.classificationSourceField;
  function tier(layer){
    if(['land_management','wilderness'].includes(layer.kind)&&precision(layer)==='generalized')return 'G';
    if(precision(layer)==='computed')return 'C';
    if(precision(layer)==='source_published'&&(layer.geometry_types||layer.geometryTypes||[]).some(type=>/Polygon$/.test(type)))return 'P';
    return 'Unknown';
  }
  function label(code){return code==='PVT'?wording.W4:wording.W8[code]||wording.W6.replace('<code>',String(code));}
  function style(layer,zoom,feature){
    const level=tier(layer),code=feature?.properties?.[field(layer)],tint=color(code);
    if(level==='G')return {color:tint,fillColor:tint,fillOpacity:.12,weight:zoom>=14?0:1,opacity:zoom>=14?0:.5,stroke:zoom<14,dashArray:'5 5'};
    if(level==='C')return {color:palette[3],fillColor:palette[3],fillOpacity:.10,weight:1,opacity:.5,dashArray:'7 5'};
    if(level==='P')return {color:tint,fillColor:tint,fillOpacity:.12,weight:1.3,opacity:.6,dashArray:null};
    return {color:layer.kind==='water'?'#73c5dc':layer.kind==='trails'?'#b4a4ad':'#b1a58a',weight:layer.kind==='water'?1.5:3,opacity:.85,fillOpacity:.10};
  }
  function legend(layer,features=[],title='',agency=''){
    const level=tier(layer),entries=[];
    if(level==='G'){
      entries.push({text:wording.W1},{text:wording.W2},{text:wording.W3});
      for(const code of new Set(features.map(feature=>feature.properties?.[field(layer)]).filter(code=>typeof code==='string')))
        entries.push({text:label(code),color:color(code)});
    }else if(level==='P')entries.push({text:wording.W9.replace('<layer title>',title).replace('<agency>',agency)});
    else if(level==='C')entries.push({text:wording.W10});
    if(layer.kind==='land_management'||level==='G')entries.push({text:wording.W5});
    return entries;
  }
  function detail(manifest,layer,feature){
    const properties=feature.properties||{},evidence=properties.evidence||{},code=String(properties[field(layer)]??'');
    const items=[{text:wording.W11.replace('<code>',code)},{text:label(code)}];
    if(evidence.agency)items.push({text:evidence.agency});
    const url=E.safeUrl(evidence.source_url);if(url)items.push({text:'View source ↗',url});
    if(evidence.retrieved_at)items.push({text:'Source fetched '+evidence.retrieved_at.slice(0,10)});
    items.push({text:wording.W7},{text:wording.W3},{text:manifest.fact_coverage.ownership.statement},{text:manifest.fact_coverage.public_access.statement},{text:layer.limitations});
    return {title:label(code),items};
  }
  const api={wording,palette,color,tier,label,style,legend,detail};
  if(typeof module!=='undefined')module.exports=api;scope.ExploreLand=api;
})(typeof globalThis!=='undefined'?globalThis:this);
