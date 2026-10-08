# Hermes Ohvernight research playbook

How the coordinator briefs and routes Hermes, written from the Hermes runs of
the M4 cycle (6–7 October 2026). It complements
[research-guide.md](research-guide.md), which is the text given to Hermes;
this file is for whoever writes the brief. Goal: less shared usage for more
output that survives review.

Hermes has no new authority from this document. It runs with web search and
page reading only.

## 1. What the M4 runs showed

| Run | Subject | Model | Outcome | Lesson |
|---|---|---|---|---|
| A | Authoritative water sources | Sol | Good | Broad source survey works when the brief lists candidate publishers and the report format |
| B | Source schema semantics | Sol | Good, with one wrong expectation | It assumed reservoir purpose codes would separate detention ponds. A count from the real service showed almost none are coded that way. Schema research needs a count, not only a dictionary |
| C | Official recreation signals | Sol | Stalled, then good | The first attempt repeated one search 50 times. The re-run with exact starting URLs and a search cap finished cleanly |
| D | Community sources and terms | Luna | Good | Terms reading is extraction; Luna was sufficient |
| E | Audit of our own water | Luna | Useful, soft numbers | It had no repository access and estimated "50–70% clutter". Counts must be computed locally and handed over |
| F | CPW structured data and terms | Sol | Good | A focused follow-up with exact endpoints and a list of metadata fields to read produced a clear "unclear" answer |
| G, H | Claim dossiers for 15 waters | Sol | Good; one rule broken | It proposed access "allowed" for hike-in lakes despite the trust rules. The brief now states the access rule as a hard rule |
| I | NHD against 3DHP | Sol | Good | Sample-feature queries in both services, with named features and coordinates supplied, gave decisive evidence |
| P1, P2 | Competitor map; customer pain | Luna | Good | Breadth research is cheap on Luna |
| P3 | Product synthesis | Sol | Good | Synthesis over supplied reports needs few tool calls |

Usage, read from the shared account before and after: a Sol run cost about
one percentage point of the weekly allowance; a Luna run cost a fraction of
that. The whole first research phase (six runs) cost about four points.

## 2. Model routing

| Use Luna (high reasoning) for | Use Sol (medium reasoning) for |
|---|---|
| Reading terms and licence pages | Ambiguous source semantics (field meanings, crosswalks) |
| Competitor and pricing surveys | Deciding a claim status from an operator's wording |
| Complaint and review clustering | Synthesis across reports |
| Source inventories and watchlists | Comparing two schemas with real records |
| Any task that is mostly "open these pages and extract" | Anything where a wrong reading becomes a wrong claim |

Start with Luna when unsure and the cost of a wrong answer is a re-run.
Start with Sol when the output feeds a trust decision.

## 3. What makes a brief work

1. **Give exact starting URLs.** Every stalled or wandering run started from
   a topic. Every clean run started from pages.
2. **Cap the method in numbers.** At most 10 searches for a focused task, 25
   for a broad one; about 40 or 70 tool calls; never repeat a query; rephrase
   once at most. State what to do when a page will not load.
3. **Give the report's sections.** Hermes fills a structure reliably. It
   wanders without one.
4. **Supply repository facts.** Hermes cannot see the repository. Compute the
   counts locally and paste them in.
5. **State trust rules as hard rules with the failure named.** "Never
   propose access allowed: a trailhead, a road or public land does not
   establish it" worked where the general principle did not.
6. **Ask for the sentence relied on.** A quoted sentence with a URL can be
   re-checked in one request. A paraphrase cannot.
7. **Ask separately about each permission in a terms review:** fetch,
   transform, store publicly, redistribute, commercial use, attribution.
8. **Run independent tracks in parallel, and synthesis after.** Three or four
   runs at once caused no trouble.
9. **Keep runs single-purpose.** One report per run; the coordinator stores
   it verbatim and writes the synthesis.

## 4. Query patterns that paid off

- ArcGIS REST: the service and each layer with `?f=pjson`; small attribute
  queries with `returnGeometry=false` and a low record count; statistics
  queries grouped by a code field.
- ArcGIS Online items:
  `https://www.arcgis.com/sharing/rest/content/items/<id>?f=pjson` for
  `licenseInfo` and `accessInformation`.
- Socrata catalogues: the catalogue API for licence and attribution fields.
- Forest Service: the forest's `alerts` pages hold forest orders, which state
  prohibitions that recreation pages do not (Maroon Lake).
- Operators: the "recreation" page for each reservoir, and any FAQ and rules
  PDF, which often hold the plainest sentence (Rueter-Hess swimming).

## 5. Sources that were consistently valuable

Agency service metadata; USGS data dictionaries and crosswalk tables; forest
order pages; water utility recreation pages (Denver Water, Douglas County,
Aurora); state park pages; official pricing pages and help centres.

## 6. Sources that wasted time or misled

- Aggregated search results for licence questions: the decisive text is on
  the publisher's own page or absent.
- Pages that return a short shell to a script (some county pages needed a
  browser-like request).
- Secondary articles about a dataset's status, when the service's own
  metadata states it.
- Community sites as evidence for anything but community sentiment.

## 7. What the coordinator re-checked by hand, and should keep re-checking

| Claim | How it was checked |
|---|---|
| Service field names and domains | Reading the `?f=pjson` endpoints directly |
| Counts by feature type in each region | A statistics query against the service |
| Operator restrictions (Cheesman, Strontia Springs, Rueter-Hess, Chatfield, Maroon Lake) | Fetching the page and finding the sentence |
| That a Fishing Atlas service exists and what it lists | Reading its metadata |
| South Platte and Hunter Creek segment classes | Counting in the canonical data |

Rule of thumb: re-check every sentence that would become a restriction or a
permission, every licence conclusion that would allow storing data, and every
number that a rule depends on. Do not re-check market observations one by
one; sample them.

## 8. Templates

- **Evidence dossier and source report:** sections 7 and 8 of
  [research-guide.md](research-guide.md).
- **Licensing checklist:** section 4 of the guide.
- **Competitor analysis:** audience; jobs; strongest features; data
  strengths; domains covered; overnight capability; offline; planning;
  social; price with page URL and date; free and paid boundary; premium
  features; weaknesses; missing cross-domain links; where users rely on
  another app.
- **Product opportunity:** target user; specific job; trigger moment; current
  workflow and apps; pain; the Ohvernight experience; smallest version; data
  required, held and missing; why someone might pay; what would make them
  cancel; competitors; defensibility; trust risk; build complexity; smallest
  validation experiment; success metric; roadmap fit.

## 9. Stop and escalation conditions

Hermes stops and reports when: the method's caps are reached; new sources
repeat what is found; the only evidence is community content; terms prohibit
the intended use; official sources conflict on a restriction; or the answer
needs someone to be contacted.

The coordinator escalates to the owner when a Hermes finding implies: a new
positive claim; a source or licence interpretation with material
uncertainty; a change to trust wording; or a product decision.

## 10. Usage discipline

- Read the shared allowance before dispatching and after each wave.
- Codex's implementation work has priority on the shared allowance.
- Do not re-run a completed track for confirmation; re-check the specific
  claims instead.
- Prefer one focused follow-up to a broad repeat.
