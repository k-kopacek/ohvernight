DRAFT — evidence note for the M6 specification draft. Not approved. Repository evidence only.

# M6 specification evidence (repository measurements)

Measured on 2026-10-19 by the specification worker from committed files at
`origin/main` `c04f5d6`, with read-only Python over the canonical trail files.
No network request was made. Nothing here interprets a source's meaning; each
item states what the committed data contains. Lengths are computed with an
equirectangular approximation and are indicative only.

Files read:

- Aspen canonical trails: `v2/trails.geojson` (manifest `v2/regions/aspen/region.json`, layer `trails`).
- Douglas canonical trails: `v2/regions/douglas-co/research.json`, pointer `/layers/trails`.
- Trail fetch: `v2/pipeline/scripts/fetch_trails.py`; Douglas reuses its `normalize` (`v2/pipeline/scripts/fetch_douglas.py`).
- Browser trail handling: `v2/explore/trail-seasons.js`, `v2/explore/browse.js`, `v2/explore/capabilities.js`.

## T1. Shape of the current trail records

Both regions hold one source, the USDA Forest Service National Forest System
Trails layer (`EDW_TrailNFSPublishWithDataStatus_01/MapServer/0`). Every
feature carries exactly `id`, `name`, `trail_number`, `surface`,
`attribute_subset`, `allowed_terra_use`, `activities` and `evidence`.

- `id` is `usfs-trail-<objectid>` (`fetch_trails.py` line 27). Whether the
  publisher documents `objectid` as persistent is not established by anything
  in the repository. The M5 draft found that `OBJECTID` is a service row number
  for a different Forest Service-hosted service; that finding is not evidence
  about this layer.
- `activities` holds nine keys (hiking, horseback_riding, mountain_biking,
  motorcycling, atv, four_wheel_drive, snowshoeing, cross_country_skiing,
  snowmobiling), each with the source strings `managed`, `accpt`, `disc`,
  `restricted` copied verbatim (contract R29).
- `attribute_subset` is `TrailNFS_MGMT` on every feature in both regions.
- `evidence.verification_method` is `arcgis_rest_query`; `last_verified` is null.
- No transport record exists for either trail layer (register N1).

## T2. Counts

| | Aspen | Douglas County |
|---|---:|---:|
| Segments | 123 | 102 |
| LineString / MultiLineString | 111 / 12 | 91 / 11 |
| Distinct `trail_number` | 87 | 78 |
| Distinct `name` | 87 | 77 |
| `trail_number` values with more than one segment | 26 (62 segments) | 11 (35 segments) |
| … all of whose segments form one connected set (end points equal at six decimals) | 26 | 7 |
| `trail_number` values with a suffix (contains `.`) | 39 | 35 |
| Exact duplicate geometries | 0 | 0 |
| Total length (indicative) | 339 km | 414 km |
| Display artifact bytes (`display/trails.geojson`) | 856,223 | 877,958 |

## T3. The roadmap's Difficult Creek case

Aspen holds two segments named `DIFFICULT CREEK`, both `trail_number` `2146`:
`usfs-trail-8921819` and `usfs-trail-8923909`, about 5.3 km together. They
share an end point exactly at six decimals. Today they are two tappable
features. Under the grouping rule proposed in section 8 they are one trail.

## T4. Cases that test the "never merged" rules

- **Same name, touching, different route number.** Douglas `TURTLE MOUNTAIN`
  is `0770` (2 segments, connected) and `0770.E` (1 segment). An end point of
  `0770` equals an end point of `0770.E`. Name and geometry both match; the
  source numbers differ. This is the case where name plus continuity would
  wrongly merge two source routes.
- **Different names touching.** End points shared across different numbers:
  Aspen 3 points (for example `1987` SUNNYSIDE with `1988` SHADYSIDE; `1989`,
  `1989.1`, `1989.3`); Douglas 5 points (for example `0770.C`, `0770.D` and
  `0657`).
- **Same number, disconnected.** Douglas `1776` COLORADO: 10 segments in 3
  connected sets. `800` INDIAN CREEK: 4 segments in 4 sets, with smallest
  end-point gaps between sets of about 6 m, 0.5 km, 1.2 km, 1.9 km and 2.3 km.
  `0646` ARROWHEAD: 2 sets about 61 m apart. `0649` TROUT CREEK: 2 sets about
  1.2 km apart.
- **Inconsistent padding within one family.** Douglas carries `0681`,
  `0681.B`, `0681.C`, `0681.E` beside `681.D` and `681.F`; also `0627` beside
  `627.A`. No two values in Douglas collide after removing zero-padding.
- **A name that is a number.** Douglas has a trail named `787` with number `0787`.
- **Suffix families.** Douglas `0770` has nine suffixed numbers (`0770.A`–`0770.I`)
  with different names (for example `SKELETON`, `LONG HOLLOW BYPASS`, `WATSON PARK`).

## T5. Activity strings

- Aspen: 14 distinct non-null (field, value) pairs; Douglas 18.
- Trailing whitespace occurs: `01/01-12/31 ` (Aspen 78 values, Douglas 2).
- Two-window values occur: `01/01-06/14,10/16-12/31` (Aspen 3).
- Douglas `disc` (discouraged) `12/01-03/14` occurs 117 times; `managed`
  `12/01-03/14` 40 times; `accpt` `12/01-03/14` 38 times.
- No segment in either region has `motorcycling.restricted` together with a
  `managed` or `accpt` value.
- Aspen: 4 segments have no motorcycling value at all; Douglas: none.

## T6. How the browser uses them today

`trail-seasons.js` `season()` compares only `restricted` dates with trip dates
("Published restriction overlaps trip"); for `managed` or `accpt` it returns
"Source dates not interpreted — see details", and with no value "Use
permission unknown". `browse.js` lists trails by segment with `#<trail_number>`
and states that the Motor Vehicle Use Map and current agency orders govern
motor vehicle use. `capabilities.js` and `browse.js` produce straight-line
listings ("Camping nearby by straight-line distance", "Trails nearby by
straight-line distance") from segment geometry. GPX export writes one segment's
geometry with the description "County-clipped source geometry, not a navigable
route or access approval."

## T7. Research inputs read (all unmerged, unreviewed)

Read with `git show`; none checked out or merged.

| PR | Branch | Used for |
|---|---|---|
| #24 | `docs/m6-source-policy-proposal` | The source decision this draft locks on; candidate concepts and open questions |
| #33 | `research/m6-motorized-evidence-prototype` | Shape of per-vehicle-class designation records and date-window parsing states |
| #29 | `research/m8-rampart-worked-example` | Model gaps (conflicting readings, instruments, day use) |
| #20 | `docs/rampart-day-use-scenario` | Rampart scenario text; not on `main` |
| #35 | `research/m7-orders-model` | Orders as entities (M7 input) |
| — | `k-kopacek/m5-spec-draft` | M5 draft; its highest rule ID is R85 |
