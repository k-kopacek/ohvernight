"""Pure validation for the regional data contract.

The manifest is a hand-reviewed declaration. This module checks that declaration,
the files it points to, and the evidence semantics without reading the clock.
"""
from __future__ import annotations

import json
import math
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

from jsonschema import Draft202012Validator, FormatChecker
from shapely.geometry import shape

from lib.common import ROOT
from fetch_trails import ACTIVITIES

REGION_MANIFEST_SCHEMA = json.loads((ROOT / "schema/region-manifest.schema.json").read_text())

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
            reviewed = [layer for layer in manifest["layers"] if layer["id"] in fact["layer_ids"] and layer["kind"] == "reviewed_sites"]
            if not reviewed:
                _error("R05", manifest, None, "reviewed_partial requires rules or reviewed sites")
            try:
                reviewed_doc = resolve(reviewed[0]["path"])
                reviewed_value = _json_pointer(reviewed_doc, reviewed[0]["pointer"])
                if not isinstance(reviewed_value, dict) or not reviewed_value.get("features"):
                    _error("R05", manifest, None, "reviewed_partial requires a reviewed site feature")
            except (KeyError, IndexError, TypeError, ValueError):
                _error("R20", manifest, reviewed[0]["id"], "reviewed sites layer does not resolve")
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
    def resolve(path):
        if path not in cache:
            cache[path] = json.loads((v2_root / path).read_text())
        return cache[path]
    return validate_region_data(manifest, resolve)
