# ADR-006: Explore uses optimized Leaflet with regional GeoJSON

## Status

Accepted. Recorded 2026-10-04 by owner decision D1. PR A lays the foundation;
PR B builds the adapter and shell.

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

- **R-1** | Payload or feature budget failure | A region's default-on layers exceed 15,000 displayed features or 1,500,000 bytes gzipped; or one display layer exceeds 5,000 features or 450,000 bytes gzipped and cannot be brought under by `min_zoom` or by splitting (section 16.5).
- **R-2** | Mobile loading or rendering threshold failure | Any timing threshold in 16.4 is missed, as a median of five runs at 390×844 with 4× CPU throttle, in three separate sessions after the loading design in 12.2 is fully implemented; or the manual real-device matrix records a reproducible pan, pinch or layer-toggle failure.
- **R-3** | M6 trail density | The M6 specification's measured trail layer for any one region exceeds the single-layer budget in R-1 after zoom gating and splitting.
- **R-4** | Statewide browsing | An approved product requirement needs one continuous view that draws detailed geometry from more than one region at once, or needs more than one region's budget loaded together.
- **R-5** | Browser memory | JS heap after load and garbage collection exceeds 66 MB (twice the M3 Aspen baseline of 33.4 MB) in three separate sessions of the committed script; or the manual matrix records a reproducible tab reload or crash on a real device while using Explore.

## Consequences

The M3 budgets and drift checks are binding, and PR A records measurements
against the committed baseline. State-wide density, M6 trail density, and
real-device behavior remain explicit future checks. Until a trigger is met,
the product does not carry the complexity or deployment requirements of a
second renderer.
