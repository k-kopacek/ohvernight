# Douglas County expansion

Research preview only. County-bounded USFS geometry is kept separate from Aspen and is not used for camping suggestions. Refresh from v2 with `python3 pipeline/scripts/fetch_douglas.py` using the existing pipeline dependencies. The complete boundary/trail/road snapshot replaces the old file only after all three succeed.

## Source audit — September 27, 2026

- Boundary: US Census TIGERweb State_County layer 1, Colorado Douglas GEOID 08035. County boundary is a clipping boundary, not a landownership polygon.
- Trails: USFS TrailNFSPublishWithDataStatus layer 0. Activity strings retained; county/state trails still missing.
- Roads: USFS MVUM_02 layer 1. Display is geometry-only; no current passability or camping permission inferred.
- Ownership: county Parcels service exists at https://apps.douglas.co.us/gisod/rest/services/Parcels/MapServer . Layer 0 BOUNDARY is linework, not public/private ownership. Ownership classification and redistribution review remain pending; do not ingest owner names for this purpose.
- Water: existing USGS source can be queried regionally; not fetched yet. Recreational display and full screening geometry must remain distinct.
- Camping: https://www.recreation.gov/camping/campgrounds/10132201 identifies designated dispersed camping at Rampart. Numbered sites and fees are required; listing describes December 1–April 1 closure with weather-dependent reopening. This rule applies to the listed area, not every place named Rampart. RIDB region import and coordinates still pending. The existing campground-name filter would omit this designated dispersed listing; use an explicitly reviewed facility allowlist when extending RIDB.
- Restrictions: https://dcsheriff.net/sheriffs-office/divisions/emergency-management/fire-restrictions/ is a county source. Federal orders must be checked separately. No live status inferred or polygon invented.

## Remaining gates

1. Add reviewed campground/designated-dispersed inventory via region-aware RIDB import; maintain source-level exclusions for day use.
2. Add ownership, water and federal/county restriction evidence with freshness tracking.
3. Add county/state trails after source and reuse review.
4. Integrate region selection into the main app only when regional rules and coverage messages are isolated from Aspen.
5. Test cross-boundary trips explicitly; never assume county-clipped segments describe complete Rampart routes.
