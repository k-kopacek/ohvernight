# Unnamed-waterbody size threshold comparison: 0.5 ha versus 2 ha

In Aspen, the approved 2 ha threshold displays 46 of 514 canonical waterbodies (43 named, 3 unnamed); a 0.5 ha threshold would display 90 (47 unnamed), which is 44 more. In Douglas County, 2 ha displays 32 of 2135 (18 named, 14 unnamed); 0.5 ha would display 127 (109 unnamed), which is 95 more. Projected compact GeoJSON size for the displayed waterbodies is 71,994 bytes (Aspen) and 119,627 bytes (Douglas) at 2 ha, and 111,896 and 227,769 bytes at 0.5 ha. Named waterbodies are unaffected by the threshold in both regions. The source `area_sqkm` property is stored to only three decimals (0.001 km2 = 0.1 ha), so areas are coarse near 0.5 ha.

## Decision for the owner

Choosing 0.5 ha instead of 2 ha would add 44 unnamed perennial waterbodies in Aspen (from 3 to 47 unnamed; total displayed 46 to 90) and 95 in Douglas County (from 14 to 109; total 32 to 127). The projected display bytes would change by +39,902 (Aspen) and +108,142 (Douglas). No named waterbody, intermittent exclusion, category-unknown exclusion or source-type exclusion changes. This report states the effect only and does not recommend a change; the approved provisional value remains 0.02 km2.

## 1. Counts

Bucket notes: "intermittent" is any lake, pond or reservoir whose `hydro_category` is intermittent (this includes reservoir fcode 43614, which the spec also lists as an ineligible code). "Source type" covers ineligible reservoir codes other than 43614, swamp/marsh (466) and any other ftype. A lake or eligible reservoir that is unnamed and under the threshold is counted only under "below threshold".

### Aspen

| Bucket | 0.5 ha | 2 ha |
|---|---|---|
| Named included | 43 | 43 |
| Unnamed included | 47 | 3 |
| **Total displayed** | 90 | 46 |
| Excluded: unnamed, below threshold | 322 | 366 |
| Excluded: intermittent, named | 0 | 0 |
| Excluded: intermittent, unnamed | 36 | 36 |
| Excluded: category-unknown lake (39000) | 3 | 3 |
| Excluded: source type | 63 | 63 |
| Excluded: other | 0 | 0 |
| **Total waterbodies** | 514 | 514 |

Exclusions by `fcode` (all non-displayed features other than the below-threshold bucket; identical at both thresholds):

| Bucket | ftype | fcode | hydro_category | Count |
|---|---|---|---|---|
| Excluded: intermittent, unnamed | 390 | 39001 | intermittent | 36 |
| Excluded: source type | 436 | 43624 | unknown | 5 |
| Excluded: source type | 466 | 46600 | unknown | 58 |
| Excluded: category-unknown lake (39000) | 390 | 39000 | unknown | 3 |

Below-threshold unnamed features by `fcode`:

- 0.5 ha: ftype 390/fcode 39004: 322
- 2 ha: ftype 390/fcode 39004: 364, ftype 390/fcode 39009: 2

### Douglas

| Bucket | 0.5 ha | 2 ha |
|---|---|---|
| Named included | 18 | 18 |
| Unnamed included | 109 | 14 |
| **Total displayed** | 127 | 32 |
| Excluded: unnamed, below threshold | 576 | 671 |
| Excluded: intermittent, named | 15 | 15 |
| Excluded: intermittent, unnamed | 1389 | 1389 |
| Excluded: category-unknown lake (39000) | 0 | 0 |
| Excluded: source type | 28 | 28 |
| Excluded: other | 0 | 0 |
| **Total waterbodies** | 2135 | 2135 |

Exclusions by `fcode` (all non-displayed features other than the below-threshold bucket; identical at both thresholds):

| Bucket | ftype | fcode | hydro_category | Count |
|---|---|---|---|---|
| Excluded: intermittent, unnamed | 390 | 39001 | intermittent | 1389 |
| Excluded: source type | 436 | 43601 | unknown | 1 |
| Excluded: source type | 436 | 43612 | unknown | 6 |
| Excluded: source type | 436 | 43624 | unknown | 20 |
| Excluded: source type | 466 | 46600 | unknown | 1 |
| Excluded: intermittent, named | 390 | 39001 | intermittent | 13 |
| Excluded: intermittent, named | 390 | 39005 | intermittent | 2 |

Below-threshold unnamed features by `fcode`:

- 0.5 ha: ftype 390/fcode 39004: 573, ftype 390/fcode 39011: 1, ftype 436/fcode 43613: 2
- 2 ha: ftype 390/fcode 39004: 665, ftype 390/fcode 39011: 4, ftype 436/fcode 43613: 2

## 2. Every named waterbody

### Aspen (43 named)

| Name | fcode | hydro_category | Area (ha) | Elevation (m) | Shown at 0.5 ha | Shown at 2 ha | Reason if not shown |
|---|---|---|---|---|---|---|---|
| American Lake | 39004 | perennial | 1.4 |  | yes | yes |  |
| Anderson Lake | 39004 | perennial | 3.6 |  | yes | yes |  |
| Cathedral Lake | 39004 | perennial | 6.9 |  | yes | yes |  |
| Christenson Reservoir | 39004 | perennial | 0.8 |  | yes | yes |  |
| Copper Lake | 39009 | perennial | 3.1 | 3450.6 | yes | yes |  |
| Crater Lake | 39009 | perennial | 7.2 | 3071.2 | yes | yes |  |
| Deadman Lake | 39004 | perennial | 0.8 |  | yes | yes |  |
| Elk Creek Reservoir Number 2 | 39004 | perennial | 0.3 |  | yes | yes |  |
| Elko Lake | 39004 | perennial | 1.1 |  | yes | yes |  |
| Emerald Lake | 39009 | perennial | 4.9 | 3186.7 | yes | yes |  |
| Granite Lakes | 39004 | perennial | 2.5 |  | yes | yes |  |
| Granite Lakes | 39004 | perennial | 1.2 |  | yes | yes |  |
| Grizzly Lake | 39004 | perennial | 3.3 |  | yes | yes |  |
| Grizzly Reservoir | 39004 | perennial | 12.7 |  | yes | yes |  |
| Henschel Lake | 39004 | perennial | 0.5 |  | yes | yes |  |
| Independence Lake | 39004 | perennial | 3.2 |  | yes | yes |  |
| Jack Lake | 39004 | perennial | 0.9 |  | yes | yes |  |
| Linkins Lake | 39004 | perennial | 4.6 |  | yes | yes |  |
| Lost Man Lake | 39004 | perennial | 5.8 |  | yes | yes |  |
| Lost Man Reservoir | 39004 | perennial | 2.5 |  | yes | yes |  |
| Marolt Reservoir | 39009 | perennial | 1.8 | 2599.0 | yes | yes |  |
| Maroon Lake | 39009 | perennial | 6.5 | 2920.0 | yes | yes |  |
| Midway Lake | 39004 | perennial | 2.0 |  | yes | yes |  |
| Petroleum Lake | 39004 | perennial | 5.0 |  | yes | yes |  |
| Ptarmigan Lake | 39004 | perennial | 2.1 |  | yes | yes |  |
| Ruby Lakes | 39004 | perennial | 1.4 |  | yes | yes |  |
| Ruby Lakes | 39004 | perennial | 0.5 |  | yes | yes |  |
| Sawyer Lake | 39004 | perennial | 4.4 |  | yes | yes |  |
| Scott Lake | 39004 | perennial | 1.5 |  | yes | yes |  |
| Silver Dollar Pond | 39004 | perennial | 0.0 |  | yes | yes |  |
| Sioux Lake | 39004 | perennial | 1.1 |  | yes | yes |  |
| Snowmass Lake | 39004 | perennial | 33.5 |  | yes | yes |  |
| Tabor Lake | 39004 | perennial | 2.2 |  | yes | yes |  |
| Tagerts Lake | 39004 | perennial | 1.8 |  | yes | yes |  |
| Taylor Lake | 39009 | perennial | 7.7 | 3518.6 | yes | yes |  |
| Truro Lake | 39004 | perennial | 2.7 |  | yes | yes |  |
| Warren Lake | 39004 | perennial | 4.9 |  | yes | yes |  |
| Warren Lakes | 39004 | perennial | 7.8 |  | yes | yes |  |
| Warren Lakes | 39004 | perennial | 3.2 |  | yes | yes |  |
| Weller Lake | 39004 | perennial | 3.5 |  | yes | yes |  |
| Whites Lake | 39009 | perennial | 0.8 | 2827.9 | yes | yes |  |
| Wildcat Reservoir | 39004 | perennial | 21.2 |  | yes | yes |  |
| Willow Lake | 39009 | perennial | 8.7 | 3595.4 | yes | yes |  |

### Douglas (33 named)

| Name | fcode | hydro_category | Area (ha) | Elevation (m) | Shown at 0.5 ha | Shown at 2 ha | Reason if not shown |
|---|---|---|---|---|---|---|---|
| Allis Reservoir | 39004 | perennial | 2.1 |  | yes | yes |  |
| Aurora-Rampart Reservoir | 39009 | perennial | 26.9 | 1802.6 | yes | yes |  |
| Barney Bird Reservoir Number One | 39004 | perennial | 3.6 |  | yes | yes |  |
| Cantrill Reservoir | 39001 | intermittent | 0.2 |  | no | no | intermittent (fcode 39001) |
| Chatfield Lake | 39009 | perennial | 562.2 | 1655.7 | yes | yes |  |
| Cheesman Lake | 39009 | perennial | 358.1 | 2085.4 | yes | yes |  |
| Circle 2 Ranch Reservoir Number 1 | 39009 | perennial | 4.9 | 1886.7 | yes | yes |  |
| Franktown Parker FPA-2 Reservoir | 39001 | intermittent | 4.8 |  | no | no | intermittent (fcode 39001) |
| Franktown Parker FPA-4 Reservoir | 39001 | intermittent | 3.8 |  | no | no | intermittent (fcode 39001) |
| Franktown Parker FPA-5 Reservoir | 39004 | perennial | 3.7 |  | yes | yes |  |
| Franktown Parker FPB-1 Reservoir | 39005 | intermittent | 7.4 | 1815.1 | no | no | intermittent (fcode 39005) |
| Franktown Parker FPE-7 Reservoir | 39001 | intermittent | 2.7 |  | no | no | intermittent (fcode 39001) |
| Franktown Parker FPE-8 Reservoir | 39001 | intermittent | 8.3 |  | no | no | intermittent (fcode 39001) |
| Franktown Parker FPM-1 Reservoir | 39001 | intermittent | 0.3 |  | no | no | intermittent (fcode 39001) |
| Franktown Parker FPP-1 Reservoir | 39001 | intermittent | 3.8 |  | no | no | intermittent (fcode 39001) |
| Franktown Parker FPR-1 Reservoir | 39005 | intermittent | 2.4 | 1942.5 | no | no | intermittent (fcode 39005) |
| Franktown Parker FPS-1 Reservoir | 39004 | perennial | 0.7 |  | yes | yes |  |
| Franktown Parker FPW-1 Reservoir | 39001 | intermittent | 4.2 |  | no | no | intermittent (fcode 39001) |
| J O Hill Reservoir | 39004 | perennial | 7.5 |  | yes | yes |  |
| McLellan Reservoir | 39009 | perennial | 77.4 | 1673.0 | yes | yes |  |
| Nelson Reservoir | 39001 | intermittent | 0.1 |  | no | no | intermittent (fcode 39001) |
| Pinery Reservoir | 39009 | perennial | 9.6 | 1862.3 | yes | yes |  |
| Platte Canyon Reservoir | 39009 | perennial | 21.3 | 1686.8 | yes | yes |  |
| Rueter-Hess Reservoir | 43619 | unknown | 87.5 |  | yes | yes |  |
| Stevens Reservoir Number 2 and 3 | 39001 | intermittent | 2.4 |  | no | no | intermittent (fcode 39001) |
| Strontia Springs Reservoir | 39004 | perennial | 32.8 |  | yes | yes |  |
| Wakeman Reservoir | 39004 | perennial | 5.8 |  | yes | yes |  |
| Waucondah Reservoir | 39004 | perennial | 7.4 |  | yes | yes |  |
| West Cherry Creek Detention Number 11 Reservoir | 39001 | intermittent | 7.7 |  | no | no | intermittent (fcode 39001) |
| West Cherry Creek Detention Number 7 Reservoir | 39004 | perennial | 1.8 |  | yes | yes |  |
| West Cherry Creek Detention Number 8 Reservoir | 39001 | intermittent | 0.4 |  | no | no | intermittent (fcode 39001) |
| West Cherry Creek Detention Number 9 Reservoir | 39001 | intermittent | 2.4 |  | no | no | intermittent (fcode 39001) |
| Wolhurst Lake | 39004 | perennial | 3.4 |  | yes | yes |  |

## 3. Aspen: unnamed perennial waterbodies between 0.5 and 2 ha

Count: 44 (unnamed, displayed at 0.5 ha but not at 2 ha; lakes/ponds perennial or eligible reservoirs; area_sqkm 0.005 to under 0.020). Centroid is the vertex average of the first outer ring. Distance is great-circle to the nearest named waterbody displayed at 2 ha. Sorted by area, descending.

| id | fcode | Area (ha) | Elevation (m) | Centroid lat | Centroid lon | Km to nearest named displayed waterbody centroid |
|---|---|---|---|---|---|---|
| nhd-72962706 | 39004 | 1.7 |  | 39.1764 | -106.8032 | 4.37 |
| nhd-72971650 | 39004 | 1.6 |  | 39.2588 | -106.6654 | 1.75 |
| nhd-72971646 | 39004 | 1.6 |  | 39.2645 | -106.6536 | 1.78 |
| nhd-72964618 | 39004 | 1.4 |  | 39.1467 | -107.0546 | 3.67 |
| nhd-65879795 | 39009 | 1.4 | 3693.0 | 39.0122 | -106.9498 | 1.07 |
| nhd-72974976 | 39004 | 1.3 |  | 39.0489 | -106.6572 | 1.46 |
| nhd-72968818 | 39004 | 1.2 |  | 39.2240 | -106.9222 | 2.83 |
| nhd-72972334 | 39004 | 1.1 |  | 39.1510 | -106.5831 | 1.26 |
| nhd-72981112 | 39004 | 1.1 |  | 39.2468 | -106.6538 | 0.43 |
| nhd-72968822 | 39004 | 1.1 |  | 39.2234 | -106.9276 | 2.50 |
| nhd-72964606 | 39004 | 0.9 |  | 39.1676 | -107.0546 | 5.84 |
| nhd-72962752 | 39004 | 0.9 |  | 39.1327 | -106.7576 | 0.37 |
| nhd-72971114 | 39004 | 0.9 |  | 39.1109 | -106.9689 | 0.43 |
| nhd-65878197 | 39004 | 0.9 |  | 39.0096 | -106.7554 | 0.73 |
| nhd-72962584 | 39004 | 0.8 |  | 39.2483 | -106.8548 | 6.18 |
| nhd-72974950 | 39004 | 0.8 |  | 39.0540 | -106.6475 | 1.06 |
| nhd-72971110 | 39004 | 0.8 |  | 39.1112 | -106.9737 | 0.84 |
| nhd-72968826 | 39004 | 0.8 |  | 39.2212 | -106.9231 | 2.96 |
| nhd-72968842 | 39004 | 0.8 |  | 39.2063 | -106.9819 | 3.97 |
| nhd-72968808 | 39009 | 0.8 | 2468.9 | 39.2380 | -106.9779 | 2.42 |
| nhd-72962676 | 39004 | 0.7 |  | 39.1910 | -106.8428 | 4.05 |
| nhd-72962588 | 39004 | 0.7 |  | 39.2236 | -106.8589 | 3.73 |
| nhd-72974992 | 39004 | 0.7 |  | 39.0290 | -106.6452 | 0.79 |
| nhd-72974966 | 39004 | 0.7 |  | 39.0514 | -106.6855 | 1.83 |
| nhd-72962604 | 39004 | 0.7 |  | 39.2086 | -106.8210 | 5.91 |
| nhd-72968820 | 39004 | 0.7 |  | 39.2239 | -106.9261 | 2.57 |
| nhd-72978728 | 39004 | 0.7 |  | 39.0648 | -107.0484 | 5.48 |
| nhd-72981196 | 39004 | 0.6 |  | 39.1463 | -106.6648 | 1.73 |
| nhd-72972306 | 39004 | 0.6 |  | 39.1851 | -106.6050 | 1.03 |
| nhd-72962748 | 39004 | 0.6 |  | 39.1459 | -106.8091 | 5.05 |
| nhd-65879789 | 39004 | 0.6 |  | 39.0272 | -106.9659 | 3.24 |
| nhd-72968374 | 39004 | 0.6 |  | 39.0226 | -106.8491 | 0.78 |
| nhd-72968850 | 39004 | 0.6 |  | 39.1951 | -106.8885 | 0.47 |
| nhd-72974986 | 39004 | 0.6 |  | 39.0328 | -106.6399 | 0.76 |
| nhd-72962614 | 39004 | 0.5 |  | 39.2078 | -106.7783 | 4.50 |
| nhd-72972348 | 39004 | 0.5 |  | 39.1255 | -106.6020 | 1.19 |
| nhd-72981154 | 39004 | 0.5 |  | 39.2031 | -106.6676 | 4.59 |
| nhd-72962660 | 39004 | 0.5 |  | 39.1962 | -106.8371 | 4.44 |
| nhd-72969572 | 39004 | 0.5 |  | 39.0054 | -106.6190 | 0.55 |
| nhd-72962690 | 39004 | 0.5 |  | 39.1837 | -106.8528 | 3.53 |
| nhd-72974956 | 39004 | 0.5 |  | 39.0528 | -106.6603 | 1.15 |
| nhd-72962696 | 39004 | 0.5 |  | 39.1829 | -106.8076 | 4.86 |
| nhd-72981162 | 39004 | 0.5 |  | 39.1763 | -106.6928 | 2.76 |
| nhd-72974990 | 39004 | 0.5 |  | 39.0296 | -106.6310 | 0.59 |

## 4. Douglas County: 30 largest unnamed perennial waterbodies between 0.5 and 2 ha

Count in this range: 95; shown below: 30; remaining: 65.

| id | fcode | Area (ha) | Elevation (m) | Centroid lat | Centroid lon | Km to nearest named displayed waterbody centroid |
|---|---|---|---|---|---|---|
| nhd-117821201 | 39004 | 1.8 |  | 39.2397 | -104.9591 | 3.16 |
| nhd-117822909 | 39004 | 1.7 |  | 39.5593 | -105.0181 | 1.20 |
| nhd-117819385 | 39004 | 1.6 |  | 39.4843 | -105.0059 | 6.49 |
| nhd-117822715 | 39004 | 1.6 |  | 39.5630 | -105.0525 | 1.33 |
| nhd-120655816 | 39004 | 1.5 |  | 39.3317 | -104.7307 | 5.01 |
| nhd-117819459 | 39004 | 1.5 |  | 39.4532 | -105.0797 | 1.31 |
| nhd-117819437 | 39004 | 1.5 |  | 39.4592 | -105.0613 | 1.23 |
| nhd-117819393 | 39004 | 1.4 |  | 39.4838 | -105.0179 | 5.66 |
| nhd-117819381 | 39004 | 1.3 |  | 39.4850 | -105.0182 | 5.74 |
| nhd-117819335 | 39004 | 1.3 |  | 39.4987 | -105.0152 | 6.19 |
| nhd-120655564 | 39004 | 1.2 |  | 39.3864 | -104.7873 | 3.60 |
| nhd-120656384 | 39004 | 1.2 |  | 39.1863 | -104.6894 | 6.51 |
| nhd-117793975 | 39004 | 1.1 |  | 39.2709 | -104.8514 | 10.31 |
| nhd-117792553 | 39004 | 1.1 |  | 39.3867 | -104.8633 | 9.98 |
| nhd-120656283 | 39004 | 1.1 |  | 39.2233 | -104.7644 | 1.17 |
| nhd-120656359 | 39004 | 1.1 |  | 39.1913 | -104.7599 | 3.17 |
| nhd-117819383 | 39004 | 1.1 |  | 39.4848 | -105.0981 | 1.13 |
| nhd-117819469 | 39004 | 1.1 |  | 39.4467 | -105.0772 | 1.01 |
| nhd-120655832 | 39004 | 1.1 |  | 39.3270 | -104.6983 | 6.83 |
| nhd-117819391 | 39004 | 1.1 |  | 39.4838 | -105.0727 | 1.32 |
| nhd-3af3a63e-8a13-480a-8693-2e5569fee39e | 39011 | 1.1 |  | 39.5476 | -104.8529 | 7.19 |
| nhd-117822705 | 39004 | 1.0 |  | 39.5653 | -105.0280 | 0.82 |
| nhd-120656220 | 39004 | 1.0 |  | 39.2542 | -104.6717 | 7.93 |
| nhd-120655011 | 39004 | 1.0 |  | 39.5138 | -104.7974 | 4.12 |
| nhd-117844323 | 39004 | 0.9 |  | 39.2312 | -105.2250 | 7.46 |
| nhd-117800473 | 39004 | 0.9 |  | 39.2630 | -104.8916 | 8.13 |
| nhd-117792393 | 39004 | 0.9 |  | 39.3841 | -104.8644 | 10.04 |
| nhd-120654851 | 39004 | 0.9 |  | 39.5583 | -104.7845 | 8.92 |
| nhd-120655215 | 39004 | 0.9 |  | 39.4615 | -104.7663 | 2.31 |
| nhd-120655711 | 39004 | 0.9 |  | 39.3574 | -104.7266 | 2.68 |

## 5. Twenty largest unnamed waterbodies included at 2 ha

### Aspen (of 3)

| id | fcode | Area (ha) | Elevation (m) | Centroid lat | Centroid lon |
|---|---|---|---|---|---|
| nhd-72968834 | 39004 | 4.0 |  | 39.2076 | -106.9648 |
| nhd-72978716 | 39004 | 2.2 |  | 39.0781 | -107.0021 |
| nhd-72964646 | 39004 | 2.2 |  | 39.1332 | -107.0125 |

### Douglas (of 14)

| id | fcode | Area (ha) | Elevation (m) | Centroid lat | Centroid lon |
|---|---|---|---|---|---|
| nhd-117822925 | 39004 | 18.2 |  | 39.5037 | -105.0808 |
| nhd-13e573b1-c56c-49c5-9298-be551598d368 | 39011 | 8.7 |  | 39.5386 | -104.8493 |
| nhd-120656304 | 39004 | 8.4 |  | 39.2116 | -104.7785 |
| nhd-117797753 | 39004 | 8.3 |  | 39.1631 | -105.1197 |
| nhd-d55467f0-7114-4faf-a083-e3aff252fd30 | 39011 | 5.4 |  | 39.5149 | -104.7767 |
| nhd-117822921 | 39004 | 4.8 |  | 39.5100 | -105.0778 |
| nhd-117822915 | 39004 | 2.9 |  | 39.5468 | -105.0425 |
| nhd-117822709 | 39004 | 2.8 |  | 39.5643 | -105.0498 |
| nhd-120655532 | 39009 | 2.7 | 1941.6 | 39.3986 | -104.6952 |
| nhd-34ab3d08-b638-4011-9e3d-167cd78fd4b5 | 39011 | 2.7 |  | 39.5466 | -104.8052 |
| nhd-117821223 | 39004 | 2.4 |  | 39.2280 | -104.9702 |
| nhd-117792557 | 39004 | 2.3 |  | 39.3849 | -104.8654 |
| nhd-117819415 | 39004 | 2.2 |  | 39.4722 | -105.0684 |
| nhd-120655625 | 39004 | 2.1 |  | 39.3748 | -104.7933 |

## 6. Suspicious structures retained, and intermittent named waterbodies

A name is not evidence of what a feature is. The lists below are CANDIDATES FOR A REVIEWED EXCLUSION ONLY. No feature is excluded by name; any exclusion must go through the reviewed exclusion list (8.5) with authoritative evidence and a recorded reason. The pattern matched (case-insensitive) was: detention, FP, treatment, sewage, tailings, pit, gravel, settling.

### Aspen: displayed at 2 ha with an infrastructure-like word in the name

None.

### Aspen: named waterbodies not displayed because they are intermittent

None.

### Douglas: displayed at 2 ha with an infrastructure-like word in the name

| Name | id | fcode | hydro_category | Area (ha) | Elevation (m) |
|---|---|---|---|---|---|
| West Cherry Creek Detention Number 7 Reservoir | nhd-120656489 | 39004 | perennial | 1.8 |  |

### Douglas: named waterbodies not displayed because they are intermittent

| Name | id | fcode | Area (ha) | Elevation (m) |
|---|---|---|---|---|
| Cantrill Reservoir | nhd-117821191 | 39001 | 0.2 |  |
| Franktown Parker FPA-2 Reservoir | nhd-120656264 | 39001 | 4.8 |  |
| Franktown Parker FPA-4 Reservoir | nhd-120656405 | 39001 | 3.8 |  |
| Franktown Parker FPB-1 Reservoir | nhd-120654954 | 39005 | 7.4 | 1815.1 |
| Franktown Parker FPE-7 Reservoir | nhd-120656502 | 39001 | 2.7 |  |
| Franktown Parker FPE-8 Reservoir | nhd-120656369 | 39001 | 8.3 |  |
| Franktown Parker FPM-1 Reservoir | nhd-120655468 | 39001 | 0.3 |  |
| Franktown Parker FPP-1 Reservoir | nhd-120654985 | 39001 | 3.8 |  |
| Franktown Parker FPR-1 Reservoir | nhd-120655756 | 39005 | 2.4 | 1942.5 |
| Franktown Parker FPW-1 Reservoir | nhd-120655704 | 39001 | 4.2 |  |
| Nelson Reservoir | nhd-117819511 | 39001 | 0.1 |  |
| Stevens Reservoir Number 2 and 3 | nhd-117800187 | 39001 | 2.4 |  |
| West Cherry Creek Detention Number 11 Reservoir | nhd-120656314 | 39001 | 7.7 |  |
| West Cherry Creek Detention Number 8 Reservoir | nhd-120656488 | 39001 | 0.4 |  |
| West Cherry Creek Detention Number 9 Reservoir | nhd-120656474 | 39001 | 2.4 |  |

## 7. Possibly useful water lost at 2 ha (objective signals only)

Only two objective signals are used: elevation above 10,000 ft, which is 3,048 m (Aspen only), and area between 1.0 and 2 ha. The lists are examples for the owner to judge. No claim is made that any of them is recreationally useful, accessible or open to the public.

### Aspen: unnamed perennial, 0.5 to 2 ha, above 10,000 ft (3,048 m): 1

Of the 44 Aspen features in the 0.5 to 2 ha range, 42 have no elevation value and cannot be tested by this signal. Of the two that have one, `nhd-65879795` is above the line and `nhd-72968808` (2,468.9 m, about 8,100 ft) is below it.

| id | fcode | Area (ha) | Elevation (m) | Elevation (ft, converted) | Centroid lat | Centroid lon | Km to nearest named displayed waterbody centroid |
|---|---|---|---|---|---|---|---|
| nhd-65879795 | 39009 | 1.4 | 3693.0 | 12,116 | 39.0122 | -106.9498 | 1.07 |

**Correction, 2026-10-07.** An earlier version of this report labelled every elevation column in feet and said no feature in this range was above 10,000 ft. The stored values are metres (`elevation_m`, specification amendment A3), so the comparison against 10,000 was made in the wrong unit. The elevation values themselves, and every count, area, byte projection and conclusion outside this subsection, are unchanged. Elevation still does not show that a water is useful, reachable or open to the public.

### Aspen: unnamed perennial, 1.0 to 2 ha: 10

| id | fcode | Area (ha) | Elevation (m) | Centroid lat | Centroid lon | Km to nearest named displayed waterbody centroid |
|---|---|---|---|---|---|---|
| nhd-72962706 | 39004 | 1.7 |  | 39.1764 | -106.8032 | 4.37 |
| nhd-72971650 | 39004 | 1.6 |  | 39.2588 | -106.6654 | 1.75 |
| nhd-72971646 | 39004 | 1.6 |  | 39.2645 | -106.6536 | 1.78 |
| nhd-72964618 | 39004 | 1.4 |  | 39.1467 | -107.0546 | 3.67 |
| nhd-65879795 | 39009 | 1.4 | 3693.0 | 39.0122 | -106.9498 | 1.07 |
| nhd-72974976 | 39004 | 1.3 |  | 39.0489 | -106.6572 | 1.46 |
| nhd-72968818 | 39004 | 1.2 |  | 39.2240 | -106.9222 | 2.83 |
| nhd-72972334 | 39004 | 1.1 |  | 39.1510 | -106.5831 | 1.26 |
| nhd-72981112 | 39004 | 1.1 |  | 39.2468 | -106.6538 | 0.43 |
| nhd-72968822 | 39004 | 1.1 |  | 39.2234 | -106.9276 | 2.50 |

### Douglas: unnamed perennial, 1.0 to 2 ha: 23

| id | fcode | Area (ha) | Elevation (m) | Centroid lat | Centroid lon | Km to nearest named displayed waterbody centroid |
|---|---|---|---|---|---|---|
| nhd-117821201 | 39004 | 1.8 |  | 39.2397 | -104.9591 | 3.16 |
| nhd-117822909 | 39004 | 1.7 |  | 39.5593 | -105.0181 | 1.20 |
| nhd-117819385 | 39004 | 1.6 |  | 39.4843 | -105.0059 | 6.49 |
| nhd-117822715 | 39004 | 1.6 |  | 39.5630 | -105.0525 | 1.33 |
| nhd-120655816 | 39004 | 1.5 |  | 39.3317 | -104.7307 | 5.01 |
| nhd-117819459 | 39004 | 1.5 |  | 39.4532 | -105.0797 | 1.31 |
| nhd-117819437 | 39004 | 1.5 |  | 39.4592 | -105.0613 | 1.23 |
| nhd-117819393 | 39004 | 1.4 |  | 39.4838 | -105.0179 | 5.66 |
| nhd-117819381 | 39004 | 1.3 |  | 39.4850 | -105.0182 | 5.74 |
| nhd-117819335 | 39004 | 1.3 |  | 39.4987 | -105.0152 | 6.19 |
| nhd-120655564 | 39004 | 1.2 |  | 39.3864 | -104.7873 | 3.60 |
| nhd-120656384 | 39004 | 1.2 |  | 39.1863 | -104.6894 | 6.51 |
| nhd-117793975 | 39004 | 1.1 |  | 39.2709 | -104.8514 | 10.31 |
| nhd-117792553 | 39004 | 1.1 |  | 39.3867 | -104.8633 | 9.98 |
| nhd-120656283 | 39004 | 1.1 |  | 39.2233 | -104.7644 | 1.17 |
| nhd-120656359 | 39004 | 1.1 |  | 39.1913 | -104.7599 | 3.17 |
| nhd-117819383 | 39004 | 1.1 |  | 39.4848 | -105.0981 | 1.13 |
| nhd-117819469 | 39004 | 1.1 |  | 39.4467 | -105.0772 | 1.01 |
| nhd-120655832 | 39004 | 1.1 |  | 39.3270 | -104.6983 | 6.83 |
| nhd-117819391 | 39004 | 1.1 |  | 39.4838 | -105.0727 | 1.32 |
| nhd-3af3a63e-8a13-480a-8693-2e5569fee39e | 39011 | 1.1 |  | 39.5476 | -104.8529 | 7.19 |
| nhd-117822705 | 39004 | 1.0 |  | 39.5653 | -105.0280 | 0.82 |
| nhd-120656220 | 39004 | 1.0 |  | 39.2542 | -104.6717 | 7.93 |

## 8. Byte projection

Projection: GeoJSON FeatureCollection of exactly the displayed waterbodies, coordinates rounded to 6 decimals, properties limited to id, name, gnis_id, water_class, hydro_category, fcode, area_sqkm, compact separators. The current figure is the present display artifact (Douglas: `waterbodies.geojson` file size; Aspen: waterbody-polygon features of `hydrology.geojson` serialised compactly, with their current properties). The current artifact is built from the older selection rule, so the comparison is indicative only.

| Region | Scenario | Features | Bytes | Change vs current |
|---|---|---|---|---|
| Aspen | current artifact | 43 | 65,812 | - |
| Aspen | 0.5 ha | 90 | 111,896 | +46,084 |
| Aspen | 2 ha | 46 | 71,994 | +6,182 |
| Douglas | current artifact | 33 | 117,180 | - |
| Douglas | 0.5 ha | 127 | 227,769 | +110,589 |
| Douglas | 2 ha | 32 | 119,627 | +2,447 |

## 9. How this was computed

- Aspen input: `/Users/kylekopacek/orca/workspaces/Ohvernight/m4a-source-preservation/v2/map-data-v2.json`, `/layers/hydrology`, features with `source_layer` equal to `waterbody`.
- Douglas input: `/Users/kylekopacek/orca/workspaces/Ohvernight/m4a-source-preservation/v2/regions/douglas-co/research.json`, `/layers/waterbodies`.
- Current artifacts: `/Users/kylekopacek/orca/workspaces/Ohvernight/m4a-source-preservation/v2/regions/aspen/display/hydrology.geojson` and `/Users/kylekopacek/orca/workspaces/Ohvernight/m4a-source-preservation/v2/regions/douglas-co/display/waterbodies.geojson`.
- Rules: `docs/specs/M4-functional-recreational-water.md` sections 8.1 and 8.2; tables from `v2/pipeline/config/water_display.json`.
- Worktree commit: `b008843`.
- Script: `/private/tmp/claude-501/-Users-kylekopacek-orca-workspaces-Ohvernight-m3-foundation/1af2c3f1-290d-4195-82ce-da82ec9d5e39/scratchpad/m4/prep/threshold_comparison.py`.
- Areas use the stored `area_sqkm` (three decimals), compared with `>=` against the threshold, so a stored 0.005 counts as 0.5 ha. Centroids are vertex averages, not area centroids. No network access or repository writes other than this report.

## Checks

- Aspen: total waterbodies 514 (expected 514: match); named 43; unique ids 514; every feature has integer ftype and fcode: True.
  - 0.5 ha: included 90 + below threshold 322 + intermittent 36 + unknown lake 3 + source type 63 + other 0 = 514; equals total: True
  - 2 ha: included 46 + below threshold 366 + intermittent 36 + unknown lake 3 + source type 63 + other 0 = 514; equals total: True
- Douglas: total waterbodies 2135 (expected 2135: match); named 33; unique ids 2135; every feature has integer ftype and fcode: True.
  - 0.5 ha: included 127 + below threshold 576 + intermittent 1404 + unknown lake 0 + source type 28 + other 0 = 2135; equals total: True
  - 2 ha: included 32 + below threshold 671 + intermittent 1404 + unknown lake 0 + source type 28 + other 0 = 2135; equals total: True
- Aspen 0.5 to 2 ha unnamed count: 44 (an earlier bounding-box probe expected about 41). A different number is expected if the probe counted a wider box (the canonical data is clipped to the region extent), counted by raw polygon area rather than the stored three-decimal `area_sqkm`, included intermittent or unknown-category features, or used a strict rather than inclusive 0.5 ha bound.
