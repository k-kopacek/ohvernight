# CPW structured data: status for M4-D

State on 2026-10-07: **TERMS STILL UNCLEAR.** M4-D is not proposed.

Basis: Hermes [track F](hermes/track-f-cpw-structured-data.md) (in the merged
research record) read the service metadata, layer schemas, ArcGIS item
records and terms pages on 2026-10-06. No further CPW research was run
overnight, because that report already answers the questions asked and a
repeat would spend shared usage without new evidence.

| Question | Finding |
|---|---|
| Automated retrieval from the public services | Clearly possible; the services allow anonymous queries and CPW describes streaming services for developers |
| Transformation for analysis or a custom map | Permitted with conditions, on CPW's own description of use by app developers |
| Storing a transformed copy in a public repository | Unclear. The NDIS Fishing Atlas services have blank copyright and licence fields. The Colorado Information Marketplace labels the Fishing Atlas "Public Domain", but that entry is a link to the application, not the data |
| Redistribution with the product | Unclear for the Fishing Atlas and the inspection-station layer; defensible with attribution for `CPWAdminData`, whose item says it is "for public distribution" but gives a disclaimer, not a licence |
| Commercial use | Not addressed anywhere found |
| Update cadence | Not stated; the 2025 Fishing Atlas service coexists with a legacy one that alone exposes the water-code layers |
| Schema | Read for the main layers. A water code exists on some layers and not others, is null in sampled ramp and waterbody records, and has no documented stability |

What would change the state: a written answer from CPW covering automated
retrieval, storing a transformed subset in a public repository,
redistribution, attribution, update expectations and commercial use. The
outreach draft is [cpw-outreach-draft.md](cpw-outreach-draft.md) in the
merged record; it has not been sent and is the owner's to send.

Until then: no CPW structured record is fetched into the repository, cached
or published. A CPW page may be cited as the source of a manually reviewed
claim (for example Chatfield State Park).
