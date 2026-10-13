<!-- Hermes product research, run R1, 2026-10-06. A research INPUT kept verbatim: recommendations, not decisions. Nothing here changes the roadmap, pricing or any product commitment. -->

# Ohvernight: From Ideas to Testable Product Bets

## Bet 1 — Overnight + activity pairing

- **TARGET USER:** Colorado weekend travelers—especially couples, families, hikers, anglers, paddlers, and cyclists—who choose an activity first and need one lawful overnight option for the same trip.

- **SPECIFIC JOB:** “Given the activity I want to do, show me overnight options that plausibly work with its access point, dates, and restrictions, while telling me what has and has not been established.”

- **TRIGGER MOMENT:** The user has selected a trail, water body, or recreation site, usually several days before a weekend trip, and opens multiple tabs to answer where to sleep nearby.

- **CURRENT WORKFLOW:** **RETRIEVED —** Users find activities in COTREX or AllTrails, possible camping in Recreation.gov, The Dyrt, iOverlander, or a land map, calculate proximity in Google Maps, and then inspect agency pages for access and camping rules. The recurring app-switching workflow appears in [dispersed-camping research](https://www.reddit.com/r/camping/comments/lckxx3/best_appwebsite_for_dispersed_camping/), [hiking/camping planning](https://www.reddit.com/r/CampingandHiking/comments/15gn7rg/phone_apps_alltrails_vs_gaia_vs/), and [Colorado trip planning](https://www.reddit.com/r/coloradohikers/comments/hc0k9a/ive_never_camped_in_the_colorado_rockies_how_do_i/).

- **CURRENT APPS USED:** COTREX, AllTrails, Gaia GPS, Google Maps, Recreation.gov, The Dyrt, Campendium, iOverlander, agency websites, and sometimes satellite imagery.

- **PAIN:** **RETRIEVED —** Proximity does not establish compatible access or lawful overnight use. Users must reconcile different names, locations, dates, jurisdictions, and rules, and one unresolved road or camping claim can invalidate the pair. Public land and mapped roads do not independently prove camping permission or access, as reflected in [Forest Service MVUM guidance](https://www.fs.usda.gov/r06/siuslaw/maps-guides/motor-vehicle-use-maps) and [USFS dispersed-camping guidance](https://www.fs.usda.gov/r02/riogrande/recreation/dispersed-camping).

- **OHVERNIGHT EXPERIENCE:** **INFERRED —**  
  1. The user selects one activity or exact recreation feature, dates, overnight type, and broad vehicle class.  
  2. Ohvernight shows two or three candidate activity–overnight pairs, including the relevant trailhead, launch, or access point rather than measuring only feature-to-feature proximity.  
  3. Each pair displays overnight permission, activity permission, access legality, relevant restrictions, source freshness, and material unknowns as separate claims.  
  4. The user compares pairs and opens the authoritative evidence before adding one to a local trip list.

- **MVP:** A pilot-area “Nearby overnight options” panel for one activity type, initially water during M4 or trails after M6. It should show developed campgrounds and only reviewed dispersed options, straight-line distance or an explicitly labeled approximate travel relationship, evidence states, sources, and unknowns. It should not generate routes, claim availability, or rank unresolved options as recommended.

- **WHAT DATA IS REQUIRED:** Canonical activity and overnight identities; activity access points; overnight type; coordinates; managing authority; applicable activity and camping rules; effective dates; source and review dates; critical restrictions; and a bounded proximity or travel relationship.

- **WHAT DATA WE ALREADY HAVE:** **RETRIEVED —** Regional maps, land-management context, Forest Service road layers, trails, water data being normalized in M4, recreation sites, Recreation.gov developed-campground inventory, a small reviewed rule set, source metadata, source-fetched dates, and an evidence model that can represent “not established.”

- **WHAT DATA WE LACK:** **UNKNOWN —** Complete water permission and launch relationships, canonical land-manager identities, COTREX trail normalization, broad camping and dispersed-camping permission coverage, reliable route travel times, current availability, complete seasonal rules, and sufficient reviewed options to avoid presenting a misleadingly narrow result set.

- **WHY USER MIGHT PAY:** **INFERRED —** Payment is plausible for reduced research work, multi-option comparison, saved pairs, larger search areas, multi-activity planning, monitoring, and offline packaging. Payment for the underlying public rules or simple proximity is weak. Planning-payment precedents include [Roadtrippers](https://roadtrippers.com/membership/) and [The Dyrt](https://thedyrt.com/pro).

- **WHAT WOULD MAKE THEM CANCEL:** Too few candidate pairs; results that still require the same number of external apps; inaccurate feature matching; unexplained omissions; “nearby” options that are not practically connected; or any case in which Ohvernight implied permission that the linked source did not establish.

- **COMPETITORS:** COTREX and AllTrails are closest on activity discovery; Recreation.gov and The Dyrt on overnight inventory; onX Backcountry on land, trails, and dispersed-camping context; Roadtrippers on trip construction. None of the reviewed products consistently centers an inspectable, authority-backed relationship between a selected activity and a lawful overnight option.

- **DEFENSIBILITY:** **INFERRED —** The interface and distance calculation are easy to copy. The defensible asset is the normalized identity and evidence graph connecting an activity, its access points, connecting roads, land managers, overnight options, rules, dates, restrictions, and source history.

- **TRUST RISK:** A nearby overnight option may be interpreted as accessible, lawful, available, or endorsed. **Guardrail:** Never promote proximity into a permission or access claim. Block established-prohibited options, separate critical unknowns from positive results, disclose whether distance is straight-line or routed, and show each source-backed claim independently.

- **BUILD COMPLEXITY:** **Medium.** The hardest part is resolving reliable activity-access-overnight relationships and rule applicability, not calculating proximity.

- **SMALLEST VALIDATION EXPERIMENT:** In under two weeks, recruit ten people planning real pilot-area trips. Manually provide each person with two evidence-linked activity–overnight pairs using a standard template. Record their original workflow, external apps still consulted, rejected pairs, and reasons for rejection. Do not describe the service as comprehensive.

- **SUCCESS METRIC:** Pass if at least **7 of 10** participants select one supplied pair as a serious plan candidate and the median number of external products consulted falls by at least **two**, without any participant mistaking proximity for established permission in the comprehension check.

- **ROADMAP FIT:** **INFERRED —** Primarily M8, with a narrow M4 water prototype possible. M4 supplies water-body and access claims; M5 supplies canonical management units; M6 supplies trail/access relationships; M7 supplies developed and dispersed overnight permission. This refines M8’s candidate-plan output and depends on those milestones rather than replacing them.

## Bet 2 — Evidence-backed access confidence

- **TARGET USER:** A dispersed camper, paddler, angler, or remote-trail visitor evaluating a location where public-land shading, a road line, a launch symbol, or a community pin does not establish legal use.

- **SPECIFIC JOB:** “Show exactly what authoritative evidence establishes about access and permission, what is conditional or conflicting, and what remains unknown.”

- **TRIGGER MOMENT:** The user opens a candidate destination card and asks whether they may legally reach it, perform the selected activity, and stay overnight there.

- **CURRENT WORKFLOW:** **RETRIEVED —** Users inspect land maps and community reports, then cross-check MVUMs, agency recreation pages, local orders, campground pages, and sometimes ranger guidance. The distinction between road designation and camping permission is documented by [Forest Service MVUM guidance](https://www.fs.usda.gov/r06/siuslaw/maps-guides/motor-vehicle-use-maps), [Rio Grande National Forest dispersed-camping guidance](https://www.fs.usda.gov/r02/riogrande/recreation/dispersed-camping), and [user verification behavior](https://www.reddit.com/r/overlanding/comments/1pinjb2/how_do_you_know_where_you_can_camp/).

- **CURRENT APPS USED:** onX, Gaia GPS, Avenza or downloaded MVUMs, Google Maps, The Dyrt, iOverlander, Recreation.gov, COTREX, and agency websites.

- **PAIN:** Land ownership, route designation, physical passability, activity permission, and overnight permission are different questions, but most tools visually compress them. Users must interpret legal language and determine whether a source applies to the exact place and date.

- **OHVERNIGHT EXPERIENCE:** **INFERRED —**  
  1. The user opens an overnight option, activity access point, or connecting road.  
  2. Ohvernight displays separate claims for activity permission, overnight permission, legal route designation, temporary restrictions, and physical-condition evidence.  
  3. Each claim carries a state—established permitted, established prohibited, conditional, conflicting, stale, or not established—plus authority, scope, effective date, and source.  
  4. The user opens the source or chooses another candidate when a critical claim remains unresolved.

- **MVP:** Apply a fixed evidence-state vocabulary to 20–30 reviewed pilot-area features. Include the source, authority, claim scope, effective date when available, review date, and plain-language reason for the state. Avoid a numeric confidence score and do not label a result “verified” without testing how users interpret that word.

- **WHAT DATA IS REQUIRED:** Stable feature and claim identities; authoritative source URLs; source type; issuing authority; geographic and activity scope; effective and expiration dates; retrieval and human-review dates; extracted rule statement; conflict links; and evidence-state rules.

- **WHAT DATA WE ALREADY HAVE:** **RETRIEVED —** Ohvernight already requires authoritative support for access and permission claims, retains per-layer sources and source-fetched information, has a small reviewed rule set, and supports honest “not established” states. Existing regional roads, land context, trails, water, recreation sites, and campgrounds provide features against which the model can be tested.

- **WHAT DATA WE LACK:** **UNKNOWN —** A complete canonical claim schema; consistent management-unit identities; normalized rule scope; source authority hierarchy; conflict-resolution policy; expiration and supersession tracking; tested consumer vocabulary; and broad reviewed coverage.

- **WHY USER MIGHT PAY:** **INFERRED —** The direct case for paying only for provenance is weak. Users may pay when the evidence model reduces manual verification through comparison, monitoring, exports, offline packets, or professional workflows. Basic restrictions, prohibitions, source links, and safety information should remain free.

- **WHAT WOULD MAKE THEM CANCEL:** Evidence states that are difficult to understand; recent-looking timestamps that imply current conditions; sources that do not apply to the exact feature; frequent “not established” results with no planning utility; or one false-positive permission claim.

- **COMPETITORS:** onX is closest on land and road context; COTREX on official Colorado trail use and closures; Recreation.gov on official federal inventory; CalTopo and Gaia on source layers. Ohvernight’s proposed distinction is claim-level provenance and explicit unresolved states across activity, access, and overnight use rather than another map overlay.

- **DEFENSIBILITY:** **INFERRED —** Strong if maintained. Stable claim identities, authority and scope normalization, conflict history, source-review history, and links among features accumulate into a provenance graph that cannot be reproduced by copying the interface.

- **TRUST RISK:** “Confidence” can sound like a guarantee of legality, passability, or safety. **Guardrail:** Prefer descriptive evidence states over one score; show the decisive source and scope; keep legal designation separate from observed condition; use “not established” for missing evidence; and never let community observations establish permission.

- **BUILD COMPLEXITY:** **Medium.** The hardest part is determining source applicability and handling conflicting or superseded rules, not rendering the evidence card.

- **SMALLEST VALIDATION EXPERIMENT:** Build two clickable card variants for ten real pilot-area examples: one using concise evidence states and one using conventional map labels. Test with 12 participants using questions that distinguish public ownership, legal access, physical passability, activity permission, and overnight permission.

- **SUCCESS METRIC:** Pass if at least **10 of 12** participants correctly answer at least **four of five** comprehension questions using the evidence-state version, and no more than **one** interprets “not established” as permitted.

- **ROADMAP FIT:** **INFERRED —** Cross-cutting foundation for M4–M8. M4 can test activity- and launch-level water claims; M5 establishes land-manager identity; M6 applies the model to trail uses and closures; M7 makes it central to camping permission; M8 consumes the states in ranking and comparison. It is a prerequisite capability, not necessarily a separate milestone.

## Bet 3 — Freshness / “when was this checked?”

- **TARGET USER:** A user planning dispersed camping, a shoulder-season trip, or a remote activity where closures, fire rules, road conditions, launch status, and operating dates may have changed.

- **SPECIFIC JOB:** “Tell me when the exact source behind this claim was checked, what period the claim covers, and whether I need to recheck it before departure.”

- **TRIGGER MOMENT:** The user evaluates a destination several days or weeks after saving it, or conducts a final review the evening before leaving.

- **CURRENT WORKFLOW:** **RETRIEVED —** Users examine review dates, reopen agency pages, search for newer alerts, and compare multiple restriction sites. Staleness complaints appear in [campsite-app discussion](https://www.reddit.com/r/camping/comments/1btql1i/campsite_app/) and [iOverlander replacement discussion](https://www.reddit.com/r/vandwellers/comments/1ku0nn7/ok_so_what_do_yall_use_now_that_ioverlander_sucks/); changing official restrictions appear through [Colorado DFPC](https://dfpc.colorado.gov/sections/wildfire-information-center/fire-restriction-information) and [BLM Colorado](https://www.blm.gov/programs/fire/regional-info/colorado/fire-restrictions).

- **CURRENT APPS USED:** Agency alert pages, DFPC, BLM and Forest Service pages, COTREX, Recreation.gov, The Dyrt, Campendium, iOverlander, AllTrails, and saved browser tabs.

- **PAIN:** A recent page retrieval does not prove that a road, fire restriction, launch, or real-world condition was recently verified. Different claims age at different rates, and most products expose either a generic update date or a community-review date without clarifying what changed.

- **OHVERNIGHT EXPERIENCE:** **INFERRED —**  
  1. The user opens a claim or saved candidate and sees both its effective date and the date Ohvernight last checked the source.  
  2. Ohvernight labels the claim current within its review policy, due for recheck, stale, source unavailable, or superseded.  
  3. The interface explains whether the timestamp applies to a legal rule, agency status, inventory record, or physical observation.  
  4. Before departure, the user receives an on-screen recheck list for time-sensitive or unavailable evidence.

- **MVP:** Add source-checked date, effective date where available, evidence class, and a manually assigned recheck interval to the existing reviewed rules and a small set of M4 water claims. Display “source checked” rather than “condition verified.” A static pre-departure recheck panel is sufficient; automated alerts are not required.

- **WHAT DATA IS REQUIRED:** Durable claim and source identities; retrieval and human-review timestamps; source publication and effective dates; expected update cadence; stale thresholds by claim type; supersession relationships; source-fetch failures; and user-facing freshness language.

- **WHAT DATA WE ALREADY HAVE:** **RETRIEVED —** Per-layer sources, source-fetched information, reviewed rules, and an evidence model. These provide a base for displaying when evidence was obtained and differentiating established claims from unknowns.

- **WHAT DATA WE LACK:** **UNKNOWN —** Claim-level rather than layer-level timestamps; source-specific change history; expected-cadence policies; reliable effective-date extraction; automated source checks; failure logging; supersession handling; and validated thresholds for when each evidence class becomes stale.

- **WHY USER MIGHT PAY:** **INFERRED —** A date label alone is not a strong paid product. Users may pay for automatic rechecks, change history, saved-plan monitoring, offline refreshes, and a pre-departure evidence audit. Basic dates, stale warnings, and restrictions should remain free.

- **WHAT WOULD MAKE THEM CANCEL:** A fresh-looking timestamp attached only to page retrieval; unnoticed source failures; repeated false alarms; stale thresholds that do not reflect the evidence type; or discovering that Ohvernight showed an old rule as current.

- **COMPETITORS:** AllTrails, The Dyrt, Campendium, and iOverlander expose review or report recency; agencies publish current notices; COTREX carries official trail information. Ohvernight would be closer to a claim-monitoring system by distinguishing effective date, source-check date, observation date, and unknown real-world condition.

- **DEFENSIBILITY:** **INFERRED —** Source-specific monitoring history compounds. Over time, Ohvernight can learn publication cadence, recurring failures, replacement URLs, supersession patterns, and which claims require manual review.

- **TRUST RISK:** Users may interpret “checked today” as “open and safe today.” **Guardrail:** Always complete the phrase—“source checked,” “rule effective,” or “observation made.” Never use one generic freshness badge, and never infer current real-world condition solely from a successful page retrieval.

- **BUILD COMPLEXITY:** **Medium.** The hardest part is defining and maintaining different freshness semantics and review cadences across heterogeneous sources.

- **SMALLEST VALIDATION EXPERIMENT:** Add freshness labels manually to 15 real claims and show three variants to 12 participants: timestamp only, timestamp plus evidence class, and timestamp plus evidence class and recheck instruction. Test what each participant believes was actually checked.

- **SUCCESS METRIC:** Pass if at least **10 of 12** participants viewing the full version correctly distinguish “source checked” from “condition verified,” and at least **8 of 12** identify the correct claims requiring a pre-departure recheck.

- **ROADMAP FIT:** **INFERRED —** Cross-cutting M4–M8 capability. M4 can establish the metadata and language; M5–M7 should preserve it as land, trail, and camping claims are added; M8 can use it in candidate comparison and recheck workflows. Automated monitoring is a later extension, not a prerequisite for showing honest timestamps.

## Bet 4 — Adventure matching

- **TARGET USER:** A visiting family or Colorado weekend traveler with fixed dates, two or more desired activities, a known vehicle, and a preference for developed or dispersed overnight use.

- **SPECIFIC JOB:** “Given my activities, dates, vehicle, overnight preferences, and tolerance for unresolved evidence, rank the trip candidates that satisfy the most important constraints.”

- **TRIGGER MOMENT:** The user knows the kind of weekend they want but has not chosen a destination—for example, “paddle and hike next weekend with two children and a crossover.”

- **CURRENT WORKFLOW:** **RETRIEVED —** Users translate the trip concept into separate searches across activity apps, camping databases, land maps, reservation systems, general maps, and agency pages. This fragmentation recurs in [camping-app discussion](https://www.reddit.com/r/camping/comments/17r9jj7/i_would_like_to_learn_about_useful_apps_and/), [AllTrails/Gaia workflow](https://www.reddit.com/r/CampingandHiking/comments/15gn7rg/phone_apps_alltrails_vs_gaia_vs/), and [Colorado planning discussion](https://www.reddit.com/r/coloradohikers/comments/hc0k9a/ive_never_camped_in_the_colorado_rockies_how_do_i/).

- **CURRENT APPS USED:** AllTrails, COTREX, CPW pages, Recreation.gov, The Dyrt, onX, Gaia GPS, Google Maps, Roadtrippers, weather products, and land-manager pages.

- **PAIN:** Every app uses different entities and filters. Users cannot readily compare complete candidate plans, and conventional recommendation systems may rank an attractive option despite unresolved permission, access, or restriction claims.

- **OHVERNIGHT EXPERIENCE:** **INFERRED —**  
  1. The user selects activities, dates, overnight style, vehicle class, acceptable distance, and whether critical unknowns should exclude a result.  
  2. Ohvernight returns a small set of candidate plans rather than isolated pins.  
  3. Each candidate explains its activity fit, overnight fit, supporting evidence, restrictions, freshness, and the exact reason it ranked above or below another candidate.  
  4. Established prohibitions are excluded, while unresolved critical claims appear in a separate “needs verification” group rather than being silently down-ranked.

- **MVP:** A manually curated or rules-based matcher for one pilot region, one overnight, and one or two activity classes. Use no behavioral personalization or generative itinerary construction. Rank only on explicit constraints and evidence states, with a maximum of three explained candidates.

- **WHAT DATA IS REQUIRED:** Normalized activities and access points; overnight inventory and permission; dates and seasonal rules; vehicle constraints; land managers; roads; restriction applicability; source freshness; distances or travel times; user constraint schema; and an auditable ranking policy.

- **WHAT DATA WE ALREADY HAVE:** **RETRIEVED —** Regional activity and overnight layers, roads, trails, recreation sites, developed campground inventory, land-management context, reviewed rules, source metadata, and an evidence model. These can support a narrow manually curated prototype.

- **WHAT DATA WE LACK:** **UNKNOWN —** Complete M4 water normalization, M5 canonical management units, M6 COTREX identities and allowed uses, M7 camping permission coverage, dependable vehicle evidence, availability, routing, statewide candidate density, and validated rules for which unknowns should block ranking.

- **WHY USER MIGHT PAY:** **INFERRED —** Advanced matching could reduce planning time and app switching, particularly for fixed-date visitors and multi-activity trips. Paid value is more plausible for multi-activity combinations, comparison sets, saved plans, monitoring, and multi-day use than for a basic filter form.

- **WHAT WOULD MAKE THEM CANCEL:** Generic or repetitive suggestions; attractive candidates that fail a basic legal or practical constraint; unexplained ranking; inadequate regional coverage; or a need to repeat the complete research process elsewhere.

- **COMPETITORS:** Roadtrippers is closest on itinerary planning; The Dyrt on campground-oriented trip planning; onX on land and vehicle context; AllTrails and COTREX on activities. The proposed distinction is evidence-aware matching across activities and overnight options rather than engagement- or popularity-led recommendations.

- **DEFENSIBILITY:** **INFERRED —** The algorithm is not the moat. Defensibility comes from normalized cross-domain identities, permission and restriction applicability, source history, and a transparent ranking policy grounded in Ohvernight’s evidence graph.

- **TRUST RISK:** Ranking can be mistaken for endorsement, legality, availability, or safety. **Guardrail:** Established prohibitions must block candidates; unresolved critical claims must not be disguised by a high aggregate score; ranking reasons and omissions must be inspectable; and safety-sensitive options must never be promoted for engagement.

- **BUILD COMPLEXITY:** **High.** The hardest part is defining a ranking policy that combines incomplete cross-domain evidence without allowing favorable factors to cancel a critical prohibition or unknown.

- **SMALLEST VALIDATION EXPERIMENT:** Run a concierge matcher for ten participants with real pilot-area trip briefs. Produce up to three manually ranked candidate plans using a fixed rubric, then reveal the ranking reasons and ask participants to compare them with their self-researched choices.

- **SUCCESS METRIC:** Pass if at least **7 of 10** participants place an Ohvernight candidate in their top two choices, at least **6 of 10** report saving an hour or more of planning work, and **zero** select a candidate after misunderstanding a critical unknown as established.

- **ROADMAP FIT:** **INFERRED —** Directly belongs with M8 and should consume—not bypass—M4–M7 evidence. Prerequisites are stable candidate pairing, management-unit and feature identities, overnight permission states, date applicability, and a tested critical-unknown policy. It does not require full multi-day generation for its first useful form.

## Bet 5 — Saved-trip monitoring

- **TARGET USER:** A traveler with a trip planned days or weeks in advance—especially a reservation holder, remote driver, paddler, family, or visitor with fixed dates and limited ability to improvise.

- **SPECIFIC JOB:** “Keep checking the authoritative sources that apply to my exact trip and tell me when a relevant claim changes, becomes stale, conflicts, or can no longer be checked.”

- **TRIGGER MOMENT:** Immediately after the user commits to a candidate plan and during the period before departure, with the highest need in the final 24–72 hours.

- **CURRENT WORKFLOW:** **RETRIEVED —** Users save links or rely on memory, then revisit county, Forest Service, BLM, CPW, reservation, road, and fire pages. Relevant sources include [Colorado DFPC](https://dfpc.colorado.gov/sections/wildfire-information-center/fire-restriction-information), [BLM Colorado fire restrictions](https://www.blm.gov/programs/fire/regional-info/colorado/fire-restrictions), and destination-specific alerts.

- **CURRENT APPS USED:** Browser bookmarks, calendar reminders, email reservation notices, Recreation.gov, COTREX, COtrip, weather apps, DFPC, BLM and Forest Service alert pages, The Dyrt, and Campendium.

- **PAIN:** A trip is a dependency graph, but users monitor it as disconnected pages. **RETRIEVED —** Detectable failures include published road or seasonal closures, fire restrictions, trail closures, permits, timed-entry requirements, water-access closures, reservation changes, and some facility outages. Partially or non-detectable failures include exact road passability, dispersed-site occupancy, parking availability, localized weather, current cell service, and undocumented gates. Sources include [White River road alerts](https://www.fs.usda.gov/r02/whiteriver/alerts/fsr-286-radical-hill-closed-due-washouts-and-unsafe-conditions), [RMNP road status](https://www.nps.gov/romo/planyourvisit/road_status.htm), [CPW camping](https://cpw.state.co.us/camping), and [Forest Service planning guidance](https://www.fs.usda.gov/r02/arp/safety-ethics).

- **OHVERNIGHT EXPERIENCE:** **INFERRED —**  
  1. The user saves a candidate plan and sees the exact claims and sources Ohvernight can monitor.  
  2. A monitoring panel distinguishes active coverage, manual-recheck items, unsupported sources, and inherently unknowable conditions.  
  3. When a source changes or cannot be checked, Ohvernight explains which activity, road, restriction, or overnight component may be affected.  
  4. Before departure, the user receives a dated status report containing changes, unchanged monitored claims, coverage gaps, and required manual checks.

- **MVP:** A manual monitoring concierge for ten saved trips. Monitor a declared set of official pages covering published closures, fire restrictions, reservations or permits, and named recreation-site status. Deliver reports only inside the research trial or through an agreed research channel; do not imply exhaustive or real-time coverage. No automated alternate recommendations are required.

- **WHAT DATA IS REQUIRED:** A stable saved-trip object; exact activities, access points, roads, overnight options, dates, and jurisdictions; trip-to-claim and claim-to-source relationships; source-check cadence; change detection; fetch-failure states; applicability rules; and notification audit history.

- **WHAT DATA WE ALREADY HAVE:** **RETRIEVED —** A simple local saved list, per-layer source information, source-fetched metadata, regional features, developed campground inventory, reviewed rules, and an evidence model. The failure taxonomy supplies an initial distinction between detectable, partially detectable, and unknowable conditions.

- **WHAT DATA WE LACK:** **UNKNOWN —** Accounts or portable saved trips, notification delivery, automated source polling, broad current closure feeds, fire applicability by exact jurisdiction, reservation-change access, weather and road feeds, source-failure handling, complete trip dependency mapping, and measured expectations about monitoring frequency.

- **WHY USER MIGHT PAY:** **INFERRED —** Monitoring provides recurring value between planning and departure and can help avoid travel to a known closure or missed permit requirement. Alerts and planning are established premium patterns in [The Dyrt](https://thedyrt.com/pro) and [Campendium](https://campendium.com/rvpro/), but willingness to pay for Ohvernight’s version remains **UNKNOWN**.

- **WHAT WOULD MAKE THEM CANCEL:** A missed high-impact published change; irrelevant alert volume; duplicate notices; reports that lack actionable trip impact; unexplained monitoring outages; or discovering that silence meant a source failed rather than that nothing changed.

- **COMPETITORS:** The Dyrt and Campendium are closest on paid alerts; Recreation.gov provides reservation communications; COTREX and agencies provide domain-specific closures; weather and road apps monitor individual hazard classes. Ohvernight’s potential distinction is monitoring the exact cross-domain claims supporting one saved trip.

- **DEFENSIBILITY:** **INFERRED —** The notification mechanism is copyable. The defensible asset is the trip-to-feature-to-jurisdiction-to-source dependency graph, together with accumulated change history, source cadence, source failures, and coverage knowledge.

- **TRUST RISK:** Silence may be interpreted as “the trip is unchanged and safe.” **Guardrail:** Every report must show the last successful check, monitored coverage, unavailable sources, unsupported failure modes, and a statement that absence of a detected change does not establish current access, passability, capacity, weather, or safety.

- **BUILD COMPLEXITY:** **High.** The hardest part is reliable spatial and legal applicability across heterogeneous sources while detecting and exposing source failure.

- **SMALLEST VALIDATION EXPERIMENT:** For up to ten real trips departing within two weeks, manually monitor a declared set of official sources and issue an initial coverage statement plus two scheduled status reports. Include at least one simulated source outage to test whether users understand silence and monitoring gaps.

- **SUCCESS METRIC:** Pass if at least **7 of 10** participants say they would enable monitoring for their next comparable trip, at least **5 of 10** express concrete willingness to pay for continued monitoring, and **10 of 10** correctly understand that no alert does not guarantee no change.

- **ROADMAP FIT:** **INFERRED —** Best tested after M7 or alongside M8 once a candidate plan has stable feature and claim identities. Freshness infrastructure can begin in M4–M7. Full monitoring requires saved trips, source operations, and notification delivery that do not currently exist.

## Bet 6 — Trip feasibility dashboard

- **TARGET USER:** A weekend traveler making a near-term go/no-go decision or comparing two destinations, especially in shoulder season, during fire season, or when the trip depends on a remote road or limited-capacity overnight option.

- **SPECIFIC JOB:** “Put the trip’s decisive constraints on one screen so I can identify what is established, what has failed, what needs rechecking, and what cannot be known in advance.”

- **TRIGGER MOMENT:** The evening before departure, the morning of travel, or when choosing between final candidate destinations.

- **CURRENT WORKFLOW:** **RETRIEVED —** Users separately check overnight status, road and seasonal closures, permits, trail status, fire restrictions, weather, snow, water access, amenities, and source dates. The workflow spans [Forest Service planning guidance](https://www.fs.usda.gov/r02/arp/safety-ethics), [NOHRSC](https://www.nohrsc.noaa.gov/interactive/html/map.html), [Colorado DFPC](https://dfpc.colorado.gov/sections/wildfire-information-center/fire-restriction-information), [RMNP road status](https://www.nps.gov/romo/planyourvisit/road_status.htm), and [Recreation.gov](https://www.recreation.gov/mobile-app/).

- **CURRENT APPS USED:** Ohvernight or land maps, Recreation.gov, COTREX or AllTrails, COtrip, weather apps, NOHRSC, AirNow or Colorado air-quality tools, DFPC, agency alert pages, and Google Maps.

- **PAIN:** A favorable status in one domain can hide a trip-blocking failure elsewhere. **RETRIEVED —** High-value pre-trip warnings are possible for published closures, seasonal gates, fire restrictions, permits, timed entry, some road incidents, waterbody closures, and facility outages. Only partial warnings are possible for vehicle passability, trail surface, dispersed occupancy, parking, smoke at a remote location, localized storms, cell service, and undocumented access changes. The planning tool cannot establish that a trip is safe or guaranteed.

- **OHVERNIGHT EXPERIENCE:** **INFERRED —**  
  1. The user opens a saved candidate and sees a checklist covering overnight permission, activity permission, access legality, published closures, reservations, fire status, road evidence, water or trail status, amenities, and freshness.  
  2. Each item is classified as established, conditional, changed, stale, conflicting, not established, or inherently uncertain.  
  3. A “trip blockers” section surfaces prohibitions, missing required permits, and known closures without allowing favorable items to offset them.  
  4. A “check before leaving” section lists forecasts, capacity, passability, and other conditions that cannot be conclusively established.

- **MVP:** A read-only dashboard for five to ten manually assembled pilot-area trips using existing Ohvernight evidence plus links to authoritative external checks. It should contain no universal feasibility percentage, “safe” label, automated weather integration, or claim that every relevant source has been checked.

- **WHAT DATA IS REQUIRED:** A stable trip object; activity and overnight permission; access routes; dates; reservations and required permits; applicable closures and restrictions; source freshness; vehicle constraints; weather, snow, smoke, and road context where licensed and available; facility status; and critical-claim definitions.

- **WHAT DATA WE ALREADY HAVE:** **RETRIEVED —** Regional map layers, roads, trails, water, recreation sites, developed campground inventory, land-management context, a small reviewed rule set, source metadata, and explicit unknown states. The failure taxonomy identifies which checks are likely to be decisive and which cannot be resolved before departure.

- **WHAT DATA WE LACK:** **UNKNOWN —** Weather, fire, smoke, road-condition, closure, and reservation feeds; complete camping permission; route-to-destination relationships; source monitoring; vehicle suitability evidence; real-time or near-real-time capacity; tested trip-blocker policy; and comprehensive geographic coverage.

- **WHY USER MIGHT PAY:** **INFERRED —** Users may pay for automatic rechecks, saved comparisons, monitoring, export, and offline use because the dashboard reduces high-stakes checking. The dashboard’s basic restrictions and material unknowns should remain free; a static summary alone has a weaker payment case.

- **WHAT WOULD MAKE THEM CANCEL:** A green summary that hides a critical unknown; missing high-impact checks; excessive warnings with no prioritization; stale external data; a need to rebuild the checklist manually; or a false implication that the tool ruled out road, capacity, or weather failures.

- **COMPETITORS:** Roadtrippers is closest on itinerary overview; onX and Gaia on spatial planning; AllTrails and COTREX on activity status; Recreation.gov on permits and campsites; weather and road products on conditions. None of the reviewed products consistently presents an evidence-backed activity-plus-overnight feasibility object, but many are stronger within their individual domains.

- **DEFENSIBILITY:** **INFERRED —** The screen is easy to copy. Defensibility would come from the underlying cross-domain claim graph, jurisdiction applicability, source monitoring, freshness logic, and a validated definition of which claims block a candidate.

- **TRUST RISK:** A compact dashboard can be read as a safety assessment. **Guardrail:** Do not use a universal go/no-go score. Give prohibitions and critical unknowns equal or greater prominence than favorable evidence, identify inherently unknowable conditions, and state that the dashboard does not establish safety, availability, or vehicle passability.

- **BUILD COMPLEXITY:** **High.** The hardest part is obtaining sufficiently current, destination-specific data across domains while preserving the limitations of each source.

- **SMALLEST VALIDATION EXPERIMENT:** Create clickable dashboards for six realistic trip scenarios: published road closure, missing permit, full reservable campground with unknown dispersed capacity, fire restriction, seasonal snow, and no detected change with one unavailable source. Test interpretation with 12 participants.

- **SUCCESS METRIC:** Pass if at least **10 of 12** participants correctly identify the decisive blocker or unresolved check in at least **five of six** scenarios, and no more than **one** interprets the dashboard as a guarantee that the trip is safe or will succeed.

- **ROADMAP FIT:** **INFERRED —** M8 presentation layer built from M4–M7 evidence. It depends on the evidence-state and freshness foundations, a stable candidate-plan object, and clear critical-claim policy. Live weather, fire, closure, and road integrations would be later prerequisites for a genuinely current dashboard and are outside the present roadmap.

## Bet 7 — Offline trip package

- **TARGET USER:** A dispersed camper, paddler, backcountry visitor, or unfamiliar Colorado traveler who expects unreliable service at the final road, trailhead, water access, or overnight location.

- **SPECIFIC JOB:** “Preserve the map context, rules, sources, contacts, and unresolved checks for my exact trip so I can use them without connectivity.”

- **TRIGGER MOMENT:** The final planning session before leaving service, particularly when the user would otherwise take screenshots, print pages, or download several unrelated offline maps.

- **CURRENT WORKFLOW:** **RETRIEVED —** Users download offline maps from AllTrails, Gaia, onX, Trailforks, or Google Maps; save reservation PDFs; take screenshots of rules and directions; and copy agency phone numbers into notes. Offline payment precedent appears in [AllTrails](https://www.alltrails.com/plans), [onX Offroad](https://www.onxmaps.com/offroad/app/pricing), [Gaia GPS](https://www.gaiagps.com/premium), [Trailforks](https://www.trailforks.com/pro/), and [CalTopo](https://caltopo.com/northern).

- **CURRENT APPS USED:** AllTrails, Gaia GPS, onX, Google Maps, Avenza, CalTopo, Trailforks, PDF readers, screenshots, notes, and Recreation.gov.

- **PAIN:** Offline maps preserve geometry but often leave the user’s evidence scattered among screenshots, browser tabs, reservation records, and agency pages. The traveler may not know which material was current when downloaded or which claims required a final live recheck.

- **OHVERNIGHT EXPERIENCE:** **INFERRED —**  
  1. The user selects a saved trip and requests an offline package.  
  2. Ohvernight lists the included map area, activity and overnight options, access references, rules, sources, contacts, timestamps, and unresolved checks.  
  3. The user performs a final live refresh and downloads or prints a versioned package.  
  4. Offline, the package continues to show its generation time, evidence dates, expiry cues, and which items may have changed since download.

- **MVP:** A downloadable or printable trip dossier generated from a saved local plan. Include static map references, coordinates, activity and overnight evidence, applicable rules, source URLs, contact details, timestamps, known restrictions, and manual-recheck items. Do not begin with full offline vector maps or navigation.

- **WHAT DATA IS REQUIRED:** A saved-trip object; exportable map or permitted static map assets; feature coordinates; applicable evidence and rules; source metadata; contacts; package version and generation time; stale thresholds; update instructions; and licensing or redistribution rights.

- **WHAT DATA WE ALREADY HAVE:** **RETRIEVED —** A static web map, a simple local saved list, regional layers, recreation and developed-campground features, reviewed rules, source links, source-fetched information, and explicit unknown states. These are sufficient to prototype a dossier without native offline navigation.

- **WHAT DATA WE LACK:** **UNKNOWN —** Confirmed redistribution and offline-storage rights for every map and source; a package generator; offline-capable client behavior; route data; durable package versioning; pre-departure refresh logic; storage limits; and evidence that users want a dossier rather than their existing screenshot workflow.

- **WHY USER MIGHT PAY:** **RETRIEVED / INFERRED —** Offline capability has one of the clearest outdoor subscription precedents, but generic offline maps are commoditized. Users might pay for a trip-specific package that preserves the exact evidence, restrictions, contacts, and unknowns they reviewed—not merely another basemap.

- **WHAT WOULD MAKE THEM CANCEL:** Missing map detail; a package that becomes stale without making that obvious; inability to include reservation or rule information legally; awkward downloads; no advantage over screenshots; or discovering that the package implied live status after connectivity was lost.

- **COMPETITORS:** AllTrails, onX, Gaia, Trailforks, CalTopo, Avenza, and Google Maps are much stronger on established offline mapping. Ohvernight’s narrower differentiation would be a versioned, evidence-centered activity-and-overnight dossier.

- **DEFENSIBILITY:** **INFERRED —** Low for offline storage itself. Defensibility improves only when the package contains Ohvernight’s normalized candidate plan, claim provenance, source applicability, freshness metadata, and explicit unresolved states.

- **TRUST RISK:** Downloaded information ages and can be mistaken for current status. **Guardrail:** Show generation time and source dates persistently, distinguish static rules from time-sensitive conditions, provide expiry or recheck cues, and never state that an offline package confirms current access or restrictions.

- **BUILD COMPLEXITY:** **Medium.** The hardest part is licensing and versioning; a printable dossier is low complexity, while a complete offline map and application state would be high complexity.

- **SMALLEST VALIDATION EXPERIMENT:** Produce trip dossiers manually for ten pilot users and offer two versions: a free on-screen plan and a downloadable/printable package. Observe whether participants actually save, print, or use the package during a trip, then ask for a real purchase choice rather than only stated interest.

- **SUCCESS METRIC:** Pass if at least **6 of 10** participants download or print the dossier, at least **4 of 10** consult it during the trip, and at least **3 of 10** choose a paid-package option in a nonbinding purchase test.

- **ROADMAP FIT:** **INFERRED —** A delivery capability after M7 or within M8 once candidate plans can be saved. A dossier can be tested before full offline application support. Prerequisites are stable plan and evidence objects, licensing review, versioning, and stale-data handling; it does not require changing the substantive M4–M7 roadmap.

## Ranking by evidence strength × feasibility with existing data

The scores below are comparative research judgments, not market-size or revenue forecasts. Evidence strength measures support for the customer problem and payment precedent. Existing-data feasibility measures how much can be tested credibly using Ohvernight’s present regional layers, reviewed evidence model, source metadata, and local saved list.

| Rank | Bet | Evidence strength | Existing-data feasibility | Product | Reason |
|---:|---|---:|---:|---:|---|
| 1 | Evidence-backed access confidence | 5/5 | 5/5 | 25 | Strong permission-verification evidence; directly uses Ohvernight’s existing trust model, reviewed rules, source metadata, and “not established” state. |
| 2 | Freshness / “when was this checked?” | 5/5 | 4/5 | 20 | Strong staleness and changing-restriction evidence; current source-fetched metadata supports a manual claim-level prototype, although monitoring history is missing. |
| 3 | Offline trip package | 4/5 | 4/5 | 16 | Strong payment precedent and a dossier can use current data without native offline maps; direct Ohvernight-specific demand remains unproven. |
| 4 | Overnight + activity pairing | 5/5 | 3/5 | 15 | The fragmentation problem is strongly demonstrated, and current data can support a narrow manual prototype; reliable pairing awaits M4–M7 normalization. |
| 5 | Adventure matching | 5/5 | 2/5 | 10 | Strong customer job and strategic fit, but current data is too incomplete for trustworthy automated ranking beyond a concierge experiment. |
| 6 | Saved-trip monitoring | 4/5 | 2/5 | 8 | Strong failure-prevention logic and paid-alert precedent, but Ohvernight lacks monitoring operations, comprehensive feeds, notification delivery, and complete trip dependencies. |
| 7 | Trip feasibility dashboard | 4/5 | 1/5 | 4 | The failure modes are well supported, but a current dashboard would have major blind spots because weather, fire, road, closure, reservation, and condition feeds do not yet exist. |

## The one bet to test first

**Evidence-backed access confidence.**

It should be tested first because it is both the highest-ranked bet and the interpretation layer on which the other six depend. Pairing, matching, monitoring, feasibility, and offline packaging can all amplify harm if users misunderstand “public,” “mapped,” “checked,” “nearby,” or “no closure found” as proof of permission or safety.

A two-week comprehension test can use data and evidence states Ohvernight already has. It can answer a foundational question before additional ingestion or automation work: can users correctly distinguish legal permission, legal route designation, physical condition, freshness, and “not established”?

A failed result would not mean abandoning provenance. It would mean revising vocabulary and information hierarchy before using those states in ranking, alerts, or compressed dashboards. A passed result would reduce product risk across M4–M8 and give the later experiments a tested presentation foundation.

## Bets I would not test yet

1. **A numeric trip-confidence or safety score.** The present evidence cannot calibrate one, and a composite score could allow favorable data to obscure one decisive prohibition or unknown.

2. **A full live trip-feasibility product.** Test dashboard comprehension with scenarios, but do not test market demand using a supposedly live dashboard until its major data omissions are explicit. Otherwise the experiment measures trust in an incomplete product.

3. **Automated alternate-plan generation.** The candidate inventory and evidence coverage are not yet broad enough to guarantee that an alternative has independent support. “No supported alternative found” must remain acceptable.

4. **Predictive vehicle passability.** MVUM designation, terrain, and road class cannot establish current clearance, traction, washout severity, trailer maneuverability, or driver capability.

5. **Real-time dispersed-site availability.** No credible pilot-area data source establishes whether a dispersed site will be vacant on arrival.

6. **Crowd-avoidance ranking.** Evidence is anecdotal, reliable current data is lacking, and ranking quieter places could redirect use toward fragile or poorly understood sites.

7. **Generic AI trip chat.** It does not solve the underlying evidence, identity, freshness, or coverage problem and could make unsupported statements sound more authoritative.

8. **Generic social reviews or new campsite pins.** Ohvernight lacks contributor density and moderation infrastructure, and community reports must never become evidence of legal permission.

9. **Achievements, streaks, or engagement ranking.** No demonstrated customer job supports them, and they could encourage unnecessary visitation or unsafe choices.

10. **A standalone paid provenance tier.** Current evidence supports payment for avoided work, monitoring, offline execution, and trip recovery—not for public-source links or evidence labels in isolation.

## Unknowns

1. **UNKNOWN — Will users pay Ohvernight specifically?** Competitor subscriptions establish payment categories and qualitative price expectations, not conversion for Ohvernight.

2. **UNKNOWN — Who is the first narrow customer segment?** A visiting family, Colorado weekend camper, paddler, dispersed camper, and overlander place different values on pairing, monitoring, vehicle evidence, and offline use.

3. **UNKNOWN — Which evidence states users understand correctly?** “Confidence,” “verified,” “current,” and green status treatments may imply guarantees. This is the highest-priority research gap.

4. **UNKNOWN — Which unresolved claims should block ranking?** Established prohibitions are clear blockers, but policy is still needed for missing access evidence, stale rules, unknown road condition, uncertain capacity, and absent activity-specific permission.

5. **UNKNOWN — How much candidate coverage is enough?** A small, high-quality result set may be useful, but sparse coverage may make pairing and matching feel incomplete or biased.

6. **UNKNOWN — How much app switching can pairing actually eliminate?** Users may continue using AllTrails, onX, Google Maps, weather tools, and reservation providers even when Ohvernight supplies a candidate plan.

7. **UNKNOWN — Whether water-plus-overnight is a sufficiently strong initial wedge.** Water rules justify M4’s evidence work, but direct customer evidence remains thinner than for camping permission and vehicle access.

8. **UNKNOWN — Monitoring expectations and acceptable cadence.** Users may expect immediate detection even when official sources update irregularly or become unavailable.

9. **UNKNOWN — Source-monitoring feasibility at scale.** Colorado agencies and jurisdictions publish notices through heterogeneous pages, maps, PDFs, feeds, and orders.

10. **UNKNOWN — Reservation and live-availability access.** The evidence base does not establish which providers permit timely, licensed integration.

11. **UNKNOWN — Offline licensing.** Map tiles, source documents, excerpts, and reservation artifacts may have different storage and redistribution rights.

12. **UNKNOWN — Actual trip-failure prevalence.** The taxonomy identifies recurring failure modes but is not a representative survey and does not establish statewide probabilities.

13. **UNKNOWN — User tolerance for honest incompleteness.** Explicit unknowns support trust, but they may also make the product feel less immediately decisive than competitors that use simpler labels.

14. **UNKNOWN — Outcome collection.** It is not known whether users will reliably report whether a road, activity, or overnight plan worked, nor whether those reports can safely improve the model without being mistaken for permission evidence.

15. **UNKNOWN — Environmental consequences of discovery and ranking.** Candidate matching could concentrate use or expose sensitive locations unless suppression, stewardship, and capacity policies are established.

16. **UNKNOWN — Competitive response.** Larger products can copy interface features. Ohvernight’s defensibility depends on maintaining deeper feature identity, provenance, rule applicability, and freshness—not on feature novelty alone.
