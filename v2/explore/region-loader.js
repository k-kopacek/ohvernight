(function(scope){
  'use strict';
  const registryApi=(typeof require==='function'?require('./layer-registry.js'):scope.LayerRegistry);
  const REGION_ID=/^[a-z0-9-]+$/;
  class RegionLoaderError extends Error{
    constructor(code,message){super(message);this.name='RegionLoaderError';this.code=code;}
  }

  function resolveRegionId(search,defaultRegion){
    let value;
    if(search instanceof URLSearchParams) value=search.get('region');
    else if(typeof search==='string') value=new URLSearchParams(search.replace(/^\?/,'')).get('region');
    else if(search && typeof search==='object') value=search.region||(
      typeof search.search==='string'?new URLSearchParams(search.search.replace(/^\?/,'')).get('region'):undefined);
    value=value===null||value===undefined||value===''?defaultRegion:value;
    if(typeof value!=='string' || !REGION_ID.test(value)){
      throw new RegionLoaderError('REGION_NOT_FOUND','Region identifier is invalid');
    }
    return value;
  }

  function joinPath(base,path){
    const left=String(base||'').replace(/\/+$/,'');
    return left?left+'/'+path:path;
  }

  function pointerGet(document,pointer){
    if(pointer===undefined||pointer===null||pointer==='') return document;
    if(typeof pointer!=='string'||pointer[0]!=='/') throw new Error('Invalid JSON pointer');
    let value=document;
    for(const raw of pointer.slice(1).split('/')){
      const token=raw.replace(/~1/g,'/').replace(/~0/g,'~');
      value=value[Array.isArray(value)?Number(token):token];
    }
    return value;
  }

  function activePath(regionId,path,kind){
    if(typeof path!=='string'||!path||path.includes('..')||path.startsWith('/')||/^https?:/i.test(path)){
      throw new Error('Invalid '+kind+' path');
    }
    const prefix='regions/'+regionId+'/';
    if(path.startsWith('regions/')&&!path.startsWith(prefix)) throw new Error('Path is outside active region');
    if(kind==='display' && !path.startsWith(prefix+'display/')) throw new Error('Display path is outside active region');
    return path;
  }

  async function readJson(fetcher,url){
    return parseResponse(await fetcher(url));
  }

  async function parseResponse(response){
    if(response && typeof response.json==='function'){
      if(response.ok===false) throw new Error('HTTP '+(response.status||0));
      return response.json();
    }
    return response;
  }

  function restoreEvidence(document){
    const table=Array.isArray(document.evidence_table)?document.evidence_table:[];
    if(!Array.isArray(document.features)) throw new Error('Display file is not a FeatureCollection');
    return {...document,features:document.features.map(feature=>{
      const properties={...(feature.properties||{})};
      if(!Object.prototype.hasOwnProperty.call(properties,'evidence')) return {...feature,properties};
      if(properties.evidence && typeof properties.evidence==='object') return {...feature,properties};
      if(!Number.isInteger(properties.evidence) || properties.evidence<0 || properties.evidence>=table.length)
        throw new Error('Display evidence reference is unresolved');
      properties.evidence=table[properties.evidence];
      return {...feature,properties};
    })};
  }

  function createRegionLoader(options={}){
    const fetcher=options.fetch;
    if(typeof fetcher!=='function') throw new TypeError('An injected fetch function is required');
    const base=options.basePath||'';
    const makeUrl=path=>joinPath(base,path);
    function requestDisplay(regionId,path,index,layerId){
      activePath(regionId,path,'display');
      const artifact=index.artifacts.find(item=>item.path===path);
      if(!artifact) throw new Error('Display artifact is not declared in the index');
      if(layerId && artifact.layer_id!==layerId) throw new Error('Display artifact layer ID does not match its declaration');
      const url=makeUrl(path)+'?v='+String(artifact.sha256||'').slice(0,12);
      return fetcher(url);
    }
    async function fetchDisplay(regionId,path,index,layerId,responsePromise){
      const document=await parseResponse(await (responsePromise||requestDisplay(regionId,path,index,layerId)));
      if(!document || document.type!=='FeatureCollection') throw new Error('Display file is not a FeatureCollection');
      if(layerId && document.layer_id!==layerId) throw new Error('Display file layer ID does not match its declaration');
      return restoreEvidence(document);
    }
    async function loadRegion(search){
      const regionId=resolveRegionId(search,options.defaultRegion);
      const manifestPath='regions/'+regionId+'/region.json';
      let manifest;
      try{manifest=await readJson(fetcher,makeUrl(manifestPath));}
      catch(error){throw new RegionLoaderError('REGION_NOT_AVAILABLE','Region manifest could not be loaded: '+error.message);}
      if(manifest&&typeof manifest==='object')options.onManifest?.(manifest);
      if(!manifest || manifest.contract_version!==1 || manifest.region?.id!==regionId){
        throw new RegionLoaderError('REGION_NOT_AVAILABLE','Manifest does not describe the requested region');
      }
      const configPath='regions/'+regionId+'/explore.json';
      const indexPath='regions/'+regionId+'/display/index.json';
      let config,index;
      try{
        [config,index]=await Promise.all([readJson(fetcher,makeUrl(configPath)),readJson(fetcher,makeUrl(indexPath))]);
      }catch(error){throw new RegionLoaderError('REGION_NOT_AVAILABLE','Region configuration or display index could not be loaded: '+error.message);}
      if(!index || !Array.isArray(index.artifacts)) throw new RegionLoaderError('REGION_NOT_AVAILABLE','Display index is invalid');
      let entries;
      try{entries=registryApi.buildLayerRegistry(manifest,config);}catch(error){throw new RegionLoaderError('REGION_NOT_AVAILABLE',error.message);}
      const declaredPaths=new Set(index.artifacts.map(item=>item.path));
      const coveragePath=manifest.coverage?.display?.path;
      if(!coveragePath || !declaredPaths.has(coveragePath)) throw new RegionLoaderError('REGION_NOT_AVAILABLE','Coverage display artifact is missing');
      let coverage;
      try{coverage=await fetchDisplay(regionId,coveragePath,index,'coverage');}catch(error){throw new RegionLoaderError('REGION_NOT_AVAILABLE','Coverage display could not be loaded: '+error.message);}
      const places={},placeDocuments={};
      await Promise.all(manifest.layers.filter(layer=>layer.format==='place_list').map(async layer=>{
        try{
          const document=await readJson(fetcher,makeUrl(activePath(regionId,layer.path,'canonical')));
          const value=pointerGet(document,layer.pointer);
          const list=value && typeof value==='object' ? value[layer.list_key] : undefined;
          if(!Array.isArray(list)) throw new Error('Place list is missing: '+layer.list_key);
          places[layer.id]=list;
          placeDocuments[layer.id]=document;
        }catch(error){places[layer.id]={state:'failed',error:error.message};}
      }));
      let rules=null;
      if(manifest.rules?.path){
        try{rules=await readJson(fetcher,makeUrl(activePath(regionId,manifest.rules.path,'rules')));}catch{}
      }
      const state=new Map(entries.map(entry=>[entry.id,{...entry,state:'idle'}]));
      async function loadLayer(layerId,zoom,responsePromise){
        const entry=state.get(layerId);
        if(!entry) throw new Error('Unknown layer: '+layerId);
        if(entry.minZoom!==null && zoom!==undefined && Number(zoom)<entry.minZoom) return {id:layerId,state:'deferred',minZoom:entry.minZoom};
        if(entry.format!=='feature_collection' || !entry.displayPath) return {id:layerId,state:'unavailable'};
        if(entry.state==='loaded')return {id:layerId,state:'loaded',count:entry.count,data:entry.data};
        entry.state='loading';
        try{
          entry.data=await fetchDisplay(regionId,entry.displayPath,index,entry.id,responsePromise);
          if(!entry.allowNullGeometry&&entry.data.features.some(feature=>feature.geometry===null))throw new Error('Layer does not allow non-spatial records');
          entry.state='loaded';
          entry.count=entry.data.features.length;
          return {id:layerId,state:'loaded',count:entry.count,data:entry.data};
        }catch(error){
          entry.state='failed';entry.error=error;
          return {id:layerId,state:'failed',error};
        }
      }
      async function loadDefaultLayers({zoom,onState,yieldTask=()=>Promise.resolve()}={}){
        const result=[];
        const defaults=[...state.values()].filter(item=>item.defaultOn&&item.format==='feature_collection');
        // Start transport together, but leave parsing/restoration and drawing to
        // the ordered task loop. Attach rejection handlers immediately so a
        // later failure cannot become an unhandled rejection while waiting.
        const pending=new Map();
        for(const entry of defaults){
          if(entry.state==='loaded'||!entry.displayPath||
            (entry.minZoom!==null&&zoom!==undefined&&Number(zoom)<entry.minZoom))continue;
          entry.state='loading';
          try{
            pending.set(entry.id,Promise.resolve(requestDisplay(regionId,entry.displayPath,index,entry.id))
              .then(response=>({response}),error=>({error})));
          }catch(error){pending.set(entry.id,Promise.resolve({error}));}
        }
        for(const entry of defaults){
          await yieldTask();onState?.({id:entry.id,state:'loading'});
          const request=pending.get(entry.id);
          const responsePromise=request?.then(value=>{
            if(value.error)throw value.error;
            return value.response;
          });
          const loaded=await loadLayer(entry.id,zoom,responsePromise);result.push(loaded);onState?.(loaded);
        }
        return result;
      }
      return {regionId,manifest,config,index,coverage,places,placeDocuments,rules,registry:entries,layers:state,loadLayer,loadDefaultLayers};
    }
    return {loadRegion,resolveRegionId:(search)=>resolveRegionId(search,options.defaultRegion)};
  }

  const api={createRegionLoader,resolveRegionId,RegionLoaderError,REGION_ID};
  if(typeof module!=='undefined') module.exports=api;
  scope.RegionLoader=api;
})(typeof globalThis!=='undefined'?globalThis:this);
