# ADR-006: Explore uses optimized Leaflet with regional GeoJSON

## Status

Accepted. Recorded 2026-10-04 by owner decision D1. Implemented in M3 PR A
as the foundation for PR B.

## Decision

M3 Explore uses Option 1: the existing vendored Leaflet renderer with a narrow
map adapter, region-scoped display artifacts, and per-layer lazy GeoJSON
loading. The loader requests only the active region's manifest, configuration,
coverage and declared layers. No MapLibre prototype, vector-tile service,
PMTiles archive, bundler, framework or new runtime dependency is introduced.

The renderer decision is deliberately limited. The adapter surface is the
approved section 8.1 surface, and display artifacts remain delivery products
derived from canonical data. This keeps the current static deployment and
allows the product to revisit rendering if measured requirements change.

## Reopening triggers

The decision is reopened by a new specification and owner decision when any
one objective trigger is observed. A trigger opens the question; it does not
choose MapLibre:

- **R-1 payload or feature budget:** a region's default-on set exceeds
  15,000 displayed features or 1,500,000 bytes gzipped, or a display layer
  exceeds 5,000 features or 450,000 bytes gzipped and cannot be remedied by
  `min_zoom` or splitting.
- **R-2 mobile loading or rendering:** a section 16.4 timing threshold fails
  in three separate sessions after the 12.2 loading design is implemented,
  or the manual device matrix records a reproducible pan, pinch or toggle
  failure.
- **R-3 M6 trail density:** a measured trail layer exceeds the R-1
  single-layer budget after zoom gating and splitting.
- **R-4 statewide browsing:** an approved requirement needs one continuous
  detailed view across more than one region or needs more than one region's
  budget loaded together.
- **R-5 browser memory:** post-GC JS heap exceeds 66 MB in three separate
  committed-script sessions, or the manual matrix records a reproducible
  Explore tab reload or crash on a real device.

## Consequences

The M3 budgets and drift checks are binding, and PR A records measurements
against the committed baseline. State-wide density, M6 trail density, and
real-device behavior remain explicit future checks. Until a trigger is met,
the product does not carry the complexity or deployment requirements of a
second renderer.
