# Performance measurement note

Written after the M4-A review, where two of nine performance sessions on the
M4-A branch missed the Douglas "all default-on layers" limit and a direct
comparison then showed `main` and M4-A to be indistinguishable. It records
what happened and proposes how to measure from M4-B on. It changes no
threshold and no method; any change to either is the owner's.

## What was measured

Unchanged `measure.mjs`; limit for Douglas "all default-on layers drawn":
135% of the same-session base.

| Run set | Session 1 | Session 2 | Session 3 | Other activity on the machine |
|---|---|---|---|---|
| M4-A checkpoint | 117.4% | 126.1% | 144.1% | The implementer's own full browser check overlapped session 3 |
| M4-A final, first set | 123.0% | 163.6% | 131.2% | A git worktree checkout (about 30 MB) during session 2 |
| M4-A final, interleaved, quiet | 119.8% | 134.3% | 119.7% | None |
| `main`, interleaved, quiet | 130.7% | 127.4% | 124.4% | None |

Absolute Douglas times in the quiet interleaved run: `main` 1,661 / 1,667 /
1,742 ms; M4-A 1,620 / 1,682 / 1,765 ms. The same-session base varied from
1,252 to 1,474 ms.

## What this shows

1. The measurement is sensitive to anything else running. Both misses
   coincided with other work, one of them started by the coordinator.
2. Even on a quiet machine a session can land at 134.3% against 135%. The
   ratio moves several points because the base moves: the session at 134.3%
   had the lowest base (1,252 ms).
3. On `main` itself the ratio sits between 124% and 131%. The margin under
   the limit is thin before any M4 change.
4. A three-session rule with a 135% limit will produce occasional misses that
   reflect noise, not a regression. The A11 miss in M3 (136.5%) had the same
   character.

## Proposed protocol for M4-B (coordinator practice; no threshold change)

- Run performance sessions on a machine with nothing else running: no agent,
  no browser check, no git operation, no build. State that in the report.
- Measure the branch and `main` interleaved (main, branch, main, branch,
  main, branch) in one sitting, and report both, with absolute times as well
  as ratios.
- Judge a regression by the comparison between the branch and `main` in the
  same sitting, in addition to the A10 limits.
- Record every session, including any that miss, with what else was running.
- A miss is still reported and never tuned around.

## For the owner, when convenient

M4-B is expected to make Douglas faster: the grouped water display is
projected to be about half the bytes and a small fraction of the features.
That is the right time to look at whether the 135% limit, measured against a
base that itself varies by 15%, is the best form for this check, or whether a
comparison with `main` in the same sitting should be the gate. No change is
proposed now.
