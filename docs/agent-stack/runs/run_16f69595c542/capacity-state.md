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

`.missions/usage_probe.py` (outside the repo) reads the newest `rate_limits` record in `~/.codex/sessions`. A background shell watcher re-reads it every 60 s. At ≥ 90% it sends the running Codex worker a SUSPENDED message through `orca orchestration send`, with no model call. Codex reached **90% at 14:54Z: SUSPENDED**. The watcher sent `ctx_7cb483f8ec6b` the stop-at-safe-boundary message. Resume condition: a reading below 70%, or the reset time (18:28Z) passing, wakes the coordinator. The reset is then verified on the first Codex activity before more than one task is admitted.

## Claude readings (2026-10-20 ~15:00Z)

Claude Code transcripts (`~/.claude/projects/*/*.jsonl`) record token counts for each message. They contain a `quotaLimits` record only when a request is **rejected** at a limit; that record has the type (`five_hour` or `seven_day`) and `resetsAt`. No plan percentage is stored locally.

The probe now reports Claude tokens over the trailing 5 hours as a relative load signal: output 632k, cache writes 1.99M, cache reads 141M. It also reports the last rejection, which is none in the last 5 hours.

Percentages for Claude still come from owner observations. A rejection record moves Claude to SUSPENDED until its `resetsAt`. `~/.claude/.credentials.json` holds credentials and is not read.

Codex 14:57Z: 92%. The in-flight worker overshot after the SUSPENDED message, and no new Codex work has been admitted.

## Claude calibration with ccusage (2026-10-20 15:27Z)

The tool is `npx -y ccusage@20.0.30 claude blocks --offline`. The version is pinned to an older release: MIT, no dependencies, it reads `~/.claude/projects` locally, and `--offline` stops it fetching prices. It was owner-suggested and is not installed globally.

**Estimated cap.** The 5-hour block that hit Claude's limit on 2026-10-19 to 20 began about 21:20Z; it was rejected with a reset at 02:20Z. It had used **$43.15** cost-equivalent, with 416k output tokens. That figure is the empirical cap. It is an estimate, because the provider's limit is not defined in dollars.

**Current block (14:00 to 19:00Z).** $19.02 used, about **44% of the estimated cap** (owner confirmed from Orca at 15:30Z: Claude 46%, Codex 92%). The burn rate is $13.07 an hour. At that rate the block would reach the cap around 17:15Z. That reading conflicts with the owner's ~6% observation, which may be a weekly figure.

**Mode: Claude CONSERVE until 19:00Z.**
- No new Claude worker is dispatched; the observer-spec worker `ctx_d68c424d40ac` finishes.
- The coordinator acts only on events.
- The conservative reading governs until a better reading exists.

**Codex** is SUSPENDED until 18:28Z (92%).

**16:15Z.**
- **Claude:** the current block is at $27.43, about 64% of the estimated cap (ccusage). That leaves roughly $11 to the owner's 90% ceiling. Only the observer-spec worker runs, no new Claude worker is admitted, and the coordinator is event-driven.
- **Codex:** SUSPENDED until the verified reset (18:28Z).
- **Queue at reset, in priority order:**
  1. MR1 fail-closed removal (owner approved);
  2. PR #36 reconcile.

## 2026-10-20 18:30Z checkpoint

- Codex: the provider-reported 5h reset (18:28Z) has passed. The last reading (92%, 14:57Z) is pre-reset. The first post-reset reading is being captured from the worker's own session; if it is ≥ 75%, dispatch stops.
- Dispatched owner-approved MR1 removal: dispatch `ctx_827752d8f6c3`, worktree `aspen-hide-research-areas`, base 3965dbf. The PR #36 reconcile stays queued until MR1 is reviewed (one Codex worker at a time while the reading is unconfirmed).
- Claude: ccusage active block $27.95 (~65% of the ~$43 calibrated cap), block ends ~19:00Z. No new Claude worker.
- 18:32Z: Codex reset verified by a fresh reading: 5h 1.0% (as_of 18:31:53Z, next reset 23:31Z), weekly 15%. Mode ACTIVE. Dispatched PR #36 reconcile: `ctx_645d9e8ebfa8`, worktree `other-listed-sites-v2`. Two Codex workers running (the cap).
