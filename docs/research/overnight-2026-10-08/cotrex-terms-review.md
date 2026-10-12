DRAFT - UNREVIEWED RESEARCH

# COTREX TERMS REVIEW

Mission: bounded licensing and terms review of COTREX (Colorado Parks and Wildlife) for roadmap M6. Hermes research plane, 2026-10-08. A research input only: not legal advice, not approval, no production authority. Rights readings are by a non-lawyer. Unclear stays unclear and nothing is resolved in favour of permission. No one was contacted, no agreement accepted, no account, key, form or login used. The clarification questions in section 5 are drafts and were NOT sent.

Budget used: 4 searches of 12; about 29 page or endpoint retrievals of 30. All retrievals are public GET requests; the ArcGIS items were read through the public sharing REST JSON. Retrieval times are UTC, 2026-10-08T22:49Z to 22:51Z.

## 1. Bottom line

1. The only full, controlling text found for COTREX content is the COTREX Terms & Conditions (Last Update October 25, 2018). It prohibits using, reposting, copying, distributing or publishing any Content without a separate written agreement with CPW. It also prohibits using geographic location data to create or augment any other data set, and prohibits crawling and any access other than the interfaces CPW provides.
2. CPW's public ArcGIS items carry only a warranty disclaimer and "as is" text in their licence field. They contain no grant of reuse, no open licence and no attribution rule. Nothing on any item says the app terms do or do not apply to the downloadable data.
3. The shapefile item's licence field is wildlife-map boilerplate ("This wildlife distribution map ..."), not trail-specific text. It is not a usable licence for trails.
4. The statewide basemap copy of COTREX Trails (gis.colorado.gov, layers 29 and 40) says: "Resale of this data is strictly forbidden." That is an explicit restriction on a different distribution of the same data.
5. The data.colorado.gov COTREX listing (tsn8-y22x) could not be retrieved. Its licence field has not been read. The generic data.colorado.gov Terms of Service were read, and they carry a mandatory disclaimer and a right to terminate.
6. CPW says "Responsibility for accuracy of the data rests with the source", and the compilation includes USFS, BLM, county and municipal data. The BLM copy hosted by CPW staff carries BLM's own terms (cite BLM, describe modifications, do not imply endorsement). No COTREX document says whether land-manager terms are preserved, overridden or waived.
7. Result: the intended M6 use (fetch, store, transform, group, publish derived display data, possibly in paid features) is not cleared by any COTREX text read. The app terms prohibit it as written. The open-data distributions are silent. Classification for the whole intended use: LOCKED pending the publisher.

## 2. Distributions reviewed (each recorded separately)

D1. COTREX application and website terms and privacy policy.
- Publisher: Colorado Parks and Wildlife (COTREX is a partnership with Natural Atlas, per https://trails.colorado.gov/).
- URLs: https://trails.colorado.gov/terms and https://trails.colorado.gov/privacy
- Dated: both "Last Update: October 25, 2018". Retrieved 2026-10-08T22:49:45Z (terms) and 22:49:46Z (privacy), HTTP 200, read in full.
- Also read: https://trails.colorado.gov/about (map attribution panel only), 22:49:46Z.

D2. CPWAdminData hosted feature service, layers 14 (COTREX Trailheads) and 15 (COTREX Trails).
- Publisher: CPW GIS Unit, ArcGIS Online org ttNGmDvKQA7oeDQ3, owner rsaccoCPW.
- URLs: item https://www.arcgis.com/sharing/rest/content/items/168fccb0583f42f1afe57de6c9ce846d?f=pjson (22:49:47Z); service https://services5.arcgis.com/ttNGmDvKQA7oeDQ3/arcgis/rest/services/CPWAdminData/FeatureServer?f=pjson (22:49:47Z); layer https://services5.arcgis.com/ttNGmDvKQA7oeDQ3/arcgis/rest/services/CPWAdminData/FeatureServer/15?f=pjson (22:49:48Z).
- Dated: item modified 2026-08-27T14:24:59Z. Layer 15 description says "These data were last updated on 2/5/2019", while its editingInfo dataLastEditDate is 2026-08-27T14:24:00Z. The two dates do not agree; no explanation is given.

D3. CPW Trails Shapefile Download (ZIP, about 770 MB).
- Item cae8ed959b8a4ed48680df62b31eec60, owner rsaccoCPW, public, published on the CPW Spatial Data Hub (https://geodata-cpw.hub.arcgis.com/datasets/cae8ed959b8a4ed48680df62b31eec60).
- Read through https://www.arcgis.com/sharing/rest/content/items/cae8ed959b8a4ed48680df62b31eec60?f=pjson at 22:49:47Z. Modified 2026-08-27T13:49:43Z.
- The Hub page itself is a script-rendered shell with no readable text (22:50:13Z, HTTP 200, 53 characters). I did not find terms text on it.
- Contents per the snippet: CPW designated trails plus COTREX trails and trailheads.

D4. Colorado State Basemap map service, COTREX Trailheads (layer 29) and COTREX Trails (layer 40).
- Publisher: Colorado Office of Information Technology (OIT), Colorado Geospatial Portal (https://geodata.colorado.gov/, a script shell with no readable text).
- URLs: https://gis.colorado.gov/public/rest/services/OIT/Colorado_State_Basemap/MapServer?f=pjson and .../MapServer/40?f=pjson, retrieved 22:50:12Z.
- Layer 40 description: "These data were last updated on 2/5/2019." Layer copyright text: "Colorado Parks & Wildlife GIS Unit". Service version 3.1.0.
- Only layer 40's JSON was read. Layer 29's JSON was not fetched (I saw its title in a search result only).

D5. data.colorado.gov (Colorado Information Marketplace) listing "Colorado Trail Explorer (COTREX)", id tsn8-y22x, plus the portal's Terms of Service.
- Listing: NOT RETRIEVED. The page, /api/views/tsn8-y22x.json, /api/views/metadata/v1/tsn8-y22x and the Socrata catalog API all returned not-found or empty (22:50:10Z to 22:50:26Z). Three methods failed. The listing may have been retired or moved.
- From a search result only (not the controlling text): "Permissions: Public", "Data Provided By Colorado Parks and Wildlife", links to an ESRI layer package and to Shapefile and KMZ files on the "State OIT GIS GeoPortal FTP site". I could not read any licence field or the download links.
- Portal terms, read in full: https://data.colorado.gov/terms, "TERMS OF SERVICE POLICY- STATE OF COLORADO", no date shown, retrieved 22:51:07Z. (The portal page /terms-of-use is 404; the Colorado.gov terms page returned HTTP 503 at 22:50:51Z and is NOT RETRIEVED.)

D6. CPW-internal and CPW-staff COTREX items in the same ArcGIS org (found by the public ArcGIS search, 22:50:46Z).
- COTREX_Trails_Populated_2026 (owner Stewardship_Admin, public). Snippet: "Uploaded to AGOL for the 2026 Field Season on 1/17/2026 by Faith Ruck, GIS Tech." Description: "last updated on 11/25/2024". Item modified 2026-09-22T18:04:50Z. Its licence field is the same trail-layer "as is" text as D2.
- COTREXTrails and others owned by eric.schuette_CoTrails (e.g. "Data Contributors", "COTREX Trails June 2025"). The two I read (COTREXTrails and the Data Contributors dashboard) have no licence text. They look like operational or working copies, not published distributions. I do not treat them as sources.
- Third-party copies (e.g. Lakewood eGIS "Trails COTREX", last updated 9/11/2019; Boulder County and contractor copies) exist. They are not controlling and were not read beyond a search snippet.

D7. Land-manager data carried inside COTREX.
- BLM: item BLM_External_Trails (https://www.arcgis.com/sharing/rest/content/items/d4ea82c17e8943fd84b358c722f13cb4?f=pjson, 22:51:09Z, modified 2025-08-28T19:16:27Z), access information "BLM Colorado".
- USFS: not re-read here. The project's TRAIL-PILOT.md (September 25, 2026) records USFS NFS Trails metadata with access constraints "None" and a use-constraints disclaimer. The USFS metadata was not re-fetched in this review.
- Counties and municipalities: no separate terms found.

## 3. Rights matrix

Legend: PERMITTED = explicitly permitted. PROHIBITED = explicitly prohibited. UNCLEAR = unclear or silent. Quotes follow the matrix. The ArcGIS items D2, D3 and D6 share the same kind of text; D3's licence field differs (wildlife boilerplate). "Same as D2" means the same text and classification.

| Right | D1 App terms | D2 CPWAdminData service | D3 Shapefile download | D4 OIT State Basemap | D5 data.colorado.gov (listing NOT RETRIEVED; portal TOS read) | D7 BLM/USFS source terms |
|---|---|---|---|---|---|---|
| Retrieval (fetch, bulk download, scraping, API) | PROHIBITED for anything but CPW's interfaces; crawling prohibited (Q1, Q3) | UNCLEAR: service is public with Query capability, maxRecordCount 2000; no use rules stated | UNCLEAR: published as a download; no use rules stated | UNCLEAR: public service with Query, no use rules; basemap copyright text says data is "made available" | UNCLEAR for the listing; portal TOS speaks of "data made available through this site" and a right to discontinue feeds (Q8) | BLM: UNCLEAR; no fetch rule in licence text. USFS: not re-read here |
| Storage, caching, retention | UNCLEAR beyond the copy ban ("copy ... any Content" is prohibited, Q1) | UNCLEAR | UNCLEAR | UNCLEAR; no retention rule | UNCLEAR; the State may "require the termination of any and all displaying, distributing or otherwise using" the data (Q9) | UNCLEAR |
| Transformation and derivatives (grouping, merging, augmenting another dataset) | PROHIBITED: "Use geographic location data to create or augment any other data set" (Q2) | UNCLEAR; licence field says "installation of the data ... its use" only | UNCLEAR | UNCLEAR; copyright text says the data "has been modified for use from its original source", which acknowledges modification but grants nothing | UNCLEAR; the TOS mandates a "modified for use" disclaimer in apps (Q8), implying modification is contemplated but not granted | BLM: modification contemplated, must be described (Q11) |
| Redistribution and publication of data or derivatives | PROHIBITED without a separate written agreement (Q1) | UNCLEAR | UNCLEAR | PROHIBITED for resale: "Resale of this data is strictly forbidden" (Q7); otherwise UNCLEAR | UNCLEAR; the TOS lets applications use the data if they carry the disclaimer (Q8) but does not state a licence | BLM: UNCLEAR; cite BLM (Q11) |
| Attribution | UNCLEAR for third parties; the app displays "© COTREX Contributors" and Natural Atlas credits (Q5), no rule for reusers | UNCLEAR; copyrightText "Colorado Parks and Wildlife" is a credit field, not a stated requirement | UNCLEAR | UNCLEAR as a requirement; copyright text is the State's modified-data notice | REQUIRED for applications using portal data: must carry the State's disclaimer (Q8) | BLM: "The BLM should be cited as the data source" (Q11) |
| Commercial use | PROHIBITED as part of the copy/publish ban; no separate commercial clause (Q1) | UNCLEAR | UNCLEAR | PROHIBITED for resale (Q7); other commercial use UNCLEAR | UNCLEAR | UNCLEAR |
| API or service terms, rate limits | PROHIBITED: other than provided interfaces; "undue burden" and scripting prohibited (Q3, Q4) | UNCLEAR: only maxRecordCount 2000 (technical); no rate limit or ArcGIS Online terms read | n/a (file download) | UNCLEAR: maxRecordCount 2000; no rate limit stated | UNCLEAR: no rate limit in the TOS; the State may discontinue feeds | n/a |
| Privacy or termination | Termination for any violation (Q9); privacy policy covers accounts and server logs, not data reuse | UNCLEAR | UNCLEAR | UNCLEAR | TOS: right to require termination of all displaying or using, "for any reason" (Q9) | UNCLEAR |
| Warranty or accuracy disclaimer relevant to status or closures | EXPLICIT: trail depiction is not an implication that it is "passable ... or open for general public use"; user must consult managers (Q6) | EXPLICIT: "AS IS"; "used and relied upon only at the user's sole risk"; user "agrees to indemnify and hold harmless" (Q10) | EXPLICIT (wildlife boilerplate wording, same "as is"/indemnify clauses) (Q10) | EXPLICIT: no representation as to "completeness, accuracy, timeliness" (Q7) | EXPLICIT: same (Q8) | BLM: "as is", user assumes risk (Q11) |
| Conflict with another text | The app terms say they govern "any content ... displayed on the COTREX application", including data. No text says the downloadable items are exempt | The licence field does not mention the app terms | Licence field mentions neither the app terms nor trails | "Resale" ban differs from the app terms' wider ban | Listing text unread | Land-manager terms not addressed anywhere in CPW text |

Classification of the whole intended use (fetch, store, transform, group, publish derived display data, possible paid features):
- D1: EXPLICITLY PROHIBITED.
- D2, D3, D6: UNCLEAR OR SILENT on every grant. Explicit only on warranty and risk.
- D4: UNCLEAR, with an EXPLICIT resale prohibition.
- D5: NOT RETRIEVED (listing); UNCLEAR (portal TOS, which requires a disclaimer and allows termination).
- D7: UNCLEAR for COTREX copies; BLM licence text asks for citation.

### Controlling sentences (quotes, with source and time)

Q1. D1, https://trails.colorado.gov/terms, section "Restrictions on Use", retrieved 2026-10-08T22:49:45Z, version "Last Update: October 25, 2018": "Use, repost, copy, distribute or publish any Content unless you have been given permission by Colorado Parks and Wildlife in a separate written agreement". "Content" is defined in the opening paragraph as including "text, graphics, photos, information, links, maps, data and geographical locations".

Q2. Same section: "Use geographic location data to create or augment any other data set".

Q3. Same section: "Access or search or attempt to access or search the COTREX application using any means other than the currently available interfaces that are provided by Colorado Parks and Wildlife as part of the COTREX application". Also: "Crawl any portion or access, reverse engineer, tamper with or use any non-public portion of the COTREX application".

Q4. Same section: "Interfere with or disrupt, or attempt to interfere with or disrupt the access or use of any user, host or network associated with the COTREX application, including ... by scripting the creation of Content in such a manner as to interfere with or create an undue burden on the COTREX application." Termination: "Colorado Parks and Wildlife may terminate your access to or use of the COTREX application at any time, effective immediately, for any violation of the Terms of Service."

Q5. D1, https://trails.colorado.gov/about, 22:49:46Z, map attribution panel: "© COTREX Contributors (Trail Managers across Colorado) Trails, Trailheads"; "© Natural Atlas Cartography, Recreation Points"; "© OpenStreetMap Contributors Roads, Minor Cartographic Features". This is how the app credits data. It is not a statement of what a reuser must do. The terms say the app was built with Natural Atlas, a contractor whose own terms I did not read.

Q6. D1, terms, "Disclaimer of Warranties": "The COTREX application is provided 'as is.'" and "Depiction of a road, trail or area by the COTREX application is not and should not be interpreted as an invitation to all types of travel or as an implication that the road, trail or area is passable, actively maintained, suitable or safe for travel or that the road, trail or area is open for general public use." Also the terms say the application "may also contain Content that ... infringes the intellectual property and other proprietary rights of third parties and the downloading, copying or use of which is subject to additional terms or conditions, stated or unstated." That last sentence is the closest D1 comes to the land-manager question (item 5 of the mission).

Q7. D4, MapServer?f=pjson copyrightText, retrieved 22:50:12Z: "The data made available here has been modified for use from its original source, which is the State of Colorado. The State of Colorado makes no representations or warranty as to the completeness, accuracy, timeliness, or content of any data made available through this site. ... Resale of this data is strictly forbidden." The same service describes layer 40 as "Responsibility for accuracy of the data rests with the source. These data were last updated on 2/5/2019".

Q8. D5, https://data.colorado.gov/terms, retrieved 22:51:07Z, no date shown: "Applications using data supplied by this site must include the following disclaimers on their sites: 'The data made available here has been modified for use from its original source, which is the State of Colorado. THE STATE OF COLORADO MAKES NO REPRESENTATIONS OR WARRANTY AS TO THE COMPLETENESS, ACCURACY, TIMELINESS, OR CONTENT OF ANY DATA MADE AVAILABLE THROUGH THIS SITE ...'" The terms contain no grant of rights, no named licence and no statement about commercial use. I could not confirm that the COTREX listing falls under this portal's terms, because I could not read the listing.

Q9. D5, same page: "The State of Colorado reserves the right to modify and/or discontinue providing any or all of the data feeds at any time and to require the termination of any and all displaying, distributing or otherwise using any or all of the data for any reason including, without limitation, your violation of any provision of these Terms of Service."

Q10. D2, item 168fccb0583f42f1afe57de6c9ce846d licenseInfo, retrieved 22:49:47Z: "ANY DATA OR INFORMATION PROVIDED BY THE DEPARTMENT OF NATURAL RESOURCES IS PROVIDED \"AS IS\" WITHOUT WARRANTY OF ANY KIND ... Data or information provided by the Department of Natural Resources shall be used and relied upon only at the user's sole risk, and the user agrees to indemnify and hold harmless the Department of Natural Resources, its officials, officers and employees from any liability arising out of the use of the data or information provided." The same item says "This map is a product and property of the Colorado Parks and Wildlife". Layer 15 says: "Responsibility for accuracy of the data rests with the source." D3 (item cae8ed95...) opens its licence field with "This wildlife distribution map is a product and property of Colorado Parks and Wildlife" and repeats the same disclaimer and indemnity. Its description says "Trails come from a variety of sources (USFS, BLM, local parks & recreation departments, local governments) and are compiled by CPW contractor Natural Atlas. Responsibility for accuracy of the data rests with the source." Indemnification is notable: the item text asks the user to indemnify the State. I did not assess whether that is enforceable or whether Ohvernight could accept it (a legal question).

Q11. D7, BLM_External_Trails licenseInfo, retrieved 22:51:09Z: "The BLM should be cited as the data source in any products derived from these data. Any Users wishing to modify the data should describe the types of modifications they have performed. The User should not misrepresent the data, nor imply that changes made were approved or endorsed by BLM." This applies to the BLM item as hosted by CPW staff. Whether the same terms follow BLM data inside the COTREX compilation is not stated.

Related, from CPW's Maps and GIS page (https://cpw.state.co.us/maps-and-gis, retrieved 22:50:12Z): "Data are available as individual ESRI Shapefiles in a WinZip file download or as a single group download in the ESRI Layer Package format. These same data are also available as web services streaming from the ArcGIS Online servers." and "This data allows outdoor enthusiasts, researchers, app developers and conservationists to analyze trends and make informed decisions and custom products." That text invites use but names no licence and does not mention COTREX specifically. Its stated update schedule covers administrative boundaries and species data, not COTREX. I do not read it as a licence.

## 4. Conflicts and ambiguities among the texts

- App terms versus the open data items. D1 prohibits copying, publishing and augmenting other datasets, and defines Content to include data downloaded or displayed on the app. The ArcGIS items (D2, D3) are public downloads of what appears to be the same trails compilation, with no licence that grants or denies reuse. Neither text refers to the other. The publisher does not say which controls. I cannot establish that the app terms apply to the separate download, and I cannot establish that they do not. Fail closed: treat D1's prohibitions as potentially applicable to every distribution of COTREX Content.
- Basemap copy versus others. D4 forbids resale and says nothing else; D2 and D3 are silent. These are different restrictions on the same underlying trails.
- Currency. The layer descriptions in D2 and D4 say data last updated 2/5/2019, while the item or edit metadata shows 2026-08-27. The earlier TRAIL-PILOT.md note reached the same conclusion (do not treat a refreshed service date as refreshed content). I did not sample features. The currency of the geometry therefore cannot be established from metadata alone.
- Source terms. COTREX is a compilation. CPW says accuracy rests with the sources, but gives no statement about whether the source agencies' own terms (for example BLM's citation rule) travel with the data, or whether CPW or Natural Atlas hold rights in the compilation.
- Contractor. Natural Atlas compiles the data and is credited on the map. No Natural Atlas terms were read. A contractor may hold rights in the compilation; this is unknown.
- Privacy policy (D1). It deals with account data and server logs; it does not restrict or enable data reuse. Not relevant to trails ingestion except that automated access would be logged under "the maps, trails, and other pages accessed".

Not read: Esri or ArcGIS Online terms and any service-level rate limits; the Colorado.gov website terms (HTTP 503); Natural Atlas terms; the COTREX Zendesk help centre; CPW's privacy and security statement; the data.colorado.gov COTREX listing; any signed CPW data-sharing agreement (none would be public).

## 5. Uncertainties only the publisher can resolve, with draft questions (NOT SENT)

Draft clarification questions for Colorado Parks and Wildlife (COTREX program / State Trails Program), for a human owner to review and send, if the owner chooses:

1. "The COTREX Terms & Conditions (Last Update October 25, 2018) prohibit using, reposting, copying, distributing or publishing any Content, including data, without a separate written agreement. Do these Terms apply to the COTREX trails and trailheads data published as ArcGIS Online items (the CPWAdminData feature service, layers 14 and 15, and the 'CPW Trails Shapefile Download' item), or are those distributions governed by a different licence? If a different licence applies, what is its name and where is it published?"
2. "May a small independent web application retrieve the COTREX trail and trailhead data from the public CPWAdminData feature service or the shapefile download, store it, transform it (grouping segments into named trails, merging with U.S. Forest Service and BLM data), and publish derived display data on a public website with attribution? If so, under what attribution wording and conditions?"
3. "Is commercial use permitted, in particular a free public map with later paid features, and does the answer differ for the derived display data versus the raw geometry and attributes?"
4. "The Terms prohibit using geographic location data 'to create or augment any other data set'. Does that prohibit joining COTREX trail geometry to another dataset (for example campsite or land-ownership data) in a published product, and does a written agreement exist that would permit it?"
5. "Are there rate limits, required caching intervals, or retention rules for the public feature service? Is a bulk-download refresh cadence documented, and what is the actual date of the current trail content, given the layer description 'last updated on 2/5/2019' while the item was edited in August 2026?"
6. "COTREX includes data from U.S. Forest Service, BLM, counties and municipalities. Do those land managers' own terms (for example BLM's request to be cited and to describe modifications) apply to COTREX copies, and do you hold the right to license their data to others? Does Natural Atlas hold any rights in the compiled data?"
7. "The data.colorado.gov listing 'Colorado Trail Explorer (COTREX)' (id tsn8-y22x) was not available to us. Does it still exist, what licence does it state, and does the State of Colorado data-portal Terms of Service apply to it? Does the statewide basemap statement 'Resale of this data is strictly forbidden' apply to COTREX layers 29 and 40?"
8. "Are COTREX closures, advisories and seasonal-closure records available through any licensed, documented feed, and may an application display them? Is there any warranty or statement about their currency that we should repeat?"

Why only the publisher can answer: each concerns the scope of a document the publisher wrote (Q1 of section 3), the existence of an unpublished agreement, or rights held by third parties (land managers, Natural Atlas). Another reading of the same text from our side would not change what CPW intends.

## 6. M6 source policy options

Option (a): Do not use COTREX until written permission.
- Allows: nothing from COTREX in code, data, derived data or screenshots. M6 proceeds on other sources.
- Does not allow: any COTREX ingestion, even for matching or reconciliation.
- Cost: no statewide gap-fill from COTREX; M6 coverage outside land-manager datasets is lost until permission is obtained.

Option (b): Use only a specific openly licensed COTREX distribution under its exact conditions.
- Allows: only if one is found. None exists today in what I read: no distribution carries an open licence (D2, D3, D6 have disclaimers only; D4 forbids resale; D5's licence field is unread).
- Does not allow: treating a public download, "Permissions: Public" (search-result text), or a government publisher as an open licence.
- Status: not currently available. It would become available only if the publisher names a licence (see section 7).

Option (c): Use COTREX for reference and links only, with no data ingestion.
- Allows: an outbound link to https://trails.colorado.gov/ (or to a trail's COTREX page) from a place in Ohvernight, and a plain mention of COTREX as a place to check. Linking to a page is not use of Content by the terms' wording, but whether a link containing a specific trail identifier is acceptable is a judgment for the owner.
- Does not allow: copying names, geometry, attributes, closures or counts; fetching the feature service; embedding COTREX tiles or iframes; storing identifiers harvested from the service.
- Risk: low on rights; the Terms' language "Use ... any Content" could be read to cover even citing a trail name. I treat that as unlikely for plain links, but it is an uncertainty.

Option (d): Rely on the land managers' own datasets (USFS, BLM) instead.
- Allows: use of USFS National Forest System Trails and MVUM (already in the pilot; USFS metadata records access constraints "None" with a disclaimer, per TRAIL-PILOT.md) and BLM data under BLM's stated terms (cite BLM, describe modifications, do not imply endorsement, per the BLM item text).
- Does not allow: county and municipal trails or State Parks trails not published by those managers; any COTREX-only content (for example closures shown only in the app). Each additional manager's terms need their own review. Coverage is uneven and the schema differs per agency.
- Open point: the BLM licence text I read is from a CPW-staff-hosted copy. The authoritative BLM publisher metadata should be read before use.

## 7. Recommendation

Recommend (d) with (c) as a supplement, and (a) as the standing rule for COTREX data: no COTREX data ingestion; use USFS (already in use) and BLM from their own publishers; link out to COTREX for reference only if the owner approves the wording. Do not pursue (b) unless a licence appears.

Reason: every COTREX distribution that was readable either prohibits the intended use (D1, D4 partly) or is silent on every grant while disclaiming accuracy and requiring the user to indemnify the State (D2, D3). Silence does not permit publication or the creation of derived datasets, and the app terms are explicit that they do. The mission's own rule is that absence of a prohibition is not allowance. Land managers' datasets have published terms and were already chosen for the pilot.

Evidence that would change the recommendation:
- Toward using COTREX data (option b or a written agreement): a written statement from CPW that the ArcGIS items and the shapefile are licensed for reuse (a named licence such as CC-BY or CC0, or a data-use agreement) that covers grouping, merging, publication, caching and commercial use; or a data.colorado.gov listing that states a licence; or CPW confirming that the app terms do not apply to the downloads. The attribution wording and any indemnification clause must be reviewed by the owner first.
- Toward tighter restriction (all options): CPW saying the app terms apply to all distributions, which would make (c) the ceiling.
- Toward making (d) enough: a coverage check showing that USFS and BLM data cover the M6 target areas, so COTREX adds little.
- Toward dropping (d) for BLM: BLM's own publisher metadata showing different terms than the hosted copy.

## 8. Not done, and limits

- No agreement accepted, no account, key, form, login or contact. No feature data from COTREX was queried or stored.
- Terms read in full: COTREX terms and privacy policy, data.colorado.gov Terms of Service. Read as JSON metadata only (not as rendered pages): the ArcGIS items and services. The Hub and Geospatial Portal pages are script-rendered shells and gave no text.
- NOT RETRIEVED: data.colorado.gov COTREX listing (tsn8-y22x, 3 methods plus the catalog API), Colorado.gov terms (HTTP 503), the Hub dataset page body, layer 29 JSON of the basemap, Esri terms, Natural Atlas terms.
- Search-result snippets used as leads only: the data.colorado.gov listing summary, the Lakewood copy, the Boulder reporting-lab article. They do not support any rights conclusion.
- Counts such as "about 770 MB" and "maxRecordCount 2000" come from single metadata reads and are not audited.
- Nothing in this file certifies a source as permitted, open or verified.

## 9. Index of sources and retrieval times (UTC, 2026-10-08)

- 22:49:45Z https://trails.colorado.gov/terms (200, read in full)
- 22:49:46Z https://trails.colorado.gov/about (200, attribution panel read)
- 22:49:46Z https://trails.colorado.gov/privacy (200, read in full)
- 22:49:47Z ArcGIS item cae8ed959b8a4ed48680df62b31eec60 (CPW Trails Shapefile Download)
- 22:49:47Z ArcGIS item 168fccb0583f42f1afe57de6c9ce846d (CPWAdminData) and its FeatureServer JSON
- 22:49:48Z CPWAdminData layer 15 JSON
- 22:50:10Z to 22:50:26Z data.colorado.gov tsn8-y22x page, JSON, metadata API, catalog API (all failed)
- 22:50:12Z OIT Colorado_State_Basemap MapServer and layer 40 JSON
- 22:50:12Z https://cpw.state.co.us/maps-and-gis
- 22:50:13Z CPW Spatial Data Hub pages (shells)
- 22:50:46Z ArcGIS public search for COTREX items (two queries)
- 22:50:47Z and 22:50:51Z data.colorado.gov/terms-of-use (404) and Colorado.gov terms (503)
- 22:51:07Z https://data.colorado.gov/terms (200, read in full)
- 22:51:08Z to 22:51:09Z ArcGIS items 25ba8f80..., 2189c80b..., e9f308c6..., d4ea82c1...
- Searches (4): COTREX licence/download; data.colorado.gov COTREX; State of Colorado data terms; plus the ArcGIS item searches above. Prior project context: M6 packet at docs/research/m6-trails/hermes/m6a-cotrex-usfs-identity.md and rampart-m6-m7-source-implications.md section 6, which reached the same reading from the app terms; this review adds the item-level licence texts, the basemap resale clause, the portal terms and the BLM item.
