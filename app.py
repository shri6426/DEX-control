import os
import sys
from pathlib import Path
from flask import (
    Flask, render_template, request, jsonify, redirect, url_for,
    send_file, abort, session
)

from config import Config, get_lan_ip, SCREENSHOTS_DIR
from dex.auth import (
    is_setup_done, setup_credentials, update_password, verify_credentials,
    login_user, logout_user, is_authenticated, generate_csrf_token,
    require_auth, require_csrf, check_rate_limit, record_failed_attempt,
    clear_rate_limit, get_pairing_pin, regenerate_pairing_pin
)
from dex.windows_controls import (
    get_volume_info, set_master_volume, change_master_volume, set_master_mute,
    get_screenshot_path
)
from dex.media_controls import get_now_playing, execute_transport_action
from dex.app_launcher import AppRegistry
from dex.macros import load_macros, save_macros, execute_macro, validate_macro_definition
from dex.profiles import load_profiles, save_profiles, reset_to_defaults
from dex.settings import load_settings, save_settings, validate_and_register_custom_app, remove_custom_app
from dex.actions import execute_action, get_action_history

app = Flask(__name__)
app.config.from_object(Config)

# Allowed host names / IPs for host header validation
import ipaddress

def is_valid_host(host_header: str) -> bool:
    if not host_header:
        return True
    host = host_header.split(":")[0].strip().lower()
    if host in {"127.0.0.1", "localhost", "0.0.0.0"} or host.endswith(".local"):
        return True
    try:
        ip = ipaddress.ip_address(host)
        if ip.is_private or ip.is_loopback:
            return True
    except ValueError:
        pass
    lan_ip = get_lan_ip().lower()
    return host == lan_ip

@app.before_request
def validate_request_host():
    # Only validate host if host header exists
    host = request.headers.get("Host")
    if host and not is_valid_host(host):
        return jsonify({"ok": False, "error": "INVALID_HOST", "message": "Host header rejected"}), 400

# ==================== PAGE ROUTES ====================

@app.route("/")
def index():
    if not is_setup_done():
        return redirect(url_for("setup_page"))
    if not is_authenticated():
        return redirect(url_for("login_page"))
    csrf = generate_csrf_token()
    return render_template("index.html", csrf_token=csrf, lan_ip=get_lan_ip())

@app.route("/login")
def login_page():
    if not is_setup_done():
        return redirect(url_for("setup_page"))
    if is_authenticated():
        return redirect(url_for("index"))
    return render_template("login.html", csrf_token=generate_csrf_token())

@app.route("/setup")
def setup_page():
    if is_setup_done():
        return redirect(url_for("login_page"))
    return render_template("setup.html")

# ==================== AUTH API ====================

@app.route("/api/v1/auth/setup", methods=["POST"])
def api_auth_setup():
    data = request.get_json(silent=True) or request.form
    password = data.get("password", "")
    ok, msg = setup_credentials(password)
    if ok:
        csrf = login_user()
        return jsonify({"ok": True, "message": msg, "csrf_token": csrf})
    return jsonify({"ok": False, "error": "SETUP_FAILED", "message": msg}), 400

@app.route("/api/v1/auth/login", methods=["POST"])
def api_auth_login():
    ip = request.remote_addr or "unknown"
    allowed, wait_secs = check_rate_limit(ip)
    if not allowed:
        return jsonify({
            "ok": False,
            "error": "RATE_LIMITED",
            "message": f"Too many failed login attempts. Please wait {wait_secs} seconds."
        }), 429

    data = request.get_json(silent=True) or request.form
    password = data.get("password", "")
    if verify_credentials(password):
        clear_rate_limit(ip)
        csrf = login_user()
        return jsonify({"ok": True, "message": "Authenticated", "csrf_token": csrf})
    else:
        record_failed_attempt(ip)
        return jsonify({"ok": False, "error": "INVALID_CREDENTIALS", "message": "Incorrect password or pairing PIN"}), 401

@app.route("/api/v1/auth/logout", methods=["POST"])
@require_auth
@require_csrf
def api_auth_logout():
    logout_user()
    return jsonify({"ok": True, "message": "Logged out successfully"})

# ==================== STATUS & HEALTH ====================

@app.route("/api/v1/status")
def api_status():
    lan_ip = get_lan_ip()
    settings = load_settings()
    auth_state = is_authenticated()
    setup_state = is_setup_done()
    
    vol = get_volume_info() if auth_state else None
    media = get_now_playing() if auth_state else None
    
    return jsonify({
        "ok": True,
        "app_name": "DEX Control",
        "version": "1.0.0",
        "authenticated": auth_state,
        "setup_completed": setup_state,
        "lan_ip": lan_ip,
        "lan_enabled": settings.get("lan_enabled", False),
        "port": settings.get("port", 5000),
        "csrf_token": session.get("csrf_token") if auth_state else None,
        "volume": vol,
        "media": media
    })

# ==================== CORE ACTIONS ====================

@app.route("/api/v1/actions", methods=["POST"])
@require_auth
@require_csrf
def api_execute_action():
    data = request.get_json(silent=True) or {}
    action_name = data.get("action")
    params = data.get("params", {})
    if not action_name:
        return jsonify({"ok": False, "error": "MISSING_ACTION", "message": "Action name is required"}), 400
    
    res = execute_action(action_name, params)
    status_code = 200 if res.get("ok") else 400
    return jsonify(res), status_code

# ==================== AUDIO API ====================

@app.route("/api/v1/volume", methods=["GET", "POST"])
@require_auth
@require_csrf
def api_volume():
    if request.method == "GET":
        return jsonify(get_volume_info())
    
    # POST
    data = request.get_json(silent=True) or {}
    if "level" in data:
        return jsonify(set_master_volume(int(data["level"])))
    elif "delta" in data:
        return jsonify(change_master_volume(int(data["delta"])))
    elif "mute" in data:
        return jsonify(set_master_mute(data.get("mute")))
    elif data.get("action") == "toggle_mute":
        return jsonify(set_master_mute(None))
    return jsonify({"ok": False, "error": "INVALID_PARAMS"}), 400

# ==================== MEDIA API ====================

@app.route("/api/v1/media", methods=["GET"])
@require_auth
def api_media():
    return jsonify(get_now_playing())

@app.route("/api/v1/media/transport", methods=["POST"])
@require_auth
@require_csrf
def api_media_transport():
    data = request.get_json(silent=True) or {}
    act = data.get("action")
    val = data.get("value")
    return jsonify(execute_transport_action(act, val))

# ==================== APPLICATIONS API ====================

@app.route("/api/v1/apps", methods=["GET"])
@require_auth
def api_list_apps():
    settings = load_settings()
    registry = AppRegistry(settings.get("custom_apps", {}))
    return jsonify({"ok": True, "apps": registry.get_registered_apps(settings.get("app_paths", {}))})

@app.route("/api/v1/apps/launch", methods=["POST"])
@require_auth
@require_csrf
def api_launch_app():
    data = request.get_json(silent=True) or {}
    app_id = data.get("app_id")
    if not app_id:
        return jsonify({"ok": False, "error": "MISSING_APP_ID"}), 400
    settings = load_settings()
    registry = AppRegistry(settings.get("custom_apps", {}))
    res = registry.launch_app(app_id, settings.get("app_paths", {}))
    return jsonify(res)

# ==================== MACROS API ====================

@app.route("/api/v1/macros", methods=["GET", "POST"])
@require_auth
def api_macros():
    if request.method == "GET":
        return jsonify({"ok": True, "macros": load_macros()})
        
    require_csrf(lambda: None)()
    data = request.get_json(silent=True) or {}
    valid, msg = validate_macro_definition(data)
    if not valid:
        return jsonify({"ok": False, "error": "VALIDATION_FAILED", "message": msg}), 400
        
    macros = load_macros()
    macro_id = data.get("id") or f"macro_{int(time.time())}"
    data["id"] = macro_id
    macros[macro_id] = data
    save_macros(macros)
    return jsonify({"ok": True, "message": f"Macro '{data.get('name')}' saved", "macro": data})

@app.route("/api/v1/macros/<macro_id>", methods=["DELETE"])
@require_auth
@require_csrf
def api_delete_macro(macro_id: str):
    macros = load_macros()
    if macro_id in macros:
        del macros[macro_id]
        save_macros(macros)
        return jsonify({"ok": True, "message": "Macro deleted"})
    return jsonify({"ok": False, "error": "NOT_FOUND", "message": "Macro not found"}), 404

@app.route("/api/v1/macros/run", methods=["POST"])
@require_auth
@require_csrf
def api_run_macro():
    data = request.get_json(silent=True) or {}
    macro_id = data.get("macro_id")
    if not macro_id:
        return jsonify({"ok": False, "error": "MISSING_MACRO_ID"}), 400
    settings = load_settings()
    registry = AppRegistry(settings.get("custom_apps", {}))
    res = execute_macro(macro_id, registry, settings.get("app_paths", {}))
    return jsonify(res)

# ==================== PROFILES API ====================

@app.route("/api/v1/profiles", methods=["GET", "POST"])
@require_auth
def api_profiles():
    if request.method == "GET":
        return jsonify(load_profiles())
        
    require_csrf(lambda: None)()
    data = request.get_json(silent=True)
    if not data or "profiles" not in data:
        return jsonify({"ok": False, "error": "INVALID_FORMAT"}), 400
    save_profiles(data)
    return jsonify({"ok": True, "message": "Profiles saved successfully"})

@app.route("/api/v1/profiles/reset", methods=["POST"])
@require_auth
@require_csrf
def api_reset_profiles():
    data = reset_to_defaults()
    return jsonify({"ok": True, "message": "Profiles restored to defaults", "profiles": data})

# ==================== SCREENSHOT RETRIEVAL ====================

@app.route("/api/v1/screenshots/<shot_id>", methods=["GET"])
@require_auth
def api_get_screenshot(shot_id: str):
    # Reject directory traversal attempts
    if ".." in shot_id or "/" in shot_id or "\\" in shot_id:
        abort(400)
    file_path = get_screenshot_path(shot_id)
    if not file_path or not file_path.exists():
        return jsonify({"ok": False, "error": "NOT_FOUND", "message": "Screenshot not found or expired"}), 404
    return send_file(file_path, mimetype="image/jpeg")

# ==================== HISTORY API ====================

@app.route("/api/v1/history", methods=["GET"])
@require_auth
def api_history():
    return jsonify({"ok": True, "history": get_action_history()})

# ==================== SETTINGS API ====================

@app.route("/api/v1/settings", methods=["GET", "POST"])
@require_auth
def api_settings():
    if request.method == "GET":
        settings = load_settings()
        pin = get_pairing_pin()
        return jsonify({
            "ok": True,
            "settings": settings,
            "lan_ip": get_lan_ip(),
            "pairing_pin": pin
        })
        
    require_csrf(lambda: None)()
    data = request.get_json(silent=True) or {}
    settings = load_settings()
    
    if "lan_enabled" in data:
        settings["lan_enabled"] = bool(data["lan_enabled"])
    if "port" in data:
        try:
            p = int(data["port"])
            if 1024 <= p <= 65535:
                settings["port"] = p
        except ValueError:
            pass
    if "app_paths" in data and isinstance(data["app_paths"], dict):
        settings["app_paths"].update(data["app_paths"])
        
    save_settings(settings)
    return jsonify({"ok": True, "message": "Settings updated", "settings": settings})

@app.route("/api/v1/settings/custom-app", methods=["POST"])
@require_auth
@require_csrf
def api_add_custom_app():
    data = request.get_json(silent=True) or {}
    app_id = data.get("id", "").strip()
    name = data.get("name", "").strip()
    path_str = data.get("path", "").strip()
    category = data.get("category", "games")
    icon = data.get("icon", "gamepad")
    
    ok, msg = validate_and_register_custom_app(app_id, name, path_str, category, icon)
    if ok:
        return jsonify({"ok": True, "message": msg})
    return jsonify({"ok": False, "error": "VALIDATION_FAILED", "message": msg}), 400

@app.route("/api/v1/settings/custom-app/<app_id>", methods=["DELETE"])
@require_auth
@require_csrf
def api_delete_custom_app(app_id: str):
    if remove_custom_app(app_id):
        return jsonify({"ok": True, "message": f"App '{app_id}' removed"})
    return jsonify({"ok": False, "error": "NOT_FOUND"}), 404

@app.route("/api/v1/settings/regenerate-pin", methods=["POST"])
@require_auth
@require_csrf
def api_regen_pin():
    pin = regenerate_pairing_pin()
    return jsonify({"ok": True, "pairing_pin": pin})

@app.route("/api/v1/settings/password", methods=["POST"])
@require_auth
@require_csrf
def api_change_password():
    data = request.get_json(silent=True) or {}
    current_p = data.get("current_password", "")
    new_p = data.get("new_password", "")
    ok, msg = update_password(current_p, new_p)
    if ok:
        return jsonify({"ok": True, "message": msg})
    return jsonify({"ok": False, "error": "PASSWORD_UPDATE_FAILED", "message": msg}), 400

# ==================== ERROR HANDLERS ====================

@app.route("/favicon.ico")
def favicon():
    return "", 204

@app.errorhandler(404)
def handle_404(e):
    if request.path.startswith("/api/"):
        return jsonify({"ok": False, "error": "NOT_FOUND", "message": "Resource not found"}), 404
    return render_template("login.html"), 404

@app.errorhandler(500)
def handle_500(e):
    return jsonify({"ok": False, "error": "INTERNAL_SERVER_ERROR", "message": "An internal error occurred"}), 500

if __name__ == "__main__":
    settings = load_settings()
    lan_enabled = settings.get("lan_enabled", True)
    host = "0.0.0.0" if lan_enabled else "127.0.0.1"
    port = settings.get("port", 5000)
    
    print("\n" + "="*50)
    print("  DEX CONTROL - Windows Personal Control Deck")
    print("="*50)
    print(f"  Local Access: http://127.0.0.1:{port}")
    lan_ip = get_lan_ip()
    print(f"  LAN Access:   http://{lan_ip}:{port} (Open on your iPad Safari)")
    print("="*50 + "\n")
    
    try:
        from waitress import serve
        serve(app, host=host, port=port, threads=8)
    except ImportError:
        app.run(host=host, port=port, debug=False)
