"""Refresh independent Douglas context layers, retaining and marking failed snapshots."""
import json
from pathlib import Path
from shapely.geometry import shape
from lib.arcgis_client import query_layer_geojson
from lib.common import source, properties, clip_geometry
from lib.evidence import make_evidence, now
from lib.water import SOURCE_FIELDS, attach_legacy_ids, normalize_feature

REC = 'https://apps.fs.usda.gov/arcx/rest/services/EDW/EDW_RecInfraRecreationSites_02/MapServer'
def main():
    path=Path(__file__).resolve().parents[2]/'regions/douglas-co/research.json'
    data=json.loads(path.read_text())
    if data.get('region') != 'douglas-co':raise ValueError('Wrong region')
    boundary=shape(data['layers']['coverage']['features'][0]['geometry'])
    data['missing_layers']=['live_restrictions','precise_parcels','verified_dispersed_candidates']
    feeds=[('recreation',REC,0,{},['objectid','site_name','site_type']),
           ('land',source('land')['base_url'],1,{'native_json':True,'page_size':1},['objectid','admin_agency_code']),
           ('wilderness',source('wilderness')['base_url'],0,{},['objectid']),
           ('waterbodies',source('water')['base_url'],12,{'where':'1=1','page_size':100},['permanent_identifier','ftype','fcode']),
           ('waterways',source('water')['base_url'],6,{'where':"gnis_name IS NOT NULL AND gnis_name <> ''",'page_size':100},['permanent_identifier','ftype','fcode'])]
    for key,url,layer,options,required in feeds:
        print('Fetching '+key,flush=True)
        try:
            if key in {'waterbodies','waterways'}:
                source_layer = 'waterbody' if key == 'waterbodies' else 'flowline'
                options['out_fields'] = ','.join(sorted({name for name in SOURCE_FIELDS[source_layer].values() if name}))
            fc=query_layer_geojson(url,layer,boundary.bounds,required_fields=required,timeout=90,**options)
            rows=[];evidence=make_evidence(f'{url}/{layer}','USFS' if key in {'recreation','wilderness'} else 'BLM multi-agency' if key=='land' else 'USGS')
            for row in fc['features']:
                g=clip_geometry(row['geometry'],boundary)
                if not g:continue
                p=properties(row)
                if key in {'waterbodies','waterways'}:
                    rows.append(normalize_feature(source_layer, row, g, evidence))
                else:
                    if key=='recreation':
                        keep=['site_name','site_type','activity_type_list','seasonal_operational_status','op_status_reason','fee_description','open_season','usda_portal_url','rec1stop_url','important_info','restrictions','water_availability','restroom_availability','directions']
                        props={k:p.get(k) for k in keep};props['name']=p.get('site_name')
                    else:props={'name':p.get('gnis_name') or p.get('wildernessname') or p.get('admin_agency_code'),'manager':p.get('admin_agency_code')}
                    props.update(id=f"{key}-{p['objectid']}",evidence=evidence)
                    rows.append({'type':'Feature','geometry':g,'properties':props})
            if key in {'waterbodies','waterways'}:
                old = data['layers'].get(key, {}).get('features', [])
                rows, _, _ = attach_legacy_ids(old, rows)
            if not rows and key != 'wilderness':
                raise ValueError('Unexpected empty layer; keep previous snapshot')
            data['layers'][key]={'type':'FeatureCollection','features':rows}
            data.setdefault('source_status',{})[key]={'status':'available','retrieved_at':now(),'count':len(rows)}
            print(key+': '+str(len(rows)),flush=True)
        except Exception as error:
            previous=data.setdefault('source_status',{}).get(key,{})
            data['source_status'][key]={**previous,'status':'failed','checked_at':now(),'error':type(error).__name__,'retained_previous':key in data['layers']}
            print(key+': failed; previous data retained if present',flush=True)
        temp=path.with_suffix('.tmp');temp.write_text(json.dumps(data,allow_nan=False));temp.replace(path)
if __name__=='__main__':main()
