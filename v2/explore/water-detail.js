(function(scope){
  'use strict';
  const E=typeof require==='function'?require('./evidence.js'):scope.ExploreEvidence;
  const wording=Object.freeze({
    WW1:'Mapped water. Access and allowed activities are not established.',
    WW2:'A mapped water feature is not permission to enter, fish, boat, paddle, swim, park or camp.',
    WW9:'From the source',WW10:'Computed by Ohvernight',WW12:'Perennial',WW13:'source segments',
    WW14:'Unnamed lake',WW15:'Unnamed reservoir',WW16:'Hydrographic category not stated by the source',
    river:'River or stream',lake:'Lake or pond',reservoir:'Reservoir'
  });
  function title(properties){
    if(typeof properties.name==='string'&&properties.name.trim())return properties.name;
    if(properties.water_class==='lake_pond')return wording.WW14;
    if(properties.water_class==='reservoir')return wording.WW15;
    return '';
  }
  function feature(manifest,declaration,record){
    const properties=record.properties||record,evidence=properties.evidence||{},shared=E.feature(
      manifest,declaration,record,declaration.title||'',NaN);
    const items=[{heading:true,text:wording.WW9}];
    const typeLabel={stream:wording.river,lake_pond:wording.lake,reservoir:wording.reservoir}[properties.water_class];
    if(typeLabel)items.push({text:typeLabel});
    if(properties.hydro_category==='perennial')items.push({text:wording.WW12});
    else if(properties.hydro_category==='unknown')items.push({text:wording.WW16});
    if(properties.water_class==='stream'&&Number.isInteger(properties.member_count))
      items.push({text:properties.member_count+' '+wording.WW13});
    if(evidence.agency)items.push({text:evidence.agency});
    const sourceLink=shared.links.find(item=>item.url);
    if(sourceLink)items.push({text:sourceLink.label,url:sourceLink.url});
    const fetched=shared.lines.find(line=>line.startsWith('Source fetched '));
    if(fetched)items.push({text:fetched});
    const limitation=shared.lines.find(line=>line===declaration.limitations);
    if(limitation)items.push({text:limitation});
    const length=properties.water_class==='stream'&&Number.isFinite(properties.length_km)?properties.length_km:null;
    const area=properties.water_class!=='stream'&&Number.isFinite(properties.area_sqkm)?properties.area_sqkm*100:null;
    if(length!==null){items.push({heading:true,text:wording.WW10},{text:length.toFixed(1)+' km'});}
    else if(area!==null){items.push({heading:true,text:wording.WW10},{text:area.toFixed(1)+' ha'});}
    items.push({text:wording.WW1},{text:wording.WW2});
    return {title:title(properties)||shared.title,items};
  }
  function searchRows(region,query=''){
    const text=String(query).trim().toLowerCase(),rows=[];
    for(const entry of region.registry.filter(item=>item.kind==='water')){
      const features=region.layers.get(entry.id)?.data?.features||[];
      for(const feature of features){
        const name=feature.properties?.name;
        if(typeof name==='string'&&name.trim()&&name.toLowerCase().includes(text))
          rows.push({entry,feature,title:name});
      }
    }
    return rows;
  }
  const api={wording,title,feature,searchRows};
  if(typeof module!=='undefined')module.exports=api;
  scope.ExploreWaterDetail=api;
})(typeof globalThis!=='undefined'?globalThis:this);
