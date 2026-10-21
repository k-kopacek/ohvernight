# 15 — Proposed one-time owner autonomy authorization record

**UNSIGNED / PROPOSED.** This is a template for an explicit, attributable owner decision, not authorization by mere presence. The owner must review the actual document/PR and approve its exact head, then amend the relevant existing contracts/ADRs through the authorized workflow. Until that happens, existing per-PR merge, M5–M8 future-scope and device gates remain binding.

## Intended bounded grant

> The owner authorizes the Ohvernight coordinator, acting through Orca, Claude, Codex and approved research workers, to pursue the Colorado-first target defined in this charter through M4 completion and M5–M8, using verified evidence sources and existing trust principles. It may choose routine implementation details; write bounded specs consistent with the target; dispatch and independently review technical tasks; run tests and open pull requests; and continue selecting authorized work after progress reports without further owner prompts. It may not expand the target, weaken evidence/trust requirements, change protected licensing/security/privacy posture, spend money, contact external parties or use paused Qwen/Odysseus infrastructure without further owner authorization.

The charter is intended to reduce owner interruptions, not to delegate legal review or approve unsupported permission claims. A milestone with required human/source confirmation remains locally gated; other permitted tasks continue.

## Independent authority choices — MUST BE EXPLICIT

### A. Product/scope authorization

`STATUS: NOT YET ADOPTED`

If adopted: the coordinator may produce bounded M5–M8 specs and implement them consistently with the approved target **after the governance documents are amended to permit this**. It must still stop for changes to the target, trust principles, original source-use policy, material unapproved source family or a contract contradiction.

### B. Production merge authority

`STATUS: NOT DELEGATED`

Choose explicitly at adoption time:

- **Conservative:** autonomous development through reviewed PR; the owner approves each exact-SHA merge.
- **Delegated:** a separately approved and enforced policy permits only explicitly scoped low-risk automatic merges meeting all gates in `10-review-merge-and-escalation.md` and amended ADR/AGENTS. Any unverified gate or changed PR SHA fails closed. Deployment is not assumed to have gone well until post-merge health checks pass.

A broad phrase “full autonomy” alone is not a safe machine-verifiable GitHub merge delegation. Record the chosen mode, effective governance commit SHA, allowed repositories, excluded files/actions, rollback operator, duration and revocation method.

### C. Real-device/UX release gate

`STATUS: EXISTING OWNER GATE RETAINED`

Replace a required owner iPhone check only if the owner separately approves a credible real Safari/device acceptance process. A Chrome viewport regression suite alone is insufficient.

### D. Runtime and usage monitoring

`STATUS: NOT INSTALLED / NOT VERIFIED`

Approve a separate implementation and installation of a minimally privileged persistent supervisor only after capability discovery, quota probe validation, restart/fail-closed tests and rollback are reviewed. Set account-pool reserve targets explicitly. The 90%-used ceiling is mandatory as an outer cap; whether to retain earlier 15%/25% reserves requires a deliberate owner policy choice.

## Revocation

Owner `STOP` means no new dispatch, no merge/deploy, no auto-resume after reset. Save a checkpoint and list any already-running safe actions that still need a termination or cleanup decision. A later `RESUME` must re-verify current policy SHA, Git state, quotas and worker status. Never infer RESUME from elapsed time.

## Final owner critique

When release acceptance is satisfied, stop expanding the scope and hand the user a usable Colorado build with test/source/coverage and scenario evidence for critique. If protected gates are unresolved, report the closest safe candidate and exactly what cannot legally/technically ship, rather than marking completion.
