# ohvernight v2 — pipeline kickoff

Satellite website with the alpine-night logo, source freshness warnings, trip-specific map layers, manual rule registry and an independent RIDB import. The header uses assets/logo-mark.svg; browser icons use favicon.svg and favicon.png. All current work and pipeline source are inside this v2 folder.

## Publish alongside the original

1. Unzip ohvernight-v2-ready-to-upload.zip.
2. Open https://github.com/k-kopacek/ohvernight → Add file → Upload files.
3. Drag the entire v2 folder into the repository root, then commit. Do not move its contents into the root.
4. After Pages deploys, compare:
   - Original: https://k-kopacek.github.io/ohvernight/
   - V2: https://k-kopacek.github.io/ohvernight/v2/

If the browser retains an older favicon, close and reopen the tab or try a private tab.

This is a separate static copy for comparison. All assets and data load using relative paths. Current changes apply to v2 only. Trip selections and saved plans share this browser's existing local storage.

Current data is a five-location research inventory, not verified winter camping availability. Map tiles require an internet connection. See DATA-LICENSE.md for source and library attribution.

## Connect RIDB once

GitHub only discovers workflows at the repository root under `.github/workflows/`; a workflow inside v2 will not run. The ready-to-copy templates are included in `pipeline/github-workflows/` so this download stays self-contained.

1. Upload this v2 folder to the `ohvernight` repository.
2. On GitHub choose Add file → Create new file. Name it `.github/workflows/ridb-check.yml` and paste the complete contents of `v2/pipeline/github-workflows/ridb-check.yml`. Commit it.
3. Confirm the repository Actions secret is named `RIDB_API_KEY`. No need to paste the key into chat or source files.
4. Open Actions → Check RIDB and export Aspen camping → Run workflow.
5. A green run confirms authentication and produces the `ridb-options` artifact. Download and unzip it; upload `ridb-options.json` into v2. The app loads the imported facilities automatically, avoiding duplicates with the manually reviewed inventory.

The workflow runs only on request, uses no AI calls, and does not publish or commit automatically. GitHub Actions has its own usage terms. A facility listing does not confirm campsite availability, fees or sleeping permission. An official search link is used when RIDB supplies no usable booking link.

## Build the map bundle

For future refreshes, create `.github/workflows/refresh-map.yml` using `pipeline/github-workflows/refresh-map.yml`. Run it with your dates and vehicle. Download its artifact and put `map-data-v2.json` in v2. Roads and research polygons display only when the selected trip matches the bundle. The full source pipeline is in `pipeline/`; the legacy `.github` file inside that folder is for the former standalone layout, not this website repository.

The browser always displays unconfirmed fire/closure coverage. A successful notice-page fetch is not a confirmed fire stage. The native BLM adapter clips and repairs geometry without simplifying coordinates. It remains generalized land management context, not a county parcel survey.

See `ROADMAP.md` for completion status and `pipeline/docs/data-contract.md` for evidence rules.
