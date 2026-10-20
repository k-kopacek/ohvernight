# M4-C implementation blueprint

Prepared by the coordinator so M4-C can start as soon as M4-B is merged and
the owner has reviewed the draft records. It adds no rule; specification
section 9 governs. M4-C is small in code and careful in content.

## 1. What M4-C waits on

| ID | Decision | Where |
|---|---|---|
| C-1 | Which waters get records in the first set | [draft-records-for-owner-review.md](draft-records-for-owner-review.md) sections 1–5 and 7 |
| C-2 | Whether a river may carry reach-scoped claims in M4-C, or waterbodies only | Same file, section 8. Recommendation: waterbodies only |
| C-3 | Whether an operator's description of an offered activity supports `allowed` | Same file, Chatfield. Recommendation: no; a sentence about permission is required |
| C-4 | Wording of each summary | Approved record by record in the pull request |
| C-5 | Whether "entering the lake is prohibited" (Maroon Lake) is recorded as swimming `prohibited` | Same file, section 5. Recommendation: yes |

## 2. Division of work

| Who | Does |
|---|---|
| Hermes | Refreshes the dossier for each chosen water on the day before the pull request: page URL, the sentence relied on, the page's own date |
| Coordinator | Re-reads every page, applies the [claim review checklist](claim-review-checklist.md), writes the record content (statuses, summaries, dates, maximum ages) in the brief |
| Codex | Implements the registry, validator rules R74 and R76, the detail section, freshness, and enters the record content exactly as given |
| Owner | Approves each claim in the pull request |

Codex does not research or decide a claim. It receives the record content as
data.

## 3. Files expected to change

| File | Change |
|---|---|
| `v2/regions/<id>/water-recreation.json` | New, one per region, with the approved records |
| `v2/regions/<id>/region.json` | `water_recreation` path; `fact_coverage.recreation_permission` to `reviewed_partial` with a rewritten statement (owner-approved wording) |
| `v2/pipeline/scripts/lib/region_contract.py` | R74, R76; schema for the registry; the `reviewed_partial` extension |
| `v2/pipeline/config/water_display.json` | `non_claim_hosts` filled in |
| `v2/explore/` water detail module | The "Agency or operator statement" section; status words; freshness; ordering (prohibited and restricted first) |
| `v2/explore/region-loader.js` | Loads the registry with the water layers; counts toward the byte budgets |
| `v2/pipeline/docs/data-contract.md` | The registry and the four-status activity claim |
| Tests | Negative fixtures for every invalid form in specification 9.2; the freshness table as a pure function with an injected time; detail rendering for each status and for an overdue restriction; browser checks for one prohibited record and one water with no record |

Must not change: the map's symbology (no restriction colour or icon, owner
decision O3); any M4-B rule; any WW string.

## 4. Commit sequence

1. `feat: validate water recreation records (R74, R76)` — schema, rules, negative fixtures. No data.
2. `feat: compute claim freshness without weakening restrictions` — pure function and tests for the table in specification 9.3.
3. `feat: show agency or operator statements in water detail` — rendering with fixtures only.
4. `data: add reviewed water recreation records` — the approved records, the manifest path and the coverage statement.
5. `test: cover reviewed claims in the browser check`.
6. `docs: contract and dossiers` — dossiers stored under `docs/research/m4-water/claims/`.

Checkpoint after step 3 (before any real record is entered) and after step 5.

## 5. Stop conditions

- A page read on the review date no longer says what the dossier quotes.
- Two official pages disagree.
- A record would need a status or wording the specification does not provide.
- A claim would rest on a facility, a designation, stocking, a map or a community source.
- An `allowed` claim has any condition specific to the water (it is then `restricted`).
- Anything suggests marking restrictions on the map.

## 6. Additional wording the owner must approve in M4-C

The `fact_coverage.recreation_permission.statement` for each region changes
when the first record lands. Proposed:

`A small number of waters carry statements reviewed from the agency's or operator's own page, each with its review date. For every other water, and for every activity not stated, nothing is established.`

## 7. Draft Codex brief (outline)

Target, read-first list and process sections as in the M4-B brief. Scope: the
six commits above. Record content is supplied as a JSON block in the brief,
written by the coordinator from confirmed sentences and approved by the
owner; Codex enters it exactly. Must not: research, edit a summary, add a
record, change a status, mark anything on the map, touch M4-B rules. Usage:
suites and one browser check; the coordinator runs repeats. Acceptance:
specification section 24 criteria 13–16.

## 8. Rollback

Revert the pull request, or empty a registry: every water then shows "Mapped
water. Access and allowed activities are not established." A single wrong
claim is set to `unknown` in a one-line change, which is always safe.
