(function(scope){
  'use strict';
  let map,baseLayer,view,controlBindings=[];
  const layers=new Map(),handlers=new Map();
  const reduced=()=>scope.matchMedia?.('(prefers-reduced-motion:reduce)').matches===true;
  function publishView(){
    if(!map)return;
    const center=map.getCenter(),bounds=map.getBounds();
    view.onViewChange?.({zoom:map.getZoom(),center:[center.lng,center.lat],
      bounds:[[bounds.getWest(),bounds.getSouth()],[bounds.getEast(),bounds.getNorth()]]});
  }
  function init(container,initialView){
    destroy();view=initialView;
    if(!scope.L)return false;
    const L=scope.L;
    map=L.map(container,{zoomControl:false,preferCanvas:true,minZoom:5,maxZoom:19,
      zoomAnimation:!reduced(),fadeAnimation:!reduced(),markerZoomAnimation:!reduced()});
    map.createPane('context');map.getPane('context').style.zIndex=350;
    map.on('moveend zoomend',publishView);
    map.setView([view.center[1],view.center[0]],view.zoom,{animate:false});
    for(const [name,delta] of [['zoomIn',1],['zoomOut',-1]]){
      const control=view.controls?.[name];if(!control)continue;
      const handler=()=>map?.setZoom(map.getZoom()+delta,{animate:!reduced()});
      control.addEventListener('click',handler);controlBindings.push([control,handler]);
    }
    L.control.scale({position:'bottomleft',imperial:true,metric:false}).addTo(map);
    setBasemap('satellite');publishView();return true;
  }
  function notify(id,feature,coordinates){handlers.get(id)?.(feature,coordinates);}
  function addLayer(id,featureCollection,style){
    removeLayer(id);if(!map)return;
    const L=scope.L;
    const pane=featureCollection.features.some(feature=>/LineString$/.test(feature.geometry?.type))?'overlayPane':'context';
    const layer=L.geoJSON(featureCollection,{pane,style,
      pointToLayer:(feature,latlng)=>L.circleMarker(latlng,{...(typeof style==='function'?style(feature):style),radius:7,pane:'markerPane'}),
      onEachFeature:(feature,item)=>item.on('click',event=>notify(id,feature,[event.latlng.lng,event.latlng.lat]))});
    layers.set(id,layer);layer.addTo(map);
  }
  function removeLayer(id){const layer=layers.get(id);if(layer&&map)map.removeLayer(layer);layers.delete(id);}
  function setVisible(id,visible){const layer=layers.get(id);if(!map||!layer)return;if(visible)layer.addTo(map);else map.removeLayer(layer);}
  function setStyle(id,style){layers.get(id)?.setStyle(style);}
  function setPins(id,pins){
    removeLayer(id);if(!map)return;
    const L=scope.L,group=L.layerGroup();
    for(const pin of pins){
      const icon=document.createElement('span');icon.className='pin-badge';icon.textContent=pin.symbol||'•';
      const marker=L.marker([pin.coordinates[1],pin.coordinates[0]],{title:pin.name,alt:pin.name,keyboard:true,
        icon:L.divIcon({className:'explore-pin',html:icon,iconSize:[44,44],iconAnchor:[22,22]})});
      marker.on('click',()=>notify(id,pin,pin.coordinates.slice()));marker.addTo(group);
    }
    layers.set(id,group);group.addTo(map);
  }
  function onFeature(id,handler){handlers.set(id,handler);}
  function fit(bounds,padding=[24,24]){
    if(!map||!bounds)return;
    map.invalidateSize();map.fitBounds(bounds.map(point=>[point[1],point[0]]),{padding,maxZoom:15,animate:!reduced()});publishView();
  }
  function setBasemap(mode){
    if(!map)return;if(baseLayer)map.removeLayer(baseLayer);
    const L=scope.L,service=mode==='satellite'?'USGSImageryOnly':'USGSTopo';
    baseLayer=L.tileLayer('https://basemap.nationalmap.gov/arcgis/rest/services/'+service+'/MapServer/tile/{z}/{y}/{x}',{
      maxNativeZoom:16,maxZoom:19,minZoom:5,keepBuffer:1,
      attribution:'Imagery / map: <a href="https://www.usgs.gov/programs/national-geospatial-program/national-map">USGS The National Map</a>'}).addTo(map);
  }
  function destroy(){
    for(const [control,handler] of controlBindings)control.removeEventListener('click',handler);
    controlBindings=[];if(map){map.off('moveend zoomend',publishView);map.remove();}
    map=null;baseLayer=null;layers.clear();handlers.clear();
  }
  const api={init,addLayer,removeLayer,setVisible,setStyle,setPins,onFeature,fit,setBasemap,destroy};
  if(typeof module!=='undefined')module.exports=api;
  scope.ExploreMap=api;
})(typeof globalThis!=='undefined'?globalThis:this);
