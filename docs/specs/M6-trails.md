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

SOURCE-NEUTRAL. These are constraints, not strings. **Exact literals are deferred to the owner** (M6-D14): they are drafted in the pull request that first renders them, approved by the owner in that pull request, and then pinned byte for byte by tests, as M4 section 10 and the M5 draft's section 11 do. Manifest wording is trust-bearing and changes only with owner approval (trust principle 8).

### 11.1 Constraints

| ID | Constraint |
|---|---|
| PC1 | **Few and short.** At most 12 new fixed strings in M6, excluding activity and vehicle-class labels. A detail line is at most 90 characters; a label at most 32; a legend line at most 60. Every string fits at 320 px width without truncation in the results sheet. |
| PC2 | **Forbidden words.** No new string contains "verified", "legal", "permitted", "open to", "safe", "current" used of status, "connected" or "continuous", except where the string states that something is *not* established (M3 A4). |
| PC3 | **Status never alone.** A status word (allowed, restricted, prohibited, not established) is always shown with its activity and, for motorized use, its vehicle class. "Motorized" is never a status subject; each class is its own line. |
| PC4 | **Management information is labelled as such.** The source's management strings appear under their own heading, distinct from the designation heading, and never with a status word. Their field names (managed, accepted, discouraged, restricted) are rendered as the source's terms, not as permission. |
| PC5 | **Restrictions first.** Prohibited, then restricted, then allowed, then not established. A review-overdue flag sits on the same line as the restriction it qualifies and never removes it. |
| PC6 | **Parts disclosed.** A trail with more than one part says, in one line, how many separate pieces are shown and that Ohvernight does not establish they connect. |
| PC7 | **Membership disclosed.** The detail states the number of source segments, as M4's WW13 does. |
| PC8 | **Unknown shown, briefly.** With an activity selected, that activity's line always shows, including when not established. With none selected, one line says use is not established for activities without a reviewed record, instead of a list of unknowns. Unknown is never omitted to save space. |
| PC9 | **Current condition.** Every trail detail carries one line saying current conditions and openness are not known to Ohvernight. |
| PC10 | **No map-level status** (follows M4 O3 unless the owner decides otherwise in M6-D13). Trails keep one line colour; status lives in the detail. |
| PC11 | **GPX.** Export of a trail writes one track with one segment per member, and its description says the geometry is source geometry, not a route, and that pieces are not established to connect. |
| PC12 | **Interaction.** A tap on any member selects the whole trail (one casing, one label), as M4 does for rivers. The M4 O6 fit cap (`tap.max_zoom_out`, `list.min_zoom`) is applied to the trail layer through its registry entry, with values confirmed on a device. The adapter is not changed. |
| PC13 | **Saved items.** A saved ID that resolves through `trail-aliases.json` opens the trail; one that resolves to nothing is shown as no longer in the source, never silently dropped. |
| PC14 | **Search and lists.** One row per trail, titled with the source name and the source's route number as published. Straight-line listings keep their straight-line wording and the "connection unverified" marking. |

### 11.2 Detail order (proposed)

Title (source name); route number; source segments (PC7); parts (PC6) where more than one; agency, source link, "Source fetched"; designation section per selected activity or all claimed activities, restrictions first (PC5), each with summary, instrument edition, `Reviewed <date>`, review overdue where it applies; the not-established line (PC8); trailhead section where a `starts_at` link exists, with its origin; coverage lines; management-information section (PC4); current-condition line (PC9); layer limitation. The last line is a fixed statement that a mapped trail is not permission to enter, ride or park (the trail counterpart of M4's WW2).

## 12. LOCKED — Source field mapping (interface only)

**Nothing here maps any field.** Each approved source needs one committed mapping file, `v2/pipeline/config/trail_sources/<namespace>.json`, that declares, for the build and the validator to read:

| L-item | Declares |
|---|---|
| L3 Identity | Segment key field and its documented persistence; route-identity field; the scope field or constant within which the route key is unique; whether any spelling equivalence is documented by the publisher |
| L4 Use | For each 9.1 key: the source field(s), the instrument kind (`legal_designation`, `agency_statement`, `management_information`), the value meaning each status, and the date field with its documented meaning; the narrow/wide width threshold where the source has one; the publishers whose pages count as the designation instrument |
| L5 Sites | Site key, site type values that are trailheads or staging areas, and any field in which the publisher names the trail a site serves |
| L6 Provenance | Service URL and layer, terms reading reference (owner decision record), edition or date field if any, refresh authority |

Validation rules R100, R107 and R118 read this file; until it exists for a namespace, those rules apply only to synthetic fixtures. A mapping that would set `allowed` from a field whose instrument is `management_information` is rejected (R107).

## 13. Contract changes

All additive to contract version 1, documented in `v2/pipeline/docs/data-contract.md` in the pull request that introduces them. Source-specific fields are LOCKED and listed in the PR that adds them.

| Change | PR | Label |
|---|---|---|
| `trail_id` and `legacy_ids` as derived segment properties; the `trail-` namespace; the trail display feature (`id`, `name`, `route_number`, `member_count`, `part_count`, `length_km`, `evidence`) | M6-A (shape), M6-C (data) | NEUTRAL shape |
| `index.json` `trail_groups` (trail ID → ordered member IDs) and `display/trail-aliases.json` with its index entry, as M4 A2 | M6-A, M6-C | NEUTRAL |
| `trail-groupings.json` and manifest `trail_groupings` path | M6-A | NEUTRAL |
| `trail-use.json`, manifest `trail_use` path, the four-status trail claim with `instrument` and `windows` | M6-A (shape), M6-E (records) | NEUTRAL shape |
| `trail-coverage.json`, manifest `trail_coverage` path | M6-A, M6-E | NEUTRAL shape |
| `trail-relationships.json`, manifest `trail_relationships` path | M6-A, M6-F | NEUTRAL shape |
| `fact_coverage.trail_access` may be `reviewed_partial` when `trail-use.json` has a non-unknown claim (extends 5.5 as M4 did for water) | M6-E | NEUTRAL |
| R29's activity key set: kept for the management strings; the 9.1 vocabulary is the claim vocabulary and is separate | M6-A | NEUTRAL |
| R61 exception list extended to the trail grouping rule (a grouped layer's display IDs are trail IDs) | M6-C | NEUTRAL |
| Per-source mapping files (section 12) and any new source fields | M6-D onward | **LOCKED** |
| Register: N1 (no trail transport record) addressed in the first LOCKED fetch PR | M6-D | LOCKED |

## 14. Validator rules

New stable IDs R100–R119. Each has at least one negative fixture and, where it protects real data, a mutation proof on the committed files (local, not committed, listed in the handoff). Rules marked (L) read a LOCKED mapping file and run on synthetic fixtures until it exists.

| ID | Rule | PR |
|---|---|---|
| R100 (L) | Every trail-source segment has `source_namespace` in the namespace table, a non-empty key, and `id` equal to the prefix plus the sanitised key from its own source fields. IDs unique within the region | M6-A, M6-D |
| R101 | Every trail ID matches the 7.2 form, is computed from its identity inputs only, and never equals or begins with a segment or site prefix (TG12, TG13) | M6-A |
| R102 | TG1–TG5 and TG7: every trail's membership has a permitted basis; no trail mixes route keys, scopes or namespaces without a reviewed grouping record naming each | M6-A |
| R103 | TG6 and TG8: no segment in two trails; `trail_groups` equals canonical `trail_id` membership | M6-A |
| R104 | TG10 and TG11: a trail's display geometry equals its members' R63-transformed geometry in member order; `member_count`, `part_count`, `length_km` and `name` equal the computed values | M6-A |
| R105 | TG9: canonical trail-source files differ from their pre-grouping committed state only by `trail_id` (checked by the build test against the snapshot hash, and by R64) | M6-C |
| R106 | `trail-use.json` conforms to 9.2: IDs resolve to displayed trails; every 9.1 key present; status in the set; `unknown` has no other key; complete evidence for every other status; no shared evidence object; `applies_to.segment_ids` are members of the trail | M6-A |
| R107 (L) | Every non-unknown claim has `instrument` `legal_designation` or `agency_statement`; `allowed` only with `legal_designation` (or `agency_statement` if M6-D7 (b)); no `source_url` on a host in the non-claim list; the cited publisher is one the mapping file names for that instrument | M6-A, M6-E |
| R108 | No segment or trail feature, canonical or display, carries a claim, status, access or condition property, or a reserved contract 5.4 property other than `id`, `name`, `evidence` (claims live only in registries) | M6-A |
| R109 | `windows`: `raw` present; parsed pairs equal the fixed parser's output for `raw`; an unparseable `raw` has no parsed pair | M6-A |
| R110 | AE2: no claim object is referenced from two activity keys; e-bike keys are `unknown` unless the mapping file maps a source class to that key | M6-A |
| R111 | `fact_coverage.trail_access` is `reviewed_partial` only when `trail-use.json` has a non-unknown claim, and its `layer_ids` name the trail layer | M6-E |
| R112 | `trail-groupings.json` conforms to 8.3: members resolve; evidence complete; statement non-empty, ≤ 160 characters; no non-claim host; no record whose members already form one source-route trail | M6-A |
| R113 | Repository level: a trail ID present in more than one region has identical non-geometry trail fields in each | M6-A |
| R114 | `trail-relationships.json` conforms to 10.3: kind in the set; both ends resolve; origin in the set; `derived` names rule and inputs; no `reviewed_candidate` without agency evidence; no link of a kind M6 does not provide | M6-A, M6-F |
| R115 | `trail-coverage.json` follows 9.6: subject resolves; category accepted in M6 (`orders` rejected); one record per subject and category; complete evidence | M6-A, M6-E |
| R116 | `trail-aliases.json` keys equal the member and legacy IDs of displayed trails and map to their current trail IDs; index entry path, bytes and SHA-256 match; not in `index.json` | M6-C |
| R117 | `legacy_ids` on segments and trails follow 7.4 (distinct, never on two features, never a current ID) | M6-C |
| R118 (L) | Every mapping file has the L3–L6 keys of section 12, and no use field mapped as `management_information` can yield a status | M6-D |
| R119 | Reserved for an amendment during delivery | — |

R29 is unchanged for the source management strings. R61 is amended, not weakened, for the grouped trail layer as M4 amended it for water.

## 15. Budgets and performance

Inherited unchanged from M3 (section 16, A10, A13) and M4 (section 14):

| Measure | Limit |
|---|---|
| Bytes to "map usable", per region | 500,000 |
| Bytes with every default-on layer, per region | 4,500,000 |
| Region default-on set | ≤ 15,000 features and ≤ 1,500,000 bytes gzipped |
| One display layer | ≤ 5,000 features and ≤ 450,000 bytes gzipped, or `min_zoom`, or split |
| Performance | Map usable ≤ 60% and all default-on layers ≤ 135% of the same-session base median; heap ≤ 115% of base; triggers R-1 to R-5 unchanged |

M6-specific (M6-D15):

| Measure | Today | Limit |
|---|---|---|
| Trail display bytes | Aspen 856,223; Douglas 877,958 [MEAS T2] | Grouping (M6-C) ≤ today's value per region: geometry is unchanged and per-feature properties fall. Any LOCKED source addition is measured and reported in its PR before data is committed; a breach stops the PR |
| `trail-aliases.json`, registries | — | Not requested before "map usable"; registries requested when a trail detail first opens |
| Douglas headroom to map-usable | Small (504,430 before M4 A2 moved the alias map) [REPO M4 A2] | Reported in M6-C; nothing trail-related is added to the initial index |

Three sessions of the unchanged `measure.mjs` at the M6-C head and at any LOCKED PR that changes display bytes, reported pass or miss. A miss is reported, not tuned around.

## 16. Tests

Offline, clock-free, nothing written inside the repository, as M3–M5.

**Python (validator, build):** a negative fixture for every rule R100–R118. Grouping on synthetic fixtures: two segments, one route key, shared end point → one trail, one part (the Difficult Creek shape); same name, shared end point, different route keys → two trails (the Turtle Mountain shape); one route key in four disconnected pieces → one trail, four parts, no added coordinate (the Indian Creek shape, TG10); two pieces 6 m apart stay two parts (8.4); same route key in two scopes → two trails; conflicting names in one route key fail the build; empty route key joins nothing; a reviewed grouping record joins two route keys and a record citing only a name is rejected; a trail ID unchanged when a member is added; legacy matching by geometry; zero-padding near-collision listed and not joined. Claims: each invalid form of 9.2; `management_information` as instrument rejected; `allowed` from an agency statement rejected unless M6-D7 (b); a claim shared by two keys rejected; e-bike from bicycle rejected; window parsing for one window, two windows, year wrap, trailing whitespace and an unparseable value; the freshness table of 9.4 and the date evaluation of AE10 as pure functions with an injected time, including an overdue prohibition still prohibited and an overdue allowed claim not established; a conflict between a restriction and an allowed claim shows the restriction.

**Node:** trail detail order of 11.2; restriction-first ordering; no status word without activity and class; management-information section carries no status word; parts line for a multi-part trail and not for a one-part trail; current-condition line always present; every approved literal against its string; a saved segment ID opens its trail through the alias file and an unresolvable one shows as no longer in the source; GPX of a multi-part trail has one segment per member; fit cap for a short trail and a long trail from a tap and from a list.

**Browser check (both regions, four sizes):** Difficult Creek selects as one trail from a tap on either member, with one casing and one label; Turtle Mountain `0770` and `0770.E` select separately; search lists one row per trail; the trail layer is within budget; detail shows the parts line for INDIAN CREEK; from M6-E a reviewed restriction shows with its source and an overdue flag when the injected time passes its age.

**Mutation proofs (local):** move a segment into another trail in `trail_groups`; merge two route keys without a grouping record; add a coordinate between parts; set an activity to `allowed` with `management_information`; copy one evidence object to two keys; put a status property on a trail feature; give two regions different names for one trail ID; drop an alias. Each must fail its named rule.

## 17. Acceptance

**Engineering, per PR:** offline suites and the browser check pass; display rebuild has no diff; each new rule passes on real data where real data exists, with negative fixtures and mutation proofs; budgets hold; three performance sessions reported where display bytes change; no non-trail canonical file changes; for LOCKED PRs, the snapshot and stability reports are committed and every unexplained difference is resolved or reported.

**Owner gates:** each PR's exact head SHA approved by the owner; the owner approves every literal in the PR that renders it; the owner approves every claim, grouping and relationship record in the PR that adds it; an iPhone Safari check of both regions passes for every PR that changes what the user sees (M6-B, M6-C, M6-E, M6-F).

**Scenario acceptance (milestone close), run by a dedicated tester who did not implement any M6 PR, on a phone:**

1. **Scenario A, Douglas dirt-bike weekend** [REPO]: every measure recorded against the previous result. Source-neutral predictions to be tested, not results: step 1 (choose a trail system) improves, because trails are named units, not segments; step 2 (are motorcycles allowed) improves only for trails with a reviewed designation record and otherwise moves from "done partly, and confusing" to "correctly said unknown"; step 3 (trailhead) improves only where a source-backed `starts_at` link exists; steps 4–7 are not expected to improve and still send the tester elsewhere; the proximity-assumption count must not rise.
2. **Scenario B, Rampart day use** [DRAFT-PR 20]: run as a canonical scenario if PR #20 is merged before M6 closes; otherwise run once as a supplementary scenario with the same steps and recorded beside Scenario A. Source-neutral expectations: the "where to ride" and "motorcycle rules" questions improve only through reviewed designation records; the hammock, fee, family-base and current-status questions are not M6's and must still be answered as unknown; "road rules separate from trail rules" is met if the detail never presents a trail claim as a road claim.
3. **Unknowns are not hidden.** No scorecard line improves by hiding an unknown; fewer apparent unknowns reached by not showing them fails the review (product scorecard). "Activities with actionable restriction evidence" is reported per trail with the count of trails with no reviewed record.
4. The coordinator writes the product review under its six headings and states plainly what M6 delivered without the source policy, if that is the outcome.

## 18. Delivery plan

Small sequential pull requests on Aspen and Douglas County only. Each is independently revertible, leaves `main` green, and needs owner approval of its exact head SHA. **NEUTRAL** PRs can start once this specification is approved. **LOCKED** PRs cannot start until the source policy (PR #24) is approved and the named L-items are recorded.

| PR | Content | Label | Visible change |
|---|---|---|---|
| **M6-A** | Contract shapes of section 13; empty registries and config; rules R101–R104, R106, R108–R110, R112–R115 on synthetic fixtures; R100, R107, R118 scaffolded on fixtures; no data, display or wording change | NEUTRAL | None |
| **M6-B** | Presentation of the existing management strings under PC4, the current-condition line (PC9), the not-established line (PC8) and the mapped-trail statement, with owner-approved literals. No data change; existing straight-line wording kept | NEUTRAL | Wording only |
| **M6-C** | Trail identity on the already-published USFS segments, with no refresh: grouping (section 8), trail display features, aliases, search by trail, interaction (PC12), parts line, GPX; R105, R116, R117 on real data; stability baseline report | **LOCKED (narrow)**: needs only M6-D2, the owner's confirmation that the published layer stays in use and that `trail_number` is its route identity within a stated scope (L3) | Trails become one feature each |
| **M6-D** | Controlled fetch of each approved source; mapping files (section 12); stable segment IDs; legacy matching; snapshot and difference records; transport records (N1) | **LOCKED** | Possibly none |
| **M6-E** | Reviewed activity claims, restriction-first, and motorized and non-motorized coverage, for the initial set: the trails Scenario A's last run evaluated and the Rampart trails PR #20 names, Douglas first; `fact_coverage.trail_access` change | **LOCKED** (instrument publishers, L4) | Designation section in detail |
| **M6-F** | Trailhead and staging identity from an approved site source and `starts_at` links, source-backed or reviewed; `governed_by` if M6-D10 and M5 allow | **LOCKED** (L5) | Trailhead section in detail |
| close | Scenario runs and product review (section 17) | NEUTRAL | — |

If the source policy is declined or delayed, M6-A and M6-B still ship, M6-C ships if M6-D2 is granted on its own, and the milestone review says plainly that activity permission and trailheads were not delivered (M6-D16).
## 19. Rollback

- **M6-A:** revert. No data or visible change.
- **M6-B:** revert; the M3 detail wording returns.
- **M6-C:** revert. Canonical data loses only `trail_id`; display returns to segments; saved segment IDs resolve as before because they were never changed.
- **M6-D:** revert; the snapshot record's pre-fetch SHA-256 values identify the state to return to.
- **M6-E / M6-F:** revert, or empty the registry. With no registry every activity shows not established and no trailhead link is shown.
- **A single wrong claim or link:** set it to `unknown` or delete the link in a one-line change; always safe. A wrong grouping record: delete it; the trails fall back to source-route grouping.

## 20. Risks

Engineering risks with their mitigations. The material risks the owner should weigh are in 22.3.

| Risk | Mitigation |
|---|---|
| Grouping joins or splits wrongly | TG1–TG14, negative fixtures for the Difficult Creek, Turtle Mountain and Indian Creek shapes, the near-miss and zero-padding reports, owner device check |
| A member name conflict blocks the build on real data | Build stops and reports (TG2); no name is picked; the owner decides per case |
| Trail display bytes or performance regress | Budgets enforced; grouping is expected to reduce per-feature properties; report, do not tune |
| Saved plans break | `trail-aliases.json`; PC13; tests for both resolving and non-resolving IDs |
| A claim is wrong at entry | Restrictions first; the instrument publisher's own page only; owner approves each record |
| A claim goes stale | 9.4 freshness; restrictions never weaken; one-line downgrade |
| Two sources disagree | AE8: both kept; never `allowed` from a conflict |
| Research inputs treated as truth | Every [DRAFT-PR] item is an input; `last_confirmed_at` only after the coordinator's read and the owner's approval |

## 21. Unknowns

Stated as unknown; none blocks approval of the source-neutral sections.

- Whether the current segment key (`objectid`) persists across the publisher's releases. [UNK]
- Whether the current route number is unique within a forest, a ranger district or nationally, and so what the scope in 8.2 is (L3). [UNK]
- Which designation instrument the source policy names for motorized use, and its field semantics and date meaning (L4). PR #24 reports map-versus-service disagreements for some Rampart routes. [DRAFT-PR 24]
- Whether any approved site source names the trail a trailhead serves in a structured field (L5). PR #24 found none complete. [DRAFT-PR 24]
- Whether the M5 specification is approved with stable land unit IDs, and whether the trail source carries a managing-unit field (M6-D10).
- Whether PR #20 (Rampart scenario) is merged before M6 closes.
- How many pilot trails will have a reviewed designation record in M6-E.
- Whether 12 new strings (PC1) are enough once the detail is drafted.

## 22. Owner decision packet

One packet. The owner can acknowledge 22.1 explicitly (silence is not approval), approve 22.2 in one reply ("accept the recommended defaults", or list exceptions by ID), and should read 22.3 before replying. A recommendation is the coordinator's proposal only.

### 22.1 Settled by default (no decision needed; already binding)

These follow from approved repository documents and are restated, not chosen, here:

1. Unknown is the default and is shown as unknown (trust principle 1, contract rule 1).
2. Never infer permission or access from a mapped trail, ownership or proximity (trust principle 2, contract rule 15).
3. Staleness never weakens a restriction; positive claims fail closed (trust principles 5 and 6, contract rules 6 and 14).
4. Presentation never exceeds the evidence; trust-bearing wording changes only with owner approval (trust principles 7 and 8).
5. Canonical source records are preserved; trails are not merged or renamed on geometric continuity or matching names alone; identity survives a jurisdiction or package boundary (ROADMAP M6).
6. Proximity is not a relationship; relationships are source-backed, reviewed or unknown (product principle 12, adventure model section 3).
7. No community or third-party content in production data (M4 D8).
8. Budgets and performance limits inherited from M3 and M4.
9. Milestone close requires a phone run of the canonical scenario by an independent tester and the six-heading product review (product scorecard).
10. No merge without the owner's approval of the exact head SHA; no ROADMAP, trust-principle or contract-rule change outside its own approved pull request.

### 22.2 Recommended defaults (acceptable in one reply)

| ID | Decision | Options | Recommendation | Bear case against it |
|---|---|---|---|---|
| M6-D1 | Scope and delivery | (a) PRs M6-A to M6-F on Aspen and Douglas only, neutral PRs first; (b) one combined PR after the source policy | (a) | Six gates and up to four device checks; owner bandwidth may be the binding constraint |
| M6-D2 | Narrow unlock for M6-C | (a) Confirm now that the already-published USFS trails layer keeps its segment-geometry and route-identity roles and that `trail_number` is its route identity within a stated scope, so M6-C can proceed before the full policy; (b) wait for the full source policy | (a), only if the owner is comfortable deciding this one role ahead of PR #24 | It pre-empts part of the source policy; if PR #24 later changes the geometry source, trail IDs and aliases are reworked |
| M6-D3 | Vocabulary and statuses | (a) The 9.1 keys, including reserved e-bike classes and `ohv_wide`, and the four statuses `allowed`, `restricted`, `prohibited`, `unknown`, matching M4; (b) three states `allowed`, `prohibited`, `unknown` | (a) | `restricted` is broad; a reader may not distinguish "season only" from "permit only" without reading the summary |
| M6-D4 | Disconnected pieces of one source route | (a) One trail with several parts, disclosed (PC6), no line between parts; (b) M4's model: each part its own trail with the same name | (a) | See MR3: a single trail feature invites a continuity assumption even with the parts line |
| M6-D5 | Reviewed grouping records | (a) Mechanism in M6-A, file ships empty unless the owner supplies records; (b) no mechanism in M6 | (a) | An empty mechanism is unused surface area; the first record will set precedent for what "one trail a user would name" means |
| M6-D6 | Adjacency tolerance | (a) Exact at six decimals, near-misses within 25 m reported only; (b) a snapping tolerance | (a) | Real pieces 6 m apart (Indian Creek) stay separate parts, which under (a) of M6-D4 only changes the parts count, but under (b) of M6-D4 creates two trails |
| M6-D7 | What can produce `allowed` | (a) Only a reviewed legal designation; (b) also a reviewed agency use statement; (c) also a validated structured field without manual review | (a) for M6, with (b) for non-motorized activities only as a later amendment | Hiking, biking and equestrian use is rarely legally designated, so under (a) almost every non-motorized activity stays not established |
| M6-D8 | Concurrent routes on one segment | (a) A segment belongs to at most one trail (TG6); concurrency only via a reviewed record; (b) many-to-many membership | (a) | A real shared section (two named trails on one tread) shows under one trail only |
| M6-D9 | Trail systems and recreation areas | (a) Reserved entity and `member_of` link; none created unless a stating source is approved; (b) create from reviewed agency pages in M6 | (a) | Rampart is a named area users think of as one place; (a) leaves it absent in M6 |
| M6-D10 | `governed_by` to M5 land units | (a) Only if M5 is approved with stable unit IDs and the trail source has a managing-unit field, through a reviewed mapping; otherwise deferred; (b) defer to M8 | (a) | Couples M6 to an unapproved M5 draft |
| M6-D11 | Roads and `approached_via` | (a) M7, sharing the 9.1 vehicle-class vocabulary; (b) M6 | (a) | Scenario A step 4 and Rampart's road-rules question do not improve in M6 |
| M6-D12 | Freshness defaults | (a) 2,160 hours for claims, shorter for seasonal at the reviewer's choice; 8,760 for grouping and relationship records; (b) 720 hours for motorized claims | (a) | See MR5; 90 days may be long for designations re-issued each season |
| M6-D13 | Map-level status | (a) None, as M4 O3; status in the detail; (b) a neutral style for trails with a reviewed motorized prohibition | (a) | A rider scanning the map cannot see where motorcycles are prohibited without opening each trail |
| M6-D14 | Wording process | (a) Constraints PC1–PC14 now; literals drafted and approved in the PR that renders them; (b) all literals in this specification before approval | (a) | Literals approved one PR at a time can drift in tone; owner sees them piecemeal |
| M6-D15 | Budgets | (a) Section 15: inherited limits, grouping ≤ today's bytes, new sources measured before commit; (b) a fixed trail-layer byte cap now | (a) | Without a number, a LOCKED source could arrive large; the stop-and-report rule is the only control |
| M6-D16 | What completes M6 | (a) M6-A, B, C, E and F, with D as needed; if the source policy is declined, A to C with the review saying plainly that activity permission and trailheads were not delivered; (b) M6 is not complete without E | (a) | A milestone titled Trails could close without answering "may I ride here?" for any trail |

### 22.3 Material risks (flagged separately)

| ID | Risk | Bear case |
|---|---|---|
| MR1 | **The source policy stays undecided.** M6-C to M6-F wait on PR #24. | M6 ships identity and wording only; Scenario A step 2 moves at best from "partly, confusing" to "correctly unknown", and the milestone is foundation, not product. Building identity on the current source first (M6-D2) may then need rework. |
| MR2 | **Route identity is the wrong key.** Grouping by the source route number is safe only if the number means "one trail" within the stated scope. | If numbers are reused across units, recycled, or assigned to segments rather than routes, number-based grouping is the "merge on a matching label" error in another form, and it would ship to every user on day one of M6-C. |
| MR3 | **One trail feature implies continuity.** Under M6-D4 (a), Indian Creek is one trail in four pieces, up to about 2.3 km apart. | The parts line may be ignored on a phone; a rider can plan through a gap that is a private inholding or does not exist on the ground. GPX of the whole trail makes the gap easy to miss. |
| MR4 | **Designation versus management confusion persists, or worsens.** Research reports disagreements between a designation map and its service fields for some Rampart routes. [DRAFT-PR 24] | Under AE8 every conflicted trail shows "not established" for motorcycles; on the very trails riders care about the product appears to regress, and the pressure to pick a reading will be strong. |
| MR5 | **Review load and ageing.** Every positive claim reverts to not established after its age. | With one reviewer and a 90-day default, the product's allowed answers decay each season unless reviews keep pace; Scenario A scores can fall between milestones with no code change. |
| MR6 | **Identifier persistence is unknown.** Segment IDs use `objectid`, whose persistence is not established. | A refresh that re-keys or re-segments could orphan saved items and claims; geometry matching cannot follow a re-segmented trail, and claims scoped to segment IDs would silently lose their subject. |
| MR7 | **A seasonal window read the wrong way round.** Designated-open windows and restriction windows have opposite meanings; the source's legend decides which (L4). The Rampart baseline is already auditing a `12/01-03/14` reading. [DRAFT-PR 20] | One mis-mapped field displays a prohibited season as allowed, the exact false positive trust principle 6 forbids, on every trail sharing that value. |

**Unlock.** Approving the M6 source policy (PR #24) — the sources per role, their terms reading, and the L3–L6 mappings — unlocks M6-C (without needing M6-D2), M6-D, M6-E and M6-F.

## Appendix A. Evidence basis

| Fact | Basis | Where |
|---|---|---|
| Segment counts, trail numbers, connectivity, Difficult Creek, Turtle Mountain, Indian Creek, padding, activity values, display bytes, saved-plan storage | [MEAS] | [m6-spec-evidence.md](../research/m6-trails/m6-spec-evidence.md) T1–T6 |
| Trail ID form, activity keys and verbatim strings | [REPO] [MEAS] | `v2/pipeline/scripts/fetch_trails.py`; contract R29 |
| Browser handling of use dates and straight-line listings | [MEAS] | `v2/explore/trail-seasons.js`, `browse.js`, `capabilities.js` |
| Trust rules, evidence semantics, fact coverage, display rules, register N1 | [REPO] | `docs/product/trust-principles.md`; `v2/pipeline/docs/data-contract.md` |
| User-facing trail identity requirement, product-alignment expectations | [REPO] | `ROADMAP.md` M6 |
| Relationship origins, coverage model, M6 obligations to M8 | [REPO] | `docs/architecture/adventure-model.md` sections 3–5 |
| Package boundary implications | [REPO] | `docs/architecture/continuous-explore.md` |
| Grouping, claim, freshness, alias and wording precedents | [REPO] | `docs/specs/M4-functional-recreational-water.md` sections 7–11, A1–A4, O3, O6 |
| Rule numbering after R85; coverage-record shape; `governed_by` rule | [DRAFT M5] | `k-kopacek/m5-spec-draft`: `docs/specs/M5-land-classification.md` sections 9, 10, 13 |
| Source-policy proposal, candidate concepts, route-label match sample (14/25), map-service conflicts | [DRAFT-PR 24] | `docs/research/m6-trails/m6-source-policy-proposal.md` on `docs/m6-source-policy-proposal` |
| Per-class designation shape, date parsing states, candidate-only joins | [DRAFT-PR 33] | `docs/research/m6-trails/m6-prototype-notes.md`, `v2/pipeline/prototypes/m6/motorized_evidence.py` |
| Model gaps: conflicting readings, instruments, day use | [DRAFT-PR 29] | `docs/research/m8-adventure/rampart-worked-example.md` |
| Rampart scenario, baseline, `12/01-03/14` audit | [DRAFT-PR 20] | `docs/product/acceptance-scenario-rampart-day-use.md` on `docs/rampart-day-use-scenario` |
| Orders as entities (M7) | [DRAFT-PR 35] | `docs/research/m7-camping/orders-as-entities.md` |
