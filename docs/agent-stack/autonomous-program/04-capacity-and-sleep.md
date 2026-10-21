# 04 — Usage accounting, 90% ceiling and sleep/wake

## Scope and limitations

This is a **control policy**, not a working provider usage API. No claim is made that the installed Claude, Codex or Orca versions expose remaining allowance programmatically. Verify supported installed interfaces first. Official Codex guidance says `/status` can show usage and resets in an interactive session; that does not establish an unattended machine-readable API. Claude subscriptions, Claude API billing, Codex plans/credits and shared pools differ.

Do not scrape authenticated web pages, undocumented account endpoints, private credentials or shell history to infer limits. Do not assume session context utilization equals account usage.

## Usage snapshot contract

A trusted host-side adapter, if available, produces for each distinct **account-level pool and applicable window**:

`pool_id; provider; meter_id; window_type (e.g. 5h, weekly, spend); used_pct (0..100) or remaining_pct; reset_at_utc (nullable); observed_at_utc; source; account_scope; confidence=verified; consumers[]`.

Persist the snapshots separately from source control; no auth tokens or account identifiers in public run reports. Each dispatch must know which pool(s) it consumes. Different worktrees, model aliases and Orca sessions do NOT create new quotas. Unknown sharing is conservatively treated as shared.

## Safety policy

- **Hard ceiling:** `used_pct >= 90` in ANY applicable metered window means `PAUSED_QUOTA` for every consumer of that pool. No new paid worker/coordinator/model request from that pool. Do not try to fill the last 10%.
- **Predictive stop:** At lower percentages, pause dispatch if the conservative estimated cost of the next bounded section could cross 90%. Begin checkpointing before the threshold (suggested at ~85%) and require a complete, durable checkpoint before a predicted crossing.
- **Current default reserves:** Existing `capacity-routing.md` uses planning defaults of 15% Claude and 25% shared Codex/Hermes remaining. Unless changed by an explicit owner-approved policy, these stricter reserve floors apply **before** the 90% ceiling (effectively pausing around 85%/75% consumed). Do not silently override them to reach 90%. To use 90% as the sole reserve ceiling, amend that file in the adoption PR with owner approval.
- **Multiple windows:** The most restrictive live window wins (5-hour, weekly and any other shared allowance). A 5-hour reset does not clear a weekly 90% condition.
- **Unverified meter:** If reliable allowance telemetry is absent or stale, `QUOTA_UNKNOWN`. No unattended paid dispatch predicated on a 90% guarantee. Save work and report what interface must be verified. A separately approved short supervised run is not proof of quota-aware autonomy.
- **Limit event:** Provider `rate_limit`/usage error means immediate pool pause even if snapshot claims capacity. Don't buy resets/credits or change provider/account/model to evade a cap.

## Wake protocol

A durable host scheduler, not a sleeping Claude process, waits for the earliest **relevant** announced reset. It may set a low-cost, bounded wake-check **after** that time, but must obtain a new verified quota snapshot and confirm EVERY gating window is below both hard and approved reserve thresholds before dispatch. Missing `reset_at_utc` -> require another supported signal or owner action; do not invent reset time.

While paused, Codex may finish an already authorized in-flight bounded section only if its own pool has verified headroom and no stop condition; otherwise checkpoint. A sleeping Claude cannot provide its own independent review, approve merges or create new cross-package assignments. Review outputs queue for wake.

## Host scheduler obligations

Use scheduler-native timers/queued jobs, no LLM polling. Avoid repeated wake prompts on provider limit errors. Record `sleep_reason`, `pool`, `window`, `snapshot`, `earliest_check`, `review_debt` and exact resume work. On restart, reread quota and runtime state, never trust yesterday's percent. Heartbeat failure triggers an operational alert/paused state, not “still working.”

## Acceptance tests for this policy

Simulate 89%, 90%, 91%; predicted crossing at 88%; 5-hour reset while weekly still 92%; independent accounts versus shared aliases; stale/unavailable quota; provider limit error; reset time passing without usage refresh; multiple consumers; scheduler restart during sleep; user revocation; account usage changing externally. No real provider usage should be spent by these tests.
