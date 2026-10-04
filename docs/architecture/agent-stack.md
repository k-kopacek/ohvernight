# Agent stack

The permanent division of responsibility between the human owner, the agents
and the tools that build Ohvernight. Settled decisions behind it are recorded
in [decisions/](decisions/). Repository working rules are in
[AGENTS.md](../../AGENTS.md).

## Roles

| Participant | Role | Responsibilities | Explicitly not |
|---|---|---|---|
| **Human owner** | Product owner | Product intent; approval of major architecture; approval of specifications; merge authority (approves each merge) | — |
| **GitHub** | Institutional memory | Durable source of truth for code, data, specifications, roadmap, principles and decisions | — |
| **Orca** | Execution plane | Worktrees, agent sessions, orchestration, messaging, decision gates | Not a record of decisions; its run state is operational, not authoritative |
| **Claude** | Technical lead | Architect; milestone coordinator; specification owner; independent reviewer | Does not modify the implementation during review; never merges autonomously |
| **Codex** | Primary implementation engineer | Coding; tests; debugging; scoped refactoring; PR preparation | Does not change approved scope; never merges autonomously |
| **Hermes** (from M4) | Research / operations | External research; source and API monitoring; licensing and terms monitoring; freshness and source-health monitoring; recurring operational reporting | Not the primary coder; not an architecture authority; not a merge authority |
| **CI** | Quality gate | Objective, automated check of tests and contract invariants on every pull request | Not a substitute for review |
| **ChatGPT** | Advisor | Product, strategy and research advice | Not a required hop in the build loop |

Hermes is not part of the stack before M4. See
[ADR-004](decisions/ADR-004-hermes-research-operations-role.md).

## Standard engineering workflow

```text
Product direction
  → Claude specification
  → human approval
  → Claude as Orca coordinator
  → Codex implementation
  → Claude review
  → Codex fixes, if required
  → CI
  → human approval
  → agent or human merge
```

1. **Product direction.** The human owner states intent. The
   [roadmap](../../ROADMAP.md) fixes milestone order.
2. **Specification.** Claude writes the milestone specification in
   `docs/specs/`, grounded in verified repository facts.
3. **Human approval.** The owner approves the specification and resolves its
   listed decisions. Approved product decisions are not rewritten without a
   reason.
4. **Coordination.** Claude runs the milestone as an Orca coordinator and
   dispatches Codex.
5. **Implementation.** Codex implements on a feature branch or worktree based
   on `origin/main`, with tests, and prepares the pull request.
6. **Review.** Claude independently inspects the complete diff, repository
   state, tests, acceptance criteria, and mutation or negative tests where the
   specification requires them.
7. **Fix loop.** Findings go back to Codex with exact detail. Review repeats
   until approved.
8. **CI.** The pull request must be green.
9. **Human approval.** Claude reports the verdict and the reviewed head SHA;
   the owner decides.
10. **Agent or human merge.** The owner merges, or an agent merges after the
    owner's explicit approval of that pull request at that head SHA.

## Blockers and escalation

Ordinary technical blockers are resolved agent-to-agent. When Codex meets a
conflict with the approved specification, the data contract, repository
reality or a stop-and-report rule, it reports to the coordinator, who decides
whether it is:

- resolvable within the approved specification — the coordinator resolves it;
- a narrow specification amendment — the coordinator amends the specification
  narrowly, records the amendment in it, and re-instructs;
- a product decision — escalated to the human owner.

Human escalation is reserved for:

- product behavior changes
- trust/safety policy changes
- major architecture changes
- meaningful milestone scope expansion
- irreversible or destructive actions
- material ambiguity with multiple reasonable product outcomes

Test failures, implementation details, small clarifications and mechanical
corrections are not escalated.

## Merge authority

**Agents may merge to `main` only after explicit human approval for that
specific pull request and reviewed head SHA.** Merging to `main` is a
production deploy (GitHub Pages publishes the repository from `main`), and
the decision is the owner's alone.

- Agents must never merge autonomously.
- Human approval must be explicit and specific to one pull request.
- Approval applies to the reviewed head SHA. If the pull request's head
  changes after approval, human approval is required again.
- Agents may not enable auto-merge unless explicitly authorized.
- Agents may not push directly to `main`.
- Agents may not force-push or rewrite shared history.

Agents may commit to feature branches, push them and open pull requests. See
[ADR-002](decisions/ADR-002-human-approved-merge-authority.md).

## Memory and authority

Agent memory, chat history and Orca session state are conveniences. When they
disagree with the repository, the repository is right. Anything that must
survive a session is written to the repository through a pull request. See
[ADR-001](decisions/ADR-001-repository-is-source-of-truth.md).
