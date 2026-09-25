import copy
import datetime as dt
import importlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from shapely.geometry import Point, LineString, box, mapping, shape
from pyproj import Geod
from lib.access import evaluate_access
from lib.arcgis_client import query_layer_geojson, describe_layer, get_json, ArcGISQueryError
from lib.common import write_fc
from lib.evidence import make_evidence
from lib.geo_utils import buffer_feet
from lib.site_adapter import build_site_feed
from lib.validation import validate_bundle
pipeline = importlib.import_module("run_pipeline")
corridors = importlib.import_module("07_build_dispersed_corridors")
leads = importlib.import_module("08_ingest_leads")
review = importlib.import_module("09_reviewed_sites")
roads = importlib.import_module("02_fetch_mvum_roads")
land = importlib.import_module("01_fetch_land_ownership")

def ev():
    return make_evidence("https://example.org/source", "Test source")

def feature(geom, **p):
    return {"type":"Feature", "geometry":json.loads(json.dumps(mapping(geom))), "properties":{"id":"fixture","evidence":ev(), **p}}

def fc(*features):
    return {"type":"FeatureCollection", "features":list(features)}

class Response:
    def __init__(self, value): self.value = value
    def raise_for_status(self): pass
    def json(self): return self.value

class Service:
    def __init__(self, broken=False): self.broken = broken
    def get(self, url, params, timeout):
        if not url.endswith("/query"):
            return Response({"type":"Feature Layer", "fields":[{"name":"OBJECTID","type":"esriFieldTypeOID"}], "maxRecordCount":100})
        if params.get("returnCountOnly"): return Response({"count":2})
        if params.get("returnIdsOnly"): return Response({"objectIds":[1,2]})
        ids = [int(x) for x in params["objectIds"].split(",")]
        if len(ids)>1: return Response({**fc(), "exceededTransferLimit":True})
        rows = [feature(Point(-106.8,39.2), OBJECTID=i) for i in ids]
        if self.broken: rows = []
        return Response(fc(*rows))

class RegressionTests(unittest.TestCase):
    def test_buffer_distance_independent_geodesic(self):
        point = Point(-106.82,39.19)
        geod = Geod(ellps="WGS84")
        for feet in (100,300):
            ring = buffer_feet(point,feet)
            for lon,lat in ring.exterior.coords:
                meters = geod.inv(point.x,point.y,lon,lat)[2]
                self.assertAlmostEqual(meters / .3048,feet,delta=.3)

    def test_vehicle_specific_season_and_whole_trip(self):
        props = {"symbol":4,"passengervehicle":"open","passengervehicle_datesopen":"05/27-09/26"}
        self.assertEqual(evaluate_access(props,"2027-01-15","2027-01-17","passenger_car")[0],"restricted")
        self.assertEqual(evaluate_access(props,"2026-09-25","2026-09-27","passenger_car")[0],"restricted")
        self.assertEqual(evaluate_access(props,"2026-09-24","2026-09-25","passenger_car")[0],"designated_open")
        self.assertEqual(evaluate_access(props,"2026-09-24","2026-09-25","motorhome")[0],"unknown")

    def test_missing_or_malformed_season_stays_unknown(self):
        for dates in (None,"","bad","05/01-10/31 plus exceptions"):
            props={"symbol":2,"passengervehicle":"open","passengervehicle_datesopen":dates}
            self.assertEqual(evaluate_access(props,"2027-01-15","2027-01-17","passenger_car")[0],"unknown")
        self.assertEqual(evaluate_access({"symbol":1},"2027-01-15","2027-01-17","passenger_car")[0],"unknown")

    def test_wrapping_seasons_multiple_windows_and_leap_day(self):
        p={"symbol":2,"passengervehicle":"open","passengervehicle_datesopen":"11/01-03/31"}
        self.assertEqual(evaluate_access(p,"2027-12-30","2028-01-02","passenger_car")[0],"designated_open")
        p["passengervehicle_datesopen"]="02/29-03/02;06/01-07/01"
        self.assertEqual(evaluate_access(p,"2028-02-29","2028-03-01","passenger_car")[0],"designated_open")
        self.assertEqual(evaluate_access(p,"2028-03-02","2028-06-01","passenger_car")[0],"restricted")

    def test_real_mvum_fields_preserved(self):
        data=fc(feature(LineString([(-106.82,39.19),(-106.81,39.19)]),
                        objectid=12,name="Actual road",symbol="4",passengervehicle="open",
                        passengervehicle_datesopen="05/27-09/26"))
        src={"base_url":"https://example.org/MapServer","layer":1,"agency":"USFS"}
        p=roads.normalize(data,src,"2027-01-15","2027-01-17","passenger_car")[0]["properties"]
        self.assertEqual(p["id"],"mvum-12")
        self.assertEqual(p["name"],"Actual road")
        self.assertEqual(p["access_status"],"restricted")
        self.assertEqual(p["vehicle_class"],"highway_legal")

    def test_land_manager_does_not_authorize_camping(self):
        data=fc(feature(box(-106.83,39.18,-106.81,39.20),OBJECTID=1,ADMIN_AGENCY_CODE="USFS"))
        p=land.normalize(data,{"base_url":"https://example.org","layer":1,"agency":"BLM"})[0]["properties"]
        self.assertEqual(p["camping_permission"],"unknown")
        self.assertEqual(p["land_class"],"unknown")

    def test_group_layer_rejected_cleanly(self):
        class Group:
            def get(self,*args,**kwargs): return Response({"type":"Group Layer","fields":None})
        with self.assertRaisesRegex(ArcGISQueryError,"not a queryable"):
            describe_layer("https://example.org",0,session=Group())

    def test_arcgis_short_transfer_split_retrieves_all_ids(self):
        rows=query_layer_geojson("https://example.org",1,(-107,39,-106,40),session=Service())
        self.assertEqual(len(rows["features"]),2)

    def test_arcgis_incomplete_batch_fails(self):
        with self.assertRaisesRegex(ArcGISQueryError,"Missing/duplicate"):
            query_layer_geojson("https://example.org",1,(-107,39,-106,40),session=Service(True))

    def test_arcgis_retries_transient_json_error(self):
        class Flaky:
            calls = 0
            def get(self, *args, **kwargs):
                self.calls += 1
                return Response({"error":{"code":500}} if self.calls < 3 else {"count":2})
        client = Flaky()
        with patch("lib.arcgis_client.time.sleep"):
            self.assertEqual(get_json(client,"https://example.org",{}),{"count":2})
        self.assertEqual(client.calls,3)

    def test_count_failure_still_requires_complete_features(self):
        class NoCount(Service):
            def get(self, url, params, timeout):
                if params.get("returnCountOnly"): return Response({"error":{"code":500}})
                return super().get(url, params, timeout)
        with patch("lib.arcgis_client.time.sleep"):
            self.assertEqual(len(query_layer_geojson("https://example.org",1,(-107,39,-106,40),session=NoCount())["features"]),2)
            with self.assertRaisesRegex(ArcGISQueryError,"Missing/duplicate"):
                query_layer_geojson("https://example.org",1,(-107,39,-106,40),session=NoCount(True))

    def test_truncated_id_list_is_rejected(self):
        class Truncated(Service):
            def get(self, url, params, timeout):
                if params.get("returnIdsOnly"): return Response({"objectIds":[1,2],"exceededTransferLimit":True})
                return super().get(url, params, timeout)
        with self.assertRaisesRegex(ArcGISQueryError,"Truncated object-ID"):
            query_layer_geojson("https://example.org",1,(-107,39,-106,40),session=Truncated())

    def test_candidate_excludes_adjacent_wilderness_water_and_private(self):
        road=feature(LineString([(-106.84,39.19),(-106.81,39.19)]),id="road1",name="Test",
                     access_status="designated_open",evaluated_trip={"arrive":"2027-01-15","depart":"2027-01-17","vehicle":"passenger_car"})
        public=box(-106.85,39.18,-106.82,39.20)
        wilderness=box(-106.835,39.1901,-106.825,39.20)
        water=Point(-106.843,39.19)
        rows=corridors.build(fc(feature(public,manager="USFS")),fc(road),fc(feature(water)),
              fc(feature(wilderness)),{"road_buffer_ft":300,"water_setback_ft":100,"required_checks":["orders"]})
        self.assertTrue(rows)
        geometry=shape(rows[0]["geometry"])
        self.assertLess(geometry.difference(public).area,1e-12)
        self.assertLess(geometry.intersection(wilderness).area,1e-12)
        self.assertFalse(geometry.contains(water))
        self.assertTrue(rows[0]["properties"]["needs_review"])
        self.assertEqual(rows[0]["properties"]["camping_permission"],"unknown")

    def test_lead_in_candidate_never_upgrades_confidence(self):
        data=[feature(box(-106.9,39.1,-106.8,39.2),id="candidate")]
        row=leads.normalize([{"lon":-106.85,"lat":39.15,"name":"Lead"}],data)[0]
        self.assertEqual(row["properties"]["evidence"]["confidence"],"unverified")
        self.assertEqual(row["properties"]["matched_candidate_ids"],["candidate"])

    def test_required_failure_preserves_previous_bundle(self):
        with tempfile.TemporaryDirectory() as path:
            previous=Path(path)/"map-data-v2.json";previous.write_text('{"previous":true}')
            with patch.object(pipeline,"execute_step",side_effect=ValueError("broken feed")):
                with self.assertRaisesRegex(RuntimeError,"preserved"):
                    pipeline.build("2027-01-15","2027-01-17",destination=path)
            self.assertEqual(previous.read_text(),'{"previous":true}')

    def test_optional_failure_is_explicit_and_never_reuses_old_layer(self):
        def execute(name):
            if name=="04_fetch_campgrounds_ridb": raise RuntimeError("no API key")
            for step,_,layers in pipeline.STEPS:
                if step==name:
                    for layer in layers: write_fc(layer+".geojson",[])
        with tempfile.TemporaryDirectory() as path:
            (Path(path)/"lodging_developed.geojson").write_text('{"obsolete":true}')
            with patch.object(pipeline,"execute_step",side_effect=execute):
                result=pipeline.build("2027-01-15","2027-01-17",destination=path)
            self.assertEqual(result["layers"]["lodging_developed"]["features"],[])
            self.assertEqual(result["source_status"]["04_fetch_campgrounds_ridb"]["status"],"unavailable")
            bad=copy.deepcopy(result)
            bad["layers"]["dispersed_corridor_points"]=fc(feature(Point(-106.82,39.19)))
            with self.assertRaisesRegex(ValueError,"Synthetic"): validate_bundle(bad)

    def test_curated_site_expires_and_requires_all_claims(self):
        review_data={"checked_on":"2026-09-24","expires_on":"2026-10-01",
            "valid_from":"2027-01-01","valid_to":"2027-01-31","vehicles":["passenger_car"],
            "sleeping_setup":"inside_vehicle","actual_site_confirmed":True,
            "claims":{k:{"status":"supported","source_url":"https://example.org/rule"} for k in review.CLAIMS}}
        row=feature(Point(-106.82,39.19),name="Reviewed site",review=review_data)
        ok=review.normalize([row],"2027-01-15","2027-01-17","passenger_car",today=dt.date(2026,9,24))[0]
        self.assertEqual(ok["properties"]["camping_permission"],"supported_for_trip")
        stale=review.normalize([row],"2027-01-15","2027-01-17","passenger_car",today=dt.date(2026,10,2))[0]
        self.assertTrue(stale["properties"]["needs_review"])
        del review_data["claims"]["vehicle_sleeping"]
        missing=review.normalize([row],"2027-01-15","2027-01-17","passenger_car",today=dt.date(2026,9,24))[0]
        self.assertTrue(missing["properties"]["needs_review"])
        blocked=review.normalize([ok],"2027-01-15","2027-01-17","passenger_car",
            today=dt.date(2026,9,24),restrictions=[box(-106.83,39.18,-106.81,39.20)])[0]
        self.assertIn("active_mapped_restriction",blocked["properties"]["review_reasons"])

    def test_candidate_and_leads_cannot_become_site_feed_pins(self):
        layers={"reviewed_sites":fc(),"lodging_developed":fc(),
                "dispersed_corridors":fc(feature(box(-106.9,39.1,-106.8,39.2)))}
        self.assertEqual(build_site_feed(layers,{})["places"],[])
