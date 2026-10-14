import unittest
import threading
import time
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dex.macros import execute_macro, _macro_execution_lock
from dex.app_launcher import AppRegistry
from dex.actions import execute_action

class TestConcurrencyAndExecution(unittest.TestCase):
    def test_macro_overlapping_execution_prevented(self):
        # Acquire macro lock manually to simulate an active running macro
        acquired = _macro_execution_lock.acquire(blocking=False)
        self.assertTrue(acquired)
        try:
            # Another execution attempt must be rejected immediately
            registry = AppRegistry()
            res = execute_macro("coding_setup", registry, {})
            self.assertFalse(res["ok"])
            self.assertIn("Another macro is currently executing", res["error"])
        finally:
            _macro_execution_lock.release()

    def test_rapid_volume_requests(self):
        # Rapid volume commands should execute safely without deadlock
        results = []
        for v in [20, 22, 24, 26, 28]:
            res = execute_action("set_volume", {"level": v})
            results.append(res["ok"])
        self.assertTrue(all(results))

    def test_app_registry_all_required_present(self):
        reg = AppRegistry()
        apps = {a["id"]: a for a in reg.get_registered_apps()}
        required = ["antigravity", "chrome", "terminal", "powershell", "whatsapp", "explorer", "taskmgr", "settings", "snipping"]
        for req in required:
            self.assertIn(req, apps)
            self.assertIn("name", apps[req])
            self.assertIn("category", apps[req])

if __name__ == "__main__":
    unittest.main()
