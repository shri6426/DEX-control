import unittest
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import app
from dex.auth import setup_credentials
from config import CREDENTIALS_FILE

class TestAPIEndpoints(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.backup_creds = None
        if CREDENTIALS_FILE.exists():
            self.backup_creds = CREDENTIALS_FILE.read_text()
            CREDENTIALS_FILE.unlink()
        setup_credentials("TestMasterPass123")
        
    def tearDown(self):
        if self.backup_creds:
            CREDENTIALS_FILE.write_text(self.backup_creds)
        elif CREDENTIALS_FILE.exists():
            CREDENTIALS_FILE.unlink()

    def login(self):
        res = self.client.post("/api/v1/auth/login", json={"password": "TestMasterPass123"})
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        return data.get("csrf_token")

    def test_status_endpoint(self):
        res = self.client.get("/api/v1/status")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data["ok"])
        self.assertEqual(data["app_name"], "DEX Control")
        self.assertTrue(data["setup_completed"])

    def test_csrf_protection_on_actions(self):
        # Authenticate first
        csrf = self.login()
        
        # 1. Action without CSRF token should be rejected
        res = self.client.post("/api/v1/actions", json={"action": "set_mute"})
        self.assertEqual(res.status_code, 403)
        data = res.get_json()
        self.assertEqual(data["error"], "INVALID_CSRF")
        
        # 2. Action with valid CSRF token in header should be accepted
        res = self.client.post(
            "/api/v1/actions",
            json={"action": "set_mute"},
            headers={"X-CSRF-Token": csrf}
        )
        self.assertIn(res.status_code, [200, 400])

    def test_volume_endpoints(self):
        csrf = self.login()
        # GET volume
        res = self.client.get("/api/v1/volume")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertIn("volume", data)

        # POST without CSRF should fail
        res = self.client.post("/api/v1/volume", json={"level": 40})
        self.assertEqual(res.status_code, 403)

        # POST with CSRF should succeed
        res = self.client.post("/api/v1/volume", json={"level": 40}, headers={"X-CSRF-Token": csrf})
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data.get("ok"))

    def test_screenshot_traversal_blocked(self):
        self.login()
        res = self.client.get("/api/v1/screenshots/..%2F..%2Fwindows%2Fsystem32%2Fcmd.exe")
        self.assertIn(res.status_code, [400, 404])
        
        res2 = self.client.get("/api/v1/screenshots/non_existent_shot_id")
        self.assertEqual(res2.status_code, 404)

    def test_host_header_validation(self):
        res = self.client.get("/api/v1/status", headers={"Host": "malicious-attacker-site.com"})
        self.assertEqual(res.status_code, 400)
        data = res.get_json()
        self.assertEqual(data["error"], "INVALID_HOST")

if __name__ == "__main__":
    unittest.main()
