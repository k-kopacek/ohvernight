# Verification — September 24, 2026

## Completed

18 offline regression tests passed under Python 3.12. These cover independently measured buffer distances; vehicle-specific access and whole-trip seasonal windows; missing and malformed designation fields; cross-year and leap-day dates; real MVUM property names; ownership remaining separate from permission; rejection of group layers; complete ArcGIS feature retrieval despite transfer limits; rejection of missing or truncated IDs; transient JSON error retries; count-query fallback; water, wilderness and private-land exclusion; community leads staying unverified; curated-site evidence and expiry; removal of synthetic pins; and preservation of previous data after failures.

The live MVUM adapter downloaded and normalized 28 road segments for January 15–17, 2027, using the passenger-car designation. Results: 26 restricted, two designated open. This does not establish snow clearance, physical passability, availability, or permission to sleep overnight.

Service metadata confirmed the configured BLM, USFS MVUM, wilderness, and USGS hydrology layer types and relevant fields. Metadata access alone is not a successful geometry download.

## Incomplete live verification

- BLM SMA: count and ID requests were inconsistent; geometry requests repeatedly returned server errors. Some individual polygons could be retrieved, but the complete required dataset could not. The production run stopped at ownership ingestion and did not create a public bundle.
- USGS hydrology: a separate live adapter check reached feature retrieval, then exhausted retries with HTTP 504 responses on the flowline layer. No complete water layer was produced.
- Wilderness: metadata verified; complete download and end-to-end exclusion remain unverified against live data because the production run stopped earlier.
- RIDB: no API key was supplied, so live inventory retrieval remains untested. Missing credentials are explicitly represented as an unavailable optional source.
- CPW: the original service returned 404; the adapter remains explicitly unavailable pending a checked replacement.
- No actual curated sites or restriction-order polygons were supplied. The pipeline does not invent sites or convert research geometry into approved places.

## Release status

Changes are local to this pipeline directory. The existing GitHub Pages MVP has not been changed by this work. Before connecting the generated bundle to that site, obtain a complete successful spatial refresh, add evidence-backed actual sites and applicable order boundaries, and implement date/vehicle reevaluation and source-status display in the map.

The original pipeline is backed up in the Codex workspace under `work/aspen-overnight-data-before-fixes-2026-09-24/`.
