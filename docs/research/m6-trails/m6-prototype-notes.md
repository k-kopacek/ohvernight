# M6 motorized-evidence prototype

This isolated pure-Python prototype shows how one Forest Service MVUM route record can retain vehicle-specific designation text alongside losslessly preserved `Dates Open` text. It parses only the month/day forms observed in the saved Package 4 road and trail samples, including two comma-separated windows and year-wrapping ranges. Unsupported or malformed strings stay verbatim and produce `UNPARSEABLE`; the prototype does not infer a replacement range.

An optional trail management-intent record is carried as a second source claim. A normalized route-number equality produces only a join candidate; it does not resolve disagreements between source fields. The record's `current_condition` is always the string `unknown`. The date lookup reports `INSIDE_WINDOW`, `OUTSIDE_WINDOW`, `NO_WINDOW_STATED`, or `UNPARSEABLE`; its docstring limits this to a legal-designation lookup, not permission, openness, or rideability.

The prototype deliberately does not decide source precedence, current legal status, seasonal orders, closures, route continuity, whether two different source IDs truly identify the same trail, or physical conditions. It has no production imports and is outside the pipeline's test discovery. The seven-record fixture is trimmed and geometry-free; it is not a production sample or an assertion that its records join to the canonical Aspen trails.

Run from `v2/pipeline/prototypes/m6/` with:

```sh
python3 -m unittest discover -s tests -v
```
