"""Run the single controlled M4-A NHD refresh without publishing canonical files."""
from __future__ import annotations

import hashlib
import json
import time
import argparse
from datetime import datetime, timezone
from collections import Counter
from pathlib import Path

from shapely.geometry import box, shape

from lib.arcgis_client import ArcGISQueryError, describe_layer, get_json, new_session
from lib.common import ROOT, bbox, clip_geometry, properties
from lib.evidence import make_evidence
from lib.water import (attach_legacy_ids, ensure_unique_feature_ids, ensure_supported_ftype,
                       legacy_geometry_matches, normalize_feature,
                       support_bridges, support_gap_boxes, water_display_config)
from build_display import display_water

SERVICE = "https://hydro.nationalmap.gov/arcgis/rest/services/nhd/MapServer"
V2 = ROOT.parent
PAGE_SIZE = 250
OUT_FIELDS = {
    "flowline": "permanent_identifier,gnis_id,gnis_name,ftype,fcode,reachcode,lengthkm,visibilityfilter,wbarea_permanent_identifier,fdate",
    "area": "PERMANENT_IDENTIFIER,GNIS_ID,GNIS_NAME,FTYPE,FCODE,AREASQKM,VISIBILITYFILTER,FDATE",
    "waterbody": "PERMANENT_IDENTIFIER,GNIS_ID,GNIS_NAME,FTYPE,FCODE,AREASQKM,ELEVATION,REACHCODE,VISIBILITYFILTER,FDATE",
}
LAYER_METADATA = {}


def _write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, separators=(",", ":"), allow_nan=False), encoding="utf-8")
    temporary.replace(path)


def _object_id(feature, oid_field):
    folded = {str(key).lower(): value for key, value in (feature.get("properties") or {}).items()}
    return folded.get(oid_field.lower(), feature.get("id"))


def _page_valid(page, batch, oid_field):
    if (not isinstance(page, dict) or page.get("type") != "FeatureCollection" or
            page.get("exceededTransferLimit") or not isinstance(page.get("features"), list)):
        return False
    actual = [_object_id(feature, oid_field) for feature in page["features"]]
    return len(actual) == len(batch) and set(actual) == set(batch) and all(feature.get("geometry") for feature in page["features"])


def controlled_layer_query(client, region, layer_name, layer_id, extent, where, out_fields,
                           raw_root: Path, query_name: str):
    """Fetch fixed-size object-ID pages and resume only the failed page on rerun."""
    if layer_id not in LAYER_METADATA:
        LAYER_METADATA[layer_id] = describe_layer(SERVICE, layer_id, timeout=90, session=client,
                                                  required_fields=["permanent_identifier", "ftype", "fcode"])
    info = LAYER_METADATA[layer_id]
    oid_field = next((field["name"] for field in info["fields"]
                      if field["type"] == "esriFieldTypeOID"), None)
    if not oid_field:
        raise ArcGISQueryError(f"layer {layer_id} has no object ID")
    base = f"{SERVICE.rstrip('/')}/{layer_id}/query"
    spatial = {"where": where, "geometry": ",".join(map(str, extent)),
               "geometryType": "esriGeometryEnvelope", "inSR": 4326,
               "spatialRel": "esriSpatialRelIntersects"}
    plan_path = raw_root / f"{region}-{query_name}-plan.json"
    expected_plan = {"region": region, "query_name": query_name, "layer_id": layer_id,
                     "where": where, "extent": list(extent), "out_fields": out_fields,
                     "page_size": PAGE_SIZE, "spatial": spatial}
    if plan_path.exists():
        plan = json.loads(plan_path.read_text(encoding="utf-8"))
        if any(plan.get(key) != value for key, value in expected_plan.items()):
            raise RuntimeError(f"refusing to change saved NHD query plan: {plan_path}")
    else:
        counts = get_json(client, base, {**spatial, "f": "json", "returnCountOnly": "true"}, 90)
        count = counts.get("count")
        ids_payload = get_json(client, base, {**spatial, "f": "json", "returnIdsOnly": "true"}, 90)
        object_ids = sorted(ids_payload.get("objectIds") or [])
        if ids_payload.get("exceededTransferLimit") or not isinstance(count, int) or count != len(object_ids) or len(object_ids) != len(set(object_ids)):
            raise ArcGISQueryError(f"layer {layer_id} count and complete ID set disagree")
        plan = {**expected_plan, "count": count, "object_ids": object_ids,
                "object_id_field": oid_field, "completed_pages": []}
        _write_json(plan_path, plan)
    object_ids = plan["object_ids"]
    pages_dir = raw_root / f"{region}-{query_name}-pages"
    pages_dir.mkdir(parents=True, exist_ok=True)
    features = []
    batches = [object_ids[start:start + PAGE_SIZE] for start in range(0, len(object_ids), PAGE_SIZE)]
    for page_number, batch in enumerate(batches, start=1):
        page_path = pages_dir / f"page-{page_number:04d}.json"
        if page_path.exists():
            page = json.loads(page_path.read_text(encoding="utf-8"))
            if not _page_valid(page, batch, oid_field):
                raise ArcGISQueryError(f"saved NHD page is incomplete: {page_path}")
        else:
            params = {"f": "geojson", "objectIds": ",".join(map(str, batch)),
                      "outFields": f"{out_fields},{oid_field}", "outSR": 4326,
                      "returnGeometry": "true", "returnZ": "false", "returnM": "false"}
            page = None
            last_error = None
            for attempt in range(3):
                try:
                    candidate = get_json(client, base, params, 120)
                    if not _page_valid(candidate, batch, oid_field):
                        raise ArcGISQueryError(f"page {page_number} did not return its complete ID set")
                    page = candidate
                    break
                except Exception as error:
                    last_error = error
                    if attempt < 2:
                        time.sleep(2 ** attempt)
            if page is None:
                raise ArcGISQueryError(f"page {page_number} failed after same-parameter retries: {last_error}")
            _write_json(page_path, page)
            plan.setdefault("completed_pages", []).append(page_number)
            _write_json(plan_path, plan)
        features.extend(page["features"])
    if not plan.get("final_ids_verified"):
        final_ids = get_json(client, base, {**spatial, "f": "json", "returnIdsOnly": "true"}, 90)
        if sorted(final_ids.get("objectIds") or []) != object_ids:
            raise ArcGISQueryError(f"layer {layer_id} object IDs changed during the controlled refresh")
        plan["final_ids_verified"] = True
        _write_json(plan_path, plan)
    query_record = {"region": region, "layer_id": layer_id, "where": where,
                    "outFields": f"{out_fields},{oid_field}", "extent_wgs84": list(extent),
                    "page_size": PAGE_SIZE, "pages": len(batches), "count": len(features),
                    "max_record_count": info.get("maxRecordCount"),
                    "elevation_field_metadata": next((field for field in info["fields"]
                                                       if field["name"].lower() == "elevation"), None)
                    if layer_id == 12 else None}
    return {"type": "FeatureCollection", "features": features}, query_record


def _old_layers(region):
    if region == "aspen":
        document = json.loads((V2 / "map-data-v2.json").read_text(encoding="utf-8"))
        old = document["layers"]["hydrology"]["features"]
        return {name: [feature for feature in old if (feature.get("properties") or {}).get("kind") == name]
                for name in ("flowline", "area", "waterbody")}
    document = json.loads((V2 / "regions/douglas-co/research.json").read_text(encoding="utf-8"))
    return {"flowline": document["layers"]["waterways"]["features"],
            "waterbody": document["layers"]["waterbodies"]["features"]}


def _canonical_layer_name(region, source_layer):
    if region == "aspen":
        return "hydrology"
    return "waterways" if source_layer == "flowline" else "waterbodies"


def _old_object_id(feature):
    value = (feature.get("properties") or {}).get("id", "").rsplit("-", 1)[-1]
    return int(value) if value.isdigit() else None


def _counts(features):
    result = {"ftype": Counter(), "fcode": Counter(), "water_class": Counter(), "hydro_category": Counter(),
              "ftype_fcode_pairs": {}, "named": 0, "unnamed": 0}
    for feature in features:
        props = feature["properties"]
        result["ftype"][str(props["ftype"])] += 1
        result["fcode"][str(props["fcode"])] += 1
        result["water_class"][props["water_class"]] += 1
        result["hydro_category"][props["hydro_category"]] += 1
        pair = (props["ftype"], props["fcode"])
        if pair not in result["ftype_fcode_pairs"]:
            result["ftype_fcode_pairs"][pair] = {
                "ftype": props["ftype"], "fcode": props["fcode"], "count": 0,
                "water_class": props["water_class"], "hydro_category": props["hydro_category"],
            }
        result["ftype_fcode_pairs"][pair]["count"] += 1
        result["named" if isinstance(props.get("name"), str) and props["name"].strip() else "unnamed"] += 1
    return {key: (dict(sorted(value.items())) if isinstance(value, Counter) else
                  [value[pair] for pair in sorted(value)] if key == "ftype_fcode_pairs" else value)
            for key, value in result.items()}


def difference_report(region, source_layer, old_features, new_features, raw_by_source_id):
    layer_name = _canonical_layer_name(region, source_layer)
    legacy_by_new, unmatched_old, unmatched_new = legacy_geometry_matches(old_features, new_features)
    old_to_new = {old_id: new_id for new_id, old_ids in legacy_by_new.items() for old_id in old_ids}
    new_by_id = {feature["properties"]["id"]: feature for feature in new_features}
    old_by_id = {feature["properties"]["id"]: feature for feature in old_features}
    name_changes = []
    for old_id, new_id in sorted(old_to_new.items()):
        before = old_by_id[old_id]["properties"].get("name")
        after = new_by_id[new_id]["properties"].get("name")
        if before != after:
            name_changes.append({"old_id": old_id, "new_id": new_id, "before": before, "after": after})
    geometry_changes = []
    for old_id in unmatched_old:
        old_object_id = _old_object_id(old_by_id[old_id])
        candidate = next((feature for feature in new_features
                          if raw_by_source_id.get(feature["properties"]["source_id"], {}).get("objectid") == old_object_id), None)
        if candidate is not None:
            geometry_changes.append({"old_id": old_id, "new_id": candidate["properties"]["id"],
                                     "objectid_diagnostic_only": old_object_id})
            before = old_by_id[old_id]["properties"].get("name")
            after = candidate["properties"].get("name")
            if before != after:
                name_changes.append({"old_id": old_id, "new_id": candidate["properties"]["id"],
                                     "before": before, "after": after,
                                     "objectid_diagnostic_only": old_object_id})
    additions = [new_by_id[ident] for ident in unmatched_new]
    removals = [old_by_id[ident] for ident in unmatched_old if ident not in {
        change["old_id"] for change in geometry_changes}]
    expected_additions = []
    unexplained_additions = []
    for feature in additions:
        props = feature["properties"]
        if region == "douglas-co" and source_layer == "waterbody" and not (props.get("name") or "").strip():
            expected_additions.append(props["id"])
        elif region == "douglas-co" and source_layer == "flowline" and props.get("support_reason") == "bridges_named_parts":
            expected_additions.append(props["id"])
        else:
            unexplained_additions.append(props["id"])
    before_kinds = Counter((feature.get("properties") or {}).get("kind", layer_name) for feature in old_features)
    before_named = sum(bool(((f.get("properties") or {}).get("name") or "").strip()) for f in old_features)
    report = {
        "region": region, "layer": layer_name, "source_layer": source_layer,
        "before": {"feature_count": len(old_features), "by_retained_kind_or_layer": dict(before_kinds),
                   "named": before_named, "unnamed": len(old_features) - before_named,
                   "ftype": "not retained in the baseline", "fcode": "not retained in the baseline"},
        "after": _counts(new_features),
        "exact_geometry_matches": len(old_to_new), "old_id_to_new_id": dict(sorted(old_to_new.items())),
        "old_ids_with_no_exact_geometry_match": sorted(unmatched_old),
        "new_ids_with_no_exact_geometry_match": sorted(unmatched_new),
        "geometry_changes_objectid_diagnostic_only": geometry_changes,
        "name_changes": name_changes,
        "removed_features": [feature["properties"]["id"] for feature in removals],
        "added_features": [feature["properties"]["id"] for feature in additions],
        "expected_scope_additions": sorted(expected_additions),
        "unexplained_additions": sorted(unexplained_additions),
        "matched_before_types_assigned_from_refresh": {
            "ftype": dict(sorted(Counter(str(new_by_id[new_id]["properties"]["ftype"])
                                           for new_id in old_to_new.values()).items())),
            "fcode": dict(sorted(Counter(str(new_by_id[new_id]["properties"]["fcode"])
                                           for new_id in old_to_new.values()).items())),
        },
    }
    report["stop_required"] = bool(geometry_changes or name_changes or removals or unexplained_additions)
    return report


def _staged_raw_properties(raw_root: Path) -> dict[str, dict]:
    """Reconstruct source attributes from saved pages without contacting NHD."""
    result = {}
    for page_path in sorted(raw_root.glob("*-pages/page-*.json")):
        page = json.loads(page_path.read_text(encoding="utf-8"))
        for feature in page.get("features", []):
            props = properties(feature)
            source_id = props.get("permanent_identifier")
            if source_id is not None:
                result[str(source_id)] = props
    return result


def review_staged(staging: Path, raw_root: Path) -> dict:
    """Recompute the difference report from saved stage and raw response files."""
    existing = json.loads((staging / "refresh-report.json").read_text(encoding="utf-8"))
    raw_by_source_id = _staged_raw_properties(raw_root)
    differences = {}
    layer_files = {
        ("aspen", "flowline"): "aspen-flowline.geojson",
        ("aspen", "area"): "aspen-area.geojson",
        ("aspen", "waterbody"): "aspen-waterbody.geojson",
        ("douglas-co", "flowline"): "douglas-co-flowline.geojson",
        ("douglas-co", "waterbody"): "douglas-co-waterbody.geojson",
    }
    config = water_display_config()
    for (region, source_layer), filename in layer_files.items():
        staged = json.loads((staging / filename).read_text(encoding="utf-8"))["features"]
        old = _old_layers(region)[source_layer]
        report = difference_report(region, source_layer, old, staged, raw_by_source_id)
        if region == "douglas-co" and source_layer == "flowline":
            gap_queries = [query for query in existing["queries"] if query.get("support_for_query")]
            gap_ids = sorted({query["support_for_query"] for query in gap_queries})
            named_by_gnis = {}
            for feature in staged:
                props = feature["properties"]
                if props.get("support_reason") != "bridges_named_parts":
                    name = props.get("name")
                    if props.get("gnis_id") and name:
                        named_by_gnis.setdefault(props["gnis_id"], name)
            support_counts = Counter(feature["properties"].get("water_class") for feature in staged
                                     if feature["properties"].get("support_reason") == "bridges_named_parts")
            report["support_report"] = {
                "gap_boxes_examined": len(gap_queries),
                "gnis_ids_examined": [{"gnis_id": ident, "river_name": named_by_gnis.get(ident)}
                                       for ident in gap_ids],
                "named_segment_count": sum(not feature["properties"].get("support_reason")
                                            for feature in staged),
                "supporting_segment_count": sum(support_counts.values()),
                "supporting_by_water_class": dict(sorted(support_counts.items())),
            }
        unsupported_ftypes = []
        for feature in staged:
            ftype = feature["properties"].get("ftype")
            try:
                ensure_supported_ftype(ftype, config)
            except ValueError:
                unsupported_ftypes.append({"id": feature["properties"].get("id"), "ftype": ftype})
        report["unsupported_ftypes"] = unsupported_ftypes
        report["stop_required"] = bool(report["stop_required"] or unsupported_ftypes)
        differences[f"{region}/{source_layer}"] = report
    existing["differences"] = differences
    existing["acceptable_differences_only"] = not any(
        report["stop_required"] for report in differences.values())
    _write_json(staging / "refresh-report.json", existing)
    return existing


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--review-staged", action="store_true",
                        help="recompute differences from saved pages without network access")
    args = parser.parse_args()
    raw_root = ROOT / "data/raw/m4a-nhd-refresh"
    staging = ROOT / "data/processed/m4a-nhd-refresh"
    if args.review_staged:
        result = review_staged(staging, raw_root)
        print(json.dumps({"staging": str(staging),
                          "acceptable_differences_only": result["acceptable_differences_only"],
                          "differences": {key: {"before": value["before"]["feature_count"],
                                                "after": value["after"]["named"] + value["after"]["unnamed"],
                                                "stop_required": value["stop_required"]}
                                          for key, value in result["differences"].items()}}, indent=2))
        if not result["acceptable_differences_only"]:
            raise SystemExit("M4-A differences need coordinator review; canonical files were not written")
        return
    raw_root.mkdir(parents=True, exist_ok=True)
    client = new_session()
    service_metadata_path = raw_root / "service-metadata.json"
    if service_metadata_path.exists():
        service_metadata = json.loads(service_metadata_path.read_text(encoding="utf-8"))
    else:
        service_metadata = get_json(client, SERVICE, {"f": "json"}, 90)
        _write_json(service_metadata_path, service_metadata)
    query_records, snapshots, difference = [], {}, {}
    config = water_display_config()
    regions = {
        "aspen": {"extent": bbox(0.005), "clip": box(*bbox(0.005)),
                  "layers": [("flowline", 6, "1=1"), ("area", 9, "1=1"), ("waterbody", 12, "1=1")]},
        "douglas-co": {},
    }
    douglas = json.loads((V2 / "regions/douglas-co/research.json").read_text(encoding="utf-8"))
    county = shape(douglas["layers"]["coverage"]["features"][0]["geometry"])
    regions["douglas-co"] = {"extent": county.bounds, "clip": county,
                              "layers": [("flowline", 6, "gnis_name IS NOT NULL AND gnis_name <> ''"),
                                         ("waterbody", 12, "1=1")]}
    all_features = {}
    for region, settings in regions.items():
        old = _old_layers(region)
        normalized_by_layer = {}
        raw_by_source_id = {}
        for source_layer, layer_id, where in settings["layers"]:
            raw_fc, query_record = controlled_layer_query(
                client, region, source_layer, layer_id, settings["extent"], where,
                OUT_FIELDS[source_layer], raw_root, source_layer)
            query_records.append(query_record)
            evidence = make_evidence(f"{SERVICE}/{layer_id}", "USGS", "high", "arcgis_rest_query")
            normalized = []
            for row in raw_fc["features"]:
                geometry = clip_geometry(row["geometry"], settings["clip"])
                if geometry:
                    feature = normalize_feature(source_layer, row, geometry, evidence,
                                                aspen=(region == "aspen"))
                    normalized.append(feature)
                    raw_by_source_id[feature["properties"]["source_id"]] = properties(row)
            normalized_by_layer[source_layer] = normalized
            _write_json(staging / f"{region}-{source_layer}-unmatched-stage.json",
                        {"type": "FeatureCollection", "features": normalized})
        supporting = []
        support_reports = []
        if region == "douglas-co":
            named = normalized_by_layer["flowline"]
            gap_boxes = support_gap_boxes(named)
            query_records.append({"support_gap_count": len(gap_boxes), "support_box_width_m": 300,
                                  "support_max_gap_m": 250, "endpoint_rounding_decimals": 6})
            candidates_by_id = {}
            for gap_index, (gnis_id, gap_extent) in enumerate(gap_boxes, start=1):
                raw_fc, query_record = controlled_layer_query(
                    client, region, "flowline", 6, gap_extent,
                    "gnis_name IS NULL OR gnis_name = ''", OUT_FIELDS["flowline"], raw_root,
                    f"support-{gap_index:04d}")
                query_record["support_for_query"] = gnis_id
                query_records.append(query_record)
                evidence = make_evidence(f"{SERVICE}/6", "USGS", "high", "arcgis_rest_query")
                for row in raw_fc["features"]:
                    geometry = clip_geometry(row["geometry"], county)
                    if not geometry:
                        continue
                    candidate = normalize_feature("flowline", row, geometry, evidence)
                    source_id = candidate["properties"]["source_id"]
                    candidate["properties"]["_support_query_gnis"] = gnis_id
                    candidates_by_id[source_id] = candidate
                    raw_by_source_id[source_id] = properties(row)
            candidates = list(candidates_by_id.values())
            kept = support_bridges(named, candidates)
            names = {}
            for feature, gnis_id in kept:
                source_id = feature["properties"]["source_id"]
                original = candidates_by_id[source_id]
                original["properties"].pop("_support_query_gnis", None)
                original["properties"]["support_for"] = gnis_id
                original["properties"]["support_reason"] = "bridges_named_parts"
                supporting.append(original)
                name = next((item["properties"].get("name") for item in named
                             if item["properties"].get("gnis_id") == gnis_id), None)
                names.setdefault(gnis_id, name)
            support_counts = Counter(feature["properties"]["water_class"] for feature in supporting)
            support_reports = [{"support_reason": "bridges_named_parts", "water_class": water_class,
                                "feature_count": count} for water_class, count in sorted(support_counts.items())]
            normalized_by_layer["flowline"].extend(supporting)
            support_reports.append({"named_segment_count": len(named), "supporting_segment_count": len(supporting),
                                    "rivers_supported": names})
        for source_layer, features in normalized_by_layer.items():
            old_layer = old.get(source_layer, [])
            features, unmatched_old, unmatched_new = attach_legacy_ids(old_layer, features)
            if source_layer == "flowline" and supporting:
                for feature in supporting:
                    feature["properties"]["legacy_ids"] = []
            ensure_unique_feature_ids(features)
            report = difference_report(region, source_layer, old_layer, features, raw_by_source_id)
            displayed = [feature for feature in features if display_water(feature)]
            unsupported_ftypes = []
            for feature in features:
                try:
                    ensure_supported_ftype(feature["properties"].get("ftype"), config)
                except ValueError:
                    unsupported_ftypes.append({"id": feature["properties"].get("id"),
                                               "ftype": feature["properties"].get("ftype")})
            report["unsupported_ftypes"] = unsupported_ftypes
            if unsupported_ftypes:
                report["stop_required"] = True
            report["support_report"] = support_reports if region == "douglas-co" and source_layer == "flowline" else []
            difference[f"{region}/{source_layer}"] = report
            snapshots[f"{region}/{source_layer}"] = {"query_feature_count": len(features),
                                                      "canonical_feature_count": len(features),
                                                      "sha256_before": hashlib.sha256(
                                                          (V2 / ("map-data-v2.json" if region == "aspen" else "regions/douglas-co/research.json")).read_bytes()).hexdigest(),
                                                      "legacy_unmatched_old": unmatched_old,
                                                      "legacy_unmatched_new": unmatched_new}
            _write_json(staging / f"{region}-{source_layer}.geojson",
                        {"type": "FeatureCollection", "features": features})
        if region == "aspen":
            all_features[region] = [feature for key in ("flowline", "area", "waterbody")
                                    for feature in normalized_by_layer[key]]
        else:
            all_features[region] = normalized_by_layer
    if all_features:
        ensure_unique_feature_ids(all_features["aspen"])
        ensure_unique_feature_ids(all_features["douglas-co"]["flowline"] + all_features["douglas-co"]["waterbody"])
    retrieved_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    result = {"service": SERVICE, "service_currentVersion": service_metadata.get("currentVersion"),
              "service_metadata": {key: value for key, value in service_metadata.items()
                                   if key in {"serviceDescription", "documentInfo", "currentVersion"}},
              "retrieved_at_utc": retrieved_at, "queries": query_records,
              "snapshots": snapshots, "differences": difference,
              "acceptable_differences_only": not any(item["stop_required"] for item in difference.values())}
    _write_json(staging / "refresh-report.json", result)
    print(json.dumps({"staging": str(staging), "retrieved_at_utc": retrieved_at,
                      "report": str(staging / "refresh-report.json"),
                      "stop_required": not result["acceptable_differences_only"]}, indent=2))
    if not result["acceptable_differences_only"]:
        raise SystemExit("M4-A differences need coordinator review; canonical files were not written")


if __name__ == "__main__":
    main()
