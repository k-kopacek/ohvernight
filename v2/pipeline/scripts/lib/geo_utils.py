"""Local metric geometry; feet are explicitly converted before buffering."""
import pyproj
from shapely.geometry import shape, mapping
from shapely.ops import transform, unary_union
WGS84 = "EPSG:4326"
LOCAL_METRIC = "EPSG:26913"  # NAD83 / UTM zone 13N
FOOT_METERS = 0.3048
assert pyproj.CRS(LOCAL_METRIC).axis_info[0].unit_name == "metre"
_forward = pyproj.Transformer.from_crs(WGS84, LOCAL_METRIC, always_xy=True).transform
_inverse = pyproj.Transformer.from_crs(LOCAL_METRIC, WGS84, always_xy=True).transform

def to_local(geom):
    return transform(_forward, geom)

def to_wgs84(geom):
    return transform(_inverse, geom)

def buffer_feet(geom, feet):
    if feet < 0:
        raise ValueError("Buffer distance must be nonnegative")
    return to_wgs84(to_local(geom).buffer(feet * FOOT_METERS))

def geojson_features_to_union(features):
    return unary_union([shape(f["geometry"]) for f in features if f.get("geometry")])

def geom_to_geojson(geom):
    return mapping(geom)
