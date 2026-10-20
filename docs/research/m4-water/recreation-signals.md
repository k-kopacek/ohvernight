# Official recreation information

What official sources can say about fishing, boating, paddling, swimming and
restrictions, and how safely each can be attached to a water feature.
Detail: Hermes [track C](hermes/track-c-recreation-signals.md).

## Three different kinds of statement

Official sources say three different things, and they must not be merged:

| Kind | Example | What it establishes | What it does not |
|---|---|---|---|
| Designation | CPW Gold Medal segment; special-regulation water | The agency classifies this water this way | That a person may reach it or fish from any bank |
| Facility | A boat ramp point; a river access point; an inspection station | The facility exists at that location | That the whole waterbody is open, or the facility is open today |
| Permission or restriction | "Boating regulations: Not permitted" (Denver Water, Strontia Springs) | What the operator allows or prohibits at this water | Anything about another activity or another water |

Only the third kind is a claim about permission. In the data contract it is
a claim object with `supported` or `restricted` status, a source URL, a
scope and a review basis. Designations and facilities are source facts about
existence.

## How each can be attached

| Relationship | Key | Risk |
|---|---|---|
| Operator page → named waterbody | Name and operator, by a person | Low when done by hand; one record at a time |
| Ramp or access point → waterbody or stream | Distance to the nearest water, then reviewed | Medium: a point near two waters; a ramp does not open a whole lake |
| Gold Medal segment → stream | Geometry overlap with the grouped stream; endpoints are prose | Medium: only part of a stream is designated |
| Fishing Atlas water code → waterbody | Water code, if the fields allow | Unknown until the field schema is read |
| USFS recreation area → water | Point to nearest water | High for anything beyond "a recreation site is near here" |

A spatial join yields a derived fact: "this facility is within N metres of
this water". It is not a statement by the source about the water.

## Restricted waters found

These are the cases where showing water as a place to recreate, with nothing
else, would mislead:

| Water | Official restriction | Source |
|---|---|---|
| Cheesman Lake | All boating and camping prohibited; water-contact sports prohibited; fishing only on the Goose Creek Arm; foot access only | Denver Water (re-read by the coordinator) |
| Strontia Springs Reservoir and Waterton Canyon | Boating not permitted; canoeing, kayaking, tubing and rafting prohibited; body contact with water prohibited | Denver Water (re-read by the coordinator) |
| Chatfield Lake | Closed to all boats and paddlecraft 1 December to ice-off | CPW (Hermes) |
| Rueter-Hess Reservoir | Recreation by reservation on set days only; craft and fishing limits | Douglas County (Hermes) |
| North Star (Roaring Fork) | Launching or taking out at North Star Beach prohibited for commercial use; low-water closures | Pitkin County (Hermes; a commercial permit document) |

Restrictions change. Under the data contract a stale restriction stays in
force and is flagged for review; a stale supported claim becomes unknown.

## Unknown

- Fishing Atlas field schemas and whether a water code joins cleanly.
- Recreation status of Grizzly Reservoir, Wildcat Reservoir, Maroon Lake
  (water use), Aurora-Rampart Reservoir.
- Reuse terms for CPW inspection stations, Pitkin County points and operator
  prose.
- Any statewide dataset of public water access points.
