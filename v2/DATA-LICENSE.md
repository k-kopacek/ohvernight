# Map data

## USFS trail pilot

`trails.geojson` contains clipped USDA Forest Service National Forest System Trails. Source: https://apps.fs.usda.gov/arcx/rest/services/EDW/EDW_TrailNFSPublishWithDataStatus_01/MapServer/0 . Metadata and usage constraints: https://data.fs.usda.gov/geodata/edw/edw_resources/meta/S_USA.TrailNFS_Publish.xml . The Forest Service disclaims accuracy, completeness, adequacy, warranties and endorsement. Retrieval is not field verification. Source attribution and retrieval time accompany each feature. No COTREX content is included in this pilot.

© OpenStreetMap contributors. The OpenStreetMap-derived map extract is published at the repository root as `../map-data.json`; location coordinates identified as OpenStreetMap in `overnight-options.json` are made available under the Open Database License 1.0:
https://opendatacommons.org/licenses/odbl/1-0/

Attribution and contributor information: https://www.openstreetmap.org/copyright

Both JSON files contain the complete data used by this site. Road way IDs, geographic feature source URLs, and source metadata are retained. Initial map data was collected September 19, 2026; additional road extracts were collected September 22, 2026. Roads are a partial local extract. Inventory notes are short factual paraphrases linked to Recreation.gov, the Forest Service, or the lodging operator, reviewed September 24, 2026. Agency vehicle designations include their retrieval date and source. These records do not establish current availability, overnight permission, or physical road conditions.


## Interactive basemap (satellite edition)

USGS The National Map imagery and topo tiles are requested directly in the browser from `basemap.nationalmap.gov`. Source services: https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer and https://basemap.nationalmap.gov/arcgis/rest/services/USGSTopo/MapServer. USGS attribution stays visible on the map. Imagery includes aerial photography and is not a current-condition feed.

Leaflet 1.9.4 is bundled under the BSD 2-Clause license; see vendor/leaflet-LICENSE.txt. OpenStreetMap-derived destination and inventory coordinates retain their linked provenance and ODbL attribution. The previous D3 map renderer is no longer used.


## Douglas County snapshot (2026-09-27)

The independent county snapshot includes US Census TIGERweb boundary geometry, USFS trails/MVUM road geometry/recreation-site inventory, BLM limited-scale surface-management context and named USGS NHD water features. Per-feature evidence retains the service URL and fetch date. Broad management geometry is not cadastral/parcel surveying. Recreation.gov Rampart is linked as an area reference; no campsite geometry or commercial third-party trail inventory was copied. Basemap attribution remains visible (Esri imagery and OpenStreetMap streets).
