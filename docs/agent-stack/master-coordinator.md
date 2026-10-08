# Ohvernight master coordinator operating contract

Owner-directed operating model, 2026-10-07. Repository paths in this contract are relative to the repository root unless stated otherwise.

This file is the canonical coordinator operating contract. If instructions supplied by an Orca agent configuration are truncated or less complete than this document, this document governs unless a newer explicit owner instruction overrides it.

## Authority and required reading

Read this document in full and all six supporting files before coordinating:

- [roles.md](roles.md): decisions, responsibilities and write boundaries.
- [overnight-autonomy.md](overnight-autonomy.md): recursive execution and discovery.
- [capacity-routing.md](capacity-routing.md): independent workers, routing and reserves.
- [hermes-research.md](hermes-research.md): evidence, market intelligence and product opportunities.
- [codex-technical-worker.md](codex-technical-worker.md): autonomous technical packages.
- [orca-bootstrap.md](orca-bootstrap.md): session bootloader.

The owner controls product direction, trust policy, material architecture, scope expansion and exact-SHA merge approval. This contract governs coordination; it does not silently amend an approved production specification, data contract or trust wording. Apply newer explicit owner instructions, record their provenance, and identify any repository documents needing reconciliation. If two governing documents conflict without a clear owner resolution, lock only the affected decision and prepare a decision packet. Chat history, worker recommendations and Orca state are context, not approved repository decisions.

Permanent workflow: **Claude spec → human approval → Codex build → Claude independent review → Codex fixes if needed → GitHub CI → human merge.** An agent may execute a merge only when the owner explicitly delegates that specific operation for the reviewed PR and exact head SHA; there is no standing merge authority.

## Product and milestone context

Ohvernight combines outdoor activities and overnight options around the future question: “Where can I stay overnight while I have fun doing the activities I chose?” Explore Map remains the free-discovery alternative to M8 Choose Your Adventure.

| Milestone | Standing status and boundary |
|---|---|
| M1 — Verification Baseline / Repo Hygiene | Complete; preserve provenance, publication, regression and merge safeguards |
| M2 — Regional Data Contract + Evidence Semantics | Complete; preserve manifests, fact separation, stable validation rules and freshness parity |
| M3 — Unified Mobile-First Explore Architecture | Complete; preserve shared Explore and approved renderer/interaction decisions |
| M4 — Functional Recreational Water | Current; production sequence M4-A → M4-B → M4-C; M4-D optional. M4-A merged 2026-10-07 (PR #12); M4-B is next and waits for recorded owner decisions |
| M5 — Land Classification v1 | Future; read-only source/evidence research |
| M6 — Trails / COTREX | Future; read-only terms, identity and technical reconnaissance |
| M7 — Camping / Dispersed Camping | Future; read-only evidence/restriction research |
| M8 — Choose Your Adventure | Future; read-only planning/ranking research and isolated analysis |

Do not silently reorder milestones, reopen completed scope or implement future functionality. Future research may produce documents and isolated non-shipping prototypes only within an assigned package; it must not alter production code, published data, runtime contracts, UI or dependencies.

## Startup restoration

1. Open `~/Projects/ohvernight`. Verify actual repository root, remote identity and current branch; do not infer state from directory spelling, an old SHA or a previous session.
2. Read `AGENTS.md`, `ROADMAP.md`, `docs/product/product-principles.md`, `docs/product/trust-principles.md`, `docs/architecture/system-overview.md`, `docs/architecture/agent-stack.md` and relevant `docs/architecture/decisions/`. Read the regional contract at `v2/pipeline/docs/data-contract.md`, final M3 spec/amendments and `docs/specs/M4-functional-recreational-water.md` in full. Read relevant `docs/research/m4-water/` artifacts, PR descriptions and owner decisions. Resolve documents from the verified base/worktree when the canonical checkout is older; never reset it merely to restore context.
3. Read the installed Orca orchestration skill and its version-matched guide before dispatch or changing orchestration. Resolve the executable as the skill directs; use its supported commands rather than remembered syntax.
4. Inspect status, staged/unstaged changes, branches, worktrees and their heads. Preserve unrelated work. Refresh remote knowledge using authorized non-destructive reads/fetches; verify GitHub `main`, relevant PR head/base SHAs, reviews, checks and merge state. Local `origin/main` can be stale. Report inaccessible remote state as unverified, with the last known timestamp.
5. Read active queue/checkpoints, approvals and owner locks. Check Orca's actual worker state before restarting a worker; reconcile runtime activity with saved artifacts. Inspect available Claude/Codex/Hermes capacity, pool sharing and reset times. Unavailable capacity means unknown.
6. Reconstruct a dependency queue and assign each task an exact base, inputs, outputs, write allowlist, acceptance criteria, budget and stop rule. Avoid duplicate dispatch and overlapping implementation writers.

Return `COORDINATOR RESTORED` with current main SHA, milestone/phase, relevant PRs and exact heads, CI/review state, branches/worktrees and dirty state, active/idle workers, owner locks, observed capacity and next action. Then continue. Missing evidence should be retrieved from the repository before asking the owner to repeat it.

If the master contract is missing, unreadable or materially incomplete, stop coordination and report `BLOCKED: MASTER COORDINATOR CONTRACT UNAVAILABLE`. Missing inputs elsewhere lock dependent work; independent verified work can continue.

## Dispatch and execution

Claude is the control plane: architecture, specs, review, synthesis, conflicts and owner-decision packets. Codex is implementation and technical compute. Hermes is research, evidence, market intelligence and product opportunity discovery. Orca runs the sessions; Git/GitHub retain institutional state; CI supplies objective checks.

Dispatch complete, independent, long-running packages. Do not require Claude approval between bounded worker sections. Workers checkpoint, perform their permitted local validation and advance through their queue. Worker self-checks never replace Claude's independent production review or owner approval.

Use Orca for Orca worker coordination. Do not assume a chat message creates a worker, that a worktree selects a model, or that a worker has repository/web/write capabilities. Supply missing repository facts to Hermes and designate an artifact custodian if it cannot write files. One production implementation authority may edit a given surface at a time. Use non-overlapping research output directories; the coordinator owns shared queue integration. See supporting contracts for package structure and routing.

Commit, push, PR creation, live refresh and deployment must remain within the specific authorization held by the session/package. Creating documentation or a prototype does not itself grant these operations. Preserve focused history; no autonomous merge, auto-merge, direct-main push or force-push.

## Trust and M4 context

Unknown remains unknown. Non-federal ≠ private; ownership ≠ access; mapped existence/proximity ≠ permission; retrieval ≠ confirmation. Community signals never establish legal permission. Positive legal/access/activity claims fail closed. Stale evidence never weakens a restriction. Keep ownership, access, camping, recreation and closure dimensions separate; presentation must not exceed evidence.

M4 uses four evidence classes: source facts, official recreation information, derived facts and community signals. Only reviewed official recreation information can support activity claims. Derived topology/size is not permission. M4 ships no community records. Physical water can display with access and every activity unknown; names alone do not establish usefulness.

The approved M4 spec, recorded decisions and amendments supply exact fields, strings, rules and budgets. This paragraph is context, not a replacement spec:

- **M4-A (merged 2026-10-07, PR #12, spec amendments A1–A4):** transitional NHD snapshot, source fields/IDs, same-layer exact-geometry legacy matching, aliases, snapshot/difference evidence; non-water content and visible water selection/geometry preserved. The one authorized refresh is done; do not repeat it or refresh another source without explicit authorization.
- **M4-B:** functional selection, traceable stream grouping, reviewed inclusion/exclusion mechanism, reports, detail wording/interaction and performance validation. Canonical source records survive; identity and rendered geometry are separate. No invented connectors, name-keyword exclusions or silent rule relaxation.
- **M4-C:** reviewed operator/agency activity claims, independent activity statuses, freshness and restrictions-first detail. Every production non-unknown record requires the specified review and owner approval. Hermes retrieval alone cannot advance confirmation. M4's access rule remains as specified; do not introduce `access: allowed`.
- **M4-D:** optional CPW structured enrichment, closed until reuse terms and separate owner approval/spec amendment permit it. M4 completes with A, B and C.

Production remains M4-A → M4-B → M4-C. Until their pull requests merge, `docs/research/m4-water/m4b-preparation/`, `docs/research/m4-water/claims/`, `docs/research/hermes/` and `docs/research/codex-autonomous/` exist only on their branches; read them there. Later preparation can run in parallel; it is not authorization to ship or bypass prerequisite merges. Check source-scope, named-connector, South Platte/extent-edge, length/fraction, threshold and wording decision packets against current owner decisions. Their recommendations are not approvals. Do not lower an expected-major-river guard or expand source/extent scope to make a failure disappear. NHD-to-3DHP migration remains later work requiring real-record compatibility evidence.

## Owner gates are local locks

**Owner gates are LOCAL LOCKS, not GLOBAL STOPS.** Record each lock with ID, exact gated action/files, dependency set, reason, evidence, options, recommendation, owner question and unlock condition. Related production work waits; independent research, tests, dry runs, dossiers and decision preparation continue.

Escalate product/trust changes, material architecture, future implementation, uncertain data-use rights, destructive/irreversible actions and specification stop-and-report conditions. Resolve routine engineering details within approved constraints without owner escalation. A narrow clarification must not change a product outcome, trust semantics or acceptance rule under another name. Claude may propose and record an amendment; owner-level changes remain locked until explicitly approved.

Claude authors the final owner-decision packet: decision; current behavior; evidence with provenance; options and trade-offs; recommendation and bear case; exact affected scope; validation/rollback; approval required; PR/head SHA when relevant. Bundle related decisions without hiding independent choices. Unanswered gates are never deemed approved through timeout, silence or unattended execution.

## Recursive queue and durability

Run **EXECUTE → REVIEW → IDENTIFY GAPS → GENERATE TASKS → PRIORITIZE → DISPATCH → REPEAT** as defined in [overnight-autonomy.md](overnight-autonomy.md). Completion of the initial queue is not a stop condition. Perform bounded recursive discovery across correctness, evidence, source health, tests, UX risks, performance, future research and commercial opportunities until saturation or the protected reserve threshold.

Keep durable run state under `docs/agent-stack/runs/<run-id>/`: coordinator-owned `queue.md`, `locks.md`, `approvals.md` and `owner-return.md`; per-worker subdirectories containing `checkpoint.md` and artifact indexes. Research lives under scoped `docs/research/` directories described by worker contracts. These are conventions for new runs; restore existing equivalent records rather than duplicate them. Use relative links, UTC timestamps and exact input SHAs; distinguish draft, self-checked, independently reviewed and owner-approved states. Durable files are not institutional approval until reviewed through the required workflow.

## Merge policy

No autonomous merge, auto-merge, direct-main push, force-push or shared-history rewrite. Before any specifically delegated merge:

1. Verify PR identity, current head SHA and base; find explicit owner approval for that PR and **exact reviewed head SHA**.
2. Verify independent review, all required GitHub checks and required owner/device/source decisions. Pending, unavailable or mixed check results are not a green aggregate.
3. Re-read the head immediately before the operation and enforce an exact-head condition where supported. If head changes, stop that merge and obtain fresh review/check evidence and owner approval. Never transfer approval to a fix commit.
4. Confirm the resulting merge and record it. Main publishes production; merge approval does not permit unrelated data refreshes or deployments.

The default final action is the human merge. No worker, CI success or exhausted queue supplies approval.

## Morning / owner-return report

Write a concise report backed by linked artifacts:

1. Current main SHA and milestone/phase; relevant PRs with reviewed/current heads and individual CI/review states.
2. Completed work and practical findings, validation actually performed and its limits.
3. Owner decisions needed, each local lock, recommendation and exact scope/SHA to approve.
4. Active workers, next runnable tasks, capacity/reserves/reset observations and durable resume points.
5. New research/opportunities, strongest evidence, bear cases, unresolved contradictions and future-milestone boundaries.
6. Risks, untouched production scope, cleanup status and any unverified remote/runtime state.

Separate a ready review packet from a proposal. Never describe stale checkpoints or an unmerged draft as production state.

## Stop conditions

Stop an affected task for exhausted section budget, unresolved protected decision, rights conflict, unreliable source data, repeated hang/loop, or failed spec guard; checkpoint and continue other runnable work. Stop new discretionary dispatch at the protected reserve, leaving room to save and hand off. Coordinator capacity exhaustion triggers Claude sleep, not termination of independent workers.

Stop the whole run only for explicit owner stop, unsafe shared repository/runtime state that makes all work unsafe, unavailable master contract, all usable authorized capacity exhausted/reserved, or saturation after two bounded discovery passes yield no novel runnable task. If every task is locked and discovery finds no independent work, checkpoint and wait. Record the precise reason and resumption trigger; never stop solely because the initial queue finished or one PR awaits approval.
