DRAFT - UNREVIEWED RESEARCH

# M6 / M7 source and schema implications - from the Rampart Range case study (Section C)

- Retrieved 2026-10-08 22:11-22:27 UTC (details per item). Builds on `rampart-evidence-closure.md` (Section A) and `rampart-relationships.md` (Section B), written earlier the same day.
- Written to generalise: Rampart examples are labelled "Rampart observation". Findings marked "general" come from published dataset descriptions, which are not specific to Rampart.
- This is a research input. It proposes no schema, changes no trust rule, and certifies nothing as verified or permitted. Rights conclusions are readings of quoted text by a non-lawyer; unclear stays unclear.
- Labels: **[SF]** source fact (dataset attribute, metadata, or published map) / **[ORI]** official recreation information / **[P]** partner / **[D]** derived / **[U]** unknown / **NOT RETRIEVED**.
- Section C budget: 4 searches (of 10); about 22 retrievals (of 30). Searches: (1) RIDB docs and terms; (2) COTREX licence and data download; (3) FSGeodata data-use and disclaimer; (4) COTREX feature service fields. Failed methods are listed in section 9.

---

## 1. Dataset inventory

| # | Dataset (publisher) | Endpoint / URL (retrieved) | Entity it carries | Update cadence as stated | Role for Ohvernight |
|---|---|---|---|---|---|
| D1 | **MVUM roads and trails, map service** `EDW_MVUM_02` (USFS Enterprise Data Warehouse) | https://apps.fs.usda.gov/arcx/rest/services/EDW/EDW_MVUM_02/MapServer, layers 1 roads, 2 trails (22:13). `EDW_MVUM_01` is the same without labels. | Designated routes by vehicle class and dates | "This data is published and refreshed on a unit by unit basis as needed and approved by the individual units in order to stay in sync and consistent with the published MVUMs." Metadata update frequency "As needed" (22:21). | M6 motorized-use rule per trail/road; M7 road access constraints |
| D2 | **MVUM published map**, South Platte Ranger District (PDF front and back) | https://www.fs.usda.gov/r02/psicc/maps-guides/motor-vehicle-use-maps and PDFs (22:13) | The legal designation as published, with a "Seasonal and Special Vehicle Designations" table | Map text: revised or "validated for the new year" each January (image-read); page last updated March 30, 2026; this PDF is dated 2025 in its file name | The controlling M6 evidence; not machine-readable |
| D3 | **Trail NFS Publish** `EDW_TrailNFSPublish_01` (USFS EDW) | https://apps.fs.usda.gov/arcx/rest/services/EDW/EDW_TrailNFSPublish_01/MapServer/0 (22:20) | NFS trail centerlines with official name and number and use fields | "Road and Trail data in the Enterprise Data Warehouse (EDW) are kept current by daily updates from forest SDE geodatabases" (service description, 22:23) | M6 trail identity and name; motorized-use fields (conflicts with D1/D2) |
| D4 | **USFS recreation sites (INFRA)** `EDW_RecInfraRecreationSites_02` (USFS EDW) | https://apps.fs.usda.gov/arcx/rest/services/EDW/EDW_RecInfraRecreationSites_02/MapServer: layer 0 site, layer 1 subsite, tables 2 activities, 3 services, 4 contacts (22:16, 22:23) | Campgrounds, picnic sites, trailheads, observation sites, with status, water, restroom, operator | Not stated in the service description. Record fields `infra_last_update` and `edw_last_modify`; observed range for 23 Rampart-area sites: 2020-06-21 to 2026-08-06 | M7 facility status and amenities; M6 trailhead identity |
| D5 | **USFS recreation opportunities** `EDW_RecreationOpportunities_01` and `EDW_RecreationAreaActivities_01` (USFS EDW) | https://apps.fs.usda.gov/arcx/rest/services/EDW/EDW_RecreationOpportunities_01/MapServer/0 ; .../EDW_RecreationAreaActivities_01/MapServer/0 (22:16, 22:23) | The public web-page content per recreation area: fees, season, restrictions, activities | "This published data is updated nightly from an XML feed maintained by the CIO Rec Portal team. This data is intended for public use and distribution." | M7 prose facts and fees; web page text equivalent |
| D6 | **Forest Service web pages and alerts** (fs.usda.gov) | https://www.fs.usda.gov/r02/psicc/recreation/... ; https://www.fs.usda.gov/r02/psicc/alerts (22:12) | Page text; alert list with order numbers and attached PDFs | Per page "Last updated"; alerts list is current at fetch | M7 orders and closures; no geometry |
| D7 | **Recreation.gov facility records** (Recreation.gov, FS org) | Web JSON `https://www.recreation.gov/api/camps/campgrounds/{facility_id}` and availability endpoint (22:12-22:14); documented API is RIDB below | Campground facility with description, campsites, type of use | Record carries `updated_date` (Flat Rocks 2025-11-25; dispersed facility 2025-12-29) | M7 reservable facilities, first-come status |
| D8 | **RIDB** (Recreation Information Database API) | https://ridb.recreation.gov/docs ; schema https://ridb.recreation.gov/shared/swagger/ridb.yaml (22:25). Requires an API key; **not called**. | RecAreas, Facilities, Campsites, Activities, Links, Organizations | Field `LastUpdatedDate`; no refresh cadence found in the swagger | M7 national facility list; recreation-area parent link `ParentRecAreaID` |
| D9 | **COTREX** (Colorado Parks and Wildlife) | https://trails.colorado.gov/ ; data downloads described on https://cpw.state.co.us/maps-and-gis ; statewide dataset record on data.colorado.gov (dataset page returned 404 on my fetch; description from a search result). **Not queried**. | Statewide trail/trailhead compilation from "over 230 trail managers" | Not stated in what I read | M6 candidate for trail enrichment; terms restrictive (section 6) |
| D10 | **Forest orders and alerts attachments** (PDF exhibits) | e.g. https://www.fs.usda.gov/sites/nfs/files/r02/psicc/publication/alerts/fseprd1174599.pdf | Orders with road-id tables and township/range exhibits | Per order effective dates (02-12-00-24-04 through December 1, 2026) | M7 orders; PDF tables only |

Not found: a geometry dataset of forest orders among the 145 EDW map-service names (listing read 22:20). Not searched beyond EDW: Forest Service Open Data (ArcGIS Hub) and data.gov copies of the same services - these are the same content republished.

---

## 2. Identifier crosswalk (Rampart observation, verified by joining retrieved records)

| Concept | Identifier and where | Observed example | Join notes |
|---|---|---|---|
| Recreation site (INFRA) | `site_cn` (D4) = `infra_cn` (D5) | FLAT ROCKS CG `5245.001621`; DUTCH FRED `10729010465` | Control numbers differ in shape per era ("5245.001621" vs "10729010465") |
| Recreation site short id | `site_id` (D4) | "03560" (leading zero) | Leading zero is significant |
| USDA recreation area id | `usda_portal_id` (D4) = `recareaid` (D5, D5 activities); in the web URL as `?recid=` | Flat Rocks CG 12931; Dutch Fred 12930; Flat Rocks TH 12933; parent "Rampart Range Recreation Area" 80379 | The web URL `?recid=12933` redirected to the forest recreation index at retrieval (22:16), so the recid URL alone is not a stable link; the slug URL worked |
| Recreation.gov facility id | `rec1stop_id` (D4) = Recreation.gov `facility_id` and `legacy_facility_id` (D7) | FLAT ROCKS CG `10165295` | Only populated for sites that exist on Recreation.gov (Flat Rocks CG yes; Dutch Fred, Flat Rocks TH no) |
| Forest unit | `recportal_unit_key` (D5) "12403"; `managing_org` "021211", `security_id` "0212" (D4); `adminorg` "021211" (D1) | same for every Rampart record | `021211` is the South Platte Ranger District code by the MVUM `districtname` |
| Recreation-area group | `complex_name` "RAMPART RANGE" (D4) | present on 11 of 23 sites | Free text; incomplete |
| MVUM road | `rte_cn` and `id`/`field_id` (D1 layer 1) | NFSR 300: id "300", `rte_cn` populated for roads (e.g. 563 -> 5724010465) | Roads carry control numbers |
| MVUM trail | `id`/`field_id` string, `rte_cn` **null** on the trails sampled, `globalid` (D1 layer 2) | "674" | Trail identity in D1 is a number string only; `name` is null |
| NFS trail | `trail_cn`, `trail_no`, `trail_name` (D3) | 0674 FLATROCK, `trail_cn` unverified for 0674; examples seen: 0770 `181861010602`, 0770.D `1993190010602` | **Zero-padding differs**: D3 "0674", D1 "674", PDF "0674", prose "#674". Some D3 numbers are unpadded ("627.A", "681.D", "681.F", "611", "615", "683", "800"). A join key needs normalization rules |
| RIDB facility | `FacilityID`, `LegacyFacilityID`, `OrgFacilityID`, `ParentRecAreaID`, `ParentOrgID` (D8 schema) | not called | **[U]** whether `OrgFacilityID` equals the USDA recreation area id: not verified, API not called |

---

## 3. M6 findings

### 3.1 Trail identity
- **User-facing identity must be built from several datasets.** D1 trails have only a number (`name` null) and many segments per trail (57 features for about 50 distinct ids in a 0.12 x 0.16 degree box; two or more segments for several trails, e.g. 770, 770.A, 690). D3 supplies the official name and number: "0674 FLATROCK", "0770.F SKELETON", "0681 SCOTTYS", "0767.A LIGHTFOOT LOOP", "0627 BEGINNER". The partner's popular names differ in spelling ("Bar Trail" vs agency "BARR"). Sub-trails use suffix notation ("681.B", ".AA"), and spurs/connectors are separate ids.
- **Seen as a gap:** the agency has no field for "alternate name", so any popular name ("Skeleton Loop", "Kiddy Corral") is not stored and the benchmark's "Skeleton Loop at Flat Rocks" cannot be matched without a reviewed mapping. Source: Section B 2.2.
- **Identifier to keep:** D3 `trail_cn` where present, plus the normalised `trail_no`; D1 `globalid` is not documented as stable across refreshes (not stated).
- **Segment-to-trail grouping:** D1 and D3 both store segments with `bmp`/`emp` (begin/end milepost). Both allow partial-trail designations (the MVUM PDF lists "0649 ... 0-1.84 and 8.24-9.45" as a milepost range). A trail-level designation is therefore not always a single value.

### 3.2 Motorized-use evidence
- **Three representations exist and disagree** (Section A 2.4, Section B 2.3): the published MVUM PDF table (May 16 - March 14 for about 40 trails), D1 (`motorcycle_datesopen` "12/01-03/14" for the same trails) and D3 (`allowed_terra_use`, `motorcycle_accpt`, `motorcycle_restricted`). For trails 0767 and 0767.A D3 says motorcycle use "restricted year-round" with `terra_motorized` Y while D1 and the PDF say open.
- **Stated rule for D3:** "When a Forest chooses to provide the highest attribute subset, TrailNFS_Mgmt, these attributes must be consistent with the Forest's published Motorized Vehicle Use Map (MVUM)." (D3 service description, 22:23.) **Rampart observation:** the observed rows (attribute subset `TrailNFS_Mgmt` for all) are not consistent with the PDF for several trails; the stated rule is therefore not a guarantee of consistency.
- **Semantics matter and are field-specific:** D3 `MOTORCYCLE_ACCPT` = "allowed, but not managed or restricted seasonally or year-round"; `MOTORCYCLE_RESTRICTED` = "restricted year-round"; D1 `MOTORCYCLE_DATESOPEN` = "Dates route is open for motorcycle travel" with the metadata caveat "It is not meant to describe when the conditions would be appropriate for that use."
- **Date format** `MM/DD-MM/DD` may hold multiple windows separated by commas ("01/01-03/14,05/16-12/31" seen on 506 and 503, 502.B). A single-window assumption silently fails: for trails the D1 value "12/01-03/14" may be one window of a split season that the field cannot fully express - this is **[U]**, not established.
- **Vehicle classes** (D1 road metadata): motorcycles appear under both `HIGHCLEARANCEVEHICLE` (as "... motorcycles and other highway legal vehicles ...") and `MOTORCYCLE` ("Two-wheeled vehicles on which the two wheels are inline"). No class distinguishes a plated from an unplated motorcycle; the plated/unplated rule lives in prose.
- **Gap:** the user's vehicle (non-street-legal dirt bike) must map to class combinations by a reviewed rule table; the datasets cannot do it alone.
- **Disclaimer text applies:** "These geospatial data and related maps or graphics are not legal documents and are not intended to be used as such." (D1 metadata; D5 service text, 22:21 and 22:23).

### 3.3 Trailhead relationships
- Trailhead identity exists in **D4** (site_type TRAILHEAD; `site_id`, `site_cn`, name, coordinates, `total_capacity`, restroom/water attributes), in **D5** (recreation area with `markeractivity` "OHV Trail Riding" - 13 such area records near Rampart), and on the **D2** map as a legend symbol "Motorized Trailhead".
- No dataset links a trailhead to a trail. The only explicit statements are prose on the Forest Service page ("The Flatrock Trail (#674) trail enters ...") (Section B 2.2). Trail "start" has to be stored as source-backed prose, reviewed candidate, or derived-from-geometry with a rule; the geometry rule (endpoint within 100 m) gave candidates that disagreed with the prose at Flat Rocks.
- **Capacity field:** `total_capacity` (e.g. Flat Rocks TH 85, Dutch Fred 55) has no unit definition in what I read - **[U]**.
- **Mislabelled places:** the Flat Rocks Trailhead page names the "South Park Ranger District" and its "approximately 6 miles" differs from the campground's "5 miles" - page text can contradict the record; datasets are no more reliable for it.

### 3.4 Road relationships
- D1 roads carry `id` and `rte_cn`, `jurisdiction` ("FS - FOREST SERVICE"), `operationalmaintlevel` ("3 - SUITABLE FOR PASSENGER CARS", "2 - HIGH CLEARANCE VEHICLES"), `surfacetype` ("AGG - CRUSHED AGGREGATE OR GRAVEL", "NAT - NATIVE MATERIAL"), vehicle class fields with dates, and `mvum_symbol_name`.
- **Road-to-place:** D1 road names encode places ("300.T FLAT ROCK CG", "506 DUTCH FRED", "300.R CABIN RIDGE PG", "300.M TOPAZ POINT PG"); orders and MVUM reference the same ids. The *name* is an agency label for the route, but no dataset states "this road serves that site". Treat as a candidate link needing review.
- **No road-network topology is published** in these datasets; derived connectivity must be computed and labelled geometric only (adventure-model rule).
- **Road jurisdiction conflicts** between D1 ("FS - FOREST SERVICE") and the partner's FAQ ("county road"): the pipeline must keep the source attribute and its source label.
- **Symbols 11 and 12** ("Special Designation, Yearlong/Seasonal") are in the MVUM metadata with no definition beyond the label. NFSR 300 and most Rampart spurs use symbol 12. A schema must carry "special designation, undefined by source" as an explicit state, not map it to open or closed.

### 3.5 Recreation-area identity
- The recreation-area concept is carried by **D5** (area record 80379 "Rampart Range Recreation Area", `markeractivity` "Intermediate Parent Group") and by Recreation.gov/RIDB `RecArea` (`ParentRecAreaID` on facilities; RIDB schema says "Recreation areas can contain one to many child facilities." - D8, 22:25). In D4, `parent_cn` is null for all 23 sites and `complex_name` is partial.
- The same place is called "Rampart Range Recreation Area", "Rampart Range Motorized Recreation Area", "Rampart Range Road", "Rampart Range Motorized Management Committee [sic]" across publishers; the committee's name appears two ways ("Motorized Management Committee", "Motorcycle Management Committee").
- **No polygon** for the recreation area was found. Boundary of "the area" in rules like "restrictions apply to the Rampart Range Motorized Recreation Area" is therefore not machine-checkable.
- Ranger-district polygons exist (`EDW_RangerDistricts_03`, not queried): context only.

---

## 4. M7 findings

### 4.1 Day-use sites, picnic facilities, and the overnight vs day-use distinction
- **D4** `site_type` values seen: CAMPGROUND, TRAILHEAD, PICNIC SITE, HORSE CAMP, OBSERVATION SITE, TARGET RANGE, DOCUMENTARY SITE, RECREATION RESIDENCE. A picnic site record (`CABIN RIDGE PS`, `TOPAZ POINT`, `DEVILS HEAD PS`) is the structured signal for "day-use picnic". `fee_charged`/`fee_type` exist ("STANDARD AMENITY FEE", "EXPANDED AMENITY FEE") but the day-use fee text is prose in D5 `feedescription` ("There is a day use fee of $7.").
- **Overnight vs day use is not a field.** Evidence is split: D5 `restrictions` text "Overnight use prohibited." (Cabin Ridge picnic area, Devils Head picnic area) is prose; Flat Rocks CG day use is prose inside `feedescription` ("$11.00 fee for day use if not camping overnight."); RIDB/Recreation.gov campsites have `TypeOfUse` (Recreation.gov availability record for site 10165296: `type_of_use` "Overnight"). The numbered dispersed sites' day-use status has no statement anywhere (Section A 6.1).
- **D4 subsite layer** (`unit_type`, `type_of_use`, `picnic_table`, `fire_pit`, `shade`, `max_vehicle_length`, `www_reservable`, `driveway_*`, `tent_pad`) would hold per-site attributes. **Rampart observation:** layer 1 returned **0** subsites in the Rampart search box, so per-site amenities (shade, table, hammock-relevant trees) do not exist in this dataset for these places. **[U]** whether the Recreation.gov "numbered campsites" of the dispersed facility are anywhere in structured form; Recreation.gov availability endpoint for the campground returned one generic site "Standard / Scan and Pay".
- **Amenities by `RecSite Services` table** (D4 table 3: `service_type`, `services_distance_from_site`): Flat Rocks CG has rows FIRE RINGS, WATER DRINKING, RESTROOMS, PICNIC TABLES "Within the Site". Dutch Fred has no rows (consistent with its "No" restroom/water). **Rampart observation:** a missing services row is not itself a statement that the amenity is absent; here it happens to agree with the attribute "No".
- **Hammock and tree rules** are not represented in any dataset read; only prose in orders and regulations (Section A 5).

### 4.2 Camping and dispersed camping
- **Developed campgrounds:** D4 (CAMPGROUND), D5, D7/D8 (campground facility). **Designated dispersed sites:** D7 facility "Rampart Range Recreation Area Designated Dispersed Camping" (10132201) with prose; D5 area record; not in D4 subsites.
- **Rules are prose or PDF:** camping outside developed and designated sites is prohibited by Order 02-12-00-24-04 (prohibition 4) and Order 2022-08 (Section A); neither is structured.
- **Reservation model:** D5 `reservation_info` ("This is a first-come, first-serve campground."); Recreation.gov `reservationCutOff` with units "Not Reservable" on the dispersed facility (an internal rule field with a value that contradicts its own label - a data-quality warning for any parser).
- **Camping legality for a setup (tent, RV length, vehicle count)** is in prose ("A maximum of eight people, two tents and two vehicles or one recreation vehicle (RV) is allowed per site."; "recreational vehicles up to 30 feet in length"). Not structured except `max_vehicle_length` on subsites (absent here).

### 4.3 Current orders and closures
- **Forest Service alerts list** (D6): per alert title, summary, start date, order number, attached PDFs; **no geometry, no API found** (the list page is the interface). Scope is written as text ("This order affects the South Platte Ranger District").
- **Orders' place scope** is expressed as road id tables, township/range exhibits, area descriptions. A structured join to places requires a person to transcribe and review.
- **Recreation.gov alerts:** not exposed by the public endpoints I tried (two 404). The search-result lead about an order in effect "from August 21, 2026 ... through ... November 14, 2026" on the Flat Rocks Recreation.gov page (Section A 1.2) shows alerts may exist on Recreation.gov that are not in the FS alerts list; **[U]**.
- **`RECAREAADVISORIES`**: D5's service description lists advisories among the related tables but the map service exposes only layer 0 (`tables []`, 22:23). Not available through this service. **[U]** whether advisories are reachable elsewhere.
- **Seasonal road closure** is prose repeated on every recreation page ("Rampart Range Road is closed by December 1 and remains closed throughout the winter ... A target date is April 1"); the MVUM has dates, the pages have a different wording ("closed ... by December 1" vs MVUM "May 16 - November 30" for passenger vehicles). The 'annual' structure and the "mud-season closure order" (April 1 - May 31) are not in a dataset.

### 4.4 Facility status
- **D4** `seasonal_operational_status` ("OPEN", "CLOSED" - ZINN RANCH is CLOSED), `op_status_reason`; no `as-of` date other than `infra_last_update`. **Rampart observation:** FLAT ROCKS CG "OPEN" while its own pages give a season that ended in September; the field is not date-bound. A status without an effective interval cannot be used for a specific weekend.
- **D5** `openstatus` ("open" / "none"), `open_season_start/end` as free text ("Early May", "Late September", "May 26, 2023" / "Sept. 24, 2023" for Indian Creek Trailhead - a past-dated season, "Mid May" / "closes December 1"). Dates are text, sometimes with a year, sometimes a month phrase, sometimes stale.
- **D6** pages show "Site Open" in some pages (Cabin Ridge, Topaz Point) and not others (Flat Rocks).
- **Operator** (`operated_by`): "Concessionaire", "US Forest Service", null. The concessionaire's identity is not in D4; Recreation.gov text names a company for the dispersed facility.
- Staleness: a retrieval time is not a confirmation; the model's `checked at` requires a person (adventure-model section 4).

### 4.5 Backup options
- No dataset says "alternative to X". Candidates have to be assembled from D4/D8 by distance and facility type and then reviewed. **Rampart observation (D4 records):** other campgrounds in the box: DEVILS HEAD CG (OPEN, Concessionaire, open "Memorial Day Weekend"; D5 season "Early May" - "Late September"), INDIAN CREEK EQUESTRIAN / "(EQUESTRIAN)" (horse camp; D5 `reservation_info` "Phone ... at least 4 days in advance" - a different reservation regime; **not** a rider backup without review). Picnic backups: Cabin Ridge PS, Topaz Point (both "open" in D5), Devils Head PS. Whether each is practical for an unplated bike and a family is the established-chain question of the adventure model; none of the data states it.
- "Absence of a backup" cannot be derived from absence of records; a person must record "checked, none".

---

## 5. Update cadence and staleness summary

| Source | Stated cadence (quote) | Observed staleness | Notes |
|---|---|---|---|
| D1 MVUM service | "published and refreshed on a unit by unit basis as needed"; metadata "As needed" | Layer carries no edit date I could read; PDF 2025 | Compare with D2 each January |
| D2 MVUM PDF | revised or validated each January (image-read); page "Last updated March 30, 2026" | file name 07302025 | |
| D3 Trail NFS Publish / roads | "kept current by daily updates from forest SDE geodatabases" | Contradicts D1 and D2 -> a daily publication does not guarantee agreement | |
| D4 INFRA | none stated | `infra_last_update` from 2020-06-21 to 2026-08-06 across 23 sites; many 2025-04-09 bulk | Per-record edit date is the freshness signal |
| D5 | "updated nightly from an XML feed" | `open_season` text may be years old | |
| D7 Recreation.gov web records | `updated_date` | 2025-11-25 and 2025-12-29 | |
| D8 RIDB | `LastUpdatedDate` per record; cadence not found | - | |
| D9 COTREX | not found | - | "Responsibility for accuracy of the data rests with the source." (data.colorado.gov description in a search result) |

---

## 6. Licence, terms and rights - quoted, per dataset

Rights questions (contract): access/fetch, scrape, transform, cache/store, publish, redistribute, commercial use, derivatives; attribution/share-alike; rate limits; retention; privacy; termination. Evidence is what I read; "not stated" is not permission.

| Dataset | Controlling text (quote) | Fetch | Cache/store/transform | Publish/redistribute | Commercial | Derivatives | Attribution | Verdict |
|---|---|---|---|---|---|---|---|---|
| **D1, D3, D4 (USFS EDW map services)** | Metadata and service text: "These geospatial data and related maps or graphics are not legal documents and are not intended to be used as such." "The data are dynamic and may change over time. The user is responsible to verify the limitations of the geospatial data and to use the data accordingly." (D1 metadata, retrieved 22:21; the same "Enterprise Data Disclaimer" text appears on https://data.fs.usda.gov/geodata/edw/, seen only as a search-result excerpt). Data.gov-style catalog entry: "Usages notes, disclaimers and conditions of use can be found in each dataset's metadata or the webpage." | Public map services; no key required | **No licence text read** in the three metadata files or service descriptions (only the disclaimer) -> **unclear** | **Unclear.** D5 says "This data is intended for public use and distribution." (D5 only) | Not stated | Not stated | Not stated | Public access evident; reuse rights **unclear** - no explicit permission or prohibition found. Do not assume a licence from the publisher being a government. |
| **D5 (recreation opportunities)** | "This published data is updated nightly from an XML feed ... This data is intended for public use and distribution." plus the same disclaimer | yes | unclear | "intended for public use and distribution" -> **closest to explicit permission**; scope of "use" undefined | not stated | not stated | not stated | Better than D1/D3/D4; still not a licence |
| **D2 (MVUM PDF)** | Published map; text on the map "MVUM Disclaimer: #1 The Forest Service reserves the right to correct, update, modify, or replace this GIS information without notification." (image-read at low resolution; wording approximate, re-read needed) | download allowed from the Forest Service page | not stated | not stated | not stated | not stated | not stated | Treat as public document, rights unclear |
| **D8 RIDB** | https://ridb.recreation.gov/ (search-result text): "The data is provided at no cost in order to encourage wide distribution and regular updates to different publications, databases, and websites ... There is no need to contact us before incorporating the data into your system. In exchange, we encourage you to provide a link to Recreation.gov and acknowledge credit, such as "data source: ridb.recreation.gov"." and "by registering to use the API and/or downloading the RIDB data, you are agreeing to be bound by the terms and conditions of the RIDB API Access Agreement." Access Agreement (search-result excerpt only; full page NOT RETRIEVED): "You have no right or license to, and shall not: (i) copy, distribute, rent, lease, lend, sublicense, transfer or make derivative works of the API, the API Documentation, the API Key (collectively, the "API Vendor Materials")"; "(iv) use the API Vendor Materials to create or make available an application programming interface ... similar to, or that would otherwise be a substitute for, the API"; "AS IS" basis; key must not be shared. Also https://www.recreation.gov/use-our-data (retrieved 22:24): "available for free to anyone who envisions a variety of uses"; "no need to contact us before incorporating Recreation.gov data into your system"; "we encourage you to provide a link to Recreation.gov and acknowledge credit". | Requires registration and API key (not used) | "to get automatic updates as frequently as needed" (use-our-data) -> caching contemplated; agreement text on storage **not read** | "encourage wide distribution" -> redistribution of data looks permitted; the agreement forbids redistributing the *API materials* | no commercial-use prohibition read; **agreement not fully read** | derivative works of the API materials prohibited; derivatives of data not addressed in excerpts | "encourage" credit (not a stated obligation) | Probably the clearest of the four for data reuse, but the Access Agreement must be read in full before any use; rate limits and termination terms **not read**. |
| **D7 Recreation.gov web JSON endpoints** (not RIDB) | not documented; Recreation.gov terms of use page **not read** | Observed to respond without login | - | - | - | - | - | **Unclear; use RIDB, not the web endpoints, in any pipeline.** Used here only to read public facility records, once each, for research. |
| **D9 COTREX** | https://trails.colorado.gov/terms (Last Update: October 25, 2018; retrieved 22:25), section "Restrictions on Use": "By accessing and using the COTREX application, you may not: Use, repost, copy, distribute or publish any Content unless you have been given permission by Colorado Parks and Wildlife in a separate written agreement; Use geographic location data to create or augment any other data set; Access or search or attempt to access or search the COTREX application using any means other than the currently available interfaces that are provided by Colorado Parks and Wildlife as part of the COTREX application; Crawl any portion ..." Also "Depiction of a road, trail or area by the COTREX application is not and should not be interpreted as an invitation to all types of travel or as an implication that the road, trail or area is passable, actively maintained, suitable or safe for travel or that the road, trail or area is open for general public use." Separate: data.colorado.gov record description (search result): "Permissions: Public"; "Responsibility for accuracy of the data rests with the source." CPW Maps and GIS page (22:26): data "available as individual ESRI Shapefiles ... or as web services" - no licence text found on that page. | via provided interfaces only | **prohibited without separate written agreement** per the app terms | prohibited without agreement (app terms) | prohibited without agreement | "create or augment any other data set" prohibited | n/a | **Locked** for any redistributed or derived Ohvernight dataset until a separate written agreement or a clear open-data licence on the downloadable dataset is shown. The tension between "Permissions: Public" on the data portal and the app terms is **unresolved**. |

Proposed clarification questions (drafts; **not sent**; no contact made):
1. To CPW (COTREX): "Do the COTREX Terms & Conditions (Last Update October 25, 2018) apply to the COTREX dataset downloadable from the Colorado Information Marketplace, and under what licence may that dataset be used in a public web application with attribution?"
2. To Recreation.gov/RIDB: "May a public, non-commercial map application cache RIDB facility and campsite records and redisplay them with attribution; what are the rate limits and the retention expectations in the API Access Agreement?"
3. To USFS EDW (data steward): "What licence or use statement applies to the EDW recreation-site (INFRA) and MVUM map-service data, and is redistribution of derived records permitted with attribution?"
4. To the South Platte Ranger District (for Section A, not C): "Which MVUM representation controls trail dates (PDF table or EDW attributes), and is Flat Rocks Campground open for day use on 10-11 October 2026?"

---

## 7. Schema gaps Ohvernight would have to model (findings, not decisions)

1. **Trail identity as two levels:** user-facing trail vs source segments with member map; source ids kept with a normalisation rule for zero padding and ".A" suffixes; official name from D3, popular names as claims with source, not as identity.
2. **Multiple conflicting source readings kept side by side** per trail and per field (PDF table, D1, D3), each with its own source id and retrieval date; "conflict - unresolved" as a state, not a coerced value.
3. **Season windows as a list of date ranges** (not one window), with an explicit "window semantics" value (legal window vs managed vs accepted vs restricted), because D1 `MM/DD-MM/DD`, D3 `*_accpt` vs `*_restricted`, and the PDF's "Dates Allowed" are different things.
4. **Vehicle model:** classes defined by the source (passenger, high clearance, motorcycle, ATV, "other wheeled OHV", <=50" classes, e-bike classes) mapped by a reviewed table to user vehicle attributes including "plated/highway legal" vs not; a plate requirement is a claim attached to an area or route class, not a boolean on a road.
5. **"Special designation, undefined by source"** (symbols 11/12) as a first-class value.
6. **Trailhead as a place with source ids** (`site_cn`, `usda_portal_id`, optional `rec1stop_id`), coordinates, source-stated amenities (restroom/water with value "No" vs absent), `total_capacity` with unit "unknown" until the source defines it.
7. **Relationship records** (adventure-model section 3): `starts_at` with origin {prose, MVUM graphic, reviewed candidate, derived-geometry}, and the quote/page for each; `member_of_recreation_area` with origin {complex_name, prose, none}.
8. **Recreation-area identity as an alias set** (Rampart Range Recreation Area / Motorized Recreation Area / Road / "RAMPART RANGE" complex), with boundary unknown.
9. **Facility status with an interval and an as-of:** (status, source, field, edit date, effective_from/to if stated, retrieved at); never a bare OPEN. Season free text ("Early May", "Late September", "May 26, 2023") parsed with a "text as published" companion field and a "parsed with confidence" flag.
10. **Overnight vs day use as separate claims per site:** `day_use` (statement, fee text, source), `overnight_use` (statement, source), `overnight_prohibited` (restriction), each independently unknown.
11. **Fee as structured value plus text:** amount, unit (per site, per vehicle, per day), who may pay by what means (cash/check/scan-and-pay) - currently prose in `feedescription`.
12. **Order as an entity:** order number, authority, effective interval, scope text, exhibits (PDF), prohibition list with CFR cites, and per-place applicability as a reviewed link; restrictions never expire by staleness.
13. **Alert/advisory as an entity** distinct from orders, with source (FS alerts, Recreation.gov alert, RRMMC banner as partner), start, end, retrieval time, and "not seen on source X" evidence (absence of an alert in one list does not remove an alert elsewhere).
14. **Operator/concessionaire** with source and date; **jurisdiction/managing org** codes (`021211`) separate from `evidence.agency`.
15. **Partner banner status** (RRMMC "Trail Status: OPEN") stored, if at all, as a partner report with retrieval time and a "stale-prone" flag; it flipped in cached copies in this session (live OPEN vs search description CLOSED).
16. **Evidence coverage items** per subject/category/jurisdiction with `checked`/`not checked` (adventure-model section 4); this research supplies *candidate* categories only: MVUM, order exhibits, Recreation.gov alerts, concessionaire status, hammock/trees, day-use of dispersed sites, picnic at trailhead.
17. **Personal data exclusion:** D4 includes a `RecSite Contacts` table (addresses, phone, email) and Recreation.gov records contain a contact email; AGENTS.md prohibits adding raw personal contact details to published data, so loaders must drop these fields by design.
18. **Rights per source row:** each dataset carries a rights status {permitted, prohibited, unclear} and the quoted text, so a locked source (COTREX today) cannot be loaded by accident.

---

## 8. Reusable observations about method (general)

- Cross-source agreement tests (PDF vs data vs prose) found real conflicts within one agency; treat the agency's *published* map as the first source and its data layers as derived presentations until reconciled.
- Counts quoted in this file (23 recreation sites in the box, 11 with `complex_name`, 57 MVUM trail features, 65 TrailNFS_Publish features) are my tallies from single queries on 2026-10-08, not audited. A numerical audit belongs to Codex.
- An ArcGIS REST service description is the cheapest authoritative source for cadence and field definitions; metadata XML files under `data.fs.usda.gov/geodata/edw/edw_resources/meta/S_USA.*.xml` give coded-value definitions (three of six guessed names returned 404).

---

## 9. Failed or incomplete access

- eCFR official API: failed (Section A).
- RIDB Access Agreement full page: two methods (curl, web extractor) returned an empty shell or failure -> **NOT RETRIEVED**; excerpts from a search result only.
- data.colorado.gov COTREX dataset page and its JSON: 404 by two methods -> **NOT RETRIEVED**; description known from search results only. COTREX features not queried (terms restrict).
- EDW recreation metadata XML for three guessed names: 404.
- RIDB API: not called (key required; not authorised).
- RecAreaFacilities/RECAREAADVISORIES tables: not exposed.
- Nothing contacted; no forms, logins or purchases.
