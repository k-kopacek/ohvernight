# Continuous geographic Explore

Status: durable architectural requirement, recorded 2026-10-08. It changes no
shipped behaviour and reopens no completed milestone. Labels used here:
**CURRENT** is what `main` does today, **PLANNED** is committed direction with
no approved specification yet, **FUTURE / DEFERRED** is recorded so it is not
lost.

## Requirement

Ohvernight Explore is ultimately **one geographic discovery surface**. A
region package is an implementation and data-delivery boundary. It is not a
navigation boundary the user should have to learn.

A user thinks "dirt-bike trails south-west of Denver" or "somewhere to camp
near the Roaring Fork". They do not think "the Douglas app" or "the Aspen
app", and a trail system, river or forest that crosses a county line is one
place to them.

## CURRENT

- One shared Explore shell (`v2/explore/`) loads exactly one region per page
  load, chosen by the `region` query parameter, with `aspen` as the default.
- The region loader refuses any path outside the active region's directory.
  That is a deliberate M3 safety property, not an oversight.
- Each region has its own manifest, coverage statement, fact coverage, display
  index and byte budgets. Search covers the active region only.
- Source data is clipped at a regional boundary. Douglas water is the single
  approved exception (kept to about 500 m beyond the county line so a river on
  the boundary is not cut into pieces).
- Outside the active region the map shows a basemap and nothing else. The
  coverage statement says that nothing is known there; the map itself does not
  mark where coverage ends.
- Feature IDs are unique within a region. Nothing guarantees uniqueness across
  regions, and nothing links a feature in one region to the same real-world
  thing in another.

## Desired future behaviour (PLANNED, no specification yet)

- One Explore map.
- Location search across every supported area.
- Data loaded lazily as the user searches or pans. No requirement to preload
  all of Colorado.
- Results that cross region and jurisdiction boundaries: a trail, river or
  management unit is one result even when two packages each hold part of it.
- A clear, on-map indication of where Ohvernight has coverage and where it has
  none.
- No "Aspen app" versus "Douglas app" mental model.

## Uncovered-area behaviour

An area with no Ohvernight coverage is **unknown**, and must read as unknown.
It must never read as empty, as unrestricted or as "nothing here".

- An uncovered area is visibly distinct from a covered area that happens to
  hold no features of a kind.
- Coverage is per kind of fact. An area can have land context and no trail
  data. See the evidence-coverage model in
  [adventure-model.md](adventure-model.md).
- A search or trip result must not silently stop at a coverage edge. If a
  candidate depends on something outside coverage, that dependency is listed
  as unknown.

## Data-loading implications

These are constraints on later design, not a design.

1. **Region packages remain the unit of publication, validation and
   provenance.** A continuous surface is a different way of *loading* them,
   not a replacement for the regional contract.
2. **A coverage index is needed**: a small, always-loaded description of which
   packages exist, their extents and what each covers, so the shell can decide
   what to fetch and can draw the edge of coverage.
3. **Identity must survive package boundaries.** Stable IDs need a namespace
   that is unique across packages, and a real-world thing that spans packages
   needs one user-facing identity (the M4 grouping work and the M6 trail
   identity requirement are the first two cases).
4. **Clipping becomes a display concern, not an identity concern.** A feature
   cut at a package edge is one feature with two delivered parts.
5. **Budgets are per view, not per region.** The M3 byte and time budgets were
   set for one region at a time; a panning surface needs budgets for what is
   on screen and for what is retained in memory.
6. **Search needs a cross-package index** that is small enough to load without
   loading the packages it points into.
7. **Evidence does not merge.** Fact coverage, limitations and source
   statements stay attached to the package and source they came from. Two
   packages with different coverage must not be presented as one uniform
   level of knowledge.

## Constraints

- Do not redesign M3. The single-region loader and its path restriction stay
  until an approved specification replaces them.
- Do not implement statewide loading now.
- The renderer decision in
  [ADR-006](decisions/ADR-006-explore-rendering-architecture.md) and its
  reopening triggers are unchanged. A continuous surface is a likely moment
  for those triggers to be evaluated; it is not itself a decision to change
  renderer.
- No trust rule is relaxed to make a cross-region result look complete.

## Likely milestone

- **M5 to M7** must not make this harder: each new source keeps stable,
  namespace-safe identities and does not assume that a region boundary is a
  real-world boundary.
- **M8** is the first milestone that needs it, because a trip candidate near a
  boundary is wrong if it can only see one side.
- **Regional expansion after M8** is where a third and later region make the
  one-region-per-page model untenable.

The milestone that implements it is the owner's decision when M8 is
specified.
