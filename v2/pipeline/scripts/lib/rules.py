"""Exact matches add sourced rule context, never a camping permission grant."""
import json
from datetime import datetime, timezone
from lib.common import ROOT

def match_rules(place_id=None, road_name=None, at=None):
    registry = json.loads((ROOT / "config/rules-registry.json").read_text())
    at = at or datetime.now(timezone.utc)
    matches = []
    for rule in registry["rules"]:
        if not ((place_id and place_id in rule.get("place_ids", [])) or
                (road_name and road_name.strip().upper() in rule.get("road_names", []))):
            continue
        confirmed = datetime.fromisoformat(rule["last_confirmed_at"].replace("Z", "+00:00"))
        age = (at - confirmed).total_seconds() / 3600
        matches.append({**rule, "freshness": "current" if 0 <= age <= rule["max_age_hours"] else "stale"})
    return matches
