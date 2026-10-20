# M7 specification — repository evidence

Status: measured facts for the M7 draft specification
([docs/specs/M7-camping.md](../../specs/M7-camping.md)). Every value here was read
from committed files at `main` `c04f5d6` on 2026-10-20 with read-only scripts
run from the repository root. No network request was made. Nothing here is a
review in the sense of trust principle 4, and nothing here is a claim about
any place.

Items are cited in the specification as [MEAS E1] to [MEAS E11].

## E1. Aspen overnight-related layers and place lists

From `v2/regions/aspen/region.json`, `v2/map-data-v2.json`,
`v2/overnight-options.json`, `v2/ridb-options.json` and
`v2/regions/aspen/explore.json`.

| Layer | Kind / format | Records | Notes |
|---|---|---:|---|
| `overnight_options` | `overnight_inventory` / `place_list` | 5 | `kind`: campground 3, dispersed 1, lodging 1. `checked_on` 2026-09-24 on all 5. `access` (an MVUM road designation object) on 3; `tent_only: true` on 1 (Silver Bar); `requires_high_clearance: true` on 1 and `stay_limit_days: 5` on 1 (both Lincoln Creek). No record has a `camping_permission` or `facts` field. `max_age_hours` 720 |
| `ridb_options` | `overnight_inventory` / `place_list` | 4 | `camping_permission: "unknown"` on 4; six `facts` per record, every one `{"status": "unknown"}`; `source_is_search` on 4. `max_age_hours` 168 |
| `lodging_developed` | `overnight_inventory` / feature collection | 0 | |
| `reviewed_sites` | `reviewed_sites` | 0 | |
| `leads` | `community_leads` | 0 | |
| `dispersed_corridors` | `research_areas` | 51 | `camping_permission` unknown, `needs_review` true, `actual_site_confirmed` false on all. `evaluated_trip` 2026-09-25 to 2026-09-26, `high_clearance`, on the first feature read. Six `required_checks`. `applicable_rule_context` `[]` on the first feature read. Explore entry title "Areas to research", `default_on: true`. Display file 709,990 bytes |
| `dispersed_corridor_points` | `research_areas`, `must_be_empty` | 0 | |
| `mvum_roads` | `roads` | 54 | `access_status`: `designated_open` 51, `restricted` 3. `vehicle_class`: `highway_legal` 37, `all_vehicles` 17. `designations` keys `passenger_car`, `high_clearance`, `motorhome`, each `{designation, dates_open}`; all 54 have `designation: "open"` for all three keys. `evaluated_trip` on every feature. Display file 417,055 bytes |
| `fire_restriction_stage` | `restriction_monitor` | 1 | `pitkin-fire-monitor`: `status` unknown, `stage` null, `last_confirmed_at` null, `max_age_hours` 24, `verification_method` `html_change_monitor`, source `https://pitkincounty.com/CivicAlerts.asp` |

Features in `v2/map-data-v2.json` carrying a `camping_permission` property: 108, every value `unknown`.

## E2. Aspen rules registry and screening configuration

`v2/pipeline/config/rules-registry.json`: one rule, `lincoln-creek-listed-sites`,
`place_ids` `["lincolncreek", "ridb-259461"]`, `road_names` `["LINCOLN CREEK"]`,
`stay_limit_days` 5, `requires_high_clearance` true, `camping_permission`
`unknown`, `last_confirmed_at` `2026-09-25T03:15:51Z`, `max_age_hours` 720. The
manifest's `rules` points to this file, and Aspen `fact_coverage.restrictions`
is `reviewed_partial` on that basis.

`v2/pipeline/config/legal_rules.yaml` `screening`: `road_buffer_ft: 300`,
`water_setback_ft: 100`, six `required_checks`, three `rules_to_review` entries
(White River camping guidance, Aspen–Sopris occupancy order, Lincoln Creek), none
with a review date.

## E3. Douglas County overnight-related records

From `v2/regions/douglas-co/research.json` and `region.json`.

- `recreation`: 36 records. `site_type`: TRAILHEAD 17, CAMPGROUND 5, PICNIC SITE 5,
  RECREATION RESIDENCE 3, and one each of HORSE CAMP, TARGET RANGE, DOCUMENTARY
  SITE, OBSERVATION SITE, FISHING SITE, DAY USE AREA. `verification_method`
  `source_fetch` on all 36. No `camping_permission` property.
- Overnight-related sentences inside the source's `restrictions` text, as the
  source holds them (unreviewed source text, not claims):

| Record | Site type | Sentence |
|---|---|---|
| `recreation-3295146` | CAMPGROUND | "You must be in a designated campground to stay overnight." |
| `recreation-3316014` | CAMPGROUND | "You must be in a designated campground to stay overnight." |
| `recreation-3295555`, `recreation-3296016`, `recreation-3306411` | CAMPGROUND | "Camping is NOT ALLOWED behind a LOCKED GATE." |
| `recreation-3304676` | HORSE CAMP | "Camping is NOT ALLOWED behind a LOCKED GATE." |
| `recreation-3296151` | TRAILHEAD | "Parking and camping in designated sites only." |
| `recreation-3311222`, `recreation-3316544` | PICNIC SITE | "Overnight use prohibited." |

- `rules`: `null`. Fact coverage: `ownership`, `road_access`, `trail_access`
  `context`; `public_access`, `camping_permission`, `closures`, `restrictions`,
  `recreation_permission` `none`.
- `recreation` display file 33,769 bytes; `roads` 208,201 bytes.

## E4. Douglas hard-coded area listing

`v2/regions/douglas-co/extras.js:3` defines one record with `geometry: null`,
`id` `rampart-designated-area`, `site_type` `DISPERSED_AREA`, a restriction
sentence paraphrasing a seasonal camping closure, and
`evidence.retrieved_at` `2026-09-27` (date only). It is register item N7,
deferred to M7.

## E5. Vehicle vocabularies in use

| Where | Keys or labels |
|---|---|
| `v2/pipeline/scripts/lib/access.py:5-7` | `passenger_car`, `high_clearance`, `motorhome` (mapped from MVUM fields `passengervehicle`, `highclearancevehicle`, `motorhome` and their `_datesopen` fields) |
| `v2/explore/capabilities.js:32`, `:57` | `passenger_car`, `high_clearance`, `motorhome` |
| `v2/explore/browse.js:20`, `:32` | display labels stored as values: `Car / SUV`, `High-clearance vehicle`, `Truck with trailer`, `Motorhome / RV` |
| `v2/regions/douglas-co/explore.json` `trip_defaults.vehicle` | `Car / SUV` |
| `v2/regions/aspen/explore.json` `trip_defaults.vehicle` | `passenger_car` |
| M6 draft 9.1 (`82a3c84`, unapproved) | trail keys `motorcycle`, `atv`, `ohv_wide`, `four_wheel_drive`, and others |

The Douglas selector is labelled "Camping vehicle"; the same panel says
"Camping vehicle suitability needs individual review" (`browse.js:33`). No
Douglas code reads the selected vehicle to evaluate anything (read from
`browse.js`; not run in a browser).

## E6. Camping listing filters in Douglas

- `v2/explore/trail-seasons.js:27`: `camping()` returns records whose
  `site_type` is `CAMPGROUND` only. The HORSE CAMP record is not in the camping
  list.
- `v2/explore/browse.js:46`: the detail renderer returns early for any record
  that is not a trail and whose `site_type` is not `CAMPGROUND`, `TRAILHEAD` or
  `DISPERSED_AREA`. The two PICNIC SITE records that carry "Overnight use
  prohibited." therefore do not reach this detail (read from code; not run in a
  browser).

## E7. Callers of the trip evaluator

`v2/index.html:8` loads `trip-rules.js` and `trust.js`.
`v2/explore/capabilities.js:16` applies `Trust.applyRules` then
`TripRules.evaluate` to every `overnight_inventory` place, de-duplicated by
`ridb_facility_id` (`capabilities.js:9-11`). Tests exercising these:
`v2/pipeline/tests/trust.test.cjs`, `staleness.test.cjs`,
`explore-capabilities.test.cjs`. The root legacy site has its own
`trip-rules.js`, which M7 does not touch.

## E8. Pipeline producers of overnight data

- `07_build_dispersed_corridors.py:48-49` builds the "possible" area from land
  polygons whose `manager` is `USFS` or `BLM`; `:57` keeps only roads whose
  `access_status` is `designated_open` for the evaluated trip; `:59` buffers by
  `road_buffer_ft`; `:83-84` take trip dates from the environment, defaulting to
  today.
- `09_reviewed_sites.py:10` fixes five claim names; `:39` hard-codes a 30-day
  review age; `:42` requires `sleeping_setup == "inside_vehicle"`; `:13` and
  `:39` read today's date; `:51` writes `camping_permission:
  "supported_for_trip"`.
- `02_fetch_mvum_roads.py:16`, `:29-30` write a trip-scoped `access_status` and
  `evaluated_trip` into published road features (register N8).
- `lib/rules.py:12-13` matches rules by place ID or by upper-cased road name.

## E9. Display sizes relevant to budgets

Aspen display: `dispersed_corridors` 709,990; `mvum_roads` 417,055;
`fire_restriction_stage` 796; `reviewed_sites` 91; `lodging_developed` 94;
`index.json` 6,366. Douglas display: `recreation` 33,769; `roads` 208,201;
`index.json` 3,709.

## E10. Numbering in the drafts M7 follows

M5 draft (`2c329e3`): rules R76–R85. M6 draft (`82a3c84`): rules R100–R119,
invariant sets TG, AE, RL1–RL8, PC1–PC14, LOCKED items L1–L6, decisions
M6-D1–M6-D16, material risks MR1–MR7.

## E11. Research pull requests read (all unreviewed drafts)

Read with `git show` from the local remote-tracking branches; branch names were
taken from `gh pr view <n> --json headRefName`.

| PR | Branch | Used for |
|---|---|---|
| #35 | `research/m7-orders-model` (`7d00426`) | Orders as entities, scope as stated, supersession, expiry, status observations, coverage example |
| #15 | `docs/research-drafts` (`83f15a3`) | `docs/research/m7-camping/M7-camping-evidence-model-draft.md` and the Hermes overnight-sources report: decomposition of the overnight question, scope levels, precedence, hard-coded behaviour list, risks, test ideas |
| #29 | `research/m8-rampart-worked-example` (`c781777`) | Model gaps: day use versus overnight, setup constraints, trailer fit, conflicting readings, two instruments |
| #20 | `docs/rampart-day-use-scenario` | Scenario B and its hammock line |

Every fact these drafts state about the web (orders, dates, fire status) was
retrieved by an agent, not reviewed, and is not re-checked here.
