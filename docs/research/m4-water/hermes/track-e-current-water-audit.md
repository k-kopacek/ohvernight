<!-- Hermes research report, M4 track E. Retrieved 2026-10-06 with web search and page reading only. This is a research INPUT, kept verbatim: it is not verified in the trust sense (ADR-004, ADR-005). The coordinator synthesis in ../recommendations.md states what was independently checked and where it disagrees. -->

# M4 Functional Recreational Water — Current Ohvernight Water Audit

Access date: 2026-10-06

Scope: This audit uses the coordinator’s read-only computations from repository commit `b45ca59`, plus web research on selected named features and the underlying USGS service. A mapped water feature does not establish ownership, public access, fishing, boating, swimming, parking, or camping permission.

## 1. Quantified current display

The USGS NHD service describes its data as including naturally occurring and constructed water features such as “canals, ditches, streams, and rivers,” as well as lakes, ponds, and reservoirs. That breadth explains why the current display is a hydrography display rather than a recreational-water inventory. [RETRIEVED] [USGS NHD MapServer](https://hydro.nationalmap.gov/arcgis/rest/services/nhd/MapServer)

| Region and layer | Canonical features | Display features | Named / unnamed | Geometry types | Main fragmentation indicators |
|---|---:|---:|---|---|---|
| Aspen hydrology | 6,926 | 1,555 | Canonical: 1,555 named, 5,371 unnamed. Display: all 1,555 named | Canonical: 6,403 LineString, 8 MultiLineString, 515 Polygon. Display: 1,508 LineString, 4 MultiLineString, 43 Polygon | 134 distinct names; 93 names occur more than once and account for 1,514 features. Roaring Fork River has 112 pieces; Snowmass Creek 83; Castle Creek 78. |
| Douglas waterbodies | 33 | 33 | 33 named, 0 unnamed | 31 Polygon, 2 MultiPolygon | Every named waterbody is a separate feature; no repeated names in this layer. |
| Douglas waterways | 2,359 | 2,359 | 2,359 named, 0 unnamed | 2,348 LineString, 11 MultiLineString | 69 distinct names; 56 names occur more than once and account for 2,346 features. East Plum Creek has 183 pieces; Bear Creek 146; Jackson Creek 116. |

[RETRIEVED: coordinator-computed counts from committed artifacts; source service URLs: Aspen flowlines](https://hydro.nationalmap.gov/arcgis/rest/services/nhd/MapServer/6), [Aspen areas](https://hydro.nationalmap.gov/arcgis/rest/services/nhd/MapServer/9), [waterbodies and Douglas waterbodies](https://hydro.nationalmap.gov/arcgis/rest/services/nhd/MapServer/12)

Aspen’s display is 97.2% line features and 2.8% polygon features. The display contains approximately 661.9 km of named line pieces, with 730 line features shorter than 0.25 km. The median displayed line piece is approximately 0.265 km. [RETRIEVED: coordinator computation;](https://hydro.nationalmap.gov/arcgis/rest/services/nhd/MapServer/6)

Douglas’s combined display contains 2,392 features: 2,359 line pieces and 33 waterbody polygons or multipolygons. Approximately 777.9 km of waterways are displayed; 1,578 line pieces are shorter than 0.25 km, and the median piece is approximately 0.160 km. [RETRIEVED: coordinator computation;](https://hydro.nationalmap.gov/arcgis/rest/services/nhd/MapServer/6)

The fragmentation ratios are material:

- Aspen: 1,514 features across 93 repeated-name groups, or approximately 16.3 pieces per repeated name. [INFERRED from coordinator counts;](https://hydro.nationalmap.gov/arcgis/rest/services/nhd/MapServer/6)
- Douglas waterways: 2,346 features across 56 repeated-name groups, or approximately 41.9 pieces per repeated name. [INFERRED from coordinator counts;](https://hydro.nationalmap.gov/arcgis/rest/services/nhd/MapServer/6)
- Examples include 112 tappable Roaring Fork River pieces and 183 East Plum Creek pieces. A user selecting one stream receives a set of hydrologic fragments, not one recreational water object. [RETRIEVED: coordinator computation;](https://hydro.nationalmap.gov/arcgis/rest/services/nhd/MapServer/6)

## 2. Apparent recreation clutter versus useful water

The current display is not suitable for treating every feature as a recreational destination.

Aspen has 134 distinct displayed names, including 14 names containing “ditch” and three containing “canal.” Those 17 utility-channel names are a minimum count of apparent non-recreational or recreation-ambiguous groups; the number of individual pieces carrying those names was not supplied. [RETRIEVED: coordinator computation;](https://hydro.nationalmap.gov/arcgis/rest/services/nhd/MapServer/6)

Aspen also displays 43 named polygon features. The largest include Snowmass Lake, Wildcat Reservoir, Grizzly Reservoir, Willow Lake, Warren Lakes, Taylor Lake, Crater Lake, Cathedral Lake, and Maroon Lake. Polygon size alone does not establish access or recreation. [RETRIEVED: coordinator computation;](https://hydro.nationalmap.gov/arcgis/rest/services/nhd/MapServer/12)

Douglas waterbodies are especially vulnerable to false recreation signals: all 33 are named, 30 names contain “reservoir,” and five polygons are smaller than 0.5 hectares. Seven are smaller than two hectares. The dataset includes several features explicitly named as detention reservoirs, but the name is not proof of public access or a recreation program. [RETRIEVED: coordinator computation;](https://hydro.nationalmap.gov/arcgis/rest/services/nhd/MapServer/12)

Douglas waterways contain 15 distinct names with “ditch” and two with “canal.” Therefore, at least 17 of 69 distinct waterway names, or approximately 24.6%, are utility-channel names. The count of individual ditch and canal pieces is not available from the supplied summary. [INFERRED from coordinator counts;](https://hydro.nationalmap.gov/arcgis/rest/services/nhd/MapServer/6)

Estimate, by displayed feature count rather than water-surface area:

- Aspen: approximately 50–70% of displayed features are apparent recreation clutter or ambiguous hydrology. This is an INFERRED range, not a measured classification. The reasoning is that nearly all displayed objects are line fragments, about half of the displayed line pieces are under 250 m, 17 distinct names are ditch/canal names, and major streams are split into many pieces. The range could be too high if short stream sections are retained for scenic, fishing, or access context.
- Douglas: approximately 70–90% of displayed features are apparent recreation clutter or ambiguous hydrology. This is also an INFERRED range. The display is dominated by short named flowline pieces, includes 17 distinct ditch/canal names, and carries 30 reservoir-labelled polygons for which no manager or recreation status is present. The estimate could be too high if the product intends to show scenic streams rather than functional recreational water.
- Confirmed useful-water examples from the checked sample are six named water features: Snowmass Lake, Maroon Lake, Chatfield Lake, Cheesman Lake, Rueter-Hess Reservoir, and Strontia Springs Reservoir. This is not a complete count of useful water in either region. [RETRIEVED; URLs below]

The key distinction is between “recreationally interesting” and “publicly usable for a particular activity.” For example, Cheesman Reservoir offers limited fishing and hiking but prohibits boating, camping, and water-contact sports. [RETRIEVED](https://www.denverwater.org/recreation/cheesman-reservoir)

## 3. Suspicious and ambiguous named features

| Feature | What the retrieved sources establish | Manager / public recreation judgment |
|---|---|---|
| Wildcat Reservoir | A Colorado water-court notice identifies Wildcat Reservoir as having municipal, irrigation, and recreation decreed uses, with 1,140 acre-feet absolute storage. [RETRIEVED](https://www.coloradojudicial.gov/sites/default/files/2026-01/December%202025%20Resume%20-%20Website%20Version.pdf) | Manager and ownership: UNKNOWN from the retrieved source. Public access, fishing, boating, swimming, parking, and camping: UNKNOWN. The word “recreation” in a water decree is not public-access permission. |
| Grizzly Reservoir | A Colorado state loan report identifies the Twin Lakes Reservoir and Canal Company as operating the Independence Pass Transmountain Diversion System, which collects water into Grizzly Reservoir and conveys it under the Continental Divide. [RETRIEVED](https://spl.cde.state.co.us/artemis/nrserials/nr316internet/nr3162023internet.pdf) | Managed by Twin Lakes Reservoir and Canal Company for water storage and transbasin diversion. Public recreation and access: UNKNOWN. No retrieved source established a public recreation program. |
| Salvation Ditch | The retrieved reporting identifies the Salvation Ditch Company, a 26-mile irrigation ditch carrying water toward McLain Flats and beyond, with a senior agricultural diversion right. [RETRIEVED](https://www.aspentimes.com/news/ditch-owner-works-to-give-river-a-boost/) | Manager: Salvation Ditch Company. Public recreation: UNKNOWN; nothing retrieved establishes public access, paddling, fishing, or swimming. This should be treated as irrigation infrastructure, not recreational water. |
| Snowmass Lake | The Forest Service identifies Snowmass Lake within the Maroon Bells-Snowmass Wilderness and states that overnight stays in designated zones require advance permits. [RETRIEVED](https://www.fs.usda.gov/r02/whiteriver/recreation/maroon-bells-snowmass-wilderness) | Recreation manager: White River National Forest, Aspen-Sopris Ranger District. Hiking and backpacking are offered; camping is restricted to designated areas and permits. The Forest Service states: “A permit is required for overnight stays.” Fishing, boating, swimming, and vehicle parking at the lake: UNKNOWN from the retrieved source. |
| Maroon Lake | The Forest Service identifies the Maroon Lake Scenic Trailhead as a White River National Forest site with hiking and backpacking. High-season parking and shuttle reservations apply, and wilderness overnight permits apply where relevant. [RETRIEVED](https://www.fs.usda.gov/r02/whiteriver/recreation/maroon-lake-scenic-trailhead-2197) | Recreation manager: White River National Forest, Aspen-Sopris Ranger District. Trail recreation is offered with access controls and fees in the scenic area. Boating, fishing, swimming, and camping at Maroon Lake itself: UNKNOWN. |
| Chatfield Lake | Chatfield State Park’s official page says boaters, anglers, canoeists, and sailors use the reservoir; it has boat ramps, a marina, fishing, and seasonal restrictions. [RETRIEVED](https://cpw.state.co.us/state-parks/chatfield-state-park/chatfield-state-park-park-highlights) | Managed for recreation by Colorado Parks and Wildlife through Chatfield State Park. Boating, fishing, and swimming are offered but regulated by inspections, zones, operating seasons, and safety rules. |
| Cheesman Lake | Denver Water states that the reservoir was purchased by the Denver Water Board and that fishing is allowed only on the Goose Creek Arm. [RETRIEVED](https://www.denverwater.org/recreation/cheesman-reservoir) | Manager: Denver Water. Fishing and hiking are offered in restricted areas and seasons. Boating and camping are expressly prohibited; swimming, wading, and other water-contact sports are prohibited. |
| Strontia Springs Reservoir | Denver Water identifies itself as owner, operator, and recreation manager. Fishing and hiking are offered, while canoeing, kayaking, tubing, rafting, swimming, and wading are prohibited. [RETRIEVED](https://www.denverwater.org/recreation/waterton-canyon-strontia-springs-resevoir) | Managed by Denver Water. Recreation is offered primarily as hiking, cycling, horseback riding, wildlife viewing, and regulated fishing; water access is restricted. The page states: “Boating regulations: Not permitted.” |
| Rueter-Hess Reservoir | Douglas County states that water recreation and fishing are open on scheduled days, with reservations, inspections, approved watercraft, and fishing permits. Recreation activities are managed by the Rueter-Hess Advisory Board. [RETRIEVED](https://www.douglasco.gov/rueter-hess-recreation/) | Public recreation is offered but tightly controlled. Paddle sports and fishing are allowed under reservations, seasonal hours, watercraft restrictions, and fishing rules. |
| Aurora-Rampart Reservoir | Aurora identifies Rampart Reservoir as part of its mountain water-supply system. Its general recreation page describes recreation at some Aurora reservoirs, but the retrieved material did not provide a Rampart-specific activity or access rule. [RETRIEVED](https://www.auroragov.org/residents/water/water_system/water_sources/mountain_supply) | Manager: Aurora Water is associated with the water supply. Rampart-specific public recreation, fishing, boating, swimming, parking, and camping: UNKNOWN. |
| Arapahoe Canal | The retrieved sources did not establish the identity, manager, access rules, or recreation status of the specific NHD feature named Arapahoe Canal. [UNKNOWN](https://hydro.nationalmap.gov/arcgis/rest/services/nhd/MapServer/6) | UNKNOWN. Do not conflate it with High Line Canal without a spatial or administrative match. |
| High Line Canal | Arapahoe County states that Denver Water transferred ownership of 45 miles to Arapahoe County in 2024, with a conservation easement held by the High Line Canal Conservancy; the canal remains a free recreational trail. [RETRIEVED](https://www.arapahoeco.gov/your_county/county_departments/open_spaces/our_work/current_projects/high_line_canal_ownership_transfer.php) | Trail recreation is offered. The manager and ownership of the specific Douglas County reach were not established by the retrieved page. Water recreation is not established; the evidence supports walking, cycling, and similar trail use, not boating or swimming. |
| Franktown Parker FP… reservoirs | USGS’s reservoir database confirms similarly named Franktown-Parker reservoirs in Douglas County, including FP-B-1 and FP-P-1, but does not establish public recreation. [RETRIEVED](https://water.usgs.gov/osw/ressed/interactive_map/map_co.html) | Individual manager, ownership, public access, fishing, boating, swimming, parking, and camping: UNKNOWN. The prefix is an identifier, not a recreation designation. |
| West Cherry Creek Detention Number… reservoirs | The NHD names identify these as detention reservoirs, but no retrieved source established their exact operator, public access, or recreation status. [UNKNOWN](https://hydro.nationalmap.gov/arcgis/rest/services/nhd/MapServer/12) | Treat as stormwater or flood-control candidates pending confirmation. Public recreation: UNKNOWN. |

## 4. Source fields and discarded evidence

The current Aspen layer carries only `id`, `kind`, `name`, and `evidence`. Douglas water layers carry `name`, `manager`, `id`, and `evidence`; the manager value is null for all 2,392 Douglas water features. [RETRIEVED: coordinator computation; source service](https://hydro.nationalmap.gov/arcgis/rest/services/nhd/MapServer)

The pipeline requests `OBJECTID` and, for Douglas’s named subset, `GNIS_NAME`. The USGS layer metadata exposes a substantially richer hydrography schema, including feature classification, network identity, reach information, flow-related attributes, and size or measurement fields. The source service description specifically identifies reach codes, flow direction, names, and centerline representations for areal water bodies. [RETRIEVED](https://hydro.nationalmap.gov/arcgis/rest/services/nhd/MapServer/6?f=pjson)

The discarded fields most important for M4 are:

1. Feature type and code: useful for separating streams, canals, ditches, reservoirs, ponds, and other constructed features.
2. Permanent NHD identifiers and reach codes: useful for joining fragments into stable water objects.
3. Flow permanence and visibility or display filters: useful for reducing ephemeral and cartographic clutter.
4. Length and area: useful for minimum-size and recreational-significance thresholds.
5. Ownership, manager, access, and activity fields where available from supplemental authoritative services.

The NHD license is permissive, but its limitations matter. USGS states: “This dataset is not intended to be used for site-specific regulatory determinations.” [RETRIEVED](https://hydro.nationalmap.gov/arcgis/rest/services/nhd/MapServer) USGS also states that National Map services and data are free and public domain, while requesting acknowledgment of the originating agency. [RETRIEVED](https://www.usgs.gov/faqs/how-should-i-cite-datasets-and-services-national-map)

## 5. Identity and pipeline problems

The current IDs are built from service `OBJECTID`. That is not a stable NHD identity and can change after source refreshes. [RETRIEVED: coordinator pipeline audit; source schema](https://hydro.nationalmap.gov/arcgis/rest/services/nhd/MapServer/6?f=pjson)

A single named stream is represented by many independently tappable geometries. This is particularly severe in Douglas, where repeated-name groups average approximately 41.9 pieces, and visible in Aspen, where the Roaring Fork River has 112 pieces. [INFERRED from coordinator counts;](https://hydro.nationalmap.gov/arcgis/rest/services/nhd/MapServer/6)

Canonical Aspen hydrology must remain separate from display selection. All 6,926 Aspen features feed setback screening, while only 1,555 named features are displayed. Removing unnamed or utility features from the canonical screening layer would risk changing a separate environmental-safety function. [RETRIEVED: coordinator pipeline audit; source service](https://hydro.nationalmap.gov/arcgis/rest/services/nhd/MapServer/6)

## Unknowns and things I could not verify

- No retrieved source established public access for most Aspen lakes, reservoirs, ponds, ditches, or canals.
- No retrieved source established the manager or access rules for most Douglas reservoirs, including the Franktown Parker and West Cherry Creek detention groups.
- The specific identity of Arapahoe Canal was not established, and it should not be assumed to be High Line Canal.
- Rampart Reservoir’s specific recreation rules were not retrieved.
- Public swimming, fishing, boating, parking, and camping permissions remain activity-specific and cannot be inferred from a feature name, geometry, ownership, or general recreation page.
- The exact number of individual pieces belonging to ditch and canal name groups was not included in the coordinator summary.
- The clutter percentages are inferred ranges, not measurements from a feature-by-feature legal or recreation classification.
- The retrieved USFS page for the former Maroon/Snowmass Trailhead URL returned 404; the current Forest Service wilderness and Maroon Lake pages loaded successfully. [RETRIEVED](https://www.fs.usda.gov/r02/whiteriver/recreation/maroon-snowmass-trailhead-1975)

## Recommendation

For M4, do not expose the current named hydrology subset as “recreational water.” Build a separate display-selection layer from canonical hydrology.

Use a conservative first-pass display policy:

1. Include waterbodies only when an authoritative recreation or land-manager source establishes public access or a clearly public recreation setting.
2. Include named rivers and streams as recreational corridors only after dissolving or grouping fragments by stable source identity and retaining one selectable logical water object.
3. Exclude or visually subordinate names containing `ditch`, `canal`, `detention`, `drainage`, or similar infrastructure terms unless an authoritative source establishes a public trail or recreation function.
4. Keep water-supply reservoirs in the map only when their access status is explicit: offered, restricted, or closed.
5. Show activity-specific permissions separately. “Fishing offered” must not imply boating, swimming, camping, or parking.
6. Preserve the full Aspen canonical layer for setback screening; apply recreation filtering only to the display artifact.
7. Start retaining stable NHD identifiers, `GNIS_NAME`, feature type and code, reach code, permanent identifier, flow permanence, length, area, source layer, and any authoritative manager/access/activity evidence.
8. Replace `OBJECTID`-only IDs with stable source identifiers plus a controlled fallback, and store a `logical_water_id` for dissolved or grouped stream features.
9. Add explicit fields such as `access_status`, `recreation_source_url`, `manager`, `activities`, `seasonal_restrictions`, `parking_status`, and `confidence`, with `unknown` as a valid value.
10. Treat absence of evidence as unknown rather than as permission.
