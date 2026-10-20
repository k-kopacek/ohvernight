# ohvernight · Aspen Snowmass

A full-screen satellite/aerial map with sourced overnight options, date/vehicle screening and a saved Plan A plus backup. Static GitHub Pages website; no build or API key required.

## Publish

1. Unzip `ohvernight-satellite-ready-to-upload.zip`.
2. In https://github.com/k-kopacek/ohvernight select **Add file → Upload files**.
3. Drag the unzipped **contents**, including the `vendor` folder, into the repository root and replace matching files.
4. Commit to the Pages publishing branch. After deployment, refresh https://k-kopacek.github.io/ohvernight/ on your phone.

This version is prepared locally, not deployed. Compare any separate GitHub edits before replacing matching files.

## What changed

- Real USGS satellite/aerial tiles across the entire viewport, with pan, pinch zoom, fit-area and a topo toggle.
- Charcoal, warm white and lime interface; floating desktop panel and expandable phone results sheet.
- Full-width vehicle selector in a trip dialog, including Passenger car / SUV.
- Official listing/booking button immediately under each selected place name, before status or evidence.
- Date/vehicle conflicts, outstanding checks, direct distance to the selected mountain and a room-backup shortcut.
- Plan A and backup saved on this device, with their current limitations displayed after date/vehicle changes. Saving is not approval or a reservation.
- External directions link; the app itself does not calculate driving times or verify routes.

## Quick phone test

Open **Edit trip** and select dates, mountain and vehicle. January 15–17, 2027 in a passenger car has road-season conflicts at Difficult and Silver Bell, a tent-only conflict at Silver Bar and a high-clearance conflict at Lincoln Creek. St. Moritz is a room backup with availability unknown.

Try June 15–17, 2027 and high clearance. Camping records remain review-needed even where their road designation covers the dates. Open a location and use the prominent official link. Save a Plan A and a different backup; refresh to check persistence. Tap **More map** to collapse the results, pan/zoom the map and try Topo. Test at 320–430px widths.

Source reviews become stale after 30 days. Recheck evidence before changing `checked_on`; changing the timestamp alone is not a review. All five current records remain unconfirmed for winter vehicle sleeping.

## Files and data sources

- `index.html`, `styles.css`, `app.js`: interface and Leaflet map.
- `trip-rules.js`: whole-trip date and vehicle evaluation.
- `overnight-options.json`: five manually curated places/areas, source links, review dates, unknowns and optional vehicle designations.
- `destinations.json`: four mountain orientation points.
- `vendor/`: locally bundled Leaflet 1.9.4 with its license.
- `map-data.json`: downloadable original OpenStreetMap-derived orientation data, retained for provenance.

Recreation.gov / [RIDB](https://ridb.recreation.gov/) supplies facility inventory; Forest Service and BLM recreation pages supply named camping locations; lodging operators supply room/booking information. The current inventory is manually curated, not an automatic feed. The experimental ownership/water pipeline is not required to display these actual locations and does not approve them.

[USGS The National Map](https://www.usgs.gov/faqs/what-are-base-map-services-or-urls-used-national-map) supplies imagery and topo tiles. Imagery is aerial/satellite context, not live snow, road conditions, access rights or vacancy. Internet is required for tiles. Missing tiles produce a visible notice while the location list remains available. USGS imagery is overzoomed past its useful native scale rather than promising additional detail.

No analytics or account is used. Trip and saved-place IDs persist only in this browser's local storage. Tile providers receive ordinary map requests; official links and directions open external websites. See DATA-LICENSE.md.

For a local preview, serve this directory over HTTP; opening index.html as a file cannot fetch its JSON data in most browsers.
