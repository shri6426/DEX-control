import unittest
import json
import time
from pathlib import Path
import sys

# Ensure d:\ipad is on sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import app
from dex.auth import (
    setup_credentials, verify_credentials, check_rate_limit,
    record_failed_attempt, clear_rate_limit
)
from config import CREDENTIALS_FILE

class TestAuthentication(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        # Backup credentials if existing
        self.backup_creds = None
        if CREDENTIALS_FILE.exists():
            self.backup_creds = CREDENTIALS_FILE.read_text()
            CREDENTIALS_FILE.unlink()
            
    def tearDown(self):
        if self.backup_creds:
            CREDENTIALS_FILE.write_text(self.backup_creds)
        elif CREDENTIALS_FILE.exists():
            CREDENTIALS_FILE.unlink()

    def test_setup_requires_minimum_length(self):
        ok, msg = setup_credentials("123")
        self.assertFalse(ok)
        self.assertIn("at least 6", msg)

    def test_setup_and_verify_credentials(self):
        ok, msg = setup_credentials("SecurePassword123")
        self.assertTrue(ok)
        
        # Verify correct password
        self.assertTrue(verify_credentials("SecurePassword123"))
        
        # Verify incorrect password fails
        self.assertFalse(verify_credentials("WrongPassword"))

    def test_unauthorized_action_rejected(self):
        setup_credentials("SecurePassword123")
        res = self.client.post("/api/v1/actions", json={"action": "show_desktop"})
        self.assertEqual(res.status_code, 401)
        data = res.get_json()
        self.assertFalse(data["ok"])
        self.assertEqual(data["error"], "UNAUTHORIZED")

    def test_rate_limiting_triggers_after_repeated_failures(self):
        ip = "192.168.1.99"
        clear_rate_limit(ip)
        
        # Record 5 failures
        for _ in range(5):
            record_failed_attempt(ip)
            
        allowed, wait_secs = check_rate_limit(ip)
        self.assertFalse(allowed)
        self.assertGreater(wait_secs, 0)
        clear_rate_limit(ip)

if __name__ == "__main__":
    unittest.main()
