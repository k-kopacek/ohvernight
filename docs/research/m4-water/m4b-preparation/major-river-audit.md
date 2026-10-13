# M4-B preparation: major-river audit

A checklist of the rivers a user would expect to see, taken only from the committed M4-A data and the grouping dry run in [grouping-dry-run.md](grouping-dry-run.md). Each region lists the rivers named in the task (whatever their size), then the largest by total named length, then the largest by drawn length, so that each has at least twelve entries. Nothing was joined, added or relaxed.

Columns. Lengths are sums of the source `length_km` unless marked geometric; `length_km` is the unclipped source length, so it overstates rivers cut by the extent, and the "geometric km inside extent" column gives the length actually present. Drawn fraction = drawn km / (perennial stream km + artificial path km). "drawn / all named km" adds non-perennial stream km to the denominator, which is how section 8.3 words the `expected_major_rivers` check ("named length"); the two differ, see case 4 in the dry-run report.

Verdicts, from the fixed list: COMPLETE (one displayable part, drawn fraction at least 0.95); COMPLETE WITH HIDDEN INTERMITTENT REACH (the same, but a non-perennial segment between perennial reaches is not drawn, so the group is drawn as separate pieces); MULTI-PART (more than one displayable part, hence more than one group); TRUNCATED (drawn fraction under 0.8); MOSTLY CENTRELINE (more than half the drawn km is artificial path); ABSENT (no group). A river whose intermittent reaches are only at its ends, with every perennial and artificial-path km drawn, is COMPLETE by this definition even though part of its named length is hidden; the "drawn / all named km" column shows how much.

## Result at a glance

| Region | Entries | COMPLETE | COMPLETE WITH HIDDEN INTERMITTENT REACH | MULTI-PART | TRUNCATED | MOSTLY CENTRELINE | ABSENT |
|---|---|---|---|---|---|---|---|
| Aspen | 14 | 12 | 0 | 1 | 0 | 0 | 1 |
| Douglas County | 17 | 11 | 2 | 0 | 2 | 0 | 2 |

No river in either list is MOSTLY CENTRELINE: the largest artificial-path share among the drawn rivers listed is Willow Creek 00185138 in Douglas at 47% (1.23 of 2.63 km); the Roaring Fork River is at 20% (9.74 of 48.82 km).

## Aspen

Selection: Roaring Fork River (00174812): required; Castle Creek (00180078): required; Maroon Creek (00180007): required; Snowmass Creek (00175217): required; Hunter Creek (00180061): required; Hunter Creek (00175223): required; Woody Creek (00179712): required; Lincoln Creek (00180316): required; Conundrum Creek (00180076): required; Fryingpan River (absent): required; Difficult Creek (00180075): top 12 by total named length; Willow Creek (00180033): top 12 by total named length; East Maroon Creek (00180261): top 12 by total named length; South Fork Fryingpan River (00179784): top 12 by total named length.

### Checklist

| River | gnis_id | perennial stream km | non-perennial stream km | artificial path km | Group id(s) | Present as a group? | Parts | drawn members | drawn km (length_km) | geometric km inside extent: drawn of all named | drawn fraction (of perennial + artificial path) | drawn / all named km | separate drawn pieces | Intermittent reach between perennial reaches? | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Roaring Fork River | 00174812 | 39.07 | 0.05 | 9.74 | nhd-gnis-00174812 | yes | 1 displayable of 1 | 111 | 48.82 | 48.81 of 48.87 | 1.00 | 1.00 | 1 | no | **COMPLETE** |
| Castle Creek | 00180078 | 30.58 | 0.00 | 0.06 | nhd-gnis-00180078 | yes | 1 displayable of 1 | 78 | 30.64 | 30.54 of 30.54 | 1.00 | 1.00 | 1 | no | **COMPLETE** |
| Maroon Creek | 00180007 | 15.15 | 0.00 | 0.03 | nhd-gnis-00180007 | yes | 1 displayable of 1 | 42 | 15.19 | 15.13 of 15.13 | 1.00 | 1.00 | 1 | no | **COMPLETE** |
| Snowmass Creek | 00175217 | 27.37 | 0.00 | 0.16 | nhd-gnis-00175217 | yes | 1 displayable of 1 | 83 | 27.53 | 27.40 of 27.40 | 1.00 | 1.00 | 1 | no | **COMPLETE** |
| Hunter Creek | 00180061 | 24.74 | 0.00 | 0.29 | nhd-gnis-00180061, nhd-gnis-00180061-p2 | yes | 2 displayable of 2 | 58 | 25.03 | 25.07 of 25.07 | 1.00 | 1.00 | 2 | no | **MULTI-PART** |
| Hunter Creek | 00175223 | 6.65 | 0.00 | 0.00 | nhd-gnis-00175223 | yes | 1 displayable of 1 | 14 | 6.65 | 6.65 of 6.65 | 1.00 | 1.00 | 1 | no | **COMPLETE** |
| Woody Creek | 00179712 | 20.29 | 0.00 | 0.02 | nhd-gnis-00179712 | yes | 1 displayable of 1 | 77 | 20.31 | 20.30 of 20.30 | 1.00 | 1.00 | 1 | no | **COMPLETE** |
| Lincoln Creek | 00180316 | 18.66 | 0.00 | 0.88 | nhd-gnis-00180316 | yes | 1 displayable of 1 | 55 | 19.55 | 19.51 of 19.51 | 1.00 | 1.00 | 1 | no | **COMPLETE** |
| Conundrum Creek | 00180076 | 15.87 | 0.00 | 0.00 | nhd-gnis-00180076 | yes | 1 displayable of 1 | 42 | 15.87 | 15.80 of 15.80 | 1.00 | 1.00 | 1 | no | **COMPLETE** |
| Fryingpan River | not in data | - | - | - | - | no | - | 0 | 0 | - | 0.00 | - | - | - | **ABSENT** |
| Difficult Creek | 00180075 | 14.08 | 0.00 | 0.00 | nhd-gnis-00180075 | yes | 1 displayable of 1 | 19 | 14.08 | 14.03 of 14.03 | 1.00 | 1.00 | 1 | no | **COMPLETE** |
| Willow Creek | 00180033 | 12.48 | 0.00 | 0.72 | nhd-gnis-00180033 | yes | 1 displayable of 1 | 52 | 13.20 | 13.20 of 13.20 | 1.00 | 1.00 | 1 | no | **COMPLETE** |
| East Maroon Creek | 00180261 | 12.85 | 0.00 | 0.26 | nhd-gnis-00180261 | yes | 1 displayable of 1 | 36 | 13.11 | 13.05 of 13.05 | 1.00 | 1.00 | 1 | no | **COMPLETE** |
| South Fork Fryingpan River | 00179784 | 12.86 | 0.00 | 0.00 | nhd-gnis-00179784 | yes | 1 displayable of 1 | 26 | 12.86 | 11.96 of 11.96 | 1.00 | 1.00 | 1 | no | **COMPLETE** |

### Centreline and area relationship

| River | gnis_id | drawn artificial-path members | all artificial-path segments | distinct waterbody_source_id among drawn | do drawn ids match a feature in the regional data? | all artificial paths of this gnis_id |
|---|---|---|---|---|---|---|
| Roaring Fork River | 00174812 | 29 (9.74 km) | 29 (9.74 km) | 5 | 4 waterbody, 1 area, 0 not in regional data | all artificial paths reference 5 ids: 4 waterbody, 1 area, 0 absent; 0 artificial paths have no waterbody_source_id |
| Castle Creek | 00180078 | 1 (0.06 km) | 1 (0.06 km) | 1 | 0 waterbody, 1 area, 0 not in regional data | all artificial paths reference 1 ids: 0 waterbody, 1 area, 0 absent; 0 artificial paths have no waterbody_source_id |
| Maroon Creek | 00180007 | 1 (0.03 km) | 1 (0.03 km) | 1 | 0 waterbody, 1 area, 0 not in regional data | all artificial paths reference 1 ids: 0 waterbody, 1 area, 0 absent; 0 artificial paths have no waterbody_source_id |
| Snowmass Creek | 00175217 | 3 (0.16 km) | 3 (0.16 km) | 1 | 1 waterbody, 0 area, 0 not in regional data | all artificial paths reference 1 ids: 1 waterbody, 0 area, 0 absent; 0 artificial paths have no waterbody_source_id |
| Hunter Creek | 00180061 | 2 (0.29 km) | 2 (0.29 km) | 2 | 2 waterbody, 0 area, 0 not in regional data | all artificial paths reference 2 ids: 2 waterbody, 0 area, 0 absent; 0 artificial paths have no waterbody_source_id |
| Hunter Creek | 00175223 | 0 (0.00 km) | 0 (0.00 km) | 0 | 0 waterbody, 0 area, 0 not in regional data | no artificial paths |
| Woody Creek | 00179712 | 1 (0.02 km) | 1 (0.02 km) | 1 | 1 waterbody, 0 area, 0 not in regional data | all artificial paths reference 1 ids: 1 waterbody, 0 area, 0 absent; 0 artificial paths have no waterbody_source_id |
| Lincoln Creek | 00180316 | 9 (0.88 km) | 9 (0.88 km) | 3 | 3 waterbody, 0 area, 0 not in regional data | all artificial paths reference 3 ids: 3 waterbody, 0 area, 0 absent; 0 artificial paths have no waterbody_source_id |
| Conundrum Creek | 00180076 | 0 (0.00 km) | 0 (0.00 km) | 0 | 0 waterbody, 0 area, 0 not in regional data | no artificial paths |
| Fryingpan River | - | - | - | - | - | No flowline with this name. Names containing "Fryingpan": South Fork Fryingpan River |
| Difficult Creek | 00180075 | 0 (0.00 km) | 0 (0.00 km) | 0 | 0 waterbody, 0 area, 0 not in regional data | no artificial paths |
| Willow Creek | 00180033 | 5 (0.72 km) | 5 (0.72 km) | 4 | 4 waterbody, 0 area, 0 not in regional data | all artificial paths reference 4 ids: 4 waterbody, 0 area, 0 absent; 0 artificial paths have no waterbody_source_id |
| East Maroon Creek | 00180261 | 5 (0.26 km) | 5 (0.26 km) | 3 | 3 waterbody, 0 area, 0 not in regional data | all artificial paths reference 3 ids: 3 waterbody, 0 area, 0 absent; 0 artificial paths have no waterbody_source_id |
| South Fork Fryingpan River | 00179784 | 0 (0.00 km) | 0 (0.00 km) | 0 | 0 waterbody, 0 area, 0 not in regional data | no artificial paths |

## Douglas County

Selection: South Platte River (00201759): required; Plum Creek (00183363): required; East Plum Creek (00185069): required; West Plum Creek (00185068): required; Cherry Creek (00181657): required; Bear Creek (00183744): required; Bear Creek (00183345): required; Jackson Creek (00183584): required; Indian Creek (00183378): required; East Cherry Creek (00185141): top 12 by total named length; West Cherry Creek (00185140): top 12 by total named length; Antelope Creek (00185144): top 12 by total named length; Happy Canyon Creek (00185007): top 12 by total named length; Willow Creek (00185138): top 12 by total named length; Trout Creek (00183711): top 12 by drawn length; Cook Creek (00193182): top 12 by drawn length; Carpenter Creek (00196378): top 12 by drawn length.

### Checklist

| River | gnis_id | perennial stream km | non-perennial stream km | artificial path km | Group id(s) | Present as a group? | Parts | drawn members | drawn km (length_km) | geometric km inside extent: drawn of all named | drawn fraction (of perennial + artificial path) | drawn / all named km | separate drawn pieces | Intermittent reach between perennial reaches? | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| South Platte River | 00201759 | 0.00 | 0.00 | 22.86 | - | no | 0 displayable of 43 | 0 | 0.00 | 0.00 of 9.51 | 0.00 | 0.00 | 0 | no | **ABSENT** |
| Plum Creek | 00183363 | 16.23 | 0.00 | 2.47 | nhd-gnis-00183363 | yes | 1 displayable of 1 | 55 | 18.70 | 18.66 of 18.66 | 1.00 | 1.00 | 1 | no | **COMPLETE** |
| East Plum Creek | 00185069 | 53.57 | 0.09 | 0.03 | nhd-gnis-00185069 | yes | 1 displayable of 1 | 182 | 53.60 | 53.36 of 53.45 | 1.00 | 1.00 | 2 | yes, 0.09 km hidden between drawn reaches | **COMPLETE WITH HIDDEN INTERMITTENT REACH** |
| West Plum Creek | 00185068 | 33.61 | 2.68 | 0.61 | nhd-gnis-00185068 | yes | 1 displayable of 1 | 87 | 34.22 | 34.14 of 36.80 | 1.00 | 0.93 | 1 | no | **COMPLETE** |
| Cherry Creek | 00181657 | 38.96 | 4.63 | 1.14 | nhd-gnis-00181657 | yes | 1 displayable of 1 | 65 | 39.87 | 39.77 of 44.11 | 0.99 | 0.89 | 1 | no | **COMPLETE** |
| Bear Creek | 00183744 | 14.71 | 0.49 | 0.96 | nhd-gnis-00183744 | yes | 1 displayable of 1 | 67 | 15.67 | 15.64 of 16.13 | 1.00 | 0.97 | 1 | no | **COMPLETE** |
| Bear Creek | 00183345 | 12.43 | 0.00 | 0.78 | nhd-gnis-00183345 | yes | 1 displayable of 1 | 76 | 13.21 | 13.10 of 13.10 | 1.00 | 1.00 | 1 | no | **COMPLETE** |
| Jackson Creek | 00183584 | 19.25 | 1.18 | 0.08 | nhd-gnis-00183584 | yes | 1 displayable of 1 | 109 | 19.33 | 19.31 of 20.48 | 1.00 | 0.94 | 1 | no | **COMPLETE** |
| Indian Creek | 00183378 | 16.84 | 1.94 | 0.00 | nhd-gnis-00183378 | yes | 1 displayable of 1 | 65 | 16.84 | 16.82 of 18.76 | 1.00 | 0.90 | 2 | yes, 0.01 km hidden between drawn reaches | **COMPLETE WITH HIDDEN INTERMITTENT REACH** |
| East Cherry Creek | 00185141 | 6.80 | 16.74 | 2.59 | nhd-gnis-00185141 | yes | 1 displayable of 2 | 8 | 6.80 | 6.79 of 24.85 | 0.72 | 0.26 | 1 | no | **TRUNCATED** |
| West Cherry Creek | 00185140 | 23.11 | 1.08 | 0.21 | nhd-gnis-00185140 | yes | 1 displayable of 1 | 21 | 23.32 | 23.27 of 24.33 | 1.00 | 0.96 | 1 | no | **COMPLETE** |
| Antelope Creek | 00185144 | 13.44 | 7.87 | 1.80 | nhd-gnis-00185144 | yes | 1 displayable of 1 | 28 | 14.57 | 14.54 of 23.07 | 0.96 | 0.63 | 1 | no | **COMPLETE** |
| Happy Canyon Creek | 00185007 | 0.00 | 12.21 | 7.23 | - | no | 0 displayable of 1 | 0 | 0.00 | 0.00 of 18.72 | 0.00 | 0.00 | 0 | no | **ABSENT** |
| Willow Creek | 00185138 | 1.40 | 14.26 | 1.96 | nhd-gnis-00185138 | yes | 1 displayable of 1 | 6 | 2.63 | 2.62 of 17.58 | 0.78 | 0.15 | 2 | yes, 0.02 km hidden between drawn reaches | **TRUNCATED** |
| Trout Creek | 00183711 | 14.56 | 0.00 | 1.51 | nhd-gnis-00183711 | yes | 1 displayable of 1 | 80 | 16.07 | 15.48 of 15.48 | 1.00 | 1.00 | 1 | no | **COMPLETE** |
| Cook Creek | 00193182 | 15.66 | 0.00 | 0.09 | nhd-gnis-00193182 | yes | 1 displayable of 1 | 57 | 15.75 | 15.43 of 15.43 | 1.00 | 1.00 | 1 | no | **COMPLETE** |
| Carpenter Creek | 00196378 | 13.35 | 1.91 | 0.00 | nhd-gnis-00196378 | yes | 1 displayable of 1 | 11 | 13.35 | 13.32 of 15.07 | 1.00 | 0.88 | 1 | no | **COMPLETE** |

### Centreline and area relationship

| River | gnis_id | drawn artificial-path members | all artificial-path segments | distinct waterbody_source_id among drawn | do drawn ids match a feature in the regional data? | all artificial paths of this gnis_id |
|---|---|---|---|---|---|---|
| South Platte River | 00201759 | 0 (0.00 km) | 75 (22.86 km) | 0 | 0 waterbody, 0 area, 0 not in regional data | all artificial paths reference 7 ids: 3 waterbody, 0 area, 4 absent; 0 artificial paths have no waterbody_source_id |
| Plum Creek | 00183363 | 1 (2.47 km) | 1 (2.47 km) | 1 | 1 waterbody, 0 area, 0 not in regional data | all artificial paths reference 1 ids: 1 waterbody, 0 area, 0 absent; 0 artificial paths have no waterbody_source_id |
| East Plum Creek | 00185069 | 1 (0.03 km) | 1 (0.03 km) | 1 | 1 waterbody, 0 area, 0 not in regional data | all artificial paths reference 1 ids: 1 waterbody, 0 area, 0 absent; 0 artificial paths have no waterbody_source_id |
| West Plum Creek | 00185068 | 3 (0.61 km) | 3 (0.61 km) | 2 | 2 waterbody, 0 area, 0 not in regional data | all artificial paths reference 2 ids: 2 waterbody, 0 area, 0 absent; 0 artificial paths have no waterbody_source_id |
| Cherry Creek | 00181657 | 5 (0.90 km) | 6 (1.14 km) | 2 | 1 waterbody, 0 area, 1 not in regional data | all artificial paths reference 3 ids: 1 waterbody, 0 area, 2 absent; 0 artificial paths have no waterbody_source_id |
| Bear Creek | 00183744 | 10 (0.96 km) | 10 (0.96 km) | 4 | 4 waterbody, 0 area, 0 not in regional data | all artificial paths reference 4 ids: 4 waterbody, 0 area, 0 absent; 0 artificial paths have no waterbody_source_id |
| Bear Creek | 00183345 | 5 (0.78 km) | 5 (0.78 km) | 5 | 5 waterbody, 0 area, 0 not in regional data | all artificial paths reference 5 ids: 5 waterbody, 0 area, 0 absent; 0 artificial paths have no waterbody_source_id |
| Jackson Creek | 00183584 | 3 (0.08 km) | 3 (0.08 km) | 2 | 2 waterbody, 0 area, 0 not in regional data | all artificial paths reference 2 ids: 2 waterbody, 0 area, 0 absent; 0 artificial paths have no waterbody_source_id |
| Indian Creek | 00183378 | 0 (0.00 km) | 0 (0.00 km) | 0 | 0 waterbody, 0 area, 0 not in regional data | no artificial paths |
| East Cherry Creek | 00185141 | 0 (0.00 km) | 8 (2.59 km) | 0 | 0 waterbody, 0 area, 0 not in regional data | all artificial paths reference 7 ids: 1 waterbody, 0 area, 6 absent; 0 artificial paths have no waterbody_source_id |
| West Cherry Creek | 00185140 | 2 (0.21 km) | 2 (0.21 km) | 2 | 2 waterbody, 0 area, 0 not in regional data | all artificial paths reference 2 ids: 2 waterbody, 0 area, 0 absent; 0 artificial paths have no waterbody_source_id |
| Antelope Creek | 00185144 | 11 (1.14 km) | 14 (1.80 km) | 8 | 8 waterbody, 0 area, 0 not in regional data | all artificial paths reference 11 ids: 11 waterbody, 0 area, 0 absent; 0 artificial paths have no waterbody_source_id |
| Happy Canyon Creek | 00185007 | 0 (0.00 km) | 9 (7.23 km) | 0 | 0 waterbody, 0 area, 0 not in regional data | all artificial paths reference 4 ids: 1 waterbody, 0 area, 3 absent; 0 artificial paths have no waterbody_source_id |
| Willow Creek | 00185138 | 3 (1.23 km) | 10 (1.96 km) | 2 | 0 waterbody, 0 area, 2 not in regional data | all artificial paths reference 6 ids: 4 waterbody, 0 area, 2 absent; 0 artificial paths have no waterbody_source_id |
| Trout Creek | 00183711 | 13 (1.51 km) | 13 (1.51 km) | 4 | 3 waterbody, 0 area, 1 not in regional data | all artificial paths reference 4 ids: 3 waterbody, 0 area, 1 absent; 0 artificial paths have no waterbody_source_id |
| Cook Creek | 00193182 | 2 (0.09 km) | 2 (0.09 km) | 2 | 2 waterbody, 0 area, 0 not in regional data | all artificial paths reference 2 ids: 2 waterbody, 0 area, 0 absent; 0 artificial paths have no waterbody_source_id |
| Carpenter Creek | 00196378 | 0 (0.00 km) | 0 (0.00 km) | 0 | 0 waterbody, 0 area, 0 not in regional data | no artificial paths |

## Three rivers in detail

**Roaring Fork River (Aspen, `gnis_id` 00174812).** The data holds 112 segments in one connected part: 82 perennial stream segments (39.07 km), 29 artificial-path segments (9.74 km) and one intermittent stream segment (0.054 km, `nhd-72972704`). The rule draws 111 members, 48.82 km, as a single connected line: every perennial segment and every artificial path, because each artificial path is reachable from a perennial segment through artificial paths alone. The only thing left out is the 54 m intermittent segment, which is a dead-end tail and not a link between drawn reaches, so there is no visible gap. Drawn fraction 1.00; one group, `nhd-gnis-00174812`; one drawn piece. The 29 artificial paths reference five `waterbody_source_id` values and all five are in the Aspen data: four waterbodies and the single area feature (`nhd-72977308`). Geometric length inside the extent is 48.81 of 48.87 km, so clipping barely affects it. Verdict: COMPLETE. The specification's example `member_count` of 96 should read 111.

**East Plum Creek (Douglas County, `gnis_id` 00185069).** The data holds 183 segments in one connected part: 181 perennial stream segments (53.57 km), one artificial path (0.03 km, through a waterbody that is in the data) and one intermittent stream segment of 0.085 km (`nhd-117837989`). The rule draws 182 members, 53.60 km, drawn fraction 1.00, as one group `nhd-gnis-00185069`. The intermittent segment lies between two perennial reaches, so the group is drawn as two separate lines of 45.77 km (130 members) and 7.83 km (52 members) with an 85 m gap where the hidden segment is. It remains one group with one identity; nothing bridges the gap. Verdict: COMPLETE WITH HIDDEN INTERMITTENT REACH. This is the longest group in either region.

**South Platte River (Douglas County, `gnis_id` 00201759).** Inside the Douglas data the river has **no perennial stream segment at all**: 0.00 km of perennial stream, 0.00 km of non-perennial stream, and 22.86 km (`length_km`) of artificial path in 75 segments. Because the county boundary follows the river, the county clip cuts those paths into 43 disconnected parts; all 114 free ends of the parts lie within 0.07 m of the coverage polygon boundary, and only 9.51 km of geometry is actually inside the county (the largest fragment is 1.37 km). The gaps between neighbouring fragments run from 28 m to 2,820 m, median 427 m; 2 are under 50 m and 15 under 250 m. The artificial paths do not connect end to end to any perennial segment of the South Platte, because there is none; they touch only artificial paths of four tributaries (Plum Creek, Turkey Creek, Horse Creek, Douglas Creek), which have different `gnis_id` values and so cannot make them drawable. No part is displayable, no group is created, and **the fraction drawn is 0%** of 22.86 km. The specification expected a single 80 m perennial segment to anchor the centre line; that segment was seen by a bounding-box probe and is not in the county-clipped data, and even with it the rule would have drawn only the fragment connected to it. The paths reference seven `waterbody_source_id` values: Cheesman Lake (4.58 km), Chatfield Lake (1.84 km) and Strontia Springs Reservoir (0.32 km) are present as waterbodies; the other four ids (16.12 km of `length_km`, 5.71 km of geometry) are river-area polygons that are not in the Douglas data, which has no area layer. Verdict: ABSENT. Under 8.3 this stops M4-B, and the remedy is an owner decision, not a change made here.

## Other observations

- **Hunter Creek (Aspen, 00180061)** is drawn in full (25.03 km) but as two groups, `nhd-gnis-00180061` (54 members, 24.01 km) and `-p2` (4 members, 1.01 km), 19 m apart. The only link in the source is a named connector segment with the same `gnis_id`, which the rule does not use. A second, unrelated Hunter Creek (00175223, 6.65 km) is complete.
- **Cherry Creek (Douglas, 00181657)**: 38.96 km perennial drawn in one piece; 4.63 km of intermittent stream at an end is hidden and one 0.23 km artificial path behind it is not drawn. Drawn fraction 0.99, or 0.89 of all named length.
- **East Cherry Creek (Douglas, 00185141)**: 6.80 km drawn out of 23.53 km of named stream (26.13 km including artificial path). A second part of 12.59 km (11.12 km intermittent, 1.47 km artificial path) has no perennial segment and is not shown.
- **Willow Creek (Douglas, 00185138)**: 2.63 km drawn in two pieces out of 17.62 km named (all classes); the creek is almost entirely intermittent. Two further Willow Creek `gnis_id` values (00183369, 00185008) are not shown at all.
- **Happy Canyon Creek (Douglas, 00185007)**: 19.44 km named, none perennial, not shown.
- **Fryingpan River (Aspen)**: not present under that name; South Fork Fryingpan River is present and complete.
- In Douglas, 5 of the checklist rivers have drawn artificial paths whose `waterbody_source_id` is not in the regional data (Cherry, Willow, Trout Creek) or have undrawn ones that are not (East Cherry, Happy Canyon); these are area polygons, which the Douglas data does not carry.

## Proposed machine-checkable fixture

**This is a proposal for the coordinator, not a decision.** It lists, per region, rivers the data shows are COMPLETE today (including COMPLETE WITH HIDDEN INTERMITTENT REACH), each with the specification's initial minimum of 0.8, in the shape `water_display.json` `expected_major_rivers` would take. The fraction used is drawn km / (perennial stream km + artificial path km); if the build adopts the "all named length" denominator instead, Antelope Creek (0.63) would fail and should be removed. The list is deliberately longer than the specification's initial five per region so the coordinator can cut it down; smaller creeks included only because they ranked by length (Difficult, Willow, East Maroon, South Fork Fryingpan; West Cherry, Antelope, Trout, Cook, Carpenter) are candidates to drop.

```json
{
  "expected_major_rivers_proposal": {
    "aspen": [
      {
        "gnis_id": "00174812",
        "name": "Roaring Fork River",
        "min_drawn_fraction": 0.8
      },
      {
        "gnis_id": "00180078",
        "name": "Castle Creek",
        "min_drawn_fraction": 0.8
      },
      {
        "gnis_id": "00180007",
        "name": "Maroon Creek",
        "min_drawn_fraction": 0.8
      },
      {
        "gnis_id": "00175217",
        "name": "Snowmass Creek",
        "min_drawn_fraction": 0.8
      },
      {
        "gnis_id": "00175223",
        "name": "Hunter Creek",
        "min_drawn_fraction": 0.8
      },
      {
        "gnis_id": "00179712",
        "name": "Woody Creek",
        "min_drawn_fraction": 0.8
      },
      {
        "gnis_id": "00180316",
        "name": "Lincoln Creek",
        "min_drawn_fraction": 0.8
      },
      {
        "gnis_id": "00180076",
        "name": "Conundrum Creek",
        "min_drawn_fraction": 0.8
      },
      {
        "gnis_id": "00180075",
        "name": "Difficult Creek",
        "min_drawn_fraction": 0.8
      },
      {
        "gnis_id": "00180033",
        "name": "Willow Creek",
        "min_drawn_fraction": 0.8
      },
      {
        "gnis_id": "00180261",
        "name": "East Maroon Creek",
        "min_drawn_fraction": 0.8
      },
      {
        "gnis_id": "00179784",
        "name": "South Fork Fryingpan River",
        "min_drawn_fraction": 0.8
      }
    ],
    "douglas-co": [
      {
        "gnis_id": "00183363",
        "name": "Plum Creek",
        "min_drawn_fraction": 0.8
      },
      {
        "gnis_id": "00185069",
        "name": "East Plum Creek",
        "min_drawn_fraction": 0.8
      },
      {
        "gnis_id": "00185068",
        "name": "West Plum Creek",
        "min_drawn_fraction": 0.8
      },
      {
        "gnis_id": "00181657",
        "name": "Cherry Creek",
        "min_drawn_fraction": 0.8
      },
      {
        "gnis_id": "00183744",
        "name": "Bear Creek",
        "min_drawn_fraction": 0.8
      },
      {
        "gnis_id": "00183345",
        "name": "Bear Creek",
        "min_drawn_fraction": 0.8
      },
      {
        "gnis_id": "00183584",
        "name": "Jackson Creek",
        "min_drawn_fraction": 0.8
      },
      {
        "gnis_id": "00183378",
        "name": "Indian Creek",
        "min_drawn_fraction": 0.8
      },
      {
        "gnis_id": "00185140",
        "name": "West Cherry Creek",
        "min_drawn_fraction": 0.8
      },
      {
        "gnis_id": "00185144",
        "name": "Antelope Creek",
        "min_drawn_fraction": 0.8
      },
      {
        "gnis_id": "00183711",
        "name": "Trout Creek",
        "min_drawn_fraction": 0.8
      },
      {
        "gnis_id": "00193182",
        "name": "Cook Creek",
        "min_drawn_fraction": 0.8
      },
      {
        "gnis_id": "00196378",
        "name": "Carpenter Creek",
        "min_drawn_fraction": 0.8
      }
    ]
  },
  "passes_0.8_per_gnis_id_but_not_complete": {
    "aspen": [
      {
        "gnis_id": "00180061",
        "name": "Hunter Creek",
        "drawn_fraction_today": 1.0,
        "verdict": [
          "MULTI-PART"
        ],
        "reason": "drawn in full but as two groups; the parts are joined in the source only by a named connector (grouping-dry-run.md, case 2)"
      }
    ],
    "douglas-co": []
  },
  "would_fail_0.8_today": {
    "aspen": [
      {
        "gnis_id": null,
        "name": "Fryingpan River",
        "drawn_fraction_today": 0,
        "verdict": [
          "ABSENT"
        ],
        "reason": "no flowline with this name in the Aspen data; only South Fork Fryingpan River is present"
      }
    ],
    "douglas-co": [
      {
        "gnis_id": "00201759",
        "name": "South Platte River",
        "drawn_fraction_today": 0.0,
        "verdict": [
          "ABSENT"
        ],
        "reason": "no perennial stream segment in the county-clipped data; 75 artificial-path segments in 43 fragments, none displayable"
      },
      {
        "gnis_id": "00185141",
        "name": "East Cherry Creek",
        "drawn_fraction_today": 0.72,
        "verdict": [
          "TRUNCATED"
        ],
        "reason": "perennial 6.80 km drawn; 2.59 km of artificial path not drawn (1.47 km in a part with no perennial segment, 1.12 km behind intermittent segments); 16.74 km is intermittent"
      },
      {
        "gnis_id": "00185007",
        "name": "Happy Canyon Creek",
        "drawn_fraction_today": 0.0,
        "verdict": [
          "ABSENT"
        ],
        "reason": "no perennial stream segment: 12.21 km intermittent and 7.23 km artificial path"
      },
      {
        "gnis_id": "00185138",
        "name": "Willow Creek",
        "drawn_fraction_today": 0.78,
        "verdict": [
          "TRUNCATED"
        ],
        "reason": "1.40 km perennial and 1.23 km artificial path drawn; 0.73 km of artificial path sits behind intermittent segments; 14.26 km is intermittent"
      }
    ]
  }
}
```

Rivers on the specification's initial list (8.3) and how they stand: Aspen — Roaring Fork River, Castle Creek, Maroon Creek, Snowmass Creek pass; Hunter Creek 00180061 passes on fraction but is MULTI-PART. Douglas — Plum Creek, East Plum Creek, West Plum Creek, Cherry Creek pass; **South Platte River fails (ABSENT)**.
