"""Exact matches add sourced rule context, never a camping permission grant."""
import json
from datetime import datetime, timezone
from lib.common import ROOT
from lib.evidence import freshness

def match_rules(place_id=None, road_name=None, at=None):
    registry = json.loads((ROOT / "config/rules-registry.json").read_text())
    at = at or datetime.now(timezone.utc)
    matches = []
    for rule in registry["rules"]:
        if not ((place_id and place_id in rule.get("place_ids", [])) or
                (road_name and road_name.strip().upper() in rule.get("road_names", []))):
            continue
        matches.append({**rule, "freshness": freshness(rule, at)})
    return matches
