# Ohvernight design specification

**Status: DRAFT, NOT APPROVED.** Written 2026-10-20 for the design-tooling
proposal ([../agent-stack/proposals/design-tooling-upgrade.md](../agent-stack/proposals/design-tooling-upgrade.md)).
It records the current Explore design as built at main `c04f5d6` and sets
targets for new work. It changes no production file and approves nothing. If
it disagrees with an approved spec, the approved spec governs; the order is
[trust-principles.md](../product/trust-principles.md) →
`v2/pipeline/docs/data-contract.md` → M3/M4 specs and owner amendments → this
document.

Every agent and design skill reads this file, and section 8 in particular,
before proposing or making a UI change. Values marked **current** are measured
from the code; values marked **target** apply to new work only and do not
require changing existing UI.

## 1. Scope and precedence

- Covers the shared Explore shell (`v2/explore/`), its regions' presentation
  config, and any future surface built on it. The original root site is out
  of scope.
- **Trust overrides taste.** No design heuristic from any skill (Emil
  Kowalski, Impeccable, Taste or otherwise) can change a protected value
  (section 8). A design skill's advice to "bolden", "colourise", shorten copy,
  add emphasis or rank results is advisory and is rejected where it would
  communicate more certainty than the evidence supports (trust principle 7).
- **Mobile first, field use.** Phone portrait at 390×844 and 320×568 is the
  primary design case; 430×932 is checked as a large phone. Tablet 768×1024
  and desktop 1440×900 follow M3 section 11.
- **Restraint.** Ohvernight is an "operate/read" surface: precision and
  legibility beat visual novelty. No gradient text, glow, decorative motion,
  hero imagery or new display fonts.

## 2. Colour tokens (UI chrome, not map semantics)

Current values from `v2/explore/explore.css`. These are UI chrome tokens. Map
and evidence colours are **protected** (section 8) and are not tokens that a
theme may restyle.

| Token | Current value | Use |
|---|---|---|
| `--ink` | `#24271f` | body text, headings |
| `--muted` | `#666c60` | secondary text (summary, layer descriptions, result meta) |
| `--line` | `#e2e4dc` | borders, dividers |
| `--paper` | `#fafbf6` | sheet, drawer, dialog and control backgrounds |
| map backdrop | `#343e30` | `.explore-map` before tiles load or when tiles are blocked |
| landing backdrop | `#20241e` | `.explore-landing` |
| pressed / selected control | `#d5f780` | `aria-pressed=true` tool and filter buttons |
| accent / focus | `#567824` | focus ring (`3px solid`, offset 2px), checkbox accent |
| handle | `#b8bdb1` | sheet and drawer grab handle |
| dialog backdrop | `#17201099` | `::backdrop` |
| map label | `#fafbf6de` on `#24271f` text | Leaflet label tooltips |

Measured contrast (WCAG 2.x relative luminance; pilot and token
arithmetic): `--ink` on `--paper` 14.58:1; `--muted` on `--paper` 5.21:1;
pressed `#d5f780` behind `--ink` 12.6:1; focus `#567824` on `--paper` 4.92:1
but **2.19:1 where the offset ring falls on the map backdrop `#343e30`**
(observation for the owner; below the 3:1 non-text target, not changed here);
`--line` on `--paper` 1.23:1 (decorative dividers only, never the sole cue
for a control or state). **Target:** text ≥ 4.5:1, large text
(≥ 24px, or ≥ 18.66px bold) ≥ 3:1, non-text UI boundaries and focus
indicators ≥ 3:1 against adjacent colours (WCAG 2.2 AA 1.4.3, 1.4.11). Text
over the map always sits on an opaque or near-opaque `--paper` surface or has
a text shadow (the region name).

A new UI colour is added only as a token here, with its contrast measured,
and never reuses a hue in a way that could be read as a map or evidence
meaning (for example green for "open" or red for "closed").

## 3. Type scale

Current: one family, `system-ui, sans-serif`; base `15px/1.5`.

| Role | Current size | Notes |
|---|---|---|
| landing title | 36px | `.explore-landing-card h1` |
| h1 (panel titles) | 22px | line-height 1.25 |
| h2 (detail title) | 18px | wraps; never truncated |
| h3 | 16px | |
| body | 15px | |
| secondary | 12px | layer descriptions, result meta, banner, map-control labels |
| summary | 11px | `.explore-summary` (sheet header) |
| map label | 11px/1.3 | |
| attribution | 9px | Leaflet attribution; exempt as a source credit link |

**Targets for new work:** no new text below 12px except attribution; form
inputs at 16px or larger where an iOS input-zoom would otherwise occur (the
current controls inherit 15px; any change is an owner-approved item, not a
silent fix, because M3 forbids a viewport restriction and the zoom behaviour
must be re-checked on a real iPhone). Trust-bearing text is never
truncated with an ellipsis where the truncation could hide a qualifier
(pilot finding: `Closures unconfirmed.` is clipped at 390×844 on main).

## 4. Spacing, radius, elevation

- Spacing steps in use: 2, 4, 5, 6, 8, 10, 12, 20 px. **Target:** new work uses
  4, 8, 12, 16, 20 and avoids new one-off values.
- Radii: 8px controls; 12px side panels (≥ 768px and short landscape); 16px
  phone sheet/drawer top corners and dialog.
- Stacking (`z-index`): map 0; top bar, map controls, sheet 500; banner 501;
  drawer 600; landing 800; selected pin 900. New layers fit this ladder.
- Safe areas: every edge uses `env(safe-area-inset-*)` through the
  `--safe-*` variables (M3 A12 item 9). Heights use the visible viewport
  (`--viewport-height`, `visualViewport`), not `100vh`.

## 5. Touch targets and interaction

- Every interactive control is at least **44×44 CSS px** (M3 section 11).
  Exceptions: links inside a sentence, and map attribution links. Map pins
  render a 28px badge inside a 44px hit area.
- `touch-action: manipulation` on controls; no global viewport zoom
  restriction (M3 A11 item 9, A12 item 8).
- Feature selection follows the M3 A14 contract (empty tap keeps selection
  and camera; line fit; point centre; generalized polygon preserves camera).
- Selection never relies on colour alone (M3 A13).

## 6. Mobile sheet behaviour

Current, from `v2/explore/sheet.js`, `explore.css` and M3 A11–A14.

| Property | Phone portrait | ≥ 768px | Short landscape (≤ 500px tall) |
|---|---|---|---|
| States | collapsed / half / expanded | collapsed / expanded side panel | collapsed / expanded side panel |
| Collapsed height | 64px (M3 limit ≤ 96 at 390×844, ≤ 88 at 320×568) | 64px | 64px, width ≤ 200px or 40vw |
| Half | 40% of usable height | n/a | n/a |
| Expanded | 75% of usable height; collapse control stays visible | width 340px, 75% height | width ≤ 320px or 40vw |
| Drag | follows the finger from the header; from the body only when the body is at scroll top | touch only | disabled |
| Snap | nearest state, or a flick (> 0.45 px/ms, less than half the range) moves one state | | |
| Tap slop on header | 4px (PR #39 proposes 10px for touch on the header) | | |
| Keyboard | toggle cycles states with Enter/Space; Escape collapses and returns focus to the toggle | | |
| Collapsed body | `inert` | | |
| Motion | height transition .15s; none under `prefers-reduced-motion` | | |

Structure (target, as proposed by PR #39 and supported by the pilot): one
normal-flow header containing the grab handle/toggle, the summary (wraps,
never ellipsised) and, in detail view, Back + title; below it **one**
scrolling body. No header child uses sticky positioning or a computed top.
Back never starts a drag. A visible boundary separates the header from the
scrolling body (pilot `proposal` variant; not approved). The layer drawer and
the sheet are mutually exclusive on phones; ≥ 45% of the map stays visible
with the drawer open.

## 7. Accessibility targets

- WCAG 2.2 AA for text contrast, non-text contrast, focus visible (2.4.7),
  focus not obscured (2.4.11), target size (2.5.8, met by the stricter 44px
  rule), reflow at 320px (1.4.10, no horizontal scroll), orientation (1.3.4)
  and reduced motion.
- Tab order follows visual order; Escape closes the top overlay and returns
  focus to its opener (M3 section 11).
- Status changes use `role="status"` (summary, banner).
- Automated checks run in headless Chrome through the existing CDP harness;
  **real iPhone Safari validation remains a human gate** wherever an approved
  spec or the owner requires it today. Headless Chrome, Playwright WebKit and
  device emulation are not substitutes.

## 8. PROTECTED — trust-bearing colours, styles and wording

No design work, skill, agent or automated fix may change these without
explicit owner approval recorded in the repository. They are copied verbatim,
with their source file, into [protected-tokens.json](protected-tokens.json)
(57 entries at `c04f5d6`), and
`node docs/design/check-protected-tokens.mjs` fails if any value is no longer
present byte-for-byte in its file. That checker is a draft outside CI; see the
proposal for the owner-gated CI step.

### 8.1 Land wording (M3 13.1, D12) — `v2/explore/land-style.js` lines 4–17

| ID | Exact text |
|---|---|
| W1 | `Generalized land management context — not parcels` |
| W2 | `Broad areas drawn at limited scale from a national agency dataset. They show which agency the source lists as managing an area. They are not property lines and do not show who owns a specific spot.` |
| W3 | `Ownership or management does not establish public access. This map does not show whether you may enter, cross, park or stay.` |
| W4 | `PVT — the source's generalized private class; not a parcel-level finding` |
| W5 | `Unshaded land is unknown — not private, not public, not open` |
| W6 | `<code> — unrecognised source code; unknown` |
| W7 | `Limited-scale boundary. It cannot locate a property line or tell you whether a specific spot is inside this area.` |
| W8 | `USFS — Forest Service; generalized source class` · `BLM — Bureau of Land Management; generalized source class` · `OTHFE — Other Federal; generalized source class` · `ST — State; generalized source class` · `LG — Local; generalized source class` |
| W9 | `<layer title> — boundary as published by <agency>` |
| W10 | `Computer-screened research areas — not campsites` |
| W11 | `Source classification: <code>` |

### 8.2 Map colours and styles

| What | Exact value | File |
|---|---|---|
| Tier-G class tints (USFS, BLM, OTHFE, ST, LG, PVT) | `['#8f9f89','#8d9da7','#a59e88','#a49ba9','#91a6a0','#9ea3a6']` | `v2/explore/land-style.js:18`, order at `:20` |
| Unrecognised-code tint | `#b8b9b6` | `land-style.js:21` |
| Trail colour | `TRAIL_COLOR='#d06030'` | `land-style.js:19` (M3 A14) |
| Water / roads and other lines | `#73c5dc` / `#b1a58a`; weights 1.5 / 2.25; opacity .85 | `land-style.js:36` |
| Tier G | fill .12; dashed `5 5`, weight 1, opacity .5; **no outline at zoom ≥ 14** | `land-style.js:33` |
| Tier C | fill .10, dashed `7 5` | `land-style.js:34` |
| Tier P | fill .12, solid weight 1.3, opacity .6 | `land-style.js:35` |
| Selected line casing | halo `#f8f8f2` (+4px), edge `#202124` (+6px) | `v2/explore/map-adapter.js:213–215` (M3 A13) |
| Selected line / other lines | width +3 (≥ 5), opacity 1 / width −.75 (≥ 1.5), opacity ×.5 (≥ .4) | `map-adapter.js:235` (A13, A14) |
| Selected polygon / neighbours | fill tier +.10 (≤ .25), no outline / fill ≤ .04 | `map-adapter.js:235` (A14) |
| Research boundary outline | `{color:'#fff',weight:1,opacity:.5,dashArray:'6 5',fill:false}` | `v2/explore/shell.js:210` |
| Fallback land style | `{color:'#91a184',weight:1,opacity:.5,fillOpacity:.1}` | `shell.js:128` |

Rules carried from M3 13.2: no tier-A styling exists; no class uses red or a
warning/clearance style; tints distinguish, never rank; no per-region
colours; context polygons never out-weigh roads or trails; generalized
geometry is never drawn as a crisp or parcel-like boundary.

### 8.3 Evidence and status wording

From `v2/explore/evidence.js` (lines 10–67): `Fetched ` /
`Source fetched `, ` · older than the refresh policy; refresh needed`,
`No retrieval status is recorded for this layer`, `latest fetch failed`,
`Source unavailable`, `Last retrieval attempt `, `View source ↗`,
`Only the portion inside our research boundary is shown. Check current agency notices before travel.`,
`Published activity dates`,
`These are source records, not a check for your trip dates. Blank records mean unknown.`,
`Managed use` / `Accepted use` / `Discouraged` / `Restricted`,
`Unknown — no published use record`, `Published uses: `,
`Current road conditions and vehicle suitability are unconfirmed.`,
`Published vehicle seasons`, `Dates not provided`,
`No campsite or camping permission has been confirmed. Screening snapshot: `,
`This is not an assessment of your selected trip.`

Other UI: `Turn layers on or off. Colors explain what the map can tell you; they do not prove a place is legal to camp.`
and `All layers start on. Dates and vehicle choices do not hide map features. Tap a road or shaded area to learn more.`
(`v2/explore/shell.js:29`); the results summary tail `Closures unconfirmed.`
(`v2/explore/browse.js:43`); ` trip conflicts` and `Listings could not load`
(`v2/explore/capabilities.js:81`); `Wildlife closures and special orders are not fully verified for this trip.`
(`v2/trust.js:48`); the Douglas coverage note and Rampart restrictions
(`v2/regions/douglas-co/extras.js:3–4`).

### 8.4 Protected by reference

- Every string in `v2/pipeline/tests/fixtures/legacy-negated-wording.json`
  (M3 A4; 11 strings).
- Manifest text rendered verbatim: `coverage.statement`,
  `fact_coverage.*.statement`, `known_gaps[]` and `layers[].limitations` in
  `v2/regions/*/region.json`. These change only through the pipeline and the
  owner (trust principle 8).
- Ordering and presence rules: legend order and W5 always last (M3 13.2
  rule 4); land detail order (13.2 rule 6); unknown, restriction and
  not-checked states stay with the result (product principle 14).

### 8.5 What design work may change

Within section 2–7 tokens and without touching section 8: spacing, radii,
dividers, layout structure, chrome colours (with contrast re-measured), type
size of non-trust UI text, and motion within reduced-motion rules. Any change
that alters how a protected string is visible (truncation, collapse behind a
disclosure, smaller size or lower contrast than its neighbours, reordering)
counts as a change to the protected item and needs owner approval.

## 9. Open items (owner)

- Whether to adopt this spec, and the protected list, as governing (proposal
  decision D1).
- Summary size 11px vs a 12px target; any change needs a real-device check.
- Whether to adopt the pilot's header/body divider after PR #39.
- Focus ring contrast over the dark map backdrop (2.19:1) on the map controls.
