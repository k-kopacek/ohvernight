# Incident: Claude usage limit reached; the 90% protection did not act

Coordinator, 2026-10-20. The owner recorded it as: "The 90% usage protection failed."

## What happened

- **2026-10-20, about 01:00Z.** Following the owner's direction of 2026-10-19 to use authorized capacity, the coordinator started three Claude workers at once: M5 revision `ctx_a32dc644347c`, M6 spec `ctx_3d717c1af120` and PR #39 diagnosis `ctx_7825d4943902`. The coordinator session itself was also running on Claude.
- **01:10Z–01:13Z.** All three workers completed. Afterwards the coordinator session reached the claude.ai usage limit, and work stopped until the reset. The harness then reported: "Your claude.ai usage limit has reset."
- **No usage reading was taken at any point.** Every pool was recorded as `QUOTA_UNKNOWN` in `queue.md`.

## Why the protection did not act

1. **There was no telemetry.** Claude usage cannot be read from a supported source while the session runs (runtime assessment U5 and U6). The 90% rule could therefore never trigger. It is a policy without a sensor.
2. **The coordinator broke its own conservative rule.** `queue.md` said "one conservative section per pool" while capacity is unknown. The 2026-10-19 dispatch put four concurrent Claude sessions on one pool. Under `QUOTA_UNKNOWN`, the owner's direction to "use already-authorized capacity" did not override the charter's "fail conservatively". The coordinator read it as if it did, and that was a coordinator error.
3. **No checkpoint was triggered by elapsed work.** Without a sensor there was no proxy budget either: no cap on concurrent sessions and no cap on work per window.

## Impact

No work was lost: each worker had committed before it finished. Coordination stopped until the reset, which is the outcome the 90% rule exists to prevent. The owner lost the reserve the rule is meant to keep for interactive use.

## Corrective rules (in force for this run from 2026-10-20, within existing authority)

- **C1.** While Claude capacity is `QUOTA_UNKNOWN`, at most **one** Claude worker runs alongside the coordinator. Codex workers are a separate pool and are limited to two concurrent workers, also unknown.
- **C2.** A Claude worker is dispatched only after the previous one has reported `worker_done` and been released.
- **C3.** The coordinator reports no usage percentage it has not read from a supported source.
- **C4.** The permanent fix is the observer and admission controller (D7 i–iv). Until the lifecycle pilot proves it, no unattended or "autonomous across resets" claim is made.

## Follow-up

The observer/admission-controller specification draft (queue Q9) takes this incident as its first acceptance scenario. Admission must refuse a dispatch that would exceed the concurrency cap while capacity is unknown. It must checkpoint and suspend without model calls when a reading crosses `min(90%, 100% − reserve)`. It may resume only on a reset observed through supported telemetry, and must not dispatch the same work twice.
