# Run run_16f69595c542 — review-debt triage (2026-10-19)

All sixteen draft PRs have green CI; only #27 conflicts with `main`. Verdicts are posted on each PR with its exact head.

| PR | Kind | Verdict / state | Next |
|---|---|---|---|
| #31 | Test: R31 negative case | Reviewed **PASS** at `843d055` | Owner exact-head approval |
| #32 | Docs: system overview corrections | Reviewed **PASS**; every correction checked against ROADMAP and M3 A13 | Owner exact-head approval |
| #22 | Tests pinning pipeline risks (`@expectedFailure`) | Reviewed **PASS** | Owner approval; merges first in its cluster |
| #26 | Fix: log geometry repairs | Reviewed **PASS** at `646eb07` | After #22: Codex drops its pin, fresh review |
| #28 | Fix: require trail activity fields (fail closed) | Reviewed **PASS** | After #26: rebase, drop pin, fresh review |
| #25 | Fix: trail drift report (fail open) | Reviewed **PASS**, one nit (wrong error label) | After #28: rebase (same lines), nit, drop pin, fresh review |
| #27 | Fix: staged display publication | **Conflicts** with `main`; not reviewed | After #25: Codex rebase, then review |
| #30 | Docs: roadmap M4 status | Refreshed by the coordinator to `457a4a7` (was stale) | Owner wording decision |
| #34 | UI: source-link wording, site types, blank fields | Not approvable by agents: changes trust-bearing wording. **Design conflict with #36** on blank fields (#34 shows "Not stated in this source record"; #36 hides blanks and adds one caution line). Stacked on #21 (merged). Overlaps #36 files. | Owner decides the blank-field design; then one PR is rebased on the other |
| #36 | Feature: other listed sites | Its own sheet/header changes are superseded by #39 | After #39 merges: Codex rebase dropping sheet changes; review; iPhone |
| #24 | Docs: M6 source policy proposal | Owner decision (source policy) | Owner |
| #20 | Docs: Rampart day-use acceptance scenario | Owner decision (acceptance scenario) | Owner |
| #15, #23 | Unreviewed research archives (~17k lines) | Not reviewed; labelled DRAFT/UNREVIEWED | Owner: merge as archive or keep as branches |
| #29, #33, #35 | Research: Rampart example, M6 motorized prototype, M7 orders model | Inputs to M6–M8 specs; not reviewed | Reviewed when the M6/M7/M8 specs are drafted |
