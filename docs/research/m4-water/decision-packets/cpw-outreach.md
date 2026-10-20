# CPW outreach decision packet

**CPW's reuse terms for structured data are unclear and only CPW can settle them. Recommendation: Option A, the owner sends the drafted message; M4-D stays closed until a written answer arrives.**

## DECISION
Send the drafted request to Colorado Parks and Wildlife about reusing its structured fishing and boating data?

## EVIDENCE
Hermes read the services, item records and terms on 2026-10-06 (`docs/research/m4-water/hermes/track-f-cpw-structured-data.md`; summary in `docs/research/m4-water/cpw-status.md`). Fetching is plainly possible. Storing a transformed copy in a public repository and redistributing it is not established: the Fishing Atlas services have blank licence fields; the State's catalogue labels the Atlas "Public Domain" but that entry is a link, not the data; `CPWAdminData` says it is "for public distribution" but gives a disclaimer, not a licence; commercial use is not addressed anywhere found.

## CURRENT BEHAVIOR
No CPW structured data is fetched, stored or shown. A CPW page may be cited as the source of a manually reviewed claim. M4-D is optional and not started.

## OPTION A — owner sends the draft
The draft is `docs/research/m4-water/cpw-outreach-draft.md`: it asks about automated retrieval, storing a transformed subset, publishing derived records, attribution, update expectations and commercial use. Suggested recipients: `DNR_wildlife.cpwinfo@state.co.us` and `ndisadmin@nrel.colostate.edu`.

## OPTION B — do not send; drop M4-D
M4 completes without CPW structured data. Ramps, Gold Medal waters and special-regulation waters stay absent.

## OPTION C — send later
After M4-B and M4-C ship, with a live example to show CPW.

## TRADEOFFS
A costs one email and may take weeks. C gives a stronger request but delays the answer. B forgoes the most useful structured recreation source in the state.

## RISKS
- A refusal or silence leaves the state as it is today; nothing is lost.
- A reply that permits reuse with conditions needs those conditions written into the attribution and the data licence file before any use.
- The message identifies the project to CPW. It should come from the owner, not an agent. No agent sends it.

## RECOMMENDATION
Option A. Add one sentence offering a link to the public map once M4-B is live. M4-A, B and C are unaffected either way.

## WHAT CHANGES IF APPROVED
The owner sends one email. Nothing in the repository changes.

## WHAT REMAINS UNCHANGED
No CPW structured data is used until a written answer exists and an M4-D specification amendment is approved.

## TESTS REQUIRED
None.

## ROLLBACK
Not applicable.
