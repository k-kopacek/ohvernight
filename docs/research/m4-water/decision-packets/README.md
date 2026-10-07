# Owner decision packets

One file per decision the owner has to make before or during M4-B and M4-C.
Each has the same sections so it can be answered quickly: decision, evidence,
current behaviour, options, trade-offs, risks, recommendation, what changes if
approved, what stays the same, tests required, rollback.

Nothing here is decided or implemented. A recommendation is the
coordinator's or the analysing agent's; the owner decides.

| # | Packet | One-line recommendation |
|---|---|---|
| 1 | [m4a-merge.md](m4a-merge.md) | Approve PR #12 at its reviewed head |
| 2 | [south-platte.md](south-platte.md) | Keep the approved rule; pad the Douglas water extent by 0.005 degrees (about 500 m, Aspen's value). The river is missing because the county clip removes the one perennial segment, 11.5 m outside the line. Preview: [south-platte-preview.html](south-platte-preview.html) |
| 3 | [connectors.md](connectors.md) | Approve: a connector carrying the river's own GNIS id joins its reaches for grouping only; never drawn |
| 4 | [extent-edge.md](extent-edge.md) | Accept edge splitting for M4 (one Aspen river affected); confirm that one source segment cut by the clip stays one member |
| 5 | [threshold.md](threshold.md) | Keep 2 ha; inspect the 26 possible-loss lakes; decide whether to allow a reviewed inclusion list for small lakes |
| 6 | [source-scope-wording.md](source-scope-wording.md) | Approve the proposed two sentences for M4-B |
| 7 | [cpw-outreach.md](cpw-outreach.md) | Send the drafted message; M4-D stays closed until a written answer |
| 8 | [monetization.md](monetization.md) | Adopt the principle: facts free, planning workflow paid; no pricing or billing yet |

## How packets 2 and 4 interact

Packet 2 recommends padding the Douglas water extent, which draws water up to
about 500 m outside the county outline and needs either an offline re-clip of
the saved M4-A pages or one more controlled NHD request. Packet 4 recommends
no extra padding for Aspen. The two are consistent: Douglas has no water
padding today and its western boundary follows its principal river; Aspen
already has 0.005 degrees and only one minor creek is affected. If the owner
authorises a request for packet 2, packet 4's Aspen ring could ride on it,
but neither packet assumes that.

The coordinator re-checked two facts packet 2 depends on: NHD segment
117795757 (South Platte River, 46006, 0.076 km) is in the saved M4-A raw
pages and absent from the canonical Douglas data, and the Aspen hydrology
layer's `extent_padding_deg` is 0.005. The other figures in packet 2 are the
analysing agent's and were not recomputed.
