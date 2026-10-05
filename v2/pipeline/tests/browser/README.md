# Explore browser checks and measurements

Run from the repository root with Node 22+ and local Chrome:

```sh
node v2/pipeline/tests/browser/run.mjs
```

Set `CHROME=/path/to/chrome` if needed. The dependency-free harness starts a
local static server, blocks every non-local request, and runs B1–B10 for
Aspen and Douglas at 320×568, 390×844, 768×1024 and 1440×900. Basemap tiles
are absent; the app must still work. The CI job name remains `browser`.

`explore-checks.mjs` checks free map area, sheet/drawer bounds, 44-pixel
controls and pins, overflow, map and sheet drags, keyboard reachability,
Escape/focus restoration, request isolation and uncompressed bytes. It
injects each manifest/config/index/display/place-list/Leaflet failure and
checks independent layer retries. It pins old URL/storage behaviour, saved
notes, capability gating and computed land styles/Unknown wording.

Every display feature is handed to the adapter. A manifest-allowed null
geometry record is counted separately, consumed by a named source-panel
control and preserved source-health wording; it gets no invented map point.
Normal page loads retain checks for uncaught exceptions, console errors,
failed local requests and requests escaping the non-local block.

Startup polling has a 60-second deadline and bounded HTTP requests.
DevTools commands have a 20-second bound; disconnects reject pending and
later commands with diagnostics. Chrome exit interrupts inspection. One
guarded `finally` closes the socket/server, reaps Chrome and removes its
temporary profile, then exits naturally. Offline unit tests cover delayed
readiness, closed ports, hung requests, child exit and DevTools failures.
Importing `run.mjs` does not launch the harness.

## Timing comparison

```sh
node v2/pipeline/tests/browser/measure.mjs > /tmp/ohvernight-performance.json
```

This separate script uses the hardened harness helpers and serves base
commit `3dc0fef` from `git show` plus the current checkout in one local Chrome
session. It measures five cold-cache runs of each version for both regions
at 390×844, device scale 2 and 4× CPU throttle. Every non-local request is
blocked. It records map-usable/default-layer readiness, the longest observed
load long task, heaviest-layer on/off latency through the next frame, and JS
heap after GC. Readiness is polled at 50 ms as in the baseline script.
Base Aspen requires its enabled landing action and all twelve layer controls; its tile-error
message uses a separate element. Base Douglas requires eight layer controls
and seven coverage rows, because blocked tiles can change its status text
before data loads. Head events are `mapUsable` (12.2 step 3) and
`defaultLayersLoaded`. Versions run back to back, five per region;
a 1500 ms settle precedes long-task/heap readings. Raw rows, medians and each
section-16.4 threshold are reported. No measured threshold is asserted in CI.

The original `docs/specs/M3-baseline/measure.mjs` is an immutable record of
how `baseline.json` was measured; it is not adapted for the new page.
The PR B report lives beside that baseline. Compare versions in one session
on one machine; historical absolute milliseconds are context only.
The report preserves the original and post-A8 threshold misses and adds
three A10 sessions. R-2 was triggered, reviewed and resolved by the owner on
2026-10-05; Leaflet is kept (A10). A8 is approved and kept. The local benchmark
is CPU/main-thread dominated; concurrent fetching showed no measurable local
timing improvement. A8 avoids deliberately serialising independent network
requests in real use; its benefit under real network latency remains
unmeasured. A10 changes the PR B limits to 60% for map usable, 135% for all
layers and 115% for heap, relative to same-session base. PR B's heap control
and architecture trigger R-5 (66 MB) are different controls. The measurement
method and other thresholds are unchanged; PR B is not merged.

The human owner must still test real iOS Safari and Android Chrome, both
regions: pan, pinch, sheet drag, drawer, trail/land details, landscape and
throttled reload. Headless Chrome does not satisfy that gate.
