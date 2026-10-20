"""Flowlines, water areas and waterbodies, with a margin beyond the AOI."""
import json
from pathlib import Path
from shapely.geometry import box
from lib.arcgis_client import query_layer_geojson
from lib.common import source, bbox, clip_geometry, write_fc
from lib.evidence import make_evidence
from lib.water import SOURCE_FIELDS, attach_legacy_ids, normalize_feature

def main():
    src = source("water")
    # ~400m margin includes water whose setback crosses the pilot boundary.
    bounds = bbox(0.005)
    previous_path = Path(__file__).resolve().parents[2] / "map-data-v2.json"
    previous = json.loads(previous_path.read_text())["layers"]["hydrology"]["features"]
    features = []
    for kind, layer in src["layers"].items():
        fields = sorted({name for name in SOURCE_FIELDS[kind].values() if name})
        fc = query_layer_geojson(src["base_url"], layer, bounds,
                                out_fields=",".join(fields), required_fields=["permanent_identifier", "ftype", "fcode"],
                                page_size=100, timeout=90)
        evidence = make_evidence(f"{src['base_url']}/{layer}", src["agency"],
                                 "high", "arcgis_rest_query")
        layer_features = []
        for row in fc["features"]:
            geometry = clip_geometry(row["geometry"], box(*bounds))
            if geometry:
                layer_features.append(normalize_feature(kind, row, geometry, evidence, aspen=True))
        old_layer = [feature for feature in previous
                     if (feature.get("properties") or {}).get("kind") == kind]
        layer_features, _, _ = attach_legacy_ids(old_layer, layer_features)
        features.extend(layer_features)
    if not features:
        raise ValueError("Unexpectedly empty hydrology; do not generate unconstrained candidates")
    write_fc("hydrology.geojson", features)

if __name__ == "__main__":
    main()
