# South Platte and Douglas padded-water integration measurements

Measured offline from the integrated canonical bundle and deterministic display artifacts. No new retrieval, rule, threshold, synthetic geometry or river-specific exception was used.

## South Platte River

- Logical group: `nhd-gnis-00201759`; GNIS `00201759`; source USGS NHD MapServer layer 6, identified by each preserved permanent identifier.
- Drawn members: 343; separate drawn lines: 343 (source-member lines, not inferred connected paths).
- Drawn length from canonical WGS84 geometry: 73.323267430090 km; artifact length 73.323 km. Rounded display coordinates are not used to compute the stored length (A8).
- Fraction: 0.964754892385, against unchanged 0.8; denominator 76.001964860517 km of perennial stream and artificial-path geometry. Exactly one logical group, all drawn members GNIS `00201759`, no North Fork `00183164` member.
- Drawn portion outside county: 64.142066540640 km, clipped to county.buffer(0.005).
- Connectivity-only members: 0; connector members: 0; synthetic members: zero.
- [All 349 South Platte source records and their treatment](south-platte-integrated-members.csv): every source ID, raw page, raw page SHA-256 and object ID; 343 are drawn (342 artificial paths plus one perennial stream), five artificial paths are undrawn, one canal is excluded from both drawing and connectivity.
- The canal-coded segment `nhd-B2C95CF5-10D7-437D-BC7B-ED86AF86528C` (source `{B2C95CF5-10D7-437D-BC7B-ED86AF86528C}`, fcode 33601) is 0.283097769969 km long and never drawn or used for connectivity. Its exclusion breaks source-graph continuity below Chatfield dam; the five disconnected artificial paths (2.678697430427 km) have no perennial seed and stay undrawn. No line fills that omission.

## Padding side effects

Canonical additions: 375 flowlines and 85 waterbodies. Existing geometries grew: 94 flowlines and 11 waterbodies; no removed or renamed feature. All 4,954 comparisons are EXPLAINED. Every pre-existing ID and its legacy IDs remain unchanged.
- [All 460 added canonical features](douglas-padding-added-features.csv), named or explicitly unnamed, includes display treatment and saved raw-page traceability.

New displayed groups and waterbodies (every newly introduced display identity):

| Kind | Display ID | Source name | Already partly held before padding |
|---|---|---|---|
| group | `nhd-gnis-00183502` | Wigwam Creek | no |
| group | `nhd-gnis-00183517` | Brush Creek | no |
| group | `nhd-gnis-00183525` | Gunbarrel Creek | no |
| group | `nhd-gnis-00201759` | South Platte River | yes |
| waterbody | `nhd-117819355` | (unnamed) | no |
| waterbody | `nhd-117822693` | Eaglewatch Lake | no |
| waterbody | `nhd-117822699` | Blackrock Lake | no |
| waterbody | `nhd-117822713` | (unnamed) | no |
| waterbody | `nhd-117822891` | Ladybug Lake | no |
| waterbody | `nhd-117822919` | (unnamed) | no |
| waterbody | `nhd-117825121` | Palmer Lake | no |
| waterbody | `nhd-117848417` | (unnamed) | no |
| waterbody | `nhd-117848419` | (unnamed) | no |
| waterbody | `nhd-120654810` | Inverness Reservoir | no |
| waterbody | `nhd-1711BC21-D607-41CD-B841-7D0E7C4A4F5A` | South Platte Reservoir | no |

Padding introduces 4 stream groups and 11 waterbodies under unchanged selection, for totals 39 and 43. New flowline GNIS identities not previously held: 00182569, 00183164, 00183331, 00183333, 00183342, 00183502, 00183517, 00183525, 00183668, 00183691, 00185048, 00185113, 00202936. Padding therefore also absorbs unrelated named streams and waterbodies in the strip; it is a uniform water-extent rule, not a South Platte exception.

## Preservation and validation

- [Unchanged-file hashes](m4b-integration-preservation-hashes.json) pin all 21 Aspen files, Aspen non-water layers and every Douglas non-water canonical layer. Douglas non-water display artifacts also remain byte-identical in Git.
- The M4-A legacy-ID CSV remains unchanged; R68 checks alias mapping for the complete displayed membership.
- Added tests require one South Platte group, 343 source members, no foreign GNIS or canal membership, and failure of the real-data county-only fixture with zero padding.
- Updated Douglas expectation pins: groups 35 → 39; displayed waterbodies 32 → 43; South Platte pending → confirmed; production pending marker present → absent. Both approved Douglas manifest strings are pinned exactly; negative pending-marker fixtures retain their historical cases explicitly.

## Byte budgets

{
  "aspen": {
    "map_usable": 382642,
    "default_on_total": 3541696,
    "water_display": 819378
  },
  "douglas-co": {
    "map_usable": 463604,
    "default_on_total": 2866450,
    "water_display": 1076496
  }
}

## Reproduction

- Start at reviewed pre-integration commit 45f877de8cdf60ecee1ebc1afe2cfd1ed39ce540 with the validated saved tiled staging directory. Run the offline comparison and preservation gates before applying; use apply_m4a_water.py --douglas-padded --apply, recompute canonical group_id via group_flowlines, and rebuild Douglas displays.
- Length and fraction use lib.water.geodesic_length_km over canonical drawn members; outside length uses each drawn member geometry.difference(county), retaining only line components; byte totals follow test_display_budgets.py exactly.
- Member CSV uses saved douglas-co-flowline-pages/page-NNNN.json matched by permanent_identifier, without publishing raw geometry or page contents.
- Independent review, owner selection-report reading and iPhone acceptance, GitHub CI and exact-head human merge approval remain.
