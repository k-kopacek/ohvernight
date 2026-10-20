# Aspen / Snowmass pilot

`/v2/` keeps the trip-planner landing; `/v2/?region=aspen&view=map` opens shared
Explore directly. Planner evaluation, Plan A / backup, trail search, nearby
lists and the adventure pilot retain their pinned base behaviour. Existing
`ohvernight-trip-v1` state is read and kept.

This directory contains the hand-reviewed [region.json](region.json), the
presentation-only [explore.json](explore.json) and generated `display/`
artifacts. The configuration declares `trail_season_check: false`: Aspen
shows published activity records without Douglas-style trip season badges.
Canonical files remain at their existing `v2/` paths. The shell never fetches
`map-data-v2.json`; transport copies come from the display index.

The 1,555 displayed water features remain the same selection. Generalized
management shading is context, not parcels or access. The non-spatial fire
monitor remains available through Sources & coverage and the unchanged
`Trust.sourceSummary` wording. Freshness follows the manifest and never hides
features or weakens restrictions. See the
[normative regional contract](../../pipeline/docs/data-contract.md).

Rebuild from the repository root with
`v2/pipeline/.venv/bin/python v2/pipeline/scripts/build_display.py`; generated
files are never hand-edited. Automated browser checks cover all four sizes;
real iOS Safari and Android Chrome checks remain required before merge.
