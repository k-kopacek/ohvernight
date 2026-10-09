DRAFT - UNREVIEWED RESEARCH

# Forest orders as first-class entities (M7 input)

This is an illustrative research model, not a claim record and not a determination that any restriction currently applies. It carries forward the Rampart research archive's checked sources and uncertainties without resolving them. The source documents were read on 2026-10-09; the archive records checks between 05:02 and 05:06 UTC.

## Proposed entity and relationship model

An order is a stable, independently addressable instrument. Its identity includes the issuing unit and the order number exactly as printed; a title, source URL, or facility name is not a substitute. The instrument type distinguishes a signed Forest Service order from a temporary fire restriction notice. A notice whose order number cannot be confirmed keeps that number unknown rather than borrowing a nearby standing order's number.

Each entity stores the instrument's own effective interval, including whether the text says “unless rescinded.” It also stores the geographic scope exactly as the instrument states it, separately from Ohvernight's applicability relationship to a site. The scope field holds a short quotation and a source pointer; it does not turn the quotation into a normalized list of affected sites. If a source states scope by road, township, distance, district, or forest-wide jurisdiction, retain that basis. Do not replace it with an inferred facility list.

The `constrained_by` relation points from a site to an order and has a stable relation ID, origin, evidence, and any derivation. The Rampart archive supports source-backed links where the order names the site's road (for example, 300.T / Flat Rocks Campground); a site inclusion calculated from a township or a quarter-mile radius is derived and must retain the exact inputs and rule. An unestablished relation stays `unknown`; proximity or a name match cannot establish it. These choices follow the relationship origins and fail-closed treatment of unclear restriction scope in `docs/architecture/adventure-model.md`.

Store prohibitions as short verbatim excerpts with the cited provision. Never paraphrase a prohibition into permission or a general-use conclusion. The example keeps the order's scope and prohibitions distinct from contextual notes; those notes are not claims.

## Effective dates, expiry, and conflict

An order reaching its printed end date remains in the record with an expired status. It is not silently removed from the site's history or from an evidence result. A later instrument is represented as a separate entity and linked with an explicit `supersedes` relation only when the source establishes that relationship. PSICC-2022-08 explicitly replaces PSICC-2017-11; that does not make it a successor to the other Rampart orders.

For the Stage 1 fire restriction, preserve independent official statements, their scope, timestamps, and checked times. The Forest Service release says Stage 1 runs from August 21 through November 14, 2026 unless rescinded; the checked PSICC alerts list is silent; the Douglas County Sheriff's page says county Stage 1 restrictions were lifted September 17. These records do not establish that the same jurisdictional instrument was rescinded: the county statement is scoped to unincorporated Douglas County, while the Forest Service release covers named ranger districts. Keep status unresolved and flag the scope mismatch rather than treating silence or the county statement as proof that the Forest Service restriction ended. The archive did not retrieve a signed Stage 1 order or confirm its order number, so the notice entity's order number is unknown. It is separate from standing Order 02-12-00-24-04.

## Evidence coverage

Coverage answers what was checked, by whom, where, and when. For example, `orders checked for Cabin Ridge Picnic Area on 2026-10-09` should name the Forest Service alerts list and the checked order sources, the Forest Service jurisdiction, and the result `checked`. If a record was found, coverage points to that record; if none was found, the fact remains unknown. Coverage never says “no order applies,” never spreads to a neighboring site or another jurisdiction, and is not a confidence or completeness score.

## Pipeline needs

The archive found these order instruments only as PDFs or PDF-linked text; it found no structured order source. A pipeline would need to retain the original document and source URL, extract text with page-level provenance (including OCR/image-derived portions), capture issuer, printed identifier, instrument type, signed and effective dates, verbatim scope and prohibitions, and record extraction confidence. It would also need explicit supersession links, jurisdiction-scoped status observations and conflicts, reviewed site relationships with source-backed/derived/unknown origins, checked-time coverage records, expiry handling that preserves history, and a human review path for corrections. Automated geographic matching must not publish applicability without a recorded derivation and review policy.

## Sources represented in the fixture

- PSICC-2022-08, order PDF and Exhibit B table: https://www.fs.usda.gov/sites/nfs/files/r02/psicc/publication/alerts/fseprd1060368.pdf and https://www.fs.usda.gov/sites/nfs/files/r02/psicc/publication/alerts/Order%202022-08%20table.pdf
- 02-12-00-23-07, food-storage order PDF: https://www.fs.usda.gov/sites/nfs/files/r02/psicc/publication/alerts/fseprd1112291.pdf
- 02-12-00-24-04 and Exhibits C/F: https://www.fs.usda.gov/sites/nfs/files/r02/psicc/publication/alerts/fseprd1174599.pdf
- Stage 1 Forest Service release: https://www.fs.usda.gov/r02/psicc/newsroom/releases/pike-san-isabel-national-forests-move-stage-1-fire-restrictions
- Forest Service alerts list: https://www.fs.usda.gov/r02/psicc/alerts
- Douglas County Sheriff's fire restriction page: https://www.dcsheriff.net/fire-restrictions/
