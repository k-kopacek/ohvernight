# 06 — Durable state, resumption and artifact boundaries

## Two different kinds of truth

- **Institutional truth:** accepted specs/ADRs/roadmap/code/data, plus GitHub PRs and reviews. This lives in Git and requires existing approval for material changes.
- **Operational truth:** which worker is currently running, last heartbeat, quota meter, lease, pending model request and temporary artifacts. It lives in restricted host state, not a public Git branch. Some sanitized work-product checkpoints may be committed to a dedicated run branch/PR under current authorizations.

Do not assume a local `.missions/` directory is replicated or that an unmerged checkpoint is approved policy. Do not commit hostnames, IPs, detailed usage/account data, raw agent transcripts, private prompts, credentials, ignored raw source archives or scraped third-party content without explicit rights review.

## Minimal structured operational state

Recommended fields (implementation schema must be validated before scheduler deployment):

- `schema_version`, `program_id`, `run_id`, `scheduler_owner`, `lease_id`, `heartbeat_utc`;
- `repo_remote`, `main_sha_observed_utc`, `active_branch`, `active_worktree`;
- `milestone`, `current_spec_sha`, `approved_scope_digest`;
- `task_queue[]`: stable ID, dependencies, output contract, assignee, state, base/head SHA, checkpoint, reviewer and gating conditions;
- `active_orca_sessions[]`: actual session/job identifiers, verified start state, ownership and latest progress;
- `review_queue[]`, `owner_locks[]`, `approvals[]` with **exact PR/head** where applicable;
- `quota_pools[]`: recent verified snapshot reference, shared consumers, projected next usage, sleep/wake reason;
- `next_action`, `last_transition_utc`, `event_sequence`, `last_error`, `state_checksum`.

Schema belongs to an implementation task; the examples in `14-sample-state-and-task.md` are illustrative only.

## Durable checkpoint rhythm

- Before launch, after every bounded subsection (at most 60 minutes by existing guidance), before a quota threshold/retry/merge and on every worker exit.
- Use atomic write-and-rename, schema validation, file permissions, versioned backup or append-only event log; flush before declaring checkpoint success.
- Save raw benchmark datasets only where rights and privacy allow; for durable Git evidence save sanitized report and hashes/relative references.
- Record **actual** base/PR SHAs, exact tests run, observed results, pending checks and the first next action. Never write guessed PASS/CI status.

## Recovery algorithm

1. Acquire scheduler lock; check an owner STOP file or equivalent.
2. Verify correct repo remote, canonical files, main head and current branch/worktree state without destructive cleanup.
3. Inspect GitHub PRs and CI, real Orca sessions, local process list, leases, checkpoint/event log and usage snapshots.
4. Reconcile discrepancies: a task with a live worker is `RUNNING`; an unobserved completion is `UNKNOWN_COMPLETION`, not `DONE`; a merged PR is `MERGED` only after matching exact GitHub evidence.
5. Resume the next bounded subsection from its last verified input SHA. A checkpoint marked completed must never be rerun unless acceptance evidence is invalid and a new task is logged.
6. Re-evaluate owner locks, trust/safety gates and quota. Then dispatch at most once.

## Ownership, cleanliness and worktree disposal

Review `git status --ignored`, untracked files, unique commits, raw/staged data, open terminals and reviewer-owned branches before any cleanup. Clean Git status is not proof no valuable ignored data exists. No force push or destructive worktree cleanup without policy. Recovery must preserve M4 source/staged data, review scratchpads and unique research unless an explicit retention decision permits removal.
