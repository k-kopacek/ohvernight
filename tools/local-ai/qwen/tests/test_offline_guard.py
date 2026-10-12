"""Prove all supported process/network entry points are denied before discovery."""
import unittest
import offline_tests


class OfflineGuardTests(unittest.TestCase):
    def test_every_guarded_entry_point_refuses_execution(self):
        with offline_tests.offline_guard():
            for obj, name in offline_tests.blocked_calls():
                with self.subTest(name=name), self.assertRaisesRegex(AssertionError, "cannot access network"):
                    getattr(obj, name)()
