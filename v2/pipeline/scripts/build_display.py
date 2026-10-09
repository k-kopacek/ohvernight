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
import os
import shutil
import tempfile
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
    kind = properties.get('kind')
    source_layer = properties.get('source_layer')
    return (
        isinstance(name, str)
        and bool(name.strip())
        and (
            (kind == 'flowline' or source_layer == 'flowline')
            and geometry.get('type') in {'LineString', 'MultiLineString'}
            or (kind == 'waterbody' or source_layer == 'waterbody')
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


def _rounded_path(points: list[Any], minimum: int) -> tuple[list[Any] | None, int]:
    rounded = _dedupe_path([_round_point(point) for point in points])
    if len(rounded) < minimum:
        return None, 1
    return rounded, 0


def _transform_geometry(geometry: dict[str, Any] | None) -> tuple[dict[str, Any] | None, int]:
    if geometry is None:
        return None, 0
    geometry_type = geometry.get('type')
    coords = geometry.get('coordinates')
    result = copy.deepcopy(geometry)
    dropped = 0
    if geometry_type == 'Point':
        result['coordinates'] = _round_point(coords)
    elif geometry_type == 'MultiPoint':
        result['coordinates'] = [_round_point(point) for point in coords]
    elif geometry_type == 'LineString':
        path, dropped = _rounded_path(coords, 2)
        if path is None:
            return None, dropped
        result['coordinates'] = path
    elif geometry_type == 'MultiLineString':
        lines, dropped = [], 0
        for line in coords:
            path, count = _rounded_path(line, 2)
            dropped += count
            if path is not None:
                lines.append(path)
        if not lines:
            raise ValueError('every MultiLineString part collapses after display rounding')
        result['coordinates'] = lines
    elif geometry_type == 'Polygon':
        rings, dropped = [], 0
        for index, ring in enumerate(coords):
            path, count = _rounded_path(ring, 4)
            dropped += count
            if index == 0 and path is None:
                return None, dropped
            if path is not None:
                rings.append(path)
        result['coordinates'] = rings
    elif geometry_type == 'MultiPolygon':
        polygons, dropped = [], 0
        for polygon in coords:
            rings = []
            exterior, count = _rounded_path(polygon[0], 4)
            dropped += count
            if exterior is None:
                continue
            rings.append(exterior)
            for hole in polygon[1:]:
                path, count = _rounded_path(hole, 4)
                dropped += count
                if path is not None:
                    rings.append(path)
            polygons.append(rings)
        if not polygons:
            raise ValueError('every MultiPolygon part collapses after display rounding')
        result['coordinates'] = polygons
    else:
        raise ValueError(f'unsupported geometry type: {geometry_type}')
    return result, dropped


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


def _display_feature(feature: dict[str, Any], evidence_indexes: dict[str, int], evidence_table: list[Any],
                     *, water: bool = False) -> tuple[dict[str, Any], int]:
    result = copy.deepcopy(feature)
    result['geometry'], dropped = _transform_geometry(feature.get('geometry'))
    if feature.get('geometry') is not None and result['geometry'] is None:
        raise ValueError(f"feature {feature.get('properties', {}).get('id')} collapses after display rounding")
    properties = copy.deepcopy(feature.get('properties') or {})
    evidence = properties.get('evidence')
    key = _canonical_json(evidence)
    if key not in evidence_indexes:
        evidence_indexes[key] = len(evidence_table)
        evidence_table.append(copy.deepcopy(evidence))
    properties['evidence'] = evidence_indexes[key]
    if water:
        retained = {'id', 'name', 'evidence', 'kind', 'source_layer'}
        properties = {name: value for name, value in properties.items() if name in retained}
    result['properties'] = properties
    return result, dropped


def build_layer(manifest: dict[str, Any], layer: dict[str, Any], root: Path = ROOT) -> tuple[dict[str, Any], dict[str, Any]]:
    source, canonical_path = _source_feature_collection(manifest, layer, root)
    source_features = source.get('features', [])
    selected = source_features
    if layer['kind'] == 'water' and any(
            {'kind', 'source_layer'} & set(f.get('properties') or {}) for f in source_features):
        selected = [feature for feature in source_features if display_water(feature)]
    evidence_indexes: dict[str, int] = {}
    evidence_table: list[Any] = []
    display_features = []
    dropped_parts = 0
    for feature in selected:
        display_feature, dropped = _display_feature(feature, evidence_indexes, evidence_table,
                                                     water=layer['kind'] == 'water')
        display_features.append(display_feature)
        dropped_parts += dropped
    output = {
        'type': 'FeatureCollection',
        'layer_id': layer['id'],
        'evidence_table': evidence_table,
        'features': display_features,
    }
    return output, {
        'layer_id': layer['id'],
        'path': f"regions/{manifest['region']['id']}/display/{layer['id']}.geojson",
        'feature_count': len(selected),
        'source_feature_count': len(source_features),
        'dropped_degenerate_parts': dropped_parts,
        'canonical_path': layer['path'],
        'canonical_sha256': hashlib.sha256(canonical_path.read_bytes()).hexdigest(),
    }


def build_coverage(manifest: dict[str, Any], root: Path = ROOT) -> tuple[dict[str, Any], dict[str, Any]]:
    coverage = manifest['coverage']
    canonical_path = root / coverage['path']
    document = _read_json(canonical_path)
    feature = _pointer(document, coverage.get('pointer', ''))
    geometry, dropped_parts = _transform_geometry(feature.get('geometry'))
    if geometry is None:
        raise ValueError('coverage collapses after display rounding')
    output = {
        'type': 'FeatureCollection',
        'layer_id': 'coverage',
        'evidence_table': [],
        'features': [{
            'type': 'Feature',
            'geometry': geometry,
            'properties': copy.deepcopy(feature.get('properties') or {}),
        }],
    }
    return output, {
        'layer_id': 'coverage',
        'path': f"regions/{manifest['region']['id']}/display/coverage.geojson",
        'feature_count': 1,
        'source_feature_count': 1,
        'dropped_degenerate_parts': dropped_parts,
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
    transport = {}
    for layer in manifest['layers']:
        reference = layer.get('status_ref')
        if reference is not None:
            transport[layer['id']] = copy.deepcopy(_pointer(
                _read_json(root / reference['path']), reference.get('pointer', '')))
    index = {'region_id': region_id, 'artifacts': entries, 'transport': transport}
    aliases = {}
    for layer, (display, _) in zip(
            (layer for layer in manifest['layers'] if layer['format'] == 'feature_collection'), built):
        if layer['kind'] != 'water':
            continue
        display_ids = {(feature.get('properties') or {}).get('id') for feature in display['features']}
        source, _ = _source_feature_collection(manifest, layer, root)
        for feature in source['features']:
            props = feature.get('properties') or {}
            if props.get('id') not in display_ids:
                continue
            for legacy_id in props.get('legacy_ids', []):
                if legacy_id in aliases:
                    raise ValueError(f'duplicate water legacy ID in display index: {legacy_id}')
                aliases[legacy_id] = props['id']
    if aliases:
        alias_path = f"regions/{region_id}/display/water-aliases.json"
        alias_data = _encoded({'region_id': region_id, 'water_id_aliases': aliases})
        index['water_aliases'] = {
            'path': alias_path,
            'bytes': len(alias_data),
            'sha256': hashlib.sha256(alias_data).hexdigest(),
        }
        artifacts[alias_path] = alias_data
    index_data = (_canonical_json(index) + '\n').encode('utf-8')
    artifacts[f"regions/{region_id}/display/index.json"] = index_data
    if write:
        output_dir.parent.mkdir(parents=True, exist_ok=True)
        stage = Path(tempfile.mkdtemp(prefix=f'.{region_id}-display-', dir=output_dir.parent))
        backup = output_dir.with_name(f'.{output_dir.name}-backup-{os.getpid()}')
        moved_old = False
        try:
            for relative, data in artifacts.items():
                destination = stage / Path(relative).name
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes(data)
            if backup.exists():
                shutil.rmtree(backup)
            if output_dir.exists():
                output_dir.replace(backup)
                moved_old = True
            try:
                stage.replace(output_dir)
            except Exception:
                if moved_old and backup.exists():
                    backup.replace(output_dir)
                    moved_old = False
                raise
            if backup.exists():
                shutil.rmtree(backup)
        finally:
            if stage.exists():
                shutil.rmtree(stage)
            if backup.exists() and not output_dir.exists():
                backup.replace(output_dir)
            elif backup.exists():
                shutil.rmtree(backup)
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
