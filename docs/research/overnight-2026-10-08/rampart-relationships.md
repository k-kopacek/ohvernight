DRAFT - UNREVIEWED RESEARCH

# Rampart Range - relationship evidence (Section B)

- Purpose: for each relationship type in `adventure-model.md` section 3, does a responsible source state it explicitly, where, with what quote, and is it available as structured data or only prose. Rampart Range (Pike NF, South Platte Ranger District) is the case study.
- Retrieved 2026-10-08 22:11-22:22 UTC. Extends `rampart-official-facts.md` and `rampart-evidence-closure.md` (Section A, same day); retrievals reused from Section A are not repeated unless a new reading was made.
- Labels: **[SF]** source fact / **[ORI]** official recreation information / **[P]** partner (RRMMC, volunteer partner, not an agency) / **[D]** derived by me with the rule shown / **[U]** unknown.
- Relationship origins follow the model: source-backed, derived, reviewed candidate, unknown. Proximity is not a relationship.
- Section B budget: 0 new searches; about 13 new retrievals (ArcGIS queries for trail names and geometry, FS TrailNFS_Publish layer, three metadata XML files, one failed metadata guess).

---

## 1. New evidence used in this section

1. **Trail names.** The EDW "Trail NFS Publish" layer (https://apps.fs.usda.gov/arcx/rest/services/EDW/EDW_TrailNFSPublish_01/MapServer/0) carries the trail's official name, `trail_no` and `trail_name`, for the Rampart trails, where the MVUM layers carry only the number (`name` is null on all 57 MVUM trail features). Examples (managing org 021211, attribute subset `TrailNFS_MGMT`): 0627 BEGINNER; 0646 ARROWHEAD; 0673 BARR; 0674 FLATROCK; 0675 CABIN RIDGE; 0677 NODDLE; 0677.A LOG JUMPER; 0679 DUTCH FRED; 0681 SCOTTYS; 0682 OVERLOOK; 0686 GARBER; 0688 BEAVER; 0690 POWERLINE; 0767 UPPER DUTCH; 0767.A LIGHTFOOT LOOP; 0770.F SKELETON. Retrieved 22:20 UTC. [SF]-grade attribute.
2. **Metadata** (retrieved 22:21 UTC): https://data.fs.usda.gov/geodata/edw/edw_resources/meta/S_USA.Trail_MVUM.xml, `S_USA.Road_MVUM.xml`, `S_USA.TrailNFS_Publish.xml`. Update frequency in all three: "As needed". Completeness "Complete" (MVUM). The recreation-opportunity metadata files I guessed (three names) returned HTTP 404 - NOT RETRIEVED.
3. **Geometry check, derived** (22:20 UTC, my calculation from the layer geometry; method in section 3.2).

---

## 2. Relationship by relationship

### 2.1 Recreation area -> its trailheads

**Explicit statement by a responsible source?** Partly, as prose, and as one incomplete structured grouping field.

| Evidence | Quote / field | Where published | Label |
|---|---|---|---|
| Trailhead pages say they belong to the area | "The following restrictions apply to the Rampart Range Motorized Recreation Area:" (on Dutch Fred Trailhead, Flat Rocks Trailhead, Sugar Creek Lower Trailhead and others) and "The Dutch Fred Trail (#679) enters into a system of 115 miles of motorcycle and ATV trails in the Rampart Range Recreation Area." | Forest Service recreation pages, e.g. https://www.fs.usda.gov/r02/psicc/recreation/dutch-fred-trailhead | [ORI], prose |
| Area page does not list its children | "Turn south on Rampart Range Road to access the OHV trails and dispersed camping areas." No list of trailheads in the page body; the only links found were generic forest menu links. | https://www.fs.usda.gov/r02/psicc/recreation/rampart-range-recreation-area (retrieved 22:20) | [ORI] |
| Parent record exists in the database, with no child pointer | Record `recareaid` 80379 "Rampart Range Recreation Area", `markeractivity` "Intermediate Parent Group". The record has no field naming children. | EDW_RecreationOpportunities_01, layer 0 | [SF]-grade, no relation field |
| Site database groups sites with a free-text label | `complex_name` = "RAMPART RANGE" on 11 of the 23 recreation sites inside the search box (including FLAT ROCKS TH, FLAT ROCKS CG, CABIN RIDGE TH, CABIN RIDGE PS, SUNSET POINT, TOPAZ POINT, DEVILS HEAD TH/CG/PS, RAMPART ENTRANCE, MILE AND A HALF). `complex_name` is **null** for DUTCH FRED, GARBER CREEK, RIM ROAD, 677A NODDLE, INDIAN CREEK (both), FLAT ROCKS OS and others that are plainly part of the same recreation area per their own pages. `parent_cn` is null on all 23. | EDW_RecInfraRecreationSites_02, layers 0 (retrieved 22:16) | [SF]-grade attribute, incomplete |
| Recreation.gov | Facility 10132201 "Rampart Range Recreation Area Designated Dispersed Camping": "Trailhead parking within the Rampart Range Recreation Area is free." Names the area and the activity; no list. | https://www.recreation.gov/api/camps/campgrounds/10132201 (record updated 2025-12-29) | [ORI], prose |
| Partner | RRMMC "parking areas" table lists trailheads by mileage from Highway 67. | https://rampartrange.org/parking-areas/ | [P] |

**Findings.**
- The relationship "trailhead X is in Rampart Range Recreation Area" is stated per trailhead in prose (restriction boilerplate and body text), but there is **no relation field**; `complex_name` covers some sites only. Absence of the label on Dutch Fred must not be read as non-membership.
- Naming is inconsistent: "Rampart Range Recreation Area" (page title, Recreation.gov, database parent), "Rampart Range Motorized Recreation Area" (restriction boilerplate; RRMMC), "Rampart Range Road" as an area label, "RAMPART RANGE" (complex_name), "Rampart Range Motorized Management Committee" vs "Motorcycle Management Committee" in partner text. A name match is not a relationship.
- Boundary of the "recreation area" as a polygon: not found in any dataset retrieved (the National Forest recreation-area polygons were not searched; EDW lists no layer I recognised for it). **[U]**

### 2.2 Trailhead or staging area -> the trails that start there

**Explicit?** Prose only, by the agency, and only by trail number, with the verb "enters". No structured field.

| Evidence | Quote | Where | Label |
|---|---|---|---|
| Flat Rocks TH | "The Flat Rocks Trailhead is located south of Indian Creek along the Rampart Range Road. The Flatrock Trail (#674) trail enters into a system of 115 miles of motorcycle and ATV trails in the Rampart Range area." | https://www.fs.usda.gov/r02/psicc/recreation/flat-rocks-trailhead ("Last updated February 18, 2025") | [ORI], prose |
| Dutch Fred TH | "The Dutch Fred Trailhead is located south of Indian Creek along the Rampart Range Road. The Dutch Fred Trail (#679) enters into a system of 115 miles of motorcycle and ATV trails in the Rampart Range Recreation Area." | .../recreation/dutch-fred-trailhead | [ORI], prose |
| Published MVUM map | Symbol "Motorized Trailhead" (legend) at "DUTCH FRED" and at "ENDURO SKILLS AREA" with leader lines to trail labels 0681.E and 0767.A (image-read; see Section A 2.2). The map does not print a sentence relating them. | South Platte MVUM back, Rampart Range Road Inset | [SF], graphic only |
| Structured trail data | MVUM roads/trails and TrailNFS_Publish have **no field** naming a trailhead, start point, or access point. Fields checked: all 60+ attribute names of both layers. | EDW_MVUM_02 layer 2; EDW_TrailNFSPublish_01 layer 0 | - |
| Structured site data | The recreation-site record for FLAT ROCKS TH/DUTCH FRED has `activity_type_list` "No Data", no trail pointer. | EDW_RecInfraRecreationSites_02 | - |
| Partner | RRMMC "RRPARK22 Trail head for trail 673 (Bar Trail) (Flat Rocks TH)"; "Dutch Fred ... trailhead for trail 681 (Scotty's Trail)". | https://rampartrange.org/parking-areas/ | [P] |

**Conflict:** agency says #674 at Flat Rocks TH, partner says #673. Agency page says #679 at Dutch Fred, partner says #681. The MVUM map labels both 0679 and 0681 (and 0767, 0767.A) at the Dutch Fred trailhead.

**Derived candidates** (my calculation, 2026-10-08 22:20 UTC, from the EDW TrailNFS_Publish geometry; rule below, section 3.2). Straight-line distance from the trailhead point (agency coordinates) to the nearest trail endpoint, and to any trail vertex:

| Trailhead (agency coords) | Trails whose line passes within 100 m | Of which, a trail *endpoint* is within 100 m |
|---|---|---|
| Flat Rocks Trailhead (39.3272819, -105.08692203) | 0770.A TUNNEL (35 m), 0627 BEGINNER (35 m, endpoint 3.7 km away), 0682 OVERLOOK (37 m), 0673 BARR (53 m), 0690 POWERLINE (87 m, endpoint 4 km away) | 0770.A, 0682, 0673 |
| Dutch Fred Trailhead (39.28573479, -105.09196036) | 0681 SCOTTYS (4 m), 0679 DUTCH FRED (12 m; endpoint 109 m) | 0681 (10 m); 0679 endpoint is 109 m, just outside |

- **Mismatch with prose:** the agency's named trail for Flat Rocks, 0674 FLATROCK, is 307 m from the campground and 405 m from the trailhead point and has no endpoint within 100 m of either. The geometry candidates (0682, 0673, 0770.A) do not include it. This is why "within N metres" must stay a *candidate* and why prose must be reviewed against the map. [D]
- **"Skeleton Loop"** (benchmark claim): the agency has a trail named SKELETON, numbered **0770.F**, motorcycle-only, at roughly latitude 39.20-39.21 (about 13 km south of Flat Rocks Trailhead; endpoints (-105.1066, 39.2109) and (-105.0684, 39.2005)). No source I read ties it to Flat Rocks Trailhead. The benchmark's "Skeleton Loop at Flat Rocks" is **not supported** by agency evidence and the geometry argues against it. [D]/[U]
- **Identifier gap:** prose says "#674" and "#679"; datasets say "0674"/"674" (TrailNFS_Publish uses "0674", MVUM_02 trail `id` uses "674", MVUM PDF table "0674", partner "673"). Without zero-padding normalization a join silently fails. Also TrailNFS_Publish contains both "0627" and "627.A", "681.D", "681.F" (unpadded) in one layer.

**Verdict:** prose needing review; derived endpoint candidates only for review; structured not available.

### 2.3 Trail -> motorized-use rule

**Explicit?** Yes - this is the one relationship that is source-backed *and* structured, but the three structured/published representations conflict.

| Representation | Fields / table | Example (trail 0674 FLATROCK) | Label |
|---|---|---|---|
| Published MVUM PDF, table "Seasonal and Special Vehicle Designations" | route numbers, description, "Dates Allowed" | row with 0674: "Trail, <50" wide (open to OHVs such as ATVs and motorcycles)", "May 16 - March 14" (image-read) | [SF], graphic/table |
| MVUM feature service layer 2 | `motorcycle` = "open", `motorcycle_datesopen` = "12/01-03/14", `seasonal` = "seasonal", `mvum_symbol_name` = "Trails open to vehicles 50" or less in width, Seasonal" | https://apps.fs.usda.gov/arcx/rest/services/EDW/EDW_MVUM_02/MapServer/2 | [SF]-grade attribute |
| TrailNFS_Publish layer | `allowed_terra_use` = "54321" (1 hiker, 2 pack and saddle, 3 bicycle, 4 motorcycle, 5 ATV), `terra_motorized` = "Y", `motorcycle_accpt` = "12/01-03/14" ("Date range for which motorcycle use is accepted"), `motorcycle_managed` null | https://apps.fs.usda.gov/arcx/rest/services/EDW/EDW_TrailNFSPublish_01/MapServer/0 | [SF]-grade attribute |
| Forest Service page prose | "a system of 115 miles of motorcycle and ATV trails"; "Registered OHVs may be subject to fines if used where they are not specifically permitted." and the registration/50-inch restrictions | .../dutch-fred-trailhead | [ORI], prose |

Conflicts (all new in this section or sharpened):
- **Dates:** PDF "May 16 - March 14" vs both datasets "12/01-03/14" for ~40 trails (see Section A 2.4).
- **Trails 0767 and 0767.A** (UPPER DUTCH, LIGHTFOOT LOOP - the partner's "Lightfoot's Loop"): PDF "Trail Open to All Vehicles May 16 - November 30" and "Trail <50" wide Dec 1 - March 14"; MVUM feature service "Trails open to all vehicles, Seasonal" with motorcycle 05/16-11/30; **TrailNFS_Publish has `allowed_terra_use` "321" (hiker, pack and saddle, bicycle - no motorcycle, no ATV) and `motorcycle_restricted` = "01/01-12/31" ("Indicates TERRA trails where motorcycle use is restricted year-round")**, while `terra_motorized` is "Y". The three sources give three different answers for a trail the partner presents as beginner riding. **[U] unresolved; must remain unknown until a person reconciles.**
- **Trail 0690 POWERLINE:** MVUM_02 "Special Designation, Yearlong" with the `motorcycle` field null and `other_ohv_lt50inches` open; TrailNFS_Publish `allowed_terra_use` "54321" and `motorcycle_accpt` "01/01-12/31"; not in the PDF table. Partner says Powerline can be used by unlicensed bikes. [U]
- **Trail 0693:** PDF "June 1 - March 31"; MVUM_02 01/01-12/31.
- **The data standard itself separates "managed", "accepted", "discouraged" and "restricted"** for each use (TrailNFS_Publish metadata: "MOTORCYCLE_ACCPT: Indicates TERRA trails where motorcycle use is allowed, but not managed or restricted seasonally or year-round."). For a pipeline this means the word "accepted" in the data is not the word "designated"; the legal designation lives in the MVUM, not in TrailNFS_Publish. The MVUM metadata states its own scope: "Any reference to Open or Dates Open refers strictly to when it is legal to use that motor vehicle on the trail. It is not meant to describe when the conditions would be appropriate for that use."
- **Disclaimer in the metadata (quote):** "These geospatial data and related maps or graphics are not legal documents and are not intended to be used as such." (MVUM trail metadata, retrieved 22:21 UTC.) The same file calls the data "dynamic" that "may change over time".

**Verdict:** source-backed in principle (structured and published map), with three-way conflicts; prose confirms vehicle class in general. Source-backed for the trails where all representations agree; must remain unknown where they conflict.

### 2.4 Road -> plated-vehicle rule

**Explicit?** Prose gives the rule at area level; structured data gives it only as vehicle *classes*.

| Evidence | Quote | Where | Label |
|---|---|---|---|
| Area-level prose | "A current license plate and valid driver’s license are required to ride on the roads." (listed under restrictions that "apply to the Rampart Range Motorized Recreation Area") | Forest Service trailhead pages (Dutch Fred, Flat Rocks TH, Sugar Creek Lower) | [ORI], prose; area, not road id |
| Road data model | Road MVUM definitions: PASSENGERVEHICLE "... vehicles less than 10,000 GVW licensed to operate on public roads"; HIGHCLEARANCEVEHICLE "'All sport utility vehicles (SUV), light trucks, motorcycles and other highway legal vehicles designed for operation on rough terrain'"; MOTORCYCLE "'Two-wheeled vehicles on which the two wheels are inline, not side-by-side'"; SYMBOL 3/4 "Roads open to highway legal vehicles only", 11/12 "Special Designation". | https://data.fs.usda.gov/geodata/edw/edw_resources/meta/S_USA.Road_MVUM.xml (22:21 UTC) | [SF] definitions |
| NFSR 300 record | symbol "Special Designation, Seasonal"; `passengervehicle` open 05/16-11/30; `motorcycle` open 12/01-03/14; no definition of "Special Designation" in the metadata beyond the symbol name. | MVUM_02 layer 1 (Section A 2.5) | [SF]-grade attribute |
| Partner | "Note that Rampart Range Road is not open to unlicensed vehicles." and FAQ "Rampart Range Road is a county road and all the rules of public roadways apply." (the second contradicts the MVUM `jurisdiction` "FS - FOREST SERVICE") | https://rampartrange.org/directions/ ; /frequently-asked-questions/ | [P] |

**Findings.** There is no road-level field in any dataset that says "plate required" for an individual road. A plate requirement is encoded only indirectly (classes "highway legal", "licensed to operate on public roads", and the absence of an OHV class or a motorcycle date for the season). The MVUM motorcycle field cannot distinguish a plated from an unplated motorcycle; the metadata's own HIGHCLEARANCEVEHICLE definition lists "motorcycles ... highway legal". A pipeline could not derive "unplated dirt bike prohibited on NFSR 300" from the data without a reviewed interpretation; the page prose is the only plain statement and it is attached to the area, not to a road id.

**Verdict:** prose needing review (area-level rule applied to a road id by a person); structured evidence is classes only; the connection to an unplated bike must be reviewed.

### 2.5 Staging area -> nearby day-use facilities

**Explicit?** No responsible source states it.

- Agency pages: Cabin Ridge Picnic Area "Just a mile north of the Devil’s Head trail" (landmark, not a trailhead relation); FS Cabin Ridge Picnic Area page and Flat Rocks Campground page do not name nearby staging areas except Flat Rocks CG: "ATVs and off-road motorcycles are allowed to enter and depart the campground for trail access." This is the closest explicit official statement tying a day-use-capable site to trail access, and it is about riding *from* the campground, with the MVUM as the controlling reference: "Consult the current motor vehicle use map for specific roads and trails open to off-road vehicles." [ORI], prose.
- Agency data: names share a stem (FLAT ROCKS TH, FLAT ROCKS CG, FLAT ROCKS OS; CABIN RIDGE TH, CABIN RIDGE PS) and `complex_name` "RAMPART RANGE" is shared by 11 sites - a shared label, not a pairing. **Name match and shared complex label are not relationships.**
- Partner: RRMMC "8.4 CABRDGPG Cabin Ridge Picnic Area (no camping), vault toilets (Cabin Ridge TH)" - the partner itself merges picnic area and trailhead into one line. [P]
- Distance: Flat Rocks Campground to Flat Rocks Trailhead about 0.28 mile straight line [D] (from the two agency coordinate pairs; road connection between them is not established, though FS spur names (300.T FLAT ROCK CG, 300.S FLAT ROCKS OVERLOOK) exist as MVUM road records).

**Verdict:** must remain derived (distance) or unknown (practical base). Agency statement exists only for "enter and depart the campground for trail access".

### 2.6 Site -> governing order and jurisdiction

**Jurisdiction (who manages):** explicit and structured.
- Recreation-site records: `managing_org` = "021211", `security_id` = "0212", `region` "02" for every site read; `operated_by` "US Forest Service" or "Concessionaire". MVUM trail/road records: `adminorg` "021211", `districtname` "South Platte Ranger District", `forestname` "Pike and San Isabel National Forests", `jurisdiction` "FS - FOREST SERVICE". Recreation.gov: `org_code` "FS". [SF]-grade attributes; EDW layers retrieved 22:13-22:16 UTC.
- Caution: that is the managing organisation of the record; it is not a statement that a specific order applies. Also the road jurisdiction conflicts with the partner's "county road" claim; follow the agency attribute, but the dispute itself is open.

**Governing order (which rules apply):** explicit in the order, **prose and PDF tables only**.
| Order | Scope statement (quote) | Where | Label |
|---|---|---|---|
| Order 2022-08 (parking and camping, South Platte RD) | "The Described Areas are all NFS lands within 1/4 mile of the centerline of the Described Roads"; Exhibit B lists road ids such as "300.T FLAT ROCK CG", "300 RAMPART RANGE", "506 DUTCH FRED" (earlier file) | https://www.fs.usda.gov/sites/nfs/files/r02/psicc/publication/alerts/Order%202022-08%20table.pdf | [SF], PDF table keyed by NFSR id |
| Order 02-12-00-24-04 (Pike NF occupancy and use) | "The following are prohibited on all National Forest System (NFS) lands within the Pikes Peak, South Platte, and South Park Ranger Districts of the Pike National Forest." (prohibitions 1-2); prohibitions 3-7 apply to "Described Areas ... shown on Exhibits B (Pikes Peak), Exhibit C (South Platte), and Exhibit D (South Park)" (this session, retrieved 22:17); Exhibit F per earlier file lists township/range and road buffers | https://www.fs.usda.gov/sites/nfs/files/r02/psicc/publication/alerts/fseprd1174599.pdf | [SF], prose plus map/table exhibits |
| Order 02-12-00-23-07 (food storage) | forest-wide "All NFS lands" | earlier file | [SF] |

- The only join key between an order and a place that is **machine-readable in principle** is the NFSR route id string in the Order 2022-08 table (for example "300.T") that equals the `id` in MVUM road records (for example 300.T FLAT ROCK CG). It is a PDF table, not a published dataset; a person would have to transcribe it, and the id normalization issue (zero-padding, ".A" suffixes) applies. Order 02-12-00-24-04 identifies places by township and range and map exhibits.
- No order dataset (forest orders as geometry) appears among the 145 services in the EDW REST directory (list read 22:20; names containing order/closure/restriction/alert: none found). Forest Service alerts are a web list with order numbers (for example "#02-12-00-24-04") but no geometry. [D] absence in a directory listing; not proof no such dataset exists elsewhere.
- Order scope applicability is not stated per recreation site anywhere. Which site is covered by "the Described Areas" has to be computed from the exhibit, so any such relationship would be a **reviewed candidate**, at best.

**Verdict:** jurisdiction: source-backed, structured. Governing order: source-backed in the order's own scope text (prose/PDF table), must be loaded as prose needing review; the site-to-order link is derived unless a person confirms against the exhibit.

---

## 3. Notes on method

### 3.1 What counted as "explicit"
A relationship was counted explicit only if a source states it in its own words, or defines it with a field whose published definition says so. Names, shared stems and shared labels do not count.

### 3.2 Derived-candidate rule used for 2.2
Rule: for each trailhead point (coordinates quoted from the agency page), compute the great-circle (haversine) distance to every trail vertex and every trail first/last vertex in the TrailNFS_Publish geometry for lon -105.16..-105.04, lat 39.22..39.38, WGS84 (EDW layer in outSR 4326). Reported minimum over vertices and over endpoints. Inputs: 65 trail features. This is a straight-line candidate rule and says nothing about legal travel, direction, gates, or whether the trail "starts" there. A derived relationship is never upgraded to source-backed by repetition.

### 3.3 Limits
- Image-read of the MVUM PDF (Section A) feeds 2.3 and 2.4; human re-read needed.
- Recreation.gov RIDB (the public API, which needs a key) was not used; the Recreation.gov web record was used instead. The Recreation.gov website's JSON endpoint is not documented as a public API; its terms were not read in this section (Section C).
- No agency or person contacted.

---

## 4. Conclusion table

Key: **S-structured** = could be loaded as source-backed from structured data; **S-prose** = source-backed, prose/PDF needing review before loading; **Derived** = must remain derived; **Unknown** = must remain unknown.

| Relationship | S-structured | S-prose (review) | Derived only | Unknown | Notes |
|---|---|---|---|---|---|
| Recreation area -> its trailheads | Partially: `complex_name` "RAMPART RANGE" on 11 of 23 sites (EDW_RecInfraRecreationSites_02) | Yes: restriction boilerplate and body text per trailhead page | No polygon found; containment would be derived | Membership of sites with null `complex_name` is not established by that field; area boundary [U] | Inconsistent area names; no `parent_cn` link |
| Trailhead/staging -> trails that start there | No field exists | Yes: "The Flatrock Trail (#674) trail enters ..."; "The Dutch Fred Trail (#679) enters ..." (verb "enters") | Endpoint-within-100 m candidates (0770.A, 0682, 0673 at Flat Rocks; 0681 at Dutch Fred) - candidates for review | Skeleton Loop at Flat Rocks (no source; geometry argues against); whether "enters" means "starts" | Prose and geometry disagree for Flat Rocks |
| Trail -> motorized-use rule | Yes, for trails where PDF table, MVUM_02 and TrailNFS_Publish agree | Plain-language class statements | No | Dates for ~40 trails (PDF vs data); 0767/0767.A; 0690; 0679 designation | Data standard says "not legal documents" |
| Road -> plated-vehicle rule | Only as vehicle classes ("highway legal", "licensed to operate on public roads"); not a per-road plate flag | Area-level "A current license plate and valid driver’s license are required to ride on the roads." | Plate rule per road id is derived by a person | Meaning of "Special Designation" for NFSR 300; spur 506 designation (conflict) | Partner says "county road"; agency data says Forest Service |
| Staging -> nearby day-use facilities | No | Only "ATVs and off-road motorcycles are allowed to enter and depart the campground for trail access" (campground, not a general staging link) | Straight-line distance; shared stems and `complex_name` are labels not links | Whether a picnic/day-use site is a practical base for a given trailhead; road connection | Partner merges picnic area and trailhead on one line |
| Site -> governing order | No machine-readable order geometry or order id on any site record | Order scope text; Order 2022-08 Exhibit B keyed by NFSR id; Order 02-12-00-24-04 exhibits by township/range | Spatial containment in "Described Areas" or 1/4-mile buffer | Which exhibit covers which site until reviewed; closures beyond the alerts list | Joining on NFSR id strings needs normalization |
| Site -> jurisdiction/managing agency | Yes: `managing_org` "021211", `security_id` "0212"; MVUM `adminorg`, `districtname`, `jurisdiction` "FS - FOREST SERVICE" | Page "Contact" text (South Platte Ranger District) | Containment in a ranger-district polygon (EDW_RangerDistricts) would be context only | Road jurisdiction vs the partner's "county road" claim | Page mislabels: Flat Rocks TH page says "South Park Ranger District"; Rampart page header says "Pikes Peak Ranger District" |

Reading guide: nothing in the table says any activity is permitted. "Source-backed" means a responsible source states the relationship, not that the user may do anything.
