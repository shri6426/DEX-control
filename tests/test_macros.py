import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dex.macros import validate_macro_definition, MAX_ACTIONS_PER_MACRO, MAX_DELAY_SECONDS

class TestMacros(unittest.TestCase):
    def test_valid_macro_definition(self):
        macro = {
            "name": "Dev Startup",
            "actions": [
                {"type": "set_volume", "level": 25},
                {"type": "delay", "seconds": 0.5},
                {"type": "launch_app", "target": "antigravity"}
            ]
        }
        valid, msg = validate_macro_definition(macro)
        self.assertTrue(valid, msg)

    def test_empty_actions_rejected(self):
        macro = {"name": "Empty", "actions": []}
        valid, msg = validate_macro_definition(macro)
        self.assertFalse(valid)
        self.assertIn("at least one action", msg)

    def test_max_actions_limit_enforced(self):
        too_many = [{"type": "delay", "seconds": 0.1}] * (MAX_ACTIONS_PER_MACRO + 1)
        macro = {"name": "Too Many", "actions": too_many}
        valid, msg = validate_macro_definition(macro)
        self.assertFalse(valid)
        self.assertIn("cannot exceed", msg)

    def test_delay_limits_enforced(self):
        # Exceeds max individual delay
        macro = {
            "name": "Long Wait",
            "actions": [{"type": "delay", "seconds": MAX_DELAY_SECONDS + 1}]
        }
        valid, msg = validate_macro_definition(macro)
        self.assertFalse(valid)
        self.assertIn("must be between 0.1 and", msg)

    def test_unapproved_action_type_rejected(self):
        macro = {
            "name": "Malicious Macro",
            "actions": [{"type": "run_shell_script", "script": "del C:\\"}]
        }
        valid, msg = validate_macro_definition(macro)
        self.assertFalse(valid)
        self.assertIn("not permitted", msg)

if __name__ == "__main__":
    unittest.main()
