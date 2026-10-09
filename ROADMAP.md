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
| M3 | Unified Mobile-First Explore Architecture | **Complete** |
| M4 | Functional Recreational Water | **In progress — M4-A complete; M4-B PAUSED_BY_OWNER** |
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

## M3 — Unified Mobile-First Explore Architecture — COMPLETE

Merged on 2026-10-06 (PR A #6, amendment A3 #7, browser-CI hardening #8,
PR B #9; `main` at `9868fe8`). The owner approved PR B after the final iPhone
Safari check passed: the camera is preserved on land and bare-map taps, the
selected trail is distinguishable, the trail colour `#d06030` is accepted for
M3 (not the final map or brand colour system), and the land selection cue is
a stronger fill with no outline. Release evidence is the owner's iPhone Safari
passes plus automated viewport coverage. The paragraphs below are the record
of how the milestone got there; where they say something is owed or awaited,
the owner decisions of A13 and A14 in the specification settled it.

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
- A full visual and marketing colour-system redesign; the M3 trail colour is
  an interim improvement.
- The full Choose Your Adventure workflow (M8).

## M4 — Functional Recreational Water

- Distinguish useful lakes, reservoirs, rivers and streams from generic
  hydrology clutter.
- Support fishing, paddling, swimming and general-recreation relevance.
- Preserve access and permission uncertainty.
- Names alone are not evidence of recreational usefulness.
- Hermes joins the agent stack in a research/operations role beginning with
  this milestone
  ([ADR-004](docs/architecture/decisions/ADR-004-hermes-research-operations-role.md)).

Status: research is complete ([docs/research/m4-water/](docs/research/m4-water/))
and the [specification](docs/specs/M4-functional-recreational-water.md) was
approved by the owner on 2026-10-06 (decisions D1–D12 and O1–O9, including
the exact wording). M4-A source preservation merged in PR #12. M4-B is in
progress on draft PR #17, PAUSED_BY_OWNER on 2026-10-08 at checkpoint 45f877d
(retrieval complete and validated; padded Douglas integration, South Platte
validation, wording, performance sessions, device check and owner approval
outstanding). M4-C reviewed official recreation claims and optional M4-D for
CPW structured data remain later delivery stages.

Technical debt recorded by M4 (owner decision D1): USGS retired the National
Hydrography Dataset on 1 October 2023. M4 uses a documented NHD snapshot as a
transitional basis. A later milestone must validate and then migrate to the
USGS 3D Hydrography Program (3DHP), and may switch only after real Aspen and
Douglas records show that the distinctions M4 relies on (perennial against
intermittent, lake against reservoir, canal against stream), the identifiers,
and every group, claim, exclusion and alias survive the mapping.

## M5 — Land Classification v1

- Authoritative federal, state, local, private and public classification where
  the source supports it.
- Non-federal is not private.
- Ownership is not access.
- Confidence, provenance and spatial precision remain explicit.
- Unknown remains unknown.
- Product-alignment acceptance expectations (added 2026-10-08, see
  [adventure-model.md](docs/architecture/adventure-model.md)): management and
  jurisdiction carry an identity that other features can be related to;
  access stays unknown where it is not established; land keeps stable
  identity for later relationships to overnight and activity features; and
  evidence coverage records which questions were checked for an area (concept
  only; shape set by that milestone's specification).

## M6 — Trails / COTREX

- COTREX for Colorado, **subject to licensing/terms verification**. No COTREX
  content is in the repository today; see
  [v2/pipeline/TRAIL-PILOT.md](v2/pipeline/TRAIL-PILOT.md).
- Hiking, mountain biking, OHV/dirt bike, equestrian and other activities.
- Equivalent authoritative sources elsewhere.
- Access, closure and current-condition claims remain evidence-backed.
- User-facing trail identity (owner requirement recorded at the close of M3,
  2026-10-06). Source geometry and feature identity are not necessarily the
  trail a user has in mind: in cases such as Difficult Creek, several
  connected source features make up what a user would reasonably call one
  trail. M6 evaluates connected source segments with the same or a similar
  name; overlapping or duplicate geometries; segment versus route identity;
  source jurisdiction boundaries; cross-source COTREX / USFS matching; and
  grouping several canonical segments into one user-facing trail where
  evidence supports it. Canonical source records stay preserved. Trail
  features are not merged or renamed on geometric continuity or matching
  names alone.
- Product-alignment acceptance expectations (added 2026-10-08): allowed
  activities and motorized restrictions as claims or unknown; trailhead and
  staging identity where a source provides it; approach and access
  relationships that are source-backed, reviewed or unknown, never inferred
  from distance; restriction evidence coverage (concept only; shape set by
  that milestone's specification); source reconciliation; and
  trail identity that survives a jurisdiction or region-package boundary.

## M7 — Camping / Dispersed Camping

- Developed campgrounds.
- Dispersed and public-land camping.
- Restrictions, closures, access, and vehicle/setup suitability.
- Eliminate inappropriate hard-coded camping-rule behavior.
- No inferred camping permission.
- Product-alignment acceptance expectations (added 2026-10-08): developed
  campground identity; dispersed-camping evidence; overnight legality and
  reservation requirements as claims; vehicle and access implications as
  constraints on routes; relationships to activities and trailheads only
  where established (geographic proximity is not evidence of practical
  camping suitability); evidence coverage (concept only; shape set by that
  milestone's specification); freshness and seasonality; and a backup option
  identified where an independent one exists, and its absence stated.

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
- Product-alignment acceptance expectations (added 2026-10-08): M8 assembles
  trip candidates from the identities, evidence and relationships of M4 to
  M7, following the trip-intent and adventure-candidate model in
  [adventure-model.md](docs/architecture/adventure-model.md). It is not
  filters on top of the map. Every candidate lists its unresolved unknowns.
  Whether
  [continuous geographic Explore](docs/architecture/continuous-explore.md) is
  implemented in or before M8 is the owner's decision when M8 is specified.

## Constraints that apply to every milestone

- [Trust principles](docs/product/trust-principles.md) and the
  [regional data contract](v2/pipeline/docs/data-contract.md).
- [Product principles](docs/product/product-principles.md).
- From M5 onward each milestone ends with the product review in
  [product-scorecard.md](docs/product/product-scorecard.md), including a run
  of the
  [canonical Douglas dirt-bike scenario](docs/product/acceptance-scenario-douglas-dirt-bike.md).
  One baseline run happens after M4 closes. It is not an M4 merge gate and
  does not change "M4 is complete with A, B and C".
- [Agent stack and workflow](docs/architecture/agent-stack.md), including
  human-approved merge authority.

## Relationship to `v2/ROADMAP.md`

[v2/ROADMAP.md](v2/ROADMAP.md) is the September 2026 execution queue from
before the milestone structure existed. It is kept as a historical working
log. Where it differs from this file on ordering or scope, this file governs.
