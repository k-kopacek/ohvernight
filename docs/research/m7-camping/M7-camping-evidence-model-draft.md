DRAFT - UNREVIEWED

# M7 camping evidence model — draft

> Preparation only. Nothing here is decided, nothing is implemented, and `ROADMAP.md` is unchanged.
> Drafted 2026-10-07 by a research agent from the Hermes report in `hermes/m7-overnight-evidence-sources.md`, the M5–M8 source watchlist, the Q3 trip-failure report, a read-only measurement of the repository at `m4a-source-preservation`, and 20 read-only HTTP GET attempts against official hosts (19 answered; appendix A).

**Labels.** Every factual statement carries one of four labels:

- `[READ IN REPO]` — measured or read in repository files. `[READ ON WEB (not coordinator verified)]` — read in a saved response from the official host. A web read is retrieval, not a review in the sense of trust principle 4, and can confirm no claim.
- `[HERMES]` — HERMES-SOURCED. Stated by the Hermes report; not re-checked.
- `[INFERENCE]` — reasoning by this agent from verified or Hermes material.
- `[UNKNOWN]` — not established by anything read.

Quoted sentences are from the saved responses and are under 25 words.

---

## 1. Summary

1. **The product makes no camping-permission claim today, and says so.** `camping_permission` is `unknown` on all 109 records that carry it; `fact_coverage.camping_permission.state` is `none` in both regions. `[READ IN REPO]`
2. **The product nevertheless draws 51 "Areas to research" polygons along Aspen forest roads.** At least 16 of the 51 are named after campground roads whose surroundings a current Forest Service order closes to camping, and five more are named after trailhead spurs where a 1996 order prohibits camping within 300 feet. The polygons are worded as research areas, not campsites, but they are the single largest overnight-related thing on the map and they sit on restricted ground. `[READ IN REPO]` for counts and names, `[READ ON WEB (not coordinator verified)]` for the orders, `[INFERENCE]` for the overlap (matched by road name; the order's map exists only as a PDF exhibit that was not read).
3. **"Can I stay here?" decomposes into eight layers, and published *data* covers only three of them** (existence, generalized management, vehicle designation). The camping rule itself exists only as prose and as forest orders with PDF map exhibits. `[READ ON WEB (not coordinator verified)]` for the sources read; `[INFERENCE]` for the generalization.
4. **The M4 claim model extends cleanly.** The same four statuses, the same evidence object and the same freshness table work for overnight use. Three additions are needed: a `scope` (site / corridor / area / default rule), an order identity with its own effective dates, and a precedence rule so that an area order overrides a site-level statement. `[INFERENCE]`
5. **A forest-wide default rule is a limit, never a permission.** The 14-day stay limit can be attached to a place only as a condition, worded so that it cannot be read as "camping is allowed here". `[INFERENCE]`
6. **Hermes was wrong on two consequential points and incomplete on a third** (section 12): fire restrictions it reported as current were lifted in all three jurisdictions two weeks earlier; the Aspen occupancy order it reported as expired is in force through 2028; and the public RIDB schema, which it could not load, contains no availability field. `[READ ON WEB (not coordinator verified)]`
7. **Availability cannot be known.** The Forest Service says so itself: "We have no way of knowing real time availability." `[READ ON WEB (not coordinator verified)]`

---

## 2. What the product says today (measured)

All figures in this section are `[READ IN REPO]` unless marked. Measured with throwaway scripts against `v2/map-data-v2.json` (run `generated_at` snapshot; pipeline steps completed 2026-09-25), `v2/overnight-options.json`, `v2/ridb-options.json`, `v2/destinations.json` and `v2/regions/douglas-co/research.json`.

### 2.1 Aspen — layers

| Layer | Kind | Features | Fields and completeness | Limitation sentence (verbatim) |
|---|---|---:|---|---|
| `lodging_developed` | `overnight_inventory` | **0** | none; source status `unavailable`, reason "RIDB_API_KEY is not configured; developed inventory unavailable" | "Facility inventory only. No availability, operating dates or vehicle-sleeping permission." |
| `dispersed_corridors` | `research_areas` | **51** (37 MultiPolygon, 14 Polygon; about 7.5 km² summed, overlaps not merged) | all 10 properties 51/51: `camping_permission` = `unknown` 51/51; `needs_review` = true 51/51; `actual_site_confirmed` = false 51/51; `site_type` = `candidate_area` 51/51; `applicable_rule_context` = `[]` 51/51; identical six `required_checks` 51/51 | "Computed screening geometry. Not a campsite and not permission." |
| `dispersed_corridor_points` | `research_areas` | **0** (`must_be_empty: true`) | — | same sentence |
| `leads` | `community_leads` | **0** | — | "Unverified reports." |
| `reviewed_sites` | `reviewed_sites` | **0** | — | "Hand-researched listings with per-record source links. Listing a place does not confirm permission, operation or availability." |
| `fire_restriction_stage` | `restriction_monitor` | **1**, null geometry | `status` = `unknown`, `stage` = null, `last_confirmed_at` = null, `max_age_hours` = 24, a page hash, `verification_method` = `html_change_monitor` | "Review dated notices and jurisdiction; no current stage inferred." |
| `wildlife_sensitivity` | `wildlife_context` | **0** | source disabled; ArcGIS 404 on 2026-09-24 | "Source disabled. Habitat context is not a closure." |
| `mvum_roads` | `roads` | **54** | all 13 properties 54/54: `access_status` `designated_open` 51, `restricted` 3 (all three "outside_designated_vehicle_season"); `road_conditions` = `unknown` 54/54; `camping_permission` = `unknown` 54/54; `vehicle_class` `highway_legal` 37, `all_vehicles` 17; maintenance level 5 ×21, 2 ×19, 3 ×12, 4 ×2; three vehicle designations per road with `dates_open` | "Published motor-vehicle designations. Not current passability, snow status or overnight permission." |

Place lists:

| List | Records | Fields and completeness | Limitation sentence |
|---|---:|---|---|
| `overnight_options` | **5** (3 campgrounds, 1 dispersed area, 1 lodge) | `source`, `mapSource`, `locationBasis`, `note`, `unknowns`, `checked_on` (all 2026-09-24) 5/5; `ridb_facility_id` 4/5; `access` (an MVUM designation) 3/5; `stay_limit_days` 1/5 (Lincoln Creek, 5); `requires_high_clearance` 1/5; `tent_only` 1/5. **No `camping_permission` field at all.** | "Hand-researched listings with per-record source links. Listing a place does not confirm permission, operation or availability." |
| `ridb_options` | **4** campgrounds (6 raw, 2 excluded by name) | `camping_permission` = `unknown` 4/4; `needs_review` = true 4/4; six `facts`, every one `{"status":"unknown"}`; `source_is_search` = true 4/4 (the link is a Recreation.gov search, not a facility page) | "Facility inventory only. No availability, operating dates or vehicle-sleeping permission." |
| `destinations` | **4** ski bases | orientation only | "Orientation points only; not reviewed arrival or parking points." |

Rules: one record in `pipeline/config/rules-registry.json`, `lincoln-creek-listed-sites` — stay limit 5 days, high clearance required, `camping_permission: "unknown"`, `last_confirmed_at` 2026-09-25, `max_age_hours` 720. Its review age runs out on about 2026-10-25. `[READ IN REPO]` for the fields, `[INFERENCE]` for the date arithmetic.

`fact_coverage` (Aspen): `camping_permission` `none` — "No camping permission is confirmed anywhere in this region. No listed facility, research area or rule record asserts it; wherever the field is present its value is unknown. A listing shows that a facility exists, not that a given setup may stay." `public_access` `none`. `closures` `none`, citing the Pitkin page and the Aspen occupancy order URL. `restrictions` `reviewed_partial` — one rule record.

### 2.2 Aspen — what a user is told

Read from `v2/explore/capabilities.js`, `v2/trip-rules.js`, `v2/trust.js`, `v2/explore/evidence.js`, and by running the evaluation functions read-only under Node with today's date.

- Layer drawer, always: "Colors explain what the map can tell you; they do not prove a place is legal to camp."
- Legend for the 51 polygons: "Computer-screened research areas — not campsites". Layer title: "Areas to research". Detail: "No campsite or camping permission has been confirmed. Screening snapshot: 2026-09-25–2026-09-26 (high clearance). This is not an assessment of your selected trip."
- Results sheet header: "6 sourced places · N trip conflicts" (5 curated plus Silver Queen from RIDB after de-duplication by facility ID). "What has been checked?" contains: "No confirmed vehicle overnights yet."; "Current fire restrictions have not been confirmed. Check official notices."; "Wildlife closures and special orders are not fully verified for this trip."; "RIDB inventory may be outdated. Open the official listing to confirm."
- Footer of the list: "Availability is not checked."
- Per place, a label and a note computed by `trip-rules.js`. With the configured default trip (2027-01-15 to 2027-01-17, passenger car):

| Place | Status | Label shown |
|---|---|---|
| Difficult Campground | excluded | "Outside mapped vehicle-access season" |
| Silver Bar Campground | excluded | "Tent-only · vehicle-sleeping mismatch" |
| Silver Bell Campground | excluded | "Outside mapped vehicle-access season" |
| Lincoln Creek dispersed camping area | excluded | "High clearance required" |
| St. Moritz Lodge | review | "Room backup · check availability" — "This is not permission to sleep in the parking lot." |
| Silver Queen Campground | review | "Source review is stale" |

  For a July trip in a high-clearance vehicle the campgrounds read "Needs trip review" with "Within the mapped campground-road designation. Full approach, current conditions, sleeping setup, operating dates and availability still need confirmation.", and Lincoln Creek reads "Dispersed area · access unverified".

**What the app tells a user about whether they may camp: nothing affirmative, anywhere.** The strongest positive statement is "Within the mapped campground-road designation", which is about a road. `[READ IN REPO]`

**Hard-coded camping-rule behaviour that exists today** (the ROADMAP's "eliminate inappropriate hard-coded camping-rule behavior"): `[READ IN REPO]`

1. `trip-rules.js` compares trip length with `stay_limit_days` and returns "Stay exceeds published limit".
2. `trip-rules.js` treats `tent_only` as a conflict for every trip, because it assumes the visitor sleeps in a vehicle.
3. `trip-rules.js` turns `requires_high_clearance` plus a passenger car into an exclusion.
4. `trip-rules.js` compares trip days with MVUM `dates_open` for one road segment per place.
5. `pipeline/config/legal_rules.yaml` fixes a 300 ft road buffer and a 100 ft water setback for the corridor builder. Neither distance is tied to a cited order. The current White River order (section 2.4) sets 100 feet from water **and from National Forest System trails**; the builder subtracts water and wilderness only. `[READ IN REPO]` and `[READ ON WEB (not coordinator verified)]`
6. `07_build_dispersed_corridors.py` can subtract manual restriction polygons from `restrictions.geojson`; none is supplied, so the evidence note records "Orders coverage remains incomplete." `[READ IN REPO]`

All six restrict or caution; none grants. Under staleness, `trip-rules.js` keeps an exclusion and adds a recheck note; it does not drop it. `[READ IN REPO]`

### 2.3 Douglas County

- `recreation` layer: **36** USFS recreation-site points. `site_type`: TRAILHEAD 17, CAMPGROUND 5, PICNIC SITE 5, RECREATION RESIDENCE 3, and one each of HORSE CAMP, TARGET RANGE, DOCUMENTARY SITE, OBSERVATION SITE, FISHING SITE, DAY USE AREA.
- Completeness: `seasonal_operational_status` 36/36 (OPEN 35, CLOSED 1); `activity_type_list` 36/36 but "No Data" on 27; `restrictions` prose 16/36; `open_season` 12/36, several dated 2021 ("May 28, 2021"); `water_availability` and `restroom_availability` 19/36; `usda_portal_url` 20/36; `rec1stop_url` 4/36; `important_info` 5/36; `fee_description` 1/36. No `camping_permission` field. `verification_method` = `source_fetch`, `last_verified` = null on all.
- Limitation sentence: "Recreation-site inventory. Season and operational attributes can be historical; no live open status."
- The `restrictions` prose already contains overnight rules, as source text: "You must be in a designated campground to stay overnight" (Osprey, Ouzel); "Overnight use prohibited." (two picnic sites); "Parking and camping in designated sites only." (Indian Creek Equestrian trailhead); "Camping is NOT ALLOWED behind a LOCKED GATE." (four sites). These are held as an undifferentiated string, not as claims.
- `extras.js` adds one hand-written record with null geometry, "Rampart Range designated dispersed camping": "Numbered designated sites only; fee required. The official listing describes a December 1–April 1 camping closure, with weather-dependent reopening. Check the listing for current rules and availability."
- What a user is told (`v2/explore/browse.js`): a "Camping" list of 5 campgrounds plus that area; summary "… 5 campgrounds · 17 trailheads. Closures unconfirmed."; on each campground the source prose under "Published restrictions", "Published season (may be historical)", and then: "Stay limits, live availability and vehicle suitability are not verified." On the area: "Area listing only: individual campsites and access points have not been mapped."
- `fact_coverage.camping_permission`: `none` — "No camping permission is confirmed. A recreation-site record shows that a facility is listed, not that it is open or that a given setup may stay." `closures`: `none`, with a link to the county sheriff's fire page. No fire layer.
- The detail renderer in `browse.js` returns early for site types other than CAMPGROUND, TRAILHEAD and DISPERSED_AREA, so "Overnight use prohibited." on the two picnic sites appears not to reach that panel. `[INFERENCE]` from reading the code; not run in a browser.

### 2.4 RIDB and the API key

`[READ IN REPO]`

- `04_fetch_campgrounds_ridb.py` reads `RIDB_API_KEY` from the environment, sends it as an `apikey` request header to `/facilities` (centre of the extent, radius 35, activity 9), and raises `MissingCredentials` when it is absent. It keeps only facilities whose name contains "campground" and not "picnic", "amphitheatre" or "day use". It reads `Reservable` and `FacilityReservationURL`; it sets `availability: "unknown"`, `winter_access: "unknown"`, `camping_permission: "unknown"`.
- `check_ridb.py` ("Never logs API keys") runs the same fetch in a separate workflow (`.github/workflows/ridb-check.yml`) and writes `v2/ridb-options.json`. `refresh-map.yml` passes the secret to the main pipeline. The key is referenced only as `${{ secrets.RIDB_API_KEY }}` and `os.environ`. No key value is in the repository.
- The published bundle was built without the key, so `lodging_developed` is empty, while `ridb-options.json` (built by the other workflow on 2026-09-25) holds four campgrounds. The two RIDB-derived artifacts disagree about whether RIDB inventory exists. `[READ IN REPO]`

---

## 3. The question decomposed

"Can I stay overnight here?" is eight separate questions. A value in one never implies a value in another (trust principle 3).

| Layer | What it means | Best source | Data, or prose / orders? | How fresh | What we hold today | What it can never establish |
|---|---|---|---|---|---|---|
| **EXISTENCE** | A source lists a campground, a designated site or a named camping area. | USFS recreation-site services (`EDW_RecInfraRecreationSites_02`, `EDW_RecreationOpportunities_01`); RIDB facilities and campsites; CPW GIS. `[READ ON WEB (not coordinator verified)]` that these services are listed in the EDW directory and the RIDB schema; `[HERMES]` for CPW GIS. | **Data.** Points, with attribute tables. Individual designated dispersed sites are **not** in any dataset read: Lincoln Creek's 22 sites and Rampart's numbered sites exist as a count in prose. `[READ ON WEB (not coordinator verified)]` for the prose; `[UNKNOWN]` whether a site-level dataset exists. | Recreation Opportunities described as refreshed nightly `[HERMES]`. Page dates seen: Lincoln Creek "Last updated June 1, 2026" while still carrying a "summer 2024" condition note `[READ ON WEB (not coordinator verified)]`. | Aspen: 5 curated + 4 RIDB places; `lodging_developed` empty. Douglas: 36 sites, 5 campgrounds, 1 horse camp, 1 hand-written area. `[READ IN REPO]` | Permission, operation, season, vacancy, or that the listed thing is where the point is. Existence is the weakest evidence concept. |
| **OWNERSHIP** | Who holds title to the ground at the spot. | County parcels; Colorado Public Parcel Composite; BLM surface-management polygons. `[HERMES]` | **Data**, at two very different precisions: limited-scale agency polygons, and parcels. | SMA and parcel refresh cadence `[UNKNOWN]`. | Aspen 3 and Douglas 5 limited-scale polygons, `spatial_precision: generalized`. No parcels. `[READ IN REPO]` | Access, permission, or which side of a line a spot is on. The South Platte prose warns "Much of the property along the river is privately owned." `[READ IN REPO]` |
| **MANAGEMENT** | Which agency and which unit (forest, ranger district, park) administers the ground and therefore issues the rules. | Agency unit boundaries; the order text names its own unit. `[INFERENCE]` | **Data** for forest and district boundaries `[UNKNOWN]` — not checked; **prose** inside each order ("all National Forest System (NFS) lands within the White River National Forest") `[READ ON WEB (not coordinator verified)]`. | Slow-changing `[INFERENCE]`. | The `manager` code on the generalized polygons only. No ranger-district attribute. `[READ IN REPO]` | That the unit's rules allow anything. Management tells you whose rules to read, nothing more. |
| **CAMPING RULE** | What the managing agency states about camping at this site, along this corridor, in this area, or across the unit: allowed with conditions, designated sites only, prohibited, stay limit, setbacks. | Forest orders on the forest alerts page; ranger-district and recreation-area pages; BLM and CPW rule pages. | **Prose and orders only.** Order text is HTML; the "Described Area" is a PDF map exhibit. No dataset of camping rules or of order geometry was found. `[READ ON WEB (not coordinator verified)]` for the four orders read; `[UNKNOWN]` whether a GIS layer of order areas exists. | Each order carries its own dates: WRNF 2024-01 to 2027-12-31; Aspen 2025-07 to 2028-12-31; WRNF 2026-13 to 2028-12-31; Pike occupancy order to **2026-12-01**; two orders from 1993 and 1996 with no end date. `[READ ON WEB (not coordinator verified)]` | One rule record (Lincoln Creek). Sixteen strings of source prose in Douglas. Two order URLs cited in config, both marked as needing review. `[READ IN REPO]` | Vacancy, physical reachability, or that a rule read last month has not been superseded. An order page lists what is prohibited; it never lists what is allowed. |
| **ACCESS** | Whether the public may lawfully reach the spot: a public road or trail all the way, no private crossing, no gate or closure order. | MVUM for the motor-vehicle designation of forest roads; closure orders; county road records. | **Data** for MVUM designation; **prose / orders** for closures; **nothing** for easements across private land. `[READ ON WEB (not coordinator verified)]` for MVUM; `[UNKNOWN]` for easements. | MVUM "published and refreshed on a unit by unit basis as needed" `[READ ON WEB (not coordinator verified)]`. | 54 Aspen MVUM segments with designations; 73 Douglas road geometries with no designation evaluated. `public_access` is `none` in both regions. `[READ IN REPO]` | Passability, snow, a locked gate on the day, or lawful approach beyond the mapped segment. |
| **VEHICLE FEASIBILITY** | Whether this vehicle can be driven there and may occupy the site: designation by vehicle class, clearance, length, trailer. | MVUM vehicle-class fields and `operationalmaintlevel`; campground pages for length limits; CDOT for the 35-foot Independence Pass limit. `[READ ON WEB (not coordinator verified)]` for the MVUM fields; `[HERMES]` for CDOT. | **Data** for designation and maintenance level (60 fields on the roads layer, with `*_datesopen` per class); **prose** for site length limits ("Max RV 20" inside a Douglas restrictions string). `[READ ON WEB (not coordinator verified)]`, `[READ IN REPO]` | As MVUM. | Aspen: three vehicle classes per road, maintenance level 54/54. Douglas: none evaluated. One `requires_high_clearance` flag. `[READ IN REPO]` | That the visitor's actual vehicle fits, turns round or clears. Designation is a legal class, not a road condition. |
| **SEASONAL STATUS** | Whether the site, road or area is in its operating or open season, and whether a seasonal or wildlife closure applies. | MVUM `*_datesopen`; campground and recreation-area pages; seasonal and wildlife closure orders. | **Data** for MVUM dates; **prose** for campground seasons ("Mid-May to December 1"); **orders** for mud-season and wildlife closures. `[READ ON WEB (not coordinator verified)]` | Prose seasons are targets and state they are weather dependent ("weather conditions may delay opening until late May"). `[READ ON WEB (not coordinator verified)]` | MVUM dates on 54 Aspen roads; `open_season` strings on 12 Douglas sites, several from 2021; `seasonal_operational_status` on 36, not presented as current. `[READ IN REPO]` | That it is open today. A season is a plan; the gate is a fact nobody publishes. |
| **RESERVATION / AVAILABILITY** | Whether a reservation is required, where it is made, and whether a site is free on the night. | Recreation.gov and CPWShop booking pages. | **Data** for "is reservable" and the booking URL (RIDB `Reservable`, `FacilityReservationURL`). **Nothing** for availability: the public RIDB schema has 63 paths and no availability field or endpoint; its `/reservations` endpoint is a dated report of past bookings. `[READ ON WEB (not coordinator verified)]` | Not applicable. | `reservable` and `reservation_url` are fetched but the layer is empty; four RIDB places link to a Recreation.gov *search*. `availability: "unknown"` is hard-set. `[READ IN REPO]` | Vacancy. First-come sites have no inventory at all: "Campsites are strictly first come, first served." `[READ ON WEB (not coordinator verified)]` |

Fire restrictions are deliberately **not** a ninth row. A fire stage says whether you may have a fire, not whether you may camp. It is a separate, fast-moving restriction that sits beside the camping answer. `[INFERENCE]`

### 3.1 The rules actually found, restrictions first

All `[READ ON WEB (not coordinator verified)]`, read today from the forest's own pages. None of this is a review, and none of it may be written into a claim without the M4 review path.

**White River National Forest, forest-wide**

- Order WRNF 2024-01, in effect 2024-01-01 to 2027-12-31: "Camping within the White River National Forest for more than 14-days with in any continuous 30-day period is prohibited".
- Order 2026-13, in effect 2026-07-01 to 2028-12-31: "Camping, unless in a Forest Service developed recreation site or designated dispersed site, within 100 feet of a body of water … or a National Forest System Trail." Hermes did not report this order.
- Order 1993-06, no end date: developed campgrounds have stay limits — five consecutive days at Silver Bar, Silver Bell, Silver Queen, Difficult, Lincoln Gulch, Portal, Weller and Lostman; three at Maroon Lake (June 19 to Labor Day). Hermes did not report this order.

**Aspen Ranger District**

- Order 2025-07, "Aspen Ranger District Occupancy and Use Prohibitions", in effect 2025-09-01 to 2028-12-31, page last updated 2026-03-05. Prohibited in the Described Areas: "Camping in Described Areas." The Described Areas include "All NFS lands within ¼ mile of Colorado Highway 82 beginning and including the Difficult Picnic Area and ending at Independence Pass Summit", the Castle Creek, Pearl Pass, Conundrum Creek, Maroon Valley, Lincoln Creek and Hunter Creek corridors, a quarter mile around Silver Bar, Silver Bell, Silver Queen, Difficult, Weller, Lostman and Portal campgrounds, Ashcroft, and the four ski-area permit areas.
- Order WRNF 1996-08, no end date: "Camping within 300 feet of a trailhead", with three named exceptions.
- Lincoln Creek recreation page, last updated 2026-06-01: "There are 22 dispersed campsites for car camping along Lincoln Creek Road." "Maximum 5 day stay limit."
- **An unresolved tension.** The HTML text of Order 2025-07 prohibits camping in the Lincoln Creek Corridor without a stated exception for designated sites, while the recreation page lists 22 campsites along the same road. The fire prohibition in the same order does carry the exception "except in campgrounds and dispersed camp sites designated and provided by the Forest Service". Whether the signed PDF, or Exhibit A, exempts the designated sites is `[UNKNOWN]`: the PDFs were not read. This is the first thing an M7 reviewer must resolve, and it is a good example of why a page listing cannot stand alone.

**Pike National Forest — South Platte, South Park and Pikes Peak districts**

- Occupancy and use order, in effect 2024-05-03 to **2026-12-01**: "Camping at any location, within the same 20-mile radius for more than 14 days within any continuous 30-day period." Also prohibited, in the Described Areas shown on exhibits: "Camping, except in Forest Service developed recreation sites or designated dispersed sites." And camping within 100 feet of water outside such sites.
- South Platte Ranger District page, last updated 2026-05-22: "No parking or camping is allowed outside of designated sites." And: "Dispersed camping is not allowed at any time along the South Platte River Corridor (Cheesman Canyon to Foxton Road) or along the Guanella Pass Scenic Byway."
- South Platte River Corridor page, last updated 2026-05-05: "Dispersed camping is prohibited." "Camping is permitted in developed campgrounds only."
- Rampart Range Recreation Area page, last updated 2026-03-27: "Dispersed camping is available in designated sites only for a fee." Roads "are closed annually by December 1".

So designated-dispersed-only areas **are** stated for both pilots: by order near Aspen, and by order plus district prose along the South Platte and Rampart Range.

### 3.2 MVUM and the dispersed-camping attribute

- The national MVUM roads layer (`EDW_MVUM_01/MapServer/1`) has 60 fields. They cover route identity, `symbol`, `seasonal`, `jurisdiction`, `operationalmaintlevel`, `surfacetype`, fifteen vehicle classes each with a `_datesopen` field, three e-bike classes, and administrative fields. **No field names dispersed camping**, a corridor distance or a camping designation. `[READ ON WEB (not coordinator verified)]`
- The layer's symbol classes are six road classes (all vehicles, highway-legal only, special designation; each yearlong or seasonal). None is a camping class. `[READ ON WEB (not coordinator verified)]`
- The EDW service directory lists 145 services. None is named for camping, dispersed use, closures or orders. The camping-relevant ones are `EDW_MVUM_01`, `EDW_MVUM_02`, `EDW_InfraRecreationSites_01`, `EDW_RecInfraRecreationSites_02`, `EDW_RecreationAreaActivities_01` and `EDW_RecreationOpportunities_01`. `[READ ON WEB (not coordinator verified)]`
- The layer warns: "Not every National Forest has data included in this feature class." `[READ ON WEB (not coordinator verified)]`
- The MVUM trails layer and the downloadable geodatabase were not inspected, so whether a dispersed-camping attribute exists anywhere outside the roads layer is `[UNKNOWN]`. The printed MVUM PDFs for the two forests were not read.
- Consequence: the corridor idea in the repository — buffer an MVUM road and call it a research area — has no camping attribute behind it. The buffer is derived from a road designation. `[INFERENCE]`

### 3.3 RIDB

- The OpenAPI document at `ridb.recreation.gov/shared/swagger/ridb.yaml` loads without a key. 63 paths: organizations, recareas, facilities, campsites, permit entrances, tours, activities, attributes, zones, events, links, media, addresses, and `/reservations`. `[READ ON WEB (not coordinator verified)]`
- The word "availability" does not appear in the schema; "available" appears once, inside an example facility description. No endpoint returns open or booked nights. `[READ ON WEB (not coordinator verified)]`
- `/reservations` "Retrieves all reservations matching given dates" and returns a `Reservation` schema of historical order fields (`HistoricalReservationID`, `StartDate`, `EndDate`, `Nights`, `EquipmentLength`, fee fields). It is a booking report, not a vacancy feed. Whether it is usable for anything in M7, and under what terms, is `[UNKNOWN]`.
- Facility fields relevant to M7: `Reservable` ("Whether the Facility is reservable"), `Enabled`, `StayLimit` (free text, up to 500 characters), `FacilityUseFeeDescription`. Campsite fields: `CampsiteType`, `TypeOfUse` (Overnight / Day), `Loop`, `CampsiteAccessible`, coordinates. `[READ ON WEB (not coordinator verified)]`
- Rate limit, stated per endpoint: "Rate Limit is set to 50 request/second." Authentication is an `Apikey` scheme. `[READ ON WEB (not coordinator verified)]`
- **API terms: not verified.** `ridb.recreation.gov/access-agreement-ridb` returned a 3.6 kB JavaScript shell with no agreement text. Hermes's summary (non-exclusive, non-transferable, revocable, "AS IS", right to impose limits or fees, attribution requested) came from a search index and stays `[HERMES]`. Whether a static site may publish a stored copy of facility records is `[UNKNOWN]` until a person reads the agreement in a browser.

### 3.4 Fire-restriction stages

| Jurisdiction | Where the stage is published | What it said today |
|---|---|---|
| Unincorporated Douglas County | `dcsheriff.net/…/fire-restrictions/` — one stable page with a dated banner | "updated on 9/17/2026"; "STAGE 1 FIRE RESTRICTIONS HAVE BEEN LIFTED FOR UNINCORPORATED DOUGLAS COUNTY, COLORADO" `[READ ON WEB (not coordinator verified)]` |
| Pitkin County | A dated press release in the county news list. `pitkincounty.com/CivicAlerts.asp`, the URL the pipeline hashes, redirects to `/m/newsflash`, the general news index. The release itself points readers to PitkinEmergency.com. | Posted 2026-09-28: "Pitkin County has officially lifted Stage 1 Fire Restrictions" (release dated Sept. 24, 2026) `[READ ON WEB (not coordinator verified)]` |
| White River National Forest | A dated alert on the forest alerts page, with a "Fire Restriction" alert-type filter | "The White River National Forest will lift fire restrictions beginning Friday, Sept. 25." Order 2026-21 `[READ ON WEB (not coordinator verified)]` |
| Pike-San Isabel | Forest alerts page ("search for fire restrictions") and a fire-danger banner by district | South Platte fire danger "Moderate". Fire danger is not a restriction stage. Whether a PSICC fire order is in force is `[UNKNOWN]`; the PSICC alerts index was not fetched. |

Three observations:

1. No machine-readable stage exists in any of the four. Each is a sentence on a page. `[READ ON WEB (not coordinator verified)]` for these four pages; a statewide feed remains `[UNKNOWN]` (Hermes found none).
2. The Pitkin monitor hashes a general news index. It changes whenever the county posts anything — the top item today is an airport grant. A changed hash therefore says almost nothing about fire. `[READ ON WEB (not coordinator verified)]` for the redirect and the page content, `[INFERENCE]` for the consequence.
3. The White River alert that announces the lifting is titled as a lifting but still attaches the Stage 1 order PDF and map, with "Alert End Date: N/A" and start date September 10. A scraper keyed on "Stage 1" would read it as a restriction in force. `[READ ON WEB (not coordinator verified)]` for the page, `[INFERENCE]` for the trap.

---

## 4. Draft claim model for overnight use

This extends the M4 model (`docs/specs/M4-functional-recreational-water.md` section 9). It introduces no new status vocabulary and no new evidence object. Everything in this section is `[INFERENCE]` — a proposal for the owner, not a decision.

### 4.1 What is kept from M4, unchanged

- Statuses: `unknown`, `allowed`, `restricted`, `prohibited`, with M4's definitions. `allowed` means the source states the activity is offered with no condition beyond general law; `restricted` means allowed only with conditions specific to the place; `prohibited` means the source states it is not allowed; `unknown` means nothing reviewed establishes any of these.
- Evidence object: `source_url` on the agency's or operator's own site, `agency`, `basis: "manual_review"`, `last_checked_at`, `last_confirmed_at`, positive `max_age_hours`, `effective_from`, `effective_to`, and a reviewer-written `summary` of at most 160 characters.
- A claim with status `unknown` has no other key. Absence of a record means unknown.
- Freshness is computed in the browser, never stored, with M4's table:

| Stored status | Within policy | Past policy |
|---|---|---|
| `allowed` | Shown as allowed | Shown as not established, with the last-reviewed date |
| `restricted` | Shown as restricted | Still shown as restricted, flagged "Review overdue" |
| `prohibited` | Shown as prohibited | Still shown as prohibited, flagged "Review overdue" |
| `unknown` | Not established | Not established |

- Forbidden sources for a claim: a facility dataset, a designation dataset, a map layer, a community site, another claim. For M7 this explicitly includes RIDB, the USFS recreation-site services, MVUM and any ownership layer. They supply existence and designation, never a claim.
- A Hermes retrieval, and the agent verification in this document, are not reviews.
- Community signals cannot set a claim. M4 section 4 rule 3 already names "camping legality".

### 4.2 What M7 adds

**A. One registry per region** — for example `v2/regions/<id>/overnight.json`, hand-curated and validated like `water-recreation.json`. It holds two record kinds: **place records** and **rule records**.

**B. `scope` on every record.** Exactly one of:

| Scope | Subject | Geometry | Highest status it may carry |
|---|---|---|---|
| `site` | One developed campground, or one agency-listed designated dispersed site or group of sites | A point with a stated `location_basis` | `allowed` |
| `corridor` | A road- or trail-defined strip the agency describes in words | None, or reviewed and labelled generalized | `restricted` |
| `area` | A named recreation area, scenic area or order "Described Area" | None, or reviewed and labelled generalized | `restricted` |
| `default_rule` | A rule the agency states for a whole unit: forest, district, state-park system, BLM Colorado | None. Identified by the unit's name | `restricted` |

`prohibited` is available at every scope. `allowed` is available only at `site`. A corridor, an area or a unit can therefore be shown as "designated sites only" or "prohibited", never as "camping allowed along here". That is what keeps a corridor from becoming blanket permission — the mistake the existing rule record already guards against in prose ("not blanket permission along the road").

**C. Overnight modes instead of M4's four activities.** A proposal of three, each present in every place record and each with its own evidence:

- `tent` — camping in a tent at the place;
- `vehicle` — sleeping in or on a passenger vehicle, van or truck at the place;
- `rv_trailer` — a motorhome or towed unit.

No mode is inferred from another. A tent-only listing gives `tent: allowed` and `vehicle: prohibited` or `unknown` depending on what the page says; it does not give "camping allowed". Whether to model three modes or one is owner decision O3.

**D. Conditions on a claim.** An optional, closed set of structured condition fields beside the summary, each of which must be supported by the same evidence: `stay_limit_days`, `reservation_required` (true / false / not stated), `fee_stated` (boolean), `max_vehicle_length_ft`, `high_clearance_stated` (boolean), `season_text` (a verbatim date phrase). A condition makes the status at most `restricted`. Conditions are data for filtering; they never produce "allowed".

**E. Order identity on rule records.** A rule record adds `order_number`, `issuing_unit`, `order_effective_from`, `order_effective_to` and `exhibit_urls`. The order's own dates are facts about the order and are distinct from the review dates. Two clocks run:

- the review clock (`last_confirmed_at` + `max_age_hours`), exactly as in M4;
- the order clock (`order_effective_to`).

When the order clock runs out and nobody has re-reviewed, the record is **not dropped and not weakened**. It stays shown with its status, flagged "Order end date passed — review overdue". Forest orders are routinely reissued; the Pike occupancy order ends 2026-12-01 and its successor cannot be assumed either way. Whether an expired order should keep displaying is owner decision O6.

**F. Attachment of a default rule to a place.** A `default_rule` attaches only by one of two reviewed routes, never by geometry alone:

1. **Explicit link.** The rule record lists `place_ids`, as the existing rules registry does. The reviewer has read that the place is inside the unit.
2. **Unit panel.** With no link, the rule appears only in a region-level panel headed by the unit's name — "Rules published for White River National Forest" — and is not attached to any map location.

It is not attached by intersecting a point with the generalized management polygons. Those polygons are limited-scale and the product already says they "cannot … tell you whether a specific spot is inside this area". Whether a parcel-precision boundary from M5 may later drive attachment is owner decision O5.

**G. A default rule never implies the place is campable.** Three mechanical guards:

1. A `default_rule` record has no `allowed` status and no mode claims. It carries a limit, not a permission.
2. Attaching a default rule does not change any mode claim on the place. A place with `tent: unknown` and an attached 14-day limit still reads "Not established" for tents.
3. The display sentence for a default rule is conditional and ends with a fixed disclaimer (section 5, string OV6).

**H. Precedence.** For one place and one mode, evaluated in this order, and before freshness can soften anything:

1. Any applicable `prohibited` at any scope → **Prohibited**.
2. Otherwise any applicable `restricted` at any scope → **Restricted**, listing every restriction.
3. Otherwise a `site` claim of `allowed`, within its review age → **Allowed**.
4. Otherwise → **Not established**.

An area order therefore overrides a site listing. The only way a site-level positive claim survives inside an order's Described Area is an explicit `exempted_by` on the site record that cites the sentence in the order itself which exempts developed or designated sites, reviewed on the same date as the order. A recreation page cannot exempt a place from an order. Until Lincoln Creek's tension (section 3.1) is resolved in the signed order, its sites would read **Prohibited — review needed** or **Not established**, not Allowed. Which of the two is owner decision O7.

"Applicable" means linked by `place_ids`. An order whose Described Area has not been linked to places appears in the unit panel and on no place.

**I. Proposed review ages** (all positive `max_age_hours`; the reviewer may shorten):

| Record | Proposed maximum age | Why |
|---|---|---|
| `site` claim, developed campground | 2,160 h (90 days), as M4 water | Operating pages change seasonally |
| `site` claim, designated dispersed | 720 h (30 days), as the existing Lincoln Creek rule | Less stable, more enforcement |
| `corridor` / `area` rule from an order | 720 h | Orders are amended without notice |
| `default_rule` from a multi-year order | 2,160 h | Slow-changing, low harm if late because it only restricts |
| Fire stage | 24 h, as today | Changed in all three jurisdictions within the last three weeks |

Past its age, an `allowed` falls to not established; everything else stays and is flagged.

**J. Dates are not evaluated to flip a claim.** As in M4 section 9.4, a seasonal rule is a `restricted` claim whose summary states the season. M7 does not compute "allowed today" from a date range. The existing `trip-rules.js` date and stay-limit comparisons may continue to raise a *conflict* (a restriction-side result) but may never clear one. Whether those comparisons survive at all is owner decision O8.

**K. What stays outside the claim model.**

- **Availability** — never a claim, never a status. A booking link and the word "unknown".
- **Fire stage** — the existing `restriction_monitor` shape (`unknown` / `confirmed`, manual review, 24 h). It is displayed next to the overnight answer and is never an input to it.
- **Vehicle designation** — remains on the road layer. A place record may point at a road ID; the designation is shown as a road fact.
- **Ownership and management** — remain map context. Neither is an input to a mode claim.



> **Verification against origin/main (`bb85785ea98c8d5fb8d5694a36744b4f96a6161a`):** Not a measured repository fact; these are proposed design dimensions. The existing section does not state either item in this wording.

Add to the dimension list (identity, geometry, inventory, setup, permission, operations, restriction,
stay/permit, availability, transport):
- transport: a partial or failed refresh must not publish an inventory that looks complete.
- stay window: the departure day is part of the trip when evaluating restrictions.
Source: Codex reconnaissance at commit 2795625, 2026-10-08; measured facts spot-checked by Hermes
UNVERIFIED whether section 4.2 already says this; the Codex review did not diff the wording.



> **Verification against origin/main (`bb85785ea98c8d5fb8d5694a36744b4f96a6161a`):** Verified: `09_reviewed_sites.py` requires point geometry inside the pilot AOI, ID/name, valid review and operating dates, five named supported claims, a selected vehicle, `sleeping_setup == "inside_vehicle"`, site confirmation, and source evidence. The curation template and script are Aspen-specific.

Current limitation: the curated reviewed-site template and 09_reviewed_sites.py are specific to Aspen
and to vehicle sleeping (inside_vehicle). They are not a general tent / RV / hammock model.
The script requires a real Point, a confirmed site, valid review and operating dates, a compatible
vehicle/sleeping setup, and evidence for five named fields.
Source: Codex reconnaissance at commit 2795625, 2026-10-08; measured facts spot-checked by Hermes
UNVERIFIED: inside_vehicle appears in v2/pipeline/docs/curation.md, but Hermes did not open the script.

### 4.3 Contract touchpoints

`[READ IN REPO]` for what exists; `[INFERENCE]` for the implications.

- The contract's own claim object (5.4) uses `unknown` / `supported` / `restricted`, and the reserved property `camping_permission` allows `unknown` or `supported_for_trip` (only in `reviewed_sites`, which has zero features). M4 section 9.2 rule 8 kept that value set separate from the water registry. An overnight registry on M4's vocabulary creates a second place where camping permission can be expressed. One of them should go: owner decision O4.
- `fact_coverage.camping_permission` would move from `none` to `reviewed_partial` on the M4 pattern, when the registry holds at least one non-unknown claim, with the statement rewritten to say that a small number of places carry reviewed agency statements and everything else is unknown.
- Rule R28 fixes `research_areas` at `camping_permission == "unknown"`. Nothing proposed here changes that.

### 4.4 A sketch, not a schema

```json
{"schema_version": 1,
 "places": [
  {"place_id": "difficult", "scope": "site", "operator": "USDA Forest Service",
   "claims": {
     "tent":       {"status": "unknown"},
     "vehicle":    {"status": "unknown"},
     "rv_trailer": {"status": "unknown"}},
   "notes": []}],
 "rules": [
  {"id": "wrnf-2024-01-stay-limit", "scope": "default_rule",
   "issuing_unit": "White River National Forest", "order_number": "WRNF 2024-01",
   "status": "restricted", "conditions": {"stay_limit_days": 14},
   "order_effective_from": "2024-01-01", "order_effective_to": "2027-12-31",
   "place_ids": [],
   "evidence": {"source_url": "https://www.fs.usda.gov/r02/whiteriver/alerts/camping-stay-limitations", "agency": "USDA Forest Service", "basis": "manual_review", "last_checked_at": null, "last_confirmed_at": null, "max_age_hours": 2160, "summary": "…"}}]}
```

The null review dates are deliberate. Nothing in this document is a review, so this sketch is not a valid record.

---

## 5. Display rules

Everything here is `[INFERENCE]`: proposed wording for owner approval, following M4 section 10. None of the strings contains "verified", "legal", "permitted" or "open to". A status word is never shown without its mode.

### 5.1 When only EXISTENCE and MANAGEMENT are known

This is the state of every place in both regions today. What may be said:

- that a named source lists the place, and when the record was fetched;
- which agency the source names as managing it;
- the source's own facts, labelled as the source's;
- that camping, access, season and availability are not established;
- where to check.

Proposed fixed strings:

| ID | String | When |
|---|---|---|
| OV1 | `Listed by the source. Whether you may stay here overnight is not established.` | A place with no registry record, or with all modes unknown |
| OV2 | `A listed campground or mapped area is not permission to camp, park overnight or sleep in a vehicle.` | Last line of every overnight detail, whatever its claims |
| OV3 | `Not established` | After a mode label when the claim is unknown, or `allowed` and past its review age |
| OV4 | `Availability is not known. Ohvernight does not check whether a site is free.` | Every overnight detail |
| OV5 | `Managed by <agency>, according to the source. Management does not establish that camping is allowed.` | When a management attribute is shown |
| OV6 | `If you camp anywhere on <unit>: <reviewer summary>. This is a limit. It does not say camping is allowed at this place.` | A default rule shown on a place or in the unit panel |
| OV7 | `Order end date passed — review overdue` | A rule whose order end date has passed without re-review |
| OV8 | `Fire restrictions are separate from camping rules and change quickly. Not confirmed here.` | Beside every overnight detail while the fire stage is unknown or stale |
| OV9 | `Computer-drawn strip beside a mapped road. It is not a campsite, not a designated camping area and not a statement that camping is allowed.` | Any computed research area, if the layer survives (O1) |

Example, Difficult Campground today:

> **Difficult Campground**
> From the source: Recreation.gov facility 231880. Source fetched 2026-09-25.
> Listed by the source. Whether you may stay here overnight is not established.
> Tent: Not established. Vehicle: Not established. RV or trailer: Not established.
> Availability is not known. Ohvernight does not check whether a site is free.
> A listed campground or mapped area is not permission to camp, park overnight or sleep in a vehicle.

Example, a reviewed prohibition (illustrative; no such record exists):

> Vehicle: Prohibited. Walk-in tent sites only. USDA Forest Service. Reviewed 2026-11-02.

Example, a default rule in the unit panel (illustrative):

> If you camp anywhere on White River National Forest: no more than 14 days in any 30-day period (Order WRNF 2024-01). This is a limit. It does not say camping is allowed at this place.

### 5.2 Ordering inside a detail

Restrictions first. Prohibitions, then restrictions, then default rules, then "From the source", then anything computed. A place with any prohibition never leads with its amenities.

### 5.3 What must never be said

1. "Camping allowed", "you can camp here", "free camping", "open", "available", "legal", "permitted", "verified", or any tick, green fill or badge with that meaning, on any record without a within-age `site` claim of `allowed`.
2. Anything affirmative at corridor, area or unit scope: no "dispersed camping along this road", no "camping corridor", no "public land — camping OK".
3. "Dispersed camping" as the name of a computed polygon. The Forest Service uses the words for designated places; a buffer is not one.
4. "No restrictions", "no closures", "no fire ban", or silence that reads as any of these. The absence of a loaded order is unknown.
5. "Open" or "in season" computed from a date range, an MVUM designation or a recreation-site status field.
6. "Sites available", "usually has space", "first come — you'll find a spot", or any occupancy language.
7. A stay limit, fee or season presented without its source and review date, or presented as the reason a place is suitable.
8. "Within the 14-day limit" as a positive result. Passing a limit check is not a finding that the stay is allowed.
9. Any ranking, default sort or map emphasis that puts an unknown place above a reviewed one, or a computed area above a listed facility, in a way that reads as a recommendation.
10. A community report as a reason to camp.

Two strings shipping today sit close to these lines and deserve an owner look in M7, not before: "Within the mapped campground-road designation." (a road fact placed where a camping answer is expected), and the layer title "Areas to research" on polygons that overlap closed ground. `[READ IN REPO]` that the strings ship; `[INFERENCE]` that they are close to the line.

---

## 6. What cannot be known from published data today

1. **Whether a site is free tonight.** No public availability field in RIDB `[READ ON WEB (not coordinator verified)]`; no CPWShop feed found `[HERMES]`; first-come sites have no inventory at all, and the district says "We have no way of knowing real time availability." `[READ ON WEB (not coordinator verified)]`
2. **Where the designated dispersed sites are.** Twenty-two at Lincoln Creek and the numbered Rampart sites exist as a count and a sign convention ("posted with a sign indicating 'P' for parking and a tent symbol"), not as coordinates. `[READ ON WEB (not coordinator verified)]` for the prose; a site-level dataset is `[UNKNOWN]`.
3. **The boundary of an order's Described Area as geometry.** It is a PDF map exhibit plus a sentence such as "within ¼ mile of". `[READ ON WEB (not coordinator verified)]` A quarter-mile buffer of a county road centreline would be our computation, not the agency's line. `[INFERENCE]`
4. **Whether a given spot is inside the forest at all.** The management polygons held are limited-scale. `[READ IN REPO]`
5. **Whether an order read last month still stands.** Orders end, are rescinded and are reissued; only the page says so, on the day. The Pike order ends 2026-12-01. `[READ ON WEB (not coordinator verified)]`
6. **Whether a road designated open is passable, gated or under snow.** MVUM is a designation. `[READ ON WEB (not coordinator verified)]`
7. **Whether the approach crosses private land.** No easement or access dataset is held or was found. `[UNKNOWN]`
8. **Whether the visitor's vehicle fits.** Length limits are prose where they exist at all. `[READ IN REPO]`
9. **Whether a campground is operating today.** Seasons are targets and "weather dependent"; the `seasonal_operational_status` field in the recreation-site service reads OPEN on 35 of 36 Douglas sites in a snapshot whose season fields include 2021 dates. `[READ IN REPO]`
10. **The current fire stage, mechanically.** Published as sentences on four different pages in four different forms. `[READ ON WEB (not coordinator verified)]`
11. **Wilderness overnight permits, quotas and zone rules** for the Maroon Bells–Snowmass area. An order page exists in the alerts index; it was not read. `[UNKNOWN]`
12. **Whether sleeping in a vehicle counts as camping at a trailhead or pull-out** under the Forest Service orders. BLM Colorado's definition includes parking a vehicle "for apparent overnight occupancy" `[HERMES]`; the Forest Service position was not read. `[UNKNOWN]`
13. **Anything about BLM or state-trust parcels in the two pilots.** No parcel-specific source was retrieved. `[HERMES]`, `[UNKNOWN]`

---

## 7. Candidate M7 scopes

All `[INFERENCE]`. Cost is given in reviewable pull requests and in recurring human review, because recurring review is the real cost of any overnight claim.

### Small — "Say less, say it correctly"

- Remove or re-word the 51 computed research areas (O1). Retire the six hard-coded behaviours, or reduce them to conflict notes (O8).
- Add the unit panel with reviewed default rules: about six records (WRNF stay limit, WRNF 100-foot rule, WRNF campground stay limits, Aspen trailhead rule, Pike stay limit, Pike water setback).
- Add reviewed **prohibitions and designated-only rules** as area and corridor rule records without geometry: Aspen Order 2025-07, South Platte River Corridor, Rampart Range, South Platte front-country.
- No `allowed` claim anywhere. No new geometry. Fix the Pitkin monitor's target or retire it.
- Fixed strings OV1–OV9.
- Cost: 3 pull requests (wording and removal; registry and validator; display). About 10 rule records to review once, then roughly 10 page reads every 30 to 90 days. Lowest trust risk: every record restricts.

### Medium — "Reviewed campgrounds"

- Everything in Small.
- Place records with mode claims for the listed developed campgrounds: about 9 near Aspen (Difficult, Silver Bar, Silver Bell, Silver Queen, Weller, Lostman, Lincoln Gulch, Portal, Maroon Lake) and 6 in Douglas (Osprey, Ouzel, Devils Head, Indian Creek, Indian Creek Equestrian, Flat Rocks) — up to 45 mode claims, many of which will stay unknown.
- Designated dispersed areas as `site` records at area precision: Lincoln Creek (after the order tension is resolved) and Rampart Range.
- One inventory path for RIDB instead of two; a booking link per place; availability fixed at unknown.
- Explicit links from each place to the default rules and orders that apply to it.
- Cost: 5 to 6 pull requests. About 15 place dossiers plus the 10 rules, re-read on a 30- to 90-day cycle — on the order of 100 page reads a year. Introduces the first `allowed` claims, so it needs the precedence tests in section 11.

### Large — "Order geometry and dispersed"

- Everything in Medium.
- Digitized Described Areas from order exhibits, labelled generalized, used to attach orders to places and to mask ground.
- Any treatment of dispersed camping outside designated sites. In both pilots the published position is restrictive: designated sites only near the roads people drive. A positive dispersed claim would need a source that states where it is allowed, and none was found. `[UNKNOWN]` whether one exists.
- Vehicle and trip filtering built on reviewed conditions rather than on hard-coded checks.
- Cost: 9 or more pull requests, a digitizing method that needs its own trust review, and geometry that must be re-checked every time an order is reissued. Depends on M5 for any precise boundary. Highest risk: a drawn order boundary invites "outside the line means allowed".

---

## 8. Owner decisions

Each with a one-line recommendation. All recommendations are `[INFERENCE]`.

| # | Decision | Recommendation |
|---|---|---|
| O1 | Keep, re-word or remove the 51 computed "Areas to research" polygons? | Remove from the map in M7; they have no camping source behind them and overlap ground a current order closes. |
| O2 | Which scope: small, medium or large? | Small first, as its own releasable slice; medium only after it has run one full review cycle. |
| O3 | Model three overnight modes (tent, vehicle, RV or trailer) or one? | Three; "tent-only" and vehicle-sleeping are where people actually get moved on. |
| O4 | Keep the contract's `camping_permission: supported_for_trip` and `supported` vocabulary beside the M4 statuses? | Retire `supported_for_trip` in M7 so there is one place and one vocabulary for an overnight claim. |
| O5 | May a default rule attach to a place by geometry? | No. Explicit reviewed link or the unit panel only, until M5 supplies a boundary fit for it. |
| O6 | When an order's end date passes without re-review, keep showing it? | Yes, flagged "Order end date passed — review overdue"; never drop a restriction silently. |
| O7 | Inside an order's Described Area, how does a listed site read before the exemption is confirmed? | "Not established", with the order shown above it as a prohibition for the area. |
| O8 | Do the stay-limit, tent-only, clearance and road-date checks in `trip-rules.js` survive? | Keep only as conflict notes fed by reviewed conditions; delete the unreviewed constants and the vehicle-sleeping assumption. |
| O9 | May `allowed` ever be shown for an overnight mode? | Only at `site` scope, only from the agency's own page for that site, only within review age. |
| O10 | What review ages? | 90 days for campgrounds and multi-year default rules, 30 days for designated dispersed sites and area orders, 24 hours for fire. |
| O11 | Fire stage: keep a monitor, or link only? | Link only in both regions until someone commits to a daily manual review; a page hash of a news index should not ship. |
| O12 | RIDB: one inventory path or two, and may stored records be published? | One path; do not expand RIDB use until a person has read the access agreement in a browser. |
| O13 | Show a booking link where availability is unknown? | Yes, to the facility's own booking page, never a search link, always beside OV4. |
| O14 | Who reviews, and how often can they actually do it? | Decide the reviewer and the cadence before the scope; the cadence sets how many records M7 can hold. |
| O15 | Is dispersed camping outside designated sites in M7 at all? | No. Show the designated-only rules; treat everything else as not established. |
| O16 | Should Douglas's source `restrictions` prose be parsed into claims? | No. Keep it as labelled source text; write claims only from a reviewed page. |

---



> **Verification against origin/main (`bb85785ea98c8d5fb8d5694a36744b4f96a6161a`):** Verified: ADR-005 makes positive claims fail closed without complete reviewed evidence and assigns trust-policy changes to the owner. The exact process requirement for future vocabulary/producer fields is a recommendation in this block, not a current validator rule.

Process rule: setup vocabulary (tent-only, trailer or RV dimensions, high clearance, capacity),
any activity/setup vocabulary, any new fact_coverage policy and any new producer field require a reviewed
amendment to the data contract (ADR-005; v2/pipeline/docs/data-contract.md) before use.
Source: Codex reconnaissance at commit 2795625, 2026-10-08; measured facts spot-checked by Hermes
(Rule follows from the contract; Hermes did not re-read the contract text for this block.)

## 9. Risks and failure modes

How a user is fined, moved on or turned around because of Ohvernight. All `[INFERENCE]` unless marked.

| # | Failure | How we would cause it | Guard |
|---|---|---|---|
| R1 | **Fined for camping in a closed corridor.** A visitor pulls off Highway 82 east of Aspen, inside an "Areas to research" polygon. | The polygon is drawn on ground where Order 2025-07 prohibits camping. A violation "is punishable as a Class B misdemeanor by a fine of not more than $5,000 for individuals" `[READ ON WEB (not coordinator verified)]`. | O1; never draw a computed overnight area; prohibitions shown first. |
| R2 | **Cited at a trailhead.** The visitor sleeps in the car at a trailhead spur. | Five research areas are named after trailhead roads; the 1996 order prohibits camping within 300 feet of a trailhead `[READ ON WEB (not coordinator verified)]`. | Same as R1; trailhead rule in the unit panel. |
| R3 | **Stale "allowed".** A campground claim is reviewed in June; an order or closure lands in August. | Review age too long, or freshness not enforced. | M4 freshness table; `allowed` falls to not established; short ages (O10). |
| R4 | **Silent expiry of a restriction.** The Pike order ends 2026-12-01, the record is dropped, and the map looks clear. | Treating an order end date as the end of the restriction. | O6; staleness never weakens a restriction. |
| R5 | **Default rule read as permission.** "14-day limit" beside a pin reads as "you may camp 14 days here". | Attaching a limit to a place without the disclaimer, or by geometry. | Section 4.2 F and G; string OV6. |
| R6 | **Listing overrides order.** A recreation page lists sites; an order closes the corridor; we show the listing. | Site scope beating area scope. | Precedence rule H; `exempted_by` must cite the order. Lincoln Creek is the live case. |
| R7 | **Turned around at a full campground.** | Any language suggesting space. | Availability never a claim; OV4. |
| R8 | **Turned around at a gate.** Rampart roads close "by December 1"; the visitor arrives on 30 November to a gate shut early. | Computing "open" from a season. | No date evaluation toward open (4.2 J). |
| R9 | **Wrong vehicle.** A 24-foot trailer at a site with "Max RV 20"; a sedan on Lincoln Creek Road. | Length and clearance held as prose or not held. | Conditions only from reviewed evidence; otherwise "not established". |
| R10 | **Fire citation.** We show "restrictions lifted" after they are reinstated. Douglas: up to "a $1000.00 fine" `[READ ON WEB (not coordinator verified)]`. | Any stored fire stage older than a day. | O11; fire never stored without daily review. |
| R11 | **Private land.** A point near the South Platte lands on private ground. | Trusting limited-scale management polygons. | No ownership input to any claim; W3 and W7 wording stays. |
| R12 | **Research passed off as review.** A Hermes or agent retrieval is written into `last_confirmed_at`. Hermes's fire and Aspen-order errors show what that would cost. | Skipping the human read. | M4 section 9.5 rule; validator cannot check it, so pull-request review must. |
| R13 | **Third-party "free camping" expectations.** Users arrive expecting us to match community maps. | Showing less than they do without saying why. | Say plainly that both pilots publish designated-sites-only rules near roads. |
| R14 | **Two RIDB artifacts disagree.** One says inventory unavailable, the other lists four campgrounds `[READ IN REPO]`. | Two pipelines, one key. | O12. |
| R15 | **Review debt.** The registry grows past what one person re-reads; everything goes "review overdue". | Choosing scope before cadence. | O14; small scope first. |

---

## 10. Tests an M7 specification will need

All `[INFERENCE]`.

**Validator, time-independent**

1. A place record has every mode present; a claim with status `unknown` has no other key.
2. Any non-unknown claim has the full evidence object, with `basis: "manual_review"` and a positive `max_age_hours`.
3. `allowed` is rejected at `corridor`, `area` and `default_rule` scope.
4. A `default_rule` record has no mode claims and cannot carry `allowed`.
5. A `source_url` on a non-claim host (ArcGIS services, `ridb.recreation.gov`, `recreation.gov` search URLs, community sites) is rejected.
6. One evidence object referenced by two modes is rejected.
7. A rule record with `order_number` has `order_effective_from`; `order_effective_to` may be null.
8. Every `place_ids` entry resolves; an `exempted_by` cites a rule ID present in the same registry.
9. A condition (`stay_limit_days` and the rest) on a claim forces status at most `restricted`.
10. Research-area features still satisfy R28; no feature anywhere carries `camping_permission` other than `unknown` once O4 is taken.
11. No property on any facility, road, land or research-area feature can express an overnight claim (the M4 R75 pattern).

**Evaluation, with an injected clock**

12. Precedence: prohibited area order plus allowed site → Prohibited. With a valid `exempted_by` → the site claim.
13. Evaluation order: a stale prohibition is still Prohibited and flagged; freshness is applied after precedence, never before.
14. A stale `allowed` → Not established, with the last-reviewed date.
15. An order past `order_effective_to` with no new review → still shown, with OV7.
16. A default rule linked to a place with all modes unknown → every mode still Not established.
17. A default rule with no link appears in the unit panel and on no place.
18. A trip-date or stay-length check can add a conflict and can never remove one or produce a positive label.
19. Missing registry, empty registry and unreadable registry all render as not established, never as "no restrictions".

**Display**

20. Fixed strings compared byte for byte; none contains "verified", "legal", "permitted" or "open to".
21. No rendered overnight detail contains "available", "open", "allowed here" or "free" outside an approved string.
22. A status word never appears without its mode label.
23. OV2 and OV4 appear on every overnight detail, whatever its claims.
24. Prohibitions and restrictions render above source facts.
25. A place with only existence and management renders exactly the OV1 pattern.
26. No layer, legend or list title contains "dispersed camping" for computed geometry.
27. Colour and ordering: an unknown place is never styled or sorted as stronger than a reviewed one; browser test.
28. The availability link goes to a facility page, never a search URL.

**Regression fixtures drawn from this research**

29. Highway 82 corridor: a point inside the Described Area never yields a positive result.
30. Lincoln Creek: recreation page lists sites, order closes corridor, no exemption recorded → not Allowed.
31. South Platte River Corridor: "Dispersed camping is prohibited." → Prohibited at area scope; developed campgrounds inside it remain whatever their own claims say, subject to precedence and an explicit exemption.
32. Pike order on 2026-12-02 with no re-review → still restricted, flagged.
33. Fire: a fixture page titled as a lifting but attaching a Stage 1 order must not parse to a stage; stage stays unknown without manual review.
34. Key hygiene: no artifact, log line, URL or fixture contains an API key; RIDB tests run offline with no key.

---



> **Verification against origin/main (`bb85785ea98c8d5fb8d5694a36744b4f96a6161a`):** Not verified as a complete gap analysis: the existing section already covers injected time, precedence, stale restrictions/support, unknown dimensions, and several trip-date cases. The remaining listed cases are proposed additions; no tests were run.

Evaluator tests (add only those missing): injected dates; fact-specific review age; full-trip restriction
starting on departure day; indefinite orders; malformed seasonality; stale positive vs stale negative;
tentative identity; tent/vehicle mismatch; unknown dimensions; partial source failure;
cross-jurisdiction rules. A stale restriction stays in force and is flagged; a stale supportive claim is unknown.
Source: Codex reconnaissance at commit 2795625, 2026-10-08; measured facts spot-checked by Hermes
UNVERIFIED which of these section 10 already lists.

## 11. What was intentionally not done

- No file other than this one was written in any repository. No git state changed. `ROADMAP.md` was not touched.
- No API key was read, sent or printed. RIDB was contacted only for its public schema and agreement page, without a key.
- No PDF was read: not the signed orders, not the exhibits, not the printed MVUMs.
- Not fetched: the PSICC alerts index, CPW, BLM, CDOT, the MVUM trails layer, PitkinEmergency.com, the Maroon Bells–Snowmass wilderness order.
- No browser run. User-facing text was read from source and by calling the evaluation functions under Node.

---

## 12. Disagreements with Hermes

| # | Hermes said | Found today | Label |
|---|---|---|---|
| D1 | White River publishes a current Stage 1 fire restriction beginning September 11, 2026. | The forest lifted it: "will lift fire restrictions beginning Friday, Sept. 25." The alert Hermes read is the lifting notice, which still attaches the Stage 1 order. | `[READ ON WEB (not coordinator verified)]` |
| D2 | Pitkin County Stage 1 applies "until further notice" from September 4, 2026. | "Pitkin County has officially lifted Stage 1 Fire Restrictions" — release dated Sept. 24, posted Sept. 28. | `[READ ON WEB (not coordinator verified)]` |
| D3 | Stage 1 restrictions are in place for unincorporated Douglas County. | "STAGE 1 FIRE RESTRICTIONS HAVE BEEN LIFTED", updated 9/17/2026. Hermes cited a county services page; the sheriff's page is the source the repository already links. | `[READ ON WEB (not coordinator verified)]` |
| D4 | The Aspen occupancy order's period "ended December 31, 2025, so it cannot establish the rule" in 2026. | Order 2025-07 is in effect 2025-09-01 to 2028-12-31 at `/alerts/aspen-rd-occupancy-and-use-prohibitions` — the URL already in the repository. Hermes read a superseded page at a different URL. | `[READ ON WEB (not coordinator verified)]` |
| D5 | No public RIDB availability field could be verified; the schema would not load. | The schema loads without a key. It has no availability field or endpoint. It does have a `/reservations` historical report that Hermes did not mention. | `[READ ON WEB (not coordinator verified)]` |
| D6 | A 300-foot vehicle distance and a 7-day Lincoln Creek limit, from an older guide whose PDF now returns not found. | Not confirmed by anything current. Current pages give a 5-day limit at Lincoln Creek, a 100-foot water-and-trail rule (Order 2026-13) and a 300-foot *trailhead* rule (Order 1996-08). The repository's 300 ft road buffer has no current source. | `[READ ON WEB (not coordinator verified)]`, `[READ IN REPO]` |
| D7 | Hermes's evidence table lists MANAGEMENT as the layer holding orders and rules. | This draft keeps MANAGEMENT as "whose rules apply" and puts orders under CAMPING RULE. A difference of framing, not of fact. | `[INFERENCE]` |
| D8 | Hermes's recommended outputs include "current official rule supports overnight use". | This draft allows that only at site scope, per mode, within review age, and never from a retrieval at answer time. | `[INFERENCE]` |

Hermes missed three orders that matter: WRNF 2026-13 (100 feet from water and trails), WRNF 1993-06 (developed-campground stay limits) and the detail of WRNF 1996-08 (trailheads). `[READ ON WEB (not coordinator verified)]`

Where Hermes was confirmed: the White River 14-day sentence, the Pike 14-day and designated-site sentences and the 2026-12-01 end date, the South Platte and Rampart designated-only statements, the absence of a dispersed-camping field in the MVUM road service, the RIDB rate limit, and the absence of any machine-readable fire feed among the pages read. `[READ ON WEB (not coordinator verified)]`

A note on numbering: the watchlist's closing recommendation describes "M7" as snow, road conditions and permits. The roadmap's M7 is Camping / Dispersed Camping. This draft follows the roadmap. `[READ IN REPO]`

---

## Appendix A — HTTP requests

Twenty GET attempts with `curl`, no credentials, official hosts only. Responses were saved outside the repository as `resp_<name>`; a local request log is in the same directory.

| # | URL | Result | Saved as |
|---:|---|---|---|
| 1 | https://www.fs.usda.gov/r02/whiteriver/alerts/camping-stay-limitations | 200 | `resp_wr_stay.html` |
| 2 | https://www.fs.usda.gov/r02/psicc/alerts/pike-national-forest-occupancy-and-use-restrictions | 200 | `resp_psicc_occ.html` |
| 3 | https://www.fs.usda.gov/r02/whiteriver/alerts | 200 | `resp_wr_alerts.html` |
| 4 | https://apps.fs.usda.gov/arcx/rest/services/EDW/EDW_MVUM_01/MapServer?f=pjson | 200 | `resp_mvum_svc.json` |
| 5 | https://apps.fs.usda.gov/arcx/rest/services/EDW/EDW_MVUM_01/MapServer/1?f=pjson | 200 | `resp_mvum_l1.json` |
| 6 | https://www.fs.usda.gov/r02/whiteriver/alerts/aspen-rd-occupancy-and-use-prohibitions | 200 | `resp_wr_aspen_occ.html` |
| 7 | https://www.fs.usda.gov/r02/whiteriver/recreation/lincoln-creek-dispersed-camping | 200 | `resp_wr_lincoln.html` |
| 8 | https://www.fs.usda.gov/r02/psicc/about-area/south-platte-ranger-district | 200 | `resp_psicc_sprd.html` |
| 9 | https://www.fs.usda.gov/r02/psicc/recreation/south-platte-river-corridor | 200 | `resp_psicc_corridor.html` |
| 10 | https://www.fs.usda.gov/r02/psicc/recreation/rampart-range-recreation-area | 200 | `resp_psicc_rampart.html` |
| 11 | https://ridb.recreation.gov/shared/swagger/ridb.yaml | 200 | `resp_ridb_swagger.yaml` |
| 12 | https://ridb.recreation.gov/access-agreement-ridb | 200, JavaScript shell only, no agreement text | `resp_ridb_agreement.html` |
| 13 | https://dcsheriff.net/sheriffs-office/divisions/emergency-management/fire-restrictions/ | 200 | `resp_dcsheriff_fire.html` |
| 14 | https://pitkincounty.com/CivicAlerts.asp | 200 after redirect to https://pitkincounty.com/m/newsflash | `resp_pitkin_fire.html` |
| 15 | https://www.fs.usda.gov/r02/whiteriver/alerts/white-river-national-forest-lifting-fire-restrictions-friday-sept-25 | 200 | `resp_wr_fire_lift.html` |
| 16 | https://apps.fs.usda.gov/arcx/rest/services/EDW?f=pjson | failed, connection reset | none |
| 17 | https://www.fs.usda.gov/r02/whiteriver/alerts/white-river-national-forest-camp-location-restrictions | 200 | `resp_wr_camp_loc.html` |
| 18 | https://www.fs.usda.gov/r02/whiteriver/alerts/aspen-rd-no-camping-within-300-trailhead-exceptions | 200 | `resp_wr_trailhead.html` |
| 19 | https://apps.fs.usda.gov/arcx/rest/services/EDW?f=pjson | 200 (retry of 16) | `resp_edw_dir2.json` |
| 20 | https://www.fs.usda.gov/r02/whiteriver/alerts/developed-campground-stay-limitations | 200 | `resp_wr_dev_stay.html` |

## Appendix B — Measurement scripts

Throwaway, in the same directory: `measure.py` and `m2.py` (feature counts, field completeness, sample records), `say.cjs` (calls `trip-rules.js` and `trust.js` read-only to capture labels), `txt.py` (HTML to text), `get.sh` (the counted `curl` wrapper). Interpreter: the repository's pipeline virtual environment with `PYTHONDONTWRITEBYTECODE=1`.
