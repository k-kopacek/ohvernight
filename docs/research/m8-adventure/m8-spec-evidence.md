DRAFT — evidence log for the M8 specification draft. Unreviewed research record, not product truth.

# M8 specification evidence log

Measured by the coordinator's worker on 2026-10-20 from committed files at
`origin/main` `3965dbf` (PR #39 merged). Read-only. No network request was made
to any publisher. No browser was run: Chrome is not installed on the
measuring machine, so the CDP byte counts that CI measures ("map usable",
"every default-on layer") were not re-measured here and are cited only as the
limits CI enforces.

Each entry gives the command or file read, and the result.

## E1. Explore capabilities per region

`v2/regions/<id>/explore.json` `capabilities`:

| Capability | Aspen | Douglas County |
|---|---|---|
| `trip_planner` | true | false |
| `adventure_pilot` | true | false |
| `trail_search` | true | true |
| `trail_season_check` | false | true |
| `gpx_export` | false | true |
| `saved_list` | false | true |
| `region_extras` | false | true |

Aspen `landing.title` is "Choose your adventure."; its lead says listings and
trails are shown "by straight-line distance". `trip_defaults` arrive
2027-01-15, depart 2027-01-17.

## E2. Fact coverage per region

`v2/regions/<id>/region.json` `fact_coverage.<dimension>.state`:

| Dimension | Aspen | Douglas County |
|---|---|---|
| `ownership` | context | context |
| `public_access` | none | none |
| `camping_permission` | none | none |
| `closures` | none | none |
| `restrictions` | reviewed_partial | none |
| `road_access` | context | context |
| `trail_access` | context | context |
| `recreation_permission` | none | none |

## E3. Aspen overnight inventory read by the pilot planner

`v2/overnight-options.json` (7,321 bytes): 5 places — 3 `campground`, 1
`dispersed`, 1 `lodging`. `v2/ridb-options.json` (7,920 bytes): 4 places, all
`campground`. Curated flags: `silverbar` `tent_only: true`; `lincolncreek`
`requires_high_clearance: true`, `stay_limit_days: 5`. `v2/destinations.json`
(1,163 bytes): 4 `resorts`, the pilot's "Mountain" input.

## E4. Douglas recreation-site records

`v2/regions/douglas-co/display/recreation.geojson` (33,769 bytes): 36 features
by source `site_type`: TRAILHEAD 17, CAMPGROUND 5, PICNIC SITE 5, RECREATION
RESIDENCE 3, TARGET RANGE 1, HORSE CAMP 1, DOCUMENTARY SITE 1, OBSERVATION
SITE 1.

## E5. Trail display features

Aspen `display/trails.geojson`: 123 features, 856,223 bytes. Douglas
`display/trails.geojson`: 102 features, 877,958 bytes. Both are source
segments (no user-facing trail identity before M6).

## E6. Pilot assembly behaviour

- `v2/trail-discovery.js:4-9` `matches()`: a trail matches an activity when the
  source's `managed` or `accpt` string for it is non-empty.
- `v2/trail-discovery.js:28-38`: `nearbyTrails()` keeps trails within 5
  straight-line miles, up to 3, de-duplicated by trail number or ID plus name;
  `adventureOptions()` pairs campground and dispersed places with them and
  sorts excluded places last, then by nearest straight-line distance.
- `v2/explore/capabilities.js:43`: dialog titled "Camping and trails by
  straight-line distance"; `:59` submit "Find my adventure →"; `:83` "What has
  been checked?"; `:87` stay type inside a collapsed "Filters" panel; `:89`
  saved slots headed "PLAN A" and "BACKUP"; `:90` list sorted excluded last,
  then straight-line distance from the chosen mountain; `:32` vehicle keys
  `passenger_car`, `high_clearance`, `motorhome`; `:117` an outbound "Open
  directions ↗" link.
- `v2/explore/browse.js:27,32,33`: Douglas activity, dates and "Camping
  vehicle" inside a collapsed "Filters" panel; `:54,58` straight-line listings
  within 5 miles, each row "connection unverified".

## E7. Module sizes (bytes, unminified)

`v2/explore/capabilities.js` 15,687; `v2/explore/browse.js` 13,790;
`v2/trip-rules.js` 4,369; `v2/trail-discovery.js` 2,611; `v2/trust.js` 3,291;
`v2/explore/shell.js` 21,648; `v2/explore/sheet.js` 8,326;
`v2/explore/map-adapter.js` 20,617.

## E8. Initial index and lazily loaded files

`display/index.json`: Aspen 6,366 bytes, Douglas 3,709 bytes.
`display/water-aliases.json` (outside the index, not requested during load):
Aspen 61,732, Douglas 88,729.

## E9. Computed research areas still on `main`

Aspen `display/dispersed_corridors.geojson` 709,990 bytes; every Aspen layer
in `explore.json` is `default_on: true`. PR #50 (interim MR1 removal from
discovery, head `dd8ad19`) is open, not merged.

## E10. Sheet structure after PR #39

`v2/explore/shell.js:28` sheet `<section id="explore-sheet">` with
`<header id="explore-sheet-header">`; `:83-95` one active list body
(`list-body`), `showList` restores the retained list and its scroll position,
`backToList` clears the map selection and returns focus. `v2/explore/sheet.js`
keeps the three states `collapsed`, `half`, `expanded` (`:3`). PR #39 moved
the header into normal flow with one scrolling body.

## E11. Draft and research inputs read (not re-checked, not product truth)

| Input | Ref | Head |
|---|---|---|
| M5 draft, PR #41 | `origin/k-kopacek/m5-spec-draft` | `2c329e3` |
| M6 draft, PR #42 | `origin/k-kopacek/m6-spec-draft` | `82a3c84` |
| M7 draft, PR #47, with MR1 audit and owner interim decision | `origin/k-kopacek/m7-spec-draft` | `b8471b1` |
| Rampart worked example, PR #29 | `origin/research/m8-rampart-worked-example` | `c781777` |
| Rampart day-use scenario B, PR #20 | `origin/docs/rampart-day-use-scenario` | `65cfd5d` |
| Research drafts incl. ranking options, PR #15 | `origin/docs/research-drafts` | `83f15a3` |

Last validator rule number in the M7 draft: R149 (reserved for an M7
amendment). M7 rules are R130–R148.

## E12. The two pilot coverage extents are not adjacent

Bounding boxes of `display/coverage.geojson` (longitude, latitude): Aspen
−107.050, 39.000 to −106.570, 39.260; Douglas County −105.329, 39.129 to
−104.661, 39.566. The gap between Aspen's east edge and Douglas County's west
edge is 1.241° of longitude, about 107 km at 39.2° N (computed, planar
approximation). No candidate can draw parts from both pilot packages, so a
cross-package candidate arises only with a third, adjacent region package, or
where a real-world feature continues past one package's own edge.
