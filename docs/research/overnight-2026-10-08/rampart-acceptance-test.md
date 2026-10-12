DRAFT - UNREVIEWED ACCEPTANCE TEST RUN 2026-10-08 (main bb85785)

# Rampart Range acceptance test: dirt bike plus family day-use, 10-11 October 2026

Tester: dedicated product acceptance tester (did not implement the product).
Scenario basis: `docs/product/acceptance-scenario-douglas-dirt-bike.md`, with the
owner's real trip substituted for the generic task.

Real task tested: "Starting from my home near Spruce Mountain / Larkspur,
Colorado, where is the closest practical place to access Rampart Range
Motorized Recreation Area for dirt biking while my family has a legal and
comfortable place nearby to spend the day with a picnic and hammock?" Vehicle:
pickup with a small trailer carrying a dirt bike that is assumed not
street-legal. Family: day use only, no overnight.

**Headline result: NO.** A viable outing was not reached inside Ohvernight. The
product names trails, trailheads and campgrounds inside Douglas County and is
honest about most of what it does not know, but it has no origin, no route, no
day-use places a user can find, shows the picnic areas as a bare name, and
tells the user that most of the Rampart trails are "Outside published use
dates" on the trip dates.

## Method and limits

- **Method: real running app.** The `main` checkout
  (`local scratch`, `bb85785`,
  working tree clean) was served with `python3 -m http.server 8765` and driven
  in local headless Chrome 154 over CDP at 390x844, device scale 2, mobile and
  touch emulation on. Basemap tiles loaded. Helper scripts lived in
  `/tmp/ohv-accept`, outside the repository. The server and Chrome were stopped
  afterwards and nothing in the repository was changed.
- Every quote under "observed in the app" is `innerText` read from the live
  DOM. Where a statement comes from reading code or data it is marked
  **(code/data read)**.
- Interactions were DOM clicks on the app's own buttons, result rows and map
  pins. Two selections (a road and the land polygons) were made by calling the
  app's own `showDetail` on the loaded feature, because canvas lines cannot be
  targeted by name; the text rendered is the app's real output for that
  feature. This is marked **(programmatic selection)**.
- **Not done:** no real phone, no real fingers, no GitHub Pages copy (same
  code, not separately opened), no external links followed, no outside
  research. Time-on-task could not be measured as a human would experience it;
  step and tap counts are given instead.
- **Deviations from the canonical scenario:** the dates are 10-11 October, not
  a summer weekend; the need is a family day-use place, not an overnight stay;
  the trail system was fixed in advance (Rampart Range). The scenario's
  "overnight option" steps were run as "family day-use option", with overnight
  noted where the product offers it.
- Tester familiarity recorded as: first-time visitor, no local knowledge used.

## Step-by-step run (the ten scenario steps with outcomes)

| # | Step | Outcome | What happened |
|---|---|---|---|
| 1 | Identify a suitable motorized trail or trail system | **Done partly** | Finder lists 76 "source segments" for Dirt biking. There is no "Rampart Range Motorized Recreation Area" entity: searching trails for "Rampart" returns "No matches in this inventory. Try a name, trail number or another activity." The user must already know trail names such as FLATROCK or DUTCH FRED, or read the map. |
| 2 | Understand whether motorcycles are actually allowed | **Done partly, and confusing** | Raw source strings are shown, for example FLATROCK #0674 "Motorcycling / Accepted use: 12/01-03/14". For the trip dates the app derives "Outside published use dates" for 40 of 76 segments, including most segments beside the Rampart trailheads. The same panel says "These are source records, not a check for your trip dates." Nothing is reviewed. |
| 3 | Identify the relevant trailhead or staging point | **Done partly** | 17 trailhead records, including FLAT ROCKS TH, DUTCH FRED, GARBER CREEK, RIM ROAD, RAMPART ENTRANCE. None is linked to a trail; none is identified as a staging or unloading area; trailer parking is explicitly unverified. |
| 4 | Approach road and access for a truck and trailer | **Not possible in Ohvernight** (partly correctly unknown) | Roads show "Road geometry only. Vehicle and season designations are not evaluated." Agency directions text exists for some trailheads, starting from Sedalia or Denver, never from Larkspur. The user goes to Google Maps (the app links to it) and to the motor-vehicle use map. |
| 5 | Identify a reasonable family day-use option | **Not possible in Ohvernight** | The finder has no picnic or day-use category. Picnic pins exist on the map but open to a name and a fetch date only. Campgrounds are the only "stay" places described. |
| 6 | Identify a backup | **Done partly** | Other trailheads and campgrounds are listed, so alternatives can be named, but none can be compared or confirmed. |
| 7 | Closures and restrictions for the dates | **Ohvernight correctly said unknown** | "No closure or fire-restriction status is loaded." Three official links are given. The user must check the Forest Service and the county. |
| 8 | Understand where each fact came from | **Done partly** | Every record names an agency and a fetch date and links out, but the "View source" link is an ArcGIS REST endpoint for the whole layer, not the record. No fact carries a review date. |
| 9 | Understand what remains unknown | **Done in Ohvernight** | The strongest part of the product. Unknowns are stated on every panel and in Sources & coverage. Two gaps: mismatched source text is not flagged, and silent omissions (fees, day use) are not listed as unknown. |
| 10 | Leave with a usable outing without extensive outside research | **Not possible in Ohvernight** | No recommended outing is produced. At least six outside sources are needed. |

## What the product answered (with quotes)

All quotes observed in the app unless marked.

**Where the area is and how to approach it (agency text, not a route).**
FLAT ROCKS TH detail, "Agency directions": "To reach this area, take U.S.
Highway 85 (Santa Fe) south to Sedalia. Turn west on Highway 67 for 10 miles to
the junction with Rampart Range Road. Flat Rock Trailhead is located
approximately 6 miles from south of Rampart Range Road." DUTCH FRED trailhead:
"...Dutch Fred Trailhead is located approximately 8 miles from south of Rampart
Range Road." FLAT ROCKS CG: "...Turn south onto Rampart Range Road for 5 miles.
Flat Rocks Campground will be on the west side of the road." Record: USFS
recreation-site inventory. The directions start from Sedalia; a Larkspur user
gets no leg from home.

**A handoff to a navigation app.** Each pinned site has "Directions to facility
↗", a Google Maps link to the pin's coordinates (for FLAT ROCKS TH,
`destination=39.327288,-105.086932`), followed by "Check approach roads and
trailer parking before travel. Directions are for this facility, not a verified
riding route."

**The riding rules, as published restriction text on some trailheads.** FLAT
ROCKS TH, "Published restrictions": "The following restrictions apply to the
Rampart Range Motorized Recreation Area: A Colorado OHV (Off Highway Vehicle)
registration or current license plate with OHV permit is required to ride on
the trails. ... A current license plate and valid driver's license are required
to ride on the roads. Only vehicles 50" or less in width can be on trails. Ride
on designated trails only. All vehicles must have a U.S. Forest Service
approved SPARK ARRESTOR." The same block appears on DUTCH FRED, GARBER CREEK,
RIM ROAD, 677A NODDLE and 677B LOG JUMPER. This one block answers four of the
user's legal questions:

- OHV registration: yes, required on trails.
- Spark arrestor: yes, required.
- Over-50-inch vehicles: not allowed on trails.
- Unlicensed dirt bike on Rampart Range Road: the text says a plate and licence
  are "required to ride on the roads". The product does not connect this
  sentence to the road named RAMPART RANGE; the user has to make that link.

It is shown as "Published restrictions" under "Published source · current
access unconfirmed", with no review.

**Which trails, by name and number, with raw use strings.** Examples for the
trip dates (10-11 October), Dirt biking selected:

| Trail (as shown) | Motorcycling string shown | ATV string | 4WD string | App's date result |
|---|---|---|---|---|
| FLATROCK · #0674 | Accepted use: 12/01-03/14 | Managed use: 12/01-03/14 | Restricted: 01/01-12/31 | Outside published use dates |
| CABIN RIDGE · #0675 | Accepted use: 12/01-03/14 | Managed use: 12/01-03/14 | Restricted: 01/01-12/31 | Outside published use dates |
| NODDLE · #0677, BEGINNER · #0627, OVERLOOK · #0682, BARR · #0673, SCOTTYS · #0681, GARBER · #0686, LONG HOLLOW · #0650, TOMAHAWK · #0685 | Accepted use: 12/01-03/14 | Managed use: 12/01-03/14 | Restricted: 01/01-12/31 | Outside published use dates |
| DUTCH FRED · #0679 | Accepted use: 06/01-11/30 | Managed use: 06/01-11/30 | Restricted: 01/01-12/31 | Within published use dates — closures unchecked |
| POWERLINE · #0690, LOG JUMPER · #0677.A, HANKHOS · #0631, SOHNDEE · #0634, WYEGYE · #0633 | Accepted use: 01/01-12/31 | Managed use: 01/01-12/31 | Restricted: 01/01-12/31 | Within published use dates — closures unchecked |
| TUNNEL · #0770.A, DEVILS ADVOCATE · #0770.C, DEVILS REVENGE · #0770.D (single-track class) | Managed use: 01/01-12/31 | Restricted: 01/01-12/31 | Restricted: 01/01-12/31 | Within published use dates — closures unchecked |
| DEVILS HEAD · #611, COLORADO · #1776, INDIAN CREEK · #800 | Restricted: 01/01-12/31 | Restricted: 01/01-12/31 | Restricted: 01/01-12/31 | not listed for Dirt biking |

Finder totals for the dates: Dirt biking 76 segments (36 within, 40 outside);
ATV 64 segments (26 within, 38 outside); 4WD 13 segments (all within). So the
product does separate motorcycle-only, ATV and full-size trails by source
string. Each trail also shows "Trail 0674", "NATIVE MATERIAL" and "Published
uses: 54321" (an unexplained code).

**Facilities, where the record is a trailhead or campground.** FLAT ROCKS TH:
"Water / No", "Restrooms / No". FLAT ROCKS CG: "Water / Yes", "Restrooms /
Vault toilets", "Listed activities: CAMPING, TENT | CAMPING, TRAILER | CAMPING,
VEHICLE | HUNTING | NATURE STUDY | PHOTOGRAPHY | PICNICKING | SPECIAL LANDCRAFT
(OHVS)", "Published season (may be historical): May 28, 2021", and "Only
licensed vehicles can operate inside campground."

**The designated dispersed camping listing** (from `extras.js`, found under
Find = Camping, no map pin): "Rampart Range designated dispersed camping",
"Numbered designated sites only; fee required. The official listing describes a
December 1–April 1 camping closure, with weather-dependent reopening. Check the
listing for current rules and availability." and "Area listing only: individual
campsites and access points have not been mapped." Link: recreation.gov
campground 10132201. This is the only place the product states a fee or a
reservation-style listing near Rampart, and it is about overnight camping.

**Where to look for current status.** Sources & coverage ends with three
links: "Forest Service alerts", "County fire restrictions", "Official maps &
motor-vehicle maps".

### The named places, exactly as the product shows them

| Place | In data | What a phone user sees |
|---|---|---|
| Rampart Range Motorized Recreation Area | Not an entity. The name occurs only inside trailhead restriction text. | Nothing to select. No boundary, no entrance, no description. |
| Rampart Range trails | 102 USFS segments, clipped to the county | Names, numbers and use strings as tabled above. Searching "Rampart" in trails finds nothing. |
| Rampart Range Road | 4 road segments named RAMPART RANGE, route id 6196010465 **(code/data read)** | **(programmatic selection)** "RAMPART RANGE / USDA Forest Service / Source fetched 2026-09-27 · older than the refresh policy; refresh needed / Road geometry only. Vehicle and season designations are not evaluated. / Current road conditions and vehicle suitability are unconfirmed." Not searchable. No statement about unlicensed vehicles. |
| RAMPART ENTRANCE (trailhead record) | Pin at 39.377162, -105.094122, near the Highway 67 junction | Detail shows directions for a different place: "This easy trail follows the Reservoirs shoreline ... Take the Rampart Range Road north from Woodland Park (turn off Hwy 24 at McDonalds) ... Follow the signs to Rampart Reservoir." and "Drinking water is available at promontory picnic area during the summer." No restriction text, no warning that the text does not match the pin. "Official listing / source" falls back to the ArcGIS endpoint. |
| FLAT ROCKS TH | Trailhead record | Restrictions block, Water No, Restrooms No, directions, Google Maps link, five straight-line trail rows (BEGINNER 0.0, OVERLOOK 0.0, BARR 0.0, POWERLINE 0.1, TURTLE MOUNTAIN 0.2). Four of the five say "Outside published use dates". |
| FLAT ROCKS CG | Campground record | As quoted above. No fee, no reservation status, no day-use statement. |
| FLAT ROCKS OS (observation site) | Has directions and "April/May" season **(code/data read)** | Name, "USFS", fetch date, generic limitation, nothing else. |
| DUTCH FRED (trailhead and trail #0679) | Both present | Trailhead: restrictions block, Water No, Restrooms No. Trail: "Accepted use: 06/01-11/30", "Within published use dates — closures unchecked". The trailhead row under the trail reads "DUTCH FRED / 0.0 straight-line miles · connection unverified". |
| CABIN RIDGE PS (picnic) | Data holds "Day Use: $7 per vehicle per day", "Overnight use prohibited. Fires only in established fire rings. Pack it in; pack it out.", "Vault toilet", water "No", directions, season "May 8" **(code/data read)** | Only: "CABIN RIDGE PS / USFS / Source fetched 2026-09-27 · older than the refresh policy; refresh needed / Recreation-site inventory. Season and operational attributes can be historical; no live open status. / View source ↗ / Sources & coverage". Not even the words "picnic site". Not in the finder. |
| TOPAZ POINT (picnic) | Data holds "Vault toilets", water "No", season "May 15" **(code/data read)** | Same bare panel as Cabin Ridge PS. Not in the finder. |
| DEVILS HEAD PS (picnic), DAKAN (day use area) | Restrictions, toilets and water fields present **(code/data read)** | Same bare panel. Not in the finder. |
| Designated dispersed camping (`extras.js`) | One area, no geometry | As quoted above. |
| Sedalia / Highway 67 | Only inside agency directions text | Readable in trailhead and campground details. Searching "Sedalia" finds nothing; "67" matches trail numbers. Highway 67 is not a road in the product. |
| Larkspur / Spruce Mountain | Absent from all Douglas data **(code/data read)** | Searching either finds nothing. No origin field, no geolocation, no address entry. |

**Is the destination inside coverage?** Partly. The trailheads, picnic areas
and trails north of roughly the county line are inside the Douglas boundary.
The product says "County boundary used to clip sources ... Nothing is known
outside it." and "Segments are clipped at the county boundary and are not
complete routes." It never says how much of the Rampart system lies outside.
The user's home area lies inside the county outline but there is nothing there
in the product.

## What it could not answer (each as a question, with the app or site a user would need)

| # | Question | Critical? | Where the user must go |
|---|---|---|---|
| 1 | How do I drive from Larkspur / Spruce Mountain to Rampart, and which entrance is closest by road? | Yes | Google Maps or Apple Maps |
| 2 | Is the approach (Highway 67, Rampart Range Road, any road from the Larkspur side) suitable for a truck and trailer and open this weekend? | Yes | Forest Service motor-vehicle use map, Forest Service alerts, county road information |
| 3 | Which trailhead is a staging area with room to park a truck and trailer and unload? | Yes | Forest Service recreation page for each trailhead; a call to the ranger district |
| 4 | Are the trails by my staging point open to motorcycles on 10-11 October, given the app says "Outside published use dates"? | Yes | Motor-vehicle use map; ranger district |
| 5 | Which trail actually starts at the trailhead, and which trails connect into a ride? | Yes | Forest Service trail map for the motorized area; a trail app |
| 6 | Can my unlicensed bike use Rampart Range Road to move between trails? | Yes | Motor-vehicle use map. The restriction text says no, but it is unreviewed and not tied to the road. |
| 7 | Where can my family legally spend the day, and is day use allowed at a campground without camping? | Yes | Forest Service recreation pages for the picnic areas and campgrounds; recreation.gov |
| 8 | Are there picnic tables and shade? May a hammock be hung? | Yes for comfort, hammock is a legality question | Forest Service recreation page; ranger district |
| 9 | What does it cost (trailhead parking, day-use fee, OHV permit)? | Yes | Forest Service recreation pages; Colorado Parks and Wildlife for OHV registration. The app gives only a phone number inside restriction text. |
| 10 | Is the family spot reservable or first-come, and is it open in October? | Yes | recreation.gov; Forest Service recreation page |
| 11 | Are there fire restrictions, closure orders or trail closures in force? | Yes | Forest Service alerts; Douglas County Sheriff fire restrictions (both linked from the app) |
| 12 | How far is the family spot from the staging point by road or on foot? | Yes | Google Maps |
| 13 | How difficult are the trails, how long is a loop? | No | Trail app or Forest Service map. The app says "No difficulty, width, direction or bike-registration eligibility has been verified." |
| 14 | Is there mobile coverage, fuel, a backup if the lot is full? | No | Outside sources |

External sources needed for this trip, counted once each: (1) a navigation app,
(2) the Forest Service motor-vehicle use map, (3) Forest Service alerts, (4)
Forest Service recreation pages for trailheads and picnic areas, (5)
recreation.gov, (6) Douglas County Sheriff fire restrictions, (7) Colorado
Parks and Wildlife OHV registration, and probably (8) a phone call to the
ranger district for hammock and day-use rules.

## Relationships

| Relationship | Established? | How |
|---|---|---|
| Origin to anything | **Not at all** | No origin can be entered. The Google Maps link carries a destination only. |
| Route to Rampart entrance | **Not at all** as a relationship | Agency directions prose from Sedalia or Denver on some records. The record named RAMPART ENTRANCE shows directions to a different place. |
| Entrance to staging / trailhead | **Not at all** | Prose mileages along Rampart Range Road ("approximately 6 miles") on some records. Road segments carry no link to sites. |
| Staging / trailhead to legal motorcycle trail | **Straight-line proximity only** | "Trails for selected activity nearby by straight-line distance", rows such as "BEGINNER · #0627 / 0.0 straight-line miles · connection unverified". |
| Trail to trailhead | **Straight-line proximity only** | "Trailheads nearby by straight-line distance". The trail DUTCH FRED and the trailhead DUTCH FRED are related only by a "0.0 straight-line miles · connection unverified" row. |
| Trail to campground | **Straight-line proximity only** | "Campgrounds nearby by straight-line distance". |
| Staging to family day-use option | **Not at all** | A trailhead page lists trails only. Picnic sites are in no listing. The only path is trailhead, then a trail, then that trail's campground rows. |
| Trail segment to trail segment (a rideable loop) | **Not at all** | "This is a county-clipped segment, not a complete route. GPX does not provide turn-by-turn guidance or confirm rideable connections." |
| Restriction text to the road or trails it governs | **Not at all** | The Rampart restriction block sits on trailhead records only. |

The product is consistent and honest that proximity is not connection. It
simply has no real relationship of any kind.

## Evidence and unknowns

**What each answer carries.**

| Answer | Source shown | Date shown | Class shown to the user |
|---|---|---|---|
| Trail use strings | "USDA Forest Service", link to the layer endpoint | "Source fetched 2026-09-27 · older than the refresh policy; refresh needed" | "Published trail geometry and use strings. Not current access or closures." Source fact, clearly labelled. |
| Date result ("Outside / Within published use dates") | None of its own | None | Not labelled as derived. Shown as a status line under the trail name. |
| Trailhead restrictions | "USFS", link to the layer endpoint and to the fs.usda.gov page | Same stale fetch line | "Published restrictions" under "Published source · current access unconfirmed". Agency statement, unreviewed. |
| Water, restrooms, season | Same | Same | "Published season (may be historical)". No per-field date. |
| Straight-line distances | None | None | Labelled straight-line and "connection unverified". Effectively marked derived. |
| Dispersed area listing | recreation.gov link | "Source fetched 2026-09-27 · older than the refresh policy; refresh needed" | No agency named; carries the recreation-site limitation line. The text is an editorial summary of the listing, not labelled as such. |
| Roads | "USDA Forest Service" | Same stale fetch line | "Road geometry only." |
| Unknowns | n/a | n/a | "Unknown — no published use record"; "unshaded land is unknown"; "access status is unknown on every feature". |

Findings:

- **No fact is reviewed and none has a review date.** Only a fetch date per
  record.
- **Every fact relied on is outside the product's own refresh policy** (168
  hours; fetched 27 September). The app says so on every panel, which is
  correct, and also means a user is planning on data the product itself calls
  overdue.
- In Sources & coverage the trail and road layers read "No retrieval status is
  recorded for this layer", while each trail and road feature reads "Source
  fetched 2026-09-27". The two statements disagree.
- "View source ↗" opens an ArcGIS REST service page for the whole layer. On a
  phone this is not evidence a person can read.
- The product does not use the vocabulary source fact / official statement /
  derived / unknown. It approximates it with "Published ...", "(may be
  historical)", "connection unverified" and "Unknown".

**Restriction categories shown as checked or not checked.** The product has no
checked / not-checked display. At baseline the scenario asks for the region
fact-coverage statements shown. They appear as unlabelled paragraphs in Sources
& coverage; the category names and the states `context` / `none` are not shown
**(states from code/data read of `region.json`)**:

| Category (state in data) | Statement shown |
|---|---|
| Ownership (context) | "Five limited-scale management polygons only. They are not parcels or surveyed boundaries..." |
| Public access (none) | "No public-access evidence is loaded..." |
| Camping permission (none) | "No camping permission is confirmed. A recreation-site record shows that a facility is listed, not that it is open or that a given setup may stay." |
| Closures (none) | "No closure or fire-restriction status is loaded. The linked county page covers county jurisdiction only; federal orders must be checked separately." |
| Restrictions (none) | "No reviewed stay limits, seasons, permits or orders are loaded." |
| Road access (context) | "USFS road geometry only. Vehicle and season designations are not evaluated; access status is unknown on every feature." |
| Trail access (context) | "USFS published trail-use strings, kept verbatim... Not evaluated against closures or current conditions." |
| Recreation permission (none) | "No recreational-use permission is loaded..." |

There is no category for day use, fees, reservations, facilities or hammocks,
so the product cannot say those are unchecked; it is silent.

**Unknowns correctly surfaced (credit).** Closures and fire restrictions;
current access ("Published source · current access unconfirmed"); road
vehicle and season designations; road conditions; trailer parking ("Check
approach roads and trailer parking before travel"); connections between places
("connection unverified"); complete routes (county clipping); camping
permission; stay limits, availability and vehicle suitability; difficulty,
width, direction and registration eligibility; staleness of every USFS record;
historical season fields; land ownership and public access; unmapped campsites
in the dispersed area. The product also deliberately does not show the
source's "OPEN" operational status field, which avoids a false "open".

## Measures

| Measure | Result |
|---|---|
| Time to a recommended outing | **Not reached.** The product never recommends an outing. A candidate (stage at FLAT ROCKS TH or DUTCH FRED; family at FLAT ROCKS CG) can be assembled, but it is not viable: its critical unknowns are not all listed by the product and several are silent. |
| Planning steps (in app, to giving up) | 14: open app; follow Douglas link; expand sheet; Find trails & camping; open Filters; set From; set Through; set vehicle; scan trails; open a trailhead; open a nearby trail; open a nearby campground; tap picnic pins; open Sources & coverage. |
| External apps and sites required | 7 certain, 8 likely (list in the previous section). Forced by: route (step 4), road legality and seasons (2, 4), closures (7), staging and day use (3, 5), fees and reservations (5), registration (2). |
| Manual searches | 5 or more in the app (trail name, trailhead name, campground, "Rampart", picnic). Outside the app at least one search per external source, about 7. |
| Address or coordinate copy-pastes | 0 for a pinned destination (the Google Maps link carries coordinates). 1 for the home origin if location services are off. 1 or more for each picnic area and for the dispersed area, which have no directions link: the user must retype the name elsewhere. Expect 3 to 4. |
| Unresolved critical questions | 12 (questions 1 to 12 above). |
| Confirmed (reviewed) facts shown | **0.** Nothing in Douglas is reviewed or confirmed. |
| Source-published statements shown and relied on | About 17: five rules in the Rampart restriction block; water and restrooms at the trailhead (2); directions prose (1); motorcycle, ATV and 4WD strings for the chosen trail (3); campground water, restrooms, listed activities, licensed-vehicles rule and season (5); dispersed area fee and closure (1). All unreviewed, all outside refresh policy. |
| Derived statements shown | 4 kinds: the date result per trail; straight-line distances; "older than the refresh policy"; the count summary "102 trail segments · 5 campgrounds · 17 trailheads". |
| Correctly surfaced unknowns | 14 (listed above). |
| Unsupported assumptions the product would lead a user to make | **4 for this trip** (target 0), detailed below, plus 1 outside this trip. |
| Proximity assumptions | 2 needed to build any plan: that the trails at 0.0 to 0.2 straight-line miles from the trailhead are reachable from it, and that a campground 0.2 straight-line miles from a trail is a nearby, reachable family spot. Each is labelled "connection unverified", so the product does not encourage them, but it offers nothing else. |
| Evidence freshness and completeness | Of about 17 statements relied on: 17 carry a source and a fetch date, 0 carry a review date, 0 are within policy. |
| Evidence coverage shown | No checked / not-checked display. Eight fact-coverage statements shown without labels: three context, five none. Nothing for day use, fees, reservations or facilities. |
| Backup available | Partly. Alternative trailheads (DUTCH FRED, GARBER CREEK, RIM ROAD) and campgrounds (DEVILS HEAD CG, INDIAN CREEK) can be named. No backup can be confirmed, and no backup day-use place can be found. |
| Explainability | Partial. The tester can say what is uncertain, because the product says it. The tester cannot say why the plan is viable, because the product gives no reason to believe the trails are open, connected or reachable. |
| Phone burden | About 12 taps to the first trail list with correct dates; 2 to 3 more per place opened. A trailhead detail is about 1,640 px tall in a 526 px panel at full height, roughly three screens of scrolling, with the rules below the fold. Issues listed below. |

**Unsupported assumptions, strictly.**

1. **Trail season.** The app tells the user that 40 of the 76 dirt-bike
   segments, including FLATROCK, CABIN RIDGE, NODDLE, BEGINNER, OVERLOOK and
   BARR, are "Outside published use dates" on 10-11 October, from a string reading "Accepted use: 12/01-03/14".
   The same panel says the records are "not a check for your trip dates" and
   "can be incomplete or surprising". The user must assume either that the
   area is mostly shut to motorcycles in October or that the product's result
   is wrong. Neither is supported. This alone can change go / no-go.
2. **RAMPART ENTRANCE.** The record a first-time visitor is most likely to open
   shows directions to Rampart Reservoir from Woodland Park and drinking water
   at a "promontory picnic area". The product shows it verbatim as "Agency
   directions" with no flag. A user would assume this text describes the
   entrance to the motorized area.
3. **Family day use at a campground.** Because picnic areas are invisible in
   the finder and blank on the map, the only described place is a campground
   that lists "PICNICKING", water and toilets. The user must assume a family
   may occupy it for the day without camping, at no stated fee, in October.
4. **Fees.** No fee is shown for any trailhead or campground, and the absence
   is not stated as unknown. The data for CABIN RIDGE PS holds "$7 per vehicle
   per day" and the app does not show it. The user is left to assume staging
   and day use are free.
5. (Outside this trip.) The TURKEY trailhead shows directions beginning
   "Travel north of Elkhart on Highway 27 to the Cottonwood Picnic Grounds",
   plainly another place, again unflagged.

**Phone burden notes.**

- A first-time user who opens `v2/` lands on the Aspen / Snowmass planner. The
  Douglas entry is a text link at the bottom: "Explore Douglas County dirt
  biking & camping →".
- In the headless phone screenshot of that landing page the select boxes, date
  inputs and the two buttons rendered as blank white boxes although their text
  is present in the DOM. This may be a headless artefact; it needs a
  real-device check before it is called a defect.
- At the default Douglas zoom the 36 pins are unlabelled white 44 px discs
  stacked on top of each other over the Rampart area. Picking Cabin Ridge PS
  or Topaz Point by sight is not possible without zooming well in.
- The sheet opens at 40 percent height. Filters are collapsed, so the dates
  default silently to today and tomorrow.
- "Camping vehicle: Truck with trailer" changes nothing in any list; it is
  only saved and exported. The note says "Camping vehicle suitability needs
  individual review."
- The same trail number appears several times as separate segments with
  opposite results (TURTLE MOUNTAIN · #0770 and ARROWHEAD · #0646 each appear
  once "Within" and once "Outside"), with nothing to tell them apart in the
  list.
- Every trailhead page ends "A nearby motorcycle trail does not permit riding
  an unlicensed bike through this campground." The caution is right; the noun
  is wrong on a trailhead.
- "Published uses: 54321" is shown without explanation.
- Saved plan works (FLAT ROCKS TH saved, listed, exportable) and repeats "No
  access or availability is confirmed."

## Proximity wording observed

All from `main` at `bb85785`, observed in the app unless marked.

| Where | Exact wording |
|---|---|
| Default landing page (Aspen) | "See camping listings and trails by straight-line distance." |
| Finder, inside the collapsed Filters block | "Nearby means within five straight-line miles, not a rideable connection." |
| Trail detail, heading | "Campgrounds nearby by straight-line distance" |
| Trail detail, heading | "Trailheads nearby by straight-line distance" |
| Trail detail, rows | "FLAT ROCKS CG / 0.2 straight-line miles · connection unverified" |
| Trail detail, empty case **(code read)** | "None in this imported inventory within five straight-line miles." |
| Trailhead and campground detail, heading | "Trails for selected activity nearby by straight-line distance" |
| Trailhead and campground detail, rows | "BEGINNER · #0627 / 0.0 straight-line miles · connection unverified / Outside published use dates" |
| Site detail, empty case **(code read)** | "No matching imported segments within five straight-line miles." |
| Trailhead and campground detail | "A nearby motorcycle trail does not permit riding an unlicensed bike through this campground." |
| Sources & coverage | "Distances to campgrounds, trailheads and trails are straight-line and are not connections." (placed inside the water / recreation-permission paragraph) |
| Aspen planner only **(code read, `capabilities.js`)** | "Distances are straight-line, not driving distances. Directions may not reflect closures or permission to use the approach." Not shown in Douglas. |

The scenario document's baseline still quotes the older headings ("Campgrounds
nearby", "Nearby trails for selected activity"); `main` now shows the
straight-line wording above. No place was found where "nearby" appears without
"straight-line" beside it, except the unlicensed-bike caution. The only
weakness is "0.0 straight-line miles": a first-time user will read 0.0 as "at
the trailhead" whatever the suffix says.

## Critical product question

**Could a first-time Rampart visitor confidently leave home using only
Ohvernight? NO.**

What keeps it from YES, in order:

1. It cannot get the user from Larkspur to anywhere. No origin, no route, no
   "closest by road".
2. It gives a date result that says most Rampart trails are outside their
   published motorcycle dates this weekend, while disclaiming that result on
   the same screen. A careful user stops here; a careless one ignores it.
   Either way the product has not answered "may I ride".
3. It cannot say where to park and unload a truck and trailer.
4. It has no usable family day-use answer: picnic areas are unsearchable and
   blank, and fee, table, shade, reservation and hammock information is
   absent.
5. It has no current status of any kind: no closures, orders, fire
   restrictions or road status. It says so, correctly.
6. Nothing connects a trailhead to a trail or to a family place except
   straight-line distance.
7. Nothing shown is reviewed, and everything shown is past the product's own
   refresh policy.
8. One prominent record (RAMPART ENTRANCE) carries directions to the wrong
   place.

What it does well: it never claims a place is open, legal or connected; it
surfaces the Rampart rule block (registration, spark arrestor, 50-inch limit,
plates on roads) that a first-timer most needs; and its proximity wording is
now unambiguous. It is a truthful research index, not yet a trip answer.

## Top gaps ranked by how much they block this trip

1. **No origin and no route.** The question "closest practical place from
   Larkspur" cannot be asked.
2. **Trail season result contradicts itself and blocks the go decision.** 40
   of 76 dirt-bike segments read "Outside published use dates" for 10-11
   October from unreviewed strings; the product needs either a reviewed season
   or no verdict.
3. **Family day use is invisible.** Picnic and day-use records are loaded and
   pinned, but they are not in the finder and their detail shows none of the
   fields the data holds (fee, toilets, water, overnight prohibition,
   directions, even the site type).
4. **No staging identity.** Nothing says which trailhead takes a truck and
   trailer or where unloading is allowed.
5. **No current status.** Closures, fire restrictions, orders and road status
   are link-outs only.
6. **No real relationships.** Trailhead to trail, staging to family place, and
   rule text to the road and trails it governs are all missing; only
   straight-line rows exist.
7. **Rampart Range Road legality for an unlicensed bike is not attached to the
   road.** The sentence exists on trailhead records; the road panel is
   geometry only.
8. **Mismatched source text shown unflagged** (RAMPART ENTRANCE, TURKEY).
9. **No fee, reservation, first-come, table, shade or hammock information**
   for any day-use place, and no statement that these are unknown.
10. **The Rampart Range Motorized Recreation Area is not a thing in the
    product.** It cannot be searched, and the product does not say how much of
    it lies outside the county clip.
11. **Evidence is stale and unreadable on a phone.** Fetch dates are 11 days
    old against a 7-day policy; "View source" is a service endpoint; the
    Sources dialog and the feature panels disagree on trail and road retrieval
    status.
12. **Phone friction.** Stacked unlabelled pins, collapsed date filters, a
    vehicle selector with no effect, duplicate segment rows, three screens of
    scrolling per place.
