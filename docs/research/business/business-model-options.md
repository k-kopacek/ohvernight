DRAFT - UNREVIEWED

# Business model options

Status: options for the owner, written 2026-10-07. This document does not
select a model, set a price or change the roadmap. No web access was used.

Labels: **HERMES-SOURCED** means a figure or fact from an unverified Hermes
web research report; its URL is carried through. **INFERENCE** is this
document's reasoning. **UNKNOWN** means the reports do not support a figure.
All arithmetic is **ILLUSTRATION**: stated assumptions run through published
prices to show the shape of a model. None of it is a forecast, and none of
the prices used is a proposed Ohvernight price.

## Summary

Three models are described: CONSERVATIVE (stay static, sell hand-made trip
answers one at a time), BALANCED (a free evidence map with a paid web
account for saving, comparing, packaging and later monitoring plans) and
AGGRESSIVE (a statewide app with offline packages, alerts, referral revenue
and a professional data product). They differ less in price than in what has
to exist before the first dollar: nothing, a small backend, or a company.

Three findings hold across all of them. First, cash costs are small at
every scale the reports can price; the binding cost in each model is the
owner's time, which no report values. Second, no report contains evidence
that anyone will pay Ohvernight anything, so every "what would have to be
true" list starts with the same untested item. Third, the trust principles
remove the easiest paywalls: anything that says whether something is
allowed, restricted, prohibited or unknown, and where that came from, cannot
sit behind payment in any model.

## What is common to all three

**The trust boundary.** Under `docs/product/trust-principles.md`, unknown is
never resolved by inference, positive claims fail closed, staleness never
weakens a restriction, and presentation (including ordering and ranking)
must not exceed the evidence. Applied to money:

- **Paywalling a restriction is unacceptable.** A closure, prohibition,
  stay limit, fire order or "not established" state that a user can only see
  after paying is a breach of the principles, not a pricing choice. The same
  holds for source, authority, review date and freshness.
- Free and paid users get identical screening. Payment may buy more
  comparison, storage, packaging or automation. It may never buy a more
  truthful answer.
- A saved plan must keep showing a newly known restriction after a
  downgrade, lapse or expiry.
- Compensation of any kind must not alter order, position or wording.
- Monitoring must never let silence read as "nothing changed".

These are the conditions stated in `personas-and-monetization.md` (Part 2)
and endorsed with one caution in
`m4-water/decision-packets/monetization.md`.

**Today's baseline.** A static site on GitHub Pages, USGS basemap tiles, no
backend, no accounts, no analytics, no billing, two regions, and
`camping_permission` and `public_access` coverage of `none`. See
`cost-and-margin-risk.md` for the cost side.

**Fees used in the arithmetic (HERMES-SOURCED).**

| Fee | Published figure | URL |
|---|---|---|
| Stripe, domestic card | 2.9% + $0.30 per transaction | https://stripe.com/pricing |
| Apple, small business | 15% of proceeds | https://developer.apple.com/app-store/small-business-program/ |
| Google Play, first $1M | 15% | https://support.google.com/googleplay/android-developer/answer/112622?hl=en |

One report quotes Stripe at 2.9% + $0.29 from The Dyrt's guidance
(https://support.thedyrt.com/hc/en-us/articles/16722251467796-Should-I-make-my-campground-bookable-with-The-Dyrt);
Stripe's own page says $0.30. The difference does not change any result
below. Sales tax and business-entity costs appear in no report: UNKNOWN.

**Comparable prices (HERMES-SOURCED; standard, not promotional).**

| Product | Annual | Monthly or short-term | URL |
|---|---|---|---|
| onX Backcountry Premium / Elite | $29.99 / $99.99 | not retrieved | https://www.onxmaps.com/backcountry/app/pricing |
| onX Offroad Premium / Elite | $34.99 / $99.99 | $14.99 (Elite) | https://www.onxmaps.com/offroad/app/pricing |
| AllTrails Plus | $35.99 | none retrieved | https://www.alltrails.com/plans |
| AllTrails Peak | UNKNOWN | UNKNOWN | https://www.alltrails.com/plans |
| CalTopo Mobile / Pro | $20 / $50 | none | https://caltopo.com/about/pricing/individual-accounts/ |
| Trailforks Pro | $53.99 | none | https://www.trailforks.com/pro/compare/ |
| The Dyrt PRO | $59.99 | none retrieved | https://support.thedyrt.com/hc/en-us/articles/360054724311-How-much-does-PRO-cost-What-is-the-renewal-cost |
| Campendium RV PRO | $59.99 | $19.99 | https://campendium.com/membership/ |
| Roadtrippers Basic / Pro / Premium | $35.99 / $49.99 / $59.99 | $11.99 / $16.99 / $19.99 (P1) | https://roadtrippers.com/rv/ |
| iOverlander Pro / Unlimited | $59.99 / $99.99 | not verified | https://ioverlander.com/subscriptions |
| FarOut Unlimited | $96 | $15 a month; $72 per six months | https://faroutguides.com/subscription/ |
| Outside+ (Gaia + Trailforks + media) | $89.99 | none | https://www.outsideonline.com/outsideplus-salesevents/?scope=anon |
| Strava | $79.99 | $11.99 | https://www.strava.com/pricing?hl=en-GB |
| Harvest Hosts | $99 to $179 | none | https://www.harvesthosts.com/plans |
| Sēkr+ | $18.99 (P1; C8B says current price UNKNOWN) | $1.99 | https://apps.apple.com/us/app/s%C4%93kr-vanlife-roadtrip-camp/id1447689037 |
| Campnab alerts | $90 / $180 / $270 | $10 / $20 / $30; pay-per-use $10 to $20 | https://campnab.com/pricing |
| Schnerp alerts | not retrieved | $15 / $29; free tier of 10 notifications | https://www.schnerp.com/pricing |
| Campflare alerts | free | free | https://campflare.com/support |

Reports disagree on Gaia GPS: $59.90 a year (P1,
https://www.gaiagps.com/premium); $39.99 in a publisher article that is not
a pricing page (P18); official checkout unreadable (C8A). Treat the current
price as UNKNOWN. Outside+ appears as $89.99 (P18, C8A, Trailforks) and as
$71.99 first-year (P1); the latter looks promotional.

Hermes's own summary of these: roughly $30 to $60 a year for mainstream
planning and offline subscriptions, $60 to $100 for specialist tiers, about
$15 a month for temporary access (`personas-and-monetization.md`).

---

## CONSERVATIVE

**Shape.** Stay exactly as built. The site and every fact on it are free.
Revenue, if any, comes from a one-off product delivered outside the site: a
hand-made or semi-automated trip brief for a specific trip in a covered
region, bought through a hosted payment link. Optionally a way to support
the project.

**Free.** The whole site: map, layers, claims, sources, dates, unknowns,
and a printable summary of the known restrictions for a place.

**Paid.** A trip brief: selected activities, two or three candidate
overnight options, the restrictions that apply, what is not established,
official links, and what to check before leaving. Paid for the labour of
assembly. Every fact in it is also free on the site or at its source.

**Price logic from comparables (ranges only).** Per-use prices in the
reports: Campnab pay-per-use scans at $10 to $20 (https://campnab.com/faq);
FarOut individual guides at $9.99 to $74.99 (P1,
https://faroutguides.com/subscription/); a month of a specialist product at
about $15 (FarOut, onX Elite). Hermes proposed testing a brief at $9, $19 and
$39; those are test cells, not comparables.

**Revenue lines.**

| Line | Realistic? |
|---|---|
| Subscription | None in this model |
| Alerts or monitoring | None |
| Booking or affiliate | Outbound links only, unpaid |
| B2B or API | None; a conversation with a local organisation costs nothing to have |
| Grants or sponsorship | UNKNOWN. No report researched grants, public funding or sponsorship. A static, open, evidence-first public-lands reference is the kind of thing that sometimes attracts them; that is INFERENCE with no evidence behind it |
| Donations | UNKNOWN; no evidence either way |

**Must be built that does not exist.** Nothing in the product. A payment
link and a delivery routine. No accounts, backend or app.

**Costs triggered.** Payment fees per sale. The owner's time per brief
(UNKNOWN; never measured). Possibly a role mailbox. Hosting unchanged.

**Trust conflicts.** Few. The main one is new: a paid, personalised brief
reads as a recommendation, and the reports say formal legal review and
insurance would be required "before marketing the service as authoritative
or personalized" (HERMES-SOURCED, `hermes/b9-bear-case.md`, section g). The
brief must also be able to say "no supported overnight option found" and
still be worth the price, which today it often would.

**Seasonality and churn exposure.** Low by construction: nothing renews.
Demand will follow the season, and revenue goes to zero when the owner is
unavailable.

**ILLUSTRATION: what covers costs.**

Assumptions: Stripe at 2.9% + $0.30; sale prices at the two ends of the
Campnab pay-per-use range, used only as placeholders; added cash cost of
running the site, zero.

| Sale price | Fee | Net per brief |
|---:|---:|---:|
| $10 | 0.029 × 10 + 0.30 = $0.59 | $9.41 |
| $20 | 0.029 × 20 + 0.30 = $0.88 | $19.12 |

Paying users needed to cover cash costs: effectively one, because there are
none. The real equation is hours. If a brief takes one hour (assumption; the
true figure is UNKNOWN), the owner earns $9.41 to $19.12 an hour before tax.
At two hours, half that. To reach a round $10,000 in a year at these
placeholder prices: 10,000 ÷ 19.12 = 524 briefs, or 10,000 ÷ 9.41 = 1,063.
INFERENCE: as income this model does not work at per-use app prices. Its
value is as an instrument: the cheapest possible test of whether anyone pays.

**What would have to be true.** Strangers pay; a useful share pay twice;
brief assembly gets fast enough to be worth doing; coverage in one region is
deep enough that the brief usually has something to say.

**Earliest honest evidence it is working.** Paid orders from people the
owner does not know, and second orders from the same people within a season.
Not sign-ups, not compliments, not traffic.

---

## BALANCED

**Shape.** The free evidence map stays as it is. A paid web account adds
persistence and workflow: saved plans that keep their evidence dependencies,
side-by-side comparison of complete activity-plus-overnight candidates, a
richer downloadable trip dossier, and, only once source monitoring exists
and its coverage can be stated, rechecks of a saved plan before departure.
Sold on the web, by season or year. This is Options A and B of the Hermes
decision packet, in sequence.

**Free.** Everything in CONSERVATIVE, plus basic matching, the reason a
candidate is or is not supported, and a plain printable summary of critical
restrictions and source dates.

**Paid.** More saved plans, comparison depth, reusable vehicle and overnight
preferences, exports, the richer dossier, and later monitored plans with
change reports.

**Price logic from comparables (ranges only).** Planning-only bundle:
the $30 to $60 mainstream band (onX Premium $29.99 to $34.99, AllTrails Plus
$35.99, Roadtrippers $35.99 to $59.99, CalTopo Pro $50). With monitoring and
dossier: Hermes cites roughly $35 to $80. Season or trip window: FarOut at
$15 a month and $72 per six months, onX Elite at $14.99 a month. Low
outlier: Sēkr+ at $18.99 a year. Standalone alert comparables: Campnab $10
to $30 a month, Schnerp $15 and $29, against Campflare at free.

INFERENCE on those anchors: every comparable covers a state, a country or
the world, with offline maps included. Ohvernight covers two counties
without them. The comparables are a ceiling, probably a distant one.

**Revenue lines.**

| Line | Realistic? |
|---|---|
| Subscription or season pass | The core line |
| Alerts or monitoring | A component of the paid tier once it can be run honestly; not sold before |
| Booking or affiliate | Optional outbound links; see trust conflicts |
| B2B or API | Not built. Interviews only |
| Grants or sponsorship | UNKNOWN, as above |

**Must be built that does not exist.** Accounts and sign-in; a database for
saved plans; entitlements; payments and tax handling; transactional email;
the source monitor (`engineering/source-monitoring-architecture.md`) and a
way to tie a saved plan to the claims it depends on; a privacy policy,
terms, data export and deletion; a support channel. The browser test harness
blocks non-local requests today, and publication happens only by reviewed
merge, so this is an architecture and governance change, not only code.

**Costs triggered.** Small in cash: a dynamic host, email, payment fees
(prices in `cost-and-margin-risk.md`). Large in attention: support, refunds,
account problems, and the monitor's triage queue, which its own design
calls "the real cost".

**Trust conflicts.**

- Monitoring: "a paid alert that misses a closure is worse than no alert"
  (coordinator's note, `m4-water/decision-packets/monetization.md`). Every
  alert must state coverage, last check, failed sources and gaps.
- A paywall beside a safety product creates pressure to move useful things
  upward. Complaint mining shows that reshuffling features into higher tiers
  is one of the most resented things incumbents do (AllTrails Peak:
  https://nz.trustpilot.com/review/alltrails.com).
- Paid comparison is paid ranking. The ranking study warns a single score
  carries the "highest risk of implying endorsement"
  (`m8-adventure/ranking-architecture-options.md`).
- Location histories and saved trips become data the project holds, with
  the privacy duties that follow (not researched in any report).
- Affiliate links, if added: see AGGRESSIVE.

**Seasonality and churn exposure.** High. HERMES-SOURCED general benchmarks:
nearly 30% of annual subscriptions cancelled in the first month; inexpensive
annual plans retain up to 36% after a year; expensive monthly plans 6.7%;
"not enough usage" is the leading reason at 32% to 47%
(https://www.revenuecat.com/pdf/state-of-subscription-apps-2025.pdf). No
outdoor-specific figure exists in the reports. A two-county product used a
few times a year is close to a worst case for "not enough usage".

**ILLUSTRATION: what covers costs.**

Assumptions: web sales through Stripe (2.9% + $0.30); annual prices at the
ends of the mainstream band, $30 and $60, as placeholders; fixed cash costs
of Cloudflare Workers Paid at $5 a month
(https://developers.cloudflare.com/workers/platform/pricing/) and Resend Pro
at $20 a month (https://resend.com/pricing), so $25 a month, $300 a year.
Database, authentication, tax tooling and domain costs are not priced in
P18: UNKNOWN, so $300 is a floor.

| Annual price | Fee | Net per payer |
|---:|---:|---:|
| $30 | 0.029 × 30 + 0.30 = $1.17 | $28.83 |
| $60 | 0.029 × 60 + 0.30 = $2.04 | $57.96 |

| To cover, per year | At $30 | At $60 |
|---|---:|---:|
| Fixed cash floor, $300 | 300 ÷ 28.83 = 11 payers | 300 ÷ 57.96 = 6 payers |
| Owner target of $10,000 (placeholder) | 347 | 173 |
| Owner target of $50,000 (placeholder) | 1,735 | 863 |
| Owner target of $100,000 (placeholder) | 3,469 | 1,726 |

The owner targets are round placeholders so the scale can be seen. No report
states what the owner's time is worth or what the owner needs.

Churn on top, using the best-case benchmark of 36% retained after a year:
holding 347 payers steady means replacing 64% of them, 0.64 × 347 = 222 new
payers every year. At the first-month figure, nearly 30% of each new annual
cohort is gone within weeks (refund treatment UNKNOWN).

How many visitors that requires cannot be computed: no report contains a
verified free-to-paid conversion rate for any outdoor product (P18,
"UNKNOWN").

**What would have to be true.** People pay for workflow when every fact is
free. Coverage becomes wide enough (at least statewide for the places people
go) that a season of use is plausible. The owner accepts a backend, accounts
and personal data. Review labour per claim is low enough to sustain that
coverage. Monitoring can be run with honestly stated coverage.

**Earliest honest evidence it is working.** In order: repeat use of saved
plans across more than one trip by the same people, measured before any
billing exists (Hermes's "retention test before billing"); then paid
conversion from that group; then renewal or a second season purchase.
Renewal is the first real signal and it is at least a year away from launch.

---

## AGGRESSIVE

**Shape.** Compete as a product: statewide Colorado coverage, a native app
with offline trip packages, push and text alerts on saved plans, referral
revenue on outbound bookings and memberships, a professional evidence
licence or API for Colorado organisations, and possibly a live
visitor-observation layer.

**Free.** The same floor as the other two. It does not move.

**Paid.** A higher tier with offline packages and monitored plans; referral
commissions; professional licences.

**Price logic from comparables (ranges only).** Consumer: the $60 to $100
specialist band (The Dyrt PRO $59.99, onX and iOverlander top tiers $99.99,
FarOut $96, Outside+ $89.99). Professional: CalTopo commercial teams from
$500 a year for up to ten users (https://caltopo.com/about/teams/) and Avenza
Pro from $169.99 a year per device
(https://store.avenza.com/pages/pricing), both from P1. Data licensing:
Campflare, Outdooractive and onX publish no commercial price (P18): UNKNOWN.
Referral: Harvest Hosts offers partners 35% of new sign-ups
(https://support.harvesthosts.com/en/articles/6112015-do-you-have-a-partner-or-affiliate-program-for-content-creators),
though its terms say the applicable rate is set in the affiliate dashboard;
Amazon pays 3.00% on outdoors
(https://affiliate-program.amazon.com/help/node/topic/GRXPHT8U84RAYDXZ). No
general campground-booking affiliate rate, REI rate or gear-rental rate was
found: UNKNOWN. Hipcamp's 15% is what hosts pay Hipcamp
(https://support.hipcamp.com/hc/en-us/articles/360024823412-How-much-does-it-cost-to-list-on-Hipcamp-and-is-there-a-commission-fee);
it is not a referral rate. Recreation.gov has no referral programme in any
report, and no reservation money goes to its contractor
(https://www.recreation.gov/faq).

**Revenue lines.**

| Line | Realistic? |
|---|---|
| Subscription | Yes, in principle, at statewide scope |
| Alerts or monitoring | Trip-claim monitoring: possible, expensive to run honestly. Campground availability alerts: no. A free specialist exists, and the reports advise against competing there |
| Booking or affiliate | Thin and unevidenced. Federal and state campgrounds, the bulk of public-land inventory, pay nothing |
| B2B or API | Demand UNKNOWN (HERMES-SOURCED as an explicit unknown). Requires clear rights to the data and service commitments one person cannot easily give |
| Grants or sponsorship | Harder to square with a commercial app; UNKNOWN |

**Must be built that does not exist.** Everything in BALANCED, plus: a
native app on two platforms; an offline package format and tile hosting;
push and text delivery; store billing; partner integrations and tracking;
an API with stable identities, documentation and uptime; if observations are
included, the full platform of
`first-party-data-flywheel-options.md` Option 3 (database, moderation,
reputation, takedown, someone on call), which that document says would let
content reach users "without the owner approving each item".

**Costs triggered.** Store commission; tile and storage costs that scale
with sessions and downloads; text-message fees (not priced in any report:
UNKNOWN); parcel data if ownership is shown ($100 to $400 per county file:
https://regrid.com/blog/datastore); moderation; support; and above all
reviewed coverage for a state. See `cost-and-margin-risk.md`.

**Trust conflicts.** This is where they concentrate.

- **Affiliate and booking incentives run directly against evidence-first
  honesty.** A referral pays when the user clicks through and buys. "Not
  established" and "prohibited here" pay nothing. The places that pay
  (private hosts, memberships, commercial campgrounds) are not the places
  the product is about (public land). Any ordering that favours paying
  destinations, or any softening of an unknown beside a paid link, breaches
  trust principle 7. The decision packet's rule is that compensation "must
  never override evidence quality, restrictions, safety, or user
  constraints". INFERENCE: the rule is easy to write and hard to keep once a
  revenue line depends on click-through.
- **Offline packages age.** A downloaded packet is a snapshot; a restriction
  issued after download is invisible. A free way to carry critical
  restrictions offline must exist, or the paywall is on safety.
- **A professional licence for claims** that are also published free in a
  public repository is selling service, history or convenience, not the
  data. Whether the curated corpus is open is undecided
  (`moat-analysis.md`, section 5).
- **Observations** invite users to read "people camped here" as permission.
  The design forbids it; the residual risk it names (false restriction
  reports as the cheapest attack) remains.
- **Scale itself.** Statewide coverage with thin review would put "unknown"
  on most of the map or tempt the product to fill gaps. The second is a
  breach; the first undermines the price.

**Seasonality and churn exposure.** Highest. Fixed obligations (apps,
support, monitoring, partner commitments) continue through shoulder seasons
while usage does not. Referral revenue follows bookings, which are seasonal:
HERMES-SOURCED, 55.9% occupancy for seasonal campgrounds in June 2025
(https://ohi.org/wp-content/uploads/2025/07/The-Data-Dig_June-2025.pdf).

**ILLUSTRATION: what covers costs.**

Assumptions: in-app sales at the 15% small-business rate; annual prices at
$60 and $100 as placeholders from the specialist band; fixed cash floor of
Workers Paid $5, Resend Scale $90 and MapTiler Flex $30 a month
(https://www.maptiler.com/cloud/pricing/), so $125 a month, $1,500 a year.
Developer-programme fees, text messages, database, moderation tooling,
insurance and any hired help are not priced in the reports: UNKNOWN, so the
floor is far below the real figure.

| Annual price | Store commission (15%) | Net per payer |
|---:|---:|---:|
| $60 | $9.00 | $51.00 |
| $100 | $15.00 | $85.00 |

| To cover, per year | At $60 | At $100 |
|---|---:|---:|
| Fixed cash floor, $1,500 | 1,500 ÷ 51 = 30 payers | 1,500 ÷ 85 = 18 payers |
| $100,000 (placeholder, about one person) | 1,961 | 1,177 |
| $300,000 (placeholder, a very small team) | 5,883 | 3,530 |

At the best-case 36% annual retention, holding 1,961 payers requires 0.64 ×
1,961 = 1,255 new payers a year. Acquisition cost per payer is UNKNOWN in
every report.

Referral lines, same caution. Harvest Hosts at 35% of a $99 membership is
$34.65 per referred sign-up, or $27.72 if the share applies to the price
after the 20% audience discount (which basis applies is UNKNOWN). $10,000 a
year needs 289 to 361 referred sign-ups from a membership aimed at
self-contained RVs. Amazon at 3%: $10,000 needs $333,333 of gear bought
through links. INFERENCE: referral income at Ohvernight's plausible traffic
is a rounding item with a disproportionate trust cost.

Professional line: at CalTopo's $500 team anchor, $100,000 needs 200
organisations; the number of plausible Colorado buyers is UNKNOWN and nobody
has asked one.

**What would have to be true.** Paid demand already proven at smaller scale.
Capital or co-workers; this is not a one-person model. Review labour low
enough for statewide coverage, or a decision to accept thin coverage and say
so. Written data rights (COTREX above all). The owner willing to hold
personal data, run moderation, sign commercial terms and change the rule
that all publication is by reviewed merge. Incumbents not responding.

**Earliest honest evidence it is working.** None is available early; that
is the nature of the model. The first honest signals are paid retention
across two seasons and a professional customer who renews. Downloads, press
and partner logos are not evidence.

---

## Side by side

| | CONSERVATIVE | BALANCED | AGGRESSIVE |
|---|---|---|---|
| First dollar requires | A payment link | Accounts, payments, backend | App, backend, partners, statewide data |
| Architecture | Unchanged | Static site plus a service | A platform |
| Governance change | None | Holding user data; scheduled source contact | Unreviewed user content; commercial obligations |
| Cash cost floor (reports) | About zero | About $300 a year plus UNKNOWNs | About $1,500 a year plus large UNKNOWNs |
| Binding cost | Owner hours per brief | Owner hours on review, support, triage | People |
| Payment fees | Stripe | Stripe | 15% store commission |
| Trust risk | Low; paid advice reads as endorsement | Medium; missed alerts, tier creep, ranking | High; affiliate incentives, stale offline, observations |
| Churn exposure | None (no renewals) | High | Highest |
| Works at two regions? | Yes | Doubtful | No |
| Earliest real signal | Weeks | A season, then a year for renewal | Two seasons |
| Reversible? | Completely | Mostly; saved plans must be exportable | Poorly |

---

## Cross-cutting evidence from the reports

### Annual versus monthly

HERMES-SOURCED facts:

- The market sells annual. AllTrails, Outside+, The Dyrt, Trailforks and
  CalTopo show no monthly price in any report.
- Where monthly exists it is priced to discourage. Twelve months at the
  monthly rate, divided by the annual price: Campendium RV PRO 12 × 19.99 ÷
  59.99 = 4.0; Roadtrippers Premium the same; Strava 12 × 11.99 ÷ 79.99 =
  1.8; onX Elite 12 × 14.99 ÷ 99.99 = 1.8; FarOut 12 × 15 ÷ 96 = 1.9.
- iOverlander raised monthly prices about 50% for new subscribers in January
  2026 and left annual alone (https://ioverlander.com/whats_coming).
- Retention favours cheap annual plans (up to 36% after a year) over
  expensive monthly ones (6.7%); nearly 30% of annual plans are cancelled in
  month one (https://www.revenuecat.com/pdf/state-of-subscription-apps-2025.pdf).
- Trials range from 7 days (AllTrails, onX) through 30 (Strava) to 90
  (Outside+, The Dyrt), per P18.
- Users resent annual auto-renewal and work around it: cancelling trials at
  once, calendar reminders, a month bought for a trip and cancelled
  (`hermes/q2-complaint-mining.md`, theme 3;
  https://www.reddit.com/r/vandwellers/comments/1ku0nn7/ok_so_what_do_yall_use_now_that_ioverlander_sucks/).
- Campnab offers pay-per-use for infrequent campers beside memberships
  (https://campnab.com/faq). FarOut sells a six-month season pass.

INFERENCE: annual billing is how incumbents survive seasonality, by
collecting in June for a product unused in November. It is also what users
most dislike. A seasonal or per-trip term fits the trust posture and the
usage pattern and gives up the forgotten-renewal revenue the incumbents
depend on. Whether a temporary option actually reduces resistance is UNKNOWN
(`personas-and-monetization.md`, unknowns).

### Willingness-to-pay signals

- People in this market pay $30 to $100 a year, and some pay for several
  products. HERMES-SOURCED panel data: 13.8% of 2,026 onX Offroad
  subscribers and 4.2% of 7,354 onX Hunt subscribers also paid for AllTrails
  between August 2024 and August 2026 (https://ask.yipitdata.com/insights).
  That is panel overlap, not conversion, and it appears in one report only
  (P18).
- The highest prices attach to certain permission (Harvest Hosts, $99 to
  $179) and to parcel-level land data (onX Elite, $99.99).
- AllTrails found its backcountry and van-life segment "often did not want
  to pay" (https://www.revenuecat.com/blog/growth/alltrails-product-channel).
  That is close to Ohvernight's first persona.
- No signal exists for paying for provenance, evidence quality or an honest
  "unknown" by themselves.
- No signal exists for Ohvernight specifically. Every persona's willingness
  to pay is rated thin, indirect or moderate-by-analogy.

### Conversion drivers

What incumbents put behind the paywall, by frequency in the reports: offline
maps; advanced planning and custom routes; alerts; private-land layers;
vehicle tools; discounts; larger itineraries. Which of these actually causes
purchase is UNKNOWN: "no retrieved evidence isolated whether offline maps,
planning, safety, community, or another feature causes outdoor-app purchase"
(`hermes/b9-bear-case.md`). No verified conversion, retention or churn rate
was found for any named outdoor product (P18).

What drives users away is better evidenced: features moved to a higher tier,
unclear renewals, paying for what feels public, and stale crowd data.

### Offline-map value

Offline is the most common paid boundary and the most common source of
trip-ending complaints (lost downloads, forced logins without service:
`hermes/q2-complaint-mining.md`, theme 4). It is also free from COTREX,
Google Maps, Organic Maps and Avenza's base tier. Roadtrippers puts it only
in its top tier and still sells the tiers beneath. The synthesis scores an
offline package 2 of 5 for defensibility. One independent builder made
offline the only paid feature because it has a direct cost and users accept
it
(https://www.reddit.com/r/overlanding/comments/1ibq1dh/after-two-years-of-teaching-myself-to-code-i/).

INFERENCE: offline maps are valuable to users and worthless as a
differentiator. For Ohvernight the relevant product is an offline evidence
dossier (rules, dates, contacts, unknowns), which is cheap to produce, needs
no tiles, and has no demand evidence at all. A free critical-restrictions
version is required whatever is charged for the richer one.

### Monitoring value

For: paid alerts exist (The Dyrt and Campendium inside $59.99 tiers; Campnab
and Schnerp at $10 to $30 a month); checking fire and closure sources by hand
is documented as fragmented; the failure-mode research finds that trips fail
mostly on a mismatch between plan and current conditions. Hermes ranks
monitoring the top revenue opportunity and the strongest recurring-value
hypothesis.

Against: the paid alert comparables monitor campsite availability, a
structured feed with a clear event, not prose rule changes. A free competitor
exists for that job. The same Hermes material scores monitoring 2 of 5 for
feasibility with existing data, calls its cost to serve "high", and lists
its scalability as unknown. The monitor design is explicit that a clean
check confirms nothing and must not be shown to users as currency
(`engineering/source-monitoring-architecture.md`, section 5, item 11), so
turning it into a paid, user-facing feature needs a new trust-bearing
specification. Reviewers of The Dyrt complain of a paid scanner that found
nothing for weeks.

INFERENCE: monitoring is the best subscription story in the reports and the
furthest from being deliverable. It is also the one paid feature where
failure is not a refund but a harmed user.

---

## Questions the owner must answer to choose

1. **Is this meant to be a business at all,** or an open reference that may
   cover its costs? The three models diverge at this question and nothing
   else resolves it.
2. **What is your time worth, and how much of it is available?** Every
   break-even above is trivial in cash and undefined in hours.
3. **Will you ask strangers for money before M7 and M8 exist?** The
   CONSERVATIVE test needs no code. Not running it is also a decision.
4. **Is a backend acceptable?** Accounts, stored trips and personal data.
   BALANCED and AGGRESSIVE are impossible without one.
5. **Is the curated corpus open?** If claims and their history are free for
   anyone to take, what exactly would a subscriber or licensee be paying for?
6. **Will you ever accept money that depends on a click-through?** If yes,
   what written rule and what test keep it away from ordering and wording?
   If no, AGGRESSIVE loses two of its lines.
7. **Depth or breadth?** Subscription value needs breadth; honest answers
   need depth; review labour limits both.
8. **Is monitoring something you are prepared to operate,** including being
   wrong in front of a paying user?
9. **Annual, seasonal or per trip?** Given what users say about renewals,
   which term are you willing to be judged by?
10. **Is a native app in scope, ever?** It brings store commission, review
    rules and a second codebase.
11. **Would you take outside money or co-workers?** AGGRESSIVE assumes it.
12. **What result, by what date, would make you stop trying to charge?**
    Hermes proposed kill criteria; none has been adopted.
