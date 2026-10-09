DRAFT - UNREVIEWED

# M5 input — what the repository holds for land today

Read-only audit, 2026-10-07. Measured from the files in the
`m4a-source-preservation` worktree at `aa5c20b`: `v2/map-data-v2.json`
(sha256 `d244adea…`), `v2/regions/douglas-co/research.json` (`cf7e6852…`), the
display artifacts, both manifests, the fetch scripts and `v2/explore/`. No
network request was made. Areas and lengths are computed in NAD83 / UTM 13N
(EPSG:26913), the pipeline's own metric projection. Nothing here is a decision
or a recommendation to build.

Each statement is marked **VERIFIED** (measured or read from a file),
**INFERENCE** (reasoned from measurements or general knowledge, not checked
against the source) or **UNKNOWN**. Candidate replacement sources are in
`docs/research/future-sources/source-watchlist-m5-m8.md` and are not repeated.

## Key findings

1. **Each region's land layer is a handful of agency-wide aggregates, not
   areas.** Aspen holds 3 polygons, Douglas 5. Each is one MultiPolygon per
   agency code. The USFS feature is source `OBJECTID` 413 and the PVT feature
   is `OBJECTID` 1069 in *both* regions, 170 km apart, so the stored features
   are clips of the same source rows. (VERIFIED.) The source layer is therefore
   dissolved by agency code over a very large area. (INFERENCE.) There is no
   forest name, unit name, parcel or any identifier below "the agency".
2. **The polygons tile each extent completely.** Land polygons cover 100.00%
   of the Aspen extent (1 m² uncovered of 1,197.8 km²) and 100.00% of Douglas
   County (40 m² of 2,180.8 km²). (VERIFIED.) The approved legend line
   "Unshaded land is unknown — not private, not public, not open" (W5)
   describes a condition that does not occur anywhere inside either region.
3. **`PVT` is the residual class and it is large.** It is 13.1% of Aspen and
   71.8% of Douglas County. (VERIFIED.) Because the tiling is complete, every
   place the source does not attribute to a listed agency carries `PVT`.
   (INFERENCE.) In Douglas, 12 of 14 named waterbodies over 5 ha, including
   Cheesman Lake, Rueter-Hess Reservoir and Aurora-Rampart Reservoir, fall
   100% inside the `PVT` polygon (VERIFIED); several of those are municipal
   utility waters (INFERENCE, general knowledge). The trust rule "non-federal
   is not private" is met in wording but the map shades non-federal land with
   the source's private code almost everywhere.
4. **The data cannot answer "can I be here / camp here" for any spot, and
   says so.** Every land feature carries `camping_permission: "unknown"` in
   Aspen; neither region carries an access field; both manifests set
   `public_access` and `camping_permission` to `none`. (VERIFIED.) What M5
   inherits is context only.
5. **The two regions publish the same source under two schemas.** Different
   layer id, id prefix, property set, classification field, freshness policy,
   evidence wording and `confidence` value. Aspen additionally publishes a
   derived `manager` value of `Private` that the app never reads. (VERIFIED.)
6. **Geometry is coarse and noisy.** Typical vertex spacing is 105–190 m per
   vertex with segments up to 400 m; Aspen's USFS polygon has 142 parts of
   which 127 are under 1 ha and 40 under 100 m². Land polygons do not overlap
   each other. (VERIFIED.)
7. **Wilderness carries no name and disagrees with the land layer at the
   edges.** Aspen's three wilderness polygons keep only an id; 3.57 km² of
   designated wilderness lies on the `PVT` land polygon. Douglas has an empty
   wilderness layer. (VERIFIED.)

## 1. Source and fields

| | Aspen | Douglas County |
|---|---|---|
| Service and layer | `BLM_Natl_SMA_LimitedScale/MapServer/1` | same |
| Script | `v2/pipeline/scripts/01_fetch_land_ownership.py` | `v2/pipeline/scripts/enrich_douglas.py` |
| Request | bbox of `aoi.geojson`, `outFields=*`, native JSON, one feature per page | bbox of county boundary, same options |
| Clip | project rectangle | Census county polygon (GEOID 08035) |
| Canonical location | `map-data-v2.json` `/layers/land_ownership` | `research.json` `/layers/land` |
| Retrieved | 2026-09-25 | 2026-09-27 |
| Features | 3 | 5 |

All VERIFIED from the scripts and files.

Fields kept:

| Property | Aspen | Douglas | Origin |
|---|---|---|---|
| `id` | `sma-<OBJECTID>` | `land-<OBJECTID>` | source `OBJECTID`, prefixed |
| `raw_admin_agency` | yes (uppercased) | no | source `ADMIN_AGENCY_CODE` |
| `manager` | derived class (`BLM`, `USFS`, `Private`) | source code verbatim (`USFS`, `OTHFE`, `ST`, `LG`, `PVT`) | see section 3 |
| `name` | no | yes; always equal to the code | fallback chain ends at the code |
| `land_class` | `"unknown"` constant | no | pipeline constant |
| `camping_permission` | `"unknown"` constant | no | pipeline constant |
| `evidence` | yes | yes | pipeline |

Fields dropped: every other attribute of the source layer. Both scripts read
only `OBJECTID` and `ADMIN_AGENCY_CODE` from the response. (VERIFIED.) The
repository does not record what else the layer offers (unit or department
name, state, acreage, source scale, edit date), so the list of dropped fields
is UNKNOWN from repository evidence alone.

Stable identifier: none beyond `OBJECTID`. `OBJECTID` is a service row number;
the repository holds no evidence that it survives republication. (UNKNOWN.)
Because one row is an entire agency's holdings, even a stable `OBJECTID` would
identify "USFS", not a place.

## 2. Codes, counts and area

Share is of the region extent. Parts are polygon parts of the MultiPolygon.

**Aspen** (extent 1,197.8 km²)

| Code | Source OBJECTID | Area km² | Share | Parts | Holes | Vertices | Perimeter km |
|---|---|---|---|---|---|---|---|
| `USFS` | 413 | 1,039.2 | 86.76% | 142 | 98 | 3,597 | 472.8 |
| `PVT` | 1069 | 157.2 | 13.12% | 110 | 139 | 3,630 | 383.5 |
| `BLM` | 25 | 1.36 | 0.11% | 3 | 0 | 44 | 8.3 |
| no polygon | — | 0.000001 | 0.00% | — | — | — | — |

**Douglas County** (extent 2,180.8 km²)

| Code | Source OBJECTID | Area km² | Share | Parts | Holes | Vertices | Perimeter km |
|---|---|---|---|---|---|---|---|
| `PVT` | 1069 | 1,565.9 | 71.80% | 62 | 8 | 4,548 | 486.6 |
| `USFS` | 413 | 570.4 | 26.16% | 3 | 39 | 2,354 | 332.0 |
| `LG` | 1055 | 19.1 | 0.87% | 8 | 1 | 557 | 52.5 |
| `OTHFE` | 1017 | 14.4 | 0.66% | 2 | 0 | 1,027 | 34.9 |
| `ST` | 1028 | 11.1 | 0.51% | 7 | 0 | 143 | 39.9 |
| no polygon | — | 0.00004 | 0.00% | — | — | — | — |

All VERIFIED. Observations on what the small classes are:

- `OTHFE` (14.3 km² main part): Chatfield Lake lies 100% inside it.
  (VERIFIED.) The code says "Other Federal" and nothing about which agency or
  who runs recreation there. (VERIFIED from the data; which agency is
  UNKNOWN from the repository.)
- `ST`: seven parts of 82–264 ha whose boundary segments have a median length
  of 400 m, i.e. quarter-mile survey-grid shapes. (VERIFIED.) These look like
  survey-section trust parcels rather than parks. (INFERENCE.)
- `LG`: one 14.5 km² part centred near 39.433, −105.063 and one 4.5 km² part
  near 39.346, −104.758, plus six fragments under 1 ha. (VERIFIED.) Which
  local body, and whether a state park sits inside or beside either, is
  UNKNOWN; the 14.5 km² part is where Roxborough is commonly mapped
  (INFERENCE, to be checked).
- No Douglas recreation site falls outside the `USFS` polygon (36 of 36
  inside it). (VERIFIED.)

## 3. How codes become classes, and what falls to Unknown

Aspen pipeline mapping (`MANAGERS` in `01_fetch_land_ownership.py`):

| Source code | Aspen `manager` | In Aspen data | In Douglas data |
|---|---|---|---|
| `USFS` | `USFS` | 1 feature | 1 |
| `BLM` | `BLM` | 1 | 0 |
| `NPS` | `NPS` | 0 | 0 |
| `FWS` | `FWS` | 0 | 0 |
| `ST` | `State_CO` | 0 | 1 (unmapped; verbatim) |
| `LG` | `Local` | 0 | 1 (verbatim) |
| `PVT` | `Private` | 1 | 1 (verbatim) |
| anything else, incl. `OTHFE` | `Unknown` | 0 | `OTHFE` ×1 (verbatim) |

Zero features fall to `Unknown` in the published data. (VERIFIED.) Douglas
applies no mapping at all.

The app does not use the derived value. Both manifests set
`classification_source_field` to the raw code (`raw_admin_agency` in Aspen,
`manager` in Douglas) and `land-style.js` labels from that field. No file
under `v2/explore/` or `v2/*.js` reads `manager` in Aspen. (VERIFIED.) The
display artifact still ships Aspen's `manager: "Private"`, `land_class` and
`camping_permission` to the browser.

App-side classes (`land-style.js`): six known codes `USFS`, `BLM`, `OTHFE`,
`ST`, `LG`, `PVT`, each with a tint; any other code is drawn grey and labelled
"`<code>` — unrecognised source code; unknown" (W6). `NPS` and `FWS`, which
the Aspen pipeline treats as known agencies, have no W8 label and would be
shown as unrecognised. (VERIFIED from code; neither code is present today.)

## 4. Where there is no polygon

Inside either extent: effectively nowhere (section 2). Outside the extent
nothing is drawn; the coverage statement says "Nothing is known outside it."
Where a land layer is switched off or fails to load the map shows the basemap
only. The legend always ends with W5. (VERIFIED from `land-style.js`.)

So the reader's actual experience is the reverse of what W5 prepares them
for: there is no unshaded land to read as unknown; there is a tinted `PVT`
area over 13% of Aspen and 72% of Douglas County.

## 5. Scale and generalisation

| Measure | Aspen USFS | Aspen PVT | Douglas USFS | Douglas PVT | Douglas OTHFE | Douglas ST |
|---|---|---|---|---|---|---|
| Perimeter per vertex (m) | 131 | 106 | 141 | 107 | 34 | 279 |
| Segment length p50 / p90 (m) | 64 / 336 | 64 / 332 | 39 / 404 | 35 / 398 | 16 / 79 | 400 / 408 |
| Parts under 1 ha | 127 of 142 | 37 of 110 | 1 of 3 | 9 of 62 | 1 of 2 | 0 of 7 |
| Parts under 100 m² | 40 | 25 | 1 | 6 | 0 | 0 |
| Parts under 1 m² | 9 | 12 | 0 | 2 | 0 | 0 |
| Holes under 1 ha | 32 of 98 | 124 of 139 | 3 of 39 | 2 of 8 | — | — |

All VERIFIED. Further measurements:

- Overlap between land polygons: 0 m² for every pair in both regions. Shared
  USFS–PVT boundary: 352.6 km in Aspen, 251.1 km in Douglas.
- Only 1 of Aspen USFS's 127 small parts touches the extent edge, so the
  slivers are internal noise along the USFS–PVT line, not clipping residue.
- Coordinates are stored with 14–15 decimal places; the display artifact
  rounds to six and drops 20 degenerate parts in Aspen and none in Douglas
  (`display/index.json`). Area change from rounding is under 320 m² per
  polygon.
- Vertex density varies by class within one layer (Douglas `OTHFE` 34 m per
  vertex against `ST` 279 m), so the layer mixes source scales. (VERIFIED
  measurement; cause INFERENCE.)
- Both manifests declare `spatial_precision: generalized`; the source name
  says "LimitedScale". The actual source scale is not recorded. (UNKNOWN.)

**Land against wilderness (Aspen).** Three wilderness polygons, 782.9 km²,
65.4% of the extent, no overlap among them, 36–104 m per vertex (finer than
land). 99.5% of wilderness area lies in the `USFS` polygon; 3.57 km² lies on
the `PVT` polygon (0.56, 0.22 and 2.79 km² per polygon). (VERIFIED.) Whether that is private inholding
or two sources drawn at different scales is UNKNOWN. Wilderness is declared
`source_published` and drawn with a solid outline; land is `generalized` and
loses its outline at zoom 14.

**Linear features against land.** 11.1 km of Aspen's 339.1 km of USFS trail
(16 features with more than 50 m each) and 1.0 km of its 65.0 km of MVUM road
run over the `PVT` polygon. In Douglas, 1.4 km of trail and 1.7 km of road do.
(VERIFIED.)

## 6. How the two regions differ

| Aspect | Aspen | Douglas |
|---|---|---|
| Layer id | `land_ownership` (register item N5) | `land` |
| Feature id | `sma-413` | `land-413` (same source row) |
| Classification field | `raw_admin_agency` | `manager` |
| Meaning of `manager` | derived class | source code |
| `fields.derived` | `manager` | none |
| Extra constants | `land_class`, `camping_permission` | none |
| `name` | absent | the code |
| `max_age_hours` | `null` (never reported stale) | 168 (already past policy) |
| Transport record | script-level `completed_at` | per-layer `retrieved_at`, `count` |
| `evidence.agency` | "BLM multi-agency Surface Management Agency" | "BLM multi-agency" |
| `evidence.confidence` (deprecated) | `high` | `unverified` (N4) |
| `evidence.notes` | limitation sentence | empty |
| Wilderness properties | `id`, `evidence` | layer empty; manifest declares `manager` |
| Coverage boundary | project rectangle | county boundary |
| Ownership statement | "Limited-scale managing-agency polygons only…" | "Five limited-scale management polygons only…" |

All VERIFIED.

## 7. What the detail sheet says

For a land polygon (`ExploreLand.detail`), in order: "Source classification:
`<code>`"; the class label (for example "USFS — Forest Service; generalized
source class", or "PVT — the source's generalized private class; not a
parcel-level finding"); the evidence agency; a source link; "Source fetched
`<date>`"; W7 (limited-scale boundary, cannot locate a property line); W3
(ownership or management does not establish public access); the manifest's
ownership statement; its public-access statement; the layer limitation. The
title is the class label. (VERIFIED.)

It makes no claim of access, permission or ownership of a spot. It also does
not say which forest or unit, how large the area is, or anything specific to
the place tapped: every tap inside the USFS aggregate returns the same sheet.

For a wilderness polygon (`ExploreEvidence.feature`): title "Wilderness" (no
name is stored), then "USFS", "Source fetched 2026-09-25", and "Designated
wilderness boundaries. Not a statement of current rules or access."
(VERIFIED.) Which of the two overlapping layers a tap selects in Aspen was not
tested. (UNKNOWN.)

## 8. Where ownership, management and access can be confused

- The source is a *surface management agency* dataset; the fact dimension in
  the manifest is `ownership`; the Aspen layer id says `land_ownership`; the
  layer title says "Land management context". `PVT` is an ownership idea
  inside a management field.
- A reader meets `PVT` over most of Douglas County, including public
  reservoirs, and may read "private, keep out". The contract says a private
  classification does not itself establish that access is prohibited (rule
  12), and W3 says so, but the tint says something first.
- A reader meets `USFS` over 87% of Aspen and may read "national forest, I
  can camp". The same polygon contains 783 km² of designated wilderness and
  every developed site, closure and order; the data distinguishes none of
  them.
- `OTHFE`, `ST` and `LG` name a level of government, not a manager or a rule
  set. State trust land, a state park and a county open space would all need
  different answers to "can I be here".
- Trails and roads published by the Forest Service cross the `PVT` polygon
  (section 5). The map gives no way to tell an easement from a generalisation
  error.
- Aspen's canonical and display files carry the bare word `Private`, which
  the presentation rules forbid as a label. It is not shown, but it is
  published.

## 9. Deficiencies

Classification: DATA GAP, TRUST ISSUE, OWNER DECISION, IMPLEMENTATION DETAIL,
FUTURE TECH DEBT.

| # | What | Evidence | Why it matters for "can I be here / camp here" | Class |
|---|---|---|---|---|
| L1 | One aggregate polygon per agency; no unit, forest or place identity | 3 and 5 features; OBJECTID 413 and 1069 shared across regions | The answer to any spot is "somewhere in USFS" — no handle for unit-specific rules, orders or contacts | DATA GAP |
| L2 | `PVT` is the residual class and dominates | 71.8% of Douglas, 13.1% of Aspen; 100% tiling; public reservoirs inside `PVT` | Public non-federal land is presented with the private code; a user is steered away from places that may be open, and learns nothing about the ones that are private | TRUST ISSUE |
| L3 | Legend promise "unshaded land is unknown" never applies | 1 m² and 40 m² uncovered | The approved safeguard for unknown land protects no real location; unknown is not visible on the map | TRUST ISSUE |
| L4 | No access or permission dimension at all | manifests: `public_access` and `camping_permission` state `none` | The layer cannot contribute to the question; it can only be mistaken for an answer | DATA GAP |
| L5 | State and local land is undifferentiated and tiny | `ST` 0.51%, `LG` 0.87% of Douglas; none in Aspen | State parks, wildlife areas, trust land and county open space, where rules differ most, are absent or indistinguishable | DATA GAP |
| L6 | "Other Federal" does not name an agency | `OTHFE` 14.4 km² containing Chatfield Lake | The user cannot tell whose rules apply | DATA GAP |
| L7 | Coarse, noisy boundaries | 105–190 m per vertex; 400 m segments; 127 of 142 Aspen USFS parts under 1 ha | Near any boundary the layer cannot say which side a campsite or pull-out is on; slivers can be tapped and described as a class | TRUST ISSUE (held by W7 today) |
| L8 | Wilderness has no name and no rule context | properties are `id` and `evidence` only | Wilderness is where vehicle, bicycle and group rules change; the user is told only "Wilderness" | DATA GAP |
| L9 | Wilderness and land disagree at the edge | 3.57 km² of wilderness on `PVT` | The user sees contradictory context with no explanation | TRUST ISSUE |
| L10 | Empty Douglas wilderness layer is indistinguishable from "no wilderness" | 0 features, status `available` | An empty layer means unknown under the trust principles; whether it is truly empty is unverified | TRUST ISSUE |
| L11 | Forest Service trails and roads cross `PVT` | 11.1 km and 1.0 km in Aspen; 1.4 and 1.7 km in Douglas | A user on a mapped trail is shown "private" beneath it, or infers access from the trail; neither is supported | TRUST ISSUE |
| L12 | Two schemas for one source | section 6 | Any M5 classification must be written twice or the regions will drift; identical source rows have different ids | IMPLEMENTATION DETAIL |
| L13 | Aspen publishes derived `Private`, `State_CO`, `Local` vocabulary nobody reads | `manager` in canonical and display files; no reader in `v2/explore/` | Published wording the owner has not approved; a second mapping to keep correct | FUTURE TECH DEBT |
| L14 | Known federal codes `NPS`, `FWS` would display as "unrecognised … unknown" | W8 has no entry; pipeline map does | A national park or refuge in a future region would be labelled unknown | FUTURE TECH DEBT |
| L15 | No stable source identifier and no source attributes kept | only `OBJECTID` and the code | Changes between refreshes cannot be detected or explained; nothing to join to another source | DATA GAP |
| L16 | Freshness policy differs for the same source | `null` in Aspen, 168 h in Douglas | Douglas shows "refresh needed" while identical Aspen data never does | OWNER DECISION |
| L17 | Layer id and fact name say ownership; source says management | N5; `fact_coverage.ownership` | The vocabulary M5 must build on already merges the two ideas the roadmap says to keep apart | OWNER DECISION |
| L18 | Reserved tier A ("authoritative classification") has no definition | M3 specification section 13 reserves it for M5 | Without a definition, a better source could be drawn with more certainty than it carries | OWNER DECISION |
| L19 | False coordinate precision in canonical files | 14–15 decimals on a limited-scale source | Not user-visible; inflates files and suggests precision to a data reader | IMPLEMENTATION DETAIL |

## Questions for the owner

1. Is `PVT` shading acceptable as it stands, given that it is the source's
   residual and covers 72% of Douglas County? Should residual land be shown
   as a class, as unknown, or not at all?
2. W5 never applies today. Should the wording, or the thing it describes,
   change?
3. What is the unit of land a user should be able to tap: an agency, a named
   unit (a forest, a park, an open space), or a parcel?
4. Which distinctions matter first for the pilot: federal agency and unit;
   state park against trust land against wildlife area; county and municipal
   open space; private? Which of them is M5 allowed to leave as unknown?
5. Is "ownership" or "management" the dimension Ohvernight publishes? If
   both, which source is allowed to speak for which?
6. Should a land class ever be allowed to say anything about access, or does
   access remain a separate reviewed claim, as M4 does for water?
7. Is the same freshness policy wanted for both regions?
8. May the Aspen layer id `land_ownership` be renamed, and may the unused
   derived `manager` vocabulary be removed from published data?
9. Does wilderness belong to M5 (as a land class or overlay) or to a later
   rules milestone? Should its name be published?
10. What should the map say where a Forest Service trail crosses land the
    land layer calls `PVT`?

## What an M5 specification must settle

- The classification vocabulary, who defines each class, and the rule for
  codes outside it; one mapping for all regions.
- The precise meaning of "unknown" on the map when the source tiles the whole
  extent, and how unknown is drawn.
- Whether `PVT` from a limited-scale source may be published as a class at
  all, and under what wording.
- The feature model: what one land record is, what its stable identifier is,
  and which source attributes are preserved (the M4-A source-preservation
  pattern is the nearest precedent).
- Which source speaks for which class, how two sources are reconciled where
  they disagree, and how the spatial precision of each is declared and
  drawn, including the definition of tier A.
- A sliver and minimum-area policy, and whether land polygons below it are
  selectable.
- The relationship of wilderness and other designations to the land class
  beneath them.
- One schema for both regions, and a migration for the Aspen layer id,
  feature ids and constants without breaking saved state.
- The freshness policy for land, and what a failed or empty refresh shows.
- The evidence required before any land record contributes to an access or
  camping statement, and confirmation that until then it contributes none.
- Acceptance measurements: share of each extent by class, share unknown,
  count and area of residual-class land, and agreement with at least one
  independent boundary source, measured on the real Aspen and Douglas data.
