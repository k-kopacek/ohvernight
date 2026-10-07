(function(scope){
  'use strict';
  function displayWater(feature){
    const p=feature.properties||{};
    return typeof p.name==='string'&&p.name.trim().length>0&&
      (((p.kind==='flowline'||p.source_layer==='flowline')&&['LineString','MultiLineString'].includes(feature.geometry?.type))||
       ((p.kind==='waterbody'||p.source_layer==='waterbody')&&['Polygon','MultiPolygon'].includes(feature.geometry?.type)));
  }
  const api={displayWater};
  if(typeof module!=='undefined')module.exports=api;
  scope.MapLayers=api;
})(typeof globalThis!=='undefined'?globalThis:this);
