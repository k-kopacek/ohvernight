"""Community reports remain unverified even when they intersect a candidate area."""
import hashlib
import json
import math
from shapely.geometry import Point, shape
from lib.common import raw_dir, read_fc, write_fc
from lib.evidence import make_evidence

def normalize(leads, corridors):
    out, seen = [], set()
    for lead in leads:
        lon, lat = float(lead["lon"]), float(lead["lat"])
        if not math.isfinite(lon) or not math.isfinite(lat) or not (-180 <= lon <= 180 and -90 <= lat <= 90):
            raise ValueError("Invalid lead coordinates")
        point = Point(lon, lat)
        matches = sorted(c["properties"]["id"] for c in corridors if shape(c["geometry"]).covers(point))
        ident = "lead-" + hashlib.sha256(json.dumps(lead, sort_keys=True).encode()).hexdigest()[:16]
        if ident in seen:
            continue
        seen.add(ident)
        out.append({"type": "Feature", "geometry": {"type": "Point", "coordinates": [lon, lat]},
            "properties": {"id": ident, "site_type": "dispersed_lead_unverified",
                "name": lead.get("name"), "notes": lead.get("notes"),
                "matched_candidate_ids": matches, "needs_review": True, "camping_permission": "unknown",
                "evidence": make_evidence(lead.get("source_url") or "https://github.com/k-kopacek/aspen-overnight",
                    lead.get("reported_by") or "Community", "unverified", "community_report",
                    reported_at=lead.get("reported_at"), notes="Spatial match is not corroboration of legal access.")}})
    return out

def main():
    path = raw_dir() / "leads_inbox.jsonl"
    leads = [json.loads(line) for line in path.read_text().splitlines() if line.strip()] if path.exists() else []
    write_fc("leads.geojson", normalize(leads, read_fc("dispersed_corridors.geojson")["features"]))

if __name__ == "__main__":
    main()
