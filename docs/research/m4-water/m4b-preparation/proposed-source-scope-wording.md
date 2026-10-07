# Proposed wording for the NHD source scope sentences (owner decision for M4-B)

The manifest `sources.usgs_nhd.scope` sentence of each region is shown in the
Sources dialog. M4-A kept both sentences exactly as on `main`, because M4-A
changes no wording. After M4-A the Aspen sentence is no longer accurate about
the stored data, and after M4-B neither sentence describes what is shown.
This is a wording decision for the owner; nothing here is applied.

## Current text (unchanged through M4-A)

Aspen:

`Hydrography retained for setback screening. Feature type, flow permanence and size are not carried. A name does not indicate recreational usefulness, public access or seasonal flow.`

Douglas County:

`Named waterbodies and flowlines only, selected by name. A display subset, not complete hydrology. A name does not indicate recreational usefulness, public access, fishing or paddling permission.`

## What is inaccurate

- Aspen: "Feature type, flow permanence and size are not carried" — they are
  carried from M4-A onward.
- Douglas: "Named waterbodies and flowlines only, selected by name" — from
  M4-A all waterbodies are stored; from M4-B selection is by source type
  code, not by name.

## Proposed text, for M4-B

A scope sentence states what the source does not establish. Proposed, with
the regional difference limited to what is stored:

Aspen:

`USGS National Hydrography Dataset, retired by USGS in 2023 and no longer maintained. Flowlines, areas and waterbodies with the source's type and hydrographic category; also used for setback screening. The source does not establish recreation, access or permission, or present-day flow.`

Douglas County:

`USGS National Hydrography Dataset, retired by USGS in 2023 and no longer maintained. Named flowlines and all waterbodies with the source's type and hydrographic category; not complete hydrology. The source does not establish recreation, access or permission, or present-day flow.`

## Alternatives

1. Approve the proposed sentences (recommended).
2. Minimal edit: delete only the inaccurate clause from each current sentence
   and keep the rest.
3. Keep the current sentences through M4. Not recommended: the Aspen sentence
   would state something untrue about the data.
