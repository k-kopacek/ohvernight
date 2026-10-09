DRAFT - UNREVIEWED; illustrative, not product truth, not a claim record

# Rampart worked example against the adventure model

This research example encodes two candidate arrangements described in the archived Rampart weekend research. It tests whether the conceptual model can carry the evidence without converting source statements, derived geometry, or gaps into Ohvernight claims. The JSON companion is illustrative only and is not consumed by the application.

## Source and identity boundary

The archive records a weekend plan with a rider and family using separate places. Plan A pairs Cabin Ridge Trailhead with Cabin Ridge Picnic Area. Plan B pairs Dutch Fred Trailhead with Cabin Ridge Picnic Area. The source record identities below are from `v2/regions/douglas-co/research.json` on `main`: Cabin Ridge TH `recreation-3311789`; Dutch Fred Trailhead `recreation-3306075`; Cabin Ridge Picnic Site `recreation-3316544`; trail 0675 `usfs-trail-8964041`; trail 0679 `usfs-trail-8971352`. Other archive-mentioned features not represented in that bundle are identified as `not in Ohvernight data`.

Archive evidence pointers use the committed archive branch paths, e.g. `docs/research/overnight-2026-10-08/rampart-weekend-plan-and-gaps.md#plan-a`; source quotes and dynamic status are only as recorded at the archive's retrieval time. They are not refreshed here. This document preserves conflicting readings side by side and does not decide them.

## Plan A — Cabin Ridge Trailhead + Cabin Ridge Picnic Area

The archive proposes the trailhead for the rider and the picnic area for family day use. It records trail 0675 and an agency statement that Cabin Ridge Trailhead accesses it. It also records the Forest Service page's “ten (10) units with picnic tables, fire rings and a vault toilet” and “day use fee of $7,” payable by check or money order. The archive's coordinates imply roughly 290 m straight-line separation and a longer road route; no source establishes a walking path. The recorded source banner “Site Open” was undated for the intended outing, so current status remains unknown.

The JSON carries the rider and family separately in Trip Intent. Its candidate includes each required part, fact-classed facts, all six named relationship types, category-level coverage, unknowns, and alternates. A `reviewed candidate` origin is used only where the archive explicitly calls the relationship a reviewed candidate; otherwise a proposed pairing is `unknown` or `derived` as recorded. This encoding does not assert the pairing is established.

## Plan B — Dutch Fred Trailhead + Cabin Ridge Picnic Area

The archive treats Dutch Fred as an alternative staging point while the family uses Cabin Ridge Picnic Area. It records Dutch Fred Trailhead as an agency site and trail 0679 as the named trail, while preserving the missing MVUM table row and disagreements between partner and agency readings. It says reuniting the parties without a road is not established; the 0681/0767 geometric possibility is not a confirmed walk or route. The Dutch Fred spur road, lot signage, trailer fit and current conditions remain unknown.

As with Plan A, each possible join has an explicit origin and evidence pointer. An unknown `relevant_to` or `approached_via` link is retained even when the points are near one another. Straight-line distance is recorded only as derived distance with its basis.

## What the model could not express

Each item is a concrete gap or awkward encoding in the conceptual model, not a claim that the proposed amendment is approved.

1. **Two parties with different roles and a reunite constraint.** Trip Intent has one user, activity list, vehicle profile and preferences, so rider and family must be flattened into one intent. Add `parties[]` with member roles, separate activity/vehicle profiles, and explicit `reunite_constraint` whose route condition remains unknown until evidenced.
2. **A day-use family option versus an overnight option.** The candidate parts include “Overnight option” and backup, while Cabin Ridge Picnic Area is specifically day use. Add typed `stay_option` with `use_period` (`day_use`, `overnight`, `unknown`) and disallow day-use from satisfying overnight intent.
3. **Partner-stated facts.** The four fact classes include community signal, but the model says M4 ships no community-signal records and does not define a partner source subtype or trust boundary. Add `source_role` and `review_state`; partner statements remain attributed and cannot establish legal designation.
4. **Conflicting source readings.** No explicit representation is defined for two retained claims about one trail or parking condition. Add `claim_set` grouping incompatible claims with source, retrieval/review time, scope, and unresolved status; never choose by recency alone.
5. **Dynamic status and checked time.** Coverage has `checked at`, but it is unclear how an agency's live “Site Open” banner (retrieved but not human-reviewed) relates to current operational status. Add separate `source_status` with observed value, source time/retrieval time, and freshness; keep it distinct from reviewed coverage and permission.
6. **Payment method.** A fee amount and check-or-money-order instruction have no dedicated model part. Add a source-fact `payment_requirement` with amount/currency, accepted methods, effective period, and unknown for unlisted methods.
7. **Hammock and other setup constraints.** Optional preferences cannot express a site rule or a specifically unresolved equipment question. Add setup/equipment constraints as `constrained_by` facts with scope/evidence and an explicit unknown state; absence of a prohibition must not mean permission.
8. **Trailer fit and staging-lot capacity.** Vehicle profile is broad and no facility capacity units or maneuvering constraints are defined. Add vehicle dimensions and facility/route constraints with units and source-backed scope; unknown remains unknown.
9. **Walking link to reunite.** Connectivity is described for vehicle routes but an on-foot path is not a separately typed network. Add travel mode to `approached_via` and `relevant_to` link chains; a road edge is not a walking path.
10. **Two regulatory instruments for one trail.** The model has restrictions but does not specify how a designation map and a separate parking order interact or conflict. Add distinct instruments and scoped provisions, with precedence only when the instruments themselves say so; preserve unresolved conflict.
11. **Plan-level alternative semantics.** “Alternates” does not specify which party or part changes. Add `alternate_delta` identifying changed entities/relationships and retained shared intent.

## What M5, M6 and M7 must supply for this candidate to be assembled automatically

| Milestone | Required input for these plans | Missing input that must remain unknown |
|---|---|---|
| M5 land | Stable identity for managing agencies/jurisdictions and source-backed `governed_by` links; ownership distinct from management and access; feature-scoped coverage. | Whether a generalized manager polygon applies to a specific lot or route; access rights not stated by a source. |
| M6 trails | Stable user-facing identity and source-member map for trails 0675/0679; activity-specific claims; trailhead/staging identities; evidence-backed or unknown `starts_at` and road approaches; order/MVUM scope and freshness. | Conflicting 0679 readings, trail condition, crossings and walk links absent a resolving source. |
| M7 camping/day use | Typed day-use facilities versus overnight options; source facts for fee and payment, facilities and status; setup-specific permission/restriction claims; seasonal status with checked/retrieved time; independent backup. | Cabin Ridge picnic current opening/availability; hammock permission; trailer fit; signage; no inferred overnight status for a picnic site. |

See [the JSON candidate](rampart-candidate.example.json) for both structured plans. It parses as JSON; the model remains conceptual and the example is not a validated product schema.
