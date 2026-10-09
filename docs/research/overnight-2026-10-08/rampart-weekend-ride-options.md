DRAFT - UNREVIEWED RESEARCH

# Rampart Range north end, 10-11 October 2026: ride options from two lots, Cabin Ridge Trailhead record, fire-restriction conflict, Topaz Point

- Prepared by Hermes (research plane). All retrievals 2026-10-09 UTC, 05:13 to about 05:21 (= evening of Thu 8 Oct, Mountain time). Times in the Sources table are from `date -u` on the research machine.
- Closes four gaps left by `rampart-weekend-legality-links-orders.md`, `rampart-weekend-facilities.md`, `rampart-weekend-route-and-conditions.md` (same folder). Those files are not redone; facts carried from them are marked CARRIED.
- Strength labels: **controlling** (regulation, signed order, the published Motor Vehicle Use Map, MVUM) / **official** (Forest Service page) / **agency data** (Forest Service GIS layer; the layer says it is not the legal instrument) / **partner** (Rampart Range Motorcycle Management Committee, RRMMC, a volunteer partner, not an agency) / **derived** (my own geometry or reasoning) / **lead** (search snippet, news, third party; never used as a fact).
- LEGAL DESIGNATION is not CURRENT CONDITION. Nothing here says any trail is passable, signed, dry, or clear of fallen trees. Unknown stays unknown.
- Budget: 5 web searches (limit 10); 36 page or service retrievals (limit 40, counting 3 failures: one GIS query HTTP 400, one Forest Service page 404, one news feed 401). No identical query repeated. Nobody contacted, no login. Scratch files are in the Hermes scratch directory, not in the repository. Only this file and CHECKPOINT.md were written.

## Headline findings

1. Every trail in the rides below is in the MVUM table (controlling) as open to motorcycles on 10-11 October, with ONE exception: **0679 Dutch Fred Trail is not in the table** (the map draws it as a seasonal trail under 50 inches wide; agency data says 1 June - 30 November). Rides that use 0679 are marked.
2. **Cabin Ridge Trailhead to Dutch Fred is a trail-only link by agency geometry (derived): 0627 south, 0679.A, 0679, about 2.5 miles one way.** It passes two avoid-list junctions (0627.A) and runs within 10 m of the Devil's Head spur road for about 110 m.
3. Cabin Ridge Trailhead: 85 "capacity" (unit undefined), no restroom, no water, no fee, "Year-round", no surface, trailer or hours field. It is on the road itself, 6 m from NFSR 300. The Forest Service never says it is a signed parking site (Order PSICC-2022-08 needs "posted with signs"). A pickup with a trailer: **no source says**.
4. **Fire restriction: UNRESOLVED on paper, probably lifted.** No Forest Service rescission document was found. Indirect Forest Service evidence plus one newspaper report point to a lift on 17 September. Plan to the stricter reading, which costs nothing at a Forest Service fire ring or with a gas stove (Gap 3).
5. Topaz Point: no trailhead at the picnic area. Nearest agency trailhead record is Devil's Head TH, about 2.7 miles by road. Topaz Point page says "Site Open" (page last updated 18 Feb 2025).

---

## Gap 1 - Ride options from Cabin Ridge Trailhead and from Dutch Fred

### 1.1 Method (so a reviewer can repeat it)

- Forest Service EDW MVUM feature service `EDW_MVUM_02`, layer 2 (trails) and layer 1 (roads), queried by bounding box, all fields, with geometry: box lon -105.125..-105.07, lat 39.245..39.30 (21 trail records, 10 road records), plus two small boxes north of Dutch Fred and west of Cabin Ridge (lon -105.085..-105.045 / lat 39.305..39.335; lon -105.14..-105.115 / lat 39.31..39.335) and one near Topaz Point. Forest Service National Forest System Trails layer `EDW_TrailNFSPublish_01` layer 0, same first box (25 records). Retrieved 05:13 to 05:16 UTC. Strength: agency data.
- Connection ("what it joins") = an endpoint of one trail within 20 m of another trail's mapped line, from those layers. DERIVED. Geometry is not a legal connection and says nothing about gates, signs, direction or condition.
- Ride miles = lengths of the mapped lines, summed along the stated sequence (my calculation, local planar approximation; expect a few percent error). They are not the agency `GIS_MILES` figures, which are shown separately.
- Road touch = mapped trail line within 15 m of a mapped road line (NFSR 300, 506, 300.O, 300.R, 502), or a true line crossing. DERIVED. Offsets under about 10 m may be digitising error; I report them, I do not interpret them.
- Avoid-list (from the earlier drafts): 0627.A, 0681.D, 0681.F, first 0.17 mile of 0770.A, northernmost 0.39 mile of 0690. No ride below uses any of them. 0681.D was not returned in any box queried (location unknown).
- Agency-stated difficulty: **none.** Neither the MVUM layer nor the National Forest System Trails layer has a difficulty field (full field lists read). `TRAIL_CLASS` is a construction standard (TC3 "developed", TC4 "highly developed", TC5 "fully developed" as printed in the MVUM layer), not a difficulty rating. The Forest Service trail pages for these lots give no trail ratings.

### 1.2 Trail facts (agency data and MVUM)

Dates in question: 10-11 October 2026. "Layer" = MVUM layer 2 motorcycle dates, known to disagree with the map for about 30 trails (carried conflict). "Table" = Seasonal and Special Vehicle Designations table on the MVUM, as read twice in the earlier draft (image reading; not machine text).

| Trail | Agency name (NFS trails layer) | GIS_MILES MVUM layer / NFS layer (mile post) | MVUM table class and season (controlling) | Layer symbol; motorcycle dates (agency data) | TRAIL_CLASS | Typical tread / grade / surface (NFS layer, coded) |
|---|---|---|---|---|---|---|
| 0675 | CABIN RIDGE | 4.843 / 4.843 (0-4.76) | Trail <50", May 16 - Mar 14 | "Trails open to vehicles 50" or less in width, Seasonal"; 12/01-03/14 | TC3 | 18-24 in; +12-20%; native |
| 0627 | BEGINNER | 9.218 / 8.927 (0.287-9.75 in NFS layer; MVUM layer mapped in two pieces, 1.31 mi + 7.70 mi) | Trail <50", May 16 - Mar 14 | same symbol; 12/01-03/14 | TC3 | 18-24 in; +5-8%; native |
| 0627.A (AVOID) | QUARRY CUT-OFF | 0.395 | not in table | "Special Designation, Yearlong"; ATV only, motorcycle empty | TC3 | grade 0-5%; native |
| 0657 | GRAMPS | 2.762 / 2.763 | Trail <50", May 16 - Mar 14 | <50" Seasonal; 12/01-03/14 | TC3 | 18-24 in; +12-20%; native |
| 0680 | LOOP | 0.472 | Trail <50", May 16 - Mar 14 | <50" Seasonal; 12/01-03/14 | TC3 | 18-24 in; +12-20%; native |
| 0679 | DUTCH FRED | 4.482 | **no row** (map draws it <50" seasonal; table silent) | <50" Seasonal; **06/01-11/30** | TC3 | 18-24 in; +12-20%; native |
| 0679.A | DEVILS HEAD SPUR | 1.056 | Trail <50", May 16 - Mar 14 | <50" Seasonal; 12/01-03/14 | TC3 | 18-24 in; +5-8%; native |
| 0679.B | TORNADO ALLEY | 3.471 | Trail <50", May 16 - Mar 14 | "Trails open to motorcycles, Yearlong"; 01/01-12/31 (ATV "restricted") | TC3 | +5-8%; native |
| 0681 | SCOTTYS | 4.30 / 4.30 | Trail <50", May 16 - Mar 14 | <50" Seasonal; 12/01-03/14 | TC3 | 18-24 in; +12-20%; native |
| 0681.B, .C, .E | (not retrieved), (not retrieved), "681.E" | 0.077, 0.059, 0.062 | Trail <50", May 16 - Mar 14 | <50" Seasonal; 12/01-03/14 | TC3 | .E: 0-5% |
| 0681.F (AVOID) | (not retrieved) | 0.158 | not in table | Special Designation, ATV; no motorcycle value | TC3 | - |
| 0685 | (not retrieved) | 3.187 | Trail <50", May 16 - Mar 14 | <50" Seasonal; 12/01-03/14 | TC3 | - |
| 0767 | UPPER DUTCH | 0.178 / 0.187 | "Trail Open to All Vehicles", May 16 - Nov 30 | "Trails open to all vehicles, Seasonal"; 05/16-11/30 | TC5 | grade 0-5%; native |
| 0767.A | LIGHTFOOT LOOP | 0.564 / 0.57 | same as 0767 | same; 05/16-11/30 | TC5 | grade 0-5%; native |
| 0770 | TURTLE MOUNTAIN | 41.282 | "Trail Open to Motorcycles only", May 16 - Mar 14 | motorcycles, Seasonal; 12/01-03/14 | TC4 | +5-8%; native |
| 0770.C, 0770.D | DEVILS ADVOCATE, DEVILS REVENGE | 1.892, 9.492 | not in table (A8 of earlier draft) | motorcycles, Yearlong; 01/01-12/31 | TC3 | +5-8%; native |
| 0690 | POWERLINE | 6.998 (mile 2.29-9.07) | drawn <50", no seasonal symbol (earlier draft) | <50" Yearlong; 01/01-12/31 | TC3 | 18-24 in; +12-20%; native |
| 0674, 0653 | FLATROCK (NFS layer); 653 name not retrieved | 3.665, 1.029 | Trail <50" (0674 and 0653 are in the table row), May 16 - Mar 14 | <50" Seasonal; 12/01-03/14 | TC4, TC3 | - |

Notes:
- All of 0675, 0627, 0657, 0680, 0679.A, 0681, 0685 are legally open to motorcycles on 10-11 October **per the controlling table** (May 16 - March 14). Strength: controlling for the date window; image-read table.
- 0767/0767.A: table and MVUM layer agree (all vehicles, 16 May - 30 Nov). The NFS trails layer disagrees (`allowed_terra_use` 321, motorcycle restricted 01/01-12/31, ATV restricted). Carried conflict; the map controls.
- 0679.B: table says <50" May 16 - Mar 14; both agency layers say motorcycles-only year-round with ATVs restricted. Both admit a motorcycle on the dates; the class differs.
- The coded tread, width and grade values are identical across many trails (TG05/TW03 on eight of them). DERIVED observation: they may be default entries, not surveyed values. Treat them as weak.

### 1.3 What each trail joins (from agency geometry, DERIVED)

Positions are miles along the named trail's mapped line from its mapped start; "DF end" is the Dutch Fred end of 0681.

| Trail | One end | Along it | Other end |
|---|---|---|---|
| 0675 (4.74 mi mapped) | Starts on 0627 at 0627 mile 6.87, 19 m from Cabin Ridge Trailhead point, 10 m from NFSR 300 | 0657, 0770.C, 0770.D and 0770 meet at 1.36; 0653 at 4.07; 0674 at 4.24 | 39.32222, -105.12749: no trail within 40 m (0677 start is 139 m away). Dead end in the data |
| 0627 (south piece, 7.70 mi) | North end 39.35979, -105.07905 on 0690 | 0657 start at 5.81; 0680 start 24 m off at 6.02; 0690 start 99 m off at 6.01; 0675 start at 6.87 (Cabin Ridge TH 1 m away at 6.88); 0627.A (AVOID) start at 7.13; picnic-area point 30 m off at 7.11 | South end 39.27426, -105.10467, 4 m from 0679.A at 0.03 mi along 0679.A |
| 0657 (2.70 mi) | NE end on 0627 (5.81 on 0627); 0690 starts on it at 0.22 | 0770 meets at 0.36-0.37; 0680 end at 0.96 | SW end at the 0675 / 0770.C / 0770.D junction (1.36 on 0675) |
| 0680 (0.46 mi) | Starts at the NFSR 300 / NFSR 506 junction (0 m from road 300) | - | Ends on 0657 at 0.96 |
| 0679.A (1.07 mi) | Starts on spur road 300.O (Devil's Head TH/CG) 0.17 mi from 300.O's start | 0627 south end at 0.03; 0627.A (AVOID) end at 0.17 | Ends on 0679 at 0.71 |
| 0679 (4.43 mi) | Starts 39.28669, -105.0922, 192 m from the end of road 506 and 106 m from the Dutch Fred point; no trail meets the start | 0681 south end at 0.07 (Dutch Fred point 12 m away, at 0.065); 0679.A at 0.71 | 39.26876, -105.07777, ON NFSR 502 (Jackson Creek South, a road). 0679.B starts on 502 about 0.16 mi along the road from there |
| 0681 (4.26 mi) | South end at Dutch Fred (2 m from the agency point); 4 m from 0679 | from DF end: 0681.B 0.43; 0767 meets at 0.33; 0681.F (AVOID) both ends at 0.77 and 1.00; 0681.C 1.84; 0681.E 3.28 | North end 39.31542, -105.0658 meets 0685 start (3 m) |
| 0767 Upper Dutch (0.18 mi) | Starts ON NFSR 300 (0 m) | touches 0681 at 767 mile 0.149 (0 m); 0767.A starts on it at 0.036 | 39.28987, -105.09193 (34 m from 0681) |
| 0767.A Lightfoot Loop (0.57 mi) | Starts on 0767 at 0.036 (52 m from road 300) | stays 37-327 m from road 300 | End 33 m from 0767 at 0.039 (a 33 m gap in the loop closure in the data) |
| 0690 (6.76 mi) | South start 39.2918, -105.0945, on 0657 at 0.22 | - | North end 39.37252, -105.09353 (last 0.39 mi AVOID) |

Not in the data (so unknown): where the Kiddy Corral is (RRMMC only); how the 0627 mapped gap of 409 m between its two pieces is bridged (both pieces end on 0690, 0.26 mi apart along it).

### 1.4 Derived rides

**DERIVED from Forest Service geometry and the MVUM table. Not a statement of current condition, signing, gates, direction of travel or legality of any junction on the ground. A rider needs the MVUM and the signs; obey posted arrows.**

Road facts used below: NFSR 300 and the spurs are closed to an unplated bike (earlier draft, high confidence: plated bike and licence needed). Colorado law has an exception for "crossing" roads: C.R.S. 33-14.5-108(1) "When crossing streets or when crossing roads, highways, or railroad tracks" (secondary host text read in the earlier draft). **No Forest Service page, order or the MVUM text layer says anything about designated trail crossings of NFSR 300**; I searched the MVUM text layer for "cross" and found only water-crossing and place-name hits. So every crossing or touch below is: **signed or designated crossing UNKNOWN.**

#### From Cabin Ridge Trailhead (39.28174, -105.10401)

Starting fact for all three: the trailhead point is 6 m from NFSR 300 and 1 m from 0627; 0675 starts 19 m away on 0627. By the layer, **0627 crosses NFSR 300 at 39.28189, -105.10411 (19 m from the lot point)**, which is also where 0675 begins. Whether the rider rolls from the lot onto the trail without touching the road is UNKNOWN. This single crossing is the only line crossing of a road in any ride from this lot.

| # | Ride | Sequence | Miles | Road touches (derived) |
|---|---|---|---|---|
| CR-1 | Short out-and-back | Lot, 0675 west to the 0657 / 0770.C / 0770.D junction, return | 1.36 each way = 2.73 | 0675 is never within 10 m of a road except its first ~2 m; within 25 m for 18 m of 7,634 m. Lot crossing only |
| CR-2 | Gramps loop | Lot, 0675 west 1.36, 0657 northeast 2.70 to its end on 0627, 0627 south 1.06 back to the lot | 5.12 | 0657: no road within 25 m. 0627 final 1.06 mi: parallels NFSR 300 (376 m of its 1,706 m is within 10 m of the road; 1,390 m within 25 m; never closer than 3 m until the lot crossing). 0680's far end (on the NFSR 300 / 506 junction) and 0690's start sit 24-99 m from the 0627 / 0657 meeting; do not take 0680. 0657 passes the 0770 junction at 0.36 and 0690's start at 0.22: stay on 0657 |
| CR-3 | Link to Dutch Fred and back | Lot, 0627 south 0.82, 0679.A 1.03, 0679 0.64 to the Dutch Fred lot, return | 2.50 each way = 5.0 | Going south from the lot the rider passes the start of 0627.A (AVOID) at 0627 mile 7.13, 0.26 mi from the lot. 0627.A's other end meets 0679.A at 0679.A mile 0.17; the 0627 / 0679.A junction is at 0679.A mile 0.03, 0.14 mi nearer the Devil's Head spur: it is the second junction, not the first. 0627 runs within 15 m of spur road 300.O for about 110 m (mile 7.575-7.643); 0679.A starts on 300.O. No line crossing. Uses 0679 for 0.64 mi: **0679 is not in the MVUM table; season UNKNOWN on the controlling map; agency data says open to motorcycles 1 June - 30 November** |

Optional extension of CR-2, not recommended on this evidence: 0675 on to 0674 (junction at 4.24 mi) heads toward Flat Rocks, 4.24 mi from the lot, beyond the 5 km reach asked for.

#### From Dutch Fred Trailhead (39.28573, -105.09196)

Starting fact: the agency point is 2 m from the south end of 0681 and 12 m from 0679. Road 506 ends 299 m from the point and 192 m from the start of 0679; no mapped trail covers that gap (cause unknown: coordinate error or unmapped track). A rider unloading at the lot does not need road 506 to reach 0681 or 0679.

| # | Ride | Sequence | Miles | Road touches (derived) |
|---|---|---|---|---|
| DF-1 | Scotty's out-and-back | Lot, 0681 north to the 0685 junction, return (turn back anywhere) | 4.25 each way = 8.51 | None. 0681 never comes within 25 m of any mapped road. Spur junctions along the way: 0681.B (0.43), 0767 (0.33), 0681.F AVOID (0.77 and 1.00, a bypass whose both ends are on 0681: stay on the main line), 0681.C (1.84), 0681.E (3.28) |
| DF-2 | Lightfoot short ride | Lot, 0681 north 0.33, 0767 north 0.11 to the 0767.A junction (767 mile 0.149 to 0.036), 0767.A loop 0.57, return | about 1.46 | No road touch if the rider turns onto 0767.A at 767 mile 0.036 (about 58 m of trail short of NFSR 300, where 0767 starts). 767.A is 37-327 m from the road. **Direction unknown: RRMMC calls it "a designated one-way trail" but no source in this session gives the direction. Follow the posted arrow.** Table and layer say motorcycles allowed; the NFS trails layer says restricted (conflict) |
| DF-3 | Lollipop: Dutch Fred - Cabin Ridge - Gramps | Lot, 0679 0.64, 0679.A 1.03, 0627 north 0.82 to the Cabin Ridge lot, then the CR-2 loop (0675, 0657, 0627) 5.12, return the same way | 10.12 | Everything in CR-3 and CR-2, including the one NFSR 300 crossing at the Cabin Ridge lot (passed twice) and the 0627.A (AVOID) junction. Uses 0679 (not in the table) for 0.64 mi each way |
| DF-alt | 0679 out-and-back | Lot, 0679 southeast to its end | 4.37 each way = 8.73 | The far end lies ON NFSR 502 (Jackson Creek South, a high-clearance road, closed to an unplated bike); turn back before it. 0679.B starts on that road 0.16 mi from the end: not reachable on trail. All of 0679 is subject to the missing-table-row problem |

### 1.5 What the partner (RRMMC) says about these trails

All partner statements. None is an agency rating. The RRMMC printed map carries beginner / intermediate / expert marks per segment but was not retrieved (NOT RETRIEVED).

- Lightfoot Loop (0767.A, 0767): "The Lightfoot Loop is a designated one-way trail. It's a beginner trail with a sampling of some of the terrain found at Rampart and is ideal for those that are new to the sport or just new to the area. The trail can be found at the Dutch Fred parking lot." and "a slightly more challenging trail loop that runs about 1 mile and is the only trail at Rampart that is one-way directional. It serves as an introduction to what Green rated trails at Rampart are like." (https://rampartrange.org/frequently-asked-questions/, 05:17 UTC.) Conflicts: "about 1 mile" vs mapped 0.57 mi (+0.18 on 0767); "at the Dutch Fred parking lot" vs geometry 0.33 mi up 0681 (about 460 m straight from the agency point).
- Beginners and kids: "The best is probably the Dutch Fred camping area ... two new beginner areas were added. One is the 'Kiddy Corral', which is basically a fenced oval loop". "Note that even the trails rated as 'easiest' can be quite challenging to new riders and small bikes." (same page). The Kiddy Corral is not in agency data (unknown legal status).
- 0627 and 0690: "The Powerline (#690) and beginner trails (#627) parallel the road most of the way and can be used to get from one area to another if your bike is not licensed." (https://rampartrange.org/directions/, 05:17 UTC; the last clause was read in the earlier draft.) The geometry agrees that 0627 runs alongside NFSR 300 (see CR-2).
- Parking list (https://rampartrange.org/parking-areas/, 05:16 UTC): "8.1 RRPARK40 Trail head for trail 675 (Cabin Ridge Trail)" at N39 16.898 W105 6.236 (= 39.28163, -105.10393, 14 m from the agency point); "7.1 RRPARK37 Trail head for trail 657 (Gramps Trail) (Gramps TH)" at 39.29355, -105.09205 (matches the 0657 start); "7.3 DUTFRDCG Dutch Fred campground and Dutch Fred Gulch. Vault toilets, Kiddy Corral, Lightfoot's Loop, trailhead for trail 681 (Scotty's Trail)".
- Partner-hosted reprint "Rampart Range by Dirt Rider Magazine" (https://rampartrange.org/rampart-range-by-dirt-rider-magazine/, 05:19 UTC): **undated and very old** (it describes the winter of 1982-83). It says the map marks "length and degree of riding difficulty ... Beginner, Intermediate and Expert", "Those levels are accurate", and describes the "easiest loop (about 12 miles)": Powerline 690, then 674 and 675 "to avoid the difficult Roi Tan Trail bypass (653)", then "Gramp's Trail 657" and back north on 690. It calls 0690 "straight, but roller coaster-like". Historical context only; trail numbers and layouts may have changed.
- Conflict: the same FAQ says "Most [ratings] were designated by the Forest Service". No Forest Service page or dataset retrieved carries a difficulty rating for these trails.
- LEAD (third party, search snippet only, not opened): onX Offroad lists "Tech Rating" 627 Beginner 2 "Easy", 681 Scotty's 3 "Easy", 657 Gramps 3 "Easy", 679 Dutch Fred 3 "Easy", 675 Cabin Ridge 4 "Moderate", and calls Scotty's Cutoff "a short detour around a big hill climb on Scotty's". Not evidence.

### 1.6 Caveats on Gap 1

- A mapped junction within 20 m is not a signed junction. Social trails, closures and downed trees (standing "downed and weakened trees" alert) are not in the data.
- 0679 is the weak link in CR-3 and DF-3 (and the only trail of DF-alt). If it is not acceptable, the clean, table-backed options are CR-1, CR-2, DF-1 and DF-2 (DF-2 subject to the 0767 data conflict).
- The 0627 / 0679.A junction at the Devil's Head spur is where the rider is closest to a campground road with a "licensed vehicles only inside the campground" rule (earlier draft, Devil's Head Campground page). Do not ride into the campground or onto 300.O.

---

## Gap 2 - Cabin Ridge Trailhead as a staging site

### 2.1 Forest Service page, in full

Source: https://www.fs.usda.gov/r02/psicc/recreation/cabin-ridge-trailhead, retrieved 2026-10-09 05:13:45 UTC, "Last updated February 18, 2025". Strength: official.

> Cabin Ridge Trailhead. Situated along the Rampart Range Road south of Highway 67, the Cabin Ridge Trailhead is located southeast of the Cabin Ridge Picnic Area. Cabin Ridge Trailhead accesses Cabin Ridge Trail (#675).
> General Information: Located southeast from the Cabin Ridge Picnic Area, and just a mile north of the Devil's Head campground, picnic area, and trail.
> Seasons of Use: Year-round
> Operational Hours: Winter closure: Rampart Range Road is closed by December 1 and remains closed throughout the winter. Rampart Range Road opens when conditions are favorable for summer recreation. A target date is April 1, but weather conditions may delay until May. Contact the South Platte Ranger District at 303-275-5610 for more information.
> Restrictions: The following restrictions apply to this trail: Dogs must be leashed at all times. Pack it in; pack it out. Practice Leave No Trace principles. Stay on designated trail. No switchbacks.
> Latitude 39.28174051, Longitude -105.10401202.
> Directions: To access the Cabin Ridge Trailhead from Denver: Travel south on Highway 85 (Santa Fe) 10 miles to the town of Sedalia. Turn west on Highway 67 and travel 10 miles west. When you get to the Rampart Range Road, turn south and continue 9.5 miles to the Cabin Ridge Trailhead.
> Facility and Amenity Information: Restrooms: No. Water: Potable water is not available at this site.
> Recreation Opportunities: Off-Highway Vehicles (OHV); OHV Trail Riding.

The page header alert strip at retrieval listed: Aspen Acres Fire Area Closure, Willow Fire Area Closure, Prescribed Fire planned on the PSICC, FSR 286 Radical Hill closure, Harris Park RX area and road closure. None names NFSR 300, Cabin Ridge or any Rampart trail.

### 2.2 Site record (Forest Service Enterprise Data Warehouse, recreation sites layer), non-empty fields

Source: https://apps.fs.usda.gov/arcx/rest/services/EDW/EDW_RecInfraRecreationSites_02/MapServer/0 (query by name), 05:13:39 UTC. Strength: agency data.

| Field | Value |
|---|---|
| site_id / site_name / site_type | 33715 / CABIN RIDGE TH / TRAILHEAD |
| seasonal_operational_status | OPEN (record last edited 2025-04-09 14:38 UTC; not a dated October confirmation) |
| development_status / development_scale | EXISTING / 3 (scale undefined in the data) |
| total_capacity | 85.0 (unit not defined: vehicles or people not stated) |
| fee_charged | N |
| restroom_availability / water_availability | "No " / "No" |
| open_season | "Year-round " |
| pack_in_out | Y |
| closest_towns | Deckers |
| operated_by | US Forest Service |
| minimum_elevation | 8,700 feet |
| restrictions | "Dogs must be leashed at all times; Pack it in; pack it out; Practice Leave No Trace principles; Stay on designated trail. No switchbacks." |
| directions | same "9.5 miles" text as the page |
| operational_hours | winter-closure text only (cut off after "Conta") |
| latitude / longitude | 39.28174051 / -105.10401202 |
| Fields that exist in the layer but are empty or absent for this record | parking surface, loading ramp, trailer parking, staging, hours of day use, accessibility, fee description |

### 2.3 Answers to the specific questions

| Question | Answer | Source / strength |
|---|---|---|
| Parking capacity | 85, unit undefined | agency data |
| Parking surface | **Not stated by any source.** NFSR 300 itself is "AGG - CRUSHED AGGREGATE OR GRAVEL", level 3, "SUITABLE FOR PASSENGER CARS" (carried). Lot surface unknown | agency data, carried |
| Signed designated parking site (Order PSICC-2022-08)? | **UNKNOWN.** The order (read 05:19 UTC) prohibits "Parking on the Described Roads or within the Described Areas unless in a developed campground or a designated parking site provided by the Forest Service that is posted with signs" within 1/4 mile of listed roads; NFSR 300 is listed; the lot is 6 m from the road, so the order applies. The Forest Service has a trailhead record (open, capacity 85) and a recreation page, but no source says the lot is posted. The MVUM front text-layer adds: "Motor vehicle designations include parking along designated routes and at facilities associated with designated routes when it is safe to do so and when not causing damage to National Forest System resources", and then points to the order for the 1/4-mile zone, which "only allows camping and/or parking in the Restricted Area where posted with these symbols". Partner: "Most are clearly designated with post and cable fencing and parking signs" and lists this lot as numbered "RRPARK40" at mile 8.1 | controlling (order, MVUM); official; partner |
| Trailer or loading notes | **None in any Forest Service source.** Partner lists loading ramps at other lots (mile 1.6, 2.8, 3.3) but not at "RRPARK40" (partner list as retrieved) | agency data; partner |
| Does a pickup with a small trailer fit? | **No source says.** No lot dimensions, polygon or trailer text exists in the data; capacity unit undefined. The only related facts: NFSR 300 is level 3 passenger-car road and the lot has no spur road | derived |
| Hours | None specific to this lot on its page. Area rule (Rampart Range Recreation Area page, CARRIED, not re-fetched): "Trailhead and OHV staging areas are open sunrise to sunset." Season "Year-round" except the road closure by 1 December | official |
| Fee | None. EDW `fee_charged` N; the page has no fee text. The picnic area next door is $7 per vehicle per day, check or money order | official; agency data |
| Restroom | None ("Restrooms No"). Nearest agency vault toilet is at Cabin Ridge Picnic Area | official |
| Water | None | official |
| Walking relationship to Cabin Ridge Picnic Area | **No agency text describes a path.** Straight-line 284 m (0.18 mi). The trailhead point is 236 m north and 158 m east of the picnic point (bearing about 34 degrees), which contradicts the page's "southeast" (carried conflict). The picnic point sits at the junction of NFSR 300 and spur 300.R (5 m from the spur's start): so the road-shoulder walk is about 0.18 mi south, and the picnic units lie along the 0.255 mi spur beyond (to about 0.44 mi from the lot). Trail 0627 runs from the lot to within 30 m of the picnic point over 0.23 mi (370 m). Whether 0627 may be walked by the family, is safe beside motorcycles, or is a path at all: UNKNOWN (NFS layer hiker field empty for 0627). Walking along NFSR 300 means sharing the road with traffic | derived |

---

## Gap 3 - Fire restriction conflict

### 3.1 Conclusion

**UNRESOLVED as a matter of documents; the weight of indirect evidence says the Stage 1 order was lifted, probably on 17 September 2026.** No Forest Service rescission or termination notice, order PDF, or news release was found. I did not find evidence that it is still in force other than the 21 August release itself. Plan to the stricter reading.

### 3.2 Evidence

Evidence the restriction was set (official):
- Forest Service news release dated 21 August 2026 (https://www.fs.usda.gov/r02/psicc/newsroom/releases/pike-san-isabel-national-forests-move-stage-1-fire-restrictions, retrieved 05:17:40 UTC): "The Pike-San Isabel National Forests will move from Stage 2 to Stage 1 Fire Restrictions beginning Aug. 21 at 12:01 a.m. through Nov. 14, unless rescinded. This includes the Pikes Peak, South Park, South Platte, Leadville, Salida and San Carlos ranger districts". It also says "Additional information for this order can be found on the PSICC alerts webpage."
- Release of 31 August (retrieved 05:17 UTC): "The San Carlos, Leadville, Salida, South Park, South Platte, and Pikes Peak Ranger Districts are currently under Stage 1 fire restrictions." (true as of 31 Aug).

Evidence it was lifted:
- Forest Service alerts list (https://www.fs.usda.gov/r02/psicc/alerts, 05:17:20 UTC): no "Fire Restriction" alert at all. Items run Oct 6, Oct 2, Oct 1, Sept 18, Sept 1, Aug 2 ...; there is no 21 August item, although the release says the order's information is on that page. Agency data / official, dynamic. Absence from a list is not proof.
- Forest Service map layer "PSICC Ranger Districts Fire Restrictions" (ArcGIS FeatureServer, https://services1.arcgis.com/gGHDlz6USftL5Pau/arcgis/rest/services/PSICCRangerDistrictsFireRestrictions_2026/FeatureServer/3, 05:17 UTC): all eight districts `FireRestct` = "1", which the layer defines as "No Restrictions" (2 = Stage 1, 3 = Stage 2). South Platte: "FireRestct": "1". Layer data last edited 2026-10-01T13:24:15Z. Agency data, dynamic.
- Fire restrictions page (https://www.fs.usda.gov/r02/psicc/fire/fire-restrictions, 05:17 UTC, "Last updated April 9, 2026"): "All fire restrictions and closures are posted on our alerts page." No stage shown.
- Newsroom list (https://www.fs.usda.gov/r02/psicc/newsroom/releases, 05:17 UTC): the 2026 releases shown are 7 Oct, 17 Sept, 31 Aug, 21 Aug. The 17 September release (fall prescribed fire) does not mention restrictions. No rescission release.
- Precedent: a web search returned a Forest Service alert titled "PSICC Lifts Stage 1 Fire Restrictions" (URL .../alerts/psicc-lifts-stage-1-fire-restrictions), snippet "the prohibitions listed in Order #02-12-00-26-07 for Stage 1 Fire Restrictions ... dated March 27, 2026 ... are hereby terminated effective May 27, 2026." That page now returns HTTP 404 (05:18:06 UTC). Pattern (derived): the forest removes both the restriction alert and the lift alert once they lapse, so a missing alert and a missing lift notice is consistent with a lift. Snippet is a lead; the 404 is official.
- Pueblo Chieftain (USA Today network, James Bartolo), published 2026-09-22T20:42Z, read at https://www.yahoo.com/news/us/articles/colorado-denied-additional-fema-aid-204235912.html (05:18:21 UTC): "Lucero's decision followed consultation with area fire chiefs and the U.S. Forest Service's decision to lift the Pike-San Isabel National Forest's fire restrictions on Sept. 17." Lead-grade (a secondary news report, on the forest's decision; the Forest Service act is not documented first-hand).
- Pueblo County Sheriff, "Posted on September 18, 2026": "Pueblo County is no longer under Stage 1 fire restrictions, effective immediately." (https://www.pueblosheriff.org/CivicAlerts.aspx?AID=654, 05:18:35 UTC; county; does not mention the Forest Service). Douglas County Sheriff: Stage 1 lifted, page "updated on 9/17/2026" (carried; same date as the reported forest lift).
- LEADS from search snippets, not opened: BLM Colorado "September 21, 2026: Stage 1 fire restrictions have been lifted"; leadville.co "Stage 1 fire restrictions are no longer posted, and no rescission notice has been published 2026-09-18" (a third-party note that agrees with my finding of no notice).
- Rejected lead: deeparrival.com says Pike-San Isabel is "under Stage 2 fire restrictions through mid-November". It contradicts the Forest Service release (Stage 1) and is not used.

Not retrieved: the order PDF for the 21 August order (its alert page is gone; an earlier draft recorded the number 02-12-00-26-37 from a search summary only); InciWeb (fire-restriction orders are not normally posted there; not checked); the forest's X and Facebook posts (lead-only sources; not retrieved).

### 3.3 What is allowed at the candidate sites

Both readings also sit under the standing Order 02-12-00-24-04 (to 1 December 2026), prohibition 3: no "fire, campfire, or stove fire except in Forest Service developed recreation sites and designated dispersed campsites" inside the Douglas County described area, which covers Cabin Ridge Picnic Area, Topaz Point, Dutch Fred and Cabin Ridge TH (earlier draft, township lookup).

| Item | If Stage 1 is IN FORCE (per the 21 Aug release summary; order text itself not retrieved) | If RESCINDED |
|---|---|---|
| Fire ring at Cabin Ridge Picnic Area | Allowed only in "a permanent metal or concrete fire pit or grate that the U.S. Forest Service has installed and maintained at its developed recreation sites (campgrounds and picnic areas)". The site page says 10 units with "fire rings" and "Fires only in established fire rings." Whether the rings are Forest Service-installed metal or concrete is not stated. Charcoal ("including fires fueled by charcoal or briquettes") is allowed only inside such a ring or grate; no portable charcoal grill set on the ground | Allowed by the standing order in a developed recreation site; site rule still "Fires only in established fire rings." |
| Gas stove with an on-off valve | Allowed: "A device solely fueled by liquid or gas that can be turned on and off used in an area barren or cleared of all flammable materials within three feet of the device". A fully enclosed metal stove with a chimney at least 5 ft long, spark screen opening 1/4 in or less, and 10 ft clearance is also allowed | At the picnic area (a developed recreation site): allowed by the standing order. At a trailhead lot: whether a lot is a "developed recreation site" is not defined (carried unknown); do not light a stove there on the strength of this file |
| Smoking | Prohibited except in an enclosed vehicle or building, a developed recreation site, or in a cleared area at least 3 ft in diameter | Not restricted by an order beyond the standing rules |
| Any fire or stove at a trailhead, along the road, or at an undesignated pullout | Stove permitted by the release if a valve device with 3 ft clear; wood or charcoal fire not permitted | Standing order prohibits stove fire outside developed sites and designated dispersed sites |

Practical consequence: **use the Forest Service fire ring or a valve-controlled gas stove inside the picnic area only.** That is allowed under every reading. Do not use a trailhead lot.

---

## Gap 4 - Topaz Point (backup family site)

| Item | Finding | Source / strength |
|---|---|---|
| Page status | "Site Open" banner; "The Topaz Point Picnic Area has ten (10) picnic sites. Picnic season begins in May and continues into October."; "Seasons of Use: May 15"; "There is a day use fee of $7. Fees are payable by check or money order."; vault toilets; no potable water. Page "Last updated February 18, 2025". No alert for Topaz or NFSR 300. https://www.fs.usda.gov/r02/psicc/recreation/topaz-point-picnic-area, 05:16 UTC | official; page status dynamic and stale |
| Site record | site_id 03571, PICNIC SITE, `seasonal_operational_status` OPEN, capacity 25, `fee_charged` N (conflicts with the page's $7), vault toilets, water No, record edited 2025-04-09, elevation 8,800 ft | agency data |
| Location | 39.2580704, -105.11731291; on NFSR 300 (2 m from the line), spur 300.M (0.073 mi) | agency data; derived |
| Trails mentioned on the page or record | None | official |
| Nearest trails by agency geometry | **0650 LONG HOLLOW** (MVUM table: <50", May 16 - Mar 14; layer 12/01-03/14, TC3; 9.85 mi): passes 124 m from the picnic point; its north start is 29 m from NFSR 300 (39.27657, -105.1095) and is not joined to any other mapped trail. **0677.A LOG JUMPER** (not in the table; layer: motorcycles and ATVs year-round; TC3; 7.04 mi): its south-east end is ON NFSR 300 about 620 m from the picnic point (39.25244, -105.11771) | agency data; derived |
| Nearest agency trailhead record | **Devil's Head TH** (site_id 27157, TRAILHEAD, capacity 80, 39.26973, -105.10486, no web page id, restroom empty). 1.04 mi straight from Topaz Point; about 2.7 mi by road (NFSR 300 about 2.1 mi to the 300.O junction, then 0.59 mi down spur 300.O). The Devil's Head trail 0611 is a hiking trail (motorized "N" in the NFS layer). By geometry it is 490-500 m from 0679.A's start and 0627's south end | agency data; derived |
| Partner trailheads near Topaz | "10.8 TOPAZPPG Topaz Point Picnic Area, vault toilet"; "11.3 RRPARK42 Trailhead for trail 677 (Log Jumper Trail)" at 39.25242, -105.11773 (matches the 0677.A end); "8.7 RRPARK41 Trailhead for trial 690 (Powerline Trail)" at 39.27668, -105.10922 (the agency geometry puts the start of 0650 there, not 0690: conflict) | partner |
| Could a rider stage legally close by? | **No agency record of a trailhead or designated parking site exists at the two trail ends near Topaz.** Order PSICC-2022-08 bars parking within 1/4 mile of NFSR 300 except in a developed campground or "designated parking site ... posted with signs". Whether the partner's numbered pullouts are posted: UNKNOWN. The nearest agency-listed trailhead is Devil's Head TH (2.7 road miles; trail access from it is 0679.A / 0627 via a campground road: not established). An unplated bike cannot ride the road between. **Realistic reading (derived): rider stages at Cabin Ridge Trailhead (2.7 road miles north of Topaz) or Dutch Fred, as in Gap 1; Topaz Point is a family site, not a staging site.** | controlling; agency data; partner; derived |
| Fire | A developed picnic area; same Gap 3 rules apply | - |

---

## Conflicts preserved

1. **Stage 1 fire restriction**: release "through Nov. 14, unless rescinded" vs no alert, map layer "No Restrictions" (edited 1 Oct), and a news report of a forest lift on 17 Sept; no rescission document retrieved.
2. 0679 Dutch Fred: drawn seasonal on the MVUM, no table row; layer says 1 June - 30 November (carried).
3. Layer motorcycle dates 12/01-03/14 vs MVUM table May 16 - March 14 for 0675, 0627, 0657, 0680, 0679.A, 0681 and others (carried; map controls).
4. 0679.B: table "<50" vs agency layers "motorcycles only, year-round, ATV restricted".
5. 0767 / 0767.A: table and MVUM layer "all vehicles" vs NFS trails layer "restricted".
6. Cabin Ridge Trailhead direction: page "southeast" of the picnic area vs coordinates (north-east).
7. Directions: Forest Service "continue 9.5 miles" to both Cabin Ridge sites vs partner mile 8.1 (trailhead) and 8.4 (picnic area).
8. Partner "RRPARK41 trailhead for trail 690" (mile 8.7) vs agency geometry (the start of 0650 is there; 0690 starts at the NFSR 506 junction).
9. Partner Dutch Fred waypoint coordinates (N39 20.463 W105 4.882) are identical to its Garber 686 entry at mile 3.3 and do not match the Forest Service point; treat as a partner typo (derived).
10. Lightfoot Loop: partner "about 1 mile" and "at the Dutch Fred parking lot" vs mapped 0.57 mi (0.75 with 0767) and 0.33 mi up 0681 from the lot.
11. MVUM sentence "Motor vehicle designations include parking along designated routes and at facilities associated with designated routes" vs Order PSICC-2022-08 (parking only in posted designated sites within 1/4 mile of NFSR 300). The MVUM itself defers to the order.
12. RRMMC says ratings "were designated by the Forest Service"; no Forest Service source retrieved carries any.
13. 0627 length: `GIS_MILES` 9.218 (MVUM) / 8.927 (NFS) / mile posts 0-9.75 vs mapped 9.0 mi in two pieces with a 409 m gap.
14. Topaz Point fee: page $7 vs record `fee_charged` N.
15. Third-party claim of Stage 2 through mid-November (deeparrival.com) vs Forest Service release (Stage 1).

## Unknowns

- Whether the Cabin Ridge lot is posted as a designated parking site; its surface, size and trailer fit; hours.
- Any designated or signed trail crossing of NFSR 300 at the Cabin Ridge lot or elsewhere on the rides.
- Direction of the one-way Lightfoot Loop; whether 0767 is usable by a motorcycle (dataset conflict).
- Season of 0679 on the controlling map; motorcycle legality of 0627.A, 0681.D, 0681.F, 0770.A's first 0.17 mile, 0690's last 0.39 mile (all avoided).
- Location and status of 0681.D (not returned by any query).
- Whether the 2025 South Platte MVUM is validated for 2026 (carried).
- The text of the 21 August order; whether it was formally terminated and when.
- Whether the picnic-area fire rings are Forest Service-installed metal or concrete; whether a trailhead lot is a "developed recreation site".
- Whether the family may walk trail 0627 between the lot and the picnic area.
- Physical condition of every trail and of NFSR 300 (no agency condition source; partner banner "Trail Status: OPEN / Rampart Range Road Status: OPEN" is undated).
- Whether the Kiddy Corral and the Flat Rocks "kiddy track" are designated riding areas.
- RRMMC printed-map ratings (NOT RETRIEVED).

## Sources

All retrieved 2026-10-09 UTC. "Agency data" rows are queries by bounding box or by name, no bulk download.

| # | URL | Publisher | Retrieved (UTC) | Strength |
|---|---|---|---|---|
| 1 | https://apps.fs.usda.gov/arcx/rest/services/EDW/EDW_MVUM_02/MapServer/2/query (box -105.125,39.245,-105.07,39.30; all fields, geometry; 21 records) and MapServer/1/query (same box, selected fields; 10 records) | USDA Forest Service, Enterprise Data Warehouse | 05:13:18 and 05:13:37 | agency data (not a legal document) |
| 2 | https://apps.fs.usda.gov/arcx/rest/services/EDW/EDW_TrailNFSPublish_01/MapServer/0/query (same box; 25 records) and MapServer/0?f=json (layer description and field list) | same | 05:13:19 and 05:19:56 | agency data |
| 3 | https://apps.fs.usda.gov/arcx/rest/services/EDW/EDW_MVUM_02/MapServer/2/query (three small boxes: north of Dutch Fred, 15 records; west of Cabin Ridge, 4 records; Topaz area, 6 records) | same | 05:16:02 to 05:16:26 | agency data |
| 4 | https://apps.fs.usda.gov/arcx/rest/services/EDW/EDW_RecInfraRecreationSites_02/MapServer/0/query (by name: 4 records; box near Topaz: 8 records; an `IN` query failed, HTTP 400) | same | 05:13:39, 05:16:24 | agency data |
| 5 | https://www.fs.usda.gov/r02/psicc/recreation/cabin-ridge-trailhead (updated Feb 18, 2025) | USDA Forest Service | 05:13:45 | official |
| 6 | https://www.fs.usda.gov/r02/psicc/recreation/topaz-point-picnic-area (updated Feb 18, 2025) | USDA Forest Service | 05:16:25 | official |
| 7 | https://www.fs.usda.gov/sites/nfs/files/r02/psicc/publication/alerts/fseprd1060368.pdf (Order PSICC-2022-08) | USDA Forest Service | 05:19:03 | controlling |
| 8 | https://www.fs.usda.gov/sites/nfs/files/r02/psicc/publication/SPLTMVUMFINALFRONT07302025.pdf and ...BACK07302025.pdf (text layer searched for parking, trailhead, cross, junction, Cabin, Topaz, Dutch labels; the seasonal table was NOT re-read: carried) | USDA Forest Service | 05:19:04, 05:19:06 | controlling |
| 9 | https://rampartrange.org/trail-info/ ; /parking-areas/ ; /frequently-asked-questions/ ; /trail-markings/ ; /about-rampart/ ; /directions/ ; /rampart-range-by-dirt-rider-magazine/ | RRMMC (volunteer partner) | 05:16:48 to 05:19:55 | partner |
| 10 | https://www.fs.usda.gov/r02/psicc/alerts ; /fire/fire-restrictions ; /newsroom/releases | USDA Forest Service | 05:17:20 to 05:17:25 | official, dynamic |
| 11 | https://www.fs.usda.gov/r02/psicc/newsroom/releases/pike-san-isabel-national-forests-move-stage-1-fire-restrictions ; .../psicc-prepares-fall-prescribed-fire-treatments ; .../rampart-reservoir-area-prescribed-fire-planned-watershed-health-pikes ; .../select-areas-reopen-aspen-acres-fire-progresses-toward-full-containment | USDA Forest Service | 05:17:40 to 05:17:47 | official |
| 12 | https://services1.arcgis.com/gGHDlz6USftL5Pau/arcgis/rest/services/PSICCRangerDistrictsFireRestrictions_2026/FeatureServer/3 (query and layer info) | Forest Service map on ArcGIS Online | 05:17:25 | agency data, dynamic |
| 13 | https://www.fs.usda.gov/r02/psicc/alerts/psicc-lifts-stage-1-fire-restrictions - HTTP 404; NOT RETRIEVED | USDA Forest Service | 05:18:06 | - |
| 14 | https://www.pueblosheriff.org/ and /CivicAlerts.aspx?AID=654 | Pueblo County Sheriff's Office | 05:18:21, 05:18:35 | county |
| 15 | https://www.yahoo.com/news/us/articles/colorado-denied-additional-fema-aid-204235912.html (canonical: chieftain.com ... 2026/09/22 ... fema-denies-housing-mitigation-aid-for-colorado-after-aspen-acres-fire) | Pueblo Chieftain via Yahoo News | 05:18:23 | lead |
| 16 | http://rmb.reuters.com/... (news feed copy of the same story) - HTTP 401; NOT RETRIEVED | Reuters feed | 05:18:06 | - |

Web searches (5), used for leads only; snippets are not cited as evidence except where labelled "lead": (1) Pike-San Isabel Stage 1 lifted/rescinded October 2026; (2) same with South Platte and Forest Order 02-12-00-26; (3) Pueblo County Stage 1 lifted, Sept. 17; (4) Pike-San Isabel lifted September 2026 with Gazette, KRDO, KOAA, Pueblo Chieftain; (5) rampartrange.org trail ratings for Gramps, Scotty's, Cabin Ridge, Dutch Fred. Not used as sources: onX Offroad, Trailforks, leadville.co, deeparrival.com, BLM Colorado page snippets, Summit Daily / Aspen Times snippets (undated, other year).
