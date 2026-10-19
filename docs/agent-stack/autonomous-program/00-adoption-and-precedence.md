# 00 — Adoption, authority and precedence

**Draft policy, not active until approved in Ohvernight.** The existence of this file grants no permissions.

## Governing precedence

1. Human owner instructions, **when explicit and attributable**; protected changes are then reconciled to the repository via approved PR/ADR.
2. `AGENTS.md`, accepted ADRs, `docs/product/trust-principles.md`, `v2/pipeline/docs/data-contract.md`, source-use/licensing requirements and approved milestone specifications.
3. `docs/agent-stack/master-coordinator.md`, `roles.md`, `capacity-routing.md`, `overnight-autonomy.md`, and other agent contracts.
4. This autonomous-program package after its adoption, insofar as it does not contradict higher authority.
5. Task packets, worker notes, live Orca status and model memory: informative but not independent authority.

If documents conflict, record the exact conflict in an owner gate. Do not quietly privilege a newer-looking document or a model's summary. A new charter cannot self-authorize a change to a governing ADR.

## Adoption decisions requiring explicit owner approval

1. **Target product:** Colorado-wide mobile Explore plus evidence-backed Choose Your Adventure, bounded by `01-target-product.md`.
2. **Implementation charter:** Coordinator may autonomously design draft specifications, research, dispatch bounded Codex packages, test, review, fix, prepare PRs and continue to the next authorized task **within already approved specifications**.
3. **Expansion of current milestone authority:** M5–M8 production work and multi-region Colorado implementation are presently owner-gated by the canonical agent/spec documents. To permit autonomous implementation after a single overall charter approval, expressly amend/supersede these gates via an owner-approved governance/spec PR, with measurable milestone contracts, without weakening trust or source-use policy.
4. **Merge delegation:** Current binding policy forbids standing auto-merge; a distinct, explicit owner-approved change would be required. See `10-review-merge-and-escalation.md`.
5. **Host runtime:** Approve installation/operation of a scheduler/usage-probe service and its local state location, restricted privileges and network access. This document alone does not run it.

## Non-negotiable retained constraints

Unknown remains unknown; ownership is not access; proximity is not a source-backed relationship; source retrieval is not verification; stale restrictions are not weakened; legal/access/permission claims fail closed; all trust-bearing publication is provenance-labeled. No privacy/credential exposure, force-push, destructive cleanup of raw data, or unapproved licensing reuse. No agent is a legal authority.

## Product autonomy versus production autonomy

**Development autonomy** means research/implementation/test/PR can proceed across many tasks within the approved scope without prompting the owner every step. **Production autonomy** means merges and deployment. These are separate grants. On GitHub Pages, merge to `main` publishes the site; do not conflate them.

Until adoption is completed, treat the package as a proposed plan only and follow the existing contracts. Do not start an unattended run from reading this document.
