# M4-B iPhone acceptance checks

Prepared in advance. The owner's iPhone Safari pass is release evidence for
M4-B, as for M3. iPad and Android remain unverified unless separately tested.
Every cell starts UNVERIFIED. Open `/v2/?region=aspen&view=map` and
`/v2/?region=douglas-co&view=map`.

| # | Action | Expected | Aspen | Douglas |
|---|---|---|---|---|
| 1 | Look at the map at the default zoom | Far fewer water lines than before; no canals or ditches; rivers read as continuous | UNVERIFIED | UNVERIFIED |
| 2 | Tap a river on the line | The whole river highlights (thicker, light halo, dark edge) along its length; other streams fade; detail opens at the partial height | UNVERIFIED | UNVERIFIED |
| 3 | Tap the same river somewhere else along it | The same river is selected; the detail does not change | UNVERIFIED | UNVERIFIED |
| 4 | Zoom in until names show; tap a river's name | Selects that river; one name per river in view, not one per piece | UNVERIFIED | UNVERIFIED |
| 5 | Zoomed in on a short creek, tap it | The map fits the creek, as trails do | UNVERIFIED | UNVERIFIED |
| 6 | Zoomed in on a long river (Roaring Fork; East Plum Creek), tap it | The map does not jump far out; where you tapped stays in view | UNVERIFIED | UNVERIFIED |
| 7 | Search for a river by name and select it | The map moves to the river without falling back to a whole-region view | UNVERIFIED | UNVERIFIED |
| 8 | Tap a lake or reservoir | Stronger tint, neighbours fade, no outline; the map does not move; detail opens | UNVERIFIED | UNVERIFIED |
| 9 | Read a river's detail | "From the source": River or stream; Perennial; a number of source segments; agency and source link; the limitation sentence. "Computed by Ohvernight": a length. Then "Mapped water. Access and allowed activities are not established." Last line: the permission disclaimer | UNVERIFIED | UNVERIFIED |
| 10 | Read a named lake's detail | Lake or pond; Perennial; an area in hectares; the same two closing lines | UNVERIFIED | UNVERIFIED |
| 11 | Douglas: open Rueter-Hess Reservoir | Reservoir; "Hydrographic category not stated by the source"; no "Perennial" | — | UNVERIFIED |
| 12 | Open an unnamed lake | Title "Unnamed lake" | UNVERIFIED | UNVERIFIED |
| 13 | Look for anything about fishing, boating, paddling or swimming | Nothing in M4-B: no activity lines, icons or colours | UNVERIFIED | UNVERIFIED |
| 14 | Layers drawer, water rows | Two rows in each region (streams; lakes and reservoirs) with the limitation sentence and On / Off | UNVERIFIED | UNVERIFIED |
| 15 | Aspen: alpine lakes near Maroon Bells and Independence Pass | Named lakes present; judge whether an unnamed lake you expect is missing (the 2 hectare threshold) | UNVERIFIED | — |
| 16 | Douglas: Chatfield, Cheesman, Strontia Springs, Rueter-Hess, South Platte River | All present; the South Platte is continuous through Waterton Canyon | — | UNVERIFIED |
| 17 | Douglas: detention and "Franktown Parker" reservoirs | Mostly gone; note any that remain | — | UNVERIFIED |
| 18 | Tap empty map with a river selected; pan; pinch; + and −; rotate to landscape | Unchanged from M3 | UNVERIFIED | UNVERIFIED |
| 19 | Slow reload | Map and pins first; water arrives with its own status; nothing blocks the map | UNVERIFIED | UNVERIFIED |

Known limitations carried from M3 and not to be re-tested as failures:
double-tap map zoom on Safari; map rotation; a chooser for overlapping
features.
