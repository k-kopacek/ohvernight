# Forest trail pilot

The website loads `v2/trails.geojson` independently of the camping research bundle. All map layers default on; dates and vehicle selections do not hide trail geometry. The current pilot contains 123 clipped USFS trail segments inside the existing Aspen study boundary, not 123 distinct complete trails or statewide coverage.

## Refresh

From the v2 folder, using Python with `pipeline/requirements.txt` installed:

```sh
python3 pipeline/scripts/fetch_trails.py
```

The command validates source fields and complete object-ID sets, clips to `pipeline/config/aoi.geojson`, then replaces `trails.geojson` atomically. Failed or empty retrievals preserve the previous snapshot. It is a separate refresh command, not yet scheduled or included in `run_pipeline.py`. Upload the refreshed `trails.geojson` with the website. The UI shows retrieval dates; these are not field-verification dates. No credentials are required.

## Source decision — checked September 25, 2026

- Selected: USDA Forest Service National Forest System Trails, layer 0 at https://apps.fs.usda.gov/arcx/rest/services/EDW/EDW_TrailNFSPublishWithDataStatus_01/MapServer/0 . Its metadata describes public trail geometry and varying attribute completeness by forest.
- Metadata: https://data.fs.usda.gov/geodata/edw/edw_resources/meta/S_USA.TrailNFS_Publish.xml . Access constraints are listed as None; use constraints disclaim accuracy, completeness, warranties and endorsement. Attribute retrieval does not prove current access.
- COTREX app terms https://trails.colorado.gov/terms restrict copying/distribution without separate written permission. The public CPWAdminData COTREX Trails layer 15 and Colorado State Basemap layer 40 both describe a February 5, 2019 data update, despite recent service publication dates. Do not treat a refreshed service date as refreshed trail content. No COTREX data was copied into this pilot. Obtain current licensed bulk-data terms from CPW before pursuing that integration.

## Activity model

Stable keys: hiking, horseback_riding, mountain_biking, motorcycling, atv, four_wheel_drive, snowshoeing, cross_country_skiing, snowmobiling.

Each stores the original USFS `managed`, `accpt`, `disc`, `restricted` strings. These retain published date ranges; they are not Boolean permissions. Missing values remain null/unknown. The interface labels each source field separately and does not resolve contradictory records or evaluate dates. E-bike permissions must not be inferred from bicycle records. Add e-bike classes and water activities when corresponding source integration is implemented.

Geometry is clipped; no distance, full-route continuity, navigation, current closure check or campsite access connection is inferred. Next work: activity-specific discovery and evidence-backed nearby camping associations, followed by geographic expansion.

## Trail layer fields as published on 2026-10-09

Fetched once from the USFS Forest Service EDW trails MapServer layer 0 with the layer-description `?f=json` request using system curl. All 39 required names are present case-insensitively. The service publishes distinct `_ACCPT` and `_DISC` fields as well as combined `_ACCPT_DISC` fields; the separate values were not replaced by the combined fields.

| Name | Alias | Type |
|---|---|---|
| `objectid` | OBJECTID | `esriFieldTypeOID` |
| `trail_name` | TRAIL_NAME | `esriFieldTypeString` |
| `trail_type` | TRAIL_TYPE | `esriFieldTypeString` |
| `trail_cn` | TRAIL_CN | `esriFieldTypeString` |
| `bmp` | BMP | `esriFieldTypeDouble` |
| `emp` | EMP | `esriFieldTypeDouble` |
| `segment_length` | SEGMENT_LENGTH | `esriFieldTypeDouble` |
| `admin_org` | ADMIN_ORG | `esriFieldTypeString` |
| `managing_org` | MANAGING_ORG | `esriFieldTypeString` |
| `security_id` | SECURITY_ID | `esriFieldTypeString` |
| `attributesubset` | ATTRIBUTESUBSET | `esriFieldTypeString` |
| `national_trail_designation` | NATIONAL_TRAIL_DESIGNATION | `esriFieldTypeInteger` |
| `trail_class` | TRAIL_CLASS | `esriFieldTypeString` |
| `accessibility_status` | ACCESSIBILITY_STATUS | `esriFieldTypeString` |
| `trail_surface` | TRAIL_SURFACE | `esriFieldTypeString` |
| `surface_firmness` | SURFACE_FIRMNESS | `esriFieldTypeString` |
| `typical_trail_grade` | TYPICAL_TRAIL_GRADE | `esriFieldTypeString` |
| `typical_tread_width` | TYPICAL_TREAD_WIDTH | `esriFieldTypeString` |
| `minimum_trail_width` | MINIMUM_TRAIL_WIDTH | `esriFieldTypeString` |
| `typical_tread_cross_slope` | TYPICAL_TREAD_CROSS_SLOPE | `esriFieldTypeString` |
| `special_mgmt_area` | SPECIAL_MGMT_AREA | `esriFieldTypeString` |
| `terra_base_symbology` | TERRA_BASE_SYMBOLOGY | `esriFieldTypeString` |
| `mvum_symbol` | MVUM_SYMBOL | `esriFieldTypeInteger` |
| `terra_motorized` | TERRA_MOTORIZED | `esriFieldTypeString` |
| `snow_motorized` | SNOW_MOTORIZED | `esriFieldTypeString` |
| `water_motorized` | WATER_MOTORIZED | `esriFieldTypeString` |
| `allowed_terra_use` | ALLOWED_TERRA_USE | `esriFieldTypeString` |
| `allowed_snow_use` | ALLOWED_SNOW_USE | `esriFieldTypeString` |
| `hiker_pedestrian_managed` | HIKER_PEDESTRIAN_MANAGED | `esriFieldTypeString` |
| `hiker_pedestrian_accpt` | HIKER_PEDESTRIAN_ACCPT | `esriFieldTypeString` |
| `hiker_pedestrian_disc` | HIKER_PEDESTRIAN_DISC | `esriFieldTypeString` |
| `hiker_pedestrian_accpt_disc` | HIKER_PEDESTRIAN_ACCPT_DISC | `esriFieldTypeString` |
| `hiker_pedestrian_restricted` | HIKER_PEDESTRIAN_RESTRICTED | `esriFieldTypeString` |
| `pack_saddle_managed` | PACK_SADDLE_MANAGED | `esriFieldTypeString` |
| `pack_saddle_accpt` | PACK_SADDLE_ACCPT | `esriFieldTypeString` |
| `pack_saddle_disc` | PACK_SADDLE_DISC | `esriFieldTypeString` |
| `pack_saddle_accpt_disc` | PACK_SADDLE_ACCPT_DISC | `esriFieldTypeString` |
| `pack_saddle_restricted` | PACK_SADDLE_RESTRICTED | `esriFieldTypeString` |
| `bicycle_managed` | BICYCLE_MANAGED | `esriFieldTypeString` |
| `bicycle_accpt` | BICYCLE_ACCPT | `esriFieldTypeString` |
| `bicycle_disc` | BICYCLE_DISC | `esriFieldTypeString` |
| `bicycle_accpt_disc` | BICYCLE_ACCPT_DISC | `esriFieldTypeString` |
| `bicycle_restricted` | BICYCLE_RESTRICTED | `esriFieldTypeString` |
| `motorcycle_managed` | MOTORCYCLE_MANAGED | `esriFieldTypeString` |
| `motorcycle_accpt` | MOTORCYCLE_ACCPT | `esriFieldTypeString` |
| `motorcycle_disc` | MOTORCYCLE_DISC | `esriFieldTypeString` |
| `motorcycle_accpt_disc` | MOTORCYCLE_ACCPT_DISC | `esriFieldTypeString` |
| `motorcycle_restricted` | MOTORCYCLE_RESTRICTED | `esriFieldTypeString` |
| `atv_managed` | ATV_MANAGED | `esriFieldTypeString` |
| `atv_accpt` | ATV_ACCPT | `esriFieldTypeString` |
| `atv_disc` | ATV_DISC | `esriFieldTypeString` |
| `atv_accpt_disc` | ATV_ACCPT_DISC | `esriFieldTypeString` |
| `atv_restricted` | ATV_RESTRICTED | `esriFieldTypeString` |
| `fourwd_managed` | FOURWD_MANAGED | `esriFieldTypeString` |
| `fourwd_accpt` | FOURWD_ACCPT | `esriFieldTypeString` |
| `fourwd_disc` | FOURWD_DISC | `esriFieldTypeString` |
| `fourwd_accpt_disc` | FOURWD_ACCPT_DISC | `esriFieldTypeString` |
| `fourwd_restricted` | FOURWD_RESTRICTED | `esriFieldTypeString` |
| `trail_no` | TRAIL_NO | `esriFieldTypeString` |
| `snowcoach_snowcat_managed` | SNOWCOACH_SNOWCAT_MANAGED | `esriFieldTypeString` |
| `snowcoach_snowcat_accpt` | SNOWCOACH_SNOWCAT_ACCPT | `esriFieldTypeString` |
| `snowcoach_snowcat_disc` | SNOWCOACH_SNOWCAT_DISC | `esriFieldTypeString` |
| `snowcoach_snowcat_accpt_disc` | SNOWCOACH_SNOWCAT_ACCPT_DISC | `esriFieldTypeString` |
| `snowcoach_snowcat_restricted` | SNOWCOACH_SNOWCAT_RESTRICTED | `esriFieldTypeString` |
| `snowmobile_managed` | SNOWMOBILE_MANAGED | `esriFieldTypeString` |
| `snowmobile_accpt` | SNOWMOBILE_ACCPT | `esriFieldTypeString` |
| `snowmobile_disc` | SNOWMOBILE_DISC | `esriFieldTypeString` |
| `snowmobile_accpt_disc` | SNOWMOBILE_ACCPT_DISC | `esriFieldTypeString` |
| `snowmobile_restricted` | SNOWMOBILE_RESTRICTED | `esriFieldTypeString` |
| `snowshoe_managed` | SNOWSHOE_MANAGED | `esriFieldTypeString` |
| `snowshoe_accpt` | SNOWSHOE_ACCPT | `esriFieldTypeString` |
| `snowshoe_disc` | SNOWSHOE_DISC | `esriFieldTypeString` |
| `snowshoe_accpt_disc` | SNOWSHOE_ACCPT_DISC | `esriFieldTypeString` |
| `snowshoe_restricted` | SNOWSHOE_RESTRICTED | `esriFieldTypeString` |
| `xcountry_ski_managed` | XCOUNTRY_SKI_MANAGED | `esriFieldTypeString` |
| `xcountry_ski_accpt` | XCOUNTRY_SKI_ACCPT | `esriFieldTypeString` |
| `xcountry_ski_disc` | XCOUNTRY_SKI_DISC | `esriFieldTypeString` |
| `xcountry_ski_accpt_disc` | XCOUNTRY_SKI_ACCPT_DISC | `esriFieldTypeString` |
| `xcountry_ski_restricted` | XCOUNTRY_SKI_RESTRICTED | `esriFieldTypeString` |
| `motor_watercraft_managed` | MOTOR_WATERCRAFT_MANAGED | `esriFieldTypeString` |
| `motor_watercraft_accpt` | MOTOR_WATERCRAFT_ACCPT | `esriFieldTypeString` |
| `motor_watercraft_disc` | MOTOR_WATERCRAFT_DISC | `esriFieldTypeString` |
| `motor_watercraft_accpt_disc` | MOTOR_WATERCRAFT_ACCPT_DISC | `esriFieldTypeString` |
| `motor_watercraft_restricted` | MOTOR_WATERCRAFT_RESTRICTED | `esriFieldTypeString` |
| `nonmotor_watercraft_managed` | NONMOTOR_WATERCRAFT_MANAGED | `esriFieldTypeString` |
| `nonmotor_watercraft_accpt` | NONMOTOR_WATERCRAFT_ACCPT | `esriFieldTypeString` |
| `nonmotor_watercraft_disc` | NONMOTOR_WATERCRAFT_DISC | `esriFieldTypeString` |
| `nonmotor_watercraft_accpt_disc` | NONMOTOR_WATERCRAFT_ACCPT_DISC | `esriFieldTypeString` |
| `nonmotor_watercraft_restricted` | NONMOTOR_WATERCRAFT_RESTRICTED | `esriFieldTypeString` |
| `gis_miles` | GIS_MILES | `esriFieldTypeDouble` |
| `e_bike_class1_managed` | E_BIKE_CLASS1_MANAGED | `esriFieldTypeString` |
| `e_bike_class1_accpt` | E_BIKE_CLASS1_ACCPT | `esriFieldTypeString` |
| `e_bike_class1_disc` | E_BIKE_CLASS1_DISC | `esriFieldTypeString` |
| `e_bike_class1_restricted` | E_BIKE_CLASS1_RESTRICTED | `esriFieldTypeString` |
| `e_bike_class2_managed` | E_BIKE_CLASS2_MANAGED | `esriFieldTypeString` |
| `e_bike_class2_accpt` | E_BIKE_CLASS2_ACCPT | `esriFieldTypeString` |
| `e_bike_class2_disc` | E_BIKE_CLASS2_DISC | `esriFieldTypeString` |
| `e_bike_class2_restricted` | E_BIKE_CLASS2_RESTRICTED | `esriFieldTypeString` |
| `e_bike_class3_managed` | E_BIKE_CLASS3_MANAGED | `esriFieldTypeString` |
| `e_bike_class3_accpt` | E_BIKE_CLASS3_ACCPT | `esriFieldTypeString` |
| `e_bike_class3_disc` | E_BIKE_CLASS3_DISC | `esriFieldTypeString` |
| `e_bike_class3_restricted` | E_BIKE_CLASS3_RESTRICTED | `esriFieldTypeString` |
| `globalid` | globalid | `esriFieldTypeGlobalID` |
| `shape` | SHAPE | `esriFieldTypeGeometry` |
| `st_length(shape)` | st_length(shape) | `esriFieldTypeDouble` |
