# Douglas County field-test edition — September 27, 2026

## Publish this package

Unzip the release. Replace the repository's existing **v2** folder with the included **v2** folder, preserving its structure. Do not put it inside another v2 folder. This includes the website, data, vendor files, and pipeline source. Commit the upload and allow GitHub Pages to finish deploying.

Open `/ohvernight/v2/regions/douglas-co/` on your GitHub Pages site, or use **Explore Douglas County dirt biking & camping** on the v2 landing page. Refresh if an older page appears. The local folder must be served over HTTP; opening index.html directly from Files will not load the data reliably.

## Test with your phone

1. Open **Find trails & camping**. Dirt biking is selected by default. Enter your actual dates and search **674** or **Flatrock**.
2. Open a result. Read its source dates and official source link. An amber badge is a research status, not an open/closed verdict. Some source records have surprising winter-only dates; compare these with the current official motor-vehicle map before travel.
3. Inspect nearby campgrounds and trailheads. Distances are straight-line proximity to a segment, not riding distance or a verified connection. Check campground restrictions—an unlicensed dirt bike cannot automatically be ridden through a campground.
4. Save a trail and campground. Close details to see the selected location highlighted on the map. Reload and check **Saved plan**.
5. Use **Layers** to toggle land, roads, trails, water, campgrounds and trailheads. Everything starts enabled. Search, activity, dates and vehicle do not hide map features. Switching activity changes trail lists and nearby-trail suggestions.
6. Try **Download segment GPX**. It contains source geometry clipped at the county boundary; use it as a research reference, not a verified itinerary. Background maps and research UI are not offline-enabled.
7. Record incorrect signs, missing trails, confusing details and usability issues under **Saved plan → Field-test notes**. Download the plan and feedback to share it back. Notes are stored only in that browser; they are not sent to a server.

## What is included

- 102 USFS trail segments, with 76 carrying positive managed/accepted motorcycle-use fields. These are not 76 confirmed open trails; multiple segments can share a trail number.
- 73 USFS motor-vehicle-road geometries. Road-specific vehicle/season permissions are not evaluated in this release.
- Five general campgrounds and 17 trailheads from official USFS recreation inventory. The equestrian campground is excluded from general camping suggestions.
- A linked Rampart designated dispersed-camping area listing. Individual numbered campsites are not mapped and cannot be routed to from this dataset.
- Five broad land-management polygons, 33 named waterbody features and 2,359 named stream features. These are feature counts, not unique named places. Wilderness query returned no intersecting features.
- Satellite/street basemaps, layer legend, prominent source links, trail-season comparison, nearby facilities, saved research, feedback download and GPX segment export.
- Existing Aspen v2 features and pipeline remain included.

## What is not ready

This is ready for product/usability testing, not a complete county access or navigation service. Live fire/wildlife closures and special orders are unconfirmed; official alert links are provided. Precise private parcels, county/state trail inventories, full cross-county routes, generated legal dispersed sites, live campsite availability, verified bike/trailer suitability, difficulty, and turn-by-turn navigation remain outstanding. Camping dates/stay limits are not comprehensively evaluated in this county edition. Choosing a camping vehicle currently records your preference; it does not validate fit.

Public land, nearby roads and water setbacks do not grant camping permission. The land layer is limited-scale management context, not a surveyed property boundary. Unshaded land is unknown. Named water is not a complete hydrology screening layer. Old facility season/open fields are never used as current access approval.

Fetched source dates and refresh failures appear under **Access & coverage notes**. Snapshots older than seven days are flagged for refresh; a recent fetch can still contain old agency attributes. No live restriction status is inferred from a successful fetch.

## Next release priorities informed by this test

1. Verify the unusual motorcycle season fields against current published motor-vehicle maps and introduce reviewed route-specific overrides with sources and verification dates.
2. Add a Douglas/PSICC restrictions monitor and a curated stay-limit/season registry before recommending camping access.
3. Map reviewed designated dispersed campsites and real access/parking connections. Add precise parcel data only with confirmed reuse rights and coverage.
4. Extend connected trail geometry beyond the county boundary, then validate a route graph and bike/vehicle restrictions before implementing navigation.
5. Add county/state trail sources, verified difficulty and facility suitability based on testing needs.

## Refresh the bundled county data

Use the pipeline Python environment with dependencies in `pipeline/requirements.txt`. From `v2`, run:

```sh
python pipeline/scripts/fetch_douglas.py
python pipeline/scripts/enrich_douglas.py
```

The first command refreshes boundary/trails/roads together and preserves existing context layers and their timestamps. The second independently refreshes recreation, land, wilderness and named water, retaining previous data and marking failures. Check `regions/douglas-co/research.json` source_status and the app's coverage panel before packaging. The county feed currently uses public USFS inventory; it does not need or expose the GitHub RIDB secret. RIDB workflow and Aspen imports remain separate.

Run pipeline Python tests and the Node `pipeline/tests/*.test.cjs` checks after changes. No build step is required for the static website.
