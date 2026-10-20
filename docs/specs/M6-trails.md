# Milestone 6 specification — Trails

Status: DRAFT — NOT APPROVED. Source-neutral sections proposed for owner review; every source-dependent section is LOCKED pending the M6 source policy (PR #24).

**For:** Codex (implementation), once approved. **Reviewer / coordinator:** Claude. **Research:** coordinator; Hermes optional. **Base:** `main` at `c04f5d6`.
**Delivery (proposed):** small sequential pull requests on the two pilot regions only (section 18). Some can start after this specification is approved; the rest are LOCKED on the source policy.
**Owner decisions:** every choice that is the owner's is in section 22, as M6-D1 to M6-D16 with a recommendation and a bear case, and as material risks MR1 to MR7. None is taken. Where this document says "M6 does X", read "this draft proposes that M6 does X, subject to the decision named".

Governing documents: `AGENTS.md`, `ROADMAP.md` (M6, including the owner's user-facing trail identity requirement of 2026-10-06 and the product-alignment expectations of 2026-10-08), `docs/agent-stack/roles.md`, `docs/product/trust-principles.md` (normative), `docs/product/product-principles.md`, `docs/product/product-scorecard.md`, `docs/product/acceptance-scenario-douglas-dirt-bike.md`, `docs/architecture/adventure-model.md`, `docs/architecture/continuous-explore.md`, ADR-005, ADR-006, `v2/pipeline/docs/data-contract.md` (normative for data), `v2/pipeline/TRAIL-PILOT.md`, `docs/specs/M3-unified-mobile-explore.md` (section 13 and amendments A1–A14) and `docs/specs/M4-functional-recreational-water.md` (the format model, and the grouping invariants G1–G10 of its section 8.3, the closest precedent for trail grouping).

## 0. Reading this draft

### 0.1 What is settled, proposed and locked

| Label | Meaning |
|---|---|
| **SOURCE-NEUTRAL** | A rule that holds whichever source the owner approves. Proposed for approval now. |
| **LOCKED** | Depends on which source is used, how its terms are read, or how one source's fields map. This draft states only the interface and the decision needed. Nothing in a LOCKED section is chosen. |
| **NORMATIVE (restated)** | Already binding through the trust principles, the data contract or an approved specification. Restated so the M6 rules can cite it; this draft does not change it. |

Section 4 lists every section with its label.

### 0.2 Evidence marks

| Mark | Meaning |
|---|---|
| [REPO] | Read from a normative or approved repository document on `main` |
| [MEAS] | Measured from committed data on `main` for this draft; recorded in [m6-spec-evidence.md](../research/m6-trails/m6-spec-evidence.md) as T1–T7 |
| [DRAFT-PR n] | Stated in an unmerged, unreviewed research pull request; not re-checked; not product truth |
| [INF] | Inference in this draft from the marked facts |
| [UNK] | Not established by anything read |

No network request was made for this draft. Every [DRAFT-PR] input is a proposal: PR #24 (source policy), PR #33 (motorized-evidence prototype), PR #29 (Rampart worked example), PR #20 (Rampart day-use scenario) and PR #35 (forest orders, M7 input). The M5 draft (`k-kopacek/m5-spec-draft`) is also unapproved; where this draft depends on an M5 interface it says so.

### 0.3 Numbering

- Validator rules continue after the M5 draft's last rule, R85, with a gap: M6 rules are **R100–R119**. R86–R99 stay free for M5 amendments.
- Trail grouping invariants are **TG1–TG14** (the `T` keeps them distinct from M4's G1–G10).
- Activity-evidence invariants are **AE1–AE12**.
- Relationship rules are **RL1–RL8**. Presentation constraints are **PC1–PC14**.
- LOCKED interfaces are **L1–L6**.

## 1. Problem

**A user sees source pieces, not trails.** Both pilots hold one source, the Forest Service National Forest System Trails layer: 123 segments in Aspen and 102 in Douglas County, each its own tappable feature, search row and GPX export. [MEAS T1, T2] The source numbers 87 trails in Aspen and 78 in Douglas. In Aspen 26 trail numbers have more than one segment; in Douglas 11. [MEAS T2] The roadmap's own example is in Aspen: Difficult Creek is two segments, number `2146`, joined end to end, and the user gets two features. [MEAS T3] [REPO ROADMAP M6]

**The easy fix is wrong.** Joining by name and touching geometry would merge Douglas `TURTLE MOUNTAIN` `0770` with `TURTLE MOUNTAIN` `0770.E`: same name, shared end point, different source routes. [MEAS T4] Joining by number alone would present Douglas `800` INDIAN CREEK, four pieces with gaps up to about 2.3 km, as if it were continuous. [MEAS T4] Neither name nor geometry is identity (adventure model, relationship rule 6). [REPO]

**Activity data is management information, shown next to dates.** Each segment carries the source's `managed`, `accpt`, `disc` and `restricted` strings for nine activities, verbatim. [MEAS T1] [REPO TRAIL-PILOT] The pilot note says these are "not Boolean permissions". [REPO] The browser already declines to turn `managed` or `accepted` dates into a verdict and compares only `restricted` dates with trip dates. [MEAS T6] There is no record anywhere of a legal motor-vehicle designation, by vehicle class, for any trail; the only pointer is the sentence that "the Motor Vehicle Use Map and current agency orders govern motor vehicle use". [MEAS T6] The Douglas fact coverage for `trail_access` is `context`. [REPO]

**Nothing a trip needs is linked.** No trailhead or staging identity exists; 17 Douglas recreation-site records carry the source site type TRAILHEAD and nothing links one to a trail. [REPO adventure-model section 2] The only connection offered between a trail and anything else is straight-line distance, labelled as such. [MEAS T6]

**Identity is not built to survive.** Trail IDs are `usfs-trail-<objectid>`; whether `objectid` persists across the publisher's releases is not established. [MEAS T1] [UNK] Nothing makes a trail that crosses the Douglas county line one trail in two packages. [REPO continuous-explore]

## 2. Goals and the product question

1. **One trail, one feature.** A trail a user would name is one selectable, searchable feature, built from preserved source segments by validated rules, with every member traceable (section 8).
2. **Never merged on name or geometry alone.** The grouping evidence is a source-stated route identity or a reviewed grouping record; the invariants say what is never joined (TG rules).
3. **Identity that lasts.** A trail's ID survives a source refresh, a re-segmentation and a region-package boundary, or the change is reported and aliased (section 7, 8.6).
4. **Activity use as evidence, per activity and per vehicle class.** Each answer is `allowed`, `restricted`, `prohibited` or `unknown`, with its source, date, scope and kind of instrument. Management information is never permission. Staleness never weakens a restriction. Unknown is shown as unknown (section 9).
5. **Relationships M7 and M8 can use.** Trailhead and staging identity where a source provides it, and `starts_at` links that are source-backed, reviewed or unknown; `governed_by` only through the trail's own source field (section 10).
6. **Short, phone-readable wording** that never exceeds the evidence (section 11).

**Product question (product principle 15).** After M6 a Douglas rider can pick a trail by the name they know and see it as one thing; can see, per vehicle class, whether a reviewed legal designation says motorcycles are allowed, restricted or prohibited on it and on which dates, or that it is not established; can tell the source's management information apart from a legal designation; and, where a source names one, can see the trailhead the agency says serves the trail. A rider still cannot learn current conditions, whether the trail is open today, how to drive to the trailhead with a trailer, or where to stay overnight. If the source policy is not approved, M6 can deliver goal 1 on the already-published segments and goals 2–3 as rules, and must say plainly that goals 4–5 are not delivered (section 18).

## 3. Out of scope

- **Choosing a source, reading a licence or terms, or mapping one source's fields.** All LOCKED (sections 6 and 12) until the source policy (PR #24) is approved.
- **Current condition, openness today, closures by order and fire status.** M6 records no current condition (AE11). Forest orders as entities are M7 input [DRAFT-PR 35]; M6 reserves the `constrained_by` interface and records order coverage as not checked (section 10).
- **Roads and approach routes.** `approached_via`, road vehicle designations and trailer suitability are M7 under this draft (M6-D11).
- **Camping, day use and overnight options** (M7), and trip assembly, ranking and routing (M8).
- **Inferred relationships.** No link from proximity, containment, a name match or a geometry match (RL1).
- **E-bike permission from bicycle records** [REPO TRAIL-PILOT]; any activity from another activity.
- **Community, partner or third-party trail content**, ratings, difficulty and photos. Trail difficulty is not modelled.
- **Navigation**: turn-by-turn, elevation profiles, travel times. GPX export stays geometry-only (PC11).
- **A third region, statewide data, continuous Explore, or a cross-package loader.** Identifiers are designed not to block them (section 7.3).
- **Any change to the region loader, the map adapter and its exports, Leaflet, ADR-006, a new dependency, build step or basemap.** The generic overlap chooser stays deferred (M3 A13).
- **Changes to land, water or camping data.** M6 reads M5 land unit IDs and M4 water IDs only if relationships to them are approved (section 10).

## 4. Section map: source-neutral and LOCKED

| § | Section | Label | Can the owner approve it now? |
|---|---|---|---|
| 1–3 | Problem, goals, scope | SOURCE-NEUTRAL | Yes |
| 5 | Evidence model | SOURCE-NEUTRAL | Yes |
| 6 | Sources | **LOCKED** (L1, L2) | Interface only |
| 7 | Canonical segments and identifiers | SOURCE-NEUTRAL rules; the key field per source is **LOCKED** (L3) | Rules yes; key no |
| 8 | User-facing trail identity | SOURCE-NEUTRAL; which field is a source's route identity is **LOCKED** (L3) | Yes |
| 9 | Activity and permission evidence | SOURCE-NEUTRAL; which instrument counts as a legal designation, and the vehicle-class mapping, are **LOCKED** (L4) | Yes |
| 10 | Relationships | SOURCE-NEUTRAL; trailhead source **LOCKED** (L5) | Yes |
| 11 | Presentation constraints | SOURCE-NEUTRAL (literals deferred to the owner) | Constraints yes; literals later |
| 12 | Source field mapping | **LOCKED** (L6) | Interface only |
| 13 | Contract changes | SOURCE-NEUTRAL shapes; source fields **LOCKED** | Shapes yes |
| 14 | Validator rules | SOURCE-NEUTRAL; three rules take a LOCKED parameter | Yes |
| 15–17 | Budgets, tests, acceptance | SOURCE-NEUTRAL | Yes |
| 18 | Delivery | SOURCE-NEUTRAL plan; PRs marked neutral or LOCKED | Yes |
| 19–21 | Rollback, risks, unknowns | SOURCE-NEUTRAL | Yes |
| 22 | Owner decision packet | — | Decisions |

Count: 18 sections are source-neutral (1–3, 5, 7–11, 13–21) and 2 are LOCKED in full (6, 12). Six of the neutral sections carry a named LOCKED parameter that they do not choose (7, 8, 9, 10, 13, 14). Section 4 is this map and section 22 the decision packet.

## 5. Evidence model

### 5.1 Classes (NORMATIVE, restated from M4 section 4)

| Class | In M6 | Can it state that an activity is allowed, restricted or prohibited? |
|---|---|---|
| Source fact | Segment geometry, name, the source's route identifier, surface, the source's management strings, source dates | No |
| Official recreation information, reviewed | A legal-designation or agency statement for one activity, one vehicle class, one trail scope, read by a person (section 9) | **Yes, and only this class** |
| Derived fact | Trail identity and member map, part count, length, date-window parse | No |
| Community signal | None. No field allows one | No |

### 5.2 Kinds of source statement about use

A source can say several different things about use. They are kept apart because they mean different things, and only one of them can be permission.

| Kind | What it says | Example shape | Can produce `allowed`? |
|---|---|---|---|
| **Legal designation** | The responsible agency designates the route for a vehicle class, on stated dates, under its own instrument | A motor vehicle use designation for a class and date window | Yes, after review (AE4) |
| **Agency use statement** | The agency's own page states that an activity is allowed, restricted or prohibited on a named trail | "Trail 1234 is closed to bicycles" | Yes for restrictions; `allowed` only if the owner accepts M6-D7 (b) |
| **Management information** | How the agency manages or intends the trail (managed, accepted, discouraged, restricted use) | Today's `managed`, `accpt`, `disc`, `restricted` strings | **Never** (AE3). Its restriction direction is shown as management information, not as a legal prohibition (AE6) |
| **Order** | A temporary or standing order with scope and dates | A closure order | M7 entity; M6 reserves the link (section 10.4) |
| **Current status** | A banner, alert or "open" flag | "Site open" | Never; it is not modelled (AE11) |

Which publisher's instrument is the legal designation for each activity is LOCKED (L4).

### 5.3 Never (NORMATIVE, restated for trails)

1. A mapped trail is not legal access, trail access or permission for any activity (contract rule 15).
2. Management information is not permission (PR #24 states the same as a proposal [DRAFT-PR 24]; it follows here from contract rule 14).
3. An activity is never inferred from another activity, from a vehicle class to another class, or from a bicycle record to an e-bike class.
4. Openness is never inferred from the absence of a mapped closure (trust principle 2).
5. A successful retrieval never advances a confirmation (contract rule 2).
6. A name match or a geometry match never creates an identity or a relationship (adventure model rule 6).
7. Proximity is not a relationship (product principle 12).

## 6. LOCKED — Sources (interface and decision only)

**This section chooses nothing.** It states what any trail source must supply for the source-neutral sections to work, and the decision the source policy must make. Candidate sources named in research [DRAFT-PR 24] are COTREX, USFS National Forest System Trails (in use today), USFS Motor Vehicle Use Map layers, BLM and county sources. This draft takes no position on any of them, including on COTREX's terms.

### L1. The source interface

A source is usable by M6 only if, for each role it is approved for, the owner's source decision records:

| Interface item | Needed by | What must be recorded |
|---|---|---|
| Role | §6 | One or more of: segment geometry; route identity; legal designation; agency use statement; management information; trailhead or staging identity; trailhead-to-trail statement |
| Scope | §9, §10 | What the source is authoritative for, and what it does not establish (contract `sources.<id>.scope`) |
| Namespace | §7 | A constant `source_namespace` and ID prefix, reserved in the namespace table (7.2) |
| Segment key | §7 | The field that identifies a source segment, and whether the publisher documents it as persistent (L3) |
| Route identity | §8 | The field, if any, that the publisher uses to say several segments are one trail, and the administrative scope inside which that value is unique (L3) |
| Vehicle-class and activity fields | §9 | Which fields carry which activity or class, mapped to the M6 vocabulary of 9.1 (L4) |
| Date semantics | §9.5 | What a date value means in that source (designated window, management window, or other), from the publisher's own documentation |
| Terms reading | all | The owner's recorded reading of reuse, storage and redistribution terms |
| Refresh | §18 | Whether a controlled fetch is authorised, with the snapshot record of M4 section 5 |

### L2. The decision needed

> **Which sources fill which roles in the two pilot regions, under which terms reading?**

Until it is made, the LOCKED pull requests of section 18 do not start, no new source is fetched and no source-specific mapping is written. The source-neutral pull requests can start once this specification is approved. Whether the source already published in both regions (USFS National Forest System Trails) may keep its present role while the policy is decided is itself part of this decision (M6-D2); this draft does not assume it.

## 7. Canonical segments and identifiers

(Section body follows in the next commit.)

## 8. User-facing trail identity
## 9. Activity and permission evidence
## 10. Relationships: what M6 provides and does not
## 11. Presentation and trust-wording constraints
## 12. LOCKED — Source field mapping (interface only)
## 13. Contract changes
## 14. Validator rules
## 15. Budgets and performance
## 16. Tests
## 17. Acceptance
## 18. Delivery plan
## 19. Rollback
## 20. Risks
## 21. Unknowns
## 22. Owner decision packet
## Appendix A. Evidence basis
