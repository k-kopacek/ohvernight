# Recommendations: proposed M4 architecture

The coordinator's synthesis of the research in this directory. It is a
proposal for the M4 specification. Nothing here is decided until the owner
approves a specification.

## 1. What M4 should achieve

Replace "every named hydrology line" with a smaller set of water a person
might visit, shown as whole rivers and lakes, with official recreation
information attached where an official source gives it and "not established"
everywhere else.

The research supports two separate jobs:

- **Selection and grouping** — decide which physical water is shown and make
  one river one thing. This can be done now from source fields already
  offered by the service the pipeline uses.
- **Enrichment** — attach official recreation information. This is slower,
  partly manual, and depends on a licence answer from CPW.

They should ship separately, selection first.

## 2. Evidence hierarchy

The owner's four classes map onto the existing data contract without a new
trust model:

| Class | Meaning | How it is carried | May it say an activity is allowed? |
|---|---|---|---|
| Source fact | Stated by the geometry source or an official dataset: name, type, perennial or intermittent, length, area, a designation, a facility's existence | Feature properties listed under the layer's `fields.source`, with provenance | No. Existence and designation only |
| Official recreation information | What an operator or agency says is allowed, restricted or closed at this water | A claim object per activity (`unknown`, `supported`, `restricted`) with source URL, scope, review basis and review date | Yes, and only this class |
| Derived fact | Computed by Ohvernight: grouped length, area, distance to a facility, which stream a piece belongs to | Properties listed under `fields.derived`; labelled as computed | No |
| Community signal | What people report | Separate records, never a claim; no verification method | No |

Rules that follow, all already in the contract's spirit:

- Each activity is its own claim. Fishing supported says nothing about
  boating or swimming.
- A designation (Gold Medal) and a facility (a ramp) are source facts. They
  do not make a claim `supported`.
- A restriction outlives its review date and is flagged; a supported claim
  past its review date becomes unknown.
- A spatial match produces a derived fact with its distance, not a source
  statement.

## 3. Source architecture

| Role | Source | Why |
|---|---|---|
| Canonical water geometry and type | USGS NHD, the service already used | It carries the type codes, perennial or intermittent status and GNIS id that selection needs. Public domain. Both regions already use it, so there is no licence change |
| Grouping key | `gnis_id` from NHD | Present today; one id per named stream |
| Successor to plan for | USGS 3DHP | NHD was retired in October 2023. 3DHP is current and has a mainstem id, but is reported to collapse the type distinctions M4 relies on, and its coverage of the two regions is unverified. M4 records 3DHP ids if they can be obtained cheaply and does not depend on them |
| Official recreation information | Operator and agency pages, reviewed by a person, for a short list of waters | The only class of source that states permission or prohibition. Highest authority; small volume |
| Official recreation facts | CPW Fishing Atlas (ramps, Gold Medal, special-regulation waters) | The best structured statewide source. Blocked on reuse terms and on reading its field schemas |
| Community signals | None in M4 | See section 6 |

Conflicts resolved:

- **NHD or 3DHP as canonical.** Track A prefers 3DHP as the current
  programme; track B shows NHD has the fields the selection rule needs and
  3DHP may not. Proposal: NHD in M4, with stable identifiers captured so a
  later move is a join and not a rebuild. The move itself is a later
  milestone decision.
- **Keyword rules or type codes.** Track E suggests excluding names
  containing "ditch", "canal" or "detention". The type code does this for
  lines from the source itself and is preferred. For waterbodies the type
  code does not separate detention structures (they are coded lake or pond),
  so a name keyword would be the only automatic signal, and a name is not
  evidence. Proposal: no name-keyword rule; use size and intermittent status
  for waterbodies, and accept that some structures remain until official
  information or a reviewed exclusion says otherwise.
- **Show only water with established public access, or show physical
  water.** Track E suggests showing a waterbody only when an official source
  establishes access. That would empty the map and would make absence of
  evidence look like absence of water. Proposal: show selected physical
  water, each with access and activities stated as not established unless a
  claim says otherwise.
- **A confidence field.** Tracks D and E suggest one. The contract retired
  confidence fields; none is added.

## 4. Selection rule (display), from source fields only

Canonical data keeps everything fetched. The rule below decides what the
browser shows.

**Lines.** Show stream and river pieces (`ftype` 460) that are perennial
(`46006`). Use artificial paths (558) only to connect a stream's pieces
through a lake. Do not show canals and ditches (336), pipelines (428) or
connectors (334). Intermittent streams (`46003`) are an owner decision:
hidden, or shown in a second, off-by-default layer labelled intermittent.
Ephemeral streams are not shown.

**Grouping.** All shown pieces with the same `gnis_id` form one stream: one
label, one selection, one detail. The pieces stay as canonical features; the
display carries a group id. Unnamed stream pieces have no group and are an
owner decision (proposal: not shown in M4).

**Waterbodies.** Show lakes, ponds and reservoirs (390, 436) that are
perennial and at or above a minimum area, named or not. Do not show
reservoirs whose code is treatment, tailings, evaporator, sewage or similar.
Intermittent lake or pond polygons are not shown. The area threshold is an
owner decision; the counts suggest testing 0.5 ha and 2 ha.

**What this does to the map**, from the counts in
[field-semantics.md](field-semantics.md):

| | Today | After the rule, roughly |
|---|---|---|
| Aspen line features to tap | 1,512 pieces | about 60 to 80 streams |
| Douglas line features to tap | 2,359 pieces | about 40 to 50 streams |
| Aspen waterbodies | 43 named | every perennial lake above the threshold, named or not |
| Douglas waterbodies | 33 named, half intermittent | about 17 perennial named, plus unnamed above the threshold |

The stream counts are estimates from distinct names and must be measured
when the fields are fetched.

## 5. What the pipeline should start keeping

For every water feature, from the service already in use: `ftype`, `fcode`,
`gnis_id`, `gnis_name`, `permanent_identifier`, `reachcode`, `lengthkm` or
`areasqkm`, `elevation` for waterbodies, `visibilityfilter`, and the
artificial path's waterbody link. Douglas should fetch unnamed features too,
so its canonical data is complete in the way Aspen's is.

Feature ids should move from the service row number to a stable source
identifier. This changes every water feature id, so saved selections and any
test that pins an id need a migration note. `permanent_identifier` is the
candidate; USGS says it can change on edit, and NHD is frozen, so in practice
it will not change again.

## 6. Community signals: not in M4

No community source found is both useful for recreation and clearly usable
for automated, stored summaries; most prohibit it outright
([community-signals.md](community-signals.md)). Recommendation: M4 defines
where a community signal would live in the evidence hierarchy and builds no
community pipeline. An optional, low-risk step is an outbound link from a
water's detail to a search on a community site, storing nothing.

## 7. Display and interaction

M4 uses the M3 selection model unchanged:

- A grouped stream is a line: tap selects the whole stream, casing and
  thicker stroke on all its pieces, the map may fit it, detail opens at the
  partial height.
- A waterbody is a polygon: tap selects with the stronger fill, the camera is
  preserved, detail opens.
- Detail shows only what is carried, in separate sections: what the source
  says (name, type, perennial or intermittent, size as a computed figure),
  official recreation information per activity where a claim exists, and the
  standing statement that access and permitted activities are not
  established where it does not. A restriction is shown as prominently as a
  permission.
- No activity icon, colour or filter implies permission. If water is styled
  or filterable by activity, it is by "official information says" and never
  by type.

One adapter question: selecting a grouped stream means highlighting many
features for one selection. The adapter's `setSelected` takes one feature id
today. Either the display merges a group's geometry into one feature (which
the display rules forbid today) or selection learns about groups. This is the
main design choice for the specification.

## 8. Contract and validation changes needed

- Display rule R61's water exception names the current selection rule; it
  must name the new one, and the validator must be able to recompute it from
  canonical fields.
- Grouping needs a derived group id on display features, and a rule that
  every member of a group shares the canonical `gnis_id`.
- New source fields declared in each manifest's `fields.source`.
- A claim per activity for water needs a home: the existing `rules` records
  with `place_ids`, or claim objects on a per-water enrichment record. The
  second is cleaner and is a contract addition.
- `fact_coverage.recreation_permission` moves from `none` or `context` to
  `reviewed_partial` only when at least one reviewed water record exists.
- Validation stays time-independent.

## 9. Budgets

Default-on payloads are 3.81 MB (Aspen) and 3.62 MB (Douglas) against
4.5 MB. Aspen's water artifact is 1.13 MB today. Dropping infrastructure,
intermittent and tiny features should shrink it; adding unnamed lakes and new
properties grows it. Proposal: water display artifacts must not exceed their
current size, measured before and after. The A10 performance limits apply
unchanged; Douglas all-layers time is the tight one.

## 10. Proposed PR breakdown

| PR | Content | Depends on |
|---|---|---|
| M4-A | Pipeline keeps the source fields and stable ids; canonical data refreshed for both regions; contract fields declared; no display change | Specification approval. Needs a live fetch from the NHD service, which must be explicitly authorised |
| M4-B | New selection rule and stream grouping in the display build; validator rules; adapter and shell support for selecting a group; detail shows type and perennial status | M4-A |
| M4-C | Official recreation information for a short reviewed list of waters, as claims per activity, with restrictions first; detail sections | M4-B; owner's list of waters |
| M4-D | CPW structured facts (ramps, Gold Medal, special regulations) | An answer on CPW reuse terms; a schema probe |

M4-A and M4-B deliver the visible clean-up. M4-C delivers trust-relevant
content for the waters that matter most. M4-D is optional for calling M4
done.

## 11. Major unknowns

1. CPW Fishing Atlas reuse terms and field schemas.
2. Whether 3DHP covers both regions with elevation-derived data, and whether
   it really loses the perennial and intermittent distinction.
3. How many streams and lakes the selection rule actually yields; the counts
   here are from a bounding-box probe and name counts.
4. Whether `gnis_id` grouping ever joins pieces that a user would not call
   one stream (forks and branches carry their own names, so probably not).
5. Recreation status of several named Aspen waters (Grizzly, Wildcat, Maroon
   Lake water use).
6. Whether trail features need the same grouping; that is recorded for M6.

## 12. Owner decisions required

1. **Canonical source:** stay on NHD for M4 and plan 3DHP later (proposed),
   or move to 3DHP now.
2. **Intermittent streams:** hide, or show in an off-by-default layer.
3. **Unnamed water:** show unnamed lakes above the size threshold (proposed
   yes); show unnamed streams (proposed no).
4. **Size threshold for lakes:** the value, after seeing both maps at 0.5 ha
   and 2 ha.
5. **Structures coded as lakes** (detention and supply reservoirs with no
   recreation information): show as physical water with "not established"
   (proposed), or allow a reviewed exclusion list.
6. **Scope of official recreation information in M4:** which waters get
   reviewed claims first. Proposed: the restricted ones first (Cheesman,
   Strontia Springs), then Chatfield, Rueter-Hess, and the Aspen waters with
   an official page.
7. **CPW:** whether the owner will ask CPW about reuse terms, and whether
   M4-D waits for the answer or drops out of M4.
8. **Community signals:** none in M4 (proposed), with or without outbound
   search links.
9. **Live fetch:** authorising the pipeline refresh that M4-A needs.
10. **Feature id change:** accepting that water feature ids change once.
