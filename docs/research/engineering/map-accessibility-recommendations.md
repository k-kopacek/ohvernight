DRAFT - UNREVIEWED

# Map accessibility design recommendations

Date: 2026-10-07. Status: recommendations only. No production file was changed and nothing here is decided. The owner decides every item marked "owner decision".

Application read (read only): `m4a-source-preservation/v2/explore/` (commit tree as found; `shell.js`, `map-adapter.js`, `land-style.js`, `explore.css`, `sheet.js`, `drawer.js`, `browse.js`, `capabilities.js`, `evidence.js`), `v2/regions/*/explore.json` and `region.json`, `docs/specs/M3-unified-mobile-explore.md` (with A11 to A14) and `docs/specs/M4-functional-recreational-water.md`, and `v2/pipeline/tests/browser/`. Standards and competitor material comes from `hermes/a17-map-accessibility.md`, which is HERMES-SOURCED and unverified; its URLs are carried through where a criterion is cited. Measurements come from throwaway scripts in `/Users/kylekopacek/.claude/jobs/1af2c3f1/tmp/a11y/` (`measure.cjs`, `ui.cjs`; the first imports the real `land-style.js` so the style values are what the app computes). The browser harness was not started and no network was used.

Evidence tags: **READ IN FILE** (measured or read in code, with file:line), **HERMES-SOURCED**, **INFERENCE**, **UNKNOWN** (needs a real device or screen reader).

File:line shorthand: `shell` = `v2/explore/shell.js`, `adapter` = `v2/explore/map-adapter.js`, `land` = `v2/explore/land-style.js`, `css` = `v2/explore/explore.css`, `sheet` = `v2/explore/sheet.js`, `spec3` = M3 spec, `spec4` = M4 spec.

## Assumed colours (read this before the contrast numbers)

The basemap is USGS imagery (default, "Satellite") or USGS Topo (`adapter:285-291`). Imagery has no single colour, so every ratio below is against a stated representative colour. These are assumptions, not samples of real tiles (UNKNOWN until sampled on a device):

| Code | Colour | Stands for |
|---|---|---|
| D1 | `#343e30` | `.explore-map` background (`css:6`, READ IN FILE value); also dark conifer imagery |
| D2 | `#1f2a1c` | shaded canopy, north-facing slope |
| M1 | `#7a7f5a` | sunlit dry hillside or meadow imagery |
| M2 | `#c8c4b8` | pale rock, gravel, early snow |
| L1 | `#f2efe9` | Topo paper |
| L2 | `#cfe0b8` | Topo forest tint |

Strokes are blended at their real opacity over the basemap, and over each land fill at its real 0.12 opacity, before the ratio is computed. Panel colours are the CSS values: ink `#24271f`, paper `#fafbf6`, muted `#666c60` (`css:1`).

## Summary: the five most valuable changes

1. **Give every selectable thing a non-map route.** Trails, camping, trailheads and (under M4) water have a list or search route (`browse.js:7`, `capabilities.js`, `spec4` "Search: water names are added"). Roads, generalized land, wilderness and the Aspen research areas (51 polygons) are reachable only by tapping the map; none of the code read offers a list route for them (READ IN FILE by reading `shell.js` `renderResults`/`renderSearch`, `browse.js`, `capabilities.js`). Add a "Map features here" list that opens the same detail. This is the single largest gap for screen-reader, switch and low-dexterity users, and it also fixes mis-taps. Touches no approved wording.
2. **Name things properly for assistive technology.** Pins are `role=button` with the visible bullet or number as content, so the content (a bullet) will usually win over the `title` as the accessible name; the map `div` has `aria-label` but no role; selecting a feature moves focus to a "Back" button, not to the feature title. Three small markup changes. Needs a real screen reader to confirm (UNKNOWN), but the code pattern is the known failure.
3. **Stop relying on colour for layer identity.** Roads and trails differ only by colour (same solid 2.25 px, 0.85 opacity). In Aspen, streams, lakes and wilderness share one style exactly. All Douglas recreation pins render as the same bullet. Add one non-colour channel per category (dash, casing, glyph). Needs owner decision (A14 says no new colour meaning; this adds shape, not colour).
4. **Make controls and focus visible on imagery.** The focus ring (`#567824`) is 2.19:1 on D1 and 1.22:1 on M1; control borders are 1.23:1 against paper; the Satellite/Topo pressed state is a 1.16:1 background change. Replace with a two-tone focus ring and a non-colour pressed cue. CSS only; no behaviour change.
5. **Raise the smallest text and let it scale.** The status line and layer notes are 11 to 12 px; all sizes are fixed `px`, the collapsed header is a fixed 64 px and the tool row does not wrap, so 200% text and 320 px width will clip or overflow (INFERENCE from CSS; needs a device). Move to `rem` with `min-height`, and test at emulated zoom.

## Findings table

Severity: High (blocks a user group or fails a Level A/AA criterion on the evidence read), Medium (degrades use or likely AA failure under stated assumptions), Low (polish or AAA).

| # | What | Evidence | Criterion | Severity |
|---|---|---|---|---|
| F1 | Roads, generalized land, wilderness, research areas (Aspen: 51) have no list, search or other non-map route to their detail | READ IN FILE: `shell.js` `renderResults` and `renderSearch` list only trails, places and trailheads; `browse.js:7` modes are trails, camping, trailheads; `capabilities.js` `inventory` is `place_list` only; `showSources` lists per-layer evidence and counts, plus null-geometry records only (`shell:80-85`). M4 adds water names to search (`spec4` section 11) but no other layer. | 1.1.1 (A) [W3C WCAG 2.2](https://www.w3.org/TR/WCAG22/); Minnesota guide [PDF](https://mn.gov/mnit/assets/Accessibility%20Guide%20for%20Interactive%20Web%20Maps_tcm38-403564.pdf) | High |
| F2 | GeoJSON lines and polygons are not focusable or announced: layers are created with `interactive:false`; only markers get `keyboard:true` | READ IN FILE `adapter:190`, `adapter:183` | 2.1.1 (A), 1.1.1 (A) | High (mitigated only if F1 is fixed) |
| F3 | Pin accessible name: `role=button` plus `tabIndex=0` on a `div` whose visible content is the glyph (`•`, a number or a symbol); `title` is set, `alt` only applies to `IMG` | READ IN FILE `adapter:182-184`, Leaflet 1.9.4 `vendor/leaflet.js` sets `role=button` and `title`, `alt` only for `IMG`. Accessible-name computation then prefers content over `title`: INFERENCE; UNKNOWN until VoiceOver/TalkBack is run | 4.1.2 Name, Role, Value (A); 1.1.1 | High |
| F4 | All 36 Douglas recreation pins (campground, trailhead, area) look identical: paper badge, bullet. Aspen pins carry a number or symbol but no type cue | READ IN FILE: display data has no `symbol` or `number`; `adapter:182` falls back to `•`; place lists carry `number` or `symbol` only for Aspen (`overnight-options.json`, `destinations.json`) | 1.4.1 (A) [W3C](https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html) | Medium |
| F5 | Trail (`#d06030`) and road (`#b1a58a`) lines differ only by colour: both solid, 2.25 px, opacity 0.85 | READ IN FILE `land:36` (computed by running `style()`; same for both regions) | 1.4.1 (A) | High |
| F6 | Aspen streams and lakes are styled by the polygon tier: `#b8b9b6`, 1.3 px, opacity 0.6, same as wilderness and Douglas waterbodies. Douglas waterways use `#73c5dc`. So "water" is grey in Aspen and blue in Douglas, and wilderness is indistinguishable from water in Aspen | READ IN FILE: `hydrology` has Polygon features so `tier()` returns P (`land:24-29`, computed output). `spec4` section 11 says "keep the single M3 water colour", which is not what Aspen renders | 1.4.1 (A); 1.4.11 (AA) | Medium (inconsistency); High for colour-only identity |
| F7 | Unselected line contrast on assumed basemaps is below 3:1 almost everywhere. Trail vs M1 is 1.04:1; vs D1 2.44:1; best 2.81:1 (L1). Roads: 1.33 to 4.85. Water (Douglas): 1.11 to 5.94. Aspen grey streams: 1.08 to 3.69 | READ IN FILE arithmetic (`measure.cjs`); basemap colours ASSUMED | 1.4.11 (AA) [W3C](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html) | Medium (imagery varies per pixel; real result UNKNOWN) |
| F8 | Selected line casing is robust: two-tone casing (near-white `#f8f8f2`, near-black `#202124`) gives at least 3.8:1 on every assumed basemap with one of the two tones (D1 halo 10.49, D2 14.01, M1 3.93/3.84, M2 edge 9.23, L1 edge 14.03, L2 11.50) | READ IN FILE `adapter:213-215`; arithmetic | 1.4.11, 1.4.1; M3 A13 requirement | Pass (strength) |
| F9 | Land class tints are nearly invisible by design: fill 0.12 gives 1.02 to 1.28:1 against the basemap; class pairs differ by CIEDE2000 of 0.0 to 1.3 as drawn, in normal vision as well as under CVD. Research areas and State land share `#a49ba9` (ΔE 0.0) | READ IN FILE `land:18,33,34`; `measure.cjs`. Design cap is 0.12 (`spec3` section 13) | 1.4.1; 1.4.11 | Medium (intentional; see Recommendation R12) |
| F10 | Legend swatch is an 8 px left border in the opaque tint. Opaque tints are ΔE 5.3 to 11 apart in normal vision and 0.5 to 7.5 under protanopia (BLM vs State 0.5; USFS vs Other Federal 1.1) | READ IN FILE `shell.js` `renderLandLegend`; `measure.cjs`. Each swatch has adjacent text, so the legend is not colour-only | 1.4.1 | Low |
| F11 | Satellite/Topo pressed state: background `#d5f780` vs `#fafbf6` is 1.16:1; `aria-pressed` is set, but sighted cue is colour only. Same for list filter buttons | READ IN FILE `css:9,23`; `shell:26` | 1.4.1 (A); 1.4.11 | Medium |
| F12 | Button, input, select borders `#e2e4dc` on paper are 1.23:1; floating tool buttons rely on fill against the map (paper on L1 is 1.10:1) | READ IN FILE `css:1,3`; arithmetic | 1.4.11 (AA) | Medium |
| F13 | Focus ring `#567824`, 3 px, offset 2: 4.92:1 on paper (panels), but 2.19 (D1), 2.92 (D2), 1.22 (M1), 2.93 (M2), 4.45 (L1), 3.65 (L2) on map backgrounds. Applies to markers and the map container | READ IN FILE `css:4`; arithmetic; backgrounds ASSUMED | 2.4.7 (AA), 1.4.11 (AA) | Medium |
| F14 | Text sizes: summary status 11 px; layer notes, layer state, tool buttons, banner, result sub-lines 12 px; map labels 11 px; Leaflet attribution 9 px (exempt in spec). Body 15 px | READ IN FILE `css:1,9,11,15,17,18,41,20` | 1.4.4 (AA) context; Health.gov 16 px guidance [HERMES-SOURCED](https://odphp.health.gov/healthliteracyonline/2016/display/full/) | Medium |
| F15 | Text contrast in panels passes: ink 14.58:1; muted `#666c60` 5.21:1 on paper (5.41 on white; 4.50 on the pressed-toggle fill) | READ IN FILE `ui.cjs` | 1.4.3 (AA) | Pass |
| F16 | Region title is paper-coloured text with a 4 px black shadow directly on the map: 10.75:1 on D1 but 1.68:1 on M2 and 1.10:1 on L1 without the shadow's help | READ IN FILE `css:8`; arithmetic; shadow benefit UNKNOWN | 1.4.3 (AA) | Medium |
| F17 | Fixed heights with clipping: collapsed sheet 64 px, header 64 px, topbar 44 px, banner 44 px, summary `nowrap` ellipsis, map labels `nowrap` ellipsis | READ IN FILE `css:7,10,11,18,41` | 1.4.4, 1.4.10, 1.4.12 (AA) [W3C](https://www.w3.org/TR/WCAG22/) | Medium (INFERENCE: clipping at 200% text; UNKNOWN on device) |
| F18 | All font sizes are fixed `px` (root `font:15px`), so OS-level text size and iOS Dynamic Type do not apply; browser page zoom does | READ IN FILE `css:1`; Dynamic Type behaviour INFERENCE | 1.4.4 (AA) | Medium |
| F19 | The tool row (`Satellite`, `Topo`, `Fit area`, `+`, `−`) is a non-wrapping flex row anchored right; at 320 px it fits only if text is default. It was passed at 320 x 568 by B2 (no horizontal scroll) at default text only | READ IN FILE `css:9`; `README` B1/B2 at 320; behaviour at larger text INFERENCE | 1.4.10 (AA) | Medium |
| F20 | Touch targets: every `button`, `input`, `select`, `textarea`, `summary` has `min-width/min-height:44px`; layer checkbox 44 x 44; pins 44 x 44 icon box with a 28 px visible badge; links inside sheet and dialog `min-height:44px`; tool gap 4 px | READ IN FILE `css:3,15,17,26,27,45`; `adapter:184`; tested by B2 (`explore-checks.mjs:157-158`) | 2.5.8 (AA, 24 px) [W3C](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html); 2.5.5 (AAA, 44 px) [W3C](https://www.w3.org/WAI/WCAG22/Understanding/target-size-enhanced.html) | Pass |
| F21 | Map tap corridor: 14 px tolerance each side of a line = 28 px wide (above 24, below 44); points 14 px plus icon box; polygons whole area. A line tap that misses by more than 14 px selects the land polygon under the finger (priority order points, labels, lines, polygons) and opens the sheet | READ IN FILE `adapter:6,32,37,45-50`; `spec3` A14 table | 2.5.8 | Low; mis-tap cost Medium (INFERENCE) |
| F22 | Tap slop 10 px: a touch that moves more than 10 px is a pan, not a selection; 280 ms deferral and a 30 px double-tap radius turn two close taps into zoom | READ IN FILE `adapter:7,8,9,95-97,150-155` | 2.5.1, 2.5.2; no gloved or tremor data. UNKNOWN: gloves/wet screens (Hermes also found none) | Medium (UNKNOWN) |
| F23 | Drag alternatives exist for the sheet (toggle button, Enter/Space, Escape) and drawer (close button, Escape); zoom has `+`/`−` buttons and double-tap; Leaflet keyboard arrows pan and +/− zoom when the map container is focused | READ IN FILE `sheet:48-60`, `drawer.js`, `shell:27`, Leaflet `keyboard:!0`, `keyboardPanDelta:80` | 2.5.1, 2.5.7 (AA) | Pass; map pan has no on-screen button (INFERENCE: arguably essential) |
| F24 | Keyboard: Tab reaches every visible control (B5), Escape closes top overlay and returns focus (A11/A12 tests), collapsed sheet body is `inert`, no positive `tabindex`; no keyboard route to a line or polygon (F2) | READ IN FILE `explore-checks.mjs:163-165,218-221`, `sheet:50` | 2.1.1, 2.4.3, 2.4.7 | Pass for controls; Fail for map features |
| F25 | Live regions: `#explore-summary` `role=status` (updates on layer load, counts; text starts "Loading"), `#explore-banner` `role=status`, planner `#count` `role=status`, trip form errors `role=alert`. No announcement on selection, layer toggle result, filter result count in the Douglas/Aspen search list, or "no hit" tap | READ IN FILE `shell:28,31`; `capabilities.js` form error; `browse.js:31`. Selection announcement absent: READ IN FILE by search for `aria-live` and `role=` | 4.1.3 Status Messages (AA) | Medium |
| F26 | Detail view: focus is moved to the Back button (`shell:123`), so a screen reader hears "Back", not the feature title (`#explore-detail-title`, an `h2`). INFERENCE; UNKNOWN until tested | READ IN FILE code; behaviour INFERENCE | 2.4.3, 4.1.3 | Medium |
| F27 | Map container: `aria-label="Interactive map"` on a `div` with no role. Names on role-less `div`s are not reliably exposed. Leaflet adds `tabindex=0` to the container | READ IN FILE `shell:24`; Leaflet source; exposure INFERENCE | 4.1.2 | Medium |
| F28 | Landing overlay (`.explore-landing`, `z-index:800`, position absolute) is a plain section; the map, tools and sheet beneath are not `inert` or `aria-hidden` while it is shown. Tab and virtual cursor may reach covered controls | READ IN FILE `capabilities.js` landing build (no `inert`), `css:24`; focus behaviour INFERENCE | 2.4.3, 1.3.2, 2.4.11 (AA) | Medium (INFERENCE) |
| F29 | Reduced motion: CSS transitions and animations are disabled; Leaflet zoom, fade and marker animation are decided once at init (`adapter:12,112-113`), and `fit()` re-reads per call (`adapter:283`). The harness runs every test with `prefers-reduced-motion: reduce` emulated, so the animated path is untested | READ IN FILE `css:22`; `explore-checks.mjs:114` | 2.3.3 (AAA) | Low |
| F30 | No `prefers-contrast`, `forced-colors` or `prefers-color-scheme` rule exists in any explore CSS; the only media features are `min-width:768px`, orientation and reduced motion | READ IN FILE by search of `css` | 1.4.11; user preference | Low to Medium |
| F31 | Zoom is not disabled: the viewport meta has no `user-scalable` or `maximum-scale`; `touch-action:manipulation` on buttons only | READ IN FILE `index.html:3`; `css:43` | 1.4.4 (AA) | Pass |
| F32 | Page language and structure: `<html lang="en">`, one `<main>`; the shell has no page-level `h1` (the drawer, dialogs and landing each contain their own `h1`) | READ IN FILE `index.html:2,7`; `shell:30,33`; `capabilities.js` landing | 3.1.1, 2.4.6, 1.3.1 | Low |
| F33 | Low bandwidth: no service worker anywhere in `v2/` (search); basemap tiles are the heavy resource and the app is tested with them absent; largest display artifacts gzip to Douglas waterways 407 KB, Aspen hydrology 267 KB, trails about 190 to 198 KB each; Leaflet 147,552 bytes | READ IN FILE sizes (`gzip -c`); harness blocks non-local requests and "the app must still work" (`README`) | ICA 2025 field-map paper [HERMES-SOURCED](https://ica-abs.copernicus.org/articles/10/111/2025/ica-abs-10-111-2025.pdf); MDN [HERMES-SOURCED](https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Guides/Best_practices) | Low |
| F34 | Overlapping features under one tap: no chooser; recorded M3 limitation (two coincident Douglas trails; search is the workaround) | READ IN FILE `spec3` A13 "Overlapping trails" | 2.5.8 spirit; Minnesota guide | Low (accepted by owner) |

## By user group

### Low vision

- Zoom: the page can be zoomed (F31). Panels are `px`-sized (F18) and several have fixed heights (F17). **Text is small where it matters**: the status line (F14, 11 px) is the only text that reports load state and counts. INFERENCE: at 200% browser zoom the 390 px phone layout becomes about 195 CSS px wide; the sheet handles that through `overflow:auto` in the body (READ IN FILE `css:12`) but the topbar, tool row and banner are fixed-height single rows.
- Contrast: panel text passes comfortably (F15). The map is the weak point: unselected lines are below 3:1 on most assumed basemaps (F7), the focus ring is weak over imagery (F13), the region title relies on a shadow (F16). The selected-line casing is strong (F8) and is the best pattern in the app.
- Magnification users also lose the line when it is thin: 1.3 px Aspen streams at 0.6 opacity (F6/F7).
- No high-contrast or large-label mode and no `prefers-contrast` support (F30).
- A real-device check is needed for pinch magnification (OS zoom) with the sheet open; see the device list.

### Colour-vision deficiencies

Simulation: Machado, Oliveira and Fernandes (2009), severity 1.0, in linear RGB; distance CIEDE2000. Script `measure.cjs`. Representative colours as above.

Line colours (opaque), closest pairs (ΔE2000; below about 10 is hard to tell apart for a thin line):

| Pair | Normal | Protan | Deutan | Tritan |
|---|---|---|---|---|
| road `#b1a58a` / grey P tier `#b8b9b6` | 11.7 | 11.7 | 11.6 | 11.7 |
| water `#73c5dc` / grey P tier | 19.3 | 13.7 | 16.5 | 23.4 |
| trail `#d06030` / road | 26.8 | 21.0 | 16.6 | 24.6 |
| road / water | 28.4 | 26.2 | 29.0 | 35.6 |
| trail / water | 48.0 | 43.6 | 43.9 | 63.0 |

- READ IN FILE: the trail/road pair is the one that must carry the most meaning and it narrows from 26.8 to 16.6 under deuteranopia; it is still separable by colour but nothing else separates them (F5).
- READ IN FILE: the closest pair overall is road vs the grey polygon-tier colour. It occurs in Aspen, where roads are `#b1a58a` and streams `#b8b9b6`. It is ΔE 11.6 to 11.7 under every simulation; both colours are low-saturation, so lightness is the only separator, and stream width (1.3 px at 0.6 opacity) is thinner than road width (2.25 px at 0.85).
- Land tints as drawn (0.12 over D1): ΔE 0.0 to 1.3 in every vision type; the classes cannot be told apart by anyone on the map. This is by the M3 design cap (`spec3` section 13.2), not a CVD-specific problem, but it means class meaning lives only in the legend and detail text (F9).
- Opaque legend swatches: worst pairs under protanopia are BLM/State 0.5 and USFS/Other Federal 1.1; deuteranopia LG/PVT 2.2 and BLM/State 2.2; tritanopia BLM/LG 2.5. The adjacent text label makes this acceptable (F10).
- Selection never relies on colour (width +3 px, never under 5 px, two-tone casing, other lines dimmed): READ IN FILE `adapter:213-237`; M3 A13 requirement.
- Hermes recommends ColorBrewer's colourblind-safe filter as a screening aid only; it does not guarantee separation over imagery [HERMES-SOURCED](https://colorbrewer2.org/). Hue is a poor channel on imagery in any case; the recommendations add shape and width.

### Motor impairments and gloved hands

- Controls are 44 px (F20), above WCAG 2.5.8's 24 px and equal to 2.5.5 and Apple HIG [HERMES-SOURCED](https://developer.apple.com/design/human-interface-guidelines/buttons). Material suggests 48 dp with 8 dp separation [HERMES-SOURCED](https://m2.material.io/design/usability/accessibility.html); the tool row pitch is 48 px (44 + 4 gap) with 4 px clear space.
- The sheet and drawer have drag alternatives (F23), satisfying 2.5.7. Pinch zoom has `+`/`−` and double-tap (F23).
- The map hit corridor is 28 px (F21). A 10 px tap-slop (F22) means a finger that rolls more than 10 px during a tap is read as a pan, so selection silently does nothing. INFERENCE: this is likely harder with gloves, tremor or a wet screen; no standard or source quantifies it (Hermes: UNKNOWN). Needs field test.
- The 280 ms deferral (`adapter:8,155`) makes every selection feel delayed by design; owner accepted it (`spec3` third real-device result).
- A miss tap selects land and opens the sheet (F21). The cost of a mis-tap is a half-height sheet that must be dismissed.
- Missing: a way to select what is under the map centre or crosshair ("select here"; Hermes recommendation [HERMES-SOURCED](https://www.w3.org/TR/WCAG22/)), and an overlap chooser (F34).
- Keyboard/switch users: Tab reaches controls and pins; lines and polygons are unreachable (F2).

### Small screens

- 320 x 568 is part of the harness matrix (B1 free map at least 72%, sheet at most 88 px collapsed, B2 no horizontal scroll and no sub-44 px control; `explore-checks.mjs:149-158`). READ IN FILE at default text size and zoom. 1.4.10 reflow is therefore evidenced for the default text size only.
- Short landscape (max-height 500 px) switches to side panels and is checked in A11/A12 for four device sizes with notches (`explore-checks.mjs:462`).
- INFERENCE: the stack of absolute-positioned rows (topbar at top 4 px, tools at 56 px, banner at 104 px, each 44 px high) leaves 568 - 148 - 64 = about 356 px of free height at 320 x 568 before any text enlargement; any growth in the three rows pushes the map area down.
- Sheet half state is 40% of the usable viewport and expanded 75% (`css:11`), with a free-map floor of 72/80/75 per size. This is a deliberate M3 contract; text enlargement must not break it.

### Older users

- 15 px body, 11/12 px secondary text (F14); Health.gov advises 16 px minimum and adjustable size for older adults [HERMES-SOURCED](https://odphp.health.gov/healthliteracyonline/2016/display/full/).
- Many words are in the sheet header and tool buttons: "Results · Expand", "Fit area". INFERENCE: "Fit area" is jargon; no label tests exist.
- Dark text on a very light background is good (14.58:1). Reversed-out text appears on the landing page (paper on `#20241e`, 15.16:1) and on the map title only.
- Tap delay (280 ms) and double-tap zoom (30 px, 280 ms) can be mis-triggered by a slow double tap. INFERENCE only.
- Confirmation and "undo" are not relevant (no destructive map actions), apart from "Remove" next to saved items (`capabilities.js`, `browse.js`), which sits adjacent to the item button with 8 px gap in a row (INFERENCE: adjacent destructive control; Hermes suggests separating them [HERMES-SOURCED](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html)).

### Bright sunlight

- UNKNOWN for everything on a real screen. What the code shows: the default is satellite imagery with a dark `#343e30` background fallback; the Topo basemap is available; there is no high-contrast mode.
- Thin, low-opacity strokes are the sunlight risk: land outlines 1 px at 0.5 (ratio 1.2 to 2.5 on assumed bases), Aspen streams 1.3 px at 0.6, unselected lines at 2.25 px 0.85. On the pale bases (M2, L1, L2) every unselected stroke measured is below 3:1; the best value on a pale base is the trail on L1 at 2.81 (F7).
- The selected casing has a near-white halo and a near-black edge, so one tone always separates from either dark or pale ground (F8): a good outdoor pattern and the one to extend.
- Map labels are ink on a 87% paper-colour pill (11.6 to 14.4:1), strong, but only appear from zoom 14, capped at 32, 11 px (`adapter:5,260`; `css:41`).
- The ICA field-mapping paper says outdoor maps may need higher contrast and simpler content [HERMES-SOURCED](https://ica-abs.copernicus.org/articles/10/111/2025/ica-abs-10-111-2025.pdf); Hermes also warns that dark is not universally best in sunlight.

### Low bandwidth

- No service worker, no offline shell (F33). The app is already tested to load and work with basemap tiles blocked (README), and all display artifacts are fetched per layer with independent retry (`shell:drawLayer`, B7/B8 tests).
- Display weight: Douglas waterways 1.79 MB raw, 407 KB gzip; Aspen hydrology 1.16 MB, 267 KB gzip; trails about 0.86 to 0.88 MB, 191 to 198 KB gzip each. The M3 contract limits bytes to map-usable at 500,000 (Douglas reached 504,430 once, M4 A2). So the weight of a layer is already a governed budget.
- All layers default on (`explore.json`), so a low-bandwidth user loads every layer unless they untick it. INFERENCE: a "data saver" default would need an owner decision against A10 performance thresholds.
- The sheet text states what has failed ("Could not load", Retry) per layer, which is good behaviour for flaky connections (READ IN FILE `shell:drawLayer`).
- Satellite is the default basemap and is the heavier one; Topo is one tap away (`css:9`).

### Screen readers

Everything in this section is INFERENCE from markup and needs VoiceOver (iOS Safari) and TalkBack (Android Chrome) to confirm.

- Controls are native `button`, `input`, `select`, `summary`, `details`, `dialog` (focus moves into `showModal()` dialogs, returns to the opener on close: READ IN FILE `shell:50-56`, tests A11/A12). Good.
- `aria-label` is set on the sheet (`Results`), the drawer (`Layers & legend`), nav groups (`Explore`, `Map controls`), zoom (`Zoom in`/`Zoom out`), and close buttons (READ IN FILE `shell:24-33`).
- `+` and `−` have `aria-label`; `×` close buttons have `aria-label`. The layer toggles are real labelled checkboxes with visible text and a visible `On`/`Off` span (READ IN FILE `shell:renderDrawer`).
- The pinned status line is `role=status`, but the sheet header is only 11 px and the live region says "Loading" first (F25).
- No role on the map `div` (F27), pins named by their glyph (F3), detail title not announced (F26), selection state announced only on pins via `aria-pressed` and not at all for lines or polygons (READ IN FILE `adapter:205,228`).
- Hermes: Apple Maps lets VoiceOver browse locations, follow a road and describe nearby places; Google Maps documents a numbered list of places in the focused area [HERMES-SOURCED](https://support.apple.com/guide/iphone/use-voiceover-in-apps-iphe4ee74be8/ios), [HERMES-SOURCED](https://support.google.com/maps/answer/6396990?hl=en-NA). Ohvernight's equivalent is its list; it covers only part of the map (F1).
- Leaflet's own accessibility page was not retrievable by Hermes (UNKNOWN).

## How relevant outdoor apps compare (HERMES-SOURCED)

All of this is from `a17-map-accessibility.md`; it documents intended features, not independent conformance (Hermes: UNKNOWN).

| App | Documented | Relevance to Ohvernight |
|---|---|---|
| AllTrails | Structured "Wheelchair-friendly" tag from surface, grade, width, obstacles, parking, with a caveat that there is "no one-size-fits-all approach" [source](https://support.alltrails.com/hc/en-us/articles/360056963411-Accessibility-guide-for-wheelchair-friendly-trails) | Structured attributes with caveats. Ohvernight has no accessibility attributes and M3/M4 avoid status claims; this is out of scope, but the caveat wording style is aligned. |
| Gaia GPS | Larger map labels, high-contrast layers, adjustable waypoint colours, platform magnification (pages not retrievable by Hermes: UNKNOWN) [Android](https://help.gaiagps.com/hc/en-us/articles/5624106908439-Accessibility-Settings-in-the-Android-app), [iOS](https://help.gaiagps.com/hc/en-us/articles/5437182417431-Accessibility-Settings-in-the-iOS-app) | Closest model for R9 (field mode): user-controlled label size, contrast and symbol colour. |
| onX | Vehicle-class lines distinguished by solid, hash marks and dash patterns; "Conditions can vary" warning [source](https://www.onxmaps.com/hunt/blog/hunting-road-accessibility-research-routes-access-points) | Direct precedent for R3 (dash/hash per road class) and for redundancy beyond hue. |
| Google Maps | Keyboard navigation, arrow-key panning, numbered list of places in the focused area, voice guidance [source](https://support.google.com/maps/answer/6396990?hl=en-NA) | Precedent for R1 (a list for what the map shows). |
| Apple Maps | VoiceOver browsing of pins, road following, location card, spoken description of nearby places [source](https://support.apple.com/guide/iphone/use-voiceover-in-apps-iphe4ee74be8/ios) | Hermes advises a simpler HTML list rather than reproducing native gestures. |

## Recommendations, ranked by value for effort

For each: what it changes; which approved M3/M4 behaviour or wording it touches (so the owner can see what needs a decision); how it could be tested in the existing harness (`v2/pipeline/tests/browser/explore-checks.mjs`, Chrome DevTools Protocol, offline).

### R1. Name the map, pins and selection for assistive technology (high value, low effort)

- Changes: give the map container a role and a short label plus description (for example a labelled `region`/`group` with `aria-describedby` giving the list route and the keyboard keys); set `aria-label` on each pin from its name plus type; after a selection, move focus to the detail title (`h2` with `tabindex=-1`) or announce "Selected: <title>" in the existing status region while keeping the Back button one Tab away. (F3, F26, F27.)
- Touches: no approved wording or interaction. New strings (type words) must pass the M3 A4 wording inventory (`FORBIDDEN_WORDS` in `layer-registry.js` applies to config, and a new string list is cleaner). Focus target after selection is current tested behaviour (`explore-checks.mjs:163`, "A11 selection"), so existing tests that assert `activeElement` is the Back button would change: owner/coordinator approval.
- Test: assert every `.leaflet-marker-icon` has `aria-label`; assert the map container has `role` and an accessible name; assert focus lands on the title after `explore.select()`. Real screen-reader result is UNKNOWN until a device test.

### R2. A "Map features here" list for every selectable layer (highest value, medium effort)

- Changes: an item in the existing sheet (alongside "Find trails & camping") that lists what is under the current viewport or centre, per layer, sorted by distance, with name or class label and layer name, opening the same detail through `showDetail`. Covers roads, land, wilderness, research areas, water (M4 adds search, but not "what is here"). (F1, F2, F21, F34.) Also resolves overlap, which M3 A13 deferred.
- Touches: M3 A13 "overlapping trails" deferral and its "generic several features under one tap → chooser" future requirement; adds a route, not a changed tap contract (A14 table unchanged). Trust wording: the list must show only existing approved labels (W1 to W11 land labels, W4 for PVT; nothing like "public"). Owner decision because it is new UI.
- Test: harness already calls `explore.select(entry, feature)` and counts features per layer; assert that for each layer the list contains every feature in the display file within the view bounds, and that selecting one produces the same `explore.state.selection` as a map tap (reuse `assertSelection`).

### R3. One non-colour channel per category (high value, medium effort; owner decision)

- Changes: roads get a dash pattern or casing that trails lack (or the reverse); water streams get a distinct width/dash from wilderness; pins get a type glyph (campground, trailhead, area) in place of the shared bullet; Aspen hydrology gets its own style instead of the polygon tier (F4, F5, F6). Keep hue exactly as is.
- Touches: `spec3` A14 "Trail readability ... Other layer colours are not redesigned and no new colour carries a meaning" (this adds shape, not colour, but is a style change); `spec3` section 13.2 rule 7 (context polygons never stronger than a road or trail line); `spec4` section 11 "Streams and waterbodies keep the single M3 water colour" and O3 "no map-level status symbols" (a type glyph for pins is not a status symbol but must be checked against O3). The Aspen water style is also an inconsistency with M4's stated assumption and should be raised regardless. Water styling lands in M4; this is the cheapest moment.
- Test: extend T4/`land-style.test.cjs` to assert pairwise-distinct (colour, weight, dash) across all current layers (a unit assertion, no browser needed); add a computed-style loop in the harness over `window.__rendered` paths.

### R4. Make focus, borders and pressed state visible on imagery (high value, low effort)

- Changes: two-tone focus ring (light inner, dark outer) on `.explore-root :focus-visible` and markers; control border darker than `#e2e4dc` (about `#8a8f84` gives roughly 3:1, calculate before choosing); pressed toggles get a non-colour cue (heavier border, check glyph or underline) in addition to fill. (F11, F12, F13.)
- Touches: none of the approved behaviour or wording. Visual only. The spec says "Focus is always visible" (`spec3` section 6) and this strengthens it.
- Test: compute contrast in the harness from `getComputedStyle(...).outlineColor` against ASSUMED backgrounds is brittle; a Node unit test on the two chosen colours plus a harness assertion that the computed `outline-style` is not `none` on `:focus-visible` markers and map container; assert `aria-pressed` buttons have a computed `border-width` or `text-decoration` difference.

### R5. Scalable text and non-clipping layout (high value, medium effort)

- Changes: `rem` units for font sizes; 14 to 16 px minimum for status line, layer notes, banner, tool buttons (not the attribution); `min-height` instead of fixed `height` for topbar, banner, header; allow the tool row and banner to wrap. (F14, F17, F18, F19.)
- Touches: M3 harness limits for sheet height and free map at 320 x 568 (sheet at most 88 px collapsed; free map at least 72%). A larger header text could break these thresholds, which are `spec3` section 16.4/20 acceptance numbers: owner decision on whether to relax them for large text only. No approved wording.
- Test: add a harness case at 320 x 568 and at 195 x 422 (200% page-zoom equivalent) via the existing `Emulation.setDeviceMetricsOverride` (already used at `explore-checks.mjs:482`); assert no horizontal overflow, no control under 44 px, no overlap of tools, banner and topbar rects. The real text-size setting (iOS Dynamic Type, Android font scale) is a device check.

### R6. Announce the right things (medium value, low effort)

- Changes: an `aria-live=polite` status for "N results", layer toggle outcome ("Wilderness on, 3 features"), "No feature at that point" on a no-hit tap, and selection; keep it terse (Hermes: announce meaningful state changes, not tiles) [HERMES-SOURCED](https://mn.gov/mnit/assets/Accessibility%20Guide%20for%20Interactive%20Web%20Maps_tcm38-403564.pdf). (F25.)
- Touches: none approved. The A14 table says "empty tap: selection and camera unchanged"; a status message does not change either.
- Test: assert the status node text after `explore.select`, after toggling a layer, after `exploremaptap` with `hit:false`; harness already listens for that event (`explore-checks.mjs:408-410`).

### R7. Inert background for the landing overlay and drawer (medium value, low effort)

- Changes: set `inert` on `.explore-map`, tools, topbar and sheet while the landing overlay is shown (or make it a modal `dialog`); restore on dismiss. (F28.)
- Touches: Escape on the landing is current behaviour (`capabilities.js` keydown) and stays. No wording.
- Test: Tab loop with the landing open must not reach a control outside it (extend B5 at `explore-checks.mjs:218-220`).

### R8. Support `prefers-contrast` and `forced-colors`, and make reduced motion live (low to medium value, low effort)

- Changes: under `prefers-contrast: more` use darker borders, 2 px focus and opaque casing on all lines; under `forced-colors` rely on system colours for controls (canvas layers are unaffected); re-read the reduced-motion query on change. (F29, F30.)
- Touches: line opacity is an A14 contract (unselected lines at about 0.4 to 0.5 while a line is selected). A user-preference override affects only users who opt in; owner decision for the casing change on all lines.
- Test: harness already uses `Emulation.setEmulatedMedia` (`explore-checks.mjs:114`); add `prefers-contrast: more` and assert computed borders and outline widths; add a case with reduced motion off so the animated path runs at least once.

### R9. A field (high-contrast) mode (high value if field use is a goal, high effort; owner decision)

- Changes: a toggle (Hermes recommendation 7) that casing all lines, raises label size and halo, simplifies the basemap (Topo or a plain one) and reduces layer density [HERMES-SOURCED](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html). Gaia GPS documents the comparable feature [HERMES-SOURCED, unverified](https://help.gaiagps.com/hc/en-us/articles/5624106908439-Accessibility-Settings-in-the-Android-app).
- Touches: `spec3` section 13 tier ceilings and A14 palette rule ("not a new map theme"); trust wording none. A new setting and a new persistent preference. Larger than M4's scope.
- Test: harness can assert the casing paths exist for every line when the mode is on. Real sunlight effectiveness is UNKNOWN until field tested.

### R10. Pan and "select here" without a drag (medium value, medium effort)

- Changes: four small pan buttons or a "Select at centre" control that opens R2's list for the point under a crosshair; keeps the selection contract. (F23 gap, F22.)
- Touches: `spec3` A14 table (a new way to hit a feature; no camera change); `spec3` control cluster size limits. Owner decision.
- Test: harness drives the control and asserts the same `explore.state.selection` as a mouse tap.

### R11. Overlap chooser (medium value, medium effort; already a known deferral)

- Changes: the generic "several features under one tap → chooser" that `spec3` A13 records as a future requirement; R2 can serve as its first version.
- Touches: `spec3` A13 "Overlapping trails (owner)". Owner decision.
- Test: the existing coincident trail case (Douglas, A12) becomes a test that both ids are offered.

### R12. Land class legibility without breaking the 0.12 cap (low to medium value, owner decision)

- Changes: leave the fill cap alone; instead make the class visible in text (a map label for large polygons at moderate zoom is off the table: no label rule exists for land), or add a legend-side "show only this class" highlight. (F9, F10.)
- Touches: `spec3` section 13.2 rules 2, 5 and 7; W1 to W11 byte-identical; A14 "no parcel-like outline". The owner set the 0.12 cap on trust grounds (a context layer must not look authoritative), so accessibility should not override it. Nothing is recommended beyond R2 (list route) and R3's legend shapes.
- Test: T4 stays as is.

### R13. Offline shell and data saver (low value now, medium effort; owner decision)

- Changes: a service worker for the shell and the last-loaded display artifacts with a visible cached date, and an option to start with layers off or with Topo. (F33.)
- Touches: `spec3` A10 performance contract and R-1 to R-5 triggers; trust: cached data must carry its fetch date (existing `Fetched <date>` lines already do). Hermes: show cached extent and date [HERMES-SOURCED](https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Guides/Best_practices).
- Test: harness blocks non-local requests already; an offline reload case would need the service worker to be registered under the local server.

## What must be checked on a real device by a human

None of this can be settled from the code. UNKNOWN until done.

1. VoiceOver on iPhone Safari and TalkBack on Android Chrome: rotor/headings, how pins are named (F3), whether the map `div` is exposed (F27), whether focus on the Back button hides the feature title (F26), what is announced when a layer loads or a feature is selected, and whether covered controls are reachable behind the landing overlay (F28).
2. Switch Control or an external keyboard: reach and activate pins; arrow-key panning and `+`/`−` on the map; verify nothing traps focus in the sheet, drawer or dialogs.
3. 200% and 300% OS text size (iOS Dynamic Type, Android font scale) and 200% page zoom at 390 and 320 px width: clipping of the summary line, tool row, banner, topbar (F17 to F19); iOS Safari ignores `px`-sized text for Dynamic Type.
4. OS magnifier and pinch zoom with the sheet in each state; check the sheet header does not obscure a focused control (2.4.11).
5. Colour: Colour Filters and Daltonization settings on iOS/Android; view trail, road, stream and land on real satellite and Topo tiles at zoom 12, 14, 16, in at least three terrain types; sample the real imagery colours behind lines and confirm or correct the assumed backgrounds above.
6. Bright sunlight at maximum brightness, both basemaps: can unselected trails, Aspen streams and land outlines be seen (F7); does the selected casing read; do map labels and the region title read (F16).
7. Gloves (thin liner, ski glove), wet screen, cold hands: does a tap on a trail select (14 px tolerance, 10 px slop, 280 ms deferral), how often does a tap become a pan (F22), and are 44 px controls hit reliably (F20). No standard or source gives numbers (Hermes: UNKNOWN).
8. Older users (65+) and users with tremor: is the 280 ms double-tap window mis-triggered, are 11 to 12 px texts readable, is "Fit area" understood, are the Satellite/Topo pressed states perceived (F11, F14).
9. One-handed and thumb reach on a large phone and on a small phone; position of the tool row at top right.
10. Poor and offline connections: load with only 3G throttling and with no connection, retry behaviour, what a user sees with tiles blocked, and the Douglas waterways 407 KB gzip layer (F33).
11. Landscape with cut-out and bottom bars on iPhone Safari (already an owner finding in M3; the accessibility angle is focus and reach of Layers and Search).
12. Reduced motion on a device with the system setting on and off, including after changing the setting while the page is open (F29).
13. High-contrast OS settings (iOS Increase Contrast, Windows forced colours with a desktop browser): controls and focus rings; confirm the canvas layers are unaffected (F30).

## Not verified, not claimed

- No screen reader, device, or browser was used; the browser harness was not started.
- Contrast ratios against imagery use six assumed colours; real tiles vary per pixel.
- The CVD figures come from one published simulation matrix (Machado et al. 2009, severity 1.0), which is a model, not a person's perception.
- The Hermes sources are unverified; where Hermes could not load an official page (Leaflet, Esri, Mapbox, Gaia, UK GDS), no claim here rests on that page.
- The recommendations do not decide access, permission, or availability; every map layer remains research context only, per `AGENTS.md` and `DATA-LICENSE.md`.
