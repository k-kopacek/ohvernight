# Ohvernight repository audit — 2026-10-01

> **Historical record, recovered 2026-10-07.** This is the original audit, found as an untracked file in a local checkout and committed unchanged below this note. It describes the repository at `9388845` on 2026-10-01. Much of it has since been addressed (see [architecture-audit.md](architecture-audit.md) for the disposition of each finding), and some statements are no longer true: for example `main` now has an active ruleset, CI runs on every pull request, and the rendering decision in M3 kept Leaflet. Its recommendations are not decisions; `ROADMAP.md` and the approved specifications govern. The `M1-spec.md` it mentions at the end was not recovered.

Read-only audit of `k-kopacek/ohvernight` at `9388845` (main, clean tree). No repo files were modified.

**What was checked and how**

- Every source file, config, doc, workflow and test was read. Data files were profiled with scripts.
- The 35 offline Python tests were run from a throwaway virtualenv outside the repo: all pass.
- The published `v2/map-data-v2.json` was validated against `schema.json` and `validate_bundle`: passes.
- GitHub settings were read through the API (Pages, workflows, branch protection).
- **Not run:** the Node tests (`*.test.cjs`) — Node is not installed on this machine. No live source fetches were made. Nothing was checked in a browser, so mobile layout findings come from reading the CSS, not from a device.

---

## 1. Current architecture

### Shape of the repo

| Path | What it is | Status |
|---|---|---|
| `/` (root `index.html`, `app.js`, …) | Original Aspen overnight prototype (5 places, Leaflet) | Legacy, still deployed at the site root |
| `v2/` | Current static app: Aspen/Snowmass planner + Explore map | Active |
| `v2/regions/douglas-co/` | Separate Douglas County dirt-bike/camping explorer | Active, but a second app |
| `v2/pipeline/` | Python data pipeline (ArcGIS/RIDB fetch → clip → validate → bundle) | Active, manual runs only |
| `.github/workflows/ridb-check.yml` | Manual RIDB export | The only installed workflow |

About 3,400 lines of hand-written code. No build step, no package manager for the frontend, no backend.

### Deployment

- GitHub Pages, **legacy build from `main` at `/`**. Every push to `main` publishes the entire repository tree, including `v2/pipeline/` (scripts, tests, raw RIDB import).
- `main` is unprotected. The repo is public. Pages carry `noindex`.
- History is 20 "Add files via upload" commits (zip uploads through the web UI) plus one hygiene commit today. The READMEs still describe the zip-upload workflow; `AGENTS.md` describes a branch workflow.

### Frontend (v2)

- Plain script tags, IIFE globals: `TripRules`, `Trust`, `MapLayers`, `TrailDiscovery`, then `app.js` (205 dense lines holding all UI state and rendering).
- Leaflet 1.9.4 (vendored) with `preferCanvas`. USGS National Map raster tiles (imagery/topo).
- On load it fetches seven files in parallel, all with `cache: 'no-store'`:
  `destinations.json`, `overnight-options.json`, `map-data-v2.json` (10.1 MB), `ridb-options.json`, `pipeline/config/rules-registry.json`, `pipeline/config/aoi.geojson`, `trails.geojson` (1.5 MB).
- Two entry modes on one page: the landing form ("Choose your adventure": mountain, dates, vehicle, one activity) and "Explore the open map".
- 12 layer definitions, all on by default, each a `L.geoJSON` built once and toggled.
- Trip evaluation runs in the browser (`TripRules.evaluate`): stay limit → source staleness → tent-only → clearance → MVUM season window.
- State persists in `localStorage` only (trip, Plan A / backup).

### Frontend (Douglas County)

- A separate page with its own JS (`preview.js`, `discovery.js`), CSS, storage keys, basemaps (Esri World Imagery + OSM tiles) and data file (`research.json`, 6.2 MB).
- Reuses only `trail-discovery.js` and Leaflet from v2.
- Adds things v2 lacks: trailheads, date-vs-season badges for trails, GPX export, field-test notes export, land coloured by manager.

### Data pipeline

- `run_pipeline.py` runs nine numbered steps into a staging directory, validates, then atomically replaces `data/processed/map-data-v2.json`. Required-step failure preserves the previous bundle; optional-step failure yields an explicit empty layer.
- Sources (`config/sources.yaml`): BLM Surface Management Agency *limited-scale* (land), USFS EDW wilderness, USFS MVUM roads, USGS NHD (flowline/area/waterbody), RIDB, a Pitkin County page-hash monitor (fire), CPW wildlife (disabled, 404).
- `lib/arcgis_client.py` fetches by object-ID set, verifies count and IDs before and after, splits on transfer limits.
- Step 07 derives "areas to research": 300 ft MVUM road buffer ∩ (USFS ∪ BLM) − wilderness − 100 ft water setback − supplied restriction polygons. Buffers are done in EPSG:26913.
- Outside the main pipeline: `fetch_trails.py` (USFS trails → `v2/trails.geojson`), `fetch_douglas.py` + `enrich_douglas.py` (→ `research.json`), `check_ridb.py` (→ `v2/ridb-options.json`).
- The study area is a single hard-coded rectangle (`config/aoi.geojson`, ~1,198 km² around Aspen).

### What the data actually contains today

| Dataset | Features | Notes |
|---|---|---|
| Aspen land | 3 polygons | USFS 86.8%, "Private" 13.1%, BLM 0.1% of the AOI |
| Aspen wilderness | 3 | 65.4% of the AOI |
| Aspen MVUM roads | 54 | evaluated for Sep 25–26 2026, high clearance |
| Aspen hydrology | 6,926 | 6,411 flowlines, 514 waterbodies, 1 area; 1,555 named |
| Aspen research polygons | 51 | 6.7 km² |
| Aspen trails (USFS) | 123 segments | 87 trail numbers; 25 segments cut at the AOI edge |
| Aspen camping | 5 curated + 4 RIDB (6 after dedupe) | plus 1 lodging backup |
| Douglas trails / roads | 102 / 73 | USFS only |
| Douglas recreation sites | 36 | 5 campgrounds, 17 trailheads, 14 other |
| Douglas water | 33 waterbodies, 2,359 stream segments | named only, 69 distinct stream names |
| Douglas land | 5 polygons | PVT 71.8%, USFS 26.1%, LG 0.9%, OTHFE 0.7%, ST 0.5% |
| Restrictions, leads, reviewed sites, wildlife | 0 | fire is one geometry-less monitor record |

---

## 2. What v2 already does well (preserve these)

1. **Epistemic discipline.** "Unknown stays unknown" is enforced in code, not just copy: `camping_permission: "unknown"` everywhere, generated areas can never validate as approved, synthetic campsite pins are prohibited by the validator, a page hash never becomes a fire stage.
2. **Provenance on every feature.** Source URL, agency, retrieval time, confidence, verification method. Derived geometry carries its inputs.
3. **Three separate status dimensions** (transport / interpretation / freshness) in `docs/data-contract.md`, with the browser re-ageing data on load.
4. **Robust ArcGIS retrieval.** ID-set completeness checks, transfer-limit splitting, HTTP-200-error retries, ring-order-independent polygon conversion with hole preservation.
5. **Atomic publication.** Staging directory, validate, then `os.replace`; failures never leave a partial bundle.
6. **Correct metric geometry.** Explicit feet→metres, projected buffering, and a test that measures buffers independently with geodesic distance.
7. **Exploration separated from trip evaluation.** Trip filters never hide map geometry; roads are styled neutrally; research polygons are labelled as a dated snapshot.
8. **Layer observability.** Each layer shows loaded count, "not loaded" vs "empty" vs "source failed", and fetch date.
9. **Original source strings retained.** MVUM and trail date windows are stored verbatim rather than collapsed to booleans.
10. **Honest proximity language.** "Straight-line to a mapped segment, not a trailhead or route."
11. **A meaningful offline test suite** (35 Python tests plus Node tests) covering the trust rules above.
12. **Careful output escaping and URL protocol checks** in both UIs; the Douglas UI builds DOM with `textContent`.
13. **Accessibility basics.** Native `<dialog>`, 44 px targets, `aria-pressed`, reduced-motion handling.

---

## 3. Technical debt and risks, ranked

### Critical

**C1. Land classification presents "non-federal" as "Private".**
- The only land source is BLM SMA *limited-scale*. In the Aspen AOI it returns three classes covering 100% of the area with no State or Local land at all. Everything that is not USFS/BLM is labelled `Private` — which necessarily includes City of Aspen, Pitkin County open space, CDOT and any state holdings.
- Douglas shows the same pattern: 71.8% PVT, 0.9% local, 0.5% state, in a county with large county open space and three state parks. I did not verify individual parcels; this needs a spot check against a parcel source, but the direction of the error is clear.
- The Douglas legend states "gray = private" as fact. The dataset cannot support that.
- `land_class` is hard-coded to `"unknown"` and never used. There is no notion of classification confidence or source scale in the data model.

**C2. The Aspen map draws private and public land in the same colour.**
- `app.js:142` applies one style per layer, so the USFS, BLM and "Private" polygons all render as the same green under the title "Land management". The manager is only visible after tapping. A user reading the map sees 100% green.

**C3. Research polygons depend on that same generalized land layer.**
- Step 07 treats "USFS or BLM" in limited-scale SMA as "possibly campable" and has no explicit private-inholding subtraction. Overlap with the SMA "Private" polygon is zero by construction (measured: 0.8 m²), but patented mining claims and small inholdings — common in the Lincoln Creek and Castle Creek corridors — are below the resolution of this source.
- The test named `test_candidate_excludes_adjacent_wilderness_water_and_private` contains no private polygon; it does not test what its name says.
- Corridors are also frozen to one trip (Sep 25–26 2026, high clearance). Only roads designated open for that trip produce polygons.

### High

**H1. No automated verification runs anywhere.**
- Neither test suite runs on push or PR. The only installed workflow is a manual RIDB export. The two workflows that would run tests live in directories GitHub ignores (`v2/pipeline/github-workflows/`, `v2/pipeline/.github/workflows/`).
- Combined with legacy Pages on an unprotected `main`, any push is an unreviewed production deploy.
- `AGENTS.md` tells agents to run `.venv/bin/python -m pytest`; pytest is not in `requirements.txt`.

**H2. Two apps, two data contracts.**
- Aspen: `map-data-v2.json` (schema v2, validated, layers named after pipeline steps). Douglas: `research.json` (schema v1, no validation, different layer names, different land vocabulary — `Private`/`State_CO` vs raw `PVT`/`ST`).
- Activity labels are defined twice. Date-window parsing exists three times with different rules (JS `TripRules`: strict `MM/DD-MM/DD`; JS `DouglasDiscovery`: 1–2 digits, en dash; Python `access.py`: also accepts "yearlong").
- Every future feature (water, trails, land) must currently be built twice.

**H3. The pipeline is hard-wired to Aspen.**
- One AOI file, `ASPEN_*` environment variables, a fixed UTM zone, a 35-mile RIDB radius from the AOI centroid, a `fetch_douglas.py` that is a copy-and-adapt rather than a parameterised region.
- Colorado west of 108°W is UTM zone 12; other states need other zones. The buffer error from using zone 13 there is small, but the pattern does not generalise.

**H4. Trip-specific evaluation is baked into published static data.**
- The bundle carries one `trip`; roads carry `access_status` for that trip; corridors exist only for it. The app has to explain that the polygons are "not an assessment of your selected trip". The raw designations needed to evaluate client-side are already in the data.

**H5. Mobile payload and main-thread cost.**
- ~12 MB of JSON per Aspen visit, re-downloaded every time (`no-store`). Pages gzips, but parse cost is on the phone.
- 5,371 of 6,926 hydrology features (most of 7.7 MB) are downloaded and never drawn; they exist only for pipeline screening.
- Identical evidence objects are repeated on every feature: 1.9 MB of the 10 MB.
- Coordinates carry 14–15 decimal places; 6 would do.
- Popup HTML is built eagerly for every feature at load (~1,800 popups; each trail popup computes distance to every place).
- `setInterval(render, 60000)` rebuilds the list, detail panel and all markers every minute, resetting open `<details>`, scroll and focus.

**H6. Staleness masks hard conflicts.**
- In `TripRules.evaluate`, the 30-day staleness check returns before the tent-only, clearance and season checks. After 2026-10-24 every curated place flips to "Source review is stale" with status `review`, and Silver Bar (tent-only) and the out-of-season roads stop being reported as conflicts. Known disqualifiers should outrank staleness.
- More generally nothing refreshes data: RIDB inventory goes stale on Oct 2, Douglas on Oct 4, curated places on Oct 24, the Lincoln Creek rule on Oct 25.

**H7. Water has no attributes to classify with.**
- Step 03 keeps only `id`, `kind`, `name`. NHD's feature type/code (perennial vs intermittent vs ephemeral, artificial path, canal/ditch), GNIS ID, reach code, area and length are discarded.
- The "named only" display filter is the only lever, and it is wrong in both directions: it hides unnamed lakes up to 54.6 acres, and it keeps every named intermittent gulch.
- Rivers are drawn as reach fragments (Roaring Fork = 112 features, each with its own popup). 361 of 514 waterbodies are under one acre.

### Medium

- **M1. Trails are fragments.** Clipped at the AOI/county line (25 of 123 Aspen segments), not dissolved by trail number, USFS-only. No COTREX; the licence question raised in `TRAIL-PILOT.md` is unresolved. No trailheads in Aspen.
- **M2. Camping inventory has three parallel paths.** `overnight-options.json` (hand-curated), `ridb-options.json` (`check_ridb.py`), and the bundle's `lodging_developed`/`site_feed` (pipeline step 04, empty and unused by the app). Dedupe is by RIDB facility ID only. The campground gate is a name regex that drops legitimately named dispersed listings (documented for Rampart).
- **M3. Mixed-geometry clip results.** `clip_geometry` can return a `GeometryCollection` (line touching the boundary). The bundle schema rejects that type, so a required step would fail the whole run; `fetch_trails.normalize` silently drops such a trail instead.
- **M4. Tracked duplicates.** `map-data-v2.json` twice (10 MB each), legacy `map-data.json` twice (0.5 MB each; only a download link uses it), Leaflet twice, `ridb-check.yml` twice, root `d3.min.js` (280 KB, unreferenced).
- **M5. Runtime coupling to pipeline paths.** The app fetches `./pipeline/config/rules-registry.json` and `aoi.geojson`. Moving the pipeline breaks the site.
- **M6. Basemap terms.** The Douglas page uses Esri World Imagery and `tile.openstreetmap.org` directly. Both have usage policies that should be confirmed before wider traffic. The v2 page uses USGS, which is fine.
- **M7. Doc drift.** `data-contract.md` says the browser hides trip-specific layers (it no longer does). READMEs are changelogs with zip-upload instructions. Counts in docs (18/28/32 tests) lag the actual 35. `USER_AGENT` and the default lead source URL point at a non-existent `aspen-overnight` site.
- **M8. CSS is patch-on-patch.** `v2/styles.css` has seven successive `@media (max-width:760px)` blocks, later ones overriding earlier ones. Hard to reason about when redesigning mobile.
- **M9. Hard-coded region UI.** The mountain `<select>` duplicates `destinations.json`; "Aspen" strings are in HTML.

### Low

- `.gitignore` ignores `data/raw/*` but `ridb-import-2026-09-25.json` is tracked there; root and nested ignore files duplicate each other.
- Manual `?v=` cache-busting on scripts while JSON is `no-store`.
- Unpinned dependency ranges; no lock file.
- No error reporting or usage telemetry of any kind (a deliberate privacy stance, but it means field failures are invisible).

---

## 4. Gap analysis against the product vision

| Vision | Today | Gap |
|---|---|---|
| **Choose Your Adventure**: state, dates, activities, camping prefs, vehicle | One hard-coded area, four ski mountains, one activity, vehicle only affects camping cards | No state/region selection; no destination concept beyond ski bases; trail seasons not evaluated against dates in v2 (they are in Douglas); results are camp-centric proximity lists |
| **Explore map**, mobile-first | Works; sheet peeks at ~13% | Two different Explore UIs; five overlay regions on a phone (top bar, two floating buttons, basemap/fit row, peek sheet, attribution); all 12 layers on by default; no search; no viewport-based loading |
| **Functional recreational water** | Named NHD features | No attributes retained, so no perennial/intermittent distinction, no size threshold, no lake/reservoir vs pond, no activity evidence (fishing, paddling, swimming), fragments not dissolved |
| **Trails**, COTREX for Colorado | USFS segments in two small areas | No COTREX, no non-USFS trails, no trailheads in v2, clipped fragments, no source-adapter abstraction, activity vocabulary lacks e-bike/OHV classes |
| **Camping** | 6 Aspen listings, 5 Douglas campgrounds, 1 unmapped dispersed area | No unified camp model (developed / designated dispersed / dispersed area), no statewide inventory, vehicle/access constraints only for 5 curated places |
| **Land** accuracy | One generalized national layer | No authoritative public-land source, no state/local distinction that can be trusted, no confidence model, "private" asserted by default |
| **Other states later** | Aspen constants throughout | Region is code, not configuration |

---

## 5. Recommended target architecture

Keep it static-first. Nothing in the vision needs a server until there are accounts or community content.

### Principles

1. **One app, many regions.** A region is data plus configuration, never a fork of the UI.
2. **One data contract.** Every region publishes the same layer types with the same field vocabulary.
3. **Static data is trip-independent.** Dates and vehicle are evaluated in the browser from stored designations.
4. **Classification carries its confidence.** A land or water class is a claim with a source, a scale and a confidence. The UI may only render it as authoritative above a stated threshold; everything else renders as unknown.
5. **Screening data and display data are different products.** The browser gets display data only.

### Layout

```
app/                    single static shell (HTML, CSS, ES modules, vendored map lib)
data/regions/<id>/      manifest.json + one file per layer
pipeline/
  sources/              one adapter per authoritative source (usfs_trails, cotrex, nhd, padus, ridb, mvum…)
  regions/<id>.yaml     boundary, CRS, enabled sources, thresholds
  contract/             JSON Schemas for manifest and each layer type
  tests/
.github/workflows/      ci.yml, deploy.yml, refresh-*.yml
```

### Region manifest

One small file per region the app loads first: region id, name, bbox, and per layer `{id, type, url, format, feature_count, schema_version, source: {name, url, licence, retrieved_at}, confidence}`. Provenance moves to the layer level, with per-feature overrides only where a feature differs. This removes the 1.9 MB of repetition and lets the app lazy-load layers when toggled or in view.

### Domain model (minimum useful fields)

- **Land**: `owner_class` (federal | state | local | tribal | private | unknown), `manager`, `designation`, `public_access` (open | restricted | closed | unknown), `source`, `source_scale`, `confidence`.
- **Water**: `class` (lake | reservoir | river | stream), `name`, `gnis_id`, `permanence`, `size`, `recreation` (evidence-backed activity flags, default unknown). One feature per named water, not per reach.
- **Trail**: `source`, `source_id`, `name`, `number`, normalized `activities` (allowed | seasonal | prohibited | unknown, with the raw string kept), `length`. Whole trails, not clipped fragments; trailheads as their own layer.
- **Camp**: `type` (developed | designated_dispersed | dispersed_area), `source`, `source_id`, `reservable`, `vehicle_constraints`, `season`, each with status and evidence.
- **Restriction**: geometry, type, effective dates, jurisdiction, evidence (already well specified in `curation.md`).

### Sources by layer

| Layer | Primary | Notes |
|---|---|---|
| Land | USGS PAD-US (manager type, manager name, public-access field) | National, public domain. SMA limited-scale becomes fallback context only. County parcels are a later, per-county decision with licence review. |
| Water | USGS NHD with attributes retained | Classify by feature code, size and name. Activity evidence from agency sources later. |
| Trails | USFS EDW nationally; COTREX for Colorado | COTREX needs written reuse confirmation from CPW first — start that conversation now, it is the long pole. |
| Camping | RIDB + USFS recreation sites + curated | One merge step with source precedence and cross-source ID matching. |
| Roads | USFS MVUM, BLM routes later | Keep raw designations; evaluate in browser. |

### Rendering

- Move the unified shell to **MapLibre GL JS** (vendored, still no build step). It handles these GeoJSON sizes far better than Leaflet canvas and gives data-driven styling and zoom-dependent filtering, which both water and land need.
- When coverage goes statewide, switch layer sources from GeoJSON to **PMTiles** on the same static host. The app code barely changes; the manifest's `format` field does.
- Do this once, at the shell-unification milestone, rather than redesigning mobile Explore on Leaflet and again later.

### Delivery

- Pages deploy via a GitHub Actions workflow that publishes only the site directory, gated on CI. The pipeline source stops being part of the public site.
- Branch protection on `main` requiring CI.
- Refresh workflows stay manual until source coverage justifies a schedule.

### Deliberately not recommended yet

A backend or database, a JS framework, a bundler, user accounts, routing/navigation, paid parcel data, scheduled AI loops.

---

## 6. Next five milestones (dependency order)

Kick off in parallel, outside the code: **ask CPW for written COTREX reuse terms.** It gates the trail milestone that follows these five and may take weeks.

### Milestone 1 — Verification baseline and repo hygiene

- **Objective:** every PR is checked automatically (Python tests, Node tests, JS syntax, published-data validation); duplicated and dead artifacts that make later work ambiguous are removed. No user-visible change.
- **Why now:** the Claude → Codex → Claude loop needs an objective gate. Today no test runs anywhere and every push to `main` deploys.
- **Affected:** `.github/workflows/`, `v2/pipeline/tests/`, `.gitignore`, `AGENTS.md`, a few doc lines, removal of the duplicate bundle and stray workflow copies.
- **Dependencies:** none.
- **Acceptance:** CI green on the PR; a deliberately corrupted data file fails CI; exactly one tracked `map-data-v2.json`; workflows exist only under root `.github/workflows/`; app files byte-identical.
- **Risks:** Node tests have not been run recently and may fail on first run; removing the duplicate bundle changes where a pipeline run's output is picked up from.

### Milestone 2 — Region data contract and pipeline parameterisation

- **Objective:** Aspen and Douglas publish the same manifest + per-layer files under one schema; pipeline takes a region config; static data carries no trip; hydrology for screening is no longer shipped to the browser; land features carry `owner_class`, `source_scale`, `confidence`, and the rule "render only what the source can support, otherwise unknown" is implemented in both UIs (this fixes C2 and the Douglas "gray = private" claim).
- **Why now:** every later feature would otherwise be built twice on shapes that are about to change.
- **Affected:** all pipeline scripts and `lib/`, schema, both frontends' loaders, tests, data files.
- **Dependencies:** M1.
- **Acceptance:** one schema validates both regions in CI; no `ASPEN_*` names remain; Aspen first-load JSON under 3 MB uncompressed; both UIs functionally unchanged except land styling and the removal of trip-frozen status; one shared date-window fixture passes in Python and JS; staleness no longer masks hard conflicts (H6).
- **Risks:** largest refactor of the five; live sources may be unavailable during regeneration (BLM and USGS both failed on Sep 24) — the migration must be able to transform existing snapshots offline.

### Milestone 3 — One mobile-first Explore shell

- **Objective:** a single app serving any region from its manifest, on MapLibre, with a compact mobile layout: one search/filter bar, one layers control, a small peek sheet, details on tap. Sensible default layers instead of everything on. Lazy layer loading. Douglas features (trailheads, season badges, GPX, saved items) become general features. The legacy root site and the Douglas fork are retired.
- **Why now:** it is the stated top product priority, and after M2 it can be built once.
- **Affected:** all of `v2/*.js|html|css`, `v2/regions/`, root legacy site.
- **Dependencies:** M2.
- **Acceptance:** at 390×844 the map occupies at least 80% of the viewport in the default state with at most three persistent controls; time-to-interactive measured on a mid-range phone profile is recorded and under an agreed budget; both regions reachable from one URL; every trust message present today is still reachable; no horizontal overflow at 320 px.
- **Risks:** renderer change is a rewrite of map code; parity with the existing trust copy is easy to lose; needs real-device testing that cannot be done from here.

### Milestone 4 — Functional recreational water

- **Objective:** a display-water product built from NHD attributes: lakes and reservoirs above a size threshold (named or not), rivers and perennial named streams, dissolved to one feature per water; drainage, ephemeral and artificial paths, ditches and sub-threshold ponds excluded. Recreation flags exist in the schema and default to unknown. The screening hydrology used for setbacks is untouched.
- **Why now:** second stated product priority; needs the contract (M2) for the split between display and screening, and the shell (M3) for zoom-dependent styling.
- **Affected:** hydrology source adapter, water layer schema, water styling, tests.
- **Dependencies:** M2, M3.
- **Acceptance:** agreed fixture list of waters that must appear (e.g. Roaring Fork River, Snowmass Lake, Grizzly Reservoir, the 54.6-acre unnamed lake) and must not appear (named intermittent gulches, sub-acre ponds); Roaring Fork is one feature; setback geometry before/after is identical.
- **Risks:** NHD feature codes are inconsistent between regions; thresholds need tuning per terrain (alpine vs plains); "useful for fishing/paddling" cannot be inferred from hydrography and must not be implied.

### Milestone 5 — Land classification v1

- **Objective:** PAD-US as the primary public-land source with manager, designation and public-access fields; SMA demoted to fallback; explicit `unknown` wherever no authoritative source covers; private shown only where a source positively asserts it. Research-polygon generation switches to the new layer and gains a real private-exclusion test.
- **Why now:** it is the highest trust risk, and dispersed-camping work depends on it. M2 already stops the UI from overstating; this replaces the source. It follows water only because water is the faster visible win once the shell exists — swap M4 and M5 if camping is the nearer goal.
- **Affected:** land source adapter, land schema, corridor step, legend, tests.
- **Dependencies:** M2 (schema), M3 (styling).
- **Acceptance:** a spot-check list of known parcels in both regions (county open space, state parks, a known inholding) classified correctly or as unknown — never as the wrong class; legend distinguishes federal / state / local / private / unknown; no polygon is labelled private solely by absence of other data.
- **Risks:** PAD-US has its own gaps and lag; conflicts between PAD-US and SMA need a documented precedence rule; parcel-level truth still requires county data.

**After these five:** trail source adapters and COTREX (pending licence), unified camping inventory, then Choose Your Adventure rebuilt on real region/activity/destination relationships.

The detailed specification for Milestone 1 is in `M1-spec.md`.
