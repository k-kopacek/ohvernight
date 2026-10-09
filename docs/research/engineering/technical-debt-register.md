# Technical-debt register



> **Verification against origin/main (`bb85785ea98c8d5fb8d5694a36744b4f96a6161a`):** Not verified by test; this is a scope statement. The register is a draft reconnaissance artifact.

DRAFT - UNREVIEWED. Technical-debt register. Reconnaissance at commit 2795625, 2026-10-08.
Entries are observations, not verified by test. This is not a security audit and found no validated
security finding. Each entry names its commit and date; counts and sizes change on refresh.
Source: Codex reconnaissance at commit 2795625, 2026-10-08; measured facts spot-checked by Hermes



> **Verification against origin/main (`bb85785ea98c8d5fb8d5694a36744b4f96a6161a`):** Verified on origin/main: `new_session()` configures urllib3 retries; `get_json()` retries ArcGIS error objects; `fetch_batch()` recursively subdivides failed batches. Not verified: the M4-B tiled transport claim, which is not part of this main checkout and was not inspected.

TD-2. Retry layering. The general ArcGIS client layers adapter retries, JSON-level retries and recursive
batch splitting, so an outage can multiply requests and wall time. Proposed follow-up (owner approval needed):
one retry and request budget per run, and resumable plans. The M4-B tiled transport avoids hidden retries
and enforces caps.
Source: Codex reconnaissance at commit 2795625, 2026-10-08; measured facts spot-checked by Hermes
UNVERIFIED: Hermes did not open the client or transport code. The live-session failure is not independently checked.



> **Verification against origin/main (`bb85785ea98c8d5fb8d5694a36744b4f96a6161a`):** Verified on origin/main: the final recheck compares sorted object-ID lists only and does not compare returned attributes. The changed-attributes conclusion follows from that implementation; source revision fingerprints remain a proposal.

TD-3. Object-ID recheck. Comparing the set of object IDs before and after cannot detect changed attributes
under an unchanged ID set. A discovery recheck shows ID consistency, not a frozen service. Source revision
fingerprints should use supported source fields. See engineering/source-monitoring-architecture.md
(already discusses fingerprints; check for overlap).
Source: Codex reconnaissance at commit 2795625, 2026-10-08; measured facts spot-checked by Hermes
UNVERIFIED: reasoning, not a measurement.



> **Verification against origin/main (`bb85785ea98c8d5fb8d5694a36744b4f96a6161a`):** Not verified: origin/main has no trail alias migration system covering these proposed cases; the listed cases are a test proposal, not executed behavior.

TD-6. Alias migration. Alias collisions correctly stop a build. Needed tests: missing old IDs, changed
namespaces, sanitisation collisions, one-to-many replacements, aliases to excluded features.
Never clear aliases to pass a build; never compare rows by position.
Source: Codex reconnaissance at commit 2795625, 2026-10-08; measured facts spot-checked by Hermes
UNVERIFIED: test list is a proposal; the build behaviour was not run.



> **Verification against origin/main (`bb85785ea98c8d5fb8d5694a36744b4f96a6161a`):** Verified: `make_valid` is called by ArcGIS native polygon conversion, clipping, and corridor construction; corridor buffers use the local metric projection EPSG:26913. Not verified: no test injected an invalid geometry and measured whether repair changed topology silently.

TD-7. Geometry repair. Clipping and display building call make_valid or ring repair, and the corridor
builder repairs and buffers in EPSG:26913. Repair can change topology. Repair must never be read as legal
or parcel-level boundary interpretation (trust-principles section 7). Future diagnostics should count
dropped or changed parts and record the original invalidity reason.
Source: Codex reconnaissance at commit 2795625, 2026-10-08; measured facts spot-checked by Hermes
UNVERIFIED: Hermes did not open the code that makes these calls; no existing doc mentions make_valid.



> **Verification against origin/main (`bb85785ea98c8d5fb8d5694a36744b4f96a6161a`):** Verified: `build_region(write=True)` writes each artifact in sequence and writes `index.json` last. Not verified: no interruption/failure injection was run to observe the resulting directory state.

TD-8. Display build is not atomic. build_region(write=True) writes artifacts one at a time, index last.
An interrupted build could leave a mixed set that Git or CI would later detect by hash. Proposal (needs a
spec): build into a temporary directory and swap, with rollback.
Source: Codex reconnaissance at commit 2795625, 2026-10-08; measured facts spot-checked by Hermes
UNVERIFIED: Hermes did not open build_display.py.



> **Verification against origin/main (`bb85785ea98c8d5fb8d5694a36744b4f96a6161a`):** Verified: current main budget limits in `test_display_budgets.py` include 500000 B map-usable and 4500000 B all display bytes. Not verified: the old measured maxima and 1887725 B water limit. Current Douglas water display files are 1770773 B waterways and 116952 B waterbodies (1887725 B combined), so the older 954452 B figure is not current.

TD-10. Display budgets at 2026-10-08 (limits from v2/pipeline/tests/browser/test_display_budgets.py).
Browser limits: map-usable 500000 B; all display bytes 4500000 B. Douglas map-usable maximum 456170 B
(headroom 43830 B, arithmetic checked). Douglas water display 954452 B equals waterways 834148 B plus
waterbodies 120304 B (checked on disk). Other maxima (Aspen 382538 and 3541592; Douglas 2736972) and
the 1887725 limit: UNVERIFIED. Re-measure with node v2/pipeline/tests/browser/measure.mjs before use.
Source: Codex reconnaissance at commit 2795625, 2026-10-08; measured facts spot-checked by Hermes



> **Verification against origin/main (`bb85785ea98c8d5fb8d5694a36744b4f96a6161a`):** Not verified on origin/main: the M4-B implementation and its E1 tests are outside this branch and were not inspected. Preserve the block’s explicit UNVERIFIED marker; no water data or raw/staging directories were changed.

TD-4. Water identity. Water uses permanent_identifier-based stable IDs, uniqueness checks, exact
historical geometry matching and carried-forward aliases. Raw permanent-ID uniqueness was not assessable in
the tiled run because it produced no feature pages. Do not state the uniqueness as established.
Source: Codex reconnaissance at commit 2795625, 2026-10-08; measured facts spot-checked by Hermes
UNVERIFIED: E1 test numbers not re-run; belongs with the M4-B status notes in docs/research/m4-water/.

