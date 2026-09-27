"""Independent Douglas County research import. Never overwrites Aspen data."""
import json
from pathlib import Path
from shapely.geometry import shape
from lib.arcgis_client import new_session, get_json, query_layer_geojson
from lib.common import clip_geometry, properties
from lib.evidence import make_evidence, now
from fetch_trails import URL as TRAIL_URL, normalize as trail

COUNTY_URL = 'https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/State_County/MapServer/1'
ROAD_URL = 'https://apps.fs.usda.gov/arcx/rest/services/EDW/EDW_MVUM_02/MapServer'

def county_boundary(client):
    fc = get_json(client, COUNTY_URL + '/query', {
        'f': 'geojson', 'where': "STATE='08' AND NAME='Douglas County'",
        'outFields': 'GEOID,NAME,STATE', 'outSR': 4326, 'returnGeometry': 'true'}, 45)
    rows = fc.get('features', [])
    if len(rows) != 1 or rows[0]['properties'].get('GEOID') != '08035':
        raise ValueError('Expected exactly Douglas County, Colorado (08035)')
    boundary = shape(rows[0]['geometry'])
    if boundary.is_empty or not boundary.is_valid or boundary.geom_type not in {'Polygon','MultiPolygon'}:
        raise ValueError('Invalid county boundary')
    rows[0]['properties']['evidence'] = make_evidence(COUNTY_URL, 'US Census Bureau')
    return fc, boundary

def normalize_road(row, boundary, evidence):
    geometry = clip_geometry(row['geometry'], boundary)
    if not geometry or geometry['type'] not in {'LineString','MultiLineString'}:
        return None
    p = properties(row)
    return {'type':'Feature','geometry':geometry,'properties':{
        'id':f"usfs-road-{p['objectid']}", 'name':p.get('name'),
        'source_route_id':p.get('rte_cn'), 'evidence':evidence,
        'access_status':'unknown', 'camping_permission':'unknown'}}

def main():
    client = new_session()
    county, boundary = county_boundary(client)
    layers = {'coverage': county}
    print('Verified Douglas County boundary', flush=True)
    for key, url, layer_id, normalize in [('trails',TRAIL_URL,0,lambda row,e:trail(row,e,boundary)),
                                         ('roads',ROAD_URL,1,lambda row,e:normalize_road(row,boundary,e))]:
        raw = query_layer_geojson(url,layer_id,boundary.bounds,session=client,
                                 required_fields=['objectid'],page_size=100,max_pages=40,timeout=45)
        evidence = make_evidence(f'{url}/{layer_id}','USDA Forest Service','high','arcgis_rest_query',
                                 notes='Retrieved source geometry, not current access or camping approval.')
        features = [f for row in raw['features'] if (f := normalize(row,evidence))]
        if not features:
            raise ValueError(f'Empty {key}; previous county snapshot preserved')
        layers[key] = {'type':'FeatureCollection','features':features}
        print(f'{key}: {len(features)} county-clipped features',flush=True)
    payload = {'schema_version':1,'region':'douglas-co','generated_at':now(),
               'status':'research_only','layers':layers,
               'missing_layers':['camping_inventory','land_ownership','water','restrictions'],
               'notes':['USFS trails only; county and state trails not included.',
                        'County boundary clips cross-county routes; these are not full itineraries.',
                        'No camping recommendations generated.']}
    target = Path(__file__).resolve().parents[2]/'regions/douglas-co/research.json'
    target.parent.mkdir(parents=True,exist_ok=True)
    temp = target.with_suffix('.tmp')
    temp.write_text(json.dumps(payload,allow_nan=False))
    temp.replace(target)
    print('Published separate Douglas research snapshot',flush=True)

if __name__ == '__main__':
    main()
