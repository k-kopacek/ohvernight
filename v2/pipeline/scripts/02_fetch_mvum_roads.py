"""Retain MVUM vehicle-specific designations and evaluate requested dates."""
import os
from datetime import date
from lib.access import VEHICLES, SYMBOLS, evaluate_access
from lib.arcgis_client import query_layer_geojson
from lib.common import source, bbox, properties, clip_geometry, write_fc
from lib.evidence import make_evidence

def normalize(fc, src, arrive, depart, vehicle):
    features = []
    for row in fc["features"]:
        p = properties(row)
        geometry = clip_geometry(row["geometry"])
        if not geometry:
            continue
        status, reason = evaluate_access(p, arrive, depart, vehicle)
        try:
            symbol = int(p.get("symbol"))
        except (TypeError, ValueError):
            symbol = None
        designations = {v: {"designation": p.get(keys[0]), "dates_open": p.get(keys[1])}
                        for v, keys in VEHICLES.items()}
        features.append({"type": "Feature", "geometry": geometry, "properties": {
            "id": f"mvum-{p['objectid']}", "source_route_id": p.get("rte_cn"),
            "name": p.get("name"), "mvum_symbol": symbol,
            "vehicle_class": SYMBOLS.get(symbol, ("unknown", "unknown"))[0],
            "designations": designations,
            "operational_maintenance_level": p.get("operationalmaintlevel"),
            "access_status": status, "access_reason": reason,
            "evaluated_trip": {"arrive": arrive, "depart": depart, "vehicle": vehicle},
            "road_conditions": "unknown", "camping_permission": "unknown",
            "evidence": make_evidence(f"{src['base_url']}/{src['layer']}", src["agency"],
                "high", "arcgis_rest_query", notes="MVUM designation is not current passability or overnight permission.")}})
    return features

def main():
    src = source("roads")
    arrive = os.environ.get("ASPEN_ARRIVE", date.today().isoformat())
    depart = os.environ.get("ASPEN_DEPART", arrive)
    vehicle = os.environ.get("ASPEN_VEHICLE", "passenger_car")
    fields = ["objectid", "name", "symbol"] + [k for pair in VEHICLES.values() for k in pair]
    fc = query_layer_geojson(src["base_url"], src["layer"], bbox(), required_fields=fields)
    if not fc["features"]:
        raise ValueError("No MVUM road coverage returned")
    write_fc("mvum_roads.geojson", normalize(fc, src, arrive, depart, vehicle))

if __name__ == "__main__":
    main()
