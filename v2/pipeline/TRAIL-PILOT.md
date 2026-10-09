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

UNVERIFIED AGAINST LIVE LAYER: the single layer-description request failed TLS certificate verification before returning data. The table below records the 39 locally required field names; live aliases and types were not captured and must not be inferred.

| Name | Alias | Type |
|---|---|---|
| `objectid` | Not verified | Not verified |
| `trail_name` | Not verified | Not verified |
| `trail_no` | Not verified | Not verified |
| `hiker_pedestrian_managed` | Not verified | Not verified |
| `hiker_pedestrian_accpt` | Not verified | Not verified |
| `hiker_pedestrian_disc` | Not verified | Not verified |
| `hiker_pedestrian_restricted` | Not verified | Not verified |
| `pack_saddle_managed` | Not verified | Not verified |
| `pack_saddle_accpt` | Not verified | Not verified |
| `pack_saddle_disc` | Not verified | Not verified |
| `pack_saddle_restricted` | Not verified | Not verified |
| `bicycle_managed` | Not verified | Not verified |
| `bicycle_accpt` | Not verified | Not verified |
| `bicycle_disc` | Not verified | Not verified |
| `bicycle_restricted` | Not verified | Not verified |
| `motorcycle_managed` | Not verified | Not verified |
| `motorcycle_accpt` | Not verified | Not verified |
| `motorcycle_disc` | Not verified | Not verified |
| `motorcycle_restricted` | Not verified | Not verified |
| `atv_managed` | Not verified | Not verified |
| `atv_accpt` | Not verified | Not verified |
| `atv_disc` | Not verified | Not verified |
| `atv_restricted` | Not verified | Not verified |
| `fourwd_managed` | Not verified | Not verified |
| `fourwd_accpt` | Not verified | Not verified |
| `fourwd_disc` | Not verified | Not verified |
| `fourwd_restricted` | Not verified | Not verified |
| `snowshoe_managed` | Not verified | Not verified |
| `snowshoe_accpt` | Not verified | Not verified |
| `snowshoe_disc` | Not verified | Not verified |
| `snowshoe_restricted` | Not verified | Not verified |
| `xcountry_ski_managed` | Not verified | Not verified |
| `xcountry_ski_accpt` | Not verified | Not verified |
| `xcountry_ski_disc` | Not verified | Not verified |
| `xcountry_ski_restricted` | Not verified | Not verified |
| `snowmobile_managed` | Not verified | Not verified |
| `snowmobile_accpt` | Not verified | Not verified |
| `snowmobile_disc` | Not verified | Not verified |
| `snowmobile_restricted` | Not verified | Not verified |
