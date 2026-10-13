"""Prove the reviewed process/network entry points are denied before discovery."""
import unittest
import offline_tests


class OfflineGuardTests(unittest.TestCase):
    def test_every_guarded_entry_point_refuses_execution(self):
        with offline_tests.offline_guard():
            for obj, name in offline_tests.blocked_calls():
                with self.subTest(name=name), self.assertRaisesRegex(AssertionError, "cannot access network"):
                    getattr(obj, name)()

    def test_ctypes_system_resolution_and_library_loading_are_blocked(self):
        import ctypes
        with offline_tests.offline_guard():
            for loader in [ctypes.CDLL, ctypes.PyDLL, ctypes.cdll.LoadLibrary]:
                with self.subTest(loader=loader), self.assertRaises(AssertionError):
                    loader(None)
            # No library is loaded: symbol denial precedes attribute/handle use.
            unloaded = object.__new__(ctypes.CDLL)
            for name in ["system", b"system"]:
                with self.subTest(name=name), self.assertRaises(AssertionError):
                    unloaded[name]
                with self.assertRaises(AssertionError):
                    unloaded.__getattr__(name)
