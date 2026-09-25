# Aspen overnight data pipeline

A research-data pipeline for the Aspen Snowmass overnight planner. It retrieves ownership context, wilderness boundaries, vehicle-specific MVUM designations, and hydrology; produces candidate research areas; and keeps actual lodging inventory separate from generated geometry.

**No generated area or community report is treated as an approved campsite.** Road designation is not winter passability, permission to sleep, or availability.

## Run locally

Use Python 3.12 or later. From this directory:

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python scripts/00_selftest.py
.venv/bin/python scripts/run_pipeline.py --arrive 2027-01-15 --depart 2027-01-17 --vehicle passenger_car
```

Vehicle options: `passenger_car`, `high_clearance`, `motorhome`. Both arrival and departure are included in access checks, so the approach must remain designated for exit day too. A road may be designated open while physical conditions remain unknown. Unsupported or missing vehicle/season fields remain unknown.

Use `--skip-slow-sources` to skip optional RIDB, wildlife, and fire inputs while testing the required spatial pipeline. Every run records which sources were available, skipped, or unavailable.

To ingest developed camping inventory, provide `RIDB_API_KEY` in your environment or a GitHub repository secret. Do not put credentials in source files. Without a key, RIDB is recorded as unavailable and its layer is empty; required spatial ingestion can still complete.

## Outputs and publication

One output is published locally: `data/processed/map-data-v2.json`. It contains:

- `trip`: the dates and vehicle actually evaluated.
- `source_status`: explicit per-step retrieval outcomes.
- `layers.land_ownership`: limited-scale agency context, with camping permission unknown.
- `layers.wilderness`: explicit geometry excluded from vehicle-camping research areas.
- `layers.mvum_roads`: original vehicle-specific designation windows plus trip evaluation.
- `layers.hydrology`: flowlines, areas, and waterbodies.
- `layers.dispersed_corridors`: candidate research polygons, always requiring review.
- `layers.dispersed_corridor_points`: always empty; synthetic road-centerline campsite pins were retired.
- `layers.lodging_developed`: RIDB camping facilities, pending setup/date review.
- `layers.reviewed_sites`: actual manually curated sites with claim-specific evidence.
- `layers.leads`: community reports, always unverified even if inside a candidate.
- `site_feed.places`: an adapter for map cards, containing only actual curated sites and RIDB inventory.
- `coverage_gaps`: known limits that a consumer must keep visible.

Each run uses a clean staging directory. Failure of a required source or validation leaves the previous bundle untouched. Optional failure produces an explicit unavailable status and an empty layer, never an old layer relabeled as fresh. Only a validated complete envelope atomically replaces the public bundle. `generated_at` is a processing timestamp; source retrieval and manual verification have separate timestamps.

The existing website still reads its embedded map data. This pipeline does not deploy or modify it. A future integration must load this bundle, preserve its source-status warnings, and reevaluate access if the traveler changes dates or vehicle. The `site_feed` adapter preserves the place-card fields but does not itself implement the site's loader or reviewed-state styling.

## Actual dispersed sites

Put reviewed site records in `data/raw/curated_sites.geojson`; see [the input guide](docs/curation.md). An absent file means no curated sites, not an error or fabricated inventory.

To receive `supported_for_trip`, a site requires an actual location, evidence for vehicle sleeping, approach access, operating season, permits/stay limits and checked closures, the right vehicle/setup, and review/date validity. Records that fail those checks remain review-needed. Mapped applicable camping/vehicle closures and wilderness also block that status.

Review evidence must be rechecked within 30 days and before its stated expiry. Support is an as-of assessment, not a guarantee of future conditions or availability.

Community reports go in `data/raw/leads_inbox.jsonl`. They are research leads, not reviewed sites. Do not scrape or republish another service's content without appropriate rights. Keep personal contact details out of inputs intended for publication.

## Restrictions and source limitations

- Supply reviewed, dated exclusion polygons in `data/raw/restrictions.geojson` (see input guide). They are applied across the whole trip, including restrictions scheduled to begin during it.
- The Aspen-Sopris occupancy order still needs reliable boundaries and effective-date review. All generated areas require review regardless of location; there is no town-box shortcut.
- Ownership is limited-scale context. It is not parcel-level clearance, and BLM land does not inherit Forest Service camping rules.
- The old CPW service returned a 404 on September 24, 2026. Its adapter is explicitly unavailable until a replacement is checked. Wildlife habitat should never be labeled as an active legal closure by itself.
- The fire monitor only detects source-page changes. It leaves stage/status unknown. Review current dated notices and their jurisdictions; an old Stage 2 headline must not become today's restriction.
- Forest camping guidance and local orders in `config/legal_rules.yaml` are a review queue, not encoded permissions. Screening distances are conservative research parameters, not legal conclusions.
- No routing engine, live booking availability, snow feed, or site-level vehicle suitability is implemented.

## Source and geometry checks

Services and layer IDs are centralized in `config/sources.yaml`. Adapters validate required fields before fetching. ArcGIS retrieval compares record counts with object IDs when count queries work, splits transfer-limited batches, rejects incomplete results, and checks the full ID set again after downloading. If the count request fails, the complete ID list and every downloaded feature are still checked. Transient HTTP errors and ArcGIS errors inside HTTP 200 responses receive bounded retries. Geometry retains the source's coordinate precision and is clipped to the pilot; nearby water beyond the pilot boundary is retained for setback calculations.

The September 24, 2026 live check retrieved 28 MVUM road segments for January 15–17, 2027: 26 restricted for passenger cars and two designated open, with physical conditions still unknown. BLM's ownership service returned intermittent query errors and repeatedly failed the required geometry download, so the end-to-end run correctly stopped without publishing a partial bundle. An independent USGS hydrology check also exhausted retries with HTTP 504 responses. Passing offline tests does not mean these external service issues are resolved. See [verification results](docs/verification.md).

Distances use NAD83 / UTM zone 13N in meters, with an explicit 0.3048 conversion from feet. Tests independently measure buffer radii with geodesic distances. The old EPSG:26953/feet mismatch is removed.

The root JSON schema describes the actual envelope and GeoJSON features. Additional checks reject invalid geometry, missing evidence, duplicate IDs, synthetic campsite pins, and generated areas marked approved.

## GitHub workflow

Pull requests and pushes run the offline regression suite. Live refresh is **manual** through Actions, with explicit dates and vehicle. A completed refresh commits only the public bundle; private/raw inputs are ignored. It does not automatically deploy the website. Keep automated scheduled refresh disabled until source coverage and the reviewed inventory are sufficient.

The original pipeline was backed up in the Codex workspace before this revision. No real reviewed sites were invented to populate the map.
