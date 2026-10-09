DRAFT - UNREVIEWED

# M6 trail identity — research packet

Prepared 2026-10-07. Preparation only: nothing here is decided, implemented
or ingested, and `ROADMAP.md` is unchanged. Companion file `M6-source-matrix.md` was not written.

## How statements are marked

| Mark | Meaning |
|---|---|
| **V-net** | VERIFIED BY AGENT in this task, from a saved HTTP response. The number in brackets is the response file in Appendix A, e.g. [13]. |
| **V-repo** | VERIFIED BY AGENT in this task by reading or running repository files at `aa5c20b` (`m4a-source-preservation`), read only. |
| **V-audit** | VERIFIED BY AGENT in `current-trail-audit.md` (measured from the repository; not re-measured here). |
| **H** | HERMES-SOURCED (`hermes/m6a-…`, `hermes/m6b-…`, or the watchlist). Web research, not verified by this task. |
| **I** | INFERENCE. A reading of verified facts, not itself verified. |
| **U** | UNKNOWN. |

A trail existing in any source never establishes that a use is allowed.
Every use, season and length below is a statement about what a source
publishes, not about what a person may do today.

---

## 1. Summary

1. **Live trust question, reported first (section 2).** The Douglas season
   string `12/01-03/14` is parsed correctly and in the direction the Forest
   Service defines: the field holds the dates on which the use is
   *accepted*, not the dates of a restriction (V-net [01]). The app is not
   inverting the source. But the app turns that string into a per-trip
   verdict, "Outside published use dates", for 40 of 102 Douglas trail
   features on a July motorcycle trip (V-repo), and three things found here
   say the verdict should not be trusted as it stands: the same ground
   carries two different published seasons (parent 0770 says `12/01-03/14`,
   its coincident children say `01/01-12/31`) (V-net [13]); COTREX gives the
   same trails `6/16-11/30` (V-net [21]); and the pipeline drops a fifth
   source field that sometimes carries the off-season dates (V-net [14]).
   Classification: **TRUST ISSUE**, with the truth of the source value
   **UNKNOWN**. Not fixed here.
2. **Every stored trail id is already dead at the source.** The repository's
   ids are `usfs-trail-<OBJECTID>`. Between the fetches of 2026-09-25/27 and
   2026-10-07 the service renumbered: all 40 sampled rows moved by exactly
   +604,919 and a query by the stored ids returns nothing (V-net [08]–[15]).
3. **The Forest Service publishes a trail-level key and the repository does
   not keep it.** `TRAIL_CN` is defined as the control number that
   "uniquely identif[ies] each trail across all Forest Service units"
   (V-net [01]) and is present in the service the pipeline already reads
   (V-net [02]). In all 40 sampled rows one `TRAIL_NO` has one `TRAIL_CN`
   (V-net [08]–[15]). `BMP`/`EMP` give each segment's place along the trail
   and expose real gaps.
4. **COTREX has an undocumented trail-level key, `place_id`, that behaves
   like one in five samples** (V-net [17], [19]–[23]) and it crosses
   jurisdictions: Indian Creek is 11 rows under one `place_id`, three of them
   managed by Denver Water. COTREX terms are not cleared (H); the ArcGIS item
   licence is a disclaimer that calls the data "a product and property of
   the Colorado Parks and Wildlife" and grants nothing (V-net [06]).
5. **The measured problem is unchanged from the audit:** 225 source features
   for about 165 trails; Aspen is easy (87 either way), Douglas has five
   clusters where two reasonable rules disagree, one parent record that
   duplicates its children, and trails cut by the extent or by non-Forest
   land (V-audit).

---

## 2. Possible live problem: the `12/01-03/14` season check

### 2.1 What the code does

File `v2/explore/trail-seasons.js` (V-repo):

- `:3-10` `windows(text)` splits on `;` or `,`, requires `M/D-M/D`, checks
  each date is real, and returns `[[1201, 314]]` for `12/01-03/14`
  (confirmed by running it).
- `:11` `covers` treats a range whose start is later than its end as
  wrapping the new year: `day >= 1201 || day <= 314`.
- `:19-20` a `restricted` string is checked first and wins.
- `:21` the `managed` and `accpt` strings are both treated as **use
  windows**. `disc` is not used as a window.
- `:23` if any trip day falls outside every window:
  `'Outside published use dates'`.
- `:24` otherwise `'Within published use dates — closures unchecked'`, or
  `'Published use discouraged — review'` when a `disc` string exists.

What the user is shown (V-repo):

- `v2/explore/browse.js:34` — the verdict is appended to every trail row in
  the "Find trails & camping" list when an activity is chosen.
- `v2/explore/browse.js:48` — the verdict is the first paragraph under the
  activity heading in the trail detail.
- `v2/explore/browse.js:49` — the raw string follows, e.g.
  `Dirt biking: Accepted use: 12/01-03/14`.
- `v2/explore/browse.js:50` — a standing caveat: "These source dates can be
  incomplete or surprising. Verify the current motor-vehicle map and agency
  alerts."
- `v2/explore/browse.js:30` — "Dates check published trail seasons, not live
  closures."
- Enabled only where `trail_season_check` is true:
  `v2/regions/douglas-co/explore.json:65` (true);
  `v2/regions/aspen/explore.json:121` (false).
- The behaviour is pinned by a test:
  `v2/pipeline/tests/douglas-discovery.test.cjs:4-5` expects `Outside` for
  September and `Within` for New Year on `accpt: '12/01-03/14'`.

Running the function on the committed Douglas data (V-repo, read only):

| Trip | Outside published use dates | Within published use dates | Published restriction overlaps trip | Use permission unknown |
|---|---|---|---|---|
| Motorcycling, 10–12 July | **40** | 36 | 26 | 0 |
| Motorcycling, 10–12 January | 2 | 74 | 26 | 0 |
| ATV, 10–12 July | 38 | 26 | 38 | 0 |
| Hiking, 10–12 May | 5 | 13 | 0 | 84 |

The 40 are 38 features with `motorcycling.accpt = 12/01-03/14` and 2 with
`motorcycling.managed = 12/01-03/14`. The string's 195 occurrences are
motorcycling 40, ATV managed 38, and hiking, riding and cycling
*discouraged* 39 each (V-repo).

### 2.2 What the source field means

Forest Service metadata `S_USA.TrailNFS_Publish.xml` (V-net [01]):

| Field | Definition (quoted) | Value description (quoted) |
|---|---|---|
| `MOTORCYCLE_MANAGED` | "Indicates TERRA trails that are designed and managed to accommodate motorcycle use year-round or seasonally" | "Date range for which motorcycle use is managed" |
| `MOTORCYCLE_ACCPT` | "Indicates TERRA trails where motorcycle use is allowed, but not managed or restricted seasonally or year-round." | "Date range for which motorcycle use is accepted." |
| `MOTORCYCLE_DISC` | "…where motorcycle use is discouraged, but not managed or restricted…" | "Date range for which motorcycle use is discouraged." |
| `MOTORCYCLE_ACCPT_DISC` | "…where motorcycle use is allowed or discouraged, but not managed or restricted…" | "Date range for which motorcycle use is accepted or discouraged." |
| `MOTORCYCLE_RESTRICTED` | "Indicates TERRA trails where motorcycle use is restricted year-round" | "Date range for which motorcycle use is restricted." |

Blank means "Not recorded"; `N/A` means "Not populated for this Attribute
Subset" (V-net [01]).

So a date range in `*_ACCPT` or `*_MANAGED` is the period in which the use
is **accepted or managed**. It is not a restriction period. The code's
reading matches the definition.

A second Forest Service layer says the same thing. The MVUM trails layer
(`EDW_MVUM_01/MapServer/2`) publishes, for the same trails by the same
control number (V-net [18]):

| Trail | Measure | `motorcycle` | `motorcycle_datesopen` | Symbol |
|---|---|---|---|---|
| Arrowhead 0646 | 0.00–0.79 | open | `05/16-11/30` | Trails open to vehicles 50" or less in width, Seasonal |
| Arrowhead 0646 | 0.83–1.19 | open | `12/01-03/14` | same |
| Trout Creek 0649 (both) | 0–1.84, 8.28–9.45 | open | `12/01-03/14` | same |
| Trout Creek Connection 0649.A | 0–1.87 | open | `12/01-03/14` | same |
| Turtle Mountain 0770 | 0–40.97 | open | `12/01-03/14` | Trails open to motorcycles, Seasonal |
| Turtle Mountain 0770 | 40.97–40.99 | open | `01/01-12/31` | Trails open to motorcycles, Yearlong |

That layer's description states: "Any reference to Open or Dates Open refers
strictly to when it is legal to use that motor vehicle on the trail."
(V-net [16].) In the South Platte Ranger District, 68 of 118 MVUM trail
records carry `12/01-03/14`; none carries a `06/16-…` window (V-net [24]).

### 2.3 Is the app showing something the source does not say?

Three separate answers.

**(a) Is the string misread or inverted? No.** (V-repo, V-net [01], [18].)
The two Forest Service layers both publish `12/01-03/14` as the open or
accepted period, and the code reads it that way.

**(b) Does the verdict go further than the source? Yes, by one step.** The
source says use is accepted from 1 December to 14 March and is silent about
July: `MOTORCYCLE_RESTRICTED` is blank on these rows (V-net [13], [14]).
"Outside published use dates" is a conclusion Ohvernight computes; no
source sentence says it. It is literally true and it is not the word
"closed", but it is shown as the headline answer to a dated trip.

**(c) Is the published value itself reliable? UNKNOWN, with evidence that
it may be incomplete.**

1. *The same ground has two published seasons.* Parent record 0770 (65.9 km)
   publishes motorcycle managed `12/01-03/14`; its children 0770.A–I, which
   the audit measured as covering 97% of the parent within 5 m (V-audit),
   publish motorcycle managed `01/01-12/31` (V-net [13]; repository data
   agrees, V-repo). For a July trip the app says "Outside published use
   dates" on `usfs-trail-8913499` and "Within published use dates —
   closures unchecked" on `usfs-trail-8939521`, which lies wholly along it
   (V-repo, by running the function). One tap on that ground gives either
   answer depending on which feature the tap resolves to.
2. *Adjacent segments of one trail have disjoint seasons.* Arrowhead 0646:
   measure 0–0.79 is `05/16-11/30`, measure 0.83–1.19 is `12/01-03/14`
   (V-net [14], [18]). There is no date on which the source says both
   halves are open.
3. *A third source disagrees.* COTREX gives Arrowhead Trail 646 and Turtle
   Mountain Trail 770 `motorcycle: yes` and `access: 6/16-11/30`
   (V-net [21]). Among COTREX rows managed by "USFS South Platte Ranger
   District", 94 carry `6/16-11/30` and none carries a December–March
   window (V-net [25]). The meaning of COTREX `access` is undocumented (U),
   and COTREX is compiled from agency data at an earlier date (sample rows
   are dated 2026-04-06, V-net [17]), so this is a conflict, not a
   correction.
4. *A possible explanation, not established:* the full season may be two
   ranges (for example `06/16-11/30` and `12/01-03/14`, i.e. closed only in
   spring), with the Forest Service field publishing one of them and COTREX
   the other (I). Nothing retrieved confirms this. The district's printed
   MVUM or a written answer from the South Platte Ranger District would
   settle it (U).
5. *A related loss in the pipeline.* `fetch_trails.py:23-25` keeps
   `managed`, `accpt`, `disc` and `restricted` and drops `*_ACCPT_DISC`
   (V-repo). For Indian Creek 800 the source publishes hiking managed
   `06/16-03/31` **and** `HIKER_PEDESTRIAN_ACCPT_DISC = 04/01-06/15`, with
   `ACCPT` and `DISC` blank (V-net [14]). The app shows "Outside published
   use dates" for a May hike on those four features (V-repo) while the
   source carries an "accepted or discouraged" statement for exactly those
   dates that the app never sees. The same pattern appears on Conundrum
   9981 (managed `06/15-10/15`, accepted-or-discouraged `10/16-06/14`)
   (V-net [14]). For the `12/01-03/14` motorcycle rows the dropped field
   only repeats the same range, so it does not explain those.

### 2.4 Classification

**TRUST ISSUE.** Evidence:

- Not an implementation defect: parsing, year-wrap and direction are right
  (V-repo, V-net [01]).
- The verdict is an Ohvernight computation presented as a trip answer on
  40 features, resting on one source string whose completeness is
  contradicted by the source's own overlapping records and by COTREX
  (V-net [13], [14], [21], [25]). Trust principle 7: presentation must not
  exceed the evidence.
- For foot travel on Indian Creek the verdict is produced while a published
  field covering those dates is discarded (V-net [14], V-repo).
- Whether motorcycles are in fact not accepted on these trails in July is
  **UNKNOWN**. Nothing here shows the Forest Service value is wrong, and
  nothing here shows the app tells anyone a use is allowed when the source
  says otherwise. In the positive direction the January verdict "Within
  published use dates — closures unchecked" agrees with both Forest Service
  layers.

Nothing was changed. The owner question is number 12 in section 12.

---

## 3. The problem: source segment versus user-facing trail

### 3.1 Measured counts (V-audit)

| Measure | Aspen | Douglas | Both |
|---|---|---|---|
| Source features | 123 | 102 | 225 |
| Distinct trail numbers | 87 | 78 | 165 |
| Distinct names | 87 | 77 | 164 |
| Names on more than one feature (features involved) | 26 (62) | 11 (36) | 37 (98) |
| Same-name sets that are not connected | 0 | 4 | 4 |
| Same name, different numbers | 0 | 1 | 1 |
| Names that are a number or placeholder | 0 | 15 | 15 |
| Search rows that repeat another row's label | 62 | 36 | 98 |
| Sum of feature lengths / unioned network, km | 339.1 / 339.0 | 413.9 / 352.5 | — |

Map, tap, detail, save and GPX all act on one source feature; search lists
each feature; only "nearby trails" groups, by number and name
(`v2/trail-discovery.js:27-31`, V-repo). The M3 specification records two
coincident Douglas trails as unselectable from the line and defers an
overlap chooser (`docs/specs/M3-unified-mobile-explore.md:161, 171`,
V-repo).

### 3.2 What the source adds that the repository lacks (V-net)

The pipeline keeps 42 of 105 source fields and none of the identity fields
below (V-repo `fetch_trails.py:17-32`; field list V-net [02]).

| Sample | Rows | `TRAIL_NO` | `TRAIL_CN` | `BMP`–`EMP` (miles) | Admin unit |
|---|---|---|---|---|---|
| Difficult Creek [08] | 2 | 2146 | 5695010314 | 0–2.5, 2.5–3.2656 | 021501 |
| Hunter Creek [09] | 4 | 2194 | 5688010314 | 0–0.6–2.45–2.7–4.4, contiguous | 021501 |
| Conundrum Creek [14] | 2 | 1981 | 5708010314 | 0–0.3, 0.3–10.3119 | 021501 |
| Conundrum [14] | 1 | 9981 | 175010431 | 0–2.508 | **020407** |
| Colorado [15] | 10 | 1776 | 6885010465 | 3.18–16.44 with gaps at 6.25–6.90 and 16.09–16.14 | 021211 |
| Indian Creek [14] | 4 | 800 | 7982010465 | 0–5.55, 6.84–7.29, 8.48–8.81, 9.19–14.10 | 021211 |
| Trout Creek [14] | 2 | 0649 | 6725010465 | 0–1.84, 8.28–9.45 | 021211 |
| Trout Creek Connection [14] | 1 | 0649.A | 1062860010602 | 0–1.87 | 021211 |
| Arrowhead [14] | 2 | 0646 | 6724010465 | 0–0.79, 0.83–1.19 | 021211 |
| Turtle Mountain [13] | 2 | 0770 | 181861010602 | 0–40.97, 40.97–40.9889 | 021211 |
| Tunnel [13] | 2 | 0770.A | 1993181010602 | 0–0.17, 0.17–6.68 | 021211 |
| 0770.B to 0770.I [13] | 1 each | 0770.B…I | eight distinct values | each from 0 | 021211 |

Readings:

- In these 40 rows `TRAIL_CN` and `TRAIL_NO` give the same partition
  (V-net). Whether that holds for all 225 features is U; it needs the
  attribute to be fetched.
- The source's own measures record the gaps. Colorado, Indian Creek, Trout
  Creek and Arrowhead are each one `TRAIL_CN` whose measure runs on across a
  missing interval (V-net). The source treats each as one trail with
  unpublished stretches (I). The audit found those gaps lie on land the land
  layer calls `PVT` for Colorado and Indian Creek (V-audit).
- Every lettered child of 0770 has its own `TRAIL_CN`. The source calls the
  children separate trails and the parent a separate trail (V-net [13]).
- Conundrum (9981) sits in a different administrative unit from Conundrum
  Creek (1981), with a different `TRAIL_CN` (V-net [14]). The audit's
  reading that this is one trail numbered by two units is consistent with
  that and still I: no source key joins them.
- Splits are measure breaks. The Difficult Creek split at mile 2.5 shows no
  difference in any of the 33 fields sampled (V-net [08]); the reason for
  the split is U.

### 3.3 Hard cases, by id (ids are the repository's, V-audit; source facts V-net)

**Douglas clusters where number and name-plus-connectivity disagree**

| Cluster | Repository ids | By number | By name + connectivity | Source evidence now available |
|---|---|---|---|---|
| Colorado, 1776 | `usfs-trail-8924501`, `-8925547`, `-8955417`, `-8955535`, `-8963975`, `-8971239`, `-8971341`, `-8972880`, `-8973227`, `-8973512` | 1 trail, 18.2 km | 3 trails | One `TRAIL_CN`; measure gaps of 0.65 mi and 0.05 mi; begins at mile 3.18, so the start lies outside what was fetched [15] |
| Indian Creek, 800 | `-8977816`, `-8970783`, `-8968633`, `-8982425` | 1 trail, 18.1 km | 3 trails | One `TRAIL_CN`; three measure gaps (1.29, 1.19, 0.38 mi) [14]. COTREX has 11 rows under one `place_id`, 3 managed by Denver Water [20] |
| Turtle Mountain, 0770 and 0770.E | `-8913499`, `-8953147`, `-8939521` | 2 trails | 1 trail, 91.3 km of line | Two `TRAIL_CN` values; parent and child publish different motorcycle seasons [13] |
| Trout Creek, 0649 | `-8972161`, `-8973336` | 1 trail | 2 trails | One `TRAIL_CN`; measure gap of 6.44 mi (1.84 to 8.28) [14] |
| Arrowhead, 0646 | `-8964639`, `-8970427` | 1 trail | 2 trails | One `TRAIL_CN`; measure gap 0.04 mi; disjoint published seasons [14], [18] |

**Parent record 0770 overlapping its children.** `usfs-trail-8913499`
(65.9 km, three parts, 6.5 km internal gap) lies 97% within 5 m of children
0770.A–F (V-audit). At source it is one row, measure 0–40.97 mi, trail
class 4, MVUM symbol 10 (seasonal); the children are class 3, symbol 9
(yearlong), each with its own `TRAIL_CN` (V-net [13]). The 30 m fragment
`usfs-trail-8953147` is the parent's second row, 40.97–40.9889 mi,
yearlong. COTREX carries "Turtle Mountain Trail" 770 as three rows under
`place_id` 7516 totalling 41.0 mi (V-net [21]); how COTREX holds the
children was not sampled (U).

**Trails cut by the extent.** 26 Aspen features of 25 trail numbers end on
the project rectangle; eight have internal gaps of 22–2,063 m: Cooper Basin
`-8932839`, Lost Man Loop `-8920907`, South Fork Lake Creek `-8955533`,
McNassar Gulch `-8961619`, Nickelson Creek `-8923933`, Geneva Lake
`-8921344`, Trail Riders `-8964672`, Conundrum Creek `-8922773` (V-audit).
With `BMP`/`EMP` kept, the published length of the whole trail is available
without fetching geometry outside the extent, and a clipped trail can be
recognised because its segments do not cover 0 to the trail's last `EMP`
(I, from V-net).

**Jurisdiction boundaries.**

- Forest to forest: Conundrum 9981 (unit 020407) against Conundrum Creek
  1981 (unit 021501); Copper Creek 9983 against East Maroon 1983 (V-audit
  for the pattern; V-net [14] for the unit codes of the first pair).
- Forest to non-Forest: Indian Creek's measure gaps coincide with COTREX
  rows managed by Denver Water (V-net [14], [20]); the Forest Service layer
  holds National Forest System trails only.
- County line: two Colorado Trail features touch the Douglas line
  (V-audit); the trail's measure starts at 3.18 in the county (V-net [15]).
- Trail numbers are not unique across units: COTREX `trail_num` 2146 is
  Difficult Creek Trail (Aspen-Sopris) and Lee's Windmill Road (Comanche);
  2194 is Hunter Creek Trail and North Arroyo Road (V-net [17], [19]).

**Other cases from the audit** (V-audit): Tunnel `-8937765` / `-8941308`
(one number, different vehicles); Graham Gulch `-8952771` and McNassar
Gulch `-8961619` (129 m shared tread, two names); the 1987 and 1992
families of named spurs in Aspen; Hunter Creek (2194) against Hunter Valley
(1992); snow routes `-8915341` and `-8932149` lying on roads.

---

## 4. How competitors model it (HERMES-SOURCED)

Everything in this section is **H**, from `hermes/m6b-…`. Trailforks and
Komoot could not be read and are U.

| Product | User-facing unit | Underlying unit | Overlap | Notes |
|---|---|---|---|---|
| AllTrails | Curated "verified route" | OSM segments, shown separately and unverified | U | Length from averaged member GPS traces |
| Gaia GPS | "Hike", which may use several trails | "Trail" (mapped path); routing snaps to OSM | U | Difficulty method not documented |
| Hiking Project | "Trail" (one trail as on a printed map) and "recommended route" | Contributor GPS tracks, reviewed | Routes may reuse trails | Difficulty is the average of community votes |
| onX Backcountry / Offroad | Trail or guided trail | U | U | Offroad shows open/closed and seasons as product fields |
| FarOut | Guide for one trail, with sections and alternates | Primary track | U | Hand-built guides |
| CalTopo | User-drawn line | none | U | Profile computed along the line |
| COTREX app | Official trails, featured routes, custom routes | Agency GIS | U | Allowed-uses view and manager-posted closures |
| OpenStreetMap | `route=hiking` relation with name and ref | Ways | Documented: several routes may share ways | No standard length, gain or difficulty method |

Patterns reported by Hermes (H): (1) a physical network kept apart from
named routes that reference it; (2) named overlays that may share ground;
(3) curated guides. None of the retrieved documentation defines "one trail"
in a way that can be copied as a rule. The cheap part to copy is the
separation of segment, named trail and user route; the expensive parts are
editorial curation, GPS-trace aggregation and closure feeds.

Checked here against data (V-net [22]): COTREX layer 15 does implement
pattern 2. A row has up to four `place_id`/`name` slots, and sampled Aspen
rows carry a summer trail in the first slot and a winter route in the
second (for example "Smugglers Cutoff Trail" with "Hunter Creek to Benedict
Huts Trail", `seasonal_1: winter`). What the slots mean is undocumented (U).

---

## 5. Candidate identity models

Common to all: canonical source segments stay as published; grouping is a
separate table or property; no geometry is invented; a group is an identity,
not a statement that the trail may be used.

### Model A — group by source trail number, or by `TRAIL_CN`

One user-facing trail per Forest Service trail record.

- A1: key is `trail_number` as stored today.
- A2: key is `TRAIL_CN`, with `TRAIL_NO` kept for display.

| Dry run | Aspen | Douglas | Both | Basis |
|---|---|---|---|---|
| A1, by `TRAIL_NO` | 87 | 78 | 165 | V-audit |
| A2, by `TRAIL_CN` | U | U | U | Same partition as A1 in all 40 sampled rows (V-net); full count needs the field fetched |
| By base number (text before the dot) | 59 | 48 | 107 | V-audit; merges trails that carry their own names |

What breaks:

- 0770 and 0770.E become two trails named Turtle Mountain, one lying on the
  other (V-audit).
- Trout Creek becomes one trail with a 6.44-mile hole (V-net [14]);
  Colorado and Indian Creek likewise with smaller holes.
- Arrowhead becomes one trail with two disjoint seasons (V-net [14]).
- A1 only: `TRAIL_NO` is not unique across units (V-net [17], [19]) and is
  not consistently zero-padded (`0681`, `681.D`; V-audit). A1 needs the
  administrative unit in the key. A2 does not.
- Conundrum 9981 and Conundrum Creek 1981 stay separate (may be right;
  owner question).
- Permanence of `TRAIL_CN` is not promised by the metadata (H; nothing
  retrieved here says otherwise) — U.

### Model B — group by name plus connectivity

Same name, joined through end points within a tolerance.

| Dry run | Aspen | Douglas | Both | Basis |
|---|---|---|---|---|
| B, 10 m | 87 | 83 | 170 | V-audit |
| B, six decimals | 87 | 84 | 171 | V-audit |
| Name only | 87 | 77 | 164 | V-audit |

What breaks:

- It is the rule the roadmap forbids as sufficient evidence: "Trail
  features are not merged or renamed on geometric continuity or matching
  names alone" (`ROADMAP.md`, M6; V-repo).
- Turtle Mountain becomes one trail of 91.3 km of line, two-thirds of it
  drawn twice (V-audit).
- Colorado, Indian Creek, Trout Creek and Arrowhead split into 3, 3, 2 and
  2 trails although the source gives each one control number and one
  continuous measure (V-net [14], [15]).
- Sensitive to tolerance (Indian Creek: 4 components at six decimals, 3 at
  10 m; V-audit) and to names: 15 Douglas names are numbers or
  placeholders, two features are both named `787` (V-audit).
- Group identity has no source key, so a stable id must be built from
  something else.

### Model C — adopt COTREX's trail-level key (`place_id`)

Finding first: **layer 15 has no field named `trail_id`, no relationships
and no domains** (V-net [05]). The only candidate trail-level key is
`place_id` (with `place_id_1`–`_3`), which is undocumented.

Sample behaviour (V-net):

| Sample | COTREX rows | `place_id` | COTREX `trail_num` | Forest Service rows | Agreement |
|---|---|---|---|---|---|
| Difficult Creek Trail [17], [23] | 5 (lengths 0, 0.2, 0, 3.9, 0 mi) | 16137 on all 5, and on no other row | 2146 | 2 (3.27 mi) | Number agrees. Segmentation differs. COTREX `horse: no`; Forest Service `ALLOWED_TERRA_USE` is `21`, which includes pack and saddle |
| Hunter Creek Trail [19] | 1 (4.4 mi) | 15409 | 2194 | 4 (to mile 4.4) | Number and total length agree |
| Indian Creek Trail [20] | 11 | 6424 on all | 800 | 4 | Number agrees; COTREX includes 3 Denver Water rows |
| Turtle Mountain Trail [21] | 3 (41.0 mi) | 7516 on all | 770 | 2 for 0770 (40.99 mi) | Leading zero dropped; length agrees with the parent |
| Arrowhead Trail [21] | 1 (0.4 mi) | 20930 | 646 | 2 (0.79 + 0.36 mi) | Partial; the other part was not found under that name and number (U) |

Dry-run count for the two regions: **none**. No COTREX data has been
ingested and none may be until terms are cleared; a count would need a
regional extract.

What breaks:

- Terms. See the matrix. Without written permission this model cannot be
  built on, only used as a private cross-check, and even that should be
  asked (question in the matrix).
- No documented meaning, uniqueness or persistence for `place_id`,
  `feature_id` or `GlobalID` (V-net [05]; H).
- No shared key with the Forest Service: COTREX has no `TRAIL_CN`;
  `trail_num` matches `TRAIL_NO` only after normalising zeros and is not
  unique statewide (V-net [17], [19], [21]).
- COTREX and the Forest Service disagree on attributes for the same trail
  (horse use on Difficult Creek; season on Arrowhead and Turtle Mountain).
  Adopting COTREX identity invites adopting its attributes; a rule for
  disagreement would be needed.
- Its strength is exactly the cases A cannot solve: one identity across
  jurisdictions (Indian Creek) and several named routes on one segment.

### Model D — a base rule plus a reviewed override list

Take A2 (or A1) as the base and keep a small reviewed file of exceptions,
in the manner of M4's reviewed lists (M4 specification section 8.5, V-repo):
each entry has the ids, the action, a reason code, a source or measurement,
a reviewer and a date.

Possible actions: `split` (one key shown as several trails), `join`
(several keys shown as one), `suppress_display` (a preserved record not
drawn, e.g. a parent laid over its children), `rename_display`.

| Dry run | Aspen | Douglas | Basis |
|---|---|---|---|
| Base A1 | 87 | 78 | V-audit |
| Entries the audit's evidence would put up for review | 1 pair (Conundrum / Conundrum Creek), plus Copper Creek / East Maroon | 5 clusters (21 features) plus the 0770 parent | V-audit |
| Resulting count | depends on owner answers | depends on owner answers | — |

What breaks:

- Every entry is a human judgement that must be re-reviewed when the source
  changes; an entry keyed on `OBJECTID` would already be dead (V-net).
  Entries must be keyed on `TRAIL_CN` and measures, or on a stable segment
  id.
- Grows with each new region; needs a rule for when the list is too long to
  be honest.
- A `join` across control numbers on the strength of a name is the thing
  the roadmap warns against; it needs stated evidence per entry.

### Comparison

| | A2 `TRAIL_CN` | B name + connectivity | C COTREX `place_id` | D A2 + overrides |
|---|---|---|---|---|
| Source-stated identity | Yes (V-net [01]) | No | Undocumented (U) | Yes, plus recorded judgement |
| Count, Aspen / Douglas | 87 / 78 expected, U until fetched | 87 / 83 | U | set by review |
| Handles the 0770 parent | No | Worse | U | Yes, by entry |
| Handles measure gaps | One trail with a stated gap | Splits | Fills some gaps with other managers' rows | Either, by entry |
| Crosses jurisdictions | No | By name only | Yes in one sample | By entry |
| Licence | Federal layer; disclaimer only (V-net [01]) | — | Not cleared (H; V-net [06]) | as base |
| Needs a refetch | Yes, attributes | No | Yes, and permission | Yes |

### Proposed invariants, in the style of M4's G1–G10

For a specification to accept, amend or reject. Written for Model A2 / D.

- **TG1.** Every member of a trail group has the same `TRAIL_CN`, and it
  equals the one in the group ID.
- **TG2.** Different `TRAIL_CN` values are never merged by name, geometry
  or proximity. A join across control numbers exists only as a reviewed
  override entry naming its evidence.
- **TG3.** Every member of a group has the same `TRAIL_NO` and the same
  administrative-unit scope. If two segments share a `TRAIL_CN` and differ
  in `TRAIL_NO`, the build stops and reports them.
- **TG4.** If members of a group differ in `TRAIL_NAME`, the build stops and
  reports them; it does not pick one. (M4 G2 precedent.)
- **TG5.** No segment belongs to two groups. A segment with an empty
  `TRAIL_CN` belongs to none and is shown as itself.
- **TG6.** Members are ordered by `BMP`. Measure ranges of members do not
  overlap. Where they are not contiguous the group records each gap
  (from, to, length); a group is never presented as continuous across a
  recorded gap.
- **TG7.** Every coordinate in a group's display geometry comes from a
  member's canonical geometry. No connector is drawn across a gap, an
  extent cut or a jurisdiction boundary. (M4 G9 precedent.)
- **TG8.** Grouping never changes, removes or reorders canonical data
  except by writing the group reference. (M4 G8.)
- **TG9.** A group never states a use, season, surface or restriction that
  is not stated on every member. Where members differ, the group shows the
  difference per member (or says "varies"); a restriction on any member is
  never dropped, weakened or averaged away.
- **TG10.** A group's length is labelled by what it is: the sum of members'
  source-stated lengths, or the source's last `EMP`, or the length of drawn
  geometry. The three are never substituted for one another, and a group
  with an extent cut or recorded gap is marked partial.
- **TG11.** A record suppressed from display by a reviewed entry stays in
  canonical data, stays reachable through search or the group's detail, and
  its restrictions remain visible on the ground it covers.
- **TG12.** The set of members of a group equals the set of canonical
  segments whose group reference is that group ID. (M4 G7.)

### Stable-id scheme (options, not a choice)

Facts that bound the choice:

- `OBJECTID` is not stable: +604,919 on every sampled row within twelve
  days (V-net [08]–[15]). The constant offset must not be relied on.
- `GLOBALID` has a unique index in the service (V-net [02]). The repository
  never stored it, so its persistence across the same rebuild could not be
  checked (U).
- `TRAIL_CN` is the documented trail key; `BMP`/`EMP` locate a segment but
  change if the Forest Service re-segments (I).
- The MVUM trails layer carries the same control number as `rte_cn`
  (V-net [18]), so the trail key also joins the two Forest Service layers.

| Record | Option 1 | Option 2 |
|---|---|---|
| Segment | `usfs-tseg-<GLOBALID, sanitised>` — only if persistence is shown across at least two fetches | `usfs-tseg-<TRAIL_CN>-<BMP in ten-thousandths of a mile>` — semantic, survives a rebuild, breaks on re-segmentation |
| Trail group | `usfs-trail-cn-<TRAIL_CN>` | same, with `-p<n>` for further parts if the owner wants a gapped trail shown as parts (M4 7.2 precedent) |
| Source record | `source_namespace` + `source_id`, kept unmodified beside the Ohvernight id (M4 7.1 precedent) | same |

Collision: today's ids are `usfs-trail-<digits>`. A group namespace of
`usfs-trail-cn-` cannot collide with them, and a validator rule can check
it, as M4 does.

Legacy mapping: M4 matched old and new records by exact canonical geometry
within a layer and refused a row-number match (M4 7.3, V-repo). The same
rule applies here with more force, because the row numbers have verifiably
moved. Saved plans hold the old ids in browser storage (V-audit), so an
alias map from old id to new display id is needed if saved plans are to
survive.

---

## 6. Overlapping trails

What exists (V-audit unless marked):

| Kind | Cases | Size |
|---|---|---|
| Parent record over its children | 0770 over 0770.A–F | 64.1 km of the parent within 5 m |
| Two named trails sharing tread | Graham Gulch / McNassar Gulch (Aspen); Powerline / Beginner (Douglas) | 129 m; 72–79 m |
| Trail coincident with a mapped road | Bald Knob, Schofield Pass Ski (Aspen, whole length); Indian Creek 397 m, Beginner 189 m (Douglas) | — |
| Several named routes on one segment (COTREX only) | Aspen rows with a second `place_id`, mostly winter routes | V-net [22]; not counted |

Questions a specification has to answer, with what the sources allow:

1. *Which record is drawn?* The source does not rank a parent above its
   children; both are published trails with different class, symbol and
   season (V-net [13]). Hiding either is an Ohvernight decision.
2. *What does a tap select?* M3 resolves a tap to one feature and defers the
   chooser. With overlap, the answer shown for uses and seasons depends on
   which feature wins (section 2.3). A chooser listing every trail under
   the tap is the only option that hides nothing (I).
3. *How is length counted?* Region totals double-count 61 km in Douglas
   (V-audit). Per-trail lengths are unaffected; any "kilometres of trail"
   figure must use the unioned network or say it is a sum of records.
4. *Do the overlapping records agree?* Not always: 0770 parent and children
   differ on motorcycle season. A rule that the stricter published season
   is shown wherever records overlap would follow trust principle 5; it is
   a product decision.

---

## 7. Names

| Fact | Basis |
|---|---|
| Forest Service `TRAIL_NAME` is "the name that the trail or trail segment is officially or legally known by", upper case | V-net [01] |
| Aspen: 87 names for 87 numbers, one to one | V-audit |
| Douglas: 15 names are a number or placeholder (`787` ×2, `788`, `662`, `787.A`, `673.A`, `681.B`, `681.C`, `681.E`, `682.AA`, `915 TRAIL`–`918 TRAIL`, `NO NAME`); one is `LOOP` | V-audit |
| The same name on two control numbers: Turtle Mountain (0770, 0770.E) | V-audit, V-net [13] |
| COTREX names are title case with "Trail" appended: "Difficult Creek Trail", "Indian Creek Trail", "Turtle Mountain Trail" | V-net [17], [20], [21] |
| COTREX holds up to four names per segment | V-net [05], [22] |
| Trail and road layers spell one place differently: Peekaboo / Peakaboo | V-audit |
| Competitors keep name, reference and alternate names as separate values (OSM `name`, `ref`) | H |

What can be done without invention: show the source name as published, with
its number; change case for display only; show "Trail 787" where the name
is the number. What would be invention: appending "Trail", expanding
`COLORADO` to "Colorado Trail", choosing between two source names, or
naming `NO NAME`. A reviewed display-name entry with a cited source is the
only route to those (I). Using a COTREX name depends on the terms.

---

## 8. Lengths and elevation gain

### Length

| Quantity | Source | Honest label | Limits |
|---|---|---|---|
| Segment length, source-stated | `SEGMENT_LENGTH` = `EMP` − `BMP`, miles | "Forest Service measure" | Kept by nobody today (V-repo). "Can be measured in a variety of ways" (V-net [01]) |
| Segment length, source GIS | `GIS_MILES` | "Forest Service GIS length" | Differs slightly: Difficult Creek 2.5 against 2.546 (V-net [08]) |
| Whole-trail length, source-stated | last `EMP` of the `TRAIL_CN` | "Published trail length" | Includes parts outside the region and across gaps; needs every row of the trail, attributes only |
| Drawn length | computed from clipped geometry | "Length shown on this map" | Not the trail's length where the extent cuts it (25 Aspen trail numbers; V-audit) |
| COTREX `length_mi_` | per row, rounded to 0.1, zero on short rows | — | Not cleared; rounding makes sums unreliable (V-net [17]) |
| COTREX `Shape__Length` | service-computed | — | The layer is in Web Mercator (wkid 102100, V-net [05]), so this is not ground metres; at 39° N it overstates by roughly a quarter (I). Hermes's "in meters" needs that caveat |

Checks: Difficult Creek's published 3.2656 mi is 5.26 km; the repository's
two clipped features sum to 5.26 km (V-audit, V-net [08]). Turtle Mountain
0770's 40.97 mi is 65.9 km against the audit's 65,935 m (V-audit,
V-net [13]). So where a trail is whole, source measure and geometry agree
in these two samples.

A group length is honest when it says which of these it is and whether the
group is partial (TG10). Out-and-back or loop distance is not in any source
and would be invention.

### Elevation gain

No elevation exists in the repository's trail data or in the Forest Service
layer: geometry is two-dimensional and there is no elevation field
(V-net [02]). `TYPICAL_TRAIL_GRADE` exists as a category and is not kept
(V-net [02], V-repo). COTREX has `min_elevat` and `max_elevat` per row, unit
undocumented; sampled values are consistent with metres (I, V-net [17]).
A minimum and maximum give a range, not a gain.

Gain therefore needs a DEM. Options, none retrieved or checked in this task
(all **U** as to current terms, format and coverage; listed so the
specification can ask):

| Option | What it would give | To be established |
|---|---|---|
| USGS 3DEP 1/3 arc-second (about 10 m) seamless DEM | Uniform coverage of both regions; federal | Access method for a static build, vertical accuracy statement, licence wording |
| USGS 3DEP 1 m lidar DEM | Better fit to narrow trails | Whether both regions are covered; file size |
| COTREX `min_elevat` / `max_elevat` | A range per row with no DEM work | Terms; unit; method |
| A third-party elevation API | Convenience | Licence, rate limits, reproducibility; conflicts with a static, reproducible build |

Whatever the source, the method is a set of choices that change the answer:
sampling interval along the line, smoothing or a minimum-climb threshold,
and direction (gain differs from one end to the other). Without them stated
next to the number, a gain figure looks like a measurement and is a model
output (trust principle 7). Gain across a gap, across a clipped trail or
along a parent that duplicates its children is not meaningful. M4 found a
unit error in a source elevation field (amendment A3, V-repo); the same
check applies.

---

## 9. Surface, uses, seasons, closures, direction, difficulty

"States" means the field exists and has a published definition. Nothing in
this table is a permission.

| Topic | What the Forest Service layer states | What COTREX layer 15 holds | What would be invention |
|---|---|---|---|
| Surface | `TRAIL_SURFACE`, the predominant expected surface; repository values: native material, imported compacted, imported loose, snow (V-net [01], V-audit). Varies between segments of one trail (Colorado; V-net [15]) | `surface`: `dirt`, `track`, `road` in samples; no domain (V-net [05], [17], [21]) | One surface for a grouped trail whose members differ; "rocky", "smooth" |
| Permitted uses | Five fields per use: managed, accepted, discouraged, accepted-or-discouraged, restricted, each a date range (V-net [01]). `ALLOWED_TERRA_USE`: "uses on TERRA Trails that are legally allowed", digits 1 hiker/pedestrian, 2 pack and saddle, 3 bicycle, 4 motorcycle, 5 ATV, 6 4WD over 50" (V-net [01]) — this confirms the audit's inferred decoding. It carries no dates: Arrowhead is `54321` on both segments while their seasons are disjoint (V-net [14]) | `hiking`, `horse`, `bike`, `motorcycle`, `atv`, `ohv_gt_50`, `highway_ve`, `dogs`: `yes`, `no`, `leashed`, `seasonally`, or a date range; undocumented (V-net [05], [17], [22]) | Reading blank as allowed or as prohibited; reading "discouraged" as closed; showing `ALLOWED_TERRA_USE` as a year-round permission; dogs from any Forest Service field (there is none) |
| Seasonal restriction | `*_RESTRICTED` date range; MVUM `*_datesopen` for motor vehicles, "strictly … when it is legal to use that motor vehicle on the trail" (V-net [16], [18]). Publication level varies by forest; both pilot units publish `TrailNFS_MGMT` (V-audit) | `access` (`6/16-11/30`, `seasonally`), `seasonalit`…`seasonal_3` (`winter`); undocumented (V-net [22], [25]) | A closed season computed as the complement of an accepted season (section 2); merging two sources' seasons |
| Closures and orders | None. The layers have no closure, order or alert field (V-net [02], [16]). Forest orders and alerts are web pages and PDFs (H) | None in layer 15 (V-net [05]). The app shows manager-posted closures; no public feed was found (H) | "Open", "no closures", or any current status from these layers |
| Direction | None. No direction field (V-net [02]). `BMP`→`EMP` is the direction of measurement, not of travel (I) | `oneway`, blank on every sampled row (V-net [17]–[22]) | Uphill/downhill-only, one-way, "best ridden clockwise" |
| Difficulty | None. `TRAIL_CLASS` is "development scale" 1–5, not difficulty (V-net [01]); `TYPICAL_TRAIL_GRADE` and tread width exist and are not kept (V-net [02]) | None in layer 15 (V-net [05]). CPW's own state-park trail inventory mentions a difficulty attribute (V-net [07], item description; not examined) | Any rating derived from grade, length, class or surface; competitors use community votes or undisclosed methods (H) |
| Managing unit | `ADMIN_ORG`, `MANAGING_ORG`: region, forest, district codes (V-net [01]) | `manager` free text, e.g. "USFS South Platte Ranger District", "Denver Water" (V-net [20]) | — |
| National designation | `NATIONAL_TRAIL_DESIGNATION`; the Colorado Trail rows in Douglas are `1`, "Not designated as a National Trail" (V-net [01], [15]) | — | Calling a trail a national trail from its name |

Source disagreements already seen, same trail (V-net):

| Trail | Forest Service | COTREX |
|---|---|---|
| Difficult Creek | `ALLOWED_TERRA_USE` `21` (includes pack and saddle); repository holds horseback managed `01/01-12/31` (V-repo) | `horse: no` |
| Arrowhead 0646 | motorcycle accepted `05/16-11/30` on one segment, `12/01-03/14` on the other | `access: 6/16-11/30`, `motorcycle: yes` |
| Turtle Mountain 0770 | motorcycle managed `12/01-03/14`, ATV restricted all year | `access: 6/16-11/30`, `motorcycle: yes`, `atv: no` |
| Indian Creek 800 | hiking managed `06/16-03/31`; accepted-or-discouraged `04/01-06/15` | `access: 6/16-11/30` on 5 of 11 rows, blank on 6 |

---

## 10. Owner decisions

Each has a one-line recommendation for discussion. None is decided.

| # | Decision | Recommendation |
|---|---|---|
| 1 | Is an identical Forest Service control number (`TRAIL_CN`), with matching number and name, enough evidence to present several segments as one trail? | Yes: it is the agency's own trail key, which is the "additional evidence" the roadmap asks for beyond name and continuity. |
| 2 | Base identity model: A2, B, C or D? | D on an A2 base: `TRAIL_CN` by rule, a short reviewed list for the exceptions. |
| 3 | Is a lettered or dotted child (1987.2, 0770.D) its own trail? | Yes, its own trail, because the source gives it its own control number and name; a "family" is a later, separate concept. |
| 4 | Turtle Mountain: which record is the user's trail, the 65.9 km parent or its children, and may a preserved record be hidden from the map? | Show the children; keep the parent preserved and reachable, and keep its season visible on that ground until the conflict is resolved. |
| 5 | A trail with measure gaps (Colorado, Indian Creek, Trout Creek, Arrowhead): one trail with stated gaps, or several? | One trail, drawn in parts, with each gap stated and nothing drawn across it. |
| 6 | A trail cut by the region boundary: shown how? | Shown as a trail marked "continues beyond this map", with the published whole-trail length beside the drawn length. |
| 7 | When members of one trail differ in use or season, what does the trail's detail show? | Each differing stretch separately; never a single merged summary; any restriction shown first. |
| 8 | What does one tap on overlapping trails do? | List every trail under the tap (the chooser deferred from M3) rather than pick one. |
| 9 | What name is shown for `787`, `NO NAME`, `LOOP`, and may names be re-cased or given "Trail"? | Show "Trail <number>" where the name is a number or placeholder; re-case only; add nothing else without a reviewed entry. |
| 10 | Which source fields are added to the canonical trail record? | At least `TRAIL_CN`, `GLOBALID`, `BMP`, `EMP`, `SEGMENT_LENGTH`, `GIS_MILES`, `ADMIN_ORG`, `MANAGING_ORG`, `TRAIL_TYPE`, `TRAIL_CLASS`, `NATIONAL_TRAIL_DESIGNATION`, `MVUM_SYMBOL` and the five `*_ACCPT_DISC` fields. |
| 11 | Identifier migration: must saved plans and links survive, and by what match? | Yes; match old to new by exact geometry as in M4, never by row number, and publish an alias map. |
| 12 | The Douglas season check (section 2): leave as is, reword, or switch off until the `12/01-03/14` value is confirmed in writing by the South Platte Ranger District? | Owner call, and it need not wait for M6; the evidence favours not showing a computed "outside use dates" verdict on these 40 features until the district answers. |
| 13 | Should "discouraged" continue to produce "Use permission unknown" for foot, stock and bicycle (84 of 102 Douglas features)? | Show the published word "discouraged" with its dates instead of "unknown"; it is a source statement, not an absence. |
| 14 | COTREX: ask CPW for written terms now, and may it be used for private comparison meanwhile? | Ask now with the questions in the matrix; ingest and publish nothing, and treat even private comparison as needing an answer. |
| 15 | Length: which figure is shown, and under what label? | Published Forest Service measure as the trail length, drawn length labelled as such when the trail is partial. |
| 16 | Elevation gain in M6 at all? | Not until a DEM source, its terms and a stated method are approved; show nothing rather than an unlabelled estimate. |
| 17 | Difficulty and direction? | Neither; no source states them. |
| 18 | Are snow routes and trails lying on roads "trails" for Ohvernight? | Keep them, typed as the source types them (`TRAIL_TYPE` SNOW), and do not style them as summer trails. |
| 19 | Cross-unit joins (Conundrum 9981 / Conundrum Creek 1981): join, link, or leave? | Leave separate and add a reviewed "continues as" link only with a cited agency source. |
| 20 | One freshness and transport policy for trails in both regions (Aspen `null`, Douglas 168 h today)? | One policy, with a recorded transport result per fetch, given the service was rebuilt within twelve days. |

---

## 11. Tests an M6 specification will need

**Source preservation and identity**

- Every canonical trail segment has a non-empty `TRAIL_CN` and source
  segment key; the build stops, with a report, if one is missing; no
  row-number fallback.
- Stability proof: two fetches on different days give the same segment ids
  and group ids for unchanged geometry. (The 2026-09-25 to 2026-10-07
  renumbering is the regression this guards.)
- Legacy mapping: every pre-M6 `usfs-trail-<OBJECTID>` id maps by exact
  geometry to a current id or is listed as unmatched; a moved row number
  does not match; an identical geometry does.
- No group id collides with a segment id or a legacy id.

**Grouping invariants (negative fixtures for each of TG1–TG12)**

- Two control numbers with the same name stay two trails (0770 / 0770.E).
- One control number with a measure gap is one trail in parts, with the gap
  recorded and no coordinate that is not in a member (Trout Creek 0649).
- A member with a different name or number under the same control number
  stops the build.
- A segment in two groups, or a group referenced by no segment, fails.
- Mutation proofs on real data: move one segment to another group; drop a
  member from a display geometry; add a connector across a gap; change one
  `TRAIL_CN`.

**The real-data acceptance set** (the audit's five clusters and ten cases)

- Expected trail counts per region under the approved rule, asserted as
  numbers.
- Difficult Creek: two segments, one trail, one search row, one label, one
  GPX file containing both segments.
- Hunter Creek: four segments, one trail; Hunter Valley remains a different
  trail.
- Turtle Mountain, Colorado, Indian Creek, Trout Creek, Arrowhead: each
  behaves as the owner decides, asserted by id.
- Count of search rows that repeat a label (98 today) falls to the number
  the rule predicts.
- Kilometres of duplicated geometry drawn (61 km in Douglas today) equals
  the approved figure.

**Uses and seasons**

- A group whose members differ in any use or season field never renders one
  merged value (Arrowhead, Tunnel, Turtle Mountain; East Snowmass Ditch,
  McNassar Gulch, Peekaboo Gulch).
- A restriction on any member is rendered; staleness or grouping never
  removes it.
- Blank renders as unknown, never as allowed or as prohibited; `N/A` renders
  as not published.
- `ALLOWED_TERRA_USE` is never rendered without its key and never as a
  dated or current permission.
- The season function, whatever is decided under decision 12: a fixture for
  `12/01-03/14` in July and in January; a fixture where `ACCPT_DISC` covers
  the trip dates (Indian Creek, May); a fixture for the 0770 parent and a
  child on the same ground.
- No string renders "open", "allowed", "legal" or "closed" from any trail
  layer field.

**Overlap and interaction (browser, both regions, four sizes)**

- A tap on a line of a grouped trail selects the whole trail from any
  member and from its label; one label per trail.
- A tap where two trails coincide reaches both (`usfs-trail-8925194` and
  `usfs-trail-8952194` are the M3 cases).
- A trail cut by the extent shows its partial marker; a gapped trail shows
  no line across the gap.

**Lengths**

- Group length equals the stated computation from members; the label names
  the kind of length; a partial group shows both figures or the marker.
- If elevation is approved: a fixed DEM tile and line give a fixed gain; the
  method string is rendered; reversing the line changes gain as expected;
  no gain is rendered for a partial or gapped trail.

**Licence gate**

- The build fails if any COTREX-derived value is present in a published
  artifact while no written permission is recorded in the repository.
- Every trail source has a transport record and one freshness policy.

---

## 12. Risks

| Risk | Evidence | What limits it |
|---|---|---|
| The Douglas season verdict misleads riders today | Section 2 | Owner decision 12; a written answer from the district |
| Identity built on a key that changes | `OBJECTID` moved by 604,919 in twelve days (V-net) | Keep `TRAIL_CN` and `GLOBALID`; prove stability over two fetches before relying on either |
| `TRAIL_CN` is not permanent either | No promise in the metadata (H) | Legacy alias map; geometry-based matching; a report of control numbers that appear or vanish between fetches |
| Grouping hides a difference in use or season | 3 of 26 Aspen and 4 of 11 Douglas multi-feature trails differ (V-audit) | TG9 and its tests |
| Hiding the 0770 parent hides its stricter season | Parent `12/01-03/14`, children all year (V-net [13]) | TG11; decision 4 |
| COTREX used without permission | Item licence grants nothing (V-net [06]); app terms prohibit reuse (H) | Licence gate test; written answer first |
| COTREX identity adopted, then changes | `place_id` undocumented; layer text still says "last updated on 2/5/2019" while edited 2026-08-27 (V-net [05]) | Do not key anything on it without a CPW statement |
| Cross-source merge produces a claim neither source makes | Four disagreements in section 9 | One source per fact; show disagreements, do not resolve them |
| A length or gain reads as surveyed | Clipped geometry; DEM method choices | TG10; labels; decision 16 |
| The override list becomes the real data model | Model D | Reason code, evidence and review date per entry; a cap or review trigger |
| Forest Service layer changes shape | Service rebuilt between fetches (V-net) | Required-field check on fetch; keep last good file (already the pipeline's behaviour, V-repo `fetch_trails.py:40-47`) |
| Sample is small | 40 Forest Service rows, about 40 COTREX rows | Treat every "in the samples" statement as provisional until the full attribute fetch is approved |
| Hermes facts not re-verified | COTREX app terms, competitor behaviour, closure feeds | Marked H throughout; verify before any specification relies on them |

---

## 13. Corrections and confirmations to the Hermes report (M6A)

| Hermes statement | Result here |
|---|---|
| COTREX is layer 15 of `CPWAdminData`; layer 2 is CPW Trail Segments | Confirmed (V-net [04], [05]). Layer 14 is COTREX Trailheads |
| "The current layer exposes 44 fields" | 45, counting `FID`, `Shape__Length` and `GlobalID` (V-net [05]) |
| No `trail_id`, no relationships, no domains | Confirmed (V-net [05]) |
| Item `licenseInfo` is a disclaimer with no reuse grant; `accessInformation` is "Colorado Parks and Wildlife" | Confirmed, quoted in the matrix (V-net [06]) |
| Stale "last updated on 2/5/2019" text against 2026-08-27 edits | Confirmed (V-net [05]) |
| `Shape__Length` is "in meters" | Web Mercator units, not ground metres (V-net [05]; I for the size of the error) |
| COTREX sample counts and key agreement unknown | Now sampled: Difficult Creek 5 rows, one `place_id`, `trail_num` 2146 (V-net [17], [23]) |
| Forest Service layer is `EDW_TrailNFSPublish_01` | The repository reads the sibling `EDW_TrailNFSPublishWithDataStatus_01`, which has the same 105 fields including `trail_cn`, `bmp`, `emp`, `globalid` (V-net [02], [03]) |
| `TRAIL_CN` definition; `BMP`/`EMP`; use families; `ALLOWED_TERRA_USE` | Confirmed from the metadata (V-net [01]) |
| Difficult Creek: 2 rows, `TRAIL_NO` 2146, `TRAIL_CN` 5695010314, 0–2.5 and 2.5–3.2656 | Confirmed (V-net [08]) |
| `OBJECTID` "should not be treated as durable" | Now demonstrated (V-net [08]–[15]) |
| COTREX app terms, About page, alerts, cadence | Not re-verified: `trails.colorado.gov` was outside this task's permitted hosts. Still H |

---

## Appendix A — every request made

25 HTTP GET requests, all with `curl`, on 2026-10-07. Metadata, or attribute
queries with `returnGeometry=false` and at most 20 records (or statistics or
a count). No geometry was requested and nothing was ingested. Responses were
saved outside the repository with the file names below; a local request log
holds the exact URLs with status codes. All returned HTTP 200.

Hosts: `data.fs.usda.gov`, `apps.fs.usda.gov`, `services5.arcgis.com`
(CPW's ArcGIS Online organisation), `www.arcgis.com`.

Forest Service trail query base, written `{T}` below:
`https://apps.fs.usda.gov/arcx/rest/services/EDW/EDW_TrailNFSPublishWithDataStatus_01/MapServer/0/query`

Forest Service field list, written `{F}`:
`objectid,globalid,trail_name,trail_no,trail_cn,bmp,emp,segment_length,gis_miles,admin_org,managing_org,trail_type,trail_class,trail_surface,national_trail_designation,mvum_symbol,terra_motorized,allowed_terra_use,motorcycle_managed,motorcycle_accpt,motorcycle_disc,motorcycle_accpt_disc,motorcycle_restricted,atv_managed,atv_accpt,atv_restricted,hiker_pedestrian_managed,hiker_pedestrian_accpt,hiker_pedestrian_disc,hiker_pedestrian_accpt_disc,hiker_pedestrian_restricted,bicycle_managed,bicycle_restricted`

Forest Service query tail, written `{Q}`:
`&outFields={F}&returnGeometry=false&resultRecordCount=20&orderByFields=trail_no,bmp&f=json`

COTREX query base, written `{C}`:
`https://services5.arcgis.com/ttNGmDvKQA7oeDQ3/arcgis/rest/services/CPWAdminData/FeatureServer/15/query`

| # | File | URL | Result |
|---|---|---|---|
| 01 | `01-usfs-meta.xml` | `https://data.fs.usda.gov/geodata/edw/edw_resources/meta/S_USA.TrailNFS_Publish.xml` | Field definitions, 105 attributes |
| 02 | `02-usfs-layer-datastatus.json` | `https://apps.fs.usda.gov/arcx/rest/services/EDW/EDW_TrailNFSPublishWithDataStatus_01/MapServer/0?f=pjson` | Layer fields and indexes |
| 03 | `03-usfs-service-datastatus.json` | `https://apps.fs.usda.gov/arcx/rest/services/EDW/EDW_TrailNFSPublishWithDataStatus_01/MapServer?f=pjson` | Service description, daily update statement |
| 04 | `04-cpw-service.json` | `https://services5.arcgis.com/ttNGmDvKQA7oeDQ3/arcgis/rest/services/CPWAdminData/FeatureServer?f=pjson` | 30 layers |
| 05 | `05-cpw-layer15.json` | `https://services5.arcgis.com/ttNGmDvKQA7oeDQ3/arcgis/rest/services/CPWAdminData/FeatureServer/15?f=pjson` | COTREX Trails, 45 fields |
| 06 | `06-agol-item-168f.json` | `https://www.arcgis.com/sharing/rest/content/items/168fccb0583f42f1afe57de6c9ce846d?f=pjson` | Service item, licence text |
| 07 | `07-agol-item-cae8.json` | `https://www.arcgis.com/sharing/rest/content/items/cae8ed959b8a4ed48680df62b31eec60?f=pjson` | Shapefile item, licence text |
| 08 | `08-usfs-difficult-creek.json` | `{T}?where=trail_name='DIFFICULT CREEK'{Q}` | 2 rows |
| 09 | `09-usfs-hunter-creek.json` | `{T}?where=trail_name='HUNTER CREEK' AND trail_no='2194'{Q}` | 4 rows |
| 10 | `10-usfs-0770-family.json` | `{T}?where=objectid IN (8913499,8916087,8917600,8923770,8925194,8928105,8937765,8939521,8941308,8951157,8952194,8953147){Q}` | **0 rows** — the repository's ids no longer exist |
| 11 | `11-usfs-douglas-aspen-hard.json` | `{T}?where=objectid IN (8964639,8970427,8968633,8970783,8977816,8982425,8972161,8973336,8928020,8916487,8922773,8925147){Q}` | **0 rows** |
| 12 | `12-usfs-colorado-trail-douglas.json` | `{T}?where=objectid IN (8924501,8925547,8955417,8955535,8963975,8971239,8971341,8972880,8973227,8973512){Q}` | **0 rows** |
| 13 | `13-usfs-0770-family.json` | as 10 with 604919 added to each id | 12 rows, names and numbers match the repository |
| 14 | `14-usfs-douglas-aspen-hard.json` | as 11 with 604919 added to each id | 12 rows, match |
| 15 | `15-usfs-colorado-trail-douglas.json` | as 12 with 604919 added to each id | 10 rows, match |
| 16 | `16-mvum-trails-layer.json` | `https://apps.fs.usda.gov/arcx/rest/services/EDW/EDW_MVUM_01/MapServer/2?f=pjson` | MVUM trails layer fields and description |
| 17 | `17-cotrex-difficult-creek.json` | `{C}?where=UPPER(name) LIKE 'DIFFICULT CREEK%' OR trail_num='2146'&outFields=*&returnGeometry=false&resultRecordCount=20&f=json` | 6 rows (5 Difficult Creek Trail, 1 unrelated road) |
| 18 | `18-mvum-trails-douglas.json` | `https://apps.fs.usda.gov/arcx/rest/services/EDW/EDW_MVUM_01/MapServer/2/query?where=id IN ('0646','0649','0649.A','0770') AND name IN ('ARROWHEAD','TROUT CREEK','TROUT CREEK CONNECTION','TURTLE MOUNTAIN')&outFields=objectid,rte_cn,id,name,bmp,emp,seg_length,symbol,mvum_symbol_name,seasonal,atv,atv_datesopen,motorcycle,motorcycle_datesopen,otherwheeled_ohv,otherwheeled_ohv_datesopen,adminorg,districtname,forestname,trailstatus,trailsystem,globalid&returnGeometry=false&resultRecordCount=20&orderByFields=id,bmp&f=json` | 7 rows |
| 19 | `19-cotrex-hunter-creek.json` | `{C}?where=trail_num='2194' OR (UPPER(name) LIKE 'HUNTER CREEK%' AND manager LIKE '%Aspen%')&outFields=*&returnGeometry=false&resultRecordCount=20&f=json` | 3 rows |
| 20 | `20-cotrex-indian-creek.json` | `{C}?where=UPPER(name) LIKE 'INDIAN CREEK%' AND trail_num LIKE '%800%'&outFields=*&returnGeometry=false&resultRecordCount=20&f=json` | 11 rows |
| 21 | `21-cotrex-arrowhead-turtle.json` | `{C}?where=(UPPER(name) LIKE 'ARROWHEAD%' AND trail_num LIKE '%646%') OR (UPPER(name) LIKE 'TURTLE MOUNTAIN%' AND trail_num LIKE '%770%')&outFields=*&returnGeometry=false&resultRecordCount=20&f=json` | 4 rows |
| 22 | `22-cotrex-multi-place-aspen.json` | `{C}?where=place_id_1>0 AND manager LIKE 'USFS Aspen%'&outFields=*&returnGeometry=false&resultRecordCount=8&f=json` | 8 rows (more exist) |
| 23 | `23-cotrex-place-16137-count.json` | `{C}?where=place_id=16137 OR place_id_1=16137 OR place_id_2=16137 OR place_id_3=16137&returnCountOnly=true&f=json` | count 5 |
| 24 | `24-mvum-southplatte-season-stats.json` | `https://apps.fs.usda.gov/arcx/rest/services/EDW/EDW_MVUM_01/MapServer/2/query?where=adminorg='021211'&outStatistics=[count of objectid as n]&groupByFieldsForStatistics=motorcycle_datesopen&returnGeometry=false&f=json` | 7 groups, 118 records |
| 25 | `25-cotrex-southplatte-access-stats.json` | `{C}?where=manager='USFS South Platte Ranger District'&outStatistics=[count of FID as n]&groupByFieldsForStatistics=access&returnGeometry=false&f=json` | 6 groups, 273 rows |

URLs are shown decoded for reading; the encoded forms are in `urls.log`.
Requests 10–12 were made before the renumbering was known and are kept as
the evidence for it.

Not requested, and why: `trails.colorado.gov` (terms and About pages) and
`fs.usda.gov` forest pages were outside the hosts permitted for this task;
no DEM source was contacted; no geometry was downloaded from any source.
