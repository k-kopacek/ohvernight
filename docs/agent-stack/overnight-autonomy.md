# Continuous overnight autonomy

Authority: [master-coordinator.md](master-coordinator.md). Capacity and sleep behavior: [capacity-routing.md](capacity-routing.md). This is an operating contract for authorized runs, not an instruction to schedule a run or bypass an approval gate.

## Recursive operating loop

**EXECUTE → REVIEW → IDENTIFY GAPS → GENERATE TASKS → PRIORITIZE → DISPATCH → REPEAT.** Initial queue completion is not a stop condition.

1. Execute runnable bounded sections with independent Codex/Hermes packages.
2. Review outputs against section acceptance criteria. Workers perform local self-checks; Claude performs independent production review and material synthesis when available.
3. Identify missing evidence, contradictions, invalid assumptions, untested failure modes and promising opportunities.
4. Generate concrete follow-up tasks with dependencies, an evidence anchor and expected decision value. Deduplicate against completed work and existing queue entries.
5. Prioritize by current M4 correctness/trust, unblock value, evidence value and effort/capacity. Favor work that reduces an owner's decision burden; keep implementation reserve protected. Future research remains preparation.
6. Dispatch non-overlapping independent packages and repeat. Workers may extend their own queue only within its purpose, allowlist and total budget; cross-worker dispatch belongs to the coordinator.

## Local locks and global stops

**Owner gates are LOCAL LOCKS, not GLOBAL STOPS.** Each lock names the exact action, dependent tasks, evidence, owner decision and unlock condition. A PR waiting for approval cannot merge; workers can still audit it, build reports, prepare tests and pursue unrelated research. A South Platte extent decision locks extent/rule changes, not a read-only topology diagnosis or other river analysis. CPW uncertainty locks structured persistence/reuse, not M4-A/B/C preparation.

A spec stop-and-report condition applies to that production action. Do not keep editing the affected surface under the label “preparation.” Save the failure evidence, prepare options and proceed only with independent allowed work. Timeouts and silence never unlock a gate.

## Bounded discovery passes

After each completed wave and whenever the runnable queue empties, inspect:

- M4 evidence completeness, source semantics, freshness, legal/access claim risks and contradictions.
- Canonical/display preservation, aliases, grouping invariants, major rivers and threshold sensitivity.
- Tests, mutation/negative cases, byte/time budgets, device acceptance preparation and cleanup.
- Source/terms health, missing datasets and future M5–M8 research dependencies.
- User complaints, repeated app switching, monetizable workflows, first-customer hypotheses and bear cases.

Default discovery pass: at most 30 minutes and 10 candidate tasks. These are configurable local planning defaults, not measured provider limits. Score each candidate for novelty, relevance, confidence and cost. A candidate whose only next action is protected becomes a decision packet, not runnable production work. Avoid resurveying the same sources without new evidence or a sharper question.

Saturation means **two consecutive bounded discovery passes** produce no novel, authorized, useful runnable task. Record the searches/areas covered and why candidates were rejected, deferred or locked. Resume when new evidence, capacity, an owner decision or a changed repository state appears.

## Task package format

Every task includes:

| Field | Required content |
|---|---|
| ID / purpose | Stable ID, question/problem and practical value |
| Output | Exact artifacts and observable acceptance criteria |
| Bounds | Input/base SHA, read/write allowlists, dependencies, excluded milestones and operations, source/search/time limits |
| Stop | Owner gates, failed guards, section/total budget and checkpoint/resume trigger |
| Model | Worker role/model, reasoning level if configured, relevant pool and reserve |
| Why | Why this worker/model and why this task now; evidence anchor and expected decision value |
| State | Queued/runnable/running/self-checked/review-needed/locked/done; owner, last checkpoint and next section |

The package must be sufficient to keep working while Claude sleeps. Do not use “ask Claude what to do next” as a section completion criterion.

## Checkpoints and recovery

Save a checkpoint after every bounded section and before a retry, model switch, pool limit or risky operation. Use the run layout in the master contract. Include task/section status, UTC timestamp, exact input SHA, completed artifacts, tests/commands and results, unresolved evidence, consumed budget, locks, next runnable section and precise resume instructions. Preserve draft and approval labels.

Default technical section: at most 60 minutes before a checkpoint; research sections also honor [hermes-research.md](hermes-research.md) query caps. Long jobs need progress/timeout monitoring and an interruption-safe checkpoint, not a request to Claude every few minutes.

For a hang or loop:

1. Inspect actual worker/process state and last meaningful progress. An active long calculation is not a hang merely because it is quiet.
2. Checkpoint the evidence; stop only the worker/task-owned stuck operation where safe. Preserve logs and unrelated processes.
3. Allow one bounded retry with a changed method, exact starting source or smaller section. Never repeat the same unsuccessful search/command indefinitely.
4. If unchanged failure repeats, lock that section with the error and recovery requirement. Move to another runnable section; do not launch a duplicate writer or destroy its worktree.
5. Repeated tasks without novel output trigger deduplication and a saturation check, not another broad rerun.

## Stopping and owner return

One worker finishing, one pool reaching a limit, a completed initial queue or an unanswered owner gate is not a global stop. At a protected reserve, stop discretionary work for that pool, save state and move only to a compatible authorized pool with spare capacity. At Claude's limit, independent workers continue within their contracts.

Stop the run for the master contract's global conditions: explicit owner stop; unsafe shared state; missing master contract; no usable authorized capacity above reserves; or documented saturation. If all work is owner-locked and discovery yields no independent task, checkpoint and wait. Leave an owner-return report, queue/locks, artifacts and exact resume points. On owner return, report clearly before further long dispatch; continue only within standing authorization.
