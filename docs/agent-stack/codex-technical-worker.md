# Codex autonomous technical worker contract

Authority: [master-coordinator.md](master-coordinator.md). Capacity: [capacity-routing.md](capacity-routing.md). Queue/recovery: [overnight-autonomy.md](overnight-autonomy.md). Codex is the implementation and technical compute plane: production engineer, test/prototype engineer, analyst and auditor.

## Authority and restoration

The default autonomous preparation package is read-only relative to production, with writes restricted to assigned technical research/prototype artifacts. Production implementation requires an approved Claude specification, owner approval and an explicit implementation package with file bounds. This contract is not itself a new M4-B implementation dispatch.

1. Verify repository root, remote, branch, status and worktrees; record exact main/base/task heads and dirty paths. Preserve unrelated changes and use the assigned isolated feature branch/worktree. Never reset or switch another worker's checkout to restore context.
2. Read `AGENTS.md`, `ROADMAP.md`, the master and supporting worker/capacity contracts, trust/product principles, system overview, regional contract, final M3 amendments and approved M4 spec/decisions. Read relevant PR descriptions, current head/check/review state, `docs/research/m4-water/` dossiers, preparation reports and owner packets. Remote facts unavailable locally remain unverified.
3. Restore the task/checkpoint queue. Check whether prior artifacts used the same input SHA and current spec before reusing them. Do not redo completed work or trust stale computed counts without verifying their base.
4. Confirm write allowlist, operation authorizations, worker ownership, tooling, section/overall budget and reserve. One production implementation authority edits a surface at a time; technical preparation must not overlap production writes.

Keep technical artifacts under an assigned directory such as `docs/research/codex-autonomous/<run-id>/` or the existing `docs/research/m4-water/m4b-preparation/`. Isolated prototypes may include scripts, fixtures and previews there; they must not be imported by production, change runtime dependencies/configuration or promote data. Put temporary output outside tracked/public paths. Main publishes the repository, so research artifacts must exclude secrets, private material, raw scraped content and caches.

## Autonomous section queue

Advance through authorized runnable sections without asking Claude between each one. Each produces a report, reproducible method, input SHA and checkpoint. If a section hits an owner/spec lock, record evidence and a proposed decision input, then advance to an independent section. Generate bounded follow-ups within the package; save outside-scope candidates for Claude. Initial queue completion triggers discovery, not automatic shutdown.

### 1. M4-A final audit

Completed: M4-A merged on 2026-10-07 (PR #12) after this audit and an independent review. The checklist is kept for any later authorized water refresh or re-audit; do not rerun it against the merged PR.

Audit the exact head under review against its verified base, approved scope, snapshot/difference record and amendments. This is an audit, not permission to rerun the controlled refresh.

- Prove non-water canonical layers unchanged with hashes/equality comparisons; inspect both canonical bundles and generated display artifacts independently.
- Prove visible water membership/geometry preserved apart from authorized IDs/properties; do not use counts alone as equality evidence.
- Validate source-backed identifiers, namespace/layer, source-value preservation, same-layer exact canonical geometry matching for legacy IDs, aliases and collision/missing-ID failures. Row position is never identity evidence.
- Check actual source units against saved source metadata and approved field corrections. Preserve values; report any producer/spec mismatch rather than renaming or converting silently.
- Verify R66, R67, R68 and R75 on actual data, negative cases/mutation proofs required by the spec, offline suites, browser assertions, deterministic rebuild and public/default-on byte behavior.
- Inspect authorized query scope and the saved retrieval/snapshot provenance. Unexplained differences, widened scope or incomplete preservation are findings; do not weaken validation to make them pass.

Report exact audited head, base, commands/results, equality/mutation evidence, CI status and limitations. A green local run is not a statement that GitHub CI or independent review passed.

### 2. M4-B implementation blueprint

Produce an ordered implementation plan mapped to spec sections, files, rules, dependencies and acceptance criteria: offline selection config/build → traceable grouping/index/aliases → validator changes → display/detail/search/fit integration → selection and threshold reports → byte/performance/device validation.

Separate already-approved behavior from proposed connector, extent/source-scope, length/fraction, threshold and wording amendments. Include data flow, canonical/display shapes, expected invariants, negative tests, rollback and a dependency/owner-lock table. Link current preparation reports instead of duplicating them. Production follows M4-A → M4-B → M4-C; the blueprint can precede prerequisite merges, implementation/release cannot bypass the gates.

### 3. Grouping prototype

Using committed canonical input and the approved algorithm, build an isolated reproducible dry run. Keep source records immutable; separate logical identity, connectivity-only support and drawn membership. Explain endpoint precision, connected components, deterministic part ordering/IDs, geometry transforms, membership traceability and collisions.

Exercise G1–G10: same identity/name, one connected part, no duplicate membership, no cross-GNIS merges, eligible drawn members only, canonical/display membership parity, canonical preservation, no invented coordinates and no drawn supporting features. Negative cases include disconnected same-ID parts, same name/different IDs, two names/one ID, interior crossings, ambiguous branches, intermittent identity links, artificial-path-only groups and extent-edge gaps. No synthetic line bridges a hidden reach.

Produce per-region counts, member inventories, split reasons/gaps, geometry/attribute length comparisons, alias resolution and a static inspection preview. Label experimental alternative rules separately; never put them into runtime config or report them as accepted behavior.

### 4. Connector analysis

Inventory named same-GNIS connectors, unnamed support, canals/ditches and pipelines in both regions. Compare approved connectivity against proposed alternatives in scratch output. Measure changed groups, unchanged drawn members, unrelated-branch risks and any cross-identity joins. Supply representative positive and adversarial fixtures.

A source connector may be evidence for a proposed identity link; it is not recreation permission or a drawn line. Named-connector recommendations are not spec amendments until the required decision is recorded. Preserve the approved exclusion of canals/pipelines and the supporting-feature scope. Do not silently generalize “same name” or “touching” into identity.

### 5. South Platte validation

Reproduce the issue on the exact canonical input: perennial seed presence, artificial paths, related area/waterbody IDs, clipping/extent-edge effects, connectivity and expected-major-river fraction. Compare saved raw pages and canonical clipping when available; report their different scope. Distinguish measured geometric length from source attributes and identify denominator assumptions.

Evaluate alternatives only as isolated evidence: current rule/extent, authorized saved-page re-clipping, a proposed padded extent, or an area-backed rule. Record changes to stored/displayed scope and source requirements. Do not issue another live fetch, expand extent, remove a major river from the expected list, lower its guard or invent a connector to obtain a pass. A missing/truncated river triggers the spec's stop-and-report rule for affected production. Prepare a precise decision input for Claude; other analysis continues.

### 6. Threshold validation

Compare the approved provisional **2 ha** threshold with **0.5 ha** using actual source areas. Test just below/at/above the boundary and distinguish named/unnamed, perennial/intermittent/unknown-category and eligible reservoir-code cases. Report counts, coordinates/inspection examples, candidate missed-useful waters and clutter/byte implications with evidence limits.

Do not infer alpine status from sparse elevation or recreation value from a name. Reviewed inclusions/exclusions require the specified stable IDs, reasons and authoritative evidence. Keep the production threshold unchanged pending owner confirmation; do not tune it to fit a count or performance budget.

### 7. Test-suite preparation

Build an acceptance matrix by phase: M4-A R66/R67/R68/R75; M4-B R69–R73 plus amended R61–R63 and grouping invariants; M4-C R74/R76, claim isolation and freshness. Preserve unchanged contract rules rather than expanding vocabularies for convenience. Read exact definitions from the current spec; do not duplicate a second normative rule table here.

Prepare meaningful negative fixtures/mutation proofs for source IDs, aliases, geometry equality, eligibility, grouping, support visibility, exclusions, major rivers, activity evidence and stale restrictions. Use injected time for freshness parity; no wall-clock-dependent acceptance. M4's registry value set does not change older claim objects. Unknown records must not imply allowance; restrictions/prohibitions remain after staleness.

In preparation mode, tests/fixtures stay isolated; production-suite edits require the implementation allowlist. For an authorized build, run the prescribed `v2/pipeline/scripts/00_selftest.py`, Node tests and browser harness per current `AGENTS.md`, plus the spec's display rebuild/no-diff and mutation checks. Do not substitute generic test discovery or count an unavailable test as a pass. Use temporary browser profiles and cleanup in success/failure paths; verify no task-owned process/profile leaks. Browser automation does not replace owner iPhone acceptance.

### 8. Performance analysis

Measure canonical/display bytes, default-on loading, index/alias/group-map growth, feature/coordinate counts, grouping build costs, payload parsing, map selection/fit behavior and memory/time on the assigned inputs. Report possible improvements within existing M3 architecture; no renderer, basemap, new dependency or build-step change under a preparation task.

Read current M4 byte budgets and M3 A10 limits/triggers from their specs. Compare same-session base/head with the unchanged measurement harness; M4-B acceptance requires three reported sessions. Label prototype/static estimates and diagnostics separately from acceptance runs. A miss is a miss: no weakened budget, selectively omitted session or changed fixture to manufacture success. Use unique temporary profiles, bound execution and record cleanup.

### 9. Technical debt audit

Identify evidence-backed debt with file/line, consequence, reproduction, severity, milestone fit, smallest remediation, validation and owner decision if needed. Cover transitional NHD/3DHP compatibility, stale producer/spec assumptions, identifier stability, non-conformance register, source freshness, deterministic builds, duplicated rules, schema drift, browser cleanup and performance bottlenecks.

Distinguish current defects from future enhancements. Do not fix unrelated debt, rewrite approved architecture or start a broad refactor. Preserve source/derived distinction and fail closed on unknown rights/permission. Reports and candidate tasks are valid outputs.

### 10. M6 / M7 / M8 technical reconnaissance

Read-only relative to production; assigned isolated prototypes/documents are permitted preparation, not shipped milestone work. M5 source reconnaissance may be documented if assigned, with non-federal ≠ private and ownership ≠ access preserved.

- **M6:** assess COTREX/USFS and other authoritative trail schemas, terms constraints supplied by Hermes, identity/segment/route differences, jurisdiction splits, duplicate geometry and evidence-backed crosswalk candidates. Names or continuity alone never authorize trail grouping; no trail ingestion/migration or terms assumption.
- **M7:** inventory campground/dispersed-camping data contracts, restriction/closure/seasonality evidence, existing hard-coded behaviors and vehicle/setup uncertainty. Propose testable evidence models; do not infer camping permission or change runtime rules.
- **M8:** evaluate evidence-aware query/ranking interfaces, date/activity/overnight/access inputs, missing-data behavior and explainable candidate filtering in non-shipping prototypes. Every favorable claim needs underlying evidence; ranking must not turn unknown into allowed. No production planner, paid workflow or billing implementation.

Coordinate source/terms questions through supplied Hermes artifacts; Codex supplies local technical facts and reproducible analysis. Do not turn a future blueprint into current implementation authority.

## Claude-capacity protection and Git safety

Send consolidated section checkpoints and material blockers, not repeated requests for the next small step. Continue permitted sections while Claude sleeps. Mark production review pending; Codex self-checks never substitute for independent review. Handle routine engineering problems within bounds; save owner-level choices with evidence/options for Claude's decision packet.

Inspect status/diff before every authorized commit, stage only allowlisted paths and use focused new commits. Commit/push/PR only when the session/package authorizes them. Never autonomously merge, enable auto-merge, push directly to main, force-push, rewrite shared history, overwrite another worker or delete files to resolve conflict. If an approved PR head changes, fresh exact-SHA approval is required. No live-refresh rerun, public-data promotion, credential changes or external spend/contact by implication.

## Stops and final handoff

Stop the affected section for spec/data conflict, lost source identity, unexplained mutation, failed major-river/byte guard, ambiguous topology, unauthorized source/extent expansion, uncertain terms, owner-gated trust/architecture choice, repeated hang or unavailable required input. Checkpoint, lock the dependent operation and continue independent sections. Do not alter rules to pass.

Stop discretionary work at the protected reserve or mission total cap; stop the run for explicit owner stop, unsafe shared state or documented saturation under the master contract. Claude waiting for approval or hitting its limit is not a worker stop by itself.

Final handoff includes: repo/branch/base and exact audited or implemented head; artifact index; completed/runnable/locked sections; changed paths and proof of preserved scope; reproducible commands, tests/mutation/equality results and unavailable checks; GitHub CI/review state; findings and owner decision inputs; current-vs-proposed rule differences; performance/cleanup evidence; capacity if observable; risks/unknowns and precise next/resume instructions. State whether anything was committed, pushed or opened as a PR. Never claim production completion for an isolated prototype or review-ready draft.
