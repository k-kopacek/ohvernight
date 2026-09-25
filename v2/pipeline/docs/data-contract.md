# Evidence contract

Ownership, road designation, actual road conditions, permission to sleep in a selected vehicle, restrictions, stay limits and seasonal rules are independent facts. An official source establishes provenance, not blanket trip approval.

Each fact needs a status, source URL, scope, last_checked_at, last_confirmed_at and a freshness threshold. Unknown facts remain unknown. A successful fetch advances last_checked_at only. Manual interpretation or a validated structured field can advance last_confirmed_at for that fact alone. A page hash never confirms a fire stage. Coverage gaps never imply private ownership or no restrictions.

Transport states: available, unavailable, skipped. Interpretation states: unknown, supported, restricted. Freshness states: current, stale, unavailable. These are separate dimensions: a restriction can still be in force even when its source is stale. Effective dates and geographic jurisdiction also apply; a fresh page does not validate future trip dates.

Initial freshness thresholds are product review policies, not agency guarantees: fire/closures 24 hours, RIDB facility inventory 7 days, manually reviewed ordinary site rules 30 days. The browser recomputes age on load and during use so preserved data visibly ages. Never reset a confirmation date merely because another layer refreshed.

`config/rules-registry.json` stores independently reviewed site exceptions. Match exact place IDs or reviewed road names. Matching a corridor adds review context only, never a permission grant. Do not inherit an assumed forest-wide 14-day limit. An unresolved or stale rule remains visible as needing confirmation. Lincoln Creek's published day limit does not establish a precise check-in/check-out counting policy.

Generated polygons remain `needs_review: true`, `camping_permission: unknown`, and never create point campsites. MVUM and candidate snapshots are tied to their evaluated trip. The browser hides trip-specific layers when dates or vehicle differ.

BLM native polygon conversion preserves ring holes and islands using even/odd filling and repairs invalid topology with Shapely. The source is generalized management context; county parcel precision and campsite legality cannot be inferred from that repair.
