"""Optional advisory runner with injected execution and cleanup, no import-time IO.

No concrete execution backend is enabled in Step 1. An approved later pilot must
provide independently inspected Orca/process observation implementations.
"""
import hashlib
import json
import shlex
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Protocol

import research_adapter as adapter
from ohvernight_bridge import ADVISORY_LABEL, MAX_BRIDGE_BYTES

ADAPTER_VERSION = "step1-installation-endpoint"
EXPECTED_ADAPTER_SHA256 = "3853972009830df50e0c0a94789d24f4d83ad0d34472fe3ede8e666f69c2f4e5"
MINIMAL_ENVIRONMENT = {"PATH": "/usr/bin:/bin"}
METADATA_FIELDS = {
    "run_id", "utc_start", "utc_end", "adapter_sha256", "adapter_version", "model",
    "endpoint_identifier", "input_sha256", "record_ids", "source_ids", "input_bytes",
    "input_tokens", "duration_s", "structural_validation_result", "failure_code",
    "cleanup_result", "review_disposition",
}


class ExecutionInterface(Protocol):
    """Implementations must use exact owned handles, never retry or infer cleanup.

    create_terminal must invoke `orca terminal create --command` with the command
    and minimal environment supplied here. It must preserve any residual handle
    on launch failure so cleanup can recover it without relaunching.
    completion waits for the exact run, returning its completion event.
    cleanup closes only the owned terminal, confirms absence via inventory, and
    independently confirms the exact adapter process has exited; it must run
    even if create_terminal fails and retain ownership internally in that case.
    """
    def create_terminal(self, *, command, environment, run_id): ...
    def completion(self, receipt, *, run_id, timeout_s): ...
    def cleanup(self, receipt, *, run_id): ...


def launch_command(python_executable, adapter_path, input_path, run_id):
    return shlex.join([
        "env", "-i", "PATH=/usr/bin:/bin", str(python_executable), "-I", "-B",
        str(adapter_path), "--input", str(input_path), "--run-id", run_id,
    ])


def default_run_root():
    return Path.home() / ".cache" / "ohvernight-qwen-runs"


class RunFailure(Exception):
    def __init__(self, code):
        self.code = code
        super().__init__(code)


def structurally_validate_completion(event, run_id, digest, records):
    if not isinstance(event, dict) or event.get("event") != "completed":
        raise RunFailure("NO_COMPLETION")
    if event.get("run_id") != run_id:
        raise RunFailure("RUN_ID_MISMATCH")
    if event.get("accepted") is not True:
        raise RunFailure("COMPLETION_REJECTED")
    if event.get("input_sha256") != digest:
        raise RunFailure("INPUT_DIGEST_MISMATCH")
    if event.get("model") != adapter.MODEL:
        raise RunFailure("MODEL_MISMATCH")
    result = event.get("result")
    try:
        # Completion is emitted only after the recovered adapter has accepted a
        # done/stop response. Recheck its result contract independently here.
        adapter.validate_response({"model": adapter.MODEL, "done": True, "done_reason": "stop",
                                   "message": {"role": "assistant", "content": json.dumps(result)}}, records)
    except (ValueError, TypeError):
        raise RunFailure("INVALID_RESULT") from None
    return [{"record_id": row["id"], "source_ids": list(row["source_ids"]),
             "advisory_classification": {"access": row["access"], "camping": row["camping"],
                                          "recreation_usefulness": row["recreation_usefulness"]},
             "advisory_notes": row["reason"], "advisory_label": ADVISORY_LABEL}
            for row in result["results"]]


def run_advisory(raw, interface, *, run_root=None, python_executable="python3", timeout_s=150):
    """Run only supplied adapter-shaped bytes. Never accepts canonical outputs.

    No token measurement exists: input_tokens stays null. This function is
    optional and is never invoked by CI except with the fake interface.
    Metadata has a fixed allowlist; exceptions and receipts are not retained.
    """
    run_id = uuid.uuid4().hex
    started = time.monotonic()
    utc_start = datetime.now(timezone.utc).isoformat()
    receipt = None
    rows = []
    records = []
    code = None
    cleanup = {"terminal_closed": False, "process_exited": False}
    structurally_valid = False
    adapter_path = Path(__file__).with_name("research_adapter.py")
    adapter_hash = None
    digest = hashlib.sha256(raw).hexdigest() if type(raw) is bytes else None
    directory = None
    try:
        if type(raw) is not bytes or len(raw) > MAX_BRIDGE_BYTES:
            raise RunFailure("INVALID_INPUT_BYTES")
        try:
            adapter_hash = hashlib.sha256(adapter_path.read_bytes()).hexdigest()
        except OSError:
            raise RunFailure("ADAPTER_UNAVAILABLE") from None
        if adapter_hash != EXPECTED_ADAPTER_SHA256:
            raise RunFailure("ADAPTER_HASH_MISMATCH")
        # Validate the one installation setting before launching any process.
        # The child independently reads the same fixed file; never pass the URL
        # in its command, environment, output metadata, or caller arguments.
        adapter.configured_endpoint()
        try:
            records = adapter.validate_records(adapter.parse_json(raw))
        except (ValueError, TypeError):
            raise RunFailure("INVALID_INPUT") from None
        root = (Path(run_root) if run_root is not None else default_run_root()).expanduser().resolve()
        repo_root = Path(__file__).resolve().parents[3]
        if root == repo_root or repo_root in root.parents:
            raise RunFailure("RUN_ROOT_INSIDE_REPOSITORY")
        directory = root / run_id
        directory.mkdir(mode=0o700, parents=True, exist_ok=False)
        input_path = directory / "input.json"
        input_path.write_bytes(raw)
        input_path.chmod(0o600)
        receipt = interface.create_terminal(command=launch_command(python_executable, adapter_path, input_path, run_id),
                                            environment=dict(MINIMAL_ENVIRONMENT), run_id=run_id)
        event = interface.completion(receipt, run_id=run_id, timeout_s=timeout_s)
        rows = structurally_validate_completion(event, run_id, digest, records)
        structurally_valid = True
    except adapter.EndpointConfigurationError as error:
        code = error.code
    except RunFailure as error:
        code = error.code
    except TimeoutError:
        code = "TIMEOUT"
    except Exception:
        code = "EXECUTION_FAILED"
    finally:
        try:
            observed = interface.cleanup(receipt, run_id=run_id)
            if (isinstance(observed, dict) and set(observed) == set(cleanup)
                    and all(type(value) is bool for value in observed.values())):
                cleanup = observed
        except Exception:
            pass
        if not all(cleanup.values()) and code is None:
            code = "CLEANUP_FAILED"
    if code is not None:
        rows = []
    metadata = {
        "run_id": run_id, "utc_start": utc_start, "utc_end": datetime.now(timezone.utc).isoformat(),
        "adapter_sha256": adapter_hash, "adapter_version": ADAPTER_VERSION, "model": adapter.MODEL,
        "endpoint_identifier": "local-evidence-service", "input_sha256": digest,
        "record_ids": [r["id"] for r in records], "source_ids": [r["source_ids"] for r in records],
        "input_bytes": len(raw) if type(raw) is bytes else None, "input_tokens": None,
        "duration_s": round(time.monotonic() - started, 3),
        "structural_validation_result": structurally_valid, "failure_code": code,
        "cleanup_result": cleanup, "review_disposition": "unreviewed",
    }
    if directory is not None:
        try:
            path = directory / "metadata.json"
            path.write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
            path.chmod(0o600)
        except OSError:
            code = "METADATA_WRITE_FAILED"
            rows = []
            metadata["failure_code"] = code
    return {"succeeded": code is None, "failure_code": code, "advisory_results": rows, "metadata": metadata}
