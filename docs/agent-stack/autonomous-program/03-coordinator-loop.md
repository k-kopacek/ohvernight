# 03 — Coordinator loop and task selection

## Core recurrence

`RESTORE → OBSERVE QUOTA/STATE → PICK → PACKAGE → DISPATCH → WAIT → INDEPENDENT REVIEW → FIX → TEST → PR/OWNER GATE → CHECKPOINT → PICK AGAIN`

A report is a checkpoint, **not a reason to stop**. Finishing one worker task or emptying the initial queue does not end the program. The scheduler invokes the coordinator again for the next eligible wave (provided quota, authority and state checks allow it).

## Picking work

First satisfy trust/security regressions and existing approved incomplete work. Then choose the task on the shortest critical path to M8 and statewide usable coverage. Prioritize enabling product capabilities over layer counts; time-to-usable-trip and unresolved critical questions outrank raw number of ingested records. Identify urgent bugs from iPhone acceptance (such as shared mobile sheet/header defects). Do not convert deferred infrastructure into a priority.

Order by: (1) trust/safety, (2) unblock value, (3) dependencies, (4) verified user value, (5) effort/cost/usage, (6) maintainability. Shortlist at most five candidate tasks per planning cycle and dedupe. Task choice cannot bypass a protected spec or merge gate.

## Dispatch packet — mandatory fields

`task_id`, `parent_objective`, `actual_base_sha`, `assigned_role`, `branch/worktree`, `read_allowlist`, `write_allowlist`, `inputs + digest`, `acceptance tests`, `negative/trust cases`, `resource cap`, `stop_conditions`, `checkpoint_location`, `reviewer`, `expected_output`, `dependent_tasks`, `specific_authorization`.

Only one implementation worker may own overlapping production files. A long worker may run bounded subsections and checkpoint without summoning Claude after each. Review debts are queued if Claude is sleeping; Codex does not approve its own merges.

## Work completion classification

- `COMPLETE_REVIEWED`: independent review and objective checks pass at exact head.
- `READY_FOR_OWNER`: protected decision/merge/device gate; leave branch unchanged and proceed to another authorized task.
- `BLOCKED`: missing permissions/rights/source/critical invariant; preserve evidence and retry only with a changed authorized method.
- `PAUSED_QUOTA`: no new dispatch in affected account pool; scheduler will verify reset.
- `DEFERRED`: useful but not on critical path, insufficient rights or outside current scope.
- `SUPERSEDED`: documented alternative merged; preserve unique research before cleanup.

Never say `shipped` for a draft PR, local working tree or prototype. Merged code and published source claims must be distinguished. Only use finalized milestone labels after its release criteria pass.

## No infinite loops

A worker may perform one justified changed-method retry after diagnosing a failure. A coordinator planning pass is bounded to 30 minutes/10 task candidates. Two consecutive discovery passes with no new authorized useful work trigger `WAIT_NO_RUNNABLE_WORK`, not repeated reasoning. A limit signal triggers pause rather than launching another model/persona in the same shared allowance.
