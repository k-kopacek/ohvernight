# Canonical acceptance scenario: Douglas County dirt-bike weekend

Status: recurring product acceptance scenario, recorded 2026-10-08. It is run
by a person at the close of every milestone from M4 onward and the result is
recorded in that milestone's product review (see
[product-scorecard.md](product-scorecard.md)). It is not an automated test and
it does not replace any engineering gate.

## Why this scenario

Douglas County and the nearby Front Range motorized trail systems exercise
every hard part of the product at once: an activity that is allowed on some
trails and prohibited on others, staging areas, forest roads with vehicle
limits, a mix of developed and dispersed camping, seasonal and fire
closures, and a county boundary that the terrain ignores.

## The task

> I have a dirt bike and a weekend. Using Ohvernight, plan a ride in or near
> Douglas County with somewhere to stay overnight.

The tester brings a stated vehicle (for example a pickup with a small trailer,
or a van) and stated dates. The trail is **not** fixed in advance: choosing it
is part of the task. For repeatability the tester records which trail system
they ended up evaluating, so a later run can compare like with like, but the
scenario must keep working if a source renames, splits or removes that trail.

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
| Time to a viable trip | Minutes from opening Ohvernight to a plan the tester would act on. "Not reached" is a valid result. |
| External apps and sites required | Count and name each one, and the step that forced it. |
| Manual transfers between apps | Each time a place name, coordinate or route is copied or re-found elsewhere. |
| Unresolved critical questions | Questions that would change the go/no-go decision and were never answered. |
| Unsupported assumptions | Things the tester had to assume that no source, in or out of Ohvernight, supported. |
| Proximity assumptions | Times the tester treated "near" as "connected", "legal" or "suitable". Counted separately because the product must never encourage it. |
| Evidence freshness and completeness | For the facts relied on: how many carried a source and a review date, and how many were within policy. |
| Evidence coverage shown | For the trail and the overnight option: which restriction categories Ohvernight showed as checked, and which as not checked. |
| Overnight backup available | Yes, no, or unknown. |
| Explainability | Can the tester say, in their own words and from what Ohvernight showed, why the plan is viable and what is still uncertain? |
| Phone burden | Run on a phone. Record taps, screens and any point where the tester gave up on the phone. |

A milestone improves the scenario when measures move in the right direction
**without** any unknown being converted into an unsupported claim. A faster
time reached by hiding uncertainty is a regression.

## Baseline

Not yet run. The first run is owed at the close of M4 and becomes the
baseline. What is known about the starting point, from the repository at
`main` on 2026-10-08, is stated here so the baseline run can be checked
against it:

- **CURRENT, present:** USFS trail segments for Douglas with the source's raw
  use strings per activity, including motorcycle use; USFS road geometry with
  source access fields; 36 recreation-site records (17 trailheads, 5
  campgrounds and 1 horse camp by the source's site type); five generalized land
  management polygons; water.
- **CURRENT, absent:** any trailhead identity linked to a trail; any route
  from a staging point to a trail or to an overnight option; any reviewed
  camping permission in Douglas; any closure or fire-restriction status for
  Douglas; any vehicle constraint attached to a road; any overnight inventory
  in Douglas beyond recreation-site records; anything outside the county
  line other than water kept to about 500 m.
- Douglas fact coverage on `main` reads `none` for public access, camping
  permission, closures and restrictions, and `context` for ownership and road
  access.

The expected baseline is therefore that steps 1 and 8 are partly possible,
step 9 is largely answered by the product saying unknown, and steps 3 to 7
send the tester elsewhere. That expectation is a prediction to be tested, not
a result.

## Keeping it stable

- The scenario text changes only by pull request.
- A second canonical scenario (for example an Aspen fishing and camping
  weekend once M4-C lands) may be added beside this one. It does not replace
  it.
- Results are kept in order, one per milestone, so the product has a
  longitudinal baseline.
