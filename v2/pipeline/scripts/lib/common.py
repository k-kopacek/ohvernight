import json
import os
from pathlib import Path
from shapely.geometry import shape, mapping
from shapely import make_valid
import yaml
ROOT = Path(__file__).resolve().parents[2]

def source(source_id):
    return yaml.safe_load((ROOT / "config/sources.yaml").read_text())["sources"][source_id]

def output_dir():
    return Path(os.environ.get("ASPEN_OUTPUT_DIR", ROOT / "data/processed"))

def raw_dir():
    return ROOT / "data/raw"

def aoi():
    return shape(json.loads((ROOT / "config/aoi.geojson").read_text())["geometry"])

def bbox(padding=0):
    x1, y1, x2, y2 = aoi().bounds
    return x1-padding, y1-padding, x2+padding, y2+padding

def properties(feature):
    return {k.lower(): v for k, v in feature["properties"].items()}

def clip_geometry(geometry, boundary=None):
    geom = make_valid(shape(geometry)).intersection(boundary if boundary is not None else aoi())
    return None if geom.is_empty else mapping(geom)

def write_fc(filename, features):
    directory = output_dir()
    directory.mkdir(parents=True, exist_ok=True)
    (directory / filename).write_text(json.dumps({"type": "FeatureCollection", "features": features}, allow_nan=False))
    print(f"{filename}: {len(features)} features")

def read_fc(filename):
    return json.loads((output_dir() / filename).read_text())
