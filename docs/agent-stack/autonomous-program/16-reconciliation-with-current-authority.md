# 16 — Reconciliation with current authority (coordinator review)

**Status: PROPOSED, NOT ACTIVE.** Coordinator review of this package against the repository at `main` `c04f5d6`, 2026-10-19. The owner's charter text in files 00–15 is unedited. This file grants no permission and changes no other document. Each conflict below stays resolved in favour of the current authority until the owner approves the listed amendment through the normal pull request workflow.

## How to read this

- **Consistent**: the charter restates current authority; nothing to amend.
- **Conflict**: the charter, once adopted, would contradict a current governing document. Adoption of the charter alone does not resolve it; the named documents must be amended in a separate owner-approved change.
- **Correction**: a factual statement in the charter or in a current document that is out of date.

## Consistent with current authority (no amendment)

| Charter provision | Current authority |
|---|---|
| Per-PR exact-SHA human merge stays binding until a governance change (00, 10, 15-B) | ADR-002; `AGENTS.md` Working rules; `master-coordinator.md` Merge policy; `roles.md`; `docs/architecture/agent-stack.md` Merge authority |
| Owner gates are local locks; silence, timeout and exhaustion never approve (02, 10) | `master-coordinator.md` Owner gates; `overnight-autonomy.md` Local locks |
| Trust semantics retained: unknown stays unknown, ownership is not access, fail closed (00) | `docs/product/trust-principles.md`; ADR-005 |
| Claude coordinates and reviews, Codex implements, Hermes researches, Orca executes, Git is the source of truth (02) | ADR-001, ADR-003, ADR-004; `roles.md` |
| Real-device owner gate retained; Chrome viewport is not a substitute (09, 10, 15-C) | M3 and M4 specifications; current practice on PR #17 |
| No external contact, spending or paid services without owner authorization (01, 02) | `roles.md` Operations and gates; `hermes-research.md` |
| Capacity: most restrictive window wins; worktrees do not create quota; unknown capacity means no broad dispatch (04) | `capacity-routing.md` Reserve policy |
| Mobile-sheet defects fixed structurally, not with offsets (09) | Owner instruction 2026-10-19 (mobile sheet structural fix) |

## Conflicts requiring an owner-approved amendment before the charter can operate as written

| ID | Charter provision | Current authority it contradicts | Proposed resolution | Documents to amend if approved |
|---|---|---|---|---|
| C1 | Standing merge delegation for low-risk PRs under all conditions in 10 | ADR-002 ("Agents must never merge autonomously"; approval specific to one PR and head); `master-coordinator.md` ("there is no standing merge authority"); `roles.md`; `agent-stack.md`; `AGENTS.md` | Keep OFF. If the owner wants delegation, a new ADR-007 superseding ADR-002 in part, plus edits to the four documents, plus a runtime enforcement check, in one reviewed PR. Recommendation: development autonomy only (owner keeps merging) until the runtime has run under supervision without incident. | ADR-002 (status: partly superseded), new ADR-007, `AGENTS.md`, `master-coordinator.md`, `roles.md`, `agent-stack.md` |
| C2 | Coordinator may write and implement M5–M8 specifications after one charter approval (00 item 3, 02 Tier B, 15-A) | `roles.md` (owner approves specifications); `master-coordinator.md` milestone table (M5–M8 "future; read-only research"; "do not implement future functionality"); `agent-stack.md` workflow (human approval of each specification) | Owner chooses: (a) keep per-milestone spec approval (one approval per milestone, development autonomy inside it), or (b) delegate spec approval within the charter's target. Recommendation: (a). One owner review per milestone spec is a small burden, and it is where product and trust decisions concentrate. | `roles.md`, `master-coordinator.md` milestone table, `agent-stack.md` workflow, `ROADMAP.md` |
| C3 | Colorado-wide continuous Explore and statewide coverage program (01, 07, 08) | `ROADMAP.md` defines M1–M8 on two pilot regions and does not include statewide expansion; `docs/architecture/continuous-explore.md` and `adventure-model.md` are conceptual, not approved specifications | Product-scope decision (Tier C). If approved, add the Colorado coverage program to `ROADMAP.md` as a delivery track with its own specification before any loader or catalog implementation. | `ROADMAP.md`; later a coverage specification |
| C4 | 90% consumed as the outer ceiling (04, 15-D) | `capacity-routing.md` reserves: shared Codex/Hermes pool protects the greater of 25% or next-day implementation cost; Claude the greater of 15% or one material review plus margin | Owner decision. The charter already applies the stricter reserves until amended. Option: 90% hard ceiling with the "next-day implementation cost" reserve retained as a predictive stop. | `capacity-routing.md` Reserve policy |
| C5 | Operational state (lease, heartbeat, quota, sessions) lives in restricted host state, not Git (06) | `master-coordinator.md` Recursive queue and durability: durable run state under `docs/agent-stack/runs/<run-id>/` | Split: sanitized queue, locks, approvals and owner-return reports stay in `docs/agent-stack/runs/`; lease, heartbeat, quota snapshots, session identifiers and anything account-related stay in host state outside the repository. No conflict in intent; the contract needs one sentence. | `master-coordinator.md` |
| C6 | A host-side supervisor starts coordinator waves and wakes after resets (04, 05, 11, 12) | No current document authorizes an installed scheduler, launch agent or unattended wake; `overnight-autonomy.md` assumes a coordinator session is present | Separate owner gate after the Codex runtime feasibility assessment (`docs/agent-stack/proposals/autonomy-runtime-feasibility.md`, in progress). Until then autonomy is `RUNTIME_NOT_READY`. | `capacity-routing.md`, `overnight-autonomy.md`, new runtime document |
| C7 | Precedence item 1: explicit owner instructions above repository documents (00) | Consistent with `master-coordinator.md`, but ADR-002 requires PR-specific approval and cannot be overridden by a general instruction | Clarify in 00 that an owner instruction can approve a specific action immediately but cannot create a standing permission that a governing ADR forbids; standing permissions require the amendment route. | This package (00), on adoption |

## Corrections

| ID | Statement | Observed state | Action |
|---|---|---|---|
| K1 | Charter README: local Qwen integration is `PAUSED_BY_OWNER` | `main` (`tools/local-ai/qwen/README.md`, PR #37) records approved exposure and pilot boundaries but no pause. The pause is an owner instruction of 2026-10-19 ("Do not resume local Qwen/Odysseus work"). | Record the pause in the repository (one line in `tools/local-ai/qwen/README.md` or `ROADMAP.md`) when the owner approves; until then agents follow the instruction. |
| K2 | `ROADMAP.md` is authoritative (README) | `ROADMAP.md` still says "M4-A next"; M4-A merged 2026-10-07 (PR #12) and M4-B is in final review (PR #17). Draft PR #30 refreshes it. | Owner review of PR #30. |
| K3 | ADR-002 Consequences: "`main` has no GitHub branch protection" | A repository ruleset `protect-main` requires the `python` and `node` checks and a branch up to date with `main` before merge. | Update ADR-002's Consequences in the governance PR. |
| K4 | Hermes as an available research plane (02) | On 2026-10-08 Hermes web retrieval stopped with `Payment Required` / `insufficient_funds`. | Treat Hermes web research as unavailable until the owner restores it; no spending without authorization. |
| K5 | Orca run continuity (05) | Observed 2026-10-19: `worker-start` fails with `consumer_fenced` when the run is bound to another coordinator session; a new run had to be created. | Input to the feasibility assessment (Q1). |
| K6 | `master-coordinator.md` startup: "Open `~/Projects/ohvernight`" | Coordinators currently run in Orca worktrees under `~/orca/workspaces/Ohvernight/`. | Clarify in the governance PR. |

## What adoption of this package alone would change

Nothing operational. Merging this documentation PR records the proposal and this reconciliation. Every conflict above remains resolved in favour of current authority until its amendment is approved. The activation sequence is in `13-implementation-plan.md`; the owner's choices are consolidated in the activation packet that accompanies this PR.
