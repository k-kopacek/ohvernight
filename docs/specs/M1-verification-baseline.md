# Milestone 1 specification — Verification baseline and repo hygiene

**For:** Codex (implementation). **Reviewer:** Claude. **Base:** `main` at `9388845`.
**Branch:** `chore/m1-verification-baseline`. Open a PR; do not push to `main`.

## Goal

After this milestone, every pull request is automatically checked by the offline Python tests, the Node tests, a JavaScript syntax check and a validation of the published data files. Duplicate and dead artifacts that would make later milestones ambiguous are removed.

**There must be no user-visible change.** The deployed site must behave identically before and after.

## Background facts (verified 2026-10-01)

- GitHub Pages uses the legacy build from `main` at `/`. Every push to `main` deploys the whole repository.
- The only installed workflow is `.github/workflows/ridb-check.yml` (manual dispatch).
- `python -m unittest discover -s v2/pipeline/tests` runs 35 tests, all passing, in under a second, with no network access.
- The Node tests have not been run in this audit (Node was unavailable). Treat their status as unknown.
- `v2/map-data-v2.json` passes `lib.validation.validate_bundle`.
- `v2/map-data-v2.json` and `v2/pipeline/data/processed/map-data-v2.json` are byte-identical, 10,086,079 bytes each, both tracked.
- `.github/workflows/ridb-check.yml` and `v2/pipeline/github-workflows/ridb-check.yml` are byte-identical.

## Owner decisions (defaults apply unless the owner says otherwise before work starts)

| # | Decision | Default |
|---|---|---|
| D1 | Stop tracking `v2/pipeline/data/processed/map-data-v2.json` | Yes. `v2/map-data-v2.json` is the single tracked copy. |
| D2 | Install `refresh-map.yml` as a real (manual-dispatch) workflow | Yes. It has `contents: read` and only uploads an artifact. |
| D3 | Delete `v2/pipeline/.github/workflows/refresh-data.yml` | Yes. GitHub ignores it, its paths are wrong for this repo, and it requests `contents: write`. |
| D4 | Node version for CI | 22 |

Items D1 and D3 delete tracked files. `AGENTS.md` requires explicit approval for deletions; approval of this spec is that approval, for these named files only.

## In scope

### 1. CI workflow

Create `.github/workflows/ci.yml`.

- Name: `CI`.
- Triggers: `pull_request` (all branches) and `push` to `main`.
- `permissions: contents: read`.
- `concurrency`: group `ci-${{ github.ref }}`, `cancel-in-progress: true`.
- No secrets. No step may contact a data source (RIDB, ArcGIS, USGS, etc.).
- Each job: `runs-on: ubuntu-latest`, `timeout-minutes: 10`.

Job `python`:
1. `actions/checkout@v4`
2. `actions/setup-python@v5` with `python-version: '3.12'`, `cache: pip`, `cache-dependency-path: v2/pipeline/requirements.txt`
3. `pip install -r v2/pipeline/requirements.txt`
4. `python v2/pipeline/scripts/00_selftest.py`

Job `node`:
1. `actions/checkout@v4`
2. `actions/setup-node@v4` with `node-version: '22'`
3. Syntax check. Run `node --check` on each of these and fail on any error:
   `v2/app.js`, `v2/map-layers.js`, `v2/trail-discovery.js`, `v2/trip-rules.js`, `v2/trust.js`, `v2/regions/douglas-co/preview.js`, `v2/regions/douglas-co/discovery.js`, `app.js`, `trip-rules.js`
4. `node --test v2/pipeline/tests/*.test.cjs` (shell-expanded glob; do not pass the directory).

If any existing Node test fails on first run, **do not edit application code to make it pass.** Stop, report the failure output in the PR description, and wait for review.

### 2. Published-data validation tests (Python)

Create `v2/pipeline/tests/test_published_data.py`. Use `unittest`, consistent with the existing suite. Resolve paths from `Path(__file__).resolve().parents[2]` (the `v2` directory). Tests must be offline and must not write any file.

Add a small shared helper inside the test module that, for a GeoJSON geometry, asserts: it builds with `shapely.geometry.shape`, is non-empty and valid, and its bounds lie within longitude ±180 and latitude ±90.

Required test cases:

**a. Aspen bundle**
- `v2/map-data-v2.json` loads and `lib.validation.validate_bundle(bundle)` does not raise.

**b. Aspen trails** (`v2/trails.geojson`)
- `type == "FeatureCollection"`; `features` is a non-empty list.
- Every `properties.id` is a non-empty string and unique.
- Every geometry type is `LineString` or `MultiLineString` and passes the geometry helper.
- Every geometry lies within the bounds of `v2/pipeline/config/aoi.geojson` expanded by 1e-6 degrees.
- Every `properties.activities` has exactly the key set of `fetch_trails.ACTIVITIES`, and each value has exactly the keys `managed`, `accpt`, `disc`, `restricted`, each `None` or a string.
- Every `properties.evidence` has `source_url` starting with `http://` or `https://`, a non-empty `agency`, and a `retrieved_at` string.

**c. Douglas snapshot** (`v2/regions/douglas-co/research.json`)
- `region == "douglas-co"` and `schema_version == 1`.
- `layers` contains exactly these keys: `coverage`, `trails`, `roads`, `recreation`, `land`, `wilderness`, `waterbodies`, `waterways`. Each is an object with a `features` list.
- `coverage` has exactly one feature with `properties.GEOID == "08035"`.
- Across all layers except `coverage`, every feature has a non-empty string `properties.id`, and IDs are globally unique.
- Every non-null geometry passes the geometry helper and lies within the coverage feature's bounds expanded by 1e-6 degrees.
- Geometry types: `trails`, `roads`, `waterways` are `LineString`/`MultiLineString`; `land`, `wilderness`, `waterbodies` are `Polygon`/`MultiPolygon`; `recreation` is `Point`.
- Every `land` feature has a non-empty string `properties.manager`.
- Every `trails` feature's `activities` has the same key set as in (b).
- Every feature outside `coverage` has `properties.evidence.source_url` starting with `http`.

**d. Place inventories** (`v2/overnight-options.json`, `v2/ridb-options.json`)
- Each has `schema_version == 1` and a list `places`.
- Within each file, every `id` matches `^[a-z0-9_-]+$` and is unique.
- Every `coordinates` is `[lon, lat]`, both finite, lon within ±180, lat within ±90.
- Every `kind` is one of `campground`, `dispersed`, `lodging`.
- Every `source` and `mapSource` parses as a URL with scheme `https` or `http`.
- Every place in `ridb-options.json` has `camping_permission == "unknown"`, `needs_review is True`, and a non-empty `ridb_facility_id`.
- `checked_on` matches `YYYY-MM-DD` and parses as a real date.

**e. Rules registry** (`v2/pipeline/config/rules-registry.json`)
- Every ID in every rule's `place_ids` either exists in the union of place IDs from the two inventories in (d), or matches `ridb-<id>` where `<id>` equals the `ridb_facility_id` of an existing inventory place.
- Every rule has `camping_permission == "unknown"`.

**f. Destinations** (`v2/destinations.json`)
- `resorts` is a non-empty list; IDs unique; coordinates valid as in (d).

Do not assert specific feature counts. Snapshots change on refresh; these tests guard structure and trust invariants, not volume.

### 3. Vocabulary parity test (Node)

Create `v2/pipeline/tests/published-data.test.cjs` using `node:test` and `node:assert/strict`.

- Load `../../trail-discovery.js` and `../../regions/douglas-co/discovery.js`.
- Assert the sorted keys of `TrailDiscovery.activities` equal the sorted keys of `DouglasDiscovery.activities`.
- Load `../../trails.geojson` and `../../regions/douglas-co/research.json`. Assert the sorted activity keys of the first trail feature in each equal that same key list.

### 4. Single tracked copy of the bundle (D1)

- `git rm v2/pipeline/data/processed/map-data-v2.json`.
- In the root `.gitignore`, delete the line `!v2/pipeline/data/processed/map-data-v2.json` and reword the comment above that block so it no longer says the processed bundle is kept. State instead that `v2/map-data-v2.json` is the tracked public copy.
- Do not change `run_pipeline.py`. It continues to write to `data/processed/`, which is now fully ignored apart from `.gitkeep`.
- In `v2/pipeline/README.md`, section "Outputs and publication", add one sentence: after a validated run, copy `data/processed/map-data-v2.json` to `v2/map-data-v2.json` to publish it; the processed copy is not tracked.

### 5. One ignore file

- Delete `v2/pipeline/.gitignore`. Its rules are already covered by the root `.gitignore`. Before deleting, confirm each of its patterns has an equivalent in the root file and list any that did not in the PR description.
- The file `v2/pipeline/data/raw/ridb-import-2026-09-25.json` is tracked but matches an ignore pattern. Add `!v2/pipeline/data/raw/ridb-import-*.json` to the root `.gitignore` directly under the existing `!v2/pipeline/data/raw/.gitkeep` line, with a comment: "Reviewed import audit copies are kept deliberately."
- After the change, `git status --ignored` must not list any currently tracked file as ignored, and `git ls-files -ci --exclude-standard` must print nothing.

### 6. One location for workflows (D2, D3)

- `git mv v2/pipeline/github-workflows/refresh-map.yml .github/workflows/refresh-map.yml`. In that file, replace the step `python -m unittest discover -s v2/pipeline/tests` with `python v2/pipeline/scripts/00_selftest.py` so CI and this workflow run tests the same way. Change nothing else in it.
- `git rm v2/pipeline/github-workflows/ridb-check.yml` (identical to the installed copy). The `v2/pipeline/github-workflows/` directory must no longer exist.
- `git rm v2/pipeline/.github/workflows/refresh-data.yml`. The `v2/pipeline/.github/` directory must no longer exist.
- Do not modify `.github/workflows/ridb-check.yml`.
- Update the text that points at the removed locations:
  - `v2/README.md`, sections "Connect RIDB once" and "Build the map bundle": replace the copy-the-template instructions with a statement that both workflows are installed under `.github/workflows/` and are run from the Actions tab. Remove the sentence about "the legacy `.github` file inside that folder".
  - `v2/LAYER-CHECK.md`: the sentence naming `pipeline/github-workflows/ridb-check.yml` as the bundled template should name only `.github/workflows/ridb-check.yml`.
  - `v2/pipeline/README.md`, section "GitHub workflow": replace the first sentence with "Pull requests and pushes to `main` run the offline regression suite through `.github/workflows/ci.yml`." Replace "A completed refresh commits only the public bundle" with "A completed refresh uploads the bundle as a workflow artifact; it does not commit or deploy."

### 7. Correct the agent instructions

In `AGENTS.md`, replace the "Verification" code block and its lead-in with instructions that work on a clean checkout:

```sh
# from the repository root, Python 3.12+ and Node 22+
python3 -m venv v2/pipeline/.venv
v2/pipeline/.venv/bin/pip install -r v2/pipeline/requirements.txt
v2/pipeline/.venv/bin/python v2/pipeline/scripts/00_selftest.py
node --test v2/pipeline/tests/*.test.cjs
```

Remove the `pytest` reference (pytest is not a declared dependency). Add one sentence: "CI runs the same commands on every pull request; a PR must be green before merge." Add one sentence under "Repository map": "GitHub Pages publishes the whole repository from `main`; merging to `main` is a production deploy."

Add a `.nvmrc` at the repository root containing `22`.

### 8. Small accuracy fixes

- `v2/pipeline/docs/data-contract.md`: the sentence "The browser hides trip-specific layers when dates or vehicle differ." is no longer true. Replace it with: "The browser keeps roads and research areas visible for every trip, styles roads neutrally, and labels research areas with the trip they were screened for."
- `v2/pipeline/scripts/lib/arcgis_client.py`: change `USER_AGENT` to `"ohvernight-data/0.2 (+https://github.com/k-kopacek/ohvernight)"`.
- `v2/pipeline/scripts/08_ingest_leads.py`: change the fallback source URL from `https://github.com/k-kopacek/aspen-overnight` to `https://github.com/k-kopacek/ohvernight`.

## Out of scope (do not do these)

- Any change to `v2/app.js`, `v2/map-layers.js`, `v2/trail-discovery.js`, `v2/trip-rules.js`, `v2/trust.js`, `v2/index.html`, `v2/styles.css`, or anything under `v2/regions/douglas-co/`.
- Any change to the content of a data file (`*.json`, `*.geojson`) other than removing the duplicate bundle.
- Any change to the root legacy site, including removing `d3.min.js`.
- Renaming `ASPEN_*` variables, restructuring directories, or changing schemas (Milestone 2).
- Adding linters, formatters, type checkers, a bundler, `package.json`, or a dependency lock.
- Running any live fetch (`run_pipeline.py`, `fetch_*.py`, `enrich_douglas.py`, `check_ridb.py`).
- Changing GitHub repository settings.
- Fixing the known issues listed in the audit (land styling, staleness ordering, payload size). They are scheduled for later milestones.

## Commit structure

Separate commits, in this order, so each can be reviewed or reverted alone:

1. `test: validate published data files and activity vocabulary`
2. `ci: run offline Python and Node checks on pull requests`
3. `chore: keep a single tracked map bundle and one ignore file`
4. `ci: consolidate workflows under .github/workflows`
5. `docs: correct verification commands and stale statements`
6. `chore: fix stale project identifiers in pipeline`

## Acceptance criteria

1. The PR shows two CI checks, `python` and `node`, both passing.
2. `python v2/pipeline/scripts/00_selftest.py` reports at least 41 tests (35 existing plus at least six new test cases), all passing.
3. Negative proof, done locally and **not committed**: temporarily duplicate one feature's `id` in `v2/trails.geojson`, show that the Python suite fails with a message naming the duplicate, then restore the file. Paste the failing output in the PR description.
4. `git ls-files | grep -c 'map-data-v2.json'` prints `1`.
5. `git ls-files | grep -E 'workflows/'` prints exactly:
   `.github/workflows/ci.yml`, `.github/workflows/refresh-map.yml`, `.github/workflows/ridb-check.yml`.
6. `git ls-files -ci --exclude-standard` prints nothing.
7. `git diff --stat main...HEAD -- v2/app.js v2/map-layers.js v2/trail-discovery.js v2/trip-rules.js v2/trust.js v2/index.html v2/styles.css v2/regions v2/map-data-v2.json v2/trails.geojson v2/overnight-options.json v2/ridb-options.json v2/destinations.json app.js index.html styles.css trip-rules.js` prints nothing.
8. The commands in the new `AGENTS.md` verification block run successfully, verbatim, on a fresh clone.
9. CI uses no secrets and completes in under three minutes.

## Edge cases and risks to handle

- **Node tests may fail on first run.** They have not been executed in this audit. Follow the stop-and-report rule in section 1.
- **`trust.test.cjs` is a plain script, not a `node:test` file.** `node --test` treats a zero exit as a pass; leave the file as it is.
- **`map-layers.test.cjs` reads the real bundle and trail file.** It will break if a future data refresh empties a layer. That is acceptable for now; do not loosen it.
- **Geometry helper performance.** `research.json` is 6 MB with about 2,600 features; validating with Shapely takes well under a second. Do not add sampling.
- **Path resolution.** New tests must work when run from the repository root (CI) and from `v2/pipeline/` (local). Use paths relative to `__file__`, never the working directory.
- **`.gitignore` negation order.** A negation only works after the pattern it overrides. Verify with acceptance criterion 6.
- **The duplicate bundle removal** shrinks the working tree, not the history. Do not rewrite history.

## Handoff back to review

Per `AGENTS.md`, the PR description must state: what changed; what was deliberately left alone; which checks ran and their output (including the Node test output, since this is its first recorded run); and any remaining uncertainty.

## Owner follow-up after merge (not for Codex)

Enable branch protection on `main` requiring the `python` and `node` checks. Until that is on, CI reports but does not gate, and any push still deploys.
