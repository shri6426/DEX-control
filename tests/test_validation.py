import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dex.settings import validate_and_register_custom_app
from dex.profiles import load_profiles, reset_to_defaults
from dex.app_launcher import AppRegistry

class TestValidation(unittest.TestCase):
    def test_custom_app_registration_requires_existing_file(self):
        ok, msg = validate_and_register_custom_app(
            "fake_app",
            "Fake Game",
            "C:\\non_existent_folder\\fake_game.exe"
        )
        self.assertFalse(ok)
        self.assertIn("does not exist", msg)

    def test_custom_app_registration_rejects_non_executable(self):
        # Point to a text file that exists
        readme = Path(__file__).resolve().parent.parent / "requirements.txt"
        ok, msg = validate_and_register_custom_app(
            "bad_ext",
            "Not An Exe",
            str(readme)
        )
        self.assertFalse(ok)
        self.assertIn("must be an executable", msg)

    def test_default_profiles_integrity(self):
        profiles_data = reset_to_defaults()
        self.assertIn("profiles", profiles_data)
        self.assertIn("general", profiles_data["profiles"])
        self.assertIn("coding", profiles_data["profiles"])
        self.assertIn("gaming", profiles_data["profiles"])
        self.assertIn("media", profiles_data["profiles"])
        
        # Verify General has at least 8 buttons
        general_btns = profiles_data["profiles"]["general"]["buttons"]
        self.assertGreaterEqual(len(general_btns), 8)

    def test_app_registry_detection(self):
        registry = AppRegistry()
        apps = registry.get_registered_apps()
        self.assertIsInstance(apps, list)
        app_ids = [a["id"] for a in apps]
        
        # All required apps must be in the registry
        for req in ["antigravity", "chrome", "terminal", "powershell", "whatsapp", "explorer", "taskmgr", "settings", "snipping"]:
            self.assertIn(req, app_ids)

if __name__ == "__main__":
    unittest.main()
