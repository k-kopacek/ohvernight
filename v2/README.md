# ohvernight v2 — pipeline kickoff

Satellite website with the alpine-night logo, source freshness warnings, independently controlled map layers, manual rule registry and an independent RIDB import. The header uses assets/logo-mark.svg; browser icons use favicon.svg and favicon.png. All current work and pipeline source are inside this v2 folder.

## Publish alongside the original

**Forest trails** adds 123 official USFS trail segments in the Aspen study area. Pink lines open trail details and published activity dates on tap. These are partial trail segments, not navigable routes; missing activity records remain unknown. The refresh script and source decision are documented in `pipeline/TRAIL-PILOT.md`. No COTREX data or API key is used for this layer.

Explore opens with the legend closed. Use **Layers & legend** for switches and explanations; all layers still start enabled. On phones, **Explore stays** opens the results panel, which otherwise occupies about 13% of the screen.

The water display includes 1,555 named waterbody/flowline features from the current dataset. All 6,926 hydrology features remain in the pipeline bundle for screening. Named water is not a verified recreation-access or perennial-water dataset; unnamed lakes are also hidden by this initial cleanup.

When uploading, preserve any newer `ridb-options.json` already in your repository. This package does not replace or refresh the RIDB import.

1. Unzip the latest ohvernight v2 delivery ZIP.
2. Open https://github.com/k-kopacek/ohvernight → Add file → Upload files.
3. Drag the entire v2 folder into the repository root, then commit. Do not move its contents into the root.
4. After Pages deploys, compare:
   - Original: https://k-kopacek.github.io/ohvernight/
   - V2: https://k-kopacek.github.io/ohvernight/v2/

If the browser retains an older favicon, close and reopen the tab or try a private tab.

This is a separate static copy for comparison. All assets and data load using relative paths. Current changes apply to v2 only. Trip selections and saved plans share this browser's existing local storage.

Current data is a five-location research inventory, not verified winter camping availability. Map tiles require an internet connection. See DATA-LICENSE.md for source and library attribution.

## How the v2 interface is organized

The first screen is the trip planner. A user chooses a mountain, dates and vehicle, then opens the results map. “Explore the open map” skips the planner and lets a user research the area directly. All 11 legend switches start on: overnight listings, mountains, land management, wilderness, water, forest roads, research areas, restrictions, community leads, reviewed sites and research boundary. Empty or missing layers say so; enabling them does not invent features. Each populated layer has a View button to fit its extent.

Trip dates, vehicle choices and list filters never remove map features. Trip conflicts still appear in listing details. Roads use a neutral color instead of reusing an earlier trip's open/closed classification. Research areas retain the dates and vehicle used to generate them, clearly labeled as a historical screening snapshot. Tap/click a road or shaded feature for its description and source; overlay explanations do not follow the cursor. Use the independent switches to control map visibility. On phones, collapse the legend with its minus button to free map space.

## Connect RIDB once

GitHub only discovers workflows at the repository root under `.github/workflows/`; a workflow inside v2 will not run. The ready-to-copy templates are included in `pipeline/github-workflows/` so this download stays self-contained.

1. Upload this v2 folder to the `ohvernight` repository.
2. On GitHub choose Add file → Create new file. Name it `.github/workflows/ridb-check.yml` and paste the complete contents of `v2/pipeline/github-workflows/ridb-check.yml`. Commit it.
3. Confirm the repository Actions secret is named `RIDB_API_KEY`. No need to paste the key into chat or source files.
4. Open Actions → Check RIDB and export Aspen camping → Run workflow.
5. A green run confirms authentication and produces the `ridb-options` artifact. Download and unzip it; upload `ridb-options.json` into v2. The app loads the imported facilities automatically, avoiding duplicates with the manually reviewed inventory. The `ohvernight-with-ridb` artifact also contains a complete website ZIP with the imported data. That ZIP uses the website files currently on GitHub; upload the latest local v2 first if you want the latest interface included.

Verified September 25: repository secret `RIDB_API_KEY` exists, but only the Pages workflow was installed at the time of inspection. Secret presence alone does not verify its value. Authentication and live inventory still require the import workflow to finish successfully. Never put the key in browser JavaScript, JSON or a downloadable artifact.

The workflow runs only on request, uses no AI calls, and does not publish or commit automatically. GitHub Actions has its own usage terms. A facility listing does not confirm campsite availability, fees or sleeping permission. An official search link is used when RIDB supplies no usable booking link.

## Build the map bundle

For future refreshes, create `.github/workflows/refresh-map.yml` using `pipeline/github-workflows/refresh-map.yml`. Run it with your dates and vehicle. Download its artifact and put `map-data-v2.json` in v2. Roads and research polygons remain visible for any trip, with the screening snapshot dates explained in the legend and feature details. The full source pipeline is in `pipeline/`; the legacy `.github` file inside that folder is for the former standalone layout, not this website repository.

The browser always displays unconfirmed fire/closure coverage. A successful notice-page fetch is not a confirmed fire stage. The native BLM adapter clips and repairs geometry without simplifying coordinates. It remains generalized land management context, not a county parcel survey.

See `ROADMAP.md` for completion status and `pipeline/docs/data-contract.md` for evidence rules.
