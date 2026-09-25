"""Detect source changes without inventing a current fire stage from page-wide keywords."""
import hashlib
import json
from lib.arcgis_client import new_session
from lib.common import source, output_dir, write_fc
from lib.evidence import make_evidence, now

def main():
    src = source("fire")
    response = new_session().get(src["url"], timeout=30)
    response.raise_for_status()
    content = response.text
    digest = hashlib.sha256(content.encode()).hexdigest()
    # Only last published source hash is read. No raw news or secrets are published.
    previous_path = output_dir().parent / "map-data-v2.json"
    previous = None
    if previous_path.exists():
        data = json.loads(previous_path.read_text())
        records = data.get("layers", {}).get("fire_restriction_stage", {}).get("features", [])
        if records:
            previous = records[0]["properties"].get("source_hash")
    write_fc("fire_restriction_stage.geojson", [{"type": "Feature", "geometry": None, "properties": {
        "id": "pitkin-fire-monitor", "type": "fire_notice_monitor", "status": "unknown", "stage": None,
        "last_checked_at": now(), "last_confirmed_at": None, "max_age_hours": 24,
        "source_hash": digest, "source_changed": None if previous is None else digest != previous,
        "needs_review": True,
        "evidence": make_evidence(src["url"], src["agency"], "unverified", "html_change_monitor",
            notes="Review current dated notices, effective periods and jurisdiction. Page hash is not a restriction stage.")}}])

if __name__ == "__main__":
    main()
