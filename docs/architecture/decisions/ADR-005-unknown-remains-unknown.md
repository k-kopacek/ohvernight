# ADR-005: Unknown remains unknown — no positive trust claim without evidence

## Status

Accepted. Recorded 2026-10-04. Enforced for published data since M2.

## Context

Ohvernight shows land management, roads, trails, water, facilities and
camping options. Users may act on what they see in ways that carry legal and
safety consequences. The data is generalized, partial and often old. The
audit found paths where the product could imply more than the data supports:
non-federal land read as private, a listing read as permission, a fetch read
as a confirmation, and staleness hiding a restriction.

## Decision

Unknown is the default and is never resolved by inference. A positive claim
of permission, access, openness or support requires complete, reviewed
evidence and otherwise fails closed to unknown. Staleness may reduce
confidence but never weakens or suppresses a known restriction. Presentation
must not communicate more certainty than the evidence supports.

The rules are stated in
[trust-principles.md](../../product/trust-principles.md) and, normatively for
data, in the
[regional data contract](../../../v2/pipeline/docs/data-contract.md).

## Consequences

- The product will often say "unknown" where a user wants an answer. That is
  intended.
- The manifest schema cannot express a complete, verified or permitted
  region; there is no such state.
- Allowed value sets are not widened to make data pass. Data that violates
  the contract is reported and recorded in the non-conformance register.
- New layers, sources and regions must declare what they do not establish.
- Changing this decision is a trust/safety policy change and requires the
  human owner.
