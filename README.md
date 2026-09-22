# Overnight · Aspen Snowmass

A responsive, static map prototype for phone user testing. Compare two campground examples with Aspen Mountain, Aspen Highlands, Buttermilk, and Snowmass.

## Publish with GitHub Pages

1. Create a public repository named `aspen-overnight` in `k-kopacek`.
2. Upload this folder's **contents** to the repository root on `main`.
3. In **Settings → Pages**, select **Deploy from a branch**, then **main** and **/(root)**. Save.
4. When deployment completes, open `https://k-kopacek.github.io/aspen-overnight/` on your phone.

That URL is the expected address, not a confirmation that the site is live. No build command, backend, API key, or paid hosting is required. The source repository and Pages website are public. The noindex tag discourages search indexing but is not access control.

GitHub instructions: https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site

## Test on your phone

Ask a participant to plan a car/SUV overnight trip near their chosen mountain. Observe whether they can:

- Select their mountain and trip dates.
- Locate and select both campground examples on the map and in the list.
- Explain each site's relationship to the destination.
- Find the evidence and distinguish a setup mismatch from a place still needing review.

Then ask what information is missing before they could confidently choose a place. Record observations separately; this prototype has no analytics, feedback collection, accounts, or saved trips.

## Current limits

This tests the interface, not whether the product solves finding a permitted winter campsite. Neither example is an approved winter vehicle-sleeping option. Silver Bar is a tent-only setup mismatch. Dates do not query availability. Distances are straight-line, not driving distances. Road geometry is a partial orientation map. Fees, winter access, road conditions, and vehicle-sleeping permission need review.

OpenStreetMap-derived map data is downloadable as `map-data.json`; see `DATA-LICENSE.md`. The D3 library and its license are included locally. The site does not contact external services until someone follows a source link.
