# M4 research: functional recreational water

Research gathered before the M4 specification, so the reasoning behind the
source and schema decisions stays in the repository. Nothing here changes the
product. It is input to `docs/specs/` for M4, which the owner approves.

Access date for all external sources: 2026-10-06.

## How to read this

- **`hermes/`** holds the Hermes research reports verbatim. Hermes ran with
  web search and page reading only. A Hermes report is a research input; it
  does not verify anything in the trust sense
  ([ADR-004](../../architecture/decisions/ADR-004-hermes-research-operations-role.md),
  [ADR-005](../../architecture/decisions/ADR-005-unknown-remains-unknown.md)).
  Each claim in a report is marked RETRIEVED, INFERRED or UNKNOWN by Hermes.
- **The files in this directory** are the coordinator's synthesis. They say
  which claims were checked independently against the primary source, where
  the reports disagree with each other or with the repository, and what is
  still unknown.
- An unknown is written as unknown. A source being reachable is retrieval,
  not confirmation.

## Files

| File | What it answers |
|---|---|
| [existing-data-audit.md](existing-data-audit.md) | What water Ohvernight shows today, how much of it is clutter, and what the pipeline discards |
| [existing-data-audit-facts.md](existing-data-audit-facts.md) | The computed counts behind the audit, from `main` at `b45ca59` |
| [field-semantics.md](field-semantics.md) | Which source fields can separate useful water from clutter, with real counts for both regions |
| [source-matrix.md](source-matrix.md) | Candidate authoritative sources for geometry, identity and recreation information |
| [recreation-signals.md](recreation-signals.md) | Official recreation information and how it can be attached to a water feature |
| [community-signals.md](community-signals.md) | Community and review sources, and what their terms allow |
| [licensing-and-terms.md](licensing-and-terms.md) | Licence and terms findings and open questions, in one place |
| [recommendations.md](recommendations.md) | Proposed evidence hierarchy, source architecture, selection rule, PR breakdown and the owner decisions required |
| [nhd-selection-probe.md](nhd-selection-probe.md) | Read-only counts of what the proposed selection rule yields in each region |

## Research tracks

| Track | Subject | Run by | Report |
|---|---|---|---|
| A | Authoritative water sources | Hermes | [hermes/track-a-authoritative-water-sources.md](hermes/track-a-authoritative-water-sources.md) |
| B | Water semantics in source schemas | Hermes | [hermes/track-b-water-semantics.md](hermes/track-b-water-semantics.md) |
| C | Official recreation signals | Hermes | [hermes/track-c-recreation-signals.md](hermes/track-c-recreation-signals.md) |
| D | Community and review signals | Hermes | [hermes/track-d-community-signals.md](hermes/track-d-community-signals.md) |
| E | Current Ohvernight water audit | Hermes, from facts computed by the coordinator | [hermes/track-e-current-water-audit.md](hermes/track-e-current-water-audit.md) |
| F | CPW structured data: services, schemas, terms (follow-up for owner decision D7) | Hermes | [hermes/track-f-cpw-structured-data.md](hermes/track-f-cpw-structured-data.md) |
| — | Repository architecture and pipeline audit; source checks | Coordinator | this directory |

The owner decided the questions in `recommendations.md` on 2026-10-06
(decisions D1–D12). The resulting proposal is
[docs/specs/M4-functional-recreational-water.md](../../specs/M4-functional-recreational-water.md),
which governs where it differs from this directory.

Tracks A to E ran in parallel. Track F followed the owner's decisions. Track C stalled on its first attempt and was
re-run with a bounded method; only the second report is kept.
