# Milestone 5 specification — Land classification v1

Status: DRAFT — NOT APPROVED. Proposed by the coordinator for owner review; nothing here is decided.

**For:** Codex (implementation), once approved. **Reviewer / coordinator:** Claude. **Research:** coordinator, with Hermes optional while it is unavailable. **Base:** `main` at `c04f5d6`.
**Delivery (proposed):** four small sequential pull requests, PR A to PR D (section 16), on the two pilot regions only.
**Owner decisions:** every choice that is the owner's is listed in section 20 as M5-D1 to M5-D17, each with options, a recommendation and the bear case. None is taken. Where this document says "M5 does X", read "this draft proposes that M5 does X, subject to the decision named".

Governing documents: `AGENTS.md`, `ROADMAP.md` (M5, including the 2026-10-08 product-alignment acceptance expectations), `docs/agent-stack/roles.md`, `docs/product/trust-principles.md` (normative), `docs/product/product-principles.md`, `docs/product/product-scorecard.md`, `docs/product/acceptance-scenario-douglas-dirt-bike.md`, `docs/architecture/adventure-model.md`, `docs/architecture/continuous-explore.md`, ADR-005, ADR-006, `v2/pipeline/docs/data-contract.md` (normative for data), `docs/specs/M3-unified-mobile-explore.md` (section 13 and amendments A1–A14) and `docs/specs/M4-functional-recreational-water.md` (the format and precedent for source preservation, identifiers and reviewed registries).

**Research basis.** The M5 research exists only on the unmerged `docs/research-drafts` branch and is DRAFT / UNREVIEWED: `docs/research/m5-land/M5-preliminary-research-gate.md` (the "gate"), `current-land-audit.md` (the "audit"), `hermes/m5-land-source-matrix.md` and `docs/research/future-sources/source-watchlist-m5-m8.md`. This draft re-checked the facts it leans on hardest with four read-only metadata requests, recorded in [m5-spec-evidence.md](../research/m5-land/m5-spec-evidence.md) as E1–E4. Claims carry their basis:

| Mark | Meaning |
|---|---|
| [V-audit] | Measured from repository files in the audit (2026-10-07) |
| [V-live] | Read from a publisher's service by the gate's author (2026-10-07) |
| [E1]–[E4] | Read from a publisher's service for this draft (2026-10-19) |
| [REPO] | Read from a normative repository document |
| [H] | Stated by Hermes, not re-checked |
| [INF] | Inference in this draft from the marked facts |
| [UNK] | Not established by anything read |

## 1. Problem

**The map shows most of Douglas County with the source's private code, and never shows unknown land.**

- The land layer in both regions comes from layer 1 of the BLM National Surface Management Agency (SMA) limited-scale service. It holds one dissolved polygon per agency per state: 3 features in Aspen, 5 in Douglas County. The USFS feature is source `OBJECTID` 413 and the `PVT` feature `OBJECTID` 1069 in both regions, 170 km apart. [V-audit] [V-live]
- The polygons tile each extent completely: 1 m² of 1,197.8 km² is uncovered in Aspen, 40 m² of 2,180.8 km² in Douglas. The approved legend line W5, "Unshaded land is unknown — not private, not public, not open", describes a condition that occurs nowhere inside either region. [V-audit]
- `PVT` is the residual class. It covers 13.1% of Aspen and 71.8% of Douglas County, including 12 of the 14 named Douglas waterbodies over 5 ha (Cheesman Lake, Rueter-Hess Reservoir, Aurora-Rampart Reservoir among them). [V-audit] It is drawn with a tint like every other class and labelled W4, "PVT — the source's generalized private class; not a parcel-level finding". [REPO]
- The publisher does not call this class private. The same service publishes it as a sublayer named "Private or Unknown", and the only Colorado row in that sublayer has `ADMIN_AGENCY_CODE` `PVT`. [E1] [E2] Contract rule 11 allows a private classification "only where the source itself classifies land as private". [REPO] The source classifies this land as private *or unknown*. The current label is narrower than the source, and the tint says something about 72% of Douglas County that the source does not.

This is the defect M5 must fix first, and it can be fixed without any new source (section 8).

**The rest of what the audit found.**

- No identity below "the agency": every tap inside the USFS aggregate returns the same sheet; no forest, park or open-space name exists. The same source row has two IDs (`sma-413` in Aspen, `land-413` in Douglas). `OBJECTID` is a service row number and differs between layers of one service for the same row (`PVT` Colorado is 1069 in layer 1 and 25 in layer 31; 25 is BLM in layer 1). [V-audit] [E2]
- Two schemas for one source: different layer ID (`land_ownership` against `land`, register item N5), classification field, property set, freshness policy (`null` against 168 hours) and evidence wording. Aspen publishes a derived `manager` value of `Private` that nothing reads. [V-audit]
- Only `OBJECTID` and `ADMIN_AGENCY_CODE` are kept; every other source attribute is dropped. [V-audit]
- No dimension for access and no record of what was looked at: `fact_coverage.ownership` is `context`, `public_access` is `none`, in both regions. [REPO]
- The federal codes `NPS` and `FWS` would display as "unrecognised … unknown". [V-audit] (None is present in either pilot region; section 8.4.)

## 2. Goals

1. Nothing is shown, styled, ordered or worded as private unless a source classifies it as private, and the SMA residual class ("Private or Unknown") is never presented as private.
2. Unknown is visible on the map inside the coverage boundary.
3. The dimensions stay separate: management (managing agency and jurisdiction unit), ownership (only where a source states it), public-access evidence, spatial precision, and coverage of which questions were reviewed. A value in one never implies a value in another (section 4).
4. One land schema for both regions. Source attributes are preserved. Identifiers are stable, carry a source namespace, contain no region ID and no row number, and are the same in every region package for the same source record (section 7).
5. Named management units (a national forest, a recreation area, a county open space) where a source the owner has approved names them (PR C, gated by M5-D6).
6. Land evidence coverage: for each unit, which questions a person reviewed and when. In M5 access is "not reviewed" for every unit (section 9).
7. Identities and coverage that M6, M7 and M8 can relate to, with no relationship, access or permission record published by M5 (section 10).

**Product question (product principle 15).** After M5 a Douglas user can tell where the source records a public managing agency and where it records none, without being told that the rest is private; can see which named unit a spot lies in, where a source names one, with a link to the managing agency's own page where a person has reviewed it; and is told plainly, on every land unit, that access has not been reviewed. A user still cannot learn from Ohvernight whether they may enter, ride, park or camp anywhere. M5 is mostly a foundation milestone that also removes a misleading signal; section 21 says so in the form the product review requires.

## 3. Out of scope

- Any access, entry, crossing, parking, camping or activity claim, and any reviewed access registry with content. The `access` coverage category is defined and reserved (section 9).
- Parcels and assessor data from any source (OIT composite, county, commercial), and any owner name. Reasons: terms, personal data, static republication, false precision. [V-live] [H] [REPO]
- COMaP ("Under no circumstances are data to be REDISTRIBUTED"). [H]
- CPW, Colorado State Land Board and county open-space layers as published data, until their publishers' terms are established (M5-D17).
- Statewide work, a third region, continuous Explore and cross-package loading. Identifiers are designed not to block them (section 7).
- Any change to the region loader (`v2/explore/region-loader.js`), the renderer or map adapter (`v2/explore/map-adapter.js`, Leaflet, the adapter's twelve exports), ADR-006, a new dependency, build step or basemap. **Interpretation, for the owner to confirm in M5-D1:** "no renderer change" is read as no change to those files and decisions. The land presentation module `v2/explore/land-style.js` (owned by M3 section 13), the display build, the manifests and the region `explore.json` files do change.
- Wilderness names and rules. The wilderness layers are unchanged; 3.57 km² of Aspen wilderness lying on today's `PVT` polygon simply stops being contradicted by a tint once PR B lands. [V-audit] Naming wilderness is recorded as a later candidate.
- Relationship records of any kind (`governed_by`, `starts_at`, `relevant_to` and the rest of the adventure model).
- Trails, roads, water, camping and trip rules.
- A definition of tier A (M5-D9).
- Display of, or branching on, any source access attribute (`Pub_Access`, Douglas `PUB_ACCESS`, Pitkin `public_access`, `restriction`, `closure`) (M5-D8).

## 4. Dimensions and evidence model

### 4.1 Dimensions

| Dimension | Question | Carried as | M5 source | What it never implies |
|---|---|---|---|---|
| Management | Which agency does the source list as managing this surface, and which unit? | Source code `admin_agency_code` (SMA) or `mang_type` / `mang_name` (PAD-US); derived `management_level`; the land unit's `id` | SMA (A, B); PAD-US if approved (C) | Ownership, access, permission, rules |
| Ownership | Who owns the land? | Only a field the source names as ownership: PAD-US `own_type`. Canonical only; not displayed in M5 (M5-D7) | PAD-US if approved | Access, or its absence. Private ownership does not establish that access is prohibited (contract rule 12) |
| Public-access evidence | May the public enter, and to do what? | Nothing. Coverage category `access` is "not reviewed" for every unit | None | — |
| Spatial precision | How exactly is the boundary drawn? | Layer `spatial_precision`; every M5 layer is `generalized` (M5-D9) | Per layer | A property line, a surveyed boundary, or which side of a line a spot is on |
| Coverage | Which questions has a person reviewed for this unit, against what, and when? | `land-coverage.json` records (section 9) | Manual review | That anything is allowed. Reviewed with nothing found settles nothing |

The SMA is a management dataset, not an ownership dataset: the publisher states that the SMA data "do not illustrate land status ownership pattern boundaries". [V-live] The contract already has no `ownership` layer kind. [REPO] M5 therefore publishes management as the land classification and treats ownership as an optional source fact.

Provenance, transport, verification and freshness keep their contract 5.4 meanings unchanged.

### 4.2 Evidence classes

M4's four classes apply (M4 section 4):

| Class | In M5 |
|---|---|
| Source fact | SMA agency code and attributes; PAD-US unit name, manager, owner type, designation, source date and identifier |
| Official information, reviewed | A management coverage record: a person read the managing agency's own page on a date (section 9) |
| Derived fact | `management_level`, area, display selection |
| Community signal | None. No field allows one |

### 4.3 Never

These restate trust principles 1, 2 and 7 and contract rules 11–15 for land. A validator rule or test enforces each where it can (sections 13 and 15).

1. Non-federal is not private.
2. Public or agency-managed is not accessible, and private is not closed.
3. `PVT` from the SMA, and the source's "Private or Unknown" class, are never shown as private: no label, title, legend entry, tint, ordering or filter says or implies private.
4. Unshaded land means unknown and nothing else, inside or outside the coverage boundary.
5. No record in a unit source is not "unprotected", "private" or "unmanaged". PAD-US lists only land someone reported. [E4]
6. A source access attribute is never an Ohvernight access value.
7. Containment inside a land polygon is not `governed_by`; it is context only (adventure model section 3).
8. A generalized boundary is never drawn or described as a property line.

## 5. Sources

### 5.1 Candidates

"Terms" quotes what the publisher says. A blank licence field, a public endpoint or an open-data portal is not permission. No row below is a licence interpretation; every use is the owner's decision.

| # | Source | What it gives M5 | Terms, as the publisher states them | Identifier | Proposed role |
|---|---|---|---|---|---|
| S1 | BLM National SMA, limited scale, layer 1 (in use) | Managing-agency class per state; fields `ADMIN_DEPT_CODE`, `ADMIN_AGENCY_CODE`, `ADMIN_UNIT_NAME`, `ADMIN_UNIT_TYPE`, `HOLD_ID`, `HOLD_DEPT_CODE`, `HOLD_AGENCY_CODE`, `ADMIN_ST`, `FAU_ID`, `SMA_ID`, `OBJECTID` [V-live] | Copyright text "Bureau of Land Management, (BLM)". No licence stated. [V-live] Already published by this site under M2 and M3 | None stable. `SMA_ID` is a class code (BLM = 2) [V-live]; `OBJECTID` is a row number [E2] | Management background in PR A and PR B (M5-D4) |
| S2 | BLM Colorado SMA | Finer polygons (260 intersect the Aspen box, 119 the Douglas box); `adm_manage` classes including `PRI` "Private" and `LOCAL` "State, County, City: Areas" [V-live] [E3] | BLM ISO record: "None, these data are considered public domain." Asks that BLM be cited and modifications described. [V-live] | `GlobalID`, persistence [UNK]. `adm_name` null in 5 of 5 sampled rows [V-live] | Not adopted in M5; recorded alternative (M5-D4) |
| S3 | USGS PAD-US 4.1, fee managers layer | Named units (Pike National Forest, Chatfield Recreation Area, Hidden Mesa) with manager, owner type, designation, source date; 487 records intersect the Douglas box, 91 the Aspen box [V-live] | "This content describes the PAD-US dataset which is in the public domain." followed by "Users are obligated to follow the terms of use of the PAD-US Data Explorer and any accompanying content." Those terms were not read [V-live] [UNK]. Citation text with DOI 10.5066/P96WBCHS [E4] | `Source_PAID`, populated in 5 of 5 sampled rows in three formats; uniqueness and persistence across releases [UNK] [V-live] [E4] | Named units in PR C, only if M5-D6 approves it after the owner reads the Data Explorer terms |
| S4 | USFS Administrative Forest boundaries | `ADMINFORESTID`, `FORESTNAME` [H] | "intended for read-only use"; not legal boundaries [H] | `ADMINFORESTID`, persistence [UNK] | Alternative for national-forest identity only (M5-D6) |
| S5 | Colorado State Land Board trust land | Trust-land context. Trust land "is not open to the public" without a lease or programme [H] | Official GIS publication and terms not identified [UNK] | [UNK] | Not used (M5-D17) |
| S6 | County open space (Douglas `OPEN_SPACE`, Pitkin Open Spaces) | Named county units with fields including access-like attributes [V-live] | No licence stated [V-live]; Douglas policy says data "may be subject to a separate contract or leasing agreement" [H] | `GLOBALID` / `globalid`, persistence [UNK] | Not used (M5-D17) |
| S7 | CPW `CPWAdminData` | State wildlife areas, state parks, walk-in access [V-live] | "product and property of the Colorado Parks and Wildlife" with an indemnity clause; "for public distribution" in the service description; no grant to republish a derived copy [V-live] | [UNK] | Not used (M5-D17) |
| S8 | COMaP | Owner, manager, easement, public-access fields [H] | "Under no circumstances are data to be REDISTRIBUTED." Paid subscription [H] | [UNK] | Excluded |
| S9 | Parcels (OIT composite, county assessor, commercial) | Owner names and addresses [V-live] | OIT: "Resale of this data is strictly forbidden." [V-live]; Regrid forbids making data available to third parties [H] | `parcel_id` and others | Excluded |

### 5.2 Proposed default and the alternatives

**Default.** PR A and PR B depend only on S1, which the site already publishes. They fix the residual-class defect, preserve the source, unify the schema and set the identifier rule with no new source and no licence question. PR C depends on S3 and does not start until the owner decides M5-D6 after reading the PAD-US Data Explorer terms; this draft does not treat those terms as cleared. If the owner declines S3, the alternative is S4 for national-forest identity only; if both are declined, PR C is dropped and land identity stays at the agency-in-state level of S1, which the milestone review must state plainly. S2 is not adopted: it names no unit, its `PRI` class is labelled "Private" by the publisher while whether it is a residual is unknown [E3], and its slivers and bytes are unmeasured.

### 5.3 Fetches and snapshots

- **PR A** performs exactly one controlled refresh of S1 for both regions (M5-D5), with every attribute the layer returns. No other source is refreshed. Every non-land canonical file is byte-identical before and after, and PR A proves it.
- **PR C**, if approved, performs exactly one controlled fetch of S3 at release 4.1, clipped to each region's coverage geometry, attributes and geometry for the fields of section 6.2 only.
- Each fetch commits a snapshot record under `docs/research/m5-land/`: service URL and layer ID; the service's `currentVersion` and any data-date text; retrieval timestamp (UTC); the exact `where`, `outFields`, geometry filter and page size; counts per region; the SHA-256 of each canonical file before and after; and, for S1, a difference report against today's data by agency code (area, parts, vertices) so that a changed boundary is visible. A difference not explained by "more fields kept" stops the PR: Codex reports and waits.
- `RIDB_API_KEY` is not involved. No credential is used.

## 6. Land record and fields retained

### 6.1 SMA management layer (both regions, PR A)

Layer ID `land` in both regions (Aspen's `land_ownership` is renamed; M5-D11). Kind `land_management`, `spatial_precision` `generalized`, `classification_source_field` `admin_agency_code`.

Copied from the source without interpretation, under `fields.source`:

| Property | From | Notes |
|---|---|---|
| `admin_agency_code` | `ADMIN_AGENCY_CODE` | The classification field. Verbatim, uppercase as published |
| `admin_dept_code` | `ADMIN_DEPT_CODE` | |
| `admin_state` | `ADMIN_ST` | |
| `admin_unit_name` | `ADMIN_UNIT_NAME` | Null on every Colorado row checked [V-live]; kept so a later non-null value is visible |
| `admin_unit_type` | `ADMIN_UNIT_TYPE` | |
| `hold_id`, `hold_dept_code`, `hold_agency_code` | `HOLD_ID`, `HOLD_DEPT_CODE`, `HOLD_AGENCY_CODE` | Kept verbatim; no M5 rule reads them |
| `fau_id` | `FAU_ID` | Kept verbatim; no M5 rule reads it |

Not kept: `OBJECTID` (a row number; recorded in the snapshot document only, so nothing can key on it), `SMA_ID` (a class code that duplicates the agency code), shape length and area fields (recomputed if needed).

Computed by the pipeline, under `fields.derived`: `source_namespace` (constant `blm_sma_natl`), `management_level` (section 8), `legacy_ids` (section 7.3).

Removed: Aspen's derived `manager` (`BLM`, `USFS`, `Private`, `State_CO`, `Local`, `Unknown`), Aspen's `raw_admin_agency` (replaced by `admin_agency_code`), Aspen's constant `land_class` and `camping_permission` on land features, Douglas's `manager` (replaced by `admin_agency_code`) and Douglas's `name` (always equal to the code). Absence of `camping_permission` means unknown, as it does everywhere (contract 5.4 rule 1).

### 6.2 PAD-US unit layer (both regions, PR C, if M5-D6 approves S3)

Layer ID `land_units`, kind `land_management`, `spatial_precision` `generalized` (M5-D9), `classification_source_field` `mang_type`.

| Property | From | Notes |
|---|---|---|
| `name` (reserved) | `Unit_Nm` | The source's unit name. Not listed under `fields`, as for water |
| `source_paid` | `Source_PAID` | The identifier (section 7) |
| `mang_type`, `mang_name`, `loc_mang` | `Mang_Type`, `Mang_Name`, `Loc_Mang` | Manager as recorded by the source. Coded values keep the source's domain label (E4) |
| `own_type` | `Own_Type` | Ownership dimension, canonical only (M5-D7) |
| `des_tp`, `loc_ds` | `Des_Tp`, `Loc_Ds` | Designation as recorded; not an access rule [H] |
| `loc_nm` | `Loc_Nm` | Local name as recorded |
| `feat_class`, `category` | `FeatClass`, `Category` | |
| `state_nm` | `State_Nm` | |
| `gis_src`, `src_date` | `GIS_Src`, `Src_Date` | The source's own record date; not the retrieval date (contract 5.4 rule 3) |
| `gis_acres` | `GIS_Acres` | |

Not kept, by name: `Own_Name` (an owner's name; M5-D7), `Pub_Access`, `Access_Src`, `Access_Dt` (access attributes; sampled values were defaults, "OA" from "GAP - Default" in 5 of 5 rows [V-live]; M5-D8), `GAP_Sts` and `IUCN_Cat` (biodiversity management intent, easily misread as access [H]), easement holder fields.

Derived: `source_namespace` (constant `usgs_padus`), `source_release` (constant `4.1`), `management_level`, `legacy_ids` (empty at creation).

No property on any land feature states access, ownership as a conclusion, or permission. The reserved properties `land_class`, `camping_permission`, `access_status`, `access_reason` and `evaluated_trip` are not used on land features (R79).

## 7. Identifiers (M5-D10)

### 7.1 Rule

A land unit ID is `<namespace prefix>-<source key>`. It is computed only from the source record. It never contains a region ID, a service row number or a sequence number. The prefixes are reserved:

| Namespace | Prefix | Source key | Example |
|---|---|---|---|
| `blm_sma_natl` | `sma-` | lowercase `ADMIN_ST`, `-`, lowercase `ADMIN_AGENCY_CODE` | `sma-co-usfs`, `sma-co-pvt` |
| `usgs_padus` | `padus-` | lowercase `Source_PAID` | `padus-g603020` |

Characters outside `[a-z0-9-]` are removed after lowercasing; the unmodified source value stays in its source field. Today's SMA layer has one row per agency per state [V-live]; PR A verifies this on the refreshed data. If two rows of one fetch produce the same ID, or a record has an empty key, the build stops and reports. There is no fallback to `OBJECTID` and no suffix to make IDs unique. Extending the key (for example with `ADMIN_DEPT_CODE`) is an owner decision.

`source_namespace` plus the source key identify the source record. The Ohvernight `id` is the only key other files use.

### 7.2 Across region packages

- **The same source record has the same ID in every region package.** USFS in Colorado is `sma-co-usfs` in Aspen and in Douglas County; today it is `sma-413` and `land-413`. [V-audit]
- **An ID identifies what its source identifies, nothing more.** `sma-co-usfs` is "the SMA's USFS row for Colorado". It is not White River National Forest and not Pike National Forest. Two forests in two regions sharing `sma-co-usfs` are the same *source record*, not the same forest.
- **A real-world unit crossing packages is one unit only where a source identifier establishes it.** If one PAD-US record covers Pike National Forest in Douglas County and in a future third region, both packages carry `padus-<that Source_PAID>`: one unit with two delivered parts (continuous-explore, data-loading implication 4). If the source splits a forest into several records, it stays several units. M5 never merges records by name, by touching geometry or by shared manager.
- **Clipping is a display concern.** Each package holds the part of a unit inside its coverage. Non-geometry source fields of one ID are identical in every package; a repository-level test checks it (R82). R21's uniqueness stays per region, as the contract defines it.

### 7.3 Legacy IDs

Every land feature that existed before PR A carries its old ID in `legacy_ids`, under the rules of M4 amendment A4: an ID once in `legacy_ids` stays there; a feature's own ID is never in its `legacy_ids`; a legacy ID on two features stops the build. Old and new features are matched by agency code and state, read from the committed data, never by row number. Expected: Aspen `sma-413`, `sma-1069`, `sma-25`; Douglas `land-413`, `land-1069`, `land-1055`, `land-1017`, `land-1028`.

No alias file is added unless PR A finds a reference to a land feature ID or to the layer ID `land_ownership` in saved state, a URL parameter or configuration other than the Aspen `explore.json` entry it renames. The region storage keys today are trip and plan keys only [REPO]; PR A verifies and reports.

## 8. Classification vocabulary and the residual class

### 8.1 Fixed tables (M5-D3)

One committed configuration file, `v2/pipeline/config/land_classes.json`, read by the build and the validator, holds both tables and the display rule.

`management_level` from SMA `admin_agency_code`:

| Code | `management_level` | Note |
|---|---|---|
| `USFS`, `BLM`, `NPS`, `FWS`, `BOR`, `DOD`, `OTHFE` | `federal` | |
| `ST` | `state` | |
| `LG` | `local` | |
| `PVT` | `none_recorded` | The publisher's class is "Private or Unknown" [E1] [E2]. M5 records that the source lists no public managing agency, not that the land is private |
| anything else | `unrecognised` | Shown as unknown with W6, as today |

`management_level` from PAD-US `mang_type`:

| Code (source label [E4]) | `management_level` |
|---|---|
| `FED` Federal | `federal` |
| `STAT` State | `state` |
| `LOC` Local Government | `local` |
| `DIST` Regional Agency Special District | `special_district` |
| `TRIB` American Indian Lands | `tribal` |
| `NGO` Non-Governmental Organization | `non_governmental` |
| `PVT` Private | `private_recorded` |
| `JNT` Joint | `joint` |
| `UNK` Unknown | `unknown` |
| anything else, including `TERR` and `DESG` | `unrecognised` |

Rules:

1. `private_recorded` is produced only from a source field whose value is the source's private code with no "or unknown" alternative. Today that is PAD-US `mang_type` `PVT`, a record of a voluntarily reported private protected area [E4], and it is a statement about the manager, not about access (contract rule 12). SMA `PVT` never produces it.
2. `management_level` is a data value for later milestones. In M5 it drives display selection (8.2) and is never itself shown as a label. Labels come from the source's own codes and names through the fixed strings of section 11.
3. A code not in a table is `unrecognised`, never a guess. Adding a code is a one-line config change with its own review.

### 8.2 Residual-class display (M5-D2)

Canonical data keeps every SMA feature, including `sma-co-pvt`. The display build excludes features whose `management_level` is `none_recorded`, exactly as M4's display excludes ineligible water. Consequences:

- Inside the coverage boundary, land the source assigns to no public managing agency is **unshaded**, and W5 becomes true for the first time. The legend adds LW1 (section 11) to say why so much is unshaded.
- It is **not selectable**. A tap there behaves as a bare-map tap (M3 A14), or selects a named unit where PR C draws one.
- Shaded share after PR B, computed from the audit's areas: Douglas County 28.2% (`USFS` 26.16, `LG` 0.87, `OTHFE` 0.66, `ST` 0.51) and unshaded 71.8%; Aspen 86.9% shaded and 13.1% unshaded. [V-audit] [INF] Most of Douglas County will read as unknown. That is honest, and it may look like a regression (section 18, risk RK3).
- W4 is no longer used and is retired. No other W string changes.

Alternatives for the owner: keep the residual polygon selectable with no fill and a detail sheet; or keep today's tint with a new label. Section 20 gives the cases.

### 8.3 Classes that remain shaded

Every other class keeps M3 section 13: tier G, one low-saturation tint per code, W8 labels, W6 for an unrecognised code, no outline at zoom 14 or more, no red, no ranking. The legend lists codes present in the display data.

### 8.4 Codes absent from both pilots

`NPS`, `FWS`, `BOR` and `DOD` are in the table but absent from both regions [V-audit]; they would be shown with W6 ("unrecognised source code; unknown"), which is safe. Adding W8 labels for them is new user-visible wording and is deferred until a region contains one.

## 9. Land evidence coverage

### 9.1 Registry (PR D)

`v2/regions/<id>/land-coverage.json`, curated by hand, validated. The manifest gains an optional top-level `land_coverage` path, additive to contract version 1.

```json
{"schema_version": 1,
 "records": [
  {"subject_id": "padus-…",
   "category": "management",
   "jurisdiction": "USDA Forest Service",
   "summary": "The Forest Service's page for this forest names it and states the Forest Service manages it.",
   "evidence": {"source_url": "https://www.fs.usda.gov/…", "agency": "USDA Forest Service",
                "basis": "manual_review", "last_checked_at": "…", "last_confirmed_at": "…",
                "max_age_hours": 8760}}]}
```

This is the adventure model's evidence-coverage item (section 4 of that document), narrowed for land:

| Field | Meaning |
|---|---|
| `subject_id` | A land unit ID in this region (`sma-…` or `padus-…`) |
| `category` | `management` (refines fact dimension `ownership`) or `access` (refines `public_access`). In M5 only `management` is accepted; `access` is reserved and rejected by the validator (R83, M5-D13) |
| `jurisdiction` | Whose page was read |
| `summary` | At most 160 characters, written by the reviewer, not copied. What the page establishes about who manages this unit. It never mentions access, entry, activity or permission |
| `evidence` | The contract 5.4 claim evidence fields, with `basis` `manual_review`, a URL on the managing agency's own site, and `last_confirmed_at` set only after the coordinator has read the page and the owner has approved the record |

Rules:

1. **Absence is "not reviewed".** Only reviewed items are stored. Every unit and category with no record is shown as not reviewed. Generalized context data is never a review (adventure model, coverage rule 3).
2. **A review is scoped** to one unit, one category and one jurisdiction. It does not spread to neighbouring units, to the SMA background row, or to other categories.
3. **A management review never creates access or permission.** It says whose rules apply and where the agency publishes them; it does not say what they are.
4. **A review whose page disagrees with the unit record** (a different manager, a unit the page does not name) produces no record. The disagreement is reported in the pull request; the source data is not edited to match.
5. **Freshness** is computed from `last_confirmed_at` and `max_age_hours`, never stored. A management review past its age is shown with "Review overdue" and is not removed. No restriction is involved, so trust principle 5's asymmetry does not arise; the record simply ages visibly.
6. **No single score.** Coverage is shown as a list of categories with results.

### 9.2 Initial set (PR D)

At most five units per region, chosen as the units that contain the most displayed trail length or recreation sites in that region, reviewed in that order. Expected candidates: in Douglas County, the unit holding Pike National Forest and the unit holding Chatfield (recorded by PAD-US with manager `USACE` [V-live], a deliberate test of "manager is not operator"); in Aspen, the unit holding White River National Forest. If PR C did not land, the subjects are SMA IDs (for example `sma-co-usfs`) and the summary may say only what the agency's page says about that agency's land in Colorado.

Each record has a dossier (page URL, the exact sentences relied on, date read) under `docs/research/m5-land/coverage/`. The coordinator reads the managing agency's page and writes the dossier. Hermes may prepare a draft dossier when it is available, but PR D does not depend on it: Hermes web research has been unavailable since 2026-10-08 (coordinator correction K4, PR #38). Whoever retrieves the page, a retrieval is not a review (ADR-004, ADR-005): `last_confirmed_at` is set only after the coordinator has read the page and the owner has approved the record in the pull request.

### 9.3 Fact coverage

`fact_coverage.ownership` becomes `reviewed_partial` in a region when its `land-coverage.json` has at least one record; its statement is rewritten (section 11.3). The contract's requirement for `reviewed_partial` is extended to accept a non-empty land coverage registry (R84), as M4 extended it for the water registry. `fact_coverage.public_access` stays `none` in both regions throughout M5.

## 10. What M5 provides to M6, M7 and M8

The adventure model asks M5 for "management and jurisdiction as an identity other entities can be `governed_by`; ownership kept separate from access; access left unknown where not established; stable, namespace-safe IDs; evidence coverage for ownership/management and access per area". [REPO]

| M5 provides | M5 does not provide |
|---|---|
| Land unit identities under section 7: namespaced, source-derived, identical across region packages for the same source record | Any relationship record. No `governed_by` is published, derived or stored by M5 |
| `management_level` and the source's own management fields on each unit | Access, entry, crossing, parking, camping, activity or overnight permission, in any form |
| Ownership as a separate canonical source fact where PAD-US states an owner type | Ownership display, owner names, parcels, title |
| Land evidence coverage records keyed by unit ID, with `management` reviewed for a few units and `access` not reviewed for every unit | Restrictions, closures, orders, seasons or fire status for land |
| `none_recorded` land drawn and worded as unknown | A finding that any land is private, public, open or closed |
| `spatial_precision` per layer, all `generalized` | A boundary precise enough to say which side of a line a spot, campsite or trailhead is on |

Rules for later milestones, recorded here so they are not lost; none is implemented in M5:

1. **`governed_by` comes from the entity's own source field, never from containment.** M6 may relate a trail to a land unit only where the trail record names its managing unit in a field the source documents (for example a Forest Service administrative-unit code) and a documented, reviewed mapping links that code to a land unit ID. A trail lying inside a polygon is context only (adventure model section 3, contract rule 13).
2. **A land unit is never an input to permission.** M7 must not derive dispersed-camping permission, a stay limit or a vehicle rule from a unit's manager, owner type or designation. Those come only from the agency's own rules, reviewed, as claims.
3. **M8 lists access as unknown for every unit** until a later milestone specifies access review. An M8 candidate that crosses or stages on land shows `Access: not reviewed` (LW8) as one of its listed unknowns.
4. **The `access` coverage category is reserved.** Its future shape follows section 9 with `category: "access"` and points to a separate, restriction-first access claim registry modelled on M4's `water-recreation.json`: unknown by default, restrictions and closures as the operator states them, and no positive status until the owner approves a review process. Neither the registry nor any record is created in M5.
5. **`none_recorded` and "no record" stay unknown downstream.** No later milestone may convert them to private, to "unrestricted" or to an empty result.

## 11. Presentation and trust wording

### 11.1 Where presentation changes

Only `v2/explore/land-style.js` (legend and detail), the display build and the manifests and `explore.json` files change. The adapter, its exports, hit testing and the camera policy of M3 A14 are untouched. Section 13 of M3 stands except where this section says otherwise:

- **PR B.** The legend no longer lists a `PVT` entry, because no `PVT` feature is displayed; W4 is retired. LW1 is added after the class entries and before W5 whenever the display index reports at least one feature excluded as `none_recorded` for that layer (section 12). W5 remains last and always present.
- **PR C.** The `land_units` layer is tier G with one neutral tint from the existing palette, fill opacity at most 0.06, dashed outline at most 1 px and none at zoom 14 or more. It has no per-type legend entries; its legend is LW2 only. It is listed above `land` in `explore.json`, so where both are drawn a tap selects the unit. A unit whose source name is null is not displayed and is counted in the PR C report. A unit whose `management_level` is `private_recorded` (a privately managed protected area the source reports) is kept in canonical data and not displayed in M5: naming it on the map raises a question M5 cannot answer, and LW3 would then print the word "Private" as a source label (M5-D7). The generic overlap chooser stays deferred (M3 A13).
- **PR D.** Coverage lines (LW6 or LW7, then LW8) are added to every land detail.

No land layer uses red, a warning style, a clearance style or a ranking. Nothing on a land feature is styled to suggest access or its absence.

### 11.2 Fixed strings (M5-D14)

Proposed exact text. Implementation uses each byte for byte, in both regions, and tests compare it against a literal. None contains "verified", "legal", "permitted", "open to" or the bare words "Private" or "Public" as a label (M3 A4 and section 13.2 rule 3). `<…>` marks a value taken from data.

| ID | Exact text | Where | Cause | PR |
|---|---|---|---|---|
| LW1 | `Unshaded inside the region: the source records no public managing agency here. That is not a finding that the land is private.` | Legend of the `land` layer, after the class entries, before W5 | The display index reports at least one `none_recorded` feature excluded from that layer | B |
| LW2 | `Named land units compiled by PAD-US — not parcels` | Legend heading of the `land_units` layer | The layer is listed | C |
| LW3 | `Manager recorded by the source: <manager>` | Unit detail, first line under the title | Every displayed unit. `<manager>` is the source's coded-value label for `mang_name` | C |
| LW4 | `Compiled boundary. It cannot locate a property line or tell you whether a specific spot is inside this unit.` | Unit detail | Every displayed unit | C |
| LW5 | `Source record dated <date>` | Unit detail, after "Source fetched" | The unit's `src_date` is present. It is the source's date, not Ohvernight's retrieval date | C |
| LW6 | `Management: reviewed <date>` | Every land detail, coverage lines; followed by the reviewer's summary, the agency, the existing "View source ↗" link, and WW7 `Review overdue` when past age | The unit has a `management` coverage record | D |
| LW7 | `Management: not reviewed` | Same place as LW6 | The unit has no `management` coverage record | D |
| LW8 | `Access: not reviewed` | Every land detail, last coverage line | Every land unit, throughout M5 | D |

Retired: W4 (PR B). Unchanged: W1–W3 and W5–W11. Reused unchanged: WW7 `Review overdue` (M4), "View source ↗", "Source fetched".

### 11.3 Manifest text (trust-bearing; M5-D14)

Manifest wording is rendered verbatim in the land detail and changes only with owner approval (trust principle 8). Proposed exact text, identical in both regions:

| ID | Field | Exact text | PR |
|---|---|---|---|
| LL1 | `land` layer `limitations` | `Limited-scale managing-agency context. Classes are the source's agency codes, shown as published. An unrecognised code is unknown.` | A |
| LL2 | `land` layer `limitations` | `Limited-scale managing-agency context. Classes are the source's agency codes, shown as published. Land the source assigns to no public managing agency is not drawn and is unknown, not private.` | B (replaces LL1) |
| LL3 | `land_units` layer `limitations` | `Named units as compiled by PAD-US 4.1 from many agencies and organisations. Boundaries are generalized and some records are years old. A unit is not evidence of access or of any allowed activity.` | C |
| OS1 | `fact_coverage.ownership.statement` | `Limited-scale managing-agency polygons only; not parcels or surveyed boundaries. Where the source records no public managing agency the land is unshaded and unknown, not private.` | B |
| OS2 | `fact_coverage.ownership.statement` | `Limited-scale managing-agency polygons, and named units where PAD-US records one; neither is a parcel or a surveyed boundary. Where no public managing agency is recorded the land is unshaded and unknown, not private.` | C (replaces OS1) |
| OS3 | `fact_coverage.ownership.statement` | OS2 or OS1 as current, followed by: ` A few units carry a reviewed statement of who manages them; every other unit is not reviewed.` | D |

`fact_coverage.public_access.statement` is unchanged in both regions. PR A changes no visible wording except LL1, which replaces two region-specific limitation sentences, one of which names the removed `manager` field.

### 11.4 Detail content

For an SMA feature, after PR B and PR D, in order: W11; the W8 or W6 label; the agency and "View source ↗"; "Source fetched `<date>`"; W7; W3; LW6 or LW7, then LW8; the ownership statement; the public-access statement; the layer limitation. This is M3 13.2 rule 6 with the coverage lines inserted.

For a unit, after PR C and PR D: title from the source name; LW3; the agency and "View source ↗"; "Source fetched `<date>`"; LW5 where present; LW4; W3; LW6 or LW7, then LW8; the ownership statement; the public-access statement; LL3.

No owner type, designation, area or access attribute is shown in M5.

## 12. Contract changes

All additive to contract version 1 and documented in `v2/pipeline/docs/data-contract.md` in the pull request that introduces them.

| Change | PR |
|---|---|
| Land source and derived fields (section 6.1); `source_namespace`, `management_level`, `legacy_ids`; removal of the unread constants and vocabulary; Aspen layer ID `land_ownership` renamed `land` (register item N5 retired) | A |
| `v2/pipeline/config/land_classes.json` | A |
| R28's land clause ("if any other property equals `private` … that source field must equal `PVT`") replaced by R79, which is stricter; the requirement for a non-empty classification field is kept | A |
| Display selection by `management_level`; the display index records, per land layer, `excluded_by_class` (a count per excluded `management_level`); R61's exception list extended from "the water selection rule" to "the water or land selection rule" | B |
| New register entry N19, "SMA residual class `PVT` was shaded and labelled as a private class", recorded and retired in PR B with R80 as its marker | B |
| `land_units` layer and its fields (section 6.2) | C |
| `land-coverage.json`, manifest `land_coverage` path, the `reviewed_partial` extension | D |

## 13. Validator rules

New stable rule IDs, continuing after R76. Each has at least one negative test on a fixture and, where it protects real data, a mutation proof on the committed files (run locally, not committed).

| ID | Rule | PR |
|---|---|---|
| R77 | Every `land_management` feature has `source_namespace` in the namespace table of 7.1, a non-empty source key, and `id` equal to the prefix plus the sanitised key computed from its own source fields. No land ID contains the region ID or a value equal to a source row number. IDs are unique within the region | A, C |
| R78 | `land_classes.json` has exactly the tables of 8.1; every land feature's `management_level` equals the value computed from its code by that file; a code outside the table is `unrecognised` | A, C |
| R79 | No land feature, canonical or display, carries a reserved property of contract 5.4 other than `id`, `name` and `evidence`; none carries a property whose name contains `access`, `permission`, `camp` or `open`; and no property value equals or begins with `private` (case-insensitive) except `management_level` `private_recorded` on a `usgs_padus` feature whose `mang_type` is `PVT` | A, C |
| R80 | A land display artifact contains no feature whose `management_level` is `none_recorded` or, from PR C, `private_recorded`; its feature set equals the canonical set minus exactly those features (and, for `land_units`, units with a null name); `excluded_by_class` equals the computed counts | B, C |
| R81 | `legacy_ids` on land features is an array of distinct non-empty strings; no legacy ID appears on two features; no legacy ID equals the current ID of any feature in the region | A |
| R82 | Repository level, across every region manifest: a land unit ID present in more than one region has the same `source_namespace` and identical values for every `fields.source` property in each | A, C |
| R83 | `land-coverage.json` conforms to 9.1: `subject_id` resolves to a land unit in that region; `category` is `management` (an `access` record fails in M5); one record per subject and category; `summary` non-empty and at most 160 characters; complete evidence with `basis` `manual_review`; `source_url` not on a host listed in `land_classes.json` `non_review_hosts` (initially the ArcGIS hosts named in section 5 and the community hosts named in the M4 configuration) | D |
| R84 | `fact_coverage.ownership` is `reviewed_partial` only when `land-coverage.json` has at least one record, and its `layer_ids` name the region's land layers; `fact_coverage.public_access` is `none` in every region | D |
| R85 | Every `usgs_padus` feature has `source_release` equal to the release pinned in `land_classes.json`, a non-empty `source_paid`, and none of the not-kept fields of 6.2 | C |

R28 is amended, not weakened: its land clause is replaced by R79, which forbids every `private` value outside one source-backed case instead of allowing it on any `PVT` feature. R21 and R61 to R65 are otherwise unchanged.

## 14. Budgets and performance

Read from M3 (section 16 and amendment A10) and M4 (section 14); none is changed.

| Measure | Limit | Source |
|---|---|---|
| Bytes to "map usable", per region | 500,000 | M3 16.4, enforced by `test_display_budgets.py`, `region-loader.test.cjs`, browser B7 |
| Bytes with every default-on layer, per region | 4,500,000 | Same |
| Region default-on set | ≤ 15,000 features and ≤ 1,500,000 bytes gzipped | M3 16.5 |
| One display layer | ≤ 5,000 features and ≤ 450,000 bytes gzipped, or `min_zoom`, or split | M3 16.5 |
| Performance | Map usable ≤ 60% and all default-on layers ≤ 135% of the same-session base median; heap ≤ 115% of base; triggers R-1 to R-5 unchanged | M3 A10, A13 |

Land-specific limits proposed for M5 (M5-D15):

| Measure | Today | Limit |
|---|---|---|
| `land` display bytes after PR A | Aspen 172,001; Douglas 206,335 [REPO, file sizes at `c04f5d6`] | Reported. If either rises more than 10%, the extra display properties are left out of the display artifact (canonical only), as M4-A did |
| `land` display bytes after PR B | — | ≤ the PR A value. Removing the residual polygon is expected to reduce it by roughly the `PVT` polygon's share of vertices [V-audit] [INF] |
| `land_units` display bytes after PR C | Not measured; no geometry was downloaded [UNK] | ≤ 250,000 per region, provisional. The PR C spike measures it before any data is committed; over the limit, PR C stops and reports. No sliver or minimum-area rule is invented to fit without owner approval |
| Requests before "map usable" | — | No land unit or coverage file is requested before the map is usable. `land-coverage.json` is requested only when a land detail opens |

Three sessions of the unchanged `measure.mjs` are run at the PR B and PR C heads and reported, pass or miss. A miss is reported, not tuned around. Douglas's headroom to the map-usable budget was small during M4-A (504,430 before amendment A2 moved the alias map out) [REPO]; PR A reports the current figure.

## 15. Tests

Offline, clock-free, nothing written inside the repository, as in M3 and M4.

**Python (validator, build, fetch transforms):** a negative fixture for each of R77–R85; the tables of 8.1, including an unknown SMA code and an unknown PAD-US type; ID sanitising, an empty key and a collision (each stops the build); legacy matching by agency code and state, where a changed row number still matches and a changed code does not; a legacy ID equal to a current ID fails; the residual feature is in canonical data and absent from display; `excluded_by_class` counts; a feature with a `private` value outside the allowed case fails; a land feature carrying `pub_access`, `camping_permission` or `access_status` fails; the same unit ID in two fixture regions with one differing source field fails R82; a PAD-US fixture record keeps every field of 6.2 and none of the not-kept fields; a coverage record with category `access`, an empty summary, a 161-character summary, an ArcGIS `source_url`, a duplicate subject and category, or an unresolved `subject_id` each fails R83; `reviewed_partial` without a coverage record fails R84; freshness of a coverage record as a pure function with an injected time.

**Node:** the legend for `land` contains no `PVT` entry, contains LW1 before W5, and W5 is last; no legend text, detail line or title for any land feature contains the word "private" except within W5, LW1 and the manifest sentences of 11.3, each of which says the land is not found to be private; every LW, LL and OS string against its literal; W4 is no longer referenced; unit detail order of 11.4; LW7 and LW8 render for a unit with no record; LW6 with summary and link for a reviewed unit, and WW7 when past age; LW8 renders for every land unit, whatever its records.

**Browser check (both regions, the four sizes of M3):** land layers load within budget; at a Douglas point inside today's `PVT` polygon (for example Cheesman Lake's centroid, from canonical water data) no land tint is drawn and a tap opens no SMA land detail; at a point inside the USFS polygon the detail shows W11, the W8 label, W7 and W3; legend shows LW1 and W5 last; from PR C a tap at a point inside a displayed unit opens that unit's detail with LW3 and LW4; from PR D every land detail shows LW8.

**Mutation proofs (local, listed in the handoff):** put the `PVT` feature back into the Douglas display artifact (R80, and B-check fails); change one feature's `admin_agency_code` without recomputing `management_level` (R78); give a land feature `management_level: "private_recorded"` from the SMA (R79); add `pub_access: "OA"` to a unit (R79, R85); give two regions different `admin_unit_type` for `sma-co-usfs` (R82); add an `access` coverage record (R83); set `reviewed_partial` with an empty registry (R84); restore W4 in the legend (Node). Each must fail the named rule or test.

## 16. Delivery

Four small sequential pull requests on the two pilot regions only. Each is independently revertible, leaves `main` green, and needs the owner's approval of its exact head SHA before merge. No PR touches the loader, the adapter, Leaflet or any non-land layer's data. No PR adds a region or any statewide data.

### PR A — Land source preservation and one schema

In: the one controlled S1 refresh for both regions (5.3); the fields of 6.1; the identifier rule of 7.1 and `legacy_ids` of 7.3; `land_classes.json`; the Aspen layer renamed `land` in `region.json` and `explore.json`; removal of the unread vocabulary and constants; LL1 in both manifests; R77, R78, R79, R81, R82 and the R28 amendment; the snapshot and difference record `docs/research/m5-land/sma-snapshot.md`; contract documentation; display artifacts rebuilt.

Must not change: which land polygons are displayed, their geometry beyond the refresh's reported differences, their tints, their labels, any W string, any interaction, or any non-land canonical file (byte-identical, proven). The browser check's assertions pass unchanged except for land feature and layer IDs.

Reports: the saved-state and URL search of 7.3; the map-usable bytes per region; land display bytes before and after.

Gate before merge: the owner reads the difference report and approves LL1.

### PR B — The residual class reads as unknown

In: the display rule of 8.2; R80; `excluded_by_class` in the display index; register entry N19; the legend and detail changes of 11.1 for PR B; W4 retired; LW1; LL2; OS1 in both manifests; the Node and browser tests of section 15 for PR B; three performance sessions.

Must not change: canonical land data; any other layer; W1–W3 and W5–W11.

Gate before merge: the owner approves LW1, LL2 and OS1 as rendered, and does an iPhone check of both regions: the Douglas map reads as mostly unshaded without looking broken, the legend explains it, a tap on unshaded land opens no land sheet, and a tap on Forest Service land shows the unchanged sheet.

### PR C — Named land units (only if M5-D6 approves a unit source)

Step 1, a measured spike with no data committed, reported in `docs/research/m5-land/padus-spike.md`: features per region after clipping; display bytes and vertices; null names; `Source_PAID` presence, formats and uniqueness in both regions together; records that overlap one another inside a region, with area; the distribution of `src_date`; the units containing each region's displayed trails and recreation sites. PR C stops and reports if the budget of section 14 is exceeded, if any `Source_PAID` is missing or duplicated, or if overlapping records would make a tap ambiguous over a material area. The owner reads the spike before step 2.

Step 2: the one controlled S3 fetch; the `land_units` layer in both regions with the fields of 6.2; R85 and the PAD-US cases of R77, R78, R79 and R82; LW2–LW5; LL3; OS2; the detail of 11.4; budgets; three performance sessions.

If the owner chose S4 instead, PR C is re-specified for national-forest identity from S4 by amendment before it starts. If the owner declined both, PR C is not built.

Gate before merge: the owner approves LW2–LW5, LL3 and OS2 as rendered, and does an iPhone check of both regions.

### PR D — Land evidence coverage

In: `land-coverage.json` for both regions with the initial set of 9.2; the manifest `land_coverage` path; R83 and R84; LW6–LW8; OS3; `fact_coverage.ownership` `reviewed_partial` where a record exists; dossiers under `docs/research/m5-land/coverage/`, written by the coordinator (Hermes optional).

Gate before merge: the owner approves each record's summary and source in the pull request.

### Milestone close

M5 is complete when PR A, PR B and PR D are merged, and PR C too unless the owner declined every unit source under M5-D6. The coordinator then writes the product review of [product-scorecard.md](../product/product-scorecard.md) from a run of the [Douglas dirt-bike scenario](../product/acceptance-scenario-douglas-dirt-bike.md) by a dedicated tester who did not implement any M5 pull request, on a phone (section 21).

## 17. Rollback

- PR A: revert. The previous canonical land files, IDs and display artifacts return together because they are committed together; the snapshot record's pre-refresh SHA-256 values identify the state to return to. The Aspen layer ID returns to `land_ownership`.
- PR B: revert. The residual polygon is drawn again with W4, exactly as before; canonical data is untouched by PR B.
- PR C: revert, or remove the `land_units` layer from both manifests. The SMA layer is unaffected.
- PR D: revert, or empty `land-coverage.json`. Every unit then shows LW7 and LW8, and `fact_coverage.ownership` returns to `context`.
- A single wrong coverage record: delete it in a one-line change; the unit shows LW7. Always safe, because a management review grants nothing.
- A wrong class mapping: a one-line change to `land_classes.json` and a rebuild; R78 catches any drift.

## 18. Risks

Risk IDs use `RK` so they cannot be confused with validator rule IDs.

| ID | Risk | Mitigation |
|---|---|---|
| RK1 | A finer or named land layer looks more certain than it is, and a user reads a unit, a manager or a reviewed management line as permission. The central risk of the milestone | Every M5 layer `generalized`; LW4 and W7 on every detail; LW8 on every detail; no access field anywhere (R79); management reviews never mention access (9.1) |
| RK2 | A source access default (PAD-US `Pub_Access` "OA" from "GAP - Default") leaks into a label, filter or colour | Not retained (6.2, R79, R85); mutation proof |
| RK3 | Showing 71.8% of Douglas County as unshaded reads as a broken map or a regression | LW1 in the legend; owner's iPhone check in PR B; the product review reports it as a trust improvement, not hidden |
| RK4 | PAD-US local records are old (sampled Douglas rows dated 2010) and a unit may have changed [V-live] | LW5 shows the source's date; LL3 says records can be years old; never described as current |
| RK5 | PAD-US granularity is uneven: Pike National Forest is one 1,097,242-acre record beside small county properties [V-live] | "Unit" means "a record the source keeps", stated in 7.2; no merging or splitting |
| RK6 | `Source_PAID` or the SMA key is not persistent, so a coverage record detaches silently after a refresh | R82 and R83 fail on an unresolved subject; any later refresh needs a difference report and a legacy map, as M4 A4 requires |
| RK7 | The PR A refresh changes boundaries for reasons the source does not explain | Difference report; stop-and-report rule (5.3) |
| RK8 | Overlapping land layers make a tap select something the user did not intend | Unit layer above SMA; spike measures overlaps; the overlap chooser stays a recorded deferral; owner device check |
| RK9 | Sources disagree at edges (3.57 km² of Aspen wilderness on today's `PVT`; Forest Service trails crossing it) and the user infers private or allowed | After PR B that land is unshaded and unknown, so no contradiction is drawn; no relationship is inferred from crossing (section 10) |
| RK10 | Licence drift: unread PAD-US Explorer terms, unstated SMA and USFS terms, or restrictive CPW and county terms are assumed away | Section 5 quotes only; M5-D6 and M5-D17 are owner decisions; no source is used before its decision |
| RK11 | Byte or time budget missed, especially Douglas map-usable headroom | Section 14 limits; nothing land-related before map usable; report, never tune |
| RK12 | Manual review becomes a standing workload that grows with regions; reviews go overdue | Initial set capped at five per region; one-year default age (M5-D13); overdue shown, not hidden |
| RK13 | Hermes is unavailable, delaying dossiers | PR D depends on the coordinator's own reading; Hermes optional |
| RK14 | Research samples are five rows per source; they show that defaults and nulls exist, not how common they are [V-live] | PR A difference report and PR C spike measure the real records before anything is committed |

## 19. Unknowns

Stated as unknown. None blocks approval of this specification; each is resolved, or stopped on, inside the PR named.

- Whether the refreshed SMA layer still has exactly one row per agency per state, and whether its boundaries have changed since 2026-09-25 and 2026-09-27 (PR A).
- Whether any saved state, URL or configuration references a land feature ID or the layer ID `land_ownership` (PR A).
- The terms of use of the PAD-US Data Explorer, and whether they restrict republishing a clipped, reclassified subset (M5-D6; not read by anyone).
- Whether `Source_PAID` is unique within the pilot records and persistent across PAD-US releases (PR C spike for uniqueness; persistence stays unknown until a second release is compared).
- PAD-US feature counts, bytes, null names and overlaps after clipping to each region (PR C spike).
- Whether the BLM Colorado SMA `PRI` class is a residual like the national "Private or Unknown" class [E3].
- Whether the USFS Administrative Forest `ADMINFORESTID` is persistent (only if M5-D6 chooses S4).
- The State Land Board's official GIS publication and terms; CPW and county reuse terms (M5-D17).
- Douglas County's current headroom to the 500,000-byte map-usable budget (PR A reports it).
- How two overlapping land layers behave under a tap on an iPhone (PR C device check).
- Which units the PR D reviews will name, and whether each agency page agrees with the unit record (PR D).

## 20. Owner decisions requested

Every decision below is the owner's. The recommendation is the coordinator's proposal only; the bear case is the strongest argument against it.

| ID | Decision | Options | Recommendation | Bear case against the recommendation |
|---|---|---|---|---|
| M5-D1 | Scope and delivery | (a) Four PRs A–D on Aspen and Douglas only, with "no renderer change" read as no change to the loader, adapter, Leaflet or ADR-006 while `land-style.js`, manifests and `explore.json` change; (b) the same without PR C; (c) one combined PR | (a) | Four gates and four device checks for a milestone whose main user-visible change is in PR B; the owner may prefer to ship PR B's fix sooner and alone |
| M5-D2 | How the SMA residual class (`PVT`, "Private or Unknown") is shown | (a) Kept in canonical data, not displayed, not selectable; LW1 explains; (b) displayed with no fill, selectable, with its own detail sheet; (c) today's tint with a new label | (a) | Users lose any way to tap "why is this blank?" and learn the source's class; under (a) a tap gives nothing, and a careful user might want the source's own words |
| M5-D3 | Classification vocabulary | (a) The `management_level` values and both tables of 8.1, with SMA `PVT` → `none_recorded` and `private_recorded` only from PAD-US `mang_type` `PVT`; (b) no derived vocabulary, source codes only; (c) a coarser federal / non-federal / unknown split | (a) | A derived vocabulary is one more mapping to keep right; `tribal`, `joint` and `special_district` exist for completeness without pilot data to test them; "non-federal" in (c) invites the very inference the roadmap forbids |
| M5-D4 | Management background source | (a) Keep BLM National SMA (S1); (b) switch to BLM Colorado SMA (S2), public domain by its metadata, finer, no unit names; (c) both | (a) for M5, with S2 recorded as a candidate | S1's geometry is coarse (105–190 m per vertex, 127 of 142 Aspen USFS parts under 1 ha) [V-audit]; S2 has a clearer public-domain statement than S1, which states no licence at all |
| M5-D5 | Live refresh | (a) One controlled refresh of S1 in PR A with a snapshot and difference record; (b) no refresh, keeping today's two fields | (a) | Every other attribute is lost without a refresh; but a refresh may change boundaries with no source explanation and widen PR A |
| M5-D6 | Named-unit source, including the licence reading | (a) PAD-US 4.1 fee layer (S3), after the owner reads and accepts the Data Explorer terms; (b) USFS Administrative Forest (S4), national forests only; (c) none in M5 | (a), conditional on the owner's reading; (b) if the terms are not acceptable or cannot be found | The PAD-US terms are unread by anyone; many records originate with states, counties and land trusts whose own terms the item does not say are extinguished; records can be 15 years old |
| M5-D7 | Ownership dimension, and privately managed units | (a) Retain PAD-US `own_type` canonically, not displayed; do not retain `Own_Name`; keep `private_recorded` units canonical and undisplayed; (b) also display owner type, and display `private_recorded` units with the source's label; (c) retain nothing about ownership | (a) | Keeping an undisplayed field invites a later consumer to show it without review; hiding reported private conservation land removes a true source record from the map and leaves it unshaded, which a user may read as "nothing here" |
| M5-D8 | Source access attributes (`Pub_Access`, `Access_Src`, `Access_Dt` and county equivalents) | (a) Not retained anywhere; (b) retained canonically, never displayed or branched on | (a) | The attribute is a real source fact, and a later access milestone may want to compare it against reviewed records; it would have to be re-fetched |
| M5-D9 | Spatial precision claims | (a) Every M5 layer `generalized`; tier A stays undefined and unused; (b) PAD-US declared `source_published` (tier P, solid outline) | (a) | PAD-US boundaries are often finer than the SMA's; drawing them as generalized understates them and makes the two land layers look alike |
| M5-D10 | Identifier scheme | (a) `sma-<state>-<agency>` and `padus-<Source_PAID>`, no row numbers, no region ID, `legacy_ids`, no alias file unless a reference is found; (b) keep row-number IDs | (a) | `sma-co-usfs` names a statewide aggregate, so it is identity in form but not a place; the scheme's value rests on `Source_PAID`, whose persistence is unknown |
| M5-D11 | Layer rename and vocabulary removal | (a) Rename Aspen `land_ownership` to `land`; remove Aspen's derived `manager`, `land_class`, `camping_permission` and Douglas's `name`; (b) keep IDs and properties for compatibility | (a) | A rename can break an unknown external reference or bookmark; the audit found no reader, but absence of a reader is not proof |
| M5-D12 | Land freshness policy | (a) One value for both regions, 8,760 hours (one year), applied as retrieval age; (b) keep `null` in Aspen and 168 in Douglas; (c) 2,160 hours | (a) | The same source is "refresh needed" forever in Douglas today and never in Aspen; a year is long for a source BLM calls a dynamic assembly, and a changed boundary could sit unflagged for months |
| M5-D13 | Coverage model | (a) Categories `management` and `access`; only `management` records accepted in M5; `summary` field; 8,760-hour default age; at most five units per region; (b) also accept `access` records, restriction-first, populated later; (c) no coverage in M5 | (a) | "Management: reviewed" next to a forest name may still be read as "this place checks out"; the one category users care about, access, stays empty |
| M5-D14 | Every new or retired user-visible string | Approve, edit or reject each of LW1–LW8, LL1–LL3, OS1–OS3 and the retirement of W4 (11.2, 11.3) | Approve as drafted | Fourteen new strings is more wording surface than M3's W set; LW1 is long for a legend line on a phone |
| M5-D15 | Land budgets | (a) The limits of section 14, including 250,000 bytes per region for `land_units`, provisional until the spike; (b) set after the spike only | (a) | A provisional number may anchor the decision before anything is measured |
| M5-D16 | What completes M5 | (a) PR A, PR B and PR D, plus PR C unless every unit source is declined; (b) PR A and PR B only | (a) | Without PR C, PR D's reviews attach to statewide agency aggregates, which adds little for a user |
| M5-D17 | State and local sources (State Land Board, CPW, county open space) | (a) Excluded from M5 until each publisher's terms are established in writing; (b) admit any whose service carries no restrictive text | (a) | State trust land, state wildlife areas and county open space are where "can I be here" answers differ most [H]; leaving them out leaves Douglas's state and local land as two small generalized classes |

Any change to the trust principles, the contract's normative rules or `ROADMAP.md` is outside this list and would need its own approved pull request.

## 21. Acceptance criteria

PR A:
1. Offline Python and Node suites and the browser check pass; display rebuild has no diff.
2. Snapshot and difference record committed; every unexplained difference resolved or reported.
3. Every non-land canonical file is byte-identical to `c04f5d6`.
4. The displayed land polygons, tints and labels are unchanged apart from IDs, properties and reported refresh differences.
5. R77, R78, R79, R81, R82 pass on real data with negative tests and mutation proofs.

PR B:
6. R80 passes with negative tests and mutation proofs; no `none_recorded` feature is in any display artifact.
7. No legend entry, detail line, title or label for any land feature contains the word "private" except inside W5, LW1 and the manifest sentences of 11.3, each of which says the land is not found to be private.
8. LW1, LL2 and OS1 match their literals; W4 is not rendered anywhere.
9. Byte budgets hold; three performance sessions reported.
10. The owner's iPhone check of both regions passes.

PR C (if built):
11. Spike report committed and read by the owner before data is committed.
12. R85 and the PAD-US cases of R77–R79 and R82 pass with negative tests and mutation proofs.
13. No access attribute exists in canonical or display data.
14. LW2–LW5, LL3 and OS2 match their literals; the unit layer is within its budget; three performance sessions reported; the owner's iPhone check passes.

PR D:
15. R83 and R84 pass with negative tests and mutation proofs.
16. Every coverage record cites the managing agency's own page, read by the coordinator, and is approved by the owner in the pull request.
17. Every land detail shows LW8; a unit with no record shows LW7.

Milestone (from [product-scorecard.md](../product/product-scorecard.md)):
18. A dedicated tester who did not implement any M5 pull request runs the Douglas dirt-bike scenario on a phone, recording every measure against the previous result.
19. The coordinator writes the product review under its six headings. It states plainly that M5 is mostly foundation. Predictions to be tested, not results: step 8 ("where each fact came from") improves for land; step 9 ("what remains unknown") improves, because land the source does not attribute is now shown as unknown and access is listed as not reviewed; "Evidence coverage shown" gains land categories (management reviewed or not, access not reviewed); time to a viable trip, planning steps and external sites are not expected to improve, and access and camping questions still send the tester elsewhere; the count of proximity assumptions is expected to be unchanged, and any rise caused by land presentation is a regression.
20. No scorecard line is improved by hiding an unknown. Fewer apparent unknowns reached by not showing them fails the review.

All: no access, permission or camping claim; no parcel or owner name; no source used before its owner decision; no change to the loader, adapter, Leaflet or any non-land layer; no merge without the owner's approval of the specific pull request and head SHA.

## Appendix A. Evidence basis

| Fact | Basis | Where |
|---|---|---|
| Feature counts, area shares, tiling, vertex spacing, wilderness and trail overlaps, schemas | [V-audit] | `current-land-audit.md` sections 1–6 (on `docs/research-drafts`) |
| National SMA aggregates (`OBJECTID` 413 is USFS for all Colorado; `ADMIN_UNIT_NAME` null); SMA's ownership disclaimer; BLM Colorado public-domain statement; PAD-US unit names, `Source_PAID` sample, default `Pub_Access`; USFS, county, OIT and CPW terms text | [V-live] | `M5-preliminary-research-gate.md` sections 2, 3, 5 and appendix A |
| "Private or Unknown" sublayer; its Colorado row is `PVT`; `OBJECTID` differs between layers | [E1] [E2] | [m5-spec-evidence.md](../research/m5-land/m5-spec-evidence.md) |
| BLM Colorado SMA class labels, including `PRI` "Private" | [E3] | Same |
| PAD-US 4.1 citation text, `Source_PAID` field, coded domains for `Pub_Access`, `Own_Type`, `Mang_Type` | [E4] | Same |
| State Land Board, COMaP, county policy, CPW programme statements, USFS Administrative Forest fields | [H] | `hermes/m5-land-source-matrix.md`, `source-watchlist-m5-m8.md` |
| Contract rules, W strings, tiers, budgets, M4 precedents | [REPO] | `data-contract.md`, M3 section 13 and A10, M4 sections 7, 9, 14 |
| Display file sizes 172,001 and 206,335 bytes | [REPO] | `v2/regions/*/display/` at `c04f5d6` |
