DRAFT - UNREVIEWED

# Source-monitoring architecture

Status: a future design for the owner to consider, written 2026-10-07. Not a
decision, not a specification and not a roadmap change. Nothing is
implemented and no source was contacted in writing this.

Labels: **HERMES-SOURCED** means the claim comes from a Hermes report the
coordinator has not re-checked. **INFERENCE** is this document's reasoning.
**UNKNOWN** means evidence is missing.

## Summary for the owner

1. **Today a source can change or disappear without anyone being told.** No
   refresh is scheduled; both workflows that contact sources are manual
   (`docs/architecture/system-overview.md`; `.github/workflows/`). Register
   item N1 records that for three layers "a failed refresh is invisible"
   (`v2/pipeline/docs/data-contract.md`).
2. **The proposal is a monitor that only ever opens issues.** Scheduled
   GitHub Actions run read-only checks and file findings in a human review
   queue. The monitor never changes a claim, a date, a manifest or any
   published file, and never opens a pull request that does.
3. **The cheapest useful check needs no network at all:** compute, from the
   committed claim registries, which reviews fall due soon and open an issue
   for each. Start there.
4. **Minimal version:** review-due issues, plus a weekly schema fingerprint
   and feature count for each ArcGIS source, plus a sentence check on each
   claim's source page. INFERENCE: on the order of fifty polite requests a
   week at current scale.
5. **A quiet monitor proves nothing.** "A fetch is not a confirmation"
   (`docs/product/trust-principles.md` section 4). A passing check advances
   nothing and must never be displayed or described as the source being
   current.
6. **The real cost is triage time, not compute.**

## 1. What exists already

| Piece | Where | Relevance |
|---|---|---|
| Transport records with `status`, `last_checked_at`, `last_retrieved_at`, `count`; rule R32 compares `count` with the layer | `data-contract.md` 5.3, 5.7 | The stored count is a ready baseline for count checks |
| A page-hash change monitor for the Pitkin County fire page that deliberately infers no stage | `v2/pipeline/scripts/06_fetch_fire_stage_monitor.py` | The pattern to generalise: "Page hash is not a restriction stage" |
| `html_change_monitor` as an approved verification method | `data-contract.md` 5.4 | The vocabulary exists |
| Claim objects with `last_checked_at`, `last_confirmed_at`, `max_age_hours`; freshness computed, never stored | `data-contract.md` 5.4; M4 spec 9.3 | Review-due dates are computable offline |
| An ArcGIS client with an identifying User-Agent, bounded retries and backoff | `v2/pipeline/scripts/lib/arcgis_client.py` | Politeness conventions to reuse |
| `sources.yaml` records "Metadata checked on 2026-09-24" and a wildlife service disabled after a 404 | `v2/pipeline/config/sources.yaml` | A source has already vanished once, found by hand |
| Hermes's role includes source, API, licensing and freshness monitoring, as inputs only | ADR-004 | Who investigates a finding |
| Query patterns that worked: `?f=pjson`, ArcGIS Online item `licenseInfo` and `accessInformation`, Socrata catalogue licence fields | `docs/research/hermes/playbook.md` section 4 | The exact requests a monitor would make |

Two observations from the research record that a monitor would have caught
or would settle. `sources.yaml` points roads at the USFS service
`EDW_MVUM_02`, while Hermes read `EDW_MVUM_01` and found a guessed
`EDW_Road_MVUM_01` returned 404 (HERMES-SOURCED,
`future-sources/source-watchlist-m5-m8.md`, unknowns). Which is current is
UNKNOWN here; it was not checked. And several agency URLs retrieved for the
failure-mode research returned 404 (HERMES-SOURCED,
`hermes/q3-trip-failure-modes.md`, unknowns). Agency URLs move.

## 2. The five questions

| Question | Check | Signal |
|---|---|---|
| Did a government service's schema change? | Schema fingerprint | Field added, removed, retyped; coded-value domain changed; layer renumbered or renamed |
| Did an operator page disappear? | Endpoint check | 404 or 410; redirect to a different path; a 200 whose content is a generic landing page |
| Is evidence stale? | Review-due computation (offline) | `last_confirmed_at + max_age_hours` is within N days or past |
| Did a feature count change dramatically? | Count check | Count for the region's extent differs from the transport record beyond a threshold; counts by code shift |
| Did a source change its licensing terms? | Terms check | Change in `licenseInfo`, `accessInformation`, `copyrightText`, catalogue licence fields, or the text of a terms page |

## 3. Components

### 3.1 Source inventory

The monitor reads what the repository already declares; it keeps no separate
list that can drift:

- every `sources.<id>.source_urls` entry in each `region.json`;
- every endpoint in `v2/pipeline/config/sources.yaml`;
- every `source_url` in a claim: the rules registry and, after M4-C,
  `water-recreation.json`;
- a small hand-kept list of terms pages per publisher, which is new.

Each entry gets a monitoring policy: which checks apply, how often, and
whether automated access is allowed at all. A source whose terms prohibit
automated collection is listed as `manual_only` and is never fetched.
HERMES-SOURCED: CAIC's terms prohibit robots and data mining, and COTREX's
prohibit crawling and non-interface access (`source-watchlist-m5-m8.md`).

### 3.2 Scheduled endpoint checks

One conditional GET per endpoint. Record status, final URL after redirects,
content type and length. Three results: reachable, unreachable, moved. A
soft-404 heuristic (the final URL differs from the requested path, or the
page no longer contains the feature's name) is reported as "possibly moved",
not asserted.

### 3.3 Schema fingerprints

For each ArcGIS layer in use, fetch `<layer>?f=pjson` and build a canonical
document: layer ID and name, geometry type, and for each field its name, type
and, where present, the coded-value domain as sorted code and label pairs.
Hash it. Store the canonical document, not only the hash, so that a change
produces a readable difference. Only the fields the pipeline actually reads
(for water: `ftype`, `fcode`, `permanent_identifier`, `gnis_id` and the rest
listed under "M4-A water source fields" in the contract) raise an alert at
schema level; changes elsewhere are logged as cosmetic.

A fingerprint cannot see a change of meaning under an unchanged name. The
playbook's lesson applies: "Schema research needs a count, not only a
dictionary". Hence 3.4.

### 3.4 Count checks

Per layer and region: a count-only query for the region's extent, compared
with the transport record's `count`; and one grouped statistics query on the
classification field the pipeline depends on. Thresholds are per layer and
held in configuration; a change above the threshold opens an issue with both
numbers. A frozen source (NHD has been unmaintained since October 2023, M4
spec section 18) should produce no change, so any change there is notable.

Counts must be read with the same filter the pipeline uses. A count
difference caused by a different query is a false alarm built into the
design.

### 3.5 Claim-page checks: page hash versus extracted sentence

A claim rests on a sentence. Hermes dossiers already record "page URL, exact
sentences relied on, date read" (M4 spec 9.5). Two ways to watch the page:

| Method | Detects | Misses | Noise |
|---|---|---|---|
| Whole-page hash | Any byte change | Nothing, in principle | Very high: timestamps, session tokens, banners, CMS rebuilds |
| Main-content hash (navigation, scripts and footers stripped; whitespace normalised) | Any change to the body text | Changes outside the extracted block | Medium |
| Extracted-sentence check: is the normalised sentence relied on still present? | The supporting sentence was removed or reworded | A new sentence that changes the meaning while the old one remains | Low |

INFERENCE: use the sentence check as the alarm and the main-content hash as
context, and report three states:

1. Sentence present, content unchanged: nothing to do.
2. Sentence present, content changed: low-priority issue for ordinary claims;
   normal priority when the claim is `restricted` or `prohibited`, or when the
   page is a closure or fire page, because an added paragraph can matter more
   than the old sentence.
3. Sentence absent, or page unreachable: issue for review; restriction-
   affecting if any claim citing the page is `restricted` or `prohibited`.

Keyword spotting ("closed", "Stage 2") is not proposed. The existing fire
monitor exists precisely to avoid "inventing a current fire stage from
page-wide keywords".

Where the anchor sentence is stored is an owner question. The M4 claim
`summary` is deliberately "written by the reviewer, not copied text", and
operator pages carry no reuse licence
(`docs/research/m4-water/licensing-and-terms.md`). An alternative that
stores no page text: keep a hash of the normalised sentence, hash every
sentence of the fetched page, and test membership. It is more brittle to
punctuation changes.

None of these states touches the claim. State 1 does not advance
`last_confirmed_at` and should not advance `last_checked_at` in committed
data either, since that would be an automated change to a claim record.

### 3.6 Freshness alerts tied to each claim's maximum age

Runs entirely offline against committed files. For every claim and rule
record, compute the due date from `last_confirmed_at` and `max_age_hours`.
Open an issue a configurable number of days before it falls due and escalate
its label when it passes. Restrictions and prohibitions get the longer lead
time: they stay in force when overdue and are shown as "Review overdue", so
an overdue restriction is a visible defect in the product, whereas an overdue
`allowed` claim quietly degrades to "Not established".

This must be an issue, never a failing check. The contract is explicit that
validation is time-independent and "data getting older must never fail CI"
(`data-contract.md` 5.4, rule 10).

### 3.7 Change classification

The monitor proposes a class; a person confirms it. Classification is a
triage hint, never an action.

| Class | Meaning | Default priority | Example |
|---|---|---|---|
| Cosmetic | No field the pipeline reads and no sentence a claim relies on changed | Log only; weekly digest | Page banner; an unused field added |
| Availability | Endpoint unreachable or moved | After N consecutive failures | The wildlife service 404 |
| Schema | A field, type, domain or layer the pipeline reads changed | Normal; blocks the next refresh of that source | Domain code relabelled |
| Semantic | Counts or content changed while the schema did not | Normal | Count by `ftype` shifts; body text changed around an intact sentence |
| Restriction-affecting | Any change on a page or source cited by a `restricted` or `prohibited` claim, a rule record, or a closure or fire source | High; never auto-closed | Supporting sentence gone from a Denver Water page |
| Licensing | Any change to terms, licence or attribution fields | High; always to the owner | `licenseInfo` edited |

Escalation rule: when unsure, classify upward. Anything touching a source
behind a restriction is restriction-affecting until a person downgrades it.

### 3.8 Human review queue

GitHub issues in the repository. One open issue per source and condition,
keyed so that repeated runs update the same issue rather than opening
duplicates. Labels carry class and state. Each issue states what was
checked, what was expected, what was found, the difference, the claims and
layers that depend on the source, and the fixed line "This is a retrieval
result. It is not a review and confirms nothing."

Who acts: the coordinator triages; Hermes may be asked for a dossier with the
exact sentence and date read (ADR-004); any change to data is a normal pull
request reviewed by the coordinator and approved by the owner. The playbook's
escalation list applies: a finding that implies a new positive claim, a
licence interpretation with material uncertainty, or a wording change goes to
the owner.

The monitor may comment "recovered" on an availability issue. It never
closes a restriction-affecting or licensing issue.

### 3.9 Where it runs

Scheduled GitHub Actions opening issues is the natural fit: the repository
already uses Actions, there is no server, and issues are where review
happens.

Constraints from the repository's rules:

- **It is not part of ordinary review.** `AGENTS.md` says live refresh
  commands "contact external sources" and are not to be run "as part of
  ordinary code review". The monitor is a separate workflow on `schedule`
  and `workflow_dispatch` only. It never runs on `pull_request`, is not a
  required check and cannot block a merge. CI stays offline.
- **Nothing merges without the owner.** The workflow gets `issues: write`
  and `contents: read`. It has no permission to push, commit or open pull
  requests. It does not run the pipeline's refresh scripts and produces no
  publishable data artifact.
- **Secrets.** The minimal version needs none. Checking RIDB would need
  `RIDB_API_KEY` as an Actions secret, as today.
- **State.** Fingerprints and hashes must persist between runs without a
  commit to `main`. Options: reviewed baselines committed to the repository
  by pull request (auditable, slow to update); state carried in the tracking
  issue body or a workflow artifact or cache (no commit, less durable); or a
  dedicated non-published branch written by the workflow (durable, but an
  automated push, which the owner would have to authorise explicitly).

INFERENCE, to be confirmed before relying on it: GitHub may disable scheduled
workflows in a repository with no recent activity, and hosted-runner address
ranges are widely shared. The first makes a heartbeat necessary (3.10); the
second makes blocking likely (section 7).

### 3.10 Heartbeat

A monitor that has stopped looks identical to a monitor that has found
nothing. Each run updates one pinned status issue with the run time, the
number of sources checked, skipped and failed. A source that could not be
checked is reported as not checked, not as unchanged. HERMES-SOURCED: "Silence
can be interpreted as 'nothing changed'"; alerts "should never promise
complete detection" (`idea-fairy-report.md`, Tier 1 item 5).

## 4. Request budgets and politeness

| Rule | Detail |
|---|---|
| Identify | The pipeline's existing User-Agent, with a link to the repository. HERMES-SOURCED: the NWS API requires an identifying User-Agent |
| Respect terms | `manual_only` sources are never fetched. Honour `robots.txt`. Only documented endpoints; HERMES-SOURCED: avoid "endpoints discovered through browser inspection" |
| Be small | Metadata and count-only queries; `returnGeometry=false`; never a bulk download from the monitor |
| Be conditional | Send `If-None-Match` or `If-Modified-Since` where the server supports them |
| Be slow | One request at a time per host; a pause between requests; jitter on the schedule so runs do not land on the hour |
| Fail quietly | At most two retries with backoff, as the client does today; then record "not checked" and stop for that host until the next run |
| Budget per source | A fixed ceiling per run and per week in configuration; the run aborts for a host that exceeds it |

Illustrative cadence (INFERENCE; not measured):

| Check | Cadence | Requests at current scale |
|---|---|---|
| Review-due computation | Daily | 0 |
| ArcGIS schema fingerprint | Weekly | About one per layer in use; on the order of 10 to 15 |
| Count and grouped statistics | Weekly | About two per layer and region |
| Claim-page sentence check | Weekly; more often for closure and fire pages in season | One per distinct page; about 10 after M4-C |
| Terms and licence fields | Monthly | One per publisher |

Access-agreement limits apply regardless: RIDB access is revocable and may be
rate-limited; Colorado DWR has a daily anonymous call limit
(`m4-water/licensing-and-terms.md`).

## 5. What must never be automated

1. Changing a claim's `status`, `summary`, `source_url`, `effective_from` or
   `effective_to`.
2. Advancing `last_confirmed_at`. Only a person's review does that, for that
   one fact (`trust-principles.md` section 4).
3. Relaxing or removing a restriction, exclusion, limit or caution for any
   reason, including the source page disappearing. A missing page does not
   mean the restriction ended.
4. Creating a claim, including a restriction, from detected text. A detected
   closure notice becomes an issue, then a reviewed claim.
5. Replacing a `source_url` with the redirect target.
6. Accepting a new schema or code mapping, or updating a baseline fingerprint
   without review.
7. Deciding what a licence change permits.
8. Closing a restriction-affecting or licensing issue.
9. Editing trust wording, manifests, `fact_coverage` or limitations.
10. Committing, opening a data pull request, merging or deploying.
11. Showing monitor results to users as currency. Any user-facing use of
    monitor output would be a new trust-bearing statement needing its own
    specification.
12. Letting a language model's reading of a page stand in for review. A
    Hermes retrieval is not a review (ADR-004, ADR-005).

## 6. Minimal and fuller versions

### Minimal

- Offline review-due issues for every claim and rule record.
- Weekly schema fingerprint and count for each ArcGIS layer the manifests
  declare.
- Weekly endpoint and sentence check for each claim page.
- Issues with the six class labels, de-duplicated; one heartbeat issue.
- Baselines committed by reviewed pull request.

What it answers: schema change (yes); page disappeared (yes); evidence stale
(yes); count changed (yes); licensing changed (no, still manual).

### Fuller

Adds, in rough order of value (INFERENCE):

1. Terms and licence monitoring for every publisher, including ArcGIS Online
   item fields and catalogue licence fields.
2. A dated change history per source, kept somewhere durable. This is the
   record that cannot be backfilled (see `product-opportunities/
   moat-analysis.md`, section 3.2) and it lets `max_age_hours` be set from
   observed cadence.
3. Per-source cadence that tightens in season for fire and closure pages.
4. Grouped statistics on every classification field, with drift thresholds.
5. Redirect and soft-404 tracking with a proposed new URL in the issue.
6. A generated source-health page for maintainers.
7. A standard Hermes follow-up brief generated from the issue: exact URL,
   the sentence previously relied on, what to quote back.
8. A second vantage point for sources that block hosted runners.
9. Dependency listing in each issue: which claims, layers, regions and,
   later, M8 pairs rest on the source.

### Cost

| Item | Minimal | Fuller |
|---|---|---|
| Build (INFERENCE) | Small: a few scripts reusing the existing client and registries, one workflow, tests against recorded fixtures | Medium: state store, history, per-source policy, reporting |
| Compute | Minutes per week | Still small |
| External services | None | Possibly one, if a second vantage point is used |
| Human triage | The real cost. Volume is UNKNOWN until it has run for a season | Grows with sources; HERMES-SOURCED: "source-monitoring feasibility is unknown at scale" |
| Testing | Offline, against saved `pjson` and page fixtures; the monitor's own tests must not contact sources, in keeping with CI | Same |

## 7. Failure modes

| Failure | Cause | Mitigation | Residual |
|---|---|---|---|
| False alarms | Page hashes change on every load; CMS rebuilds; a count read with a different filter | Sentence check as the alarm; main-content hashing; thresholds; cosmetic class goes to a digest | Alert fatigue if thresholds are wrong; a fatigued reviewer misses the real one |
| Silent page rewrite | A new paragraph changes the rule while the old sentence stays; rule moves to a PDF or a second page | State 2 raised at normal priority for restriction pages; periodic full human re-read driven by `max_age_hours` | The monitor does not replace scheduled review. It only brings some reviews forward |
| Meaning changes under a stable schema | A code is reused; a field is repurposed | Grouped counts | Small shifts pass unnoticed |
| Bot blocking | Agency firewalls challenge or block datacentre addresses; pages return "a short shell to a script" (playbook section 6) | Treat as not checked, never as "page gone"; require N consecutive failures; mark the source `manual_only` and schedule a human check | Some sources will only ever be checked by a person |
| Soft 404 | A removed page redirects to a home page with status 200 | Final-URL comparison; sentence check fails | Heuristic |
| Monitor silently stopped | Workflow disabled, token expired, script error swallowed | Heartbeat issue; a failed run opens its own issue | Someone must look at the heartbeat |
| "Green" read as confirmed | A clean run is mistaken for the claim being current | Fixed disclaimer line in every issue; no user-facing output; no date advanced | A habit risk among maintainers |
| Baseline drift | Baselines updated routinely without reading the difference | Baseline changes only by reviewed pull request showing the readable difference | Review quality |
| Over-collection | Storing page text or responses beyond what terms allow | Store fingerprints and hashes; keep sentences only if the owner decides so | Hash-only storage weakens history |
| Being a bad citizen | Too frequent, or fetching sources whose terms forbid it | Budgets, `manual_only`, honouring `robots.txt` | A terms change the monitor has not yet noticed |
| Queue neglect | Issues opened faster than they are triaged | Digest for cosmetic; hard cap on new issues per run, overflow summarised | An unattended queue is worse than none, because it looks like diligence |

## 8. Owner decisions this raises

1. Is a scheduled workflow that contacts external sources acceptable, given
   that all contact with sources is manual today?
2. May the workflow hold `issues: write`? May it ever write to a
   non-published state branch, or must all state be committed by reviewed
   pull request?
3. Which sources may be fetched automatically, and who reads the terms that
   decide it?
4. May the sentence a claim relies on be stored in the repository, or only
   its hash?
5. Should a clean check ever update `last_checked_at` on a claim? This
   document assumes not.
6. What lead time before a review falls due, and is it longer for
   restrictions?
7. Thresholds for count changes, per layer.
8. Who triages, and how much time per week is the owner willing to spend on
   the queue?
9. Should monitoring start before M5, to begin accumulating source history?
10. Is a public issue the right place for a licensing or restriction
    finding, or should some findings be private?
11. Is a second vantage point, or any paid service, acceptable for sources
    that block hosted runners?

## Unknowns

- Which sources block automated requests from hosted runners. Not tested.
- Whether the operator pages behind the M4-C claims are stable enough for a
  sentence check to be quiet.
- How often real changes occur; no history exists.
- Scheduled-workflow behaviour in an inactive repository, as noted in 3.9.
- Whether `EDW_MVUM_02` or `EDW_MVUM_01` is the current USFS service.
- Triage volume at M7 scale, when forest orders and county notices enter.
