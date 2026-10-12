"""Block reviewed network/process entry points before discovery; not a sandbox."""
import socket
import _socket
import ctypes
import multiprocessing.process
import os
import http.client
import urllib.request
import subprocess
import sys
import unittest
from pathlib import Path
from contextlib import ExitStack, contextmanager
from unittest.mock import patch

try:
    import _posixsubprocess
except ImportError:
    _posixsubprocess = None


def forbidden(*args, **kwargs):
    raise AssertionError("Offline Qwen tests cannot access network or launch processes")


def blocked_calls():
    calls = [(socket, "socket"), (_socket, "socket"), (socket, "create_connection"),
             (subprocess, "Popen"), (multiprocessing.process.BaseProcess, "start"),
             (ctypes.CDLL, "__init__"),
             (urllib.request, "urlopen"), (http.client.HTTPConnection, "connect")]
    calls.extend((os, name) for name in dir(os)
                 if name in {"system", "fork", "forkpty", "posix_spawn", "posix_spawnp"}
                 or name.startswith("exec") or name.startswith("spawn"))
    if _posixsubprocess is not None:
        calls.append((_posixsubprocess, "fork_exec"))
    return calls


@contextmanager
def offline_guard():
    with ExitStack() as stack:
        for obj, name in blocked_calls():
            stack.enter_context(patch.object(obj, name, forbidden))
        for name in ("__getattr__", "__getitem__"):
            original = getattr(ctypes.CDLL, name)
            def guarded_symbol(self, symbol, *args, _original=original, **kwargs):
                if symbol in ("system", b"system"):
                    forbidden()
                return _original(self, symbol, *args, **kwargs)
            stack.enter_context(patch.object(ctypes.CDLL, name, guarded_symbol))
        yield


if __name__ == "__main__":
    with offline_guard():
        suite = unittest.defaultTestLoader.discover(str(Path(__file__).with_name("tests")))
        result = unittest.TextTestRunner(verbosity=2).run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)
