# Product principles

Durable guidance for what Ohvernight is for and how product choices are made.
These are principles, not implementation detail; specifications in
`docs/specs/` decide how each milestone applies them. Trust-sensitive rules
are stated normatively in [trust-principles.md](trust-principles.md).

1. **Help people choose an adventure.** Discovery should help a user decide
   where to go and what to do, not merely display map layers.
2. **Explore Map stays useful.** Open-ended discovery without trip filters
   remains a first-class experience alongside guided selection.
3. **Mobile usability matters.** The product is used on a phone, often in the
   field. The map needs room, and controls must not crowd it out.
4. **Relevance over volume.** Outdoor-recreation relevance matters more than
   the amount of data shown.
5. **Functional recreation over geographic clutter.** Show the lake someone
   can plan around before the drainage line nobody can use.
6. **Prefer authoritative sources.** Agency and other primary sources come
   first, with attribution and reuse terms respected.
7. **Uncertainty must be visible.** What is unknown, unchecked or out of date
   is shown as such, not hidden or smoothed over.
8. **Claims must not exceed evidence.** Legal, access and permission claims
   are limited to what a reviewed source supports.
9. **UX must not imply unsupported certainty.** Styling, labels, wording and
   ranking carry meaning; none may suggest more confidence than the data has.
10. **Expand through shared contracts.** A new region uses the shared regional
    contract and evidence semantics, not one-off app semantics.

Principles 11 to 15 state direction recorded 2026-10-08. The linked documents
label what is CURRENT, PLANNED and FUTURE; none of these describes shipped
behaviour unless that document says so.

11. **One Explore surface.** Explore is ultimately one geographic discovery
    surface. Region packages are a data-delivery boundary, not a navigation
    boundary for the user. See
    [continuous-explore.md](../architecture/continuous-explore.md).
12. **Proximity is not a relationship.** Being near something does not
    establish connection, access, suitability or permission. Trips are
    assembled from identified things and established links between them, and
    every link that is not established is shown as unknown. See
    [adventure-model.md](../architecture/adventure-model.md).
13. **Not checked is not the same as no restriction.** What Ohvernight has
    looked for is recorded separately from what it found, and what it has not
    looked for is visible.
14. **Intent stays visible.** Location, activities, dates and, later, the
    vehicle and access profile stay primary and easy to change. Evidence
    detail and advanced filtering are secondary and are not where core
    discovery controls live. Unknown, restriction and not-checked states are
    not evidence detail; they stay with the result.
15. **Every milestone answers a product question.** From M5 onward a
    milestone reports what a user can newly accomplish, measured against the
    [canonical acceptance scenario](acceptance-scenario-douglas-dirt-bike.md)
    and the [product scorecard](product-scorecard.md), as well as what
    capability was added.
