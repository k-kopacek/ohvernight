(function(scope){
  'use strict';
  const transport=(typeof require==='function'?require('./transport.js'):scope.ExploreTransport);

  class LayerRegistryError extends Error{
    constructor(message){super(message);this.name='LayerRegistryError';}
  }

  function buildLayerRegistry(manifest,config){
    if(!manifest || !Array.isArray(manifest.layers)) throw new LayerRegistryError('Manifest layers are missing');
    if(!config || !Array.isArray(config.layers)) throw new LayerRegistryError('Explore layers are missing');
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
        styleTier:layer.spatial_precision==='generalized'?'G':layer.spatial_precision==='source_published'?'P':layer.spatial_precision==='computed'?'C':'U',
        statusText:layer.status_ref?'Loading':'No retrieval status is recorded for this layer',
        freshnessText:layer.max_age_hours===null||layer.max_age_hours===undefined?'Fetched date only':`Refresh policy: ${layer.max_age_hours} hours`,
        order:Number.isFinite(item.order)?item.order:0,
        defaultOn:item.default_on===true,
        minZoom:item.min_zoom===null||item.min_zoom===undefined?null:item.min_zoom,
        format:layer.format,
        kind:layer.kind,
        displayPath:layer.display?.path||null,
        canonicalPath:layer.path,
        pointer:layer.pointer,
        sourceIds:Array.isArray(layer.source_ids)?layer.source_ids.slice():[],
        statusRef:layer.status_ref||null,
        maxAgeHours:layer.max_age_hours,
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

  const api={buildLayerRegistry,createLayerRegistry:buildLayerRegistry,LayerRegistryError,
    normalizeTransport:transport.normalizeTransport};
  if(typeof module!=='undefined') module.exports=api;
  scope.LayerRegistry=api;
})(typeof globalThis!=='undefined'?globalThis:this);
