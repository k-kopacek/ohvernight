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
                     ) -> tuple[dict[str, Any], int]:
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
    result['properties'] = properties
    return result, dropped


def _water_context(manifest: dict[str, Any], root: Path) -> dict[str, Any] | None:
    from shapely.geometry import shape
    from lib.water import group_flowlines, select_water_features, water_display_config

    water_layers = [layer for layer in manifest['layers']
                    if layer.get('kind') == 'water' and layer.get('display', {}).get('select')]
    if not water_layers:
        return None
    stream_layer = next(layer for layer in water_layers if layer['display']['select'] == 'streams')
    canonical, _ = _source_feature_collection(manifest, stream_layer, root)
    canonical_features = canonical.get('features', [])
    review = {'inclusions': [], 'exclusions': []}
    review_ref = manifest.get('water_review')
    if isinstance(review_ref, dict):
        review_doc = _read_json(root / review_ref['path'])
        review = _pointer(review_doc, review_ref.get('pointer', ''))
    coverage_doc = _read_json(root / manifest['coverage']['path'])
    coverage_feature = _pointer(coverage_doc, manifest['coverage'].get('pointer', ''))
    coverage = shape(coverage_feature['geometry'])
    clip_padding = stream_layer.get('extent_padding_deg', 0.0) or 0.0
    config = water_display_config()
    grouped = group_flowlines(canonical_features, config, region_id=manifest['region']['id'],
                              review=review, coverage=coverage.buffer(clip_padding))
    body_layer = next(layer for layer in water_layers if layer['display']['select'] == 'bodies')
    body_collection, _ = _source_feature_collection(manifest, body_layer, root)
    body_features = [feature for feature in body_collection.get('features', [])
                     if (feature.get('properties') or {}).get('source_layer') == 'waterbody']
    body_decisions = select_water_features(body_features, config, review)
    selected_body_ids = {row['feature']['properties']['id'] for row in body_decisions
                         if row['eligible']}
    all_water_features = {feature['properties']['id']: feature
                          for feature in [*canonical_features, *body_features]}
    return {'canonical_features': canonical_features, 'all_water_features': list(all_water_features.values()),
            'body_features': body_features,
            'selected_body_ids': selected_body_ids, 'grouped': grouped, 'config': config,
            'review': review, 'body_layer': body_layer}


def build_layer(manifest: dict[str, Any], layer: dict[str, Any], root: Path = ROOT,
                water_context: dict[str, Any] | None = None) -> tuple[dict[str, Any], dict[str, Any]]:
    source, canonical_path = _source_feature_collection(manifest, layer, root)
    source_features = source.get('features', [])
    selected = source_features
    selector = (layer.get('display') or {}).get('select')
    if layer['kind'] == 'water' and selector in {'streams', 'bodies'}:
        if water_context is None:
            water_context = _water_context(manifest, root)
        if selector == 'streams':
            selected = water_context['grouped']['groups']
        else:
            selected = [feature for feature in water_context['body_features']
                        if feature['properties']['id'] in water_context['selected_body_ids']]
    evidence_indexes: dict[str, int] = {}
    evidence_table: list[Any] = []
    display_features = []
    dropped_parts = 0
    for feature in selected:
        if selector == 'bodies':
            props = feature.get('properties') or {}
            feature = {**feature, 'properties': {key: props.get(key) for key in
                        ('id', 'name', 'gnis_id', 'water_class', 'hydro_category', 'fcode',
                         'area_sqkm', 'evidence')}}
        display_feature, dropped = _display_feature(feature, evidence_indexes, evidence_table)
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
    water_context = _water_context(manifest, root)
    built = [build_layer(manifest, layer, root, water_context) for layer in layers]
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
    transport = {}
    for layer in manifest['layers']:
        reference = layer.get('status_ref')
        if reference is not None:
            transport[layer['id']] = copy.deepcopy(_pointer(
                _read_json(root / reference['path']), reference.get('pointer', '')))
    index = {'region_id': region_id, 'artifacts': entries, 'transport': transport}
    if water_context is not None:
        index['water_groups'] = water_context['grouped']['water_groups']
    aliases = {}
    if water_context is not None:
        targets = {member_id: group_id
                   for group_id, member_ids in water_context['grouped']['water_groups'].items()
                   for member_id in member_ids}
        targets.update({ident: ident for ident in water_context['selected_body_ids']})
        for feature in water_context['all_water_features']:
            props = feature.get('properties') or {}
            target = targets.get(props.get('id'))
            if target is None:
                continue
            for legacy_id in props.get('legacy_ids', []):
                if legacy_id in aliases:
                    raise ValueError(f'duplicate water legacy ID in display index: {legacy_id}')
                aliases[legacy_id] = target
    if aliases:
        alias_path = f"regions/{region_id}/display/water-aliases.json"
        alias_data = _encoded({'region_id': region_id, 'water_id_aliases': aliases})
        index['water_aliases'] = {
            'path': alias_path,
            'bytes': len(alias_data),
            'sha256': hashlib.sha256(alias_data).hexdigest(),
        }
        artifacts[alias_path] = alias_data
        if write:
            target = root / alias_path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(alias_data)
    index_data = (_canonical_json(index) + '\n').encode('utf-8')
    artifacts[f"regions/{region_id}/display/index.json"] = index_data
    if write:
        output_dir.mkdir(parents=True, exist_ok=True)
        (output_dir / 'index.json').write_bytes(index_data)
    return {'manifest': manifest, 'index': index, 'artifacts': artifacts}


def build_water_report(root: Path = ROOT) -> dict[str, Any]:
    """Compute the offline M4-B selection/grouping summary without writing files."""
    result = {}
    for region_id in ("aspen", "douglas-co"):
        manifest = _read_json(root / "regions" / region_id / "region.json")
        context = _water_context(manifest, root)
        grouped = context["grouped"]
        group_summaries = {row["group_id"]: row for row in grouped["group_summaries"]}
        expected_rivers = {}
        for check in grouped["major_river_checks"]:
            expected_rivers[check["gnis_id"]] = {
                "group_ids": check["group_ids"],
                "member_counts": [group_summaries[group_id]["member_count"]
                                  for group_id in check["group_ids"]],
                "drawn_fraction": check["drawn_fraction"],
                "state": ("PENDING_EXTERNAL_SOURCE_REFRESH"
                          if any(item["gnis_id"] == check["gnis_id"]
                                 for item in grouped["pending_external_source_refresh"])
                          else "confirmed"),
            }
        result[region_id] = {
            "group_count": len(grouped["groups"]),
            "members_per_expected_river": expected_rivers,
            "multi_part_gnis_ids": grouped["multi_part_gnis_ids"],
            "connectors_used_with_lengths": grouped["connectors_used"],
            "extent_edge_splits": grouped["extent_edge_splits"],
            "waterbodies_displayed_at_0_02_sqkm": len(context["selected_body_ids"]),
        }
    return result


def build_selection_report(root: Path = ROOT) -> str:
    """Render the deterministic section 8.6 review report from committed data."""
    from collections import Counter, defaultdict
    from shapely.geometry import shape
    from lib.water import geodesic_length_km, select_water_features

    lines = ['# M4-B water selection report', '',
             'Generated from committed canonical data and `water_display.json`; no source is contacted.', '']
    for region_id in ('aspen', 'douglas-co'):
        manifest = _read_json(root / 'regions' / region_id / 'region.json')
        context = _water_context(manifest, root)
        grouped = context['grouped']
        by_member = {member: group_id for group_id, members in grouped['water_groups'].items()
                     for member in members}
        displayed_ids = set(by_member) | context['selected_body_ids']
        all_features = context['all_water_features']
        display_counts = Counter()
        not_display_counts = Counter()
        for feature in all_features:
            props = feature.get('properties') or {}
            key = (props.get('water_class', 'unknown'), props.get('hydro_category', 'unknown'))
            (display_counts if props.get('id') in displayed_ids else not_display_counts)[key] += 1

        built = build_region(region_id, root, write=False)
        index = built['index']
        artifact_by_id = {entry['layer_id']: entry for entry in index['artifacts']}
        stream_layer_id = next(layer['id'] for layer in manifest['layers']
                               if layer.get('display', {}).get('select') == 'streams')
        body_layer = context['body_layer']
        body_features = context['body_features']
        selected_2ha = context['selected_body_ids']
        decisions_05 = select_water_features(body_features, context['config'], context['review'],
                                             threshold_sqkm=0.005)
        selected_05 = {row['feature']['properties']['id'] for row in decisions_05 if row['eligible']}

        def body_artifact_bytes(selected_ids):
            evidence_indexes, evidence_table, features = {}, [], []
            for feature in body_features:
                if feature['properties']['id'] not in selected_ids:
                    continue
                props = feature.get('properties') or {}
                projection = {key: props.get(key) for key in
                              ('id', 'name', 'gnis_id', 'water_class', 'hydro_category',
                               'fcode', 'area_sqkm', 'evidence')}
                display_feature, _ = _display_feature({**feature, 'properties': projection},
                                                       evidence_indexes, evidence_table)
                features.append(display_feature)
            return len(_encoded({'type': 'FeatureCollection', 'layer_id': body_layer['id'],
                                 'evidence_table': evidence_table, 'features': features}))

        stream_bytes = len(built['artifacts'][artifact_by_id[stream_layer_id]['path']])
        body_bytes_2ha = len(built['artifacts'][artifact_by_id[body_layer['id']]['path']])
        body_bytes_05 = body_artifact_bytes(selected_05)
        stream_summaries = grouped['group_summaries']
        members_distribution = Counter(row['member_count'] for row in stream_summaries)
        lines.extend([f'## {region_id}', '', '### Source feature selection by class and category', '',
                      '| Water class | Hydro category | Displayed members or bodies | Not displayed |',
                      '|---|---:|---:|---:|'])
        keys = sorted(set(display_counts) | set(not_display_counts))
        for water_class, category in keys:
            lines.append(f'| {water_class} | {category} | {display_counts[(water_class, category)]} | {not_display_counts[(water_class, category)]} |')
        lines.extend(['', '### Groups and connectivity', '',
                      f'- Stream groups: {len(grouped["groups"])}',
                      '- Members per group distribution (member count: number of groups): ' +
                      (', '.join(f'{count}: {members_distribution[count]}'
                                 for count in sorted(members_distribution)) or 'none'),
                      '- Multi-part GNIS IDs and part group IDs: ' +
                      (json.dumps(grouped['multi_part_gnis_ids'], sort_keys=True) if grouped['multi_part_gnis_ids'] else 'none'),
                      '- Connectors used with geodesic lengths in km: ' +
                      (json.dumps(grouped['connectors_used'], ensure_ascii=False, sort_keys=True) if grouped['connectors_used'] else 'none'),
                      '- Extent-edge splits and drawn line counts: ' +
                      (json.dumps(grouped['extent_edge_splits'], ensure_ascii=False, sort_keys=True) if grouped['extent_edge_splits'] else 'none'),
                      '- Reviewed exclusions: ' +
                      (json.dumps(context['review'].get('exclusions', []), ensure_ascii=False, sort_keys=True)
                       if context['review'].get('exclusions') else 'none'), ''])

        def body_rows(features):
            output = []
            for feature in features:
                props = feature.get('properties') or {}
                try:
                    point = shape(feature['geometry']).representative_point()
                    coordinates = [round(point.x, 6), round(point.y, 6)]
                except (KeyError, TypeError, ValueError):
                    coordinates = None
                output.append({'id': props.get('id'), 'name': props.get('name'),
                               'area_sqkm': props.get('area_sqkm'),
                               'elevation_m': props.get('elevation_m'),
                               'coordinates_lon_lat': coordinates})
            return output

        decisions_2ha = select_water_features(body_features, context['config'], context['review'])
        excluded_2ha = [row['feature'] for row in decisions_2ha
                        if not row['eligible'] and row['reason'] != 'reviewed_exclusion']
        included_at_05_but_not_2 = [row['feature'] for row in decisions_05
                                    if row['eligible'] and row['feature']['properties']['id'] not in selected_2ha]
        included_2ha_features = [row['feature'] for row in decisions_2ha if row['eligible']]
        unnamed_05 = sum(not ((row['feature'].get('properties') or {}).get('name') or '').strip()
                         for row in decisions_05 if row['eligible'])
        unnamed_2ha = sum(not ((row['feature'].get('properties') or {}).get('name') or '').strip()
                          for row in decisions_2ha if row['eligible'])
        lines.extend(['### Waterbody threshold comparison', '',
                      '| Threshold | Unnamed included | Total displayed | Water display bytes |',
                      '|---|---:|---:|---:|',
                      f'| 0.5 ha (0.005 km²) | {unnamed_05} | {len(selected_05)} | {stream_bytes + body_bytes_05} |',
                      f'| 2 ha (0.02 km²) | {unnamed_2ha} | {len(selected_2ha)} | {stream_bytes + body_bytes_2ha} |',
                      '', 'Largest waterbodies excluded at 2 ha and included at 0.5 ha:', '',
                      '```json',
                      json.dumps(body_rows(sorted(included_at_05_but_not_2,
                                                  key=lambda feature: (-(feature['properties'].get('area_sqkm') or 0),
                                                                       feature['properties']['id']))[:20]),
                                 ensure_ascii=False, indent=2),
                      '```', '', 'Twenty smallest waterbodies included at 2 ha:', '', '```json',
                      json.dumps(body_rows(sorted(included_2ha_features,
                                                  key=lambda feature: (feature['properties'].get('area_sqkm') or 0,
                                                                       feature['properties']['id']))[:20]),
                                 ensure_ascii=False, indent=2), '```', ''])

        artificial_by_gnis = defaultdict(list)
        for feature in context['canonical_features']:
            props = feature.get('properties') or {}
            if (props.get('water_class') == 'artificial_path' and props.get('gnis_id')
                    and isinstance(props.get('name'), str) and props['name'].strip()
                    and not props.get('support_for')):
                artificial_by_gnis[props['gnis_id']].append(feature)
        drawn_artificial = defaultdict(list)
        for member_id, group_id in by_member.items():
            member = next((feature for feature in context['canonical_features']
                           if (feature.get('properties') or {}).get('id') == member_id), None)
            if member and (member.get('properties') or {}).get('water_class') == 'artificial_path':
                drawn_artificial[(member['properties']['gnis_id'], group_id)].append(member)
        wide_paths = []
        group_gnis = defaultdict(list)
        for summary in stream_summaries:
            group_gnis[summary['gnis_id']].append(summary['group_id'])
        for gnis_id, features in sorted(artificial_by_gnis.items()):
            total = geodesic_length_km(features)
            if total <= 2:
                continue
            drawn_ids = [ident for ident in by_member
                         if any((feature.get('properties') or {}).get('id') == ident
                                for feature in features)]
            drawn_features = [feature for feature in features
                              if (feature.get('properties') or {}).get('id') in drawn_ids]
            drawn_length = geodesic_length_km(drawn_features)
            fraction = drawn_length / total if total else 0.0
            if drawn_length == 0 or fraction < 0.8:
                wide_paths.append({'gnis_id': gnis_id,
                                   'name': (features[0].get('properties') or {}).get('name'),
                                   'artificial_path_length_km': round(total, 3),
                                   'drawn_artificial_path_length_km': round(drawn_length, 3),
                                   'drawn_fraction': round(fraction, 6),
                                   'group_ids': group_gnis.get(gnis_id, [])})
        lines.extend(['### Named artificial-path rivers over 2 km that are undrawn or under 80%', '',
                      '```json', json.dumps(wide_paths, ensure_ascii=False, indent=2), '```', ''])
        if region_id == 'douglas-co':
            lines.extend(['**PENDING_EXTERNAL_SOURCE_REFRESH:** Douglas South Platte River `00201759` is absent from the committed source bundle. Douglas counts and geometry will change when the padded NHD refresh lands.', ''])
        else:
            lines.extend(['South Platte River pending marker is Douglas-only; Aspen is not affected.', ''])
    lines.extend(['## Reviewer notes', '',
                  'To be written by Codex after the padded refresh and checked by the coordinator.', ''])
    return '\n'.join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('regions', nargs='*', default=['aspen', 'douglas-co'])
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--water-report', action='store_true',
                        help='print M4-B water selection and grouping without writing files')
    parser.add_argument('--report', action='store_true',
                        help='write the deterministic M4-B section 8.6 selection report')
    args = parser.parse_args()
    if args.water_report:
        print(json.dumps(build_water_report(args.root), ensure_ascii=False, indent=2))
        return
    if args.report:
        target = args.root.parent / 'docs' / 'research' / 'm4-water' / 'selection-report.md'
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(build_selection_report(args.root), encoding='utf-8')
        print(f'wrote {target}')
        return
    for region_id in args.regions:
        build_region(region_id, args.root, write=True)
        print(f"built {region_id}")


if __name__ == '__main__':
    main()
