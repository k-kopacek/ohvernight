# Canonical acceptance scenario B: Rampart family day-use and dirt-bike outing

Status: recurring product acceptance scenario, approved by the owner and
recorded 2026-10-08, with its baseline run of the same date. It is run by a
dedicated tester who did not implement the work, at the close of every
milestone from M5 onward, and the result is recorded in the product review (see
[product-scorecard.md](product-scorecard.md)). It is not an automated test, it
replaces no engineering gate, and it is not a merge gate for M4.

It does **not** replace
[Scenario A](acceptance-scenario-douglas-dirt-bike.md). The two test different
things, and both are longitudinal product benchmarks for M5 to M8:

| | Tests |
|---|---|
| **Scenario A** | Douglas dirt-bike riding with overnight planning. |
| **Scenario B** (this document) | Rampart dirt-bike riding with a family spending the day nearby and no overnight stay. |

Labels: **CURRENT** is what `main` does today, **PLANNED** is direction without
an approved specification.

## Why this scenario

It is a real outing, not a constructed one. It adds what Scenario A does not
exercise: a starting point, a second party with different needs from the
rider, day use as distinct from overnight use, a named recreation area that
the user thinks of as one place, and a late-season date on which seasonal
facilities and published seasons matter.

## The task

> Starting from my home near Spruce Mountain / Larkspur, where is the closest
> practical place to access Rampart Range Motorized Recreation Area for dirt
> biking while my family has a legal and comfortable place nearby to spend the
> day with a picnic and hammock?

Fixed for every run, so that results are comparable across milestones:

- **Origin:** near Larkspur / Spruce Mountain, Colorado. It is stated only at
  that precision.
- **Rider:** a dirt bike that is not street-legal, carried in a pickup with a
  small trailer.
- **Family:** remains nearby for the day to picnic, read and, if it is
  established that they may, use a hammock. No overnight stay is required.
- **Needs:** legal and practical staging, current restrictions, and a backup.
- **"Closest"** means practical driving. It never means straight-line
  distance.
- **Timing:** an October weekend. The baseline run used 10–11 October 2026.
  The timing stays late-season in every run, because seasonal ambiguity was
  one of the important failures of the baseline.
- **Tester familiarity:** recorded with the result, as in Scenario A.

Unlike Scenario A, the destination area is fixed in advance. Choosing the
staging point and the family's day-use place within it is the task.

## Definitions

The definitions of **critical question**, **within policy** and **planning
step** in
[Scenario A](acceptance-scenario-douglas-dirt-bike.md#definitions) apply
unchanged. **Viable trip** applies with one substitution: where Scenario A
names an overnight option, this scenario names the family's day-use place. It
remains a plan the tester would act on with every unknown it depends on
listed, and it is not a statement that anything is permitted.

## What the tester tries to do

The ten steps of Scenario A are used so the two results can be compared, with
steps 5 and 6 read as the family's day-use place and its backup:

1. Identify a suitable motorized trail or trail system.
2. Understand whether motorcycles are actually allowed on it.
3. Identify the relevant trailhead or staging point.
4. Understand approach-road and access considerations for their vehicle.
5. Identify at least one reasonable place for the family to spend the day.
6. Identify a backup where one exists.
7. Understand important closures and restrictions for their dates.
8. Understand where each fact came from.
9. Understand what remains unknown or unverified.
10. Leave with a usable outing without extensive outside research.

Each step is recorded with Scenario A's outcome vocabulary: **done in
Ohvernight**, **done partly**, **not possible in Ohvernight**, or **Ohvernight
correctly said unknown**. "Correctly said unknown" is a good outcome.

### Trip-completeness questions

The tester also records, question by question, whether Ohvernight answered:

- where to drive;
- where to park;
- where to unload and stage;
- where to ride;
- what the rules are, keeping road rules separate from trail rules: whether
  motorcycles may use the trails and which ones, other vehicle classes,
  whether the access road may be ridden on a bike that is not street-legal,
  registration and equipment requirements such as a spark arrestor, and
  seasonal dates;
- where the family can spend the day;
- what facilities exist;
- what fees apply;
- hammock status. Where no reviewed source settles it, the correct product
  answer is exactly `Hammock use: Not established from reviewed sources.`
  Trees being present establishes nothing;
- what is currently open or closed, shown separately from static rules and
  with the time it was checked;
- a backup option.

### Relationships that must be real

The product must establish these as relationships in the sense of
[adventure-model.md](../architecture/adventure-model.md), not offer proximity
in their place:

- origin → route → recreation-area entrance → staging point → motorcycle
  trail the bike may use;
- staging point → the family's day-use place.

"Within X miles" is not a substitute for either chain. The tester records
every place where the product offers straight-line distance instead, and the
wording it uses.

## Expected answer shape (PLANNED)

This is the shape that M8 output is judged against. It is not built.

- **Best plan** — one concise recommendation.
- **Why this fits** — rider and family suitability.
- **Getting there** — origin to access and staging.
- **Ride** — motorcycle options and trail connections, with their evidence.
- **Family base** — picnic, day-use or campsite information.
- **Rules you need to know** — registration, equipment, road restrictions,
  fees.
- **Current conditions** — status and restrictions, each with a checked time.
- **What we still don't know** — every unresolved item, named.
- **Alternatives** — two or three backups with the reason to choose each.
- **Sources & evidence** — expandable detail, not primary-screen clutter.

Each important statement identifies its source and checked date and whether
it is a source fact, official recreation information, a derived fact or
unknown, using the fact classes of the
[M4 specification](../specs/M4-functional-recreational-water.md). A
recommendation is a derived statement and says why.

## Measures

The [measures of Scenario A](acceptance-scenario-douglas-dirt-bike.md#measures)
apply unchanged, with "overnight backup available" read as "backup available".
This scenario adds:

| Measure | How it is taken |
|---|---|
| Manual searches | Count of searches the tester typed, in or out of Ohvernight. |
| Confirmed facts | Reviewed facts Ohvernight showed and the tester relied on. |
| Derived statements | Statements Ohvernight computed and showed, by kind. |
| Correctly surfaced unknowns | Places where Ohvernight said a thing is unknown and that was the right answer. Higher is a positive trust result. |
| Unsupported assumptions induced | Things the product would lead this user to assume without support. **The target is zero.** |

The same rule holds: a measure that improves because an unknown was hidden or
converted into an unsupported claim is a regression.

## Baseline

Run 2026-10-08 on `main` at `bb85785`, for the weekend of 10–11 October 2026,
by a dedicated tester who did not implement the work. The tester drove the
real app, served locally, in headless Chrome at 390×844 with touch emulation.
It was **not** run on a real phone, the published copy was not used, no
external link was followed, and human time-on-task was not measured; steps and
taps were recorded in its place.

### Verdict

`NO — a first-time Rampart visitor cannot currently plan the outing confidently using only Ohvernight.`

No viable trip was reached.

### Step outcomes

| Step | Outcome |
|---|---|
| 1. Trail system | Done partly |
| 2. Motorcycles allowed | Done partly, and confusing |
| 3. Trailhead or staging point | Done partly |
| 4. Approach road for a pickup and trailer | Not possible in Ohvernight |
| 5. Family day-use place | Not possible in Ohvernight |
| 6. Backup | Done partly |
| 7. Closures and restrictions | Ohvernight correctly said unknown |
| 8. Provenance | Done partly |
| 9. Unknowns | Done in Ohvernight |
| 10. Usable outing | Not possible in Ohvernight |

### Metrics

| Measure | Baseline |
|---|---|
| Time to a viable trip | Not reached |
| Planning steps in the app | 14 |
| External apps and sites required | 7 confirmed, likely 8 |
| Manual copy or retype transfers | 3–4 |
| Unresolved critical questions | 12 |
| Confirmed (reviewed) facts | 0 |
| Source-published statements relied on | About 17, all past the refresh policy |
| Correctly surfaced unknowns | 14 |
| Unsupported assumptions induced | 4 |
| Proximity assumptions made | 2, both labelled "connection unverified" |
| Evidence coverage shown | No checked / not-checked display. The eight region fact-coverage statements were shown. |
| Backup available | Only partly established: alternatives could be named, none confirmed |
| Explainability | Partial: the tester could say what is uncertain, not why a plan is viable |

The fourteen correctly surfaced unknowns are a positive trust result. The four
induced assumptions are defects or gaps to reduce toward zero:

1. the trail season verdict shown for the trip dates;
2. the directions text shown on the Rampart Entrance trailhead record;
3. a campground being usable for a family's day use;
4. fees being silently absent.

### Credit

The product never claimed that anything was open, legal or connected, and it
stated unknowns on every panel. The straight-line wording was in place
everywhere the tester looked.

### Under audit

Two baseline observations are under audit. Neither is recorded here as a
finding that the app is wrong.

- **Trail use-date semantics.** For the trip dates the app marked 40 of 76
  motorcycling segments outside published use dates. Of those 40, 38 carry
  only the source's `accepted` range `12/01-03/14`, and 2 carry only the same
  range in `managed`. The source-field meaning and whether this date verdict is
  appropriate remain under audit; this scenario does not record it as a finding.
- **Directions text.** On at least two recreation-site records the text shown
  as agency directions appears to describe a different destination.

### Not recorded as product truth

An external benchmark for this outing was researched from official sources on
2026-10-08. It is unreviewed research and is not part of this document. Nothing
here states a route, a fee, an order or a status for the outing.

## Critical gaps and roadmap placement

The baseline found these relationships and facts missing. Placement is the
owner's, recorded 2026-10-08. **Roadmap order is unchanged.**

| Milestone | Gap |
|---|---|
| **M6** | Recreation-area identity; trailhead → trail relationship; motorized-use evidence; staging and access identity. |
| **M6 / M7** | Road-specific motorized restrictions; parking and order relationships. |
| **M7** | Family day-use as an option type; staging → day-use relationship; current orders, closures and evidence coverage. |
| **M8** | Origin → driving relationship; closest practical, not straight-line; explicit answers for facts the user asked about and that remain unknown, such as hammock use and trailer suitability. |

## Target by M8

Set by the owner:

- a viable outing generated inside Ohvernight;
- no more than one external source required, for exceptional verification;
- zero unsupported assumptions;
- clear rider staging;
- evidence for which trails and uses apply to the rider's bike;
- a practical family base;
- current-status evidence;
- at least one usable alternate where the data supports it;
- unresolved facts explicitly shown, not hidden.

The target is never met by weakening evidence requirements.

## Keeping it stable

- The scenario text changes only by pull request.
- The origin, vehicle, family needs and late-season timing stay fixed.
- Results are kept in order, one per milestone, beside those of Scenario A.
