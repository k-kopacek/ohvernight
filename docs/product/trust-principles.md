# Trust principles

**This document is normative.** It states the trust rules every milestone,
specification, agent and reviewer must hold to. The machine-checked form of
these rules for published data is the
[regional data contract](../../v2/pipeline/docs/data-contract.md). If the two
ever appear to disagree, the data contract governs for data and validation,
and the disagreement is a defect to fix by pull request.

Ohvernight publishes research context. It does not grant or confirm legal
access, camping permission, availability or current conditions.

## 1. Unknown remains unknown

A missing claim, a missing layer, an empty layer and an unavailable source all
mean unknown. None of them means private, closed, open, unrestricted or
permitted. Unknown is the default, and it is never resolved by inference.

## 2. Never infer

| Never infer | From |
|---|---|
| Private land | Land being non-federal, unshaded, or carrying an unrecognised agency code |
| Public access | Ownership or managing-agency classification |
| Camping permission | A facility or listing existing |
| Legal access | A mapped road or trail |
| Recreation permission | A mapped water feature |
| Fishing, paddling or swimming permission | A feature existing or having a name |
| Openness | The absence of a mapped closure |
| Verification | A successful retrieval |
| Current conditions | Historical data |

Proximity is not a connection. Straight-line distance to a road, trail,
facility, water feature or public land establishes nothing about access.

## 3. Keep these concepts separate

A value in one never implies a value in another.

Evidence concepts:

- **Existence** — a source lists the feature or facility.
- **Provenance** — where the record came from and when it was copied.
- **Transport / retrieval** — whether the last fetch attempt worked.
- **Interpretation** — what a reviewed source says about one fact for one
  place.
- **Verification** — whether a person reviewed that interpretation, how, and
  when.
- **Freshness** — whether that verification is still within policy. Computed,
  never stored.

Fact dimensions:

- **Ownership** (or managing-agency classification)
- **Public access**
- **Camping permission**
- **Recreation permission**
- **Restrictions and closures**
- **Road and trail access**

Existence is the weakest of these. A record with good provenance and a recent
successful fetch still says nothing about permission, access or current
status.

## 4. A fetch is not a confirmation

A successful retrieval or check advances only checked and retrieved
timestamps. Only manual review, or a structured source field the contract
names as validated, advances a confirmation, and only for that one fact. A
retrieval date is not the date the agency last revised the content.

## 5. Staleness never weakens a restriction

Stale evidence may reduce confidence. It must never weaken or suppress a known
restriction.

- A stale or never-confirmed supportive claim is treated as unknown.
- A stale or never-confirmed restriction, exclusion, limit or caution remains
  in force and is additionally flagged for review.
- Evaluation order must not let a staleness result pre-empt a known
  restriction.

## 6. Positive claims fail closed

Any value that asserts permission, access, openness or support requires
complete, reviewed evidence. If any required part is missing, the value is
unknown.

## 7. Presentation must not exceed the evidence

Presentation must not communicate greater certainty than the evidence
supports. This covers styling, colour, labels, wording, ordering and ranking.
Generalized or computed geometry must not be drawn or described as a surveyed,
parcel-level or legally precise boundary.

## 8. Language

No manifest, test or document describes a region, layer or place as verified,
complete, open, permitted or legal. Trust-bearing wording in manifests is
changed only with owner approval.

## Changing these principles

A change here is a trust/safety policy change. It requires human-owner
approval and a pull request; no agent may change it on its own authority. See
[ADR-005](../architecture/decisions/ADR-005-unknown-remains-unknown.md).
