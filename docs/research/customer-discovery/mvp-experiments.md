# MVP experiments: cheapest useful validation per opportunity

**Summary.** The seven Tier 1 opportunities in `docs/research/product-opportunities/idea-fairy-report.md` (pairing, access confidence, freshness, adventure matching, saved-trip monitoring, trip feasibility, offline package) are the same seven bets in `product-bets.md`, so this file has seven experiments plus one cross-cutting demand test (E8). Each gives HYPOTHESIS, EXPERIMENT, COST, TIME, SUCCESS THRESHOLD, FAILURE THRESHOLD and WHAT WE LEARN, followed by the experiment's own trust risk and what it does not prove. Thresholds are numbers fixed before the test. **No experiment takes payment, collects card details, or presents a fake purchase.** Where a price is tested, it is by stated choice among labelled options only, with a visible line that nothing is for sale. Nothing here is to be run, built or published until the owner decides to; no business decision is made here. The recommended order for the first three and the stop condition are at the end.

Evidence labels: **HERMES-SOURCED**, **VERIFIED**, **INFERENCE**, **UNKNOWN**.

## Rules that apply to every experiment

These come from the repository trust principles (`docs/product/trust-principles.md`, VERIFIED, read in the m4a worktree) and `AGENTS.md`.

1. **No invented facts.** Every claim shown to a participant comes from a real source the participant can open. If we do not have a source, the card says "not established" or "unknown". No placeholder permitted/closed/open states, even in a prototype.
2. **No implied access.** A fake door or landing page must not suggest a place is legal, open, available, safe or endorsed. Use the existing wording in the product (for example "Published source, current access unconfirmed").
3. **Fake doors say they are fake.** A button for a feature that does not exist must, after click, say "This feature is not built yet" and record a click count only. No account, no email required, no payment.
4. **No payment, no deposit, no pre-order, no card form.** Not even a "reserve" or "waitlist with price". Stated preference between labelled options is the strongest allowed signal and is weak evidence of willingness to pay; see E8.
5. **Real trips need honest caveats.** If a concierge recommendation is given for someone's real trip, attach the standard line that research is not permission and the user must confirm with the land manager before travel.
6. **Location privacy.** Do not ask for or retain exact home locations, favourite spots or trip routes beyond what is needed; store under participant codes and delete after write-up. See the security review for storage rules.
7. **Pre-register thresholds.** Write the thresholds below into the notes before the first participant. Do not change them after seeing results. Record any change as a new, separately labelled experiment.
8. **Do not run on the live site.** Use a private page, a printed or PDF card, or a clickable prototype. Merging to `main` publishes the whole repository (`AGENTS.md`), so do not put test material in the repository's published paths.

Cost and time are my estimates (INFERENCE) in owner hours unless stated; no money is needed unless noted.

## Mapping

| # | Opportunity (Tier 1) / Bet | Experiment type |
|---|---|---|
| E1 | 1. Overnight plus activity pairing / Bet 1 | Manual concierge recommendation |
| E2 | 2. Evidence-backed access confidence / Bet 2 | Clickable prototype with comprehension questions |
| E3 | 3. Freshness, "when was this checked?" / Bet 3 | Structured survey and five-user interview test |
| E4 | 4. Adventure matching / Bet 4 | Trip-planning concierge |
| E5 | 5. Saved-trip monitoring and alerts / Bet 5 | Concierge with a fake-door sign-up and simulated outage |
| E6 | 6. Trip feasibility on one screen / Bet 6 | Clickable scenarios (scenario comprehension) |
| E7 | 7. Offline expedition package / Bet 7 | Manual PDF dossier and non-binding choice |
| E8 | Cross-cutting: pricing and demand | Pricing page test without payment |

## E1. Overnight plus activity pairing

- **HYPOTHESIS:** People who choose an activity first can be given two evidence-linked activity-and-overnight pairs by hand that they treat as serious plan candidates, and the pairs cut the number of other tools they consult. (`product-bets.md`, Bet 1.)
- **EXPERIMENT:** Concierge. Recruit 10 people (from the interview kit's channels) who are planning a real pilot-area or Colorado weekend trip in the next 3 weeks. Use the product's existing pilot data and official links to hand-build two candidate pairs per person on a one-page template: activity access point, overnight option, separate claim rows (activity permission, overnight permission, access legality, restrictions, source and date, unknowns). Deliver by PDF. Before delivery record what they have done so far and which tools they use. After delivery run a 10-minute call: which pair would you pursue, what else did you still open, what is missing. Add a 3-question comprehension check (does "nearby" mean allowed? what does "not established" mean? what would you check before going?).
- **COST:** About 3 owner hours per participant for research and one page (30 hours total); no money.
- **TIME:** 2 to 3 weeks including recruiting.
- **SUCCESS THRESHOLD:** At least 7 of 10 select a supplied pair as a serious candidate; median external tools consulted falls by at least 2; 0 of 10 treat proximity as permission in the comprehension check. (Same numbers as Bet 1 in `product-bets.md`; chosen by Hermes, not by me.)
- **FAILURE THRESHOLD:** 4 or fewer of 10 select a pair, or the median reduction in tools is 0 or 1, or 2 or more participants read "nearby" as permitted.
- **WHAT WE LEARN:** Whether pairing is valued before any M8 build; how many options are enough; which rows people actually read; which unknowns block a decision; which tools they still need.
- **TRUST RISK OF THE EXPERIMENT:** A pair on paper can read as a recommendation of a place to sleep. Mitigation: each row shows its source and "not established" where we have none; add the "research, not permission" line; never rank; never call a result "recommended" or "safe". Block any option with an established prohibition. Do not offer dispersed options we have not reviewed.
- **WHAT IT DOES NOT PROVE:** That the pairing can be automated or scaled; that results generalise beyond ten motivated volunteers; that anyone will pay; that coverage is wide enough. Hand-picked pairs overstate what a data-limited product could do today.

## E2. Evidence-backed access confidence

- **HYPOTHESIS:** Users shown concise evidence states ("established permitted", "conditional", "not established", and so on) correctly separate land ownership, legal access, camping permission, and physical conditions, and do not read "not established" as permitted. (`product-bets.md`, Bet 2; also the highest-ranked bet.)
- **EXPERIMENT:** Clickable prototype (static pages or slides) with two card variants for 10 real reviewed examples: one with the evidence-state vocabulary and one with conventional map labels. Each participant sees both, order randomised. Ask five questions per example (is the land public? may you drive there? may you camp? is the road passable now? how recent is the information?) and one "what does this word mean" question each for "not established", "conditional" and "checked". Recruit 12.
- **COST:** About 12 hours to build cards and instructions; 12 sessions at 20 minutes each; no money.
- **TIME:** 2 weeks.
- **SUCCESS THRESHOLD:** At least 10 of 12 answer at least 4 of 5 questions correctly with the evidence-state version, and no more than 1 of 12 reads "not established" as permitted. (Bet 2 numbers.)
- **FAILURE THRESHOLD:** 7 or fewer of 12 reach 4 of 5, or 3 or more read "not established" as permitted, or the conventional-label variant scores within 1 correct answer of the evidence-state variant.
- **WHAT WE LEARN:** Which words are safe, which sound like guarantees (for example "confidence", "verified"); whether the evidence format beats ordinary labels at all; where the information hierarchy confuses people.
- **TRUST RISK OF THE EXPERIMENT:** Real examples must be accurate: use only features with a real linked source and a current review. If an example has no authoritative source, show it as "not established", not as a guess. Do not use the word "verified" until the test itself shows how it is read. Include at least one prohibition and one unknown among the 10 examples, so the test is not only good news.
- **WHAT IT DOES NOT PROVE:** That users will act on the states in a real trip; that the underlying claims are right; that they will pay for evidence; that results hold for people who never take a test. It measures comprehension only.

## E3. Freshness, "when was this checked?"

- **HYPOTHESIS:** Users shown a full freshness label (timestamp, what was checked, a recheck instruction) correctly distinguish "source checked" from "condition verified". (`product-bets.md`, Bet 3.)
- **EXPERIMENT:** Structured survey plus a short interview test. Prepare 15 real claims, each with three label variants: timestamp only; timestamp plus evidence class; timestamp plus class plus recheck instruction. Randomise each of 12 participants into one variant per claim. Ask "what do you think was actually checked, and when?", "would you need to check anything before you go?". Add five-user observation of a real person asked to find the date a claim was last checked.
- **COST:** About 10 hours; no money. A free survey form can host the structured part.
- **TIME:** 2 weeks.
- **SUCCESS THRESHOLD:** At least 10 of 12 correctly distinguish "source checked" from "condition verified" with the full version, and at least 8 of 12 name the claims that need a recheck before departure. (Bet 3 numbers.)
- **FAILURE THRESHOLD:** 7 or fewer of 12 distinguish them with the full version, or the full version is no better than timestamp-only by more than 2 participants.
- **WHAT WE LEARN:** Whether a "checked" date creates false comfort; which wording prevents that; which claims users prioritise for a recheck.
- **TRUST RISK OF THE EXPERIMENT:** Showing recent dates on stale-looking claims can create false comfort for the test itself. Use only real retrieval dates and say plainly in the test which are old. Never show a "last checked today" label that we did not produce. The product already separates source fetch dates from conditions in code (VERIFIED: `v2/explore/evidence.js` lines 8-14 build "Fetched <date>" lines, and "older than the refresh policy" text), so use those formulations.
- **WHAT IT DOES NOT PROVE:** That freshness changes decisions or purchases; that monitoring is operationally feasible; that the checks are right. It tests wording comprehension only.

## E4. Adventure matching

- **HYPOTHESIS:** A hand-ranked list of up to three candidate plans, built from a user's dates, vehicle, activities and overnight style, lands in their top two choices and saves at least an hour of planning. (`product-bets.md`, Bet 4.)
- **EXPERIMENT:** Trip-planning concierge. Take 10 real trip briefs (dates, vehicle, two or more activities, overnight style, tolerance for unknowns). Build up to three plans using a fixed written rubric and show the reasoning for each ranking and for each exclusion. Ask them to compare against what they would have chosen themselves, and count the hours they report saving. Include one brief for which "no supported plan found" is the honest answer, and see whether trust survives.
- **COST:** About 4 owner hours per brief (40 hours total); no money.
- **TIME:** 3 weeks.
- **SUCCESS THRESHOLD:** At least 7 of 10 place a supplied plan in their top two; at least 6 of 10 report saving an hour or more; 0 of 10 select a plan after misreading a critical unknown as established. (Bet 4 numbers.)
- **FAILURE THRESHOLD:** 4 or fewer of 10 place a plan in their top two; fewer than 3 of 10 report saving an hour; or any participant picks a plan because a critical unknown looked established.
- **WHAT WE LEARN:** Whether a matching product has a job to do beyond E1; which constraints people relax; whether "no supported alternative" is acceptable.
- **TRUST RISK OF THE EXPERIMENT:** Ranking looks like endorsement. Mitigation: show the rubric and the reason for every order; never include an option with an established prohibition; label each plan "research suggestion, not verified"; do not use the word "best". Do not rank unresolved options above resolved ones.
- **WHAT IT DOES NOT PROVE:** That an algorithm can match this quality; that coverage supports it in other areas; paying behaviour. A person doing the matching by hand has more judgement than any near-term system.

## E5. Saved-trip monitoring and alerts

- **HYPOTHESIS:** Users with trips 1 to 3 weeks out would use monitoring for a comparable next trip, and understand that no alert does not mean no change. (`product-bets.md`, Bet 5.)
- **EXPERIMENT:** Concierge plus a fake door. For up to 10 real trips departing in the next 2 weeks: write a coverage statement listing exactly which official sources we will watch and which we will not; send two scheduled status reports by hand (email or message) stating last check, what changed, what could not be checked; include one simulated source outage notice, clearly labelled as a test after the fact. Then show a single "Turn on monitoring for my next trip" button that is a labelled fake door: on click it says "This is not built yet. Nothing was saved," and the click is counted; no email or account is requested. Finish with a 10-minute call.
- **COST:** About 6 owner hours per trip including weekly checks (60 hours total). Because this requires real manual checks of official sources, keep it to a defined small set. No money; no software.
- **TIME:** 3 to 4 weeks (trips depart within 2 weeks, then follow-up).
- **SUCCESS THRESHOLD:** At least 7 of 10 say they would enable monitoring for their next comparable trip, backed by a past behaviour of rechecking sources on a prior trip; at least 5 of 10 click the fake door unprompted at the end; 10 of 10 correctly understand that no alert does not guarantee no change. (Bet 5 sets 7/10, 5/10 and 10/10; the click metric is mine.) Willingness-to-pay is not a pass criterion here because no payment is taken.
- **FAILURE THRESHOLD:** 4 or fewer of 10 would enable it, or 2 or more misread silence as safety, or participants report reports as noise.
- **WHAT WE LEARN:** Appetite for monitoring; acceptable cadence; how people read silence and gaps; which sources matter to them.
- **TRUST RISK OF THE EXPERIMENT:** The highest of all eight. Silence reads as "all clear." Mitigation: each report states last successful check, covered and uncovered sources, and the line that absence of a detected change does not establish current access, passability, capacity, weather or safety. Never say "no changes, you are good to go." Do not run this for a trip where someone may rely on it for safety (remote backcountry, fire-season dispersed camping) unless they confirm separately with the land manager. The fake door must not imply the feature exists.
- **WHAT IT DOES NOT PROVE:** That monitoring is feasible at scale (it is a hand check of a few pages); that anyone will pay; that people would respond to real alerts; how often failures occur. See `product-bets.md`, Unknowns 8 and 9.

## E6. Trip feasibility on one screen

- **HYPOTHESIS:** People shown a compact feasibility checklist (not a score) correctly name the decisive blocker or unresolved check and do not read it as a guarantee. (`product-bets.md`, Bet 6.)
- **EXPERIMENT:** Clickable scenarios (static pages). Build six scenarios as in `product-bets.md`: a published road closure, a missing permit, a full reservable campground with unknown dispersed capacity, a fire restriction, seasonal snow, and "no change detected" with one source unavailable. Use fictional, clearly labelled example places, not real locations. Show each to 12 participants; ask what stops the trip, what remains unresolved, and whether the screen means the trip is safe.
- **COST:** About 10 hours; no money.
- **TIME:** 2 weeks.
- **SUCCESS THRESHOLD:** At least 10 of 12 identify the decisive blocker or unresolved check in at least 5 of 6 scenarios; no more than 1 of 12 reads the screen as a guarantee. (Bet 6 numbers.)
- **FAILURE THRESHOLD:** 7 or fewer of 12 identify the blocker in 5 of 6 scenarios, or 3 or more read it as a guarantee.
- **WHAT WE LEARN:** Whether compression hides nuance; whether blockers and unknowns need more prominence; which signal types people understand.
- **TRUST RISK OF THE EXPERIMENT:** This is a scenario test, not a live dashboard. Use fictional places labelled "example", not real places, so no invented fact is attached to a real location. Do not present it as a working product, and do not test demand with it. `product-bets.md` says a full live dashboard should not be tested for market demand yet because the feeds do not exist.
- **WHAT IT DOES NOT PROVE:** Market demand, data feasibility, or that people will use a dashboard on a real trip. Scenario comprehension only.

## E7. Offline expedition package

- **HYPOTHESIS:** Users given a printable dossier for a real trip will download or print it, consult it during the trip, and prefer the packaged version in a non-binding choice. (`product-bets.md`, Bet 7.)
- **EXPERIMENT:** Manual dossier. For 10 pilot users, hand-produce a PDF with map references, rules, source links, dates, contacts (official agency contacts only, no personal contacts), generation time and explicit "recheck before departure" cues. Offer it next to a free on-screen version. Count who saves or prints it, ask after the trip who consulted it and when, and at the end ask a non-binding "which would you pick" among labelled options. No price is taken and nothing is sold.
- **COST:** About 4 owner hours per dossier (40 hours total); printing cost is optional and small. No payment collected.
- **TIME:** 3 to 4 weeks (the trip must happen).
- **SUCCESS THRESHOLD:** At least 6 of 10 download or print the dossier; at least 4 of 10 consult it during the trip; at least 3 of 10 pick the packaged version in the non-binding choice. (Bet 7 numbers; the choice step is non-binding so no payment is involved.)
- **FAILURE THRESHOLD:** 3 or fewer of 10 download or print it, or 1 or fewer consults it during the trip.
- **WHAT WE LEARN:** Whether offline value is real before any offline infrastructure; which sections are used; how participants treat the age of a package.
- **TRUST RISK OF THE EXPERIMENT:** A paper or PDF dossier freezes information; a person may rely on it after it goes stale. Mitigation: show generation time and source dates on every page and a bold recheck line; separate static rules from time-sensitive conditions; never state it confirms current access. Include only licensed content. Licensing of map tiles and source excerpts is UNKNOWN (`product-bets.md`, Unknowns 11), so avoid reproducing tiles or long excerpts; link instead.
- **WHAT IT DOES NOT PROVE:** That people would pay, since the choice is non-binding and the product is free; that the licensing allows it at scale; that a native offline app is needed.

## E8. Cross-cutting pricing and demand test (no payment)

Not a Tier 1 item, but the reports list an unproven willingness-to-pay as the biggest unknown (`idea-fairy-report.md`, Unknowns 1). This is the only experiment about price.

- **HYPOTHESIS:** When presented with plain descriptions of Free, Plus and trip-pass options, a clear share of target users choose a paid option for a reason that matches a real past spend. (`idea-fairy-report.md`, Suggested next experiments 8.)
- **EXPERIMENT:** Pricing page test without payment. A private page or printed card shows three labelled options (Free; Plus with saved trips, monitoring, offline; a trip pass) drawn from the Pricing observations in `idea-fairy-report.md`, each stating plainly that this is research, nothing is for sale and no payment is taken. Ask interview participants (from the earlier tests) to choose one and explain why. Record choice and reason; follow with the question "what do you pay for today that is closest to this?" Do not show a Buy button. Do not collect an email or card. Do not let a choice here count as revenue evidence.
- **COST:** About 6 hours of build, 12 to 20 short sessions folded into other calls; no money.
- **TIME:** 2 weeks, run after E1 to E7 have given participants real context.
- **SUCCESS THRESHOLD:** At least 8 of 20 choose a paid option, and at least 5 of those 8 tie the choice to a concrete past spend (a named current subscription and its trigger). Higher thresholds are not claimed.
- **FAILURE THRESHOLD:** 4 or fewer of 20 choose a paid option, or fewer than 3 of those can name a comparable past purchase.
- **WHAT WE LEARN:** Which bundle people lean towards and why; whether the stated reason matches past behaviour (a sign the choice is real); which features are expected free.
- **TRUST RISK OF THE EXPERIMENT:** A pricing page can read as a working service. Mitigation: a banner on every option states "research only; nothing is for sale; no payment is taken"; keep all restrictions, warnings and source links visible in every tier, as `idea-fairy-report.md` and `product-bets.md` require (basic restrictions and sources stay free); never gate a safety or legal fact in the mock-up.
- **WHAT IT DOES NOT PROVE:** Actual willingness to pay. Stated choice is not purchase; the report itself warns not to treat clicks as revenue proof. Only real payment would measure that, and this document does not authorise any.

## Recommended order for the first three

| Order | Experiment | Why |
|---|---|---|
| 1 | **E2 Evidence-backed access confidence** | It tests the vocabulary every other bet displays, uses data and states the product already has, needs no real trips and has the shortest cycle. `product-bets.md` ranks it first and says a failed result means revising vocabulary before building anything on top. HERMES-SOURCED reasoning, adopted by me. |
| 2 | **E1 Overnight plus activity pairing** | It tests the strongest demonstrated customer pain (fragmented planning), costs only owner hours, and exercises the comprehension lessons from E2 in a real planning context. Run recruiting during E2. |
| 3 | **E3 Freshness** | It reuses E2's participants and format, adds almost no build cost, and addresses the "checked is not verified" risk that E5 and E7 depend on. |

E5 (monitoring) and E7 (offline) follow only after E2 and E3 show people read the labels correctly. E4 and E6 follow E1. E8 comes last, after participants have context.

## What result would stop the line of work

These are the stop conditions I would suggest the owner consider; the decision is the owner's.

1. **Stop evidence-state work as designed** if E2 fails twice: after one revision of vocabulary and layout, still fewer than 10 of 12 reach 4 of 5, or 3 or more of 12 read "not established" as permitted. Users misreading the core states means every ranking, alert and dashboard built on them could cause harm.
2. **Stop the pairing and matching line** if E1 and E4 both fail: 4 or fewer of 10 select a pair or plan, and median external-tool reduction is under 2. That would mean the fragmentation pain does not convert into value.
3. **Stop monitoring and offline as paid ideas** if E5 and E7 fail their thresholds and E8 shows 4 or fewer of 20 choosing any paid option with no named past spend.
4. **Stop recruiting a segment** after 8 interviews with no sign of the pain in the kit's section 7 (for example, most participants never check permission or never rechecked anything), and record that as a finding.
5. **Pause any experiment** immediately if a participant is observed treating a research card as permission to enter, camp, drive or fish somewhere; correct them in the session, record it as a trust incident, and revisit wording before continuing.

Failure of one experiment is information, not a verdict: each result should be written up with the pre-registered threshold beside it, and the owner decides what changes.
