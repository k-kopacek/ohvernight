# ohvernight execution queue

The scheduled kickoff was deleted; work started directly in the existing task.

## Implemented in this delivery

- Restored the latest pipeline, preserved the Downloads copy, and included the working source under v2/pipeline.
- Independent RIDB credential check and paginated export, with explicit failures, validated inventory, atomic publication and a manual GitHub Actions template. Browser importer avoids known facility duplicates and keeps trip permission unknown.
- BLM native JSON adapter with exact study-area clipping, topology repair, hole/island preservation and complete ID checks. USGS requests use smaller batches and split failing batches within bounded request retries.
- Expanded the study area to include Lincoln Creek; the previous east boundary excluded it.
- Source-linked Lincoln Creek rule registry; no assumed forest-wide permission or stay limit. Unknown road rules remain unknown.
- Browser freshness logic, visible unconfirmed fire/closure notices, confidence labels and map-layer toggles. Trip-specific roads and candidates are hidden when a user's dates or vehicle differ from the generated snapshot.
- Python regression tests and mobile/desktop verification.

## Must still be verified or built

1. Run the independent RIDB workflow with the existing GitHub secret; local checks cannot establish whether that secret is valid. Upload the resulting inventory JSON to v2.
2. Verify a complete live map build and inspect generated Lincoln Creek plus a neighboring corridor against official camping rules. Generated areas remain research polygons, not legal campsite recommendations.
3. Audit Pitkin parcel coverage, ownership fields and reuse terms; add county public/private/unknown polygons. Federal management shading is only generalized context. Audit each additional county before expansion, and scope any paid fallback separately.
4. Expand the existing county page-change monitor to Forest Service orders and wildlife notices. Track successful retrieval separately from human-confirmed status, jurisdiction, effective periods and staleness. A page hash alone must never approve fire use or clear a closure.
5. Review and map order boundaries; connect confirmed restrictions and site-specific rules to candidate screening and trip evaluations. Do not ship candidate approvals before this coverage is real.
6. Add issue reporting/community leads with moderation and clear separation from verified agency facts. Add suitable product terms and obtain legal review before broader reliance; source caveats are not a substitute.
7. User-test finding an overnight option plus a backup near Aspen. Add actual route distance/approach checks once the overnight flow is useful. Full navigation, trails, GPX, wider counties and paid datasets remain later work.

## Delivery constraints

Keep all code and data together in v2. Workflow templates are included there, but GitHub requires their installed copies at repository-root `.github/workflows/`. No scheduled AI loops, automatic public deployment, purchased services or broad security scans are part of this kickoff.
