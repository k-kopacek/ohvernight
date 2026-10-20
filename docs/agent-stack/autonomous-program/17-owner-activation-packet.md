# 17 — Owner activation packet

**Status: AWAITING OWNER DECISIONS.** Coordinator, 2026-10-19; consolidated the same day at the owner's direction. This is the one packet for PRs #38 (this charter) and #40 (the governance amendments). Evidence: [16 — reconciliation](16-reconciliation-with-current-authority.md) and the Codex [runtime feasibility assessment](../proposals/autonomy-runtime-feasibility.md).

Nothing below is active because a draft PR exists, because a PR merges, or because the owner is silent. Each grant takes effect only from the owner's explicit answer, and merging #38 and #40 records those answers; it does not add to them.

## Three separate grants

Autonomy is split into three grants. Each one is decided on its own, and approving one never implies another.

| | Grant | What it allows | What it never allows | Decisions |
|---|---|---|---|---|
| **1** | **Development autonomy** | Inside an owner-approved milestone spec: continuous design, coding, testing, independent review, CI, draft PRs, rebases, research and spec drafting, without asking at each step. The coordinator escalates only protected decisions. | Merging. Changing trust wording, thresholds, licence interpretations or source selection. Starting work on a milestone whose spec is unapproved, beyond drafting and read-only research. Spending money. | D1, D3, D4, D6, D8 |
| **2** | **Production-merge authority** | Unchanged: an agent merges only after the owner approves that specific PR at its exact head SHA. | Any standing or delegated merge permission. Auto-merge. Merging because CI is green or a review passed. | D2 |
| **3** | **Unattended runtime** | After the pilot and a separate activation decision: work continuing across sessions and usage resets under a model-free supervisor. | Starting before the pilot is reviewed. Bypassing a usage limit by changing account, model or identity. | D5, D7, D10 |

Grant 1 needs nothing from grants 2 or 3. Until grant 3 is activated the program is `RUNTIME_NOT_READY`: the coordinator works while a session is open and checkpoints when it closes.

## Recommended defaults — one reply accepts them all

| ID | Decision | Recommended default |
|---|---|---|
| D1 | Adopt the target product and charter (files 00–15) as the program's direction | **Approve.** The charter keeps every current trust, licensing, merge and device rule. |
| D3 | How M5–M8 specs are approved | **(a)** The owner approves each milestone spec once. Inside it, agents decide routine matters. |
| D4 | Colorado-wide scope | **Add a Colorado coverage track** to `ROADMAP.md`. Its spec is drafted after M4 closes. No loader or catalog change before that spec is approved. |
| D6 | Where run state lives | Sanitized queue, locks, approvals and reports go in `docs/agent-stack/runs/`. Lease, heartbeat, quota and session IDs stay in private host state. |
| D8 | Record the Qwen/Odysseus pause in the repo | **Approve** one banner line in `tools/local-ai/qwen/README.md`. |
| D2 | Merge authority | **(a)** Per-PR exact-SHA owner approval stays. A delegated low-risk merge policy (file 10) would need its own ADR. That ADR is not proposed now. |
| D5 | Usage ceiling and provider modes (updated 2026-10-20) | **(a)** `min(90%, 100% − reserve)` per window: at most 75% of the shared Codex/Hermes pool and 85% of Claude. The owner's modes (CONSERVE at 75–80%, CLOSING at 85%, SUSPENDED at the ceiling, Claude pivot) apply within that limit (PR #40, `capacity-routing.md`). Under the current 25% reserve the Codex pool is therefore SUSPENDED from 75%, and the 85% and 90% stages take effect only if you also choose **(c) lower the Codex/Hermes reserve to 10%**. The coordinator recommends keeping 25% until a verified quota reading exists (U5, U6), so that a mis-estimate cannot exhaust the pool. |
| D7 | Runtime path | **Approve (i)–(iv):** (i) observer/admission-controller spec, (ii) offline implementation and tests, (iii) one authenticated quota read each for Codex and Claude using existing sign-ins, (iv) a disposable lifecycle pilot, with permission to restart Orca, sleep and reboot once. **(v) activation is decided later**, after the pilot results. |
| D10 | Codex startup update prompt | The owner is handling the prompt in the terminal (2026-10-19). **Also approve (c)** within D7: a Codex setting that suppresses the startup update check for agent launches, so an unattended run is never stopped by it. The owner applies updates deliberately. |
| D9 | Governance PR | Draft PR #40 already applies these defaults. If an answer differs, it is edited to match before approval. |

## Communication (owner direction 2026-10-20)

One consolidated daily report, plus exceptions: a milestone, an owner decision, a critical blocker, an unresolvable acceptance failure, or a prolonged suspension. Routine worker events are recorded in run state, not messaged. This is proposed in `master-coordinator.md` (PR #40).

## Material risks, flagged separately

- **R1 — Development autonomy is a real change.** Under grant 1 the coordinator dispatches and reviews without asking. The owner sees work at three points: spec approval, each exact-SHA merge, and the iPhone checks. Bear case: a misdirected sequence of draft PRs costs agent capacity before the owner sees it. Mitigation: work is confined to approved specs, and every PR stays a draft until the owner acts.
- **R2 — No delegated merge.** Keeping D2 (a) means every production change waits for the owner. That is the throughput limit, and it is intended. Main deploys production, and real-device checks have repeatedly found Safari defects that automated checks missed.
- **R3 — Quota telemetry is not verified (U5, U6, U8).** Until D7 (iii) succeeds, every pool is `QUOTA_UNKNOWN`. Dispatch stays attended and conservative. No usage percentage is reported.
- **R4 — The D7 (iv) pilot restarts Orca and reboots once.** It runs in a disposable run, only with this approval.

## Approval order

1. Answer this packet, in the format below.
2. Approve PR #38 at its exact head SHA. This records the proposal and the answers.
3. Approve PR #40 at its exact head SHA. This applies them to the canonical contracts.

Grant 1 starts when #40 merges.

## How to answer

`Autonomy: accept defaults`, or list changes inline, for example `Autonomy: accept defaults except D4 defer`.

## Recorded, not decisions

- **K4.** Hermes web research stopped on 2026-10-08 with a billing error. No spending happens without the owner.
- **Paused.** Local Qwen/Odysseus work stays `PAUSED_BY_OWNER`.
- **Continues under current authority, whatever the answers:**
  - the M4-B final gates;
  - the PR #39 mobile-sheet fix;
  - M4-C commits 1–3, which need Codex;
  - spec drafting for M5 (PR #41) and the source-neutral part of M6;
  - review-debt triage.
