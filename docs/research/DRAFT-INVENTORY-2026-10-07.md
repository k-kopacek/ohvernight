# Research drafts added 2026-10-07: inventory

These 27 files were written on 2026-10-07 by Hermes and by Claude research agents and were sitting uncommitted in a worktree. They are stored here so they are not lost. **None has been reviewed by the coordinator. Nothing in them is decided, approved or verified for production, and none changes `ROADMAP.md`.**

"Evidence level" is what each file says about itself, not a coordinator finding:

- **Hermes sourced** — web research by Hermes, stored as returned; cites publisher pages but nobody has re-read them.
- **Repository measured** — a Claude agent measured or read files in the repository (labelled VERIFIED inside the file). Not re-checked by the coordinator.
- **Inference** — synthesis of other reports here; no new source was read.

| File | Subject | Evidence level | Written by |
|---|---|---|---|
| `m4-water/claims/hermes-w2-third-set-and-conflicts.md` | M4 (M4-C dossiers and claim conflicts) | Hermes sourced | Hermes |
| `m4-water/depth-audit.md` | M4 (adversarial audit of spec and M4-A at `aa5c20b`) | Repository measured | Claude agent |
| `m5-land/current-land-audit.md` | M5 | Repository measured | Claude agent |
| `m5-land/hermes/m5-land-source-matrix.md` | M5 | Hermes sourced | Hermes |
| `m5-land/M5-preliminary-research-gate.md` | M5 | Inference, with some repository measurement | Claude agent |
| `m6-trails/current-trail-audit.md` | M6 | Repository measured | Claude agent |
| `m6-trails/hermes/m6a-cotrex-usfs-identity.md` | M6 (COTREX and USFS terms, schema, identity) | Hermes sourced | Hermes |
| `m6-trails/hermes/m6b-competitor-trail-identity.md` | M6 | Hermes sourced | Hermes |
| `m6-trails/M6-trail-identity-research-packet.md` | M6 | Inference, with some repository measurement | Claude agent |
| `m7-camping/hermes/m7-overnight-evidence-sources.md` | M7 | Hermes sourced | Hermes |
| `m7-camping/M7-camping-evidence-model-draft.md` | M7 | Mixed: repository measured, agent-read web pages, Hermes sourced | Claude agent |
| `m8-adventure/ranking-architecture-options.md` | M8 | Inference | Claude agent |
| `product-opportunities/hermes/b9-bear-case.md` | Product strategy | Hermes sourced | Hermes |
| `product-opportunities/hermes/c8a-competitor-strategy-mapping.md` | Product strategy | Hermes sourced | Hermes |
| `product-opportunities/hermes/c8b-competitor-strategy-camping.md` | Product strategy | Hermes sourced | Hermes |
| `product-opportunities/bear-case.md` | Product strategy | Inference from Hermes reports | Claude agent |
| `product-opportunities/competitor-delta.md` | Product strategy | Inference from Hermes reports | Claude agent |
| `product-opportunities/moat-analysis.md` | Product strategy | Inference | Claude agent |
| `product-opportunities/first-party-data-flywheel-options.md` | Product strategy | Inference | Claude agent |
| `customer-discovery/interview-kit.md` | Customer research | Inference from Hermes reports | Claude agent |
| `customer-discovery/mvp-experiments.md` | Customer research | Inference from Hermes reports | Claude agent |
| `business/hermes/p18-pricing-and-costs.md` | Business and pricing | Hermes sourced | Hermes |
| `business/business-model-options.md` | Business and pricing | Inference from Hermes reports | Claude agent |
| `engineering/hermes/a17-map-accessibility.md` | Technical research | Hermes sourced | Hermes |
| `engineering/map-accessibility-recommendations.md` | Technical research | Repository measured, plus Hermes sourced | Claude agent |
| `engineering/source-monitoring-architecture.md` | Technical research | Inference | Claude agent |

Paths are relative to `docs/research/`. That is 26 files; the 27th, `engineering/security-and-abuse-review.md`, is deliberately not in this pull request (see below).

## Notes

- **Duplicates.** None is a duplicate. `product-opportunities/bear-case.md` is a synthesis of `hermes/b9-bear-case.md`, and `competitor-delta.md` of the two `c8` reports; both layers are kept.
- **Stale base.** The repository-measured files read the M4-A branch at `aa5c20b`. M4-A has since merged with one more code fix (legacy IDs across a later fetch); the depth audit should be re-read against `main` before anyone relies on it.
- **Broken link.** `M6-trail-identity-research-packet.md` names a companion `M6-source-matrix.md` that was never written.
- **Held back.** `engineering/security-and-abuse-review.md` describes a weakness in the legacy root site that it says is not exploitable with today's data. This repository is public, so the file is left out until the owner decides whether to fix first or publish as is.
- **Trust.** The M4-C dossier file is research input only. No claim record exists anywhere, and every dossier needs a coordinator re-read of the source and owner approval before any production record.
