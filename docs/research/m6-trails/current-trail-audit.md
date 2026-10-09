DRAFT - UNREVIEWED

# M6 input — what the repository holds for trails today

Read-only audit, 2026-10-07. Measured from the files in the
`m4a-source-preservation` worktree at `aa5c20b`: `v2/trails.geojson` (sha256
`65f1fbd1…`, Aspen), `v2/regions/douglas-co/research.json` (`cf7e6852…`,
`/layers/trails`), the MVUM road layers, the display artifacts, both
manifests, the fetch scripts and `v2/explore/`. No network request was made.
Lengths are computed in NAD83 / UTM 13N (EPSG:26913) and are lengths of the
clipped geometry in the files, not trail lengths. Nothing here is a decision.

Statements are marked **VERIFIED** (measured or read from a file),
**INFERENCE** or **UNKNOWN**. Candidate sources and the COTREX terms question
are in `docs/research/future-sources/source-watchlist-m5-m8.md` and are not
repeated.

## Key findings

1. **A feature is a source segment, not a trail.** Aspen has 123 features
   for 87 trail numbers; Douglas has 102 for 78. In Aspen 62 features (half)
   share their name with another feature; in Douglas 36 do. (VERIFIED.)
2. **In Aspen, name and number agree perfectly and every same-name set is
   connected.** 87 names, 87 numbers, one-to-one; all 26 multi-feature names
   join end to end at six decimals. Difficult Creek is the typical case, not
   a special one: two features, `usfs-trail-8921819` (4,025 m) and
   `usfs-trail-8923909` (1,232 m), both number 2146, sharing an endpoint.
   Grouping by number and grouping by name-plus-connectivity give the same 87
   trails. (VERIFIED.)
3. **Douglas is where grouping gets hard.** The two rules give 78 and 83
   trails and disagree on 5 clusters covering 21 features. Four same-name
   sets are not connected (Colorado, Indian Creek, Trout Creek, Arrowhead),
   and one name spans two numbers (Turtle Mountain). (VERIFIED.)
4. **The overlapping-trails limitation is one parent record.** Douglas
   feature `usfs-trail-8913499` (Turtle Mountain, number 0770, 65.9 km)
   duplicates the geometry of six lettered children 0770.A–F; 64.1 km (97%)
   of it lies within 5 m of them. Douglas double-counts 61 km of line,
   almost all of it from this record. Aspen has one 129 m overlap between differently named trails.
   (VERIFIED.)
5. **No stable trail identifier is kept.** Ids are `usfs-trail-<OBJECTID>`.
   The source's trail key is not stored, although the road layers do store
   their route key. Saved plans, GPX names and any future grouping table rest
   on a service row number. (VERIFIED that it is not kept; stability of
   `OBJECTID` is UNKNOWN.)
6. **Use and season are published verbatim and are thin for foot travel in
   Douglas.** 84 of 102 Douglas features give "Use permission unknown" for
   hiking in the app's season check, and 40 of 102 are reported "Outside
   published use dates" for motorcycling in July because their window reads
   `12/01-03/14`. Whether that string means what the check assumes is
   UNKNOWN. (Counts VERIFIED.)
7. **A quarter of Aspen's trails are cut by the project rectangle.** 25 of 87
   trail numbers have a feature ending on the extent boundary, and eight
   features have internal gaps of 22–2,063 m where the trail leaves and
   re-enters. (VERIFIED.)

## 1. Source and fields

Both regions: USDA Forest Service
`EDW_TrailNFSPublishWithDataStatus_01/MapServer/0`, `outFields=*`, fetched by
`v2/pipeline/scripts/fetch_trails.py` (Aspen, clipped to the project
rectangle, 2026-09-25) and `fetch_douglas.py` (clipped to the county, using
the same `normalize`, 2026-09-27). Forest Service trails only; no county,
state, BLM or COTREX content. (VERIFIED.)

| Property | Source field | Notes |
|---|---|---|
| `id` | `OBJECTID` | prefixed `usfs-trail-` |
| `name` | `TRAIL_NAME` | upper case as published |
| `trail_number` | `TRAIL_NO` | string |
| `surface` | `TRAIL_SURFACE` | |
| `attribute_subset` | `ATTRIBUTESUBSET` | `TrailNFS_MGMT` on all 225 features |
| `allowed_terra_use` | `ALLOWED_TERRA_USE` | digit string, undecoded |
| `activities` | 9 activities × `MANAGED`, `ACCPT`, `DISC`, `RESTRICTED` | 36 strings, verbatim |
| `evidence` | pipeline | one retrieval timestamp per region |

42 source fields are read; everything else is dropped. The watchlist records
that the sibling service carries `TRAIL_CN`, `TRAIL_TYPE`, `TRAIL_CLASS`,
`ADMIN_ORG`, `MANAGING_ORG`, typical grade and tread width and an MVUM symbol;
none is kept here. Segment measures, published lengths, trail type and class,
managing unit and any national-trail designation are therefore absent.
(VERIFIED that they are absent; the exact field list of the service used is
UNKNOWN from repository evidence.) The app shows no length or elevation, by
the M3 rule that fields are never fabricated.

The same schema is used in both regions. Differences are in the manifest
only: Douglas declares `max_age_hours: 168`, Aspen `null`; neither has a
transport record (register item N1); layer titles are "Forest trails" and
"USFS trail segments"; the season check, GPX export and saved list are
enabled in Douglas only.

## 2. Counts and identity

| Measure | Aspen | Douglas |
|---|---|---|
| Features | 123 | 102 |
| LineString / MultiLineString | 111 / 12 | 91 / 11 |
| Features with a name | 123 | 102 |
| Features with a number | 123 | 102 |
| Number but no name; name but no number | 0; 0 | 0; 0 |
| Distinct names | 87 | 77 |
| Distinct numbers | 87 | 78 |
| Distinct base numbers (text before the dot) | 59 | 48 |
| Names on more than one feature (features involved) | 26 (62) | 11 (36) |
| Largest same-name set | 4 (Hunter Creek) | 10 (Colorado) |
| Same-name sets not connected at six decimals | 0 | 4 |
| Same-name sets not connected within 10 m | 0 | 4 |
| Features in those disconnected sets | 0 | 18 |
| Same name, different numbers | 0 | 1 (Turtle Mountain: 0770, 0770.E) |
| Same number, different names | 0 | 0 |
| Base numbers carrying more than one name | 14 | 16 |
| Names that are a number or a placeholder | 0 | 15 |
| Ids shared between regions | 0 | 0 |

All VERIFIED. Connectivity was tested four ways (shared endpoint at six
decimals; endpoints within 10 m; endpoint within 10 m of the other line;
lines within 10 m anywhere). The count of disconnected names is 4 under all
four; only Indian Creek changes, from 4 components at six decimals to 3 at
10 m.

Number formats (VERIFIED): Aspen `9999` ×72, `9999.9` ×36, `9999.9A` ×11,
`9A999` ×2 and two snow routes `SNO-130.3C`, `SNO-1472`. Douglas `9999` ×53,
`9999.A` ×32, `999` ×13, `999.A` ×3, `9999.AA` ×1. Douglas mixes `0681` with
`681.D` and `681.F`, so the base number is not consistently zero-padded. The
dotted suffix marks spurs, cut-offs and connectors that carry their own
names (INFERENCE from the names), for example base 1987 in Aspen: Sunnyside
(1987), Sunnyside Plunge Cutoff (.1), Sunnyside Plunge (.2), Secret Single
Track (.3), Smugglers Cutoff (.4).

Douglas placeholder names (VERIFIED): `787` ×2, `788`, `662`, `787.A`,
`673.A`, `681.B`, `681.C`, `681.E`, `682.AA`, `915 TRAIL`, `916 TRAIL`,
`917 TRAIL`, `918 TRAIL` (numbers 1915–1918) and `NO NAME` (0770.B). One
trail is named simply `LOOP` (0680).

## 3. Overlap and duplicate geometry

Test: for each ordered pair, the length of A lying within 5 m of B; reported
where it exceeds 50 m.

| Region | Differently named pairs | Features involved | Same-name pairs |
|---|---|---|---|
| Aspen | 1 | 2 | 0 |
| Douglas | 6 | 8 | 1 |

Aspen (VERIFIED): Graham Gulch `usfs-trail-8952771` (1506) and McNassar Gulch
`usfs-trail-8961619` (1505) share 129 m.

Douglas (VERIFIED), all against Turtle Mountain `usfs-trail-8913499` (0770,
65,935 m) except the last:

| Other feature | Number | Its length m | Share of it within 5 m of 0770 |
|---|---|---|---|
| Turtle Mountain `usfs-trail-8939521` | 0770.E | 25,357 | 100% |
| Devils Revenge `usfs-trail-8917600` | 0770.D | 15,031 | 94% |
| Skeleton `usfs-trail-8925194` | 0770.F | 11,551 | 100% |
| Tunnel `usfs-trail-8937765` | 0770.A | 10,477 | 98% |
| Devils Advocate `usfs-trail-8951157` | 0770.C | 3,020 | 85% |
| No Name `usfs-trail-8952194` | 0770.B | 209 | 100% |
| Powerline `usfs-trail-8979189` / Beginner `usfs-trail-8982355` | 0690 / 0627 | — | 72–79 m shared |

Children A–F sum to 65.6 km against the parent's 65.9 km. The parent is a
route-level record laid over its own segments. (INFERENCE from the
measurement.) `usfs-trail-8925194` and `usfs-trail-8952194` are the two
features the M3 specification records as unselectable from the line. The sum
of Douglas feature lengths is 413.9 km; the unioned network is 352.5 km.
Aspen: 339.1 km against 339.0 km.

Trails against MVUM roads (VERIFIED): in Aspen two snow routes are entirely
within 5 m of a mapped road — Bald Knob `usfs-trail-8915341` (SNO-130.3C)
and Schofield Pass Ski `usfs-trail-8932149` (9S317). In Douglas, Indian Creek
`usfs-trail-8970783` shares 397 m and Beginner `usfs-trail-8982355` 189 m
with a road. Names do not line up across layers: trail "PEEKABOO GULCH"
(1476) against road "PEAKABOO GULCH".

Connectivity alone cannot define a trail. 67 of 123 Aspen features and 74 of
102 Douglas features lie within 10 m of a differently named feature; the
whole Douglas layer forms 20 connected networks, the largest holding 60
features. (VERIFIED.)

## 4. Length and geometry

Clipped feature length in metres (VERIFIED):

| | Total km | Min | p10 | p25 | Median | p75 | p90 | Max | Under 100 m | Under 500 m |
|---|---|---|---|---|---|---|---|---|---|---|
| Aspen | 339.1 | 29 | 237 | 611 | 1,423 | 3,429 | 7,242 | 15,029 | 4 | 26 |
| Douglas | 413.9 | 26 | 163 | 471 | 1,722 | 4,804 | 10,477 | 65,935 | 6 | 28 |

Median vertex spacing is 15 m in both regions. Grouped by number, the median
trail is 2,271 m in Aspen and 2,435 m in Douglas.

Clipping (VERIFIED): 26 Aspen features, belonging to 25 of 87 trail numbers,
have an endpoint within 2 m of the project rectangle. Eight of Aspen's twelve
multi-part features have parts more than 10 m apart, all on the boundary:
Cooper Basin `usfs-trail-8932839` (5 parts, gaps to 2,063 m), Lost Man Loop
`usfs-trail-8920907` (4 parts, to 1,986 m), South Fork Lake Creek
`usfs-trail-8955533` (1,510 m), McNassar Gulch `usfs-trail-8961619` (665 m),
Nickelson Creek `usfs-trail-8923933` (451 m), Geneva Lake
`usfs-trail-8921344` (190 m), Trail Riders `usfs-trail-8964672` (26 m) and
Conundrum Creek `usfs-trail-8922773` (22 m). In Douglas only two Colorado
Trail features touch the county line, but three features have internal gaps
away from it: Turtle Mountain `usfs-trail-8913499` (6,528 m), Beginner
`usfs-trail-8982355` (410 m) and Arrowhead `usfs-trail-8970427` (327 m).

Display artifacts keep every feature and property; rounding to six decimals
drops one degenerate part each from `usfs-trail-8939494` (787) and
`usfs-trail-8966777` (Barr). (VERIFIED.)

Against other layers (VERIFIED): 228.8 km of Aspen's 339.1 km of trail is
inside designated wilderness; 47 features lie wholly inside and 24 cross the
boundary. 11.1 km of Aspen trail and 1.4 km of Douglas trail lie on the land
layer's `PVT` polygon.

## 5. Use, surface and season fields

| Field | Aspen (n = 123) | Douglas (n = 102) |
|---|---|---|
| `surface` | 123 present: native material 119, snow 3, imported loose 1 | 102 present: native material 98, imported compacted 4 |
| `allowed_terra_use` | 119 present: `21` ×74, `321` ×40, `1` ×5; null ×4 | 102 present: `54321` ×47, `321` ×20, `4321` ×16, `654321` ×13, `5321` ×4, `21` ×2 |
| Any activity string | 123 | 102 |

Features with at least one string for the activity (managed / accepted /
discouraged / restricted counts in brackets), VERIFIED:

| Activity | Aspen | Douglas |
|---|---|---|
| Hiking | 83 (23 / 62 / 1 / 0) | 75 (18 / 0 / 57 / 0) |
| Horseback riding | 110 (70 / 33 / 2 / 5) | 73 (15 / 1 / 57 / 0) |
| Mountain biking | 115 (30 / 5 / 0 / 80) | 76 (17 / 0 / 57 / 2) |
| Motorcycling | 119 (0 / 0 / 0 / 119) | 102 (16 / 60 / 0 / 26) |
| ATV | 119 (0 / 0 / 0 / 119) | 102 (51 / 13 / 0 / 38) |
| 4WD | 119 (0 / 0 / 0 / 119) | 102 (13 / 0 / 0 / 89) |
| Snowshoeing | 0 | 0 |
| Cross-country skiing | 4 | 0 |
| Snowmobiling | 4 | 0 |

Observations:

- `allowed_terra_use` is displayed as "Published uses: 321" with no key. The
  repository does not define the digits. (VERIFIED.) The data is consistent
  with 1 foot, 2 stock, 3 bicycle, 4 motorcycle, 5 ATV, 6 4WD: Tunnel
  `usfs-trail-8937765` is `4321` with motorcycling managed and ATV
  restricted, while its neighbour `usfs-trail-8941308` is `5321` with ATV
  managed and motorcycling restricted. (INFERENCE.)
- Nine distinct date strings in Aspen and seven in Douglas. All parse as
  month/day ranges; one value carries a trailing space (`01/01-12/31 `, 78
  occurrences in Aspen, 2 in Douglas) which the app's parser trims.
- No feature has a use window and a restriction on the same activity.
- In Douglas, 57 features give hiking, riding and cycling only a
  *discouraged* string. The season check ignores `disc` when there is no
  managed or accepted value and returns "Use permission unknown" — for
  hiking, 84 of 102 features.
- `12/01-03/14` appears 195 times in Douglas (motorcycling accepted ×38 and
  managed ×2, ATV managed ×38, and the matching discouraged strings). Read
  literally as a use window, 40 of 102 features are "Outside published use
  dates" for a July motorcycle trip and "Within published use dates" in
  January. Whether the source means a use season or the inverse is UNKNOWN
  and was not checkable offline.
- Four Aspen features lying more than 200 m inside wilderness carry no
  bicycle restriction string: Sugarbowl `usfs-trail-8913830` and Trail Riders
  `usfs-trail-8964672` (bicycle *managed* all year), and both Graham Gulch
  features (blank). (VERIFIED measurement; whether source or boundary is
  wrong is UNKNOWN.)
- Features of one trail differ. In Aspen 3 of 26 multi-feature trails have
  segments with different use profiles (East Snowmass Ditch, McNassar Gulch,
  Peekaboo Gulch: bicycle restricted on one segment, not on the next). In
  Douglas 4 of 11 do (Turtle Mountain, Tunnel, Arrowhead, Bear Mountain), and
  Colorado differs by surface. The other 23 Aspen splits show no difference
  in any kept field, so the source splits on something that was dropped.
  (VERIFIED counts; cause INFERENCE.)
- The Aspen snow routes (`SNO-…`, `9S317`) have null `allowed_terra_use` and
  only ski and snowmobile strings, and are drawn like every other trail.

## 6. How the app treats identity today

- Map, tap, highlight, detail, save and GPX all operate on one source
  feature. The detail says "Only the portion inside our research boundary is
  shown." (VERIFIED.)
- Trail search lists every feature under its name: 62 of 123 Aspen rows and
  36 of 102 Douglas rows repeat another row's label. Hunter Creek appears
  four times, Colorado ten. (VERIFIED.)
- One place already groups: `TrailDiscovery.nearbyTrails` keeps the first
  feature per `trail_number|name` key. So "nearby trails" is by number and
  name while search, map and detail are by segment. (VERIFIED.)
- GPX files are named from `trail_number`, so each segment of a trail
  downloads under the same filename with one segment inside. (VERIFIED.)
- Saved plans store `usfs-trail-<OBJECTID>`. (VERIFIED.)
- Labels are drawn per feature from zoom 14, so a multi-segment trail can be
  labelled several times. (INFERENCE from the code; not rendered here.)

## 7. Dry run of two grouping rules

Rule A: one trail per distinct `trail_number`. Rule B: features with the same
name that are connected through endpoints within 10 m. No feature lacks a
name or a number, so neither rule produces fallback singletons.

| | Features | Rule A | Rule B (10 m) | Rule B (six decimals) | Name only | Base number |
|---|---|---|---|---|---|---|
| Aspen | 123 | 87 | 87 | 87 | 87 | 59 |
| Douglas | 102 | 78 | 83 | 84 | 77 | 48 |
| Both | 225 | 165 | 170 | 171 | 164 | 107 |

Aspen: the partitions are identical; 26 groups have more than one feature.
(VERIFIED.)

Douglas: 72 groups are identical; A has 6 groups B does not, B has 11 that A
does not; they disagree in five places (VERIFIED):

| Trail | Features | Rule A | Rule B | What separates them |
|---|---|---|---|---|
| Colorado, 1776 | 10 | 1 trail, 18.2 km | 3 trails | gaps of 22 m and 866 m; the larger gap's midpoint is on the `PVT` land polygon |
| Indian Creek, 800 | 4 | 1 trail, 18.1 km | 3 trails | gaps of 501 m and 1,173 m, midpoints on `PVT` |
| Turtle Mountain, 0770 and 0770.E | 3 | 2 trails | 1 trail, 91.3 km of line | same name; 0770.E wholly overlaps 0770 |
| Trout Creek, 0649 | 2 | 1 trail | 2 trails | 1,086 m apart; Trout Creek Connection (0649.A) runs between |
| Arrowhead, 0646 | 2 | 1 trail | 2 trails | 62 m apart; trail `788` passes within 1 m of the gap |

Neither rule looks at overlap, at the lettered children of a base number, at
similarly named trails, or at trails cut by the boundary; both therefore
agree, and may both be wrong, on those.

### The ten hardest cases

1. **Turtle Mountain, Douglas.** `usfs-trail-8913499` (0770, 65.9 km, three
   parts with a 6.5 km gap) duplicates children 0770.A–F; `usfs-trail-8939521`
   (0770.E) has the parent's name; `usfs-trail-8953147` is a 30 m fragment of
   0770 with a different motorcycle season. Is 0770 a trail, a route, or a
   system? Rule A makes two trails, rule B one of 91 km.
2. **Colorado Trail, Douglas.** Ten features, three components, clipped twice
   at the county line, gaps over land the land layer calls `PVT`, surface
   changing between segments. A user means one long-distance trail that
   leaves the county and the Forest Service data.
3. **Indian Creek, Douglas.** `usfs-trail-8977816` and `usfs-trail-8970783`
   join only within 10 m, not at six decimals; `usfs-trail-8968633` and
   `usfs-trail-8982425` sit 0.5–1.2 km away across `PVT`; 397 m follows a
   road.
4. **Arrowhead, Douglas.** `usfs-trail-8964639` (season `05/16-11/30`) and
   `usfs-trail-8970427` (`12/01-03/14`) are 62 m apart with opposite
   published seasons. Grouping them forces a choice of which season the
   trail shows.
5. **Tunnel, Douglas.** `usfs-trail-8937765` (motorcycle) and
   `usfs-trail-8941308` (ATV, 274 m) are connected and share a number but
   allow different vehicles; the first is also 98% coincident with 0770.
6. **Trout Creek and Trout Creek Connection, Douglas.** Same base number,
   similar names, the "connection" (`usfs-trail-8928020`, 3.0 km) is longer
   than either Trout Creek feature and fills their gap.
7. **Conundrum and Conundrum Creek, Aspen.** `usfs-trail-8916487`
   (Conundrum, 9981, ending on the boundary) and Conundrum Creek (1981,
   `usfs-trail-8922773`, `usfs-trail-8925147`), 1.7 km apart inside the
   extent. Copper Creek (9983, three features) against East Maroon (1983)
   shows the same 9xxx/1xxx pattern. This looks like one trail numbered by
   two administrative units. (INFERENCE.) Neither rule joins them.
8. **Graham Gulch and McNassar Gulch, Aspen.** 129 m of shared tread under
   two names and numbers; McNassar `usfs-trail-8961619` has a 665 m internal
   gap at the boundary; segments differ on bicycle use.
9. **Lost Man Loop and Cooper Basin, Aspen.** Single features broken into
   four and five parts by the project rectangle, with gaps to 2 km. A
   "loop" that is not closed in the data. Cooper Basin also runs 2.0 km over
   `PVT`.
10. **The 1987 and 1992 families, Aspen.** Sunnyside with four named
    offshoots; Hunter Valley with Upper Hunter Valley and four spurs of
    133–217 m (South Spur, North Spur, McCloskey Lot, Lazy Man Short Cut).
    Grouping by base number gives 59 Aspen trails and merges trails people
    name separately; not grouping leaves 130 m stubs as trails in their own
    right. Hunter Creek (2194) and Hunter Valley (1992) are different trails
    with near-identical names.

## 8. Problems

Classification: DATA GAP, TRUST ISSUE, OWNER DECISION, IMPLEMENTATION DETAIL,
FUTURE TECH DEBT.

| # | What | Evidence | Class |
|---|---|---|---|
| T1 | No stable source trail identifier is stored | ids are `usfs-trail-<OBJECTID>`; roads keep `source_route_id`, trails nothing equivalent | DATA GAP |
| T2 | Segment-defining attributes are dropped | 23 of 26 Aspen splits show no difference in any kept field | DATA GAP |
| T3 | Forest Service only; trails end at the forest and at the clip | manifest gaps; Colorado and Indian Creek gaps over `PVT`; 25 of 87 Aspen trails cut | DATA GAP |
| T4 | The same trail is presented as several unrelated results | 62 of 123 and 36 of 102 search rows repeat a label | IMPLEMENTATION DETAIL until grouping is decided, then OWNER DECISION |
| T5 | Two identity rules already coexist in the app | "nearby" groups by number and name; everything else is per segment | FUTURE TECH DEBT |
| T6 | A route-level record overlaps its own segments | 0770 against 0770.A–F, 64.1 km | OWNER DECISION (which record is the trail) |
| T7 | Segments of one trail carry different uses and seasons | 3 of 26 Aspen, 4 of 11 Douglas | TRUST ISSUE if grouped without showing the difference |
| T8 | Season strings may not mean what the check assumes | `12/01-03/14` ×195; 40 of 102 "outside published use dates" in July | TRUST ISSUE |
| T9 | "Discouraged" becomes "unknown" for foot, stock and bicycle | 84 of 102 Douglas features for hiking | TRUST ISSUE |
| T10 | `allowed_terra_use` shown as raw digits | "Published uses: 321" | DATA GAP (no decoded meaning in the repository) |
| T11 | Placeholder and generic names | 15 Douglas names such as `787`, `NO NAME`; `LOOP` | OWNER DECISION (what a user-facing name is) |
| T12 | Winter routes are styled and listed as trails | 4 Aspen snow routes, 2 lying on roads | OWNER DECISION |
| T13 | Published wilderness and bicycle strings disagree | 4 Aspen features | TRUST ISSUE |
| T14 | No published length; clipped geometry is the only length available | M3 specification; section 4 | DATA GAP |
| T15 | Trail and road names for the same place differ | Peekaboo / Peakaboo | IMPLEMENTATION DETAIL |
| T16 | No transport record; freshness policy differs by region | N1; `null` against 168 h | OWNER DECISION |
| T17 | GPX filename collides across segments of one trail | named from `trail_number` | IMPLEMENTATION DETAIL |
| T18 | Saved plans depend on `OBJECTID` | storage keys hold feature ids | FUTURE TECH DEBT |
| T19 | Number formatting is inconsistent | `0681` against `681.D` | IMPLEMENTATION DETAIL |

## Questions for the owner

1. For Difficult Creek and the 25 Aspen trails like it — same number, same
   name, joined end to end, no conflicting attributes — is that enough
   evidence to present one trail? The roadmap says not on continuity or
   matching names alone; is an identical agency trail number the additional
   evidence, or is something more required?
2. When segments of one trail carry different uses or seasons, what does the
   trail's detail show: the most restrictive, each segment, or no summary?
3. Is a lettered or dotted child (1987.2, 0770.D) its own trail, part of its
   parent, or both?
4. For Turtle Mountain, which record is the user's trail: the 65.9 km parent
   or its six named children? May a source record be hidden from the map
   while staying preserved?
5. Should a trail with a gap (Colorado, Indian Creek) be one trail with a
   stated gap, or several? Does it matter that the gap is on land the land
   layer calls `PVT`?
6. Is a trail cut by the region boundary shown as a trail, as "part of" a
   trail, or held back until the region is widened?
7. Are snow routes and trails coincident with roads trails for Ohvernight's
   purposes?
8. What name does a user see for `787`, `NO NAME` or `LOOP`?
9. Should the `12/01-03/14` season check stay enabled in Douglas until the
   meaning of the string is confirmed with the Forest Service?
10. Must saved plans and shared links survive a change of trail identity, and
    for how long?

## What an M6 specification must settle

- The identity model: canonical segment, user-facing trail and (if any)
  route or system as separate records; which source field is the stable key
  for each; and where the grouping table lives so canonical source records
  stay untouched.
- The evidence required to group, stated as a rule that can be dry-run on
  this data: trail number, name, connectivity tolerance, attribute
  agreement, and what happens when they conflict. This audit's five Douglas
  disagreements and ten hard cases are the minimum test set.
- Treatment of overlap: parent-and-child records, shared tread between two
  named trails, and trails coincident with roads, together with the
  "several features under one tap" interaction deferred from M3.
- How uses and seasons are summarised across grouped segments without
  weakening a restriction, and the confirmed meaning of each source field
  (`managed`, `accpt`, `disc`, `restricted`, `allowed_terra_use`) before any
  of them drives a badge or filter.
- Which dropped source attributes are preserved (stable key, type, class,
  managing unit, published length, designation), following the M4-A
  source-preservation pattern.
- Clipping: whether geometry is fetched beyond the region boundary, and how a
  truncated trail is labelled.
- Jurisdiction joins: the same trail under two unit numbers (9981 and 1981),
  and matching to a second source if COTREX terms allow, with a rule for
  disagreement.
- What a user-facing name is when the source name is a number or a
  placeholder.
- Identifier migration for saved plans, GPX names and deep links.
- One freshness and transport policy for trails in both regions.
- Acceptance measurements on the real data: user-facing trail count per
  region, number of grouped trails with conflicting attributes, number of
  disconnected groups, kilometres of duplicated geometry, and count of
  search results that repeat a label.
