# M4-B validation plan

Prepared by the coordinator before M4-B starts, to shorten design time. It
restates the approved specification
([M4-functional-recreational-water.md](../../../specs/M4-functional-recreational-water.md),
sections 8, 11, 13 and 15) as concrete cases. It adds no rule. Where this
file and the specification differ, the specification governs.

Fixture conventions: tiny hand-written FeatureCollections, coordinates to six
decimals, one `gnis_id` per stream unless the case says otherwise.
"Segment" means a canonical flowline feature. "Drawn" means its geometry is in
a display feature.

## 1. Eligibility (R69, R72)

| # | Fixture | Expected |
|---|---|---|
| E1 | Canal, `ftype` 336, named, `gnis_id` set | Not displayed; not a grouping candidate |
| E2 | Ditch, `ftype` 336 `fcode` 33600, same `gnis_id` as a perennial stream and touching it | Not displayed; not used for connectivity; the stream's group is unaffected |
| E3 | Pipeline, `ftype` 428 | Not displayed |
| E4 | Connector, `ftype` 334, named | Not displayed; never a drawn member |
| E5 | Stream `46006` with empty `gnis_id` and empty name | Not displayed |
| E6 | Stream `46006` with a name and empty `gnis_id` | Not displayed (no group can be formed); listed in the selection report |
| E7 | Stream `46003` (intermittent), named | Not displayed; stays in canonical data |
| E8 | Stream `46007` (ephemeral), named | Not displayed |
| E9 | Stream `46000` (category unknown), named | Not displayed |
| E10 | Stream `46006`, named, `gnis_id` set | Displayed as a group |
| E11 | Lake `39004`, named, 0.001 km² | Displayed (named perennial: any size) |
| E12 | Lake `39004`, unnamed, 0.0200 km² | Displayed (at the threshold) |
| E13 | Lake `39004`, unnamed, 0.0199 km² | Not displayed |
| E14 | Lake `39004`, unnamed, `area_sqkm` null | Not displayed; listed in the report |
| E15 | Lake `39001` (intermittent), named, 0.5 km² | Not displayed |
| E16 | Lake `39000` (category unknown), named | Not displayed |
| E17 | Reservoir `43619`, named | Displayed; `hydro_category` `unknown`; never described as perennial |
| E18 | Reservoir `43600`, unnamed, 0.03 km² | Displayed |
| E19 | Reservoir `43600`, unnamed, 0.01 km² | Not displayed |
| E20 | Reservoir `43614` (water storage, intermittent), named | Not displayed |
| E21 | Reservoir `43624` (treatment), named, 1 km² | Not displayed |
| E22 | Each remaining ineligible reservoir code: 43601, 43603–43612, 43623, 43625, 43626 | Not displayed |
| E23 | Each eligible reservoir code: 43600, 43613, 43615, 43617, 43618, 43619, 43621 | Displayed when named |
| E24 | Swamp or marsh `466`, named | Not displayed |
| E25 | Aspen area-layer feature (`source_layer` `area`) | Not displayed |
| E26 | Display artifact contains one feature the rule excludes (mutation) | R69 and R72 fail |
| E27 | Display artifact omits one feature the rule includes (mutation) | R69 fails |
| E28 | Threshold changed in the artifact but not in `water_display.json` (mutation) | R69 fails |

## 2. Reviewed lists (R73)

| # | Fixture | Expected |
|---|---|---|
| X1 | Exclusion for one eligible lake, complete evidence | That lake is not displayed; every other feature unchanged; canonical data unchanged |
| X2 | Exclusion whose `feature_id` is a stream group ID | The whole group is not displayed |
| X3 | Exclusion with an unknown `feature_id` | R73 fails |
| X4 | Exclusion with a reason code outside the set | R73 fails |
| X5 | Exclusion with empty `statement`, or no `source_url`, or a non-HTTP URL | R73 fails |
| X6 | Exclusion whose `source_url` host is in `non_claim_hosts` (a community site) | R73 fails |
| X7 | Exclusion with complete evidence, but the feature is still in the display artifact (mutation) | R73 fails |
| X8 | Inclusion for a named intermittent lake, complete evidence | Displayed |
| X9 | Inclusion with reason code other than `reviewed_intermittent_waterbody` | R73 fails |
| X10 | Inclusion for a canal | R73 fails: inclusions apply to waterbodies only |
| X11 | A record whose `statement` only restates the feature's name | Cannot be machine-checked; reviewer checklist item. The validator does require a non-empty statement and a source URL |
| X12 | `reviewed_at` not RFC 3339 | R73 fails |

## 3. Grouping (R70, R71; invariants G1–G10)

| # | Fixture | Expected |
|---|---|---|
| G-a | Three perennial segments, one `gnis_id`, end to end | One group `nhd-gnis-<id>`, `member_count` 3, one MultiLineString of three lines in member-ID order |
| G-b | Two sets of perennial segments, same `gnis_id`, 5 km apart, nothing between | Two groups: `nhd-gnis-<id>` (longer) and `nhd-gnis-<id>-p2`; reported as multi-part |
| G-c | Two perennial reaches joined by an intermittent segment of the same `gnis_id` | One group; geometry is two separate lines; the intermittent segment is not drawn and has `group_id` null; no coordinate lies in the gap (G9) |
| G-d | Two perennial reaches joined only by a segment with a different `gnis_id` | Two groups (no joining through another river) |
| G-e | Two streams with different `gnis_id` values meeting end to end | Two groups, never merged (G5) |
| G-f | Two streams with the same name and different `gnis_id` | Two groups with the same `name` |
| G-g | One `gnis_id` carrying two different names | Build fails and reports both segments (G2) |
| G-h | Perennial segments either side of a lake, artificial paths through the lake with the same `gnis_id` | One group; artificial paths drawn; `member_count` includes them |
| G-i | Artificial path with the group's `gnis_id`, separated from every perennial segment by an intermittent segment | Not drawn |
| G-j | A `gnis_id` with artificial paths only | No group; listed in the wide-river report |
| G-k | Wide river: one short perennial segment then a long chain of artificial paths | One group; the chain is drawn; drawn fraction reported |
| G-l | Supporting unnamed bridge (`support_for` set) between two named parts | One group; the bridge is not drawn, has no `group_id`, is not a display feature (G10) |
| G-m | Unnamed feature near a gap that does not touch both sides | Not kept as support; two groups |
| G-n | Segment listed under two groups in `water_groups` (mutation) | R70 fails (G4) |
| G-o | A member moved to another group in `water_groups` (mutation) | R70 fails (G7) |
| G-p | A member's line dropped from the group geometry (mutation) | R71 fails |
| G-q | A straight line added between two members (mutation) | R71 fails (G9) |
| G-r | `member_count` or `length_km` altered (mutation) | R71 fails |
| G-s | Canonical `group_id` set on a canal (mutation) | R70 fails (G6) |
| G-t | Rebuild from the same canonical data twice | Byte-identical artifacts and identical group IDs (reproducibility) |
| G-u | Member order shuffled in canonical input | Same group IDs and same display geometry (ordering by ID, not input order) |
| G-v | A group ID equal to some feature ID (constructed) | Validator rejects (7.2) |
| G-w | Expected major river absent | Build fails with the stop-and-report message |
| G-x | Expected major river drawn below its fraction | Build fails |
| G-y | Expected major river containing a member with another `gnis_id` (mutation) | Build fails |
| G-z | Branch: a named fork (own `gnis_id`) joining the main stem | Fork is its own group; main stem unaffected |

## 4. Identity and aliases (R68, carried from M4-A)

| # | Fixture | Expected |
|---|---|---|
| I1 | Every legacy ID of a grouped segment | Maps in `water-aliases.json` to the group ID |
| I2 | Every legacy ID of a displayed waterbody | Maps to its feature ID |
| I3 | Legacy ID of an undisplayed segment (intermittent, canal) | Absent from the alias file; present in canonical `legacy_ids` |
| I4 | Alias pointing at a group that does not contain that segment (mutation) | R68 fails |
| I5 | `water_groups` member list vs canonical `group_id` | Equal as sets, ordered by ID |

## 5. Display content and wording

| # | Case | Expected |
|---|---|---|
| D1 | Grouped stream detail | "From the source": `River or stream`, `Perennial`, `<n> source segments`, agency, source link, fetched date, the approved limitation sentence. "Computed by Ohvernight": length in km. Then WW1. Last line WW2 |
| D2 | Named perennial lake | `Lake or pond`, `Perennial`; area in hectares under "Computed by Ohvernight" |
| D3 | Reservoir with unknown category | `Reservoir`, WW16, and no `Perennial` |
| D4 | Unnamed lake | Title WW14 |
| D5 | Unnamed reservoir | Title WW15 |
| D6 | Any water, M4-B | No activity label, no status word, no WW8 section (those are M4-C) |
| D7 | Every WW string and label | Equal to the literal in the specification, byte for byte |
| D8 | Limitation sentence | Identical in both manifests and equal to the approved literal |
| D9 | No string contains "verified", "legal", "permitted" or "open to" | M3 A4 inventory test still green |

## 6. Interaction (uses M3 selection unchanged)

| # | Case | Expected |
|---|---|---|
| U1 | Tap a stream on one member line | Whole group selected: casing and thicker stroke on every line; one label; detail at the partial height |
| U2 | Tap the same stream on a different member line | Same group ID selected |
| U3 | Tap the stream's label | Same group ID |
| U4 | Short stream, map tap | Fits exactly as an M3 line |
| U5 | Very long river, map tap, where fitting needs more than two zoom levels out | No fit; zoom unchanged; tapped point stays in view above the sheet |
| U6 | Very long river selected from search | Map moves to it; zoom not below `list.min_zoom` |
| U7 | Trail selection | Unchanged from M3 (no fit policy on trails) |
| U8 | Tap a lake | Selected with the stronger fill; centre and zoom unchanged; zero fit calls |
| U9 | Tap where a stream crosses a lake | Line wins over polygon (M3 priority) |
| U10 | Empty-map tap with a stream selected | Selection and camera unchanged (A14) |
| U11 | Water names in search | Selecting one selects the group or waterbody |
| U12 | No canal or ditch in the rendered water layer | Asserted from `water_class`, not from names |

## 7. Budgets

| # | Check | Limit |
|---|---|---|
| B1 | Aspen water display artifacts, total bytes | ≤ 1,134,855 |
| B2 | Douglas water display artifacts, total bytes | ≤ 1,887,725 |
| B3 | Bytes to map usable, each region | ≤ 500,000 |
| B4 | Default-on total, each region | ≤ 4,500,000 |
| B5 | Alias and group maps | Not requested during load |
| B6 | Three performance sessions, unchanged `measure.mjs` | A10 limits; a miss is reported |

## 8. Mutation proofs (local, not committed)

1. Change one `fcode` in canonical data → R67.
2. Add a canal to a display artifact → R69, R72.
3. Remove an eligible lake from a display artifact → R69.
4. Move a segment between groups in `water_groups` → R70.
5. Drop a member line from a group geometry → R71.
6. Insert a connecting line between two parts → R71 (G9).
7. Give two segments of one `gnis_id` different names → build stop (G2).
8. Lower the threshold in the artifact only → R69.
9. Add an exclusion with no evidence → R73.
10. Leave an excluded feature in the artifact → R73.
11. Remove an expected major river's longest reach → build stop.
12. Point an alias at the wrong group → R68.

## 9. Stable rule IDs used

R68 (aliases to group IDs), R69, R70, R71, R72, R73; R61–R63 as amended for
grouped layers; R64 and R65 unchanged. R74 and R76 belong to M4-C.
