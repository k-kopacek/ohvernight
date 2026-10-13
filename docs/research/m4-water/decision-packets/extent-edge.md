# Extent-edge decision packet

Clipping to the region edge turns exactly one displayed river into several tappable rivers: Granite Creek in Aspen (three groups, 1.58 km drawn in total, about three quarters of the creek lies outside the extent); Douglas County has none apart from the South Platte, which is handled separately. **Recommendation: accept region-edge splitting for M4 (Option A), and write down one clarification the build already relies on — a single source segment that the clip cut into several lines stays one member.** A read-only prototype shows that fetching source geometry 250 m beyond the Aspen extent would make Granite Creek one group, but it needs a second live fetch, a contract change and new pipeline and validator rules to fix one small creek.

## DECISION

Should a river that leaves and re-enters the region stay split into separate same-named groups (accept), or should the pipeline fetch source geometry beyond the edge, for connectivity only, so that it becomes one group?

## EVIDENCE

Read-only analysis of the M4-A canonical data (commit `aa5c20b`) under the approved grouping rule, plus one small read-only prototype fetch for Aspen (two requests, listed below).

**Boundaries used.** Aspen: the rectangle west -107.055, south 38.995, east -106.565, north 39.265. This is `v2/pipeline/config/aoi.geojson` plus 0.005 degrees, and equals the bounds of the flowline data exactly. Douglas: the county polygon at `/layers/coverage`; distances are to the polygon boundary, not to a bounding box.

**How often clipping creates extra user-facing groups.**

| | Aspen | Douglas County |
|---|---:|---:|
| Displayed rivers (`gnis_id`) / groups | 67 / 71 | 35 / 35 |
| Rivers with more than one displayed group | 3 | 0 |
| ... caused by the extent edge | **1** (Granite Creek, 3 groups) | **0** |
| ... caused by an excluded connector | 2 (Hunter Creek, Galena Creek; see the connector packet) | 0 |
| ... other cause | 0 | 0 |
| Groups with a free end within 30 m of the boundary | 27 of 71 (25 rivers) | 17 of 35 (17 rivers) |
| Single-group rivers simply cut off at the edge | 24, with 179.8 km drawn (35% of 514.4 km) | 17, with 261.4 km drawn (61% of 428.8 km) |

So the edge creates 2 extra groups out of 71 in Aspen and none in Douglas. Being cut off at the edge is common and unremarkable; being split by it is rare.

Douglas notes. Of the 17, six end on the western boundary (Plum, Bear, Pine, Fourmile, Sugar and Horse Creeks) and the local raw M4-A pages hold no segment of those rivers beyond the county, which is consistent with a mouth on the boundary river rather than a cut; ten end on the south or north edge, where the raw pages stop too, so this cannot be told locally; one (East Cherry Creek) has a source segment outside. The South Platte River (43 fragments, none displayed) is the county-boundary case being handled by another agent and is not analysed here. Two rivers have a second, hidden part at the boundary (East Cherry Creek, Coal Creek); neither produces a second displayed group.

**A finding the dry run had not surfaced.** Three Aspen groups are held together only because one source segment was cut by the clip into several lines and is still stored as one feature. Counted line by line, the drawn geometry is more fragmented than the group count suggests:

| River | Groups today | Separate drawn lines at the edge | Sizes of the drawn lines (km) |
|---|---:|---:|---|
| Granite Creek 00179785 | 3 | 5 | group 1: 0.595, 0.242, 0.031; group 2: 0.482; group 3: 0.233 |
| South Fork Fryingpan River 00179784 | 1 | 2 | 11.941 and 0.024 |
| South Fork Lake Creek 00180366 | 1 | 2 | 2.225 and 0.311 |

The approved rule joins end points of *segments*; a clipped segment keeps all its end points, so its pieces stay together. That is source-backed (one NHD feature, one `source_id`) and invents no geometry, but owner decision O2 says "no joining across extent-edge gaps", so it should be confirmed rather than assumed. If it were forbidden, Aspen would have 5 more groups, including one 24 m long.

**Is the Granite Creek split understandable from geometry alone?** Partly. All five drawn lines lie on the east edge within a 3.2 km stretch (latitude 39.224 to 39.253). The gaps between the three groups are 284 m and 881 m, both under 1 km, and every gap end is exactly on the edge, so with the coverage boundary visible it reads as one creek weaving along the border. But the pieces are small (0.03 to 0.6 km) and search or a list will show "Granite Creek" three times. The source `length_km` attribute overstates them (4.15, 0.70, 0.57 km stated; 0.87, 0.48, 0.23 km drawn), which is open question Q4.

**Padding prototype (Aspen).** Flowlines for 12 `gnis_id` values were fetched in a box 0.05 degrees beyond the extent: Granite Creek, South Fork Lake Creek, and the ten cut-off rivers with the most drawn length. 547 features came back. Inside the extent the live features match the canonical data exactly (415 of 415 source ids). Parts were then recomputed with source geometry clipped at each padding distance used for connectivity only; display stays clipped to today's extent. "Strict" counts each clipped line separately; the bracket is the count when a clipped segment is kept as one member (today's behaviour).

| River | 0 m (today) | 250 m | 500 m | 1 km | 2 km | 5 km | Resolves at |
|---|---|---:|---:|---:|---:|---:|---|
| Granite Creek | 5 [3] | 1 | 1 | 1 | 1 | 1 | 125 m |
| South Fork Fryingpan River | 2 [1] | 1 | 1 | 1 | 1 | 1 | 25 m |
| South Fork Lake Creek | 2 [1] | 1 | 1 | 1 | 1 | 1 | 150 m |
| Roaring Fork River, Snowmass Creek, Woody Creek, North Fork Crystal River, Bowman Creek, Tellurium Creek, West Snowmass Creek, Pine Creek, Bear Creek | 1 [1] | 1 | 1 | 1 | 1 | 1 | already one; padding changes nothing |

Resolving distances were found by stepping the padding in 25 m increments. The creeks leave the extent by very little: Granite Creek's loops go at most 60 m outside, and two segments wholly outside (at most 123 m out) complete the join. 250 m of padding resolves every edge split found in Aspen. Using same-`gnis_id` connectors as well made no difference to this table.

**Cost of the padded ring (Aspen).** Measured for the 12 fetched rivers; the last two columns are estimates for all named stream and centre-line segments, made from the density inside the extent (1.10 segments per square km, about 1.7 kB per canonical feature). They are estimates, not measurements.

| Padding | Segments of the 12 rivers touching the ring (new to the data / already held but clipped) | Their length in the ring | Estimated bytes for the 12 | Estimated all named segments in the ring | Estimated bytes |
|---|---|---:|---:|---:|---:|
| 250 m | 25 (7 / 18) | 10.4 km | 45 kB | about 40 | about 70 kB |
| 500 m | 35 (17 / 18) | 15.8 km | 67 kB | about 80 | about 135 kB |
| 1 km | 65 (47 / 18) | 22.3 km | 107 kB | about 165 | about 275 kB |
| 2 km | 95 (77 / 18) | 33.9 km | 154 kB | about 335 | about 565 kB |
| 5 km | 145 (127 / 18) | 59.2 km | 252 kB | about 905 | about 1.5 MB |

For scale, the Aspen canonical flowlines are 6,411 features and 9.27 MB, of which named stream and centre-line segments are 1,395 features and 2.35 MB. The 5 km row is a slight undercount east and west: 0.05 degrees is 5.6 km north-south but only 4.3 km east-west. A fetch limited to the three affected rivers at 250 m would be 11 segments.

**Douglas.** No displayed river is split by the county boundary, so padding would change no displayed group there today (South Platte aside). Local raw pages show East Cherry Creek's hidden second part would join its displayed part through one outside segment; nothing more would be drawn. Padding around a county polygon is a buffer of an irregular shape, not a rectangle, and the county's western boundary is itself a river.

## CURRENT BEHAVIOR

Specification 8.3 and O2: parts separated by a gap at the extent edge are separate groups with the same name; nothing is joined across the edge. Granite Creek is three groups (`nhd-gnis-00179785`, `-p2`, `-p3`). A source segment cut into several lines by the clip stays one member, which keeps South Fork Fryingpan River and South Fork Lake Creek as one group each. The grouping report lists the split.

## OPTION A

Accept region-edge splitting. No new fetch. Granite Creek stays three groups. Add one clarifying sentence so the clipped-segment behaviour is a stated rule, and make the grouping report show the split plainly. Recommended.

## OPTION B

Fetch source geometry in a padded ring beyond the extent (250 m is enough for Aspen) and use it for connectivity only; display stays clipped to today's extent and nothing in the ring is drawn, selectable or labelled. Granite Creek becomes one group drawn as five short lines. Wording if chosen: "Named stream and artificial-path segments within 250 m outside a region's water extent are kept as supporting features with `support_reason` `extent_edge_continuity`. They take part in connectivity for their own `gnis_id` only. They are never drawn, never selectable, never used for screening, never counted in any length, and never have a `group_id`."

## OPTION C

Treat every part of one `gnis_id` whose free ends are on the extent edge as one logical group without fetching anything (the third alternative in open question Q3). Not source-backed: the data held cannot show the pieces connect outside, and O2 forbids inferring it. Not recommended. (Hiding short parts under a minimum length was also floated in Q3; it removes real perennial water from the map and is likewise not recommended.)

## TRADEOFFS

| | A accept | B pad 250 m | C infer |
|---|---|---|---|
| Granite Creek | 3 groups, 5 short lines | 1 group, the same 5 short lines | 1 group |
| New live fetch | none | yes, both regions or Aspen only | none |
| Source-backed | yes | yes | no |
| Contract, pipeline, validator changes | none (one sentence in the specification) | several (see below) | rule change against O2 |
| Benefit today | n/a | one creek in Aspen; nothing in Douglas | one creek |

## RISKS

- A: three same-named entries for one small creek at the far north-east corner; a later region may have a more important river on its edge, where this would matter more.
- B: the specification allows exactly one live refresh in M4, already used; data would be stored outside the stated coverage ("nothing is known outside it"); Aspen's hydrology layer also feeds setback screening, so ring segments must be reliably excluded from it; one more class of hidden feature to validate. The ring-size figures are estimates.
- Both: this prototype covered 12 of Aspen's 32 edge-touching named rivers by live geometry. The other 20 are each a single connected part inside the extent, so padding cannot change their group count; that follows from the local data, not from the fetch.
- Uncertainty: nothing was fetched for Douglas. The Douglas statements rest on local canonical data and the local raw M4-A pages, which stop at the county's bounding box.

## RECOMMENDATION

Accept region-edge splitting for M4 (Option A). The edge splits one minor creek that lies mostly outside the region, and the cost of fixing it is out of proportion: a second live fetch, a contract change and new hidden-feature rules. Option B is proven workable at 250 m and is the right follow-up if the owner dislikes three Granite Creeks on the device, or when a later region puts a significant river on its edge. If a second controlled NHD request is approved anyway for the South Platte question, the ring could be added to that same request; this packet does not assume it.

Exact wording for specification 8.3:

> Grouping uses only source geometry held inside the region's water extent. Two reaches of one `gnis_id` that connect only through source geometry outside the extent are separate parts, and separate groups with the same name. M4 does not fetch geometry beyond the extent to join them and never infers continuity from nearness along the edge. One source segment (one `source_id`) that clipping has cut into several lines remains one segment and one member; its lines are drawn as clipped and nothing is drawn across the gap. The grouping report lists every `gnis_id` divided at the extent edge, with its groups, the number of separate drawn lines, their drawn lengths and the gaps between them.

## WHAT CHANGES IF APPROVED

- One paragraph added to specification 8.3 (above). No change to any group, id or drawn line.
- The grouping report gains a count of separate drawn lines per group, so edge fragmentation is visible (today: Granite Creek 5 lines in 3 groups; South Fork Fryingpan River and South Fork Lake Creek 2 lines in 1 group each).
- Granite Creek is recorded as a known, accepted edge split.

## WHAT REMAINS UNCHANGED

- All groups: Aspen 71 (69 if the connector packet is approved), Douglas 35.
- The extent, `extent_padding_deg` (0.005 for Aspen hydrology, 0 for Douglas), the canonical data, the fetch scope and the contract.
- No geometry invented; no join across an extent-edge gap between different source segments.
- The South Platte question, decided separately.

If Option B were chosen instead, in plain terms the pipeline would need: an authorised extra request to NHD layer 6 per region for the ring; storage of ring segments as supporting features with a reason; a larger `extent_padding_deg` for the water layer (Aspen from 0.005 to about 0.008; Douglas from 0 to a non-zero value, with a buffered county shape rather than a rectangle) and a revised coverage statement; two clip shapes instead of one (display and screening at today's extent, connectivity at the padded one); exclusion of ring segments from Aspen setback screening, from display, from every length and from the expected-river fraction; and validator rules and tests for all of that.

## TESTS REQUIRED

1. Fixture: two reaches of one `gnis_id` whose facing ends are both on the extent edge, with no held segment between them: two groups, same name, ids `...` and `...-p2`. Never one group, whatever the gap.
2. Fixture: one source segment stored as a MultiLineString of two lines (clipped): one member, one group; the display geometry contains both lines and no coordinate that is not in the canonical geometry (G9).
3. Fixture: two different source segments of one `gnis_id` with ends 1 m apart on the edge and no shared end point: two groups (no joining by nearness).
4. Real data: Granite Creek 00179785 is exactly three groups; South Fork Fryingpan River 00179784 and South Fork Lake Creek 00180366 are exactly one group each.
5. Report check: the grouping report lists Granite Creek as an extent-edge split with 3 groups and 5 drawn lines.

## ROLLBACK

Option A changes only specification text and the report, so rollback is reverting that paragraph; no data or display artifact changes. If Option B were adopted later, rollback would be: drop the ring features (they are marked by `support_reason`), restore `extent_padding_deg`, rebuild; drawn geometry would be identical either way, only group ids would change back.

## REQUESTS MADE

Two read-only GET requests to NHD MapServer layer 6, on 2026-10-06, by `curl -sL --max-time 120`. Both succeeded on the first attempt (500 and 47 features). Raw responses are stored only in `/private/tmp/claude-501/-Users-kylekopacek-orca-workspaces-Ohvernight-m3-foundation/1af2c3f1-290d-4195-82ce-da82ec9d5e39/scratchpad/m4/prep/extent-edge/` (`page-offset-0.json`, `page-offset-500.json`, `requests.txt`). Nothing fetched is in any repository.

1. `https://hydro.nationalmap.gov/arcgis/rest/services/nhd/MapServer/6/query?where=gnis_id%20IN%20('00179785','00180366','00174812','00175217','00179712','00179784','00175591','00180330','00180332','00175219','00180331','00175215')&geometry=-107.105,38.945,-106.515,39.315&geometryType=esriGeometryEnvelope&inSR=4326&spatialRel=esriSpatialRelIntersects&outFields=OBJECTID,permanent_identifier,gnis_id,gnis_name,ftype,fcode,reachcode,lengthkm,wbarea_permanent_identifier&outSR=4326&returnGeometry=true&returnZ=false&returnM=false&orderByFields=OBJECTID&resultRecordCount=500&f=geojson&resultOffset=0`
2. The same URL with `resultOffset=500`.

The twelve ids are Granite Creek, South Fork Lake Creek, Roaring Fork River, Snowmass Creek, Woody Creek, South Fork Fryingpan River, North Fork Crystal River, Bowman Creek, Tellurium Creek, West Snowmass Creek, Pine Creek and Bear Creek.

## HOW THIS WAS COMPUTED

- Data: worktree `/Users/kylekopacek/orca/workspaces/Ohvernight/m4a-source-preservation` at commit `aa5c20b`, read only: `v2/map-data-v2.json` (`/layers/hydrology`, flowlines), `v2/regions/douglas-co/research.json` (`/layers/waterways`, `/layers/coverage`), `v2/pipeline/config/aoi.geojson`, and the untracked local raw pages `v2/pipeline/data/raw/m4a-nhd-refresh/douglas-co-flowline-pages/`.
- Scripts (outside every repository), in `/private/tmp/claude-501/-Users-kylekopacek-orca-workspaces-Ohvernight-m3-foundation/1af2c3f1-290d-4195-82ce-da82ec9d5e39/scratchpad/m4/prep/connector-extent/`: `part2_local.py` (multi-part rivers, free ends, distance to the boundary), `fetch_padded.sh` (the two requests), `part2_padding.py` (parts at each padding, ring cost), `part2_extra.py` (loop excursions, drawn-line sizes, Douglas checks), all using an unmodified copy of the approved-rule script `grouping.py`. Outputs: `part2_local.txt`, `part2_padding.txt`, `part2_extra.txt` there.
- Method: a free end is a line end shared with no other line of the same part. Distances use a local equal-distance projection; the Douglas distance is to the county polygon boundary. For padding, each fetched feature was clipped to the extent grown by the stated distance, each resulting line was a node, nodes sharing an end point (six decimals) were joined within one `gnis_id`, and a part counted as displayed when it held a perennial named stream line inside today's extent. At 0 m this reproduces the approved result (3 groups for Granite Creek by segment, 5 by line).
- Limits: bytes are estimated from the average size of a canonical named flowline feature (726 bytes of properties plus about 45 bytes per vertex); the all-rivers ring columns scale by density and are rough. Lengths are from stored geometry unless marked as the source attribute.
