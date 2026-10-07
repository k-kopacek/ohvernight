# Open questions for M4-B, from the dry runs

Raised by the read-only dry runs in this directory
([grouping-dry-run.md](grouping-dry-run.md),
[major-river-audit.md](major-river-audit.md),
[threshold-comparison.md](threshold-comparison.md)), run against the M4-A
canonical data. Nothing here is decided. Items marked **owner** need the
owner; items marked **coordinator** are clarifications the coordinator can
record as specification amendments, listed here so they are visible.

## Q1 — The South Platte River is not drawn at all in Douglas County (owner)

The approved rule (specification 8.3, owner decision O9) draws a river's
centre lines only where they connect to a perennial stream segment of the
same river. In the Douglas data the South Platte has no perennial stream
segment at all: it is 75 artificial-path segments (22.9 km by source length).
The 80 m perennial segment the specification mentions came from a
bounding-box probe and lies outside the county.

Two further facts:

- The county boundary follows the river, so clipping to the county cuts it
  into 43 disconnected pieces; only about 9.5 km of its geometry is inside
  the county.
- Douglas has no NHD area layer, so the wide-river polygons those centre
  lines run through are not in the data. Three of the seven referenced
  waterbodies are present (Cheesman Lake, Chatfield Lake, Strontia Springs
  Reservoir).

O9 says: if a major river is missing, stop and report; do not weaken the
rule. This is that report, made before M4-B starts.

Alternatives:

1. **Fetch the Douglas NHD area layer and let the area's own category decide.**
   A centre line is drawn when it runs through an area or waterbody that the
   source codes as a perennial stream or river (or a displayed lake). Needs a
   second, small controlled NHD request for Douglas layer 9, a rule
   amendment, and a decision on the clipping below. Most faithful to the
   source.
2. **Pad the Douglas water extent** so that a river forming the county
   boundary is not cut into fragments (Aspen already uses a 0.005 degree
   padding for water). Changes what is stored and shown at the county edge.
   Probably needed together with 1.
3. **A reviewed inclusion** for the South Platte group, with the area
   polygon's source category as its evidence. Works today without a new
   fetch, but the result is still 43 fragments.
4. **Accept that the South Platte is not shown in M4** and list it as a known
   gap. Not recommended: it is the principal river of the county and runs
   through three of the waters that M4-C will describe.

Recommendation: 1 with 2, as a small amendment to M4-B, with the extra
request authorised explicitly.

The same mechanism would also restore Happy Canyon Creek (7.2 km, artificial
path only), Kinney Creek (4.7 km) and the truncated East Cherry Creek and
Willow Creek, where they run through perennial areas.

## Q2 — Named connectors carrying the river's own GNIS id (coordinator; reported to owner)

Hunter Creek (on the expected list) and Galena Creek each split into two
groups 19 m and 139 m apart. In both cases the source joins the two reaches
with a *connector* segment that carries the same name and `gnis_id`. The
specification excludes connectors from grouping, and admits them only as
"supporting features", which M4-A defined for Douglas only.

Owner decision O2 allows a hidden source reach to establish continuity when
identity agrees, source topology supports it, no unrelated branch is absorbed
and nothing is invented. A connector with the river's own `gnis_id` meets all
four. Proposed clarification: a connector or other non-drawn flowline that
carries the group's `gnis_id` may be used for connectivity, in both regions;
it is never drawn and never selectable. Canals and pipelines stay excluded
even with a matching id.

## Q3 — Rivers cut by the extent edge (owner)

Granite Creek (Aspen) becomes three groups of 4.2, 0.7 and 0.6 km, all ending
on the east edge of the extent, because the river leaves and re-enters. O2
forbids joining across extent-edge gaps, and the rule is followed. The result
is three tappable features with one name. Alternatives: accept (recommended
for M4); or hide parts under a minimum drawn length; or treat parts of one
`gnis_id` as one logical group with several drawn lines when the only gaps
are at the extent edge. The last two change the approved rule.

## Q4 — Length shown for a river (coordinator)

`length_km` from the source is the unclipped segment length. Summing it
overstates rivers at the extent edge (Granite Creek: 4.15 km stated, 0.87 km
drawn; Aspen total 534 km by attribute, 514 km by geometry). Proposed
clarification: the length shown under "Computed by Ohvernight", the ordering
of parts, and the expected-river fraction are computed from the drawn
geometry, not from the source attribute. The source attribute stays in
canonical data.

## Q5 — What the expected-major-rivers fraction measures (coordinator)

The specification says "a minimum drawn fraction of the river's named length
inside the extent". Proposed clarification: per `gnis_id`, drawn geometric
length divided by the geometric length of all its stream and artificial-path
segments inside the extent that the rule could draw if connected (perennial
stream plus artificial path), counting every group of that `gnis_id`. The
proposed fixture is in [major-river-audit.md](major-river-audit.md). Rivers
that fail today: South Platte (absent), East Cherry Creek (0.72), Willow
Creek (0.78). The Fryingpan River is not in the Aspen data and is not listed.

## Q6 — Very short intermittent slivers (owner, low priority)

Seven Douglas streams are drawn as two lines because a single segment of 7 to
85 m is coded intermittent (East Plum Creek: one 85 m segment in 54 km). The
group and its identity are intact; there is a small visible gap. The rule
has no exception and none is proposed. Mentioned so the owner is not
surprised on the device.

## Q7 — The 2 hectare threshold (owner, already scheduled)

At 2 ha Aspen shows 3 unnamed lakes; at 0.5 ha, 47. Elevation is recorded for
only 10 Aspen waterbodies, so "alpine lakes" cannot be picked out from the
data; the 44 between 0.5 and 2 ha are listed with coordinates in
[threshold-comparison.md](threshold-comparison.md) for the owner to look at.
The provisional threshold is unchanged.

## Q8 — Estimates in the specification that the real data corrects (coordinator)

Section 23 of the specification estimated 62 and 56 stream groups; the clipped
data gives 71 (Aspen) and 35 (Douglas). The Roaring Fork example
`member_count` is 111, not 96. Waterbodies at 2 ha are 46 and 32, not 42 and
37. These are corrections to estimates, to be recorded with M4-B.
