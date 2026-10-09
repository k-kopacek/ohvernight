# M4-B water selection report

Generated from committed canonical data and `water_display.json`; no source is contacted.

## aspen

### Source feature selection by class and category

| Water class | Hydro category | Displayed members or bodies | Not displayed |
|---|---:|---:|---:|
| artificial_path | unknown | 126 | 342 |
| canal_ditch | unknown | 0 | 170 |
| connector | unknown | 0 | 65 |
| lake_pond | intermittent | 0 | 36 |
| lake_pond | perennial | 46 | 366 |
| lake_pond | unknown | 0 | 3 |
| pipeline | unknown | 0 | 13 |
| reservoir | unknown | 0 | 5 |
| stream | ephemeral | 0 | 2425 |
| stream | intermittent | 0 | 1804 |
| stream | perennial | 1147 | 320 |
| swamp_marsh | unknown | 0 | 58 |

### Groups and connectivity

- Stream groups: 69
- Members per group distribution (member count: number of groups): 1: 3, 2: 4, 3: 2, 4: 5, 5: 2, 6: 5, 7: 5, 8: 1, 9: 4, 10: 4, 12: 3, 13: 3, 14: 6, 15: 1, 18: 2, 19: 2, 22: 1, 24: 1, 26: 2, 27: 1, 33: 1, 36: 1, 37: 1, 42: 2, 52: 1, 55: 1, 58: 1, 77: 1, 78: 1, 83: 1, 111: 1
- Multi-part GNIS IDs and part group IDs: ["00179785"]
- Connectors used with geodesic lengths in km: [{"gnis_id": "00180061", "group_id": "nhd-gnis-00180061", "id": "nhd-165836028", "length_km": 0.019228, "name": "Hunter Creek"}, {"gnis_id": "00180317", "group_id": "nhd-gnis-00180317", "id": "nhd-72975294", "length_km": 0.139771, "name": "Galena Creek"}]
- Extent-edge splits and drawn line counts: [{"drawn_lengths_km": [0.8661886223345853, 0.48158491482301213, 0.23275833101211788], "gaps_m": [1358.775, 283.848], "gnis_id": "00179785", "group_ids": ["nhd-gnis-00179785", "nhd-gnis-00179785-p2", "nhd-gnis-00179785-p3"], "line_counts": [4, 1, 3]}]
- Reviewed exclusions: none

### Waterbody threshold comparison

| Threshold | Unnamed included | Total displayed | Water display bytes |
|---|---:|---:|---:|
| 0.5 ha (0.005 km²) | 47 | 90 | 859852 |
| 2 ha (0.02 km²) | 3 | 46 | 819378 |

Largest waterbodies excluded at 2 ha and included at 0.5 ha:

```json
[
  {
    "id": "nhd-72962706",
    "name": null,
    "area_sqkm": 0.017,
    "elevation_m": null,
    "coordinates_lon_lat": [
      -106.802718,
      39.17638
    ]
  },
  {
    "id": "nhd-72971646",
    "name": null,
    "area_sqkm": 0.016,
    "elevation_m": null,
    "coordinates_lon_lat": [
      -106.653548,
      39.26457
    ]
  },
  {
    "id": "nhd-72971650",
    "name": null,
    "area_sqkm": 0.016,
    "elevation_m": null,
    "coordinates_lon_lat": [
      -106.665195,
      39.258775
    ]
  },
  {
    "id": "nhd-72964618",
    "name": null,
    "area_sqkm": 0.014,
    "elevation_m": null,
    "coordinates_lon_lat": [
      -107.054685,
      39.146704
    ]
  },
  {
    "id": "nhd-65879795",
    "name": null,
    "area_sqkm": 0.013589500000000001,
    "elevation_m": 3692.9568000000004,
    "coordinates_lon_lat": [
      -106.949806,
      39.012193
    ]
  },
  {
    "id": "nhd-72974976",
    "name": null,
    "area_sqkm": 0.013000000000000001,
    "elevation_m": null,
    "coordinates_lon_lat": [
      -106.657201,
      39.048876
    ]
  },
  {
    "id": "nhd-72968818",
    "name": null,
    "area_sqkm": 0.012,
    "elevation_m": null,
    "coordinates_lon_lat": [
      -106.922341,
      39.223932
    ]
  },
  {
    "id": "nhd-72968822",
    "name": null,
    "area_sqkm": 0.011000000000000001,
    "elevation_m": null,
    "coordinates_lon_lat": [
      -106.927761,
      39.223429
    ]
  },
  {
    "id": "nhd-72972334",
    "name": null,
    "area_sqkm": 0.011000000000000001,
    "elevation_m": null,
    "coordinates_lon_lat": [
      -106.583203,
      39.151173
    ]
  },
  {
    "id": "nhd-72981112",
    "name": null,
    "area_sqkm": 0.011000000000000001,
    "elevation_m": null,
    "coordinates_lon_lat": [
      -106.653929,
      39.246849
    ]
  },
  {
    "id": "nhd-65878197",
    "name": null,
    "area_sqkm": 0.009000000000000001,
    "elevation_m": null,
    "coordinates_lon_lat": [
      -106.755483,
      39.00968
    ]
  },
  {
    "id": "nhd-72962752",
    "name": null,
    "area_sqkm": 0.009000000000000001,
    "elevation_m": null,
    "coordinates_lon_lat": [
      -106.757628,
      39.132607
    ]
  },
  {
    "id": "nhd-72964606",
    "name": null,
    "area_sqkm": 0.009000000000000001,
    "elevation_m": null,
    "coordinates_lon_lat": [
      -107.054667,
      39.167574
    ]
  },
  {
    "id": "nhd-72971114",
    "name": null,
    "area_sqkm": 0.009000000000000001,
    "elevation_m": null,
    "coordinates_lon_lat": [
      -106.968806,
      39.110945
    ]
  },
  {
    "id": "nhd-72962584",
    "name": null,
    "area_sqkm": 0.008333730000000001,
    "elevation_m": null,
    "coordinates_lon_lat": [
      -106.854829,
      39.248381
    ]
  },
  {
    "id": "nhd-72968826",
    "name": null,
    "area_sqkm": 0.008,
    "elevation_m": null,
    "coordinates_lon_lat": [
      -106.922953,
      39.221254
    ]
  },
  {
    "id": "nhd-72968842",
    "name": null,
    "area_sqkm": 0.008,
    "elevation_m": null,
    "coordinates_lon_lat": [
      -106.982056,
      39.206342
    ]
  },
  {
    "id": "nhd-72971110",
    "name": null,
    "area_sqkm": 0.008,
    "elevation_m": null,
    "coordinates_lon_lat": [
      -106.9736,
      39.111173
    ]
  },
  {
    "id": "nhd-72974950",
    "name": null,
    "area_sqkm": 0.008,
    "elevation_m": null,
    "coordinates_lon_lat": [
      -106.647469,
      39.053997
    ]
  },
  {
    "id": "nhd-72968808",
    "name": null,
    "area_sqkm": 0.00763619,
    "elevation_m": 2468.88,
    "coordinates_lon_lat": [
      -106.977949,
      39.23793
    ]
  }
]
```

Twenty smallest waterbodies included at 2 ha:

```json
[
  {
    "id": "nhd-72971158",
    "name": "Silver Dollar Pond",
    "area_sqkm": 0,
    "elevation_m": null,
    "coordinates_lon_lat": [
      -106.883708,
      39.043332
    ]
  },
  {
    "id": "nhd-72964542",
    "name": "Elk Creek Reservoir Number 2",
    "area_sqkm": 0.00317863,
    "elevation_m": null,
    "coordinates_lon_lat": [
      -107.008777,
      39.235312
    ]
  },
  {
    "id": "nhd-133049530",
    "name": "Henschel Lake",
    "area_sqkm": 0.005,
    "elevation_m": null,
    "coordinates_lon_lat": [
      -106.587217,
      39.028189
    ]
  },
  {
    "id": "nhd-72969566",
    "name": "Ruby Lakes",
    "area_sqkm": 0.005,
    "elevation_m": null,
    "coordinates_lon_lat": [
      -106.615913,
      39.014741
    ]
  },
  {
    "id": "nhd-72972304",
    "name": "Deadman Lake",
    "area_sqkm": 0.008,
    "elevation_m": null,
    "coordinates_lon_lat": [
      -106.58135,
      39.189275
    ]
  },
  {
    "id": "nhd-72982256",
    "name": "Christenson Reservoir",
    "area_sqkm": 0.00801449,
    "elevation_m": null,
    "coordinates_lon_lat": [
      -106.970205,
      39.264032
    ]
  },
  {
    "id": "nhd-72968858",
    "name": "Whites Lake",
    "area_sqkm": 0.008162870000000001,
    "elevation_m": 2827.9344,
    "coordinates_lon_lat": [
      -106.894845,
      39.185919
    ]
  },
  {
    "id": "nhd-72974974",
    "name": "Jack Lake",
    "area_sqkm": 0.009000000000000001,
    "elevation_m": null,
    "coordinates_lon_lat": [
      -106.627077,
      39.049508
    ]
  },
  {
    "id": "nhd-72972310",
    "name": "Sioux Lake",
    "area_sqkm": 0.011000000000000001,
    "elevation_m": null,
    "coordinates_lon_lat": [
      -106.602762,
      39.175914
    ]
  },
  {
    "id": "nhd-72978806",
    "name": "Elko Lake",
    "area_sqkm": 0.011000000000000001,
    "elevation_m": null,
    "coordinates_lon_lat": [
      -107.052077,
      39.015575
    ]
  },
  {
    "id": "nhd-72972274",
    "name": "Granite Lakes",
    "area_sqkm": 0.012,
    "elevation_m": null,
    "coordinates_lon_lat": [
      -106.568854,
      39.23119
    ]
  },
  {
    "id": "nhd-72968354",
    "name": "American Lake",
    "area_sqkm": 0.014,
    "elevation_m": null,
    "coordinates_lon_lat": [
      -106.829785,
      39.056428
    ]
  },
  {
    "id": "nhd-72969570",
    "name": "Ruby Lakes",
    "area_sqkm": 0.014,
    "elevation_m": null,
    "coordinates_lon_lat": [
      -106.619698,
      39.010347
    ]
  },
  {
    "id": "nhd-72972326",
    "name": "Scott Lake",
    "area_sqkm": 0.015000000000000001,
    "elevation_m": null,
    "coordinates_lon_lat": [
      -106.617808,
      39.157283
    ]
  },
  {
    "id": "nhd-72968848",
    "name": "Marolt Reservoir",
    "area_sqkm": 0.01764992,
    "elevation_m": 2599.0296000000003,
    "coordinates_lon_lat": [
      -106.888335,
      39.199318
    ]
  },
  {
    "id": "nhd-72962754",
    "name": "Tagerts Lake",
    "area_sqkm": 0.018000000000000002,
    "elevation_m": null,
    "coordinates_lon_lat": [
      -106.753763,
      39.131022
    ]
  },
  {
    "id": "nhd-72981176",
    "name": "Midway Lake",
    "area_sqkm": 0.02,
    "elevation_m": null,
    "coordinates_lon_lat": [
      -106.666885,
      39.161765
    ]
  },
  {
    "id": "nhd-65880737",
    "name": "Ptarmigan Lake",
    "area_sqkm": 0.021,
    "elevation_m": null,
    "coordinates_lon_lat": [
      -106.670163,
      39.040203
    ]
  },
  {
    "id": "nhd-72964646",
    "name": null,
    "area_sqkm": 0.022000000000000002,
    "elevation_m": null,
    "coordinates_lon_lat": [
      -107.013018,
      39.133241
    ]
  },
  {
    "id": "nhd-72974934",
    "name": "Tabor Lake",
    "area_sqkm": 0.022000000000000002,
    "elevation_m": null,
    "coordinates_lon_lat": [
      -106.65734,
      39.062769
    ]
  }
]
```

### Named artificial-path rivers over 2 km that are undrawn or under 80%

```json
[]
```

South Platte River pending marker is Douglas-only; Aspen is not affected.

## douglas-co

### Source feature selection by class and category

| Water class | Hydro category | Displayed members or bodies | Not displayed |
|---|---:|---:|---:|
| artificial_path | unknown | 94 | 161 |
| canal_ditch | unknown | 0 | 73 |
| connector | unknown | 0 | 1 |
| lake_pond | intermittent | 0 | 1404 |
| lake_pond | perennial | 31 | 669 |
| pipeline | unknown | 0 | 12 |
| reservoir | unknown | 1 | 29 |
| stream | intermittent | 0 | 504 |
| stream | perennial | 1514 | 0 |
| swamp_marsh | unknown | 0 | 1 |

### Groups and connectivity

- Stream groups: 35
- Members per group distribution (member count: number of groups): 6: 1, 8: 1, 9: 1, 11: 2, 17: 1, 18: 2, 20: 1, 21: 2, 28: 2, 32: 2, 33: 1, 34: 2, 37: 2, 54: 1, 55: 1, 57: 1, 58: 1, 59: 1, 63: 1, 65: 2, 67: 1, 76: 2, 80: 1, 87: 1, 109: 1, 182: 1
- Multi-part GNIS IDs and part group IDs: none
- Connectors used with geodesic lengths in km: none
- Extent-edge splits and drawn line counts: none
- Reviewed exclusions: none

### Waterbody threshold comparison

| Threshold | Unnamed included | Total displayed | Water display bytes |
|---|---:|---:|---:|
| 0.5 ha (0.005 km²) | 109 | 127 | 1063829 |
| 2 ha (0.02 km²) | 14 | 32 | 954452 |

Largest waterbodies excluded at 2 ha and included at 0.5 ha:

```json
[
  {
    "id": "nhd-117821201",
    "name": null,
    "area_sqkm": 0.018000000000000002,
    "elevation_m": null,
    "coordinates_lon_lat": [
      -104.958924,
      39.239702
    ]
  },
  {
    "id": "nhd-117822909",
    "name": null,
    "area_sqkm": 0.017,
    "elevation_m": null,
    "coordinates_lon_lat": [
      -105.018259,
      39.559109
    ]
  },
  {
    "id": "nhd-117819385",
    "name": null,
    "area_sqkm": 0.016,
    "elevation_m": null,
    "coordinates_lon_lat": [
      -105.005841,
      39.484434
    ]
  },
  {
    "id": "nhd-117822715",
    "name": null,
    "area_sqkm": 0.016,
    "elevation_m": null,
    "coordinates_lon_lat": [
      -105.053467,
      39.563052
    ]
  },
  {
    "id": "nhd-117819437",
    "name": null,
    "area_sqkm": 0.015000000000000001,
    "elevation_m": null,
    "coordinates_lon_lat": [
      -105.060927,
      39.45915
    ]
  },
  {
    "id": "nhd-117819459",
    "name": null,
    "area_sqkm": 0.015000000000000001,
    "elevation_m": null,
    "coordinates_lon_lat": [
      -105.080088,
      39.453255
    ]
  },
  {
    "id": "nhd-120655816",
    "name": null,
    "area_sqkm": 0.015000000000000001,
    "elevation_m": null,
    "coordinates_lon_lat": [
      -104.730998,
      39.331665
    ]
  },
  {
    "id": "nhd-117819393",
    "name": null,
    "area_sqkm": 0.014,
    "elevation_m": null,
    "coordinates_lon_lat": [
      -105.017935,
      39.48379
    ]
  },
  {
    "id": "nhd-117819335",
    "name": null,
    "area_sqkm": 0.013000000000000001,
    "elevation_m": null,
    "coordinates_lon_lat": [
      -105.015352,
      39.498922
    ]
  },
  {
    "id": "nhd-117819381",
    "name": null,
    "area_sqkm": 0.013000000000000001,
    "elevation_m": null,
    "coordinates_lon_lat": [
      -105.018148,
      39.484977
    ]
  },
  {
    "id": "nhd-120655564",
    "name": null,
    "area_sqkm": 0.012,
    "elevation_m": null,
    "coordinates_lon_lat": [
      -104.787369,
      39.386381
    ]
  },
  {
    "id": "nhd-120656384",
    "name": null,
    "area_sqkm": 0.012,
    "elevation_m": null,
    "coordinates_lon_lat": [
      -104.689429,
      39.18631
    ]
  },
  {
    "id": "nhd-117792553",
    "name": null,
    "area_sqkm": 0.011000000000000001,
    "elevation_m": null,
    "coordinates_lon_lat": [
      -104.863852,
      39.386791
    ]
  },
  {
    "id": "nhd-117793975",
    "name": null,
    "area_sqkm": 0.011000000000000001,
    "elevation_m": null,
    "coordinates_lon_lat": [
      -104.851141,
      39.270951
    ]
  },
  {
    "id": "nhd-117819383",
    "name": null,
    "area_sqkm": 0.011000000000000001,
    "elevation_m": null,
    "coordinates_lon_lat": [
      -105.098088,
      39.484716
    ]
  },
  {
    "id": "nhd-117819391",
    "name": null,
    "area_sqkm": 0.011000000000000001,
    "elevation_m": null,
    "coordinates_lon_lat": [
      -105.072631,
      39.483751
    ]
  },
  {
    "id": "nhd-117819469",
    "name": null,
    "area_sqkm": 0.011000000000000001,
    "elevation_m": null,
    "coordinates_lon_lat": [
      -105.077172,
      39.446606
    ]
  },
  {
    "id": "nhd-120655832",
    "name": null,
    "area_sqkm": 0.011000000000000001,
    "elevation_m": null,
    "coordinates_lon_lat": [
      -104.698466,
      39.326878
    ]
  },
  {
    "id": "nhd-120656283",
    "name": null,
    "area_sqkm": 0.011000000000000001,
    "elevation_m": null,
    "coordinates_lon_lat": [
      -104.764223,
      39.223391
    ]
  },
  {
    "id": "nhd-120656359",
    "name": null,
    "area_sqkm": 0.011000000000000001,
    "elevation_m": null,
    "coordinates_lon_lat": [
      -104.759965,
      39.191321
    ]
  }
]
```

Twenty smallest waterbodies included at 2 ha:

```json
[
  {
    "id": "nhd-120655126",
    "name": "Franktown Parker FPS-1 Reservoir",
    "area_sqkm": 0.007,
    "elevation_m": null,
    "coordinates_lon_lat": [
      -104.746148,
      39.480882
    ]
  },
  {
    "id": "nhd-120656489",
    "name": "West Cherry Creek Detention Number 7 Reservoir",
    "area_sqkm": 0.018000000000000002,
    "elevation_m": null,
    "coordinates_lon_lat": [
      -104.771931,
      39.141136
    ]
  },
  {
    "id": "nhd-117813853",
    "name": "Allis Reservoir",
    "area_sqkm": 0.021,
    "elevation_m": null,
    "coordinates_lon_lat": [
      -104.852377,
      39.132718
    ]
  },
  {
    "id": "nhd-120655625",
    "name": null,
    "area_sqkm": 0.021,
    "elevation_m": null,
    "coordinates_lon_lat": [
      -104.793053,
      39.374716
    ]
  },
  {
    "id": "nhd-117819415",
    "name": null,
    "area_sqkm": 0.022000000000000002,
    "elevation_m": null,
    "coordinates_lon_lat": [
      -105.06839,
      39.47215
    ]
  },
  {
    "id": "nhd-117792557",
    "name": null,
    "area_sqkm": 0.023,
    "elevation_m": null,
    "coordinates_lon_lat": [
      -104.865404,
      39.384803
    ]
  },
  {
    "id": "nhd-117821223",
    "name": null,
    "area_sqkm": 0.024,
    "elevation_m": null,
    "coordinates_lon_lat": [
      -104.9701,
      39.227998
    ]
  },
  {
    "id": "nhd-120655532",
    "name": null,
    "area_sqkm": 0.027,
    "elevation_m": 1941.6,
    "coordinates_lon_lat": [
      -104.695651,
      39.398809
    ]
  },
  {
    "id": "nhd-34ab3d08-b638-4011-9e3d-167cd78fd4b5",
    "name": null,
    "area_sqkm": 0.027,
    "elevation_m": null,
    "coordinates_lon_lat": [
      -104.805666,
      39.546758
    ]
  },
  {
    "id": "nhd-117822709",
    "name": null,
    "area_sqkm": 0.028,
    "elevation_m": null,
    "coordinates_lon_lat": [
      -105.049695,
      39.564362
    ]
  },
  {
    "id": "nhd-117822915",
    "name": null,
    "area_sqkm": 0.029,
    "elevation_m": null,
    "coordinates_lon_lat": [
      -105.042942,
      39.547115
    ]
  },
  {
    "id": "nhd-117822893",
    "name": "Wolhurst Lake",
    "area_sqkm": 0.034,
    "elevation_m": null,
    "coordinates_lon_lat": [
      -105.037521,
      39.566117
    ]
  },
  {
    "id": "nhd-120655638",
    "name": "Barney Bird Reservoir Number One",
    "area_sqkm": 0.036000000000000004,
    "elevation_m": null,
    "coordinates_lon_lat": [
      -104.748178,
      39.374537
    ]
  },
  {
    "id": "nhd-120656287",
    "name": "Franktown Parker FPA-5 Reservoir",
    "area_sqkm": 0.037000000000000005,
    "elevation_m": null,
    "coordinates_lon_lat": [
      -104.751806,
      39.219067
    ]
  },
  {
    "id": "nhd-117822921",
    "name": null,
    "area_sqkm": 0.048,
    "elevation_m": null,
    "coordinates_lon_lat": [
      -105.077691,
      39.509936
    ]
  },
  {
    "id": "nhd-120655219",
    "name": "Circle 2 Ranch Reservoir Number 1",
    "area_sqkm": 0.049,
    "elevation_m": 1886.7,
    "coordinates_lon_lat": [
      -104.72402,
      39.46434
    ]
  },
  {
    "id": "nhd-d55467f0-7114-4faf-a083-e3aff252fd30",
    "name": null,
    "area_sqkm": 0.054,
    "elevation_m": null,
    "coordinates_lon_lat": [
      -104.776708,
      39.515239
    ]
  },
  {
    "id": "nhd-117819477",
    "name": "Wakeman Reservoir",
    "area_sqkm": 0.058,
    "elevation_m": null,
    "coordinates_lon_lat": [
      -105.053864,
      39.438169
    ]
  },
  {
    "id": "nhd-117800481",
    "name": "Waucondah Reservoir",
    "area_sqkm": 0.07400000000000001,
    "elevation_m": null,
    "coordinates_lon_lat": [
      -104.985177,
      39.259497
    ]
  },
  {
    "id": "nhd-117844343",
    "name": "J O Hill Reservoir",
    "area_sqkm": 0.075,
    "elevation_m": null,
    "coordinates_lon_lat": [
      -105.160492,
      39.143258
    ]
  }
]
```

### Named artificial-path rivers over 2 km that are undrawn or under 80%

```json
[
  {
    "gnis_id": "00185007",
    "name": "Happy Canyon Creek",
    "artificial_path_length_km": 6.543,
    "drawn_artificial_path_length_km": 0.0,
    "drawn_fraction": 0.0,
    "group_ids": []
  },
  {
    "gnis_id": "00185092",
    "name": "Kinney Creek",
    "artificial_path_length_km": 4.668,
    "drawn_artificial_path_length_km": 0.0,
    "drawn_fraction": 0.0,
    "group_ids": []
  },
  {
    "gnis_id": "00185141",
    "name": "East Cherry Creek",
    "artificial_path_length_km": 2.448,
    "drawn_artificial_path_length_km": 0.0,
    "drawn_fraction": 0.0,
    "group_ids": [
      "nhd-gnis-00185141"
    ]
  },
  {
    "gnis_id": "00201759",
    "name": "South Platte River",
    "artificial_path_length_km": 9.514,
    "drawn_artificial_path_length_km": 0.0,
    "drawn_fraction": 0.0,
    "group_ids": []
  }
]
```

**PENDING_EXTERNAL_SOURCE_REFRESH:** Douglas South Platte River `00201759` is absent from the committed source bundle. Douglas counts and geometry will change when the padded NHD refresh lands.

## Reviewer notes

To be written by Codex after the padded refresh and checked by the coordinator.
