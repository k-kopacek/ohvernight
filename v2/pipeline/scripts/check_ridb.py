"""Independent credential check and atomic campground export. Never logs API keys."""
import argparse
import importlib
import json
import os
from pathlib import Path
import sys
import tempfile
from urllib.parse import urlparse, quote

import requests
from lib.arcgis_client import new_session
from lib.common import ROOT, source
from lib.evidence import now

ridb = importlib.import_module("04_fetch_campgrounds_ridb")

def safe_url(value):
    if not isinstance(value, str):
        return None
    parsed = urlparse(value)
    return value if parsed.scheme == "https" and parsed.hostname and not parsed.username and not parsed.password else None

def export(destination, client=None):
    features = ridb.normalize(ridb.fetch_facilities(client))
    if not features:
        raise ValueError("RIDB authenticated, but no facilities survived the Aspen coverage filter")
    checked = now()
    places = []
    for feature in features:
        p = feature["properties"]
        booking = safe_url(p.get("reservation_url"))
        places.append({"id": p["id"], "ridb_facility_id": p["id"].removeprefix("ridb-"),
            "name": p["name"], "kind": "campground", "number": "C",
            "coordinates": feature["geometry"]["coordinates"], "checked_on": checked[:10],
            "source": booking or "https://www.recreation.gov/search?q=" + quote(p["name"]),
            "source_is_search": not bool(booking), "mapSource": p["evidence"]["source_url"],
            "locationBasis": "RIDB facility coordinate; not an individual campsite",
            "note": "Official camping inventory. Site type, vehicle sleeping and operating dates need review.",
            "unknowns": ["Suitable individual site and vehicle sleeping permission", "Full approach and current restrictions", "Availability, price and operating dates"],
            "camping_permission": "unknown", "needs_review": True,
            "facts": {name: {"status": "unknown"} for name in ("ownership", "road_access", "camping_permission", "restrictions", "stay_limit", "seasonality")},
            "evidence": p["evidence"]})
    payload = {"schema_version": 1, "generated_at": checked,
        "source_status": {"status": "available", "last_checked_at": checked,
            "last_confirmed_at": checked, "max_age_hours": 168,
            "scope": "Facility inventory only; no availability or restriction confirmation"},
        "places": places}
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    # Replace only after a complete validated fetch; failed calls preserve old data.
    with tempfile.NamedTemporaryFile(mode="w", dir=destination.parent, delete=False) as handle:
        staged = Path(handle.name)
        json.dump(payload, handle, allow_nan=False, separators=(",", ":"))
    try:
        os.replace(staged, destination)
    finally:
        staged.unlink(missing_ok=True)
    return len(places)

def smoke(client=None):
    key = os.environ.get("RIDB_API_KEY", "").strip()
    if not key:
        raise ridb.MissingCredentials("Set the Actions repository secret RIDB_API_KEY")
    response = (client or new_session()).get(source("ridb")["base_url"] + "/facilities",
        headers={"apikey": key}, params={"limit": 1}, timeout=30)
    response.raise_for_status()
    payload = response.json()
    if not isinstance(payload, dict) or not isinstance(payload.get("RECDATA"), list) or not isinstance(payload.get("METADATA"), dict):
        raise ValueError("RIDB response schema was unexpected")

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--smoke-only", action="store_true")
    parser.add_argument("--output", type=Path, default=ROOT.parent / "ridb-options.json")
    args = parser.parse_args()
    try:
        smoke()
        print("PASS: RIDB accepted the configured API key.")
        if not args.smoke_only:
            print(f"PASS: exported {export(args.output)} Aspen-area facilities to {args.output.name}.")
    except ridb.MissingCredentials:
        print("FAIL: RIDB_API_KEY is missing. Add it under repository Settings > Secrets and variables > Actions.")
        return 2
    except requests.HTTPError as exc:
        status = exc.response.status_code if exc.response is not None else None
        print("FAIL: RIDB rejected access (401/403). Check or replace RIDB_API_KEY." if status in (401,403)
              else f"FAIL: RIDB returned HTTP {status}. Previous inventory preserved.")
        return 3
    except (requests.RequestException, ValueError, KeyError, TypeError):
        print("FAIL: RIDB request or data validation failed. Previous inventory preserved; check service status and coverage.")
        return 4
    return 0

if __name__ == "__main__":
    sys.exit(main())
