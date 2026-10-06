# Field semantics: what separates useful water from clutter

Question: which source-backed characteristics distinguish water a person
might use for recreation from hydrology clutter?

Sources: Hermes track B
([report](hermes/track-b-water-semantics.md)), and the coordinator's own
read of the live service metadata and a read-only statistics probe on
2026-10-06.

## Checked independently

The coordinator read the service metadata directly and confirms:

- The NHD service the pipeline already uses,
  `https://hydro.nationalmap.gov/arcgis/rest/services/nhd/MapServer`, exposes
  on layer 6 (flowline): `permanent_identifier`, `gnis_id`, `gnis_name`,
  `lengthkm`, `reachcode`, `ftype`, `fcode`, `visibilityfilter`,
  `wbarea_permanent_identifier`, `mainpath`, `innetwork`; and on layer 12
  (waterbody): `PERMANENT_IDENTIFIER`, `GNIS_ID`, `GNIS_NAME`, `AREASQKM`,
  `ELEVATION`, `REACHCODE`, `FTYPE`, `FCODE`, `VISIBILITYFILTER`, with
  subtypes Reservoir 436, LakePond 390, SwampMarsh 466, Playa 361, Ice Mass
  378, Estuary 493.
- The 3DHP service exists at
  `https://hydro.nationalmap.gov/arcgis/rest/services/3DHP_all/MapServer`
  (layer 50 flowline, 60 waterbody) with `id3dhp`, `mainstemid`, `gnisid`,
  `gnisidlabel`, `featuretype`, `featuretypelabel`, `lengthkm`,
  `waterbodyid3dhp`, `streamorder`, `levelpath`. Its credit line reads
  "Data refreshed September 4, 2026".

Not checked independently: the meaning of each `FCode` value (taken from
Hermes's reading of the USGS data dictionary), and the NHD-to-3DHP crosswalk.

## What the type codes mean

From the USGS NHD data dictionary, as retrieved by Hermes:

| Kind | `ftype` | Codes that matter |
|---|---|---|
| Stream or river | 460 | `46006` perennial, `46003` intermittent, `46007` ephemeral, `46000` unknown |
| Canal or ditch | 336 | `33600`, `33601` aqueduct |
| Pipeline | 428 | several |
| Connector | 334 | network link, not a water feature a person sees |
| Artificial path | 558 | modelled centre line through a lake or wide river |
| Lake or pond | 390 | `39004`, `39009` to `39012` perennial; `39001`, `39005`, `39006` intermittent |
| Reservoir | 436 | `43613` to `43617`, `43621` water storage; `43624` treatment; `43601` aquaculture; tailings, evaporator, sewage and others |
| Swamp or marsh | 466 | |

## Real counts in the two regions

Read-only statistics from the NHD service for each region's bounding box
(features intersecting the box, so slightly more than the clipped repository
data). Raw output:
[existing-data-audit-facts.md](existing-data-audit-facts.md) describes the
repository side; the probe output is reproduced here.

### Flowlines that carry a name (what the map shows today)

| Type | Aspen pieces | Aspen km | Douglas pieces | Douglas km |
|---|---:|---:|---:|---:|
| Stream or river, perennial `46006` | 1,087 | 485 | 2,026 | 536 |
| Stream or river, intermittent `46003` | 79 | 25 | 807 | 284 |
| Artificial path `55800` | 124 | 18 | 670 | 140 |
| Canal or ditch `336xx` | 97 | 95 | 84 | 110 |
| Pipeline `428xx` | 7 | 27 | 15 | 43 |
| Connector `33400` | 3 | 0.2 | 1 | 0.1 |

No named flowline in either region is coded ephemeral.

### All flowlines, named or not

| Type | Aspen pieces | Aspen km | Douglas pieces | Douglas km |
|---|---:|---:|---:|---:|
| Perennial stream `46006` | 1,384 | 664 | 2,671 | 673 |
| Intermittent stream `46003` | 1,647 | 811 | 16,012 | 4,682 |
| Ephemeral stream `46007` | 2,244 | 877 | 15,158 | 3,285 |
| Artificial path | 430 | 41 | 2,788 | 312 |
| Canal or ditch | 158 | 141 | 119 | 135 |
| Pipeline | 9 | 29 | 26 | 77 |
| Connector | 60 | 2 | 29 | 5 |

### Waterbodies

| Type | Aspen all | Aspen named | Douglas all | Douglas named |
|---|---:|---:|---:|---:|
| Lake or pond, perennial `39004` | 365 | 31 | 761 | 10 |
| Lake or pond, perennial with stage `39009`, `39011` | 10 | 8 | 16 | 7 |
| Lake or pond, intermittent `39001`, `39005` | 31 | 0 | 1,463 | 18 |
| Lake or pond, unknown `39000` | 3 | 0 | 0 | 0 |
| Reservoir, any purpose `436xx` | 5 | 0 | 35 | 1 |
| Swamp or marsh | 54 | 0 | 1 | 0 |

## What this shows

1. **Type codes remove real clutter from the lines.** Canals, ditches,
   pipelines and connectors are about 122 km of the named lines shown in
   Aspen and 153 km in Douglas. They can be excluded on a source field, with
   no keyword matching on names.
2. **Perennial against intermittent is a usable, honest distinction.** In
   Douglas 807 named pieces (284 km) are intermittent streams. They need not
   be hidden, but they can be shown as intermittent or left out of the
   default view.
3. **Artificial paths should not be separate tappable things.** They are the
   modelled line through a lake or wide river. They matter for joining a
   river's pieces together and should not appear as their own feature.
4. **Reservoir purpose codes will not solve the Douglas reservoir clutter.**
   Hermes track B expected the reservoir purpose code to separate water
   storage from treatment and detention structures. The counts show that
   almost every *named* waterbody in both regions is coded as a lake or pond
   (390), including features named "… Reservoir" and "… Detention Number …
   Reservoir". Only one named Douglas waterbody is coded 436. So the
   reservoir purpose code is useful where present and nearly absent where it
   is needed. Detention and supply structures have to be handled another way:
   by size, by intermittent status (18 of the 36 named Douglas waterbodies
   in the probe are intermittent lake or pond), and by official recreation evidence.
5. **One stream is one GNIS name application.** All pieces of the Roaring
   Fork River share one `gnis_id` (retrieved by Hermes; not re-run by the
   coordinator). `gnis_id` is the grouping key that is present today; 3DHP
   adds `mainstemid`.
6. **Names are sparse on waterbodies.** In Aspen 39 of 409 lakes and ponds
   carry a name. A name is a reasonable aid to discovery and labelling. It is
   not evidence of usefulness, and requiring one hides most alpine lakes.

## What none of these fields says

No field in NHD, NHDPlus HR or 3DHP states ownership, public access, or
permission to fish, boat, swim, park or camp. Perennial does not mean usable
today. "Water storage" does not mean open to the public. Every feature
selected on these fields is physical water with access and permitted
activities unknown until a separate official source says otherwise.

## 3DHP and the type codes

Hermes reports, from the USGS crosswalk tables, that 3DHP collapses lake,
pond and every reservoir subtype into one "Lake" type, and collapses
perennial, intermittent and ephemeral streams into one river type. If that is
right, 3DHP alone cannot reproduce the perennial and intermittent distinction
above. The coordinator has not verified the crosswalk. It matters for the
choice of canonical source and is listed as an open question in
[recommendations.md](recommendations.md).

## Unknown

- How completely `fcode`, `gnis_id` and `visibilityfilter` are populated
  across each region. The statistics above show the codes are populated for
  every feature counted; names are not.
- Whether NHDPlus HR stream order, drainage area and mean annual flow are
  populated for the two regions. Hermes's queries timed out.
- Whether `permanent_identifier`, `reachcode` or `id3dhp` are guaranteed
  stable across releases. Hermes found USGS statements that a
  `permanent_identifier` can change on edit.
