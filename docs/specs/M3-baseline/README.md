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
All five measures pass for both regions in each of the three new A10 sessions.
The comparison code is `v2/pipeline/tests/browser/measure.mjs`; the historical
`measure.mjs` above remains byte-identical. It serves base files directly
from Git and head files from the checkout, blocks non-local requests and
uses the hardened browser-harness cleanup. Its method and threshold results
are recorded in the report.

```sh
node v2/pipeline/tests/browser/measure.mjs > /tmp/ohvernight-performance.json
```

The deterministic browser job asserts no timings. The owner's real-device
matrix and the reviewer's independent same-session comparison remain owed.

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
the real-device matrix is still owed by the owner.
