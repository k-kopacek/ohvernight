(function(scope){
  'use strict';
  let map,baseLayer,view,controlBindings=[];
  const layers=new Map(),handlers=new Map(),styles=new Map(),labelRules=new Map(),labelled=new Set();
  const LABEL_LIMIT=32;
  let selected=null;
  const reduced=()=>scope.matchMedia?.('(prefers-reduced-motion:reduce)').matches===true;
  function publishView(){
    if(!map)return;
    const center=map.getCenter(),bounds=map.getBounds();
    refreshLabels();view.onViewChange?.({zoom:map.getZoom(),center:[center.lng,center.lat],
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
  function marker(latlng,pin){
    const L=scope.L,icon=document.createElement('span');icon.className='pin-badge';icon.textContent=pin.symbol||pin.number||'•';
    return L.marker(latlng,{title:pin.name,alt:pin.name,keyboard:true,pane:'markerPane',
      icon:L.divIcon({className:'explore-pin',html:icon,iconSize:[44,44],iconAnchor:[22,22]})});
  }
  function addLayer(id,featureCollection,style){
    removeLayer(id);if(!map)return;
    const L=scope.L;
    const pane=featureCollection.features.some(feature=>/LineString$/.test(feature.geometry?.type))?'overlayPane':'context';
    const layer=L.geoJSON(featureCollection,{pane,style,
      pointToLayer:(feature,latlng)=>marker(latlng,feature.properties),
      onEachFeature:(feature,item)=>item.on('click',event=>notify(id,feature,[event.latlng.lng,event.latlng.lat]))});
    layers.set(id,layer);styles.set(id,style);layer.addTo(map);
  }
  function removeLayer(id){const layer=layers.get(id);if(layer&&map)map.removeLayer(layer);layers.delete(id);styles.delete(id);labelRules.delete(id);refreshLabels();if(selected?.id===id)selected=null;}
  function setVisible(id,visible){const layer=layers.get(id);if(!map||!layer)return;if(visible)layer.addTo(map);else map.removeLayer(layer);refreshLabels();}
  function applySelection(id){
    const layer=layers.get(id),style=styles.get(id);if(!layer)return;
    layer.eachLayer(item=>{
      const feature=item.feature,featureId=feature?.properties?.id||item.featureId;
      const chosen=selected?.id===id&&selected.featureId===featureId;
      const icon=item.getElement?.();if(icon){icon.dataset.featureId=String(featureId);icon.classList.toggle('is-selected',chosen);icon.setAttribute('aria-pressed',String(chosen));}
      if(feature&&style&&item.setStyle){
        const base=typeof style==='function'?style(feature):style;
        const polygon=/Polygon$/.test(feature.geometry?.type);
        // Polygon selection changes relative emphasis, preserving its palette,
        // precision treatment and all tier opacity/outline ceilings.
        const emphasis=selected?.id===id?(polygon?{fillOpacity:chosen?base.fillOpacity:Math.min(base.fillOpacity||0,.04)}:chosen?{weight:(base.weight||1)+2,opacity:1}:{}):{};
        item.setStyle({...base,...emphasis});item.options.selected=!!chosen;
      }
    });
  }
  function setSelected(id,featureId){
    const previous=selected?.id;selected=featureId===null?null:{id,featureId};
    if(previous)applySelection(previous);if(selected)applySelection(id);
  }
  function setStyle(id,style){styles.set(id,style);layers.get(id)?.setStyle(style);if(selected?.id===id)applySelection(id);}
  function setPins(id,pins){
    removeLayer(id);if(!map)return;
    const L=scope.L,group=L.layerGroup();
    for(const pin of pins){
      const item=marker([pin.coordinates[1],pin.coordinates[0]],pin);item.featureId=pin.id;item.labelProperties=pin;
      item.on('click',()=>notify(id,pin,pin.coordinates.slice()));item.addTo(group);
    }
    layers.set(id,group);group.addTo(map);
  }
  function refreshLabels(){
    for(const item of labelled)item.unbindTooltip();labelled.clear();if(!map)return;
    const occupied=[],bounds=map.getBounds();let count=0;
    for(const [id,rule] of labelRules){
      const layer=layers.get(id);if(!layer||!map.hasLayer(layer)||map.getZoom()<rule.minZoom)continue;
      let shown=0;layer.eachLayer(item=>{
        if(shown>=rule.max||count>=LABEL_LIMIT)return;
        const properties=item.feature?.properties||item.labelProperties,name=properties?.[rule.property];
        if(typeof name!=='string'||!name.trim())return;
        const position=item.getLatLng?.()||item.getCenter?.();if(!position||!bounds.contains(position))return;
        const point=map.latLngToContainerPoint(position);if(point.y<120)return;
        const box={left:point.x-90,right:point.x+90,top:point.y-12,bottom:point.y+12};
        if(occupied.some(other=>box.left<other.right+8&&box.right+8>other.left&&box.top<other.bottom+8&&box.bottom+8>other.top))return;
        const text=document.createElement('span');text.textContent=name;
        item.bindTooltip(text,{permanent:true,interactive:false,direction:'center',className:'explore-map-label'}).openTooltip();
        occupied.push(box);labelled.add(item);shown++;count++;
      });
    }
  }
  function setLabels(id,rule){
    if(rule)labelRules.set(id,{property:rule.property,minZoom:rule.minZoom,max:Math.max(0,Math.min(LABEL_LIMIT,Math.floor(rule.max)))});
    else labelRules.delete(id);refreshLabels();
  }
  function onFeature(id,handler){handlers.set(id,handler);}
  function fit(bounds,padding=[24,24]){
    if(!map||!bounds)return;
    const inset=Array.isArray(padding)?{padding}:{paddingTopLeft:padding.topLeft,paddingBottomRight:padding.bottomRight};
    map.invalidateSize();map.fitBounds(bounds.map(point=>[point[1],point[0]]),{...inset,maxZoom:15,animate:!reduced()});publishView();
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
    map=null;baseLayer=null;layers.clear();handlers.clear();styles.clear();labelRules.clear();labelled.clear();selected=null;
  }
  const api={init,addLayer,removeLayer,setVisible,setStyle,setPins,onFeature,fit,setBasemap,destroy,setSelected,setLabels};
  if(typeof module!=='undefined')module.exports=api;
  scope.ExploreMap=api;
})(typeof globalThis!=='undefined'?globalThis:this);
