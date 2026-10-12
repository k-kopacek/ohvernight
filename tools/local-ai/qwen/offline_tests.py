"""Fail closed on network before importing any tests; never launches Orca."""
import socket
import os
import http.client
import urllib.request
import subprocess
import sys
import unittest
from pathlib import Path
from contextlib import ExitStack, contextmanager
from unittest.mock import patch


def forbidden(*args, **kwargs):
    raise AssertionError("Offline Qwen tests cannot access network or launch processes")


def blocked_calls():
    calls = [(socket, "socket"), (socket, "create_connection"), (subprocess, "Popen"),
             (urllib.request, "urlopen"), (http.client.HTTPConnection, "connect")]
    calls.extend((os, name) for name in dir(os)
                 if name in {"system", "fork", "forkpty", "posix_spawn", "posix_spawnp"}
                 or name.startswith("exec") or name.startswith("spawn"))
    return calls


@contextmanager
def offline_guard():
    with ExitStack() as stack:
        for obj, name in blocked_calls():
            stack.enter_context(patch.object(obj, name, forbidden))
        yield


if __name__ == "__main__":
    with offline_guard():
        suite = unittest.defaultTestLoader.discover(str(Path(__file__).with_name("tests")))
        result = unittest.TextTestRunner(verbosity=2).run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)
