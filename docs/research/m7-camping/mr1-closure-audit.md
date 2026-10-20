> **Status: research record (2026-10-20). Audit classifications, not surveyed legal-boundary determinations.** OVERLAPS, POSSIBLE and NO EVIDENCE describe how the stated scope of each order compares with Ohvernight's computed polygons. The comparison uses USGS road centrelines and PLSS sections; no order exhibit was georeferenced. NO EVIDENCE never establishes camping permission.
>
> **Owner decision 2026-10-20 (M7-MR1): interim presentation mitigation authorized.** The whole "Areas to research" layer is to be removed from Aspen's user-facing discovery now (separate narrow PR). The canonical data, attribution, this evidence and the generation pipeline are preserved for M7. The underlying logic still requires permanent retirement or replacement in M7 (M7-D14).

# MR1 bounded evidence audit: Aspen "Areas to research" vs in-force camping orders

- Task: `task_9b085e58398d`. Owner direction 2026-10-20 (M7 PR #47, MR1).
- Auditor: Claude worker. Repository read at `origin/main` `3965dbf`, read-only.
- Agency pages read on 2026-10-20 with plain GETs; about 36 requests in all (the fetch log is in section 7).
- Status: **unreviewed research.** This is not a legal determination. Nothing here says camping is allowed anywhere. "NO EVIDENCE" means only that I found no in-force order whose stated scope covers the polygon.

## 1. Summary

All 51 polygons in `dispersed_corridors` ("Areas to research", `default_on: true`) were checked. `dispersed_corridor_points` has 0 features, so there was nothing to check there.

| Class | Count | Meaning in this audit |
|---|---:|---|
| **OVERLAPS** | **32** | The stated scope of an in-force order that prohibits or restricts camping area-wide covers the polygon, wholly or partly. Coverage was matched by a named campground or Described Area, or measured against a named road corridor or lake (method in section 3). |
| **POSSIBLE** | **10** | An order's scope may cover the polygon, but I cannot resolve it without the order's map registered to ground, legal road geometry, or the district line. |
| **NO EVIDENCE** | **9** | I located no in-force order whose area-wide scope covers the polygon. **This does not mean camping is allowed.** 3 of these 9 still partly overlap the forest-wide 100 ft trail setback (O5). |
| Total | 51 | |

Further findings:

- **The producer aims at restricted ground by construction.** It buffers every `designated_open` MVUM road by 300 ft. In Aspen most of those roads are short spurs that serve developed campgrounds, trailheads and the Maroon Lake parking lots. These are the exact places the district's orders protect. 30 of the 51 polygons are named after a campground, trailhead, parking, day-use, picnic-ground or administrative-site spur. 28 of those 30 are OVERLAPS; the other 2 are Emerald Lake PG (POSSIBLE) and Aspen Admin. Site (NO EVIDENCE).
- **Setback orders hit part of the polygons as well.**
  - WRNF Order 2026-13 (in force since 2026-07-01) prohibits camping within 100 ft of any National Forest System trail. Water is covered too, but the builder already removes it. Mapped USFS trails fall within 100 ft of 0.4 % to 35.4 % of the area of 25 polygons that touch WRNF, including 3 NO EVIDENCE ones.
  - Order WRNF 1996-08 prohibits camping within 300 ft of any Aspen Ranger District trailhead. 5 polygons are named trailhead spurs.
  - The builder subtracts neither the trail setback nor the trailhead setback.
- **Forests:** the 51 polygons span four ranger districts. 37 are in WRNF Aspen RD only (Aspen Admin. Site is 92.7 % in it, with the rest outside any district polygon). 2 are in WRNF Sopris RD only. 5 are in GMUG Gunnison RD only. 1 is in PSICC Leadville RD. 6 straddle a district line: Aspen/Gunnison 4 and Sopris/Gunnison 2. The pipeline treats Aspen as White River only, so orders from two other forests apply to its data unseen. **No polygon is on BLM land**, so I did not look at BLM orders.
- **Recommendation:** remove the layer from display now as a whole-layer fail-closed step, then finish M7-D14 removal from data in M7-B (option b, sequenced). Section 5 gives the reasoning, the bear cases and the literals that need owner approval.

## 2. Method

1. **Inventory.**
   - Polygons come from `origin/main:v2/regions/aspen/display/dispersed_corridors.geojson`.
   - `source_route_id` comes from the matching `mvum_roads` feature (`source_road_id` → `id`). It is the MVUM internal ID, not the signed road number; I did not decode it.
   - Bboxes come from the polygon coordinates.
   - Districts come from intersecting each polygon with USFS EDW ranger-district polygons (`EDW_RangerDistricts_03/MapServer/1`, generalized to 0.0002°, about 20 m) and are reported as % of area.
   - PLSS sections come from BLM CadNSDI first-division polygons. Many sections here are unsurveyed or protracted, and numbers above 36 are BLM lot or protracted identifiers.
2. **Orders.** I listed every alert on the WRNF, GMUG and PSICC alert indexes. I then read the full HTML order text of each camping-related order that could reach the polygons. I read two map exhibits as PDFs: Aspen 2025-07 Exhibit A and GMUG-2022-10. All other signed PDFs and exhibits were not read.
3. **Translating order text to geometry** (planar, UTM 13N; ¼ mi = 402.3 m, ½ mi = 804.7 m, 100 ft = 30.5 m). Road centrelines are **USGS National Map transportation** features, not legal or surveyed geometry:
   - SH 82: `state_route = 82` (layers 30–31), keeping only segments that reach east of −106.785°. This approximates "beginning and including the Difficult Picnic Area".
   - CR 23: the "LINCOLN CREEK" road.
   - CR 15: the "CASTLE CREEK" road, plus "PEARL PASS".
   - CR 13 / NFSR 125: the "MAROON LAKE" road.
   - CR 4: the "FRYING PAN" road.
   - Maroon Lake: the NHD waterbody polygon in `hydrology.geojson`.
   - Trails for O5: `trails.geojson` (USFS published trails).
   - For each polygon I computed the % of its area inside each buffer.
   - "Within ¼ mile outside of X Campground" was matched **by name**: the polygon is the 300 ft buffer of the MVUM spur named after that campground, so all of its land outside the campground lies within 300 ft of the spur, which is less than ¼ mile. The Wildwood W½ was split at the section's bbox mid-longitude.
   - GMUG-2022-10 states its area only as a township/range envelope plus a map. Inside the envelope, a polygon is POSSIBLE. Outside it, the order gives NO EVIDENCE.
4. **Classification.** Each polygon's class is the strongest result across the area-wide orders: O2, O3, O4 and O7 to O11. The setback orders O5 and O6 are reported in a separate column, because they cover only part of every polygon they touch. O5 applies only to the part of a polygon inside WRNF.
5. **What I did not do.**
   - I did not register any exhibit map to coordinates.
   - I did not read the signed PDFs except the GMUG one.
   - I did not decide whether the developed-campground interiors inside some polygons may be camped in. That is governed by campground operation and is not a permission this audit can give.
   - I did not compute permission anywhere.

## 3. Per-polygon table

The "basis" column cites the ledger IDs in section 4. Percentages are shares of polygon area.

| # | id | name | MVUM source_route_id | bbox (W,S,E,N) | district(s) (% area) | PLSS | class | basis | setback overlap (part of polygon) |
|---|---|---|---|---|---|---|---|---|---|
| 1 | `candidate-mvum-13509408` | BRAILLE TRAILHEAD | 553010314 | -106.649, 39.1248, -106.6458, 39.1268 | Aspen RD 100.0 | T11S R83W S03 | **OVERLAPS** | O2 SH 82 Corridor: 100.0% ≤¼ mi of SH 82 east of Difficult | O5: 35.4% ≤100 ft of mapped NFS trail; O6: trailhead spur (by name) |
| 2 | `candidate-mvum-13460994` | CATHEDRAL LAKE | 567010314 | -106.8083, 39.0407, -106.8026, 39.0453 | Aspen RD 100.0 | T11S R84W S31, T11S R84W S52, T12S R84W S05, T12S R84W S06 … | **OVERLAPS** | O2 Castle Creek Road Corridor: 89.7% ≤¼ mi of USGS "CASTLE CREEK" road (CR 15); also touches T11S R84W S31 (Ashcroft Townsite sections: POSSIBLE) | — |
| 3 | `candidate-mvum-13466193` | CATHEDRAL LAKE | 567010314 | -106.8093, 39.042, -106.8062, 39.0459 | Aspen RD 100.0 | T11S R84W S31, T11S R84W S52, T12S R84W S06, T12S R84W S41 | **OVERLAPS** | O2 Castle Creek Road Corridor: 42.0% ≤¼ mi of USGS "CASTLE CREEK" road (CR 15); also touches T11S R84W S31 (Ashcroft Townsite sections: POSSIBLE) | O5: 10.1% ≤100 ft of mapped NFS trail |
| 4 | `candidate-mvum-13460857` | DIFFICULT CAMPGROUND | 508723010602 | -106.7746, 39.1408, -106.7714, 39.1432 | Aspen RD 100.0 | T10S R84W S33 | **OVERLAPS** | O2 "Difficult Described Area" (¼ mi outside Difficult CG) by name; 100.0% of area ≤¼ mi of SH 82 (O2 SH 82 Corridor) | — |
| 5 | `candidate-mvum-13460926` | DIFFICULT CAMPGROUND | 508718010602 | -106.7749, 39.1397, -106.7699, 39.1436 | Aspen RD 100.0 | T10S R84W S33 | **OVERLAPS** | O2 "Difficult Described Area" (¼ mi outside Difficult CG) by name; 100.0% of area ≤¼ mi of SH 82 (O2 SH 82 Corridor) | — |
| 6 | `candidate-mvum-13461277` | DIFFICULT CAMPGROUND | 508722010602 | -106.7753, 39.1403, -106.7725, 39.1432 | Aspen RD 100.0 | T10S R84W S33 | **OVERLAPS** | O2 "Difficult Described Area" (¼ mi outside Difficult CG) by name; 93.4% of area ≤¼ mi of SH 82 (O2 SH 82 Corridor) | O5: 6.4% ≤100 ft of mapped NFS trail |
| 7 | `candidate-mvum-13462631` | DIFFICULT CAMPGROUND | 508721010602 | -106.7735, 39.1397, -106.7707, 39.1423 | Aspen RD 100.0 | T10S R84W S33 | **OVERLAPS** | O2 "Difficult Described Area" (¼ mi outside Difficult CG) by name; 100.0% of area ≤¼ mi of SH 82 (O2 SH 82 Corridor) | — |
| 8 | `candidate-mvum-13464932` | DIFFICULT CAMPGROUND | 508720010602 | -106.7758, 39.1403, -106.7732, 39.1424 | Aspen RD 100.0 | T10S R84W S33 | **OVERLAPS** | O2 "Difficult Described Area" (¼ mi outside Difficult CG) by name; 80.1% of area ≤¼ mi of SH 82 (O2 SH 82 Corridor) | O5: 12.5% ≤100 ft of mapped NFS trail |
| 9 | `candidate-mvum-13465565` | DIFFICULT CAMPGROUND | 508719010602 | -106.7754, 39.1402, -106.7732, 39.142 | Aspen RD 100.0 | T10S R84W S33 | **OVERLAPS** | O2 "Difficult Described Area" (¼ mi outside Difficult CG) by name; 69.8% of area ≤¼ mi of SH 82 (O2 SH 82 Corridor) | O5: 22.6% ≤100 ft of mapped NFS trail |
| 10 | `candidate-mvum-13465567` | DIFFICULT CAMPGROUND | 508725010602 | -106.7753, 39.1418, -106.773, 39.1436 | Aspen RD 100.0 | T10S R84W S33 | **OVERLAPS** | O2 "Difficult Described Area" (¼ mi outside Difficult CG) by name; 100.0% of area ≤¼ mi of SH 82 (O2 SH 82 Corridor) | — |
| 11 | `candidate-mvum-13466061` | DIFFICULT CAMPGROUND | 508714010602 | -106.7739, 39.139, -106.7704, 39.1423 | Aspen RD 100.0 | T10S R84W S33 | **OVERLAPS** | O2 "Difficult Described Area" (¼ mi outside Difficult CG) by name; 99.7% of area ≤¼ mi of SH 82 (O2 SH 82 Corridor) | — |
| 12 | `candidate-mvum-13466146` | DIFFICULT CAMPGROUND | 508726010602 | -106.775, 39.1416, -106.7725, 39.1436 | Aspen RD 100.0 | T10S R84W S33 | **OVERLAPS** | O2 "Difficult Described Area" (¼ mi outside Difficult CG) by name; 100.0% of area ≤¼ mi of SH 82 (O2 SH 82 Corridor) | — |
| 13 | `candidate-mvum-13466506` | DIFFICULT CAMPGROUND | 20010314 | -106.7827, 39.142, -106.7729, 39.1496 | Aspen RD 100.0 | T10S R84W S28, T10S R84W S33 | **OVERLAPS** | O2 "Difficult Described Area" (¼ mi outside Difficult CG) by name; 100.0% of area ≤¼ mi of SH 82 (O2 SH 82 Corridor) | — |
| 14 | `candidate-mvum-13465168` | EAST MAROON TRAILHEAD | 565010314 | -106.9061, 39.1239, -106.9031, 39.1277 | Aspen RD 100.0 | T11S R85W S05 | **OVERLAPS** | O3/O2: 100.0% ≤¼ mi of USGS "MAROON LAKE" road (taken as Maroon Creek Rd / CR 13); West Maroon 0.0% ≤½ mi of lake | O5: 5.4% ≤100 ft of mapped NFS trail; O6: trailhead spur (by name) |
| 15 | `candidate-mvum-13465578` | GROTTOS PARKING LOT | 552010314 | -106.7047, 39.1179, -106.7023, 39.1203 | Aspen RD 100.0 | T11S R83W S06 | **OVERLAPS** | O2 SH 82 Corridor: 100.0% ≤¼ mi of SH 82 east of Difficult | — |
| 16 | `candidate-mvum-13461518` | INDEPENDENCE GRAVEL PIT | 557010314 | -106.6443, 39.1252, -106.6416, 39.1286 | Aspen RD 100.0 | T11S R83W S03 | **OVERLAPS** | O2 SH 82 Corridor: 100.0% ≤¼ mi of SH 82 east of Difficult | — |
| 17 | `candidate-mvum-13465530` | LINCOLN GULCH CAMPGROUND | 16010314 | -106.6968, 39.1162, -106.6913, 39.1181 | Aspen RD 100.0 | T11S R83W S05, T11S R83W S06, T11S R83W S07, T11S R83W S08 | **OVERLAPS** | O2 SH 82 Corridor 100.0% and Lincoln Creek Corridor 100.0% | O5: 6.0% ≤100 ft of mapped NFS trail |
| 18 | `candidate-mvum-13464940` | LOST MAN CAMPGROUND | 550010314 | -106.6262, 39.12, -106.6234, 39.1225 | Aspen RD 100.0 | T11S R83W S02 | **OVERLAPS** | O2 "Lostman Described Area" by name; SH 82 Corridor 100.0% | O5: 21.1% ≤100 ft of mapped NFS trail |
| 19 | `candidate-mvum-13466056` | LOST MAN TRAILHEAD | 6525010314 | -106.625, 39.1209, -106.6225, 39.1229 | Aspen RD 100.0 | T11S R83W S02 | **OVERLAPS** | O2 SH 82 Corridor: 100.0% ≤¼ mi of SH 82 east of Difficult | O5: 15.7% ≤100 ft of mapped NFS trail; O6: trailhead spur (by name) |
| 20 | `candidate-mvum-13461274` | MAROON LAKE | 566010314 | -106.9434, 39.0986, -106.9404, 39.1006 | Aspen RD 100.0 | T11S R86W S13 | **OVERLAPS** | O3: 100.0% ≤½ mi of Maroon Lake (NHD polygon); O2 Maroon Valley Corridor ends at Maroon Lake | O5: 0.4% ≤100 ft of mapped NFS trail |
| 21 | `candidate-mvum-13466628` | MAROON LAKE | 508264010602 | -106.9425, 39.0984, -106.9333, 39.1032 | Aspen RD 100.0 | T11S R85W S42, T11S R86W S12, T11S R86W S13 | **OVERLAPS** | O3: 89.8% ≤½ mi of Maroon Lake (NHD polygon); O2 Maroon Valley Corridor ends at Maroon Lake | O5: 5.8% ≤100 ft of mapped NFS trail |
| 22 | `candidate-mvum-13506718` | MAROON LAKE DAY USE | 6526010314 | -106.9423, 39.0978, -106.9373, 39.1007 | Aspen RD 100.0 | T11S R86W S13 | **OVERLAPS** | O3: 100.0% ≤½ mi of Maroon Lake (NHD polygon); O2 Maroon Valley Corridor ends at Maroon Lake | O5: 11.8% ≤100 ft of mapped NFS trail |
| 23 | `candidate-mvum-13460859` | MAROON LAKE OVERNIGHT PARKING | 524312010602 | -106.939, 39.0987, -106.9365, 39.1009 | Aspen RD 100.0 | T11S R86W S13 | **OVERLAPS** | O3: 100.0% ≤½ mi of Maroon Lake (NHD polygon); O2 Maroon Valley Corridor ends at Maroon Lake | O5: 4.3% ≤100 ft of mapped NFS trail |
| 24 | `candidate-mvum-13460920` | MAROON LAKE OVERNIGHT PARKING | 6527010314 | -106.9386, 39.0992, -106.9359, 39.1015 | Aspen RD 100.0 | T11S R86W S13 | **OVERLAPS** | O3: 100.0% ≤½ mi of Maroon Lake (NHD polygon); O2 Maroon Valley Corridor ends at Maroon Lake | — |
| 25 | `candidate-mvum-13460856` | NEW YORK CREEK TRAILHEAD | 19010314 | -106.6611, 39.0934, -106.6587, 39.0957 | Aspen RD 100.0 | T11S R83W S16 | **OVERLAPS** | O2 Lincoln Creek Corridor: 100.0% ≤¼ mi of USGS "LINCOLN CREEK" road (CR 23, SH 82 to Portal); Portal also "Portal Described Area" by name | O5: 15.3% ≤100 ft of mapped NFS trail; O6: trailhead spur (by name) |
| 26 | `candidate-mvum-13465494` | PORTAL CAMPGROUND | 17010314 | -106.613, 39.0749, -106.6114, 39.0776 | Aspen RD 100.0 | T11S R83W S24 | **OVERLAPS** | O2 Lincoln Creek Corridor: 100.0% ≤¼ mi of USGS "LINCOLN CREEK" road (CR 23, SH 82 to Portal); Portal also "Portal Described Area" by name | O5: 3.2% ≤100 ft of mapped NFS trail |
| 27 | `candidate-mvum-13466088` | SILVER BAR CAMPGROUND | 562010314 | -106.8945, 39.1456, -106.8919, 39.1477 | Aspen RD 100.0 | T10S R85W S28 | **OVERLAPS** | O2 "Maroon Bells Scenic Area Described Area" (¼ mi outside Silver Bar/Bell/Queen) by name; O3 100.0% ≤¼ mi of Maroon Creek Rd | O5: 10.9% ≤100 ft of mapped NFS trail |
| 28 | `candidate-mvum-13460991` | SILVER BELL CAMPGROUND | 563010314 | -106.8969, 39.1415, -106.894, 39.1443 | Aspen RD 100.0 | T10S R85W S32, T10S R85W S33 | **OVERLAPS** | O2 "Maroon Bells Scenic Area Described Area" (¼ mi outside Silver Bar/Bell/Queen) by name; O3 100.0% ≤¼ mi of Maroon Creek Rd | O5: 7.3% ≤100 ft of mapped NFS trail |
| 29 | `candidate-mvum-13466504` | SILVER QUEEN CAMPGROUND | 564010314 | -106.9034, 39.1282, -106.9007, 39.1308 | Aspen RD 100.0 | T10S R85W S32, T11S R85W S05 | **OVERLAPS** | O2 "Maroon Bells Scenic Area Described Area" (¼ mi outside Silver Bar/Bell/Queen) by name; O3 100.0% ≤¼ mi of Maroon Creek Rd | O5: 10.1% ≤100 ft of mapped NFS trail |
| 30 | `candidate-mvum-13465102` | WELLER LAKE CAMPGROUND | 549010314 | -106.722, 39.1201, -106.7193, 39.1223 | Aspen RD 100.0 | T11S R84W S01 | **OVERLAPS** | O2 SH 82 Corridor 100.0% (name differs from "Weller Campground", not relied on) | — |
| 31 | `candidate-mvum-13465161` | WEST MAROON TRAILHEAD | 6529010314 | -106.9353, 39.102, -106.9329, 39.1043 | Aspen RD 100.0 | T11S R85W S42, T11S R86W S12, T11S R86W S13 | **OVERLAPS** | O3/O2: 100.0% ≤¼ mi of USGS "MAROON LAKE" road (taken as Maroon Creek Rd / CR 13); West Maroon 11.7% ≤½ mi of lake | O5: 30.8% ≤100 ft of mapped NFS trail; O6: trailhead spur (by name) |
| 32 | `candidate-mvum-13461217` | WILDWOOD SCHOOL | 1026010314 | -106.7835, 39.1479, -106.7818, 39.1498 | Aspen RD 100.0 | T10S R84W S28 | **OVERLAPS** | O4 Wildwood Parcel: 100% in W½ S28 T10S R84W (BLM PLSS; half split at section bbox midpoint), on Hwy 82; name matches "Wildwood Lane" | — |
| 33 | `candidate-mvum-13499372` | BELLVIEW | 1162010431 | -107.0124, 39.0, -107.0033, 39.01 | Gunnison RD 100.0 | T12S R86W S20, T12S R86W S43, T12S R86W S48 | **POSSIBLE** | O8 Crested Butte area (GMUG Gunnison RD): polygon in the order's stated township/range envelope (T12S, R84–87W); designated area only on Exhibit A map, not registered | — |
| 34 | `candidate-mvum-13465452` | CRYSTAL RIVER | 371010314 | -107.05, 39.0143, -107.0459, 39.0247 | Gunnison RD 4.2; Sopris RD 95.6 | T12S R86W S07, T12S R86W S44, T12S R87W S12, T12S R87W S13 | **POSSIBLE** | 4.2% in GMUG Gunnison RD inside O8 envelope (T12S R86–87W); 95.6% Sopris RD, outside every O7 Described Area | O5: 8.0% ≤100 ft of mapped NFS trail |
| 35 | `candidate-mvum-13492616` | EMERALD LAKE PG | 910010431 | -107.0455, 39.0061, -107.0372, 39.0135 | Gunnison RD 100.0 | T12S R86W S44, T12S R86W S45 | **POSSIBLE** | O8 Crested Butte area (GMUG Gunnison RD): polygon in the order's stated township/range envelope (T12S, R84–87W); designated area only on Exhibit A map, not registered | — |
| 36 | `candidate-mvum-13466150` | MONTEZUMA | 569010314 | -106.8573, 39.0047, -106.8369, 39.0205 | Aspen RD 100.0 | T12S R85W S11, T12S R85W S13, T12S R85W S14, T12S R85W S43 … | **POSSIBLE** | O2 Pearl Pass Road Corridor: 16.0% ≤¼ mi of USGS "PEARL PASS" road, but corridor endpoints (Pearl Pass TH; CR 15 crossing of Castle Creek) not locatable | — |
| 37 | `candidate-mvum-13465523` | PARADISE BASIN | 377010314 | -107.05, 39.0142, -107.0464, 39.017 | Sopris RD 100.0 | T12S R86W S44, T12S R87W S13 | **POSSIBLE** | EDW district boundary puts it 100% in WRNF Sopris RD (no O7 area applies), but O8 Exhibit A labels "Paradise Basin" at the edge of its hatched area; jurisdiction line unresolved | O5: 10.6% ≤100 ft of mapped NFS trail |
| 38 | `candidate-mvum-13499366` | SCHOFIELD PASS | 933010431 | -107.0481, 39.0, -107.0225, 39.0161 | Gunnison RD 95.2; Sopris RD 4.7 | T12S R86W S20, T12S R86W S44, T12S R86W S45, T12S R86W S46 | **POSSIBLE** | O8 Crested Butte area (GMUG Gunnison RD): polygon in the order's stated township/range envelope (T12S, R84–87W); designated area only on Exhibit A map, not registered | O5: 26.1% ≤100 ft of mapped NFS trail |
| 39 | `candidate-mvum-13467522` | TAYLOR LAKE BYPASS | 1852010431 | -106.7587, 39.0108, -106.7483, 39.0179 | Gunnison RD 100.0 | T12S R84W S10, T12S R84W S11, T12S R84W S15 | **POSSIBLE** | O8 Crested Butte area (GMUG Gunnison RD): polygon in the order's stated township/range envelope (T12S, R84–87W); designated area only on Exhibit A map, not registered | — |
| 40 | `candidate-mvum-13510013` | TAYLOR PASS | 1504010431 | -106.7578, 39.0, -106.7102, 39.0216 | Gunnison RD 98.9; Aspen RD 1.1 | T12S R83W S18, T12S R84W S10, T12S R84W S11, T12S R84W S13 … | **POSSIBLE** | O8 Crested Butte area (GMUG Gunnison RD): polygon in the order's stated township/range envelope (T12S, R84–87W); designated area only on Exhibit A map, not registered | — |
| 41 | `candidate-mvum-13467528` | TAYLOR PASS DIVIDE | 1505010431 | -106.7558, 39.02, -106.7336, 39.0459 | Gunnison RD 31.6; Aspen RD 68.4 | T11S R84W S55, T12S R84W S10, T12S R84W S11, T12S R84W S37 … | **POSSIBLE** | O8 Crested Butte area (GMUG Gunnison RD): polygon in the order's stated township/range envelope (T12S, R84–87W); designated area only on Exhibit A map, not registered | — |
| 42 | `candidate-mvum-13492619` | TAYLOR RIVER HEAD | 1853010431 | -106.7618, 39.0, -106.7538, 39.0216 | Gunnison RD 95.9; Aspen RD 4.1 | T12S R84W S10, T12S R84W S15 | **POSSIBLE** | O8 Crested Butte area (GMUG Gunnison RD): polygon in the order's stated township/range envelope (T12S, R84–87W); designated area only on Exhibit A map, not registered | — |
| 43 | `candidate-mvum-13465913` | ASPEN ADMIN. SITE | 1010314 | -106.8314, 39.1948, -106.8302, 39.1963 | Aspen RD 92.7 | T10S R85W S12 | **NO EVIDENCE** | Aspen RD, T10S R85W S12; no O2 Described Area; ski-area permit boundaries not checked | — |
| 44 | `candidate-mvum-13465447` | GOLD HILL | 560010314 | -106.7357, 39.0445, -106.7315, 39.0514 | Gunnison RD 2.9; Aspen RD 97.1 | T11S R84W S55 | **NO EVIDENCE** | Aspen RD (2.9% Gunnison RD, T11S, outside O8 envelope); not in an O2 corridor (5598 m from Castle Creek Rd) | — |
| 45 | `candidate-mvum-13461267` | LENADO | 5010314 | -106.7705, 39.2439, -106.7507, 39.26 | Aspen RD 100.0 | T9S R84W S21, T9S R84W S22, T9S R84W S27 | **NO EVIDENCE** | Aspen RD, T9S R84W: outside every O2 Described Area named and outside the Exhibit A hatching | O5: 0.7% ≤100 ft of mapped NFS trail |
| 46 | `candidate-mvum-13461434` | LENADO | 5010314 | -106.7681, 39.256, -106.7629, 39.26 | Aspen RD 100.0 | T9S R84W S21, T9S R84W S22 | **NO EVIDENCE** | Aspen RD, T9S R84W: outside every O2 Described Area named and outside the Exhibit A hatching | — |
| 47 | `candidate-mvum-13466505` | LENADO | 5010314 | -106.743, 39.2561, -106.7257, 39.26 | Aspen RD 100.0 | T9S R84W S23, T9S R84W S24 | **NO EVIDENCE** | Aspen RD, T9S R84W: outside every O2 Described Area named and outside the Exhibit A hatching | O5: 1.9% ≤100 ft of mapped NFS trail |
| 48 | `candidate-mvum-13446823` | PEAKABOO GULCH | 5939010465 | -106.5843, 39.014, -106.57, 39.0303 | Leadville RD 100.0 | T12S R82W S37, T12S R82W S40, T12S R82W S42 | **NO EVIDENCE** | PSICC Leadville RD, T12S R82W: outside Twin Lakes / Turquoise Lake areas of O10 (T9–11S R80–81W) | — |
| 49 | `candidate-mvum-13499358` | PINE CREEK | 972280010602 | -106.6818, 39.0219, -106.6702, 39.0348 | Gunnison RD 100.0 | T12S R83W S04, T12S R83W S39, T12S R83W S40, T12S R83W S41 … | **NO EVIDENCE** | GMUG Gunnison RD, T12S R83W: outside O8 envelope; not in O9 Lower/Upper Taylor areas as stated | — |
| 50 | `candidate-mvum-13461542` | SOUTH FORK FRYINGPAN | 280010314 | -106.6001, 39.2367, -106.5889, 39.26 | Sopris RD 100.0 | T9S R82W S18, T9S R82W S19, T9S R82W S30 | **NO EVIDENCE** | Sopris RD: 4208 m from USGS "FRYING PAN" road (CR 4), beyond O7 ¼ mi corridor | O5: 4.0% ≤100 ft of mapped NFS trail |
| 51 | `candidate-mvum-13492677` | TELLURIUM | 1206010431 | -106.6749, 39.0, -106.6611, 39.0332 | Gunnison RD 100.0 | T12S R83W S16, T12S R83W S39, T12S R83W S42 | **NO EVIDENCE** | GMUG Gunnison RD, T12S R83W: outside O8 envelope (R84–87W) and upstream of O9 Taylor endpoints | — |

## 4. Order ledger

Every page below was read on **2026-10-20** with a plain GET on `www.fs.usda.gov`. Quotes are verbatim from the HTML order text on the alert page, unless marked as coming from an exhibit or PDF. "Expiry" is the "Alert End Date" or the implementation sentence.

### Area-wide camping prohibitions (used for classification)

**O2. WRNF Order #2025-07, "Aspen RD, Occupancy and Use Prohibitions".** In force. Effective 2025-09-01 to 2028-12-31. "/S/Brian Glaspell Signed 08/29/25". Page last updated March 5, 2026.
- URL: https://www.fs.usda.gov/r02/whiteriver/alerts/aspen-rd-occupancy-and-use-prohibitions
- Exhibit A, read as PDF: https://www.fs.usda.gov/sites/nfs/files/r02/whiteriver/publication/alerts/AspenClosureOrderExhibitA_D3.pdf
- "…the following are prohibited on the National Forest System (NFS) lands in the Aspen Ranger District … described below and shown on the attached map incorporated into this Order as Exhibit A (the "Described Areas"): … Camping in Described Areas. 36 C.F.R. § 261.58(e)"
- "Maroon Valley Corridor – All NFS lands within ¼ mile of Pitkin County Road 13 beginning at the Forest boundary and ending at Maroon Lake."
- "Maroon Bells Scenic Area Described Area - All NFS lands within ¼ mile outside of the Silver Bar, Silver Bell and Silver Queen campgrounds."
- "Difficult Described Area - All NFS lands within ¼ mile outside of the Difficult Campground." The Weller and Lostman entries use the same wording.
- "Castle Creek Road Corridor – All NFS lands within ¼ mile of Pitkin County Road 15 beginning at the Forest boundary and ending at its junction with NFS Road (NFSR) 102 and within ¼ mile of NFSR 103 beginning at the junction with Pitkin County Road 15 and ending at the Pearl Pass Trailhead."
- "Pearl Pass Road Corridor - All NFS lands within ¼ mile of Pitkin County Road 15 beginning at the Pearl Pass Trailhead and ending were Pitkin County Road 15 crosses Castle Creek."
- "Colorado Highway 82 Corridor – All NFS lands within ¼ mile of Colorado Highway 82 beginning and including the Difficult Picnic Area and ending at Independence Pass Summit."
- "Lincoln Creek Corridor – All NFS lands within ¼ mile of Pitkin County Road 23 beginning at its junction with Colorado Highway 82 and ending at the Portal Campground."
- "Portal Described Area – All NFS Lands within ¼ mile outside of the Portal Campground."
- "Ashcroft Townsite – All NFS lands within the Ashcroft Townsite in Sections 29, 30, 31, and 32, T.11S, R84W."
- "Ski Areas – … all NFS lands within Special Use Permit Area for the resorts."
- Exhibit A legend (PDF): "2) Camping except in campground and dispersed campsites designated and provided by the Forest Service".
- **Text conflict.** The order text has no exception for designated sites, but the exhibit legend does. Either reading prohibits camping on the computed polygons, which are not designated sites, so the classification does not depend on which is right.
- The map shows the SH 82 corridor running from Difficult through Weller, Grottos, Lincoln Gulch, Lost Man, Discovery and Braille to the Independence Pass top. It shows the Lincoln Creek corridor with New York and Tabor down to Portal, the Castle Creek corridor with American Lake, Cathedral and Pearl Pass, and the Maroon valley with the Silver campgrounds, East and West Maroon and Maroon Bells. Taylor Pass/Express Creek is shown outside the hatching.

**O3. WRNF-2022-03, Maroon Bells Scenic Area / Maroon Valley prohibitions.** In force. Effective 2022-04-26 "until rescinded or until November 15, 2027". "Done at Glenwood Springs, Colorado this 26th day of April 2022."
- URL: https://www.fs.usda.gov/r02/whiteriver/alerts/maroon-bells-scenic-area-maroon-valley-prohibitions
- "The Described Area includes Maroon Lake, the ½ mile from the edge of Maroon Lake, and ¼ mile on either side of the edge of Maroon Creek Road."
- "The Described Road is the segment of Maroon Creek Road (also known as NFS Road 125 or Pitkin County Road 13) starting at the Aspen Highlands Transportation Center and ending at its terminus near Maroon Lake."
- "4. Camping outside of developed recreation sites. 36 C.F.R. 261.58(e)"

**O4. WRNF-2023-07, Wildwood Parcel occupancy and use.** In force. Effective 2023-06-01 to 2028-12-31. "Signed and issued on May 19, 2023".
- URL: https://www.fs.usda.gov/r02/whiteriver/alerts/wildwood-parcel-occupancy-and-use
- "4. Camping. 36 C.F.R. § 261.58(e)"
- "The Described Area is in the W½ of Section 28 and E½ of Section 29, Township 10 South, Range 84 West, 6th P.M., in Pitkin County, Colorado. It includes the NFS lands along Highway 82 north of the Wildwood Boat Launch, the Wildwood Boat Launch Road and its surrounding area, and the portions of Wildwood Lane that are part of the White River National Forest."

**O7. WRNF Order 2025-08, Sopris RD Occupancy and Use Prohibitions.** In force. Effective 2025-09-01 to 2028-12-31. "/S/Brian Glaspell Signed 08/29/25".
- URL: https://www.fs.usda.gov/r02/whiteriver/alerts/sopris-ranger-district-occupancy-and-use-prohibitions
- "Camping in the Described Areas. 36 C.F.R. § 261.58(e)."
- "Frying Pan River Corridor – All NFS lands within ¼ mile of County Road 4."
- "Crystal River Corridor – All NFS lands within ¼ mile of Highway 133, beginning at the Forest boundary … and ending at the town of Marble…"
- The other Described Areas name the Ruedi, Dearhamer, Elk Wallow, Chapman, Avalanche, Redstone and Bogan Flats campgrounds, Nast Lake, Sunlight and Babbish Gulch. None is near a polygon.

**O8. GMUG-2022-10, Crested Butte Area Camping and Fire Prohibitions (Gunnison RD).** In force. Effective 2022-06-14 "until rescinded or until June 30, 2027". "Executed in Delta, Colorado this 14th day of June 2022." The PDF is digitally signed 2022.06.14.
- URL: https://www.fs.usda.gov/r02/gmug/alerts/crested-butte-area-camping-and-fire-prohibitions
- PDF: https://www.fs.usda.gov/sites/nfs/files/r02/gmug/publication/alerts/GMUG-2022-10.pdf
- "The Described Area is located near Crested Butte, Colorado in Gunnison County within the Townships 12, 13, 14 North, Ranges 84, 85, 86, 87 West, 6th PM."
- "1. Camping, except in Cement Creek Campground, Lake Irwin Campground, or Gothic Campground or in a Forest Service designated campsite marked with a post with the site number and universal camping symbol."
- **Text anomaly.** The text says "North", but the exhibit labels the same townships "T.12S." etc. I read the envelope as South.
- The exhibit's hatched "Designated Camping Area (Restricted Area)" reaches north to the Bellview and Schofield area, labelled "Paradise Basin", and east into T.12S R.84W near Pearl Pass and Star Peak. I did not register it to coordinates.

**O9. GMUG-2022-09, Taylor Canyon and Reservoir camping restrictions.** In force. Effective 2022-06-09 "until rescinded or until May 31, 2027". Executed 2022-06-06.
- URL: https://www.fs.usda.gov/r02/gmug/alerts/taylor-canyon-and-reservoir-camping-restrictions
- "The Lower Taylor Area … within 500 yards of County Road 742 … beginning at the Forest Boundary at Almont … and ending at River's End Campground in Taylor Park (Section 5, Township 13S, Range 83W…)."
- "Camping within 100 feet of the high water line of the Taylor River from where it enters the Taylor Reservoir to the Dorchester Campground…"
- Both areas lie downstream of the polygons, so none was classified under O9.

**O10. PSICC Order 02-12-00-24-05, San Isabel NF (Leadville, Salida, San Carlos RDs) occupancy and use.** In force. Effective 2024-04-05 to **2026-12-01**.
- URL: https://www.fs.usda.gov/r02/psicc/alerts/san-isabel-national-forest-occupancy-and-use-restrictions
- "Camping within 100 feet of a body of water (such as a lake, stream, pond, or river) unless in a Forest Service developed recreation site or designated dispersed site."
- "Camping, except in Forest Service developed recreation sites and designated dispersed sites, in the Turquoise Lake Recreation Area, Twin Lakes Recreation Area (Exhibit E Leadville)…"
- "Twin Lakes Recreation Area … Sections 15, 16, 17, 18, 19, 20, 21, 22 and 23, Township 11 South, Range 80 West."
- **This order expires in 6 weeks.** Its successor is unknown.

**O11. PSICC Order 2003-03, camping in areas posted closed.** No end date.
- URL: https://www.fs.usda.gov/r02/psicc/alerts/prohibition-camping-areas-posted-closed-camping
- "Camping in an area, developed site or campground that is posted as closed to camping."
- Its scope is on-the-ground posting, so it cannot be checked from here.

### Setback orders (reported per polygon as partial overlap)

**O5. WRNF Order 2026-13, "White River National Forest Camp Location Restrictions".** In force. Effective 2026-07-01 to 2028-12-31. "/S/Brian Glaspell Signed 1st day of July, 2026."
- URL: https://www.fs.usda.gov/r02/whiteriver/alerts/white-river-national-forest-camp-location-restrictions
- "Camping, unless in a Forest Service developed recreation site or designated dispersed site, within 100 feet of a body of water (such as a lake, stream, pond, river, wetland) or a National Forest System Trail."
- "DESCRIBED AREA 100 feet of lakes, streams, ponds, rivers, wetlands, and National Forest System trails on or within the White River National Forest."
- The builder subtracts 100 ft of NHD water: 0 % of polygon area remains within 100 ft of loaded hydrology. It does not subtract trails or wetlands. NHD wetlands are not loaded.

**O6. WRNF 1996-08, "Aspen RD, No camping within 300' of trailhead, with exceptions".** No end date. "DONE at Glenwood Springs, Colorado this 10th day of October, 1996."
- URL: https://www.fs.usda.gov/r02/whiteriver/alerts/aspen-rd-no-camping-within-300-trailhead-exceptions
- "…the following acts are prohibited within the boundaries of the Aspen Ranger District … Camping within 300 feet of a trailhead, except for the following: Capitol Trailhead …; Hardscrabble Trailhead …; and Haypark/Thomas Lakes Trailhead…"
- Trailhead locations are not loaded, so the only matches are polygons whose spur is named "… TRAILHEAD". Other trailheads on Exhibit A, such as Cathedral, Grottos, Tabor and Portal, sit at or near further polygons.

### Read and judged not to restrict where the polygons are

| ID | Order | Dates | Why not classified |
|---|---|---|---|
| O1a | WRNF 2024-01, camping stay limitations. https://www.fs.usda.gov/r02/whiteriver/alerts/camping-stay-limitations | 2024-01-01 to 2027-12-31 | A time limit, not a closure: "Camping … for more than 14-days with in any continuous 30-day period" |
| O1b | WRNF 1993-06, developed campground stay limitations. https://www.fs.usda.gov/r02/whiteriver/alerts/developed-campground-stay-limitations | 1993-06-23, no end | Time limits inside the named campgrounds, for example "FIVE CONSECUTIVE DAYS … Difficult Campground" |
| O1c | WRNF 1997-04, unlicensed OHV and camping. https://www.fs.usda.gov/r02/whiteriver/alerts/unlicensed-ohvvehicle-restrictions-and-camping | 1997-03-03, no end | A 14-day limit; "Specific areas may have stricter camping limits in effect if needed." |
| O1d | GMUG-2017-08, general occupancy. https://www.fs.usda.gov/r02/gmug/alerts/general-occupancy-and-use-grand-mesa-uncompahgre-and-gunnison-national-forests | 2017-07-12 to 2027-07-12 | Stay limits. Its 500-yard rings name only Mosca, Dinner Station and Big Creek, none near a polygon. It also restates the Taylor areas (see O9) |
| — | WRNF 2025-12, Aspen RD seasonal elk-calving area closures. https://www.fs.usda.gov/r02/whiteriver/alerts/aspen-rd-seasonal-area-and-trail-closures-and-dog-restricitions | 2025-03-10 to 2029-08-01 | Areas A–C lie around Snowmass ski area and Burnt Mountain. No polygon is there |
| — | WRNF-2019-30, ski area prohibitions. https://www.fs.usda.gov/r02/whiteriver/alerts/ski-area-prohibitions | 2019-11 to 2029-12-31 | Ski Safety Act entry, not camping |
| — | GMUG-2022-08, Tincup camping restrictions. https://www.fs.usda.gov/r02/gmug/alerts/tincup-camping-restrictions | 2022-06-09 to 2027-05-31 | T14–15S R81W. No polygon is there |
| — | PSICC 2022-08, designated camping and parking. https://www.fs.usda.gov/r02/psicc/alerts/occupancy-and-use-restrictions-designated-camping-and-parking-areas | 2022-07-20 to 2027-07-20 | South Platte RD only |

## 5. Recommendation (for owner decision)

**Recommended: (b), sequenced.**
1. Now: remove the `dispersed_corridors` layer from Aspen display. That means dropping the Explore entry, or emptying the display file, whichever Codex judges smaller and reversible.
2. Then: the full M7-D14 removal from canonical data, the manifest and the producer in M7-B, as the M7 draft proposes.

I do not recommend (a) on its own, and I recommend (c) only as a fallback.

### (a) Fail-closed exclusion of the 42 OVERLAPS and POSSIBLE polygons; keep the 9 NO EVIDENCE ones
- **Trust reasoning.** It removes every polygon this audit could tie to an order. It is the narrowest change that answers "do displayed areas overlap closures".
- **Bear case.** The 9 survivors would read as *vetted*: "these are the ones that passed the closure check". This audit cannot support that.
  - NO EVIDENCE is not permission.
  - 3 of the 9 still overlap the O5 trail setback.
  - Trailhead (O6), wetland (O5) and posted (O11) restrictions are unmapped.
  - O10 expires on 2026-12-01.
  - The survivors are still built from the inferences the M7 draft rejects: possibility from management, an uncited 300 ft buffer, and a frozen trip evaluation.
- **Second bear case.** Doing it "properly" through the producer's `manual_exclusions()` needs polygon geometry for each order. The only geometry I have is my own approximation from USGS centrelines, and the order exhibits are unregistered PDFs. Committing it would publish home-made order boundaries as if they were the agency's. A hand-picked ID exclusion list avoids that, but it is a one-off that rots with the next MVUM refresh.
- **Literals.** Any legend or coverage note explaining the exclusion. A change to `fact_coverage.closures.statement` if orders are cited.

### (b) Full removal of the layer (M7-D14)
- **Trust reasoning.** The audit shows a structural defect, not a few bad polygons. The producer buffers the spur roads into campgrounds, trailheads and Maroon Lake, which are exactly what the orders protect. 33 of 51 are named after such spurs, and 63 % of the layer overlaps an area-wide prohibition. The layer is on by default, it is the largest overnight object on the map, and its title invites the reading "go look here". Removal is the only option that does not leave a residual implication of permission.
- **Bear case.**
  - Aspen's map looks emptier and loses its most visible overnight layer.
  - The 9 NO EVIDENCE polygons, which a careful user might have researched, disappear with the rest.
  - Removing it from display alone before M7-B leaves canonical data and the producer in place, so a later pipeline run could re-surface it. The interim step needs a guard. R143 in the M7 draft does this later.
  - It is a production deploy through `main`, so it needs the usual approval.
- **Literals.** None strictly required if the entry is simply dropped. If the owner wants a "removed" notice or a changed `known_gaps` or `fact_coverage` sentence, that wording needs approval.

### (c) Presentation change: default-off plus caveat
- **Trust reasoning.** This is the cheapest change, and it stops the layer appearing unasked.
- **Bear case.** Anyone who switches the layer on still sees 32 polygons that this audit ties to in-force camping prohibitions, under a title that reads as a suggestion. A caveat cannot undo the geometry: drawing a shape around Difficult Campground or Maroon Lake says "research camping here" louder than any sentence. The mobile sheet also has little room for a caveat. Of the three options, this keeps the trust failure MR1 describes.
- **Literals.** A new layer title replacing "Areas to research", the caveat sentence itself, and any legend text, all in the CP2 terminology space the M7 draft reserves for owner approval.

Under any option, `v2/pipeline/config/legal_rules.yaml` should not be cited as a legal setback. Its `road_buffer_ft: 300` has no source, and the orders that do exist set ¼ mile, ½ mile, 300 ft (trailheads) and 100 ft (water and trails).

## 6. Unknowns
1. **Exhibit maps were not registered.**
   - Every corridor test uses USGS road centrelines, not the agency's Exhibit A geometry. A road named "MAROON LAKE" in USGS was taken to be Maroon Creek Road (CR 13 / NFSR 125), and the Difficult start of the SH 82 corridor was approximated at −106.785°.
   - OVERLAPS that rest on centreline geometry alone: SH 82 ×5 (Independence Gravel Pit, Grottos Parking Lot, Lost Man TH, Braille TH, Weller Lake CG); Lincoln Creek ×1 (New York Creek TH; Lincoln Gulch CG also falls in the SH 82 test); Castle Creek ×2 (Cathedral Lake); Maroon Creek Road ×2 (East and West Maroon TH; West Maroon is also within ½ mi of the lake). The other OVERLAPS also match a Described Area by name or the Maroon Lake polygon.
   - The visual read of Exhibit A agrees with every OVERLAPS call.
2. **Signed order PDFs were not read** except GMUG-2022-10. The O2 HTML and its Exhibit A legend disagree on the designated-site exception. The classification does not depend on it, but an M7 order record does.
3. **GMUG-related POSSIBLE polygons (9 of the 10; the tenth is Montezuma)** need GMUG-2022-10's Exhibit A registered. Visually, Bellview, Schofield Pass and Emerald Lake PG look inside the hatching, and the Taylor Pass group is near its north-east edge. **Paradise Basin** is labelled on the GMUG exhibit, but EDW puts the polygon in WRNF Sopris RD, so the jurisdiction line is unresolved.
4. **Developed-campground interiors.** Where a polygon includes a campground loop, camping on a paid site there is governed by campground operation (O1b stay limits, season, fees). This audit makes no statement about it.
5. **Unmapped restrictions:**
   - wetlands (O5);
   - trailhead locations (O6) other than the five named spurs;
   - posted closures (O11);
   - ski-area permit boundaries (O2);
   - Ashcroft Townsite, which is within its four sections but not delineated, and is relevant to both Cathedral Lake polygons;
   - Pearl Pass corridor endpoints (Montezuma).
6. **Fire restrictions and temporary closures.** WRNF's index lists "white-river-national-forest-lifting-fire-restrictions-friday-sept-25", which I did not read. Seasonal road or campground closures were not evaluated.
7. **Expiries inside the research horizon.** O10 expires 2026-12-01. O9 and O8 expire 2027-05-31 and 2027-06-30. O1d expires 2027-07-12. O1a expires 2027-12-31. Successors are unknown either way.
8. **District boundaries are generalized** (about 20 m). The split polygons (Gold Hill 2.9 % Gunnison, Taylor Pass 1.1 % Aspen) and Aspen Admin. Site (7.3 % outside any district polygon) may shift.
9. **PR #15 lead versus this audit.** PR #15 counted "at least 16" campground-named overlaps by name. This audit finds 32 OVERLAPS by stated scope and geometry. The lead was directionally right and undercounted.

## 7. Provenance

- **Repository** (read-only, through `git show`):
  - `origin/main:v2/regions/aspen/{display/*.geojson,region.json,explore.json}`
  - `origin/main:v2/pipeline/scripts/07_build_dispersed_corridors.py`
  - `origin/main:v2/pipeline/config/legal_rules.yaml`
  - M7 draft `origin/k-kopacek/m7-spec-draft:docs/specs/M7-camping.md` §12.2 and `docs/research/m7-camping/m7-spec-evidence.md` E1
  - PR #15 `origin/docs/research-drafts:docs/research/m7-camping/M7-camping-evidence-model-draft.md` §3.1, Appendix A
  - PR #35 `origin/research/m7-orders-model` file list
  - I ran `git fetch` to update remote refs and changed no working-tree state.
- **Web, 2026-10-20**, all GET (POST only for the PLSS query body size):
  - fs.usda.gov alert pages ×18, alert indexes ×3, exhibit/order PDFs ×2;
  - apps.fs.usda.gov EDW ranger districts ×2;
  - gis.blm.gov PLSS CadNSDI ×1;
  - carto.nationalmap.gov transportation ×10, including 3 failed malformed queries and 2 schema reads.
- **Scratch analysis**, outside the repository: `/private/tmp/claude-501/-Users-kylekopacek-orca-workspaces-Ohvernight-runtime-observer-spec/9ad0efbc-5bd8-41f4-b3ad-cbc185ab2258/scratchpad/` (`analysis.json`, `analyze.py`, `an2.py`, `table.py`, `web/`, `pdf/`).
- Nothing was written to the repository.
