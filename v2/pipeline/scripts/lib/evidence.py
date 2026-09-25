"""Fetching a source is not a legal or on-site verification."""
from datetime import datetime, timezone

def now():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

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
