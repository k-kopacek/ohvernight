# M4-B Gate 2: comparator and clip-line analysis

This is an offline, read-only analysis after retrieval report commit `d448cdbbabc8753383d398c950beae972a2044dd`. No production comparator, tolerance, source query, canonical data or artifact is changed. The production report still classifies 103 existing geometries as NOT EXPLAINED. The coordinator accepted retrieval as complete and requested this analysis before any integration.

## Why the production comparator rejects the 103

`compare_layer` in `v2/pipeline/scripts/refresh_m4b_douglas_water.py` currently checks changed geometry with this predicate (`tolerance = 1e-10`, in geographic degrees):

```python
if not bg.equals_exact(ag, tolerance):
    grown_part = ag.difference(bg)
    lost_part = bg.difference(ag)
    padded_strip = padded.difference(county)
    grows_only_into_strip = (lost_part.is_empty or
                            (lost_part.length <= tolerance and lost_part.area <= tolerance))
    growth_inside_strip = (not grown_part.is_empty and
                          padded_strip.buffer(tolerance).covers(grown_part))
    if grows_only_into_strip and growth_inside_strip:
        changed_geometry.append(ident)
    else:
        other_changes.append(ident)
```

Here `bg` is old canonical geometry and `ag` is newly clipped geometry. This computes direct old/new set subtraction. It does not test the approved county-reclip invariant. For a source line clipped independently to two boundaries, the old interpolated county-edge coordinates need not be recognized as lying on the new source segment by direct floating-point line subtraction. The resulting apparent lost/grown segments can lie inside the county even when intersecting the new geometry with the county reproduces the old geometry exactly.

Worked example `nhd-117795343`, South Platte River:

| Measurement | Result |
|---|---:|
| Old geometry | MultiLineString, three parts |
| New geometry | LineString |
| Old geodesic length | 247.971556799 m |
| New geodesic length | 893.600494419 m |
| Direct old-minus-new length | 0.0012722526689242842 degrees / 124.104429215 m |
| Direct old-minus-new area | 0 |
| Direct new-minus-old length | 0.008247993467854021 degrees / 769.733366835 m |
| `grows_only_into_strip` | false |
| `growth_inside_strip` | false |
| `padded.covers(new)` | true |
| Old equals new intersected with county, exact coordinate order and zero tolerance | true |
| Old source record and source geometry equal newly retrieved record | true |
| New maximum distance outside county | 36.281824 m |

The source has the same 18 vertices and every raw property is unchanged. The old raw source clipped directly to the county, and the new raw source clipped directly to the county, both reproduce the old canonical geometry exactly. Saved-page paths and hashes are retained in the untracked analysis JSON; raw pages are not published. This is a comparator defect relative to the approved county-reclip rule, not evidence for a deliberate additional restriction in the approved specification.

## Three waterbodies: no source change or tolerance needed for county reclip

Measurements use NAD83 / UTM zone 13N (`EPSG:26913`) with `always_xy=True`. The county reclip is performed in the native geographic coordinates first, then old and reclip geometries are projected for metric area and Hausdorff comparisons. Projecting first would define a different clip. Zero below is the computed double-precision result, not a bound on all numerical errors.

| Source ID | Old minus reclip, m² | Reclip minus old, m² | Hausdorff, m | Old within new in native coordinates | Raw vertices before/after |
|---|---:|---:|---:|---|---:|
| 117822715 | 0 | 0 | 0 | true | 56 / 56 |
| 117822899 | 0 | 0 | 0 | true | 22 / 22 |
| 117834809 (Strontia Springs Reservoir) | 0 | 0 | 0 | false | 1178 / 1178 |

All three county re-clips satisfy both `old.equals(reclip)` and `old.normalize().equals_exact(reclip.normalize(), 0)`. Their unique coordinate sets are identical: zero differing vertices, so there are no differing vertices to locate on the county clip line. The earlier three exact-order failures are ring/part coordinate-order differences, not displaced vertices. Normalization here is diagnostic ordering only; it moves, rounds and deletes no coordinate, and no normalized geometry is written to data.

For each of the three, the old and new raw geometry JSON and all raw properties are identical. The fdate values are respectively `1073952000000`, `1073952000000` and `1278963533000`; fcode values are `39004`, `39001`, `39004`; source areas are `0.016`, `0.02`, `0.328` km². Vertex counts away from the exact native county line are also 56, 22 and 1178, identical before/after, with identical vertex sequences. Both old and new raw-source county clips reproduce canonical geometry exactly. The false old-within-new predicate for Strontia must be reported, but it does not overturn the exact county-reclip result; direct subset predicates and independently clipped boundaries are numerically inconsistent here, as in the worked flowline.

[Metric, source-property and saved-page/hash sidecar](nhd-padded-clip-line-metrics.csv) contains every measurement, including geographic and projected within predicates. M4-A source pages were read from the existing source-preservation worktree's ignored `v2/pipeline/data/raw/m4a-nhd-refresh/`; none was copied into the published tree or fetched again.

## All 103: extent containment and maximum distance

The [containment sidecar](nhd-padded-comparator-containment.csv) lists each original flagged feature and its maximum distance outside the county. The maximum is **554.911375 m**. This is consistent with the fixed 0.005-degree water buffer; it is not a new extent. Directed containment radius is measured in EPSG:26913 by binary search with width below 0.00024 m and 256 circular segments per quadrant; the buffer polygon approximation error is below 0.003 m at these radii. These settings affect measurement only, not acceptance.

For all original 103, `new.difference(padded).is_empty` is true and the county reclip is topologically equal with zero tolerance. For 100, original coordinate-order equality also holds; all 103 match normalized coordinate ordering at zero tolerance.

`padded.covers(new)` nevertheless returns false for four: `nhd-117816831`, `nhd-120651557`, `nhd-117822697`, `nhd-117822739`. Every one has an empty outside difference, zero outside length/area and a padded re-intersection geometrically equal to the new feature. Their staged geometry is exactly reproduced by clipping its saved source to the same padded polygon. The reported outside vertices have zero computed metric distance to the native padded boundary. This is an exact predicate inconsistency at interpolated clip-line points; no buffered extent or tolerance was applied to classify them in this analysis. [Reclip equality](nhd-padded-reclip-equality.csv) and [containment residuals](nhd-padded-containment-residuals.csv) record these facts.

## Proposed smallest correction; not implemented

Use the approved invariant directly for existing changed geometry, rather than infer it from direct old/new subtraction:

```python
if not bg.equals(ag):
    within_padding = ag.difference(padded).is_empty
    county_part_unchanged = bg.equals(ag.intersection(county))
    if within_padding and county_part_unchanged:
        changed_geometry.append(ident)
    else:
        other_changes.append(ident)
```

Empty `new minus padded` is the set definition of containment. `equals` checks geometric equality without a tolerance and permits ring/part ordering differences. There is no buffer, rounding, snapping, simplification, new tolerance or feature exception. Existing identity/name/type/code rejection and added-feature checks are preserved. The existing change-detection `equals_exact(..., 1e-10)` becomes geometric equality without that numeric tolerance so a small inside-county displacement cannot bypass the new invariant.

An isolated temporary copy of the function passed nine synthetic checks: approved strip extension; rejection of an inside-county change; rejection of an inside change of only `1e-11` degrees; shrinkage; extent overflow; extent overflow of only `1e-11` degrees; renamed feature; retyped feature; changed fcode. [Proposal check results](nhd-padded-comparator-proposal-checks.csv). These are analysis tests, not replacements or modifications of production tests. Before a production correction is approved, they would become persistent tests alongside the existing extent tests and the real regression example.

The proposed function explains every original 103 but exposes one additional strictly nonempty padding residual on **nhd-120030962** (Cheesman Lake), which the old comparator accepted under its existing tolerance. Therefore the proposed full report is still not ready for canonical application: 94 flowline extensions pass; ten waterbody extensions pass; this one waterbody remains NOT EXPLAINED.

Its raw source geometry (2,891 vertices), all raw properties, fdate `1351468800000`, fcode `39009` and source area `3.58143493` km² are identical to M4-A. Both old/new raw county clips reproduce old canonical geometry exactly; its county reclip is equal with zero tolerance, with zero projected lost/gained area and Hausdorff distance. Its staged geometry is reproduced exactly by clipping the saved source to the padded polygon. However, `new minus padded` is a three-vertex sliver with native area **2.5968993836371877e-19 degrees²**, projected area **2.117038273201713e-10 m²**, and perimeter **19.288792541026133 m**. Two triangle vertices differ only by one latitude ULP (`39.21276995580687` versus `39.21276995580686`). This is clipping arithmetic, not a changed source geometry. Its maximum distance outside the county is 553.555489 m. The strict proposal continues to reject it; no tolerance or canonical change has been made.

Coordinator review is required on the comparator correction and this newly exposed residual. If accepting it needs any tolerance or a revised numerical predicate, that question goes to the owner; it is not implemented autonomously. The three initially queried waterbodies require no county-reclip tolerance. Production source SHA-256 remains `1dc15f75ab76391964bd852f65bd5d3070e239e04696801470887c108003c570`; canonical Douglas SHA-256 remains `55f0896051697fc52b46add755e89a0a7f9e14f267d5b6884788da58f0165e9d`. No Phase F work has begun.

## Owner additions: complete source proof and additional metrics

The [source-identity sidecar](nhd-padded-source-identity.csv) compares every original flagged source record, plus Cheesman Lake: **104 complete old/new records, zero source changes**. It compares every raw attribute after case normalization of attribute keys and the entire unclipped raw geometry JSON, not only fdate, area or a sampled vertex count. All old/new source IDs, canonical IDs, names, type and code are identical. Both sets of saved raw records clip directly to the old county geometry exactly. New saved source padded clips reproduce staging exactly. The original 100 exact-order county-reclip matches therefore satisfy all four owner conditions: unchanged source, unchanged identity/name/type/code, empty outside-padding difference and exact old-order county-reclip geometry. The three additional waterbodies satisfy exact geometric equality with coordinate ordering ignored and zero tolerance. No shape or topology change occurs away from the clip boundary.

| Source ID | Name | Old source ID / new source ID | Old clipped area, m² | New county-reclipped area, m² | Symmetric difference, m² | Maximum boundary displacement, m |
|---|---|---|---:|---:|---:|---:|
| 117822715 | unnamed | 117822715 / 117822715 | 6690.4861702411345 | 6690.486170241133 | 0 | 0 |
| 117822899 | unnamed | 117822899 / 117822899 | 5185.7028825334155 | 5185.7028825334155 | 0 | 0 |
| 117834809 | Strontia Springs Reservoir | 117834809 / 117834809 | 115450.62219567689 | 115450.62219567689 | 0 | 0 |

The first area's last summation digits differ with coordinate ordering, while the actual projected symmetric difference is empty. All gained/lost projected areas and Hausdorff values are zero as reported above. There are no changed vertices, hence no displaced vertices away from the boundary or on it. This measurement does not justify calling a changed upstream record a clipping effect; every upstream record and its raw geometry was compared directly and is identical.

### CLIP-BOUNDARY TOLERANCE DECISION: original three waterbodies

Recommended tolerance for these three: **zero**, absolute, with no relative tolerance. Exact geometric equality of the county reclip already passes, so numeric acceptance is unnecessary. Coordinate-order equivalence is not a spatial tolerance and changes no coordinates. The proposed negative checks include rejecting actual inside-county and outside-padding displacements of `1e-11` degrees; persistent tests will include source-ID changes and missing records as requested. This packet authorizes no tolerance or named exception.

Cheesman Lake is a separate newly exposed padding residual, with the measured values above. Its source is likewise identical, but the zero-tolerance subset rule still rejects its nonempty outside difference. No threshold is proposed or implemented for that residual in this checkpoint; accepting it requires a further owner decision on the specific padded clip operation. No Phase F work is eligible while it remains unexplained.
