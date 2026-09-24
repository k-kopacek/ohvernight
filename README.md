# Overnight · Aspen Snowmass

Ready-to-upload static website, with five sourced places/areas and trip-specific date/vehicle screening. No build step, server account, API key or paid service is required.

## Your next step: update GitHub

1. Unzip `aspen-overnight-ready-to-upload.zip`.
2. Open https://github.com/k-kopacek/aspen-overnight and select **Add file → Upload files**.
3. Upload the **contents** of the unzipped folder to the repository root, replacing existing files. Include both JSON files and all three JavaScript files.
4. Commit to the branch used by Pages. After deployment completes, open https://k-kopacek.github.io/aspen-overnight/ and refresh.

This package has not been deployed. Keep the existing Pages configuration. If the GitHub copy has separate changes made after this local prototype, compare those before replacing its files.

## Quick phone test

- January 15–17, 2027, passenger car: Difficult and Silver Bell show a vehicle-season conflict. Silver Bar is tent-only; Lincoln Creek requires high clearance. St. Moritz is a room backup with availability unknown.
- June 15–17, 2027: Difficult and Silver Bell move to needs-review, not approved. Their road designations cover those days; operating dates and overnight permissions still need review.
- Select dispersed camping, hide mismatches, then switch between passenger car and high clearance. Lincoln Creek appears for high clearance with access still unverified. Its pin represents the area, not one of its 22 campsites.
- Select a mountain and compare locations. Distances are straight-line, not driving distance or time. Local road coverage is incomplete, especially near Lincoln Creek.
- Open a place's sources. Ask a tester whether they can identify what remains unknown before choosing a primary option and a backup.

Source reviews become stale after 30 days. Recheck them before changing `checked_on`; a timestamp update alone is not a review. Stale records do not receive a fresh access assessment.

## Updating locations

`overnight-options.json` is the curated inventory. Edit it to add or update actual locations without changing the website code. It includes sources, location basis, review date, unresolved questions, vehicle requirements and optional source-backed road designations. Keep unknown facts unknown. The website fetches it and `map-data.json` independently of the experimental spatial ingestion pipeline.

`trip-rules.js` handles whole-trip date and vehicle checks. `app.js` loads data and renders the map. The inventory is manually curated; automatic RIDB synchronization is not connected. The failed ownership/water feeds do not supply permissions or recommendation pins.

## Sources to expand next

- Recreation.gov RIDB: https://ridb.recreation.gov/ — structured federal facility and campsite inventory. An API key supports scheduled imports; downloadable inventory is also offered at https://ridb.recreation.gov/download. Inventory is not live availability.
- Forest Service recreation listings: https://www.fs.usda.gov/r02/whiteriver/recreation/lincoln-creek-dispersed-camping — actual named dispersed areas and campground details. Curate individual sites only when their locations and conditions are evidenced.
- BLM recreation listings: https://www.blm.gov/visit — actual developed/dispersed recreation locations; land-ownership polygons alone are not campsites.
- Lodging operators: https://www.stmoritzlodge.com/ — direct room descriptions and booking links. Do not assume vacancy, price or vehicle-sleeping permission from a hotel's existence.

Current inventory: Difficult, Silver Bar, Silver Bell, Lincoln Creek dispersed area, St. Moritz Lodge. No confirmed winter vehicle-sleeping options or booking availability are claimed. Map data licensing is documented in DATA-LICENSE.md. Serve over HTTP for local preview; opening index.html directly as a file cannot fetch the JSON files in most browsers.
