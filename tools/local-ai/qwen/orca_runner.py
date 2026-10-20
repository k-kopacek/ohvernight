"""Optional advisory runner with injected execution and cleanup, no import-time IO.

No concrete execution backend is enabled in Step 1. An approved later pilot must
provide independently inspected Orca/process observation implementations.
"""
import hashlib
import json
import math
import os
import signal
import shlex
import time
import threading
import uuid
from datetime import datetime, timezone
from contextlib import contextmanager
from pathlib import Path
from typing import Protocol

import research_adapter as adapter
from ohvernight_bridge import ADVISORY_LABEL, MAX_BRIDGE_EVIDENCE_BYTES

ADAPTER_VERSION = "step1-owner-gated"
EXPECTED_ADAPTER_SHA256 = "87bccf01f13298ffcc1d68d0c6b393c8d5e135d13807b0bc11307b4c8e6862fd"
MINIMAL_ENVIRONMENT = {"PATH": "/usr/bin:/bin"}
CLEANUP_TIMEOUT_S = 5
COMPLETION_FIELDS = {"event", "run_id", "accepted", "input_sha256", "model", "result",
                     "elapsed_s", "explanations"}
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
    return adapter.installation_home() / ".cache" / "ohvernight-qwen-runs"


class RunFailure(Exception):
    def __init__(self, code):
        self.code = code
        super().__init__(code)


class DeadlineExpired(BaseException):
    """An execution backend's ordinary Exception handler must not swallow this."""


def require_owner_exposure_review():
    adapter.require_owner_exposure_review()


@contextmanager
def execution_deadline(seconds, *, allow_unavailable=False):
    """POSIX main-thread timer; refuse a competing timer rather than overwrite it."""
    if (threading.current_thread() is not threading.main_thread()
            or signal.getitimer(signal.ITIMER_REAL)[0] != 0):
        if allow_unavailable:
            # Cleanup still runs when this thread cannot own a signal timer.
            yield
            return
        raise RunFailure("DEADLINE_UNAVAILABLE")
    previous = signal.getsignal(signal.SIGALRM)

    def expired(signum, frame):
        raise DeadlineExpired()

    previous_mask = None
    signal.signal(signal.SIGALRM, expired)
    try:
        signal.setitimer(signal.ITIMER_REAL, seconds)
        yield
    finally:
        try:
            try:
                previous_mask = signal.pthread_sigmask(signal.SIG_BLOCK, {signal.SIGALRM})
            finally:
                try:
                    signal.setitimer(signal.ITIMER_REAL, 0)
                finally:
                    signal.signal(signal.SIGALRM, previous)
        finally:
            if previous_mask is not None:
                try:
                    # Discard a pending expiration of our timer before restoring
                    # the mask, so it cannot be delivered to the previous handler.
                    if signal.SIGALRM in signal.sigpending():
                        signal.sigwait({signal.SIGALRM})
                finally:
                    signal.pthread_sigmask(signal.SIG_SETMASK, previous_mask)


def structurally_validate_completion(event, run_id, digest, records):
    if not isinstance(event, dict) or event.get("event") != "completed":
        raise RunFailure("NO_COMPLETION")
    if not set(event) <= COMPLETION_FIELDS:
        raise RunFailure("UNEXPECTED_COMPLETION_FIELDS")
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
             "advisory_classification": {"adapter_vocabulary": {
                 "access": row["access"], "camping": row["camping"],
                 "recreation_usefulness": row["recreation_usefulness"]}},
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
        if type(timeout_s) not in (int, float) or not math.isfinite(timeout_s) or timeout_s <= 0:
            raise RunFailure("INVALID_TIMEOUT")
        with execution_deadline(timeout_s):
            if type(raw) is not bytes or len(raw) > MAX_BRIDGE_EVIDENCE_BYTES:
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
            require_owner_exposure_review()
            adapter.configured_endpoint()
            try:
                records = adapter.validate_records(adapter.parse_json(raw))
            except (ValueError, TypeError):
                raise RunFailure("INVALID_INPUT") from None
            root = (Path(run_root) if run_root is not None else default_run_root()).expanduser().resolve()
            repo_root = Path(__file__).resolve().parents[3]
            if root == repo_root or repo_root in root.parents or adapter.repository_root(root) is not None:
                raise RunFailure("RUN_ROOT_INSIDE_REPOSITORY")
            root.mkdir(mode=0o700, parents=True, exist_ok=True)
            if root.stat().st_mode & 0o077:
                raise RunFailure("RUN_ROOT_PERMISSIONS")
            directory = root / run_id
            directory.mkdir(mode=0o700, parents=True, exist_ok=False)
            input_path = directory / "input.json"
            fd = os.open(input_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
            with os.fdopen(fd, "wb") as input_file:
                input_file.write(raw)
            receipt = interface.create_terminal(command=launch_command(python_executable, adapter_path, input_path, run_id),
                                                environment=dict(MINIMAL_ENVIRONMENT), run_id=run_id)
            event = interface.completion(receipt, run_id=run_id, timeout_s=max(0, timeout_s - (time.monotonic() - started)))
            rows = structurally_validate_completion(event, run_id, digest, records)
            structurally_valid = True
    except (adapter.EndpointConfigurationError, adapter.ExposureReviewError) as error:
        code = error.code
    except RunFailure as error:
        code = error.code
    except (TimeoutError, DeadlineExpired):
        code = "TIMEOUT"
    except Exception:
        code = "EXECUTION_FAILED"
    finally:
        try:
            with execution_deadline(CLEANUP_TIMEOUT_S, allow_unavailable=True):
                observed = interface.cleanup(receipt, run_id=run_id)
            if (isinstance(observed, dict) and set(observed) == set(cleanup)
                    and all(type(value) is bool for value in observed.values())):
                cleanup = observed
        except (Exception, DeadlineExpired):
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
            fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
            with os.fdopen(fd, "w", encoding="utf-8") as metadata_file:
                metadata_file.write(json.dumps(metadata, indent=2) + "\n")
        except OSError:
            code = "METADATA_WRITE_FAILED"
            rows = []
            metadata["failure_code"] = code
    return {"succeeded": code is None, "failure_code": code, "advisory_results": rows, "metadata": metadata}
