# M4-B implementation blueprint

Prepared by the coordinator while M4-A awaited merge approval, so that M4-B
can be dispatched as soon as the owner answers the open decisions. It adds no
rule. The approved specification
([M4-functional-recreational-water.md](../../../specs/M4-functional-recreational-water.md))
governs; this file turns it into an execution plan and a draft brief.

M4-B must not start until: PR #12 (M4-A) is merged; and the owner has decided
the South Platte rule, connector handling, extent-edge behaviour, the size
threshold, the layer titles and the source-scope wording. Where a step
depends on a decision it is marked **[D-n]** and the draft brief carries a
placeholder.

## 1. Decisions M4-B waits on

| ID | Decision | Packet | Effect on the plan |
|---|---|---|---|
| D-1 | South Platte / centre lines through areas | [south-platte.md](../decision-packets/south-platte.md) | May add a Douglas area layer, one more controlled NHD request, a rule amendment and a Douglas water padding. Adds a step 0 |
| D-2 | Connectors with the river's own GNIS id | [connectors.md](../decision-packets/connectors.md) | One line in the grouping rule; two more tests |
| D-3 | Extent-edge splitting | [extent-edge.md](../decision-packets/extent-edge.md) | Accept (no change) or fetch padded geometry for connectivity (adds to step 0) |
| D-4 | Size threshold | [threshold.md](../decision-packets/threshold.md) | One number in `water_display.json`, or an inclusion rule |
| D-5 | Layer titles | section 6 below | Two strings in each `explore.json` |
| D-6 | Source-scope sentences | [source-scope-wording.md](../decision-packets/source-scope-wording.md) | Two strings in two manifests |

## 2. Corrections the real data makes to the specification's estimates

To be recorded as a coordinator amendment (A4) when M4-B starts.

| Specification says | M4-A data shows |
|---|---|
| About 62 and 56 stream groups | 71 (Aspen) and 35 (Douglas) |
| Roaring Fork `member_count` example 96 | 111 |
| 42 and 37 waterbodies at 2 ha | 46 and 32 |
| South Platte has an 80 m perennial stream segment in Douglas | It has none inside the county |
| Group `length_km` is the sum of members' source `length_km` | Source length is unclipped and overstates rivers at the edge; compute from drawn geometry (proposed clarification) |

## 3. Files expected to change

| File | Change |
|---|---|
| `v2/pipeline/scripts/lib/water.py` | Eligibility (8.2); grouping (8.3); group IDs; selection report |
| `v2/pipeline/scripts/build_display.py` | `display.select` (`streams`, `bodies`); grouped display features; `water_groups`; aliases to group IDs; richer waterbody display properties; `--report` |
| `v2/pipeline/scripts/lib/region_contract.py` | R69–R73; amended R61–R63 for grouped layers; R68 for group aliases; manifest schema for `display.select` and `water_review` |
| `v2/pipeline/config/water_display.json` | `expected_major_rivers`; threshold [D-4]; fit policy values if kept in config |
| `v2/map-data-v2.json`, `v2/regions/douglas-co/research.json` | Derived `group_id` on drawn members only. [D-1] may add a Douglas area layer |
| `v2/regions/*/region.json` | Aspen: two water layers over one canonical pointer; limitation sentence (approved); scope sentence [D-6]; fields declarations |
| `v2/regions/*/explore.json` | Two water layer entries with titles [D-5] |
| `v2/regions/*/display/*` | `water_streams.geojson`, `water_bodies.geojson` (Aspen); `waterways.geojson`, `waterbodies.geojson` (Douglas); `index.json`; `water-aliases.json`; possibly `water-groups.json` |
| `v2/regions/*/water-review.json` | New, empty lists unless the owner supplies entries |
| `v2/explore/layer-registry.js` | Fit policy per kind and geometry; two water layers |
| `v2/explore/shell.js` | Fit policy (tap cap, list minimum zoom); water in search; nothing water-specific in the adapter |
| `v2/explore/evidence.js` or a small new `v2/explore/water-detail.js` | Water detail sections 1–3, 5, 6 with the WW strings |
| `v2/explore/land-style.js` | Nothing new expected; water keeps its one colour |
| `v2/map-layers.js` | Legacy copy of the selection rule: keep consistent or retire if unused |
| `v2/pipeline/docs/data-contract.md` | Display contract additions; rules R69–R73; grouped-layer forms of R61–R63 |
| `docs/research/m4-water/selection-report.md` | Generated report with the 0.5 ha and 2 ha comparison |
| Tests | `test_water_m4b.py` (new), `test_region_contract.py`, `test_display_artifacts.py`, `test_display_budgets.py`, Node tests for detail and fit, `explore-checks.mjs` |

Must not change: `v2/explore/map-adapter.js` exports (twelve); vendored
Leaflet; `trust.js`; `trip-rules.js`; non-water layers; `measure.mjs`;
`run.mjs` lifecycle; thresholds and budgets.

## 4. Commit sequence

Each commit leaves both suites green. One commit per step where practical.

| # | Commit | Content |
|---|---|---|
| 0 | `data: …` only if [D-1] or [D-3] require it | The additional controlled NHD request, with a snapshot addendum and difference report, before any rule work |
| 1 | `feat: compute water display eligibility from source type codes` | Pure functions and unit tests; no artifact change |
| 2 | `feat: group stream segments by GNIS identity and connectivity` | Grouping, invariants G1–G10, unit tests, canonical `group_id`; no artifact change yet |
| 3 | `feat: validate water selection and grouping (R69–R73)` | Validator rules and negative fixtures; amended R61–R63 |
| 4 | `data: rebuild water display artifacts with selection and grouping` | Manifests, display artifacts, aliases to groups, `water_groups`, empty review lists |
| 5 | **CHECKPOINT 1** | Coordinator reviews data and report before any interface work |
| 6 | `feat: show water detail from source fields` | Detail sections and WW strings; no activity content |
| 7 | `feat: cap the fit for long rivers through a per-layer fit policy` | Shell and registry; tests for a short line and a long river |
| 8 | `feat: add water names to search` | |
| 9 | `test: cover water selection, grouping and detail in the browser check` | |
| 10 | `docs: selection report, contract and specification amendment references` | Generated report; contract docs |
| 11 | **CHECKPOINT 2** | Coordinator review; then performance sessions by the coordinator |

## 5. Stop conditions

Codex stops and asks, without working around:

- an expected major river is absent, below its drawn fraction, or contains a foreign member;
- a `gnis_id` carries two names;
- a rule as written produces a result the brief does not anticipate for a named, prominent water;
- a byte budget would be exceeded;
- any wording is needed that the specification does not give;
- the 2 ha rule excludes water the selection report's reviewer note calls clearly useful;
- anything in M4-B appears to need an activity or access field.

## 6. Layer titles (decision D-5)

Today both regions' water layers are titled from `explore.json`: Aspen has one
layer, "Named water". After M4-B each region has two water layers that are no
longer selected by name alone. Proposed titles, identical in both regions:

| Layer | Proposed title | Alternative |
|---|---|---|
| Streams | `Rivers and streams` | `Rivers & streams` |
| Waterbodies | `Lakes and reservoirs` | `Lakes & reservoirs` |

These are user-facing strings and need the owner's approval. They state
physical type only.

## 7. Expected results (to be confirmed by the build, not asserted from here)

| | Aspen | Douglas County |
|---|---:|---:|
| Stream groups | 71 (72 or 73 if connectors are not used for continuity) | 35, plus the South Platte if [D-1] is approved |
| Waterbodies at 2 ha | 46 | 32 |
| Line bytes | about 746,000 (from 1,097,000) | about 833,000 (from 1,787,000) |
| Waterbody bytes | about 72,000 | about 120,000 |
| Tappable water features | about 117 (from 1,555) | about 67 (from 2,392) |

Budgets: Aspen water artifacts ≤ 1,134,855 bytes in total; Douglas ≤
1,887,725. Both projections are well inside.

## 8. Verification the coordinator will run

Python and Node suites; display rebuild; the browser check twice; an
interleaved performance comparison against `main` (three sessions each, quiet
machine, nothing else running); canonical comparison against the M4-A head
(only `group_id` and, if approved, the added area layer may differ); every
group recomputed independently from canonical data with the dry-run script
and compared with the artifact; every WW string against its literal;
mutation proofs 1–12 of [validation-plan.md](validation-plan.md).

## 9. Draft Codex brief

Placeholders in ALL CAPS between double brackets are filled from the owner's
decisions before dispatch.

```text
Ohvernight M4-B — Functional recreational-water display. You are Codex, the single production implementation authority. Claude is coordinator, specification owner and independent reviewer. Hermes does research only. The human owner approves merges. Questions and blockers go to the coordinator through the Orca ask/escalation commands in your preamble, never to the human.

TARGET
- Worktree: [[WORKTREE PATH]]. Branch: [[BRANCH]], at origin/main [[MAIN SHA]] (M4-A merged). Do not create, rename or switch branches.
- Baseline verified here by the coordinator: Python [[N]] OK; Node [[N]] pass. The venv is at v2/pipeline/.venv.

READ FIRST, in full: AGENTS.md; docs/specs/M4-functional-recreational-water.md (APPROVED and authoritative, including amendments A1–A[[N]]); sections 8, 10, 11, 12, 13 (R69–R73 and the amended R61–R63), 14, 15, 16 "M4-B", 17 and 24 criteria 6–12; v2/pipeline/docs/data-contract.md; docs/research/m4-water/m4b-preparation/ (grouping-dry-run.md, major-river-audit.md, threshold-comparison.md, validation-plan.md, implementation-blueprint.md) and docs/research/m4-water/decision-packets/; docs/specs/M3-unified-mobile-explore.md amendments A13 and A14 (selection, fit, casing). Then the code: v2/pipeline/scripts/lib/water.py, build_display.py, lib/region_contract.py, v2/pipeline/config/water_display.json, v2/explore/shell.js, layer-registry.js, evidence.js, capabilities.js, map-adapter.js (read only — its twelve exports must not change), both region.json and explore.json files, and the water tests.

OWNER DECISIONS THAT BIND THIS WORK
- South Platte / centre lines: [[D-1 TEXT AND EXACT RULE WORDING]]
- Connectors: [[D-2 TEXT AND EXACT RULE WORDING]]
- Extent edge: [[D-3 TEXT]]
- Size threshold: [[D-4 VALUE OR RULE]]
- Layer titles: [[D-5 EXACT STRINGS]]
- Source-scope sentences: [[D-6 EXACT STRINGS]]
- Approved and exact, from specification section 10: WW1–WW16, the labels, and the water-layer limitation sentence. Use them byte for byte. Any other wording you need is a question for the coordinator.

SCOPE — specification section 16 "M4-B", in this order, one commit per step where practical, both suites green after each:
[[STEP 0 IF D-1 OR D-3 REQUIRE A CONTROLLED NHD REQUEST: scope, single session, snapshot addendum, difference report, stop on any unexplained difference]]
1. Eligibility (8.1, 8.2) as pure functions with unit tests. No artifact change.
2. Grouping (8.3) with invariants G1–G10 and unit tests; write canonical group_id on drawn members only. Group length shown to users is computed from the drawn geometry. No artifact change yet.
3. Validator rules R69–R73 and the amended R61–R63, each with a negative fixture; R68 extended so every legacy ID of a grouped segment maps to its group ID.
4. Manifests and display artifacts: Aspen's one canonical hydrology layer exposed as two display layers (streams, bodies) through display.select; Douglas waterways grouped; waterbody display properties per 8.4; water_groups; empty water-review.json for both regions; expected_major_rivers in water_display.json exactly as given: [[FIXTURE]].
>>> CHECKPOINT 1: after step 4, with both suites and the display rebuild green, send an ask beginning "CHECKPOINT 1 — M4-B data" with: commits; groups per region; waterbodies per region; every multi-part gnis_id; every expected major river with its drawn fraction; bytes per artifact and both budgets; canonical differences against the M4-A head; the generated selection report path. WAIT for the reply.
5. Water detail (11): sections "From the source", "Computed by Ohvernight", then WW1, then WW2 last. WW12 only when the category is perennial, WW16 when it is unknown. No activity label, status word or WW8 section — those are M4-C.
6. Fit policy (11, owner decision O6): per layer and geometry in the layer registry, not in the adapter. Water streams: map tap never zooms out more than 2 levels (if the group will not fit, keep the zoom and keep the tapped point in view above the sheet); list or search selection may fit down to a minimum zoom of 11. Every other layer: unchanged M3 behaviour. Tests for a short line and a very long river, both origins.
7. Water names in search for both regions.
8. Browser checks per validation-plan.md sections 5–7.
9. Selection report (8.6) generated by build_display.py --report and committed, with the 0.5 ha and 2 ha comparison and your reviewer note; contract documentation.
>>> CHECKPOINT 2: after step 9, with both suites, the display rebuild and ONE full browser check green, send an ask beginning "CHECKPOINT 2 — M4-B complete for review". WAIT for the reply before the final handoff.

MUST NOT
- Add any activity, access or claim field, registry or wording (M4-C). R75 stays green.
- Remove water by name keyword. Add a name-based rule anywhere.
- Invent geometry: no connecting line between members; G9.
- Change the adapter's exports, the vendored Leaflet, trust.js, trip-rules.js, any non-water layer, measure.mjs, run.mjs lifecycle, any threshold or budget.
- Change the 2 ha threshold or any rule to make a check pass. If an expected major river is absent, truncated or wrongly grouped: STOP AND REPORT.
- Weaken or delete an existing test. Where M4-B supersedes an assertion (the old named-water selection), replace it with the M4-B behaviour and list it.
- Edit the specification. Clarifications come to the coordinator.
- Add a dependency, colour system, icon or map-level status symbol.

STOP CONDITIONS (ask, do not work around): the list in implementation-blueprint.md section 5.

BUDGETS: Aspen water display artifacts in total ≤ 1,134,855 bytes; Douglas ≤ 1,887,725; bytes to map usable ≤ 500,000; default-on total ≤ 4,500,000; the alias and group maps are not requested during load.

TESTS: every case in validation-plan.md sections 1–7 that applies to M4-B, mapped to rule IDs; mutation proofs 1–12 run locally, not committed, with a clean tree afterwards.

USAGE AND PROCESS: Python suite, Node suite and the full browser check ONCE each on the final head, plus focused runs. No repeated consecutive browser runs and no performance sessions — the coordinator runs those on a quiet machine. Commit on this branch only; no push, PR, merge, amend or history rewrite. Temporary files under the OS temp directory, removed before worker_done. Leave the owner's port-8000 server alone.

ACCEPTANCE: specification section 24 criteria 6–11. Handoff (AGENTS.md format) written to [[REPORT PATH]] and passed as --report-path with worker_done: commits; groups and waterbodies per region; the expected-river table; bytes; every changed pre-existing assertion; mutation-proof output; implementation choices where the specification was silent; remaining uncertainty; and the iPhone checks the owner owes (iphone-acceptance.md).
```

## 10. Rollback boundaries

- Steps 1–3 add code and tests only; reverting them changes nothing a user sees.
- Step 4 changes artifacts and manifests together; reverting it restores the M4-A display exactly.
- Steps 5–8 are interface changes that depend on step 4.
- The whole pull request reverts to the M4-A state: old selection rule, stable IDs.
- A wrong threshold, exclusion or expected-river entry is a one-line data change and a rebuild.
