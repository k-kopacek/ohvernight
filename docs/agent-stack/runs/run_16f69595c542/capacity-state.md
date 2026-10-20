# Run run_16f69595c542 — capacity state

Sanitized; account, session and lease details stay in private host state. Policy: owner direction 2026-10-20 (proposed in PR #40 `capacity-routing.md`; the existing reserves remain binding).

| Pool | Latest observation | Source | Mode | Admission |
|---|---|---|---|---|
| Codex (shared with Hermes) | ~78% consumed, 2026-10-20 ~14:25Z | Owner planning observation (not telemetry) | **SUSPENDED for new work** (past the 75% effective ceiling under the 25% reserve; above CONSERVE in any case) | The one running bounded section (`ctx_e63673a0f954`, PR #39 test-sequencing fix: one test file, already in validation) may finish. Nothing new is admitted |
| Claude | ~1% consumed, 2026-10-20 ~14:25Z | Owner planning observation | ACTIVE (incident rule C1: one Claude worker beside the coordinator while there is no telemetry) | Observer spec worker `ctx_d68c424d40ac` running |
| Hermes | Unavailable (billing, K4); pool independence from Codex not verified | — | Not used | — |

Reset condition for Codex: a verified reset (a supported reading or an owner statement), then `READY_TO_RESUME`. The coordinator does not poll Codex usage with Claude.

## WAITING_FOR_CODEX_CAPACITY (implementation-ready or owner-gated)

| Task | State | Also gated by |
|---|---|---|
| Rebase #26, #28, #25 (drop `@expectedFailure`) after #22 merges | Ready once #22 merges | Owner approval of #22 |
| **PR #39 desktop toolbar-height pin** (CI 39440087880 at `e9d9f4d`: the mobile jitter check now passes; Douglas 1024-half toolbar is 75.5 vs a macOS-pinned 53, most likely a font wrap) — brief `.missions/codex-pr39-desktop-toolbar-pin.md` | Ready, **critical path for M4/#39** | Codex capacity |
| Rebase #27 onto main | Ready | — |
| Rebase #36 onto merged #39 (drop its own sheet changes) | Ready once #39 merges | L2 |
| Protected-token CI test (design D2) | Brief to write | Owner answer on PR #43 |
| M4-C commits 4–6 (real records) | Blueprint exists | L5 (C-1…C-5) |
| M5 PR A | Spec draft #41 | M5 approval |
| M6-A/B (source-neutral) | Spec draft #42 | M6 approval |

## Claude queue (pivot), in priority order, one worker at a time

1. Observer/admission-controller spec draft (running).
2. Implementation-ready Codex briefs for M5 PR A and M6-A, so Codex can start the moment the owner approves (briefs only; no production edits).
3. Coordinator review of PR #44 CI and PR #39 CI as they finish (coordinator, event-driven).

Next autonomous action: `ctx_e63673a0f954` is done (`e9d9f4d`, reviewed and pushed, worker released). PR #39 is WAITING_FOR_CODEX_CAPACITY on the toolbar-pin brief. Nothing further is admitted to Codex until a verified reset or an owner exception.
