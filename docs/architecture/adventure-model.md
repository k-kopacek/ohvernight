# Adventure model: relationships, evidence coverage and trip candidates

Status: conceptual model, recorded 2026-10-08. It is documentation only. It
defines no schema, adds no validator rule and implements nothing. Its purpose
is to state which identities and relationships M5, M6 and M7 must preserve so
that M8 can assemble trips, and to do so without weakening any rule in
[trust-principles.md](../product/trust-principles.md) or the
[regional data contract](../../v2/pipeline/docs/data-contract.md).

Labels: **CURRENT** is what `main` does today, **PLANNED** is direction
without an approved specification, **FUTURE / DEFERRED** is recorded for
later.

The question the product must eventually answer:

> Where can I do the activities I care about, how do I get there, where can I
> reasonably stay overnight nearby, what restrictions apply, and what is still
> unknown?

## 1. Proximity is not a relationship

**PROXIMITY IS NOT A RELATIONSHIP.** Distance between two mapped things is a
computed fact about geometry. It establishes nothing else.

A campground five miles from a trail does not prove:

- usable road connectivity between them;
- that the road suits a trailer, or the user's vehicle at all;
- that the vehicle may legally use that road;
- that both are on the same side of a river, ridge or closed gate;
- that the campground is a practical place to stage from;
- that the activity is permitted on the trail.

This extends contract rule 15 ("Straight-line proximity is not a connection")
from individual features to the assembly of a trip.

### CURRENT state of proximity in the app

`v2/trail-discovery.js` computes straight-line distance from an overnight
place to trail geometry and lists up to three trails within five miles
(`nearbyTrails`, `adventureOptions`), surfaced in Aspen through the
`adventure_pilot` capability. That is a distance listing. It is not a
relationship in the sense of this document, and nothing in this model may be
populated from it. Whether its present wording is clear enough about that is
raised as an owner question in the pull request that adds this document.

## 2. Entities

Only what is needed to state the relationships. Nothing here is a schema.

| Entity | CURRENT | Notes |
|---|---|---|
| Activity feature (trail, water, later others) | Trails: USFS source segments with raw use strings, both regions. Water: NHD, grouped rivers from M4-B. | User-facing trail identity is M6. Water activity claims are M4-C. |
| Trailhead or staging area | **Does not exist** as an identity. Douglas has 36 recreation-site records, 17 of them with source `site_type` TRAILHEAD; nothing links one to a trail. | M6. |
| Road or access route | USFS road geometry in both regions, with source access fields. No route between two things is represented. | M6 and M7. |
| Vehicle or access constraint | Aspen planner holds trip rules for some setups; not attached to roads or routes. | M7; "inappropriate hard-coded camping-rule behaviour" is already on the M7 list. |
| Overnight option | Aspen: developed lodging, RIDB options, reviewed sites, research areas. Douglas: recreation-site records only (five with source `site_type` CAMPGROUND, one HORSE CAMP), with no camping permission established. | M7. |
| Agency, operator or jurisdiction | Carried per record as `evidence.agency` and per manifest source. Not an entity with its own identity. | M5. |
| Restriction, closure or seasonal rule | Aspen fire-restriction monitor and reviewed rules; Douglas none loaded. | M5 to M7, per kind. |

## 3. Relationships

A relationship is a statement connecting two identified entities. It carries
its own evidence. It is never implied by the entities merely existing near
each other.

Each relationship has one of three origins:

- **source-backed**: a responsible source states it (a trailhead record names
  the trail; a motor vehicle use map designates the road).
- **derived**: computed from source data by a documented, reproducible rule
  (two segments share an endpoint at source precision). A derived relationship
  is labelled as derived and never upgraded to source-backed by repetition.
- **unknown**: not established. This is the default.

| Relationship | Meaning | Source-backed? | May be derived? | Evidence required | Stays UNKNOWN when | Proximity alone |
|---|---|---|---|---|---|---|
| activity feature `starts_at` / `accessed_from` trailhead or staging area | This is a place from which the feature is reached. | Yes, where a managing agency's record, map or page names the trailhead for the trail. | Only as a *candidate*: a trailhead point that touches the trail's source geometry at source precision. A candidate is listed for review, not published as a relationship. | The source statement, or a reviewed candidate. | No source names it and no reviewed candidate exists. | **Insufficient.** A parking area 200 m from a trail may be on the wrong side of a fence. |
| trailhead or staging area `approached_via` road or access route | This road is how a vehicle reaches the place. | Yes, from agency directions or a designated-route map. | Only as a candidate from network topology (the point lies on the road geometry). | Source statement or reviewed candidate; the road's own designation evidence is separate. | The road network to the place is not established. | **Insufficient.** |
| road or access route `associated_with` vehicle or access constraint | A limit that applies to using it: vehicle class, width, clearance, season, permit, gate. | Yes: motor vehicle use maps, travel-management orders, operator pages. | No. A constraint is never derived from geometry, surface or appearance. | Reviewed source, with jurisdiction and effective dates. | No reviewed source. Absence of a stated limit is **not** "no limit". | Not applicable. |
| trail or trailhead `relevant_to` overnight option | Staying here is a practical base for doing that. | Rarely; sometimes an operator states it. | Yes, but only as a composition of established links: the overnight option and the trailhead are each `approached_via` routes that connect, and no known constraint excludes the user's vehicle. | Every link in the chain, each with its own evidence. | Any link in the chain is unknown. The candidate may still be shown, with the unknown link named. | **Insufficient.** This is the central case. |
| any entity `governed_by` agency, operator or jurisdiction | Who sets the rules here. | Yes: the managing agency in the source record. | Spatial containment in a management polygon gives *context* only (contract rule 12 and rule 13: generalized polygons are not parcel-level). | Source record for the entity itself. | Only generalized polygon context exists. | Not applicable. |
| any entity `constrained_by` restriction, closure or seasonal rule | A rule that limits use, with its scope and dates. | Yes: the order or rule and its stated scope. | No. A restriction's applicability to a feature is established from the order's own scope, not from distance to something the order mentions. | Reviewed record with authority, jurisdiction, scope and effective interval. | Scope is unclear. A restriction of unclear scope is **retained and flagged**, never dropped (trust principle 5). | **Insufficient**, in both directions. |

Rules that hold for every relationship:

1. Unknown is the default and is stored as absence, not as `false`.
2. A relationship has a direction, two stable IDs, an origin, and evidence.
3. A derived relationship names its rule and its inputs.
4. Staleness never removes a restricting relationship (`constrained_by`,
   `associated_with` a constraint). It may demote a supporting one to unknown.
5. A chain is only as established as its weakest link, and the weakest link is
   what the user is shown.
6. No relationship is created by a name match alone or a geometry match alone
   (the Difficult Creek lesson, generalised).

The model can stay at JSON and document level. Nothing here requires a graph
database, and one must not be introduced because the picture looks like a
graph. Technology is chosen later from real scale and query needs.

## 4. Evidence coverage

### The problem

Two different situations look identical in data today:

- "No restriction exists."
- "Ohvernight has not checked that category of restriction."

Only the second is ever true by default. The model must make the difference
visible.

### CURRENT

The contract already has region-level **fact coverage**: eight dimensions
(`ownership`, `public_access`, `camping_permission`, `closures`,
`restrictions`, `road_access`, `trail_access`, `recreation_permission`), each
with a state of `none`, `context` or `reviewed_partial`. There is deliberately
no state meaning complete, verified or permitted. It applies to a whole
region and says nothing about one feature or one trip.

### PLANNED concept

**Evidence coverage** records *what was looked for*, separately from *what was
found*. It extends the existing fact coverage downward, from a region to a
feature, relationship or trip candidate. It is not a second, competing
vocabulary: a later specification should refine the eight existing dimensions
rather than invent parallel ones.

A coverage item answers, for one subject and one category:

| Field | Meaning |
|---|---|
| category | What kind of rule or fact was checked (list below). |
| subject | The feature, relationship or area the check applies to. |
| jurisdiction and source | Whose rules were checked, and where. A check of county rules says nothing about federal orders. |
| checked at | When Ohvernight looked. |
| review-by | When the check is due again, from product review policy held in data. |
| result | Exactly one of: **claim recorded**, **restriction recorded**, **checked, nothing determinable**, **not checked**. |

Candidate categories, to be settled by the specification that first needs
each: ownership and management; access; motorized-use rules; camping rules;
seasonal closures; fire and emergency closures; reservation and permit
requirements; water activity rules; road and access restrictions.

### Rules

1. **Coverage never creates permission.** `motorized rules: checked` does not
   mean `motorcycles: allowed`. Permission comes only from a claim, under the
   existing fail-closed rule.
2. **"Checked, nothing determinable" is not "no restriction".** It means a
   named source was read on a date and did not settle the question.
3. **Not checked is the default** and is shown, not hidden.
4. **Coverage is scoped.** A check is for one category, one jurisdiction and
   one subject. It does not spread to neighbouring features, to other
   categories or to other jurisdictions.
5. **Coverage ages.** A check past its review-by date is shown as stale. A
   stale check never weakens a recorded restriction.
6. **There is no "fully covered" state**, for the same reason fact coverage
   has no "complete" state.
7. Coverage is reported as a list of categories with results, never collapsed
   into a single score that could read as confidence or safety.

## 5. Trip intent and adventure candidate (M8, PLANNED)

M8 must not be filters on top of the map. It assembles a coherent candidate
outing from identified entities, established relationships and their
evidence, and says plainly what it could not establish.

### Trip intent

What the user tells the product. None of it is evidence.

- geography (a place, an area, or "near here");
- dates, including the departure day;
- activities;
- vehicle and access profile;
- overnight preference;
- optional constraints and preferences.

### Adventure candidate

| Part | What it is | Kind of fact |
|---|---|---|
| Primary activity feature or features | The trail, water or other feature, by user-facing identity. | Source fact (existence, geometry, source attributes). |
| Activity permission for the chosen activity | Whether the activity is allowed there. | Official recreation claim, or unknown. Never derived. |
| Access or staging point | The trailhead or staging area. | Source fact for the place; the link to the feature is source-backed, a reviewed candidate, or unknown. |
| Approach and access context | The road or route, and constraints on it. | Source fact and official claim for designations; derived for network connectivity; unknown otherwise. |
| Overnight option | Where to stay. | Source fact for existence; official claim for permission and reservation rules; unknown otherwise. |
| Backup overnight option | A second, independent option where one exists. | As above. Absence of a backup is stated, not hidden. |
| Distance and travel relationship | How the parts relate in space. | Derived, labelled as straight-line or as network distance, with its basis. Never presented as travel time unless a routing source supports it. |
| Applicable restrictions | Closures, seasons, orders, limits. | Official claim. Retained when stale. |
| Evidence and provenance | Source, agency, retrieval and review dates for every part. | Source fact. |
| Evidence coverage | Which categories were checked for each part. | Recorded by Ohvernight; not a claim. |
| Freshness | Whether each review is within policy for the trip dates. | Derived, computed at evaluation time, never stored. |
| Unresolved unknowns | Every link or question not established, named individually. | Unknown, by definition. |
| Viability explanation | Why this candidate is offered, in terms of what is established. | Derived from the parts above. It adds no fact of its own. |
| Alternates | Other candidates, and what differs. | Derived. |
| First-party observations | What a user later reports. | **FUTURE / DEFERRED.** Not evidence of permission; M4 has no community records. |

There is no final ranking algorithm here and none is proposed. Two properties
are fixed now because they are trust properties, not ranking choices:

- A candidate is never made to look more complete by omitting its unknowns.
- Ordering must not imply confidence the evidence does not have (trust
  principle 7). A candidate with a critical unknown must not outrank a fully
  established one merely for being closer.

### What M5, M6 and M7 must provide

| Milestone | Must provide for M8 |
|---|---|
| **M5 Land** | Management and jurisdiction as an identity other entities can be `governed_by`; ownership kept separate from access; access left unknown where not established; stable, namespace-safe IDs; coverage results for ownership/management and access per area. |
| **M6 Trails** | User-facing trail identity separate from source segments, with the member map preserved; per-activity use including motorized classes as claims or unknown; trailhead and staging identities where a source provides them; `starts_at` and `approached_via` links as source-backed, reviewed or unknown; restriction and closure links with coverage; identity that survives a jurisdiction or package boundary. |
| **M7 Camping** | Developed campground identity; dispersed-camping evidence without inferred permission; overnight legality as a claim for a setup and place; reservation and stay-limit claims; vehicle and access implications as constraints on routes, not as assumptions; `relevant_to` only as an established chain; seasonality and freshness; enough independent options that a backup can be offered. |
| **M4 Water (already specified)** | Grouped river identity (M4-B) and reviewed activity claims with allowed, restricted, prohibited and unknown semantics (M4-C). Water is not functionally complete on geometry and display alone. |

## 6. Discovery UX principle (FUTURE)

Primary user intent stays visible and easy to change. At minimum: location or
search, selected activities, dates, and eventually the vehicle and access
profile. Detailed evidence and advanced filtering are secondary. Core
discovery controls are not buried in a generic collapsed Filters panel.

This does not authorise a redesign of the current M4 interface.

## Guardrails

- Do not reopen M1 to M3 without necessity.
- Do not implement M8 early.
- Do not weaken a trust rule so that a candidate looks complete.
- Do not infer a relationship from distance, permission from ownership,
  access from the existence of a road or trail, or suitability from
  proximity.
- Do not change roadmap order automatically.
- Do not add infrastructure before data and relationships require it.
