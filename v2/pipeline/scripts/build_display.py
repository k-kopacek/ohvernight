"""Build deterministic, per-layer GeoJSON delivery artifacts.

The canonical region files remain authoritative.  This module only derives
display geometry and an evidence lookup table; it never contacts a source or
reads the clock.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]


def _pointer(document: Any, pointer: str) -> Any:
    current = document
    if not pointer:
        return current
    for token in pointer[1:].split('/'):
        token = token.replace('~1', '/').replace('~0', '~')
        current = current[int(token)] if isinstance(current, list) else current[token]
    return current


def display_water(feature: dict[str, Any]) -> bool:
    """Python port of MapLayers.displayWater, with no semantic changes."""
    properties = feature.get('properties') or {}
    name = properties.get('name')
    geometry = feature.get('geometry') or {}
    return (
        isinstance(name, str)
        and bool(name.strip())
        and (
            properties.get('kind') == 'flowline'
            and geometry.get('type') in {'LineString', 'MultiLineString'}
            or properties.get('kind') == 'waterbody'
            and geometry.get('type') in {'Polygon', 'MultiPolygon'}
        )
    )


def _round_point(point: list[Any]) -> list[Any]:
    return [round(float(point[0]), 6), round(float(point[1]), 6)]


def _dedupe_path(points: list[Any]) -> list[Any]:
    if not points:
        return []
    closed = points[0] == points[-1]
    result = [points[0]]
    for point in points[1:]:
        if point != result[-1]:
            result.append(point)
    if closed:
        if len(result) == 1:
            return result
        if result[-1] != result[0]:
            result.append(result[0])
    return result


def _round_coordinates(value: Any, depth: int = 0) -> Any:
    if not isinstance(value, list):
        return value
    if value and isinstance(value[0], (int, float)):
        return _round_point(value)
    rounded = [_round_coordinates(item, depth + 1) for item in value]
    # At this depth each child is a coordinate path for LineString/Polygon
    # rings. The geometry type is applied by _round_geometry below.
    return rounded


def _round_geometry(geometry: dict[str, Any] | None) -> dict[str, Any] | None:
    if geometry is None:
        return None
    result = copy.deepcopy(geometry)
    coords = geometry.get('coordinates')
    if geometry.get('type') == 'Point':
        result['coordinates'] = _round_point(coords)
    elif geometry.get('type') == 'MultiPoint':
        result['coordinates'] = [_round_point(point) for point in coords]
    elif geometry.get('type') == 'LineString':
        result['coordinates'] = _dedupe_path([_round_point(point) for point in coords])
    elif geometry.get('type') == 'MultiLineString':
        result['coordinates'] = [_dedupe_path([_round_point(point) for point in line]) for line in coords]
    elif geometry.get('type') == 'Polygon':
        result['coordinates'] = [_dedupe_path([_round_point(point) for point in ring]) for ring in coords]
    elif geometry.get('type') == 'MultiPolygon':
        result['coordinates'] = [
            [_dedupe_path([_round_point(point) for point in ring]) for ring in polygon]
            for polygon in coords
        ]
    else:
        result['coordinates'] = _round_coordinates(coords)
    return result


def _canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False)


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding='utf-8'))


def _source_feature_collection(manifest: dict[str, Any], layer: dict[str, Any], root: Path) -> tuple[dict[str, Any], Path]:
    path = root / layer['path']
    document = _read_json(path)
    value = _pointer(document, layer.get('pointer', ''))
    if not isinstance(value, dict) or value.get('type') != 'FeatureCollection':
        raise ValueError(f"{manifest['region']['id']}/{layer['id']} is not a FeatureCollection")
    return value, path


def _display_feature(feature: dict[str, Any], evidence_indexes: dict[str, int], evidence_table: list[Any]) -> dict[str, Any]:
    result = copy.deepcopy(feature)
    result['geometry'] = _round_geometry(feature.get('geometry'))
    properties = copy.deepcopy(feature.get('properties') or {})
    evidence = properties.get('evidence')
    key = _canonical_json(evidence)
    if key not in evidence_indexes:
        evidence_indexes[key] = len(evidence_table)
        evidence_table.append(copy.deepcopy(evidence))
    properties['evidence'] = evidence_indexes[key]
    result['properties'] = properties
    return result


def build_layer(manifest: dict[str, Any], layer: dict[str, Any], root: Path = ROOT) -> tuple[dict[str, Any], dict[str, Any]]:
    source, canonical_path = _source_feature_collection(manifest, layer, root)
    source_features = source.get('features', [])
    selected = source_features
    if layer['kind'] == 'water' and any('kind' in (f.get('properties') or {}) for f in source_features):
        selected = [feature for feature in source_features if display_water(feature)]
    evidence_indexes: dict[str, int] = {}
    evidence_table: list[Any] = []
    output = {
        'type': 'FeatureCollection',
        'layer_id': layer['id'],
        'evidence_table': evidence_table,
        'features': [_display_feature(feature, evidence_indexes, evidence_table) for feature in selected],
    }
    return output, {
        'layer_id': layer['id'],
        'path': f"regions/{manifest['region']['id']}/display/{layer['id']}.geojson",
        'feature_count': len(selected),
        'source_feature_count': len(source_features),
        'canonical_path': layer['path'],
        'canonical_sha256': hashlib.sha256(canonical_path.read_bytes()).hexdigest(),
    }


def build_coverage(manifest: dict[str, Any], root: Path = ROOT) -> tuple[dict[str, Any], dict[str, Any]]:
    coverage = manifest['coverage']
    canonical_path = root / coverage['path']
    document = _read_json(canonical_path)
    feature = _pointer(document, coverage.get('pointer', ''))
    output = {
        'type': 'FeatureCollection',
        'layer_id': 'coverage',
        'evidence_table': [],
        'features': [{
            'type': 'Feature',
            'geometry': _round_geometry(feature.get('geometry')),
            'properties': copy.deepcopy(feature.get('properties') or {}),
        }],
    }
    return output, {
        'layer_id': 'coverage',
        'path': f"regions/{manifest['region']['id']}/display/coverage.geojson",
        'feature_count': 1,
        'source_feature_count': 1,
        'canonical_path': coverage['path'],
        'canonical_sha256': hashlib.sha256(canonical_path.read_bytes()).hexdigest(),
    }


def _encoded(value: Any) -> bytes:
    return (_canonical_json(value) + '\n').encode('utf-8')


def build_region(region_id: str, root: Path = ROOT, write: bool = False) -> dict[str, Any]:
    manifest = _read_json(root / 'regions' / region_id / 'region.json')
    layers = [layer for layer in manifest['layers'] if layer['format'] == 'feature_collection']
    built = [build_layer(manifest, layer, root) for layer in layers]
    built.append(build_coverage(manifest, root))
    output_dir = root / 'regions' / region_id / 'display'
    entries = []
    artifacts: dict[str, bytes] = {}
    for value, entry in built:
        data = _encoded(value)
        complete = {**entry, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
        entries.append(complete)
        artifacts[entry['path']] = data
        if write:
            target = root / entry['path']
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
    index = {'region_id': region_id, 'artifacts': entries}
    index_data = (_canonical_json(index) + '\n').encode('utf-8')
    artifacts[f"regions/{region_id}/display/index.json"] = index_data
    if write:
        output_dir.mkdir(parents=True, exist_ok=True)
        (output_dir / 'index.json').write_bytes(index_data)
    return {'manifest': manifest, 'index': index, 'artifacts': artifacts}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('regions', nargs='*', default=['aspen', 'douglas-co'])
    parser.add_argument('--root', type=Path, default=ROOT)
    args = parser.parse_args()
    for region_id in args.regions:
        build_region(region_id, args.root, write=True)
        print(f"built {region_id}")


if __name__ == '__main__':
    main()
