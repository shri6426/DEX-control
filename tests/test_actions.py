import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dex.actions import execute_action, get_action_history
from dex.windows_controls import APPROVED_SHORTCUTS, send_shortcut

class TestActions(unittest.TestCase):
    def test_unknown_action_rejected(self):
        res = execute_action("arbitrary_command_exec", {"cmd": "calc.exe"})
        self.assertFalse(res["ok"])
        self.assertEqual(res["error"], "UNKNOWN_ACTION")

    def test_volume_validation(self):
        # Missing level
        res = execute_action("set_volume", {})
        self.assertFalse(res["ok"])
        self.assertEqual(res["error"], "MISSING_PARAM")
        
        # Invalid non-integer level
        res = execute_action("set_volume", {"level": "invalid_string"})
        self.assertFalse(res["ok"])
        self.assertEqual(res["error"], "INVALID_PARAM")

    def test_lock_pc_requires_explicit_confirmation(self):
        # Attempt without confirmation
        res = execute_action("lock_pc", {})
        self.assertFalse(res["ok"])
        self.assertEqual(res["error"], "CONFIRMATION_REQUIRED")

    def test_shortcut_allowlist_enforcement(self):
        # Unapproved shortcut should fail
        res = send_shortcut("Ctrl+Alt+Del")
        self.assertFalse(res["ok"])
        self.assertIn("not in the approved allowlist", res["error"])
        
        # Verify approved shortcuts list contains all required keys
        expected = ["Win+E", "Win+Shift+S", "Ctrl+Shift+Esc", "Alt+Tab", "Win+D", "Ctrl+C", "Ctrl+V", "Ctrl+Z", "Ctrl+Shift+T"]
        for s in expected:
            self.assertIn(s, APPROVED_SHORTCUTS)

    def test_history_logging(self):
        execute_action("set_volume", {"level": 30})
        history = get_action_history()
        self.assertGreater(len(history), 0)
        latest = history[0]
        self.assertEqual(latest["action"], "Volume Set")

if __name__ == "__main__":
    unittest.main()
