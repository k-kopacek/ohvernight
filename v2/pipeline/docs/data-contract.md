# Ohvernight regional data contract

This is the normative contract for regional research data. A manifest at
`v2/regions/<region_id>/region.json` declares coverage, sources, layers,
transport-status locations, freshness policy, and facts that remain unknown.
The validator in `scripts/lib/region_contract.py` enforces computable rules;
browser consumers must preserve the same semantics.

## Regional manifest

Every manifest has `contract_version: 1`, a `research_only` region status, one
coverage declaration, declared sources, layers, eight fact-coverage dimensions,
and non-empty `known_gaps`. Paths are relative to `v2/`, use `/`, contain no
`..` segment, and never begin with `/`. A coverage statement must say that the
boundary is not a land-ownership or access boundary. A feature-collection
layer declares geometry types, null-geometry policy, spatial precision, field
provenance, and limitations. A place-list declares its list key.

The eight fact dimensions are `ownership`, `public_access`,
`camping_permission`, `closures`, `restrictions`, `road_access`,
`trail_access`, and `recreation_permission`. Their only states are `none`,
`context`, and `reviewed_partial`; there is no `complete`, `verified`, `open`,
or `permitted` state. `context` requires a non-empty layer list.
`reviewed_partial` requires a rules registry or a reviewed-sites record.

## Evidence semantics

These concepts are distinct and one never implies another:

| Concept | Question | Values / carrier |
|---|---|---|
| Existence | Does a source list this feature or facility? | record presence |
| Provenance | Where did the record come from and when was it copied? | feature evidence and manifest source |
| Transport | Did the last retrieval attempt work? | `available`, `unavailable`, `skipped` |
| Interpretation | What does a reviewed source say about one fact? | `unknown`, `supported`, `restricted` claim |
| Verification | Did a person review that interpretation, how, and when? | claim/rule/evidence fields |
| Freshness | Is that verification within policy? | computed `current`, `stale`, `unavailable` |

Unknown is the default. A successful fetch advances a checked/retrieved time,
not a confirmation time. Retrieval date is not content date. A page hash never
confirms a fire stage. Freshness thresholds are product policy held in data;
the browser recomputes age and must not reset a confirmation date when another
layer refreshes.

`evidence.confidence` is deprecated and retained only for schema compatibility.
Consumers must not display it, branch on it, or treat it as confidence in
ownership, access, or permission. `last_verified` may be non-null only with
`verification_method: "manual_claim_review"`.

Freshness never weakens a restriction. A stale or never-confirmed supported
claim becomes unknown; a stale restricted claim, exclusion, limit, or caution
remains in force and is additionally flagged for review. Positive claims fail
closed. A mapped road, trail, facility, water feature, nearby public land, or
straight-line proximity does not establish legal access, camping permission,
road access, trail access, or recreational permission.

Approved verification methods are exactly:
`arcgis_rest_query`, `source_fetch`, `rest_api`, `html_change_monitor`,
`derived_intersection`, and `manual_claim_review`. `null` means no method has
been applied; it is not verification. In a `community_leads` layer the method
must be null, while report origin remains in `source_url`, `agency`, and, for
leads, `reported_at`. No `community_report` method exists.

Reserved feature properties are `id`, `name`, `site_type`, `evidence`,
`camping_permission`, `access_status`, `access_reason`, `road_conditions`,
`land_class`, `needs_review`, `actual_site_confirmed`, `evaluated_trip`,
`status`, `stage`, `type`, `last_checked_at`, `last_confirmed_at`,
`max_age_hours`, `tent_only`, `requires_high_clearance`, `stay_limit_days`,
and `max_stay_days`. They are never listed under `fields`. Camping permission
is `unknown`, except for a fully reviewed site with an evaluated trip and
manual claim review. `access_status` is unknown unless its trip, reason, and
unknown road conditions are present. `land_class` and `road_conditions` remain
unknown.

Generated polygons remain `needs_review: true`,
`camping_permission: "unknown"`, and never create point campsites. MVUM and
candidate snapshots are tied to their evaluated trip. Do not infer Private
from a non-federal or unshaded area: a Private/PVT value is only the source's
generalized classification. Ownership and access are separate dimensions.

## Transport records and legacy aliases

Canonical transport records use `status`, `last_checked_at`, and
`last_retrieved_at`. `available` requires a retrieval timestamp;
`unavailable` and `skipped` require a reason. A non-available record retaining
features must say `retained_previous: true`. Transport records never contain a
confirmation timestamp. The validator normalizes and reports these aliases:

| Legacy field/value | Normalized to |
|---|---|
| `completed_at` | `last_retrieved_at` and `last_checked_at` |
| `retrieved_at` | `last_retrieved_at` |
| `checked_at` | `last_checked_at` |
| `status: "failed"` | `unavailable` |
| `error` | `reason` |
| `available` without retrieval field | retrieval inferred from checked time |
| `last_confirmed_at` on transport | ignored and reported; never confirmation |

`config/rules-registry.json` stores independently reviewed site exceptions.
Matching exact place IDs or reviewed road names adds context only and never
grants permission. Do not inherit a forest-wide 14-day limit. The Lincoln
Creek published day limit does not establish a precise check-in/check-out
counting policy.

## Validator rules

Every failure is a `ContractError` with a stable rule ID. R31 is a report,
not a failure, because missing transport records are pinned
non-conformances.

| ID | Requirement |
|---|---|
| R01 | Manifest matches the manifest schema and conditional contract. |
| R02 | Manifest region ID matches its directory. |
| R03 | Referenced paths are safe and exist under `v2/`. |
| R04 | Layer/source IDs are unique and declared sources are used. |
| R05 | Fact coverage references declared layers and obeys state requirements. |
| R10 | Coverage is a valid non-empty WGS84 Polygon/MultiPolygon feature. |
| R20 | Feature collections have the required envelope. |
| R21 | Feature IDs are non-empty and unique across a region. |
| R22 | Geometry is valid, declared, in bounds, and null only when allowed. |
| R23 | Evidence provenance and verification method are present and valid. |
| R24 | Agency/derived evidence URLs are declared with safe prefix rules. |
| R25 | `last_verified` requires manual claim review. |
| R26 | Feature fields are declared and reserved names stay out of `fields`. |
| R27 | Reserved properties fail closed for positive permission/access claims. |
| R28 | Kind-specific safety rules hold for candidates, leads, monitors, and land. |
| R29 | Trail activities match the producer vocabulary and record shape. |
| R30 | Transport status, timestamps, and reasons are valid after aliasing. |
| R31 | Missing non-curated transport status is reported in the report. |
| R32 | Transport count equals the layer feature count. |
| R33 | Unavailable data with features records retained previous data. |
| R40 | Place-list IDs and coordinates are valid and unique. |
| R41 | Place-list camping and claim objects fail closed. |
| R50 | Rules registry records contain required review evidence. |

## Known non-conformance register

M2 records these known violations rather than silently repairing them. N6 and
N15 are fixed runtime regressions, retained as regression markers.

| ID | Non-conformance | Pinned by |
|---|---|---|
| N1 | No transport record: Aspen `trails`; Douglas `trails`, `roads`. | T5 |
| N2 | Legacy transport aliases remain in the snapshots. | T5 |
| N3 | RIDB uses `last_confirmed_at` for a fetch time; validator ignores it. | T5 |
| N4 | `evidence.confidence` differs for the same source across regions. | T7 |
| N5 | Aspen `land_ownership` is limited-scale management context. | R28 |
| N6 | Staleness ordering hid restrictions; fixed in M2. | T10–T14 |
| N7 | Rampart designated-dispersed listing is hard-coded in `preview.js`. | Milestone 3 |
| N8 | Aspen MVUM carries past-trip `designated_open` values. | R27 |
| N9 | 7- and 30-day thresholds remain hard-coded in browser code. | Milestone 3 |
| N10 | Douglas operational attributes may be historical. | Manifest fields |
| N11 | Place-list source URLs are not checked against declared sources. | Milestone 3 |
| N12 | Douglas snapshot predates current fetch status for roads/trails. | T5 |
| N13 | Legacy `v2/map-data.json` is outside the region manifests. | Milestone 3 |
| N14 | Per-feature evidence is duplicated for payload compatibility. | Milestone 3 |
| N15 | Root legacy staleness ordering hid restrictions; fixed in M2. | T15 |
| N16 | Two unrelated rule orderings can still hide a restriction. | Deferred |
| N17 | Land styling exceeds generalized evidence. | Milestone 3 |
| N18 | Water display lacks recreational-use semantics. | Manifest limitations |

The BLM native polygon conversion preserves ring holes and islands using
even/odd filling and repairs invalid topology with Shapely. That source is
generalized management context; county parcel precision and campsite legality
cannot be inferred from the repair.

All checks are offline, resolve paths from the caller, do not read the clock,
and never change published data. A future refresh that adds a layer, source,
or property must update the region manifest in the same pull request; CI
enforces that decision point.
