DRAFT - UNREVIEWED

# M8 ranking architecture options

Status: design options for the owner, written 2026-10-07. Nothing here is a
decision, a specification or a roadmap change. Nothing is implemented.

Labels used: **HERMES-SOURCED** means the claim comes from a Hermes report
that the coordinator has not re-checked (see
`docs/research/product-opportunities/README.md`). **INFERENCE** is this
document's own reasoning. **UNKNOWN** means the evidence is missing. Unlabelled
statements about the repository were read from the cited file.

## Summary for the owner

1. **Today's data cannot support a ranking that gates on permission.** Both
   regions declare `camping_permission` as `none` and `public_access` as
   `none` in `fact_coverage`; Aspen has one reviewed rule record and Douglas
   has none (`v2/regions/*/region.json`). A design that only ranks options
   with established overnight permission returns nothing. Every option below
   is judged on whether it stays honest when almost everything is unknown.
2. **Five architectures are described.** They are not exclusive: D is a data
   layer the others can sit on, and E is an optional layer on top.

   | | Architecture | One-line character |
   |---|---|---|
   | A | Hard filters, then a transparent deterministic score | Familiar; one number per result; highest risk of implying endorsement |
   | B | Two axes: fit orders, evidence is shown beside it | Unknowns lower stated evidence, never position |
   | C | Constraint satisfaction with explained eliminations | No score; three groups and a reason for every exclusion |
   | D | Pipeline-built "overnight + activity" pair table | The data substrate; makes the static site workable |
   | E | Optional local personalisation | Re-weights fit only; never touches evidence |

3. **The smallest honest first version is C on top of a small D**: one region,
   pairs built offline, results in three groups (restricted or excluded, meets
   stated constraints with unknowns listed, not evaluable), ordered inside a
   group by one declared neutral key. No score and no "best".
4. **The largest owner decision** is whether an unknown may change a
   result's position at all. The Hermes synthesis asks for a ranking policy
   that "penalizes unknown or stale critical claims" (HERMES-SOURCED,
   `idea-fairy-report.md`, Tier 1 item 4). The trust principles say ordering
   and ranking must not communicate more certainty than the evidence supports
   (`docs/product/trust-principles.md` section 7). Those pull in different
   directions and the options below resolve the tension differently.

## 1. What the repository gives M8 to work with

The roadmap states the M8 inputs and output: state or location, dates,
activities, camping or lodging preference, vehicle and access constraints;
"ranked adventure options based on verified evidence"; and the owner's core
question (`ROADMAP.md`, M8). `docs/architecture/system-overview.md` records
that there is no backend, database, API, account system or analytics, that
trip and saved state stays in browser local storage, and that an Aspen pilot
planner exists with "unchanged inputs/ranking". The existing evaluator is
`v2/trip-rules.js` (`evaluate(place, trip, today, policy)`, with the date
injected) and `v2/trust.js`; exclusions precede cautions and conflicting rules
merge conservatively.

| Input or signal | Exists in the repository today | Gap | Candidate source (HERMES-SOURCED, `future-sources/source-watchlist-m5-m8.md`) |
|---|---|---|---|
| Location | Region manifests and coverage polygons; place coordinates | No statewide extent; two pilot regions | — |
| Dates | Trip dates in the evaluator; `effective_from` / `effective_to` on claims; MVUM seasonal designations evaluated for one past trip (register item N8) | Seasonal rules are prose in `summary` and are not evaluated (M4 spec 9.4) | MVUM vehicle-specific date fields |
| Activities | Trail-use strings kept verbatim (`trail_access: context`); four water activities per reviewed water after M4-C | No COTREX; water claims cover a handful of waters | USFS trails, BLM GTLF; COTREX blocked on written permission |
| Vehicle | Three classes in the refresh workflow (`passenger_car`, `high_clearance`, `motorhome`); one rule with `requires_high_clearance` | Douglas roads are geometry only; `road_conditions` is always `unknown` | MVUM `PASSENGERVEHICLE`, `HIGHCLEARANCEVEHICLE`, maintenance level; BLM observed route-use class |
| Drive tolerance | Straight-line distance can be computed | No routing or travel-time data. "Proximity is not a connection" (`trust-principles.md` section 2) | UNKNOWN: no licensed routing source identified |
| Camping style | `overnight_inventory` layers in Aspen (`overnight_options`, `ridb_options`); `reviewed_sites`; computed research areas that stay `needs_review: true` | Douglas has no overnight inventory layer; Rampart listing is hard-coded (N7); M7 not started | RIDB; BLM recreation sites; forest dispersed-camping pages (prose) |
| Amenities | UNKNOWN which RIDB attributes are retained in `ridb-options.json` | Not modelled as claims | RIDB facility and campsite attributes |
| Dogs | Nothing | No field, no source | Operator and agency pages state pet rules per destination (HERMES-SOURCED, `hermes/q3-trip-failure-modes.md`) |
| Children | Nothing | No authoritative source exists for "suitable for children" (INFERENCE) | — |
| Accessibility | Nothing | UNKNOWN whether RIDB accessibility attributes are reliable | RIDB, UNKNOWN |
| Remoteness | Derivable from geometry | Would be a derived fact and must be labelled as computed (M4 spec section 4) | — |
| Weather, snow | Nothing | No feed | NWS API (open, needs identifying User-Agent); SNOTEL; SNODAS. CAIC prohibits automated collection |
| Closures | `closures: none` in both regions | No structured national endpoint for forest orders | USFS alerts (HTML, PDF); CPW closures via COTREX (blocked) |
| Fire restrictions | Aspen `fire_restriction_stage` is a page-hash change monitor; status is `unknown` and stage is null by design (`06_fetch_fire_stage_monitor.py`) | No stage is known anywhere | DFPC, BLM, county sheriffs; not standardized |
| Recreation permissions | `recreation_permission: none` until M4-C adds a small registry | Unknown for nearly every water | Operator pages, reviewed by hand |

INFERENCE: of the sixteen inputs the brief lists, three can constrain results
with reviewed evidence today (dates against a reviewed rule, vehicle against a
reviewed rule, water activity against a reviewed claim), three can be computed
(location, straight-line distance, remoteness), and the rest are unknown for
every candidate. A first version should ask only for inputs it can act on, and
say so, rather than collect sixteen and silently ignore twelve.

## 2. Constraints every option must satisfy

- Static site: no request-time server. Anything expensive is precomputed by
  the pipeline and delivered as a display artifact under the existing
  budgets and hash checks (`data-contract.md`, display delivery contract;
  ADR-006 triggers R-1 and R-5).
- Freshness is computed in the browser from `last_confirmed_at` and
  `max_age_hours` and is never stored (`data-contract.md` 5.4; M4 spec 9.3).
  A pair table therefore cannot store "current"; it stores references to
  claims and the browser evaluates them at view time.
- A stale supportive claim becomes not established; a stale restriction stays
  in force and is flagged (`trust-principles.md` section 5).
- Fixed trust wording avoids "verified", "legal", "permitted" and "open to"
  (M4 spec section 10). Explanation text below follows that rule.
- Dates, vehicle and list filters do not hide map geometry today
  (`system-overview.md`). INFERENCE: M8 results should keep that property;
  the map remains the free-discovery alternative.

## 3. Candidate architectures

The explanation sketches and the JSON row below use real place names from
the repository, but their distances, counts and dates are illustrative. None
is a measured value or a reviewed claim.

### A. Hard filters, then a transparent deterministic score

**How it works.** Step 1 removes candidates with a reviewed restriction or
prohibition that applies to the stated trip (activity prohibited, vehicle
excluded, stay limit exceeded). Step 2 computes a weighted sum of fit terms
(distance, number of chosen activities nearby, overnight style match) with
published weights, and sorts by it. Pipeline precomputes distances and
activity counts; the browser applies gates and weights in a pure function.

**Data needed.** Pair distances (computable today); reviewed restrictions
(one rule, a few water claims after M4-C). The weights themselves are a
product judgement with no evidence behind them (INFERENCE).

**Unknowns.** Two sub-variants, and the choice matters. A1: unknown terms
contribute zero, which pushes well-documented places up and is a hidden
penalty on unknown. A2: unknown terms are excluded from both numerator and
denominator, which lets a place with one favourable fact outrank a place with
five. Neither is neutral.

**Explanation sketch.**

> Lincoln Creek listed sites + Grizzly Reservoir. 6 km apart in a straight
> line; this is not a driving distance. Matches: high-clearance vehicle,
> 2 nights (stay limit 5, reviewed 2026-09-25). Not established: camping
> permission, current road condition, fire restrictions, availability.
> Ordered 2nd of 7 by distance and activity match only.

**Failure modes.**

| Failure | How it happens here |
|---|---|
| Confident recommendation into a closure | A high score reads as endorsement; `closures: none` means no closure can ever gate |
| Stale restriction | Safe if the gate reads stored status, not freshness. Unsafe if a gate is coded as "current restriction" |
| Popularity bias | Documentation bias: places with more records score higher under A1 |
| Ranking implies permission | Highest of all options. A single number invites "top result is fine to camp at" |

HERMES-SOURCED: the product-bets report lists "a numeric trip-confidence or
safety score" first among bets not to test yet, because a composite could let
favourable data obscure one decisive prohibition or unknown
(`product-bets.md`, "Bets I would not test yet").

**Testability.** Good. Pure function, golden vectors shared between Python
and JavaScript in the manner of the existing freshness parity vectors.
**Cost.** Small to build; high to defend, because every weight is an owner
decision and every reordering needs an explanation.

### B. Two axes: fit orders, evidence is displayed beside it

**How it works.** Reviewed restrictions gate as in A. Remaining candidates
are ordered by fit only. Evidence is a separate, non-numeric statement per
candidate: a count of the dimensions that matter for this trip and how many
are established, restricted or not established. Unknown never moves a
candidate; it changes what is said about it. The user may opt to sort or
filter by evidence, as an explicit action.

**Data needed.** The same as A, plus a fixed list per trip type of the
dimensions that matter (overnight permission, activity permission, access,
restrictions, closures, fire). That list is itself trust-bearing wording.

**Unknowns.** Handled as the brief's example: they lower stated evidence, not
position. The honest consequence is that, today, every candidate shows nearly
the same line ("1 of 6 established"), so the evidence axis discriminates
little until M5 to M7 land.

**Explanation sketch.**

> Ordered by straight-line distance from Maroon Lake.
> Evidence for this trip: 1 restriction reviewed, 0 permissions established,
> 5 not established. Open the list.
> This order says nothing about whether camping is allowed here.

**Failure modes.** Closure: same exposure as A, but no score amplifies it.
Stale restriction: the evidence line shows "review overdue" while the gate
holds. Popularity bias: absent if the fit key is distance; present if fit ever
includes "number of nearby features". Implied permission: reduced, not
removed; position one in any list is read as a recommendation (INFERENCE).

**Testability.** Good. Property test: changing any claim from established to
unknown, or ageing it, never changes order. **Cost.** Small to medium; the
evidence line needs comprehension testing, which Hermes names as the
highest-priority research gap (HERMES-SOURCED, `product-bets.md`, "The one
bet to test first").

### C. Constraint satisfaction with explained eliminations

**How it works.** Each input becomes a constraint evaluated per candidate to
one of four results: `conflicts` (a reviewed restriction contradicts the
trip), `satisfied` (a reviewed, in-policy claim supports it), `not
established`, or `not applicable`. There is no score. Results are placed in
three groups, in this order on screen:

1. Ruled out by a reviewed restriction, each with the restriction and its
   source. Restrictions first.
2. No reviewed conflict found; the list of what is not established is shown
   on every card.
3. Could not be evaluated (source unavailable, outside coverage).

Inside a group the order is one declared neutral key (straight-line distance
or name), stated above the list.

**Data needed.** Nothing beyond what exists; it degrades to "group 2, with
six unknowns each" when data is thin, which is the truthful state of both
regions today.

**Unknowns.** First-class. "Not established" is a result, and the group
heading must not be worded as a pass. HERMES-SOURCED: "Make 'not established'
a first-class result" and "No supported alternative found must remain valid"
(`hermes/q3-trip-failure-modes.md`, recommendation 9; `idea-fairy-report.md`,
alternate-plan risks).

**Explanation sketch.**

> Ruled out for this trip (1)
> Cheesman Lake, paddling: Prohibited. All boating prohibited. Denver
> Water. Reviewed 2026-10-20.
>
> No reviewed conflict found (4). This is not a statement that the trip is
> allowed. For each: camping permission, access, closures and fire
> restrictions are not established.
>
> Not evaluated (2): source unavailable when this data was built.

**Failure modes.** Closure: the group-2 heading is the control; if it ever
reads as "OK", the design fails. Stale restriction: eliminations use stored
status, so a stale prohibition still eliminates and is flagged. Popularity
bias: none. Implied permission: lowest of the options, because there is no
rank to misread. Its own failure is usefulness: a user may find seven
undifferentiated cards unhelpful (INFERENCE), and group 1 could wrongly
suggest that everything not listed there is unrestricted. "Openness is never
inferred from the absence of a mapped closure" (`trust-principles.md`
section 2) must be restated in the interface.

**Testability.** Best. Each constraint is a small pure function with a truth
table; eliminations are exact strings that can be compared to literals, as
M4 does for its sixteen fixed strings. **Cost.** Small.

### D. Pairwise "overnight + activity" relationship table, built in the pipeline

**How it works.** The pipeline emits, per region, a table of pairs: one
overnight candidate, one activity feature, and the relationship between them.
The browser loads the table on entering the planner, not at map start, so it
does not add to initial bytes (the pattern M4-A uses for
`water-aliases.json`).

Sketch of one row (INFERENCE; not a contract proposal):

```json
{"overnight_id": "lincolncreek",
 "activity_id": "nhd-…",
 "activity_kinds": ["paddling", "fishing"],
 "relation": {"kind": "straight_line", "km": 6.1, "computed": true},
 "connection": {"status": "unknown"},
 "claim_refs": ["rules:lincoln-creek-listed-sites",
                "water_recreation:nhd-…#paddling"],
 "not_established": ["camping_permission", "public_access",
                     "closures", "fire_restriction", "road_condition"]}
```

Rules that make it safe: the table stores references to claims, never copied
statuses or freshness; `connection` is a claim object and is `unknown` unless
a reviewed source states that this overnight place serves this activity
place; the distance is a derived fact and is labelled as computed.

**Data needed.** Stable IDs on both sides. Water gets them in M4-A
(`nhd-` plus source ID). Trails are source segments, not user-facing trails,
until M6 (`ROADMAP.md`, M6 trail identity). INFERENCE: a pair table built
before M6 would pair campsites with trail fragments; water and reviewed
places are the only clean activity side today.

**Unknowns.** Explicit per row in `not_established`. A pair the pipeline
never generated is unknown, not incompatible; the interface must say that the
table covers a stated radius and stated layers.

**Failure modes.** Closure: none added, none prevented. Stale restriction:
safe only if rows hold references; a copied status would freeze. Popularity
bias: a radius cut-off favours dense areas (INFERENCE). Implied permission:
the word "pair" suggests the two go together. HERMES-SOURCED: "Nearby may be
misread as accessible" (`idea-fairy-report.md`, Tier 1 item 1).

**Testability.** Good: rebuild-and-compare, as for display artifacts
(R60–R65); a validator rule that every `claim_refs` entry resolves and that
no row contains a status word. **Cost.** Medium. Size is the risk: with N
overnight candidates and M activity features inside a radius the table grows
as N×M; a cap per overnight candidate and a byte budget are needed. Counts
for M7-scale inventories are UNKNOWN.

### E. Optional personalisation layer

**How it works.** A profile in local storage (vehicle class, overnight
style, preferred activities, distance tolerance, whether critical unknowns
should be hidden) pre-fills the inputs and may change the fit key in A or B.
It never reads or writes evidence, never changes a group in C, and is never
sent anywhere, because there is nowhere to send it.

**Data needed.** None from the pipeline.

**Unknowns.** Not its concern, which is the point: the layer is forbidden
from touching them.

**Explanation sketch.** "Using your saved vehicle: high clearance. Change."

**Failure modes.** A learned preference that drifts toward what the user
clicked is engagement ranking; HERMES-SOURCED conditions for promoting this
idea include "profiles capture constraints that affect feasibility, not
engagement-oriented taste signals" (`idea-fairy-report.md`, Tier 3). A "hide
unknowns" switch can hide the most important line on the card.

**Testability.** Property test: with and without a profile, the set of
eliminations and every evidence statement are identical. **Cost.** Small.
HERMES-SOURCED: scored Tier 3, "useful support infrastructure, not a
standalone opportunity".

### Comparison

| | A score | B two axes | C constraints | D pair table | E profile |
|---|---|---|---|---|---|
| Works with today's data | Yes, but misleading | Yes, low discrimination | Yes, truthfully thin | Water side only | Yes |
| Unknown changes position | Yes (either variant) | No | No | n/a | No |
| Risk of implied permission | High | Medium | Low | Medium (wording) | Low |
| Explanation burden | High | Medium | Low | Low | Low |
| Build cost (INFERENCE) | Small | Small–medium | Small | Medium | Small |
| Needs a server | No | No | No | No | No |

## 4. What must not be ranked or implied

Drawn from `trust-principles.md`, ADR-005, the M4 specification and
HERMES-SOURCED lists (`q3-trip-failure-modes.md`, "Failure modes the tool
must never claim to rule out"; `idea-fairy-report.md`, rejected ideas).

1. No result is ordered or labelled by permission, safety or "best". An
   unqualified best-campsite or safe-route ranking was rejected by the
   synthesis as a violation of the evidence boundary.
2. No single numeric confidence, feasibility or safety score.
3. The absence of a retrieved closure, restriction or fire stage never
   improves a position and is never worded as open.
4. A candidate with a reviewed prohibition for a chosen activity is not
   ranked below others; it is shown as ruled out, with the source.
5. Staleness never moves a restricted candidate up. A stale supportive claim
   is treated as not established.
6. Proximity is never worded as access, connection or "serves". Straight-line
   distance is labelled as such every time it is shown.
7. Popularity, review counts, crowding and "least crowded" are not ranking
   terms. Crowd avoidance was rejected (HERMES-SOURCED) partly because it
   routes people to fragile places.
8. Community or first-party observations never enter a gate or a fit term in
   a way that can relax a restriction (see
   `product-opportunities/first-party-data-flywheel-options.md`).
9. Compensation, affiliate status or tier never affects order or screening.
   HERMES-SOURCED: the monetization packet treats paid ranking with weaker
   free screening as a violation (`personas-and-monetization.md`).
10. Vehicle fit is never stated as passable. A designation is a legal fact
    for a date, not a road condition; `road_conditions` is always `unknown`
    in the contract.
11. Availability is never implied. Nothing in the repository checks it.
12. Computed research areas (`needs_review: true`) are not overnight
    candidates.
13. Suitability for children, dogs or accessibility needs is never inferred
    from a facility existing.

## 5. Minimal first version

INFERENCE, offered as the smallest thing that is both useful and honest:

- Architecture C over a small D, in one region, with the activity side
  limited to features that have stable IDs and at least some reviewed claims
  (water after M4-C), and the overnight side limited to listed inventory, not
  research areas.
- Inputs asked: activity, dates, vehicle class, overnight style. Nothing the
  product cannot act on.
- Output: the three groups of section 3C; each card lists its sources, review
  dates and what is not established; one declared ordering key.
- Fixed, owner-approved strings for group headings and the distance label,
  tested as literals.
- No score, no profile, no weather, no closures, and a visible statement of
  which dimensions this version does not check.

This is close to the "Nearby overnight options" panel that Hermes proposes
as the pairing MVP (HERMES-SOURCED, `product-bets.md`, Bet 1), and to the
concierge experiment it suggests running before building anything. Whether to
build before that experiment is an owner decision.

Tests that would go with any option:

| Property | Check |
|---|---|
| Restriction monotonicity | Adding a restriction never improves a candidate's group or position |
| Staleness monotonicity | Advancing the injected date never improves any candidate |
| Evidence removal | Removing a supportive claim never improves a candidate; under B and C it never changes order |
| Parity | Python and JavaScript produce identical output for shared vectors |
| Wording | No output string contains the forbidden words; group-2 heading equals the approved literal |
| Time independence | Validation of the pair table reads no clock |
| Determinism | Same inputs, same order; ties broken by ID |

## 6. Owner decisions this raises

1. May an unknown ever change a result's position (A), or only what is said
   about it (B, C)? This is the conflict between the Hermes recommendation
   and trust principle 7.
2. Is a numeric score acceptable at all? If so, where are its weights
   recorded and who approves a change?
3. What is the exact wording of the group that has no reviewed conflict? It
   is the most trust-sensitive string in M8.
4. Which reviewed restrictions eliminate, and which only caution? The
   existing evaluator already distinguishes exclusions from cautions.
5. May straight-line distance be shown as an ordering key, given that
   proximity is not a connection? If not, what is the neutral key?
6. Does M8 begin before M6 and M7 supply trail identity and camping
   evidence, on water pairs only, or wait?
7. Which inputs are asked for in the first version? Asking for dogs,
   children or accessibility with no data behind them is a promise the
   product cannot keep.
8. Is a local profile wanted, and may it include a "hide results with
   unknowns" switch?
9. Is a `connection` claim between an overnight place and an activity place a
   new claim type needing a contract change and its own review rules?
10. What is the byte budget for a pair table, and is it loaded only on
    entering the planner?
11. Should the evidence-state comprehension test Hermes proposes run before
    any of this is specified?

## Unknowns

- Whether users read position one as a recommendation regardless of wording.
- Whether a three-group result with no ranking is useful enough to return to.
- Pair-table size at M7 inventory scale.
- Whether any licensed routing or travel-time source is usable on a static
  site.
- Whether the NWS API can be called from the browser within its terms; the
  browser test harness blocks all non-local requests, so a live call would
  also need a testing approach.
