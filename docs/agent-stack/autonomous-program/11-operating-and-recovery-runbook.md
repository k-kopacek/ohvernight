# 11 — Runtime operations, pause, failures and final report

## Run lifecycle

Before launch verify Git remote/main, AGENTS, accepted specs, owner-approved autonomy activation, Orca orchestration interface, worker capacity accounting, actual worktrees and approvals; refuse startup if missing critical instructions or scheduler lease. Load the **latest committed** policy, not local draft README.

## Pause/stop reasons

- `PAUSED_QUOTA`: Claude or Codex pool near budget; resume only after verified capacity.
- `WAIT_OWNER`: protected policy/spec/source/device/merge gate; continue unrelated tasks.
- `BLOCKED_SOURCE`: legal reuse rights or official source semantics unresolved; do not infer permission.
- `BLOCKED_TRUST`: tests/claims conflict with normative policy; fail closed.
- `BLOCKED_RUNTIME`: scheduler state, worker identity or checkout cannot be trusted; stop dispatch and inspect.
- `WAIT_NO_RUNNABLE_WORK`: two bounded discovery passes found none; low-cost host schedule checks for new approved work/owner decision.
- `STOPPED_BY_OWNER`: do not dispatch, merge, restart or continue until explicit owner restart.

## Runtime supervisor health checks

Use a monotonically increasing event ID/lease, stable task IDs and idempotent worktree creation. Record actual Orca worker state and pending approval prompts. Health is not “a terminal exists”: require observed progress/expected process and heartbeat. A prompt waiting for a permission approval must alert and checkpoint, not grant permissions via broad auto-approve. Treat reported CI/performance results as assertions pending exact-head verification.

## Quota wake examples

If Claude 5-hour window resets but its weekly window remains at 93% used, **keep Claude asleep**. If Codex has available 5-hour capacity but shares exhausted weekly allowance with another runner, **keep Codex asleep**. If both show verified headroom but no independent reviewer is available, implementation drafts may continue; no self-review and no unauthorized merge. If neither usage source can be read, stop unattended requests rather than estimating from wall time.

## Failure & rollback

For a timeout or crash, checkpoint and inspect worker before retry. Retry only once with changed bound/method if authorized. For failed merge/CI/device tests, preserve evidence and isolate that PR. For source-license or critical trust defect in published production, prioritize disable/revert only under existing authorized deployment/rollback policy; notify owner and do not conceal unknowns. Never auto-delete ignored datasets or abandoned worktrees based solely on `git status`.

## Daily progress without owner dependency

Produce one concise **progress packet** per day or meaningful milestone: merged versus draft SHAs, new user-capable behavior, scenario delta, open trust/coverage risk, capacity/sleep state, active workers, next actions and protected owner asks. Reports are informational, not a prompt/answer blocking rendezvous. A paused system reports pause honestly; no promise of work continuing without a verified host scheduler.

## Final critique package

When the entire scoped product reaches its acceptance bar, stop new feature dispatch. Provide product demo, release matrix, known unknowns and coverage, source/license evidence, security/privacy and CI state, iPhone results, ranking explanations, user scorecard and technical-debt decisions. Label only demonstrably merged/deployed capabilities SHIPPED. Hand off to owner for critique and requested revisions. Do not claim “complete” from passing tests alone.
