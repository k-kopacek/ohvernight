# System overview

Repository architecture after M3 PR B merged (2026-10-06). R-2 was
triggered, reviewed and resolved by the owner on 2026-10-05: Leaflet is kept
(A10). The original threshold misses remain recorded. A8 is approved and
kept. The first iPhone Safari pass on 2026-10-05 failed several mobile-UX
items. A11 remediation is implemented. One of its three performance sessions
missed the Douglas all-layers limit; the owner accepted that result as
run-to-run variation under A13, and it remains recorded as a miss. The final
iPhone Safari validation passed on 2026-10-06; iPad and Android device checks
remain unverified and deferred. PR B is merged and M3 is complete.
Plans are in the [roadmap](../../ROADMAP.md).

## Shape of the system

Ohvernight is a static website plus an offline research-data pipeline. There
is no backend, database, API, account system or analytics. Nothing runs on
a server at request time.

```text
agency sources ──(manual refresh)──▶ Python pipeline ──▶ canonical JSON / GeoJSON
                                                             │ offline display build
                                                             ▼
                                               per-region display artifacts
                                                             │ reviewed pull request
                                                             ▼
                                                main → GitHub Pages
                                                             │
                                                             ▼
                                               shared Explore + Leaflet
```

## Browser surfaces

Plain HTML, CSS and JavaScript run without a build step, framework, bundler
or `package.json`. Vendored Leaflet 1.9.4 draws the map; both v2 regions use
the existing USGS imagery/topographic pair. Trip and saved state stays in
browser local storage.

| Surface | Location | Behaviour |
|---|---|---|
| Original site | Root `index.html`, `app.js`, `trip-rules.js`, `styles.css` | Retained for comparison; PR B leaves it untouched. |
| Unified v2 | `v2/index.html`, `v2/app.js`, `v2/explore/` | Aspen planner/adventure capabilities and Douglas browse/season/saved/GPX capabilities share one mobile-first Explore shell. |
| Douglas bookmark | `v2/regions/douglas-co/index.html` | Forwards to `/v2/?region=douglas-co&view=map`; includes a plain fallback link. |

The host declares the default region. `?region=<id>` selects a validated
region; `&view=map` skips the planner. Shared modules contain no region IDs,
region paths or regional presentation text. Region configuration carries
presentation, storage keys and capabilities; `extras.js` is the only
region-specific capability code. The legacy fire-monitor selector in
`v2/trust.js` is deliberately preserved under amendment A7.

`map-adapter.js` alone calls Leaflet. Its original ten exports are joined by
`setSelected(id, featureId | null)` and
`setLabels(id, {property, minZoom, max} | null)`, as recorded in
[specification section 8.1](../specs/M3-unified-mobile-explore.md#81-renderer-adapter).
No Leaflet object leaves the adapter. The loader
fetches the active manifest, presentation config and display index, then
coverage and small place lists. Pins and coverage are usable before
feature layers. Under approved A8, eligible default-on
requests start together; parsing, evidence restoration and drawing proceed
one layer per task in configured order, retaining the yields. An earlier
pending response waits its turn; a failed response does not block the next
layer. Failed layers have independent retry controls, off layers stay unloaded,
and `min_zoom` gates first loading. Detail content is built on selection.

The local benchmark is CPU/main-thread dominated; concurrent fetching showed
no measurable local timing improvement. A8 avoids deliberately serialising
independent network requests in real use; its benefit under real network
latency remains unmeasured. A10's PR B heap threshold (115% of same-session
base) and the architecture trigger R-5 (66 MB) are different controls.

On phones the results sheet has collapsed, half and expanded states, moved
by dragging its handle/header; its content scrolls independently. Search,
browse and planner results and feature detail live in the same sheet, with
Back returning to the retained list and filters. Tapping a feature selects,
highlights and fits it with sheet-aware padding. Opening the layer drawer
collapses the sheet, and opening the sheet closes the drawer on phones.
Labels use only source names, appear from zoom 14 and share a 32-label cap.
Double-tap zooms the map; local zoom-control handling prevents page zoom
without restricting accessibility zoom globally. These interactions have
automated Chrome coverage; final iPhone Safari validation passed. iPad and
Android device checks remain unverified and deferred.

The map stays north-up. Rotation and compass were not implemented: Leaflet
1.9.4 has no bearing API, and the evaluated GPL-3.0 `leaflet-rotate` dependency
patches Leaflet globally. Pursuing rotation is the owner's decision under
A11. Phone landscape layout is covered independently of map bearing.

Dates, vehicle and list filters do not hide map geometry. Land styling
follows spatial precision: generalized management context uses restrained
dashed boundaries and exact approved wording, with Unknown last.

## Pipeline and published data

`v2/pipeline/` is a Python 3.12 research-data pipeline using requests,
shapely, pyproj, PyYAML and jsonschema. Numbered scripts build the Aspen
bundle; separate scripts retrieve trails, Douglas data and RIDB inventory.
Live refreshes run only on explicit request and may require `RIDB_API_KEY`.
They produce artifacts; they never publish automatically.

Staging output is untracked at `v2/pipeline/data/processed/map-data-v2.json`.
After validation, publication promotes it to the canonical
`v2/map-data-v2.json` through review. Shared pipeline logic is in
`v2/pipeline/scripts/lib/`; `v2/pipeline/config/` remains Aspen-only.

| Region | Canonical files | Browser delivery |
|---|---|---|
| Aspen | `v2/map-data-v2.json`, `trails.geojson`, `overnight-options.json`, `ridb-options.json`, `destinations.json`, pipeline rules/coverage | Small place lists/rules and `regions/aspen/display/` |
| Douglas | `v2/regions/douglas-co/research.json` | `regions/douglas-co/display/`; verbatim extras listing/coverage |

Canonical paths and data are unchanged by PR B. The browser never fetches
either canonical geometry bundle. `build_display.py` generates delivery
GeoJSON with six-decimal coordinates, consecutive duplicates removed, and
only parts made degenerate by rounding dropped. Entire feature collapse
fails the build. Properties and evidence stay unchanged; evidence is stored
once per layer and restored by the loader. Each index carries artifact and
canonical hashes/counts plus verbatim transport copies for every non-null
`status_ref`, including place-list layers. Delivery is reproducible offline.

The root `map-data.json` remains the legacy OpenStreetMap extract.
Attribution and limits remain in [DATA-LICENSE.md](../../DATA-LICENSE.md)
and `v2/DATA-LICENSE.md`.

## Contract and trust

Each region has `region.json`, validated by the normative
[data contract](../../v2/pipeline/docs/data-contract.md), and a closed-schema
`explore.json` validated by `explore-config.schema.json`. Configuration
contains presentation only; limitations, source scope, freshness and
fact-coverage statements belong to the manifest.

Stable rules R01–R50 and R66–R68/R75 validate canonical semantics; R60–R65
validate derived delivery, including byte hashes, exact selection,
properties/evidence, approved rounding and canonical transport copies.
Display geometry is never used for a canonical contract check. The pinned
non-conformance sets do not grow.

| Concept | Implementation |
|---|---|
| Provenance | Canonical per-feature evidence and manifest sources; safe URLs/text in `explore/evidence.js` |
| Retrieval status | Canonical transport records, copied verbatim into display indexes and normalized by shared vectors |
| Freshness | Python/JS parity vectors; v2 runtime policy comes from the active manifest's hours |
| Trip evaluation | `v2/trip-rules.js`, `v2/trust.js`; exclusions precede cautions and conflicting rules merge conservatively |
| Source-health wording | Preserved `Trust.sourceSummary`, supplied loaded monitor evidence and the RIDB place document |
| Limitations | Manifest statements rendered verbatim; no use of the deprecated evidence confidence field |
| Known gaps | N1–N18 register in the data contract; N9 retired for v2, N14 for browser delivery, N17 as a regression marker |

Staleness never erases existence, hides a layer or weakens a restriction.
The root legacy evaluator retains its 30-day threshold. Canonical evidence
duplication remains. The hard-coded Rampart record remains deferred to M7.

## Verification and deployment

GitHub Pages publishes the whole repository from `main`: merging is a
production deploy. Claude specifies and reviews independently, Codex builds,
CI checks, and the human approves the reviewed head before merge.

`.github/workflows/ci.yml` runs offline without secrets:

- `python`: `00_selftest.py`, including R60–R65, rebuild, config and budgets.
- `node`: syntax checks and `node --test v2/pipeline/tests/*.test.cjs`,
  including base compatibility, region isolation, wording and adapter surface.
- `browser`: headless Chrome B1–B10 and A11 interaction checks for both regions
  at four sizes, with landscape checks at the phone sizes; bounded
  DevTools startup/commands, all non-local requests blocked, guarded cleanup.

Browser checks assert geometry, focus, request sets and bytes, not time.
Separate five-run local timing/heap comparisons use
`v2/pipeline/tests/browser/measure.mjs`; the historical baseline script is
unchanged. The performance record preserves all three required A11 sessions
and four diagnostic sessions. Required session 2 missed Douglas
`allDefaultLayersMs` at 136.4954% of base against the 135% limit; it remains
recorded as a miss. The owner accepted it as run-to-run variation under A13.
No specific A11-code inefficiency was identified in the diagnosis; diagnostic
runs do not replace acceptance sessions. Final iPhone Safari validation
passed; iPad and Android device checks remain deferred.
Manual `refresh-map.yml` and `ridb-check.yml` upload artifacts without
committing or deploying; no refresh is scheduled.

## Deferred areas

| Area | Current limit | Milestone |
|---|---|---|
| Water | Name-based display subset; no recreational-use semantics | M4 |
| Land classification | Limited-scale source classes only; no parcel-level finding | M5 |
| Trails | County/study-clipped USFS segments; no COTREX | M6 |
| Camping | Small research inventory; Rampart listing remains hard-coded | M7 |
| Choose Your Adventure | Existing Aspen pilot, unchanged inputs/ranking | M8 |

Optimized Leaflet is the approved M3 renderer. Payload, timing, memory and
future product triggers in ADR-006 govern any later reconsideration.
