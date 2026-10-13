# Execution topology and capacity routing

Authority: [master-coordinator.md](master-coordinator.md). Section and discovery behavior: [overnight-autonomy.md](overnight-autonomy.md).

## Topology

Claude dispatches complete Codex technical and Hermes research packages through Orca, then spends its capacity on architecture, independent review, conflicts, synthesis and owner decisions. Workers advance section-to-section with durable checkpoints. Claude consumes milestone-sized outputs and escalations; it is not a constantly supervising parent or a repetitive compute engine.

**Worktrees are file-isolation boundaries, not model-usage boundaries.** Different branches, worktrees, terminals or worker names do not create independent allowances. Multiple workers/models may share the same account pool. Check actual provider/account usage and reset windows; never infer independence from process topology or model labels.

Hermes missions should be long-lived independent packages with several bounded sections and a finite overall budget. A mission can complete a source survey, terms matrix, dossier set, market/pain analysis and targeted second pass without returning to Claude between each section. Independence does not expand its write authority or bypass owner gates.

Codex performs both production engineering and technical analysis: counts, topology, grouping dry runs, schema comparisons, prototypes, tests, audits and performance. Claude should receive the computed artifacts and review the material conclusions instead of repeatedly doing those calculations itself.

## Routing

| Work | Route | Reason |
|---|---|---|
| Architecture, specs, independent review, trust conflicts, synthesis, owner-decision packets | Claude | Judgment and cross-project accountability |
| Implementation, local counts, data comparisons, grouping/topology, tests, dry runs, prototypes, performance and audits | Codex | Reproducible technical compute and engineering |
| Broad extraction, official source inventories, straightforward terms extraction, competitor surveys, complaint clustering and watchlists | Hermes + Luna | Bounded breadth with inexpensive extraction |
| Ambiguous terms, source semantics, nuanced operator claims, real-record crosswalk interpretation and high-value synthesis | Hermes + Sol | Higher interpretation cost and consequences |

Luna/Sol are routing labels; verify the actual available model identifiers before dispatch. Use the least costly adequate route. Escalate a focused ambiguous section from Luna to Sol with the gathered evidence, not a full restart. Neither model's conclusion is legal clearance or approval. Do not invent current prices, quotas or supported reasoning settings; consult available account/runtime information when configuring them.

## Reserve policy

Preserve a **next-day implementation reserve**, especially in any pool shared by Hermes and Codex. Research must not consume the allowance needed for the next approved build, acceptance tests, fixes and handoff.

At startup record, for every observable pool: remaining allowance, window/reset, consumers, task estimate, next-day implementation estimate and protected reserve. Owner-set thresholds govern. If none exist, use these conservative planning defaults and record them as defaults, not provider facts:

- Shared Codex/Hermes pool: protect the greater of 25% of the applicable full window or the estimated next-day implementation/verification cost plus handoff margin.
- Claude pool: protect the greater of 15% of the applicable full window or one material review plus an owner-return synthesis/checkpoint margin.
- Use the most restrictive applicable window; a near-term reset does not erase a weekly constraint. Percentages apply only when the denominator and sharing are actually known.
- If capacity cannot be observed, mark it unknown, avoid a broad parallel wave, run one conservative bounded section and reassess. Do not claim a reserve is available or exhaust an unknown pool in pursuit of saturation.

Check usage before dispatch, after meaningful waves and on a limit signal. Let workers estimate the next section and checkpoint before it would cross a reserve. Cap concurrency by pool and implementation ownership, not just the number of available worktrees. Do not convert these defaults into claims about task cost based on historical runs.

## Claude sleep / 5-hour limit

If Claude approaches or reaches its 5-hour limit, save the queue, local locks, current SHAs, review debt, owner packets and exact resume instructions. Ensure already-authorized worker packages have inputs, next sections, budgets and stop conditions; then allow independent workers to continue.

Codex continues authorized implementation/analysis and self-checks. Hermes continues research sections/checkpoints and evidence-backed second passes. Outputs requiring Claude review accumulate as `review-needed`; owner-level conflicts become locked packets. Workers do not self-approve, merge or repeatedly wake Claude. Claude resumes by reading the checkpoints and reviewing deltas rather than reconstructing every intermediate step.

The limit does not create new authority. If no coordinator capacity remains to dispatch, workers may generate/execute only in-package follow-ups. Cross-package changes wait for the coordinator or explicit owner instructions.

## When a pool reaches a limit

1. Save the active section and its artifacts, observed limit/reset and next runnable step; preserve file ownership and any owned process state.
2. Continue independent work using other pools only where capacity, model suitability and authorization are verified. Do not shift research into Claude merely because Hermes is limited.
3. If Codex is limited, Hermes can finish dossiers/market work and Claude can review available artifacts within reserve. Production implementation waits; Hermes does not become the coder.
4. If Hermes/Luna/Sol shares a limited Codex pool, stop shared discretionary work. A different model name or worktree is not a bypass. Use a genuinely separate authorized pool only if confirmed.
5. If Claude is limited, use the sleep behavior above. If all pools are exhausted or at protected reserves, checkpoint and stop new dispatch until reset or owner adjustment.

No automatic paid upgrade, credit purchase or reserve reduction. Avoid polling unchanged limits. Record reset/resume triggers, and do not promise workers will continue if the runtime has actually stopped them.
