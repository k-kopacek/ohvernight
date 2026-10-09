DRAFT - UNREVIEWED

# PR #15 RESEARCH TRIAGE

Reviewer: Hermes (document-review plane, read-only). Date: 2026-10-08. Base: branch research/overnight-2026-10-08, built on the research-drafts branch of draft PR #15. No network used. No file other than this one was changed. Nothing here is decided; every classification is a recommendation to the coordinator and owner.

## Method and limits

- Inputs read: DRAFT-INVENTORY-2026-10-07.md; docs/product/trust-principles.md; ROADMAP.md (first 150 lines); codex-recon-review.md (full); adventure-model.md in full to section 3, and the heading lists of continuous-explore.md and product-scorecard.md (M3 checkout). `docs/agent-stack/hermes-research.md` does not exist on this branch (the directory docs/agent-stack/ is absent); the nearest are docs/research/hermes/playbook.md and research-guide.md, which I did not read.
- Reading depth. No draft was read line by line. For every one of the 26 files I read the first lines and the heading list and ran repository-wide term searches (trust words, licence words, local paths, keys and contact patterns, present-tense product claims). Read in more depth than that: ranking-architecture-options.md (sections 1, 2, Option C and D), hermes-w2-third-set (status rule, every ALLOWED row, recommendation), M6 packet section 2, M5 matrix licence and access entries. Everything else is "skimmed". A classification of KEEP therefore means "no problem found by this depth of reading", not "checked".
- Several files measure the repository at aa5c20b (M4-A branch, pre-merge). I did not re-measure them against main.
- I re-ran two of the Codex facts for this task (see Task 2): the all-null trail-use counts and the trail-discovery.js lines.
- The 26 files are those listed in the inventory. The inventory says "27 files" in its first sentence and "26" later; the 27th (security-and-abuse-review.md) is deliberately absent. Not changed here. Note also that docs/research/ contains many other files not in the inventory (for example hermes/, future-sources/, many m4-water/ files and product-opportunities/*.md such as product-bets.md); I did not triage them.

## Task 1 - Table

Classes: KEEP, KEEP WITH EDITS, MERGE INTO, HOLD, DROP. Depth: skimmed unless stated. Paths relative to docs/research/.

| # | File | One line | Class | Edits / reason | Depth |
|---|---|---|---|---|---|
| 1 | m4-water/claims/hermes-w2-third-set-and-conflicts.md | Hermes dossiers for ~20 Douglas and Aspen waters plus claim conflicts. | HOLD | Unverified web research; inventory itself says no claim record may exist before a coordinator re-read of each source and owner approval. Its status labels ALLOWED (lines 57, 59, 159, 183, 297, 299, 301) and the "Publish now" list (about line 388) read as approvals. Needs the same coordinator re-read applied to the other dossier sets (see m4c-dossier-review.md). | skimmed + all ALLOWED rows + recommendation |
| 2 | m4-water/depth-audit.md | Adversarial audit of M4 spec and M4-A at aa5c20b: trust issues, data gaps, test gaps, owner decisions. | HOLD | Stale base (aa5c20b); inventory says one finding (legacy IDs, G1) was fixed after. Re-read against main, strike fixed items, then merge. T5 (Douglas water "refresh needed" from 2026-10-14) is time-limited and will be stale within a week. | skimmed |
| 3 | m5-land/current-land-audit.md | Measured audit of land data in the repo: fields, codes, areas, where ownership/access get confused. | KEEP WITH EDITS | Add a snapshot header: measured at aa5c20b, sha256 prefixes are of that tree; re-run counts against main before M5 spec. No trust-word problem found. | skimmed |
| 4 | m5-land/hermes/m5-land-source-matrix.md | Hermes matrix of Colorado land sources, licences, access datasets. | HOLD | Contains licence statements (lines 42, 54: "public domain"; 71: COMaP "no redistribution") and an access statement (line 247, "can support a legal-access claim"). All unverified web reads; M5 licence gate is an owner decision (see M5 gate section 5). Merge only with a banner: publisher statements, not permission to reuse or to claim access. | skimmed + licence entries |
| 5 | m5-land/M5-preliminary-research-gate.md | Owner-facing M5 gate: deficiencies, source checks, ownership vs access, licence concerns, owner decisions. | KEEP WITH EDITS | Delete the local path at line 361. Reword line 267 ("Finer and public domain") to "stated as public domain in publisher metadata; terms not read". Section 9 ("What M5 must not claim") is exactly right; keep. | skimmed |
| 6 | m6-trails/current-trail-audit.md | Measured audit of trail data: counts, overlap, lengths, use strings, ten hard cases. | KEEP WITH EDITS | Re-measure at main; add the unknown-use counts (Task 2 block 1). Section 8 problems list is useful and consistent with the merged model. | skimmed |
| 7 | m6-trails/hermes/m6a-cotrex-usfs-identity.md | Hermes: COTREX terms, schemas, USFS schema, trail vs segment identity. | HOLD | Depends on COTREX terms and written-permission status (ROADMAP M6 licensing gate): unverified external fact and owner decision. Overlaps TRAIL-PILOT.md; reconcile before merge. | skimmed |
| 8 | m6-trails/hermes/m6b-competitor-trail-identity.md | Hermes: how AllTrails, Gaia, onX etc. model trail identity. | KEEP | Self-labelled Hermes-sourced and dated; claims about third-party products are unverified but not trust-bearing. Add "retrieved 2026-10-07, may be out of date" if absent. | skimmed |
| 9 | m6-trails/M6-trail-identity-research-packet.md | Packet for M6: segment vs trail, models A-D, overlap, names, lengths, owner decisions, tests, risks. | KEEP WITH EDITS | Remove local path (line 884). Broken link to M6-source-matrix.md at line 5 (file never written): delete or mark "not written". Section 2 ("possible live problem", season check) was measured at aa5c20b; re-run on main and date it. Add Task 2 blocks 2-6. | skimmed + section 2 |
| 10 | m7-camping/hermes/m7-overnight-evidence-sources.md | Hermes: sources needed to answer "can I stay overnight here" (MVUM, RIDB, fire, closures). | HOLD | Unverified; RIDB agreement terms (lines ~201, 345) and dated fire/closure facts go stale. Needs source re-read for anything beyond "source exists". | skimmed |
| 11 | m7-camping/M7-camping-evidence-model-draft.md | M7 claim model, display rules, candidate scopes, owner decisions, test list. | KEEP WITH EDITS | Remove local path (line 572). Labels "[VERIFIED web]" (lines 159, 171) conflict with trust principle 4 and 8 vocabulary: rename to "READ ON WEB (not coordinator verified)". 70 KB; consider splitting appendices A/B. Add Task 2 blocks 7-10. Measured base aa5c20b. | skimmed |
| 12 | m8-adventure/ranking-architecture-options.md | Five ranking architectures, constraints, what must not be ranked, minimal first version. | KEEP WITH EDITS | Written before adventure-model.md merged. Option D calls its table a "relationship table" (line 241); adopt the merged vocabulary (relevant_to is a composed chain; weakest link shown) or say it does not use it. Sample explanation texts (about lines 128, 219) carry invented "Reviewed 2026-09-25 / 2026-10-20" dates; label as illustrative. Add Task 2 blocks 11-14. Strong on trust rules otherwise. | partly read |
| 13 | product-opportunities/hermes/b9-bear-case.md | Hermes: nine ways the product fails, with evidence. | KEEP | Labelled and sourced. Mentions legal review needed before marketing as authoritative (good). | skimmed |
| 14 | product-opportunities/hermes/c8a-competitor-strategy-mapping.md | Hermes: onX, Gaia, AllTrails, CalTopo, Trailforks, FarOut, COTREX strategy. | KEEP | Competitor facts unverified; dated. | skimmed |
| 15 | product-opportunities/hermes/c8b-competitor-strategy-camping.md | Hermes: Dyrt, Hipcamp, Campendium, iOverlander, etc. | KEEP WITH EDITS | Pitch lines at about 85, 144, 199, 227 say Ohvernight offers "legal context" / "legal-status context" / "legal and recreation context". Reword to "agency-rule context"; Ohvernight does not determine legality (trust-principles intro). | skimmed + term search |
| 16 | product-opportunities/bear-case.md | Synthesis: twelve reasons the product fails and what would change the mind. | KEEP WITH EDITS | Line 476 "Federal sources are public domain; USFS trail and road data exists independently of COTREX" is a licence generalisation presented as fact; qualify to "some federal datasets state they are public domain; terms of each dataset not verified". | skimmed + line 476 |
| 17 | product-opportunities/competitor-delta.md | Synthesis of c8a/c8b: what each competitor leaves open for Ohvernight. | KEEP WITH EDITS | Line 167 "Where can I legally sleep" used as a product feature question; reword to "Where may I be allowed to ...: what the agency pages say". Otherwise correctly says Ohvernight has not yet reviewed claims. | skimmed |
| 18 | product-opportunities/moat-analysis.md | Candidate moats and six-month copy test. | KEEP | Inference, labelled; states "no moat today". | skimmed |
| 19 | product-opportunities/first-party-data-flywheel-options.md | Options for user observations kept apart from authoritative fact. | KEEP | Consistent with trust principles (line 19 states observations establish no permission). Owner questions at section 5. | skimmed |
| 20 | customer-discovery/interview-kit.md | Interview script, screener, consent and note rules. | KEEP | Consent rules exclude home addresses, exact spots, plate numbers (line 58): good. Owner must still choose recruiting channels. | skimmed |
| 21 | customer-discovery/mvp-experiments.md | Seven cheap validation experiments plus a pricing test. | KEEP WITH EDITS | Experiments E1/E4 show overnight+activity pairs; add one line that any prototype must follow adventure-model.md (connection stays unverified, as the current app already marks it). The "nearby read as permitted" failure threshold (line 42) is good. | skimmed |
| 22 | business/hermes/p18-pricing-and-costs.md | Hermes: competitor prices, platform fees, data/AI costs. | HOLD | Time-sensitive web prices (line 100 quotes an "OpenAI GPT-6 Luna" price; Regrid, Stripe, Apple fees). Unverified and will age; hold until the owner decides monetisation. | skimmed |
| 23 | business/business-model-options.md | Three business model options with illustrative arithmetic. | HOLD | Depends on owner monetisation decision (see m4-water/decision-packets/monetization.md) and on p18 prices. Clearly labelled illustration and no selection; low trust risk, but keep out of the first batch. | skimmed |
| 24 | engineering/hermes/a17-map-accessibility.md | Hermes: map accessibility criteria and recommendations. | KEEP | Standards-based; Hermes-sourced and labelled. | skimmed |
| 25 | engineering/map-accessibility-recommendations.md | Measured findings and ranked recommendations against v2/explore at aa5c20b. | KEEP WITH EDITS | Re-verify file:line references against main (shell.js, sheet.js, css lines move). Many "VERIFIED" labels (51 hits) mean "read in the file at aa5c20b"; rename to "READ IN FILE". Items touching trust wording or colour meaning need owner approval (it says so). | skimmed |
| 26 | engineering/source-monitoring-architecture.md | Future design for monitoring sources for change; budgets; what must never be automated. | KEEP | Clearly "future design, nothing implemented". Names RIDB_API_KEY only as an Actions secret. Section 5 forbids automating confirmation, consistent with trust rule 4. | skimmed |

Counts: KEEP 8 (rows 8, 13, 14, 18, 19, 20, 24, 26); KEEP WITH EDITS 11 (rows 3, 5, 6, 9, 11, 12, 15, 16, 17, 21, 25); HOLD 7 (rows 1, 2, 4, 7, 10, 22, 23); MERGE INTO 0; DROP 0. Total 26.

MERGE INTO: none. The inventory is right that the Hermes reports and their syntheses are different layers (bear-case.md over b9, competitor-delta.md over c8a/c8b). Two possible later folds, not recommended now: a17 into map-accessibility-recommendations.md after both are merged; m6a with docs/TRAIL-PILOT.md (not read). DROP: none; nothing is superseded, though the held files age quickly.

## Trust or accuracy problems

File and line numbers are in the checkout at the time of writing. "Local path" items are not secrets but should not be committed.

Trust-rule overreach and wording
1. m4-water/claims/hermes-w2-third-set-and-conflicts.md:57, 59 - "Fishing" and "Paddling / kayaking" ALLOWED, resting on "The confluence provides access for fishing, kayaking and trail use." That is a description of access, and the file's own status rule says access is never labelled allowed. Treat as UNKNOWN until re-read.
2. same file:301 - Swimming ALLOWED from "Boating, swimming, and water skiing are all possible in the area"; the row itself notes the page defines no swim area or dates. Inferred permission. Downgrade.
3. same file:159, 183, 297, 299 - ALLOWED labels; quoted statements are closer to permission but each needs reach, date and live-page re-check before any record. Ruedi's 2026 closure dates will have moved.
4. same file, Recommendation (about lines 386-388) - "Publish now:" list. Conflicts with the inventory's "no claim record exists ... owner approval" and with trust-principles section 8. Replace with "Candidates for a reviewed record".
5. product-opportunities/bear-case.md:476 - "Federal sources are public domain". Licence generalisation; see licensing below.
6. product-opportunities/hermes/c8b-competitor-strategy-camping.md:~85, 144, 199, 227 and competitor-delta.md:167 - "legal context", "legal-status context", "legally sleep": implies Ohvernight determines legality.
7. m7-camping/M7-camping-evidence-model-draft.md:159, 171 and engineering/map-accessibility-recommendations.md (51 uses) - "VERIFIED" used for "read by an agent". Trust principle 4 reserves verification for reviewed interpretation. Rename.
8. m8-adventure/ranking-architecture-options.md:~128, ~219 - sample UI text shows "reviewed 2026-09-25" and "Reviewed 2026-10-20" as if records exist. Mark illustrative. (The ROADMAP's own phrase "based on verified evidence", quoted at section 1, is roadmap wording; leave it.)

Licensing claims presented as permission or fact
9. m5-land/hermes/m5-land-source-matrix.md:42, 54 - "public domain" for BLM Colorado SMA and PAD-US, quoted from publishers; line 292 correctly warns not to generalise. m5 gate lines 35, 195, 267 repeat it; 197 notes PAD-US Data Explorer terms were not read. Nobody should read "public domain" as clearance to republish clipped or reclassified data.
10. same matrix:71 - COMaP states data must not be redistributed. A restriction, correctly noted; it matters for any M5 source decision.
11. same matrix:247 - "can support a legal-access claim to reach BLM land". Its own next line limits this. Needs "(not established by Ohvernight)" wording in any published form.

Security-sensitive or hygiene
12. m5-land/M5-preliminary-research-gate.md:361, m6-trails/M6-trail-identity-research-packet.md:884, m7-camping/M7-camping-evidence-model-draft.md:572 - absolute local paths (local scratch). Remove.
13. No credentials, keys or contact details found. RIDB_API_KEY appears by name only (M7 draft 37, 105-108, 535; source-monitoring 227-228). M7 draft:37 quotes the pipeline's error string; harmless. engineering/security-and-abuse-review.md is correctly not in the PR; no draft discusses the legacy-site weakness by search (terms: legacy site, root site, exploit, bypass).

Accuracy and currency
14. m6-trails/M6-trail-identity-research-packet.md:5 - companion M6-source-matrix.md does not exist (known in the inventory).
15. m4-water/depth-audit.md:4 and G1 - stale base; G1 (legacy ID chain) fixed after aa5c20b per inventory. depth-audit T5: "refresh needed from 2026-10-14".
16. m5-land/current-land-audit.md, m6-trails/current-trail-audit.md, m7 draft section 2, map-accessibility-recommendations.md - counts, hashes and file:line references measured at aa5c20b.
17. business/hermes/p18-pricing-and-costs.md:100 - quotes an API price for a model I cannot confirm exists; unverified, time-sensitive.

Contradiction with the merged product model (adventure-model.md, continuous-explore.md, product-scorecard.md)
18. m8 ranking options Option D (~241-264): the "pair" with a "relationship" and a `connection` claim defaulting to unknown is compatible in spirit, but uses its own words. adventure-model.md defines relevant_to as a composed chain whose weakest link is shown, and says nothing may be populated from today's distance listings. The doc also lists "straight-line distance" as a neutral ordering key (lines ~202, 409): adventure-model flags the present distance wording as an owner question. Present as an open owner decision, not a design default.
19. Not found: no file claims statewide or continuous Explore behaviour, and none treats trailheads as existing entities (adventure-model: they do not exist as identities; the M7 draft reads 17 TRAILHEAD site types as source records, which agrees). Searched only; continuous-explore.md was read by headings, so I cannot rule out a conflict in the accessibility files about region-bound assumptions (map-accessibility-recommendations.md assumes the shell at aa5c20b).

Future plans stated as current behaviour
20. None found in the 26 by term search (checked "Ohvernight shows/offers/provides/has/checks..."). Strategy files consistently say Ohvernight "has not" reviewed claims. Outside the 26: product-opportunities/product-bets.md:21 says "Ohvernight shows two or three candidate activity-overnight pairs"; it is not in this PR, but it describes a future feature in present tense and conflicts with the merged model. Flag for whoever owns that file.

## Proposed merge order

Batch 1 - low risk, could be approved first (no trust or licence content, no stale measurement, labelled as research): 13 b9-bear-case, 14 c8a, 8 m6b, 18 moat-analysis, 19 flywheel options, 20 interview-kit, 24 a17-map-accessibility, 26 source-monitoring-architecture. (8 files.)

Batch 2 - after small wording edits listed above: 15 c8b, 16 bear-case, 17 competitor-delta, 21 mvp-experiments, 5 M5 gate, 3 current-land-audit.

Batch 3 - after re-measuring against main and applying Task 2 additions: 6 current-trail-audit, 9 M6 packet, 11 M7 draft, 12 M8 ranking options, 25 map-accessibility-recommendations.

Batch 4 - hold for owner decision or coordinator re-read: 1 W2 dossiers, 2 depth-audit, 4 M5 matrix, 7 m6a, 10 m7 sources, 22 p18, 23 business-model-options.

Dependencies: 15-17 should be merged together with their Hermes sources (13, 14, and c8b itself). 4 should wait until the M5 licence decision. 22 and 23 merge together or not at all.

## Task 2 - Codex findings, grouped by destination

Provenance line on every block. Items marked UNVERIFIED rest on code or data Hermes did not open. Do not paste before the coordinator has diffed the destination section (the Codex review searched by key term only and could not tell whether a section already says the same). Nothing was edited.

### A. m6-trails/current-trail-audit.md

Block 1 (M6-5). Place: new short paragraph in section 5 (use, surface and season fields), or after "Key findings".
```
Unknown-use counts, display snapshot of 2026-10-08
Segments in which all four raw strings (managed, accpt, disc, restricted) are null for an activity.
Null means unknown. It does not mean permitted, and it does not mean prohibited.
  hiking:           Aspen 40 of 123 segments;  Douglas 27 of 102
  mountain biking:  Aspen  8;                  Douglas 26
  motorcycling:     Aspen  4;                  Douglas  0
Counted from v2/regions/<region>/display/trails.geojson, not canonical data. Counts will change on refresh.
Source: Codex reconnaissance at commit 2795625, 2026-10-08; measured facts spot-checked by Hermes
(Hermes re-ran these six counts with jq on the display files; canonical data not checked.)
```

### B. m6-trails/M6-trail-identity-research-packet.md

Block 2 (M6-7). Place: section 11, tests.
```
Test requirement: presentation de-duplication is not identity.
v2/trail-discovery.js nearbyTrails() keeps segments within 5 straight-line miles, sorts by distance,
drops repeats of the key (trail_number || id) + '|' + name, and keeps the first three (lines 25-38).
A farther segment with the same name and number can vanish from "nearby" while search and selection still
target that canonical segment. If trail_number is empty the key falls back to the id.
An M6 test must show that search, detail, selection, nearby and saved aliases all resolve to the same segment.
This describes current presentation behaviour; it is not an identity rule.
Source: Codex reconnaissance at commit 2795625, 2026-10-08; measured facts spot-checked by Hermes
(Hermes read lines 25-38 on this branch. Whether the fallback matters for real data: UNVERIFIED.)
```

Block 3 (M6-8). Place: section 5, "Candidate identity models", marked unreviewed.
```
Unreviewed observation: reuse boundary with water grouping (lib/water.py).
Technique that may carry over: six-decimal endpoint keys, sorted components, input immutability,
canonical-to-display maps, legacy aliases.
Rules that must not carry over: GNIS names, perennial propagation, O1 bridges, connector rules.
group_flowlines must not be applied to trails as it stands.
Source: Codex reconnaissance at commit 2795625, 2026-10-08; measured facts spot-checked by Hermes
UNVERIFIED: Hermes did not open lib/water.py; the claim about what the module does is Codex's.
```

Block 4 (M6-9). Place: section 5, proposed invariants. Check first whether many-to-many is already stated (the Codex review found it only in m6a).
```
Invariant candidate: membership is many-to-many.
One source segment may belong to several official routes; a route may have disconnected display parts.
Water grouping assigns each flowline to one group; trails must not copy that rule.
Source: Codex reconnaissance at commit 2795625, 2026-10-08; measured facts spot-checked by Hermes
UNVERIFIED as a data fact: no multi-route segment was shown; this is a design constraint.
```

Block 5 (M6-12, TD-5, TD-6). Place: section 11, tests. Add only cases not already present.
```
Additional test cases for an M6 specification (add only those missing):
- source key replacement (a republished service changes object IDs)
- two routes that cross with no shared node
- alias round trip: old saved ID -> alias -> current ID -> same segment
- alias migration: missing old IDs, changed namespaces, sanitisation collisions, one-to-many
  replacements, aliases that point to an excluded feature
- never clear aliases to make a build pass; never compare rows by position
- before refreshing into saved selections, verify permanent keys and change history (zero repeated IDs
  today does not show stability after a republish)
Source: Codex reconnaissance at commit 2795625, 2026-10-08; measured facts spot-checked by Hermes
(Zero repeated trail IDs: verified. Roads using source_route_id in Douglas: UNVERIFIED.)
```

Block 6 (Difficult Creek sentence). Place: section 3 or the hard-cases list, only if absent.
```
The water feature Difficult Creek and the trail Difficult Creek Trail are different namespaces.
Never match a trail to a water feature by name. Aspen trail records usfs-trail-8921819 and
usfs-trail-8923909 (trail number 2146) are grouping candidates only; no reviewed grouping exists.
Source: Codex reconnaissance at commit 2795625, 2026-10-08; measured facts spot-checked by Hermes
(Both IDs exist in Aspen and none in Douglas: verified. Shared endpoint, merge result and equal activity
objects: UNVERIFIED; may rest on rounded display geometry.)
```

### C. m7-camping/M7-camping-evidence-model-draft.md

Block 7 (M7-8). Place: section 4.2 "What M7 adds", only these two lines if missing.
```
Add to the dimension list (identity, geometry, inventory, setup, permission, operations, restriction,
stay/permit, availability, transport):
- transport: a partial or failed refresh must not publish an inventory that looks complete.
- stay window: the departure day is part of the trip when evaluating restrictions.
Source: Codex reconnaissance at commit 2795625, 2026-10-08; measured facts spot-checked by Hermes
UNVERIFIED whether section 4.2 already says this; the Codex review did not diff the wording.
```

Block 8 (M7-9). Place: section 8, owner decisions.
```
Process rule: setup vocabulary (tent-only, trailer or RV dimensions, high clearance, capacity),
any activity/setup vocabulary, any new fact_coverage policy and any new producer field require a reviewed
amendment to the data contract (ADR-005; v2/pipeline/docs/data-contract.md) before use.
Source: Codex reconnaissance at commit 2795625, 2026-10-08; measured facts spot-checked by Hermes
(Rule follows from the contract; Hermes did not re-read the contract text for this block.)
```

Block 9 (M7-11). Place: section 10, tests. Add only missing cases.
```
Evaluator tests (add only those missing): injected dates; fact-specific review age; full-trip restriction
starting on departure day; indefinite orders; malformed seasonality; stale positive vs stale negative;
tentative identity; tent/vehicle mismatch; unknown dimensions; partial source failure;
cross-jurisdiction rules. A stale restriction stays in force and is flagged; a stale supportive claim is unknown.
Source: Codex reconnaissance at commit 2795625, 2026-10-08; measured facts spot-checked by Hermes
UNVERIFIED which of these section 10 already lists.
```

Block 10 (M7-6). Destination: section 4 of the M7 draft (the Codex-suggested v2/pipeline/docs/curation.md is not a PR #15 draft; propose the same sentence there in a later, separate change).
```
Current limitation: the curated reviewed-site template and 09_reviewed_sites.py are specific to Aspen
and to vehicle sleeping (inside_vehicle). They are not a general tent / RV / hammock model.
The script requires a real Point, a confirmed site, valid review and operating dates, a compatible
vehicle/sleeping setup, and evidence for five named fields.
Source: Codex reconnaissance at commit 2795625, 2026-10-08; measured facts spot-checked by Hermes
UNVERIFIED: inside_vehicle appears in v2/pipeline/docs/curation.md, but Hermes did not open the script.
```

### D. m8-adventure/ranking-architecture-options.md

Block 11 (M8-2). Place: section 1, after the table. Describes today only.
```
Current behaviour (v2/trail-discovery.js, lines 25-38): adventureOptions() takes campground and dispersed
places, finds trails within 5 straight-line miles (up to 3, de-duplicated by trail_number-or-id plus name),
and sorts places with status "excluded" last, then by nearest trail distance. This is a distance listing.
It is not a date-evaluated or permission-evaluated result and not a verified-adventure engine.
See docs/architecture/adventure-model.md section 1.
Source: Codex reconnaissance at commit 2795625, 2026-10-08; measured facts spot-checked by Hermes
(Lines 25-38 read by Hermes. UI wording and the managed/accpt filter: UNVERIFIED.)
```

Block 12 (M8-5). Place: appendix, only if sections 2 and 5 do not already hold it.
```
Query envelope, seven dimensions (design input, not a schema):
1 geography: coverage boundary kept separate from search radius
2 dates: ISO, timezone, whole trip including departure day
3 activities: unsupported coverage is not permission
4 overnight: candidate geometry is not an option
5 vehicle/setup: unknown is retained, not defaulted
6 distance/access: direct-distance basis; routing only from a reviewed source
7 evidence context: pinned data versions, evaluator version, injected time
Source: Codex reconnaissance at commit 2795625, 2026-10-08; measured facts spot-checked by Hermes
(Design proposal; nothing measured.)
```

Block 13 (M8-8). Place: section 2, constraints.
```
Additional ranking constraints: deterministic tie-break on stable IDs; keep the raw facts behind each rank
term; measure freshness per fact, not by a document's generated_at; do not read evidence.confidence in a
score (the data contract note N4 says it differs across regions); never penalise a region for missing data.
Source: Codex reconnaissance at commit 2795625, 2026-10-08; measured facts spot-checked by Hermes
UNVERIFIED: that evidence.confidence is formally "deprecated"; N4 notes the cross-region difference.
```

Block 14 (M8-11, M8-12). Place: section 5, minimal first version, or the future M8 spec test section.
```
Acceptance fixtures: unknown vs unsupported region or activity; absent vs empty vs failed inventory;
historical evaluated trips; restriction beginning mid-trip or on departure day; stale positive and stale
negative; activity conflicts; missing dimensions; proximity without connection; duplicate cross-source
options; group aliases; ordering invariance. Include a no-result explanation and a pointer to free Explore
instead of manufacturing itinerary certainty.
Source: Codex reconnaissance at commit 2795625, 2026-10-08; measured facts spot-checked by Hermes
(Test list; not run.)
```

### E. engineering/technical-debt-register.md (new file; destination for the technical-debt items)

Per the Codex review, a short register with the preamble below; the owner has not yet decided that a register file should exist (see Owner decisions). Each entry is a separate block.

Block 15 (preamble, TD-15).
```
DRAFT - UNREVIEWED. Technical-debt register. Reconnaissance at commit 2795625, 2026-10-08.
Entries are observations, not verified by test. This is not a security audit and found no validated
security finding. Each entry names its commit and date; counts and sizes change on refresh.
Source: Codex reconnaissance at commit 2795625, 2026-10-08; measured facts spot-checked by Hermes
```

Block 16 (TD-2). Written at the level of "a budget is needed", not as request recipes.
```
TD-2. Retry layering. The general ArcGIS client layers adapter retries, JSON-level retries and recursive
batch splitting, so an outage can multiply requests and wall time. Proposed follow-up (owner approval needed):
one retry and request budget per run, and resumable plans. The M4-B tiled transport avoids hidden retries
and enforces caps.
Source: Codex reconnaissance at commit 2795625, 2026-10-08; measured facts spot-checked by Hermes
UNVERIFIED: Hermes did not open the client or transport code. The live-session failure is not independently checked.
```

Block 17 (TD-3).
```
TD-3. Object-ID recheck. Comparing the set of object IDs before and after cannot detect changed attributes
under an unchanged ID set. A discovery recheck shows ID consistency, not a frozen service. Source revision
fingerprints should use supported source fields. See engineering/source-monitoring-architecture.md
(already discusses fingerprints; check for overlap).
Source: Codex reconnaissance at commit 2795625, 2026-10-08; measured facts spot-checked by Hermes
UNVERIFIED: reasoning, not a measurement.
```

Block 18 (TD-6).
```
TD-6. Alias migration. Alias collisions correctly stop a build. Needed tests: missing old IDs, changed
namespaces, sanitisation collisions, one-to-many replacements, aliases to excluded features.
Never clear aliases to pass a build; never compare rows by position.
Source: Codex reconnaissance at commit 2795625, 2026-10-08; measured facts spot-checked by Hermes
UNVERIFIED: test list is a proposal; the build behaviour was not run.
```

Block 19 (TD-7). Principle may become an ADR later; owner choice.
```
TD-7. Geometry repair. Clipping and display building call make_valid or ring repair, and the corridor
builder repairs and buffers in EPSG:26913. Repair can change topology. Repair must never be read as legal
or parcel-level boundary interpretation (trust-principles section 7). Future diagnostics should count
dropped or changed parts and record the original invalidity reason.
Source: Codex reconnaissance at commit 2795625, 2026-10-08; measured facts spot-checked by Hermes
UNVERIFIED: Hermes did not open the code that makes these calls; no existing doc mentions make_valid.
```

Block 20 (TD-8).
```
TD-8. Display build is not atomic. build_region(write=True) writes artifacts one at a time, index last.
An interrupted build could leave a mixed set that Git or CI would later detect by hash. Proposal (needs a
spec): build into a temporary directory and swap, with rollback.
Source: Codex reconnaissance at commit 2795625, 2026-10-08; measured facts spot-checked by Hermes
UNVERIFIED: Hermes did not open build_display.py.
```

Block 21 (TD-10). Dated budget status.
```
TD-10. Display budgets at 2026-10-08 (limits from v2/pipeline/tests/browser/test_display_budgets.py).
Browser limits: map-usable 500000 B; all display bytes 4500000 B. Douglas map-usable maximum 456170 B
(headroom 43830 B, arithmetic checked). Douglas water display 954452 B equals waterways 834148 B plus
waterbodies 120304 B (checked on disk). Other maxima (Aspen 382538 and 3541592; Douglas 2736972) and
the 1887725 limit: UNVERIFIED. Re-measure with node v2/pipeline/tests/browser/measure.mjs before use.
Source: Codex reconnaissance at commit 2795625, 2026-10-08; measured facts spot-checked by Hermes
```

Block 22 (TD-4). Home is the m4-water identity docs; a short pointer here is the only item that can be added now.
```
TD-4. Water identity. Water uses permanent_identifier-based stable IDs, uniqueness checks, exact
historical geometry matching and carried-forward aliases. Raw permanent-ID uniqueness was not assessable in
the tiled run because it produced no feature pages. Do not state the uniqueness as established.
Source: Codex reconnaissance at commit 2795625, 2026-10-08; measured facts spot-checked by Hermes
UNVERIFIED: E1 test numbers not re-run; belongs with the M4-B status notes in docs/research/m4-water/.
```

Block 23 (TD-11). HELD - do not paste. The E3 dry-session numbers (Douglas map-usability 919.9 ms against 870.24; all-default 2126.6 against 1958.04; three final sessions remaining) exist only in untracked files in the m4b worktree. They should be published only through the owner-approved performance record, once the coordinator decides whether those untracked files are published as a unit. Status: UNVERIFIED by Hermes (not re-run).

Items from the Codex review not routed, per its "Do not publish" list: M6-1 to 4, 10, 11, 13; M7-1, 3, 4, 5, 12, 13; M8-3, 4, 6, 7, 9; TD-9, TD-14; TD-13 at most one profiling to-do line. Raw logs in the overnight folder were not reviewed and should be checked for local paths and request URLs before any commit.

## Owner decisions needed

1. Whether the W2 dossier file (draft 1) and the other Hermes dossier sets may ever feed claim records, and who re-reads the sources first. Until then it stays HOLD.
2. M5 and M6 licensing: accept or reject "publisher says public domain" as sufficient to use a dataset; COTREX written permission; COMaP no-redistribution. Gates files 4 and 7.
3. Monetisation direction (files 22 and 23); both HOLD until chosen.
4. Whether a technical-debt register file should exist (Task 2 block 15), or the entries belong in ROADMAP.md or an ADR.
5. Whether the untracked overnight performance folder (overnight-report, performance-procedure, E1/E2 notes) is published as a unit; blocks TD-11.
6. M8: may straight-line distance be shown or used as an ordering key (ranking options question 5; adventure-model raises the wording as an owner question), and whether Option D adopts the adventure-model vocabulary.
7. Vocabulary: rename "VERIFIED" in agent-measured research to a non-trust word (files 11 and 25), and "legal context" in strategy copy (file 15, 17).
8. Whether the M5 gate and the audits should be re-measured against main before merge or merged as dated snapshots.
9. Whether product-opportunities/product-bets.md:21 ("Ohvernight shows ... pairs") should be corrected; outside this PR.
10. Whether security-and-abuse-review.md stays withheld (inventory note); not part of this triage.

END OF TRIAGE. DRAFT - UNREVIEWED.
