DRAFT - UNREVIEWED TECHNICAL AUDIT (main bb85785)

# RECREATION DIRECTIONS INTEGRITY AUDIT

Scope: every recreation-site record that carries directions text. Read-only audit of `main` at `bb85785` (checkout `m3-foundation`), offline. Judgements use only evidence inside the committed data, except where a line is marked GENERAL KNOWLEDGE. No agency page was opened; the research worker should verify the records listed in section 8.

## 1. Summary

| | count |
|---|---|
| Recreation records in Douglas `recreation` layer | 36 |
| Records with directions text (all audited) | 18 |
| CONSISTENT | 13 |
| AMBIGUOUS | 3 |
| MISMATCH | 2 |
| Of the 18, rendered to users today under "Agency directions" | 14 (5 campgrounds, 9 trailheads) |
| Mismatches rendered to users today | 2 of 2 |

- Both known suspects are confirmed as mismatches on in-data evidence: RAMPART ENTRANCE (`recreation-3314802`) and TURKEY (`recreation-3310732`). Their activity lists, and RAMPART ENTRANCE's `important_info`, are also foreign to the site.
- Root cause is not a join in this repository. The pipeline performs no join: `enrich_douglas.py` copies 14 attributes from each row of one ArcGIS layer. The wrong text is in the source row as retrieved, or was introduced by the agency's own pairing of site inventory with descriptive text. Which of those cannot be determined offline.
- The repository's part in the defect is that it republishes the text under the label "Agency directions" with no integrity check, next to a link whose caption says "Directions are for this facility".
- The two mismatches and one consistent record (DEVILS HEAD TH) share a signature no other record has: descriptive text and a real activity list, with a null `usda_portal_url`. That signature is a usable fail-closed gate.
- Aspen has no equivalent. Its manifest has no `recreation_sites` layer, and none of `v2/overnight-options.json`, `v2/ridb-options.json`, `v2/map-data-v2.json` or `v2/destinations.json` contains a `directions` key.

## 2. How the text gets into the data

`v2/pipeline/scripts/enrich_douglas.py` (not `fetch_douglas.py`, which builds coverage, trails and roads only):

- Source: `https://apps.fs.usda.gov/arcx/rest/services/EDW/EDW_RecInfraRecreationSites_02/MapServer`, layer 0 (`:10`, `:17`), queried by the county bounding box with all fields (`:28`), required fields `objectid, site_name, site_type` (`:17`).
- Each returned row is clipped to the county (`:31`) and reduced to a fixed list of 14 attributes (`:38-39`):

```python
keep=['site_name','site_type','activity_type_list','seasonal_operational_status','op_status_reason','fee_description','open_season','usda_portal_url','rec1stop_url','important_info','restrictions','water_availability','restroom_availability','directions']
props={k:p.get(k) for k in keep};props['name']=p.get('site_name')
```

- The id is `recreation-<OBJECTID>` and one shared evidence object is attached to every feature (`:29`, `:41`).

There is no lookup by name, by ID or by portal page. `directions`, `important_info`, `restrictions`, `water_availability`, `restroom_availability` and `activity_type_list` arrive on the same source row as `site_name` and the geometry. A wrong match therefore cannot be created by this code; it can only be passed through.

How a wrong match can still occur (INFERENCE, not verified):

- The service name suggests the layer combines the agency's site inventory with descriptive text maintained for the public recreation pages. If that pairing is done upstream by something weaker than a page ID, such as a site name within an administrative unit, generic names can attach to the wrong page.
- Evidence for that in this data: all 20 records with a `usda_portal_url` have a distinct `recid` and all their text is consistent or merely ambiguous. The only 3 records that have descriptive text without a portal URL are RAMPART ENTRANCE, TURKEY and DEVILS HEAD TH, and they are the only non-campground, non-horse-camp records whose `activity_type_list` is a real list instead of `No Data`. Two of those three are wrong.
- GENERAL KNOWLEDGE, to be confirmed by research: the forest unit that manages Douglas County's national forest land also administers the Cimarron National Grassland in Kansas, which would explain how a "Turkey Trail" page from Elkhart, Kansas, is within reach of a name-based pairing for a Colorado site called TURKEY.

Join keys of the mismatched records (everything the pipeline retains):

| id | OBJECTID | `site_name` | `site_type` | `usda_portal_url` | `rec1stop_url` |
|---|---|---|---|---|---|
| `recreation-3314802` | 3314802 | RAMPART ENTRANCE | TRAILHEAD | null | null |
| `recreation-3310732` | 3310732 | TURKEY | TRAILHEAD | null | null |

No other source identifier survives. The `keep` list drops every other attribute, so the committed data cannot show which upstream key carried the text. I could not list the layer's other fields offline.

## 3. Where and how it is rendered

`v2/explore/browse.js`:

- `:43` — the browse detail runs only for trail segments and for `site_type` CAMPGROUND, TRAILHEAD or DISPERSED_AREA.
- `:52` — for those, each non-empty field that is not the literal `No Data` is printed as a heading and a paragraph. Labels: `Published restrictions`, `Important information`, `Listed activities`, `Fees (verify current price)`, `Published season (may be historical)`, `Water`, `Restrooms`, `Agency directions`.
- `:44` — the link "Official listing / source ↗" uses `rec1stop_url`, else `usda_portal_url`, else `evidence.source_url` (`:5`). For both mismatched records it falls through to the ArcGIS layer URL, so the user has no agency page to compare against.
- `:47` — "Directions to facility ↗" opens Google Maps at the record's coordinates, with the caption "Check approach roads and trailer parking before travel. Directions are for this facility, not a verified riding route." That link is coordinate-based and is not affected. The caption sits in the same panel as the wrong "Agency directions" text.
- The display artifact `v2/regions/douglas-co/display/recreation.geojson` carries the same 17 properties as the canonical file for all 36 records.

What a user sees today on RAMPART ENTRANCE (a trailhead at the north end of the `RAMPART RANGE` road line, 0.33 mi from INDIAN CREEK campground): "Important information — Drinking water is available at promontory picnic area during the summer."; "Listed activities — CAMPING, TENT | CROSS-COUNTRY SKIING, SNOWSHOEING | FISHING | …"; "Agency directions — This easy trail follows the Reservoirs shoreline … Take the Rampart Range Road north from Woodland Park …".

On TURKEY: "Listed activities — CAMPING, GENERAL DAY | HIKING | …"; "Agency directions — Travel north of Elkhart on Highway 27 to the Cottonwood Picnic Grounds …".

The contaminated activity lists matter separately: they put the word "camping" on two trailhead panels.

## 4. The two mismatches

### 4.1 RAMPART ENTRANCE (`recreation-3314802`)

In-data evidence:

- Location: -105.09412, 39.37716. It is 0.01 mi from the `RAMPART RANGE` road geometry, 0.33 mi from INDIAN CREEK campground, 0.35 mi from the INDIAN CREEK EQUESTRIAN trailhead and 17.1 miles north of the county's southern edge. Nearest trails are BEGINNER 0627 (0.07 mi) and 787 (0.12 mi).
- The text describes a reservoir shoreline trail and routes via "Woodland Park", "Hwy 24", "Colorado Springs", "Manitou Springs", "Garden of the Gods", "Forest Service Road 306" and "Rainbow Gulch Trail". None of those names occurs in any other record's directions. Every one of the other 16 non-suspect directions texts routes via Sedalia, Highway 67, Rampart Range Road, Deckers or Sprucewood.
- No waterbody named "Rampart Reservoir" exists in the Douglas `waterbodies` layer (2,135 features). The only similar name, "Aurora-Rampart Reservoir", is 5.0 miles from the record and is a different name; the text's route does not lead to it.
- No Douglas trail segment is named "Rainbow Gulch" and no road is numbered 306 in the `roads` layer names.
- `important_info` names a "promontory picnic area"; no Douglas recreation record has that name.
- `activity_type_list` includes tent camping, fishing and cross-country skiing for a `TRAILHEAD`.
- No `usda_portal_url`.

GENERAL KNOWLEDGE (not from the dataset; approximate coordinates): Rampart Reservoir and Woodland Park lie south of Douglas County, roughly 29 and 27 straight-line miles from this record.

Conclusion: the directions, important information and activity list describe a different place.

### 4.2 TURKEY (`recreation-3310732`)

In-data evidence:

- Location: -105.17501, 39.30101. It is 0.13 mi from the 677B LOG JUMPER trailhead; nearest trails are NODDLE 0677 (0.10 mi) and LOG JUMPER 0677.A (0.11 mi).
- The text names "Elkhart", "Highway 27", "Cottonwood Picnic Grounds", "Cimarron River Bridge", "Cimarron Recreation Area", "FS700 (South River Road)", "Turkey Trail" and "Wilburton Crossing". None occurs in any other record's directions.
- No waterway named "Cimarron River" exists in the Douglas `waterways` layer (2,359 features). "Cottonwood Creek" exists but the text says picnic grounds, not a creek.
- The only Douglas features with "Turkey" in the name are trail TURKEY TRACK NORTH (10.9 mi from the record), road TURKEY TRACK (11.1 mi) and Turkey Creek (10.3 mi). None is a "Turkey Trail" at this location.
- `activity_type_list` says "CAMPING, GENERAL DAY | HIKING | HIKING - MODERATE | VIEWING WILDFLOWERS | VIEWING WILDLIFE" for a trailhead that sits on motorised trail geometry.
- No `usda_portal_url`.

GENERAL KNOWLEDGE (not from the dataset; approximate coordinates): Elkhart, Kansas, is roughly 240 straight-line miles from this record.

Conclusion: the directions and activity list describe a different place.

## 5. All 18 records

Reference used for mileage checks: the RAMPART ENTRANCE point, which lies on the `RAMPART RANGE` road line near INDIAN CREEK and therefore approximates the Highway 67 junction that most texts measure from. Straight-line distances are shorter than road miles; I checked ordering, not equality.

| # | id | name | site_type | lon, lat | agency page | rendered today | class |
|---|---|---|---|---|---|---|---|
| 1 | `recreation-3295555` | DEVILS HEAD CG | CAMPGROUND | -105.10510, 39.27178 | https://www.fs.usda.gov/recarea/psicc/recarea/?recid=12925 | yes | CONSISTENT |
| 2 | `recreation-3306411` | FLAT ROCKS CG | CAMPGROUND | -105.09222, 39.32749 | https://www.fs.usda.gov/recarea/psicc/recarea/?recid=12931 | yes | CONSISTENT |
| 3 | `recreation-3296016` | INDIAN CREEK | CAMPGROUND | -105.09912, 39.38006 | https://www.fs.usda.gov/recarea/psicc/recarea/?recid=12951 | yes | CONSISTENT |
| 4 | `recreation-3295146` | OSPREY | CAMPGROUND | -105.17663, 39.34883 | https://www.fs.usda.gov/recarea/psicc/recarea/?recid=12975 | yes | CONSISTENT |
| 5 | `recreation-3316014` | OUZEL | CAMPGROUND | -105.18778, 39.32060 | https://www.fs.usda.gov/recarea/psicc/recarea/?recid=12976 | yes | CONSISTENT |
| 6 | `recreation-3304676` | INDIAN CREEK (EQUESTRIAN) | HORSE CAMP | -105.10388, 39.37862 | https://www.fs.usda.gov/recarea/psicc/recarea/?recid=12952 | no | AMBIGUOUS |
| 7 | `recreation-3305648` | FLAT ROCKS OS | OBSERVATION SITE | -105.08526, 39.32622 | https://www.fs.usda.gov/recarea/psicc/recarea/?recid=12932 | no | CONSISTENT |
| 8 | `recreation-3316544` | CABIN RIDGE PS | PICNIC SITE | -105.10586, 39.27962 | https://www.fs.usda.gov/recarea/psicc/recarea/?recid=12917 | no | CONSISTENT |
| 9 | `recreation-3311222` | DEVILS HEAD PS | PICNIC SITE | -105.10484, 39.27030 | https://www.fs.usda.gov/recarea/psicc/recarea/?recid=12926 | no | CONSISTENT |
| 10 | `recreation-3317905` | 677A NODDLE | TRAILHEAD | -105.12905, 39.32202 | https://www.fs.usda.gov/recarea/psicc/recarea/?recid=12898 | yes | AMBIGUOUS |
| 11 | `recreation-3313430` | 677B LOG JUMPER | TRAILHEAD | -105.17256, 39.30142 | https://www.fs.usda.gov/recarea/psicc/recarea/?recid=12899 | yes | AMBIGUOUS |
| 12 | `recreation-3311789` | CABIN RIDGE TH | TRAILHEAD | -105.10402, 39.28175 | https://www.fs.usda.gov/recarea/psicc/recarea/?recid=12918 | yes | CONSISTENT |
| 13 | `recreation-3314280` | DEVILS HEAD TH | TRAILHEAD | -105.10487, 39.26974 | none | yes | CONSISTENT |
| 14 | `recreation-3306075` | DUTCH FRED | TRAILHEAD | -105.09197, 39.28574 | https://www.fs.usda.gov/recarea/psicc/recarea/?recid=12930 | yes | CONSISTENT |
| 15 | `recreation-3302920` | FLAT ROCKS TH | TRAILHEAD | -105.08693, 39.32729 | https://www.fs.usda.gov/recarea/psicc/recarea/?recid=12933 | yes | CONSISTENT |
| 16 | `recreation-3304006` | GARBER CREEK | TRAILHEAD | -105.07872, 39.35814 | https://www.fs.usda.gov/recarea/psicc/recarea/?recid=12936 | yes | CONSISTENT |
| 17 | `recreation-3314802` | RAMPART ENTRANCE | TRAILHEAD | -105.09412, 39.37716 | none | yes | MISMATCH |
| 18 | `recreation-3310732` | TURKEY | TRAILHEAD | -105.17501, 39.30101 | none | yes | MISMATCH |

### 1. DEVILS HEAD CG — CONSISTENT

- id `recreation-3295555`, `site_type` CAMPGROUND, coordinates -105.10510, 39.27178
- `usda_portal_url`: https://www.fs.usda.gov/recarea/psicc/recarea/?recid=12925
- `rec1stop_url`: null
- `evidence.source_url`: https://apps.fs.usda.gov/arcx/rest/services/EDW/EDW_RecInfraRecreationSites_02/MapServer/0 (retrieved 2026-09-27T14:15:40.744887Z, method `source_fetch`, confidence `unverified`)
- Directions text, verbatim:

> To reach this area, take U.S. Highway 85 south to Sedalia. Turn west on Highway 67 for 10 miles to the junction with Rampart Range Road. Turn south onto Rampart Range Road for 10 miles. Devil s Head Campground will have a signed turn off.

- Judgement: Text names "Devil s Head Campground"; Sedalia, Highway 67, then 10 miles south on Rampart Range Road. Record is 7.3 straight-line miles from the RAMPART ENTRANCE point, which lies 0.01 mi from the `RAMPART RANGE` road line near the Highway 67 end.

### 2. FLAT ROCKS CG — CONSISTENT

- id `recreation-3306411`, `site_type` CAMPGROUND, coordinates -105.09222, 39.32749
- `usda_portal_url`: https://www.fs.usda.gov/recarea/psicc/recarea/?recid=12931
- `rec1stop_url`: https://www.recreation.gov/camping/campgrounds/10165295
- `evidence.source_url`: https://apps.fs.usda.gov/arcx/rest/services/EDW/EDW_RecInfraRecreationSites_02/MapServer/0 (retrieved 2026-09-27T14:15:40.744887Z, method `source_fetch`, confidence `unverified`)
- Directions text, verbatim:

> To reach this area, take U.S. Highway 85 south to Sedalia. Turn west on Highway 67 for 10 miles to the junction with Rampart Range Road. Turn south onto Rampart Range Road for 5 miles. Flat Rocks Campground will be on the west side of the road.

- Judgement: Names "Flat Rocks Campground", 5 miles south on Rampart Range Road, west side. Record is 3.4 straight-line miles from the road junction reference and is west of FLAT ROCKS OS and FLAT ROCKS TH.

### 3. INDIAN CREEK — CONSISTENT

- id `recreation-3296016`, `site_type` CAMPGROUND, coordinates -105.09912, 39.38006
- `usda_portal_url`: https://www.fs.usda.gov/recarea/psicc/recarea/?recid=12951
- `rec1stop_url`: https://www.recreation.gov/camping/campgrounds/233883
- `evidence.source_url`: https://apps.fs.usda.gov/arcx/rest/services/EDW/EDW_RecInfraRecreationSites_02/MapServer/0 (retrieved 2026-09-27T14:15:40.744887Z, method `source_fetch`, confidence `unverified`)
- Directions text, verbatim:

> To reach this area, take U.S. Highway 85 south to Sedalia, then take Highway 67. The Indian Creek complex is located less than a mile west of the Rampart Range Road Junction on Highway 67.

- Judgement: Names "Indian Creek complex", less than a mile west of the Rampart Range Road junction on Highway 67. Record is 0.33 mi from the RAMPART ENTRANCE point, and west of it.

### 4. OSPREY — CONSISTENT

- id `recreation-3295146`, `site_type` CAMPGROUND, coordinates -105.17663, 39.34883
- `usda_portal_url`: https://www.fs.usda.gov/recarea/psicc/recarea/?recid=12975
- `rec1stop_url`: https://www.recreation.gov/camping/campgrounds/10165515
- `evidence.source_url`: https://apps.fs.usda.gov/arcx/rest/services/EDW/EDW_RecInfraRecreationSites_02/MapServer/0 (retrieved 2026-09-27T14:15:40.744887Z, method `source_fetch`, confidence `unverified`)
- Directions text, verbatim:

> From Denver: Take U.S. Highway 285 to Pine Junction. Take south on Jefferson County Road 126 and drive for approximately 25 miles to Douglas County 67 at Deckers. Campground is located 10 miles north of Deckers on the left hand side. From Sedalia: Take U.S. Highway 67 from Sedalia to Sprucewood. Stay on 67 South (straight) until you reach pavement at the South Platte River. Go 4 mile nouth to Osprey Campground, which is on the left hand side.

- Judgement: Names "Osprey Campground"; 10 miles north of Deckers. OUZEL says 7 miles north of Deckers and OSPREY is 2.0 straight-line miles north of OUZEL. The Sedalia variant (4 miles against 1 mile) keeps the same 3-mile difference. Text has the typo "nouth".

### 5. OUZEL — CONSISTENT

- id `recreation-3316014`, `site_type` CAMPGROUND, coordinates -105.18778, 39.32060
- `usda_portal_url`: https://www.fs.usda.gov/recarea/psicc/recarea/?recid=12976
- `rec1stop_url`: https://www.recreation.gov/camping/campgrounds/10165520
- `evidence.source_url`: https://apps.fs.usda.gov/arcx/rest/services/EDW/EDW_RecInfraRecreationSites_02/MapServer/0 (retrieved 2026-09-27T14:15:40.744887Z, method `source_fetch`, confidence `unverified`)
- Directions text, verbatim:

> From Denver: Take U.S. Highway 285 to Pine Junction. Take south on Jefferson County Road 126 and drive for approximately 25 miles to Douglas County 67 at Deckers. Campground is located 7 miles north of Deckers on the left hand side. From Sedalia: Take U.S. Highway 67 from Sedalia to Sprucewood. Stay on 67 South (straight) until you reach pavement at the South Platte River. Go 1 mile nouth to Ouzel Campground, which is on the left hand side.

- Judgement: Names "Ouzel Campground"; ordering against OSPREY is consistent (see OSPREY).

### 6. INDIAN CREEK (EQUESTRIAN) — AMBIGUOUS

- id `recreation-3304676`, `site_type` HORSE CAMP, coordinates -105.10388, 39.37862
- `usda_portal_url`: https://www.fs.usda.gov/recarea/psicc/recarea/?recid=12952
- `rec1stop_url`: null
- `evidence.source_url`: https://apps.fs.usda.gov/arcx/rest/services/EDW/EDW_RecInfraRecreationSites_02/MapServer/0 (retrieved 2026-09-27T14:15:40.744887Z, method `source_fetch`, confidence `unverified`)
- Directions text, verbatim:

> Drive south from Denver, Colorado on U.S. Hwy 85 (Santa Fe St.) to Sedalia. Turn right (west) onto Douglas County Road 67. Drive on Hwy 67 slightly over 10 miles (from Sedalia) to the Indian Creek Campground, which is located approximately 2 miles. Turn right into the campground. There is a small fee parking area outside the campground. The trailhead is just to the right of the parking area. Both the Indian Creek Campground and the Equestrian Campground are fee areas–even for parking.

- Judgement: Text routes to "the Indian Creek Campground" and then describes "the trailhead ... just to the right of the parking area"; it reads as written for the trailhead or the complex, not the horse camp. The mileage sentence is garbled ("slightly over 10 miles ... which is located approximately 2 miles"). Place and road names match the location (0.27 mi from INDIAN CREEK campground, on the `INDIAN CREEK EQUESTRIAN` road line). A separate TRAILHEAD record, INDIAN CREEK EQUESTRIAN (recid 12953), has no directions. Not rendered today (HORSE CAMP).

### 7. FLAT ROCKS OS — CONSISTENT

- id `recreation-3305648`, `site_type` OBSERVATION SITE, coordinates -105.08526, 39.32622
- `usda_portal_url`: https://www.fs.usda.gov/recarea/psicc/recarea/?recid=12932
- `rec1stop_url`: null
- `evidence.source_url`: https://apps.fs.usda.gov/arcx/rest/services/EDW/EDW_RecInfraRecreationSites_02/MapServer/0 (retrieved 2026-09-27T14:15:40.744887Z, method `source_fetch`, confidence `unverified`)
- Directions text, verbatim:

> To reach this area, take U.S. Highway 85 south to Sedalia. Turn west on Highway 67 for 10 miles to the junction with Rampart Range Road. Turn south onto Rampart Range Road for 5 miles. Located on the east side of the Rampart Range Road just south of Flat Rocks Campground.

- Judgement: East side of Rampart Range Road, just south of Flat Rocks Campground. Record is east and slightly south of FLAT ROCKS CG (0.38 mi). Not rendered today (OBSERVATION SITE).

### 8. CABIN RIDGE PS — CONSISTENT

- id `recreation-3316544`, `site_type` PICNIC SITE, coordinates -105.10586, 39.27962
- `usda_portal_url`: https://www.fs.usda.gov/recarea/psicc/recarea/?recid=12917
- `rec1stop_url`: null
- `evidence.source_url`: https://apps.fs.usda.gov/arcx/rest/services/EDW/EDW_RecInfraRecreationSites_02/MapServer/0 (retrieved 2026-09-27T14:15:40.744887Z, method `source_fetch`, confidence `unverified`)
- Directions text, verbatim:

> To access the Cabin Ridge picnic area from Denver: Travel south on Highway 85 / Santa Fe 10 miles to the town of Sedalia. Turn west on Highway 67 and travel 10 miles west. When you get to the Rampart Range Road, turn south and continue 9.5 miles to the Cabin Ridge Picnic Area.

- Judgement: Names "Cabin Ridge Picnic Area", 9.5 miles south on Rampart Range Road; same route and mileage as CABIN RIDGE TH, 0.18 mi away. Not rendered today (PICNIC SITE).

### 9. DEVILS HEAD PS — CONSISTENT

- id `recreation-3311222`, `site_type` PICNIC SITE, coordinates -105.10484, 39.27030
- `usda_portal_url`: https://www.fs.usda.gov/recarea/psicc/recarea/?recid=12926
- `rec1stop_url`: null
- `evidence.source_url`: https://apps.fs.usda.gov/arcx/rest/services/EDW/EDW_RecInfraRecreationSites_02/MapServer/0 (retrieved 2026-09-27T14:15:40.744887Z, method `source_fetch`, confidence `unverified`)
- Directions text, verbatim:

> To reach this area, take U.S. Highway 85 (Evans) south to Sedalia. Turn west on Highway 67 for 10 miles to the junction with Rampart Range Road (NFSR 300). Devil s Head Picnic Area is located approximately 10 miles south on Rampart Range Road.

- Judgement: Names "Devil s Head Picnic Area", about 10 miles south on Rampart Range Road; 0.04 mi from DEVILS HEAD TH. Not rendered today (PICNIC SITE). Field-level query: `water_availability` is "Yes" here while DEVILS HEAD CG, 0.14 mi away, says "No water" and "No water on site."

### 10. 677A NODDLE — AMBIGUOUS

- id `recreation-3317905`, `site_type` TRAILHEAD, coordinates -105.12905, 39.32202
- `usda_portal_url`: https://www.fs.usda.gov/recarea/psicc/recarea/?recid=12898
- `rec1stop_url`: null
- `evidence.source_url`: https://apps.fs.usda.gov/arcx/rest/services/EDW/EDW_RecInfraRecreationSites_02/MapServer/0 (retrieved 2026-09-27T14:15:40.744887Z, method `source_fetch`, confidence `unverified`)
- Directions text, verbatim:

> From Denver, travel Hwy 85/Santa Fe South for 10 miles to Sedalia. Turn west on Hwy 67 for 14 miles to Sprucewood. Stay straight on Hwy 67 south for 2.5 miles.

- Judgement: Text names no site and stops mid-route ("Stay straight on Hwy 67 south for 2.5 miles."). Route (Sedalia, Hwy 67, Sprucewood) fits the area, and the 2.5 against 6.5 miles for 677B LOG JUMPER fits their relative positions (LOG JUMPER lies 2.7 straight-line miles further south-west). Nothing in the text ties it to this record by name. Nearest trail geometry is NODDLE 0677.

### 11. 677B LOG JUMPER — AMBIGUOUS

- id `recreation-3313430`, `site_type` TRAILHEAD, coordinates -105.17256, 39.30142
- `usda_portal_url`: https://www.fs.usda.gov/recarea/psicc/recarea/?recid=12899
- `rec1stop_url`: null
- `evidence.source_url`: https://apps.fs.usda.gov/arcx/rest/services/EDW/EDW_RecInfraRecreationSites_02/MapServer/0 (retrieved 2026-09-27T14:15:40.744887Z, method `source_fetch`, confidence `unverified`)
- Directions text, verbatim:

> From Denver, travel south on Hwy 85/ Santa Fe drive 10 miles to Sedalia.  Travel west on Hwy 67 for 14 miles to Sprucewood. Continue south on Hwy 67 for 6.5 miles.

- Judgement: Same pattern as 677A NODDLE: no site name, route ends "Continue south on Hwy 67 for 6.5 miles." The TURKEY record is 0.13 mi away; the nearest trail geometry to both is NODDLE 0677 and LOG JUMPER 0677.A.

### 12. CABIN RIDGE TH — CONSISTENT

- id `recreation-3311789`, `site_type` TRAILHEAD, coordinates -105.10402, 39.28175
- `usda_portal_url`: https://www.fs.usda.gov/recarea/psicc/recarea/?recid=12918
- `rec1stop_url`: null
- `evidence.source_url`: https://apps.fs.usda.gov/arcx/rest/services/EDW/EDW_RecInfraRecreationSites_02/MapServer/0 (retrieved 2026-09-27T14:15:40.744887Z, method `source_fetch`, confidence `unverified`)
- Directions text, verbatim:

> To access the Cabin Ridge Trailhead from Denver: Travel south on Highway 85 (Santa Fe) 10 miles to the town of Sedalia. Turn west on Highway 67 and travel 10 miles west. When you get to the Rampart Range Road, turn south and continue 9.5 miles to the Cabin Ridge Trailhead.

- Judgement: Names "Cabin Ridge Trailhead", 9.5 miles south on Rampart Range Road.

### 13. DEVILS HEAD TH — CONSISTENT

- id `recreation-3314280`, `site_type` TRAILHEAD, coordinates -105.10487, 39.26974
- `usda_portal_url`: null
- `rec1stop_url`: null
- `evidence.source_url`: https://apps.fs.usda.gov/arcx/rest/services/EDW/EDW_RecInfraRecreationSites_02/MapServer/0 (retrieved 2026-09-27T14:15:40.744887Z, method `source_fetch`, confidence `unverified`)
- Directions text, verbatim:

> Devils Head Lookout Trail can be reached by traveling approximately ten miles west of Sedalia on Highway 67 to the Rampart Range Road. Turn left (south) on the Rampart Range Road for approximately eight and one-half miles to the trailhead. Park your car in the picnic area to begin the hike.

- Judgement: Names "Devils Head Lookout Trail" and "Park your car in the picnic area"; record is 0.03 mi from trail DEVILS HEAD 611 and 0.04 mi from DEVILS HEAD PS. Two cautions. It says "approximately eight and one-half miles" on Rampart Range Road where DEVILS HEAD CG and PS say 10 and CABIN RIDGE, 0.7 to 0.8 mi further north, says 9.5. And it shares the signature of the two mismatches: descriptive text and an activity list but no portal URL.

### 14. DUTCH FRED — CONSISTENT

- id `recreation-3306075`, `site_type` TRAILHEAD, coordinates -105.09197, 39.28574
- `usda_portal_url`: https://www.fs.usda.gov/recarea/psicc/recarea/?recid=12930
- `rec1stop_url`: null
- `evidence.source_url`: https://apps.fs.usda.gov/arcx/rest/services/EDW/EDW_RecInfraRecreationSites_02/MapServer/0 (retrieved 2026-09-27T14:15:40.744887Z, method `source_fetch`, confidence `unverified`)
- Directions text, verbatim:

> To reach this area, take U.S. Highway 85 (Santa Fe) south to Sedalia. Turn west on Highway 67 for 10 miles to the junction with Rampart Range Road. Dutch Fred Trailhead is located approximately 8 miles from south of Rampart Range Road.

- Judgement: Names "Dutch Fred Trailhead", about 8 miles along Rampart Range Road; 6.3 straight-line miles from the junction reference, between FLAT ROCKS (6) and CABIN RIDGE (9.5). Wording is garbled ("from south of Rampart Range Road").

### 15. FLAT ROCKS TH — CONSISTENT

- id `recreation-3302920`, `site_type` TRAILHEAD, coordinates -105.08693, 39.32729
- `usda_portal_url`: https://www.fs.usda.gov/recarea/psicc/recarea/?recid=12933
- `rec1stop_url`: null
- `evidence.source_url`: https://apps.fs.usda.gov/arcx/rest/services/EDW/EDW_RecInfraRecreationSites_02/MapServer/0 (retrieved 2026-09-27T14:15:40.744887Z, method `source_fetch`, confidence `unverified`)
- Directions text, verbatim:

> To reach this area, take U.S. Highway 85 (Santa Fe) south to Sedalia. Turn west on Highway 67 for 10 miles to the junction with Rampart Range Road. Flat Rock Trailhead is located approximately 6 miles from south of Rampart Range Road.

- Judgement: Names "Flat Rock Trailhead", about 6 miles; FLAT ROCKS CG says 5 miles and is 0.28 mi away.

### 16. GARBER CREEK — CONSISTENT

- id `recreation-3304006`, `site_type` TRAILHEAD, coordinates -105.07872, 39.35814
- `usda_portal_url`: https://www.fs.usda.gov/recarea/psicc/recarea/?recid=12936
- `rec1stop_url`: null
- `evidence.source_url`: https://apps.fs.usda.gov/arcx/rest/services/EDW/EDW_RecInfraRecreationSites_02/MapServer/0 (retrieved 2026-09-27T14:15:40.744887Z, method `source_fetch`, confidence `unverified`)
- Directions text, verbatim:

> To reach this area, take U.S. Highway 85 (Santa Fe) south to Sedalia. Turn west on Highway 67 for 10 miles to the junction with Rampart Range Road. Trailhead is located approximately 3 miles from south of Rampart Range Road.

- Judgement: Does not name the site ("Trailhead is located approximately 3 miles") but the mileage fits: 1.6 straight-line miles from the junction reference, the first site south of it with directions.

### 17. RAMPART ENTRANCE — MISMATCH

- id `recreation-3314802`, `site_type` TRAILHEAD, coordinates -105.09412, 39.37716
- `usda_portal_url`: null
- `rec1stop_url`: null
- `evidence.source_url`: https://apps.fs.usda.gov/arcx/rest/services/EDW/EDW_RecInfraRecreationSites_02/MapServer/0 (retrieved 2026-09-27T14:15:40.744887Z, method `source_fetch`, confidence `unverified`)
- Directions text, verbatim:

> This easy trail follows the Reservoirs shoreline providing opportunities for fishing access, picnicking and enjoying the beauty of the area.
>
> 1. Take the Rampart Range Road north from Woodland Park (turn off Hwy 24 at McDonalds).This road will take you past the Woodland Park schools and a portion of Woodland Park`s residential area. Follow the signs to Rampart Reservoir.
>
> 2. (From Colorado Springs) If you are looking for a scenic drive prior to your hike, the Rampart Range Road offers scenic vistas of Colorado Springs and many canyons. Take the Manitou Springs exit as if going to Garden of the Gods. After going past "Balanced Rock" a sign on the left will indicate the Rampart Range Road. This route should be chosen only if you have an extra hour of driving time.
>
> During the winter, Forest Service Road 306 to Rampart Reservoir is closed with a gate. Additional cross country ski access is via Rainbow Gulch Trail which begins on Rampart Range Road a little west of road 306.

- Judgement: See section 4.1.

### 18. TURKEY — MISMATCH

- id `recreation-3310732`, `site_type` TRAILHEAD, coordinates -105.17501, 39.30101
- `usda_portal_url`: null
- `rec1stop_url`: null
- `evidence.source_url`: https://apps.fs.usda.gov/arcx/rest/services/EDW/EDW_RecInfraRecreationSites_02/MapServer/0 (retrieved 2026-09-27T14:15:40.744887Z, method `source_fetch`, confidence `unverified`)
- Directions text, verbatim:

> Travel north of Elkhart on Highway 27 to the Cottonwood Picnic Grounds (just south of the Cimarron River Bridge). Vehicles may be parked at the Picnic Grounds. Some visitors choose to pick up the Turkey Trail at the Cimarron Recreation Area, 4 miles east of Highway 27 on FS700 (South River Road). Restrooms are available at the Cottonwood picnic Ground and the Cimarron Recreation Area. The Turkey Trail begins at the far eastern end of Cottonwood Picnic Grounds near the southern end of the Cimarron River bridge on highway 27.  The trail ends one mile east of Wilburton Crossing.

- Judgement: See section 4.2.


## 6. Other fields that look copied or inconsistent

Checked across all 36 records: `important_info`, `water_availability`, `restroom_availability`, `restrictions`, `activity_type_list`, `open_season`, `fee_description`.

- No directions text is shared verbatim by two records.
- Shared `restrictions` text, each plausibly a deliberate area-wide notice: OSPREY and OUZEL (riverside campground rules); DEVILS HEAD PS and CABIN RIDGE PS (picnic rules, "Overnight use prohibited"); 677A NODDLE and 677B LOG JUMPER (Rampart Range Motorized Recreation Area rules). Four more trailheads carry near-identical variants of the motorised-area notice.
- RAMPART ENTRANCE `important_info` and `activity_type_list`: foreign (section 4.1).
- TURKEY `activity_type_list`: foreign (section 4.2).
- DEVILS HEAD PS `water_availability` "Yes" against DEVILS HEAD CG "No water" and "No water on site.", 0.14 mi apart. Could be true or copied; needs the agency page.
- OUZEL `restroom_availability` "Vault toilet" against its own `important_info` "Portable toilets available during full service camping." Internal conflict.
- INDIAN CREEK `water_availability` "Yes" against its own `important_info` "Water availability is questionable …". Internal conflict the app shows side by side.
- RIM ROAD `restrictions` contains unrendered database escape text: `driver'||chr(38)||'rsquo;s` and `50'||chr(38)||'rdquo;`. It is shown verbatim today (TRAILHEAD).
- `open_season` values carry a year on 7 records ("May 28, 2021", "May 1, 2021", "January 1, 2021"), which dates the descriptive text.
- `seasonal_operational_status` is `OPEN` on 35 records and `CLOSED` on 1; it is not rendered (see the site facts packet).

## 7. Remediation and tests (not implemented)

Fail-closed display, in order of preference:

1. Render descriptive text (`directions`, `important_info`, `activity_type_list`, `restrictions`, `water_availability`, `restroom_availability`, `fee_description`, `open_season`) only when the record has an agency page URL (`usda_portal_url` or `rec1stop_url`) that the text can be checked against, and always show that link beside it. Otherwise show: `The source record carries descriptive text that could not be tied to an agency page for this site. It is not shown.` On this snapshot the gate withholds text on 4 of 36 records: RAMPART ENTRANCE, TURKEY, DEVILS HEAD TH and DAKAN (a day use area whose only descriptive value is restrooms "One CXT double", not rendered today).
2. Relabel `Agency directions` as `Directions text published in the source record (not checked against this location)`.
3. Keep the coordinate-based "Directions to facility" link; it does not depend on the text.

The URL gate is a heuristic that happens to separate the bad records in this snapshot. It is not proof that text on a record with a URL is right, which is why the three AMBIGUOUS records still need a human check.

Pipeline:

- Retain the source's own identifiers for each row (site and recreation-area keys, whatever the layer exposes) so the pairing can be audited. This adds `fields.source` entries to `v2/regions/douglas-co/region.json` and the contract table in `docs/specs/M2-regional-data-contract.md:380`.
- Add a reviewed quarantine list keyed by `recreation-<OBJECTID>`, applied in `enrich_douglas.py`, that nulls the descriptive fields for named records and records why. Do not auto-correct or re-pair text.
- Add a non-blocking integrity report at fetch time: records with descriptive text and no portal URL; records whose directions share no token with `site_name` and no road or town token with the regional majority. Report for review, never decide automatically.
- Report upstream to the agency once research confirms the pages.

Tests:

- Node unit test on the browse detail (or an extracted pure function): a record with text and no agency URL renders the withheld notice and none of the eight labelled fields.
- Published-data test: no rendered descriptive text on a record without an agency URL; pin `recreation-3314802` and `recreation-3310732` as withheld.
- Browser check: open RAMPART ENTRANCE and assert "Woodland Park" and "promontory" are absent.
- Python test for the quarantine list in `v2/pipeline/tests/test_douglas.py`.

Files a fix would touch: `v2/explore/browse.js:5`, `:44`, `:52`; optionally `v2/pipeline/scripts/enrich_douglas.py:38-42`; `v2/regions/douglas-co/region.json` and `display/recreation.geojson` only if fields are added or data is regenerated; the tests above.

## 8. Records for the research worker to verify against the agency page

| priority | record | id | what to check | URL in the data |
|---|---|---|---|---|
| 1 | RAMPART ENTRANCE | `recreation-3314802` | Which agency page the text belongs to; whether this trailhead has a page at all | none (`evidence.source_url` is the ArcGIS layer) |
| 1 | TURKEY | `recreation-3310732` | Same; whether the site exists under this name near Log Jumper | none |
| 2 | DEVILS HEAD TH | `recreation-3314280` | Text has no page URL; confirm it and the 8.5-mile figure | none; sibling pages https://www.fs.usda.gov/recarea/psicc/recarea/?recid=12925 and https://www.fs.usda.gov/recarea/psicc/recarea/?recid=12926 |
| 2 | 677A NODDLE | `recreation-3317905` | Directions name no site; confirm they are this page's | https://www.fs.usda.gov/recarea/psicc/recarea/?recid=12898 |
| 2 | 677B LOG JUMPER | `recreation-3313430` | Same | https://www.fs.usda.gov/recarea/psicc/recarea/?recid=12899 |
| 2 | INDIAN CREEK (EQUESTRIAN) | `recreation-3304676` | Directions read as trailhead text; compare with recid 12953 | https://www.fs.usda.gov/recarea/psicc/recarea/?recid=12952 and https://www.fs.usda.gov/recarea/psicc/recarea/?recid=12953 |
| 3 | DEVILS HEAD PS | `recreation-3311222` | Water "Yes" against the campground's "No water" | https://www.fs.usda.gov/recarea/psicc/recarea/?recid=12926 |
| 3 | OUZEL | `recreation-3316014` | Vault against portable toilets | https://www.fs.usda.gov/recarea/psicc/recarea/?recid=12976 |
| 3 | RIM ROAD | `recreation-3307758` | Escape artefacts in restrictions text | https://www.fs.usda.gov/recarea/psicc/recarea/?recid=12983 |

## 9. Could not determine

- Whether the wrong text is in the live ArcGIS row today or was specific to the 2026-09-27 retrieval. No network.
- The upstream key that pairs a site row with descriptive text. The pipeline keeps no source identifier beyond OBJECTID.
- Whether the committed file was produced by the committed script (the repository history shows upload commits).
- Whether the portal URLs resolve; they were not opened.
