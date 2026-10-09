DRAFT - UNREVIEWED

# M6A — COTREX and USFS trail data: terms, services, schema, and identity

> Hermes report (GPT-5.6 sol), 2026-10-07, stored as returned. HERMES-SOURCED: web research only, no repository access. Nothing here is verified by the coordinator unless another document says so, and nothing is decided.

Accessed 2026-10-07. Research only; no contact was made.

## COTREX terms

### Published data

- **PRIMARY SOURCE — Current authoritative service.** CPW publishes COTREX trails as layer 15, `COTREX Trails`, in the hosted `CPWAdminData` feature service:
  - Service: https://services5.arcgis.com/ttNGmDvKQA7oeDQ3/arcgis/rest/services/CPWAdminData/FeatureServer?f=pjson
  - Layer: https://services5.arcgis.com/ttNGmDvKQA7oeDQ3/arcgis/rest/services/CPWAdminData/FeatureServer/15?f=pjson
  - ArcGIS Online item: https://www.arcgis.com/sharing/rest/content/items/168fccb0583f42f1afe57de6c9ce846d?f=pjson

- **PRIMARY SOURCE — Distinct CPW layers.** `CPWAdminData` contains both layer 2, `CPW Trail Segments`, and layer 15, `COTREX Trails`. They are different datasets; layer 2 is CPW-managed-property trail inventory, while layer 15 is the statewide COTREX compilation. https://services5.arcgis.com/ttNGmDvKQA7oeDQ3/arcgis/rest/services/CPWAdminData/FeatureServer?f=pjson

- **PRIMARY SOURCE — Downloads.** CPW publishes a downloadable ZIP shapefile item named `CPW Trails Shapefile Download`, containing CPW designated trails plus COTREX trails and trailheads. https://geodata-cpw.hub.arcgis.com/datasets/cae8ed959b8a4ed48680df62b31eec60 and https://www.arcgis.com/sharing/rest/content/items/cae8ed959b8a4ed48680df62b31eec60?f=pjson

- **PRIMARY SOURCE — Service exports.** The feature service advertises CSV, shapefile, SQLite, GeoPackage, file geodatabase, feature collection, GeoJSON, KML, and Excel exports; layer 15 additionally advertises Parquet. This establishes technical availability, not permission to redistribute. https://services5.arcgis.com/ttNGmDvKQA7oeDQ3/arcgis/rest/services/CPWAdminData/FeatureServer?f=pjson and https://services5.arcgis.com/ttNGmDvKQA7oeDQ3/arcgis/rest/services/CPWAdminData/FeatureServer/15?f=pjson

### License, attribution, and redistribution

- **PRIMARY SOURCE — Restriction first.** The COTREX application terms prohibit users from distributing application content without a separate agreement. Decisive wording: “Use, repost, copy, distribute or publish any Content unless you have been given permission”. They also prohibit using geographic-location data to create or augment another dataset. https://trails.colorado.gov/terms

- **PRIMARY SOURCE — Scope of application terms.** “Content” expressly includes maps, data, and geographic locations uploaded, downloaded, or displayed in COTREX. https://trails.colorado.gov/terms

- **PRIMARY SOURCE — ArcGIS item license.** The CPW ArcGIS item’s `licenseInfo` is an “as is,” liability, interpretation, and indemnification disclaimer. It does not contain an affirmative redistribution grant or a standard open-data license. Its `accessInformation` is `Colorado Parks and Wildlife`. https://www.arcgis.com/sharing/rest/content/items/168fccb0583f42f1afe57de6c9ce846d?f=pjson

- **PRIMARY SOURCE — Download item license.** The shapefile item also has a custom disclaimer rather than an affirmative reuse license. The item is publicly visible and downloadable, but public access is not permission to republish. https://www.arcgis.com/sharing/rest/content/items/cae8ed959b8a4ed48680df62b31eec60?f=pjson

- **PRIMARY SOURCE — COTREX map attribution.** The COTREX About page displays `© COTREX Contributors` for trails and trailheads, `© Natural Atlas` for cartography/recreation POIs/base-map data, and OpenStreetMap attribution for roads and minor cartographic features. It does not state that this displayed attribution alone authorizes third-party redistribution. https://trails.colorado.gov/about

- **UNKNOWN — Redistribution in Ohvernight.** No retrieved CPW source affirmatively permits republishing the COTREX trail geometry or attributes in a separate public static site. The COTREX application terms point the other way and require a “separate written agreement.” Whether the separately published ArcGIS/open-data copy is intentionally governed by different reuse rights is not stated. Redistribution should therefore be treated as **UNKNOWN / not cleared**, not allowed. https://trails.colorado.gov/terms and https://www.arcgis.com/sharing/rest/content/items/168fccb0583f42f1afe57de6c9ce846d?f=pjson

### Disclaimer and update timing

- **PRIMARY SOURCE — Safety/access disclaimer.** COTREX says depiction of a trail does not imply it is passable, maintained, safe, or “open for general public use.” https://trails.colorado.gov/terms

- **PRIMARY SOURCE — Source responsibility.** CPW says COTREX trails come from USFS, BLM, local parks and recreation departments, and local governments, and that responsibility for accuracy rests with the source. https://www.arcgis.com/sharing/rest/content/items/cae8ed959b8a4ed48680df62b31eec60?f=pjson

- **PRIMARY SOURCE — Current publication date.** The service and item say the hosted service was generated on 2026-08-27; layer `editingInfo` also reports data and schema edits on that date. https://services5.arcgis.com/ttNGmDvKQA7oeDQ3/arcgis/rest/services/CPWAdminData/FeatureServer?f=pjson and https://services5.arcgis.com/ttNGmDvKQA7oeDQ3/arcgis/rest/services/CPWAdminData/FeatureServer/15?f=pjson

- **PRIMARY SOURCE — Stale embedded description.** Layer 15 still says “last updated on 2/5/2019,” contradicting its 2026 `editingInfo`. That sentence should not be used as the current data date. https://services5.arcgis.com/ttNGmDvKQA7oeDQ3/arcgis/rest/services/CPWAdminData/FeatureServer/15?f=pjson

- **UNKNOWN — Cadence.** The retrieved CPW publisher metadata gives a current generation/edit date but no recurring COTREX update schedule. A Boulder County derivative says quarterly, but that is not CPW’s own statement and therefore does not establish CPW’s cadence. CPW’s general GIS schedule covers administrative and wildlife layers, not COTREX. https://cpw.state.co.us/maps-and-gis

## COTREX schema

The current layer exposes 44 fields. The service supplies field names, types, lengths, and nullability, but no field descriptions or coded-value domains. Meanings below are therefore divided between documented system behavior and name-based inference. https://services5.arcgis.com/ttNGmDvKQA7oeDQ3/arcgis/rest/services/CPWAdminData/FeatureServer/15?f=pjson

| Field(s) | Published type | Meaning/evidence |
|---|---:|---|
| `FID` | OID | **PRIMARY SOURCE:** system-maintained object ID and layer unique-ID field. It identifies a published row, not a documented real-world trail. |
| `GlobalID` | GlobalID | **PRIMARY SOURCE:** non-null, unique indexed GlobalID for each feature row. No persistence guarantee is stated. |
| `feature_id` | String(254) | **UNKNOWN:** likely a source/segment feature identifier, but CPW provides no definition, uniqueness constraint, domain, or stability promise. |
| `place_id`, `place_id_1`, `place_id_2`, `place_id_3` | Integer | **INFERENCE:** identifiers for as many as four associated places/routes represented on the same segment. CPW provides no formal definition or stability promise. |
| `name`, `name_1`, `name_2`, `name_3` | String(254) | **INFERENCE:** as many as four names associated with the segment. This structure could represent overlaps, aliases, or joined places; the metadata does not distinguish them. |
| `trail_num`, `trail_num_`, `trail_num1`, `trail_nu_1` | String(254) | **INFERENCE:** as many as four source trail numbers associated with the segment. Their correspondence to the four name/place slots is not documented. |
| `type` | String(254) | **INFERENCE:** trail/facility type. No value domain or definition is published. |
| `surface` | String(254) | **INFERENCE:** surface description. No value domain is published. |
| `oneway` | String(254) | **INFERENCE:** one-way status or direction. Encoding is undocumented. |
| `hiking`, `horse`, `bike`, `motorcycle`, `atv`, `ohv_gt_50`, `highway_ve`, `dogs` | String(254) | **INFERENCE:** use-related values for hiking, equestrian, bicycle, motorcycle, ATV, OHV over 50 inches, highway vehicles, and dogs. The metadata does not define values, provenance, effective dates, or whether blank means prohibited, unknown, or not supplied. These fields must not independently be converted into an “allowed” status. |
| `snowmobile`, `ski`, `snowshoe` | String(254) | **INFERENCE:** winter-use values. Encoding and authority are undocumented. |
| `plowed`, `groomed`, `groomer_ur` | String(254) | **INFERENCE:** winter-maintenance fields, with `groomer_ur` probably a groomer URL; formal definitions are absent. |
| `access` | String(254) | **UNKNOWN:** an access-related source value, not a documented permission determination. |
| `seasonalit`, `seasonal_1`, `seasonal_2`, `seasonal_3` | String(254) | **INFERENCE:** as many as four seasonal statements, potentially corresponding to overlapping trail/place records. Encoding, applicable use, and legal effect are not documented. |
| `manager` | String(254) | **INFERENCE:** managing organization supplied for the segment. No controlled organization identifier is provided. |
| `length_mi_` | Double | **INFERENCE:** segment length in miles. |
| `min_elevat`, `max_elevat` | Double | **INFERENCE:** minimum and maximum elevation; units are not defined in layer metadata. |
| `url` | String(254) | **INFERENCE:** source or information URL. |
| `INPUT_DATE`, `EDIT_DATE` | Date, UTC | **INFERENCE:** source input and edit dates. The service defines UTC but does not explain which system or source event each date records. |
| `Shape__Length` | Double | **PRIMARY SOURCE:** service-computed geometry length in meters. |

Additional schema findings:

- **PRIMARY SOURCE — No `trail_id`.** The current published layer has `feature_id` and four `place_id` fields but no field literally named `trail_id`. https://services5.arcgis.com/ttNGmDvKQA7oeDQ3/arcgis/rest/services/CPWAdminData/FeatureServer/15?f=pjson

- **PRIMARY SOURCE — No relationships.** The layer publishes no ArcGIS relationships or related route table that would resolve `place_id` values into a documented trail-level entity. https://services5.arcgis.com/ttNGmDvKQA7oeDQ3/arcgis/rest/services/CPWAdminData/FeatureServer/15?f=pjson

- **PRIMARY SOURCE — No value domains.** All listed fields have `domain: null`; CPW does not publish machine-readable definitions for use, season, access, type, surface, or manager values in this layer. https://services5.arcgis.com/ttNGmDvKQA7oeDQ3/arcgis/rest/services/CPWAdminData/FeatureServer/15?f=pjson

- **INFERENCE — Overlap support.** Four parallel `place_id`/`name` and trail-number slots appear designed to retain multiple trail identities on one geometry segment. Because CPW does not document the slots, this should be treated as a possible grouping aid, not a guaranteed overlap model. https://services5.arcgis.com/ttNGmDvKQA7oeDQ3/arcgis/rest/services/CPWAdminData/FeatureServer/15?f=pjson

## USFS schema

### Service and currency

- **PRIMARY SOURCE — Service.** The current public layer is `Trans_Trail_NFS_Publish`, layer 0 of `EDW_TrailNFSPublish_01`. https://apps.fs.usda.gov/arcx/rest/services/EDW/EDW_TrailNFSPublish_01/MapServer/0?f=pjson

- **PRIMARY SOURCE — Publication subsets.** Forests may publish `TrailNFS_Centerline`, `TrailNFS_Basic`, or `TrailNFS_Mgmt`. Centerline contains location/name/number; Basic adds characteristics; Mgmt adds managed, accepted, discouraged, and restricted-use information. https://apps.fs.usda.gov/arcx/rest/services/EDW/EDW_TrailNFSPublish_01/MapServer?f=pjson and https://data.fs.usda.gov/geodata/edw/edw_resources/meta/S_USA.TrailNFS_Publish.xml

- **PRIMARY SOURCE — Daily pipeline.** The service description says EDW road and trail data are kept current by daily updates from forest geodatabases and that a newly added trail should appear the next day. https://apps.fs.usda.gov/arcx/rest/services/EDW/EDW_TrailNFSPublish_01/MapServer

### Identity and segmentation fields

| Field | Meaning |
|---|---|
| `TRAIL_NAME` | **PRIMARY SOURCE:** “The name that the trail or trail segment is officially or legally known by.” It may therefore vary by segment. https://data.fs.usda.gov/geodata/edw/edw_resources/meta/S_USA.TrailNFS_Publish.xml |
| `TRAIL_NO` | **PRIMARY SOURCE:** official numeric or alphanumeric trail identifier. It is a trail attribute, but uniqueness across forests is not promised. https://data.fs.usda.gov/geodata/edw/edw_resources/meta/S_USA.TrailNFS_Publish.xml |
| `TRAIL_CN` | **PRIMARY SOURCE:** an Oracle control number generated to “uniquely identify each trail across all Forest Service units.” This is the published route/trail-level grouping key. https://data.fs.usda.gov/geodata/edw/edw_resources/meta/S_USA.TrailNFS_Publish.xml |
| `BMP`, `EMP` | **PRIMARY SOURCE:** beginning and ending measure points for a segment along the trail route. https://data.fs.usda.gov/geodata/edw/edw_resources/meta/S_USA.TrailNFS_Publish.xml |
| `SEGMENT_LENGTH` | **PRIMARY SOURCE:** segment length in miles, calculated as `EMP - BMP`. https://data.fs.usda.gov/geodata/edw/edw_resources/meta/S_USA.TrailNFS_Publish.xml |
| `GIS_MILES` | **PRIMARY SOURCE:** GIS-calculated segment length, which may differ from `SEGMENT_LENGTH`. https://data.fs.usda.gov/geodata/edw/edw_resources/meta/S_USA.TrailNFS_Publish.xml |
| `GLOBALID` | **PRIMARY SOURCE:** unique indexed GlobalID on each published feature row. It is therefore segment-row identity in this service, but persistence across publication rebuilds is undocumented. https://apps.fs.usda.gov/arcx/rest/services/EDW/EDW_TrailNFSPublish_01/MapServer/0?f=pjson |
| `OBJECTID` | **PRIMARY SOURCE:** generated service row identifier. It should not be treated as durable identity. https://apps.fs.usda.gov/arcx/rest/services/EDW/EDW_TrailNFSPublish_01/MapServer/0?f=pjson |

### Characteristics

- **PRIMARY SOURCE — `TRAIL_CLASS`.** Prescribed development and management scale: 1 minimally developed through 5 fully developed; `N` means unavailable for the published subset. https://data.fs.usda.gov/geodata/edw/edw_resources/meta/S_USA.TrailNFS_Publish.xml

- **PRIMARY SOURCE — `TRAIL_SURFACE`.** Predominant expected surface, with documented values including native material, imported compacted material, asphalt, snow, blank, and `N/A`. https://data.fs.usda.gov/geodata/edw/edw_resources/meta/S_USA.TrailNFS_Publish.xml

- **PRIMARY SOURCE — `NATIONAL_TRAIL_DESIGNATION`.** Segment-level designation code: `0` not populated, `1` not designated, `2` other National Trail, and `3` National Scenic or National Historic Trail. https://data.fs.usda.gov/geodata/edw/edw_resources/meta/S_USA.TrailNFS_Publish.xml

- **PRIMARY SOURCE — Other Basic fields.** The service also publishes accessibility status, surface firmness, typical grade, typical and minimum tread width, cross slope, special-management area, and display/symbology fields. https://apps.fs.usda.gov/arcx/rest/services/EDW/EDW_TrailNFSPublish_01/MapServer/0?f=pjson

### Use fields

- **PRIMARY SOURCE — Use families.** For each relevant mode, the service publishes `*_MANAGED`, `*_ACCPT`, `*_DISC`, `*_ACCPT_DISC`, and `*_RESTRICTED` fields. Terra modes include hiker/pedestrian, pack-and-saddle, bicycle, motorcycle, ATV, and four-wheel-drive/OHV over 50 inches. Snow and water modes and class 1–3 e-bikes have corresponding families. https://apps.fs.usda.gov/arcx/rest/services/EDW/EDW_TrailNFSPublish_01/MapServer/0?f=pjson

- **PRIMARY SOURCE — Date encoding.** Populated use fields contain date ranges such as `01/01-12/31`; e-bike metadata expressly says the format is `MM/DD`. https://data.fs.usda.gov/geodata/edw/edw_resources/meta/S_USA.TrailNFS_Publish.xml

- **PRIMARY SOURCE — Combined fields.** `ALLOWED_TERRA_USE` concatenates codes for hiker/pedestrian, pack-and-saddle, bicycle, motorcycle, ATV, and 4WD over 50 inches. `ALLOWED_SNOW_USE` similarly encodes snowshoe, cross-country ski, and snowmobile. https://data.fs.usda.gov/geodata/edw/edw_resources/meta/S_USA.TrailNFS_Publish.xml

- **RESTRICTION / PRIMARY SOURCE.** Blank means not recorded, and `N/A` can mean the forest did not publish that attribute subset. Neither value supports an inference that a use is permitted. https://data.fs.usda.gov/geodata/edw/edw_resources/meta/S_USA.TrailNFS_Publish.xml

## Trail versus segment identity

### COTREX

- **PRIMARY SOURCE.** Each geometry row has a system `FID`, a `GlobalID`, a `feature_id`, and up to four place/name/number slots. The service does not document which of these represents source feature, physical segment, named trail, or displayed route. https://services5.arcgis.com/ttNGmDvKQA7oeDQ3/arcgis/rest/services/CPWAdminData/FeatureServer/15?f=pjson

- **UNKNOWN — Stable segment ID.** `GlobalID` is technically unique in the current service and `feature_id` looks source-oriented, but CPW gives no statement that either survives quarterly/full-service replacement, geometry splitting, merging, or re-ingestion.

- **UNKNOWN — Stable route ID.** One or more `place_id*` values may group segments into named places/routes, but no definition, related table, uniqueness rule, or persistence guarantee was retrieved.

- **INFERENCE — Tapping behavior.** Rendering and hit-testing raw COTREX rows will naturally produce separately tappable segments. A UI should not assume one row equals one complete named trail, particularly where `name_1`–`name_3` may represent overlaps. https://services5.arcgis.com/ttNGmDvKQA7oeDQ3/arcgis/rest/services/CPWAdminData/FeatureServer/15?f=pjson

### USFS

- **PRIMARY SOURCE — Trail identity.** `TRAIL_CN` identifies the trail across Forest Service units; repeated rows with the same `TRAIL_CN` are portions of that trail. https://data.fs.usda.gov/geodata/edw/edw_resources/meta/S_USA.TrailNFS_Publish.xml

- **PRIMARY SOURCE — Segment identity.** `BMP` and `EMP` identify a measured interval of the trail, while `SEGMENT_LENGTH` describes that interval. The feature row’s `GLOBALID` distinguishes the particular published segment feature. https://data.fs.usda.gov/geodata/edw/edw_resources/meta/S_USA.TrailNFS_Publish.xml and https://apps.fs.usda.gov/arcx/rest/services/EDW/EDW_TrailNFSPublish_01/MapServer/0?f=pjson

- **UNKNOWN — `TRAIL_CN` stability.** The metadata explicitly promises nationwide uniqueness but does not expressly promise immutability across route retirement, recreation, database migration, or major editing. It is the best documented route key, but “stable forever” is not established.

- **INFERENCE — Recommended USFS identity model.** Use `TRAIL_CN` as the trail grouping key, and `(TRAIL_CN, BMP, EMP)` as the semantic segment key. Retain `GLOBALID` for source traceability, but do not use `OBJECTID` as durable identity.

## Cross-source identity

- **PRIMARY SOURCE — COTREX includes USFS input.** CPW says COTREX trails come from several sources, explicitly including USFS, and are compiled by CPW contractor Natural Atlas. https://www.arcgis.com/sharing/rest/content/items/cae8ed959b8a4ed48680df62b31eec60?f=pjson

- **PRIMARY SOURCE — No exposed USFS control number.** COTREX layer 15 does not publish a `TRAIL_CN` field. Its closest source field is `trail_num` plus three similarly named variants. https://services5.arcgis.com/ttNGmDvKQA7oeDQ3/arcgis/rest/services/CPWAdminData/FeatureServer/15?f=pjson

- **INFERENCE — Possible match.** For USFS-derived records, a COTREX `trail_num*` may preserve `TRAIL_NO`; matching should additionally use manager and geometry because USFS does not promise that `TRAIL_NO` is nationally unique.

- **UNKNOWN — Shared key.** No retrieved CPW metadata states that `feature_id`, any `place_id`, or any `trail_num*` is copied from `TRAIL_CN`, `GLOBALID`, or another durable USFS key. There is therefore no documented lossless shared key between the current public COTREX and USFS services.

- **INFERENCE — Crosswalk method.** A defensible crosswalk would need source manager + normalized trail number + name + geometric overlap, while retaining uncertainty and possible many-to-many matches. Name alone is unsafe because the USFS national service contains unrelated same-name trails in multiple forests.

## Uses, seasons and closures

### Restrictions first

- **PRIMARY SOURCE.** COTREX itself says a mapped trail does not imply that it is open for general public use and directs users to landowners, managers, and governing agencies for current legality. https://trails.colorado.gov/terms

- **PRIMARY SOURCE.** The USFS trail layer says the richest `TrailNFS_Mgmt` attributes must be consistent with the forest’s published Motor Vehicle Use Map, but publication completeness varies by forest. https://apps.fs.usda.gov/arcx/rest/services/EDW/EDW_TrailNFSPublish_01/MapServer?f=pjson

- **INFERENCE.** Even a populated annual date range in either source is not sufficient to declare current access: emergency orders, fire restrictions, wildlife closures, maintenance closures, and more recent manager notices may supersede the base trail record.

### COTREX alerts and closures

- **PRIMARY SOURCE.** CPW says more than 36 agency partners post real-time advisories, closures, hazards, and other alerts in COTREX. https://cpw.state.co.us/news/12042025/colorado-trail-explorer-cotrex-app-shares-trail-closures-protect-wintering-wildlife

- **PRIMARY SOURCE.** CPW says displayed seasonal closures include descriptions, boundaries, and links, apply to motorized and nonmotorized activity, and are mandatory and enforceable. https://cpw.state.co.us/news/12042025/colorado-trail-explorer-cotrex-app-shares-trail-closures-protect-wintering-wildlife

- **PRIMARY SOURCE.** COTREX support documentation says closure/advisory records are created and ended by participating managers and may be associated spatially with followable areas; individual trails could not be followed at the documented time. https://cotrex.zendesk.com/hc/en-us/articles/360050882514-How-do-public-notifications-and-email-subscriptions-work

- **PRIMARY SOURCE — Not in trail layer.** Layer 15 has no alert, closure-status, closure-boundary, order-number, or alert-effective-date fields. https://services5.arcgis.com/ttNGmDvKQA7oeDQ3/arcgis/rest/services/CPWAdminData/FeatureServer/15?f=pjson

- **UNKNOWN — Machine-readable closure feed.** No official public ArcGIS layer, documented API, or licensed download for COTREX closures/alerts was found in the bounded review. The alerts visible in the application therefore cannot be assumed available for ingestion or redistribution.

### USFS closures

- **PRIMARY SOURCE.** White River National Forest publishes current alerts on its forest website, including restriction/closure notices and associated Forest Order numbers where applicable. https://www.fs.usda.gov/r02/whiteriver/alerts

- **PRIMARY SOURCE.** Examples visible on the accessed page included an FSR 286 motorized-traffic closure, an overnight-parking closure at Maroon Creek Road, and Stage 1 fire restrictions. These demonstrate that current restrictions live outside the EDW trail geometry layer. https://www.fs.usda.gov/r02/whiteriver/alerts

- **UNKNOWN — Machine-readable orders.** The retrieved White River page is structured web content with links/order references, but no official geospatial closure API or documented machine-readable forest-order feed was discovered. Forest orders may also be PDFs whose legal boundary descriptions require interpretation.

## Sample records

All sample queries used `returnGeometry=false`. No permission conclusion is drawn from any use attribute.

### Difficult Creek

- **PRIMARY SOURCE — USFS count.** Exact `TRAIL_NAME='DIFFICULT CREEK'` returned **2 records**. Count query: https://apps.fs.usda.gov/arcx/rest/services/EDW/EDW_TrailNFSPublish_01/MapServer/0/query?f=json&where=trail_name%3D%27DIFFICULT%20CREEK%27&returnCountOnly=true

- **PRIMARY SOURCE — USFS identity.** Both records have `TRAIL_NO=2146` and `TRAIL_CN=5695010314`. Their measured intervals are `0.0–2.5` and `2.5–3.2656`, with distinct segment `GLOBALID` values. Attribute query: https://apps.fs.usda.gov/arcx/rest/services/EDW/EDW_TrailNFSPublish_01/MapServer/0/query?where=trail_name%20LIKE%20%27%25DIFFICULT%20CREEK%25%27&outFields=objectid,globalid,trail_name,trail_no,trail_cn,bmp,emp,segment_length,gis_miles,admin_org,managing_org,attributesubset,trail_class,trail_surface,national_trail_designation,hiker_pedestrian_managed,hiker_pedestrian_accpt,hiker_pedestrian_disc,hiker_pedestrian_accpt_disc,hiker_pedestrian_restricted,pack_saddle_managed,bicycle_managed,motorcycle_managed,atv_managed&returnGeometry=false&resultRecordCount=20&f=pjson

- **PRIMARY SOURCE — Raw use attributes.** Both Difficult Creek rows publish `TrailNFS_MGMT`, native-material surface, `HIKER_PEDESTRIAN_ACCPT=01/01-12/31`, and `PACK_SADDLE_MANAGED=01/01-12/31`. These are source attributes, not a determination of current permission. Same query URL as above.

- **UNKNOWN — COTREX exact count and IDs.** The current CPW endpoint’s detailed attribute query failed to load through the retrieval service. A broader `name LIKE '%DIFFICULT%'` count returned **19 statewide rows**, but that is not a valid count for the Aspen Difficult Creek trail because it can include other names and locations. Broad count query: https://services5.arcgis.com/ttNGmDvKQA7oeDQ3/arcgis/rest/services/CPWAdminData/FeatureServer/15/query?f=json&where=name%20like%20%27%25DIFFICULT%25%27&returnCountOnly=true

- **UNKNOWN — Cross-source agreement.** COTREX-to-USFS agreement on `TRAIL_NO=2146` could not be verified from a successfully retrieved COTREX sample, and COTREX exposes no `TRAIL_CN` field.

### Cathedral Lake

- **PRIMARY SOURCE — USFS count.** Exact `TRAIL_NAME='CATHEDRAL LAKE'` returned **2 records**. Count query: https://apps.fs.usda.gov/arcx/rest/services/EDW/EDW_TrailNFSPublish_01/MapServer/0/query?f=json&where=trail_name%3D%27CATHEDRAL%20LAKE%27&returnCountOnly=true

- **PRIMARY SOURCE — USFS identity.** Both rows have `TRAIL_NO=1984` and `TRAIL_CN=6338010314`; intervals are `0.0–2.0` and `2.0–2.7185`, with distinct `GLOBALID` values. Attribute query: https://apps.fs.usda.gov/arcx/rest/services/EDW/EDW_TrailNFSPublish_01/MapServer/0/query?where=trail_name%20LIKE%20%27%25CATHEDRAL%20LAKE%25%27&outFields=objectid,globalid,trail_name,trail_no,trail_cn,bmp,emp,segment_length,gis_miles,admin_org,managing_org,attributesubset,trail_class,trail_surface,national_trail_designation,hiker_pedestrian_managed,hiker_pedestrian_accpt,hiker_pedestrian_disc,hiker_pedestrian_accpt_disc,hiker_pedestrian_restricted,pack_saddle_managed,bicycle_managed,motorcycle_managed,atv_managed&returnGeometry=false&resultRecordCount=20&f=pjson

- **PRIMARY SOURCE — Raw use attributes.** Both rows publish `TrailNFS_MGMT`, native-material surface, and annual `HIKER_PEDESTRIAN_MANAGED` and `PACK_SADDLE_MANAGED` ranges. These are not a current access determination. Same query URL as above.

- **UNKNOWN — COTREX exact count and IDs.** A title-case exact COTREX query returned zero, while broader `name LIKE '%CATHEDRAL%'` returned **32 statewide rows**. Because casing/naming and geographic filtering were not resolved, neither result establishes the Aspen trail’s COTREX record count. Exact query: https://services5.arcgis.com/ttNGmDvKQA7oeDQ3/arcgis/rest/services/CPWAdminData/FeatureServer/15/query?where=name%3D%27Cathedral%20Lake%27&outFields=FID%2CGlobalID%2Cfeature_id%2Cplace_id%2Cname%2Cplace_id_1%2Cname_1%2Cplace_id_2%2Cname_2%2Cplace_id_3%2Cname_3%2Ctrail_num%2Ctrail_num_%2Ctrail_num1%2Ctrail_nu_1%2Cmanager%2Clength_mi_&returnGeometry=false&f=pjson ; broad count: https://services5.arcgis.com/ttNGmDvKQA7oeDQ3/arcgis/rest/services/CPWAdminData/FeatureServer/15/query?f=json&where=name%20like%20%27%25CATHEDRAL%25%27&returnCountOnly=true

### What the samples establish

- **PRIMARY SOURCE.** USFS Difficult Creek and Cathedral Lake each consist of two separately published segment rows but one shared `TRAIL_CN` per named trail. The segment boundaries are expressed by contiguous `BMP`/`EMP` ranges. Sample query URLs above.

- **INFERENCE.** For USFS data, Ohvernight can group the two tappable features into a trail entity using `TRAIL_CN`, while still retaining each segment for attributes and geometry.

- **UNKNOWN.** The equivalent COTREX grouping and cross-source identifier agreement remain unverified because the public schema does not define its identity fields and the detailed sample responses did not load.

## Other aggregations

- **PRIMARY SOURCE — USGS National Digital Trails.** USGS aggregates trails from “predominantly authoritative sources” into the National Transportation Database. Data are available through the National Map Viewer, Trails Explorer, downloadable state/national shapefiles or geodatabases, and National Map services. https://www.usgs.gov/national-digital-trails/data and https://www.usgs.gov/national-digital-trails/how-access-or-view-usgs-trails-dataset-0

- **PRIMARY SOURCE — Public-domain statement.** USGS describes the digital trails dataset as a nationwide public-domain geospatial aggregation. https://www.usgs.gov/national-digital-trails/how-access-or-view-usgs-trails-dataset-0

- **INFERENCE.** National Digital Trails may be useful as a geometry/name comparison layer and as a more clearly reusable national aggregation, but aggregation can lose source-specific route identity and current use/closure semantics.

- **UNKNOWN.** This review did not establish whether current Colorado NDT features preserve USFS `TRAIL_CN`, COTREX `feature_id`, or another source key. It should not be assumed to solve cross-source identity.

## Unknowns

1. **COTREX redistribution permission:** no affirmative permission for republication in a separate static site was found; COTREX application terms prohibit distribution without a separate written agreement. https://trails.colorado.gov/terms
2. **COTREX identifier semantics:** `feature_id`, `place_id*`, and the four trail-number fields are undocumented.
3. **COTREX identifier stability:** no field is promised stable across updates, rebuilds, splits, merges, or source replacement.
4. **COTREX route grouping:** no documented trail-level relationship or related route table is exposed.
5. **Shared USFS key:** COTREX does not expose `TRAIL_CN`; no documented crosswalk was found.
6. **COTREX cadence:** current publication dates are available, but no official recurring cadence was found.
7. **COTREX closures API:** official closures exist in the app, but no licensed public machine-readable feed was found.
8. **USFS closure API:** forest alerts and orders are published on forest pages, but no authoritative geospatial/order API was found in this review.
9. **`TRAIL_CN` permanence:** nationwide uniqueness is documented; indefinite persistence is not.
10. **Exact COTREX sample counts and identifier agreement:** detailed Aspen sample queries failed or were inconclusive, so these remain unknown rather than inferred from statewide substring counts.

## Recommendation

1. Continue using USFS EDW segments, but model two levels:
   - trail: `TRAIL_CN`;
   - segment: source `GLOBALID` plus `TRAIL_CN`, `BMP`, and `EMP`.
   Do not use `OBJECTID` as durable identity. https://data.fs.usda.gov/geodata/edw/edw_resources/meta/S_USA.TrailNFS_Publish.xml

2. Group USFS segments sharing `TRAIL_CN` into one selectable trail presentation while preserving segment-level use, surface, class, and measure differences. Display overlaps as multiple trail identities rather than choosing one name by geometry alone.

3. Do not publish COTREX data in Ohvernight until redistribution rights are affirmatively established. Public ArcGIS access and downloads do not override the COTREX terms’ separate-written-agreement requirement. https://trails.colorado.gov/terms

4. If COTREX use is later cleared, retain every raw identity slot—`feature_id`, all `place_id*`, `name*`, and trail-number fields—and first measure uniqueness and persistence across at least two releases. Do not initially collapse them into one undocumented `trail_id`.

5. Build any COTREX–USFS crosswalk as probabilistic provenance data using manager, trail number, name, and geometric overlap. Never represent a match as authoritative unless CPW documents a shared key.

6. Treat trail-use and seasonal fields as source attributes, not current permission. Before showing any “allowed/open” status, require a current sentence from the responsible agency or operator and check separately published closures/orders. Use the COTREX and USFS base layers only for discovery and restriction-first prompts.
