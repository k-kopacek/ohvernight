"""Run the single authorized M4-B Douglas padded NHD refresh into staging."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from shapely.geometry import box, shape

from build_display import display_water
from lib.common import ROOT, clip_geometry
from lib.evidence import make_evidence
from lib.water import (attach_legacy_ids, ensure_supported_ftype,
                       ensure_unique_feature_ids, normalize_feature,
                       support_bridges, support_gap_boxes, water_display_config)

SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))
import refresh_m4a_water as m4a  # noqa: E402

V2 = ROOT.parent
SERVICE = m4a.SERVICE
PRIOR_RAW_ROOT = ROOT / "data/raw/m4b-douglas-water"
RAW_ROOT = ROOT / "data/raw/m4b-douglas-water-objectid"
STAGING = ROOT / "data/processed/m4b-douglas-water-objectid"
PAD_DEG = 0.005
COUNT_ID_TIMEOUT = 180


def write_json(path: Path, value, *, indent=None):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False,
                               separators=None if indent else (",", ":"),
                               indent=indent, allow_nan=False) + "\n", encoding="utf-8")


def source_counts(features):
    by_ftype, by_fcode, pairs = Counter(), Counter(), Counter()
    for feature in features:
        props = feature["properties"]
        by_ftype[str(props["ftype"])] += 1
        by_fcode[str(props["fcode"])] += 1
        pairs[(str(props["ftype"]), str(props["fcode"]))] += 1
    return {"feature_count": len(features), "ftype": dict(sorted(by_ftype.items())),
            "fcode": dict(sorted(by_fcode.items())),
            "ftype_fcode": [{"ftype": key[0], "fcode": key[1], "count": count}
                            for key, count in sorted(pairs.items())]}


def padded_water_geometry(county, padding=PAD_DEG):
    """Return the fixed geographic-degree buffer used only by Douglas water."""
    if padding != PAD_DEG:
        raise ValueError(f"Douglas water padding is fixed at {PAD_DEG} degrees")
    return county.buffer(padding)


def preservation_hashes(v2_root=V2):
    """Hash all Aspen files and each non-water canonical layer for the proof."""
    aspen_files = {"map-data-v2.json": hashlib.sha256(
        (v2_root / "map-data-v2.json").read_bytes()).hexdigest()}
    aspen_root = v2_root / "regions/aspen"
    for path in sorted(item for item in aspen_root.rglob("*") if item.is_file()):
        aspen_files[path.relative_to(v2_root).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    aspen_bundle = json.loads((v2_root / "map-data-v2.json").read_text(encoding="utf-8"))
    douglas_bundle = json.loads((v2_root / "regions/douglas-co/research.json").read_text(encoding="utf-8"))

    def digest(value):
        encoded = json.dumps(value, ensure_ascii=False, sort_keys=True,
                             separators=(",", ":"), allow_nan=False).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()

    return {
        "aspen_files": aspen_files,
        "aspen_non_water_layers": {key: digest(value) for key, value in
                                    sorted(aspen_bundle["layers"].items()) if key != "hydrology"},
        "douglas_non_water_layers": {key: digest(value) for key, value in
                                     sorted(douglas_bundle["layers"].items())
                                     if key not in {"waterways", "waterbodies"}},
    }


def _feature_map(features):
    result = {}
    for feature in features:
        ident = feature["properties"].get("id")
        if ident in result:
            raise ValueError(f"duplicate water feature ID {ident}")
        result[ident] = feature
    return result


def compare_layer(layer_id, old_features, new_features, county, padded, tolerance=1e-10):
    old_by_id, new_by_id = _feature_map(old_features), _feature_map(new_features)
    old_ids, new_ids = set(old_by_id), set(new_by_id)
    removed, added = sorted(old_ids - new_ids), sorted(new_ids - old_ids)
    changed_geometry, name_changed, other_changes = [], [], []
    for ident in sorted(old_ids & new_ids):
        before, after = old_by_id[ident], new_by_id[ident]
        bp, ap = before["properties"], after["properties"]
        if bp.get("name") != ap.get("name"):
            name_changed.append(ident)
        if (bp.get("source_id"), bp.get("ftype"), bp.get("fcode")) != (
                ap.get("source_id"), ap.get("ftype"), ap.get("fcode")):
            other_changes.append(ident)
        bg, ag = shape(before["geometry"]), shape(after["geometry"])
        if not bg.equals_exact(ag, tolerance):
            grown_part = ag.difference(bg)
            lost_part = bg.difference(ag)
            padded_strip = padded.difference(county)
            grows_only_into_strip = (lost_part.is_empty or
                                     (lost_part.length <= tolerance and lost_part.area <= tolerance))
            growth_inside_strip = (not grown_part.is_empty and
                                   padded_strip.buffer(tolerance).covers(grown_part))
            if grows_only_into_strip and growth_inside_strip:
                changed_geometry.append(ident)
            else:
                other_changes.append(ident)
    added_outside_strip = []
    strip = padded.difference(county)
    for ident in added:
        geom = shape(new_by_id[ident]["geometry"])
        if not geom.intersects(strip) or not padded.buffer(tolerance).covers(geom):
            added_outside_strip.append(ident)
    return {
        "layer": layer_id,
        "before": source_counts(old_features),
        "after": source_counts(new_features),
        "added_ids": added,
        "removed_ids": removed,
        "geometry_grew_ids": changed_geometry,
        "name_changed_ids": name_changed,
        "other_existing_changes": sorted(set(other_changes)),
        "added_outside_padding_ids": added_outside_strip,
        "existing_id_map": {ident: ident for ident in sorted(old_ids & new_ids)},
        "explained": not (removed or name_changed or other_changes or added_outside_strip),
    }


def _query(client, layer, layer_id, extent, where, name):
    return m4a.controlled_layer_query(client, "douglas-co", layer, layer_id, extent, where,
                                      m4a.OUT_FIELDS[layer], RAW_ROOT, name,
                                      count_id_timeout=COUNT_ID_TIMEOUT)


def _is_named_flowline(raw_feature):
    """Match the old server predicate exactly: not SQL NULL and not empty text."""
    properties = {str(key).lower(): value
                  for key, value in (raw_feature.get("properties") or {}).items()}
    name = properties.get("gnis_name")
    return name is not None and name != ""


def _derive_flowlines(raw_features, padded, evidence):
    """Return only named Douglas flowlines and O1 bridges from saved layer-6 rows."""
    named, unnamed = [], []
    raw_named_count = 0
    for row in raw_features:
        is_named = _is_named_flowline(row)
        raw_named_count += int(is_named)
        geometry = row.get("geometry")
        if not geometry:
            continue
        clipped = clip_geometry(geometry, padded)
        if not clipped:
            continue
        feature = normalize_feature("flowline", row, clipped, evidence)
        (named if is_named else unnamed).append((row, feature))

    named_features = [feature for _, feature in named]
    gap_boxes = support_gap_boxes(named_features)
    candidates_by_id = {}
    # ArcGIS spatialRelIntersects with esriGeometryEnvelope selects a row when
    # its source geometry intersects this same box; testing the saved geometry
    # against box(*extent) locally is the identical predicate. The layer-6
    # object-ID discovery extent already bounded the saved candidate universe.
    for gnis_id, extent in gap_boxes:
        query_box = box(*extent)
        for row, feature in unnamed:
            if not query_box.intersects(shape(row["geometry"])):
                continue
            candidate = dict(feature)
            candidate["properties"] = dict(feature["properties"])
            candidate["properties"]["_support_query_gnis"] = gnis_id
            source_id = candidate["properties"]["source_id"]
            candidates_by_id[source_id] = candidate

    kept = support_bridges(named_features, list(candidates_by_id.values()))
    supporting = []
    support_names = {}
    for feature, gnis_id in kept:
        candidate = candidates_by_id[feature["properties"]["source_id"]]
        candidate["properties"].pop("_support_query_gnis", None)
        candidate["properties"]["support_for"] = gnis_id
        candidate["properties"]["support_reason"] = "bridges_named_parts"
        supporting.append(candidate)
        support_names[gnis_id] = next((item["properties"].get("name") for item in named_features
                                       if item["properties"].get("gnis_id") == gnis_id), None)
    return named_features + supporting, {
        "named_flowlines": raw_named_count,
        "named_flowlines_canonical": len(named_features),
        "supporting_features_kept": len(supporting),
        "unnamed_flowlines": len(raw_features) - raw_named_count,
        "unnamed_discarded": len(raw_features) - raw_named_count - len(supporting),
        "support_gap_count": len(gap_boxes),
        "supporting_features_by_water_class": dict(sorted(Counter(
            feature["properties"]["water_class"] for feature in supporting).items())),
        "supporting_gnis_names": support_names,
    }


def run():
    if not RAW_ROOT.exists():
        RAW_ROOT.mkdir(parents=True)
    STAGING.mkdir(parents=True, exist_ok=True)
    if (STAGING / "refresh-report.json").exists():
        raise RuntimeError("staging report already exists; refusing to overwrite a completed session")
    retrieved_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    client = m4a.new_session()
    metadata_path = RAW_ROOT / "service-metadata.json"
    if metadata_path.exists():
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    else:
        metadata = m4a.get_json(client, SERVICE, {"f": "json"}, 90)
        write_json(metadata_path, metadata)

    bundle_path = V2 / "regions/douglas-co/research.json"
    bundle = json.loads(bundle_path.read_text(encoding="utf-8"))
    coverage = shape(bundle["layers"]["coverage"]["features"][0]["geometry"])
    padded = padded_water_geometry(coverage)
    extent = padded.bounds
    old_layers = {"waterways": bundle["layers"]["waterways"]["features"],
                  "waterbodies": bundle["layers"]["waterbodies"]["features"]}
    before_hash = hashlib.sha256(bundle_path.read_bytes()).hexdigest()
    preserve_before = preservation_hashes()
    query_records, normalized = [], {}
    evidence6 = make_evidence(f"{SERVICE}/6", "USGS", "high", "arcgis_rest_query")
    evidence12 = make_evidence(f"{SERVICE}/12", "USGS", "high", "arcgis_rest_query")

    # Save every primary response page for both layers before deriving rows.
    raw_by_layer = {}
    for source_layer, layer_id, where in (
            ("flowline", 6, "1=1"),
            ("waterbody", 12, "1=1")):
        raw_fc, record = _query(client, source_layer, layer_id, extent, where, source_layer)
        query_records.append(record)
        raw_by_layer[source_layer] = raw_fc

    normalized["flowline"], flowline_counts = _derive_flowlines(
        raw_by_layer["flowline"]["features"], padded, evidence6)
    waterbodies = []
    for row in raw_by_layer["waterbody"]["features"]:
        geom = clip_geometry(row["geometry"], padded)
        if geom:
            waterbodies.append(normalize_feature("waterbody", row, geom, evidence12))
    normalized["waterbody"] = waterbodies

    old_by_source_layer = {"flowline": old_layers["waterways"], "waterbody": old_layers["waterbodies"]}
    diff = {}
    for source_layer in ("flowline", "waterbody"):
        features = normalized[source_layer]
        features, unmatched_old, unmatched_new = attach_legacy_ids(old_by_source_layer[source_layer], features)
        ensure_unique_feature_ids(features)
        unsupported_ftypes = []
        for feature in features:
            try:
                ensure_supported_ftype(feature["properties"].get("ftype"), water_display_config())
            except ValueError:
                unsupported_ftypes.append({"id": feature["properties"].get("id"),
                                           "ftype": feature["properties"].get("ftype")})
        layer_id = "waterways" if source_layer == "flowline" else "waterbodies"
        record = compare_layer(layer_id, old_layers[layer_id], features, coverage, padded)
        record["legacy_unmatched_old_geometry_ids"] = unmatched_old
        record["legacy_unmatched_new_geometry_ids"] = unmatched_new
        record["unsupported_ftypes"] = unsupported_ftypes
        record["explained"] = record["explained"] and not unsupported_ftypes
        record["display_count_current_rule"] = sum(display_water(feature) for feature in features)
        diff[layer_id] = record
        filename = "flowline" if source_layer == "flowline" else "waterbody"
        write_json(STAGING / f"douglas-co-{filename}.geojson",
                   {"type": "FeatureCollection", "features": features})

    existing_legacy = {legacy for features in old_layers.values() for feature in features
                       for legacy in feature["properties"].get("legacy_ids", [])}
    new_legacy = [legacy for features in normalized.values() for feature in features
                  for legacy in feature["properties"].get("legacy_ids", [])]
    legacy_counts = Counter(new_legacy)
    legacy_missing = sorted(existing_legacy - set(new_legacy))
    legacy_duplicated = sorted(ident for ident, count in legacy_counts.items() if count != 1)
    report = {
        "service": SERVICE, "service_currentVersion": metadata.get("currentVersion"),
        "service_metadata": {key: metadata.get(key) for key in ("currentVersion", "documentInfo", "serviceDescription")},
        "retrieved_at_utc": retrieved_at,
        "prior_failed_attempt_directory": PRIOR_RAW_ROOT.relative_to(ROOT).as_posix(),
        "retrieval_strategy": "padded-envelope object-ID discovery; local exact name filter; local O1 derivation",
        "scope": "Douglas water only; named flowlines plus locally derived O1 supporting features; all waterbodies",
        "support_box_predicate": (
            "Locally test each saved layer-6 geometry against the same 300 m gap-box envelope. "
            "This is equivalent to the replaced esriGeometryEnvelope / esriSpatialRelIntersects "
            "query; saved rows were first bounded by the padded-envelope object-ID query."
        ),
        "extent_padding_deg": PAD_DEG, "clip_bounds_wgs84": list(padded.bounds),
        "county_bounds_wgs84": list(coverage.bounds), "queries": query_records,
        "count_id_timeout_seconds": COUNT_ID_TIMEOUT,
        "local_filter_counts": {**flowline_counts,
                                 "waterbodies": len(raw_by_layer["waterbody"]["features"]),
                                 "waterbodies_canonical": len(waterbodies)},
        "support_gap_count": flowline_counts["support_gap_count"],
        "supporting_feature_count": flowline_counts["supporting_features_kept"],
        "supporting_features_by_water_class": flowline_counts["supporting_features_by_water_class"],
        "supporting_gnis_names": flowline_counts["supporting_gnis_names"],
        "before_sha256": before_hash, "preservation_hashes_before": preserve_before,
        "differences": diff,
        "legacy_ids_missing": legacy_missing, "legacy_ids_duplicate": legacy_duplicated,
        "acceptable_differences_only": (all(item["explained"] for item in diff.values()) and
                                         not legacy_missing and not legacy_duplicated),
    }
    write_json(STAGING / "refresh-report.json", report, indent=2)
    summary = {"raw": str(RAW_ROOT), "staging": str(STAGING),
               "retrieved_at_utc": retrieved_at,
               "acceptable_differences_only": report["acceptable_differences_only"],
               "counts": {layer: {"before": value["before"]["feature_count"],
                                   "after": value["after"]["feature_count"],
                                   "added": len(value["added_ids"]),
                                   "removed": len(value["removed_ids"]),
                                   "geometry_grew": len(value["geometry_grew_ids"]),
                                   "name_changed": len(value["name_changed_ids"])}
                          for layer, value in diff.items()},
               "supporting_feature_count": len(kept)}
    print(json.dumps(summary, indent=2))
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", action="store_true", help="start the one authorized live session")
    args = parser.parse_args()
    if not args.run:
        raise SystemExit("pass --run to begin the one authorized Douglas-only NHD session")
    RAW_ROOT.mkdir(parents=True, exist_ok=True)
    prior_attempts = sorted(RAW_ROOT.glob("attempt-*.json"))
    attempt_number = len(prior_attempts) + 1
    attempt_path = RAW_ROOT / f"attempt-{attempt_number:04d}.json"
    started_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    attempt = {
        "attempt": attempt_number,
        "started_at_utc": started_at,
        "retrieval_strategy": "padded-envelope object-ID discovery; local exact name filter; local O1 derivation",
        "prior_failed_attempt_directory": PRIOR_RAW_ROOT.relative_to(ROOT).as_posix(),
        "service": SERVICE,
        "layers": [6, 12],
        "extent_padding_deg": PAD_DEG,
        "primary_queries": [
            {"layer": 6, "where": "1=1",
             "outFields": f"{m4a.OUT_FIELDS['flowline']},OBJECTID", "extent_wgs84": None,
             "page_size": m4a.PAGE_SIZE, "count_id_timeout_seconds": COUNT_ID_TIMEOUT},
            {"layer": 12, "where": "1=1",
             "outFields": f"{m4a.OUT_FIELDS['waterbody']},OBJECTID", "extent_wgs84": None,
             "page_size": m4a.PAGE_SIZE, "count_id_timeout_seconds": COUNT_ID_TIMEOUT},
        ],
        "count_id_timeout_seconds": COUNT_ID_TIMEOUT,
        "outcome": "running",
    }
    bundle = json.loads((V2 / "regions/douglas-co/research.json").read_text(encoding="utf-8"))
    coverage = shape(bundle["layers"]["coverage"]["features"][0]["geometry"])
    extent = list(padded_water_geometry(coverage).bounds)
    for query in attempt["primary_queries"]:
        query["extent_wgs84"] = extent
    if attempt_path.exists():
        raise RuntimeError(f"refusing to overwrite attempt record {attempt_path}")
    write_json(attempt_path, attempt, indent=2)
    try:
        report = run()
    except Exception as error:
        attempt.update(outcome="failed", failed_at_utc=datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
                       error_type=type(error).__name__, error=str(error))
        write_json(attempt_path, attempt, indent=2)
        raise
    attempt.update(outcome=("staged_review_required" if not report["acceptable_differences_only"] else "staged"),
                   completed_at_utc=datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
                   report_path=str(STAGING / "refresh-report.json"))
    write_json(attempt_path, attempt, indent=2)
    if not report["acceptable_differences_only"]:
        raise SystemExit("Douglas padding differences need coordinator review; canonical files were not written")


if __name__ == "__main__":
    main()
