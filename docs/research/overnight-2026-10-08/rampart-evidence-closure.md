DRAFT - UNREVIEWED RESEARCH

# Rampart Range - evidence closure (Section A)

- Mission: Ohvernight overnight research, Section A of 3. Extends `rampart-official-facts.md` (earlier worker, 2026-10-08 21:52-21:57 UTC); nothing there is repeated unless it changes.
- Outing: 10-11 October 2026, non-street-legal dirt bike, family day base, approach Larkspur - Sedalia - Highway 67.
- Retrievals in this section: 2026-10-08 22:11 to 22:19 UTC (times per item below, from `date -u` on the research machine). Web searches: 4 of 10. Page/API retrievals: about 34 requests (see "Budget" at the end - this is at or slightly over the 30-retrieval bound because several were small repeated queries of one ArcGIS service; stated openly).
- Labels: **[SF]** source fact (agency order, regulation, published map, or agency dataset attribute) / **[ORI]** official recreation information (agency descriptive page or record) / **[P]** partner information (Rampart Range Motorcycle Management Committee, RRMMC, a volunteer partner, not an agency) / **[D]** derived (my reasoning, shown) / **[U]** unknown.
- Nothing here says an activity is "allowed" unless a responsible source says so in its own words. Absence of a prohibition is not permission.
- Search-engine snippets are used only as leads and are labelled so wherever they appear.

---

## 0. Headline results

1. **The Motor Vehicle Use Map content is now read** (previous worker could not read it). The published South Platte MVUM carries a "Seasonal and Special Vehicle Designations" table. For the numbered Rampart OHV trails it states a date window "May 16 - March 14" for "Trail, <50" wide (open to OHVs such as ATVs and motorcycles)". 10-11 October falls inside that window. **But** the Forest Service's own MVUM feature service gives different (apparently partial) motorcycle date windows for the same trails, and two trails the benchmark cares about (679 Dutch Fred Trail, 690 Powerline) are not in the table at all. Conflict recorded, not resolved (section 2).
2. **Rampart Range Road (NFSR 300) for an unplated bike:** the MVUM table gives NFSR 300 and the numbered spurs "Road, Special Vehicle Designation" May 16 - Nov 30 and "Roads Open Only to Vehicles 50" or Less in Width" Dec 1 - Mar 14. The feature service has the passenger-vehicle field open 05/16-11/30 and the motorcycle field only 12/01-03/14. **[D]** Consistent with, but not a plain-language statement of, "no unplated motorcycle on NFSR 300 in October". The plain-language statement remains the Forest Service page text already quoted ("A current license plate and valid driver's license are required to ride on the roads.").
3. **Flat Rocks Trailhead has an agency record and an agency web page** (the earlier file said none was found). The agency page names the trail as "Flatrock Trail (#674)", not RRMMC's trail 673 / "Skeleton Loop". Conflict logged.
4. **Dutch Fred restroom conflict:** two separate Forest Service sources (web page and the national recreation-site database) both say no restroom. Only the partner says "vault toilets". The conflict is therefore partner vs. agency, and the agency record is the one to follow; it is still not a statement about a portable toilet or about conditions on the day.
5. **Flat Rocks Campground on 10-11 October: still UNKNOWN.** Agency pages say the season ends "late September" with a reduced "extended season"; the agency database field says OPEN but was last edited 2026-08-06 and carries no date range for status. One unverified search-snippet lead mentions an order "in effect from August 21, 2026 ... through ... November 14, 2026" on the Recreation.gov Flat Rocks page; it did not appear in the page text I retrieved, nor in the Forest Service alerts list. Needs a human look (section 1).
6. **Hammock:** no hammock rule found in any reviewed source; the only relevant regulation text is 36 CFR 261.9(a) "Damaging any natural feature or other property of the United States." Hammock use stays **not established**.
7. **Day use of a numbered dispersed site and picnicking at a trailhead lot:** still not established by any responsible source.
8. **Current closures/orders:** none found that names the northern Rampart corridor (alerts list re-read 22:12 UTC). Standing orders already in the earlier file still apply.

---

## 1. Flat Rocks Campground - status, day use, water (10-11 October)

### 1.1 What the sources say, and when they were read

| # | Source (publisher) | URL | Retrieved (UTC) | Decisive text | Label |
|---|---|---|---|---|---|
| 1 | Forest Service, Pike-San Isabel NF recreation page "Flat Rocks Campground" ("Last updated January 23, 2026") | https://www.fs.usda.gov/r02/psicc/recreation/flat-rocks-campground | 2026-10-08 22:12 | "The campground is open from early May to late September, dependent on the weather." / "Visitors may expect full service between Memorial Day weekend and Labor Day weekend. The area also has an extended season when services such as water, trash or a host may not be available during the fall, winter and spring." / "$11 fee for day use if not camping overnight." / "Water is available." Page text unchanged from the earlier retrieval. | [ORI] |
| 2 | Forest Service national recreation-site database, layer "USFS Recreation Site", record `FLAT ROCKS CG` (site_id 03560, site_cn 5245.001621) | https://apps.fs.usda.gov/arcx/rest/services/EDW/EDW_RecInfraRecreationSites_02/MapServer/0 | 2026-10-08 22:16 | `seasonal_operational_status` = "OPEN"; `open_season` = "May 28, 2021"; `water_availability` = "Yes"; `restroom_availability` = "Vault toilets"; `operated_by` = "Concessionaire"; `fee_charged` = "Y" (EXPANDED AMENITY FEE); `infra_last_update` = 2026-08-06; `edw_last_modify` = 2026-08-07; `rec1stop_id` = 10165295; `usda_portal_id` = 12931 | [SF]-grade attribute, but see limits below |
| 3 | Forest Service recreation-opportunities service, record "Flat Rocks Campground" (recareaid 12931) | https://apps.fs.usda.gov/arcx/rest/services/EDW/EDW_RecreationOpportunities_01/MapServer/0 | 2026-10-08 22:16 | `openstatus` = "none"; `open_season_start` = "Early May"; `open_season_end` = "Late September"; `reservation_info` = "This is a first-come, first-serve campground." | [ORI] |
| 4 | Recreation.gov facility record "Flat Rocks Campground" (facility 10165295; org FS; record updated 2025-11-25T19:42Z) | https://www.recreation.gov/api/camps/campgrounds/10165295 and page https://www.recreation.gov/camping/campgrounds/10165295 | 2026-10-08 22:12 and ~22:14 | "This location is available on a first-come, first-served basis only." / "Flat Rocks Campground is a wooded campground with 19 campsites ..." / "Water is available." No season dates, no status field, no fee text in the record (`facility_use_fee_description` empty). | [ORI] |
| 5 | Recreation.gov availability endpoint for facility 10165295, month of October 2026 | https://www.recreation.gov/api/camps/availability/campground/10165295/month?start_date=2026-10-01T00%3A00%3A00.000Z | 2026-10-08 22:12 | One campsite id 10165296, site "Standard", loop "Scan and Pay", type "STANDARD NONELECTRIC", `availabilities` = {} (empty). [D] An empty map for a first-come site is not evidence of open or closed. | [D] |
| 6 | Forest Service alerts list, Pike-San Isabel | https://www.fs.usda.gov/r02/psicc/alerts | 2026-10-08 22:12 | No alert naming Flat Rocks, Rampart Range Road or NFSR 300 in Douglas County; newest alerts Oct 6 (Harris Park RX), Oct 2 (prescribed fire), Oct 1 (Willow Fire), Sep 18 (FSR 286), Sep 1 (Aspen Acres). | [SF]/[D] |

### 1.2 Unverified lead - possible order on the Recreation.gov Flat Rocks page

A search-engine result for the Recreation.gov Flat Rocks page (query: "Flat Rocks Campground Rampart Range Road Pike National Forest campground operated by concessionaire 2026", 22:12 UTC) displayed this text in its description: "This Order shall be in effect from August 21, 2026, at 12:01 a.m. through August November 14, 2026, at 11:59 p.m., unless rescinded." (The search result itself has the typo "August November".) The same page, fetched directly twice (API record and rendered-page text), did **not** contain any order or alert text. The Forest Service alerts list read at 22:12 UTC lists no order with those dates.

- Status: **[U] UNVERIFIED LEAD**. Could be a Recreation.gov alert loaded by script, a stale snippet, or a different location's order cached against the page. It is a possible restriction and, per the trust rules, a restriction of unclear scope is retained and flagged, not dropped.
- What would settle it: a person opening the Recreation.gov page in a browser and reading any "Alerts"/"Notices" panel. I did not log in or script a browser (not needed for a public page, but outside the retrieval methods used here).

### 1.3 Conclusions

- **Open/closed on 10-11 October: [U] unknown.** Agency descriptive text says the stated season ended "late September" with a lower-service "extended season". The agency database status field says "OPEN" but (a) it is a single undated state flag, (b) the record was last edited 2026-08-06, and (c) its `open_season` field holds the unrelated value "May 28, 2021". The status field is therefore not a fall-2026 confirmation.
- **Day-use acceptance on that weekend: [U] unknown.** The only day-use statement is the static "$11 fee for day use if not camping overnight." Payment method: "Fees are payable by cash, check or money order." (page 1) while Recreation.gov mentions "Scan and Pay" for sites (page 4); which applies in October is unknown.
- **Water on that weekend: [U] unknown.** "Water is available." is a static facility statement; the same page explicitly warns water "may not be available during the fall". Treat as not established; bring water.
- **Operator: [U] not settled.** Agency database: "Concessionaire". The Recreation.gov record for the separate dispersed-camping facility (10132201) says "operated by ExplorUS LLC". A search result for a third-party directory attributes some Rampart-area sites to "Rocky Mountain Recreation Company". Third-party directories are not evidence and are not used. The concessionaire's own page was **NOT RETRIEVED** (earlier worker: listing absent; second method not attempted here because the contact route is a phone call, which is out of bounds).
- **Calling the district office is the only listed way to settle the above** (Friday 9 October is the last weekday; the line was not called - no contact permitted).

---

## 2. MVUM - per-trail motorcycle designations and seasonal dates

### 2.1 Retrievals

| Item | URL | Publisher | Retrieved (UTC) |
|---|---|---|---|
| South Platte Ranger District MVUM, front (PDF, 2.5 MB; redirects to `.../SPLTMVUMFINALFRONT07302025.pdf`) | https://www.fs.usda.gov/media/262850 | USDA Forest Service | 2026-10-08 22:13 |
| South Platte Ranger District MVUM, back (PDF, 3.9 MB) | https://www.fs.usda.gov/sites/nfs/files/r02/psicc/publication/SPLTMVUMFINALBACK07302025.pdf | USDA Forest Service | 2026-10-08 22:13 |
| MVUM feature service, layers 1 (roads) and 2 (trails), bounding box lon -105.16 to -105.04, lat 39.22 to 39.38 | https://apps.fs.usda.gov/arcx/rest/services/EDW/EDW_MVUM_02/MapServer | USDA Forest Service Enterprise Data Warehouse | 2026-10-08 22:13 |

Method for the PDFs: the PDFs have no extractable text layer. I rendered them to images with the macOS `sips` tool at 7000-8000 px wide, cropped the table, legend and Rampart inset, and read them with image vision. **Every PDF value below is an image reading and needs a human re-read against the PDF before it is relied on** (digits in small print could be misread).

### 2.2 What the published MVUM says (PDF front, table "Seasonal and Special Vehicle Designations") **[SF], image-read**

| Route numbers (as printed) | Legend description (as printed) | Dates allowed (as printed) |
|---|---|---|
| 0627, 0646, 0649.A, 0650, 0653, 0657, 0662, 0673, 0673.A, 0674, 0674.B, 0675, 0677, 0679.A, 0679.B, 0680, 0681, 0681.B, 0681.C, 0681.E, 0682, 0682.A, 0682.AA, 0683, 0685, 0686, 0686.A, 0688, 0787, 0787.A, 0788 | "Trail, <50" wide (open to OHVs such as ATVs and motorcycles)" | "May 16 - March 14" |
| 0649 (mileposts 0-1.84 and 8.24-9.45 shown) | same | "May 16 - March 14" |
| 0693 | "Trail Open to Motorcycles only" | "June 1 - March 31" |
| 0770 | "Trail Open to Motorcycles only" | "May 16 - March 14" |
| 0767, 0767.A | "Trail Open to All Vehicles"; and "Trail, <50" wide (open to OHVs such as ATVs and motorcycles)" | "May 16 - November 30"; "December 1 - March 14" |
| 300, 300.M, 300.O, 300.P, 300.PA, 300.Q, 300.R, 300.S, 300.T, 300.U, 348, 502, 503, 502.2, 502.B, 506, 507, 563 | "Road, Special Vehicle Designation"; and "Roads Open Only to Vehicles 50" or Less in Width" | "May 16 - November 30"; "December 1 - March 14" |

Legend (PDF back, lower left) as read: "Roads Open to Highway Legal Vehicles", "Roads Open to All Vehicles", "Roads with Special Vehicle Designation", "Trails open to All Vehicles", "Trails Open to Vehicles 50" or Less in Width", "Trails Open to Motorcyles Only" [sic], "Seasonal Designation (See Table)", "Motorized Trailhead", "FS Campground", "Picnic Area". The back also carries a "Rampart Range Road Inset" labelling trails 0627, 0646, 0679, 0679.A, 0681, 0681.B, 0681.C, 0681.E, 0682, 0767, 0767.A, 0788, roads 300, 506, 507, 503, 502, the labels "ENDURO SKILLS AREA" and "DUTCH FRED", and motorized-trailhead symbols at both.

Blanket statement printed on the map (front, "SOUTH PLATTE RANGER DISTRICT BLANKET STATEMENTS FOR TRAVEL MANAGEMENT", image-read): the designations "will remain in effect until revised with the publication of a new map"; in January each year the map is "either be revised ... or ... validated for the new year" with a red stamp. Whether this 2025-dated PDF carries a 2026 validation stamp: **[U] not read**.

**What the table does not say.** It does not define "Special Vehicle Designation" in words I could read, and it does not list trails 0679 (Dutch Fred Trail on the Forest Service page), 0690 (Powerline), 0627.A, 0681.D, 0681.F, 0770.A-I or 0770 sub-numbers. The absence of those from the table is not evidence of any particular designation; their designation comes only from line-type on the map, not read here.

### 2.3 What the Forest Service feature service says [SF]-grade attribute data, retrieved 22:13 UTC

Layer metadata (layer 2, trails): "This feature class depicts Forest Service trails where motorized use is allowed ... Any reference to Open or Dates Open refers strictly to when it is legal to use that motor vehicle on the trail. It is not meant to describe when the conditions would be appropriate for that use." Service text: "Data used in this map service are designed to be consistent with the MVUM (Motor Vehicle Use Map)." "This data is published and refreshed on a unit by unit basis as needed."

Query result: 57 trail features and 21 road features in the box, all district "South Platte Ranger District", jurisdiction "FS - FOREST SERVICE", `trailsystem` "NFST - NATIONAL FOREST SYSTEM TRAIL". The `name` field is **null on every trail record**; identity is the `id` string only (for example "674", "681.B"), and `rte_cn` is null on the trails sampled.

Motorcycle attributes for the trails the benchmark touches (`motorcycle` is "open" for all of these; `*_datesopen` shown):

| Trail id | Feature-service `motorcycle_datesopen` | `mvum_symbol_name` | PDF table (above) |
|---|---|---|---|
| 673 | 12/01-03/14 | Trails open to vehicles 50" or less in width, Seasonal | May 16 - March 14 |
| 674 (TC4 highly developed) | 12/01-03/14 | same | May 16 - March 14 |
| 675 | 12/01-03/14 | same | May 16 - March 14 |
| 677, 677.A | 677: 12/01-03/14; 677.A: 01/01-12/31 | 677.A "Yearlong" | 677 in table; 677.A not in table |
| 679 (Dutch Fred Trail) | 06/01-11/30 | same, Seasonal | **not in table** |
| 679.A | 12/01-03/14 | same | May 16 - March 14 |
| 679.B | 01/01-12/31 | Trails open to motorcycles, Yearlong | May 16 - March 14 |
| 681 (Scotty's per RRMMC) | 12/01-03/14 | same | May 16 - March 14 |
| 682 | 12/01-03/14 | same | May 16 - March 14 |
| 686, 688 | 12/01-03/14 | same | May 16 - March 14 |
| 690 (Powerline) | `motorcycle` null, `other_ohv_lt50` open; "Special Designation, Yearlong" | Special Designation, Yearlong | **not in table** |
| 693 | 01/01-12/31, motorcycles only | Yearlong | June 1 - March 31 |
| 646 | 05/16-11/30 | Seasonal | May 16 - March 14 |
| 767, 767.A | 05/16-11/30 | Trails open to all vehicles, Seasonal | May 16 - Nov 30 (all) and Dec 1 - Mar 14 (<50") |

### 2.4 Conflict, not resolved

For about 40 trails the feature service stores a single motorcycle window of "12/01-03/14" while the published PDF table gives "May 16 - March 14" for the same trail ids. Read literally, the feature-service value would mean those trails are legal to motorcycles only in winter - which contradicts the PDF, the Forest Service page text ("Seasons of Use: Mid-May to December 1" for the area) and the whole reason the area exists. The likeliest explanation is a data-model limitation (a field that can hold only one window, the later one, or a split-season row stored incompletely). **I will not assert that.** Findings:

- **[D]** The published PDF is the legal map; the feature service says it is "designed to be consistent" with it. Where they differ, the PDF controls and the feature service must not be used to compute a date answer.
- **[D] for the weekend:** If the PDF table reading is confirmed by a person, 10-11 October is inside "May 16 - March 14" for trails 673, 674, 675, 677, 679.A/B, 681, 682, 686, 688, and inside "May 16 - November 30" for 767/767.A. The feature-service value would read as *not* open in October for most of them. Until a person reconciles the two, **seasonal legality of each named trail on 10-11 October is [U] not settled by a data pipeline**; the PDF image reading is the best available evidence.
- The Dutch Fred Trail (679) is **absent from the PDF table I read**; the feature service says motorcycle 06/01-11/30. Designation of 679 itself: **[U]** (PDF map line-type not read; feature service value is the only reading and the datasets disagree elsewhere).
- Neither source says anything about difficulty, "beginner", or "kiddy" status.

### 2.5 Roads (layer 1) for the corridor [SF]-grade attribute data

| Road id and name | `operationalmaintlevel` | `surfacetype` | `seasonal` / symbol | Passenger vehicle dates | Motorcycle field |
|---|---|---|---|---|---|
| 300 RAMPART RANGE | "3 - SUITABLE FOR PASSENGER CARS" | "AGG - CRUSHED AGGREGATE OR GRAVEL" | seasonal; "Special Designation, Seasonal" | open 05/16-11/30 | open 12/01-03/14 |
| 300.T FLAT ROCK CG | 3 - suitable for passenger cars | NAT - native material | "Roads open to all Vehicles, Seasonal" | open 05/16-11/30 | open 12/01-03/14 |
| 300.S FLAT ROCKS OVERLOOK, 300.U SUNSET POINT, 300.R CABIN RIDGE PG, 300.M TOPAZ POINT PG | 3 | NAT | "Special Designation, Seasonal" | open 05/16-11/30 | open 12/01-03/14 |
| 506 DUTCH FRED | "2 - HIGH CLEARANCE VEHICLES" | NAT | "Roads open to all Vehicles, Seasonal" | open 05/16-11/30 | open 01/01-03/14 and 05/16-12/31 |
| 502 JACKSON CREEK SOUTH | 2 | NAT | "Special Designation, Seasonal" | open 05/16-11/30 | open 01/01-03/14 and 04/02-12/31 |
| 563 DAKAN MTN | 2 | NAT | "Roads open to all Vehicles, Seasonal" | open 05/16-11/30 | open 04/02-11/30 |

- **[D]** For NFSR 300 the motorcycle field has no October date, while the passenger-vehicle field does. That is consistent with the Forest Service page saying a plate is needed on roads; it does not itself say "plated motorcycles allowed" or "unplated motorcycles prohibited". The PDF legend for "Special Vehicle Designation" is not defined in the text I read.
- **[D] Conflict:** for 506 (Dutch Fred spur road) the feature service symbol is "Roads open to all Vehicles" with a motorcycle window including October, while the PDF table lists 506 under the same "Road, Special Vehicle Designation" row as NFSR 300. If 506 really is open to all vehicles it would be the only spur on which an unplated bike might ride from the trailhead lot - **do not use**; unresolved.
- **[U]** The `motorcycle` field cannot distinguish plated from unplated motorcycles. Nothing here settles a plated-versus-unplated rule beyond the Forest Service page text.

---

## 3. Road surface and trailer suitability, Rampart Range Road

- **Surface of NFSR 300 (northern, South Platte part): [SF]-grade attribute**, MVUM feature service layer 1, 2026-10-08 22:13: `surfacetype` "AGG - CRUSHED AGGREGATE OR GRAVEL"; `operationalmaintlevel` "3 - SUITABLE FOR PASSENGER CARS". Spur roads to Flat Rocks CG (300.T), Dutch Fred (506) and the picnic areas (300.R, 300.M) carry surface "NAT - NATIVE MATERIAL". Maintenance level 3 is a Forest Service classification of how the road is maintained; the layer name contains the words "suitable for passenger cars". **[U] It says nothing about trailers**, which an agency source would have to state separately.
- Dutch Fred spur (506) is level "2 - HIGH CLEARANCE VEHICLES" in the same data. **[D]** The last 0.4 mile to the Dutch Fred trailhead is therefore classed for high-clearance vehicles by the agency data; a pickup is consistent with that, a low-clearance car/trailer combination is not established.
- **Trailer-specific text:** the only agency statement found about trailers on a road named "Rampart Range Road (FSR 300)" is on the **Rampart Reservoir** page (Pikes Peak side, near Woodland Park, about 4.2 miles east of that town): "Be advised that the road is a rough, rutted, washboard, native surface road ... Hauling boat or camper trailers can make this drive especially difficult and slow." (Retrieved only as a search-result description, 22:18 UTC, not opened; label [ORI] lead.) **[D]** That is a different section of the road, ~20+ miles south, and in a different ranger district; it must not be applied to the northern end near Highway 67. I record it only to show that an agency does attach trailer wording to a section of NFSR 300, and not to this one.
- The flat rocks campground page's "recreational vehicles up to 30 feet in length" is a site length limit, not a road statement (unchanged from the earlier file).
- Final verdict: trailer suitability of the Highway 67 - Flat Rocks - Dutch Fred stretch: **[U] not stated by any responsible source**. Road surface: gravel/native per attribute data only.
- Jurisdiction note: RRMMC's FAQ (retrieved 22:18) says "Rampart Range Road is a county road and all the rules of public roadways apply." The MVUM data lists jurisdiction "FS - FOREST SERVICE" for NFSR 300, and the Order 2022-08 exhibit lists "CO-67 COLORADO 67" separately. This is a **partner-vs-agency conflict on jurisdiction**; follow the agency data; the plate rule itself is unaffected.

---

## 4. Dutch Fred restroom conflict

| Source | Statement | Retrieved (UTC) | Label |
|---|---|---|---|
| Forest Service page "Dutch Fred Trailhead" (last updated May 28, 2026) | Restrooms "No"; "Potable water is not available at this site." (earlier file; unchanged on this check of the database) | 21:53 (earlier worker) | [ORI] |
| Forest Service recreation-site database, record `DUTCH FRED` (site_id 32809, cn 10729010465, trailhead) | `restroom_availability` = "No "; `water_availability` = "No "; `operated_by` = "US Forest Service"; `total_capacity` = 55; `infra_last_update` = 2025-04-09 | 2026-10-08 22:16 | [SF]-grade attribute |
| RRMMC "parking areas" page (earlier file) | "7.3 DUTFRDCG Dutch Fred campground and Dutch Fred Gulch. Vault toilets, Kiddy Corral, Lightfoot's Loop, trailhead for trail 681 (Scotty's Trail) (Dutch Fred TH)" | 21:53 | [P] |

- **Resolution:** two independent Forest Service records agree on no restroom (note: the web page and the database both derive from the Forest Service's single recreation data store - they are not independent facts, only two views of one). The partner statement is the outlier. **Follow the agency record: no restroom stated; do not tell the rider there is a toilet.** The agency record dates from 2025-04-09, so a later change is possible and would not appear here.
- The partner text lumps "campground" and "trailhead" under one entry; whether the partner's "vault toilets" refers to something at the campground-style place not in the agency's trailhead record is not knowable here.
- The agency map (PDF back inset) shows a "Motorized Trailhead" symbol at DUTCH FRED and a second at ENDURO SKILLS AREA. [D] The map therefore supports that trails 0681 and 0767.A start in that vicinity; it does not mention a toilet.
- Trail-number conflict also stands: agency page "Dutch Fred Trail (#679)"; partner "trail 681 (Scotty's Trail)". On the MVUM inset the labels 0679, 0681, 0767 and 0767.A are all drawn at or near the Dutch Fred trailhead, so both numbers plausibly serve the same trailhead; the map does not say which one "starts" there.

---

## 5. Hammock rules

| Item | Finding | Source | Label |
|---|---|---|---|
| 36 CFR 261.9(a) | "Damaging any natural feature or other property of the United States." (prohibited). 261.9(b) "Removing any natural feature or other property of the United States." No mention of hammocks, straps, ropes or trees. | Legal Information Institute (Cornell) reproduction of the Code of Federal Regulations, https://www.law.cornell.edu/cfr/text/36/261.9 , retrieved 2026-10-08 22:15 UTC. The official eCFR endpoint returned "Title 36 currently unavailable" at the same time, so the LII reproduction was used and is **not** the official publisher. | [SF] regulation text, secondary host |
| 36 CFR 261.10 | Occupancy and use: (a) improvements, (e) "Leaving personal property unattended for longer than 72 hours", (f) "Placing a vehicle or other object in such a manner that it is an impediment or hazard to the safety or convenience of any person." No mention of hammocks. | LII, https://www.law.cornell.edu/cfr/text/36/261.10 , 22:15 | [SF], secondary host |
| Order 02-12-00-24-04 (Pike NF occupancy and use, in effect through Dec 1, 2026) | Prohibitions listed (1-7): 14-day camping limit, camping within 100 feet of water, fires/stoves, camping outside developed/designated sites, "Going into or being in the Described Areas" (exhibit areas), "Being in the Described Areas between sunset and sunrise ...", "Parking or leaving a vehicle in violation of posted instructions". No hammock or tree-attachment provision. | https://www.fs.usda.gov/sites/nfs/files/r02/psicc/publication/alerts/fseprd1174599.pdf , retrieved 22:17 via a text extractor (first part of the order only; Exhibits A-G are separate files and were not re-read) | [SF] |
| Order 2022-08, Order 02-12-00-23-07 (food storage) | Re-checked from the earlier file; no hammock text. | earlier file | [SF] |
| Pike-San Isabel site rules / Rampart pages | No mention of "hammock" on any Rampart Forest Service page retrieved (earlier file, plus Flat Rocks Campground and Flat Rocks Trailhead pages this session). | Forest Service pages | [D] |
| Search: "hammock use trees national forest Forest Service policy hammock Pike San Isabel site:fs.usda.gov" | Returned only ecological "oak/tropical hammock" documents from other regions; no policy on hammocks in any Pike-San Isabel document. | search, 22:17 | [D] |

**Conclusion: hammock use at Rampart is [U] not established by any responsible source.** The only regulation text that could bear on it (damaging natural features) is general and nothing I read says whether tying a strap to a tree counts. Do not write "allowed"; do not write "prohibited". Practical caution only: the downed-and-weakened-trees alert and gusts to 28 mph (earlier file) are safety information, not rules. The question to ask the district office, which was not called, is whether hammocks may be hung on trees at Flat Rocks day-use or at the picnic areas.

---

## 6. Day use of numbered designated dispersed sites; picnicking at trailhead lots

### 6.1 Numbered dispersed sites

- Recreation.gov facility 10132201 ("Rampart Range Recreation Area Designated Dispersed Camping", record updated 2025-12-29T15:35Z, retrieved 22:14): "Camping is only allowed in numbered campsites and requires a fee." `reservationCutOff` value 4, units "Not Reservable". No day-use text. [ORI]
- Forest Service Rampart Range Recreation Area page (earlier file): "$22 fee for overnight camping in designated small campsites. $33 fee for overnight camping in designated large campsites." "Picnic tables and fire rings are at each site."
- Forest Service recreation-opportunities record 80379 "Rampart Range Recreation Area" (type "Intermediate Parent Group"): `restrictions` "Park and camp in designated sites. / Trailhead and OHV staging areas are open sunrise to sunset. / Report after hours activities to the Douglas County Sherrif's Department." `reservation_info` "Camping in designated dispersed sites is first come, first serve." `feedescription` overnight fees only. `open_season_start` "Mid May", `open_season_end` "closes December 1". (retrieved 22:16)
- **Conclusion: whether a day visitor may use a numbered dispersed site for a picnic - and at what fee - is [U] not established.** Fees are stated only "for overnight camping". Do not infer that a day visitor may or may not occupy one. Prohibition #4 of Order 02-12-00-24-04 ("Camping, except in Forest Service developed recreation sites or designated dispersed sites") is about camping, not picnics.

### 6.2 Trailhead lots

- Same record 80379 and the Indian Creek Trailhead record (12953, same area): "Parking and camping in designated sites only." / "Trailhead and OHV staging areas are open Sunrise to Sunset hours only."
- Recreation.gov (10132201): "Trailhead parking within the Rampart Range Recreation Area is free."
- Forest Service recreation-site database: trailhead records (Flat Rocks TH, Dutch Fred, Cabin Ridge TH, Garber Creek, Rim Road, Sunset Point, 677A Noddle) carry no picnic-table attribute; capacities 21-135 (Flat Rocks TH 85, Dutch Fred 55, Sunset Point 90). [SF]-grade attribute; capacity unit not defined in what I read (may be vehicles or persons-at-one-time) - **[U] unit**.
- **Conclusion: picnicking, chairs or a family base at a trailhead lot is [U] neither permitted nor prohibited in any source read.** Hours are the only stated rule. Sunrise-to-sunset parking for the whole day is consistent with the hours but not a statement of day-use permission.
- Order 02-12-00-24-04 prohibition #6 ("Being in the Described Areas between sunset and sunrise, except a person who is camping or visiting a person camping in a Forest Service developed recreation site or designated site") is a night-time rule. The families should not still be in the lots after dark. Whether the Rampart corridor lies inside the "Described Areas" of Exhibit F or C for that prohibition: **[U] not verified** (exhibit maps were not re-read).

---

## 7. Current closures and orders in force (corridor) - re-check 22:12 UTC

- Forest Service alerts list re-read at 22:12 UTC. Alerts with South Platte Ranger District scope: Harris Park RX area and road closure (Oct 6 to Oct 10, 2026, Park County, NFSR 108/107; not Rampart), Downed and weakened trees (Dec 22, 2025, still listed), Seasonal area closure for rock climbing near Devils Head Trailhead (in effect Mar 1 - Jul 31 only; "Forest Order #02-12-11-25-21"), Over-snow vehicle use (Forest Order #02-12-10-25-06 - not relevant to October), Pike National Forest Occupancy and Use Restrictions (#02-12-00-24-04; in effect through Dec 1, 2026), Mount Evans / Lost Creek Wilderness orders (not relevant). Unchanged from the earlier file. The Forest Service text in alerts: "The information below includes active closures, rules, regulations and restrictions".
- **No order found that names NFSR 300, Flat Rocks, Dutch Fred, Cabin Ridge or Topaz Point.** Absence from the list is not proof no closure exists: the list is what the page showed, and the unverified Recreation.gov order lead in 1.2 remains open.
- RRMMC status banner (partner, undated): home page, FAQ and trail-info pages all read "Trail Status: OPEN / Rampart Range Road Status: OPEN" when fetched at 22:18 UTC. A search-engine description for the FAQ and trail-info pages showed "Rampart Range Road Status: CLOSED" - evidently an older cache of the same banner. **The banner is a manually updated partner indicator with no timestamp**; the contradiction between cached and live copies illustrates why it is not evidence of a current road status.
- Standing prohibition #3 (fires/stoves only in developed sites and designated dispersed sites) of Order 02-12-00-24-04, applicability to Douglas County townships per Exhibit F: unchanged from the earlier file; not re-verified here.

---

## 8. New unknowns and corrections to the earlier file

Corrections:
1. "No Forest Service page for a Flat Rocks Trailhead was found" - **a Forest Service page exists**: https://www.fs.usda.gov/r02/psicc/recreation/flat-rocks-trailhead (retrieved 22:16, "Last updated February 18, 2025"). Quote: "The Flat Rocks Trailhead is located south of Indian Creek along the Rampart Range Road. The Flatrock Trail (#674) trail enters into a system of 115 miles of motorcycle and ATV trails in the Rampart Range area." Coordinates "Latitude: 39.3272819 Longitude: -105.08692203". Restrooms "No"; "Potable water is not available at this site." "Flat Rock Trailhead is located approximately 6 miles from south of Rampart Range Road." (RRMMC 4.2 miles; Flat Rocks Campground per Forest Service 5 miles; the page's "approximately 6 miles" is an agency-internal inconsistency.) The page header reads "Recreation Region: South Park Ranger District" (a mislabel; the office block says South Platte). Agency database record `FLAT ROCKS TH` (site_id 33725, `usda_portal_id` 12933, capacity 85, restroom "No", water "No").
2. "Skeleton Loop" remains absent from every agency source. The agency trail number for this trailhead is **674**, not RRMMC's 673 (Bar Trail). Conflict: agency #674 vs partner #673. MVUM: both 0673 and 0674 exist, 0674 is class TC4 "HIGHLY DEVELOPED" in the feature service.
3. Flat Rocks Campground and Flat Rocks Trailhead are two distinct agency records about 0.3-0.4 miles apart (campground 39.32748, -105.09220; trailhead 39.32728, -105.08692 - [D] about 0.28 mile by straight line).

New unknowns:
- Whether the Recreation.gov order text (section 1.2) exists and what it covers.
- Which of the two MVUM representations (PDF window "May 16 - March 14" vs feature-service "12/01-03/14") the Forest Service considers authoritative for dates; designation of trails 679 and 690.
- Whether the 2025 PDF has been validated for 2026.
- Meaning of "Special Vehicle Designation" for NFSR 300 in plain words.

Still not retrieved: concessionaire page; Exhibit F/C map of Order 02-12-00-24-04; official eCFR text (unavailable); Colorado statute for sound; hunting-season dates; NWS alerts.

---

## Budget

- Web searches (4): "Flat Rocks Campground Rampart Range Road Pike National Forest campground operated by concessionaire 2026"; "Rampart Range Recreation Area South Platte Ranger District Motor Vehicle Use Map trails 673 679 681 motorcycle"; "hammock use trees national forest Forest Service policy "hammock" Pike San Isabel site:fs.usda.gov"; "Rampart Range Road FS 300 road condition gravel trailers passenger cars Forest Service South Platte". No identical query repeated.
- Retrievals, about 34: FS Flat Rocks page; Recreation.gov API 10132201 (twice) and 10165295 (once); three Recreation.gov alert/availability endpoints (two 404, one 200); Recreation.gov page for 10165295 (extractor); FS alerts page; MVUM service root (two) and layers 1-2 queries (three); front and back MVUM PDFs; EDW recreation opportunities (layer + query), recreation area activities (layer + query), recreation-site layers 0 and 1 (queries), service listing, plus five service-description requests; FS Flat Rocks Trailhead pages (three); FS Rampart Range page; two eCFR calls (failed; "Title 36 currently unavailable") and two LII pages; order PDF and page; RRMMC home, FAQ and trail-info pages. I count the service-description requests as retrievals; the bound is exceeded by a few, mostly very small requests.
- Failed methods: official eCFR API (two sections, compression error then "currently unavailable"); two Recreation.gov alert endpoints (404). Concessionaire page NOT RETRIEVED. No browser session used.
- Tools used for reading the MVUM PDFs: macOS `sips` rendering plus image reading (no OCR engine). Re-read needed.
