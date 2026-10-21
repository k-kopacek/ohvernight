# Runtime observer and admission controller — specification

**Status: DRAFT — NOT APPROVED. Activates nothing (D7 i).**

Claude, 2026-10-20, written for owner decision D7 (i) in the [owner activation packet](../autonomous-program/17-owner-activation-packet.md) (charter branch `docs/autonomy-charter`). Base: `main` `3965dbf`. This document specifies software that does not exist. Writing or merging it installs, schedules, configures and enables nothing. No account, setting, permission, automation or launch service was changed while preparing it. The only commands run were read-only `--help` discovery, `git show` and mailbox checks for this dispatch.

## 0. Reading guide

| Section | Content |
|---|---|
| 1 | Purpose, scope, non-goals |
| 2 | Inputs and the evidence behind each rule |
| 3 | Architecture: one model-free observer process, one admission front door |
| 4 | Usage policy: pools, windows, ceiling, owner modes, caps, in-flight accounting |
| 5 | Telemetry sources, freshness and failure behaviour |
| 6 | State machines: controller, pool, attempt, mailbox item |
| 7 | Lifecycle: checkpoint, suspend, reset, resume exactly once, orphans, restart/sleep/reboot |
| 8 | Mailbox surfacing and coordinator wake (incident 2) |
| 9 | Startup and permission prompts |
| 10 | Security, permissions, kill switch, rollback |
| 11 | Acceptance: offline tests, scenarios, lifecycle pilot, activation boundary |
| 12 | Engineering choices decided here |
| 13 | Owner decision packet and material risks |
| 14 | UNKNOWN register |

Normative words: **must**, **must not**, **may**. Where this document says "decided", the choice is a routine engineering default that the implementer may tune only through review of this spec. It is not an owner question.

## 1. Purpose, scope, non-goals

### Purpose

Two incidents on 2026-10-20 showed that the current capacity rules are policy without enforcement:

1. **Incident 1 (~01:00Z).** Four concurrent Claude sessions ran on one pool while Claude capacity was `QUOTA_UNKNOWN`. The coordinator then reached the claude.ai usage limit. No reading was ever taken, so the 90% rule could not act ([incident record](../runs/run_16f69595c542/incident-2026-10-20-claude-usage-limit.md), branch `runs/run_16f69595c542`).
2. **Incident 2 (~18:35–21:30Z).** Two Codex workers sent blocking `question` and `escalation` messages. None was answered for about three hours. The coordinator relied on terminal notifications that never arrived.

This specification defines:

- a **model-free observer**: a small host process that reads telemetry and Orca state, keeps a private journal and makes **no LLM call**, whether it is observing, suspended or recovering; and
- an **admission controller**: a front door that every worker dispatch passes through. It admits or refuses each start or resume against the usage policy and records an idempotent intent before anything happens.

### In scope

Usage admission, concurrency caps, telemetry adapters, checkpoint/suspend/resume, duplicate-dispatch prevention, orphan and restart handling, mailbox surfacing, prompt detection, kill switch, tests and the D7 (iv) pilot plan.

### Non-goals

- **No planning authority.** The observer never chooses work, writes specs, reviews, approves or merges. It admits only packages that the coordinator or owner has already queued. It never creates a Task.
- **No coordinator replacement.** It never rebinds a Run, never sends as the coordinator with `--from` impersonation and never takes over a fenced Run (U4).
- **No competing framework.** Orca stays the only orchestration plane, Git the only institutional record. The observer is not an agent, has no prompt, and adds no scheduler beside Orca: no cron, no Orca automation, no second controller.
- **No quota bypass.** It never changes account, provider identity or model to get past a limit, never buys credits and never redeems a reset.
- **No guarantee of a hard ceiling.** It enforces conservative admission. Telemetry lag, external consumers and in-flight overshoot mean usage can still cross a threshold (risk MR1).
- **Unattended autonomy is not claimed.** See §11.4.

## 2. Inputs and evidence

| ID | Source | What this spec takes from it |
|---|---|---|
| A1 | `AGENTS.md`; `docs/agent-stack/{master-coordinator,roles,overnight-autonomy,capacity-routing,orca-bootstrap}.md` at `3965dbf` | Authority, checkpoints, reserves, local locks, no autonomous merge |
| A2 | `capacity-routing.md` on `k-kopacek/autonomy-governance` (PR #40) | Outer ceiling `min(90%, 100% − reserve)`; owner modes ACTIVE / CONSERVE / CLOSING / SUSPENDED / READY_TO_RESUME; Claude pivot; "no polling with a model"; unknown capacity blocks unattended dispatch |
| A3 | Charter `05-orca-runtime.md`, `04-capacity-and-sleep.md`, `06-checkpoints-and-recovery.md`, `16`, `17` (branch `docs/autonomy-charter`) | Supervisor duties, state split (C5/D6), wake protocol, D5, D7, D10 |
| A4 | `proposals/autonomy-runtime-feasibility.md` (Codex, 2026-10-19), same branch | Supported interfaces, journal design, U1–U9, failure table |
| A5 | Incident record, `runs/run_16f69595c542` | Scenario 1; rules C1–C4 |
| A6 | `capacity-state.md`, same run branch | Telemetry verified in this run; Codex overshoot 88% → 92% after the SUSPENDED message; reset at 18:28Z verified by a fresh reading at 18:32Z; ccusage calibration |
| A7 | Coordinator addendum, 2026-10-20 21:55Z | Incident 2 as scenario 2; telemetry evidence; ESTIMATE labelling; credential file is never read |
| A8 | `orca --help`, `orca orchestration --help`, `check`, `inbox`, `ask`, `send`, `reply`, `request-show`, `worker-start`, `worker-list`, `terminal wait`, `orca automations --help` (Orca 1.4.224 per A4) | The CLI verbs this spec relies on. Help text is evidence of interface, not of behaviour under restart |

CLI facts this design depends on, from A8:

- `check` by default consumes the oldest unacknowledged FIFO batch and replays it until `--ack`. `--peek` returns unread messages without marking them read; `--all` returns every message and does not mark read.
- `ask` notes: "Timeout leaves the question pending; resume with the original message ID."
- `worker-start` exits 0 only for `ready`. A failed or `outcome_unknown` start exits 1 and reports `stage`/`failedStage`, `effects`, `residualResources` and recovery commands. `--retry-of` needs `--task` naming the failed Task.
- `request-show --request <id>` reports whether a mutation already took effect.
- `terminal wait --for tui-idle` exists.
- `orca account add|select|rm` exist. The observer must never invoke them.

## 3. Architecture

```text
 owner ──(STOP / DISABLED / ATTEND commands, local files)──┐
                                                          ▼
 ┌──────────────────────── observer process (model-free) ───────────────────────┐
 │  loop every 60 s:                                                            │
 │   1 kill-switch check   2 telemetry adapters   3 Orca read adapter           │
 │   4 pool state machine  5 attempt reconciliation 6 mailbox surfacing         │
 │   7 actions (fixed-template messages, owner notifications, wake)             │
 │  journal: state.sqlite3 (WAL, fsync) — private host state                    │
 └──────────────────────────────────────────────────────────────────────────────┘
        ▲ read                       ▲ admit / refuse (same journal, same lock)
        │                            │
 telemetry files / app-server   `ohv-admit` front door ◄── coordinator (Claude) runs it
 Orca CLI (read verbs)                │                     instead of bare worker-start
                                      ▼
                         orca orchestration worker-start (exact allowlisted argv)
```

### 3.1 Components

1. **Observer process.** One user-level process. Decided: Python 3.12 standard library only, no third-party packages, no network listener. It runs as the owner's user and is started by hand for the pilot (OD7).
2. **Admission front door `ohv-admit`.** A command in the same package that shares the journal and the lock. The coordinator calls it instead of calling `orca orchestration worker-start` directly. It runs in the coordinator's terminal, so Orca sees the coordinator's own caller identity. This avoids the unverified question of whether a host process can act for a coordinator (U4, U7). Subcommands (decided): `ohv-admit start`, `ohv-admit resume`, `ohv-admit status`, `ohv-admit attend`, `ohv-admit release`.
3. **Telemetry adapters** (§5). Read-only. Each returns a typed reading or an explicit absence.
4. **Orca read adapter.** Uses only documented CLI read verbs: `run-show`, `task-list`, `dispatch-show`, `worker-list` (all pages), `worker-show`, `inbox`, `check --peek` or `check --all` (§8, U10), `request-show`, `terminal show`, `terminal wait --for tui-idle`. It never opens Orca's private SQLite database for writing, and the implementation must not depend on its private tables.
5. **Action adapter.** Holds the only outbound actions, a closed allowlist:
   - `orca orchestration send` with a fixed template (§7.2, §8) to an exact Task and Dispatch;
   - the coordinator wake (§8.3);
   - a local owner notification (`osascript -e 'display notification …'`) plus an append to the private `owner-alerts.log`;
   - from `ohv-admit` only: `orca orchestration worker-start` with validated argv.

   Nothing else. In particular there is no `reply`, `ask`, `gate-resolve`, `task-update`, `worker-stop`, `worker-abandon`, `worker-release`, `reset`, `run-use`, `account …`, `automations …`, `git push`, merge, or keystroke into a prompt.

### 3.2 State location (C5 / D6 split)

| Where | What | Who writes |
|---|---|---|
| Repo, run branch, `docs/agent-stack/runs/<run-id>/` | Sanitized queue, locks, approvals, capacity-state summary (mode per pool, source class, UTC time; no account identifiers), owner-return report | Coordinator only, under its package authority. **The observer never writes to the repository** |
| Repo, worker branch, `docs/agent-stack/runs/<run-id>/<worker>/checkpoint.md` | Worker checkpoint: input/working SHA, dirty paths, completed sections, tests, next step, Task/Dispatch IDs | The worker, when its package authorizes a commit |
| Private host state, `~/Library/Application Support/Ohvernight/autonomy/` (mode `0700`, files `0600`) | `policy.json` (versioned, hashed); `state.sqlite3` (journal); `telemetry/<pool>.json` (selected fields only); `controller.lock`; `DISABLED`; `STOP`; `ATTENDED_UNTIL`; `owner-alerts.log` | Observer and `ohv-admit` only |

The private state holds the lease, heartbeat, quota readings, Orca session, terminal and request IDs, and any account-scoped value. None of it is committed, quoted in PR text or posted.

### 3.3 Model-free invariant

The observer and `ohv-admit` must not start an agent for their own purposes, call a model API, send a prompt to a model, or create an Orca automation (an automation runs an agent). Their effects on model usage are limited to:

- **Admitting a queued start or resume.** That work then consumes its pool, and it is accounted for (§4.4).
- **Sending a fixed-template message to a running worker.** A worker reading that message spends tokens inside a section that has already been admitted and reserved.
- **The coordinator wake (§8.3).** It is allowed only while the Claude pool admits coordinator work. Otherwise the owner is notified instead.

No probe call, measurement call or "are you there" prompt is ever made.

## 4. Usage policy

### 4.1 Pools and windows

A **pool** is one provider account allowance. A **window** is one metered interval of that pool (Codex primary 300 min and secondary 10 080 min; Claude `five_hour` and `seven_day`). Worktrees, terminals, Runs, model names and worker names never create a pool. Configured pools (decided, in `policy.json`):

| Pool | Consumers | Windows | Reserve (A1) |
|---|---|---|---|
| `claude` | Coordinator session, every `--agent claude` worker, any interactive Claude Code use on the same account | 5h, 7d | max(15%, one material review + owner-return margin) |
| `codex` | Every `--agent codex` worker, interactive Codex use; Hermes counts as a consumer until its independence is verified (A2) | 300 min, 10 080 min | max(25%, next-day build + verification + handoff) |

Membership is configuration and is never inferred. An unknown consumer is assumed to share the pool. Hermes is unavailable (K4) and is not admitted by this controller.

### 4.2 Ceiling and thresholds

For each window: `ceiling = min(90, 100 − reserve)`. Equality blocks. Owner mode thresholds (A2), clamped so that none exceeds the ceiling:

| Threshold | Value | Claude (reserve 15%) | Codex (reserve 25%) |
|---|---|---|---|
| `conserve_at` | 75 | 75 | collapses into ceiling (75) |
| `closing_at` | 85 | collapses into ceiling (85) | collapses (75) |
| `ceiling` | `min(90, 100 − reserve)` | 85 | 75 |

Decided: `conserve_at` takes the lower bound of the owner's 75–80% range, because the lower bound is the conservative choice. A threshold at or above the ceiling collapses: with current reserves, Codex goes straight from ACTIVE to SUSPENDED at 75%, and Claude goes from CONSERVE to SUSPENDED at 85%. CLOSING becomes reachable only if the owner lowers a reserve (D5 (c)). This document does not change any reserve.

### 4.3 Mode per pool

The pool's mode is computed from the **most conservative accepted reading** of each window, and the most restrictive window decides. A five-hour reset never clears a weekly SUSPENDED.

| Mode | Observed share consumed (worst window) | Admission |
|---|---|---|
| `QUOTA_UNKNOWN` | No fresh accepted reading for some applicable window | Supervised only, under the unknown-quota caps (§4.5); unattended: nothing |
| `ACTIVE` | below `conserve_at` | New sections, if the projection rule (§4.4) passes |
| `CONSERVE` | `conserve_at` ≤ u < `closing_at` | No new discretionary section. Running sections may finish if projected to fit under the ceiling; implementation-ready work is queued for after the reset. Claude pivot applies when Codex is here or worse |
| `CLOSING` | `closing_at` ≤ u < ceiling | Nothing new. A checkpoint request goes to each running section at its next safe boundary |
| `SUSPENDED` | u ≥ ceiling, or any rejection or limit event | No dispatch. Immediate checkpoint requests; tasks become `WAITING_FOR_CAPACITY` |
| `AWAITING_RESET_EVIDENCE` | Every constraining `resets_at` has passed, but no post-reset reading exists | No dispatch, except the single reset probe (§7.4) |
| `RESET_PROBE` | One admitted post-reset section is running so that a fresh reading can appear | Nothing else admitted |
| `READY_TO_RESUME` | A post-reset reading confirms a successor window below `conserve_at` in every window | Waiting tasks resume first, each exactly once (§7.5); then `ACTIVE` |

The owner's percentage is a **planning observation** (A2). It may move a pool to a more conservative mode at any time. It may move a pool to a less conservative mode only in a supervised session, only for that session, and the journal records it as an owner observation. It never confirms a reset for unattended use and is never reported as telemetry.

### 4.4 Admission rule and in-flight accounting

`ohv-admit start` admits a section for pool `p` only if **all** of the following hold:

1. The controller is `OBSERVING` (not starting, reconciling, degraded or disabled), and the `STOP` and `DISABLED` sentinels are absent.
2. The mode is `ACTIVE` (or `READY_TO_RESUME` for a resume, or `RESET_PROBE` for the probe slot), or `QUOTA_UNKNOWN` in a supervised session within the unknown caps.
3. The concurrency cap is not reached (§4.5). Count every **non-terminal attempt** of the pool, including attempts the journal never admitted that are discovered in `worker-list` (`UNADMITTED`, §6.3 L23), plus the coordinator for `claude`.
4. For every applicable window `w`:

```text
used_w            = most conservative accepted reading for w        (unknown ⇒ rule 4 fails unless rule 2's unknown cap applies)
inflight_w        = Σ reservation_w over every non-terminal attempt of p
                    (full reservation kept until the attempt is terminal — double counting is deliberate)
section_w         = policy.section_reservation[p][w]   (per section; per-task override may only be larger)
checkpoint_w      = policy.checkpoint_reservation[p][w]
admit iff used_w + inflight_w + section_w + checkpoint_w < ceiling_w      (strict)
```

5. The task is in the coordinator queue, recorded through `ohv-admit` with its package ID, the exact argv and its pool. The observer never adds work.
6. The argv passes validation (§10.2).

A refusal returns a machine-readable reason code and a one-line human message, and leaves no side effect except a journal row. Reason codes (decided): `CONTROLLER_NOT_OBSERVING`, `DISABLED`, `STOPPED`, `MODE_<mode>`, `CAP_UNKNOWN_QUOTA`, `CAP_POOL`, `PROJECTED_OVER_CEILING:<window>`, `READING_STALE:<window>`, `UNATTENDED_NOT_ACTIVATED`, `ARGV_REJECTED`, `DUPLICATE_ATTEMPT`, `UNRESOLVED_ATTEMPT`, `COORDINATOR_ABSENT`.

Planning defaults for reservations, all owner decision OD4. They are written down as defaults, not provider facts. Units are percentage points of the window:

| Pool / window | Section | Checkpoint | Basis |
|---|---|---|---|
| codex 300 min | 10 | 5 | A6: one in-flight worker went from 88% to 92% within about 3 min of the SUSPENDED message |
| codex 10 080 min | 2 | 1 | Weekly moved 14% → 15% across a reset (A6) |
| claude 5h | 20 | 5 | A6 ESTIMATE: burn about $13/h against a calibrated ~$43 block |
| claude 7d | — | — | No source; the window stays unknown, so Claude stays `QUOTA_UNKNOWN` for any unattended purpose |

The pilot replaces these defaults with observed per-section deltas, recorded with their source (§11.3, PS7).

### 4.5 Concurrency caps

| Condition | Claude workers (beside the coordinator) | Codex workers |
|---|---|---|
| `QUOTA_UNKNOWN`, supervised (incident rule C1) | 1 | 2 |
| Pool known, until the pilot calibrates reservations | 1 | 2 |
| Unattended, before D7 (v) | 0 new | 0 new |

Rule C2 also holds: the next Claude worker is admitted only after the previous Claude worker has reported `worker_done` and been released (`ohv-admit release`, or a `worker-list` observation of `released`).

**Owner exceptions.** The owner may raise a cap for a supervised session with `ohv-admit attend --cap claude=3 --until <UTC>`, run by the owner in a terminal. The journal records the exception with its time, scope and expiry. Decided: expiry defaults to the end of the current five-hour window. An exception never overrides a mode. A CONSERVE or worse reading from any accepted source, including an ESTIMATE, still refuses new work (scenario 1b).

### 4.6 Never bypass

`ohv-admit` derives the pool from `--agent`. It refuses a start whose stated purpose is to move work to another pool because the first one is suspended, unless routing in `capacity-routing.md` already allows that route (the Claude pivot covers Claude's own role, not Codex implementation). It never runs `orca account add|select|rm`. It does not change `--model` to escape a limit; a model change within a pool is ordinary routing and changes no accounting. When a reading carries an account identity (Codex `accountId`) and that identity changes between readings, the pool drops to `QUOTA_UNKNOWN` and the owner is notified. The account identifier is never written outside private state.

### 4.7 No fabricated percentages

Every percentage the observer stores or shows carries a **source class**: `VERIFIED`, `VERIFIED_IN_RUN`, `ESTIMATE`, `OWNER_OBSERVATION` or `REJECTION_EVENT` (§5). `ohv-admit status` prints the class next to each number. A window without a reading prints `unknown`. Nothing is interpolated, extrapolated from a clock, or derived from token counts and then presented as a provider percentage.

## 5. Telemetry

### 5.1 Sources

Each source is an UNKNOWN to settle in the pilot, unless noted as verified in run `run_16f69595c542`.

| ID | Pool | Source | Class | Status | Allowed use |
|---|---|---|---|---|---|
| T1 | codex | Newest `rate_limits` record in `~/.codex/sessions/**/*.jsonl` (`primary` = 300 min, `secondary` = 10 080 min; `used_percent`, `resets_at`). Selected fields only, read line by line; all other content is discarded unread | `VERIFIED_IN_RUN` | Read successfully 2026-10-20 (A6, A7). It is an internal cache, not a public contract (A4 E10). Format drift is U12 | Any downward move; reset confirmation in a supervised session; unattended authority only if the owner accepts it (OD2) |
| T2 | codex | `codex app-server`, stdio JSON-RPC `initialize` → `account/rateLimits/read`, no thread or turn created, process closed after the read | `VERIFIED` once U5 passes | Not exercised (U5); requires separate owner authorization (D7 iii) | Preferred unattended authority. Needs no model call and is fresh while idle, if U5 confirms that |
| T3 | claude | Status-line selected-field bridge: the status-line command appends `rate_limits.five_hour` / `seven_day` (`used_percentage`, `resets_at`) and the receipt time to `telemetry/claude.json` | `VERIFIED` once U6 passes | Not configured. Configuring it is a settings change that needs owner approval at pilot time (D7 iii, OD3). It is event-fed: a reading exists only after a model response | Supervised and unattended authority once U6 passes. Never proof of a reset by itself (windows are dropped after reset) |
| T4 | claude | `quotaLimits` record in `~/.claude/projects/*/*.jsonl` (`type`, `resetsAt`), written only when a request is rejected at a limit. Selected fields only | `REJECTION_EVENT` | Format observed 2026-10-20 (A6) | Always: moves the pool to `SUSPENDED` until `resetsAt` |
| T5 | claude | `npx --no-install ccusage@20.0.30 claude blocks --offline` cost per five-hour block, divided by the calibrated block cap | `ESTIMATE` | Calibrated once: ~$43.15 cap from the block rejected on 2026-10-19/20; owner Orca reading 46% against the ESTIMATE's 44% at 15:30Z (A6) | Only toward a more conservative mode. Never unlocks admission, never confirms a reset. Always labelled `ESTIMATE`. Re-calibrated by the coordinator on each T4 event. The observer runs it only when the package is already cached (`--no-install`), so it never downloads |
| T6 | any | Owner statement, recorded by `ohv-admit attend --observed claude=46` | `OWNER_OBSERVATION` | Available | §4.3 rules |
| T7 | any | Provider limit error surfaced in a worker's `worker_done` or escalation (`rate_limit`, usage limit reached) | `REJECTION_EVENT` | Available through the mailbox | Pool goes to `SUSPENDED` immediately, whatever any snapshot says |

Excluded (A4, A7): rendered `/usage` or `/status` screens, terminal titles, Orca's private database, OAuth or web usage endpoints, browser cookies, `~/.claude/.credentials.json` and any credential file. The observer **must not open** the credential file. A unit test asserts that the adapter's path allowlist excludes it (test X5).

### 5.2 Freshness

Decided defaults, in `policy.json`:

- **Fresh.** `observed_at` is no more than 10 min old **and** precedes no admitted activity of that pool. A reading taken before an attempt was admitted remains usable only together with that attempt's full reservation (§4.4).
- **Pre-reset.** `now ≥ resets_at`. The reading describes a finished window. It is never evidence for the successor window.
- **Stale.** Older than 10 min while any attempt of the pool is non-terminal, or older than 60 min otherwise, or pre-reset. A stale reading may still hold the pool at a conservative mode. It never admits anything.
- **Absent, malformed, or with a mismatched window or account.** The window is unknown.
- **Codex T1 caveat (A7).** T1 is written only when Codex runs. A reading therefore stays stale until the next Codex activity. A reset is confirmed only by a fresh reading taken **after** the first post-reset call (§7.4).
- **Clock discontinuity.** If wall-clock time and monotonic time disagree by more than 2 poll intervals (sleep, wake, manual clock change), every reading becomes stale and the controller goes to `RECONCILING`.

### 5.3 Conflicts

When sources disagree, the most conservative accepted value per window wins. On 2026-10-20 the ESTIMATE (44%) conflicted with an owner observation (~6%, probably weekly), and the estimate governed (scenario 6). A `REJECTION_EVENT` beats every snapshot.

## 6. State machines

Four machines. State and transition IDs are stable; each test in §11 names the IDs it covers.

### 6.1 Controller (process) — 6 states, 11 transitions

States: `OFF`, `STARTING`, `RECONCILING`, `OBSERVING`, `DEGRADED`, `DISABLED`.

| ID | From → To | Trigger and guard | Effect |
|---|---|---|---|
| C1 | OFF → STARTING | Manual start (pilot) or approved launch service (OD7) | Load `policy.json`; verify its hash and schema version |
| C2 | STARTING → RECONCILING | `controller.lock` acquired (`fcntl` exclusive); journal opens and passes integrity check | New controller epoch written |
| C3 | STARTING → OFF | Lock held by a live process, or policy or journal invalid | Exit non-zero; owner notification. Never two controllers |
| C4 | RECONCILING → OBSERVING | Orca reachable; every non-terminal attempt matched to Orca state (§7.6); one telemetry pass done | Admission opens, subject to §4.4 |
| C5 | RECONCILING → DEGRADED | Orca unreachable; Run fenced or rebound; ambiguous attempt that cannot be reconciled; journal schema mismatch | Admission refused; owner notification |
| C6 | OBSERVING → RECONCILING | Clock discontinuity; Orca runtime ID changed; coordinator handle changed in `run-show` | Readings marked stale; admission closed until C4 |
| C7 | OBSERVING → DEGRADED | Orca unreachable for 3 consecutive polls; journal write or fsync failure; disk full | As C5 |
| C8 | DEGRADED → RECONCILING | The degrading condition is gone on 2 consecutive polls | — |
| C9 | any → DISABLED | `DISABLED` sentinel present (checked at loop start and immediately before each mutation) | Every outbound action stops, except the local owner notification and journal writes. `ohv-admit` refuses everything |
| C10 | DISABLED → OFF | Process exit (signal, or owner stop) | Journal flushed. Removing the sentinel does **not** resume; only C1 does |
| C11 | any → OFF | `STOP` sentinel or SIGTERM | Flush; release lock; no further action. Running workers are untouched |

### 6.2 Pool — 8 states, 16 transitions

States: `QUOTA_UNKNOWN` (initial), `ACTIVE`, `CONSERVE`, `CLOSING`, `SUSPENDED`, `AWAITING_RESET_EVIDENCE`, `RESET_PROBE`, `READY_TO_RESUME`.

| ID | From → To | Trigger and guard |
|---|---|---|
| P1 | QUOTA_UNKNOWN → ACTIVE | Fresh accepted reading for **every** applicable window; worst window below `conserve_at` |
| P2 | QUOTA_UNKNOWN → CONSERVE / CLOSING / SUSPENDED | Fresh accepted reading; worst window in that band (an ESTIMATE or owner observation may do this alone) |
| P3 | ACTIVE → CONSERVE | Worst window reaches `conserve_at` |
| P4 | CONSERVE → CLOSING | Worst window reaches `closing_at` (only when below the ceiling, so not reachable under current reserves) |
| P5 | ACTIVE / CONSERVE / CLOSING → SUSPENDED | Worst window reaches the ceiling |
| P6 | ACTIVE / CONSERVE / CLOSING → QUOTA_UNKNOWN | Some applicable window becomes stale, absent, malformed or account-mismatched |
| P7 | SUSPENDED → AWAITING_RESET_EVIDENCE | Wall clock passes `resets_at` of **every** constraining window. A missing `resets_at` never fires this; the pool stays SUSPENDED and the owner is notified |
| P8 | AWAITING_RESET_EVIDENCE → READY_TO_RESUME | Fresh reading with `observed_at > resets_at_old`, a later `resets_at` (successor window), and every window below `conserve_at` |
| P9 | AWAITING_RESET_EVIDENCE → RESET_PROBE | The source is activity-fed (T1, T3), no fresh reading exists, the session is supervised (unattended: only after D7 (v) and OD2), and the queue holds an admissible waiting task |
| P10 | RESET_PROBE → READY_TO_RESUME | The probe section produced a fresh reading that satisfies the P8 guard |
| P11 | RESET_PROBE → SUSPENDED | The fresh reading still constrains, or a rejection event occurs |
| P12 | AWAITING_RESET_EVIDENCE → SUSPENDED | A fresh reading shows the window has not reset, or another window (for example weekly) still constrains |
| P13 | READY_TO_RESUME → ACTIVE | Every `WAITING_FOR_CAPACITY` task of the pool has been resumed once, refused, or handed back to the coordinator; mode recomputed |
| P14 | CONSERVE / CLOSING → lower band | A fresh `VERIFIED` or `VERIFIED_IN_RUN` reading shows the worst window lower. Estimates and owner observations cannot do this unattended |
| P15 | any except SUSPENDED → SUSPENDED | Rejection event (T4, T7), whatever the snapshots say |
| P16 | any → mode of the owner's band | Owner observation at or above a threshold that is stricter than the current mode |

### 6.3 Attempt (one Orca Dispatch of one Task section) — 12 states, 23 transitions

States: `QUEUED`, `INTENT_RECORDED`, `DISPATCHED`, `RUNNING`, `CHECKPOINT_REQUESTED`, `WAITING_FOR_CAPACITY`, `DONE`, `SETTLED`, `FAILED`, `OUTCOME_UNKNOWN`, `BLOCKED_PROMPT`, `UNVERIFIABLE`.

Terminal for reservation purposes: `WAITING_FOR_CAPACITY`, `DONE`, `SETTLED`, `FAILED`. `BLOCKED_PROMPT` frees its reservation but keeps its concurrency slot. Every other state holds both.

Idempotency key (decided): `(run_id, task_id, section_id, attempt_seq)`. One logical section has at most one non-terminal attempt at a time, enforced by a unique partial index in the journal.

| ID | From → To | Trigger and guard | Effect |
|---|---|---|---|
| L1 | QUEUED → INTENT_RECORDED | §4.4 admits | Write intent (UUID, exact argv, reservation, policy hash) and fsync **before** any Orca call |
| L2 | QUEUED → QUEUED | §4.4 refuses | Journal row with the reason code; no Orca call |
| L3 | INTENT_RECORDED → DISPATCHED | `worker-start` exits 0 (`ready`) | Record request ID, Task ID, Dispatch ID, terminal handle |
| L4 | INTENT_RECORDED → OUTCOME_UNKNOWN | `outcome_unknown`; lost response; `ohv-admit` crashed before writing the receipt | Reservation kept; reconcile (L16/L17); never replay blind |
| L5 | INTENT_RECORDED → FAILED | Exit 1 with a proven `failedStage` and no residual effects | Reservation freed |
| L6 | INTENT_RECORDED → BLOCKED_PROMPT | `failedStage: agent_readiness` with a prompt blocker (for example `agent-update-prompt`) | §9 |
| L7 | DISPATCHED → RUNNING | First heartbeat for the exact Task and Dispatch, or `worker-show` reports the agent live | — |
| L8 | RUNNING → CHECKPOINT_REQUESTED | Pool enters CLOSING or SUSPENDED, or the projection of this attempt crosses the ceiling | Send the fixed-template checkpoint request (§7.2) once; start the grace timer |
| L9 | CHECKPOINT_REQUESTED → WAITING_FOR_CAPACITY | `worker_done --outcome failed` for the exact IDs whose body starts `INCOMPLETE - resume at`, with a checkpoint commit SHA | Reservation freed; resume record created |
| L10 | CHECKPOINT_REQUESTED → DONE | The worker finished the section anyway (`worker_done --outcome succeeded`, exact IDs) | Reservation freed |
| L11 | RUNNING → DONE | `worker_done --outcome succeeded`, exact Task and Dispatch | Reservation freed; the mailbox item goes to the coordinator (§8) |
| L12 | DONE → SETTLED | `worker-list` shows the terminal `released`, or `ohv-admit release` | Concurrency slot freed (rule C2) |
| L13 | DISPATCHED / RUNNING / CHECKPOINT_REQUESTED → UNVERIFIABLE | No heartbeat for 3 intervals (15 min); Orca reports `restored_unconfirmed`; clock discontinuity; Orca restarted | Keep reservation and slot; no replacement writer; owner notification if this lasts more than 30 min |
| L14 | UNVERIFIABLE → RUNNING | Positive liveness for the **same** Dispatch | — |
| L15 | UNVERIFIABLE → FAILED | Positive exit evidence: `worker-show` shows stopped or failed, or the terminal has exited | Reservation freed; the coordinator decides on any retry |
| L16 | OUTCOME_UNKNOWN → DISPATCHED | `request-show` reports `completed`; receipt replayed | Record receipt |
| L17 | OUTCOME_UNKNOWN → FAILED | `request-show` reports `absent` **and** `task-list` / `dispatch-show` / `worker-list` show no attempt for the Task created after the intent time | Reservation freed. If either check is ambiguous, stay in OUTCOME_UNKNOWN and notify the owner |
| L18 | WAITING_FOR_CAPACITY → INTENT_RECORDED | `ohv-admit resume`: pool `READY_TO_RESUME` or `ACTIVE`; §4.4 admits; this resume record not yet consumed | New attempt with `attempt_seq + 1`; argv carries the same `--task` and `--retry-of <previous dispatch>`; the resume record is consumed in the same transaction |
| L19 | FAILED → INTENT_RECORDED | Coordinator-requested retry via `ohv-admit start --retry-of`; Orca's three-failure circuit breaker not tripped; at most one automatic resume per task per window | As L18 |
| L20 | BLOCKED_PROMPT → RUNNING | The owner resolved the prompt by hand; positive liveness | — |
| L21 | BLOCKED_PROMPT → FAILED | Coordinator or owner settles the attempt as failed | Slot freed |
| L22 | RUNNING → FAILED | `worker_done --outcome failed` without a checkpoint marker, or a T7 limit error with positive exit | Reservation freed; T7 also fires P15 |
| L23 | (none) → RUNNING, flagged `UNADMITTED` | `worker-list` shows a live worker of the Run that has no journal intent | Adopted with a full section reservation; counted against caps; the owner is notified once per Dispatch. This is how a bypass of the front door shows up |

Not transitions, and each tested: `worker_done` carrying a stale Dispatch ID (a straggler from an earlier retry) changes nothing. A `heartbeat` is never completion. An empty `check` result is never completion.

### 6.4 Mailbox item — 4 states, 7 transitions

States: `NEW`, `SURFACED`, `ESCALATED`, `RESOLVED`. Items are messages addressed to the coordinator whose type is `question`, `escalation`, `worker_done` or `decision_gate` (and any type that `check` reports as blocking, if a later Orca version adds one).

"Resolved" depends on the type: for a `question`, a `reply` whose parent is that message ID exists; for an `escalation`, a reply exists or the coordinator acknowledged the Delivery; for a `worker_done`, the Delivery holding it has been acknowledged.

| ID | From → To | Trigger and guard |
|---|---|---|
| M1 | (none) → NEW | A poll sees an unresolved item that the journal does not yet know (keyed by message ID) |
| M2 | NEW → SURFACED | Wake sent (§8.3): the Claude pool admits coordinator work, the coordinator terminal is idle at its input, and no prompt signature matches |
| M3 | NEW → ESCALATED | Wake not possible: Claude SUSPENDED or AWAITING_RESET_EVIDENCE; coordinator absent; terminal not idle for 10 min; prompt detected; or controller DISABLED (owner notification only) |
| M4 | SURFACED → RESOLVED | Type-specific resolution observed |
| M5 | SURFACED → ESCALATED | Not resolved 15 min after the wake |
| M6 | ESCALATED → RESOLVED | Type-specific resolution observed |
| M7 | ESCALATED → ESCALATED | Re-notification of a still-open `question` or `escalation` at 60 min, then once in the daily report. No further repeats (owner communication policy: exceptions, not routine messages) |

**An ask timeout is not an answer.** When a worker's `ask` times out, the question stays pending in Orca ("Timeout leaves the question pending", A8). The item stays NEW, SURFACED or ESCALATED. No state of any machine treats a timeout, a silence or an elapsed deadline as a reply or an approval (tests B20, S2.4).

**Totals: 30 states, 57 transitions** (C 11, P 16, L 23, M 7).

## 7. Lifecycle

### 7.1 Checkpoint contents

When an attempt goes to `WAITING_FOR_CAPACITY`, two records exist:

- **Repo (worker writes, sanitized):** `docs/agent-stack/runs/<run-id>/<worker>/checkpoint.md` on the worker's branch, committed when the package allows a commit. It contains: UTC time; input SHA and head SHA; dirty paths; completed sections and their artifacts; the exact tests run and their results; unresolved evidence; the next section; resume instructions; Task and Dispatch IDs. No usage numbers, account data or transcript text.
- **Private journal (observer writes):** attempt row (IDs, request ID, argv hash, reservation, policy hash), the pool readings that caused the suspension (source class, values, `observed_at`, `resets_at`), the resume record (`task_id`, `retry_of`, worktree selector, `consumed=false`), and the checkpoint commit SHA reported in `worker_done`.

### 7.2 Suspend without model calls

On L8 the observer sends exactly one message per attempt, from a fixed template with no generated text:

```text
orca orchestration send --to dispatch:<dispatch_id> --type checkpoint_request \
  --subject "CAPACITY <MODE>: checkpoint at next safe boundary" \
  --body "Pool <pool> is <MODE> (<source class>, observed <UTC>). Finish the current step, commit your checkpoint, then send worker_done --outcome failed with body 'INCOMPLETE - resume at <next step>'. Do not start a new section." \
  --task-id <task_id> --dispatch-id <dispatch_id>
```

(`--type checkpoint_request` assumes Orca accepts custom message types. If it does not, the type falls back to `escalation` with the same subject; settled in pilot step PS0.) The observer then waits. Grace (decided): 20 min in CLOSING, 10 min in SUSPENDED. After the grace period it notifies the owner (`CHECKPOINT_OVERDUE`) and keeps waiting. **It never stops, kills or abandons a worker** (OD8). When the provider itself cuts the worker off at the limit, the result is L13 or L22.

Throughout the suspension the observer makes no model call. It keeps polling telemetry and the mailbox without a model: file reads, Orca read verbs and, if U5 passes and OD2 allows it, the T2 app-server read.

### 7.3 Observing the reset

A timer only ever schedules a **read**; it never authorizes a dispatch. At each constraining `resets_at` the observer re-reads telemetry (P7). A reset is confirmed only by the P8 or P10 guard: a reading received after the old reset time, naming a later reset boundary, and below `conserve_at` in every window. A clock passing `resets_at`, an absent Claude window (dropped after reset), a sparse or null notification and zero token activity are each **not** confirmation. A five-hour reset while the weekly window still constrains keeps the pool SUSPENDED (P12).

### 7.4 The reset probe

T1 and T3 only produce readings when the provider is used. The first post-reset section is therefore the probe: real queued work, never a measurement call. Exactly one section is admitted, with concurrency 1 and the full reservation. Nothing else is admitted until its fresh reading arrives (P10 or P11). This is what the coordinator did by hand at 18:30–18:32Z on 2026-10-20 (scenario 4). The probe is allowed in a supervised session; unattended use requires D7 (v) and OD2. When T2 is available (U5), the probe is unnecessary for Codex, because T2 reads without a model call.

For Claude, the probe is the coordinator's own first turn after the reset in a supervised session. The observer never opens a Claude turn for this purpose.

### 7.5 Resume exactly once

1. The pool reaches `READY_TO_RESUME`. The observer orders the `WAITING_FOR_CAPACITY` resume records by the coordinator's queue priority.
2. Supervised (v1): the observer wakes the coordinator with the fixed wake text (§8.3) naming the ready pool. The coordinator runs `ohv-admit resume --task <task_id>`. Unattended (only after D7 (v)): see OD2. Without activation, the observer never issues the start itself.
3. `ohv-admit resume`, in one journal transaction under the lock: checks that the resume record is unconsumed; enumerates `task-list`, `dispatch-show` and `worker-list` (all pages) for the Task; refuses with `UNRESOLVED_ATTEMPT` if any attempt of the Task is non-terminal or unverifiable; checks §4.4; records the intent and marks the record consumed (L18); then runs `orca orchestration worker-start --task <task_id> --retry-of <previous_dispatch> <same placement and agent flags>`.
4. If the response is lost: the attempt goes to `OUTCOME_UNKNOWN`, `request-show` runs against the recorded request ID, and the attempt is never re-run blind. Whether a request ID can be chosen in advance by the caller is U7. Until U7 passes, a crash before the request ID is known leaves the attempt OUTCOME_UNKNOWN, and the owner is notified.
5. A second `ohv-admit resume` for the same record returns `DUPLICATE_ATTEMPT` and makes no Orca call (test L18b).

The resumed worker reads its checkpoint and continues from the next step. A section marked complete in its checkpoint is never re-run unless the coordinator logs a new task (A3 06).

### 7.6 Reconciliation (C2 → C4), orphans

On every entry to `RECONCILING`:

1. Check the sentinels. Verify the Run ID and coordinator handle against the journal (`run-show`).
2. Enumerate the Run's Tasks, Dispatches and workers (all pages, `--include-remote`).
3. For each journal attempt that is not terminal, match it to Orca by Dispatch ID:

| Orca evidence | Journal result |
|---|---|
| Live, same Dispatch | RUNNING (L14) |
| Settled succeeded | DONE (L11) |
| Settled failed or stopped | FAILED (L15) |
| `restored_unconfirmed`, missing, PTY live with agent unproven | UNVERIFIABLE (L13); reservation kept; no new writer on that surface |
| Request ID known, receipt pending or absent | OUTCOME_UNKNOWN, then L16 or L17 |

4. A worker in Orca with no journal intent is adopted under L23.
5. Then telemetry is re-read. Readings taken before the reconciliation count as stale.

**Orphan cases:**

- **Coordinator absent.** The coordinator terminal is gone, `run-show` names a different handle, or the Run is fenced (`consumer_fenced`, K5). The run is flagged `COORDINATOR_ABSENT`. Every admission is refused, because only the coordinator dispatches and the observer has no coordinator authority. Workers keep running inside their packages. Mailbox items go to the owner (M3). The observer never runs `run-use`, `--takeover-legacy` or `--from <coordinator>` to repair this (U4).
- **Orphaned worker.** A live worker whose Task is settled, or whose Dispatch is not current. It becomes UNVERIFIABLE, with the reservation kept and the owner notified. No `worker-stop` is issued.
- **Orphaned Run.** Orca restarted and the Run's records are unreadable or changed. The controller goes to `DEGRADED`, and nothing is admitted until an owner-attended reconciliation (U1).

### 7.7 Orca restart, host sleep, reboot

| Event | Detection | Behaviour |
|---|---|---|
| Observer restart | C1 | Lock, journal reload, RECONCILING; no admission until C4 |
| Orca app restart | Orca unreachable, then the runtime ID changes | DEGRADED (C7), then RECONCILING (C8, C6); attempts UNVERIFIABLE until liveness is proven (U1) |
| Host sleep and wake | Clock discontinuity | C6; all readings stale; heartbeats missing during sleep are not treated as worker death (L13, never L15) (U2) |
| Reboot | Manual start, or the approved launch service at login (OD7) | As observer restart. Processes are presumed gone, but that is recorded only from positive evidence (U3) |
| Network loss | Orca or provider unreachable | Same as Orca unreachable; T7 events are not inferred |

The observer never prevents sleep, never changes power, firewall or login settings and never wakes the machine (A3 05).

## 8. Mailbox surfacing and coordinator wake (incident 2)

### 8.1 Polling, without consuming

Every 60 s (decided) the observer reads the coordinator's mailbox through a **non-consuming** view. In preference order: `orca orchestration inbox --terminal <coordinator> --full --json`; then `orca orchestration check --terminal <coordinator> --run <run> --all --json`. It must never use plain `check` (which hands out the FIFO batch and changes what the coordinator receives) and never `--ack`. Whether these views work from a process that is not an Orca terminal, and whether they reveal Delivery acknowledgement and reply linkage, is U10. Until U10 passes, the pilot runs the observer from its own Orca terminal in the Run's home worktree, and that terminal never sends as the coordinator.

### 8.2 Latency bound

Decided: every unresolved `question`, `escalation`, `worker_done` and `decision_gate` is in NEW within one poll interval (≤ 60 s after Orca stores it) and is SURFACED or ESCALATED within **two poll intervals (≤ 120 s)**. If a poll fails, the bound restarts from the next successful poll. Three failed polls are C7 (DEGRADED), which itself notifies the owner, so silence cannot last longer than about 3 min plus one interval without an owner notification.

### 8.3 Coordinator wake

The wake is one fixed line sent to the coordinator terminal with `orca terminal send`, only when **all** of the following hold:

- the Claude pool admits coordinator work: mode ACTIVE or CONSERVE, or QUOTA_UNKNOWN in a supervised session;
- `orca terminal wait --terminal <coordinator> --for tui-idle --timeout-ms 5000` reports idle;
- a `terminal read` of the visible tail matches **no** prompt signature (§9);
- no wake was sent in the previous 5 min.

Wake text (fixed): `OBSERVER: <n> unresolved orchestration item(s) (<types>). Run: orca orchestration check`. It carries no other content, so a worker's message text never reaches the coordinator's input through the observer.

Whether `tui-idle` reliably separates "at the input box" from "showing a permission or update prompt" is U11. If U11 fails, the wake is withdrawn and M2 is replaced by M3: owner notification only.

### 8.4 Owner notification

A local macOS notification plus an append to `owner-alerts.log`, both model-free. They contain the item type, the worker's display name, the Task ID and the age, never the message body. External channels (Hermes, Telegram, Slack) are not used (OD5).

## 9. Startup and permission prompts

**Detection.** Any of:

- `worker-start` returns `failedStage: agent_readiness` with a blocker naming a prompt (observed 2026-10-19: `Agent startup blocked: agent-update-prompt`, Dispatch `ctx_40ac84f09719`);
- `worker-show` attention or next-action fields report one;
- the read-only `terminal read` tail of a worker or the coordinator matches a fixed signature list in `policy.json`: update available or install, "trust this folder", tool or permission approval, login or credentials. The list is decided at implementation and reviewed.

**Response.**

- The attempt goes to BLOCKED_PROMPT (L6), or the prompt condition is recorded on a running attempt.
- **Nothing is ever answered.** The observer sends no keystroke, no Enter, no `y` and no option to any prompt. It accepts no update, changes no setting and does not retry: a retry hits the same prompt and counts toward Orca's circuit breaker.
- The owner is notified immediately: prompt kind, terminal display name, Task ID.
- The concurrency slot stays held until L20 or L21.

Suppressing the Codex startup update check (D10 (c)) is a setting change and the owner's decision, outside this spec.

## 10. Security and permissions

### 10.1 Boundaries

- No new credentials, tokens, keys or accounts. The T2 read (if approved) uses Codex's existing managed sign-in through its own binary; the observer never handles the token. No credential file is opened (§5.1).
- No account changes: no `orca account …`, no login or logout, no plan change, no credit purchase, no reset redemption.
- No configuration changes by the observer. The T3 bridge and any launch service are owner-approved installation steps for the pilot, not something the observer does.
- No network listener. Outbound use is limited to the local Orca socket, plus the T2 child process if approved.
- Telemetry and Orca text is data. No string read from a file, a message or a recovery hint is executed. Orca's returned "next action" argv is never run as given; `ohv-admit` rebuilds argv from its own allowlist.
- `tools/local-ai/` is not touched (PAUSED_BY_OWNER).
- Production gates unchanged: no merge, push to main, auto-merge, PR creation or external message by the observer, ever.

### 10.2 `ohv-admit` argv allowlist

Allowed: `orca orchestration worker-start` with `--task` (required; `--spec` is refused, so the front door cannot create new Tasks), `--worktree`, `--agent` ∈ {claude, codex}, `--model`, `--effort`, `--retry-of`, `--timeout-ms`, `--run` (must equal the journal's Run), `--display-name`, `--name`, `--base-branch`, `--repo`, `--setup`, `--json`. Refused: `--on` (remote servers are out of scope for v1), `--terminal` reuse (it cannot be fenced cleanly), `--from` other than the caller itself, and any other verb.

### 10.3 Kill switch and rollback

- **Kill switch:** `touch "$HOME/Library/Application Support/Ohvernight/autonomy/DISABLED"`. Checked at loop start and immediately before every mutation (C9). It stops all admissions, messages and wakes. Owner notifications and journal writes continue.
- **Full stop:** `touch …/STOP`, or stop the process (C11).
- **Rollback to today's manual process:** the coordinator calls `orca orchestration worker-start` directly again and follows the C1–C4 incident rules by hand. Nothing in Orca, Git or any provider depends on the observer, so removing it needs no migration. The journal is kept for reconciliation.
- Neither switch stops, undoes or abandons running workers, deletes worktrees or changes settings. Re-enabling after DISABLED needs an explicit owner decision and a fresh C1.

## 11. Acceptance

### 11.1 Offline unit tests

Location (proposed for D7 (ii)): `tools/autonomy/observer/` with `tests/`. Test runner: Python 3.12 stdlib `unittest`, plus an injected clock, an injected Orca fake (recorded and synthetic JSON fixtures) and injected telemetry files. No network, no model, no real Orca, no real provider files. Fixture files are synthetic or sanitized (no account IDs). Adding the suite to CI is a separate reviewed change in D7 (ii).

**One test per transition (57).** `test_C1` … `test_C11`, `test_P1` … `test_P16`, `test_L1` … `test_L23`, `test_M1` … `test_M7`. Each test asserts:

- the guard: positive case, plus the nearest negative case;
- the resulting state;
- the journal rows written;
- the exact set of outbound actions (usually empty);
- that the fake model counter is 0.

**Boundary and invariant tests (25):**

| ID | Assertion |
|---|---|
| B1 | Equality blocks: projection exactly at the ceiling is refused, for both pools |
| B2 | 89 / 90 / 91 with a 10% reserve, and 74 / 75 / 76 with a 25% reserve, land in the right modes |
| B3 | Threshold collapse: with Codex reserve 25%, ACTIVE goes straight to SUSPENDED at 75 |
| B4 | A cost-based reserve larger than the percentage reserve lowers the ceiling |
| B5 | Five-hour reset with weekly at 92% stays SUSPENDED (P12) |
| B6 | Missing `resets_at`: P7 never fires, owner notified |
| B7 | Timer passing `resets_at` without a fresh reading: no admission |
| B8 | Pre-reset reading after `resets_at` is not evidence (P8 guard negative) |
| B9 | Claude window dropped after reset: absence ≠ reset |
| B10 | Clock jump forward and backward goes to C6, readings stale |
| B11 | In-flight double counting: two running attempts plus one new projection refused at the right point |
| B12 | `UNADMITTED` worker (L23) counted against the cap and the projection |
| B13 | Account ID change goes to QUOTA_UNKNOWN (P6) |
| B14 | Malformed and truncated JSONL line: window unknown, no crash |
| B15 | ESTIMATE can raise strictness but never lower it (P14 negative) |
| B16 | Owner observation lower than the reading: ignored unattended, recorded supervised |
| B17 | Duplicate `ohv-admit resume`: `DUPLICATE_ATTEMPT`, zero Orca calls |
| B18 | Crash injected after intent and before `worker-start`, after `worker-start` and before receipt, and after `worker_done` processing and before journal commit: replay is idempotent and never starts twice |
| B19 | Stale-Dispatch `worker_done` is ignored |
| B20 | Heartbeat and empty check are not completion |
| B21 | Lock contention: second controller exits (C3) |
| B22 | `DISABLED` set between admission check and `worker-start`: no start (C9 re-check) |
| B23 | Policy hash mismatch: C3 |
| B24 | Journal fsync failure: C7, no admission |
| B25 | Circuit breaker: after a third consecutive failure, `ohv-admit` refuses a further retry |

**Security tests (6):**

| ID | Assertion |
|---|---|
| X1 | The action adapter has exactly the allowlisted verbs; any other verb raises |
| X2 | argv validation refuses `--spec`, `--on`, `--terminal`, a foreign `--from`, and verbs other than `worker-start` |
| X3 | Orca "next action" strings and message bodies are never executed or forwarded into a terminal |
| X4 | No prompt is answered: with a prompt signature in the terminal tail, zero `terminal send` calls |
| X5 | The telemetry path allowlist excludes `~/.claude/.credentials.json` and any `*credentials*` path; opening one raises |
| X6 | No module imports a network or model client; static check over the package |

### 11.2 Scenario tests (incident replays, offline)

**Scenario 1: incident of 2026-10-20 ~01:00Z (must refuse the fourth concurrent Claude session).**

- **S1.1.** Fixture: Claude pool QUOTA_UNKNOWN (no T3, no T4, no ESTIMATE); supervised; coordinator live; no Claude workers. The coordinator requests, in order, M5 revision, M6 spec and PR #39 diagnosis. Expected: the first is admitted (2 sessions); the second is refused `CAP_UNKNOWN_QUOTA` (it would be the third); the third is refused `CAP_UNKNOWN_QUOTA` (it would be the **fourth** concurrent Claude session).
- **S1.2.** After the first `worker_done`, but before release: the next request is still refused (rule C2). After release: admitted.
- **S1.3.** Unattended (no `ATTENDED_UNTIL`, D7 (v) not activated): the first request is refused `UNATTENDED_NOT_ACTIVATED`.
- **S1.4 (1b).** Owner exception `--cap claude=3` recorded at 14:40Z with owner observation 6%, then T5 ESTIMATE 64% at 16:15Z: the exception admits up to 3 while the pool is ACTIVE. Once the ESTIMATE puts Claude in CONSERVE, any further start is refused `MODE_CONSERVE`.
- **S1.5.** A worker started by bare `worker-start`, bypassing the front door, appears in `worker-list`: it is adopted under L23, the owner is notified, and the next admission counts it.

**Scenario 2: incident of 2026-10-20 ~18:35–21:30Z (unanswered blocking messages).**

- **S2.1.** Fixture: two Codex workers each send a `question` (via `ask`) and an `escalation` to the coordinator at 18:35Z; the coordinator neither checks nor replies. Expected: all four items are NEW by the first poll, and SURFACED (wake sent) within 120 s of the injected clock.
- **S2.2.** Coordinator still silent: ESCALATED (owner notified) at wake + 15 min; one re-notification at 60 min; no further notifications. Total notifications ≤ 3 per item over 3 h.
- **S2.3.** Claude pool SUSPENDED at 18:35Z: no wake; owner notified within 120 s (M3).
- **S2.4.** A worker's `ask` times out at 18:45Z: the question stays open in every machine. No attempt or item transition treats it as answered, and no reply is synthesized.
- **S2.5.** The coordinator `reply`s to one question: that item is RESOLVED; the others are not.
- **S2.6.** Observer polls use only non-consuming views: the fake asserts zero plain `check` and zero `--ack` calls, and that the coordinator's later `check` returns the same batch it would have returned without the observer.
- **S2.7.** Coordinator terminal shows a permission prompt: no wake (X4), owner notified.

**Scenario 3: Codex overshoot (A6, 14:52–14:57Z).** Reading 88% with one running section, then 90%, then 92%. Expected: SUSPENDED from the first reading at or above 75% (P5; the ceiling is 75); one checkpoint request (L8); no new admission; the overshoot to 92% is recorded and the journal flags it as `OVERSHOOT_AFTER_SUSPEND` for reservation calibration.

**Scenario 4: Codex reset (A6, 18:28–18:32Z).** SUSPENDED at 92% with `resets_at` 18:28Z, then the clock passes 18:28Z (P7), no fresh T1. Expected: `AWAITING_RESET_EVIDENCE`. In a supervised session the queued MR1 task is admitted as the single probe (P9). The fresh T1 at 18:31:53Z shows 1.0%, next reset 23:31Z, weekly 15%: READY_TO_RESUME (P10). The waiting task resumes once (L18), then ACTIVE (P13). A second admission is allowed only after P10.

**Scenario 5: Codex update prompt (2026-10-19).** `worker-start` returns `failedStage: agent_readiness`, `agent-update-prompt`. Expected: L6; zero keystrokes; zero retries; owner notified; slot held; L20 after the owner clears it by hand.

**Scenario 6: conflicting Claude readings (A6, 15:27–15:30Z).** ESTIMATE 44% and owner observation 6%. Expected: the 44% governs; status prints `44% (ESTIMATE)`; no percentage without its class.

**Scenario 7: Orca restart mid-section.** Orca unreachable for 3 polls, then back with a new runtime ID and the worker `restored_unconfirmed`. Expected: C7, C8, C6; attempt UNVERIFIABLE; no new writer; after the worker's next heartbeat, RUNNING (L14).

**Scenario 8: coordinator fenced.** `run-show` returns a different coordinator handle. Expected: C6, then `COORDINATOR_ABSENT`; every admission refused; mailbox items go to the owner; zero `run-use` calls.

Totals for D7 (ii) acceptance: **57 transition tests + 25 boundary tests + 6 security tests = 88 unit tests, plus 8 scenarios (18 scenario cases).**

### 11.3 D7 (iv) lifecycle pilot

**Preconditions.**

- D7 (ii) is implemented, all offline tests pass, Claude has independently reviewed it, and the owner has approved the pilot (OD6).
- D7 (iii) reads are authorized: one T2 read, and the T3 bridge configuration.
- No production writer is live on the host. Pilot steps PS1–PS3 restart or reboot the machine, which interrupts every Orca session.

**Setup.**

- A disposable Orca Run created for the pilot.
- A disposable worktree on branch `pilot/observer-<date>`, never pushed.
- Two harmless tasks: a Codex worker that writes a timestamp into a scratch file and reports, and a Claude worker that does the same. Each is bounded to about 5 min.
- Observer started by hand, first in **shadow mode** for one hour: it observes and journals, but `ohv-admit` only logs its decision and the coordinator dispatches by hand. Then live mode.
- Spend cap for the whole pilot (decided): at most 6 Codex sections and 4 Claude sections, at most 1 of each running at a time.

| Step | Action | Pass criteria |
|---|---|---|
| PS0 | Shadow hour, then live: admit, run and settle one task per pool | Shadow decisions match the coordinator's manual decisions; every transition journaled; the `checkpoint_request` message type is accepted or falls back as specified; T1, T2 and T3 readings present with source class; zero observer model calls |
| PS1 | With one worker running and one unanswered `question` pending, restart Orca once | C7 → C8 → C6 → C4 observed; the attempt is UNVERIFIABLE until positive liveness, then RUNNING or FAILED from evidence; the pending question is surfaced again within 120 s of Orca returning; no duplicate Dispatch (Task and Dispatch counts compared before and after); U1 result recorded |
| PS2 | Sleep the Mac across a known `resets_at` or a test deadline, then wake | Clock discontinuity detected; all readings stale; no admission until a fresh reading; no heartbeat gap treated as exit; U2 result recorded |
| PS3 | Checkpoint a section to WAITING_FOR_CAPACITY, then reboot once and log in | Observer starts (by hand, or via the launch service if OD7 allows); reconciliation finds the WAITING task, resumes it exactly once after a fresh reading, and leaves no second attempt; U3 result recorded |
| PS4 | Set `DISABLED` during a live admission | No start; no message; owner notification only; running worker untouched |
| PS5 | Inject a `question` and an `escalation` from the pilot worker; leave them unanswered | NEW within 60 s; SURFACED or ESCALATED within 120 s; re-notified at 60 min; never treated as answered after the worker's `ask` timeout; U10 and U11 results recorded |
| PS6 | Observe one natural reset of either pool (no forced reset, no credit) | Reset confirmed only via the P8 or P10 guard; resume exactly once |
| PS7 | Calibration | Per-section deltas for each pool and window recorded with source class; proposed reservation values written for owner review (OD4) |

**Pilot fails** on any one of the following:

- any observer-initiated model call;
- any duplicate Dispatch for one section;
- any keystroke into a prompt;
- any admission while QUOTA_UNKNOWN in unattended mode;
- any unresolved blocking item without a wake or owner notification after 120 s of successful polling;
- any read of a credential file;
- any repo write by the observer;
- any account or setting change by the observer.

The pilot report is committed by the coordinator to the run branch, sanitized.

### 11.4 What is not claimed

**Unattended autonomy is not claimed by this specification, by its implementation, or by passing the offline tests.** Until the D7 (iv) pilot passes **and** the owner separately decides D7 (v) activation, the program remains `RUNTIME_NOT_READY`:

- the observer runs only supervised;
- unattended admission is hard-wired off (`UNATTENDED_NOT_ACTIVATED`);
- Claude stays attended-only until U6 passes, because its weekly window has no source;
- no "autonomous across resets" claim appears in any report (incident rule C4).

## 12. Engineering choices decided here

These are routine defaults inside the approved constraints, recorded so that review can check them. None is an owner question.

- Python 3.12 stdlib; SQLite WAL journal with `synchronous=FULL`; `fcntl` lock; atomic write-and-rename for telemetry snapshots.
- Poll interval 60 s, for both telemetry and mailbox.
- Freshness 10 min with active consumers, 60 min otherwise.
- Heartbeat loss after 3 intervals (15 min).
- Checkpoint grace 20 min (CLOSING) and 10 min (SUSPENDED).
- Surfacing bound 120 s; ack deadline 15 min; one re-notification at 60 min; wake rate limit 5 min.
- `conserve_at = 75` (lower bound of the owner's range); `closing_at = 85`; thresholds clamp to the ceiling.
- Full reservation is kept for every non-terminal attempt (deliberate double counting).
- Owner cap exceptions expire at the end of the current five-hour window.
- `ohv-admit` runs in the coordinator's terminal (no caller impersonation). `--spec`, `--on` and `--terminal` are refused.
- The observer never writes the repository and never stops a worker.
- Owner notification is local only (macOS notification and log), carrying no message bodies.
- Pilot spend cap: 6 Codex and 4 Claude sections, one per pool at a time.

## 13. Owner decision packet

One reply can accept every recommended default: `Observer spec: accept defaults`, or `accept defaults except OD<n> …`. Nothing is approved by silence, by timeout or by merging this draft.

| ID | Decision | Recommended default |
|---|---|---|
| OD1 | Approve this spec as the basis for D7 (ii), the offline implementation and tests | **Approve** after Claude's own spec review is answered and any owner edits are applied. Implementation goes to Codex under the normal workflow |
| OD2 | Telemetry authority for unattended use | **T2 (app-server read) only, after U5 passes.** T1 stays valid for supervised sessions and for every move toward a more conservative mode, but is not unattended authority, because it is an undocumented cache (MR4). An unattended reset probe is not allowed |
| OD3 | Claude telemetry | **Approve configuring the T3 status-line bridge during the pilot (D7 iii).** Claude stays attended-only until U6 passes **and** a weekly-window source exists. ccusage stays an ESTIMATE that can only tighten |
| OD4 | Reservations and caps | **Keep the incident caps (Claude 1 beside the coordinator, Codex 2) and the §4.4 reservation defaults until PS7 calibration**, then decide new values from the pilot report. Owner cap exceptions are allowed only in supervised sessions and expire with the window |
| OD5 | Wake and notification channels | **Coordinator wake via fixed-text `terminal send` only when idle and prompt-free (withdrawn if U11 fails); owner notification local only.** No Hermes, Telegram or Slack channel in v1 |
| OD6 | Pilot authority (D7 iv detail) | **One Orca restart, one sleep, one reboot, in a disposable Run and worktree, at a time with no production writer live, within the §11.3 spend cap** |
| OD7 | Host service | **Manual start for the pilot.** A single user LaunchAgent is considered only after the pilot passes, as part of D7 (v). No root daemon, no sleep inhibition, no Orca automation |
| OD8 | Automatic worker stop | **Never in v1.** The observer requests checkpoints and notifies; only the coordinator or owner stops a worker |

### Material risks, flagged separately

- **MR1: conservative admission is not a hard ceiling.** Telemetry lag, interactive use by the owner on the same accounts and in-flight overshoot (88% → 92% after SUSPENDED, A6) mean a pool can cross a threshold. Reservations reduce the risk but do not remove it (U8). Reports must say "conservative admission", never "guaranteed below 90%".
- **MR2: Claude has no verified percentage and no weekly source.** Until U6 passes and a weekly source exists, every Claude decision rests on caps, rejection events, estimates and owner observations. That is why Claude stays attended-only.
- **MR3: the wake types into the coordinator's terminal.** If idle detection misreads a prompt as the input box (U11), the wake text could land in a prompt. Mitigations: idle check, prompt signatures, a fixed text with no `y` or option keys, a rate limit, and withdrawal if U11 fails.
- **MR4: T1 is an internal Codex file.** A Codex update can change it silently. The adapter fails closed (window unknown), which stops admission rather than misreading. It is not unattended authority (OD2).
- **MR5: the pilot interrupts the host.** The restart and reboot steps stop every Orca session on the machine. Schedule them with no production work live.
- **MR6: the mailbox views may not be fully non-consuming from outside the coordinator (U10).** If the only available views alter read state, the observer could hide a message from the coordinator. Test S2.6 and pilot step PS5 must pass before the observer polls a real coordinator mailbox.

## 14. UNKNOWN register

U1–U9 are from the feasibility assessment (A4); U10–U12 are new here. All are settled in the pilot or by the named check, not assumed.

| ID | Unknown | Settled by |
|---|---|---|
| U1 | Orca app-restart persistence and worker survival | PS1 |
| U2 | Sleep/wake liveness and timers | PS2 |
| U3 | Reboot/login recovery and observer startup | PS3 |
| U4 | Current-Run orphan and rebind semantics (`consumer_fenced`) | Not needed for v1: the observer never rebinds; recorded only (scenario 8). Required before any unattended coordinator replacement |
| U5 | Codex app-server read: buckets, `ordinaryUsageAllowed`, idle freshness | D7 (iii) single read; PS6 |
| U6 | Claude status-line payload completeness and idle-reset behaviour | D7 (iii) bridge; PS0, PS6 |
| U7 | Caller-chosen initial request ID; idempotency across caller identities | Pilot B18 counterpart on real Orca; until then a lost pre-ID response leaves the attempt OUTCOME_UNKNOWN |
| U8 | Hard-percentage enforcement versus bounded section cost | PS7 calibration; MR1 stays until then |
| U9 | Permission parity after resume; checkpoint handshake | Offline X4, B18, L8–L10; PS3 |
| U10 | Whether `inbox --terminal` or `check --all/--peek` work from a non-coordinator process without consuming, and expose ack and reply linkage | PS5; S2.6 against real Orca in the disposable Run |
| U11 | Whether `terminal wait --for tui-idle` separates an idle input box from a prompt | PS5; adversarial check with a deliberate prompt in the pilot terminal |
| U12 | T1 record stability across Codex versions | Re-checked at every Codex update; the adapter fails closed |
