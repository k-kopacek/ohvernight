# M3 performance baseline

Evidence for the architecture decision and the acceptance thresholds in
[../M3-unified-mobile-explore.md](../M3-unified-mobile-explore.md), section 16.

- `baseline.json` — raw results, measured on 2026-10-04 at `main` commit
  `3dc0fef` with headless Chrome 154 on macOS.
- `measure.mjs` — the script that produced them. Node 22 or later and a local
  Chrome; no npm dependency.

## Reproduce

From the repository root, at the commit being measured:

```sh
python3 -m http.server 8765 --bind 127.0.0.1 &
node docs/specs/M3-baseline/measure.mjs > /tmp/ohvernight-baseline.json
```

Set `CHROME=/path/to/chrome` if Chrome is not in a standard location, and
`BASE=http://host:port` to measure another server.

## Limits

- The local server sends no compression and adds no network delay, so byte
  counts are uncompressed and timings are parse-and-build time.
- `cpuThrottle: 4` is Chrome's CPU throttle, a rough stand-in for a mid-range
  phone. No real device was measured.
- Timings vary between machines and runs. Compare runs made on the same
  machine; do not gate CI on them.
- Basemap tiles are requested from USGS and Esri/OpenStreetMap by the current
  pages; they are excluded from the same-origin byte counts.
- The script targets the page structure at `3dc0fef`. It is a record of the
  baseline, not the M3 browser check, which is specified separately.

## PR B comparison

`pr-b-performance.json` records five runs each of base `3dc0fef` and the
PR B application per session at 390×844 with 4× CPU throttle. Three original
sessions and three separate post-A8 sessions are preserved, with raw values
and every threshold comparison. A separate section adds three A10 sessions,
using the owner's amended thresholds without rewriting earlier results.
All five measures passed for both regions in each of those three pre-A11
A10 sessions. The appended `a11_mobile_ux_remediation` section preserves
three later required sessions at `86f1c97` and four diagnostic sessions,
including all raw rows, limits, ratios, head commits and helper SHA-256.
Required A11 session 2 missed Douglas `allDefaultLayersMs` at 136.4954% of
base against 135%; this is NOT a pass. The diagnostic ratios at `5fd5903`,
`f65dacd`, `bf2f3dc` and `810ff18` are 127.0951%, 124.1308%, 127.9431% and
122.8470% respectively. These are diagnostic evidence, not acceptance;
they identified no specific inefficiency in the A11 code and do not replace
the required sessions. The miss's disposition belongs to the owner.
The comparison code is `v2/pipeline/tests/browser/measure.mjs`; the historical
`measure.mjs` above remains byte-identical. It serves base files directly
from Git and head files from the checkout, blocks non-local requests and
uses the hardened browser-harness cleanup. Its method and threshold results
are recorded in the report.

```sh
node v2/pipeline/tests/browser/measure.mjs > /tmp/ohvernight-performance.json
```

The deterministic browser job asserts no timings. The first iPhone Safari
pass on 2026-10-05 failed several mobile-UX items; A11 remediation is
implemented, and a second real-device pass and merge approval remain owed.

A11's phone results sheet has collapsed, half and expanded states moved by
drag. Search, browse and planner results and feature detail share the sheet
with Back; a feature tap selects, highlights and fits it. Source-name labels
appear from zoom 14 and are capped at 32 globally; the drawer and sheet are
mutually exclusive on phones. Double-tap zooms the map and local zoom-control
handling prevents page zoom. Automated Chrome checks cover these properties;
they do not claim a real-device pass. The adapter adds only `setSelected` and
`setLabels` to its original ten exports. The map stays north-up: rotation
and compass were not implemented because Leaflet 1.9.4 has no bearing API
and the evaluated GPL-3.0 `leaflet-rotate` dependency patches Leaflet globally.
The rotation decision is with the owner.

All deterministic budgets pass. The original Douglas all-default-layer time
and heap thresholds were missed before and after A8; those results stand.
R-2 was triggered, reviewed and resolved by the owner on 2026-10-05: Leaflet
is kept (A10). This owner amendment is not a retroactive pass. A10 limits map
usable to 60% and all layers to 135% of same-session base all-layer time, and
heap to 115% of same-session base heap for the same region. The PR B heap
control and architecture trigger R-5 (66 MB) are different controls.
The report preserves the first discarded comparison, whose county status
selector fired early on a blocked basemap tile, and explains the approved
readiness correction. A8 is approved and kept: eligible fetches start together
while parsing, restoration and drawing stay ordered, with one layer per task
and the existing yields. The local benchmark is CPU/main-thread dominated;
concurrent fetching showed no measurable local timing improvement. A8 avoids
deliberately serialising independent network requests in real use; its
benefit under real network latency remains unmeasured. PR B is not merged;
the second real-device pass and the A11 performance-miss disposition are
still owed by the owner.
