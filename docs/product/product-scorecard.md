# Product scorecard and milestone product review

Status: review practice, recorded 2026-10-08. It applies from M5 onward, and
once after M4 closes for the baseline run; it is not a merge gate for M4. It
adds a product question to milestone review; it removes no engineering gate.

## Two questions at every milestone

**Engineering:** what trustworthy capability did we add?

**Product:** what new thing can a user successfully accomplish?

A milestone that can answer only the first has improved the foundation and
not yet the product. That is sometimes the right milestone to build. It must
be said plainly when it is.

## Scorecard

Lightweight on purpose. Each line is recorded with its previous value.
There are two canonical scenarios,
[Scenario A](acceptance-scenario-douglas-dirt-bike.md) (Douglas dirt-bike with
overnight planning) and
[Scenario B](acceptance-scenario-rampart-day-use.md) (Rampart dirt-bike with
family day use). "Canonical scenario" below means each of them, reported
separately.
Measures taken from the scenario use the scenario's names and its
[definitions](acceptance-scenario-douglas-dirt-bike.md#definitions) of viable
trip, critical question, within policy and planning step. "Viable" is never a
statement that anything is permitted.

| Measure | Source | Reported beside |
|---|---|---|
| Time to a viable trip | Canonical scenario | Step outcomes |
| Planning steps required | Canonical scenario | Step outcomes |
| External apps and sites required | Canonical scenario | Step outcomes |
| Manual transfers between apps | Canonical scenario | |
| Unresolved critical questions | Canonical scenario | |
| Unsupported assumptions | Canonical scenario | |
| Proximity assumptions made (lower is better) | Canonical scenario | |
| Evidence freshness and completeness | Canonical scenario | |
| Evidence coverage shown | Canonical scenario. By category, never a single score. | |
| Overnight backup available | Canonical scenario | |
| Explainability | Canonical scenario | |
| Phone burden | Canonical scenario, run on a phone | |
| Linked trip components established | Data: relationships that are source-backed or reviewed candidates, by kind (see [adventure-model.md](../architecture/adventure-model.md)) | The count of unknown links of the same kind |
| Activities with actionable restriction evidence | Data: reviewed allowed, restricted or prohibited records against the features of the trail system the scenario evaluated, as records per feature | The features of that system with no reviewed record |
| Candidate trips with a viable overnight option | From M8, as a share of candidates; before then, the scenario result | The unknowns each candidate lists |
| Candidate trips with a backup option | From M8, as a share of candidates; before then, the scenario result | The unknowns each candidate lists |
| Stale evidence warnings | Data: reviews past policy among the facts a trip would rely on | The count of reviewed facts, and any change to `max_age_hours` policy since the last review |

Feature count, layer count and bytes shipped remain engineering and data
measures. They are not product success and are not reported as such.

No scorecard line may be improved by weakening a trust rule. A lower count of
unknowns reached by not showing them is a failure of the review.

A product that answers "unknown" to everything scores well on the scenario's
step outcomes. Only the time, planning-step and external-apps measures offset
that, which is why they are reported beside the step outcomes.

## Milestone product review

At the end of every milestone from M5 onward, and once after M4 closes for the
baseline, report:

### SHIPPED
What engineering or data capability landed.

### USER CAN NOW
What concrete new task a user can complete.

### USER STILL CANNOT
What important trip-planning questions remain unresolved.

### OUTSIDE RESEARCH STILL REQUIRED
What still forces the user into other apps or sites, by name.

### TRUST / UNKNOWN STATE
What remains unknown and why.

### ACCEPTANCE SCENARIO RESULT
How each canonical scenario,
[Scenario A](acceptance-scenario-douglas-dirt-bike.md) and
[Scenario B](acceptance-scenario-rampart-day-use.md), performs now against the
previous milestone, measure by measure. Both are reported.

The review is written by the coordinator, from a scenario run by a dedicated
tester who did not implement the work. An automated check passing is not a
scenario result.
