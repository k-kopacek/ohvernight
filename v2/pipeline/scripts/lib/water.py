"""M4-A NHD source-field normalization and legacy identity helpers."""
from __future__ import annotations

import json
import math
import re
import copy
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


def _reviewed_ids(review: dict[str, Any] | None, key: str) -> set[str]:
    if not review:
        return set()
    result = set()
    for item in review.get(key, []):
        if isinstance(item, dict) and isinstance(item.get("feature_id"), str):
            result.add(item["feature_id"])
    return result


def select_water_features(features: list[dict[str, Any]], config: dict[str, Any] | None = None,
                          review: dict[str, Any] | None = None, *,
                          threshold_sqkm: float | None = None) -> list[dict[str, Any]]:
    """Return the 8.2 eligibility decision for each canonical water feature.

    The optional threshold is for offline comparison reports only; contract
    validation calls this without it and therefore always uses configuration.
    No name content is inspected, only whether a source name is non-empty.
    """
    config = config or water_display_config()
    threshold = (config["unnamed_waterbody_min_area_sqkm"] if threshold_sqkm is None
                 else threshold_sqkm)
    if isinstance(threshold, bool) or not isinstance(threshold, (int, float)) or threshold < 0:
        raise ValueError("waterbody threshold must be a non-negative number")
    exclusions = _reviewed_ids(review, "exclusions")
    inclusions = _reviewed_ids(review, "inclusions")
    results = []
    for feature in features:
        props = feature.get("properties") or {}
        ident = props.get("id")
        source_layer = props.get("source_layer") or props.get("kind")
        try:
            water_class, hydro_category = classify(props.get("ftype"), props.get("fcode"), config)
        except (KeyError, TypeError, ValueError):
            water_class, hydro_category = "other", "unknown"
        named = isinstance(props.get("name"), str) and bool(props["name"].strip())
        eligible, reason = False, "unsupported_layer"

        if ident in exclusions:
            reason = "reviewed_exclusion"
        elif source_layer in {"flowline", "stream"}:
            if water_class != "stream":
                reason = "non_stream_flowline"
            elif not named:
                reason = "unnamed_stream"
            elif not isinstance(props.get("gnis_id"), str) or not props["gnis_id"].strip():
                reason = "stream_without_gnis_id"
            elif hydro_category != "perennial":
                reason = f"stream_{hydro_category}"
            else:
                eligible, reason = True, "eligible_perennial_stream"
        elif source_layer in {"waterbody", "lake", "reservoir"}:
            allowed_review_inclusion = (
                ident in inclusions and hydro_category in {"intermittent", "unknown"}
                and water_class in {"lake_pond", "reservoir"}
            )
            reservoir_code_ok = (water_class != "reservoir" or
                                 props.get("fcode") in config["reservoir_eligible_fcodes"])
            if allowed_review_inclusion:
                eligible, reason = True, "reviewed_inclusion"
            elif water_class not in {"lake_pond", "reservoir"} or not reservoir_code_ok:
                reason = "ineligible_waterbody_class_or_code"
            elif hydro_category == "intermittent":
                reason = "intermittent_waterbody"
            elif water_class == "lake_pond" and hydro_category != "perennial":
                reason = "unstated_lake_category"
            elif water_class == "reservoir" and hydro_category not in {"perennial", "unknown"}:
                reason = "ineligible_reservoir_category"
            elif named:
                eligible, reason = True, "eligible_named_waterbody"
            else:
                area = props.get("area_sqkm")
                if (isinstance(area, (int, float)) and not isinstance(area, bool)
                        and area >= threshold):
                    eligible, reason = True, "eligible_unnamed_waterbody_at_threshold"
                elif area is None:
                    reason = "unnamed_waterbody_area_unknown"
                else:
                    reason = "unnamed_waterbody_below_threshold"
        results.append({"feature": feature, "eligible": eligible, "reason": reason,
                        "water_class": water_class, "hydro_category": hydro_category})
    return results


def _line_parts(feature: dict[str, Any]) -> list[list[list[float]]]:
    geometry = feature.get("geometry") or {}
    if geometry.get("type") == "LineString":
        return geometry.get("coordinates", []) and [geometry["coordinates"]] or []
    if geometry.get("type") == "MultiLineString":
        return geometry.get("coordinates", [])
    raise ValueError(f"flowline {feature.get('properties', {}).get('id')} has non-line geometry")


def geodesic_length_km(features: list[dict[str, Any]]) -> float:
    """Measure canonical line geometry on the WGS84 ellipsoid in kilometres."""
    from pyproj import Geod

    geod = Geod(ellps="WGS84")
    total_m = 0.0
    for feature in features:
        for line in _line_parts(feature):
            if len(line) < 2:
                continue
            lon = [float(point[0]) for point in line]
            lat = [float(point[1]) for point in line]
            total_m += abs(geod.line_length(lon, lat))
    return total_m / 1000.0


def _rounded_line_parts(feature: dict[str, Any]) -> tuple[list[list[list[float]]], int]:
    lines, dropped = [], 0
    for line in _line_parts(feature):
        rounded = []
        for point in line:
            coordinate = [round(float(point[0]), 6), round(float(point[1]), 6)]
            if not rounded or rounded[-1] != coordinate:
                rounded.append(coordinate)
        if len(rounded) < 2:
            dropped += 1
        else:
            lines.append(rounded)
    return lines, dropped


def _endpoint_keys(feature: dict[str, Any]) -> set[tuple[float, float]]:
    points = set()
    for line in _line_parts(feature):
        if len(line) >= 2:
            points.add(tuple(round(float(value), 6) for value in line[0][:2]))
            points.add(tuple(round(float(value), 6) for value in line[-1][:2]))
    return points


def _flowline_candidates(features: list[dict[str, Any]], *, include_connectors: bool = True):
    by_gnis: dict[str, list[dict[str, Any]]] = {}
    support_ids = set()
    connector_ids = set()
    for feature in features:
        props = feature.get("properties") or {}
        ident = props.get("id")
        water_class = props.get("water_class")
        gnis = props.get("gnis_id")
        support_for = props.get("support_for")
        if support_for:
            if gnis and gnis != support_for:
                raise ValueError(f"support feature {ident} carries foreign GNIS ID {gnis} for {support_for}")
            if water_class in {"stream", "artificial_path", "connector"}:
                by_gnis.setdefault(str(support_for), []).append(feature)
                support_ids.add(ident)
            continue
        if not isinstance(gnis, str) or not gnis.strip():
            continue
        if water_class in {"stream", "artificial_path"}:
            by_gnis.setdefault(gnis, []).append(feature)
        elif include_connectors and water_class == "connector":
            by_gnis.setdefault(gnis, []).append(feature)
            connector_ids.add(ident)
    return by_gnis, support_ids, connector_ids


def _connected_components(nodes: list[str], adjacency: dict[str, set[str]]) -> list[list[str]]:
    remaining = set(nodes)
    result = []
    while remaining:
        start = min(remaining)
        pending, found = [start], set()
        while pending:
            ident = pending.pop()
            if ident in found:
                continue
            found.add(ident)
            pending.extend(sorted(adjacency[ident] - found, reverse=True))
        remaining.difference_update(found)
        result.append(sorted(found))
    return result


def _component_groups(features: list[dict[str, Any]], config: dict[str, Any], review: dict[str, Any],
                      *, include_connectors: bool):
    by_gnis, support_ids, connector_ids = _flowline_candidates(
        features, include_connectors=include_connectors)
    selected = {row["feature"]["properties"].get("id"): row["eligible"]
                for row in select_water_features(features, config, review)}
    output_groups, water_groups, assignments = [], {}, {
        (feature.get("properties") or {}).get("id"): None for feature in features
    }
    summaries, connectors_used = [], []
    for gnis_id, candidates in sorted(by_gnis.items()):
        candidates = sorted(candidates, key=lambda f: f["properties"]["id"])
        lookup = {feature["properties"]["id"]: feature for feature in candidates}
        names = {}
        for feature in candidates:
            props = feature.get("properties") or {}
            ident = props.get("id")
            if ident in support_ids:
                continue
            name = props.get("name")
            names.setdefault(name, []).append(ident)
        if len(names) > 1:
            detail = ", ".join(f"{name!r}: {sorted(ids)}" for name, ids in
                                sorted(names.items(), key=lambda row: repr(row[0])))
            raise ValueError(f"multiple names under GNIS {gnis_id}: {detail}")
        name = next(iter(names), None)
        if not isinstance(name, str) or not name.strip():
            continue
        endpoint_index: dict[tuple[float, float], set[str]] = {}
        for feature in candidates:
            ident = feature["properties"]["id"]
            for endpoint in _endpoint_keys(feature):
                endpoint_index.setdefault(endpoint, set()).add(ident)
        adjacency = {ident: set() for ident in lookup}
        for connected in endpoint_index.values():
            for ident in connected:
                adjacency[ident].update(connected - {ident})
        parts = _connected_components(sorted(lookup), adjacency)
        displayable = []
        for part in parts:
            seeds = {ident for ident in part if selected.get(ident, False)
                     and ident not in support_ids}
            if not seeds:
                continue
            drawn = set(seeds)
            pending = sorted(seeds)
            while pending:
                current = pending.pop(0)
                for neighbor in sorted(adjacency[current] - drawn):
                    props = lookup[neighbor]["properties"]
                    if (props.get("water_class") == "artificial_path"
                            and neighbor not in support_ids):
                        drawn.add(neighbor)
                        pending.append(neighbor)
            member_ids = sorted(drawn)
            part_length = geodesic_length_km([lookup[ident] for ident in member_ids])
            displayable.append({"all_ids": part, "drawn_ids": member_ids,
                                "drawn_length_km": part_length,
                                "tie_id": min(member_ids)})
        displayable.sort(key=lambda part: (-part["drawn_length_km"], part["tie_id"]))
        for part_number, part in enumerate(displayable, start=1):
            group_id = f"nhd-gnis-{gnis_id}" + (f"-p{part_number}" if part_number > 1 else "")
            exclusion_ids = _reviewed_ids(review, "exclusions")
            if group_id in exclusion_ids:
                continue
            members = [lookup[ident] for ident in part["drawn_ids"]]
            name_set = {feature["properties"].get("name") for feature in members}
            if len(name_set) != 1 or next(iter(name_set)) != name:
                raise ValueError(f"G2 group {group_id} member names differ")
            lines = []
            for member in members:
                member_lines, dropped = _rounded_line_parts(member)
                if dropped and not member_lines:
                    raise ValueError(f"R63 drawn member {member['properties']['id']} collapses after rounding")
                lines.extend(member_lines)
            length_km = part["drawn_length_km"]
            evidence = copy.deepcopy(members[0]["properties"].get("evidence"))
            group_feature = {
                "type": "Feature",
                "geometry": {"type": "MultiLineString", "coordinates": lines},
                "properties": {"id": group_id, "name": name, "gnis_id": gnis_id,
                               "water_class": "stream", "hydro_category": "perennial",
                               "member_count": len(members), "length_km": round(length_km, 3),
                               "evidence": evidence},
            }
            output_groups.append(group_feature)
            water_groups[group_id] = part["drawn_ids"]
            for ident in part["drawn_ids"]:
                if assignments.get(ident) is not None:
                    raise ValueError(f"G4 member {ident} belongs to more than one group")
                assignments[ident] = group_id
            connector_records = []
            for ident in part["all_ids"]:
                if ident not in connector_ids:
                    continue
                connector = lookup[ident]["properties"]
                if connector.get("gnis_id") != gnis_id or connector.get("name") != name:
                    raise ValueError(f"G11 connector {ident} GNIS or name differs from group {group_id}")
                record = {"id": ident, "gnis_id": gnis_id, "name": connector.get("name"),
                          "group_id": group_id,
                          "length_km": round(geodesic_length_km([lookup[ident]]), 6)}
                connector_records.append(record)
                connectors_used.append(record)
            connectivity_ids = sorted(set(part["all_ids"]) - set(part["drawn_ids"]))
            summaries.append({"group_id": group_id, "gnis_id": gnis_id, "name": name,
                              "member_ids": part["drawn_ids"], "connectivity_ids": connectivity_ids,
                              "connector_ids": [item["id"] for item in connector_records],
                              "drawn_length_km": length_km, "line_count": len(lines),
                              "member_count": len(members)})
    feature_ids = set(assignments)
    collisions = feature_ids & set(water_groups)
    if collisions:
        raise ValueError(f"group ID collides with a canonical feature ID: {sorted(collisions)}")
    return {"groups": output_groups, "water_groups": water_groups,
            "group_assignments": assignments, "group_summaries": summaries,
            "connectors_used": sorted(connectors_used, key=lambda row: (row["gnis_id"], row["id"]))}


def _river_source_stats(features: list[dict[str, Any]], groups: list[dict[str, Any]],
                        water_groups: dict[str, list[str]], config: dict[str, Any], region_id: str):
    expected = config.get("expected_major_rivers", {}).get(region_id, [])
    groups_by_gnis = {}
    for feature in groups:
        props = feature["properties"]
        groups_by_gnis.setdefault(props.get("gnis_id"), []).append(feature)
    by_id = {(feature.get("properties") or {}).get("id"): feature for feature in features}
    checks = []
    for row in expected:
        gnis_id = row["gnis_id"]
        minimum = row.get("minimum_drawn_fraction", 0.8)
        source = [feature for feature in features
                  if not (feature.get("properties") or {}).get("support_for")
                  and (feature.get("properties") or {}).get("gnis_id") == gnis_id
                  and ((feature.get("properties") or {}).get("water_class") == "artificial_path"
                       or ((feature.get("properties") or {}).get("water_class") == "stream"
                           and (feature.get("properties") or {}).get("hydro_category") == "perennial"))]
        denominator = geodesic_length_km(source)
        drawn_features = []
        for group_feature in groups_by_gnis.get(gnis_id, []):
            group_id = group_feature["properties"]["id"]
            drawn_features.extend(by_id[ident] for ident in water_groups.get(group_id, [])
                                  if ident in by_id)
        numerator = geodesic_length_km(drawn_features)
        checks.append({"gnis_id": gnis_id, "minimum_drawn_fraction": minimum,
                       "group_ids": [feature["properties"]["id"] for feature in groups_by_gnis.get(gnis_id, [])],
                       "group_present": bool(groups_by_gnis.get(gnis_id)),
                       "seed_present": any((feature.get("properties") or {}).get("water_class") == "stream"
                                            and (feature.get("properties") or {}).get("hydro_category") == "perennial"
                                            for feature in source),
                       "drawn_length_km": numerator, "source_length_km": denominator,
                       "drawn_fraction": min(1.0, numerator / denominator) if denominator else 0.0,
                       "member_gnis_ids": [feature["properties"].get("gnis_id") for feature in drawn_features]})
    return checks


def _extent_edge_splits(group_summaries, features, coverage):
    if coverage is None:
        return []
    from shapely.geometry import Point, shape

    if hasattr(coverage, "boundary"):
        boundary = coverage.boundary
    else:
        geometry = coverage.get("geometry") if isinstance(coverage, dict) and coverage.get("type") == "Feature" else coverage
        boundary = shape(geometry).boundary
    by_id = {(feature.get("properties") or {}).get("id"): feature for feature in features}
    summaries_by_gnis = {}
    for row in group_summaries:
        summaries_by_gnis.setdefault(row["gnis_id"], []).append(row)
    splits = []
    from pyproj import Geod
    geod = Geod(ellps="WGS84")
    for gnis_id, rows in sorted(summaries_by_gnis.items()):
        if len(rows) < 2:
            continue
        edge = False
        for row in rows:
            for ident in row["member_ids"]:
                for line in _line_parts(by_id[ident]):
                    for coordinate in (line[0], line[-1]):
                        if boundary.distance(Point(float(coordinate[0]), float(coordinate[1]))) <= 1e-6:
                            edge = True
        if edge:
            row_endpoints = []
            for row in rows:
                endpoints = []
                for ident in row["member_ids"]:
                    for line in _line_parts(by_id[ident]):
                        if len(line) >= 2:
                            endpoints.extend((line[0][:2], line[-1][:2]))
                row_endpoints.append(endpoints)
            gaps = []
            for index in range(len(row_endpoints) - 1):
                distances = []
                for left in row_endpoints[index]:
                    for right in row_endpoints[index + 1]:
                        _, _, distance = geod.inv(float(left[0]), float(left[1]),
                                                   float(right[0]), float(right[1]))
                        distances.append(abs(distance))
                gaps.append(round(min(distances), 3) if distances else None)
            splits.append({"gnis_id": gnis_id, "group_ids": [row["group_id"] for row in rows],
                           "line_counts": [row["line_count"] for row in rows],
                           "drawn_lengths_km": [row["drawn_length_km"] for row in rows],
                           "gaps_m": gaps})
    return splits


def validate_expected_major_rivers(result: dict[str, Any], config: dict[str, Any], region_id: str):
    """Fail on missing, short or foreign expected rivers; report only the one pending absence."""
    expected = config.get("expected_major_rivers", {}).get(region_id, [])
    pending = config.get("pending_external_source_refresh")
    if pending is not None and (set(pending) != {"region_id", "gnis_id", "state", "reason"}
                                or pending.get("state") != "PENDING_EXTERNAL_SOURCE_REFRESH"
                                or not pending.get("reason")
                                or pending.get("region_id") != "douglas-co"
                                or pending.get("gnis_id") != "00201759"):
        raise ValueError("invalid pending external source refresh marker")
    checks = {row["gnis_id"]: row for row in result.get("major_river_checks", [])}
    pending_rows = []
    for river in expected:
        gnis_id = river["gnis_id"]
        check = checks.get(gnis_id)
        minimum = river.get("minimum_drawn_fraction", 0.8)
        if (isinstance(minimum, bool) or not isinstance(minimum, (int, float))
                or not 0 <= minimum <= 1):
            raise ValueError(f"invalid minimum drawn fraction for major river {gnis_id}")
        if check is None:
            raise ValueError(f"expected major river {gnis_id} missing validation record")
        is_pending = (pending is not None and pending.get("region_id") == region_id
                      and pending.get("gnis_id") == gnis_id and not check["seed_present"])
        if not check["group_present"] or not check["seed_present"]:
            if is_pending:
                pending_rows.append({**check, "state": pending["state"], "reason": pending["reason"]})
                continue
            raise ValueError(f"expected major river {gnis_id} missing a perennial drawn group")
        foreign = sorted({value for value in check["member_gnis_ids"] if value != gnis_id})
        group_gnis = {feature.get("properties", {}).get("id"):
                      feature.get("properties", {}).get("gnis_id")
                      for feature in result.get("groups", [])}
        foreign.extend(sorted(group_id for group_id in check.get("group_ids", [])
                              if group_gnis.get(group_id) != gnis_id))
        if foreign:
            raise ValueError(f"expected major river {gnis_id} has foreign group members {foreign}")
        if check["drawn_fraction"] < check["minimum_drawn_fraction"]:
            raise ValueError(f"expected major river {gnis_id} drawn fraction {check['drawn_fraction']:.6f} below {check['minimum_drawn_fraction']:.6f}")
    result["pending_external_source_refresh"] = pending_rows
    return pending_rows


def group_flowlines(features: list[dict[str, Any]], config: dict[str, Any] | None = None, *,
                    region_id: str, review: dict[str, Any] | None = None, coverage=None,
                    enforce_major: bool = True) -> dict[str, Any]:
    """Group canonical flowlines without mutating them or inventing coordinates."""
    config = config or water_display_config()
    review = review or {"inclusions": [], "exclusions": []}
    ids = [(feature.get("properties") or {}).get("id") for feature in features]
    if any(not ident for ident in ids) or len(ids) != len(set(ids)):
        raise ValueError("grouping requires unique non-empty canonical feature IDs")
    with_connectors = _component_groups(features, config, review, include_connectors=True)
    without_connectors = _component_groups(features, config, review, include_connectors=False)
    if {ident for ident, group_id in with_connectors["group_assignments"].items() if group_id} != {
            ident for ident, group_id in without_connectors["group_assignments"].items() if group_id}:
        raise ValueError("G11 connector participation changed the drawn member set")
    checks = _river_source_stats(features, with_connectors["groups"], with_connectors["water_groups"],
                                 config, region_id)
    result = {**with_connectors, "major_river_checks": checks,
              "multi_part_gnis_ids": sorted({row["gnis_id"] for row in with_connectors["group_summaries"]
                                              if sum(other["gnis_id"] == row["gnis_id"]
                                                     for other in with_connectors["group_summaries"]) > 1})}
    result["extent_edge_splits"] = _extent_edge_splits(result["group_summaries"], features, coverage)
    if enforce_major:
        validate_expected_major_rivers(result, config, region_id)
    return result


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
