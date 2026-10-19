DRAFT - UNREVIEWED

# M5 specification — evidence checked while drafting

Read-only metadata requests made on 2026-10-19 by the Claude specification
worker for [M5-land-classification.md](../../specs/M5-land-classification.md).
Four HTTP GET requests, attributes and metadata only, no geometry, nothing
ingested. Responses were kept outside the repository. Each line states only
what the response says. Nothing here interprets a licence or decides anything.

The wider research this builds on is on the unmerged `docs/research-drafts`
branch: `docs/research/m5-land/M5-preliminary-research-gate.md`,
`current-land-audit.md`, `hermes/m5-land-source-matrix.md` and
`docs/research/future-sources/source-watchlist-m5-m8.md`. Those are DRAFT /
UNREVIEWED and keep their own basis marks.

| # | Retrieved (UTC) | URL | Exact fact |
|---|---|---|---|
| E1 | 2026-10-19T23:23:26Z | `https://gis.blm.gov/arcgis/rest/services/lands/BLM_Natl_SMA_LimitedScale/MapServer/layers?f=pjson` | Layer 1, the layer the pipeline queries today, is named "Surface Management Agency" and its description reads: "This is used to enable an identify or query of all the surface management agency layers. There is no symbology enabled for performance reasons." Layers 16 and 31 of the same service are named "Private or Unknown"; layer 16's description is "Labels for the Private or Unknown lands". Both have `minScale` 36118. |
| E2 | 2026-10-19T23:23:47Z | `https://gis.blm.gov/arcgis/rest/services/lands/BLM_Natl_SMA_LimitedScale/MapServer/31/query?where=ADMIN_ST%3D%27CO%27&outFields=OBJECTID,ADMIN_AGENCY_CODE,ADMIN_ST,ADMIN_UNIT_NAME&returnGeometry=false&f=pjson` | The "Private or Unknown" layer returns exactly one Colorado row: `OBJECTID` 25, `ADMIN_AGENCY_CODE` `PVT`, `ADMIN_ST` `CO`, `ADMIN_UNIT_NAME` null. The same Colorado `PVT` row is `OBJECTID` 1069 in layer 1 (audit, [V-audit]), and `OBJECTID` 25 in layer 1 is the BLM row. `OBJECTID` therefore differs between layers of one service for the same agency-and-state row. |
| E3 | 2026-10-19T23:23:26Z | `https://gis.blm.gov/coarcgis/rest/services/lands/BLM_Colorado_Surface_Management_Agency/FeatureServer/1?f=pjson` | Renderer field `adm_manage`. Value labels: `BLM` "Bureau of Land Management"; `BIA` "Indian Reservation"; `BLM_LU` and `USFS_LU` "Bankhead-Jones Land Use Lands"; `BOR` "Bureau of Reclamation"; `DOD` "Military Reservation"; `LOCAL` "State, County, City: Areas"; `NPS` "National Park Service"; `OTHER` "Other Federal"; `PRI` "Private"; `STA` "State"; `USFS` "US Forest Service"; `USFS_NG` "National Grasslands"; `USFW` "US Fish and Wildlife Service". Copyright text "BLM, Colorado". Description: "This data set is a result of compiling differing source materials of various vintages. … Ongoing updates are made." Whether `PRI` is a residual class is not stated. |
| E4 | 2026-10-19T23:23:26Z | `https://services.arcgis.com/v01gqwM5QqNysAAi/arcgis/rest/services/Fee_Managers_PADUS/FeatureServer/0?f=pjson` | Layer name `PADUS4_1FeeManagers`. Copyright text: "U.S. Geological Survey (USGS) Gap Analysis Project (GAP), 2025, Protected Areas Database of the United States (PAD-US) 4.1: U.S. Geological Survey data release, https://doi.org/10.5066/P96WBCHS". A `Source_PAID` field is present. Coded domains: `Pub_Access` = `OA` Open Access, `RA` Restricted Access, `XA` Closed, `UK` Unknown; `Own_Type` and `Mang_Type` = `FED`, `TRIB`, `STAT`, `DIST`, `LOC`, `NGO`, `PVT` "Private", `JNT`, `UNK` "Unknown", `TERR`, `DESG` "Designation". The description says PAD-US includes "public land and voluntarily provided private protected areas" and "strives to be a complete inventory". No licence sentence is in the layer JSON. |

Not checked in this session: the "terms of use of the PAD-US Data Explorer"
that the PAD-US item text refers to (research gate, S3); the State Land
Board's official GIS publication and terms; CPW and county terms. Those stay
UNKNOWN.
