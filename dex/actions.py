import time
import uuid
from typing import Dict, Any, List
from dex.windows_controls import (
    get_volume_info, set_master_volume, change_master_volume, set_master_mute,
    capture_screen, toggle_desktop, lock_workstation, send_shortcut
)
from dex.media_controls import execute_transport_action, get_now_playing
from dex.app_launcher import AppRegistry
from dex.macros import execute_macro
from dex.settings import load_settings

# In-memory action history log (capped at 50)
_action_history: List[Dict[str, Any]] = []

def get_action_history() -> List[Dict[str, Any]]:
    return list(reversed(_action_history))

def log_action(action_name: str, details: str, success: bool):
    entry = {
        "id": f"act_{int(time.time())}_{uuid.uuid4().hex[:6]}",
        "action": action_name,
        "details": details,
        "success": success,
        "timestamp": time.time(),
        "time_str": time.strftime("%H:%M:%S")
    }
    _action_history.append(entry)
    if len(_action_history) > 50:
        _action_history.pop(0)

def execute_action(action_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """Strictly validated action execution dispatch."""
    settings = load_settings()
    app_registry = AppRegistry(settings.get("custom_apps", {}))
    custom_paths = settings.get("app_paths", {})

    if action_name == "get_status":
        vol = get_volume_info()
        media = get_now_playing()
        return {
            "ok": True,
            "volume": vol,
            "media": media
        }

    elif action_name == "set_volume":
        level = params.get("level")
        if level is None:
            log_action("Volume Set", "Missing level parameter", False)
            return {"ok": False, "error": "MISSING_PARAM", "message": "Volume level is required (0-100)"}
        try:
            level = int(level)
        except ValueError:
            return {"ok": False, "error": "INVALID_PARAM", "message": "Volume must be an integer"}
        res = set_master_volume(level)
        success = res.get("ok", False)
        log_action("Volume Set", f"Set to {level}%", success)
        return {
            "ok": success,
            "action": "set_volume",
            "result": res,
            "message": f"Volume set to {level}%" if success else res.get("error", "Volume error")
        }

    elif action_name == "volume_step":
        delta = params.get("delta", 5)
        try:
            delta = int(delta)
        except ValueError:
            return {"ok": False, "error": "INVALID_PARAM", "message": "Delta must be an integer"}
        res = change_master_volume(delta)
        success = res.get("ok", False)
        new_vol = res.get("volume", "?")
        log_action("Volume Step", f"{'+' if delta > 0 else ''}{delta}% -> {new_vol}%", success)
        return {
            "ok": success,
            "action": "volume_step",
            "result": res,
            "message": f"Volume changed by {delta}% (now {new_vol}%)"
        }

    elif action_name == "set_mute":
        mute_val = params.get("mute")  # None triggers toggle
        res = set_master_mute(mute_val)
        success = res.get("ok", False)
        state_str = "Muted" if res.get("is_muted") else "Unmuted"
        log_action("Audio Mute", state_str, success)
        return {
            "ok": success,
            "action": "set_mute",
            "result": res,
            "message": f"Audio {state_str}"
        }

    elif action_name == "media_transport":
        m_action = params.get("action")
        value = params.get("value")
        res = execute_transport_action(m_action, value)
        success = res.get("ok", False)
        log_action(f"Media {m_action}", res.get("message", "Media action"), success)
        return res

    elif action_name == "screenshot":
        res = capture_screen()
        success = res.get("ok", False)
        log_action("Screenshot", res.get("filename", "Captured"), success)
        return {
            "ok": success,
            "action": "screenshot",
            "result": res,
            "message": "Screen captured successfully" if success else res.get("error", "Screenshot failed")
        }

    elif action_name == "show_desktop":
        res = toggle_desktop()
        success = res.get("ok", False)
        log_action("Show Desktop", "Desktop toggled", success)
        return res

    elif action_name == "lock_pc":
        # Requires explicit confirmation flag from frontend
        confirmed = bool(params.get("confirmed"))
        if not confirmed:
            return {
                "ok": False,
                "error": "CONFIRMATION_REQUIRED",
                "message": "Locking the Windows laptop requires explicit confirmation."
            }
        res = lock_workstation()
        success = res.get("ok", False)
        log_action("Lock PC", "Workstation locked", success)
        return res

    elif action_name == "send_shortcut":
        shortcut = params.get("shortcut")
        res = send_shortcut(shortcut)
        success = res.get("ok", False)
        log_action(f"Shortcut {shortcut}", "Executed", success)
        return res

    elif action_name == "launch_app":
        app_id = params.get("app_id")
        focus = params.get("focus", True)
        res = app_registry.launch_app(app_id, custom_paths, focus_if_running=focus)
        success = res.get("ok", False)
        log_action(f"Launch {app_id}", res.get("message", "App launch"), success)
        return res

    elif action_name == "run_macro":
        macro_id = params.get("macro_id")
        res = execute_macro(macro_id, app_registry, custom_paths)
        success = res.get("ok", False)
        log_action(f"Macro {macro_id}", res.get("message", "Macro execution"), success)
        return res

    return {
        "ok": False,
        "error": "UNKNOWN_ACTION",
        "message": f"Action '{action_name}' is not in the approved action registry"
    }
