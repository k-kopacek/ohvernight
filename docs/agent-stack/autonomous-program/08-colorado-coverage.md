# 08 — Statewide Colorado expansion strategy

**Proposed direction**, aligned with `docs/architecture/continuous-explore.md`; currently that document is PLANNED without an approved implementation spec. This document alone does not authorize replacing the loader or bulk fetching.

## Target architecture

- One continuous Explore surface, not per-county applications.
- Versioned region packages remain the validation, publication and provenance unit.
- Small initial coverage/catalog index describing package extents, layer/category coverage, relevant versions and digests.
- Cross-package lightweight search index; lazy spatial loading/prefetch by viewport and selected candidate; bounded cache and release of offscreen data.
- Namespace-safe canonical identities across packages; user-facing identity deduplication only when source identifiers/review establish it. Regions may contain clipped display parts of the same true feature.
- Facts/claims and freshness/coverage never merge merely because geometry overlaps.
- Coverage displayed by category: not covered, fetched but not reviewed, reviewed with restricted/supported/unknown claims. Treat null/unknown distinctly from verified absence.

## Geographic rollout

1. **Contract proof:** current Aspen + Douglas with a representative edge-crossing river/trail/site; identify cross-region IDs and source overlaps.
2. **Third region:** choose a geographically meaningful Colorado package to stress cross-boundary identity, hydrology, trails, road/access relationships and device/performance budgets. Source availability, not convenience, determines selection.
3. **Regional expansion waves:** batch region packages by source family/ownership geography, independent worker output, strong source coverage metrics and automated cross-package invariants. No county-by-county owner prompt if adopted spec already permits those regions.
4. **Statewide catalog:** add statewide location search, no silent dead zones, per-category coverage audit. Mark gaps honestly even if statewide map shell is available.
5. **Hardening:** large-view memory, network fallback, slow connection, tiny screen, cross-county route ambiguity, duplicated name collisions, unknowns/staleness.

## Retired NHD caution

M4's NHD snapshot is transitional; USGS 3DHP is a candidate successor. Require real-record parity proofs (hydro categories, water type, canals, source IDs, group memberships, exclusions, aliases and activity-claim linkage) and a separate approved migration decision before changing the canonical source or scaling NHD assumptions broadly. Do not silently re-identify or lose old source records.

## Performance and correctness gates

Retain M3/M4 performance measurement discipline. Define per-visible-view budgets for many packages, not only per-region cold-load. Measure map usable, default layers, long tasks, memory, layer toggles, payload, scroll interactions, search and cache eviction on target phone. No threshold weakening to make expanded data pass. Known false open/access/camping implications block publication even if performance passes.

## Source rights

Validate use, attribution, storage, redistribution, API limitations and freshness for each authoritative family. `COTREX` access/content is NOT automatically licensed; upstream agency sources can be alternatives only after verified rights. Unresolved rights = omit/defer that data, not a model-generated legal interpretation.
