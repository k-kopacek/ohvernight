DRAFT - UNREVIEWED

# M4 water design: adversarial depth audit

Read-only audit by an independent reviewer on 2026-10-07, against the approved
specification (amendments A1–A3) and the M4-A implementation at `aa5c20b`
(draft PR #12). Nothing here is decided; the owner decides. It does not
repeat what is already recorded in `m4b-preparation/`, `decision-packets/`,
`claims/` or `hermes-track-i-3dhp-migration.md`; where a finding extends a
recorded item, it says so.

Method: throwaway Python run on the committed canonical data
(`v2/map-data-v2.json`, `v2/regions/douglas-co/research.json`), the display
artifacts, the manifests, the saved raw NHD pages and the code. No network
request, nothing written in the M4-A worktree. The grouping rule of 8.3 was
re-implemented independently and reproduces the dry run (71 Aspen groups,
1,273 drawn members; 35 Douglas groups, 1,608 drawn members).

Each statement is marked **VERIFIED** (measured or read in code),
**INFERENCE** (follows from verified facts about code not yet written) or
**UNKNOWN**.

## Summary

1. **A lake with a drawn stream through it cannot be selected by tapping it at ordinary zooms.** At Aspen's opening zoom (12), 24 of 46 displayed lakes have no tappable area at all; Maroon Lake has 1% at zoom 14. In M4-C a tap on Maroon Lake would open West Maroon Creek with "access and allowed activities are not established", while the lake's reviewed prohibition stays unseen (T1).
2. **Running either ordinary hydrology fetch script after M4-A merges erases every pre-M4 legacy ID** and replaces it with a self-alias; no validator rule notices (G1).
3. **A stale `restricted` claim is shown as a restriction forever**, but a restriction is also a conditional permission ("reservation required"). If the operator later closes the activity, the detail keeps implying it is available (T2).
4. **The lakes M4-C cares about most are cut by the county clip**: Cheesman is drawn at 37% of its source area, Strontia Springs at 35% in three pieces, Chatfield at 56%, McLellan at 11%. The area the detail would state is the uncut source figure (T3).
5. **The saved raw NHD pages, the only copy of the snapshot of a retired service, are git-ignored files in one worktree with no recorded hashes**, and two decision packets offer an "offline re-clip" that depends on them (D1).

Also notable: group IDs with `-pN` can silently re-point a claim (T4); from
2026-10-14 every Douglas water detail will say "refresh needed" about a
dataset that cannot be refreshed (T5); the owner-approved limitation sentence
says displayed streams are coded perennial, which is not true of drawn centre
lines (O1).

## TRUST ISSUE

### T1 — Lakes under a drawn stream are not selectable by tap

- **What.** The adapter resolves a tap by priority: point, label, line, polygon (`v2/explore/map-adapter.js:48`), and a line is hit within 14 px (`map-adapter.js:6`, `:37`). A lake polygon is chosen only where no line is within 14 px. The 8.3 rule draws the named centre line through a lake, so the lake's own area is mostly or wholly inside the stream's hit band. VERIFIED from code.
- **Evidence (VERIFIED, computed).** Share of each displayed lake's area farther than 14 px from any stream line that M4-B would draw, at 39.3° N:

| Region | Displayed | No tappable area at z11 | z12 | z13 | z14 | Under 10% tappable at z14 |
|---|---:|---:|---:|---:|---:|---:|
| Aspen (opens at z12) | 46 | 34 | 24 | 18 | 8 | 14 |
| Douglas (opens at z10) | 32 | 10 | 9 | 7 | 3 | 6 |

| Water (M4-C candidate) | z12 | z13 | z14 | z15 | Line that wins |
|---|---:|---:|---:|---:|---|
| Maroon Lake `nhd-72971124` | 0% | 0% | 1% | 21% | West Maroon Creek |
| Crater Lake `nhd-72971138` | 0% | 0% | 0% | 19% | West Maroon Creek |
| Grizzly Reservoir `nhd-72969562` | 0% | 0% | 7% | 42% | Lincoln Creek, Grizzly Creek |
| Strontia Springs Reservoir | 45% | 60% | 65% | 71% | Bear Creek |
| Chatfield Lake | 45% | 69% | 84% | 92% | Plum Creek |
| Cheesman Lake | 79% | 85% | 89% | 93% | Turkey Creek |

  If the South Platte is drawn (decision D-1), using only the segments already inside the county as a lower bound: Cheesman 26%, Chatfield 29%, Strontia Springs 17% at z12. Trails and roads also outrank polygons, so the real figures are lower.
- **Why it matters.** Validation case U9 records "line wins over polygon" as expected behaviour. Its scale, and its M4-C consequence, are not recorded: a person taps a lake that carries a reviewed prohibition and reads WW1 for a creek. INFERENCE for M4-C (no claims exist yet).
- **Classification.** TRUST ISSUE (also an owner decision on tap priority for water).
- **Follow-up.** (1) Add a browser check: tap the centroid of Maroon Lake at z13 and assert which feature is selected; record the result as the accepted behaviour or as a failure. (2) Question for the owner: when a tap is inside a displayed waterbody, should the waterbody win over a stream line of the water layers (a shell or registry rule; the adapter's exports need not change)? (3) If not, M4-C must at least show, in a stream's detail, that it passes through a water with a record.

### T2 — Staleness never downgrades `restricted`, which is partly a permission

- **What.** 9.3: `allowed` past its age becomes "Not established"; `restricted` stays "Restricted · Review overdue" indefinitely. A `restricted` claim states that the activity is available on conditions. Draft examples: Rueter-Hess paddling "Reservation required; set days and hours"; Chatfield swimming "Designated swim beach only, Memorial Day to Labor Day". If the operator ends the activity, the stale line still tells the reader it can be done. The asymmetry treats `restricted` as the safe side; relative to `prohibited` it is the permissive side. VERIFIED against the specification text; INFERENCE about behaviour.
- **Related.** `effective_to` is stored but never evaluated (9.4). Maroon Lake's order ends 2027-11-15; after that the detail shows "Prohibited" until someone edits the record. That direction is conservative. An `effective_from` in the future is shown as in force now.
- **Classification.** TRUST ISSUE; needs an owner decision because it changes an approved table.
- **Follow-up.** Question for the owner: past its maximum age, should a `restricted` line keep the status word but replace the reviewer's summary with a fixed sentence (for example "Conditions last reviewed <date>; check the operator's page"), or carry a hard second limit after which it reads "Not established"? Add the chosen case to the freshness pure-function test.

### T3 — Clipped lakes: stated area, slivers, and the three priority waters

- **What.** `area_sqkm` is the source attribute of the whole lake. Douglas geometry is cut at the county polygon. The detail's "Computed by Ohvernight" area (specification 11, item 3) would state the whole lake for a polygon drawn in part. The dry run recorded the same defect for `length_km` (Q4) and the South Platte packet mentions Cheesman once as a padding failure mode; the area statement, the other lakes and the slivers are not recorded.
- **Evidence (VERIFIED).**

| Water | Source km² | Drawn km² | Drawn share | Pieces |
|---|---:|---:|---:|---|
| Chatfield Lake `nhd-117822739` | 5.622 | 3.175 | 56% | 1 |
| Cheesman Lake `nhd-120030962` | 3.581 | 1.322 | 37% | 2, one of them 10 m² (a 5-point ring) |
| Strontia Springs Reservoir `nhd-117834809` | 0.328 | 0.116 | 35% | 3 (0.39, 1.11, 10.04 ha) |
| McLellan Reservoir `nhd-117822697` | 0.774 | 0.088 | 11% | 1 |
| Wolhurst Lake `nhd-117822893` | 0.034 | 0.0024 | 7% | 1 (0.24 ha) |
| Unnamed `nhd-117822709` | 0.028 | 0.015 | 54% | 1; passes the 2 ha test on the source figure, drawn at 1.5 ha |

  Aspen: no displayed lake is cut. All clip-made multipart geometry is created by the clip (0 multipart features in the raw pages; 8 + 11 lines and 2 polygons in canonical data). The proposed 500 m Douglas padding does not restore Chatfield or McLellan.
- **Classification.** TRUST ISSUE (a computed figure that does not describe what is drawn), with a DATA GAP behind it.
- **Follow-up.** (1) Extend proposed clarification Q4 to area: compute the displayed area from drawn geometry, or show the source figure under "From the source" and not under "Computed by Ohvernight". (2) Question for the owner: keep waterbodies whole when any part is inside the region (clip lines, not polygons)? (3) Test: no display polygon part under a stated minimum area; today that fails on Cheesman's 10 m² part.

### T4 — `-pN` group IDs can re-point a claim or an exclusion without failing validation

- **What.** 8.3 step 5 numbers the parts of a `gnis_id` by perennial length. The number is a rank, not an identity. Any change to membership (padding, the connector decision, a re-clip, a reviewed exclusion of one part, a source change) can swap which reach is `nhd-gnis-<id>` and which is `-p2`. `water-recreation.json` and `water-review.json` key on display IDs (9.2 rule 1, 8.5). R73 and R74 check only that the ID resolves, so a record that now points at a different reach still passes. INFERENCE (none of this is implemented).
- **Evidence (VERIFIED).** Three Aspen `gnis_id` values are multi-part today, giving four `-pN` IDs. Galena Creek's two parts are 1.658 km and 1.529 km of perennial length: 129 m decides which is the base ID. Granite Creek's order is 4.148 / 0.701 / 0.566 km by attribute and 0.867 / 0.482 / 0.233 km by geometry (same order today). The specification does not say whether numbering happens before or after exclusions.
- **Classification.** TRUST ISSUE.
- **Follow-up.** (1) Each registry and review record carries the water's `name` and `gnis_id` (and for a part, its lowest member ID) as a cross-check; R73 and R74 fail on mismatch. (2) Fixture: add one segment so two parts swap rank; the build must fail or the record must follow the reach. (3) State in 8.3 that numbering is computed before exclusions.

### T5 — Douglas water will read "refresh needed" from 2026-10-14

- **What.** The Douglas water layers declare `max_age_hours: 168` (`v2/regions/douglas-co/region.json`, layers `waterbodies` and `waterways`); Aspen's `hydrology` declares `null`. `v2/explore/evidence.js:12` and `:44` append "older than the refresh policy; refresh needed" to the layer row and to every feature's "Source fetched" line when the age is exceeded. VERIFIED.
- **Evidence.** Retrieval time `2026-10-07T00:32:43Z` plus 168 h is `2026-10-14T00:32:43Z`. After that every Douglas water detail says a refresh is needed. The source was retired in 2023 and cannot change; the specification authorises one fetch in M4 (section 5); the refresh tool cannot be re-run safely (G1). The two regions will say different things about the same frozen dataset.
- **Classification.** TRUST ISSUE (a statement that implies newer data exists).
- **Follow-up.** Question for the owner: set the Douglas water layers to `null` like Aspen, with the retirement stated in the scope sentence (packet 6 already proposes that wording)? Add a test that both regions' water layers declare the same policy.

## DATA GAP

### D1 — The raw snapshot of a retired service is not preserved

- **What.** The saved pages (`v2/pipeline/data/raw/m4a-nhd-refresh/`, 15 MB; staging 35 MB) are ignored by `.gitignore:42` and exist only in the `m4a-source-preservation` worktree. `nhd-snapshot.md` records SHA-256 for the canonical files only, not for the raw pages. VERIFIED.
- **Why it matters.** Packets 2 and 4 offer "an offline re-clip of the saved M4-A raw pages" as the way to avoid a second request. The pages also hold the 1,248 named Douglas flowlines and 142 waterbodies the county clip dropped (South Platte River 271 segments, North Fork South Platte 98, Buffalo Creek 85). Removing the worktree after merge removes them. Whether the NHD service stays online is UNKNOWN.
- **Classification.** DATA GAP.
- **Follow-up.** Before the worktree is removed: archive the two directories outside the repository, and add a manifest of file names, sizes and SHA-256 to `nhd-snapshot.md`. Owner question: is a compressed archive of public-domain raw pages acceptable as a release asset?

### D2 — Source feature dates are kept but never shown; most displayed lakes are from 2003

- **Evidence (VERIFIED).** `source_date` of displayed waterbodies: Aspen 34 of 46 dated 2003, 8 dated 2012; Douglas 16 of 32 dated 2004. Drawn stream members are mostly 2012 (1,160 of 1,273; 1,501 of 1,608). Rueter-Hess is dated 2014-01-15 at 0.875 km². Whether that outline matches the reservoir today is UNKNOWN.
- **What.** Detail content (specification 11, item 2) shows "Source fetched 2026-10-07" and not the feature's own date, so the only date a reader sees is the newest one.
- **Classification.** DATA GAP in what is presented; the remedy is an OWNER DECISION on wording.
- **Follow-up.** Question for the owner: add a line under "From the source" giving the source's feature date (it needs an approved label).

## TEST GAP

### G1 — An ordinary fetch after M4-A destroys the legacy ID chain, and R68 passes

- **What.** `03_fetch_hydrology.py` (the `attach_legacy_ids(old_layer, layer_features)` call) and `enrich_douglas.py` (same call for `waterbodies` and `waterways`) match new features against the *current* canonical file. `attach_legacy_ids` (`lib/water.py:173-178`) overwrites `legacy_ids` with the IDs of the matched old features. Before M4-A those were row-number IDs. After M4-A they are the feature's own ID.
- **Evidence (VERIFIED by running the real function on the committed data, in memory).**

| Layer | Features | Pre-M4 legacy IDs lost | Left with a self-alias |
|---|---:|---:|---:|
| Aspen waterbodies | 514 | 514 | 514 |
| Douglas waterbodies | 2,135 | 33 (all that had one) | 2,135 |
| Douglas waterways | 2,359 | 2,359 | 2,359 |

  R68 (`lib/region_contract.py:256-286`) requires distinct non-empty strings, no legacy ID on two features, and alias keys equal to displayed legacy IDs. A self-alias satisfies all three. `refresh_m4a_water.py --review-staged` has the same single-use shape: it diffs against `origin/main` (`:284`), which after merge is the new data.
- **Extends.** The South Platte packet says the padded extent needs "an addendum to the ID map" and that cut segments "become longer". Longer geometry fails exact-geometry matching, so those features would lose their legacy IDs as well.
- **Classification.** TEST GAP (a missing rule over a latent defect).
- **Follow-up.** (1) R68: a legacy ID must not equal any current feature ID in the region. (2) A test pinning the committed legacy counts (Aspen 6,926; Douglas 2,392) and failing if `nhd-snapshot-id-map.csv` and canonical `legacy_ids` disagree. (3) Any re-clip or re-fetch carries `legacy_ids` forward by `id`, never by re-matching.

### G2 — "Ambiguous branch" has no definition, and no loop or braid fixture exists

- **What.** O2 and 8.3 forbid joining "where a branch is ambiguous". The algorithm (steps 2–3) has no such test: a braid or loop of one `gnis_id` is simply one connected component and both channels are drawn. The validation plan has no fixture for two segments sharing both end points, or for three same-`gnis_id` segments at one node.
- **Evidence (VERIFIED).** The real data has none: 0 parts with a cycle, 0 nodes where three or more candidates of one `gnis_id` meet, 0 closed single lines, in both regions. So the rule is untested, not violated.
- **Classification.** TEST GAP.
- **Follow-up.** Two fixtures (loop; three-way node) with the expected result written down, and a build report line listing every node of degree three or more within a `gnis_id`, so the first real case is seen.

### G3 — ID uniqueness is case-sensitive and sanitising can merge distinct source IDs

- **Evidence (VERIFIED).** Source IDs come in three forms: numeric (8 or 9 digits), braced upper-case GUID (54 Aspen, 5 Douglas) and bare lower-case GUID (46 Douglas). `sanitize_source_id` (`lib/water.py:55-61`) deletes every character outside `[A-Za-z0-9-]` and does not fold case. No collision exists today: 0 duplicate IDs, 0 duplicates ignoring case, 0 IDs beginning `nhd-gnis-`, 0 IDs shared between regions.
- **What could collide.** `{X}` with `X`; `12.3` with `123`; `a_b` with `ab`; and two IDs differing only in case stay distinct for R66 but not for a case-insensitive consumer (a URL, a file name). R66 would catch an exact collision only.
- **Classification.** TEST GAP.
- **Follow-up.** R66 also checks uniqueness ignoring case; a unit test for the three collision shapes.

### G4 — The alias file has no reader

- **Evidence (VERIFIED).** The only reference to `water-aliases.json` outside the pipeline is `v2/pipeline/tests/browser/explore-checks.mjs:254`, which asserts it is *not* requested. No code resolves a legacy ID. Specification 7.3 says "the browser resolves an ID through the display index".
- **Consequences.** In M4-B the alias keys shrink to displayed features: about 239 Aspen and 751 Douglas line features, and every hidden waterbody, drop out of the file. R68 requires that, so nothing fails; an outside reference to such an ID gets no answer and no "was removed" marker. If the canonical feature later disappears (a source change), `nhd-snapshot-id-map.csv` is the only record. Growth is bounded: one key per displayed feature per ID generation (61,732 and 88,729 bytes today).
- **Classification.** TEST GAP now; FUTURE TECH DEBT if left.
- **Follow-up.** Either a ten-line resolver with a test (legacy ID → display ID, or "not displayed"), or strike the sentence from 7.3 and call the file an offline record.

## IMPLEMENTATION DETAIL

### I1 — Water has no labels today, and the adapter's rule would anchor a river's label on its first member

- **Evidence (VERIFIED).** `v2/explore/shell.js:134` sets labels only for kinds `trails` and `recreation_sites`. The label anchor is `item.getCenter()` (`map-adapter.js:265`); in the vendored Leaflet 1.9.4, `Polyline.getCenter` uses `_defaultShape()`, which for a multi-line is the first line only. A label is drawn only when the anchor is inside the viewport, and for trails only from zoom 14.
- **Consequence (INFERENCE).** With members ordered by `id` (8.3 step 7) the anchor is the member with the lowest ID. Roaring Fork (111 members, 48.8 km) would be anchored on a 201 m segment; Maroon Creek, Difficult Creek, Cherry Creek and Jackson Creek at one end of the river. In 30 of 71 Aspen groups and 19 of 35 Douglas groups the anchor is in the outer third of the group's extent; in 17 and 9 groups the anchor member is under 100 m long. A person looking at the middle of a long river sees no name. Specification 11 says "a stream gets one label, placed by the adapter's existing rule", and case U3 taps it.
- **Follow-up.** Coordinator to decide before the brief goes out: (a) no stream labels in M4-B (strike U3), or (b) anchor on the visible member nearest the viewport centre. (b) changes adapter internals, which the draft brief currently forbids.

### I2 — "Ordered by `id`" is ambiguous

- **Evidence (VERIFIED).** IDs mix 8- and 9-digit numbers and GUIDs. String order and numeric order differ in 56 of 71 Aspen groups (0 of 35 in Douglas). The order sets the MultiLineString's line order, `water_groups`, the tie-break in step 5 and the label anchor (I1).
- **Follow-up.** State "Unicode code-point order of the `id` string" in 8.3 and use the same comparison in Python and JavaScript; case G-u covers reproducibility but not the definition.

### I3 — A member can be several lines

- **Evidence (VERIFIED).** Three drawn members are clip-made MultiLineStrings: `nhd-165831253` (Granite Creek, 3 pieces, 0.45 km drawn of 1.82), `nhd-72972600` (South Fork Fryingpan River, 2), `nhd-133040832` (South Fork Lake Creek, 2). Step 7 says each member is "appended as one line"; case G-a expects lines equal to members. The extent-edge packet asks the owner to confirm such a segment stays one member; the validator consequence is not written down.
- **Follow-up.** R71 compares the flattened lines of the ordered members, and `member_count` counts features, not lines. One fixture with a two-piece member.

### I4 — Zero and coarse areas

- **Evidence (VERIFIED).** `area_sqkm` is exactly 0 on 87 Aspen and 272 Douglas waterbodies (largest real area among them 0.05 ha) and is quantised to 0.001 km² on most others (367 of 514; 1,798 of 2,135). One displayed water is affected: Silver Dollar Pond (`nhd-72971158`), source area 0, real area 0.027 ha, which the detail would show as "0.0 ha". No unnamed lake sits between 0.0195 and 0.02 km², so the threshold comparison has no floating-point edge today.
- **Follow-up.** Decide the display for a zero area (omit the line). Validation case E14 covers null but not zero.

### I5 — `apply_m4a_water.py` does not reproduce the committed manifests

- **Evidence (VERIFIED).** Lines 116–118 and 131–134 write new `sources.usgs_nhd.scope` sentences ("NHD source geometry and retained source attributes…"). The committed manifests carry the old sentences, pinned by `pipeline/tests/test_region_contract.py:25-26`. So the manifests were restored by hand after the script ran, and running the script again would put unapproved trust text in both manifests (the pinned test would then fail, which is the safeguard).
- **Follow-up.** Remove the two assignments, or mark the script as historical in its docstring.

### I6 — A group can carry only one evidence reference

- **What.** The grouped display feature has a single `evidence` index (8.4). Today every flowline in a region shares one evidence object (VERIFIED: one row in each evidence table). A partial re-fetch (the padded Douglas strip) would give new members a later `retrieved_at` unless the whole layer is re-stamped. The specification does not say what a group shows when members disagree. INFERENCE.
- **Follow-up.** One sentence in 8.4: the build fails if a group's drawn members do not share one evidence object.

## OWNER DECISION

### O1 — The approved limitation sentence overstates "coded perennial" for streams

- **Sentence (O5, exact).** "Displayed streams and lakes are coded perennial; some reservoirs have no hydrographic category stated by the source."
- **Evidence (VERIFIED).** Drawn centre lines are coded `55800`, which states no category: 17.9 of 514.4 km drawn in Aspen and 13.3 of 428.8 km in Douglas; 38 of 71 and 22 of 35 groups contain some. Roaring Fork River is 20% centre line; Willow Creek `00185138` is 47%. If the South Platte is drawn as packet 2 recommends, 73.2 km of it would be shown as "River or stream · Perennial" on the strength of 0.08 km of perennial stream (the packet's own figure). "Some reservoirs" is one feature: Rueter-Hess is the only displayed feature the source types as a reservoir in either region.
- **Question.** Keep the sentence as approved, or amend it (for example "…streams are selected where the source codes them perennial; centre lines through lakes and wide rivers carry no category…")? WW12 on a group has the same issue.

### O2 — Twenty displayed waters named "Reservoir" would be labelled "Lake or pond"

- **Evidence (VERIFIED).** The source types them `390` (lake or pond): 6 in Aspen (Grizzly, Wildcat, Lost Man, Marolt, Christenson, Elk Creek Number 2) and 14 in Douglas (including Strontia Springs, Aurora-Rampart, Platte Canyon and McLellan). Aspen's five `436` features are all `43624` (treatment) and are hidden. WW15 "Unnamed reservoir" cannot occur with today's data.
- **Question.** Is "Lake or pond" under "From the source" acceptable beside a title that says Reservoir? It is faithful to the source and will look like an error.

### O3 — What the claim registry (specification 9) cannot express

Checked against the draft records. INFERENCE from the schema text unless marked.

| Gap | Example | Smallest remedy to consider |
|---|---|---|
| One `operator` string | Rueter-Hess: Douglas County runs recreation, Parker Water owns it. Chatfield: CPW and the Corps of Engineers | Allow a list, or define `operator` as "who publishes the rule" |
| One `source_url` per claim | Rueter-Hess boating rests on the main page and the FAQ page | Allow a second URL in the same evidence object |
| A rule tied to an activity M4 does not model | Maroon Lake: float tubes are prohibited, so the line reads "Fishing: Not established" while a fishing method is prohibited | Decide whether such a rule may set fishing to `restricted` |
| `restricted` covers four different things (place, season, reservation, craft) | Cheesman fishing; Chatfield swimming; Rueter-Hess paddling | Goal 7 says claims are queryable by M8; one status word cannot be queried by kind. Record as known debt or add an optional `conditions` list |
| A water in several polygons | Warren Lakes, Granite Lakes and Ruby Lakes are each two features with one `gnis_id` and one name (VERIFIED) | A record needs writing twice; search shows the name twice |
| A river in several groups | Hunter Creek today (two groups of one `gnis_id`) | Same |
| Conflicting official pages | Checklist item 12 puts the conflict in `notes`; `notes` has no schema and no rendering rule | Define `notes` as strings, not rendered |
| No identity check in the record | See T4 | `name` and `gnis_id` in the record |
| Reach-scoped rules | Already recorded as C-2 | Addition: if the South Platte is drawn and river records are deferred, a tap in Waterton Canyon shows WW1 beside Strontia Springs' "Prohibited", though the same operator sentence covers that reach |

All twelve draft and candidate water IDs in `draft-records-for-owner-review.md` exist in the M4-A data and are eligible under 8.2 (VERIFIED).

## FUTURE TECH DEBT

### F1 — What a move off NHD breaks in this code, beyond track I

Track I covers the rules. These are the code and data points (VERIFIED locations; consequences are INFERENCE):

| Where | Hard-coded | Effect of a 3DHP move |
|---|---|---|
| `refresh_m4a_water.py:23`, `:354-361`; `config/sources.yaml:19`; `enrich_douglas.py` feeds | Service URL and layer numbers 6, 9, 12 | Edited in three places |
| `refresh_m4a_water.py:59`; `lib/water.py:23-45` | Required fields `permanent_identifier`, `ftype`, `fcode`; the field map | 3DHP has none of the three |
| `lib/water.py:65`, `:149`; `lib/region_contract.py:243-244` | Prefix `nhd-` and namespace `usgs_nhd`, in both the build and the validator | R66 rejects any other namespace, so NHD and 3DHP features cannot coexist during validation |
| `lib/water.py:181-213` | Legacy matching by exact geometry JSON | Any coordinate difference matches nothing; every alias is lost |
| Group ID `nhd-gnis-<gnis_id>` | The 8-character zero-padded string (VERIFIED: every `gnis_id` is 8 digits) | Track I's samples show `gnisid` without leading zeros (`202884` against `00202884`). A naive rebuild changes every group ID and orphans every claim, exclusion and alias. Keeping the ID needs explicit padding, and keeps a `nhd-` prefix on data that is no longer NHD |
| `water_display.json` | Keys are NHD `ftype` and `fcode` | Already in track I |
| Per-feature `evidence.source_url`; manifest `source_urls` | NHD layer URLs | Rewritten on every feature |

- **Follow-up.** No action in M4. Add to the roadmap item in section 18: "group-ID continuity test: the padded `gnis_id` of every M4 group resolves in the candidate source".

### F2 — The refresh tooling is single-use

`refresh_m4a_water.py` has no extent or region arguments, refuses to change a saved query plan (`:75-76`, a sound safeguard), and its review mode compares against `origin/main` (`:284`). A padded Douglas request (packet 2) therefore needs a code change to the script that the specification calls the single controlled refresh, and must not reuse `attach_legacy_ids` (G1). VERIFIED. Follow-up: name this in step 0 of the M4-B blueprint.

## Checked and sound

| Area | Result | Status |
|---|---|---|
| Field completeness | `source_id`, `ftype`, `fcode`, `visibility_filter`, `source_date` never null in any layer. `name` and `gnis_id` are both set or both null on every feature (0 named with no `gnis_id`, 0 the reverse), with no blank or padded strings. `reach_code` null only on 58 + 1 swamp or marsh rows. No `fcode` outside the configuration's recorded list. `length_km` never zero or negative | VERIFIED |
| Raw pages against canonical | Every query returned its planned count; every `permanent_identifier` distinct and non-null; every canonical feature is in the raw pages; the only raw features missing from canonical data are those the clip removed | VERIFIED |
| One `gnis_id`, two unrelated rivers | None. Every multi-part gap is explained by a connector, the extent edge or an undisplayable stub; largest gap between displayable parts 1.36 km (Granite Creek, edge) | VERIFIED |
| Same name, different `gnis_id`, adjacent | None share an end point; nearest pair is 11.5 km apart | VERIFIED |
| One `gnis_id`, two names | None, across all flowline classes | VERIFIED |
| Near-miss end points | None. Canonical coordinates carry 13–14 decimals; rounding to six neither splits nor merges any part. No end point of one part lies on the interior of another part of the same river | VERIFIED |
| Line topology | 0 duplicate geometries (including reversed), 0 self-intersecting lines, 0 lines that collapse at six decimals. Shortest lines are clip slivers (0.84 m and 0.86 m), neither a group on its own | VERIFIED |
| Polygon topology | 0 invalid polygons, 0 overlaps between displayed waterbodies; holes on 9 + 4 features, handled by the hit test | VERIFIED |
| Unnamed members in a named group | Impossible with this data: members share a non-empty `gnis_id`, and name follows `gnis_id` | VERIFIED |
| Canal names in the stream class | 0 perennial stream segments carry a ditch, canal, tunnel or conduit name | VERIFIED |
| River through a lake | Named centre lines carry the river's `gnis_id`; no group is broken at a lake. 85 Aspen and 66 Douglas drawn centre-line segments run through small lakes that are not displayed, which only means the line continues | VERIFIED |
| Display against canonical (M4-A) | 0 orphan display features, 0 duplicate IDs, 0 geometry differences beyond six-decimal rounding and duplicate-vertex removal, 0 property differences, 0 dropped parts, 0 invalid shapes after rounding | VERIFIED |
| Orphan display feature | Caught today by R61's ID-set equality (`region_contract.py:410-413`). For grouped layers the amended R61 with R69 and R70 covers it as specified | VERIFIED today; INFERENCE for M4-B |
| Legacy IDs (as committed) | Exactly one per pre-M4 feature, none shared, none equal to a current ID; alias keys equal displayed legacy IDs; the full map is committed as `nhd-snapshot-id-map.csv` | VERIFIED |
| Hidden large water | No lake or reservoir of 10 ha or more is hidden by the 8.2 rule in either region | VERIFIED |
| Clip output types | Only lines and polygons result. `clip_geometry` could return a point or a mixed collection on a future re-clip; `build_display.py` and R22 would stop the build | VERIFIED today; INFERENCE for a re-clip |
| Manifest statements | Layer limitations hold for what M4-A displays; `source_urls` match the evidence on features; `extent_padding_deg` holds (Aspen vertices reach exactly the padded box). The two scope sentences are false as packet 6 already records. `spatial_precision: source_published` holds except for the 184 + 82 lines and 7 + 12 polygons cut by the clip | VERIFIED |

## Proposed follow-up tasks, ranked

| # | Task | Finding | Who | Size |
|---|---|---|---|---|
| 1 | Archive the raw and staged NHD files outside the worktree and record their hashes in `nhd-snapshot.md` | D1 | Coordinator, before the worktree is removed | Minutes |
| 2 | R68: a legacy ID may not equal a current ID; pin the legacy counts; forbid re-matching in any re-clip | G1 | M4-B brief, step 0 or 3 | Small |
| 3 | Owner question and browser check on tapping a lake that has a stream through it | T1 | Owner, before M4-B checkpoint 2 | Decision plus one check |
| 4 | Owner question on stale `restricted` claims and on `effective_to` | T2 | Owner, before M4-C | Decision plus one test |
| 5 | Records carry `name` and `gnis_id`; R73 and R74 cross-check; numbering fixed before exclusions | T4 | M4-B (review list) and M4-C | Small |
| 6 | Area from drawn geometry, or moved under "From the source"; minimum polygon-part size; owner question on keeping lakes whole | T3 | Extend Q4; owner | Small plus decision |
| 7 | Douglas water `max_age_hours`: decide before 2026-10-14 | T5 | Owner | One line |
| 8 | Limitation sentence and "Lake or pond" label: confirm or amend | O1, O2 | Owner, with packet 6 | Decision |
| 9 | Stream labels: none in M4-B, or anchor on the visible member | I1 | Coordinator | Decision; (b) is medium |
| 10 | Define ID order; multi-line members in R71; zero area; one evidence object per group | I2, I3, I4, I6 | Coordinator amendments | Small |
| 11 | Loop and three-way-node fixtures; degree-three report line | G2 | M4-B tests | Small |
| 12 | Case-insensitive ID uniqueness | G3 | M4-B tests | Small |
| 13 | Alias resolver with a test, or strike the sentence in 7.3 | G4 | Coordinator | Small |
| 14 | Registry gaps table: decide which are accepted debt | O3 | Owner, with C-1 to C-5 | Decision |
| 15 | Show the source feature date | D2 | Owner | Decision plus one string |
| 16 | Remove the scope assignments from `apply_m4a_water.py` | I5 | Any later pull request | Minutes |
| 17 | Roadmap note on group-ID continuity and the single-use refresh tool | F1, F2 | Coordinator | Minutes |

## What could not be established

- Whether the NHD service will stay online, and whether Rueter-Hess's 2014 outline matches the reservoir today (no network).
- How the tap priority and label anchor behave on a device; the figures are computed from the adapter's code and geometry, not observed.
- The South Platte tappability figures after padding: computed only from the segments already inside the county, so they are a lower bound on the effect.
- The 3DHP `gnisid` format: taken from track I's retrieved samples, not re-checked.
