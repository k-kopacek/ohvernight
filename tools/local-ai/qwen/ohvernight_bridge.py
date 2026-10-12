"""One-way selected public input conversion. Never emits canonical data."""
import copy
import json

import research_adapter as adapter

ADVISORY_LABEL = "AI-assisted advisory — structurally validated, factually unverified"
# Serialized evidence ONLY; excludes system prompt and chat template.
# This 3,072-byte cap is NOT the 3,072-token target or permission for inference.
MAX_BRIDGE_EVIDENCE_BYTES = 3072
REQUIRED = {"id", "access_status", "camping_permission", "source_ids"}
OPTIONAL = {"ownership", "name", "restriction_freshness", "recreation_evidence"}


class BridgeError(ValueError):
    def __init__(self, code):
        self.code = code
        super().__init__(code)


def prepare_advisory_input(records):
    """Accept only explicitly selected fields; do not accept whole GeoJSON records.

    Positive values must already have passed the canonical evidence contract.
    This projection converter cannot establish the legitimacy of that assessment.
    """
    if not isinstance(records, list) or not 1 <= len(records) <= 8:
        raise BridgeError("INVALID_RECORDS")
    mapped = []
    for record in records:
        if not isinstance(record, dict) or not REQUIRED <= set(record) or not set(record) <= REQUIRED | OPTIONAL:
            raise BridgeError("INVALID_FIELDS")
        access = record["access_status"]
        camping = record["camping_permission"]
        if access == "restricted":
            raise BridgeError("UNREPRESENTABLE_ACCESS_RESTRICTED")
        if type(access) is not str or access not in {"unknown", "designated_open"}:
            raise BridgeError("INVALID_ACCESS")
        if type(camping) is not str or camping not in {"unknown", "supported_for_trip"}:
            raise BridgeError("INVALID_CAMPING")
        row = {key: copy.deepcopy(value) for key, value in record.items() if key in OPTIONAL | {"id", "source_ids"}}
        row["access"] = {"unknown": "unknown", "designated_open": "allowed"}[access]
        row["camping"] = {"unknown": "unknown", "supported_for_trip": "allowed"}[camping]
        mapped.append(row)
    try:
        adapter.validate_records(mapped)
    except (ValueError, TypeError) as error:
        raise BridgeError("INVALID_ADAPTER_INPUT") from error
    raw = json.dumps(mapped).encode("utf-8")
    if len(raw) > MAX_BRIDGE_EVIDENCE_BYTES:
        raise BridgeError("BYTE_GUARD_EXCEEDED")
    return raw
