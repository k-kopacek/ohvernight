PROPOSAL - FOR OWNER REVIEW, NOT APPROVED

# M6 source policy and roadmap wording proposal

Repository behavior below was checked against `origin/main` at `bb85785ea98c8d5fb8d5694a36744b4f96a6161a`. This is a proposal only; it does not change `ROADMAP.md`, the pipeline, a contract, or data. The Rampart evidence references point to unreviewed drafts proposed for archive by docs PR #23 at `docs/research/overnight-2026-10-08/`; the bounded MVUM technical audit is Package 4 research at `research-overnight/docs/research/m6-trails/mvum-technical-feasibility.md` and is not product truth.

## 1. Proposed normative source policy

Ohvernight obtains trail and recreation data from the authoritative upstream agency publishers and normalizes those records into its evidence model. It does not ingest through an aggregation product. COTREX is not a production data dependency under the terms reviewed; it may appear only as an external user link labelled as an external resource, never as Ohvernight's evidence source.

For each question, prefer the agency responsible for that specific legal or management decision. A source is authoritative only within its stated scope: the Forest Service Motor Vehicle Use Map (MVUM) for designated motorized use on National Forest System roads and trails; Forest Service recreation pages for facility information; and the county for county fire restrictions. Legal-use dates mean only the legal designations the source defines; they do not establish physical rideability or current openness. Management-intent attributes are not permission. When sources conflict, preserve the readings side by side with provenance and scope; do not collapse them into a verdict.

Source-feature identity is not user-facing trail identity. A geometry segment is not necessarily a whole trail, and trail segments are never merged on name, touching geometry, or shared agency alone. Preserve source records and make any user-facing grouping evidence-backed, explicit, and reversible.

## 2. Alternative exact M6 roadmap sections

Each block below is a complete replacement for the existing `## M6` section on `main`, through the line before `## M7`. All retain the current M6 scope and the October 8 product-alignment acceptance expectations. No milestone order or status is proposed to change.

### Alternative A — recommended: Trails / Authoritative Agency Sources

Recommended because it describes the source strategy without narrowing M6 to motorized use or implying that a single source covers every activity.

```markdown
## M6 — Trails / Authoritative Agency Sources

- Ingest trail and recreation data from authoritative upstream agency publishers; do not ingest through an aggregation product. COTREX is not a production data dependency under the terms reviewed; it may appear only as an external user link labelled as an external resource, never as Ohvernight's evidence source.
- Hiking, mountain biking, OHV/dirt bike, equestrian and other activities.
- Prefer the agency responsible for each specific legal or management decision; use each source only within its scope. Access, closure and current-condition claims remain evidence-backed. Legal-use dates are source-defined designations, not rideability or current openness; management intent is not permission. Conflicting sources stay side by side, not collapsed into a verdict.
- Equivalent authoritative sources elsewhere.
- User-facing trail identity (owner requirement recorded at the close of M3, 2026-10-06). Source geometry and feature identity are not necessarily the trail a user has in mind: in cases such as Difficult Creek, several connected source features make up what a user would reasonably call one trail. M6 evaluates connected source segments with the same or a similar name; overlapping or duplicate geometries; segment versus route identity; source jurisdiction boundaries; cross-source reconciliation; and grouping several canonical segments into one user-facing trail where evidence supports it. Canonical source records stay preserved. Trail features are not merged or renamed on geometric continuity or matching names alone.
- Product-alignment acceptance expectations (added 2026-10-08): allowed activities and motorized restrictions as claims or unknown; trailhead and staging identity where a source provides it; approach and access relationships that are source-backed, reviewed or unknown, never inferred from distance; restriction evidence coverage (concept only; shape set by that milestone's specification); source reconciliation; and trail identity that survives a jurisdiction or region-package boundary.
```

### Alternative B — Trails / Motorized & Recreation Access

```markdown
## M6 — Trails / Motorized & Recreation Access

- Ingest trail and recreation data from authoritative upstream agency publishers; do not ingest through an aggregation product. COTREX is not a production data dependency under the terms reviewed; it may appear only as an external user link labelled as an external resource, never as Ohvernight's evidence source.
- Hiking, mountain biking, OHV/dirt bike, equestrian and other activities.
- Prefer the agency responsible for each specific legal or management decision; use each source only within its scope. Access, closure and current-condition claims remain evidence-backed. Legal-use dates are source-defined designations, not rideability or current openness; management intent is not permission. Conflicting sources stay side by side, not collapsed into a verdict.
- Equivalent authoritative sources elsewhere.
- User-facing trail identity (owner requirement recorded at the close of M3, 2026-10-06). Source geometry and feature identity are not necessarily the trail a user has in mind: in cases such as Difficult Creek, several connected source features make up what a user would reasonably call one trail. M6 evaluates connected source segments with the same or a similar name; overlapping or duplicate geometries; segment versus route identity; source jurisdiction boundaries; cross-source reconciliation; and grouping several canonical segments into one user-facing trail where evidence supports it. Canonical source records stay preserved. Trail features are not merged or renamed on geometric continuity or matching names alone.
- Product-alignment acceptance expectations (added 2026-10-08): allowed activities and motorized restrictions as claims or unknown; trailhead and staging identity where a source provides it; approach and access relationships that are source-backed, reviewed or unknown, never inferred from distance; restriction evidence coverage (concept only; shape set by that milestone's specification); source reconciliation; and trail identity that survives a jurisdiction or region-package boundary.
```

### Alternative C — Trails / Trail Identity & Access Evidence

```markdown
## M6 — Trails / Trail Identity & Access Evidence

- Ingest trail and recreation data from authoritative upstream agency publishers; do not ingest through an aggregation product. COTREX is not a production data dependency under the terms reviewed; it may appear only as an external user link labelled as an external resource, never as Ohvernight's evidence source.
- Hiking, mountain biking, OHV/dirt bike, equestrian and other activities.
- Prefer the agency responsible for each specific legal or management decision; use each source only within its scope. Access, closure and current-condition claims remain evidence-backed. Legal-use dates are source-defined designations, not rideability or current openness; management intent is not permission. Conflicting sources stay side by side, not collapsed into a verdict.
- Equivalent authoritative sources elsewhere.
- User-facing trail identity (owner requirement recorded at the close of M3, 2026-10-06). Source geometry and feature identity are not necessarily the trail a user has in mind: in cases such as Difficult Creek, several connected source features make up what a user would reasonably call one trail. M6 evaluates connected source segments with the same or a similar name; overlapping or duplicate geometries; segment versus route identity; source jurisdiction boundaries; cross-source reconciliation; and grouping several canonical segments into one user-facing trail where evidence supports it. Canonical source records stay preserved. Trail features are not merged or renamed on geometric continuity or matching names alone.
- Product-alignment acceptance expectations (added 2026-10-08): allowed activities and motorized restrictions as claims or unknown; trailhead and staging identity where a source provides it; approach and access relationships that are source-backed, reviewed or unknown, never inferred from distance; restriction evidence coverage (concept only; shape set by that milestone's specification); source reconciliation; and trail identity that survives a jurisdiction or region-package boundary.
```

## 3. Model concepts, existing architecture, and candidate sources

`docs/architecture/adventure-model.md` is a conceptual model on `main`, not an approved M6 data schema. Its M6 row (section 5) requires user-facing trail identity with a preserved member map, activity use as claims or unknown, trailhead/staging identities where sourced, source-backed/reviewed-candidate/unknown `starts_at` and `approached_via` relationships, restriction/closure links with evidence coverage, and identity across jurisdiction/package boundaries. Section 3 says proximity alone establishes no relationship; section 4 says coverage does not create permission and must be scoped and dated. Candidate sources below are scoped evidence inputs, not proof that a future join is valid.

| Concept M6 must preserve | Adventure-model reference | Candidate source and Rampart evidence |
|---|---|---|
| Source feature identity | Section 2, activity feature; section 3 stable IDs | Preserve each source namespace, layer, and feature key. Package 4 found distinct MVUM `OBJECTID`/`GLOBALID`/route-label fields and no direct join from MVUM route labels to canonical `usfs-trail-<objectid>` IDs. See Package 4 audit and archive drafts `rampart-relationships.md`, `rampart-m6-m7-source-implications.md`. |
| User-facing trail identity | Section 2, activity feature; section 5 M6 member map | Forest Service Trail NFS Publish names/numbers and reviewed trail-system evidence may inform a grouping; MVUM `ID` is a route-number label, not a trail identity. The archive's `rampart-relationships.md` reports examples where the Trail NFS layer has names/numbers while MVUM trail `name` is null. |
| Geometry segment identity | Section 2 activity feature and section 3 relationship endpoints | Retain source geometry and each feature's own ID; use the relevant source publisher's trail layer and MVUM geometry as separate records. `rampart-m6-m7-source-implications.md` reports multiple distinct geometries per number and divergent source representations. |
| Trail system / recreation-area identity | Sections 2–3 entity/jurisdiction concepts; no dedicated trail-system entity is defined | Forest Service recreation-area pages and published MVUM map may identify the area and designated routes; structured trail-to-area membership was not found in Package 4 or the Rampart drafts. Treat as an open model/source gap, not a spatial-containment join. See `rampart-official-facts.md`, `rampart-relationships.md`, and `rampart-weekend-plan-and-gaps.md`. |
| Trailhead / staging identity | Section 2 trailhead or staging entity; section 3 `starts_at` / `accessed_from` | Forest Service recreation-site records/pages supply site records; explicit agency page language can support a named trailhead link for that trail. The drafts report Cabin Ridge Trailhead page naming Trail #675, while many relationships remain absent. See `rampart-relationships.md`, `rampart-weekend-facilities.md`, `rampart-weekend-ride-options.md`. |
| Governing agency | Section 2 agency/operator/jurisdiction; section 3 `governed_by` | Use a source record's own managing-organization/jurisdiction fields where populated; evidence publisher is provenance, not necessarily the governing agency. Package 4 found MVUM fields for forest, district, admin organization; see audit field inventory and `rampart-m6-m7-source-implications.md`. |
| Activity claims | Section 5 M6 and section 5 M8 activity permission; section 4 coverage | MVUM published map for designated motorized use within map scope; structured MVUM layers can carry separate vehicle class/date values but must be reconciled to the map. Existing Trail NFS use strings are management-intent evidence and remain separate. See `rampart-evidence-closure.md`, `rampart-weekend-legality-links-orders.md`, and `trail-date-semantics-research.md`. |
| Motorcycle / ATV / full-size vehicle rules | Sections 3 `associated_with` constraint and `constrained_by`; section 4 motorized-use coverage | MVUM trail/road class fields and official MVUM map/table; Forest Service recreation text for requirements such as a current plate and valid driver's license on roads. Package 4 found distinct motorcycle, ATV, passenger, high-clearance, and width-class fields; plated status is not a structured field. See `rampart-m6-m7-source-implications.md` and `rampart-weekend-ride-options.md`. |
| Seasonal restrictions | Sections 3 `constrained_by`; section 4 seasonal-closure coverage and aging | MVUM map's seasonal/special designation and its date table; structured `_datesopen` fields are strings that can have two comma-separated windows. The Rampart drafts report conflicts between the map table and service fields for some trails; preserve both with source scope. Forest orders supply separate scoped closures. See `rampart-evidence-closure.md`, `rampart-weekend-route-and-conditions.md`. |
| Route relationships | Section 3 `starts_at`, `approached_via`; section 4 access coverage | Agency directions, MVUM designations and official trailhead pages can supply source-backed links; geometry/network topology can only nominate a reviewed candidate. `rampart-relationships.md` and `rampart-weekend-facilities.md` distinguish explicit links from proximity/derived observations. |
| Evidence | Sections 3 and 5 provenance/verification; section 4 coverage | Retain source URL, publisher, retrieval time, reviewed source/version, scope and applicable dates. Package 4 found no per-feature edit date in the three sampled layers; see its update-field analysis and `trail-date-semantics-technical-audit.md`. |
| Freshness | Section 4 coverage aging; section 5 M8 freshness | Record retrieval time separately from review time and source edit time. Package 4 found no per-feature edit timestamp in the sampled MVUM/NFS Roads schemas; publisher cadence statements do not establish feature-level freshness. See Package 4 audit and `rampart-m6-m7-source-implications.md`. |
| Evidence coverage | Section 4; section 5 M6 requires restriction/closure coverage | Track what was checked by subject, category, jurisdiction/source and review date. MVUM retrieval alone is not a human review and does not establish all-order/current-condition coverage. See `rampart-weekend-plan-and-gaps.md` and `rampart-weekend-route-and-conditions.md`. |

### Package 4 findings used here (bounded sample only)

The technical audit identified MVUM roads (layer 1) and trails (layer 2) plus National Forest System Roads in Forest Service EDW on the existing `apps.fs.usda.gov` host. It made nine bounded requests; the samples contained 25 MVUM trail, 17 MVUM road, and 17 NFS Roads records. In the trail sample, MVUM route labels matched held `trail_number` values exactly for 2/25 and after zero-padding normalization for 14/25; 11/25 remained unmatched. A route label is therefore only a candidate crosswalk: it does not establish source-feature identity, geometry equality, route membership, or user-facing identity. The sampled MVUM/NFS Roads `RTE_CN` values matched 17/17, but this sample does not prove a global one-to-one join.

The samples carry separate per-class fields and raw date strings, including comma-separated two-window seasons; the map's table and the service fields are separate representations. No per-feature update timestamp was present in the returned layer metadata/fields. These observations are feasibility evidence only and do not establish legal interpretation or a production source design.

## 4. Rampart Range model-validation questions

The sources listed are evidence candidates named in the archive drafts, not a statement that the research is current or complete. The Package 4 sample is small and spatially bounded.

| Question | Candidate source that can answer, or gap |
|---|---|
| What is the recreation area? | Forest Service Rampart Range Recreation Area page (`rampart-official-facts.md`); official descriptive prose. No structured recreation-area identity or extent was identified in the drafts. |
| Which trails belong to it? | Published MVUM map and Forest Service trail records can identify/designate routes; `rampart-relationships.md` and `rampart-weekend-plan-and-gaps.md` do not establish a complete structured area-membership source. No structured source for complete membership. |
| Which trails allow motorcycles? | Published South Platte MVUM Seasonal and Special Vehicle Designations table plus service fields, kept side by side; the drafts record conflicts on some routes (`rampart-evidence-closure.md`, `rampart-weekend-legality-links-orders.md`). |
| Which trails allow ATVs? | Published MVUM table's vehicle designation and MVUM `atv` / `atv_datesopen` fields. Preserve any map/service disagreement; no cross-source verdict is assumed. |
| What are the width limits? | Published MVUM route legend/table and class-specific MVUM width fields (`*_lt50inches`, `*_gt50inches`); sample does not supply a generic measured width for a rider's vehicle. |
| What are the seasonal legal-use dates? | Published MVUM table and map legend, with EDW MVUM date fields retained separately. The Rampart drafts report disagreement for some routes; no Ohvernight resolution is proposed. |
| Which trailheads or staging areas serve them? | Forest Service recreation-site pages/directions where they explicitly name a route (for example Cabin Ridge Trailhead to Trail #675, per `rampart-weekend-ride-options.md`). No complete structured trailhead-to-trail relationship source. |
| Which roads require plated vehicles? | Forest Service recreation-area page text states the plate/driver-license requirement on roads; MVUM provides route/vehicle designations. No structured “plated vehicle required” attribute was found in Package 4 samples. |
| What current orders apply? | Signed Forest Service orders and current agency alerts for the order's named scope; the archive's `rampart-weekend-route-and-conditions.md` records that status was time-sensitive and not fully resolved. No structured source for complete current-order applicability. |

## 5. Open owner questions

1. Confirm Alternative A, B, or C, including whether the title should foreground agency sourcing, motorized access, or trail identity.
2. Confirm the stated COTREX posture for roadmap text: no production data dependency and an external user link only under the reviewed terms.
3. For conflicts between the published MVUM and its feature service, which reviewed evidence process and display treatment should a future M6 specification require? This proposal requires preservation without a verdict but does not define adjudication.
4. Which agency-published sources, if any, are approved for structured trail-system membership, complete trailhead/staging links, and plated-road requirements when no structured fields exist?
5. What source-level and human-review freshness periods should M6 specify for MVUM designations, trail records, and orders? Package 4 found no per-feature edit timestamps.
6. Which additional agencies, states, and activity classes are in the first M6 implementation scope, beyond the existing roadmap's activities and equivalent authoritative sources elsewhere?
