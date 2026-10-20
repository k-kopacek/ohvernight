<!-- Hermes research report, M4 track I. Retrieved 2026-10-06 with web search and page reading only, under a bounded method. This is a research INPUT, kept verbatim. It is not a review and establishes no claim: a claim exists only when a record is written in the repository, the coordinator has read the page, and the owner has approved it (ADR-004, ADR-005; M4 specification section 9.5). -->

# 3DHP Migration Dossier: Colorado Representative Features

Access date: 2026-10-06

Scope: read-only comparison of the retired USGS National Hydrography Dataset (NHD) and the live USGS 3D Hydrography Program `3DHP_all` service. Queries were attribute-only (`returnGeometry=false`) and limited to at most 20 records. No claim here establishes public access or permission to fish, boat, paddle, swim, park, or camp.

## Executive findings

| Finding | Status | Evidence |
|---|---|---|
| 3DHP collapses NHD perennial, intermittent, and ephemeral Stream/River FCodes into one flowline feature type, code `1`. | RETRIEVED | The official crosswalk maps NHD `46003`, `46006`, and `46007` alike to 3DHP `River`; the live flowline schema has no permanence or hydrographic-category field. [USGS crosswalk](https://www.usgs.gov/ngp-standards-and-specifications/3d-hydrography-program-product-specification-crosswalk-tables) [Flowline layer metadata](https://hydro.nationalmap.gov/arcgis/rest/services/3DHP_all/MapServer/50?f=pjson) |
| The perennial/intermittent/ephemeral distinction does not survive in the present `3DHP_all` feature attributes, domains, or separate service tables. | RETRIEVED | The service advertises `tables: []`; flowline fields and the data dictionary contain no permanence field. [3DHP service metadata](https://hydro.nationalmap.gov/arcgis/rest/services/3DHP_all/MapServer?f=pjson) [USGS flowline dictionary](https://www.usgs.gov/ngp-standards-and-specifications/3d-hydrography-program-3dhpall-flowline) |
| 3DHP also collapses natural lakes, ponds, and every listed reservoir subtype into waterbody feature type `3`, `Lake`. | RETRIEVED | USGS defines 3DHP Lake as including “natural and manmade lakes, ponds and reservoirs”; the crosswalk maps NHD `390xx` and `436xx` to Lake. [USGS waterbody dictionary](https://www.usgs.gov/ngp-standards-and-specifications/3d-hydrography-program-3dhpall-waterbody) [USGS crosswalk](https://www.usgs.gov/ngp-standards-and-specifications/3d-hydrography-program-product-specification-crosswalk-tables) |
| Reservoir purpose and treatment/tailings/sewage distinctions do not survive in the present waterbody schema. | RETRIEVED | The live waterbody fields are limited to IDs, date, name, feature type, area, and work unit; no reservoir-purpose field or related table exists. [Waterbody layer metadata](https://hydro.nationalmap.gov/arcgis/rest/services/3DHP_all/MapServer/60?f=pjson) [3DHP service metadata](https://hydro.nationalmap.gov/arcgis/rest/services/3DHP_all/MapServer?f=pjson) |
| NHD Artificial Path becomes a 3DHP Waterbody Connector; its `waterbodyid3dhp` links the centerline to the polygon it traverses. | RETRIEVED | The crosswalk maps `55800` to Waterbody Connector. Waterton Canyon returns connectors linked to waterbody `OISYK`. [USGS crosswalk](https://www.usgs.gov/ngp-standards-and-specifications/3d-hydrography-program-product-specification-crosswalk-tables) [Waterton 3DHP query](https://hydro.nationalmap.gov/arcgis/rest/services/3DHP_all/MapServer/50/query?f=pjson&where=gnisid%3D201759&geometry=-105.12%2C39.47%2C-105.05%2C39.52&geometryType=esriGeometryEnvelope&inSR=4326&spatialRel=esriSpatialRelIntersects&outFields=id3dhp%2Cfeaturedate%2Cmainstemid%2Cgnisid%2Cgnisidlabel%2Cfeaturetype%2Cfeaturetypelabel%2Cwaterbodyid3dhp%2Cstreamorder%2Chydrosequence%2Clevelpath%2Cworkunitid&returnGeometry=false&resultRecordCount=20) |
| `id3dhp` is explicitly not persistent. The service carries no NHD `permanent_identifier` or `reachcode` field. | RETRIEVED | USGS says `id3dhp` is a “unique identifier that is not persistent.” Neither live layer schema contains an NHD-ID field. [USGS flowline dictionary](https://www.usgs.gov/ngp-standards-and-specifications/3d-hydrography-program-3dhpall-flowline) [USGS waterbody dictionary](https://www.usgs.gov/ngp-standards-and-specifications/3d-hydrography-program-3dhpall-waterbody) |
| All sampled Colorado 3DHP records returned `workunitid="NHD"`; no EDH work-unit polygon intersected the broad sample envelope. | RETRIEVED | Representative feature queries below all returned `NHD`; the EDH work-unit query over approximately `-107,39` to `-104.7,39.65` returned no features. [EDH work-unit query](https://hydro.nationalmap.gov/arcgis/rest/services/3DHP_all/MapServer/92/query?f=pjson&where=1%3D1&geometry=-107.0%2C39.0%2C-104.7%2C39.65&geometryType=esriGeometryEnvelope&inSR=4326&spatialRel=esriSpatialRelIntersects&outFields=*&returnGeometry=false&resultRecordCount=20) |
| Moving now would break Ohvernight’s perennial-only and reservoir-purpose filters. | INFERRED | Those rules require distinctions absent from the current 3DHP schema. [Flowline metadata](https://hydro.nationalmap.gov/arcgis/rest/services/3DHP_all/MapServer/50?f=pjson) [Waterbody metadata](https://hydro.nationalmap.gov/arcgis/rest/services/3DHP_all/MapServer/60?f=pjson) |

## Service and schema state

The service description says 3DHP uses elevation-derived hydrography where available and supplements it with NHD elsewhere; EDH eventually replaces NHD by collection area. The live service credits report: “Data refreshed September 4, 2026.” [3DHP service metadata](https://hydro.nationalmap.gov/arcgis/rest/services/3DHP_all/MapServer?f=pjson) — RETRIEVED.

A separate USGS access page says “3DHP Web Services Last Updated July 2026” and says new EDH data and attributes are added quarterly. That page therefore lags the service’s own September 4 refresh statement. [USGS access page](https://www.usgs.gov/3d-hydrography-program/access-3dhp-data-products) — RETRIEVED.

USGS describes the 2023 product as provisional and says the data model and products remain under development. [USGS service specification](https://www.usgs.gov/ngp-standards-and-specifications/3d-hydrography-program-products-3dhpall-2023-service-specification) — RETRIEVED.

### Complete relevant coded domains

#### Flowline `featuretype`

| Code | USGS domain description | Operational interpretation | Status |
|---:|---|---|---|
| 1 | River | Natural channelized flowline | RETRIEVED |
| 2 | Canal | Engineered canal/ditch | RETRIEVED |
| 3 | Drainageway | Low-area drainage path upstream of discernible channelization | RETRIEVED |
| 4 | Surface Connector | Abstract surface or near-surface connection | RETRIEVED |
| 5 | Waterbody Connector | Abstract connection across polygonal water | RETRIEVED |
| 6 | Elevation Breaching Connector | Connector breaching an obstructing elevation value, commonly a culvert | RETRIEVED |
| 7 | Hydro Unenforced Connector | Flow not determined by the surface-water network; includes most pipelines | RETRIEVED |

Source for all rows: [USGS flowline data dictionary](https://www.usgs.gov/ngp-standards-and-specifications/3d-hydrography-program-3dhpall-flowline).

The live renderer uses labels `River`, `Canal`, `Drainageway`, `Surface Connector`, `Waterbody Connector`, `Elevation Breaching Connector`, and `Hydro Unenforced Connector`. Some NHD-derived query results instead return `featuretypelabel="Channel Line"` for code `1`; filtering should therefore use numeric `featuretype`, not the label. [Flowline layer metadata](https://hydro.nationalmap.gov/arcgis/rest/services/3DHP_all/MapServer/50?f=pjson) [Castle Creek query](https://hydro.nationalmap.gov/arcgis/rest/services/3DHP_all/MapServer/50/query?f=pjson&where=gnisid%3D1139440&outFields=id3dhp%2Cfeaturedate%2Cmainstemid%2Cgnisid%2Cgnisidlabel%2Cfeaturetype%2Cfeaturetypelabel%2Cwaterbodyid3dhp%2Cstreamlevel%2Cstreamorder%2Chydrosequence%2Clevelpath%2Cworkunitid&returnGeometry=false&resultRecordCount=20) — RETRIEVED.

#### Waterbody `featuretype`

| Code | Description | Coverage | Status |
|---:|---|---|---|
| 1 | River | Polygonal flowing water | RETRIEVED |
| 2 | Canal | Polygonal canal | RETRIEVED |
| 3 | Lake | Natural and manmade lakes, ponds, and reservoirs | RETRIEVED |
| 4 | Ocean or Great Lake | Ocean/Great Lake terminal waterbody | RETRIEVED |

Source for all rows: [USGS waterbody data dictionary](https://www.usgs.gov/ngp-standards-and-specifications/3d-hydrography-program-3dhpall-waterbody).

#### Other flowline coded domains

| Field | Values | Status |
|---|---|---|
| `flowdirection` | `0` undetermined from elevation; `1` digitized direction and vertices descend; `2` digitized direction but vertices ascend | RETRIEVED |
| `onsurface` | `0` elevated above another hydrography feature; `1` on land surface; `2` below land surface | RETRIEVED |
| `divergence` | `0` none; `1` main path; `2` minor path | RETRIEVED |

Source: [USGS flowline data dictionary](https://www.usgs.gov/ngp-standards-and-specifications/3d-hydrography-program-3dhpall-flowline).

#### Permanence/category domains

| Sought classification | Live field | Domain | Separate table | Finding |
|---|---|---|---|---|
| Perennial/intermittent/ephemeral | None | None | None advertised | RETRIEVED |
| Waterbody hydrographic category | None | None | None advertised | RETRIEVED |
| Reservoir purpose/type | None | None | None advertised | RETRIEVED |
| Lake versus reservoir | None beyond combined `featuretype=3` | `3 = Lake` combines both | None advertised | RETRIEVED |

Sources: [Flowline layer metadata](https://hydro.nationalmap.gov/arcgis/rest/services/3DHP_all/MapServer/50?f=pjson), [Waterbody layer metadata](https://hydro.nationalmap.gov/arcgis/rest/services/3DHP_all/MapServer/60?f=pjson), and [service metadata showing no tables](https://hydro.nationalmap.gov/arcgis/rest/services/3DHP_all/MapServer?f=pjson).

## NHD-to-3DHP classification crosswalk

| NHD type | NHD code(s) | 3DHP result | Information retained or lost | Status |
|---|---:|---|---|---|
| Stream/River | `46000`, `46003`, `46006`, `46007` | Flowline `1`, River | Stream identity survives; permanence is lost | RETRIEVED |
| Polygonal Stream/River | Same family | Waterbody `1`, River | Wide-river polygon survives | RETRIEVED |
| Artificial Path | `55800` | Flowline `5`, Waterbody Connector | Centerline-through-water role survives | RETRIEVED |
| Canal/Ditch | `33600`, `33601`, `33603` | Flowline or waterbody `2`, Canal | Canal class survives; detailed subtype does not | RETRIEVED |
| Connector | `33400` | Flowline `4`, Surface Connector, for NHD conversion | Connector class changes to a more specific 3DHP class | RETRIEVED |
| Pipeline | `42800`–`42824` | Flowline `7`, Hydro Unenforced Connector | Pipeline identity and subtype are collapsed | RETRIEVED |
| Underground Conduit | `42000`–`42003` | Flowline `7`, Hydro Unenforced Connector | Conduit identity and positional-accuracy subtype are collapsed | RETRIEVED |
| Lake/Pond | `39000` family | Waterbody `3`, Lake | Lake/pond and permanence distinctions are collapsed | RETRIEVED |
| Reservoir | `43600` family | Waterbody `3`, Lake | Reservoir identity, purpose, construction, and permanence are collapsed | RETRIEVED |

Source for all mappings: [USGS NHD-to-3DHP crosswalk](https://www.usgs.gov/ngp-standards-and-specifications/3d-hydrography-program-product-specification-crosswalk-tables).

For EDH input, connector mapping is more nuanced: indefinite-surface connectors map to `4`, artificial paths to `5`, culvert/terrain-breach connectors to `6`, and generic/non-NHD/underground/pipeline connectors to `7`. [USGS EDH-to-3DHP crosswalk](https://www.usgs.gov/ngp-standards-and-specifications/3d-hydrography-program-product-specification-crosswalk-tables) — RETRIEVED.

## Representative Colorado comparisons

Raw 3DHP `featuredate` is shown as returned. `1694649600000` was common to every listed sample. Every listed 3DHP sample returned `workunitid="NHD"`.

### Rivers, streams, and engineered flowlines

| Sample | NHD retrieved values | 3DHP retrieved values | Finding | Status |
|---|---|---|---|---|
| Roaring Fork River, GNIS `174812` | Example channel: permanent ID `72963510`; reachcode `14010004000123`; FType/FCode `460/46006`. Example artificial path: `165818861`; `14010004000100`; `558/55800`. | Channel example `18GUY`: type `1`, label `Channel Line`, mainstem `https://geoconnex.us/ref/mainstems/40769`, streamorder `6`, hydrosequence `27909300`, levelpath `27503096`. Connector example `13LM1`: type `5`, `Waterbody Connector`, waterbody `OHC6D`, same mainstem and levelpath. | Perennial NHD channels and artificial paths become one named 3DHP mainstem composed of channel lines and waterbody connectors. | RETRIEVED |
| Castle Creek near Aspen, GNIS `1139440` | Broad name query returned permanent ID `166075586`; reachcode `17100307000655`; FType/FCode `460/46006`. | `10NU`: type `1`, `Channel Line`; mainstem `https://geoconnex.us/ref/mainstems/2329581`; streamorder `3`; hydrosequence `15844924`; levelpath `15773689`. Other sampled segments shared that mainstem and levelpath; `FJD2W` was connector type `5` through waterbody `OJ7ML`. | Stream classification and network grouping survive, but the NHD perennial code does not. | RETRIEVED |
| Happy Canyon Creek, GNIS `188116` | Examples include `70220685`, reachcode `14020006004977`, FCode `46003`; `70225621`, reachcode `14020006000033`, FCode `46006`; and artificial path `70222999`, FCode `55800`. | `139AQ`: type `1`, `Channel Line`; mainstem `https://geoconnex.us/ref/mainstems/66510`; streamorder `5`; hydrosequence `27300460`; levelpath `27295610`. `4G91Q`: type `5`, connector through `LYVVA`. | One NHD-named creek contains both intermittent and perennial segments, but its 3DHP records no longer expose that difference. | RETRIEVED |
| South Platte River, Waterton Canyon | Example NHD area: permanent ID `117824519`, unnamed, FType/FCode `460/46006`. Example NHD centerlines include `160751115`, reachcode `10190002000436`, FType/FCode `558/55800`. | Waterbody `OISYK`: type `1`, `River`, area `0.33042565` km². Connector `1YOZC`: type `5`, linked to `OISYK`; mainstem `https://geoconnex.us/ref/mainstems/313255`; streamorder `8`; hydrosequence `28484910`; levelpath `22245985`. | 3DHP preserves the wide-river polygon and carries a linked centerline across it. | RETRIEVED |
| Salvation Ditch, GNIS `202674` | Targeted NHD query failed twice with HTTP 504, so its NHD row is UNKNOWN from this session. | `10K0R`: type `2`, `Canal`; mainstem `https://geoconnex.us/usgs/mainstems/9114397`; streamorder `3`; hydrosequence `1758842`; levelpath `1297911`. Also present: `69FRE`, type `7`, Hydro Unenforced Connector; `F1L6W`, type `5`, linked to waterbody `K8HBM`. | Canal segments are directly excludable, but the named engineered route can also contain connector types. | RETRIEVED / UNKNOWN |

Sources:

- [Roaring Fork NHD query](https://hydro.nationalmap.gov/arcgis/rest/services/nhd/MapServer/6/query?f=pjson&where=gnis_id%3D%2700174812%27&outFields=permanent_identifier%2Creachcode%2Cgnis_id%2Cgnis_name%2Cftype%2Cfcode%2Cflowdir&returnGeometry=false&resultRecordCount=20)
- [Roaring Fork 3DHP query](https://hydro.nationalmap.gov/arcgis/rest/services/3DHP_all/MapServer/50/query?f=pjson&where=gnisid%3D174812&outFields=id3dhp%2Cfeaturedate%2Cmainstemid%2Cgnisid%2Cgnisidlabel%2Cfeaturetype%2Cfeaturetypelabel%2Cwaterbodyid3dhp%2Cstreamlevel%2Cstreamorder%2Chydrosequence%2Clevelpath%2Cworkunitid&returnGeometry=false&resultRecordCount=20)
- [Broad NHD name query containing Castle Creek](https://hydro.nationalmap.gov/arcgis/rest/services/nhd/MapServer/6/query?f=pjson&where=gnis_name%20LIKE%20%27%25Roaring%20Fork%20River%25%27%20OR%20gnis_name%20LIKE%20%27%25Castle%20Creek%25%27%20OR%20gnis_name%20LIKE%20%27%25Happy%20Canyon%20Creek%25%27%20OR%20gnis_name%20LIKE%20%27%25Big%20Dry%20Creek%25%27&outFields=permanent_identifier%2Creachcode%2Cgnis_id%2Cgnis_name%2Cftype%2Cfcode%2Cflowdir%2Cvisibilityfilter&returnGeometry=false&resultRecordCount=20)
- [Castle Creek 3DHP query](https://hydro.nationalmap.gov/arcgis/rest/services/3DHP_all/MapServer/50/query?f=pjson&where=gnisid%3D1139440&outFields=id3dhp%2Cfeaturedate%2Cmainstemid%2Cgnisid%2Cgnisidlabel%2Cfeaturetype%2Cfeaturetypelabel%2Cwaterbodyid3dhp%2Cstreamlevel%2Cstreamorder%2Chydrosequence%2Clevelpath%2Cworkunitid&returnGeometry=false&resultRecordCount=20)
- [Happy Canyon NHD query](https://hydro.nationalmap.gov/arcgis/rest/services/nhd/MapServer/6/query?f=pjson&where=gnis_id%3D%2700188116%27&outFields=permanent_identifier%2Creachcode%2Cgnis_id%2Cgnis_name%2Cftype%2Cfcode%2Cflowdir&returnGeometry=false&resultRecordCount=20)
- [Happy Canyon 3DHP query](https://hydro.nationalmap.gov/arcgis/rest/services/3DHP_all/MapServer/50/query?f=pjson&where=gnisid%3D188116&outFields=id3dhp%2Cfeaturedate%2Cmainstemid%2Cgnisid%2Cgnisidlabel%2Cfeaturetype%2Cfeaturetypelabel%2Cwaterbodyid3dhp%2Cstreamlevel%2Cstreamorder%2Chydrosequence%2Clevelpath%2Cworkunitid&returnGeometry=false&resultRecordCount=20)
- [Waterton NHD area query](https://hydro.nationalmap.gov/arcgis/rest/services/nhd/MapServer/9/query?f=pjson&where=ftype%3D460&geometry=-105.12%2C39.47%2C-105.05%2C39.52&geometryType=esriGeometryEnvelope&inSR=4326&spatialRel=esriSpatialRelIntersects&outFields=permanent_identifier%2Cgnis_id%2Cgnis_name%2Cftype%2Cfcode%2Cresolution&returnGeometry=false&resultRecordCount=20)
- [Waterton NHD flowline query](https://hydro.nationalmap.gov/arcgis/rest/services/nhd/MapServer/6/query?f=pjson&where=gnis_id%3D%2700201759%27&geometry=-105.12%2C39.47%2C-105.05%2C39.52&geometryType=esriGeometryEnvelope&inSR=4326&spatialRel=esriSpatialRelIntersects&outFields=permanent_identifier%2Creachcode%2Cgnis_id%2Cgnis_name%2Cftype%2Cfcode%2Cflowdir&returnGeometry=false&resultRecordCount=20)
- [Waterton 3DHP waterbody query](https://hydro.nationalmap.gov/arcgis/rest/services/3DHP_all/MapServer/60/query?f=pjson&where=featuretype%3D1&geometry=-105.12%2C39.47%2C-105.05%2C39.52&geometryType=esriGeometryEnvelope&inSR=4326&spatialRel=esriSpatialRelIntersects&outFields=id3dhp%2Cfeaturedate%2Cmainstemid%2Cgnisid%2Cgnisidlabel%2Cfeaturetype%2Cfeaturetypelabel%2Careasqkm%2Cworkunitid&returnGeometry=false&resultRecordCount=20)
- [Waterton 3DHP connector query](https://hydro.nationalmap.gov/arcgis/rest/services/3DHP_all/MapServer/50/query?f=pjson&where=gnisid%3D201759&geometry=-105.12%2C39.47%2C-105.05%2C39.52&geometryType=esriGeometryEnvelope&inSR=4326&spatialRel=esriSpatialRelIntersects&outFields=id3dhp%2Cfeaturedate%2Cmainstemid%2Cgnisid%2Cgnisidlabel%2Cfeaturetype%2Cfeaturetypelabel%2Cwaterbodyid3dhp%2Cstreamorder%2Chydrosequence%2Clevelpath%2Cworkunitid&returnGeometry=false&resultRecordCount=20)
- [Salvation Ditch 3DHP query](https://hydro.nationalmap.gov/arcgis/rest/services/3DHP_all/MapServer/50/query?f=pjson&where=gnisid%3D202674&outFields=id3dhp%2Cfeaturedate%2Cmainstemid%2Cgnisid%2Cgnisidlabel%2Cfeaturetype%2Cfeaturetypelabel%2Cwaterbodyid3dhp%2Cstreamlevel%2Cstreamorder%2Chydrosequence%2Clevelpath%2Cworkunitid&returnGeometry=false&resultRecordCount=20)

### Lakes, reservoirs, and ponds

| Sample | NHD values | 3DHP values | Finding | Status |
|---|---|---|---|---|
| Chatfield Lake | ID `117822739`; reachcode `10190002001067`; GNIS `00202884`; FType/FCode `390/39009` | `L11WE`; GNIS `202884`; type `3`, `Lake`; area `5.62239081` km²; mainstem null | NHD perennial lake becomes generic 3DHP Lake. | RETRIEVED |
| Chatfield Reservoir | ID `90214667`; reachcode `14050001002566`; GNIS `00173386`; FType/FCode `390/39004` | `IOEU5`; GNIS `173386`; type `3`, `Lake`; area `0.046` km²; mainstem null | The name contains “Reservoir,” but the attributes classify it only as Lake. The name is not a dependable reservoir-purpose field. | RETRIEVED / INFERRED |
| Rueter-Hess Reservoir | ID `{C4A03B96-2738-484A-995F-2B66C36738E0}`; reachcode `10190003010390`; GNIS `02761016`; FType/FCode `436/43619` | `JIQFW`; GNIS `2761016`; type `3`, `Lake`; area `0.87539065` km²; mainstem null | NHD Reservoir/nonearthen classification is lost. | RETRIEVED |
| Maroon Lake | ID `72971124`; reachcode `14010004000796`; GNIS `00180260`; FType/FCode `390/39009` | `IOFDL`; GNIS `180260`; type `3`, `Lake`; area `0.06517674` km²; mainstem null | Lake geometry and GNIS identity survive; perennial status does not. | RETRIEVED |
| Douglas County intermittent ponds | Example NHD row: ID `117816305`; reachcode `10190002014147`; null GNIS/name; FType/FCode `390/39001`. Nineteen additional rows were returned in the envelope. | Example 3DHP rows in the same envelope include `IMF9A`, null GNIS/name, type `3`, `Lake`, area `0.001` km², and `INXN5`, area `0.002` km². | The geometry-free queries cannot prove which 3DHP record corresponds to which NHD pond. The 3DHP records expose no intermittent flag. | RETRIEVED / UNKNOWN |

Sources:

- [Named NHD waterbody query](https://hydro.nationalmap.gov/arcgis/rest/services/nhd/MapServer/12/query?f=pjson&where=gnis_name%20LIKE%20%27%25Chatfield%25%27%20OR%20gnis_name%20LIKE%20%27%25Rueter-Hess%25%27%20OR%20gnis_name%20LIKE%20%27%25Maroon%20Lake%25%27&outFields=permanent_identifier%2Creachcode%2Cgnis_id%2Cgnis_name%2Cftype%2Cfcode%2Cresolution%2Cvisibilityfilter&returnGeometry=false&resultRecordCount=20)
- [Named 3DHP waterbody query](https://hydro.nationalmap.gov/arcgis/rest/services/3DHP_all/MapServer/60/query?f=pjson&where=gnisidlabel%20LIKE%20%27%25Chatfield%25%27%20OR%20gnisidlabel%20LIKE%20%27%25Rueter-Hess%25%27%20OR%20gnisidlabel%20LIKE%20%27%25Maroon%20Lake%25%27&outFields=id3dhp%2Cfeaturedate%2Cmainstemid%2Cgnisid%2Cgnisidlabel%2Cfeaturetype%2Cfeaturetypelabel%2Careasqkm%2Cworkunitid&returnGeometry=false&resultRecordCount=20)
- [Douglas County NHD intermittent-pond query](https://hydro.nationalmap.gov/arcgis/rest/services/nhd/MapServer/12/query?f=pjson&where=fcode%3D39001&geometry=-104.95%2C39.45%2C-104.75%2C39.58&geometryType=esriGeometryEnvelope&inSR=4326&spatialRel=esriSpatialRelIntersects&outFields=permanent_identifier%2Creachcode%2Cgnis_id%2Cgnis_name%2Cftype%2Cfcode%2Cresolution&returnGeometry=false&resultRecordCount=20)
- [Douglas County 3DHP Lake query](https://hydro.nationalmap.gov/arcgis/rest/services/3DHP_all/MapServer/60/query?f=pjson&where=featuretype%3D3&geometry=-104.95%2C39.45%2C-104.75%2C39.58&geometryType=esriGeometryEnvelope&inSR=4326&spatialRel=esriSpatialRelIntersects&outFields=id3dhp%2Cfeaturedate%2Cmainstemid%2Cgnisid%2Cgnisidlabel%2Cfeaturetype%2Cfeaturetypelabel%2Careasqkm%2Cworkunitid&returnGeometry=false&resultRecordCount=20)

## Identifiers and stability

| Identifier | Meaning and observed behavior | Stability/crosswalk finding | Status |
|---|---|---|---|
| `id3dhp` | Seven-character base-36 identifier for an individual 3DHP feature | USGS explicitly says it “is not persistent.” It is unsuitable as an immutable public source ID across refreshes. | RETRIEVED |
| `mainstemid` | Cross-dataset URI for flowlines on a river’s headwater-to-outlet path | Intended as a persistent, scale-independent, cross-dataset identifier. It identifies a mainstem, not an individual segment. | RETRIEVED |
| `gnisid` | Permanent unique number assigned by GNIS to a geographic feature name | Stable for the name, nullable on unnamed features, and not an individual geometry-segment ID. | RETRIEVED |
| NHD `permanent_identifier` | Individual NHD feature identifier | Present in NHD queries but absent from both live 3DHP schemas. | RETRIEVED |
| NHD `reachcode` | NHD reach identifier | Present in NHD queries but absent from both live 3DHP schemas. | RETRIEVED |
| Direct NHD-segment crosswalk field | Field carrying `permanent_identifier` or `reachcode` | None in the live flowline or waterbody schemas. | RETRIEVED |
| `workunitid` | Source/work-unit marker | Every sampled record returned `NHD`; it identifies source provenance in these samples, not the old NHD segment identifier. | RETRIEVED |

Sources: [USGS flowline dictionary](https://www.usgs.gov/ngp-standards-and-specifications/3d-hydrography-program-3dhpall-flowline), [USGS waterbody dictionary](https://www.usgs.gov/ngp-standards-and-specifications/3d-hydrography-program-3dhpall-waterbody), [flowline schema](https://hydro.nationalmap.gov/arcgis/rest/services/3DHP_all/MapServer/50?f=pjson), and [waterbody schema](https://hydro.nationalmap.gov/arcgis/rest/services/3DHP_all/MapServer/60?f=pjson).

USGS calls mainstem identifiers “persistent, scale-independent unique identifiers” and says they support crosswalks among historical datasets and 3DHP. [USGS hydrography history](https://www.usgs.gov/3d-hydrography-program/abridged-history-hydrography-datasets) — RETRIEVED.

No retrieved source says that `id3dhp` remains stable between service refreshes; the specification says the opposite. [USGS flowline dictionary](https://www.usgs.gov/ngp-standards-and-specifications/3d-hydrography-program-3dhpall-flowline) — RETRIEVED.

## Network identifiers

| Field | USGS meaning | Sample evidence | Status |
|---|---|---|---|
| `mainstemid` | Cross-dataset ID for a headwater-to-outlet river path | All 20 retrieved Roaring Fork rows shared `https://geoconnex.us/ref/mainstems/40769`. | RETRIEVED |
| `levelpath` | Hydrosequence of the most downstream flowline on the same StreamLevel path | All 20 retrieved Roaring Fork rows had `27503096`. | RETRIEVED |
| `streamorder` | Strahler stream order | Roaring Fork sampled values varied from `2` through `8`; it is segment-specific, not a river-group key. | RETRIEVED |
| `hydrosequence` | Nationally unique topological sequence; upstream values are larger when a path exists | Roaring Fork sample values included `27514648`, `27612062`, `27909300`, and `27975832`. | RETRIEVED |
| `streamlevel` | Numeric main-path level intended to be constant for a mainstem | Roaring Fork sample value was consistently `2`. | RETRIEVED |

Sources: [USGS flowline dictionary](https://www.usgs.gov/ngp-standards-and-specifications/3d-hydrography-program-3dhpall-flowline) and [Roaring Fork query](https://hydro.nationalmap.gov/arcgis/rest/services/3DHP_all/MapServer/50/query?f=pjson&where=gnisid%3D174812&outFields=id3dhp%2Cfeaturedate%2Cmainstemid%2Cgnisid%2Cgnisidlabel%2Cfeaturetype%2Cfeaturetypelabel%2Cwaterbodyid3dhp%2Cstreamlevel%2Cstreamorder%2Chydrosequence%2Clevelpath%2Cworkunitid&returnGeometry=false&resultRecordCount=20).

The retrieved Roaring Fork sample supports grouping that river by `mainstemid`, but the result was capped at 20 and reported `exceededTransferLimit=true`; it does not prove every Roaring Fork segment nationwide has that value. [Roaring Fork query](https://hydro.nationalmap.gov/arcgis/rest/services/3DHP_all/MapServer/50/query?f=pjson&where=gnisid%3D174812&outFields=id3dhp%2Cfeaturedate%2Cmainstemid%2Cgnisid%2Cgnisidlabel%2Cfeaturetype%2Cfeaturetypelabel%2Cwaterbodyid3dhp%2Cstreamlevel%2Cstreamorder%2Chydrosequence%2Clevelpath%2Cworkunitid&returnGeometry=false&resultRecordCount=20) — RETRIEVED.

A named river should not be grouped solely by GNIS ID if end-to-end hydrologic identity matters: GNIS identifies a name, while `mainstemid` identifies the mainstem path. Combining `gnisid`, `mainstemid`, topology, and connector inclusion is safer. [USGS flowline dictionary](https://www.usgs.gov/ngp-standards-and-specifications/3d-hydrography-program-3dhpall-flowline) — INFERRED.

## Wide rivers and rivers passing through lakes

In Waterton Canyon, NHD returned a polygonal perennial Stream/River area and multiple Artificial Path flowlines. [Waterton NHD area query](https://hydro.nationalmap.gov/arcgis/rest/services/nhd/MapServer/9/query?f=pjson&where=ftype%3D460&geometry=-105.12%2C39.47%2C-105.05%2C39.52&geometryType=esriGeometryEnvelope&inSR=4326&spatialRel=esriSpatialRelIntersects&outFields=permanent_identifier%2Cgnis_id%2Cgnis_name%2Cftype%2Cfcode%2Cresolution&returnGeometry=false&resultRecordCount=20) [Waterton NHD flowline query](https://hydro.nationalmap.gov/arcgis/rest/services/nhd/MapServer/6/query?f=pjson&where=gnis_id%3D%2700201759%27&geometry=-105.12%2C39.47%2C-105.05%2C39.52&geometryType=esriGeometryEnvelope&inSR=4326&spatialRel=esriSpatialRelIntersects&outFields=permanent_identifier%2Creachcode%2Cgnis_id%2Cgnis_name%2Cftype%2Cfcode%2Cflowdir&returnGeometry=false&resultRecordCount=20) — RETRIEVED.

3DHP represents that arrangement as:

1. waterbody `OISYK`, type `1`, River; and
2. multiple flowlines of type `5`, Waterbody Connector, each with `waterbodyid3dhp="OISYK"`.

[Waterton 3DHP waterbody query](https://hydro.nationalmap.gov/arcgis/rest/services/3DHP_all/MapServer/60/query?f=pjson&where=featuretype%3D1&geometry=-105.12%2C39.47%2C-105.05%2C39.52&geometryType=esriGeometryEnvelope&inSR=4326&spatialRel=esriSpatialRelIntersects&outFields=id3dhp%2Cfeaturedate%2Cmainstemid%2Cgnisid%2Cgnisidlabel%2Cfeaturetype%2Cfeaturetypelabel%2Careasqkm%2Cworkunitid&returnGeometry=false&resultRecordCount=20) [Waterton 3DHP connector query](https://hydro.nationalmap.gov/arcgis/rest/services/3DHP_all/MapServer/50/query?f=pjson&where=gnisid%3D201759&geometry=-105.12%2C39.47%2C-105.05%2C39.52&geometryType=esriGeometryEnvelope&inSR=4326&spatialRel=esriSpatialRelIntersects&outFields=id3dhp%2Cfeaturedate%2Cmainstemid%2Cgnisid%2Cgnisidlabel%2Cfeaturetype%2Cfeaturetypelabel%2Cwaterbodyid3dhp%2Cstreamorder%2Chydrosequence%2Clevelpath%2Cworkunitid&returnGeometry=false&resultRecordCount=20) — RETRIEVED.

The same model handles a river crossing a lake: the in-water line is a Waterbody Connector, and `waterbodyid3dhp` points to the enclosing lake polygon. The Roaring Fork sample includes connectors through waterbodies `OHC6D`, `OHJL1`, and `LWAXC`; Castle Creek includes one through `OJ7ML`. [Roaring Fork query](https://hydro.nationalmap.gov/arcgis/rest/services/3DHP_all/MapServer/50/query?f=pjson&where=gnisid%3D174812&outFields=id3dhp%2Cfeaturedate%2Cmainstemid%2Cgnisid%2Cgnisidlabel%2Cfeaturetype%2Cfeaturetypelabel%2Cwaterbodyid3dhp%2Cstreamlevel%2Cstreamorder%2Chydrosequence%2Clevelpath%2Cworkunitid&returnGeometry=false&resultRecordCount=20) [Castle Creek query](https://hydro.nationalmap.gov/arcgis/rest/services/3DHP_all/MapServer/50/query?f=pjson&where=gnisid%3D1139440&outFields=id3dhp%2Cfeaturedate%2Cmainstemid%2Cgnisid%2Cgnisidlabel%2Cfeaturetype%2Cfeaturetypelabel%2Cwaterbodyid3dhp%2Cstreamlevel%2Cstreamorder%2Chydrosequence%2Clevelpath%2Cworkunitid&returnGeometry=false&resultRecordCount=20) — RETRIEVED.

Therefore, excluding all connector flowlines before constructing river geometry would break centerline continuity through wide rivers and lakes. Connectors should be excluded from recreation eligibility, but retained internally for network assembly and centerline rendering. This is an implementation inference, not an access or recreation-permission finding. [USGS flowline dictionary](https://www.usgs.gov/ngp-standards-and-specifications/3d-hydrography-program-3dhpall-flowline) — INFERRED.

## Data provenance and currency

| Question | Finding | Status |
|---|---|---|
| Current live-service refresh date | September 4, 2026 | RETRIEVED |
| Public access-page update statement | July 2026 | RETRIEVED |
| Update cadence | USGS says new EDH data and attributes are added quarterly | RETRIEVED |
| Sample source | Every sampled feature returned `workunitid="NHD"` | RETRIEVED |
| EDH coverage over the broad Colorado sample envelope | Layer 92 returned no EDH work-unit features | RETRIEVED |
| Are the sampled features elevation-derived? | No evidence retrieved that they are; the direct feature marker says `NHD` | RETRIEVED |
| How to tell per feature | Inspect `workunitid`; `NHD` denotes converted NHD in these records. For EDH, also inspect the EDH Workunit Area layer and its work-unit fields. | RETRIEVED / INFERRED |
| Future source stability | USGS says EDH will replace NHD data as EDH is collected, so geometry, segmentation, and `id3dhp` can change. | RETRIEVED / INFERRED |

Sources: [live service metadata](https://hydro.nationalmap.gov/arcgis/rest/services/3DHP_all/MapServer?f=pjson), [USGS access page](https://www.usgs.gov/3d-hydrography-program/access-3dhp-data-products), [USGS service specification](https://www.usgs.gov/ngp-standards-and-specifications/3d-hydrography-program-products-3dhpall-2023-service-specification), and [EDH work-unit query](https://hydro.nationalmap.gov/arcgis/rest/services/3DHP_all/MapServer/92/query?f=pjson&where=1%3D1&geometry=-107.0%2C39.0%2C-104.7%2C39.65&geometryType=esriGeometryEnvelope&inSR=4326&spatialRel=esriSpatialRelIntersects&outFields=*&returnGeometry=false&resultRecordCount=20).

## Ohvernight rule impact

| Ohvernight rule | Result after a direct move | Why | Status |
|---|---|---|---|
| Select perennial streams only | BREAKS | 3DHP collapses NHD `46003`, `46006`, and `46007` to River and exposes no permanence field. | RETRIEVED / INFERRED |
| Exclude canals/ditches | SURVIVES, with testing | `featuretype=2` identifies canals, including Salvation Ditch samples. Wide polygon canals also use waterbody type `2`. | RETRIEVED |
| Exclude pipelines | PARTIALLY BREAKS | Pipelines map to type `7`, but type `7` also includes underground conduits, generic connectors, and non-NHD connectors. Pipelines can be conservatively excluded only by excluding the entire type. | RETRIEVED / INFERRED |
| Exclude connectors from displayed recreation features | SURVIVES | Types `4`–`7` are distinguishable numerically. | RETRIEVED |
| Exclude connectors from network construction | BREAKS NETWORKS | Type `5` supplies centerlines through water polygons; Salvation Ditch also contains connector segments. | RETRIEVED / INFERRED |
| Show perennial lakes only | BREAKS | NHD intermittent and perennial lake FCodes both map to type `3`, and no permanence attribute survives. | RETRIEVED / INFERRED |
| Exclude treatment, tailings, sewage, disposal, and similar reservoirs | BREAKS | All listed NHD reservoir purposes map to generic type `3`, Lake. | RETRIEVED / INFERRED |
| Distinguish natural lake from reservoir | BREAKS | The waterbody domain explicitly combines natural and manmade lakes, ponds, and reservoirs. | RETRIEVED |
| Group a river by GNIS ID with end-to-end connectivity | PARTIALLY SURVIVES | GNIS survives for named segments, but is nullable and identifies the name rather than the complete hydrologic mainstem. `mainstemid`, topology, and connectors are also needed. | RETRIEVED / INFERRED |
| Draw centerlines through wide-river areas | SURVIVES | Waterbody Connector plus `waterbodyid3dhp` provides the required centerline/polygon relationship. | RETRIEVED |
| Stable source-backed feature IDs | BREAKS for segment IDs | USGS explicitly says `id3dhp` is not persistent, and the live schema carries neither NHD permanent ID nor reachcode. | RETRIEVED / INFERRED |
| Stable river-level grouping | LIKELY SURVIVES | USGS describes mainstem IDs as persistent and cross-dataset; sampled Roaring Fork records shared one mainstem ID. | RETRIEVED |
| Preserve old NHD behavior while source is still NHD-derived | DOES NOT SURVIVE AUTOMATICALLY | Although `workunitid=NHD`, the 3DHP transformation has already discarded permanence and reservoir-purpose attributes. | RETRIEVED / INFERRED |

Primary evidence: [USGS crosswalk](https://www.usgs.gov/ngp-standards-and-specifications/3d-hydrography-program-product-specification-crosswalk-tables), [flowline dictionary](https://www.usgs.gov/ngp-standards-and-specifications/3d-hydrography-program-3dhpall-flowline), [waterbody dictionary](https://www.usgs.gov/ngp-standards-and-specifications/3d-hydrography-program-3dhpall-waterbody), [flowline schema](https://hydro.nationalmap.gov/arcgis/rest/services/3DHP_all/MapServer/50?f=pjson), and [waterbody schema](https://hydro.nationalmap.gov/arcgis/rest/services/3DHP_all/MapServer/60?f=pjson).

## Required validation gates before switching

1. **Permanence restoration:** obtain an official, maintained 3DHP attribute or crosswalk that restores stream and waterbody perennial/intermittent/ephemeral values. Without it, perennial-only selection must fail closed. Current absence is RETRIEVED. [Flowline schema](https://hydro.nationalmap.gov/arcgis/rest/services/3DHP_all/MapServer/50?f=pjson) [Waterbody schema](https://hydro.nationalmap.gov/arcgis/rest/services/3DHP_all/MapServer/60?f=pjson)

2. **Reservoir-purpose restoration:** prove that natural lakes can be separated from storage, treatment, tailings, sewage, disposal, filtration, settling, cooling, and similar reservoirs using an official maintained source. Current 3DHP cannot do so. [USGS crosswalk](https://www.usgs.gov/ngp-standards-and-specifications/3d-hydrography-program-product-specification-crosswalk-tables) — RETRIEVED.

3. **Stable-ID design:** do not publish `id3dhp` as an immutable ID. Define and test a versioned identity scheme using appropriate combinations of source release, `mainstemid`, `gnisid`, geometry lineage, and local IDs. [USGS flowline dictionary](https://www.usgs.gov/ngp-standards-and-specifications/3d-hydrography-program-3dhpall-flowline) — INFERRED from the retrieved non-persistence warning.

4. **Cross-release churn test:** snapshot at least two quarterly service releases and measure additions, deletions, splits, merges, `id3dhp` changes, mainstem changes, and source transitions from `NHD` to EDH. Quarterly updates and eventual EDH replacement are RETRIEVED. [USGS access page](https://www.usgs.gov/3d-hydrography-program/access-3dhp-data-products) [Service metadata](https://hydro.nationalmap.gov/arcgis/rest/services/3DHP_all/MapServer?f=pjson)

5. **Numeric-code test:** filter on numeric `featuretype`, not `featuretypelabel`, because code `1` returned `Channel Line` in sampled NHD-derived flowlines while the formal domain calls it River. [Castle Creek query](https://hydro.nationalmap.gov/arcgis/rest/services/3DHP_all/MapServer/50/query?f=pjson&where=gnisid%3D1139440&outFields=id3dhp%2Cfeaturedate%2Cmainstemid%2Cgnisid%2Cgnisidlabel%2Cfeaturetype%2Cfeaturetypelabel%2Cwaterbodyid3dhp%2Cstreamlevel%2Cstreamorder%2Chydrosequence%2Clevelpath%2Cworkunitid&returnGeometry=false&resultRecordCount=20) — RETRIEVED.

6. **Connector policy test:** retain type `5` internally for topology and centerlines, while preventing it from being interpreted as an independently eligible recreation feature. Test Waterton Canyon, Roaring Fork, Castle Creek, Happy Canyon Creek, and Salvation Ditch. [USGS flowline dictionary](https://www.usgs.gov/ngp-standards-and-specifications/3d-hydrography-program-3dhpall-flowline) — INFERRED.

7. **Wide-water rendering test:** verify every Waterbody Connector references an existing `waterbodyid3dhp`, remains inside or appropriately connected to that polygon, and joins channel lines at both ends. Waterton provides a concrete fixture with `OISYK`. [Waterton connector query](https://hydro.nationalmap.gov/arcgis/rest/services/3DHP_all/MapServer/50/query?f=pjson&where=gnisid%3D201759&geometry=-105.12%2C39.47%2C-105.05%2C39.52&geometryType=esriGeometryEnvelope&inSR=4326&spatialRel=esriSpatialRelIntersects&outFields=id3dhp%2Cfeaturedate%2Cmainstemid%2Cgnisid%2Cgnisidlabel%2Cfeaturetype%2Cfeaturetypelabel%2Cwaterbodyid3dhp%2Cstreamorder%2Chydrosequence%2Clevelpath%2Cworkunitid&returnGeometry=false&resultRecordCount=20) — INFERRED.

8. **Mainstem completeness test:** validate that all expected Roaring Fork segments—including channel and waterbody connectors—share mainstem `https://geoconnex.us/ref/mainstems/40769`, with no disconnected omissions. The bounded sample supports but does not prove completeness. [Roaring Fork query](https://hydro.nationalmap.gov/arcgis/rest/services/3DHP_all/MapServer/50/query?f=pjson&where=gnisid%3D174812&outFields=id3dhp%2Cfeaturedate%2Cmainstemid%2Cgnisid%2Cgnisidlabel%2Cfeaturetype%2Cfeaturetypelabel%2Cwaterbodyid3dhp%2Cstreamlevel%2Cstreamorder%2Chydrosequence%2Clevelpath%2Cworkunitid&returnGeometry=false&resultRecordCount=20) — RETRIEVED / UNKNOWN.

9. **GNIS exception test:** quantify unnamed/null-GNIS flowlines and waterbodies and ensure they neither disappear nor merge incorrectly. The sampled Waterton polygon and Douglas ponds had null GNIS values. [Waterton waterbody query](https://hydro.nationalmap.gov/arcgis/rest/services/3DHP_all/MapServer/60/query?f=pjson&where=featuretype%3D1&geometry=-105.12%2C39.47%2C-105.05%2C39.52&geometryType=esriGeometryEnvelope&inSR=4326&spatialRel=esriSpatialRelIntersects&outFields=id3dhp%2Cfeaturedate%2Cmainstemid%2Cgnisid%2Cgnisidlabel%2Cfeaturetype%2Cfeaturetypelabel%2Careasqkm%2Cworkunitid&returnGeometry=false&resultRecordCount=20) [Douglas waterbody query](https://hydro.nationalmap.gov/arcgis/rest/services/3DHP_all/MapServer/60/query?f=pjson&where=featuretype%3D3&geometry=-104.95%2C39.45%2C-104.75%2C39.58&geometryType=esriGeometryEnvelope&inSR=4326&spatialRel=esriSpatialRelIntersects&outFields=id3dhp%2Cfeaturedate%2Cmainstemid%2Cgnisid%2Cgnisidlabel%2Cfeaturetype%2Cfeaturetypelabel%2Careasqkm%2Cworkunitid&returnGeometry=false&resultRecordCount=20) — RETRIEVED.

10. **EDH transition test:** repeat all fixtures after Colorado EDH work units appear. Do not assume converted-NHD behavior predicts EDH geometry, segmentation, attribution, or IDs. USGS says EDH replaces NHD as it becomes available. [3DHP service metadata](https://hydro.nationalmap.gov/arcgis/rest/services/3DHP_all/MapServer?f=pjson) — RETRIEVED / INFERRED.

11. **Access separation test:** keep hydrographic existence and geometry separate from recreation access and permission. Neither NHD nor 3DHP classification establishes fishing, boating, paddling, swimming, parking, camping, or bank access. The 3DHP service itself says it is not intended for site-specific regulatory determinations. [3DHP service metadata](https://hydro.nationalmap.gov/arcgis/rest/services/3DHP_all/MapServer?f=pjson) — RETRIEVED / INFERRED.

## Unknowns

- Whether USGS will add streamflow permanence to a future `3DHP_all` field or separate service is UNKNOWN. The current service does not contain it, although USGS’s broader program page says 3DHP intends to improve attribution of streamflow permanence. No future schema or delivery date was retrieved. [USGS 3DHP program page](https://www.usgs.gov/3d-hydrography-program) [Current flowline schema](https://hydro.nationalmap.gov/arcgis/rest/services/3DHP_all/MapServer/50?f=pjson)

- Whether an official segment-level NHD `permanent_identifier`/`reachcode` to `id3dhp` crosswalk exists outside the live service and the retrieved product crosswalk is UNKNOWN. No such field or table appeared in the retrieved live service. [3DHP service metadata](https://hydro.nationalmap.gov/arcgis/rest/services/3DHP_all/MapServer?f=pjson)

- Exact NHD attributes for Salvation Ditch are UNKNOWN because both targeted NHD requests timed out; only the 3DHP values and the official class crosswalk were retrieved. [Salvation Ditch 3DHP query](https://hydro.nationalmap.gov/arcgis/rest/services/3DHP_all/MapServer/50/query?f=pjson&where=gnisid%3D202674&outFields=id3dhp%2Cfeaturedate%2Cmainstemid%2Cgnisid%2Cgnisidlabel%2Cfeaturetype%2Cfeaturetypelabel%2Cwaterbodyid3dhp%2Cstreamlevel%2Cstreamorder%2Chydrosequence%2Clevelpath%2Cworkunitid&returnGeometry=false&resultRecordCount=20)

- A one-to-one pairing between a particular unnamed Douglas County NHD intermittent pond and a particular 3DHP Lake is UNKNOWN because the required queries were geometry-free and 3DHP exposes no NHD permanent ID. [NHD pond query](https://hydro.nationalmap.gov/arcgis/rest/services/nhd/MapServer/12/query?f=pjson&where=fcode%3D39001&geometry=-104.95%2C39.45%2C-104.75%2C39.58&geometryType=esriGeometryEnvelope&inSR=4326&spatialRel=esriSpatialRelIntersects&outFields=permanent_identifier%2Creachcode%2Cgnis_id%2Cgnis_name%2Cftype%2Cfcode%2Cresolution&returnGeometry=false&resultRecordCount=20) [3DHP pond-area query](https://hydro.nationalmap.gov/arcgis/rest/services/3DHP_all/MapServer/60/query?f=pjson&where=featuretype%3D3&geometry=-104.95%2C39.45%2C-104.75%2C39.58&geometryType=esriGeometryEnvelope&inSR=4326&spatialRel=esriSpatialRelIntersects&outFields=id3dhp%2Cfeaturedate%2Cmainstemid%2Cgnisid%2Cgnisidlabel%2Cfeaturetype%2Cfeaturetypelabel%2Careasqkm%2Cworkunitid&returnGeometry=false&resultRecordCount=20)

- End-to-end completeness of the Roaring Fork mainstem is UNKNOWN because the query was capped at 20 and exceeded the transfer limit. [Roaring Fork query](https://hydro.nationalmap.gov/arcgis/rest/services/3DHP_all/MapServer/50/query?f=pjson&where=gnisid%3D174812&outFields=id3dhp%2Cfeaturedate%2Cmainstemid%2Cgnisid%2Cgnisidlabel%2Cfeaturetype%2Cfeaturetypelabel%2Cwaterbodyid3dhp%2Cstreamlevel%2Cstreamorder%2Chydrosequence%2Clevelpath%2Cworkunitid&returnGeometry=false&resultRecordCount=20)

- Public access and recreation permission for every sampled water feature are UNKNOWN. Hydrography metadata does not establish those rights.

## Recommendation

Do not switch Ohvernight’s production selection logic from retired NHD to the current `3DHP_all` service.

RETRIEVED evidence shows that 3DHP preserves useful geometry, GNIS identifiers, mainstem grouping, network derivatives, wide-river polygons, and linked centerlines. It also cleanly identifies canals and broad connector classes. [USGS flowline dictionary](https://www.usgs.gov/ngp-standards-and-specifications/3d-hydrography-program-3dhpall-flowline) [USGS waterbody dictionary](https://www.usgs.gov/ngp-standards-and-specifications/3d-hydrography-program-3dhpall-waterbody)

The current service nevertheless removes three attributes required by Ohvernight’s existing safety-oriented rules: stream permanence, waterbody permanence, and reservoir purpose. It also supplies only a nonpersistent individual-feature ID and no live NHD permanent-ID/reachcode crosswalk field. [USGS crosswalk](https://www.usgs.gov/ngp-standards-and-specifications/3d-hydrography-program-product-specification-crosswalk-tables) [Flowline schema](https://hydro.nationalmap.gov/arcgis/rest/services/3DHP_all/MapServer/50?f=pjson) [Waterbody schema](https://hydro.nationalmap.gov/arcgis/rest/services/3DHP_all/MapServer/60?f=pjson)

Continue using the retired NHD source for current rule fidelity. Build a parallel, non-production 3DHP evaluation pipeline for topology and geometry only, retain Waterbody Connectors internally, and reconsider migration only after every validation gate above passes—especially official restoration of permanence and reservoir-purpose classifications and a tested stable-ID strategy.
