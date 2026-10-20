"""Import curated site records. Require evidence for the full trip and sleeping setup."""
import datetime as dt
import json
import os
from urllib.parse import urlparse
from shapely.geometry import Point, shape
from lib.common import raw_dir, read_fc, aoi, write_fc
from lib.evidence import now

CLAIMS = ("vehicle_sleeping", "approach_access", "operating_season", "permits_and_stay_limit", "closures_checked")

def normalize(records, arrive, depart, vehicle, today=None, restrictions=()):
    today = today or dt.date.today()
    first, last = dt.date.fromisoformat(arrive), dt.date.fromisoformat(depart)
    out = []
    for row in records:
        p = row["properties"]
        if row["geometry"]["type"] != "Point" or not aoi().covers(shape(row["geometry"])):
            raise ValueError("Curated site must be a point inside the pilot")
        if not p.get("id") or not p.get("name"):
            raise ValueError("Curated site requires a stable ID and name")
        review = p["review"]
        checked = dt.date.fromisoformat(review["checked_on"])
        expires = dt.date.fromisoformat(review["expires_on"])
        if checked > today or expires < checked:
            raise ValueError("Invalid review dates")
        valid_start = dt.date.fromisoformat(review["valid_from"])
        valid_end = dt.date.fromisoformat(review["valid_to"])
        if valid_end < valid_start:
            raise ValueError("Invalid reviewed operating dates")
        claims = review.get("claims", {})
        complete = all(claims.get(c, {}).get("status") == "supported" for c in CLAIMS)
        for claim in claims.values():
            url = urlparse(claim.get("source_url", ""))
            if url.scheme not in {"https", "http"} or not url.netloc:
                raise ValueError("Each reviewed claim requires an actual source URL")
        reasons = []
        if not complete: reasons.append("required_claims_not_supported")
        if not (checked <= today <= expires) or (today-checked).days > 30: reasons.append("review_stale")
        if not (valid_start <= first <= last <= valid_end): reasons.append("dates_outside_review")
        if vehicle not in review.get("vehicles", []): reasons.append("vehicle_not_reviewed")
        if review.get("sleeping_setup") != "inside_vehicle": reasons.append("sleeping_setup_not_reviewed")
        if review.get("actual_site_confirmed") is not True: reasons.append("actual_site_unconfirmed")
        if any(shape(row["geometry"]).intersects(g) for g in restrictions): reasons.append("active_mapped_restriction")
        ev = p["evidence"]
        if not ev.get("agency") or urlparse(ev.get("source_url","")).scheme not in {"https","http"}:
            raise ValueError("Site evidence must identify the source and agency")
        copied = dict(p)
        copied.update({"site_type": p.get("site_type", "curated_overnight_site"),
                       "needs_review": bool(reasons), "review_reasons": reasons,
                       "camping_permission": "supported_for_trip" if not reasons else "unknown",
                       "availability": "unknown", "evaluated_trip": {
                           "arrive": arrive, "depart": depart, "vehicle": vehicle},
                       "evidence": {**ev, "retrieved_at": now(), "last_verified": checked.isoformat(),
                                    "confidence": "medium" if not reasons else "unverified",
                                    "verification_method": "manual_claim_review"}})
        out.append({"type": "Feature", "geometry": row["geometry"], "properties": copied})
    return out

def main():
    path = raw_dir() / "curated_sites.geojson"
    records = json.loads(path.read_text())["features"] if path.exists() else []
    arrive = os.environ.get("ASPEN_ARRIVE", dt.date.today().isoformat())
    depart = os.environ.get("ASPEN_DEPART", arrive)
    vehicle = os.environ.get("ASPEN_VEHICLE", "passenger_car")
    from importlib import import_module
    restrictions, _ = import_module("07_build_dispersed_corridors").manual_exclusions(arrive, depart)
    # Explicit wilderness exclusion also applies to vehicle-sleeping site records.
    restrictions += [shape(f["geometry"]) for f in read_fc("wilderness.geojson")["features"]]
    write_fc("reviewed_sites.geojson", normalize(records, arrive, depart, vehicle, restrictions=restrictions))

if __name__ == "__main__":
    main()
