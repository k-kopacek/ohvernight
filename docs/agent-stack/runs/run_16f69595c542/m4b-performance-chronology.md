# M4-B performance: definitive chronology

Coordinator, 2026-10-20, at the owner's direction. Records reconciled against raw artifacts; nothing rerun, nothing discarded. **Verdict: the applicable acceptance set has not met the M4 performance gate. The gate is not passed, and nothing in this file claims otherwise.**

## Constants for every session

| Item | Value | How it was verified |
|---|---|---|
| Measured head | `06d642597609ab7da88cb2c5a780ef63b74a9039` (PR #17 head) | `headCommit` in every `session-*.json` |
| Same-session base | `3dc0fef` | `baseCommit` in every `session-*.json` |
| Benchmark script | `v2/pipeline/tests/browser/measure.mjs`, blob `40869bf88072edfaa6a198276f9655811a273adb`, last changed `3cca3f4` on 2026-10-05 | `git rev-parse 06d6425:…` equals the on-disk `hash-object`; there is no uncommitted change |
| Chrome / Node | Chrome 154.0.8037.95 / Node v24.21.0 | session JSON |
| Method | 4× CPU throttle, 390×844, cold cache. Five base Aspen, five base Douglas, five head Aspen, then five head Douglas runs, back to back | session JSON |
| Acceptance rule | M4 §14 and M3 §16.4/A10. Limits as a share of the same-session base: map usable ≤ 60%, default layers ≤ 135%, heaviest toggle ≤ 125%, heap ≤ 115%. Longest task ≤ 50% of the same-session Aspen base. Three sessions | mission briefs and the harness `thresholds` |

Raw artifacts are untracked under `m4b-functional-water/docs/research/engineering/`.

## Chronology (all 2026-10-13; local time MDT, UTC−6)

| Time | Event | Set | Douglas map usable (head / base median, ms; share of base) | Douglas default layers (ms; share of base) | Result | Machine state |
|---|---|---|---|---|---|---|
| 11:03–11:05 | Session 1 | **First set** (integration mission) | 1,039 / 1,632; 63.7% | 2,304 / 1,632; 141.2% | **MISS ×2** | Start load 5.25 (15-min average 14.61), with no load gate. The coordinator confirmed that another reviewer's browser harness and suites were running |
| 11:07–11:19 | Load gate | First set | — | — | — | Waited 720 s, until the 1-minute load fell below 4.0 |
| 11:19–11:20 | Session 2 | First set | 544 / 1,319; 41.3% | 1,442 / 1,319; 109.3% | PASS (all metrics, both regions) | Start load 3.39. No end reading was recorded |
| 11:21–11:23 | Session 3 | First set | 560 / 1,292; 43.4% | 1,394 / 1,292; 108.0% | PASS (all metrics, both regions) | Start load 3.88. No end reading was recorded |
| 11:26 | Integration status report | First set | — | — | "sessions 2 and 3 pass; session 1 misses under competing load; owner disposition required; no blanket pass claimed" | — |
| after 11:26, before 11:37 | **Owner decision, option 2** | — | — | — | The owner neither accepted nor rejected the first set. A **new, separate set of three** became the acceptance set, with a stop rule: stop at the first miss | `.missions/codex-m4b-clean-performance.md` |
| 11:39–11:41 | Session 1 | **Clean set (the acceptance set)** | 911 / 1,449; 62.9% | 1,997 / 1,449; 137.8% | **MISS ×2** | Load gate passed at once: 3.90, with no project test processes. End load 9.30. Nothing else was observed during the run, but nothing was monitoring continuously |
| 11:41 | Stop rule applied | Clean set | — | — | Sessions 2 and 3 were never run | `stop.json` |
| 11:43 | Clean-set report | Clean set | — | — | "does not meet the existing rules … not a waiver or acceptance decision" | `.missions/m4b-clean-performance-report.md` |

Raw Douglas head samples, five runs each, in ms:

| Session | Map usable | Default layers |
|---|---|---|
| First set, session 1 | 771, 1,039, 816, 2,042, 1,989 | 1,652, 2,304, 1,762, 3,671, 3,387 |
| First set, session 2 | 590, 547, 529, 544, 541 | 1,501, 1,442, 1,338, 1,359, 1,465 |
| First set, session 3 | 555, 523, 560, 632, 565 | 1,394, 1,326, 1,342, 1,464, 1,482 |
| Clean set, session 1 | 734, 961, 911, 945, 760 | 2,002, 1,933, 2,003, 1,997, 1,585 |

## Where the contradiction came from

**No record claims three quiet passing sessions.** Two reports said "three sessions", and both meant the first set:

1. Codex's integration status report at 11:26.
2. The coordinator's final-review report of 2026-10-19: "three sessions ran. Sessions 2 and 3 passed every metric. Session 1 missed two Douglas limits under other load". The coordinator's PR #17 description of 2026-10-19 said the same.

Both are accurate about the first set. **The coordinator's 2026-10-19 report and PR description were wrong to stop there.** They omitted that the owner had replaced the first set with the clean set, and that the clean set's session 1 missed. That omission is the coordinator's error. It was corrected in the PR #17 description later on 2026-10-19.

A second source of confusion is the M4-A merge packet (`docs/research/m4-water/decision-packets/m4a-merge.md`). It says "an interleaved comparison on a quiet machine … all six sessions pass". That was M4-A, at a different head, and it does not apply to M4-B.

## Which set governs

By the owner's option-2 decision of 2026-10-13, the **clean set** is the acceptance set, and the first set is history. The clean set stopped at a miss, so **M4-B performance acceptance is not met.**

The following are facts only, with no conclusion drawn from them:

- In the clean session the head was about 1.7 times slower in map usable (911 against 544–560 ms) than in first-set sessions 2 and 3, at the same code and with a similar base.
- Load had risen from 3.90 to 9.30 by the end of the clean session.
- The load gate checks only the start of a session.
- The 2026-10-07 measurement note found the Douglas default-layers ratio at 124–131% on `main` itself on a quiet machine, so the margin under 135% is thin before any M4 change.

## What is not done

- No rerun, which the owner forbade.
- No tuning.
- No change to a threshold or the method.
- Neither record is discarded.

## Owner options (the owner's authority only)

- **(a)** Accept the merge with this record as a recorded miss. Exact-head approval would then state that.
- **(b)** Order a fresh acceptance set under a protocol fixed **before** it runs, for example the 2026-10-07 note's interleaved main/branch comparison with continuous load sampling. The clean-set miss stays on the record, and the new set is judged by its own pre-declared rule, not chosen because the earlier result was inconvenient.
- **(c)** Amend the performance gate's form, for example to a same-sitting comparison with `main`, as the 2026-10-07 note suggested. This is a specification change.

The coordinator does not recommend among these; performance acceptance is the owner's.
