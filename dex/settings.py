import json
from pathlib import Path
from typing import Dict, Any, Tuple
from config import CONFIG_FILE

DEFAULT_SETTINGS = {
    "lan_enabled": True,
    "port": 5000,
    "app_paths": {
        "antigravity": "",
        "chrome": "",
        "terminal": "",
        "powershell": ""
    },
    "custom_apps": {}
}

def load_settings() -> Dict[str, Any]:
    if CONFIG_FILE.exists():
        try:
            stored = json.loads(CONFIG_FILE.read_text())
            # Ensure defaults for missing keys
            for k, v in DEFAULT_SETTINGS.items():
                if k not in stored:
                    stored[k] = v
            return stored
        except Exception:
            pass
    CONFIG_FILE.write_text(json.dumps(DEFAULT_SETTINGS, indent=2))
    return DEFAULT_SETTINGS.copy()

def save_settings(settings: Dict[str, Any]):
    CONFIG_FILE.write_text(json.dumps(settings, indent=2))

def validate_and_register_custom_app(app_id: str, name: str, path_str: str, category: str = "games", icon: str = "gamepad") -> Tuple[bool, str]:
    """Validate executable path before saving to server registry."""
    clean_id = app_id.replace("_", "").replace("-", "")
    if not app_id or not clean_id.isalnum():
        return False, "Application ID must be alphanumeric"
    if not name or len(name) > 40:
        return False, "Application name must be between 1 and 40 characters"
    if not path_str:
        return False, "Path is required"
    
    p = Path(path_str)
    if not p.is_file():
        return False, f"The file '{path_str}' does not exist on this Windows PC"
    if p.suffix.lower() not in [".exe", ".bat", ".cmd"]:
        return False, "File must be an executable (.exe)"
        
    settings = load_settings()
    settings["custom_apps"][app_id] = {
        "name": name,
        "path": str(p.resolve()),
        "category": category,
        "icon": icon
    }
    save_settings(settings)
    return True, f"Application '{name}' registered successfully"

def remove_custom_app(app_id: str) -> bool:
    settings = load_settings()
    if app_id in settings["custom_apps"]:
        del settings["custom_apps"][app_id]
        save_settings(settings)
        return True
    return False
