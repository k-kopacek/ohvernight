"""Read ArcGIS feature layers by ID; reject incomplete or changed snapshots."""
import requests
import time
from shapely.geometry import Polygon, mapping, box
from shapely import make_valid
from shapely.ops import unary_union
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
USER_AGENT = "aspen-overnight-data/0.2 (+https://k-kopacek.github.io/aspen-overnight/)"

class ArcGISQueryError(RuntimeError):
    pass

def native_features(payload, boundary=None):
    """Convert ArcGIS JSON requested in EPSG:4326, preserving polygon holes."""
    sr = payload.get("spatialReference", {})
    if sr.get("latestWkid", sr.get("wkid")) != 4326:
        raise ArcGISQueryError("Native geometry did not confirm WGS84")
    if not isinstance(payload.get("features"), list):
        raise ArcGISQueryError("Native response missing features")
    rows = []
    for row in payload["features"]:
        g = row.get("geometry") or {}
        if "rings" in g:
            # ArcGIS rings can contain holes and islands in arbitrary order.
            # Even/odd filling retains both without assuming the first ring is a shell.
            polygon = Polygon()
            for ring in g["rings"]:
                part = Polygon([p[:2] for p in ring])
                if not part.is_valid:
                    repaired = make_valid(part)
                    part = repaired if repaired.geom_type in {"Polygon", "MultiPolygon"} else unary_union(
                        [g for g in repaired.geoms if g.geom_type in {"Polygon", "MultiPolygon"}])
                if part.is_empty:
                    raise ArcGISQueryError("Invalid native polygon ring")
                # National ownership features can contain thousands of remote rings.
                # Intersection distributes over even/odd filling: crop each ring
                # before combining, retaining exact coordinates without simplification.
                if boundary is not None:
                    part = part.intersection(boundary)
                    if part.is_empty or part.area == 0:
                        continue
                polygon = polygon.symmetric_difference(part)
            if polygon.geom_type not in {"Polygon", "MultiPolygon"}:
                raise ArcGISQueryError("Invalid native polygon")
            geometry = mapping(polygon)
        elif "paths" in g:
            geometry = {"type": "MultiLineString", "coordinates": [[p[:2] for p in path] for path in g["paths"]]}
        elif "x" in g and "y" in g:
            geometry = {"type": "Point", "coordinates": [g["x"], g["y"]]}
        elif "points" in g:
            geometry = {"type": "MultiPoint", "coordinates": [p[:2] for p in g["points"]]}
        else:
            raise ArcGISQueryError("Missing or unsupported native geometry")
        rows.append({"type": "Feature", "properties": row.get("attributes", {}), "geometry": geometry})
    return rows

def new_session():
    client = requests.Session()
    retry = Retry(total=2, backoff_factor=0.5, status_forcelist=[429, 500, 502, 503, 504])
    client.mount("https://", HTTPAdapter(max_retries=retry))
    client.headers["User-Agent"] = USER_AGENT
    return client

def get_json(client, url, params, timeout=90):
    # ArcGIS also reports transient server failures inside HTTP 200 responses.
    for attempt in range(3):
        response = client.get(url, params=params, timeout=timeout)
        response.raise_for_status()
        value = response.json()
        if isinstance(value, dict) and "error" not in value:
            return value
        error = value.get("error") if isinstance(value, dict) else "not an object"
        code = error.get("code") if isinstance(error, dict) else None
        if code not in {429, 500, 502, 503, 504} or attempt == 2:
            raise ArcGISQueryError(f"{url}: {error}")
        time.sleep(0.5 * 2 ** attempt)

def describe_layer(base_url, layer_id, timeout=30, session=None, required_fields=()):
    info = get_json(session or new_session(), f"{base_url.rstrip('/')}/{layer_id}", {"f": "json"}, timeout)
    if info.get("type") != "Feature Layer" or not isinstance(info.get("fields"), list):
        raise ArcGISQueryError(f"Layer {layer_id} is {info.get('type')}, not a queryable feature layer")
    fields = {f["name"].lower() for f in info["fields"]}
    missing = set(map(str.lower, required_fields)) - fields
    if missing:
        raise ArcGISQueryError(f"Layer {layer_id} missing {sorted(missing)}; available: {sorted(fields)}")
    return info

def query_layer_geojson(base_url, layer_id, bbox_wgs84, where="1=1", out_fields="*",
                        page_size=100, max_pages=1000, timeout=90, session=None,
                        required_fields=(), native_json=False):
    client = session or new_session()
    info = describe_layer(base_url, layer_id, timeout, client, required_fields)
    oid = next((f["name"] for f in info["fields"] if f["type"] == "esriFieldTypeOID"), None)
    if not oid:
        raise ArcGISQueryError("Layer has no object-ID field")
    url = f"{base_url.rstrip('/')}/{layer_id}/query"
    spatial = {"where": where, "geometry": ",".join(map(str, bbox_wgs84)),
               "geometryType": "esriGeometryEnvelope", "inSR": 4326,
               "spatialRel": "esriSpatialRelIntersects"}
    try:
        counts = get_json(client, url, {**spatial, "f": "json", "returnCountOnly": "true"}, timeout)
    except (ArcGISQueryError, requests.RequestException):
        # Some servers fail count queries while their complete ID query works.
        # ArcGIS returnIdsOnly is not subject to the feature-page record limit.
        # Still verify every requested ID and repeat the full ID query at the end.
        counts = None
        print(f"Count query unavailable for layer {layer_id}; checking complete object-ID sets", flush=True)
    payload = get_json(client, url, {**spatial, "f": "json", "returnIdsOnly": "true"}, timeout)
    if payload.get("exceededTransferLimit") or (payload.get("properties") or {}).get("exceededTransferLimit"):
        raise ArcGISQueryError("Truncated object-ID response")
    if not isinstance(payload.get("objectIds"), list) and (counts or {}).get("count") != 0:
        raise ArcGISQueryError("Missing complete object-ID list")
    ids = sorted(payload.get("objectIds") or [])
    if (counts is not None and counts.get("count") != len(ids)) or len(ids) != len(set(ids)):
        raise ArcGISQueryError("Count/ID mismatch: dataset changed or incomplete IDs")
    size = min(page_size, info.get("maxRecordCount") or page_size)
    if size < 1 or len(ids) > size * max_pages:
        raise ArcGISQueryError("Query exceeds configured record limit")
    fields = out_fields if out_fields == "*" else f"{out_fields},{oid}"

    def fetch_batch(batch):
        try:
            result = get_json(client, url, {"f": "json" if native_json else "geojson", "objectIds": ",".join(map(str, batch)),
                              "outFields": fields, "outSR": 4326, "returnGeometry": "true",
                              "returnZ": "false", "returnM": "false"}, timeout)
        except (requests.RequestException, ArcGISQueryError):
            if len(batch) < 2:
                raise
            middle = len(batch) // 2
            return fetch_batch(batch[:middle]) + fetch_batch(batch[middle:])
        rows = result.get("features")
        if (not native_json and result.get("type") != "FeatureCollection") or not isinstance(rows, list):
            raise ArcGISQueryError("Expected GeoJSON FeatureCollection")
        limited = result.get("exceededTransferLimit") or (result.get("properties") or {}).get("exceededTransferLimit")
        if limited:
            if len(batch) < 2:
                raise ArcGISQueryError("Single feature exceeds transfer limit")
            middle = len(batch) // 2
            return fetch_batch(batch[:middle]) + fetch_batch(batch[middle:])
        if native_json:
            rows = native_features(result, box(*bbox_wgs84))
        actual = [next((v for k, v in f.get("properties", {}).items() if k.lower() == oid.lower()), f.get("id")) for f in rows]
        if set(actual) != set(batch) or len(actual) != len(batch):
            raise ArcGISQueryError("Missing/duplicate IDs; refusing partial data")
        if any(not f.get("geometry") for f in rows):
            raise ArcGISQueryError("Missing feature geometry")
        return rows

    features = []
    for offset in range(0, len(ids), size):
        features.extend(fetch_batch(ids[offset:offset + size]))
    final = get_json(client, url, {**spatial, "f": "json", "returnIdsOnly": "true"}, timeout)
    if final.get("exceededTransferLimit") or (final.get("properties") or {}).get("exceededTransferLimit"):
        raise ArcGISQueryError("Truncated final object-ID response")
    if sorted(final.get("objectIds") or []) != ids:
        raise ArcGISQueryError("Dataset IDs changed during download; retry a fresh run")
    return {"type": "FeatureCollection", "features": features}
