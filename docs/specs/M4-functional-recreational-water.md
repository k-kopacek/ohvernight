# Milestone 4 specification — Functional recreational water

**For:** Codex (implementation). **Reviewer / coordinator:** Claude. **Research:** Hermes. **Base:** `main` at `b45ca59`.
**Status:** APPROVED by the owner on 2026-10-06: architecture (decisions D1–D12, O1–O9) and the exact wording of section 10 (O5, with the owner's edits). Production implementation may begin in the approved order M4-A, then M4-B, then M4-C. M4-D remains optional and separately gated.
**Delivery:** four sequential pull requests, M4-A to M4-D (section 16). M4 is complete when A, B and C are merged. M4-D is optional.
**Owner decisions:** D1–D12 and O1–O9 of 2026-10-06 are recorded in section 21 and are binding on this document.

Governing documents: `AGENTS.md`, `ROADMAP.md`, `docs/architecture/agent-stack.md`, `docs/architecture/system-overview.md`, `docs/architecture/decisions/` (ADR-004, ADR-005, ADR-006), `docs/product/product-principles.md`, `docs/product/trust-principles.md`, `v2/pipeline/docs/data-contract.md`, `docs/specs/M3-unified-mobile-explore.md` (final, with amendments A1–A14), and the research record in `docs/research/m4-water/`.

## 1. Problem

The map shows every named hydrology line as water. In Aspen that is 1,512 line pieces and 43 waterbodies; in Douglas County 2,359 line pieces and 33 waterbodies. One river is many tappable pieces (Roaring Fork River: 112). Canals, ditches and pipelines are shown as if they were places to visit. Most Douglas "reservoirs" are structures. Only named lakes are shown, so most alpine lakes near Aspen are missing. Nothing says what an operator allows or prohibits at the few waters where that is published, including two where boating is prohibited.

The pipeline keeps a name and nothing else. Feature type, perennial or intermittent status, size and stable identifiers are discarded, and IDs are built from a service row number.

Evidence: [existing-data-audit.md](../research/m4-water/existing-data-audit.md), [field-semantics.md](../research/m4-water/field-semantics.md).

## 2. Goals

1. The water layer shows water a person might visit: perennial rivers and streams as whole rivers, and perennial lakes and reservoirs.
2. One river or stream is normally one selectable feature with one label, while every canonical source segment is preserved and traceable.
3. Selection is made from source fields, never from name keywords.
4. Physical water may be shown with every recreation and access property unknown. That is valid data (D12).
5. Where an operator or agency publishes what is allowed or prohibited at a water, a reviewed claim per activity says so, restrictions first.
6. The four-class evidence model (source fact, official recreation information, derived fact, community signal) is part of the architecture. M4 ships no community-signal records.
7. Water records are usable by M8: stable IDs, and activity claims that can be queried.

## 3. Out of scope

- Any M5 to M8 work. No ranking, no "near me", no trip planning.
- Switching the canonical source to 3DHP (D1).
- A separate intermittent-stream layer (D2).
- Displaying unnamed streams (D3).
- Ingesting, scraping or storing any third-party community or review content (D8).
- Persisting or republishing CPW structured data before its terms are resolved (D7).
- Inferring any activity claim from a ramp, a designation, stocking, proximity, existence, a name or community discussion (D6).
- Removing water by name keyword (D5).
- A new renderer, dependency, build step or basemap. Rotation, double-tap zoom, an overlap chooser and the other M3 deferrals stay deferred.
- Changes to land, trails, roads, camping or trip rules.
- Trail grouping (recorded for M6).

## 4. Evidence model

Four classes. Only the second can state that an activity is allowed, restricted or prohibited.

| Class | Meaning | Carried as | Contract home |
|---|---|---|---|
| Source fact | Stated by the geometry source: name, type, hydrographic category, length, area, identifiers | Feature properties with provenance | `fields.source`, `evidence` |
| Official recreation information | What an operator or agency states about one activity at one water | An activity claim (section 9) | New `water_recreation` registry |
| Derived fact | Computed by Ohvernight: group membership, grouped length, area in hectares | Feature properties, labelled as computed in the interface | `fields.derived` |
| Community signal | What people report | Not implemented in M4. Reserved shape in section 9.6 | — |

Rules:

1. A source fact about existence, designation or a facility never changes an activity claim.
2. A derived fact is never worded as a statement by a source.
3. A community signal can never establish legal access, ownership, permission, closure status or camping legality. No field in the schema lets it.
4. Unknown is the default for every activity and for access. Absence of a record means unknown, not allowed and not prohibited.

## 5. Canonical source and the M4 snapshot (D1, D9)

**Source.** USGS National Hydrography Dataset, `https://hydro.nationalmap.gov/arcgis/rest/services/nhd/MapServer`, layers 6 (flowline), 9 (area) and 12 (waterbody). Public domain. Retired by USGS on 1 October 2023 and no longer maintained. Its use in M4 is transitional (section 18).

**Refresh.** M4-A performs exactly one controlled live refresh of the NHD layers for both regions. It is the only live fetch authorised in M4. `RIDB_API_KEY` is not involved. No other source is refreshed: every non-water layer in the canonical bundles must be byte-identical before and after, and M4-A proves it.

**Scope fetched.**

| Region | Flowlines (layer 6) | Areas (layer 9) | Waterbodies (layer 12) |
|---|---|---|---|
| Aspen | All, within the existing padded extent (unchanged scope; this layer also feeds setback screening) | All (unchanged) | All (unchanged) |
| Douglas County | Features with a non-empty `gnis_name`, plus the minimum unnamed supporting features defined below (O1) | Not fetched (unchanged) | **All**, named or not (new: needed for D3) |

**Douglas supporting features (O1).** The roughly 34,000 unnamed Douglas flowlines are not fetched. After the named features are fetched, M4-A computes the parts of each `gnis_id` (section 8.3). Where two parts of one `gnis_id` have end points within 250 m of each other, M4-A queries the service for unnamed flowlines intersecting a 300 m box around that gap and keeps an unnamed feature only when it is a *bridge*: a stream, artificial-path or connector segment, or a chain of them, whose two free ends touch members of that same `gnis_id` on either side. Each kept feature carries the derived properties `support_for` (the `gnis_id`) and `support_reason` (`bridges_named_parts`). Nothing else unnamed is kept. A supporting feature is used for connectivity only: it is never drawn, never selectable, never labelled and never a display feature. The snapshot document reports the number of named segments, the number of supporting unnamed segments by `support_reason` and `water_class`, and the rivers they support. If reliable grouping turns out to need more than this, M4-A stops and reports; it does not widen the fetch.

**Snapshot record.** M4-A commits `docs/research/m4-water/nhd-snapshot.md` containing: service URL and layer IDs; the service's own `currentVersion` and any data-date text it returns; retrieval timestamp (UTC); the exact `where`, `outFields`, extent and page size of each query; feature counts returned per layer and region; and the SHA-256 of each canonical file before and after.

**Difference report.** The same document reports, per region and layer, comparing the canonical data before and after:

- counts by `ftype` and `fcode`;
- features added and removed, matched by geometry;
- features whose geometry changed;
- features whose name changed;
- every old ID and the new ID it maps to, and every old ID with no match.

A difference that is not explained by "more fields kept" or by the Douglas waterbody scope change stops M4-A: Codex reports it and waits. Nothing is silently overwritten.

## 6. Fields retained

Copied from the source without interpretation and listed under each water layer's `fields.source`:

| Property | From (layer 6 / layers 9, 12) | Type | Notes |
|---|---|---|---|
| `name` | `gnis_name` / `GNIS_NAME` | string or null | Reserved property; unchanged meaning |
| `gnis_id` | `gnis_id` / `GNIS_ID` | string or null | Kept as a string, leading zeros preserved |
| `source_id` | `permanent_identifier` / `PERMANENT_IDENTIFIER` | string | The stable source identifier |
| `ftype` | `ftype` / `FTYPE` | integer | NHD feature type |
| `fcode` | `fcode` / `FCODE` | integer | NHD feature code |
| `reach_code` | `reachcode` / `REACHCODE` | string or null | Not on layer 9 |
| `length_km` | `lengthkm` | number or null | Flowlines only |
| `area_sqkm` | `AREASQKM` | number or null | Polygons only |
| `elevation_m` | `ELEVATION` | number or null | Waterbodies only. Metres, stored unconverted (A3) |
| `visibility_filter` | `visibilityfilter` / `VISIBILITYFILTER` | integer or null | Kept, not used by any M4 rule |
| `waterbody_source_id` | `wbarea_permanent_identifier` | string or null | Flowlines only: the waterbody an artificial path runs through |
| `source_date` | `fdate` / `FDATE` | string or null | The source's feature date, RFC 3339 |

Computed by the pipeline and listed under `fields.derived`:

| Property | Meaning |
|---|---|
| `source_namespace` | Constant `usgs_nhd` |
| `source_layer` | `flowline`, `area` or `waterbody` (replaces Aspen's `kind`, which is kept as an alias for one milestone; see 7.3) |
| `water_class` | `stream`, `artificial_path`, `canal_ditch`, `pipeline`, `connector`, `lake_pond`, `reservoir`, `swamp_marsh`, `other`, from `ftype` by the fixed table in 8.1 |
| `hydro_category` | `perennial`, `intermittent`, `ephemeral` or `unknown`, from `fcode` by the fixed table in 8.1. `unknown` means the source code states no hydrographic category; it is never presented as perennial (O8) |
| `group_id` | Flowlines only: the stream group this segment belongs to, or null (section 8.3) |
| `legacy_ids` | Array of every ID this feature had before M4-A (section 7.3) |
| `support_for`, `support_reason` | Douglas only: set on an unnamed feature kept solely to establish a named river's continuity (section 5). Null or absent on every other feature |

Douglas's always-null `manager` property is removed from the water layers (it was never populated). Nothing else is removed.

No property states access, ownership or permission. The reserved properties of contract section 5.4 are not used on water features.

## 7. Identifiers (D10)

### 7.1 Feature ID

`id` = `nhd-` + the sanitised `source_id`. Sanitising removes every character outside `[A-Za-z0-9-]` (NHD permanent identifiers may be GUIDs written with braces); the unmodified value stays in `source_id`. Example: `source_id` `{5C0F2A10-…}` gives `id` `nhd-5C0F2A10-…`. If two features in a region would get the same ID, or a feature has no `source_id`, M4-A stops and reports; there is no row-number fallback.

`source_namespace` + `source_id` identify the source record. The Ohvernight `id` is the only key other files use.

### 7.2 Group ID

A stream group's ID is `nhd-gnis-<gnis_id>` for the group's main part and `nhd-gnis-<gnis_id>-p<n>` (n from 2) for further parts (section 8.3). A group ID never collides with a feature ID because feature IDs never begin `nhd-gnis-`; a validator rule checks it.

A waterbody is never grouped. Its display ID is its feature ID.

### 7.3 Legacy mapping

Every water feature that existed before M4-A carries its old ID in `legacy_ids`. Old and new features are matched by exact canonical geometry equality within the same layer; a row-number match alone is not accepted. Old features with no match, and new features with none, are listed in the snapshot document.

**A1 — alias scope clarification (coordinator, 2026-10-06).** Canonical `legacy_ids` covers every matched pre-M4 water feature, whether or not it is displayed. `index.json` `water_id_aliases` covers only displayed features: its keys equal the legacy IDs of features in the region's water display artifacts and each value is that feature's current display ID. Legacy IDs for undisplayed canonical features remain on the canonical feature and are omitted from the display index. R68 checks these scopes separately and verifies that every displayed alias agrees with canonical data.

**A2 — alias file and field declarations (coordinator, 2026-10-07, during M4-A).** (1) The alias map is not carried in `index.json`. With it there, Douglas's bytes to "map usable" reached 504,430 against the 500,000 limit. Section 14 already allowed moving it to a separate file; A2 makes that the rule for both regions regardless of index size. The map lives in `regions/<id>/display/water-aliases.json` as `{"region_id": …, "water_id_aliases": {legacy_id: display_id}}`, written by `build_display.py`. `index.json` carries a `water_aliases` entry with the file's path, `sha256` and `bytes`, and no `water_id_aliases` key. The browser does not request the file during load, and it counts toward neither byte budget; the browser check asserts both. Where this document says `index.json` gains `water_id_aliases`, read the alias file. (2) `name` is a reserved property under the data contract and is not listed under `fields.source`; section 6 lists it only to say it is copied from the source. (3) In M4-A the water display artifacts carry only `id`, `name`, the evidence reference, Aspen's `kind` and `source_layer`; the other new properties are canonical only until M4-B rebuilds the water display. (4) An `fcode` that states no hydrographic category is classified `unknown` and is not an error; the build stops only for an `ftype` outside the `water_class` table. The codes observed in the M4-A snapshot are listed in `water_display.json` for the record.

**A3 — elevation unit (coordinator, 2026-10-07, during M4-A review).** This specification first named the waterbody elevation property `elevation_ft` and asked for the source unit to be checked. The check, made in review, shows the NHD `ELEVATION` values are metres: the field's range domain is −400 to 9,000 and the stored values are exact multiples of 0.3048 (Crater Lake 3071.1648). The property is therefore `elevation_m`, with the source value stored unconverted. The evidence is recorded in `docs/research/m4-water/nhd-snapshot.md`. Only 10 waterbodies in each region carry a value, so elevation cannot be used by any M4 rule.

The browser resolves an ID through the display index: `index.json` gains `water_id_aliases`, an object mapping each legacy ID to the current display ID (a group ID for a grouped segment). No saved state stores water IDs today (verified: no storage key, test or config references one), so the alias map exists for external references and for future use, and costs one small object. Aspen's `kind` property is kept alongside `source_layer` through M4 and removed in a later milestone.

## 8. Display selection and grouping (D2, D3, D4, D5, D11)

Canonical data keeps every fetched feature. This section decides only what the browser is given. All rules are computed by `build_display.py` from committed canonical files, offline, with no clock.

### 8.1 Fixed tables

`water_class` from `ftype`: 460 → `stream`; 558 → `artificial_path`; 336 → `canal_ditch`; 428 → `pipeline`; 334 → `connector`; 390 → `lake_pond`; 436 → `reservoir`; 466 → `swamp_marsh`; anything else → `other`.

`hydro_category` from `fcode`: `46006`, `39004`, `39009`, `39010`, `39011`, `39012`, `43615`, `43621` → `perennial`; `46003`, `39001`, `39005`, `39006`, `43614` → `intermittent`; `46007` → `ephemeral`; everything else → `unknown`. These follow the service's coded-value domain, reproduced in [nhd-selection-probe.md](../research/m4-water/nhd-selection-probe.md).

Reservoir eligibility from `fcode`. The domain states a reservoir type for some codes and only a construction material, or nothing, for others. Not eligible, because the source states a type that is not open water for recreation: `43601` aquaculture, `43603` decorative pool, `43604` and `43605` tailings pond, `43606`, `43625`, `43626` disposal, `43607` and `43623` evaporator, `43608` swimming pool, `43609` cooling pond, `43610` filtration pond, `43611` settling pond, `43612` sewage treatment pond, `43624` treatment. Not eligible, because the source states it is intermittent: `43614`. Eligible: `43600` (no type stated), `43613`, `43615`, `43617`, `43621` (water storage), `43618`, `43619` (construction material only). For `43600`, `43613`, `43617`, `43618` and `43619` the source does not state a hydrographic category; they are displayed with `hydro_category` `unknown` and are never described as perennial. Rueter-Hess Reservoir is coded `43619`. The owner approved this treatment (O8): physical existence may be displayed; the category is recorded as `unknown`; every activity and access stays unknown unless a claim says otherwise.

The tables live in one committed configuration file, `v2/pipeline/config/water_display.json`, with the size threshold. The validator and the build read the same file. M4-A adds the file; if the live data contains an `fcode` not in the tables, the build maps it to `unknown` and the snapshot document lists it.

### 8.2 Eligibility

| Feature | Displayed when |
|---|---|
| Stream segment | `water_class` is `stream`, `hydro_category` is `perennial`, and `gnis_id` and `name` are non-empty |
| Artificial path | Never on its own. Drawn as part of a group when it carries the group's `gnis_id` and connects to the group's drawn segments (8.3). NHD represents a wide river as an area polygon with a named artificial path down its centre, so for some rivers most of the drawn line is artificial path |
| Canal or ditch, pipeline, connector | Never |
| Intermittent, ephemeral or not-stated stream | Never in M4 (D2). Kept in canonical data |
| Unnamed stream | Never (D3) |
| Lake or pond, named | `hydro_category` is `perennial`. Any area |
| Lake or pond, unnamed | `hydro_category` is `perennial` and `area_sqkm` ≥ the threshold |
| Reservoir (436) | `fcode` is an eligible reservoir code (8.1); named at any area, unnamed at or above the threshold |
| Intermittent lake, pond or reservoir; lake or pond with no stated category (`39000`) | Never, unless listed in the reviewed inclusion list (8.5) |
| Swamp or marsh, area-layer features, other | Never |
| Any feature in the reviewed exclusion list (8.5) | Never |

Threshold: `unnamed_waterbody_min_area_sqkm` = `0.02` (2 hectares), provisional (D4).

A named waterbody that is intermittent is not displayed. That removes about half of the named Douglas waterbodies; the owner accepted this (O4). One may be brought back only by a reviewed inclusion (8.5) with authoritative evidence and a recorded reason. A name is never an inclusion reason.

### 8.3 Stream grouping

A group is a set of canonical flowline segments shown as one display feature.

**Identity and geometry are separate (O2).** A group is a logical river. Its drawn geometry may be several separate lines, because reaches that are not perennial are not drawn. No geometry is ever invented: no straight connector or any other synthetic line crosses a hidden reach.

**Candidates.** Segments of the region's flowline layer whose `water_class` is `stream` (any hydrographic category) or `artificial_path`, with a non-empty `gnis_id`; and, for connectivity only, supporting features whose `support_for` equals that `gnis_id` (section 5). Canals and pipelines are never candidates. A connector is a candidate only as a supporting feature.

**Algorithm.**

1. Partition candidates by `gnis_id`.
2. Within one `gnis_id`, build a graph: two segments are adjacent when an end point of one equals an end point of the other, after rounding canonical coordinates to six decimals. Interior crossings do not connect.
3. Each connected component is a *part*. Two reaches of one `gnis_id` are therefore one part when source segments of that same river, drawn or not, connect them end to end. They are separate parts when nothing in the source connects them: a gap at the extent edge, disconnected source geometry, or a connection that exists only through a different `gnis_id`.
4. A part is *displayable* when it contains at least one segment eligible under 8.2.
5. Order the displayable parts of a `gnis_id` by total perennial length, longest first, ties broken by the smallest member `id`. The first gets the group ID `nhd-gnis-<gnis_id>`, the rest `-p2`, `-p3`, ….
6. A group's display geometry is the MultiLineString of its eligible stream segments plus the artificial-path segments of the same part that are reachable from an eligible segment through artificial paths alone: an artificial path is drawn when at least one of its end points touches a segment already drawn, computed to a fixed point. An artificial path separated from every eligible segment by a non-perennial stream segment is not drawn. Intermittent, ephemeral and not-stated stream segments of the part are used for connectivity only and are never drawn.
7. Member segments are ordered by `id`. Each member's geometry is transformed exactly as R63 requires and appended as one line of the MultiLineString.

**Invariants (validated; section 13).**

- G1. Every member of a group has the same `gnis_id`, and it equals the one in the group ID.
- G2. Every member of a group has the same `name`. If two segments share a `gnis_id` and differ in `name`, the build fails and reports them; it does not pick one.
- G3. A group's members form one connected component under the adjacency rule. Disconnected sets are never one group.
- G4. No segment belongs to two groups. A segment with an empty `gnis_id` belongs to none.
- G5. Different `gnis_id` values are never merged, whatever their names or geometry. Two streams with the same name and different IDs stay two groups.
- G6. Every drawn member is either an eligible stream segment or an artificial path drawn under step 6. No canal, pipeline, connector or non-perennial stream is drawn. Every group has at least one eligible perennial stream segment.
- G7. The set of members of a group equals the set of canonical segments whose `group_id` is that group ID. Canonical `group_id` is null for every segment that is not a drawn member.
- G8. Grouping never changes, removes or reorders anything in the canonical data except by writing `group_id`.
- G9. Every coordinate in a group's display geometry comes from a drawn member's canonical geometry. No line is added between members.
- G10. A supporting feature is never a drawn member and never has a `group_id`.

**Wide rivers.** The probe found the South Platte River in the Douglas extent with a single perennial stream segment of 80 m; the rest of the river there is artificial path through area polygons. Under step 6 it is drawn only as far as artificial paths connect to that segment. The selection report therefore lists, per region, every named `gnis_id` whose artificial paths total more than 2 km and (a) are not drawn at all because the part has no perennial stream segment, or (b) are drawn for less than 80% of their length. The owner approved the connected-centre-line rule (O9). `water_display.json` also carries `expected_major_rivers`: for each region a list of `gnis_id` values with a minimum drawn fraction of the river's named length inside the extent (initially 0.8). Initial list, to be confirmed against M4-A data: Aspen — Roaring Fork River, Castle Creek, Maroon Creek, Snowmass Creek, Hunter Creek; Douglas — South Platte River, Plum Creek, East Plum Creek, West Plum Creek, Cherry Creek. The build fails when a listed river is absent, is drawn below its fraction, or contains a member with another `gnis_id`. Codex and the coordinator also inspect each listed river on the rendered map in M4-B. If a major river is missing, materially cut short or wrongly grouped, M4-B stops and reports. The rule and the fraction are not weakened to make the check pass; a different rule (for example one using the area polygon's own category) needs owner approval.

**Reporting.** The build writes a grouping report (section 8.6) listing every `gnis_id` with more than one displayable part, with part lengths and the gap between parts, so that real rivers split by an undrawn intermittent reach, by the extent boundary, or by a source error are visible to the reviewer and the owner. M4 never joins separate parts: not across an extent-edge gap, not across disconnected geometry, not through a different `gnis_id`, and not where a branch is ambiguous (O2). Separate parts of one `gnis_id` remain separate groups with the same name.

### 8.4 Display features

The water display artifact changes shape for grouped layers. A stream display feature is:

```json
{"type": "Feature",
 "geometry": {"type": "MultiLineString", "coordinates": [[[-106.82, 39.19], [-106.81, 39.19]]]},
 "properties": {"id": "nhd-gnis-00174812", "name": "Roaring Fork River", "gnis_id": "00174812",
   "water_class": "stream", "hydro_category": "perennial",
   "member_count": 96, "length_km": 48.8, "evidence": 0}}
```

`length_km` on a group is the sum of the drawn members' `length_km` and is a derived fact. Membership is not repeated in the artifact: it is recoverable from canonical `group_id` (G7), and `index.json` carries `water_groups`, mapping each group ID to its ordered member IDs, which the browser does not need to read to draw or select.

A waterbody display feature keeps its canonical properties (`id`, `name`, `gnis_id`, `water_class`, `hydro_category`, `fcode`, `area_sqkm`, `evidence`) and its canonical geometry transformed as today.

Layer structure after M4-B:

| Region | Before | After |
|---|---|---|
| Aspen | `hydrology` (one mixed layer) | Canonical `hydrology` unchanged as one layer for screening. Two display artifacts derived from it: `water_streams` and `water_bodies`. The manifest declares them as two `water` layers pointing at the same canonical pointer with a `display.select` of `streams` or `bodies` |
| Douglas | `waterbodies`, `waterways` | Same two layers; `waterways` display becomes grouped streams |

Both regions therefore present the same two user-facing layers, titled from the manifest, which matters for the shared shell.

### 8.5 Reviewed lists (D5, D3)

`v2/regions/<id>/water-review.json`, curated by hand, validated, optional:

```json
{"exclusions": [
   {"feature_id": "nhd-…", "reason_code": "stormwater_detention",
    "evidence": {"source_url": "https://…", "agency": "…", "statement": "Short factual statement of what the source establishes."},
    "reviewed_at": "2026-10-20T00:00:00Z"}],
 "inclusions": [
   {"feature_id": "nhd-…", "reason_code": "reviewed_intermittent_waterbody",
    "evidence": {"source_url": "https://…", "agency": "…", "statement": "…"},
    "reviewed_at": "2026-10-20T00:00:00Z"}]}
```

Exclusion reason codes: `stormwater_detention`, `water_treatment`, `industrial_or_tailings`, `water_supply_no_public_use`, `not_a_waterbody`, `duplicate_of`. Inclusion reason codes: `reviewed_intermittent_waterbody`.

Rules: `feature_id` is a canonical feature ID or a group ID in that region; `source_url` is HTTP(S) and is not a community source; `statement` is non-empty and is not a quotation longer than 25 words; `reviewed_at` is RFC 3339. A record whose only support is the feature's name is invalid, and the validator rejects an exclusion whose `statement` is empty. An exclusion removes the feature from display only; canonical data is unchanged. `water_supply_no_public_use` is permitted only with a source that states it; a water that is merely restricted is not excluded, it gets claims (section 9).

M4-B ships both lists empty unless the owner supplies entries. An excluded feature is listed in the grouping and selection report.

### 8.6 Selection report and the threshold comparison (D4)

`build_display.py --report` writes, and M4-B commits, `docs/research/m4-water/selection-report.md`:

- per region: counts displayed and not displayed by `water_class` and `hydro_category`; number of groups; pieces per group distribution; the multi-part `gnis_id` list;
- the threshold comparison at 0.5 ha and at 2 ha, per region: number of unnamed waterbodies included; total displayed waterbodies; display artifact bytes; the twenty largest waterbodies excluded at 2 ha and included at 0.5 ha, with area, elevation and coordinates; the twenty smallest included at 2 ha;
- a short reviewer's note on obvious useful water lost at 2 ha and obvious pond or detention clutter kept.

The report is generated; the note is written by Codex and checked by the coordinator. The threshold in `water_display.json` stays `0.02` unless the owner changes it after reading the report. If the report shows clearly useful water excluded at 2 ha, M4-B stops before merge and the examples go to the owner.

## 9. Official recreation claims (D6, D12)

### 9.1 Registry

`v2/regions/<id>/water-recreation.json`, curated by hand, validated. The manifest gains an optional top-level `water_recreation` path, additive to contract version 1.

```json
{"schema_version": 1,
 "records": [
  {"water_id": "nhd-…",
   "operator": "Denver Water",
   "claims": {
     "fishing":  {"status": "restricted", "summary": "Fishing only on the Goose Creek Arm.", "evidence": {"source_url": "https://www.denverwater.org/recreation/cheesman-reservoir", "agency": "Denver Water", "basis": "manual_review", "last_checked_at": "…", "last_confirmed_at": "…", "max_age_hours": 2160, "effective_from": null, "effective_to": null}},
     "boating":  {"status": "prohibited", "summary": "All boating prohibited.", "evidence": {"…": "…"}},
     "paddling": {"status": "prohibited", "summary": "All boating prohibited.", "evidence": {"…": "…"}},
     "swimming": {"status": "prohibited", "summary": "Water-contact sports prohibited.", "evidence": {"…": "…"}}},
   "access": {"status": "unknown"},
   "notes": []}]}
```

### 9.2 Rules

1. `water_id` is a display ID in that region: a waterbody feature ID or a stream group ID. One record per water.
2. Exactly four activities are modelled: `fishing`, `boating`, `paddling`, `swimming`. Each is present in every record. `boating` means motorized or trailered craft; `paddling` means hand-powered craft. Where a source says "all boating", both are set from it, each with its own evidence object citing the same page.
3. `status` is one of `unknown`, `allowed`, `restricted`, `prohibited`.
   - `allowed`: the source states the activity is offered or allowed at this water, with no condition beyond general law.
   - `restricted`: the source states it is allowed only with conditions specific to this water (place, season, reservation, craft type, permit).
   - `prohibited`: the source states it is not allowed.
   - `unknown`: nothing reviewed establishes any of the above.
4. Every status other than `unknown` has its own `evidence` object with an HTTP(S) `source_url` on the operator's or agency's own site, `agency`, `basis` equal to `manual_review`, `last_checked_at`, `last_confirmed_at`, a positive `max_age_hours`, and a non-empty `summary` of at most 160 characters written by the reviewer, not copied text. A claim with status `unknown` has no other key.
5. No activity is inferred from another. The validator cannot check intent, so it checks form: an activity may share a `source_url` with another, but each must carry its own `summary`, and a record in which a single evidence object is referenced by more than one activity is invalid.
6. `access` is a claim about reaching the water lawfully. In M4 it is `unknown` in every record unless the same operator page states an access rule, in which case it is `restricted` with its own evidence (for example "foot access only"). It is never `allowed` in M4.
7. Forbidden sources for a claim: a facility dataset, a designation dataset, a stocking report, a map layer, a community site, another activity's claim. The validator rejects a `source_url` on a host listed in `water_display.json` `non_claim_hosts` (initially the ArcGIS and Socrata hosts and the community sites named in the research), and review rejects the rest.
8. These statuses are a new value set for this registry only. The existing claim object of contract 5.4 (`unknown`, `supported`, `restricted`) is unchanged and still governs rules and reviewed sites.

### 9.3 Freshness

Computed in the browser from `last_confirmed_at` and `max_age_hours`, never stored, exactly as for existing claims.

| Stored status | Within policy | Past policy |
|---|---|---|
| `allowed` | Shown as allowed | Shown as not established, with "last reviewed" date |
| `restricted` | Shown as restricted | Still shown as restricted, flagged "review overdue" |
| `prohibited` | Shown as prohibited | Still shown as prohibited, flagged "review overdue" |
| `unknown` | Not established | Not established |

Staleness never weakens a restriction or prohibition. Default `max_age_hours` for water claims is 2,160 (90 days); the reviewer may set a shorter one for seasonal rules. Validation is time-independent.

### 9.4 Seasonal and conditional rules

A seasonal closure (for example Chatfield's boating closure from 1 December to ice-off) is a `restricted` claim whose `summary` states the season. `effective_from` and `effective_to` are used only for a dated one-off closure. M4 does not evaluate dates to flip a claim to allowed or prohibited "today".

### 9.5 Initial set (M4-C)

Reviewed in this order, restrictions first. Each needs the operator's own page read by the reviewer on the review date.

1. Cheesman Lake — Denver Water.
2. Strontia Springs Reservoir — Denver Water.
3. Rueter-Hess Reservoir — Douglas County / Parker Water.
4. Chatfield Lake — Colorado Parks and Wildlife (state park page).
5. Aspen-region waters with a direct operator or agency page: candidates are Maroon Lake and Snowmass Lake (USFS), Grizzly Reservoir, Wildcat Reservoir, and the Roaring Fork River. A water whose page establishes nothing about an activity gets `unknown` for it; a record of four unknowns is not written.

Ruedi Reservoir is outside the current Aspen extent and is not added. Research for each record is prepared by Hermes as a dossier (page URL, exact sentences relied on, date read); the claim is written and reviewed in the repository by the normal workflow. A Hermes retrieval is not a review (ADR-004, ADR-005): `last_confirmed_at` is set only when the coordinator has read the page and the owner has approved the record in the pull request.

`fact_coverage.recreation_permission` for a region becomes `reviewed_partial` when its registry has at least one record with a non-unknown claim; its statement is rewritten to say that a small number of waters carry reviewed operator statements and everything else is unknown. The contract's requirement for `reviewed_partial` is extended to accept a non-empty `water_recreation` registry.

### 9.6 Community signals (D8)

Not implemented. No file, field or code path for community records is added in M4. The reserved shape, for a later milestone, is a separate registry whose records carry: source name, canonical URL, the source's own ID, matched water ID and match method, observation date, retrieval date, signal kind, a paraphrase, an observation count, the terms URL read, and any deletion deadline; with no verification method and no ability to set a claim.

Future options, recorded and not built: sources whose terms clearly permit reuse (Wikidata for identity; OpenStreetMap for comparison under ODbL); outbound discovery links that store nothing; and first-party Ohvernight observations in a later milestone.

## 10. Trust wording

**Status: approved by the owner on 2026-10-06 (O5), with edits: WW8 reworded, WW16 added, `motorized` spelling, and the limitation sentence replaced.** The strings are exact. Implementation uses them byte for byte and does not rewrite, shorten or vary them by region.

Fixed strings, compared against literals in tests. None contains "verified", "legal", "permitted" or "open to" (M3 A4 rule). A status word is never shown without its activity. All of them appear only in the water feature detail in the results sheet, except WW14 and WW15, which are also the feature's title in search results.

### 10.1 The sixteen fixed strings

| ID | String | Where it appears | Evidence or state that causes it |
|---|---|---|---|
| WW1 | `Mapped water. Access and allowed activities are not established.` | Water detail, in place of the operator-statement section | The water has no record in the recreation registry |
| WW2 | `A mapped water feature is not permission to enter, fish, boat, paddle, swim, park or camp.` | Water detail, always the last line | Every water feature, whatever its claims |
| WW3 | `Not established` | Water detail, operator-statement section, after an activity label or `Access` | That activity's claim is `unknown`; or its stored status is `allowed` and the review is past its maximum age |
| WW4 | `Allowed` | Same place, after an activity label | The claim is `allowed`, with complete qualifying authoritative evidence, and that evidence is within its approved freshness window. In no other case |
| WW5 | `Restricted` | Same place, after an activity label or `Access` | The claim is `restricted`, with complete evidence; shown whether or not the review is overdue |
| WW6 | `Prohibited` | Same place, after an activity label | The claim is `prohibited`, with complete evidence; shown whether or not the review is overdue. The word is not softened |
| WW7 | `Review overdue` | Same line as WW5 or WW6 | The claim is `restricted` or `prohibited` and its last confirmation is older than its maximum age. The restriction itself is not weakened |
| WW8 | `Agency or operator statement` | Water detail, heading of the section that lists the activities, followed by the operator's name | The water has a record in the recreation registry |
| WW9 | `From the source` | Water detail, heading of the first section | Every water feature |
| WW10 | `Computed by Ohvernight` | Water detail, heading of the section holding length or area | Every water feature that has a length or an area |
| WW11 | `Reviewed` | Water detail, after each non-unknown activity line, followed by the date of last confirmation | The claim is `allowed`, `restricted` or `prohibited`. It means a person reviewed the evidence and the claim on that date |
| WW12 | `Perennial` | Water detail, "From the source" section | The source code states the feature is perennial. The source's own term is kept; it is not replaced by a plainer word that could imply more than the classification establishes |
| WW13 | `source segments` | Water detail, "From the source" section, after a number, as in `96 source segments` | The feature is a grouped stream |
| WW14 | `Unnamed lake` | Detail title and search-result title | A lake or pond with no source name |
| WW15 | `Unnamed reservoir` | Detail title and search-result title | A reservoir with no source name |
| WW16 | `Hydrographic category not stated by the source` | Water detail, "From the source" section, in the place WW12 would take | The displayed feature is eligible under section 8 and its `hydro_category` is `unknown` (for example Rueter-Hess Reservoir). Perennial or intermittent status is never inferred |

### 10.2 Labels used with them

These are also user-facing and fixed.

| String | Where it appears | Evidence or state that causes it |
|---|---|---|
| `Fishing` | Operator-statement section, start of an activity line | The water has a record |
| `Boating (motorized or trailered)` | Same | The water has a record |
| `Paddling` | Same | The water has a record |
| `Swimming` | Same | The water has a record |
| `Access` | Same, last line of the section | The water has a record |
| `River or stream` | "From the source" section, type line | Source type is stream or river |
| `Lake or pond` | Same | Source type is lake or pond |
| `Reservoir` | Same | Source type is reservoir |

An activity line reads: label, status word, the reviewer's summary, a link to the operator's page, then `Reviewed` and the date, then `Review overdue` when it applies. Example, for a claim that is prohibited and within its review age: `Boating (motorized or trailered): Prohibited. All boating prohibited. Denver Water. Reviewed 2026-10-20.` The summary is written per claim by the reviewer and approved by the owner in M4-C; it is not one of the fixed strings.

Reused unchanged from M3: the agency name, the source link label, the "Source fetched" line and the rendering of the layer limitation sentence.

### 10.3 Water-layer limitation sentence

The manifest `limitations` sentence for each water layer is rewritten in M4-B and rendered verbatim, as today, in the layer drawer row and in the "From the source" section of every water detail. Approved text, identical in both regions:

`Rivers, streams, lakes and reservoirs selected from source type codes. Displayed streams and lakes are coded perennial; some reservoirs have no hydrographic category stated by the source. Unnamed streams and intermittent water are not shown. A mapped water feature is not evidence of access or of any allowed activity.`

## 11. Interaction

M4 adds no interaction model. It uses M3's (A14).

| Tap target | Behaviour |
|---|---|
| Grouped stream, on any member line or on its label | Selects the whole group: every line of the MultiLineString gets the selected stroke and casing; other streams dim; the map may fit the group; detail opens at the partial height |
| Waterbody | Selects with the stronger fill; camera preserved; detail opens at the partial height |
| Empty map | Unchanged from A14 |

Because a group is one display feature, the adapter's twelve exports, `setSelected`, labels and hit testing need no new concept. A stream gets one label, placed by the adapter's existing rule. The registry entry for the waterbody layer relies on the polygon default (`preserve`); the stream layer on the line default (`fit`).

**Fit policy (O6).** Fitting a long river can zoom far out. The shell's camera policy (M3 A14) gains an optional per-layer fit policy, read from the layer registry entry; the adapter is not changed and has no water-specific logic.

| Policy field | Meaning | Water streams | Every other layer |
|---|---|---|---|
| `tap.max_zoom_out` | On a map-tap selection, the most zoom levels the fit may zoom out from the current zoom | 2 | not set: M3 behaviour unchanged |
| `list.min_zoom` | On a selection from search or a results list, the lowest zoom a fit may reach | 11 | not set: M3 behaviour unchanged |

Map tap: the river is selected and highlighted and its detail opens. If fitting it would zoom out more than `tap.max_zoom_out` levels, the map does not fit; it keeps its zoom and keeps the tapped point in view above the sheet. Search or list selection: the map may move to the river and fit it, but not below `list.min_zoom`; if the whole river does not fit at that zoom the map centres on the member nearest the river's midpoint. Both values live in the registry's defaults for line features of kind `water`, are configurable, and are confirmed on a device in M4-B. Trails and other lines carry no fit policy, so their M3 behaviour is unchanged. Tests cover a short feature (fits exactly as in M3) and a very long river (capped) for both origins.

**Detail content**, in this order, only where the value is carried:

1. Title: the name, or WW14 / WW15 for an unnamed waterbody.
2. `From the source`: type label; WW12 when `hydro_category` is `perennial`, WW16 when it is `unknown`; for a stream, `<n> source segments`; agency; source link; "Source fetched" date; the layer limitation sentence.
3. `Computed by Ohvernight`: length in kilometres for a stream or area in hectares for a waterbody, to one decimal.
4. If the water has a recreation record: WW8 with the operator's name, then one line per activity — label, status word, summary, link, `Reviewed <date>`, and `Review overdue` when it applies. Activities with status unknown show `Not established`. Prohibited and restricted lines come before allowed ones.
5. If it has no record: WW1.
6. Always last: WW2.

No icon, colour, filter or sort implies an activity. Streams and waterbodies keep the single M3 water colour. M4 adds no restriction colour, warning icon or other status symbol to the map (O3). The map communicates physical water identity and type; restriction and activity status are in the feature detail.

Search: water names are added to the existing search list for both regions, as source names. Selecting one selects the group or waterbody.

## 12. Contract changes

All additive to contract version 1 and documented in `v2/pipeline/docs/data-contract.md` in the pull request that introduces them.

| Change | PR |
|---|---|
| New source and derived fields on water layers; removal of Douglas `manager` on water | A |
| `v2/pipeline/config/water_display.json` | A |
| `display/water-aliases.json` and the `index.json` `water_aliases` entry (A2) | A (aliases to feature IDs), B (aliases to group IDs) |
| Layer `display.select` (`streams`, `bodies`) and grouped display features; R61–R63 amended for grouped layers | B |
| `index.json` `water_groups` | B |
| `water-review.json` and manifest `water_review` path | B |
| `water-recreation.json`, manifest `water_recreation` path, the four-status activity claim, `reviewed_partial` extension | C |

## 13. Validator rules

New stable rule IDs. Each has at least one negative test on a fixture and, where it protects real data, a mutation proof on the committed files (run locally, not committed).

| ID | Rule | PR |
|---|---|---|
| R66 | Every water feature has non-empty `source_id`, `source_namespace` equal to `usgs_nhd`, integer `ftype` and `fcode`, and `id` equal to `nhd-` plus the sanitised `source_id`. IDs are unique within a region | A |
| R67 | `water_class` and `hydro_category` equal the values computed from `ftype` and `fcode` by `water_display.json` | A |
| R68 | `legacy_ids` is an array of distinct non-empty strings; no legacy ID appears on two features; `water_id_aliases` keys equal the legacy IDs of displayed water features, map to their existing display IDs, agree with canonical data and contain nothing else (A1) | A, B |
| R69 | The display set of a water layer equals exactly the set computed from canonical data by section 8.2, the threshold, and the reviewed lists. No eligible feature is missing and no ineligible feature is present | B |
| R70 | Grouping invariants G1–G7, G9, G10 hold for every group; `water_groups` equals the canonical `group_id` membership | B |
| R71 | A group display feature's geometry equals the ordered, R63-transformed geometry of its drawn members; `member_count` and `length_km` equal the computed values; `name` and `gnis_id` equal the members' | B |
| R72 | No display feature of a water layer has a `water_class` of `canal_ditch`, `pipeline`, `connector`, `swamp_marsh` or `other`. A displayed stream group or lake has `hydro_category` `perennial`; a displayed reservoir has an eligible reservoir code; the only exceptions are listed inclusions | B |
| R73 | `water-review.json` conforms to 8.5: IDs resolve, reason codes are in the set, evidence is complete, no community host, and no excluded feature is displayed | B |
| R74 | `water-recreation.json` conforms to 9.2: IDs resolve to display IDs; exactly the four activities; status in the set; complete evidence for every non-unknown status; no shared evidence object; no `non_claim_hosts` URL; `access` never `allowed` | C |
| R75 | A water feature or display feature carries no property named for an activity or for access, and none of the reserved properties of contract 5.4; claims live only in the registry | A, C |
| R76 | `fact_coverage.recreation_permission` is `reviewed_partial` only when the registry has a non-unknown claim, and its `layer_ids` name the water layers | C |

R61, R62 and R63 are amended, not weakened: for an ungrouped layer they are unchanged; for a grouped layer R61's "every feature ID exists in the canonical layer" becomes "every display ID is a group ID in `water_groups` or a canonical feature ID", and R62 and R63 apply to each member through R71. R64 and R65 are unchanged.

## 14. Budgets and performance

Byte budgets (enforced in the browser check, as in M3):

| Measure | Limit |
|---|---|
| Bytes to "map usable" | 500,000 (unchanged) |
| Bytes with every default-on layer | 4,500,000 (unchanged) |
| Aspen water display artifacts, total | ≤ 1,134,855 (today's `hydrology.geojson`) |
| Douglas water display artifacts, total | ≤ 1,887,725 (today's `waterbodies.geojson` + `waterways.geojson`) |
| Alias map | In `water-aliases.json`, outside `index.json`, never requested during load (A2) |
| `index.json` growth from `water_groups` (M4-B) | reported; if it would push either region over the map-usable budget, the group map moves to a separate file that the browser does not load by default |

Performance: the A10 limits and triggers R-1 to R-5 apply unchanged. M4-B is expected to reduce feature count and bytes; three sessions of the unchanged `measure.mjs` are run at the M4-B head and reported, pass or miss. A miss is reported, not tuned around.

## 15. Tests

Offline, clock-free, nothing written inside the repository, as in M3.

**Python (validator and build):** a negative fixture for every rule R66–R76; the fixed tables; ID sanitising and collision; legacy mapping by geometry (a moved row number does not match; an identical geometry does); eligibility for each row of 8.2 at, just below and just above the threshold; grouping: same `gnis_id` in two disconnected sets gives two groups; two `gnis_id` values touching end to end stay two groups; a segment with empty `gnis_id` joins nothing; same `gnis_id` with two names fails the build; an intermittent reach connects two perennial reaches into one group whose geometry is two separate lines, with no coordinate added between them (G9); two reaches of one `gnis_id` with nothing in the source between them stay two groups; a reach connected only through a different `gnis_id` is not joined; a supporting unnamed feature bridges two named parts and is never drawn or given a group; an unnamed feature that does not bridge is not kept; an expected major river that is missing, below its drawn fraction or carrying a foreign member fails the build; an artificial path is drawn when it connects to a drawn segment through artificial paths alone and not when a non-perennial segment lies between; a group cannot consist of artificial paths only; each reservoir code of 8.1 is eligible or not as listed; a canal with the same `gnis_id` is neither drawn nor used for connectivity; exclusion and inclusion lists; claims: each invalid form of 9.2; freshness table of 9.3 as a pure function with an injected time.

**Node:** detail rendering for a grouped stream, a named lake, an unnamed lake, a water with claims in each status and with an overdue restriction; every WW string against a literal; no activity status rendered without evidence; WW16 and not WW12 rendered when the category is `unknown`; fit policy for a short feature and a very long river, from a map tap and from a list.

**Browser check (both regions, four sizes):** the water layers load within budget; a real stream group selects as one feature from a tap on two different member lines and from its label, with one casing set and one label; a real waterbody selects with the camera preserved; detail shows the M4 sections and WW2; no canal or ditch name appears in the rendered water layer (asserted from `water_class`, not from names); from M4-C, Cheesman's detail shows `Prohibited` for boating with its link, and a water with no record shows WW1.

**Mutation proofs (local, listed in the handoff):** change one `fcode` in canonical data; move a segment to another group in `water_groups`; add a canal to a display artifact; drop a member from a group's geometry; set an activity to `allowed` with no evidence; point a claim at an ArcGIS host; lower the threshold in the artifact but not in config. Each must fail the named rule.

## 16. Delivery

Four sequential pull requests. Each is independently revertible and leaves `main` green.

### M4-A — Source preservation and canonical enrichment

In: the fetch scripts keep the fields of section 6; the one controlled NHD refresh; stable IDs; `legacy_ids`; `water_display.json`; R66, R67, R68, R75; the snapshot and difference document; contract documentation; display artifacts rebuilt with the **current** selection rule so the map shows the same features under new IDs with new properties carried.

Must not change: which water features are displayed, their geometry, any non-water layer, any interaction, any wording. The browser check's existing assertions pass unchanged except for water feature IDs. Bytes may rise from the new properties; M4-A reports the rise, and if either region exceeds the default-on budget the extra display properties are deferred to M4-B.

### M4-B — Functional recreational-water display

In: section 8 in full; grouped display features; the Aspen display split into streams and bodies; `water-review.json` (empty unless supplied); R69–R73 and the R61–R63 amendments; the selection report with the 0.5 ha and 2 ha comparison; detail sections 1 to 3, 5 and 6 of section 11; WW strings; the fit cap; water in search; budgets; three performance sessions; manifest limitation text.

Gate before merge: the owner reads the selection report and confirms or changes the threshold, and does an iPhone check of both regions.

### M4-C — Reviewed official recreation claims

In: `water-recreation.json` for both regions with the initial set of 9.5; R74, R76; detail section 4; freshness; `fact_coverage` change; Hermes dossiers stored under `docs/research/m4-water/claims/`.

Gate before merge: the owner approves each record's wording and source in the pull request.

### M4-D — CPW structured enrichment (optional)

Not specified here beyond its boundary. It may start only after written confirmation of reuse terms from CPW covering fetch, transformation, storage in a public repository and redistribution, and after a schema probe. Until then no CPW structured record is committed, cached in the repository or published. A CPW page may still be cited as the source of a manually reviewed claim. M4-D needs its own specification amendment and owner approval. See [track F](../research/m4-water/hermes/track-f-cpw-structured-data.md).

## 17. Rollback

- M4-A: revert the pull request. The previous canonical files, IDs and display artifacts return together because they are committed together. The pre-refresh SHA-256 values in the snapshot document identify the state to return to.
- M4-B: revert the pull request. The display returns to the M4-A artifacts (old rule, new IDs). The canonical data from M4-A is untouched by M4-B except for `group_id`, which the revert removes.
- M4-C: revert, or empty the registry. With no registry every water shows WW1.
- A single wrong claim: set it to `unknown` in a one-line change; that is always safe.
- A wrong exclusion or threshold: one-line data change and a rebuild.

## 18. Technical debt: NHD is transitional (D1)

NHD is frozen. Errors in it will not be corrected at source, and USGS is replacing it with 3DHP. M4 records this debt and a roadmap item is added for a later milestone:

**3DHP validation and migration.** Using real Aspen and Douglas records, establish before any switch:

1. whether 3DHP preserves the distinctions M4 relies on — perennial against intermittent, lake against reservoir, reservoir purpose, canal and pipeline against stream — or how they can be carried over;
2. whether `id3dhp` and `mainstemid` are stable, and how they map to NHD `permanent_identifier` and `gnis_id` for every displayed feature;
3. coverage and geometry differences in both regions, feature by feature for displayed water;
4. that every M4 group, claim, exclusion and alias survives the mapping with no orphan.

Until those are shown, M4 data stays on the NHD snapshot. M4-A stores no 3DHP identifier; fetching one is part of the validation work, not M4.

## 19. Risks

| Risk | Mitigation |
|---|---|
| The live refresh returns data that differs from September's in ways not explained by the change | Difference report; stop and report rule in section 5 |
| `permanent_identifier` missing or duplicated | R66; stop and report; no fallback |
| Grouping joins or splits wrongly | Invariants G1–G10, negative tests, the multi-part report, owner check on device |
| A wide river is mostly artificial path in NHD and is drawn short or not at all | Step 6 draws connected artificial paths; the selection report lists every affected river; stop-and-report rule in 8.3 |
| The perennial rule hides a stream people use that NHD codes intermittent | Selection report lists every named intermittent-only stream; the owner can ask for a reviewed inclusion mechanism for streams (not in M4) |
| The 2 ha rule hides useful lakes, or keeps ponds | Threshold comparison with examples; owner confirms |
| Structures coded as lakes remain | Reviewed exclusion list; honest "not established" wording |
| A claim goes stale or the operator changes a rule | Freshness; restrictions never weaken; one-line downgrade to unknown |
| A claim is wrong at entry | Restrictions first; operator's own page only; owner approves each record |
| Fit on a long river zooms out too far | Fit cap with tests |
| Byte or time budget missed | Budgets enforced; group geometry reduces feature count; report, do not tune |
| Hermes output treated as verified | Dossiers are inputs; `last_confirmed_at` only after coordinator read and owner approval |

## 20. Unknowns

Stated as unknown; none blocks approval of this specification.

- The exact counts the rule yields in each region. A read-only attribute probe gives the estimates in section 23; the real numbers come from M4-A data and the M4-B report.
- Whether every displayed feature has a `permanent_identifier` and whether any `gnis_id` carries two names.
- How many rivers split into more than one part.
- The unit of NHD `ELEVATION`.
- Recreation status of Grizzly Reservoir, Wildcat Reservoir, and water use at Maroon Lake and Snowmass Lake.
- CPW reuse terms (M4-D only).
- Whether 3DHP can replace NHD without loss (section 18).

## 21. Owner decisions recorded (2026-10-06)

| ID | Decision |
|---|---|
| D1 | NHD is canonical for M4, explicitly transitional; no switch to 3DHP until real records prove the distinctions and identifiers survive; roadmap item added |
| D2 | Intermittent streams preserved in canonical data, not displayed in the primary layer, no separate layer in M4 |
| D3 | Named perennial waterbodies eligible at any area; unnamed perennial only above the threshold; unnamed streams not displayed; intermittent waterbodies not displayed unless individually reviewed |
| D4 | 2 hectares provisional; 0.5 ha against 2 ha comparison produced in M4-A/B; threshold not changed silently |
| D5 | No name-keyword removal; reviewed exclusion list with stable ID, reason code, authoritative evidence, source and review date |
| D6 | Small reviewed initial set, restrictions first; fishing, boating, paddling, swimming modelled independently as allowed, prohibited, restricted or unknown; no inference; restrictions take precedence and staleness never weakens them |
| D7 | M4 not blocked on CPW; focused Hermes follow-up done; M4-D optional; no uncertain CPW data persisted |
| D8 | No third-party community data in the production pipeline; four-class model kept; zero community records acceptable |
| D9 | One controlled live NHD refresh in M4-A with a reproducible record and difference report; no visible change in M4-A |
| D10 | One-time ID migration to stable source-backed identifiers, with namespace, legacy aliases, group IDs and member traceability |
| D11 | Grouping with validated invariants and negative tests; no blind "same GNIS ID is one feature" |
| D12 | Physical water may be displayed with every recreation and access property unknown |

## 22. Owner decisions on O1–O9 (2026-10-06)

| ID | Decision |
|---|---|
| O1 | Do not fetch all unnamed Douglas stream segments. Fetch named stream features, features needed for wide-river centre lines, and the minimum unnamed supporting features that continuity genuinely needs, each traceable and explainable, never shown as separate features; report the counts and reasons; stop and report if this makes reliable grouping impossible |
| O2 | Identity and rendered geometry are separate. A river may be one group across an intervening intermittent reach when GNIS identity agrees, source topology establishes continuity, no unrelated branch is absorbed and no geometry is invented. No synthetic connector. No joining across extent-edge gaps, disconnected geometry, different GNIS IDs or ambiguous branches. Member source IDs preserved. Positive and negative tests |
| O3 | No restriction colours, warning icons or other map-level status symbols in M4. Status belongs in the detail |
| O4 | Named intermittent waterbodies hidden by default; included only through a reviewed inclusion with authoritative evidence and a recorded reason; a name is not a reason |
| O5 | Approved with edits: WW1–WW7 and WW9–WW15 as proposed; WW8 changed to "Agency or operator statement" (not "Official statement"); WW16 added for an unstated hydrographic category; "motorized" spelling; "Reviewed" and "Perennial" kept; the limitation sentence replaced with the owner's exact wording, identical in both regions |
| O6 | Fit cap approved: a map-tap selection never zooms out more than about two levels to fit a river; search and list selection may fit more broadly down to a configurable minimum zoom; ordinary short lines unchanged; the policy is per layer and geometry, not hard-coded in the adapter; tests for a short feature and a very long river |
| O7 | Pursue clarification from CPW. A draft outreach message is in [cpw-outreach-draft.md](../research/m4-water/cpw-outreach-draft.md). M4-A, B and C do not wait. M4-D stays optional and needs separate written approval and a specification amendment once terms are clear |
| O8 | Display otherwise-eligible reservoirs whose attributes establish neither perennial nor intermittent and no exclusion condition; never label them perennial; record the category as unknown; activities and access stay unknown |
| O9 | Connected-centre-line rule approved: no invented geometry, source identity and member IDs preserved, no unrelated area or centre line absorbed, a missing or truncated major river detected by build and test; major rivers explicitly inspected in M4-B; stop and report, never weaken the rule |

The four-pull-request structure is approved. M4 completes after A, B and C. M4-D is optional.

## 23. Measured and estimated counts

From the coordinator's read-only probes of the NHD service on 2026-10-06 (attributes and statistics only; features intersecting each region's bounding box, so slightly more than the clipped repository data). Raw output is in [existing-data-audit-facts.md](../research/m4-water/existing-data-audit-facts.md) and [nhd-selection-probe.md](../research/m4-water/nhd-selection-probe.md).

### Streams

| | Aspen | Douglas County |
|---|---:|---:|
| Line pieces shown today | 1,512 | 2,359 |
| Named perennial stream segments | 1,087 | 2,026 |
| Stream groups by `gnis_id` (before splitting into parts) | 62 | 56 |
| Distinct names among them | 58 | 54 |
| Names used by two different `gnis_id` values | 4 (Hunter, Pine, Copper, Sawyer Creek) | 2 (Bear, Pine Creek) |
| Groups under 2 km / 2 to 10 km / over 10 km | 7 / 41 / 14 | 6 / 30 / 20 |
| Named streams that are intermittent only, so not displayed | 9 | 27 |
| Named artificial-path segments | 124 | 670 |
| … whose `gnis_id` has a perennial stream segment | 113 | 502 |
| Segments with a `permanent_identifier` | all 1,290 fetched, all distinct | all 3,503 fetched, all distinct |

Longest groups: Roaring Fork River (82 segments, 39 km), Castle Creek, Snowmass Creek, Hunter Creek; East Plum Creek (181 segments, 54 km), Cherry Creek, West Plum Creek. The South Platte River has one perennial stream segment (80 m) in the Douglas extent; see 8.3.

Named streams not displayed because NHD codes them intermittent include, in Douglas, Big Dry Creek, Coal Creek, Cottonwood Creek, Happy Canyon Creek and 23 others; in Aspen, nine small creeks. Connectivity was not tested, so the number of parts per group is unknown.

### Waterbodies

| | Aspen | Douglas County |
|---|---:|---:|
| Lakes, ponds and reservoirs in the source | 414 | 2,275 |
| Named | 39 | 36 |
| Shown today | 43 | 33 |
| Named and eligible (perennial lake, or eligible reservoir code) | 39 | 18 |
| Named and not eligible (intermittent) | 0 | 18 |
| Unnamed perennial | 336 | 764 |
| Unnamed perennial at or above 2 ha | 3 | 19 |
| Unnamed perennial at or above 0.5 ha | 44 | 123 |
| **Displayed at 2 ha** | **42** | **37** |
| Displayed at 0.5 ha | 83 | 141 |

In Douglas the 18 named waterbodies hidden as intermittent are almost all "Franktown Parker FP…" and "West Cherry Creek Detention Number …" structures, plus Mann, Cantrill, Fairview, Stevens and Nelson reservoirs. Three perennial-coded structures remain displayed (Franktown Parker FPA-5 and FPS-1, West Cherry Creek Detention Number 7) and are candidates for a reviewed exclusion. The named eligible set includes Chatfield Lake, Cheesman Lake, McLellan Reservoir, Strontia Springs Reservoir, Aurora-Rampart Reservoir, Platte Canyon Reservoir and Rueter-Hess Reservoir.

In Aspen every named lake is perennial and stays. The 2 ha threshold adds 3 unnamed lakes; 0.5 ha would add 44, with 41 between 0.5 and 2 ha (the largest 1.7 ha). Whether those 41 are alpine lakes worth showing is exactly what the threshold comparison in 8.6 must show with examples. Two named Aspen waterbodies are under 0.5 ha (Silver Dollar Pond, Elk Creek Reservoir Number 2) and stay because they are named.

### Net effect, estimated

| | Today | After M4-B |
|---|---:|---:|
| Aspen tappable water features | 1,555 | about 104 (62 streams, 42 waterbodies) |
| Douglas tappable water features | 2,392 | about 93 (56 streams, 37 waterbodies) |

## 24. Acceptance criteria

M4-A:
1. Both suites and the browser check pass; display rebuild has no diff.
2. Snapshot and difference document committed; every unexplained difference resolved or reported.
3. Every non-water layer's canonical content is byte-identical to `b45ca59`.
4. The set of displayed water features is unchanged apart from IDs and added properties (asserted by geometry).
5. R66, R67, R68, R75 pass on real data with negative tests and mutation proofs.

M4-B:
6. R69–R73 and the amended R61–R63 pass with negative tests and mutation proofs.
7. No canal, ditch, pipeline, connector, intermittent or unnamed stream is in a display artifact.
8. Every displayed stream is a group satisfying G1–G10; every group is traceable to its members.
9. Selection report committed with the threshold comparison; owner has confirmed the threshold.
10. Byte budgets hold; three performance sessions reported.
11. Detail shows only carried fields; every WW string matches its literal; no activity wording without a claim.
12. Owner's iPhone check of both regions passes.

M4-C:
13. R74 and R76 pass with negative tests and mutation proofs.
14. Every non-unknown claim cites the operator's own page, read by the coordinator, and is approved by the owner in the pull request.
15. An overdue restriction is still shown as a restriction.
16. A water with no record shows WW1 and WW2 and nothing about activities.

All: no M5–M8 functionality; no community data; no CPW structured data; no merge without owner approval of the specific pull request and head SHA.
