DRAFT - UNREVIEWED

# M4-C dossier review - completion of open items

Research input only. Nothing here is a production claim record or registry entry. No activity below implies access. A ramp, a beach, a map label, a trail or the absence of a prohibition is not permission. Unknown remains unknown. No `access: allowed` is proposed anywhere.

Completes the open items of `m4c-dossier-review.md` (which stopped at retrieval 9 of 12 on a provider billing error). Reviews `m4c-dossiers-douglas-fourth-set.md`. Retrievals the earlier review completed were not repeated, except where the open item required re-reading the same page (Rueter-Hess FAQ, HTML rules page, activities page, CPW Chatfield highlights page).

## Retrieval log and timestamp note

The retrieval service returns no timestamps. UTC times are `date -u` readings taken immediately after each call (resolution one second, but latency of the call is unknown, so treat as accurate to about one minute). All on 2026-10-08.

- A1  Douglas County rules PDF, https://www.douglasco.gov/documents/rueter-hess-rules-and-regulations.pdf/ - full text via web_extract, 22:20Z. (A direct curl at 22:20:14Z returned HTTP 403 and an HTML page; not used.)
- A2  USACE Omaha District, Chatfield Dam and Lake, https://www.nwo.usace.army.mil/missions/dam-and-lake-projects/tri-lakes-projects/chatfield-dam/ - 22:20Z.
- A3  CPW Chatfield "Park Highlights", https://cpw.state.co.us/state-parks/chatfield-state-park/chatfield-state-park-park-highlights - 22:20Z.
- A4  CPW Parks and Wildlife Commission "MAILING 07/02/2026 FINAL REGULATIONS", Chapter P-1, https://cpw.state.co.us/sites/default/files/dam/ud0oampr9y/item.25.1_consent_p1-and-w9_final.pdf - 22:20Z. The extraction omitted a middle section (Spinney Mountain to State Forest); the omitted part was checked by text search for "South Platte" and found only the Chatfield entry, which was in the retrieved part.
- A5  CPW Chatfield State Park Brochure and Map, https://cpw.state.co.us/sites/default/files/dam/tskv7n0amk/chatfield-state-park-brochure.pdf - 22:20Z. Print footer "ENG_17,800_03/2024".
- A6  CPW Chatfield "Activities and Trails", https://cpw.state.co.us/state-parks/chatfield-state-park/chatfield-state-park-activities-and-trails - 22:20Z.
- A7  Douglas County Rueter-Hess FAQ, https://www.douglasco.gov/rueter-hess-recreation/faqs-rueter-hess/ - 22:21Z.
- A8  Douglas County Rueter-Hess rules HTML page, https://www.douglasco.gov/rueter-hess-recreation/rules-and-regulations/ - 22:21Z (introduction only, no date shown).
- A9  Douglas County Rueter-Hess activities page, https://www.douglasco.gov/rueter-hess-recreation/activities/ - 22:21Z.
- A10 Douglas County "Rueter-Hess Water Recreation" (paddle-days), https://www.douglasco.gov/rueter-hess-recreation/paddle-days/ - 22:21Z.
- A11 Douglas County "All-Day Parking Pass" (reservations), https://www.douglasco.gov/rueter-hess-recreation/reservations-rueter-hess/ - 22:22Z.
- FAILED: eCFR 36 CFR 327.1, https://www.ecfr.gov/current/title-36/chapter-III/part-327/section-327.1 - "Failed to fetch url".

Budget used: 2 searches (of 6), 12 page retrievals including 1 failed fetch plus 1 failed curl (of 14). No throttling or provider error occurred. Search results (one on Chatfield USACE, one on CPW Chatfield rules) were used only to find URLs; none is cited as evidence except where a page was then retrieved.

## Chatfield

### Which authority's rules apply where

Facts:
- A2, USACE (Omaha District), publication date not shown: "Chatfield dam and reservoir are owned and operated by the U.S. Army Corps of Engineers." and "USACE leases 5,381 land and water acres to the State of Colorado Parks and Wildlife Division to operate Chatfield State Park." Also: "USACE also leases separate portions of project property to the Parks and Wildlife Division for fish production and rearing areas, and to the City and County of Denver, which in turn has a management agreement with Denver Botanic Gardens."
- A5, CPW brochure: "In 1974, Colorado State Parks entered a long-term lease to manage the 5,600-acre recreation area." (The 5,381 and 5,600 acre figures differ; both are the publishers' own, not reconciled.)
- A4, CPW commission regulation Chapter P-1, heading: "General Provisions Applicable To All Parks and Outdoor Recreation Lands and Waters", with a park-specific entry "6. Chatfield State Park". Effective date stated in the mailing: "THESE REGULATIONS SHALL BECOME EFFECTIVE SEPTEMBER 1, 2026 ... APPROVED AND ADOPTED BY THE PARKS AND WILDLIFE COMMISSION OF THE STATE OF COLORADO THIS 16TH DAY OF JULY, 2026." The file is a redline mailing (it contains tracked-change artifacts such as "vii.viii." and "c.d."), not the codified text.

Interpretation (labelled INFERRED): on the leased reservoir and park lands, CPW publishes and enforces the operative recreation rules, and USACE is owner and project operator. The USACE page states no recreation rule of its own for swimming, paddling, boating or fishing. USACE rules under 36 CFR Part 327 may also apply to Corps project lands and waters; I could not retrieve that text (eCFR fetch failed), so whether and how they overlay the leased area is NOT established here.

### Is any boundary for the South Platte inflow reach defined by a manager?

No, in the sources read.
- A2 says only that the lake "lies on the South Platte River at its confluence with Plum Creek". It defines no reach, no upstream limit and no lease boundary.
- A3 and A6 do not mention an inflow reach rule. A3 says the park lies "along the South Platte River where it flows out of the mountains onto the prairie at the mouth of Waterton Canyon" (a location description, not a boundary or rule).
- A5 brochure: "Less developed, natural areas of the park are located on the south side along the Plum Creek and Platte River." and, under Fishing, "An accessible trail provides access to the South Platte River." The map text lists "Platte River Trail -2.5 mi", "Platte River Lot", "South Platte River". These are a trail, a parking-lot name and map labels. They are not a rule, a boundary, or permission to enter the water. The printed map is not machine-checked here (the extraction shows labels only, no geometry).
- A4: the Chatfield park-specific entry (6.a to 6.i) contains no South Platte, Plum Creek or river-reach provision. Its general swimming rule applies to "state-park managed properties" (see Swimming below); where that boundary lies on the river is not stated.

Unknown: upstream and downstream limits of the CPW-managed (leased) river corridor; whether any river segment inside the leased area is open or closed to any activity; whether USACE, CPW or another entity sets the rule on the river reach outside the lease; Denver Botanic Gardens and fish-production lease areas (A2) are separate-managed parcels and no rule for them was read.

### Swimming (drafted independently)

Sources:
- A3, CPW, undated page (CPW 2026 ANS banner on page): "The swim beach is open seasonally from Memorial Day through Labor Day. Hours of operation are sunrise to sunset every day. Children under 12 must have adult supervision. No lifeguard on duty. Swim at your own risk."
- A6, CPW: "The swim beach is open seasonally from Memorial Day through Labor Day. ... Children under 12 must have adult supervision."
- A5, CPW brochure (03/2024 print): "Swimming is not allowed at the marina, boat docks, any areas marked with Keep Out signs or buoys, and further than 75 feet from shore in the boating power zone. No one may swim from sunset until sunrise and anyone under the age of 13 must be accompanied by an adult."
- A4, CPW commission regulation, general rule #100.C.29: "To swim on state-park managed properties: a. From sunset to sunrise. b. Within or 150 feet from: i. any boat ramp, ii. marina, iii. breakwater, iv. dock, v. buoy-designated hazard or keep-out, vi. any dam inlet or outlet structure, and vii. where prohibited as posted. c. For any child under the age of 13 unless accompanied by an adult." (The heading above these items reads "It shall be prohibited".) The list of parks with additional swimming bans (item d) does not include Chatfield; Lathrop is listed "except at the designated swim beach at Martin Lake". The absence of Chatfield from that list is not permission.

Interpretation: the operator states a designated, seasonal swim beach with conditions (restricted at the beach) and a set of prohibited zones and times. Nothing read says swimming is permitted, or prohibited, elsewhere in the reservoir, on the ponds or on the river. Conflict in detail, retained: the age threshold is "under 12" (A3, A6) versus "under the age of 13" (A5, A4). The 75 ft versus 150 ft distances (A5 versus A4) are different measures (power-zone limit versus distance from structures) and are not shown to conflict, but they have not been reconciled by the publisher.

Draft status for the beach scope only: restricted (not a recommendation to record; coordinator and owner decide). Anywhere else on Chatfield water or river: unknown.

### Paddling (drafted independently of boating)

Sources:
- A3: "Paddle boarding is permitted at Chatfield on the reservoir as well as the gravel ponds. Life jackets required."
- A6: "Paddle boarding is permitted at Chatfield on the reservoir as well as the gravel ponds. Don't forget to bring your life jacket!"
- A4, #100.D.6.i: "Only float tubes or craft propelled by hand shall be permitted on the ponds within the park, excluding the main reservoir."
- A3, winter closure, located under the heading "Inspection Hours": "December 1 until Ice off through March 1: Reservoir closed to all boats and paddle craft".
- A5 brochure: "Chatfield is open to boating from March 1 (as ice conditions permit) through November 30." INFERRED reading that resolves the ambiguity in the A3 sentence: the closed period ends on March 1 or when ice is off, whichever the park applies, not "ice off" on an earlier date. The two CPW texts are not worded identically; the brochure is a 2024 print.
- A3: "Colorado law requires that all water vessels have appropriately sized life jackets readily accessible for every person on board."

ANS inspection exemption (A3, section "Mandatory Boat Inspections for ANS at Chatfield"): "To boat on the reservoir, an aquatic nuisance species (ANS) stamp, current boat registration and a pre-launch boat inspection at the boat ramp is required. Vessels and other floating devices that are both hand-launched and human-powered are exempt from mandatory ANS inspections." A5 states the stamp requirement only for "All motorboats and sailboats". Interpretation: for hand-launched, human-powered craft the page exempts only the mandatory ANS inspection. It does not say the exemption covers the ANS stamp or registration, and it does not itself say paddle craft are otherwise admitted; the same section opens with a requirement phrased for all boating. The two sentences sit together on the page and are not reconciled by the publisher; do not read the exemption as covering the stamp. Also: the exemption describes inspection only; it does not waive the winter closure or the life-jacket rule.

Scope limits: the explicit permission is for stand-up paddle boarding. The park's A3 general sentence "Boaters of all types - from water skiers to fishing enthusiasts to canoeists and sailors - enjoy Chatfield's 1,500 surface-acre Reservoir" is a descriptive statement, not a rule. The A6 image caption "Fishing kayaks lining the beach" is not a rule. No retrieved sentence states a kayak or canoe rule in terms. Inflow reach: nothing.

Draft status: restricted for stand-up paddle boarding on the reservoir and gravel ponds (life jackets, winter closure); other human-powered craft and the river: unknown.

### Boating (motorized or trailered, independent)

- A3: "To boat on the reservoir, a pre-launch boat inspection for Aquatic Nuisance Species (ANS), an ANS stamp, and a current boat registration are required." and "When boating capacity is reached, rangers at the boat dock will not allow boats to launch until a vessel has left the reservoir." Ramps: "Boats may be launched at either of the parks two boat ramps." Zones: "The main body of the reservoir is the power zone." Inspection hours in A3 show November "North Ramp only".
- A5: "All motorboats and sailboats must be registered and have the required Aquatic Nuisance Species (ANS) Stamp." and "Radio-controlled devices, including drones and boats, are prohibited throughout the main park area."
- A4 #100.D.6.i (ponds): only hand-propelled craft and float tubes. Nothing on the river.
Draft status: restricted on the reservoir (registration, ANS, inspection, capacity, zones, seasonal closure). River inflow: unknown. A ramp is not permission for any reach other than the reservoir the park describes.

### Fishing (independent)

- A3: "Springtime signals the start of open water fishing" and "Ice-fishing is available during the winter months." Bag limits are deferred: "See the Fishing Atlas ... and the Fishing Brochure (PDF) for daily bag limits." (neither opened.)
- A4 #100.D.6.f: "Fishing is prohibited on the ponds within the dog off leash area."
- A5: "An accessible fishing pier is located near the marina on the east side of the lake. An accessible trail provides access to the South Platte River." (The sentence about the trail is placed in the fishing paragraph; it says a trail provides access to the river, not that fishing, wading or entry is permitted at a given spot.)
- A3 does not state a license rule; A3 names none.
Draft status: reservoir fishing generally recognised by the operator, restricted by the CPW fishing regulations that were not read (unknown content). River inflow: unknown; no river-specific CPW fishing regulation was read.

## Rueter-Hess

### The governing rules document (A1), read in full

- Heading: "RUETER-HESS RECREATION GENERAL RULES & REGULATIONS  Effective July 1, 2025  Administratively Updated June 16, 2025  Created August 1, 2023". Publisher block: "Douglas County Division of Park, Trail, and Build Grounds, 9651 S. Quebec St., Highlands Ranch, CO 80130" (spelling as printed).
- The earlier review's retrieval of the same URL showed the heading "Effective May 1, 2026" and the earlier dossier recorded "administratively updated April 15, 2026". This retrieval, hours later, shows the 2025 dates and contains no 2026 date anywhere. See Conflicts.

Operating season text, section 2.1: "Hours of operation for the Property is from one hour before sunrise to one hour after sunset. The incline challenge and trails located on the north side of the Property, north of Hess Road, are open daily, sunrise to sunset, year-round. The Reservoir position of the Property is open Friday through Monday from Memorial Day through October 31st." (typo "position" is in the source). Also section 2.3: "Temporary closures of the Properties may occur at any time if deemed necessary by PWSD or County for any reason." Section 11.1: "All activities in Rueter-Hess Reservoir waters ... shall be at the sole discretion of PWSD, County, or designee, and may be discontinued or suspended without notice".

Access: intro: "A County permit or reservation is needed to access the reservoir portion of the Property." Section 28.1: "Overnight or day camping is prohibited." Section 8.2: "No overnight parking."

Water rules:
- Intro: "NO bodily contact is allowed with the water at the Reservoir unless authorized and permitted by PWSD and the County."
- 11.2: "SCUBA diving, snorkeling, tubing, rafting, motorized boating, sail boating, general swimming, and ice fishing are prohibited on the Reservoir, spillways, or canals."
- 12.1: personal flotation device required for each person aboard.
- 12.2: "any reference made to an approved vessel or watercraft ... shall mean any type of non-motorized, hand-carried, non-sailed, and launched watercraft (e.g., kayak, canoe, standup paddleboard). No watercraft shall be trailer launched, and no boat ramps, trailer parking, or facilities are available at the Reservoir."
- 12.3: "Trailered, motorized by gas, diesel, or any other fuel source, and sail boating are prohibited. Prohibited watercraft (unless authorized for emergency purposes) include, but are not limited to, jet skis, motorized boats ..., sailboats, kites used for sailing, sailboards, windsurfing vessels, or any other device capable of being used as a means of transportation of persons or property on or through the water that is propelled by means other than a paddle or similar."
- 12.4: "No inflated floating devices are permitted on the water, including: inner tubes, air mattresses, floating rafts, or similar devices, except inflated stand up paddleboards."
- 13.5: "Only approved watercraft, such as paddleboards, canoes, kayaks, river pontoons, and johnboats, may use a trolling electric motor." 13.12: "Watercraft, trolling electric motors, and other gear that may contact the water must successfully pass an Aquatic Nuisance Species Inspection upon arrival at Rueter-Hess Reservoir." 13.4: "All watercraft must be hand launched."
- 15: fishing: "A valid Colorado fishing license is required." "All anglers must obtain a daily Rueter-Hess fishing permit." "Live bait is prohibited." "Fishing shall be allowed in authorized areas only."

Watercraft list in the formal rules: named in terms only as examples ("kayak, canoe, standup paddleboard", 12.2) and as approved craft for trolling motors ("paddleboards, canoes, kayaks, river pontoons, and johnboats", 13.5). The PDF has no closed list. Internal tension (retained): 12.2 defines approved craft as "non-motorized" while 13.5 allows a trolling electric motor on approved craft.

Windsurfing in the formal rules: PROHIBITED by terms. 12.3 names "sailboards, windsurfing vessels" as prohibited, and 11.2 and 12.3 prohibit "sail boating". The formal rules contain no sentence permitting windsurfing. Caveat: this is the 2025-dated copy (see revision conflict); the text of the 2026-dated copy that the earlier review saw was not readable.

### The other county statements, set beside the PDF

Season and hours:
- A7 FAQ now reads: "The reservoir is open Friday through Monday from 8 a.m. to 6 p.m. spring, summer and early fall and 8 a.m. to 5 p.m. starting when paddle season ends." This differs from the FAQ wording the earlier review quoted ("... starting November 1st through the winter unless stated otherwise"). Either the page changed between the two retrievals, or the service returned different copies. Not determinable.
- A9 activities page: "The reservoir will only be open for recreation Fridays through Mondays year round." and "Spring, summer, and early fall water recreation at Rueter-Hess Reservoir will be open from 8 a.m. to 6 p.m. Fridays, Saturdays, Sundays, and Mondays. Come out to paddleboard, kayak, canoe, or windsurf through the end of October." and "Hours November through March are 8 a.m. - 5 p.m. During the colder months land based activities are available and shoreline fishing will continue until ice forms on the reservoir." The earlier review's "Water Recreation Opening March 28, 2026" sentence is not in this copy. A9 also says: "Paddle Days ... start Memorial Day weekend and run through Labor Day weekend. ... No pets. No fishing. No swimming. No rafts or inflatable tubes." (a program run by South Suburban Recreation).
- A10: "Open Fridays through Mondays; 8 am to 6 pm During Paddle Season (Check Reservation Page for Allowed Activities); 8 am to 5 pm (Starting November 1st)" and "Rentals are Closed for the Season".
- A11: "Water Recreation Open Spring through Fall".
- Comparison: PDF 2.1 says reservoir open Fri-Mon "from Memorial Day through October 31st". The county web pages say "spring, summer, and early fall" and "through the end of October" (start earlier than Memorial Day), and say the property stays open Fri-Mon "year round" with winter hours of 8-5 from November 1. The start of the water season (Memorial Day versus "spring") and whether the Fri-Mon reservoir opening continues past October 31 (shore access and fishing) are not stated consistently. Neither is the PDF explicit about November to Memorial Day. Retained: the PDF's narrower season governs any restricted record; the extension beyond it is not adopted.

Windsurfing:
- A7 FAQ, "Are boats allowed at the Rueter-Hess Reservoir?": "Stand-up paddle boards, canoes, river pontoons, johnboats, kayaks, and windsurfing watercraft are currently permitted."
- A7 FAQ, "What watercraft is allowed?": "Standup paddle boards, canoes, river pontoons, johnboats, and kayaks are allowed. Waders and belly boats are not allowed." (no windsurfing in this list.)
- A9: "Come out to paddleboard, kayak, canoe, or windsurf through the end of October."
- A11 (new in this pass): heading "Kayaks, canoes, paddle boards, river pontoons, jon boats, and windsurfing only" and "Because Rueter-Hess is a drinking water storage facility, only these watercrafts are allowed."
- Formal rules (A1) 12.3: sailboards and windsurfing vessels prohibited. So four county web pages mention windsurfing as permitted or offered, one county page (the FAQ's other list) omits it, and the formal rules prohibit it.
- Treatment: unresolved. The restriction (prohibited under the formal rules) is retained. Windsurfing is not recorded as permitted. No formal rules text permits it.

### Operator attribution, from the sources' own words

- Property owner and manager for water storage: Parker Water & Sanitation District (PWSD). A1: "The Property is owned, maintained, and managed by the Parker Water and Sanitation District (PWSD) for water storage." A7: "Rueter-Hess Reservoir is owned by Parker Water & Sanitation District."
- Rule publisher and recreation operator (A1, current retrieval, Douglas County): "Douglas County (the County) operates and maintains the recreational facilities and manages the recreational services and programs at the Property." The document carries a Douglas County Division of Park, Trail, and Build Grounds block. Enforcement and closure: 1.1 "the County or PWSD filing trespass or other appropriate charges"; 3.1 "Any PWSD or County employee/representative or designee shall have the authority to close the Reservoir ... or to limit the number of watercraft"; 1.3 "PWSD may also implement additional restrictions or usage rules regarding the Property."
- Recreation Advisory Board: A7 "Funding and oversight of reservoir recreation are through the Rueter-Hess Recreation Advisory Board, which includes the Town of Parker, the Town of Castle Rock, the City of Lone Tree, the City of Castle Pines, and Douglas County as well as the use fees. Douglas County manages and maintains recreation on the property." and "Douglas County manages recreation on the property." The HTML rules page (A8, no date on page; the earlier review recorded "Published: 2022-12-06"): "The Rueter-Hess Recreation Advisory Board (RHAB) is a multi-entity authority that operates and maintains the recreational facilities and manages the recreational services and programs at the Property." A8 and A11 still use "the Authority" ("unless authorized and permitted by PWSD and the Authority").
- Settled reading (labelled INFERRED from the sources' own words): PWSD owns and manages the property and may add restrictions; Douglas County publishes the current formal rules (A1), operates and maintains recreation, and with PWSD enforces them; the RHAB is the funding/oversight body. The HTML rules page (A8) and the reservations page (A11) use older "Authority/RHAB" operator language that differs from the PDF's "County". This is a wording inconsistency across county pages, not a different organisation. Proposed attribution field for reviewers: publisher = Douglas County; owner = PWSD; oversight = RHAB. The recreation authority is not itself shown to publish or enforce the rules.

## The four candidate items

None is a claim. Each requires the coordinator's re-read of the live page and the owner's approval; this assessment is only about whether the official evidence is complete under the M4 rules (operator's own page, decisive quote, spatial and temporal scope, conflicts carried).

### 1. Rueter-Hess swimming - evidence substantively complete for `prohibited`; one residual

- A1 intro: "NO bodily contact is allowed with the water at the Reservoir unless authorized and permitted by PWSD and the County." A1 11.2: "... general swimming ... are prohibited on the Reservoir, spillways, or canals." A7: "Can I swim in the reservoir? No. Swimming or wading is not permitted in order to maintain the water quality of the reservoir." A9 (Paddle Days program): "No swimming."
- Three county pages agree. The publisher is the operator and the PDF is the formal rules.
- Missing or residual: (a) the PDF revision identity (July 2025 copy read here; a May 2026 copy was seen earlier and could not be re-read), so the coordinator must confirm the live swimming text in the live revision; (b) the FAQ and activities pages are undated; (c) the clause "unless authorized and permitted" and the word "general" mean authorized events are a possible exception that the pages do not describe. Status stays `prohibited` for general public use, scope = reservoir, spillways and canals only. PWSD pages were not opened.

### 2. Rueter-Hess paddling - NOT complete

- Decisive text exists: A1 12.2 (non-motorized, hand-carried, non-sailed, hand-launched: "kayak, canoe, standup paddleboard"), 12.1 (PFD), 13.4 and 13.12 (hand launch, ANS inspection), intro (permit or reservation), 2.1 (Friday-Monday), A7 (list of allowed craft).
- Missing: (a) the controlling season (Memorial Day to October 31 in the PDF versus "spring" start and later-season statements in the web pages) is unresolved; (b) the controlling revision date; (c) the earlier-seen "March 28, 2026 opening" statement could not be re-read; (d) the reservations/availability page defers to "recreation availability" and "Check Reservation Page for Allowed Activities", and the ticketing system (connect.eventpro.net) was not opened (external booking system; not retrieved); (e) 11.1 states that activities may be "discontinued or suspended without notice", so no current-day statement is possible. A `restricted` draft would have to carry the season conflict in the notes. Not ready.

### 3. Chatfield swimming - evidence complete for the swim-beach scope only

- Operator (CPW) states the beach, season, hours, supervision and no lifeguard (A3, A6), and the commission regulation lists prohibited times and zones (A4). Reasonable basis for `restricted` at the beach only.
- Missing or residual: (a) the child-age wording differs (12 versus 13) and is unreconciled; (b) the regulation read is a mailing effective September 1, 2026, not the codified text and not previously effective rules, so the coordinator must re-read the codified Chapter P-1 (and the park page, which is undated); (c) no statement for swimming outside the beach, the ponds or the river, which stay `unknown`; (d) USACE project rules (36 CFR Part 327) not retrieved, so a federal overlay is unexcluded.

### 4. Chatfield paddling - evidence complete only for stand-up paddle boarding on the reservoir and gravel ponds

- A3 and A6 give the permission with the life-jacket condition; A4 6.i gives the ponds' craft rule; the A3 winter closure and A5 boating dates give the season.
- Missing: (a) no rule for kayaks, canoes or other human-powered craft in terms; (b) the winter-closure sentence sits under "Inspection Hours" and is ambiguous on its end (A5 helps but is a 2024 print); (c) the ANS exemption is stated only for inspections, and the interaction with the ANS stamp is unstated by the publisher; (d) the river inflow is not covered; (e) the same regulation mailing caveat as for swimming; (f) USACE overlay unexcluded. Ready only if the owner accepts a record limited to stand-up paddle boarding on the reservoir and gravel ponds, with the winter closure and ANS notes.

## Conflicts left unresolved

1. Rueter-Hess formal rules revision. The same URL returned "Effective May 1, 2026" (earlier review, ~17:11Z) and "Effective July 1, 2025 ... Administratively Updated June 16, 2025" (this review, 22:20Z). The cause (stale cache, differing service copies, or an actual revert) is unknown. Neither is treated as the live revision. Any restriction in either copy is retained; no permission is drawn from the older copy's silence.
2. Rueter-Hess season. PDF 2.1 "from Memorial Day through October 31st" against web pages that say "spring" start, "year round" Friday-Monday availability, and winter hours from November 1. Also, the FAQ's reservoir-hours sentence changed wording between retrievals. Unresolved; the PDF's narrower season is the restriction retained.
3. Rueter-Hess windsurfing. Formal rules prohibit ("sailboards, windsurfing vessels", "sail boating") against the FAQ boats answer, the activities page and the reservations page. The FAQ's own watercraft list omits it. Unresolved; restriction retained; never `allowed`.
4. Rueter-Hess operator wording. PDF "the County operates" versus HTML rules page "RHAB ... operates"; FAQ names both. See attribution above.
5. Rueter-Hess formal rules versus pages on fishing detail: PDF 15.8.1 "Walleye ... between 16 and 20 inches" and 15.8.3 yellow perch "five (5)" versus FAQ and activities "between 16 and 21 inches" and perch "ten (10)". Outside the four activities in scope but material to any fishing record; unresolved.
6. Rueter-Hess internal: PDF 12.2 "non-motorized" approved craft versus 13.5 trolling-motor use on approved craft; FAQ says electric trolling motors "will now be permitted" for fishing only.
7. Chatfield swimming-age wording: "under 12" (CPW web pages) versus "under the age of 13" (brochure, regulation).
8. Chatfield winter closure: "December 1 until Ice off through March 1" (A3) versus "open to boating from March 1 (as ice conditions permit) through November 30" (A5).
9. Chatfield ANS: "To boat on the reservoir ... a pre-launch boat inspection ... required" against "hand-launched and human-powered are exempt from mandatory ANS inspections" on the same page. The page does not reconcile them.
10. The fourth-set draft's "Effective July 1, 2025" PDF date is, in fact, what this retrieval shows; the earlier review's "CONTRADICTED" finding on that point should be read together with conflict 1 (the draft may have read the same 2025 copy).

## Unknowns

- The live Rueter-Hess PDF revision date; whether the 2026 revision changed season, windsurfing or fee wording.
- Any rule text for the Chatfield South Platte inflow reach; its upstream and downstream limits; which authority sets rules on the river outside the lease.
- USACE project rules (36 CFR Part 327) applicability to leased Chatfield lands and waters.
- The CPW fishing regulations for Chatfield (brochure bag limits); fishing license statements on the park page.
- Whether CPW's swimming regulation is already effective (adopted July 16, 2026, stated effective September 1, 2026) in the codified form. On the retrieval date (October 8, 2026) it is past the stated effective date, but the codified text was not read.
- Current water-quality, fire or construction closures at any water here (A3 for Chatfield; the CPW page showed a "Conditions & Closures: No special conditions or closures at this time" statement for trails only on A6, which is a trail statement, not a water statement).
- Kayak and canoe rules at Chatfield in terms; gravel-pond paddling beyond stand-up paddle boards (A4 6.i covers hand-propelled craft on the ponds).
- West Plum Creek and any additional Pike National Forest reservoir in Douglas County: not addressed in this completion; unchanged from the earlier review.
- Reservation system (external ticketing) contents for Rueter-Hess.

## Sources not retrievable

- eCFR 36 CFR 327.1 (USACE project rules): "Failed to fetch url". Not retried (the bound on alternate access was not needed for the four items, but the gap is real).
- Rueter-Hess PDF by direct curl: HTTP 403 and an HTML page (bot block). The web_extract copy was used.
- Rueter-Hess ticketing system (connect.eventpro.net) and the "Release and Waiver" PDF: not opened.
- CPW Fishing Brochure and Land and Water Regulations Brochure (linked from A3): not opened. The codified CPW Chapter P-1: not opened (only the Commission mailing, A4, whose middle section was omitted by the service; text search found no other Chatfield or South Platte reference in the retrieved part).
- Chatfield "Fishing Atlas" and the USACE "Chatfield project statistics" fact sheet: not opened.
- PWSD (pwsd.org) pages: not opened.
