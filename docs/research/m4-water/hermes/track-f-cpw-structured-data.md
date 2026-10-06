<!-- Hermes research report, M4 track F (focused follow-up on CPW structured data, owner decision D7). Retrieved 2026-10-06 with web search and page reading only. This is a research INPUT, kept verbatim: it is not verified in the trust sense (ADR-004, ADR-005). -->

# CPW Structured Fishing and Boating Data: Reuse and Redistribution Review

Research date: 2026-10-06

Scope: Colorado Fishing Atlas REST services, selected fishing and boating layers, CPW’s ArcGIS Online organization, Colorado Information Marketplace metadata and applicable public-facing terms. This is an evidence review, not legal advice.

## Which service is current

### Service inventory

[RETRIEVED] The NDIS ArcGIS root currently contains these relevant folders:

- `FishingAtlas`
- `FishingAtlas2025`
- `CPW`
- `HuntingAtlas`
- `HuntingAtlas2025`

Source: https://ndismaps.nrel.colostate.edu/arcgis/rest/services?f=pjson

[RETRIEVED] `FishingAtlas` contains:

- `FishingAtlas/FishingAtlas_Base_Map`
- `FishingAtlas/FishingAtlas_Data`
- `FishingAtlas/FishingAtlas_Main_Map`

Source: https://ndismaps.nrel.colostate.edu/arcgis/rest/services/FishingAtlas?f=pjson

[RETRIEVED] `FishingAtlas2025` contains:

- `FishingAtlas2025/BaseData2025`
- `FishingAtlas2025/FishingInfo2025`
- `FishingAtlas2025/LandAccess2025`
- `FishingAtlas2025/LandAccessSub2025`
- `FishingAtlas2025/NonDisplay2025`

Source: https://ndismaps.nrel.colostate.edu/arcgis/rest/services/FishingAtlas2025?f=pjson

### Comparison

| Property | Legacy `FishingAtlas_Data` | `FishingInfo2025` |
|---|---|---|
| URL | https://ndismaps.nrel.colostate.edu/arcgis/rest/services/FishingAtlas/FishingAtlas_Data/MapServer?f=pjson | https://ndismaps.nrel.colostate.edu/arcgis/rest/services/FishingAtlas2025/FishingInfo2025/MapServer?f=pjson |
| Map name | `Layers` | `FishingInfo2025` |
| Layer-list entries | 17: IDs 0–16, including one group | 36: IDs 0–35, including 11 scale/group layers and 25 feature-layer entries |
| Structure | One copy of each thematic layer | Scale-dependent copies of Fishing Information and Special Regulations layers |
| Accessible Fishing Area | Absent | ID 0 |
| Fishing Information Point | ID 0, direct feature layer | Group ID 1; feature layers 3, 5 and 7 |
| Boat Ramp | ID 3 | ID 8 |
| Special Regulations | Stream 5, lake 12, property 13 | Scale-dependent stream/lake/property layers at IDs 11–32 |
| Gold Medal Streams/Lakes | IDs 8 and 9 | IDs 34 and 35 |
| All Streams / All Lakes | IDs 10 and 11 | Absent from this service |
| Watercode Streams / Waterbodies | IDs 15 and 16 | Absent from this service |
| `description` | Empty | Empty |
| `copyrightText` | Empty | Empty |
| `documentInfo.Title` | Empty | `Map` |
| Other document information | Author, Comments, Subject, Category and Keywords empty | Same fields empty |
| Antialiasing | `None` | `Fast` |
| Capabilities | `Map,Query,Data` | `Map,Query,Data` |
| Query formats | `JSON, geoJSON` | `JSON, geoJSON, PBF` |
| Maximum records | 1,000 | 2,000 |
| Extensions | `KmlServer` | Empty |
| Additional query features | Standard legacy query support | Adds clipping, spatial filtering and query-data-elements support |

[INFERRED] `FishingAtlas2025/FishingInfo2025` is the current display service. Reasons:

1. It is explicitly versioned `2025`.
2. The live Fishing Atlas displays “Accessible Fishing Area” and scale-grouped Fishing Information layers matching the 2025 service.
3. Its legend and explanatory text match the 2025 layer organization.
4. It has newer ArcGIS Pro/CIM metadata and a 2,000-record limit.

Live application: https://ndismaps.nrel.colostate.edu/fishingatlas

[INFERRED] The legacy `FishingAtlas_Data` service remains operational and useful as a structured-data/search service, especially because it uniquely exposes `All Streams`, `All Lakes`, `Watercode Streams`, and `Watercode Waterbodies`. Its continued availability does not establish that it is current, licensed for republication, or contractually stable.

## Layer schemas

The requested names below are from the legacy `FishingAtlas/FishingAtlas_Data` service. Type strings and aliases are reproduced from each layer’s `?f=pjson`. Unless noted, every field’s `domain` is `null`.

### Fishing Information Point

| Property | Value |
|---|---|
| Layer / source | ID 0 — https://ndismaps.nrel.colostate.edu/arcgis/rest/services/FishingAtlas/FishingAtlas_Data/MapServer/0?f=pjson |
| Geometry | `esriGeometryPoint`; geometry field `Shape` |
| Fields: exact name — type — alias | `Shape` — `esriFieldTypeGeometry` — `Shape`; `WATERCODE` — `esriFieldTypeString` (10) — `WATERCODE`; `FA_NAME` — `esriFieldTypeString` (100) — `FA_NAME`; `FA_NAME2` — `esriFieldTypeString` (100) — `FA_NAME2`; `DISP_PRIORITY` — `esriFieldTypeSmallInteger` — `DISP_PRIORITY`; `PROP_NAME` — `esriFieldTypeString` (100) — `PROP_NAME`; `DRIVING_URL` — `esriFieldTypeString` (255) — `DRIVING_URL`; `SURVEY_URL` — `esriFieldTypeString` (255) — `SURVEY_URL`; `OPP_FAMILY` — `esriFieldTypeString` (10) — `OPP_FAMILY`; `OPP_RUSTIC` — `esriFieldTypeString` (10) — `OPP_RUSTIC`; `OPP_ICE` — `esriFieldTypeString` (10) — `OPP_ICE`; `STOCKED` — `esriFieldTypeString` (50) — `STOCKED`; `LOC_TYPE` — `esriFieldTypeString` (30) — `LOC_TYPE`; `COUNTYNAME` — `esriFieldTypeString` (15) — `COUNTYNAME`; `REPORTS_URL` — `esriFieldTypeString` (255) — `REPORTS_URL`; `ELEV_FT_TXT` — `esriFieldTypeString` (10) — `ELEV_FT_TXT`; `PROP_ID` — `esriFieldTypeString` (255) — `PROP_ID`; `BOATING` — `esriFieldTypeString` (20) — `BOATING`; `ACCESS_EASE` — `esriFieldTypeString` (10) — `ACCESS_EASE`; `FISH_PRESSURE` — `esriFieldTypeString` (10) — `FISH_PRESSURE`; `HANDI_PIER` — `esriFieldTypeString` (10) — `HANDI_PIER`; `UNI_ID` — `esriFieldTypeInteger` — `UNI_ID`; `Illegal_Stocking` — `esriFieldTypeString` (255) — `Illegal_Stocking`; `SpotURL` — `esriFieldTypeString` (255) — `SpotURL`; `OBJECTID_12` — `esriFieldTypeOID` — `OBJECTID_12`; `CONTACT_CODE` — `esriFieldTypeString` (5) — `CONTACT_CODE`; `DOW_NAME` — `esriFieldTypeString` (100) — `DOW_NAME`; `xval` — `esriFieldTypeSingle` — `xval`; `yval` — `esriFieldTypeSingle` — `yval`; `ELEV_FT` — `esriFieldTypeInteger` — `ELEV_FT`; `SHOW` — `esriFieldTypeSmallInteger` — `SHOW`; `NOSHOW_REASON` — `esriFieldTypeString` (100) — `NOSHOW_REASON`; `PROP_URL` — `esriFieldTypeString` (255) — `PROP_URL`; `Custom_DD_field` — `esriFieldTypeSmallInteger` — `Custom_DD_field`; `Quality` — `esriFieldTypeSmallInteger` — `Quality`; `GoldMedal` — `esriFieldTypeSmallInteger` — `GoldMedal`; `SUP` — `esriFieldTypeSmallInteger` — `SUP`; `SUP_Desc` — `esriFieldTypeString` (255) — `SUP_Desc` |
| Coded-value domains | None |
| Water code | `WATERCODE`, string length 10 |

### Boat Ramp

| Property | Value |
|---|---|
| Layer / source | ID 3 — https://ndismaps.nrel.colostate.edu/arcgis/rest/services/FishingAtlas/FishingAtlas_Data/MapServer/3?f=pjson |
| Geometry | `esriGeometryPoint`; geometry field `SHAPE` |
| Fields | `OBJECTID` — `esriFieldTypeOID` — `OBJECTID`; `SHAPE` — `esriFieldTypeGeometry` — `SHAPE`; `Manager` — `esriFieldTypeString` (50) — `Manager`; `Property` — `esriFieldTypeString` (50) — `Property`; `FeatureName` — `esriFieldTypeString` (50) — `FeatureName`; `WaterLevelService` — `esriFieldTypeString` (25) — `WaterLevelService`; `Watercode` — `esriFieldTypeString` (8) — `Watercode`; `BoatInspection` — `esriFieldTypeSmallInteger` — `BoatInspection`; `InfoURL` — `esriFieldTypeString` (255) — `InfoURL`; `Notes` — `esriFieldTypeString` (100) — `Notes`; `CollectionDate` — `esriFieldTypeDate` — `CollectionDate`; `CollectionMethod` — `esriFieldTypeString` (20) — `CollectionMethod`; `Water_Type` — `esriFieldTypeString` (10) — `Water_Type`; `SHOW` — `esriFieldTypeSmallInteger` — `SHOW` |
| Coded-value domains | None |
| Water code | `Watercode`, string length 8 |

### Gold Medal Streams

| Property | Value |
|---|---|
| Layer / source | ID 8 — https://ndismaps.nrel.colostate.edu/arcgis/rest/services/FishingAtlas/FishingAtlas_Data/MapServer/8?f=pjson |
| Geometry | `esriGeometryPolyline`; geometry field `Shape` |
| Fields | `OBJECTID` — `esriFieldTypeOID` — `OBJECTID`; `WATERNAME` — `esriFieldTypeString` (30) — `WATERNAME`; `Gold_Medal_Stretch` — `esriFieldTypeString` (50) — `Gold_Medal_Stretch`; `Shape` — `esriFieldTypeGeometry` — `Shape`; `INPUT_ID` — `esriFieldTypeString` (255) — `INPUT_ID`; `INPUT_DATE` — `esriFieldTypeDate` — `INPUT_DATE`; `EDITOR_NAME` — `esriFieldTypeString` (255) — `EDITOR_NAME`; `EDIT_DATE` — `esriFieldTypeDate` — `EDIT_DATE`; `Shape_Length` — `esriFieldTypeDouble` — `Shape_Length` |
| Coded-value domains | None |
| Water code | No `WATERCODE` field |

### Gold Medal Lakes

| Property | Value |
|---|---|
| Layer / source | ID 9 — https://ndismaps.nrel.colostate.edu/arcgis/rest/services/FishingAtlas/FishingAtlas_Data/MapServer/9?f=pjson |
| Geometry | `esriGeometryPolygon`; geometry field `Shape` |
| Fields | `OBJECTID` — `esriFieldTypeOID` — `OBJECTID`; `AREA` — `esriFieldTypeDouble` — `CDPW.DBO.GoldMedalLakes.AREA`; `PERIMETER` — `esriFieldTypeDouble` — `PERIMETER`; `FEATURE1` — `esriFieldTypeInteger` — `FEATURE1`; `CONDITION1` — `esriFieldTypeInteger` — `CONDITION1`; `TYPE1` — `esriFieldTypeInteger` — `TYPE1`; `CODE` — `esriFieldTypeInteger` — `CODE`; `CODE2` — `esriFieldTypeInteger` — `CODE2`; `CODE3` — `esriFieldTypeInteger` — `CODE3`; `NAME` — `esriFieldTypeString` (50) — `NAME`; `AREA_BIO` — `esriFieldTypeString` (3) — `AREA_BIO`; `DOW_NAME` — `esriFieldTypeString` (30) — `DOW_NAME`; `DOW_NAME2` — `esriFieldTypeString` (30) — `DOW_NAME2`; `Shape_Leng` — `esriFieldTypeDouble` — `Shape_Leng`; `Shape` — `esriFieldTypeGeometry` — `Shape`; `Shape_Length` — `esriFieldTypeDouble` — `Shape_Length`; `Shape_Area` — `esriFieldTypeDouble` — `Shape_Area` |
| Coded-value domains | None |
| Water code | No `WATERCODE` field |

### Special Fishing Regulations (stream)

| Property | Value |
|---|---|
| Layer / source | ID 5 — https://ndismaps.nrel.colostate.edu/arcgis/rest/services/FishingAtlas/FishingAtlas_Data/MapServer/5?f=pjson |
| Geometry | `esriGeometryPolyline`; geometry field `Shape` |
| Fields | `OBJECTID` — `esriFieldTypeOID` — `OBJECTID`; `Shape` — `esriFieldTypeGeometry` — `Shape`; `LOC_ID` — `esriFieldTypeInteger` — `LOC_ID`; `Shape_Length` — `esriFieldTypeDouble` — `Shape_Length` |
| Coded-value domains | None |
| Water code | No `WATERCODE` field |

### Special Fishing Regulations (lake)

| Property | Value |
|---|---|
| Layer / source | ID 12 — https://ndismaps.nrel.colostate.edu/arcgis/rest/services/FishingAtlas/FishingAtlas_Data/MapServer/12?f=pjson |
| Geometry | `esriGeometryPolygon`; geometry field `Shape` |
| Fields | `OBJECTID` — `esriFieldTypeOID` — `OBJECTID`; `Shape` — `esriFieldTypeGeometry` — `Shape`; `LOC_ID` — `esriFieldTypeInteger` — `LOC_ID`; `WATERCODE` — `esriFieldTypeString` (10) — `WATERCODE`; `Shape_Length` — `esriFieldTypeDouble` — `Shape_Length`; `Shape_Area` — `esriFieldTypeDouble` — `Shape_Area` |
| Coded-value domains | None |
| Water code | `WATERCODE`, string length 10 |

### Special Fishing Regulations (property)

| Property | Value |
|---|---|
| Layer / source | ID 13 — https://ndismaps.nrel.colostate.edu/arcgis/rest/services/FishingAtlas/FishingAtlas_Data/MapServer/13?f=pjson |
| Geometry | `esriGeometryPolygon`; geometry field `SHAPE` |
| Fields | `OBJECTID` — `esriFieldTypeOID` — `OBJECTID`; `SHAPE` — `esriFieldTypeGeometry` — `SHAPE`; `SHAPE_Length` — `esriFieldTypeDouble` — `SHAPE_Length`; `SHAPE_Area` — `esriFieldTypeDouble` — `SHAPE_Area`; `LOC_ID` — `esriFieldTypeInteger` — `LOC_ID`; `PropNum` — `esriFieldTypeInteger` — `PropNum` |
| Coded-value domains | None |
| Water code | No `WATERCODE` field |

### Watercode Streams

| Property | Value |
|---|---|
| Layer / source | ID 15 — https://ndismaps.nrel.colostate.edu/arcgis/rest/services/FishingAtlas/FishingAtlas_Data/MapServer/15?f=pjson |
| Geometry | `esriGeometryPolyline`; geometry field `Shape` |
| Fields | `OBJECTID` — `esriFieldTypeOID` — `OBJECTID`; `WATERCODE` — `esriFieldTypeString` (5) — `WATERCODE`; `CATEGORY` — `esriFieldTypeString` (3) — `CATEGORY`; `OBSOLETE` — `esriFieldTypeSmallInteger` — `OBSOLETE`; `COMMENT` — `esriFieldTypeString` (1073741822) — `COMMENT`; `NOTES` — `esriFieldTypeString` (50) — `NOTES`; `ALT_CODE` — `esriFieldTypeString` (10) — `ALT_CODE`; `WC_CHECK` — `esriFieldTypeString` (5) — `WC_CHECK`; `Shape` — `esriFieldTypeGeometry` — `Shape`; `WC_INT` — `esriFieldTypeInteger` — `WC_INT`; `WATERNAME` — `esriFieldTypeString` (50) — `WATERNAME`; `Shape_Length` — `esriFieldTypeDouble` — `Shape_Length` |
| Coded-value domains | None |
| Water code | `WATERCODE`, string length 5; also `ALT_CODE`, `WC_CHECK`, and numeric `WC_INT` |

### Watercode Waterbodies

| Property | Value |
|---|---|
| Layer / source | ID 16 — https://ndismaps.nrel.colostate.edu/arcgis/rest/services/FishingAtlas/FishingAtlas_Data/MapServer/16?f=pjson |
| Geometry | `esriGeometryPolygon`; geometry field `Shape` |
| Fields | `OBJECTID` — `esriFieldTypeOID` — `OBJECTID`; `ComID` — `esriFieldTypeInteger` — `ComID`; `FDate` — `esriFieldTypeDate` — `FDate`; `Resolution` — `esriFieldTypeInteger` — `Resolution`; `GNIS_ID` — `esriFieldTypeString` (10) — `GNIS_ID`; `GNIS_Name` — `esriFieldTypeString` (65) — `GNIS_Name`; `Elevation` — `esriFieldTypeDouble` — `Elevation`; `ReachCode` — `esriFieldTypeString` (14) — `ReachCode`; `FType` — `esriFieldTypeInteger` — `FType`; `FCode` — `esriFieldTypeInteger` — `FCode`; `DOW_NAME` — `esriFieldTypeString` (50) — `DOW_NAME`; `WATERCODE` — `esriFieldTypeString` (10) — `WATERCODE`; `ALT_WATERCODE` — `esriFieldTypeString` (10) — `ALT_WATERCODE`; `NOTES` — `esriFieldTypeString` (50) — `NOTES`; `Shape` — `esriFieldTypeGeometry` — `Shape`; `CATEGORY` — `esriFieldTypeString` (3) — `Category`; `OBSOLETE` — `esriFieldTypeSmallInteger` — `Obsolete`; `WC_INT` — `esriFieldTypeInteger` — `WC_INT`; `Shape_Length` — `esriFieldTypeDouble` — `Shape_Length`; `Shape_Area` — `esriFieldTypeDouble` — `Shape_Area`; `VxCount` — `esriFieldTypeInteger` — `VxCount` |
| Water code | `WATERCODE`, string length 10; `ALT_WATERCODE`, string length 10; numeric `WC_INT` |
| Subtype field | `FType`; default subtype 390 |

Domains:

- `Resolution`, coded-value domain `WS1_Resolution`: `1 = Local`, `2 = High`, `3 = Medium`.
- `Elevation`, range domain `WS1_ElevationRange`: `-400` through `9000`.
- `FCode` is subtype-dependent:
  - `FType 361` (`Playa`): `36100 = Playa`.
  - `FType 378` (`Ice Mass`): `37800 = Ice Mass`.
  - `FType 466` (`SwampMarsh`): `46600 = Swamp/Marsh`; `46601 = Swamp/Marsh: Hydrographic Category: Intermittent`; `46602 = Swamp/Marsh: Hydrographic Category: Perennial`.
  - `FType 493` (`Estuary`): `49300 = Estuary`.
  - `FType 390` (`LakePond`): `39000 = Lake/Pond`; `39001 = Lake/Pond: Hydrographic Category = Intermittent`; `39006 = Lake/Pond: Hydrographic Category = Intermittent; Stage = Date of Photography`; `39005 = Lake/Pond: Hydrographic Category = Intermittent; Stage = High Water Elevation`; `39004 = Lake/Pond: Hydrographic Category = Perennial`; `39009 = Lake/Pond: Hydrographic Category = Perennial; Stage = Average Water Elevation`; `39011 = Lake/Pond: Hydrographic Category = Perennial; Stage = Date of Photography`; `39010 = Lake/Pond: Hydrographic Category = Perennial; Stage = Normal Pool`; `39012 = Lake/Pond: Hydrographic Category = Perennial; Stage = Spillway`.
  - `FType 436` (`Reservoir`): `43600 = Reservoir`; `43618 = Reservoir: Construction Material = Earthen`; `43619 = Reservoir: Construction Material = Nonearthen`; `43601 = Reservoir: Reservoir Type = Aquaculture`; `43609 = Reservoir: Reservoir Type = Cooling Pond`; `43603 = Reservoir: Reservoir Type = Decorative Pool`; `43606 = Reservoir: Reservoir Type = Disposal`; `43625 = Reservoir: Reservoir Type = Disposal; Construction Material = Earthen`; `43626 = Reservoir: Reservoir Type = Disposal; Construction Material = Nonearthen`; `43607 = Reservoir: Reservoir Type = Evaporator`; `43623 = Reservoir: Reservoir Type = Evaporator; Construction Material = Earthen`; `43610 = Reservoir: Reservoir Type = Filtration Pond`; `43611 = Reservoir: Reservoir Type = Settling Pond`; `43612 = Reservoir: Reservoir Type = Sewage Treatment Pond`; `43608 = Reservoir: Reservoir Type = Swimming Pool`; `43605 = Reservoir: Reservoir Type = Tailings Pond`; `43604 = Reservoir: Reservoir Type = Tailings Pond; Construction Material = Earthen`; `43624 = Reservoir: Reservoir Type = Treatment`; `43617 = Reservoir: Reservoir Type = Water Storage`; `43614 = Reservoir: Reservoir Type = Water Storage; Construction Material = Earthen; Hydrographic Category = Intermittent`; `43615 = Reservoir: Reservoir Type = Water Storage; Construction Material = Earthen; Hydrographic Category = Perennial`; `43613 = Reservoir: Reservoir Type = Water Storage; Construction Material = Nonearthen`; `43621 = Reservoir: Reservoir Type = Water Storage; Hydrographic Category = Perennial`.

### All Lakes

| Property | Value |
|---|---|
| Layer / source | ID 11 — https://ndismaps.nrel.colostate.edu/arcgis/rest/services/FishingAtlas/FishingAtlas_Data/MapServer/11?f=pjson |
| Geometry | `esriGeometryPolygon`; geometry field `Shape` |
| Fields | `OBJECTID` — `esriFieldTypeOID` — `OBJECTID`; `Shape` — `esriFieldTypeGeometry` — `Shape`; `Search_Name` — `esriFieldTypeString` (100) — `Search_Name`; `COUNTYNAME` — `esriFieldTypeString` (15) — `COUNTYNAME`; `Shape_Length` — `esriFieldTypeDouble` — `Shape_Length`; `Shape_Area` — `esriFieldTypeDouble` — `Shape_Area` |
| Coded-value domains | None |
| Water code | No `WATERCODE` field |

### All Streams

| Property | Value |
|---|---|
| Layer / source | ID 10 — https://ndismaps.nrel.colostate.edu/arcgis/rest/services/FishingAtlas/FishingAtlas_Data/MapServer/10?f=pjson |
| Geometry | `esriGeometryPolyline`; geometry field `Shape` |
| Fields | `OBJECTID_1` — `esriFieldTypeOID` — `OBJECTID_1`; `Shape` — `esriFieldTypeGeometry` — `Shape`; `Search_Nam` — `esriFieldTypeString` (100) — `Search_Nam`; `COUNTYNAME` — `esriFieldTypeString` (15) — `COUNTYNAME`; `Shape_Length` — `esriFieldTypeDouble` — `Shape_Length` |
| Coded-value domains | None |
| Water code | No `WATERCODE` field |

## Example records

All queries used `where=1=1`, `outFields=*`, `returnGeometry=false`, and `resultRecordCount=3`.

### Boat Ramp

[RETRIEVED] Query:

https://ndismaps.nrel.colostate.edu/arcgis/rest/services/FishingAtlas/FishingAtlas_Data/MapServer/3/query?where=1%3D1&outFields=%2A&returnGeometry=false&resultRecordCount=3&f=pjson

| Field | Record 1 | Record 2 | Record 3 |
|---|---:|---:|---:|
| `OBJECTID` | 1 | 2 | 3 |
| `Manager` | `CDOW` | `CDOW` | `CDOW` |
| `Property` | `Holbrook Reservoir SWA` | `Holbrook Reservoir SWA` | `Horse Creek Reservoir SWA` |
| `FeatureName` | null | null | null |
| `WaterLevelService` | `Low` | `High` | `High` |
| `Watercode` | null | null | null |
| `BoatInspection` | 0 | 0 | 0 |
| `InfoURL` | `http://wildlife.state.co.us/LandWater/StateWildlifeAreas/Pages/swa.aspx` | same | same |
| `Notes` | `Low water ramp` | `High water ramp` | `High water ramp` |
| `CollectionDate` | 1174953600000 | 1174953600000 | 1174953600000 |
| `CollectionMethod` | `Digitized` | `Digitized` | `Digitized` |
| `Water_Type` | null | null | null |
| `SHOW` | 1 | 1 | 1 |

[INFERRED] The three records demonstrate that the nominal join field is not reliably populated: all three `Watercode` values are null.

### Watercode Waterbodies

[RETRIEVED] Query:

https://ndismaps.nrel.colostate.edu/arcgis/rest/services/FishingAtlas/FishingAtlas_Data/MapServer/16/query?where=1%3D1&outFields=%2A&returnGeometry=false&resultRecordCount=3&f=pjson

| Field | Record 1 | Record 2 | Record 3 |
|---|---:|---:|---:|
| `OBJECTID` | 1 | 2 | 4 |
| `ComID` | 127981769 | 127981845 | 127981035 |
| `FDate` | 1098380872000 | 1098380899000 | 1098380996000 |
| `Resolution` | 2 | 2 | 2 |
| `GNIS_ID` | null | null | null |
| `GNIS_Name` | null | null | null |
| `Elevation` | 7574 | 5725 | 4763 |
| `ReachCode` | `11020002012911` | `11020002012976` | `11020002012307` |
| `FType` | 390 | 390 | 390 |
| `FCode` | 39004 | 39004 | 39009 |
| `DOW_NAME` | null | null | null |
| `WATERCODE` | null | null | null |
| `ALT_WATERCODE` | null | null | null |
| `NOTES` | null | null | null |
| `CATEGORY` | null | null | null |
| `OBSOLETE` | null | null | null |
| `WC_INT` | null | null | null |
| `Shape_Length` | 144.80066598752407 | 220.91444323616068 | 346.71116365854766 |
| `Shape_Area` | 1347.9836672195086 | 3181.1634609207317 | 7980.9221397243773 |
| `VxCount` | 12 | 11 | 12 |

[INFERRED] `ComID` and `ReachCode` appear to be National Hydrography Dataset identifiers. They are populated in these examples, while every CPW water-code field is null.

### Special Fishing Regulations (lake)

[RETRIEVED] Query:

https://ndismaps.nrel.colostate.edu/arcgis/rest/services/FishingAtlas/FishingAtlas_Data/MapServer/12/query?where=1%3D1&outFields=%2A&returnGeometry=false&resultRecordCount=3&f=pjson

| Field | Record 1 | Record 2 | Record 3 |
|---|---:|---:|---:|
| `OBJECTID` | 1 | 2 | 3 |
| `LOC_ID` | 2 | 4 | 5 |
| `WATERCODE` | `52301` | `79372` | `53683` |
| `Shape_Length` | 7690.3293054019141 | 32134.437647129314 | 2588.2263205052914 |
| `Shape_Area` | 659180.60805103346 | 31361265.610061221 | 170334.47675054855 |

## CPW ArcGIS Online services

[RETRIEVED] The organization endpoint lists a large number of public services. The following named services are facially relevant to fishing, boating, public access, state parks or State Wildlife Areas; opaque `service_<id>` services were not classified without opening each one.

Source: https://services5.arcgis.com/ttNGmDvKQA7oeDQ3/ArcGIS/rest/services?f=pjson

### Fishing and aquatic data

- `CPW_Quality_Waters`
- `CPWLakeNames`
- `FishingClinicMap_Districts`
- `Fishing_Closures`
- `Drought_Related_Fishing_Regulations`
- `CPWHPHAquaticData`
- `CPWSB181AquaticData`
- `CPWAdminData` — includes Gold Medal waters and aquatic management layers
- `CPW_SamplingData_2017`
- `CPWSpeciesData`

### Boating and aquatic nuisance species

- `Boatable_Waters`
- `PublicWID` — Watercraft Inspection Stations
- `WatercraftMovement`
- `SharedBoats_2020`
- `ANS_MasterList_OnePer_Prohibited_3`
- `CPW_ANS_Sampling_2018`
- `CPW_ANS_Sampling_2019`
- `CPW_PlanktonTow_26`

### Access, parks and wildlife properties

- `RiverAccessPoints`
- `CPWAdminData`
- `Axial_SWA_Parcels`
- `SP_Boundaries_20240216`
- `State_Park_Boundaries_Populated_2026`
- `State_Park_Roads_Populated_2026`
- `CPW_Facilities_Populated_2025`
- `COTREXTrailheads`
- `COTREXTrails`
- `COTREX_Trailheads`
- `COTREX_Spring26`
- `COTREX_Trails_Populated_2026`

[UNKNOWN] This is a name-based relevance list, not proof that every service is production-authoritative. The organization directory also contains drafts, tests, surveys and opaque service names.

### CPWAdminData item metadata

[RETRIEVED]

- Service item ID: `168fccb0583f42f1afe57de6c9ce846d`
- Owner: `rsaccoCPW`
- Access: `public`
- Modified: `1787840699000`
- Attribution / `accessInformation`: `Colorado Parks and Wildlife`
- Description: “This is an ArcGIS Feature Service generated by the Colorado Parks and Wildlife GIS Unit on August 27, 2026 for distributing Colorado state parks and wildlife GIS data for public distribution.”
- `licenseInfo`: a CPW ownership, interpretation, warranty, risk and indemnity notice; it does not contain an express copyright license or standard open-data license.
- Relevant layers include:
  - `CPW Gold Medal Streams`
  - `CPW Gold Medal Lakes`
  - `CPW Managed Properties (public access only)`
  - `CPW Aquatic Native Species Conservation Waters`
  - `CPW Aquatic Sportfish Management Waters`
  - `CPW Aquatic Cutthroat Trout Designated Crucial Habitat`
  - `CPW Aquatic Gold Medal Waters`

Item metadata: https://www.arcgis.com/sharing/rest/content/items/168fccb0583f42f1afe57de6c9ce846d?f=pjson

Service: https://services5.arcgis.com/ttNGmDvKQA7oeDQ3/ArcGIS/rest/services/CPWAdminData/FeatureServer?f=pjson

### PublicWID item metadata

[RETRIEVED]

- Service item ID: `a84b40079bac4e2d87644cf920fcb6ff`
- Title: `Public WID Stations`
- Owner: `robert.walters_CPW`
- Access: `public`
- Modified: `1788826199000`
- Attribution / `accessInformation`: empty
- `licenseInfo`: empty
- Description and snippet: empty
- Layer: `Watercraft Inspection Stations`

Item metadata: https://www.arcgis.com/sharing/rest/content/items/a84b40079bac4e2d87644cf920fcb6ff?f=pjson

Service: https://services5.arcgis.com/ttNGmDvKQA7oeDQ3/ArcGIS/rest/services/PublicWID/FeatureServer?f=pjson

[INFERRED] Public visibility and anonymous query capability permit viewing and technical retrieval. They do not, by themselves, grant permission to copy and redistribute the dataset.

## Terms, licence and attribution findings

### CPW Maps and GIS page

[RETRIEVED] CPW affirmatively presents GIS data for download and streaming:

> “These same data are also available as web services streaming from the ArcGIS Online servers.”

[RETRIEVED] CPW describes downstream analytical and product use:

> “This data allows outdoor enthusiasts, researchers, app developers and conservationists to analyze trends and make informed decisions and custom products.”

Source: https://cpw.state.co.us/maps-and-gis

[INFERRED] These statements support retrieval, analysis and creating derived products. They are not a complete license: the page does not identify a standard license, expressly grant copying/distribution rights, address public Git repositories, or specify attribution terms.

### Fishing Atlas service metadata

[RETRIEVED] Both compared NDIS MapServers have empty:

- `description`
- `serviceDescription`
- `copyrightText`
- `documentInfo.Author`
- `documentInfo.Comments`

Sources:

- https://ndismaps.nrel.colostate.edu/arcgis/rest/services/FishingAtlas/FishingAtlas_Data/MapServer?f=pjson
- https://ndismaps.nrel.colostate.edu/arcgis/rest/services/FishingAtlas2025/FishingInfo2025/MapServer?f=pjson

[INFERRED] A blank copyright or license field is not permission and should not be treated as a public-domain dedication.

### Fishing Atlas disclaimer

[RETRIEVED] The live application requires agreement to a use disclaimer. Decisive excerpts:

> “Information depicted is for reference purposes only and is compiled from the best available sources.”

> “Reasonable efforts have been made to ensure accuracy.”

> “The Colorado Parks and Wildlife is not responsible for damages that may arise from the use of this mapping application.”

Source: https://ndismaps.nrel.colostate.edu/fishingatlas

[RETRIEVED] The application says:

> “Download a Comma Delimited File.”

Source: same URL.

[INFERRED] The download feature supports end-user extraction from the application, but the disclaimer does not expressly authorize republication or bulk mirroring.

### Colorado Information Marketplace

[RETRIEVED] Socrata catalog entry `dr62-dnnu` reports:

- Name: `Fishing Atlas`
- Asset type: `href`
- License ID: `PUBLIC_DOMAIN`
- License name: `Public Domain`
- Attribution: `DNR - Colorado Parks and Wildlife`
- Attribution link: `https://ndismaps.nrel.colostate.edu/index.html?app=FishingAtlas`
- Description: `This mapping application is provided to fishermen as a virtual scouting tool.`
- Provenance: `official`
- The entry contains no data columns and points to the external NDIS application.

Catalog API:

https://api.us.socrata.com/api/catalog/v1?q=Fishing%20Atlas&search_context=data.colorado.gov

View metadata:

https://data.colorado.gov/api/views/dr62-dnnu.json

[INFERRED] “Public Domain” is the strongest affirmative reuse indicator found. However, the Socrata object is an `href`, not a hosted copy of the ArcGIS records. It is unclear whether the license was intended to cover:

1. only the catalog/link record;
2. the Fishing Atlas application as a whole; or
3. every underlying CPW/CSU/third-party layer exposed by the application.

Conservative treatment therefore cannot extend the designation automatically to every REST layer.

### Data.colorado.gov terms

[RETRIEVED] The terms require application disclaimers:

> “Applications using data supplied by this site must include the following disclaimers on their sites:”

[RETRIEVED] Required source statement:

> “The data made available here has been modified for use from its original source, which is the State of Colorado.”

[RETRIEVED] The State reserves termination rights over feeds:

> “The State of Colorado reserves the right to modify and/or discontinue providing any or all of the data feeds at any time”

Source: https://data.colorado.gov/terms

[INFERRED] Those terms clearly apply to data supplied through data.colorado.gov. Whether they govern records fetched directly from NDIS is uncertain because the Fishing Atlas catalog object is only an external link.

### CPWAdminData

[RETRIEVED] Its item description explicitly says the service was generated “for distributing Colorado state parks and wildlife GIS data for public distribution.”

[RETRIEVED] Attribution is `Colorado Parks and Wildlife`.

[RETRIEVED] Its `licenseInfo` begins:

> “This map is a product and property of the Colorado Parks and Wildlife”

and states:

> “Care should be taken in interpreting these data.”

Source: https://www.arcgis.com/sharing/rest/content/items/168fccb0583f42f1afe57de6c9ce846d?f=pjson

[INFERRED] “Public distribution” supports redistribution of CPWAdminData. Nevertheless, the item’s license text is a disclaimer, not a standard license, and does not expressly grant modification, sublicensing or creation of derivative databases. Written confirmation remains advisable for repository persistence.

### PublicWID

[RETRIEVED] The ArcGIS item is public, but `licenseInfo`, `accessInformation`, description and snippet are all blank.

Source: https://www.arcgis.com/sharing/rest/content/items/a84b40079bac4e2d87644cf920fcb6ff?f=pjson

[INFERRED] This establishes public access only. It does not establish a right to redistribute Watercraft Inspection Station records.

### CSU / NDIS terms

[RETRIEVED] No NDIS-specific terms or license page was found at `https://ndismaps.nrel.colostate.edu/terms`; it returned no content. The live Fishing Atlas exposes a disclaimer but no redistribution license.

[RETRIEVED] CSU’s general disclaimer says:

> “Colorado State University does not warrant that the use of this information is free of any claims of copyright infringement.”

Source: https://www.colostate.edu/disclaimer/

[INFERRED] CSU’s disclaimer does not grant reuse rights. It reinforces the need to identify the actual owner and license of each underlying layer.

[UNKNOWN] A separate current NDIS/CSU license governing REST-service copying and redistribution was not located.

### State of Colorado general website terms / copyright

[UNKNOWN] No general State of Colorado terms or copyright page applicable to `cpw.state.co.us` or the NDIS REST services was located at the expected Colorado.gov terms URLs. The pages checked returned 404 responses. Agency- or application-specific terms should therefore control rather than assuming a statewide open license.

## Is fetch / transform / persist in a public repository / redistribute permitted?

| Activity | Assessment | Evidence and conditions |
|---|---|---|
| Fetch from the public REST endpoints | **Clearly permitted** for ordinary public querying and download | The services expose anonymous `Query`/`Data` capabilities; CPW says the data are available through streaming web services; the Fishing Atlas offers CSV download. This does not imply permission to overload, scrape around controls, or rely on permanent availability. |
| Transform for analysis or a custom map | **Permitted with conditions** | CPW expressly identifies app developers and “custom products”; the Colorado catalog labels the Fishing Atlas `Public Domain`. Retain provenance, do not imply official status, preserve warnings, and verify regulations against official publications. Third-party layers require separate review. |
| Persist a complete or substantial transformed copy in a public Git repository | **Unclear** | The NDIS services have blank copyright/license fields. The Socrata object is only an `href`, making the scope of its `Public Domain` label uncertain. `PublicWID` has a blank license. CPWAdminData says “public distribution” but supplies only a disclaimer, not an explicit derivative-database license. |
| Redistribute records with the static site | **Unclear** for NDIS Fishing Atlas and PublicWID; **permitted with conditions** is defensible for CPWAdminData | CPWAdminData expressly states that it is for public distribution and names CPW as attribution. For NDIS and PublicWID, no explicit redistribution grant was found. Obtain written CPW confirmation before shipping a mirrored data bundle. |
| Redistribute third-party layers seen in the Fishing Atlas | **Unclear; potentially prohibited under source-specific terms** | The application includes Esri, USFS, BLM, COMaP and other sources. CPW cannot necessarily license those sources onward. Review each source separately. |

### Minimum conditions if CPW confirms reuse

1. Attribute: `Colorado Parks and Wildlife`.
2. Identify the source service URL and retrieval date.
3. State that Ohvernight transformed the data.
4. Include the State disclaimer required by data.colorado.gov if CPW confirms those terms apply.
5. State that data may change and are for reference only.
6. Link users to current CPW regulations rather than presenting mapped regulations as legally definitive.
7. Do not apply Ohvernight’s code license to the data unless CPW confirms that licensing.
8. Keep third-party datasets in separately attributed files with their own licenses.

## What a water-code join would and would not establish

[RETRIEVED] Water-code-like fields occur inconsistently:

- Fishing Information Point: `WATERCODE`, length 10.
- Boat Ramp: `Watercode`, length 8.
- Special Regulations lake: `WATERCODE`, length 10.
- Watercode Streams: `WATERCODE`, length 5, plus `ALT_CODE`, `WC_CHECK`, and `WC_INT`.
- Watercode Waterbodies: `WATERCODE` and `ALT_WATERCODE`, each length 10, plus `WC_INT`.
- Gold Medal, All Lakes, All Streams, stream regulations and property regulations lack a water-code field.

[RETRIEVED] The three sampled lake-regulation records have populated five-digit codes: `52301`, `79372`, and `53683`. The three sampled Boat Ramp and Watercode Waterbodies records have null water codes.

[INFERRED] A successful exact water-code match would establish that CPW assigned the same stored code to the records in those particular service versions. It may support a deterministic thematic join.

It would not establish:

- that the code is globally unique;
- that it is permanent across annual service revisions;
- that leading zeros may safely be removed;
- that length differences are harmless;
- that `WATERCODE`, `ALT_WATERCODE`, `WC_INT`, NHD `ComID`, and `ReachCode` are interchangeable;
- that every ramp or waterbody has a code;
- that one code corresponds to exactly one polygon or stream segment;
- that the geometries are coincident or survey-grade;
- that a joined regulation is currently legally effective;
- that the joined records share a license;
- that a match authorizes redistribution.

[INFERRED] Treat water codes as versioned CPW business identifiers, not proven immutable primary keys. Preserve them as strings, including leading zeros. Store the source service, layer ID, retrieval timestamp and original object ID with every joined record. Validate uniqueness, null rates, one-to-many relationships and cross-version changes before relying on the join.

## Contact for a written answer

[RETRIEVED] The Fishing Atlas itself gives this technical/contact address:

- `ndisadmin@nrel.colostate.edu`
- Wording: “Please send your questions, comments, or problems with the Colorado FishingAtlas to ndisadmin@nrel.colostate.edu.”
- Source: https://ndismaps.nrel.colostate.edu/fishingatlas

[RETRIEVED] CPW’s official contact form currently directs questions to:

- `DNR_wildlife.cpwinfo@state.co.us`
- Source: https://cpw.state.co.us/form/contact

[RETRIEVED] CPW headquarters:

- 303-297-1192
- Source: https://cpw.state.co.us/contact-us

[UNKNOWN] A named CPW GIS licensing officer or dedicated public CPW GIS email was not found. `ndisadmin@nrel.colostate.edu` is the most specific Fishing Atlas technical contact, but it is a CSU/NREL address rather than a CPW legal/licensing address.

Recommended written request: email both `DNR_wildlife.cpwinfo@state.co.us` and `ndisadmin@nrel.colostate.edu`, asking CPW GIS/Data Stewardship to answer or route the request. Identify every service and layer, and ask for an explicit written grant covering automated fetch, transformation, public Git storage and redistribution.

## Unknowns

- [UNKNOWN] Whether the Socrata `Public Domain` designation covers the underlying REST features or only the external-link catalog record.
- [UNKNOWN] Whether NDIS has unpublished, embedded or institutional terms governing bulk extraction.
- [UNKNOWN] Whether CPW owns every attribute and geometry in the legacy Fishing Atlas layers.
- [UNKNOWN] Whether any Fishing Atlas fields incorporate third-party protected material.
- [UNKNOWN] Whether public-repository persistence is considered “public distribution” under the CPWAdminData description.
- [UNKNOWN] Whether CPW requires a particular attribution placement or exact disclaimer for direct ArcGIS/NDIS use.
- [UNKNOWN] Whether CPW permits relicensing the data under an open-source/content license. Do not assume it does.
- [UNKNOWN] The intended stability or lifecycle of the legacy `FishingAtlas_Data` endpoint.
- [UNKNOWN] A published data dictionary defining `WATERCODE`, `LOC_ID`, `UNI_ID`, `WC_INT`, `CATEGORY`, `OBSOLETE` and alternate-code semantics.
- [UNKNOWN] Whether water codes are unique, immutable, or intentionally shared across related water features.
- [UNKNOWN] Whether the mapped special-regulation records are synchronized with the legally controlling regulations on every update.
- [UNKNOWN] The licence for PublicWID; its licence and attribution fields are blank.

## Recommendation

[INFERRED] Do not commit a complete mirror of the NDIS Fishing Atlas or PublicWID data to the public Ohvernight repository yet.

Proceed in two tracks:

1. For immediate development, query the public services during a non-distributed build or maintain a private/local research cache. Keep raw provenance and do not represent the output as authoritative regulations.
2. Request written CPW permission that explicitly covers:
   - automated and recurring REST fetches;
   - transformation and joins;
   - storage of raw and derived records in a public Git repository;
   - redistribution with an open-source static site;
   - commercial and non-commercial downstream reuse;
   - required attribution and disclaimer text;
   - whether the Socrata `Public Domain` designation covers the REST layers;
   - whether `WATERCODE` is intended as a durable join key.

For data that can be sourced from `CPWAdminData`, its “public distribution” statement makes it the preferable CPW source over legacy NDIS layers, subject to attribution and written clarification about derivative/public-repository use. For PublicWID and legacy Fishing Atlas records, a blank license is insufficient.
