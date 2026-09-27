# Douglas County expansion

Field-test edition. See ../../DOUGLAS-TESTING.md for publishing, testing, inventory and limitations. County data remains separate from Aspen. Refresh from v2 with `python3 pipeline/scripts/fetch_douglas.py`, then `python3 pipeline/scripts/enrich_douglas.py` using the pipeline dependencies. Base refresh preserves enrichment and original timestamps; failed enrichment retains old data with a failed status. Nearby camping is proximity only, never a verified riding connection or access approval.

## Source audit — September 27, 2026

- Boundary: US Census TIGERweb State_County layer 1, Colorado Douglas GEOID 08035. County boundary is a clipping boundary, not a landownership polygon.
- Trails: USFS TrailNFSPublishWithDataStatus layer 0. Activity strings retained; county/state trails still missing.
- Roads: USFS MVUM_02 layer 1. Display is geometry-only; no current passability or camping permission inferred.
- Ownership: county Parcels service exists at https://apps.douglas.co.us/gisod/rest/services/Parcels/MapServer . Layer 0 BOUNDARY is linework, not public/private ownership. Ownership classification and redistribution review remain pending; do not ingest owner names for this purpose.
- Land context: BLM National SMA LimitedScale layer 1 provides five broad polygons (USFS, other federal, state, local, private). These are not surveyed parcels. Unshaded areas are unknown.
- Water: USGS NHD layers 12 and 6 provide 33 named waterbody and 2,359 named flowline features. This is a display subset, not full screening hydrology.
- Facilities: USFS RecInfraRecreationSites_02 layer 0 supplies five general campgrounds and 17 trailheads. Horse-only camping is excluded from general suggestions. Published season and operational attributes can be historical; no live-open status is inferred.
- Camping: https://www.recreation.gov/camping/campgrounds/10132201 identifies designated dispersed camping at Rampart. Numbered sites and fees are required; listing describes December 1–April 1 closure with weather-dependent reopening. This rule applies to the listed area, not every place named Rampart. RIDB region import and coordinates still pending. The existing campground-name filter would omit this designated dispersed listing; use an explicitly reviewed facility allowlist when extending RIDB.
- Restrictions: https://dcsheriff.net/sheriffs-office/divisions/emergency-management/fire-restrictions/ is a county source. Federal orders must be checked separately. No live status inferred or polygon invented.

## Remaining gates

1. Add reviewed campground/designated-dispersed inventory via region-aware RIDB import; maintain source-level exclusions for day use.
2. Add current federal/county restriction evidence, precise parcel context and reviewed facility rules. Source timestamps and failed-refresh messages already accompany imported context.
3. Add county/state trails after source and reuse review.
4. Integrate region selection into the main app only when regional rules and coverage messages are isolated from Aspen.
5. Test cross-boundary trips explicitly; never assume county-clipped segments describe complete Rampart routes.
