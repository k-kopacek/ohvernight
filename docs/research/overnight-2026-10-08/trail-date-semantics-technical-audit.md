DRAFT - UNREVIEWED TECHNICAL AUDIT (main bb85785)

# TRAIL DATE SEMANTICS AUDIT (technical half)

Scope: how the app turns USFS trail-use date strings into "Within / Outside published use dates" for a trip. Read-only audit of `main` at `bb85785` (checkout `m3-foundation`), offline. All counts were computed from the committed data with throwaway scripts in `/tmp/ohv-audit`, and the verdicts were produced by running the real `v2/explore/trail-seasons.js` and `v2/trail-discovery.js` under Node against the published display file. This report does not say what the source fields mean; that is the research worker's half. Statements about meaning below are labelled INFERENCE.

## 1. Summary

- The "40 of 76" figure reproduces exactly for motorcycling on 2026-10-10 to 2026-10-11: 76 segments are listed by the finder, 40 get "Outside published use dates", 36 get "Within published use dates — closures unchecked". A further 26 segments are not listed (they evaluate to "Published restriction overlaps trip").
- The 40 are: 38 segments whose only motorcycle string is `accpt = 12/01-03/14`, plus 2 whose only motorcycle string is `managed = 12/01-03/14`.
- The verdict is driven by the union of `managed` and `accpt`, read as "the dates on which the use is published". Any trip day not inside that union is "Outside". Dates the source does not mention are therefore treated as outside, not as unknown.
- In Douglas no segment has more than one of the four fields populated for any activity (0 of 918 activity cells). So "outside" is always derived from a single partial-year string plus silence for the rest of the year.
- The source's own `allowed_terra_use` code contains the digit 4 on all 76 listed segments, including all 40 marked outside, and on none of the 26 restricted ones. INFERENCE: the source treats motorcycles as an allowed use on those 40 segments in some sense; the data does not say in which months.
- The verdict is enabled only for Douglas County (`trail_season_check: true`). Aspen shows the raw strings only.
- `v2/pipeline/TRAIL-PILOT.md` says the interface "does not resolve contradictory records or evaluate dates", and the shared detail panel prints "These are source records, not a check for your trip dates." The Douglas browse module evaluates dates anyway, in the same panel.
- Recommendation: suppress the within/outside verdict and show the raw strings as unknown (option C in section 9) until the research half establishes the field meanings. Not implemented.

## 2. Source service and field mapping

Service: `https://apps.fs.usda.gov/arcx/rest/services/EDW/EDW_TrailNFSPublishWithDataStatus_01/MapServer`, layer 0 (`v2/pipeline/scripts/fetch_trails.py:8`). Douglas reuses the same URL and the same `normalize` function (`v2/pipeline/scripts/fetch_douglas.py:8`, `:56`).

Fetch: `query_layer_geojson` (`v2/pipeline/scripts/lib/arcgis_client.py:95`) requests `outFields=*` (`:95`, `:126`, `:130-131`), so every attribute is retrieved and all but the ones below are dropped. Attribute names are lower-cased by `properties()` (`v2/pipeline/scripts/lib/common.py:25-26`), so matching is case-insensitive.

| stored property | raw source attribute (case-insensitive) | code |
|---|---|---|
| `id` | `usfs-trail-` + `OBJECTID` | `fetch_trails.py:27` |
| `name` | `TRAIL_NAME` | `:27` |
| `trail_number` | `TRAIL_NO` | `:28` |
| `surface` | `TRAIL_SURFACE` | `:28` |
| `attribute_subset` | `ATTRIBUTESUBSET` | `:29` |
| `allowed_terra_use` | `ALLOWED_TERRA_USE` | `:30` |
| `activities.<key>.managed` | `<PREFIX>_MANAGED` | `:23-25` |
| `activities.<key>.accpt` | `<PREFIX>_ACCPT` | `:23-25` |
| `activities.<key>.disc` | `<PREFIX>_DISC` | `:23-25` |
| `activities.<key>.restricted` | `<PREFIX>_RESTRICTED` | `:23-25` |

Prefixes (`fetch_trails.py:9-15`): hiking `HIKER_PEDESTRIAN`, horseback_riding `PACK_SADDLE`, mountain_biking `BICYCLE`, motorcycling `MOTORCYCLE`, atv `ATV`, four_wheel_drive `FOURWD`, snowshoeing `SNOWSHOE`, cross_country_skiing `XCOUNTRY_SKI`, snowmobiling `SNOWMOBILE`.

Points to hand to the research worker:

- There is no handling of a combined `*_ACCPT_DISC` attribute anywhere in the repository (grep for `accpt_disc` returns nothing). The code reads `<PREFIX>_ACCPT` and `<PREFIX>_DISC` as two attributes. The committed data has non-null values in both `accpt` and `disc` (for example Douglas hiking `disc` on 57 segments, motorcycling `accpt` on 60), so the response evidently carried two separate attributes when it was fetched. I could not confirm the live field list offline.
- The activity attributes are not validated. `required_fields` is `objectid, trail_name, trail_no` for Aspen (`fetch_trails.py:35`) and `objectid` only for Douglas (`fetch_douglas.py:59`). If the service renamed an activity attribute, every value would silently become null and the app would show "Use permission unknown".
- The committed files were added by upload commits (`git log` for `fetch_trails.py`: `4c3917d`, `41367ce` "Add files via upload"), so the repository does not prove the data was produced by the current code. The retrieval timestamps are Aspen `2026-09-25T21:32:09Z` and Douglas `2026-09-27T14:05:56Z`.

## 3. Normalisation

All of it is one expression, `fetch_trails.py:23-25`: `p.get(f'{prefix}_{suffix}') or None`.

- Empty string and missing attribute both become `null`. Comment at `:22`: "Keep published date/rule strings verbatim. Missing is unknown, never allowed."
- No trimming, casing, splitting or date parsing happens in the pipeline. Trailing spaces survive: `"01/01-12/31 "` appears on 2 Douglas and 78 Aspen activity cells.
- A whitespace-only string would be kept (truthy in Python). None exists in either file.
- Geometry is clipped to the boundary (`fetch_trails.py:19`); attributes are per source segment (OBJECTID), not per trail. Douglas has 102 segments covering 78 distinct trail numbers.
- The display artifact loaded by the browser (`v2/regions/douglas-co/display/trails.geojson`) carries the same activity values: 0 differences across 102 Douglas and 123 Aspen segments.
- The regional contract checks shape only: rule R29 (`v2/pipeline/docs/data-contract.md:259`, `v2/pipeline/scripts/lib/region_contract.py:708`) requires exactly the nine activity keys and the four sub-keys, each null or a string.

## 4. Verdict logic

`v2/explore/trail-seasons.js`.

Parsing, `windows(text)` (`:3-10`):

- Falsy input returns `null` (`:4`).
- The string is split on `;` or `,` (`:5`). Each part is trimmed and must match `M/D - M/D` with one or two digits, a hyphen or en dash and optional spaces (`:6`). Each month/day must be a real calendar date in a leap year, so `02/29` is accepted and `13/01` or `02/30` is rejected (`:7`).
- One unparseable part makes the whole string `null` (`:6`). A trailing separator does that too: `"12/01-03/14;"` returns `null`.
- A range is stored as two `MMDD` integers (`:8`). There is no year.

Coverage, `covers(ranges, day)` (`:11`): inclusive at both ends. If start is after end the range wraps the year: `day >= start || day <= end`. So `12/01-03/14` covers 1 December to 14 March and nothing else.

Trip days, `days(start, end)` (`:12-16`): both must be valid `YYYY-MM-DD`, end not before start, span at most 366 days; every day from start to end inclusive is checked.

Verdict, `season(feature, activity, start, end)` (`:17-25`), in this order:

| step | condition | user-visible string | line |
|---|---|---|---|
| 1 | trip dates invalid | `Choose valid trip dates` | `:18` |
| 2 | `restricted` parses and any trip day is inside it | `Published restriction overlaps trip` | `:19` |
| 3 | `restricted` is non-empty and does not parse | `Restriction needs review` | `:20` |
| 4 | `managed` and `accpt` both empty | `Use permission unknown` | `:21` |
| 5 | `managed` or `accpt` non-empty and does not parse | `Use dates need review` | `:22` |
| 6 | any trip day is in neither `managed` nor `accpt` | `Outside published use dates` | `:23` |
| 7 | `disc` non-empty | `Published use discouraged — review` | `:24` |
| 8 | otherwise | `Within published use dates — closures unchecked` | `:24` |

Consequences, each checked by running the function:

- `managed` and `accpt` are interchangeable and combined as a union. `{managed: 01/01-12/31, accpt: 12/01-03/14}` gives "Within" in October.
- `disc` is never parsed or compared with the trip. Any non-empty `disc` changes "Within" to "discouraged" whatever its dates, and a segment with only `disc` gives "Use permission unknown" (57 Douglas hiking segments).
- `"N/A"` or any other text gives "Use dates need review" or "Restriction needs review". Empty or null is treated as absent.
- Multiple ranges work when separated by `,` or `;` (Aspen `01/01-06/14,10/16-12/31` parses to two ranges).
- A one-day trip and a two-day trip give the same counts for 10 October; the verdict is "Outside" if any single day is uncovered.

Where it is shown (`v2/explore/browse.js`):

- Finder row: a `<span>` with the verdict under each trail result when an activity is selected (`:34`).
- Finder membership: `T.matches` lists a segment for an activity only if `managed` or `accpt` is non-empty (`v2/trail-discovery.js:7`). Restricted-only and `disc`-only segments are not listed.
- Detail panel: heading with the activity label, then the verdict paragraph (`:48`); then the raw strings as `Dirt biking: Accepted use: 12/01-03/14` using the labels `Managed use`, `Accepted use`, `Discouraged`, `Restricted` (`:49`); then "These source dates can be incomplete or surprising. Verify the current motor-vehicle map and agency alerts. No difficulty, width, direction or bike-registration eligibility has been verified." (`:50`).
- Filter note: "Dates check published trail seasons, not live closures." (`:30`).
- Defaults: trip dates are today and tomorrow (`:15-16`) and the Douglas default activity is `motorcycling` (`v2/regions/douglas-co/explore.json`, `trip_defaults`). A first-time visitor in October sees the 40 "Outside" rows without choosing anything.
- The same panel also contains the shared evidence block (`v2/explore/evidence.js:50-57`), which lists every activity's raw strings under "Published activity dates" with the sentence "These are source records, not a check for your trip dates. Blank records mean unknown." That sentence and the verdict contradict each other on one screen.

No region `explore.json` holds season rules; the only configuration is the capability flag.

## 5. Raw value distribution

Counts are segments. Every activity has four fields; "(null)" rows complete each field to the layer total.

### 5.1 Douglas County (`v2/regions/douglas-co/research.json`, `/layers/trails`, 102 segments)

| activity | field | raw value (verbatim, quotes show trailing spaces) | segments |
|---|---|---|---|
| hiking | managed | `"01/01-12/31"` | 13 |
| hiking | managed | `"06/16-03/31"` | 5 |
| hiking | managed | (null) | 84 |
| hiking | accpt | (null) | 102 |
| hiking | disc | `"01/01-12/31"` | 15 |
| hiking | disc | `"05/16-11/30"` | 1 |
| hiking | disc | `"06/01-03/31"` | 1 |
| hiking | disc | `"06/01-11/30"` | 1 |
| hiking | disc | `"12/01-03/14"` | 39 |
| hiking | disc | (null) | 45 |
| hiking | restricted | (null) | 102 |
| horseback_riding | managed | `"01/01-12/31"` | 11 |
| horseback_riding | managed | `"06/16-03/31"` | 4 |
| horseback_riding | managed | (null) | 87 |
| horseback_riding | accpt | `"06/16-03/31"` | 1 |
| horseback_riding | accpt | (null) | 101 |
| horseback_riding | disc | `"01/01-12/31"` | 15 |
| horseback_riding | disc | `"05/16-11/30"` | 1 |
| horseback_riding | disc | `"06/01-03/31"` | 1 |
| horseback_riding | disc | `"06/01-11/30"` | 1 |
| horseback_riding | disc | `"12/01-03/14"` | 39 |
| horseback_riding | disc | (null) | 45 |
| horseback_riding | restricted | (null) | 102 |
| mountain_biking | managed | `"01/01-12/31"` | 12 |
| mountain_biking | managed | `"06/16-03/31"` | 5 |
| mountain_biking | managed | (null) | 85 |
| mountain_biking | accpt | (null) | 102 |
| mountain_biking | disc | `"01/01-12/31"` | 15 |
| mountain_biking | disc | `"05/16-11/30"` | 1 |
| mountain_biking | disc | `"06/01-03/31"` | 1 |
| mountain_biking | disc | `"06/01-11/30"` | 1 |
| mountain_biking | disc | `"12/01-03/14"` | 39 |
| mountain_biking | disc | (null) | 45 |
| mountain_biking | restricted | `"01/01-12/31 "` | 2 |
| mountain_biking | restricted | (null) | 100 |
| motorcycling | managed | `"01/01-12/31"` | 13 |
| motorcycling | managed | `"06/01-03/31"` | 1 |
| motorcycling | managed | `"12/01-03/14"` | 2 |
| motorcycling | managed | (null) | 86 |
| motorcycling | accpt | `"01/01-12/31"` | 20 |
| motorcycling | accpt | `"05/16-11/30"` | 1 |
| motorcycling | accpt | `"06/01-11/30"` | 1 |
| motorcycling | accpt | `"12/01-03/14"` | 38 |
| motorcycling | accpt | (null) | 42 |
| motorcycling | disc | (null) | 102 |
| motorcycling | restricted | `"01/01-12/31"` | 26 |
| motorcycling | restricted | (null) | 76 |
| atv | managed | `"01/01-12/31"` | 11 |
| atv | managed | `"05/16-11/30"` | 1 |
| atv | managed | `"06/01-11/30"` | 1 |
| atv | managed | `"12/01-03/14"` | 38 |
| atv | managed | (null) | 51 |
| atv | accpt | `"01/01-12/31"` | 13 |
| atv | accpt | (null) | 89 |
| atv | disc | (null) | 102 |
| atv | restricted | `"01/01-12/31"` | 38 |
| atv | restricted | (null) | 64 |
| four_wheel_drive | managed | `"01/01-12/31"` | 13 |
| four_wheel_drive | managed | (null) | 89 |
| four_wheel_drive | accpt | (null) | 102 |
| four_wheel_drive | disc | (null) | 102 |
| four_wheel_drive | restricted | `"01/01-12/31"` | 89 |
| four_wheel_drive | restricted | (null) | 13 |
| snowshoeing | managed | (null) | 102 |
| snowshoeing | accpt | (null) | 102 |
| snowshoeing | disc | (null) | 102 |
| snowshoeing | restricted | (null) | 102 |
| cross_country_skiing | managed | (null) | 102 |
| cross_country_skiing | accpt | (null) | 102 |
| cross_country_skiing | disc | (null) | 102 |
| cross_country_skiing | restricted | (null) | 102 |
| snowmobiling | managed | (null) | 102 |
| snowmobiling | accpt | (null) | 102 |
| snowmobiling | disc | (null) | 102 |
| snowmobiling | restricted | (null) | 102 |

### 5.2 Aspen (`v2/trails.geojson`, the manifest path for the Aspen `trails` layer, 123 segments)

| activity | field | raw value (verbatim, quotes show trailing spaces) | segments |
|---|---|---|---|
| hiking | managed | `"01/01-12/31"` | 12 |
| hiking | managed | `"06/01-10/31"` | 3 |
| hiking | managed | `"06/15-10/15"` | 6 |
| hiking | managed | `"06/21-05/14"` | 2 |
| hiking | managed | (null) | 100 |
| hiking | accpt | `"01/01-06/14,10/16-12/31"` | 3 |
| hiking | accpt | `"01/01-12/31"` | 59 |
| hiking | accpt | (null) | 61 |
| hiking | disc | `"01/01-12/31"` | 1 |
| hiking | disc | (null) | 122 |
| hiking | restricted | (null) | 123 |
| horseback_riding | managed | `"01/01-12/31"` | 63 |
| horseback_riding | managed | `"06/01-10/31"` | 7 |
| horseback_riding | managed | (null) | 53 |
| horseback_riding | accpt | `"01/01-12/31"` | 27 |
| horseback_riding | accpt | `"06/15-10/15"` | 6 |
| horseback_riding | accpt | (null) | 90 |
| horseback_riding | disc | `"01/01-12/31"` | 2 |
| horseback_riding | disc | (null) | 121 |
| horseback_riding | restricted | `"01/01-12/31 "` | 5 |
| horseback_riding | restricted | (null) | 118 |
| mountain_biking | managed | `"01/01-12/31"` | 3 |
| mountain_biking | managed | `"05/21-11/22"` | 25 |
| mountain_biking | managed | `"06/21-05/14"` | 2 |
| mountain_biking | managed | (null) | 93 |
| mountain_biking | accpt | `"01/01-12/31"` | 1 |
| mountain_biking | accpt | `"05/12-11/22"` | 1 |
| mountain_biking | accpt | `"05/21-11/22"` | 3 |
| mountain_biking | accpt | (null) | 118 |
| mountain_biking | disc | (null) | 123 |
| mountain_biking | restricted | `"01/01-12/31"` | 8 |
| mountain_biking | restricted | `"01/01-12/31 "` | 72 |
| mountain_biking | restricted | (null) | 43 |
| motorcycling | managed | (null) | 123 |
| motorcycling | accpt | (null) | 123 |
| motorcycling | disc | (null) | 123 |
| motorcycling | restricted | `"01/01-12/31"` | 119 |
| motorcycling | restricted | (null) | 4 |
| atv | managed | (null) | 123 |
| atv | accpt | (null) | 123 |
| atv | disc | (null) | 123 |
| atv | restricted | `"01/01-12/31"` | 119 |
| atv | restricted | (null) | 4 |
| four_wheel_drive | managed | (null) | 123 |
| four_wheel_drive | accpt | (null) | 123 |
| four_wheel_drive | disc | (null) | 123 |
| four_wheel_drive | restricted | `"01/01-12/31"` | 119 |
| four_wheel_drive | restricted | (null) | 4 |
| snowshoeing | managed | (null) | 123 |
| snowshoeing | accpt | (null) | 123 |
| snowshoeing | disc | (null) | 123 |
| snowshoeing | restricted | (null) | 123 |
| cross_country_skiing | managed | `"01/01-12/31"` | 3 |
| cross_country_skiing | managed | `"11/15-05/30"` | 1 |
| cross_country_skiing | managed | (null) | 119 |
| cross_country_skiing | accpt | (null) | 123 |
| cross_country_skiing | disc | (null) | 123 |
| cross_country_skiing | restricted | (null) | 123 |
| snowmobiling | managed | (null) | 123 |
| snowmobiling | accpt | (null) | 123 |
| snowmobiling | disc | (null) | 123 |
| snowmobiling | restricted | `"01/01-12/31"` | 3 |
| snowmobiling | restricted | `"01/01-12/31 "` | 1 |
| snowmobiling | restricted | (null) | 119 |

## 6. Motorcycling, every Douglas segment, verdict for 2026-10-10

Verdicts are identical for the two-day trip 2026-10-10 to 2026-10-11. Sorted by finder membership, then verdict, then name.

| name | trail no. | id | managed | accpt | disc | restricted | in finder (motorcycling) | verdict 2026-10-10 |
|---|---|---|---|---|---|---|---|---|
| 662 | 0662 | usfs-trail-8964124 | - | 12/01-03/14 | - | - | listed | Outside published use dates |
| 673.A | 0673.A | usfs-trail-8959897 | - | 12/01-03/14 | - | - | listed | Outside published use dates |
| 681.B | 0681.B | usfs-trail-8960182 | - | 12/01-03/14 | - | - | listed | Outside published use dates |
| 681.C | 0681.C | usfs-trail-8973245 | - | 12/01-03/14 | - | - | listed | Outside published use dates |
| 681.E | 0681.E | usfs-trail-8971356 | - | 12/01-03/14 | - | - | listed | Outside published use dates |
| 682.AA | 0682.AA | usfs-trail-8941276 | - | 12/01-03/14 | - | - | listed | Outside published use dates |
| 787 | 0787 | usfs-trail-8939494 | - | 12/01-03/14 | - | - | listed | Outside published use dates |
| 787 | 0787 | usfs-trail-8954929 | - | 12/01-03/14 | - | - | listed | Outside published use dates |
| 787.A | 0787.A | usfs-trail-8958080 | - | 12/01-03/14 | - | - | listed | Outside published use dates |
| 788 | 0788 | usfs-trail-8937987 | - | 12/01-03/14 | - | - | listed | Outside published use dates |
| ARROWHEAD | 0646 | usfs-trail-8970427 | - | 12/01-03/14 | - | - | listed | Outside published use dates |
| BARR | 0673 | usfs-trail-8966777 | - | 12/01-03/14 | - | - | listed | Outside published use dates |
| BARR | 0673 | usfs-trail-8982529 | - | 12/01-03/14 | - | - | listed | Outside published use dates |
| BEAVER | 0688 | usfs-trail-8978422 | - | 12/01-03/14 | - | - | listed | Outside published use dates |
| BEGINNER | 0627 | usfs-trail-8968192 | - | 12/01-03/14 | - | - | listed | Outside published use dates |
| BEGINNER | 0627 | usfs-trail-8982355 | - | 12/01-03/14 | - | - | listed | Outside published use dates |
| CABIN RIDGE | 0675 | usfs-trail-8964041 | - | 12/01-03/14 | - | - | listed | Outside published use dates |
| DEVILS HEAD SPUR | 0679.A | usfs-trail-8965397 | - | 12/01-03/14 | - | - | listed | Outside published use dates |
| FERN | 683 | usfs-trail-8967882 | 12/01-03/14 | - | - | - | listed | Outside published use dates |
| FLATROCK | 0674 | usfs-trail-8971354 | - | 12/01-03/14 | - | - | listed | Outside published use dates |
| GARBER | 0686 | usfs-trail-8993725 | - | 12/01-03/14 | - | - | listed | Outside published use dates |
| GARBER CUTOFF | 0686.A | usfs-trail-8977986 | - | 12/01-03/14 | - | - | listed | Outside published use dates |
| GRAMPS | 0657 | usfs-trail-8972062 | - | 12/01-03/14 | - | - | listed | Outside published use dates |
| LONG HOLLOW | 0650 | usfs-trail-8970993 | - | 12/01-03/14 | - | - | listed | Outside published use dates |
| LONG HOLLOW | 0650 | usfs-trail-8972150 | - | 12/01-03/14 | - | - | listed | Outside published use dates |
| LONG HOLLOW | 0650 | usfs-trail-8982514 | - | 12/01-03/14 | - | - | listed | Outside published use dates |
| LONG HOLLOW | 0650 | usfs-trail-8982941 | - | 12/01-03/14 | - | - | listed | Outside published use dates |
| LONG HOLLOW | 0650 | usfs-trail-8983013 | - | 12/01-03/14 | - | - | listed | Outside published use dates |
| LOOP | 0680 | usfs-trail-8968615 | - | 12/01-03/14 | - | - | listed | Outside published use dates |
| NODDLE | 0677 | usfs-trail-8982905 | - | 12/01-03/14 | - | - | listed | Outside published use dates |
| OVERLOOK | 0682 | usfs-trail-8977669 | - | 12/01-03/14 | - | - | listed | Outside published use dates |
| OVERLOOK CUTOFF | 0682.A | usfs-trail-8972469 | - | 12/01-03/14 | - | - | listed | Outside published use dates |
| ROI TAN | 0653 | usfs-trail-8972879 | - | 12/01-03/14 | - | - | listed | Outside published use dates |
| SCOTTYS | 0681 | usfs-trail-8969650 | - | 12/01-03/14 | - | - | listed | Outside published use dates |
| SPUR B | 0674.B | usfs-trail-8970932 | - | 12/01-03/14 | - | - | listed | Outside published use dates |
| TOMAHAWK | 0685 | usfs-trail-8978965 | - | 12/01-03/14 | - | - | listed | Outside published use dates |
| TROUT CREEK | 0649 | usfs-trail-8972161 | - | 12/01-03/14 | - | - | listed | Outside published use dates |
| TROUT CREEK | 0649 | usfs-trail-8973336 | - | 12/01-03/14 | - | - | listed | Outside published use dates |
| TROUT CREEK CONNECTION | 0649.A | usfs-trail-8928020 | - | 12/01-03/14 | - | - | listed | Outside published use dates |
| TURTLE MOUNTAIN | 0770 | usfs-trail-8913499 | 12/01-03/14 | - | - | - | listed | Outside published use dates |
| 915 TRAIL | 1915 | usfs-trail-8939993 | - | 01/01-12/31 | - | - | listed | Within published use dates — closures unchecked |
| 916 TRAIL | 1916 | usfs-trail-8941277 | - | 01/01-12/31 | - | - | listed | Within published use dates — closures unchecked |
| 917 TRAIL | 1917 | usfs-trail-8916094 | - | 01/01-12/31 | - | - | listed | Within published use dates — closures unchecked |
| 918 TRAIL | 1918 | usfs-trail-8925808 | - | 01/01-12/31 | - | - | listed | Within published use dates — closures unchecked |
| ARROWHEAD | 0646 | usfs-trail-8964639 | - | 05/16-11/30 | - | - | listed | Within published use dates — closures unchecked |
| BEAR MOUNTAIN | 0693 | usfs-trail-8970743 | 06/01-03/31 | - | - | - | listed | Within published use dates — closures unchecked |
| BEAR MOUNTAIN | 0693 | usfs-trail-8982151 | 01/01-12/31 | - | - | - | listed | Within published use dates — closures unchecked |
| BERGEN ROCK | 0770.I | usfs-trail-8928105 | 01/01-12/31 | - | - | - | listed | Within published use dates — closures unchecked |
| COX CONUNDRUM | 1348.G | usfs-trail-8951159 | - | 01/01-12/31 | - | - | listed | Within published use dates — closures unchecked |
| DEVILS ADVOCATE | 0770.C | usfs-trail-8951157 | 01/01-12/31 | - | - | - | listed | Within published use dates — closures unchecked |
| DEVILS REVENGE | 0770.D | usfs-trail-8917600 | 01/01-12/31 | - | - | - | listed | Within published use dates — closures unchecked |
| DRURY TRAIL | 349 | usfs-trail-8932040 | - | 01/01-12/31 | - | - | listed | Within published use dates — closures unchecked |
| DUTCH FRED | 0679 | usfs-trail-8971352 | - | 06/01-11/30 | - | - | listed | Within published use dates — closures unchecked |
| FLAKE | 1344.B | usfs-trail-8923771 | - | 01/01-12/31 | - | - | listed | Within published use dates — closures unchecked |
| HANKHOS | 0631 | usfs-trail-8972895 | - | 01/01-12/31 | - | - | listed | Within published use dates — closures unchecked |
| HILL TOP TRAIL | 1348.E | usfs-trail-8952581 | - | 01/01-12/31 | - | - | listed | Within published use dates — closures unchecked |
| ILLINOIS GULCH TRAIL | 1350.A | usfs-trail-8931886 | - | 01/01-12/31 | - | - | listed | Within published use dates — closures unchecked |
| LITTLE MOAB | 1344 | usfs-trail-8916340 | - | 01/01-12/31 | - | - | listed | Within published use dates — closures unchecked |
| LOG JUMPER | 0677.A | usfs-trail-8924965 | - | 01/01-12/31 | - | - | listed | Within published use dates — closures unchecked |
| LONG HOLLOW BYPASS | 0770.G | usfs-trail-8916087 | 01/01-12/31 | - | - | - | listed | Within published use dates — closures unchecked |
| LOOKOUT TRAIL | 1348.D | usfs-trail-8915327 | - | 01/01-12/31 | - | - | listed | Within published use dates — closures unchecked |
| MARK TRAIL | 1347.C | usfs-trail-8952582 | - | 01/01-12/31 | - | - | listed | Within published use dates — closures unchecked |
| NO NAME | 0770.B | usfs-trail-8952194 | 01/01-12/31 | - | - | - | listed | Within published use dates — closures unchecked |
| OVERLOOK TRAIL | 1348.B | usfs-trail-8937767 | - | 01/01-12/31 | - | - | listed | Within published use dates — closures unchecked |
| PLATTE VIEW | 0693.A | usfs-trail-8942121 | 01/01-12/31 | - | - | - | listed | Within published use dates — closures unchecked |
| POWERLINE | 0690 | usfs-trail-8979189 | - | 01/01-12/31 | - | - | listed | Within published use dates — closures unchecked |
| QUARRY TRAIL | 1350.B | usfs-trail-8924906 | - | 01/01-12/31 | - | - | listed | Within published use dates — closures unchecked |
| SKELETON | 0770.F | usfs-trail-8925194 | 01/01-12/31 | - | - | - | listed | Within published use dates — closures unchecked |
| SOHNDEE | 0634 | usfs-trail-8972245 | - | 01/01-12/31 | - | - | listed | Within published use dates — closures unchecked |
| TORNADO ALLEY | 0679.B | usfs-trail-8924301 | 01/01-12/31 | - | - | - | listed | Within published use dates — closures unchecked |
| TUNNEL | 0770.A | usfs-trail-8937765 | 01/01-12/31 | - | - | - | listed | Within published use dates — closures unchecked |
| TURKEY TRACK NORTH | 761 | usfs-trail-8971176 | - | 01/01-12/31 | - | - | listed | Within published use dates — closures unchecked |
| TURTLE MOUNTAIN | 0770.E | usfs-trail-8939521 | 01/01-12/31 | - | - | - | listed | Within published use dates — closures unchecked |
| TURTLE MOUNTAIN | 0770 | usfs-trail-8953147 | 01/01-12/31 | - | - | - | listed | Within published use dates — closures unchecked |
| WATSON PARK | 0770.H | usfs-trail-8923770 | 01/01-12/31 | - | - | - | listed | Within published use dates — closures unchecked |
| WYEGYE | 0633 | usfs-trail-8971084 | - | 01/01-12/31 | - | - | listed | Within published use dates — closures unchecked |
| BEGINNER/SCOTTYS CONNECTOR | 681.D | usfs-trail-8915333 | - | - | - | 01/01-12/31 | not-listed | Published restriction overlaps trip |
| COLORADO | 1776 | usfs-trail-8924501 | - | - | - | 01/01-12/31 | not-listed | Published restriction overlaps trip |
| COLORADO | 1776 | usfs-trail-8925547 | - | - | - | 01/01-12/31 | not-listed | Published restriction overlaps trip |
| COLORADO | 1776 | usfs-trail-8955417 | - | - | - | 01/01-12/31 | not-listed | Published restriction overlaps trip |
| COLORADO | 1776 | usfs-trail-8955535 | - | - | - | 01/01-12/31 | not-listed | Published restriction overlaps trip |
| COLORADO | 1776 | usfs-trail-8963975 | - | - | - | 01/01-12/31 | not-listed | Published restriction overlaps trip |
| COLORADO | 1776 | usfs-trail-8971239 | - | - | - | 01/01-12/31 | not-listed | Published restriction overlaps trip |
| COLORADO | 1776 | usfs-trail-8971341 | - | - | - | 01/01-12/31 | not-listed | Published restriction overlaps trip |
| COLORADO | 1776 | usfs-trail-8972880 | - | - | - | 01/01-12/31 | not-listed | Published restriction overlaps trip |
| COLORADO | 1776 | usfs-trail-8973227 | - | - | - | 01/01-12/31 | not-listed | Published restriction overlaps trip |
| COLORADO | 1776 | usfs-trail-8973512 | - | - | - | 01/01-12/31 | not-listed | Published restriction overlaps trip |
| COLORADO TR CONNECTOR | 619 | usfs-trail-8970935 | - | - | - | 01/01-12/31 | not-listed | Published restriction overlaps trip |
| DEVILS HEAD | 611 | usfs-trail-8971316 | - | - | - | 01/01-12/31 | not-listed | Published restriction overlaps trip |
| FERN SOUTH | 630 | usfs-trail-8962228 | - | - | - | 01/01-12/31 | not-listed | Published restriction overlaps trip |
| INDIAN CAVE | 705 | usfs-trail-8968711 | - | - | - | 01/01-12/31 | not-listed | Published restriction overlaps trip |
| INDIAN CREEK | 800 | usfs-trail-8968633 | - | - | - | 01/01-12/31 | not-listed | Published restriction overlaps trip |
| INDIAN CREEK | 800 | usfs-trail-8970783 | - | - | - | 01/01-12/31 | not-listed | Published restriction overlaps trip |
| INDIAN CREEK | 800 | usfs-trail-8977816 | - | - | - | 01/01-12/31 | not-listed | Published restriction overlaps trip |
| INDIAN CREEK | 800 | usfs-trail-8982425 | - | - | - | 01/01-12/31 | not-listed | Published restriction overlaps trip |
| LIGHTFOOT LOOP | 0767.A | usfs-trail-8967058 | - | - | - | 01/01-12/31 | not-listed | Published restriction overlaps trip |
| QUARRY CUT-OFF | 627.A | usfs-trail-8924494 | - | - | - | 01/01-12/31 | not-listed | Published restriction overlaps trip |
| RINGTAIL | 699 | usfs-trail-8913821 | - | - | - | 01/01-12/31 | not-listed | Published restriction overlaps trip |
| SCOTTYS ROCK | 681.F | usfs-trail-8927026 | - | - | - | 01/01-12/31 | not-listed | Published restriction overlaps trip |
| TUNNEL | 0770.A | usfs-trail-8941308 | - | - | - | 01/01-12/31 | not-listed | Published restriction overlaps trip |
| UPPER DUTCH | 0767 | usfs-trail-8913823 | - | - | - | 01/01-12/31 | not-listed | Published restriction overlaps trip |
| ZINN | 615 | usfs-trail-8965330 | - | - | - | 01/01-12/31 | not-listed | Published restriction overlaps trip |


### 6.1 Reproduction of "40 of 76"

| motorcycling, 2026-10-10 to 2026-10-11 | segments |
|---|---|
| listed by the finder (`managed` or `accpt` non-empty) | 76 |
| of those, "Outside published use dates" | 40 |
| of those, "Within published use dates — closures unchecked" | 36 |
| not listed, "Published restriction overlaps trip" (`restricted = 01/01-12/31`) | 26 |
| total | 102 |

The 40 are 38 × `accpt = 12/01-03/14` and 2 × `managed = 12/01-03/14` (FERN 683, TURTLE MOUNTAIN 0770 segment `usfs-trail-8913499`). The 36 are 20 × `accpt = 01/01-12/31`, 13 × `managed = 01/01-12/31`, and one each of `accpt = 05/16-11/30`, `accpt = 06/01-11/30`, `managed = 06/01-03/31`.

The same segments on other dates, for comparison: 10 to 11 July 2026 gives the same 40 outside; 10 to 11 January 2026 gives 74 within and 2 outside (the two summer-range segments, ARROWHEAD `usfs-trail-8964639` and DUTCH FRED). ATV on 10 October: 64 listed, 38 outside (`managed = 12/01-03/14`), 26 within.

## 7. Consistency across regions and tests

Capability:

- Douglas: `trail_season_check: true`, `trip_planner: false` (`v2/regions/douglas-co/explore.json`).
- Aspen: `trail_season_check: false`, `trip_planner: true` (`v2/regions/aspen/explore.json`).
- The gate is one line, `v2/explore/capabilities.js:24`: `if(!caps.trip_planner)return caps.trail_season_check?scope.ExploreBrowse.attach(shell):null;`. The flag switches on the whole Browse module (finder, saved plan, recreation-site detail and the season verdict), not just the verdict. Setting it to `false` for Douglas would remove the finder and the campground and trailhead detail as well.
- Aspen therefore never calls `season()`. It shows the raw strings through `evidence.js:50-57` only. The interpretation is not applied inconsistently across regions; it is applied in one region.
- If the same function were run on Aspen for 10 to 11 October (hypothetical, not shown to anyone): hiking 82 listed, all "Within"; mountain biking 35 listed, all "Within", 80 unlisted restricted; cross-country skiing 4 listed, 1 "Outside" (`managed = 11/15-05/30`).

Tests that pin the current interpretation:

| test | what it pins |
|---|---|
| `v2/pipeline/tests/douglas-discovery.test.cjs:3-10` | `accpt: 12/01-03/14` is "Outside" on 27 to 28 September and "Within" on 31 December to 2 January; restriction wins; unparseable restriction needs review; empty record is unknown; invalid date and month rejected |
| `v2/pipeline/tests/explore-compatibility.test.cjs:24-29` with `fixtures/explore-compatibility.json` | 8 `seasonCases` with the exact strings (including "Outside published use dates" for `accpt: 12/01-03/14`), 7 `windows` cases, `days` cases |
| `v2/pipeline/tests/trail-discovery.test.cjs:3` | `matches` exercised with an `accpt`-only hiking fixture and a `restricted`-only bicycle fixture |
| `v2/pipeline/tests/test_trails.py:10-18` | pipeline keeps strings verbatim and leaves a missing attribute null |
| `v2/pipeline/tests/test_published_data.py:51`, `region_contract.py:708` (R29) | shape of `activities` only |
| `v2/pipeline/tests/published-data.test.cjs:13` | activity key set of `trail-seasons.js` equals the pipeline's |

I found no browser-harness assertion on the verdict strings (grep of `v2/pipeline/tests/browser/*.mjs`). No test states what `managed`, `accpt`, `disc` or `restricted` mean; the tests pin behaviour, not a documented source definition. `docs/specs/M3-unified-mobile-explore.md:849` lists a `trail-seasons.test.cjs` that does not exist under that name.

## 8. Internal-consistency evidence (INFERENCE from the data alone)

Nothing in this section establishes meaning. It records patterns the research worker can test against the agency definition.

### 8.1 Do the fields tile the year within one activity on one segment?

An "activity cell" is one activity on one segment. Days were compared on a 366-day calendar.

| region | cells | no field | one field, full year | one field, partial year | several fields, tile the year exactly (complementary) | several fields, overlapping | several fields, gaps |
|---|---|---|---|---|---|---|---|
| Douglas | 918 | 388 | 306 | 224 | 0 | 0 | 0 |
| Aspen | 1,107 | 434 | 617 | 53 | 3 | 0 | 0 |

- Douglas never populates two fields for the same activity on the same segment. The complement test cannot be run there. Every partial-year value stands alone and the rest of the year is unstated.
- The only multi-field cells anywhere are 3 Aspen hiking segments: `managed = 06/15-10/15` with `accpt = 01/01-06/14,10/16-12/31`. They tile the year exactly, with no overlap.
- INFERENCE: in those 3 cells `accpt` is the complement of `managed` in time, and both describe use that is published for the trail (managed in summer, accepted the rest of the year). That fits treating `managed` and `accpt` as two positive categories that partition the year. It does not show that a lone `accpt = 12/01-03/14` means "accepted only in winter"; it is equally the pattern you would see if `accpt` were recorded only for the part of the year that is not the managed season and the managed season were missing from the record.

### 8.2 The same date string recurs across activities on a segment

Douglas segments grouped by their full signature (m = managed, a = accpt, d = disc, r = restricted):

| segments | motorcycle | ATV | 4WD | hiking | bicycle | pack/saddle | `allowed_terra_use` |
|---|---|---|---|---|---|---|---|
| 38 | a 12/01-03/14 | m 12/01-03/14 | r 01/01-12/31 | d 12/01-03/14 | d 12/01-03/14 | d 12/01-03/14 | 54321 |
| 13 | a 01/01-12/31 | a 01/01-12/31 | m 01/01-12/31 | - | - | - | 654321 |
| 11 | r 01/01-12/31 | r 01/01-12/31 | r 01/01-12/31 | m 01/01-12/31 | m 01/01-12/31 | m 01/01-12/31 | 321 |
| 10 | m 01/01-12/31 | r 01/01-12/31 | r 01/01-12/31 | d 01/01-12/31 | d 01/01-12/31 | d 01/01-12/31 | 4321 |
| 6 | a 01/01-12/31 | m 01/01-12/31 | r 01/01-12/31 | - | - | - | 54321 |
| 4 | r 01/01-12/31 | m 01/01-12/31 | r 01/01-12/31 | d 01/01-12/31 | d 01/01-12/31 | d 01/01-12/31 | 5321 |
| 4 | r 01/01-12/31 | r 01/01-12/31 | r 01/01-12/31 | m 06/16-03/31 | m 06/16-03/31 | m 06/16-03/31 | 321 |
| 16 | 11 other signatures, 1 to 3 segments each | | | | | | |

- On every segment with a partial-year string, the identical string is used for every non-restricted activity, under whichever field that activity has. The 38-segment cluster reads: ATV managed, motorcycle accepted, hiking, bicycle and pack/saddle discouraged, all `12/01-03/14`.
- INFERENCE: the date range behaves like one segment-level value and the field name carries the per-activity category (managed for, accepted, discouraged). The four fields look like a classification of each use on the segment, not four independent seasons.
- Under the app's current reading, those 38 segments are published for ATVs and motorcycles only from 1 December to 14 March, and the source says nothing about any use for the other eight and a half months, while `allowed_terra_use` lists five uses. Under a different reading, in which `12/01-03/14` is a seasonal exception or closure window attached to the segment, the verdict would be inverted. The data cannot distinguish these.
- `12/01-03/14` is the only winter-only window in the Douglas data (40 motorcycle cells). The other partial-year values are `06/16-03/31` (5 segments), `06/01-03/31` (1), `05/16-11/30` (1) and `06/01-11/30` (1), which all include summer and autumn.

### 8.3 Segments of one trail with different strings

Four trail numbers have segments whose motorcycle strings differ:

| trail | segment strings |
|---|---|
| ARROWHEAD 0646 | `accpt 12/01-03/14` on one segment, `accpt 05/16-11/30` on the other |
| TURTLE MOUNTAIN 0770 | `managed 12/01-03/14`, `managed 01/01-12/31` |
| BEAR MOUNTAIN 0693 | `managed 06/01-03/31`, `managed 01/01-12/31` |
| TUNNEL 0770.A | `managed 01/01-12/31`, `restricted 01/01-12/31` |

Under the current reading the two ARROWHEAD segments are never in season on the same day. INFERENCE: either the source records are inconsistent between adjacent segments or the windows do not mean what the app assumes.

### 8.4 `allowed_terra_use` agrees with the fields on which uses, not when

Assuming the digits are 1 hiker, 2 pack/saddle, 3 bicycle, 4 motorcycle, 5 ATV, 6 4WD (my reading of the pattern in this data; not confirmed against agency documentation):

| Douglas | digit present | digit absent |
|---|---|---|
| motorcycle (4) | 76: every `managed` or `accpt` segment, including all 40 with `12/01-03/14` | 26: every `restricted 01/01-12/31` segment |
| ATV (5) | 64: every `managed` or `accpt` segment | 38: every `restricted` segment |
| 4WD (6) | 13: `managed 01/01-12/31` | 89: `restricted 01/01-12/31` |
| bicycle (3) | 100: `managed`, `disc` or empty | 2: `restricted` |

There are 0 exceptions in Douglas and 0 in Aspen (Aspen motorcycle: digit absent on all 123; 119 restricted, 4 empty). Hiking segments that carry only `disc` still have digit 1. INFERENCE: `managed`, `accpt` and `disc` all mark a use the source counts as allowed on the segment, and `restricted` marks one it does not. This supports the app's choice of which segments to list. It says nothing about whether October is inside or outside the allowed period.

## 9. Recommendation (not implemented)

Options:

| option | change | effect on the 40 | risk |
|---|---|---|---|
| A. Keep | none | still "Outside published use dates" | If the research half finds the windows are not exclusive use seasons, the app is telling riders that 40 segments are out of season when they may not be, and "Within … closures unchecked" for the reverse case in winter |
| B. Change the driving field | for example drive "within" from `managed` only, or invert partial-year `accpt` | depends on the definition | Replaces one unverified reading with another; only defensible after the research half lands and cites the agency definition |
| C. Suppress the verdict, show raw strings as unknown | `season()` stops returning within/outside; the finder and detail show the source strings with a neutral label | "Published dates not interpreted" plus the raw strings | Loses the convenience of a per-trip answer; nothing false is shown |

Recommended now: C. Reasons that do not depend on what the fields mean:

1. The verdict treats months the source does not mention as "outside". `docs/product/trust-principles.md` section 1 says a missing claim means unknown and is never resolved by inference.
2. `v2/pipeline/TRAIL-PILOT.md` ("Activity model") states the interface does not evaluate dates, and `evidence.js:52` tells the user the dates are not a check for the trip. The verdict contradicts both.
3. No test or document in the repository cites a source definition for the four fields.
4. Section 8.2 and 8.3 show the current reading produces results that are hard to reconcile within the source's own data.

Whether "Published restriction overlaps trip" should also be suppressed is a judgement for the coordinator. It depends on the meaning of `restricted` in the same way, although all 155 non-null `restricted` values in Douglas are full-year, so the date arithmetic adds nothing there.

After the research half reports, B becomes possible, and the within/outside wording could return for full-year strings only if the definition supports it.

What a fail-closed display would say (proposed wording, for owner approval):

- Finder row, in place of the verdict: `Source dates not interpreted — see details`
- Detail, in place of the verdict paragraph: `Published source dates, not checked against your trip. Ohvernight has not confirmed what these date ranges mean for when riding is allowed. Dates the source does not list are unknown.`
- Raw strings unchanged but labelled by source field name, for example `Dirt biking — source field "accepted": 12/01-03/14`, so the label does not assert that the range is the accepted season.
- Filter note at `browse.js:30`: replace "Dates check published trail seasons, not live closures." with `Trip dates do not filter or grade trails.`
- Full-year restricted segments could keep a neutral statement of the source value, for example `Source lists this use as restricted 01/01-12/31`.

Files a fix would touch:

- `v2/explore/trail-seasons.js:17-25` (`season`), and possibly `:2` labels.
- `v2/explore/browse.js:30` (filter note), `:34` (row verdict), `:48-50` (detail verdict, field labels, caveat), `:28` (date inputs, if dates no longer affect trails).
- `v2/trail-discovery.js:7` only if the listing rule changes (it encodes the same `managed || accpt` reading; `disc`-only segments are currently unlisted).
- `v2/explore/evidence.js:52`, `:56` if the shared labels change; this file is also used by Aspen.
- `v2/pipeline/TRAIL-PILOT.md` and `v2/regions/douglas-co/README.md`, to match whatever behaviour ships.
- Not `v2/regions/douglas-co/explore.json`: the `trail_season_check` flag cannot be used as the switch because of `capabilities.js:24`. A separate capability would need `v2/explore/layer-registry.js:19`, `v2/pipeline/schema/explore-config.schema.json` and `v2/pipeline/tests/test_explore_config.py`.
- Optional pipeline hardening: add the activity attribute names to `required_fields` in `fetch_trails.py:35` and `fetch_douglas.py:59` so a renamed attribute fails the fetch.

Tests a fix would touch:

- `v2/pipeline/tests/douglas-discovery.test.cjs:3-10`.
- `v2/pipeline/tests/fixtures/explore-compatibility.json` (`seasonCases`) and `explore-compatibility.test.cjs:24-29`. These are labelled as pinned base-commit outputs, so changing them is a deliberate behaviour change that needs to be called out in the pull request.
- A new test that a partial-year string never yields a positive or negative trip verdict, and a browser check that the Douglas finder shows no "Outside"/"Within" text.
- `v2/pipeline/tests/legacy-wording.test.cjs` and `proximity-wording.test.cjs` should be run against any new wording.

## 10. Could not determine

- The agency definitions of `MANAGED`, `ACCPT`, `DISC` and `RESTRICTED`, and whether a date range is a season of use or something else. Research half.
- Whether the live service exposes `*_ACCPT` and `*_DISC` separately or a combined attribute. No network.
- The digit mapping of `ALLOWED_TERRA_USE`. Inferred from the pattern only.
- Whether the committed data was generated by the committed code.
