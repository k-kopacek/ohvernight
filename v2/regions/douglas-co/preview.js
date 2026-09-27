(async()=>{
 const status=document.getElementById('status');
 try{
  const response=await fetch('./research.json',{cache:'no-store'});if(!response.ok)throw Error('Missing research data');
  const data=await response.json();if(data.region!=='douglas-co'||data.schema_version!==1)throw Error('Unsupported research data');
  const map=L.map('map',{preferCanvas:true});
  L.tileLayer('https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}',{maxNativeZoom:16,maxZoom:19,attribution:'Imagery: USGS The National Map'}).addTo(map);
  const boundary=L.geoJSON(data.layers.coverage,{style:{color:'white',weight:2,fill:false},interactive:false}).addTo(map);map.fitBounds(boundary.getBounds(),{padding:[20,20]});
  for(const [id,color] of [['roads','#ead294'],['trails','#f6a9ed']]){
   const layer=L.geoJSON(data.layers[id],{style:{color,weight:3},onEachFeature:(f,l)=>{
    const p=f.properties,box=document.createElement('div'),title=document.createElement('strong');title.textContent=p.name||'Unnamed '+(id==='roads'?'road':'trail');box.append(title);
    const note=document.createElement('p');note.textContent='Mapped segment only. Current access, conditions and camping permission are unconfirmed.';box.append(note);
    const link=document.createElement('a');link.textContent='Official source ↗';link.target='_blank';link.rel='noopener noreferrer';
    try{const url=new URL(p.evidence.source_url);if(url.protocol==='https:'){link.href=url.href;box.append(link);}}catch{}
    l.bindPopup(box);
   }}).addTo(map);
   document.getElementById(id).onchange=event=>event.target.checked?layer.addTo(map):map.removeLayer(layer);
  }
  status.textContent=`${data.layers.trails.features.length} trail segments · ${data.layers.roads.features.length} road segments · fetched ${data.generated_at.slice(0,10)}`;
 }catch{status.textContent='Douglas research data could not load. Reload the page; Aspen remains available.';for(const id of ['roads','trails'])document.getElementById(id).disabled=true;}
})();
