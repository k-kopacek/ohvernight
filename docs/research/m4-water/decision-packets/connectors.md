# Connector owner decision packet

Hunter Creek and Galena Creek in Aspen are each shown as two rivers only because the short source segment that joins their two reaches is coded as a "connector", which the approved rule ignores. **Recommendation: approve Option B — a connector that carries the river's own `gnis_id` may be used to establish continuity for that river only, and is never drawn.** On today's data this merges exactly those two rivers (Aspen 71 groups become 69), changes no drawn line anywhere, and every adversarial check below came back empty.

## DECISION

May a connector segment that carries a non-empty `gnis_id` take part in connectivity for that same `gnis_id` only (never drawn, never selectable, never joining a different `gnis_id`)? Yes or no.

## EVIDENCE

Read-only dry run on the M4-A canonical data (commit `aa5c20b`), both regions, local data only.

**Counts.**

| Region | Connectors | With a `gnis_id` | Without | Total length |
|---|---:|---:|---:|---:|
| Aspen (all flowlines are held) | 65 | 3 | 62 | 1.99 km |
| Douglas County (named flowlines only are held) | 1 | 1 | 0 | 0.05 km |

Douglas cannot contain an unnamed connector: unnamed flowlines were not fetched there (owner decision O1).

**The four connectors that carry a `gnis_id`.** Length is measured from the stored geometry. Every one has both end points on segments of its own `gnis_id` and on nothing else.

| Region | id | Name | `gnis_id` | km | Touches at one end | Touches at the other end |
|---|---|---|---|---:|---|---|
| Aspen | `nhd-165836028` | Hunter Creek | 00180061 | 0.019 | Hunter Creek 00180061 stream (perennial) | Hunter Creek 00180061 stream (perennial) |
| Aspen | `nhd-165836035` | Wildcat Creek | 00179702 | 0.023 | Wildcat Creek 00179702 stream (intermittent) | Wildcat Creek 00179702 stream (intermittent) |
| Aspen | `nhd-72975294` | Galena Creek | 00180317 | 0.139 | Galena Creek 00180317 stream (perennial) | Galena Creek 00180317 artificial_path (unknown) |
| Douglas | `nhd-120648577` | Kinney Creek | 00185092 | 0.050 | Kinney Creek 00185092 artificial_path (unknown) | Kinney Creek 00185092 stream (intermittent) |

**Result of the proposed rule against the approved rule.**

| `gnis_id` | River | Region | Groups before | Groups after | Drawn segments before / after | Drawn km before / after (source attribute) | Drawn km before / after (geometry) |
|---|---|---|---:|---:|---|---|---|
| 00180061 | Hunter Creek | Aspen | 2 (24.01 km and 1.01 km, 19 m apart) | 1 | 58 / 58 | 25.03 / 25.03 | 25.07 / 25.07 |
| 00180317 | Galena Creek | Aspen | 2 (1.97 km and 1.57 km, 139 m apart) | 1 | 10 / 10 | 3.54 / 3.54 | 3.54 / 3.54 |
| 00179702 | Wildcat Creek | Aspen | 0 (not displayed: intermittent) | 0 | 0 / 0 | 0 / 0 | 0 / 0 |
| 00185092 | Kinney Creek | Douglas | 0 (not displayed: no perennial segment) | 0 | 0 / 0 | 0 / 0 | 0 / 0 |

Wildcat Creek and Kinney Creek change only internally (two hidden parts become one hidden part); nothing a user sees changes.

| Region | Groups before | Groups after | Drawn segments | Drawn km (attribute) | Drawn km (geometry) |
|---|---:|---:|---|---|---|
| Aspen | 71 | 69 | 1,273 before and after, identical set of ids | 534.41 both | 514.39 both |
| Douglas County | 35 | 35 | 1,608 before and after, identical set of ids | 431.06 both | 428.77 both |

Nothing else changes: every other `gnis_id` has the same groups with the same members. No connector is drawn under either rule.

**Is each connector between two parts, or on one side only?** All four are source-topologically *between* two parts of the same `gnis_id`: removing the connector splits the river into exactly two pieces, one at each end. For Hunter Creek and Galena Creek both pieces are displayed; for Wildcat Creek and Kinney Creek neither is. No same-`gnis_id` connector hangs off one side only.

**Adversarial checks.**

| Check | Result |
|---|---|
| (a) Does any same-`gnis_id` connector also touch a segment of a different `gnis_id`, or an unnamed segment? | No. 0 of 4. Each end touches only its own river. No branch can be absorbed. |
| (b) Are there unnamed connectors lying between two parts of one `gnis_id`? | No. 0 of 62. Only one unnamed connector touches a named stream at all: `nhd-72964444` (347 m), Lime Creek at one end and an unnamed intermittent stream at the other. |
| (b) What would a rule that also used unnamed connectors join? | Tested two ways: within one `gnis_id`, and across any `gnis_id`. Both cause 0 group merges on today's data, so none across different names. It is still unsafe in principle: an unnamed connector has no identity, 39 of the 62 touch a canal or ditch at one end (20 of them a named ditch), and the rest join unnamed streams. It would add nothing now and could join a river to a ditch crossing in another region. |
| (c) Does using same-`gnis_id` connectors make a group whose drawn pieces are far apart? | No. The longest undrawn connector used is 139 m (Galena Creek); Hunter Creek's is 19 m; the two hidden ones are 23 m and 50 m. |
| (d) Canals/ditches and pipelines that carry a `gnis_id` | Aspen: 103 canal or ditch segments and 11 pipeline segments carry a `gnis_id`. Douglas: 73 and 12. **None carries the `gnis_id` of any displayed river.** Where the id is shared with stream or centre-line segments (Aspen 37 canal segments over 5 ids, 5 pipeline segments over 3 ids; Douglas 32 canal segments over 2 ids, 3 pipeline segments over 1 id) the id belongs to a ditch, canal or tunnel itself: Salvation Ditch, Elk Creek Ditch, New York Collection Canal, Lincoln Gulch Connection Canal, the two Twin Lakes tunnels, Arapahoe Canal, Pleasant Park Ditch. None has a displayed group. |
| (d) What if they too were used for connectivity? | Tested: 0 displayed groups change in either region. They should still not be used. They are engineered conveyances, not river reaches (the Twin Lakes Tunnel Number 1 pipeline segments total 6.2 km), the specification already says they are never candidates, and using them buys nothing. |

**Every unnamed connector (Aspen, 62).** None has a `gnis_id`; none is used by the proposed rule.

| id | Name | `gnis_id` | km | Touches at one end | Touches at the other end |
|---|---|---|---:|---|---|
| `nhd-133017832` | (none) | (none) | 0.027 | unnamed no id stream (perennial) | unnamed no id stream (perennial) |
| `nhd-165826052` | (none) | (none) | 0.025 | Powell Mc Kenzie Ditch 00180008 canal_ditch (unknown); unnamed no id stream (intermittent) | unnamed no id stream (intermittent) |
| `nhd-165826053` | (none) | (none) | 0.010 | unnamed no id canal_ditch (unknown); unnamed no id stream (intermittent) | unnamed no id stream (intermittent) |
| `nhd-165826619` | (none) | (none) | 0.010 | Elk Creek Ditch Number 2 00169493 canal_ditch (unknown); unnamed no id stream (ephemeral) | unnamed no id stream (intermittent) |
| `nhd-165826620` | (none) | (none) | 0.012 | Elk Creek Ditch Number 2 00169493 canal_ditch (unknown); unnamed no id stream (ephemeral) | unnamed no id stream (intermittent) |
| `nhd-165830087` | (none) | (none) | 0.022 | unnamed no id canal_ditch (unknown); unnamed no id stream (intermittent) | unnamed no id stream (intermittent) |
| `nhd-165830088` | (none) | (none) | 0.026 | unnamed no id canal_ditch (unknown); unnamed no id stream (intermittent) | unnamed no id stream (intermittent) |
| `nhd-165830204` | (none) | (none) | 0.027 | unnamed no id stream (intermittent) | unnamed no id stream (intermittent) |
| `nhd-165830208` | (none) | (none) | 0.014 | unnamed no id stream (intermittent) | unnamed no id stream (intermittent) |
| `nhd-165830209` | (none) | (none) | 0.032 | unnamed no id stream (intermittent) | unnamed no id stream (intermittent) |
| `nhd-165830210` | (none) | (none) | 0.014 | unnamed no id stream (ephemeral) | unnamed no id stream (intermittent) |
| `nhd-165830212` | (none) | (none) | 0.011 | Red Mountain Ditch 00180037 canal_ditch (unknown); unnamed no id stream (intermittent) | unnamed no id stream (intermittent) |
| `nhd-165830213` | (none) | (none) | 0.031 | unnamed no id stream (intermittent) | unnamed no id stream (intermittent) |
| `nhd-165833322` | (none) | (none) | 0.013 | unnamed no id canal_ditch (unknown); unnamed no id stream (intermittent) | unnamed no id stream (intermittent) |
| `nhd-165833323` | (none) | (none) | 0.012 | unnamed no id canal_ditch (unknown); unnamed no id stream (intermittent) | unnamed no id stream (intermittent) |
| `nhd-165833591` | (none) | (none) | 0.029 | Brush Creek Ditch 00179703 canal_ditch (unknown); unnamed no id stream (intermittent) | unnamed no id stream (intermittent) |
| `nhd-165833695` | (none) | (none) | 0.011 | unnamed no id canal_ditch (unknown); unnamed no id stream (intermittent) | unnamed no id stream (intermittent) |
| `nhd-165835996` | (none) | (none) | 0.032 | unnamed no id stream (intermittent) | unnamed no id stream (intermittent) |
| `nhd-165835997` | (none) | (none) | 0.040 | unnamed no id canal_ditch (unknown); unnamed no id stream (intermittent) | unnamed no id stream (intermittent) |
| `nhd-165835998` | (none) | (none) | 0.012 | Red Mountain Ditch 00180037 canal_ditch (unknown); unnamed no id stream (intermittent) | unnamed no id stream (intermittent) |
| `nhd-165835999` | (none) | (none) | 0.029 | unnamed no id stream (intermittent) | unnamed no id stream (intermittent) |
| `nhd-165836000` | (none) | (none) | 0.023 | unnamed no id stream (intermittent) | unnamed no id stream (intermittent) |
| `nhd-165836001` | (none) | (none) | 0.027 | unnamed no id stream (intermittent) | unnamed no id stream (intermittent) |
| `nhd-165836002` | (none) | (none) | 0.019 | unnamed no id canal_ditch (unknown); unnamed no id stream (intermittent) | unnamed no id stream (intermittent) |
| `nhd-165836003` | (none) | (none) | 0.025 | Red Mountain Ditch 00180037 canal_ditch (unknown); unnamed no id stream (intermittent) | unnamed no id stream (intermittent) |
| `nhd-165836004` | (none) | (none) | 0.023 | unnamed no id canal_ditch (unknown); unnamed no id stream (intermittent) | unnamed no id stream (intermittent) |
| `nhd-165836005` | (none) | (none) | 0.034 | unnamed no id stream (intermittent) | unnamed no id stream (intermittent) |
| `nhd-165836006` | (none) | (none) | 0.028 | Red Mountain Ditch 00180037 canal_ditch (unknown); unnamed no id stream (intermittent) | unnamed no id stream (intermittent) |
| `nhd-165836007` | (none) | (none) | 0.029 | unnamed no id canal_ditch (unknown); unnamed no id stream (intermittent) | unnamed no id stream (intermittent) |
| `nhd-165836008` | (none) | (none) | 0.029 | Red Mountain Ditch 00180037 canal_ditch (unknown); unnamed no id stream (intermittent) | unnamed no id stream (intermittent) |
| `nhd-165836009` | (none) | (none) | 0.022 | unnamed no id canal_ditch (unknown); unnamed no id stream (intermittent) | unnamed no id stream (intermittent) |
| `nhd-165836010` | (none) | (none) | 0.034 | Red Mountain Ditch 00180037 canal_ditch (unknown); unnamed no id stream (intermittent) | unnamed no id stream (intermittent) |
| `nhd-165836011` | (none) | (none) | 0.035 | unnamed no id canal_ditch (unknown); unnamed no id stream (intermittent) | unnamed no id stream (intermittent) |
| `nhd-165836012` | (none) | (none) | 0.027 | unnamed no id stream (intermittent) | unnamed no id stream (intermittent) |
| `nhd-165836013` | (none) | (none) | 0.023 | unnamed no id stream (intermittent) | unnamed no id stream (intermittent) |
| `nhd-165836014` | (none) | (none) | 0.022 | unnamed no id stream (intermittent) | unnamed no id stream (intermittent) |
| `nhd-165836015` | (none) | (none) | 0.036 | unnamed no id canal_ditch (unknown); unnamed no id stream (intermittent) | unnamed no id stream (intermittent) |
| `nhd-165836016` | (none) | (none) | 0.020 | Red Mountain Ditch 00180037 canal_ditch (unknown); unnamed no id stream (intermittent) | unnamed no id stream (intermittent) |
| `nhd-165836017` | (none) | (none) | 0.027 | unnamed no id canal_ditch (unknown); unnamed no id stream (intermittent) | unnamed no id stream (intermittent) |
| `nhd-165836018` | (none) | (none) | 0.032 | unnamed no id stream (intermittent) | unnamed no id stream (intermittent) |
| `nhd-165836019` | (none) | (none) | 0.022 | Red Mountain Ditch 00180037 canal_ditch (unknown); unnamed no id canal_ditch (unknown); unnamed no id stream (intermittent) | unnamed no id stream (intermittent) |
| `nhd-165836020` | (none) | (none) | 0.022 | unnamed no id canal_ditch (unknown); unnamed no id stream (intermittent) | unnamed no id stream (intermittent) |
| `nhd-165836021` | (none) | (none) | 0.030 | Red Mountain Ditch 00180037 canal_ditch (unknown); unnamed no id stream (intermittent) | unnamed no id stream (intermittent) |
| `nhd-165836022` | (none) | (none) | 0.028 | Red Mountain Ditch 00180037 canal_ditch (unknown); unnamed no id stream (intermittent) | unnamed no id stream (intermittent) |
| `nhd-165836023` | (none) | (none) | 0.043 | unnamed no id stream (intermittent) | unnamed no id stream (intermittent) |
| `nhd-165836024` | (none) | (none) | 0.023 | unnamed no id canal_ditch (unknown); unnamed no id stream (intermittent) | unnamed no id stream (intermittent) |
| `nhd-165836025` | (none) | (none) | 0.029 | unnamed no id stream (intermittent) | unnamed no id stream (intermittent) |
| `nhd-165836026` | (none) | (none) | 0.019 | unnamed no id stream (intermittent) | unnamed no id stream (intermittent) |
| `nhd-165836027` | (none) | (none) | 0.018 | unnamed no id stream (intermittent) | unnamed no id stream (intermittent) |
| `nhd-165836029` | (none) | (none) | 0.035 | unnamed no id canal_ditch (unknown); unnamed no id stream (ephemeral); unnamed no id stream (intermittent) | unnamed no id stream (intermittent) |
| `nhd-165836030` | (none) | (none) | 0.016 | Lemond Ditch 00180015 canal_ditch (unknown); unnamed no id stream (intermittent) | unnamed no id stream (intermittent) |
| `nhd-165836031` | (none) | (none) | 0.013 | Lemond Ditch 00180015 canal_ditch (unknown); unnamed no id stream (intermittent) | unnamed no id stream (intermittent) |
| `nhd-165836034` | (none) | (none) | 0.013 | unnamed no id stream (intermittent) | unnamed no id stream (intermittent) |
| `nhd-165836036` | (none) | (none) | 0.021 | unnamed no id stream (intermittent) | unnamed no id stream (intermittent) |
| `nhd-165836037` | (none) | (none) | 0.026 | McKenzie Wildcat Ditch 00180010 canal_ditch (unknown); unnamed no id stream (intermittent) | unnamed no id stream (intermittent) |
| `nhd-165836038` | (none) | (none) | 0.027 | McKenzie Wildcat Ditch 00180010 canal_ditch (unknown); unnamed no id stream (intermittent) | unnamed no id stream (intermittent) |
| `nhd-165836039` | (none) | (none) | 0.017 | McKenzie Wildcat Ditch 00180010 canal_ditch (unknown); unnamed no id stream (intermittent) | unnamed no id stream (intermittent) |
| `nhd-165836040` | (none) | (none) | 0.018 | McKenzie Wildcat Ditch 00180010 canal_ditch (unknown); unnamed no id stream (intermittent) | unnamed no id stream (intermittent) |
| `nhd-165836041` | (none) | (none) | 0.055 | unnamed no id canal_ditch (unknown); unnamed no id stream (intermittent) | unnamed no id stream (intermittent) |
| `nhd-165836042` | (none) | (none) | 0.015 | unnamed no id canal_ditch (unknown); unnamed no id stream (intermittent) | unnamed no id stream (intermittent) |
| `nhd-72964444` | (none) | (none) | 0.347 | unnamed no id stream (intermittent) | Lime Creek 00175029 stream (perennial) |
| `nhd-72981554` | (none) | (none) | 0.017 | unnamed no id artificial_path (unknown) | unnamed no id artificial_path (unknown) |

## CURRENT BEHAVIOR

Specification 8.3: "A connector is a candidate only as a supporting feature." Supporting features exist only for Douglas (unnamed bridges, O1) and none was needed. So a connector never links anything today. Hunter Creek, which is on the expected-major-rivers list, appears as two tappable rivers 19 m apart (ids `nhd-gnis-00180061` and `nhd-gnis-00180061-p2`); Galena Creek as two, 139 m apart.

## OPTION A

Keep the approved rule. Hunter Creek and Galena Creek stay two groups each. Nothing to change. The Hunter Creek expected-river check must then be defined per `gnis_id` across groups, or its main group passes at 0.96.

## OPTION B

Use a connector for connectivity when, and only when, it carries the same non-empty `gnis_id` as the segments it joins. Never drawn, never selectable. Hunter Creek and Galena Creek become one group each. Recommended.

## OPTION C

Wider: also use unnamed connectors, or canals and pipelines that carry the id (the wider wording floated in open question Q2, "connector or other non-drawn flowline"). Same visible result as B today; adds classes with no identity or of a different nature. Not recommended.

## TRADEOFFS

| | A | B | C |
|---|---|---|---|
| Hunter Creek, Galena Creek | two groups each | one group each | one group each |
| Drawn lines | unchanged | unchanged | unchanged |
| Rule text | none | one sentence, one invariant | wider wording, harder to test |
| Fits O2 (same identity, source topology, no branch absorbed, nothing invented) | yes | yes, all four conditions met by construction | not for unnamed connectors (no identity) |

## RISKS

- A future region could contain a long same-`gnis_id` connector (for example under a dam or through a culvert), giving one group with a long undrawn gap. This is the same situation as a hidden intermittent reach, which O2 already accepts. Mitigation: the grouping report lists every connector used and its length.
- A source naming error could put a river's `gnis_id` on the wrong connector. It could then only link two reaches that already carry that same id and physically touch it, so a different river cannot be absorbed.
- Uncertainty: the evidence is two regions and four connectors. The safety argument does not depend on the sample: partitioning by `gnis_id` happens first, and connectors are never drawn and never pass "drawn" status to a centre line.

## RECOMMENDATION

Approve Option B. It generalises safely because of three properties that hold by construction, not by luck of the data: it cannot cross `gnis_id` values (G5 is untouched), it cannot change what is drawn, and it uses only a segment the source itself placed between the two reaches.

Exact wording for specification 8.3, replacing "A connector is a candidate only as a supporting feature":

> A connector segment (`water_class` `connector`) that carries a non-empty `gnis_id` is a connectivity-only candidate for that `gnis_id` and for no other. Within its own `gnis_id` it takes part in the adjacency of step 2 exactly as a non-perennial stream segment does. It is never drawn, never selectable, never labelled and never a display feature; it is not counted in `member_count` or `length_km`, does not make a part displayable, does not pass drawn status to an artificial path, and never has a `group_id`. It cannot connect segments of a different `gnis_id`. A connector with an empty `gnis_id` is used only as a supporting feature under section 5. Canals, ditches and pipelines are never candidates, whatever `gnis_id` they carry.

New invariant:

> G11. Connector participation never changes the set of drawn segments. The drawn members of a region computed with and without connectivity-only connectors are identical; only the assignment of drawn segments to groups of the same `gnis_id` may differ. Every connectivity-only connector has the same `gnis_id` and `name` as its group, and the grouping report lists each one with its length.

## WHAT CHANGES IF APPROVED

- Aspen stream groups: 71 become 69. The ids `nhd-gnis-00180061-p2` and `nhd-gnis-00180317-p2` no longer exist. Hunter Creek is one group of 58 drawn members (25.03 km); Galena Creek one group of 10 (3.54 km).
- One sentence and one invariant in specification 8.3; G6 and G10 wording extended to name connectivity-only connectors.
- The grouping report gains a list of connectors used (today: 2 displayed, 2 hidden).
- Hunter Creek passes the expected-major-rivers check as one group at 1.00.

## WHAT REMAINS UNCHANGED

- Every drawn line, in both regions (1,273 and 1,608 segments, same ids).
- Douglas groups (35).
- Canals, ditches, pipelines and unnamed connectors: still never used.
- Different `gnis_id` values are never merged; no geometry is invented; canonical data is untouched except `group_id`.
- The extent-edge question (Granite Creek) is separate; see the extent-edge packet.

## TESTS REQUIRED

Positive fixtures:
1. Two perennial reaches of one `gnis_id` joined end to end by a connector with the same `gnis_id`: one group; the connector is not in the display geometry, not in `water_groups`, has `group_id` null; `member_count` and `length_km` exclude it.
2. A perennial reach and an artificial path joined by a same-id connector (the Galena Creek shape): one group; the artificial path is drawn only if it was drawn without the connector.
3. Real data: Hunter Creek 00180061 and Galena Creek 00180317 are each exactly one group in Aspen.

Negative fixtures:
4. Connector with an empty `gnis_id` between two reaches of one river: two groups.
5. Connector carrying river X's id whose other end touches only river Y: X and Y stay separate; the connector joins nothing.
6. Connector with river X's id touching X at one end and both X and Y at the other: X is one group; Y is not a member.
7. Canal segment and pipeline segment carrying the river's `gnis_id` between two reaches: two groups.
8. Same-id connector between a perennial reach and a part that has only artificial paths: one part, but those artificial paths stay undrawn (no drawn status through a connector).
9. G11 as a build check on both regions: the drawn set with and without connector participation is identical.
10. A connector whose `name` differs from the group's name: the build fails under G2.

## ROLLBACK

Remove the sentence and G11 and rebuild the display artifacts from the unchanged canonical data. The two `-p2` group ids return. No canonical data, source fetch or contract change is involved, so rollback is one revert of the build rule and its fixtures.

## HOW THIS WAS COMPUTED

- Data: worktree `/Users/kylekopacek/orca/workspaces/Ohvernight/m4a-source-preservation` at commit `aa5c20b` (`v2/map-data-v2.json` `/layers/hydrology` flowlines; `v2/regions/douglas-co/research.json` `/layers/waterways`). Read only. No network.
- Scripts (outside every repository): `/private/tmp/claude-501/-Users-kylekopacek-orca-workspaces-Ohvernight-m3-foundation/1af2c3f1-290d-4195-82ce-da82ec9d5e39/scratchpad/m4/prep/connector-extent/part1_connectors.py`, using an unmodified copy of the approved-rule script `grouping.py` in the same folder. Output: `part1_out.txt`, `part1_out.json` there.
- Method: the approved rule was run as is; then rerun with connectors that carry a `gnis_id` added as connectivity-only candidates; then, as adversarial variants, with unnamed connectors usable by any river, with canals, with pipelines, and with all three. Groups, members and drawn lengths were compared id by id. Adjacency is a shared end point after rounding to six decimals, as in the specification.
- Limits: two regions; Douglas holds named flowlines only. "Touches" means a shared end point; a segment ending on the interior of another is not counted, in line with the approved adjacency rule.
