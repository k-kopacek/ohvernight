# 17 — Owner activation packet

**Status: AWAITING OWNER DECISIONS.** Coordinator, 2026-10-19. One packet for every decision needed to move from today's supervised operation to bounded autonomous development. Evidence: [16 — reconciliation](16-reconciliation-with-current-authority.md) and the Codex [runtime feasibility assessment](../proposals/autonomy-runtime-feasibility.md). Nothing below is active until the owner answers. Silence approves nothing.

## Bottom line

Development autonomy can start as soon as decisions D1–D3 are answered and the governance PR (D9) merges. That means continuous design, coding, testing, independent review and draft PRs within approved specifications, without asking at each step. Unattended operation across usage resets cannot start yet. The building blocks exist, but the assessment found nine UNKNOWNs (U1–U9), and the two most important are unresolved: Claude usage can't be read freshly while idle, and Orca can't hand an orphaned run to a new coordinator. D7 approves the work that would resolve them. Until then autonomy is `RUNTIME_NOT_READY`: the coordinator works while a session is open and checkpoints when it closes.

## Decisions

| ID | Decision | Options | Recommendation |
|---|---|---|---|
| D1 | Adopt the target product and charter (files 00–15) as the program's direction | Approve / approve with changes / reject | **Approve.** The charter preserves every current trust, licensing, merge and device rule. |
| D2 | Merge authority (C1) | (a) **Conservative:** owner approves each exact-SHA merge; agents run everything up to that point. (b) Delegated low-risk merges under the conditions in file 10, via a new ADR superseding part of ADR-002. | **(a) now.** Revisit (b) after the runtime has run under supervision without incident. Main deploys production; your iPhone checks have found Safari defects that Chrome missed. |
| D3 | Specification approval for M5–M8 (C2) | (a) Owner approves each milestone spec once; inside it, agents decide everything routine. (b) Coordinator writes and adopts specs within the charter. | **(a).** One review per milestone is where product and trust decisions concentrate; everything inside it proceeds without prompts. |
| D4 | Colorado-wide scope (C3) | Add a Colorado coverage program to `ROADMAP.md` as a delivery track with its own specification, or defer | **Add as a track.** Spec drafted after M4 closes; no loader or catalog change before that spec is approved. |
| D5 | Usage ceiling (C4) | (a) `min(90%, 100% − current reserve)` per window: at most 75% consumed for the shared Codex/Hermes pool and 85% for Claude. (b) 90% hard ceiling with the next-day implementation cost kept as a predictive stop. | **(a) until telemetry is verified (U5/U6, U8); then (b).** The assessment shows that only conservative admission is possible today, not a hard ceiling. |
| D6 | Where run state lives (C5) | Sanitized queue, locks, approvals and reports in `docs/agent-stack/runs/`; lease, heartbeat, quota and session IDs in private host state | **Approve** (one sentence in `master-coordinator.md`). |
| D7 | Runtime path (C6) | Approve, in order: (i) a specification for a model-free observer and admission controller (no activation); (ii) its offline implementation with the tests in the assessment; (iii) one documented authenticated quota read each for Codex (`account/rateLimits/read`) and Claude (a selected-field status-line bridge), using existing sign-ins, with no extra model calls; (iv) an isolated lifecycle pilot in a disposable Orca run, with your permission to restart Orca, sleep and reboot once, covering U1–U4 and U7; (v) activation, decided separately afterwards. | **Approve (i)–(iv). Decide (v) after reviewing the pilot results.** |
| D8 | Record the local Qwen/Odysseus pause in the repository (K1) | One line in `tools/local-ai/qwen/README.md` | **Approve.** |
| D9 | Governance PR | The coordinator prepares one documentation PR applying D2–D6 and D8, plus corrections K2, K3 and K6, to `AGENTS.md`, `master-coordinator.md`, `roles.md`, `agent-stack.md`, `capacity-routing.md`, `ROADMAP.md`, ADR-002 and the Qwen README | **Approve preparation.** That PR still needs your exact-SHA merge approval. |

Not decisions, recorded for completeness: Hermes web research stopped on 2026-10-08 with a billing error (K4); no spending happens without you. No standing merge permission exists, and none is activated by this packet.

## What continues regardless of these answers

M4-B final gate (your iPhone check, then exact-SHA approval of PR #17); the shared mobile-sheet structural fix (in review); draft PRs #15, #20 and #22–#36 awaiting review; M4-C preparation within the approved M4 specification; read-only M5–M8 research.

## How to answer

Reply with one line per decision, for example: `D1 approve; D2 a; D3 a; D4 add; D5 a; D6 approve; D7 i-iv; D8 approve; D9 approve`. Any change of wording or scope can be given inline. Merging PR #38 itself records the proposal and this packet; it activates nothing.
