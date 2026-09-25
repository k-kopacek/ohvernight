"""Stage a complete run, validate it, then atomically replace one public bundle."""
import argparse
from contextlib import contextmanager
import datetime as dt
import importlib
import json
import os
from pathlib import Path
import tempfile
import uuid
from lib.access import VEHICLES, trip_dates
from lib.common import ROOT, write_fc
from lib.evidence import now
from lib.validation import validate_bundle
from lib.site_adapter import build_site_feed

STEPS = [
 ("01_fetch_land_ownership", True, ["land_ownership", "wilderness"]),
 ("02_fetch_mvum_roads", True, ["mvum_roads"]),
 ("03_fetch_hydrology", True, ["hydrology"]),
 ("04_fetch_campgrounds_ridb", False, ["lodging_developed"]),
 ("05_fetch_wildlife_closures", False, ["wildlife_sensitivity"]),
 ("06_fetch_fire_stage_monitor", False, ["fire_restriction_stage"]),
 ("07_build_dispersed_corridors", True, ["dispersed_corridors", "dispersed_corridor_points"]),
 ("08_ingest_leads", True, ["leads"]),
 ("09_reviewed_sites", True, ["reviewed_sites"]),
]

@contextmanager
def environment(values):
    previous = {k: os.environ.get(k) for k in values}
    os.environ.update(values)
    try:
        yield
    finally:
        for k,v in previous.items():
            if v is None: os.environ.pop(k, None)
            else: os.environ[k] = v

def execute_step(name):
    importlib.import_module(name).main()

def build(arrive, depart, vehicle="passenger_car", skip_optional=False, destination=None):
    trip_dates(arrive, depart)
    if vehicle not in VEHICLES:
        raise ValueError("Unsupported vehicle")
    destination = Path(destination or ROOT / "data/processed")
    destination.mkdir(parents=True, exist_ok=True)
    trip = {"arrive": arrive, "depart": depart, "vehicle": vehicle}
    statuses = {}
    # Same filesystem as destination ensures the final replace is atomic.
    with tempfile.TemporaryDirectory(prefix=".staging-", dir=destination) as scratch:
        with environment({"ASPEN_OUTPUT_DIR": scratch, "ASPEN_ARRIVE": arrive,
                          "ASPEN_DEPART": depart, "ASPEN_VEHICLE": vehicle}):
            for name, required, layers in STEPS:
                try:
                    if skip_optional and not required:
                        statuses[name] = {"status": "skipped", "reason": "Optional sources skipped by request"}
                        for layer in layers: write_fc(layer + ".geojson", [])
                        continue
                    print(f"Running {name}", flush=True)
                    execute_step(name)
                    for layer in layers:
                        if not (Path(scratch) / (layer+".geojson")).exists():
                            raise ValueError(f"Missing output layer: {layer}")
                    statuses[name] = {"status": "available", "completed_at": now()}
                except Exception as exc:
                    if required:
                        raise RuntimeError(f"Required step {name} failed; previous published data preserved: {exc}") from exc
                    statuses[name] = {"status": "unavailable", "reason": str(exc)[:500]}
                    print(f"Optional source unavailable: {name}: {exc}", flush=True)
                    for layer in layers: write_fc(layer + ".geojson", [])
            layers = {layer: json.loads((Path(scratch)/(layer+".geojson")).read_text())
                      for _,_,names in STEPS for layer in names}
            bundle = {"schema_version": 2, "run_id": str(uuid.uuid4()), "generated_at": now(),
                "trip": trip, "source_status": statuses, "layers": layers,
                "coverage_gaps": ["Site-specific orders are not exhaustively mapped",
                                 "Current road/snow conditions and availability are not automatically verified",
                                 "Limited-scale ownership does not establish a site's legal boundary"],
                "site_feed": build_site_feed(layers, trip)}
            validate_bundle(bundle)
            staged = Path(scratch) / "map-data-v2.json"
            staged.write_text(json.dumps(bundle, separators=(",", ":"), allow_nan=False))
            os.replace(staged, destination / "map-data-v2.json")
    print(f"Published validated research bundle: {destination / 'map-data-v2.json'}")
    return bundle

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--arrive", required=True, help="ISO arrival date")
    parser.add_argument("--depart", required=True, help="ISO departure date, included in access checks")
    parser.add_argument("--vehicle", choices=sorted(VEHICLES), default="passenger_car")
    parser.add_argument("--skip-slow-sources", action="store_true", help="Skip optional RIDB, wildlife and fire inputs")
    args = parser.parse_args()
    build(args.arrive, args.depart, args.vehicle, args.skip_slow_sources)

if __name__ == "__main__":
    main()
