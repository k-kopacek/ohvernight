# Existing data audit: the water Ohvernight shows today

Sources: counts computed by the coordinator from `main` at `b45ca59`
([existing-data-audit-facts.md](existing-data-audit-facts.md)); Hermes track
E's interpretation of those counts and its checks of named features
([report](hermes/track-e-current-water-audit.md)); the type-code counts in
[field-semantics.md](field-semantics.md).

## What is there

| | Aspen | Douglas County |
|---|---|---|
| Canonical water features | 6,926 (6,411 line pieces, 515 polygons) | 2,392 (2,359 line pieces, 33 polygons) |
| Unnamed | 5,371 | 0 — only named features were ever fetched |
| Shown on the map | 1,555: every named feature | 2,392: everything |
| Distinct names shown | 134 | 69 stream names, 33 waterbody names |
| Display artifact size | 1.13 MB | 0.12 MB waterbodies; waterways separately |
| Source | USGS NHD MapServer, layers 6, 9, 12 | USGS NHD MapServer, layers 6, 12 |

## Problems, in order of effect on a user

1. **One stream is many tappable pieces.** Roaring Fork River is 112
   features; East Plum Creek 183. A repeated name averages about 16 pieces in
   Aspen and about 42 in Douglas. About half of all pieces are shorter than
   250 m. Tapping "a river" selects a fragment.
2. **Infrastructure is shown as water to visit.** By source type code, named
   canals, ditches and pipelines are about 122 km of the lines shown in Aspen
   and 153 km in Douglas. The longest "stream" in Douglas is the Arapahoe
   Canal at 62 km. Salvation Ditch (20 km) is an irrigation ditch run by a
   ditch company (Hermes, citing the Aspen Times).
3. **Douglas waterbodies are mostly not places to go.** 30 of 33 names
   contain "Reservoir"; many are "Franktown Parker FP…" and "West Cherry
   Creek Detention Number …" structures. Half the named waterbodies in the
   probe are coded intermittent. No manager or recreation status is carried:
   the `manager` field is null on every water feature.
4. **The features that matter are indistinguishable from the rest.**
   Chatfield Lake, Cheesman Lake, Rueter-Hess Reservoir and Strontia Springs
   Reservoir look the same as a detention pond, and carry nothing about what
   their operators allow.
5. **Useful water is hidden in Aspen.** Selection by name shows 39 of about
   409 lakes and ponds. The other 370 unnamed lakes and ponds are not shown.
   Many are very small, and some are alpine lakes a hiker would look for.

## How much is clutter

Hermes track E estimates 50 to 70% of the Aspen display and 70 to 90% of the
Douglas display is clutter or ambiguous, by feature count. Those are inferred
ranges, not measurements, and they count fragments.

The type-code counts allow a firmer statement for the lines. Of the named
line pieces shown:

| | Aspen | Douglas |
|---|---:|---:|
| Perennial stream or river | 1,087 pieces, 485 km | 2,026 pieces, 536 km |
| Intermittent stream | 79, 25 km | 807, 284 km |
| Artificial path through a waterbody | 124, 18 km | 670, 140 km |
| Canal, ditch, pipeline, connector | 107, 122 km | 100, 153 km |

So by length about 19% of the Aspen lines and 14% of the Douglas lines are
infrastructure, and a further 4% and 25% are intermittent streams. The
larger part of the clutter a user feels is fragmentation, which grouping
fixes without removing any water.

## What the pipeline discards

The fetch keeps a name and which service layer a feature came from. It
discards, although the service returns them: feature type and code
(`ftype`, `fcode`), GNIS id, permanent identifier, reach code, length, area,
elevation, visibility filter, and the link from an artificial path to its
waterbody. Feature IDs are built from the service row number (`OBJECTID`),
which is not a stable identifier.

Douglas requests only named features, so the canonical Douglas data cannot
answer "what unnamed water is here".

## What must not be broken

- Aspen's full hydrology (all 6,926 features) is an input to setback
  screening for dispersed-camping corridors
  (`v2/pipeline/scripts/07_build_dispersed_corridors.py`). Canonical data and
  display selection are separate; thinning the canonical layer would change a
  safety screen.
- Display rules R61 to R63 require each display feature to equal a canonical
  feature, with the only permitted exclusion being the current water
  selection rule. Grouping pieces and changing the selection rule both need a
  contract change.
- The Aspen and Douglas default-on payloads are 3.81 MB and 3.62 MB against a
  4.5 MB limit. Water enrichment has to fit; removing clutter and fragments
  from the display artifact gives room.

## Named features checked

From Hermes tracks C and E. The coordinator re-read the two Denver Water
pages and confirms the wording.

| Feature | What an official source says | Status for Ohvernight |
|---|---|---|
| Chatfield Lake | CPW state park: boating, paddleboarding, fishing, ramps, seasonal swim beach; closed to all boats 1 December to ice-off | Official recreation information exists |
| Cheesman Lake | Denver Water: fishing only on the Goose Creek Arm; all boating and camping prohibited; water-contact sports prohibited; foot access only | Restricted. A wrong positive here would be harmful |
| Strontia Springs Reservoir | Denver Water: boating not permitted; body contact with water prohibited | Restricted |
| Rueter-Hess Reservoir | Douglas County: recreation by reservation on set days, with craft and fishing restrictions | Official information exists, tightly conditioned |
| Ruedi Reservoir | USFS: boating, fishing, ramp; inspection required | Official recreation information exists (outside the current Aspen extent) |
| Roaring Fork and Fryingpan Rivers | CPW Gold Medal designation on named segments | Fishery designation only; says nothing about bank access |
| Maroon Lake, Snowmass Lake | USFS: access reservations and wilderness permits | Water use unknown |
| Grizzly Reservoir, Wildcat Reservoir | No official recreation page found | Unknown |
| Aurora-Rampart Reservoir | Not found under that name | Unknown |
| Franktown Parker and West Cherry Creek Detention reservoirs | No manager or recreation source found | Unknown; almost certainly not destinations |
| Salvation Ditch, Arapahoe Canal, High Line Canal | Irrigation and supply infrastructure; High Line Canal has a trail beside it | Not recreational water |
