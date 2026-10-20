"""Validate the actual output envelope and geometry before publication."""
import json
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker
from shapely.geometry import shape
from lib.common import ROOT

def validate_bundle(bundle):
    schema = json.loads((ROOT / "schema/schema.json").read_text())
    Draft202012Validator(schema, format_checker=FormatChecker()).validate(bundle)
    for name, layer in bundle["layers"].items():
        ids = set()
        for feature in layer["features"]:
            p = feature["properties"]
            if p["id"] in ids:
                raise ValueError(f"Duplicate ID in {name}: {p['id']}")
            ids.add(p["id"])
            geometry = feature["geometry"]
            if geometry is None:
                if name != "fire_restriction_stage":
                    raise ValueError(f"Unexpected null geometry in {name}")
                continue
            geom = shape(geometry)
            if not geom.is_valid or geom.is_empty:
                raise ValueError(f"Invalid/empty geometry in {name}")
            x1,y1,x2,y2 = geom.bounds
            if not (-180 <= x1 <= x2 <= 180 and -90 <= y1 <= y2 <= 90):
                raise ValueError("Geometry outside WGS84 range")
            if name == "dispersed_corridors":
                if p.get("needs_review") is not True or p.get("camping_permission") != "unknown":
                    raise ValueError("Generated candidate must never be approved")
    if bundle["layers"]["dispersed_corridor_points"]["features"]:
        raise ValueError("Synthetic campsite pins are prohibited")
    site_ids = {f["properties"]["id"] for name in ("reviewed_sites", "lodging_developed")
                for f in bundle["layers"][name]["features"]}
    if any(p["id"] not in site_ids for p in bundle["site_feed"]["places"]):
        raise ValueError("Site feed contains a generated or unverified community pin")
