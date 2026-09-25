"""RIDB inventory needs a key; inventory never implies winter availability."""
import os
import math
from shapely.geometry import Point
from lib.arcgis_client import new_session
from lib.common import source, aoi, write_fc
from lib.evidence import make_evidence

class MissingCredentials(RuntimeError):
    pass

def fetch_facilities(client=None):
    key = os.environ.get("RIDB_API_KEY")
    if not key:
        raise MissingCredentials("RIDB_API_KEY is not configured; developed inventory unavailable")
    src = source("ridb")
    client = client or new_session()
    center = aoi().centroid
    results, seen, offset, expected_total = [], set(), 0, None
    for _ in range(100):
        response = client.get(src["base_url"] + "/facilities", headers={"apikey": key},
            params={"latitude": center.y, "longitude": center.x, "radius": 35,
                    "activity": 9, "limit": 50, "offset": offset, "full": "true"}, timeout=30)
        response.raise_for_status()
        payload = response.json()
        if "RECDATA" not in payload or "METADATA" not in payload:
            raise ValueError("RIDB returned an unexpected schema")
        batch = payload["RECDATA"]
        total = payload["METADATA"].get("RESULTS", {}).get("TOTAL_COUNT")
        if type(total) is not int or total < 0 or not isinstance(batch, list):
            raise ValueError("RIDB total count missing")
        if expected_total is not None and total != expected_total:
            raise ValueError("RIDB count changed during download")
        expected_total = total
        for row in batch:
            ident = str(row["FacilityID"])
            if ident in seen:
                raise ValueError("RIDB pagination repeated a facility")
            seen.add(ident)
        results.extend(batch)
        offset += len(batch)
        if offset >= total:
            if offset != total:
                raise ValueError("RIDB count changed during download")
            return results
        if not batch:
            raise ValueError("RIDB pagination ended before total count")
    raise ValueError("RIDB pagination limit reached")

def normalize(facilities):
    features = []
    bounds = aoi()
    for fac in facilities:
        try:
            lat, lon = float(fac["FacilityLatitude"]), float(fac["FacilityLongitude"])
        except (KeyError, TypeError, ValueError):
            continue
        if not all(map(math.isfinite, (lat, lon))) or not bounds.covers(Point(lon, lat)):
            continue
        # RIDB activity filtering supplies camping inventory; FacilityTypeDescription
        # is often generic and is not a reliable cabin/campground classifier.
        ident = str(fac["FacilityID"])
        url = f"https://ridb.recreation.gov/api/v1/facilities/{ident}"
        features.append({"type": "Feature", "geometry": {"type": "Point", "coordinates": [lon, lat]},
            "properties": {"id": f"ridb-{ident}", "name": fac.get("FacilityName") or "Unnamed RIDB facility",
                "site_type": "camping_facility_unreviewed", "ridb_facility_type": fac.get("FacilityTypeDescription"),
                "reservable": fac.get("Reservable") if isinstance(fac.get("Reservable"), bool) else None,
                "reservation_url": fac.get("FacilityReservationURL") or None,
                "camping_permission": "unknown", "winter_access": "unknown", "availability": "unknown",
                "needs_review": True,
                "evidence": make_evidence(url, "Recreation.gov / RIDB", "high", "rest_api",
                    notes="Published camping inventory; site type, sleeping setup and trip availability require review.")}})
    return features

def main():
    write_fc("lodging_developed.geojson", normalize(fetch_facilities()))

if __name__ == "__main__":
    main()
