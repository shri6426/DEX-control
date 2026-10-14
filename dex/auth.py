import json
import time
import secrets
from functools import wraps
from typing import Dict, Tuple
from flask import session, request, jsonify, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from config import CREDENTIALS_FILE

# IP rate limiting store: {ip: [timestamp1, timestamp2, ...]}
_rate_limits: Dict[str, list] = {}
RATE_LIMIT_MAX_ATTEMPTS = 5
RATE_LIMIT_WINDOW_SECONDS = 60
LOCKOUT_SECONDS = 60
_lockouts: Dict[str, float] = {}

def is_setup_done() -> bool:
    return CREDENTIALS_FILE.exists()

def check_rate_limit(ip: str) -> Tuple[bool, int]:
    """Returns (is_allowed, wait_seconds_remaining)."""
    now = time.time()
    lockout_until = _lockouts.get(ip, 0)
    if now < lockout_until:
        return False, int(lockout_until - now)
    
    # Filter attempts within window
    attempts = [t for t in _rate_limits.get(ip, []) if now - t < RATE_LIMIT_WINDOW_SECONDS]
    _rate_limits[ip] = attempts
    
    if len(attempts) >= RATE_LIMIT_MAX_ATTEMPTS:
        _lockouts[ip] = now + LOCKOUT_SECONDS
        return False, LOCKOUT_SECONDS
    return True, 0

def record_failed_attempt(ip: str):
    now = time.time()
    attempts = _rate_limits.get(ip, [])
    attempts.append(now)
    _rate_limits[ip] = attempts
    if len(attempts) >= RATE_LIMIT_MAX_ATTEMPTS:
        _lockouts[ip] = now + LOCKOUT_SECONDS

def clear_rate_limit(ip: str):
    _rate_limits.pop(ip, None)
    _lockouts.pop(ip, None)

def setup_credentials(password: str) -> Tuple[bool, str]:
    if is_setup_done():
        return False, "Setup has already been completed. Use settings to change credentials."
    if not password or len(password) < 6:
        return False, "Password must be at least 6 characters."
    
    salt_hash = generate_password_hash(password, method="scrypt")
    payload = {
        "password_hash": salt_hash,
        "created_at": time.time(),
        "pairing_pin": str(secrets.randbelow(900000) + 100000)
    }
    CREDENTIALS_FILE.write_text(json.dumps(payload, indent=2))
    return True, "Credentials created successfully."

def update_password(current_password: str, new_password: str) -> Tuple[bool, str]:
    if not is_setup_done():
        return False, "Setup not complete."
    if not verify_credentials(current_password):
        return False, "Current password is incorrect."
    if not new_password or len(new_password) < 6:
        return False, "New password must be at least 6 characters."
    
    data = json.loads(CREDENTIALS_FILE.read_text())
    data["password_hash"] = generate_password_hash(new_password, method="scrypt")
    data["updated_at"] = time.time()
    CREDENTIALS_FILE.write_text(json.dumps(data, indent=2))
    return True, "Password updated successfully."

def get_pairing_pin() -> str:
    """Returns the current pairing PIN (for authenticated user in Settings)."""
    if not is_setup_done():
        return ""
    try:
        data = json.loads(CREDENTIALS_FILE.read_text())
        return data.get("pairing_pin", "")
    except Exception:
        return ""

def regenerate_pairing_pin() -> str:
    if not is_setup_done():
        return ""
    data = json.loads(CREDENTIALS_FILE.read_text())
    new_pin = str(secrets.randbelow(900000) + 100000)
    data["pairing_pin"] = new_pin
    CREDENTIALS_FILE.write_text(json.dumps(data, indent=2))
    return new_pin

def verify_credentials(password: str) -> bool:
    if not is_setup_done():
        return False
    try:
        data = json.loads(CREDENTIALS_FILE.read_text())
        stored_hash = data.get("password_hash", "")
        stored_pin = data.get("pairing_pin", "")
        # Allow either full password or pairing pin
        if check_password_hash(stored_hash, password):
            return True
        if stored_pin and password.strip() == stored_pin.strip():
            return True
        return False
    except Exception:
        return False

def generate_csrf_token() -> str:
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_hex(24)
    return session["csrf_token"]

def is_authenticated() -> bool:
    return bool(session.get("authenticated") is True)

def login_user() -> str:
    session.clear()
    session["authenticated"] = True
    session["auth_time"] = time.time()
    session["csrf_token"] = secrets.token_hex(24)
    return session["csrf_token"]

def logout_user():
    session.clear()

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not is_setup_done():
            if request.path.startswith("/api/"):
                return jsonify({"ok": False, "error": "SETUP_REQUIRED", "message": "Initial setup required"}), 403
            return redirect(url_for("setup_page"))
            
        if not is_authenticated():
            if request.path.startswith("/api/"):
                return jsonify({"ok": False, "error": "UNAUTHORIZED", "message": "Authentication required"}), 401
            return redirect(url_for("login_page"))
            
        return f(*args, **kwargs)
    return decorated

def require_csrf(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if request.method in ["POST", "PUT", "DELETE"]:
            token = request.headers.get("X-CSRF-Token") or request.form.get("csrf_token")
            expected = session.get("csrf_token")
            if not token or not expected or not secrets.compare_digest(token, expected):
                return jsonify({"ok": False, "error": "INVALID_CSRF", "message": "Invalid or missing CSRF token"}), 403
        return f(*args, **kwargs)
    return decorated
