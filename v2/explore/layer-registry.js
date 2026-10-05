(function(scope){
  'use strict';
  const FORBIDDEN_WORDS=/\b(verified|legal|permitted|open|allowed|private|public)\b/i;
  class LayerRegistryError extends Error{
    constructor(message){super(message);this.name='LayerRegistryError';}
  }

  function validateConfig(manifest,config){
    const fail=()=>{throw new LayerRegistryError('Explore configuration is invalid');};
    const object=(value,keys,required=[])=>{
      if(!value||typeof value!=='object'||Array.isArray(value)||Object.keys(value).some(key=>!keys.includes(key))||required.some(key=>!Object.hasOwn(value,key)))fail();
    };
    object(config,['explore_version','region_id','initial_view','layers','capabilities','official_links','storage_keys','trip_defaults','landing','export_names'],
      ['explore_version','region_id','initial_view','layers','capabilities','official_links']);
    if(config.explore_version!==1||config.region_id!==manifest.region?.id||!/^[a-z0-9-]+$/.test(config.region_id))fail();
    object(config.initial_view,['center','zoom'],['center','zoom']);
    const center=config.initial_view.center,zoom=config.initial_view.zoom;
    if(!Array.isArray(center)||center.length!==2||!center.every(Number.isFinite)||Math.abs(center[0])>180||Math.abs(center[1])>90||!Number.isFinite(zoom)||zoom<5||zoom>19)fail();
    const capabilities=['trip_planner','trail_search','trail_season_check','gpx_export','saved_list','adventure_pilot'];
    object(config.capabilities,[...capabilities,'region_extras'],capabilities);
    if(Object.values(config.capabilities).some(value=>typeof value!=='boolean'))fail();
    if(!Array.isArray(config.layers)||!Array.isArray(config.official_links))fail();
    for(const item of config.layers){
      object(item,['layer_id','title','order','default_on','min_zoom'],['layer_id','title','order','default_on','min_zoom']);
      if(typeof item.layer_id!=='string'||typeof item.title!=='string'||!item.title||!Number.isFinite(item.order)||typeof item.default_on!=='boolean'||
        (item.min_zoom!==null&&(!Number.isFinite(item.min_zoom)||item.min_zoom<5||item.min_zoom>19)))fail();
    }
    for(const item of config.official_links){
      object(item,['label','url'],['label','url']);
      try{if(typeof item.label!=='string'||!item.label||!['http:','https:'].includes(new URL(item.url).protocol))fail();}catch{fail();}
    }
    if(config.storage_keys){object(config.storage_keys,['trip','plan','notes']);if(Object.values(config.storage_keys).some(value=>typeof value!=='string'||!/^[a-z0-9-]+$/.test(value)))fail();}
    if(config.trip_defaults){
      object(config.trip_defaults,['resort','arrive','depart','vehicle','start','end','activity']);
      for(const [key,value] of Object.entries(config.trip_defaults)){
        if(typeof value!=='string')fail();
        if(['arrive','depart','start','end'].includes(key)){
          const timestamp=Date.parse(value+'T00:00:00Z');
          if(!/^\d{4}-\d{2}-\d{2}$/.test(value)||!Number.isFinite(timestamp)||new Date(timestamp).toISOString().slice(0,10)!==value)fail();
        }
      }
    }
    if(config.export_names){object(config.export_names,['plan']);if(Object.values(config.export_names).some(value=>typeof value!=='string'||!/^[a-z0-9-]+\.json$/.test(value)))fail();}
    if(config.landing){
      object(config.landing,['eyebrow','title','lead','note','explore_label','mountains','region_links']);
      for(const [key,value] of Object.entries(config.landing))if(!['mountains','region_links'].includes(key)&&typeof value!=='string')fail();
      for(const item of config.landing.mountains||[]){object(item,['value','label'],['value','label']);if(typeof item.value!=='string'||typeof item.label!=='string')fail();}
      for(const item of config.landing.region_links||[]){object(item,['region_id','label'],['region_id','label']);if(!/^[a-z0-9-]+$/.test(item.region_id)||typeof item.label!=='string'||!item.label)fail();}
    }
    // Only the landing action field has a separately pinned wording exception.
    const checkWords=(value,path='')=>{
      if(typeof value==='string'&&path!=='landing.explore_label'&&FORBIDDEN_WORDS.test(value))fail();
      if(Array.isArray(value))value.forEach((child,index)=>checkWords(child,path+'.'+index));
      else if(value&&typeof value==='object')Object.entries(value).forEach(([key,child])=>checkWords(child,path?path+'.'+key:key));
    };
    checkWords(config);
  }

  function buildLayerRegistry(manifest,config){
    if(!manifest || !Array.isArray(manifest.layers)) throw new LayerRegistryError('Manifest layers are missing');
    if(!config || !Array.isArray(config.layers)) throw new LayerRegistryError('Explore layers are missing');
    validateConfig(manifest,config);
    const manifestLayers=new Map(manifest.layers.map(layer=>[layer.id,layer]));
    const seen=new Set();
    const entries=config.layers.map(item=>{
      if(!item || typeof item.layer_id!=='string' || seen.has(item.layer_id)) throw new LayerRegistryError('Explore layer IDs must be unique');
      const layer=manifestLayers.get(item.layer_id);
      if(!layer) throw new LayerRegistryError('Explore layer is not in the manifest: '+item.layer_id);
      seen.add(item.layer_id);
      return {
        id:item.layer_id,
        title:item.title,
        description:layer.limitations,
        kind:layer.kind,
        spatialPrecision:layer.spatial_precision,
        classificationSourceField:layer.classification_source_field||null,
        statusRef:layer.status_ref||null,
        maxAgeHours:layer.max_age_hours,
        order:Number.isFinite(item.order)?item.order:0,
        defaultOn:item.default_on===true,
        minZoom:item.min_zoom===null||item.min_zoom===undefined?null:item.min_zoom,
        format:layer.format,
        displayPath:layer.display?.path||null,
        canonicalPath:layer.path,
        pointer:layer.pointer,
        sourceIds:Array.isArray(layer.source_ids)?layer.source_ids.slice():[],
        geometryTypes:Array.isArray(layer.geometry_types)?layer.geometry_types.slice():[],
        state:'idle'
      };
    });
    for(const layer of manifest.layers){
      if(layer.format==='feature_collection' && layer.display && !seen.has(layer.id)){
        throw new LayerRegistryError('Displayed manifest layer is absent from Explore config: '+layer.id);
      }
    }
    return entries.sort((a,b)=>a.order-b.order||a.id.localeCompare(b.id));
  }

  const api={buildLayerRegistry,validateConfig,LayerRegistryError};
  if(typeof module!=='undefined') module.exports=api;
  scope.LayerRegistry=api;
})(typeof globalThis!=='undefined'?globalThis:this);
