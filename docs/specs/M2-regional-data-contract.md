# Milestone 2 specification — Unified regional data contract and evidence semantics

**For:** Codex (implementation). **Reviewer:** Claude. **Base:** `main` at `c604baf`.
**Branch:** `k-kopacek/m2-regional-data-contract`. Open a PR; do not push to `main`.
**Status:** APPROVED by the owner on 2026-10-04. **Revision 4** (amendment A1 below resolves an implementation blocker). Ready for implementation.

## Amendments

**A1 (revision 4) — `verification_method` may be null; resolution of the `community_report` blocker.**

- *Blocker.* Codex stopped, as section 5.4 required, because `v2/pipeline/scripts/08_ingest_leads.py` emits `verification_method: "community_report"`, which is not in the approved vocabulary.
- *Owner decision.* A community report describes where an input came from. It is provenance, not verification. An unreviewed community lead has had no verification method applied. `community_report` is **not** added to the vocabulary.
- *Resolution.* `verification_method` may be `null`, meaning no verification method has been applied. The six approved strings are unchanged. `08_ingest_leads.py` emits `null`. No new provenance field is added: the report's origin is already preserved by `evidence.source_url`, `evidence.agency`, `evidence.reported_at` and `site_type: "dispersed_lead_unverified"`.
- *Necessary consequence.* `schema.json` currently requires `verification_method` to be a non-empty string, so `validate_bundle` would reject any bundle containing a lead once the script emits `null`. One property of `schema.json` is therefore changed to accept `null`. Nothing else in that file changes.
- *Sections changed by A1:* 4, 5.4, 5.6 (note on `leads`), 5.7 (R23, R28), 6, 8 (T4, new T16), 9 (criteria 3, 4, 11, new 18–19), 10, 11. No other scope is revisited.

## 1. Problem

Ohvernight publishes two regions, and each one invented its own data shape.

Facts verified against the repository on 2026-10-04 (43 Python tests and 14 Node tests pass at the base commit):

| # | Verified fact | Where |
|---|---|---|
| F1 | Aspen data is spread over six files with three different envelopes: a schema-v2 bundle keyed by pipeline step, a bare FeatureCollection, and three place lists. | `v2/map-data-v2.json`, `v2/trails.geojson`, `v2/overnight-options.json`, `v2/ridb-options.json`, `v2/destinations.json`, `v2/pipeline/config/rules-registry.json` |
| F2 | Douglas data is one file with a fourth envelope (`schema_version: 1`, layers keyed by layer name). | `v2/regions/douglas-co/research.json` |
| F3 | Only the Aspen bundle has a JSON Schema. Its title is "Aspen research bundle v2" and it hard-codes Aspen layer names. | `v2/pipeline/schema/schema.json` |
| F4 | Transport status has four shapes: `{status, completed_at, reason}` (bundle), `{status, retrieved_at, count}` with a `failed` state written by the script (Douglas), `{status, last_checked_at, last_confirmed_at, max_age_hours, scope}` (RIDB inventory), and none at all (Aspen trails; Douglas trails, roads and boundary). | bundle, `research.json`, `ridb-options.json`, `enrich_douglas.py` |
| F5 | `data-contract.md` says every fact needs a status, source URL, scope, `last_checked_at`, `last_confirmed_at` and a freshness threshold. The per-feature `evidence` object has none of `scope`, `last_checked_at`, `last_confirmed_at` or a threshold. | `v2/pipeline/docs/data-contract.md`, `schema.json` `$defs.evidence` |
| F6 | `evidence.confidence` means different things for the same source. BLM limited-scale land polygons are `high` in Aspen and `unverified` in Douglas. `high` describes the fetch, but it sits on a land-management feature and can be read as confidence in ownership. | 7,161 features `high`, 2,434 `unverified`, same BLM URL in both regions |
| F7 | `evidence.last_verified` is `null` on all 9,647 published features. | both regions |
| F8 | Freshness is implemented four times with different thresholds and edge behaviour: `Trust.freshness` (data-driven), `lib/rules.py` (future-dated record → `stale`, where JS returns `unavailable`), `trip-rules.js` (hard-coded 30 days on `checked_on`), `preview.js` (hard-coded 7 days on `retrieved_at`). | named files |
| F9 | Nothing declares, per region, which high-trust questions the data cannot answer. Aspen has three free-text `coverage_gaps`; Douglas has `missing_layers` and `notes`. | bundle, `research.json` |
| F10 | Aspen hydrology is clipped to the study area plus a 0.005° margin; 730 of 6,926 features extend past the study boundary. Every other layer in both regions lies inside its boundary. | `03_fetch_hydrology.py`, measured |
| F11 | Feature IDs are unique across all Aspen FeatureCollection layers, including trails. | measured |

The consequence: a third region cannot be added without inventing a fifth shape, the main app cannot offer region selection (Douglas README gate 4), and the written evidence contract is not enforced on anything.

**Architecture-audit context.** The original audit was written outside the repository and was not preserved. The owner restated its findings on 2026-10-04. Each one is listed here with where this specification represents it.

| # | Audit finding | Represented in M2 by |
|---|---|---|
| A1 | Non-federal land must never be inferred to mean Private. | 5.4 rule 11; R28 (`land_management`); ownership statements in 5.6 |
| A2 | Ownership/classification and public access are separate evidence dimensions. | 5.4 rule 12; separate `ownership` and `public_access` dimensions in 5.5 |
| A3 | Land styling must not imply certainty the data does not support. | `spatial_precision` (5.2); 5.4 rule 13; N17. The styling change itself is UI work and stays in Milestone 3. |
| A4 | Staleness must never weaken or suppress a known restriction. | 5.4 rule 6; **fixed at runtime in 5.9** |
| A5 | Stale-rule ordering can hide tent-only, clearance, seasonal or stay-limit restrictions. | **Fixed in 5.9**; tests T10–T13 |
| A6 | Retrieval or checking is not confirmation; a fetch advances a checked/observed timestamp only. | 5.3; 5.4 rule 2; R30; N3 pinned by T5 |
| A7 | Existence, permission/access, provenance, verification and freshness are distinct concepts. | 5.4 concept table |
| A8 | Missing evidence fails closed for positive claims. | 5.4 rules 1 and 14; R27, R28, R41 |
| A9 | Water lacks semantics for recreational usefulness; relied on names; dropped source attributes. | `recreation_permission` dimension (5.5); water `limitations` and source scope (5.6); N18. Reprocessing water is not in M2. |
| A10 | Some trail/road/source paths lack fetch-status and provenance visibility. | R31; N1 and N12, pinned by T5 |
| A11 | Aspen payload is large with repeated provenance; keep the ability to fix it later without mixing it with evidence semantics. | 5.1 forward-compatibility note; N14. No payload change in M2. |
| A12 | A mapped feature or nearby public land does not establish access, camping, road, trail or recreational permission. | 5.4 rule 15; statements in 5.6 |

## 2. Desired behavior

After this milestone:

1. Each region has one small, hand-reviewed **manifest** that declares its coverage, sources, layers, transport-status locations, freshness policy and an explicit statement of what is unknown for each high-trust fact dimension.
2. One Python validator checks every region's manifest **and the published data it points at** against one contract, in CI, on every pull request.
3. The evidence semantics are written once, normatively, and the parts that are computable are pinned by shared test vectors that both the Python and JavaScript implementations must pass.
4. Existing data that does not meet the contract is recorded in a pinned **non-conformance register**, so it cannot grow silently.

5. Freshness can no longer make a result less restrictive. The known staleness-ordering defect is fixed at runtime (5.9), so the shipped behaviour matches the contract this milestone establishes.

**One deliberate behaviour change:** the staleness fix in 5.9, applied to `v2/` and to the root legacy `trip-rules.js`. Apart from that there must be no user-visible change: no published data file changes, and no other browser code changes.

## 3. In scope

1. Normative contract document (rewrite of `v2/pipeline/docs/data-contract.md`).
2. JSON Schema for the region manifest.
3. Two manifests: Aspen and Douglas County.
4. Python validator module with stable rule IDs.
5. Python `freshness` function at parity with `Trust.freshness`, shared test vectors, and its use in `lib/rules.py`.
6. Tests, including negative tests per rule and pinned non-conformance sets.
7. The staleness-ordering fix in `v2/trip-rules.js`, `v2/trust.js` and the root legacy `trip-rules.js`, exactly as specified in 5.9 and nothing more.
8. Small documentation updates.

## 4. Out of scope (do not do these)

- Any change to `v2/app.js`, `v2/map-layers.js`, `v2/trail-discovery.js`, `v2/index.html`, `v2/styles.css`, or any `.js`, `.css` or `.html` under `v2/regions/`. Any change to `v2/trip-rules.js` or `v2/trust.js` beyond 5.9.
- Any change to the content of a published data file: `v2/map-data-v2.json`, `v2/trails.geojson`, `v2/overnight-options.json`, `v2/ridb-options.json`, `v2/destinations.json`, `v2/map-data.json`, `v2/regions/douglas-co/research.json`, `v2/pipeline/config/rules-registry.json`.
- Any change to `lib/validation.py::validate_bundle`. Any change to `v2/pipeline/schema/schema.json` other than the single property named in amendment A1 (5.4).
- Any change to fetch or build scripts (`01`–`09`, `fetch_*.py`, `enrich_douglas.py`, `check_ridb.py`, `run_pipeline.py`). In particular, do not make the pipeline write manifests. **One exception (A1):** `08_ingest_leads.py` may be changed only as far as needed to emit `verification_method: null` instead of `"community_report"`.
- Moving or renaming Aspen data files, renaming layer keys, renaming `ASPEN_*` variables.
- Region selection, a region loader, or any browser consumer of the manifest (Milestone 3).
- Fixing any item in the non-conformance register (section 7.6). They are recorded, not repaired. The staleness defect is the one exception and is specified in 5.9.
- Land styling, legend or colour changes; reprocessing or reclassifying water; payload or provenance de-duplication; any new label, panel or other UI change.
- Running any live fetch.
- New dependencies, `package.json`, linters, formatters or a JSON Pointer library.
- The root legacy site, with one narrow exception approved by the owner: the staleness fix to the root `trip-rules.js` in 5.9. No other root file changes. Do not modernise, refactor, restyle, back-port the stay-limit check, or otherwise touch the legacy site.

## 5. Architecture and data-contract changes

### 5.1 Design summary

- The manifest is **static and hand-reviewed**. It holds declarations that change only when a human changes the region's sources or scope.
- **Dynamic** facts (when a fetch last ran, whether it failed) stay in the data files where the pipeline already writes them. The manifest points at them.
- The manifest is additive. Existing files, envelopes and the Aspen bundle schema are untouched.
- No index of regions. Regions are discovered by globbing `v2/regions/*/region.json`.
- **Forward compatibility for payload work.** The manifest's `sources` are the authoritative provenance declaration. R23 and R24 are written against "the feature's evidence", so a later milestone can replace the repeated per-feature `evidence` object with a reference to a declared source without changing any evidence semantics. M2 does not change payload or de-duplicate provenance, and payload optimisation must not be used as a reason to alter the semantics in 5.4.

Recommendation, not current behaviour: Milestone 3 makes the browser read the manifest for coverage and source panels and retires the non-conformances. This milestone only makes that possible.

### 5.2 Region manifest

Location: `v2/regions/<region_id>/region.json`. All `path` values are relative to the `v2/` directory, use `/` separators, and contain no `..` segment and no leading `/`. `pointer` is an RFC 6901 JSON Pointer; the empty string means the document root.

```json
{
  "contract_version": 1,
  "region": {"id": "douglas-co", "name": "Douglas County, Colorado", "state": "CO", "status": "research_only"},
  "coverage": {
    "path": "regions/douglas-co/research.json",
    "pointer": "/layers/coverage/features/0",
    "kind": "clipping_boundary",
    "source_id": "census_county",
    "statement": "County boundary used to clip sources. It is not a land-ownership or access boundary. Nothing is known outside it."
  },
  "sources": {
    "usgs_nhd": {
      "type": "agency",
      "agency": "USGS",
      "source_urls": ["https://hydro.nationalmap.gov/arcgis/rest/services/nhd/MapServer/12", "https://hydro.nationalmap.gov/arcgis/rest/services/nhd/MapServer/6"],
      "scope": "Named waterbodies and flowlines only, selected by name. A display subset, not complete hydrology. A name does not indicate recreational usefulness, public access, fishing or paddling permission."
    }
  },
  "layers": [
    {
      "id": "waterways",
      "kind": "water",
      "format": "feature_collection",
      "path": "regions/douglas-co/research.json",
      "pointer": "/layers/waterways",
      "source_ids": ["usgs_nhd"],
      "status_ref": {"path": "regions/douglas-co/research.json", "pointer": "/source_status/waterways"},
      "max_age_hours": 168,
      "geometry_types": ["LineString", "MultiLineString"],
      "allow_null_geometry": false,
      "must_be_empty": false,
      "extent_padding_deg": 0,
      "spatial_precision": "source_published",
      "fields": {"source": ["manager"], "derived": []},
      "limitations": "Named features only."
    }
  ],
  "rules": null,
  "fact_coverage": { "...": "exactly the eight dimensions in 5.5" },
  "known_gaps": ["..."]
}
```

Field definitions:

| Field | Rule |
|---|---|
| `contract_version` | Constant `1`. |
| `region.id` | `^[a-z0-9-]+$`, equal to the manifest's directory name. |
| `region.status` | Constant `research_only`. The schema has no other value. |
| `coverage.kind` | `clipping_boundary` (from a declared source; `source_id` required) or `project_defined_extent` (hand-authored; `source_id` must be `null`). |
| `coverage.statement` | Non-empty. Must say the boundary is not an ownership or access boundary. |
| `sources.<id>.type` | `agency`, `derived`, `curated`, or `community`. |
| `sources.<id>.source_urls` | Array of `http(s)` URLs. At least one for `agency` and `derived`; may be empty for `curated` and `community`, whose records carry their own URLs. |
| `sources.<id>.scope` | Non-empty statement of what the source does **not** establish. |
| `layers[].kind` | One of: `land_management`, `wilderness`, `roads`, `trails`, `water`, `recreation_sites`, `overnight_inventory`, `destinations`, `research_areas`, `restriction_monitor`, `wildlife_context`, `community_leads`, `reviewed_sites`. There is deliberately no `ownership` kind. |
| `layers[].format` | `feature_collection` or `place_list`. A `place_list` layer also has `list_key` (for example `places`, `resorts`) and omits `geometry_types`, `allow_null_geometry`, `extent_padding_deg` and `fields`. |
| `layers[].status_ref` | `{path, pointer}` to a transport record (5.3), or `null`. `null` is permitted without a register entry only when every source of the layer has type `curated`. |
| `layers[].max_age_hours` | Positive number, or `null` meaning "no freshness policy is defined; show the retrieval date and never label it current". |
| `layers[].must_be_empty` | `true` forbids any feature. Used for synthetic campsite points. |
| `layers[].extent_padding_deg` | Non-negative number. Degrees by which features may lie outside the coverage bounds. |
| `layers[].spatial_precision` | Required for `feature_collection` layers. `generalized` (limited-scale or simplified geometry that cannot locate a boundary at site level), `source_published` (geometry as the agency publishes it, possibly clipped), or `computed` (geometry produced by the pipeline). It describes the geometry only. It is the data a later UI needs to avoid drawing generalized context as if it were a surveyed boundary. |
| `layers[].classification_source_field` | Required for `land_management` layers, forbidden elsewhere. Names the property that holds the source's own classification code, verbatim. It must be listed in `fields.source`. |
| `layers[].fields.source` | Property names copied or renamed from a source attribute without interpretation. |
| `layers[].fields.derived` | Property names computed or mapped by the pipeline. |
| `rules` | `null` or `{"path": "..."}` pointing at a rules registry scoped to this region. |
| `known_gaps` | Array of non-empty strings. |

Every object in the schema sets `additionalProperties: false`.

### 5.3 Transport record

A transport record says whether the last retrieval attempt worked. It says nothing about what the source means.

Canonical shape, required for any new region or producer:

```json
{"status": "available", "last_checked_at": "2026-09-27T14:16:40Z", "last_retrieved_at": "2026-09-27T14:16:40Z", "count": 2359}
{"status": "unavailable", "last_checked_at": "...", "last_retrieved_at": "...", "reason": "...", "retained_previous": true}
```

- `status`: `available`, `unavailable` or `skipped`.
- `last_checked_at`: last attempt, successful or not.
- `last_retrieved_at`: last successful retrieval. Never advanced by a failed attempt.
- A transport record never contains `last_confirmed_at` or any other confirmed/verified timestamp. A successful retrieval or check advances only the checked and retrieved timestamps. Confirmation belongs to claims (5.4).

Legacy aliases, read by `normalize_transport` and reported so that tests can pin them:

| Legacy field or value | Normalised to | Present in |
|---|---|---|
| `completed_at` | `last_retrieved_at` and `last_checked_at` | Aspen bundle `source_status.*` |
| `retrieved_at` | `last_retrieved_at` | Douglas `source_status.*` |
| `checked_at` | `last_checked_at` | written by `enrich_douglas.py` on failure |
| `status: "failed"` | `unavailable` | written by `enrich_douglas.py` on failure |
| `error` | `reason` | written by `enrich_douglas.py` on failure |
| `available` with `last_checked_at` and no retrieval field | `last_retrieved_at := last_checked_at` | `ridb-options.json` |
| `last_confirmed_at` present on a transport record | ignored; never read as a confirmation; reported as legacy alias `last_confirmed_at` | `ridb-options.json` (N3) |

If `last_checked_at` is absent after aliasing, it takes the value of `last_retrieved_at`.

### 5.4 Evidence semantics (normative)

Six distinct concepts. A value in one never implies a value in another.

| Concept | Question | Values | Carried by |
|---|---|---|---|
| Existence | Does a source list this feature or facility? | presence of a record | the feature or place record itself |
| Provenance | Where did this record come from, and when was it copied? | `source_url`, `agency`, `retrieved_at` | feature `evidence`, manifest `sources` |
| Transport | Did the last retrieval attempt work? | `available`, `unavailable`, `skipped` | transport record |
| Interpretation (permission, access, restriction) | What does a reviewed source say about one fact for one place? | `unknown`, `supported`, `restricted` | claim object, rule record |
| Verification | Did a person review that interpretation, how, and when? | `basis`, `verification_method`, `last_confirmed_at`, `last_verified` | claim object, rule record, `evidence` |
| Freshness | Is that verification still within policy? | `current`, `stale`, `unavailable` | **computed, never stored** |

Existence is the weakest of these. A record existing, with good provenance and a successful recent fetch, still says nothing about permission, access or current status.

Rules:

1. **Unknown is the default.** A missing claim, a missing layer, an empty layer and an unavailable source all mean unknown. None means "private", "closed", "open", "unrestricted" or "permitted".
2. **A fetch is not a confirmation.** A successful retrieval or check advances only checked/observed timestamps: `retrieved_at`, `last_retrieved_at`, `last_checked_at`. It never advances `last_confirmed_at` or `last_verified`. Only manual review, or a structured source field that the contract names as validated, advances a confirmation timestamp, and only for that one fact.
3. **Retrieval date is not content date.** `retrieved_at` says when Ohvernight copied the record, not when the agency last revised it.
4. **`evidence.confidence` is deprecated.** It is retained for schema compatibility. It must not be displayed, branched on, or read as confidence in ownership, access or permission. New producers set it but consumers ignore it.
5. **`evidence.last_verified`** may be non-null only when `verification_method` is `manual_claim_review`. It is therefore always `null` when `verification_method` is `null`.
6. **Freshness never weakens a restriction.** A stale or never-confirmed `supported` claim is treated as `unknown`. A stale or never-confirmed `restricted` claim, exclusion, limit or caution **remains in force** and is additionally flagged as needing review. Evaluation order must not let a staleness result pre-empt a known tent-only, clearance, seasonal, stay-limit or other restriction. Section 5.9 makes the shipped code conform.
7. **Freshness thresholds are product review policy**, held in data (`max_age_hours`), not in code.
8. **Trip-scoped evaluations** carry the `evaluated_trip` they were computed for. They are historical for any other trip.
9. **Generated geometry** stays `needs_review: true`, `camping_permission: "unknown"` and never produces point campsites.
10. **Validation is time-independent.** No contract check depends on the current date. Data getting older must never fail CI.
11. **Non-federal is not private.** A private classification may be published only where the source itself classifies the land as private, and then only as the source's generalized classification. The absence of a federal or public polygon, an unshaded area, and an unrecognised agency code all mean unknown.
12. **Ownership is not access.** Ownership or managing-agency classification and public access are separate dimensions. Public or agency-managed land does not establish that the public may enter, cross, park or stay. Private classification does not by itself establish that access is prohibited.
13. **Presentation must not exceed the evidence.** A consumer must not present a `generalized` or `computed` layer with styling, labels or wording that implies a surveyed, parcel-level or legally precise boundary. This rule binds future UI work; M2 records the current gap as N17 and does not change styling.
14. **Positive claims fail closed.** Any value that asserts permission, access, openness or support requires a complete claim object or reviewed record. If any required part is missing, the value is `unknown` and the validator rejects the positive value.
15. **A mapped feature is not permission.** A mapped road, trail, facility or water feature, and proximity to public land or to any of these, does not establish legal access, camping permission, road access, trail access or recreational permission. Straight-line proximity is not a connection.
16. **No verification method is not a verification.** `verification_method: null` means none has been applied. It never implies verified, reviewed, confirmed, permitted, current or trusted. A community lead remains unverified whether or not it falls inside a candidate area and whether or not ingestion succeeded.

Timestamps are RFC 3339 in UTC.

**Claim object.** Used wherever one fact about one place is interpreted:

```json
{"status": "unknown"}
{"status": "restricted", "source_url": "https://...", "scope": "...", "basis": "manual_review",
 "last_checked_at": "...", "last_confirmed_at": "...", "max_age_hours": 720,
 "effective_from": null, "effective_to": null}
```

`status` other than `unknown` requires `source_url` (`http(s)`), non-empty `scope`, `basis` in {`manual_review`, `validated_structured_field`}, `last_confirmed_at`, and `max_age_hours > 0`.

**Rule record** (rules registry): requires `id`, non-empty `scope`, `source_url`, `last_confirmed_at`, `max_age_hours > 0`, and `camping_permission == "unknown"`. Every `place_ids` entry resolves to a place ID in the same region's `place_list` layers, or to `ridb-<id>` where `<id>` is the `ridb_facility_id` of such a place.

**Reserved feature properties.** These names may appear on any feature, are never listed under `fields`, and take only these values:

| Property | Allowed values |
|---|---|
| `id` | non-empty string |
| `name` | string or `null` |
| `evidence` | provenance object |
| `camping_permission` | `"unknown"`. `"supported_for_trip"` only in a `reviewed_sites` layer, and only with `needs_review: false`, an `evaluated_trip`, and `evidence.verification_method == "manual_claim_review"`. |
| `access_status` | `"unknown"`, `"restricted"`, `"designated_open"`. Any value other than `"unknown"` requires `evaluated_trip`, `access_reason`, and `road_conditions == "unknown"`. |
| `access_reason` | string |
| `road_conditions` | `"unknown"` |
| `land_class` | `"unknown"` |
| `needs_review` | boolean |
| `actual_site_confirmed` | `false`, or `true` only in a `reviewed_sites` layer |
| `evaluated_trip` | `{arrive, depart, vehicle}` |

**`verification_method`** (amended by A1). The value is either `null` or exactly one of six approved strings: `arcgis_rest_query`, `source_fetch`, `rest_api`, `html_change_monitor`, `derived_intersection`, `manual_claim_review`.

- `null` means no verification method has been applied to the record.
- `null` must never be read, displayed or branched on as verified, reviewed, confirmed, permitted, current or trusted.
- Any non-null value must be one of the six strings. Any other string, including `community_report` and the empty string, is invalid.
- An unverified community lead stays unverified regardless of spatial intersection with a candidate area and regardless of successful ingestion. In a `community_leads` layer the value must be `null`.
- Where a report or record came from is provenance. It is carried by `evidence.source_url`, `evidence.agency` and, for leads, `evidence.reported_at`. Do not add a provenance field for this.
- The five retrieval and derivation strings describe how a record was obtained or computed. Only `manual_claim_review` records a human review, which is why rule 5 ties `last_verified` to it.

Authorised changes for A1, and nothing beyond them:

- `v2/pipeline/scripts/08_ingest_leads.py`: pass `None` as the verification method in the existing `make_evidence` call. No other change to that file. `lib/evidence.py::make_evidence` already accepts it and needs no change for this.
- `v2/pipeline/schema/schema.json`: `$defs.evidence.properties.verification_method` becomes `{"type": ["string", "null"], "minLength": 1}`. The property stays in `required`. No other change to that file. The bundle schema does not enumerate method strings today and still does not; the enumeration is enforced by R23.

The enumeration of every `make_evidence` / `derived_evidence` call site and literal `verification_method` in `v2/pipeline/scripts/` is still required. If any script other than `08_ingest_leads.py` emits a value outside the six strings, **stop and report it**.

### 5.5 Fact coverage

Each manifest declares exactly these eight dimensions: `ownership`, `public_access`, `camping_permission`, `closures`, `restrictions`, `road_access`, `trail_access`, `recreation_permission`.

```json
"ownership": {"state": "context", "layer_ids": ["land"], "official_urls": [], "statement": "..."}
```

| `state` | Meaning |
|---|---|
| `none` | No evidence for this dimension is loaded. |
| `context` | Generalised or source-published context is loaded. It cannot answer the question for a specific site or trip. `layer_ids` must be non-empty. |
| `reviewed_partial` | At least one individually reviewed record exists. Everything else is unknown. Requires a non-null `rules`, or a `reviewed_sites` layer with at least one feature. |

There is deliberately **no state meaning complete, verified or permitted**. The schema cannot express a positive regional claim.

### 5.6 Manifest content

Use this content exactly. The statements are trust-bearing; do not reword them. Source `scope` text not given below is copied from `v2/pipeline/config/sources.yaml` where a `scope` exists.

**Aspen** — `v2/regions/aspen/region.json`. `region`: id `aspen`, name `Aspen / Snowmass pilot`, state `CO`. `coverage`: path `pipeline/config/aoi.geojson`, pointer `""`, kind `project_defined_extent`, `source_id: null`, statement "Project-defined research extent. It is not a land-ownership or access boundary. Nothing is known outside it." `rules`: `{"path": "pipeline/config/rules-registry.json"}`.

Sources:

| id | type | agency | source_urls | scope |
|---|---|---|---|---|
| `blm_sma` | agency | BLM multi-agency Surface Management Agency | `https://gis.blm.gov/arcgis/rest/services/lands/BLM_Natl_SMA_LimitedScale/MapServer/1` | from `sources.yaml` |
| `usfs_wilderness` | agency | USFS | `https://apps.fs.usda.gov/arcx/rest/services/EDW/EDW_Wilderness_01/MapServer/0` | Designated wilderness boundaries. Not a statement of current rules or access. |
| `usfs_mvum` | agency | USFS | `https://apps.fs.usda.gov/arcx/rest/services/EDW/EDW_MVUM_02/MapServer/1` | Published motor-vehicle designations. Not current passability, snow status or overnight permission. |
| `usgs_nhd` | agency | USGS | `.../nhd/MapServer/6`, `/9`, `/12` | Hydrography retained for setback screening. Feature type, flow permanence and size are not carried. A name does not indicate recreational usefulness, public access or seasonal flow. |
| `usfs_trails` | agency | USDA Forest Service | `https://apps.fs.usda.gov/arcx/rest/services/EDW/EDW_TrailNFSPublishWithDataStatus_01/MapServer/0` | Published trail geometry and use strings. Not current access or closures. |
| `ridb` | agency | Recreation.gov / RIDB | `https://ridb.recreation.gov/api/v1` | Facility inventory only. No availability, operating dates or vehicle-sleeping permission. |
| `pitkin_fire_page` | agency | Pitkin County | `https://pitkincounty.com/CivicAlerts.asp` | from `sources.yaml` |
| `cdot_wildlife` | agency | CDOT | the `sources.yaml` `wildlife.base_url` | Source disabled. Habitat context is not a closure. |
| `ohvernight_pipeline` | derived | Aspen research pipeline | `https://github.com/k-kopacek/ohvernight` | Computed screening geometry. Not a campsite and not permission. |
| `curated_inventory` | curated | Ohvernight manual research | `[]` | Hand-researched listings with per-record source links. Listing a place does not confirm permission, operation or availability. |
| `community_leads` | community | Community reports | `[]` | Unverified reports. |
| `osm_destinations` | curated | OpenStreetMap contributors | `[]` | Orientation points only; not reviewed arrival or parking points. |

Layers (`BUNDLE` = `map-data-v2.json`; status pointer is into the same file):

| id | kind | path / pointer | sources | status pointer | max_age_hours | geometry_types | flags | fields.source | fields.derived |
|---|---|---|---|---|---|---|---|---|---|
| `land_ownership` | land_management | BUNDLE `/layers/land_ownership` | blm_sma | `/source_status/01_fetch_land_ownership` | null | Polygon, MultiPolygon | | raw_admin_agency | manager |
| `wilderness` | wilderness | BUNDLE `/layers/wilderness` | usfs_wilderness | `/source_status/01_fetch_land_ownership` | null | Polygon, MultiPolygon | | | |
| `mvum_roads` | roads | BUNDLE `/layers/mvum_roads` | usfs_mvum | `/source_status/02_fetch_mvum_roads` | null | LineString, MultiLineString | | source_route_id, mvum_symbol, operational_maintenance_level, designations | vehicle_class |
| `hydrology` | water | BUNDLE `/layers/hydrology` | usgs_nhd | `/source_status/03_fetch_hydrology` | null | LineString, MultiLineString, Polygon, MultiPolygon | `extent_padding_deg: 0.005` | | kind |
| `lodging_developed` | overnight_inventory | BUNDLE `/layers/lodging_developed` | ridb | `/source_status/04_fetch_campgrounds_ridb` | 168 | Point | | see note | see note |
| `wildlife_sensitivity` | wildlife_context | BUNDLE `/layers/wildlife_sensitivity` | cdot_wildlife | `/source_status/05_fetch_wildlife_closures` | 24 | Polygon, MultiPolygon | | | |
| `fire_restriction_stage` | restriction_monitor | BUNDLE `/layers/fire_restriction_stage` | pitkin_fire_page | `/source_status/06_fetch_fire_stage_monitor` | 24 | (empty list) | `allow_null_geometry: true` | | type, status, stage, last_checked_at, last_confirmed_at, max_age_hours, source_hash, source_changed |
| `dispersed_corridors` | research_areas | BUNDLE `/layers/dispersed_corridors` | ohvernight_pipeline | `/source_status/07_build_dispersed_corridors` | null | Polygon, MultiPolygon | | | site_type, source_road_id, applicable_rule_context, required_checks |
| `dispersed_corridor_points` | research_areas | BUNDLE `/layers/dispersed_corridor_points` | ohvernight_pipeline | `/source_status/07_build_dispersed_corridors` | null | Point | `must_be_empty: true` | | |
| `leads` | community_leads | BUNDLE `/layers/leads` | community_leads | `/source_status/08_ingest_leads` | null | Point | | see note | see note |
| `reviewed_sites` | reviewed_sites | BUNDLE `/layers/reviewed_sites` | curated_inventory | `/source_status/09_reviewed_sites` | null | Point | | see note | see note |
| `trails` | trails | `trails.geojson` `""` | usfs_trails | **null** | null | LineString, MultiLineString | | trail_number, surface, attribute_subset, allowed_terra_use, activities | |
| `overnight_options` | overnight_inventory | `overnight-options.json`, `list_key: places` | curated_inventory | null | null | — | place_list | — | — |
| `ridb_options` | overnight_inventory | `ridb-options.json`, `list_key: places` | ridb | `ridb-options.json` `/source_status` | 168 | — | place_list | — | — |
| `destinations` | destinations | `destinations.json`, `list_key: resorts` | osm_destinations | null | null | — | place_list | — | — |

Note for the three currently empty layers (`lodging_developed`, `leads`, `reviewed_sites`): populate `fields` from the property names the producing script emits (`04_fetch_campgrounds_ridb.py`, `08_ingest_leads.py`, `09_reviewed_sites.py`), classified by the rule in 5.2, and list the result in the PR description for review. For `leads`, the fields are derived from `08_ingest_leads.py` as amended by A1.

`spatial_precision`: `generalized` for `land_ownership`; `computed` for `dispersed_corridors` and `dispersed_corridor_points`; `source_published` for every other `feature_collection` layer. `classification_source_field` for `land_ownership`: `raw_admin_agency`.

`limitations` for `hydrology`: "Retained for setback screening. Display currently selects features by name only; a name is not evidence of recreational usefulness, access or flow." For `land_ownership`: "Limited-scale management context. `manager` is mapped from the source agency code; an unrecognised code is Unknown, never Private." Other layers: a non-empty sentence taken from the matching source `scope`.

Fact coverage:

| Dimension | state | layer_ids | official_urls | statement |
|---|---|---|---|---|
| ownership | context | land_ownership | — | Limited-scale managing-agency polygons only. They are not parcels or surveyed boundaries. A Private label repeats the source's generalized classification and is not a parcel-level finding. Land outside a federal polygon is not thereby private, and unshaded land is unknown. |
| public_access | none | — | — | No public-access evidence is loaded. Ownership and access are separate questions: managing-agency context, a mapped road or trail, or nearby public land does not establish that the public may enter or cross land. |
| camping_permission | none | — | — | No camping permission is confirmed anywhere in this region. No listed facility, research area or rule record asserts it; wherever the field is present its value is unknown. A listing shows that a facility exists, not that a given setup may stay. |
| closures | none | fire_restriction_stage, wildlife_sensitivity | `https://pitkincounty.com/CivicAlerts.asp`, `https://www.fs.usda.gov/r02/whiteriver/alerts/aspen-rd-occupancy-and-use-prohibitions` | No closure or fire-restriction status is confirmed. The county page monitor detects page changes only and the wildlife source is unavailable. No mapped closure does not mean no closure. |
| restrictions | reviewed_partial | — | — | One reviewed rule record exists, for the agency-listed Lincoln Creek dispersed sites. All other stay limits, seasons, permits and orders are unknown. |
| road_access | context | mvum_roads | — | USFS motor-vehicle designations, evaluated for the trip recorded on each feature and not for the visitor's trip. Current conditions, snow, passability and the full approach are unknown. |
| trail_access | context | trails | — | USFS published trail-use strings, kept verbatim. Not evaluated against dates, closures or current conditions. |
| recreation_permission | none | hydrology | — | No recreational-use permission is loaded. A mapped or named water feature does not establish public access, fishing, paddling or swimming permission, or that the water is usable for recreation. Distances to trails, roads and water are straight-line and are not connections. |

`known_gaps`: the three strings currently in the bundle's `coverage_gaps`, verbatim.

**Douglas County** — `v2/regions/douglas-co/region.json`. `region` and `coverage` as in the example in 5.2. `rules`: `null`. All layers: path `regions/douglas-co/research.json`, `max_age_hours: 168` (the policy already shipped in `preview.js`).

Sources: `census_county` (US Census Bureau, `https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/State_County/MapServer/1`, scope "County boundary used for clipping. Not a land-ownership polygon."), `usfs_trails`, `usfs_mvum`, `usfs_wilderness`, `blm_sma` (URLs as Aspen), `usfs_rec_sites` (USFS, `https://apps.fs.usda.gov/arcx/rest/services/EDW/EDW_RecInfraRecreationSites_02/MapServer/0`, scope "Recreation-site inventory. Season and operational attributes can be historical; no live open status."), `usgs_nhd` (URLs `/12` and `/6`, scope "Named waterbodies and flowlines only, selected by name. A display subset, not complete hydrology. A name does not indicate recreational usefulness, public access, fishing or paddling permission."). For `usfs_mvum` in this region the scope is "Road geometry only. Vehicle and season designations are not evaluated."

| id | kind | pointer | sources | status pointer | geometry_types | fields.source |
|---|---|---|---|---|---|---|
| `trails` | trails | `/layers/trails` | usfs_trails | **null** | LineString, MultiLineString | trail_number, surface, attribute_subset, allowed_terra_use, activities |
| `roads` | roads | `/layers/roads` | usfs_mvum | **null** | LineString, MultiLineString | source_route_id |
| `recreation` | recreation_sites | `/layers/recreation` | usfs_rec_sites | `/source_status/recreation` | Point | site_name, site_type, activity_type_list, seasonal_operational_status, op_status_reason, fee_description, open_season, usda_portal_url, rec1stop_url, important_info, restrictions, water_availability, restroom_availability, directions |
| `land` | land_management | `/layers/land` | blm_sma | `/source_status/land` | Polygon, MultiPolygon | manager |
| `wilderness` | wilderness | `/layers/wilderness` | usfs_wilderness | `/source_status/wilderness` | Polygon, MultiPolygon | manager |
| `waterbodies` | water | `/layers/waterbodies` | usgs_nhd | `/source_status/waterbodies` | Polygon, MultiPolygon | manager |
| `waterways` | water | `/layers/waterways` | usgs_nhd | `/source_status/waterways` | LineString, MultiLineString | manager |

All `fields.derived` are empty.

`spatial_precision`: `generalized` for `land`; `source_published` for every other layer. `classification_source_field` for `land`: `manager`. `limitations` for `waterbodies` and `waterways`: "Named features only. A name is not evidence of recreational usefulness, access or flow." For `land`: "Limited-scale management context. `manager` is the source agency code, verbatim." Other layers: a non-empty sentence taken from the matching source `scope`.

| Dimension | state | layer_ids | official_urls | statement |
|---|---|---|---|---|
| ownership | context | land | — | Five limited-scale management polygons only. They are not parcels or surveyed boundaries. The PVT code repeats the source's generalized classification and is not a parcel-level finding. Land outside a federal polygon is not thereby private, and unshaded land is unknown. |
| public_access | none | — | — | No public-access evidence is loaded. Ownership and access are separate questions: managing-agency context, a mapped road or trail, or nearby public land does not establish that the public may enter or cross land. |
| camping_permission | none | — | — | No camping permission is confirmed. A recreation-site record shows that a facility is listed, not that it is open or that a given setup may stay. |
| closures | none | — | `https://dcsheriff.net/sheriffs-office/divisions/emergency-management/fire-restrictions/` | No closure or fire-restriction status is loaded. The linked county page covers county jurisdiction only; federal orders must be checked separately. |
| restrictions | none | — | — | No reviewed stay limits, seasons, permits or orders are loaded. |
| road_access | context | roads | — | USFS road geometry only. Vehicle and season designations are not evaluated; access status is unknown on every feature. |
| trail_access | context | trails | — | USFS published trail-use strings, kept verbatim. Segments are clipped at the county boundary and are not complete routes. Not evaluated against closures or current conditions. |
| recreation_permission | none | waterbodies, waterways | — | No recreational-use permission is loaded. A mapped or named water feature does not establish public access, fishing, paddling or swimming permission, or that the water is usable for recreation. Distances to campgrounds, trailheads and trails are straight-line and are not connections. |

`known_gaps`: the snapshot's current `notes` verbatim, followed by "No live restrictions feed.", "No precise parcel data.", "No verified dispersed-camping candidates."

### 5.7 Validator

New module `v2/pipeline/scripts/lib/region_contract.py`.

- `ContractError(ValueError)` with attributes `rule`, `region`, `layer`. `str()` begins `"<rule> <region>/<layer>: "`.
- `normalize_transport(record) -> (normalized: dict, legacy_used: list[str])`.
- `validate_region_data(manifest, resolve) -> report`. `resolve(path)` returns the parsed JSON document for a `path`. Pure: no file access, no clock.
- `validate_region(manifest_path, v2_root=None) -> report`. Loads the manifest, checks R03, builds a caching `resolve` over `v2_root`, calls `validate_region_data`.
- `report` is a dict: `{"region", "layers": {id: feature_count}, "unrecorded_status_layers": [...], "legacy_transport": {layer_id: [aliases]}}`.
- JSON Pointer resolution is a small local function (RFC 6901, including `~0` and `~1`).
- The module must not import `datetime.now`, `time`, or otherwise read the clock.

Rules. Each failure raises `ContractError` with the rule ID.

| ID | Rule |
|---|---|
| R01 | Manifest validates against `region-manifest.schema.json`. |
| R02 | `region.id` equals the manifest's directory name. |
| R03 | Every `path` is relative, has no `..` and no leading `/`, and resolves to an existing file under `v2/`. |
| R04 | Layer IDs are unique. Every `source_id` is declared. Every declared source is used by a layer or by `coverage`. |
| R05 | `fact_coverage`: every `layer_ids` entry is a declared layer; `context` has at least one; `reviewed_partial` meets 5.5. |
| R10 | Coverage resolves to a GeoJSON Feature whose geometry is a valid, non-empty Polygon or MultiPolygon within longitude ±180 and latitude ±90. |
| R20 | A `feature_collection` layer resolves to an object with `type == "FeatureCollection"` and a `features` list. |
| R21 | Every feature `properties.id` is a non-empty string, unique across **all** `feature_collection` layers of the region. |
| R22 | Geometry is `null` only when `allow_null_geometry`. Otherwise it is valid, non-empty, of a declared type, and its bounds lie within the coverage bounds expanded by `extent_padding_deg + 1e-6`. |
| R23 | Every feature has `evidence` with an `http(s)` `source_url`, non-empty `agency`, an RFC 3339 `retrieved_at`, and a `verification_method` key that is present and is either `null` or one of the six approved strings. A missing key, an empty string or any other string fails. |
| R24 | For a layer whose sources are all `agency` or `derived`: every feature's `evidence.source_url` equals a declared `source_urls` entry of one of the layer's sources, or starts with such an entry followed by `/` or `?`. |
| R25 | `evidence.last_verified` is `null` unless `verification_method == "manual_claim_review"`. |
| R26 | Every feature property name is reserved, or listed in the layer's `fields.source` or `fields.derived`. No reserved name appears in `fields`. |
| R27 | Reserved properties hold only the values allowed in 5.4. |
| R28 | Kind rules. `research_areas`: `needs_review is True`, `camping_permission == "unknown"`, `actual_site_confirmed is False`, `evaluated_trip` present. `community_leads`: `needs_review is True`, `camping_permission == "unknown"`, `evidence.verification_method is None` and `evidence.last_verified is None`. `restriction_monitor`: `needs_review is True`; `status` is `"unknown"` or `"confirmed"`; `"unknown"` requires `stage is None` and `last_confirmed_at is None`; `"confirmed"` requires non-null `last_confirmed_at`, `max_age_hours > 0` and `evidence.verification_method == "manual_claim_review"`. `must_be_empty` layers have zero features. `land_management`: every feature has a non-empty string in the layer's `classification_source_field`; and if any other property of the feature equals `private` (case-insensitive), that source field equals `PVT`. |
| R29 | `trails`: `properties.activities` has exactly the key set of `fetch_trails.ACTIVITIES`; each value has exactly `managed`, `accpt`, `disc`, `restricted`, each `None` or a string. |
| R30 | A non-null `status_ref` resolves to an object. After normalisation `status` is in the enum; `available` has a parseable `last_retrieved_at`; `unavailable` and `skipped` have a non-empty `reason`. A `last_confirmed_at` on the record is never used to satisfy this rule. |
| R31 | A layer with `status_ref: null` and any non-`curated` source is added to `report["unrecorded_status_layers"]`. This is reported, not raised. |
| R32 | If the transport record has `count`, it equals the layer's feature count. |
| R33 | If normalised `status` is not `available` and the layer has features, the record has `retained_previous is True`. |
| R40 | A `place_list` layer resolves to a list under `list_key`. Each item's `id` matches `^[a-z0-9_-]+$` and is unique within the layer. `coordinates` is `[lon, lat]`, finite and in range. |
| R41 | In a `place_list`: `camping_permission`, if present, is `"unknown"`; every value in `facts`, if present, is a valid claim object (5.4). |
| R50 | Rules registry: every rule is a valid rule record (5.4). |

### 5.8 Freshness parity

- Add `freshness(record, now)` to `v2/pipeline/scripts/lib/evidence.py`. `now` is a required timezone-aware `datetime`. It returns exactly what `Trust.freshness` returns in `v2/trust.js` for the same input: `unavailable` when `last_confirmed_at` is missing or unparseable, when `max_age_hours` is missing, non-numeric, zero or negative, or when the timestamp is in the future; `stale` when age is strictly greater than the threshold; otherwise `current`. A date-only string is midnight UTC.
- Change `lib/rules.py::match_rules` to call it. Behaviour change, pipeline only: a future-dated rule becomes `unavailable` instead of `stale`. Existing tests in `test_kickoff.py` must still pass unmodified.
- Add `v2/pipeline/tests/fixtures/freshness-vectors.json`: a list of `{name, now, record, expected}`. At least these cases: current; stale; age exactly equal to the threshold (`current`); one second over (`stale`); missing `last_confirmed_at` with a `last_checked_at` present; `null` `last_confirmed_at`; future timestamp; `max_age_hours` of `0`, `-1`, `null`, missing and `"24"`; unparseable timestamp; date-only timestamp; `null` record.
- Both languages run every vector.

### 5.9 Staleness must not weaken a restriction (runtime fix)

Verified defect at the base commit:

- `v2/trip-rules.js::evaluate` returns `review` / "Source review is stale" when `checked_on` is missing, in the future or more than 30 days old. That return sits **before** the tent-only, high-clearance and vehicle-access-season checks. Only the stay-limit check runs first.
- `v2/trust.js::applyRules` copies a matching rule's `stay_limit_days` and `requires_high_clearance` onto the place only when the rule is `current`.
- All five places in `overnight-options.json` have `checked_on: 2026-09-24`. From 2026-10-25, with no code change, Silver Bar (tent-only) and Lincoln Creek for a passenger car both change from `excluded` to `review`.

In `v2/` the fix is limited to these two functions; no other file under `v2/` changes for it. The root legacy copy is covered at the end of this section.

**`TripRules.evaluate(place, trip, today)`**

Define the *fresh result* as what the base-commit function returns for the same `place` and `trip` when the staleness check does not fire. Define `stale` by the existing predicate, unchanged (`checked_on` missing or unparseable, `today` unparseable, `today` before `checked_on`, or more than 30 days after it).

1. The invalid-trip-dates result is returned first, unchanged.
2. If not `stale`: return the fresh result with `sourceStale: false`. `status`, `label` and `tripNote` are identical to the base commit for every input.
3. If `stale` and the fresh result is a **restriction outcome** — `status === "excluded"`, or the "Motorhome suitability unverified" caution — return it with the same `status` and `label`, with `tripNote` equal to the fresh `tripNote` followed by the suffix below, and `sourceStale: true`.
4. If `stale` and the fresh result is anything else: return the existing stale result (`status: "review"`, label "Source review is stale", the existing `tripNote`) with `sourceStale: true`. This covers the lodging label, the dispersed label and the "Within the mapped campground-road designation" note. A stale supportive statement becomes unknown.
5. The relative order of every check other than staleness is unchanged.

Stale suffix, exact text, with one leading space: ` The source review is out of date; recheck the linked sources before travel.`

**`Trust.applyRules(place, registry, now)`**

1. The branch for zero or for two or more matching rules is unchanged.
2. For exactly one matching rule, restrictive values are merged **regardless of the rule's freshness**, and the most restrictive value wins:
   - `stay_limit_days` becomes the smallest finite positive number among `place.stay_limit_days ?? place.max_stay_days` and `rule.stay_limit_days`. If neither is a finite positive number, the property is not set.
   - `requires_high_clearance` becomes `true` if it is `true` on the place or on the rule. Otherwise the place's value is left as it is.
   - A rule value that is missing, `null` or less strict never replaces a stricter place value.
3. `ruleReview` and `ruleSource` are unchanged: `ruleReview` is `null` only when the rule is `current`.

The most-restrictive merge is part of this fix because applying stale rules unconditionally would otherwise let a stale, looser rule overwrite a stricter place value.

**Root legacy `trip-rules.js::evaluate`** (owner-approved exception to the legacy-site restriction)

The root file is a published surface with the same defect: its staleness return sits before the lodging, tent-only, high-clearance and vehicle-access-season checks. It has no stay-limit check and no rules registry.

- Apply the `TripRules.evaluate` contract above (steps 1–5) to the root function, with the same definition of `stale`, the same restriction outcomes, the same exact suffix and the same `sourceStale` property.
- "Fresh result" here means what the **root** base-commit function returns. Do not add the stay-limit check or anything else the root function does not already do.
- Change only what is needed to move the staleness decision. Keep the file's existing structure and formatting. Do not copy the `v2` file over it.
- No other root file changes: not `app.js`, `index.html`, `styles.css` or any root data file.

No Python change is needed for this section. `09_reviewed_sites.py` already fails closed: a stale review yields `needs_review: true` and `camping_permission: "unknown"`.

## 6. Files expected to change

New:

- `v2/pipeline/schema/region-manifest.schema.json`
- `v2/pipeline/scripts/lib/region_contract.py`
- `v2/regions/aspen/region.json`
- `v2/regions/aspen/README.md` — states that Aspen's app and data live in `v2/` and that this directory holds only the manifest.
- `v2/regions/douglas-co/region.json`
- `v2/pipeline/tests/test_region_contract.py`
- `v2/pipeline/tests/test_community_leads.py`
- `v2/pipeline/tests/fixtures/freshness-vectors.json`
- `v2/pipeline/tests/evidence-parity.test.cjs`
- `v2/pipeline/tests/staleness.test.cjs`
- `v2/pipeline/tests/fixtures/trip-evaluation-golden.json`

Modified:

- `v2/pipeline/docs/data-contract.md` — rewritten as the normative contract: sections 5.2–5.5 of this spec, the rule table, the legacy alias table, and the non-conformance register. Keep every existing statement that is still true, including the BLM topology paragraph and the Lincoln Creek counting caveat.
- `v2/pipeline/scripts/lib/evidence.py`, `v2/pipeline/scripts/lib/rules.py`
- `v2/pipeline/scripts/08_ingest_leads.py` — amendment A1 only.
- `v2/pipeline/schema/schema.json` — amendment A1 only (one property).
- `v2/trip-rules.js`, `v2/trust.js` — section 5.9 only.
- `trip-rules.js` (repository root) — section 5.9 only.
- `v2/pipeline/README.md` — one paragraph: adding or changing a layer, source or property requires updating the region manifest, and CI enforces it.
- `v2/regions/douglas-co/README.md` — one sentence pointing at `region.json` and the contract.
- `AGENTS.md` — under "Repository map", one bullet: each region has `v2/regions/<id>/region.json`, validated against `v2/pipeline/docs/data-contract.md`.

`.github/workflows/ci.yml` needs no change: Python tests are discovered and the Node glob picks up the new file. Do not edit it.

## 7. Trust and provenance requirements

1. Manifest statements in 5.6 are copied exactly. Any wording change needs owner approval.
2. No manifest, test or document may describe any region, layer or place as verified, complete, open, permitted or legal.
3. Never widen an allowed value set to make existing data pass. If real data fails a rule as written here, **stop and report** the rule ID, the file and the count. That is a finding for the reviewer, not something to code around.
4. Do not derive, backfill or invent a transport record, a timestamp or a claim. Missing stays missing and is reported through R31.
5. Preserve `DATA-LICENSE.md` attributions. Do not add source content to a manifest beyond the service URL, agency name and scope sentence.
6. **Non-conformance register.** Add this table to `data-contract.md`. These are known violations of the contract in shipped data or code. M2 records them and, except for N6, does not fix them.

| ID | Non-conformance | Pinned by test |
|---|---|---|
| N1 | No transport record: Aspen `trails`; Douglas `trails`, `roads`. A failed refresh of these is invisible. | yes (T5) |
| N2 | Legacy transport aliases: `completed_at` (Aspen bundle), `retrieved_at` (Douglas), `available` without a retrieval field (`ridb-options.json`). `enrich_douglas.py` would also write `failed`, `checked_at`, `error`. | yes (T5) |
| N3 | `ridb-options.json` `source_status.last_confirmed_at` is set by a fetch, contrary to rule 2 in 5.4, and `Trust.sourceSummary` reads it for inventory freshness. The validator ignores it and never treats it as a confirmation. Fixing the producer, the data file and the reader is deferred (decision D7). | yes (T5) |
| N4 | `evidence.confidence` is inconsistent across regions for the same source (F6). | T7 guards consumers |
| N5 | The Aspen layer key `land_ownership` says ownership, but the data is limited-scale management context. `Private` / `PVT` values are the source's generalized classification, not ownership findings. | kind is `land_management`; R28 |
| N6 | Staleness ordering in `trip-rules.js` and `Trust.applyRules`. **Fixed in M2 (5.9).** Kept in the register as a regression marker. | yes (T10–T14) |
| N7 | The Rampart designated-dispersed listing, including a paraphrased seasonal closure and a date-only `retrieved_at`, is hard-coded in `preview.js`, outside any data file or schema. | no — Milestone 3 |
| N8 | Aspen `mvum_roads` publishes `access_status: designated_open` on 51 features for a past trip (2026-09-25 to 26, high clearance). | R27 requires `evaluated_trip` |
| N9 | Freshness thresholds of 7 and 30 days are hard-coded in `preview.js` and `trip-rules.js`. The 30-day predicate is deliberately unchanged by 5.9. | no — Milestone 3 |
| N10 | Douglas `recreation` carries the verbatim source attribute `seasonal_operational_status` (`OPEN` on 35 of 36 records), which may be historical. | declared under `fields.source` |
| N11 | `place_list` records carry per-record source URLs that are not checked against declared sources. | no |
| N12 | The committed Douglas snapshot predates the current `fetch_douglas.py`: it has no `source_status` for trails or roads and different `notes`. | follows from N1 |
| N13 | `v2/map-data.json` (legacy OpenStreetMap extract) is published and not covered by any manifest. | no |
| N14 | Per-feature `evidence` is duplicated on every feature (payload size). Not addressed in M2; see the forward-compatibility note in 5.1. | no |
| N15 | The root legacy site's `trip-rules.js` had the same staleness-before-restrictions ordering. **Fixed in M2 (5.9)** by owner decision D6. Kept as a regression marker. | yes (T15) |
| N16 | Two orderings unrelated to freshness can still hide a restriction: in `trip-rules.js` the motorhome clearance caution returns before the vehicle-access-season exclusion, and `Trust.applyRules` applies no rule values when two or more rules match. | no |
| N17 | Land styling exceeds the evidence. The Douglas page fills limited-scale polygons with a distinct colour per manager code, including `PVT`; both apps draw generalized polygons as crisp boundaries. | `spatial_precision` declared; styling unchanged |
| N18 | Water lacks semantics for recreational usefulness. Display selection relies on the presence of a name; NHD feature type, permanence and size attributes are dropped at ingest in both regions. | declared in `limitations` and `recreation_permission` |

## 8. Test requirements

All tests are offline, write no file inside the repository, and do not read the clock. Resolve paths from `__file__`.

**`v2/pipeline/tests/test_region_contract.py`** (`unittest`):

- **T1 Real regions validate.** Glob `v2/regions/*/region.json`; assert the set of region IDs is exactly `{"aspen", "douglas-co"}`; `validate_region` raises nothing for each.
- **T2 Declared surface is complete.** The set of `path` values across the Aspen manifest equals exactly `{map-data-v2.json, trails.geojson, overnight-options.json, ridb-options.json, destinations.json, pipeline/config/aoi.geojson, pipeline/config/rules-registry.json}`. Douglas equals `{regions/douglas-co/research.json}`. Every key under the bundle's `layers` and under Douglas `layers` other than `coverage` is declared by a manifest layer.
- **T3 Fact coverage.** Each manifest has exactly the eight dimensions; the statements equal the text in 5.6 (compare against literals in the test).
- **T4 Negative tests, one per rule R01–R50 except R31.** Build a minimal valid synthetic region in memory (manifest dict plus a dict-backed `resolve`), assert it validates, then for each rule apply one mutation and assert `ContractError` with that exact `rule`. Mutations must include at least:
  - R22: a feature outside coverage; a null geometry where not allowed; an undeclared geometry type.
  - R24: an evidence URL from an undeclared host; a URL that merely shares a prefix without a `/` or `?` boundary (`.../MapServer/12` must not match a declared `.../MapServer/1`).
  - R25: `last_verified` set on an `arcgis_rest_query` feature.
  - R23: `verification_method: "community_report"`; `verification_method: ""`; the key absent. A positive case in the same test: a feature with `verification_method: null` in a non-lead layer validates.
  - R26: an undeclared property; a reserved name listed in `fields`.
  - R27: `camping_permission: "allowed"`; `camping_permission: "supported_for_trip"` outside `reviewed_sites`; `access_status: "designated_open"` without `evaluated_trip`; `land_class: "public"`; `road_conditions: "open"`.
  - R28: a research area with `needs_review: false`; a restriction monitor with `status: "confirmed"` and `verification_method: "html_change_monitor"`; a feature in a `must_be_empty` layer; a community lead with `verification_method: "source_fetch"`; a community lead with `needs_review: false`; a land feature with an empty classification source field; a land feature with `manager: "Private"` whose source field is `LG`.
  - R30: `status: "ok"`; `available` with no timestamp; `unavailable` with no reason.
  - R33: `unavailable` with features and no `retained_previous`.
  - R41: a `facts` entry `{"status": "supported"}` with no source.
  - R05: `reviewed_partial` with `rules: null` and no reviewed site; `context` with empty `layer_ids`.
  - R01: `region.status: "verified"`; a `fact_coverage` state of `"complete"`; a ninth dimension; a missing dimension.
- **T5 Pinned non-conformance.** `unrecorded_status_layers` equals exactly `["trails"]` for Aspen and `["roads", "trails"]` for Douglas (sorted). The set of legacy aliases used equals exactly `{"completed_at"}` across Aspen bundle layers, `{"retrieved_at"}` across Douglas layers, and the inferred-retrieval alias plus `last_confirmed_at` for `ridb_options`. A new region or layer using a legacy alias fails this test.
- **T6 `normalize_transport`.** Each row of the alias table in 5.3, plus a canonical record that reports no legacy use, plus `failed` → `unavailable`.
- **T7 Deprecated confidence is not consumed.** No file matching `v2/*.js` or `v2/regions/*/*.js` contains a match for the regular expression `\.confidence(?![-\w])|\[['"]confidence['"]\]` (the CSS class name `confidence-badge` is not a match).
- **T8 Clock independence.** The source text of `region_contract.py` does not contain `datetime.now`, `utcnow`, `date.today` or `import time`.
- **T9 Freshness vectors (Python).** Every vector in the fixture.

**`v2/pipeline/tests/test_community_leads.py`** (`unittest`, amendment A1). Offline; writes no file.

- **T16a Normalised lead is unverified.** Call `08_ingest_leads.normalize` with one lead that lies **inside** a candidate corridor polygon. Assert: `matched_candidate_ids` is non-empty; `evidence.verification_method is None`; `needs_review is True`; `camping_permission == "unknown"`; `evidence.confidence == "unverified"`; `evidence.last_verified is None`; `site_type == "dispersed_lead_unverified"`.
- **T16b Intersection changes nothing.** Normalise the same lead against no corridors. Every property asserted in T16a is equal, apart from `matched_candidate_ids` being empty.
- **T16c Origin is preserved without a new field.** A lead with `source_url`, `reported_by` and `reported_at` yields those values in `evidence.source_url`, `evidence.agency` and `evidence.reported_at`. The set of `evidence` keys equals the set produced at the base commit.
- **T16d The bundle schema accepts it.** Load the published bundle in memory, insert the T16a feature into `layers.leads`, and assert `validate_bundle` does not raise. Assert the feature does not appear in `site_feed.places`.
- **T16e The contract accepts it and nothing looser.** With the synthetic region from T4: a `community_leads` layer holding the T16a feature validates; the same feature with `verification_method: "community_report"` raises R23.
- **T16f The literal is gone.** The source text of `08_ingest_leads.py` does not contain `community_report`.

**`v2/pipeline/tests/evidence-parity.test.cjs`** (`node:test`): load the same fixture and assert `Trust.freshness(record, Date.parse(now)) === expected` for every vector, with one sub-test per vector name.

**`v2/pipeline/tests/staleness.test.cjs`** (`node:test`). Every call passes an explicit `today` / `now`; no test reads the clock.

- **T10 Fresh behaviour is unchanged.** Commit `fixtures/trip-evaluation-golden.json`, generated by running the **base-commit** `v2/trip-rules.js` and `v2/trust.js` (`git show c604baf:<path>`) over: every place in `overnight-options.json` and `ridb-options.json`; the three vehicles; the trips `2026-07-10 → 2026-07-12`, `2027-01-15 → 2027-01-17` and `2026-07-10 → 2026-07-18`; `today = "2026-09-26"`; rules applied with `now = 2026-09-26T00:00:00Z`. The test asserts the current code returns the same `status`, `label` and `tripNote` for every row, and `sourceStale === false`. State the generating command in the PR description.
- **T11 Stale restriction outcomes survive.** Synthetic places, one per restriction: stay limit exceeded; `tent_only`; `requires_high_clearance` with `passenger_car`; `requires_high_clearance` with `motorhome`; vehicle-access season outside the trip. For each, with `today` 31 days after `checked_on`, with `checked_on` missing, and with `checked_on` in the future: `status` and `label` equal the fresh result, `tripNote` equals the fresh `tripNote` plus the exact suffix, and `sourceStale === true`.
- **T12 Stale supportive outcomes become unknown.** For a lodging place, a dispersed place and a place inside its vehicle-access season, when stale: label is "Source review is stale", `status` is `"review"`, and `tripNote` does not contain "Within the mapped".
- **T13 Monotonicity on shipped data.** For every row of the T10 matrix, evaluate again with `today = "2027-06-01"` and rules applied at `now = 2027-06-01T00:00:00Z`. Wherever the fresh `status` is `"excluded"`, the stale `status` is `"excluded"`.
- **T14 `applyRules`.** With one matching rule that is (a) stale and (b) missing `last_confirmed_at`: `stay_limit_days` and `requires_high_clearance` are still applied and `ruleReview` is non-null. A place limit of 3 with a rule limit of 5 stays 3. A place with `requires_high_clearance: true` and a rule with `false` or no value stays `true`. A rule with no `stay_limit_days` does not remove the place's limit. End to end: a place with no limits of its own, one stale matching rule (5 days, high clearance), is `excluded` for an 8-night trip and `excluded` for `passenger_car`.
- **T15 Root legacy file.** `require` the root `trip-rules.js` (three directories above the test). Repeat T10 against a second golden set generated from the base-commit root file over every place in the root `overnight-options.json`, with the same vehicles, trips and `today`. Repeat T11 (without the stay-limit case), T12 and T13 against the root function and root inventory. Store the root rows under a separate top-level key in `trip-evaluation-golden.json`.

Existing tests are not modified. `test_published_data.py` and `trust.test.cjs` continue to pass unchanged.

## 9. Acceptance criteria

1. CI shows `python` and `node` passing on the PR.
2. `v2/pipeline/.venv/bin/python v2/pipeline/scripts/00_selftest.py` reports more than 43 tests, all passing. `node --test v2/pipeline/tests/*.test.cjs` reports more than 14 tests, all passing.
3. This prints nothing:
   `git diff --stat main...HEAD -- v2/app.js v2/map-layers.js v2/trail-discovery.js v2/index.html v2/styles.css v2/map-data-v2.json v2/map-data.json v2/trails.geojson v2/overnight-options.json v2/ridb-options.json v2/destinations.json v2/regions/douglas-co/research.json v2/regions/douglas-co/preview.js v2/regions/douglas-co/discovery.js v2/regions/douglas-co/index.html v2/regions/douglas-co/county.css v2/pipeline/config v2/pipeline/scripts/lib/validation.py .github app.js index.html styles.css overnight-options.json destinations.json map-data.json`
4. `git diff --name-only main...HEAD -- v2/pipeline/scripts` prints exactly `v2/pipeline/scripts/08_ingest_leads.py`, `v2/pipeline/scripts/lib/evidence.py`, `v2/pipeline/scripts/lib/region_contract.py`, `v2/pipeline/scripts/lib/rules.py`.
5. `git ls-files 'v2/regions/*/region.json'` prints exactly the two manifests.
6. The number of rule IDs with a negative test equals the number of rules in 5.7 minus R31. The PR description lists each rule ID beside its test name.
7. Every fact-coverage statement in both manifests is byte-identical to section 5.6.
8. Mutation proofs, run locally and **not committed**. For each, paste the failing output naming the rule, then restore the file:
   a. In `research.json`, set one `land` feature's `camping_permission` to `"allowed"` → R27.
   b. In `research.json`, change `source_status.recreation.count` to `35` → R32.
   c. In `map-data-v2.json`, set the fire feature's `status` to `"confirmed"` → R28.
   d. In `map-data-v2.json`, add one feature to `dispersed_corridor_points` → R28 (and `validate_bundle` also fails).
   e. In `v2/regions/douglas-co/region.json`, change `ownership.state` to `"complete"` → R01.
   f. In `trails.geojson`, change one feature's `evidence.source_url` to `https://example.org/` → R24.
9. Both suites complete in under 60 seconds locally, and CI in under three minutes.
10. `grep -rn "RIDB_API_KEY\|apikey" v2/regions/*/region.json` prints nothing.
11. The PR description follows the `AGENTS.md` handoff format and lists: the `fields` chosen for the three empty Aspen layers; the `verification_method` enumeration result; any rule where real data failed as written.
12. `git diff --name-only main...HEAD -- 'v2/*.js' 'v2/*.html' 'v2/*.css'` prints exactly `v2/trip-rules.js` and `v2/trust.js`.
13. Staleness mutation proofs, run locally and **not committed**; paste the failing test names, then restore:
    a. Move the staleness return in `v2/trip-rules.js` back above the tent-only check → T11 and T13 fail.
    b. Restore the `current ? {...} : {}` condition in `Trust.applyRules` → T14 fails.
    c. Make `applyRules` assign the rule's values unconditionally (no most-restrictive merge) → T14 fails.
14. T10 passes against a golden file whose rows were produced by base-commit code, and the PR description shows the command that produced it.
15. `git diff --name-only main...HEAD -- ':(glob)*'` (top-level files only) prints exactly `AGENTS.md` and `trip-rules.js`.
16. Root mutation proof, not committed: move the staleness return in the root `trip-rules.js` back above the tent-only check → T15 fails. Paste the failing test names.
17. The root `trip-rules.js` diff contains no change other than the staleness decision: no stay-limit logic, no reformatting, no renames.
18. (A1) The `08_ingest_leads.py` diff changes only the verification-method argument of the existing `make_evidence` call. The `schema.json` diff changes only `$defs.evidence.properties.verification_method`. `grep -rn "community_report" v2/pipeline/scripts v2/pipeline/schema` prints nothing.
19. (A1) Mutation proofs, not committed: restore `"community_report"` in `08_ingest_leads.py` → T16a and T16f fail; add `"community_report"` to the validator's approved set → T4 (R23) and T16e fail; make the validator accept a non-null method on a community lead → T4 (R28) fails. Paste the failing test names.

## 10. Migration and compatibility

- The contract, manifests and validator are purely additive: no existing file format, schema or data file changes.
- **One runtime behaviour change (5.9).** With current evidence nothing changes (T10). Once a place's review is more than 30 days old, restriction outcomes now persist where they previously collapsed to "Source review is stale". Results gain a `sourceStale` boolean; Neither `v2/app.js` nor the root `app.js` reads it, and neither is changed. The same change applies to the root legacy page.
- Rolling back is reverting the PR. The staleness fix is its own commit and can be reverted alone, but doing so reintroduces N6.
- `schema.json` and `validate_bundle` remain the gate inside `run_pipeline.py`. The region contract is an additional gate that runs in the test suite.
- **A1 compatibility.** No published data file changes: the published `leads` layer is empty, so no shipped feature carries `community_report` or `null`. The `schema.json` change only widens one property to accept `null`; every bundle that validated before still validates. A consumer must treat a `null` method as "none applied"; no browser code reads `verification_method` today.
- **New operational constraint.** A future data refresh that adds a property, a layer or a source URL will fail CI until the manifest is updated in the same PR. This is intended: it forces a human decision about what a new field means. Document it in `v2/pipeline/README.md`.
- The `refresh-map.yml` workflow uploads an artifact and does not run the region contract. The contract runs when the artifact is promoted to `v2/map-data-v2.json` through a PR.
- `contract_version` starts at `1`. A breaking change to the manifest increments it; the validator rejects unknown versions (R01).

Commit structure, in order:

1. `fix: keep known restrictions when evidence is stale`
2. `fix: apply the same staleness rule to the legacy site`
3. `feat: add shared freshness function with cross-language vectors`
4. `feat: add region manifest schema and contract validator`
5. `fix: record no verification method for community leads`
6. `feat: declare Aspen and Douglas County region manifests`
7. `test: validate regions and pin known non-conformance`
8. `docs: make the data contract normative`

## 11. Known risks

- **Real data may fail a rule as written.** The rules were derived from measured data, but not every rule was executed. Section 7 item 3 applies: stop and report.
- **Manifest drift.** The manifest is hand-maintained. T1, T2 and R26 are what keep it honest; do not weaken them.
- **Prefix matching in R24** accepts any URL beneath a declared URL. This is needed for per-facility RIDB URLs and is narrower than host matching, but it is not exact.
- **Reference semantics without a consumer.** The claim object is normative text only until Milestone 3 gives it a browser consumer. Rule 6 is the exception: 5.9 enforces it in the two functions that evaluate places today.
- **Staleness fix is date-sensitive.** All Aspen places go stale on 2026-10-25. If M2 merges after that date, the fix changes live output on merge; before it, the change appears on that date. Either way the direction is more restrictive.
- **Golden fixture integrity.** T10 only proves "unchanged when fresh" if the golden file really came from base-commit code. The reviewer will regenerate it.
- **Remaining restriction-hiding paths.** N16 is not a freshness defect and is not fixed here, in either `v2/` or the root file.
- **Legacy exception creep.** The root change is one function in one file. Any further root edit is out of scope and a review finding.
- **Null as a soft spot.** Allowing `null` could let a producer skip the method to dodge the vocabulary. R28 requires `null` for leads, and rule 16 with R25 and R27 ensures a `null` method can never back `last_verified`, `supported_for_trip` or a confirmed restriction.
- **Bundle schema is permissive.** `schema.json` accepts any non-empty string as a method. The six-string limit is enforced only by the region contract (R23), which runs in the test suite, not inside `run_pipeline.py`.
- **Bundle size in tests.** The 10 MB bundle is parsed by several tests. Cache per path inside `validate_region`.
- **JavaScript and Python date parsing differ.** The vectors restrict inputs to RFC 3339 UTC, date-only and garbage. Other formats are out of contract.
- **Projection.** `lib/geo_utils.py` hard-codes UTM zone 13N. Both current regions are inside it. A region west of 108°W needs a different zone; this contract does not address it.
- **Aspen-only configuration.** `sources.yaml`, `legal_rules.yaml` and `aoi.geojson` are single-region. The manifest references them but does not generalise them.

## Owner decisions (all resolved 2026-10-04)

| # | Decision | Outcome |
|---|---|---|
| D1 | M2 changes no published data. The only browser-code change is the staleness fix in 5.9. Other register items are recorded, not fixed. | Decided. |
| D2 | `max_age_hours` for Aspen context layers is `null`; Douglas keeps the shipped 168. | Approved. |
| D3 | Aspen manifest at `v2/regions/aspen/region.json`; Aspen data stays in `v2/`. | Approved. |
| D4 | `lib/rules.py` adopts the shared `freshness`; a future-dated rule becomes `unavailable`. | Approved. |
| D5 | Manifest wording in 5.6 and the stale suffix in 5.9 are trust-bearing text. | Approved as written. |
| D6 | Root legacy `trip-rules.js` staleness defect. | **Changed by owner: fix in M2**, strictly scoped per 5.9. N16 stays out. |
| D7 | `ridb-options.json` stores a fetch time as `last_confirmed_at` (N3). | Approved as a pinned, deferred violation. |
| D8 | Eighth fact dimension `recreation_permission`. | Approved. |
| D9 | (Revision 4) `verification_method` may be `null`; `community_report` is not added; `08_ingest_leads.py` emits `null`. | Decided by owner. |
| D10 | (Revision 4) One-property change to `schema.json` so a bundle containing a lead still validates. | Architect's necessary consequence of D9. **Approved by owner as implemented, 2026-10-04.** |

## Handoff back to review

Per `AGENTS.md`: what changed; what was deliberately left alone; which checks ran with output; remaining uncertainty. Include the items listed in acceptance criterion 11 and the mutation-proof output from criterion 8.
