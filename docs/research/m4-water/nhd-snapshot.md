# M4-A NHD snapshot and difference report

## Retrieval record

- Service: `https://hydro.nationalmap.gov/arcgis/rest/services/nhd/MapServer`
- Service currentVersion: `11.3`; service documentInfo Version: `3.3.0`.
- Service metadata contained no data-date text: `True`. The returned NHD features retain their source `fdate` values as `source_date`.
- First persisted service-metadata response (the CLI launch timestamp was not captured): `2026-10-07T00:31:37.877546Z`. Refresh completed at `2026-10-07T00:32:43.278494Z`. The exact CLI start is therefore bounded by the first-response timestamp, not independently recorded.
- One controlled refresh session; no request was made to 3DHP or any other host. No RIDB stage/key was used, and stage 07 did not run.
- Raw pages are under ignored `v2/pipeline/data/raw/m4a-nhd-refresh/`; normalized stages and this report are under ignored `v2/pipeline/data/processed/m4a-nhd-refresh/`.
- Aspen used its existing 0.005-degree padded AOI. Douglas layer 6 queried named flowlines only; layer 12 queried all waterbodies; no Douglas layer 9 request was made.

## Exact queries and returned counts

Every feature query used count + complete object-ID enumeration, then GeoJSON batches of at most 250 object IDs, `outSR=4326`, geometry enabled. `outFields` includes the layer's `OBJECTID` after the listed source fields. The object-ID count comes from the saved immutable query plan; returned count is the number of service features.

| Region/query | Layer | where | outFields | extent (WGS84 minX,minY,maxX,maxY) | batch size / pages | object IDs | returned |
|---|---:|---|---|---|---:|---:|---:|
| aspen 6  | 6 | `1=1` | `permanent_identifier,gnis_id,gnis_name,ftype,fcode,reachcode,lengthkm,visibilityfilter,wbarea_permanent_identifier,fdate,OBJECTID` | `-107.05499999999999,38.995,-106.565,39.265` | 250 / 26 | 6411 | 6411 |
| aspen 9  | 9 | `1=1` | `PERMANENT_IDENTIFIER,GNIS_ID,GNIS_NAME,FTYPE,FCODE,AREASQKM,VISIBILITYFILTER,FDATE,OBJECTID` | `-107.05499999999999,38.995,-106.565,39.265` | 250 / 1 | 1 | 1 |
| aspen 12  | 12 | `1=1` | `PERMANENT_IDENTIFIER,GNIS_ID,GNIS_NAME,FTYPE,FCODE,AREASQKM,ELEVATION,REACHCODE,VISIBILITYFILTER,FDATE,OBJECTID` | `-107.05499999999999,38.995,-106.565,39.265` | 250 / 3 | 514 | 514 |
| douglas-co 6  | 6 | `gnis_name IS NOT NULL AND gnis_name <> ''` | `permanent_identifier,gnis_id,gnis_name,ftype,fcode,reachcode,lengthkm,visibilityfilter,wbarea_permanent_identifier,fdate,OBJECTID` | `-105.32944499965761,39.12947900008431,-104.66058399994039,39.56619299967445` | 250 / 15 | 3607 | 3607 |
| douglas-co 12  | 12 | `1=1` | `PERMANENT_IDENTIFIER,GNIS_ID,GNIS_NAME,FTYPE,FCODE,AREASQKM,ELEVATION,REACHCODE,VISIBILITYFILTER,FDATE,OBJECTID` | `-105.32944499965761,39.12947900008431,-104.66058399994039,39.56619299967445` | 250 / 10 | 2277 | 2277 |
| Douglas support planning | 6 | Derived from named endpoints; 26 boxes, endpoints rounded to 6 decimals, maximum gap 250 m, each envelope 300 m wide | n/a | n/a | no feature page | 26 boxes | n/a |
| douglas-co 6 support_for=00185006 | 6 | `gnis_name IS NULL OR gnis_name = ''` | `permanent_identifier,gnis_id,gnis_name,ftype,fcode,reachcode,lengthkm,visibilityfilter,wbarea_permanent_identifier,fdate,OBJECTID` | `-104.800504,39.4604089,-104.7970089,39.4631181` | 250 / 1 | 3 | 3 |
| douglas-co 6 support_for=00201759 | 6 | `gnis_name IS NULL OR gnis_name = ''` | `permanent_identifier,gnis_id,gnis_name,ftype,fcode,reachcode,lengthkm,visibilityfilter,wbarea_permanent_identifier,fdate,OBJECTID` | `-105.3034612,39.1663968,-105.2999769,39.1691091` | 250 / 1 | 7 | 7 |
| douglas-co 6 support_for=00201759 | 6 | `gnis_name IS NULL OR gnis_name = ''` | `permanent_identifier,gnis_id,gnis_name,ftype,fcode,reachcode,lengthkm,visibilityfilter,wbarea_permanent_identifier,fdate,OBJECTID` | `-105.2981127,39.1713369,-105.2946284,39.174049` | 250 / 1 | 1 | 1 |
| douglas-co 6 support_for=00201759 | 6 | `gnis_name IS NULL OR gnis_name = ''` | `permanent_identifier,gnis_id,gnis_name,ftype,fcode,reachcode,lengthkm,visibilityfilter,wbarea_permanent_identifier,fdate,OBJECTID` | `-105.2963777,39.1721535,-105.2928934,39.1748655` | 250 / 1 | 5 | 5 |
| douglas-co 6 support_for=00201759 | 6 | `gnis_name IS NULL OR gnis_name = ''` | `permanent_identifier,gnis_id,gnis_name,ftype,fcode,reachcode,lengthkm,visibilityfilter,wbarea_permanent_identifier,fdate,OBJECTID` | `-105.2535061,39.2419876,-105.25002,39.2446984` | 250 / 1 | 4 | 4 |
| douglas-co 6 support_for=00201759 | 6 | `gnis_name IS NULL OR gnis_name = ''` | `permanent_identifier,gnis_id,gnis_name,ftype,fcode,reachcode,lengthkm,visibilityfilter,wbarea_permanent_identifier,fdate,OBJECTID` | `-105.2529626,39.2416931,-105.2494765,39.2444039` | 250 / 1 | 4 | 4 |
| douglas-co 6 support_for=00201759 | 6 | `gnis_name IS NULL OR gnis_name = ''` | `permanent_identifier,gnis_id,gnis_name,ftype,fcode,reachcode,lengthkm,visibilityfilter,wbarea_permanent_identifier,fdate,OBJECTID` | `-105.2526836,39.2414631,-105.2491975,39.2441739` | 250 / 1 | 4 | 4 |
| douglas-co 6 support_for=00201759 | 6 | `gnis_name IS NULL OR gnis_name = ''` | `permanent_identifier,gnis_id,gnis_name,ftype,fcode,reachcode,lengthkm,visibilityfilter,wbarea_permanent_identifier,fdate,OBJECTID` | `-105.2525415,39.2414231,-105.2490555,39.2441339` | 250 / 1 | 4 | 4 |
| douglas-co 6 support_for=00201759 | 6 | `gnis_name IS NULL OR gnis_name = ''` | `permanent_identifier,gnis_id,gnis_name,ftype,fcode,reachcode,lengthkm,visibilityfilter,wbarea_permanent_identifier,fdate,OBJECTID` | `-105.2522625,39.2411931,-105.2487765,39.2439039` | 250 / 1 | 4 | 4 |
| douglas-co 6 support_for=00201759 | 6 | `gnis_name IS NULL OR gnis_name = ''` | `permanent_identifier,gnis_id,gnis_name,ftype,fcode,reachcode,lengthkm,visibilityfilter,wbarea_permanent_identifier,fdate,OBJECTID` | `-105.2517495,39.2409626,-105.2482635,39.2436734` | 250 / 1 | 2 | 2 |
| douglas-co 6 support_for=00201759 | 6 | `gnis_name IS NULL OR gnis_name = ''` | `permanent_identifier,gnis_id,gnis_name,ftype,fcode,reachcode,lengthkm,visibilityfilter,wbarea_permanent_identifier,fdate,OBJECTID` | `-105.2330535,39.2527094,-105.2295676,39.2554196` | 250 / 1 | 1 | 1 |
| douglas-co 6 support_for=00201759 | 6 | `gnis_name IS NULL OR gnis_name = ''` | `permanent_identifier,gnis_id,gnis_name,ftype,fcode,reachcode,lengthkm,visibilityfilter,wbarea_permanent_identifier,fdate,OBJECTID` | `-105.208909,39.2907573,-105.2054221,39.2934667` | 250 / 1 | 2 | 2 |
| douglas-co 6 support_for=00201759 | 6 | `gnis_name IS NULL OR gnis_name = ''` | `permanent_identifier,gnis_id,gnis_name,ftype,fcode,reachcode,lengthkm,visibilityfilter,wbarea_permanent_identifier,fdate,OBJECTID` | `-105.207331,39.2940363,-105.2038441,39.2967457` | 250 / 1 | 3 | 3 |
| douglas-co 6 support_for=00201759 | 6 | `gnis_name IS NULL OR gnis_name = ''` | `permanent_identifier,gnis_id,gnis_name,ftype,fcode,reachcode,lengthkm,visibilityfilter,wbarea_permanent_identifier,fdate,OBJECTID` | `-105.2068349,39.2913878,-105.2033481,39.2940972` | 250 / 1 | 2 | 2 |
| douglas-co 6 support_for=00201759 | 6 | `gnis_name IS NULL OR gnis_name = ''` | `permanent_identifier,gnis_id,gnis_name,ftype,fcode,reachcode,lengthkm,visibilityfilter,wbarea_permanent_identifier,fdate,OBJECTID` | `-105.20647,39.2928613,-105.2029831,39.2955707` | 250 / 1 | 6 | 6 |
| douglas-co 6 support_for=00201759 | 6 | `gnis_name IS NULL OR gnis_name = ''` | `permanent_identifier,gnis_id,gnis_name,ftype,fcode,reachcode,lengthkm,visibilityfilter,wbarea_permanent_identifier,fdate,OBJECTID` | `-105.1855805,39.3307661,-105.1820926,39.3334749` | 250 / 1 | 8 | 8 |
| douglas-co 6 support_for=00201759 | 6 | `gnis_name IS NULL OR gnis_name = ''` | `permanent_identifier,gnis_id,gnis_name,ftype,fcode,reachcode,lengthkm,visibilityfilter,wbarea_permanent_identifier,fdate,OBJECTID` | `-105.1729728,39.3745198,-105.1694832,39.3772282` | 250 / 1 | 4 | 4 |
| douglas-co 6 support_for=00201759 | 6 | `gnis_name IS NULL OR gnis_name = ''` | `permanent_identifier,gnis_id,gnis_name,ftype,fcode,reachcode,lengthkm,visibilityfilter,wbarea_permanent_identifier,fdate,OBJECTID` | `-105.1724978,39.3739208,-105.1690082,39.3766292` | 250 / 1 | 6 | 6 |
| douglas-co 6 support_for=00201759 | 6 | `gnis_name IS NULL OR gnis_name = ''` | `permanent_identifier,gnis_id,gnis_name,ftype,fcode,reachcode,lengthkm,visibilityfilter,wbarea_permanent_identifier,fdate,OBJECTID` | `-105.1721955,39.3802578,-105.1687056,39.3829661` | 250 / 1 | 8 | 8 |
| douglas-co 6 support_for=00201759 | 6 | `gnis_name IS NULL OR gnis_name = ''` | `permanent_identifier,gnis_id,gnis_name,ftype,fcode,reachcode,lengthkm,visibilityfilter,wbarea_permanent_identifier,fdate,OBJECTID` | `-105.1720923,39.3736668,-105.1686028,39.3763751` | 250 / 1 | 6 | 6 |
| douglas-co 6 support_for=00201759 | 6 | `gnis_name IS NULL OR gnis_name = ''` | `permanent_identifier,gnis_id,gnis_name,ftype,fcode,reachcode,lengthkm,visibilityfilter,wbarea_permanent_identifier,fdate,OBJECTID` | `-105.172008,39.3801448,-105.1685181,39.3828531` | 250 / 1 | 8 | 8 |
| douglas-co 6 support_for=00201759 | 6 | `gnis_name IS NULL OR gnis_name = ''` | `permanent_identifier,gnis_id,gnis_name,ftype,fcode,reachcode,lengthkm,visibilityfilter,wbarea_permanent_identifier,fdate,OBJECTID` | `-105.1714329,39.3794013,-105.1679431,39.3821096` | 250 / 1 | 8 | 8 |
| douglas-co 6 support_for=00201759 | 6 | `gnis_name IS NULL OR gnis_name = ''` | `permanent_identifier,gnis_id,gnis_name,ftype,fcode,reachcode,lengthkm,visibilityfilter,wbarea_permanent_identifier,fdate,OBJECTID` | `-105.1323827,39.4583799,-105.1288904,39.461087` | 250 / 1 | 4 | 4 |
| douglas-co 6 support_for=00201759 | 6 | `gnis_name IS NULL OR gnis_name = ''` | `permanent_identifier,gnis_id,gnis_name,ftype,fcode,reachcode,lengthkm,visibilityfilter,wbarea_permanent_identifier,fdate,OBJECTID` | `-105.128957,39.4565565,-105.125465,39.4592635` | 250 / 1 | 10 | 10 |
| douglas-co 6 support_for=00201759 | 6 | `gnis_name IS NULL OR gnis_name = ''` | `permanent_identifier,gnis_id,gnis_name,ftype,fcode,reachcode,lengthkm,visibilityfilter,wbarea_permanent_identifier,fdate,OBJECTID` | `-105.0802126,39.5173707,-105.0767194,39.5200762` | 250 / 1 | 1 | 1 |
| douglas-co 6 support_for=00201759 | 6 | `gnis_name IS NULL OR gnis_name = ''` | `permanent_identifier,gnis_id,gnis_name,ftype,fcode,reachcode,lengthkm,visibilityfilter,wbarea_permanent_identifier,fdate,OBJECTID` | `-105.0666383,39.5531114,-105.0631438,39.5558165` | 250 / 0 | 0 | 0 |

## Difference summary

All legacy matching used exact canonical clipped-geometry JSON equality within one source layer. Row position was never used. Duplicate geometry on either side is treated as ambiguous and does not match. OBJECTID was used only as a diagnostic when exact geometry did not match.

| Region/layer | Before | After | Exact matches | Added | Removed | Geometry changes | Name changes | Unmatched old / new |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| aspen/flowline | 6411 | 6411 | 6411 | 0 | 0 | 0 | 0 | 0 / 0 |
| aspen/area | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 / 0 |
| aspen/waterbody | 514 | 514 | 514 | 0 | 0 | 0 | 0 | 0 / 0 |
| douglas-co/flowline | 2359 | 2359 | 2359 | 0 | 0 | 0 | 0 | 0 / 0 |
| douglas-co/waterbody | 33 | 2135 | 33 | 2102 | 0 | 0 | 0 | 0 / 2102 |

No existing feature was removed; no existing geometry or name changed. Aspen has no additions. Douglas has 2,102 added unnamed waterbodies, all within the approved scope. The offline recomputation from saved raw pages and staged layers set `acceptable_differences_only` to `True`.

### Counts by source type and code

### aspen/flowline

Before: 6411 total (1512 named, 4899 unnamed); baseline retained no ftype/fcode values. After: 6411 total (1512 named, 4899 unnamed).

| ftype | fcode | count | water_class | hydro_category |
|---:|---:|---:|---|---|
| 334 | 33400 | 65 | connector | unknown |
| 336 | 33600 | 170 | canal_ditch | unknown |
| 428 | 42800 | 2 | pipeline | unknown |
| 428 | 42802 | 3 | pipeline | unknown |
| 428 | 42803 | 8 | pipeline | unknown |
| 460 | 46003 | 1804 | stream | intermittent |
| 460 | 46006 | 1466 | stream | perennial |
| 460 | 46007 | 2425 | stream | ephemeral |
| 558 | 55800 | 468 | artificial_path | unknown |

### aspen/area

Before: 1 total (0 named, 1 unnamed); baseline retained no ftype/fcode values. After: 1 total (0 named, 1 unnamed).

| ftype | fcode | count | water_class | hydro_category |
|---:|---:|---:|---|---|
| 460 | 46006 | 1 | stream | perennial |

### aspen/waterbody

Before: 514 total (43 named, 471 unnamed); baseline retained no ftype/fcode values. After: 514 total (43 named, 471 unnamed).

| ftype | fcode | count | water_class | hydro_category |
|---:|---:|---:|---|---|
| 390 | 39000 | 3 | lake_pond | unknown |
| 390 | 39001 | 36 | lake_pond | intermittent |
| 390 | 39004 | 402 | lake_pond | perennial |
| 390 | 39009 | 10 | lake_pond | perennial |
| 436 | 43624 | 5 | reservoir | unknown |
| 466 | 46600 | 58 | swamp_marsh | unknown |

### douglas-co/flowline

Before: 2359 total (2359 named, 0 unnamed); baseline retained no ftype/fcode values. After: 2359 total (2359 named, 0 unnamed).

| ftype | fcode | count | water_class | hydro_category |
|---:|---:|---:|---|---|
| 334 | 33400 | 1 | connector | unknown |
| 336 | 33600 | 73 | canal_ditch | unknown |
| 428 | 42803 | 6 | pipeline | unknown |
| 428 | 42807 | 3 | pipeline | unknown |
| 428 | 42813 | 3 | pipeline | unknown |
| 460 | 46003 | 504 | stream | intermittent |
| 460 | 46006 | 1514 | stream | perennial |
| 558 | 55800 | 255 | artificial_path | unknown |

### douglas-co/waterbody

Before: 33 total (33 named, 0 unnamed); baseline retained no ftype/fcode values. After: 2135 total (33 named, 2102 unnamed).

| ftype | fcode | count | water_class | hydro_category |
|---:|---:|---:|---|---|
| 390 | 39001 | 1402 | lake_pond | intermittent |
| 390 | 39004 | 685 | lake_pond | perennial |
| 390 | 39005 | 2 | lake_pond | intermittent |
| 390 | 39009 | 8 | lake_pond | perennial |
| 390 | 39011 | 7 | lake_pond | perennial |
| 436 | 43601 | 1 | reservoir | unknown |
| 436 | 43612 | 6 | reservoir | unknown |
| 436 | 43613 | 2 | reservoir | unknown |
| 436 | 43619 | 1 | reservoir | unknown |
| 436 | 43624 | 20 | reservoir | unknown |
| 466 | 46600 | 1 | swamp_marsh | unknown |

### Elevation unit

The NHD layer 12 source field is `ELEVATION`. Its service range domain is `[-400, 9000]`; the service metadata includes no unit. The retained values are exact multiples of 0.3048: Whites Lake 2827.9344 (9,278 ft × 0.3048), Crater Lake 3071.1648 (10,076 ft × 0.3048), and Maroon Lake 2919.984 (9,580 ft × 0.3048). This confirms the source values are metres. There are 10 non-null elevations among Aspen's 514 waterbodies and 10 among Douglas's 2,135 waterbodies. The canonical property is `elevation_m`; each value is stored unconverted at the source value and precision.


### Douglas supporting-feature review

- Named flowline segments: 2,359.
- Qualifying gap boxes examined: 26; end points were rounded to six decimal places and candidate gaps were at most 250 m, with each query box 300 m wide.
- Unnamed supporting segments kept: 0 (water_class counts: none). No rivers received supporting segments.
- GNIS IDs examined: `00185006 (Arapahoe Canal), 00201759 (South Platte River)`.

### Complete legacy ID and unmatched-feature lists

The complete old ID to new ID mapping and unmatched-feature list is in [`nhd-snapshot-id-map.csv`](nhd-snapshot-id-map.csv) (11420 data rows: 9318 exact-geometry legacy mappings and 2102 new features without an old geometry match; no old IDs were unmatched). Rows with an empty `legacy_id` record additions. The mapping is also recoverable from canonical `legacy_ids` properties.

## Display preservation and bytes

The multiset of display geometries is identical by water display layer:

| Display layer | Before features | After features | Geometry multiset identical |
|---|---:|---:|---|
| Aspen `flowline` | 1512 | 1512 | True |
| Aspen `waterbody` | 43 | 43 | True |
| Aspen `area` | 0 | 0 | True |
| Douglas `waterways` | 2359 | 2359 | True |
| Douglas `waterbodies` | 33 | 33 | True |

The unchanged current selection rule displays named flowlines and named waterbodies. Aspen retains 1,512 named flowlines and 43 named waterbodies; its water-area layer has no displayed features. Douglas retains 2,359 named waterways and 33 named waterbodies. New source fields and derived values remain complete in canonical data. The coordinator-approved M4-A size fallback limits display water properties to `id`, `name`, the evidence reference and the selection fields (`kind` in Aspen, `source_layer` in Douglas); other new display properties are deferred to M4-B.

| Water artifact | Before bytes | After bytes |
|---|---:|---:|
| Aspen hydrology | 1134855 | 1163589 |
| Douglas waterways | 1770773 | 1786803 |
| Douglas waterbodies | 116952 | 117180 |

The alias maps live in `water-aliases.json`, outside default-loaded artifacts: Aspen `61732` bytes; Douglas `88729` bytes. Each index contains only the alias file path, byte count and SHA-256 digest. The browser does not request either file during initial map or default-layer load.

| Region | Bytes-to-map-usable before | after | Default-on total before | after | Limits |
|---|---:|---:|---:|---:|---|
| Aspen | 341,777 | 342,266 | 3,816,308 | 3,845,531 | 500,000 / 4,500,000 |
| Douglas | 412,528 | 413,143 | 3,626,603 | 3,643,476 | 500,000 / 4,500,000 |

The byte totals use the repository's static budget calculation over the map-usable resources and default display artifacts; the final browser check independently reports the runtime resource totals.

## Non-water preservation

Parsed JSON comparison against `origin/main` found every non-water canonical layer equal:

- `v2/map-data-v2.json`: `land_ownership`, `wilderness`, `mvum_roads`, `lodging_developed`, `wildlife_sensitivity`, `fire_restriction_stage`, `dispersed_corridors`, `dispersed_corridor_points`, `leads`, `reviewed_sites` (all equal: True).
- `v2/regions/douglas-co/research.json`: `coverage`, `trails`, `roads`, `recreation`, `land`, `wilderness` (all equal: True).

All non-water display GeoJSON artifacts are byte-identical to `origin/main`: `True` (18 artifacts). Non-water `source_status` entries and other top-level canonical fields are also unchanged. The only canonical data changes are Aspen `hydrology`, Douglas `waterways`/`waterbodies`, their water source status records, the two water manifest declarations, and the related display artifacts/indexes/alias files. Douglas `manager` was removed only from `waterways` and `waterbodies`.

## Informational unknown-code inventory

These are the snapshot-observed fcodes that map to `hydro_category: unknown`; this list does not drive classification. `domain_text` is null when the source notes did not retain a code-level label.

```json
[
  {
    "domain_text": "network link",
    "fcode": 33400
  },
  {
    "domain_text": "canal or ditch",
    "fcode": 33600
  },
  {
    "domain_text": null,
    "fcode": 39000
  },
  {
    "domain_text": null,
    "fcode": 42800
  },
  {
    "domain_text": null,
    "fcode": 42802
  },
  {
    "domain_text": null,
    "fcode": 42803
  },
  {
    "domain_text": null,
    "fcode": 42807
  },
  {
    "domain_text": null,
    "fcode": 42813
  },
  {
    "domain_text": "aquaculture",
    "fcode": 43601
  },
  {
    "domain_text": "sewage treatment pond",
    "fcode": 43612
  },
  {
    "domain_text": "water storage",
    "fcode": 43613
  },
  {
    "domain_text": "construction material only",
    "fcode": 43619
  },
  {
    "domain_text": "treatment",
    "fcode": 43624
  },
  {
    "domain_text": null,
    "fcode": 46600
  },
  {
    "domain_text": "modelled centre line through lake or wide river",
    "fcode": 55800
  }
]
```

## Service snapshot and implementation limits

- The NHD service response included currentVersion `11.3` and documentInfo Version `3.3.0`; it did not include a source data-date. Values are source-fetched context and do not establish recreation, access or permission.
- No 3DHP identifiers were requested or stored. No selection rule, geometry, non-water layer, UI wording, styling or map interaction was changed.
- Aspen canonical hydrology still contains all 6,926 features; geometry matches all current features. Stage 07 was not re-run, and identical Aspen hydrology geometries mean its setback-screening corridors need no change.

## M4-B section 1 — BLOCKED_EXTERNAL: USGS NHD SERVICE DEGRADED

The owner-authorized Douglas padded-water refresh did not obtain any feature
response pages. The only saved source response is the service metadata; four
attempts reached read-timeout or repeated HTTP 504 failures before a complete
layer-6 count and object-ID plan could be saved. Attempt 3 was the final
attempt under the initial owner decision. Attempt 4 was one controlled retry
scheduled by the coordinator under the owner's instruction that a later retry
may be made, with the same query policy, when the work reaches the point that
needs the padded data. No M4-A response page was used, and canonical data,
manifests and display artifacts were not changed.

### Service and query scope

- Endpoint: `https://hydro.nationalmap.gov/arcgis/rest/services/nhd/MapServer`.
- Saved service metadata: `currentVersion` `11.3`, documentInfo Version
  `3.3.0`; the metadata contains no source data-date text.
- Requested layers: 6 (flowline) and 12 (waterbody). No layer 9 or Aspen
  request was made.
- Geographic clip: `county.buffer(0.005)`. Query envelope, WGS84
  minX,minY,maxX,maxY: `-105.33444166966446,39.1244790184437,-104.65558407460871,39.57119268762119`.
- Intended layer 6 query: `where=gnis_name IS NOT NULL AND gnis_name <> ''`;
  `outFields=permanent_identifier,gnis_id,gnis_name,ftype,fcode,reachcode,lengthkm,visibilityfilter,wbarea_permanent_identifier,fdate,OBJECTID`;
  feature page size 250.
- Intended layer 12 query: `where=1=1`;
  `outFields=PERMANENT_IDENTIFIER,GNIS_ID,GNIS_NAME,FTYPE,FCODE,AREASQKM,ELEVATION,REACHCODE,VISIBILITYFILTER,FDATE,OBJECTID`;
  feature page size 250.
- O1 support query where-clause, if qualifying gap boxes had been derived:
  `gnis_name IS NULL OR gnis_name = ''`; its boxes were never computed because
  no layer-6 features were retrieved. Supporting-feature count is therefore
  **not determined**, not zero.
- Count-only and ID-only requests carry no `outFields` and no feature page
  size. The first count-only request used a 90 second read timeout. Attempts 2
  and 3 configured 180 seconds for count and ID requests; page size and query
  logic were unchanged.

### Attempt record (UTC)

| Attempt | Request reached | Outcome |
|---|---|---|
| 1 — metadata response saved at `2026-10-07T20:52:11.910813Z`; the feature query followed immediately | Layer 6 count-only query with the intended named-flowline where-clause and padded envelope | Read timeout after the 90 second timeout policy and configured retries; failed, observed by the worker at `2026-10-07T21:01:17Z`. No count, ID plan or feature page was saved. |
| 2 — started `2026-10-07T21:03:10.791689Z` | Layer 6 metadata endpoint `/6?f=json` | Repeated HTTP 504 responses; failed at `2026-10-07T21:03:24.193607Z`, before the count query. |
| 3 — started `2026-10-07T21:21:13.336794Z` | Layer 6 count-only query with the same named-flowline where-clause and padded envelope; the layer-6 metadata response was saved | Repeated HTTP 504 responses; failed at `2026-10-07T21:21:29.489422Z`. This was the final attempt under the initial owner decision. |
| 4 — started `2026-10-08T00:27:09.546312Z` | Layer 6 count-only query: `where=gnis_name IS NOT NULL AND gnis_name <> ''`, envelope `-105.33444166966446,39.1244790184437,-104.65558407460871,39.57119268762119` | Repeated HTTP 504 responses (`RetryError: too many 504 error responses`); failed at `2026-10-08T00:33:12.832201Z`, before the count query completed. This was the one controlled retry scheduled by the coordinator under the owner's retry-later instruction. |

The saved service metadata and all four attempt records remain under the
ignored `v2/pipeline/data/raw/m4b-douglas-water/` directory. No count or ID
request completed, so returned feature counts are unavailable for both layers;
layer 12 and O1 support queries were not reached. No staging difference report
was produced. Additions, removals, geometry changes, name changes, and the list
of lengthened IDs are **not evaluated**; these are not inferred to be zero.

### Canonical state left unchanged

The current canonical Douglas counts below are both the pre-attempt and
post-attempt counts because apply was never run. The values are canonical
NHD-source counts, not results from the failed refresh.

| Layer | Features | ftype | fcode | Count |
|---|---:|---:|---:|---:|
| waterways | 2,359 | 334 | 33400 | 1 |
| waterways | 2,359 | 336 | 33600 | 73 |
| waterways | 2,359 | 428 | 42803 | 6 |
| waterways | 2,359 | 428 | 42807 | 3 |
| waterways | 2,359 | 428 | 42813 | 3 |
| waterways | 2,359 | 460 | 46003 | 504 |
| waterways | 2,359 | 460 | 46006 | 1,514 |
| waterways | 2,359 | 558 | 55800 | 255 |
| waterbodies | 2,135 | 390 | 39001 | 1,402 |
| waterbodies | 2,135 | 390 | 39004 | 685 |
| waterbodies | 2,135 | 390 | 39005 | 2 |
| waterbodies | 2,135 | 390 | 39009 | 8 |
| waterbodies | 2,135 | 390 | 39011 | 7 |
| waterbodies | 2,135 | 436 | 43601 | 1 |
| waterbodies | 2,135 | 436 | 43612 | 6 |
| waterbodies | 2,135 | 436 | 43613 | 2 |
| waterbodies | 2,135 | 436 | 43619 | 1 |
| waterbodies | 2,135 | 436 | 43624 | 20 |
| waterbodies | 2,135 | 466 | 46600 | 1 |

`v2/regions/douglas-co/research.json` SHA-256 before/after this work:
`cf7e6852a8549c5e63e12ef07ddbe9a30ace7323a3e874219eb6a7c9d03969ab`.
The South Platte source ID `117795757` is not present in the current canonical
water layers; the failed refresh could not establish whether it is now
available from the source. The lengthened-feature count and O1 supporting
feature count remain undetermined.

No canonical bundle, manifest, or display artifact changed. The unchanged
`v2/map-data-v2.json` SHA-256 is
`d244adea6d600f6530b2cbcb3b859ea5647c448c1737e1f9508e3d1e9a0143fe`; the
combined SHA-256 over all 18 files in `v2/regions/aspen/` (sorted relative
paths and each file's SHA-256) is
`1eb72f89701553509a13807248b5760be01cb2339678fedbcaeb589025e782a5`.
The aggregate SHA-256 of canonical non-water layer hashes is
`0e9efb81f456682c87d23bf8c292f7b396161db88e766cf453f9704b1d089e16` for the
Aspen bundle and
`737ad420382d161e22bcab28e1f18a33007442fa0e64da78885dabbca9c669e9` for
Douglas; these digests use sorted layer names and canonical JSON layer
content.
Douglas currently uses 413,116 bytes to map-usable resources and 3,643,449
bytes for the default-on total, below the 500,000 and 4,500,000 limits.

## M4-B section 2 — BLOCKED_EXTERNAL: NHD SERVICE CANNOT COMPLETE PADDED DOUGLAS REFRESH

The one coordinator-approved session using the owner-approved object-ID
retrieval strategy failed before layer 6 object-ID discovery. The layer 6
count-only request returned repeated HTTP 504 responses and exhausted the
configured HTTP retries. Live fetching stopped at that failure. No layer 6
count, object-ID plan, response page, or layer 12 result was obtained; the
four earlier attempts remain recorded in M4-B section 1 and were not changed.

### Approved strategy and exact request

- Session started `2026-10-08T01:00:35.241139Z` and failed
  `2026-10-08T01:05:48.775435Z` UTC. This was attempt 1 in the new ignored
  directory `v2/pipeline/data/raw/m4b-douglas-water-objectid/`; its durable
  attempt record identifies the prior four-attempt directory as
  `v2/pipeline/data/raw/m4b-douglas-water/`.
- The failed query was the layer 6 count-only request at
  `https://hydro.nationalmap.gov/arcgis/rest/services/nhd/MapServer/6/query`
  with `where=1=1`, `geometry=-105.33444166966446,39.1244790184437,-104.65558407460871,39.57119268762119`,
  `geometryType=esriGeometryEnvelope`, `inSR=4326`,
  `spatialRel=esriSpatialRelIntersects`, `f=json`,
  `returnCountOnly=true`, and a 180 second timeout. The service returned
  `RetryError: too many 504 error responses`; the count is unavailable.
- The intended layer 6 object-ID discovery request used the same padded
  envelope and spatial relation with `where=1=1` and
  `returnIdsOnly=true`. It was not sent because the count request failed.
- The layer 6 page request, with the existing outFields and 250 object-ID page
  size, was not reached. Layer 12's unchanged `where=1=1` count, ID discovery
  and page requests were not reached. No O1 boxes or local candidates were
  derived.
- Service metadata (`currentVersion` 11.3, documentInfo Version 3.3.0) and
  layer 6 metadata were saved in the new raw directory. No response pages or
  staging difference report were produced.

The prior four failures all occurred under the original layer 6 named-feature
count query `where=gnis_name IS NOT NULL AND gnis_name <> ''`; their attempt
records and saved metadata remain unchanged in the earlier raw directory.
This session used only the approved change of strategy: layer 6 object IDs by
the padded envelope with `where=1=1`, exact local name filtering after saved
pages, and local O1 derivation from those saved layer 6 rows. The local 300 m
box check is equivalent to the replaced envelope-intersects query because it
tests the saved source geometry against the same gap-box envelope with the
same intersection predicate. Layer 12, host, layers, padded clip polygon,
fields, page size and count/ID timeout policy were unchanged.

No result counts, source-ID comparison, existing-feature comparison, South
Platte expected-major-river check, or difference classification can be made
from this failed session. No canonical data, manifest, display artifact,
selection report, or tracked raw response page was written or changed. Any
future retrieval attempt requires renewed owner review.

## BLOCKED_EXTERNAL_PARTIAL: NHD TILED REFRESH INCOMPLETE

The owner-approved tiled session at reviewed head cb4d9c5 started 2026-10-08T13:23:11.605408Z and stopped 2026-10-08T14:25:41.693942Z UTC.
Stop reason: layer 6 level-2 tile 3.1.1 failed twice. Live fetching stopped; no other strategy was tried.
Endpoint: https://hydro.nationalmap.gov/arcgis/rest/services/nhd/MapServer; intended layers 6 and 12 only. Saved currentVersion 11.3, documentInfo Version 3.3.0; no source data-date was inferred.
Approved clip remains county.buffer(0.005); full padded envelope: -105.33444166966446,39.1244790184437,-104.65558407460871,39.57119268762119.
Initial deterministic 2x2 tiles are SW (0), SE (1), NW (2), NE (3), with shared edges computed once. Only a twice-failed tile divides into four children, to a maximum two levels below the initial grid (1/64 of the original envelope).
Queries use where=1=1, geometryType=esriGeometryEnvelope, inSR=4326, spatialRel=esriSpatialRelIntersects, f=json, and either returnCountOnly=true or returnIdsOnly=true. Geometry is each exact tile envelope below. Every request and response is saved before interpretation in the new ignored v2/pipeline/data/raw/m4b-douglas-water-tiled directory.
Requests use the committed 180 second count/ID timeout, at most two tile attempts, at least 60 seconds between attempts on the same tile and at least 2 seconds between any requests, without hidden HTTP or ArcGIS retries.
Discovery requests per layer, including retries: {"6": 31}; total HTTP requests including metadata: 33; hard cap 150 per layer was not reached.
Saved valid feature pages: 0. No final layer result, staging canonical output, canonical apply, manifest change, display rebuild or selection-report change occurred.
The earlier four named-filter failures and the fifth full-envelope where=1=1 failure remain recorded above; all nine earlier raw files are byte-identical to their pre-session hashes.

| Layer | Tile | Depth | Exact envelope (WGS84 west,south,east,north) | Outcome | Attempts | Accepted leaf IDs | Attempt outcomes and returned counts |
|---|---|---:|---|---|---:|---:|---|
| 6 | 0 | 0 | -105.33444166966446,39.1244790184437,-104.99501287213658,39.34783585303245 | complete | 2 | 20190 | 1: service_failure, UTC 2026-10-08T13:23:14.688249+00:00, count None, IDs unavailable; 2: complete, UTC 2026-10-08T13:27:16.710014+00:00, count 20190, IDs 20190 |
| 6 | 1 | 0 | -104.99501287213658,39.1244790184437,-104.65558407460871,39.34783585303245 | complete | 1 | 3668 | 1: complete, UTC 2026-10-08T13:28:07.350328+00:00, count 3668, IDs 3668 |
| 6 | 2 | 0 | -105.33444166966446,39.34783585303245,-104.99501287213658,39.57119268762119 | complete | 1 | 10923 | 1: complete, UTC 2026-10-08T13:30:18.064486+00:00, count 10923, IDs 10923 |
| 6 | 3 | 0 | -104.99501287213658,39.34783585303245,-104.65558407460871,39.57119268762119 | subdivided | 2 | unavailable | 1: service_failure, UTC 2026-10-08T13:32:11.196462+00:00, count 3141, IDs unavailable; 2: service_failure, UTC 2026-10-08T13:38:41.563187+00:00, count None, IDs unavailable |
| 6 | 3.0 | 1 | -104.99501287213658,39.34783585303245,-104.82529847337264,39.45951427032682 | subdivided | 2 | unavailable | 1: service_failure, UTC 2026-10-08T13:41:41.834918+00:00, count None, IDs unavailable; 2: service_failure, UTC 2026-10-08T13:45:43.995979+00:00, count None, IDs unavailable |
| 6 | 3.0.0 | 2 | -104.99501287213658,39.34783585303245,-104.91015567275461,39.403675061679635 | complete | 1 | 252 | 1: complete, UTC 2026-10-08T13:48:44.309798+00:00, count 252, IDs 252 |
| 6 | 3.0.1 | 2 | -104.91015567275461,39.34783585303245,-104.82529847337264,39.403675061679635 | complete | 1 | 163 | 1: complete, UTC 2026-10-08T13:51:15.412880+00:00, count 163, IDs 163 |
| 6 | 3.0.2 | 2 | -104.99501287213658,39.403675061679635,-104.91015567275461,39.45951427032682 | complete | 1 | 341 | 1: complete, UTC 2026-10-08T13:56:01.432471+00:00, count 341, IDs 341 |
| 6 | 3.0.3 | 2 | -104.91015567275461,39.403675061679635,-104.82529847337264,39.45951427032682 | complete | 2 | 176 | 1: service_failure, UTC 2026-10-08T13:58:28.620547+00:00, count None, IDs unavailable; 2: complete, UTC 2026-10-08T14:02:30.597902+00:00, count 176, IDs 176 |
| 6 | 3.1 | 1 | -104.82529847337264,39.34783585303245,-104.65558407460871,39.45951427032682 | subdivided | 2 | unavailable | 1: service_failure, UTC 2026-10-08T14:02:52.844210+00:00, count None, IDs unavailable; 2: service_failure, UTC 2026-10-08T14:06:54.820801+00:00, count 748, IDs unavailable |
| 6 | 3.1.0 | 2 | -104.82529847337264,39.34783585303245,-104.74044127399068,39.403675061679635 | complete | 2 | 169 | 1: service_failure, UTC 2026-10-08T14:11:40.957874+00:00, count 169, IDs unavailable; 2: complete, UTC 2026-10-08T14:17:17.678352+00:00, count 169, IDs 169 |
| 6 | 3.1.1 | 2 | -104.74044127399068,39.34783585303245,-104.65558407460871,39.403675061679635 | EXTERNALLY_BLOCKED | 2 | unavailable | 1: service_failure, UTC 2026-10-08T14:18:28.553870+00:00, count None, IDs unavailable; 2: service_failure, UTC 2026-10-08T14:22:30.524882+00:00, count 198, IDs unavailable |
| 6 | 3.1.2 | 2 | -104.82529847337264,39.403675061679635,-104.74044127399068,39.45951427032682 | NOT_REQUESTED | 0 | unavailable | none |
| 6 | 3.1.3 | 2 | -104.74044127399068,39.403675061679635,-104.65558407460871,39.45951427032682 | NOT_REQUESTED | 0 | unavailable | none |
| 6 | 3.2 | 1 | -104.99501287213658,39.45951427032682,-104.82529847337264,39.57119268762119 | NOT_REQUESTED | 0 | unavailable | none |
| 6 | 3.3 | 1 | -104.82529847337264,39.45951427032682,-104.65558407460871,39.57119268762119 | NOT_REQUESTED | 0 | unavailable | none |

Layer 6 has 16 tile definitions, 3 subdivided parents and 8 accepted leaves; partial leaf-ID count 35882, partial unique object IDs 35621, partial boundary duplicates 261. These are partial object-ID observations, not complete source-record counts.
Unresolved tiles and exact envelopes: [{"envelope": [-104.99501287213658, 39.45951427032682, -104.82529847337264, 39.57119268762119], "id": "3.2"}, {"envelope": [-104.82529847337264, 39.45951427032682, -104.65558407460871, 39.57119268762119], "id": "3.3"}, {"envelope": [-104.74044127399068, 39.34783585303245, -104.65558407460871, 39.403675061679635], "id": "3.1.1"}, {"envelope": [-104.82529847337264, 39.403675061679635, -104.74044127399068, 39.45951427032682], "id": "3.1.2"}, {"envelope": [-104.74044127399068, 39.403675061679635, -104.65558407460871, 39.45951427032682], "id": "3.1.3"}].

Layer 12's planned initial grid was wholly NOT_REQUESTED:

| Layer | Tile | Exact envelope | Outcome |
|---|---|---|---|
| 12 | 0 | -105.33444166966446,39.1244790184437,-104.99501287213658,39.34783585303245 | NOT_REQUESTED |
| 12 | 1 | -104.99501287213658,39.1244790184437,-104.65558407460871,39.34783585303245 | NOT_REQUESTED |
| 12 | 2 | -105.33444166966446,39.34783585303245,-104.99501287213658,39.57119268762119 | NOT_REQUESTED |
| 12 | 3 | -104.99501287213658,39.34783585303245,-104.65558407460871,39.57119268762119 | NOT_REQUESTED |

Layer 12 was not reached. Named-flowline, O1-support, unnamed-discarded, waterbody and final permanent-identifier counts are not determined; local derivation never ran.
Retrieval differences, South Platte member count, drawn length/fraction/lines and padding side effects are not evaluated from partial coverage. No missing tile is approximated.
Canonical Douglas remains 2,359 waterways and 2,135 waterbodies. Canonical mutations (added, lengthened, removed and changed-name features) are all zero because apply did not run; this is not a comparison of complete retrieved data.
Douglas canonical SHA-256 before/after: 55f0896051697fc52b46add755e89a0a7f9e14f267d5b6884788da58f0165e9d. All Aspen files and every Douglas non-water layer retain their pre-session hashes.
The ignored staging directory contains no canonical GeoJSON or refresh report. The pending_external_source_refresh marker remains; data integration and Gate 2 are blocked. Independent offline Part E work proceeds; any new live session needs renewed owner review.

### Section 8 historical STILL INCOMPLETE outcome and operator continuation

The section-8 usage stop interrupted page 52 after 51 accepted pages (12,750 records). The one blocked-snapshot resume had already been consumed at 2026-10-08T16:16:36.720894Z, and layer-6 discovery was complete: 37,680 unique IDs in 13 leaves, eight original and five resumed. The interrupted request file and its top-level running attempt record remain byte-identical.
A Hermes operator then ran plain --run four times: 17:06:29Z replayed interrupted page 52 with no request and stopped ResumeLater; 17:23:30Z completed page 52 on attempt 2 and page 53 failed HTTP 504; 17:41:13Z completed page 53 on attempt 2 and pages 54–55, then page 56 failed HTTP 504; 17:57:27Z retried page 56 and reached a 120-second read timeout, stopping ExternalBlocked at 17:59:30Z. Section 8 was STILL INCOMPLETE with 55/151 pages, 13,750 saved records, no final verification or layer 12, and no canonical mutation. This historical block was lifted only by the owner-approved section-9 transport policy; the earlier failures were not erased.

### Durable retry policy and complete attempt accounting

Version 1 is four total attempts per page, including all old/interrupted attempts, at least 900 seconds after the previous attempt finished and unchanged two-second global pacing. Service failures queue while other pages proceed, followed by eligible retries inside the process. Valid accepted pages are immutable and never requested again. The migration UTC and previous page-terminal error are retained in the saved plan/session; no second --resume-blocked was consumed. Tile discovery and final per-leaf verification are unchanged.
Actual saved histories satisfy the four-attempt budget, 900-second same-page interval and global request pacing. Exhausted pages: none. Full original/operator/section-9 record outcomes, times, errors, batch sizes, fields and request hashes: [record attempt sidecar](nhd-padded-record-attempts.csv). All tiled HTTP attempts, including metadata, original and resumed discovery and verification: [request history](nhd-padded-request-history.csv). Object-ID lists and raw features remain ignored.
Total tiled HTTP requests 238, of which 136 are new in section 9; record-page attempts 169. Earlier full-envelope sessions used hidden retries, so their underlying HTTP counts are unavailable rather than inferred.
Record-page transient failures by page and attempt: [{"attempt": 1, "error": "request interrupted; response unknown", "layer": "6", "page": 52, "utc": "2026-10-08T16:22:05.874718+00:00"}, {"attempt": 1, "error": "HTTP 504", "layer": "6", "page": 53, "utc": "2026-10-08T17:24:26.699842+00:00"}, {"attempt": 1, "error": "HTTP 504", "layer": "6", "page": 56, "utc": "2026-10-08T17:41:47.733393+00:00"}, {"attempt": 2, "error": "HTTPSConnectionPool(host='hydro.nationalmap.gov', port=443): Read timed out. (read timeout=120)", "layer": "6", "page": 56, "utc": "2026-10-08T17:57:30.300743+00:00"}, {"attempt": 3, "error": "HTTPSConnectionPool(host='hydro.nationalmap.gov', port=443): Read timed out. (read timeout=120)", "layer": "6", "page": 56, "utc": "2026-10-08T21:32:05.700870+00:00"}, {"attempt": 1, "error": "HTTPSConnectionPool(host='hydro.nationalmap.gov', port=443): Read timed out. (read timeout=120)", "layer": "6", "page": 62, "utc": "2026-10-08T21:37:15.973814+00:00"}, {"attempt": 1, "error": "HTTPSConnectionPool(host='hydro.nationalmap.gov', port=443): Read timed out. (read timeout=120)", "layer": "6", "page": 65, "utc": "2026-10-08T21:41:06.510973+00:00"}, {"attempt": 1, "error": "HTTP 502", "layer": "6", "page": 141, "utc": "2026-10-08T21:52:10.144584+00:00"}].
Final layer facts: {"12": {"boundary_duplicates_removed": 7, "final_verification": true, "original_leaves": 0, "pages": 10, "raw_leaf_ids": 2369, "records": 2362, "resumed_leaves": 4, "unique_ids": 2362}, "6": {"boundary_duplicates_removed": 367, "final_verification": true, "original_leaves": 8, "pages": 151, "raw_leaf_ids": 38047, "records": 37680, "resumed_leaves": 5, "unique_ids": 37680}}. Every discovered ID is present exactly once in saved pages; every permanent identifier is unique within and across layers. Every complete leaf passed final ID-set verification. Only shared tile-edge duplicates were removed; no source record was deduplicated by name or geometry.
All 187 pre-existing immutable tiled files and nine earlier raw files are byte-identical to their saved proofs. File hashes, including old/new request and accepted-page files: [integrity sidecar](nhd-padded-file-integrity.csv). Canonical Douglas SHA-256 before/after retrieval remains 55f0896051697fc52b46add755e89a0a7f9e14f267d5b6884788da58f0165e9d. No canonical/display/alias/selection artifact has been applied; Gate 2 is required.

## M4-B section 9 — Completed Douglas padded NHD retrieval

Reviewed page-policy head: a880be1932773c2a77bef10e0617b7a4e23633f6; original tiled transport head: cb4d9c5; session UTC range 2026-10-08T13:23:11.979699+00:00 to 2026-10-08T22:08:56.369383+00:00.
Source: https://hydro.nationalmap.gov/arcgis/rest/services/nhd/MapServer; layers 6 and 12 only. Service currentVersion 11.3; documentInfo Version 3.3.0.
The saved metadata is retained verbatim in the ignored raw directory; no source data-date is inferred from retrieval or service version.
Clip polygon: county.buffer(0.005); envelope: -105.33444166966446,39.1244790184437,-104.65558407460871,39.57119268762119.
Initial 2x2 rectangles share precomputed midpoints, ordered SW/SE/NW/NE. Only a failed tile can split into four children; at most two subdivision levels below the initial grid. Leaves cover the same envelope exactly.
The five earlier failed attempts remain above and in their original ignored directories; none was overwritten. Their full-envelope count queries are not rerun.
Each tile uses where=1=1, esriGeometryEnvelope, inSR=4326 and esriSpatialRelIntersects for returnCountOnly and returnIdsOnly, with a 180 second timeout. The per-tile count, IDs and raw response are saved before interpretation. Retries are at least 60 seconds apart per tile and every request at least 2 seconds apart.
Final verification rechecks each saved leaf ID set. Duplicate IDs across shared tile edges are expected, counted and removed before ascending-ID pages of 250 records. Permanent identifiers key the sorted staged records; geometry and names never deduplicate.

| Layer | Raw leaf IDs | Boundary duplicates removed | Unique source records | Before canonical | Staged after (not applied) | Added | Lengthened accepted | Removed | Changed name |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| waterways | 38047 | 367 | 37680 | 2359 | 2734 | 375 | 0 | 0 | 0 |
| waterbodies | 2369 | 7 | 2362 | 2135 | 2220 | 85 | 2 | 0 | 0 |

Requests: 238 total HTTP requests; discovery including retries and final verification: {"12": 12, "6": 54}.
Tile definitions: 20; subdivided parents: 3; completed leaves: 17.
Failed/retried attempts: 7 tiles with service failures; detailed outcomes, UTC times and full envelopes are in [the tile table](nhd-padded-tile-history.csv).
Local filter counts: {"named_flowlines": 3693, "named_flowlines_canonical": 2734, "support_gap_count": 1, "supporting_features_by_water_class": {}, "supporting_features_kept": 0, "supporting_gnis_names": {}, "unnamed_discarded": 33987, "unnamed_flowlines": 33987, "waterbodies": 2362, "waterbodies_canonical": 2220}.
Layer 6 outFields: permanent_identifier,gnis_id,gnis_name,ftype,fcode,reachcode,lengthkm,visibilityfilter,wbarea_permanent_identifier,fdate,OBJECTID.
Layer 12 outFields: PERMANENT_IDENTIFIER,GNIS_ID,GNIS_NAME,FTYPE,FCODE,AREASQKM,ELEVATION,REACHCODE,VISIBILITYFILTER,FDATE,OBJECTID.
Record page parameters are f=geojson, ascending objectIds from the saved plan, outSR=4326, returnGeometry=true, returnZ=false and returnM=false. Every page is saved before local name filtering, unchanged local O1 derivation and clipping; discarded unnamed flowlines exist only in ignored saved raw responses.
Exact spatial queries and metadata requests: [query sidecar](nhd-padded-spatial-queries.csv). Object-ID page parameters and response pages remain in the ignored raw session; no raw feature or unnamed flowline ID inventory is committed.
Every pre-existing canonical feature, with old/new ID, source ID, name, ftype, fcode, county-clip contact, geometry equality and classified difference: [feature comparison](nhd-padded-feature-comparison.csv).
Every existing Douglas flowline is in the retrieved named set: True. Named means exactly gnis_name is not null and is not the empty string.
Every permanent identifier unique: yes; missing legacy IDs: 0; duplicated legacy IDs: 0.
All differences EXPLAINED: no.
NOT EXPLAINED: 103 existing geometries (94 flowlines and nine waterbodies); every ID is listed in [the geometry discrepancy sidecar](nhd-padded-unexplained-geometries.csv).
Canonical data and display artifacts have not been applied; coordinator Gate 2 remains required.

### Gate 2 — canonical integration stopped by the comparison

The unchanged production comparison classifies 103 existing geometry changes as **NOT EXPLAINED**: 94 flowlines and nine waterbodies. The full comparison has 4,954 rows: 4,851 EXPLAINED and 103 NOT EXPLAINED. No old feature was removed or renamed, and every old ID, source identity, ftype, fcode and retained source field is unchanged. The 375 added flowlines and 85 added waterbodies intersect the padded strip and remain inside the approved padded extent; two existing waterbodies pass the unchanged extension check.
Counts before and staged after by source ftype and fcode: [source-count sidecar](nhd-padded-source-counts.csv). All 103 flagged IDs, geometry types, unchanged identity fields, topological equality, exact county-reclip equality and measured lost/gained geometry are listed in [the discrepancy sidecar](nhd-padded-unexplained-geometries.csv). These are diagnostics, not an alternative acceptance predicate.
Of the flagged changes, 100 reproduce the old geometry exactly when the new geometry is intersected with the county polygon. None is topologically equal before that intersection. Three waterbodies do not reproduce the exact old county clip: nhd-117822715, nhd-117822899 and nhd-117834809 (Strontia Springs Reservoir). The unchanged production comparator does not accept these results as padding-only differences. No tolerance, comparator, clipping, grouping, selection or stable-ID rule was changed to accept them.
The plain retrieval process finished at both layers verified and exited 1 because acceptable_differences_only is false. This is a comparison stop, not exhausted transport or incomplete retrieval; no page exhausted its budget. No further live request was made after completion.
Canonical Douglas research SHA-256 remains 55f0896051697fc52b46add755e89a0a7f9e14f267d5b6884788da58f0165e9d. Aspen, all non-water Douglas layers, manifests, display artifacts, aliases, selection report and the pending South Platte marker remain unchanged. Phase F, approved Douglas wording/pins, branch integration, final South Platte production measurements, final byte budgets, browser validation and three final performance sessions have not run. Gate 2 review must resolve the 103 NOT EXPLAINED geometries before canonical integration can proceed.

### Gate 2 follow-up: comparator defect and strict padding residual

The coordinator accepted retrieval as complete and requested docs-only analysis before application. [The comparator analysis](nhd-padded-comparator-analysis.md) proves all original 103 county re-clips are geometrically equal without tolerance; the three previously exact-order failures are coordinate-order differences with identical source geometry and attributes. All original 103 have an empty outside-padding difference, though four direct covers predicates fail at clip-line points. The proposed exact subset/reclip comparator passes nine isolated synthetic checks and explains the original 103, but exposes one formerly tolerated sliver on nhd-120030962: 2.117038273201713e-10 m² after UTM projection. The full proposal therefore remains blocked on that single numerical residual. No production comparator, tolerance, source, canonical data, wording or artifact has changed; Gate 2 and any owner numerical decision remain required.

### Corrected production comparison: one strict residual remains

After proving all original flagged source records unchanged, the owner-authorized minimal county-reclip comparator correction was implemented with positive and negative regression tests. [The complete post-fix comparison](nhd-padded-feature-comparison-postfix.csv) has 4,953 EXPLAINED rows and one NOT EXPLAINED row, `nhd-120030962` (Cheesman Lake). All original 103 discrepancies pass; the corrected zero-tolerance extent check rejects this newly exposed 2.117038273201713e-10 m² padding sliver instead of accepting it through the old tolerance. [Analysis, exact predicates, source proof and measurements](nhd-padded-comparator-analysis.md) remain the decision record. No tolerance, named exception or canonical mutation was applied; staging remains unacceptable and Phase F is stopped pending owner disposition at Gate 2.
