# M5 preliminary research gate — land

Prepared 2026-10-07 for the owner. This is preparation only: it decides
nothing, implements nothing and does not change `ROADMAP.md`. Recommendations
are offered so the owner has something to accept or reject.

Inputs: `current-land-audit.md` (measured from the repository),
`hermes/m5-land-source-matrix.md` and
`../future-sources/source-watchlist-m5-m8.md` (Hermes web research), the
roadmap, trust principles, data contract and M4 specification in the
`m4a-source-preservation` worktree, and 25 read-only metadata requests made
for this document (appendix A).

Basis marks used throughout:

| Mark | Meaning |
|---|---|
| **[V-live]** | VERIFIED BY AGENT: read from a publisher's service in this session; the saved response is named in appendix A |
| **[V-audit]** | VERIFIED BY AGENT: measured from repository files in `current-land-audit.md` |
| **[REPO]** | Read from a normative repository document |
| **[H]** | HERMES-SOURCED: stated by the Hermes report, not re-checked |
| **[INF]** | Inference by this agent from the marked facts |
| **[UNK]** | UNKNOWN: not established by anything read |

## 1. Summary

Today's land layer is one polygon per agency per state. The source's own
name for the `PVT` class is "Private or Unknown", it covers 72% of Douglas
County, and the map never shows unknown land. [V-live] [V-audit]

No dataset checked can say what a person may do on a piece of land. Where an
access attribute exists it is a default: five of five PAD-US rows sampled
carry `Pub_Access` "OA" with source "GAP - Default". [V-live]

A finer source exists and is public domain by its own metadata (BLM Colorado
SMA), but it still names no unit: its `SMA_ID` is an agency class code, and
`adm_name` was empty in all five rows sampled. [V-live] PAD-US 4.1 does name
units (Pike National Forest, Chatfield Recreation Area, Hidden Mesa) and has
a live service Hermes could not reach. [V-live]

Parcels carry owner names and addresses and restrictive or absent terms.
[V-live] [H]

The main decisions are: what the tappable unit is; what to do with the
residual "private or unknown" class; whether any access attribute is ever
shown; and whether reviewed access statements belong in M5 or later.

## 2. Current-data deficiencies

Ranked by effect on a user's trust. Evidence is in the audit unless marked.
Classes: DATA GAP, TRUST ISSUE, OWNER DECISION, IMPLEMENTATION DETAIL, FUTURE
TECH DEBT. "L" numbers are the audit's.

| Rank | Deficiency | Evidence | Class |
|---|---|---|---|
| 1 | The residual class is published as private. `PVT` is 71.8% of Douglas County and 13.1% of Aspen; 12 of 14 named Douglas waterbodies over 5 ha lie wholly inside it (L2). The source service names this class "Private or Unknown" (layers 16 and 31) and lists `unknown` among its keywords. The app labels it "the source's generalized private class". Contract rule 11 allows a private classification "only where the source itself classifies land as private". | [V-audit] [V-live] [REPO] | TRUST ISSUE |
| 2 | Unknown never appears. Polygons cover 100.00% of both extents, so the approved legend line "Unshaded land is unknown" (W5) applies to 1 m² and 40 m² (L3). | [V-audit] | TRUST ISSUE |
| 3 | One aggregate per agency; no place identity (L1). Confirmed at source: OBJECTID 413 is USFS for all Colorado (96,884 km² of shape area), 1069 is `PVT` for all Colorado; `ADMIN_UNIT_NAME` is null on the USFS, `OTHFE`, `ST` and `PVT` rows. The audit's inference that the layer is dissolved by agency and state is now verified. | [V-audit] [V-live] | DATA GAP |
| 4 | No access or permission dimension, and none available from this source (L4). | [V-audit] | DATA GAP |
| 5 | Forest Service trails and roads cross `PVT` (11.1 km and 1.0 km in Aspen; 1.4 km and 1.7 km in Douglas) with no way to tell an easement from a drawing error (L11). | [V-audit] | TRUST ISSUE |
| 6 | Coarse, noisy boundaries: 105–190 m per vertex, 400 m segments, 127 of 142 Aspen USFS parts under 1 ha (L7). | [V-audit] | TRUST ISSUE (held by W7 wording today) |
| 7 | State and local land is tiny and undifferentiated (`ST` 0.51%, `LG` 0.87% of Douglas; none in Aspen) (L5). | [V-audit] | DATA GAP |
| 8 | "Other Federal" names no agency (L6). PAD-US names the same place: manager `USACE`, unit "Chatfield Recreation Area", owner `UNK`. | [V-audit] [V-live] | DATA GAP |
| 9 | Wilderness has no name (L8) and 3.57 km² of it lies on `PVT` (L9). The Forest Service wilderness layer does carry `areaname` and `areaid`. | [V-audit] [V-live] | DATA GAP / TRUST ISSUE |
| 10 | An empty Douglas wilderness layer cannot be told from "no wilderness" (L10). | [V-audit] | TRUST ISSUE |
| 11 | No stable identifier and no source attributes kept (L15). The national `SMA_ID` is not a feature identifier either: it is 2 for BLM in both the national and the Colorado service. | [V-audit] [V-live] | DATA GAP |
| 12 | Vocabulary says ownership; the source says management (L17). The source states it does "not illustrate land status ownership pattern boundaries or contain land ownership attribute details". | [V-audit] [V-live] | OWNER DECISION |
| 13 | Tier A ("authoritative classification") is reserved and undefined (L18). | [V-audit] | OWNER DECISION |
| 14 | Freshness policy differs for one source: `null` in Aspen, 168 h in Douglas (L16). | [V-audit] | OWNER DECISION |
| 15 | Two schemas for one source (L12). | [V-audit] | IMPLEMENTATION DETAIL |
| 16 | False coordinate precision, 14–15 decimals (L19). | [V-audit] | IMPLEMENTATION DETAIL |
| 17 | Aspen publishes an unread derived `manager: "Private"` (L13). | [V-audit] | FUTURE TECH DEBT |
| 18 | `NPS` and `FWS` would display as "unrecognised" (L14). | [V-audit] | FUTURE TECH DEBT |

Rank 1 is new in its force. The audit showed that `PVT` behaves as a
residual; the service itself confirms that the publisher calls it "Private or
Unknown". The current label is narrower than the source's.

## 3. Source matrix

"Mark" is the evidence mark for the row as a whole. A blank licence field is
recorded as "none stated", which is not permission.

### 3.1 Checked in this session

| # | Source and publisher | What it contains | Real fields | Scale or accuracy | Stable unit-level id | Licence or use text (quoted) | Cadence | Does NOT establish | Mark |
|---|---|---|---|---|---|---|---|---|---|
| S1 | **BLM National SMA, limited scale** (`gis.blm.gov/arcgis/.../BLM_Natl_SMA_LimitedScale/MapServer/1`). In use today. | One multipolygon per agency per state. Display classes include "Private or Unknown". | `OBJECTID`, `SMA_ID`, `ADMIN_DEPT_CODE`, `ADMIN_AGENCY_CODE`, `ADMIN_UNIT_NAME`, `ADMIN_UNIT_TYPE`, `HOLD_ID`, `HOLD_DEPT_CODE`, `HOLD_AGENCY_CODE`, `ADMIN_ST`, `FAU_ID`, shape fields | Service draws only when zoomed in past 1:36,118 (`minScale`). No accuracy stated. | **No.** `SMA_ID` is a class code (BLM = 2). `OBJECTID` identifies "an agency in Colorado". | Copyright text only: "Bureau of Land Management, (BLM)". No licence stated. | "dynamic assembly"; no interval stated | Ownership ("do not illustrate land status ownership pattern boundaries"), unit, access, any activity | VERIFIED BY AGENT |
| S2 | **BLM Colorado SMA** (`gis.blm.gov/coarcgis/.../BLM_Colorado_Surface_Management_Agency/FeatureServer/1`) | Many polygons per class: 260 intersect the Aspen box, 119 the Douglas box. Classes `BLM`, `BOR`, `BIA`, `DOD`, `USFS`, `USFS_NG`, `NPS`, `USFW`, `OTHER`, `STA`, `LOCAL`, `PRI`, `BLM_LU`, `USFS_LU`. `LOCAL` is labelled "State, County, City: Recreation Areas". | `OBJECTID`, `adm_code`, `adm_manage`, `adm_name`, `GIS_acres`, `SMA_ID`, `GlobalID`, shape fields | "small scale (1:24,000 and smaller)"; sources "ranging from GCDB to 24K to 100K"; "both scale and accuracy may vary across the data set" | **Partly.** `GlobalID` per polygon exists; whether it survives edits is UNK. `SMA_ID` is a class code (2 = BLM, 2387 = LOCAL). `adm_name` null in 5 of 5 sampled rows, so no unit name. | ISO metadata: "None, these data are considered public domain." Also: "The BLM should be cited as the data source in any products derived from these data. Any Users wishing to modify the data should describe the types of modifications they have performed." and "neither legal documents nor land surveys". | Text says "subject to update daily"; the same record's maintenance code says `quarterly` and `irregular` | Ownership, unit identity, access, any activity. Whether `PRI` is also a residual is UNK. | VERIFIED BY AGENT |
| S3 | **USGS PAD-US 4.1, fee layer** (`services.arcgis.com/v01gqwM5QqNysAAi/.../Fee_Managers_PADUS/FeatureServer/0`, layer name `PADUS4_1FeeManagers`) | Named protected-area records: 487 intersect the Douglas box, 91 the Aspen box. Only land someone has reported; everything else has no record. | `FeatClass`, `Category`, `Own_Type`, `Own_Name`, `Loc_Own`, `Mang_Type`, `Mang_Name`, `Loc_Mang`, `Des_Tp`, `Loc_Ds`, `Unit_Nm`, `Loc_Nm`, `State_Nm`, `Agg_Src`, `GIS_Src`, `Src_Date`, `GIS_Acres`, `Source_PAID`, `WDPA_Cd`, `Pub_Access`, `Access_Src`, `Access_Dt`, `GAP_Sts`, `IUCN_Cat`, `Date_Est`, `EsmtHldr`, `EHoldTyp`, plus source and date fields for each | None stated in the service. Per-record `GIS_Src` and `Src_Date` vary: sampled rows range from 2010 to 2024. | **Candidate.** `Source_PAID` exists and is populated in 5 of 5 rows, in three formats (`G603020`, a 32-character hex value, `10032675`). Stability across releases and uniqueness are UNK. | Item text: "This content describes the PAD-US dataset which is in the public domain." Followed by: "Users are obligated to follow the terms of use of the PAD-US Data Explorer and any accompanying content." Licence field is a no-warranty statement. Citation in `copyrightText` with DOI 10.5066/P96WBCHS. | Versioned: 4.0 April 2024, 4.1 March 2025; ten releases since 2009. Service data last edited 2025-06-04. | Access or any activity. `Pub_Access` was "OA" from "GAP - Default" in 5 of 5 rows. Granularity varies: Pike National Forest is one 1,097,242-acre record. | VERIFIED BY AGENT |
| S4 | **USFS Basic Ownership** (`apps.fs.usda.gov/arcx/.../EDW_BasicOwnership_01/MapServer/0`) | Forest Service or non-Forest-Service land inside forest boundaries, merged by class | `ownerclassification`, `region`, `forestname`, `objectid`, shape fields. Values: `USDA FOREST SERVICE`, `NON-FS`, `UNPARTITIONED RIPARIAN INTEREST` | Draws only past 1:3,000,000. "appropriate for general mapping and analysis" | **No** id on the service beyond `objectid`. `forestname` gives the forest. | "This dataset is intended for read-only use." No licence or copyright text on the layer. | Not stated on the layer; weekly per Hermes [H] | Who owns `NON-FS` land; access; any activity | VERIFIED BY AGENT |
| S5 | **USFS Surface Ownership** (`.../EDW_SurfaceOwnership_01/MapServer/0`) | Ownership by land transaction | `surfaceownershipid`, `casename`, `localcaseid`, `ownerclassification`, `statusmethod`, `status`, `recordedacres`, `gis_acres`, `actiondate`, `nfs_landunit_fk`, `landstatuscaseid`, `nfslandunitname`, and tax and payment fields | Draws only past 1:3,000,000. "detailed information suitable for advanced mapping" | **Yes in form**: `surfaceownershipid` (40-character string). Persistence UNK. It identifies a transaction, not a place a user knows. | "intended for read-only use". No licence or copyright text on the layer. | Not stated on the layer | Access; any activity; legal boundary | VERIFIED BY AGENT |
| S6 | **USFS Wilderness: Legal Status** (`.../EDW_WildernessStatus_01/MapServer/0`) | Wilderness polygons, split by legal action | `wildernessstatusid`, `casename`, `areatype`, `areaname`, `areaid`, `boundarystatus`, `actiondate`, `officialacres`, `gis_acres`, `wilderness_fk`, `region` | Not stated | **Candidate**: `areaid` (6 characters) and `wilderness_fk` for the area; `wildernessstatusid` for the part | "intended for read-only use". No licence text. The description says a separate "Wilderness dataset" has whole-area boundaries; that layer was not checked. | Not stated | Current rules in a wilderness; access | VERIFIED BY AGENT |
| S7 | **Pitkin County Open Spaces** (`maps.pitkincounty.com/.../Hosted/Open_Spaces/MapServer/101`) | Named open space, parks, preserves, golf courses | 39 fields including `name`, `type`, `ownership`, `owner_type`, `maintainer`, `restriction`, `closure`, `closedondate`, `openondate`, `recreation`, `manageplan`, `planningarea`, `globalid`, `last_edited_date` | Not stated | **Yes in form**: `globalid`. Persistence UNK. | Copyright text only: "Pitkin County Open Space and Trails, City of Aspen Parks Department". No licence stated. | Not stated; `last_edited_date` per row | That the public may enter or do anything. The `restriction` and `closure` values were not read. | VERIFIED BY AGENT |
| S8 | **Pitkin County parcels** (`.../Hosted/Parcel_Boundary/MapServer/0`) | Assessor parcels | 60-plus fields including `parcel`, `pin`, `accountnumber`, `globalid`, **`owner_name`, `owner_address1`, `owner_address2`, `owner_city`, `owner_state`, `owner_zip`**, `legal`, `situs_address`, sale and valuation fields | Not stated | `parcel`, `pin`, `globalid` | Copyright "Pitkin County". Disclaimer only: joined "for purposes of Pitkin County Government use"; changes can take "up to sixty days". No licence stated. | Up to 60 days behind recordation | Access; a surveyed line; current title | VERIFIED BY AGENT |
| S9 | **Douglas County `OPEN_SPACE`** (`apps.douglas.co.us/gisod/.../Landuse/FeatureServer/5`) | County open-space polygons | `SITE`, `CATEGORY`, `PUB_ACCESS`, `FUNDS_USED`, `MPCODE`, `DEEDED_ACRES`, `COMMENTS`, `GLOBALID`, `created_date`, `last_edited_date` | Not stated | **Yes in form**: `GLOBALID` | **None stated.** Description and copyright fields are empty on the layer and the service. Hermes reports a county policy that data "may be subject to a separate contract or leasing agreement" [H]. | Not stated; edit dates per row | Access. What `PUB_ACCESS` values mean was not read. | VERIFIED BY AGENT (schema); licence UNKNOWN |
| S10 | **Colorado Public Parcels, OIT** (`gis.colorado.gov/public/.../Colorado_Public_Parcels/FeatureServer`) | Statewide parcel composite | Layer 0 `Colorado_Public_Parcel_Composite` confirmed. Field list (`owner`, `ownerAdd`, `parcel_id`, …) is from Hermes [H]. | Not checked | `parcel_id`, `account` [H] | "Resale of this data is strictly forbidden. Commercial use of the data is allowed so long as the State of Colorado is attributed in relevant application documentation." Attribution sentence given. | "Updates are collected annually" | Access; current county record; title | VERIFIED BY AGENT (terms); fields HERMES-SOURCED |
| S11 | **CPW `CPWAdminData`** (`services5.arcgis.com/ttNGmDvKQA7oeDQ3/.../CPWAdminData/FeatureServer`) | 30 layers including "CPW Managed Properties (public access only)" (5), "CPW Walk In Access Program" (12), "CPW Fee Title Parcels" (29), "COTREX Trails" (15) | Layer list only. Layer fields not read. | Not checked | UNK | Item text: "This map is a product and property of the Colorado Parks and Wildlife … Data or information provided by the Department of Natural Resources shall be used and relied upon only at the user's sole risk, and the user agrees to indemnify and hold harmless the Department". Service description: "for public distribution". No redistribution grant. | Service generated 2026-08-27; annual schedule per Hermes [H] | Which activities a property allows; that a Walk-In Access polygon is posted or in season | VERIFIED BY AGENT (existence, terms text); fields UNKNOWN |

### 3.2 Not re-checked

| # | Source | What Hermes reports | Mark |
|---|---|---|---|
| S12 | Colorado State Land Board trust land | Map application only; no schema, licence or id found. Trust land "is not open to the public" without a lease or programme. An ArcGIS search in this session found public items titled "Colorado State Land Board Surface Ownership" and several `SLB_*` services, all with an empty licence field and none confirmed as the Board's official publication. [V-live] for the search result only. | HERMES-SOURCED; publisher and terms UNKNOWN |
| S13 | COMaP (CSU / CNHP) | Owner, manager, easement holder, `PUBLIC_ACCESS`. "Under no circumstances are data to be REDISTRIBUTED." Paid subscription. | HERMES-SOURCED |
| S14 | USFS Administrative Forest | `ADMINFORESTID`, `FORESTNAME`. Boundary can include private land. | HERMES-SOURCED |
| S15 | Pitkin Open Space Easement | Includes a `public_access` field and `globalid`. | HERMES-SOURCED |
| S16 | Douglas County parcels and conservation easements | Layers `PARCELS`, `CONSERVATION_EASEMENTS`; assessor ids. | HERMES-SOURCED |
| S17 | BLM Public Lands Access Data (PLAD) | Easements and reserved access to BLM land; does "not allow for use of the non-BLM lands crossed". Schema not retrieved. | HERMES-SOURCED |
| S18 | Regrid, ReportAll, LightBox, CoreLogic | Commercial parcels. Regrid's store licence prohibits "making the Data available to third parties". Others unread. | HERMES-SOURCED |
| S19 | PAD-US designation, easement and proclamation layers | Other PAD-US services exist (`Manager_Name_PADUS`, `Proclamation_and_Other_Planning_Boundaries_PADUS`, `PADUS_Designation_Manager_Types`); schemas not read. [V-live] for existence. | UNKNOWN |

### 3.3 Disagreements with Hermes

| # | Hermes said | Found | Effect |
|---|---|---|---|
| D1 | PAD-US ArcGIS endpoint unavailable; no polygon identifier established. | A live PAD-US 4.1 fee service exists and carries `Source_PAID`. | PAD-US is usable as a unit source; id stability still to test. |
| D2 | National `SMA_ID` "exists", stability unknown. | `SMA_ID` is an agency class code, identical for BLM in the national and Colorado services. It cannot identify a feature. | Neither SMA service offers a unit identifier. Only Colorado's `GlobalID` identifies a polygon. |
| D3 | USFS Basic Ownership has `BASICOWNERSHIPID` and `GIS_ACRES`. | The live service layer has neither: `ownerclassification`, `region`, `forestname`, `objectid` only. Hermes read the download metadata; the download may differ. | No stable id from that service. |
| D4 | USFS field `NFS_LANDUNIT_FKA`. | Real field `nfs_landunit_fk`; all service fields are lower case. | Minor. |
| D5 | Pitkin Open Spaces exposes `type`, `name`, `planningarea`. | 39 fields, including `restriction`, `closure`, `closedondate`, `openondate`, `maintainer`, `globalid`. | The county layer is richer than reported; the access-like fields raise the same risk as `Pub_Access`. |
| D6 | USFS wilderness schema not retrieved; id unknown. | Schema retrieved; `areaname`, `areaid`, `wilderness_fk` exist. | Wilderness can be named. |
| D7 | CPW schema and licence unknown. | Service and 30-layer list found, with CPW's "product and property" and indemnity text. | Existence settled; permission to republish is not. |
| D8 | BLM Colorado public-domain statement cited from data.gov. | Confirmed in BLM's own ISO record, with a request to cite BLM and describe modifications. The same record gives the cadence as `quarterly` and `irregular` beside the "daily" note. | Licence stronger than reported; cadence less certain. |
| D9 | Recommends exposing `Pub_Access` as a "generalized access category". | Five of five sampled rows are a default, not a review. | This document recommends against showing it at all (decision 6). |
| D10 | National SMA has a "Private or Unknown" display class (noted, not connected to the product). | Confirmed, and it is the class the product publishes as `PVT`. | Deficiency rank 1. |

## 4. Ownership versus management versus access

### 4.1 Three questions, three kinds of source

| Question | What can answer it | What cannot |
|---|---|---|
| Who manages the surface here? | SMA (S1, S2); PAD-US `Mang_Name`, `Loc_Mang` (S3) | — |
| Who owns it? | Ownership records: USFS Surface Ownership for Forest Service land (S5); county parcels (S8, S16); PAD-US `Own_Name` where filled | SMA. The publisher says so. [V-live] |
| May the public enter, and to do what? | Only a statement by the manager or operator about that place and that activity: a rule page, an order, a lease, a posted sign | Every dataset in section 3, including the ones with an access field |

One sampled record shows all three apart: PAD-US lists Chatfield with
manager `USACE`, owner `UNK` and access "OA" by default. [V-live] The same
ground is `OTHFE` in the national SMA. [V-audit] None of the three says who
runs recreation there or what its rules are.

### 4.2 How the product must keep them apart

1. One layer kind, `land_management`. The contract already has no `ownership`
   kind. [REPO] Owner and designation, where published, are source facts on a
   record, each with its own provenance.
2. No field, colour, label, ordering or filter on a land feature expresses
   access or permission. Contract rule 12 and trust principle 2 already
   forbid inferring public access from ownership or managing agency. [REPO]
3. A source's access attribute (`Pub_Access`, Douglas `PUB_ACCESS`, Pitkin
   `public_access`, `restriction`, `closure`) is a source fact about what a
   database says. It is never an Ohvernight access value, and section 8
   recommends it is not displayed.
4. Access and activity statements, if M5 has any, live in a separate
   reviewed registry keyed to a land unit, as M4 does for water. [REPO] The
   M4 rule carries over unchanged: a map layer, a designation dataset and a
   facility dataset are forbidden sources for a claim.
5. Camping is not an M5 subject. The roadmap gives it to M7. [REPO]

### 4.3 What can honestly be said about private land

- Nothing in use today establishes that any spot is private. The current
  source class is "Private or Unknown". [V-live]
- An honest sentence available now is: "The source records no public managing
  agency here. That is not a finding that the land is private, and not a
  finding about access." [INF]
- Only a parcel or ownership record can support "a source records a private
  owner here", and then only as that source's record on its date, not as a
  boundary and not as "keep out". Contract rule 12: a private classification
  "does not itself establish access is prohibited". [REPO]
- PAD-US records some private conservation land (`Mang_Name` `PVT`, `NGO`).
  [V-live] That is a record of a protected holding, not of access.

### 4.4 What can honestly be said about land with no record

Today it cannot arise: every square metre of both extents is assigned an
agency code, and `PVT` is the residual, so "unknown" is never drawn.
[V-audit] The trust principles say an empty or missing layer means unknown.
[REPO] Three consequences:

- If the residual class stays a tinted class, the product keeps saying
  something about 72% of Douglas County that its source does not say. [INF]
- If a unit source such as PAD-US becomes the land feature, most of Douglas
  County will have no record. That is the first time "no record" would be
  visible, and it needs its own wording: "No land record in the sources
  loaded. Not private, not public, not open." [INF]
- "No record" in a source that only lists reported protected areas must not
  be reworded as "unprotected" or "private". [INF]

## 5. Licensing concerns

| Source | Position | Basis |
|---|---|---|
| BLM Colorado SMA | Public domain by its own metadata; cite BLM; describe modifications; do not imply BLM endorsed changes. Clipping, simplifying and reclassifying are modifications and would need a stated note. | [V-live]; last clause [INF] |
| BLM National SMA | No licence text on the service. Already published by the site. US federal works are generally uncopyrightable, but the service does not say so. | [V-live]; [INF] |
| PAD-US 4.1 | "in the public domain", then "obligated to follow the terms of use of the PAD-US Data Explorer". Those terms were not read. Many records originate from states, counties and land trusts; the item does not say their terms are extinguished. | [V-live]; [UNK] |
| USFS services | "read-only use"; no licence text on any layer checked. | [V-live] |
| CPW | "product and property" of CPW with an indemnity clause; "for public distribution" in the service description. No grant to republish a derived copy. | [V-live] |
| Pitkin, Douglas open space | No licence stated. Douglas policy may require an agreement. | [V-live]; [H] |
| State Land Board | Publisher's official service and terms not identified. | [UNK] |
| COMaP | Redistribution prohibited. Not usable in a public repository. | [H] |

**Parcels.** Four separate problems, any one of which is enough to stop:

1. **Terms.** OIT forbids "resale" and requires attribution. [V-live]
   Whether a free public site that republishes parcel geometry is acceptable,
   and whether a future paid feature would be "resale", is not answered by
   the text. [UNK] County terms sit underneath the state composite and differ
   by county. [H] Regrid's standard licence forbids making data available to
   third parties. [H]
2. **Personal data.** Pitkin's parcel layer carries owner names and mailing
   addresses. [V-live] The agent guide forbids raw personal contact details
   in published data. [REPO] Any parcel use would have to drop every owner
   field before anything is written to the repository.
3. **A static site republishes whatever it loads.** A GeoJSON file on GitHub
   Pages is a full copy anyone can download. A "display only" licence cannot
   be honoured. [INF]
4. **False precision.** Parcel lines look like property lines. Pitkin says
   its linework is approximate and not a surveyed record. [H] Trust principle
   7 forbids drawing generalized geometry as parcel-level or legally precise.
   [REPO]

A blank licence field, a public endpoint or an "open data" portal is not
permission. [INF]

## 6. Likely architecture

Costs are against today's land files: 172,001 bytes for Aspen and 206,335
for Douglas, one request each. [V-audit, file sizes read from the display
directories] Budgets are 500,000 bytes to "map usable" and 4,500,000 with
every default-on layer. [REPO] **No geometry was downloaded for this
document, so every byte figure for a new source is an unmeasured estimate.**
A measured spike is needed before any specification.

| | Option A — finer SMA only | Option B — PAD-US units, SMA as background | Option C — B plus a reviewed access registry |
|---|---|---|---|
| What the user taps | A finer agency polygon; still "USFS", no name | A named unit (forest, park, open space) where PAD-US has one; otherwise agency context or "no record" | As B, with a reviewed statement on the units that have been reviewed |
| Source | BLM Colorado SMA (S2) replaces S1 | PAD-US fee layer (S3) for units; S2 or S1 for federal background | As B, plus `v2/regions/<id>/land-access.json`, hand-curated, modelled on M4's `water-recreation.json` |
| Features per region | About 260 and 119 before clipping [V-live, box counts] | About 91 and 487 units before clipping [V-live], plus background | Same as B; registry starts with a short reviewed list |
| Bytes | Likely several times today's; many polygons are tiny (sampled: 11 m², 124 m²) and need a sliver rule [INF] | Unit layer likely comparable to today's land file; total up to about double if SMA stays as background [INF] | B plus a small JSON, probably tens of kilobytes [INF] |
| Requests | 1, as now | 2 (units, background); background could load on demand | 3; the registry need not load before a land sheet opens |
| Stable id | `GlobalID`, persistence untested | `Source_PAID`, persistence and uniqueness untested | Registry keys on the B unit id; inherits its risk |
| Maintenance | One source that may change daily; no version to pin | PAD-US is versioned (a release every one to two years); pin the version; local records can be 15 years old | B plus a human review of every record on a schedule (M4 uses 90 days) |
| Fixes | Boundary coarseness; splits `OTHFE`-type classes somewhat | No place identity; "Other Federal"; state and local land; wilderness names | The only option that says anything a user can act on, and only from an operator's own page |
| Does not fix | No unit identity; residual private class remains unless relabelled; no access | Residual class (must still be decided); access; local data age | Coverage: unreviewed units stay unknown |
| New risk | Finer lines read as property lines | PAD-US overlaps by design; a default `Pub_Access` value leaking into display; 2010 local data shown as current | A stale or wrong statement is the most harmful error the product can make; review load grows with every region |

Notes:

- A and B are not exclusive; B's background layer is A or today's S1. [INF]
- C is a model, not a dataset. It mirrors M4 section 9: one record per unit,
  each statement with its own evidence object, a URL on the operator's own
  site, manual review, `last_confirmed_at`, a maximum age, and unknown as the
  default. [REPO] It could be specified in M5 and populated later.
- In every option the residual class and the "no record" wording have to be
  settled first (section 4.4).
- Parcels are in none of the options.

## 7. Major owner decisions

| # | Decision | Recommendation | Reason |
|---|---|---|---|
| 1 | What is the residual `PVT` class shown as? | Label it with the source's own name, "Private or Unknown", draw it as unknown, and stop tinting it as a class. | The source does not call it private; rule 11 and W5 both assume unknown is visible. |
| 2 | What unit does a user tap? | A named unit where a source names one; agency context elsewhere. | It is the only handle for unit-specific rules later; SMA cannot provide it. |
| 3 | Is the published dimension ownership or management? | Management. Rename the Aspen `land_ownership` layer; treat owner as an optional source fact. | The source and the contract both say management. |
| 4 | Which background source: national SMA or Colorado SMA? | Run a measured spike on Colorado SMA before choosing. | Finer and public domain, but unmeasured bytes, slivers and untested ids. |
| 5 | Is PAD-US admitted, and for what? | Yes, for unit name, manager, designation and source date only, pinned to a version. | Verified live; names real places; versioned. |
| 6 | May any source access attribute (`Pub_Access`, `PUB_ACCESS`, `public_access`, `restriction`) be displayed? | No. Do not display it or branch on it; decide separately whether it is kept in canonical data at all. | Sampled values are defaults; a displayed "Open" would be read as permission. |
| 7 | Do reviewed access statements belong in M5? | Specify the registry shape in M5; populate nothing, or a very small reviewed set, until the owner approves a review process. | Keeps M5 a classification milestone while reserving the only honest route to access. |
| 8 | Which statuses may a land access statement take? | Unknown by default; restrictions and closures as stated by the operator; no positive status in M5. | M4 never sets access to `allowed`; positive claims fail closed. |
| 9 | Are parcels in scope? | No, not in M5. | Terms, owner names and addresses, static republication and false precision. |
| 10 | State and local sources (CPW, State Land Board, county open space)? | Admit each only after its publisher confirms terms in writing; until then PAD-US is the only state and local unit source. | No licence text grants republication. |
| 11 | Does wilderness get a name in M5? | Yes: publish `areaname` and a stable area id as a designation overlay; rules stay out. | The field exists; a name adds identity without a claim. |
| 12 | What does tier A mean? | Leave it undefined and unused in M5 unless a source states an accuracy. | No source checked states one; a tier named "authoritative" would overstate. |
| 13 | What is the stable-id rule? | Namespace plus the source's own id, no row-number fallback; test persistence across two fetches first. | M4's rule; `OBJECTID` and `SMA_ID` are both unsuitable. |
| 14 | One freshness policy for land? | Yes, one policy for both regions, set per source. | The same data is stale in one region and never stale in the other. |
| 15 | What does the map say where a Forest Service trail crosses the residual class? | A fixed sentence that the two sources disagree or differ in scale, and that neither establishes access. | Otherwise the user infers either "private" or "allowed". |
| 16 | One schema, and may Aspen's ids and unread `manager` values be migrated and removed? | Yes, with a legacy id map as M4 did. | Removes published wording nobody approved and prevents drift. |

## 8. Risks

| # | Risk | Basis |
|---|---|---|
| R1 | A finer or named land layer looks more certain than it is, and users read it as permission. This is the central risk of the milestone. | [INF]; trust principle 7 [REPO] |
| R2 | An access default leaks into the interface through a label, a filter or a colour. | [V-live] sample; [INF] |
| R3 | Relabelling the residual class turns most of Douglas County "unknown", which is honest but may read as a regression. | [V-audit]; [INF] |
| R4 | PAD-US local records are old. Sampled Douglas County rows are dated 2010. A unit may have changed hands or boundaries since. | [V-live] |
| R5 | PAD-US granularity is uneven: a whole national forest is one record beside a 356-acre county property. "Unit" will not mean one thing. | [V-live] |
| R6 | Identifiers may not persist. `GlobalID` and `Source_PAID` are untested across updates; a registry keyed on them could detach silently. | [UNK] |
| R7 | Colorado SMA changes without versions, so two fetches may differ with no explanation, and its metadata is inconsistent about cadence. | [V-live] |
| R8 | Overlapping records (fee, easement, designation, proclamation) produce several answers for one tap. | [H]; [INF] |
| R9 | Sources disagree at edges (3.57 km² of wilderness on `PVT` today). More sources mean more visible disagreement. | [V-audit]; [INF] |
| R10 | Licence drift: terms unread (PAD-US Explorer), unstated (USFS, counties) or restrictive (CPW indemnity) are assumed away. | [V-live] |
| R11 | Byte and performance budgets: nothing was measured. | [REPO]; [UNK] |
| R12 | A reviewed registry creates a standing human workload that grows with regions; overdue reviews accumulate. | [INF] from M4 [REPO] |
| R13 | Samples here are five rows per source. They show that defaults and nulls exist, not how common they are. | [V-live] |

## 9. What M5 must not claim

M5 must not state, style, order or imply any of the following:

1. That camping, parking, entry, crossing or any other activity is allowed
   anywhere, on the strength of ownership, managing agency, designation, a
   unit's existence or any public-access attribute in any dataset.
2. That land is private because it is non-federal, has no record, or carries
   a residual or unrecognised code.
3. That land is open because it is public, federal, state, county or
   protected. State trust land is the standing counter-example. [H]
4. That land is closed or off limits because a source classes it as private.
5. That any line is a property line, a surveyed boundary or a legal boundary.
6. That a unit's record is current because it was fetched recently.
7. That a named unit's rules are those of its agency in general.
8. That a trail or road crossing a land class has, or lacks, a right of way.
9. That the absence of a restriction record means there is no restriction.
10. That a region, layer or unit is verified, complete, open, permitted or
    legal. [REPO, trust principle 8]

## 10. Open questions

### For the owner

1. Decisions 1 to 16 above; 1, 2, 6 and 7 shape everything else.
2. Is a map that shows most of Douglas County as unknown acceptable?
3. Is M5 allowed to finish with no access statement at all, leaving that to a
   later milestone?
4. Who performs and re-performs manual review if a registry is created, and
   how many units is a sustainable first set?
5. Should a measured spike (bytes, feature counts after clipping, sliver
   counts, agreement between sources, id persistence over two fetches) be
   commissioned before the specification is written?

### For an outside party

| Ask | Of whom |
|---|---|
| Do the "terms of use of the PAD-US Data Explorer" restrict republishing a clipped, reclassified subset? Is `Source_PAID` unique and persistent across versions? | USGS Gap Analysis Project (pad-us@usgs.gov is the address the service gives) |
| Is `GlobalID` persistent across edits? Is `PRI` a residual class, like the national "Private or Unknown"? Which cadence is right? | BLM Colorado State Office |
| Is there a licence for the national SMA service? | BLM headquarters |
| May a derived subset of `CPWAdminData` property layers be republished, given the "product and property" and indemnity text? | Colorado Parks and Wildlife GIS unit |
| Which service is the official trust-land publication, under what terms? | Colorado State Land Board |
| Under what terms may the Open Spaces layer be republished? What do `restriction`, `closure` and `public_access` mean? | Pitkin County GIS; Open Space and Trails |
| Is an agreement required for `OPEN_SPACE`? What do `PUB_ACCESS` values mean? | Douglas County GIS |
| Does free public republication, or a later paid feature, count as "resale"? | Colorado OIT GIS team (only if parcels are ever reconsidered) |

### Still unknown after this session

- Geometry size, vertex density and sliver counts of S2 and S3 for either
  region.
- Whether S2 tiles the extent completely, as S1 does.
- How often `Pub_Access` is a default across each region, and what the
  non-default values are.
- Field schemas of the CPW layers, Douglas parcels, Pitkin easements, PLAD
  and the other PAD-US layers.
- Everything in section 3.2.

## Appendix A — requests made

All 25 were HTTP GET with `curl`, metadata or attribute-only, no geometry.
All returned HTTP 200. The responses and request log `urls.log` are saved
outside the repository. Request 9 returned no rows (a multipoint filter the server did
not honour) and is not relied on.

| # | Saved as | URL |
|---|---|---|
| 1 | `01-blm-natl-sma-service.json` | `https://gis.blm.gov/arcgis/rest/services/lands/BLM_Natl_SMA_LimitedScale/MapServer?f=pjson` |
| 2 | `02-blm-natl-sma-layer1.json` | `https://gis.blm.gov/arcgis/rest/services/lands/BLM_Natl_SMA_LimitedScale/MapServer/1?f=pjson` |
| 3 | `03-blm-natl-sma-rows.json` | `https://gis.blm.gov/arcgis/rest/services/lands/BLM_Natl_SMA_LimitedScale/MapServer/1/query?where=OBJECTID+IN+(413,1069,25,1017,1028)&outFields=*&returnGeometry=false&resultRecordCount=5&f=pjson` |
| 4 | `04-blm-co-sma-layer1.json` | `https://gis.blm.gov/coarcgis/rest/services/lands/BLM_Colorado_Surface_Management_Agency/FeatureServer/1?f=pjson` |
| 5 | `05-blm-co-sma-mapserver.json` | `https://gis.blm.gov/coarcgis/rest/services/lands/BLM_Colorado_Surface_Management_Agency/MapServer?f=pjson` |
| 6 | `06-usfs-basicownership-0.json` | `https://apps.fs.usda.gov/arcx/rest/services/EDW/EDW_BasicOwnership_01/MapServer/0?f=pjson` |
| 7 | `07-blm-co-sma-count-aspen.json` | `https://gis.blm.gov/coarcgis/rest/services/lands/BLM_Colorado_Surface_Management_Agency/FeatureServer/1/query?where=1%3D1&geometry=-107.05,39.0,-106.57,39.26&geometryType=esriGeometryEnvelope&inSR=4326&spatialRel=esriSpatialRelIntersects&returnCountOnly=true&f=pjson` |
| 8 | `08-blm-co-sma-count-douglas.json` | same query with `geometry=-105.329445,39.129479,-104.660584,39.566193` |
| 9 | `09-blm-co-sma-points-douglas.json` | same layer `/query` with a five-point `esriGeometryMultipoint` filter, `outFields=*&returnGeometry=false&resultRecordCount=5&f=pjson` (empty result) |
| 10 | `10-arcgis-search-padus.json` | `https://www.arcgis.com/sharing/rest/search?q=PAD-US%204%20owner%3Ajlrose_usgs%20OR%20(title%3A%22PAD-US%22%20AND%20type%3A%22Feature%20Service%22%20AND%20orgid%3Av01gqwM5QqNysAAi)&num=20&f=json` |
| 11 | `11-padus-fee-layer0.json` | `https://services.arcgis.com/v01gqwM5QqNysAAi/arcgis/rest/services/Fee_Managers_PADUS/FeatureServer/0?f=pjson` |
| 12 | `12-padus-fee-count-douglas.json` | same layer `/query?where=1%3D1&geometry=-105.329445,39.129479,-104.660584,39.566193&geometryType=esriGeometryEnvelope&inSR=4326&spatialRel=esriSpatialRelIntersects&returnCountOnly=true&f=pjson` |
| 13 | `13-padus-fee-count-aspen.json` | same with `geometry=-107.05,39.0,-106.57,39.26` |
| 14 | `14-padus-fee-sample-douglas.json` | same layer `/query?where=1%3D1&geometry=-105.10,39.40,-104.75,39.56&geometryType=esriGeometryEnvelope&inSR=4326&spatialRel=esriSpatialRelIntersects&outFields=*&returnGeometry=false&resultRecordCount=5&f=pjson` |
| 15 | `15-usfs-surfaceownership-0.json` | `https://apps.fs.usda.gov/arcx/rest/services/EDW/EDW_SurfaceOwnership_01/MapServer/0?f=pjson` |
| 16 | `16-usfs-wilderness-0.json` | `https://apps.fs.usda.gov/arcx/rest/services/EDW/EDW_WildernessStatus_01/MapServer/0?f=pjson` |
| 17 | `17-pitkin-openspaces-101.json` | `https://maps.pitkincounty.com/arcgis/rest/services/Hosted/Open_Spaces/MapServer/101?f=pjson` |
| 18 | `18-pitkin-parcel-0.json` | `https://maps.pitkincounty.com/arcgis/rest/services/Hosted/Parcel_Boundary/MapServer/0?f=pjson` |
| 19 | `19-douglas-landuse-fs.json` | `https://apps.douglas.co.us/gisod/rest/services/Landuse/FeatureServer?f=pjson` |
| 20 | `20-oit-parcels-fs.json` | `https://gis.colorado.gov/public/rest/services/Address_and_Parcel/Colorado_Public_Parcels/FeatureServer?f=pjson` |
| 21 | `21-douglas-openspace-5.json` | `https://apps.douglas.co.us/gisod/rest/services/Landuse/FeatureServer/5?f=pjson` |
| 22 | `22-arcgis-search-cpw-slb.json` | `https://www.arcgis.com/sharing/rest/search?q=(title%3ACPWAdminData%20OR%20title%3A%22CPW%20Admin%22%20OR%20(%22Colorado%20State%20Land%20Board%22%20AND%20(surface%20OR%20ownership%20OR%20trust)))%20AND%20type%3A%22Feature%20Service%22&num=25&f=json` |
| 23 | `23-cpw-admindata-fs.json` | `https://services5.arcgis.com/ttNGmDvKQA7oeDQ3/arcgis/rest/services/CPWAdminData/FeatureServer?f=pjson` |
| 24 | `24-blm-co-sma-sample-douglas.json` | `https://gis.blm.gov/coarcgis/rest/services/lands/BLM_Colorado_Surface_Management_Agency/FeatureServer/1/query?where=adm_manage+NOT+IN+('PRI','USFS')&geometry=-105.329445,39.129479,-104.660584,39.566193&geometryType=esriGeometryEnvelope&inSR=4326&spatialRel=esriSpatialRelIntersects&outFields=*&returnGeometry=false&orderByFields=OBJECTID&resultRecordCount=5&f=pjson` |
| 25 | `25-blm-co-sma-iso-metadata.json` (XML content) | `https://gis.blm.gov/coarcgis/rest/services/lands/BLM_Colorado_Surface_Management_Agency/FeatureServer/1/metadata?format=iso19139` |

Limits of this check:

- Counts in requests 7, 8, 12 and 13 are features intersecting a bounding
  box, not features clipped to the region.
- Row samples are five rows. Request 24 excluded `PRI` and `USFS` and was
  ordered by `OBJECTID`, so it shows one `BLM` and four `LOCAL` rows.
- Requests 10 and 22 are ArcGIS Online catalogue searches. They show that
  items exist and what their item pages say; they do not show who an item's
  official publisher is.
- No `usgs.gov`, `slb.colorado.gov`, `cpw.state.co.us`, COMaP or commercial
  page was fetched. Statements about those pages remain HERMES-SOURCED.
