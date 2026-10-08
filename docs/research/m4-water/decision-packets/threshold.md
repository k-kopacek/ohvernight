# Waterbody size threshold decision packet

**Recommendation: keep the 2 ha provisional threshold for M4 (Option A), and treat the 26 POSSIBLE LOSS features below as an inspection queue rather than lowering the threshold.** Lowering to 0.5 ha would add 44 unnamed Aspen waterbodies and 95 unnamed Douglas waterbodies; by the derived screens only 24 Aspen and 2 Douglas of them look potentially product-relevant, and 93 of the 95 Douglas additions lie on private land with no mapped trail or recreation site within 1 km (the trail and recreation layers cover only Forest Service features, so that screen is weak). These screens are distances and land classes, not evidence of recreation or access.

## DECISION

Do you confirm the provisional unnamed-waterbody display threshold of 2 ha (0.02 km2), or change it to 0.5 ha, to an intermediate value, or to 2 ha plus a reviewed inclusion list of specific smaller perennial lakes?

## EVIDENCE

Scope: unnamed perennial lakes and ponds and eligible reservoirs from 0.5 ha up to (not including) 2 ha (44 in Aspen, 95 in Douglas County). Named waterbodies of the same size (14 Aspen, 2 Douglas) are already displayed at any area and are unaffected by the threshold. Full per-feature data is in `threshold-candidates.csv`; a map preview is in `threshold-preview.html` (open it directly in a browser; it is self-contained).

Buckets (criteria stated in HOW THIS WAS COMPUTED, applied mechanically):

| Bucket | Aspen | Douglas |
|---|---|---|
| POSSIBLE LOSS | 24 | 2 |
| KEEP AT 2 HA | 15 | 93 |
| LIKELY CLUTTER | 5 | 0 |
| Total unnamed, 0.5 to under 2 ha | 44 | 95 |

Aspen context: of the 44, 18 lie inside a designated wilderness polygon and 23 on USFS-managed land; 3 fall outside the land-ownership layer, which has only three polygons. Douglas context: 93 of 95 are on land the source classes as private (PVT) and 2 on other federal land (OTHFE). Douglas has no wilderness features.

Possible loss features, Aspen, by area descending (derived columns are distances and containment only):

| Feature id | Lat, lon (point inside) | Ha | fcode | m to trail (derived) | Nearest trail (derived) | m to rec site (derived) | In wilderness (derived) | Land manager (derived) | elevation_m | Triggers (derived) |
|---|---|---|---|---|---|---|---|---|---|---|
| nhd-72971650 | 39.2588, -106.6653 | 1.6 | 39004 | 1380 | SAWYER LAKE | 15838 | yes | USFS |  | wilderness; public land (USFS) |
| nhd-65879795 | 39.0122, -106.9499 | 1.4 | 39009 | 646 | COPPER CREEK | 14040 | yes | USFS | 3693 m | wilderness; public land (USFS) |
| nhd-72974976 | 39.0489, -106.6572 | 1.3 | 39004 | 680 | TABOR CREEK | 14199 | yes | USFS |  | wilderness; public land (USFS) |
| nhd-72972334 | 39.1511, -106.5831 | 1.1 | 39004 | 1171 | LOST MAN LOOP | 16241 | yes | USFS |  | wilderness; public land (USFS) |
| nhd-72981112 | 39.2468, -106.6539 | 1.1 | 39004 | 490 | SAWYER LAKE | 15395 | yes | USFS |  | wilderness; public land (USFS) |
| nhd-65878197 | 39.0096, -106.7554 | 0.9 | 39004 | 3038 | COOPER BASIN | 14661 | no | USFS |  | public land (USFS) |
| nhd-72971114 | 39.1109, -106.9689 | 0.9 | 39004 | 172 | WILLOW LAKE | 6436 | yes | USFS |  | trail<=200m; wilderness; public land (USFS) |
| nhd-72971110 | 39.1112, -106.9737 | 0.8 | 39004 | 229 | WILLOW LAKE | 6808 | yes | USFS |  | wilderness; public land (USFS) |
| nhd-72974950 | 39.0540, -106.6475 | 0.8 | 39004 | 123 | TABOR CREEK | 14404 | yes | USFS |  | trail<=200m; wilderness; public land (USFS) |
| nhd-72974966 | 39.0515, -106.6856 | 0.7 | 39004 | 948 | NEW YORK CREEK | 12389 | yes | USFS |  | wilderness; public land (USFS) |
| nhd-72974992 | 39.0293, -106.6451 | 0.7 | 39004 | 790 | PETROLEUM LAKE | 16503 | no | USFS |  | public land (USFS) |
| nhd-72978728 | 39.0648, -107.0483 | 0.7 | 39004 | 1990 | NORTH FORK CRYSTAL RIVER | 14864 | yes | USFS |  | wilderness; public land (USFS) |
| nhd-65879789 | 39.0272, -106.9659 | 0.6 | 39004 | 1172 | RUSTLER GULCH | 13015 | yes | USFS |  | wilderness; public land (USFS) |
| nhd-72968374 | 39.0226, -106.8490 | 0.6 | 39004 | 898 | CATHEDRAL LAKE | 12988 | yes | USFS |  | wilderness; public land (USFS) |
| nhd-72972306 | 39.1851, -106.6049 | 0.6 | 39004 | 1940 | SOUTH FORK PASS | 15111 | yes | USFS |  | wilderness; public land (USFS) |
| nhd-72974986 | 39.0327, -106.6399 | 0.6 | 39004 | 624 | PETROLEUM LAKE | 16520 | no | USFS |  | public land (USFS) |
| nhd-72981196 | 39.1463, -106.6647 | 0.6 | 39004 | 856 | MIDWAY | 9182 | yes | USFS |  | wilderness; public land (USFS) |
| nhd-72962614 | 39.2074, -106.7782 | 0.5 | 39004 | 240 | UPPER HUNTER VALLEY | 7300 | no | USFS |  | public land (USFS) |
| nhd-72969572 | 39.0054, -106.6191 | 0.5 | 39004 | 1916 | ANDERSON LAKE | 19968 | no | USFS |  | public land (USFS) |
| nhd-72972348 | 39.1256, -106.6020 | 0.5 | 39004 | 1300 | LINKINS LAKE | 14687 | yes | USFS |  | wilderness; public land (USFS) |
| nhd-72974956 | 39.0528, -106.6603 | 0.5 | 39004 | 902 | TABOR CREEK | 13703 | yes | USFS |  | wilderness; public land (USFS) |
| nhd-72974990 | 39.0296, -106.6310 | 0.5 | 39004 | 76 | PETROLEUM LAKE | 17301 | no | Private |  | trail<=200m |
| nhd-72981154 | 39.2031, -106.6677 | 0.5 | 39004 | 1132 | HUNTER CREEK | 11200 | yes | USFS |  | wilderness; public land (USFS) |
| nhd-72981162 | 39.1762, -106.6926 | 0.5 | 39004 | 1760 | MIDWAY | 7759 | yes | USFS |  | wilderness; public land (USFS) |

Possible loss features, Douglas, by area descending:

| Feature id | Lat, lon (point inside) | Ha | fcode | m to trail (derived) | Nearest trail (derived) | m to rec site (derived) | In wilderness (derived) | Land manager (derived) | elevation_m | Triggers (derived) |
|---|---|---|---|---|---|---|---|---|---|---|
| nhd-117822715 | 39.5629, -105.0522 | 1.6 | 39004 | 13265 | COLORADO | 20555 | n/a (layer empty) | OTHFE |  | public land (OTHFE) |
| nhd-117822917 | 39.5289, -105.0756 | 0.5 | 39004 | 9002 | COLORADO | 16291 | n/a (layer empty) | OTHFE |  | public land (OTHFE) |

The nearest-trail name is a derived fact about the nearest mapped Forest Service trail line; the trail may be several kilometres away and a name is not evidence that the water is reached from it. Only 2 of the 44 Aspen features carry an elevation and none of the Douglas features do (across the whole canonical waterbody layers only 10 Aspen and 10 Douglas features do), so elevation cannot be used as a screen.

Intermediate thresholds, information only (stored areas have 0.1 ha precision, so 1.0 ha means a stored `area_sqkm` of 0.010 or more; 1.5 ha means 0.015 or more):

| Region | Threshold | Unnamed features added vs 2 ha | of which POSSIBLE LOSS recovered | of which KEEP AT 2 HA added | of which LIKELY CLUTTER added |
|---|---|---|---|---|---|
| Aspen | 0.5 ha | 44 | 24 | 15 | 5 |
| Aspen | 1.0 ha | 10 | 5 | 3 | 2 |
| Aspen | 1.5 ha | 3 | 1 | 1 | 1 |
| Douglas | 0.5 ha | 95 | 2 | 93 | 0 |
| Douglas | 1.0 ha | 24 | 1 | 23 | 0 |
| Douglas | 1.5 ha | 7 | 1 | 6 | 0 |

Projected waterbody display bytes (same method as the threshold comparison: compact GeoJSON, 6-decimal coordinates, seven properties; named waterbodies included at every threshold):

| Region | Threshold | Displayed waterbodies | Projected bytes | Change vs 2 ha |
|---|---|---|---|---|
| Aspen | 0.5 ha | 90 | 111,896 | +39,902 |
| Aspen | 1 ha | 56 | 81,860 | +9,866 |
| Aspen | 1.5 ha | 49 | 75,010 | +3,016 |
| Aspen | 2 ha | 46 | 71,994 | +0 |
| Douglas | 0.5 ha | 127 | 227,769 | +108,142 |
| Douglas | 1 ha | 55 | 150,205 | +30,578 |
| Douglas | 1.5 ha | 39 | 129,024 | +9,397 |
| Douglas | 2 ha | 32 | 119,627 | +0 |

## CURRENT BEHAVIOR (2 ha provisional)

Under the approved rule (specification sections 8.1 and 8.2, owner decisions D3 to D5) a perennial lake or pond, or an eligible reservoir, is displayed if it is named (any area) or if it is unnamed and at least 2 ha. At 2 ha Aspen displays 46 waterbodies (71,994 projected bytes) and Douglas displays 32 (119,627 bytes). Of these, 3 (Aspen) and 14 (Douglas) are unnamed waterbodies of 2 ha or more, which appear in the preview as the second colour for comparison. The 44 and 95 unnamed features of 0.5 to 2 ha are not displayed. The threshold is provisional.

## OPTION A (keep 2 ha)

No change. Smallest display, no new unlabelled shapes. The cost is that small unnamed perennial lakes are absent, including the 24 Aspen and 2 Douglas features flagged above, most of them in or near wilderness in Aspen. Whether any of them matter to users is not established by the data.

## OPTION B (0.5 ha)

Display every unnamed perennial lake, pond or eligible reservoir of 0.5 ha or more. Adds 44 (Aspen) and 95 (Douglas) features, recovering all 26 flagged features and adding 108 KEEP AT 2 HA and 5 LIKELY CLUTTER features. Display bytes rise by 39,902 (Aspen) and 108,142 (Douglas); Douglas display data grows by about 90 percent.

## OPTION C (an intermediate value or a rule)

C1, 1.0 ha: adds 10 Aspen and 24 Douglas features; recovers 5 and 1 POSSIBLE LOSS; adds 2 and 0 LIKELY CLUTTER and 3 and 23 KEEP AT 2 HA. Bytes +9,866 and +30,578.

C2, 1.5 ha: adds 3 Aspen and 7 Douglas features; recovers 1 and 1 POSSIBLE LOSS; bytes +3,016 and +9,397.

C3, 2 ha plus a reviewed inclusion list for specific smaller perennial lakes. Note that the approved specification allows a reviewed inclusion list only for intermittent waterbodies (section 8.5). An inclusion list for small perennial lakes is a rule change that the owner must approve, and each entry would need authoritative evidence and a recorded reason; a name or proximity is never a reason. This keeps the display small and lets the 26-feature queue be reviewed feature by feature.

## TRADEOFFS

| | A: 2 ha | B: 0.5 ha | C1: 1.0 ha | C3: 2 ha + list |
|---|---|---|---|---|
| Unnamed features added (Aspen + Douglas) | 0 | 44 + 95 | 10 + 24 | list size |
| POSSIBLE LOSS recovered | 0 | 24 + 2 | 5 + 1 | chosen entries |
| Other additions (KEEP + CLUTTER) | 0 | 20 + 93 | 5 + 23 | 0 |
| Extra bytes (Aspen + Douglas) | 0 | 148,044 | 40,444 | small |
| Rule change needed | no | threshold value only | threshold value only | yes (new rule) |
| Owner review effort | none | none | none | review each entry |

Bytes are not the deciding factor: even 0.5 ha adds under 110 KB per region. The real tradeoffs are unlabelled shapes on the map (an unnamed pond has no name to show), the Douglas additions being mostly private-land ponds, and the lost Aspen high-country water.

## RISKS

- The buckets use derived proximity and land context. They do not establish recreation, access, fishing, paddling or public availability; a feature in POSSIBLE LOSS may be useless to visitors and one in KEEP AT 2 HA may be valuable.
- The trail layers are Forest Service trails only (Aspen 123 features, Douglas 102), and the Douglas recreation-site layer is Forest Service sites only. Douglas has no wilderness features. A Douglas pond near a county or city trail would appear far from any trail, so the Douglas KEEP AT 2 HA count is probably an overestimate of the true no-loss set.
- Aspen has no recreation-site layer in the region manifest; the Aspen recreation distance uses the RIDB facility inventory (`ridb-options.json`), a facility inventory only.
- The Aspen land-ownership layer has three polygons, and 3 features fall outside it (shown as "outside land layer", never guessed).
- Areas are stored at 0.1 ha precision, so features near a boundary may fall on either side of a threshold in a fresh data pull.
- No feature in the table has been researched for an authoritative page; "authoritative page exists" is `unknown` for every row.
- None of the 139 in-scope features is a reservoir by `ftype`, so the source-backed infrastructure indicator is blank for all and gives no signal about detention or storage structures; this does not mean they are natural.
- Option C3 adds ongoing review work and a new rule that must be written into the specification.

## RECOMMENDATION

Keep 2 ha (Option A) for M4. Reasons: the approved rule is already a defensible, simple statement; lowering it adds many unlabelled shapes, mostly in Douglas on private land; and the data cannot show that any of the small features is useful. If the owner wants the Aspen high-country water, the narrower and safer path is Option C3 limited to features the owner inspects from the list above, with a recorded reason for each, which requires approving a rule change. If the owner prefers a pure threshold change, 1.0 ha recovers 5 Aspen and 1 Douglas flagged features at a cost of 5 and 23 other additions, and is the most sensible intermediate value on this evidence. The approved provisional value of 2 ha is not changed by this packet.

## WHAT CHANGES IF APPROVED

Option A: nothing; the threshold is recorded as confirmed rather than provisional. Option B or C1/C2: the single value `unnamed_waterbody_min_area_sqkm` in `v2/pipeline/config/water_display.json` changes, specification 8.2 and decision D4 are updated, and the displayed waterbody sets and snapshot counts are regenerated. Option C3: the specification gains a reviewed inclusion rule for small perennial lakes (section 8.5 extended), a list file with a reason and evidence per entry, validator support, and regenerated display data.

## WHAT REMAINS UNCHANGED

Named waterbodies (displayed at any area), the exclusion of intermittent, ephemeral, unknown-category and ineligible-source-type features, the reservoir eligibility table, the stream rules, the rule that a name is never an inclusion reason, canonical data in `v2/map-data-v2.json` and the Douglas research file, and the trust principle that every activity and access stays unknown unless a claim says otherwise.

## TESTS REQUIRED

A validator and build test that the threshold in `water_display.json` is what the builder and validator both read; a test that boundary areas (stored 0.005, 0.010, 0.015, 0.020) are treated as inclusive at the chosen value; a test that named waterbodies and the excluded categories are unchanged; regenerated counts and projected bytes recorded in the snapshot document and compared with this packet; for C3, tests that an inclusion entry without evidence and reason is rejected and that a name alone cannot create an entry. The standard checks (`00_selftest.py` and the Node tests) must stay green.

## ROLLBACK

Revert the configuration value (and, for C3, remove the inclusion list) and regenerate the display data; the canonical data is untouched by any option, so rollback is a config revert plus a rebuild.

## HOW THIS WAS COMPUTED

Data: worktree `/Users/kylekopacek/orca/workspaces/Ohvernight/m4a-source-preservation` at commit `aa5c20b` (read-only, via `git rev-parse --short HEAD`). Aspen waterbodies are features of `v2/map-data-v2.json` `/layers/hydrology` with `source_layer` equal to `waterbody`; Douglas waterbodies are `v2/regions/douglas-co/research.json` `/layers/waterbodies`.

Scope and classification: display eligibility copied from `scratchpad/m4/prep/threshold_comparison.py` (specification 8.1 and 8.2 and `water_display.json`). In scope are unnamed perennial lake/pond (`ftype` 390) and eligible reservoir (436) features with stored `area_sqkm` of 0.005 up to under 0.020. Named features of that size are listed in the CSV with group `NAMED_UNAFFECTED` and have no bucket; unnamed features of 0.020 or more are group `COMPARISON_GE2HA`.

Point: the polygon's area centroid if inside the polygon (holes respected), otherwise the midpoint of the widest interior span of a horizontal scan line. Distances are metres from that point to the nearest line segment, on a local equirectangular projection; the nearest named displayed waterbody distance is to its boundary. Layers: trails (Aspen `v2/trails.geojson`; Douglas `/layers/trails`), roads (Aspen `/layers/mvum_roads`; Douglas `/layers/roads`), recreation sites (Aspen `v2/ridb-options.json` places; Douglas `/layers/recreation`), wilderness (Aspen `/layers/wilderness`; Douglas layer is empty), land (property `manager`: Aspen `/layers/land_ownership`, Douglas `/layers/land`; the `land_class` property is `unknown` throughout in Aspen and is not used). The road layers are Forest Service MVUM roads only, so no source-backed "developed valley" signal exists and the cluster-of-ponds rule from the brief was not used. Road distance is in the CSV for context but is not a bucket criterion.

Bucket criteria (applied in this order, mechanically):

1. POSSIBLE LOSS if any one of: point within 200 m of a mapped trail; point inside a wilderness polygon; point within 500 m of a recreation-site feature; point on land whose `manager` is anything other than private (PVT or Private), including federal, state and local manager classes.
2. Otherwise KEEP AT 2 HA if the point is on private land (PVT or Private) and more than 1000 m from every trail and every recreation-site feature.
3. Otherwise LIKELY CLUTTER, the residual: private land with a trail within 200 to 1000 m (excluded above 200 m) or a recreation site within 500 to 1000 m, or land class not determinable (outside the land layer). It is a residual, not a positive finding of clutter, and the owner may disagree with the split between buckets 2 and 3.

The source-backed infrastructure indicator is filled only for `ftype` 436 from the `fcode` meaning in the specification; it is blank for all 139 in-scope features. Elevation is `elevation_m` where present. Intermediate-threshold counts take the in-scope features at or above each value. Byte projection reuses the method of the existing script (compact GeoJSON, 6-decimal coordinates, properties id, name, gnis_id, water_class, hydro_category, fcode, area_sqkm).

Scripts, all in `/private/tmp/claude-501/-Users-kylekopacek-orca-workspaces-Ohvernight-m3-foundation/1af2c3f1-290d-4195-82ce-da82ec9d5e39/scratchpad/m4/prep/threshold-product/`: `compute.py`, `build_outputs.py` (CSV and HTML) and `build_md.py` (this packet). The preview HTML draws pond polygons at 5 decimals, other waterbodies simplified to about 5 m, trails simplified to about 40 m (all trails included), and uses no external code or tiles. The CSV has 172 rows.
