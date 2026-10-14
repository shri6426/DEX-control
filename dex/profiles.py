import json
from typing import Dict, Any, List
from config import PROFILES_FILE

DEFAULT_PROFILES = {
    "default_profile": "general",
    "profiles": {
        "general": {
            "id": "general",
            "name": "General",
            "icon": "layout-grid",
            "description": "Everyday Windows controls, volume, and quick tools",
            "is_builtin": True,
            "buttons": [
                {"id": "btn_vol_mute", "label": "Mute Toggle", "icon": "volume-x", "category": "audio", "action": "set_mute", "size": "1x1"},
                {"id": "btn_vol_down", "label": "Vol -5%", "icon": "volume-1", "category": "audio", "action": "volume_step", "params": {"delta": -5}, "size": "1x1"},
                {"id": "btn_vol_up", "label": "Vol +5%", "icon": "volume-2", "category": "audio", "action": "volume_step", "params": {"delta": 5}, "size": "1x1"},
                {"id": "btn_media_pp", "label": "Play / Pause", "icon": "play", "category": "media", "action": "media_transport", "params": {"action": "play_pause"}, "size": "1x1"},
                {"id": "btn_screenshot", "label": "Screenshot", "icon": "camera", "category": "system", "action": "screenshot", "size": "1x1"},
                {"id": "btn_desktop", "label": "Desktop", "icon": "monitor", "category": "system", "action": "show_desktop", "size": "1x1"},
                {"id": "btn_antigravity", "label": "Antigravity", "icon": "code", "category": "apps", "action": "launch_app", "params": {"app_id": "antigravity"}, "size": "1x1"},
                {"id": "btn_chrome", "label": "Chrome", "icon": "globe", "category": "apps", "action": "launch_app", "params": {"app_id": "chrome"}, "size": "1x1"},
                {"id": "btn_explorer", "label": "Explorer", "icon": "folder", "category": "system", "action": "launch_app", "params": {"app_id": "explorer"}, "size": "1x1"},
                {"id": "btn_taskmgr", "label": "Task Manager", "icon": "activity", "category": "system", "action": "launch_app", "params": {"app_id": "taskmgr"}, "size": "1x1"},
                {"id": "btn_settings", "label": "Settings", "icon": "settings", "category": "system", "action": "launch_app", "params": {"app_id": "settings"}, "size": "1x1"},
                {"id": "btn_lock", "label": "Lock PC", "icon": "lock", "category": "system", "action": "lock_pc", "requires_confirmation": True, "size": "1x1"}
            ]
        },
        "coding": {
            "id": "coding",
            "name": "Coding",
            "icon": "code",
            "description": "Development shortcuts, terminals, and workflow macros",
            "is_builtin": True,
            "buttons": [
                {"id": "btn_macro_setup", "label": "Dev Setup", "icon": "sparkles", "category": "macros", "action": "run_macro", "params": {"macro_id": "coding_setup"}, "size": "2x1"},
                {"id": "btn_c_ag", "label": "Antigravity", "icon": "code", "category": "apps", "action": "launch_app", "params": {"app_id": "antigravity"}, "size": "1x1"},
                {"id": "btn_c_term", "label": "Terminal", "icon": "terminal", "category": "apps", "action": "launch_app", "params": {"app_id": "terminal"}, "size": "1x1"},
                {"id": "btn_c_ps", "label": "PowerShell", "icon": "command-line", "category": "apps", "action": "launch_app", "params": {"app_id": "powershell"}, "size": "1x1"},
                {"id": "btn_c_chrome", "label": "Chrome", "icon": "globe", "category": "apps", "action": "launch_app", "params": {"app_id": "chrome"}, "size": "1x1"},
                {"id": "btn_c_snip", "label": "Snip Tool", "icon": "crop", "category": "system", "action": "send_shortcut", "params": {"shortcut": "Win+Shift+S"}, "size": "1x1"},
                {"id": "btn_c_alt_tab", "label": "Switch App", "icon": "layers", "category": "system", "action": "send_shortcut", "params": {"shortcut": "Alt+Tab"}, "size": "1x1"},
                {"id": "btn_c_reopen", "label": "Reopen Tab", "icon": "rotate-ccw", "category": "browser", "action": "send_shortcut", "params": {"shortcut": "Ctrl+Shift+T"}, "size": "1x1"},
                {"id": "btn_c_undo", "label": "Undo (Ctrl+Z)", "icon": "corner-up-left", "category": "shortcuts", "action": "send_shortcut", "params": {"shortcut": "Ctrl+Z"}, "size": "1x1"},
                {"id": "btn_c_copy", "label": "Copy", "icon": "copy", "category": "shortcuts", "action": "send_shortcut", "params": {"shortcut": "Ctrl+C"}, "size": "1x1"},
                {"id": "btn_c_paste", "label": "Paste", "icon": "clipboard", "category": "shortcuts", "action": "send_shortcut", "params": {"shortcut": "Ctrl+V"}, "size": "1x1"}
            ]
        },
        "gaming": {
            "id": "gaming",
            "name": "Gaming",
            "icon": "gamepad",
            "description": "In-game audio, performance monitor, and background music",
            "is_builtin": True,
            "buttons": [
                {"id": "btn_g_mute", "label": "Mute", "icon": "volume-x", "category": "audio", "action": "set_mute", "size": "1x1"},
                {"id": "btn_g_v50", "label": "Vol 50%", "icon": "volume-1", "category": "audio", "action": "set_volume", "params": {"level": 50}, "size": "1x1"},
                {"id": "btn_g_v100", "label": "Vol 100%", "icon": "volume-2", "category": "audio", "action": "set_volume", "params": {"level": 100}, "size": "1x1"},
                {"id": "btn_g_pp", "label": "Play / Pause", "icon": "play", "category": "media", "action": "media_transport", "params": {"action": "play_pause"}, "size": "1x1"},
                {"id": "btn_g_next", "label": "Next Track", "icon": "skip-forward", "category": "media", "action": "media_transport", "params": {"action": "next"}, "size": "1x1"},
                {"id": "btn_g_taskmgr", "label": "Task Manager", "icon": "activity", "category": "system", "action": "launch_app", "params": {"app_id": "taskmgr"}, "size": "1x1"},
                {"id": "btn_g_desktop", "label": "Desktop", "icon": "monitor", "category": "system", "action": "show_desktop", "size": "1x1"},
                {"id": "btn_g_shot", "label": "Screenshot", "icon": "camera", "category": "system", "action": "screenshot", "size": "1x1"},
                {"id": "btn_g_snip", "label": "Snipping", "icon": "crop", "category": "system", "action": "send_shortcut", "params": {"shortcut": "Win+Shift+S"}, "size": "1x1"}
            ]
        },
        "media": {
            "id": "media",
            "name": "Media Deck",
            "icon": "music",
            "description": "Full playback controls, track navigation, and volume presets",
            "is_builtin": True,
            "buttons": [
                {"id": "btn_m_prev", "label": "Previous", "icon": "skip-back", "category": "media", "action": "media_transport", "params": {"action": "previous"}, "size": "1x1"},
                {"id": "btn_m_play", "label": "Play / Pause", "icon": "play", "category": "media", "action": "media_transport", "params": {"action": "play_pause"}, "size": "2x1"},
                {"id": "btn_m_next", "label": "Next Track", "icon": "skip-forward", "category": "media", "action": "media_transport", "params": {"action": "next"}, "size": "1x1"},
                {"id": "btn_m_v0", "label": "0%", "icon": "volume-x", "category": "audio", "action": "set_volume", "params": {"level": 0}, "size": "1x1"},
                {"id": "btn_m_v25", "label": "25%", "icon": "volume", "category": "audio", "action": "set_volume", "params": {"level": 25}, "size": "1x1"},
                {"id": "btn_m_v50", "label": "50%", "icon": "volume-1", "category": "audio", "action": "set_volume", "params": {"level": 50}, "size": "1x1"},
                {"id": "btn_m_v75", "label": "75%", "icon": "volume-2", "category": "audio", "action": "set_volume", "params": {"level": 75}, "size": "1x1"},
                {"id": "btn_m_v100", "label": "100%", "icon": "volume-2", "category": "audio", "action": "set_volume", "params": {"level": 100}, "size": "1x1"},
                {"id": "btn_m_mute", "label": "Mute Toggle", "icon": "volume-x", "category": "audio", "action": "set_mute", "size": "1x1"}
            ]
        }
    }
}

def load_profiles() -> Dict[str, Any]:
    if PROFILES_FILE.exists():
        try:
            return json.loads(PROFILES_FILE.read_text())
        except Exception:
            pass
    PROFILES_FILE.write_text(json.dumps(DEFAULT_PROFILES, indent=2))
    return DEFAULT_PROFILES.copy()

def save_profiles(data: Dict[str, Any]):
    PROFILES_FILE.write_text(json.dumps(data, indent=2))

def reset_to_defaults():
    save_profiles(DEFAULT_PROFILES)
    return DEFAULT_PROFILES.copy()
