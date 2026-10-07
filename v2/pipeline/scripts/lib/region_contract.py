"""Pure validation for the regional data contract.

The manifest is a hand-reviewed declaration. This module checks that declaration,
the files it points to, and the evidence semantics without reading the clock.
"""
from __future__ import annotations

import json
import copy
import hashlib
import math
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

from jsonschema import Draft202012Validator, FormatChecker
from shapely.geometry import shape

from lib.common import ROOT
from fetch_trails import ACTIVITIES
from lib.water import (classify as classify_water, group_flowlines,
                       select_water_features)

REGION_MANIFEST_SCHEMA = json.loads((ROOT / "schema/region-manifest.schema.json").read_text())
WATER_DISPLAY_CONFIG = json.loads((ROOT / "config/water_display.json").read_text())

APPROVED_VERIFICATION_METHODS = {
    "arcgis_rest_query", "source_fetch", "rest_api", "html_change_monitor",
    "derived_intersection", "manual_claim_review",
}
FACT_DIMENSIONS = {
    "ownership", "public_access", "camping_permission", "closures",
    "restrictions", "road_access", "trail_access", "recreation_permission",
}
TRANSPORT_STATUSES = {"available", "unavailable", "skipped"}
RESERVED_PROPERTIES = {
    "id", "name", "evidence", "camping_permission", "access_status", "access_reason",
    "road_conditions", "land_class", "needs_review", "actual_site_confirmed", "evaluated_trip",
}


class ContractError(ValueError):
    def __init__(self, rule: str, region: str, layer: str | None, detail: str):
        self.rule, self.region, self.layer = rule, region, layer
        prefix = f"{region}/{layer}" if layer else region
        super().__init__(f"{rule} {prefix}: {detail}")


def _error(rule, manifest, layer, detail):
    raise ContractError(rule, manifest.get("region", {}).get("id", "?"), layer, detail)


def _json_pointer(document, pointer):
    if pointer == "":
        return document
    if not isinstance(pointer, str) or not pointer.startswith("/"):
        raise KeyError(pointer)
    current = document
    for token in pointer[1:].split("/"):
        token = token.replace("~1", "/").replace("~0", "~")
        if isinstance(current, list):
            current = current[int(token)]
        else:
            current = current[token]
    return current


def _display_water(feature):
    properties = feature.get("properties") or {}
    geometry = feature.get("geometry") or {}
    name = properties.get("name")
    return (isinstance(name, str) and bool(name.strip()) and
            (((properties.get("kind") == "flowline" or properties.get("source_layer") == "flowline") and
              geometry.get("type") in {"LineString", "MultiLineString"}) or
             ((properties.get("kind") == "waterbody" or properties.get("source_layer") == "waterbody") and
              geometry.get("type") in {"Polygon", "MultiPolygon"})))


def _display_round_path(points, minimum):
    if not points:
        return None, 1
    rounded = [[round(float(point[0]), 6), round(float(point[1]), 6)] for point in points]
    closed = rounded[0] == rounded[-1]
    result = [rounded[0]]
    for point in rounded[1:]:
        if point != result[-1]:
            result.append(point)
    if closed and len(result) > 1 and result[-1] != result[0]:
        result.append(result[0])
    if len(result) < minimum:
        return None, 1
    return result, 0


def _display_transform_geometry(geometry):
    if geometry is None:
        return None, 0
    result = dict(geometry)
    coords = geometry.get("coordinates")
    geometry_type = geometry.get("type")
    if geometry_type == "Point":
        result["coordinates"] = [round(float(coords[0]), 6), round(float(coords[1]), 6)]
    elif geometry_type == "MultiPoint":
        result["coordinates"] = [[round(float(point[0]), 6), round(float(point[1]), 6)] for point in coords]
    elif geometry_type == "LineString":
        path, dropped = _display_round_path(coords, 2)
        return (None, dropped) if path is None else ({**result, "coordinates": path}, dropped)
    elif geometry_type == "MultiLineString":
        lines, dropped = [], 0
        for line in coords:
            path, count = _display_round_path(line, 2)
            dropped += count
            if path is not None:
                lines.append(path)
        if not lines:
            return None, dropped
        result["coordinates"] = lines
    elif geometry_type == "Polygon":
        rings, dropped = [], 0
        for index, ring in enumerate(coords):
            path, count = _display_round_path(ring, 4)
            dropped += count
            if index == 0 and path is None:
                return None, dropped
            if path is not None:
                rings.append(path)
        result["coordinates"] = rings
    elif geometry_type == "MultiPolygon":
        polygons, dropped = [], 0
        for polygon in coords:
            if not polygon:
                dropped += 1
                continue
            exterior, count = _display_round_path(polygon[0], 4)
            dropped += count
            if exterior is None:
                continue
            rings = [exterior]
            for hole in polygon[1:]:
                path, count = _display_round_path(hole, 4)
                dropped += count
                if path is not None:
                    rings.append(path)
            polygons.append(rings)
        if not polygons:
            return None, dropped
        result["coordinates"] = polygons
    else:
        raise ValueError(f"unsupported geometry type: {geometry_type}")
    return result, 0 if geometry_type in {"Point", "MultiPoint"} else dropped


def _display_geometry_well_formed(geometry):
    if not isinstance(geometry, dict) or not geometry.get("type") or "coordinates" not in geometry:
        return False
    geometry_type = geometry["type"]
    coords = geometry["coordinates"]
    if geometry_type == "Point":
        return isinstance(coords, list) and len(coords) >= 2 and all(isinstance(value, (int, float)) and math.isfinite(value) for value in coords[:2])
    if geometry_type == "MultiPoint":
        return isinstance(coords, list) and bool(coords) and all(
            isinstance(point, list) and len(point) >= 2 and all(isinstance(value, (int, float)) and math.isfinite(value) for value in point[:2])
            for point in coords
        )
    if geometry_type == "LineString":
        return isinstance(coords, list) and len(coords) >= 2 and all(isinstance(point, list) and len(point) >= 2 for point in coords)
    if geometry_type == "MultiLineString":
        return isinstance(coords, list) and bool(coords) and all(
            isinstance(line, list) and len(line) >= 2 and all(isinstance(point, list) and len(point) >= 2 for point in line)
            for line in coords
        )
    if geometry_type == "Polygon":
        return isinstance(coords, list) and bool(coords) and all(
            isinstance(ring, list) and len(ring) >= 4 and ring[0] == ring[-1] for ring in coords
        )
    if geometry_type == "MultiPolygon":
        return isinstance(coords, list) and bool(coords) and all(
            isinstance(polygon, list) and bool(polygon) and all(
                isinstance(ring, list) and len(ring) >= 4 and ring[0] == ring[-1] for ring in polygon
            ) for polygon in coords
        )
    return False


def _display_json_bytes(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n").encode("utf-8")


def _resolved_bytes(resolve, path, document):
    raw_bytes = getattr(resolve, "raw_bytes", None)
    if raw_bytes is not None and path in raw_bytes:
        return raw_bytes[path]
    return _display_json_bytes(document)


def validate_water_alias_file(index, document, raw_bytes, region_id):
    """Validate the deferred alias artifact reference and return its alias map."""
    if not isinstance(index, dict) or "water_id_aliases" in index:
        _error("R68", {"region": {"id": region_id}}, None,
               "water aliases must not be embedded in display index.json")
    entry = index.get("water_aliases")
    expected_path = f"regions/{region_id}/display/water-aliases.json"
    if (not isinstance(entry, dict) or set(entry) != {"path", "bytes", "sha256"} or
            entry.get("path") != expected_path):
        _error("R68", {"region": {"id": region_id}}, None,
               "display index water alias artifact reference is missing or invalid")
    if (not isinstance(document, dict) or set(document) != {"region_id", "water_id_aliases"} or
            document.get("region_id") != region_id or not isinstance(document.get("water_id_aliases"), dict)):
        _error("R68", {"region": {"id": region_id}}, None, "water alias file is invalid")
    aliases = document["water_id_aliases"]
    if any(not isinstance(key, str) or not key or not isinstance(value, str) or not value
           for key, value in aliases.items()):
        _error("R68", {"region": {"id": region_id}}, None, "water alias file has invalid IDs")
    if (entry.get("bytes") != len(raw_bytes) or
            entry.get("sha256") != hashlib.sha256(raw_bytes).hexdigest()):
        _error("R68", {"region": {"id": region_id}}, None,
               "water alias file hash or byte count differs from index")
    return aliases


def _display_error(manifest, layer, detail):
    _error("R60", manifest, layer, detail)


def validate_water_contract_data(manifest, canonical, config, aliases, display_features):
    """Validate M4-A water identity, fixed classifications, aliases and R75."""
    region = manifest.get("region", {}).get("id", "?")
    by_legacy = {}
    ids = set()
    any_enriched = any(
        any(key in (feature.get("properties") or {}) for key in
            ("source_id", "source_namespace", "ftype", "fcode", "water_class", "hydro_category", "legacy_ids"))
        for layer_id, feature in canonical
    )
    if not any_enriched:
        return
    current_water_ids = {(feature.get("properties") or {}).get("id") for _, feature in canonical}
    for layer_id, feature in canonical:
        props = feature.get("properties") or {}
        source_id = props.get("source_id")
        expected_id = None
        if isinstance(source_id, str) and source_id:
            sanitized = re.sub(r"[^A-Za-z0-9-]", "", source_id)
            expected_id = "nhd-" + sanitized if sanitized else None
        if (not isinstance(source_id, str) or not source_id or props.get("source_namespace") != "usgs_nhd" or
                isinstance(props.get("ftype"), bool) or not isinstance(props.get("ftype"), int) or
                isinstance(props.get("fcode"), bool) or not isinstance(props.get("fcode"), int) or
                props.get("id") != expected_id or expected_id is None or expected_id in ids):
            _error("R66", manifest, layer_id, "invalid, missing or duplicate source ID, ftype, fcode or derived ID")
        ids.add(expected_id)
        try:
            water_class, hydro_category = classify_water(props["ftype"], props["fcode"], config)
        except (KeyError, TypeError, ValueError):
            _error("R67", manifest, layer_id, "water ftype or fcode cannot be classified")
        if props.get("water_class") != water_class or props.get("hydro_category") != hydro_category:
            _error("R67", manifest, layer_id, "water_class or hydro_category differs from water_display.json")
        legacy = props.get("legacy_ids")
        if (not isinstance(legacy, list) or any(not isinstance(value, str) or not value for value in legacy)
                or len(legacy) != len(set(legacy))):
            _error("R68", manifest, layer_id, "legacy_ids must be distinct non-empty strings")
        for legacy_id in legacy:
            if legacy_id in current_water_ids:
                _error("R68", manifest, layer_id,
                       f"legacy ID {legacy_id} equals the ID of a current water feature")
            if legacy_id in by_legacy:
                _error("R68", manifest, layer_id, f"legacy ID {legacy_id} occurs on multiple water features")
            by_legacy[legacy_id] = props["id"]
        forbidden = {"fishing", "fish", "boating", "boat", "paddling", "paddleboarding", "swimming", "swim",
                     "activities", "access", "public_access"} | (RESERVED_PROPERTIES - {"id", "name", "evidence"})
        if forbidden & set(props):
            _error("R75", manifest, layer_id, f"water feature carries reserved activity/access properties: {sorted(forbidden & set(props))}")
    displayed_legacy = {}
    displayed_ids = set()
    for layer_id, feature in display_features:
        props = feature.get("properties") or {}
        display_id = props.get("id")
        displayed_ids.add(display_id)
        for legacy_id, canonical_display_id in by_legacy.items():
            if canonical_display_id != display_id:
                continue
            if legacy_id in displayed_legacy:
                _error("R68", manifest, layer_id, f"display repeats legacy ID {legacy_id}")
            displayed_legacy[legacy_id] = display_id
    if not isinstance(aliases, dict) or set(aliases) != set(displayed_legacy):
        _error("R68", manifest, None, "water_id_aliases keys do not exactly match displayed legacy IDs")
    if any(value not in displayed_ids for value in aliases.values()):
        _error("R68", manifest, None, "water_id_aliases contains a target that is not a display ID")
    if any(aliases.get(legacy_id) != display_id or by_legacy.get(legacy_id) != display_id
           for legacy_id, display_id in displayed_legacy.items()):
        _error("R68", manifest, None, "water_id_aliases does not match canonical legacy mapping")


def _validate_water_review(review, canonical, region_id, config, group_ids=()):
    """Validate the optional, manually reviewed M4 inclusion/exclusion lists."""
    if review is None:
        return {"inclusions": [], "exclusions": []}
    manifest = {"region": {"id": region_id}}
    if not isinstance(review, dict) or set(review) != {"inclusions", "exclusions"}:
        _error("R73", manifest, None, "water-review must contain only inclusions and exclusions")
    canonical_by_id = {(feature.get("properties") or {}).get("id"): feature
                       for _, feature in canonical}
    valid_ids = set(canonical_by_id) | set(group_ids)
    exclusions, inclusions, seen = [], [], set()
    allowed_exclusions = {"stormwater_detention", "water_treatment", "industrial_or_tailings",
                          "water_supply_no_public_use", "not_a_waterbody", "duplicate_of"}
    records = (("exclusions", allowed_exclusions, exclusions),
               ("inclusions", {"reviewed_intermittent_waterbody"}, inclusions))
    community_hosts = {"facebook.com", "reddit.com", "youtube.com", "instagram.com",
                       "alltrails.com", "wikiloc.com", "tripadvisor.com"}
    for field, reason_codes, output in records:
        rows = review[field]
        if not isinstance(rows, list):
            _error("R73", manifest, None, f"water-review {field} must be an array")
        for row in rows:
            expected = {"feature_id", "reason_code", "evidence", "reviewed_at"}
            if not isinstance(row, dict) or set(row) != expected:
                _error("R73", manifest, None, f"water-review {field} record has invalid fields")
            ident, reason = row["feature_id"], row["reason_code"]
            if not isinstance(ident, str) or not ident or ident not in valid_ids:
                _error("R73", manifest, None, f"water-review ID {ident!r} does not resolve to canonical data")
            if ident in seen:
                _error("R73", manifest, None, f"water-review ID {ident} is duplicated or conflicts")
            seen.add(ident)
            if reason not in reason_codes:
                _error("R73", manifest, None, f"water-review reason code {reason!r} is invalid")
            evidence = row["evidence"]
            if not isinstance(evidence, dict) or set(evidence) != {"source_url", "agency", "statement"}:
                _error("R73", manifest, None, "water-review evidence must have source_url, agency and statement")
            source_url = evidence["source_url"]
            parsed = urlparse(source_url) if isinstance(source_url, str) else None
            if (parsed is None or parsed.scheme not in {"http", "https"} or not parsed.hostname
                    or any(parsed.hostname == host or parsed.hostname.endswith("." + host)
                           for host in community_hosts | set(config.get("non_claim_hosts", [])))):
                _error("R73", manifest, None, "water-review source must be HTTP(S) and non-community")
            statement = evidence["statement"]
            if (not isinstance(evidence["agency"], str) or not evidence["agency"].strip()
                    or not isinstance(statement, str) or not statement.strip()):
                _error("R73", manifest, None, "water-review evidence is incomplete")
            feature_name = (canonical_by_id.get(ident, {}).get("properties") or {}).get("name")
            statement_words = set(re.findall(r"[a-z0-9]+", statement.casefold()))
            name_words = set(re.findall(r"[a-z0-9]+", str(feature_name or "").casefold()))
            name_only_fillers = {"a", "an", "the", "is", "was", "called", "named", "known", "as", "site", "water"}
            if (statement.strip().casefold() == str(feature_name or "").strip().casefold()
                    or (name_words and statement_words <= name_words | name_only_fillers)):
                _error("R73", manifest, None, "water-review statement cannot be supported only by the feature name")
            if reason == "water_supply_no_public_use" and not re.search(
                    r"no public use|not open to the public|public use is not allowed|public access is not allowed",
                    statement, re.IGNORECASE):
                _error("R73", manifest, None,
                       "water_supply_no_public_use requires evidence that states no public use")
            quoted = re.findall(r"(?:\"([^\"]*)\"|'([^']*)')", statement)
            if any(len((first or second).split()) > 25 for first, second in quoted):
                _error("R73", manifest, None, "water-review quotation exceeds 25 words")
            reviewed_at = row["reviewed_at"]
            try:
                parsed_date = datetime.fromisoformat(reviewed_at.replace("Z", "+00:00"))
            except (AttributeError, TypeError, ValueError):
                parsed_date = None
            if parsed_date is None or parsed_date.tzinfo is None:
                _error("R73", manifest, None, "water-review reviewed_at must be RFC 3339")
            props = (canonical_by_id.get(ident, {}).get("properties") or {})
            if field == "inclusions" and not (
                    props.get("source_layer") == "waterbody"
                    and props.get("water_class") in {"lake_pond", "reservoir"}
                    and props.get("hydro_category") in {"intermittent", "unknown"}):
                _error("R73", manifest, None, "reviewed inclusion must target an intermittent waterbody")
            output.append(row)
    return {"inclusions": inclusions, "exclusions": exclusions}


def validate_m4b_water_layer(manifest, layer, canonical_features, display_features,
                             config=None, review=None):
    """Run R69-R73 and grouped R61-R63 against a fixture or future grouped artifact."""
    from lib.water import water_display_config
    config = config or water_display_config()
    region_id = manifest.get("region", {}).get("id", "?")
    layer_id = layer.get("id", "water")
    select = (layer.get("display") or {}).get("select")
    possible_group_ids = ()
    if select == "streams":
        try:
            possible_group_ids = [feature["properties"]["id"] for feature in
                                  group_flowlines(canonical_features, config, region_id=region_id,
                                                  enforce_major=False)["groups"]]
        except (ValueError, KeyError, TypeError) as exc:
            _error("R70", manifest, layer_id, str(exc))
    selection = _validate_water_review(review, [(layer_id, feature) for feature in canonical_features],
                                       region_id, config, possible_group_ids)
    by_id = {(feature.get("properties") or {}).get("id"): feature for feature in display_features}
    if len(by_id) != len(display_features):
        _error("R61", manifest, layer_id, "display has duplicate IDs")
    if select == "bodies":
        decisions = select_water_features(canonical_features, config, selection)
        eligible = {row["feature"]["properties"]["id"] for row in decisions
                    if row["eligible"] and (row["feature"].get("properties") or {}).get("source_layer") == "waterbody"}
        if set(by_id) != eligible:
            _error("R69", manifest, layer_id, "waterbody display set differs from reviewed eligibility")
        for ident in eligible:
            props = (by_id[ident].get("properties") or {})
            water_class, category = classify_water(props.get("ftype"), props.get("fcode"), config)
            if props.get("water_class") != water_class or props.get("hydro_category") != category:
                _error("R72", manifest, layer_id, f"displayed waterbody {ident} has incorrect classification")
            if water_class not in {"lake_pond", "reservoir"} or category != "perennial":
                if ident not in {row["feature_id"] for row in selection["inclusions"]}:
                    _error("R72", manifest, layer_id, f"displayed waterbody {ident} is outside allowed classes")
        return {"water_groups": {}, "group_assignments": {}}
    if select != "streams":
        _error("R60", manifest, layer_id, "M4 water display requires select streams or bodies")
    try:
        grouped = group_flowlines(canonical_features, config, region_id=region_id,
                                  review=selection, enforce_major=True)
    except (ValueError, KeyError, TypeError) as exc:
        _error("R70", manifest, layer_id, str(exc))
    expected = {feature["properties"]["id"]: feature for feature in grouped["groups"]}
    if set(by_id) != set(expected):
        _error("R69", manifest, layer_id, "stream display group set differs from canonical selection")
    for ident, expected_feature in expected.items():
        actual = by_id[ident]
        props = actual.get("properties") or {}
        exp_props = expected_feature["properties"]
        if actual.get("geometry") != expected_feature.get("geometry"):
            _error("R71", manifest, layer_id, f"group {ident} geometry differs from ordered member geometry")
        for key in ("name", "gnis_id", "member_count", "length_km"):
            if props.get(key) != exp_props.get(key):
                _error("R71", manifest, layer_id, f"group {ident} {key} differs from canonical members")
        if props.get("water_class") != "stream" or props.get("hydro_category") != "perennial":
            _error("R72", manifest, layer_id, f"group {ident} has an unsupported class")
        expected_properties = expected_feature.get("properties") or {}
        if _display_json_bytes(props) != _display_json_bytes(expected_properties):
            _error("R62", manifest, layer_id, f"group {ident} properties or evidence differ from its members")
    expected_membership = grouped["group_assignments"]
    for feature in canonical_features:
        props = feature.get("properties") or {}
        ident = props.get("id")
        if props.get("group_id") != expected_membership.get(ident):
            _error("R70", manifest, layer_id, f"canonical group_id membership differs for {ident}")
    return grouped


def _validate_water_contract(manifest, resolve):
    canonical, display = [], []
    for layer in manifest["layers"]:
        if layer.get("kind") != "water" or layer.get("format") != "feature_collection":
            continue
        document = resolve(layer["path"])
        features = _json_pointer(document, layer.get("pointer", ""))["features"]
        canonical.extend((layer["id"], feature) for feature in features)
        if layer.get("display"):
            displayed = resolve(layer["display"]["path"]).get("features", [])
            display.extend((layer["id"], feature) for feature in displayed)
    if not canonical:
        return
    if manifest.get("water_review") is not None:
        region_id = manifest.get("region", {}).get("id", "?")
        review_path = manifest["water_review"].get("path")
        if review_path != f"regions/{region_id}/water-review.json":
            _error("R73", manifest, None, "water-review path must be region-scoped")
        try:
            review_document = resolve(review_path)
        except (KeyError, IndexError, TypeError, ValueError, FileNotFoundError):
            _error("R73", manifest, None, "water-review file does not resolve")
        possible_group_ids = ()
        if any((feature.get("properties") or {}).get("source_layer") == "flowline"
               for _, feature in canonical):
            try:
                possible_group_ids = [feature["properties"]["id"] for feature in
                                      group_flowlines([feature for _, feature in canonical],
                                                      WATER_DISPLAY_CONFIG, region_id=region_id,
                                                      enforce_major=False)["groups"]]
            except (ValueError, KeyError, TypeError) as exc:
                _error("R70", manifest, None, str(exc))
        _validate_water_review(review_document, canonical, region_id,
                               WATER_DISPLAY_CONFIG, possible_group_ids)
    # Older contract fixtures can declare a water layer without the M4 source
    # identity fields. Only M4-enriched data has the deferred alias artifact.
    any_enriched = any(
        any(key in (feature.get("properties") or {}) for key in
            ("source_id", "source_namespace", "ftype", "fcode", "water_class", "hydro_category", "legacy_ids"))
        for _, feature in canonical
    )
    if not any_enriched:
        validate_water_contract_data(manifest, canonical, WATER_DISPLAY_CONFIG, {}, display)
        return
    index_path = f"regions/{manifest['region']['id']}/display/index.json"
    index = resolve(index_path) if any(layer.get("display") for layer in manifest["layers"] if layer.get("kind") == "water") else {}
    aliases = {}
    if index:
        alias_entry = index.get("water_aliases")
        if isinstance(alias_entry, dict) and isinstance(alias_entry.get("path"), str):
            try:
                alias_document = resolve(alias_entry["path"])
            except (KeyError, IndexError, TypeError, ValueError, FileNotFoundError):
                _error("R68", manifest, None, "water alias file does not resolve")
            aliases = validate_water_alias_file(
                index, alias_document, _resolved_bytes(resolve, alias_entry["path"], alias_document),
                manifest["region"]["id"])
        else:
            validate_water_alias_file(index, None, b"", manifest["region"]["id"])
    validate_water_contract_data(manifest, canonical, WATER_DISPLAY_CONFIG, aliases, display)


def _validate_display(manifest, resolve, coverage):
    region_id = manifest["region"]["id"]
    declared = [(layer["id"], layer) for layer in manifest["layers"] if layer.get("display")]
    if manifest.get("coverage", {}).get("display"):
        declared.append(("coverage", manifest["coverage"]))
    if not declared:
        return
    water_review = None
    if manifest.get("water_review") is not None:
        review_path = manifest["water_review"].get("path")
        try:
            water_review = resolve(review_path)
        except (KeyError, IndexError, TypeError, ValueError, FileNotFoundError):
            _error("R73", manifest, None, "water-review file does not resolve")
    index_path = f"regions/{region_id}/display/index.json"
    try:
        index = resolve(index_path)
    except (KeyError, IndexError, TypeError, ValueError, FileNotFoundError):
        _display_error(manifest, None, "display index does not resolve")
    if not isinstance(index, dict) or not isinstance(index.get("artifacts"), list):
        _display_error(manifest, None, "display index is invalid")
    entries = {entry.get("layer_id"): entry for entry in index["artifacts"] if isinstance(entry, dict)}
    if set(entries) != {layer_id for layer_id, _ in declared} or len(entries) != len(index["artifacts"]):
        _display_error(manifest, None, "display index does not list exactly declared artifacts")
    expected_prefix = f"regions/{region_id}/display/"
    if any(not isinstance(entry.get("path"), str) or not entry["path"].startswith(expected_prefix) or
           entry["path"] == expected_prefix or ".." in Path(entry["path"]).parts or entry["path"].startswith("/")
           for entry in index["artifacts"] if isinstance(entry, dict)):
        _display_error(manifest, None, "display index contains a path outside the active region")
    status_layers = [layer for layer in manifest["layers"] if layer.get("status_ref") is not None]
    transport = index.get("transport")
    if not isinstance(transport, dict) or set(transport) != {layer["id"] for layer in status_layers}:
        _error("R65", manifest, None, "display transport keys differ from canonical status references")
    for layer in status_layers:
        reference = layer["status_ref"]
        try:
            canonical_record = _json_pointer(resolve(reference["path"]), reference.get("pointer", ""))
        except (KeyError, IndexError, TypeError, ValueError, FileNotFoundError):
            _error("R65", manifest, layer["id"], "canonical transport reference does not resolve")
        if not isinstance(canonical_record, dict) or _display_json_bytes(transport[layer["id"]]) != _display_json_bytes(canonical_record):
            _error("R65", manifest, layer["id"], "display transport differs from canonical record")
    for layer_id, declaration in declared:
        if layer_id != "coverage" and declaration.get("format") != "feature_collection":
            _display_error(manifest, layer_id, "display is allowed only on feature collections")
        display_ref = declaration["display"]
        display_path = display_ref.get("path") if isinstance(display_ref, dict) else None
        if (not isinstance(display_path, str) or not display_path.startswith(expected_prefix) or
                display_path == expected_prefix or ".." in Path(display_path).parts or display_path.startswith("/")):
            _display_error(manifest, layer_id, "display path is outside the region display directory")
        entry = entries.get(layer_id)
        if not isinstance(entry, dict) or entry.get("path") != display_path:
            _display_error(manifest, layer_id, "display index path does not match manifest")
        try:
            display_document = resolve(display_path)
        except (KeyError, IndexError, TypeError, ValueError, FileNotFoundError):
            _display_error(manifest, layer_id, "display file does not resolve")
        display_bytes = _resolved_bytes(resolve, display_path, display_document)
        if entry.get("bytes") != len(display_bytes) or entry.get("sha256") != hashlib.sha256(display_bytes).hexdigest():
            _display_error(manifest, layer_id, "display file hash or byte count differs from index")
        if entry.get("canonical_sha256") != hashlib.sha256(_resolved_bytes(resolve, declaration["path"], resolve(declaration["path"]))).hexdigest():
            _error("R64", manifest, layer_id, "canonical file hash differs from index")
        if layer_id == "coverage":
            if (display_document.get("type") != "FeatureCollection" or display_document.get("layer_id") != "coverage" or
                    len(display_document.get("features", [])) != 1):
                _error("R61", manifest, layer_id, "coverage display is not a single FeatureCollection feature")
            display_feature = display_document["features"][0]
            canonical_feature = _json_pointer(resolve(declaration["path"]), declaration.get("pointer", ""))
            expected_geometry, dropped = _display_transform_geometry(canonical_feature.get("geometry"))
            if display_feature.get("geometry") != expected_geometry or not _display_geometry_well_formed(display_feature.get("geometry")):
                _error("R63", manifest, layer_id, "coverage geometry is not rounded as declared")
            if display_feature.get("properties") != canonical_feature.get("properties"):
                _error("R63", manifest, layer_id, "coverage properties differ from canonical coverage")
            if entry.get("source_feature_count") != 1 or entry.get("dropped_degenerate_parts") != dropped:
                _error("R63", manifest, layer_id, "coverage display drop count or source count differs from canonical coverage")
            continue
        if display_document.get("type") != "FeatureCollection" or display_document.get("layer_id") != layer_id:
            _error("R61", manifest, layer_id, "display file is not the declared layer FeatureCollection")
        canonical_document = resolve(declaration["path"])
        canonical_features = _json_pointer(canonical_document, declaration.get("pointer", ""))["features"]
        display_features = display_document.get("features")
        display_select = (declaration.get("display") or {}).get("select")
        if declaration.get("kind") == "water" and display_select in {"streams", "bodies"}:
            if display_select == "streams":
                if (entry.get("feature_count") != len(display_features)
                        or entry.get("source_feature_count") != len(canonical_features)):
                    _error("R61", manifest, layer_id, "grouped display counts differ from canonical selection")
                table = display_document.get("evidence_table")
                if not isinstance(table, list):
                    _error("R62", manifest, layer_id, "grouped display evidence table is missing")
                restored = []
                for feature in display_features:
                    clone = copy.deepcopy(feature)
                    properties = clone.get("properties") or {}
                    index = properties.get("evidence")
                    if not isinstance(index, int) or isinstance(index, bool) or not 0 <= index < len(table):
                        _error("R62", manifest, layer_id, "group evidence reference is invalid")
                    properties["evidence"] = table[index]
                    restored.append(clone)
                validate_m4b_water_layer(manifest, declaration, canonical_features,
                                         restored, WATER_DISPLAY_CONFIG, water_review)
                continue
            validate_m4b_water_layer(manifest, declaration, canonical_features,
                                     display_features, WATER_DISPLAY_CONFIG, water_review)
        selected = canonical_features
        if declaration["kind"] == "water" and display_select == "bodies":
            decisions = select_water_features(canonical_features, WATER_DISPLAY_CONFIG,
                                              water_review or {"inclusions": [], "exclusions": []})
            selected = [row["feature"] for row in decisions
                        if row["eligible"] and (row["feature"].get("properties") or {}).get("source_layer") == "waterbody"]
        elif declaration["kind"] == "water" and any(
                {"kind", "source_layer"} & set(feature.get("properties") or {})
                for feature in canonical_features):
            selected = [feature for feature in canonical_features if _display_water(feature)]
        if entry.get("feature_count") != len(display_features) or len(display_features) != len(selected) or entry.get("source_feature_count") != len(canonical_features):
            _error("R61", manifest, layer_id, "display feature count differs from canonical selection")
        by_id = {feature.get("properties", {}).get("id"): feature for feature in display_features}
        canonical_by_id = {feature.get("properties", {}).get("id"): feature for feature in selected}
        if set(by_id) != set(canonical_by_id):
            _error("R61", manifest, layer_id, "display feature IDs differ from canonical selection")
        evidence_table = display_document.get("evidence_table")
        if not isinstance(evidence_table, list):
            _error("R62", manifest, layer_id, "display evidence table is missing")
        dropped_total = 0
        for ident, canonical_feature in canonical_by_id.items():
            display_feature = by_id[ident]
            canonical_geometry = canonical_feature.get("geometry")
            display_geometry = display_feature.get("geometry")
            if (display_geometry or {}).get("type") != (canonical_geometry or {}).get("type"):
                _error("R63", manifest, layer_id, "display geometry type differs from canonical geometry")
            try:
                expected_geometry, dropped = _display_transform_geometry(canonical_geometry)
            except (TypeError, ValueError, KeyError, IndexError):
                _error("R63", manifest, layer_id, "canonical geometry cannot be transformed")
            if display_geometry != expected_geometry:
                _error("R63", manifest, layer_id, "display coordinates differ from canonical rounding")
            if display_geometry is not None and not _display_geometry_well_formed(display_geometry):
                _error("R63", manifest, layer_id, "display geometry is empty or structurally invalid")
            if canonical_geometry is not None and expected_geometry is None:
                _error("R63", manifest, layer_id, "display geometry dropped an entire feature")
            dropped_total += dropped
            properties = display_feature.get("properties", {})
            evidence_index = properties.get("evidence")
            if not isinstance(evidence_index, int) or isinstance(evidence_index, bool) or not 0 <= evidence_index < len(evidence_table):
                _error("R62", manifest, layer_id, "display evidence reference is invalid")
            restored = copy.deepcopy(properties)
            restored["evidence"] = evidence_table[evidence_index]
            canonical_properties = canonical_feature.get("properties", {})
            expected_properties = canonical_properties
            if declaration["kind"] == "water":
                display_fields = {"id", "name", "kind", "source_layer", "evidence"}
                expected_properties = {key: value for key, value in canonical_properties.items()
                                       if key in display_fields}
            if _display_json_bytes(restored) != _display_json_bytes(expected_properties):
                _error("R62", manifest, layer_id, "display evidence or properties differ from canonical feature")
        if entry.get("dropped_degenerate_parts") != dropped_total:
            _error("R63", manifest, layer_id, "display drop count differs from canonical rounding")


def normalize_transport(record):
    """Return canonical transport fields and the legacy aliases observed."""
    if not isinstance(record, dict):
        return record, []
    result = dict(record)
    legacy = []
    if "completed_at" in result:
        legacy.append("completed_at")
        result.setdefault("last_retrieved_at", result["completed_at"])
        result.setdefault("last_checked_at", result["completed_at"])
    if "retrieved_at" in result:
        legacy.append("retrieved_at")
        result.setdefault("last_retrieved_at", result["retrieved_at"])
    if "checked_at" in result:
        legacy.append("checked_at")
        result.setdefault("last_checked_at", result["checked_at"])
    if result.get("status") == "failed":
        legacy.append("failed")
        result["status"] = "unavailable"
    if "error" in result:
        legacy.append("error")
        result.setdefault("reason", result["error"])
    if result.get("status") == "available" and "last_retrieved_at" not in result and result.get("last_checked_at"):
        legacy.append("inferred_retrieval")
        result["last_retrieved_at"] = result["last_checked_at"]
    if "last_confirmed_at" in result:
        legacy.append("last_confirmed_at")
    if "last_checked_at" not in result and result.get("last_retrieved_at"):
        result["last_checked_at"] = result["last_retrieved_at"]
    return result, legacy


def _parse_timestamp(value, allow_date=False):
    if not isinstance(value, str):
        return None
    if allow_date and re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        try:
            return datetime.strptime(value, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        except ValueError:
            return None
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z", value):
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)
    except ValueError:
        return None


def _source_ids(manifest, layer):
    return [manifest["sources"][source_id] for source_id in layer["source_ids"]]


def _geometry_bounds(geometry):
    parsed = shape(geometry)
    if parsed.is_empty or not parsed.is_valid:
        raise ValueError("empty or invalid geometry")
    west, south, east, north = parsed.bounds
    if not (-180 <= west <= east <= 180 and -90 <= south <= north <= 90):
        raise ValueError("geometry outside WGS84 range")
    return parsed, (west, south, east, north)


def _check_evidence(manifest, layer, feature):
    props = feature.get("properties", {})
    evidence = props.get("evidence")
    if not isinstance(evidence, dict):
        _error("R23", manifest, layer["id"], "evidence is required")
    url = evidence.get("source_url")
    parsed = urlparse(url or "")
    if parsed.scheme not in {"http", "https"} or not parsed.netloc or not evidence.get("agency") or not _parse_timestamp(evidence.get("retrieved_at")):
        _error("R23", manifest, layer["id"], "invalid evidence provenance")
    if "verification_method" not in evidence or (evidence["verification_method"] is not None and evidence["verification_method"] not in APPROVED_VERIFICATION_METHODS):
        _error("R23", manifest, layer["id"], "verification_method is missing or not approved")
    if evidence.get("last_verified") is not None and evidence.get("verification_method") != "manual_claim_review":
        _error("R25", manifest, layer["id"], "last_verified requires manual_claim_review")
    sources = _source_ids(manifest, layer)
    if all(source["type"] in {"agency", "derived"} for source in sources):
        allowed = [declared for source in sources for declared in source["source_urls"]]
        if not any(url == base or url.startswith(base + "/") or url.startswith(base + "?") for base in allowed):
            _error("R24", manifest, layer["id"], f"undeclared evidence source {url}")


def _check_reserved(manifest, layer, feature):
    props = feature.get("properties", {})
    fields = layer.get("fields", {"source": [], "derived": []})
    declared = set(fields.get("source", [])) | set(fields.get("derived", []))
    if RESERVED_PROPERTIES & declared:
        _error("R26", manifest, layer["id"], "reserved property listed in fields")
    if set(props) - RESERVED_PROPERTIES - declared:
        _error("R26", manifest, layer["id"], f"undeclared properties: {sorted(set(props) - RESERVED_PROPERTIES - declared)}")
    if not isinstance(props.get("id"), str) or not props["id"]:
        _error("R21", manifest, layer["id"], "feature id must be non-empty")
    if "name" in props and props["name"] is not None and not isinstance(props["name"], str):
        _error("R27", manifest, layer["id"], "name must be a string or null")
    if "needs_review" in props and not isinstance(props["needs_review"], bool):
        _error("R27", manifest, layer["id"], "needs_review must be boolean")
    if "access_reason" in props and not isinstance(props["access_reason"], str):
        _error("R27", manifest, layer["id"], "access_reason must be a string")
    if "actual_site_confirmed" in props:
        if not isinstance(props["actual_site_confirmed"], bool):
            _error("R27", manifest, layer["id"], "actual_site_confirmed must be boolean")
        if props["actual_site_confirmed"] is True and layer["kind"] != "reviewed_sites":
            _error("R27", manifest, layer["id"], "actual_site_confirmed is reserved for reviewed sites")
    if "evaluated_trip" in props:
        trip = props["evaluated_trip"]
        if not isinstance(trip, dict) or not {"arrive", "depart", "vehicle"} <= set(trip):
            _error("R27", manifest, layer["id"], "evaluated_trip requires arrive, depart and vehicle")
    if "camping_permission" in props and props["camping_permission"] != "unknown":
        if not (layer["kind"] == "reviewed_sites" and props["camping_permission"] == "supported_for_trip" and props.get("needs_review") is False and props.get("evaluated_trip") and props.get("evidence", {}).get("verification_method") == "manual_claim_review"):
            _error("R27", manifest, layer["id"], "positive camping permission is not supported")
    if props.get("access_status") not in {None, "unknown", "restricted", "designated_open"}:
        _error("R27", manifest, layer["id"], "invalid access_status")
    if props.get("access_status") not in {None, "unknown"} and (not props.get("evaluated_trip") or "access_reason" not in props or props.get("road_conditions") != "unknown"):
        _error("R27", manifest, layer["id"], "positive access_status needs a trip, reason and unknown road_conditions")
    if props.get("road_conditions") not in {None, "unknown"} or props.get("land_class") not in {None, "unknown"}:
        _error("R27", manifest, layer["id"], "road_conditions and land_class must remain unknown")


def _check_kind(manifest, layer, feature):
    props = feature["properties"]
    kind = layer["kind"]
    if kind == "research_areas" and (props.get("needs_review") is not True or props.get("camping_permission") != "unknown" or props.get("actual_site_confirmed") is not False or not props.get("evaluated_trip")):
        _error("R28", manifest, layer["id"], "research areas must fail closed")
    if kind == "community_leads" and (props.get("needs_review") is not True or props.get("camping_permission") != "unknown" or props.get("evidence", {}).get("verification_method") is not None or props.get("evidence", {}).get("last_verified") is not None):
        _error("R28", manifest, layer["id"], "community leads must remain unverified")
    if kind == "restriction_monitor":
        status = props.get("status")
        if props.get("needs_review") is not True or status not in {"unknown", "confirmed"}:
            _error("R28", manifest, layer["id"], "restriction monitor is not fail-closed")
        if status == "unknown" and (props.get("stage") is not None or props.get("last_confirmed_at") is not None):
            _error("R28", manifest, layer["id"], "unknown monitor cannot carry a confirmation")
        if status == "confirmed" and (not props.get("last_confirmed_at") or not isinstance(props.get("max_age_hours"), (int, float)) or props["max_age_hours"] <= 0 or props.get("evidence", {}).get("verification_method") != "manual_claim_review"):
            _error("R28", manifest, layer["id"], "confirmed monitor lacks reviewed evidence")
    if kind == "land_management":
        field = layer.get("classification_source_field")
        value = props.get(field)
        if not isinstance(value, str) or not value:
            _error("R28", manifest, layer["id"], "classification source field is empty")
        if any(isinstance(v, str) and v.lower() == "private" for key, v in props.items() if key != field) and value.upper() != "PVT":
            _error("R28", manifest, layer["id"], "private classification conflicts with source code")


def _check_claim(claim):
    if not isinstance(claim, dict) or claim.get("status") not in {"unknown", "supported", "restricted"}:
        return False
    if claim["status"] == "unknown":
        return True
    return (isinstance(claim.get("source_url"), str) and urlparse(claim["source_url"]).scheme in {"http", "https"}
            and bool(claim.get("scope")) and claim.get("basis") in {"manual_review", "validated_structured_field"}
            and _parse_timestamp(claim.get("last_confirmed_at")) and isinstance(claim.get("max_age_hours"), (int, float)) and claim["max_age_hours"] > 0)


def _check_rules(manifest, resolve):
    rules_ref = manifest.get("rules")
    if not rules_ref:
        return
    try:
        registry = _json_pointer(resolve(rules_ref["path"]), rules_ref.get("pointer", ""))
    except (KeyError, IndexError, TypeError, ValueError):
        _error("R50", manifest, None, "rules registry does not resolve")
    if not isinstance(registry, dict) or not isinstance(registry.get("rules"), list):
        _error("R50", manifest, None, "rules registry is invalid")
    place_ids = set()
    ridb_ids = set()
    for layer in manifest["layers"]:
        if layer["format"] != "place_list":
            continue
        try:
            document = resolve(layer["path"])
            places = _json_pointer(document, layer.get("pointer", "")).get(layer["list_key"], [])
        except (KeyError, IndexError, TypeError, ValueError):
            _error("R50", manifest, layer["id"], "place list does not resolve")
        for place in places:
            if isinstance(place, dict):
                if isinstance(place.get("id"), str):
                    place_ids.add(place["id"])
                if place.get("ridb_facility_id") is not None:
                    ridb_ids.add(str(place["ridb_facility_id"]))
    for rule in registry["rules"]:
        if not isinstance(rule, dict) or not isinstance(rule.get("id"), str) or not rule["id"] or not rule.get("scope") or urlparse(rule.get("source_url", "")).scheme not in {"http", "https"} or not _parse_timestamp(rule.get("last_confirmed_at")) or not isinstance(rule.get("max_age_hours"), (int, float)) or rule["max_age_hours"] <= 0 or rule.get("camping_permission") != "unknown":
            _error("R50", manifest, None, "invalid rule record")
        for place_id in rule.get("place_ids", []):
            if place_id not in place_ids and not (place_id.startswith("ridb-") and place_id[5:] in ridb_ids):
                _error("R50", manifest, None, f"rule references unknown place {place_id}")


def _validate_layer(manifest, layer, resolve, coverage_bounds, ids, report):
    layer_id = layer["id"]
    try:
        document = resolve(layer["path"])
    except (KeyError, IndexError, TypeError, ValueError, FileNotFoundError):
        _error("R03", manifest, layer_id, "path does not resolve")
    try:
        value = _json_pointer(document, layer["pointer"])
    except (KeyError, IndexError, TypeError, ValueError):
        _error("R40" if layer["format"] == "place_list" else "R20", manifest, layer_id, "layer pointer does not resolve")
    item_count = 0
    if layer["format"] == "place_list":
        places = value.get(layer["list_key"]) if isinstance(value, dict) else None
        if not isinstance(places, list):
            _error("R40", manifest, layer_id, "place list is missing")
        seen = set()
        for place in places:
            if not isinstance(place, dict):
                _error("R40", manifest, layer_id, "place must be an object")
            ident = place.get("id")
            if not isinstance(ident, str) or not re.fullmatch(r"[a-z0-9_-]+", ident) or ident in seen:
                _error("R40", manifest, layer_id, "invalid or duplicate place id")
            seen.add(ident)
            coords = place.get("coordinates")
            if not isinstance(coords, list) or len(coords) != 2 or not all(isinstance(n, (int, float)) and not isinstance(n, bool) and math.isfinite(n) for n in coords) or not (-180 <= coords[0] <= 180 and -90 <= coords[1] <= 90):
                _error("R40", manifest, layer_id, "invalid coordinates")
            if place.get("camping_permission") not in {None, "unknown"}:
                _error("R41", manifest, layer_id, "place-list camping permission must be unknown")
            facts = place.get("facts")
            if facts is not None and (not isinstance(facts, dict) or any(not _check_claim(claim) for claim in facts.values())):
                _error("R41", manifest, layer_id, "invalid place-list claim")
        item_count = len(places)
    else:
        if not isinstance(value, dict) or value.get("type") != "FeatureCollection" or not isinstance(value.get("features"), list):
            _error("R20", manifest, layer_id, "not a FeatureCollection")
        if layer.get("must_be_empty") and value["features"]:
            _error("R28", manifest, layer_id, "must_be_empty layer contains features")
        item_count = len(value["features"])
        padding = layer.get("extent_padding_deg", 0) + 1e-6
        west, south, east, north = coverage_bounds
        for feature in value["features"]:
            props = feature.get("properties", {})
            ident = props.get("id")
            if ident in ids:
                _error("R21", manifest, layer_id, f"duplicate feature id {ident}")
            ids.add(ident)
            geometry = feature.get("geometry")
            if geometry is None:
                if not layer.get("allow_null_geometry"):
                    _error("R22", manifest, layer_id, "null geometry is not allowed")
            else:
                try:
                    parsed, bounds = _geometry_bounds(geometry)
                except (TypeError, ValueError, KeyError) as exc:
                    _error("R22", manifest, layer_id, str(exc))
                if not layer.get("geometry_types") or geometry.get("type") not in layer["geometry_types"]:
                    _error("R22", manifest, layer_id, "undeclared geometry type")
                if bounds[0] < west - padding or bounds[1] < south - padding or bounds[2] > east + padding or bounds[3] > north + padding:
                    _error("R22", manifest, layer_id, "geometry outside coverage")
            _check_evidence(manifest, layer, feature)
            _check_reserved(manifest, layer, feature)
            _check_kind(manifest, layer, feature)
            if layer["kind"] == "trails":
                activities = props.get("activities")
                expected = set(ACTIVITIES)
                if set(activities or {}) != expected or any(set(record or {}) != {"managed", "accpt", "disc", "restricted"} or any(v is not None and not isinstance(v, str) for v in (record or {}).values()) for record in (activities or {}).values()):
                    _error("R29", manifest, layer_id, "trail activity records do not match producer")
    report["layers"][layer_id] = item_count
    status_ref = layer.get("status_ref")
    if status_ref is None:
        if any(source["type"] != "curated" for source in _source_ids(manifest, layer)):
            report["unrecorded_status_layers"].append(layer_id)
        return
    try:
        status_doc = resolve(status_ref["path"])
        status = _json_pointer(status_doc, status_ref.get("pointer", ""))
    except (KeyError, IndexError, TypeError, ValueError):
        _error("R30", manifest, layer_id, "status reference does not resolve")
    if not isinstance(status, dict):
        _error("R30", manifest, layer_id, "transport record must be an object")
    normalized, legacy = normalize_transport(status)
    if normalized.get("status") not in TRANSPORT_STATUSES:
        _error("R30", manifest, layer_id, "invalid transport status")
    if normalized["status"] == "available" and not _parse_timestamp(normalized.get("last_retrieved_at")):
        _error("R30", manifest, layer_id, "available transport needs retrieval timestamp")
    if normalized["status"] in {"unavailable", "skipped"} and not normalized.get("reason"):
        _error("R30", manifest, layer_id, "unavailable transport needs reason")
    if "count" in normalized and normalized["count"] != item_count:
        _error("R32", manifest, layer_id, "transport count does not match features")
    if normalized["status"] != "available" and item_count and normalized.get("retained_previous") is not True:
        _error("R33", manifest, layer_id, "unavailable data must retain previous snapshot")
    if legacy:
        report["legacy_transport"][layer_id] = legacy


def validate_region_data(manifest, resolve):
    region_id = manifest.get("region", {}).get("id", "?")
    errors = sorted(Draft202012Validator(REGION_MANIFEST_SCHEMA, format_checker=FormatChecker()).iter_errors(manifest), key=lambda e: list(e.path))
    if errors:
        raise ContractError("R01", region_id, None, errors[0].message)
    if manifest["coverage"]["kind"] == "clipping_boundary" and not manifest["coverage"].get("source_id"):
        _error("R01", manifest, None, "clipping boundary requires a source")
    if manifest["coverage"]["kind"] == "project_defined_extent" and manifest["coverage"].get("source_id") is not None:
        _error("R01", manifest, None, "project extent cannot have a source")
    if "ownership or access boundary" not in manifest["coverage"]["statement"]:
        _error("R01", manifest, None, "coverage statement must disclaim ownership and access")
    layer_ids = [layer["id"] for layer in manifest["layers"]]
    if len(layer_ids) != len(set(layer_ids)):
        _error("R04", manifest, None, "layer IDs are not unique")
    used_sources = set()
    for layer in manifest["layers"]:
        if not set(layer["source_ids"]) <= set(manifest["sources"]):
            _error("R04", manifest, layer["id"], "undeclared source")
        used_sources.update(layer["source_ids"])
        if layer["format"] == "feature_collection":
            if (not layer.get("geometry_types") and not layer.get("allow_null_geometry")) or "fields" not in layer or not layer.get("spatial_precision"):
                _error("R01", manifest, layer["id"], "feature collection geometry and fields declaration incomplete")
            if layer["kind"] == "land_management" and layer.get("classification_source_field") not in layer["fields"].get("source", []):
                _error("R01", manifest, layer["id"], "classification source field must be a source field")
            if layer["kind"] != "land_management" and "classification_source_field" in layer:
                _error("R01", manifest, layer["id"], "classification source field is only for land management")
        else:
            if not layer.get("list_key") or any(name in layer for name in ("geometry_types", "allow_null_geometry", "extent_padding_deg", "fields")):
                _error("R01", manifest, layer["id"], "place list shape is invalid")
    for source_id, source in manifest["sources"].items():
        if source["type"] in {"agency", "derived"} and not source["source_urls"]:
            _error("R01", manifest, None, f"source {source_id} requires a source URL")
    if manifest["coverage"].get("source_id"):
        used_sources.add(manifest["coverage"]["source_id"])
    if set(manifest["sources"]) != used_sources:
        _error("R04", manifest, None, "declared source is not used")
    if set(manifest["fact_coverage"]) != FACT_DIMENSIONS:
        _error("R01", manifest, None, "fact coverage must contain exactly eight dimensions")
    for fact in manifest["fact_coverage"].values():
        if fact["state"] == "context" and not fact["layer_ids"]:
            _error("R05", manifest, None, "context fact requires layer IDs")
        if fact["state"] == "reviewed_partial" and manifest.get("rules") is None:
            reviewed_layers = [layer for layer in manifest["layers"] if layer["kind"] == "reviewed_sites"]
            if not reviewed_layers:
                _error("R05", manifest, None, "reviewed_partial requires rules or reviewed sites")
            has_reviewed_feature = False
            for reviewed in reviewed_layers:
                try:
                    reviewed_doc = resolve(reviewed["path"])
                    reviewed_value = _json_pointer(reviewed_doc, reviewed["pointer"])
                except (KeyError, IndexError, TypeError, ValueError):
                    _error("R20", manifest, reviewed["id"], "reviewed sites layer does not resolve")
                if not isinstance(reviewed_value, dict) or not isinstance(reviewed_value.get("features"), list):
                    _error("R20", manifest, reviewed["id"], "reviewed sites layer is not a FeatureCollection")
                has_reviewed_feature = has_reviewed_feature or bool(reviewed_value["features"])
            if not has_reviewed_feature:
                _error("R05", manifest, None, "reviewed_partial requires a reviewed site feature")
        if not set(fact["layer_ids"]) <= set(layer_ids):
            _error("R05", manifest, None, "fact references undeclared layer")
    try:
        coverage_doc = resolve(manifest["coverage"]["path"])
        coverage = _json_pointer(coverage_doc, manifest["coverage"]["pointer"])
        if coverage.get("type") != "Feature" or coverage.get("geometry") is None:
            raise ValueError("coverage is not a feature")
        coverage_shape, coverage_bounds = _geometry_bounds(coverage["geometry"])
        if coverage_shape.geom_type not in {"Polygon", "MultiPolygon"}:
            raise ValueError("coverage geometry must be Polygon or MultiPolygon")
    except (KeyError, IndexError, TypeError, ValueError) as exc:
        _error("R10", manifest, None, str(exc))
    _validate_display(manifest, resolve, coverage)
    _validate_water_contract(manifest, resolve)
    report = {"region": region_id, "layers": {}, "unrecorded_status_layers": [], "legacy_transport": {}}
    _check_rules(manifest, resolve)
    ids = set()
    for layer in manifest["layers"]:
        _validate_layer(manifest, layer, resolve, coverage_bounds, ids, report)
    report["unrecorded_status_layers"].sort()
    return report


def validate_region(manifest_path, v2_root=None):
    manifest_path = Path(manifest_path)
    v2_root = Path(v2_root) if v2_root is not None else ROOT.parent.parent
    manifest = json.loads(manifest_path.read_text())
    if manifest.get("region", {}).get("id") != manifest_path.parent.name:
        raise ContractError("R02", manifest.get("region", {}).get("id", "?"), None, "manifest ID does not match directory")
    paths = [manifest.get("coverage", {}).get("path")] + [layer.get("path") for layer in manifest.get("layers", [])]
    coverage_display = manifest.get("coverage", {}).get("display")
    if coverage_display:
        paths.append(coverage_display.get("path"))
    paths += [layer.get("display", {}).get("path") for layer in manifest.get("layers", []) if layer.get("display")]
    if manifest.get("coverage", {}).get("display") or any(layer.get("display") for layer in manifest.get("layers", [])):
        region_id = manifest.get("region", {}).get("id", "?")
        paths.append(f"regions/{region_id}/display/index.json")
    if manifest.get("rules"):
        paths.append(manifest["rules"].get("path"))
    for path in paths:
        if not isinstance(path, str) or path.startswith("/") or ".." in Path(path).parts:
            raise ContractError("R03", manifest.get("region", {}).get("id", "?"), None, f"invalid path {path}")
        target = (v2_root / path).resolve()
        if v2_root.resolve() not in target.parents and target != v2_root.resolve() or not target.is_file():
            raise ContractError("R03", manifest.get("region", {}).get("id", "?"), None, f"missing path {path}")
    status_paths = [layer["status_ref"]["path"] for layer in manifest.get("layers", []) if layer.get("status_ref")]
    for path in status_paths:
        if not isinstance(path, str) or path.startswith("/") or ".." in Path(path).parts:
            raise ContractError("R03", manifest.get("region", {}).get("id", "?"), None, f"invalid status path {path}")
        target = (v2_root / path).resolve()
        if v2_root.resolve() not in target.parents and target != v2_root.resolve() or not target.is_file():
            raise ContractError("R03", manifest.get("region", {}).get("id", "?"), None, f"missing status path {path}")
    cache = {}
    raw_bytes = {}
    def resolve(path):
        if path not in cache:
            source = v2_root / path
            raw_bytes[path] = source.read_bytes()
            cache[path] = json.loads(raw_bytes[path])
        return cache[path]
    resolve.raw_bytes = raw_bytes
    return validate_region_data(manifest, resolve)
