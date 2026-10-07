# M6B — How competitors model trail identity

> Hermes report (GPT-5.6 luna), 2026-10-07, stored as returned. HERMES-SOURCED: web research only, no repository access. Nothing here is verified by the coordinator unless another document says so, and nothing is decided.

Research basis: official help centres, product documentation, product pages, engineering/product pages, and official agency documentation retrieved in this session. “PRIMARY SOURCE” means the publisher’s page was read. “INFERENCE” is a design conclusion from those sources. “UNKNOWN” means the retrieved official material did not establish the point.

## AllTrails

- MODEL — PRIMARY SOURCE: AllTrails separates a curated “verified route” from map-only trail segments. Verified routes are the user-facing trail pages and navigation lines; OSM segments are separate dashed map data. https://support.alltrails.com/hc/en-us/articles/4410231246100-Verified-routes-vs-OSM-OpenStreetMap-segments
- HOW SEGMENTS ARE GROUPED — PRIMARY SOURCE: AllTrails aims for each trail page to have an accurate, hand-curated route. OSM segments remain individual source-map segments and are not directly verified by AllTrails. https://support.alltrails.com/hc/en-us/articles/4410231246100-Verified-routes-vs-OSM-OpenStreetMap-segments
- OVERLAP HANDLING — UNKNOWN: The retrieved documentation does not explain deduplication or identity rules when several verified routes follow the same physical ground.
- NAMES — PRIMARY SOURCE: Trail names can be suggested as edits, alongside the trailhead, length, difficulty, dog status, and route geometry. The edit is moderated. https://support.alltrails.com/hc/en-us/articles/360018930672-How-to-update-or-change-information-about-a-trail
- METRICS — PRIMARY SOURCE: Verified-route length is based on anonymized member GPS recordings, averaged to define the route, then measured along elevation-aware short segments. The retrieved source explains distance, but not a separate elevation-gain formula. https://support.alltrails.com/hc/en-us/articles/45256736225556-How-does-AllTrails-calculate-the-length-of-a-verified-trail
- DIFFICULTY — UNKNOWN: The official difficulty-rating article linked by search was not retrievable at the attempted URL, so the assignment method is not reported here. https://support.alltrails.com/hc/en-us/articles/360020609552-Difficulty-ratings-on-AllTrails
- USES / CLOSURES — PRIMARY SOURCE: AllTrails documents private segments and tells users to verify that they are “safely and legally allowed” before using alternative OSM segments. It also receives park and land-manager alerts and accounts for seasonal changes, disasters, and maintenance. These are signals, not independent permission evidence. https://support.alltrails.com/hc/en-us/articles/4410231246100-Verified-routes-vs-OSM-OpenStreetMap-segments https://support.alltrails.com/hc/en-us/articles/30315531476628-How-does-a-trail-end-up-on-AllTrails
- SOURCE DATA — PRIMARY SOURCE: Sources include OSM for map segments; park officials; proprietary data and automation; member feedback; and land-manager information through the Public Lands Program. https://support.alltrails.com/hc/en-us/articles/360018930672-How-to-update-or-change-information-about-a-trail https://support.alltrails.com/hc/en-us/articles/30315531476628-How-does-a-trail-end-up-on-AllTrails https://support.alltrails.com/hc/en-us/articles/11555324555924-AllTrails-map-legend
- WHAT A SMALL TEAM COULD COPY CHEAPLY — INFERENCE: Keep a canonical, reviewed trail geometry separate from imported network segments; attach source, review state, name, and warning fields to each.
- WHAT IS EXPENSIVE — INFERENCE: GPS-trace aggregation, moderation, source synchronization, and land-manager alert partnerships are the expensive parts.

## Gaia GPS

- MODEL — PRIMARY SOURCE: Gaia distinguishes a “Trail” as a mapped footpath or road from a “Hike” as a known route frequently traveled as an activity. A hike may use one trail or several trails. https://help.gaiagps.com/hc/en-us/articles/360048827494-Search-for-hikes-parks-trails-and-places-in-the-Android-app https://help.gaiagps.com/hc/en-us/articles/1500006593982-Search-for-hikes-parks-trails-and-places-in-the-iOS-app
- HOW SEGMENTS ARE GROUPED — PRIMARY SOURCE: A user-facing hike can be composed of multiple underlying trails. User-created routes can snap to existing trails or be drawn as straight-line geometry. https://help.gaiagps.com/hc/en-us/articles/360048827494-Search-for-hikes-parks-trails-and-places-in-the-Android-app https://help.gaiagps.com/hc/en-us/articles/115003640568-Create-and-Measure-Routes-on-gaiagps-com
- OVERLAP HANDLING — UNKNOWN: No retrieved Gaia documentation explains how two hikes or routes that share the same trail segments are deduplicated or displayed together.
- NAMES — PRIMARY SOURCE: Saved routes have a route title and notes. The retrieved documentation does not describe aliases or multiple official names for one trail. https://help.gaiagps.com/hc/en-us/articles/115003640568-Create-and-Measure-Routes-on-gaiagps-com
- METRICS — PRIMARY SOURCE: Gaia displays route distance and cumulative ascent/descent with an elevation profile. Snap-to-trail routing uses OSM data. https://help.gaiagps.com/hc/en-us/articles/115003640568-Create-and-Measure-Routes-on-gaiagps-com
- DIFFICULTY — PRIMARY SOURCE / UNKNOWN: Gaia exposes difficulty as a search/filter attribute for hikes, but the retrieved official material does not state how the rating is assigned. https://help.gaiagps.com/hc/en-us/articles/360048827494-Search-for-hikes-parks-trails-and-places-in-the-Android-app
- USES / CLOSURES — PRIMARY SOURCE: Hiking, cycling, and driving are routing modes. They describe route-planning behavior, not permission. No closure or seasonal-status model was established in the retrieved help pages. https://help.gaiagps.com/hc/en-us/articles/115003640568-Create-and-Measure-Routes-on-gaiagps-com
- SOURCE DATA — PRIMARY SOURCE: OSM is explicitly used for snap-to-trail routing; Gaia also supports multiple map layers and sources. https://help.gaiagps.com/hc/en-us/articles/115003640568-Create-and-Measure-Routes-on-gaiagps-com https://help.gaiagps.com/hc/en-us/articles/9067661557399-How-to-Use-Gaia-GPS
- WHAT A SMALL TEAM COULD COPY CHEAPLY — INFERENCE: Model a physical network separately from named activity routes, then let a route reference many network segments.
- WHAT IS EXPENSIVE — INFERENCE: Maintaining popular-hike identities, routing coverage, map-source integrations, and activity-specific discovery is expensive.

## onX Backcountry

- MODEL — PRIMARY SOURCE: The product presents hiking trails, trailheads, waypoints, route details, and custom routes as separate planning and navigation concepts. The retrieved page does not define a formal trail-versus-route data schema. https://www.onxmaps.com/backcountry/app/features/hiking-trail-maps
- HOW SEGMENTS ARE GROUPED — UNKNOWN: The official hiking page says it integrates trails from various sources but does not explain segment grouping or route composition. https://www.onxmaps.com/backcountry/app/features/hiking-trail-maps
- OVERLAP HANDLING — UNKNOWN: No retrieved onX Backcountry source explains overlapping trail identities.
- NAMES — UNKNOWN: No retrieved source explains aliases, alternate names, or whether names belong to physical segments or curated routes.
- METRICS — PRIMARY SOURCE: onX Backcountry exposes trail difficulty, terrain, elevation gain, custom-route distance, and elevation changes. The retrieved source does not explain the calculation method. https://www.onxmaps.com/backcountry/app/features/hiking-trail-maps
- DIFFICULTY — PRIMARY SOURCE / UNKNOWN: Difficulty is presented as a trail insight, but the rating assignment method is not documented in the retrieved source. https://www.onxmaps.com/backcountry/app/features/hiking-trail-maps
- USES / CLOSURES — PRIMARY SOURCE: The product presents public/private land data, access regulations, and activity modes. The retrieved hiking page does not establish a closure-status workflow. Land boundaries or an access-regulation layer are not, by themselves, permission evidence. https://www.onxmaps.com/backcountry/app/features/hiking-trail-maps
- SOURCE DATA — PRIMARY SOURCE: onX says Backcountry integrates trails and public-land data from various sources; the company says its broader map foundation combines federal, state, and county agency data that is organized and verified before publication. https://www.onxmaps.com/backcountry/app/features/hiking-trail-maps https://www.onxmaps.com/discoveronx
- WHAT A SMALL TEAM COULD COPY CHEAPLY — INFERENCE: Separate trail geometry, route-planning geometry, land ownership, and source provenance.
- WHAT IS EXPENSIVE — INFERENCE: Nationwide source licensing, agency-data normalization, offline map delivery, and editorial verification.

## onX Offroad

- MODEL — PRIMARY SOURCE: The user-facing unit is a guided motorized trail with a guidebook-style description, difficulty, vehicle clearance, and access information. Users can also plan custom routes. https://www.onxmaps.com/offroad/app/features/trail-maps
- HOW SEGMENTS ARE GROUPED — UNKNOWN: The retrieved source does not explain whether a guided trail is one physical segment, a concatenation of segments, or a named route over a network.
- OVERLAP HANDLING — UNKNOWN: No retrieved source explains how shared roads or trails are handled when multiple guided trails use them.
- NAMES — UNKNOWN: No retrieved source explains alternate names or whether a name is attached to a physical segment, guided trail, or area.
- METRICS — PRIMARY SOURCE / UNKNOWN: The product exposes trail difficulty, vehicle clearance, route planning, and vehicle-type filtering. The retrieved page does not establish how length or elevation gain are computed. https://www.onxmaps.com/offroad/app/features/trail-maps
- DIFFICULTY — PRIMARY SOURCE / UNKNOWN: Difficulty ratings are displayed and guided trails are vetted by a network of guides, but the rating rubric was not retrieved. https://www.onxmaps.com/offroad/app/features/trail-maps
- USES / CLOSURES — PRIMARY SOURCE: onX Offroad presents vehicle types, open/closed status, access information, seasonal closures, public/private land boundaries, and vehicle restrictions. These are product fields; a map label alone is not independent permission evidence. https://www.onxmaps.com/offroad/app/features/trail-maps
- SOURCE DATA — PRIMARY SOURCE: Sources include nationwide motorized-trail data, official onX Trail Guides, and a team of off-roaders who map and detail guided trails. https://www.onxmaps.com/offroad/app/features/trail-maps
- WHAT A SMALL TEAM COULD COPY CHEAPLY — INFERENCE: A single curated route object with explicit vehicle-use evidence, closure records, source links, and a computed geometry profile.
- WHAT IS EXPENSIVE — INFERENCE: Guide coverage, field verification, vehicle-specific classification, and continuously maintained closure data.

## Trailforks

- MODEL — UNKNOWN: Trailforks’ official About, route-planner, hiking, and help pages were found in official search results, but direct retrieval of the publisher pages failed with a payment-required retrieval error. I do not treat the snippets as read primary-source evidence.
- HOW SEGMENTS ARE GROUPED — UNKNOWN: Not reported because the official pages could not be read directly.
- OVERLAP HANDLING — UNKNOWN.
- NAMES — UNKNOWN.
- METRICS — UNKNOWN.
- DIFFICULTY — UNKNOWN.
- USES / CLOSURES — UNKNOWN.
- SOURCE DATA — UNKNOWN.
- WHAT A SMALL TEAM COULD COPY CHEAPLY — INFERENCE: Do not copy a Trailforks-specific pattern until its official documentation can be read and its trail, route, and user-ridelog objects are confirmed.
- WHAT IS EXPENSIVE — UNKNOWN from this session.

Attempted official sources: https://www.trailforks.com/about/ https://www.trailforks.com/about/features/route_planner/ https://www.trailforks.com/about/activity/hiking/ https://help.trailforks.com/hc/en-us/articles/5431676240535-Find-that-Must-Ride-Trail https://help.trailforks.com/hc/en-us/articles/16602255252119-How-to-Use-the-Trailforks-Map

## CalTopo

- MODEL — PRIMARY SOURCE: CalTopo treats a line as a user-created vector object. Lines can be designated as a route or track and can represent a trail, route, bearing, boundary, or watercourse. https://training.caltopo.com/all_users/objects/lines-and-polys
- HOW SEGMENTS ARE GROUPED — PRIMARY SOURCE: Lines are made of connected points and can be split, joined, extended, reversed, simplified, or snapped to map features. The documentation describes editing operations, not a canonical trail-segment identity model. https://training.caltopo.com/all_users/objects/existing-lines https://training.caltopo.com/all_users/objects/lines-and-polys
- OVERLAP HANDLING — UNKNOWN: The retrieved documentation does not describe deduplication or shared identity for overlapping lines.
- NAMES — PRIMARY SOURCE: A line has a title displayed on the map and in the object menu, plus a description. https://training.caltopo.com/all_users/objects/lines-and-polys
- METRICS — PRIMARY SOURCE: CalTopo’s line profile reports total distance, lowest/highest points, and total elevation gain/loss calculated along the line. The profile is based on elevation change over line distance. https://training.caltopo.com/all_users/objects/existing-lines
- DIFFICULTY — UNKNOWN: No retrieved CalTopo documentation establishes a trail difficulty rating or assignment method.
- USES / CLOSURES — UNKNOWN: Route and track are user-object types, not documented permission statuses. No canonical closure or seasonal trail-status model was retrieved.
- SOURCE DATA — PRIMARY SOURCE / UNKNOWN: Snap-to drawing follows map features, but the retrieved documentation does not identify the underlying source datasets. https://training.caltopo.com/all_users/objects/lines-and-polys
- WHAT A SMALL TEAM COULD COPY CHEAPLY — INFERENCE: User-owned line objects, explicit route/track type, title, description, geometry editing, and elevation profiles.
- WHAT IS EXPENSIVE — INFERENCE: High-quality basemaps, map-feature snapping, robust geometry editing, and terrain/statistics infrastructure.

## FarOut

- MODEL — PRIMARY SOURCE: A FarOut “guide” is a detailed map for one trail or river. Guides contain a primary track, elevation, waypoints, campsites, water, junctions, and other route information. https://faroutguides.com/features/
- HOW SEGMENTS ARE GROUPED — PRIMARY SOURCE: Guides can be divided into sections, and the track can include side trails and alternate routes. The retrieved documentation does not specify whether alternates are separate identities or geometry branches within one guide. https://faroutguides.com/features/ https://faroutguides.com/help/
- OVERLAP HANDLING — UNKNOWN: No retrieved source explains identity handling where guides or alternate routes share ground.
- NAMES — PRIMARY SOURCE / UNKNOWN: Users select a guide and can switch between full trails and sections. Alias handling or multiple official names were not documented. https://faroutguides.com/help/
- METRICS — PRIMARY SOURCE / UNKNOWN: FarOut provides detailed elevation profiles and distance calculations to waypoints, but the retrieved documentation does not state the distance or elevation algorithm. https://faroutguides.com/features/
- DIFFICULTY — UNKNOWN: No retrieved official FarOut source describes a difficulty-rating method.
- USES / CLOSURES — PRIMARY SOURCE: FarOut publishes alerts and information including fire closures, reroutes, camping restrictions, wildlife reports, and permit requirements. These are advisory data fields and do not independently establish permission. https://faroutguides.com/app-basics/
- SOURCE DATA — PRIMARY SOURCE: Route data is collected from trusted individuals and partner organizations. Water information is gathered from trusted sources and checked by users; community comments and recorded tracks are separate user content. https://faroutguides.com/features/ https://faroutguides.com/help/
- WHAT A SMALL TEAM COULD COPY CHEAPLY — INFERENCE: A guide object containing a primary route, explicit sections, waypoint records, source notes, alerts, and user annotations.
- WHAT IS EXPENSIVE — INFERENCE: Handcrafted long-distance guides, field-maintained waypoints, partner relationships, offline packaging, and current closure/reroute updates.

## Hiking Project

- MODEL — PRIMARY SOURCE: Hiking Project explicitly separates a “trail” from a “recommended route.” A trail is a single trail as shown on a printed map; a recommended route is a complete route that may use one or more trails. https://www.hikingproject.com/help/21/overview-of-site-name-features
- HOW SEGMENTS ARE GROUPED — PRIMARY SOURCE: Trails are added individually and in their entirety. Recommended routes are local-favorite routes that often use multiple trails. https://www.hikingproject.com/mapping
- OVERLAP HANDLING — PRIMARY SOURCE / UNKNOWN: The model permits a recommended route to use multiple trail objects, but the retrieved documentation does not explain geometry deduplication or how shared portions are represented. https://www.hikingproject.com/help/21/overview-of-site-name-features https://www.hikingproject.com/mapping
- NAMES — PRIMARY SOURCE: Trail and recommended-route pages are distinct user-facing objects. Alias and alternate-name behavior is not documented in the retrieved sources. https://www.hikingproject.com/help/21/overview-of-site-name-features
- METRICS — PRIMARY SOURCE: Length follows the mapped start and end points; loops and out-and-backs may show round-trip length. Elevation ascent/descent is total gain/loss in the mapped direction. Grade is derived from the mapped GPS track and an elevation model, with stated accuracy limitations. https://www.hikingproject.com/help/21/overview-of-site-name-features
- DIFFICULTY — PRIMARY SOURCE: Difficulty is the average of community votes, with categories from Easy through Very Difficult. https://www.hikingproject.com/help/21/overview-of-site-name-features
- USES / CLOSURES — PRIMARY SOURCE: Hiking Project says it documents legal trails approved by local land managers, but that policy does not prove the current permission status of any individual trail. It exposes access issues, closure dates, restrictions, land-manager links, and dog-related fields. https://www.hikingproject.com/share/trail https://www.hikingproject.com/help/21/overview-of-site-name-features
- SOURCE DATA — PRIMARY SOURCE: The database is community-built; contributors submit GPS tracks, photos, trails, routes, ratings, and conditions. Contributions are reviewed in-house, and trail pages link land managers and local clubs. https://www.hikingproject.com/mapping https://www.hikingproject.com/help/21/overview-of-site-name-features
- WHAT A SMALL TEAM COULD COPY CHEAPLY — INFERENCE: Use two first-class objects: a maintained physical trail and a curated route that references one or more trails.
- WHAT IS EXPENSIVE — INFERENCE: Editorial review, contributor moderation, community ratings, field conditions, and maintaining land-manager relationships.

## Komoot

- MODEL — UNKNOWN: The attempted official help pages did not load. No reliable primary-source evidence was obtained for Komoot’s trail, tour, route, or track identity model.
- HOW SEGMENTS ARE GROUPED — UNKNOWN.
- OVERLAP HANDLING — UNKNOWN.
- NAMES — UNKNOWN.
- METRICS — UNKNOWN.
- DIFFICULTY — UNKNOWN.
- USES / CLOSURES — UNKNOWN.
- SOURCE DATA — UNKNOWN.
- WHAT A SMALL TEAM COULD COPY CHEAPLY — UNKNOWN from this session.
- WHAT IS EXPENSIVE — UNKNOWN from this session.

Attempted official sources: https://help.komoot.com/hc/en-us/articles/360023079132-How-does-komoot-calculate-the-elevation-gain https://help.komoot.com/hc/en-us/articles/360023079152-How-does-komoot-calculate-the-difficulty-of-a-tour https://help.komoot.com/hc/en-us/articles/360023079172-How-does-komoot-know-if-a-way-is-accessible https://help.komoot.com/hc/en-us/articles/360023079192-How-does-komoot-generate-tour-suggestions

## COTREX app

- MODEL — PRIMARY SOURCE: COTREX presents official trails, featured routes, trailheads, and recorded trips. It also lets users create and share custom routes on “authorized trails,” but the product statement itself is not evidence that a particular route is currently permitted. https://cpw.state.co.us/cpw-apps https://cpw.state.co.us/news/05192023/cotrex-app-verified-source-trail-info-colorado-public-lands
- HOW SEGMENTS ARE GROUPED — PRIMARY SOURCE / UNKNOWN: COTREX describes a statewide network of official trails and supports measuring any trail segment, but the retrieved documentation does not explain how one trail is split, merged, or grouped into a route. https://cpw.state.co.us/cpw-apps https://play.google.com/store/apps/details?id=com.cotrexapp&hl=en_US
- OVERLAP HANDLING — UNKNOWN: No retrieved COTREX documentation explains multiple named routes sharing the same trail ground.
- NAMES — UNKNOWN: The retrieved sources show featured routes and trails but do not document aliases, alternate names, or naming precedence.
- METRICS — PRIMARY SOURCE: COTREX supports distance, elevation profiles, and trail grade for custom routes; it also supports distance and elevation profiles for trail segments. https://cpw.state.co.us/news/05192023/cotrex-app-verified-source-trail-info-colorado-public-lands https://play.google.com/store/apps/details?id=com.cotrexapp&hl=en_US
- DIFFICULTY — UNKNOWN: No retrieved source explains a difficulty field or its assignment method.
- USES / CLOSURES — PRIMARY SOURCE: COTREX offers an “allowed uses” map view and activity filters, plus official alerts and closures. Those fields should be treated as agency-published evidence only when the underlying agency notice is available; their existence does not itself establish permission. https://cpw.state.co.us/cpw-apps https://cpw.state.co.us/news/05192023/cotrex-app-verified-source-trail-info-colorado-public-lands
- SOURCE DATA — PRIMARY SOURCE: COTREX is built from GIS data supplied by hundreds of land-management agencies, with the Colorado documentation describing information “directly from the source.” The app describes itself as using official-source information rather than unreliable crowdsourced trail data. https://cpw.state.co.us/news/05192023/cotrex-app-verified-source-trail-info-colorado-public-lands https://play.google.com/store/apps/details?id=com.cotrexapp&hl=en_US
- WHAT A SMALL TEAM COULD COPY CHEAPLY — INFERENCE: Store agency trail geometry, agency identity, source URL, publication/update time, use evidence, closure evidence, and user-created route geometry separately.
- WHAT IS EXPENSIVE — INFERENCE: Agency onboarding, GIS normalization, authoritative update feeds, and statewide coverage.

## OpenStreetMap

- MODEL — PRIMARY SOURCE: OSM models physical paths as ways and named/signed hiking itineraries as `type=route` relations with `route=hiking`. The relation is the route identity; its member ways provide the geometry. https://wiki.openstreetmap.org/wiki/Relation:route https://wiki.openstreetmap.org/wiki/Tag:route=hiking
- HOW SEGMENTS ARE GROUPED — PRIMARY SOURCE: A hiking relation contains the different ways making up the route, and member order matters. OSM distinguishes a route relation from the individual ways that form it. https://wiki.openstreetmap.org/wiki/Tag:route=hiking https://wiki.openstreetmap.org/wiki/Relation:route
- OVERLAP HANDLING — PRIMARY SOURCE: OSM explicitly documents multiple routes sharing the same ways. A route master can contain directions and variants. https://wiki.openstreetmap.org/wiki/Relation:route
- NAMES — PRIMARY SOURCE: Route relations can carry `name`, `ref`, `operator`, `network`, direction, origin, and destination tags. This permits different named routes to reference the same physical way. https://wiki.openstreetmap.org/wiki/Relation:route https://wiki.openstreetmap.org/wiki/Tag:route=hiking
- METRICS — PRIMARY SOURCE / UNKNOWN: `distance=*` is listed as a useful `route=hiking` relation tag, but the retrieved documentation does not prescribe a universal calculation method for length, elevation gain, or grade. https://wiki.openstreetmap.org/wiki/Tag:route=hiking
- DIFFICULTY — UNKNOWN: No canonical difficulty-rating calculation was established in the retrieved OSM route documentation.
- USES / CLOSURES — PRIMARY SOURCE: OSM’s `access=*` family describes “the legal accessibility of a feature.” The documentation says access tags should follow signage and legal regulation, not common or typical use. A `route=hiking` relation alone does not grant permission. https://wiki.openstreetmap.org/wiki/Key:access
- SOURCE DATA — PRIMARY SOURCE: OSM is a collaborative, user-maintained geographic database. The retrieved route pages establish the data model and tagging rules; they do not establish that any particular trail is official.
- WHAT A SMALL TEAM COULD COPY CHEAPLY — INFERENCE: Separate physical ways from named route relations; allow many routes to reference the same way; preserve relation-level names, references, operators, and evidence.
- WHAT IS EXPENSIVE — INFERENCE: Global volunteer editing, validation, relation maintenance, dispute resolution, and full routing/rendering infrastructure.

## Patterns

1. Editorial trail plus curated route — PRIMARY SOURCE / INFERENCE: Hiking Project explicitly separates a physical trail from a recommended multi-trail route; AllTrails separates verified routes from OSM segments; COTREX separates official trails, featured routes, and custom routes. This is the clearest model for a discovery product. https://www.hikingproject.com/help/21/overview-of-site-name-features https://support.alltrails.com/hc/en-us/articles/4410231246100-Verified-routes-vs-OSM-OpenStreetMap-segments https://cpw.state.co.us/cpw-apps

2. Network geometry plus named overlays — PRIMARY SOURCE / INFERENCE: OSM treats ways as physical geometry and route relations as named itineraries that can overlap. Gaia’s hikes similarly can combine multiple trails, while CalTopo treats routes and tracks as user-owned line objects. https://wiki.openstreetmap.org/wiki/Relation:route https://help.gaiagps.com/hc/en-us/articles/360048827494-Search-for-hikes-parks-trails-and-places-in-the-Android-app https://training.caltopo.com/all_users/objects/lines-and-polys

3. Guidebook route plus evidence and waypoints — PRIMARY SOURCE / INFERENCE: FarOut and onX Offroad emphasize curated guides, route details, waypoints, access/closure information, and editorial maintenance rather than a fully general trail ontology. https://faroutguides.com/features/ https://www.onxmaps.com/offroad/app/features/trail-maps

## What an evidence-first product should not copy

- Do not collapse a physical segment, a named route, a recommended itinerary, and a user-recorded track into one “trail” object. The documented products keep at least some of these distinct. https://www.hikingproject.com/help/21/overview-of-site-name-features https://wiki.openstreetmap.org/wiki/Relation:route https://support.alltrails.com/hc/en-us/articles/4410231246100-Verified-routes-vs-OSM-OpenStreetMap-segments
- Do not infer permission from a line, public ownership, a map label, a route relation, a trailhead, or an “allowed uses” filter. OSM says access tagging must follow legal ground truth, and AllTrails warns users to establish that they are legally allowed on alternative segments. https://wiki.openstreetmap.org/wiki/Key:access https://support.alltrails.com/hc/en-us/articles/4410231246100-Verified-routes-vs-OSM-OpenStreetMap-segments
- Do not treat community conditions, recent GPS use, or popularity as an official open-status signal. Hiking Project’s condition reports are contributor-maintained and become unknown after 100 days without an update. https://www.hikingproject.com/help/21/overview-of-site-name-features
- Do not hide metric provenance. Distance, elevation gain, and grade are computed differently across products: AllTrails uses averaged member GPS paths and elevation-aware distance; Hiking Project uses mapped endpoints, mapped travel direction, GPS tracks, and an elevation model; CalTopo profiles user-drawn lines. https://support.alltrails.com/hc/en-us/articles/45256736225556-How-does-AllTrails-calculate-the-length-of-a-verified-trail https://www.hikingproject.com/help/21/overview-of-site-name-features https://training.caltopo.com/all_users/objects/existing-lines
- Do not overwrite multiple names into one opaque string. Preserve official name, alternate name, reference, operator, source, and the object to which each name applies. OSM’s relation-level `name` and `ref` model supports this separation. https://wiki.openstreetmap.org/wiki/Relation:route
- Do not copy expensive editorial systems before proving the identity model. Start with explicit geometry, route references, evidence records, source URLs, and status timestamps; add curation and user content as separate layers. This is an INFERENCE from the documented separation used by Hiking Project, AllTrails, COTREX, and FarOut. https://www.hikingproject.com/mapping https://support.alltrails.com/hc/en-us/articles/30315531476628-How-does-a-trail-end-up-on-AllTrails https://cpw.state.co.us/news/05192023/cotrex-app-verified-source-trail-info-colorado-public-lands https://faroutguides.com/features/

## Unknowns

- Trailforks and Komoot could not be directly read through the available retrieval path; their identity, overlap, metric, difficulty, and source models remain unknown in this session.
- AllTrails’ current difficulty-rating algorithm was not retrieved.
- Gaia’s difficulty assignment, closure model, and overlap handling were not retrieved.
- onX Backcountry and onX Offroad do not document enough in the retrieved pages to establish their segment graph, alias model, or metric formulas.
- FarOut does not document its difficulty method, alias model, or exact elevation/distance calculations in the retrieved sources.
- COTREX does not document its trail splitting, overlap, alias, or difficulty model in the retrieved sources.
- CalTopo’s underlying map-source attribution for snap-to features was not established by the retrieved training pages.
- OSM documentation retrieved here does not define a universal elevation, grade, closure, or difficulty computation.
- No retrieved product documentation establishes a reliable cross-product standard for “one trail,” “one route,” or “one name.”

## Recommendation

For Ohvernight, use a three-layer identity model:

1. Physical segment — geometry, segment identifier, surface/type, agency/operator source, and evidence-backed access or restriction records.
2. Named route — a named itinerary referencing ordered physical segments, with official name, alternate names, reference, operator, direction, and route-source evidence.
3. User plan or track — user-created or recorded geometry, explicitly non-authoritative unless separately reviewed.

Compute length, elevation gain, and grade from the stored geometry with a visible method and timestamp. Store permission, closure, seasonal status, and permitted-use claims as separate evidence records tied to an agency or operator URL. Treat missing evidence as unknown, never as allowed or open.
