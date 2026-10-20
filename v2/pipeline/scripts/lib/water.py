"""M4-A NHD source-field normalization and legacy identity helpers."""
from __future__ import annotations

import json
import math
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


WATER_DISPLAY_PATH = Path(__file__).resolve().parents[2] / "config" / "water_display.json"


def water_display_config() -> dict[str, Any]:
    return json.loads(WATER_DISPLAY_PATH.read_text(encoding="utf-8"))


def _int_keyed(mapping: dict[str, Any]) -> dict[int, Any]:
    return {int(key): value for key, value in mapping.items()}

SOURCE_FIELDS = {
    "flowline": {
        "name": "gnis_name", "gnis_id": "gnis_id", "source_id": "permanent_identifier",
        "ftype": "ftype", "fcode": "fcode", "reach_code": "reachcode",
        "length_km": "lengthkm", "area_sqkm": None, "elevation_m": None,
        "visibility_filter": "visibilityfilter", "waterbody_source_id": "wbarea_permanent_identifier",
        "source_date": "fdate",
    },
    "area": {
        "name": "gnis_name", "gnis_id": "gnis_id", "source_id": "permanent_identifier",
        "ftype": "ftype", "fcode": "fcode", "reach_code": None,
        "length_km": None, "area_sqkm": "areasqkm", "elevation_m": None,
        "visibility_filter": "visibilityfilter", "waterbody_source_id": None,
        "source_date": "fdate",
    },
    "waterbody": {
        "name": "gnis_name", "gnis_id": "gnis_id", "source_id": "permanent_identifier",
        "ftype": "ftype", "fcode": "fcode", "reach_code": "reachcode",
        "length_km": None, "area_sqkm": "areasqkm", "elevation_m": "elevation",
        "visibility_filter": "visibilityfilter", "waterbody_source_id": None,
        "source_date": "fdate",
    },
}


def _source_property(properties: dict[str, Any], name: str | None) -> Any:
    if name is None:
        return None
    folded = {str(key).lower(): value for key, value in properties.items()}
    return folded.get(name.lower())


def sanitize_source_id(source_id: Any) -> str:
    if not isinstance(source_id, str) or not source_id.strip():
        raise ValueError("water feature has no permanent source_id")
    sanitized = re.sub(r"[^A-Za-z0-9-]", "", source_id)
    if not sanitized:
        raise ValueError("water source_id is empty after sanitizing")
    return sanitized


def feature_id(source_id: Any) -> str:
    return "nhd-" + sanitize_source_id(source_id)


def ensure_unique_feature_ids(features: list[dict[str, Any]]) -> None:
    seen = set()
    for feature in features:
        ident = feature.get("properties", {}).get("id")
        if not isinstance(ident, str) or not ident:
            raise ValueError("water feature has no id")
        if ident in seen:
            raise ValueError(f"duplicate water feature ID {ident}")
        seen.add(ident)


def classify(ftype: Any, fcode: Any, config: dict[str, Any] | None = None) -> tuple[str, str]:
    if isinstance(ftype, bool) or not isinstance(ftype, int):
        raise ValueError("water ftype must be an integer")
    if isinstance(fcode, bool) or not isinstance(fcode, int):
        raise ValueError("water fcode must be an integer")
    config = config or water_display_config()
    return (_int_keyed(config["water_class_by_ftype"]).get(ftype, "other"),
            _int_keyed(config["hydro_category_by_fcode"]).get(fcode, "unknown"))


def ensure_supported_ftype(ftype: Any, config: dict[str, Any] | None = None) -> str:
    """Reject a source feature type that falls through to the ``other`` class."""
    if isinstance(ftype, bool) or not isinstance(ftype, int):
        raise ValueError("water ftype must be an integer")
    config = config or water_display_config()
    water_class = _int_keyed(config["water_class_by_ftype"]).get(ftype)
    if water_class is None:
        raise ValueError(f"unsupported water ftype {ftype}")
    return water_class


def normalize_source_fields(layer: str, source_properties: dict[str, Any]) -> dict[str, Any]:
    if layer not in SOURCE_FIELDS:
        raise ValueError(f"unsupported NHD layer {layer}")
    fields = {key: _source_property(source_properties, source_name)
              for key, source_name in SOURCE_FIELDS[layer].items() if source_name is not None}
    fields["source_id"] = fields["source_id"] if isinstance(fields["source_id"], str) else (
        str(fields["source_id"]) if fields["source_id"] is not None else None)
    fields["gnis_id"] = fields["gnis_id"] if fields["gnis_id"] is None else str(fields["gnis_id"])
    if fields["source_id"] is None or not fields["source_id"].strip():
        raise ValueError("water feature has no permanent source_id")
    fields["ftype"] = _as_integer(fields["ftype"], "ftype")
    fields["fcode"] = _as_integer(fields["fcode"], "fcode")
    if fields["visibility_filter"] is not None:
        fields["visibility_filter"] = _as_integer(fields["visibility_filter"], "visibility_filter")
    for field in ("length_km", "area_sqkm", "elevation_m"):
        if field in fields and fields[field] is not None:
            value = fields[field]
            if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
                raise ValueError(f"water {field} must be a finite number or null")
    for field in ("name", "gnis_id", "reach_code", "waterbody_source_id"):
        if field in fields and fields[field] is not None and not isinstance(fields[field], str):
            fields[field] = str(fields[field])
    if "source_date" in fields and isinstance(fields["source_date"], (int, float)) and not isinstance(fields["source_date"], bool):
        if not math.isfinite(fields["source_date"]):
            raise ValueError("water source_date must be a valid timestamp or null")
        fields["source_date"] = datetime.fromtimestamp(fields["source_date"] / 1000, timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")
    return fields


def _as_integer(value: Any, field: str) -> int:
    if isinstance(value, bool):
        raise ValueError(f"water {field} must be an integer")
    if isinstance(value, int):
        return value
    if isinstance(value, str) and re.fullmatch(r"-?\d+", value):
        return int(value)
    raise ValueError(f"water {field} must be an integer")


def enrich_properties(layer: str, source_properties: dict[str, Any], evidence: dict[str, Any],
                      legacy_ids: list[str], *, aspen: bool = False,
                      support_for: str | None = None,
                      support_reason: str | None = None) -> dict[str, Any]:
    source = normalize_source_fields(layer, source_properties)
    water_class, hydro_category = classify(source["ftype"], source["fcode"])
    properties = {
        "id": feature_id(source["source_id"]),
        **source,
        "evidence": evidence,
        "source_namespace": "usgs_nhd",
        "source_layer": layer,
        "water_class": water_class,
        "hydro_category": hydro_category,
        "legacy_ids": list(legacy_ids),
    }
    if aspen:
        properties["kind"] = {"flowline": "flowline", "waterbody": "waterbody", "area": "area"}[layer]
    if support_for is not None:
        properties["support_for"] = str(support_for)
        properties["support_reason"] = support_reason or "bridges_named_parts"
    return properties


def normalize_feature(layer: str, raw_feature: dict[str, Any], geometry: dict[str, Any],
                      evidence: dict[str, Any], legacy_ids: list[str] | None = None,
                      *, aspen: bool = False, support_for: str | None = None,
                      support_reason: str | None = None) -> dict[str, Any]:
    return {"type": "Feature", "geometry": geometry,
            "properties": enrich_properties(layer, raw_feature.get("properties", {}), evidence,
                                             legacy_ids or [], aspen=aspen,
                                             support_for=support_for, support_reason=support_reason)}


def attach_legacy_ids(old_features: list[dict[str, Any]], new_features: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[str], list[str]]:
    legacy_by_new, unmatched_old, unmatched_new = legacy_geometry_matches(old_features, new_features)
    old_by_id = {feature["properties"]["id"]: feature for feature in old_features}
    assigned_legacy: dict[str, str] = {}
    for feature in new_features:
        feature_id = feature["properties"]["id"]
        matched_ids = set(legacy_by_new.get(feature_id, []))
        if feature_id in old_by_id:
            matched_ids.add(feature_id)
        aliases = []
        seen = set()
        for old in old_features:
            old_id = old["properties"]["id"]
            if old_id not in matched_ids:
                continue
            prior = old["properties"].get("legacy_ids", [])
            if not isinstance(prior, list):
                raise ValueError(f"legacy_ids on old water feature {old_id} must be a list")
            for legacy_id in [*prior, old_id]:
                if legacy_id == feature_id or legacy_id in seen:
                    continue
                if legacy_id in assigned_legacy:
                    raise ValueError(f"legacy water ID {legacy_id} would be assigned to multiple features")
                seen.add(legacy_id)
                aliases.append(legacy_id)
        feature["properties"]["legacy_ids"] = aliases
        assigned_legacy.update({legacy_id: feature_id for legacy_id in aliases})
    ensure_unique_feature_ids(new_features)
    return new_features, unmatched_old, unmatched_new


def geometry_key(geometry: dict[str, Any]) -> str:
    """Exact canonical JSON equality; no spatial tolerance or row-number fallback."""
    return json.dumps(geometry, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def legacy_geometry_matches(old_features: list[dict[str, Any]], new_features: list[dict[str, Any]]) -> tuple[dict[str, list[str]], list[str], list[str]]:
    """Return new-ID to prior IDs, plus unmatched old and new IDs.

    Geometry is compared exactly within one caller-selected source layer. An
    ambiguous duplicate geometry on either side is deliberately left unmatched.
    """
    old_by_geometry: dict[str, list[dict[str, Any]]] = defaultdict(list)
    new_by_geometry: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for feature in old_features:
        old_by_geometry[geometry_key(feature["geometry"])].append(feature)
    for feature in new_features:
        new_by_geometry[geometry_key(feature["geometry"])].append(feature)
    legacy_by_new: dict[str, list[str]] = defaultdict(list)
    unmatched_old, unmatched_new = [], []
    old_ids = {f["properties"]["id"] for f in old_features}
    new_ids = {f["properties"]["id"] for f in new_features}
    matched_old, matched_new = set(), set()
    for key in old_by_geometry.keys() & new_by_geometry.keys():
        olds, news = old_by_geometry[key], new_by_geometry[key]
        if len(olds) != 1 or len(news) != 1:
            continue
        old_id, new_id = olds[0]["properties"]["id"], news[0]["properties"]["id"]
        legacy_by_new[new_id].append(old_id)
        matched_old.add(old_id)
        matched_new.add(new_id)
    unmatched_old.extend(sorted(old_ids - matched_old))
    unmatched_new.extend(sorted(new_ids - matched_new))
    return dict(legacy_by_new), unmatched_old, unmatched_new


def splice_layer(bundle: dict[str, Any], layer_id: str, replacement: dict[str, Any]) -> dict[str, Any]:
    """Copy a bundle while replacing exactly one layer, leaving others equal."""
    if layer_id not in bundle.get("layers", {}):
        raise ValueError(f"bundle has no layer {layer_id}")
    result = dict(bundle)
    result["layers"] = dict(bundle["layers"])
    result["layers"][layer_id] = replacement
    return result


def support_bridges(named_features: list[dict[str, Any]], candidates: list[dict[str, Any]],
                    *, max_gap_m: float = 250.0, tolerance_m: float = 2.0) -> list[tuple[dict[str, Any], str]]:
    """Keep candidate line components that connect two named parts of one GNIS ID.

    The caller scopes candidates to the prescribed 300 m query boxes. End point
    components use six-decimal WGS84 coordinates and gap distances use UTM 13N.
    """
    from pyproj import Transformer

    metric = Transformer.from_crs("EPSG:4326", "EPSG:26913", always_xy=True)
    to_metric = metric.transform

    def parts(feature):
        geometry = feature.get("geometry") or {}
        if geometry.get("type") == "LineString":
            return [geometry.get("coordinates", [])]
        if geometry.get("type") == "MultiLineString":
            return geometry.get("coordinates", [])
        return []

    def line_ends(feature):
        return [(tuple(round(float(value), 6) for value in line[0][:2]),
                 tuple(round(float(value), 6) for value in line[-1][:2]))
                for line in parts(feature) if len(line) >= 2]

    def metric_distance(left, right):
        lx, ly = to_metric(*left)
        rx, ry = to_metric(*right)
        return ((lx-rx) ** 2 + (ly-ry) ** 2) ** 0.5

    by_gnis: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for feature in named_features:
        props = feature.get("properties", {})
        gnis_id = props.get("gnis_id")
        if isinstance(gnis_id, str) and gnis_id:
            by_gnis[gnis_id].append(feature)
    kept: dict[str, tuple[dict[str, Any], str]] = {}
    for gnis_id, named in by_gnis.items():
        named_lines = [(feature, ends) for feature in named for ends in line_ends(feature)]
        if len(named_lines) < 2:
            continue
        # Build named endpoint components using the specified six-decimal keys.
        named_parents = list(range(len(named_lines)))
        def named_root(index):
            while named_parents[index] != index:
                named_parents[index] = named_parents[named_parents[index]]
                index = named_parents[index]
            return index
        for i, (_, left) in enumerate(named_lines):
            for j in range(i + 1, len(named_lines)):
                if set(left) & set(named_lines[j][1]):
                    named_parents[named_root(j)] = named_root(i)
        named_components: dict[int, list[tuple[float, float]]] = defaultdict(list)
        named_point_counts: dict[int, Counter] = defaultdict(Counter)
        for index, (_, ends) in enumerate(named_lines):
            named_point_counts[named_root(index)].update(ends)
        for component_id, counts in named_point_counts.items():
            named_components[component_id] = [point for point, count in counts.items() if count == 1]

        gnis_candidates = [feature for feature in candidates
                           if feature.get("properties", {}).get("water_class") in
                           {"stream", "artificial_path", "connector"}
                           and feature.get("properties", {}).get("_support_query_gnis", gnis_id) == gnis_id
                           and line_ends(feature)]
        if not gnis_candidates:
            continue
        candidate_segments = [(feature_index, ends)
                              for feature_index, feature in enumerate(gnis_candidates)
                              for ends in line_ends(feature)]
        parents = list(range(len(candidate_segments)))
        def root(index):
            while parents[index] != index:
                parents[index] = parents[parents[index]]
                index = parents[index]
            return index
        def join(left, right):
            a, b = root(left), root(right)
            if a != b:
                parents[b] = a
        for i, (_, left) in enumerate(candidate_segments):
            for j in range(i + 1, len(candidate_segments)):
                if min(metric_distance(a, b) for a in left for b in candidate_segments[j][1]) <= tolerance_m:
                    join(i, j)
        groups: dict[int, list[int]] = defaultdict(list)
        for index in range(len(candidate_segments)):
            groups[root(index)].append(index)
        for indices in groups.values():
            touching_named = set()
            candidate_point_counts = Counter(point for index in indices
                                              for point in candidate_segments[index][1])
            chain_endpoints = [point for point, count in candidate_point_counts.items() if count == 1]
            for component_id, ends in named_components.items():
                if any(metric_distance(endpoint, named_end) <= tolerance_m
                       for endpoint in chain_endpoints for named_end in ends):
                    touching_named.add(component_id)
            if len(touching_named) < 2:
                continue
            # At least one pair of touched named parts must be close enough to
            # have produced the prescribed gap query.
            if not any(min(metric_distance(a, b) for a in named_components[a_index]
                           for b in named_components[b_index]) <= max_gap_m
                       for a_index in touching_named for b_index in touching_named if a_index < b_index):
                continue
            feature_indices = {candidate_segments[index][0] for index in indices}
            for feature_index in feature_indices:
                feature = gnis_candidates[feature_index]
                ident = feature.get("properties", {}).get("source_id") or feature.get("properties", {}).get("id")
                if ident:
                    kept[ident] = (feature, gnis_id)
    return list(kept.values())


def support_gap_boxes(named_features: list[dict[str, Any]], *, max_gap_m: float = 250.0,
                      box_width_m: float = 300.0) -> list[tuple[str, tuple[float, float, float, float]]]:
    """Find prescribed Douglas gap-query boxes from six-decimal endpoint parts."""
    from pyproj import Transformer
    from shapely.geometry import LineString, Point, box
    from shapely.ops import transform

    to_metric = Transformer.from_crs("EPSG:4326", "EPSG:26913", always_xy=True).transform
    to_wgs84 = Transformer.from_crs("EPSG:26913", "EPSG:4326", always_xy=True).transform
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for feature in named_features:
        gnis = (feature.get("properties") or {}).get("gnis_id")
        if isinstance(gnis, str) and gnis:
            grouped[gnis].append(feature)
    result = set()
    for gnis, features in grouped.items():
        lines = []
        for feature in features:
            geometry = feature.get("geometry") or {}
            if geometry.get("type") == "LineString":
                lines.append(LineString([[round(float(x), 6), round(float(y), 6)] for x, y, *_ in geometry["coordinates"]]))
            elif geometry.get("type") == "MultiLineString":
                lines.extend(LineString([[round(float(x), 6), round(float(y), 6)] for x, y, *_ in part])
                             for part in geometry["coordinates"])
        if len(lines) < 2:
            continue
        parents = list(range(len(lines)))
        def root(index):
            while parents[index] != index:
                parents[index] = parents[parents[index]]
                index = parents[index]
            return index
        def join(left, right):
            a, b = root(left), root(right)
            if a != b:
                parents[b] = a
        endpoints = [set((tuple(line.coords[0]), tuple(line.coords[-1]))) for line in lines]
        for i, ends in enumerate(endpoints):
            for j in range(i + 1, len(lines)):
                if ends & endpoints[j]:
                    join(i, j)
        parts: dict[int, list[int]] = defaultdict(list)
        for index in range(len(lines)):
            parts[root(index)].append(index)
        part_points = {}
        for part_id, indices in parts.items():
            endpoint_counts = Counter(point for index in indices for point in endpoints[index])
            free = [point for point, count in endpoint_counts.items() if count == 1]
            part_points[part_id] = [transform(to_metric, Point(*point)) for point in free]
        part_ids = sorted(parts)
        for pos, first in enumerate(part_ids):
            for second in part_ids[pos + 1:]:
                pairs = [(left, right, left.distance(right))
                         for left in part_points[first] for right in part_points[second]]
                if not pairs:
                    continue
                left, right, distance = min(pairs, key=lambda item: item[2])
                if distance > max_gap_m:
                    continue
                center_x, center_y = (left.x + right.x) / 2, (left.y + right.y) / 2
                half = box_width_m / 2
                bbox_wgs84 = transform(to_wgs84, box(center_x-half, center_y-half,
                                                     center_x+half, center_y+half)).bounds
                result.add((gnis, tuple(round(value, 7) for value in bbox_wgs84)))
    return sorted(result)
