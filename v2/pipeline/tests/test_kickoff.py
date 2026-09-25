import datetime as dt
import importlib
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from shapely.geometry import shape, Point
from lib.arcgis_client import native_features, ArcGISQueryError
from lib.common import aoi
from lib.rules import match_rules
import check_ridb
from test_pipeline import Service, Response
from lib.arcgis_client import query_layer_geojson

class KickoffTests(unittest.TestCase):
    def test_native_hole_and_island_ignore_ring_order(self):
        rings = [
            [[2,2],[2,8],[8,8],[8,2],[2,2]],
            [[0,0],[0,10],[10,10],[10,0],[0,0]],
            [[4,4],[4,6],[6,6],[6,4],[4,4]]]
        payload={"spatialReference":{"wkid":4326},"features":[{"attributes":{"OBJECTID":9},"geometry":{"rings":rings}}]}
        result=native_features(payload)[0]
        geom=shape(result["geometry"])
        self.assertEqual(geom.area,68)
        self.assertTrue(geom.contains(Point(5,5)))
        self.assertFalse(geom.contains(Point(3,3)))
        self.assertEqual(result["properties"]["OBJECTID"],9)

    def test_native_self_touching_ring_repaired(self):
        payload={"spatialReference":{"wkid":4326},"features":[{"attributes":{},"geometry":{"rings":[[[0,0],[2,2],[0,2],[2,0],[0,0]]]}}]}
        geom=shape(native_features(payload)[0]["geometry"])
        self.assertTrue(geom.is_valid)
        self.assertEqual(geom.area,2)

    def test_native_unknown_projection_rejected(self):
        for sr in ({},{"wkid":3857}):
            with self.assertRaises(ArcGISQueryError):
                native_features({"spatialReference":sr,"features":[]})

    def test_native_id_completeness_is_still_enforced(self):
        class Native(Service):
            def get(self,url,params,timeout):
                if params.get("objectIds"):
                    ids=[int(v) for v in params["objectIds"].split(",")]
                    return Response({"spatialReference":{"wkid":4326},"features":[{"attributes":{"OBJECTID":i},"geometry":{"x":-106.8,"y":39.2}} for i in ids]})
                return super().get(url,params,timeout)
        self.assertEqual(len(query_layer_geojson("https://example.org",1,(-107,39,-106,40),session=Native(),native_json=True)["features"]),2)

    def test_aoi_covers_lincoln_creek_agency_coordinate(self):
        self.assertTrue(aoi().covers(Point(-106.691097,39.115492)))

    def test_rule_staleness_and_no_permission_inheritance(self):
        current=match_rules(place_id="lincolncreek",at=dt.datetime(2026,9,26,tzinfo=dt.timezone.utc))[0]
        self.assertEqual(current["stay_limit_days"],5)
        self.assertEqual(current["camping_permission"],"unknown")
        self.assertEqual(current["freshness"],"current")
        self.assertEqual(match_rules(road_name="SOME OTHER ROAD"),[])
        self.assertEqual(match_rules(place_id="lincolncreek",at=dt.datetime(2027,1,1,tzinfo=dt.timezone.utc))[0]["freshness"],"stale")

    def test_missing_key_does_not_make_request(self):
        with patch.dict(os.environ,{},clear=True):
            with self.assertRaises(check_ridb.ridb.MissingCredentials):
                check_ridb.smoke()

    def test_ridb_count_change_is_rejected(self):
        class Changed:
            calls=0
            def get(self,*args,**kwargs):
                self.calls+=1
                return Response({"RECDATA":[{"FacilityID":self.calls}],"METADATA":{"RESULTS":{"TOTAL_COUNT":2 if self.calls==1 else 3}}})
        with patch.dict(os.environ,{"RIDB_API_KEY":"test-placeholder"}):
            with self.assertRaisesRegex(ValueError,"count changed"):
                check_ridb.ridb.fetch_facilities(Changed())

    def test_ridb_export_preserves_previous_on_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            out=Path(directory)/"ridb-options.json"
            out.write_text('{"previous":true}')
            with patch.object(check_ridb.ridb,"fetch_facilities",side_effect=ValueError("broken")):
                with self.assertRaises(ValueError):check_ridb.export(out)
            self.assertEqual(out.read_text(),'{"previous":true}')

    def test_export_has_no_permission_or_live_availability_claim(self):
        facilities=[{"FacilityID":101,"FacilityName":"Test Camp","FacilityLatitude":39.15,"FacilityLongitude":-106.8,"FacilityReservationURL":"javascript:bad","Reservable":True}]
        with tempfile.TemporaryDirectory() as directory:
            out=Path(directory)/"ridb-options.json"
            with patch.object(check_ridb.ridb,"fetch_facilities",return_value=facilities):
                self.assertEqual(check_ridb.export(out),1)
            place=json.loads(out.read_text())["places"][0]
            self.assertTrue(place["source"].startswith("https://www.recreation.gov/search?"))
            self.assertEqual(place["camping_permission"],"unknown")
            self.assertEqual(place["facts"]["restrictions"]["status"],"unknown")

if __name__=="__main__":unittest.main()
