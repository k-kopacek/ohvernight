# ohvernight execution queue

The scheduled kickoff was deleted; work started directly in the existing task.

## Completed local increment — September 25

Mobile Explore now has a roughly 13% collapsed results panel and an on-demand, keyboard-accessible layer drawer. All layers remain enabled initially and independent of trip filters. The initial water cleanup displays named waterways/waterbodies only while preserving the complete screening geometry. It does not yet classify perennial flow or recreation access. Verified at 320, 390, 768, 1024 and 1440px widths; layer and trust tests pass.

Next: validate official Colorado trail source access and reuse terms, define a shared activity vocabulary, then implement a small trail ingestion pilot. Richer water classification needs source attributes and recreation-access evidence, including treatment of unnamed lakes. Statewide coverage and adventure ranking remain pending.

## Latest user direction — supersedes the earlier priority order

- User reports the RIDB API-key issue is resolved. Do not repeat credential troubleshooting. A successful data import and publication are separate checks; verify them only when needed for the next implementation.
- Minimize credit use: small implementation batches, focused local checks, reuse existing assets and integrations, and no unsolicited parallel agents or design-tool round trips.
- Two experiences share the data: **Choose Your Adventure** (state, dates, activities, relevant destinations) and **Explore Map** (free discovery without trip filtering). Colorado is the initial supported state; do not imply other states have coverage.
- Mobile Explore comes first: nearly full-screen map, compact search/filter controls, layers in an on-demand drawer, and a small collapsed place sheet. Keep available layers enabled by default while reducing panel obstruction. Open details only on tap.
- Recreational water display comes next: prioritize lakes/reservoirs, rivers and significant streams using real source attributes. Suppress drainage and flow-path clutter on the display. Preserve the full hydrology dataset for screening and setbacks; display filtering must not weaken spatial exclusions. Named/perennial water does not by itself establish public access, fishing permission or paddling suitability.
- Establish a small shared activity vocabulary, then assess official Colorado trail-data access, licensing, attributes and completeness before implementing COTREX-related ingestion. The pasted discussion proposes COTREX coverage; it does not establish that all app data is downloadable or reusable. Preserve unknown activity/access permissions instead of guessing them.
- Connect camping, trailheads/trails and recreational water through geographic relationships, then build activity-based destination results. Distinguish straight-line proximity from a usable route and verified access. Existing camping/access/restrictions evidence rules remain in force.
- Sequence: **mobile Explore → recreational-water display → activity model and trail-source validation → trail ingestion → adventure search → evidence-based destination ranking**. Start with a few representative Colorado areas before statewide detailed ingestion. Figma is optional, not a prerequisite or an authorized new design project.

The audit below records the earlier delivery state; it is not a fresh claim that the API key remains broken.

## Implemented in this delivery

- Restored the latest pipeline, preserved the Downloads copy, and included the working source under v2/pipeline.
- Independent RIDB credential check and paginated export, with explicit failures, validated inventory, atomic publication and a manual GitHub Actions template. Browser importer avoids known facility duplicates and keeps trip permission unknown.
- BLM native JSON adapter with exact study-area clipping, topology repair, hole/island preservation and complete ID checks. USGS requests use smaller batches and split failing batches within bounded request retries.
- Expanded the study area to include Lincoln Creek; the previous east boundary excluded it.
- Source-linked Lincoln Creek rule registry; no assumed forest-wide permission or stay limit. Unknown road rules remain unknown.
- Browser freshness logic, visible unconfirmed fire/closure notices, confidence labels and map-layer toggles. September 25 update: all layers start enabled, and dates/vehicle no longer filter map geometry. Neutral road styling and dated research descriptions prevent reusing a prior trip's suitability assessment.
- Python regression tests and mobile/desktop verification.

## Must still be verified or built

### September 25 functionality audit and revised priority

The local bundle generated September 25 contains 3 management-area features, 3 wilderness features, 54 MVUM road segments, 6,926 water features and 51 generated research polygons. These are feature counts, not campsite counts. The browser inventory remains 5 manually sourced places: `ridb-options.json` is absent, the developed-inventory layer is empty, and there are no mapped wildlife or fire restrictions. The fire record is an unconfirmed page monitor with no geometry. Wilderness data is used by screening but has no browser overlay.

The bundle is evaluated for September 25–26, 2026 and `high_clearance`. The default browser trip is January 15–17, 2027 and `passenger_car`. The earlier exact-trip matching hid roads and research polygons for that default. The research-area checkbox also started off. Both visibility problems are fixed in the September 25 layer update.

Delivered locally: all 11 layer switches on by default; counts and empty/unavailable explanations; study boundary and wilderness overlay; View buttons; click/tap source details; cached geometry instead of recreating thousands of water features on each trip edit. List conflicts still update without removing map pins. RIDB repository secret presence was confirmed in GitHub, but its import workflow was not installed. An updated workflow template exports both the inventory and an optional full-site download; no automatic website publication.

Continue in this order, keeping work local for manual GitHub upload:

1. **Make the integration observable.** Show per-layer loaded counts, coverage, fetch date and missing-data states. Distinguish an unavailable feed from a successful empty result. Add a visible study-area boundary and a way to fit the map to a selected layer. Acceptance: a user can tell what loaded and why any selected layer is absent.
2. **Separate exploration from trip evaluation.** Keep road geometry visible as neutral research context when dates differ; do not reuse its prior trip's open designation. Allow research polygons to be inspected as a clearly dated snapshot, without implying suitability for the current trip. Add click/tap details with road name, source and outstanding checks. Acceptance: default trip, changed trip and open exploration all retain intelligible layers, with no stale suitability claim.
3. **Prove the overnight inventory import.** Run the RIDB workflow using the existing GitHub secret and import its validated output. Check known facilities, duplicates and official listing links. Acceptance: imported records reach both the map and results list, and missing credentials or failed requests remain visible.
4. **Prove one generated corridor end to end.** Compare Lincoln Creek and one neighboring corridor with supplied geometry, screening exclusions and source-linked rules. Acceptance: known controls produce expected inclusions/exclusions, with unresolved camping permission left unknown. A polygon count is not sufficient validation.
5. **Expand Colorado research coverage in regional packages.** Start with statewide management/wilderness context and developed camping inventory, then add roads and detailed water by region or viewport. Exercise additional mountain and western Colorado regions before claiming statewide coverage. Avoid a single statewide copy of the current all-in-one JSON bundle. Acceptance: a phone can load a new region, inspect its sources, and identify coverage gaps without downloading the whole state's detailed geometry.

Statewide browsing and verified overnight recommendations are separate milestones. County parcels, restriction monitoring, mapped orders and rule reviews below remain required; larger coverage does not supply them automatically. Full trails/navigation remains later work.

### Remaining source and verification work

1. Run the independent RIDB workflow with the existing GitHub secret; local checks cannot establish whether that secret is valid. Upload the resulting inventory JSON to v2.
2. Verify a complete live map build and inspect generated Lincoln Creek plus a neighboring corridor against official camping rules. Generated areas remain research polygons, not legal campsite recommendations.
3. Audit Pitkin parcel coverage, ownership fields and reuse terms; add county public/private/unknown polygons. Federal management shading is only generalized context. Audit each additional county before expansion, and scope any paid fallback separately.
4. Expand the existing county page-change monitor to Forest Service orders and wildlife notices. Track successful retrieval separately from human-confirmed status, jurisdiction, effective periods and staleness. A page hash alone must never approve fire use or clear a closure.
5. Review and map order boundaries; connect confirmed restrictions and site-specific rules to candidate screening and trip evaluations. Do not ship candidate approvals before this coverage is real.
6. Add issue reporting/community leads with moderation and clear separation from verified agency facts. Add suitable product terms and obtain legal review before broader reliance; source caveats are not a substitute.
7. User-test finding an overnight option plus a backup near Aspen. Add actual route distance/approach checks once the overnight flow is useful. Full navigation, trails, GPX, wider counties and paid datasets remain later work.

## Delivery constraints

Keep all code and data together in v2. Workflow templates are included there, but GitHub requires their installed copies at repository-root `.github/workflows/`. No scheduled AI loops, automatic public deployment, purchased services or broad security scans are part of this kickoff.
