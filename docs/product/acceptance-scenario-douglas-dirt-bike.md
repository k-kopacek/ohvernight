# Canonical acceptance scenario: Douglas County dirt-bike weekend

Status: recurring product acceptance scenario, recorded 2026-10-08. A
dedicated tester who did not implement the work runs it once after M4 closes,
for the baseline, and then at the close of every milestone from M5 onward. The
result is recorded in the product review (see
[product-scorecard.md](product-scorecard.md)). It is not an automated test, it
replaces no engineering gate, and it is not a merge gate for M4.

This is **Scenario A**. [Scenario B](acceptance-scenario-rampart-day-use.md),
the Rampart family day-use and dirt-bike outing, runs beside it and does not
replace it.

## Why this scenario

Douglas County and the nearby Front Range motorized trail systems exercise
every hard part of the product at once: an activity that is allowed on some
trails and prohibited on others, staging areas, forest roads with vehicle
limits, a mix of developed and dispersed camping, seasonal and fire
closures, and a county boundary that the terrain ignores.

## The task

> I have a dirt bike and a weekend. Using Ohvernight, plan a ride in or near
> Douglas County with somewhere to stay overnight.

Fixed for every run, so that results are comparable across milestones:

- **Vehicle profile:** a pickup towing a small trailer that carries the bike.
- **Season class:** a summer weekend inside the main riding season. The actual
  dates used are recorded with the result.
- **Tester familiarity:** the tester records how well they already know the
  area, because prior knowledge shortens the time and hides unknowns.

The trail is **not** fixed in advance: choosing it is part of the task. For
repeatability the tester records which trail system they ended up evaluating,
so a later run can compare like with like, but the scenario must keep working
if a source renames, splits or removes that trail.

## Definitions

- **Viable trip:** a plan the tester would act on that names the trail or
  trail system, the staging point and an overnight option, with every unknown
  it depends on listed. It is not a statement that anything is permitted.
- **Critical question:** a question whose answer would change the go/no-go
  decision.
- **Within policy:** inside the data-held `max_age_hours` for that fact.
- **Planning step:** one distinct action the tester takes towards the plan,
  in or out of Ohvernight (a search, a selection, a filter change, opening
  another app or site).

## What the tester tries to do

1. Identify a suitable motorized trail or trail system.
2. Understand whether motorcycles are actually allowed on it.
3. Identify the relevant trailhead or staging point.
4. Understand approach-road and access considerations for their vehicle.
5. Identify at least one reasonable overnight option.
6. Identify a backup overnight option where one exists.
7. Understand important closures and restrictions for their dates.
8. Understand where each fact came from.
9. Understand what remains unknown or unverified.
10. Leave with a usable outing without extensive outside research.

For each step record one of: **done in Ohvernight**, **done partly** (say what
was missing), **not possible in Ohvernight** (say where the tester went
instead), or **Ohvernight correctly said unknown**.

"Correctly said unknown" is a good outcome, not a failure. A step fails when
the product is silent, misleading, or leaves the tester to assume.

## Measures

| Measure | How it is taken |
|---|---|
| Time to a viable trip | Minutes from opening Ohvernight to a viable trip as defined above. "Not reached" is a valid result. |
| Planning steps required | Count of planning steps as defined above, to the viable trip or to giving up. |
| External apps and sites required | Count and name each one, and the step that forced it. |
| Manual transfers between apps | Each time a place name, coordinate or route is copied or re-found elsewhere. |
| Unresolved critical questions | Critical questions, as defined above, that were never answered. |
| Unsupported assumptions | Things the tester had to assume that no source, in or out of Ohvernight, supported. |
| Proximity assumptions made | Times the tester treated "near" as "connected", "legal" or "suitable". Lower is better. Counted separately because the product must never encourage it. |
| Evidence freshness and completeness | For the facts relied on: how many carried a source and a review date, and how many were within policy. |
| Evidence coverage shown | For the trail and the overnight option: which restriction categories Ohvernight showed as checked, and which as not checked. At baseline, where that concept does not exist in the product, record the region fact-coverage statements shown. |
| Overnight backup available | Yes, no, or unknown. |
| Explainability | Can the tester say, in their own words and from what Ohvernight showed, why the plan is viable and what is still uncertain? |
| Phone burden | Run on a phone. Record taps, screens and any point where the tester gave up on the phone. |

A milestone improves the scenario when measures move in the right direction
**without** any unknown being converted into an unsupported claim. A faster
time reached by hiding uncertainty is a regression.

A product that answers "unknown" to everything scores well on the step
outcomes. Only the time, planning-step and external-apps measures offset that,
so they are always reported beside the step outcomes.

## Baseline

Not yet run. The first run is owed after M4 closes and becomes the baseline.
What is known about the starting point, from the repository at `main` on
2026-10-08, is stated here so the baseline run can be checked against it.

**CURRENT, present in Douglas:**

- 102 USFS trail segments with the source's raw use strings for nine
  activities, including motorcycling.
- 73 USFS road segments with name and source route ID only (no source access
  fields; `access_status` is `unknown` on every road).
- 36 recreation-site records (17 trailheads, 5 campgrounds and 1 horse camp by
  the source's site type). They carry the source's own operational status,
  and some carry published restriction text and a published season. None of
  that is reviewed.
- One area listing without geometry, Rampart Range designated dispersed
  camping, whose text states a 1 December to 1 April camping closure from the
  official listing.
- Five generalized land management polygons, and water clipped to the county.
- A Browse finder for trails, camping and trailheads, with an activity
  selector, a date check against published trail seasons, a camping-vehicle
  selector, a saved plan and GPX export.
- Straight-line listings: "Campgrounds nearby by straight-line distance" and
  "Trailheads nearby by straight-line distance" under a trail, and "Trails for
  selected activity nearby by straight-line distance" under a point site,
  within five straight-line miles, each row marked "connection unverified".

**CURRENT, absent in Douglas:**

- any trailhead identity linked to a trail;
- any route from a staging point to a trail or to an overnight option;
- any reviewed camping permission;
- any reviewed closure or fire-restriction status;
- any vehicle constraint attached to a road;
- anything outside the county line. Water kept to about 500 m beyond it is
  approved for M4-B and is not on `main`.

Douglas fact coverage on `main` reads `context` for ownership, road access and
trail access, and `none` for public access, camping permission, closures,
restrictions and recreation permission.

The expected baseline, as a prediction to be tested and not a result:

- Steps 1 and 8 are partly possible.
- Steps 2, 3 and 5 are partly served in the product today: step 2 by the
  source's unreviewed use strings, steps 3 and 5 by the straight-line
  listings.
- Because steps 3 and 5 rest on straight-line listings, the count of proximity
  assumptions made is expected to be above zero.
- Step 9 is largely answered by the product saying unknown.
- Steps 4, 6 and 7 largely send the tester elsewhere; the unreviewed
  restriction and season text on some site records is the only in-product
  material for step 7.

## Keeping it stable

- The scenario text changes only by pull request.
- [Scenario B](acceptance-scenario-rampart-day-use.md) was added beside this
  one on 2026-10-08. A further scenario (for example an Aspen fishing and
  camping weekend once M4-C lands) may be added the same way. None replaces
  this one.
- Results are kept in order, one per milestone, so the product has a
  longitudinal baseline.
