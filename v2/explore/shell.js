(function(scope){
  'use strict';
  const element=(tag,text,className)=>{const node=document.createElement(tag);if(text!==undefined)node.textContent=text;if(className)node.className=className;return node;};
  const button=(text,handler)=>{const node=element('button',text);node.type='button';node.addEventListener('click',handler);return node;};
  function bounds(featureCollection){
    const points=[];
    const visit=value=>{if(!Array.isArray(value))return;if(typeof value[0]==='number')points.push(value);else value.forEach(visit);};
    for(const feature of featureCollection.features||[])visit(feature.geometry?.coordinates);
    if(!points.length)return null;
    let west=Infinity,south=Infinity,east=-Infinity,north=-Infinity;
    for(const [lon,lat] of points){west=Math.min(west,lon);south=Math.min(south,lat);east=Math.max(east,lon);north=Math.max(north,lat);}
    return [[west,south],[east,north]];
  }
  function mercatorPoint(coordinate,zoom){
    const scale=256*2**zoom,latitude=Math.max(-85.0511287798,Math.min(85.0511287798,coordinate[1]))*Math.PI/180;
    return {x:(coordinate[0]+180)/360*scale,y:(1-Math.log(Math.tan(latitude)+1/Math.cos(latitude))/Math.PI)/2*scale};
  }
  function inverseMercator(point,zoom){
    const scale=256*2**zoom,x=point.x/scale,y=point.y/scale;
    return [x*360-180,Math.atan(Math.sinh(Math.PI*(1-2*y)))*180/Math.PI];
  }
  function fitZoomForBounds(box,size,padding={}){
    if(!box||!Array.isArray(box)||box.length!==2)return null;
    const a=mercatorPoint(box[0],0),b=mercatorPoint(box[1],0),left=padding.topLeft?.[0]||0,top=padding.topLeft?.[1]||0,
      right=padding.bottomRight?.[0]||0,bottom=padding.bottomRight?.[1]||0;
    const width=Math.max(1,size.width-left-right),height=Math.max(1,size.height-top-bottom),spanX=Math.abs(b.x-a.x),spanY=Math.abs(b.y-a.y);
    const value=Math.log2(Math.min(width/Math.max(spanX,1e-12),height/Math.max(spanY,1e-12)));
    return Math.max(5,Math.min(15,Math.floor(value+1e-8)));
  }
  function viewportBoundsAt(coordinate,zoom,size,padding={}){
    const left=padding.topLeft?.[0]||0,top=padding.topLeft?.[1]||0,right=padding.bottomRight?.[0]||0,bottom=padding.bottomRight?.[1]||0;
    const width=Math.max(1,size.width-left-right)*.97,height=Math.max(1,size.height-top-bottom)*.97;
    const center=mercatorPoint(coordinate,zoom),west=inverseMercator({x:center.x-width/2,y:center.y},zoom)[0],
      east=inverseMercator({x:center.x+width/2,y:center.y},zoom)[0],
      north=inverseMercator({x:center.x,y:center.y-height/2},zoom)[1],
      south=inverseMercator({x:center.x,y:center.y+height/2},zoom)[1];
    return [[west,south],[east,north]];
  }
  const WGS84={a:6378137,f:1/298.257223563,b:6356752.314245179};
  function inverseGeodesic(start,end){
    const {a,f,b}=WGS84,toRad=Math.PI/180,phi1=start[1]*toRad,phi2=end[1]*toRad,L=(end[0]-start[0])*toRad;
    if(Math.abs(phi1-phi2)<1e-15&&Math.abs(L)<1e-15)return {distance:0,bearing:0};
    const U1=Math.atan((1-f)*Math.tan(phi1)),U2=Math.atan((1-f)*Math.tan(phi2)),sinU1=Math.sin(U1),cosU1=Math.cos(U1),
      sinU2=Math.sin(U2),cosU2=Math.cos(U2);let lambda=L,sinSigma,cosSigma,sigma,sinAlpha,cosSqAlpha,cos2SigmaM;
    for(let i=0;i<100;i++){
      const sinLambda=Math.sin(lambda),cosLambda=Math.cos(lambda),x=cosU2*sinLambda,
        y=cosU1*sinU2-sinU1*cosU2*cosLambda;
      sinSigma=Math.hypot(x,y);if(!sinSigma)return {distance:0,bearing:0};
      cosSigma=sinU1*sinU2+cosU1*cosU2*cosLambda;sigma=Math.atan2(sinSigma,cosSigma);
      sinAlpha=cosU1*cosU2*sinLambda/sinSigma;cosSqAlpha=1-sinAlpha*sinAlpha;
      cos2SigmaM=cosSqAlpha>1e-15?cosSigma-2*sinU1*sinU2/cosSqAlpha:0;
      const C=f/16*cosSqAlpha*(4+f*(4-3*cosSqAlpha)),next=L+(1-C)*f*sinAlpha*(sigma+C*sinSigma*(cos2SigmaM+C*cosSigma*(-1+2*cos2SigmaM*cos2SigmaM)));
      if(Math.abs(next-lambda)<1e-12){lambda=next;break;}lambda=next;
    }
    const uSq=cosSqAlpha*(a*a-b*b)/(b*b),A=1+uSq/16384*(4096+uSq*(-768+uSq*(320-175*uSq))),
      B=uSq/1024*(256+uSq*(-128+uSq*(74-47*uSq))),delta=B*sinSigma*(cos2SigmaM+B/4*(cosSigma*(-1+2*cos2SigmaM*cos2SigmaM)-
        B/6*cos2SigmaM*(-3+4*sinSigma*sinSigma)*(-3+4*cos2SigmaM*cos2SigmaM)));
    const bearing=Math.atan2(cosU2*Math.sin(lambda),cosU1*sinU2-sinU1*cosU2*Math.cos(lambda));
    return {distance:b*A*(sigma-delta),bearing};
  }
  function directGeodesic(start,bearing,distance){
    const {a,f,b}=WGS84,toRad=Math.PI/180,phi1=start[1]*toRad,lambda1=start[0]*toRad,
      sinAlpha1=Math.sin(bearing),cosAlpha1=Math.cos(bearing),tanU1=(1-f)*Math.tan(phi1),
      cosU1=1/Math.sqrt(1+tanU1*tanU1),sinU1=tanU1*cosU1,sigma1=Math.atan2(tanU1,cosAlpha1),
      sinAlpha=cosU1*sinAlpha1,cosSqAlpha=1-sinAlpha*sinAlpha,uSq=cosSqAlpha*(a*a-b*b)/(b*b),
      A=1+uSq/16384*(4096+uSq*(-768+uSq*(320-175*uSq))),B=uSq/1024*(256+uSq*(-128+uSq*(74-47*uSq)));
    let sigma=distance/(b*A),previous;
    for(let i=0;i<100;i++){
      const cos2=Math.cos(2*sigma1+sigma),sinSigma=Math.sin(sigma),cosSigma=Math.cos(sigma),delta=B*sinSigma*(cos2+B/4*(cosSigma*(-1+2*cos2*cos2)-
        B/6*cos2*(-3+4*sinSigma*sinSigma)*(-3+4*cos2*cos2)));
      previous=sigma;sigma=distance/(b*A)+delta;if(Math.abs(sigma-previous)<1e-12)break;
    }
    const sinSigma=Math.sin(sigma),cosSigma=Math.cos(sigma),tmp=sinU1*sinSigma-cosU1*cosSigma*cosAlpha1,
      phi2=Math.atan2(sinU1*cosSigma+cosU1*sinSigma*cosAlpha1,(1-f)*Math.sqrt(sinAlpha*sinAlpha+tmp*tmp)),
      lambda=Math.atan2(sinSigma*sinAlpha1,cosU1*cosSigma-sinU1*sinSigma*cosAlpha1),cos2=Math.cos(2*sigma1+sigma),
      C=f/16*cosSqAlpha*(4+f*(4-3*cosSqAlpha)),L=lambda-(1-C)*f*sinAlpha*(sigma+C*sinSigma*(cos2+C*cosSigma*(-1+2*cos2*cos2)));
    return [(lambda1+L)/toRad,phi2/toRad];
  }
  function waterMidpointMember(feature){
    const geometry=feature.geometry;if(!geometry||!['LineString','MultiLineString'].includes(geometry.type))return null;
    const lines=geometry.type==='LineString'?[geometry.coordinates]:geometry.coordinates,
      lengths=lines.map(line=>line.slice(1).reduce((sum,point,index)=>sum+inverseGeodesic(line[index],point).distance,0)),
      total=lengths.reduce((sum,length)=>sum+length,0);
    if(!total)return lines.length?{line:lines[0],point:lines[0][0],lineIndex:0}:null;
    // The river midpoint is the point at half its drawn WGS84 geodesic length across the ordered member lines.
    let remaining=total/2;
    for(let lineIndex=0;lineIndex<lines.length;lineIndex++){
      const line=lines[lineIndex];if(remaining>lengths[lineIndex]){remaining-=lengths[lineIndex];continue;}
      for(let i=1;i<line.length;i++){
        const inverse=inverseGeodesic(line[i-1],line[i]);if(remaining>inverse.distance){remaining-=inverse.distance;continue;}
        return {line,point:directGeodesic(line[i-1],inverse.bearing,remaining),lineIndex};
      }
      return {line,point:line.at(-1),lineIndex};
    }
    return null;
  }
  function selectionCameraPolicy(entry,geometryType){
    const geometryPolicy=/Polygon$/.test(geometryType||'')?'preserve':'fit';
    const override=entry?.selectionCameraPolicy;
    if(override==='fit'||override==='preserve')return override;
    return geometryPolicy;
  }
  function selectionFitAction(entry,geometryType,origin,currentZoom,fitZoom){
    if(selectionCameraPolicy(entry,geometryType)==='preserve')return 'preserve';
    const policy=entry?.fitPolicy||{};
    if(origin==='tap'&&Number.isFinite(policy.tap?.max_zoom_out)&&Number.isFinite(currentZoom)&&Number.isFinite(fitZoom)&&
       currentZoom-fitZoom>policy.tap.max_zoom_out)return 'tap-cap';
    if(origin!=='tap'&&Number.isFinite(policy.list?.min_zoom)&&Number.isFinite(fitZoom)&&fitZoom<policy.list.min_zoom)return 'list-cap';
    return 'fit';
  }
  function createShell(host,options){
    const M=scope.ExploreMap,E=scope.ExploreEvidence;
    host.classList.add('explore-root');
    const viewport=scope.visualViewport,viewportChanged=()=>{if(viewport?.scale&&viewport.scale!==1)return;host.style.setProperty('--viewport-height',(viewport?.height||scope.innerHeight)+'px');host.style.setProperty('--viewport-top',(viewport?.offsetTop||0)+'px');};
    viewportChanged();for(const name of ['resize','orientationchange'])scope.addEventListener(name,viewportChanged);for(const name of ['resize','scroll'])viewport?.addEventListener(name,viewportChanged);
    host.innerHTML=`<div id="explore-map" class="explore-map" aria-label="Interactive map"></div>
      <header class="explore-topbar"><span class="explore-region"></span><nav aria-label="Explore"><button id="explore-layers" type="button" aria-expanded="false">Layers</button><button id="explore-search" type="button">Search</button></nav></header>
      <nav class="explore-tools" aria-label="Map controls"><button id="explore-satellite" type="button" aria-pressed="true">Satellite</button><button id="explore-topo" type="button" aria-pressed="false">Topo</button><button id="explore-fit" type="button">Fit area</button><button id="explore-zoom-in" type="button" aria-label="Zoom in">+</button><button id="explore-zoom-out" type="button" aria-label="Zoom out">−</button></nav>
      <section id="explore-sheet" class="explore-sheet" aria-label="Results"><div class="explore-sheet-header"><button id="explore-sheet-toggle" class="explore-sheet-toggle" type="button" aria-expanded="false">Results · Expand</button><p id="explore-summary" class="explore-summary" role="status">Loading</p></div><div id="explore-sheet-body" class="explore-sheet-body" inert><div id="explore-list-view"><div id="explore-list-body"></div><div id="explore-search-view" hidden><button id="explore-search-back" type="button">Results</button><details class="explore-filters"><summary>Filters</summary><label>Trail name or number<input id="explore-query" type="search"></label><label>Activity<select id="explore-activity"><option value="">All activities</option></select></label></details><div id="explore-search-results"></div></div></div><section id="explore-detail-view" hidden><div class="explore-detail-heading"><button id="explore-detail-back" type="button">Back</button><h2 id="explore-detail-title">Source details</h2></div><div id="explore-detail-body"></div></section></div></section>
      <aside id="explore-drawer" class="explore-drawer" aria-label="Layers & legend" hidden><div class="explore-heading"><h1>Layers & legend</h1><button id="explore-drawer-close" type="button" aria-label="Close layers">×</button></div><div class="explore-drawer-body"><p>Turn layers on or off. Colors explain what the map can tell you; they do not prove a place is legal to camp.</p><p>All layers start on. Dates and vehicle choices do not hide map features. Tap a road or shaded area to learn more.</p><button id="explore-sources" type="button">Sources & coverage</button><div id="explore-layer-list"></div></div></aside>
      <dialog id="explore-source-dialog" class="explore-dialog" aria-labelledby="explore-source-title"><div class="explore-heading"><h1 id="explore-source-title">Sources & coverage</h1><button type="button" data-close aria-label="Close sources">×</button></div><div id="explore-source-body"></div></dialog>
      <div id="explore-banner" class="explore-banner" role="status" hidden><span></span><button type="button">Dismiss</button></div>`;
    const $=id=>host.querySelector('#explore-'+id);
    const sheet=scope.ExploreSheet.createSheet($('sheet'),$('sheet-toggle'),$('sheet-body'));
    const drawer=scope.ExploreDrawer.createDrawer($('drawer'),$('layers'),$('drawer-close'));
    const phone=()=>!scope.matchMedia('(min-width:768px)').matches||scope.ExploreSheet.shortLandscape();
    const drawerState=event=>{if(phone()&&event.detail.open)sheet.setState('collapsed');};
    const sheetState=event=>{if(phone()&&event.detail.state!=='collapsed')drawer.close(false);};
    const bottomSheetViewport=()=>!scope.matchMedia('(min-width:768px)').matches&&!scope.ExploreSheet.shortLandscape();
    const mapTap=event=>{
      drawer.close();
      if(event.detail?.hit===false&&bottomSheetViewport()&&sheet.state!=='collapsed')sheet.setState('collapsed');
    };
    $('drawer').addEventListener('drawerstatechange',drawerState);
    $('sheet').addEventListener('sheetstatechange',sheetState);$('map').addEventListener('exploremaptap',mapTap);
    let region,manifest,mapAvailable=false,zoom=options.initialView?.zoom||10;
    const visibleLayers=new Set(),rows=new Map(),state={mapUsable:false,defaultLayersLoaded:false,view:null};
      const active={state,visibleLayers,sheet,drawer,get region(){return region;},showSources,showDetail,select,showList,isListActive,openDialog,$,element,button,drawLayer};
    function banner(text){$('banner').hidden=false;$('banner').querySelector('span').textContent=text;}
    $('banner').querySelector('button').onclick=()=>{$('banner').hidden=true;};
    const dialogOpeners=new Map(),boundDialogs=new WeakSet();
    function openDialog(dialog,opener=document.activeElement){
      for(const other of host.querySelectorAll('dialog[open]'))other.close();
      if(!opener||opener.closest('[hidden],[inert]'))opener=$('sheet-toggle');
      if(!boundDialogs.has(dialog)){dialog.addEventListener('close',()=>dialogOpeners.get(dialog)?.focus());boundDialogs.add(dialog);}
      dialogOpeners.set(dialog,opener);dialog.showModal();dialog.querySelector('button').focus();
    }
    for(const dialog of host.querySelectorAll('dialog')){
      dialog.querySelector('[data-close]').onclick=()=>dialog.close();
    }
    function appendEvidence(box,output){
      if(output.items){for(const item of output.items){
        const node=element(item.heading?'h3':item.url?'a':'p',item.text);if(item.url){node.href=item.url;node.target='_blank';node.rel='noopener noreferrer';}box.append(node);
      }return;}
      for(const line of output.lines)box.append(element('p',line));
      for(const item of output.links){const link=element('a',item.label);link.href=item.url;link.target='_blank';link.rel='noopener noreferrer';box.append(link);}
    }
    function showSources(){
      const body=$('source-body');body.replaceChildren();
      if(manifest)appendEvidence(body,E.region(manifest));
      if(region)for(const declaration of manifest.layers){
        const entry=region.registry.find(item=>item.id===declaration.id),loaded=region.layers.get(declaration.id);
        body.append(element('h2',entry?.title||declaration.id));
        appendEvidence(body,E.layer(manifest,declaration,region.index,loaded?.count||0,Date.now()));
        if(loaded?.state==='loaded')body.append(element('p',loaded.count+' features'));
        for(const feature of loaded?.data?.features||[])if(feature.geometry===null&&declaration.allow_null_geometry===true){
          const node=button(feature.properties.name||entry.title,()=>showDetail(entry,feature));node.dataset.nonspatial=declaration.id;body.append(node);
        }
      }
      for(const link of region?.config.official_links||[])appendEvidence(body,{lines:[],links:[{label:link.label,url:E.safeUrl(link.url)}].filter(item=>item.url)});
      if(active.extras?.coverage)body.append(element('p',active.extras.coverage.text));
      openDialog($('source-dialog'));
    }
    let listScroll=0,listOpener,activeList=$('list-body');
    function isListActive(node){return activeList===node;}
    function showList(node=activeList){
      const changed=node!==activeList;activeList=node;
      if(!node.parentNode||node.parentNode!==$('list-view'))$('list-view').append(node);
      for(const child of $('list-view').children)child.hidden=child!==node;
      $('list-view').hidden=false;$('detail-view').hidden=true;
      $('sheet-body').scrollTop=changed?0:listScroll;
      if(!sheet.expanded)sheet.setState('half');
    }
    function backToList(){if(state.selection)M.setSelected(state.selection.layerId,null);state.selection=null;showList();listOpener?.focus({preventScroll:true});}
    $('detail-back').onclick=backToList;
    $('search-back').onclick=()=>showList($('list-body'));
    function select(entry,feature,origin='list',tapCoordinates=null){
      if(!entry)return;
      const featureId=feature.properties?.id||feature.id;
      state.selection={layerId:entry.id,featureId};
      M.setSelected(entry.id,featureId);
      const geometry=feature.geometry||(feature.coordinates?{type:'Point',coordinates:feature.coordinates}:null);
      if(mapAvailable&&geometry){
        visibleLayers.add(entry.id);const row=rows.get(entry.id);if(row){row.check.checked=true;row.mode.textContent='On';}M.setVisible(entry.id,true);
        if(selectionCameraPolicy(entry,geometry.type)==='fit'){
          const phone=!scope.matchMedia('(min-width:768px)').matches&&!scope.ExploreSheet.shortLandscape();
          const mapRect=$('map').getBoundingClientRect(),panelRect=$('sheet').getBoundingClientRect(),safeBottom=parseFloat(scope.getComputedStyle(host).getPropertyValue('--safe-bottom'))||0;
          const panelWidth=scope.ExploreSheet.shortLandscape()?Math.min(320,host.clientWidth*.4):340;
          const padding={topLeft:[phone?24:panelRect.left-mapRect.left+panelWidth+24,$('zoom-in').getBoundingClientRect().bottom-mapRect.top+8],bottomRight:[24,phone?Math.round(scope.ExploreSheet.panelViewport(host)*.4)+safeBottom+24:safeBottom+24]},
            policy=entry.fitPolicy||{},fitBounds=bounds({features:[{geometry}]}),size={width:mapRect.width,height:mapRect.height},
            currentZoom=zoom,fitZoom=fitZoomForBounds(fitBounds,size,padding),action=selectionFitAction(entry,geometry.type,origin,currentZoom,fitZoom);
          if(action==='fit')M.fit(fitBounds,padding);
          else if(action==='tap-cap'){
            const coordinate=Array.isArray(tapCoordinates)?tapCoordinates:waterMidpointMember(feature)?.point;
            if(coordinate){M.fit(viewportBoundsAt(coordinate,currentZoom,size,padding),padding);if(currentZoom>15)scope.setTimeout(()=>{for(let i=15;i<currentZoom;i++)$('zoom-in').click();},350);}
          }else if(action==='list-cap'){
            const midpoint=waterMidpointMember(feature),minimum=policy.list.min_zoom;
            if(midpoint)M.fit(viewportBoundsAt(midpoint.point,minimum,size,padding),padding);
          }
        }
      }
      showFeatureDetail(entry,feature);
    }
    function showDetail(entry,feature,origin='list',tapCoordinates=null){select(entry,feature,origin,tapCoordinates);}
    function showFeatureDetail(entry,feature){
      if($('detail-view').hidden){listScroll=$('sheet-body').scrollTop;listOpener=document.activeElement;}
      for(const dialog of host.querySelectorAll('dialog[open]'))dialog.close();
      const declaration=manifest.layers.find(layer=>layer.id===entry.id),body=$('detail-body');body.replaceChildren();
      const output=entry.kind==='water'?scope.ExploreWaterDetail.feature(manifest,declaration,feature):scope.ExploreLand?.tier(declaration)==='G'?scope.ExploreLand.detail(manifest,declaration,feature):E.feature(manifest,declaration,feature,entry.title,Date.now());
      $('detail-title').textContent=output.title;const actions=element('div',undefined,'explore-detail-actions');body.append(actions);appendEvidence(body,output);
      body.append(button('Sources & coverage',showSources));
      options.onDetail?.(active,entry,feature,body);
      $('list-view').hidden=true;$('detail-view').hidden=false;$('sheet-body').scrollTop=0;
      sheet.setState('half');$('detail-back').focus({preventScroll:true});
      active.capabilities?.detail(entry,feature,body,actions);
    }
    function styleFor(entry){
      if(scope.ExploreLand)return feature=>scope.ExploreLand.style(entry,zoom,feature);
      return {color:'#91a184',weight:1,opacity:.5,fillOpacity:.1};
    }
    function drawLayer(result){
      const entry=region.layers.get(result.id),row=rows.get(result.id);
      if(row){row.status.textContent=result.state==='loaded'?(result.count?result.count+' map features loaded':'No features in this dataset'):result.state==='failed'?'Could not load':result.state==='loading'?'Loading':'';row.retry.hidden=result.state!=='failed';}
      if(result.state==='loaded'){
        if(mapAvailable){M.addLayer(entry.id,result.data,styleFor(entry));if(['trails','recreation_sites'].includes(entry.kind)||entry.kind==='water'&&entry.displaySelect==='streams')M.setLabels(entry.id,{property:'name',minZoom:14,max:entry.kind==='water'?32:24});M.onFeature(entry.id,(feature,coordinates)=>showDetail(entry,feature,'tap',coordinates));M.setVisible(entry.id,visibleLayers.has(entry.id));}
        options.onLayer?.(active,entry,result.data);renderResults();if(!$('search-view').hidden)renderSearch();
        renderLandLegend(entry,row?.legend,result.data.features);
      }
    }
    async function load(entry){drawLayer({id:entry.id,state:'loading'});drawLayer(await region.loadLayer(entry.id,zoom));}
    function viewChanged(value){
      state.view=value;zoom=value.zoom;
      if(!region)return;
      for(const entry of region.registry){
        if(region.layers.get(entry.id).state==='loaded')M.setStyle(entry.id,styleFor(entry));
        else if(visibleLayers.has(entry.id)&&entry.minZoom!==null&&zoom>=entry.minZoom&&region.layers.get(entry.id).state!=='loading')void load(entry);
      }
    }
    function renderDrawer(){
      const list=$('layer-list');list.replaceChildren();
      for(const entry of region.registry){
        const row=element('section',undefined,'explore-layer'),label=element('label'),check=element('input');check.type='checkbox';check.checked=entry.defaultOn;check.id='layer-'+entry.id;
        if(check.checked)visibleLayers.add(entry.id);label.append(check,element('span',entry.title));
        const mode=element('span',check.checked?'On':'Off','explore-layer-mode'),status=element('span','', 'explore-layer-state'),retry=button('Retry',()=>void load(entry));retry.hidden=true;
        const actions=element('div',undefined,'explore-layer-actions');actions.append(mode,status,retry,button('Show source',showSources));
        const legend=element('div',undefined,'explore-land-legend');
        const agencies=[...new Set(entry.sourceIds.map(id=>manifest.sources[id]?.agency).filter(Boolean))];
        row.dataset.layerId=entry.id;row.append(label);if(agencies.length)row.append(element('p','Source: '+agencies.join(' · '),'explore-layer-source'));
        row.append(element('p',entry.description,'explore-layer-limitation'),actions,legend);list.append(row);rows.set(entry.id,{row,status,retry,check,legend,mode});renderLandLegend(entry,legend,[]);
        if(entry.format==='place_list'){const list=region.places[entry.id];status.textContent=Array.isArray(list)?(list.length?list.length+' locations loaded':'No features in this dataset'):'Could not load';}
        check.onchange=()=>{
          if(check.checked)visibleLayers.add(entry.id);else visibleLayers.delete(entry.id);
          mode.textContent=check.checked?'On':'Off';M.setVisible(entry.id,check.checked);
          if(check.checked&&entry.format==='feature_collection'&&region.layers.get(entry.id).state!=='loaded')void load(entry);
        };
      }
    }
    function renderLandLegend(entry,box,features){
      if(!box||!scope.ExploreLand)return;box.replaceChildren();
      const agency=manifest.sources[entry.sourceIds[0]]?.agency||'';
      for(const item of scope.ExploreLand.legend(entry,features,entry.title,agency)){
        const node=element('p',item.text);if(item.color)node.style.borderLeft='8px solid '+item.color;box.append(node);
      }
    }
    function renderResults(){
      if(active.capabilities){active.capabilities.render();
        if(Object.values(region.places).some(list=>!Array.isArray(list))){$('summary').textContent='Listings could not load';$('sheet-body').append(element('p','Listings could not load'));}
        return;}
      if(options.renderResults){options.renderResults(active);return;}
      const body=$('list-body');body.replaceChildren();
      const lists=Object.entries(region.places),failed=lists.some(([,list])=>!Array.isArray(list));
      if(failed)body.append(element('p','Listings could not load'));
      let count=0;
      for(const [id,list] of lists){if(!Array.isArray(list))continue;count+=list.length;
        for(const place of list){const entry=region.registry.find(item=>item.id===id);body.append(button(place.name,()=>showDetail(entry,place)));}
      }
      $('summary').textContent=failed?'Listings could not load':count+' locations loaded';
    }
    function renderSearch(){
      const box=$('search-results');box.replaceChildren();
      for(const entry of region.registry.filter(item=>item.kind==='trails'))for(const feature of [...(region.layers.get(entry.id).data?.features||[])].sort((a,b)=>(a.properties.name||'').localeCompare(b.properties.name||'')))
        if(scope.TrailDiscovery.matches(feature,$('query').value,$('activity').value)){const node=button(feature.properties.name||entry.title,()=>showDetail(entry,feature));node.dataset.feature=feature.properties.id;box.append(node);}
      for(const row of scope.ExploreWaterDetail.searchRows(region,$('query').value)){const node=button(row.feature.properties.name,()=>showDetail(row.entry,row.feature));node.dataset.feature=row.feature.properties.id;box.append(node);}
    }
    $('query').oninput=renderSearch;$('activity').onchange=renderSearch;
    $('search').onclick=()=>{if(active.capabilities?.search){active.capabilities.search();return;}renderSearch();showList($('search-view'));};$('sources').onclick=showSources;
    for(const mode of ['satellite','topo'])$(mode).onclick=()=>{M.setBasemap(mode);$('satellite').setAttribute('aria-pressed',String(mode==='satellite'));$('topo').setAttribute('aria-pressed',String(mode==='topo'));};
    $('fit').onclick=()=>{sheet.setExpanded(false);M.fit(bounds(region?.coverage||{features:[]}));};
    async function start(){
      mapAvailable=M.init($('map'),{...(options.initialView||{center:[0,0],zoom:10}),onViewChange:viewChanged,controls:{zoomIn:$('zoom-in'),zoomOut:$('zoom-out')}});
      if(!mapAvailable){$('map').textContent='Map could not load';for(const node of host.querySelectorAll('.explore-tools button'))node.disabled=true;}
      const loader=scope.RegionLoader.createRegionLoader({fetch:options.fetch||scope.fetch.bind(scope),basePath:options.basePath||'',defaultRegion:options.defaultRegion,
        onManifest:value=>{manifest=value;options.onManifest?.(value);}});
      try{
        region=await loader.loadRegion(options.search??scope.location.search);active.manifest=manifest;
        if(region.config.capabilities.region_extras){
          try{await new Promise((resolve,reject)=>{const script=element('script');script.src=(options.basePath?options.basePath.replace(/\/$/,'')+'/':'')+'regions/'+region.regionId+'/extras.js';script.onload=resolve;script.onerror=reject;host.append(script);});active.extras=scope.RegionExtras;}catch{active.extrasFailed=true;}
        }
        active.capabilities=scope.ExploreCapabilities?.attach(active);
        host.querySelector('.explore-region').textContent=manifest.region.name;
        renderDrawer();renderResults();
        if(mapAvailable)for(const entry of region.registry.filter(item=>item.kind==='water'&&item.displaySelect==='streams'))M.setLabels(entry.id,{property:'name',minZoom:14,max:32});
        if(mapAvailable){M.addLayer('coverage',region.coverage,{color:'#fff',weight:1,opacity:.5,dashArray:'6 5',fill:false});M.fit(bounds(region.coverage));for(const entry of region.registry.filter(item=>item.format==='place_list')){
          const pins=active.capabilities?.pins?.(entry)||region.places[entry.id];if(Array.isArray(pins)){M.setPins(entry.id,pins);M.setLabels(entry.id,{property:'name',minZoom:14,max:8});M.onFeature(entry.id,pin=>showDetail(entry,pin));M.setVisible(entry.id,visibleLayers.has(entry.id));}
        }}
        $('search').hidden=!region.config.capabilities.trail_search;
        for(const [id,label] of Object.entries(scope.TrailDiscovery?.activities||{})){const option=element('option',label);option.value=id;$('activity').append(option);}
        state.mapUsable=true;options.onReady?.(active);
        await new Promise(resolve=>requestAnimationFrame(()=>setTimeout(resolve,0)));
        await region.loadDefaultLayers({zoom,onState:drawLayer,yieldTask:()=>new Promise(resolve=>setTimeout(resolve,0))});
        state.defaultLayersLoaded=true;options.onComplete?.(active);return active;
      }catch(error){
        state.error=error.code||'REGION_NOT_AVAILABLE';$('summary').textContent='Region not available';$('sheet-body').replaceChildren(element('p','Region not available'));
        const link=element('a','Return to default region');link.href='?region='+encodeURIComponent(options.defaultRegion)+'&view=map';$('sheet-body').append(link);
        sheet.setExpanded(true);if(manifest)$('sheet-body').append(button('Sources & coverage',showSources));
        return active;
      }
    }
    active.start=start;active.renderResults=renderResults;active.renderSearch=renderSearch;
    active.destroy=()=>{for(const name of ['resize','orientationchange'])scope.removeEventListener(name,viewportChanged);for(const name of ['resize','scroll'])viewport?.removeEventListener(name,viewportChanged);$('drawer').removeEventListener('drawerstatechange',drawerState);$('sheet').removeEventListener('sheetstatechange',sheetState);$('map').removeEventListener('exploremaptap',mapTap);sheet.destroy();drawer.destroy();M.destroy();host.replaceChildren();};
    return active;
  }
  const api={createShell,bounds,selectionCameraPolicy,fitZoomForBounds,viewportBoundsAt,waterMidpointMember,selectionFitAction};if(typeof module!=='undefined')module.exports=api;scope.ExploreShell=api;
})(typeof globalThis!=='undefined'?globalThis:this);
