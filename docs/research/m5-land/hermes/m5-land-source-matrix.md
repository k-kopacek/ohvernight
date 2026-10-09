DRAFT - UNREVIEWED

# M5 — Land Source Matrix for Colorado

> Hermes report (GPT-5.6 luna), 2026-10-07, stored as returned. HERMES-SOURCED: web research only, no repository access. Nothing here is verified by the coordinator unless another document says so, and nothing is decided.

Access date: 2026-10-07. Research only; nothing is ingested or published.

Status labels:

- PRIMARY SOURCE — read on the publisher’s own page, service metadata, or publisher-hosted terms.
- INFERENCE — conclusion drawn from retrieved primary material.
- UNKNOWN — not established by retrieved material.

## Executive findings

- [PRIMARY SOURCE] The BLM National Surface Management Agency layer is a management-jurisdiction dataset, not a land-title or access dataset. BLM states that SMA depicts an agency’s “surface administrative jurisdiction” and does not show ownership-pattern boundaries. [BLM National SMA metadata](https://gis.blm.gov/arcgis/rest/services/lands/BLM_Natl_SMA_LimitedScale/MapServer?f=pjson)
- [PRIMARY SOURCE] PAD-US 4.1 is the most recent PAD-US release retrieved, released in March 2025. It contains owner, manager, designation, conservation-status, and categorical public-access attributes, but USGS warns that access is primarily assigned categorically rather than through individual-unit review. [PAD-US Data History](https://www.usgs.gov/programs/gap-analysis-project/pad-us-data-history) · [PAD-US Data Overview](https://www.usgs.gov/programs/gap-analysis-project/science/pad-us-data-overview)
- [PRIMARY SOURCE] Colorado State Land Board trust land is not generally open to public recreation. Public access depends on a recreation lease, permit, or a CPW access-program lease, and the State Land Board states that other recreational uses are prohibited unless posted. [State Land Board public access](https://slb.colorado.gov/public-access) · [State Land Board recreation leases](https://slb.colorado.gov/lease/recreation)
- [PRIMARY SOURCE] CPW’s Walk-In Access program authorizes a narrow activity and time window: hunting only, generally on foot, with program-specific license, season, signage, and property restrictions. [CPW Walk-In Access](https://cpw.state.co.us/activities/hunting/where-hunt/walk-access-program)
- [PRIMARY SOURCE] County parcel and open-space data identify parcels, ownership, easements, restrictions, or managing agencies, but the retrieved county material does not make those datasets general recreation-permission authorities. Douglas County expressly warns that protected-land properties do not necessarily indicate public access. [Pitkin parcel metadata](https://maps.pitkincounty.com/arcgis/rest/services/Hosted/Parcel_Boundary/MapServer/0?f=pjson) · [Douglas County protected-land search result](https://www.douglasco.gov/documents/open-space-and-protected-lands.pdf/)
- [PRIMARY SOURCE] Commercial parcel terms are materially different from open-data terms. Regrid’s standard store license prohibits resale, sublicensing, or otherwise making the data available to third parties, although it permits rendering parcel polygons in a way that prevents customers from obtaining a substantial copy. [Regrid Data Store License](https://app.regrid.com/store/license)

## Matrix

### 1. BLM National Surface Management Agency

- PUBLISHER: Bureau of Land Management.
- WHAT IT CONTAINS: Federal surface-management polygons classified by active federal surface-managing agency. Retrieved fields include `OBJECTID`, `SHAPE`, `SMA_ID`, `ADMIN_DEPT_CODE`, `ADMIN_AGENCY_CODE`, `ADMIN_UNIT_NAME`, `ADMIN_UNIT_TYPE`, `HOLD_ID`, `HOLD_DEPT_CODE`, `HOLD_AGENCY_CODE`, `ADMIN_ST`, `FAU_ID`, `SHAPE_Length`, and `SHAPE_Area`. [PRIMARY SOURCE](https://gis.blm.gov/arcgis/rest/services/lands/BLM_Natl_SMA_LimitedScale/MapServer/layers?f=pjson)
- GEOGRAPHY/SCALE: National coverage across the continental United States, Alaska, Hawaii, Puerto Rico, Guam, American Samoa, and the U.S. Virgin Islands. The limited-scale service is intended for display below approximately 1:36,000; the cached BLM-only service is available at ArcGIS tiling level 14, approximately 1:36,000. [PRIMARY SOURCE](https://gis.blm.gov/arcgis/rest/services/lands/BLM_Natl_SMA_LimitedScale/MapServer?f=pjson) · [PRIMARY SOURCE](https://gis.blm.gov/arcgis/rest/services/lands/BLM_Natl_SMA_Cached_BLM_Only/MapServer/layers?f=pjson)
- ENDPOINT URL: [Limited-scale national SMA MapServer](https://gis.blm.gov/arcgis/rest/services/lands/BLM_Natl_SMA_LimitedScale/MapServer) · [National SMA including private/unknown display class](https://gis.blm.gov/arcgis/rest/services/lands/BLM_Natl_SMA_Cached_with_PriUnk/MapServer) · [Cached BLM-only service](https://gis.blm.gov/arcgis/rest/services/lands/BLM_Natl_SMA_Cached_BLM_Only/MapServer)
- LICENCE/TERMS: [UNKNOWN] The retrieved national service metadata provides BLM copyright and limitations but no clear redistribution grant. BLM states, “The SMA data do not illustrate land status ownership pattern boundaries.” [PRIMARY SOURCE](https://gis.blm.gov/arcgis/rest/services/lands/BLM_Natl_SMA_Cached_BLM_Only/MapServer/layers?f=pjson)
- UPDATE CADENCE: [PRIMARY SOURCE] The service is described as a dynamic assembly of data maintained by federal and local offices. A fixed national refresh interval was not stated. [UNKNOWN] [National SMA metadata](https://gis.blm.gov/arcgis/rest/services/lands/BLM_Natl_SMA_LimitedScale/MapServer?f=pjson)
- STABLE IDENTIFIER: `SMA_ID` exists. [UNKNOWN] The retrieved metadata does not promise that `SMA_ID` remains stable across edits or service rebuilds. [PRIMARY SOURCE](https://gis.blm.gov/arcgis/rest/services/lands/BLM_Natl_SMA_LimitedScale/MapServer/layers?f=pjson)
- WHAT IT DOES NOT ESTABLISH: It does not establish fee ownership, title, legal boundary accuracy, public access, route legality, recreation permission, camping permission, overnight permission, or activity legality. [PRIMARY SOURCE](https://gis.blm.gov/arcgis/rest/services/lands/BLM_Natl_SMA_LimitedScale/MapServer?f=pjson)
- KNOWN LIMITS: It is assembled from source data maintained by different offices and sources; scale and accuracy may vary. The separate `Private or Unknown` label category should not be treated as proof that every polygon is private. [PRIMARY SOURCE](https://gis.blm.gov/arcgis/rest/services/lands/BLM_Natl_SMA_Cached_with_PriUnk/MapServer/layers?f=pjson)

### 2. BLM Colorado Surface Management Agency

- PUBLISHER: Bureau of Land Management, Colorado State Office.
- WHAT IT CONTAINS: Colorado surface-management polygons. The retrieved service exposes fields including `OBJECTID`, `SMA_ID`, `GIS_acres`, `adm_code`, `adm_manage`, `adm_name`, and geometry/shape fields; the renderer uses management codes such as `BLM`, `BOR`, `BIA`, `DOD`, `USFS`, `NPS`, `USFW`, `STA`, `LOCAL`, `PRI`, and `OTHER`. [PRIMARY SOURCE](https://gis.blm.gov/coarcgis/rest/services/lands/BLM_Colorado_Surface_Management_Agency/FeatureServer/1?f=pjson)
- GEOGRAPHY/SCALE: Colorado statewide. BLM describes the intended use as small-scale analysis at 1:24,000 and smaller, but the underlying source material ranges from 1:100,000 to 1:24,000 and includes differing vintages. [PRIMARY SOURCE](https://gis.blm.gov/coarcgis/rest/services/lands/BLM_Colorado_Surface_Management_Agency/FeatureServer/1/metadata?format=iso19139) · [BLM Colorado service](https://gis.blm.gov/coarcgis/rest/services/lands/BLM_Colorado_Surface_Management_Agency/MapServer)
- ENDPOINT URL: [BLM Colorado SMA FeatureServer layer 1](https://gis.blm.gov/coarcgis/rest/services/lands/BLM_Colorado_Surface_Management_Agency/FeatureServer/1) · [MapServer](https://gis.blm.gov/coarcgis/rest/services/lands/BLM_Colorado_Surface_Management_Agency/MapServer)
- LICENCE/TERMS: [PRIMARY SOURCE] The BLM Colorado catalog record identifies the data as public domain: “None, these data are considered public domain.” It also retains BLM’s no-warranty, no-legal-survey limitations. [BLM Colorado catalog record](https://catalog.data.gov/dataset/blm-colorado-surface-management-agency)
- UPDATE CADENCE: [PRIMARY SOURCE] “This dataset is subject to update daily.” [BLM Colorado service](https://gis.blm.gov/coarcgis/rest/services/lands/BLM_Colorado_Surface_Management_Agency/MapServer)
- STABLE IDENTIFIER: `SMA_ID` exists; `adm_code` and `adm_manage` are classification fields. [UNKNOWN] Stable-ID behavior is not stated. [PRIMARY SOURCE](https://gis.blm.gov/coarcgis/rest/services/lands/BLM_Colorado_Surface_Management_Agency/FeatureServer/1?f=pjson)
- WHAT IT DOES NOT ESTABLISH: It does not establish fee ownership, a legal parcel boundary, public access, route permission, camping, overnight use, or permission for a chosen activity. The service describes who manages the surface, not what a visitor may do. [PRIMARY SOURCE](https://gis.blm.gov/coarcgis/rest/services/lands/BLM_Colorado_Surface_Management_Agency/FeatureServer/1/metadata?format=iso19139)
- KNOWN LIMITS: Mixed source scales, vintages, and linework; process steps and publication dates are not reflected in the service metadata. [PRIMARY SOURCE](https://gis.blm.gov/coarcgis/rest/services/lands/BLM_Colorado_Surface_Management_Agency/MapServer)

### 3. USGS PAD-US 4.1

- PUBLISHER: U.S. Geological Survey Gap Analysis Project.
- WHAT IT CONTAINS: Protected-area polygons covering fee ownership, easements, designations, and other protected-area records. Retrieved real fields include `Mang_Name`, `Mang_Type`, `Own_Name`, `Own_Type`, `Pub_Access`, `GAP_Sts`, `Des_Tp`, `Unit_Nm`, `GIS_Acres`, `Date_Est`, and source/reference fields. [PRIMARY SOURCE](https://www.usgs.gov/programs/gap-analysis-project/pad-us-data-manual) · [PAD-US metadata search result](https://data.usgs.gov/datacatalog/metadata/USGS.652d4ebbd34e44db0e2ee458.xml)
- GEOGRAPHY/SCALE: National terrestrial and marine inventory, including public lands and voluntarily provided private protected areas. USGS recommends PAD-US for general information across more than one agency and warns against using it as a fine-scale legal boundary product. [PRIMARY SOURCE](https://www.usgs.gov/programs/gap-analysis-project/science/pad-us-data-overview) · [PAD-US 4.0 metadata limitations](https://data.usgs.gov/datacatalog/metadata/USGS.652d4ebbd34e44db0e2ee458.xml)
- ENDPOINT URL: [PAD-US download and web-service directory](https://www.usgs.gov/programs/gap-analysis-project/science/pad-us-data-overview) · [PAD-US web services page](https://www.usgs.gov/programs/gap-analysis-project/science/pad-us-data-web-services) · [PAD-US DOI](https://doi.org/10.5066/P96WBCHS). The retrieved National Map ArcGIS endpoint was temporarily unavailable during this session: [attempted endpoint](https://edits.nationalmap.gov/arcgis/rest/services/PAD-US/PAD_US_Landforms/MapServer/0?f=pjson).
- LICENCE/TERMS: [PRIMARY SOURCE] The PAD-US Data Manual states, “All data suitable for distribution in the public domain.” [PAD-US Data Manual](https://www.usgs.gov/programs/gap-analysis-project/pad-us-data-manual)
- UPDATE CADENCE: [PRIMARY SOURCE] Version 4.1 was released in March 2025. [PAD-US Data History](https://www.usgs.gov/programs/gap-analysis-project/pad-us-data-history) [UNKNOWN] No fixed recurring refresh interval was retrieved.
- STABLE IDENTIFIER: The dataset has a stable DOI, `10.5066/P96WBCHS`. [PRIMARY SOURCE](https://doi.org/10.5066/P96WBCHS) [UNKNOWN] A stable polygon identifier was not established from the retrieved material; `OBJECTID` should not be assumed stable across releases.
- WHAT `Pub_Access` ACTUALLY MEANS: `Pub_Access` is a general public-access category:
  - `OA` / Open: no special access requirement, although regular hours may apply.
  - `RA` / Restricted: special permit, registration, or highly variable/seasonal access.
  - `XA` / Closed: no public access.
  - `UK` / Unknown: information unavailable.
  [PRIMARY SOURCE](https://data.usgs.gov/datacatalog/metadata/USGS.652d4ebbd34e44db0e2ee458.xml)
- CAVEATS: USGS states that access is “fully attributed but primarily assigned categorically instead of through individual unit review.” [PRIMARY SOURCE](https://www.usgs.gov/programs/gap-analysis-project/science/pad-us-data-overview) `Pub_Access` is not an activity-specific authorization, not a camping authorization, and not a statement that overnight use is permitted.
- WHAT `GAP_Sts` MEANS: It measures management intent for biodiversity protection, not visitor access. [PRIMARY SOURCE](https://www.usgs.gov/programs/gap-analysis-project/pad-us-data-manual)
- WHAT `Des_Tp` MEANS: It is the standardized designation type, such as a national park, wilderness, conservation area, or conservation easement. It is not itself an access rule. [PRIMARY SOURCE](https://www.usgs.gov/programs/gap-analysis-project/pad-us-data-manual)
- WHAT IT DOES NOT ESTABLISH: It does not establish title for every record, a current agency rule, exact legal boundaries, route legality, camping, overnight use, or permission for a particular activity. Overlapping records can represent different fee, easement, and designation interests. [PRIMARY SOURCE](https://data.usgs.gov/datacatalog/metadata/USGS.652d4ebbd34e44db0e2ee458.xml)

### 4. COMaP — Colorado Ownership, Management and Protection

- PUBLISHER: Colorado Natural Heritage Program and Colorado State University Geospatial Centroid.
- WHAT IT CONTAINS: Protected-land polygons and records from more than 300 sources, with attributes including owner, manager, easement holder, and public access. The publisher’s terms specifically refer to a `PUBLIC_ACCESS` field for map services. [PRIMARY SOURCE](https://comap.cnhp.colostate.edu/terms-of-use/) · [COMaP brochure](https://comap.cnhp.colostate.edu/wp-content/uploads/2016/04/COMaP_White_Paper.pdf)
- GEOGRAPHY/SCALE: Colorado statewide protected lands, including public lands and private conservation easements. The publisher describes more than 28,000 protected-land entries. [PRIMARY SOURCE](https://comap.cnhp.colostate.edu/about-comap/) · [COMaP brochure](https://comap.cnhp.colostate.edu/wp-content/uploads/2016/04/COMaP_White_Paper.pdf)
- ENDPOINT URL: [COMaP viewer](https://comap.cnhp.colostate.edu/comap/) · [COMaP downloads](https://comap.cnhp.colostate.edu/comap-downloads/) · [COMaP terms](https://comap.cnhp.colostate.edu/terms-of-use/)
- LICENCE/TERMS: [PRIMARY SOURCE] The publisher states, “Under no circumstances are data to be REDISTRIBUTED.” It also states, “By downloading or viewing COMaP data, no right has been created to access protected lands.” [COMaP terms](https://comap.cnhp.colostate.edu/terms-of-use/)
- COST: [PRIMARY SOURCE] The retrieved publisher brochure reports annual organization subscriptions of $175 for nonprofits, $300 for government and small businesses, $500 for corporations and academic units, with fees subject to change and redistribution prohibited. [COMaP brochure](https://comap.cnhp.colostate.edu/wp-content/uploads/2016/04/COMaP_White_Paper.pdf)
- UPDATE CADENCE: [PRIMARY SOURCE] Data are continually updated, and the user is responsible for downloading the latest dataset. [COMaP terms](https://comap.cnhp.colostate.edu/terms-of-use/)
- STABLE IDENTIFIER: [UNKNOWN] No stable polygon identifier was established from the retrieved material.
- WHAT IT DOES NOT ESTABLISH: It does not create access rights, trespass permission, activity authorization, or an overnight-use right. The publisher specifically warns that many protected lands are not open to the public. [PRIMARY SOURCE](https://comap.cnhp.colostate.edu/terms-of-use/)
- LICENSING FIT FOR OHVERNIGHT: [INFERENCE] COMaP is unsuitable for redistribution in a public static site under the retrieved standard terms. A map-service arrangement may exist, but it would require compliance with the publisher’s special-use terms and a paid subscription. [COMaP terms](https://comap.cnhp.colostate.edu/terms-of-use/)

### 5. Colorado State Land Board trust-land GIS

- PUBLISHER: Colorado State Land Board.
- WHAT IT CONTAINS: Surface trust land, trust mineral estate, ownership records, current lease records, and related trust-asset records. [PRIMARY SOURCE](https://slb.colorado.gov/maps)
- GEOGRAPHY/SCALE: Statewide Colorado trust lands and mineral estate. [PRIMARY SOURCE](https://slb.colorado.gov/maps)
- ENDPOINT URL: [State Land Board map server](https://gis.colorado.gov/trustlands/) · [SLB maps page](https://slb.colorado.gov/maps) · [SLB ArcGIS maps](https://slb.colorado.gov/maps/arcgis)
- REAL FIELD NAMES: [UNKNOWN] The retrieved map application did not expose a machine-readable layer schema. The map supports searches by township/range, section, county, lease number, lessee name, property name, and coordinates, but those search labels are not confirmed field names. [PRIMARY SOURCE](https://slb.colorado.gov/maps)
- LICENCE/TERMS: [UNKNOWN] A redistribution licence for the GIS records was not retrieved.
- UPDATE CADENCE: [UNKNOWN] The map states that it contains current lease records, but no fixed update schedule was retrieved. [PRIMARY SOURCE](https://slb.colorado.gov/maps)
- STABLE IDENTIFIER: Lease number and other ownership-record identifiers exist in the map’s search functions, but [UNKNOWN] no stable polygon identifier was established.
- PUBLIC ACCESS RULE: [PRIMARY SOURCE] The State Land Board states, “This land -- called trust land -- is not open to the public.” It then says public access occurs when a property is leased for public recreation. [State Land Board public access](https://slb.colorado.gov/public-access)
- PUBLIC ACCESS PROGRAM: [PRIMARY SOURCE] CPW’s Hunting and Fishing Access Program provides seasonal and limited access on enrolled properties. The State Land Board states, “Unless posted on property, all other recreational uses are prohibited.” [State Land Board public access](https://slb.colorado.gov/public-access)
- WHAT IT DOES NOT ESTABLISH: Ownership of trust land does not establish public recreation access. A lease record alone does not establish that a visitor’s chosen activity or overnight use is allowed; the controlling lease, current signs, site rules, and agency/operator page are needed. [PRIMARY SOURCE](https://slb.colorado.gov/lease/recreation)

### 6. Colorado Parks and Wildlife

- PUBLISHER: Colorado Parks and Wildlife.
- WHAT IT CONTAINS: State Wildlife Area boundaries, State Park boundaries, CPW properties, Public Access Properties, Walk-In Access boundaries, recreation facilities, trails, wildlife layers, hunting/fishing access layers, and related map products. [PRIMARY SOURCE](https://cpw.state.co.us/maps-and-gis)
- GEOGRAPHY/SCALE: Colorado statewide. CPW provides shapefiles, ArcGIS layer packages, ArcGIS web services, KMZ files, GeoPDFs, and interactive Hunting and Fishing Atlases. [PRIMARY SOURCE](https://cpw.state.co.us/maps-and-gis)
- ENDPOINT URL: [CPW GIS and maps](https://cpw.state.co.us/maps-and-gis) · [CPW ArcGIS Hub downloads](https://geodata-cpw.hub.arcgis.com/search?q=download) · [CPW Hunting Atlas](https://ndismaps.nrel.colostate.edu/index.html?app=HuntingAtlas) · [CPW State Wildlife Area Finder](https://cpw.state.co.us/swa-finder) · [CPW Walk-In Access](https://cpw.state.co.us/activities/hunting/where-hunt/walk-access-program)
- REAL FIELD NAMES: [UNKNOWN] The retrieved public CPW GIS page identifies datasets and formats but does not expose the layer schemas or stable feature fields.
- LICENCE/TERMS: [UNKNOWN] A general CPW GIS redistribution licence was not retrieved.
- UPDATE CADENCE: [PRIMARY SOURCE] CPW publishes an annual schedule: administrative boundaries in February and March, Public Access Properties in August, regular Walk-In Access boundaries in September, late-season Walk-In Access boundaries in November, and wildlife species data in December. [PRIMARY SOURCE](https://cpw.state.co.us/maps-and-gis)
- STABLE IDENTIFIER: [UNKNOWN] No stable public feature identifier was established.
- STATE WILDLIFE AREAS: [PRIMARY SOURCE] SWAs may be state- or privately owned, have different allowed activities by property, and require an SWA pass or valid hunting/fishing license for most visitors. [CPW SWA Finder](https://cpw.state.co.us/swa-finder)
- WALK-IN ACCESS: [PRIMARY SOURCE] WIA properties require program rules, a valid small-game license, a habitat stamp, foot access, applicable dates, and posted boundary signs. CPW states, “Access into properties is by foot and hunting only; all other activities are prohibited.” [CPW Walk-In Access](https://cpw.state.co.us/activities/hunting/where-hunt/walk-access-program)
- WHAT IT DOES NOT ESTABLISH: A CPW boundary does not by itself establish that hiking, biking, camping, boating, overnight use, or any other activity is allowed. Each property’s current rules and restrictions control. [PRIMARY SOURCE](https://cpw.state.co.us/swa-finder)

### 7. U.S. Forest Service ownership and administrative boundaries

#### Basic Ownership

- PUBLISHER: USDA Forest Service.
- WHAT IT CONTAINS: Surface-ownership parcels dissolved by ownership classification. Retrieved fields include `BASICOWNERSHIPID`, `OWNERCLASSIFICATION`, `GIS_ACRES`, `REGION`, `FORESTNAME`, `OBJECTID`, and geometry. [PRIMARY SOURCE](https://data.fs.usda.gov/geodata/edw/edw_resources/meta/S_USA.BasicOwnership.xml)
- GEOGRAPHY/SCALE: National Forest System lands and related national coverage. The Basic Ownership map service is displayed at broad mapping scales and is intended for general mapping and analysis. [PRIMARY SOURCE](https://apps.fs.usda.gov/arcx/rest/services/EDW/EDW_BasicOwnership_01/MapServer?f=pjson)
- ENDPOINT URL: [USFS Basic Ownership MapServer](https://apps.fs.usda.gov/arcx/rest/services/EDW/EDW_BasicOwnership_01/MapServer) · [Basic Ownership metadata](https://data.fs.usda.gov/geodata/edw/edw_resources/meta/S_USA.BasicOwnership.xml)
- LICENCE/TERMS: [PRIMARY SOURCE] The Forest Service states that the data are intended for read-only use and that its maps “are not legal documents.” [Basic Ownership metadata](https://data.fs.usda.gov/geodata/edw/edw_resources/meta/S_USA.BasicOwnership.xml)
- UPDATE CADENCE: [PRIMARY SOURCE] The metadata says the data are dynamic and current to the date of publication. [UNKNOWN] A universal fixed refresh interval was not established.
- STABLE IDENTIFIER: `BASICOWNERSHIPID` exists. [UNKNOWN] Stability across national refreshes is not promised.
- WHAT IT DOES NOT ESTABLISH: It does not establish title, legal descriptions, exact legal boundaries, restrictions, public access, or permission for activities. [PRIMARY SOURCE](https://apps.fs.usda.gov/arcx/rest/services/EDW/EDW_BasicOwnership_01/MapServer?f=pjson)

#### Surface Ownership

- PUBLISHER: USDA Forest Service.
- WHAT IT CONTAINS: Transaction-level surface-ownership parcels. Retrieved fields include `SURFACEOWNERSHIPID`, `CASENAME`, `LOCALCASEID`, `OWNERCLASSIFICATION`, `STATUSMETHOD`, `STATUS`, `RECORDEDACRES`, `GIS_ACRES`, `PILT_IND`, `PAYMENTTYPE`, `ACTIONDATE`, `ACTIONFISCALYEAR`, `ACTIONCALYEAR`, `COMMENTS`, `REGION`, `NFS_LANDUNIT_FKA`, `LANDSTATUSCASEID`, `FISCALLANDTYPE`, `MISSIONDEPENDENCY`, `PREDOMINANTUSE`, `HISTORICALSTATUS`, and `NFSLANDUNITNAME`. [PRIMARY SOURCE](https://data.fs.usda.gov/geodata/edw/edw_resources/meta/S_USA.SurfaceOwnership.xml)
- GEOGRAPHY/SCALE: National Forest System surface-estate parcels, with more detail than Basic Ownership. [PRIMARY SOURCE](https://apps.fs.usda.gov/arcx/rest/services/EDW/EDW_SurfaceOwnership_01/MapServer?f=pjson)
- ENDPOINT URL: [USFS Surface Ownership MapServer](https://apps.fs.usda.gov/arcx/rest/services/EDW/EDW_SurfaceOwnership_01/MapServer) · [Surface Ownership metadata](https://data.fs.usda.gov/geodata/edw/edw_resources/meta/S_USA.SurfaceOwnership.xml)
- LICENCE/TERMS: [PRIMARY SOURCE] Read-only use and no-warranty/legal-document limitations apply. [PRIMARY SOURCE](https://data.fs.usda.gov/geodata/edw/edw_resources/meta/S_USA.SurfaceOwnership.xml)
- UPDATE CADENCE: [PRIMARY SOURCE] The national dataset page listed a Surface Ownership refresh of October 4, 2026. [USFS national datasets](https://data.fs.usda.gov/geodata/edw/datasets.php?dsetCategory=boundaries)
- STABLE IDENTIFIER: `SURFACEOWNERSHIPID` is a source GUID; `LOCALCASEID`, `LANDSTATUSCASEID`, and `NFS_LANDUNIT_FKA` also exist. [PRIMARY SOURCE](https://data.fs.usda.gov/geodata/edw/edw_resources/meta/S_USA.SurfaceOwnership.xml)
- WHAT IT DOES NOT ESTABLISH: Ownership records do not establish public recreation permission, camping permission, route legality, or overnight use. [PRIMARY SOURCE](https://data.fs.usda.gov/geodata/edw/edw_resources/meta/S_USA.SurfaceOwnership.xml)

#### Administrative Forest boundaries

- PUBLISHER: USDA Forest Service.
- WHAT IT CONTAINS: Administrative Forest polygons. Retrieved fields include `ADMINFORESTID`, `REGION`, `FORESTNUMBER`, `FORESTORGCODE`, `FORESTNAME`, and `GIS_ACRES`. [PRIMARY SOURCE](https://data.fs.usda.gov/geodata/edw/edw_resources/meta/BdyAdm_LSRS_AdministrativeForest.xml)
- GEOGRAPHY/SCALE: National administrative-forest areas. The boundary can include private lands and other government lands. [PRIMARY SOURCE](https://apps.fs.usda.gov/arcx/rest/services/EDW/EDW_ForestSystemBoundaries_01/MapServer?f=pjson)
- ENDPOINT URL: [USFS Administrative Forest MapServer](https://apps.fs.usda.gov/arcx/rest/services/EDW/EDW_ForestSystemBoundaries_01/MapServer) · [Administrative Forest metadata](https://data.fs.usda.gov/geodata/edw/edw_resources/meta/BdyAdm_LSRS_AdministrativeForest.xml)
- LICENCE/TERMS: [PRIMARY SOURCE] The data are intended for read-only use and are not legal boundaries. [PRIMARY SOURCE](https://data.fs.usda.gov/geodata/edw/edw_resources/meta/BdyAdm_LSRS_AdministrativeForest.xml)
- UPDATE CADENCE: [PRIMARY SOURCE] The national dataset page lists a refresh of October 4, 2026. [USFS national datasets](https://data.fs.usda.gov/geodata/edw/datasets.php?dsetCategory=boundaries)
- STABLE IDENTIFIER: `ADMINFORESTID` exists. [UNKNOWN] The metadata does not promise persistence across edits.
- WHAT IT DOES NOT ESTABLISH: It does not establish ownership. It does not establish public access or permission. The Forest Service explicitly says administrative boundaries can encompass private lands and that ownership layers should be reviewed for federally managed parcels. [PRIMARY SOURCE](https://data.fs.usda.gov/geodata/edw/edw_resources/meta/BdyAdm_LSRS_AdministrativeForest.xml)

#### Wilderness

- PUBLISHER: USDA Forest Service.
- WHAT IT CONTAINS: Wilderness-area legal-status polygons and associated administrative tables. [PRIMARY SOURCE](https://apps.fs.usda.gov/arcx/rest/services/EDW/EDW_WildernessStatus_01/MapServer?f=pjson)
- GEOGRAPHY/SCALE: National Forest Service wilderness areas. [PRIMARY SOURCE](https://apps.fs.usda.gov/arcx/rest/services/EDW/EDW_WildernessStatus_01/MapServer?f=pjson)
- ENDPOINT URL: [USFS Wilderness Legal Status MapServer](https://apps.fs.usda.gov/arcx/rest/services/EDW/EDW_WildernessStatus_01/MapServer)
- REAL FIELD NAMES: [UNKNOWN] The retrieved service metadata exposed the layer and related table names but the wilderness feature schema was not successfully retrieved.
- LICENCE/TERMS: [PRIMARY SOURCE] USFS read-only and no-warranty limitations apply to the national data program. [USFS national datasets](https://data.fs.usda.gov/geodata/edw/datasets.php?dsetCategory=boundaries)
- UPDATE CADENCE: [PRIMARY SOURCE] The national dataset page lists the Wilderness Areas: Legal Status refresh as October 4, 2026. [USFS national datasets](https://data.fs.usda.gov/geodata/edw/datasets.php?dsetCategory=boundaries)
- STABLE IDENTIFIER: [UNKNOWN]
- WHAT IT DOES NOT ESTABLISH: Wilderness status establishes a designation and restriction context, not a blanket statement that every activity or overnight use is allowed. The applicable forest order, wilderness regulations, site rules, and current restrictions remain necessary. [PRIMARY SOURCE](https://apps.fs.usda.gov/arcx/rest/services/EDW/EDW_WildernessStatus_01/MapServer?f=pjson)

### 8. Pitkin County open space, easements, and parcels

- PUBLISHER: Pitkin County GIS, Pitkin County Open Space and Trails, and City of Aspen Parks Department for relevant layers.
- WHAT IT CONTAINS:
  - `Open Spaces` polygons with fields exposed or referenced by the service including `type`, `name`, and `planningarea`; the layer description says attributes include ownership, year acquired, property restriction, and managing agency. [PRIMARY SOURCE](https://maps.pitkincounty.com/arcgis/rest/services/Hosted/Open_Spaces/MapServer/101?f=pjson)
  - `Open Space Easement` polygons with `ease_holder`, `acres`, `year`, `parcel`, `name`, `ownership`, `comment`, `short_owner`, `owner_type`, `recept_no`, `fund_partner`, `public_access`, `maintainer`, `co_holder`, `last_edited_date`, `created_date`, `recept_date`, and `globalid`. [PRIMARY SOURCE](https://maps.pitkincounty.com/arcgis/rest/services/Hosted/Open_Space_Easement/FeatureServer/3?f=pjson)
  - Parcel polygons with `parcel`, `pin`, `accountnumber`, `owner_name`, `legal`, `situs_address`, `platted_acres`, `mapped_acres`, `globalid`, and related assessor fields. [PRIMARY SOURCE](https://maps.pitkincounty.com/arcgis/rest/services/Hosted/Parcel_Boundary/MapServer/0?f=pjson)
- GEOGRAPHY/SCALE: Pitkin County and the Aspen-area open-space system; parcel service extent is countywide. The open-space service title identifies a 2025-08-27 republication, but no universal scale specification was retrieved. [PRIMARY SOURCE](https://maps.pitkincounty.com/arcgis/rest/services/Hosted/Open_Spaces/MapServer?f=pjson)
- ENDPOINT URL: [Pitkin parcels](https://maps.pitkincounty.com/arcgis/rest/services/Hosted/Parcel_Boundary/MapServer/0) · [Pitkin open spaces](https://maps.pitkincounty.com/arcgis/rest/services/Hosted/Open_Spaces/MapServer/101) · [Pitkin open-space easements](https://maps.pitkincounty.com/arcgis/rest/services/Hosted/Open_Space_Easement/FeatureServer/3)
- LICENCE/TERMS: [UNKNOWN] The retrieved service metadata provides copyright and disclaimers but not a general redistribution licence. Pitkin states that parcel linework is approximate and not a licensed surveyed legal land record. [PRIMARY SOURCE](https://maps.pitkincounty.com/arcgis/rest/services/Hosted/Parcel_Boundary/MapServer/0?f=pjson)
- UPDATE CADENCE: [PRIMARY SOURCE] Pitkin states that recorded property changes may take up to 60 days to become public. [Pitkin parcel disclaimer search result](https://pitkincounty.com/478/Disclaimer) [UNKNOWN] Open-space and easement refresh cadence was not retrieved.
- STABLE IDENTIFIER: Parcel `globalid` and `parcel`/`pin` fields exist; easement `globalid` and `parcel` fields exist. [PRIMARY SOURCE](https://maps.pitkincounty.com/arcgis/rest/services/Hosted/Parcel_Boundary/MapServer/0?f=pjson) · [PRIMARY SOURCE](https://maps.pitkincounty.com/arcgis/rest/services/Hosted/Open_Space_Easement/FeatureServer/3?f=pjson)
- WHAT IT DOES NOT ESTABLISH: The `public_access` field is evidence that the county maintains an access-related attribute, not by itself a permission sentence for a chosen activity. Parcel ownership, open-space classification, easement holder, managing agency, or property restriction does not establish camping, overnight use, or access from a particular route.

### 9. Douglas County open space and parcel services

- PUBLISHER: Douglas County, Colorado GIS and Assessor offices.
- WHAT IT CONTAINS:
  - Parcel services with layers named `BOUNDARY`, `CONSERVATION_EASEMENTS`, `PARCELS_HISTORY`, `TAXDISTRICT_CHANGES`, `PARCELS`, `TAXDISTRICT`, and `SUBDIVISION`. [PRIMARY SOURCE](https://apps.douglas.co.us/gisod/rest/services/Parcels/FeatureServer?f=pjson)
  - Assessor downloads with fields including `Account_No`, `Owner_Name`, `State_Parcel_No`, `Total_Net_Acres`, `Legal_Descr`, `Sale_Date`, `Sale_Price`, `Grantor`, `Grantee`, `Recording_No`, `Actual_Value`, `Assessed_Value`, and related property fields. [PRIMARY SOURCE](https://www.douglasco.gov/assessor/data-downloads/)
  - GIS-derived layers including `OPEN_SPACE`, `LANDUSE_AREAS`, `CONSERVATION_EASEMENTS`, and parcel layers. [PRIMARY SOURCE](https://apps.douglas.co.us/gisod/rest/services/Landuse/FeatureServer?f=pjson) · [PRIMARY SOURCE](https://apps.douglas.co.us/gisod/rest/services/Parcels/FeatureServer?f=pjson)
- GEOGRAPHY/SCALE: Douglas County, Colorado. The services use Colorado State Plane feet; a fixed cartographic scale was not retrieved. [PRIMARY SOURCE](https://apps.douglas.co.us/gisod/rest/services/Parcels/FeatureServer?f=pjson)
- ENDPOINT URL: [Douglas parcel FeatureServer](https://apps.douglas.co.us/gisod/rest/services/Parcels/FeatureServer) · [Douglas land-use FeatureServer](https://apps.douglas.co.us/gisod/rest/services/Landuse/FeatureServer) · [Douglas GIS/open-data portal](https://dcdata-dougco.opendata.arcgis.com/)
- LICENCE/TERMS: [PRIMARY SOURCE] Douglas County’s policy says digital data requests may be subject to a separate contract or leasing agreement and that the county makes no guarantee of accuracy or completeness. [Douglas County GIS data policy](https://www.douglasco.gov/documents/gis-data.pdf/)
- UPDATE CADENCE: [PRIMARY SOURCE] Assessor downloads state “Last Updated: 10/1/2026” and “Next Update: 11/2/2026.” [Douglas County Assessor downloads](https://www.douglasco.gov/assessor/data-downloads/) [UNKNOWN] The GIS service refresh cadence was not retrieved.
- STABLE IDENTIFIER: `Account_No` and `State_Parcel_No` are assessor identifiers; service schemas also expose `GLOBALID` and `BOUNDARY_EID` for relevant layers. [PRIMARY SOURCE](https://www.douglasco.gov/assessor/data-downloads/) · [PRIMARY SOURCE](https://apps.douglas.co.us/gisod/rest/services/Parcels/FeatureServer/0?f=pjson)
- PUBLIC ACCESS: [PRIMARY SOURCE] Douglas County’s open-space page distinguishes public and limited-access properties and states that organized use requires permitting. It also identifies at least one open-space property as special-event-permit-only. [Douglas County open-space properties](https://www.douglasco.gov/open-space-natural-resources/properties/)
- RESTRICTION: [PRIMARY SOURCE] A Douglas County protected-land map warns, “Properties shown do not indicate public access.” [Douglas County protected-land map](https://www.douglasco.gov/documents/open-space-and-protected-lands.pdf/)
- WHAT IT DOES NOT ESTABLISH: Parcel ownership, conservation-easement geometry, open-space status, or a trail/open-space polygon does not establish general access, a chosen activity, camping, or overnight use.

### 10. Colorado statewide public parcels — OIT

- PUBLISHER: Colorado Governor’s Office of Information Technology GIS Team, using county, municipal, and regional government sources.
- WHAT IT CONTAINS: Statewide parcel polygons with `OBJECTID`, `sharing`, `countyName`, `countyFips`, `parcel_id`, `account`, `situsAdd`, `sitAddCty`, `sitAddZip`, `owner`, `owner2`, `ownerAdd`, `legalDesc`, `landSqft`, `landAcres`, `subCode`, `subName`, `zoningCode`, `zoningDesc`, `landUseCde`, `landUseDsc`, `saleDate`, `salePrice`, `apprValTot`, `asedValTot`, `URL`, and `dateReceived`. [PRIMARY SOURCE](https://gis.colorado.gov/public/rest/services/Address_and_Parcel/Colorado_Public_Parcels/FeatureServer/0?f=pjson)
- GEOGRAPHY/SCALE: Colorado statewide, aggregated from county and local sources. The item metadata specifies a display range from 1:500,000 to 1:5,000. [PRIMARY SOURCE](https://gis.colorado.gov/public/rest/services/Address_and_Parcel/Colorado_Public_Parcels/FeatureServer/0/iteminfo?f=pjson)
- ENDPOINT URL: [OIT Colorado Public Parcels FeatureServer](https://gis.colorado.gov/public/rest/services/Address_and_Parcel/Colorado_Public_Parcels/FeatureServer/0) · [service metadata](https://gis.colorado.gov/public/rest/services/Address_and_Parcel/Colorado_Public_Parcels/FeatureServer?f=pjson)
- LICENCE/TERMS: [PRIMARY SOURCE] Commercial use is allowed with attribution, but “Resale of this data is strictly forbidden.” OIT provides a sufficient attribution statement in the service metadata. [PRIMARY SOURCE](https://gis.colorado.gov/public/rest/services/Address_and_Parcel/Colorado_Public_Parcels/FeatureServer?f=pjson)
- UPDATE CADENCE: [PRIMARY SOURCE] Updates are collected annually. [OIT item metadata](https://gis.colorado.gov/public/rest/services/Address_and_Parcel/Colorado_Public_Parcels/FeatureServer/0/iteminfo?f=pjson)
- STABLE IDENTIFIER: `parcel_id` and `account` are source identifiers; `OBJECTID` is service-generated. [UNKNOWN] The retrieved metadata does not establish a statewide immutable identifier across annual composites.
- WHAT IT DOES NOT ESTABLISH: Owner attributes are not permission attributes. The statewide composite does not establish public access, activity permission, camping, overnight use, route legality, or current title. OIT directs errors to the relevant county authority. [PRIMARY SOURCE](https://gis.colorado.gov/public/rest/services/Address_and_Parcel/Colorado_Public_Parcels/FeatureServer?f=pjson)

### 11. Commercial parcel sources and alternatives

#### Regrid

- PUBLISHER: Regrid / Loveland Technologies.
- WHAT IT CONTAINS: Nationwide parcel geometry and related owner, situs-address, mailing-address, parcel-ID, land-use, and property-context data. Regrid advertises a persistent Regrid UUID. [PRIMARY SOURCE](https://support.regrid.com/docs/general-faqs)
- GEOGRAPHY/SCALE: Nationwide, state, and county delivery; formats include Shapefile, GeoPackage, GeoJSON, CSV, SQL, Parquet, API, and Esri-compatible Feature Service. [PRIMARY SOURCE](https://regrid.com/nationwide-parcels)
- ENDPOINT URL: [Regrid Data Store](https://app.regrid.com/store) · [Regrid license](https://app.regrid.com/store/license) · [Regrid nationwide parcels](https://regrid.com/nationwide-parcels)
- LICENCE/TERMS: [PRIMARY SOURCE] The standard store licence is nonexclusive and non-transferable; it requires credit and prohibits resale, sublicensing, or “otherwise making the Data available to third parties.” It permits rendering high-resolution parcel polygons only in a manner that reasonably prevents customers from obtaining a substantial copy. [Regrid Data Store License](https://app.regrid.com/store/license)
- UPDATE CADENCE: [PRIMARY SOURCE] A store purchase is a one-time export with no further updates; the broader Regrid product page advertises continuously refreshed products. These are different delivery models. [Regrid Data Store License](https://app.regrid.com/store/license) · [Regrid nationwide parcels](https://regrid.com/nationwide-parcels)
- STABLE IDENTIFIER: Regrid advertises a persistent Regrid UUID. [PRIMARY SOURCE](https://support.regrid.com/docs/general-faqs)
- WHAT IT DOES NOT ESTABLISH: Parcel data does not establish public access, activity permission, camping, or overnight use.
- OHVERNIGHT FIT: [INFERENCE] The standard store licence is not a safe fit for redistributing parcel data in an open-source static site. A custom enterprise licence would be needed if the site displays or caches substantial parcel geometry or attributes.

#### ReportAll

- PUBLISHER: ReportAll USA.
- WHAT IT CONTAINS: A national parcel layer with parcel boundaries and property attributes; the publisher advertises downloadable GIS formats and enterprise licensing. [PRIMARY SOURCE](https://reportallusa.com/products/national-parcel-layer)
- GEOGRAPHY/SCALE: The retrieved publisher page advertises coverage of 3,230 U.S. counties and multiple export formats. [PRIMARY SOURCE](https://reportallusa.com/products/national-parcel-layer)
- ENDPOINT URL: [ReportAll National Parcel Layer](https://reportallusa.com/products/national-parcel-layer) · [ReportAll parcel data](https://reportallusa.com/our-parcel-data)
- LICENCE/TERMS: [UNKNOWN] The retrieved material describes enterprise, API, feature-service, and reseller options but did not expose the public-static-site licence text.
- UPDATE CADENCE: [PRIMARY SOURCE] The publisher advertises that 90% of properties were updated in the previous 12 months and 70% within six months. [ReportAll National Parcel Layer](https://reportallusa.com/products/national-parcel-layer)
- STABLE IDENTIFIER: [UNKNOWN]
- WHAT IT DOES NOT ESTABLISH: Parcel coverage and ownership attributes do not establish recreation access or permission.
- OHVERNIGHT FIT: [INFERENCE] Do not ingest or redistribute without a written licence covering static-site display, caching, open-source distribution, attribution, and derivative data.

#### LightBox and CoreLogic

- PUBLISHERS: LightBox and CoreLogic.
- WHAT THEY CONTAIN: Commercial parcel/property data products are advertised by their respective publishers. [PRIMARY SOURCE](https://lightboxre.com/data/parcel-data) · [PRIMARY SOURCE](https://www.corelogic.com/intelligence/parcel-data/)
- LICENCE/TERMS: [UNKNOWN] The retrieved publisher pages did not load in this session. No public-static-site licence conclusion is supported.
- OHVERNIGHT FIT: [INFERENCE] Treat as commercially licensed and unsuitable for ingestion until the exact contract is reviewed.

#### County-direct alternatives

- PUBLISHERS: County assessor and GIS offices.
- WHAT THEY CONTAIN: Local parcel, ownership, conservation-easement, open-space, and land-use records, depending on county.
- LICENCE/TERMS: [PRIMARY SOURCE] County-direct terms vary. Douglas County states that digital requests may require a separate contract or leasing agreement. [Douglas County GIS policy](https://www.douglasco.gov/documents/gis-data.pdf/) [UNKNOWN] Pitkin County’s retrieved service metadata did not provide a general redistribution grant.
- OHVERNIGHT FIT: [INFERENCE] County-direct sources are preferable for local currency and authority, but each county’s exact licence, update schedule, field sensitivity, and redistribution terms must be recorded separately.

### 12. Datasets that state public access specifically

#### BLM Public Lands Access Data

- PUBLISHER: Bureau of Land Management.
- WHAT IT CONTAINS: Legal public-access locations to BLM-managed public lands through acquired easements and patent-reserved access rights; lines and polygons are available. [PRIMARY SOURCE](https://www.blm.gov/programs/recreation/recreation-programs/travel-and-transportation/public-lands-access-data)
- ENDPOINT URL: [BLM PLAD page](https://www.blm.gov/programs/recreation/recreation-programs/travel-and-transportation/public-lands-access-data) · [PLAD polygon service](https://services1.arcgis.com/KbxwQRRfWyEYLgp4/arcgis/rest/services/BLM_Natl_PLAD_Poly/FeatureServer/1)
- LICENCE/TERMS: [UNKNOWN] The retrieved page establishes the purpose and legal-access content, but not a complete redistribution licence.
- UPDATE CADENCE: [PRIMARY SOURCE] BLM describes PLAD as a living dataset updated as records are refined and new access is acquired. [PRIMARY SOURCE](https://www.blm.gov/programs/recreation/recreation-programs/travel-and-transportation/public-lands-access-data)
- STABLE IDENTIFIER: [UNKNOWN] The polygon schema was not successfully retrieved.
- WHAT IT ESTABLISHES: [PRIMARY SOURCE] It can support a legal-access claim to reach BLM land where the mapped easement or reservation applies.
- WHAT IT DOES NOT ESTABLISH: BLM warns that mapped access “does not allow for use of the non-BLM lands crossed.” It also does not establish permission for activities on BLM land after arrival. [PRIMARY SOURCE](https://www.blm.gov/programs/recreation/recreation-programs/travel-and-transportation/public-lands-access-data)

#### CPW Walk-In Access

- [PRIMARY SOURCE] CPW states that WIA properties are open only during program-specific dates, require program compliance, and are accessed on foot for hunting. [CPW WIA](https://cpw.state.co.us/activities/hunting/where-hunt/walk-access-program)
- [PRIMARY SOURCE] A WIA atlas polygon without boundary signs is not sufficient: CPW says a property must be posted with WIA boundary signs to be open to hunting. [CPW WIA](https://cpw.state.co.us/activities/hunting/where-hunt/walk-access-program)
- [PRIMARY SOURCE] WIA is not a general recreation or overnight dataset. CPW states that all activities other than hunting are prohibited on WIA properties. [CPW WIA](https://cpw.state.co.us/activities/hunting/where-hunt/walk-access-program)

#### State Trust Land Hunting and Fishing Access Program

- [PRIMARY SOURCE] The State Land Board and CPW identify enrolled trust lands with seasonal or limited hunting and fishing access. [State Land Board public access](https://slb.colorado.gov/public-access) · [CPW State Trust Land Finder](https://cpw.state.co.us/stl-finder)
- [PRIMARY SOURCE] Trust-land access is property-specific, seasonal, and rule-bound. CPW states that signs at individual properties describe allowed uses, rules, and time frames. [CPW State Trust Land Finder](https://cpw.state.co.us/stl-finder)
- [PRIMARY SOURCE] The program does not establish general camping or overnight permission. The State Land Board states that other recreational uses are prohibited unless posted. [State Land Board public access](https://slb.colorado.gov/public-access)

#### Conservation easements and access attributes

- [PRIMARY SOURCE] PAD-US includes conservation easements and a `Pub_Access` category, but the category is generalized and often categorical. [PAD-US Overview](https://www.usgs.gov/programs/gap-analysis-project/science/pad-us-data-overview)
- [PRIMARY SOURCE] COMaP includes public-access information and a `PUBLIC_ACCESS` field for map-service use, but its terms state that viewing the data creates no right to access protected lands. [COMaP terms](https://comap.cnhp.colostate.edu/terms-of-use/)
- [PRIMARY SOURCE] Pitkin County’s easement layer contains `public_access`, but the field is an attribute and not itself a permission sentence for every activity. [Pitkin easement service](https://maps.pitkincounty.com/arcgis/rest/services/Hosted/Open_Space_Easement/FeatureServer/3?f=pjson)
- [UNKNOWN] No retrieved statewide Colorado conservation-easement dataset was found that independently establishes general public recreation access across all easements. A conservation easement can restrict development without granting public entry; the easement instrument and holder’s current rules are needed.

## Ownership versus management versus access

- [PRIMARY SOURCE] Ownership answers who holds a fee or surface estate interest. USFS Surface Ownership and OIT/county parcel data are ownership-oriented. [USFS Surface Ownership metadata](https://data.fs.usda.gov/geodata/edw/edw_resources/meta/S_USA.SurfaceOwnership.xml) · [OIT Colorado parcels](https://gis.colorado.gov/public/rest/services/Address_and_Parcel/Colorado_Public_Parcels/FeatureServer/0?f=pjson)
- [PRIMARY SOURCE] Management answers which agency administers or manages a surface area. BLM SMA and USFS Administrative Forest boundaries are management or administrative datasets. [BLM National SMA](https://gis.blm.gov/arcgis/rest/services/lands/BLM_Natl_SMA_LimitedScale/MapServer?f=pjson) · [USFS Administrative Forest metadata](https://data.fs.usda.gov/geodata/edw/edw_resources/meta/BdyAdm_LSRS_AdministrativeForest.xml)
- [PRIMARY SOURCE] Access answers whether, when, how, and under what conditions the public may enter or perform a specified activity. CPW WIA rules, State Land Board leases, BLM PLAD access rights, and agency-specific property pages are access evidence. [CPW WIA](https://cpw.state.co.us/activities/hunting/where-hunt/walk-access-program) · [State Land Board recreation](https://slb.colorado.gov/lease/recreation) · [BLM PLAD](https://www.blm.gov/programs/recreation/recreation-programs/travel-and-transportation/public-lands-access-data)
- [INFERENCE] A polygon can be owned by one party, managed by another, and accessible only under a third party’s lease or easement. This is directly illustrated by State Land Board trust lands leased to CPW and by conservation easements included in PAD-US and COMaP. [State Land Board public access](https://slb.colorado.gov/public-access) · [PAD-US Overview](https://www.usgs.gov/programs/gap-analysis-project/science/pad-us-data-overview) · [COMaP terms](https://comap.cnhp.colostate.edu/terms-of-use/)
- [PRIMARY SOURCE] USFS warns that an Administrative Forest boundary can include private lands and other government lands, while ownership layers represent parcels tied to legal transactions. [USFS Administrative Forest metadata](https://data.fs.usda.gov/geodata/edw/edw_resources/meta/BdyAdm_LSRS_AdministrativeForest.xml)
- [PRIMARY SOURCE] BLM says SMA does not show land-status ownership patterns. [BLM National SMA](https://gis.blm.gov/arcgis/rest/services/lands/BLM_Natl_SMA_LimitedScale/MapServer?f=pjson)
- [INFERENCE] Apparent disagreements between sources are expected where they use different concepts, source dates, scales, overlays, or update cycles. They should not be resolved by silently choosing the most permissive layer.
- [INFERENCE] Recommended precedence for an access claim: current restriction or closure; agency/operator rule page; current lease, permit, or easement; access-specific agency dataset; ownership/management context; generalized protected-area or map layer. This ordering follows the sources’ own warnings that agencies are authoritative for their lands and that generalized data do not create access rights. [PAD-US Overview](https://www.usgs.gov/programs/gap-analysis-project/science/pad-us-data-overview) · [COMaP terms](https://comap.cnhp.colostate.edu/terms-of-use/)

## Private and unknown land

- [PRIMARY SOURCE] The national BLM service contains a `Private or Unknown` display class. [BLM national SMA layers](https://gis.blm.gov/arcgis/rest/services/lands/BLM_Natl_SMA_Cached_with_PriUnk/MapServer/layers?f=pjson)
- [INFERENCE] `Private or Unknown` must be stored as two separate application meanings only if a parcel or authoritative ownership source supports the distinction. Otherwise the honest value is `unknown`.
- [INFERENCE] No public manager recorded does not prove private ownership, and private ownership does not prove that no public access easement exists.
- [PRIMARY SOURCE] State trust land demonstrates why “publicly owned” is not equivalent to “open to the public”: the State Land Board requires a lease, permit, or other authorization. [State Land Board public access](https://slb.colorado.gov/public-access)
- [INFERENCE] Where no permission sentence, current lease, permit, access easement, or activity-specific agency rule was retrieved, Ohvernight should display `unknown`, not `allowed` and not `prohibited`.
- [INFERENCE] “Unknown” should also cover missing route legality, missing current restrictions, unresolved inholdings, conflicting source geometries, and access that is seasonally or permit-dependent.

## Licensing concerns

- [PRIMARY SOURCE] PAD-US states that its data are suitable for public-domain distribution. [PAD-US Data Manual](https://www.usgs.gov/programs/gap-analysis-project/pad-us-data-manual)
- [PRIMARY SOURCE] BLM Colorado’s catalog record identifies that dataset as public domain, but the national BLM service’s exact licence text was not retrieved. Do not automatically generalize the Colorado catalog statement to every BLM product. [BLM Colorado catalog](https://catalog.data.gov/dataset/blm-colorado-surface-management-agency) · [BLM National SMA](https://gis.blm.gov/arcgis/rest/services/lands/BLM_Natl_SMA_LimitedScale/MapServer?f=pjson)
- [PRIMARY SOURCE] OIT allows commercial use with attribution but prohibits resale. [OIT Colorado parcels](https://gis.colorado.gov/public/rest/services/Address_and_Parcel/Colorado_Public_Parcels/FeatureServer?f=pjson)
- [PRIMARY SOURCE] COMaP prohibits redistribution and requires direct registration/download or special-use handling. [COMaP terms](https://comap.cnhp.colostate.edu/terms-of-use/)
- [PRIMARY SOURCE] Regrid prohibits making licensed data available to third parties, subject to its rendering exception. [Regrid license](https://app.regrid.com/store/license)
- [PRIMARY SOURCE] Douglas County may require a separate contract or leasing agreement for digital data. [Douglas County GIS policy](https://www.douglasco.gov/documents/gis-data.pdf/)
- [UNKNOWN] CPW, Pitkin County, State Land Board, and the retrieved national USFS service pages did not expose a complete public-static-site redistribution licence.
- [INFERENCE] An ArcGIS REST endpoint, downloadable shapefile, or public viewer is not by itself proof that Ohvernight may copy, cache, transform, redistribute, or serve the data.
- [INFERENCE] A static site can accidentally redistribute restricted data through vector tiles, downloadable GeoJSON, browser caches, source maps, API responses, or an open-source repository even if the visible map is only a small subset.
- [INFERENCE] A licence review must cover geometry, attributes, derived classifications, cached tiles, screenshots, attribution, update obligations, commercial use, open-source distribution, and whether users can recover a substantial portion of the source data.

## Questions an owner must decide

- [INFERENCE] Is M5 modeling ownership, management, public access, activity permission, or all four as separate claims?
- [INFERENCE] Will the schema distinguish `owner`, `manager`, `designation`, `access_status`, `activity_status`, `restriction`, `source_date`, `source_url`, and `evidence_text`?
- [INFERENCE] Will `allowed` require an agency/operator sentence that expressly permits the relevant activity, location, and time period?
- [INFERENCE] Will restrictions and closures override generalized access categories?
- [INFERENCE] Will `Pub_Access=Open` be displayed as “general access category” rather than “activity allowed”?
- [INFERENCE] Will overnight use be modeled separately from entry, hiking, hunting, fishing, camping, and vehicle access?
- [INFERENCE] Which source wins when BLM SMA, PAD-US, USFS, county parcels, and CPW boundaries disagree?
- [INFERENCE] Are private and unknown land displayed separately, and will the map avoid implying trespass?
- [INFERENCE] Are parcel owner names necessary for the product, or can Ohvernight use parcel geometry and a generalized ownership class?
- [INFERENCE] Will each polygon retain source dataset, source version, retrieval date, source identifier, and the exact current terms URL?
- [INFERENCE] Will M5 include BLM PLAD route/easement data separately from SMA management polygons?
- [INFERENCE] Will CPW WIA, CPW SWA, and State Trust Land access be treated as seasonal program overlays rather than permanent land categories?
- [INFERENCE] Will the application suppress a positive access label when the source says access is restricted, seasonal, permit-based, sign-dependent, or unknown?
- [INFERENCE] Which datasets are acceptable under Ohvernight’s open-source and static-hosting requirements without negotiated licences?
- [INFERENCE] What is the update SLA for each source, and how will stale access claims be removed?
- [INFERENCE] Will the product show “verify current rules with the managing agency” for every access-sensitive layer?

## Unknowns

- [UNKNOWN] The national BLM SMA redistribution licence was not established from the retrieved national service metadata.
- [UNKNOWN] Stable polygon identifiers for BLM SMA, PAD-US, COMaP, CPW, State Land Board, and wilderness layers were not established.
- [UNKNOWN] PAD-US’s current ArcGIS layer endpoint was temporarily unavailable during this session; use the DOI/download source until the service is rechecked.
- [UNKNOWN] PAD-US 4.1’s exact current polygon-ID field was not established from the retrieved material.
- [UNKNOWN] COMaP’s full terms page was not fully readable in this session because the publisher site presented a reCAPTCHA gate, although the publisher’s search result and brochure exposed the decisive terms.
- [UNKNOWN] CPW’s exact layer schemas and a general CPW GIS redistribution licence were not retrieved.
- [UNKNOWN] The State Land Board map application’s exact layer schemas, stable identifiers, and redistribution terms were not retrieved.
- [UNKNOWN] Pitkin County’s general redistribution licence and open-space/easement refresh schedule were not retrieved.
- [UNKNOWN] Douglas County’s exact open-space service endpoint and open-data licence were not retrieved; the portal itself did not extract successfully.
- [UNKNOWN] The exact licences for ReportAll, LightBox, and CoreLogic for a public open-source static site were not retrieved.
- [UNKNOWN] No statewide conservation-easement dataset retrieved in this session independently establishes general public recreation access across all easements.
- [UNKNOWN] No source retrieved here establishes overnight permission for a generalized land polygon without a location-specific agency/operator rule, lease, permit, or other permission document.

## Recommendation

Use separate M5 layers and claims rather than replacing the current manager layer with a single “public land” layer:

1. Use BLM Colorado SMA for management context, with a clear `management_only` label and the daily-update/source-scale caveat.
2. Use USFS Basic Ownership or Surface Ownership for Forest Service ownership context; use Administrative Forest only for administrative-unit labeling, never ownership.
3. Use PAD-US 4.1 as a national cross-agency context layer and expose `Pub_Access` as a generalized access category, never as automatic activity permission.
4. Keep CPW WIA, CPW SWA, State Trust Land access, and BLM PLAD as separate access-evidence layers with date, season, permit, sign, and activity restrictions.
5. Treat county parcel, open-space, and easement services as ownership or local-management context unless the county’s own page expressly states the relevant public activity and conditions.
6. Exclude COMaP from redistribution unless Ohvernight obtains and implements a compatible subscription or special-use licence.
7. Exclude Regrid and other commercial parcels unless a written licence permits the exact static-site, open-source, caching, attribution, and user-display model.
8. Make `unknown` the default whenever the source only shows ownership, management, designation, public access category, facility, trail, road, or map presence.
9. Require an agency/operator permission sentence before assigning `allowed`; store the sentence, URL, access date, season, permit condition, and activity scope with the claim.
10. For the Aspen and Douglas pilots, prioritize Pitkin/Douglas county-direct data, BLM Colorado SMA, USFS ownership/administrative layers, CPW access-specific layers, State Land Board lease/access records, and BLM PLAD. Do not use generalized ownership or management polygons to answer the overnight question by themselves.
