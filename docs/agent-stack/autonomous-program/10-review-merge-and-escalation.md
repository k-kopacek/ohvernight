# 10 — Code review, merge authority and escalation

## Binding policy now

`AGENTS.md`, `docs/agent-stack/master-coordinator.md`, `docs/agent-stack/roles.md`, `docs/architecture/agent-stack.md` and ADR-002 require **owner approval for each PR and exact reviewed head SHA**. Main is deployed through GitHub Pages. Until an accepted owner-approved change to those controls exists, **the coordinator may not auto-merge** even under a broad instruction to “finish the project.” No agent may push directly to main, force-push or rewrite history.

## Current workflow

Claude spec → owner approval where current specs require → Codex implementation → independent Claude review → Codex fixes → exact-head CI/performance/device/source gates → owner exact-SHA merge authorization → merge and post-merge verification. An independent reviewer examines actual diff/source/claims; “approve with nits” never overrides a failing acceptance requirement. A changed head resets exact-head review/approval.

## Optional future standing delegation — requires separate owner governance approval

The owner may choose to amend the above files/ADR in a specific reviewed PR and delegate **low-risk, bounded** automatic merges only when ALL conditions below hold:

1. The merged autonomy charter and approved milestone spec explicitly cover the exact task and files. No new owner trust/product/source-use/material architecture decision was needed.
2. Same-head independent review PASS (not self-review); all required checks, security/source/payload/performance/device gates pass. Neither missing nor pending counts as pass.
3. No positive permission/access/legal/source claims requiring human confirmation were generated without that independent human review; no trust-bearing wording changes without the required approval.
4. No live refresh, account/service setup, new recurring charge, permission widening, external outreach, destructive migration or new data-source rights assumption.
5. No unresolved severe regression, owner STOP/PAUSE, approved budget threshold, branch-base drift, concurrent writer or unverified runtime state.
6. Merge is atomic with an exact expected SHA and confirmed base/check results; record PR, head, merge commit and rollback trigger; stop immediately on mismatch.
7. Deployment has a proven rollback plan; publish a concise release trace to the owner without requiring a reply.

Under this **proposed** policy, protected changes, M4-C approval of positive official claims as presently specified, mandatory owner phone acceptance not yet delegated, new sources/licensing and irreversible operations still need owner action. Standing merge delegation is OFF until explicitly enabled by an accepted governance change and enforced by runtime configuration. Do not turn it on because the owner stays silent.

## Device validation caveat

The owner has repeatedly found real Safari defects not reproduced by Chrome. Automatic merging of UI branches subject to a real-device owner gate would conflict with current requirements. The agent may build a more reliable Safari/device lab for approval, but must not quietly replace the human gate.

## Escalation packet

Only escalate genuine protected changes. Provide: exact decision, facts and sources, present approved behavior, options (including defer/unknown), risk and trust downside, recommendation, affected files/PR/base/head, validation and rollback, and **what other work can continue**. No vague “what next?” questions.

## Approved-by-silence is prohibited

Usage exhaustion, timeout, owner unavailability, a long successful test streak or a worker's internal conviction grants no production permission. The coordinator should continue independent allowed work, accumulating owner decisions instead of repeatedly asking.
