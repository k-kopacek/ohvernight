# 13 — Adoption and runtime implementation sequence

## Step 0 — documentary proposal (what this package provides)

Read, critique and approve the target product and scope. Commit these Markdown files in a docs-only PR through existing exact-SHA approval; add minimal pointers to `AGENTS.md` and the existing coordinator contract once accepted. Do not alter original historical decisions without an explicit amendment. Record any obsolete milestone status from live Git, not an invented completion report.

## Step 1 — authority decision (separate protected gate)

Decide if owner wants **development autonomy only** (full independent planning/coding through draft PRs, owner still merges) or **bounded standing merge delegation**. If delegation is chosen, prepare a separate reviewed ADR/AGENTS/agent-stack PR with exact conditions in `10-review-merge-and-escalation.md`; until merged, no automatic merge. Decide whether approved scope extends production implementation of M5–M8 without new owner-approved specs, or whether milestone specs will still be owner-approved. This is necessary to avoid falsely claiming “no questions until final.”

## Step 2 — runtime feasibility spike (read-only first)

Codex inspects installed Orca version-matched skill/CLI, Claude and Codex real account/usage interfaces, OS scheduler options and current running workers. Produce **supported** control surfaces and limitations: `QUOTA_TELEMETRY_VERIFIED` or `QUOTA_UNKNOWN`; `ORCA_PERSISTENCE_VERIFIED` or `RUNTIME_NOT_READY`. Do not install a daemon, change permissions, access undocumented account endpoints or issue model requests without separate authorization.

## Step 3 — build smallest host-side supervisor (requires owner-approved task)

Implement state machine, atomic lease/checkpoints, owner stop switch, worker reconciliation, quota probes and wake timer as an isolated testable package. Dry-run without model calls. No public network listener, no broad tool auto-approval and no credentials in logs. Pass failure/restart/overlapping-quota tests and independent review. Installation/autorun is separately approved.

## Step 4 — short, supervised burn-in

Run a bounded, visible session with trivial already-authorized Ohvernight work to verify:

- complete tasks without prompting owner for routine choices;
- checkpoint and resume after a simulated quota pause;
- recover after intentional scheduler restart;
- avoid duplicate dispatch or overlapping writers;
- preserve existing repo/PR/device/security gates;
- report exact usage source/reset and any unknown fields.

Do NOT artificially consume the subscription to reach 90%. Inject simulated snapshots into a dry-run; live validation can use naturally occurring changes if safe.

## Step 5 — enable persistent unattended mode

Only after acceptance and approval: schedule coordinator waves through verified Orca supported invocation; require quota probe freshness and branch/worker reconciliation on every dispatch. Restrict scope to accepted charter; keep independent product review and human-protected gates. Do not assume the owner never needs to be contacted if source claims require human verification.

## Step 6 — scope-to-product delivery

Build M4 completion → M5/M6/M7 evidence relationships → Colorado continuous discovery → M8 ranked candidates under accepted specs. Track progress with product scorecard and user scenarios, not just feature counts. At the end produce the final product critique bundle and stop creating new features.

## Proposed one-line references, NOT applied

- `AGENTS.md`: “For the owner-approved bounded autonomous product program, see `docs/agent-stack/autonomous-program/README` [actual path]. Its authority is limited by the existing specs/ADRs and the adopted governance policy.”
- `docs/agent-stack/master-coordinator.md`: “If enabled by an approved PR, follow `autonomous-program/12-coordinator-bootstrap.md` for scope, quota and durable runtime; no silent change to exact-SHA merge or source/owner gates.”

Correct path/wording and approvals at implementation time; these are examples, not code changes.
