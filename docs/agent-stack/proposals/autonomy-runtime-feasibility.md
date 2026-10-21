# Autonomous runtime feasibility

Draft technical assessment, 2026-10-19; evidence collected starting at 22:32 UTC.
**Not approved for activation. Nothing installed, enabled, scheduled, or updated.**

## Result and scope

Persistence and quota-aware admission are **partly feasible** with the installed tools. Orca supplies durable coordination records, attempt identities, recovery receipts, and scheduled prompts. Codex exposes a generated quota protocol; Claude Code documents quota fields in status-line JSON. These establish useful building blocks, not a verified unattended restart-and-resume system. In particular, fresh Claude quota observations while idle, current-Run coordinator replacement, and worker recovery across restart/reboot remain UNKNOWN. A strict account-wide consumption ceiling also requires control of competing consumers and a defensible bound on work already admitted.

Recommendation: approve a separate specification for an **observer/admission controller first**, then an isolated recovery pilot after the checks below. Do not activate overnight scheduling from this assessment. The optional code prototype is deferred: Q1/Q2 do not yet establish the complete recovery and fresh-reset path. Synthetic tests alone would not close those gaps.

Target: `k-kopacek/autonomy-feasibility` in the assigned worktree. Starting HEAD and local `origin/main` were both `c04f5d6acd19f6bc81d324dd0d4947660cd051cc`; the worktree was clean. Those are local observations, not refreshed GitHub state. Only this proposal is changed; production, data, local-AI tools, provider configuration, permissions, and startup configuration are outside scope. No additional model invocation to measure usage or authenticated quota request was made.

## Evidence register and reproduction

Every installed-tool conclusion below refers to these commands, generated schemas, or existing local files. Design choices are explicitly proposals. Official web documentation was retrieved on **2026-10-19**; it can describe a newer release, so installed help/schema take precedence for installed capability. No private transcripts, database dumps, credentials, or machine caches are included in this commit.

| ID | First-hand evidence and decisive observation |
|---|---|
| E1 | `pwd`; `git status --short`; `git branch --show-current`; `git rev-parse HEAD origin/main`; `git remote -v`: assigned checkout/branch, clean start, equal local heads, `k-kopacek/ohvernight` origin. No fetch performed. |
| E2 | `codex --version`: `codex-cli 0.160.1`; `claude --version`: `2.1.303 (Claude Code)`. `orca status --json` reports `result.runtime.appVersion: 1.4.224`; `/usr/libexec/PlistBuddy -c 'Print :CFBundleShortVersionString' /Applications/Orca.app/Contents/Info.plist` agrees. `orca --version` emits general help rather than a numeric version in this installation. No update accepted. |
| E3 | `orca --help`; `orca orchestration --help`; **each** orchestration subcommand's `--help`, listed below. `run-create` explicitly says a Run never schedules or places workers. |
| E4 | `orca skills get orchestration --json`, plus `--reference references/recovery-and-cleanup.md`, `references/messaging-and-gates.md`, `references/coordinator-loop.md`, and `references/legacy-contract-migration.md`: version-matched local lifecycle, replay, liveness, recovery, and takeover documentation. |
| E5 | `orca skills get orca-cli --json`; `orca skills get orca-cli --reference references/automations.md --json`; `orca automations --help`; **each** automation subcommand's `--help`. Singular `orca automation --help` is rejected; the installed noun is `automations`. |
| E6 | Read-only SQLite connection to `~/Library/Application Support/Orca/orchestration.db` using URI `mode=ro`; `PRAGMA user_version` is 43. `SELECT name, sql FROM sqlite_master WHERE type='table'` shows on-disk `runs`, `tasks`, `dispatch_contexts`, `messages`, `deliveries`, `mutation_receipts`, `question_threads`, `worker_dispatches`, `worker_terminal_resources`, and `worker_terminal_archives`. Table presence proves storage now, not a recovery SLA. |
| E7 | `orca orchestration run-show --id run_bec8936210b9 --json`; `orca orchestration worker-show --dispatch ctx_9852cc201116 --json`; predecessor `worker-show --dispatch ctx_40ac84f09719 --json`: actual binding, live current attempt, failed predecessor and retry linkage, detailed below. These read-only inspections used the local runtime socket. |
| E8 | `codex --help`; `codex exec --help`; `codex resume --help`; `codex debug --help`; `codex app-server --help`; `codex app-server generate-json-schema --help`. Generated offline with `codex app-server generate-json-schema --out /private/tmp/autonomy-feasibility-evidence/codex-schema`, without `--experimental`. |
| E9 | Generated `codex-schema/ClientRequest.json`, `ServerNotification.json`, `v2/GetAccountRateLimitsResponse.json`, and `v2/AccountRateLimitsUpdatedNotification.json` under the E8 output directory. These are version-matched schemas, not a live account response. Regenerate rather than depend on the temporary directory surviving. |
| E10 | An existing Codex session record under `~/.codex/sessions/` (file name withheld from this public document): selected only `event_msg` / `token_count` / `rate_limits` fields, one observation on 2026-10-19. It contains 300-minute and 10,080-minute windows. This is a cached internal file, not an established public telemetry contract. |
| E11 | `claude --help`: JSON/stream-JSON print output, API-dollar budget flag, resume/background commands and permission controls; no standalone quota-read command advertised. `~/.claude/settings.json` has a `statusLine` command configuration; only its presence/type was inspected. No hook executed or configuration changed. |
| E12 | Official [Claude Code status-line documentation](https://code.claude.com/docs/en/statusline), especially Available data and Usage limits; official [monitoring documentation](https://code.claude.com/docs/en/monitoring-usage), Available metrics. |
| E13 | Official [Codex App Server documentation](https://developers.openai.com/codex/app-server/) (redirected to [ChatGPT Learn](https://learn.chatgpt.com/docs/app-server)), Authentication / Rate limits and protocol initialization. |
| E14 | Installed `man launchd.plist`: `KeepAlive`, `RunAtLoad`, `StartInterval`, `StartCalendarInterval`, `LimitLoadToSessionType`; `orca serve --help`: foreground headless runtime, stopped with Ctrl+C. No launch service was loaded and no server started. |
| E15 | Current repository `AGENTS.md`, `docs/agent-stack/{master-coordinator,roles,overnight-autonomy,capacity-routing,codex-technical-worker,orca-bootstrap,hermes-research}.md`, `docs/architecture/agent-stack.md`, and product/trust principles. These establish authority, checkpoints, independent workers, reserves and owner gates. |

Help coverage (each command below was executed with `--help`, without invoking its action):

```text
orca orchestration:
  run-create run-use run-current run-list run-show
  send check reply inbox ask
  task-create task-list task-update dispatch dispatch-show request-show
  worker-start worker-show worker-read worker-stop worker-abandon
  worker-release worker-retain worker-list
  coordinator-start coordinator-stop gate-create gate-resolve gate-list reset
orca automations:
  list show create edit remove run runs
```

For E6, reproduce without reading record bodies or authentication material:

```python
import sqlite3
from pathlib import Path
path = Path.home() / "Library/Application Support/Orca/orchestration.db"
connection = sqlite3.connect(path.as_uri() + "?mode=ro", uri=True)
print(connection.execute("PRAGMA user_version").fetchone())
for name, sql in connection.execute(
    "SELECT name, sql FROM sqlite_master WHERE type='table' ORDER BY name"
):
    print(name, sql)
```

E6 is implementation evidence only. Never write Orca's database or implement the controller against its private tables. Supported CLI reads must remain the integration boundary. Initial sandboxed runtime inspection returned `runtime_access_denied`/EPERM; approved socket access succeeded. This is an execution boundary, not evidence that Orca was stopped. [E3, E4, E7]

## Q1 — Orca persistence, supervision and recovery: partly feasible

### What is durable, and what survival is unverified

| Object | Evidence today | App restart | Machine sleep/wake | Reboot/login |
|---|---|---|---|---|
| Runs | On-disk `runs`; live Run read succeeds [E6, E7] | Record recovery UNKNOWN | Read/recovery after wake UNKNOWN | Record recovery UNKNOWN |
| Tasks / Dispatches | On-disk task/attempt rows, actual retry linkage [E6, E7] | Restored authority/liveness UNKNOWN | Lease/liveness freshness after wake UNKNOWN | Reconciliation and process recovery UNKNOWN |
| Worker terminals / agents | Current attempt has fleet `live`, terminal identity and process incarnation [E7] | Process survival/reattachment UNKNOWN | Agent/network recovery UNKNOWN | Same-process survival cannot be assumed; automatic replacement/resume UNKNOWN |
| Worktrees / commits | Git worktree files and local commit history [E1] | On-disk material exists; Orca rediscovery UNKNOWN | Post-wake rediscovery UNKNOWN | Post-login rediscovery UNKNOWN; no reboot test |
| Messages / asks / Deliveries | Database records; local guide promises durable enqueue and replay-until-ack [E4, E6] | Exact restart replay/consumer recovery UNKNOWN | Delivery/attention after wake UNKNOWN | Exact replay/consumer recovery UNKNOWN |
| Automations / run history | Supported scheduling/history interfaces [E5] | Execution while app closed UNKNOWN | Catch-up policy enforcement UNKNOWN | Host startup/login behavior UNKNOWN |

No restart, sleep or reboot was induced. The database and Git are durable storage evidence; they do not prove that an agent, authenticated consumer, or scheduler comes back alive. The exact event tests that settle these UNKNOWNs are U1–U3 below. No event gets a survival guarantee from a filename or capability name.

### Supervision and scheduling actually offered

`worker-start` composes worker placement/readiness/input/resource ownership. `worker-list --run <id> --include-remote --json` provides agent fleet liveness, attention and literal next-action argv, with cursor pagination. `worker-show` also exposes PTY observations: a live PTY alone does not prove a live agent. `worker-read` reads a proven transcript or bounded terminal output. Missing/stale status, contact loss, a quiet transcript, TUI idle and an expired heartbeat are not positive exit evidence. Preserve `unverifiable`; do not launch another writer. [E3, E4]

Heartbeat is a typed `send` message with exact Task and Dispatch IDs. The current worker preamble requests a heartbeat every five minutes; that is this dispatch's reporting contract, not an observed automatic kill/retry timeout. `check --wait` emits transport keepalives every 15 seconds, explicitly unrelated to worker heartbeat. There is no verified automatic restart policy implied by either mechanism. [E3; live dispatch instructions]

`worker-stop` fences/stops the exact supervised worker; `worker-abandon` fences orchestration without claiming the process stopped; release follows accepted settlement, archives output and applies resource-ownership checks. Retrying a proven failed/stopped attempt uses the same Task plus `--retry-of <dispatch-id>` and explicit placement. The guide documents a circuit breaker after three consecutive Task failures. `request-show` resolves uncertain mutation receipts. The old `coordinator-start` is retired and documented as having no effects; it is not an unattended scheduler. `reset` is destructive recovery, not a routine restart. [E3, E4]

Orca automations accept presets, five-field cron and RRULE, timezone, enabled/disabled state, missed-run grace, history, and a bounded precheck: zero continues; nonzero records a skipped run. Existing-workspace session reuse is supported; if its prior terminal is gone, the guide says it falls back to a fresh session. None of this establishes Task/Dispatch deduplication, quota enforcement, app-closed execution, or exact missed-run handling. Do not equate automation run history with orchestration Runs. `serve` is a foreground headless option, not evidence of an installed persistent service. [E5, E14]

### Coordinator binding and the reported fence

The current Run read identifies coordinator `term_358f0904-eda0-4b7b-b472-76a928e2f425` and `consumer_generation: 1`. The read-only database schema also records coordinator handle, pane key, optional Orca session ID and the generation at which that session ID is valid; Deliveries carry consumer generations. In this Run the optional session ID is null, so it would be wrong to claim this binding is session-ID-based in every mode. [E6, E7]

`run-create` creates and binds a namespace; `run-use --id <id>` binds an existing Run. Its help advertises `--takeover-legacy` specifically for legacy takeover from the live invoking coordinator terminal. The legacy guide says that takeover fences the old coordinator, moves pending mail, and preserves workers/processes/files; it must not be used while the original coordinator is actively coordinating. These are **legacy-specific** promises, not proof of ordinary current-Run takeover when a coordinator disappears. [E3, E4]

The task input reports `worker-start` returning `consumer_fenced` when bound to another coordinator session. That incident was **not independently reproduced**: deliberately dispatching or rebinding this active Run would alter coordination. A bounded read-only search of the four most recent stored mutation receipts matching that string found no matching receipt; this neither disproves the report nor establishes its cause. Current-Run orphan recovery, precise fence conditions and whether rebinding preserves pending Deliveries are **UNKNOWN**; U4 specifies the isolation test. A host scheduler cannot gain coordinator authority simply by supplying `--from`, copying IDs, or retrying under a new Run. [E3, E4, E6]

There is a real retry example: predecessor `ctx_40ac84f09719` for `task_390f1834de81` is failed at `agent_readiness`, with `Agent startup blocked: agent-update-prompt`. Current `ctx_9852cc201116` names that predecessor in `retryOfDispatchId`, is dispatched/ready and fleet-live, and reuses the terminal resource. This proves supported retry metadata and current progress; it does not prove unattended handling of that update prompt. The requested Codex 0.161.0 update was not installed or independently queried. [E2, E7; task input]

## Q2 — Supported usage telemetry: partly feasible

### Codex 0.160.1

The installed app-server interface is advertised as experimental. Its default generated schema, without experimental fields enabled, contains request `account/rateLimits/read` and notification `account/rateLimits/updated`. `GetAccountRateLimitsResponse` requires `rateLimits`, with optional/null `rateLimitsByLimitId`; each `RateLimitSnapshot` may have nullable primary/secondary windows. A `RateLimitWindow` requires integer `usedPercent`; `windowDurationMins` and `resetsAt` can be null or missing. Therefore neither slot proves a five-hour or weekly window: classify by returned duration, require applicability evidence, and fail closed on missing applicable windows. [E8, E9]

Other decisive installed fields: `accountId` associates the snapshot with an account when available; `ordinaryUsageAllowed` is nullable, and its schema explicitly says unavailable permission must not be inferred from percentages or reset times. `spendControlReached` is also nullable. Rolling notifications are sparse; their schema says merge available values into the last read snapshot or refetch, and nullable account metadata does not clear a previously observed value. A missing window/permission is not a successful reset. Reject account changes and stale snapshots rather than silently inheriting another pool's data. [E9]

The official protocol documents JSON-RPC initialization and the quota read/notification, per-bucket values, and Unix-seconds reset timestamps. It also documents token-history reads separately. The smallest future adapter should use this protocol, not parse `/status` screen text. Do not call login/logout, earned-reset consumption, add-credits email, or other mutations. The actual authenticated read, all applicable buckets, account mapping, backend permission availability and freshness while idle remain UNKNOWN here; see U5. [E13; installed structure E9]

An existing session record (2026-10-19) carried a `limit_id: codex` entry with a 300-minute and a 10,080-minute window, each with a used percentage and a reset time; the values are withheld from this public document under the charter's rule against committing usage or account data (06). This is an observation of a cached record, **not a current headroom assertion**. Its snake-case fields differ from the public app-server schema. Neither token totals, cost totals, nor this historical cache establish complete pool membership, a stable file contract, provider quota denominators, or current reset completion. No direct credential file or private backend endpoint was used. [E10]

### Claude Code 2.1.303

Installed help offers `--output-format json|stream-json` and `--max-budget-usd` for print-mode API dollars; neither advertises subscription-window headroom. No standalone quota-read subcommand appears in that help. Background/resume commands provide session management, not quota proof. A status-line command is configured locally, but no current payload was captured and no configuration was edited. [E2, E11]

The official status-line JSON contract documents `rate_limits.five_hour` and `seven_day`, each with `used_percentage` and Unix-seconds `resets_at`. Availability is conditional: supported subscription/gateway context, after the first API response; windows can be independently absent and are dropped after reset time. Thus absent data cannot verify recovery. A future status-line bridge can atomically retain selected fields and receipt time, but is event-fed, not an established independent idle refresh. Actual payload availability, account-wide completeness and an idle fresh-reset read remain UNKNOWN (U6). No TUI scraping or configuration change was performed. [E12]

Official monitoring lists token/cost metrics; those are consumption observations, not evidence of a subscription allowance or reset. [E12] Supported machine-readable data exists, but full automatic dispatch after an idle reset is not established for this installation. Do not bootstrap it by spending a model call merely to measure usage. A missing observation keeps that pool blocked.

### Interface classification

| Interface | Classification for this proposal |
|---|---|
| Version-matched Codex generated app-server protocol | Documented machine interface; command marked experimental; authenticated behavior not exercised [E8, E9, E13] |
| Claude status-line stdin JSON | Documented event-fed machine interface; local payload and idle recovery unverified [E11, E12] |
| Claude print JSON, token/cost metrics; Codex token-history reads | Supported outputs, insufficient evidence of applicable subscription windows [E8, E11–E13] |
| Codex session `token_count.rate_limits` records | Observed internal historical cache; not approved as scheduler authority [E10] |
| Orca private SQLite / recovery JSON / provider cache files | Storage/diagnostic evidence only; no established public quota contract [E6, E9–E11] |
| `/usage`, `/status` rendered screens; terminal title/status text | Human-facing display; not used as machine telemetry |
| Undocumented OAuth usage endpoints, browser cookies, credential extraction | Not investigated or proposed |

No price, request quota, fixed task cost, account sharing, or reset cadence is inferred from a model name, UI label or example duration.

## Q3 — Smallest host-side controller: design feasible, activation blocked

This section is a **proposal**, not installed behavior. Separate a model-free observer/admission controller from Claude's planning authority. It may admit only packages already approved and queued by Claude/owner; it must not invent scope or substitute Codex for the coordinator. [Authority: E15]

### Components and state locations

1. **One user process**, standard-library Python or Node, with one loop and per-pool decisions. Start manually for a future pilot. Only after validation, a user LaunchAgent may supervise it. `KeepAlive` supports relaunching a process; `StartInterval` can miss events during sleep, whereas `StartCalendarInterval` coalesces missed events on wake. These host semantics do not prove Orca readiness or wake the machine. Do not add cron, a second controller, or an Orca prompt automation alongside it. [Host evidence: E14]
2. **Read-only telemetry adapters** for the documented Codex protocol and an owner-approved Claude bridge, each returning explicitly identified pool/account, source version, received-at, applicable windows, used percent, reset times and any admission/spend restrictions. Until U5/U6 pass, adapters yield UNKNOWN. Do not guess shared membership for Hermes; configure verified consumers. [Interface basis: E8–E13; pool policy E15]
3. **Atomic admission/checkpoint journal**, proposed private root `~/Library/Application Support/Ohvernight/autonomy/`: `policy.json` (version/hash, reserves, estimates, ceiling and source provenance); `state.sqlite3` (transactions for pools, task attempts, request IDs, checkpoint acknowledgements and event journal); `telemetry/<pool>.json` (selected fields only); `controller.lock`; and `DISABLED` (kill switch). None of these paths is created by this assessment. Use user-only permissions, no credentials or full transcripts, and no private runtime files in Git/public output.
4. **Durable worker checkpoints** remain in the existing repository convention `docs/agent-stack/runs/<run-id>/<worker>/checkpoint.md`, with coordinator queue/locks/approvals/owner-return at the run root. Include input/working SHA, dirty paths, completed section/artifacts/tests, exact Task/Dispatch/request IDs, scope/approval provenance, remaining budget, next step and reset evidence. Commit only when the package authorizes a commit; never auto-stage unrelated work. [E15]
5. **An Orca adapter**, disabled until current-coordinator binding recovery is verified. Enumerate Tasks/Dispatches and reconcile exact attempts before any mutation. Use only documented CLI commands and receipts, never private SQLite writes or terminal approval keystrokes. The controller can observe without coordinator authority; it cannot claim lifecycle authority it has not proved. [E3, E4, E6]

### Ceiling and admission rule

Apply the strictest constraint to **every applicable window in a pool**. Proposed configuration supports a 90%-consumed ceiling, but that owner preference does not replace today's reserves. Let values below be percent of that particular window, with costs converted only using a known denominator:

```text
reserve(Codex/Hermes, window) = max(25, next_day_build_and_verification_plus_handoff)
reserve(Claude, window)       = max(15, material_review_plus_return_and_checkpoint_margin)
effective_ceiling             = min(configured_ceiling=90, 100 - reserve)
admit only if                 used + outstanding_reserved_cost
                              + next_section_bound + checkpoint_bound
                              < effective_ceiling
```

Thus baseline ceilings are at most 75% for the shared Codex/Hermes pool and at most 85% for Claude, and may be lower. Estimates and margins are per window; an unknown denominator or missing estimate is UNKNOWN, not zero. Equality blocks. Weekly exhaustion still blocks after a five-hour reset. This is a stricter proposed admission rule consistent with `capacity-routing.md`; the task explicitly overrides that document's fallback of one conservative section when observation is unavailable: **unknown capacity means no dispatch**. [E15; current task instruction]

Serialize admission and reserve all accepted/in-flight sections, including checkpoint costs. Start with one active section per verified shared pool; external/unmanaged consumers require either conservative bounded reservations or blocking. Samples have an owner-approved maximum age, but a timestamp alone does not prove absence of intervening consumers. A forecast is not a hard consumption bound. Until bounded section cost, telemetry lag and competing consumption are controlled, advertise this as conservative admission/checkpoint policy, **not a guarantee that account usage can never cross a percentage**. Hard enforcement is UNKNOWN (U8).

### State machine

| State | Behavior and transition |
|---|---|
| `running` | Reconcile exact active work; admit only approved ready sections with fresh complete telemetry and reservations. Before the next section would fail the rule, persist `checkpointing` and request an exact-attempt checkpoint; admit nothing further for that pool. |
| `checkpointing` | Wait for durable checkpoint acknowledgement at a safe section boundary. A sent message is not acknowledgement. Preserve active work and resource ownership. Successful acknowledgement moves to `sleeping` for a capacity constraint or `blocked` for an authority/permission issue; missing/failed acknowledgement remains blocked with the active attempt recorded. |
| `sleeping` | Persist all constraining windows and the next observation deadline. Perform no model work. A timer only permits a fresh read; it never authorizes dispatch. Wake on the earliest relevant verified reset deadline, reevaluate all windows, and reschedule remaining constraints without hot polling. |
| `resuming` | Acquire the single-controller lock; reload policy/authorization and committed state; enumerate runtime, tasks, attempts, resources and mail; obtain fresh telemetry. Resume only the exact safe next section after positive reset/capacity evidence and ownership checks. Running/completed/uncertain attempts are never re-dispatched. |
| `blocked` | UNKNOWN/stale quota, missing account mapping, missing authorization, fence, prompt, lost runtime/lease, incompatible schema or unsafe dirty state. No dependent dispatch. Independent pools may proceed only through their own fully verified gates. Exit only after new positive evidence; no timeout supplies approval. |

On a reset deadline, require an observation received **after** the old deadline, matching account/bucket/window, positively identifying the successor window (e.g. later reset boundary plus observed usable consumption) and satisfying the reserve rule. Require any backend admission restrictions to permit work; installed Codex's unavailable `ordinaryUsageAllowed` is not inferred true. A stale sample, advanced wall clock, zero token history, sparse null notification, dropped Claude window or returned permission error does not prove a reset. A sliding/changed window contract requires adapter validation, not fabricated epoch arithmetic. [Design based on E9, E12]

If a future supported source explicitly establishes no window applies, record that applicability evidence; omission by itself is not that evidence. Backoff/TTL are configurable host policy, not provider limits. Persist UTC deadlines, use a monotonic clock for in-process waits, and re-read on clock discontinuity or wake. Unknown reset times block instead of guessing five hours or seven days from now.

## Q4 — Coordinator or Codex unavailable: partly feasible

Already-authorized independent workers may continue within package inputs, file ownership, section budgets and reserves while Claude sleeps; cross-package dispatch, independent Claude review and owner decisions wait. Codex unavailability does not turn Hermes into an implementation worker. Same-pool Hermes work stops at the shared reserve; other pools proceed only with verified separation and permission. These are repository rules, not guarantees of process survival. [E15]

The proposed host process can keep its own journal, wait on deadlines and make permitted telemetry/runtime reads without model inference. It cannot restore a crashed provider or take coordinator ownership based only on a timeout. If Orca is unavailable, retain intent/receipts and mark the runtime unverifiable; no starts, rebinds, cleanup, invented completion, or competing editors. If the host sleeps, do not promise execution until it wakes. A LaunchAgent may relaunch the controller in its approved user session, but authenticated provider and Orca recovery still require U1–U6. [E3, E4, E14]

At each section boundary workers write and acknowledge their checkpoints before continuing. For predicted ceiling crossing the controller stops admission early enough to reserve checkpoint capacity. If an agent dies mid-section, preserve dirty files and the last checkpoint; restarting a task from that checkpoint requires runtime reconciliation and proof that the former writer is exited/fenced safely. Do not blindly kill a calculation or close a terminal to save quota. An acknowledgement lost across transport is reconciled by IDs and saved artifacts. [E4, E15]

**Without a human:** only approved queued work may resume after verified capacity/reset, a valid same-authority runtime recovery, and proven exclusive attempt ownership. Read-only observer recovery is the first practical increment. Autonomous replacement of a missing current-Run coordinator is not verified, and Claude's idle telemetry gap prevents promising full unattended resumption. Keep those transitions blocked until U4/U6 pass; an owner approval prompt remains human-gated indefinitely.

## Q5 — Idempotency and permission boundaries: partly feasible

Use a stable logical package/section key plus `run_id`, `task_id`, `dispatch_id`, `retry_of`, explicit placement, input SHA, package hash, coordinator generation/identity and policy version. One Task represents work; one Dispatch represents an attempt. Never create a new Task with `--spec` to route around a failed attempt or circuit breaker. [E3, E4]

Proposed dispatch transaction:

1. Acquire an OS file lock for the controller and use a transactional journal. Store a new controller epoch/lease owner; lease expiry authorizes reconciliation only, never a replacement writer. A second controller must acquire the lock and positively reconcile outstanding operations. A lease counter alone does not fence Orca processes.
2. Reload exact authorization, source/file allowlists, latest checkpoint and pool reservation. Enumerate `task-list`, `dispatch-show`, `worker-list` with all pages, then exact `worker-show` as needed. A completed Task is not run again; active, pending-start and unverifiable attempts retain reservations and block replacement. [CLI basis E3, E4]
3. Persist a local intent UUID **before** issuing the permitted mutation against an already-known Task. Record the tool-issued request ID and returned Task/Dispatch immediately, preserving exact arguments for recovery with `--retry-request`. The help describes that flag as recovery, not a general first-call idempotency-key API: whether a client can preassign the initial Orca request ID is UNKNOWN (U7). A local intent UUID must not be passed off as an Orca receipt identity. If the first response is lost before an Orca request ID is known, reconcile the known Task/attempt and block if ambiguous; do not replay blind. Do not assume a host-process restart retains Orca caller identity. [E3, E4; schema E6]
4. After a lost response, use `request-show --request <id> --json`. `completed` replays the prior receipt; `pending` requires inspecting the original command before exact replay; `absent` means no receipt under that caller identity, not proof of no effect. Reconcile Task/Dispatch/worktree/resource state before any retry. Caller-identity changes are a blocker until U7 passes. [E3, E4]
5. Retry only a proven failed/stopped attempt, same Task, explicit `--retry-of` and placement. An abandoned worker can remain live: do not start another writer on its surface until exclusivity is positively established. Inspect `failedStage`, `effects`, `residualResources` and exact recovery receipts. [E3, E4]
6. Process every message in a delivered batch before acknowledging it. Persist processed message IDs, exact-attempt completion and resource disposition before `check --ack`. A crash between processing and acknowledgement must replay idempotently. Accept worker completion only for its authoritative Task+Dispatch; a stale retry's success cannot settle the current attempt. An empty check/heartbeat is not completion. [E3, E4]

**Prompts:** the controller has no approve/reply-to-permission/accept-update path. It records `blocked: permission-required`, preserves exact operation and scope, checkpoints if possible, and presents the existing human workflow on return. An update prompt is also a blocker; do not accept 0.161.0 to get past it. Claude's advertised permission flags and Codex's approval controls are not authorization to change them. Existing settings remain in force; a resumed session must not gain wider sandbox, permissions or executable allowances. [E2, E7, E8, E11, E15]

Merges (including exact-SHA approval), pushes to main, credential use, external messages, and source-scope changes stay human-gated. This package additionally prohibits **all pushes and PR creation**. A future controller must only call narrow allowlisted operations on approved package IDs; it must not execute shell commands supplied by telemetry or arbitrary next-action strings. Validate a returned recovery argv against the allowed verb, exact IDs and scope before using it. Orca gates/CI green state are not owner approval, and a new PR head invalidates earlier exact-SHA approval. [E15; current task]

## Failure modes and required validation

| Failure | Required result |
|---|---|
| Quota source absent, stale, malformed, mismatched account, missing applicable window or permission | `blocked`, no dispatch, preserve prior evidence without treating it as fresh |
| Next section + outstanding work + checkpoint could meet/exceed any ceiling | Checkpoint before further dispatch, then sleep; larger reserve always wins |
| Short window resets but weekly/model/spend constraint persists | Continue waiting; do not substitute a model or paid credits |
| Claude drops an expired window or no event arrives while idle | UNKNOWN, no auto-resume and no measurement inference call |
| Lost start response or controller crash before journaling receipt | Reconcile request identity and runtime effects; never create another logical Task |
| Missing heartbeat, sleep, network loss, `restored_unconfirmed` | Treat as unverifiable, preserve locks/reservations, inspect; no inferred exit |
| Coordinator fenced / Run rebound / caller identity changed | Block mutations; no `--from` impersonation or blind takeover |
| Permission, update, workspace trust or credential prompt | Block that operation; no automatic prompt approval or settings edit |
| Unknown dirty files or overlapping implementation writer | Block affected task; preserve files; no reset/delete cleanup |
| Disk full, failed fsync/transaction, incompatible state/schema, clock jump | Stop admission; preserve recoverable state and require fresh evidence |
| Controller disabled mid-operation | Issue no further mutations; reconcile any already-accepted operation manually |

### UNKNOWN register: exact checks that would settle activation gaps

These are future tests, **not authorization to perform them now**. Event tests require a disposable Run/workspace with no production writer and explicit owner permission to restart/sleep/reboot; provider reads must be separately authorized to use existing managed authentication, without exposing it.

| ID | UNKNOWN | Exact settling check |
|---|---|---|
| U1 | App restart persistence and terminal/agent survival | In a disposable Run record `run-show`, `task-list`, `dispatch-show`, `worker-list`, exact `worker-show`, non-consuming mailbox views, terminal identity and Git status/HEAD; leave an unacknowledged delivery and question; restart Orca once with owner approval; compare IDs, generations, process incarnation, proven agent liveness and replay/ack behavior before any restart/retry mutation. Test terminal and structured worker modes separately if both will be supported. |
| U2 | Sleep/wake liveness, timers and automation grace | In the same isolated harness record before-state and one approved harmless scheduled run; sleep across a known deadline, wake, enumerate/reconcile, and inspect `automations runs --id <id> --json` for skipped/caught-up/duplicate behavior. Test beyond and within the configured grace window. |
| U3 | Reboot/login recovery and service startup | Approve a disposable controller pilot and Run; checkpoint, reboot once, log into the intended user session, repeat U1 comparisons, and verify controller startup, retained queue, absent/present processes, blocked prompts and exactly one recovery attempt. Test app-open and app-closed cases separately. |
| U4 | Current-Run orphan/rebind semantics; reported `consumer_fenced` | In a disposable current Run, bind coordinator A, retain a worker and pending Delivery, positively end A, then from a real authenticated coordinator B inspect `run-current/run-show` and attempt the documented `run-use --id <id> --json`; capture success/error, old/new generations, inbox replay, worker continuity and mutation authority. Do not use `--takeover-legacy` as a substitute. Also test a refused second coordinator while A remains live, without starting an editor. |
| U5 | Actual Codex account buckets, admission permission and idle freshness | With separate authorization, start only the documented stdio app-server, complete `initialize`/`initialized`, issue exactly one `account/rateLimits/read` request (no thread/turn creation), inspect selected schema fields/account identity and close the owned process. At a naturally occurring reset, repeat one read to establish successor-window and `ordinaryUsageAllowed` semantics; never consume a reset credit. |
| U6 | Claude's actual complete quota payload and fresh idle-reset source | With owner approval for a non-mutating bridge configuration, capture selected stdin fields on the next already-authorized normal response, with receipt time; do not generate a measurement call. Leave the session idle across a naturally occurring reset and inspect whether a new payload is independently refreshed. If it is absent/dropped/stale, obtain a tool-documented standalone read or keep auto-resume blocked. Establish any additional applicable/model/spend windows and pool identity explicitly. |
| U7 | Initial request-ID control and mutation idempotency across caller identities | First establish from tool documentation/schema whether an initial mutation can carry a caller-selected request ID, or emits its tool-issued ID before a response can be lost. In a disposable Run perform one harmless approved mutation, capture its actual ID, lose only the client response, restart that client, run `request-show` and exact `--retry-request`, then compare Task/Dispatch/message counts. Repeat across runtime restart and separately lose the response before any request ID is known; the latter must reconcile a known Task or block. Test pending/absent receipts without treating absence as permission to duplicate. |
| U8 | Hard percentage enforcement, task-cost bounds and shared consumers | Define owner-approved account/consumer/window mappings and per-section/checkpoint upper bounds in the same units; test concurrent admitted and external consumption, sample lag, rounding and overrun with synthetic telemetry first. If bounds or control cannot be established, explicitly approve only conservative admission, not a hard ceiling promise. No model load test is allowed. |
| U9 | Permission parity after resume and stop/checkpoint handshake | In an isolated offline adapter test inject a blocked tool/permission/update prompt, lost checkpoint acknowledgement, stale completion and changed policy/input SHA; prove zero approval responses, zero forbidden operations, no duplicate writer and no admission before durable checkpoint reconciliation. Then review the exact future runtime launch arguments against existing settings without changing them. |

### Test plan before any implementation is activated

Start with a pure decision function plus journal tests: standard library, synthetic or reviewed recorded quota fixtures and an injected clock, no network and no executable provider/Orca adapter in unit tests. Required cases: greater-of reserve for both pools; all applicable windows; equality; next-day/review cost larger than percentage reserve; null/missing/malformed usage/reset/account/permission; unknown estimates; in-flight reservations; checkpoint requested before dispatch; checkpoint acknowledgement required; no timer-only resume; fresh successor window required; short reset with weekly restriction; Claude missing-at-reset; clock jumps; restarted controller skips running/completed/uncertain attempts; transactional intent before side effect; receipt replay/absence; stale Dispatch completion; lock contention; disabled-controller checks; and a closed allowlist excluding prompt approval, credential operations, merges, pushes and external messages.

Use fault injection at every journal/dispatch/ack boundary. Test a crash after accepted mutation but before local receipt, and a crash after completion processing but before mailbox acknowledgement. Distinguish logical at-most-one admission from proof of no duplicate external effect. Then perform U1–U9 in an owner-approved pilot, have Claude independently review the final implementation, and obtain explicit activation approval. No test should use model calls to discover allowance. If code is later added, run its offline tests and the existing Node suite once without editing that suite. [Workflow: E15]

## Rollback and owner decisions

Proposed one-step return to today's manual admission is:

```sh
touch "$HOME/Library/Application Support/Ohvernight/autonomy/DISABLED"
```

This is a future contract: the state directory must already exist from approved activation, and every controller entry, admission and mutation must consult this sentinel. Setting it prevents automatic dispatch/retry/rebind/ack/cleanup; preserve journal and checkpoints for manual Orca reconciliation. It does not kill or undo a worker/operation already accepted, erase worktrees, change provider settings, or remove human authority. A later approved service can remain inert until separately unloaded; removing the sentinel must require a new explicit activation decision. No rollback command or runtime installation is executed here because nothing has been activated.

| Owner decision before activation | Recommendation |
|---|---|
| Whether to build and activate a runtime at all | Approve a separate observer-only specification first; retain manual dispatch until U1–U9 and independent review pass. This assessment grants no activation. |
| 90% desired ceiling versus current reserves | Keep `min(90%, 100% - current greater-of reserve)` per window; do not relax `capacity-routing.md` through configuration. Any reserve-policy change needs explicit approval. |
| Exact account/pool membership, applicable windows, next-day build/review estimates and margins | Record verified shared consumers, per-window denominators and bounded costs; unknown input blocks that pool. Never infer Hermes separation from its model name. |
| Hard ceiling guarantee versus conservative admission | Accept only conservative admission until bounded cost, lag and competing consumers are controlled; do not market an estimate as enforcement. |
| Permission to use authenticated read-only telemetry and a Claude bridge | Approve only the documented quota reads and minimal local selected-field bridge, under existing managed auth; no credential extraction, private endpoints, credit redemption or measurement inference. Do not change configuration during this assessment. |
| Host lifecycle and service choice | Pilot a manually started user process, then a single user LaunchAgent if warranted; no root daemon, sleep inhibition, paid host or headless Orca service by implication. Explicitly choose intended logged-in/app-open availability. |
| Coordinator replacement and recovery authority | Keep current-Run auto-takeover disabled pending U4; require positive exclusivity, preserved workers/mail and original package authority before a future approved replacement. |
| Allowed queue/actions, retries, locks and freshness | Limit to explicitly approved bounded sections; one controller and conservative pool concurrency; preserve Orca's circuit breaker; choose TTL/backoff/checkpoint deadlines as policy values, never guessed provider limits. |
| Restart/sleep/reboot pilot and data retention | Approve isolated lifecycle tests separately, minimal user-private state and retention/backup policy; no published transcripts or credential-bearing dumps. |
| Kill switch, permission prompts and protected actions | Approve the one-step disable contract; prompts remain blocked for human action. Preserve exact-SHA merges, main pushes, credential use, external messages and source-scope changes as human gates. |

## Validation and handoff

This is a documentation-only assessment; no prototype or runtime adapter was added. Evidence gathering used local help, generated schemas, selected existing local state, repository contracts and the linked official documentation. Event recovery, authenticated quota refresh, configuration changes, startup integration and permission handling were deliberately not exercised; the UNKNOWN register gives the exact follow-up tests.

Validation performed: `node --test v2/pipeline/tests/*.test.cjs` ran once, with **133 passed, 0 failed, 0 skipped**; its output is in the temporary local file `/private/tmp/autonomy-feasibility-node-tests.log`. No suite was edited. Whitespace, cited repository paths and the staged one-file diff are checked before the local commit. Python/browser suites were not run for this documentation-only change; GitHub CI and Claude independent review remain pending. No push, PR, merge, scheduling or activation is authorized by this deliverable.
