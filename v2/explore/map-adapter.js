(function(scope){
  'use strict';
  let map,baseLayer,view,controlBindings=[],mapBindings=[];
  const layers=new Map(),handlers=new Map(),styles=new Map(),labelRules=new Map(),labelled=new Set();
  const LABEL_LIMIT=32;
  const HIT_TOLERANCE=14;
  const TOUCH_TAP_WINDOW=280;
  let pendingTap,mouseTapZoom;
  let selected=null;
  const reduced=()=>scope.matchMedia?.('(prefers-reduced-motion:reduce)').matches===true;
  function segmentDistance(point,a,b){
    const dx=b.x-a.x,dy=b.y-a.y,den=dx*dx+dy*dy;
    const t=den?Math.max(0,Math.min(1,((point.x-a.x)*dx+(point.y-a.y)*dy)/den)):0;
    return Math.hypot(point.x-a.x-t*dx,point.y-a.y-t*dy);
  }
  function ringContains(point,ring){
    let inside=false;
    for(let i=0,j=ring.length-1;i<ring.length;j=i++){
      const a=ring[j],b=ring[i];if(segmentDistance(point,a,b)<1e-8)return true;
      if((a.y>point.y)!==(b.y>point.y)&&point.x<(b.x-a.x)*(point.y-a.y)/(b.y-a.y)+a.x)inside=!inside;
    }
    return inside;
  }
  // Pure geometry predicates. Projection and renderer objects stay here.
  function hitGeometry(point,geometry,project){
    if(!geometry)return null;
    const {type,coordinates:c}=geometry;
    if(type==='Point'||type==='MultiPoint'){
      const distance=Math.min(...(type==='Point'?[c]:c).map(p=>{const q=project(p);return Math.hypot(point.x-q.x,point.y-q.y);}));
      return distance<=HIT_TOLERANCE?{priority:0,distance}:null;
    }
    if(type==='LineString'||type==='MultiLineString'){
      let distance=Infinity;
      for(const line of type==='LineString'?[c]:c){let previous;for(const p of line){const q=project(p);if(previous)distance=Math.min(distance,segmentDistance(point,previous,q));previous=q;}}
      return distance<=HIT_TOLERANCE?{priority:1,distance}:null;
    }
    if(type==='Polygon'||type==='MultiPolygon'){
      for(const polygon of type==='Polygon'?[c]:c){const rings=polygon.map(r=>r.map(project));
        if(ringContains(point,rings[0])&&!rings.slice(1).some(r=>ringContains(point,r)))return {priority:2,distance:0};}
    }
    return null;
  }
  function chooseHit(candidates){
    return candidates.sort((a,b)=>a.priority-b.priority||a.distance-b.distance||
      (a.priority===2?a.area-b.area:0)||b.order-a.order||String(a.featureId).localeCompare(String(b.featureId)))[0]||null;
  }
  function resolveTap(point){
    const candidates=[],project=p=>map.latLngToContainerPoint([p[1],p[0]]);let order=0;
    const surface=map.getContainer?.()?.getBoundingClientRect();
    // Tooltips keep pointer-events:none. Only their actual visible boxes count
    // as a hit, routed to the same source feature as the geometry beneath.
    if(surface)for(const item of labelled){
      const id=item.labelLayerId,box=item.getTooltip?.()?.getElement?.()?.getBoundingClientRect();
      if(!box?.width||!handlers.has(id)||!map.hasLayer(layers.get(id)))continue;
      if(point.x>=box.left-surface.left&&point.x<=box.right-surface.left&&point.y>=box.top-surface.top&&point.y<=box.bottom-surface.top){
        const feature=item.feature||item.labelProperties;
        return {layerId:id,featureId:feature.properties?.id||feature.id,feature};
      }
    }
    for(const [id,group] of layers){order++;if(!handlers.has(id)||!map.hasLayer(group))continue;
      group.eachLayer(item=>{
        const feature=item.feature||item.labelProperties,geometry=feature?.geometry||(feature?.coordinates?{type:'Point',coordinates:feature.coordinates}:null);
        if(!geometry)return;
        const bound=item.getBounds?.(),position=item.getLatLng?.();
        let a,b;
        if(bound){a=map.latLngToContainerPoint(bound.getNorthWest());b=map.latLngToContainerPoint(bound.getSouthEast());}
        else if(position)a=b=map.latLngToContainerPoint(position);else return;
        const icon=item.getElement?.()?.getBoundingClientRect(),iconHit=surface&&icon&&point.x>=icon.left-surface.left&&point.x<=icon.right-surface.left&&point.y>=icon.top-surface.top&&point.y<=icon.bottom-surface.top;
        if(!iconHit&&(point.x<Math.min(a.x,b.x)-HIT_TOLERANCE||point.x>Math.max(a.x,b.x)+HIT_TOLERANCE||point.y<Math.min(a.y,b.y)-HIT_TOLERANCE||point.y>Math.max(a.y,b.y)+HIT_TOLERANCE))return;
        const hit=iconHit?{priority:0,distance:Math.hypot(point.x-a.x,point.y-a.y)}:hitGeometry(point,geometry,project);
        if(hit)candidates.push({...hit,layerId:id,featureId:feature.properties?.id||feature.id,feature,order,area:Math.abs((b.x-a.x)*(b.y-a.y))});
      });
    }
    return chooseHit(candidates);
  }
  function selectTap(point){
    const hit=resolveTap(point);if(!hit)return;
    const ll=map.containerPointToLatLng(point);notify(hit.layerId,hit.feature,[ll.lng,ll.lat]);
  }
  function cancelTap(){if(pendingTap)scope.clearTimeout(pendingTap);pendingTap=null;}
  function doubleClick(event){
    cancelTap();
    // An immediate mouse selection may fit a large feature. A double click
    // still zooms from the view in which the user began the gesture.
    if(event.originalEvent?.pointerType!=='touch'&&!event.originalEvent?.sourceCapabilities?.firesTouchEvents&&mouseTapZoom!==undefined)
      map.setZoomAround(event.latlng,Math.min(19,mouseTapZoom+1),{animate:false});
  }
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
    map=L.map(container,{zoomControl:false,doubleClickZoom:true,preferCanvas:true,minZoom:5,maxZoom:19,
      zoomAnimation:!reduced(),fadeAnimation:!reduced(),markerZoomAnimation:!reduced()});
    map.createPane('context');map.getPane('context').style.zIndex=350;
    map.on('moveend zoomend',publishView);
    map.on('dblclick',doubleClick);
    const surface=map.getContainer?.();
    if(surface){const click=event=>{
      if(event.detail>1||event.target.closest?.('.leaflet-control')||map.dragging?.moved()||(!event.clientX&&!event.clientY))return;
      const r=surface.getBoundingClientRect(),point={x:event.clientX-r.left,y:event.clientY-r.top};
      cancelTap();if(event.pointerType==='touch'||event.sourceCapabilities?.firesTouchEvents)pendingTap=setTimeout(()=>selectTap(point),TOUCH_TAP_WINDOW);else {mouseTapZoom=map.getZoom();selectTap(point);}
    };surface.addEventListener('click',click,true);mapBindings.push([surface,'click',click,true]);}
    map.setView([view.center[1],view.center[0]],view.zoom,{animate:false});
    for(const [name,delta] of [['zoomIn',1],['zoomOut',-1]]){
      const control=view.controls?.[name];if(!control)continue;
      const handler=event=>{event?.preventDefault();map?.setZoom(map.getZoom()+delta,{animate:false});};
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
    const layer=L.geoJSON(featureCollection,{pane,style,interactive:false,
      pointToLayer:(feature,latlng)=>marker(latlng,feature.properties),
      onEachFeature:(feature,item)=>{if(item.getLatLng)item.on('click',event=>{if(event.originalEvent?.type?.startsWith('key'))notify(id,feature,feature.geometry.coordinates.slice());});}});
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
      item.on('click',event=>{if(event.originalEvent?.type?.startsWith('key'))notify(id,pin,pin.coordinates.slice());});item.addTo(group);
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
        item.labelLayerId=id;occupied.push(box);labelled.add(item);shown++;count++;
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
    cancelTap();
    for(const [node,name,handler,capture] of mapBindings)node.removeEventListener(name,handler,capture);mapBindings=[];
    for(const [control,handler] of controlBindings)control.removeEventListener('click',handler);
    controlBindings=[];if(map){map.off('moveend zoomend',publishView);map.off('dblclick',doubleClick);map.remove();}
    map=null;baseLayer=null;mouseTapZoom=undefined;layers.clear();handlers.clear();styles.clear();labelRules.clear();labelled.clear();selected=null;
  }
  const api={init,addLayer,removeLayer,setVisible,setStyle,setPins,onFeature,fit,setBasemap,destroy,setSelected,setLabels};
  if(typeof module!=='undefined')module.exports=api;
  scope.ExploreMap=api;
})(typeof globalThis!=='undefined'?globalThis:this);
