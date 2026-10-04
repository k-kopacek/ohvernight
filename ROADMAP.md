# Ohvernight roadmap

This is the canonical Ohvernight milestone roadmap. It is authoritative unless
changed by an approved repository update: a pull request to this file, merged
by the human owner. Chat transcripts, agent memory and Orca session state are
not authoritative; see
[ADR-001](docs/architecture/decisions/ADR-001-repository-is-source-of-truth.md).

Each milestone is implemented from an approved specification in `docs/specs/`.
A roadmap entry states intent and boundaries. The specification, once approved,
states the exact scope.

| Milestone | Title | Status |
|---|---|---|
| M1 | Verification Baseline / Repo Hygiene | **Complete** |
| M2 | Regional Data Contract + Evidence Semantics | **Complete** |
| M3 | Unified Mobile-First Explore Architecture | **Next** |
| M4 | Functional Recreational Water | Planned |
| M5 | Land Classification v1 | Planned |
| M6 | Trails / COTREX | Planned |
| M7 | Camping / Dispersed Camping | Planned |
| M8 | Choose Your Adventure | Planned |

## M1 — Verification Baseline / Repo Hygiene — COMPLETE

Specification: [docs/specs/M1-verification-baseline.md](docs/specs/M1-verification-baseline.md).
Merged in pull request #1.

- Canonical publication path: `v2/map-data-v2.json` is the single tracked,
  app-facing bundle; pipeline output under `v2/pipeline/data/processed/` is
  untracked staging.
- CI/test baseline: offline Python and Node suites and a JavaScript syntax
  check run on every pull request.
- Integrity/provenance safeguards: published-data structure, geometry,
  provenance and registry tests; one ignore file; one workflow location.
- Fire-monitor fallback and regression coverage.
- Orca workflow validation (pull request #2,
  [docs/orca-workflow.md](docs/orca-workflow.md)).
- Human merge gate.

## M2 — Regional Data Contract + Evidence Semantics — COMPLETE

Specification: [docs/specs/M2-regional-data-contract.md](docs/specs/M2-regional-data-contract.md).
Normative contract: [v2/pipeline/docs/data-contract.md](v2/pipeline/docs/data-contract.md).
Merged in pull request #3.

- One manifest per region (`v2/regions/<id>/region.json`).
- Explicit evidence, freshness and provenance semantics.
- Unknown remains unknown.
- Ownership, public access, camping permission and recreation permission are
  separate dimensions.
- Validator with stable rule IDs (R01–R50).
- Freshness parity across Python and JavaScript, pinned by shared vectors.
- Staleness must never weaken a known restriction; the ordering defect was
  fixed at runtime in `v2/` and in the root legacy site.
- Aspen and Douglas County manifests.
- Pinned non-conformance register (N1–N18).

## M3 — Unified Mobile-First Explore Architecture — NEXT

- Unify the Aspen and Douglas County app structure.
- Fix mobile map real-estate problems.
- Resolve land styling and evidence presentation (register item N17).
- Address the deferred rule-ordering defects that are not freshness-related
  (register item N16).
- Evaluate optimized Leaflet with lazy GeoJSON against a MapLibre/vector
  architecture.
- **Do not pre-commit to MapLibre before this milestone.** The rendering
  architecture is an open decision that M3 makes; until then the app is
  Leaflet and no document should present another choice as settled.

## M4 — Functional Recreational Water

- Distinguish useful lakes, reservoirs, rivers and streams from generic
  hydrology clutter.
- Support fishing, paddling, swimming and general-recreation relevance.
- Preserve access and permission uncertainty.
- Names alone are not evidence of recreational usefulness.
- Hermes joins the agent stack in a research/operations role beginning with
  this milestone
  ([ADR-004](docs/architecture/decisions/ADR-004-hermes-research-operations-role.md)).

## M5 — Land Classification v1

- Authoritative federal, state, local, private and public classification where
  the source supports it.
- Non-federal is not private.
- Ownership is not access.
- Confidence, provenance and spatial precision remain explicit.
- Unknown remains unknown.

## M6 — Trails / COTREX

- COTREX for Colorado, **subject to licensing/terms verification**. No COTREX
  content is in the repository today; see
  [v2/pipeline/TRAIL-PILOT.md](v2/pipeline/TRAIL-PILOT.md).
- Hiking, mountain biking, OHV/dirt bike, equestrian and other activities.
- Equivalent authoritative sources elsewhere.
- Access, closure and current-condition claims remain evidence-backed.

## M7 — Camping / Dispersed Camping

- Developed campgrounds.
- Dispersed and public-land camping.
- Restrictions, closures, access, and vehicle/setup suitability.
- Eliminate inappropriate hard-coded camping-rule behavior.
- No inferred camping permission.

## M8 — Choose Your Adventure

- Inputs: state/location, dates, activities, camping/lodging preferences, and
  vehicle/access constraints where relevant.
- Output: ranked adventure options based on verified evidence.
- Explore Map remains the free-discovery alternative.

## Constraints that apply to every milestone

- [Trust principles](docs/product/trust-principles.md) and the
  [regional data contract](v2/pipeline/docs/data-contract.md).
- [Product principles](docs/product/product-principles.md).
- [Agent stack and workflow](docs/architecture/agent-stack.md), including
  human-only merge authority.

## Relationship to `v2/ROADMAP.md`

[v2/ROADMAP.md](v2/ROADMAP.md) is the September 2026 execution queue from
before the milestone structure existed. It is kept as a historical working
log. Where it differs from this file on ordering or scope, this file governs.
