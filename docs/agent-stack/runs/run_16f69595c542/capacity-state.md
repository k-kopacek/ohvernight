# Run run_16f69595c542 — capacity state

Sanitized; account, session and lease details stay in private host state. Policy: owner direction 2026-10-20 (proposed in PR #40 `capacity-routing.md`; the existing reserves remain binding).

| Pool | Latest observation | Source | Mode | Admission |
|---|---|---|---|---|
| Codex (shared with Hermes) | **Machine reading 2026-10-20 14:52Z: 5-hour window 88% (resets 18:28Z); weekly 14% (resets 10-27 13:28Z)**, from Codex session logs via the model-free probe `.missions/usage_probe.py`. Earlier: ~78% (owner observation); **owner-authorized exception 2026-10-20 ~14:40Z: 'allow it to keep working'** — PR #39 toolbar-pin task `ctx_7cb483f8ec6b` running, 2026-10-20 ~14:25Z | Owner planning observation (not telemetry) | **SUSPENDED for new work** (past the 75% effective ceiling under the 25% reserve; above CONSERVE in any case) | The one running bounded section (`ctx_e63673a0f954`, PR #39 test-sequencing fix: one test file, already in validation) may finish. Nothing new is admitted |
| Claude | ~6% consumed, 2026-10-20 ~14:40Z | Owner planning observation (`orca usage` is not available in Orca 1.4.224, so there is no machine reading) | ACTIVE; primary worker (owner: transition work to Claude). No machine-readable Claude usage file found: Claude Code's status-line `rate_limits` goes to Orca's hook and is not persisted (`last-status.json` does not keep it). Owner observations are used until a reading exists | Cap raised from one to three concurrent Claude workers on the owner's observation: observer spec `ctx_d68c424d40ac`, M7 spec `ctx_d6dd8647b5a8`, Codex-ready briefs `ctx_d63fcb401482`. Re-check against the owner's next observation before adding more |
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

## Model-free monitoring

`.missions/usage_probe.py` (outside the repo) reads the newest `rate_limits` record in `~/.codex/sessions`. A background shell watcher re-reads it every 60 s. At ≥ 90% it sends the running Codex worker a SUSPENDED message through `orca orchestration send`, with no model call. Mode now: Codex **CLOSING**, and `ctx_7cb483f8ec6b` has been told to checkpoint at its next safe boundary.
