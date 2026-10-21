# Milestone 8 specification — Choose Your Adventure

Status: DRAFT — NOT APPROVED. Source-dependent sections LOCKED.

**For:** Codex (implementation), once approved. **Reviewer / coordinator:** Claude. **Research:** coordinator; Hermes optional. **Base:** `main` at `3965dbf` (PR #39 merged).
**Delivery (proposed):** small sequential pull requests on the two pilot regions only (section 26), each marked NEUTRAL or LOCKED. NEUTRAL ones can start once this specification is approved and the start gate of M8-D2 is met; LOCKED ones wait for the M5–M7 decision or delivery they name.
**Owner decisions:** section 30 is one consolidated packet: what is already settled, recommended defaults the owner can accept in one reply, the continuous-Explore decision (presented with options and no recommendation), and material risks flagged separately with their own decisions. Routine engineering choices are decided in the body and listed in 30.5. Where this document says "M8 does X", read "this draft proposes that M8 does X, subject to the decision named".

Governing documents: `AGENTS.md`, `ROADMAP.md` (M8, including the owner product direction of 2026-10-05 and the product-alignment expectations of 2026-10-08), `docs/agent-stack/roles.md`, `docs/product/trust-principles.md` (normative), `docs/product/product-principles.md`, `docs/product/product-scorecard.md`, `docs/product/acceptance-scenario-douglas-dirt-bike.md`, `docs/architecture/adventure-model.md`, `docs/architecture/continuous-explore.md`, `docs/architecture/system-overview.md`, ADR-005, ADR-006, `v2/pipeline/docs/data-contract.md` (normative for data), `docs/specs/M3-unified-mobile-explore.md` (approved; the shell, sheet, adapter and budgets), and `docs/specs/M4-functional-recreational-water.md` (approved; the format model, the evidence classes and the claim and freshness precedents).

## 0. Reading this draft

### 0.1 What is settled, proposed and locked

| Label | Meaning |
|---|---|
| **SOURCE-NEUTRAL** | A rule that holds whichever sources the owner approves and however the open M5–M7 decisions fall. Proposed for approval now. |
| **LOCKED** | Depends on an open M5, M6 or M7 decision, or on a source the owner has not selected. This draft states only the interface M8 reads and the decision IDs it waits on. Nothing in a LOCKED section is chosen. |
| **OWNER DECISION** | A product-architecture question the roadmap reserves for the owner when M8 is specified (continuous Explore, section 16). Options are set out; none is recommended. |
| **NORMATIVE (restated)** | Already binding through the trust principles, the data contract or an approved specification. Restated so M8 requirements can cite it; this draft does not change it. |

Section 4 lists every section with its label.

### 0.2 Evidence marks

| Mark | Meaning |
|---|---|
| [REPO] | Read from a normative or approved repository document on `main` |
| [MEAS En] | Measured from committed files on `main` for this draft; recorded in [m8-spec-evidence.md](../research/m8-adventure/m8-spec-evidence.md) as E1–E12 |
| [DRAFT M5], [DRAFT M6], [DRAFT M7] | Stated in an unapproved specification draft: M5 `k-kopacek/m5-spec-draft` `2c329e3` (PR #41), M6 `k-kopacek/m6-spec-draft` `82a3c84` (PR #42), M7 `k-kopacek/m7-spec-draft` `b8471b1` (PR #47). Their decisions are open |
| [DRAFT-PR n] | Stated in an unmerged, unreviewed research pull request: #29 (Rampart worked example), #20 (Rampart family day-use Scenario B), #15 (M4–M8 research drafts, including `m8-adventure/ranking-architecture-options.md`). Input only, never authority |
| [INF] | Inference in this draft from the marked facts |
| [UNK] | Not established by anything read |

No network request was made to any publisher for this draft. Every statement in a [DRAFT-PR] input about a route, fee, order or status was an agent's retrieval, which is not a review (trust principle 4); this draft uses those inputs only to shape the model, the fixtures and the scenarios, never as data.

### 0.3 Numbering

- **Requirements are R150 onward.** The M7 draft's last rule is R149 (reserved for an M7 amendment). [MEAS E11] R01–R149 are validator rules. M8 is mostly browser behaviour, so each M8 requirement names how it is enforced: **V** validator rule, **N** Node test, **B** browser check, **H** human review at a gate. A V requirement is a stable validator rule in the existing sense. The count is in section 30.6.
- Trip parts are **TP1–TP10** (definitions, section 8.2). Existing pilot behaviours are **PB1–PB12** (section 20). Degraded states are **DS1–DS13** (section 11). Dependency interfaces are **DI1–DI10** (section 7).
- LOCKED interfaces continue the M7 draft's L7–L11: M8's are **L12–L17**.
- Relationship rules continue the M7 draft's RL9–RL15, and M6's RL1–RL8 apply unchanged: M8 adds **RL16–RL18**.
- Owner decisions are **M8-D1 to M8-D20**; material risks are **M8-MR1 to M8-MR7**.

## 1. Problem

**The product has a pilot labelled "Choose your adventure" that pairs places by straight-line distance.** Aspen's landing says "Choose your adventure." and leads with "See camping listings and trails by straight-line distance". [MEAS E1] Its assembly pairs each campground or dispersed listing with up to three trail segments within five straight-line miles whose source management strings name the activity, and orders places with a trip conflict last, then nearest first. [MEAS E6] That is a distance listing. Its wording is honest about that, but it is not the outing the roadmap asks for, and its order rewards nearness, which the adventure model forbids when the nearer candidate has an unknown the farther one has established. [REPO adventure-model section 5]

**Douglas has no planner at all.** Its activity, dates and vehicle sit inside a collapsed "Filters" panel of a Browse finder (product principle 14 says core intent is not buried there), and its connections are straight-line listings marked "connection unverified". [MEAS E6] [REPO product-principles 14]

**Almost nothing a trip needs is established yet.** Fact coverage reads `none` for camping permission, closures, public access and recreation permission in both regions, and `context` for trail and road access. [MEAS E2] No trailhead is linked to a trail, no overnight place to anything, no road constraint to a route. [REPO scenario A baseline] M4 to M7 are each building one part of the evidence; M5, M6 and M7 are unapproved drafts whose key decisions are open. [DRAFT M5] [DRAFT M6] [DRAFT M7]

**The two canonical outings fail today.** Scenario A's baseline is predicted to send the tester elsewhere for approach, backup and closures; Scenario B's baseline reached no viable trip, needed seven or eight external sites, and induced four unsupported assumptions. [REPO scenario A] [DRAFT-PR 20]

The problem M8 solves is therefore not "rank the map". It is to assemble candidate outings from identified things and established links, say plainly which links and answers are not established, order candidates only by what is established, and keep the free map one tap away.

## 2. Goals and the product question

1. **Trip intent, visible and editable.** Location or region, dates, activities, overnight (or day-use) preference, and vehicle and access profile, held as one intent that stays on screen and is changed in one tap (section 6).
2. **Adventure candidates, not filtered layers.** Each candidate is an assembly of trip parts with identities and evidence, following the adventure model (section 8). Map layers are never filtered by intent.
3. **Every unknown listed.** Each candidate names every part and link that is not established, individually, beside the result (sections 9 and 19).
4. **Order from verified evidence only, with the reason shown.** No hidden score. A candidate never outranks another because it is closer, better documented by a source that is not a review, or because a fact about it is missing (section 10).
5. **Restrictions first, fail closed.** A reviewed restriction that applies to the trip rules the candidate out and is shown, never hidden; missing data never produces a positive answer (section 9).
6. **Honest empty and degraded states.** "Ohvernight found no candidate" never reads as "there is nothing here" (section 11).
7. **Explore Map stays the free-discovery alternative,** one tap from every planner screen (section 17).
8. **Mobile first,** on the M3 shell and the PR #39 sheet structure (section 18).

**Product question (product principle 15).** After M8 a user can state where, when, what they want to do, how they sleep and what they drive, and get a short list of candidate outings in which each part — the trail or water, the activity rule for their vehicle and dates, the staging point, the approach, the overnight place and its rule for their setup, a backup, and the orders that constrain them — is either shown with its reviewed source and date, shown as ruling the candidate out, or named as not established. The user can see why each candidate is in its position, and can leave the planner for the open map at any time. A user still cannot learn availability, current conditions, driving time, or whether a gate is open today. How much of each candidate is established depends on what M4–M7 deliver; where they deliver little, M8 says so candidate by candidate instead of looking complete (section 11, M8-MR2).

## 3. Out of scope

- **Selecting, approving or reading the terms of any source.** PAD-US (M5-D6), COTREX (M6 source policy, PR #24) and any RIDB expansion (M7-MR6) stay locked. M8 introduces no new source and fetches nothing.
- **Routing, driving distance and travel time.** No routing source is approved; section 15 is LOCKED (L17). Straight-line distance is never presented as driving distance or time.
- **Availability, vacancy, current conditions, openness today, weather, snow, road condition.** Never a claim, never a status (M7 section 3; M6 AE11 [DRAFT M6]).
- **Creating evidence.** M8 writes no claim, coverage record, relationship, order or constraint. It reads the M4–M7 registries and evaluators and composes their results.
- **Inferring anything those milestones decline to infer:** permission from listing, ownership, management or proximity; a relationship from distance, name or geometry; suitability from a road's existence.
- **Computed camping geometry.** The Aspen "Areas to research" polygons are never an overnight part of any candidate, under every option of M7-D14 (R173). [MEAS E9] [DRAFT M7 12.2]
- **Inputs the product cannot act on:** dogs, children, accessibility, amenities, crowding, difficulty, scenery. Asking for them would promise answers no source supports. [DRAFT-PR 15 ranking-architecture-options section 1]
- **Personalisation or learned preference,** popularity, review counts, affiliate or paid placement. [DRAFT-PR 15 ranking-architecture-options section 4]
- **Accounts, servers, analytics.** State stays in the browser (system overview). [REPO]
- **Any change to the region loader's path restriction, the map adapter and its twelve exports, Leaflet, ADR-006, a new dependency, build step or basemap,** except as the owner's continuous-Explore decision (section 16) explicitly authorises. The root legacy site is not touched.
- **Changes to M4–M7 data, registries, evaluators or wording.** M8 reads them.

## 4. Section map: source-neutral, LOCKED and owner decision

| § | Section | Label | Can the owner approve it now? |
|---|---|---|---|
| 1–3 | Problem, goals, scope | SOURCE-NEUTRAL | Yes |
| 5 | Evidence model | NORMATIVE (restated) + SOURCE-NEUTRAL | Yes |
| 6 | Trip intent | SOURCE-NEUTRAL; the activity, vehicle-class and setup vocabularies are **LOCKED** (L12) | Rules yes; vocabularies no |
| 7 | Dependency contract on M4–M7 | SOURCE-NEUTRAL interfaces; each interface's delivery carries the decision IDs it waits on | Interfaces yes |
| 8 | Candidate assembly | SOURCE-NEUTRAL | Yes |
| 9 | Part evaluation and ruling out | SOURCE-NEUTRAL | Yes |
| 10 | Ordering and the explanation | SOURCE-NEUTRAL | Yes |
| 11 | Empty and degraded states | SOURCE-NEUTRAL | Yes |
| 12 | Day-use base (Scenario B) | **LOCKED** (L13: M7-D16) | Interface only |
| 13 | Staging, approach, `relevant_to` and backup parts | **LOCKED** (L14: M6 L2/L5, M6-D2; M7 L9, M7-D2, M7-D11) | Interface only |
| 14 | Land and jurisdiction lines | **LOCKED** (L15: M5-D6, M5-D13 / R1, M6-D10) | Interface only |
| 15 | Getting there | **LOCKED** (L17: no routing source) | Interface only |
| 16 | Continuous geographic Explore | **OWNER DECISION** (M8-D19) | Decision |
| 17 | Explore Map as the free-discovery alternative | SOURCE-NEUTRAL | Yes |
| 18 | Mobile-first interface | SOURCE-NEUTRAL | Yes |
| 19 | Presentation constraints | SOURCE-NEUTRAL (literals deferred to the owner) | Constraints yes; literals later |
| 20 | Retiring the pilot planner | SOURCE-NEUTRAL | Yes |
| 21 | Contract and configuration changes | SOURCE-NEUTRAL | Yes |
| 22 | Validator rules | SOURCE-NEUTRAL | Yes |
| 23–25 | Budgets, tests, acceptance | SOURCE-NEUTRAL | Yes |
| 26 | Delivery | SOURCE-NEUTRAL plan; PRs marked NEUTRAL or LOCKED | Yes |
| 27–29 | Rollback, risks, unknowns | SOURCE-NEUTRAL | Yes |
| 30 | Owner decision packet | — | Decisions |

Count: **23 sections are source-neutral** (1–3, 5–11, 17–29), two of which carry a named LOCKED parameter that they do not choose (6: the L12 vocabularies; 7: the L16 trail parts model); **4 are LOCKED in full** (12, 13, 14, 15); and **1 is an owner decision** (16). Section 0 is the reading guide, section 4 this map and section 30 the decision packet.

## 5. Evidence model

### 5.1 Classes (NORMATIVE, restated from M4 section 4)

| Class | In M8 | Can it change a candidate's group or order? |
|---|---|---|
| Source fact | Existence, location, names, source attributes and source text of every part, as M4–M7 publish them | No, except that a source fact can make a feature **relevant** to an activity under M8-D5 (8.3). Relevance is never permission and never an ordering key |
| Official recreation information, reviewed | M4 water claims; M6 trail claims; M7 setup claims, orders, fire restrictions and access constraints; M5 management coverage | **Yes, and only this class**, plus established relationships built from it (5.2) |
| Derived fact | Straight-line distance, pairing basis, a computed `relevant_to` chain, the candidate's own composition | A straight-line distance may only break ties (M8-D7). A computed chain counts only when every link in it is established (RL5, RL14) |
| Community signal | None. No field allows one | No |

Evidence coverage is recorded by Ohvernight; it is not evidence and is none of the four classes. [REPO adventure-model section 5]

### 5.2 What counts as established for M8

A trip part is **established** for a trip only when the M4–M7 evaluator that owns it returns, for the user's activity, vehicle class, setup and every trip day, a result that rests on reviewed evidence within policy:

| Part kind | Established when | Never established by |
|---|---|---|
| Activity permission | The owning evaluator returns Allowed or Restricted, within policy, for that activity (and class) on every trip day | A source management or use string; a mapped trail or water; another activity's claim |
| Relationship | Origin `source_backed` or `reviewed_candidate`, within policy; a `derived` link only where its owning milestone permits that rule | Proximity, containment, a name match, touching geometry, network topology alone |
| Overnight or day-use answer | The M7 evaluator returns Allowed or Restricted for the user's setup on every night | A listing, a reservation link, a facility dataset, land management, an area polygon |
| Backup | The M7 backup predicate (RL15) returns an independent backup | A straight-line neighbour |

**R150 (N).** M8 computes no claim status of its own. Every activity, overnight, constraint and freshness result comes from the evaluator of the milestone that owns that registry, called with the trip and an injected clock. M8 composes results; it does not re-implement them.

**R151 (N).** A Restricted result counts as established **with conditions**, and its conditions are carried to the candidate and listed before anything else on it (M8-D9). An Allowed or Restricted result past its review age is whatever its owning evaluator returns (a stale Allowed is not established; a stale Restricted stays Restricted and is flagged review overdue). M8 never recomputes freshness.

**R152 (N).** Evidence coverage never changes a candidate's group or order. "Checked" with no record is not "no restriction" and is never shown as a pass. [REPO adventure-model section 4 rules 1–2]

**R153 (N, H).** Nothing M8 shows is described as verified, complete, open, permitted, legal, safe, suitable or best (trust principle 8). A candidate is never called a plan the user can rely on; "viable" keeps the scenario's meaning and is not shown as a status. [REPO]

## 6. Trip intent (inputs)

SOURCE-NEUTRAL. The vocabularies of activities, vehicle classes and setups are LOCKED (L12).

### 6.1 Fields

Trip intent is what the user tells the product. None of it is evidence (adventure model section 5).

| Field | Values | Required | Notes |
|---|---|---|---|
| `where` | One of: a region (the active package); a named place from the region's search list (destination, trail, water, site); "my location" (browser geolocation, on request) | Yes; defaults to the active region | Under M8-D19 (a) the search area never extends past the active package (16) |
| `dates` | `arrive` and `depart` (ISO dates; departure day included); or a single date for a day outing | Yes | 1–366 nights, as today's `tripDays` [REPO `v2/trip-rules.js:7-13`] |
| `activities` | One or two keys (M8-D4) from the combined vocabulary: M6 trail activities and classes, M4 water activities `fishing`, `boating`, `paddling`, `swimming` | Yes | LOCKED vocabulary (L12) |
| `base` | `overnight` (default) or `day_use` | Yes | `day_use` is LOCKED (section 12) |
| `setup` | For `overnight`: one of the M7 setups (`tent`, `vehicle_sleeping`, `trailer_or_rv`); `hammock` only as an additional question | Yes for `overnight` | LOCKED vocabulary (L12, M7-D3) |
| `place_kinds` | Which overnight kinds to consider (developed campground, designated dispersed area, lodging) | No; default all except lodging | Kinds from M7 7.1 [DRAFT M7] |
| `vehicle` | One vehicle class, `towing` yes/no, optional combined length in feet | Yes; "not chosen" is a valid value | LOCKED vocabulary (L12, M7-D11, M6-D11) |

### 6.2 Rules

**R154 (N).** Intent is user input. It is never stored as evidence, never written into any data file and never leaves the browser (M7 VS9). It is kept under the region's existing trip storage key; no new storage key is added for it.

**R155 (N).** An unrecognised or missing stored value becomes "not chosen", never a default class or setup. Every class- or setup-dependent answer then reads not established (M7 12.3). [DRAFT M7]

**R156 (N).** "My location" is requested only when the user taps it, is held in memory for the session, is never written to storage and is never sent anywhere. It is used only to choose the search area and the straight-line tie-break of M8-D7. Without it the planner works fully.

**R157 (N).** The departure day is a trip day for every date evaluation (M7 CE10, M6 AE10). A day outing has one trip day and no night.

**R158 (N).** Changing any intent field re-assembles candidates from scratch. No result from an earlier intent is reused, kept or shown as current.

**R159 (B).** Map geometry is never added, removed or restyled by intent (M3 section 11, "Explore without a trip"). [REPO]

**R160 (N).** The planner asks for nothing it cannot act on. Inputs out of scope in section 3 have no control. Each input that no loaded registry can evaluate in the active region is shown with a one-line statement that the region has no reviewed evidence for it yet (AP7), rather than being silently ignored.

**R161 (N).** At most two activities per trip (M8-D4 (a)). Each chosen activity needs its own activity part in every candidate; an activity is never satisfied by another activity's feature or claim (M4 9.2 rule 5, M6 AE2).

**R162 (B).** Intent is shown, summarised, in the sheet header at every sheet state, and opens for editing in one tap (product principle 14). Activities, dates, base and vehicle are never placed inside a collapsed generic "Filters" panel.

### L12. Vocabularies (LOCKED)

M8 uses, and does not define, three vocabularies. It shows only keys that the owning specification has approved, labelled as that specification approves.

| Vocabulary | Owned by | Open decisions | Until decided |
|---|---|---|---|
| Trail activities and vehicle classes | M6 9.1 [DRAFT M6] | M6-D3 (keys and statuses); M6 source policy L2, L4 | M8's activity control offers the trail activities already published today (`v2/trail-discovery.js` `activities`), labelled as source use information only, and every trail activity part reads not established |
| Road vehicle classes and towing | M7 10.2 [DRAFT M7] | M7-D11; M6-D11 | The vehicle control offers the three Aspen keys and "not chosen"; every constraint reads not established |
| Overnight setups | M7 8.1 [DRAFT M7] | M7-D3 | The setup control is shown, and every overnight answer reads not established |
| Water activities | M4 9.2 [REPO] | None (approved) | — |

## 7. Dependency contract on M4–M7

SOURCE-NEUTRAL interfaces. Each interface states what M8 reads. Where an M5–M7 decision is still open, the interface names it and the dependent M8 behaviour is LOCKED in sections 12–15 instead of being chosen here.

### 7.1 Interfaces

| ID | Interface M8 reads | Owner | Shape M8 relies on | Status | Open decisions it waits on |
|---|---|---|---|---|---|
| DI1 | Water identity: waterbody feature IDs and stream group IDs, stable across refreshes, with aliases | M4-A, M4-B | `nhd-…` IDs; `water_groups`; `water-aliases.json` [REPO M4 7] | Approved; M4-B delivery | None |
| DI2 | Water activity claims: `fishing`, `boating`, `paddling`, `swimming`, `access` per water, four statuses, with evidence, freshness computed in the browser | M4-C | `water-recreation.json` [REPO M4 9]; claim machinery in PR #44 (unmerged) | Approved; M4-C delivery | None |
| DI3 | Land unit identity and management coverage; access always not reviewed | M5 | `sma-…` / `padus-…` IDs; `land-coverage.json`; M5 rule 3: every candidate on land lists access as not reviewed [DRAFT M5 7, 9, 10] | Draft | M5-D6 (PAD-US terms), M5-D13 / R1 (coverage), M5-D10 now an engineering choice |
| DI4 | User-facing trail identity with members, parts and aliases | M6-C | `trail-…` IDs, member map, parts disclosure [DRAFT M6 8] | Draft | M6-D2 or the M6 source policy (PR #24, L2, L3); M6-D4 (parts model, L16 below) |
| DI5 | Trail activity and vehicle-class claims, restriction-first, with windows, and trail coverage | M6-E | `trail-use.json`, `trail-coverage.json`; four statuses; AE1–AE12 [DRAFT M6 9] | Draft | M6-D3, M6-D7, M6 L4 |
| DI6 | Trailhead and staging identity, and `starts_at` links | M6-F | `trail-relationships.json` [DRAFT M6 10] | Draft | M6 L5, M6 source policy |
| DI7 | Overnight places: identity, kind, `use_period`, and per-setup results from the M7 evaluator | M7-A, M7-C, M7-E | `overnight-places.json`, `overnight-use.json`; `v2/explore/overnight.js` [DRAFT M7 7, 8, 12.3] | Draft | M7-D2, M7-D3, M7-D4, M7-D5, M7 L7, L8, L10 |
| DI8 | Orders, fire restrictions and `constrained_by` links, with the region orders panel | M7-D | `orders.json`, `overnight-relationships.json`; CP6–CP8 [DRAFT M7 9, 11.2] | Draft | M7-D7 / M7-MR2, M7-D8, M7-D9, M7 L7, L10 |
| DI9 | Vehicle constraints, `approached_via` links, and the computed `relevant_to` and backup predicates | M7-F | `access-constraints.json`; RL14, RL15 as pure functions [DRAFT M7 10, 11.5] | Draft | M7-D11, M7 L9 |
| DI10 | Region identity, coverage extent, fact coverage, limitations and source statements | M2, M3 | `region.json`, `explore.json`, `display/index.json`, coverage outline [REPO] | Approved; on `main` | None, unless M8-D19 changes loading |

### L16. Trail parts model (LOCKED parameter of DI4)

Under M6-D4 (a) one trail may have several disconnected parts; under (b) each part is its own trail. M8 does not choose. Its rule holds under both: **R163 (N).** A candidate names the trail as M6 identifies it, carries M6's parts disclosure unchanged wherever the trail is named, and never states or implies that parts connect. If M6 adopts (b), each part is a separate activity feature for assembly.

### 7.2 Rules for consuming interfaces

**R164 (N).** M8 reads each interface only through its owning module's published functions or its validated registry file. It adds no property to any feature and no record to any registry.

**R165 (N, B).** An interface whose file is absent, empty, unavailable or failed to load makes every part that depends on it **not established**, and the candidate says which part and why (DS3, DS4). Absence is never read as "no restriction", "no claim needed" or "allowed" (trust principle 1).

**R166 (N).** A registry that exists but holds no record for a subject means that subject's parts are not established. It never means the subject was checked.

**R167 (N).** M8 never shapes, filters or reorders M4–M7 data to make a candidate look complete (M6 10.4 [DRAFT M6]). A part M4–M7 do not provide is listed as not established.

**R168 (N).** An identity that M4–M7 have not established is not created by M8. Two records are one part only where the owning milestone's identity rules say so (M6 TG, M7 EI3, M5 7.2); never by name, distance or geometry.

## 8. Candidate assembly

SOURCE-NEUTRAL.

### 8.1 What a candidate is

An **adventure candidate** is one assembly, for one trip intent, of the parts below. It is computed in the browser when the planner opens or the intent changes, and is never stored as a result (R158, R250).

### 8.2 Trip parts

| Part | What it is | Provided by | Required for every candidate? |
|---|---|---|---|
| TP1 Activity feature | The trail (by M6 identity, or source segment before M6-C) or water (by M4 identity), one per chosen activity | DI1, DI4 | Yes |
| TP2 Activity permission | The activity's result for the user's class and trip days | DI2, DI5 | Yes; may be not established |
| TP3 Staging point | The trailhead or staging area, with its link to TP1 | DI6 | Shown always; not established until M6-F and section 13 unlock |
| TP4 Approach and vehicle | `approached_via` roads to TP3 and TP5, and the constraint results for the user's vehicle | DI9 | Shown always; never positive (M7 VS4) |
| TP5 Base | The overnight place (or, under section 12, the day-use place) | DI7 | Yes |
| TP6 Base answer | The M7 setup result for the user's setup and every night; for a day-use base, the day-use answer | DI7 | Yes; may be not established |
| TP7 `relevant_to` link | The composed chain between TP5 and TP3 or TP1 | DI9 | Shown always |
| TP8 Restrictions | Orders, fire restrictions and constraints reached through `constrained_by` for TP1, TP3, TP5, with trip-date evaluation | DI8 | Shown always; "not checked" when none reviewed |
| TP9 Backup | An independent backup base by RL15, or the stated absence of one | DI9 | Shown always |
| TP10 Land and jurisdiction | The governing unit lines and "Access: not reviewed" | DI3 | Shown always |

### 8.3 Assembly steps

1. **Search area.** The active region, narrowed to the stated place or location if given (R156). Under M8-D19 (a) the search area never crosses the package edge; where the search area or a candidate's straight-line bound reaches the coverage edge, DS9 applies.
2. **Activity features.** For each chosen activity, the features that are **relevant** to it (M8-D5): (a) a reviewed claim for that activity that is not `unknown`; or (b) the source's own use or management field naming the activity (trails), labelled as source information; or (c) for a water activity, every water M4-B displays. Relevance is never by name.
3. **Bases.** For `overnight`: places of the chosen kinds whose `use_period` is `overnight` (M7 7.1). Until M7-C delivers kinds, bases are exactly the places today's camping lists already show (the Aspen overnight inventory, and the Douglas camping list, which today includes source site type `CAMPGROUND` only, `v2/explore/trail-seasons.js:27` [MEAS E3, E4]), each with every answer not established. This keeps current behaviour and chooses no site-type-to-kind mapping, which is M7's (L8); if the owner withdraws any of those records' existence role under M7-D2, it is not a base. A `day_use_site` never satisfies an overnight base (M7 CE13).
4. **Pairing.** Each base is paired with activity features by the strongest available **pairing basis** (RL16): (i) an established `relevant_to` chain; (ii) a shared established staging point; (iii) the straight-line search bound of M8-D6, labelled as a search bound and never as a connection. A pair is only ever formed within the search area.
5. **Multi-activity.** With two activities, a candidate holds one feature per activity, each paired with the same base by its own basis. Two features are never paired with each other.
6. **Parts.** Fill TP2–TP10 from the interfaces for the trip.
7. **Group and order** (sections 9 and 10).
8. **Cap.** At most 30 candidates are kept per trip, and each base appears in at most 3 candidates, chosen by the ordering of section 10 before the cap is applied. The cap is shown ("Ohvernight lists at most 30"). (Engineering choice.)

### 8.4 Rules

**R169 (N).** No candidate is formed from a relationship that its owning milestone has not established. A straight-line search bound forms a candidate only as basis (iii), and that basis is shown on the candidate.

**R170 (N).** RL16 (pairing basis). Every pair carries exactly one pairing basis from 8.3 step 4. Basis (iii) is a derived fact, labelled with its distance, its measurement (straight-line to the nearest member) and the statement that a connection is not established. It is never titled near, nearby, close, base, serves, connected, backup or recommended (M7 CP14).

**R171 (N).** RL17 (weakest link shown). A candidate shows the weakest link of each of its chains by name, first, under its part (RL5). A candidate with any unknown link is still shown, with that link named (adventure model section 3).

**R172 (N).** Relevance under 8.3 step 2 (b) or (c) is a source fact or a selection fact. It never sets TP2, never appears beside a status word, and is never an ordering key (R189).

**R173 (N, V).** No part of any candidate is drawn from a layer of kind `research_areas`, from any computed buffer, setback or synthetic point, under every option of M7-D14 (contract rule 9). R257 enforces it in data.

**R174 (N).** A base of kind `lodging` is a candidate only if the user includes lodging in `place_kinds`. M8 makes no lodging permission claim; TP6 for lodging reads that the operator's own terms apply, under an approved literal.

**R175 (N).** A candidate never combines parts from two region packages under M8-D19 (a). Under (b) or (c) it may, only through identities that survive the package boundary (continuous-explore implication 3), and the evidence of each part stays attached to its own package (implication 7).

**R176 (N).** Pairing basis (iii) uses the same straight-line function for every candidate (today's `distanceMiles`, an equirectangular approximation [MEAS E6]), and the function's basis is stated in the explanation. It is never upgraded to network or driving distance.

**R177 (N).** Assembly is deterministic: the same intent, data and injected clock produce the same candidates in the same order. Ties end on stable IDs.

**R178 (N).** Assembly is a pure function, `v2/explore/adventure.js`, taking the intent, the loaded registries, the owning evaluators and an injected clock. It reads no clock, storage or network of its own. (Engineering choice; the coordinator may rename.)

**R179 (N).** A candidate is never made to look more complete by omitting a part. All ten parts are present on every candidate detail, each either with its evidence, as ruling it out, or as not established (adventure model section 5).

**R180 (N).** Saved candidates store the intent and part IDs only. On reopening, parts are re-evaluated under the current data and clock; a part ID that no longer resolves is shown as "no longer in the source", never dropped silently (M6 PC13). No status, freshness or order is saved.

## 9. Part evaluation and ruling out

SOURCE-NEUTRAL.

### 9.1 Groups

Every candidate lands in exactly one group:

| Group | When | Shown |
|---|---|---|
| **G1 Candidates** | No reviewed restriction rules it out | First, ordered by section 10 |
| **G2 Ruled out for this trip** | At least one reviewed result rules it out (9.2) | After G1, in full, never collapsed away (M8-D8); its count is stated at the top of the results |
| **G3 Could not be evaluated** | A required interface failed to load or the search area is outside coverage (DS3, DS9) | Last, with the reason |

### 9.2 What rules a candidate out

**R181 (N).** A candidate is ruled out when, for any trip day or night, the owning evaluator returns any of: the chosen activity Prohibited for the user's class (TP2); the base Prohibited for the user's setup (TP6), including by an order provision; a reviewed vehicle constraint Excluded on an established approach (TP4); an in-force order provision that prohibits the activity or camping and that reaches the part through an established `constrained_by` link (TP8); or a stay longer than a reviewed stay limit.

**R182 (N).** A ruled-out candidate lists every restriction that rules it out, with its source, dates and review state, before anything else on it. A restriction past its review age still rules out and is flagged review overdue (trust principle 5; M7 8.6).

**R183 (N).** A candidate is never ruled out by an unknown, a not-checked coverage item, a missing record, a source text field, a management string, an ended order, or a restriction whose scope does not reach the part through an established link. A restriction of unclear scope is listed on the candidate as "may apply; scope not established" and in the orders panel (M7 OR7); it does not rule out and is never dropped.

**R184 (N).** A Restricted result keeps the candidate in G1, with every condition listed first (R151). A condition the trip cannot be checked against (for example a length limit when the user gave no length) is listed as unresolved for this trip.

**R185 (N).** A fire restriction never rules a candidate out of camping and never feeds TP6 (M7 9.6). It is shown in its own line with its jurisdiction and checked time.

**R186 (N).** Two reviewed results that disagree about one part are both shown with their sources; the part is never established from a conflict. A conflict involving a restriction is treated as the restriction for grouping (M6 AE8, M7 CE9).

**R187 (N).** An order past its stated end is listed as ended, with "a successor has not been checked" until a later review says otherwise (M7-D8 (a) or as decided). It never moves a candidate from G2 to G1 by itself being read as openness (M7 OR8).

**R188 (N).** Monotonicity. Adding a reviewed restriction to any part never moves a candidate to a better group or a higher position. Advancing the injected clock never improves any candidate's group or position. Removing a supportive record never improves either. (Property tests, section 24.)

## 10. Ordering and the explanation

SOURCE-NEUTRAL. The method is M8-D7; its material risk is M8-MR1.

### 10.1 The ordering (M8-D7 (a))

Within G1, candidates are ordered by these keys, in this order, every one of which is shown in the candidate's explanation:

| Key | What it compares | Direction |
|---|---|---|
| K1 | The set of required trip parts that are **established** for this trip (5.2): TP2 for each activity, TP3 link, TP4 approach link, TP6, TP7, TP9. A candidate whose established set strictly contains another's ranks above it | More established first |
| K2 | Where K1 sets are incomparable or equal: the number of those parts established | More first |
| K3 | Among equals: the number of parts established only with conditions | Fewer first |
| K4 | Among equals, only if the user gave a place or location: straight-line distance from it to the base, labelled as straight-line | Shorter first |
| K5 | Stable ID of the base, then of each activity feature | Lexical |

G2 is ordered by K5 only. G3 by K5 only.

### 10.2 Rules

**R189 (N).** Ordering reads only K1–K5. Coverage, relevance, source facts, source text, management strings, feature counts, popularity, region, data volume and the number of records a part carries are never ordering inputs.

**R190 (N).** A candidate never outranks another for being closer when it has a required part not established that the other has established (adventure model section 5). K4 is reached only between candidates whose K1–K3 are equal.

**R191 (N).** There is no numeric score, weight, percentage, fraction, bar, star, badge or colour for rank or completeness. Counts in K2 and K3 are never shown as "n of m"; the explanation names the parts (AP4). [REPO adventure-model section 4 rule 7]

**R192 (N).** Every G1 candidate carries an explanation in three short lines, each from approved literals with data values (M8-D10): **why it is listed** (its pairing basis per activity); **why it is in this position** (which of K1–K4 placed it above the next candidate, by part name); **what is still not established** (every required part not established, by name). The explanation adds no fact of its own (adventure model, viability explanation).

**R193 (N).** The results list states the ordering method once, above the first candidate, in one approved line, and states that order is not a recommendation and not a statement that anything is allowed.

**R194 (N).** When every G1 candidate has the same K1 set, the list says so in one line ("No candidate has more established than another"), so K4 or K5 is not mistaken for a judgement.

**R195 (N).** The first candidate is never labelled best, top, recommended or suggested; nothing is visually distinguished as first beyond its position.

**R196 (N).** A user may switch, for the current view only, between the default order and ordering by name. No other sort is offered. Switching never changes groups. (Engineering choice within M8-D7.)

**R197 (N).** The ordering function is pure and separately testable from assembly, with a published key table matching 10.1 (section 24).

**R198 (H).** The reviewed records that make parts established are chosen for review by a rule recorded in the M4–M7 delivery plans, not by which candidates would rank first; M8 adds no review queue. M8-MR1 records why.

## 11. Empty and degraded states

SOURCE-NEUTRAL.

| ID | State | What the user sees (constraints; literals approved later) |
|---|---|---|
| DS1 | Intent incomplete (no activity, invalid dates) | The field to fix; no candidate list; the map stays usable |
| DS2 | No relevant activity feature in the search area | "Ohvernight found no [activity] feature in its data for this area"; that this does not mean there is none; a link to the open map; the region's limitations |
| DS3 | A required interface failed to load | The affected part reads not established on every candidate, with a retry for that file; candidates that need it for grouping go to G3 |
| DS4 | An interface not yet delivered (M5–M7 not merged) | One line naming the evidence the region does not yet have; every dependent part reads not established. This is the expected state at M8-B |
| DS5 | No base of the chosen kinds | Says so; offers to include other kinds; never offers a day-use place for an overnight need |
| DS6 | Every candidate ruled out | G2 in full with each restriction; a line that other dates, setups or vehicles change the answer; never "nothing is available" |
| DS7 | Every candidate has the same established set | R194 line |
| DS8 | All reviews past age | Each stale restriction still rules out and is flagged; each stale supportive answer reads not established with its date |
| DS9 | Search area at or beyond the coverage edge | One line that Ohvernight has no data beyond the edge; candidates whose straight-line bound crosses it say the far side was not searched (continuous-explore, uncovered-area behaviour) |
| DS10 | Activity not supported in the region | The activity is shown as having no Ohvernight data in this region, not as unavailable |
| DS11 | Geolocation refused or outside coverage | Planner continues with the region; outside coverage reads as DS9 |
| DS12 | Storage unavailable | Intent works for the session; a line that it will not be kept |
| DS13 | Cap reached | The cap line of 8.3 step 8 |

**R199 (N, B).** No empty or degraded state uses "none", "nothing here", "no restrictions", "all clear", "unavailable" (of a place) or "closed" as its message about a place or area.

**R200 (B).** Every empty or degraded state keeps the "Explore the map" action visible (section 17).

**R201 (N).** A degraded state never hides a candidate that can be assembled; it marks the affected parts.

**R202 (N).** DS4 and DS9 are distinct from DS2: "not delivered", "outside coverage" and "searched, nothing found" are three different messages.

**R203 (B).** A failed registry has an independent retry, as M3 layers do; retrying re-runs assembly.

**R204 (N).** The planner works with zero M5–M7 registries present, producing candidates whose parts beyond TP1 and TP5 all read not established (DS4). This is tested on both regions (section 24).

## 12. LOCKED — Day-use base (Scenario B)

**This section chooses nothing.** Scenario B asks for a rider's staging point and a family's day-use place, with a link between them, and no overnight stay. [DRAFT-PR 20] Whether M7 delivers a `day_use_site` kind with `use_period` is M7-D16, which is open. [DRAFT M7 24.2]

### L13. Interface and decision needed

| Needs | From | Decision |
|---|---|---|
| `day_use_site` kind and `use_period: day_use` | M7 7.1 | M7-D16 |
| Day-use answers for the family (picnic, hammock as its own question), restriction-first | M7 8.1 `hammock`, 8.5 CE13 | M7-D3, M7-D16 |
| Staging → day-use place link | M7 RL14 composition | M7-F, L9 |
| Separate party profiles (rider and family) | M8-D16 | M8-D16 |

The rules that hold whichever way M7-D16 falls:

**R205 (N).** A day-use place never satisfies an overnight base, and an overnight place is offered as a day-use base only where its own reviewed record states day use. [DRAFT M7 CE13]

**R206 (N).** Where no reviewed source settles hammock use, the candidate says exactly what Scenario B requires: `Hammock use: Not established from reviewed sources.` (pending owner approval as an M8 literal; Scenario B states it). Trees being present establishes nothing. [DRAFT-PR 20]

**R207 (N).** The link between a staging point and a day-use place is a vehicle-route composition (RL14) unless a source states a walking link; a road edge is never a walking path, and a walking link is not established by distance. [DRAFT-PR 29 gap 9]

If M7-D16 is (b), `base: day_use` is not offered in M8 and Scenario B is run as supplementary with step 5 recorded as not possible in Ohvernight.

## 13. LOCKED — Staging, approach, `relevant_to` and backup parts

**This section chooses nothing.** TP3, TP4, TP7 and TP9 depend on trailhead identity and `starts_at` (M6, L5 and the M6 source policy, or M6-D2), on road designations and `approached_via` (M7-F, L9), on the shared vehicle vocabulary (M7-D11, M6-D11), and on the backup predicate (M7 RL15).

### L14. Interface and decisions needed

| Part | Reads | Decisions |
|---|---|---|
| TP3 | `starts_at` links trail → site, origin and evidence | M6 L2, L5; M6-D2; M6-D16 |
| TP4 | `approached_via` links; constraint results for profile and dates | M7 L9; M7-D11; M7-D2 |
| TP7 | `relevant_to(place, trail or trailhead, profile)` → established, or unknown with the missing link named | M7 RL14 |
| TP9 | `backup(place, trip)` → place with basis, or absence with reason | M7 RL15 |

Rules that hold whichever way those decisions fall:

**R208 (N).** M8 calls `relevant_to` and `backup` as M7 provides them and never computes either itself. Until they are delivered, TP7 reads not established and TP9 reads "No independent backup is established", never "none exists".

**R209 (N).** TP4 is never positive. Where every reviewed constraint passes, the candidate names what was checked and says vehicle suitability is not established (M7 CP10).

**R210 (N).** A user's saved alternate is the user's choice, labelled as such; the word "backup" is reserved for a TP9 result. (Replaces PB8.)

**R211 (N).** RL18 (staging before approach). Where TP3 is not established, TP4 for the activity side reads not established, because no approach can be attached to an unidentified staging point.

**R212 (N).** A trailhead that M6 does not identify is never created from a trail end point, a parking area, a road junction or a Douglas `TRAILHEAD` record's proximity to a trail (M6 10.2). [DRAFT M6]

## 14. LOCKED — Land and jurisdiction lines

**This section chooses nothing.** Which land unit identities exist depends on M5-D6 (PAD-US terms; M5 PR C conditional), whether management coverage is shown on M5-D13 / R1, and whether trails relate to units on M6-D10. [DRAFT M5 20] [DRAFT M6 22.2]

### L15. Interface and decisions needed

| Line | Reads | Decisions |
|---|---|---|
| Governing unit of TP1, TP3, TP5 | `governed_by` from the entity's own source field (M5 rule 1, M6 RL7, M7 RL12) | M5-D6, M6-D10, M7 RL12 |
| Management review | `land-coverage.json` `management` record | M5-D13 / R1 |
| Access | Always "Access: not reviewed" (LW8 if approved) | M5 R1 |

**R213 (N).** Every candidate that crosses or stages on land lists access as not reviewed until a later milestone specifies access review (M5 rule 3). [DRAFT M5 10] Containment in a land polygon is shown as context only and never relates a part to a unit.

**R214 (N).** A management review never improves a candidate's group or order (R189) and never appears beside a status word.

## 15. LOCKED — Getting there

**This section chooses nothing.** Scenario B's "origin → route → entrance" chain and its "closest means practical driving" rule need a routing source with a road network and terms the owner has read. None is proposed or approved. [DRAFT-PR 20] [DRAFT-PR 15 ranking-architecture-options, "Drive tolerance": UNKNOWN]

### L17. Interface and decision needed

> **Which routing or road-network source, if any, may establish a driving route or time between a stated origin and a staging point, under which terms reading?**

Until it is decided (M8-D15):

**R215 (N).** Every candidate shows "Driving route and time: not established", and no distance on any candidate is called driving, travel or closest.

**R216 (N, H).** The existing outbound directions link is kept with its existing wording that directions may not reflect closures or permission to use the approach. [MEAS E6] It opens an external site and is counted as one by the scenario tester.

## 16. OWNER DECISION — Continuous geographic Explore (M8-D19)

The roadmap reserves this choice for the owner when M8 is specified. [REPO ROADMAP M8; continuous-explore.md, "Likely milestone"] This draft sets out the options and their consequences. It does not recommend one.

### 16.1 Facts that bear on it

- Explore loads exactly one region package per page load; the loader refuses other regions' paths, by design (M3). [REPO continuous-explore CURRENT]
- The two pilot extents are about 107 km apart and do not touch, so no candidate can combine Aspen and Douglas parts. [MEAS E12] A cross-package candidate arises only with a third, adjacent package, or where a real-world feature continues past one package's own edge (the Douglas trails are clipped to the county). [REPO system-overview, deferred areas]
- M5, M6 and M7 drafts each keep identities that survive a package boundary (M5 7.2, M6 7.3, M7 EI6); none is approved. [DRAFT M5] [DRAFT M6] [DRAFT M7]
- A continuous surface needs a coverage index, a cross-package search index and per-view budgets (continuous-explore implications 2, 5, 6), and is a likely moment for the ADR-006 reopening triggers to be evaluated. [REPO]

### 16.2 Options

| Option | What M8 does | What changes elsewhere | Main cost | Main risk |
|---|---|---|---|---|
| **(a) Not in M8** | One package per page load. The search area stops at the package edge; DS9 says so on every affected candidate. Continuous Explore becomes a later milestone | ROADMAP gains a post-M8 entry (its own PR) | None now | Users near an edge get candidates that silently stop at it, mitigated only by the DS9 line; R-4 stays unmet |
| **(b) Coverage index and cross-package search only** | A small, always-loaded coverage index of packages, extents and per-kind coverage; search across packages that switches the page to the chosen package; on-map "no coverage" indication. Candidates stay within one package | Loader gains a coverage-index read (a narrow M3 amendment); no change to the path restriction for feature data | Small–medium | The two pilots gain little (they are not adjacent); value appears only with a third region |
| **(c) Full continuous Explore in M8** | One map; packages loaded lazily as the user pans or searches; candidates may combine parts from adjacent packages through boundary-surviving identities; per-view budgets | M3 loader restriction replaced by an approved amendment; budgets re-specified per view; ADR-006 triggers evaluated | Large; probably the largest part of M8 | Couples M8 to every M5–M7 identity decision and to the renderer decision; delays the planner |
| **(d) A separate milestone before M8** | M8 as (a) or (c), but continuous Explore is specified and delivered first as its own milestone | ROADMAP order changes (owner PR) | Schedule | Moves the planner, the roadmap's stated M8 outcome, later |

### 16.3 Rules that hold under every option

**R217 (N, B).** An uncovered area reads as unknown, never as empty or unrestricted, and is visibly distinct from a covered area with no feature of a kind (continuous-explore, uncovered-area behaviour).

**R218 (N).** A candidate never silently stops at a coverage edge: a dependency outside coverage is listed as not established (DS9).

**R219 (N).** Evidence does not merge across packages: each part's fact coverage, limitations and source statements stay those of its own package (continuous-explore implication 7).

## 17. Explore Map as the free-discovery alternative

SOURCE-NEUTRAL. Product principle 2. [REPO]

**R220 (B).** "Explore the map" is one tap from the landing, from the intent editor, from every results state and from every candidate detail. It closes the planner surfaces and leaves the map with every layer at its own switch.

**R221 (B).** Opening Explore requires no intent. Entering with `&view=map` skips the planner, as today. [REPO system-overview]

**R222 (B).** Selecting a candidate highlights its parts on the map using the adapter's existing `setSelected` per layer, and fits them with sheet-aware padding under the existing camera policy, including the M4 O6 fit cap for water and the M6 cap for trails where approved. No adapter export is added (M3 8.1). [REPO]

**R223 (B).** Tapping a map feature while a candidate is open shows that feature's own detail with Back to the candidate; it does not add it to the candidate.

## 18. Mobile-first interface

SOURCE-NEUTRAL. Built on the M3 shell and the PR #39 sheet structure: the sheet header in normal flow with one scrolling body, three states (collapsed, half, expanded), shared drag and snap gestures, and Back to the retained list and scroll position. [MEAS E10] [REPO M3 section 11, A11, A13, A14]

### 18.1 Surfaces

| Surface | Where | Content |
|---|---|---|
| Landing | Existing landing element | Intent form (6.1), "Find candidates", "Explore the map" |
| Intent summary | Sheet header, every state | One line: where, dates, activities, base and setup, vehicle; one tap opens the editor |
| Intent editor | Existing dialog pattern | The 6.1 fields; Escape and close return focus |
| Results | Sheet body (`list-body`) | Ordering line (R193), counts of G2 and G3, G1 candidate cards, G2, G3 |
| Candidate card | Results | Base name and kind; activity feature per activity; the restriction or condition line first if any; the three explanation lines (R192) |
| Candidate detail | Sheet body, Back to results | Section order in 18.2 |
| Orders panel | M7's panel | Reachable from every candidate detail (M7 CP8) |

### 18.2 Candidate detail order

Follows Scenario B's expected answer shape, without its "Best plan" heading (R195). [DRAFT-PR 20]

1. Restrictions and conditions that apply (G2 reasons first, then Restricted conditions, then "may apply" orders), each with source, dates, review state.
2. Why this is listed and why in this position (R192).
3. Activity part per activity: feature, then the activity result for the class and dates (TP1, TP2), then parts disclosure (R163).
4. Staging and approach (TP3, TP4) and Getting there (R215).
5. Base and its answer for the setup (TP5, TP6); for day use, section 12.
6. Link between base and staging (TP7), with the missing link named.
7. Backup (TP9) or its stated absence.
8. Fire line (R185).
9. Land lines (TP10).
10. Still not established: every unestablished part, by name (repeats the third explanation line in full).
11. Coverage list per part (checked or not checked, with dates; never a score).
12. Sources and evidence: per part, source, agency, retrieval and review dates (M3 shared evidence presentation).
13. The fixed lines of each owning milestone (M4 WW2, M6 trail line, M7 CP5).

### 18.3 Requirements

**R224 (B).** The M3 free-map, touch-target, sheet-height, drawer, keyboard and reduced-motion requirements hold unchanged with the planner open at 320×568, 390×844, 768×1024 and 1440×900, and in phone landscape. [REPO M3 section 11]

**R225 (B).** The intent summary fits on one line at 320 px or wraps to at most two without truncating any field's value; it is part of the sheet header and is reachable and operable in the collapsed state.

**R226 (B).** Results and candidate detail live in the one scrolling sheet body; no nested scroll container is added (PR #39). [MEAS E10]

**R227 (B).** Back from a candidate detail returns to the results with their scroll position and the same intent; Back from a feature opened from a candidate returns to the candidate (R223).

**R228 (B).** The restriction or condition line of a card is visible without expanding the card, at 320 px, in the half state.

**R229 (B).** Every candidate card is one focusable control with an accessible name containing the base name, the activity features and, if ruled out, that it is ruled out.

**R230 (B).** Opening the intent editor closes the layer drawer on phones, as the sheet does today.

**R231 (N, B).** "Not established" lines are never hidden behind an expander on the card or in the detail; evidence detail (sources, coverage) may be collapsed (product principle 14).

**R232 (B).** The planner adds no permanent obstruction to the map; after closing every planner surface the default-state free-map thresholds of M3 section 11 hold.

**R233 (H).** An iPhone Safari check of both regions by the owner gates every PR that changes what the user sees (M3 A13 release evidence).

## 19. Presentation and trust-wording constraints

SOURCE-NEUTRAL. These are constraints, not strings. **Exact literals are deferred to the owner** (M8-D13): drafted in the pull request that first renders them, approved by the owner there, and then pinned byte for byte by tests, as M4 section 10 and the M5–M7 drafts do. Literals owned by M4–M7 are reused unchanged and never reworded by M8. Trust-bearing manifest wording changes only with owner approval (trust principle 8). The Aspen landing strings are presentation configuration in `explore.json` and are replaced only by owner-approved literals.

| Requirement | Constraint |
|---|---|
| **R234 (N)** AP1 Few and short | At most 20 new fixed strings in M8, excluding part labels and reused M4–M7 strings. A line at most 90 characters; a label at most 32; every string fits at 320 px in the sheet without truncation |
| **R235 (N)** AP2 Forbidden words | No new string contains "verified", "legal", "permitted", "open", "available", "safe", "suitable", "best", "top", "recommended", "closest", "nearby", "connected", "guaranteed" or "current" used of status, except where it states that something is *not* established (M3 A4) |
| **R236 (N)** AP3 Status never alone | A status word is shown with its activity and class, its setup, or its vehicle class (M6 PC3, M7 CP3). "Trip", "candidate" and "adventure" are never the subject of a status word |
| **R237 (N)** AP4 No score | Rank and completeness are never shown as a number, fraction, percentage, bar, star, badge or colour (R191) |
| **R238 (N)** AP5 Restrictions first | On cards and in detail: prohibitions, then restrictions and conditions, then established answers, then not established (M6 PC5, M7 CP4) |
| **R239 (N)** AP6 Pairing basis named | Every pair shows its basis; basis (iii) shows its distance as straight-line and that a connection is not established (R170) |
| **R240 (N)** AP7 Unchecked inputs stated | Where a chosen input has no reviewed evidence in the region, one line says so (R160) |
| **R241 (N)** AP8 Order disclaimer | One line above results states the method and that order is not a recommendation or permission (R193) |
| **R242 (N)** AP9 No "plan" certainty | A saved candidate is "saved", never "planned", "booked" or "confirmed"; saving says it does not confirm suitability or availability (existing wording kept) [MEAS E6] |
| **R243 (N)** AP10 Empty states | Empty and degraded messages follow section 11 and R199 |
| **R244 (N)** AP11 Backup reserved | "Backup" appears only for a TP9 result (R210) |
| **R245 (N)** AP12 Day use labelled | A day-use base carries its day-use label; it is never counted or titled as an overnight option (M7 CP17) |
| **R246 (N)** AP13 Ruled out is not hidden | G2's heading and count appear above G1; G2 is listed in full |
| **R247 (N)** AP14 Map has no candidate status | No candidate colour, rank number, pin badge or status symbol on the map (follows M4 O3, M6-D13, M7-D17); the selected candidate uses the existing selection styling |
| **R248 (N)** AP15 Distances | Every distance shown says straight-line; none is a time |
| **R249 (N)** AP16 Explanation from literals | The three explanation lines (R192) are built from approved literals plus data values only; no free-form generated text |

## 20. Retiring the pilot planner

SOURCE-NEUTRAL. The roadmap records that the Aspen pilot keeps "unchanged inputs/ranking" until M8. [REPO system-overview] This section lists every pilot behaviour M8 replaces, with file and line, and its disposition. None of them grants permission; their wording is careful about straight-line distance. The problem is that they are not assemblies, they order by nearness, and their intent controls are buried or region-specific.

| ID | Where | Behaviour | Disposition (PR) |
|---|---|---|---|
| PB1 | `v2/regions/aspen/explore.json` `landing` | "Choose your adventure." with a straight-line lead | Replaced by owner-approved landing literals for the shared planner (M8-B) |
| PB2 | `v2/trail-discovery.js:33-38` `adventureOptions` | Places × trails within 5 straight-line miles, up to 3, by source management strings | Replaced by assembly (section 8); `adventureOptions` removed once no caller remains (M8-C) |
| PB3 | `v2/trail-discovery.js:37`; `v2/explore/capabilities.js:90` | Excluded last, then nearest | Replaced by groups and K1–K5 (sections 9, 10) (M8-C) |
| PB4 | `v2/explore/capabilities.js:43` | Dialog "Camping and trails by straight-line distance" | Retired; candidates live in the sheet (M8-C) |
| PB5 | `v2/explore/capabilities.js:53-55` | "Mountain" select of 4 resorts as the only location input [MEAS E3] | Destinations become named places in `where` (6.1); stored resort migrates to that place (M8-C) |
| PB6 | `v2/explore/capabilities.js:32` | Three vehicle keys | The L12 vehicle vocabulary (M8-B) |
| PB7 | `v2/explore/capabilities.js:83-86` | "What has been checked?" region summary | Per-candidate coverage list (18.2 item 11); region fact coverage stays in "Access & coverage notes" (M8-C) |
| PB8 | `v2/explore/capabilities.js:89` | Saved slots headed "PLAN A" and "BACKUP" | "Saved" candidates and the user's alternates; "backup" reserved (R210, R244) (M8-C) |
| PB9 | `v2/explore/capabilities.js:87` | Stay type inside collapsed "Filters" | `place_kinds` in intent (6.1) (M8-C) |
| PB10 | `v2/explore/browse.js:27-33` | Douglas activity, dates, vehicle in collapsed "Filters" | Douglas Browse reads the shared intent; the fields move to the intent editor; Browse stays as the free-discovery list (M8-D12) (M8-C) |
| PB11 | `v2/explore/browse.js:54,58`; `v2/explore/capabilities.js` trail detail | Straight-line listings under details | Kept, with their wording and "connection unverified" marking (M6 PC14, M7 CP14); they are not candidates and never feed assembly |
| PB12 | `v2/explore/capabilities.js:117` | Outbound directions link | Kept (R216) |

**R250 (N).** The planner stores intent and saved candidates only (R180); the pilot's stored `trip` and `plan` values migrate on read: resort → named place; vehicle keys kept or "not chosen"; saved `plan.a`/`plan.b` place IDs → saved bases without an activity part, which the user completes. An unrecognised value is dropped with a one-line notice, never mapped to a default.

**R251 (N).** Douglas stored trips migrate as M7 12.3 specifies for vehicles; dates and activity keep their keys. Douglas saved trail and site IDs, notes and GPX export keep working unchanged.

**R252 (N).** No capability flag is removed until both regions run the shared planner; `trip_planner` and `adventure_pilot` are replaced by one `adventure_planner` capability (21).

**R253 (N).** The straight-line listings of PB11 keep their wording byte for byte unless the owner approves a change in the PR that renders it.

**R254 (N).** Every existing assertion about the pilot that protects trust behaviour (rule ordering, staleness, "Saving a place does not confirm…") is carried to a test of the new planner before the old code is deleted; none is dropped (M7 12.3 pattern).

## 21. Contract and configuration changes

All additive. M8 adds no data registry and no canonical data.

| Change | PR | Label |
|---|---|---|
| `explore-config.schema.json`: capability `adventure_planner` (replacing `trip_planner` and `adventure_pilot` after M8-C); an optional `adventure` block with presentation literals and the search-bound value of M8-D6 | M8-A (schema), M8-B (Aspen), M8-C (Douglas, retirement) | NEUTRAL |
| `trip_defaults` gains `base`, `setup`, `place_kinds`, `towing`; keeps existing keys | M8-B | NEUTRAL |
| Contract documentation: an M8 section stating that M8 reads, and never writes, the M4–M7 registries; the R257–R262 rules | M8-A | NEUTRAL |

**R255 (V).** Configuration carries presentation and the search-bound value only. No status, claim, evidence, limitation or coverage statement is in `explore.json` (M3 10.2).

**R256 (V).** The `adventure` block's literals are closed-schema keys with owner-approved values; tests compare them to literals.

## 22. Validator rules

Stable rules for the few M8 facts the validator can see. Each has a negative fixture and, where it protects real data, a mutation proof (local, not committed).

| ID | Rule | PR |
|---|---|---|
| **R257 (V)** | No region manifest lists a `research_areas` layer or any computed overnight geometry among the inputs the `adventure_planner` capability reads; the planner's input set is a closed list in the schema (R173) | M8-A |
| **R258 (V)** | `explore.json` `adventure.search_bound_miles` is a positive number not greater than the value approved under M8-D6 | M8-A |
| **R259 (V)** | No published feature, place, registry record or configuration carries a property named for a candidate, rank, score, order, pairing or `relevant_to` (the M4 R75 pattern) | M8-A |
| **R260 (V)** | A region with `adventure_planner` declares the base kinds it offers, each one that M7 defines (or, before M7-C, one of the published inventory kinds) | M8-B |
| **R261 (V)** | `trip_defaults` values are in the approved vocabularies or "not chosen" | M8-B |
| **R262 (V)** | After M8-C, no manifest declares `trip_planner` or `adventure_pilot` | M8-C |

## 23. Budgets and performance

Inherited unchanged from M3 (section 16, A10, A13) and M4 (section 14), and as the M6 and M7 drafts restate them:

| Measure | Limit |
|---|---|
| Bytes to "map usable", per region | 500,000 |
| Bytes with every default-on layer, per region | 4,500,000 |
| Region default-on set | ≤ 15,000 features and ≤ 1,500,000 bytes gzipped |
| One display layer | ≤ 5,000 features and ≤ 450,000 bytes gzipped, or `min_zoom`, or split |
| Performance | Map usable ≤ 60% and all default-on layers ≤ 135% of the same-session base median; heap ≤ 115% of base; triggers R-1 to R-5 unchanged |

M8-specific (M8-D14):

| Requirement | Measure | Today | Limit |
|---|---|---|---|
| **R263 (B)** | Bytes before "map usable" added by M8 | — | 0. The planner module and registries it reads are not requested before map usable |
| **R264 (B)** | Planner modules (`adventure.js` and its interface code), unminified | Pilot `capabilities.js` 15,687 and `trail-discovery.js` 2,611 [MEAS E7] | ≤ 25,000 bytes combined for new planner code; the pilot code it replaces is removed in M8-C |
| **R265 (B)** | Registries requested on entering the planner | — | Only those the intent needs; each at most once per page load; within the M7 cap of 150,000 bytes raw per region for overnight registries [DRAFT M7 17] |
| **R266 (N)** | Assembly and ordering time, median of five runs at 4× CPU on the largest fixture (30 bases × 150 activity features × 2 activities) | — | ≤ 150 ms, local, reported; a miss is reported, not tuned around |
| **R267 (B)** | Douglas initial index | 3,709 bytes [MEAS E8]; headroom small [REPO M4 A2] | Nothing planner-related is added to `index.json` |
| **R268 (N)** | Candidate count | — | ≤ 30 per trip; each base in ≤ 3 candidates (8.3 step 8) |

No pipeline-built pair table is added: results depend on view-time freshness and trip dates, so a precomputed table would freeze them. [DRAFT-PR 15 ranking-architecture-options D] If R266 is missed, a pipeline-built index of candidate pairings by ID only, with no status, is the fallback, by specification amendment. Three sessions of the unchanged `measure.mjs` are run at the M8-B and M8-C heads, reported pass or miss.

## 24. Tests

Offline, clock-free, nothing written inside the repository, as M3–M7.

**Node (assembly and ordering, injected clock, synthetic fixtures for M5–M7 interfaces until they are delivered):**

- Interfaces: with no M5–M7 registries, both regions assemble candidates whose parts beyond TP1 and TP5 read not established (R204); a failed registry gives DS3 with the named part; an empty registry is not "checked" (R166).
- Ruling out: a trail Prohibited for `motorcycle` on one trip day → G2 with the claim; Prohibited for `atv` only → no effect on a `motorcycle` trip; a setup Prohibited by an order provision through an established `constrained_by` → G2; the same order with no link → "may apply" and G1 (R183); an overdue prohibition → G2 flagged; an overdue Allowed → not established (R151); departure day alone inside a prohibition → G2 (R157); a fire restriction → shown, no G2 (R185); conflicting claims → restriction wins (R186).
- Ordering: K1 superset wins regardless of distance; a nearer candidate with fewer established parts never outranks (R190); equal K1 → K2, K3; K4 only with a stated origin; ties on K5; switching to name order never changes groups (R196).
- Properties (R188), generated over fixtures: adding a restriction never improves group or position; advancing the clock never improves; removing a supportive record never improves; moving a base closer changes nothing but K4; adding a coverage record, a source management string or a source text field changes nothing (R152, R189); determinism across 100 shuffles of input order (R177).
- Pairing: basis (i) beats (ii) beats (iii); basis (iii) label always present (R170); no pair outside the search area; no pair across packages under M8-D19 (a) (R175); research-area features never used (R173).
- Relevance: a trail with only a management string is relevant and shows no status (R172); a name match alone is never relevant.
- Day use (with fixtures, LOCKED shape): a `day_use_site` never satisfies overnight (R205); hammock line exact (R206).
- Backup and `relevant_to`: called, never computed; absent → stated absence (R208); user alternate never labelled backup (R210).
- Intent: unknown stored values become not chosen (R155); geolocation never written to storage (R156); migration of Aspen `trip`/`plan` and Douglas trips (R250, R251).
- Wording: every approved literal against its string; no output contains an AP2 term outside an approved negated string; no output contains a digit followed by "of" for rank or a percent sign (R191, R237); status words always with their subject (R236).
- Carried assertions from the pilot tests (R254).

**Python (validator):** a negative fixture for each of R255–R262.

**Browser check (both regions, four sizes and phone landscape):** M3 section 11 measures with the planner open and closed (R224, R232); the intent summary in the header at every sheet state (R162, R225); one scrolling body (R226); Back paths (R227); restriction line visible on a card at 320 px half state (R228); "Explore the map" in every state (R220); `&view=map` skips the planner (R221); candidate selection highlights parts with no new adapter export (R222); no planner request before map usable (R263); a forced registry failure shows DS3 with a working retry (R203); map geometry unchanged by intent (R159).

**Mutation proofs (local):** add a `rank` property to a place; point the planner at a research-area layer; set the search bound above the approved value; reorder K1 and K4 in the key table; make the planner read `management` strings as TP2; drop G2 from the rendered list. Each must fail its named requirement.

## 25. Acceptance

**Engineering, per PR:** offline suites and the browser check pass; display rebuild has no diff; each new rule passes on real data with negative fixtures and mutation proofs; budgets hold; three performance sessions reported where code on the load path changes; property tests pass.

**Owner gates:** each PR's exact head SHA approved by the owner; every literal approved in the PR that renders it; iPhone Safari check of both regions for M8-B, M8-C and every LOCKED PR that changes what the user sees (R233).

**Scenario acceptance (milestone close), run on a phone by a dedicated tester who implemented no M8 PR:**

1. **Scenario A, Douglas dirt-bike weekend** [REPO]. Every measure recorded against the previous result. Source-neutral predictions to be tested, not results: the tester reaches a candidate list from intent without opening Browse filters; each candidate names its pairing basis, and the proximity-assumption count does not rise; step 2 (motorcycles allowed) improves only where M6-E records exist, otherwise reads correctly unknown on the candidate; steps 3, 4 and 6 improve only where M6-F and M7-F links exist, otherwise each is named as not established on every candidate; step 7 shows reviewed orders where M7-D records exist and "not checked" otherwise; step 9 is answered on every candidate by its "still not established" line; time to a viable trip and planning steps are expected to fall even where unknowns remain, because the unknowns are collected on one card instead of found across screens [INF].
2. **Scenario B, Rampart family day use** [DRAFT-PR 20]. Run as canonical if PR #20 is merged before M8 closes, otherwise once as a supplementary scenario. The owner's "Target by M8" is reported line by line as met, partly met or not met, with the dependency that blocks each line; it is never met by weakening evidence. Source-neutral expectations: if M7-D16 (a) is delivered, the family base is a day-use place with its own restrictions and never an overnight option; the hammock line reads exactly as R206 unless a reviewed page settles it; "closest" is never shown, and Getting there reads not established (R215); current-status lines show only reviewed orders and fire records with checked times; a backup is a TP9 result or its stated absence.
3. **Aspen supplementary scenario (this specification only; not canonical).** "A summer weekend near Aspen: hike and fish, tent, passenger car, no towing." Fixed: an Aspen named place as `where`, dates in July of the run year, recorded familiarity. Source-neutral expectations: water candidates are any M4-displayed water, with fishing established only where an M4-C record exists, and Cheesman-style prohibitions ruling out; no computed research area appears as a base under any option (R173); a tent-only place is not ruled out for `tent` (the M7 H2 correction) and its vehicle-sleeping answer is not offered as the tester's; a high-clearance restriction carried by M7 12.4 rules out the passenger car with "review overdue" if past age. The result is recorded in the M8 product review only; adding it as a canonical scenario needs its own pull request (scenario A, "Keeping it stable").
4. **Unknowns are not hidden.** No scorecard line improves by hiding an unknown. "Candidate trips with a viable overnight option" and "with a backup option" are reported, for the first time, as shares of candidates for each scenario intent, each beside the unknowns its candidates list (product scorecard). [REPO]
5. The coordinator writes the product review under its six headings and states plainly what M8 delivered on the data M4–M7 actually provided, if that is less than this specification describes.

## 26. Delivery plan

Small sequential pull requests on Aspen and Douglas County only. Each is independently revertible, leaves `main` green, keeps app, pipeline and data changes in separate commits, and needs owner approval of its exact head SHA. **NEUTRAL** PRs can start once this specification is approved and the M8-D2 start gate is met. **LOCKED** PRs cannot start until the named decision is made and the interface delivered.

| PR | Content | Label | Visible change |
|---|---|---|---|
| **M8-A** | `adventure.js` assembly and ordering as pure functions on synthetic fixtures for DI1–DI10; property tests; schema and contract text of section 21; R257–R259; no UI | NEUTRAL | None |
| **M8-B** | Shared planner UI in Aspen (behind `adventure_planner`): landing, intent summary and editor, results, candidate detail, degraded states; reads whatever M4–M7 registries exist (DS4 otherwise); R260, R261; owner-approved literals | NEUTRAL | Aspen planner replaced by candidates; most parts read not established |
| **M8-C** | Douglas planner; Douglas Browse reads shared intent; Aspen pilot retired (PB2–PB10); storage migration; R262 | NEUTRAL | Douglas gains the planner; Filters fields move to intent |
| **M8-D** | Wire DI4–DI6 as M6 delivers them: trail identity and parts (L16), trail claims, `starts_at` (TP3) | **LOCKED** (M6-D2 or M6 source policy; M6-D4; L5) | Trail parts and staging established where records exist |
| **M8-E** | Wire DI7–DI9 as M7 delivers them: setup answers, orders, constraints, `relevant_to`, backup; day-use base if M7-D16 (a) | **LOCKED** (L13, L14; M7-D2, M7-D3, M7-D11, M7-D16; M7 L7–L10) | Base answers, restrictions, backup lines |
| **M8-F** | Land lines (L15) as M5 delivers them | **LOCKED** (M5-D6, M5-D13 / R1, M6-D10) | Management lines; access not reviewed |
| **M8-G** | Continuous Explore work under M8-D19 (b) or (c) only | OWNER DECISION | Per option |
| close | Scenario runs and product review (section 25) | NEUTRAL | — |

If M5–M7 deliver little, M8-A to M8-C still ship and the review says plainly that most parts read not established and why (M8-D17).

## 27. Rollback

- **M8-A:** revert. No visible change.
- **M8-B / M8-C:** revert. The pilot planner and Browse filters return; stored intent written in the new shape is read by the old code as defaults, reported in the PR as the rollback cost. Saved Douglas trail and site IDs are untouched.
- **M8-D / M8-E / M8-F:** revert; the affected parts read not established again (DS4).
- **A wrong candidate:** M8 holds no data, so a wrong candidate is fixed in the M4–M7 record that caused it, under that milestone's rules. A restriction is never removed to improve a candidate (trust principle 5).

## 28. Risks

Engineering risks with their mitigations. The material risks the owner should weigh are in 30.4.

| Risk | Mitigation |
|---|---|
| The planner re-implements a claim evaluation and drifts from its owner | R150, R164; tests call the owning evaluators |
| A straight-line pairing reads as a connection | R170, R239, R248; Scenario A proximity count |
| Ordering rewards nearness | R190 and property tests |
| An unknown silently improves a candidate | R188 monotonicity properties |
| A registry fails and parts read as fine | R165, DS3 |
| Intent leaks into data or storage beyond the trip key | R154, R156 |
| The planner crowds the map on phones | R224, R232; device check |
| Assembly too slow on a phone | Cap (R268), budget (R266), fallback index by amendment |
| Pilot trust assertions lost in retirement | R254 |
| Research inputs treated as truth | Every [DRAFT-PR] item is input only; M8 adds no evidence |

## 29. Unknowns

Stated as unknown; none blocks approval of the source-neutral sections.

- Whether M5, M6 and M7 are approved as drafted, and which of their open decisions fall which way (sections 12–15 wait on them).
- How many reviewed records M4-C, M6-E and M7-E deliver per region, and so whether ordering will discriminate at all at M8 close (M8-MR2). [UNK]
- Whether users read position one as a recommendation regardless of the ordering line. [DRAFT-PR 15] [UNK]
- Whether a 5-mile straight-line search bound is too tight or too loose for the pilots' terrain. [UNK]
- Whether any routing source is usable on a static site under acceptable terms (L17). [UNK]
- Whether the Rampart trail system continues past the Douglas county line in a way a candidate would need (M8-D19). [UNK]
- Whether PR #20 (Scenario B) is merged before M8 closes.
- Whether 20 new strings (R234) are enough.
- Assembly time on a real mid-range phone; R266 is measured with CPU throttling only.

## 30. Owner decision packet

One packet. The owner can acknowledge 30.1 explicitly (silence is not approval), accept 30.2 in one reply, must choose 30.3 explicitly (no default is offered), and should read and answer 30.4 separately. 30.5 lists engineering choices decided in the body, which need no answer. A recommendation is the coordinator's proposal only.

### 30.1 Settled by default (no decision needed; already binding)

1. Unknown is the default and is shown as unknown (trust principle 1, contract rule 1).
2. Never infer permission, access, a relationship or suitability from a listing, ownership, management, a mapped road or trail, or proximity (trust principle 2; contract rules 12 and 15; product principle 12).
3. Staleness never weakens a restriction; positive claims fail closed (trust principles 5 and 6).
4. Presentation, including ordering and ranking, never exceeds the evidence; trust-bearing wording changes only with owner approval (trust principles 7 and 8).
5. M8 assembles candidates from M4–M7 identities, evidence and relationships, is not filters on the map, and lists every candidate's unknowns (ROADMAP M8).
6. A candidate never outranks another merely for being closer when it has an unknown the other has established; a candidate is never made to look complete by omitting its unknowns (adventure model section 5).
7. Explore Map remains the free-discovery alternative (product principle 2, ROADMAP M8).
8. No community or third-party content; no availability claim (M4 D8; M7).
9. Budgets and performance limits inherited from M3 and M4.
10. PAD-US, COTREX and RIDB expansion stay locked; M8 selects no source.
11. Milestone close requires a phone run of the canonical scenario by an independent tester and the six-heading product review.
12. No merge without the owner's approval of the exact head SHA; no ROADMAP, trust-principle or contract-rule change outside its own approved pull request.

### 30.2 Recommended defaults (acceptable in one reply)

| ID | Decision | Options | Recommendation | Bear case against it |
|---|---|---|---|---|
| M8-D1 | Scope and delivery | (a) PRs M8-A to M8-F on Aspen and Douglas only, neutral first; (b) one combined PR after M7 closes | (a) | Up to six gates and five device checks; owner bandwidth may bind first |
| M8-D2 | Start gate | (a) Approve the specification now; begin M8-A only after the M7 milestone review, in roadmap order ("do not implement M8 early"); (b) begin M8-A on fixtures once M6-A and M7-A shapes merge | (a) | M8 waits on every M7 PR, including LOCKED ones that may stall on the source decision (M8-MR2) |
| M8-D3 | Trip intent fields | (a) The 6.1 fields; out-of-scope inputs not asked; unchecked inputs stated (R160); (b) also amenities, dogs and accessibility as unevaluated preferences | (a) | Users who care most about dogs or accessibility find no control at all |
| M8-D4 | Activities per trip | (a) One or two, each needing its own feature; (b) one | (a) | Two-activity candidates multiply unknowns per card and assembly cost |
| M8-D5 | Activity relevance basis | (a) A reviewed claim, or the source's own use or management field naming the activity (labelled as source information), or for water any M4-displayed water; never by name; (b) reviewed claims only | (a) | See M8-MR6: "the source lists motorcycle use" sits beside "Motorcycle: not established" and may be read as permission; (b) leaves the planner empty until M6-E |
| M8-D6 | Pairing basis and search bound | (a) Established chain, then shared staging, then a 5-mile straight-line search bound from the base to the nearest member, labelled as a search bound (matching today's listings); (b) established chains only; (c) the whole search area | (a) | 5 miles is arbitrary: it misses practical options beyond it and includes impractical ones across a ridge (M8-MR7) |
| M8-D7 | Ordering | (a) K1–K5 of 10.1: established parts by set and count, conditions, straight-line tie-break only with a stated origin, stable ID; reasons shown, no score; (b) groups only, ordered by name; (c) a published weighted score | (a), with M8-MR1 decided | See M8-MR1: the review queue, not the user's fit, decides the order |
| M8-D8 | Ruled-out candidates | (a) Their own group after G1, listed in full, count stated above G1; (b) behind a toggle; (c) mixed in last | (a) | A long G2 pushes useful content down on a phone |
| M8-D9 | Restricted answers | (a) Established with conditions; conditions listed first; ranked below an equal candidate with fewer conditions (K3); (b) treated as not established for ordering | (a) | "Designated sites only" may read as a pass when the user does not read the condition |
| M8-D10 | Explanation | (a) Three lines per card from approved literals: why listed, why here, still not established; (b) full detail only | (a) | Three lines per card make the list long at 320 px |
| M8-D11 | Pilot retirement | (a) Replace `trip_planner`/`adventure_pilot` with one `adventure_planner` in both regions; migrate storage (section 20); (b) keep the Aspen pilot beside the planner | (a) | Aspen users lose the familiar landing and the resort selector |
| M8-D12 | Douglas Browse | (a) Kept as the free-discovery list, reading the shared intent; activity, dates and vehicle move to the intent editor; (b) Browse unchanged | (a) | Changes the M4-era interface the adventure model said not to redesign before M8 |
| M8-D13 | Wording process | (a) Constraints R234–R249 now; literals approved in the PR that renders them; (b) all literals in this specification | (a) | Literals approved piecemeal can drift in tone |
| M8-D14 | Budgets | (a) Section 23: nothing before map usable, ≤ 25,000 bytes of planner code, ≤ 150 ms assembly, ≤ 30 candidates; (b) a looser assembly budget | (a) | The 150 ms figure is a guess until real registries exist |
| M8-D15 | Routing | (a) None in M8; Getting there reads not established; outbound directions link kept; (b) specify a routing source by amendment once one is proposed | (a) | Scenario B's "closest practical" and "where to drive" stay unanswered in the product |
| M8-D16 | Two parties (Scenario B) | (a) One profile and a `day_use` base (section 12, LOCKED on M7-D16); separate party profiles deferred; (b) `parties[]` with separate profiles in M8 | (a) | The rider's trailer and the family's car cannot be evaluated separately [DRAFT-PR 29 gap 1] |
| M8-D17 | What completes M8 | (a) M8-A to M8-C, plus each LOCKED PR whose dependency has been delivered; the review states plainly what was not delivered and why; (b) M8 is not complete without M8-D and M8-E | (a) | A milestone titled Choose Your Adventure could close with most parts reading not established |
| M8-D18 | Scenarios at close | (a) Scenario A; Scenario B canonical if PR #20 merges, else supplementary; the Aspen supplementary scenario of 25.3; (b) Scenario A only | (a) | Three phone runs per close; the Aspen scenario is not canonical and so not longitudinal |
| M8-D20 | Day trips | (a) A single date with no night is a valid intent (needed for Scenario B); (b) overnight only | (a) | Widens M8 beyond the core overnight question |

### 30.3 Continuous geographic Explore (M8-D19) — choose one; no recommendation

| Option | Summary |
|---|---|
| (a) | Not in M8; one package per page load; edges stated (DS9); later milestone |
| (b) | Coverage index and cross-package search only; candidates within one package |
| (c) | Full continuous Explore in M8, with lazy packages, cross-package candidates and per-view budgets |
| (d) | A separate milestone before M8 |

Consequences, costs and risks are in section 16.2. The rules of 16.3 hold under every option. This decision is the owner's by the roadmap; no default is assumed, and M8-G does not start until it is made.

### 30.4 Material risks (flagged separately, each with its decision)

| ID | Risk and decision | Options | Recommended | Bear case |
|---|---|---|---|---|
| M8-MR1 | **The review queue decides the ranking.** Under M8-D7 (a), a candidate rises because a person reviewed its parts. The M7 draft chooses its initial review set from the places Scenario A's last run and PR #20 name. [DRAFT M7 20] Ranking would then reward the scenario's own places, and a scenario score could improve because of what was reviewed, not what fits the user | (a) Accept D7 (a) with R198: initial review sets in M4–M7 chosen by a published rule independent of scenario outcomes, and the ordering line on every list; (b) choose D7 (b) until each region has reviewed records for most bases | (a) | Even with a neutral rule, well-reviewed places rise and unreviewed ones sink; a user reads that as quality |
| M8-MR2 | **M8 ships before M5–M7 deliver enough.** With today's data every part beyond TP1 and TP5 reads not established (DS4), and every candidate has the same K1 set | (a) M8-D2 (a) and M8-D17 (a): ship A–C, say so plainly, wire LOCKED PRs as data lands; (b) hold M8 until M6-E and M7-E have merged | (a) | The planner may look like a regression from the pilot, which at least listed nearby trails; owner and testers may judge the milestone a failure |
| M8-MR3 | **Candidates stop at a package edge.** Under M8-D19 (a), the Rampart area or any trail system continuing past the Douglas county line is seen from one side only | Decided by M8-D19; DS9 and R218 apply under every option | — | Users near an edge plan with half the picture, warned by one line |
| M8-MR4 | **Scenario B's owner targets may be unreachable without new sources.** "No more than one external source", "current-status evidence" and "practical driving" need routing, current orders and status that no approved source provides [DRAFT-PR 20] | (a) Report each target as met, partly met or not met with its blocking dependency; never meet a target by weakening evidence; (b) gate M8 close on the targets | (a) | M8 closes with the owner's stated targets unmet, and the reason is outside M8 |
| M8-MR5 | **Order changes with no data change.** Reviews age daily; a candidate's established parts become not established and its position falls, so the list differs between Friday and Saturday | (a) Accept, with the review date on each part and "review overdue" on stale restrictions; (b) freeze order at a data version | (a) | Users see the list reshuffle and lose trust; (b) would freeze staleness and is ruled out by trust principle 5 |
| M8-MR6 | **Relevance read as permission (M8-D5 (a)).** A trail is listed for motorcycles because the source's management field names motorcycles, while its permission reads not established | (a) R172 and R236: relevance never beside a status word; "source information" heading; (b) M8-D5 (b) | (a) | A rider may treat "listed for motorcycles" as "motorcycles allowed", the Scenario A step 2 confusion that already exists today |
| M8-MR7 | **The search bound shapes what users see (M8-D6 (a)).** A fixed straight-line bound includes places across a ridge or river and excludes practical ones further out | (a) Bound shown on every basis (iii) pair; owner may change the value by configuration with R258; (b) D6 (b) established chains only | (a) | The bound is the most influential number in the planner and has no evidence behind it |

### 30.5 Decided engineering choices (no owner answer needed)

The coordinator may change these by amendment within the trust rules and the requirements, reporting any change to the owner.

| Choice | Recorded in |
|---|---|
| One R-number series from R150, with enforcement letters | 0.3 |
| `v2/explore/adventure.js` as the pure assembly and ordering module | R178 |
| Candidate cap 30, each base in at most 3 | 8.3 step 8, R268 |
| Groups G1–G3 and their order | 9.1 |
| Name order as the only alternative sort | R196 |
| Geolocation on request only, memory only | R156 |
| Saved candidates store intent and part IDs only | R180 |
| No pipeline pair table; fallback by amendment | 23 |
| Detail section order | 18.2 |
| Storage migration rules | R250, R251 |

### 30.6 Totals and answer format

**Requirements:** 119 (R150–R268). By primary enforcement letter: N 89, B 20, V 8, H 2; some also carry a second letter. **LOCKED:** sections 12, 13, 14, 15 in full, and the L12 vocabulary parameter of section 6 and the L16 parts parameter of section 7; interfaces L12–L17. **Owner decisions:** 20 (M8-D1 to M8-D20: 19 recommended defaults in 30.2 and M8-D19 continuous Explore in 30.3 with no recommendation). **Material risks:** 7 (M8-MR1 to M8-MR7).

**Answer format:** `M8: accept defaults; D19 <a|b|c|d>; MR1 a; MR2 a; MR4 a; MR5 a; MR6 a; MR7 a` (or name any default to change, for example `M8: accept defaults except D6 b; D19 a; MR1 b; MR2 b; MR4 a; MR5 a; MR6 a; MR7 a`). MR3 is decided by D19.

**Unlock.** The open M5–M7 decisions named in L12–L16 unlock M8-D, M8-E and M8-F as each is decided and delivered; L17 (routing) stays locked until a routing source is proposed; M8-D19 unlocks M8-G.

## Appendix A. Evidence basis

| Fact | Basis | Where |
|---|---|---|
| Capabilities, fact coverage, inventory counts and flags, recreation-site types, trail feature counts, pilot assembly and wording, module sizes, index sizes, research-area bytes, sheet structure, pilot extents | [MEAS] | [m8-spec-evidence.md](../research/m8-adventure/m8-spec-evidence.md) E1–E12 |
| Trust rules, never-infer table, staleness asymmetry, fail-closed, presentation, language | [REPO] | `docs/product/trust-principles.md` |
| One Explore surface, proximity is not a relationship, not checked is not no restriction, intent visible, product question | [REPO] | `docs/product/product-principles.md` 2, 11–15 |
| Relationship origins, chain rules, evidence coverage, trip intent, adventure candidate parts, ordering properties, M5–M7 obligations | [REPO] | `docs/architecture/adventure-model.md` sections 1, 3–6 |
| Single-region loading, coverage behaviour, data-loading implications, decision reserved for M8 | [REPO] | `docs/architecture/continuous-explore.md` |
| M8 inputs, output, core question, product-alignment expectations | [REPO] | `ROADMAP.md` M8 |
| Evidence classes, claim statuses, freshness table, wording process, budgets | [REPO] | `docs/specs/M4-functional-recreational-water.md` sections 4, 9, 10, 14 |
| Shell, sheet, adapter exports, mobile requirements, budgets, growth budget | [REPO] | `docs/specs/M3-unified-mobile-explore.md` sections 8.1, 11, 16 |
| Scenario A task, definitions, measures, baseline facts | [REPO] | `docs/product/acceptance-scenario-douglas-dirt-bike.md` |
| Scorecard lines for candidates with viable overnight and backup options | [REPO] | `docs/product/product-scorecard.md` |
| Land unit IDs, coverage, access always not reviewed, decisions M5-D6, M5-D13 / R1 | [DRAFT M5] | `k-kopacek/m5-spec-draft` `2c329e3`: sections 7, 9, 10, 20 |
| Trail identity and parts, activity vocabulary and claims, relationships RL1–RL8, decisions M6-D2–D16, L1–L6 | [DRAFT M6] | `k-kopacek/m6-spec-draft` `82a3c84`: sections 0.3, 8–12, 22 |
| Overnight places, setups, precedence, orders, vehicle constraints, `relevant_to` and backup predicates, presentation CP1–CP17, decisions M7-D1–D20, MR1 interim decision, last rule R149 | [DRAFT M7] | `k-kopacek/m7-spec-draft` `b8471b1`: sections 0.3, 7–13, 16, 20, 24; `docs/research/m7-camping/mr1-closure-audit.md` |
| Two parties, day use versus overnight, conflicting readings, walking link, hammock, payment | [DRAFT-PR 29] | `docs/research/m8-adventure/rampart-worked-example.md` on `research/m8-rampart-worked-example` `c781777` |
| Scenario B task, expected answer shape, baseline, owner targets by M8 | [DRAFT-PR 20] | `docs/product/acceptance-scenario-rampart-day-use.md` on `docs/rampart-day-use-scenario` `65cfd5d` |
| Ranking architectures A–E, what must not be ranked, minimal first version, property tests | [DRAFT-PR 15] | `docs/research/m8-adventure/ranking-architecture-options.md` on `docs/research-drafts` `83f15a3` |
