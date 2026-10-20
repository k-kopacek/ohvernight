# ADR-004: Hermes joins in M4 as research/operations, not build authority

## Status

Accepted. Recorded 2026-10-04. Takes effect at the start of M4.

## Context

From M4 onward the milestones depend on external facts that change: source
and API availability, licensing and terms (for example COTREX in M6), data
freshness and source health. Watching these is recurring operational work,
distinct from specifying or implementing a change.

## Decision

Hermes joins the agent stack beginning with M4 in a research and operations
role: external research, source and API monitoring, licensing and terms
monitoring, freshness and source-health monitoring, and recurring operational
reporting. Hermes is not the primary coder, not an architecture authority and
not a merge authority.

## Consequences

- Hermes is not part of the stack for M3.
- Hermes's findings are inputs. They become project facts only when recorded
  in the repository through the normal workflow.
- A Hermes report does not verify anything in the trust sense: a successful
  check of a source is retrieval, not confirmation
  ([ADR-005](ADR-005-unknown-remains-unknown.md)).
- Implementation stays with Codex and architecture with Claude
  ([ADR-003](ADR-003-claude-coordinates-codex-implements.md)).
- How Hermes is run and where its reports are stored is not decided here.
