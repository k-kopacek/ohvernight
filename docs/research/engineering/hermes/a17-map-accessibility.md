DRAFT - UNREVIEWED

# Ohvernight A17 — Map Accessibility and Field Usability

> Hermes report (GPT-5.6 luna), 2026-10-07, stored as returned. HERMES-SOURCED: web research only, no repository access. Nothing here is verified by the coordinator unless another document says so, and nothing is decided.

Access date: 2026-10-07

Scope: mobile-first Leaflet web map with tappable trails, roads, streams, polygons, points, detail sheets, and layer toggles. Findings distinguish publisher requirements from implementation inferences. No access, permission, or activity-status conclusions are made.

## Binding criteria

WCAG 2.2 is the technical accessibility baseline. Section 508 directly binds U.S. federal agencies and federally used or procured ICT; it is not, by itself, a legal determination for Ohvernight. Section 508 requires comparable access and alternative access where compliance creates an undue burden. [PRIMARY SOURCE — W3C WCAG 2.2](https://www.w3.org/TR/WCAG22/) [PRIMARY SOURCE — U.S. Access Board](https://www.access-board.gov/ict/app-d.html)

| Criterion | What it requires | How an interactive map typically fails |
|---|---|---|
| 1.1.1 Non-text Content — Level A | Provide an equivalent for meaningful non-text content. For a map, this means an accessible textual representation of meaningful places, lines, polygons, states, and relationships. [PRIMARY SOURCE — Minnesota interactive web map guide](https://mn.gov/mnit/assets/Accessibility%20Guide%20for%20Interactive%20Web%20Maps_tcm38-403564.pdf) | The map is visually rich but exposes no equivalent list, summary, or accessible feature descriptions. |
| 1.4.1 Use of Color — Level A | Color must not be the only way to distinguish information. W3C states: “Use information in addition to color, such as shape or text, to convey meaning.” [PRIMARY SOURCE — W3C](https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html) | “Open,” “closed,” activity type, land class, or route difficulty is communicated only by hue. |
| 1.4.3 Contrast (Minimum) — Level AA | Text generally needs 4.5:1 contrast, or 3:1 for large text. [PRIMARY SOURCE — Esri accessibility guidance](https://developers.arcgis.com/javascript/latest/accessibility/) | Labels, sheet text, legends, or button text disappear against satellite imagery, terrain, or transparent overlays. |
| 1.4.10 Reflow — Level AA | Content must work without loss of information or functionality at a 320 CSS-pixel viewport width and without requiring two-dimensional scrolling, except where two-dimensional layout is essential. [PRIMARY SOURCE — W3C WCAG 2.2](https://www.w3.org/TR/WCAG22/) | The detail sheet, layer controls, legend, or filters require horizontal scrolling or overlap when text is enlarged. The map itself can remain spatial, but surrounding controls cannot depend on a fixed desktop layout. |
| 1.4.11 Non-text Contrast — Level AA | Visual information needed to identify controls, states, and meaningful graphics must have sufficient contrast against adjacent colors. [PRIMARY SOURCE — W3C](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html) | Thin trail strokes, selected polygons, focus rings, location markers, layer-toggle states, or icons blend into the basemap. |
| 1.4.12 Text Spacing — Level AA | Content must remain usable when line height is at least 1.5 times font size, paragraph spacing at least 2 times font size, letter spacing at least 0.12 times font size, and word spacing at least 0.16 times font size. [PRIMARY SOURCE — W3C WCAG 2.2](https://www.w3.org/TR/WCAG22/) | A detail sheet clips, overlaps, or hides text when users apply custom spacing or browser accessibility styles. |
| 2.1.1 Keyboard — Level A | All functionality must be operable through a keyboard interface. [PRIMARY SOURCE — W3C WCAG 2.2](https://www.w3.org/TR/WCAG22/) | Panning, zooming, selecting a feature, opening a detail sheet, changing layers, or dismissing a modal works only with pointer events. |
| 2.4.7 Focus Visible — Level AA | Keyboard focus must be visibly apparent. [PRIMARY SOURCE — W3C WCAG 2.2](https://www.w3.org/TR/WCAG22/) | Browser focus outlines are removed, or focus moves into a map feature that has no visible indication. |
| 2.4.11 Focus Not Obscured (Minimum) — Level AA | Focused controls must not be entirely hidden by author-created content. [PRIMARY SOURCE — W3C](https://www.w3.org/WAI/standards-guidelines/wcag/new-in-22/) | A focused layer toggle or feature control is covered by the detail sheet, sticky header, or mobile browser viewport. |
| 2.5.1 Pointer Gestures — Level A | Multipoint or path-based gestures must have a single-pointer alternative unless the gesture is essential. [PRIMARY SOURCE — W3C WCAG 2.2](https://www.w3.org/TR/WCAG22/) | Zoom requires pinch only; a layer or feature action requires a complex gesture; map operation is unavailable through buttons or single taps. |
| 2.5.5 Target Size (Enhanced) — Level AAA | Custom pointer targets should be at least 44 by 44 CSS pixels. W3C describes the goal as: “Make custom targets at least 44 by 44 pixels.” [PRIMARY SOURCE — W3C](https://www.w3.org/WAI/WCAG22/Understanding/target-size-enhanced.html) | Small layer icons, close buttons, compass controls, or line features require precise tapping. |
| 2.5.7 Dragging Movements — Level AA | Functionality using dragging must also be achievable with a single pointer without dragging, unless dragging is essential. [PRIMARY SOURCE — W3C WCAG 2.2](https://www.w3.org/TR/WCAG22/) | Map panning, moving a slider, or changing a route can only be done by dragging and has no arrow/button or direct-selection alternative. |
| 2.5.8 Target Size (Minimum) — Level AA | Pointer targets must be at least 24 by 24 CSS pixels, or meet the spacing, equivalent-control, inline, user-agent, or essential exceptions. W3C says the target is “at least 24 by 24 CSS pixels.” [PRIMARY SOURCE — W3C](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html) | Adjacent controls are smaller than 24 pixels, or a narrow line is the only way to select a feature and no equivalent list control exists. |

### Map-specific government and platform guidance

- Minnesota’s 2024 state guide treats interactive maps as applications that users may operate with a mouse, keyboard, voice, or other mechanism, and recommends alternatives when an interactive map is inaccessible. [PRIMARY SOURCE — State of Minnesota](https://mn.gov/mnit/assets/Accessibility%20Guide%20for%20Interactive%20Web%20Maps_tcm38-403564.pdf)
- Massachusetts GIS guidance recommends descriptive alternative text, a legend, and search as alternative ways to interact with a map. [PRIMARY SOURCE — Mass.gov](https://www.mass.gov/info-details/gis-accessibility-guidance-storymaps)
- WAI’s image-map guidance requires text alternatives for the image and each interactive region and recommends redundant text links when image-map behavior is unreliable. This is not a complete GIS-map specification, but the interaction pattern is relevant. [PRIMARY SOURCE — W3C WAI](https://www.w3.org/WAI/tutorials/images/imagemap/)
- Leaflet’s official accessibility search result says its map container and markers are keyboard operable by default and recommends descriptive marker `alt` or `title` text and keyboard/screen-reader testing. The page could not be directly loaded in this session; treat implementation details as unverified. [UNKNOWN — official Leaflet page found, direct retrieval failed](https://leafletjs.com/examples/accessibility/)
- Esri’s official JavaScript accessibility documentation search result describes keyboard navigation, alternative text, semantic structure, ARIA attributes, live regions, and dark/light contrast support. Direct retrieval failed in this session. [UNKNOWN — official Esri page found, direct retrieval failed](https://developers.arcgis.com/javascript/latest/accessibility/)
- Mapbox’s official iframe documentation search result says an informative iframe `title` provides context for screen-reader users and users with limited connectivity. Direct retrieval failed in this session. [UNKNOWN — official Mapbox page found, direct retrieval failed](https://docs.mapbox.com/help/glossary/iframe/)

## Colour and symbol

- ColorBrewer distinguishes sequential schemes for ordered values, diverging schemes for values around a meaningful midpoint, and qualitative schemes for nominal categories. It states: “Qualitative schemes are best suited to representing nominal or categorical data.” [PRIMARY SOURCE — ColorBrewer](https://colorbrewer2.org/learnmore/schemes.html)
- ColorBrewer exposes a “colorblind safe” selection mode. Use it as a filter, not as proof that every chosen color remains distinguishable over every basemap. [PRIMARY SOURCE — ColorBrewer](https://colorbrewer2.org/)
- Categorical Ohvernight layers should use hue plus at least one non-colour cue: label, icon shape, dash pattern, casing, width, texture, or direct feature selection. This follows WCAG’s color requirement. [INFERENCE — W3C](https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html)
- For lines, use a minimum visual hierarchy such as:
  - primary route: solid, wider casing plus contrasting interior;
  - secondary route: dashed or narrower;
  - uncertain or approximate geometry: distinct dash pattern plus text state;
  - selected route: increased width, high-contrast casing, and a non-colour focus indicator.
  This is an implementation inference, not a retrieved peer-reviewed measurement of which dash, casing, or width combination performs best. [INFERENCE — W3C](https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html) [INFERENCE — onX route-symbol documentation](https://www.onxmaps.com/hunt/blog/hunting-road-accessibility-research-routes-access-points)
- onX’s official documentation demonstrates practical redundancy by distinguishing vehicle classes with solid lines, hash marks, and different dash patterns. It also warns that “Conditions can vary.” This supports the design pattern, not the accuracy of Ohvernight’s classifications or any access conclusion. [PRIMARY SOURCE — onX](https://www.onxmaps.com/hunt/blog/hunting-road-accessibility-research-routes-access-points)
- Avoid red/green as the sole distinction. Use text such as “seasonal,” “unknown,” “closed,” or “operator-reported” alongside symbols. A map feature’s existence, colour, or geometry must not imply permission or availability.
- Use a stable legend that explains every line, fill, icon, dash, and uncertainty state. Layer toggles should expose the same names in accessible text.
- Do not encode a categorical layer with a sequential light-to-dark ramp unless the categories have an actual order. [PRIMARY SOURCE — ColorBrewer](https://colorbrewer2.org/learnmore/schemes.html)

## Touch and motor

- WCAG 2.2 AA requires 24 by 24 CSS-pixel pointer targets, subject to exceptions; the AAA enhanced criterion uses 44 by 44 CSS pixels. [PRIMARY SOURCE — W3C](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html) [PRIMARY SOURCE — W3C](https://www.w3.org/WAI/WCAG22/Understanding/target-size-enhanced.html)
- Apple recommends a button hit region of at least 44 by 44 points and emphasizes sufficient surrounding space and press feedback. [PRIMARY SOURCE — Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/buttons)
- Material recommends 48 by 48 dp touch targets, explains that the visual icon can be smaller than the responding area, and recommends at least 8 dp separation in many cases. [PRIMARY SOURCE — Material Design](https://m2.material.io/design/usability/accessibility.html)
- Use at least 44–48 CSS pixels for Ohvernight’s common controls, including layer toggles, zoom controls, sheet actions, close buttons, search results, and list rows. This exceeds WCAG AA and aligns better with mobile platform guidance. [INFERENCE — W3C](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html) [PRIMARY SOURCE — Apple](https://developer.apple.com/design/human-interface-guidelines/buttons) [PRIMARY SOURCE — Material Design](https://m2.material.io/design/usability/accessibility.html)
- Keep the visible line thin if cartography requires it, but provide a larger invisible interaction corridor around the line. Do not make the corridor the only representation of the feature; expose the same feature in a list or search result. [INFERENCE — W3C](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html) [PRIMARY SOURCE — Minnesota guide](https://mn.gov/mnit/assets/Accessibility%20Guide%20for%20Interactive%20Web%20Maps_tcm38-403564.pdf)
- Separate adjacent controls and avoid placing destructive or irreversible actions beside frequent map actions. This is a design inference from target-size and motor-accuracy requirements. [INFERENCE — W3C](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html)
- Provide single-tap alternatives for pinch zoom, long-press actions, and drag-only interactions. Include plus/minus buttons, “select here,” “open feature list,” and numeric or text fields where appropriate. [INFERENCE — W3C](https://www.w3.org/TR/WCAG22/)
- No retrieved standards or peer-reviewed source in this session quantified tap accuracy with gloves or wet hands. Treat outdoor conditions as a field-testing requirement, not as a solved specification. [UNKNOWN]

## Sunlight and contrast

- A 2025 mobile thematic-cartography paper states that field maps may be used away from fast internet connections and in bright sunlight, and that outdoor maps may need higher contrast. It also notes that limited-data locations may require simplification for loading. [PRIMARY SOURCE — International Cartographic Association paper](https://ica-abs.copernicus.org/articles/10/111/2025/ica-abs-10-111-2025.pdf)
- WCAG 1.4.11 applies to non-text graphics required to understand content, including meaningful lines, boundaries, markers, icons, and selected states. [PRIMARY SOURCE — W3C](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html)
- Provide a high-contrast presentation mode with:
  - subdued or simplified basemap;
  - strong casing around important lines;
  - opaque or near-opaque label halos;
  - larger labels and controls;
  - reduced visual clutter;
  - explicit “unknown” and restriction symbols;
  - preserved text and list alternatives.
  This is an inference from WCAG and field-map guidance. [INFERENCE — W3C](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html) [PRIMARY SOURCE — ICA paper](https://ica-abs.copernicus.org/articles/10/111/2025/ica-abs-10-111-2025.pdf)
- Offer both light and dark basemap options, but do not assume dark is universally best in sunlight. Reflections, display brightness, terrain detail, and label contrast determine field legibility. [INFERENCE — ICA paper](https://ica-abs.copernicus.org/articles/10/111/2025/ica-abs-10-111-2025.pdf)
- A government health-literacy guide recommends at least 16-pixel text, larger text for older adults, user-adjustable text size, and strong contrast. It recommends dark text on a very light background as generally easiest to read and using reversed-out text sparingly. [PRIMARY SOURCE — Health.gov](https://odphp.health.gov/healthliteracyonline/2016/display/full/)
- Do not rely on a dark-mode toggle alone. The high-contrast mode should also change line casing, label backgrounds, symbol size, focus treatment, and the density of visible layers.

## Screen readers and list equivalents

- The map should have a concise accessible name and description, such as “Outdoor recreation map showing trails, roads, water, land designations, and overnight-related places near the current viewport.” [INFERENCE — Minnesota guide](https://mn.gov/mnit/assets/Accessibility%20Guide%20for%20Interactive%20Web%20Maps_tcm38-403564.pdf)
- Provide a “List view” that is equivalent to the current map viewport or active filters. Each result should expose:
  - name;
  - feature type;
  - distance and direction from the current center or user location, if available;
  - geometry summary, such as “line,” “area,” or “point”;
  - relevant restrictions first;
  - operator or managing entity;
  - source and update date;
  - explicitly unknown fields;
  - an action to open the same detail sheet.
  This is an implementation inference grounded in government map guidance requiring text alternatives and list/table alternatives. [INFERENCE — Minnesota guide](https://mn.gov/mnit/assets/Accessibility%20Guide%20for%20Interactive%20Web%20Maps_tcm38-403564.pdf) [PRIMARY SOURCE — Mass.gov](https://www.mass.gov/info-details/gis-accessibility-guidance-storymaps)
- The list must not say “accessible,” “open,” “legal,” or “allowed” merely because a point, trail, road, facility, public land polygon, or map layer exists. Those statuses require separate permission evidence from the relevant agency or operator.
- Use ordinary HTML buttons, links, headings, lists, and disclosure elements for controls and results. Avoid exposing thousands of decorative tile elements as tab stops. [INFERENCE — Minnesota guide](https://mn.gov/mnit/assets/Accessibility%20Guide%20for%20Interactive%20Web%20Maps_tcm38-403564.pdf)
- Announce meaningful state changes through the detail sheet or a controlled live region: selected feature, active layer, result count, filter change, map loading, offline state, and “no results.” Avoid announcing every tile or geometry redraw. [INFERENCE — Minnesota guide](https://mn.gov/mnit/assets/Accessibility%20Guide%20for%20Interactive%20Web%20Maps_tcm38-403564.pdf)
- Keep the map itself optional for non-visual users. A user should be able to search, filter, inspect results, and read details without exploring a spatial canvas.
- Apple Maps provides a useful native pattern: VoiceOver can browse locations and pins, follow a road, open a location card, and request a description of nearby places. [PRIMARY SOURCE — Apple Support](https://support.apple.com/guide/iphone/use-voiceover-in-apps-iphe4ee74be8/ios)
- Google Maps documents keyboard map navigation, a highlighted map area, and a numbered list of places in that area. [PRIMARY SOURCE — Google Maps Help](https://support.google.com/maps/answer/6396990?hl=en-NA)
- WAI’s image-map guidance supports redundant text links for interactive regions when the visual interaction is unreliable. [PRIMARY SOURCE — W3C WAI](https://www.w3.org/WAI/tutorials/images/imagemap/)

## Low bandwidth

- MDN recommends a custom offline page instead of a generic browser error and describes service workers and the Cache API as mechanisms for reusing resources without a network connection. [PRIMARY SOURCE — MDN](https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Guides/Best_practices)
- The field-map literature identifies limited connectivity as a reason to simplify mobile thematic maps for loading. [PRIMARY SOURCE — ICA paper](https://ica-abs.copernicus.org/articles/10/111/2025/ica-abs-10-111-2025.pdf)
- Prioritize the application shell, search, current filters, detail-sheet structure, and a lightweight base layer before optional overlays. [INFERENCE — MDN](https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Guides/Best_practices) [PRIMARY SOURCE — ICA paper](https://ica-abs.copernicus.org/articles/10/111/2025/ica-abs-10-111-2025.pdf)
- Progressive loading should:
  - load visible viewport data first;
  - defer hidden layers and distant geometry;
  - simplify lines and polygons at smaller scales;
  - avoid loading all layer attributes into the initial bundle;
  - show loading progress and stale/offline state;
  - allow the user to cancel expensive layer loads.
  These are implementation inferences from offline and limited-connectivity guidance. [INFERENCE — MDN](https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Guides/Best_practices) [PRIMARY SOURCE — ICA paper](https://ica-abs.copernicus.org/articles/10/111/2025/ica-abs-10-111-2025.pdf)
- If offline data is offered, show exactly what is cached, its date, its geographic extent, and which fields may be stale. Offline availability must not be presented as current permission or current operating status.

## What outdoor apps document

| Product | Documented accessibility or field-usability feature | Relevance and limitation |
|---|---|---|
| AllTrails | AllTrails documents a “Wheelchair-friendly” trail tag based on surface, grade, width, obstacles, parking, and other criteria. It states: “there is no one-size-fits-all approach to accessibility.” [PRIMARY SOURCE — AllTrails](https://support.alltrails.com/hc/en-us/articles/360056963411-Accessibility-guide-for-wheelchair-friendly-trails) | Strong example of publishing structured accessibility attributes and caveats. AllTrails says users should check local sources and that the tag does not guarantee full ADA/ABA compliance. It is trail-use documentation, not a substitute for operator permission. |
| Gaia GPS | Gaia’s official Android/iOS accessibility search results describe larger map labels, high-contrast map layers, adjustable waypoint colors, and use of platform magnification and color-correction tools. [UNKNOWN — official Gaia pages found, direct retrieval failed](https://help.gaiagps.com/hc/en-us/articles/5624106908439-Accessibility-Settings-in-the-Android-app) [UNKNOWN — official Gaia iOS page found, direct retrieval failed](https://help.gaiagps.com/hc/en-us/articles/5437182417431-Accessibility-Settings-in-the-iOS-app) | Useful model for user-controlled label size, contrast, and symbol color. Direct page verification was unavailable in this session. |
| onX | onX documents vehicle-class line symbology, road/trail dates, surface type, managing entity, and access-point research. It warns that conditions vary and says property access may depend on the owner or local government. [PRIMARY SOURCE — onX](https://www.onxmaps.com/hunt/blog/hunting-road-accessibility-research-routes-access-points) | Strong field-uncertainty model and symbol redundancy. The documented map layer does not establish permission, and no dedicated general assistive-technology accessibility page was retrieved in this session. |
| Google Maps | Google documents screen-reader use, keyboard shortcuts, arrow-key map movement, a numbered list of places in the focused area, detailed voice guidance, and wheelchair-accessibility attributes in supported locations. [PRIMARY SOURCE — Google Maps Help](https://support.google.com/maps/answer/6396990?hl=en-NA) | Strong example of pairing spatial navigation with a list equivalent and structured accessibility attributes. Coverage and availability vary by platform and location. |
| Apple Maps | Apple documents VoiceOver exploration of locations and pins, road following, POI browsing, location cards, and a spoken description of nearby places. [PRIMARY SOURCE — Apple Support](https://support.apple.com/guide/iphone/use-voiceover-in-apps-iphe4ee74be8/ios) | Strong example of screen-reader-specific map interaction. Ohvernight should provide a simpler HTML list equivalent rather than attempting to reproduce native map gestures. |

## Twelve recommendations ranked by value for effort

1. High value / low effort — Make the detail sheet and all layer controls native, labelled HTML controls with a logical keyboard order. Preserve visible focus and ensure focus is not hidden by the sheet. [INFERENCE — W3C](https://www.w3.org/TR/WCAG22/) [PRIMARY SOURCE — Minnesota guide](https://mn.gov/mnit/assets/Accessibility%20Guide%20for%20Interactive%20Web%20Maps_tcm38-403564.pdf)

2. High value / medium effort — Build a first-class “List view” equivalent for the current viewport and active filters. Include restrictions first, source date, operator, and unknown fields. [INFERENCE — Minnesota guide](https://mn.gov/mnit/assets/Accessibility%20Guide%20for%20Interactive%20Web%20Maps_tcm38-403564.pdf) [PRIMARY SOURCE — Mass.gov](https://www.mass.gov/info-details/gis-accessibility-guidance-storymaps)

3. High value / low effort — Use 44–48 CSS pixels for common controls and add hit-slop around narrow visible lines, points, and icons. Keep adjacent targets separated. [INFERENCE — W3C](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html) [PRIMARY SOURCE — Apple](https://developer.apple.com/design/human-interface-guidelines/buttons) [PRIMARY SOURCE — Material Design](https://m2.material.io/design/usability/accessibility.html)

4. High value / medium effort — Add non-drag and non-pinch alternatives: plus/minus zoom, arrow-key panning, “search this area,” direct feature-list selection, and accessible range controls. [INFERENCE — W3C](https://www.w3.org/TR/WCAG22/)

5. High value / medium effort — Replace colour-only layer semantics with labels, icons, dash patterns, casing, width, or textures. Apply ColorBrewer’s colorblind-safe filter and test the chosen palette over every basemap. [PRIMARY SOURCE — ColorBrewer](https://colorbrewer2.org/) [INFERENCE — W3C](https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html)

6. High value / low effort — Add a persistent legend that names every symbol, line style, fill, focus state, uncertainty state, and restriction state. Make the legend keyboard and screen-reader accessible. [INFERENCE — W3C](https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html) [PRIMARY SOURCE — Minnesota guide](https://mn.gov/mnit/assets/Accessibility%20Guide%20for%20Interactive%20Web%20Maps_tcm38-403564.pdf)

7. High value / medium effort — Implement a high-contrast field mode that simplifies the basemap, strengthens line casing, increases label size, adds label halos, and reduces visible layer density. [INFERENCE — W3C](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html) [PRIMARY SOURCE — ICA paper](https://ica-abs.copernicus.org/articles/10/111/2025/ica-abs-10-111-2025.pdf)

8. High value / medium effort — Make the detail sheet reflow at narrow widths and remain usable with 200% text zoom, larger system fonts, text spacing, and browser zoom. [PRIMARY SOURCE — W3C WCAG 2.2](https://www.w3.org/TR/WCAG22/) [PRIMARY SOURCE — Health.gov](https://odphp.health.gov/healthliteracyonline/2016/display/full/)

9. High value / medium effort — Expose meaningful state changes through a restrained live region: selected feature, result count, active layers, loading, offline mode, and no-result states. [INFERENCE — Minnesota guide](https://mn.gov/mnit/assets/Accessibility%20Guide%20for%20Interactive%20Web%20Maps_tcm38-403564.pdf)

10. High value / medium effort — Add progressive loading and an offline-capable shell. Cache the application shell and explicitly show cached extent, data date, and stale fields. [PRIMARY SOURCE — MDN](https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Guides/Best_practices) [INFERENCE — ICA paper](https://ica-abs.copernicus.org/articles/10/111/2025/ica-abs-10-111-2025.pdf)

11. Medium value / low effort — Set a readable default body size, use relative units, allow user-controlled type scaling, and keep labels from becoming the only route to understanding a feature. [PRIMARY SOURCE — Health.gov](https://odphp.health.gov/healthliteracyonline/2016/display/full/) [PRIMARY SOURCE — W3C WCAG 2.2](https://www.w3.org/TR/WCAG22/)

12. High value / medium effort — Test end-to-end with keyboard-only navigation, VoiceOver, TalkBack, browser zoom, high-contrast settings, colour-vision simulation, bright sunlight, older users, motor-impaired users, gloves, wet screens, and intermittent connectivity. Record failures by feature type rather than only by page. [INFERENCE — Leaflet accessibility guidance](https://leafletjs.com/examples/accessibility/) [PRIMARY SOURCE — Minnesota guide](https://mn.gov/mnit/assets/Accessibility%20Guide%20for%20Interactive%20Web%20Maps_tcm38-403564.pdf)

## Unknowns

- UNKNOWN — Ohvernight’s current implementation was not inspected in this research session, so its present WCAG conformance is unknown.
- UNKNOWN — No peer-reviewed or standards-based measurement of dash pattern, casing, and line-width combinations was retrieved within the 20-search limit. The recommendation to combine them is an inference from WCAG and documented map practice.
- UNKNOWN — No retrieved standards or peer-reviewed source quantified the effect of gloves or wet hands on Ohvernight’s target sizes or Leaflet interactions. Field testing is required.
- UNKNOWN — The UK GDS article “Why you need to make your maps accessible” was found in official search results, but direct page retrieval failed in this session. [UK GDS page](https://services.blog.gov.uk/2023/02/22/why-you-need-to-make-your-maps-accessible/)
- UNKNOWN — Leaflet’s accessibility page and reference documentation, Esri’s JavaScript accessibility page, Mapbox’s iframe documentation, and Gaia GPS accessibility pages were found through official publisher-domain results, but direct extraction failed in this session. Their snippets were not treated as decisive requirements. [Leaflet](https://leafletjs.com/examples/accessibility/) [Esri](https://developers.arcgis.com/javascript/latest/accessibility/) [Mapbox](https://docs.mapbox.com/help/glossary/iframe/) [Gaia GPS](https://help.gaiagps.com/hc/en-us/articles/5624106908439-Accessibility-Settings-in-the-Android-app)
- UNKNOWN — No dedicated general assistive-technology accessibility documentation for onX was retrieved in this session. The onX material retrieved documents field data, symbols, conditions, and access uncertainty rather than an accessibility audit.
- UNKNOWN — App documentation describes intended features, not independent accessibility conformance or real-world reliability.
- UNKNOWN — A map layer, road, trail, ramp, facility, public-ownership polygon, stocking record, designation, or community report does not establish permission or an allowed activity.

## Recommendation

Adopt WCAG 2.2 Level AA as Ohvernight’s product target, with 44–48 CSS-pixel controls as the mobile baseline. Make the list/detail experience a complete alternative to spatial tapping, put restrictions and source dates before discovery content, and treat every access or activity status as unknown unless supported by permission language on the relevant agency or operator page. Prioritize recommendations 1–6 before adding more map layers.
