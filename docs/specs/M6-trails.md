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

SOURCE-NEUTRAL rules. Which field is each source's segment key and route identity is LOCKED (L3).

### 7.1 Canonical segments are preserved

Every source segment stays in canonical data as the source published it, with its own ID, geometry and source fields. A user-facing trail (section 8) is a derived layer over segments. Grouping writes one derived property on a segment, `trail_id`, and changes nothing else (TG9). A segment with no trail is still a canonical record.

### 7.2 Identifier rules

| Thing | ID form | Rule |
|---|---|---|
| Segment | `<segment prefix>-<sanitised segment key>` | Computed from the source record only. No region ID, sequence number or Ohvernight-assigned number. A service row number is used only if the publisher documents it as the persistent key (L3); otherwise the build uses the documented key, and if the source has none the segment's persistence is recorded as unknown in the snapshot record and legacy matching (7.4) carries identity across refreshes |
| Trail | `trail-<namespace short>-<scope>-<sanitised route key>` | From the source's route identity and the administrative scope inside which it is unique (8.2). Never from a name or from member IDs, so a trail keeps its ID when its segments change |
| Trail from a reviewed grouping record | `trail-rv-<record key>` | Only where section 8.3 applies |
| Trailhead or staging area | `<site prefix>-<sanitised site key>` | As for segments, from the site source (L5) |

Sanitising lowercases and removes characters outside `[a-z0-9-]`; the unmodified value stays in its source field. Route keys are compared **exactly as published**, after trimming surrounding whitespace only. Zero-padding, case and suffixes are not normalised unless the publisher documents that two spellings are the same route (L3). Douglas has `0681` beside `681.D`; normalising would be a guess. [MEAS T4] Values that would collide after removing zero-padding are listed in the build report for review and never joined; there are none in either pilot today. [MEAS T4]

If two records of one fetch produce the same segment ID, or a segment has an empty key, the build stops and reports. There is no fallback and no suffix added to make an ID unique. A trail ID never equals or begins with a segment prefix; a validator rule checks it (R101).

Reserved namespaces. The table is filled in by the source decision (L3); M6 reserves the trail prefix now.

| Namespace | Prefix | Status |
|---|---|---|
| (user-facing trail) | `trail-` | Reserved by M6 |
| USFS National Forest System Trails (in use) | `usfs-trail-` | Existing; whether it remains, and its key, are L3 |
| Any further trail, designation or site source | to be assigned | LOCKED |

### 7.3 Across region packages (continuous-explore implications 3 and 4)

- **The same source route has the same trail ID in every region package.** A trail crossing the Douglas county line into a future neighbouring package has one ID, with one delivered part in each package. [REPO continuous-explore]
- **A trail ID identifies what its source identifies.** It is the source's route within the stated scope. It is not a claim that the route is continuous, ridable end to end, or the same as a route in another source.
- **Clipping is a display concern.** Each package holds the members inside its coverage. Non-geometry trail fields of one trail ID are identical in every package that holds it; a repository-level rule checks it (R113).
- **Evidence does not merge.** Activity claims are scoped to the members and the region package they were reviewed for (AE9). A claim reviewed in Douglas does not appear in another package unless a reviewer records it there.

### 7.4 Legacy IDs and aliases

The rules of M4 amendment A4 apply to segments and to trails: an ID once in `legacy_ids` stays there; a feature's own ID is never in its `legacy_ids`; a legacy ID on two features stops the build. Old and new segments are matched by exact canonical geometry within the same layer, or by the same current ID; a row-number match alone is not accepted.

Douglas Browse's saved plan stores up to 40 feature IDs, so a saved trail is held today by its segment ID. [MEAS T6] When trails become the selectable feature, a saved segment ID must still open its trail. The display therefore carries a `trail-aliases.json` file mapping each displayed member's segment ID, and each legacy ID, to its current trail ID, modelled on M4 A2: it is outside `index.json`, not requested during load, and read only when a saved ID does not resolve.

## 8. User-facing trail identity

SOURCE-NEUTRAL. The only LOCKED parameter is which field of an approved source is its route identity, and its scope (L3).

### 8.1 What a user-facing trail is

A user-facing trail is the set of canonical segments that a source, or a reviewed record, says are one named route, shown as one display feature. It has:

- an **identity** (its ID, name and route key), from 8.2 or 8.3;
- **members** (canonical segments), every one traceable;
- **parts**: the connected sets of members under the adjacency rule of 8.4.

**Identity and continuity are separate.** M4 kept them separate for rivers by making each disconnected part its own group (M4 G3). For trails this draft proposes the opposite default, because the source's route identity, not geometry, says what the trail is (M6-D4): one trail may have several parts, drawn as one MultiLineString with no line between them, and the detail says how many separate pieces are shown (PC6). Continuity between parts is never stated or implied. If the owner prefers M4's model, each part becomes its own trail with the suffix `-p<n>` and the same name, exactly as M4 8.3 step 5 does.

### 8.2 Grouping by source route identity (the default)

1. Candidates are the segments of one source namespace whose route key is non-empty.
2. Partition candidates by (namespace, scope, route key), where scope is the administrative unit within which the publisher says the route key is unique (L3). Route keys from different scopes are never compared.
3. Each partition is one trail. Its members are ordered by segment ID.
4. Within a trail, build the adjacency graph of 8.4; each connected component is a part. Parts are ordered by total length, longest first, ties by smallest member ID.
5. The trail's display geometry is each member's geometry, transformed as R63 requires, one line per member in member order. Nothing else.
6. The trail's display name is its members' name. If members of one trail carry different names, the build stops and reports them (TG2); it does not pick one.

Difficult Creek (Aspen `2146`, two segments sharing an end point) becomes one trail with one part. [MEAS T3] Douglas `800` INDIAN CREEK becomes one trail with four parts. Douglas `0770` and `0770.E` TURTLE MOUNTAIN stay two trails, though they share a name and an end point. [MEAS T4]

### 8.3 Reviewed grouping records (where the source does not say)

Where a person can show from a responsible agency's own page or map that several source routes are one trail a user would name, a reviewed grouping record may join them. It is the only way two route keys, or segments from two namespaces, become one trail.

`v2/regions/<id>/trail-groupings.json`, curated by hand, validated, optional:

```json
{"schema_version": 1,
 "records": [
  {"key": "…", "name": "…",
   "members": {"route_keys": [{"namespace": "…", "scope": "…", "route_key": "…"}], "segment_ids": []},
   "evidence": {"source_url": "https://…", "agency": "…", "statement": "Short factual statement of what the page establishes.",
                "basis": "manual_review", "last_checked_at": "…", "last_confirmed_at": "…", "max_age_hours": 8760}}]}
```

Rules: the statement is written by the reviewer, at most 160 characters, never a quotation longer than 25 words, and says what the page establishes about the trail's identity, never about use or access; the `source_url` is on the agency's own site and not on a host in the configuration's non-claim list; a record whose only support is a shared name or touching geometry is invalid; `last_confirmed_at` is set only after the coordinator has read the page and the owner has approved the record in the pull request (as M4-C). A stale grouping record is shown as "review overdue" and is not removed; it is an identity statement, not a restriction, so trust principle 5's asymmetry does not arise. A reviewed record never joins members whose source names conflict without stating which name the agency uses. In M6 the file ships empty unless the owner supplies records (M6-D5).

**Cross-source matching** (for example a designation record and a trail-geometry record for the same route) is a candidate only. A normalised route-number match is a candidate, as PR #33 also treats it; in the research sample it matched 14 of 25 records after zero-padding normalisation and 11 not at all. [DRAFT-PR 24] [DRAFT-PR 33] Candidates are listed in the build report and are never published as identity or as a claim's subject until a reviewed crosswalk record (10.3, LOCKED on sources) confirms each one.

### 8.4 Adjacency

Two members are adjacent when an end point of one equals an end point of the other after rounding canonical coordinates to six decimals. Interior crossings and near misses do not connect. No snapping tolerance is applied (M6-D6): Douglas INDIAN CREEK has two pieces about 6 m apart that stay separate parts. [MEAS T4] The build report lists every pair of parts of one trail whose nearest end points are within 25 m, so the reviewer and owner see near-misses; the report changes nothing.

### 8.5 Invariants (validated; R102–R105)

- **TG1.** Every member of a source-route trail has the trail's namespace, scope and route key.
- **TG2.** Every member of a trail has the same name. Conflicting names fail the build.
- **TG3.** Different route keys are never in one trail unless a reviewed grouping record (8.3) names each of them.
- **TG4.** Segments of different namespaces are never in one trail unless a reviewed grouping record names each of them.
- **TG5.** A name match, a touching end point, an overlap, a shared agency, containment in an area, or a computed geometric similarity is never a grouping basis, alone or together.
- **TG6.** A segment belongs to at most one trail (M6-D8 covers concurrent routes).
- **TG7.** A segment with an empty route key belongs to no source-route trail; it may join a trail only through a reviewed grouping record that lists its segment ID.
- **TG8.** The set of members of a trail equals the set of canonical segments whose `trail_id` is that trail ID.
- **TG9.** Grouping never changes, removes or reorders canonical data except by writing `trail_id`.
- **TG10.** Every coordinate in a trail's display geometry comes from a member's canonical geometry. No line is added between members or between parts.
- **TG11.** A trail's `part_count` equals the number of connected components of its members under 8.4.
- **TG12.** A trail ID is computed from identity inputs only (8.2 or 8.3), never from members, names or geometry, so adding or removing a member does not change it.
- **TG13.** A trail ID never collides with a segment ID or a site ID, in any namespace.
- **TG14.** Suffixed and parent route keys (`0770` and `0770.E`) are different routes. A relationship between them (spur, branch, system) is not modelled in M6 except through a reviewed grouping record.

### 8.6 Stability across refreshes

On a later controlled fetch (LOCKED PRs only), the build compares the new trail set with the committed one and writes a stability report: trails added and removed; trails whose member set changed; trails whose name changed; segment IDs that moved between trails; and new name conflicts. A trail whose route key disappears is not silently dropped: its ID joins the `legacy_ids` of a trail only where a member's geometry or ID matches (7.4); otherwise it is listed as removed and its saved-state alias resolves to nothing, which the browser shows as "no longer in the source" (PC13). A difference not explained by the source stops the PR: Codex reports and waits.

### 8.7 Trail systems and recreation areas

A trail system or recreation area (for example the Rampart Range motorized area [DRAFT-PR 20]) is an identity only where a source or a reviewed record names its member trails. Containment inside an area polygon, nearness, or a shared name prefix never makes a trail a member. M6 reserves the entity and the `member_of` relationship (10.1) and creates none unless the source decision approves a source that states membership (M6-D9). PR #24 found no structured membership source. [DRAFT-PR 24]

## 9. Activity and permission evidence

SOURCE-NEUTRAL. Which instrument is the legal designation for each activity, and how a source's classes map to the vocabulary, are LOCKED (L4).

### 9.1 Vocabulary

Activities and motorized vehicle classes are modelled independently. No answer is derived from another (AE2).

| Key | Meaning | Notes |
|---|---|---|
| `hiking` | On foot | |
| `horseback_riding` | Equestrian, ridden or led stock | |
| `mountain_biking` | Non-motorized bicycle | Never implies any e-bike class |
| `ebike_class_1`, `ebike_class_2`, `ebike_class_3` | Electric bicycles by class | Reserved. `unknown` everywhere unless a source states the class itself |
| `motorcycle` | Two-wheeled motor vehicle (dirt bike) | |
| `atv` | All-terrain vehicle at or under the width the source states | |
| `ohv_wide` | Side-by-side, UTV or other OHV wider than the source's narrow class | The width threshold is the source's (L4) |
| `four_wheel_drive` | Full-size high-clearance or 4WD vehicle | |
| `snowmobile`, `snowshoeing`, `cross_country_skiing` | Winter use | Kept as today |

The mapping from a source's own classes to these keys is LOCKED (L4). A source class that does not map exactly to one key is not forced onto one: it stays a source fact and every key it might touch stays `unknown`. The prototype in PR #33 found fourteen MVUM classes for one route record [DRAFT-PR 33]; the vocabulary may need refining once the source is chosen, which is a specification amendment, not an implementation detail.

### 9.2 The claim

Activity claims live in a reviewed registry, never as properties on a segment or trail (R108), as M4 kept water claims in `water-recreation.json`.

`v2/regions/<id>/trail-use.json`, validated:

```json
{"schema_version": 1,
 "records": [
  {"trail_id": "trail-…",
   "applies_to": {"scope": "whole_trail", "segment_ids": []},
   "claims": {
     "motorcycle": {"status": "restricted", "instrument": "legal_designation",
       "windows": [{"raw": "05/01-11/30", "start": "05-01", "end": "11-30"}],
       "summary": "Designated for motorcycles in the stated season only.",
       "evidence": {"source_url": "https://…", "agency": "…", "basis": "manual_review",
                    "source_edition": "…", "last_checked_at": "…", "last_confirmed_at": "…",
                    "max_age_hours": 2160, "effective_from": null, "effective_to": null}},
     "atv": {"status": "prohibited", "instrument": "legal_designation", "summary": "…", "evidence": {"…": "…"}},
     "hiking": {"status": "unknown"}},
   "notes": []}]}
```

| Field | Rule |
|---|---|
| `trail_id` | A displayed trail ID in that region |
| `applies_to` | `whole_trail`, or `segments` with the listed member IDs. A claim that the source states for part of a trail applies only to those members (AE9) |
| `status` | `unknown`, `allowed`, `restricted`, `prohibited`, with M4 9.2 rule 3's meanings. `restricted` means allowed only with a condition specific to this trail (season, permit, width, direction) |
| `instrument` | `legal_designation`, `agency_statement`. Required for every non-unknown status. `management_information` is not an accepted value: it is never a claim (AE3) |
| `windows` | For a seasonal claim: the source's date text verbatim in `raw`, and the parsed month-day pairs. A value that does not parse keeps `raw` and has no `start`/`end` (9.5) |
| `summary` | At most 160 characters, written by the reviewer, not copied |
| `evidence` | Contract 5.4 claim evidence with `basis` `manual_review` (or `validated_structured_field` only if M6-D7 (c) is approved), the publisher's own URL, `source_edition` (the map edition, order number or page date the reviewer read, or null where the page states none), `last_checked_at`, `last_confirmed_at`, positive `max_age_hours`, and `effective_from`/`effective_to` for a dated one-off |

Every key of 9.1 is present in every record. A status of `unknown` has no other key. One evidence object is never shared by two claims (M4 9.2 rule 5).

### 9.3 Invariants (validated where they can be; R106–R111)

- **AE1. Unknown is the default** and is stored as `{"status": "unknown"}` or as absence of a record. A trail with no record has every activity unknown.
- **AE2. No inference across activities or classes.** `motorcycle` never sets `atv`; `mountain_biking` never sets an e-bike class; `hiking` never sets anything.
- **AE3. Management information is never permission.** The source's managed, accepted, discouraged or restricted-use strings stay source facts on the segment. They cannot be cited as the instrument of a claim and cannot produce `allowed`.
- **AE4. Positive claims fail closed.** `allowed` needs a reviewed legal designation or, only if M6-D7 (b) is approved, a reviewed agency statement; complete evidence; scope covering the members; and a review within policy. Missing any part gives `unknown` (trust principle 6).
- **AE5. Restrictions first.** A prohibited or restricted claim is shown whenever one exists, whether or not the review is overdue, and before any allowed claim.
- **AE6. Management restrictions are shown as management information.** A source's `restricted` management string is shown with that label (PC4). It is not upgraded to a legal prohibition, and it is not hidden because no legal record exists.
- **AE7. Staleness never weakens a restriction.** The freshness table of 9.4 applies.
- **AE8. Conflicts stay side by side.** Where two reviewed records disagree about one activity on one member, both are kept and shown with their sources. The displayed result for that activity is never `allowed`: a conflict that involves a restriction shows the restriction; any other conflict shows not established. No reading is chosen by recency or source rank unless an instrument itself states precedence. [DRAFT-PR 24] [DRAFT-PR 29]
- **AE9. Claims are scoped.** A claim covers the members it names, in the package where it was reviewed. It does not spread to other members, other trails, connected trails, trails in the same area, or another package.
- **AE10. Date evaluation never creates permission.** A trip date inside a designated window yields at most the claim's own status; a date outside it yields not designated for those dates. Neither is a statement that the trail is open (9.5).
- **AE11. No current condition.** M6 stores no open/closed status, no condition, no live banner, and no "current" wording. Current condition is unknown, always, and the detail says so (PC9).
- **AE12. A source's absence of a value is unknown.** A designation source that does not list a trail, or lists it without a class, establishes nothing about that class.

### 9.4 Freshness (NORMATIVE pattern, from M4 9.3)

| Stored status | Within policy | Past policy |
|---|---|---|
| `allowed` | Allowed, with its scope and dates | Not established, with the last review date |
| `restricted` | Restricted, with its condition | Still restricted, flagged review overdue |
| `prohibited` | Prohibited | Still prohibited, flagged review overdue |
| `unknown` | Not established | Not established |

Computed from `last_confirmed_at` and `max_age_hours`, never stored, as for existing claims. Validation stays time-independent (contract rule 10). Proposed default `max_age_hours` for designation claims is 2,160 (90 days), shorter at the reviewer's choice for a seasonal claim, and 8,760 for grouping records (M6-D12). A new edition of the source instrument does not refresh a review; it is a reason to review again.

### 9.5 Seasonal and date-bounded designations

- The source's date text is kept verbatim in `raw`. Only the exact forms the build recognises are parsed: `MM/DD-MM/DD`, comma-separated windows, and windows that wrap the year end. Trailing whitespace is trimmed before parsing and kept in `raw`. [MEAS T5] [DRAFT-PR 33]
- An unparseable value is kept and treated asymmetrically: for a positive claim the dates are unknown, so the result is not established; for a restriction it stays in force and is flagged for review. It is never replaced by a guessed window.
- A window means what the publisher's legend for that instrument says (L4). Whether a management window means a season of use is not inferred; today's browser already declines to infer it. [MEAS T6]
- Trip-date evaluation (AE10) is computed at view time for the dates the user entered, never stored, and shown with those dates.
- A dated one-off (`effective_from`/`effective_to`) is a restriction or a positive claim with an interval. When the interval has ended the record stays in the registry and history; the browser shows it as ended only for trip dates after its end, and never treats an ended restriction as evidence of openness.

### 9.6 Evidence coverage for trails (adventure model section 4)

For each trail and category, coverage records whether a person checked a named source, separately from what was found. `v2/regions/<id>/trail-coverage.json` follows the M5 draft's `land-coverage.json` shape (subject, category, jurisdiction, summary, evidence) with subject a trail ID. [DRAFT M5 9.1] Categories in M6:

| Category | Refines | In M6 |
|---|---|---|
| `motorized_use_rules` | `trail_access` | Accepted (LOCKED PRs only, because the check reads a source) |
| `non_motorized_use_rules` | `trail_access` | Accepted (as above) |
| `seasonal_closures` | `closures` | Accepted when the instrument checked states seasons |
| `orders` | `closures`, `restrictions` | Reserved: not checked for every trail in M6; M7 owns orders [DRAFT-PR 35] |
| `current_condition` | — | Not a coverage category. Current condition is unknown, not "not checked" |

The coverage rules of the adventure model apply unchanged: coverage never creates permission; checked with no record is not "no restriction"; not checked is the default and is shown; coverage is scoped; it ages; there is no fully-covered state and no single score.

## 10. Relationships: what M6 provides and does not

SOURCE-NEUTRAL. The trailhead source is LOCKED (L5).

### 10.1 Relationship rules

- **RL1.** A relationship is created only by a source statement or a reviewed record. Proximity, containment, name match, touching geometry and network topology produce at most an unpublished candidate (adventure model section 3).
- **RL2.** Every relationship has a direction, two stable IDs, an origin (`source_backed`, `derived`, `reviewed_candidate`), evidence, and is stored in a registry, not as a feature property. Unknown is absence.
- **RL3.** A derived relationship names its rule and inputs and is never upgraded to source-backed by repetition.
- **RL4.** A reviewed candidate confirmed against geometry alone stays a candidate and is not published.
- **RL5.** A chain is only as established as its weakest link, and the weakest link is shown.
- **RL6.** Staleness never removes a restricting relationship; a stale supporting relationship is treated as unknown.
- **RL7.** `governed_by` comes only from the trail's own source field naming its managing unit, mapped by a documented, reviewed table to an M5 land unit ID. Lying inside a land polygon is context only. [DRAFT M5 10 rule 1]
- **RL8.** No relationship asserts access, legal travel, parking, camping, current condition or vehicle suitability.

### 10.2 What M6 provides and what it does not

| M6 provides (where the approved source supports it) | M6 does not provide |
|---|---|
| User-facing trail identity with its member map, parts and aliases | Any statement that a trail is continuous, ridable, open or legally accessible |
| Activity and vehicle-class claims, restriction-first, from reviewed instruments, with seasons | Current condition, openness today, closures by order, fire status |
| Management information shown as such | Management information as permission |
| Trailhead or staging identity, where a source provides a site record (L5) | A trailhead invented from a trail end point, a parking area or a road junction |
| `starts_at` links: source-backed where a source or the agency's page names the trail for the site; reviewed candidate; otherwise unknown | `starts_at` from a site touching or lying near a trail. Geometric touching yields an unpublished candidate list only |
| `governed_by` from the trail's own managing-unit field to an M5 land unit, through a reviewed mapping, if M5's unit identities exist (RL7) | `governed_by` from containment in a land polygon |
| Coverage for motorized and non-motorized use rules per trail | "No restriction found" as a result; order coverage (M7) |
| Reserved `constrained_by` link shape from trail to an M7 order entity | Any order entity or order record |
| Reserved `member_of` link to a trail system, populated only from a stating source (8.7) | Membership from an area polygon or name |

### 10.3 Relationship registry

`v2/regions/<id>/trail-relationships.json`, validated, holds `starts_at` and, if approved, `governed_by` and `member_of` links:

```json
{"schema_version": 1,
 "links": [
  {"id": "rel-…", "kind": "starts_at", "from": "trail-…", "to": "<site id>",
   "origin": "source_backed",
   "evidence": {"source_url": "https://…", "agency": "…", "statement": "…", "basis": "manual_review",
                "last_checked_at": "…", "last_confirmed_at": "…", "max_age_hours": 8760}}]}
```

A `derived` link names `rule` and `inputs`. Candidates are written to the build report only, never to this file. A reviewed crosswalk between two sources' records for one route (8.3) is a link of kind `same_route_as` with origin `reviewed_candidate` confirmed against an agency source; which sources it may join is LOCKED (L3).

### 10.4 Relationship to M5, M4, M7 and M8

- **M5 land.** M6 reads M5 land unit IDs for `governed_by` only if the M5 specification is approved with stable unit IDs and the trail source carries a managing-unit field (RL7, M6-D10). M6 never derives land access, and a trail on land the M5 layer leaves unknown stays unknown for access.
- **M4 water.** M6 creates no relationship between a trail and a water feature. A trail named after a creek (Difficult Creek trail and Difficult Creek stream are both in Aspen [MEAS T3] [REPO M4 data]) is not related to it by the name. Water activity claims and trail activity claims are separate registries.
- **M7 camping and orders.** M7 consumes trail IDs, trailhead IDs and `starts_at` links; it owns `approached_via`, road vehicle constraints, day-use and overnight options, orders as entities [DRAFT-PR 35], and `relevant_to`. M6 does not create those.
- **M8.** M8 reads the trail identity, the activity claims per vehicle class, the coverage list and the relationship registry, and lists every absent link as an unknown. M6 must not shape data to make an M8 candidate look complete.
- **Existing straight-line listings** ("Camping nearby", "Trails nearby", "Nearby trails for selected activity") remain distance listings. Under M6 they list trails rather than segments (one row per trail, measured to the nearest member) and keep their straight-line wording. They are not relationships and are never written to the registry.
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
