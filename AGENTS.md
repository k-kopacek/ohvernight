# Ohvernight agent guide

## Repository map

- `v2/` is the current Ohvernight v2 static web application.
- `v2/pipeline/` is the separate research-data pipeline. It produces an
  untracked staging bundle at `data/processed/map-data-v2.json`; after
  validation, copy/promote it to the canonical app-facing
  `v2/map-data-v2.json`. It does not deploy or modify the website automatically.
- `v2/regions/` contains region-specific field-test experiences. Keep a
  region's app, styles, research data, and README together.
- Each region has `v2/regions/<id>/region.json`, validated against
  `v2/pipeline/docs/data-contract.md`.
- The repository root retains the original site for comparison. Do not
  silently replace it while working on v2.
- GitHub Pages publishes the whole repository from `main`; merging to `main` is
  a production deploy.

## Working rules

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
```

CI runs the same commands on every pull request; a PR must be green before merge.

The pipeline's live refresh commands contact external sources and may require
`RIDB_API_KEY`; do not run them as part of ordinary code review. Read the
pipeline README and source verification notes before changing data contracts,
access rules, or publication behavior.

## Agent handoff

Every handoff should state what changed, what was intentionally left alone,
which checks ran, and any remaining uncertainty. Keep app, pipeline, and data
changes separate when practical so each commit is easy to review or revert.
