# Curated inputs

These files are intentionally excluded from Git by default. Add only publishable, reviewed material deliberately.

## Site records: data/raw/curated_sites.geojson

Use a GeoJSON FeatureCollection of actual Point locations within the pilot. This template is illustrative, not a real reviewed campsite:

```json
{
  "type": "FeatureCollection",
  "features": [{
    "type": "Feature",
    "geometry": {"type": "Point", "coordinates": [-106.82, 39.19]},
    "properties": {
      "id": "replace-with-stable-site-id",
      "name": "Replace with actual site name",
      "site_type": "dispersed_site",
      "notes": "Describe actual site and limitations",
      "evidence": {
        "source_url": "https://replace-with-actual-agency-source.example/",
        "agency": "Actual managing agency"
      },
      "review": {
        "checked_on": "2026-09-24",
        "expires_on": "2026-10-01",
        "valid_from": "2026-09-24",
        "valid_to": "2026-10-01",
        "vehicles": ["passenger_car"],
        "sleeping_setup": "inside_vehicle",
        "actual_site_confirmed": false,
        "claims": {
          "vehicle_sleeping": {"status": "unknown", "source_url": "https://replace-with-actual-agency-source.example/"},
          "approach_access": {"status": "unknown", "source_url": "https://replace-with-actual-agency-source.example/"},
          "operating_season": {"status": "unknown", "source_url": "https://replace-with-actual-agency-source.example/"},
          "permits_and_stay_limit": {"status": "unknown", "source_url": "https://replace-with-actual-agency-source.example/"},
          "closures_checked": {"status": "unknown", "source_url": "https://replace-with-actual-agency-source.example/"}
        }
      }
    }
  }]
}
```

Replace the coordinates and URLs with actual evidence before adding a record. Each required claim must be explicitly supported by evidence covering the selected dates and setup. Do not change unknown to supported merely because a site falls inside a candidate polygon. A record with an expired review, an unsupported claim, a mismatched vehicle or an active mapped exclusion remains review-needed.

An official source listing a facility is evidence that it exists. It is not automatically evidence of winter operations, car sleeping permission, or availability. Keep those claims distinct.

## Restrictions: data/raw/restrictions.geojson

Use Polygon/MultiPolygon features with properties:

- `id`: stable order/area identifier.
- `type`: `camping_ban` or `vehicle_access_closure`.
- `effective_start`: ISO date.
- `effective_end`: ISO date, or null for an indefinite order.
- `evidence`: source_url, agency, retrieved_at (ISO timestamp), last_verified (ISO date), confidence and verification_method.

A reviewer must verify the geometry against the order exhibit. Any overlap between the restriction's effective period and the trip excludes that geometry. Unknown boundaries must not be substituted with an arbitrary bounding box; the pipeline keeps all remaining candidate areas review-needed.

## Community leads: data/raw/leads_inbox.jsonl

One object per line with `lon`, `lat`, optional `name`, `notes`, `reported_at`, and `source_url`. Reports stay unverified after spatial matching. Site IDs are based on record content to remain stable when input order changes. Avoid personal identifiers in public output.
