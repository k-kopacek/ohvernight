DRAFT - UNREVIEWED RESEARCH

# Rampart Range (north end), 10-11 October 2026: motorcycle legality, trailhead-trail links, forest orders

- Prepared by a bounded research worker standing in for the Hermes lane. Retrievals 2026-10-09 04:57 to 05:06 UTC (evening of 8 October, Mountain time). Times below are UTC from `date -u` on the research machine, per batch.
- Trip: Sat-Sun 10-11 October 2026; dirt bike assumed NOT street-legal (no plate), trucked in; family at a nearby picnic / day-use site.
- Extends, and does not repeat, `rampart-official-facts.md`, `rampart-evidence-closure.md`, `rampart-relationships.md`, `trail-date-semantics-research.md` (same folder).
- Strength labels: **CONTROLLING** (regulation, signed forest order, the published Motor Vehicle Use Map) / **OFFICIAL** (agency page or agency dataset; not the legal instrument) / **PARTNER** (Rampart Range Motorcycle Management Committee, RRMMC, a volunteer partner) / **LEAD**. **DERIVED** marks my own reasoning or geometry calculation.
- LEGAL DESIGNATION and CURRENT PHYSICAL CONDITION are kept apart. Nothing below is a statement that a trail is passable, signed, dry or clear of downed trees.
- Budget: 3 web searches (of 30). About 66 page/service requests, 7 of them failures - this is a few over the 60 bound; stated openly. No one contacted, no login, nothing edited except this file. Scratch downloads are in `/tmp/rampart-w3/` (not in any repository).

## How the MVUM was re-read (method, so a reviewer can repeat it)

1. Both South Platte MVUM PDFs were downloaded again (front 2,559,879 bytes; back 3,957,882 bytes; 04:57 UTC).
2. The earlier draft said the PDFs have no text layer. **That is only partly right.** Opened with PyMuPDF 1.28 (installed in a throwaway virtual environment under `/tmp`), each PDF has a real text layer for the legend, the "Explanation of legend items", the prohibitions, the blanket statements and every route label on the map and inset. Those quotes below are **text-layer reads, not image reads**.
3. The "Seasonal and Special Vehicle Designations" table is NOT in the text layer (it is embedded as graphics). I rendered it from the vector PDF at about 300 dpi equivalent and read the image. So the table is still an image reading - a second, independent one, at higher resolution than the first.
4. Line types on the Rampart Range Road Inset (which symbol a route is drawn with, and whether it carries the grey "seasonal" halo) are my image reading of high-zoom renders.
5. Forest Service MVUM feature service `EDW_MVUM_02` layers 1 (roads) and 2 (trails) were queried once each for the box lon -105.14..-105.04, lat 39.26..39.38 (50 trail records, 19 road records), all fields, with geometry.
6. NOT ATTEMPTED: the Avenza georeferenced version and the interactive Forest Service MVUM web map (same underlying PDF and the same EDW layer respectively; no added authority).

---

## A. Motorcycle legality

### A1. Controlling rule

| Fact | Quote | Source | Strength | Static/dynamic |
|---|---|---|---|---|
| Riding anywhere not designated on the MVUM is prohibited | "it is prohibited to possess or operate a motor vehicle on National Forest System lands in that administrative unit or Ranger District other than in accordance with those designations" | 36 CFR 261.13, eCFR, https://www.ecfr.gov/current/title-36/section-261.13 (renderer API), 05:05 UTC | CONTROLLING | static |
| Same, as printed on the map | "It is prohibited to possess or operate a motor vehicle on National Forest System lands on the South Platte Ranger District other than in accordance with these designations (36 CFR 261.13)" ... "This prohibition applies regardless of the presence or absence of signs." | South Platte MVUM (front), text layer, https://www.fs.usda.gov/sites/nfs/files/r02/psicc/publication/SPLTMVUMFINALFRONT07302025.pdf, 04:57 UTC | CONTROLLING | static |
| Designation is by vehicle class and season | "shall be designated by vehicle class and, if appropriate, by time of year" | 36 CFR 212.51(a), eCFR, 05:05 UTC | CONTROLLING | static |
| State law still applies | "As a motor vehicle operator, you are also subject to State traffic law, including State requirements for licensing, registration, and operation of the vehicle in question." and "The designation "road or trail open to all motor vehicles" does not supersede State traffic law." | MVUM front, text layer | CONTROLLING | static |
| Off-road operating rules | prohibited "to operate any vehicle off National Forest System, State or County roads: (a) Without a valid license as required by State law. (b) Without an operable braking system. (c) From one-half hour after sunset to one-half hour before sunrise unless equipped with working head and tail lights. (d) In violation of any applicable noise emission standard established by any Federal or State agency. ... (i) In violation of State law established for vehicles used off roads." | 36 CFR 261.15, eCFR, 05:05 UTC | CONTROLLING | static |
| Temporary closures can override the map | "Designated roads, trails and areas may also be subject to temporary, emergency closures. As a visitor, you must comply with signs notifying you of such restrictions." | MVUM front, text layer | CONTROLLING | static |
| Not on the map means not open | "If a route is not on the MVUM, it is not open to motorized use. Signs may or may not be posted; regardless, it is the driver's responsibility to reference the MVUM to stay on designated motorized routes." | https://www.fs.usda.gov/r02/psicc/maps-guides/motor-vehicle-use-maps, 05:05 UTC | OFFICIAL | static |

**Which edition is in force.** The forest's MVUM index lists, for this district only, "South Platte Ranger District 2025 MVUM PDF (front) / 2025 MVUM PDF (back)" while other districts show "2026 MVUM PDF" (page "Last updated March 30, 2026"). The PDF cover reads "Colorado Sept 2025"; it carries "Digitally signed by BRIAN BANKS Date: 2025.12.10". The map says both that designations "will remain in effect until superseded by the next year's MVUM" and that each January it "will either be revised with the publication of a new map, or it will be validated for the new year by the Ranger District with a red stamp that says: "Valid for Year 20__"". I saw no such stamp on the downloaded PDF. **Whether the 2025 map has been formally validated for 2026 is UNKNOWN**; it is the only South Platte MVUM the forest publishes today.

### A2. Trail classes on the South Platte MVUM and whether each admits a motorcycle

Legend (text layer, MVUM front and back): "Roads Open to Highway Legal Vehicles", "Roads Open to All Vehicles", "Roads with Special Vehicle Designation", "Trails open to All Vehicles", "Trails Open to Vehicles 50" or Less in Width", "Trails Open to Motorcyles Only" [sic], "Seasonal Designation (SeeTable)".

"Explanation of legend items" (text layer, MVUM front) - CONTROLLING:

| Class | Printed definition | Motorcycle admitted? |
|---|---|---|
| Trails Open to Vehicles 50" or Less in Width | "Trails open only to motor vehicles less than 50 inches in width at the widest point on the vehicle." | Yes (a motorcycle is under 50 inches). The table words it "Trail, <50" wide (open to OHVs such as ATVs and motorcycles)". |
| Trails Open to Motorcycles Only | "Trails open only to motorcycles. Sidecars are not permitted." | Yes; ATVs are not. |
| Trails Open to All Vehicles | "Trails open to all motor vehicles, including both highway legal and nonhighway legal vehicles." | Yes. |
| Roads Open to All Vehicles | "Roads open to all motor vehicles, including smaller off highway vehicles that may not be licensed for highway use (not to oversize or overweight vehicles under State traffic law)." | Yes, including unplated - subject to State law (see A4). |
| Roads Open to Highway Legal Vehicles Only | "Roads open only to motor vehicles licensed under State law for general operation on all public roads." | Plated only. |
| Special Vehicle Designation | "This symbol indicates the road or trail is open to classes of vehicles other than those listed above. Refer to the Seasonal and Special Vehicle Designations Table for further instructions." | Not stated here; see A4. |
| Seasonal Designation | "This symbol, used in conjunction with one of the other road or trail symbols, indicates that the route is open only during certain portions of the year. Refer to the Seasonal and Special Vehicle Designations Table for further instructions." | - |

- **ATVs**: admitted on "<50 inch" trails and "all vehicles" trails, not on "motorcycles only" trails. Forest Service page: "Only vehicles 50" or less in width can be on trails." (https://www.fs.usda.gov/r02/psicc/recreation/dutch-fred-trailhead, 05:04 UTC, OFFICIAL).
- **The 50-inch rule**: the MVUM definition quoted above (CONTROLLING) and 36 CFR 212.1 "Trail. A route 50 inches or less in width or a route over 50 inches wide that is identified and managed as a trail." (eCFR, 05:05 UTC).

### A3. Seasonal table - my independent reading, and agreement with the earlier reading

Table "Seasonal and Special Vehicle Designations" (MVUM back, upper left; identical table on the front, lower right). Columns: Route Numbers / Legend (Linetype, Description) / Dates Allowed / Beginning Mile Post / Ending Mile Post. Rows relevant here, as I read them:

| Route numbers | Description | Dates allowed | Mile posts |
|---|---|---|---|
| 0627, 0646, 0649.A, 0650, 0653, 0657, 0662, 0673, 0673.A, 0674, 0674.B, 0675, 0677, 0679.A, 0679.B, 0680, 0681, 0681.B, 0681.C, 0681.E, 0682, 0682.A, 0682.AA, 0683, 0685, 0686, 0686.A, 0688, 0787, 0787.A, 0788 | "Trail, <50" wide (open to OHVs such as ATVs and motorcycles)" | "May 16 - March 14" | Entire Length |
| 0649 | same | "May 16 - March 14" | "0-1.84", "8.24-9.45" |
| 0693 | "Trail Open to Motorcycles only" | "June 1 - March 31" | Entire Length |
| 0767, 0767.A | "Trail Open to All Vehicles" / "Trail, <50" wide (open to OHVs such as ATVs and motorcycles)" | "May 16 - November 30" / "December 1 - March 14" | Entire Length |
| 0770 | "Trail Open to Motorcycles only" | "May 16 - March 14" | Entire Length |
| 300, 300.M, 300.O, 300.P, 300.PA, 300.Q, 300.R, 300.S, 300.T, 300.U, 348, 502, 503, 502.2, 502.B, 506, 507, 563 | "Road, Special Vehicle Designation" / "Roads Open Only to Vehicles 50" or Less in Width" | "May 16 - November 30" / "December 1 - March 14" | Entire Length |

**Agreement:** my reading of every row above matches the earlier image-based reading in `rampart-evidence-closure.md` section 2.2, route for route and date for date. I found no digit I would read differently. Two independent image readings now agree; the table is still not machine-readable text, so a person glancing at the PDF remains the final check.

**10-11 October 2026 falls inside "May 16 - March 14" and inside "May 16 - November 30".** On the MVUM table, every listed numbered Rampart trail above is legally open to motorcycles on the trip dates. Strength CONTROLLING (image-read twice). Legal designation only.

**New findings the earlier draft did not have:**

1. **0690 (Powerline) is on the map, drawn as "Trails Open to Vehicles 50" or Less in Width" with NO grey seasonal halo** (my image reading; label "0690" is in the text layer of the inset). A route with no seasonal symbol has no row in a seasonal table - that is why 0690 is absent from it. The agency layer agrees: `690`, mile 2.29-9.07, "Trails open to vehicles 50" or less in width, Yearlong", `motorcycle` open "01/01-12/31" (EDW_MVUM_02 layer 2, 04:59 UTC, OFFICIAL). **Earlier unknown resolved: 0690 is a year-round <50-inch trail.** Caveat: the northernmost piece, mile 9.07-9.456 near the Highway 67 entrance, is "Special Designation, Yearlong" in the layer with only `other_ohv_lt50inches` open and the motorcycle field empty - motorcycle status of that last 0.39 mile is UNKNOWN.
2. **0679 (Dutch Fred Trail) is on the map, drawn as a <50-inch trail WITH the seasonal halo, but has no row in the table** (0679.A and 0679.B are listed; 0679 is not). The map therefore says "seasonal, see table" and the table is silent. The agency layer gives `679` motorcycle open "06/01-11/30" (OFFICIAL, not the legal instrument). 10-11 October is inside that window. **Legal season of 0679 from the controlling map: UNKNOWN (internal omission); from agency data: June 1 - November 30.**
3. **Short connectors that the agency layer shows as ATV-only**: `627.A` (Quarry Cut-Off), `681.D` (Beginner/Scottys Connector), `681.F`, and the first 0.17 mile of `770.A` (Tunnel) are "Special Designation, Yearlong" with only `atv` open "01/01-12/31" and no motorcycle value; the companion trails dataset marks motorcycles "restricted" year-round on them. None of them is in the MVUM table and I did not find their labels in the inset text. **Motorcycle legality on these four short pieces: UNKNOWN - treat as not established.** The 770.A piece starts 35 m from the Flat Rocks Trailhead point (see B), while the published map draws a motorcycles-only dotted line leaving the trailhead symbol there. Conflict preserved.

### A4. Agency layer versus the published map (the "12/01-03/14" problem)

- For 30-odd trails the layer still stores motorcycle "12/01-03/14" only (confirmed again at 04:59 UTC for 627, 673, 673.A, 674, 674.B, 675, 677, 679.A, 680, 681, 681.B/C/E, 682, 682.A/AA, 685, 686, 686.A, 688, 787, 787.A, 788 and others).
- New evidence about why: the layer **can** hold two windows in one field - road `506` has motorcycle "01/01-03/14,05/16-12/31" - and trail `646` appears as two records, mile 0-0.79 "05/16-11/30" and mile 0.83-1.19 "12/01-03/14", whose union is the map's "May 16 - March 14". DERIVED: the trail records look like half of a two-part season was published. I still cannot prove that; it is an inference.
- The layer's own description: "The feature class is consistent with the appropriate National Forest's Motor Vehicle Use Map (MVUM)." and "Any reference to Open or Dates Open refers strictly to when it is legal to use that motor vehicle on the trail." Its metadata (earlier draft): "not legal documents".
- **Position:** the signed published map is the instrument 36 CFR 261.13 enforces. Where the layer and the map disagree, the map controls and the layer is a known-defective copy for these trails. The conflict is preserved in "Conflicts preserved"; I do not use the layer to answer "is it open in October" except where the map itself is silent (0679, 0690).

### A5. "Road, Special Vehicle Designation" and Rampart Range Road (NFSR 300)

What the controlling map says, in full: the legend definition quoted in A2 ("open to classes of vehicles other than those listed above. Refer to the ... Table for further instructions") and the table row "Road, Special Vehicle Designation - May 16 - November 30" followed by "Roads Open Only to Vehicles 50" or Less in Width - December 1 - March 14". **The table gives no further instruction naming the classes allowed from May 16 to November 30. The map is circular on this point; it does not say in words that non-street-legal vehicles are, or are not, permitted on NFSR 300 in the summer-fall season.** NFSR 300 is drawn with the "Roads with Special Vehicle Designation" line type plus seasonal halo (my image reading).

What fills the gap:

| Evidence | Content | Strength |
|---|---|---|
| EDW_MVUM_02 layer 1, road `300 RAMPART RANGE` (mile 38.299-56.666), "Special Designation, Seasonal", 04:59 UTC | `passengervehicle`, `highclearancevehicle`, `truck`, `bus`, `motorhome` open "05/16-11/30"; `atv`, `motorcycle`, `otherwheeled_ohv`, `tracked_ohv_lt50inches`, `other_ohv_lt50inches` open "12/01-03/14"; the over-50-inch OHV classes are empty | OFFICIAL |
| Same layer, a road the layer labels "Roads open to highway legal vehicles only" (`513 INDIAN CREEK CG`) | the same five classes and nothing else | OFFICIAL |
| Forest Service trailhead pages (Dutch Fred, Flat Rocks, Garber Creek), restrictions that "apply to the Rampart Range Motorized Recreation Area" | "A current license plate and valid driver's license are required to ride on the roads." | OFFICIAL |
| Colorado statute | "It is unlawful to operate an off-highway vehicle on the public streets, roads, or highways of this state ... except ... When a street, road, or highway is designated open by the state or any agency of the state; When crossing streets or when crossing roads, highways, or railroad tracks ..." C.R.S. 33-14.5-108(1) | CONTROLLING text, read on a secondary host (colorado.public.law, "Current through Fall 2025"), 05:05 UTC |
| RRMMC directions page | "Note that Rampart Range Road is not open to unlicensed vehicles." | PARTNER |
| RRMMC FAQ | "Any vehicle operating on the road must have a valid license plate ... and the operator must posses a valid drivers license with a motorcycle endorsement. The exceptions to this rule are portions of Dakan Road, Jackson Creek Road and Watson Park Road." (The same answer calls it "a county road", which conflicts with the agency's "FS - FOREST SERVICE" jurisdiction value.) | PARTNER |

DERIVED: from 16 May to 30 November the classes open on NFSR 300 in the agency data are exactly the highway-legal set; the under-50-inch OHV classes are open on it only from 1 December to 14 March, which matches the table's second row. That is what makes it "special" - a highway-legal road in season that becomes an OHV route in winter. **Answer: a plated, street-legal motorcycle and a licensed rider are required on Rampart Range Road on 10-11 October; an unplated dirt bike may not be ridden on it.** Confidence HIGH. Basis: OFFICIAL prose + OFFICIAL data + state statute + PARTNER, all consistent; the CONTROLLING map is consistent with this but does not state it in words.

**Spur roads to the trailheads - not uniform, and internally inconsistent in the map:**

| Spur | MVUM table | MVUM line type as drawn (my image reading) | EDW layer | Other |
|---|---|---|---|---|
| 506 Dutch Fred (0.2 mile) | listed in the "Road, Special Vehicle Designation" row | drawn with the "Roads Open to All Vehicles" pattern (heavy line with white dashes) plus seasonal halo | "Roads open to all Vehicles, Seasonal"; motorcycle and ATV open "01/01-03/14,05/16-12/31" | RRMMC's list of road exceptions does not include it |
| 300.T Flat Rock CG (0.58 mile) | same row | drawn with the "Roads Open to All Vehicles" pattern plus halo | symbol "Roads open to all Vehicles, Seasonal" but motorcycle/ATV dates only "12/01-03/14" | Forest Service campground page: "ATVs and off-road motorcycles are allowed to enter and depart the campground for trail access." and "this is the only designated campground allowing off-road vehicles on the road" |
| 300.U Sunset Point (0.1 mile) | same row | a very short stub; looked like the all-vehicles pattern, low confidence | "Special Designation, Seasonal", OHV classes winter only | - |
| 300.S Flat Rocks Overlook, 300.R Cabin Ridge PG, 300.M Topaz Point PG | same row | not examined closely | "Special Designation, Seasonal", OHV classes winter only | - |

**Unplated bike on the spurs: UNKNOWN / conflicting.** The table (controlling) puts 506 and 300.T with NFSR 300; the same map's line work and the agency layer draw them as open to all vehicles; the Forest Service page says off-road motorcycles may enter and leave Flat Rocks Campground. Not resolved. Practical consequence: unload at the trailhead lot and ride from the lot onto a trail; do not ride the spur roads on the unplated bike unless a ranger confirms it.

### A6. Moving between staging areas without using the road

- PARTNER, explicit: "The Powerline (#690) and beginner trails (#627) parallel the road most of the way and can be used to get from one area to another if your bike is not licensed." (https://rampartrange.org/directions/, 05:04 UTC).
- CONTROLLING/OFFICIAL support for the legality of those two trails: 0627 is in the MVUM table as a <50-inch trail, "May 16 - March 14"; 0690 is drawn as a <50-inch trail with no seasonal restriction and is year-round in the agency layer (mile 2.29-9.07).
- DERIVED from agency geometry (EDW_MVUM_02, my calculation, straight-line): `627` (name BEGINNER in the Forest Service trails layer) passes within 1-58 m of the agency points for Rampart Entrance (111 m), Mile and a Half (32 m), Garber Creek (14 m), Sunset Point (37 m), Flat Rocks TH (35 m), Rim Road (58 m), Cabin Ridge TH (1 m) and Cabin Ridge Picnic Site (32 m), and ends near Devils Head. `690` runs from about 39.2918, -105.0945 (near the 506 / NFSR 300 junction) north to about 39.3725, -105.0935, passing 81 m from Flat Rocks TH, 107 m from Sunset Point, 58 m from Garber Creek and 22 m from Mile and a Half.
- **Classification: SOURCE-BACKED by the partner, consistent with the controlling map and agency geometry.** No agency sentence states it. Both trails touch or cross NFSR 300 in places (geometry within 10 m); State law allows "crossing" a road, and the exact crossing points, gates and signing are UNKNOWN. This is a legal-designation finding; whether the whole length is rideable on a given day is not known.
- Dutch Fred to that corridor: 0627 does not pass the Dutch Fred lot. By geometry, 0681 runs north from the lot to 0767, whose north end sits on NFSR 300 about 20 m from 0627. DERIVED only; it needs a road crossing.

### A7. Registration, decal, spark arrester, sound, lights

| Requirement | Quote | Source | Strength | Static/dynamic |
|---|---|---|---|---|
| Registration or permit to operate | "All Off-Highway Vehicles must have either a current or valid Colorado Registration Card and two Decals or one Colorado Off-Highway Vehicle Permit to operate in Colorado. This includes while in route, in staging areas and on public land roads and designated trails. ... valid from April 1 through March 31 each year" | Colorado Parks and Wildlife, https://cpw.state.co.us/register-off-highway-vehicle, 05:05 UTC | OFFICIAL (state agency) | static, annual |
| Resident: card with the bike plus two decals | "Resident OHVs must have both a valid OHV Registration card available with the vehicle, and two current OHV Registration decals properly displayed on and affixed to the vehicle." | same | OFFICIAL | static |
| Decal position on a dirt bike | "position one decal on each of the outside faces of the upper end of the forks" | same | OFFICIAL | static |
| Non-resident: one permit | "All Non-Resident OHVs must have one valid OHV Permit properly displayed on and affixed to the vehicle or carry the valid bright green OHV Permit." | same | OFFICIAL | static |
| If just bought online | "You are required to carry your registration confirmation receipt on you while in the field, until you receive your registration card and decals" | same | OFFICIAL | static |
| On the map itself | "State of Colorado OHV sticker required for all users of motorized trails regardless of vehicle type." | MVUM front, text layer | CONTROLLING | static |
| Forest Service | "A Colorado OHV (Off Highway Vehicle) registration or current license plate with OHV permit is required to ride on the trails." | Dutch Fred Trailhead page, 05:04 UTC | OFFICIAL | static |
| Spark arrester | "All vehicles must have a U.S. Forest Service approved SPARK ARRESTOR." | Dutch Fred / Flat Rocks / Garber Creek trailhead pages | OFFICIAL | static |
| Spark arrester, state law | "No off-highway vehicle shall be operated upon public land unless it is equipped with ... Brakes and a muffler and spark arrester which conform to the standards prescribed by regulation of the division"; fine "for a violation relating to a spark arrester is one hundred fifty dollars" | C.R.S. 33-14.5-109, secondary host colorado.public.law, 05:05 UTC | CONTROLLING text, secondary host | static |
| Spark arrester, partner | "The rangers frequently run spark arrestor checks ... Many motocross bikes do not come with spark arrestors." | RRMMC FAQ, 05:04 UTC | PARTNER | - |
| **Sound limit** | "An off-highway vehicle operated within the state shall not emit more than the following level of sound when measured using SAE J1287: If manufactured before January 1, 1998 99 db(A); If manufactured on or after January 1, 1998 96 db(A)." | C.R.S. 25-12-110(1), secondary host colorado.public.law, 05:05 UTC | CONTROLLING text, secondary host | static |
| Sound, federal hook | 36 CFR 261.15(d) quoted in A1 makes a State noise standard enforceable on the forest off roads | eCFR | CONTROLLING | static |
| Sound, partner | "As of July 1, 2010, the 96db limit is now enforceable in Colorado and you may receive a ticket if you are over." | https://rampartrange.org/sound-limits/ | PARTNER | - |
| Lights | State: "At least one lighted head lamp and one lighted tail lamp ... while being operated between the hours of sunset and sunrise" (C.R.S. 33-14.5-109); federal 261.15(c) quoted above | as above | CONTROLLING | static |

- **Sound limit answer:** it is statute, not only partner lore - 96 dB(A) for a bike built on or after 1 January 1998, 99 dB(A) for older, SAE J1287 stationary test. The statute text was read on a non-official host; the Colorado Parks and Wildlife sound-law page (`/thingstodo/Pages/OHVsSoundLaw.aspx`) returned HTTP 404 - NOT RETRIEVED. No Forest Service page stating a decibel figure was found.
- Lights: required only for riding between sunset and sunrise. Trailheads are "open sunrise to sunset" in any case (Forest Service area page).
- A driver's licence is required by the Forest Service only "to ride on the roads" (quote above). Whether Colorado requires any licence for off-road trail riding by an adult was NOT researched.

### A8. Trails reachable from each candidate trailhead: legal class and dates on 10-11 October

"MVUM" = the controlling table/line type; "Layer" = EDW_MVUM_02 motorcycle dates (OFFICIAL, known-defective for most trails). Names are from the Forest Service trails layer (EDW_TrailNFSPublish_01, `trail_name`). How each trail relates to the trailhead is in section B.

| Trail | Name (agency) | MVUM class | MVUM dates | Layer motorcycle dates | Legal for a motorcycle 10-11 Oct per MVUM |
|---|---|---|---|---|---|
| 0627 | BEGINNER | <50" | May 16 - March 14 | 12/01-03/14 (conflict) | YES |
| 0690 | POWERLINE | <50", no seasonal symbol | none printed (year-round) | 01/01-12/31 (mile 2.29-9.07) | YES; last 0.39 mile at the north entrance UNKNOWN |
| 0673, 0673.A | BARR | <50" | May 16 - March 14 | 12/01-03/14 (conflict) | YES |
| 0674, 0674.B | FLATROCK, SPUR B | <50" | May 16 - March 14 | 12/01-03/14 (conflict) | YES |
| 0682, 0682.A, 0682.AA | OVERLOOK | <50" | May 16 - March 14 | 12/01-03/14 (conflict) | YES |
| 0770 | TURTLE MOUNTAIN | Motorcycles only | May 16 - March 14 | 12/01-03/14 for mile 0-40.97; 01/01-12/31 beyond | YES |
| 0770.A (first 0.17 mile at Flat Rocks) | TUNNEL | not in table; drawn dotted at the trailhead | - | ATV only, no motorcycle value | UNKNOWN |
| 0770.A (mile 0.17-6.68) | TUNNEL | not in table | - | "Trails open to motorcycles, Yearlong" 01/01-12/31 | not in the table; layer says yes; treat as OFFICIAL-only |
| 0688 | BEAVER | <50" | May 16 - March 14 | 12/01-03/14 (conflict) | YES |
| 0686, 0686.A | GARBER, GARBER CUTOFF | <50" | May 16 - March 14 | 12/01-03/14 (conflict) | YES |
| 0787, 0787.A | (unnamed) | <50" | May 16 - March 14 | 12/01-03/14 (conflict) | YES |
| 0662 | (unnamed) | <50" | May 16 - March 14 | 12/01-03/14 (conflict) | YES |
| 0681, 0681.B/C/E | SCOTTYS | <50" | May 16 - March 14 | 12/01-03/14 (conflict) | YES |
| 0681.D, 0681.F | BEGINNER/SCOTTYS CONNECTOR | not in table | - | ATV only | UNKNOWN |
| 0679 | DUTCH FRED | <50", seasonal symbol | **no row in the table** | 06/01-11/30 | UNKNOWN on the map; YES per agency data |
| 0679.A | DEVILS HEAD SPUR | <50" | May 16 - March 14 | 12/01-03/14 (conflict) | YES |
| 0767, 0767.A | UPPER DUTCH, LIGHTFOOT LOOP | Trail Open to All Vehicles | May 16 - November 30 | 05/16-11/30 | YES (a third agency dataset says motorcycles "restricted" all year - see Conflicts) |
| 0680 | (not looked up) | <50" | May 16 - March 14 | 12/01-03/14 (conflict) | YES |
| 0675 | CABIN RIDGE | <50" | May 16 - March 14 | 12/01-03/14 (conflict) | YES |
| 0627.A | QUARRY CUT-OFF | not in table | - | ATV only | UNKNOWN |

### A9. Current orders or closures affecting these trails (legal status, as of 05:02-05:04 UTC 9 Oct)

- The forest alerts list (44 entries, https://www.fs.usda.gov/r02/psicc/alerts) contains **no order naming NFSR 300 in Douglas County, Flat Rocks, Dutch Fred, Sunset Point, Cabin Ridge, Topaz Point or any numbered Rampart trail.** OFFICIAL, dynamic. Absence from a web list is not proof that no closure is posted on the ground.
- South Platte district items on the list: Harris Park RX closure (Park County; see C6), "Downed and weakened trees on South Platte Ranger District" (a condition notice, not an order), Devils Head climbing closure (1 March - 31 July only), over-snow vehicle order (not October), Mount Evans and Lost Creek wilderness orders (not here), and the standing orders in section C.
- CURRENT PHYSICAL CONDITION is a separate matter and is not established by any agency source: RRMMC's undated banner read "Trail Status: OPEN / Rampart Range Road Status: OPEN" at 05:04 UTC (PARTNER, dynamic, no timestamp).

---

## B. Trailhead -> trail relationships

Rules used. SOURCE-BACKED = a responsible source says the trail is at / starts at / is reached from that trailhead. DERIVED-STRONG = no sentence says it, but the Forest Service's own MVUM line geometry has a trail **endpoint** within about 50 m of the Forest Service's own coordinate for the trailhead, and the published MVUM inset shows the same arrangement. DERIVED-WEAK = a trail merely passes nearby. Distances are my straight-line calculations from EDW_MVUM_02 geometry (04:59 UTC) to the agency site coordinates (EDW_RecInfraRecreationSites_02 and the Forest Service pages, which agree). Geometry is not a legal connection and says nothing about gates, signs or direction. Difficulty: **no agency source states a difficulty for any of these trails**; the Forest Service "trail class" (TC3 developed, TC4 highly developed, TC5 fully developed) is a construction standard, not a difficulty rating, and is shown only as that.

| Staging area (agency record) | Trail | Vehicle class (MVUM) | Evidence | Classification |
|---|---|---|---|---|
| **Dutch Fred TH** (39.28573, -105.09196; capacity 55; restroom "No") | 0679 DUTCH FRED | <50" | Forest Service page: "The Dutch Fred Trail (#679) enters into a system of 115 miles of motorcycle and ATV trails". Geometry: line passes 11 m from the point; its mapped north end is 107 m from it. | SOURCE-BACKED (agency) |
| Dutch Fred TH | 0681 SCOTTYS | <50" | RRMMC: "trailhead for trail 681 (Scotty's Trail) (Dutch Fred TH)". Geometry: 0681's south end is 10 m from the agency point and 4 m from 0679. MVUM inset labels both 0681 and 0679 at Dutch Fred. | SOURCE-BACKED (partner) and DERIVED-STRONG |
| Dutch Fred area | 0767.A LIGHTFOOT LOOP, 0767 UPPER DUTCH | All vehicles, May 16 - Nov 30 | RRMMC FAQ: "The Lightfoot Loop is a designated one-way trail. It's a beginner trail ... The trail can be found at the Dutch Fred parking lot." MVUM inset prints "0767.A" beside the DUTCH FRED label. Geometry puts the loop beside the NFSR 300 / 506 junction, about 450-520 m north of the agency trailhead coordinate, joined to 0681 by 0767. | SOURCE-BACKED (partner) for "at Dutch Fred"; exact position relative to the lot DERIVED |
| Dutch Fred area | "Kiddy Corral" | not a numbered route | RRMMC only: "a fenced oval loop". Not found on the MVUM or in agency data. | PARTNER only; legal status as a designated riding area UNKNOWN |
| Dutch Fred area | 0680 | <50" | Geometry: starts 1 m from the top of road 506 at NFSR 300, leads west toward 0657 / 0770. | DERIVED-WEAK (not at the lot) |
| **Flat Rocks TH** (39.32728, -105.08692; capacity 85; restroom "No") | 0673 BARR | <50" | RRMMC: "Trail head for trail 673 (Bar Trail) (Flat Rocks TH)". Geometry: 0673 starts at NFSR 300 51 m from the agency point. | SOURCE-BACKED (partner) and DERIVED-STRONG |
| Flat Rocks TH | 0674 FLATROCK | <50" | Forest Service page: "The Flatrock Trail (#674) trail enters into a system of 115 miles". Geometry: 0674 does **not** reach the trailhead - its east end is about 0.8 km west-north-west, 18 m from 0673 and 403 m from the campground point. | SOURCE-BACKED (agency) as the trail the trailhead serves; reached via 0673 by geometry (DERIVED) |
| Flat Rocks TH | 0682 OVERLOOK | <50" | Geometry: north end on NFSR 300, 38 m from the point (the other side of the road as mapped). RRMMC ties 0682 to the separate overlook lot: "Flat Rocks overlook, kiddy track, trailhead for trail 682 (Overlook Trail)" at mile 4.6. | DERIVED-STRONG for proximity; SOURCE-BACKED (partner) for the overlook lot, not this lot |
| Flat Rocks TH | 0770 TURTLE MOUNTAIN via 0770.A TUNNEL | Motorcycles only | MVUM inset: a motorcycles-only dotted line leaves the trailhead symbol. Geometry: 0770.A starts 35 m from the point on spur 300.T; 0770 proper is about 270 m south. Agency layer marks the first 0.17 mile ATV-only. | DERIVED-STRONG that a route starts here; motorcycle legality of the first 0.17 mile UNKNOWN |
| Flat Rocks TH | 0627 BEGINNER, 0690 POWERLINE | <50" | Geometry: pass 35 m and 81 m away. Partner statement that both parallel the road. | DERIVED-WEAK (pass by; partner-backed as through-routes) |
| Flat Rocks TH | "Skeleton Loop" | - | Agency trail named SKELETON is 0770.F, about 13 km south (earlier draft). No source ties it to Flat Rocks. | NOT SUPPORTED |
| Flat Rocks CG (39.32749, -105.09220) | access to trails | - | Forest Service: "ATVs and off-road motorcycles are allowed to enter and depart the campground for trail access." Geometry: nearest trail is 0673 at 119 m; no trail endpoint within 150 m. Which trail and by what path is not stated. | SOURCE-BACKED that access exists; the specific trail UNKNOWN |
| **Sunset Point TH** (39.34808, -105.08571; capacity 90; no Forest Service web page - HTTP 404) | 0688 BEAVER | <50" | RRMMC: "Loading ramp, vault toilet, trailhead for trail 688 (Beaver Trail) (Sunset Point TH)". Geometry: 0688's west end is on NFSR 300, 71 m from the agency point. MVUM inset shows a trailhead symbol and "0688" there. | SOURCE-BACKED (partner) and DERIVED (71 m, across or along the road) |
| Sunset Point TH | 0627 BEGINNER | <50" | Geometry: passes 37 m away. | DERIVED-WEAK |
| Sunset Point TH | 0690 POWERLINE, 0787.A | <50" | Geometry: 0690 passes 107 m away; 0787.A ends 121 m away, 7 m from 0690. | DERIVED-WEAK |
| **Northern "Main Parking Lot"** (RRMMC mile 1.6, 39.36355, -105.08180, "Loading ramp") | - | - | No Forest Service page. Nearest agency records: MILE AND A HALF trailhead (39.36002, -105.07883, capacity 50), about 470 m from the partner coordinate, and RAMPART ENTRANCE trailhead (39.37716, -105.09412, capacity 135) at the Highway 67 end. **Which agency record is the partner's "Main Parking Lot" is UNKNOWN.** | UNKNOWN (identity) |
| Mile and a Half TH | 0690, 0627 | <50" | Geometry: 22 m and 32 m (two 0627 pieces end here). | DERIVED-STRONG that 0627 reaches it; no source sentence |
| Rampart Entrance TH | 0627, 0690, 0787 | <50" | Geometry: 0627 north end 111 m, 0690 north end 127 m (the piece with no motorcycle value), 0787 north end 194 m. | DERIVED-WEAK |
| **Garber Creek TH** (39.35813, -105.07872; capacity 55; restroom "No") | 0686 GARBER | <50" | Forest Service page: "The Garber Creek Trail (#686) enters into a system of 115 miles ..." Geometry: 0686's north end is 15 m from the point. RRMMC lists 686 trailheads at mile 1.8 and 3.3. | SOURCE-BACKED (agency) and DERIVED-STRONG |
| **Cabin Ridge TH** (39.28174, -105.10401; capacity 85; restroom "No") | 0675 CABIN RIDGE | <50" | Forest Service page: "Cabin Ridge Trailhead accesses Cabin Ridge Trail (#675)." Geometry: 0675 starts 18 m away; 0627 passes 1 m away. | SOURCE-BACKED (agency) and DERIVED-STRONG |
| Cabin Ridge Picnic Area (39.27961, -105.10585) | 0627, 0627.A | <50"; 0627.A unknown for motorcycles | Geometry only: 0627 passes 32 m from the picnic-site point; 0627.A starts 52 m away. The Forest Service page says the trailhead "is located southeast of the Cabin Ridge Picnic Area" (two separate sites, about 290 m apart by my calculation). | DERIVED-WEAK; no source says a rider may arrive at the picnic area by trail |
| Topaz Point Picnic Area | - | - | Outside the queried box; not examined. | UNKNOWN |

**Dutch Fred conflict (#679 vs #681): RESOLVED as "both true, two different trails".** Evidence: the Forest Service trails layer names 0679 DUTCH FRED and 0681 SCOTTYS as separate trails; the MVUM inset prints both labels at Dutch Fred; by Forest Service geometry 0681's south end and the 0679 line are 4 m apart and both within 11 m of the Forest Service trailhead coordinate. Neither source is in error; each names a different one of the two trails that meet at the lot. Residual oddity: the Forest Service road layer ends road 506 (0.2 mile) about 300 m short of the Forest Service trailhead coordinate, so either the coordinate or the mapped road end is imprecise. Which, UNKNOWN.

**Flat Rocks conflict (#674 agency vs #673 partner): EXPLAINED, not an error on the partner's side.** By Forest Service geometry the trail that begins at the trailhead is 0673 (BARR; the partner's "Bar Trail"); 0674 FLATROCK begins about 0.8 km away off 0673. The agency sentence ("enters into a system") is true as a description of what the trailhead leads to, but 0674 is not the trail you ride out of the lot on. The conflict is preserved because no agency sentence says so; this is DERIVED.

**Partner difficulty statements (PARTNER only):** Lightfoot's Loop "serves as an introduction to what Green rated trails at Rampart are like"; "even the trails rated as "easiest" can be quite challenging to new riders and small bikes"; the Sprucewood-side lot gives "access to some of the more difficult trails". Ratings live on the RRMMC printed map, which was not retrieved. The Forest Service area page describes the area as "From intermediate to expert riders".

---

## C. Forest orders - rule packet for the weekend

All order documents below were opened as PDFs or full order text from the forest's alerts pages (05:02-05:03 UTC 9 Oct). Township and range for each site were looked up from the Bureau of Land Management national PLSS service (`gis.blm.gov/.../BLM_Natl_PLSS_CadNSDI/MapServer/1`, 05:03 UTC): **Flat Rocks TH, Flat Rocks CG and Sunset Point TH are in T. 8 S., R. 69 W.; Dutch Fred TH, Cabin Ridge PA and Topaz Point PA are in T. 9 S., R. 69 W.** (6th Principal Meridian).

### C1. Order PSICC-2022-08 - camping and parking near listed roads

- Order number as printed: "ORDER # PSICC-2022-08" (the alerts list shortens it to "#2022-08"). **Earlier-reported number verified.**
- Effective: "in effect on July 20, 2022, at 12:01 am, and shall remain in effect until July 20, 2027, or until rescinded". Signed 19 July 2022. Replaces PSICC-2017-11.
- Prohibitions: "1. Camping within the Described Areas unless in a developed campground or a designated dispersed campsite provided by the Forest Service that is posted with signs. 36 C.F.R. 261.58(e)" and "2. Parking on the Described Roads or within the Described Areas unless in a developed campground or a designated parking site provided by the Forest Service that is posted with signs. 36 C.F.R. 261.58(g)".
- Scope: "The Described Roads are shown on Exhibit A and listed on Exhibit B. The Described Areas are all NFS lands within 1/4 mile of the centerline of the Described Roads, Highways and County Roads as shown on Exhibit A." Exhibit B (table PDF, text layer) lists, among others: 300 RAMPART RANGE, 300.M TOPAZ POINT PG, 300.R CABIN RIDGE PG, 300.S FLAT ROCKS OVERLOOK, 300.T FLAT ROCK CG, 300.U SUNSET POINT, 506 DUTCH FRED, 507, 502, 503, 563, CO-67.
- The MVUM repeats it and adds: "This Order only allows camping and/or parking in the Restricted Area where posted with these symbols" (parking / camping pictograms).
- Meaning for the trip: park the truck and trailer only in a signed designated parking site (trailhead lot, picnic area, campground); no pulling off along Rampart Range Road or Highway 67 to unload or picnic, and no camping outside a developed campground or a signed numbered site.
- Scope by site: Dutch Fred TH **YES** (road 506 listed; the agency point is about 300 m from the mapped road end and about 440 m from NFSR 300 - inside 1/4 mile of 506). Cabin Ridge PA **YES** (300.R). Flat Rocks TH **YES** (300, 300.T). Flat Rocks CG **YES** (300.T). Topaz Point PA **YES** (300.M). Sunset Point TH **YES** (300.U). Each of these is itself the kind of posted site the order exempts; whether each lot is actually "posted with signs" is a ground fact, UNKNOWN from here.
- Source: https://www.fs.usda.gov/sites/nfs/files/r02/psicc/publication/alerts/fseprd1060368.pdf and `.../Order%202022-08%20table.pdf`; CONTROLLING; static until 20 July 2027.

### C2. Order 02-12-00-23-07 - food storage

- Number verified. Effective "from June 6, 2023, at 12:01 am, through June 5, 2028, at 11:59 pm, unless rescinded". Signed 5 June 2023.
- Scope: "All NFS lands located on the Pike-San Isabel National Forests & Cimarron and Comanche National Grasslands, which includes the Pikes Peak, South Platte, South Park, Leadville, Salida and San Carlos Ranger Districts."
- Prohibition: "Possessing or leaving unattended any food ..., any refuse ..., or other bear attractants (such as bird feeders, cooking equipment, personal care products, and coolers), unless it is: a. Stored inside a hard-sided vehicle or camper. b. Stored inside a securable container or vehicle constructed of a solid, non-pliable material ... c. Suspended at least ten feet above the ground and four feet from any tree ... d. Being eaten, prepared for eating, or transported in a motor vehicle. 36 C.F.R. 261.58(cc)".
- Meaning: the picnic is fine while food is being eaten or prepared; coolers, stove and rubbish go into the closed cab or a hard-sided container whenever the family steps away - an open pickup bed is not obviously "hard-sided" storage (my reading, not stated).
- Scope by site: **YES for all five** (forest-wide).
- Source: https://www.fs.usda.gov/sites/nfs/files/r02/psicc/publication/alerts/fseprd1112291.pdf; CONTROLLING; static until 5 June 2028.

### C3. Order 02-12-00-24-04 - Pike National Forest occupancy and use (fires, stoves, camping)

- Number verified. Effective "from May 3, 2024 at 12:01 a.m. through December 1st, 2026, at 11:59 p.m., unless rescinded". Signed 3 May 2024. **Earlier-reported end date verified.**
- District-wide (all three Pike districts): "1. Camping at any location, within the same 20-mile radius for more than 14 days within any continuous 30-day period." "2. Camping within 100 feet of a body of water ... unless in a Forest Service developed recreation site or designated dispersed site."
- Only inside the "Described Areas" (Exhibits B-D maps, E-G tables): "3. Building, maintaining, attending or using a fire, campfire, or stove fire except in Forest Service developed recreation sites and designated dispersed campsites. 36 C.F.R. 261.52(a)"; "4. Camping, except in Forest Service developed recreation sites or designated dispersed sites."; "5. Going into or being in the Described Areas."; "6. Being in the Described Areas between sunset and sunrise, except a person who is camping or visiting a person camping ..."; "7. Parking or leaving a vehicle in violation of posted instructions."
- Exhibit F (South Platte table, "Revised 2/16/24"), the row that matters: "South Platte Ranger District in Douglas County - T. 7 S. R. 69 W; T. 8 S. R. 69 W; T. 8 S. R. 70 W; T. 9 S. R. 68 W. T. 9 S. R. 69 W. T. 9 S. R. 70 W; T. 10 S. R. 68 W; T. 10 S. R. 69 W and T. 10 S. R. 70 W - **#3 within the area**". Other rows: South Platte River Corridor (#3, #4, #6 within 1/4 mile of the river); The Chutes (#5); Sugar Creek Road (#3, #6 within 1/2 mile); "Dakan Road ... #3 and #6 within 1/2 mile of Dakan Road (NFSR 563)".
- Exhibit C (South Platte map, dated 3/18/2024, viewed as an image): a magenta "Described Areas (No Campfires)" polygon labelled "South Platte in Douglas County" covers the Rampart corridor; the map's own printed place labels FLAT ROCKS, DUTCH FRED, CABIN RIDGE, DEVILS HEAD and TOPAZ POINT sit inside it. The blue-striped "No Entry Sunset to Sunrise" strip follows Dakan Road, east of the corridor.
- **Scope by site for prohibition #3 (fire / stove):** Dutch Fred TH **YES** (T. 9 S., R. 69 W.); Cabin Ridge PA **YES** (T. 9 S., R. 69 W.); Flat Rocks TH **YES** (T. 8 S., R. 69 W.); Flat Rocks CG **YES** (T. 8 S., R. 69 W.); Topaz Point PA **YES** (T. 9 S., R. 69 W.); Sunset Point TH **YES** (T. 8 S., R. 69 W.). Basis: Exhibit F township list + BLM township lookup + Exhibit C map. The earlier draft's "not verified" is now verified.
- **Scope for #4, #5, #6:** Exhibit F applies only #3 to the Douglas County block. #6 applies within 1/2 mile of Dakan Road; all six sites are more than 3 km from NFSR 563 by my calculation, so **NO** for #6. #5: **NO**. (Designated-site-only camping in the corridor comes from Order PSICC-2022-08, not from this order's #4.)
- Meaning: a campfire, charcoal grill or **camp stove** may be used only inside a Forest Service developed recreation site or a designated dispersed campsite. The picnic areas and the campground are developed recreation sites with fire rings (Cabin Ridge page: "Fires only in established fire rings."). **Whether a trailhead parking lot counts as a "developed recreation site" for stove use is UNKNOWN** (the order does not define the term; 36 CFR 261.2 was not retrieved). Do not run a stove at a trailhead lot on the strength of this file.
- Sources: order https://www.fs.usda.gov/sites/nfs/files/r02/psicc/publication/alerts/fseprd1174599.pdf; Exhibit F `.../%28Exhibit%20F%29%20South%20Platte%20Ranger%20District%20Table.pdf`; Exhibit C `.../image/alerts/%28Exhibit%20C%29%20South%20Platte%20Ranger%20District%20Map.jpg`. CONTROLLING; static until 1 December 2026.
- Related, not a forest order: Douglas County Sheriff, "STAGE 1 FIRE RESTRICTIONS HAVE BEEN LIFTED FOR UNINCORPORATED DOUGLAS COUNTY, COLORADO", page stamp "updated on 9/17/2026" (https://www.dcsheriff.net/fire-restrictions/, read from raw page text 05:06 UTC; county; dynamic). No Stage 1 or Stage 2 forest fire-restriction order appears on the forest alerts list. The standing prohibition #3 applies regardless.

### C4. Dispersed camping in the corridor

- Rule source 1: Order PSICC-2022-08 prohibition 1 (C1) - CONTROLLING.
- Rule source 2: Forest Service area page (05:05 UTC): "Dispersed camping is available in designated sites only for a fee." "Park and camp in designated sites." "$22 fee for overnight camping in designated small campsites. $33 fee for overnight camping in designated large campsites." "No restrooms are in the dispersed camping areas." - OFFICIAL.
- 14-day limit and 100-foot water setback: Order 02-12-00-24-04 #1 and #2.
- Meaning: not relevant to a day trip unless plans change; if they do, only a signed numbered site or the campground.

### C5. Vehicle rules (summary; details in A)

- 36 CFR 261.13 + South Platte MVUM (CONTROLLING): ride only designated routes, in the designated class and season.
- Order 02-12-00-24-04 #7: "Parking or leaving a vehicle in violation of posted instructions." Exhibit F does not apply #7 to the Douglas County block by name; obey posted signs in any case.
- Area page (OFFICIAL): "Trailhead and OHV staging areas are open sunrise to sunset." "All OHVs must be registered."
- Mud-season closure order (1 April - 31 May, per the area page) and the December road closure: not in effect on 10-11 October. The mud-season order document itself was not found on the alerts list - NOT RETRIEVED, not needed for October.
- Order 02-12-09-22-18 "Rampart Range Road 300 Winter Closure": Pikes Peak Ranger District, 1 December - 1 April; not this district, not this month.

### C6. Temporary and prescribed-fire closures on 10-11 October

- **Harris Park RX area and road closure, Order 02-12-11-26-41** (order text read on the alert page, 05:03 UTC): "in effect from October 6, 2026 at 10:00 am through October 10, 2026 at 11:59 pm"; "The Described Area is north of Harris Park, Park County, Colorado, in Sections 11, 12, 13, and 14 of Township 6 South, Range 73 West ... and Sections 7, 17, 18, 19, and 20 of Township 6 South, Range 72 West"; roads "NFSR 108, 108.A, 108.B, and 107". Scope for all five sites: **NO** (different townships, different county). Still active on the Saturday elsewhere in the district. CONTROLLING; dynamic.
- **Prescribed fire notice** (alert, "Last updated October 8, 2026"; not an order): "The Rampart Reservoir Area prescribed fire, located approximately three miles east of Woodland Park, is planned for Oct. 8-9. Smoke production could last a couple of days ..." and "The O'Brien prescribed fire, three miles west of Lake George in Park County, is planned for Oct. 9." **Changed since the earlier draft, which recorded "Oct. 8" only.** Neither is in the northern corridor; no closure of the northern corridor is stated. Smoke is possible. OFFICIAL; dynamic.
- No order found closing any part of the northern Rampart corridor for 10-11 October. Scope for all five sites: **NO known temporary closure**; this is a statement about the alerts list at 05:02 UTC, not about signs on the ground.
- Recreation.gov lead from the earlier draft (an order "in effect from August 21, 2026 ... through ... November 14, 2026" seen only in a search snippet): the Recreation.gov public alert endpoint returned `{"alerts":[]}` for Flat Rocks Campground (10165295), for the dispersed-camping facility (10132201) and for the parent recreation area at 05:06 UTC, and one targeted web search found no such order. **Still UNVERIFIED and now less likely to concern Flat Rocks; not disproved.**

### C7. Site-specific rules found

- Cabin Ridge Picnic Area: "Overnight use prohibited. Fires only in established fire rings. Pack it in; pack it out." (earlier draft; OFFICIAL). Cabin Ridge Trailhead page: "Dogs must be leashed at all times".
- Flat Rocks Campground and area page: "Dogs must be on a leash at all times." (earlier draft).
- No order document specific to any single one of the five sites was found.

---

## Agreement and disagreement with earlier drafts

Agree:
- MVUM table rows and dates: full agreement with the earlier image reading (A3).
- Order numbers and dates: PSICC-2022-08 (to 20 July 2027), 02-12-00-23-07 (to 5 June 2028), 02-12-00-24-04 (to 1 December 2026), 02-12-11-26-41 (Harris Park, to 10 October 23:59) - all verified against the order documents.
- The agency layer's "12/01-03/14" motorcycle values and the conclusion that the published map controls.
- Unplated bike not legal on NFSR 300; Dutch Fred restroom "No" in both agency records; no agency difficulty ratings; "Skeleton Loop at Flat Rocks" unsupported.

Disagree or correct:
1. "The PDFs have no extractable text layer" - **not correct for the legend, definitions, blanket statements and route labels**, which extract as text with PyMuPDF. Only the seasonal table is graphics.
2. "It does not define 'Special Vehicle Designation' in words I could read" - the map **does** define it (quoted in A2), but the definition defers to the table and the table adds nothing, so the practical point (the map does not name the classes) stands.
3. "0690 ... `motorcycle` null ... not in table ... [U]" - the earlier draft picked up only the 0.39-mile northern piece. The main 6.8 miles are a year-round <50-inch trail in the layer and are drawn without a seasonal symbol on the map. Resolved.
4. "Designation of 679 itself: [U] (PDF map line-type not read)" - line type now read: <50-inch trail with seasonal halo, absent from the table.
5. Fire/stove order scope "not verified" - now verified YES for all six sites by township lookup and Exhibit C.
6. Prescribed fire date is now "Oct. 8-9" plus a second burn (O'Brien, 9 October).
7. `rampart-evidence-closure.md` said the map inset shows motorized-trailhead symbols supporting "trails 0681 and 0767.A start in that vicinity" - agreed, and now quantified: 0681 ends 10 m from the agency trailhead point; the 0767.A loop is roughly 450-520 m north of that point beside NFSR 300.
8. `rampart-relationships.md` endpoint candidates for Flat Rocks (0770.A, 0682, 0673) and Dutch Fred (0681; 0679 at 109 m) are reproduced from the MVUM layer geometry (35, 38, 51 m; 10 m; 107 m). New: the first 0.17 mile of 0770.A is ATV-only in the agency data.

## Conflicts preserved

1. **Trail season, published map vs agency layer**: map "May 16 - March 14" vs layer motorcycle "12/01-03/14" for about 30 numbered trails. Map is the controlling instrument; layer is OFFICIAL but says it is not a legal document. Unresolved as to cause.
2. **0767 / 0767.A (Upper Dutch, Lightfoot Loop)**: MVUM table "Trail Open to All Vehicles, May 16 - November 30"; MVUM layer agrees (motorcycle 05/16-11/30); the Forest Service trails dataset says `allowed_terra_use` "321" (no motorcycle, no ATV) and motorcycle "restricted" 01/01-12/31; partner calls it a beginner motorcycle loop. Map controls; the third dataset contradicts it.
3. **0679 Dutch Fred Trail**: drawn seasonal on the map, missing from the map's table; layer says 06/01-11/30.
4. **Spur roads 506 and 300.T**: table says "Road, Special Vehicle Designation"; the same map's line work and the agency layer say "Roads open to all vehicles"; the Forest Service campground page says off-road motorcycles may enter and leave the campground; the layer's own dates for 300.T contradict its own symbol. The partner's list of roads open to unplated vehicles omits both.
5. **0770.A first 0.17 mile at Flat Rocks TH**: map draws a motorcycles-only line from the trailhead symbol; layer says ATV-only special designation.
6. **Flat Rocks trail number**: agency page #674; partner #673; agency geometry puts 0673 at the lot and 0674 0.8 km away.
7. **Dutch Fred trail number**: agency #679; partner #681 - both exist at the lot (resolved as two trails; kept here because no single source says so).
8. **Dutch Fred trailhead position**: agency coordinate is about 300 m beyond the mapped end of road 506.
9. **Road jurisdiction**: partner "Rampart Range Road is a county road"; agency data `jurisdiction` "FS - FOREST SERVICE".
10. **Dutch Fred restroom**: agency "No"; partner "Vault toilets" (not re-researched; another worker has facilities).
11. **MVUM edition**: "superseded by the next year's MVUM" vs "validated ... with a red stamp" vs a 2025-dated, unstamped PDF being the only one published in October 2026.
12. **Area mileage**: Forest Service "115 miles"; partner "nearly 200 miles" (carried from the earlier draft).

## Unknowns

- Whether the 2025 South Platte MVUM has been validated for 2026.
- Legal season of 0679 on the controlling map; motorcycle legality of 0627.A, 0681.D, 0681.F, the first 0.17 mile of 0770.A and the last 0.39 mile of 0690.
- Whether an unplated bike may use spur roads 506, 300.T, 300.U.
- Exact road-crossing points for 0627 / 0690 and whether each is signed.
- Which agency record corresponds to the partner's "Main Parking Lot" at mile 1.6.
- Legal status of the "Kiddy Corral" and the Flat Rocks "kiddy track" as designated riding areas (not on the MVUM as areas; the map's text mentions designated "areas" generally but I saw none drawn here).
- Whether a trailhead lot is a "developed recreation site" for the stove rule.
- Whether each lot is actually posted as a designated parking site.
- Any trail-to-picnic-area arrival for the rider at Cabin Ridge or Topaz Point; Topaz Point trail relationships not examined at all.
- Whether Colorado requires a driver's licence or safety certificate for off-road riding by the rider (not researched; relevant if the rider is a minor).
- CURRENT PHYSICAL CONDITION of every trail and of NFSR 300: not established by any agency source; partner banner undated.
- The Recreation.gov "August 21 - November 14, 2026" order lead.
- NOT RETRIEVED: Colorado Parks and Wildlife sound-law page (HTTP 404); official Colorado statute host (statutes read on colorado.public.law); 36 CFR 261.2 definitions; Forest Service pages for Sunset Point and Rampart Entrance trailheads (HTTP 404 on guessed addresses); the mud-season order; RRMMC printed map with trail ratings; Avenza and interactive MVUM viewers (not attempted).

## Sources

All retrieved 2026-10-09 UTC.

| # | URL | Publisher | Retrieved | Strength | Static/dynamic |
|---|---|---|---|---|---|
| 1 | https://www.fs.usda.gov/sites/nfs/files/r02/psicc/publication/SPLTMVUMFINALFRONT07302025.pdf (via /media/262850) | USDA Forest Service | 04:57 | CONTROLLING | static (annual) |
| 2 | https://www.fs.usda.gov/sites/nfs/files/r02/psicc/publication/SPLTMVUMFINALBACK07302025.pdf | USDA Forest Service | 04:57 | CONTROLLING | static (annual) |
| 3 | https://apps.fs.usda.gov/arcx/rest/services/EDW/EDW_MVUM_02/MapServer (root; layer 2 description; layer 1 and 2 queries for the box) | USDA Forest Service, Enterprise Data Warehouse | 04:59 | OFFICIAL (not a legal document) | dynamic |
| 4 | https://apps.fs.usda.gov/arcx/rest/services/EDW/EDW_TrailNFSPublish_01/MapServer/0 (box query) | same | 04:59 | OFFICIAL | dynamic |
| 5 | https://apps.fs.usda.gov/arcx/rest/services/EDW/EDW_RecInfraRecreationSites_02/MapServer/0 (box query) | same | 04:59 | OFFICIAL | dynamic |
| 6 | https://apps.fs.usda.gov/arcx/rest/services/EDW/EDW_RoadBasic_01/MapServer/0 (small box at Dutch Fred) | same | 05:06 | OFFICIAL | dynamic |
| 7 | https://www.fs.usda.gov/r02/psicc/alerts | USDA Forest Service | 05:02 | OFFICIAL | dynamic |
| 8 | https://www.fs.usda.gov/r02/psicc/alerts/occupancy-and-use-restrictions-designated-camping-and-parking-areas ; order PDF `.../publication/alerts/fseprd1060368.pdf` ; `.../publication/alerts/Order%202022-08%20table.pdf` | USDA Forest Service | 05:02 | CONTROLLING | static |
| 9 | https://www.fs.usda.gov/r02/psicc/alerts/food-storage-prohibitions-pike-san-isabel-national-forests ; `.../publication/alerts/fseprd1112291.pdf` | USDA Forest Service | 05:02 | CONTROLLING | static |
| 10 | https://www.fs.usda.gov/r02/psicc/alerts/pike-national-forest-occupancy-and-use-restrictions ; `.../publication/alerts/fseprd1174599.pdf` ; Exhibit F table PDF ; Exhibit C map JPG | USDA Forest Service | 05:02-05:03 | CONTROLLING | static |
| 11 | https://www.fs.usda.gov/r02/psicc/alerts/harris-park-rx-area-and-road-closure | USDA Forest Service | 05:03 | CONTROLLING | dynamic |
| 12 | https://www.fs.usda.gov/r02/psicc/alerts/prescribed-fire-planned-psicc | USDA Forest Service | 05:03 | OFFICIAL | dynamic |
| 13 | https://gis.blm.gov/arcgis/rest/services/Cadastral/BLM_Natl_PLSS_CadNSDI/MapServer/1 (six point queries) | Bureau of Land Management | 05:03 | OFFICIAL | static |
| 14 | https://www.fs.usda.gov/r02/psicc/recreation/dutch-fred-trailhead (updated May 28, 2026) ; /flat-rocks-trailhead (Feb 18, 2025) ; /cabin-ridge-trailhead (Feb 18, 2025) ; /garber-creek-trailhead (Feb 18, 2025) | USDA Forest Service | 05:04 | OFFICIAL | static |
| 15 | https://www.fs.usda.gov/r02/psicc/recreation/sunset-point-trailhead ; /rampart-entrance-trailhead - HTTP 404, NOT RETRIEVED (guessed addresses) | USDA Forest Service | 05:04 | - | - |
| 16 | https://www.fs.usda.gov/r02/psicc/maps-guides/motor-vehicle-use-maps (updated March 30, 2026) ; https://www.fs.usda.gov/r02/psicc/recreation/rampart-range-recreation-area | USDA Forest Service | 05:05 | OFFICIAL | static |
| 17 | https://www.ecfr.gov/api/renderer/v1/content/enhanced/current/title-36 - sections 261.13, 261.15, 212.51, 212.1 (first four attempts without redirect-following returned HTTP 302) | Office of the Federal Register / GPO, eCFR | 05:05 | CONTROLLING | static |
| 18 | https://cpw.state.co.us/register-off-highway-vehicle ; https://cpw.state.co.us/activities/off-highway-vehicles-and-snowmobiles | Colorado Parks and Wildlife | 05:05 | OFFICIAL (state) | static |
| 19 | https://cpw.state.co.us/thingstodo/Pages/OHVsSoundLaw.aspx - HTTP 404, NOT RETRIEVED | Colorado Parks and Wildlife | 05:05 | - | - |
| 20 | https://colorado.public.law/statutes/crs_25-12-110 ; crs_33-14.5-108 ; crs_33-14.5-109 ("Current through Fall 2025") | Public.Law (secondary host of Colorado Revised Statutes; not the official publisher) | 05:05 | CONTROLLING text, secondary host | static |
| 21 | https://www.dcsheriff.net/fire-restrictions/ ("updated on 9/17/2026") | Douglas County Sheriff's Office | 05:06 | county | dynamic |
| 22 | https://www.recreation.gov/api/camps/campgrounds/10165295 ; https://www.recreation.gov/api/communication/external/alert (three location queries, all empty) | Recreation.gov | 05:06 | OFFICIAL | dynamic |
| 23 | https://rampartrange.org/ ; /parking-areas/ ; /directions/ ; /frequently-asked-questions/ ; /sound-limits/ ; /trail-info/ | RRMMC (volunteer partner, not an agency) | 05:04 | PARTNER | mixed; status banner dynamic and undated |

Web searches (3), used only as leads: Colorado OHV sound limit and statute; the "August 21 - November 14, 2026" order lead; October 2026 Rampart closures. No snippet is quoted as evidence.
