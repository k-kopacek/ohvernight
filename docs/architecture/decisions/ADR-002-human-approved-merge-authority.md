# ADR-002: Human-approved merge authority

## Status

Accepted. Recorded 2026-10-04.

## Context

GitHub Pages publishes the whole repository from `main`, so merging to `main`
is a production deploy. The product makes trust-sensitive statements about
land, access and camping. Agents write and review most of the changes, and
can also perform the mechanical act of merging.

## Decision

Merge authority belongs to the human owner. Agents may merge to `main` only
after explicit human approval for that specific pull request and reviewed head
SHA.

- Agents must never merge autonomously.
- Human approval must be explicit and specific to one pull request. A general
  or earlier go-ahead, or approval of a different pull request, is not
  approval.
- Approval applies to the reviewed head SHA. If the pull request's head
  changes after approval, human approval is required again.
- Agents may not enable auto-merge unless explicitly authorized.
- Agents may not push directly to `main`.
- Agents may not force-push or rewrite shared history.

The owner may also merge personally.

## Consequences

- Every production change passes a human decision, after agent review and CI.
- A coordinator's final output is a verdict and a report naming the head SHA.
  It merges only if the owner then approves that pull request at that SHA.
- Before merging, an agent confirms the pull request's current head still
  equals the approved SHA. If it does not, the agent stops and asks again.
- A pull request waits for the owner even when it is reviewed and green.
- At the time of writing, `main` has no GitHub branch protection, so this rule
  is held by convention and agent instruction, not by the platform. Enabling
  protection that requires the `python` and `node` checks is an owner
  follow-up noted in the M1 specification.
