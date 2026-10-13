# NHD source-scope wording decision packet

**The Aspen source-scope sentence is inaccurate after M4-A, and neither sentence will describe M4-B's selection. Recommendation: approve Option A, the two proposed sentences, to take effect in M4-B.**

## DECISION
Which text should the two `sources.usgs_nhd.scope` sentences carry from M4-B?

## EVIDENCE
The sentence is shown in the Sources dialog for each region. M4-A kept both byte-identical to `main` and pinned them with a test, because M4-A changes no wording.

Current, Aspen: `Hydrography retained for setback screening. Feature type, flow permanence and size are not carried. A name does not indicate recreational usefulness, public access or seasonal flow.`

Current, Douglas County: `Named waterbodies and flowlines only, selected by name. A display subset, not complete hydrology. A name does not indicate recreational usefulness, public access, fishing or paddling permission.`

What is no longer true: Aspen's "Feature type, flow permanence and size are not carried" (they are, from M4-A). Douglas's "Named waterbodies and flowlines only, selected by name" (all waterbodies are stored from M4-A; selection is by source type code from M4-B).

## CURRENT BEHAVIOR
Both sentences are shown unchanged. The Aspen one understates what is stored. It overclaims nothing.

## OPTION A — proposed sentences
Aspen: `USGS National Hydrography Dataset, retired by USGS in 2023 and no longer maintained. Flowlines, areas and waterbodies with the source's type and hydrographic category; also used for setback screening. The source does not establish recreation, access or permission, or present-day flow.`

Douglas County: `USGS National Hydrography Dataset, retired by USGS in 2023 and no longer maintained. Named flowlines and all waterbodies with the source's type and hydrographic category; not complete hydrology. The source does not establish recreation, access or permission, or present-day flow.`

## OPTION B — minimal edit
Delete only the inaccurate clause from each current sentence and keep the rest.

Aspen: `Hydrography retained for setback screening. A name does not indicate recreational usefulness, public access or seasonal flow.`

Douglas County: `Named flowlines and all waterbodies. Not complete hydrology. A name does not indicate recreational usefulness, public access, fishing or paddling permission.`

## OPTION C — keep the current sentences through M4
Not recommended: the Aspen sentence would keep saying something untrue about the data.

## TRADEOFFS
A says more, including that the dataset is retired, which is honest and slightly alarming. B is shorter and says nothing about the dataset's status.

## RISKS
A scope sentence is trust text. Any change needs the owner's exact approval, and the two regions should not drift apart in meaning.

## RECOMMENDATION
Option A, applied in M4-B together with the limitation sentence already approved, with a test pinning both literals. If the South Platte decision adds an area layer to Douglas, the Douglas sentence gains "areas" and is re-approved at that point.

## WHAT CHANGES IF APPROVED
Two strings in two manifests, in M4-B. The Sources dialog shows the new text.

## WHAT REMAINS UNCHANGED
Every other manifest string; the approved WW strings; the limitation sentence.

## TESTS REQUIRED
Literal comparison of both sentences; the existing wording inventory test (no "verified", "legal", "permitted", "open to").

## ROLLBACK
Restore the two strings.
