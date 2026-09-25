"""An explicit adapter for the prototype's place cards; excludes candidate geometry."""
from urllib.parse import urlparse
def build_site_feed(layers, trip):
    records = layers["reviewed_sites"]["features"] + layers["lodging_developed"]["features"]
    places = []
    seen = set()
    for row in records:
        p = row["properties"]
        if p["id"] in seen:
            raise ValueError("Duplicate site ID across curated/RIDB inventory")
        seen.add(p["id"])
        reviewed = p.get("camping_permission") == "supported_for_trip" and not p.get("needs_review", True)
        url = p.get("reservation_url") or p["evidence"]["source_url"]
        if urlparse(url).scheme not in {"http", "https"}:
            url = p["evidence"]["source_url"]
        places.append({"id": p["id"], "number": len(places)+1, "name": p["name"],
            "coordinates": row["geometry"]["coordinates"],
            "status": "reviewed" if reviewed else "review",
            "label": "Reviewed for this trip" if reviewed else "Needs trip and setup review",
            "note": "Availability is not checked. " + (p.get("notes") or "Check the source and sleeping-setup rules."),
            "source": url, "mapSource": p["evidence"]["source_url"],
            "locationBasis": "Published facility point or manually reviewed site location",
            "evidence": p["evidence"], "availability": "unknown"})
    return {"evaluated_trip": trip, "places": places,
            "integration_note": "Merge these places into the existing map model; preserve resorts/roads/waterways. Reevaluate when trip dates or vehicle change."}
