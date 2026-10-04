"""Fetching a source is not a legal or on-site verification."""
from datetime import datetime, timezone
import math
import re

def now():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

def freshness(record, now):
    """Return the contract freshness state without reading the clock."""
    if not isinstance(now, datetime) or now.tzinfo is None:
        raise ValueError("now must be timezone-aware")
    if not isinstance(record, dict):
        return "unavailable"

    raw_timestamp = record.get("last_confirmed_at")
    if not isinstance(raw_timestamp, str):
        return "unavailable"
    try:
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}", raw_timestamp):
            timestamp = datetime.fromisoformat(raw_timestamp).replace(tzinfo=timezone.utc)
        else:
            timestamp = datetime.fromisoformat(raw_timestamp.replace("Z", "+00:00"))
            if timestamp.tzinfo is None:
                return "unavailable"
            timestamp = timestamp.astimezone(timezone.utc)
    except (TypeError, ValueError):
        return "unavailable"

    hours = record.get("max_age_hours")
    if isinstance(hours, bool) or not isinstance(hours, (int, float)) or not math.isfinite(hours) or hours <= 0:
        return "unavailable"
    current = now.astimezone(timezone.utc)
    if timestamp > current:
        return "unavailable"
    return "stale" if (current - timestamp).total_seconds() > hours * 3600 else "current"

def make_evidence(source_url, agency, confidence="unverified", verification_method="source_fetch",
                  last_verified=None, notes=None, photos=None, **extra):
    if confidence not in {"high", "medium", "low", "unverified"}:
        raise ValueError("Invalid confidence")
    return {"source_url": source_url, "agency": agency, "retrieved_at": now(),
            "last_verified": last_verified, "confidence": confidence,
            "verification_method": verification_method, "notes": notes or "",
            **({"photos": photos} if photos else {}), **extra}

def derived_evidence(derived_from, method_notes):
    return make_evidence("https://github.com/k-kopacek/ohvernight", "Aspen research pipeline",
                         "low", "derived_intersection", notes=method_notes, inputs=derived_from)
