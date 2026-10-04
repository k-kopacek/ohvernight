# System overview

What Ohvernight is today, described from the repository as of the M2 merge
(2026-10-04). This document describes what exists, not what is planned. Plans
are in the [roadmap](../../ROADMAP.md).

## Shape of the system

Ohvernight is a static website plus an offline data pipeline. There is no
backend, database, API, service, account system or analytics. Nothing runs on
a server at request time.

```text
agency sources ──(manual, on demand)──▶ Python pipeline ──▶ JSON / GeoJSON files
                                                              │ committed by pull request
                                                              ▼
                                                 repository `main`
                                                              │ GitHub Pages
                                                              ▼
                                          static pages + Leaflet in the browser
```

## Browser applications

All three are plain HTML, CSS and JavaScript with no build step, bundler,
framework or `package.json`. Maps use Leaflet 1.9.4, vendored in the
repository. Basemap tiles are requested by the browser from USGS The National
Map. Trip selections and saved plans live only in the browser's local storage.

| Surface | Location | Notes |
|---|---|---|
| Original site | repository root (`index.html`, `app.js`, `trip-rules.js`, `styles.css`) | Retained for comparison. Not to be silently replaced. Its only M2 change was the staleness fix in `trip-rules.js`. |
| v2 app (Aspen / Snowmass) | `v2/` (`index.html`, `app.js`, `map-layers.js`, `trail-discovery.js`, `trip-rules.js`, `trust.js`) | Trip planner, Choose Your Adventure pilot, Explore map, trail search. |
| Douglas County field test | `v2/regions/douglas-co/` (`index.html`, `preview.js`, `discovery.js`, `county.css`) | A separate page with its own app code and data file. |

The Aspen and Douglas experiences are separate applications with different
code and data envelopes. There is no region selector and no shared region
loader. No browser code reads the region manifests yet.

## Data pipeline

`v2/pipeline/` is a Python 3.12 research-data pipeline (requests, shapely,
pyproj, PyYAML, jsonschema).

- Numbered scripts `01`–`09` plus `run_pipeline.py` build the Aspen bundle.
  Separate scripts fetch trails (`fetch_trails.py`), Douglas County data
  (`fetch_douglas.py`, `enrich_douglas.py`) and the RIDB inventory
  (`check_ridb.py`).
- Pipeline output is written to an untracked staging path,
  `v2/pipeline/data/processed/map-data-v2.json`. After validation it is copied
  to the canonical app-facing `v2/map-data-v2.json` through a pull request.
  The pipeline does not deploy or modify the website.
- Live refreshes contact external sources, run only on request, and may need
  `RIDB_API_KEY` from the environment or a GitHub Actions secret.
- Shared logic lives in `v2/pipeline/scripts/lib/`. Configuration lives in
  `v2/pipeline/config/` (`sources.yaml`, `legal_rules.yaml`, `aoi.geojson`,
  `rules-registry.json`) and is Aspen-only today.

## Published data

| Region | Files | Envelope |
|---|---|---|
| Aspen | `v2/map-data-v2.json` (about 10 MB), `v2/trails.geojson`, `v2/overnight-options.json`, `v2/ridb-options.json`, `v2/destinations.json`, `v2/pipeline/config/rules-registry.json` | Schema-v2 bundle, a bare FeatureCollection, and place lists |
| Douglas County | `v2/regions/douglas-co/research.json` (about 6 MB) | One file, `schema_version: 1`, layers keyed by name |

`v2/map-data.json` is a legacy OpenStreetMap extract that is published but not
covered by any manifest. Attribution and limits are in
[DATA-LICENSE.md](../../DATA-LICENSE.md) and `v2/DATA-LICENSE.md`.

## Deployment

GitHub Pages publishes the whole repository from `main`. **Merging to `main`
is a production deploy.** There is no staging environment and no separate
release step.

## CI and tests

`.github/workflows/ci.yml` runs on every pull request and on pushes to `main`,
offline and without secrets:

- `python`: `v2/pipeline/scripts/00_selftest.py` (88 tests at the M2 merge).
- `node`: `node --check` on the browser scripts, then
  `node --test v2/pipeline/tests/*.test.cjs` (38 tests at the M2 merge).

Two further workflows, `refresh-map.yml` and `ridb-check.yml`, are manual
dispatch only. They upload artifacts and do not commit or deploy. Nothing is
scheduled.

At the time of writing, `main` has no GitHub branch protection: CI reports but
does not technically block a merge, and the human approval gate is held by
convention. Enabling protection is an owner follow-up recorded in the M1
specification.

## Regional data contract (M2)

- Each region has a hand-reviewed manifest, `v2/regions/<id>/region.json`
  (`aspen`, `douglas-co`). It declares coverage, sources, layers, where each
  layer's transport status lives, freshness policy, and what is unknown for
  each of eight fact dimensions.
- The manifest schema is `v2/pipeline/schema/region-manifest.schema.json`.
- The validator is `v2/pipeline/scripts/lib/region_contract.py`, with stable
  rule IDs R01–R50. It checks each manifest and the published data it points
  at. It runs in the Python test suite, so CI enforces it.
- The contract is additive: the existing data files, envelopes and the Aspen
  bundle schema (`v2/pipeline/schema/schema.json`, checked by
  `lib/validation.py::validate_bundle`) are unchanged.
- Adding or changing a layer, source or feature property requires updating
  the region manifest in the same pull request.

## Where evidence, provenance and freshness live

| Concept | Where it lives |
|---|---|
| Normative definitions | [v2/pipeline/docs/data-contract.md](../../v2/pipeline/docs/data-contract.md); principles in [trust-principles.md](../product/trust-principles.md) |
| Provenance | Per-feature `evidence` object (`source_url`, `agency`, `retrieved_at`, `verification_method`); manifest `sources` |
| Transport / retrieval status | `source_status` records inside the data files, in several legacy shapes; manifests point at them through `status_ref` |
| Interpretation and verification | Rule records in `v2/pipeline/config/rules-registry.json`; reviewed-site records; the claim object defined in the contract |
| Freshness | Computed, never stored: `Trust.freshness` in `v2/trust.js` and `freshness` in `v2/pipeline/scripts/lib/evidence.py`, held at parity by `v2/pipeline/tests/fixtures/freshness-vectors.json` |
| Trip evaluation | `TripRules.evaluate` in `v2/trip-rules.js` and the root `trip-rules.js`; `Trust.applyRules` in `v2/trust.js` |
| Known violations | The non-conformance register (N1–N18) in the data contract, pinned by tests where possible |

## Major deferred areas

These are known gaps, not current capabilities. Milestone ownership is set in
the [roadmap](../../ROADMAP.md).

| Area | Current state | Milestone |
|---|---|---|
| Mobile Explore architecture | Two separate apps; map space on phones is constrained; rendering approach (Leaflet with lazy GeoJSON, or MapLibre/vector) is undecided | M3 |
| Land presentation and classification | Generalized management polygons drawn as crisp boundaries (N17); classification is limited-scale context only | M3 (presentation), M5 (classification) |
| Recreational water semantics | Display selects by name; feature type, permanence and size are dropped at ingest (N18) | M4 |
| Trails / COTREX | USFS trail segments only; no COTREX content; licensing and terms unverified | M6 |
| Camping / dispersed camping | Small curated and RIDB inventories; one Douglas listing and its seasonal closure are hard-coded in app code (N7, which the register currently assigns to Milestone 3) | M7 |
| Choose Your Adventure | An Aspen-only pilot pairing one activity with nearby listings | M8 |
