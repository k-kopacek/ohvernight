<!-- Hermes research report, M4 track B. Retrieved 2026-10-06 with web search and page reading only. This is a research INPUT, kept verbatim: it is not verified in the trust sense (ADR-004, ADR-005). The coordinator synthesis in ../recommendations.md states what was independently checked and where it disagrees. -->

# M4 Track B — Water semantics in real source schemas

**Access date:** 2026-10-06  
**Scope:** USGS NHD, NHDPlus High Resolution, and 3D Hydrography Program source schemas.  
**Status vocabulary:** **RETRIEVED** = read from the cited source today; **INFERRED** = reasoned from retrieved source facts; **UNKNOWN** = not established.

## Bottom line

**INFERRED:** Useful recreational-water candidates can be separated from hydrology clutter using source-backed physical and cartographic characteristics: feature class/type, detailed `FCode`, hydrographic category, reservoir purpose, polygon area, flowline length, stream order, drainage area, modeled mean annual flow, official-name presence, and map-scale visibility. These support candidate selection and ranking—not recreation or access claims. [NHD schema](https://www.usgs.gov/ngp-standards-and-specifications/national-hydrography-dataset-nhd-data-dictionary-feature-classes) [NHD domains](https://www.usgs.gov/ngp-standards-and-specifications/national-hydrography-dataset-nhd-data-dictionary-feature-domains) [NHDPlus HR layer 3](https://hydro.nationalmap.gov/arcgis/rest/services/NHDPlus_HR/MapServer/3?f=pjson)

**INFERRED:** None of the inspected NHD, NHDPlus HR, or 3DHP fields establishes public ownership, legal access, fishing, boating, swimming, parking, or camping permission. A feature’s existence, size, name, perennial status, or reservoir purpose is not evidence of any permission. [NHD flowline schema](https://hydro.nationalmap.gov/arcgis/rest/services/nhd/MapServer/6?f=pjson) [NHD waterbody schema](https://hydro.nationalmap.gov/arcgis/rest/services/nhd/MapServer/12?f=pjson) [3DHP flowline schema](https://hydro.nationalmap.gov/arcgis/rest/services/3DHP_all/MapServer/50?f=pjson) [3DHP waterbody schema](https://hydro.nationalmap.gov/arcgis/rest/services/3DHP_all/MapServer/60?f=pjson)

## Services and actual schemas

| Source | Actual service/layer | Retrieved schema characteristics |
|---|---|---|
| NHD | [Service](https://hydro.nationalmap.gov/arcgis/rest/services/nhd/MapServer?f=pjson); [6 Flowline](https://hydro.nationalmap.gov/arcgis/rest/services/nhd/MapServer/6?f=pjson) | **RETRIEVED:** Polyline fields include string `permanent_identifier` (40), `gnis_id` (10), `gnis_name` (65), double `lengthkm`, string `reachcode` (14), integer `ftype`, `fcode`, `visibilityfilter`, and waterbody-link field `wbarea_permanent_identifier`. |
| NHD | [9 Area](https://hydro.nationalmap.gov/arcgis/rest/services/nhd/MapServer/9?f=pjson) | **RETRIEVED:** Polygon fields include `PERMANENT_IDENTIFIER`, `GNIS_ID`, `GNIS_NAME`, double `AREASQKM`, `ELEVATION`, integer `FTYPE`, `FCODE`, and `VISIBILITYFILTER`; this published layer has no `REACHCODE`. |
| NHD | [12 Waterbody](https://hydro.nationalmap.gov/arcgis/rest/services/nhd/MapServer/12?f=pjson) | **RETRIEVED:** Polygon fields include those above plus string `REACHCODE`; coded subtypes are LakePond, Reservoir, SwampMarsh, Playa, Ice Mass, and Estuary. |
| NHDPlus HR | [Service](https://hydro.nationalmap.gov/arcgis/rest/services/NHDPlus_HR/MapServer?f=pjson); [3 NetworkNHDFlowline](https://hydro.nationalmap.gov/arcgis/rest/services/NHDPlus_HR/MapServer/3?f=pjson) | **RETRIEVED:** Carries the NHD identifiers and classifications plus `nhdplusid`, `streamorde`, `levelpathi`, `totdasqkm`, and flow-estimate fields including `qama`. The service identifies its data refresh as October 2022. |
| 3DHP | [Service](https://hydro.nationalmap.gov/arcgis/rest/services/3DHP_all/MapServer?f=pjson); [50 Flowline](https://hydro.nationalmap.gov/arcgis/rest/services/3DHP_all/MapServer/50?f=pjson); [60 Waterbody](https://hydro.nationalmap.gov/arcgis/rest/services/3DHP_all/MapServer/60?f=pjson) | **RETRIEVED:** Flowlines expose `id3dhp`, `mainstemid`, integer `gnisid`, `gnisidlabel`, `featuretype`, `featuretypelabel`, `lengthkm`, `waterbodyid3dhp`, `streamorder`, and `levelpath`. Waterbodies expose corresponding IDs, name fields, type fields, and `areasqkm`. The service says data were refreshed September 4, 2026. |

**RETRIEVED:** The 3DHP service exists at the real URL above and combines elevation-derived hydrography where available with NHD-derived content elsewhere; NHD content is to be replaced as elevation-derived data arrive. Its stated use constraints include: “**None. All data are open and non-proprietary.**” [3DHP service metadata](https://hydro.nationalmap.gov/arcgis/rest/services/3DHP_all/MapServer?f=pjson)

## Feature meaning that separates water from clutter

### Flowlines

**RETRIEVED:** NHD `FType` is a three-digit feature type; `FCode` is five digits, with the first three identifying the type and the final two encoding characteristics. Relevant flowline types are Connector 334, CanalDitch 336, Pipeline 428, StreamRiver 460, and ArtificialPath 558. StreamRiver is “Body of flowing water”; ArtificialPath is a modeling abstraction through waterbodies or along shorelines. [NHD feature-class dictionary](https://www.usgs.gov/ngp-standards-and-specifications/national-hydrography-dataset-nhd-data-dictionary-feature-classes)

**RETRIEVED:** StreamRiver codes distinguish unknown seasonality (`46000`), intermittent (`46003`), perennial (`46006`), and ephemeral (`46007`). Intermittent means water for part of the year but more than only after storms or snowmelt; perennial means throughout the year except infrequent severe drought; ephemeral means only during or after local rainstorms or heavy snowmelt. [NHD feature domains](https://www.usgs.gov/ngp-standards-and-specifications/national-hydrography-dataset-nhd-data-dictionary-feature-domains)

**INFERRED:** `46006` is stronger evidence of persistent physical water than `46003`, `46007`, or `46000`, but it says nothing about depth, width, fish, navigability, water quality, current conditions, or permission. Treat `46000` as unknown—not perennial—even though the service renderer groups it visually with perennial lines. [Layer 6 renderer and domains](https://hydro.nationalmap.gov/arcgis/rest/services/nhd/MapServer/6?f=pjson)

**RETRIEVED:** Connector is an unspecified network connection; CanalDitch is an artificial open waterway; Pipeline is a closed conduit. These are hydrologically meaningful but poor default recreational-water candidates. [NHD feature-class dictionary](https://www.usgs.gov/ngp-standards-and-specifications/national-hydrography-dataset-nhd-data-dictionary-feature-classes)

### Waterbodies

**RETRIEVED:** NHD waterbody `FType` values are Playa 361, Ice Mass 378, LakePond 390, Reservoir 436, SwampMarsh 466, and Estuary 493. LakePond is standing water with a predominantly natural shoreline; Reservoir is a constructed basin containing water or other liquids; Playa is an undrained desert-basin flat; SwampMarsh is vegetated land inundated or saturated for a significant part of the year. [NHD feature-class dictionary](https://www.usgs.gov/ngp-standards-and-specifications/national-hydrography-dataset-nhd-data-dictionary-feature-classes)

**RETRIEVED:** LakePond codes distinguish unknown (`39000`), intermittent (`39001`, `39005`, `39006`), and perennial (`39004`, `39009`–`39012`) conditions, sometimes with stage such as normal pool or spillway elevation. [Waterbody layer metadata](https://hydro.nationalmap.gov/arcgis/rest/services/nhd/MapServer/12?f=pjson)

**RETRIEVED:** Reservoir `FCode` values distinguish aquaculture (`43601`), decorative pool, tailings pond (`43604`/`43605`), disposal, evaporator (`43607`/`43623`), swimming pool, cooling, filtration, settling, sewage treatment, treatment (`43624`), and water storage (`43613`–`43617`, `43621`). [Waterbody layer metadata](https://hydro.nationalmap.gov/arcgis/rest/services/nhd/MapServer/12?f=pjson)

**INFERRED:** Tailings, disposal, evaporator, sewage-treatment, filtration, settling, treatment, cooling, decorative-pool, swimming-pool, and aquaculture codes are defensible exclusions from a general outdoor-recreation discovery layer. Water-storage reservoirs may remain candidates, but “water storage” does not imply recreation or public access. Unknown-purpose `43600` should remain unknown rather than being promoted. [Waterbody layer metadata](https://hydro.nationalmap.gov/arcgis/rest/services/nhd/MapServer/12?f=pjson)

## Names, identifiers, segmentation, and artificial paths

**RETRIEVED:** `GNIS_ID` is a permanent unique identifier for a GNIS name application, and is null when no name is associated; `GNIS_NAME` stores the proper name. `Permanent_Identifier` identifies an individual NHD feature occurrence. A 14-character `ReachCode` consists of an eight-digit HUC8 plus six digits unique within that HUC8 and is required for NHD flowlines. [NHD feature-class dictionary](https://www.usgs.gov/ngp-standards-and-specifications/national-hydrography-dataset-nhd-data-dictionary-feature-classes)

**RETRIEVED:** The NHDPlus guide calls ReachCode a permanent reach identifier, but NHD maintains reach-code cross-reference information over time. The VisibilityFilter documentation also records that editing can change a feature’s `Permanent_Identifier`. Therefore neither should be treated as an immutable geometry ID across arbitrary releases without versioning or crosswalks. [NHDPlus HR guide](https://pubs.usgs.gov/publication/sir20255031/full) [VisibilityFilter known issues](https://www.usgs.gov/national-hydrography/visibilityfilter)

**RETRIEVED:** A Roaring Fork River query returned more than 20 flowline records with one `gnis_id` (`00174812`) but many permanent identifiers and reach codes. Records included both perennial StreamRiver (`46006`) and ArtificialPath (`55800`) features. Artificial paths carried a common `wbarea_permanent_identifier` where they crossed a polygon. [Roaring Fork query](https://hydro.nationalmap.gov/arcgis/rest/services/nhd/MapServer/6/query?f=pjson&where=gnis_name%3D%27Roaring%20Fork%20River%27&outFields=permanent_identifier%2Cgnis_id%2Cgnis_name%2Clengthkm%2Creachcode%2Cftype%2Cfcode%2Cwbarea_permanent_identifier&returnGeometry=false&resultRecordCount=20)

**INFERRED:** Group by `GNIS_ID` to collect segments carrying the same official name application; use `ReachCode` for a reach, not the whole named river. In NHDPlus HR, `LevelPathI` identifies a modeled main-stem path and can group its component flowlines. It is not equivalent to the legal or vernacular extent of a named stream. [NHDPlus HR guide](https://pubs.usgs.gov/publication/sir20255031/full)

**RETRIEVED:** NHD artificial paths complete the network through waterbody/area polygons where no obvious channel exists; isolated waterbodies do not contain them. The cited rules are explicitly dated January 2011 and warn that they may differ from later update rules. [NHD feature rules](https://www.usgs.gov/ngp-standards-and-specifications/national-hydrography-data-set-feature-rules)

**RETRIEVED:** In current 3DHP, the Roaring Fork River sample contains many separate records sharing `gnisid` 174812, one `mainstemid` URL, and one `levelpath`; Waterbody Connector records have populated `waterbodyid3dhp`, while sampled Channel Line records do not. [3DHP Roaring Fork query](https://hydro.nationalmap.gov/arcgis/rest/services/3DHP_all/MapServer/50/query?f=pjson&where=gnisidlabel%3D%27Roaring%20Fork%20River%27&outFields=id3dhp%2Cmainstemid%2Cgnisid%2Cgnisidlabel%2Cfeaturetype%2Cfeaturetypelabel%2Clengthkm%2Cwaterbodyid3dhp%2Cstreamorder%2Clevelpath&returnGeometry=false&resultRecordCount=20)

## Size and ranking fields

**RETRIEVED:** NHD uses computed `LengthKM` for lines and `AreaSqKm` for polygons. NHDPlus HR adds modified-Strahler `StreamOrde`, total upstream drainage area `TotDASqKm`, `LevelPathI`, and `QAMA` (alias `FlowEstARunoffMA`, mean annual flow from runoff). The live service field is `qama`; no field literally named `QA_MA` appears in layer 3. [NHDPlus HR layer 3](https://hydro.nationalmap.gov/arcgis/rest/services/NHDPlus_HR/MapServer/3?f=pjson) [NHDPlus HR guide](https://pubs.usgs.gov/publication/sir20255031/full)

**RETRIEVED:** `VisibilityFilter` is a cartographic-generalization field indicating suitability at a scale and larger scales; values include 24,000 through 5,000,000, with queries such as `VisibilityFilter >= 250000`. USGS says the field is in testing and some zero values are incorrectly assigned. [VisibilityFilter documentation](https://www.usgs.gov/national-hydrography/visibilityfilter)

**RETRIEVED:** A Pitkin-area sample contained named and unnamed perennial LakePond polygons from 0 to about 0.008 square kilometers, with populated reach codes and VisibilityFilter values. Thus these fields are populated in at least this sample, but names are frequently null. [Pitkin waterbody query](https://hydro.nationalmap.gov/arcgis/rest/services/nhd/MapServer/12/query?f=pjson&where=1%3D1&geometry=-107.05%2C39.15%2C-106.75%2C39.3&geometryType=esriGeometryEnvelope&inSR=4326&spatialRel=esriSpatialRelIntersects&outFields=PERMANENT_IDENTIFIER%2CGNIS_ID%2CGNIS_NAME%2CAREASQKM%2CREACHCODE%2CFTYPE%2CFCODE%2CVISIBILITYFILTER&returnGeometry=false&resultRecordCount=20)

## Safe uses in an M4 selection rule

| Characteristic | Safe use | False-positive / false-negative risk |
|---|---|---|
| **Feature type / FCode** | **INFERRED:** Include LakePond and suitable StreamRiver; exclude connectors, pipelines, playas, ice, and industrial reservoir purposes. | A physical lake or river may still be private, inaccessible, hazardous, or non-recreational; exclusion can omit unusual legitimate recreation sites. [NHD domains](https://www.usgs.gov/ngp-standards-and-specifications/national-hydrography-dataset-nhd-data-dictionary-feature-domains) |
| **Hydrographic category** | **INFERRED:** Prefer perennial; down-rank intermittent; normally suppress ephemeral. | Perennial does not mean usable today; intermittent water can support seasonal recreation. Population is demonstrated in retrieved samples, not audited region-wide. [Layer 6](https://hydro.nationalmap.gov/arcgis/rest/services/nhd/MapServer/6?f=pjson) |
| **Reservoir purpose** | **INFERRED:** Exclude clearly industrial/treatment purposes; retain water-storage only as an unverified candidate. | Purpose may be unknown or miscoded; water storage can be closed, and some aquaculture facilities might offer controlled recreation. [Layer 12](https://hydro.nationalmap.gov/arcgis/rest/services/nhd/MapServer/12?f=pjson) |
| **Area / length** | **INFERRED:** Remove tiny polygons and line fragments, or rank larger features higher. | Small alpine lakes and short accessible reaches may be valuable; large features can be inaccessible. Threshold choice is a product decision, not source semantics. [NHD schema](https://www.usgs.gov/ngp-standards-and-specifications/national-hydrography-dataset-nhd-data-dictionary-feature-classes) |
| **Stream order / drainage area / QAMA** | **INFERRED:** Rank larger network channels; combine rather than using one field alone. | Headwater recreation can be lost; modeled annual flow does not establish current flow, depth, safety, or access. Actual M4-region population of NHDPlus `qama` is **UNKNOWN** because the live query timed out. [NHDPlus layer 3](https://hydro.nationalmap.gov/arcgis/rest/services/NHDPlus_HR/MapServer/3?f=pjson) |
| **Named status** | **INFERRED:** Use non-null GNIS name as a discoverability boost, never a permission signal or hard requirement. | Many real waterbodies are unnamed; official names can apply to inaccessible or unsuitable features. [NHD dictionary](https://www.usgs.gov/ngp-standards-and-specifications/national-hydrography-dataset-nhd-data-dictionary-feature-classes) |
| **VisibilityFilter** | **INFERRED:** Use only for display density or a weak prominence ranking. | It is not recreational significance, and known bad zero values can create omissions or network gaps. [VisibilityFilter](https://www.usgs.gov/national-hydrography/visibilityfilter) |

## 3DHP migration consequence

**RETRIEVED:** The NHD-to-3DHP crosswalk collapses LakePond and every Reservoir subtype into 3DHP `Lake`, and collapses perennial, intermittent, ephemeral, and unspecified StreamRiver into 3DHP `River`/current Channel Line. Pipeline and underground-conduit distinctions collapse into Hydro Unenforced Connector. [3DHP crosswalk](https://www.usgs.gov/ngp-standards-and-specifications/3d-hydrography-program-product-specification-crosswalk-tables)

**INFERRED:** Current 3DHP is useful for modern IDs, mainstem grouping, waterbody linkage, length/area, and available stream order. Its published schema cannot, by itself, reproduce the safer NHD rules based on hydrographic category or reservoir purpose. Preserve or separately join the original NHD `FCode` while transition coverage is mixed. [3DHP flowline schema](https://hydro.nationalmap.gov/arcgis/rest/services/3DHP_all/MapServer/50?f=pjson) [3DHP waterbody schema](https://hydro.nationalmap.gov/arcgis/rest/services/3DHP_all/MapServer/60?f=pjson)

## Unknowns and things I could not verify

- **UNKNOWN:** Region-wide completeness and non-null rates for every candidate field in Pitkin and Douglas Counties. Retrieved samples prove some population, not completeness.
- **UNKNOWN:** NHDPlus HR `streamorde`, `totdasqkm`, `levelpathi`, and `qama` population in the two pilot regions; two live service queries timed out. [NHDPlus query endpoint](https://hydro.nationalmap.gov/arcgis/rest/services/NHDPlus_HR/MapServer/3/query)
- **UNKNOWN:** Whether 3DHP’s current seven-character `id3dhp`, `levelpath`, or `mainstemid` has a documented long-term stability guarantee. The schema shows the fields and samples show population, but no retrieved page established an immutability policy. [3DHP layer 50](https://hydro.nationalmap.gov/arcgis/rest/services/3DHP_all/MapServer/50?f=pjson)
- **UNKNOWN:** Any public-access, ownership, fishing, boating, swimming, parking, camping, safety, or water-quality status for any retrieved feature. None of the inspected fields supplies those determinations.

## Recommendation

**INFERRED:** Build M4’s hydrology-side candidate filter from NHD/NHDPlus semantics, while treating 3DHP as a parallel migration source:

1. Start with NHD Waterbody LakePond and non-industrial Reservoir polygons plus NHD Flowline StreamRiver.
2. Exclude Pipeline, Connector, CanalDitch by default; retain ArtificialPath only for topology/grouping, not as a separate recreation feature.
3. Prefer explicit perennial codes; label unspecified and intermittent status honestly.
4. Exclude reservoir FCodes for treatment, sewage, filtration, settling, disposal, tailings, evaporator, cooling, decorative pool, swimming pool, and aquaculture from general discovery.
5. Apply conservative area, aggregate-length, stream-order, drainage-area, and flow rankings rather than asserting recreational suitability.
6. Deduplicate named streams with `GNIS_ID`, use `ReachCode` for reach identity, and use NHDPlus `LevelPathI` or 3DHP `mainstemid`/`levelpath` for modeled mainstem grouping.
7. Keep access and permission as separate evidence layers. Until authoritative access evidence is joined, every selected water feature must remain “physical water candidate; access and permitted activities unknown.”
