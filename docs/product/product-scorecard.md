# Product scorecard and milestone product review

Status: review practice, recorded 2026-10-08. It applies from M5 onward, and
to the close of M4 for the baseline run. It adds a product question to
milestone review; it removes no engineering gate.

## Two questions at every milestone

**Engineering:** what trustworthy capability did we add?

**Product:** what new thing can a user successfully accomplish?

A milestone that can answer only the first has improved the foundation and
not yet the product. That is sometimes the right milestone to build. It must
be said plainly when it is.

## Scorecard

Lightweight on purpose. Each line is recorded with its previous value.

| Measure | Source |
|---|---|
| Time to a viable trip | Canonical scenario |
| External apps and sites required | Canonical scenario |
| Manual transfers between apps | Canonical scenario |
| Planning steps required | Canonical scenario |
| Mobile interaction burden | Canonical scenario, run on a phone |
| Unresolved critical unknowns | Canonical scenario |
| Unsupported proximity assumptions avoided | Canonical scenario and review of the interface: places where the product declined to imply a link |
| Linked trip components established | Data: relationships that are source-backed or reviewed, by kind (see [adventure-model.md](../architecture/adventure-model.md)) |
| Evidence coverage | Data: for the features a trip would use, which restriction categories are checked, by category. Never a single score. |
| Activities with actionable restriction evidence | Data: activities for which at least one reviewed allowed, restricted or prohibited record exists in the scenario area |
| Candidate trips with a viable overnight option | From M8; before then, the scenario result |
| Candidate trips with a backup option | From M8; before then, the scenario result |
| Stale evidence warnings | Data: reviews past policy among the facts a trip would rely on |

Feature count, layer count and bytes shipped remain engineering and data
measures. They are not product success and are not reported as such.

No scorecard line may be improved by weakening a trust rule. A lower count of
unknowns reached by not showing them is a failure of the review.

## Milestone product review

At the end of every milestone, report:

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
How the
[canonical Douglas dirt-bike scenario](acceptance-scenario-douglas-dirt-bike.md)
performs now against the previous milestone, measure by measure.

The review is written by the coordinator, from a scenario run by a person. An
automated check passing is not a scenario result.
