# ADR-003: Claude coordinates, Codex implements

## Status

Accepted. Recorded 2026-10-04. Used for M1 and M2.

## Context

If one agent specifies, implements and reviews the same change, review is not
independent. M1 and M2 were delivered with the roles split, and M2's two
review rounds returned findings that were fixed before merge.

## Decision

Claude is the technical lead: architect, specification owner, milestone
coordinator and independent reviewer. Codex is the primary implementation
engineer: coding, tests, debugging, scoped refactoring and pull-request
preparation. Claude does not modify Codex's implementation during review;
findings go back to Codex to fix.

## Consequences

- The author of a change is never its only reviewer.
- Specifications must be precise enough to implement and to review against,
  with acceptance criteria and, where needed, mutation or negative tests.
- Ordinary blockers are resolved between the two agents; only the cases
  listed in [agent-stack.md](../agent-stack.md) go to the owner.
- Fixes cost a round trip through the coordinator instead of a direct edit.
  That cost is accepted to keep review independent.
- Neither agent merges autonomously
  ([ADR-002](ADR-002-human-approved-merge-authority.md)).
