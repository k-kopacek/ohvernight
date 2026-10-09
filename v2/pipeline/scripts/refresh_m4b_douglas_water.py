"""Run the single authorized M4-B Douglas padded NHD refresh into staging."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import requests
from requests.adapters import HTTPAdapter

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
OBJECTID_RAW_ROOT = ROOT / "data/raw/m4b-douglas-water-objectid"
RAW_ROOT = ROOT / "data/raw/m4b-douglas-water-tiled"
STAGING = ROOT / "data/processed/m4b-douglas-water-tiled"
PAD_DEG = 0.005
COUNT_ID_TIMEOUT = 180
DISCOVERY_CAP = 150
MAX_TILE_DEPTH = 2
PAGE_RETRY_POLICY = {"version": 1, "max_attempts": 4, "min_retry_seconds": 900}
PADDING_ARTIFACT_MAX_AREA_M2 = 1e-6
PADDING_ARTIFACT_MAX_DISTANCE_M = 1e-6


def write_json(path: Path, value, *, indent=None):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False,
                               separators=None if indent else (",", ":"),
                               indent=indent, allow_nan=False) + "\n", encoding="utf-8")
    temporary.replace(path)


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


def _padding_artifact_within_limits(area_m2, maximum_distance_m):
    return (math.isfinite(area_m2) and math.isfinite(maximum_distance_m)
            and 0 <= area_m2 <= PADDING_ARTIFACT_MAX_AREA_M2
            and 0 <= maximum_distance_m <= PADDING_ARTIFACT_MAX_DISTANCE_M)


def _padding_residual_metrics(outside, padded):
    """Measure the native residual in local equirectangular metres.

    This affine projection preserves the source's straight geographic edges;
    projecting only vertices into a curved projection would change the clip.
    """
    from pyproj import Transformer
    from shapely import make_valid
    from shapely.ops import transform

    centre = padded.centroid
    local_crs = (f"+proj=eqc +lat_ts={centre.y} +lat_0={centre.y} "
                 f"+lon_0={centre.x} +datum=WGS84 +units=m +no_defs")
    project = Transformer.from_crs(4326, local_crs, always_xy=True).transform
    projected = transform(project, outside)
    area_m2 = projected.area
    residual = make_valid(projected)
    boundary = transform(project, padded)
    if residual.is_empty or boundary.covers(residual):
        return area_m2, 0.0
    # Containment of the entire residual, not just its vertices, bounds its
    # directed distance to the padded polygon. Polygonal buffers give a
    # conservative upper bound; they do not change the acceptance limit.
    low, high = 0.0, PADDING_ARTIFACT_MAX_DISTANCE_M
    while not boundary.buffer(high, quad_segs=256).covers(residual):
        high *= 2
        if not math.isfinite(high):
            raise ValueError("cannot measure padding residual distance")
    for _ in range(40):
        middle = (low + high) / 2
        if boundary.buffer(middle, quad_segs=256).covers(residual):
            high = middle
        else:
            low = middle
    return area_m2, high


def _existing_feature_within_padding(geometry, padded):
    outside = geometry.difference(padded)
    if outside.is_empty:
        return True
    return _padding_artifact_within_limits(*_padding_residual_metrics(outside, padded))


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
        if not bg.equals(ag):
            # Independent clips can interpolate county-edge points differently
            # from direct old/new subtraction. Test the approved invariant
            # County reclip stays exact; only padded containment has the
            # owner-approved absolute metric allowance for clip residuals.
            within_padding = _existing_feature_within_padding(ag, padded)
            county_part_unchanged = bg.equals(ag.intersection(county))
            if within_padding and county_part_unchanged:
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


class ExternalBlocked(RuntimeError):
    """The authorized transport cannot establish complete spatial coverage."""


class ServiceFailure(RuntimeError):
    """A timeout or server failure eligible for the bounded service policy."""


class TileOverflow(RuntimeError):
    """A transfer-limited ID response must be subdivided, never accepted."""


class ResumeLater(RuntimeError):
    """One saved record page may resume after the fixed 15 minute interval."""


def prepare_session(*, resume_blocked=False, now=time.time):
    """Consume the one explicit authorization before changing discovery state."""
    path = RAW_ROOT / "session.json"
    if (STAGING / "refresh-report.json").exists():
        raise RuntimeError("staging report already exists; refusing to overwrite a completed session")
    session = json.loads(path.read_text()) if path.exists() else None
    if resume_blocked:
        if session and session.get("resume_number", 0):
            raise RuntimeError("the one blocked-snapshot resume has already been consumed")
        if not session or not session.get("blocked"):
            raise RuntimeError("--resume-blocked requires a previously blocked tiled snapshot")
        states = [json.loads(p.read_text()) for p in RAW_ROOT.glob("layer-*-tiles.json")]
        if not any(state.get("blocked") for state in states):
            raise RuntimeError("blocked snapshot has no externally blocked tile state")
        session.update(resume_number=1,
                       resume_started_at_utc=datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
                       original_blocked=session.pop("blocked"))
        write_json(path, session, indent=2)
    elif session and session.get("blocked"):
        legacy_page_block = False
        for plan_path in sorted(RAW_ROOT.glob("douglas-co-*-plan.json")):
            plan = json.loads(plan_path.read_text())
            for number in plan.get("failed_pages", {}):
                if session["blocked"] == f"layer {plan['layer_id']} page {number} failed twice":
                    legacy_page_block = True
        if not legacy_page_block:
            raise ExternalBlocked(session["blocked"])
        migrate_page_policy_session(session, path, now())
        if session.get("blocked"):
            raise ExternalBlocked(session["blocked"])
    elif session is None:
        session = {"retrieved_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")}
        write_json(path, session, indent=2)

    # Replayable activation after the authorization record is durable. A crash
    # here can continue without consuming a second resume or resetting its tries.
    if session.get("resume_number") == 1:
        for state_path in sorted(RAW_ROOT.glob("layer-*-tiles.json")):
            state = json.loads(state_path.read_text())
            if state.get("resume_number") == 1:
                continue
            state.update(resume_number=1, original_blocked=state.pop("blocked", None),
                         original_unresolved_tiles=state.pop("unresolved_tiles", []))
            for tile in state["tiles"].values():
                if tile["status"] == "complete":
                    tile["completed_in"] = "original"
            write_json(state_path, state, indent=2)
    migrate_page_policy_session(session, path, now())
    return session


def split_tiles(extent, parent=None):
    """Compute shared edges once; SW, SE, NW, NE are numbered 0 through 3."""
    west, south, east, north = extent
    xs = (west, (west + east) / 2, east)
    ys = (south, (south + north) / 2, north)
    return [{"id": f"{parent}.{index}" if parent is not None else str(index),
             "extent": [xs[x], ys[y], xs[x + 1], ys[y + 1]]}
            for index, (x, y) in enumerate(((0, 0), (1, 0), (0, 1), (1, 1)))]


class SavedTransport:
    """One HTTP request per call, paced and persisted before interpretation.

    Neither requests' adapter nor ArcGIS get_json may retry behind this ledger.
    Injected clock/sleep/client allow all policy tests to remain network-free.
    """
    def __init__(self, client, root, *, now=time.time, sleep=time.sleep, resume_number=0):
        self.client, self.root = client, Path(root)
        self.resume_number = resume_number
        self.now, self.sleep = now, sleep
        self.ledger_path = self.root / "request-ledger.json"
        self.ledger = (json.loads(self.ledger_path.read_text()) if self.ledger_path.exists()
                       else {"last_finished": 0, "discovery_requests": {}})

    def pause_until(self, deadline):
        while self.now() < deadline:
            self.sleep(min(60, deadline - self.now()))

    def request(self, path, url, params, timeout, *, context=None, layer=None):
        path = Path(path)
        if path.exists():
            record = json.loads(path.read_text())
            if (record["url"], record["params"], record["timeout"]) != (url, params, timeout):
                raise RuntimeError(f"saved request parameters changed: {path}")
        else:
            if layer is not None:
                counts = self.ledger["discovery_requests"]
                if counts.get(str(layer), 0) >= DISCOVERY_CAP:
                    raise ExternalBlocked(f"layer {layer} reached {DISCOVERY_CAP} discovery requests")
                counts[str(layer)] = counts.get(str(layer), 0) + 1
            self.pause_until(self.ledger["last_finished"] + 2)
            record = {"url": url, "params": params, "timeout": timeout,
                      "timestamp_utc": datetime.fromtimestamp(self.now(), timezone.utc).isoformat(),
                      "context": context, "outcome": "interrupted", "finished_epoch": self.now()}
            # An interrupted request counts and is never silently issued again.
            write_json(path, record, indent=2)
            self.ledger["last_finished"] = self.now()
            write_json(self.ledger_path, self.ledger, indent=2)
            try:
                response = self.client.get(url, params=params, timeout=timeout, allow_redirects=False)
                record.update(status_code=response.status_code, response_text=response.text,
                              outcome="received")
                if context and "page" in context:
                    try:
                        _request_payload(record, path)
                    except ServiceFailure as error:
                        record.update(outcome="service_failure", error=str(error))
            except (requests.Timeout, requests.ConnectionError) as error:
                record.update(outcome="service_failure", error=str(error))
            except requests.RequestException as error:
                record.update(outcome="fatal", error=str(error))
            finally:
                record["finished_epoch"] = self.now()
                write_json(path, record, indent=2)
                self.ledger["last_finished"] = self.now()
                write_json(self.ledger_path, self.ledger, indent=2)
        return _request_payload(record, path)


def _request_payload(record, path):
    if record["outcome"] in {"interrupted", "service_failure"}:
        raise ServiceFailure(record.get("error", "request interrupted; response unknown"))
    if record["outcome"] == "fatal":
        raise RuntimeError(record["error"])
    status = record["status_code"]
    if 500 <= status <= 599:
        raise ServiceFailure(f"HTTP {status}")
    if not 200 <= status < 300:
        raise RuntimeError(f"HTTP {status}: {record['url']}")
    try:
        value = json.loads(record["response_text"])
    except ValueError as error:
        raise RuntimeError(f"invalid JSON: {path}") from error
    if not isinstance(value, dict):
        raise RuntimeError(f"response is not an object: {path}")
    if "error" in value:
        code = value["error"].get("code") if isinstance(value["error"], dict) else None
        if isinstance(code, int) and 500 <= code <= 599:
            raise ServiceFailure(f"ArcGIS {value['error']}")
        raise RuntimeError(f"ArcGIS {value['error']}")
    return value


def _spatial(extent):
    return {"where": "1=1", "geometry": ",".join(map(str, extent)),
            "geometryType": "esriGeometryEnvelope", "inSR": 4326,
            "spatialRel": "esriSpatialRelIntersects"}


def _validated_ids(payload, count):
    ids = payload.get("objectIds")
    if ids is None and count == 0 and "objectIds" in payload:
        ids = []
    if payload.get("exceededTransferLimit"):
        raise TileOverflow("truncated tile ID response")
    if not isinstance(ids, list) or any(type(ident) is not int for ident in ids):
        raise RuntimeError("tile has no valid object ID list")
    if len(ids) != len(set(ids)):
        raise RuntimeError("duplicate IDs within one tile")
    if type(count) is not int or count < 0:
        raise RuntimeError("tile count is not a non-negative integer")
    if count != len(ids):
        raise TileOverflow("tile count and complete ID set disagree")
    return sorted(ids)


def discover_tiles(transport, layer_id, extent, info, *, tile_order=None):
    """Persist each attempt; union only complete leaves, independent of order."""
    root = transport.root
    state_path = root / f"layer-{layer_id}-tiles.json"
    expected = {"layer_id": layer_id, "extent": list(extent), "max_depth": MAX_TILE_DEPTH,
                "request_cap": DISCOVERY_CAP}
    if state_path.exists():
        state = json.loads(state_path.read_text())
        if any(state.get(key) != value for key, value in expected.items()):
            raise RuntimeError("saved tile discovery plan changed")
        if state.get("blocked"):
            raise ExternalBlocked(state["blocked"])
    else:
        state = {**expected, "resume_number": transport.resume_number,
                 "tiles": {tile["id"]: {**tile, "depth": 0, "status": "pending",
                                                  "attempts": []}
                                     for tile in split_tiles(extent)}}
        write_json(state_path, state, indent=2)
    base = f"{SERVICE}/{layer_id}/query"
    resume = transport.resume_number
    prefix = f"resume-{resume}-" if resume else ""
    attempts_key = "resume_attempts" if resume else "attempts"
    completed_in = f"resume-{resume}" if resume else "original"

    def visit(tile_id):
        tile = state["tiles"][tile_id]
        if tile["status"] == "complete":
            return
        if tile["status"] == "subdivided":
            for child in tile["children"]:
                visit(child)
            return
        attempts = tile.setdefault(attempts_key, [])
        for number in range(1, 3):
            attempt_path = root / f"layer-{layer_id}-tiles" / tile_id / f"{prefix}attempt-{number}.json"
            if attempt_path.exists():
                attempt = json.loads(attempt_path.read_text())
            else:
                previous = attempts or tile["attempts"]
                if previous:
                    transport.pause_until(previous[-1]["finished_epoch"] + 60)
                attempt = {"tile_id": tile_id, "envelope": tile["extent"], "attempt": number,
                           "timestamp_utc": datetime.fromtimestamp(transport.now(), timezone.utc).isoformat(),
                           "queries": [], "count": None, "object_ids": None, "outcome": "running"}
                if resume:
                    attempt["resume_number"] = resume
                write_json(attempt_path, attempt, indent=2)
            if attempt["outcome"] == "complete":
                tile.update(status="complete", object_ids=attempt["object_ids"], count=attempt["count"],
                            completed_in=completed_in)
                break
            if attempt["outcome"] in {"service_failure", "overflow"}:
                if len(attempts) < number:
                    attempts.append(attempt)
                continue
            if attempt["outcome"] in {"fatal", "externally_blocked"}:
                raise RuntimeError(f"tile {tile_id} has stopped: {attempt['error']}")
            try:
                responses = {}
                for kind, flag in (("count", "returnCountOnly"), ("ids", "returnIdsOnly")):
                    params = {**_spatial(tile["extent"]), "f": "json", flag: "true"}
                    if params not in attempt["queries"]:
                        attempt["queries"].append(params)
                    write_json(attempt_path, attempt, indent=2)
                    responses[kind] = transport.request(
                        attempt_path.with_name(f"{prefix}attempt-{number}-{kind}.json"), base, params,
                        COUNT_ID_TIMEOUT, context={"tile_id": tile_id, "envelope": tile["extent"],
                                                   "attempt": number, "phase": kind,
                                                   "resume_number": resume}, layer=layer_id)
                    if kind == "count":
                        attempt["count"] = responses[kind].get("count")
                        if responses[kind].get("exceededTransferLimit"):
                            raise TileOverflow("truncated tile count response")
                    else:
                        attempt["object_ids"] = responses[kind].get("objectIds")
                    write_json(attempt_path, attempt, indent=2)
                attempt["count"] = responses["count"].get("count")
                attempt["object_ids"] = responses["ids"].get("objectIds")
                # Save returned counts/IDs before validating or combining them.
                write_json(attempt_path, attempt, indent=2)
                ids = _validated_ids(responses["ids"], attempt["count"])
                attempt.update(outcome="complete", object_ids=ids)
                tile.update(status="complete", object_ids=ids, count=attempt["count"],
                            completed_in=completed_in)
            except (ServiceFailure, TileOverflow) as error:
                attempt.update(outcome="overflow" if isinstance(error, TileOverflow) else "service_failure",
                               error=str(error))
            except Exception as error:
                attempt.update(outcome="externally_blocked" if isinstance(error, ExternalBlocked) else "fatal",
                               error=str(error))
                raise
            finally:
                attempt["finished_epoch"] = transport.now()
                write_json(attempt_path, attempt, indent=2)
                if len(attempts) < number:
                    attempts.append(attempt)
                else:
                    attempts[number - 1] = attempt
                write_json(state_path, state, indent=2)
            if tile["status"] == "complete":
                break
        else:
            if tile["depth"] >= MAX_TILE_DEPTH:
                raise ExternalBlocked(f"layer {layer_id} level-2 tile {tile_id} failed twice")
            children = split_tiles(tile["extent"], tile_id)
            tile.update(status="subdivided", children=[child["id"] for child in children])
            for child in children:
                state["tiles"][child["id"]] = {**child, "depth": tile["depth"] + 1,
                                               "status": "pending", "attempts": []}
            write_json(state_path, state, indent=2)
            for child in tile["children"]:
                visit(child)

    try:
        initial = [tile["id"] for tile in split_tiles(extent)]
        for tile_id in (tile_order or initial):
            visit(tile_id)
        leaves = sorted((tile for tile in state["tiles"].values()
                         if tile["status"] != "subdivided"), key=lambda tile: tile["id"])
        if any(tile["status"] != "complete" for tile in leaves):
            raise RuntimeError("tile order did not cover the entire envelope")
        ids = sorted({ident for tile in leaves for ident in tile["object_ids"]})
        state.update(object_ids=ids, raw_leaf_id_count=sum(len(tile["object_ids"]) for tile in leaves),
                     duplicates_removed=sum(len(tile["object_ids"]) for tile in leaves) - len(ids),
                     coverage_complete=True)
        write_json(state_path, state, indent=2)
        return ids, state
    except ExternalBlocked as error:
        state.update(blocked=str(error), coverage_complete=False,
                     unresolved_tiles=[{"id": tile["id"], "envelope": tile["extent"]}
                                       for tile in state["tiles"].values()
                                       if tile["status"] not in {"complete", "subdivided"}])
        write_json(state_path, state, indent=2)
        raise


def _page_params(plan, number):
    start = (number - 1) * plan["page_size"]
    batch = plan["object_ids"][start:start + plan["page_size"]]
    return batch, {"f": "geojson", "objectIds": ",".join(map(str, batch)),
                   "outFields": f"{plan['out_fields']},{plan['object_id_field']}", "outSR": 4326,
                   "returnGeometry": "true", "returnZ": "false", "returnM": "false"}


def reconcile_page_policy(plan, plan_path, now):
    """Immutable request files, including interrupted ones, own attempt counts.

    Rebuild after every process start, so a crash before the plan write cannot
    drop a queue entry or reissue a spent request. Migration changes only the plan.
    """
    if plan.get("page_retry_policy") not in (None, PAGE_RETRY_POLICY):
        raise RuntimeError("saved page retry policy changed")
    if not plan.get("page_retry_policy"):
        plan["page_retry_policy"] = dict(PAGE_RETRY_POLICY)
        plan["page_policy_migrated_at_utc"] = datetime.fromtimestamp(now, timezone.utc).isoformat()
    pages_dir = plan_path.with_name(plan_path.name.replace("-plan.json", "-pages"))
    total = (len(plan["object_ids"]) + plan["page_size"] - 1) // plan["page_size"]
    old_failures = plan.get("failed_pages", {})
    old_states = plan.get("page_attempts", {})
    states, queue, complete = {}, {}, []
    for number in range(1, total + 1):
        batch, params = _page_params(plan, number)
        paths = sorted(pages_dir.glob(f"request-{number:04d}-*.json"),
                       key=lambda path: int(path.stem.rsplit("-", 1)[1]))
        attempts = [int(path.stem.rsplit("-", 1)[1]) for path in paths]
        if attempts != list(range(1, len(paths) + 1)) or len(paths) > PAGE_RETRY_POLICY["max_attempts"]:
            raise RuntimeError(f"page {number} has inconsistent immutable attempt files")
        entry = {"attempts": len(paths), "next_eligible_epoch": 0, "status": "pending"}
        for attempt, path in enumerate(paths, 1):
            record = json.loads(path.read_text())
            expected = (f"{SERVICE}/{plan['layer_id']}/query", params, 120, {"page": number, "attempt": attempt})
            if (record["url"], record["params"], record["timeout"], record["context"]) != expected:
                raise RuntimeError(f"saved request parameters changed: {path}")
            entry["last_finished_epoch"] = record["finished_epoch"]
            entry["next_eligible_epoch"] = record["finished_epoch"] + PAGE_RETRY_POLICY["min_retry_seconds"]
            try:
                page = _request_payload(record, path)
            except ServiceFailure as error:
                entry.update(status="queued", error=str(error))
            else:
                if not m4a._page_valid(page, batch, plan["object_id_field"]):
                    raise RuntimeError(f"layer {plan['layer_id']} page {number} did not return its complete ID set")
                entry.update(status="recoverable")
        page_path = pages_dir / f"page-{number:04d}.json"
        if page_path.exists():
            if not m4a._page_valid(json.loads(page_path.read_text()), batch, plan["object_id_field"]):
                raise RuntimeError(f"saved layer {plan['layer_id']} page {number} is incomplete")
            entry["status"] = "complete"
            complete.append(number)
        elif entry["status"] == "queued":
            # The old policy recorded failure at replay time, sometimes later
            # than the request finished (interrupted page 52). Never shorten it.
            old = old_failures.get(str(number), {})
            entry["next_eligible_epoch"] = max(entry["next_eligible_epoch"],
                old.get("finished_epoch", 0) + PAGE_RETRY_POLICY["min_retry_seconds"],
                old_states.get(str(number), {}).get("next_eligible_epoch", 0))
            if entry["attempts"] >= PAGE_RETRY_POLICY["max_attempts"]:
                entry["status"] = "exhausted"
            queue[str(number)] = dict(entry)
        states[str(number)] = entry
    plan.update(page_attempts=states, failed_pages=queue, completed_pages=complete)
    write_json(plan_path, plan, indent=2)
    return pages_dir


def migrate_page_policy_session(session, session_path, now):
    """Replayable activation; only obsolete page-failed-twice blocks lift."""
    migrated = []
    for plan_path in sorted(session_path.parent.glob("douglas-co-*-plan.json")):
        plan = json.loads(plan_path.read_text())
        reconcile_page_policy(plan, plan_path, now)
        migrated.append(plan)
    if "page_retry_policy" not in session:
        session.update(page_retry_policy=dict(PAGE_RETRY_POLICY),
                       page_policy_migrated_at_utc=datetime.fromtimestamp(now, timezone.utc).isoformat())
    elif session["page_retry_policy"] != PAGE_RETRY_POLICY:
        raise RuntimeError("saved session page retry policy changed")
    for plan in migrated:
        for number, entry in plan["page_attempts"].items():
            if (session.get("blocked") == f"layer {plan['layer_id']} page {number} failed twice"
                    and entry["attempts"] < PAGE_RETRY_POLICY["max_attempts"]):
                session["page_policy_original_blocked"] = session.pop("blocked")
    write_json(session_path, session, indent=2)


def retrieve_record_pages(transport, plan, plan_path):
    pages_dir = reconcile_page_policy(plan, plan_path, transport.now())
    features = {}
    config = water_display_config()

    def accept(number, page):
        batch, _ = _page_params(plan, number)
        if not m4a._page_valid(page, batch, plan["object_id_field"]):
            raise RuntimeError(f"layer {plan['layer_id']} page {number} did not return its complete ID set")
        for row in page["features"]:
            props = {str(key).lower(): value for key, value in row["properties"].items()}
            source_id = props.get("permanent_identifier")
            if not isinstance(source_id, str) or not source_id:
                raise RuntimeError("missing permanent_identifier")
            if source_id in features:
                raise RuntimeError(f"permanent_identifier conflict or record under two object IDs: {source_id}")
            ensure_supported_ftype(props.get("ftype"), config)
            features[source_id] = row
        page_path = pages_dir / f"page-{number:04d}.json"
        if not page_path.exists():
            write_json(page_path, page)
        plan["page_attempts"][str(number)]["status"] = "complete"
        plan["failed_pages"].pop(str(number), None)
        if number not in plan["completed_pages"]:
            plan["completed_pages"].append(number)
            plan["completed_pages"].sort()
        write_json(plan_path, plan, indent=2)

    # Read/validate all accepted pages before attempting incomplete ones.
    for key, entry in plan["page_attempts"].items():
        number = int(key)
        if entry["status"] == "complete":
            accept(number, json.loads((pages_dir / f"page-{number:04d}.json").read_text()))
        elif entry["status"] == "recoverable":
            _, params = _page_params(plan, number)
            attempt = entry["attempts"]
            page = transport.request(pages_dir / f"request-{number:04d}-{attempt}.json",
                f"{SERVICE}/{plan['layer_id']}/query", params, 120,
                context={"page": number, "attempt": attempt})
            accept(number, page)

    while True:
        pending = [int(key) for key, entry in plan["page_attempts"].items()
                   if entry["status"] not in {"complete", "exhausted"}]
        if not pending:
            break
        for number in pending:
            entry = plan["page_attempts"][str(number)]
            if transport.now() < entry["next_eligible_epoch"]:
                continue
            attempt = entry["attempts"] + 1
            _, params = _page_params(plan, number)
            path = pages_dir / f"request-{number:04d}-{attempt}.json"
            try:
                page = transport.request(path, f"{SERVICE}/{plan['layer_id']}/query", params, 120,
                                         context={"page": number, "attempt": attempt})
            except ServiceFailure as error:
                record = json.loads(path.read_text())
                entry.update(attempts=attempt, last_finished_epoch=record["finished_epoch"],
                             next_eligible_epoch=record["finished_epoch"] + PAGE_RETRY_POLICY["min_retry_seconds"],
                             error=str(error), status=("exhausted" if attempt >= PAGE_RETRY_POLICY["max_attempts"]
                                                      else "queued"))
                plan["failed_pages"][str(number)] = dict(entry)
                write_json(plan_path, plan, indent=2)
            else:
                record = json.loads(path.read_text())
                entry.update(attempts=attempt, last_finished_epoch=record["finished_epoch"])
                accept(number, page)
        pending = [entry for entry in plan["page_attempts"].values()
                   if entry["status"] not in {"complete", "exhausted"}]
        if pending:
            transport.pause_until(min(entry["next_eligible_epoch"] for entry in pending))
    exhausted = sorted(int(key) for key, entry in plan["page_attempts"].items() if entry["status"] == "exhausted")
    if exhausted:
        plan["exhausted_pages"] = exhausted
        write_json(plan_path, plan, indent=2)
        raise ExternalBlocked(f"layer {plan['layer_id']} record pages exhausted {PAGE_RETRY_POLICY['max_attempts']} attempts: {exhausted}")
    return features


def tiled_layer_query(transport, layer_name, layer_id, extent, out_fields):
    root = transport.root
    info = transport.request(root / f"layer-{layer_id}-metadata-response.json",
                             f"{SERVICE}/{layer_id}", {"f": "json"}, COUNT_ID_TIMEOUT)
    fields = info.get("fields") or []
    required = {"permanent_identifier", "ftype", "fcode"}
    if info.get("type") != "Feature Layer" or not required <= {f["name"].lower() for f in fields}:
        raise RuntimeError(f"layer {layer_id} metadata missing required fields")
    oid = next((f["name"] for f in fields if f["type"] == "esriFieldTypeOID"), None)
    if not oid or type(info.get("maxRecordCount")) is not int or info["maxRecordCount"] <= 0:
        raise RuntimeError(f"layer {layer_id} has no object ID or positive record page limit")
    ids, tiles = discover_tiles(transport, layer_id, extent, info)
    plan_path = root / f"douglas-co-{layer_name}-plan.json"
    expected = {"layer_id": layer_id, "extent": list(extent), "out_fields": out_fields,
                "page_size": m4a.PAGE_SIZE, "object_ids": ids, "object_id_field": oid}
    if plan_path.exists():
        plan = json.loads(plan_path.read_text())
        if any(plan.get(key) != value for key, value in expected.items()):
            raise RuntimeError("saved tiled record retrieval plan changed")
    else:
        plan = {**expected, "failed_pages": {}, "completed_pages": []}
        write_json(plan_path, plan, indent=2)
    features = retrieve_record_pages(transport, plan, plan_path)
    base = f"{SERVICE}/{layer_id}/query"
    batches = [ids[start:start + m4a.PAGE_SIZE] for start in range(0, len(ids), m4a.PAGE_SIZE)]
    # Recheck each complete leaf without ever returning to the unreliable full envelope.
    # Verification is a single request per leaf, included in the discovery cap.
    if not plan.get("final_ids_verified"):
        try:
            for tile in sorted(tiles["tiles"].values(), key=lambda item: item["id"]):
                if tile["status"] != "complete":
                    continue
                verify_name = (f"resume-{transport.resume_number}-verify.json"
                               if transport.resume_number else "verify.json")
                payload = transport.request(root / f"layer-{layer_id}-tiles" / tile["id"] / verify_name,
                                            base, {**_spatial(tile["extent"]), "f": "json",
                                                   "returnIdsOnly": "true"}, COUNT_ID_TIMEOUT,
                                            context={"tile_id": tile["id"], "phase": "verify",
                                                     "resume_number": transport.resume_number}, layer=layer_id)
                if (not payload.get("exceededTransferLimit") and
                        isinstance(payload.get("objectIds"), list) and
                        all(type(ident) is int for ident in payload["objectIds"]) and
                        sorted(payload["objectIds"]) != tile["object_ids"]):
                    raise RuntimeError(f"layer {layer_id} tile {tile['id']} IDs changed during session")
                current = _validated_ids(payload, tile["count"])
                if current != tile["object_ids"]:
                    raise RuntimeError(f"layer {layer_id} tile {tile['id']} IDs changed during session")
                tile["verified"] = True
                write_json(root / f"layer-{layer_id}-tiles.json", tiles, indent=2)
        except (ServiceFailure, TileOverflow, ExternalBlocked) as error:
            tiles.update(blocked=str(error), coverage_complete=False, verification_incomplete=True,
                         unresolved_tiles=[{"id": item["id"], "envelope": item["extent"]}
                                           for item in tiles["tiles"].values()
                                           if item["status"] == "complete" and not item.get("verified")])
            write_json(root / f"layer-{layer_id}-tiles.json", tiles, indent=2)
            raise ExternalBlocked(f"layer {layer_id} final tile verification blocked: {error}") from error
        plan["final_ids_verified"] = True
        write_json(plan_path, plan, indent=2)
    record = {"region": "douglas-co", "layer_id": layer_id, "where": "1=1",
              "resume_number": transport.resume_number,
              "outFields": f"{out_fields},{oid}", "extent_wgs84": list(extent),
              "page_size": m4a.PAGE_SIZE, "pages": len(batches), "count": len(features),
              "tiles": tiles, "discovery_requests": transport.ledger["discovery_requests"].get(str(layer_id), 0),
              "count_id_timeout_seconds": COUNT_ID_TIMEOUT, "max_record_count": info["maxRecordCount"]}
    return {"type": "FeatureCollection", "features": [features[key] for key in sorted(features)]}, record


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


def run(*, resume_blocked=False):
    if not RAW_ROOT.exists():
        RAW_ROOT.mkdir(parents=True)
    STAGING.mkdir(parents=True, exist_ok=True)
    session = prepare_session(resume_blocked=resume_blocked)
    retrieved_at = session["retrieved_at_utc"]
    client = requests.Session()
    client.mount("https://", HTTPAdapter(max_retries=0))
    client.headers["User-Agent"] = "ohvernight-data/0.2 (+https://github.com/k-kopacek/ohvernight)"
    transport = SavedTransport(client, RAW_ROOT)
    transport.resume_number = session.get("resume_number", 0)
    metadata = transport.request(RAW_ROOT / "service-metadata-response.json", SERVICE, {"f": "json"}, 90)

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
    for evidence in (evidence6, evidence12):
        evidence["retrieved_at"] = retrieved_at

    # Save every primary response page for both layers before deriving rows.
    raw_by_layer = {}
    raw_source_ids = set()
    for source_layer, layer_id, where in (
            ("flowline", 6, "1=1"),
            ("waterbody", 12, "1=1")):
        raw_fc, record = tiled_layer_query(transport, source_layer, layer_id, extent,
                                          m4a.OUT_FIELDS[source_layer])
        query_records.append(record)
        raw_by_layer[source_layer] = raw_fc
        for row in raw_fc["features"]:
            props = {str(key).lower(): value for key, value in row["properties"].items()}
            source_id = props["permanent_identifier"]
            if source_id in raw_source_ids:
                raise RuntimeError(f"permanent_identifier conflict across layers: {source_id}")
            raw_source_ids.add(source_id)
    client.close()

    normalized["flowline"], flowline_counts = _derive_flowlines(
        raw_by_layer["flowline"]["features"], padded, evidence6)
    waterbodies = []
    for row in raw_by_layer["waterbody"]["features"]:
        geom = clip_geometry(row["geometry"], padded)
        if geom:
            waterbodies.append(normalize_feature("waterbody", row, geom, evidence12))
    normalized["waterbody"] = waterbodies
    ensure_unique_feature_ids(normalized["flowline"] + normalized["waterbody"])

    old_by_source_layer = {"flowline": old_layers["waterways"], "waterbody": old_layers["waterbodies"]}
    diff = {}
    for source_layer in ("flowline", "waterbody"):
        features = sorted(normalized[source_layer], key=lambda feature: feature["properties"]["id"])
        features, unmatched_old, unmatched_new = attach_legacy_ids(old_by_source_layer[source_layer], features)
        ensure_unique_feature_ids(features)
        for feature in features:
            ensure_supported_ftype(feature["properties"].get("ftype"), water_display_config())
        normalized[source_layer] = features
        layer_id = "waterways" if source_layer == "flowline" else "waterbodies"
        record = compare_layer(layer_id, old_layers[layer_id], features, coverage, padded)
        record["legacy_unmatched_old_geometry_ids"] = unmatched_old
        record["legacy_unmatched_new_geometry_ids"] = unmatched_new
        record["unsupported_ftypes"] = []
        record["display_count_current_rule"] = sum(display_water(feature) for feature in features)
        diff[layer_id] = record

    existing_legacy = {legacy for features in old_layers.values() for feature in features
                       for legacy in feature["properties"].get("legacy_ids", [])}
    new_legacy = [legacy for features in normalized.values() for feature in features
                  for legacy in feature["properties"].get("legacy_ids", [])]
    legacy_counts = Counter(new_legacy)
    legacy_missing = sorted(existing_legacy - set(new_legacy))
    legacy_duplicated = sorted(ident for ident, count in legacy_counts.items() if count != 1)
    if legacy_missing or legacy_duplicated:
        raise ValueError(f"legacy IDs missing={legacy_missing}, duplicated={legacy_duplicated}")
    for source_layer, features in normalized.items():
        write_json(STAGING / f"douglas-co-{source_layer}.geojson",
                   {"type": "FeatureCollection", "features": features})
    report = {
        "service": SERVICE, "service_currentVersion": metadata.get("currentVersion"),
        "service_metadata": {key: metadata.get(key) for key in ("currentVersion", "documentInfo", "serviceDescription")},
        "retrieved_at_utc": retrieved_at,
        "resume_number": session.get("resume_number", 0),
        "resume_started_at_utc": session.get("resume_started_at_utc"),
        "prior_failed_attempt_directory": PRIOR_RAW_ROOT.relative_to(ROOT).as_posix(),
        "retrieval_strategy": "tiled padded-envelope object-ID discovery; local exact name filter; local O1 derivation",
        "prior_objectid_attempt_directory": OBJECTID_RAW_ROOT.relative_to(ROOT).as_posix(),
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
               "supporting_feature_count": flowline_counts["supporting_features_kept"]}
    print(json.dumps(summary, indent=2))
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", action="store_true", help="start the one authorized live session")
    parser.add_argument("--resume-blocked", action="store_true",
                        help="consume the one authorized resume of the blocked tiled snapshot")
    args = parser.parse_args()
    if not args.run:
        raise SystemExit("pass --run to begin the one authorized Douglas-only NHD session")
    RAW_ROOT.mkdir(parents=True, exist_ok=True)
    session = prepare_session(resume_blocked=args.resume_blocked)
    prior_attempts = sorted(RAW_ROOT.glob("attempt-*.json"))
    attempt_number = len(prior_attempts) + 1
    attempt_path = RAW_ROOT / f"attempt-{attempt_number:04d}.json"
    started_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    attempt = {
        "attempt": attempt_number,
        "resume_number": session.get("resume_number", 0),
        "started_at_utc": started_at,
        "retrieval_strategy": "tiled padded-envelope object-ID discovery; local exact name filter; local O1 derivation",
        "initial_grid": "2x2; SW, SE, NW, NE; at most two subdivisions",
        "discovery_request_cap_per_layer": DISCOVERY_CAP,
        "prior_objectid_attempt_directory": OBJECTID_RAW_ROOT.relative_to(ROOT).as_posix(),
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
        if not isinstance(error, ResumeLater):
            session_path = RAW_ROOT / "session.json"
            session = json.loads(session_path.read_text())
            session["blocked"] = str(error)
            write_json(session_path, session, indent=2)
        raise
    attempt.update(outcome=("staged_review_required" if not report["acceptable_differences_only"] else "staged"),
                   completed_at_utc=datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
                   report_path=str(STAGING / "refresh-report.json"))
    write_json(attempt_path, attempt, indent=2)
    if not report["acceptable_differences_only"]:
        raise SystemExit("Douglas padding differences need coordinator review; canonical files were not written")


if __name__ == "__main__":
    main()
