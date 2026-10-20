# NHD selection probe

Read-only attribute probe of the NHD MapServer by the coordinator on
2026-10-06, to estimate what the proposed M4 selection rule yields. No
geometry was fetched and nothing was written to the repository's data. Counts
are of features intersecting each region's bounding box, so they are slightly
higher than the clipped repository data, and connectivity between segments
was not tested. Real numbers come from M4-A data and the M4-B selection
report.

Reservoir codes: the first run of this probe treated only "water storage"
codes as eligible, which leaves out Rueter-Hess Reservoir (`43619`,
"Construction Material = Nonearthen"). The specification's rule was corrected
from the service's coded-value domain as a result; see section 8.1 of the
specification. "named not perennial" below therefore includes Rueter-Hess,
which the corrected rule displays.

```text
Read-only attribute probe of the NHD MapServer, 2026-10-06 (no geometry fetched; features intersecting each region bounding box).

== aspen
 named perennial stream pieces: 1087  -> distinct gnis_id groups: 62 ; distinct names: 58 ; names shared by >1 gnis_id: {'Hunter Creek': 2, 'Pine Creek': 2, 'Copper Creek': 2, 'Sawyer Creek': 2}
 group length km: under 0.5: 0, 0.5-2: 7, 2-10: 41, over 10: 14
 longest groups: [('Roaring Fork River', 82, 39.1), ('Castle Creek', 77, 30.6), ('Snowmass Creek', 80, 27.4), ('Hunter Creek', 56, 24.7), ('Woody Creek', 72, 19.6), ('Lincoln Creek', 46, 18.7), ('Conundrum Creek', 42, 15.9), ('Maroon Creek', 41, 15.2)]
 shortest groups: [('Collins Creek', 2, 1.35), ('Nickelson Creek', 3, 1.44), ('Lime Creek', 4, 1.48), ('Sawyer Creek', 2, 1.74), ('Truro Creek', 2, 1.82), ('East River', 5, 1.93), ('Copper Creek', 2, 1.98), ('Jack Creek', 2, 2.18)]
 named groups that are intermittent-only (would not display): 9 ['Casaday Creek', 'Cliff Creek', 'Hannon Creek', 'Johnson Creek', 'Little Elk Creek', 'Sawmill Creek', 'Silver Creek', 'Wilbur Creek', 'Wildcat Creek']
 named artificial-path pieces: 124 of which gnis_id belongs to a perennial group: 113
 permanent_identifier present on all pieces: True ; distinct: 1290 of 1290
 waterbodies (390/436) total: 414  named: 39  unnamed: 375  fcodes: {39004: 365, 39001: 31, 39009: 10, 43624: 5, 39000: 3}
 named perennial (eligible at any size): 39 ; named not perennial (not displayed): 0 []
  unnamed perennial >= 0.5 ha: 44 (of 336 unnamed perennial); total eligible waterbodies: 83
  unnamed perennial >= 2.0 ha: 3 (of 336 unnamed perennial); total eligible waterbodies: 42
  unnamed perennial between 0.5 and 2 ha (lost at 2 ha): 41 ; areas ha: [1.7, 1.6, 1.36, 1.3, 1.2, 1.1, 1.1, 1.1, 0.9, 0.9, 0.9, 0.83, 0.8, 0.8, 0.8]
  named perennial smaller than 0.5 ha: [('Silver Dollar Pond', 0), ('Elk Creek Reservoir Number 2', 0.32)]
  named perennial, all (name, ha): [('Snowmass Lake', 33.5), ('Wildcat Reservoir', 21.2), ('Grizzly Reservoir', 12.7), ('Willow Lake', 8.7), ('Warren Lakes', 7.8), ('Taylor Lake', 7.7), ('Crater Lake', 7.2), ('Cathedral Lake', 6.9), ('Maroon Lake', 6.5), ('Lost Man Lake', 5.8), ('Petroleum Lake', 5.0), ('Emerald Lake', 4.9), ('Warren Lake', 4.9), ('Linkins Lake', 4.6), ('Sawyer Lake', 4.4), ('Anderson Lake', 3.6), ('Weller Lake', 3.5), ('Grizzly Lake', 3.3), ('Warren Lakes', 3.2), ('Copper Lake', 3.1), ('Truro Lake', 2.7), ('Granite Lakes', 2.5), ('Lost Man Reservoir', 2.5), ('Tabor Lake', 2.2), ('Ptarmigan Lake', 2.1), ('Midway Lake', 2.0), ('Tagerts Lake', 1.8), ('Marolt Reservoir', 1.8), ('Scott Lake', 1.5), ('Ruby Lakes', 1.4), ('American Lake', 1.4), ('Sioux Lake', 1.1), ('Jack Lake', 0.9), ('Whites Lake', 0.8), ('Deadman Lake', 0.8), ('Henschel Lake', 0.5), ('Ruby Lakes', 0.5), ('Elk Creek Reservoir Number 2', 0.3), ('Silver Dollar Pond', 0)]
  largest unnamed perennial (ha): [4.0, 2.2, 2.2, 1.7, 1.6, 1.4, 1.3, 1.2, 1.1, 1.1]

== douglas-co
 named perennial stream pieces: 2026  -> distinct gnis_id groups: 56 ; distinct names: 54 ; names shared by >1 gnis_id: {'Bear Creek': 2, 'Pine Creek': 2}
 group length km: under 0.5: 1, 0.5-2: 5, 2-10: 30, over 10: 20
 longest groups: [('East Plum Creek', 181, 53.6), ('Cherry Creek', 60, 39.0), ('West Plum Creek', 84, 33.6), ('West Cherry Creek', 19, 23.1), ('Jackson Creek', 106, 19.2), ('Indian Creek', 65, 16.8), ('Plum Creek', 54, 16.2), ('Cook Creek', 55, 15.7)]
 shortest groups: [('South Platte River', 1, 0.08), ('Willow Creek', 3, 1.4), ('Casto Creek', 3, 1.57), ('Trail Creek', 10, 1.75), ('Green Mountain Creek', 5, 1.95), ('Tramway Creek', 16, 1.98), ('Last Resort Creek', 21, 2.63), ('Camp Creek', 11, 2.7)]
 named groups that are intermittent-only (would not display): 27 ['Big Dry Creek', 'Brush Creek', 'Coal Creek', 'Cook Creek', 'Cottonwood Creek', 'Crowfoot Creek', 'Deep Creek', 'Douglas Creek', 'Elk Creek', 'Gold Creek', 'Happy Canyon Creek', 'Jarre Creek']
 named artificial-path pieces: 670 of which gnis_id belongs to a perennial group: 502
 permanent_identifier present on all pieces: True ; distinct: 3503 of 3503
 waterbodies (390/436) total: 2275  named: 36  unnamed: 2239  fcodes: {39004: 761, 39001: 1461, 43612: 6, 43624: 23, 39011: 7, 43613: 4, 39005: 2, 39009: 9, 43601: 1, 43619: 1}
 named perennial (eligible at any size): 17 ; named not perennial (not displayed): 19 [('Mann Reservoir', 39001, 0.3), ('Franktown Parker FPB-1 Reservoir', 39005, 7.4), ('West Cherry Creek Detention Number 8 Reservoir', 39001, 0.4), ('Cantrill Reservoir', 39001, 0.2), ('Franktown Parker FPA-2 Reservoir', 39001, 4.8), ('Fairview Reservoir', 39001, 7.2), ('Fairview Reservoir Number 2', 39001, 1.1), ('Franktown Parker FPM-1 Reservoir', 39001, 0.3), ('West Cherry Creek Detention Number 11 Reservoir', 39001, 7.7), ('Franktown Parker FPA-4 Reservoir', 39001, 3.8), ('Franktown Parker FPR-1 Reservoir', 39005, 2.4), ('Franktown Parker FPE-7 Reservoir', 39001, 2.7), ('Franktown Parker FPW-1 Reservoir', 39001, 4.2), ('West Cherry Creek Detention Number 9 Reservoir', 39001, 2.4), ('Stevens Reservoir Number 2 and 3', 39001, 2.4), ('Franktown Parker FPP-1 Reservoir', 39001, 3.8), ('Franktown Parker FPE-8 Reservoir', 39001, 8.3), ('Nelson Reservoir', 39001, 0.1), ('Rueter-Hess Reservoir', 43619, 87.5)]
  unnamed perennial >= 0.5 ha: 123 (of 764 unnamed perennial); total eligible waterbodies: 140
  unnamed perennial >= 2.0 ha: 19 (of 764 unnamed perennial); total eligible waterbodies: 36
  unnamed perennial between 0.5 and 2 ha (lost at 2 ha): 104 ; areas ha: [1.8, 1.7, 1.7, 1.6, 1.6, 1.5, 1.5, 1.5, 1.4, 1.3, 1.3, 1.2, 1.2, 1.1, 1.1]
  named perennial smaller than 0.5 ha: []
  named perennial, all (name, ha): [('Chatfield Lake', 562.2), ('Cheesman Lake', 358.1), ('McLellan Reservoir', 77.4), ('Strontia Springs Reservoir', 32.8), ('Aurora-Rampart Reservoir', 26.9), ('Platte Canyon Reservoir', 21.3), ('Pinery Reservoir', 9.6), ('J O Hill Reservoir', 7.5), ('Waucondah Reservoir', 7.4), ('Wakeman Reservoir', 5.8), ('Circle 2 Ranch Reservoir Number 1', 4.9), ('Franktown Parker FPA-5 Reservoir', 3.7), ('Barney Bird Reservoir Number One', 3.6), ('Wolhurst Lake', 3.4), ('Allis Reservoir', 2.1), ('West Cherry Creek Detention Number 7 Reservoir', 1.8), ('Franktown Parker FPS-1 Reservoir', 0.7)]
  largest unnamed perennial (ha): [22.7, 18.2, 8.7, 8.4, 8.3, 5.4, 4.8, 4.3, 3.4, 3.1]

```

## NHD waterbody feature-code domain (read from the service, 2026-10-06)

```text
39000 Lake/Pond
39001 Lake/Pond: Hydrographic Category = Intermittent
39004 Lake/Pond: Hydrographic Category = Perennial
39005 Lake/Pond: Hydrographic Category = Intermittent; Stage = High Water Elevation
39006 Lake/Pond: Hydrographic Category = Intermittent; Stage = Date of Photography
39009 Lake/Pond: Hydrographic Category = Perennial; Stage = Average Water Elevation
39010 Lake/Pond: Hydrographic Category = Perennial; Stage = Normal Pool
39011 Lake/Pond: Hydrographic Category = Perennial; Stage = Date of Photography
39012 Lake/Pond: Hydrographic Category = Perennial; Stage = Spillway
43600 Reservoir
43601 Reservoir: Reservoir Type = Aquaculture
43603 Reservoir: Reservoir Type = Decorative Pool
43604 Reservoir: Reservoir Type = Tailings Pond; Construction Material = Earthen
43605 Reservoir: Reservoir Type = Tailings Pond
43606 Reservoir: Reservoir Type = Disposal
43607 Reservoir: Reservoir Type = Evaporator
43608 Reservoir: Reservoir Type = Swimming Pool
43609 Reservoir: Reservoir Type = Cooling Pond
43610 Reservoir: Reservoir Type = Filtration Pond
43611 Reservoir: Reservoir Type = Settling Pond
43612 Reservoir: Reservoir Type = Sewage Treatment Pond
43613 Reservoir: Reservoir Type = Water Storage; Construction Material = Nonearthen
43614 Reservoir: Reservoir Type = Water Storage; Construction Material = Earthen; Hydrographic Category = Intermittent
43615 Reservoir: Reservoir Type = Water Storage; Construction Material = Earthen; Hydrographic Category = Perennial
43617 Reservoir: Reservoir Type = Water Storage
43618 Reservoir: Construction Material = Earthen
43619 Reservoir: Construction Material = Nonearthen
43621 Reservoir: Reservoir Type = Water Storage; Hydrographic Category = Perennial
43623 Reservoir: Reservoir Type = Evaporator; Construction Material = Earthen
43624 Reservoir: Reservoir Type = Treatment
43625 Reservoir: Reservoir Type = Disposal; Construction Material = Earthen
43626 Reservoir: Reservoir Type = Disposal; Construction Material = Nonearthen
```
