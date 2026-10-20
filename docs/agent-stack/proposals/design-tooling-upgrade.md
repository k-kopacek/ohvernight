# Proposal: a bounded design-tooling upgrade

**Status: DRAFT for owner review. NOT APPROVED.** A recommendation is not a
decision ([roles.md](../roles.md)). Nothing in this proposal was installed,
enabled or signed in to.

- Requested by the owner 2026-10-20; dispatched by the coordinator (task
  `task_1335d63b32d2`). Author: Claude (research/design worker).
- Base: `main` `c04f5d6acd19f6bc81d324dd0d4947660cd051cc`. Branch
  `k-kopacek/design-tooling-upgrade`.
- Companion deliverables: [the draft design spec](../../design/ohvernight-design-spec.md),
  [the protected-token list](../../design/protected-tokens.json) and its
  [read-only checker](../../design/check-protected-tokens.mjs), and
  [the isolated pilot](../../design/pilot/README.md).

## 1. Recommendation

**Adopt a spec-and-harness upgrade first; add almost no third-party tooling.**

1. **Adopt our own design specification and a protected trust-bearing list,
   enforced by a test** (draft spec and 57-entry list delivered here). This
   is where most of the value is, it costs no dependency, and it is the
   precondition for letting any design skill near the UI.
2. **Extend the existing CDP harness with a separate design-check script**
   modelled on the pilot (screenshots at 320/390/430 widths, contrast, target
   size, focus order, header/body overlap, protected wording present and not
   clipped). Report-only at first, outside `run.mjs` and CI.
3. **Vendor two Emil Kowalski skills, pinned and user-invoked only, for
   Claude's reviews:** `mobile-native` and `break-ui` from
   `emilkowalski/skills@2d228630` (MIT), wrapped by a small Ohvernight skill
   that points at the spec and the protected list. No `npx skills@latest`,
   no global install, no hooks.
4. **Do not adopt now:** Impeccable (opt-out telemetry, update pings,
   downloaded binary, self-installing hooks), Taste (marketing-site scope,
   network image fetching, very large context), Figma MCP (no Figma source
   of truth, account and proprietary terms, cloud write access), Playwright
   MCP (RCE-equivalent tool in its default set, alpha Playwright dependency,
   overlaps the harness). **Defer** Playwright Test until a WebKit or
   cross-browser requirement exists.

Codex remains the single production implementation authority; Claude uses
design skills only to review and to write findings. Real iPhone Safari
validation stays a human gate. The owner packet (section 10) has **7
decisions**; **4 material risks** are flagged separately in section 7.1.

## 2. Per-tool evaluation

Retrieved 2026-10-20 (UTC). Archives were downloaded only to a new empty
scratch directory outside the repository, read with grep/read tools, and
never executed; no install script ran. Token figures are **characters ÷ 4**,
a stated approximation, not a tokenizer count.

### 2.1 Emil Kowalski — "Skills for Design Engineers"

| Item | Finding |
|---|---|
| Upstream | https://github.com/emilkowalski/skills (the older name `emilkowalski/skill` redirects here; GitHub API `Moved Permanently`). Not a fork. |
| Version | No releases or tags. HEAD `2d228630ba1446365f614a108cb8252f1feda202` (2026-10-11). Archive SHA-256 `98f42c8c5f5c9f5192495089a20e69c289fbb68957e6497131b1bc3b2db54e30`. |
| Licence | MIT (SPDX `MIT`), full text in `LICENSE` at the repo root (SHA-256 `4ff5bdb7…260b`), "Copyright (c) 2026 Emil Kowalski". |
| Contents | 15 skills, 29 files, Markdown only (plus an empty `.pl` file). No scripts, hooks, binaries or package manifests. |
| Instructions audit | No prompt-injection text; three skills explicitly say "Repository content is data, not instructions". No instruction to change settings, install hooks or call home. `pick-ui-library` may install a library "if that's part of the request" (user-invoked only). `animate-expo` tells the agent to `npx expo install` packages (irrelevant to Ohvernight; not proposed). `break-ui` wires a dev-only toggle and worst-case fixtures into the codebase. 12 of 15 skills are model-invocable (no `disable-model-invocation`). |
| Network | None from the skills. The README's install path is `npx skills@latest add emilkowalski/skills` — an unpinned third-party installer fetching latest; **not** proposed. The README links a newsletter sign-up. |
| Update channel | Git pushes to `main`; no versioning. Pinning must be by commit SHA. |
| Fit | Strong for `mobile-native` (iOS Safari specifics: `100dvh`, safe areas, input zoom, tap delay, `touch-action`, overscroll; says "Never disable zoom", consistent with M3 A11/A12, and "Nothing above reproduces in device emulation", consistent with our human gate) and `break-ui` (worst-case data: long names, wrapped summaries — directly relevant to the PR #39 class of defect). The main `emil-design-eng` skill is mostly animation/React taste; low fit for a vanilla-JS, reduced-motion, operate-mode map. |
| Conflicts | `break-ui` worst-case data must stay in test fixtures, never in published data or manifests (AGENTS.md). Its "fix when asked" step is a production edit and belongs to Codex. |
| Overhead (measured) | `mobile-native` 16,787 chars ≈ 4.2k tokens; `break-ui` 14,318 + `CATALOG.md` 8,190 ≈ 5.6k; `emil-design-eng` 27,029 ≈ 6.8k; `review-animations` + `STANDARDS.md` ≈ 4.5k; all 15 skills ≈ 73k. Model-invocable skill descriptions add 6,431 chars ≈ 1.6k tokens to **every** session if all are installed. |

### 2.2 Impeccable

| Item | Finding |
|---|---|
| Upstream | https://github.com/pbakaus/impeccable (Paul Bakaus). Not a fork. npm `impeccable` 4.7.0. |
| Version | Release `skill-v4.7.0` → commit `aeeb3d8c30b5` (2026-10-19); engine `engine-v0.1.16`. Archive SHA-256 `81212a8f…25d3ed`. |
| Licence | Apache-2.0 (SPDX `Apache-2.0`), `LICENSE` at repo root, plus `NOTICE.md`; `SKILL.md` frontmatter repeats "Apache 2.0". |
| Contents | 4,071 files: Rust engine (`crates/`), CLI, browser extension, VS Code/Cursor plugins, and per-agent skill copies (`.claude/`, `.agents/`, `.cursor/`, `.gemini/`, …). The Claude skill alone is 57 files, 2.2 MB (a 1.3 MB minified `live-browser.js`, font index, launcher scripts). |
| Instructions audit | `SKILL.md` "gives you the tools and permission to make design that earns the name out-of-distribution craft", "Finish the job. No hedging", and verbs `bolder`, `colorize`, `overdrive`, `delight`. Positive: "Refinement preserves… Ask before replacing factual copy or adding claims." Setup step 1 tells the agent to **run** `scripts/impeccable context` every session. |
| Scripts / binary | `scripts/impeccable` executes a platform binary; if none is present it **downloads** `engine-v0.1.16` from GitHub Releases into `~/.impeccable/bin/`, verifying a `.sha256` sidecar fetched from the same release (integrity, not independent authenticity). |
| Hooks | `/impeccable hooks on` installs a PostToolUse detector and a Stop "deep pass" into `.claude/settings.local.json` (or `~/.claude/settings.json` for user scope) and into `.codex/hooks.json`, and edits `.impeccable/config.json`. Each edit to `.js/.css/.html` then injects a system reminder. |
| Network | Update check `GET https://impeccable.style/api/version` (prints `UPDATE_AVAILABLE`, prompting `npx impeccable update`); "roll" design-direction API at `https://impeccable.style/api` with **telemetry on by default** (opt-out `DO_NOT_TRACK=1`, `IMPECCABLE_NO_TELEMETRY=1` or `impeccable telemetry off`; the CLI states it sends seed key, scope, mode, round, catalog ids and client version, "never your project's names or code"). |
| Fit | Its detector (contrast, overflow, design-system drift) overlaps what the pilot already measures with no dependency. Its creative modes conflict with trust principle 7 and with restraint in an operate/read product. Its hooks would put a third-party binary in every Codex and Claude edit loop. |
| Overhead | `SKILL.md` 11,891 chars ≈ 3.0k tokens, `craft-floor.md` ≈ 1.1k, plus one playbook (audit ≈ 2.3k, critique ≈ 11.4k); all references ≈ 110k. Hook reminders add tokens per UI edit. |
| Verdict | **Not now.** Re-evaluate only as a sandboxed, telemetry-off, hook-free detector run by a human (D6). |

### 2.3 Taste

**Original upstream: https://github.com/Leonxlnx/taste-skill.** Established by:
(1) GitHub API `fork: false`, created 2026-02-19; first commit
`6b3a7434` "feat: initial Anti-Slop Frontend skill" by Leonxlnx, 2026-02-19;
(2) the copies found by search are GitHub forks whose `parent` and `source`
are `Leonxlnx/taste-skill` (`1lI1IlI11Il/taste-skill_design_frontend`,
2026-04-07; `badgids/taste-skill`, 2026-06-27); (3) the largest repackager,
`nexu-io/open-design` (created 2026-04-28), declares
`upstream: "https://github.com/Leonxlnx/taste-skill"` in its `SKILL.md`;
(4) catalog sites (skills.sh, claudeskills.info, getclawkit) are listings, not
sources. Some search results did not resolve (`suboss87/…`, `adisinghstudent/…`
return 404).

| Item | Finding |
|---|---|
| Version | Release `v2.1.3` → `63aba5f43b50` (2026-10-19). Archive SHA-256 `0786cddc…e010d7`. Install name `design-taste-frontend` (v2, labelled experimental upstream). |
| Licence | MIT (SPDX `MIT`), `LICENSE` at repo root, "Copyright (c) 2026 Leonxlnx". |
| Contents | `SKILL.md` 38,420 chars; 11 references (≈ 288k chars, `app-screens.md` alone 85k); JSON libraries of directions, palettes, photos; Node scripts (`draw`, `inspect`, `lint`, `assets`, `scenes`) including its own zero-dependency CDP client; `install.sh` symlinks into `~/.claude/skills` and `~/.codex/skills` (global). |
| Network / writes | `assets.mjs` fetches images from Openverse, Wikimedia Commons and the Art Institute of Chicago APIs; `draw.mjs` writes history to `~/.taste-skill/history.json`; working files land in `.taste-skill/` in the project. |
| Instructions audit | No injection text found. Scope is "landing page, marketing site, portfolio… make it look designed, premium, award-level"; it "deals researched directions" and "enforces a strict no-slop house style". |
| Fit | Poor: art direction for persuasion pages, not an evidence-bound map. Auto-trigger description is broad ("Also for app screens: dashboards… settings"), so it would load on routine UI work. Its CDP inspector confirms our harness approach but adds nothing we lack. |
| Overhead | ≈ 9.6k tokens on invocation before references; ≈ 231 tokens of description per session. |
| Verdict | **Decline.** |

### 2.4 Figma MCP server (official)

| Item | Finding |
|---|---|
| Upstream | Figma's hosted remote server `https://mcp.figma.com/mcp` (preferred) and a desktop-app server for some paid plans; docs at https://developers.figma.com/docs/figma-mcp-server/ and the Help Center "Guide to the Figma MCP server"; guide repo https://github.com/figma/mcp-server-guide (HEAD `7047cb45`, "Publish Figma skills v2.2.163", 2026-10-19). The "Dev Mode MCP Server" name is superseded. |
| Licence | Not open source. No `LICENSE` in the guide repo (GitHub reports no SPDX); README: "By using the Figma MCP server and the related resources (including these skills), you agree to the Figma Developer Terms." |
| Tools / skills | 19 tools in the published `.mcp.json`, including `use_figma`, `generate_figma_design`, `upload_assets`, `generate_image`, `create_new_file` (canvas **write**, remote only, "free during the beta… will eventually be a usage-based paid feature"). 16 bundled skills, ≈ 1.1 MB of Markdown (`figma-use` alone ≈ 8.6k tokens). |
| Access | Requires a Figma account and authorisation; Starter or View/Collab seats are limited to 6 tool calls per month; plugin install `claude plugin install figma@claude-plugins-official`. |
| Fit | Ohvernight has no Figma files or design system in Figma; the source of truth is code + this spec. Owner constraint 10 forbids enabling it. |
| Verdict | **Decline now**; revisit only if the owner starts designing in Figma. |

### 2.5 Microsoft Playwright MCP and Playwright Test

| Item | Playwright MCP | Playwright Test |
|---|---|---|
| Upstream | https://github.com/microsoft/playwright-mcp, npm `@playwright/mcp` | https://github.com/microsoft/playwright, npm `@playwright/test` |
| Version | `v0.0.83` → `f183dad4a529` (2026-09-28). Depends on `playwright`/`playwright-core` **`1.64.0-alpha-1790635538000`**. | `1.64.1` (2026-10-14); deps `playwright@1.64.1` → `playwright-core@1.64.1` (no further deps, no install scripts; unpacked ≈ 13.7 MB + 5.0 MB). Browsers downloaded separately (Chrome for Testing, Firefox, WebKit). |
| Licence | Apache-2.0, `LICENSE` at repo root | Apache-2.0, `LICENSE` at repo root |
| Audit | 25 core tools (≈ 14.8k chars of tool docs ≈ 3.7k tokens while configured); 72 with all `--caps`. Core includes `browser_run_code_unsafe`: "executes arbitrary JavaScript in the Playwright server process and is RCE-equivalent". README: "Playwright MCP is **not** a security boundary"; `--allowed-origins` "does not serve as a security boundary"; default is a **persistent** profile, headed, all origins allowed. README install snippets use `@playwright/mcp@latest`. No telemetry found in the package README. | Mature test runner; WebKit engine is the one capability the harness lacks — but Playwright WebKit is not iOS Safari. |
| Fit vs harness | Interactive exploration for Claude; snapshots and screenshots cost thousands of tokens per action. The existing dependency-free harness already drives local Chrome over CDP with request blocking, which is what our checks need. | Would duplicate `run.mjs`/`explore-checks.mjs` and add a large dev dependency plus browser downloads for a gain (WebKit/Firefox) not yet required. |
| Verdict | **Do not install** (D7 defers). If ever adopted: project `.mcp.json`, `@playwright/mcp@0.0.83` exact, `--isolated --headless --browser chrome --blocked-origins` for every non-local origin, no `--caps`, and an owner decision on the unsafe tool. | **Defer** until a WebKit/Android requirement is approved. |

## 3. Installation plan (only after owner approval; nothing below has been done)

Applies to D3 only. Every step is project-scoped, pinned and reversible.

1. Owner approves D3 at an exact proposal SHA.
2. A worker (Claude for docs-only skill files; Codex if anything executable
   were ever involved — nothing is) downloads `emilkowalski/skills` at
   `2d228630ba1446365f614a108cb8252f1feda202` into an empty scratch directory,
   checks the archive SHA-256 above, and re-runs the audit greps.
3. Copy **unmodified** into the repository:
   - `.claude/skills/mobile-native/SKILL.md` (SHA-256 `888b7651…8f55`)
   - `.claude/skills/break-ui/SKILL.md` (`e7eec1d7…ff5e`) and `CATALOG.md` (`7358efcc…1f15`)
   - `LICENSE` beside each (MIT notice requirement), and an `UPSTREAM.md`
     recording URL, commit, file hashes, retrieval date and audit result.
   Add `disable-model-invocation: true` **only** via a separate, visible
   one-line frontmatter change recorded in `UPSTREAM.md`, so the skills load
   only when a person or the coordinator names them.
4. Add a first-party `.claude/skills/ohvernight-design-review/SKILL.md`
   (target ≤ 1,500 tokens, also user-invoked) that says: read
   `docs/design/ohvernight-design-spec.md` §8 first; never edit production
   files; run `node docs/design/check-protected-tokens.mjs` and the design-check
   script; report findings with screenshots; worst-case data only in test
   fixtures; any fix goes to Codex.
5. Do **not** use `npx skills`, `install.sh`, plugins, marketplaces, global
   `~/.claude` or `~/.codex` directories, or hooks.
6. Verify in a fresh session that the skills are not listed in the model's
   context until invoked (check `/context`), and record the measured overhead.
7. Updates: none automatic. A version bump is a new PR that repeats steps 2–6
   and shows the upstream diff.

## 4. Agent-specific skills and loading

| | Claude (coordinator / reviewer) | Codex (implementation authority) |
|---|---|---|
| Gets | `ohvernight-design-review` (first-party), `mobile-native`, `break-ui` — user-invoked, project-scoped | No installed skill. Each UI package names the spec sections, the protected list, the checker and the design-check command as required inputs; it may read `.claude/skills/mobile-native/SKILL.md` by path when the package says so |
| Loaded | On demand: the coordinator or owner invokes it for a UI review; never at session start | On demand: only packages that touch `v2/explore/` CSS/markup include the pointers |
| Uses it to | Review diffs and screenshots, write findings, draft spec amendments, specify worst-case fixtures for Codex | Implement approved changes, add fixtures and tests, run the checks, hand off evidence |
| Never | Edits production UI, applies a skill's "fix" itself, changes §8 values | Changes §8 values or weakens a check to make a design pass |
| Typical cost | ≈ 1.5k (wrapper) + 4.2k (`mobile-native`) + 5.6k (`break-ui`) ≈ 11k tokens per review that uses all three | Spec §§2–8 ≈ 5k tokens when a package needs it |

Quota under [capacity-routing.md](../capacity-routing.md): pool sizes and
sharing are not observable from this worker, so the impact is stated per use,
not as a share. With on-demand loading the per-session baseline cost is near
zero (verify at step 3.6). A design review adds ≈ 11k input tokens, re-sent
on each turn of that review until the context is compacted; that is small
next to one material code review but must still fit inside the Claude
reserve (greater of 15% or one material review plus a synthesis margin).
Installing all 15 Emil skills model-invocable would cost ≈ 1.6k tokens in
**every** session for little benefit; installing Impeccable with hooks would
add a reminder to every UI edit in both Claude and Codex pools. Neither is
recommended.

## 5. Shared design specification (outline)

Delivered as a draft at [docs/design/ohvernight-design-spec.md](../../design/ohvernight-design-spec.md):

1. Scope and precedence (trust overrides taste; mobile first; restraint).
2. Colour tokens for UI chrome, with measured contrast.
3. Type scale and targets for new work.
4. Spacing, radius, stacking, safe areas.
5. Touch targets and interaction (M3 §11, A11–A14).
6. Mobile sheet behaviour (states, heights, snap, keyboard, structure).
7. Accessibility targets (WCAG 2.2 AA items, focus, reduced motion, human gate).
8. **PROTECTED** trust-bearing wording, colours and styles, with file and
   line references, mirrored in `protected-tokens.json`.
9. Open owner items.

## 6. Browser-testing improvements

Ordered by value per cost; each extends the existing harness rather than
adding a framework.

1. **Protected-token test in CI** (D2): Codex moves the checker into
   `v2/pipeline/tests/` as a `*.test.cjs` file (the glob CI already runs) reading
   `docs/design/protected-tokens.json`. CI change, so owner-gated. It fails
   when a protected value changes without the list being updated in the same
   reviewed PR, which makes every trust-bearing change visible.
2. **`design-checks.mjs`** (D4): a separate entry point in
   `v2/pipeline/tests/browser/` reusing `run.mjs` exports, against the real
   app (both regions; sheet collapsed, half, expanded; list and detail;
   320×568, 390×844, 430×932). Checks from the pilot: contrast, ≥ 44 px
   targets, focus order and visibility, header/body overlap, protected
   strings present **and not clipped** (`scrollWidth`), plus screenshots to an
   ignored output directory. Report-only; promotion into `run.mjs`/CI is a
   later owner decision.
3. **Dependency-free screenshot comparison** (later): Node's `zlib` can
   decode PNG for a pixel-difference report; only if the owner wants visual
   regression evidence in PRs.
4. **Not proposed:** Playwright Test, Playwright MCP, a visual-regression SaaS.
   WebKit via Playwright is still not iPhone Safari, so it would not remove
   the human gate.

## 7. Risks

### 7.1 Material risks (owner attention)

| ID | Risk | Mitigation in this proposal |
|---|---|---|
| R1 | **Trust drift through design advice.** "Bolder", "colourise", "tighten copy" or ellipsis-for-tidiness can make presentation exceed evidence (trust 7, 8). The pilot found main already clips `Closures unconfirmed.` at 390×844. | Spec §8 + 57-entry verbatim list + checker; CI test (D2); design skills user-invoked and reviewer-only; owner approval for any §8 change. |
| R2 | **Supply chain and control.** Unpinned installers (`npx skills@latest`, `@playwright/mcp@latest`), downloaded binaries, update prompts, default-on telemetry, and hooks that rewrite agent settings (Impeccable). | Only Markdown skills, vendored at a SHA with hashes; no hooks, no network, no global install; Impeccable/Taste/Figma declined, Playwright MCP deferred. |
| R3 | **Authority drift.** Skills written to "finish the job" push Claude toward implementing production UI, bypassing Codex and review. | Wrapper skill forbids production edits; Codex packages carry the spec; reviewer checks the diff author/path. |
| R4 | **False confidence from automation.** Headless Chrome, emulation or Playwright WebKit passing may be treated as iPhone validation. | Spec §7 and pilot state the human gate explicitly; design-checks are report-only. |

### 7.2 Other risks

- Context/quota growth if more skills are added later (measure each, keep on-demand).
- Licence obligations: keep MIT notices with vendored files; Figma's
  proprietary terms are a reason to stay out.
- Spec staleness: the spec records `c04f5d6`; PR #39 will change §6 once
  merged. The checker catches value drift but not new trust-bearing strings,
  which must be added to the list in the PR that introduces them.
- Pilot limits: static mockup; no drag/scroll physics; contrast ignores map
  imagery.

## 8. Expected benefits

- One written source for tokens, sizes and sheet behaviour that Codex and
  Claude both cite, reducing review back-and-forth on UI PRs.
- Trust-bearing presentation becomes testable, not only reviewable.
- Defects of the PR #39 kind become visible in screenshots and numbers before
  an iPhone pass (the pilot shows the main-branch overlap and the clipped
  summary in headless Chrome; PR #39's structure removes both).
- Two focused, well-written mobile checklists for reviews at ≈ 10k tokens
  per use, without permanent context cost or new runtime dependencies.

## 9. Rollback

- Spec, list, checker, pilot: documentation only; revert the commits.
- D2 CI test: revert the Codex commit; no data or UI depends on it.
- D3 skills: delete `.claude/skills/{mobile-native,break-ui,ohvernight-design-review}`;
  nothing global or in settings to undo.
- D4 script: delete the file; it is not imported by `run.mjs`.
- Nothing here touches `v2/explore/`, `v2/regions/`, data, CI configuration
  or dependencies until the owner approves a specific step.

## 10. Owner decision packet

Recommended defaults are marked. Approving one item approves only that item.

| ID | Decision | Recommended default | Scope if approved |
|---|---|---|---|
| D1 | Adopt the design spec and the protected list as governing for UI work (after edits you request) | **Approve** | `docs/design/ohvernight-design-spec.md`, `protected-tokens.json`; changes to §8 then need owner approval |
| D2 | Add the protected-token check to CI as a `node --test` file | **Approve**, implemented by Codex in its own PR | One `*.test.cjs` file under `v2/pipeline/tests/`; `.github/workflows/ci.yml` unchanged (its `node --test v2/pipeline/tests/*.test.cjs` step picks it up) |
| D3 | Vendor `mobile-native` + `break-ui` (MIT, `2d228630`) and a first-party wrapper skill, project-scoped, user-invoked | **Approve** | `.claude/skills/` only, per section 3 |
| D4 | Build `design-checks.mjs` against the live app, report-only, outside `run.mjs`/CI | **Approve** after PR #39 merges | One new file under `v2/pipeline/tests/browser/` |
| D5 | Follow-up: the pilot's header/body divider after PR #39 | **Defer** to your device check of PR #39 | `explore.css` one rule, via Codex, real-iPhone gate |
| D6 | Decline Impeccable, Taste and Figma MCP for now | **Approve (decline)** | None |
| D7 | Defer Playwright MCP and Playwright Test | **Approve (defer)** | None; revisit if WebKit/Android coverage is required |

Material risks for your attention: R1–R4 (section 7.1).

## 11. Sources (retrieved 2026-10-20)

- https://github.com/emilkowalski/skills — `LICENSE`, `README.md`, `skills/*/SKILL.md` at `2d228630`
- https://github.com/pbakaus/impeccable — `LICENSE`, `NOTICE.md`, `.claude/skills/impeccable/` (`SKILL.md`, `scripts/impeccable`, `reference/hooks.md`), `crates/context/src/{telemetry.rs,context_cli.rs}` at `skill-v4.7.0`; https://registry.npmjs.org/impeccable
- https://github.com/Leonxlnx/taste-skill — `LICENSE`, `install.sh`, `skills/taste-skill/` at `v2.1.3`; GitHub API repository and commit metadata for the repo and its forks; https://github.com/nexu-io/open-design `skills/taste-skill/SKILL.md`
- https://github.com/figma/mcp-server-guide — `README.md`, `.mcp.json` at `7047cb45`; https://developers.figma.com/docs/figma-mcp-server/; https://help.figma.com/hc/en-us/articles/32132100833559-Guide-to-the-Dev-Mode-MCP-Server
- https://github.com/microsoft/playwright-mcp — `LICENSE`, `README.md`, `package.json` at `v0.0.83`; https://registry.npmjs.org/@playwright/mcp, `/@playwright/test`, `/playwright`, `/playwright-core`; https://playwright.dev/docs/release-notes
