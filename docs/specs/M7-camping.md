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
| `exempted_by` | Order provision references whose own text exempts this place (8.4 step 2) |

Every setup key is present in every record. A status of `unknown` has no other key. One evidence object is never shared by two claims (M4 9.2 rule 5). A place with no record has every setup unknown.

### 8.4 Precedence and evaluation (pure, view time)

For one place, one setup and the trip dates the user entered, evaluated in this order, **before** freshness can soften anything:

1. Collect every applicable claim: the place's own `site` claims, and the claims and order provisions reached through the place's `constrained_by` links (11.2) and its `governed_by` unit's default rules.
2. Any applicable `prohibited` → **Prohibited**. The one exception is an order provision from which the place's record carries a reviewed `exempted_by`, citing the order's own exception sentence (for example "unless in a developed campground or designated dispersed site") and reviewed against the same order edition; that provision is then not applied to the place. A recreation page cannot exempt a place from an order. [DRAFT-PR 15 4.2 H]
3. Otherwise any applicable `restricted` → **Restricted**, listing every condition and its source.
4. Otherwise a `site` claim of `allowed` → **Allowed**, only if its review is within policy **and** (M7-D5) the place's `orders` coverage for its governing jurisdiction is `checked` within policy.
5. Otherwise → **Not established**.
6. Then apply freshness (8.6) to the result's parts: a stale or never-confirmed restriction stays and is flagged review overdue; a stale `allowed` becomes not established.

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
- **OR4.** No provision allows anything. An order's exception is recorded as the order's text; it becomes a place's `exempted_by` only by review (8.4 step 2).
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

## 12. Removing the hard-coded camping-rule behaviour

SOURCE-NEUTRAL. The roadmap asks M7 to "eliminate inappropriate hard-coded camping-rule behavior". [REPO ROADMAP M7] This section lists every such behaviour found on `main`, with file and line, and its disposition. All of them restrict or caution; none grants permission. [MEAS E1, E7, E8] The problem is that they restrict on unreviewed constants, on an assumed setup, by name, or by a trip evaluation frozen into published data, so their answers cannot be traced to a reviewed instrument and cannot be corrected without code changes.

### 12.1 Inventory

| ID | Where | Behaviour | Why it is inappropriate | Disposition (PR) |
|---|---|---|---|---|
| H1 | `v2/trip-rules.js:28-30`; `v2/trust.js:14-17`, `:29-31` | Excludes any trip longer than `stay_limit_days` (or `max_stay_days`) on a place record, and merges place and rule limits by minimum | The limit on the curated listing has no evidence object of its own; the label "published limit" is not traceable to a review | Becomes a `stay_limit_days` condition on a reviewed claim (8.3), carried by the migration rule (12.4). Evaluated by CE7 and CE10 (M7-B) |
| H2 | `v2/trip-rules.js:32` | `tent_only` excludes every trip with the label "Tent-only · vehicle-sleeping mismatch" | Assumes every visitor sleeps in a vehicle; a tent camper is told the place conflicts | Becomes `vehicle_sleeping` and `trailer_or_rv` prohibited, `tent` unknown, per 8.1 (M7-B) |
| H3 | `v2/trip-rules.js:33-34` | `requires_high_clearance` plus `passenger_car` excludes | A curated flag without its own evidence decides a vehicle exclusion | Becomes a `high_clearance_stated` access constraint (10.3), carried by 12.4 (M7-B) |
| H4 | `v2/trip-rules.js:44-45` | Same flag plus `motorhome` gives "Motorhome suitability unverified" | As H3; implies other combinations were verified | Becomes a condition result under 10.4 (M7-B) |
| H5 | `v2/trip-rules.js:35-42` | Compares trip days with MVUM `dates_open` of one road chosen per place; outside the window excludes, inside it shows "Within the mapped campground-road designation" | The place-to-road link has no evidence; a road fact is placed where a camping answer is expected [DRAFT-PR 15 5.3] | The road becomes an `approached_via` link carried by 12.4; the designation is evaluated by 10.4; the positive-sounding note is retired (M7-B) |
| H6 | `v2/trip-rules.js:24` | Staleness behaviour keyed on the label string `'Motorhome suitability unverified'` | Trust behaviour depends on a display string | Replaced by status-based freshness (8.6) (M7-B) |
| H7 | `v2/pipeline/scripts/09_reviewed_sites.py:10`, `:13`, `:39`, `:42`, `:51` | Five fixed claim names; a 30-day review age in code; vehicle sleeping as the only reviewable setup; today's date read at build time; writes `camping_permission: "supported_for_trip"` | Policy in code, time-dependent output, one setup only, a second vocabulary for permission | Retired with the `reviewed_sites` producer under M7-D6; review ages come from data (8.6) (M7-B) |
| H8 | `v2/pipeline/config/legal_rules.yaml:5-6` | `road_buffer_ft: 300`, `water_setback_ft: 100` | Distances with no cited order; research reports the current orders set different distances for different features [DRAFT-PR 15] | Removed with H9; any setback in future is an order provision (9.2), not a constant (M7-B) |
| H9 | `v2/pipeline/scripts/07_build_dispersed_corridors.py:48-49`, `:57`, `:59`, `:83-84` | Builds 51 "Areas to research" polygons from land whose manager is USFS or BLM, around roads `designated_open` for one evaluated trip, buffered by H8, with trip dates from the environment or today | Camping possibility inferred from management ([DRAFT M5] 10 rule 2), computed camping geometry, frozen trip evaluation; default-on [MEAS E1] | Removed from display and canonical data under M7-D14 (M7-B); producer retired |
| H10 | `v2/pipeline/scripts/02_fetch_mvum_roads.py:16`, `:29-30`; `lib/access.py:38-65` | Writes a trip-scoped `access_status` and `evaluated_trip` into every published road feature | Register N8: 51 features say `designated_open` for a past trip [REPO] | Published features keep only source designations; evaluation moves to view time (VS6, R142) (M7-B) |
| H11 | `v2/pipeline/scripts/lib/rules.py:12-13`; `rules-registry.json` `road_names` | Attaches rule context by upper-cased road name | A name match creates a relationship (adventure model rule 6) | Replaced by `constrained_by` and `approached_via` links (11.2, 11.3); `road_names` retired (M7-B) |
| H12 | `v2/regions/douglas-co/extras.js:3` | Rampart designated dispersed area hard-coded in JavaScript, with a paraphrased seasonal closure and a date-only retrieval | Register N7, deferred to M7 [REPO] | Moved verbatim to `overnight-places.json` as an unreviewed existence record; its sentence kept as source text with its date (CP13) (M7-B); reviewed in M7-E |
| H13 | `v2/explore/trail-seasons.js:27`; `v2/explore/browse.js:46` | Camping list includes `CAMPGROUND` only; the detail stops for site types outside three, so the HORSE CAMP is not listed and "Overnight use prohibited." on two picnic sites is never shown [MEAS E6] | Silent omission of an overnight place and of two overnight restrictions | Kind table (7.1, R145) decides inclusion; every overnight-relevant record's source restriction text is shown (CP13) (M7-C) |
| H14 | `v2/explore/browse.js:20`, `:32`; `v2/explore/capabilities.js:32`, `:57` | Two vehicle vocabularies; Douglas stores display labels and evaluates nothing; Aspen accepts three keys | Vocabularies can silently disagree once roads enter the model [DRAFT M6 9.1 note] | One profile (10.1) and one table (10.2), with saved-value migration (12.3) (M7-B) |

### 12.2 The computed research areas (H8, H9)

The 51 polygons are labelled as research areas, not campsites, and carry `camping_permission: unknown`. [MEAS E1] They are still the largest overnight-related object on the Aspen map, on by default, and they are built from inferences the trust principles forbid elsewhere: possibility from management, relevance from proximity to a designated road, and a buffer with no cited source. Research reports that at least sixteen are named after campground roads whose surroundings a current order closes to camping. [DRAFT-PR 15] [UNK] The recommended disposition is removal from display and canonical data, with the producer and its configuration retired and the manifest layers removed (M7-D14, M7-MR1). Keeping them reworded is the alternative.

### 12.3 The replacement

- One pure evaluator module, `v2/explore/overnight.js`, replaces `v2/trip-rules.js` and the camping parts of `v2/trust.js` in `v2/`. It takes a place, the region's registries, a profile, trip dates and an injected clock, and returns per-setup results, per-constraint vehicle results and the coverage list. It writes nothing and reads no clock of its own. The root legacy site's `trip-rules.js` is not touched. [MEAS E7]
- `Trust.freshness` stays the single freshness function for v2.
- Douglas saved trips migrate on read: "Car / SUV" → `passenger_car`; "High-clearance vehicle" → `high_clearance`; "Motorhome / RV" → `motorhome`; "Truck with trailer" → class not established, `towing: yes`. Aspen saved values are already keys. An unrecognised value becomes not established, never a default class.
- Every existing staleness and rule-ordering assertion in `trust.test.cjs` and `staleness.test.cjs` (including the N6 and N16 markers) is carried to the new evaluator with an equivalent case before the old one is deleted; none is dropped. [REPO register N6, N16]

### 12.4 Migration rule: no restriction a user sees today disappears

M7-B must not remove a restriction to remove the code that produced it.

1. Every restricting fact the old behaviour used is carried into the new registries as a restriction: the Lincoln Creek rule record (stay limit and clearance) with its existing `last_confirmed_at` [MEAS E2]; the listing fields `tent_only`, `requires_high_clearance` and `stay_limit_days`, and each listing's curated road designation link, with the listing's `source` URL and its `checked_on` date as the confirmation date (M7-D12).
2. Each carried record is past its age on arrival and is therefore shown restricted and flagged review overdue (8.6). It is never shown as allowed.
3. A parity test enumerates every place, every vehicle key and a grid of trip dates across a year: wherever the old evaluator returned an exclusion, the new evaluator returns a prohibition, restriction or exclusion for the corresponding setup or profile. The single intended difference is H2: a tent at a tent-only place is no longer excluded; it reads not established.
4. Retiring the computed areas (H9) removes no restriction: they carried none. [MEAS E1]

## 13. Presentation and trust-wording constraints

SOURCE-NEUTRAL. These are constraints, not strings. **Exact literals are deferred to the owner** (M7-D18): drafted in the pull request that first renders them, approved by the owner there, and then pinned byte for byte by tests, as M4 section 10 and the M5 and M6 drafts do. Manifest wording is trust-bearing and changes only with owner approval (trust principle 8). Research proposes candidate strings (OV1–OV9) that the first rendering PR may start from. [DRAFT-PR 15 5.1]

| ID | Constraint |
|---|---|
| CP1 | **Few and short.** At most 16 new fixed strings in M7, excluding setup, vehicle-class and category labels. A detail line at most 90 characters; a label at most 32; a legend line at most 60. Every string fits at 320 px in the results sheet without truncation |
| CP2 | **Forbidden words.** No new string contains "verified", "legal", "permitted", "open", "available", "safe", "suitable", "free camping", "current" used of status, "connected" or "dispersed camping" as the name of anything Ohvernight computed, except where the string states that something is *not* established (M3 A4) |
| CP3 | **Status never alone.** A status word is always shown with its setup (tent, vehicle, trailer or RV, hammock) or, for a vehicle result, its class. "Camping" is never a status subject on its own |
| CP4 | **Restrictions first.** Prohibited, then restricted, then allowed, then not established; orders and fire restrictions before source facts; a review-overdue flag on the same line as the restriction it qualifies |
| CP5 | **Two lines on every overnight detail,** whatever its claims: a listing or mapped area is not permission to camp, park overnight or sleep in a vehicle; availability is not known to Ohvernight. A booking link appears only beside the second and only to the facility's own page, never a search URL |
| CP6 | **Orders are shown as instruments:** issuer, number as printed or "number not established", stated dates, scope summary, and a link. An ended order says it ended on its stated date and that a successor has not been checked (9.3) |
| CP7 | **Origin disclosed.** A `constrained_by` link that is derived says it applies by the order's stated scope as computed by Ohvernight, and never says the order does not apply anywhere |
| CP8 | **Orders panel.** Each region shows its reviewed orders and fire restrictions, including those linked to no place, in one panel reachable from every overnight detail. An empty panel says orders were not checked, never that there are none |
| CP9 | **A default rule is a limit.** A unit-wide stay limit is worded as a limit for anyone camping in that unit, followed by a fixed statement that it does not say camping is allowed at the place |
| CP10 | **Vehicle results never certify.** Results read excluded, condition or not established; where reviewed constraints pass, the detail names what was checked and states that suitability is not established |
| CP11 | **Fire is separate.** Fire restrictions sit in their own line or section, with jurisdiction and checked time, never inside a setup line |
| CP12 | **No map-level camping status** (follows M4 O3 unless M7-D17 decides otherwise). No green, tick or badge for any camping result |
| CP13 | **Source text is labelled source text.** A source's restriction, season, fee or status field is shown under a source heading with its retrieval date, never with a status word, for every overnight-relevant record including picnic sites and horse camps |
| CP14 | **Straight-line listings keep their wording** and the "connection unverified" marking, and are never titled backup, near, base or recommended |
| CP15 | **Backup stated.** Where M7 shows backups, an independent one is named with its basis, and where none is established the detail says so (RL15) |
| CP16 | **Coverage as a list.** Overnight coverage is a list of categories with checked or not checked and review dates; never a score, percentage or badge |
| CP17 | **Day use labelled.** A day-use place in any overnight list carries its day-use label and its overnight restriction; it is never counted as an overnight option |

**Detail order (proposed).** Title and kind; use period; restrictions section (prohibitions, restrictions, order lines, review flags); setup lines (CP3) for the selected setup or all four; vehicle results for the profile (CP10); fire line (CP11); coverage list (CP16); backup line where shown (CP15); source facts (CP13); provenance and "Source fetched"; the two fixed lines of CP5; layer limitation.

## 14. LOCKED — Source field mapping (interface only)

**Nothing here maps any field.** Each approved source needs one committed mapping file, `v2/pipeline/config/overnight_sources/<namespace>.json`, that declares, for the build and the validator to read:

| L-item | Declares |
|---|---|
| L7 Instruments | For each instrument kind (`agency_statement`, `order`, `fire_restriction`), the publishers and hosts whose pages count, and whether short quotations may be stored |
| L8 Identity and kinds | Place key field and its documented persistence; the source site-type values and their place kind (7.1) or `not_overnight`; any field that is a shared publisher key across sources (EI3) |
| L9 Vehicle | For the road-designation instrument: the field per vehicle class of 10.2, the value meaning designated or not, the date field and its documented meaning, the width threshold where one exists |
| L10 Provenance and terms | Service URL and layer, terms reading reference (owner decision record), edition or date field if any, refresh authority |
| L11 Non-claim hosts | Hosts whose pages can never be a claim's `source_url` for this source (facility datasets, designation datasets, search pages, community sites) |

Rules R132, R138 and R148 read these files; until one exists for a namespace they apply only to synthetic fixtures. A mapping that would set any setup status from a source field is rejected (R148): statuses come only from reviewed records.

## 15. Contract changes

All additive to contract version 1 except the two retirements marked, documented in `v2/pipeline/docs/data-contract.md` in the pull request that introduces them. Source-specific fields are LOCKED and listed in the PR that adds them.

| Change | PR | Label |
|---|---|---|
| Manifest paths `overnight_places`, `overnight_use`, `orders`, `overnight_relationships`, `overnight_coverage`, `access_constraints`; the registries of 7.3, 8.3, 9.2, 10.3, 11.1 and 8.7 | M7-A (shape), later PRs (records) | NEUTRAL shape |
| `v2/pipeline/config/overnight.json` (issuer and jurisdiction codes, place-kind table interface, non-claim hosts) and `vehicle_classes.json` | M7-A | NEUTRAL |
| The four-status overnight claim with `instrument`, `conditions`, `windows` and `exempted_by`, as a registry-only value set (as M4 9.2 rule 8) | M7-A | NEUTRAL |
| **Retirement:** `camping_permission: supported_for_trip` and the `reviewed_sites` layer kind; the rules registry (`rules`) migrated into `overnight-use.json` and `access-constraints.json`; R50 then applies to no file (M7-D6) | M7-B | NEUTRAL |
| **Retirement:** the `research_areas` kind's producer and both Aspen research-area layers (M7-D14) | M7-B | NEUTRAL |
| Road features keep source designations; no trip-scoped `access_status` or `evaluated_trip` on published features (N8 retired) | M7-B | NEUTRAL |
| `fact_coverage.camping_permission` may be `reviewed_partial` only when `overnight-use.json` has a non-unknown claim; `closures` and `restrictions` when `orders.json` or overnight coverage has a record; R05 extended accordingly (as M4 did for water). Aspen `restrictions` keeps `reviewed_partial` through the migrated Lincoln Creek record | M7-B, M7-D, M7-E | NEUTRAL |
| Register: N7 retired (Rampart record moved to data); N8 retired | M7-B | NEUTRAL |
| M6 amendment: trail coverage category `orders` accepted; `constrained_by` trail → order populated | M7-D | NEUTRAL |
| Per-source mapping files (section 14) and any new source fields | M7-C onward | **LOCKED** |

## 16. Validator rules

New stable IDs R130–R149. Each has at least one negative fixture and, where it protects real data, a mutation proof on the committed files (local, not committed, listed in the handoff). Rules marked (L) read a LOCKED mapping file and run on synthetic fixtures until it exists.

| ID | Rule | PR |
|---|---|---|
| R130 | `overnight-places.json` conforms to 7.3; every place has one kind and use period from the fixed tables; geometry is null or the source's; no `campsite` without a source point (EI1, EI2) | M7-A |
| R131 | `overnight-use.json` conforms to 8.3: subjects resolve; every setup key present; status in the set; `unknown` has no other key; complete evidence for every other status; no shared evidence object; `allowed` only at `site` scope with `instrument` `agency_statement`; any condition caps the status at `restricted`; `hammock` unknown unless a record states it; `exempted_by` cites an existing order provision with an exception (CE3–CE7) | M7-A |
| R132 (L) | No claim, order or constraint `source_url` on a host in the non-claim list; the cited publisher is one the mapping file names for that instrument | M7-A, M7-D, M7-E |
| R133 | `orders.json` conforms to 9.2: ID form; issuer; `order_number_as_printed` a non-empty string or null; instrument type and scope basis in their sets; `through` not before `from`; at least one provision; every provision effect `prohibits` or `limits`; summaries ≤ 160 characters; quotations ≤ 25 words and present only where the issuer's mapping allows; complete evidence (OR1–OR4) | M7-A |
| R134 | `supersedes` targets exist, form no cycle and carry a non-empty basis (OR6) | M7-A |
| R135 | Fire restrictions: `stage_as_stated` and jurisdiction present; every status observation has publisher, jurisdiction, summary and checked time; no fire record whose only evidence method is `html_change_monitor`; R28's monitor clause unchanged (OR10, OR11) | M7-A |
| R136 | `overnight-relationships.json` conforms to 11.1: kind in the set; both ends resolve across the region's places, roads, M6 trails and trailheads and M5 land units; origin in the set; `derived` names rule and inputs, and its rule is one 11.2 permits; no `reviewed_candidate` without agency evidence; no `relevant_to` stored (RL9–RL14) | M7-A |
| R137 | `overnight-coverage.json` follows 8.7: subject resolves; category in the set; one record per subject, category and jurisdiction; complete evidence; at least one source checked named | M7-A |
| R138 (L) | `access-constraints.json` conforms to 10.3: subject road or place resolves; classes in the shared table; constraint kind in the set; status `prohibited`, `restricted` or `unknown`; complete evidence; for `designation`, the field mapping exists (VS3, VS4) | M7-A, M7-F |
| R139 | `vehicle_classes.json` is exactly the 10.2 table; every key in Aspen road `designations` and in the M6 claim vocabulary is in it; every pair named in 10.2 has a recorded mapping or non-mapping | M7-A |
| R140 | No feature or place, canonical or display, carries an overnight claim property: no property name containing `camp`, `overnight`, `stay`, `permission` or `suitab` except the reserved `camping_permission` with value `unknown` and listed source fields (the M4 R75 pattern) | M7-A |
| R141 | No manifest declares a `reviewed_sites` layer and no record anywhere holds `camping_permission` other than `unknown` (after M7-D6) | M7-B |
| R142 | No published road feature carries `access_status` other than `unknown`, or `evaluated_trip` (VS6) | M7-B |
| R143 | No manifest declares a `research_areas` layer with features (after M7-D14 (a)); under (b), every such layer's title and legend avoid the CP2 terms | M7-B |
| R144 | `fact_coverage.camping_permission` is `reviewed_partial` only when `overnight-use.json` has a non-unknown claim; `closures` and `restrictions` only with an order, fire or coverage record of that category, or (for `restrictions`) the migrated rule records; `layer_ids` name existing layers | M7-B, M7-D, M7-E |
| R145 | Every source site type in a published overnight-relevant layer maps to a place kind or `not_overnight` in the kind table; none is dropped (EI8) | M7-C |
| R146 | IDs follow 7.4; reserved prefixes never begin a source-record ID; `legacy_ids` follow M4 A4 (EI9) | M7-A, M7-C |
| R147 | Repository level: an order ID present in more than one region has identical non-geometry fields in each (EI6) | M7-A |
| R148 (L) | Every overnight mapping file has the L7–L11 keys of section 14; no source field is mapped to a setup status | M7-C |
| R149 | Reserved for an amendment during delivery | — |

R28 and R50 are amended, not weakened: R28's `research_areas` clause no longer has a layer to apply to once M7-D14 (a) lands, and R50 applies to no file once the rules registry is migrated (M7-D6); both stay in the validator until those PRs merge.

## 17. Budgets and performance

Inherited unchanged from M3 (section 16, A10, A13), M4 (section 14) and the M6 draft (section 15):

| Measure | Limit |
|---|---|
| Bytes to "map usable", per region | 500,000 |
| Bytes with every default-on layer, per region | 4,500,000 |
| Region default-on set | ≤ 15,000 features and ≤ 1,500,000 bytes gzipped |
| One display layer | ≤ 5,000 features and ≤ 450,000 bytes gzipped, or `min_zoom`, or split |
| Performance | Map usable ≤ 60% and all default-on layers ≤ 135% of the same-session base median; heap ≤ 115% of base; triggers R-1 to R-5 unchanged |

M7-specific (M7-D19):

| Measure | Today | Limit |
|---|---|---|
| Aspen research-area display | 709,990 bytes, default-on [MEAS E9] | 0 after M7-B under M7-D14 (a) |
| Overnight registries, per region, combined | — | ≤ 150,000 bytes raw; none requested before "map usable"; requested when an overnight detail, the camping list or the orders panel first opens |
| Evaluator module | `trip-rules.js` and `trust.js` today | Not larger than 20,000 bytes unminified |
| Douglas initial index | Headroom small [REPO M4 A2] | Nothing overnight-related is added to `index.json` |

Three sessions of the unchanged `measure.mjs` at the M7-B head and at any PR that changes display bytes, reported pass or miss. A miss is reported, not tuned around.

## 18. Tests

Offline, clock-free, nothing written inside the repository, as M3–M6.

**Python (validator and build):** a negative fixture for every rule R130–R148. Places: a `campsite` without a source point rejected; a reviewed place with invented geometry rejected; an unmapped source site type rejected (the HORSE CAMP shape). Claims: each invalid form of 8.3; `allowed` at area, corridor or unit scope rejected; `allowed` with a condition rejected; a hammock claim from a page that does not state it is caught by review, and a hammock value without evidence rejected; one evidence object on two setups rejected; a non-claim host rejected. Orders: empty-string order number rejected; borrowed number caught by review and a duplicate-number pair across issuers kept distinct; `through` before `from`; a provision with effect `allows` rejected; a supersession cycle; a quotation over 25 words. Fire: a record supported only by a page hash rejected. Relationships: a `constrained_by` derived from containment in a land polygon rejected; a stored `relevant_to` rejected; a `same_place_as` by name only rejected. Published data: a road with a trip-scoped `access_status` rejected; a `supported_for_trip` value rejected; a research-area feature rejected after M7-B.

**Node (evaluator, injected clock):**

- Precedence: a site `allowed` plus an area order prohibiting camping with no exemption → Prohibited (the Lincoln Creek shape [DRAFT-PR 15]); with a reviewed `exempted_by` citing the order's own exception → the site claim; a recreation-page "exemption" → still Prohibited.
- `allowed` within age but `orders` coverage not checked → Not established (M7-D5 (a)).
- Freshness after precedence: an overdue prohibition still Prohibited and flagged; an overdue `allowed` → Not established with its date; a never-confirmed restriction stays.
- Orders and dates: trip inside an order interval → applies; departure day alone inside it → applies; trip after `through` with no later review → listed as ended, successor not checked, never openness; `unless_rescinded` with null `through` → applies; superseded order not evaluated after the successor's `from`.
- Fire: a county lifting and a forest restriction → forest restriction shown, county statement shown for its own jurisdiction; a forest alerts page silent → still shown, flagged; a fixture alert titled as a lifting but attaching a stage order does not end anything (OR11). [DRAFT-PR 15] [DRAFT-PR 35]
- Default rule: a forest stay limit linked to a place with all setups unknown → every setup still Not established; the limit shown as a limit.
- Setups: tent-only place → `vehicle_sleeping` and `trailer_or_rv` Prohibited, `tent` Not established; hammock Not established.
- Vehicle: a designation prohibiting `passenger_car` on an established approach → Excluded for that class only; the same road with no `approached_via` → Not established; `four_wheel_drive` designation never satisfies `high_clearance` or the reverse; `towing: yes` with a `no_trailers_stated` constraint → Excluded; all constraints passing → names checks, says suitability not established.
- `relevant_to` and backup: chain complete → computed; any missing link → unknown with that link named; two places under the same in-force closure provision → not independent; no qualifying place → absence stated; a straight-line neighbour never returned.
- Day use: a picnic site with "Overnight use prohibited." source text shows that text under CP13 and never counts as an overnight option.
- Migration: the parity test of 12.4 rule 3; Douglas saved labels migrate as 12.3; an unknown saved value becomes not established.
- Carried assertions: every case of `trust.test.cjs` and `staleness.test.cjs` that tests restriction retention or rule ordering, re-expressed against the new evaluator (12.3).
- Wording: every approved literal against its string; no rendered overnight detail contains a CP2 term outside an approved negated string; status words always with a setup or class; CP5's two lines on every overnight detail.

**Browser check (both regions, four sizes):** Aspen without the research-area layer and within budget; the camping list includes the Douglas horse camp; a picnic site detail shows its overnight restriction text; a place detail renders restrictions first and the CP5 lines; the orders panel opens from a detail and says "not checked" when empty; the vehicle control round-trips a migrated Douglas saved value; from M7-D, a reviewed order and an overdue flag render when the injected time passes its age.

**Mutation proofs (local):** set a setup to `allowed` at area scope; remove an order exemption a site relies on; copy one evidence object to two setups; add `access_status: designated_open` to a road; add a research-area feature; store a `relevant_to`; derive `constrained_by` from containment; give two regions different fields for one order ID. Each must fail its named rule.

## 19. Acceptance

**Engineering, per PR:** offline suites and the browser check pass; display rebuild has no diff; each new rule passes on real data where real data exists, with negative fixtures and mutation proofs; budgets hold; three performance sessions reported where display bytes change; for M7-B, the 12.4 parity test passes and no restriction visible before the PR is missing after it; for LOCKED PRs, the snapshot and difference reports are committed.

**Owner gates:** each PR's exact head SHA approved by the owner; every literal approved in the PR that renders it; every place, claim, order, constraint and relationship record approved in the PR that adds it, with `last_confirmed_at` set only after the coordinator has read the page and the owner has approved the record (as M4-C); an iPhone Safari check of both regions for every PR that changes what the user sees (M7-B, M7-C, M7-D, M7-E, M7-F).

**Scenario acceptance (milestone close), run by a dedicated tester who did not implement any M7 PR, on a phone:**

1. **Scenario A, Douglas dirt-bike weekend** [REPO]: every measure recorded against the previous result. Source-neutral predictions to be tested, not results: step 5 (an overnight option) improves only where a reviewed setup claim exists, and otherwise reads "correctly said unknown" for the tester's setup rather than a bare listing; step 6 (backup) is answered as a named independent backup or as a stated absence, never by a straight-line listing; step 7 (closures and restrictions for the dates) improves only where reviewed order and fire records exist, and the orders panel shows "not checked" otherwise; step 4 (approach for the pickup and trailer) improves only where an `approached_via` link and a reviewed constraint exist, and never reads "suitable"; the proximity-assumption count must not rise.
2. **Scenario B, Rampart day use** [DRAFT-PR 20]: run as a canonical scenario if PR #20 is merged before M7 closes, otherwise once as a supplementary scenario beside Scenario A. Source-neutral expectations: the family base is answered as a day-use place with its own restrictions, never as an overnight option (CE13); hammock reads not established unless a reviewed page states it; fees and payment appear only as source facts or reviewed conditions; orders and fire lines show issuer, dates and checked time.
3. **Unknowns are not hidden.** No scorecard line improves by hiding an unknown (product scorecard). "Activities with actionable restriction evidence" is reported for overnight places as records per place and setup, with the count of places with no reviewed record. "Candidate trips with a viable overnight option" and "with a backup option" are reported as the scenario result, as the scorecard requires before M8.
4. The coordinator writes the product review under its six headings and states plainly what M7 delivered without the source policy, if that is the outcome.

## 20. Delivery plan

Small sequential pull requests on Aspen and Douglas County only. Each is independently revertible, leaves `main` green, keeps app, pipeline and data changes in separate commits, and needs owner approval of its exact head SHA. **NEUTRAL** PRs can start once this specification is approved. **LOCKED** PRs cannot start until the source decision (L10) is made and the named L-items are recorded.

| PR | Content | Label | Visible change |
|---|---|---|---|
| **M7-A** | Contract shapes of section 15; empty registries; `overnight.json` and `vehicle_classes.json`; the pure evaluator and backup predicate on fixtures; rules R130, R131, R133–R137, R139, R140, R146, R147 on fixtures, R132 and R138 scaffolded; no data, display or wording change | NEUTRAL | None |
| **M7-B** | Removal of H1–H12 and H14: evaluator wired in; registries populated only by the 12.4 migration; research areas and their producer removed (M7-D14); trip-scoped road evaluation removed (N8); Rampart record moved to data (N7); rules registry and `reviewed_sites` retired (M7-D6); vehicle profile and saved-value migration; owner-approved literals for CP3–CP5, CP9, CP10, CP14; R141–R144 on real data; parity test | NEUTRAL | Research areas gone; setup lines read not established or restricted; vehicle control changes in Douglas |
| **M7-C** | Place identity and kinds on the already-published records (Aspen listings and inventory, Douglas recreation sites): kind table, `use_period`, legacy IDs, horse camp in the camping list, source restriction text on every overnight-relevant record (H13, CP13), `same_place_as` from a shared publisher key; R145, R148 | **LOCKED (narrow)**: needs only M7-D2, the owner's confirmation that those published records keep their existence role and which site types are which kind (L8) | Horse camp listed; picnic-site overnight text shown |
| **M7-D** | Order and fire-restriction records for the initial set (12 orders at most per region, chosen as those governing the places Scenario A's last run and PR #20 name); `constrained_by` links; orders panel (CP6–CP8); `orders` and `fire_restrictions` coverage; the M6 `orders` amendment | **LOCKED** (L7, L10) | Orders panel; order lines in details |
| **M7-E** | Reviewed setup claims and `camping_rules` and `reservation_and_permits` coverage for the initial set (at most 8 places per region, Douglas first); `fact_coverage.camping_permission` change | **LOCKED** (L7) | Setup lines carry reviewed statuses |
| **M7-F** | Road designation constraints for Douglas and re-reviewed Aspen constraints; `approached_via` links; `vehicle_constraints` coverage; `relevant_to` and backup shown where established (CP15) | **LOCKED** (L9) | Vehicle results; backup line |
| close | Scenario runs and product review (section 19) | NEUTRAL | — |

If the source decision is declined or delayed, M7-A and M7-B still ship, M7-C ships if M7-D2 is granted on its own, and the milestone review says plainly that reviewed camping permission, orders, vehicle constraints and backups were not delivered (M7-D20).

## 21. Rollback

- **M7-A:** revert. No data or visible change.
- **M7-B:** revert. The research areas, the old evaluator, the rules registry and the hard-coded Rampart record return together; nothing else depends on them. Saved Douglas trips written in the new form are read by the old code as an unknown vehicle and fall back to its default, which is reported in the PR as the rollback cost.
- **M7-C:** revert; place IDs were not changed, so saved items resolve as before.
- **M7-D / M7-E / M7-F:** revert, or empty the registry. With no registry every setup reads not established, the orders panel says not checked and every vehicle result is not established.
- **A single wrong record:** set a claim to `unknown`, delete a link, or mark an order superseded, in a one-line change. Deleting a **restriction** needs its own owner approval in the PR, with the reviewed source that ends it; a restriction is never deleted to tidy data (trust principle 5).

## 22. Risks

Engineering risks with their mitigations. The material risks the owner should weigh are in 24.3.

| Risk | Mitigation |
|---|---|
| Removing the hard-coded behaviour drops a restriction | 12.4 migration rule and parity test; owner gate on M7-B |
| A claim is wrong at entry | Restrictions first; the publisher's own page only; owner approves each record |
| An order is read with the wrong scope or dates | Scope held as stated with its exhibit URLs; unclear scope retained in the orders panel; owner approves each order |
| Two instruments disagree | CE9 and 9.4: both shown; never `allowed` from a conflict |
| A stale fire record misleads | 24-hour age; a recorded restriction stays flagged; a recorded lifting becomes "not checked recently" |
| Vehicle vocabularies drift between M6 and M7 | One table and R139 |
| Douglas saved trips break | Migration on read; unknown values become not established; tested |
| Registries add load time | Lazy load after "map usable"; byte cap; measured |
| Research inputs treated as truth | Every [DRAFT-PR] item is an input; `last_confirmed_at` only after the coordinator's read and the owner's approval |

## 23. Unknowns

Stated as unknown; none blocks approval of the source-neutral sections.

- Whether the research reports that some research areas lie on ground closed to camping are correct. [DRAFT-PR 15] [UNK]
- Whether the Lincoln Creek listing is exempted from the order research says covers its corridor; the signed order and exhibit were not read by anyone. [DRAFT-PR 15] [UNK]
- Whether any approved source publishes designated dispersed sites, order scopes or fire stages as structured data. Research found none. [DRAFT-PR 15] [DRAFT-PR 35] [UNK]
- Whether the RIDB access agreement permits publishing stored facility records (M7-MR6). [DRAFT-PR 15] [UNK]
- Whether sleeping in a vehicle at a trailhead or pull-out counts as camping under the pilots' forest orders. [DRAFT-PR 15] [UNK]
- Whether the M5 specification is approved with stable land unit IDs, which RL10 and RL12 need, and whether place records carry a managing-unit field.
- Whether the M6 specification is approved with trailhead identities and `starts_at` links, which RL14 needs.
- Whether PR #20 (Scenario B) is merged before M7 closes.
- How many records a reviewer can keep within the proposed ages (M7-MR5).
- Whether 16 new strings (CP1) are enough once the detail is drafted.

## 24. Owner decision packet

One packet. The owner can acknowledge 24.1 explicitly (silence is not approval), accept 24.2 in one reply ("accept the recommended defaults", or list exceptions by ID), and should read and answer 24.3 separately. 24.4 lists engineering choices decided in the body, which need no answer. A recommendation is the coordinator's proposal only.

### 24.1 Settled by default (no decision needed; already binding)

1. Unknown is the default and is shown as unknown (trust principle 1, contract rule 1).
2. No inferred camping permission: never from a listing, facility, ownership, management, a mapped road or trail, or proximity (trust principle 2; contract rules 12 and 15; ROADMAP M7).
3. Staleness never weakens a restriction; positive claims fail closed (trust principles 5 and 6; contract rules 6 and 14).
4. Presentation never exceeds the evidence; trust-bearing wording changes only with owner approval (trust principles 7 and 8).
5. Proximity is not a relationship; relationships are source-backed, reviewed or unknown, and `relevant_to` only as an established chain (product principle 12; adventure model section 3; ROADMAP M7).
6. Generated geometry never produces point campsites (contract rule 9).
7. Availability is never a claim.
8. No community or third-party content in production data (M4 D8).
9. Budgets and performance limits inherited from M3, M4 and the M6 draft.
10. Milestone close requires a phone run of the canonical scenario by an independent tester and the six-heading product review (product scorecard).
11. No merge without the owner's approval of the exact head SHA; no ROADMAP, trust-principle or contract-rule change outside its own approved pull request.

### 24.2 Recommended defaults (acceptable in one reply)

| ID | Decision | Options | Recommendation | Bear case against it |
|---|---|---|---|---|
| M7-D1 | Scope and delivery | (a) PRs M7-A to M7-F on Aspen and Douglas only, neutral PRs first; (b) one combined PR after the source decision | (a) | Six gates and up to five device checks; owner bandwidth may bind first |
| M7-D2 | Narrow unlock for M7-C | (a) Confirm now that the already-published overnight records (Aspen listings and inventory, Douglas recreation sites) keep their existence role, with the site-type-to-kind table of 7.1; (b) wait for the full source decision | (a), only if the owner is comfortable deciding this one role ahead of the full decision | It pre-empts part of the source decision, including for RIDB records whose terms are unread (M7-MR6) |
| M7-D3 | Setups and statuses | (a) `tent`, `vehicle_sleeping`, `trailer_or_rv`, reserved `hammock`; statuses `allowed`, `restricted`, `prohibited`, `unknown` as M4; (b) one "camping" status | (a) | Four setups multiply review work; agencies rarely state vehicle sleeping explicitly, so most lines stay not established |
| M7-D4 | What can produce `allowed` | (a) Only a reviewed page of the responsible agency or operator for that one place, at site scope; never area, corridor or unit; never a facility dataset; (b) also an area-level designation page | (a) | Designated dispersed areas, where people actually camp near the pilots, cannot read allowed at area level |
| M7-D5 | Does `allowed` also need checked orders? | (a) Yes: `allowed` shows only when the place's `orders` coverage is checked within policy; (b) no | (a) | Almost nothing reaches allowed until orders are reviewed; Scenario A step 5 stays at "correctly unknown" longer |
| M7-D6 | One home for overnight permission | (a) Retire `supported_for_trip`, the `reviewed_sites` kind and the rules registry, migrating into the M7 registries; (b) keep both vocabularies | (a) | A contract retirement in a feature milestone; reverting M7-B must restore them together |
| M7-D8 | Orders past their stated end date | (a) Listed as ended on the stated date, successor not checked, never openness, until a later review records a successor or its absence; (b) treated as in force until re-reviewed; (c) dropped | (a) | (a) can read as "this closure is over" when the agency has reissued it; (b) is stricter but shows an order that has in fact ended as current |
| M7-D9 | Fire restrictions | (a) Mechanism for reviewed fire records with a 24-hour age; until someone commits to daily review, link-only lines per jurisdiction; retire the Pitkin page-hash monitor from display; (b) keep the monitor as is | (a) | Link-only fire lines send the user elsewhere for the question most likely to change on the day |
| M7-D10 | Freshness defaults | (a) 2,160 h developed-campground claims; 720 h designated dispersed, corridor and order-derived rules and orders; 24 h fire; 8,760 h place existence; (b) 720 h for every claim | (a) | See M7-MR5: the 720 h items decay monthly with one reviewer |
| M7-D11 | Vehicle vocabulary and profile | (a) One shared table (10.2), Aspen keys kept, explicit non-mapping of `high_clearance` and `four_wheel_drive`, profile of class + towing + optional length, Douglas labels migrated; (b) keep separate road and trail vocabularies | (a) | Two controls instead of one on a phone; "Truck with trailer" users must pick a class |
| M7-D12 | Restrictions carried from today's listings | (a) Carry `tent_only`, clearance, stay limit and each listing's road link as restrictions dated by the listing's `checked_on`, shown review overdue (12.4); (b) carry them as unreviewed source text only | (a) | (a) treats a curator's note of 2026-09-24 as a review date; (b) would remove exclusions users see today |
| M7-D13 | Source restriction text (Douglas) | (a) Kept as labelled source text, shown on every overnight-relevant record including picnic sites and the horse camp; never parsed into claims; (b) parse into claims | (a) | Users see "Overnight use prohibited." as source text with no status, the same weight as amenities |
| M7-D15 | Dispersed camping outside designated sites | (a) Not established everywhere in M7; area, corridor and unit rules may restrict only; (b) allow positive dispersed claims at area scope from agency pages | (a) | Users expecting "free camping" maps see nothing positive; the product looks emptier than competitors |
| M7-D16 | Day use | (a) `day_use_site` kind and `use_period`, never satisfying overnight; Scenario B's family base answered as day use; (b) out of M7 | (a) | Widens M7 beyond its title; one more kind to review |
| M7-D17 | Map-level camping status | (a) None, as M4 O3; (b) a neutral style for places with a reviewed prohibition | (a) | A user scanning the map cannot see prohibited places without opening each |
| M7-D18 | Wording process | (a) Constraints CP1–CP17 now; literals approved in the PR that renders them; (b) all literals in this specification | (a) | Literals approved piecemeal can drift in tone |
| M7-D19 | Budgets | (a) Section 17: inherited limits, research areas to zero, registries ≤ 150,000 bytes lazy; (b) a fixed per-registry cap | (a) | The registry cap is a guess until real records exist |
| M7-D20 | What completes M7 | (a) M7-A to M7-F; if the source decision is declined, A to C with the review saying plainly that reviewed permission, orders, vehicle constraints and backups were not delivered; (b) M7 is not complete without M7-E | (a) | A milestone titled Camping could close without answering "may I camp here?" for any place |

### 24.3 Material risks (flagged separately, each with its decision)

| ID | Risk and decision | Options | Recommended | Bear case |
|---|---|---|---|---|
| M7-MR1 | **Computed research areas on restricted ground (M7-D14).** 51 default-on polygons built from management, a trip-scoped designation and an uncited 300 ft buffer; research reports some overlap ground a current order closes to camping. [MEAS E1] [DRAFT-PR 15] | (a) Remove from display and data in M7-B; (b) keep, reworded, until orders are reviewed | (a) | Aspen's map loses its most visible overnight layer and looks emptier; users who used it to find candidate areas lose that, and the product says "not established" instead |
| M7-MR2 | **Order applicability computed from an order's stated scope (M7-D7).** Orders state scope as distance from listed roads or as survey townships. [DRAFT-PR 35] The adventure model says `constrained_by` is not derived. [REPO] | (a) Never computed: links only source-backed, by administrative unit through `governed_by`, or reviewed per place; computed candidates go to the build report; unlinked orders always in the orders panel; (b) computed from the stated scope, restricting direction only, labelled computed (CP7), which needs an adventure-model amendment | (a) | Under (a) an order that does apply to a campground is not shown on it until a person reviews the link; the user must open the orders panel to see it |
| M7-MR3 | **A listing overrides an order.** A recreation page lists sites while an order closes the corridor; showing the listing as allowed sends a user into a citation. Research names Lincoln Creek as a live case. [DRAFT-PR 15] | Covered by 8.4 step 2 and M7-D5 (a) | Accept 8.4 and M7-D5 (a) | Places inside an order's scope read prohibited or not established even where the agency intends them to be used, until the exemption is reviewed |
| M7-MR4 | **The source decision stays open.** M7-C to M7-F wait on L10. | — | Decide L10 with M6's source policy | M7 ships removal and wording only; Scenario A steps 4–7 move at best to "correctly unknown"; the milestone is foundation, not product |
| M7-MR5 | **Review load and decay.** Orders at 720 h, fire at 24 h, claims at 2,160 h, for up to 20 places and 12 orders per region. | Set the reviewer and cadence before M7-D and M7-E start | Decide reviewer and cadence first; size M7-D and M7-E to it | With one reviewer the product's answers decay to "review overdue" or "not established" within a month, and scenario scores can fall between milestones with no code change |
| M7-MR6 | **RIDB records published without a read access agreement.** Aspen publishes four RIDB-derived records today; research could not load the agreement text. [MEAS E1] [DRAFT-PR 15] | Owner reads the agreement before M7-C relies on RIDB records (part of L10) | Read it first; no expansion of RIDB use until then | If the terms restrict storage or redistribution, existing published data is already exposed and M7-C's identity work on those records is wasted |
| M7-MR7 | **A limit read as permission.** A forest-wide stay limit beside a place reads as "you may camp here for 14 days". | Covered by CE11 and CP9 | Accept CE11 and CP9 | Even with the fixed sentence, a phone user may read the limit line alone; the line is still shown, because hiding a restriction is worse |

### 24.4 Decided engineering choices (no owner answer needed)

The coordinator may change these by amendment within the trust rules and the validator rules, reporting any change to the owner.

| Choice | Recorded in |
|---|---|
| Identifier forms, reserved prefixes and legacy handling | 7.4 |
| Registry split into six files and their names | 7.3, 8.3, 8.7, 9.2, 10.3, 11.1 |
| `relevant_to` computed at view time, never stored | 11.5 |
| One pure evaluator module replacing `trip-rules.js` in `v2/`; `Trust.freshness` kept | 12.3 |
| Saved-value migration for Douglas vehicles | 12.3 |
| Rule numbering R130–R149 and invariant prefixes | 0.3 |
| Initial set sizes (12 orders, 8 places per region) | 20 |
| Quotation and summary lengths (25 words, 160 characters) | 7.3, 9.2 |

**Totals.** 20 owner decisions (M7-D1 to M7-D20: 18 recommended defaults in 24.2, and M7-D7 and M7-D14 decided with material risks M7-MR2 and M7-MR1 in 24.3); 7 material risks.

**Answer format:** `M7: accept defaults; D14 a; D7 a` (or name any default to change, for example `M7: accept defaults except D10 b; D14 b; D7 a`).

**Unlock.** The owner's source decision (L10) — sources per role, their terms reading, and the L7–L11 mappings — unlocks M7-C (without needing M7-D2), M7-D, M7-E and M7-F.

## Appendix A. Evidence basis

| Fact | Basis | Where |
|---|---|---|
| Overnight layers, counts, fields, rules registry, screening constants, Douglas records and source text, Rampart record, vehicle vocabularies, list filters, evaluator callers, producers, display sizes | [MEAS] | [m7-spec-evidence.md](../research/m7-camping/m7-spec-evidence.md) E1–E9 |
| Hard-coded behaviours H1–H14 | [REPO] [MEAS] | Files and lines in 12.1 |
| Trust rules, evidence semantics, fact coverage, rules 6, 9, 12, 15, R28, R50, register N6, N7, N8, N16 | [REPO] | `docs/product/trust-principles.md`; `v2/pipeline/docs/data-contract.md` |
| M7 scope and product-alignment expectations | [REPO] | `ROADMAP.md` M7, M8 |
| Relationship origins, coverage model, M7 obligations to M8 | [REPO] | `docs/architecture/adventure-model.md` sections 3–5 |
| Package boundary implications | [REPO] | `docs/architecture/continuous-explore.md` |
| Claim statuses, freshness table, registry-only value set, wording process | [REPO] | `docs/specs/M4-functional-recreational-water.md` sections 9 and 10 |
| Land unit IDs, coverage-record shape, `governed_by` and permission rules | [DRAFT M5] | `k-kopacek/m5-spec-draft` `2c329e3`: sections 7, 9, 10 |
| Rule numbering after R119; vehicle vocabulary and coordinator note; RL1–RL8; link shape; `orders` category reserved | [DRAFT M6] | `k-kopacek/m6-spec-draft` `82a3c84`: sections 0.3, 9.1, 9.6, 10 |
| Orders as entities, scope as stated, supersession, expiry, status observations, coverage example | [DRAFT-PR 35] | `docs/research/m7-camping/orders-as-entities.md`, `orders.example.json` on `research/m7-orders-model` |
| Overnight question decomposed, scope levels, precedence, `exempted_by`, research-area overlap, hard-coded list, candidate strings, risks and test ideas | [DRAFT-PR 15] | `docs/research/m7-camping/M7-camping-evidence-model-draft.md` on `docs/research-drafts` |
| Day use versus overnight, setup constraints, conflicting readings, two instruments | [DRAFT-PR 29] | `docs/research/m8-adventure/rampart-worked-example.md` |
| Scenario B, hammock line | [DRAFT-PR 20] | `docs/product/acceptance-scenario-rampart-day-use.md` on `docs/rampart-day-use-scenario` |
