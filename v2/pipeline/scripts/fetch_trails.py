"""Refresh the bounded USFS trail pilot; preserve the last good file on failure."""
import json
from pathlib import Path
from lib.arcgis_client import query_layer_geojson
from lib.common import bbox, clip_geometry, properties
from lib.evidence import make_evidence, now

URL = 'https://apps.fs.usda.gov/arcx/rest/services/EDW/EDW_TrailNFSPublishWithDataStatus_01/MapServer'
ACTIVITIES = {
    'hiking': 'hiker_pedestrian', 'horseback_riding': 'pack_saddle',
    'mountain_biking': 'bicycle', 'motorcycling': 'motorcycle',
    'atv': 'atv', 'four_wheel_drive': 'fourwd',
    'snowshoeing': 'snowshoe', 'cross_country_skiing': 'xcountry_ski',
    'snowmobiling': 'snowmobile',
}

def normalize(row, evidence):
    p = properties(row)
    geometry = clip_geometry(row['geometry'])
    if not geometry or geometry['type'] not in {'LineString', 'MultiLineString'}:
        return None
    # Keep published date/rule strings verbatim. Missing is unknown, never allowed.
    activities = {activity: {suffix: p.get(f'{prefix}_{suffix}') or None
                            for suffix in ('managed', 'accpt', 'disc', 'restricted')}
                  for activity, prefix in ACTIVITIES.items()}
    return {'type': 'Feature', 'geometry': geometry, 'properties': {
        'id': f"usfs-trail-{p['objectid']}", 'name': p.get('trail_name'),
        'trail_number': p.get('trail_no'), 'surface': p.get('trail_surface'),
        'attribute_subset': p.get('attributesubset'),
        'allowed_terra_use': p.get('allowed_terra_use'),
        'activities': activities, 'evidence': evidence,
    }}

def main():
    fc = query_layer_geojson(URL, 0, bbox(), required_fields=['objectid', 'trail_name', 'trail_no'],
                            page_size=100, max_pages=20, timeout=45)
    evidence = make_evidence(URL + '/0', 'USDA Forest Service', 'high', 'arcgis_rest_query',
                             notes='Source retrieval only; current access and closures unverified.')
    features = [f for row in fc['features'] if (f := normalize(row, evidence))]
    if not features:
        raise ValueError('Empty trail pilot; previous snapshot preserved')
    target = Path(__file__).resolve().parents[2] / 'trails.geojson'
    temporary = target.with_suffix('.tmp')
    temporary.write_text(json.dumps({'type': 'FeatureCollection', 'generated_at': now(),
                                    'scope': 'Aspen pilot boundary; clipped trail segments',
                                    'features': features}, allow_nan=False))
    temporary.replace(target)
    print(f'{len(features)} trail segments written to {target.name}')

if __name__ == '__main__':
    main()
