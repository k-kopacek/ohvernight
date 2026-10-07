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

Before: 2135 total (33 named, 2102 unnamed); baseline retained no ftype/fcode values. After: 2135 total (33 named, 2102 unnamed).

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
