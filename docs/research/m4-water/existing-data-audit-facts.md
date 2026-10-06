# Ohvernight water audit — computed facts (coordinator, main at b45ca59)

Computed read-only from the committed canonical bundles and display artifacts. Lengths and areas are approximate planar estimates for audit only.

## Region aspen

Sources used by water layers:
- `usgs_nhd`: {"type": "agency", "agency": "USGS", "source_urls": ["https://hydro.nationalmap.gov/arcgis/rest/services/nhd/MapServer/6", "https://hydro.nationalmap.gov/arcgis/rest/services/nhd/MapServer/9", "https://hydro.nationalmap.gov/arcgis/rest/services/nhd/MapServer/12"], "scope": "Hydrography retained for setback screening. Feature type, flow permanence and size are not carried. A name does not indicate recreational usefulness, public access or seasonal flow."}

### Layer `hydrology` (canonical `map-data-v2.json` pointer `/layers/hydrology`)

- manifest limitations: Retained for setback screening. Display currently selects features by name only; a name is not evidence of recreational usefulness, access or flow.
- manifest fields: {"source": [], "derived": ["kind"]}  max_age_hours: None
- source status record: {"status": "available", "completed_at": "2026-09-25T03:22:40.085459Z"}
- canonical bytes of file: 10086079  display artifact bytes: 1134855

**CANONICAL: 6926 features**
- geometry types: {'LineString': 6403, 'MultiLineString': 8, 'Polygon': 515}
- property keys (count of features carrying each): {'id': 6926, 'kind': 6926, 'name': 6926, 'evidence': 6926}
- named: 1555, unnamed: 5371
- values of `kind`: {'"flowline"': 6411, '"waterbody"': 514, '"area"': 1}
- values of `evidence`: {'{"source_url": "https://hydro.nationalmap.gov/arcgis/rest/se': 6926}
- distinct names: 134; names carried by more than one feature: 93 (features in those groups: 1514)
- most repeated names: {'Roaring Fork River': 112, 'Snowmass Creek': 83, 'Castle Creek': 78, 'Woody Creek': 77, 'Hunter Creek': 73, 'Lincoln Creek': 55, 'Willow Creek': 52, 'Conundrum Creek': 42, 'Maroon Creek': 42, 'Brush Creek': 37, 'East Maroon Creek': 36, 'East Snowmass Creek': 36}
- name-word counts over distinct names (a name can match several): {'creek': 71, 'lake': 36, 'ditch': 14, 'fork': 9, 'reservoir': 8, 'river': 7, 'canal': 3, 'gulch': 1, 'spring': 1, 'pond': 1}
- line feature length km: min 0.001 / median 0.292 / p90 0.917 / max 12.893 ; total 2647.7 km; features under 0.25 km: 2809
- polygon area km2: min 0.000 / median 0.002 / p90 0.021 / max 0.333 ; under 0.005 km2 (0.5 ha): 376; under 0.02 km2 (2 ha): 459

**DISPLAY: 1555 features**
- geometry types: {'LineString': 1508, 'MultiLineString': 4, 'Polygon': 43}
- property keys (count of features carrying each): {'evidence': 1555, 'id': 1555, 'kind': 1555, 'name': 1555}
- named: 1555, unnamed: 0
- values of `evidence`: {'0': 1512, '1': 43}
- values of `kind`: {'"flowline"': 1512, '"waterbody"': 43}
- distinct names: 134; names carried by more than one feature: 93 (features in those groups: 1514)
- most repeated names: {'Roaring Fork River': 112, 'Snowmass Creek': 83, 'Castle Creek': 78, 'Woody Creek': 77, 'Hunter Creek': 73, 'Lincoln Creek': 55, 'Willow Creek': 52, 'Conundrum Creek': 42, 'Maroon Creek': 42, 'Brush Creek': 37, 'East Maroon Creek': 36, 'East Snowmass Creek': 36}
- name-word counts over distinct names (a name can match several): {'creek': 71, 'lake': 36, 'ditch': 14, 'fork': 9, 'reservoir': 8, 'river': 7, 'canal': 3, 'gulch': 1, 'spring': 1, 'pond': 1}
- line feature length km: min 0.002 / median 0.265 / p90 0.998 / max 12.893 ; total 661.9 km; features under 0.25 km: 730
- polygon area km2: min 0.000 / median 0.027 / p90 0.077 / max 0.333 ; under 0.005 km2 (0.5 ha): 3; under 0.02 km2 (2 ha): 17
- example display features (first 3 properties): [{'evidence': 0, 'id': 'nhd-flowline-41313', 'kind': 'flowline', 'name': 'Hunter Creek'}, {'evidence': 0, 'id': 'nhd-flowline-41337', 'kind': 'flowline', 'name': 'Lost Man Creek'}, {'evidence': 0, 'id': 'nhd-flowline-41520', 'kind': 'flowline', 'name': 'Roaring Fork River'}]
- largest polygons (km2, name): [(0.333, 'Snowmass Lake'), (0.211, 'Wildcat Reservoir'), (0.127, 'Grizzly Reservoir'), (0.087, 'Willow Lake'), (0.077, 'Warren Lakes'), (0.076, 'Taylor Lake'), (0.072, 'Crater Lake'), (0.069, 'Cathedral Lake'), (0.065, 'Maroon Lake'), (0.058, 'Lost Man Lake'), (0.05, 'Petroleum Lake'), (0.049, 'Warren Lake')]
- longest named line groups (km): [('Roaring Fork River', 48.8), ('Hunter Creek', 31.7), ('Castle Creek', 30.4), ('Snowmass Creek', 27.3), ('Woody Creek', 20.3), ('Salvation Ditch', 19.7), ('Lincoln Creek', 19.5), ('McKenzie Wildcat Ditch', 16.2), ('Conundrum Creek', 15.7), ('Maroon Creek', 15.1), ('Difficult Creek', 14.0), ('Willow Creek', 13.2), ('East Maroon Creek', 13.0), ('West Maroon Creek', 12.6), ('South Fork Fryingpan River', 11.9)]

- canonical example feature properties: [{'id': 'nhd-flowline-41284', 'kind': 'flowline', 'name': None, 'evidence': {'source_url': 'https://hydro.nationalmap.gov/arcgis/rest/services/nhd/MapServer/6', 'agency': 'USGS', 'retrieved_at': '2026-09-25T03:22:28.230211Z', 'last_verified': None, 'confidence': 'high', 'verification_method': 'arcgis_rest_query', 'notes': ''}}, {'id': 'nhd-flowline-41294', 'kind': 'flowline', 'name': None, 'evidence': {'source_url': 'https://hydro.nationalmap.gov/arcgis/rest/services/nhd/MapServer/6', 'agency': 'USGS', 'retrieved_at': '2026-09-25T03:22:28.230211Z', 'last_verified': None, 'confidence': 'high', 'verification_method': 'arcgis_rest_query', 'notes': ''}}]

## Region douglas-co

Sources used by water layers:
- `usgs_nhd`: {"type": "agency", "agency": "USGS", "source_urls": ["https://hydro.nationalmap.gov/arcgis/rest/services/nhd/MapServer/12", "https://hydro.nationalmap.gov/arcgis/rest/services/nhd/MapServer/6"], "scope": "Named waterbodies and flowlines only, selected by name. A display subset, not complete hydrology. A name does not indicate recreational usefulness, public access, fishing or paddling permission."}

### Layer `waterbodies` (canonical `regions/douglas-co/research.json` pointer `/layers/waterbodies`)

- manifest limitations: Named features only. A name is not evidence of recreational usefulness, access or flow.
- manifest fields: {"source": ["manager"], "derived": []}  max_age_hours: 168
- source status record: {"status": "available", "retrieved_at": "2026-09-27T14:16:07.724731Z", "count": 33}
- canonical bytes of file: 6173713  display artifact bytes: 116952

**CANONICAL: 33 features**
- geometry types: {'Polygon': 31, 'MultiPolygon': 2}
- property keys (count of features carrying each): {'name': 33, 'manager': 33, 'id': 33, 'evidence': 33}
- named: 33, unnamed: 0
- values of `manager`: {'null': 33}
- values of `evidence`: {'{"source_url": "https://hydro.nationalmap.gov/arcgis/rest/se': 33}
- distinct names: 33; names carried by more than one feature: 0 (features in those groups: 0)
- most repeated names: {'Franktown Parker FPB-1 Reservoir': 1, 'Franktown Parker FPA-5 Reservoir': 1, 'Wakeman Reservoir': 1, 'Franktown Parker FPS-1 Reservoir': 1, 'McLellan Reservoir': 1, 'West Cherry Creek Detention Number 8 Reservoir': 1, 'Cheesman Lake': 1, 'Cantrill Reservoir': 1, 'Franktown Parker FPA-2 Reservoir': 1, 'J O Hill Reservoir': 1, 'Barney Bird Reservoir Number One': 1, 'Chatfield Lake': 1}
- name-word counts over distinct names (a name can match several): {'reservoir': 30, 'creek': 4, 'lake': 3, 'spring': 1}
- polygon area km2: min 0.001 / median 0.042 / p90 0.268 / max 3.160 ; under 0.005 km2 (0.5 ha): 5; under 0.02 km2 (2 ha): 7

**DISPLAY: 33 features**
- geometry types: {'Polygon': 31, 'MultiPolygon': 2}
- property keys (count of features carrying each): {'evidence': 33, 'id': 33, 'manager': 33, 'name': 33}
- named: 33, unnamed: 0
- values of `evidence`: {'0': 33}
- values of `manager`: {'null': 33}
- distinct names: 33; names carried by more than one feature: 0 (features in those groups: 0)
- most repeated names: {'Franktown Parker FPB-1 Reservoir': 1, 'Franktown Parker FPA-5 Reservoir': 1, 'Wakeman Reservoir': 1, 'Franktown Parker FPS-1 Reservoir': 1, 'McLellan Reservoir': 1, 'West Cherry Creek Detention Number 8 Reservoir': 1, 'Cheesman Lake': 1, 'Cantrill Reservoir': 1, 'Franktown Parker FPA-2 Reservoir': 1, 'J O Hill Reservoir': 1, 'Barney Bird Reservoir Number One': 1, 'Chatfield Lake': 1}
- name-word counts over distinct names (a name can match several): {'reservoir': 30, 'creek': 4, 'lake': 3, 'spring': 1}
- polygon area km2: min 0.001 / median 0.042 / p90 0.268 / max 3.160 ; under 0.005 km2 (0.5 ha): 5; under 0.02 km2 (2 ha): 7
- example display features (first 3 properties): [{'evidence': 0, 'id': 'waterbodies-421494', 'manager': None, 'name': 'Franktown Parker FPB-1 Reservoir'}, {'evidence': 0, 'id': 'waterbodies-783555', 'manager': None, 'name': 'Franktown Parker FPA-5 Reservoir'}, {'evidence': 0, 'id': 'waterbodies-834368', 'manager': None, 'name': 'Wakeman Reservoir'}]
- largest polygons (km2, name): [(3.16, 'Chatfield Lake'), (1.316, 'Cheesman Lake'), (0.871, 'Rueter-Hess Reservoir'), (0.268, 'Aurora-Rampart Reservoir'), (0.212, 'Platte Canyon Reservoir'), (0.115, 'Strontia Springs Reservoir'), (0.095, 'Pinery Reservoir'), (0.087, 'McLellan Reservoir'), (0.083, 'Franktown Parker FPE-8 Reservoir'), (0.077, 'West Cherry Creek Detention Number 11 Reservoir'), (0.074, 'J O Hill Reservoir'), (0.073, 'Franktown Parker FPB-1 Reservoir')]

- canonical example feature properties: [{'name': 'Franktown Parker FPB-1 Reservoir', 'manager': None, 'id': 'waterbodies-421494', 'evidence': {'source_url': 'https://hydro.nationalmap.gov/arcgis/rest/services/nhd/MapServer/12', 'agency': 'USGS', 'retrieved_at': '2026-09-27T14:16:07.657228Z', 'last_verified': None, 'confidence': 'unverified', 'verification_method': 'source_fetch', 'notes': ''}}, {'name': 'Franktown Parker FPA-5 Reservoir', 'manager': None, 'id': 'waterbodies-783555', 'evidence': {'source_url': 'https://hydro.nationalmap.gov/arcgis/rest/services/nhd/MapServer/12', 'agency': 'USGS', 'retrieved_at': '2026-09-27T14:16:07.657228Z', 'last_verified': None, 'confidence': 'unverified', 'verification_method': 'source_fetch', 'notes': ''}}]

### Layer `waterways` (canonical `regions/douglas-co/research.json` pointer `/layers/waterways`)

- manifest limitations: Named features only. A name is not evidence of recreational usefulness, access or flow.
- manifest fields: {"source": ["manager"], "derived": []}  max_age_hours: 168
- source status record: {"status": "available", "retrieved_at": "2026-09-27T14:16:40.946196Z", "count": 2359}
- canonical bytes of file: 6173713  display artifact bytes: 1770773

**CANONICAL: 2359 features**
- geometry types: {'LineString': 2348, 'MultiLineString': 11}
- property keys (count of features carrying each): {'name': 2359, 'manager': 2359, 'id': 2359, 'evidence': 2359}
- named: 2359, unnamed: 0
- values of `manager`: {'null': 2359}
- values of `evidence`: {'{"source_url": "https://hydro.nationalmap.gov/arcgis/rest/se': 2359}
- distinct names: 69; names carried by more than one feature: 56 (features in those groups: 2346)
- most repeated names: {'East Plum Creek': 183, 'Bear Creek': 146, 'Jackson Creek': 116, 'West Plum Creek': 98, 'Indian Creek': 81, 'Cherry Creek': 80, 'Trout Creek': 80, 'Willow Creek': 79, 'West Creek': 76, 'South Platte River': 75, 'Pine Creek': 68, 'Gove Creek': 64}
- name-word counts over distinct names (a name can match several): {'creek': 50, 'ditch': 15, 'canal': 2, 'river': 1, 'spring': 1}
- line feature length km: min 0.001 / median 0.160 / p90 0.727 / max 14.850 ; total 777.9 km; features under 0.25 km: 1578

**DISPLAY: 2359 features**
- geometry types: {'LineString': 2348, 'MultiLineString': 11}
- property keys (count of features carrying each): {'evidence': 2359, 'id': 2359, 'manager': 2359, 'name': 2359}
- named: 2359, unnamed: 0
- values of `evidence`: {'0': 2359}
- values of `manager`: {'null': 2359}
- distinct names: 69; names carried by more than one feature: 56 (features in those groups: 2346)
- most repeated names: {'East Plum Creek': 183, 'Bear Creek': 146, 'Jackson Creek': 116, 'West Plum Creek': 98, 'Indian Creek': 81, 'Cherry Creek': 80, 'Trout Creek': 80, 'Willow Creek': 79, 'West Creek': 76, 'South Platte River': 75, 'Pine Creek': 68, 'Gove Creek': 64}
- name-word counts over distinct names (a name can match several): {'creek': 50, 'ditch': 15, 'canal': 2, 'river': 1, 'spring': 1}
- line feature length km: min 0.001 / median 0.160 / p90 0.727 / max 14.850 ; total 777.9 km; features under 0.25 km: 1578
- example display features (first 3 properties): [{'evidence': 0, 'id': 'waterways-57636', 'manager': None, 'name': 'Bear Creek'}, {'evidence': 0, 'id': 'waterways-57660', 'manager': None, 'name': 'East Plum Creek'}, {'evidence': 0, 'id': 'waterways-57687', 'manager': None, 'name': 'Pine Creek'}]
- longest named line groups (km): [('Arapahoe Canal', 62.3), ('East Plum Creek', 53.3), ('Cherry Creek', 44.0), ('Willow Creek', 38.3), ('West Plum Creek', 36.7), ('Bear Creek', 29.1), ('Highline Canal', 27.9), ('East Cherry Creek', 24.8), ('West Cherry Creek', 24.3), ('Antelope Creek', 23.0), ('Jackson Creek', 20.4), ('Indian Creek', 18.7), ('Happy Canyon Creek', 18.7), ('Cook Creek', 18.7), ('Plum Creek', 18.6)]

- canonical example feature properties: [{'name': 'Bear Creek', 'manager': None, 'id': 'waterways-57636', 'evidence': {'source_url': 'https://hydro.nationalmap.gov/arcgis/rest/services/nhd/MapServer/6', 'agency': 'USGS', 'retrieved_at': '2026-09-27T14:16:39.094281Z', 'last_verified': None, 'confidence': 'unverified', 'verification_method': 'source_fetch', 'notes': ''}}, {'name': 'East Plum Creek', 'manager': None, 'id': 'waterways-57660', 'evidence': {'source_url': 'https://hydro.nationalmap.gov/arcgis/rest/services/nhd/MapServer/6', 'agency': 'USGS', 'retrieved_at': '2026-09-27T14:16:39.094281Z', 'last_verified': None, 'confidence': 'unverified', 'verification_method': 'source_fetch', 'notes': ''}}]

## Pipeline: where water is fetched and what is dropped

- `v2/pipeline/scripts/03_fetch_hydrology.py` mentions hydrology (29 lines)
- `v2/pipeline/scripts/07_build_dispersed_corridors.py` mentions hydrology (94 lines)
- `v2/pipeline/scripts/build_display.py` mentions hydrology (272 lines)
- `v2/pipeline/scripts/enrich_douglas.py` mentions hydrology (46 lines)
- `v2/pipeline/scripts/run_pipeline.py` mentions hydrology (98 lines)

## What the pipeline requests and keeps (read from the code)

- Aspen (`v2/pipeline/scripts/03_fetch_hydrology.py`): queries three layers of `https://hydro.nationalmap.gov/arcgis/rest/services/nhd/MapServer` — 6 (flowline), 9 (area), 12 (waterbody) — by bounding box with a ~400 m margin, with only `OBJECTID` required. It keeps `id` (`nhd-<kind>-<objectid>`), `kind` (flowline / area / waterbody, i.e. which service layer it came from), `name` (from `gnis_name`) and the evidence record. Every other NHD attribute returned by the service is discarded (for example feature type and code, permanent identifier, reach code, GNIS id, length or area, flow direction, visibility filter, elevation — whichever the service provides).
- Douglas (`v2/pipeline/scripts/enrich_douglas.py`): queries layer 12 (waterbodies) and layer 6 (flowlines) with `where gnis_name IS NOT NULL AND gnis_name <> ''`, requesting only `objectid` and `gnis_name`. It keeps `name` and a `manager` field that is always null for water. No area layer.
- The Aspen canonical hydrology (all 6,926 features, named or not) is also an input to setback screening for dispersed-camping corridors (`07_build_dispersed_corridors.py`); the browser display artifact is the named subset only.
- Identity: `id` is built from the service `OBJECTID`, which is not a stable NHD identifier.
- Display today: Aspen shows 1,555 named features (1,512 flowline pieces, 43 waterbodies); Douglas shows 33 named waterbodies and 2,359 named flowline pieces. A single stream appears as many separate features (Roaring Fork River: 112 pieces; Arapahoe Canal: 62 km of pieces).
- Owner observation relevant to the audit: the map is cluttered with hydrologic lines of little recreational use (ditches, canals, detention reservoirs, tiny ponds), and one stream is many tappable pieces.

## Source-service statistics probe (coordinator, read-only, 2026-10-06)

```text
NHD MapServer read-only statistics by envelope (features intersecting the region bounding box; counts differ slightly from the clipped repository data). Columns: ftype, fcode, feature count, total km (flowlines) or km2 (waterbodies).
== aspen (-107.05, 39.0, -106.57, 39.26)
  flowline ALL  : [(334, 33400, 60, 1.9), (336, 33600, 158, 141.4), (428, 42800, 2, 2.4), (428, 42802, 2, 0.1), (428, 42803, 5, 26.4), (460, 46003, 1647, 811.3), (460, 46006, 1384, 664.4), (460, 46007, 2244, 877.3), (558, 55800, 430, 40.5)]
  flowline NAMED: [(334, 33400, 3, 0.2), (336, 33600, 97, 95.3), (428, 42802, 2, 0.1), (428, 42803, 5, 26.4), (460, 46003, 79, 24.6), (460, 46006, 1087, 484.8), (558, 55800, 124, 18.3)]
  waterbody ALL  : [(390, 39000, 3, 0.0), (390, 39001, 31, 0.1), (390, 39004, 365, 2.2), (390, 39009, 10, 0.4), (436, 43624, 5, 0), (466, 46600, 54, 1.8)]
  waterbody NAMED: [(390, 39004, 31, 1.4), (390, 39009, 8, 0.4)]
== douglas-co (-105.329, 39.129, -104.661, 39.566)
  flowline ALL  : [(334, 33400, 29, 4.8), (336, 33600, 118, 134.5), (336, 33601, 1, 0.3), (428, 42801, 4, 12.9), (428, 42803, 6, 25.0), (428, 42807, 11, 38.6), (428, 42813, 5, 0.4), (460, 46003, 16012, 4682.4), (460, 46006, 2671, 672.9), (460, 46007, 15158, 3285.4), (558, 55800, 2788, 312.3)]
  flowline NAMED: [(334, 33400, 1, 0.1), (336, 33600, 83, 110.0), (336, 33601, 1, 0.3), (428, 42803, 6, 25.0), (428, 42807, 6, 17.6), (428, 42813, 3, 0.3), (460, 46003, 807, 283.5), (460, 46006, 2026, 536.3), (558, 55800, 670, 140.1)]
  waterbody ALL  : [(390, 39001, 1461, 3.2), (390, 39004, 761, 3.4), (390, 39005, 2, 0.1), (390, 39009, 9, 10.6), (390, 39011, 7, 0.2), (436, 43601, 1, 0.0), (436, 43612, 6, 0.0), (436, 43613, 4, 0.0), (436, 43619, 1, 0.9), (436, 43624, 23, 0.2), (466, 46600, 1, 0.0)]
  waterbody NAMED: [(390, 39001, 16, 0.5), (390, 39004, 10, 0.7), (390, 39005, 2, 0.1), (390, 39009, 7, 10.6), (436, 43619, 1, 0.9)]
```
