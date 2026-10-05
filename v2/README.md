# Ohvernight v2 — unified Explore

`/v2/` opens the Aspen / Snowmass trip planner. **Explore the open map** skips
trip entry; `/v2/?region=aspen&view=map` opens the map directly.
`/v2/?region=douglas-co&view=map` opens Douglas County. Existing bookmarks to
`/v2/regions/douglas-co/` forward with `location.replace` and retain a plain
link when scripts are off.

The map is the page. On phones the results sheet has three states —
collapsed, half and expanded — moved by dragging the handle/header, with
independently scrolling content. Search, browse and planner results and
feature detail live in the sheet; Back returns to the retained list and
filters. Tapping a feature selects, highlights and fits it. The layer drawer
and the sheet are mutually exclusive on phones: opening one collapses or
closes the other. Source-name labels appear from zoom 14 with a global cap
of 32; unnamed features receive no invented label. Double-tap zooms the map,
and local zoom-control handling prevents page zoom without blocking page
zoom globally. These changes have automated Chrome coverage; real-device
retesting is still owed. Every layer starts on and loads
progressively; dates, vehicle and list filters never remove map features.
Approved and kept amendment A8 starts eligible default-on requests together,
then parses and draws one layer per task in order with the existing yields.
Source details are built when selected. **Sources & coverage** carries the
manifest's statements and limitations verbatim, with per-layer retrieval
status from the display index. A stale source does not remove a feature or
weaken a restriction.

## Preserved capabilities

Aspen keeps the planner, Plan A / backup, trail search, nearby lists and the
Choose Your Adventure pilot. The pilot's inputs and ranking are unchanged;
it pairs a published trail activity with nearby camping listings and does
not establish a connecting route. Trip conflicts remain visible.

Douglas keeps trails/camping/trailheads browsing, published-season checks,
saved research, field-test notes, plan export and segment GPX export. The
Rampart area listing and coverage note live verbatim in `extras.js`. GPX
uses the approved six-decimal display geometry, including any parts removed
by the display builder after rounding; it performs no further transformation.

Existing browser storage keys are preserved: `ohvernight-trip-v1`,
`ohvernight-douglas-plan-v1`, `ohvernight-douglas-plan-v1-notes` and
`ohvernight-douglas-plan-v1-trip`. Saved IDs that no longer resolve are dropped.

## Code and data

- `index.html` and `app.js` host the shared shell and declare its default region.
- `explore/` contains shared loading, UI, renderer and capability modules.
  `map-adapter.js` is the only module that calls vendored Leaflet 1.9.4.
  Its original ten exports plus `setSelected` and `setLabels` are pinned by
  the exact adapter-surface test; no Leaflet object leaves it.
- `regions/<id>/region.json` declares data, sources, freshness and limitations;
  `explore.json` declares presentation and capabilities under a closed schema.
- `regions/<id>/display/` contains reproducible delivery artifacts: selected
  geometry rounded to six decimals, evidence tables and verbatim transport
  copies in `index.json`. Canonical published files remain unchanged.
- `map-layers.js` retains the pinned `displayWater` selection rule for the
  builder/tests. The displayed Aspen water subset remains 1,555 features from
  6,926 canonical hydrology features. Names do not establish recreational use.

Both regions use the existing USGS imagery/topographic pair. Land is
**Generalized land management context — not parcels**. Unshaded land remains
unknown; source management classes do not establish access or camping permission.
Map tiles need a connection. See [DATA-LICENSE.md](DATA-LICENSE.md), the
[regional contract](pipeline/docs/data-contract.md) and the
[system overview](../docs/architecture/system-overview.md).

The map is north-up. Rotation and compass were not implemented: Leaflet
1.9.4 has no bearing API, and the evaluated GPL-3.0 `leaflet-rotate` dependency
patches Leaflet globally. Whether to pursue rotation remains the owner's
decision under A11; landscape layout has separate automated coverage.

## Verify and publish

From the repository root:

```sh
v2/pipeline/.venv/bin/python v2/pipeline/scripts/00_selftest.py
node --test v2/pipeline/tests/*.test.cjs
node v2/pipeline/tests/browser/run.mjs
v2/pipeline/.venv/bin/python v2/pipeline/scripts/build_display.py
```

The browser check blocks all non-local requests and checks both regions at
four viewport sizes. Timing comparisons and the human real-device matrix
are separate; see [browser instructions](pipeline/tests/browser/README.md).
The app has no build step, package manager, backend or runtime dependency
beyond vendored Leaflet. Requests use normal HTTP caching and display hashes.

R-2 was triggered, reviewed and resolved by the owner on 2026-10-05; Leaflet
is kept (A10). The original threshold misses remain recorded. The local
benchmark is CPU/main-thread dominated; concurrent fetching showed no
measurable local timing improvement. A8 avoids deliberately serialising
independent network requests in real use; its benefit under real network
latency remains unmeasured. The PR B heap threshold (115% of same-session
base) and architecture trigger R-5 (66 MB) are different controls. The first
iPhone Safari pass on 2026-10-05 failed several mobile-UX items; A11
remediation is implemented. Required A11 performance session 2 missed the
Douglas all-layers limit at 136.4954% against 135%; this is not a pass and
awaits the owner's disposition. Four diagnostic sessions identified no
specific inefficiency in the A11 code and do not replace the required
sessions. PR B is not merged; a second real-device pass and merge approval
are still owed by the owner.

GitHub Pages publishes the repository from `main`. A reviewed pull request,
green CI and explicit human approval are required before merging. The root
legacy site remains available for comparison. Manual RIDB and map refresh
workflows produce artifacts for review; they do not publish automatically.
Never put `RIDB_API_KEY` in browser code or published data.
