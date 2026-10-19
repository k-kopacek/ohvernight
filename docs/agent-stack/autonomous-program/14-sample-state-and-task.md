# 14 — Example operational artifacts (not live state)

The examples below are **illustrative**. They are not proof that Orca exposes these APIs, that any quota snapshot exists, that the model can sleep/wake itself, or that these tasks have been approved.

## Example task packet

```yaml
task_id: M6-TRAIL-IDENTITY-003
parent_objective: M6 trail grouping and verified trailhead relationships
status: QUEUED
repo_remote: k-kopacek/ohvernight
base_sha: VERIFY_AT_DISPATCH
branch: feature/M6-trail-identity-003
worker: Codex
reviewer: Claude
inputs:
  - docs/specs/M6-...  # only when approved
  - relevant source records with identifiers and checked rights
write_allowlist:
  - assigned test and trail-identity implementation paths
excluded:
  - legal permission invention
  - source refresh outside approved scope
  - main merge
acceptance:
  - source IDs and canonical records remain unchanged
  - explicit negative cases for same-name unrelated trails
  - independent review and CI at exact head
stop:
  - unapproved licensing or unknown source semantics
  - ambiguous source identity
checkpoint: PRIVATE_RUN_STATE/task-M6-TRAIL-IDENTITY-003.json
```

## Example quota snapshot — test fixture only

```json
{
  "pool_id": "codex-subscription-pool",
  "window_type": "weekly",
  "used_pct": 90,
  "observed_at_utc": "EXAMPLE_ONLY",
  "reset_at_utc": "EXAMPLE_ONLY",
  "source": "VERIFIED_ADAPTER_REQUIRED",
  "confidence": "example-not-observation",
  "consumers": ["codex-worker", "other-shared-consumers"],
  "decision": "PAUSED_QUOTA"
}
```

## Example recovery checklist

```text
[ ] exact repo and remote match
[ ] accepted charter and current spec SHA verified
[ ] owner stop not set
[ ] scheduler lease acquired; prior leases reconciled
[ ] Orca live sessions reconciled with queued tasks
[ ] GitHub PR exact heads / CI observed
[ ] no unprotected overlapping implementation writer
[ ] quota snapshots fresh and all relevant windows below stop rules
[ ] owner locks remain locked until actual approval
[ ] next task has explicit write allowlist and finite budget
[ ] progress saved atomically before launch
```

## Example final completion message

`OHVERNIGHT COLORADO V1 — OWNER PRODUCT CRITIQUE READY`

Include: production and staging SHAs, scenarios and phone test outcomes, use-case completion, evidence/claim coverage by topic/region, unknowns and trust exceptions, performance, licensing, merge audit and rollback. “Owner critique ready” is not proof that the owner has approved every release gate.
