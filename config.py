import os
import secrets
import socket
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
SCREENSHOTS_DIR = DATA_DIR / "screenshots"
CONFIG_FILE = DATA_DIR / "settings.json"
CREDENTIALS_FILE = DATA_DIR / "credentials.json"
PROFILES_FILE = DATA_DIR / "profiles.json"
MACROS_FILE = DATA_DIR / "macros.json"
SECRET_KEY_FILE = DATA_DIR / "secret_key.bin"

DATA_DIR.mkdir(parents=True, exist_ok=True)
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)

def get_or_create_secret_key() -> bytes:
    """Load or generate a persistent cryptographic secret key for Flask sessions."""
    if SECRET_KEY_FILE.exists():
        try:
            key = SECRET_KEY_FILE.read_bytes()
            if len(key) >= 32:
                return key
        except Exception:
            pass
    key = secrets.token_bytes(32)
    SECRET_KEY_FILE.write_bytes(key)
    return key

def get_lan_ip() -> str:
    """Detect private LAN IPv4 address for iPad connection."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0.5)
        # Does not actually transmit packets, just resolves the active outbound interface
        s.connect(("10.255.255.255", 1))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        try:
            return socket.gethostbyname(socket.gethostname())
        except Exception:
            return "127.0.0.1"

class Config:
    SECRET_KEY = get_or_create_secret_key()
    PORT = 5000
    SESSION_COOKIE_NAME = "dex_session"
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"  # Allows iPad browser navigation
    PERMANENT_SESSION_LIFETIME = 86400 * 7  # 7 days
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max payload
    
    @classmethod
    def is_setup_completed(cls) -> bool:
        return CREDENTIALS_FILE.exists()
