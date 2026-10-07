# First-party data flywheel options

Status: design options for the owner, written 2026-10-07. Not a decision, not
a specification and not a roadmap change. Nothing is implemented.

Labels: **HERMES-SOURCED** means the claim comes from a Hermes report the
coordinator has not re-checked. **INFERENCE** is this document's reasoning.
**UNKNOWN** means evidence is missing.

## Summary for the owner

1. **The product has no first-party data today and no way to receive any.**
   There is no backend, account system or analytics; saved state stays in
   browser local storage (`docs/architecture/system-overview.md`). Any
   flywheel starts from zero.
2. **One rule holds every option together: an observation can never set or
   relax a permission status. It may flag that a restriction might exist.**
   The M4 specification already reserves this: a community signal "can never
   establish legal access, ownership, permission, closure status or camping
   legality. No field in the schema lets it" (section 4, rule 3), and
   `community_report` is not a verification method (`data-contract.md` 5.4).
3. **Three options, from a link to a platform.**

   | Option | What users can do | Needs beyond the static site | Changes governance? |
   |---|---|---|---|
   | 1. Report a stale source | Tell Ohvernight a source or claim looks wrong | Nothing, or a role mailbox | No |
   | 2. Moderated structured observations | Submit a dated, enumerated observation about an existing feature; published after human review by pull request | A small submission endpoint and a private queue | No |
   | 3. Live observation platform | Accounts, reputation, photos, near-real-time publication, saved-trip sync, trip outcomes | Backend, database, auth, storage, moderation tooling, policies | Yes: content would publish without per-item owner approval |

4. **Only Option 1 fits the repository as it is run today.** It improves the
   authoritative data (faster re-review) rather than adding a second kind of
   data, and it carries almost no trust risk.
5. **The fast-decaying observation kinds (campsite occupancy, today's road
   or trail condition) cannot work under Options 1 or 2**, because
   publication by reviewed pull request takes days. They need Option 3 or
   should be declined.
6. HERMES-SOURCED: the source watchlist recommends deferring first-party
   observations "until the product has explicit consent, licensing, privacy,
   provenance, moderation, takedown, and 'observation is not permission'
   controls" (`future-sources/source-watchlist-m5-m8.md`, recommendation).
   The synthesis scores the idea Tier 2 (63) with trust risk 4 of 5.

## 1. What "improves with use" can mean here

| Signal | Who benefits | Fastest useful age | Risk if mishandled |
|---|---|---|---|
| Stale-source report | Reviewers: which claim to re-read first | Days | Low |
| User correction (wrong name, wrong place, wrong grouping) | Data quality | Weeks | Low to medium |
| Posted-sign report ("sign says no overnight parking") | Reviewers and, labelled, other users | Days to weeks | Medium: false restriction reports |
| Road-condition observation | Other users | Hours to days | High: read as passable |
| Trail-condition observation | Other users | Hours to days | High: read as safe or snow-free |
| Water-condition observation (ramp closed, low water) | Other users | Days | High: read as boating allowed |
| Campsite occupancy | Other users | Hours | High: read as available; concentrates use |
| Saved trips | The user; later, monitoring | — | Privacy |
| Destinations actually visited, outcomes | Review priority; warning calibration | Months, in aggregate | Privacy; "people went, so it is allowed" |

HERMES-SOURCED: the failure-mode research lists what a tool must never claim,
including that a gate is passable because it is unlocked or closed "because a
community report says so", that a dispersed site will be available on arrival,
and that a road is passable for a given vehicle
(`hermes/q3-trip-failure-modes.md`). Every observation kind above touches one
of those.

INFERENCE: the flywheel with the best ratio of value to risk is not "users
tell each other about conditions". It is "users tell reviewers where the
authoritative data is wrong or old, and reviewers fix the authoritative
data". The first is a community product competing with far larger ones. The
second makes the existing asset better and needs almost nothing built.

## 2. Keeping observation and authoritative fact apart

### 2.1 Data model

The existing model has four evidence classes; only "official recreation
information" can state that something is allowed, restricted or prohibited
(M4 spec section 4). Section 9.6 reserves the shape of a community record:
a separate registry, "with no verification method and no ability to set a
claim". The sketch below extends that reserved shape to first-party
observations. It is a sketch for discussion, not a contract proposal.

Separate file, separate layer kind, separate source type:
`v2/regions/<id>/observations.json`, declared in the manifest as a new
registry whose source `type` is `community` (the type exists today) and whose
`scope` statement says what observations do not establish.

```json
{"schema_version": 1,
 "observations": [
  {"id": "obs-2027-000123",
   "feature_id": "nhd-…",
   "kind": "posted_sign",
   "value": "sign_states_restriction",
   "subject": "overnight_parking",
   "observed_on": "2027-06-14",
   "received_at": "2027-06-15T02:10:00Z",
   "expires_after_hours": 720,
   "corroboration": {"independent_reports": 2, "window_hours": 168},
   "photo": {"held": true, "published": false},
   "reporter": {"class": "pseudonymous"},
   "moderation": {"state": "published", "moderated_at": "2027-06-16T15:00:00Z"},
   "review_ref": "issue-412",
   "superseded_by": null}]}
```

| Field | Rule |
|---|---|
| `feature_id` | Must resolve to an existing display feature in the region. Observations cannot create places. HERMES-SOURCED: "do not accept new campsite pins" (`idea-fairy-report.md`, Tier 2 item 5) |
| `kind` | Closed set: `stale_source`, `correction`, `posted_sign`, `road_condition`, `trail_condition`, `water_condition`, `site_occupancy` |
| `value` | Closed set per kind. No free text is ever published; free text goes to the moderator only |
| `observed_on` | Date the person saw it. Distinct from `received_at`. Day precision by default |
| `expires_after_hours` | Per-kind product policy held in data, like `max_age_hours`. After expiry the browser does not show the observation |
| `corroboration` | A count of independent reports in a window. A count, not a confidence |
| `reporter.class` | `anonymous` or `pseudonymous`. No name, handle, contact detail or device identifier is published, consistent with the rule against raw personal contact details in published data (`AGENTS.md`) |
| `superseded_by` | Reference to the reviewed claim that resolved it, when a reviewer has read an agency source |

Forbidden in an observation record, enforced by the validator in the manner
of R75 (which rejects activity or access properties on water features):

- any of `status`, `camping_permission`, `access_status`, `access`,
  `claims`, `allowed`, `restricted`, `prohibited`, `supported`;
- `verification_method`, `last_confirmed_at`, `last_verified`, `basis`;
- any key that is the name of a `fact_coverage` dimension.

Two further structural rules:

1. **No code path reads observations when computing a claim's displayed
   status, a trip evaluation, a filter or an M8 result group.** A test loads
   a region with and without its observations file and asserts those outputs
   are byte-identical.
2. **`fact_coverage` is unaffected.** A region does not move from `none` to
   `reviewed_partial` because observations exist.

### 2.2 The asymmetry

| An observation that suggests… | May it be shown? | What it triggers |
|---|---|---|
| A restriction might exist (posted sign, locked gate, closure notice) | Yes, labelled, near the top of the feature detail | A review-queue item. The claim changes only when a reviewer reads an agency or operator source |
| A condition is poor (washout, snow, ramp unusable) | Yes, labelled, dated | Nothing automatic |
| A condition is favourable (road dry, gate open, sites free) | Only where no reviewed restriction or closure applies to that feature, and never beside a permission line | Nothing |
| Something is allowed, or "we camped here without trouble" | Never. There is no value for it in the closed sets | — |

Where a reviewed restriction or prohibition exists, favourable observations
for that feature are suppressed entirely (agency-source override). An
observation that contradicts a reviewed `allowed` claim does not change the
claim's displayed status; it is shown beneath as a report and opens a review
item marked urgent.

### 2.3 Exact display rules

1. Observations appear only in their own section of the feature detail,
   under a fixed heading that is not WW8 "Agency or operator statement". A
   candidate, for owner approval: `Visitor reports. Not agency statements.`
2. The section never uses the words Allowed, Restricted, Prohibited,
   Reviewed, or any of the forbidden trust words. "Reviewed" (WW11) stays
   reserved for claims.
3. Every line carries the observed date and, where relevant, the count:
   `Posted sign reported: no overnight parking. Seen 2027-06-14. 2 reports.
   Ohvernight has not reviewed an agency source for this.`
4. Observations never change map styling, a feature's colour, a label, a
   list badge, a filter result or an ordering.
5. Observations use a visual treatment that is distinct from claims and is
   not green or red.
6. An expired observation is not shown. A count of hidden older reports may
   be shown without their content.
7. The section ends with a fixed line stating that reports are not
   permission and may be wrong or out of date.
8. With no observations, the section is absent. Absence of reports is not
   worded as "no problems reported".
9. A restriction-suggesting report is shown even when a reviewed claim says
   allowed, with the claim unchanged and the conflict stated.

## 3. Trust and moderation mechanisms

| Mechanism | Design | Limit |
|---|---|---|
| Dated observations with decay | Per-kind expiry in data; browser computes age, as for claims. Illustrative starting values (INFERENCE, not evidence-based): occupancy 12 h, road or trail condition 7 d, water condition 14 d, posted sign 30 d | Half-lives are UNKNOWN; Hermes lists "useful report half-life" as something to validate |
| Corroboration counts | Independent means different reporters and different days or sessions. Shown as a count, never as a score | Cheap to fake without accounts |
| Reporter reputation | Internal only. Earned when a report is later borne out by a reviewed agency source; lost on withdrawn reports. Never displayed as a badge next to a report | Needs accounts (Option 3). A visible reputation would lend authority the report must not have |
| Photo evidence | Required for `posted_sign`. Location and device metadata stripped before any storage beyond moderation. Photos are not published by default | Photos of people, plates and private property; storage and takedown duties |
| Agency-source override | A reviewed claim always wins on status; favourable reports are suppressed under a restriction; `superseded_by` closes a report once a reviewer has read the source | Depends on reviewer capacity |
| Moderation before publication | Options 1 and 2: nothing a user submits is published without a person approving it | Latency; reviewer time |
| Abuse and poisoning resistance | Closed value sets; existing features only; rate limits per reporter and per area; no publication of a single uncorroborated restriction report without a photo; expiry | See below |
| Privacy of location histories | Saved trips and visited places stay on the device by default. Nothing about a person's trips is published. Aggregates, if ever collected, are coarse, thresholded and used for review priority only | A trip history is sensitive: it says when someone is away from home and where they sleep |

**Poisoning cases to design against (INFERENCE).**

| Attack | Why someone would | Control |
|---|---|---|
| False "posted: no camping" reports | To keep a favourite place quiet; a neighbour deterring visitors | Photo required; corroboration; expiry; shown as unreviewed; reviewer resolves against the agency source |
| False favourable reports | To make a place look usable | Cannot relax anything; suppressed under restrictions; expire |
| Mass submissions | Vandalism | Rate limits; moderation; closed sets mean nothing offensive can be published |
| Targeting a person or property | Harassment | No free text published; photos unpublished; existing public features only |
| Revealing sensitive sites | Carelessness | No new pins; HERMES-SOURCED: discovery can "expose fragile sites" |

One residual risk is not controllable by design: the asymmetry that makes the
system safe (restriction-suggesting reports are shown, permission-suggesting
ones are not) also makes false restriction reports the cheapest attack. The
controls reduce it; they do not remove it.

**Popularity.** Visit counts and occupancy must not become a ranking input.
HERMES-SOURCED: crowd avoidance was rejected partly because a crowd ranking
"could redirect users to fragile or poorly understood locations".

**Contribution terms.** Every option that stores a submission needs the
contributor's agreement to a licence for it, a privacy statement and a
takedown path. None exists today.

## 4. Three options

### Option 1 — "Report a stale source" (minimal, no accounts)

**What it is.** Beside every source link and review date, a link that opens
a pre-filled report naming the feature ID, the claim, the source URL and the
displayed review date. Two delivery choices, both static:

- a pre-filled issue link to the public repository (the reporter needs a
  GitHub account; the report is public);
- a pre-filled `mailto:` to a role address (no account; private; the address
  is published).

Nothing a reporter writes is ever published by the site. The report enters
the same human review queue the source monitor would use
(`docs/research/engineering/source-monitoring-architecture.md`). The only
effect on the product is that a reviewer re-reads a source sooner and, if
warranted, changes a claim through the normal pull request with the owner's
approval.

It may be paired with purely local features that share nothing: saved trips
and a "visited" mark in local storage, exportable by the user.

**Requires beyond a static site.** Nothing for the issue link. A role
mailbox for the mail link. Reviewer time.

**What improves with use.** Review priority. Reports become, over time, a
record of which sources go stale fastest.

**Failure modes.** Few reports, because there are few users (contribution
density is UNKNOWN, HERMES-SOURCED). Public issues may contain personal or
location detail a reporter did not intend to publish. Reports of "the app is
wrong, I camped there fine" must not be actioned as evidence. An unanswered
report queue signals neglect.

### Option 2 — Moderated structured observations, published by pull request

**What it is.** A short form on the feature detail: pick a kind, pick a
value from a closed list, give the date seen, optionally attach a photo. No
account. Submissions go to a private queue. A moderator approves or
rejects; approved observations are added to `observations.json` in a pull
request that goes through CI and the owner's approval like any data change,
and are displayed under the rules of section 2.3.

**Requires beyond a static site.** One small submission endpoint (a
serverless function or a third-party form service) with spam protection; a
private store for the queue and any photos; a privacy statement and
contribution terms; a moderation routine. The published site stays static.

**Which kinds fit.** Only slow-decaying ones: `stale_source`, `correction`,
`posted_sign`, and seasonal-scale conditions ("road gated for winter",
"bridge out"). Daily conditions and occupancy do not survive a
days-long review cycle and should be excluded from this option rather than
shown late.

**What improves with use.** As Option 1, plus a visible, dated layer of
restriction-suggesting reports ahead of formal review.

**Failure modes.** Moderator time becomes the bottleneck and published
reports lag. Without accounts, corroboration is weak and one person can file
several reports. A third-party form service holds user submissions under its
own terms. An approved observation that later proves false has been
published under the project's name. Users may read the reports section as
complete ("nothing reported, so it is fine") despite rule 8.

### Option 3 — Live observation platform

**What it is.** Accounts or pseudonymous keys; observations published
within minutes subject to automated checks, with moderation after the fact;
internal reputation; photos; corroboration across reporters; saved trips
synchronised across devices; optional "how did it go" outcome reports after a
trip date; aggregate signals feeding review priority.

**Requires beyond a static site.** A backend with a database,
authentication, object storage, rate limiting, moderation tooling, abuse
reporting, data export and deletion, terms, a privacy policy, a takedown
process and someone on call for it. The browser would fetch observations
from a live service, a new kind of request for the application; the browser
test harness blocks non-local requests today.

**Governance consequence.** Observation content would reach users without
the owner approving each item. That is outside the current rule that
publication happens by reviewed merge (`AGENTS.md`; ADR-002) and would need
an explicit owner decision that the rule covers authoritative data and code,
not user observations. The separation in section 2 is what would make such a
decision defensible.

**What improves with use.** Everything in the table of section 1, including
the fast-decaying kinds and outcome history. HERMES-SOURCED: outcome history
is "potentially strong but long-term" and its collection is unvalidated.

**Failure modes.** All of the above at higher speed: a false report is live
before anyone sees it. Low density makes the layer look empty or stale, which
is the complaint users already make about crowdsourced products
(HERMES-SOURCED, `hermes/p2-customer-pain-and-workflows.md`, theme 4).
Location histories become a breach target. Occupancy reports steer people to
the same places. Operating cost and attention move from data review to
community management. The product starts to resemble the incumbents it is
weakest against (see `moat-analysis.md`, section 3.5).

### Comparison

| | Option 1 | Option 2 | Option 3 |
|---|---|---|---|
| Static site preserved | Yes | Yes for readers | No |
| Accounts | None | None | Yes |
| Publishes user content | Never | After human approval, by pull request | Yes, live |
| Observation kinds supported | Stale source, correction (as review input) | Slow-decaying kinds | All |
| Owner approval per published item | n/a | Yes | No |
| Privacy exposure | Minimal | Submissions and photos in a private queue | Accounts, trips, locations |
| Running cost (INFERENCE) | Reviewer time | Reviewer time plus a small service | Sustained engineering and moderation |
| Trust risk | Low | Medium | High |

## 5. Owner decisions this raises

1. Does Ohvernight want to hold first-party observations at all, or remain
   an authoritative-source product? (HERMES-SOURCED as owner question 6.)
2. Is a backend ever acceptable, and for what?
3. May user-submitted content be published without per-item owner approval?
4. For Option 1: public issue link, private mail link, or both?
5. Is a visible "visitor reports" section acceptable in the feature detail,
   and what is its exact heading and closing line? These are trust-bearing
   strings.
6. May a restriction-suggesting report be shown before a reviewer has read
   an agency source, given that false restriction reports are the cheapest
   attack?
7. Are campsite occupancy and same-day conditions in scope ever, given the
   rejection of crowd-based features?
8. Are favourable condition reports shown at all, or only cautionary ones?
9. Photos: required, optional or refused? Published or moderator-only?
10. What licence do contributors grant, and is the observation set open
    data?
11. Are visit and outcome data ever collected, even in aggregate?
12. Should an expired restriction-suggesting report stay in the review queue
    until a person resolves it, even though it is no longer displayed?

## Unknowns

- Whether anyone would contribute; contribution density and moderation cost
  are unmeasured.
- Real decay times for each observation kind.
- Whether users understand the separation of report from agency statement.
  HERMES-SOURCED: comprehension of evidence states is the first thing to
  test.
- Legal duties attached to holding user submissions, photos and location
  data. Not researched in any report in the repository.
