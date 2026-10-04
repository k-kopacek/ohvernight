# Architecture audit — reconstructed durable record

**This is not a verbatim copy of the original audit.** The original
architecture audit was written outside the repository and was not preserved
(see the M2 specification, section 1). This record is reconstructed from what
the repository does preserve:

- the findings the owner restated on 2026-10-04, recorded as A1–A12 in
  [docs/specs/M2-regional-data-contract.md](../specs/M2-regional-data-contract.md);
- the verified facts F1–F11 in the same specification;
- the background facts and out-of-scope list in
  [docs/specs/M1-verification-baseline.md](../specs/M1-verification-baseline.md);
- the non-conformance register N1–N18 in
  [v2/pipeline/docs/data-contract.md](../../v2/pipeline/docs/data-contract.md);
- the owner's summary of the audit supplied when this record was created.

Where the original wording, dates or measurements are not preserved, this
record does not supply them. Its purpose is to keep the findings and their
disposition from depending on any chat or agent memory.

Status key: **Fixed** (resolved in M1 or M2), **Pinned** (recorded in the
non-conformance register and held by a test or declaration, not repaired),
**Deferred** (owned by a future milestone).

## Findings

### 1. Architecture as found

The product was a static site published by GitHub Pages from `main`, with a
Leaflet map, JSON/GeoJSON data files and an offline Python pipeline. No
backend. This remains the architecture; see
[system-overview.md](../architecture/system-overview.md). It is context, not
a defect.

### 2. Region format and UI divergence — partly fixed, partly deferred

Aspen and Douglas County each invented their own data shape and their own app.
Aspen data was spread over six files with three envelopes; Douglas was one
file with a fourth. Transport status had four shapes. Freshness was
implemented four times with different thresholds and edge behaviour.

- **Fixed (M2):** one manifest per region, one contract, one validator, and
  Python/JavaScript freshness parity pinned by shared vectors.
- **Deferred (M3):** the two apps are still separate, no browser code reads
  the manifests, and there is no region selection.
- **Pinned:** legacy transport shapes (N2); hard-coded 7- and 30-day
  thresholds (N9).

### 3. Publication-path mismatch — fixed (M1)

The map bundle existed as two tracked, byte-identical copies: the pipeline's
processed output and the app-facing file. Workflow definitions were duplicated
in locations GitHub does not read, and no CI ran on pull requests. M1 made
`v2/map-data-v2.json` the single tracked, canonical app-facing bundle, made
pipeline output untracked staging, consolidated workflows under
`.github/workflows/`, added CI, and added a fire-monitor fallback from the old
staging baseline to the canonical bundle with a regression test.

### 4. Land misclassification risk; non-federal must not become private — rule fixed, classification deferred

Limited-scale managing-agency polygons could be read as ownership findings,
and land outside a federal polygon could be read as private.

- **Fixed (M2):** the contract states that non-federal is not private and
  that ownership is not access; there is no `ownership` layer kind; validator
  rule R28 requires a `private` value to be backed by the source's own
  classification code.
- **Pinned:** the Aspen layer key `land_ownership` still says ownership (N5);
  `evidence.confidence` differs across regions for the same source (N4).
- **Deferred (M5):** authoritative land classification.

### 5. Public/private/management styling risk — pinned, deferred (M3)

Both apps draw generalized polygons as crisp boundaries, and the Douglas page
fills them with a distinct colour per manager code, including `PVT`. Styling
implies certainty the data does not have. M2 added the `spatial_precision`
declaration a UI needs and the rule that presentation must not exceed the
evidence; it did not change styling. Recorded as N17. Owned by M3.

### 6. Staleness ordering could hide stronger restrictions — fixed (M2)

A stale source review returned "Source review is stale" before the tent-only,
high-clearance and vehicle-access-season checks ran, and stale rules were not
applied to places. An exclusion could therefore decay into a softer "review"
result as evidence aged. Fixed at runtime in `v2/trip-rules.js`,
`v2/trust.js` and the root `trip-rules.js`. Kept in the register as
regression markers N6 and N15.

- **Deferred (M3):** two orderings unrelated to freshness can still hide a
  restriction (N16).

### 7. Retrieval conflated with confirmation — rule fixed, one instance pinned

Some paths treated a successful fetch as a confirmation. The contract now
states that a fetch advances only checked and retrieved timestamps.

- **Pinned:** `ridb-options.json` stores a fetch time as `last_confirmed_at`
  and `Trust.sourceSummary` reads it (N3). The validator ignores it. Fixing
  the producer, data file and reader is deferred by owner decision D7.

### 8. Missing fetch-status and provenance for some sources — pinned

Aspen trails and Douglas trails and roads have no transport record, so a
failed refresh of them is invisible (N1, N12). The validator reports these
layers rather than failing, and a test pins the exact set so it cannot grow.
Per-record source URLs in place lists are not checked against declared
sources (N11). Not assigned to a specific roadmap milestone beyond the
register's notes.

### 9. Water: name-based filtering and insufficient recreation semantics — pinned, deferred (M4)

Water display selects features by the presence of a name. Feature type, flow
permanence and size are dropped at ingest in both regions. A name is not
evidence of recreational usefulness, access or flow. M2 added the
`recreation_permission` dimension and the layer limitations; it did not
reprocess water. Recorded as N18. Owned by M4.

### 10. Aspen payload size and repeated provenance — pinned, unassigned

The Aspen bundle is about 10 MB and repeats the `evidence` object on every
feature. M2 deliberately changed no payload but kept the door open: the
manifest `sources` are the authoritative provenance declaration, so a later
change can replace repeated evidence with a reference without changing
evidence semantics. Recorded as N14. Payload optimisation must not be used as
a reason to alter evidence semantics. Relevant to the M3 rendering evaluation.

### 11. Fail-closed behaviour for trust-sensitive claims — fixed as a rule (M2)

Missing evidence must fail closed for positive claims. The contract requires a
complete claim object or reviewed record for any value asserting permission,
access, openness or support, and the validator rejects the positive value
otherwise (R27, R28, R41). The claim object has no browser consumer yet.

### 12. A mapped feature is not permission — fixed as a rule (M2)

A mapped road, trail, facility or water feature, or proximity to public land,
does not establish access or permission. Stated in the contract and in each
manifest's fact-coverage statements.

### 13. COTREX integration — deferred (M6), subject to licensing/terms

COTREX was not integrated. The trail pilot recorded that the COTREX app terms
restrict copying and distribution without separate written permission, and
that public GIS mirrors described 2019 trail content
([v2/pipeline/TRAIL-PILOT.md](../../v2/pipeline/TRAIL-PILOT.md)). No COTREX
content is in the repository. Integration depends on verified licensing and
terms.

### 14. MapLibre — deferred to M3, not assumed

Whether to keep Leaflet with optimized, lazily loaded GeoJSON or move to a
MapLibre/vector architecture is undecided. M3 evaluates it. Until then the
app is Leaflet and no document should treat MapLibre as chosen.

## Disposition summary

| Finding | Fixed in | Pinned as | Future owner |
|---|---|---|---|
| Publication-path mismatch, no CI | M1 | — | — |
| Region data-shape divergence | M2 | N2, N9 | M3 (app unification) |
| Non-federal is not private; ownership is not access | M2 (rule) | N4, N5 | M5 |
| Land styling implies certainty | — | N17 | M3 |
| Staleness hides restrictions | M2 | N6, N15 (markers) | — |
| Non-freshness rule ordering | — | N16 | M3 |
| Retrieval read as confirmation | M2 (rule) | N3 | unassigned (decision D7) |
| Missing fetch status / provenance | — | N1, N11, N12 | unassigned |
| Water semantics | M2 (dimension only) | N18 | M4 |
| Payload size, repeated provenance | — | N14 | unassigned; relevant to M3 |
| Fail-closed positive claims | M2 | — | — |
| Hard-coded camping listing and thresholds | — | N7, N9 | M3 per register; M7 per roadmap |
| COTREX | — | — | M6, subject to terms |
| Map rendering architecture | — | — | M3 decision |

## Known gaps in this record

- The original audit document, its date and its author are not in the
  repository.
- The register assigns N7, N9, N11, N13 and N14 to "Milestone 3"; the roadmap
  places camping-rule cleanup in M7. The M3 specification should state which
  register items it actually retires.
