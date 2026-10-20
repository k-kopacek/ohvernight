# Milestone 7 specification — Camping and dispersed camping

Status: DRAFT — NOT APPROVED. Source-neutral sections proposed for owner review; source-dependent sections LOCKED.

**For:** Codex (implementation), once approved. **Reviewer / coordinator:** Claude. **Research:** coordinator; Hermes optional. **Base:** `main` at `c04f5d6`.
**Delivery (proposed):** small sequential pull requests on the two pilot regions only (section 20), each marked NEUTRAL or LOCKED. The neutral ones can start once this specification is approved; the LOCKED ones wait for the owner's source decision.
**Owner decisions:** section 24 is one consolidated packet: what is already settled, recommended defaults the owner can accept in one reply, and material risks flagged separately with their own decisions. Routine engineering choices are decided in the body and listed in 24.4. Where this document says "M7 does X", read "this draft proposes that M7 does X, subject to the decision named".

Governing documents: `AGENTS.md`, `ROADMAP.md` (M7, including the product-alignment expectations of 2026-10-08, and M8), `docs/agent-stack/roles.md`, `docs/product/trust-principles.md` (normative), `docs/product/product-principles.md`, `docs/product/product-scorecard.md`, `docs/product/acceptance-scenario-douglas-dirt-bike.md`, `docs/architecture/adventure-model.md`, `docs/architecture/continuous-explore.md`, ADR-005, ADR-006, `v2/pipeline/docs/data-contract.md` (normative for data), and `docs/specs/M4-functional-recreational-water.md` (the format model, and the claim, freshness and wording precedents of its sections 9 and 10).

## 0. Reading this draft

### 0.1 What is settled, proposed and locked

| Label | Meaning |
|---|---|
| **SOURCE-NEUTRAL** | A rule that holds whichever source the owner approves. Proposed for approval now. |
| **LOCKED** | Depends on which source is used, how its licence or terms are read, or how one source's fields map. This draft states only the interface and the decision needed. Nothing in a LOCKED section is chosen. |
| **NORMATIVE (restated)** | Already binding through the trust principles, the data contract or an approved specification. Restated so the M7 rules can cite it; this draft does not change it. |

Section 4 lists every section with its label.

### 0.2 Evidence marks

| Mark | Meaning |
|---|---|
| [REPO] | Read from a normative or approved repository document on `main` |
| [MEAS En] | Measured from committed files on `main` for this draft; recorded in [m7-spec-evidence.md](../research/m7-camping/m7-spec-evidence.md) as E1–E11 |
| [DRAFT-PR n] | Stated in an unmerged, unreviewed research pull request; not re-checked; not product truth |
| [DRAFT M5], [DRAFT M6] | Stated in the unapproved M5 draft (`k-kopacek/m5-spec-draft`, `2c329e3`) or M6 draft (`k-kopacek/m6-spec-draft`, `82a3c84`) |
| [INF] | Inference in this draft from the marked facts |
| [UNK] | Not established by anything read |

No network request was made to any publisher for this draft. Every [DRAFT-PR] input is a proposal: PR #35 (forest orders as entities), PR #15 (the M7 camping evidence-model draft and the Hermes overnight-sources report), PR #29 (Rampart worked example) and PR #20 (Rampart day-use scenario). Every statement those drafts make about an order, a date or a fire stage was an agent's retrieval, which is not a review (trust principle 4); this draft uses them only to shape the model and the fixtures, never as data.

### 0.3 Numbering

- Validator rules continue after the M6 draft's last rule, R119, with a gap: M7 rules are **R130–R149**. R120–R129 stay free for M6 amendments. [MEAS E10]
- Entity and identity invariants are **EI1–EI9**. Camping-evidence invariants are **CE1–CE14**. Order invariants are **OR1–OR11**. Vehicle and setup invariants are **VS1–VS9**.
- Relationship rules continue the M6 draft's RL1–RL8, which apply unchanged: M7 adds **RL9–RL15**.
- Presentation constraints are **CP1–CP17** (the `C` keeps them distinct from M6's PC1–PC14).
- Hard-coded behaviours found in the code are **H1–H14** (section 12).
- LOCKED interfaces continue the M6 draft's L1–L6: M7's are **L7–L11**.
- Owner decisions are **M7-D1 to M7-D20**; material risks are **M7-MR1 to M7-MR7**.

## 1. Problem

**The product says nothing affirmative about camping, which is right, but it still acts on camping rules that nobody reviewed.** `camping_permission` is `unknown` on all 108 features of the Aspen bundle that carry it, and fact coverage for `camping_permission` is `none` in both regions. [MEAS E1, E3] Behind that, `v2/trip-rules.js` turns three hand-written fields on curated listings into exclusions for every trip: a stay limit, a "tent-only" flag that assumes the visitor sleeps in a vehicle, and a high-clearance flag. [MEAS E1] [REPO `trip-rules.js:28-34`] These are the "inappropriate hard-coded camping-rule behaviour" the roadmap names. Section 12 lists all fourteen found.

**The largest overnight object on the Aspen map is computed, not sourced.** Fifty-one "Areas to research" polygons, on by default and 709,990 display bytes, are a 300 ft buffer around roads that an MVUM evaluation for one past trip called `designated_open`, intersected with land whose generalized manager is USFS or BLM. [MEAS E1, E2, E8] No source names those strips as camping places, the buffer distance cites no order, and choosing land by its manager is the inference M5 forbids. [DRAFT M5 10 rule 2] Research reports that some of them sit on ground a current order closes to camping. [DRAFT-PR 15] [UNK whether that is so]

**Rules exist only as prose and orders.** In Douglas the only overnight rules in the product are nine sentences inside the source's free-text `restrictions` field, such as "Overnight use prohibited." on two picnic sites, which the Browse detail never shows because it stops early for picnic sites. [MEAS E3, E6] The Rampart designated dispersed area is a hard-coded record in a region JavaScript file (register N7). [MEAS E4] Research found that forest orders, the instruments that actually close or limit camping, are published as PDFs with exhibits, carry their own scope and dates, and supersede one another; no structured order source was found. [DRAFT-PR 35] [DRAFT-PR 15]

**Vehicle words do not agree.** Aspen uses `passenger_car`, `high_clearance` and `motorhome`; Douglas stores the display labels "Car / SUV", "High-clearance vehicle", "Truck with trailer" and "Motorhome / RV", and evaluates nothing with them. The M6 draft adds trail classes such as `motorcycle` and `four_wheel_drive`. [MEAS E5] [DRAFT M6 9.1] A trailer is not a vehicle class in any of them, yet Scenario A's fixed profile is a pickup towing a trailer. [REPO scenario A]

**Nothing links an overnight option to anything.** The only connection offered between a campground and a trail is straight-line distance, labelled as such. [REPO adventure-model section 1] There is no backup concept, so its absence cannot be stated.

## 2. Goals and the product question

1. **Overnight places with identity.** Developed campgrounds, designated dispersed areas, agency-described corridors and individual sites are distinct, identified entities, never computed from geometry (section 7).
2. **Camping permission as evidence.** For each place and each overnight setup, the answer is `allowed`, `restricted`, `prohibited` or `unknown`, scoped to that place and to dates, from a reviewed instrument. Permission is never inferred. Staleness never weakens a restriction (section 8).
3. **Orders as first-class entities**, with issuer, number as printed, stated scope and dates, provisions, supersession and history, and with fire restrictions held the same way (section 9).
4. **Vehicle and setup suitability as evidence,** on one vocabulary shared with M6, where a reviewed constraint can exclude and nothing can certify suitability (section 10).
5. **Relationships M8 can use:** `constrained_by`, `approached_via`, `governed_by`, and `relevant_to` only as an established chain; and a backup option identified where an independent one is established, with its absence stated (section 11).
6. **The hard-coded rule behaviour removed** without dropping any restriction it carried (section 12).

**Product question (product principle 15).** After M7 a Douglas rider can open a campground and see, for a tent, a vehicle and a trailer separately, whether a reviewed agency statement says camping is allowed, restricted or prohibited there for their dates, or that it is not established; can see which reviewed orders and fire restrictions constrain that place, with their dates and where they came from; can see whether a reviewed constraint excludes their pickup and trailer from the approach, without ever being told the approach is suitable; can see whether another overnight option is established as an independent backup, or that none is; and can see which of these questions Ohvernight checked and which it did not. A rider still cannot learn availability, current conditions or whether a gate is open today. If the source policy is not approved, M7 can deliver goal 6, the removal of the computed areas and the identity of already-published records, and must say plainly that goals 2–5 are not delivered as data (section 20).

## 3. Out of scope

- **Choosing a source, reading a licence or terms, or mapping one source's fields.** All LOCKED (sections 6 and 14).
- **Availability and vacancy.** Never a claim and never a status. A booking link is shown only beside the statement that availability is not known (CP5). Research found no public availability field. [DRAFT-PR 15]
- **Current conditions and openness today.** M7 stores no open/closed flag, gate state, snow or road condition. A source's own status field stays a labelled source fact (CP13).
- **Dispersed camping outside designated sites**, at corridor, area or unit scope, as a positive answer (M7-D15). The published position near the pilots' roads is restrictive. [DRAFT-PR 15]
- **Computed camping geometry** of any kind: buffers, setbacks, "possible" land, synthetic campsite points (contract rule 9).
- **Digitizing order exhibits** into geometry. An order's scope is held as stated (section 9).
- **Trip assembly, ranking and routing** (M8). M7 provides predicates and data, not candidates.
- **Lodging permission.** The Aspen lodging record keeps its present wording; M7 makes no lodging claim.
- **Community, partner or third-party camping content** and ratings (M4 D8).
- **Any change to the region loader, the map adapter and its exports, Leaflet, ADR-006, a new dependency, build step or basemap**, and the root legacy site's own `trip-rules.js`. [MEAS E7]
- **Changes to land, water or trail data**, except where M7 reads M5 land unit IDs and M6 trail and trailhead IDs for relationships.

## 4. Section map: source-neutral and LOCKED

| § | Section | Label | Can the owner approve it now? |
|---|---|---|---|
| 1–3 | Problem, goals, scope | SOURCE-NEUTRAL | Yes |
| 5 | Evidence model | SOURCE-NEUTRAL | Yes |
| 6 | Sources | **LOCKED** (L7, L10) | Interface only |
| 7 | Entities and identity | SOURCE-NEUTRAL; which source key forms a place ID, and which source site types are which kind, are **LOCKED** (L8) | Rules yes; keys no |
| 8 | Camping-permission evidence | SOURCE-NEUTRAL; which publishers' pages count as an instrument is **LOCKED** (L7) | Yes |
| 9 | Orders and fire restrictions | SOURCE-NEUTRAL; which issuers' publications are read is **LOCKED** (L7) | Yes |
| 10 | Vehicle and setup suitability | SOURCE-NEUTRAL; the road-designation instrument and its field mapping are **LOCKED** (L9) | Yes |
| 11 | Relationships | SOURCE-NEUTRAL | Yes |
| 12 | Removing the hard-coded behaviour | SOURCE-NEUTRAL | Yes |
| 13 | Presentation constraints | SOURCE-NEUTRAL (literals deferred to the owner) | Constraints yes; literals later |
| 14 | Source field mapping | **LOCKED** (L11) | Interface only |
| 15 | Contract changes | SOURCE-NEUTRAL shapes; source fields **LOCKED** | Shapes yes |
| 16 | Validator rules | SOURCE-NEUTRAL; three rules take a LOCKED parameter | Yes |
| 17–19 | Budgets, tests, acceptance | SOURCE-NEUTRAL | Yes |
| 20 | Delivery | SOURCE-NEUTRAL plan; PRs marked NEUTRAL or LOCKED | Yes |
| 21–23 | Rollback, risks, unknowns | SOURCE-NEUTRAL | Yes |
| 24 | Owner decision packet | — | Decisions |

Count: **20 sections are source-neutral** (1–3, 5, 7–13, 15–23) and **2 are LOCKED in full** (6, 14). Six of the neutral sections carry a named LOCKED parameter that they do not choose (7, 8, 9, 10, 15, 16). Section 0 is the reading guide, section 4 this map and section 24 the decision packet.

## 5. Evidence model

### 5.1 Classes (NORMATIVE, restated from M4 section 4)

| Class | In M7 | Can it state that camping is allowed, restricted or prohibited? |
|---|---|---|
| Source fact | A facility or site record: existence, location with its basis, source site type, the source's own season, status, fee and restriction text | No. Source restriction text is shown as source text (CP13), never parsed into a claim (M7-D13) |
| Official recreation information, reviewed | An agency or operator page for one place, or an order, read by a person (sections 8 and 9) | **Yes, and only this class** |
| Derived fact | Distance, a date-window parse, an order's applicability where a permitted derivation rule applies (11.2) | No. A derived applicability can carry a restriction to a place, never a permission |
| Community signal | None. No field allows one | No |

### 5.2 The overnight question, decomposed

"Can I stay here?" is several questions. A value in one never implies a value in another (trust principle 3). [DRAFT-PR 15 section 3]

| Question | Held in M7 as | Can it make camping allowed? |
|---|---|---|
| Existence: does a source list the place? | Source fact on the place record | No |
| Management: whose rules apply? | `governed_by` to an M5 land unit, from the place's own source field (RL9) | No (M5 rule 2) |
| Camping rule: what does the agency say about camping here, for this setup? | Claim per setup (section 8) | **Yes**, only at site scope (CE5) |
| Orders and closures: what instruments constrain it, when? | Order entities and `constrained_by` links (section 9) | No; restrict only |
| Fire restriction | Order entity of type `fire_restriction` (9.6) | No; it is beside the camping answer, never an input to it |
| Vehicle and approach: can this vehicle lawfully get there and occupy the site? | Constraints and `approached_via` (sections 10, 11) | No; a constraint can only exclude |
| Season | Claim windows and order dates (8.5, 9.3) | No date creates permission (CE10) |
| Reservation and fee | Claim conditions (8.3) | No |
| Availability | Not modelled | — |

### 5.3 Never (NORMATIVE, restated for camping)

1. A listed facility, an inventory record, a mapped area or a reservation link is not camping permission (trust principle 2, contract rule 15).
2. Land ownership, managing agency, a land unit's designation or a public-land polygon is not camping permission (contract rule 12; [DRAFT M5] 10 rule 2).
3. A mapped road, a road designation or an MVUM date window is not camping permission and not current passability (contract rule 15).
4. The absence of a loaded order is not openness and not "no restriction" (trust principle 2; adventure model coverage rule 2).
5. One setup never implies another: a tent claim says nothing about sleeping in a vehicle, and neither says anything about a trailer.
6. A successful retrieval never advances a confirmation; an agent's retrieval is not a review (contract rule 2; trust principle 4).
7. Proximity is not a relationship (product principle 12); a name match or a geometry match never creates an identity or a relationship (adventure model rule 6).

## 6. LOCKED — Sources (interface and decision only)

**This section chooses nothing.** It states what any overnight source must supply for the source-neutral sections to work, and the decision the owner must make. Candidates named in research [DRAFT-PR 15] [DRAFT-PR 35] include the sources already published (USFS recreation-site records in Douglas, Recreation.gov/RIDB facility records and hand-curated listings in Aspen, MVUM road designations in Aspen), forest order publications, ranger-district and recreation-area pages, operator pages, county fire pages, and state and BLM rule pages. This draft takes no position on any of them, including on the RIDB access agreement (M7-MR6).

### L7. The source interface

A source is usable by M7 only if, for each role it is approved for, the owner's source decision records:

| Interface item | Needed by | What must be recorded |
|---|---|---|
| Role | §6 | One or more of: place existence; place location; source site type; camping instrument (site page); order or fire instrument; road vehicle designation; place vehicle condition; reservation link |
| Scope | §8, §9 | What the source is authoritative for, and what it does not establish (contract `sources.<id>.scope`) |
| Namespace | §7 | A constant `source_namespace` and ID prefix (7.4) |
| Place key | §7 | The field that identifies a place, and whether the publisher documents it as persistent (L8) |
| Instrument publishers | §8, §9 | Whose pages count as an instrument for which scope: for example, the managing agency's own page for its own site; an order only from its issuing unit |
| Quotation | §9 | Whether short quotations of an instrument may be stored and published (9.2), under the owner's terms reading |
| Terms reading | all | The owner's recorded reading of reuse, storage and redistribution terms (L10) |
| Refresh | §20 | Whether a controlled fetch is authorised, with the snapshot record of M4 section 5 |

### L10. The decision needed

> **Which sources fill which overnight roles in the two pilot regions, under which terms reading?**

Until it is made, the LOCKED pull requests of section 20 do not start, no new source is fetched and no source-specific mapping is written. Whether the overnight sources already published in both regions may keep their present roles while the policy is decided is itself part of this decision (M7-D2); this draft does not assume it.

## 7. Entities and identity

SOURCE-NEUTRAL rules. Which source key forms each place ID, and which source site types map to which kind, are LOCKED (L8).

### 7.1 Overnight places

An overnight place is one identified thing a person could stay at or within. It is either a canonical source record (a feature or place-list item, preserved as published) or a reviewed place record (7.3). Every place has exactly one `place_kind`:

| Kind | What it is | Geometry | Notes |
|---|---|---|---|
| `developed_campground` | An agency- or operator-run facility with defined sites. Group and equestrian campgrounds are this kind with the source site type kept (for example Douglas `HORSE CAMP`) | Point with a stated `location_basis` | [MEAS E3] |
| `designated_dispersed_area` | An area where the agency states that camping is at designated sites only, without the sites mapped | `null`, or a source-published geometry labelled with its precision | Rampart Range, Lincoln Creek are the shapes [MEAS E1, E4] |
| `dispersed_corridor` | A road- or trail-defined strip the agency describes in words | `null`, or source-published only | Never computed. The 51 Aspen research polygons are not this kind (12.2) |
| `campsite` | One individual site | Point, only from a source that publishes it | Never synthetic (contract rule 9); `part_of` its campground or area only where a source states it (RL13) |
| `day_use_site` | A picnic or day-use place | Point | `use_period: day_use`. It may carry an overnight prohibition; it never satisfies an overnight need (CE13) |
| `lodging` | A room operator | Point | Present in Aspen. No camping claim is made about it |

`use_period` is `overnight`, `day_use` or `unknown` and comes from the source or the reviewed record, never from the name. A source site type that is not overnight-relevant (for example `TARGET RANGE`) maps to `not_overnight`; nothing is dropped silently (R145).

### 7.2 Orders, fire restrictions and units

- An **order** is an instrument (section 9): an independently identified entity with issuer, number as printed, stated scope, stated dates and provisions. It is not a property of a place.
- A **fire restriction** is an order of instrument type `fire_restriction` (9.6).
- A **governing unit** is an M5 land unit (forest, district, park) identified by M5's IDs. [DRAFT M5 7] M7 creates no unit entity.

### 7.3 Reviewed place records

Where a responsible agency's own page describes a place that no approved source holds as a record (Rampart's designated dispersed area is the current case [MEAS E4]), a reviewed place record in `v2/regions/<id>/overnight-places.json` may establish its existence:

```json
{"schema_version": 1,
 "places": [
  {"id": "place-rv-…", "name": "…", "place_kind": "designated_dispersed_area", "use_period": "overnight",
   "geometry": null, "location_basis": "No location published; area named by the agency",
   "evidence": {"source_url": "https://…", "agency": "…", "statement": "Short factual statement of what the page establishes about existence.",
                "basis": "manual_review", "last_checked_at": "…", "last_confirmed_at": "…", "max_age_hours": 8760}}]}
```

The statement says what the page establishes about the place's existence and kind, never about permission, at most 160 characters, never a quotation longer than 25 words. A reviewed place record never carries geometry the source did not publish.

### 7.4 Identifiers (decided engineering choice; the coordinator may change it)

| Thing | ID form | Rule |
|---|---|---|
| Place from a source record | Unchanged: the source record's existing canonical ID (`recreation-<n>`, `ridb-<n>`, curated keys) | Which source key forms a new place ID is LOCKED (L8). Until then M7 changes no place ID |
| Reviewed place | `place-rv-<sanitised reviewer key>` | 7.3 only |
| Order | `order-<issuer code>-<sanitised number as printed>` | Number compared exactly as printed; never borrowed from another instrument (OR2) |
| Order with no confirmed number | `order-<issuer code>-nn-<sanitised reviewer key>` | `order_number_as_printed: null` |
| Fire restriction | `fire-<jurisdiction code>-<sanitised key>` | |
| Relationship | `rel-<kind>-<sanitised from>-<sanitised to>` | |

Sanitising lowercases and removes characters outside `[a-z0-9-]`; the unmodified value stays in its own field. Issuer and jurisdiction codes are a fixed table in `v2/pipeline/config/overnight.json`. If two records produce one ID, the build stops and reports; there is no suffix. Legacy IDs follow M4 amendment A4. The prefixes `place-rv-`, `order-`, `fire-` and `rel-` are reserved and never begin a source-record ID (R146).

### 7.5 Identity invariants (validated; R130, R146, R147)

- **EI1.** A place has exactly one kind and one use period.
- **EI2.** A place's geometry is the source's geometry or null. No buffer, centroid of a road, setback or synthetic point is a place (contract rule 9).
- **EI3.** Two records are the same place only where a source-stated shared key establishes it (declared in the mapping file, L8), or a reviewed `same_place_as` link names both (RL13). Never by name, proximity or a facility name containing a road name. [MEAS E7: today's de-duplication uses `ridb_facility_id`]
- **EI4.** A campsite is `part_of` a campground or area only by a source statement.
- **EI5.** An order's identity is its issuer and its number as printed. A title, a URL or a facility name is not an order identity. [DRAFT-PR 35]
- **EI6.** An order that crosses region packages (forest-wide) has one ID and identical non-geometry fields in every package that holds it (continuous-explore implication 3; R147). Evidence about its applicability does not merge across packages (CE12).
- **EI7.** No region JavaScript file defines a place, order or rule record (register N7; tested in 18).
- **EI8.** Every source site type in a published overnight-relevant layer is mapped to a kind or to `not_overnight` (R145).
- **EI9.** A legacy ID once recorded stays recorded; a feature's own ID is never in its `legacy_ids` (M4 A4).

## 8. Camping-permission evidence

SOURCE-NEUTRAL. Which publishers' pages count as an instrument for which scope is LOCKED (L7).

### 8.1 Setups

A claim is per **setup**: how the person sleeps. Setups are modelled independently; no answer is derived from another (CE3).

| Key | Meaning |
|---|---|
| `tent` | Sleeping in a tent at the place |
| `vehicle_sleeping` | Sleeping in or on a passenger vehicle, van, truck or camper shell |
| `trailer_or_rv` | Sleeping in a towed trailer or a self-contained motorhome |
| `hammock` | Reserved. `unknown` everywhere unless a reviewed page states it; trees being present establishes nothing [DRAFT-PR 20] |

Setups are not vehicle classes. A vehicle class (section 10) is what you drive; a setup is how you sleep. A pickup towing a trailer that carries a bike, with the rider in a tent, is vehicle class plus towing for the approach, and `tent` for the night.

### 8.2 Scope of a claim

| Scope | Subject | Highest status it may carry |
|---|---|---|
| `site` | One place (any kind of 7.1) | `allowed` |
| `area` | A named area or an order's described area | `restricted` |
| `corridor` | An agency-described strip | `restricted` |
| `unit` | A whole forest, district or park, as a default rule (for example a stay limit across a forest) | `restricted` |

`prohibited` is available at every scope. `allowed` is available only at `site` (CE5). An area, corridor or unit rule can say "designated sites only", "prohibited" or "no more than N days", never "camping allowed along here". [DRAFT-PR 15 4.2 B]

### 8.3 The claim registry

`v2/regions/<id>/overnight-use.json`, curated, validated:

```json
{"schema_version": 1,
 "records": [
  {"subject": {"kind": "place", "id": "recreation-…"}, "scope": "site",
   "claims": {
     "tent": {"status": "restricted", "instrument": "agency_statement",
       "conditions": {"stay_limit_days": 14, "reservation": "required", "fee_stated": true,
                      "designated_sites_only": true, "max_vehicle_length_ft": null},
       "windows": [{"raw": "05/15-09/30", "start": "05-15", "end": "09-30"}],
       "summary": "Reservation required; stated season only.",
       "evidence": {"source_url": "https://…", "agency": "…", "basis": "manual_review",
                    "source_edition": null, "last_checked_at": "…", "last_confirmed_at": "…",
                    "max_age_hours": 2160, "effective_from": null, "effective_to": null}},
     "vehicle_sleeping": {"status": "prohibited", "instrument": "agency_statement", "summary": "…", "evidence": {"…": "…"}},
     "trailer_or_rv": {"status": "unknown"},
     "hammock": {"status": "unknown"}},
   "exempted_by": [],
   "notes": []}]}
```

| Field | Rule |
|---|---|
| `subject` | A place ID for `site` scope; an order ID, an M5 unit ID or a reviewed area/corridor place ID for the other scopes |
| `status` | `unknown`, `allowed`, `restricted`, `prohibited`, with M4 9.2 rule 3's meanings. `restricted` means allowed only with a condition specific to this subject |
| `instrument` | `agency_statement` (the responsible agency's or operator's own page for this subject) or `order` (a provision of an order entity, cited by `order_id`). Required for every non-unknown status |
| `conditions` | Optional, closed set: `stay_limit_days`, `reservation` (`required`, `not_required`, `not_stated`), `fee_stated`, `designated_sites_only`, `max_vehicle_length_ft`, `high_clearance_stated`, `no_trailers_stated`. Each is supported by the same evidence. Any condition makes the status at most `restricted` (CE7) |
| `windows` | The source's date text verbatim in `raw`, and parsed month-day pairs where the fixed parser recognises the form (as the M6 draft 9.5) |
| `summary` | At most 160 characters, written by the reviewer, not copied |
| `evidence` | Contract 5.4 claim evidence with `basis` `manual_review`, the publisher's own URL, `source_edition` (page date or order number read, or null), `last_checked_at`, `last_confirmed_at`, positive `max_age_hours`, and `effective_from`/`effective_to` for a dated one-off |
| `exempted_by` | Order provision references whose own text exempts this place (8.4 step 3) |

Every setup key is present in every record. A status of `unknown` has no other key. One evidence object is never shared by two claims (M4 9.2 rule 5). A place with no record has every setup unknown.

### 8.4 Precedence and evaluation (pure, view time)

For one place, one setup and the trip dates the user entered, evaluated in this order, **before** freshness can soften anything:

1. Collect every applicable claim: the place's own `site` claims, and the claims and order provisions reached through the place's `constrained_by` links (11.2) and its `governed_by` unit's default rules.
2. Any applicable `prohibited` → **Prohibited**.
3. Unless the place's record carries a reviewed `exempted_by` that cites the order's own exemption sentence (for example "unless in a developed campground or designated dispersed site"), reviewed against the same order edition. A recreation page cannot exempt a place from an order. [DRAFT-PR 15 4.2 H]
4. Otherwise any applicable `restricted` → **Restricted**, listing every condition and its source.
5. Otherwise a `site` claim of `allowed` → **Allowed**, only if its review is within policy **and** (M7-D5) the place's `orders` coverage for its governing jurisdiction is `checked` within policy.
6. Otherwise → **Not established**.
7. Then apply freshness (8.6) to the result's parts: a stale or never-confirmed restriction stays and is flagged review overdue; a stale `allowed` becomes not established.

The evaluator is one pure function with an injected clock (section 12.3). Validation stays time-independent (contract rule 10).

### 8.5 Invariants (validated where they can be; R131, R132, R140)

- **CE1. Unknown is the default** and is stored as `{"status": "unknown"}` or as absence.
- **CE2. No inferred permission.** No claim is produced from a listing, an inventory record, a reservation link, a road designation, a land unit, an area polygon, a straight-line distance, a name, a source status field or the absence of an order.
- **CE3. No inference across setups.** `tent` never sets `vehicle_sleeping`; neither sets `trailer_or_rv`; nothing sets `hammock`.
- **CE4. Positive claims fail closed.** `allowed` needs a reviewed `agency_statement` for that place, complete evidence, review within policy and, under M7-D5, checked order coverage. Missing any part gives not established (trust principle 6).
- **CE5. `allowed` only at site scope.** A rule at area, corridor or unit scope can restrict or prohibit; it can never allow.
- **CE6. Restrictions first.** A prohibited or restricted result is shown whenever one applies, whether or not its review is overdue, and before any allowed claim.
- **CE7. Conditions cap the status.** A claim with any condition is at most `restricted`. Passing a condition check (a stay inside the limit) is never a positive result.
- **CE8. Staleness never weakens a restriction** (8.6, trust principle 5). Evaluation order must not let staleness pre-empt a stay-limit, setup, clearance, length, seasonal or order restriction (contract rule 6).
- **CE9. Conflicts stay side by side.** Two reviewed records that disagree about one setup at one place are both kept and shown with their sources; the result is never `allowed`: a conflict involving a restriction shows the restriction; any other conflict shows not established. No reading is chosen by recency or source rank unless an instrument states precedence. [DRAFT-PR 29]
- **CE10. Dates never create permission.** A trip inside a stated window yields at most the claim's own status; a trip outside it yields not established for those dates, or the restriction. The departure day is part of the trip. [DRAFT-PR 15]
- **CE11. A default rule is a limit, never a permission.** Attaching a unit's stay limit to a place changes no setup claim at that place.
- **CE12. Claims are scoped** to the subject and the region package in which they were reviewed. They do not spread to neighbouring places, other setups, other jurisdictions or another package.
- **CE13. Day use is not overnight.** A `day_use_site` never satisfies an overnight need, whatever its claims; its overnight prohibition is shown as a restriction.
- **CE14. Source text is not a claim.** A source's free-text restriction field (Douglas `restrictions` [MEAS E3]) stays source text. A reviewer may write a claim from the agency page it came from; the field itself is never parsed into a status.

### 8.6 Freshness (NORMATIVE pattern, from M4 9.3)

| Stored status | Within policy | Past policy |
|---|---|---|
| `allowed` | Allowed, with its conditions and dates | Not established, with the last review date |
| `restricted` | Restricted, with its conditions | Still restricted, flagged review overdue |
| `prohibited` | Prohibited | Still prohibited, flagged review overdue |
| `unknown` | Not established | Not established |

Computed from `last_confirmed_at` and `max_age_hours`, never stored. Proposed defaults (M7-D10): developed-campground site claims 2,160 hours; designated dispersed areas and corridors 720 hours; area, corridor and unit rules from orders 720 hours; fire restrictions 24 hours; reviewed place existence 8,760 hours. A new edition of a page or order does not refresh a review; it is a reason to review again.

### 8.7 Evidence coverage for overnight places (adventure model section 4)

`v2/regions/<id>/overnight-coverage.json` follows the M5 draft's `land-coverage.json` shape (subject, category, jurisdiction, summary, evidence). [DRAFT M5 9.1] The subject is a place ID. Categories in M7, each refining an existing fact-coverage dimension:

| Category | Refines |
|---|---|
| `camping_rules` | `camping_permission` |
| `orders` | `closures`, `restrictions` |
| `seasonal_closures` | `closures` |
| `fire_restrictions` | `closures` |
| `reservation_and_permits` | `restrictions` |
| `vehicle_constraints` | `road_access` |

The adventure model's coverage rules apply unchanged: coverage never creates permission; checked with no record is not "no restriction"; not checked is the default and is shown; coverage is scoped to one subject, category and jurisdiction; it ages; there is no fully-covered state and no single score. A coverage record names every source checked (an order index, a district alerts page), as PR #35's example does. [DRAFT-PR 35]

M7 also makes the M6 draft's reserved `orders` category for trails accepted (an amendment to the M6 specification's 9.6 and R115, made in M7-D's pull request). [DRAFT M6 9.6]

## 9. Orders and fire restrictions as entities

SOURCE-NEUTRAL. Which issuers' publications are read is LOCKED (L7).

### 9.1 Why orders are entities

An order closes or limits camping over a scope it states, for dates it states, and is replaced by later orders. Held as a property of a place it loses its scope, its dates and its history, and a place drawn outside an order's mapped edge reads as open. Held as an entity, one order constrains many places through links (11.2), can be superseded by a named successor, and keeps its history when it ends. [DRAFT-PR 35]

### 9.2 The order registry

`v2/regions/<id>/orders.json`, curated, validated:

```json
{"schema_version": 1,
 "orders": [
  {"id": "order-…", "issuing_unit": "…", "issuer_code": "…", "governing_unit_ids": ["padus-…"],
   "order_number_as_printed": "…", "instrument_type": "signed_order",
   "title": "…",
   "effective": {"from": "…", "through": "…", "unless_rescinded": true},
   "scope": {"basis": "distance_from_named_features", "summary": "…", "quotation": "…", "exhibit_urls": ["https://…"]},
   "provisions": [
     {"key": "p1", "category": "camping", "effect": "prohibits", "setups": ["tent", "vehicle_sleeping", "trailer_or_rv"],
      "summary": "…", "quotation": "…", "citation": "36 C.F.R. 261.58(e)",
      "exceptions": [{"kind": "developed_site", "quotation": "…"}, {"kind": "designated_dispersed_site", "quotation": "…"}]}],
   "supersedes": [{"order_id": "order-…", "basis": "The order states that it replaces the earlier order."}],
   "evidence": {"source_url": "https://…", "agency": "…", "basis": "manual_review", "source_edition": "…",
                "last_checked_at": "…", "last_confirmed_at": "…", "max_age_hours": 720}}]}
```

| Field | Rule |
|---|---|
| `instrument_type` | `signed_order`, `fire_restriction`, `regulation`, `agency_rule_page`. A press release or alert is evidence about an order, not an order |
| `order_number_as_printed` | The number exactly as printed, or `null` where no number is confirmed. Never an empty string and never borrowed (OR2) |
| `governing_unit_ids` | M5 land unit IDs, through the reviewed issuer table (RL10). Empty if M5 is not approved |
| `effective` | `from` required; `through` the stated end or `null`; `unless_rescinded` as stated |
| `scope.basis` | One of `named_places`, `named_roads`, `named_trails`, `distance_from_named_features`, `plss_townships`, `administrative_unit`, `map_exhibit`, `other` |
| `scope.summary` | At most 160 characters, by the reviewer |
| `scope.quotation`, `provisions[].quotation`, `exceptions[].quotation` | Optional, at most 25 words each, only if the owner's terms reading allows storing quotations of that issuer (L7). A quotation is never paraphrased into permission |
| `provisions[].category` | `camping`, `stay_limit`, `fire`, `parking`, `vehicle_use`, `area_closure`, `food_storage`, `occupancy_other` |
| `provisions[].effect` | `prohibits` or `limits`. There is no `allows` (OR4) |
| `provisions[].exceptions` | The instrument's own exceptions, by kind (`developed_site`, `designated_dispersed_site`, `permit_holder`, `other`), as stated |
| `supersedes` | Only where the instrument states it (OR6) |

### 9.3 Three clocks

| Clock | From | Means |
|---|---|---|
| Order interval | `effective.from`, `effective.through` | When the instrument says it applies. A fact about the order |
| Review | `last_confirmed_at`, `max_age_hours` | Whether Ohvernight's reading is within policy. Computed, never stored |
| Trip | The user's arrive and depart dates, departure day included | What the user asked about. Never stored |

An order is evaluated for the trip dates: it applies to a trip day inside its interval. For a trip day after `through`:

- the order is still listed with the place's restrictions, marked as ended on its stated date, with "whether it was extended or replaced has not been checked" until a review dated after `through` records a successor or its absence (M7-D8);
- it is never removed from history and never shown as openness (OR8).

An order whose `through` is null and whose text says "unless rescinded" applies until a reviewed record states its rescission.

### 9.4 Supersession and conflict

- A later order is a separate entity, linked by `supersedes` only where its own text says so. [DRAFT-PR 35]
- Two in-force orders constraining one place are both shown; the stricter provision governs the result (8.4 step 2), and neither is dropped.
- A superseded order stays in the registry with a `superseded_by` derived from the successor's `supersedes`, and is not evaluated for dates after the successor's `from`.

### 9.5 Invariants (validated where they can be; R133–R135)

- **OR1.** An order has an issuer, an instrument type, a `from` date, a scope basis and summary, at least one provision and complete evidence.
- **OR2.** `order_number_as_printed` is the printed number or null; a number is never taken from a nearby or standing order. [DRAFT-PR 35]
- **OR3.** `through`, when present, is not before `from`.
- **OR4.** No provision allows anything. An order's exception is recorded as the order's text; it becomes a place's `exempted_by` only by review (8.4 step 3).
- **OR5.** Scope is held as stated. It is never turned into a list of affected places, a buffer or a polygon by the build (M7-D7 for applicability).
- **OR6.** `supersedes` targets exist, form no cycle, and each carries a non-empty basis.
- **OR7.** A restriction of unclear scope is retained and shown in the region's orders panel (CP8), never dropped (adventure model, `constrained_by` row).
- **OR8.** An ended or superseded order is never evidence of openness.
- **OR9.** An order's review going stale never weakens its provisions (trust principle 5).
- **OR10.** Status observations from different jurisdictions never resolve one another (9.6).
- **OR11.** A page hash, an alert title or a feed entry never creates or ends an order; only a reviewed record does.

### 9.6 Fire restrictions

A fire restriction is an order of instrument type `fire_restriction` with a `stage_as_stated` string and a jurisdiction. It adds `status_observations`: each a publisher, the publisher's statement as a reviewer summary, the jurisdiction the statement covers, and its checked time. [DRAFT-PR 35]

- A statement from one jurisdiction (a county) never establishes the status of another jurisdiction's restriction (a forest). Silence on an alerts page is an observation of silence, not of rescission. Same-jurisdiction observations that disagree leave the restriction shown as in force for its stated interval and flagged unresolved (OR10, trust principle 5).
- Fire restrictions constrain fires, stoves and smoking. They are shown beside the camping answer and are never an input to a setup claim. [DRAFT-PR 15 section 3]
- Proposed `max_age_hours` 24 (M7-D10). Past 24 hours a recorded restriction stays shown and flagged review overdue; a recorded lifting becomes "not checked recently".
- The existing `restriction_monitor` record (Aspen `pitkin-fire-monitor`, a page hash) is transport, not a stage, under R28. [MEAS E1] Research reports that the hashed page is a general news index. [DRAFT-PR 15] Its disposition is M7-D9.

## 10. Vehicle and setup suitability

SOURCE-NEUTRAL. Which instrument is the road designation in each pilot, and how its fields map to the vocabulary, are LOCKED (L9).

### 10.1 The user's profile is not evidence

A trip's **vehicle profile** is what the user says they drive: one `vehicle_class` (10.2), `towing` (yes, no), and optionally a combined length in feet. Their **setup** (8.1) is how they sleep. Neither is evidence about any place. Douglas currently stores display labels and evaluates nothing with them [MEAS E5]; M7 replaces them with the profile and migrates saved values (12.3).

### 10.2 One vehicle-class vocabulary, shared with M6

One fixed table, `v2/pipeline/config/vehicle_classes.json`, serves roads (M7) and trails (M6). It answers the M6 coordinator note of 9.1 with an explicit mapping or explicit non-mapping for every key. [DRAFT M6 9.1] [MEAS E5]

| Key | Domain | Existing use | Mapping and non-mapping |
|---|---|---|---|
| `passenger_car` | road | Aspen `mvum_roads` `designations`; Aspen planner | Kept as is. Douglas "Car / SUV" migrates to it |
| `high_clearance` | road | Aspen `mvum_roads`; Aspen planner | Kept as is. Douglas "High-clearance vehicle" migrates to it. **Not** `four_wheel_drive`: neither implies the other |
| `motorhome` | road | Aspen `mvum_roads`; Aspen planner | Kept as is. Douglas "Motorhome / RV" migrates to it. A trailer is not a motorhome |
| `four_wheel_drive` | trail and road | M6 draft trail key | No existing road key maps to it |
| `motorcycle` | trail and road | M6 draft trail key | Scenario A's bike. A road designation for motorcycles is a separate class from `passenger_car`; a street-legal question is not modelled |
| `atv`, `ohv_wide` | trail and road | M6 draft trail keys | Width threshold is the source's (L9) |
| `mountain_biking`, `ebike_class_1`–`3`, non-motorized and winter keys | trail | M6 draft | Not road classes in M7 |

`towing` is a profile modifier, not a class. "Truck with trailer" migrates to the user's chosen class with `towing: yes`; until they choose, the class is not established and every class-dependent constraint reads not established (12.3). A source class that does not map exactly to one key stays a source fact and every key it might touch stays unknown (as the M6 draft 9.1). R139 checks that the Aspen road keys and the M6 trail keys are all in the table.

### 10.3 Constraints

`v2/regions/<id>/access-constraints.json`, curated, validated. A constraint is a reviewed statement that limits who or what may use a road or occupy a place:

| `constraint` | Subject | Meaning | Source |
|---|---|---|---|
| `designation` | road | The road is designated, or not, for a vehicle class on stated dates | The road-designation instrument (L9) |
| `max_vehicle_length_ft` | place or road | A stated length limit | Agency or operator page |
| `high_clearance_stated` | place or road | The agency states high clearance is required | Agency page |
| `four_wheel_drive_stated` | place or road | Required, or `recommended` | Agency page |
| `no_trailers_stated` | place or road | Trailers are not allowed or not suitable, as stated | Agency page |
| `seasonal_gate` | road | A stated seasonal closure of the road | Agency page or order |

Each carries `classes` (the 10.2 keys it concerns), `status` (`prohibited`, `restricted`, `unknown` — there is no "suitable"), stated `windows` where relevant, a reviewer summary and complete evidence. A `recommended` statement is a caution, never an exclusion.

### 10.4 Evaluation

For a profile, a place and the place's established `approached_via` roads (11.3), each constraint yields one of:

| Result | When | Presented as |
|---|---|---|
| Excluded | A reviewed constraint prohibits the profile's class, length or towing, for a trip day | The constraint, its source and dates |
| Condition | A reviewed constraint restricts (season, length the user has not given, a recommendation) | The condition |
| Not established | No reviewed constraint for this class, or the approach is not established, or the class is not chosen | "Not established" for that question |

There is no positive result. Where every reviewed constraint passes, the detail says which constraints were checked and that suitability is not established (CP10). A road's designation is evaluated at view time for the dates entered; no trip-scoped evaluation is published (VS6).

### 10.5 Invariants (validated where they can be; R138, R139, R142)

- **VS1.** Suitability is never inferred from a road's surface, maintenance level, symbol, width, name, appearance or a vehicle-class designation for another class.
- **VS2.** The absence of a stated limit is not "no limit". An unreviewed road is not established for every class.
- **VS3.** A designation for one class never sets another (as M6 AE2).
- **VS4.** A constraint can exclude; nothing certifies suitability.
- **VS5.** A stated recommendation is a caution, not an exclusion and not a requirement.
- **VS6.** No published feature carries a trip-scoped `access_status` or `evaluated_trip`; road designations stay source facts and are evaluated at view time (retires register N8).
- **VS7.** A constraint on a road reaches a place only through an established `approached_via` link (RL11). A road near a place constrains nothing.
- **VS8.** Staleness never weakens a constraint that excludes or restricts (trust principle 5); a stale permissive designation reads not established.
- **VS9.** The profile is user input, never stored as evidence and never shared beyond the browser's existing saved-trip keys.

## 11. Relationships

SOURCE-NEUTRAL. The M6 draft's RL1–RL8 apply unchanged: relationships are created only by a source statement or a reviewed record; each has a direction, two stable IDs, an origin, evidence, and lives in a registry; derived links name their rule and inputs; staleness never removes a restricting relationship; a chain is only as established as its weakest link; no relationship asserts access, legal travel, parking, camping, current condition or vehicle suitability. [DRAFT M6 10.1]

### 11.1 Registry

`v2/regions/<id>/overnight-relationships.json`, validated, holds `constrained_by`, `approached_via`, `governed_by`, `part_of` and `same_place_as` links with the M6 link shape (`id`, `kind`, `from`, `to`, `origin`, `evidence`, and `rule` and `inputs` for a derived link). [DRAFT M6 10.3] Candidates are written to the build report only, never to this file. `relevant_to` is never stored (RL14).

### 11.2 `constrained_by`: place, trail, trailhead or road → order

| Origin | When |
|---|---|
| `source_backed` | The order or its exhibit names the place, its road or the trail (for example an exhibit table row naming a campground's spur road) [DRAFT-PR 35] |
| `derived` (administrative unit) | The order's scope basis is `administrative_unit`, and the subject has a source-backed `governed_by` link to a unit in the order's `governing_unit_ids`. Rule and inputs recorded. Containment in a generalized polygon is never an input |
| `derived` (stated geometric scope) | Only if the owner chooses M7-D7 (b): the order's own stated distance or township rule computed against source geometry, published in the restricting direction only and labelled computed |
| `reviewed_candidate` | A person confirmed, from the order and its exhibit, that the subject is inside the stated scope |
| `unknown` | Default |

Rules:

- **RL9 (restriction asymmetry).** A `constrained_by` link only ever carries a restriction. The absence of a link never means the order does not apply; a subject outside a computed scope is never shown as unaffected.
- **RL10 (issuer to unit).** An order's `governing_unit_ids` come from a reviewed issuer table mapping issuing units to M5 land unit IDs. If M5 unit IDs are not approved, the list is empty and the order appears in the region's orders panel (CP8) instead of on places. [DRAFT M5 10 rule 1]

An order with no link to a place still appears in that region's orders panel, so a restriction of unclear scope is retained and visible (OR7).

### 11.3 `approached_via`: place or trailhead → road

`source_backed` where agency directions or a designated-route map state the road; `reviewed_candidate` where the place's point lies on the road geometry and a person confirmed it against an agency source; otherwise unknown. A candidate from network topology is listed for review only. [REPO adventure model section 3]

- **RL11.** A road constraint reaches a place only through `approached_via` (VS7). The approach from the road network to that road is not established by M7 and is listed as unknown.

### 11.4 `governed_by`, `part_of`, `same_place_as`

- **RL12.** `governed_by` from a place to an M5 land unit comes only from the place record's own managing-unit field, through a documented reviewed mapping (M5 rule 1). Lying inside a land polygon is context only. A land unit is never an input to a permission (M5 rule 2).
- **RL13.** `part_of` (campsite → campground or area) and `same_place_as` (two source records, one place) are source-backed or reviewed only; never by name, proximity or a shared road name.

### 11.5 `relevant_to` and backups

- **RL14 (`relevant_to` is computed, never stored).** An overnight place is `relevant_to` a trail or trailhead only as a composition, computed at view time: the place `approached_via` road A and the trailhead `approached_via` road B, each established; a connection between A and B established by a source or reviewed link; and vehicle-constraint coverage recorded for those roads for the user's class. Any missing link makes `relevant_to` unknown, and the detail names the missing link. M6 supplies `starts_at` trail→trailhead links. [DRAFT M6 10.4] [REPO adventure model section 3]
- **RL15 (backup).** A place B is an **independent backup** for place A, for a trip, only when all hold: B is not A, not `part_of` A and not `same_place_as` A; B's result for the user's setup is not Prohibited for the trip; B is not constrained by an in-force `camping` or `area_closure` provision that also constrains A; and B's approach does not depend on the only established approach to A. Where any of these is not established, B is not a backup and the reason is named. Where no place qualifies, the absence is stated (CP15). Straight-line listings are never backups.

M7 provides the backup predicate as a pure function and the data it reads; M8 decides how candidates use it.

### 11.6 What M7 provides and does not

| M7 provides (where the approved source supports it) | M7 does not provide |
|---|---|
| Overnight place identity and kind, with use period | Places from geometry, buffers, setbacks or names |
| Setup claims per place, restriction-first, from reviewed instruments | Permission at area, corridor or unit scope; availability; current status |
| Order and fire-restriction entities with scope, dates, provisions, supersession and history | Order geometry; a list of places generated from an order's scope (unless M7-D7 (b)) |
| Vehicle constraints and `approached_via` links, restriction-only | A statement that a vehicle is suitable, or that a road is passable |
| `constrained_by`, `governed_by`, `part_of`, `same_place_as` links | Links from proximity, containment or name |
| `relevant_to` and backup as computed predicates over established links | Stored `relevant_to`; a backup from distance |
| Overnight coverage per place and category | "No restriction found" as a result |
| The `orders` coverage category for M6 trails | Trail activity claims (M6) |
