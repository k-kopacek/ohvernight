# Ohvernight agent guide

## Repository map

- `v2/` is the current Ohvernight v2 static web application.
- `v2/pipeline/` is the separate research-data pipeline. It produces an
  untracked staging bundle at `data/processed/map-data-v2.json`; after
  validation, copy/promote it to the canonical app-facing
  `v2/map-data-v2.json`. It does not deploy or modify the website automatically.
- `v2/explore/` contains the shared mobile-first Explore shell, region loader,
  renderer adapter, evidence presentation and capability modules. Only
  `map-adapter.js` uses Leaflet directly.
- `v2/regions/` contains each region's manifest, presentation configuration,
  generated display artifacts, canonical regional data and README. Douglas
  `extras.js` holds the preserved region-specific listing and coverage note;
  its old entry page forwards to the shared shell.
- Each region has `v2/regions/<id>/region.json`, validated against
  `v2/pipeline/docs/data-contract.md`.
- The repository root retains the original site for comparison. Do not
  silently replace it while working on v2.
- GitHub Pages publishes the whole repository from `main`; merging to `main` is
  a production deploy.

## Institutional memory

The repository is the source of truth for project context. Agent memory, chat
history and Orca session state are not authoritative. Read these before
planning milestone work:

- `ROADMAP.md` — canonical milestone roadmap.
- `docs/specs/` — approved milestone specifications.
- `docs/product/trust-principles.md` and `docs/product/product-principles.md`.
- `docs/architecture/agent-stack.md` — roles, workflow, escalation and merge
  authority.
- `docs/architecture/system-overview.md` and `docs/architecture/decisions/`.
- `docs/audits/architecture-audit.md` — findings behind M1, M2 and later
  milestones.

## Working rules

- Never merge to `main` autonomously. An agent may merge only after explicit
  human approval for that specific pull request and reviewed head SHA. If the
  pull request's head changes after approval, approval is required again. Do
  not enable auto-merge unless explicitly authorized, and never push directly
  to `main`.
- Treat `origin/main` as the shared history. Never force-push, rewrite history,
  or delete files to resolve a conflict without explicit user approval.
- Use a short-lived feature branch or isolated worktree for changes. Inspect
  `git status`, the staged diff, and the relevant tests before committing.
- Preserve source attribution and the limitations documented in
  `DATA-LICENSE.md` and the pipeline documentation. Map layers are research
  context, not legal access or availability guarantees.
- Keep credentials out of source and data. `RIDB_API_KEY` belongs in the
  environment or a GitHub Actions secret, never in a committed file.
- Do not add raw personal contact details, scraped third-party content, or
  machine-generated caches to published data.
- Treat `v2/map-data-v2.json` as the app-facing public bundle. Pipeline raw
  inputs and staging output are ignored by design; update the ignore rules
  deliberately if a new public artifact is required.

## Verification

From the repository root, with Python 3.12+ and Node 22:

```sh
python3 -m venv v2/pipeline/.venv
v2/pipeline/.venv/bin/pip install -r v2/pipeline/requirements.txt
v2/pipeline/.venv/bin/python v2/pipeline/scripts/00_selftest.py
node --test v2/pipeline/tests/*.test.cjs
node v2/pipeline/tests/browser/run.mjs
```

CI runs the offline Python, Node and `browser` checks on every pull request;
a PR must be green before merge. The browser harness needs local Chrome and
blocks non-local requests. Performance comparisons are reported separately
with `node v2/pipeline/tests/browser/measure.mjs`; real-device checks remain
a human gate.

The pipeline's live refresh commands contact external sources and may require
`RIDB_API_KEY`; do not run them as part of ordinary code review. Read the
pipeline README and source verification notes before changing data contracts,
access rules, or publication behavior.

## Agent handoff

Every handoff should state what changed, what was intentionally left alone,
which checks ran, and any remaining uncertainty. Keep app, pipeline, and data
changes separate when practical so each commit is easy to review or revert.
