"""Fail closed on network before importing any tests; never launches Orca."""
import socket
import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import patch


def forbidden(*args, **kwargs):
    raise AssertionError("Offline Qwen tests cannot access network or launch processes")


if __name__ == "__main__":
    with patch.object(socket, "socket", forbidden), patch.object(socket, "create_connection", forbidden), \
            patch.object(subprocess, "Popen", forbidden):
        suite = unittest.defaultTestLoader.discover(str(Path(__file__).with_name("tests")))
        result = unittest.TextTestRunner(verbosity=2).run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)
