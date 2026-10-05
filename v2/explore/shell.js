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
  function createShell(host,options){
    const M=scope.ExploreMap,E=scope.ExploreEvidence;
    host.classList.add('explore-root');
    host.innerHTML=`<div id="explore-map" class="explore-map" aria-label="Interactive map"></div>
      <header class="explore-topbar"><span class="explore-region"></span><nav aria-label="Explore"><button id="explore-layers" type="button" aria-expanded="false">Layers</button><button id="explore-search" type="button">Search</button></nav></header>
      <nav class="explore-tools" aria-label="Map controls"><button id="explore-satellite" type="button" aria-pressed="true">Satellite</button><button id="explore-topo" type="button" aria-pressed="false">Topo</button><button id="explore-fit" type="button">Fit area</button><button id="explore-zoom-in" type="button" aria-label="Zoom in">+</button><button id="explore-zoom-out" type="button" aria-label="Zoom out">−</button></nav>
      <section id="explore-sheet" class="explore-sheet" aria-label="Results"><div class="explore-sheet-header"><button id="explore-sheet-toggle" class="explore-sheet-toggle" type="button" aria-expanded="false">Results · Expand</button><p id="explore-summary" class="explore-summary" role="status">Loading</p></div><div id="explore-sheet-body" class="explore-sheet-body" inert></div></section>
      <aside id="explore-drawer" class="explore-drawer" aria-label="Layers & legend" hidden><div class="explore-heading"><h1>Layers & legend</h1><button id="explore-drawer-close" type="button" aria-label="Close layers">×</button></div><button id="explore-sources" type="button">Sources & coverage</button><div id="explore-layer-list"></div></aside>
      <dialog id="explore-source-dialog" class="explore-dialog" aria-labelledby="explore-source-title"><div class="explore-heading"><h1 id="explore-source-title">Sources & coverage</h1><button type="button" data-close aria-label="Close sources">×</button></div><div id="explore-source-body"></div></dialog>
      <dialog id="explore-detail-dialog" class="explore-dialog" aria-labelledby="explore-detail-title"><div class="explore-heading"><h1 id="explore-detail-title">Source details</h1><button type="button" data-close aria-label="Close details">×</button></div><div id="explore-detail-body"></div></dialog>
      <dialog id="explore-search-dialog" class="explore-dialog" aria-labelledby="explore-search-title"><div class="explore-heading"><h1 id="explore-search-title">Find trails</h1><button type="button" data-close aria-label="Close search">×</button></div><label>Trail name or number<input id="explore-query" type="search"></label><label>Activity<select id="explore-activity"><option value="">All activities</option></select></label><div id="explore-search-results"></div></dialog>
      <div id="explore-banner" class="explore-banner" role="status" hidden><span></span><button type="button">Dismiss</button></div>`;
    const $=id=>host.querySelector('#explore-'+id);
    const sheet=scope.ExploreSheet.createSheet($('sheet'),$('sheet-toggle'),$('sheet-body'));
    const drawer=scope.ExploreDrawer.createDrawer($('drawer'),$('layers'),$('drawer-close'));
    let region,manifest,mapAvailable=false,zoom=options.initialView?.zoom||10;
    const visibleLayers=new Set(),rows=new Map(),state={mapUsable:false,defaultLayersLoaded:false,view:null};
      const active={state,visibleLayers,sheet,drawer,get region(){return region;},showSources,showDetail,openDialog,$,element,button,drawLayer};
    function banner(text){$('banner').hidden=false;$('banner').querySelector('span').textContent=text;}
    $('banner').querySelector('button').onclick=()=>{$('banner').hidden=true;};
    const dialogOpeners=new Map();
    function openDialog(dialog,opener=document.activeElement){
      for(const other of host.querySelectorAll('dialog[open]'))other.close();
      dialogOpeners.set(dialog,opener);dialog.showModal();dialog.querySelector('button').focus();
    }
    for(const dialog of host.querySelectorAll('dialog')){
      dialog.querySelector('[data-close]').onclick=()=>dialog.close();
      dialog.addEventListener('close',()=>dialogOpeners.get(dialog)?.focus());
    }
    function appendEvidence(box,output){
      if(output.items){for(const item of output.items){
        const node=element(item.url?'a':'p',item.text);if(item.url){node.href=item.url;node.target='_blank';node.rel='noopener noreferrer';}box.append(node);
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
        if(loaded?.state==='loaded')body.append(element('p',loaded.count+' map features loaded'));
      }
      for(const link of region?.config.official_links||[])appendEvidence(body,{lines:[],links:[{label:link.label,url:E.safeUrl(link.url)}].filter(item=>item.url)});
      if(active.extras?.coverage)body.append(element('p',active.extras.coverage.text));
      openDialog($('source-dialog'));
    }
    function showDetail(entry,feature){
      const declaration=manifest.layers.find(layer=>layer.id===entry.id),body=$('detail-body');body.replaceChildren();
      const output=scope.ExploreLand?.tier(declaration)==='G'?scope.ExploreLand.detail(manifest,declaration,feature):E.feature(manifest,declaration,feature,entry.title,Date.now());
      $('detail-title').textContent=output.title;appendEvidence(body,output);
      body.append(button('Sources & coverage',showSources));
      options.onDetail?.(active,entry,feature,body);openDialog($('detail-dialog'));
      active.capabilities?.detail(entry,feature,body);
    }
    function styleFor(entry){
      if(scope.ExploreLand)return feature=>scope.ExploreLand.style(entry,zoom,feature);
      return {color:'#91a184',weight:1,opacity:.5,fillOpacity:.1};
    }
    function drawLayer(result){
      const entry=region.layers.get(result.id),row=rows.get(result.id);
      if(row){row.status.textContent=result.state==='loaded'?(result.count?result.count+' map features loaded':'No features in this dataset'):result.state==='failed'?'Could not load':result.state==='loading'?'Loading':'';row.retry.hidden=result.state!=='failed';}
      if(result.state==='loaded'){
        if(mapAvailable){M.addLayer(entry.id,result.data,styleFor(entry));M.onFeature(entry.id,feature=>showDetail(entry,feature));M.setVisible(entry.id,visibleLayers.has(entry.id));}
        options.onLayer?.(active,entry,result.data);renderResults();
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
        const status=element('span','', 'explore-layer-state'),retry=button('Retry',()=>void load(entry));retry.hidden=true;
        const actions=element('div',undefined,'explore-layer-actions');actions.append(status,retry,button('Show source',showSources));
        const legend=element('div',undefined,'explore-land-legend');
        row.append(label,element('p',entry.description),actions,legend);list.append(row);rows.set(entry.id,{row,status,retry,check,legend});renderLandLegend(entry,legend,[]);
        check.onchange=()=>{
          if(check.checked)visibleLayers.add(entry.id);else visibleLayers.delete(entry.id);
          M.setVisible(entry.id,check.checked);
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
      if(active.capabilities){active.capabilities.render();return;}
      if(options.renderResults){options.renderResults(active);return;}
      const body=$('sheet-body');body.replaceChildren();
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
        if(scope.TrailDiscovery.matches(feature,$('query').value,$('activity').value))box.append(button(feature.properties.name||entry.title,()=>showDetail(entry,feature)));
    }
    $('query').oninput=renderSearch;$('activity').onchange=renderSearch;
    $('search').onclick=()=>{if(active.capabilities?.search){active.capabilities.search();return;}renderSearch();openDialog($('search-dialog'));};$('sources').onclick=showSources;
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
        if(mapAvailable){M.fit(bounds(region.coverage));for(const entry of region.registry.filter(item=>item.format==='place_list')){
          const pins=region.places[entry.id];if(Array.isArray(pins)){M.setPins(entry.id,pins);M.onFeature(entry.id,pin=>showDetail(entry,pin));M.setVisible(entry.id,visibleLayers.has(entry.id));}
        }}
        $('search').hidden=!region.config.capabilities.trail_search;
        for(const [id,label] of Object.entries(scope.TrailDiscovery?.activities||{})){const option=element('option',label);option.value=id;$('activity').append(option);}
        state.mapUsable=true;options.onReady?.(active);
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
    active.destroy=()=>{sheet.destroy();drawer.destroy();M.destroy();host.replaceChildren();};
    return active;
  }
  const api={createShell,bounds};if(typeof module!=='undefined')module.exports=api;scope.ExploreShell=api;
})(typeof globalThis!=='undefined'?globalThis:this);
