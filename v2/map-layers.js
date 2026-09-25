(function(scope){
  'use strict';
  const definitions=[
    {id:'places',title:'Overnight listings',description:'Campgrounds, dispersed areas and rooms. Tap a pin for details.',color:'#f8faef',kind:'pins'},
    {id:'resorts',title:'Mountains',description:'Aspen / Snowmass destinations.',color:'#263024',kind:'pins'},
    {id:'land',key:'land_ownership',feed:'01_fetch_land_ownership',title:'Land management',description:'Broad agency boundaries; not precise public/private parcels.',color:'#88a075'},
    {id:'wilderness',key:'wilderness',feed:'01_fetch_land_ownership',title:'Wilderness',description:'Protected wilderness boundaries. Check agency rules before planning access.',color:'#b5a0de'},
    {id:'water',key:'hydrology',feed:'03_fetch_hydrology',title:'Named water',description:'Named waterbodies and waterways. Seasonal flow, recreation access and activity suitability are not verified.',color:'#73c5dc'},
    {id:'roads',key:'mvum_roads',feed:'02_fetch_mvum_roads',title:'Forest vehicle roads',description:'Mapped routes. A line does not mean the road is open or suitable for your vehicle.',color:'#ead294',kind:'line'},
    {id:'candidates',key:'dispersed_corridors',feed:'07_build_dispersed_corridors',title:'Areas to research',description:'Computer-screened areas near roads. Campsites and camping permission are unconfirmed.',color:'#e9a965',kind:'dashed'},
    {id:'restrictions',keys:['wildlife_sensitivity','fire_restriction_stage'],title:'Restrictions',description:'Mapped notices only. Missing shading does not mean there are no restrictions.',color:'#d6604d'},
    {id:'leads',key:'leads',feed:'08_ingest_leads',title:'Community leads',description:'Unverified reports for further research.',color:'#dfa5c9'},
    {id:'reviewed',key:'reviewed_sites',feed:'09_reviewed_sites',title:'Reviewed sites',description:'Sites with individual review records. Read each record before relying on it.',color:'#86c9b2'},
    {id:'coverage',title:'Research boundary',description:'Current study area. Detailed coverage outside this outline has not been loaded.',color:'#ffffff',kind:'dashed'}
  ];
  function features(record){return (record?.type==='Feature'?[record]:record?.features||[]).filter(f=>f.geometry);}
  function displayWater(feature){
    const p=feature.properties||{};
    return typeof p.name==='string'&&p.name.trim().length>0&&
      ((p.kind==='flowline'&&['LineString','MultiLineString'].includes(feature.geometry?.type))||
       (p.kind==='waterbody'&&['Polygon','MultiPolygon'].includes(feature.geometry?.type)));
  }
  function describe(bundle,coverage,placeCount,resortCount){
    return definitions.map(d=>{
      const sourceRecords=d.id==='coverage'?features(coverage):(d.keys||[d.key]).flatMap(k=>features(bundle?.layers?.[k]));
      const records=d.id==='water'?sourceRecords.filter(displayWater):sourceRecords;
      const count=d.id==='places'?placeCount:d.id==='resorts'?resortCount:records.length;
      const source=bundle?.source_status?.[d.feed];
      const loaded=d.kind==='pins'||(d.id==='coverage'?!!coverage:!!bundle?.layers&&(d.keys||[d.key]).some(k=>bundle.layers[k]));
      let status=count?count.toLocaleString()+(d.kind==='pins'?' locations loaded':' map features loaded'):'No features in this dataset';
      if(!loaded)status='Data not loaded';
      else if(d.id==='water')status=`${count.toLocaleString()} named features shown · ${sourceRecords.length.toLocaleString()} retained for screening`;
      if(loaded&&source&&source.status!=='available')status=count?status+' · latest fetch failed':'Source unavailable';
      if(d.id==='restrictions'&&!count)status='No mapped restrictions · coverage incomplete';
      const fetched=source?.completed_at||records[0]?.properties?.evidence?.retrieved_at;
      return {...d,records,count,sourceCount:sourceRecords.length,status,fetched};
    });
  }
  const api={definitions,describe,displayWater};
  if(typeof module!=='undefined')module.exports=api;
  scope.MapLayers=api;
})(typeof globalThis!=='undefined'?globalThis:this);
