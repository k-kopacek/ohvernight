# Ohvernight roadmap

This is the canonical Ohvernight milestone roadmap. It is authoritative unless
changed by an approved repository update: a pull request to this file,
approved by the human owner. Chat transcripts, agent memory and Orca session
state are not authoritative; see
[ADR-001](docs/architecture/decisions/ADR-001-repository-is-source-of-truth.md).

Each milestone is implemented from an approved specification in `docs/specs/`.
A roadmap entry states intent and boundaries. The specification, once approved,
states the exact scope.

| Milestone | Title | Status |
|---|---|---|
| M1 | Verification Baseline / Repo Hygiene | **Complete** |
| M2 | Regional Data Contract + Evidence Semantics | **Complete** |
| M3 | Unified Mobile-First Explore Architecture | **In progress — A11 implemented; performance disposition, second real-device pass and merge approval owed** |
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

## M3 — Unified Mobile-First Explore Architecture — IN PROGRESS

Status: Phase A selected optimized Leaflet behind a narrow adapter
([approved specification](docs/specs/M3-unified-mobile-explore.md),
[ADR-006](docs/architecture/decisions/ADR-006-explore-rendering-architecture.md)).
PR A is merged; PR B is not merged. R-2 was triggered, reviewed and resolved
by the owner on 2026-10-05: Leaflet is kept (A10). A8 is approved and kept.
The local benchmark is CPU/main-thread dominated; concurrent fetching showed
no measurable local timing improvement. A8 avoids deliberately serialising
independent network requests in real use; its benefit under real network
latency remains unmeasured. PR B's heap limit (115% of same-session base)
and the architecture trigger R-5 (66 MB) are different controls.

The first real-device pass (iPhone Safari, 2026-10-05, both regions) failed
several mobile-UX items. A11 remediation is implemented: the phone results
sheet has collapsed, half and expanded states moved by drag; search, browse
and planner results and feature detail share the sheet with Back; feature
taps select, highlight and fit; source-name labels appear from zoom 14 and
are capped; the layer drawer and sheet are mutually exclusive on phones;
double-tap zooms the map and local zoom-control handling prevents page zoom.
The adapter adds `setSelected` and `setLabels` to its original ten exports.
Automated Chrome coverage does not establish a real-device pass.

One of the three required A11 performance sessions missed the Douglas
all-layers limit: session 2 measured 136.4954% of base against 135%. This is
not a pass and awaits the owner's disposition. Four diagnostic sessions
identified no specific inefficiency in the A11 code; they do not replace
acceptance sessions. A second real-device pass and merge approval are owed.

The map stays north-up. Rotation and compass were not implemented because
Leaflet 1.9.4 has no bearing API and the evaluated GPL-3.0 `leaflet-rotate`
dependency patches Leaflet globally; pursuing rotation is the owner's decision.

- Unify the Aspen and Douglas County app structure.
- Fix mobile map real-estate problems.
- Resolve land styling and evidence presentation (register item N17).
- Address the deferred rule-ordering defects that are not freshness-related
  (register item N16).
- The rendering architecture evaluation selected optimized Leaflet with lazy
  GeoJSON; A10 keeps Leaflet, with the existing reopening triggers in force.

Owner decisions after the third real-device pass (2026-10-06, A13). Release
evidence for M3 is the owner's iPhone Safari pass plus automated viewport
coverage; iPad is unverified and deferred, Android Chrome is unverified.
Deferred beyond M3, each recorded so it is not lost:

- Double-tap map zoom on mobile Safari is unreliable and is deferred to later
  map UX work. Pinch, the + / − controls and page-zoom prevention work.
- A generic "several features under one tap → chooser" interaction, for
  coincident or overlapping selectable features. Two Douglas trails cannot be
  selected from the line today; search selects them.
- Map rotation and a compass, to be revisited when the renderer decision
  naturally reopens. No GPL rotation plugin and no renderer change in M3.
- iPad and Android real-device validation.

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
- Owner product direction (recorded 2026-10-05): the core question this
  milestone answers is "Where can I stay overnight while I have fun doing the
  activities I chose?" Discovery must combine activities, trails, water and
  recreation, camping and overnight options, location, dates, and later access
  and vehicle constraints. M3 supplies only the reusable results, selection
  and detail interaction that this workflow will populate.

## Constraints that apply to every milestone

- [Trust principles](docs/product/trust-principles.md) and the
  [regional data contract](v2/pipeline/docs/data-contract.md).
- [Product principles](docs/product/product-principles.md).
- [Agent stack and workflow](docs/architecture/agent-stack.md), including
  human-approved merge authority.

## Relationship to `v2/ROADMAP.md`

[v2/ROADMAP.md](v2/ROADMAP.md) is the September 2026 execution queue from
before the milestone structure existed. It is kept as a historical working
log. Where it differs from this file on ordering or scope, this file governs.
