import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from shapely.geometry import LineString, Polygon, box, mapping

V2 = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(V2 / "pipeline" / "scripts"))

import refresh_m4a_water as m4a  # noqa: E402
from lib.evidence import make_evidence  # noqa: E402
from lib.water import group_flowlines, normalize_feature, select_water_features  # noqa: E402
from refresh_m4b_douglas_water import (  # noqa: E402
    _derive_flowlines,
    _is_named_flowline,
)


EVIDENCE = make_evidence("https://hydro.example/6", "USGS", "high", "arcgis_rest_query")
PADDED = box(-106, 38, -104, 40)


def raw(ident, geometry, *, name=None, gnis=None, ftype=460, fcode=46006,
        layer="flowline", area=None):
    props = {
        "permanent_identifier": ident,
        "gnis_id": gnis,
        "gnis_name": name,
        "ftype": ftype,
        "fcode": fcode,
        "reachcode": None,
        "lengthkm": 1.0,
        "visibilityfilter": None,
        "wbarea_permanent_identifier": None,
        "fdate": None,
        "areasqkm": area,
        "elevation": None,
    }
    return {"type": "Feature", "geometry": mapping(geometry), "properties": props}


class DouglasObjectIdRefreshTests(unittest.TestCase):
    def test_local_filter_matches_old_server_predicate_including_empty_and_null(self):
        rows = [raw("named", LineString([(-105, 39), (-104.9, 39)]), name="River"),
                raw("empty", LineString([(-105, 39), (-104.9, 39)]), name=""),
                raw("null", LineString([(-105, 39), (-104.9, 39)]), name=None),
                raw("spaces", LineString([(-105, 39), (-104.9, 39)]), name="  ")]
        old_server_result = {row["properties"]["permanent_identifier"] for row in rows
                             if row["properties"]["gnis_name"] is not None
                             and row["properties"]["gnis_name"] != ""}
        local_result = {row["properties"]["permanent_identifier"] for row in rows
                        if _is_named_flowline(row)}
        self.assertEqual(local_result, old_server_result)
        self.assertEqual(local_result, {"named", "spaces"})
        self.assertFalse(_is_named_flowline(rows[1]))
        self.assertFalse(_is_named_flowline(rows[2]))

    def test_only_named_rows_and_kept_o1_bridge_survive_local_flowline_derivation(self):
        rows = [
            raw("named-a", LineString([(-105, 39), (-104.999, 39)]), name="River", gnis="0001"),
            raw("named-b", LineString([(-104.998, 39), (-104.997, 39)]), name="River", gnis="0001"),
            raw("bridge", LineString([(-104.999, 39), (-104.998, 39)]), gnis="0001"),
            raw("not-bridge", LineString([(-104.9993, 39.001), (-104.9992, 39.001)]), gnis="0001"),
            raw("unnamed-stream", LineString([(-104.8, 39), (-104.7, 39)]), gnis="9999"),
        ]
        canonical, counts = _derive_flowlines(rows, PADDED, EVIDENCE)
        by_source = {feature["properties"]["source_id"]: feature for feature in canonical}
        self.assertEqual(set(by_source), {"named-a", "named-b", "bridge"})
        self.assertEqual(by_source["bridge"]["properties"]["support_for"], "0001")
        self.assertEqual(by_source["bridge"]["properties"]["support_reason"], "bridges_named_parts")
        self.assertEqual(counts["named_flowlines"], 2)
        self.assertEqual(counts["supporting_features_kept"], 1)
        self.assertEqual(counts["unnamed_discarded"], 2)

    def test_saved_full_extent_discovery_stops_on_duplicate_object_ids(self):
        prior_metadata = dict(m4a.LAYER_METADATA)
        m4a.LAYER_METADATA[6] = {
            "fields": [{"name": "OBJECTID", "type": "esriFieldTypeOID"}],
            "maxRecordCount": 250,
        }
        try:
            with tempfile.TemporaryDirectory() as directory, patch.object(
                    m4a, "get_json", side_effect=[{"count": 2}, {"objectIds": [7, 7]}]):
                with self.assertRaisesRegex(m4a.ArcGISQueryError, "count and complete ID set disagree"):
                    m4a.controlled_layer_query(
                        object(), "douglas-co", "flowline", 6, (-1, -1, 1, 1),
                        "1=1", m4a.OUT_FIELDS["flowline"], Path(directory),
                        "flowline", count_id_timeout=180)
                self.assertFalse(list(Path(directory).glob("*-plan.json")))
        finally:
            m4a.LAYER_METADATA.clear()
            m4a.LAYER_METADATA.update(prior_metadata)

    def test_selection_and_grouping_cannot_draw_or_display_excluded_water(self):
        rows = [
            raw("river-a", LineString([(-105, 39), (-104.999, 39)]), name="River", gnis="0001"),
            raw("river-b", LineString([(-104.998, 39), (-104.997, 39)]), name="River", gnis="0001"),
            raw("river-bridge", LineString([(-104.999, 39), (-104.998, 39)]), gnis="0001"),
            raw("unnamed-stream", LineString([(-104.8, 39), (-104.7, 39)]), gnis="9001"),
            raw("intermittent", LineString([(-104.6, 39), (-104.5, 39)]), name="Seasonal", gnis="9002",
                fcode=46003),
            raw("canal", LineString([(-104.5, 39), (-104.4, 39)]), name="Canal", gnis="9003",
                ftype=336, fcode=33600),
            raw("ditch", LineString([(-104.4, 39), (-104.3, 39)]), name="Ditch", gnis="9004",
                ftype=336, fcode=33600),
            raw("pipeline", LineString([(-104.3, 39), (-104.2, 39)]), name="Pipeline", gnis="9005",
                ftype=428, fcode=42803),
            raw("connector", LineString([(-104.2, 39), (-104.1, 39)]), name="Connector", gnis="9006",
                ftype=334, fcode=33400),
        ]
        flowlines, counts = _derive_flowlines(rows, PADDED, EVIDENCE)
        waterbodies = []
        for row in (
            raw("intermittent-lake", Polygon([(-105, 39), (-104.999, 39), (-104.999, 39.001),
                                               (-105, 39.001), (-105, 39)]), name="Seasonal Lake",
                ftype=390, fcode=39001, layer="waterbody", area=2),
            raw("ineligible-reservoir", Polygon([(-104.99, 39), (-104.989, 39), (-104.989, 39.001),
                                                 (-104.99, 39.001), (-104.99, 39)]), name="Treatment Pond",
                ftype=436, fcode=43624, layer="waterbody", area=2),
            raw("swamp", Polygon([(-104.98, 39), (-104.979, 39), (-104.979, 39.001),
                                  (-104.98, 39.001), (-104.98, 39)]), name="Marsh",
                ftype=466, fcode=46600, layer="waterbody", area=2),
            raw("unnamed-small-lake", Polygon([(-104.97, 39), (-104.969, 39), (-104.969, 39.001),
                                               (-104.97, 39.001), (-104.97, 39)]), name=None,
                ftype=390, fcode=39004, layer="waterbody", area=0.01),
        ):
            waterbodies.append(normalize_feature("waterbody", row, row["geometry"], EVIDENCE))

        selected_flow = select_water_features(flowlines)
        selected_bodies = select_water_features(waterbodies)
        grouped = group_flowlines(flowlines, region_id="douglas-co", enforce_major=False)
        drawn_ids = {ident for ids in grouped["water_groups"].values() for ident in ids}
        self.assertEqual(drawn_ids, {"nhd-river-a", "nhd-river-b"})
        self.assertEqual({feature["properties"]["id"] for feature in grouped["groups"]},
                         {"nhd-gnis-0001"})
        self.assertEqual(counts["supporting_features_kept"], 1)
        self.assertNotIn("unnamed-stream", {feature["properties"]["source_id"] for feature in flowlines})
        self.assertFalse(any(row["eligible"] for row in selected_flow
                             if row["feature"]["properties"]["source_id"] not in {"river-a", "river-b"}))
        # Waterbody display artifacts are built from eligible selections;
        # none of these four records can enter that displayed set.
        displayed_waterbody_ids = {row["feature"]["properties"]["id"]
                                   for row in selected_bodies if row["eligible"]}
        self.assertEqual(displayed_waterbody_ids, set())
        self.assertEqual({row["feature"]["properties"]["source_id"] for row in selected_bodies},
                         {"intermittent-lake", "ineligible-reservoir", "swamp", "unnamed-small-lake"})


if __name__ == "__main__":
    unittest.main()
