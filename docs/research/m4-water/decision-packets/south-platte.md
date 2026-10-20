# South Platte owner decision packet

The South Platte River is missing from Douglas County because the county clip removes the one 76 m perennial segment the approved rule needs, not because the rule is wrong; that segment lies 11.5 m outside the county line. Keeping Douglas water out to about 500 m beyond the county line, as Aspen already does, draws the river as one 73.2 km line from above Cheesman Lake to Chatfield Lake with the approved rule unchanged. Every option that keeps the current clip leaves the river in 57 visible fragments, whatever the rule.

**Recommendation: Option D. Pad the Douglas water extent by 0.005 degrees (about 500 m) and keep the approved rule exactly as written.**

Preview of the options side by side: [south-platte-preview.html](south-platte-preview.html). Nothing here is decided, and nothing in the repository or the published data was changed.

## DECISION

Should Douglas County water be kept out to about 500 m beyond the county line, so that the already-approved rule draws the South Platte as one river (Option D), instead of changing the rule (B), adding a reviewed exception (C) or leaving the river absent (A)?

## EVIDENCE

Source, fetched live from the USGS NHD service for the box -105.35, 39.10, -104.95, 39.60 (see REQUESTS MADE). All lengths are geometric unless marked.

| South Platte River, `gnis_id` 00201759, in the box | Segments | km |
|---|---:|---:|
| Artificial path (558 / 55800) | 370 | 84.20 |
| Perennial stream (460 / 46006) | 1 | 0.076 |
| Canal or ditch (336 / 33601), the Chatfield dam outlet | 1 | 0.283 |
| Total | 372 | 84.56 |

- Identity: every one of the 372 carries `gnis_id` 00201759 and `gnis_name` South Platte River. No second name.
- Position against the county polygon: 9.51 km inside (11%); 75.02 km outside. Of the outside length, 56.3 km is within 25 m of the county, 62.3 km within 100 m, 65.8 km within 250 m, 66.6 km within 500 m and 68.0 km within 1,000 m. 46.3 km of the river lies within 5 m of the boundary line itself and 63.9 km within 25 m.
- Between the lakes (Cheesman outlet to Chatfield inlet, shortest source path): 56.09 km in 280 segments, 4.51 km inside the county, 51.56 km outside, never more than 79 m outside.
- The one perennial stream segment is NHD 117795757, 76 m long, at 39.2087, -105.2718, just below Cheesman dam. It is 11.5 m outside the county and has no length inside it. In the source it is the link between Cheesman Lake's centre lines (17.3 km with the river above the lake) and the 60.0 km chain down to Chatfield.
- The canal-coded segment is 283 m at the Chatfield dam outlet, 63 m outside the county. Below it is a separate 6.9 km reach, of which 0.33 km is inside the county.
- The saved M4-A raw pages already hold 346 of the 372 segments, and their geometry is identical to today's fetch.

What the centre lines run through (`wbarea_permanent_identifier`):

| Feature | Layer | ftype / fcode | Source area km² | In county km² | Segments | Centre-line km |
|---|---|---|---:|---:|---:|---:|
| 117824529 (Cheesman to Strontia Springs) | area 9 | 460 / 46006, stream or river, perennial | 1.206 | 0.269 | 198 | 38.15 |
| 117824519 (Strontia Springs to Chatfield) | area 9 | 460 / 46006 | 0.330 | 0.097 | 64 | 15.25 |
| 117824543 (above Cheesman Lake) | area 9 | 460 / 46006 | 0.226 | 0.052 | 38 | 9.73 |
| 117824517 (below Chatfield dam) | area 9 | 460 / 46006 | 0.116 | 0.010 | 5 | 3.39 |
| 120654507 (further downstream, up to 3.8 km outside) | area 9 | 460 / 46006 | 0.864 | 0 | 3 | 3.42 |
| 117824547 (Chatfield flood pool) | area 9 | 403 / 40308, inundation area | 12.922 | 7.956 | 1 | 0.12 |
| Cheesman Lake 120030962 | waterbody 12 | 390 / 39009, perennial | 3.581 | 1.322 | 36 | 7.56 |
| Chatfield Lake 117822739 | waterbody 12 | 390 / 39009, perennial | 5.622 | 3.175 | 7 | 3.90 |
| Strontia Springs Reservoir 117834809 | waterbody 12 | 390 / 39004, perennial | 0.328 | 0.115 | 17 | 2.61 |
| Redtail Lake 117822685 (outside the county) | waterbody 12 | 390 / 39004 | 0.047 | 0 | 1 | 0.08 |

The area polygons carry no GNIS id or name. The river areas are 22 to 34 m wide on average.

Verified in the canonical data (commit `aa5c20b`): 75 segments, all artificial path, 22.86 km by source `length_km`, 9.51 km of geometry, no stream segment of any category. 55 reference the four `46006` areas, 20 reference the three lakes. All 26 area identifiers that Douglas centre lines reference and that are absent from the data were looked up: 4 are `46006`, 22 are `48400` (wash).

## CURRENT BEHAVIOR

The approved rule (8.2, 8.3 step 4) draws a river only where a part contains a named perennial stream segment. The Douglas data has none for the South Platte, because the only one is 11.5 m outside the clip. Nothing is drawn, and the expected-major-rivers check would stop the M4-B build.

The clip fragments the river because the county line follows it. The 75 segments become 89 separate lines, 43 parts under the specification's adjacency rule and 57 separate visible pieces. All 114 free ends lie within 0.07 m of the county boundary: every break is a clip cut, none is a source gap. The largest piece is 1.07 km; 28 of the 57 are shorter than 100 m. The three lakes are cut the same way (Cheesman Lake shows 1.32 of 3.58 km²).

## OPTION A

Keep the approved rule and the current clip. Nothing is drawn.

- Drawn: 0 segments, 0 km, 0 groups, 0 pieces. Not continuous.
- Other rivers: none change. Requests: none. Storage: none.
- Trust: rests on source classification only. Implies nothing about access.
- Failure mode: the county's principal river is absent; the expected-major-rivers check fails unless the South Platte is removed from the list.

## OPTION B

A centre line may also start a group when the area or waterbody it runs through is a `46006` area or a waterbody M4 displays.

B1, current clip: 75 segments, 9.51 km, 43 groups, 57 visible pieces. Not continuous.

B2, padded extent (clipped to the padded polygon; whole-segment keep in brackets):

| Padding | Drawn segments | Drawn km | Groups | Visible pieces | Cheesman to Chatfield in one piece |
|---|---:|---:|---:|---:|---|
| 100 m | 342 | 71.65 (75.16) | 6 (4) | 7 (4) | yes |
| 250 m | 345 | 75.09 (75.62) | 2 (2) | 5 (2) | yes |
| 500 m | 347 | 75.86 (76.69) | 2 (2) | 2 (2) | yes |
| 1,000 m | 352 | 77.23 (77.40) | 2 (2) | 2 (2) | yes |

The second group is the reach below Chatfield dam (2.62 km at 500 m), which the source joins to the lake only through the canal-coded outlet.

Other rivers, same rule:

| River | `gnis_id` | Before km | After km (B1) | After km (B2, 500 m) | Why |
|---|---|---:|---:|---:|---|
| Kinney Creek | 00185092 | 0 | 3.59 | 3.59 | Two centre lines through a perennial pond start the group; step 6 then pulls in 3.12 km of centre line through wash areas. Its stream segments are all intermittent |
| Willow Creek | 00183369 | 0 | 0.24 | 0.25 | Centre lines through Wakeman Reservoir |
| Douglas Creek | 00183692 | 0 | 0.08 | 0.08 | Centre lines through Cheesman Lake |
| Deer Creek | 00182569 | 0 | 0 | 0.51 | Centre line through Chatfield Lake |
| North Fork South Platte River | 00183164 | 0 | 0 | 0.62 | Centre lines through a `46006` area |
| Willow Creek | 00183331 | 0 | 0 | 0.43 | Centre line through Strontia Springs Reservoir |
| Goose Creek | 00183668 | 0 | 0 | 0.40 | Centre lines through Cheesman Lake |
| Wildcat, Spring, Brush (00183342) creeks | — | 0 | 0 | 0.02, 0.02, 0.01 | Confluence stubs inside a `46006` area |

Unchanged under B1 and B2: Happy Canyon Creek (0 km), East Cherry Creek (6.79), Cherry Creek (39.77), Plum Creek (18.66), East Plum Creek (53.37, plus 0.15 from padding), West Plum Creek (34.14), Willow Creek 00185138 (2.62). B2 also carries every padding effect listed under Option D. Douglas groups: 35 today, 81 under B1, 50 under B2 at 500 m.

A narrow form, `46006` areas only and no waterbody clause, removes the Kinney, Willow, Douglas, Deer and Goose Creek effects. With the current clip it draws less of the South Platte (56 segments, 5.72 km, 45 pieces) because the lake centre lines are cut off from the river ones.

- Requests: one attribute-only query of layer 9 for the referenced identifiers (26 features, 6.3 KB today; at least 3 more identifiers appear in the padded extent). No area geometry is needed. B2 also needs the padded extent (see Option D).
- Storage: one new property on each centre-line segment (255 today), about 8 KB. Display: Douglas grouped streams 834 KB today, 857 KB (B1), 905 KB (B2, 500 m).
- Trust: rests on source classification only, and each centre line carries its own evidence. Implies nothing about access.
- Failure modes: B1 gives 43 tappable features all named South Platte River; the waterbody clause labels intermittent creeks as perennial rivers where they pass through a pond; a rule amendment against O9's "do not weaken the rule" needs the owner; three referenced identifiers in the padded extent were not classified, so the B2 numbers for other rivers could rise slightly.

## OPTION C

Reviewed inclusion of the South Platte group as it is, current clip.

- Drawn: 75 segments, 9.51 km, 43 groups, 57 visible pieces. Not continuous.
- Other rivers: none change. Requests: none. Display: +20 KB.
- Storage and contract: `water-review.json` has no stream inclusion today. It needs a new reason code, an inclusion keyed by `gnis_id`, and an exception to G6 (every group has a perennial stream segment).
- Trust: rests on a hand-made exception. The evidence would be the same layer 9 record Option B reads automatically. Implies nothing about access.
- Failure modes: 43 tappable fragments; the exception has to be maintained by hand; the fragments still look like a data error on the map.

## OPTION D

Pad the Douglas water extent and keep the approved rule unchanged. Once the extent reaches 12 m past the county line, the 76 m perennial segment is in the data and step 6 of the approved rule draws the centre lines connected to it. This is the behaviour section 8.3 ("Wide rivers") already describes.

| Padding | Drawn segments | Drawn km | Groups | Visible pieces | Drawn fraction | Cheesman to Chatfield in one piece |
|---|---:|---:|---:|---:|---:|---|
| 100 m | 282 | 56.28 | 1 | 1 | 0.79 | yes, but the check at 0.8 fails |
| 250 m | 341 | 72.95 | 1 | 2 | 0.97 | yes; a gap above Cheesman Lake |
| 500 m | 342 | 73.24 | 1 | 1 | 0.97 | yes |
| 0.005 degrees (Aspen's padding) | 343 | 73.32 | 1 | 1 | 0.97 | yes |
| 1,000 m | 347 | 73.98 | 1 | 1 | 0.96 | yes |

At 500 m the drawn line is 9.18 km inside the county and 64.03 km outside it. By what it runs through: 59.0 km through `46006` areas, 14.1 km through the three displayed lakes, 0.12 km through the Chatfield flood pool, 0.08 km of perennial stream. The source's own area category therefore agrees with the result, although the rule does not read it. Not drawn: the 2.62 km below Chatfield dam (0.33 km of it inside the county), which sits behind the canal-coded outlet.

Other rivers at 500 m (padding only; no rule change):

| River | `gnis_id` | Before km | After km |
|---|---|---:|---:|
| Wigwam Creek (new group, stub) | 00183502 | 0 | 0.56 |
| Brush Creek (new group, stub) | 00183517 | 0 | 0.58 |
| Gunbarrel Creek (new group, stub) | 00183525 | 0 | 0.67 |
| Trout Creek | 00183711 | 15.48 | 16.04 |
| Cook Creek | 00193182 | 15.44 | 15.75 |
| West Creek | 00183713 | 11.70 | 11.91 |
| East Plum Creek | 00185069 | 53.37 | 53.52 |
| Little Turkey Creek | 00183694 | 3.15 | 3.25 |
| Bear Creek | 00183345 | 13.09 | 13.15 |
| Trail Creek | 00183712 | 1.56 | 1.61 |
| Turkey Creek | 00183698 | 8.54 | 8.58 |
| Fourmile Creek | 00183714 | 11.44 | 11.45 |
| Sugar Creek, Pine Creek | 00183549, 00183561 | 7.489, 11.953 | 7.491, 11.955 |

Happy Canyon, Kinney, East Cherry, Cherry, Plum and West Plum creeks and all three Willow Creeks do not change. Douglas groups go from 35 to 39; drawn length from 428.8 to 505.4 km, of which 73.2 km is the South Platte.

- Requests: none for the rule. For the extent, either re-clip the saved M4-A raw pages offline, or repeat the two Douglas queries once with the extent enlarged by the padding (about 3,600 flowlines and 2,300 waterbodies, about 7.5 MB raw). At 250 m the saved pages hold every South Platte segment; at 500 m two or three segments (0.24 km) fall outside them.
- Storage: canonical waterways 2,359 to 2,696 features, about 4.09 to 4.46 MB (+0.37 MB, 9%). If waterbodies get the same padding, 2,135 to 2,160 features and 32 to 37 displayed. Display: Douglas grouped streams 834 to 897 KB; the South Platte feature is 55 KB. The Douglas water display limit is 1,888 KB.
- Trust: rests on source classification and source topology only, under the rule the owner already approved. Implies nothing about access. It does draw water up to 500 m outside the county outline, where no other layer has data.
- Failure modes: the whole river depends on one 76 m segment, so if a later source loses it the river disappears (the expected-major-rivers check catches this); three tributary stubs under 0.7 km appear on the far bank; lakes are still cut where they extend past the padding (Cheesman Lake 2.98 of 3.58 km² at 500 m); the manifest sentence "Nothing is known outside it" needs a water exception.

## COMPARISON TABLE

| Option | Drawn km | Groups | Visible pieces | Continuous? | New source request | Other rivers affected | Trust basis |
|---|---:|---:|---:|---|---|---|---|
| A. Approved rule, current clip | 0 | 0 | 0 | no | none | none | source classification |
| B1. Area-category rule, current clip | 9.51 | 43 | 57 | no | layer 9 attributes, 26 features, 6 KB | Kinney +3.59, Willow +0.24, Douglas +0.08 km | source classification, per centre line |
| B2. Area-category rule, 500 m padding | 75.86 | 2 | 2 | yes | layer 9 attributes, about 30 features; padded extent | 10 rivers gain a group (Kinney +3.59 km), plus all of D's | source classification, per centre line |
| C. Reviewed inclusion, current clip | 9.51 | 43 | 57 | no | none | none | hand-made exception |
| D. Approved rule, 500 m padding | 73.24 | 1 | 1 | yes | none for the rule; padded extent | 3 new stubs under 0.7 km; 11 rivers longer by up to 0.56 km | source classification and topology, rule unchanged |

## TRADEOFFS

- Padding is what makes the river continuous. No rule change does that with the current clip.
- D changes the data extent and leaves the rule alone. B changes the rule and still needs the padding.
- B gives each centre line its own source evidence and adds the 2.6 km below Chatfield dam. It costs a new request, a new property, an amendment, and unwanted pond-seeded creeks unless narrowed.
- D shows water on the Jefferson County side of the river. That is where the source puts the river.
- C is quick and needs no request, but the result is fragments and a new kind of exception.

## RISKS

- Padded water outside the county outline could be read as coverage there. The manifest wording has to say it is not.
- D rests on one short segment. The build check is the safeguard; the area categories corroborate the result today.
- Features wholly outside the saved pages' bounding box but inside the padding were measured for the South Platte only. For other rivers this is not established.
- NHD is retired and not maintained; a later source migration could change segment structure for any option.
- Not established: how the padded line reads on the phone in the real application. The preview is a plain SVG.

## RECOMMENDATION

Option D. It restores exactly the behaviour the approved specification describes, keeps O9 intact, needs no new source layer and no new kind of exception, and produces one group, one line, 73.2 km, with 0.97 of the drawable river drawn. The source's own area categories agree with it. If the owner later wants each centre line to carry its own evidence, the narrow form of B can be added on top without undoing anything. Proposed wording for the specification, section 5:

> **Douglas water extent.** The Douglas water layers (NHD flowlines and waterbodies) are fetched for, and clipped to, the Douglas County coverage polygon enlarged by 0.005 degrees (about 500 m), the same water padding Aspen uses. Every other Douglas layer stays clipped to the county polygon. Water in the padded strip is source geometry outside the county; nothing else is known there. The selection and grouping rules of sections 8.2 and 8.3 are unchanged. The South Platte River (`gnis_id` 00201759) is listed in `expected_major_rivers` for Douglas with a minimum drawn fraction of 0.8.

## WHAT CHANGES IF APPROVED

- Specification: the paragraph above in section 5; the "Wide rivers" paragraph of 8.3 corrected to say the 76 m segment is 11.5 m outside the county and inside the padded extent.
- Request: one controlled repeat of the two Douglas NHD queries with the padded extent, authorised explicitly, or an offline re-clip of the saved raw pages if the owner prefers no request.
- Data: Douglas `research.json` waterways gain about 337 features and waterbodies about 25; the snapshot document and the ID map gain an addendum. No existing feature inside the county changes except that segments cut at the county line become longer.
- Manifest: `extent_padding_deg` 0.005 on the two Douglas water layers; the coverage and water limitation sentences say water extends about 500 m past the county line.
- Configuration: `expected_major_rivers` for Douglas lists the South Platte.
- Display: rebuilt; the South Platte appears as one feature, `nhd-gnis-00201759`.

## WHAT REMAINS UNCHANGED

- Sections 8.2 and 8.3, invariants G1 to G10 and owner decision O9.
- Aspen, in every respect.
- Every non-water Douglas layer, byte for byte. The county coverage polygon.
- No area layer, no new property, no reviewed inclusion, no invented or joined geometry.
- Happy Canyon Creek, Kinney Creek and the truncated East Cherry Creek stay as they are.
- No claim about access, fishing or boating on the river.

## TESTS REQUIRED

- The South Platte is one group, `nhd-gnis-00201759`, one connected line, with members running through Cheesman Lake, Strontia Springs Reservoir and Chatfield Lake.
- Its drawn fraction is at least 0.8 (measured 0.97).
- Negative: with the padding set to zero the group is absent and the build fails on `expected_major_rivers`.
- Negative: no member has another `gnis_id`; the North Fork South Platte River (00183164) is not absorbed; the canal-coded outlet segment and the reach below Chatfield dam are not drawn and appear in the selection report.
- Every drawn coordinate comes from a canonical member; no line is added.
- No Douglas water feature lies further from the county polygon than the padding.
- Non-water layers are byte-identical before and after.
- The grouping report lists the new stub groups (Wigwam, Brush, Gunbarrel creeks).
- Byte budgets hold. The river is inspected on the rendered map and on the phone.

## ROLLBACK

Set the padding back to zero and rebuild, or revert the commit. A re-clip at zero padding reproduced the current 2,359 features and the same rule totals in this prototype; byte identity of the rebuilt file was not tested. No rule, identifier scheme or interface change needs undoing.

## REQUESTS MADE

Four read-only requests to `hydro.nationalmap.gov`, on 2026-10-06 local time (about 03:14 UTC on 2026-10-07). Each succeeded on the first attempt. Responses are saved outside every repository.

1. Flowlines, 372 features, 245,316 bytes:
   `https://hydro.nationalmap.gov/arcgis/rest/services/nhd/MapServer/6/query?where=gnis_id%3D%2700201759%27&geometry=-105.35,39.10,-104.95,39.60&geometryType=esriGeometryEnvelope&inSR=4326&spatialRel=esriSpatialRelIntersects&outFields=permanent_identifier,gnis_id,gnis_name,ftype,fcode,reachcode,lengthkm,visibilityfilter,wbarea_permanent_identifier,fdate,OBJECTID&outSR=4326&returnGeometry=true&orderByFields=OBJECTID&resultRecordCount=500&resultOffset=0&f=geojson`
2. Area polygons the centre lines reference, 6 features, 814,538 bytes:
   `https://hydro.nationalmap.gov/arcgis/rest/services/nhd/MapServer/9/query?where=PERMANENT_IDENTIFIER+IN+(%27117822685%27,%27117824517%27,%27117824519%27,%27117824529%27,%27117824543%27,%27117824547%27,%27120654507%27)&outFields=PERMANENT_IDENTIFIER,GNIS_ID,GNIS_NAME,FTYPE,FCODE,AREASQKM,VISIBILITYFILTER,FDATE,OBJECTID&outSR=4326&returnGeometry=true&resultRecordCount=500&f=geojson`
3. Waterbodies the centre lines reference, 4 features, 191,222 bytes:
   `https://hydro.nationalmap.gov/arcgis/rest/services/nhd/MapServer/12/query?where=PERMANENT_IDENTIFIER+IN+(%27117822739%27,%27117834809%27,%27120030962%27,%27117822685%27,%27117824517%27,%27117824519%27,%27117824529%27,%27117824543%27,%27117824547%27,%27120654507%27)&outFields=PERMANENT_IDENTIFIER,GNIS_ID,GNIS_NAME,FTYPE,FCODE,AREASQKM,ELEVATION,REACHCODE,VISIBILITYFILTER,FDATE,OBJECTID&outSR=4326&returnGeometry=true&resultRecordCount=500&f=geojson`
4. Category of every area the Douglas centre lines reference, attributes only, 26 features, 6,301 bytes:
   `https://hydro.nationalmap.gov/arcgis/rest/services/nhd/MapServer/9/query?where=PERMANENT_IDENTIFIER+IN+(%27117797757%27,%27117824517%27,%27117824519%27,%27117824529%27,%27117824543%27,%27120656953%27,%27120656961%27,%27120656968%27,%27120656969%27,%27120656970%27,%27120656971%27,%27120656974%27,%27120656977%27,%27120657003%27,%27120657004%27,%27120657006%27,%27120657007%27,%27120657008%27,%27120657037%27,%27120657041%27,%27120657064%27,%27120657065%27,%27120657066%27,%27120657067%27,%27120657068%27,%27120657069%27)&outFields=PERMANENT_IDENTIFIER,GNIS_ID,GNIS_NAME,FTYPE,FCODE,AREASQKM,VISIBILITYFILTER,FDATE,OBJECTID&returnGeometry=false&resultRecordCount=500&f=json`

## HOW THIS WAS COMPUTED

- Canonical data: `v2/regions/douglas-co/research.json` in the `m4a-source-preservation` worktree at commit `aa5c20b`, read only.
- Also read: the saved M4-A raw pages in that worktree's ignored `v2/pipeline/data/raw/m4a-nhd-refresh/` (3,607 named Douglas flowlines, unclipped; 2,277 waterbodies). The padded scenarios for other rivers come from these pages.
- Scripts, all in `/private/tmp/claude-501/-Users-kylekopacek-orca-workspaces-Ohvernight-m3-foundation/1af2c3f1-290d-4195-82ce-da82ec9d5e39/scratchpad/m4/prep/south-platte/`:
  - `analyze.py`: source characterisation, clip fragmentation, every rule and padding; writes `results.json`. In this script rule code `D` means the narrow form of Option B; the packet's Option D is rule `A` on a padded extent.
  - `extras.py`: per-river differences, waterbody counts, what remains undrawn; writes `extras.json`.
  - `degpad.py`: the 0.005 degree padding; writes `degpad.json`.
  - `build_preview.py`: the prototype GeoJSON files and the preview page.
  - `grouping.py` and `diag_south_platte.py`: unedited copies of the earlier dry-run scripts, for reference.
- Prototype geometry, same folder: `proto-B1-current-clip.geojson`, `proto-B2-pad500m.geojson`, `proto-C-reviewed-inclusion.geojson`, `proto-D-pad500m-approved-rule.geojson`. Raw responses are in `raw/`.
- Run with the pipeline's own interpreter (shapely 2.1.2, pyproj 3.8.0), with bytecode writing off so that nothing is written into the worktree.
- Method: lengths are geodesic on GRS80; distances and buffers are in UTM zone 13N. Adjacency is the specification's: end points equal after rounding to six decimals. "Visible pieces" counts connected drawn lines, so a clipped segment with two disjoint lines counts twice; "groups" counts the specification's parts. Padded extents were clipped to the buffered county polygon, as the pipeline's clip does; the whole-segment variant is shown in brackets under Option B. Display bytes are compact GeoJSON at six decimals. Canonical byte figures for padded extents are estimates from geometry bytes plus the average property size.
- Check: re-clipping the raw pages at zero padding reproduces the canonical 2,359 flowline features and the dry run's 35 groups and 1,608 drawn segments.
