"""Apply an already reviewed M4-A staged NHD refresh to canonical water layers."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

from build_display import build_region
from lib.water import splice_layer

SCRIPTS = Path(__file__).resolve().parent
PIPELINE = SCRIPTS.parent
V2 = PIPELINE.parent
SOURCE_FIELDS = {
    "aspen": ["gnis_id", "source_id", "ftype", "fcode", "reach_code", "length_km", "area_sqkm",
               "elevation_m", "visibility_filter", "waterbody_source_id", "source_date"],
    "flowline": ["gnis_id", "source_id", "ftype", "fcode", "reach_code", "length_km",
                  "visibility_filter", "waterbody_source_id", "source_date"],
    "waterbody": ["gnis_id", "source_id", "ftype", "fcode", "reach_code", "area_sqkm",
                   "elevation_m", "visibility_filter", "source_date"],
}
DERIVED_FIELDS = ["source_namespace", "source_layer", "water_class", "hydro_category", "legacy_ids"]


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value, *, indent=None):
    path.write_text(json.dumps(value, ensure_ascii=False, separators=None if indent else (",", ":"),
                                indent=indent, allow_nan=False) + "\n", encoding="utf-8")


def write_region_manifest(path: Path, manifest, water_layer_ids):
    """Update only the source and water-layer lines in the compact manifests."""
    lines = path.read_text(encoding="utf-8").splitlines()
    source_found = False
    layer_ids_found = set()
    for index, line in enumerate(lines):
        if '"usgs_nhd":' in line:
            indent = line[:len(line) - len(line.lstrip())]
            comma = "," if line.rstrip().endswith(",") else ""
            value = json.dumps(manifest["sources"]["usgs_nhd"], ensure_ascii=False,
                               separators=(", ", ": "))
            lines[index] = f'{indent}"usgs_nhd": {value}{comma}'
            source_found = True
            continue
        for layer in manifest["layers"]:
            layer_id = layer.get("id")
            if layer_id not in water_layer_ids or not re.match(
                    r'^\s*\{"id":\s*"' + re.escape(layer_id) + r'"', line):
                continue
            indent = line[:len(line) - len(line.lstrip())]
            comma = "," if line.rstrip().endswith(",") else ""
            lines[index] = indent + json.dumps(layer, ensure_ascii=False, separators=(", ", ": ")) + comma
            layer_ids_found.add(layer_id)
            break
    if not source_found or layer_ids_found != set(water_layer_ids):
        raise ValueError("manifest is not in the expected compact line format; no manifest written")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


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
    write_region_manifest(aspen_manifest_path, aspen_manifest, {"hydrology"})
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
    write_region_manifest(douglas_manifest_path, douglas_manifest, {"waterways", "waterbodies"})
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


def apply_douglas_padded_refresh(report_path: Path, v2_root: Path = V2):
    """Apply only the coordinator-reviewed M4-B Douglas padded-water stage."""
    report_path = Path(report_path)
    report = read_json(report_path)
    if (not report.get("acceptable_differences_only") or
            set(report.get("differences", {})) != {"waterways", "waterbodies"} or
            any(not row.get("explained") for row in report["differences"].values()) or
            report.get("legacy_ids_missing") or report.get("legacy_ids_duplicate")):
        raise ValueError("refusing to apply a Douglas refresh with unexplained differences")

    staging = report_path.parent
    path = v2_root / "regions/douglas-co/research.json"
    from refresh_m4b_douglas_water import preservation_hashes
    preservation_before = preservation_hashes(v2_root)
    if preservation_before != report.get("preservation_hashes_before"):
        raise ValueError("refusing to apply: non-water or Aspen inputs changed since staging")
    if hashlib.sha256(path.read_bytes()).hexdigest() != report.get("before_sha256"):
        raise ValueError("refusing to apply: Douglas canonical input changed since staging")
    bundle = read_json(path)
    waterways = read_json(staging / "douglas-co-flowline.geojson")["features"]
    waterbodies = read_json(staging / "douglas-co-waterbody.geojson")["features"]
    retrieved_at = report["retrieved_at_utc"]
    for feature in waterways + waterbodies:
        evidence = feature.get("properties", {}).get("evidence")
        if isinstance(evidence, dict):
            evidence["retrieved_at"] = retrieved_at
    bundle["layers"] = dict(bundle["layers"])
    bundle["layers"]["waterways"] = {"type": "FeatureCollection", "features": waterways}
    bundle["layers"]["waterbodies"] = {"type": "FeatureCollection", "features": waterbodies}
    bundle.setdefault("source_status", {})["waterways"] = {
        "status": "available", "retrieved_at": retrieved_at, "count": len(waterways)}
    bundle["source_status"]["waterbodies"] = {
        "status": "available", "retrieved_at": retrieved_at, "count": len(waterbodies)}
    write_json(path, bundle)

    manifest_path = v2_root / "regions/douglas-co/region.json"
    lines = manifest_path.read_text(encoding="utf-8").splitlines()
    found = set()
    for index, line in enumerate(lines):
        if not line.lstrip().startswith('{"id": "waterways"') and not line.lstrip().startswith('{"id": "waterbodies"'):
            continue
        layer_id = "waterways" if '"id": "waterways"' in line else "waterbodies"
        updated, count = re.subn(r'("extent_padding_deg":\s*)[0-9.]+', r'\g<1>0.005', line, count=1)
        if count != 1:
            raise ValueError(f"could not set Douglas {layer_id} extent padding")
        lines[index] = updated
        found.add(layer_id)
    if found != {"waterways", "waterbodies"}:
        raise ValueError("Douglas water layer declarations were not both found")
    manifest_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    built = build_region("douglas-co", v2_root, write=True)
    report["canonical_sha256_after"] = hashlib.sha256(path.read_bytes()).hexdigest()
    preservation_after = preservation_hashes(v2_root)
    if preservation_after != preservation_before:
        raise ValueError("non-water or Aspen preservation hash changed during Douglas apply")
    report["preservation_hashes_after"] = preservation_after
    report["display_build_artifacts"] = sorted(built["artifacts"])
    write_json(report_path, report, indent=2)
    print(json.dumps({"retrieved_at_utc": retrieved_at,
                      "changed_paths": [str(path), str(manifest_path),
                                        *[str(v2_root / item) for item in built["artifacts"]]],
                      "canonical_sha256_after": report["canonical_sha256_after"]}, indent=2))
    return [path, manifest_path, *[v2_root / item for item in built["artifacts"]]]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", type=Path, help="refresh-report.json produced by refresh_m4a_water.py")
    parser.add_argument("--apply", action="store_true", help="write canonical files and rebuild displays")
    parser.add_argument("--douglas-padded", action="store_true",
                        help="apply a reviewed M4-B Douglas-only padded-water stage")
    args = parser.parse_args()
    report = read_json(args.report)
    if not report.get("acceptable_differences_only"):
        raise SystemExit("staged differences require review; canonical data not written")
    if not args.apply:
        print("Refresh report is eligible to apply. Re-run with --apply after reviewing its complete differences.")
        return
    if args.douglas_padded:
        apply_douglas_padded_refresh(args.report)
    else:
        apply_refresh(args.report)


if __name__ == "__main__":
    main()
