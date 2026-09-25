# Layer update — September 25

## Try this after uploading v2

1. Open the website and choose **Explore the open map**, then **Layers & legend**. All layer switches start on. The initial research data has 54 forest road segments, 51 research polygons, 1,555 displayed named water features (6,926 retained for screening), 3 land-management features and 3 wilderness features. These are map-feature counts, not campsite counts.
2. Change dates and vehicle using **Edit trip**. Roads, research areas and location pins remain on the map. The list can still explain conflicts for your trip.
3. Turn Named water off and back on. Only that layer changes. Use **View** beside Forest vehicle roads or Areas to research to find their extent; the drawer closes automatically.
4. Tap a road or shaded feature. Details open on tap/click, with source information. They do not follow your mouse. Research polygons explain their screening dates and do not claim verified camping permission.
5. On your phone, use **Layers & legend** to open the drawer and its close button to return to the map. Use **Explore stays / More map** to open and close the listing sheet. Escape closes the legend and restores keyboard focus.
6. Restrictions, community leads and reviewed sites currently have no mapped features. Their empty states are deliberate and do not mean an area is unrestricted.

## RIDB connection

The GitHub repository has a secret named `RIDB_API_KEY` and the import workflow has been installed. The user reports that the key issue is resolved. This UI update does not rerun the import or verify publication of its output. The bundled workflow template is `pipeline/github-workflows/ridb-check.yml`; its active repository location is `.github/workflows/ridb-check.yml`.

The import checks authentication, fetches and validates campground records, and exports `ridb-options.json`. Put that JSON in v2; the next page load imports it into the map and listing sheet. The key stays inside GitHub Actions. The workflow also provides a downloadable site ZIP containing the imported JSON. It does not publish the website automatically.

## Verification performed

- 28 Python pipeline regression tests passed.
- JavaScript syntax checks and four Node test results passed, covering real layer counts, missing versus empty/failed feeds, geometry-free fire notices, freshness and rule handling.
- Local browser: all 11 switches enabled; trip changed to October 10–12 with Motorhome / RV while road/research counts stayed present; all nine initial pins remained visible.
- Local browser: filtering the list down to two entries retained all map pins; turning listings off left four resort pins; turning listings back on restored nine pins.
- Local browser: tap opened water feature source details. The research boundary was made non-interactive so it cannot intercept clicks on underlying features.
- Desktop, 390px and 320px phone layouts inspected; no horizontal document overflow at phone widths and no captured browser console errors.

Not yet verified: live RIDB authentication/import, statewide coverage, current road conditions, and legal camping permission for generated research areas.
