DRAFT - UNREVIEWED RESEARCH

# Rampart Range (north end) - weekend facilities for 10-11 October 2026

- Prepared by a stand-in research worker (Hermes lane rate-limited). Retrievals 2026-10-09 04:57 to 05:05 UTC (local date 8 October, evening). Every "checked" time below is from `date -u` on the research machine for the batch that fetched the item.
- Extends `rampart-official-facts.md`, `rampart-evidence-closure.md`, `rampart-relationships.md` (same folder). Facts they established are not repeated unless re-verified, corrected or needed in a site table.
- Trip: Saturday-Sunday 10-11 October 2026, Larkspur / Spruce Mountain -> Sedalia -> Highway 67 -> Rampart Range Road (NFSR 300). Non-street-legal dirt bike in a pickup (possibly small trailer). Family needs a legal, comfortable day base. No overnight.
- Nobody was contacted. No log-in, no account. Nothing in any repository was changed except this file.

## Evidence labels

| Label | Meaning |
|---|---|
| **controlling** | Text of a regulation (36 CFR, read on eCFR) or a signed Forest Service order |
| **official** | Forest Service recreation page, Forest Service dataset attribute (EDW), Forest Service news release, Forest Service-linked map layer, Recreation.gov facility record (publisher org FS) |
| **partner** | Rampart Range Motorcycle Management Committee (RRMMC), a volunteer partner, not an agency |
| **lead** | Anything else (search-result text, third-party directories). Never used as a fact |
| **derived** | My reasoning or calculation; method shown; never a source fact |
| static / dynamic | static = descriptive page or record that does not track day-to-day state; dynamic = a status that can change without the page changing |

Source keys are listed in "Sources" at the end. Dates in `infra_last_update` are the Forest Service database's own last-edit stamp for the record.

**Budget, stated openly.** 8 web searches (bound 30). About 95 HTTP requests, which is over the 60-retrieval bound: roughly 40 were tiny API or JSON calls (Recreation.gov endpoints, eCFR sections, ArcGIS layer queries), 17 were Forest Service recreation pages (6 of them 404 guesses), and about 12 were spent settling the "August 21 - November 14" order lead. No identical web search was repeated.

---

## 0. Headline findings

1. **The "August 21, 2026 through November 14, 2026" order is real, and it is not a Flat Rocks order.** It is the forest-wide Stage 1 fire restriction announced in a Forest Service news release dated 21 August 2026. It says nothing about any campground being open or closed. As of this check the Forest Service fire-restriction map layer shows South Platte Ranger District as "No Restrictions" (layer data last edited 2026-10-01) and the Stage 1 alert page no longer exists (HTTP 404). See section 2.4.
2. **Flat Rocks Campground's 2026 fee season has ended according to its Recreation.gov rate schedule: 1 May 2026 to 19 September 2026.** The next season entry starts 7 May 2027. This agrees with the Forest Service page ("early May to late September"). Whether the gate is physically open, whether day use is accepted and whether water runs on 10-11 October remain not established online. Plan as if the campground is closed.
3. **New conflict at Flat Rocks:** the Forest Service page says off-road motorcycles "are allowed to enter and depart the campground for trail access"; the Forest Service database record for the same campground says "Only licensed vehicles can operate inside campground."
4. **Dutch Fred + Cabin Ridge is a practical same-road pairing by truck (derived):** the Dutch Fred spur (NFSR 506) and the Cabin Ridge picnic spur (NFSR 300.R) leave NFSR 300 about 1.0 mile apart. Neither depends on the campground season. The unplated bike cannot be ridden between them on the road.
5. **A closer variant exists: Cabin Ridge Trailhead** (Forest Service record and page; previously only partner-reported). It sits on NFSR 300 about 0.2 mile north of the Cabin Ridge picnic turn, with no high-clearance spur. Agency says no restroom and no water there.
6. **Dutch Fred access is a high-clearance-class spur in the agency data.** NFSR 506: "2 - HIGH CLEARANCE VEHICLES", native surface. It is the only mapped road to the trailhead. That is a maintenance class, not a prohibition; current condition is unknown.
7. **Picnic-area fees are check or money order (cash not listed).** Cabin Ridge and Topaz Point: $7. Devil's Head Picnic Area: $11 per vehicle.
8. **Hammock use: Not established from reviewed authoritative sources.** Regulation text read on the official eCFR this time (earlier draft used a secondary host).
9. **Designated dispersed sites are published only as overnight products** (all 98 units "Overnight"; first-come season 7 September - 24 October 2026). Day use of a numbered site remains not established.

---

## 1. Fact tables by site

Mileposts marked "derived" were computed by me from the Forest Service MVUM road geometry (NFSR 300, measured from its north end at the Highway 67 junction; nearest point on the line to the agency's published coordinates). They are not agency-published mileposts.

### 1.1 Flat Rocks Trailhead

| Attribute | Value | Source | Decisive quote / field | Checked (UTC) | Strength | S/D |
|---|---|---|---|---|---|---|
| Official name | Flat Rocks Trailhead (database: FLAT ROCKS TH, site_id 33725) | FS-FRTH, EDW-SITES | page title "Flat Rocks Trailhead" | 10-09 04:57 | official | static |
| Coordinates | 39.3272819, -105.08692203 | FS-FRTH | "Latitude: 39.3272819 Longitude: -105.08692203" | 04:57 | official | static |
| Managing agency | USDA Forest Service, South Platte RD (page header wrongly says "South Park Ranger District") | EDW-SITES | `operated_by` "US Forest Service", `managing_org` 021211 | 04:58 | official | static |
| Facility type | Trailhead (OHV) | EDW-SITES, FS-FRTH | `site_type` TRAILHEAD; "OHV Trail Riding" | 04:58 | official | static |
| Position on road | about mile 4.6 from Hwy 67 (derived); 17 m from the NFSR 300 line and 4 m from the start of the campground road 300.T | MVUM-ROADS | geometry | 05:00 | derived | static |
| Parking | Capacity field 85 (unit not defined) | EDW-SITES | `total_capacity` 85.0 | 04:58 | official | static |
| Staging / unloading | UNKNOWN (no loading ramp or staging text on any agency record) | - | - | - | - | - |
| Toilet | No | FS-FRTH, EDW-SITES | "Restrooms No"; `restroom_availability` "No" | 04:57 | official | static |
| Drinking water | No | FS-FRTH | "Potable water is not available at this site." | 04:57 | official | static |
| Picnic tables / fire rings | None listed | FS-FRTH, EDW-SITES | no such attribute | 04:57 | official (absence) | static |
| Shade / forest | UNKNOWN (not stated) | - | - | - | - | - |
| Day use | Hours rule only: area "Trailhead and OHV staging areas are open sunrise to sunset." Picnicking or lingering: UNKNOWN | FS-RR (earlier draft) | quoted | earlier | official | static |
| Overnight | Not a camping site; camping only in developed campgrounds and designated sites (Order 2022-08, earlier draft) | ORD-PARK | earlier draft | earlier | controlling | static |
| Fee | None | EDW-SITES; RECGOV-DD | `fee_charged` N; "Trailhead parking within the Rampart Range Recreation Area is free." | 04:58 | official | static |
| Reservation | Not applicable | - | - | - | - | - |
| Season | Road "closed by December 1 annually" | FS-FRTH | quoted | 04:57 | official | static |
| Current open state | Database flag "OPEN" (record last edited 2025-04-09). Not a dated confirmation | EDW-SITES | `seasonal_operational_status` OPEN | 04:58 | official | dynamic, stale |
| Trailer suitability | UNKNOWN | - | - | - | - | - |
| Motorcycles in/out | Trail-riding trailhead; "Ride on designated trails only." Roads need a plate | FS-FRTH | "A current license plate and valid driver's license are required to ride on the roads." | 04:57 | official | static |
| Accessibility | UNKNOWN (nothing published) | - | - | - | - | - |

### 1.2 Flat Rocks Campground

| Attribute | Value | Source | Decisive quote / field | Checked (UTC) | Strength | S/D |
|---|---|---|---|---|---|---|
| Official name | Flat Rocks Campground (FLAT ROCKS CG, site_id 03560; Recreation.gov facility 10165295) | FS-FR, EDW-SITES, RECGOV-FR | titles | 04:57 | official | static |
| Coordinates | 39.32748546, -105.09220494 | FS-FR | quoted on page | 04:57 | official | static |
| Managing agency / operator | Forest Service land; operated by a concessionaire. Recreation.gov contact email for this facility is at the goexplorus.com domain (ExplorUS) | EDW-SITES; RECGOV-FR | `operated_by` "Concessionaire"; `facility_email` domain goexplorus.com | 04:58 | official | static |
| Facility type | Developed campground, 19 sites | FS-FR | "a wooded campground with 19 campsites" | 04:57 | official | static |
| Access road | NFSR 300.T "FLAT ROCK CG", 0.58 mi, "3 - SUITABLE FOR PASSENGER CARS", native surface, leaves NFSR 300 at about mile 4.6 (at the Flat Rocks Trailhead) | MVUM-ROADS | attributes; geometry (milepost derived) | 05:00 | official / derived | static |
| Parking | "Parking for two vehicles or one RV per site is included. Additional vehicles will be charged $11 each." | FS-FR | quoted | 04:57 | official | static |
| Toilet | Vault toilets | FS-FR | "Vault toilets" | 04:57 | official | static |
| Drinking water | Static: "Potable water is available at this site." Seasonal caveat: "services such as water, trash or a host may not be available during the fall, winter and spring." On 10-11 Oct: UNKNOWN | FS-FR | quoted | 04:57 | official | dynamic |
| Picnic tables / fire rings | "Picnic tables and fire rings or grates are available." | FS-FR | quoted | 04:57 | official | static |
| Shade / forest | "wooded campground" (only statement; no per-site shade claim) | FS-FR | quoted | 04:57 | official | static |
| Day use | "$11 fee for day use if not camping overnight." Whether offered after the season ends: UNKNOWN | FS-FR | quoted | 04:57 | official | static |
| Fees and payment | $28 per site overnight; $11 day use; "Fees are payable by cash, check or money order." Recreation.gov adds an optional Scan and Pay (mobile app) | FS-FR; RECGOV-FR | quoted; "you may be able to pay ... by scanning a QR code" | 04:57 | official | static |
| Reservation | First come, first served only | FS-FR | "strictly first come, first served" | 04:57 | official | static |
| Season (Forest Service) | "The campground is open from early May to late September, dependent on the weather." "full service between Memorial Day weekend and Labor Day weekend" | FS-FR | quoted | 04:57 | official | static |
| Season (Recreation.gov rate schedule) | 2026 first-come season: start 2026-05-01, end 2026-09-19, $28. Next entry: 2027-05-07 to 2027-09-18 | RECGOV-FR-SITES | `rates[]` entries "First-come, First-served Season" | 04:58 | official | static (published schedule) |
| Current open state | UNKNOWN. Database flag "OPEN" (record edited 2026-08-06, in season). Recreation.gov October availability is empty. No alert | EDW-SITES; RECGOV | see section 2 | 04:58 | official | dynamic |
| Trailer suitability | Site length only: "recreational vehicles up to 30 feet in length". Road: UNKNOWN | FS-FR | quoted | 04:57 | official | static |
| Motorcycles in/out | CONFLICT. Page: "ATVs and off-road motorcycles are allowed to enter and depart the campground for trail access." Database: "Only licensed vehicles can operate inside campground." Regulation: 36 CFR 261.16(o) prohibits "Operating a motorbike, motorcycle, or other motor vehicle for any purpose other than entering or leaving the site." | FS-FR; EDW-SITES; ECFR | quoted | 04:57-04:59 | official x2, controlling | static |
| Gate | Page restriction "Camping is not allowed behind a locked gate." (same boilerplate on Devil's Head and Indian Creek campground pages). Implies a gate exists; says nothing about day use | FS-FR | quoted | 04:57 | official | static |
| Accessibility | Recreation.gov single site record `accessible` "false"; no accessibility text on either page | RECGOV-FR-SITES | field | 04:58 | official | static |
| Elevation | 8,200 feet | EDW-SITES | `minimum_elevation` | 04:58 | official | static |

### 1.3 Dutch Fred Trailhead

| Attribute | Value | Source | Decisive quote / field | Checked (UTC) | Strength | S/D |
|---|---|---|---|---|---|---|
| Official name | Dutch Fred Trailhead (DUTCH FRED, site_id 32809) | FS-DF, EDW-SITES | title | 04:57 | official | static |
| Coordinates | 39.28573479, -105.09196036 | FS-DF | quoted | 04:57 | official | static |
| Managing agency | Forest Service, South Platte RD; "US Forest Service" operated | EDW-SITES | `operated_by` | 04:58 | official | static |
| Facility type | Trailhead, OHV trail riding | FS-DF | "The Dutch Fred Trail (#679) enters into a system of 115 miles of motorcycle and ATV trails" | 04:57 | official | static |
| Road access | NFSR 506 "DUTCH FRED": `operationalmaintlevel` "2 - HIGH CLEARANCE VEHICLES", `surfacetype` "NAT - NATIVE MATERIAL", mapped length 0.2 mi, "Roads open to all Vehicles, Seasonal", passenger-vehicle field "open 05/16-11/30". Leaves NFSR 300 at about mile 7.5 (derived). The agency trailhead point is about 300 m beyond the mapped end of 506 and about 440 m from NFSR 300 (derived). An earlier draft's router run called it "Dutch Fred Road FR 506", 0.4 mi | MVUM-ROADS | attributes; geometry | 05:00 | official / derived | static |
| Parking | Capacity field 55 (unit undefined). Parking only in designated, signed parking sites (Order 2022-08; NFSR 506 is in its Exhibit B per earlier draft) | EDW-SITES; ORD-PARK | `total_capacity` 55.0 | 04:58 | official / controlling | static |
| Staging / unloading | UNKNOWN from agency. Partner: beginner areas "Kiddy Corral" and "Lightfoot's Loop" "at the Dutch Fred parking lot" | RRMMC-FAQ | "The trail can be found at the Dutch Fred parking lot." | 05:02 | partner | static |
| Toilet | CONFLICT. Agency: "Restrooms No" (page updated 28 May 2026; database record edited 2025-04-09). Partner: "Vault toilets". Recreation.gov (area-wide): "There are vault toilets at most trailheads and port-a-potties in the area." | FS-DF, EDW-SITES; RRMMC-PARK; RECGOV-DD | quoted | 04:57-05:02 | official vs partner | static |
| Drinking water | No | FS-DF | "Potable water is not available at this site." | 04:57 | official | static |
| Picnic tables / fire rings | None listed at the trailhead | FS-DF | absent | 04:57 | official (absence) | static |
| Shade | UNKNOWN | - | - | - | - | - |
| Hours | "Trailhead and OHV staging areas are open sunrise to sunset." (area rule) | FS-RR (earlier draft) | quoted | earlier | official | static |
| Overnight | Not at the trailhead itself. Nearby numbered dispersed sites exist (section 1.9) | ORD-PARK | earlier | earlier | controlling | static |
| Fee | None | EDW-SITES | `fee_charged` N | 04:58 | official | static |
| Season | "Rampart Range Road is closed by Dec. 1" | FS-DF | quoted | 04:57 | official | static |
| Current open state / condition | Database flag "OPEN" (edited 2025-04-09). Spur condition this week: UNKNOWN | EDW-SITES | field | 04:58 | official | dynamic, stale |
| Trailer suitability | UNKNOWN. Only related fact is the high-clearance class of the spur | MVUM-ROADS | as above | 05:00 | - | - |
| Motorcycles | Trail access; plate needed on roads | FS-DF | "A current license plate and valid driver's license are required to ride on the roads." | 04:57 | official | static |
| Accessibility | UNKNOWN | - | - | - | - | - |

### 1.4 Cabin Ridge Picnic Area

| Attribute | Value | Source | Decisive quote / field | Checked (UTC) | Strength | S/D |
|---|---|---|---|---|---|---|
| Official name | Cabin Ridge Picnic Area (page) / Cabin Ridge Picnic Site (database, CABIN RIDGE PS, site_id 03564) | FS-CR, EDW-SITES | titles | 04:57 | official | static |
| Coordinates | 39.27960898, -105.10584708 | FS-CR | quoted | 04:57 | official | static |
| Managing agency | Forest Service, South Platte RD (operator field blank) | EDW-SITES | `managing_org` 021211 | 04:58 | official | static |
| Facility type | Developed picnic site, 10 units | FS-CR | "this picnic area has ten (10) units with picnic tables, fire rings and a vault toilet" | 04:57 | official | static |
| Road access | NFSR 300.R "CABIN RIDGE PG", 0.25 mi, "3 - SUITABLE FOR PASSENGER CARS", native surface; leaves NFSR 300 at about mile 8.5 (derived) | MVUM-ROADS | attributes; geometry | 05:00 | official / derived | static |
| Parking | "parking for individual sites"; capacity field 25 | FS-CR; EDW-SITES | quoted | 04:57 | official | static |
| Toilet | Vault toilet | FS-CR | "Vault toilet" | 04:57 | official | static |
| Drinking water | No | FS-CR | "Potable water is not available at this site." | 04:57 | official | static |
| Picnic tables | Yes, 10 | FS-CR | "Picnic tables are available at this site. 10" | 04:57 | official | static |
| Fire rings | Yes; "Fires only in established fire rings." | FS-CR | quoted | 04:57 | official | static |
| Shade / forest | "Nestled in the woods along Rampart Range Road" (only statement) | FS-CR | quoted | 04:57 | official | static |
| Day use | Yes - purpose-built day-use site | FS-CR | "Picnicking - Single" | 04:57 | official | static |
| Overnight | Prohibited | FS-CR | "Overnight use prohibited." | 04:57 | official | static |
| Fee and payment | "$7 per vehicle per day" (database); "Day use fee of $7.00 payable by check or money order. Self servicing fee tube is available." Cash is not listed. "Golden Age & Golden Access Cardholders: 50% discount off day use fee." | EDW-SITES; FS-CR | quoted | 04:57-04:58 | official | static |
| Reservation | None published; UNKNOWN whether units can fill | - | - | - | - | - |
| Season | "Seasons of Use: May 8" (no end date). "Rampart Range Road is closed by December 1" | FS-CR | quoted | 04:57 | official | static |
| Current open state | Page banner "Site Open"; database flag "OPEN", record last edited 2026-08-06. Not a dated October confirmation | FS-CR; EDW-SITES | "Site Open"; `seasonal_operational_status` OPEN | 04:57-04:58 | official | dynamic |
| Trailer suitability | UNKNOWN | - | - | - | - | - |
| Motorcycles | Developed recreation site: 36 CFR 261.16(o) (entering or leaving only) and (n) ("Operating a bicycle, motorbike, or motorcycle on a trail unless designated for this use"). The spur is a road, so an unplated bike has no stated way in | ECFR; FS-DF road rule | quoted | 04:59 | controlling / derived | static |
| Accessibility | UNKNOWN | - | - | - | - | - |
| Elevation | 8,700 feet | EDW-SITES | `minimum_elevation` | 04:58 | official | static |

### 1.5 Cabin Ridge Trailhead (new: agency page and record found)

| Attribute | Value | Source | Decisive quote / field | Checked (UTC) | Strength | S/D |
|---|---|---|---|---|---|---|
| Official name | Cabin Ridge Trailhead (CABIN RIDGE TH, site_id 33715) | FS-CRTH, EDW-SITES | title | 04:57 | official | static |
| Coordinates | 39.28174051, -105.10401202 | FS-CRTH | quoted | 04:57 | official | static |
| Type / trail | OHV trailhead; "Cabin Ridge Trailhead accesses Cabin Ridge Trail (#675)." | FS-CRTH | quoted | 04:57 | official | static |
| Position | On NFSR 300 (6 m from the line) at about mile 8.3; the picnic spur turn is about 0.2 mile farther south (both derived). Page says "located southeast of the Cabin Ridge Picnic Area"; by the two coordinate pairs it is north-east of it - minor conflict | MVUM-ROADS; FS-CRTH | geometry; quoted | 05:00 | derived / official | static |
| Parking | Capacity field 85 (unit undefined) | EDW-SITES | `total_capacity` 85.0 | 04:58 | official | static |
| Toilet / water | No / No. (Partner prints "vault toilets (Cabin Ridge TH)" on its picnic-area line - that is the picnic area's toilet) | FS-CRTH; RRMMC-PARK | "Restrooms No"; "Potable water is not available at this site." | 04:57 | official | static |
| Fee | None | EDW-SITES | `fee_charged` N | 04:58 | official | static |
| Season | "Year-round" with the road winter closure | FS-CRTH | quoted | 04:57 | official | static |
| Current state | Database flag "OPEN" (edited 2025-04-09) | EDW-SITES | field | 04:58 | official | dynamic, stale |
| Staging, trailer, shade, accessibility | UNKNOWN | - | - | - | - | - |

### 1.6 Topaz Point Picnic Area

| Attribute | Value | Source | Decisive quote / field | Checked (UTC) | Strength | S/D |
|---|---|---|---|---|---|---|
| Official name | Topaz Point Picnic Area / Picnic Site (TOPAZ POINT, site_id 03571) | FS-TP, EDW-SITES | titles | 04:57 | official | static |
| Coordinates | 39.2580704, -105.11731291 | FS-TP | quoted | 04:57 | official | static |
| Managing agency | Forest Service, "US Forest Service" operated | EDW-SITES | `operated_by` | 04:58 | official | static |
| Type | Picnic site, 10 sites | FS-TP | "The Topaz Point Picnic Area has ten (10) picnic sites." | 04:57 | official | static |
| Road access | On NFSR 300 at about mile 11.0 (derived); spur 300.M is 0.07 mi, maintenance level 3, native surface | MVUM-ROADS | attributes; geometry | 05:00 | official / derived | static |
| Toilet / water | Vault toilets / no water | FS-TP | "Vault toilets"; "Potable water is not available at this site." | 04:57 | official | static |
| Tables / fire rings | "picnic sites" (tables not separately itemised); fire rings not stated | FS-TP | quoted | 04:57 | official | static |
| Fee | CONFLICT. Page: "There is a day use fee of $7. Fees are payable by check or money order." Database: `fee_charged` "N" | FS-TP; EDW-SITES | quoted | 04:57-04:58 | official x2 | static |
| Season | "Picnic season begins in May and continues into October." "Seasons of Use: May 15" | FS-TP | quoted | 04:57 | official | static |
| Overnight | Not stated on the page (Order 2022-08 camping rule applies along NFSR 300) | FS-TP; ORD-PARK | absent | 04:57 | official / controlling | static |
| Current state | Page banner "Site Open"; database "OPEN" (edited 2025-04-09) | FS-TP; EDW-SITES | quoted | 04:57 | official | dynamic, stale |
| Shade, parking, trailer, accessibility | UNKNOWN | - | - | - | - | - |
| Elevation | 8,800 feet | EDW-SITES | `minimum_elevation` | 04:58 | official | static |

### 1.7 Sunset Point Trailhead, the northern "main lot", Garber Creek, Rampart Entrance, Rim Road

No Forest Service recreation page was found for Sunset Point, Rampart Entrance, Mile and a Half or Rim Road (slug guesses returned 404; the database records for the first three carry no web-page id). The database records are the only agency evidence.

| Site (database name, site_id) | Agency coordinates | Mile on NFSR 300 (derived) | Capacity field | Fee | Toilet / water (agency) | Partner statement (RRMMC, partner) | Record edited |
|---|---|---|---|---|---|---|---|
| RAMPART ENTRANCE (35067), trailhead | 39.37716, -105.09412 | 0.0 (at the Hwy 67 junction) | 135 | N | not populated | Partner FAQ: in winter "only the first parking lot near Highway 67 is accessible" | 2021-06-01 |
| MILE AND A HALF (35069), trailhead | 39.36002, -105.07883 | 1.65 | 50 | N | not populated | "1.6 RRPARK07 Loading ramp (Main Parking Lot)" - same mile; partner coordinates differ (N39 21.813 W105 4.908) | 2021-06-01 |
| GARBER CREEK (35079), trailhead; page "Garber Creek Trailhead" | 39.3581298, -105.07871472 | 1.84 | 55 | N | "Restrooms No"; no potable water | "1.8 RRPARK09 Trailhead for trail 686 (Garber)". Agency page says "approximately 3 miles" - internal inconsistency | 2023-04-21 |
| SUNSET POINT (33724), trailhead | 39.34808, -105.08571 | 2.80; spur 300.U 0.1 mi, level 3 | 90 | N | not populated (UNKNOWN from agency) | "2.8 RRPARK15 Loading ramp, vault toilet, trailhead for trail 688 (Beaver Trail) (Sunset Point TH)"; partner coordinates about 750 m from the agency point | 2021-06-01 |
| FLAT ROCKS OS (03574), "Flat Rocks Scenic Overlook", observation site | 39.32621268, -105.08524815 | 4.70; spur 300.S 0.08 mi | 50 | N | not populated | "4.6 FLTRCKOL Flat Rocks overlook, kiddy track, trailhead for trail 682" | 2025-04-09 |
| RIM ROAD (35080), trailhead | 39.30385, -105.08785 | 6.39 (at the NFSR 507 junction) | 21 | N | "No" / "No" | - | 2023-04-21 |

- All checked 2026-10-09 04:58 UTC (EDW-SITES) and 05:02 UTC (RRMMC-PARK). Strength: official for the database fields (static, several years old); partner for the RRMMC column; derived for miles.
- The "main lot" is a partner name. By milepost it matches the agency's MILE AND A HALF trailhead (derived match, not stated by either source).
- Flat Rocks Scenic Overlook, agency description: "provides views to the east towards Perry Park and Castle Rock"; "Located on the east side of the Rampart Range Road just south of Flat Rocks Campground." No tables, toilet or water are listed. A free scenic stop, not an established picnic base.
- Staging, loading ramps, toilets, trailers, shade: UNKNOWN from any agency source for all of these.

### 1.8 Devil's Head Picnic Area and Campground (same road, about mile 9.5)

| Attribute | Devil's Head Picnic Area | Devil's Head Campground |
|---|---|---|
| Coordinates | 39.27029244, -105.10483112 | 39.2717739, -105.10509165 |
| Access | Spur NFSR 300.O "DEVILS HEAD TH/CG", 0.6 mi, level 3, native surface; leaves NFSR 300 near mile 9.4-9.5 (derived) | same spur system (300.P, 300.Q) |
| Facilities | "five (5) picnic units"; "Vault toilets"; "Picnic tables are available" | Vault toilets; picnic tables; no water |
| Water | CONFLICT: page "Potable water is not available at this site."; database `water_availability` "Yes" | "Potable water is not available" |
| Fee | CONFLICT: page "$11 day use fee per vehicle."; database `fee_charged` "N" | "$11 fee for day use if not camping overnight." "cash, check or money order. A scan and pay option are available." |
| Rules | "Overnight use prohibited. Fires only in established fire rings. Pack it in; pack it out." "Dogs must be on a leash at all times." | "Only licensed vehicles can operate inside the campground." |
| Season / state | No season stated; road closed by 1 December | "Only the upper loop of the campground is open at this time." "typically open from Memorial Day week to late September. Full service ends after Labor Day weekend." Page updated 1 May 2026 |
| Source, checked, strength | FS-DHP (updated 11 March 2026), EDW-SITES; 04:57-04:58; official; static | FS-DHC, EDW-SITES; 04:57-04:58; official; season is dynamic |

Realistic as a family base only if the family wants the Devil's Head lookout hike (trail described on the Flat Rocks page as "a 1.4-mile trail, which has a 940-foot elevation gain"; tower "usually staffed mid-May through mid-September"). The campground is past its stated season, exactly like Flat Rocks. No OHV access inside it.

### 1.9 Numbered designated dispersed sites (Recreation.gov facility 10132201)

| Attribute | Value | Source | Quote / field | Checked (UTC) | Strength | S/D |
|---|---|---|---|---|---|---|
| Operator | "operated by ExplorUS LLC" | RECGOV-DD | quoted | 04:57 | official | static |
| Inventory | 98 numbered units; loops labelled NFSR 300, NFSR 507 (Rim Road), NFSR 502/503 (Jackson Creek), NFSR 348 (Long Hollow), NFSR 563 (Dakan Road), Watson Park | RECGOV-DD-SITES | site names and `loop` | 04:59 | official | static |
| Type of use | Every unit: `type_of_use` "Overnight". No day-use product exists | RECGOV-DD-AVAIL | field, 98 of 98 | 04:59 | official | static |
| 2026 season and fee | Peak 2026-05-22 to 2026-09-06; "First-come, First-served Season" 2026-09-07 to 2026-10-24; $22 (standard) / $33 (group). October dates show "Not Reservable" (walk-up) | RECGOV-DD-SITES, RECGOV-DD-AVAIL | `rates[]`; `availabilities` | 04:59 | official | static schedule |
| Amenities | "Picnic tables and fire rings are at each site."; "No restrooms are in the dispersed camping areas."; no water (earlier draft). Unit attributes: Max people 8, max vehicles 2, driveway "Gravel", pets yes, check-in 2:00 PM, check-out 12:00 PM | FS-RR (earlier); RECGOV-DD-SITES | quoted; attributes | 04:59 | official | static |
| Day use by a non-camper | UNKNOWN. Not offered, not prohibited in any reviewed source | - | - | - | - | - |
| Sites near the candidates (derived from published unit coordinates) | Sites 51-60 ("Rim Road") have coordinates between 39.2862 and 39.2904, -105.092: within about 50-500 m of the Dutch Fred Trailhead point (Site 60: 39.286235, -105.09207). Site 61: 39.27835, -105.10866, about 280 m from Cabin Ridge Picnic Area. Many units have no published coordinates | RECGOV-DD-SITES | `latitude`/`longitude` | 04:59 | derived | static |

- This explains the partner's phrase "Dutch Fred campground": there is no agency campground of that name; there are numbered dispersed sites beside the trailhead (derived).
- Label conflict: Recreation.gov files those units under loop "NFSR 507"/"Rim Road", while the Forest Service road data puts NFSR 507 "RIM" at mile 6.4, a mile north of Dutch Fred. Not resolved; cosmetic for this trip.

---

## 2. Flat Rocks resolution

### 2.1 What is established

| Question | Answer | Basis |
|---|---|---|
| Official operating season | Forest Service: "open from early May to late September, dependent on the weather"; full service Memorial Day weekend to Labor Day weekend. Recreation.gov rate schedule: 2026-05-01 to 2026-09-19 | FS-FR; RECGOV-FR-SITES (official, static) |
| Is 10-11 October inside the published season? | No. Three weeks after the last published 2026 date | derived from the two sources above |
| Reservations | None; first come, first served | FS-FR |
| Operator | Concessionaire; Recreation.gov contact email is at goexplorus.com. The partner site's "Developed Campgrounds" link still points to rockymountainrec.com, which does not list this campground (earlier draft) - treat the partner link as stale | EDW-SITES; RECGOV-FR; RRMMC |
| Riding access | Flat Rocks Trailhead is a separate, free, Forest Service-operated site at the mouth of the campground road. It does not depend on the campground. The campground road is "Roads open to all Vehicles, Seasonal" in the road data. Whether an unplated bike may be ridden inside the campground is in conflict (table 1.2) | EDW-SITES; MVUM-ROADS; FS-FR |
| Does a campground closure block family day use? | Not established. The only rule found is about camping: Order 2003-03 prohibits "Camping in an area, developed site or campground that is posted as closed to camping." Nothing reviewed says a closed campground may or may not be entered on foot or used for a picnic. If the gate is locked, vehicles cannot enter regardless | ORD-CLOSEDCAMP (controlling, static) |

### 2.2 What is NOT established (10-11 October)

- Whether the campground gate is physically open.
- Whether day use is accepted after the fee season and, if so, whether the $11 fee applies and how it is paid with no host.
- Whether the water system is on. The page itself warns water "may not be available during the fall". Assume none.
- Whether the vault toilets are unlocked.
- Whether the family may park at the Flat Rocks Trailhead lot and walk in.

### 2.3 Signals that look like status but are not

- Database `seasonal_operational_status` "OPEN": last edited 2026-08-06, during the season; the same record still carries "open_season = May 28, 2021" and a description ending "between April 30, 2021 and September 27, 2021". Not evidence for October 2026.
- Recreation.gov October availability `{}` (empty): consistent with "no fee season", not proof of a locked gate.
- A third-party directory shown in search results labelled the campground "Closed for winter" - lead only, not opened, not used.

### 2.4 The "August 21, 2026 through November 14, 2026" lead - RESOLVED

- **Confirmed to exist; refuted as a Flat Rocks order.** Forest Service news release dated 21 August 2026 (opened, FS-NEWS-STAGE1): "The Pike-San Isabel National Forests will move from Stage 2 to Stage 1 Fire Restrictions beginning Aug. 21 at 12:01 a.m. through Nov. 14, unless rescinded. This includes the Pikes Peak, South Park, South Platte, Leadville, Salida and San Carlos ranger districts".
- **What it covers:** fires, smoking, explosives and welding - forest-wide. It prohibits "Building, maintaining, attending, or using a fire (including fires fueled by charcoal or briquettes), except if it is in: A permanent metal or concrete fire pit or grate that the U.S. Forest Service has installed and maintained at its developed recreation sites (campgrounds and picnic areas)"; or "A device solely fueled by liquid or gas that can be turned on and off used in an area barren or cleared of all flammable materials within three feet of the device". It closes no site and no road.
- **Order number:** a search-result summary gave "02-12-00-26-37". The order document itself was not opened (its alert page now returns HTTP 404), so the number is a lead.
- **Is it still in force on 10-11 October? Evidence points to no; not certain.**
  - Forest Service fire-restriction map layer (linked from the forest's fire-restrictions page): South Platte Ranger District `FireRestct` = code "1", which the layer's own domain defines as "No Restrictions" (2 = "Stage 1", 3 = "Stage 2"). All eight districts read "No Restrictions". Layer data last edited 2026-10-01 13:24 UTC. Checked 05:04 UTC. Official, dynamic.
  - Forest Service alerts list (where the forest says "All fire restrictions and closures are posted"): no fire-restriction alert present at 05:00 UTC; the Stage 1 alert URL returns 404.
  - No rescission news release was found in the newsroom list (latest items: 7 October prescribed fire, 17 September prescribed fire, 31 August Aspen Acres, 21 August Stage 1).
  - Douglas County: "STAGE 1 FIRE RESTRICTIONS HAVE BEEN LIFTED FOR UNINCORPORATED DOUGLAS COUNTY" (page "updated on 9/17/2026"), re-read 05:03 UTC.
- **Why it appeared on the Recreation.gov page:** not determined. The page's alert banner is filled from `/api/communication/external/alert` (confirmed in the page's own script); that endpoint returned `{"alerts":[]}` for this facility at 04:58 and 05:03 UTC. Limit: it also returned empty for three unrelated control facilities, so an anonymous request may never return alerts; a rendered browser view was NOT RETRIEVED (browser tool not connected).
- **Effect on the plan either way:** a picnic at a Forest Service fire ring in a developed picnic area, or on a gas stove with a shut-off valve, would be permitted even under Stage 1. A charcoal grill brought from home would not be under Stage 1.

### 2.5 Derived conclusion for Flat Rocks

Do not plan the family day around Flat Rocks Campground. Its published season is over, and nothing online establishes gate, day-use, water or toilet status. Flat Rocks Trailhead remains a legitimate free staging candidate with no agency-listed toilet or water. If the owner prefers Flat Rocks, one phone call settles it (section 7).

---

## 3. Dutch Fred + Cabin Ridge pairing assessment

### 3.1 Dutch Fred - answers to the specific questions

- **Staging legality:** it is an agency trailhead record with "OHV Trail Riding" as its listed activity, and the published MVUM inset shows a motorized-trailhead symbol at "DUTCH FRED" (earlier draft, image-read). Parking must be in designated, signed parking (Order 2022-08). Official / controlling, static.
- **Parking:** capacity field 55, unit undefined. Trailer parking: UNKNOWN.
- **Toilet conflict - not resolved; follow the agency.** Agency "Restrooms No" (page updated 28 May 2026; database 2025-04-09) versus partner "Vault toilets". The two agency views share one data store, so they are one statement, not two. Plan on no toilet at Dutch Fred. Nearest agency-listed toilet: Cabin Ridge Picnic Area vault toilet.
- **Hours:** sunrise to sunset (area rule). **Fee:** none.
- **The "high clearance" designation - exact wording and scope.** The source is the Forest Service MVUM road record for NFSR 506 "DUTCH FRED": field `operationalmaintlevel` = "2 - HIGH CLEARANCE VEHICLES", `surfacetype` = "NAT - NATIVE MATERIAL". By contrast NFSR 300 and the Flat Rocks, Cabin Ridge, Topaz Point, Sunset Point and Devil's Head spurs are all "3 - SUITABLE FOR PASSENGER CARS". Does it apply to the trailhead access itself? **Yes (derived):** 506 starts on NFSR 300 and is the only mapped road toward the trailhead point, which lies about 300 m beyond its mapped end. It is a maintenance classification, not a vehicle prohibition: the same record lists passenger vehicles as "open 05/16-11/30". The dataset metadata did not yield a readable plain-language definition of level 2; the general Forest Service definition ("passenger car traffic is not a consideration") appeared only in a search summary and is a lead.
- **Current condition of the spur:** UNKNOWN. Standing district notice about downed and weakened trees still listed (earlier draft).
- **Practical reading (derived):** a pickup fits the class. A low car, or a low trailer on a rutted native-surface spur, is not established either way.

### 3.2 Cabin Ridge - answers

- **Open status:** "Site Open" banner and database "OPEN" (edited 2026-08-06). No end-of-season date is published; the only stated closure is the road by 1 December. Official, dynamic, not a dated confirmation.
- **Tables:** 10 units with tables. **Fire:** fire rings; "Fires only in established fire rings." **Toilet:** vault. **Water:** none - bring all water.
- **Fee:** $7 per vehicle per day, self-service fee tube, "payable by check or money order". Bring a cheque. Whether cash in the envelope is accepted is UNKNOWN.
- **Overnight:** "Overnight use prohibited." Also 36 CFR 261.16(e): "Occupying between 10 p.m. and 6 a.m. a place designated for day use only."
- **Relationship to Dutch Fred:** same road, NFSR 300. Dutch Fred spur junction about mile 7.5; Cabin Ridge spur junction about mile 8.5 - **1.0 mile apart on NFSR 300**, by my measurement on Forest Service road geometry (derived). Partner mileages 7.3 and 8.4 give 1.1 miles. The earlier draft's router run gave 1.0 mile between spurs and 1.8 miles door to door. Straight-line distance between the two agency coordinate pairs: about 0.85 mile (derived).

### 3.3 Verdict (DERIVED - no source states this pairing)

**Dutch Fred -> Cabin Ridge is a practical same-road rider/family pairing, with conditions.**

Reasoning:
1. Both are Forest Service sites with their own records, both flagged open, neither tied to the concessionaire campground season that has ended.
2. They are about 1 mile apart on one road, so the truck can drop the rider and bike at Dutch Fred and reach the picnic area in a few minutes.
3. Cabin Ridge is the only purpose-built, fee-paid day-use site in this stretch with tables, fire rings and a toilet; the family's use there is the use the site is published for.

Conditions and limits:
- The unplated bike may not be ridden on NFSR 300, the 506 spur as a "road", or the picnic spur. The rider and family reunite by truck, or on foot from Cabin Ridge Trailhead.
- Dutch Fred: plan on no toilet and no water; spur is high-clearance class, condition unknown.
- Cabin Ridge: no water; cheque or money order; 10 units, no reservation, fill risk unknown.
- Trail connectivity and trail legality were not assessed here (another worker).

**Variant worth weighing (derived): stage at Cabin Ridge Trailhead instead of Dutch Fred.** It is on NFSR 300 itself (no high-clearance spur), about 0.2 mile from the picnic turn, capacity field 85, and the agency says it accesses Cabin Ridge Trail #675. By geometry, trail 0627 (named BEGINNER in the agency trail layer) passes within a few metres of this trailhead and about 30 m from the picnic site - a proximity candidate only, not a statement that it may be ridden or that it connects. Trade-off: partner sources put the beginner features (Kiddy Corral, Lightfoot's Loop) at Dutch Fred, not here.

---

## 4. Backups

| Option | Why someone would rationally choose it | What it costs | Evidence gaps |
|---|---|---|---|
| **Topaz Point Picnic Area** (mile ~11.0) | The only site whose page speaks to October: "Picnic season begins in May and continues into October." Sits directly on NFSR 300 (70 m spur). Farther from the busy northern staging lots, so plausibly quieter (not stated by any source) | About 2.5 miles past Cabin Ridge; rider staging nearby is thin on agency evidence; fee conflict ($7 on the page, "N" in the database) | Tables and fire rings not itemised; no overnight rule on the page; record last edited 2025-04-09 |
| **Devil's Head Picnic Area** (mile ~9.5) | Gives the family something to do: the Devil's Head lookout trail starts there | $11 per vehicle; only 5 units; 0.6 mile spur; a popular hiking trailhead | Water conflict (page no, database yes); fee conflict; tower staffing ended mid-September per the Flat Rocks page |
| **Flat Rocks Trailhead + Flat Rocks Scenic Overlook** (mile ~4.6-4.7) | Shortest drive on the forest road; overlook is free with views east | No tables, toilet or water at either per agency; campground beside them is out of season | Whether lingering at an overlook or trailhead is provided for: unknown |
| **Flat Rocks Campground day use** | The only site with potable water and the only one where the page ties the site itself to trail access | $11; cash accepted | Open / day use / water / toilets on 10-11 October all unknown - needs the phone call |

Evidence supports two solid family options (Cabin Ridge, Topaz Point) and one conditional (Devil's Head). The numbered dispersed sites are not offered as a day-use backup: only overnight use is published.

---

## 5. Hammock

`Hammock use: Not established from reviewed authoritative sources.`

Reviewed and found silent on hammocks, straps, ropes or attaching anything to trees: 36 CFR 261.2, 261.9, 261.10, 261.16, 261.58 (official eCFR, title 36 current as of 2026-10-07); Order 02-12-00-24-04 (re-read 05:03 UTC); Order 2003-03; the Stage 1 release; Forest Service pages for Flat Rocks Campground, Flat Rocks Trailhead, Dutch Fred, Cabin Ridge (both), Topaz Point, Devil's Head (both), Garber Creek, Indian Creek Campground; Recreation.gov records and notices for facilities 10165295 and 10132201; RRMMC home, FAQ and parking pages (text-searched for "hammock": no hit). The concessionaire's corporate site (goexplorus.com) has no campground-rules or facility pages at all (sitemap read 05:00 UTC). No Rocky Mountain Region or Pike-San Isabel hammock FAQ was found by two searches.

Related rules that were found (controlling, static, ECFR, checked 04:59 UTC):

| Provision | Text |
|---|---|
| 36 CFR 261.9(a) | Prohibited: "Damaging any natural feature or other property of the United States." |
| 36 CFR 261.2 (definition) | "Damaging means to injure, mutilate, deface, destroy, cut, chop, girdle, dig, excavate, kill or in any way harm or disturb." |
| 36 CFR 261.16(a) | Developed recreation sites: "Occupying any portion of the site for other than recreation purposes." |
| 36 CFR 261.16(g) | "Placing, maintaining, or using camping equipment except in a place specifically designated or provided for such equipment." |
| 36 CFR 261.2 (definition) | "Camping equipment means the personal property used in or suitable for camping, and includes any vehicle used for transportation and all equipment in possession of a person camping." |
| 36 CFR 261.10(f) | "Placing a vehicle or other object in such a manner that it is an impediment or hazard to the safety or convenience of any person." |
| 36 CFR 261.10(a) | "Constructing, placing, or maintaining any kind of road, trail, structure, fence, enclosure, communications equipment, sign, or other improvement ... without a special use authorization" |

- None of these names a hammock. Whether a strap round a tree "girdles" or "harms" it, or whether a day-use hammock is "camping equipment" outside a designated place, is a judgement for the agency, not for this file. I do not characterise it either way.
- Other national forests' hammock guidance surfaced only as search summaries (a Superior National Forest wilderness page; a National Park Service campground notice). They are other units, were not opened, and are leads that do not apply here.
- Safety, not a rule: the district's standing notice says trees "may be weakened and could fall" (earlier draft).
- **Remaining path:** a call to the South Platte Ranger District is the only way found to get an answer in advance. On the day, posted site signs or a host could also answer it. A free-standing hammock frame avoids the tree question but is equally unaddressed by any source.

---

## 6. Conflicts preserved

| # | Topic | Source A | Source B | Handling |
|---|---|---|---|---|
| 1 | OHVs inside Flat Rocks Campground | Page: "ATVs and off-road motorcycles are allowed to enter and depart the campground for trail access." | Database record: "Only licensed vehicles can operate inside campground." | Both official. Unresolved. 36 CFR 261.16(o) limits any motor vehicle in a developed site to entering or leaving |
| 2 | Dutch Fred toilet | Agency: "Restrooms No" | Partner: "Vault toilets"; Recreation.gov area text: "vault toilets at most trailheads and port-a-potties in the area" | Follow agency; plan on none |
| 3 | Flat Rocks open state | Database flag "OPEN" (edited 2026-08-06) | Page season "early May to late September"; Recreation.gov season ended 2026-09-19 | Flag is stale; status unknown |
| 4 | Stage 1 fire restrictions | News release: through 14 November "unless rescinded" | Fire-restriction map: "No Restrictions" (edited 2026-10-01); alert page removed | Later, dynamic official source suggests lifted; no rescission notice found |
| 5 | Topaz Point fee | Page: "$7" | Database: `fee_charged` N | Bring a cheque for $7 |
| 6 | Devil's Head Picnic Area water and fee | Page: no potable water; "$11 day use fee per vehicle" | Database: water "Yes"; fee "N" | Assume no water; assume fee |
| 7 | Garber Creek distance | Page: "approximately 3 miles" | Geometry: mile 1.84; partner: 1.8 | Geometry and partner agree |
| 8 | Sunset Point and "Main Parking Lot" coordinates | Agency points at miles 2.80 and 1.65 | Partner coordinates 750 m and about 450 m away, same stated miles | Use agency coordinates |
| 9 | Cabin Ridge Trailhead direction | Page: "southeast of the Cabin Ridge Picnic Area" | Coordinates: north-east of it | Use coordinates |
| 10 | Dispersed-site loop label near Dutch Fred | Recreation.gov: "Rim Road / NFSR 507" | Road data: NFSR 507 leaves NFSR 300 at mile 6.4 | Cosmetic; unresolved |
| 11 | Flat Rocks operator | Recreation.gov contact domain: ExplorUS | Partner link: Rocky Mountain Recreation Company | Follow Recreation.gov; partner link stale |
| 12 | Picnic payment | Cabin Ridge, Topaz: "check or money order" | Campgrounds: "cash, check or money order" | Take a cheque |

Earlier-draft conflicts (trail numbers 673/674 and 679/681, MVUM date windows, road jurisdiction) are unchanged and belong to the trail-legality worker.

---

## 7. Requires a phone call

Office: **South Platte Ranger District**, 30403 Kings Valley Drive, Suite 2-115, Conifer, CO 80433. Published phone **303-275-5610**. Published hours "Monday-Friday, 8:00 a.m. - 4:30 p.m. (Closed on federal holidays)" (Mountain time; source FS-FR office block, checked 04:57 UTC). **Friday 9 October is the only business day left before the trip**; Monday 12 October is the Columbus Day federal holiday. Not called.

Recreation.gov also publishes, for both the Flat Rocks Campground record and the dispersed-camping record: "For facility specific information, please call (303) 647-2366." Hours for that line are not published. Not called.

Exact questions, in priority order:

1. "Is the Flat Rocks Campground gate open this weekend, 10-11 October? If the campground is closed for the season, may a family still use a site or the grounds for day use, is the $11 day-use fee still collected, and are the water and vault toilets on?"
2. "Is Cabin Ridge Picnic Area open this weekend, and is the $7 fee tube cheque-or-money-order only, or is cash accepted?"
3. "Is there a toilet of any kind at the Dutch Fred Trailhead right now? Is the Dutch Fred spur road (NFSR 506) passable for a pickup towing a small trailer?"
4. "May visitors hang a hammock from trees at Cabin Ridge or Topaz Point picnic areas, or at Flat Rocks Campground? Are tree-protecting straps required, or is a free-standing frame expected?"
5. "Are any fire restrictions in effect on the South Platte district this weekend? Was the Stage 1 order of 21 August rescinded?"
6. "May a family spend the day at a trailhead lot (chairs, picnic) while a rider is out, and may a numbered dispersed site be used for day use only? At what fee?"
7. "Inside Flat Rocks Campground, may an unplated, OHV-registered motorcycle be ridden from a site to the trail, or only street-licensed vehicles?"

---

## 8. Remaining unknowns that affect the Saturday decision

- Flat Rocks Campground: gate, day use, fee, water, toilets (question 1).
- Dutch Fred: toilet; spur condition; trailer turning and parking room.
- Cabin Ridge and Topaz Point: dated confirmation of open status; whether cash is accepted; how full they get; shade at individual units.
- Hammock permission anywhere.
- Fire restriction state on the day (map says none as of 1 October).
- Trailer suitability of NFSR 300 and every spur (no agency statement).
- Day use of numbered dispersed sites; lingering at trailhead lots.
- Accessibility features at every site (nothing published).
- Rendered Recreation.gov page alerts panel (not retrieved in a browser).

---

## Sources

All retrieved 2026-10-09 UTC between 04:57 and 05:05. Forest Service pages and partner pages were read as raw HTML converted to text locally; APIs were read as JSON.

| Key | URL | Publisher | Retrieved |
|---|---|---|---|
| FS-FR | https://www.fs.usda.gov/r02/psicc/recreation/flat-rocks-campground (last updated January 23, 2026) | USDA Forest Service | 04:57 |
| FS-FRTH | https://www.fs.usda.gov/r02/psicc/recreation/flat-rocks-trailhead (February 18, 2025) | USDA Forest Service | 04:57 |
| FS-DF | https://www.fs.usda.gov/r02/psicc/recreation/dutch-fred-trailhead (May 28, 2026) | USDA Forest Service | 04:57 |
| FS-CR | https://www.fs.usda.gov/r02/psicc/recreation/cabin-ridge-picnic-area (February 18, 2025) | USDA Forest Service | 04:57 |
| FS-CRTH | https://www.fs.usda.gov/r02/psicc/recreation/cabin-ridge-trailhead (February 18, 2025) | USDA Forest Service | 04:57 |
| FS-TP | https://www.fs.usda.gov/r02/psicc/recreation/topaz-point-picnic-area (February 18, 2025) | USDA Forest Service | 04:57 |
| FS-DHP | https://www.fs.usda.gov/r02/psicc/recreation/devils-head-picnic-area (March 11, 2026) | USDA Forest Service | 04:57 |
| FS-DHC | https://www.fs.usda.gov/r02/psicc/recreation/devils-head-campground (May 1, 2026) | USDA Forest Service | 04:57 |
| FS-GC | https://www.fs.usda.gov/r02/psicc/recreation/garber-creek-trailhead (February 18, 2025) | USDA Forest Service | 04:57 |
| FS-IC | https://www.fs.usda.gov/r02/psicc/recreation/indian-creek-campground (January 23, 2026) - read for comparison only | USDA Forest Service | 04:57 |
| FS-RR | https://www.fs.usda.gov/r02/psicc/recreation/rampart-range-recreation-area - re-fetched; quotes as in the earlier draft | USDA Forest Service | 04:57 |
| EDW-SITES | https://apps.fs.usda.gov/arcx/rest/services/EDW/EDW_RecInfraRecreationSites_02/MapServer/0 (24 records in box -105.16,39.22 to -105.04,39.40) | USDA Forest Service Enterprise Data Warehouse | 04:58 |
| MVUM-ROADS | https://apps.fs.usda.gov/arcx/rest/services/EDW/EDW_MVUM_02/MapServer/1 (attributes and geometry) | USDA Forest Service | 05:00 |
| FS trail layers | https://apps.fs.usda.gov/arcx/rest/services/EDW/EDW_TrailNFSPublish_01/MapServer/0 and EDW_MVUM_02/MapServer/2 - proximity only | USDA Forest Service | 05:01 |
| RECGOV-FR | https://www.recreation.gov/api/camps/campgrounds/10165295 (record updated 2025-11-25); page https://www.recreation.gov/camping/campgrounds/10165295 (script shell only) | Recreation.gov, org FS | 04:57, 05:02 |
| RECGOV-FR-SITES | https://www.recreation.gov/api/search/campsites?fq=asset_id%3A10165295 | Recreation.gov | 04:58 |
| RECGOV-DD | https://www.recreation.gov/api/camps/campgrounds/10132201 (record updated 2025-12-29) | Recreation.gov, org FS | 04:57 |
| RECGOV-DD-SITES / -AVAIL | https://www.recreation.gov/api/search/campsites?fq=asset_id%3A10132201 ; https://www.recreation.gov/api/camps/availability/campground/10132201/month?start_date=2026-10-01T00%3A00%3A00.000Z | Recreation.gov | 04:59 |
| RECGOV alerts | https://www.recreation.gov/api/communication/external/alert?location_id=10165295&location_type=Campground (returned `{"alerts":[]}`; also empty for 10132201 and three controls) | Recreation.gov | 04:58, 05:03 |
| ECFR | https://www.ecfr.gov/api/versioner/v1/full/2026-10-07/title-36.xml?part=261&section=261.2 (and 261.9, 261.10, 261.16, 261.58) | Office of the Federal Register / GPO (official eCFR) | 04:59 |
| FS-ALERTS | https://www.fs.usda.gov/r02/psicc/alerts | USDA Forest Service | 05:00 |
| ORD-CLOSEDCAMP | https://www.fs.usda.gov/r02/psicc/alerts/prohibition-camping-areas-posted-closed-camping (Order 2003-03) | USDA Forest Service | 05:00 |
| ORD-OCC | https://www.fs.usda.gov/r02/psicc/alerts/pike-national-forest-occupancy-and-use-restrictions (Order 02-12-00-24-04) | USDA Forest Service | 05:03 |
| FS-NEWS-STAGE1 | https://www.fs.usda.gov/r02/psicc/newsroom/releases/pike-san-isabel-national-forests-move-stage-1-fire-restrictions (August 21, 2026) | USDA Forest Service | 05:03 |
| FS newsroom list | https://www.fs.usda.gov/r02/psicc/newsroom/releases | USDA Forest Service | 05:03 |
| FS-FIRE | https://www.fs.usda.gov/r02/psicc/fire/fire-restrictions (April 9, 2026) | USDA Forest Service | 05:03 |
| FS-FIREMAP | https://services1.arcgis.com/gGHDlz6USftL5Pau/arcgis/rest/services/PSICCRangerDistrictsFireRestrictions_2026/FeatureServer/3 (layer "PSICC Ranger Districts Fire Restrictions", behind the web map "USFS Region 02-PSICC Fire Restrictions Web Map" in the experience linked from FS-FIRE; data last edited 2026-10-01T13:24Z) | Forest Service map hosted on ArcGIS Online | 05:04 |
| Stage 1 alert page | https://www.fs.usda.gov/r02/psicc/alerts/pike-san-isabel-national-forests-stage-1-fire-restrictions - HTTP 404, NOT RETRIEVED | USDA Forest Service | 05:03 |
| DCSO | https://www.dcsheriff.net/fire-restrictions/ ("updated on 9/17/2026") | Douglas County Sheriff's Office | 05:03 |
| RRMMC-HOME / -PARK / -FAQ | https://www.rampartrange.org/ ; https://rampartrange.org/parking-areas/ ; https://rampartrange.org/frequently-asked-questions/ (banner "Trail Status: OPEN / Rampart Range Road Status: OPEN", undated) | RRMMC (partner) | 05:02 |
| Concessionaire | https://goexplorus.com/ and its sitemaps - no facility or rules pages exist; campground page NOT AVAILABLE | ExplorUS | 05:00 |
| Road metadata | https://data.fs.usda.gov/geodata/edw/edw_resources/meta/S_USA.Road_MVUM.xml - fetched; no readable maintenance-level definition extracted | USDA Forest Service | 05:04 |

NOT RETRIEVED / failed: Forest Service pages for Sunset Point, Rampart Entrance, Mile and a Half, Rim Road, Flat Rocks overlook, Devil's Head trailhead (slug guesses, 404); rendered Recreation.gov page (browser extension not connected); Recreation.gov `/rules` endpoint (401, requires sign-in - not attempted further); the Stage 1 order document; Order 02-12-00-24-04 exhibit maps; any plain-language Forest Service definition of maintenance level 2.

Web searches (8), used to find URLs and as leads only: the "August 21, 2026" / "November 14, 2026" order with Flat Rocks; ExplorUS Flat Rocks season and day use; Forest Service hammock rules (site-restricted); Pike-San Isabel hammock rules; the order dates with "fire restrictions rescinded"; maintenance level 2 definition; hammocks in developed campgrounds (restricted to fs.usda.gov, usda.gov, recreation.gov). Search summaries are not cited as evidence anywhere above except where explicitly labelled "lead".

Method notes:
- Mileposts, site-to-road offsets and site-to-trail proximities are my own calculations on Forest Service line geometry (WGS84, great-circle and point-to-segment distances). They need a human check against the printed MVUM before reuse.
- `infra_last_update` epoch values were converted to dates by me.
- Recreation.gov's website JSON endpoints are not a documented public API; their date fields are quoted as published and their end dates may be exclusive.
