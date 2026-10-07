# M4-B owner decision packet (consolidated)

Prepared by the coordinator on 2026-10-07, after M4-A merged (`main` at `f2c2de2`, PR #12). **Nothing here is decided.** Production M4-B does not start until the owner answers items 1 to 7. Each item has an approval line the owner can answer with a letter.

This packet replaces nothing. It gathers the four detailed packets in this directory ([south-platte.md](south-platte.md), [connectors.md](connectors.md), [extent-edge.md](extent-edge.md), [threshold.md](threshold.md)), [source-scope-wording.md](source-scope-wording.md) and [open-questions-for-m4b.md](../m4b-preparation/open-questions-for-m4b.md), and adds what Codex's independent recomputation found. Codex's work is on the local branch `codex/autonomous-technical-prep` at `d7837f8` (`docs/research/codex-autonomous/2026-10-07/WATER-TECHNICAL-VALIDATION.md`); it is not on GitHub yet.

How the evidence was checked for this packet: the coordinator read the approved specification in full, the detailed packets' decisions, options and recommendations, and Codex's validation report, and re-ran the elevation check against the merged data. The coordinator did not recompute the South Platte, connector or extent-edge numbers; where the original packet and Codex's recomputation agree, that is stated, and where they differ, both figures are given.

## Summary

| # | Question | Recommendation | Owner's stated leaning | Rule or wording change |
|---|---|---|---|---|
| 1 | South Platte: pad Douglas water by 0.005°? | Yes, with one new authorized NHD request for Douglas | Approve if still supported | Extent, data, coverage wording |
| 2 | Same-GNIS connectors count for connectivity? | Yes, connectivity only | Yes, connectivity only | One sentence, one invariant |
| 3 | Granite Creek and other extent-edge splits | Accept the split | Accept unless padding fixes it | One clarifying paragraph |
| 4 | Unnamed-waterbody threshold | Keep 2 ha | Keep 2 ha | None |
| 5 | Layer titles | `Rivers and streams`, `Lakes and reservoirs` | Same | Two strings per region |
| 6 | Source-scope wording | Option A, adjusted if item 1 is approved | — | Two strings |
| 7 | Grouped river length | Computed from held geometry | Computed from displayed geometry | Three definitions |

The evidence still supports every one of the owner's leanings. Item 1 carries a question the leaning did not cover: where the padded data comes from.

---

## 1. South Platte extent and padding

**Question.** Should the two Douglas water layers be kept out to 0.005° (about 430 m east-west, 556 m north-south) beyond the county line, with the approved selection and grouping rules unchanged? And if yes, is one new NHD request for Douglas authorized to fill the padded strip?

**Evidence.**

- Under the approved rule the South Platte River is not drawn at all in Douglas County. The only named perennial stream segment the rule needs (source id `117795757`) lies 11.5 m outside the county line. The county line follows the river, so the clip cuts the river's 75 centre-line segments into 57 visible pieces.
- With 0.005° padding and no rule change, the river becomes one group, `nhd-gnis-00201759`, drawn as one continuous line of 343 members and 73.3 km from above Cheesman Lake to Chatfield Lake. The original packet and Codex's recomputation agree on this.
- The drawn fraction is 0.96 by either measure Codex tried (0.965 by geometry, 0.956 by source length). The original packet's 0.97 was rounded. Both pass the 0.8 check.
- No other river is absorbed. The North Fork South Platte River stays separate. The 2.6 km below Chatfield dam stays undrawn because the source joins it only through a canal-coded segment.
- Side effects of the padding alone: three new short groups appear (Wigwam Creek 0.5 km, Brush Creek 0.6 km, Gunbarrel Creek 0.6 km); eleven existing rivers lengthen slightly (largest, Trout Creek, +0.56 km); 335 flowlines and 25 waterbodies are added; 94 existing flowlines get longer. At 2 ha Douglas shows 37 waterbodies, up from 32.
- **New finding (Codex).** The saved M4-A response pages cannot fill the whole padded strip. The M4-A query box leaves 63.4 km² of the padded shape uncovered. The saved pages plus the packet's targeted South Platte sample are enough to draw the river; they are not enough to say that every other water in the strip is present.

**Options.**

| | What it is | Result |
|---|---|---|
| A | Keep the current clip and rule | South Platte absent; the expected-major-rivers check stops the M4-B build |
| B | Change the rule: a centre line may start a group when the area it runs through is coded perennial stream or river | Still 57 fragments without padding; needs the Douglas area layer, a new request and a rule amendment; also draws some pond-seeded creeks |
| C | Reviewed inclusion for the South Platte | 43 tappable fragments; needs a new kind of exception |
| D1 | Pad by 0.005°, rule unchanged, **with one new controlled NHD request** for the two Douglas water queries at the padded extent | One river, one line; the padded strip is complete |
| D2 | Pad by 0.005°, rule unchanged, **from saved pages only** | One river, one line; other water in 63.4 km² of the strip may be missing, and the coverage wording must say so |

**Trade-offs.** Padding is the only thing that makes the river continuous; no rule change does. D leaves the approved rule alone. D1 costs a second live request, which the specification does not currently allow (section 5 authorizes exactly one, already used). D2 needs no request but stores a strip that is knowingly incomplete, which is hard to describe honestly in one sentence and would be a trap for M5 to M8.

**Recommendation.** D1. Bear case: the result rests on one 76 m segment; if a future source drops it the river disappears again. The build's expected-major-rivers check is the safeguard, and the source's own area categories agree with the result today.

**Code and data impact.**

- Specification section 5: a Douglas water-extent paragraph, and an explicit authorization for one more NHD request (Douglas layers 6 and 12 only, padded extent, same host, no key). Section 8.3: correct the "Wide rivers" paragraph.
- Data: Douglas `research.json` water layers grow by about 335 flowlines and 25 waterbodies; the snapshot document and ID map gain an addendum. Legacy IDs carry forward under amendment A4, which was fixed for exactly this case.
- Manifest: the padding on the two Douglas water layers; `expected_major_rivers` lists the South Platte.
- Every non-water layer stays clipped to the county and byte-identical.

**Tests required.** South Platte is one group and one connected line; drawn fraction at least 0.8; with padding at zero the build fails on the expected-rivers check; no member carries another `gnis_id`; no drawn coordinate is invented; no Douglas water feature lies beyond the padding; non-water layers byte-identical; every pre-existing legacy ID still present exactly once; byte budgets hold; the river is inspected on the phone.

**Trust impact.** Water is drawn up to about 500 m outside the county outline, on the Jefferson County side of the river. The coverage and limitation text must say that water in that strip is source geometry only and that nothing else is known there. This interacts with item 6. No access, activity or ownership statement changes.

**Approval line.** Choose A, B, C, D1 or D2. If D1: "I authorize one further NHD request for Douglas County layers 6 and 12 at the padded extent."

---

## 2. Same-GNIS connector continuity

**Question.** May a connector segment that carries a non-empty `gnis_id` take part in connectivity for that same `gnis_id` only: never drawn, never selectable, never joining a different `gnis_id`?

**Evidence.** Hunter Creek (on the expected-rivers list) and Galena Creek in Aspen each appear as two rivers, 19 m and 139 m apart, only because the short source segment joining their reaches is coded as a connector. Of 66 connectors in the two regions (65 Aspen, 1 Douglas), four carry a `gnis_id`; all four touch only their own river at both ends. With the proposed rule Aspen goes from 71 groups to 69 and Douglas stays at 35. The set of drawn segments, every drawn coordinate and every total length are unchanged. Codex reproduced this independently and found no foreign neighbour, ambiguous end or cycle.

**Options.** A: keep the rule; Hunter and Galena stay two groups each. B: same-`gnis_id` connectors count for connectivity only. C: also use unnamed connectors, or canals and pipelines carrying the id.

**Trade-offs.** B fits owner decision O2 on all four conditions (same identity, source topology, no branch absorbed, nothing invented). C does not: an unnamed connector has no identity, and canals and pipelines are a different kind of feature.

**Recommendation.** B, matching the owner's leaning. Bear case: the evidence is four connectors. The safety does not depend on the sample: segments are partitioned by `gnis_id` first, and a connector is never drawn and cannot pass drawn status to a centre line.

**Code and data impact.** One sentence in specification 8.3 and a new invariant G11 (the drawn set is identical with and without connector participation). The exact wording is in [connectors.md](connectors.md). The group IDs `nhd-gnis-00180061-p2` and `nhd-gnis-00180317-p2` never come into existence. No canonical data change.

**Tests required.** Ten fixtures listed in [connectors.md](connectors.md): three positive (including Hunter and Galena as exactly one group each on real data) and seven negative (empty-id connector, connector touching another river, canal and pipeline with the river's id, no drawn status through a connector, name mismatch fails the build, and G11 on both regions).

**Trust impact.** None on what is shown or claimed. Identity only.

**Approval line.** Choose A, B or C.

---

## 3. Granite Creek and extent-edge handling

**Question.** Should a river that leaves and re-enters the region stay split into separate same-named groups?

**Evidence.** Granite Creek in Aspen becomes three groups (five short drawn lines, 1.58 km drawn in total) because about three quarters of the creek lies outside the extent. It is the only displayed river in either region split this way, apart from the South Platte. One of its source segments (`nhd-165831253`) is itself cut into several lines by the clip. A read-only prototype showed that fetching 250 m beyond the Aspen extent would make it one group.

**Does the item 1 padding fix it?** No. Item 1 pads Douglas only. Granite Creek is in Aspen, which already has 0.005° water padding. Fixing it needs a separate Aspen fetch.

**Options.** A: accept the split and write down the clipped-segment rule. B: fetch a 250 m ring beyond the extent for connectivity only. C: treat parts whose free ends are on the edge as one group without fetching.

**Trade-offs.** B needs another live fetch, a contract change and new hidden-feature rules, and the Aspen hydrology layer also feeds setback screening, so ring segments would have to be kept out of that. C infers continuity the data cannot show, which O2 forbids.

**Recommendation.** A, matching the owner's leaning. Bear case: three entries named Granite Creek at the north-east corner may look like an error on the phone; B remains available later.

**Code and data impact.** One paragraph in specification 8.3 (exact wording in [extent-edge.md](extent-edge.md)), including the clarification that one source segment cut into several lines stays one member. The grouping report gains a count of drawn lines per group. No group, ID or drawn line changes.

**Tests required.** Two reaches with facing ends on the edge and nothing held between them give two groups; one clipped multi-line source segment is one member with no invented coordinate; two segments 1 m apart on the edge are not joined; Granite Creek is exactly three groups on real data.

**Trust impact.** None. Splitting is the conservative reading.

**Approval line.** Choose A, B or C.

---

## 4. The 2 ha threshold

**Question.** Confirm 2 ha for unnamed perennial waterbodies, or change it?

**Evidence.** At 2 ha Aspen shows 46 waterbodies (43 named, 3 unnamed) and Douglas 32 (18 named, 14 unnamed). At 0.5 ha Aspen would show 90 and Douglas 127: 44 and 95 more, all unnamed perennial lakes or ponds. Codex's counts match the original comparison exactly. By derived screens only (distance to a mapped Forest Service trail, wilderness, land class), 24 Aspen and 2 Douglas of the additions look possibly relevant; 93 of the 95 Douglas additions are on private land with no mapped trail within 1 km. These screens are not evidence of recreation or access.

**Corrections made on 2026-10-07.** The comparison report labelled elevations in feet when the values are metres, and said no Aspen feature in the 0.5 to 2 ha range was above 10,000 ft. One is: `nhd-65879795`, 1.4 ha, 3,693 m (12,116 ft). The report is corrected. Only 2 of the 44 Aspen features carry any elevation, so elevation still cannot pick out alpine lakes. Separately, the threshold packet says areas are stored at 0.1 ha precision; Codex found 17 Aspen and 14 Douglas waterbodies with finer values, so the build must compare exact stored areas. Neither correction changes a count or the recommendation.

**Options.** A: keep 2 ha. B: 0.5 ha. C1: 1.0 ha (adds 10 Aspen and 24 Douglas). C3: 2 ha plus a reviewed inclusion list for specific small perennial lakes, which is a new rule.

**Trade-offs.** Bytes do not decide this (0.5 ha adds under 110 KB per region). The real cost of lowering is many unlabelled shapes, mostly Douglas private-land ponds. The real cost of 2 ha is that some small Aspen high-country lakes are absent.

**Recommendation.** A, matching the owner's leaning. Bear case: one unnamed 1.4 ha lake at 12,116 ft is the kind of water a hiker looks for, and it will not be shown. If that matters after the iPhone check, C3 is the narrow fix and needs its own approval.

**Code and data impact.** None for A; D4 is recorded as confirmed.

**Tests required.** The builder and validator read the same value; areas exactly at the threshold are included; values just below are not; named and excluded categories are unaffected.

**Trust impact.** None. An absent unnamed pond makes no claim.

**Approval line.** Choose A, B, C1 or C3. The specification's own gate still applies: the owner reads the selection report and confirms before M4-B merges.

---

## 5. Layer titles

**Question.** What are the two water layer titles, identical in both regions?

**Evidence.** Today the titles are `Named water` (Aspen, one layer), `Named lakes & reservoirs` and `Named streams` (Douglas). After M4-B both regions have the same two layers and selection is no longer by name, so "Named" is wrong. The approved type labels in the detail are `River or stream`, `Lake or pond` and `Reservoir`.

**Options.** A: `Rivers and streams` and `Lakes and reservoirs`. B: `Rivers & streams` and `Lakes & reservoirs`.

**Trade-offs.** A matches the approved limitation sentence, which already says "Rivers, streams, lakes and reservoirs". B is two characters shorter per row in the layer drawer.

**Recommendation.** A, matching the owner's leaning. Bear case: the second layer also holds ponds, which the title does not name; the detail's type line does.

**Code and data impact.** Two strings in each region's `explore.json`.

**Tests required.** Literal comparison in both regions; the existing wording check (no "verified", "legal", "permitted", "open to").

**Trust impact.** Low. The titles state physical type only.

**Approval line.** Choose A or B, or give exact strings.

---

## 6. Source-scope wording

**Question.** What do the two `sources.usgs_nhd.scope` sentences say from M4-B?

**Evidence.** M4-A kept both sentences byte-identical and pinned them. The Aspen sentence now says "Feature type, flow permanence and size are not carried", which is untrue since M4-A. The Douglas sentence says "Named waterbodies and flowlines only, selected by name", which is untrue for waterbodies since M4-A and for selection from M4-B. Neither overclaims anything about access.

**Options.** The exact sentences for A and B are in [source-scope-wording.md](source-scope-wording.md).

- A: new sentences that name the dataset, say it was retired in 2023, say what is stored, and say the source does not establish recreation, access, permission or present-day flow.
- B: delete only the untrue clause from each current sentence.
- C: leave both through M4.

**If item 1 is approved**, the Douglas sentence under A needs one more clause. Proposed Douglas text for A in that case:

`USGS National Hydrography Dataset, retired by USGS in 2023 and no longer maintained. Named flowlines and all waterbodies with the source's type and hydrographic category, kept to about 500 m beyond the county line; not complete hydrology. The source does not establish recreation, access or permission, or present-day flow.`

**Trade-offs.** A is the most honest and mentions that the dataset is retired, which may read as alarming. B is shorter and silent on that. C keeps a false sentence on screen.

**Recommendation.** A, with the padded Douglas text if item 1 is D1. Bear case: "retired … no longer maintained" on a sources dialog may reduce confidence in data that is still the best available.

**Code and data impact.** Two strings in two manifests; the M4-A pin test is updated to the new literals.

**Tests required.** Literal comparison of both sentences; the wording check.

**Trust impact.** High: this is trust text. Only the owner's exact wording ships.

**Approval line.** Choose A, B or C, or supply exact sentences.

---

## 7. Grouped river length

**Question.** Which length does a grouped river show, and which length do the build's ordering and checks use?

**Evidence.** The specification (8.4) says a group's `length_km` is the sum of its members' source `length_km`. The source value is the unclipped segment length. Summed, it overstates any river cut by the extent: Granite Creek is 5.4 km by source sum and 1.6 km as drawn; all Aspen drawn members total 534.4 km by source and 514.5 km by geometry; Douglas 431.1 against 428.8. The two can also disagree the other way (East Plum Creek: 53.6 by source, 53.4 by geometry). Three things use a length: the number shown under `Computed by Ohvernight`, the ordering of a river's parts (which decides which part gets the plain group ID), and the expected-major-rivers fraction.

**Options.**

| | Displayed length | Part ordering and expected-river fraction |
|---|---|---|
| A | Sum of source `length_km` (as specified) | Source sum |
| B | Geometric length of the group's drawn geometry | Geometric length |
| C | Both shown, labelled separately | Geometric length |

**Trade-offs.** A is what the specification says today but shows a length the user cannot see on the map, and for an edge river most of it is outside the region. B shows what is drawn and is a derived fact, which is what the `Computed by Ohvernight` heading already says. C is the most complete and adds a second number and a second label, which needs new approved wording.

**Recommendation.** B, matching the owner's leaning, with these definitions:

- Displayed length: the geodesic (WGS84) length of the group's drawn members, measured on the canonical geometry held in the region, in kilometres to one decimal, under `Computed by Ohvernight`.
- Part ordering (8.3 step 5): by drawn geometric length, longest first; the tie-break is unchanged.
- Expected-river fraction: per `gnis_id`, drawn geometric length divided by the geometric length of all its perennial stream and artificial-path segments held in the region, counting every group of that `gnis_id`.
- The source `length_km` stays on every canonical segment and is not shown for a group.

Bear case: a geometric length depends on the clip, so a river's displayed length changes if the extent changes (item 1 would change eleven Douglas rivers slightly). That is accurate, but it means the number is about the map, not about the river. If item 1 is approved, the South Platte's 73.3 km includes 64 km drawn outside the county line, all of it visible on the map.

**Code and data impact.** Specification 8.3 step 5, 8.3 "Wide rivers" and 8.4; rule R71 checks the computed value. `length_km` on a group display feature keeps its name and becomes the geometric value. No canonical change.

**Tests required.** A group whose source sum and geometric length differ shows the geometric one; a clipped edge river (Granite Creek) shows its drawn length; part ordering is stable under the new measure; the expected-river fraction for each listed river is computed with the stated denominator; R71 fails when the stored length is changed.

**Trust impact.** Positive. The number shown describes what is drawn and sits under the computed heading. No source length for hidden or out-of-region reaches is presented as the visible river's length.

**Approval line.** Choose A, B or C.

---

## Coordinator clarifications that need no owner decision

Recorded here so they are visible. The coordinator will write them into the specification as amendments when M4-B is dispatched, unless the owner objects.

- Section 23 estimates corrected to measured values: 71 Aspen and 35 Douglas stream groups before any decision above (not 62 and 56); Roaring Fork has 111 drawn members (not 96); waterbodies at 2 ha are 46 and 32 (not 42 and 37).
- The 80 m South Platte perennial segment named in 8.3 is 76 m long and lies outside the county.
- Seven Douglas streams are drawn as two lines because one segment of 7 to 85 m is coded intermittent (East Plum Creek: one 85 m segment in 54 km). The rule has no exception and none is proposed. Mentioned so it is not a surprise on the phone.
- Technical items Codex found that M4-B must handle and that change no approved behaviour: the manifest schema is closed and needs the new keys; the validator counts a canonical pointer twice when two display layers share it (the Aspen split); the Douglas Browse search path needs water added separately from the shell.

## What happens after the answers

1. The coordinator records the decisions and the wording in the specification as owner decisions, in a documentation pull request for the owner's approval.
2. If item 1 is D1, the request is made once by Codex under the same controls as the M4-A refresh, with a snapshot addendum.
3. Codex implements M4-B from the amended specification. The coordinator reviews independently. CI, three performance sessions and the owner's iPhone check of both regions gate the merge, as the specification already says.

Nothing in M4-B changes any activity, access or permission statement. Those belong to M4-C.
