"""Generate candidate research areas, never synthetic campsite pins."""
import json
import os
import datetime as dt
import yaml
from shapely.geometry import shape, mapping, Polygon, MultiPolygon, GeometryCollection
from shapely.ops import unary_union
from shapely import make_valid
from lib.common import ROOT, read_fc, raw_dir, write_fc
from lib.geo_utils import buffer_feet
from lib.evidence import derived_evidence
from lib.rules import match_rules

def polygon_only(geometry):
    if isinstance(geometry, (Polygon, MultiPolygon)):
        return geometry
    return unary_union([polygon_only(g) for g in geometry.geoms
                        if isinstance(g, (Polygon, MultiPolygon, GeometryCollection))]) if hasattr(geometry, "geoms") else Polygon()

def manual_exclusions(arrive, depart):
    path = raw_dir() / "restrictions.geojson"
    if not path.exists():
        return [], ["site_specific_orders_not_completely_mapped"]
    records = json.loads(path.read_text())
    areas, evidence = [], []
    start, end = dt.date.fromisoformat(arrive), dt.date.fromisoformat(depart)
    for row in records["features"]:
        p = row["properties"]
        first = dt.date.fromisoformat(p["effective_start"])
        last = dt.date.fromisoformat(p["effective_end"]) if p.get("effective_end") else dt.date.max
        if last < first:
            raise ValueError("Restriction has reversed effective dates")
        if p["type"] not in {"camping_ban", "vehicle_access_closure"}:
            continue
        if first <= end and last >= start:
            if not row.get("geometry") or not p.get("evidence"):
                raise ValueError("Applicable restriction is missing geometry/evidence")
            geom = make_valid(shape(row["geometry"]))
            if geom.geom_type not in {"Polygon", "MultiPolygon"}:
                raise ValueError("Restriction needs polygon geometry")
            areas.append(geom)
            evidence.append(p["evidence"])
    return areas, evidence

def build(land, roads, water, wilderness, rules, restrictions=(), restriction_evidence=()):
    if not land["features"] or not roads["features"] or not water["features"]:
        raise ValueError("Required spatial coverage is empty")
    possible = unary_union([make_valid(shape(f["geometry"])) for f in land["features"]
                            if f["properties"]["manager"] in {"USFS", "BLM"}])
    wild = unary_union([make_valid(shape(f["geometry"])) for f in wilderness["features"]])
    wet = unary_union([buffer_feet(make_valid(shape(f["geometry"])), rules["water_setback_ft"])
                       for f in water["features"]])
    exclusion = unary_union([wild, wet, *restrictions])
    out = []
    for road in roads["features"]:
        p = road["properties"]
        if p["access_status"] != "designated_open":
            continue
        buffered = buffer_feet(shape(road["geometry"]), rules["road_buffer_ft"])
        candidate = polygon_only(make_valid(buffered.intersection(possible).difference(exclusion)))
        if candidate.is_empty:
            continue
        inputs = [p["evidence"], *restriction_evidence]
        for layer in (land, water, wilderness):
            # Preserve source URLs/timestamps without duplicating every record's evidence.
            unique = {json.dumps(f["properties"]["evidence"], sort_keys=True): f["properties"]["evidence"]
                      for f in layer["features"]}
            inputs.extend(unique.values())
        out.append({"type": "Feature", "geometry": mapping(candidate), "properties": {
            "id": f"candidate-{p['id']}", "site_type": "candidate_area",
            "source_road_id": p["id"], "name": p.get("name"),
            "applicable_rule_context": match_rules(road_name=p.get("name")),
            "needs_review": True, "camping_permission": "unknown", "actual_site_confirmed": False,
            "evaluated_trip": p["evaluated_trip"], "required_checks": rules["required_checks"],
            "evidence": derived_evidence(inputs,
                "Metric road screening buffer intersected with limited-scale USFS/BLM context; "
                "water, wilderness and supplied effective restrictions removed. "
                "Orders coverage remains incomplete. No campsite existence or legal permission inferred.")}})
    return out

def main():
    rules = yaml.safe_load((ROOT / "config/legal_rules.yaml").read_text())["screening"]
    arrive = os.environ.get("ASPEN_ARRIVE", dt.date.today().isoformat())
    depart = os.environ.get("ASPEN_DEPART", arrive)
    areas, evidence = manual_exclusions(arrive, depart)
    # String missing-coverage notes are not evidence objects.
    records = build(read_fc("land_ownership.geojson"), read_fc("mvum_roads.geojson"),
                    read_fc("hydrology.geojson"), read_fc("wilderness.geojson"), rules,
                    areas, [e for e in evidence if isinstance(e, dict)])
    write_fc("dispersed_corridors.geojson", records)
    write_fc("dispersed_corridor_points.geojson", [])  # Explicitly retire synthetic pins.

if __name__ == "__main__":
    main()
