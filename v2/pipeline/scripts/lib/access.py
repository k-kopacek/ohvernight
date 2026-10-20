"""MVUM designation for the entire trip; not snow, passability, or sleeping permission."""
import datetime as dt
import re

VEHICLES = {"passenger_car": ("passengervehicle", "passengervehicle_datesopen"),
            "high_clearance": ("highclearancevehicle", "highclearancevehicle_datesopen"),
            "motorhome": ("motorhome", "motorhome_datesopen")}
SYMBOLS = {1: ("all_vehicles", "yearlong"), 2: ("all_vehicles", "seasonal"),
           3: ("highway_legal", "yearlong"), 4: ("highway_legal", "seasonal"),
           11: ("special_designation", "yearlong"), 12: ("special_designation", "seasonal")}

def trip_dates(arrive, depart):
    start, end = dt.date.fromisoformat(arrive), dt.date.fromisoformat(depart)
    if end < start or (end-start).days > 366:
        raise ValueError("Trip must be ordered and at most 366 days")
    return [start + dt.timedelta(days=i) for i in range((end-start).days + 1)]

def parse_windows(value):
    if not value or not str(value).strip():
        return None
    text = str(value).strip()
    if text.lower() in {"yearlong", "year-round", "year round", "all year"}:
        return [((1, 1), (12, 31))]
    parts = re.split(r"\s*[;,]\s*", text)
    windows = []
    for part in parts:
        match = re.fullmatch(r"(\d{1,2})/(\d{1,2})\s*[-–]\s*(\d{1,2})/(\d{1,2})", part)
        if not match:
            return None
        a,b,c,d = map(int, match.groups())
        try:
            dt.date(2000,a,b); dt.date(2000,c,d)
        except ValueError:
            return None
        windows.append(((a,b),(c,d)))
    return windows

def evaluate_access(props, arrive, depart, vehicle):
    days = trip_dates(arrive, depart)
    key, dates_key = VEHICLES[vehicle]
    try:
        symbol = int(props.get("symbol"))
    except (TypeError, ValueError):
        return "unknown", "missing_or_invalid_symbol"
    if symbol not in SYMBOLS:
        return "unknown", "context_route_not_designated_for_this_check"
    permission = str(props.get(key) or "").strip().lower()
    if permission in {"closed", "no", "not allowed"}:
        return "restricted", "vehicle_not_designated"
    if permission != "open":
        return "unknown", "vehicle_designation_missing_or_unrecognized"
    raw = str(props.get(dates_key) or "").strip()
    windows = parse_windows(raw)
    if windows is None:
        if raw:
            return "unknown", "unparsed_vehicle_dates"
        if SYMBOLS[symbol][1] != "yearlong":
            return "unknown", "seasonal_dates_missing"
        windows = [((1,1),(12,31))]
    def includes(day):
        md = day.month, day.day
        return any((a <= md <= b) if a <= b else (md >= a or md <= b) for a,b in windows)
    if not all(includes(day) for day in days):
        return "restricted", "outside_designated_vehicle_season"
    return "designated_open", "mvum_designation_only_conditions_unknown"
