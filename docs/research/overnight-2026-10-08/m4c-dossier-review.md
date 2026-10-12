DRAFT - UNREVIEWED RESEARCH
BLOCKED_PROVIDER: HERMES

DRAFT - UNREVIEWED RESEARCH

# M4-C DOSSIER REVIEW

Review of `docs/research/overnight-2026-10-08/m4c-dossiers-douglas-fourth-set.md` (partial draft). Research input only. Nothing here is a production claim or registry entry. No activity below implies access. Ownership, management, a ramp, a map label, stocking, or the absence of a prohibition is not permission. Unknown remains unknown.

Stop reason: the 9th retrieval attempt (USACE Chatfield Lake page) failed with a provider billing error (HTTP 402 insufficient_funds, via the web_extract provider). Work stopped there, with no retry. Retrievals used: 9 of 12 allowed (8 returned content, 1 failed). The Denver Water pages, the Gill Trail page and the Pike NF reservoir enumeration were not re-opened.

Retrieval-time note: web_extract does not return timestamps. Times below are from the system clock (`date -u`) read at the time of the calls, resolution one minute. All retrievals fall in 2026-10-08 17:11Z to about 17:13Z. Treat as approximate to a few minutes.

Retrieval log (R-numbers used below):
- R1  Douglas County, rules PDF, https://www.douglasco.gov/documents/rueter-hess-rules-and-regulations.pdf/ , ~17:11Z. Extraction was truncated (see Sources not retrievable).
- R2  Douglas County, FAQ, https://www.douglasco.gov/rueter-hess-recreation/faqs-rueter-hess/ , ~17:11Z. Full text, no page date shown.
- R3  Colorado Parks and Wildlife, https://cpw.state.co.us/state-parks/chatfield-state-park/chatfield-state-park-park-highlights , ~17:11Z. Full text.
- R4  Douglas County, HTML rules page, https://www.douglasco.gov/rueter-hess-recreation/rules-and-regulations/ , ~17:11Z. Only the introduction came back. Page metadata: "Published: 2022-12-06".
- R5  Douglas County, activities page, https://www.douglasco.gov/rueter-hess-recreation/activities/ , ~17:11Z. Partial and garbled in places, no page date shown.
- R6  Same PDF URL as R1, fetched with curl, 2026-10-08T17:11:39Z. This was a second access method, tried because R1 was truncated. It returned an HTML document, not a PDF, and was not parsed or used as evidence.
- R7  Town of Castle Rock, https://www.crgov.com/1791/Source-Water , ~17:12Z. Full text.
- R8  US Army Corps of Engineers (Omaha District), Chatfield Lake page, URL guessed, ~17:12Z. FAILED, billing error 402. No content.
- R9  USDA Forest Service, Pike-San Isabel NF, https://www.fs.usda.gov/r02/psicc/recreation/south-platte-river-corridor , ~17:12Z. Page says "Last updated May 5, 2026".

## Official evidence confirmed

Rueter-Hess (operator: Douglas County, for the Parker Water & Sanitation District property)

- R1, formal rules PDF heading: "GENERAL RULES & REGULATIONS ... Effective May 1, 2026". Only this heading and a few page fragments survived extraction.
- R2 FAQ, swimming: "No. Swimming or wading is not permitted in order to maintain the water quality of the reservoir."
- R2 FAQ, watercraft: "Standup paddle boards, canoes, river pontoons, johnboats, and kayaks are allowed. Waders and belly boats are not allowed." Also: "All watercraft must be hand launched, there is no boat ramp." "No trailers allowed on the property."
- R2 FAQ, ANS: "all watercraft, trolling electric motors, and other gear that may contact the water must successfully pass an Aquatic Nuisance Species Inspection upon arrival".
- R2 FAQ, trolling motors: "The use of electric trolling motors for non-fishing activities is prohibited." Also: "The limited use of electric trolling motors for fishing purposes will now be permitted."
- R2 FAQ, fishing: "all anglers are required to obtain a free daily fishing permit". Also: "After November 1st anglers may fish from shore until ice forms on the reservoir."
- R2 FAQ, entry: "Vehicles driving into the reservoir portion of the property need to make an online vehicle reservation".
- R2 FAQ, hours: "The reservoir is open Friday through Monday from 8 a.m. to 6 p.m. and 8 a.m. to 5 p.m. starting November 1st through the winter unless stated otherwise."
- R5 activities: "The reservoir will only be open for recreation Fridays through Mondays year round." Also: "Water Recreation Opening March 28, 2026 ... Come out to paddleboard, kayak, canoe, or windsurf through the end of October."

Chatfield State Park (publisher: CPW)

- R3, swimming: "The swim beach is open seasonally from Memorial Day through Labor Day. ... No lifeguard on duty. Swim at your own risk."
- R3, paddling: "Paddle boarding is permitted at Chatfield on the reservoir as well as the gravel ponds. Life jackets required."
- R3, boating: "To boat on the reservoir, a pre-launch boat inspection for Aquatic Nuisance Species (ANS), an ANS stamp, and a current boat registration are required." Also: "When boating capacity is reached, rangers at the boat dock will not allow boats to launch until a vessel has left the reservoir."
- R3, closure, listed under "Inspection Hours": "December 1 until Ice off through March 1: Reservoir closed to all boats and paddle craft".
- R3, fishing: "Springtime signals the start of open water fishing ..." and "Ice-fishing is available during the winter months." Bag limits are deferred to the Fishing Brochure.

South Platte corridor near Deckers (publisher: USFS, Pike-San Isabel NF, South Platte Ranger District; updated May 5, 2026)

- R9: "The confluence provides access for fishing, kayaking and trail use."
- R9: "Note: Watercraft may pass through private property but are not allowed to stop on private property."
- R9: Seasons of Use "Year-round"; Operational Hours "One hour before sunrise and one hour after sunset."; "Day use only between Pine Creek Road and Buffalo Creek and along Sugar Creek Road."
- R9: "Dispersed camping is prohibited." "Parking is permitted in designated sites only."

Castle Rock (publisher: Town of Castle Rock; source-water page)

- R7: "existing local water rights in Plum Creek that go back to the 1860s".
- R7: "The Plum Creek diversion and pump station were completed in 2021 allowing Castle Rock Water access to the water rights and imported water within East Plum Creek."
- R7: "six new alluvial wells were constructed along East Plum Creek". The page does not contain the phrase "West Plum Creek".

## Conflicts

C1. Rueter-Hess governing document date. UNRESOLVED as to the update date; the draft's effective date is CONTRADICTED.
- Draft: the PDF says "Effective July 1, 2025" and "Administratively Updated June 16, 2025".
- R1 now: "Effective May 1, 2026". The earlier dossier (`dossiers-douglas-county.md:178`, `:232`) records "effective May 1, 2026; administratively updated April 15, 2026".
- The administrative-update line did not survive extraction in R1, so April 15, 2026 is not re-confirmed here. The 2025 dates in the draft are not seen on the retrieved document. A document revision between the earlier dossier and the draft cannot be excluded. The draft gives no retrieval time, so an out-of-date cached copy is possible. Both documents are labelled "unresolved", with the restriction retained. The coordinator must open the PDF directly.

C2. Rueter-Hess operating season. UNRESOLVED; keep the restriction.
- Side A, formal PDF (as quoted by the draft and by `dossiers-douglas-county.md:239`): reservoir portion open Friday to Monday "from Memorial Day through October 31st". NOT re-confirmed by me, because the R1 extraction lost the text. It rests on the earlier dossier and the draft.
- Side B, R2 FAQ: "The reservoir is open Friday through Monday from 8 a.m. to 6 p.m. and 8 a.m. to 5 p.m. starting November 1st through the winter unless stated otherwise." R5: "The reservoir will only be open for recreation Fridays through Mondays year round." R2: "After November 1st anglers may fish from shore until ice forms".
- Interpretive note, labelled INFERRED: R5 says watercraft recreation runs "through the end of October" (from March 28, 2026). So the pages may differ on the shore and fishing season rather than the water season. This cannot be settled from the pages. Neither page is dated. The FAQ and activities pages show no date.
- The draft calls this a conflict "requiring A3 treatment". "A3" is not defined in the files I read. See Errors.

C3. Rueter-Hess windsurfing. UNRESOLVED; keep it as not established (treat as prohibited or unknown, never allowed).
- Permitting side, R2 FAQ ("Are boats allowed at the Rueter-Hess Reservoir?"): "Stand-up paddle boards, canoes, river pontoons, johnboats, kayaks, and windsurfing watercraft are currently permitted."
- Permitting side, R5 activities: "Come out to paddleboard, kayak, canoe, or windsurf through the end of October."
- Same FAQ, "What watercraft is allowed?": the list is stand-up paddle boards, canoes, river pontoons, johnboats and kayaks. Windsurfing is absent from that list. This is a second, internal inconsistency in R2.
- Prohibiting side: the formal rules are said (draft; `dossiers-douglas-county.md:238`) to prohibit sail boating, sailboards and "windsurfing vessels". NOT re-confirmed by me (R1 truncated).
- Reading: the draft's account that the FAQ permits and the formal rules prohibit is SUPPORTED for the FAQ half and for the activities page. The prohibition half is unverified here. The draft cites only the FAQ for windsurfing and omits the activities page, which also says "windsurf".

C4. Rueter-Hess operating entity, a minor inconsistency.
- Draft (quoting the PDF): "Douglas County (the County) operates and maintains the recreational facilities and manages the recreational services and programs." Not re-confirmed.
- R4 (HTML rules page, "Published: 2022-12-06"): "The Rueter-Hess Recreation Advisory Board (RHAB) is a multi-entity authority that operates and maintains the recreational facilities and manages the recreational services and programs at the Property."
- R2 FAQ: "Douglas County manages recreation on the property" and "Funding and oversight of reservoir recreation are through the Rueter-Hess Recreation Advisory Board".
- The pages name the operator differently. This is not material to any status, but the "operator" field needs a reviewer's decision.

## Unknowns

- West Plum Creek: manager, reach, bank or parcel ownership, entry points, and any fishing, boating, paddling or swimming rule. R7 mentions only Plum Creek and East Plum Creek. No other source was opened. Nothing is established.
- Chatfield inflow: no manager-defined boundary, upstream or downstream limit, or river-specific rule was found. R3 never uses the words "South Platte" or "inflow". The question of which authority's rules apply on the reach (CPW state park, federal reservoir owner, or other) is not established. The one candidate authority I tried, the USACE page (R8), was not retrieved. No source in this review states who has rule-making authority above or below the park boundary.
- Pike National Forest reservoir in Douglas County: no authoritative source I read names one. R9 says only that the Upper South Platte watershed "contains five major municipal and several smaller reservoirs", unnamed, with no county. Whether a Douglas County reservoir managed as a Pike NF recreation site exists is unknown. A negative is not established either; only that this review found no named reservoir.
- Rueter-Hess: the controlling season (C2), the controlling revision date (C1), windsurfing status (C3), the full text of the PDF.
- Chatfield: the scope of the winter closure sentence. It sits under "Inspection Hours" and reads "December 1 until Ice off through March 1". Whether "through March 1" is an end date or a date by which ice is expected off is unclear on the page. See the first Error.
- Whether any current closure or advisory (water quality, fire, construction) applies to any water here. Not checked beyond banners. R2 and R5 carry a Stage 1 fire-restriction banner (Douglas County, Aug. 20, 2026); R3 carries a Stage 2 fire-restriction banner. None is a water-activity rule.
- Waterton Canyon, Strontia Springs and Gill Trail items from the draft: not re-opened (budget and stop).

## Claims that fail closed (and why)

All four activities and access are `unknown` for each of the following. Do not write a record.
- Chatfield inflow reach of the South Platte: no boundary, no river-specific operator text. Reservoir text does not transfer (checks 2, 3 and 14 of the claim checklist). Also fails: the draft's "identity" support (see Errors).
- West Plum Creek: no operator, no reach, no rule.
- Any Pike National Forest reservoir in Douglas County: identity not established. Do not create a candidate from a name match.
- Rueter-Hess windsurfing: conflicting official statements. Keep it as not established; never `allowed`. Do not fold it into paddling.
- Rueter-Hess season as a claim: conflicting. A seasonal claim would have to name both statements, or be omitted. Retain the restriction.
- Cherry Creek at Castlewood and Plum/East Plum Creek: the draft is `unknown`. R7 confirms the Castle Rock source page is about water rights and wells, not recreation. I did not open the Castlewood page.
- Access for every water in this review: stays `unknown`. The Rueter-Hess reservation and parking-pass text and the Chatfield park hours are conditions of entry to a managed property. Whether any is a "stated access rule" that the spec allows as `restricted` (spec 9.2 rule 6) is a decision for the coordinator and owner. This review does not propose it.

## Possibly ready for later owner review

Each item is draft only. None is a claim. Each needs the coordinator's re-read of the live page and the owner's approval under spec section 9, and none implies access. I include only items where the operator's own page I read states the activity directly.

- Rueter-Hess, swimming: candidate `prohibited`. R2 (Douglas County FAQ): "No. Swimming or wading is not permitted in order to maintain the water quality of the reservoir." The formal PDF text was not re-read by me, and the FAQ is undated. The coordinator should confirm against the PDF at its current revision (C1).
- Chatfield, swimming: candidate `restricted`, designated swim beach, seasonal. R3: "The swim beach is open seasonally from Memorial Day through Labor Day." This is a reservoir-only statement. Matches the checklist's own worked example.
- Chatfield, paddling: candidate `restricted`, reservoir and gravel ponds, life jackets, and the winter closure (see Unknowns about the sentence). R3: "Paddle boarding is permitted at Chatfield on the reservoir as well as the gravel ponds. Life jackets required." The scope is stand-up paddleboarding. A statement about other hand-powered craft is not in this review.
- Rueter-Hess, paddling: candidate `restricted`, only the listed craft types, hand launch, ANS inspection, reservation for vehicles, set days and hours. R2 as quoted above. The season conflict (C2) must be written into the notes.

Not ready: Rueter-Hess boating, fishing and windsurfing (their decisive text sits in the PDF I could not read, or conflicts); every Chatfield boating and fishing item (fishing text is generic, and boating carries the ANS-exemption nuance in the Errors); everything on the South Platte corridor (no reach-specific CPW rule re-opened).

## Errors or overreach found in the reviewed draft

1. Chatfield identity "supports association with inflowing streams". UNSUPPORTED. The cited sentence (R3 "Hazards") reads "With the fluctuation of stream flows, boaters should always watch carefully for floating debris in the reservoir." It is a boating hazard note about the reservoir. It does not name the South Platte or any inflow, and does not support any association with a river reach. The draft's final result (identity unknown, blocked) is correct; its reasoning is not.
2. Chatfield "Operator or agency" section is incomplete. It states the retrieved page establishes state-park recreation. It does not note that the draft never retrieved any federal or other owner/authority page. The question "which authority's rules apply where" is left unaddressed. I could not close it either (R8 failed).
3. Chatfield boating. The draft quotes the ANS inspection requirement without the same page's exemption: "Vessels and other floating devices that are both hand-launched and human-powered are exempt from mandatory ANS inspections." This matters for paddling and should be carried in any paddling note. The draft's boating requirement is a motorized or trailered statement; the page's paddling sentence is separate. Keep them independent.
4. Chatfield closure sentence. The draft quotes "December 1 until Ice off through March 1: Reservoir closed to all boats and paddle craft" as a seasonal closure without noting it sits under "Inspection Hours", and that "through March 1" is ambiguous with "Ice off". It should not be reduced to dates.
5. Rueter-Hess effective date. CONTRADICTED. The draft says the PDF reads "Effective July 1, 2025" and "Administratively Updated June 16, 2025". R1 reads "Effective May 1, 2026". The draft gives no retrieval time. It also says "exact time NOT RETRIEVED" for every source, so the date conflict cannot be placed in time. The earlier dossier's May 1, 2026 date is the one corroborated here.
6. Rueter-Hess season. The draft's FAQ half is SUPPORTED (matches R2 closely). The PDF half ("from Memorial Day through October 31st") is UNVERIFIED by me. The draft misses R5's "Fridays through Mondays year round" and "through the end of October", which complicates the conflict (C2).
7. Windsurfing. Draft is SUPPORTED on the FAQ permitting it, but incomplete: it misses the activities-page "windsurf" sentence and the FAQ's own list that omits windsurfing. The draft's phrase "Leave unresolved pending owner review" is the right treatment.
8. Operator attribution. The draft attributes operation of recreation to Douglas County from the PDF. R4 attributes it to the Rueter-Hess Recreation Advisory Board (C4). Not verified either way against the current PDF.
9. "Time-of-day NOT RETRIEVED" for every source. The draft's source blocks have no retrieval timestamp at all, which fails the dossier format (UTC retrieval timestamp is required). The draft says the timestamp endpoint failed. A system clock was available. The excerpts that I could re-open did match, except where noted.
10. Pike NF section. The draft's conclusion (identity unknown) is SUPPORTED, but the draft cites no official page at all for the Pike NF question. It also leans on the existing Aurora Rampart dossier. I did not re-check that dossier's Douglas County placement, and the placement is worth a look, since the draft itself warns about a similarly named Rampart Reservoir elsewhere.
11. West Plum Creek. SUPPORTED as unknown. The draft's quotations of R7 are accurate. One caution: the draft opens by saying it did not establish a reach and then lists "road-crossing and adjacent-trail facts" under Access, but cites no source for any road crossing or trail on West Plum Creek. These facts are not established by anything in this review, and the sentence should not have been written as if they were.
12. Draft uses "A3" and "A1" labels (for example "A3 treatment", "A1 owner-review triage") that I could not find defined in the files I read. Not a factual error; a traceability gap.
13. The draft's "Potentially reviewable" list names "South Platte corridor day-use/private-property constraints". R9 confirms the text. But "Day use only" applies to named road segments (Pine Creek Road to Buffalo Creek, Sugar Creek Road), and "Watercraft ... not allowed to stop on private property" is not a statement that watercraft may stop on public land. It is not a basis for a paddling or access claim.

## Sources not retrievable

- Rueter-Hess formal rules PDF, full text (R1, R6): the extraction returned only the heading "Effective May 1, 2026" and page fragments (for example "13.6.1. Maximum boat length is fourteen (14) feet", "18.4. Pets are prohibited from entering the water or onto the ice at all times."). The curl fetch returned an HTML document, not the PDF, and was not used. So the season text, the windsurfing prohibition, the "Administratively Updated" line and the operator sentence were NOT re-confirmed. A second access method was tried and also failed; the PDF is marked inaccessible for this review.
- Douglas County HTML rules page (R4): only the introduction returned; no activity rules.
- USACE Chatfield Lake page (R8): the URL was a guess and the call failed with a provider billing error (402). No content. This is the stop reason.
- Any Forest Service or other page naming reservoirs in the Pike National Forest part of Douglas County: not attempted beyond R9.
- Any official page for West Plum Creek: not found or attempted beyond R7.
- Denver Water Waterton Canyon page, the Gill Trail page, the CPW Castlewood page, and the CPW fishing regulations for the South Platte reaches: not re-opened.
- PWSD Rueter-Hess pages (water quality closings): not re-opened.

## Next bounded step (for the coordinator)

Open the Rueter-Hess PDF directly (a browser, not an extraction service) and read the revision line, the season sentence, and the windsurfing sentence. Then read the USACE and CPW pages for the Chatfield boundary question. No other review step is blocked.
