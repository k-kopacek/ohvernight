# M4-A merge decision packet

**PR #12 is reviewed and green. Recommendation: approve it for merge at head `aa5c20bc990591f310045aa8413763e9abc5f926`.**

## DECISION
Approve pull request #12 (M4-A, source preservation) for merge at that exact head?

## EVIDENCE
- CI on that head: `python`, `node`, `browser` all pass.
- Coordinator's own runs at the last code commit (`2d7e13a`): Python 152 pass, Node 122 pass, display rebuild with no diff, full browser check passing.
- Independent data checks: every non-water layer in both canonical bundles identical to `main`; every previous water geometry present, with no removal and no geometry or name change; 6,926 + 2,359 + 2,135 water feature IDs unique and built from the source's permanent identifier; every previous ID carried exactly once in `legacy_ids`; displayed water identical to `main` by geometry and name; manifest wording identical to `main`; no activity, access or grouping field anywhere.
- The one live NHD request (owner decision D9) is documented in `docs/research/m4-water/nhd-snapshot.md`.
- Performance: an interleaved comparison on a quiet machine shows `main` and M4-A indistinguishable; all six sessions pass every limit. Two earlier sessions that missed the Douglas all-layers limit overlapped other work on the machine and are recorded in the pull request.

## CURRENT BEHAVIOR
`main` stores a name and little else for each water feature, with IDs built from a service row number.

## OPTION A — approve and merge
M4-B can start. The map looks exactly the same.

## OPTION B — hold
Nothing changes; M4-B stays blocked. Useful only if the owner wants to read the snapshot document first.

## TRADEOFFS
The canonical files grow (Aspen 10.1 → 12.5 MB, Douglas 6.2 → 10.2 MB). The browser does not load them.

## RISKS
- Water feature IDs change once. Nothing in the app stores them; old IDs are kept as aliases.
- NHD is a retired dataset; M4 records that as technical debt.

## RECOMMENDATION
Approve PR #12 at `aa5c20bc990591f310045aa8413763e9abc5f926`.

## WHAT CHANGES IF APPROVED
`main` gains the NHD source fields, stable water IDs, the type-code tables, four validator rules, the alias files, the snapshot record and specification amendments A1–A3.

## WHAT REMAINS UNCHANGED
Everything a user sees: which water is drawn, its geometry, every string, every interaction. Every non-water layer.

## TESTS REQUIRED
None further before merge. After merge: post-merge CI on `main`.

## ROLLBACK
Revert the merge commit. Canonical files, IDs and display artifacts return together.
