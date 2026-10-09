DRAFT - UNREVIEWED

# Moat analysis

Status: analysis for the owner, written 2026-10-07. Not a decision, not a
business-model selection and not a roadmap change.

Labels: **HERMES-SOURCED** means the claim comes from a Hermes report the
coordinator has not re-checked. **INFERENCE** is this document's reasoning.
**UNKNOWN** means evidence is missing. Nothing here was checked against the
web. Statements about what onX, AllTrails or any other company would do are
INFERENCE throughout; no report in the repository contains evidence of any
competitor's plans.

## Summary for the owner

The question asked of every concept: if Ohvernight ships this and it works,
why can an incumbent not copy it in six months?

1. **For most concepts the honest answer is: they can.** The code is public,
   the inputs are public agency data, and the features are ordinary product
   work for a funded team. Open-source code and public agency data are not
   moats.
2. **Two candidate moats are realistic, both labour-and-time assets, and
   neither defends anything yet:** reviewed access-rule normalization, and a
   historical record of how sources behave. Each is cumulative, cannot be
   bought off the shelf, and has a reason an incumbent might decline to copy
   it.
3. **Both are undermined by the repository being public.** Reviewed claims
   and their history are committed to a public repository. Anyone can copy
   them. No software licence file was found at the repository root, and
   `DATA-LICENSE.md` covers third-party data attribution, not Ohvernight's
   own curated records. Whether the curated corpus is open is an undecided
   owner question, and it decides whether these two are moats at all.
4. **The durable advantage, if there is one, is a posture and an operation,
   not an asset:** saying "not established" and "prohibited" where a
   coverage-driven product has reasons not to. That is a positioning
   advantage. It protects nothing if an incumbent chooses to match it.

| Candidate moat | Ranking |
|---|---|
| Access-rule normalization | REALISTIC MOAT |
| Historical source freshness | REALISTIC MOAT |
| Normalized cross-domain feature graph | POSSIBLE MOAT |
| Feature-identity reconciliation | POSSIBLE MOAT |
| First-party observations | POSSIBLE MOAT |
| Proprietary user outcomes | POSSIBLE MOAT |
| Provenance / evidence infrastructure | NOT A MOAT |
| Monitoring infrastructure | NOT A MOAT |
| Saved-trip graph | NOT A MOAT |
| User preference history | NOT A MOAT |

This differs from the Hermes synthesis, which calls the evidence/provenance
graph the "strongest potential moat" and source monitoring a "strong
potential moat" (HERMES-SOURCED, `idea-fairy-report.md`, "Product moat
opportunities"). The difference is deliberate and explained in section 2.

## 1. Where Ohvernight stands today

- Two pilot regions. `camping_permission`, `public_access`, `closures` and
  `recreation_permission` are `none` in both manifests; Aspen has one
  reviewed rule record; Douglas has none (`v2/regions/*/region.json`,
  `v2/pipeline/config/rules-registry.json`).
- M4-C will add reviewed water claims for roughly five to nine waters
  (`docs/specs/M4-functional-recreational-water.md`, 9.5).
- No accounts, backend, analytics or users on record
  (`docs/architecture/system-overview.md`). There is no first-party data of
  any kind.
- Sources are public-domain or public agency services with attribution
  duties; several valuable ones are closed until terms are answered: COTREX,
  COMaP, CAIC, CPW structured data (HERMES-SOURCED,
  `future-sources/source-watchlist-m5-m8.md`;
  `docs/research/m4-water/licensing-and-terms.md`).

INFERENCE: on these facts Ohvernight has no moat today. What follows is
about which could exist, when, and at what price.

## 2. Product concepts and the six-month copy test

Concepts are the Tier 1 and Tier 2 candidates of `idea-fairy-report.md` and
the seven bets of `product-bets.md` (all HERMES-SOURCED as concepts and
scores). The copy assessment is INFERENCE.

| Concept (Hermes score) | Could a funded incumbent copy it in six months? | What, if anything, would slow them |
|---|---|---|
| Freshness / "when was this checked?" (90) | The display, yes, in weeks. Claim-level review dates need claim-level review | They would need reviewed claims to date; see access-rule normalization |
| Evidence-backed access confidence (88) | The interface, yes. The content only at the rate people can read orders and operator pages | Labour per jurisdiction; reluctance to print "not established" over most of the map |
| Overnight + activity pairing (85) | Yes. Proximity pairing over their own larger inventories is routine | Nothing structural. They hold more campsites and trails than Ohvernight does |
| Adventure matching (80) | Yes. HERMES-SOURCED: Roadtrippers and Campendium already offer AI-assisted planning (`idea-fairy-report.md`, rejected ideas) | Only the evidence beneath it |
| Saved-trip monitoring (78) | Yes. HERMES-SOURCED: The Dyrt and Campendium already paywall alerts | Trip-to-claim dependencies need claims |
| Trip feasibility on one screen (75) | Yes. Hermes itself says "the one-screen interface is copyable" | The claims beneath it |
| Offline expedition package (75) | Already shipped by most. HERMES-SOURCED: offline is a standard paywall; Hermes scores its defensibility 2 of 5 | Nothing |
| Vehicle-aware access (70) | onX is ahead (HERMES-SOURCED: "onX already has substantial strength") | Ohvernight would be the copier |
| Alternate plans after closure (68) | Yes, once they have monitoring | Evidence for each alternative |
| Dynamic trip confidence (65) | Yes; a score is easy to ship and hard to calibrate for anyone | Outcome data, which nobody in the reports is shown to have |
| First-party local intelligence (63) | Incumbents already collect reports at a scale Ohvernight cannot approach | Strict separation of observation from authority is a design choice they could adopt |
| Multi-day itineraries (63) | Already shipped by Roadtrippers and Campendium (HERMES-SOURCED) | Nothing |

INFERENCE: every concept reduces to the same dependency. The features are
copyable; what is slow to copy is a body of reviewed, dated, per-place
statements of what an authority says, and the discipline of not filling the
gaps. The rest of this document is therefore about assets, not features.

## 3. Candidate moats

### 3.1 Access-rule normalization — REALISTIC MOAT

**What it is.** Turning prose (forest orders, operator recreation pages,
county rules) into per-place, per-activity claims with a status, a reviewer's
summary, a source URL, a review date and a maximum age. The repository does
this today for one rule and will for a few waters (M4 spec section 9).

**Why it could defend.** It is manual, per-jurisdiction and perishable. A
claim goes stale in 90 days by default and must be re-read. HERMES-SOURCED:
there is no national structured endpoint for forest orders; county sheriff
restriction feeds are not standardized (`source-watchlist-m5-m8.md`). The
playbook records that even a capable research agent proposed "access allowed"
against the rules, and that every sentence becoming a restriction or
permission is re-checked by hand (`docs/research/hermes/playbook.md`,
sections 1 and 7). The cost of doing this correctly is real.

**Why an incumbent might not copy it (INFERENCE).** Three structural
reasons, none proven: (a) a national product must cover everywhere, and
claim-level review does not scale to everywhere at a consumer price; (b)
printing "not established" across most of a map contradicts a
coverage-and-confidence product story; (c) stating per-place permission
invites liability that "contact the land manager" avoids. HERMES-SOURCED:
onX's own guidance advises users to contact the land manager and check local
regulations (`hermes/p1-competitive-landscape-and-pricing.md`, finding 7).

**Why it might not defend.** Money buys reviewers. An incumbent could cover
Colorado's most-visited places in a season if it decided the liability was
acceptable. And the claims are in a public repository; unless the owner
decides otherwise they can simply be taken, with their sources.

**Time and data before it defends anything.** INFERENCE: nothing below
statewide coverage of the places people actually go is defensible; two
counties are a demonstration. Order of magnitude: hundreds to low thousands
of reviewed claims, re-reviewed on schedule for at least two seasons, so that
the history shows the operation is real. At the current pace (single-digit
claims per milestone) that is years. The review rate, not the software, is
the constraint.

### 3.2 Historical source freshness — REALISTIC MOAT

**What it is.** A dated record of when each source changed, failed, moved,
changed schema or changed terms; how often an operator rewrites a page; when
seasonal closures were actually posted each year.

**Why it could defend.** It is the only asset on the list that cannot be
bought, licensed or backfilled. A competitor starting in 2028 cannot learn
what a county page said in 2026. HERMES-SOURCED: "a long-running
source-monitoring history reveals source cadence, recurring conflicts, and
coverage gaps that a new competitor would not immediately possess"
(`idea-fairy-report.md`, Tier 1 item 3). It also has compounding internal
uses: setting `max_age_hours` from observed cadence rather than guesswork,
and knowing which sources to distrust.

**Incumbent disincentive (INFERENCE).** None in principle; it is cheap for
them. The protection is purely the head start.

**Why it might not defend.** Its direct user value is modest: users want
today's status, not a source's history. It defends only as an input to
better review policy and, later, to seasonal expectations ("this gate has
opened between these dates in past years", which is itself a current-from-
historical inference the trust principles forbid stating as current). If the
history lives in public issues and commits, it is copyable. If it records
only hashes and not content, much of its analytical value is lost; if it
stores content, licensing questions arise for prose sources that carry no
reuse licence (`m4-water/licensing-and-terms.md`).

**Time and data.** Zero value in year one. Useful internally after one full
season cycle (12 months); arguably defensible after two to three, across
dozens of sources. Requires the monitoring in
`docs/research/engineering/source-monitoring-architecture.md` to start early,
which is its main argument for starting early.

### 3.3 Normalized cross-domain feature graph — POSSIBLE MOAT

**What it is.** One model linking water, land, trails, roads, overnight
places, restrictions and dates. HERMES-SOURCED: both P1 and the synthesis
call this "the defensible product layer".

**Assessment.** The nodes are public agency features. The schema is in a
public repository. Joining public layers is competent GIS work that every
incumbent has already done at national scale for its own domains. What is
not routine is the cross-domain edge that carries a claim, for example "this
campground serves this launch" as a reviewed statement rather than a distance.
Those edges are access-rule normalization under another name.

**Incumbent disincentive (INFERENCE).** Organizational, not structural:
HERMES-SOURCED, the market is "fragmented by job" and onX sells separate
memberships per activity (`p1`, finding 1; `personas-and-monetization.md`,
customer resistance). A company organized by vertical has friction building
across verticals. Friction is not a barrier.

**Time and data.** Requires M4 to M7 complete for at least a state. Until
then it is a design. Defends only to the extent 3.1 does.

### 3.4 Feature-identity reconciliation — POSSIBLE MOAT

**What it is.** Stable IDs, aliases, group membership and merge or split
history: which 96 source segments are one river; which NHD record is which
3DHP record; which COTREX trail is which USFS trail (`ROADMAP.md`, M6 trail
identity; M4 spec section 7 and the 3DHP debt in section 18).

**Assessment.** Tedious, cumulative and necessary. HERMES-SOURCED: called a
"strong foundational moat". INFERENCE: it is a foundation, and a weak moat.
Incumbents maintain their own identity tables and do not need Ohvernight's.
The output is published in the display artifacts and the alias file, so the
crosswalk is copyable by design. Where it could matter is as a public good:
if Ohvernight's IDs became the reference others link to, that is a standards
position, which is a different kind of advantage and an owner choice.

**Incumbent disincentive.** None.

**Time and data.** Statewide crosswalks across at least three source
families, maintained through one upstream migration (NHD to 3DHP is the
first test). Two to three years.

### 3.5 First-party observations — POSSIBLE MOAT

**What it is.** Dated reports of road, trail, water and site conditions from
Ohvernight's own users.

**Assessment.** This is the classic data network effect and the incumbents
already have it. HERMES-SOURCED: Ohvernight "has no demonstrated contributor
or transaction network, while larger competitors already have communities";
contribution density is unknown. Ohvernight starts at zero against products
with large review bodies. HERMES-SOURCED: users also complain that
crowdsourced data goes stale and is sometimes harmful (`p2`, pain theme 4),
which is an opening for a narrower, dated, structured kind of observation,
but an opening is not a moat.

**Incumbent disincentive (INFERENCE).** Slight: their review corpora are
engagement assets, and expiring old reports or refusing new campsite pins
reduces content volume. They could still add an expiry date tomorrow.

**Time and data.** A dense, current observation set in one region: sustained
weekly reports on the same few hundred features through a season. Needs a
backend, moderation and users, none of which exist. Defensible only locally,
and only while density is maintained. Three years or never.

### 3.6 Proprietary user outcomes — POSSIBLE MOAT

**What it is.** What happened: the trip went ahead, was turned back at a
gate, found the site full.

**Assessment.** The only item here that would be truly proprietary: nobody
else could have Ohvernight's users' outcomes. HERMES-SOURCED: "potentially
strong but long-term"; whether users will report outcomes accurately is
unvalidated; the research found no dataset linking planned trips to outcomes
(`idea-fairy-report.md`, unknowns 10; `q3-trip-failure-modes.md`, unknowns).
Two hard limits. First, an outcome can never be evidence of permission
("no inference of legality from successful past use", HERMES-SOURCED), so its
use is confined to calibrating warnings and review priority. Second, it needs
accounts or at least a submission path, consent, and volume.

**Incumbent disincentive.** None. Larger products could collect far more.

**Time and data.** Thousands of reported outcomes with trip context. With no
users today, the horizon is UNKNOWN and long.

### 3.7 Provenance / evidence infrastructure — NOT A MOAT

The claim object, the freshness rule, the validator and the fixed wording are
in a public repository and documented in `v2/pipeline/docs/data-contract.md`.
A competent team could reimplement the model in weeks, and is welcome to.
HERMES-SOURCED: no evidence was found that anyone pays for evidence quality
on its own. The infrastructure is a prerequisite for 3.1 and a credible
signal of intent. It is the container, not the contents. Ranked as it is
because the brief asks about the infrastructure; the contents are 3.1.

Incumbent disincentive (INFERENCE): the same as 3.1(b), a reluctance to show
unknowns, which is a reason they might not want it, not a reason they could
not have it.

### 3.8 Monitoring infrastructure — NOT A MOAT

Scheduled checks, schema fingerprints and page hashes are commodity
engineering; change-detection services exist as products. The design in
`source-monitoring-architecture.md` could be rebuilt by anyone in days. Its
value is that it produces 3.2 and feeds 3.1. The history is the asset; the
scheduler is not.

### 3.9 Saved-trip graph — NOT A MOAT

Saved trips exist in every competitor. HERMES-SOURCED: the asset would be
"the maintained trip-to-source dependency graph", but that graph is only as
good as the claims it points to, and a weekend trip is short-lived, so
switching cost is low (INFERENCE). Today trips are in browser local storage
and Ohvernight cannot see them at all. This is a retention mechanism if
monitoring is built. It defends nothing by itself.

### 3.10 User preference history — NOT A MOAT

HERMES-SOURCED: "Weak moat. Useful infrastructure but easily copied";
defensibility scored 1 of 5. A vehicle class and three activity ticks can be
re-entered in a competing product in a minute. Nothing to add.

## 4. Reading across the list

| Question | Answer |
|---|---|
| What is copyable in six months? | Every feature, the schema, the code, the monitoring, and any data that is public in the repository |
| What is not copyable at any price? | Elapsed time: the history of sources and, if they ever exist, user outcomes |
| What is copyable only with sustained labour? | Reviewed, re-reviewed claims per place |
| What might an incumbent decline to copy? | Showing unknown and prohibited prominently; taking per-place responsibility for a statement |
| What does being open and static cost? | The corpus and its history are takeable. No accounts means no first-party data of any kind |
| What does it buy? | Auditable trust, no engagement incentive, low running cost. These are positioning, not moats |

INFERENCE: the Hermes framing "the likely moat is a system, not one feature"
is fair as a description of how the parts depend on each other. It should
not be read as saying the system is hard to copy. The system is a public
design. The scarce input is reviewed claims kept current, and the scarce
resource behind that is reviewer time.

## 5. Owner decisions this raises

1. Is Ohvernight's curated corpus (claims, crosswalks, change history) meant
   to be open for anyone to reuse? If yes, sections 3.1 and 3.2 are public
   goods, not moats, and that may be the intent. If no, a licence and
   possibly a private store are needed, which conflicts with "the repository
   is the source of truth" as currently practised.
2. No software licence file was found at the repository root. Which licence
   applies to the code?
3. Is a moat wanted at all? An open, trusted reference with no moat is a
   coherent project. It is not a venture-style business. This document does
   not choose.
4. Depth or breadth: deep review of a few regions (strong locally, no state
   coverage) or thin coverage of Colorado (weaker everywhere)? The realistic
   moats need depth sustained over time.
5. Should source monitoring start now, purely to begin accumulating history
   that cannot be backfilled?
6. Is a backend ever acceptable? Sections 3.5, 3.6 and 3.9 are impossible
   without one.
7. How is reviewer capacity to grow? It is the binding constraint on the
   only labour-based moat.
8. Is a COTREX partnership to be pursued? HERMES-SOURCED: it is the
   highest-value trail and closure source and is blocked on written
   permission. A written agreement that others lack would be an advantage of
   a different kind; whether CPW would grant one, or grant it exclusively, is
   UNKNOWN.

## Unknowns

- Any competitor's roadmap, cost structure or legal posture. All
  disincentives above are reasoning, not evidence.
- Whether users value claim-level evidence enough to switch products
  (HERMES-SOURCED as the top unknown).
- The real cost per reviewed claim and per re-review. The M4 cycle gives a
  first data point but it is not recorded as a rate.
- Whether prose sources may be archived for history, as opposed to hashed.
