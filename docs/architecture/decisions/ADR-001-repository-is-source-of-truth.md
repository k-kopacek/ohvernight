# ADR-001: The GitHub repository is the institutional source of truth

## Status

Accepted. Recorded 2026-10-04.

## Context

Ohvernight is built by a human owner working with several agents across many
chats and Orca sessions. Roadmap, trust rules, role definitions and audit
findings had been living in chat transcripts and agent memory. Those are lost
or drift when a session ends, and the original architecture audit was already
lost that way.

## Decision

The GitHub repository is the durable source of truth for code, data,
specifications, the roadmap, product and trust principles, the agent
architecture and major technical decisions. Agent memory, chat history and
Orca session state are conveniences, not authority.

## Consequences

- When memory or a chat disagrees with the repository, the repository is
  right.
- Anything that must outlive a session is written to the repository through a
  pull request.
- Agents read `AGENTS.md`, `ROADMAP.md`, the relevant specification and the
  documents under `docs/` before planning work, and do not rely on recall.
- Changing the roadmap, a principle or a decision means changing a file, with
  review and human approval.
- Documentation has to be maintained; a stale document is a defect.
