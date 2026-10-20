# Ohvernight roles and authority

Read [master-coordinator.md](master-coordinator.md) as the canonical operating contract. These boundaries apply to independent workers as well as supervised sessions.

| Participant | Responsibilities and decisions | Write boundary | Merge boundary |
|---|---|---|---|
| Human owner | Product, trust policy, material architecture, milestone scope, specification approval, source-use decisions and exact-SHA merge approval | May authorize changes across the repo; changes remain attributable in Git | Default merge executor; may explicitly delegate one PR merge at its reviewed exact SHA |
| Claude | Control plane: coordinator, architect, technical lead, spec owner, independent reviewer, synthesizer, owner-decision packet author; resolves routine engineering conflicts within approved scope | Assigned specs, architecture/decision drafts, review findings, research synthesis and coordinator-owned run records; never silently edits production implementation while reviewing | Cannot approve its own merge authority or merge autonomously; only an explicitly delegated exact-SHA operation |
| Codex | Implementation and technical compute: production engineering, tests, prototypes, data analysis, dry runs, audits and performance work; chooses routine implementation details inside approved bounds | One assigned production surface at a time after approved spec/package; technical research/prototypes in an isolated allowlist; no unrelated data or policy edits | No autonomous merge; worker handoff is normally the endpoint, with any merge operation separately delegated by owner |
| Hermes | Research/evidence/market/product opportunity plane; independently advances long-lived missions; proposes evidence-backed opportunities and source interpretations | Production read-only. Assigned research documents/checkpoints only when file access is granted; otherwise outputs go to a designated custodian. No production code, canonical data, runtime schemas/config or dependencies | No merge authority; cannot publish claims or treat a recommendation as owner approval |
| Orca | Orchestration/execution plane: sessions, worktrees, messages, dependencies and operational gates | Manages authorized execution state; does not grant agents new write or decision powers | Never supplies human approval; must not configure autonomous merge |
| Git / GitHub | Institutional source of truth: attributable code/data, specs, approved decisions, branches, exact PR heads, review and CI evidence | Stores work through authorized branches/PRs; unmerged proposals remain proposals | Records merge evidence; a permissive repository setting is not owner authorization |
| CI | Objective gate: executes required automated checks against identified code | Test artifacts/check results; any generated artifact must follow publication rules | Green CI is necessary, not owner approval; pending/unavailable checks are not success |

## Decision ownership

- Claude drafts specs and material architecture options; the owner approves them. Codex implements the approved contract; Claude independently reviews it; Codex fixes findings; GitHub CI checks the final head; the owner approves the exact-SHA merge.
- Workers may resolve bounded implementation/research details, choose reproducible methods, create negative tests and advance to the next authorized section without asking Claude between sections.
- Hermes may interpret evidence for a draft dossier, but cannot establish production confirmation, permission, trust policy or legal reuse clearance. Claude re-reads claim-bearing sources; the owner approves production records as required by M4.
- Codex may demonstrate that a rule fails on real data, but cannot relax the rule, change acceptance thresholds or widen a fetch to make it pass.
- A recommendation is not a decision. Silence, capacity exhaustion and schedule pressure never unlock owner gates.

## File ownership and independent review

Every dispatch names a base SHA, branch/worktree, write allowlist and artifact directory. Worktrees isolate files, not model usage. Only one production implementation authority edits overlapping files at a time. Independent research workers use separate subdirectories; the coordinator integrates the shared queue and summaries. Workers must not overwrite another checkpoint or stage unrelated changes.

Claude's spec authorship does not prevent independent review of Codex's implementation; the reviewer must inspect the actual diff, evidence and final SHA instead of trusting worker conclusions. Codex self-tests and Hermes confidence labels never substitute for that review. Any reviewer-authored implementation change returns through Codex validation and a fresh review of the new head.

## Operations and gates

Use the authorization in the session/package for edit, commit, push/PR, live refresh and merge; one does not automatically authorize the next. No agent may autonomously merge, enable auto-merge, push directly to main, force-push or rewrite shared history. The full exact-SHA policy is in [master-coordinator.md](master-coordinator.md).

Owner gates are local locks. A blocked merge, disputed source interpretation or gated feature does not stop independent authorized research/preparation. Future M5–M8 work stays read-only relative to production. Customer interviews, email, agency outreach, paid services and public posting require explicit owner authorization before external contact or spend; draft artifacts can proceed.
