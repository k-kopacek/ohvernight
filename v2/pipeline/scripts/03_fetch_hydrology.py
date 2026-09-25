"""Flowlines, water areas and waterbodies, with a margin beyond the AOI."""
from shapely.geometry import box
from lib.arcgis_client import query_layer_geojson
from lib.common import source, bbox, properties, clip_geometry, write_fc
from lib.evidence import make_evidence

def main():
    src = source("water")
    # ~400m margin includes water whose setback crosses the pilot boundary.
    bounds = bbox(0.005)
    features = []
    for kind, layer in src["layers"].items():
        fc = query_layer_geojson(src["base_url"], layer, bounds, required_fields=["OBJECTID"],
                                page_size=10, timeout=45)
        evidence = make_evidence(f"{src['base_url']}/{layer}", src["agency"],
                                 "high", "arcgis_rest_query")
        for row in fc["features"]:
            p = properties(row)
            geometry = clip_geometry(row["geometry"], box(*bounds))
            if geometry:
                features.append({"type": "Feature", "geometry": geometry, "properties": {
                    "id": f"nhd-{kind}-{p['objectid']}", "kind": kind, "name": p.get("gnis_name"),
                    "evidence": evidence}})
    if not features:
        raise ValueError("Unexpectedly empty hydrology; do not generate unconstrained candidates")
    write_fc("hydrology.geojson", features)

if __name__ == "__main__":
    main()
