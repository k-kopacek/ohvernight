"""Installation-only endpoint checks, no actual network or subprocess calls."""
import contextlib
import io
import ipaddress
import json
import os
import socket
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import research_adapter as adapter


def address(number):
    return str(ipaddress.IPv4Address(number))


def url(host):
    return f"http://{host}:11434/api/chat"


class EndpointTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="qwen-config-test-")
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "endpoint"
        self.original_endpoint_path = adapter.endpoint_setting_path
        p = patch.object(adapter, "endpoint_setting_path", return_value=self.path)
        p.start(); self.addCleanup(p.stop)
        p = patch.object(adapter, "require_owner_exposure_review", return_value="synthetic-owner-review")
        p.start(); self.addCleanup(p.stop)
        p = patch.object(socket, "socket", side_effect=AssertionError("No network"))
        p.start(); self.addCleanup(p.stop)

    def test_allowed_loopback_and_cgnat_boundaries(self):
        for host in [address(2130706433), address(2130706434),
                     address(1681915904), address(1686110207), "[::1]"]:
            for suffix in ["", "\n"]:
                value = url(host)
                self.path.write_text(value + suffix)
                self.assertEqual(adapter.configured_endpoint(), value)

    def test_invalid_hosts_and_url_components(self):
        good = url(address(2130706433))
        cases = [url("localhost"), url(address(1681915903)), url(address(1686110208)),
                 url(address(3232235777)), url(address(167772161)), url(address(2886729729)),
                 url(address(134744072)), url("[::2]"), url("[::1%lo]"), "",
                 good.replace("http:","https:"), good.replace("http:","HTTP:"),
                 good.replace(":11434",":11435"), good.replace(":11434",""),
                 good.replace(":11434",":011434"), good.replace("/api/chat","/api/generate"),
                 good.replace("/api/chat","/api/chat/"), good + "?x=1", good + "?",
                 good + "#fragment", good + "#", " " + good, good + "\n\n",
                 good.replace("//","//user:password@"), good.replace("//","//@"),
                 "http://[broken:11434/api/chat", "x"*1025]
        for value in cases:
            with self.subTest(value=value):
                self.path.write_text(value)
                with self.assertRaises(adapter.EndpointConfigurationError) as caught:
                    adapter.configured_endpoint()
                self.assertEqual(caught.exception.code,"ENDPOINT_SETTING_INVALID")
        self.path.write_bytes(b"\xff")
        with self.assertRaises(adapter.EndpointConfigurationError) as caught:adapter.configured_endpoint()
        self.assertEqual(caught.exception.code,"ENDPOINT_SETTING_INVALID")

    def test_missing_unreadable_and_repository_setting(self):
        with self.assertRaises(adapter.EndpointConfigurationError) as caught:adapter.configured_endpoint()
        self.assertEqual(caught.exception.code,"ENDPOINT_SETTING_MISSING")
        self.path.write_text(url(address(2130706433)))
        with patch.object(adapter.os,"open",side_effect=PermissionError()):
            with self.assertRaises(adapter.EndpointConfigurationError) as caught:adapter.configured_endpoint()
        self.assertEqual(caught.exception.code,"ENDPOINT_SETTING_UNREADABLE")
        repository = Path(self.temp.name) / "synthetic-repository"
        repository.mkdir(); (repository / ".git").mkdir()
        with patch.object(adapter,"endpoint_setting_path",return_value=repository / "endpoint"):
            with self.assertRaises(adapter.EndpointConfigurationError) as caught:adapter.configured_endpoint()
        self.assertEqual(caught.exception.code,"ENDPOINT_SETTING_IN_REPOSITORY")

    def test_missing_or_invalid_configuration_precedes_any_request(self):
        for value in [None,"invalid"]:
            if value is not None:self.path.write_text(value)
            output=io.StringIO()
            with patch("sys.argv",["adapter","--input","unused","--run-id","offline"]), \
                    patch.object(adapter.urllib.request,"Request",side_effect=AssertionError("Must not request")), \
                    contextlib.redirect_stdout(output):
                self.assertEqual(adapter.main(),1)
            event=json.loads(output.getvalue())
            self.assertEqual(event["event"],"failed")
            self.assertEqual(event["failure_code"],"ENDPOINT_SETTING_MISSING" if value is None else "ENDPOINT_SETTING_INVALID")

    def test_redirects_and_proxies_stay_refused(self):
        with self.assertRaisesRegex(ValueError,"redirect refused"):
            adapter.NoRedirect().redirect_request(None,None,302,"",{},url(address(134744072)))
        opener=adapter.urllib.request.build_opener(adapter.urllib.request.ProxyHandler({}),adapter.NoRedirect())
        self.assertFalse(any(isinstance(handler,adapter.urllib.request.ProxyHandler) and handler.proxies for handler in opener.handlers))

    def test_resolution_errors_and_staged_adapter_copy(self):
        with patch.object(Path,"resolve",side_effect=RuntimeError("symlink loop")):
            with self.assertRaises(adapter.EndpointConfigurationError) as caught:adapter.configured_endpoint()
        self.assertEqual(caught.exception.code,"ENDPOINT_SETTING_UNREADABLE")
        value=url(address(2130706433)); self.path.write_text(value)
        # The validated launch recipe can stage the adapter in a private temp
        # directory; that location must not make '/' count as a repository.
        with patch.object(adapter,"__file__",str(Path(self.temp.name)/"research_adapter.py")):
            self.assertEqual(adapter.configured_endpoint(),value)
            repository = Path(self.temp.name) / "other-checkout"
            repository.mkdir(); (repository / ".git").mkdir()
            with patch.object(adapter, "endpoint_setting_path", return_value=repository / "setting"):
                with self.assertRaises(adapter.EndpointConfigurationError) as caught:
                    adapter.configured_endpoint()
            self.assertEqual(caught.exception.code, "ENDPOINT_SETTING_IN_REPOSITORY")

    def test_parent_child_home_resolution_ignores_home_environment(self):
        account_home = adapter.installation_home()
        with patch.dict(os.environ, {"HOME": self.temp.name}):
            self.assertEqual(adapter.installation_home(), account_home)
            self.assertEqual(self.original_endpoint_path().parents[2], account_home)
            self.assertEqual(adapter.exposure_review_setting_path().parents[2], account_home)

    def test_endpoint_symlink_outside_git_writable_and_wrong_owner_rejected(self):
        target = self.path.with_name("outside-git-endpoint")
        target.write_text(url(address(2130706433)))
        self.path.symlink_to(target)
        with self.assertRaises(adapter.EndpointConfigurationError) as caught:
            adapter.configured_endpoint()
        self.assertEqual(caught.exception.code, "ENDPOINT_SETTING_UNSAFE")
        self.path.unlink()
        self.path.write_text(target.read_text())
        for mode in [0o666, 0o620, 0o602]:
            self.path.chmod(mode)
            with self.subTest(mode=mode), self.assertRaises(adapter.EndpointConfigurationError) as caught:
                adapter.configured_endpoint()
            self.assertEqual(caught.exception.code, "ENDPOINT_SETTING_UNSAFE")
        self.path.chmod(0o600)
        uid = adapter.os.getuid()
        with patch.object(adapter.os, "getuid", return_value=uid + 1):
            with self.assertRaises(adapter.EndpointConfigurationError) as caught:
                adapter.configured_endpoint()
        self.assertEqual(caught.exception.code, "ENDPOINT_SETTING_UNSAFE")
        with patch.object(adapter, "endpoint_setting_path", return_value=self.path.parent):
            with self.assertRaises(adapter.EndpointConfigurationError) as caught:
                adapter.configured_endpoint()
        self.assertEqual(caught.exception.code, "ENDPOINT_SETTING_UNSAFE")

    def test_missing_account_home_becomes_oserror_and_cli_event(self):
        with patch.object(adapter.pwd, "getpwuid", side_effect=KeyError("synthetic missing uid")):
            with self.assertRaisesRegex(OSError, "Account home unavailable"):
                adapter.installation_home()
            # Restore the genuine path resolver, bypassing this class's setting mock.
            output = io.StringIO()
            with patch.object(adapter, "endpoint_setting_path", self.original_endpoint_path), \
                    patch("sys.argv", ["adapter", "--input", "unused", "--run-id", "offline"]), \
                    contextlib.redirect_stdout(output):
                self.assertEqual(adapter.main(), 1)
            self.assertEqual(json.loads(output.getvalue()),
                             {"event": "failed", "run_id": "offline",
                              "failure_code": "ENDPOINT_SETTING_UNREADABLE"})


if __name__ == "__main__":unittest.main()
