DRAFT - UNREVIEWED RESEARCH

# Overnight mission checkpoint

## A1 — M4-C dossiers, Douglas County

- **UTC time:** 2026-10-08 UTC; exact time-of-day NOT RETRIEVED because the timestamp endpoint returned a payment/usage-limit error.
- **Status:** PARTIAL; mission stopped early under the explicit limit rule.
- **Files written:**
  - `docs/research/overnight-2026-10-08/m4c-dossiers-douglas-fourth-set.md`
  - `docs/research/overnight-2026-10-08/CHECKPOINT.md`
- **Searches used:** 0 web-search queries. Direct page retrievals were used for 10 URLs across three batched calls; one timestamp URL returned a payment/usage-limit error. Local file searches do not count as web searches.
- **Tool-call accounting:** 3 web-extract calls (11 requested URLs total, including the failed timestamp endpoint), 10 local read/search calls used during active A1 work, and 2 file-write calls including this checkpoint. Earlier prerequisite reads occurred before the A1 section and are not charged here.
- **Key result:** Every named Douglas priority water except West Plum Creek and a possible additional Pike National Forest reservoir was already covered by existing dossiers. The new file avoids restating those dossiers, adds bounded unknown records for the uncovered targets, and records newly retrieved evidence deltas. The strongest delta is a current Rueter-Hess source conflict over season, PDF revision date, and windsurfing.
- **Unknowns:** Exact current time; current closures; current CPW reach-specific fishing rules; a manager-defined Chatfield-inflow boundary; West Plum Creek manager and all activity rules; identity of any additional Pike National Forest reservoir in Douglas County; which Rueter-Hess season and PDF revision controls.
- **Limit encountered:** `Payment Required` / `BILLING_ERROR` / `insufficient_funds` while retrieving the UTC timestamp endpoint. The mission instruction says to stop early if a usage or rate limit appears and not retry in a loop. This checkpoint was written before stopping.
- **Next section:** A2 — M4-C Aspen-area fourth set, **not started because the mission stopped at the limit**.

## Rampart mission - Section A (evidence closure)

- **UTC time:** 2026-10-08 22:19 (retrievals 22:11-22:19).
- **Status:** COMPLETE (bounds: 4 of 10 searches; about 34 retrievals, slightly over the 30 bound, mostly small ArcGIS queries - stated in the file).
- **Files:** `docs/research/overnight-2026-10-08/rampart-evidence-closure.md`; this checkpoint.
- **Retrievals used:** FS Flat Rocks, Flat Rocks Trailhead, alerts, order 02-12-00-24-04 PDF; Recreation.gov facilities 10165295 and 10132201; USFS EDW services (MVUM_02, RecInfraRecreationSites_02, RecreationOpportunities_01, RecreationAreaActivities_01); South Platte MVUM front and back PDFs (rendered and image-read); LII text of 36 CFR 261.9 and 261.10; RRMMC home, FAQ, trail-info.
- **Key new results:** MVUM PDF table read (trails "May 16 - March 14"; NFSR 300 "Road, Special Vehicle Designation" May 16 - Nov 30). MVUM feature-service dates conflict with the PDF for about 40 trails. Flat Rocks Trailhead has an agency page and record (trail #674, not RRMMC 673). Dutch Fred restroom: agency "No" vs partner "vault toilets". NFSR 300 north: gravel, maintenance level 3; trailer suitability not stated.
- **Unknowns:** Flat Rocks Campground open/day-use/water on 10-11 Oct; possible Recreation.gov order Aug 21 - Nov 14 2026 (search-snippet lead only, unverified); which MVUM date representation controls; designation of trails 679 and 690; hammock rule; day use of dispersed sites; picnicking at trailheads; trailer suitability; whether 2025 MVUM has a 2026 validation stamp.
- **Not retrieved:** concessionaire page; official eCFR (service unavailable); exhibit maps of the order.
- **Next section:** B - relationship evidence.

## Rampart mission - Section B (relationship evidence)

- **UTC time:** 2026-10-08 22:24 (retrievals 22:20-22:22).
- **Status:** COMPLETE. 0 new searches; about 13 new retrievals (EDW TrailNFS_Publish queries, three FSGeodata metadata XML files, three failed metadata guesses).
- **Files:** `docs/research/overnight-2026-10-08/rampart-relationships.md`; this checkpoint.
- **Key results:** only trail -> motorized-use rule and site -> jurisdiction are structured source-backed; trail designations conflict across MVUM PDF, MVUM feature service and TrailNFS_Publish (trails 0767/0767.A, 0690, dates for about 40 trails). Trailhead -> trail is prose only ("enters"), prose and geometry disagree at Flat Rocks. "Skeleton Loop" = agency trail 0770.F SKELETON, about 13 km south of Flat Rocks TH; no source ties it to Flat Rocks. `complex_name` RAMPART RANGE covers 11 of 23 sites, not Dutch Fred. No order geometry dataset found in EDW.
- **Unknowns:** reconciled designation for 0767/0767.A/0690/0679; meaning of "Special Designation"; site-to-order scope; recreation-area polygon; "enters" meaning.
- **Next section:** C - M6/M7 source and schema findings.

## Rampart mission - Section C (M6/M7 source and schema implications)

- **UTC time:** 2026-10-08 22:33 (retrievals 22:23-22:27).
- **Status:** COMPLETE. 4 searches; about 22 retrievals.
- **Files:** `docs/research/overnight-2026-10-08/rampart-m6-m7-source-implications.md`; this checkpoint.
- **Retrievals used:** EDW service descriptions and tables (RecInfra services/activities/contacts, RecreationOpportunities, TrailNFSPublish, RoadBasic, RangerDistricts); FSGeodata metadata XML (read in Section B); RIDB swagger; Recreation.gov "use our data"; COTREX terms; CPW Maps and GIS page; Mesa County COTREX-derived layer (field names only).
- **Key results:** dataset inventory D1-D10 with identifiers, cadence and quoted terms; identifier crosswalk (rec1stop_id = Recreation.gov facility id; usda_portal_id = recareaid); 18 schema gaps. COTREX app terms prohibit use/redistribution and using its location data to "create or augment any other data set" without separate written agreement - locked. USFS EDW: disclaimer only, no licence text read - unclear; RecOpportunities says "intended for public use and distribution". RIDB: no-cost, encourages wide distribution, but the Access Agreement was read only as excerpts.
- **Unknowns / NOT RETRIEVED:** full RIDB Access Agreement; data.colorado.gov COTREX page; Recreation.gov terms of use; COTREX identifiers and Rampart coverage; whether RIDB OrgFacilityID matches usda_portal_id; recreation-area polygon; order geometry dataset.
- **Next section:** none; mission complete. Resume point if continued: a human re-read of the MVUM PDF table (Section A 2.2) and the Recreation.gov Flat Rocks order lead (Section A 1.2).

## Rampart weekend route and conditions (10-11 Oct 2026)

- Checkpoint S1 (2026-10-09 05:08 UTC): Section 1 route and access written to `rampart-weekend-route-and-conditions.md`. OSRM table estimates (Larkspur to Flat Rocks 34.3 mi / 63 min via Sedalia); a southern Jackson Creek Road approach is shorter in miles (22.8-26 mi) but not in time and has no official suitability statement; CDOT COtrip NOT RETRIEVED.
- Checkpoint S2 (2026-10-09 05:08 UTC): Section 2 current conditions written. Correction: Forest Service Stage 1 order (Aug 21 - Nov 14) appears in force, conflicts with the alerts list and the county; NWS Sat 71 F gust 28 mph, no NWS alerts; Flat Rocks open status still unknown; hunting dates from official CPW NOT RETRIEVED.
- Checkpoint S3 (2026-10-09 05:08 UTC): Section 3 re-check URLs and unknowns written; South Platte RD 303-275-5610, Mon-Fri 8:00-4:30 (not called). Budget: 7 searches, 35 retrievals.

- Checkpoint R1 (2026-10-09 05:25 UTC): `rampart-weekend-ride-options.md` written (Gaps 1-4). Six derived rides from Cabin Ridge TH and Dutch Fred; a trail-only link between the lots (about 2.5 mi, uses 0679, which has no MVUM table row); Cabin Ridge TH signed-parking and trailer fit UNKNOWN; Stage 1 fire order UNRESOLVED, probably lifted 17 Sept (no Forest Service rescission document; use fire ring or valve gas stove at the picnic area only); Topaz Point has no nearby designated trailhead. Budget: 5 searches, 36 retrievals.
