# M4-B preparation: stream-grouping dry run

Read-only dry run of the grouping rule in section 8.3 of `docs/specs/M4-functional-recreational-water.md`, run on the committed M4-A data in the `m4a-source-preservation` worktree (`v2/map-data-v2.json` pointer `/layers/hydrology`; `v2/regions/douglas-co/research.json` pointers `/layers/waterways` and `/layers/waterbodies`). Nothing in the repository data was changed, no network was contacted, no geometry was added, and no rule was relaxed. The scripts are standard-library Python kept in the session scratchpad (`m4/prep/grouping.py`, `report.py`, `diag_south_platte.py`, `assemble.py`); they are not part of the repository.

## Summary

The rule runs cleanly on both regions and every structural check passes: no build stop, no segment in two groups, no canal, pipeline or connector in any group. Aspen's 1,512 displayed line pieces become **71 groups** from 67 `gnis_id` values, and Douglas County's 2,359 become **35 groups** from 35 `gnis_id` values; the projected stream artifacts are about 746 kB and 833 kB, down 32% and 53% from today's line features. The most important result is that the **South Platte River is not drawn at all in Douglas County**: the committed data holds no perennial stream segment for it, only 75 artificial-path segments in 43 disconnected fragments cut by the county boundary, so no part is displayable and the `expected_major_rivers` check would fail. In Aspen, **Hunter Creek and Galena Creek each split into two groups** because the only link between their two parts is a short named connector segment of the same `gnis_id`, which the rule does not use for connectivity; Granite Creek splits into three small groups where it weaves across the east edge of the extent. Douglas has no multi-part river, but seven groups are drawn as two separate lines because a very short intermittent-coded segment (7 to 85 m) sits between perennial reaches; East Plum Creek is one of them. Several Douglas creeks lose most of their mapped length because their upper or middle reaches are coded intermittent (East Cherry Creek, Willow Creek, Happy Canyon Creek, Kinney Creek), which is the rule working as written. Finally, `length_km` is the full source length of a segment even where the segment was clipped at the extent, so a group's summed `length_km` overstates the drawn length for edge rivers (Granite Creek 4.15 km stated, 0.87 km actually drawn).

## Cases needing a decision or a rule clarification

| # | Case | What the data shows | What is not settled |
|---|---|---|---|
| 1 | South Platte River absent (Douglas) | `gnis_id` 00201759 has 75 segments, all `artificial_path`; zero `stream` segments of any category. 43 parts, none displayable. All 114 free ends of those parts lie within 0.07 m of the Douglas County coverage polygon boundary: the river is the county line and the county clip cuts it into fragments. Summed `length_km` 22.86 km, but only 9.51 km of geometry lies inside the county. The specification (8.3, 23) expected one 80 m perennial segment; that came from a bounding-box probe and is not in the committed, county-clipped data. | The rule draws nothing and the river is on the 8.3 expected list, so M4-B would stop. A different rule (for example the area polygon's category, or a reviewed inclusion) needs owner approval. Note also that the area polygons are not in the Douglas data: 4 of the 7 `waterbody_source_id` values the South Platte paths reference are absent from the region (they carry 16.12 km of `length_km`, 5.71 km of geometry); the other 3 are Cheesman Lake, Chatfield Lake and Strontia Springs Reservoir. Even if every fragment were drawn it would be 43 separate groups or pieces. |
| 2 | Named connectors of the same `gnis_id` (Aspen) | Hunter Creek 00180061: two parts 19 m apart (24.01 km and 1.01 km), joined in the source by connector `nhd-165836028` named Hunter Creek with the same `gnis_id` (0.019 km). Galena Creek 00180317: two parts 139 m apart (1.97 km and 1.57 km), joined by connector `nhd-72975294` named Galena Creek (0.138 km). A third named connector, `nhd-165836035` Wildcat Creek, joins the two non-displayable parts of Wildcat Creek. | 8.3 says a connector is a candidate "only as a supporting feature", and supporting features (`support_for`) are defined for Douglas only; none exists in either region. As written the rule gives two groups each. Hunter Creek is on the expected-major-rivers list. Should a connector that itself carries the group's `gnis_id` count for connectivity (never drawn)? That would make each river one group drawn in two pieces. I did not apply it. |
| 3 | What "drawn fraction" and "absent" mean for a multi-part river | Hunter Creek 00180061 draws 100% of its perennial and artificial-path length, but across two groups; its main group alone holds 24.01 of 25.03 km (0.96). | 8.3 says the build fails when a listed river "is drawn below its fraction" without saying whether the fraction is per `gnis_id` (all groups) or for the base group `nhd-gnis-<id>` only. |
| 4 | Denominator of the expected-major-rivers fraction | 8.3 says "of the river's named length inside the extent". This audit was asked to use drawn / (perennial stream + artificial path). The two differ wherever a river has intermittent reaches: Cherry Creek 0.99 versus 0.89, Antelope Creek 0.96 versus 0.63, East Cherry Creek 0.72 versus 0.26. | Which denominator the build check uses. With "all named length" a river with a long intermittent headwater can never reach 0.8 however correctly it is drawn. |
| 5 | `length_km` overstates clipped rivers | `length_km` is the unclipped source attribute. Drawn members sum to 534.41 km by attribute and 514.39 km by geometry in Aspen (431.06 and 428.77 in Douglas). Worst groups: South Fork Lake Creek 6.08 stated, 2.54 drawn; Granite Creek 4.15 and 0.87; Nickelson Creek 4.72 and 2.63 (section 12 of each region). | 8.4 defines a group's `length_km` as the sum of members' `length_km` and calls it a derived fact. For edge rivers it would state a length the map does not show. It also drives part ordering (step 5) and every fraction. Keep the attribute sum, or compute from clipped geometry? |
| 6 | Granite Creek: three groups at the extent edge (Aspen) | Parts of 4.15, 0.70 and 0.57 km (`length_km`) all end exactly on the east edge at longitude -106.565; the creek weaves in and out of the bounding box. Gaps 284 m and 881 m. | Rule-conformant (never join across an extent gap). The result is three tappable features called Granite Creek, two of them under 1 km. Reported for the owner; nothing joined. |
| 7 | Slivers of intermittent stream splitting perennial rivers (Douglas) | Seven groups are drawn as two separate lines because one intermittent-coded segment lies between perennial reaches: East Plum Creek 85 m, Willow Creek 00185138 20 m, Fourmile, Pine, Turkey, Indian and Little Turkey Creek about 7 to 13 m each. Total hidden connecting length 0.15 km. | Rule-conformant and one group each. The East Plum Creek gap (85 m) will be visible when zoomed in; the others are below about 13 m. Whether this needs a reviewed exception is an owner question; the rule does not provide one. |
| 8 | Artificial paths stranded behind intermittent reaches (Douglas) | 161 of 255 named artificial-path segments are not drawn (43.67 of 57.12 km): 139 in parts with no perennial segment, 22 separated from every perennial segment by an intermittent one. Over 2 km and undrawn: South Platte River 22.86 km, Happy Canyon Creek 7.23 km, Kinney Creek 4.66 km, East Cherry Creek 2.59 km. | These are the 8.3 "wide rivers" report cases. East Cherry Creek is drawn for 6.80 of 26.13 km (all named classes); Willow Creek 00185138 for 2.63 of 17.62 km; Happy Canyon and Kinney Creek not at all. Working as specified; listed so the owner sees it. |
| 9 | Fryingpan River is not in the Aspen data | No flowline is named Fryingpan River. Only South Fork Fryingpan River (00179784, 12.86 km, complete) is present. | Do not put Fryingpan River in `expected_major_rivers` for Aspen; the build would fail on a river outside the extent. |
| 10 | "Extent" for the Douglas grouping report | Douglas data is clipped to the county polygon (`/layers/coverage`), not to a rectangle. A bounding-box test for "near extent edge", as requested for this dry run, cannot detect edge gaps there. Douglas has no multi-part displayable river, so the classification was not exercised, but the South Platte fragments are all boundary cuts. | The 8.6 grouping report should measure gaps against the coverage polygon for Douglas. The M4-A supporting-feature review kept 0 features, consistent with this. |
| 11 | Specification estimates versus this run | Spec section 23 estimated 62 Aspen and 56 Douglas groups; the run gives 71 and 35. Douglas is lower because the probe counted the bounding box and the committed data is county-clipped (1,514 named perennial segments, not 2,026). The 8.4 example shows Roaring Fork with `member_count` 96; the run gives 111 (82 perennial stream + 29 artificial path), 48.82 km. Section 23 lists Pine Creek as a duplicated Douglas name; only one Pine Creek `gnis_id` is in the clipped data. | Estimates in the specification should be refreshed from this run; no rule change implied. |
| 12 | Three groups named Hunter Creek (Aspen) | `gnis_id` 00180061 (two groups, east of Aspen) and 00175223 (one group, 6.65 km, near the west edge). Bear Creek has two `gnis_id` values in Douglas. Never merged, per G5. | Search and labels will show the same name several times; information only. |

## Checks

| Check | Aspen | Douglas County |
|---|---|---|
| Flowline count (expected Aspen 6,411; Douglas 2,359) | PASS — 6,411 | PASS — 2,359 |
| Every candidate assigned to exactly one part | PASS — 1,395 of 1,395 candidates, max multiplicity 1 | PASS — 2,273 of 2,273 candidates, max multiplicity 1 |
| No segment in two groups | PASS — max multiplicity 1 | PASS — max multiplicity 1 |
| Sum of drawn members equals segments that would carry a group_id | PASS — 1,273 = 1,273 | PASS — 1,608 = 1,608 |
| G1: every member carries the gnis_id of its group id | PASS | PASS |
| G3: every group's part is one connected component | PASS | PASS |
| G6: every drawn member is an eligible stream or an artificial path; every group has an eligible segment | PASS | PASS |
| No canal, pipeline or connector is a candidate or member | PASS | PASS |
| Group ids unique | PASS — 71 of 71 | PASS — 35 of 35 |
| G2: one name per gnis_id among candidates | PASS — 0 conflicts | PASS — 0 conflicts |

Supporting features (`support_for`) are part of 8.3 but none is present in either region's data, so none was used. Build stops (G2): none in either region. Ambiguous branches (three or more segments of one `gnis_id` at one end point): none in either region.

Method notes. End points are the first and last vertex of each LineString, and of each part of a MultiLineString, rounded to six decimals. Distances use an equirectangular approximation. Lengths are sums of `length_km` unless a column says "geometric". The byte projection uses the property list given for this dry run and omits `evidence`, which 8.4 includes (about 13 bytes per feature). "Today" in section 11 is the committed display artifact in the same worktree.

## Aspen

### 1. Source segments considered

| water_class | hydro_category | segments | km | with gnis_id | candidates |
|---|---|---|---|---|---|
| artificial_path | unknown | 468 | 43.85 | 138 | 138 |
| canal_ditch | unknown | 170 | 151.97 | 103 | 0 |
| connector | unknown | 65 | 1.99 | 3 | 0 |
| pipeline | unknown | 13 | 30.04 | 11 | 0 |
| stream | ephemeral | 2425 | 937.35 | 0 | 0 |
| stream | intermittent | 1804 | 866.17 | 110 | 110 |
| stream | perennial | 1466 | 703.56 | 1147 | 1147 |

| Measure | Count |
|---|---|
| Total flowlines | 6411 |
| Candidates (stream or artificial path, non-empty gnis_id) | 1395 |
| Eligible segments (named perennial stream with gnis_id) | 1147 |
| Empty gnis_id | 4899 |
| Named but no gnis_id | 0 |
| gnis_id but no name | 0 |
| Distinct gnis_id among candidates | 82 |
| Supporting features (`support_for`) present | 0 |

### 2. Groups

| Measure | Count |
|---|---|
| gnis_id values with at least one displayable part | 67 |
| Groups in total (including -p2, ...) | 71 |
| gnis_id values with more than one displayable part | 3 |
| gnis_id values with no displayable part | 15 |
| - intermittent/ephemeral only | 8 |
| - artificial path only | 6 |
| - other | 1 |
| Non-displayable parts belonging to a gnis_id that does have a group | 1 |
| - their length, km | 0.23 |

Named streams with no displayable part (not shown):

| Class | Name | gnis_id | segments | parts | km | composition (km) |
|---|---|---|---|---|---|---|
| intermittent/ephemeral only | Casaday Creek | 00179726 | 13 | 1 | 3.73 | stream/intermittent 3.73 |
| intermittent/ephemeral only | Wilbur Creek | 00179728 | 14 | 1 | 3.55 | stream/intermittent 3.55 |
| intermittent/ephemeral only | Sawmill Creek | 00179727 | 9 | 1 | 3.50 | stream/intermittent 3.50 |
| intermittent/ephemeral only | Little Elk Creek | 00175027 | 8 | 2 | 3.12 | stream/intermittent 3.12 |
| intermittent/ephemeral only | Johnson Creek | 00179724 | 5 | 1 | 2.84 | stream/intermittent 2.84 |
| intermittent/ephemeral only | Silver Creek | 00179729 | 10 | 1 | 2.77 | stream/intermittent 2.77 |
| intermittent/ephemeral only | Hannon Creek | 00179725 | 9 | 1 | 2.17 | stream/intermittent 2.17 |
| intermittent/ephemeral only | Cliff Creek | 00179764 | 8 | 1 | 2.11 | stream/intermittent 2.11 |
| artificial path only | Twin Lakes Reservoir and Canal Company Tunnel Number 1 | 00180355 | 1 | 1 | 0.16 | artificial_path/unknown 0.16 |
| artificial path only | Lincoln Gulch Connection Canal | 00202697 | 1 | 1 | 0.12 | artificial_path/unknown 0.12 |
| artificial path only | Elk Creek Ditch | 00202300 | 1 | 1 | 0.11 | artificial_path/unknown 0.11 |
| artificial path only | New York Collection Canal | 00202696 | 1 | 1 | 0.10 | artificial_path/unknown 0.10 |
| artificial path only | Salvation Ditch | 00202674 | 1 | 1 | 0.09 | artificial_path/unknown 0.09 |
| artificial path only | Twin Lakes Reservoir Tunnel Number 2 | 00169494 | 1 | 1 | 0.01 | artificial_path/unknown 0.01 |
| other | Wildcat Creek | 00179702 | 24 | 2 | 7.04 | artificial_path/unknown 1.21; stream/intermittent 5.83 |

Non-displayable parts of a gnis_id that also has a group (these fragments are not shown and get no group id):

| Name | gnis_id | non-displayable parts | segments | km | composition (km) |
|---|---|---|---|---|---|
| Spruce Creek | 00179739 | 1 | 1 | 0.23 | stream/intermittent 0.23 |

### 3. Distribution

| Drawn members per group | Value |
|---|---|
| min | 1 |
| median | 10 |
| p90 | 42 |
| max | 111 |
| total drawn members | 1273 |

| Drawn length per group, km | Groups |
|---|---|
| under 0.5 | 0 |
| 0.5-2 | 7 |
| 2-10 | 49 |
| over 10 | 15 |
| total drawn km | 534.41 |

Shortest groups:

| Group id | Name | drawn members | drawn km |
|---|---|---|---|
| nhd-gnis-00179785-p3 | Granite Creek | 3 | 0.566 |
| nhd-gnis-00179785-p2 | Granite Creek | 1 | 0.701 |
| nhd-gnis-00175590 | South Fork Crystal River | 1 | 0.895 |
| nhd-gnis-00180061-p2 | Hunter Creek | 4 | 1.012 |
| nhd-gnis-00188782 | Middle Brush Creek | 1 | 1.319 |
| nhd-gnis-00180317-p2 | Galena Creek | 5 | 1.566 |
| nhd-gnis-00180317 | Galena Creek | 5 | 1.970 |
| nhd-gnis-00175576 | Rock Creek | 7 | 2.058 |
| nhd-gnis-00175029 | Lime Creek | 6 | 2.079 |
| nhd-gnis-00179722 | Collins Creek | 7 | 2.173 |
| nhd-gnis-00180034 | Jack Creek | 2 | 2.182 |
| nhd-gnis-00180318 | Truro Creek | 4 | 2.233 |

### 4. Multi-part gnis_id values

Bounding extent of all flowline vertices: west -107.055000, south 38.995000, east -106.565000, north 39.265000.

| Name | gnis_id | Group id | drawn members | drawn km | part segments | nearest other part | gap m | nearest part end to extent m | gap ends to extent m | Class | Shortest path between the parts through other flowlines in the data (diagnostic, not used) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Galena Creek | 00180317 | nhd-gnis-00180317 | 5 | 1.97 | 5 | 00180317-p2 | 139 | 3713 | 4759 | (c) larger | 1 seg, 0.14 km: 1x connector/unknown 'Galena Creek' 00180317 |
| Galena Creek | 00180317 | nhd-gnis-00180317-p2 | 5 | 1.57 | 5 | 00180317 | 139 | 4481 | 4759 | (c) larger | 1 seg, 0.14 km: 1x connector/unknown 'Galena Creek' 00180317 |
| Granite Creek | 00179785 | nhd-gnis-00179785 | 2 | 4.15 | 2 | 00179785-p3 | 881 | 0 | 0 | (a) near extent edge | no path within 12 hops |
| Granite Creek | 00179785 | nhd-gnis-00179785-p2 | 1 | 0.70 | 3 | 00179785-p3 | 284 | 0 | 0 | (a) near extent edge | no path within 12 hops |
| Granite Creek | 00179785 | nhd-gnis-00179785-p3 | 3 | 0.57 | 3 | 00179785-p2 | 284 | 0 | 0 | (a) near extent edge | no path within 12 hops |
| Hunter Creek | 00180061 | nhd-gnis-00180061 | 54 | 24.01 | 54 | 00180061-p2 | 19 | 4894 | 7401 | (b) gap under 50 m | 1 seg, 0.02 km: 1x connector/unknown 'Hunter Creek' 00180061 |
| Hunter Creek | 00180061 | nhd-gnis-00180061-p2 | 4 | 1.01 | 4 | 00180061 | 19 | 7409 | 7401 | (b) gap under 50 m | 1 seg, 0.02 km: 1x connector/unknown 'Hunter Creek' 00180061 |

### 5. Intermittent connectivity

| Measure | Count |
|---|---|
| Groups whose part contains any non-perennial stream segment | 8 |
| - drawn as several separate pieces (non-perennial reach lies between drawn reaches) | 0 |
| - drawn as one piece (non-perennial segments are only tails or side stubs) | 8 |
| Groups drawn as one piece, all | 71 |
| Total undrawn connecting km across the several-piece groups | 0.00 |

"Undrawn connecting km" is the length of the undrawn members that remain after repeatedly removing undrawn dead-end tails, i.e. the hidden reaches that lie between drawn reaches. "All undrawn km" also counts the tails.

_None._

### 6. Same name, different gnis_id

Centroid is the mean of the drawn vertices.

| Name | gnis_id | groups | drawn km | centroid lat | centroid lon |
|---|---|---|---|---|---|
| Copper Creek | 00180274 | 1 | 3.48 | 39.0034 | -106.9461 |
| Copper Creek | 00175216 | 1 | 2.41 | 39.1611 | -107.0340 |
| Hunter Creek | 00175223 | 1 | 6.65 | 39.2288 | -107.0046 |
| Hunter Creek | 00180061 | 2 | 25.03 | 39.2046 | -106.7203 |
| Pine Creek | 00180331 | 1 | 5.90 | 39.0151 | -106.6777 |
| Pine Creek | 00180302 | 1 | 4.35 | 39.0345 | -106.8254 |
| Sawyer Creek | 00179763 | 1 | 2.81 | 39.2545 | -106.6482 |
| Sawyer Creek | 00180282 | 1 | 3.23 | 39.0869 | -106.8304 |

### 7. Build stops

gnis_id values carrying more than one distinct name (checked across ALL flowline classes, not only candidates):

_None._

Segments with a name but an empty gnis_id that would otherwise be eligible (named perennial stream): **0**.

Perennial stream segments with a gnis_id but an empty name: **0**.

### 8. Artificial paths

| Artificial paths | segments | km |
|---|---|---|
| All | 468 | 43.85 |
| Unnamed / no gnis_id (never candidates) | 330 | 23.94 |
| Named with gnis_id | 138 | 19.91 |
| - drawn | 126 | 17.89 |
| - not drawn: part has no eligible segment | 11 | 1.81 |
| - not drawn: separated from every eligible segment by a non-perennial stream segment | 1 | 0.21 |

gnis_id values whose artificial paths total more than 2 km and are not drawn at all or drawn for less than 80%:

_None._

For reference, every gnis_id with more than 2 km of artificial path:

| Name | gnis_id | artificial-path km | drawn km | fraction |
|---|---|---|---|---|
| Roaring Fork River | 00174812 | 9.74 | 9.74 | 1.00 |

### 9. Canals, ditches, pipelines and connectors

| water_class | segments excluded | km | with gnis_id | members of any group or candidates |
|---|---|---|---|---|
| canal_ditch | 170 | 151.97 | 103 | 0 |
| pipeline | 13 | 30.04 | 11 | 0 |
| connector | 65 | 1.99 | 3 | 0 |
| other classes | 0 | 0.00 | 0 | 0 |

Confirmed: none is a candidate or a member of any group: **True**.

### 10. Ambiguous branches (information only)

| Measure | Count |
|---|---|
| End-point nodes where three or more candidate segments of one gnis_id meet | 0 |
| - of which three or more DRAWN members meet | 0 |
| gnis_id values with at least one such node | 0 |
| by number of segments meeting | n/a |

_None._

### 11. Resulting display size

| Measure | Today | Projected (grouped) | Change |
|---|---|---|---|
| Display line features | 1,512 (expected 1,512) | 71 | -95.3% |
| Source segments drawn | 1,512 | 1,273 | -15.8% |
| Vertices | 34,340 | 30,532 | -11.1% |
| Bytes, line features serialised compactly | 1,097,296 | 745,858 | -32.0% |
| Bytes, gzip -9 of the same | 248,753 | 197,111 | -20.8% |
| Current file on disk (as committed, includes 43 polygons) | 1,163,589 |  |  |

Of today's 1,512 displayed line features, 1,273 remain drawn as group members, 239 are no longer drawn, and 0 segments are drawn that are not displayed today.

| No longer drawn: water_class | hydro_category | named? | features |
|---|---|---|---|
| stream | intermittent | named | 110 |
| canal_ditch | unknown | named | 103 |
| artificial_path | unknown | named | 12 |
| pipeline | unknown | named | 11 |
| connector | unknown | named | 3 |

### 12. `length_km` versus the geometry actually inside the extent

`length_km` is the source attribute of the whole source segment. Where a segment was clipped at the regional extent the attribute still carries the full source length, so sums of `length_km` overstate what is inside the extent and what is drawn. Geometric km below is measured from the stored coordinates (equirectangular approximation).

| Measure | sum of length_km | geometric km | difference |
|---|---|---|---|
| All flowlines | 2734.93 | 2654.04 | 80.89 |
| Candidates | 569.37 | 546.07 | 23.30 |
| Drawn members | 534.41 | 514.39 | 20.02 |

Segments whose `length_km` differs from their geometric length by more than 5% and 20 m: 181 of 6,411; 30 of them are drawn members.

Groups whose `length_km` sum exceeds their drawn geometric length by more than 0.2 km:

| Name | Group id | length_km sum (the proposed group length_km) | geometric km drawn | overstatement km |
|---|---|---|---|---|
| South Fork Lake Creek | nhd-gnis-00180366 | 6.08 | 2.54 | 3.54 |
| Granite Creek | nhd-gnis-00179785 | 4.15 | 0.87 | 3.28 |
| Nickelson Creek | nhd-gnis-00175222 | 4.72 | 2.63 | 2.09 |
| Capitol Creek | nhd-gnis-00175028 | 6.28 | 4.61 | 1.67 |
| Tellurium Creek | nhd-gnis-00180332 | 7.17 | 5.97 | 1.19 |
| Taylor River | nhd-gnis-00188791 | 3.28 | 2.26 | 1.02 |
| South Fork Fryingpan River | nhd-gnis-00179784 | 12.86 | 11.96 | 0.90 |
| Copper Creek | nhd-gnis-00180274 | 3.48 | 2.60 | 0.88 |
| Spruce Creek | nhd-gnis-00179739 | 3.65 | 2.96 | 0.69 |
| Middle Brush Creek | nhd-gnis-00188782 | 1.32 | 0.74 | 0.58 |
| Bear Creek | nhd-gnis-00175215 | 5.40 | 4.85 | 0.54 |
| Pine Creek | nhd-gnis-00180331 | 5.90 | 5.37 | 0.52 |
| West Snowmass Creek | nhd-gnis-00175219 | 6.04 | 5.67 | 0.37 |
| Granite Creek | nhd-gnis-00179785-p3 | 0.57 | 0.23 | 0.33 |
| South Fork Crystal River | nhd-gnis-00175590 | 0.90 | 0.58 | 0.32 |
| Cooper Creek | nhd-gnis-00180306 | 3.77 | 3.52 | 0.25 |
| Granite Creek | nhd-gnis-00179785-p2 | 0.70 | 0.48 | 0.22 |
| Rock Creek | nhd-gnis-00175576 | 2.06 | 1.84 | 0.22 |
| Bowman Creek | nhd-gnis-00180330 | 7.34 | 7.14 | 0.20 |

## Douglas County

### 1. Source segments considered

| water_class | hydro_category | segments | km | with gnis_id | candidates |
|---|---|---|---|---|---|
| artificial_path | unknown | 255 | 57.12 | 255 | 255 |
| canal_ditch | unknown | 73 | 97.70 | 73 | 0 |
| connector | unknown | 1 | 0.05 | 1 | 0 |
| pipeline | unknown | 12 | 26.06 | 12 | 0 |
| stream | intermittent | 504 | 208.70 | 504 | 504 |
| stream | perennial | 1514 | 417.60 | 1514 | 1514 |

| Measure | Count |
|---|---|
| Total flowlines | 2359 |
| Candidates (stream or artificial path, non-empty gnis_id) | 2273 |
| Eligible segments (named perennial stream with gnis_id) | 1514 |
| Empty gnis_id | 0 |
| Named but no gnis_id | 0 |
| gnis_id but no name | 0 |
| Distinct gnis_id among candidates | 55 |
| Supporting features (`support_for`) present | 0 |

### 2. Groups

| Measure | Count |
|---|---|
| gnis_id values with at least one displayable part | 35 |
| Groups in total (including -p2, ...) | 35 |
| gnis_id values with more than one displayable part | 0 |
| gnis_id values with no displayable part | 20 |
| - intermittent/ephemeral only | 4 |
| - artificial path only | 3 |
| - other | 13 |
| Non-displayable parts belonging to a gnis_id that does have a group | 1 |
| - their length, km | 12.59 |

Named streams with no displayable part (not shown):

| Class | Name | gnis_id | segments | parts | km | composition (km) |
|---|---|---|---|---|---|---|
| intermittent/ephemeral only | Willow Creek | 00185008 | 9 | 1 | 6.16 | stream/intermittent 6.16 |
| intermittent/ephemeral only | Deep Creek | 00183551 | 32 | 1 | 4.64 | stream/intermittent 4.64 |
| intermittent/ephemeral only | West Bear Creek | 00183344 | 8 | 1 | 4.38 | stream/intermittent 4.38 |
| intermittent/ephemeral only | Cook Creek | 00185011 | 5 | 1 | 3.29 | stream/intermittent 3.29 |
| artificial path only | South Platte River | 00201759 | 75 | 43 | 22.86 | artificial_path/unknown 22.86 |
| artificial path only | Arapahoe Canal | 00185006 | 3 | 2 | 0.17 | artificial_path/unknown 0.17 |
| artificial path only | Pleasant Park Ditch | 02724011 | 1 | 1 | 0.05 | artificial_path/unknown 0.05 |
| other | Happy Canyon Creek | 00185007 | 30 | 1 | 19.44 | artificial_path/unknown 7.23; stream/intermittent 12.21 |
| other | Willow Creek | 00183369 | 43 | 1 | 15.24 | artificial_path/unknown 0.35; stream/intermittent 14.90 |
| other | Big Dry Creek | 00182310 | 30 | 1 | 14.19 | artificial_path/unknown 0.07; stream/intermittent 14.12 |
| other | Jarre Creek | 00183373 | 31 | 1 | 12.39 | artificial_path/unknown 0.18; stream/intermittent 12.21 |
| other | Crowfoot Creek | 00193202 | 11 | 1 | 10.99 | artificial_path/unknown 0.85; stream/intermittent 10.14 |
| other | Kinney Creek | 00185092 | 20 | 2 | 9.18 | artificial_path/unknown 4.65; stream/intermittent 4.53 |
| other | Coal Creek | 00184993 | 14 | 2 | 8.61 | artificial_path/unknown 0.25; stream/intermittent 8.36 |
| other | Little Willow Creek | 00183361 | 25 | 1 | 8.44 | artificial_path/unknown 0.08; stream/intermittent 8.36 |
| other | Cottonwood Creek | 00184958 | 7 | 1 | 8.11 | artificial_path/unknown 0.16; stream/intermittent 7.95 |
| other | Piney Creek | 00185047 | 16 | 1 | 6.77 | artificial_path/unknown 1.81; stream/intermittent 4.96 |
| other | Rainbow Creek | 00183368 | 29 | 1 | 6.33 | artificial_path/unknown 0.04; stream/intermittent 6.29 |
| other | Elk Creek | 00193197 | 4 | 1 | 5.11 | artificial_path/unknown 0.28; stream/intermittent 4.83 |
| other | Douglas Creek | 00183692 | 10 | 1 | 1.31 | artificial_path/unknown 0.08; stream/intermittent 1.23 |

Non-displayable parts of a gnis_id that also has a group (these fragments are not shown and get no group id):

| Name | gnis_id | non-displayable parts | segments | km | composition (km) |
|---|---|---|---|---|---|
| East Cherry Creek | 00185141 | 1 | 7 | 12.59 | artificial_path/unknown 1.47; stream/intermittent 11.12 |

### 3. Distribution

| Drawn members per group | Value |
|---|---|
| min | 6 |
| median | 34 |
| p90 | 80 |
| max | 182 |
| total drawn members | 1608 |

| Drawn length per group, km | Groups |
|---|---|
| under 0.5 | 0 |
| 0.5-2 | 1 |
| 2-10 | 18 |
| over 10 | 16 |
| total drawn km | 431.06 |

Shortest groups:

| Group id | Name | drawn members | drawn km |
|---|---|---|---|
| nhd-gnis-00183712 | Trail Creek | 9 | 1.608 |
| nhd-gnis-00185138 | Willow Creek | 6 | 2.628 |
| nhd-gnis-00183726 | Camp Creek | 11 | 2.695 |
| nhd-gnis-00183595 | Middle Garber Creek | 32 | 3.258 |
| nhd-gnis-00183694 | Little Turkey Creek | 21 | 3.277 |
| nhd-gnis-00183725 | Eagle Creek | 20 | 3.999 |
| nhd-gnis-00183564 | South Garber Creek | 34 | 4.419 |
| nhd-gnis-00183565 | North Garber Creek | 33 | 4.513 |
| nhd-gnis-00183538 | Watson Park Creek | 28 | 4.759 |
| nhd-gnis-00183743 | Stark Creek | 34 | 5.531 |
| nhd-gnis-00183576 | Spring Creek | 17 | 5.847 |
| nhd-gnis-00183563 | Horse Creek | 37 | 6.373 |

### 4. Multi-part gnis_id values

Bounding extent of all flowline vertices: west -105.314121, south 39.129526, east -104.661774, north 39.566187.

_None._

### 5. Intermittent connectivity

| Measure | Count |
|---|---|
| Groups whose part contains any non-perennial stream segment | 27 |
| - drawn as several separate pieces (non-perennial reach lies between drawn reaches) | 7 |
| - drawn as one piece (non-perennial segments are only tails or side stubs) | 20 |
| Groups drawn as one piece, all | 28 |
| Total undrawn connecting km across the several-piece groups | 0.15 |

"Undrawn connecting km" is the length of the undrawn members that remain after repeatedly removing undrawn dead-end tails, i.e. the hidden reaches that lie between drawn reaches. "All undrawn km" also counts the tails.

| Name | Group id | drawn km | undrawn connecting km | of which artificial path km | connecting segments | all undrawn km in part | separate drawn pieces |
|---|---|---|---|---|---|---|---|
| East Plum Creek | nhd-gnis-00185069 | 53.60 | 0.09 | 0.00 | 1 | 0.09 | 2 |
| Willow Creek | nhd-gnis-00185138 | 2.63 | 0.02 | 0.00 | 1 | 14.99 | 2 |
| Fourmile Creek | nhd-gnis-00183714 | 11.50 | 0.01 | 0.00 | 1 | 1.50 | 2 |
| Pine Creek | nhd-gnis-00183561 | 11.98 | 0.01 | 0.00 | 1 | 0.96 | 2 |
| Turkey Creek | nhd-gnis-00183698 | 8.59 | 0.01 | 0.00 | 1 | 0.01 | 2 |
| Indian Creek | nhd-gnis-00183378 | 16.84 | 0.01 | 0.00 | 1 | 1.94 | 2 |
| Little Turkey Creek | nhd-gnis-00183694 | 3.28 | 0.01 | 0.00 | 1 | 0.01 | 2 |

### 6. Same name, different gnis_id

Centroid is the mean of the drawn vertices.

| Name | gnis_id | groups | drawn km | centroid lat | centroid lon |
|---|---|---|---|---|---|
| Bear Creek | 00183744 | 1 | 15.67 | 39.2441 | -105.0080 |
| Bear Creek | 00183345 | 1 | 13.21 | 39.3758 | -105.1078 |

Names shared by several gnis_id values where fewer than two have a displayable part (information):

| Name | gnis_id values |
|---|---|
| Cook Creek | 00185011, 00193182 |
| Willow Creek | 00183369, 00185008, 00185138 |

### 7. Build stops

gnis_id values carrying more than one distinct name (checked across ALL flowline classes, not only candidates):

_None._

Segments with a name but an empty gnis_id that would otherwise be eligible (named perennial stream): **0**.

Perennial stream segments with a gnis_id but an empty name: **0**.

### 8. Artificial paths

| Artificial paths | segments | km |
|---|---|---|
| All | 255 | 57.12 |
| Unnamed / no gnis_id (never candidates) | 0 | 0.00 |
| Named with gnis_id | 255 | 57.12 |
| - drawn | 94 | 13.45 |
| - not drawn: part has no eligible segment | 139 | 40.59 |
| - not drawn: separated from every eligible segment by a non-perennial stream segment | 22 | 3.07 |

gnis_id values whose artificial paths total more than 2 km and are not drawn at all or drawn for less than 80%:

| Name | gnis_id | artificial-path km | drawn km | fraction | Case | Why |
|---|---|---|---|---|---|---|
| South Platte River | 00201759 | 22.86 | 0.00 | 0.00 | (a) not drawn at all | 22.86 km in a part with no perennial stream segment |
| Happy Canyon Creek | 00185007 | 7.23 | 0.00 | 0.00 | (a) not drawn at all | 7.23 km in a part with no perennial stream segment |
| Kinney Creek | 00185092 | 4.66 | 0.00 | 0.00 | (a) not drawn at all | 4.66 km in a part with no perennial stream segment |
| East Cherry Creek | 00185141 | 2.59 | 0.00 | 0.00 | (a) not drawn at all | 1.47 km in a part with no perennial stream segment; 1.12 km separated from every perennial segment by a non-perennial stream segment |

For reference, every gnis_id with more than 2 km of artificial path:

| Name | gnis_id | artificial-path km | drawn km | fraction |
|---|---|---|---|---|
| South Platte River | 00201759 | 22.86 | 0.00 | 0.00 |
| Happy Canyon Creek | 00185007 | 7.23 | 0.00 | 0.00 |
| Kinney Creek | 00185092 | 4.66 | 0.00 | 0.00 |
| East Cherry Creek | 00185141 | 2.59 | 0.00 | 0.00 |
| Plum Creek | 00183363 | 2.47 | 2.47 | 1.00 |

### 9. Canals, ditches, pipelines and connectors

| water_class | segments excluded | km | with gnis_id | members of any group or candidates |
|---|---|---|---|---|
| canal_ditch | 73 | 97.70 | 73 | 0 |
| pipeline | 12 | 26.06 | 12 | 0 |
| connector | 1 | 0.05 | 1 | 0 |
| other classes | 0 | 0.00 | 0 | 0 |

Confirmed: none is a candidate or a member of any group: **True**.

### 10. Ambiguous branches (information only)

| Measure | Count |
|---|---|
| End-point nodes where three or more candidate segments of one gnis_id meet | 0 |
| - of which three or more DRAWN members meet | 0 |
| gnis_id values with at least one such node | 0 |
| by number of segments meeting | n/a |

_None._

### 11. Resulting display size

| Measure | Today | Projected (grouped) | Change |
|---|---|---|---|
| Display line features | 2,359 (expected 2,359) | 35 | -98.5% |
| Source segments drawn | 2,359 | 1,608 | -31.8% |
| Vertices | 58,618 | 34,552 | -41.1% |
| Bytes, line features serialised compactly | 1,786,521 | 833,419 | -53.3% |
| Bytes, gzip -9 of the same | 404,864 | 213,202 | -47.3% |
| Current file on disk (as committed) | 1,786,803 |  |  |

Of today's 2,359 displayed line features, 1,608 remain drawn as group members, 751 are no longer drawn, and 0 segments are drawn that are not displayed today.

| No longer drawn: water_class | hydro_category | named? | features |
|---|---|---|---|
| stream | intermittent | named | 504 |
| artificial_path | unknown | named | 161 |
| canal_ditch | unknown | named | 73 |
| pipeline | unknown | named | 12 |
| connector | unknown | named | 1 |

### 12. `length_km` versus the geometry actually inside the extent

`length_km` is the source attribute of the whole source segment. Where a segment was clipped at the regional extent the attribute still carries the full source length, so sums of `length_km` overstate what is inside the extent and what is drawn. Geometric km below is measured from the stored coordinates (equirectangular approximation).

| Measure | sum of length_km | geometric km | difference |
|---|---|---|---|
| All flowlines | 807.23 | 780.11 | 27.12 |
| Candidates | 683.42 | 661.94 | 21.48 |
| Drawn members | 431.06 | 428.77 | 2.28 |

Segments whose `length_km` differs from their geometric length by more than 5% and 20 m: 82 of 2,359; 8 of them are drawn members.

Groups whose `length_km` sum exceeds their drawn geometric length by more than 0.2 km:

| Name | Group id | length_km sum (the proposed group length_km) | geometric km drawn | overstatement km |
|---|---|---|---|---|
| Trout Creek | nhd-gnis-00183711 | 16.07 | 15.48 | 0.59 |
| Cook Creek | nhd-gnis-00193182 | 15.75 | 15.43 | 0.32 |
| West Creek | nhd-gnis-00183713 | 11.97 | 11.71 | 0.26 |
| East Plum Creek | nhd-gnis-00185069 | 53.60 | 53.36 | 0.24 |
