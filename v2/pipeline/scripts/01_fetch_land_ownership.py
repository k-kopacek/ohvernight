"""Ownership is context, never blanket camping permission. Wilderness is explicit."""
from lib.arcgis_client import query_layer_geojson
from lib.common import source, bbox, properties, clip_geometry, write_fc
from lib.evidence import make_evidence

MANAGERS = {"USFS": "USFS", "BLM": "BLM", "NPS": "NPS", "FWS": "FWS",
            "ST": "State_CO", "PVT": "Private", "LG": "Local"}

def normalize(fc, src):
    evidence = make_evidence(f"{src['base_url']}/{src['layer']}", src["agency"],
        "high", "arcgis_rest_query", notes="Agency attribution only; limited-scale geometry, no camping permission inferred.")
    features = []
    for row in fc["features"]:
        p = properties(row)
        geometry = clip_geometry(row["geometry"])
        if not geometry:
            continue
        code = str(p.get("admin_agency_code") or "").upper()
        features.append({"type": "Feature", "geometry": geometry, "properties": {
            "id": f"sma-{p['objectid']}", "manager": MANAGERS.get(code, "Unknown"),
            "land_class": "unknown", "camping_permission": "unknown",
            "raw_admin_agency": code, "evidence": evidence}})
    return features

def main():
    src = source("land")
    fc = query_layer_geojson(src["base_url"], src["layer"], bbox(),
                            required_fields=["OBJECTID", "ADMIN_AGENCY_CODE"],
                            native_json=True, page_size=1, timeout=45)
    if not fc["features"]:
        raise ValueError("No ownership coverage returned for the pilot")
    write_fc("land_ownership.geojson", normalize(fc, src))
    src = source("wilderness")
    fc = query_layer_geojson(src["base_url"], src["layer"], bbox())
    features = []
    for row in fc["features"]:
        p = properties(row)
        geometry = clip_geometry(row["geometry"])
        if geometry:
            features.append({"type": "Feature", "geometry": geometry, "properties": {
                "id": f"wilderness-{p.get('objectid', row.get('id'))}",
                "evidence": make_evidence(f"{src['base_url']}/{src['layer']}", src["agency"],
                                         "high", "arcgis_rest_query")}})
    write_fc("wilderness.geojson", features)

if __name__ == "__main__":
    main()
