# Ohvernight bounded autonomous build charter — adoption package

**Status: PROPOSED, NOT ACTIVE.** This is a standalone, repo-ready Markdown instruction package. It was drafted from the existing Ohvernight `AGENTS.md`, `ROADMAP.md`, `docs/agent-stack/` contracts, product/trust principles, adventure model and continuous-Explore direction. It does **not** modify the live repository or Orca configuration.

## What it is

A scoped operating charter for building a trustworthy, mobile-first, Colorado-wide Ohvernight product with fewer routine owner prompts. It describes coordinator behavior, autonomous task sequencing, objective gates, pause/resume semantics, and the final product evaluation.

## What it is not

- Not a running scheduler or background daemon. Markdown alone cannot keep a model session alive, wake it at reset, or observe usage.
- Not a guarantee that Claude or Codex usage can be read programmatically at 90%. That must be confirmed for the installed versions, account types and Orca execution path.
- Not authority to ignore the currently binding **per-PR, exact-head human merge gate**, existing specs, source licensing, security or real-device owner gates. These require explicit, attributable owner-approved governance changes before any standing delegation applies.
- Not permission to unpause Odysseus/Qwen, purchase credits, start paid services, issue third-party communications or broaden the project beyond Ohvernight.

## Where these files belong, after review

Copy the directory `docs/agent-stack/autonomous-program/` into a dedicated documentation PR. After that PR is accepted, add a brief pointer in `AGENTS.md` and `docs/agent-stack/master-coordinator.md`; reconcile any authority changes through the existing PR/ADR workflow. Do not overwrite the existing agent-stack files wholesale.

## Recommended reading order

1. `00-adoption-and-precedence.md` — activation gates, contradictions and unchanged rules.
2. `01-target-product.md` — what the final product must actually do.
3. `02-autonomy-and-authority.md` — decisions agents may take; protected owner decisions.
4. `03-coordinator-loop.md` — task selection, dispatch, review and continuation.
5. `04-capacity-and-sleep.md` — Claude/Codex 90% exhaustion ceiling, multi-window quotas.
6. `05-orca-runtime.md` — the **separately implemented** persistence/wake mechanism.
7. `06-checkpoints-and-recovery.md` — state model and idempotent restart.
8. `07-milestones-and-dependencies.md` — M4 through M8 and Colorado expansion gates.
9. `08-colorado-coverage.md` — statewide architecture and rollout.
10. `09-testing-and-product-acceptance.md` — release/user acceptance.
11. `10-review-merge-and-escalation.md` — PR/CI/review/merge authority.
12. `11-operating-and-recovery-runbook.md` — failures, pause, rollback, reports.
13. `12-coordinator-bootstrap.md` — compact startup prompt and behavior.
14. `13-implementation-plan.md` — minimal changes needed to activate, in safe order.
15. `14-sample-state-and-task.md` — example shapes (examples, not real state).
16. `15-owner-activation-record.md` — optional one-time, explicit scoped authorization template.

## Activation sequence

**A. Approve the target and scope.** Explicitly approve or adjust the product charter; record changes by documentation PR.

**B. Decide on merge delegation.** Existing GitHub Pages `main` merges deploy production. Until the owner approves a specific change to governance, every merge still needs exact-SHA human approval. Autonomous development and draft PRs can still run without continuous owner involvement.

**C. Implement and verify a host-side Orca scheduler and usage probes.** The coordinator alone cannot schedule its own wake-up when its provider refuses more calls. The scheduler must survive model-session exit, use observed official/supported usage signals, and pass restart/crash tests. No ability is assumed without verification.

**D. Start the autonomous program.** Only when A–C are satisfied. The coordinator restores actual Git/Orca state and begins bounded task waves, sleeping and resuming as appropriate.

**E. Final owner product critique.** The desired norm is one substantive evaluation of a usable product, with interrupts only for genuine protected gates and failures.

## Existing source-of-truth constraints

- `ROADMAP.md` is authoritative until changed via approved PR.
- `docs/product/trust-principles.md` and `v2/pipeline/docs/data-contract.md` remain normative.
- `docs/architecture/adventure-model.md` and `docs/architecture/continuous-explore.md` are **conceptual**, not currently approved implementation specs.
- M4 completes after A+B+C; M4-D is optional.
- M5–M8 have not all received owner-approved production specifications.
- Cross-region loading/statewide Colorado currently needs a spec and design decision, not an unreviewed loader replacement.
- `tools/local-ai/qwen/` may exist on `main`, but integration remains **PAUSED_BY_OWNER**.
