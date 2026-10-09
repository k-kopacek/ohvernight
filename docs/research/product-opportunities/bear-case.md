DRAFT - UNREVIEWED

# Ohvernight bear case

Status: analysis for the owner, written 2026-10-07. Not a decision, not a
business-model selection and not a roadmap change. No web access was used;
this is synthesis of the reports already in `docs/research/`.

Labels: **HERMES-SOURCED** means the statement comes from a Hermes web
research report that nobody has re-checked; its URL is carried through.
**INFERENCE** is this document's reasoning. **UNKNOWN** means the reports do
not support a figure or a conclusion. Repository facts are cited by file.

## Summary

The business case for Ohvernight rests on a pain nobody has measured, a
product that cannot yet answer its own headline question, and a supply of
reviewed claims that one person has to produce and keep current. None of the
reports read for this document contains a single observation of
someone paying, or offering to pay, for what Ohvernight proposes. What the
reports do establish is that the planning workflow is fragmented, that
permission is hard to determine, and that incumbents disclaim the question
rather than answer it. That is a real gap. It is not yet a market.

The most likely way this fails is quiet: the map gets better milestone by
milestone, nobody is asked for money, and the review workload grows until it
consumes the owner. The most fatal way is loud: a stale or over-read claim
sends someone somewhere they may not be. The project is unusually well
defended against the second and almost undefended against the first.

Ranking below is by likelihood multiplied by how fatal the outcome is to the
**business** (a paying niche). Several of these would leave a perfectly good
open reference project standing. That distinction matters and is returned to
in the judgement.

| Rank | Failure reason | Likelihood | Fatal to the business? |
|---:|---|---|---|
| 1 | Nobody pays: the switching pain is real but too small, too rare, or already tolerated | High | Yes |
| 2 | The honest answer today is "unknown", and stays that way for the places people ask about | High | Yes, until fixed |
| 3 | Reviewed-claim upkeep outgrows one owner | High as scope grows | Yes |
| 4 | No route to users, and no instrument to tell whether anyone came | High | Yes |
| 5 | Nothing is defensible: free government products below, funded incumbents above, open code and public data in between | Medium to high | Slowly |
| 6 | Every revenue line needs things that do not exist and that the architecture and governance currently exclude | High | Delays indefinitely |
| 7 | Two regions cannot carry an annual price | High | For subscription, yes |
| 8 | A user reads proximity or ownership as permission, or a restriction goes stale | Low to medium | Potentially terminal |
| 9 | Seasonality and churn | High if a subscription is sold | Serious |
| 10 | Purchase is driven by offline maps, which Ohvernight should not build | Medium | Serious |
| 11 | Key sources stay closed or withdraw | Medium | For M6, yes |
| 12 | The agent-built process itself: single point of failure, and agents that have already proposed unsafe claims | Medium | Serious |

---

## 1. Nobody pays

**The case.** HERMES-SOURCED: no academic, agency or industry survey was
found that measures how many outdoor travellers use several apps, how much it
bothers them, or what they would pay to stop; "the central pain claim is
therefore UNKNOWN, not validated" (`hermes/b9-bear-case.md`, section a). The
customer-pain reports are qualitative: source counts are URLs, not people,
and "can establish recurring workflows and pain patterns, but not market size
or willingness-to-pay percentages" (`hermes/p2-customer-pain-and-workflows.md`,
method). The persona document marks trip frequency, current subscriptions,
acquisition channel and premium feature as INFERRED for every persona, and
says evidence that the first-choice customer would pay Ohvernight is "thin"
(`personas-and-monetization.md`, Part 1).

HERMES-SOURCED supporting facts:

- Average outings per participant fell from 70.5 to 62.5 (an 11.4% fall) in
  2023 while participation rose to 175.8 million.
  https://outdoorindustry.org/press-release/outdoor-participation-hits-record-levels-for-ninth-consecutive-year/
- AllTrails' former chief executive said its original backcountry and
  van-life users "often did not want to pay"; growth came from moving to a
  casual mass audience. https://www.revenuecat.com/blog/growth/alltrails-product-channel
- Sēkr, built explicitly to reduce multi-app planning, went dormant and was
  being wound down before Peace Vans acquired it in December 2023.
  https://techcrunch.com/2024/06/04/travel-app-sekr-wants-to-help-you-plan-your-next-road-trip-with-its-new-ai-tool/
- Users resist "paying for information users believe is freely available
  from maps or agencies".
  https://www.reddit.com/r/CampingandHiking/comments/1hr2kaw/i_am_curiously_what_you_think/
  (snippet-only; the page was blocked to Hermes).
- No report found evidence that anyone pays for evidence quality or
  provenance by itself (`product-bets.md`, "Bets I would not test yet",
  item 10; `m4-water/decision-packets/monetization.md`).

INFERENCE: the people who feel the pain most sharply are the experienced
ones who already run a five-app stack. They are also the ones who have
already solved it, know the ranger district's phone number, and are the
segment AllTrails found least willing to pay. The people for whom a single
answer would be most valuable are novices, who do not know the question
exists and will not search for "source-backed overnight permission".

**Best counter-evidence.** HERMES-SOURCED: Roadtrippers sells integrated
planning at $35.99 to $59.99 a year and says it has supported more than 38
million trips (https://roadtrippers.com/media-center/, https://roadtrippers.com/);
AllTrails had more than one million subscribers in the cited case study
(https://www.revenuecat.com/blog/growth/alltrails-product-channel); one user
describes paying for a month of a camping service for a trip and cancelling
(https://www.reddit.com/r/vandwellers/comments/1ku0nn7/ok_so_what_do_yall_use_now_that_ioverlander_sucks/).
Outdoor people do pay roughly $30 to $100 a year for planning, offline and
access tools. None of these figures reveals active subscribers or
profitability for an integration product, and none concerns provenance.

**Mitigation.** Only one: ask for money before building more. Nothing in the
code can substitute.

**Assumption to validate, and how cheaply.** That a defined Colorado cohort
will make a real payment for a synthesised activity-plus-overnight answer.
HERMES-SOURCED test: a manually produced trip brief sold at several price
points, measuring paid conversion, refunds and repeat purchase within a
season (`hermes/b9-bear-case.md`, sections a and b). Cost: the owner's time
and a payment link. No accounts, backend or roadmap change needed. Hermes's
proposed kill line is fewer than 10% of qualified prospects paying; that
threshold is Hermes's suggestion, not an evidence-based benchmark.

---

## 2. The honest answer today is "unknown"

**The case (repository facts, not visible to Hermes).** Both pilot regions
declare `camping_permission` and `public_access` as `none`. Aspen has one
reviewed rule record; Douglas has none (`moat-analysis.md`, section 1;
`m8-adventure/ranking-architecture-options.md`, summary item 1). The ranking
study says it plainly: "a design that only ranks options with established
overnight permission returns nothing."

The headline question in `ROADMAP.md` (M8) is "Where can I stay overnight
while I have fun doing the activities I chose?" Camping is M7; matching is
M8; M4 is in progress and will add reviewed water claims for roughly five to
nine waters (`moat-analysis.md`, section 1). The product that the thesis
describes is four milestones away, and when it arrives it will still say
"not established" for almost everything, because the trust principles
correctly forbid inferring permission from a facility, a listing, ownership
or a road (`docs/product/trust-principles.md`, sections 1, 2 and 6).

INFERENCE: this is the structural trap of the whole project. The
differentiator is refusing to guess. A product that refuses to guess is only
as useful as its reviewed claims, and reviewed claims are the scarcest thing
it has. Competitors look more useful precisely because they are willing to
show a pin and a disclaimer. A user comparing the two on a Thursday night
sees one app with two hundred candidate sites and one with a grey map and
the word "unknown". Honesty that returns nothing is not obviously better for
the user than a hedged guess plus a link to the ranger district.

There is a second-order problem. HERMES-SOURCED: the controlling agencies do
publish the answer for specific places: the White River National Forest
lists 22 dispersed sites and a five-day limit at Lincoln Creek
(https://www.fs.usda.gov/r02/whiteriver/recreation/lincoln-creek-dispersed-camping)
and an Aspen Ranger District order running 1 September 2025 to 31 December
2028
(https://www.fs.usda.gov/r02/whiteriver/alerts/aspen-rd-occupancy-and-use-prohibitions).
The material to be honest *and* useful exists for the pilot regions. It has
not been turned into claims.

**Best counter-evidence.** Incumbents disclaim the same question. COTREX's
terms say depiction "is not ... an invitation to all types of travel"
(https://trails.colorado.gov/terms); The Dyrt's layers show where camping
"may" be allowed
(https://support.thedyrt.com/hc/en-us/articles/360049651571-What-map-layers-does-The-Dyrt-PRO-have);
onX advises contacting the land manager
(https://www.onxmaps.com/backcountry/blog/dispersed-camping-what-is-how-to-find).
All HERMES-SOURCED. Nobody answers it well, so a small number of real
answers might stand out.

**Mitigation.** Depth before breadth: a few dozen reviewed overnight claims
for the places people actually go in one region would change "unknown" into
a mix of "prohibited here", "designated sites only", "stay limit applies"
and "not established". This reorders nothing in the roadmap by itself, but
it is in tension with waiting for M7.

**Assumption to validate.** That an honest result with mostly unknowns is
still useful enough to return to. HERMES-SOURCED test: show 20 users cards
with confirmed, restricted and unknown examples and ask what they believe
they may do (`hermes/b9-bear-case.md`, section g; ranked first in
`product-bets.md`). Two weeks, existing data. It tests comprehension. It
does not test whether they would come back.

---

## 3. Reviewed-claim upkeep outgrows one owner

**The case.** Every claim is manual, per place, per activity, and perishable:
stale after 90 days by default and then re-read (`moat-analysis.md`, 3.1).
The moat study's own estimate is that nothing is defensible below "hundreds
to low thousands of reviewed claims, re-reviewed on schedule for at least two
seasons", and that "at the current pace (single-digit claims per milestone)
that is years. The review rate, not the software, is the constraint"
(INFERENCE in that document). Every data change is a pull request the owner
personally approves (`AGENTS.md`).

HERMES-SOURCED evidence that upkeep is expensive even for the well-resourced:

- Gaia GPS dropped Esri World Imagery in March 2025 because licensing costs
  rose.
  https://blog.gaiagps.com/gaia-gps-is-improving-satellite-imagery-saying-goodbye-to-esri-world-imagery/
- 21% of sampled government pages had at least one broken link; 38% of 2013
  pages were gone by 2023.
  https://www.pewresearch.org/data-labs/2024/05/17/when-online-content-disappears/
- COTREX, with more than 230 trail managers (B9) or more than 225 (C8A; the
  reports differ), still warns its data "can still vary in accuracy and
  timeliness".
  https://cpw.state.co.us/news/12042025/colorado-trail-explorer-cotrex-app-shares-trail-closures-protect-wintering-wildlife
- Several agency URLs returned 404 during Hermes's own research
  (`hermes/q3-trip-failure-modes.md`, unknowns), and a source in the pipeline
  has already vanished once and been found by hand
  (`engineering/source-monitoring-architecture.md`, section 1).

Arithmetic, as illustration only. Hermes proposes a ceiling of 15 minutes per
record per month (`hermes/b9-bear-case.md`, recommendation). That number is a
proposed kill criterion, not a measurement; the true rate is UNKNOWN
(`moat-analysis.md`, unknowns).

| Reviewed claims | At 15 min per claim per month | Meaning |
|---:|---:|---|
| 100 | 25 hours a month | A serious hobby |
| 1,000 | 250 hours a month | More than one full-time person |

INFERENCE: the monitoring design does not relieve this. It only opens
issues, never changes a claim, and says of itself that "the real cost is
triage time, not compute" and that "an unattended queue is worse than none,
because it looks like diligence"
(`engineering/source-monitoring-architecture.md`). Agents can draft; under
the trust principles an agent's reading never stands in for review. Review
is the one step that does not parallelise.

**Best counter-evidence.** The site is static and bounded; it can link out
instead of ingesting; the pilot is two counties. The cost per claim has
never been measured, so it may be lower than feared.

**Mitigation.** Cap the catalogue at what measured labour supports; treat
the number of reviewed claims as the scarce budget every milestone spends.

**Assumption to validate.** Minutes per claim per month. HERMES-SOURCED test:
100 pilot records checked weekly for 12 weeks, logging failures, wording
changes and review minutes. The M4-C cycle will produce a first data point
if someone records it as a rate.

---

## 4. No route to users, and no instrument to notice them

**The case.** HERMES-SOURCED: AllTrails' organic growth came from hyperlocal
trail pages plus accumulated user content
(https://www.revenuecat.com/blog/growth/alltrails-product-channel); it later
added paid acquisition, where Apple reports a 119% rise in acquisition in six
months, spend undisclosed (https://ads.apple.com/app-store/success-stories/alltrails).
The top 5% of new subscription apps earn more than 400 times the bottom
quarter after a year, and the bottom quarter earn no more than $19
(https://www.revenuecat.com/pdf/state-of-subscription-apps-2025.pdf).

Project-specific and worse: there are no accounts, no backend and no
analytics (`moat-analysis.md`, section 1; `first-party-data-flywheel-options.md`,
summary). INFERENCE: Ohvernight cannot currently tell whether it has ten
visitors or ten thousand, which features are used, or whether anyone returns.
A single-page map application also gives search engines little to index
compared with a page per trail. The owner has no stated distribution channel
in any document read.

**Best counter-evidence.** HERMES-SOURCED: The Outbound Collective says it
reaches more than 15 million users a year with a small bootstrapped team
(https://www.theoutbound.com/jobs); its age, revenue and acquisition cost are
UNKNOWN. Static, evidence-rich pages for narrow local questions are cheap for
this architecture to produce.

**Mitigation.** Local, non-scalable channels (clubs, outfitters, ranger
districts, Colorado forums) fit two counties. They do not fit a business.

**Assumption to validate.** That search demand exists for
activity-plus-overnight questions that incumbents answer badly.
HERMES-SOURCED test: 20 evidence-rich pages for narrow Aspen and Douglas
questions, 60 to 90 days, measuring impressions and qualified visits. This
requires some privacy-respecting measurement, which is an owner decision the
project has not taken.

---

## 5. Nothing is defensible

**The case.** The moat study's first finding: asked whether an incumbent
could copy each concept in six months, "for most concepts the honest answer
is: they can." Code is public, inputs are public agency data, the schema is
documented, and no software licence file was found at the repository root;
`DATA-LICENSE.md` covers third-party attribution and not Ohvernight's own
curated records (`moat-analysis.md`, summary). The two realistic moats
(reviewed access-rule normalisation and a history of source behaviour) are
labour and elapsed time, and both sit in a public repository where "anyone
can copy them".

Below the product, free: COTREX, Recreation.gov, the NPS app, Organic Maps,
Google Maps offline (HERMES-SOURCED, `hermes/b9-bear-case.md`, section e,
with URLs there). Above it, funded: AllTrails with 100 million members
(https://www.alltrails.com/press/alltrails-community-reaches-100-million-members);
Outside with 25 brands and a bundle (https://www.outsideinc.com/); onX with
a TCV investment (https://www.onxmaps.com/news) and, most pointedly, a
motorised dispersed-camping layer already shipped in Offroad
(https://www.onxmaps.com/news).

INFERENCE: if Ohvernight ever proves the niche pays, it will have proved it
in public, with its method, schema and data available to the company best
placed to scale it.

**Best counter-evidence.** INFERENCE from `moat-analysis.md`: incumbents may
decline to copy, because printing "not established" across a national map
contradicts a coverage story and stating per-place permission invites
liability. HERMES-SOURCED: onX sells each activity separately and says so
(https://support.onxmaps.com/hc/en-us/articles/16141122642829-What-s-the-difference-between-onX-Hunt-onX-Offroad-and-onX-Backcountry),
so the cross-activity seam is real. These are reasons incumbents might not
bother. They are not barriers, and no report contains evidence of any
competitor's plans.

**Mitigation.** None found that fits an open repository. The moat study
frames it as an owner choice: an open trusted reference with no moat "is a
coherent project. It is not a venture-style business."

**Assumption to validate.** Whether the curated corpus is meant to be open.
Cost: a decision, not an experiment.

---

## 6. Every revenue line needs what does not exist

**The case.** HERMES-SOURCED and repository-confirmed: Ohvernight "does not
have accounts, durable cloud-saved trips, notifications, offline packages,
routing, weather, fire or closure feeds, statewide coverage, or a billing
system" (`personas-and-monetization.md`, current behaviour). Saved state is
browser local storage. The browser test harness blocks non-local requests
(`AGENTS.md`). Publication happens only by reviewed merge.

INFERENCE: the strongest recurring-revenue idea in the reports (saved-trip
monitoring) needs accounts, a database, scheduled source checks, notification
delivery and support, and the coordinator has already noted that "a paid
alert that misses a closure is worse than no alert"
(`m4-water/decision-packets/monetization.md`). It scores 2 of 5 for
feasibility with existing data (`product-bets.md`). The project's low running
cost and its auditability come from being static. Monetising means giving
that up, or selling something that needs no backend, such as a one-off brief.

**Best counter-evidence.** A payment link and a manually produced brief need
no backend. Costs of the backend pieces are small in cash terms (see
`business/cost-and-margin-risk.md`).

**Mitigation.** Sequence: sell by hand first, build only what a paid test
has justified.

**Assumption to validate.** Whether a backend is ever acceptable (asked in
`moat-analysis.md`, `first-party-data-flywheel-options.md` and
`engineering/source-monitoring-architecture.md`, and not yet answered).

---

## 7. Two regions cannot carry an annual price

**The case.** HERMES-SOURCED: "a one-region static product may not provide
enough repeat workflow value to sustain an annual subscription"; "deep
Aspen-area and Douglas County coverage can validate the workflow but may be
insufficient for a broad Colorado subscription"
(`personas-and-monetization.md`, Option A weakness and risk 5). INFERENCE:
the two regions are also unlike each other (a destination valley and a Front
Range county), so few users plan in both, and a weekend camper exhausts either
in a season. onX's smallest sold unit is a whole state at $34.99 a year
(https://www.onxmaps.com/hunt/app/pricing, HERMES-SOURCED).

**Best counter-evidence.** Depth in one valley could be worth paying for
once, per trip, to a visitor with fixed dates. That is a trip-pass argument,
not a subscription argument.

**Mitigation.** Sell per trip or per season while coverage is narrow.
Expansion to statewide runs straight into reason 3.

**Assumption to validate.** Trips per person per year inside the covered
area. Ask in the concierge test; costs nothing extra.

---

## 8. Someone reads the map as permission, or a restriction goes stale

**The case.** HERMES-SOURCED: closures shown in COTREX are "mandatory and
enforceable"
(https://cpw.state.co.us/news/12042025/colorado-trail-explorer-cotrex-app-shares-trail-closures-protect-wintering-wildlife);
corner-crossing litigation ran for years over what parcel geometry implies
(https://law.justia.com/cases/federal/appellate-courts/ca10/23-8043/23-8043-2025-03-18.html);
hikers blamed AllTrails for a 2025 rescue, which AllTrails disputed
(https://cowboystatedaily.com/2025/09/29/hikers-rescued-from-medicine-bow-peak-say-gps-app-led-them-astray/);
Appalachian Trail managers report users repeating illegal campsites learned
from apps (https://news.vt.edu/articles/2025/03/clahs-trail-technology-research.html,
18 managers, qualitative).

Project-specific: one owner, no entity, legal review or insurance mentioned
in any document read (UNKNOWN whether they exist). M8 pairs overnight places
with activities by proximity, and "proximity is not a connection" is a trust
principle; the ranking study notes that a single score carries "highest risk
of implying endorsement".

**Best counter-evidence.** This is the risk the project has worked hardest
on: fail-closed positive claims, staleness never weakening a restriction,
fixed wording, validator rules. HERMES-SOURCED: no adjudicated case was found
holding an outdoor-planning app liable for an inaccurate access
recommendation (`hermes/b9-bear-case.md`, unknowns). Likelihood is lower here
than at any competitor.

**Mitigation.** Already in place in the data contract. Residual: charging
money raises the standard of care in users' eyes, and a paid recommendation
reads as an endorsement.

**Assumption to validate.** That users do not read "near", "public" or
"mapped" as "allowed" despite the wording. Same comprehension test as
reason 2.

---

## 9. Seasonality and churn

**The case.** HERMES-SOURCED: across more than 75,000 subscription apps,
nearly 30% of annual subscriptions were cancelled in the first month;
inexpensive annual plans retained up to 36% after a year; expensive monthly
plans retained 6.7%; "not enough usage" was the leading cancellation reason
at 32% to 47%
(https://www.revenuecat.com/pdf/state-of-subscription-apps-2025.pdf). These
are general app benchmarks; no outdoor-specific churn cohort was found.
Complaint mining finds recurring resentment of annual auto-renewal across
AllTrails, Gaia, The Dyrt and others (`hermes/q2-complaint-mining.md`,
theme 3, URLs there).

**Best counter-evidence.** Colorado has winter and summer seasons; whether
Ohvernight's cohort plans in both is UNKNOWN. Campnab sells pay-per-use scans
for infrequent campers alongside memberships (https://campnab.com/faq,
HERMES-SOURCED), so per-trip pricing has precedent.

**Mitigation.** Trip or season passes; annual only for repeat buyers.

**Assumption to validate.** Second purchase within a season. Falls out of
the concierge test.

---

## 10. People pay for offline maps

**The case.** HERMES-SOURCED: offline is the standard paywall at onX,
AllTrails, Gaia, Trailforks, CalTopo and iOverlander
(`hermes/p1-competitive-landscape-and-pricing.md`, finding 4, URLs there);
an independent builder made offline the only paid feature because users
dislike broad paywalls
(https://www.reddit.com/r/overlanding/comments/1ibq1dh/after-two-years-of-teaching-myself-to-code-i/).
The synthesis scores an offline package's defensibility at 2 of 5. A static
web app is the wrong tool to compete with mature offline engines, and offline
reliability failures are "trip-ending" for incumbents with far more
engineering (`hermes/q2-complaint-mining.md`, theme 4).

**Best counter-evidence.** HERMES-SOURCED: Roadtrippers charges at lower
tiers that exclude offline (https://roadtrippers.com/), and free products
(COTREX, Google Maps, Organic Maps) already give offline maps away, so
offline alone is not what is scarce. Which feature actually causes purchase
is UNKNOWN in every report.

**Mitigation.** A printable or downloadable evidence dossier, not a map
engine. The trust boundary requires a free version of the critical
restrictions regardless.

**Assumption to validate.** HERMES-SOURCED test: three prototypes (planning
only; plus dossier; plus offline map) and measure real checkout.

---

## 11. Key sources stay closed

**The case.** HERMES-SOURCED: COTREX's terms prohibit reposting, copying and
using its geographic data "to create or augment another dataset"
(https://trails.colorado.gov/terms). `ROADMAP.md` makes M6 "subject to
licensing/terms verification" and records that no COTREX content is in the
repository. CAIC and CPW structured data are likewise closed until terms are
answered (`moat-analysis.md`, section 1). RIDB access is revocable and may be
rate-limited or charged above a volume
(https://ridb.recreation.gov/access-agreement-ridb). USGS has already retired
the hydrography dataset M4 is built on
(https://www.usgs.gov/national-hydrography/national-hydrography-dataset;
recorded as debt in `ROADMAP.md`).

**Best counter-evidence.** Federal sources are public domain; USFS trail and
road data exists independently of COTREX. A written COTREX agreement would be
an advantage others lack; whether CPW would grant one is UNKNOWN.

**Mitigation.** Ask CPW in writing early. Cost: one letter.

---

## 12. The process is a single point of failure

**The case (project-specific).** One human approves every merge. If the
owner stops for three months, every claim passes its 90-day age: restrictions
correctly remain in force and are flagged, supportive claims degrade to
unknown, and the product quietly returns to an unannotated map. The moat
study records that "even a capable research agent proposed 'access allowed'
against the rules, and that every sentence becoming a restriction or
permission is re-checked by hand". INFERENCE: agents make the building cheap
and make the reviewing more necessary, not less. The cost of agent
subscriptions and model usage appears in no report (UNKNOWN).

**Best counter-evidence.** The repository is the source of truth and is
unusually well documented; a successor could pick it up. Failing closed is
the right way to degrade.

**Mitigation.** None found for the bus factor short of a second reviewer.

---

## What would change my mind

**Toward optimism:**

- Strangers (not friends) pay for a manually produced Aspen or Douglas trip
  brief, and a meaningful share buy a second one in the same season.
- Measured review labour comes in well under Hermes's 15-minutes-a-month
  ceiling across a 100-claim sample over 12 weeks.
- A few dozen reviewed overnight claims in one region make the product
  visibly more useful than the incumbents for the same 25 trip tasks, judged
  by people who do not know which is which.
- Twenty narrow local pages earn non-branded search traffic in 90 days.
- CPW answers a written request about COTREX with a yes.
- A Colorado organisation (a tourism office, an outfitter association, a
  land-manager partner) asks, unprompted, to use or fund the claims.

**Toward concluding it is not a business:**

- Fewer than about one in ten qualified prospects pays for the brief, or
  nobody buys twice.
- Comprehension testing shows users still read "public" or "nearby" as
  "allowed".
- The review queue falls behind within one season at pilot scale.
- An incumbent ships claim-level, dated, source-linked permission statements
  for Colorado. onX is the one to watch.
- The owner decides the curated corpus is open and no backend is ever
  acceptable. Both are respectable choices; together they describe a public
  good, not a company.

## Overall judgement

In plain words: there is a real hole in the market and no evidence yet that
anyone will pay to have it filled. The product is honest, careful and, for
the question it claims to answer, currently empty. The plan to fill it runs
through four more milestones and an amount of manual review that one person
cannot sustain much past two counties. Nothing that gets built can be kept
from a competitor.

As a business, on today's evidence, I would bet against it. Not because the
idea is wrong, but because the things most likely to kill it (no demand
signal, no distribution, review labour, an empty core answer) are exactly the
things no milestone on the roadmap addresses, while the things the roadmap
addresses superbly (trust semantics, data contracts, careful rendering) are
not what is in doubt.

As an open, trustworthy reference for two regions, it is already succeeding
and could continue to at almost no cash cost.

The cheapest useful thing the owner could learn costs no code: whether ten
strangers will pay for a hand-made answer. Until that is known, every
business-model document in this directory, including the companion ones
written today, is arranging furniture in a house nobody has asked to live in.
