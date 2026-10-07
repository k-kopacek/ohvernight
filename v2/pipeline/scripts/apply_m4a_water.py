"""Apply an already reviewed M4-A staged NHD refresh to canonical water layers."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from build_display import build_region
from lib.water import splice_layer

SCRIPTS = Path(__file__).resolve().parent
PIPELINE = SCRIPTS.parent
V2 = PIPELINE.parent
SOURCE_FIELDS = {
    "aspen": ["gnis_id", "source_id", "ftype", "fcode", "reach_code", "length_km", "area_sqkm",
               "elevation_ft", "visibility_filter", "waterbody_source_id", "source_date"],
    "flowline": ["gnis_id", "source_id", "ftype", "fcode", "reach_code", "length_km",
                  "visibility_filter", "waterbody_source_id", "source_date"],
    "waterbody": ["gnis_id", "source_id", "ftype", "fcode", "reach_code", "area_sqkm",
                   "elevation_ft", "visibility_filter", "source_date"],
}
DERIVED_FIELDS = ["source_namespace", "source_layer", "water_class", "hydro_category", "legacy_ids"]


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value, *, indent=None):
    path.write_text(json.dumps(value, ensure_ascii=False, separators=None if indent else (",", ":"),
                                indent=indent, allow_nan=False) + "\n", encoding="utf-8")


def set_retrieved_at(features, retrieved_at):
    for feature in features:
        evidence = feature.get("properties", {}).get("evidence")
        if isinstance(evidence, dict):
            evidence["retrieved_at"] = retrieved_at


def apply_refresh(report_path: Path, v2_root: Path = V2):
    report_path = Path(report_path)
    report = read_json(report_path)
    if not report.get("acceptable_differences_only") or any(
            value.get("stop_required") for value in report.get("differences", {}).values()):
        raise ValueError("refusing to apply a refresh with unexplained differences")
    staging = report_path.parent
    retrieved_at = report["retrieved_at_utc"]
    changed = []

    aspen_path = v2_root / "map-data-v2.json"
    aspen = read_json(aspen_path)
    hydrology = read_json(staging / "aspen-flowline.geojson")["features"]
    hydrology.extend(read_json(staging / "aspen-area.geojson")["features"])
    hydrology.extend(read_json(staging / "aspen-waterbody.geojson")["features"])
    set_retrieved_at(hydrology, retrieved_at)
    aspen = splice_layer(aspen, "hydrology", {"type": "FeatureCollection", "features": hydrology})
    status = aspen.setdefault("source_status", {}).setdefault("03_fetch_hydrology", {"status": "available"})
    status.update(status="available", last_retrieved_at=retrieved_at, last_checked_at=retrieved_at,
                  count=len(hydrology))
    write_json(aspen_path, aspen)
    changed.append(str(aspen_path))

    douglas_path = v2_root / "regions/douglas-co/research.json"
    douglas = read_json(douglas_path)
    waterways = read_json(staging / "douglas-co-flowline.geojson")["features"]
    waterbodies = read_json(staging / "douglas-co-waterbody.geojson")["features"]
    set_retrieved_at(waterways, retrieved_at)
    set_retrieved_at(waterbodies, retrieved_at)
    douglas["layers"] = dict(douglas["layers"])
    douglas["layers"]["waterways"] = {"type": "FeatureCollection", "features": waterways}
    douglas["layers"]["waterbodies"] = {"type": "FeatureCollection", "features": waterbodies}
    douglas.setdefault("source_status", {})["waterways"] = {
        "status": "available", "retrieved_at": retrieved_at, "count": len(waterways)}
    douglas["source_status"]["waterbodies"] = {
        "status": "available", "retrieved_at": retrieved_at, "count": len(waterbodies)}
    write_json(douglas_path, douglas)
    changed.append(str(douglas_path))

    aspen_manifest_path = v2_root / "regions/aspen/region.json"
    aspen_manifest = read_json(aspen_manifest_path)
    water = next(layer for layer in aspen_manifest["layers"] if layer["id"] == "hydrology")
    water["fields"] = {"source": SOURCE_FIELDS["aspen"],
                       "derived": DERIVED_FIELDS + ["kind"]}
    aspen_manifest["sources"]["usgs_nhd"]["scope"] = (
        "NHD source geometry and retained source attributes for flowlines, areas and waterbodies. "
        "Source classification does not establish recreation, access or permission.")
    write_json(aspen_manifest_path, aspen_manifest, indent=2)
    changed.append(str(aspen_manifest_path))

    douglas_manifest_path = v2_root / "regions/douglas-co/region.json"
    douglas_manifest = read_json(douglas_manifest_path)
    for layer in douglas_manifest["layers"]:
        if layer["id"] not in {"waterways", "waterbodies"}:
            continue
        source_layer = "flowline" if layer["id"] == "waterways" else "waterbody"
        layer["fields"] = {"source": SOURCE_FIELDS[source_layer],
                           "derived": DERIVED_FIELDS + (["support_for", "support_reason"]
                                                        if source_layer == "flowline" else [])}
    douglas_manifest["sources"]["usgs_nhd"]["scope"] = (
        "NHD source geometry and retained source attributes; Douglas flowlines are named with only "
        "reviewed supporting bridges, and all waterbodies are retained. Classification does not "
        "establish recreation, access or permission.")
    write_json(douglas_manifest_path, douglas_manifest, indent=2)
    changed.append(str(douglas_manifest_path))

    for region_id in ("aspen", "douglas-co"):
        built = build_region(region_id, v2_root, write=True)
        changed.extend(str(v2_root / relative) for relative in built["artifacts"])
    after_hashes = {
        "map-data-v2.json": hashlib.sha256(aspen_path.read_bytes()).hexdigest(),
        "regions/douglas-co/research.json": hashlib.sha256(douglas_path.read_bytes()).hexdigest(),
    }
    report["canonical_sha256_after"] = after_hashes
    for key, snapshot in report.get("snapshots", {}).items():
        path = "map-data-v2.json" if key.startswith("aspen/") else "regions/douglas-co/research.json"
        snapshot["sha256_after"] = after_hashes[path]
    write_json(report_path, report, indent=2)
    print(json.dumps({"retrieved_at_utc": retrieved_at, "changed_paths": changed}, indent=2))
    return changed


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", type=Path, help="refresh-report.json produced by refresh_m4a_water.py")
    parser.add_argument("--apply", action="store_true", help="write canonical files and rebuild displays")
    args = parser.parse_args()
    report = read_json(args.report)
    if not report.get("acceptable_differences_only"):
        raise SystemExit("staged differences require review; canonical data not written")
    if not args.apply:
        print("Refresh report is eligible to apply. Re-run with --apply after reviewing its complete differences.")
        return
    apply_refresh(args.report)


if __name__ == "__main__":
    main()
