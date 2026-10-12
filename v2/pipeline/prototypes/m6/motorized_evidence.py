"""Research-only normalization for source MVUM designation strings."""

from __future__ import annotations

from datetime import date
import re
from typing import Any, Mapping


_DATE_WINDOW = re.compile(r"(?P<sm>\d{2})/(?P<sd>\d{2})-(?P<em>\d{2})/(?P<ed>\d{2})\Z")
_VEHICLE_FIELDS = {
    "passenger_vehicle": ("passengervehicle", "passengervehicle_datesopen"),
    "high_clearance_vehicle": ("highclearancevehicle", "highclearancevehicle_datesopen"),
    "truck": ("truck", "truck_datesopen"),
    "bus": ("bus", "bus_datesopen"),
    "motorhome": ("motorhome", "motorhome_datesopen"),
    "four_wd_over_50_inches": ("fourwd_gt50inches", "fourwd_gt50_datesopen"),
    "two_wd_over_50_inches": ("twowd_gt50inches", "twowd_gt50_datesopen"),
    "tracked_ohv_over_50_inches": ("tracked_ohv_gt50inches", "tracked_ohv_gt50_datesopen"),
    "other_ohv_over_50_inches": ("other_ohv_gt50inches", "other_ohv_gt50_datesopen"),
    "atv": ("atv", "atv_datesopen"),
    "motorcycle": ("motorcycle", "motorcycle_datesopen"),
    "other_wheeled_ohv": ("otherwheeled_ohv", "otherwheeled_ohv_datesopen"),
    "tracked_ohv_under_50_inches": ("tracked_ohv_lt50inches", "tracked_ohv_lt50_datesopen"),
    "other_ohv_under_50_inches": ("other_ohv_lt50inches", "other_ohv_lt50_datesopen"),
}


def _attributes(record: Mapping[str, Any]) -> Mapping[str, Any]:
    """Accept an ArcGIS feature or its attributes object."""
    attributes = record.get("attributes", record)
    if not isinstance(attributes, Mapping):
        raise TypeError("record attributes must be a mapping")
    return attributes


def parse_date_windows(raw: Any) -> dict[str, Any]:
    """Parse only the exact month/day shapes in MVUM samples; always retain raw input."""
    if raw is None or raw == "":
        return {"raw": raw, "state": "NO_WINDOW_STATED", "windows": []}
    if not isinstance(raw, str):
        return {"raw": raw, "state": "UNPARSEABLE", "windows": []}

    parsed: list[dict[str, Any]] = []
    for raw_window in raw.split(","):
        match = _DATE_WINDOW.fullmatch(raw_window)
        if match is None:
            return {"raw": raw, "state": "UNPARSEABLE", "windows": []}
        start = (int(match["sm"]), int(match["sd"]))
        end = (int(match["em"]), int(match["ed"]))
        try:
            date(2000, *start)
            date(2000, *end)
        except ValueError:
            return {"raw": raw, "state": "UNPARSEABLE", "windows": []}
        parsed.append({
            "raw": raw_window,
            "start": {"month": start[0], "day": start[1]},
            "end": {"month": end[0], "day": end[1]},
        })
    return {"raw": raw, "state": "PARSED", "windows": parsed}


def _source_feature(attributes: Mapping[str, Any], source_layer: str | None) -> dict[str, Any]:
    return {
        "source_layer": source_layer,
        "objectid": attributes.get("objectid"),
        "globalid": attributes.get("globalid"),
        "route_number": attributes.get("id"),
        "rte_cn": attributes.get("rte_cn"),
    }


def normalize_record(
    record: Mapping[str, Any],
    management_intent: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Preserve MVUM designation claims and, when supplied, separate trail-intent claims."""
    attributes = _attributes(record)
    source_layer = record.get("source_layer")
    source_feature = _source_feature(attributes, source_layer if isinstance(source_layer, str) else None)
    vehicle_designations: dict[str, Any] = {}
    for vehicle_class, (designation_field, dates_field) in _VEHICLE_FIELDS.items():
        vehicle_designations[vehicle_class] = {
            "designation_raw": attributes.get(designation_field),
            "dates_open": parse_date_windows(attributes.get(dates_field)),
        }

    source_claims = [{
        "kind": "mvum_legal_designation",
        "source_feature": source_feature,
        "route_label": attributes.get("id"),
        "name": attributes.get("name"),
        "symbol": attributes.get("symbol"),
        "vehicle_designations": vehicle_designations,
    }]
    if management_intent is not None:
        source_claims.append({
            "kind": "trail_management_intent",
            "source_feature": {
                "source_layer": management_intent.get("source_layer"),
                "id": management_intent.get("id"),
                "trail_number": management_intent.get("trail_number"),
            },
            "activities": management_intent.get("activities"),
        })

    return {"source_claims": source_claims, "current_condition": "unknown"}


def route_number_key(value: Any) -> tuple[str, ...] | None:
    """Return a comparison key that removes numeric zero-padding but keeps suffixes."""
    if not isinstance(value, (str, int)) or isinstance(value, bool):
        return None
    text = str(value).strip()
    if not text:
        return None
    parts = text.split(".")
    normalized: list[str] = []
    for part in parts:
        if not part:
            return None
        if part.isdigit():
            normalized.append(str(int(part)))
        else:
            normalized.append(part.upper())
    return tuple(normalized)


def join_candidate(
    mvum_record: Mapping[str, Any],
    management_intent: Mapping[str, Any],
) -> dict[str, Any] | None:
    """Return a route-number candidate with both source claims kept side by side."""
    attributes = _attributes(mvum_record)
    mvum_route = attributes.get("id")
    trail_route = management_intent.get("trail_number")
    mvum_key = route_number_key(mvum_route)
    if mvum_key is None or mvum_key != route_number_key(trail_route):
        return None
    normalized = normalize_record(mvum_record, management_intent=management_intent)
    return {
        "match_basis": "normalized_route_number_candidate",
        "mvum_route_number_raw": mvum_route,
        "trail_route_number_raw": trail_route,
        "source_claims": normalized["source_claims"],
        "current_condition": "unknown",
    }


def date_window_status(record: Mapping[str, Any], vehicle_class: str, day: date) -> str:
    """Return a legal-designation lookup, not permission, openness, or rideability."""
    if not isinstance(day, date):
        raise TypeError("day must be a datetime.date")
    normalized = record if "source_claims" in record else normalize_record(record)
    claims = normalized.get("source_claims", [])
    mvum = next((claim for claim in claims if claim.get("kind") == "mvum_legal_designation"), None)
    designation = (mvum or {}).get("vehicle_designations", {}).get(vehicle_class)
    windows = (designation or {}).get("dates_open", {})
    state = windows.get("state")
    if state == "UNPARSEABLE":
        return "UNPARSEABLE"
    if state != "PARSED":
        return "NO_WINDOW_STATED"

    month_day = (day.month, day.day)
    for window in windows["windows"]:
        start = (window["start"]["month"], window["start"]["day"])
        end = (window["end"]["month"], window["end"]["day"])
        inside = start <= month_day <= end if start <= end else month_day >= start or month_day <= end
        if inside:
            return "INSIDE_WINDOW"
    return "OUTSIDE_WINDOW"
