# Source matrix

Candidate sources for water geometry, identity and recreation information.
Detail and URLs for every row are in Hermes
[track A](hermes/track-a-authoritative-water-sources.md) and
[track C](hermes/track-c-recreation-signals.md). "Checked" means the
coordinator read the service or page directly on 2026-10-06.

## Geometry and identity

| Source | What it gives | Licence as found | Freshness | Recreation or access meaning | Role proposed | Checked |
|---|---|---|---|---|---|---|
| USGS NHD (MapServer layers 6, 9, 12) | Lines and polygons with type codes, perennial or intermittent status, GNIS id and name, length, area, reach code | Public domain; USGS asks for acknowledgement | Retired 1 October 2023, no longer maintained | None | Canonical for M4 (already the source in both regions) | Schema and counts: yes |
| USGS 3DHP (`3DHP_all`, layers 50, 60) | Current national hydrography with `id3dhp`, `mainstemid`, GNIS id, stream order | "None. All data are open and non-proprietary." | Service says refreshed 4 September 2026 | None | Planned successor; not canonical yet | Schema: yes. Coverage of the two regions: no |
| USGS NHDPlus HR | NHD plus stream order, drainage area, mean annual flow, level path | Public domain | Service data from October 2022; no longer maintained | None | Optional ranking attributes | No |
| USGS GNIS | Official names and a unique feature id | Public domain | Refreshed every other month | None | Identity and grouping key, through `gnis_id` | No |
| Colorado DWR / CDSS | Structures, reservoirs and dams with a `wdid`, type and GNIS id | Not established; anonymous API limit 1,000 calls a day | Per-record `modified` | None; water administration | Possible later cross-reference for reservoirs | No |
| Pitkin County GIS | County streams and waterbodies with a type and flow category | Not found | Not stated | None | Reference only | No |
| Douglas County GIS | County streams and lakes | County guidance says no licence restriction | Not stated | None | Reference only | No |
| OpenStreetMap | Community-mapped water and tags | ODbL: attribution and share-alike | Continuous | Community tags only | Comparison only, kept out of canonical data | No |

## Official recreation information

| Source | What it supports | Describes | Join to a water feature | Machine-readable | Licence as found | Role proposed | Checked |
|---|---|---|---|---|---|---|---|
| CPW Fishing Atlas | Fishing information points, boat ramps, special regulations, Gold Medal waters, water-code streams and waterbodies | Existence and designation; the atlas itself warns that anglers must know where private property is | Water code may allow a keyed join; field schemas not retrieved. Otherwise spatial | Yes: ArcGIS REST | Marketplace catalogue labels it "Public Domain"; dataset terms not confirmed | First recreation source to probe | Service exists with 17 layers: yes |
| CPW Gold Medal streams | Gold Medal designation on a described segment | Designation of fishery quality, not access | Geometry and prose endpoints; no GNIS id | Yes | CPW item text advises care in interpretation; licence not stated | Enrichment | No |
| CPW watercraft inspection stations | A named ramp, its open or closed status, hours and restrictions | Facility existence and current status | Name and distance, reviewed | Yes | Blank licence field | Enrichment; status is volatile | No |
| CPW stocking report | A recent stocking at a named water | An event; not access | Name | HTML table | Not found | Link out, or later | No |
| CPW state park pages | Activities, seasons and closures at a park | Permission and restriction, in prose | By hand | No | Not found | Reviewed claim source | Chatfield wording: via Hermes only |
| USFS recreation opportunities and sites | Recreation areas, activities, facilities, status, restrictions | Facility and activity existence at a point | `RECAREAID`; spatial to water | Yes; nightly | "intended for public use and distribution"; not to be used to determine ownership or restrictions | Enrichment | No |
| Recreation.gov RIDB | Federal recreation areas and facilities | Existence | RIDB ids | Yes; key required | Revocable API agreement; rate limits possible | Already used for campgrounds; no new use proposed | No |
| Pitkin County Open Space points | River access points, launches, parking, season, closures | Facility existence at a point | Spatial, short distance, reviewed | CSV | Not found | Enrichment for Aspen, after a licence answer | No |
| Operator pages (Denver Water, Douglas County, Aurora, Parker Water) | What is allowed and prohibited at one water | Permission and restriction, in prose | By hand, by name and operator | No | Not found | Reviewed claim source; the highest authority for one water | Cheesman and Strontia Springs: yes |
| CWCB environmental and recreation service | Boating and Gold Medal attributes on streams | Unknown | Unknown | Token required or not found | Unknown | Do not use | No |

## Disagreements and gaps between the reports

- Track A recommends 3DHP as canonical geometry. Track B reports that 3DHP
  collapses the type distinctions M4 needs. The coordinator's proposal keeps
  NHD for M4 and plans the move; see
  [recommendations.md](recommendations.md).
- Tracks A and C cite different Fishing Atlas service URLs
  (`FishingAtlas/FishingAtlas_Data` and `FishingAtlas2025/FishingInfo2025`).
  The coordinator confirmed the first exists and lists boat-ramp, Gold Medal,
  special-regulation and water-code layers. Which is current is not settled.
- No source gives a statewide dataset of public water access. Access
  information exists per facility and per operator.
