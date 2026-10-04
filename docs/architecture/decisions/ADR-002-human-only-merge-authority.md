# ADR-002: Human-only merge authority

## Status

Accepted. Recorded 2026-10-04. In practice since M1.

## Context

GitHub Pages publishes the whole repository from `main`, so merging to `main`
is a production deploy. The product makes trust-sensitive statements about
land, access and camping. Agents write and review most of the changes.

## Decision

Only the human owner merges to `main`. Agents may commit to feature branches,
push them and prepare pull requests. No agent may merge to `main`, push to
`main`, enable auto-merge, force-push or rewrite shared history.

## Consequences

- Every production change passes a human decision, after agent review and CI.
- A coordinator's final output is a verdict and a report, never a merge.
- A pull request waits for the owner even when it is approved and green.
- At the time of writing, `main` has no GitHub branch protection, so this rule
  is held by convention and agent instruction, not by the platform. Enabling
  protection that requires the `python` and `node` checks is an owner
  follow-up noted in the M1 specification.
