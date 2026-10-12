DRAFT - UNREVIEWED TECHNICAL AUDIT (main bb85785)

# RECREATION SITE FACTS PACKET

Scope: preparation only for a possible small product change, so that recreation-site facts already in the data are shown usefully. Read-only audit of `main` at `bb85785` (checkout `m3-foundation`), offline. Nothing is implemented. Douglas County is the only region with a `recreation_sites` layer; Aspen has none.

## 1. Summary

- 36 recreation records, 10 source site types. All 36 are pinned on the map. Only 22 (5 CAMPGROUND, 17 TRAILHEAD) get any site facts in their panel. The other 14 show name, agency, fetch date and the layer limitation, and nothing else.
- The cause is one line, `v2/explore/browse.js:43`, which returns early for every `site_type` other than CAMPGROUND, TRAILHEAD and DISPERSED_AREA. For those 14 records it also skips the agency page link, although 7 of them have one.
- Every field on the records is declared in the manifest and passes the regional contract. Nothing is carried undeclared. No schema or manifest change is needed to render more.
- The source's operational status (`OPEN` on 35 of 36) is carried and declared but rendered nowhere. Recommendation: keep it withheld.
- A small post-M4 change is feasible for display only: show the already-declared published facts for all site types under an explicit "published by the source, not reviewed" label, with the agency link and the fetch date. It should ship with, or after, the directions integrity gate from the companion audit. Classifying sites as day-use or overnight in the finder, and anything that reads as overnight permission, belongs to M7.
- Both recreation and trail data were fetched on 2026-09-27 and passed the 168-hour refresh policy on 2026-10-04. Every panel already says "older than the refresh policy; refresh needed".

## 2. Fields and fill rates

Source: `v2/regions/douglas-co/research.json`, `/layers/recreation`, 36 features. A cell is the number of records with a non-null value. "placeholder" counts values that are the literal `No Data` or `N/A`.

| site_type | n | fee_description | restrictions | open_season | seasonal_operational_status | op_status_reason | restroom_availability | water_availability | activity_type_list | important_info | directions | usda_portal_url | rec1stop_url |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TRAILHEAD | 17 | 0 | 8 | 1 | 17 | 0 | 7 | 7 | 17 (14 placeholder) | 1 | 9 | 8 | 0 |
| CAMPGROUND | 5 | 0 | 5 | 5 | 5 | 0 | 5 | 5 | 5 | 4 | 5 | 5 | 4 |
| PICNIC SITE | 5 | 1 | 2 | 4 | 5 | 0 | 5 | 5 | 5 (5 placeholder) | 0 | 2 | 5 | 0 |
| RECREATION RESIDENCE | 3 | 0 | 0 | 0 | 3 | 0 | 0 | 0 | 3 (3 placeholder) | 0 | 0 | 0 | 0 |
| HORSE CAMP | 1 | 0 | 1 | 1 | 1 | 0 | 1 | 1 | 1 | 0 | 1 | 1 | 0 |
| OBSERVATION SITE | 1 | 0 | 0 | 1 | 1 | 0 | 0 | 0 | 1 (1 placeholder) | 0 | 1 | 1 | 0 |
| DAY USE AREA | 1 | 0 | 0 | 0 | 1 | 0 | 1 | 1 (1 placeholder) | 1 (1 placeholder) | 0 | 0 | 0 | 0 |
| FISHING SITE | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 (1 placeholder) | 0 | 0 | 0 | 0 |
| TARGET RANGE | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 (1 placeholder) | 0 | 0 | 0 | 0 |
| DOCUMENTARY SITE | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 (1 placeholder) | 0 | 0 | 0 | 0 |
| ALL | 36 | 1 | 16 | 12 | 36 | 0 | 19 | 19 | 36 (27 placeholder) | 5 | 18 | 20 | 4 |

Also present on all 36: `site_type`, `site_name`, `name` (a copy of `site_name`), `id`, `evidence`.

Value notes:

- `fee_description`: one value in the whole layer, CABIN RIDGE PS, `Day Use:\n$7 per vehicle per day`. No campground carries a fee. An empty fee must not be read as free.
- `seasonal_operational_status`: `OPEN` × 35, `CLOSED` × 1 (ZINN RANCH, DOCUMENTARY SITE). `op_status_reason`: empty on all 36.
- `open_season`: 8 distinct values. 7 records carry a 2021 date ("May 28, 2021" × 3, "May 1, 2021" × 2, "January 1, 2021" × 2); the rest are "Memorial Day Weekend", "April/May", "Year-round", "May 8", "May 15". It reads as an opening date, not a season range.
- `water_availability`: `No` × 8, `Yes` × 4, `No water` × 3, `NO WATER` × 2, `None` × 1, `N/A` × 1.
- `restroom_availability`: `Vault toilet` × 7, `No` × 6, `Vault toilets` × 4, one portable-toilet sentence, `One CXT double` × 1.
- `restrictions`: 13 distinct texts on 16 records. RIM ROAD's contains database escape text (`'||chr(38)||'rsquo;`).
- Cabin Ridge picnic site (`recreation-3316544`), the acceptance-test example: fee as above; restrictions "… Overnight use prohibited. Fires only in established fire rings. Pack it in; pack it out."; restrooms "Vault toilet"; water "No" (the data says no water at this site); `open_season` "May 8"; directions present; portal page https://www.fs.usda.gov/recarea/psicc/recarea/?recid=12917.

## 3. Declared, validated, undeclared

Manifest `v2/regions/douglas-co/region.json:17`, layer `recreation`, kind `recreation_sites`:

- `fields.source` declares all 14: `site_name, site_type, activity_type_list, seasonal_operational_status, op_status_reason, fee_description, open_season, usda_portal_url, rec1stop_url, important_info, restrictions, water_availability, restroom_availability, directions`. `fields.derived` is empty.
- `id`, `name` and `evidence` are reserved names (`v2/pipeline/docs/data-contract.md:147-161`) and are correctly not listed.
- Contract rule R26 (`data-contract.md:256`) requires every property to be reserved or declared, so an undeclared field would fail validation. The data has exactly the 14 declared plus the 3 reserved. Carried but undeclared: none.
- The contract does not validate the content of any of the 14. They are free text. Known note N10 (`data-contract.md:340`, `docs/specs/M2-regional-data-contract.md:544`) records that `seasonal_operational_status` is verbatim and may be historical.
- The pipeline writes exactly this list (`v2/pipeline/scripts/enrich_douglas.py:38-39`); the display artifact `display/recreation.geojson` keeps all of it.
- Layer limitation text: "Recreation-site inventory. Season and operational attributes can be historical; no live open status." Freshness: `max_age_hours: 168`, status record at `/source_status/recreation`, retrieved `2026-09-27T14:15:40Z`.
- `fact_coverage.restrictions` in the same manifest says "No reviewed stay limits, seasons, permits or orders are loaded." and `camping_permission` says "No camping permission is confirmed. A recreation-site record shows that a facility is listed, not that it is open or that a given setup may stay."

## 4. What is rendered today, and by which code

Map: the whole layer is drawn, so all 36 are pinned, with name labels from zoom 14 (`v2/explore/shell.js:134`).

Panel, part one, for every record (`shell.js:114-125`, `v2/explore/evidence.js:39-68`): title from `name`; agency ("USFS"); "Source fetched 2026-09-27 · older than the refresh policy; refresh needed"; the layer limitation; a "View source ↗" link to `evidence.source_url`, which is the ArcGIS layer, not the site's page. `evidence.js` has branches for trails, roads and research areas and none for `recreation_sites`.

Panel, part two, the browse detail (`v2/explore/browse.js:42-56`):

```js
if(!f.properties.activities&&!['CAMPGROUND','TRAILHEAD','DISPERSED_AREA'].includes(f.properties.site_type))return;
```

That is line 43. It is the exact branch that leaves picnic and day-use records nearly empty. For the 22 records that pass it:

| element | code | note |
|---|---|---|
| "Official listing / source ↗" | `:44`, `:5` | `rec1stop_url`, else `usda_portal_url`, else the ArcGIS URL. For the 4 campgrounds with a Recreation.gov URL the Forest Service page is never linked |
| "Published source · current access unconfirmed" | `:44` | |
| Save to plan | `:45` | |
| "Directions to facility ↗" (coordinates) | `:47` | |
| `restrictions` → "Published restrictions" | `:52` | |
| `important_info` → "Important information" | `:52` | |
| `activity_type_list` → "Listed activities" | `:52` | suppressed when `No Data` |
| `fee_description` → "Fees (verify current price)" | `:52` | no campground or trailhead has a value, so this never appears today |
| `open_season` → "Published season (may be historical)" | `:52` | |
| `water_availability` → "Water" | `:52` | `N/A` is not suppressed, only `No Data` |
| `restroom_availability` → "Restrooms" | `:52` | |
| `directions` → "Agency directions" | `:52` | see the directions integrity audit |
| stay-limit caveat | `:53` | |
| nearby trails for the selected activity | `:54` | |
| "Check alerts & coverage" | `:55` | |

Never rendered for any site type: `site_type` as a value (only via the row label), `seasonal_operational_status`, `op_status_reason`, `site_name`.

The 14 records that fail line 43 (5 PICNIC SITE, 3 RECREATION RESIDENCE, 1 each HORSE CAMP, OBSERVATION SITE, DAY USE AREA, FISHING SITE, TARGET RANGE, DOCUMENTARY SITE) get part one only. They lose the agency page link (7 of them have a `usda_portal_url`: 5 picnic sites, the horse camp, the observation site), the coordinate directions link, the save button and the "Check alerts & coverage" button. Their type is not stated anywhere in the panel.

Finder (`browse.js:7`, `:26`, `:35`; `v2/explore/trail-seasons.js:26`):

- The "Find" control has three modes: Trails, Camping, Trailheads.
- Camping lists the Rampart Range area listing from `extras.js` plus records whose `site_type` is exactly `CAMPGROUND` (5). Trailheads lists `site_type === 'TRAILHEAD'` (17).
- No mode lists any other type, so 14 records can only be reached by tapping a pin.
- The summary line counts "campgrounds" and "trailheads" the same way (`:40`).
- Pinned by tests: `v2/pipeline/tests/douglas-discovery.test.cjs:12` ("camping excludes trailheads and horse camps") and `explore-compatibility.test.cjs:36-44` with `browseCounts` in `fixtures/explore-compatibility.json`.
- Latent hazard: `kind()` at `browse.js:6` labels anything that is not a trail, trailhead or dispersed area as "Campground". It is unreachable for the 14 today. If the gate at line 43 or the finder is widened without changing `kind()`, a picnic site would be labelled "Campground" in rows and in the exported plan.

## 5. Proposed smallest safe improvement (not implemented)

### 5.1 What to render, for all site types

A single block in the site panel, headed:

`Published by the Forest Service — not reviewed by Ohvernight`

followed by the existing fetch line ("Source fetched 2026-09-27 · older than the refresh policy; refresh needed") and then, when present and not a placeholder:

| field | proposed label | kind |
|---|---|---|
| `site_type` | `Source site type: PICNIC SITE` (verbatim) | static |
| `usda_portal_url` | `Forest Service page ↗` | static |
| `rec1stop_url` | `Recreation.gov listing ↗` | static |
| `restrictions` | `Published restrictions (source text)` | semi-static |
| `fee_description` | `Published fee (verify current price)` | dynamic |
| `restroom_availability` | `Restrooms (source text)` | static |
| `water_availability` | `Water (source text; seasonal supply not confirmed)` | dynamic |
| `open_season` | `Published opening date or season (may be historical)` | dynamic |
| `important_info` | `Source notes` | dynamic |
| `activity_type_list` | `Activities listed by the source` | static |
| `directions` | `Directions text published in the source record` | static, gated |

Rules:

- Values are shown verbatim. No summarising, no badges such as "Fee", "No water" or "Day use" derived from the text.
- Both links are shown when both exist. Today the Forest Service page is hidden behind the Recreation.gov link for four campgrounds.
- Suppress placeholders `No Data` and `N/A`; show nothing instead of "unknown" chips for absent fields, plus one closing line: `Fields the source leaves blank are unknown.`
- Apply the directions integrity gate from the companion audit to every descriptive field: no agency page URL, no descriptive text.
- Keep the existing closing caveat (`:53`) for campgrounds. For other types use a neutral equivalent, for example `This record shows that a facility is listed. It does not show that it is available, or what is allowed there today.`

### 5.2 Day-use and picnic versus overnight, without inferring permission

- Classify by the source's `site_type` only, shown verbatim. Do not create an Ohvernight category such as "day use" or "overnight" and do not derive one from restriction text.
- "Overnight use prohibited" appears in the `restrictions` text of DEVILS HEAD PS and CABIN RIDGE PS. Show it as source text under "Published restrictions". Do not turn it into a flag, and do not conclude the reverse for the 3 picnic sites whose `restrictions` is empty.
- Finder: the smallest safe step is a fourth mode, `Other listed sites`, that lists the 14 records with the verbatim site type as the row label. Keep the Camping mode as `CAMPGROUND` only. Whether HORSE CAMP belongs under camping is an identity and permission question for M7; the current exclusion is pinned by a test.
- Fix `kind()` so that any type outside the known three is labelled with its verbatim site type, never "Campground".

### 5.3 Static versus dynamic, and staleness

- Static enough to show with the fetch date: `site_type`, links, `restroom_availability`, `activity_type_list`, `directions`, `restrictions`.
- Dynamic: `fee_description`, `water_availability`, `open_season`, `important_info`, `seasonal_operational_status`, `op_status_reason`.
- The block should carry the fetch line once at the top, using the existing `E.retrievalLine` logic (`evidence.js:9-15`) so the stale wording is identical everywhere.
- Dynamic fields keep a per-label qualifier (table above). When the layer is past its refresh policy, add one line under the heading: `These values were read on 2026-09-27 and may have changed.`
- `open_season` values with an explicit past year (7 records) are evidence that the descriptive text itself is years old. The label must keep "may be historical".

### 5.4 What must not be shown

- `seasonal_operational_status`. Keep it withheld. Reasons: it is `OPEN` on 35 of 36 records, including seven whose opening date is given as 2021; `op_status_reason` is empty everywhere, so there is no date or reason attached; the manifest limitation says the layer has "no live open status"; `docs/product/trust-principles.md` sections 2 and 6 forbid inferring current conditions from historical data and require reviewed evidence for any value asserting openness; section 8 keeps "open" out of manifests, tests and documents. Printing "OPEN" beside a site, however labelled, reads as a current status.
- The single `CLOSED` value (ZINN RANCH) is equally undated. Recommendation: withhold it too in the small change, for symmetry and because one undated value is not a status feed. If the owner wants negative signals surfaced, the wording would be `The source record lists this site as closed (undated)`, and that is an owner decision.
- `op_status_reason`: nothing to show.
- Any derived statement: "free", "no fee", "open year-round", "camping allowed", "day use only", "has water".
- Descriptive text on records that fail the directions integrity gate (RAMPART ENTRANCE, TURKEY, DEVILS HEAD TH and DAKAN on this snapshot).
- Silent clean-up of source text in the browser. RIM ROAD's escape artefacts should be shown verbatim or fixed in the pipeline as a documented transformation, not patched in the renderer.

### 5.5 Schema, manifest and files

- Schema or manifest change needed: none for rendering. All fields are already in `fields.source`.
- Not needed but worth a later decision: retaining source identifiers (companion audit), which would add `fields.source` entries.
- Any change to `limitations` or `fact_coverage` wording needs owner approval (trust principles section 8). The proposal does not require one.

Frontend files touched:

- `v2/explore/browse.js`: `:5` (links), `:6` (`kind`), `:7` and `:26` and `:35` (optional fourth finder mode and its count text), `:18` and `:37` (whether other types can be saved; recommend no for the small change), `:43` (the gate), `:52-53` (the facts block and caveat).
- `v2/explore/explore.css` only if the block needs styling.
- Alternative placement: a `recreation_sites` branch in `v2/explore/evidence.js:39-68`, which would show the facts in any region whether or not the Browse module is attached. It is the cleaner home but changes a file shared with Aspen and its parity tests. For the smallest change, stay in `browse.js`.

Tests needed:

- Node unit test for a pure facts function exported from `browse.js`: labels; placeholder suppression including `N/A`; status never present in output for `OPEN` or `CLOSED`; both links; URL gate; verbatim text.
- Node test that `kind()` returns the verbatim type for PICNIC SITE and HORSE CAMP.
- Browser check: open CABIN RIDGE PS from its pin and assert the fee, the restriction text, restrooms, the Forest Service link and the stale fetch line are present and the string "OPEN" is absent.
- Published-data assertion that no rendered string for the layer contains the status values.
- If the finder gains a mode: update `browseCounts` in `fixtures/explore-compatibility.json` and `explore-compatibility.test.cjs:36-44`. These are pinned base-commit values, so the pull request must call the change out.
- Run `legacy-wording.test.cjs` and `proximity-wording.test.cjs` against the new labels.

## 6. Trust and freshness concerns

- Staleness: recreation was retrieved `2026-09-27T14:15:40Z`; the 168-hour policy expired `2026-10-04T14:15Z`. On 2026-10-08 the data is about 11 days old. Showing more fields from a stale snapshot increases exposure; a refresh (a human-run, networked step) should precede or accompany the change.
- Provenance: `evidence.confidence` is `unverified` and `verification_method` is `source_fetch` on every record. The heading must not use "verified", "official facts" or similar. A fetch is not a confirmation (trust principles section 4).
- Integrity: two records carry another site's text and three more are ambiguous (companion audit). Widening what is rendered before the gate exists would publish more unverifiable text, including on the horse camp.
- Restrictions text is already rendered for campgrounds and trailheads, so showing it for picnic sites adds no new category of claim. It does sit beside `fact_coverage.restrictions`, which says no reviewed restrictions are loaded; the "not reviewed" heading keeps the two consistent.
- Internal conflicts in the source will be visible side by side (INDIAN CREEK water "Yes" with a note that water is questionable; OUZEL vault against portable toilets). That is acceptable if the block is clearly source text, and is a reason not to summarise.
- Sparse data: fee is filled on 1 of 36 and season on 12 of 36. The block will be short for most records and must not make absence look like a negative.
- RECREATION RESIDENCE (3) and DOCUMENTARY SITE (1) are pinned today with no context. Whether they should be pinned at all is a product question outside this packet.

## 7. Timing: small post-M4 change or M7?

- Safe as a small post-M4 change: sections 5.1, 5.3, 5.4, the `kind()` fix and the agency links, for all site types, provided the directions integrity gate ships first or in the same pull request and the status stays withheld. It adds no field, no schema change, no inference and no new claim type; it fixes an omission in presenting declared source fields.
- Borderline, owner's call: the fourth finder mode. It is small but changes pinned finder counts and makes non-camping sites discoverable next to camping.
- Wait for M7: any day-use versus overnight classification, treating HORSE CAMP as camping, reservation or fee logic, anything that expresses overnight legality, and structured (non-verbatim) restroom, water or fee values. `ROADMAP.md` assigns "developed campground identity", "overnight legality and reservation requirements as claims" and "freshness and seasonality" to M7.
- Scheduling the work is the coordinator's and owner's decision under `docs/agent-stack/`; this packet only states what is technically separable.

## 8. Could not determine

- Whether the source layer exposes further useful fields (site identifiers, last-updated dates, capacity). The pipeline keeps 14 attributes and I had no network access.
- Whether `seasonal_operational_status` has a meaning other than current status in the agency's data dictionary.
- Whether the committed display artifact would be regenerated unchanged by `build_display.py`; not run.
