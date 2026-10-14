import json
import time
import threading
from typing import Dict, Any, List, Tuple
from config import MACROS_FILE
from dex.windows_controls import (
    set_master_volume, set_master_mute, send_shortcut, toggle_desktop
)
from dex.media_controls import execute_transport_action

MAX_ACTIONS_PER_MACRO = 10
MAX_DELAY_SECONDS = 5.0
MAX_TOTAL_MACRO_RUNTIME = 30.0

# Execution lock to prevent overlapping runs
_macro_execution_lock = threading.Lock()

DEFAULT_MACROS = {
    "coding_setup": {
        "id": "coding_setup",
        "name": "Coding Setup",
        "icon": "code",
        "category": "development",
        "description": "Opens Antigravity IDE, Windows Terminal, and Google Chrome.",
        "requires_confirmation": False,
        "actions": [
            {"type": "launch_app", "target": "antigravity"},
            {"type": "delay", "seconds": 0.5},
            {"type": "launch_app", "target": "terminal"},
            {"type": "delay", "seconds": 0.5},
            {"type": "launch_app", "target": "chrome"}
        ]
    },
    "focus_mode": {
        "id": "focus_mode",
        "name": "Focus Mode",
        "icon": "eye",
        "category": "workflow",
        "description": "Sets master volume to 25% and opens Antigravity IDE.",
        "requires_confirmation": False,
        "actions": [
            {"type": "set_volume", "level": 25},
            {"type": "delay", "seconds": 0.3},
            {"type": "launch_app", "target": "antigravity"}
        ]
    },
    "media_chill": {
        "id": "media_chill",
        "name": "Media Setup",
        "icon": "music",
        "category": "media",
        "description": "Sets volume to 40% and toggles media playback.",
        "requires_confirmation": False,
        "actions": [
            {"type": "set_volume", "level": 40},
            {"type": "delay", "seconds": 0.2},
            {"type": "media_transport", "action": "play_pause"}
        ]
    }
}

def load_macros() -> Dict[str, Any]:
    if MACROS_FILE.exists():
        try:
            return json.loads(MACROS_FILE.read_text())
        except Exception:
            pass
    # Initialize with defaults
    MACROS_FILE.write_text(json.dumps(DEFAULT_MACROS, indent=2))
    return DEFAULT_MACROS.copy()

def save_macros(macros: Dict[str, Any]):
    MACROS_FILE.write_text(json.dumps(macros, indent=2))

def validate_macro_definition(macro: Dict[str, Any]) -> Tuple[bool, str]:
    if not isinstance(macro, dict):
        return False, "Macro must be a JSON object"
    
    name = macro.get("name", "").strip()
    if not name or len(name) > 50:
        return False, "Macro name must be between 1 and 50 characters"
        
    actions = macro.get("actions", [])
    if not isinstance(actions, list):
        return False, "Actions must be a list"
    if len(actions) == 0:
        return False, "Macro must contain at least one action"
    if len(actions) > MAX_ACTIONS_PER_MACRO:
        return False, f"A macro cannot exceed {MAX_ACTIONS_PER_MACRO} actions"
        
    total_delay = 0.0
    for idx, act in enumerate(actions):
        if not isinstance(act, dict):
            return False, f"Action #{idx+1} is invalid"
        act_type = act.get("type")
        
        if act_type == "delay":
            secs = float(act.get("seconds", 0))
            if secs <= 0 or secs > MAX_DELAY_SECONDS:
                return False, f"Delay in action #{idx+1} must be between 0.1 and {MAX_DELAY_SECONDS} seconds"
            total_delay += secs
            if total_delay > MAX_TOTAL_MACRO_RUNTIME:
                return False, f"Total macro delay exceeds maximum limit of {MAX_TOTAL_MACRO_RUNTIME} seconds"
                
        elif act_type == "set_volume":
            lvl = act.get("level")
            if lvl is None or not (0 <= int(lvl) <= 100):
                return False, f"Volume in action #{idx+1} must be between 0 and 100"
                
        elif act_type == "set_mute":
            pass
            
        elif act_type == "media_transport":
            m_act = act.get("action")
            if m_act not in ["play_pause", "next", "previous", "stop"]:
                return False, f"Invalid media action '{m_act}' in action #{idx+1}"
                
        elif act_type == "launch_app":
            app_id = act.get("target")
            if not app_id or not isinstance(app_id, str):
                return False, f"Invalid application target in action #{idx+1}"
                
        elif act_type == "send_shortcut":
            s_name = act.get("shortcut")
            from dex.windows_controls import APPROVED_SHORTCUTS
            if s_name not in APPROVED_SHORTCUTS:
                return False, f"Shortcut '{s_name}' in action #{idx+1} is not approved"
                
        elif act_type == "show_desktop":
            pass
            
        else:
            return False, f"Action type '{act_type}' in action #{idx+1} is not permitted"
            
    return True, "Valid"

def execute_macro(macro_id: str, app_registry, custom_configs: Dict[str, str]) -> Dict[str, Any]:
    """Execute macro sequence safely with timeout and error tracking."""
    macros = load_macros()
    macro = macros.get(macro_id)
    if not macro:
        return {"ok": False, "error": f"Macro '{macro_id}' not found"}
        
    is_valid, err = validate_macro_definition(macro)
    if not is_valid:
        return {"ok": False, "error": f"Invalid macro: {err}"}
        
    if not _macro_execution_lock.acquire(blocking=False):
        return {"ok": False, "error": "Another macro is currently executing. Please wait."}
        
    start_time = time.time()
    actions = macro.get("actions", [])
    executed_steps = []
    
    try:
        for idx, act in enumerate(actions):
            if (time.time() - start_time) > MAX_TOTAL_MACRO_RUNTIME:
                return {
                    "ok": False,
                    "error": "Macro execution timed out",
                    "step_failed": idx + 1,
                    "completed_steps": executed_steps
                }
                
            act_type = act.get("type")
            
            if act_type == "delay":
                secs = min(MAX_DELAY_SECONDS, float(act.get("seconds", 0.5)))
                time.sleep(secs)
                executed_steps.append(f"Waited {secs}s")
                
            elif act_type == "set_volume":
                res = set_master_volume(int(act.get("level", 50)))
                if not res.get("ok"):
                    return {"ok": False, "error": res.get("error", "Volume error"), "step_failed": idx + 1}
                executed_steps.append(f"Set volume to {act.get('level')}%")
                
            elif act_type == "set_mute":
                mute_val = act.get("mute")
                res = set_master_mute(mute_val)
                executed_steps.append(f"Set mute state")
                
            elif act_type == "media_transport":
                res = execute_transport_action(act.get("action", "play_pause"))
                executed_steps.append(f"Media transport {act.get('action')}")
                
            elif act_type == "launch_app":
                target = act.get("target")
                res = app_registry.launch_app(target, custom_configs)
                if not res.get("ok"):
                    return {"ok": False, "error": res.get("error", f"Failed to launch {target}"), "step_failed": idx + 1}
                executed_steps.append(f"Launched {target}")
                
            elif act_type == "send_shortcut":
                s_name = act.get("shortcut")
                res = send_shortcut(s_name)
                if not res.get("ok"):
                    return {"ok": False, "error": res.get("error"), "step_failed": idx + 1}
                executed_steps.append(f"Sent shortcut {s_name}")
                
            elif act_type == "show_desktop":
                toggle_desktop()
                executed_steps.append("Toggled desktop")
                
        return {
            "ok": True,
            "message": f"Macro '{macro.get('name')}' executed successfully",
            "duration": round(time.time() - start_time, 2),
            "steps": executed_steps
        }
    finally:
        _macro_execution_lock.release()
