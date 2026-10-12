"""Informational, fail-open reporting for published USFS trail snapshots."""
import hashlib
import json


def _canonical_hash(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()).hexdigest()


def report_trail_drift(previous_path, current_features, label='trails', douglas=False):
    """Print deterministic differences; malformed prior snapshots never block publication."""
    try:
        with open(previous_path, encoding='utf-8') as stream:
            previous = json.load(stream)
        if douglas:
            previous = previous.get('layers', {}).get('trails', {})
        if not isinstance(previous, dict) or not isinstance(previous.get('features'), list):
            raise ValueError('previous snapshot is not a feature collection')
        old_features = previous['features']
        old = {}
        for feature in old_features:
            props = feature.get('properties') or {}
            feature_id = props.get('id')
            if feature_id is None:
                raise ValueError('prior feature is missing properties.id')
            if feature_id in old:
                raise ValueError(f'duplicate prior feature id {feature_id}')
            old[feature_id] = feature
        current = {}
        for feature in current_features:
            props = feature.get('properties') or {}
            feature_id = props.get('id')
            if feature_id is None:
                raise ValueError('prior feature is missing properties.id')
            if feature_id in current:
                raise ValueError(f'duplicate current feature id {feature_id}')
            current[feature_id] = feature
        added = sorted(set(current) - set(old))
        removed = sorted(set(old) - set(current))
        if added:
            print(f'{label} drift: added IDs: {", ".join(added)}')
        if removed:
            print(f'{label} drift: removed IDs: {", ".join(removed)}')
        for feature_id in sorted(set(current) & set(old)):
            before, after = old[feature_id], current[feature_id]
            changes = []
            if _canonical_hash(before.get('geometry')) != _canonical_hash(after.get('geometry')):
                changes.append(f"geometry: {_canonical_hash(before.get('geometry'))} -> {_canonical_hash(after.get('geometry'))}")
            bp, ap = before['properties'], after['properties']
            for key in sorted((set(bp) | set(ap)) - {'evidence', 'activities'}):
                if bp.get(key) != ap.get(key):
                    changes.append(f'{key}: {bp.get(key)!r} -> {ap.get(key)!r}')
            ba, aa = bp.get('activities') or {}, ap.get('activities') or {}
            for activity in sorted(set(ba) | set(aa)):
                before_fields, after_fields = ba.get(activity) or {}, aa.get(activity) or {}
                for field in sorted(set(before_fields) | set(after_fields)):
                    if before_fields.get(field) != after_fields.get(field):
                        changes.append(f'activities.{activity}.{field}: {before_fields.get(field)!r} -> {after_fields.get(field)!r}')
            if changes:
                print(f'{label} drift {feature_id}: ' + '; '.join(changes))
    except FileNotFoundError:
        return
    except Exception as error:
        print(f'drift comparison skipped: {error}')
