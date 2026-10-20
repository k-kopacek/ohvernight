# Orca Development Workflow

Ohvernight uses isolated Git worktrees for agent development.

- Codex is the primary implementation agent.
- Claude Code is the architecture and independent review agent.
- Work begins from `origin/main`.
- Production changes are made on feature branches/worktrees, never directly on `main`.
- Tests required by AGENTS.md must pass before a PR is considered ready.
- Land ownership, recreation access, camping permission, closures, and provenance must never be inferred when evidence is insufficient.
- Unknown remains unknown.
- Agents must never merge to `main` autonomously. An agent may merge only
  after explicit human approval for that specific pull request and reviewed
  head SHA; if the head changes after approval, approval is required again.
- Agents must not enable auto-merge unless explicitly authorized, push
  directly to `main`, force-push, or rewrite shared history.
