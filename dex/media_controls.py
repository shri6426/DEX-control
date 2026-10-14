import json
import time
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional
from dex.windows_controls import send_media_key, get_volume_info, set_master_volume, change_master_volume, set_master_mute

WORKER_SCRIPT = Path(__file__).resolve().parent / "gsmtc_worker.ps1"

_cached_now_playing: Optional[Dict[str, Any]] = None
_last_query_time: float = 0
CACHE_TTL = 1.0  # 1 second cache to prevent sub-process spam

def get_now_playing(force: bool = False) -> Dict[str, Any]:
    """Retrieve current Windows media playback information and metadata."""
    global _cached_now_playing, _last_query_time
    now = time.time()
    
    if not force and _cached_now_playing and (now - _last_query_time) < CACHE_TTL:
        return _cached_now_playing
    
    if not WORKER_SCRIPT.exists():
        return {"ok": False, "has_session": False, "error": "Media worker script missing"}
    
    try:
        proc = subprocess.run(
            ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(WORKER_SCRIPT), "-Action", "query"],
            capture_output=True,
            text=True,
            timeout=3.5,
            creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0
        )
        if proc.returncode == 0 and proc.stdout.strip():
            raw = proc.stdout.strip()
            data = json.loads(raw)
            result = {
                "ok": True,
                "has_session": data.get("has_session", False),
                "title": data.get("title", ""),
                "artist": data.get("artist", ""),
                "album": data.get("album", ""),
                "app_id": data.get("app_id", ""),
                "playback_status": data.get("playback_status", "Stopped"),
                "can_play": data.get("can_play", True),
                "can_pause": data.get("can_pause", True),
                "can_next": data.get("can_next", True),
                "can_previous": data.get("can_previous", True),
                "can_fast_forward": data.get("can_fast_forward", False),
                "can_rewind": data.get("can_rewind", False),
                "position": round(data.get("position", 0), 1),
                "duration": round(data.get("duration", 0), 1),
                "volume": get_volume_info()
            }
            _cached_now_playing = result
            _last_query_time = now
            return result
    except Exception as e:
        pass
    
    # Return minimal response if query timed out or failed
    vol = get_volume_info()
    return {
        "ok": True,
        "has_session": False,
        "playback_status": "Idle",
        "volume": vol
    }

def execute_transport_action(action: str, value: Optional[float] = None) -> Dict[str, Any]:
    """Execute media control action (play_pause, next, previous, fast_forward, rewind, seek)."""
    global _cached_now_playing
    _cached_now_playing = None  # Invalidate cache on explicit action
    
    valid_actions = ["play_pause", "next", "previous", "fast_forward", "rewind", "seek"]
    if action not in valid_actions:
        return {"ok": False, "error": f"Invalid media action '{action}'"}
    
    # Try GSMTC first via worker
    try:
        args = ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(WORKER_SCRIPT), "-Action", action]
        if action == "seek" and value is not None:
            args.extend(["-PositionSeconds", str(value)])
            
        proc = subprocess.run(
            args,
            capture_output=True,
            text=True,
            timeout=3.0,
            creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0
        )
        if proc.returncode == 0 and proc.stdout.strip():
            res = json.loads(proc.stdout.strip())
            if res.get("unsupported"):
                return {"ok": False, "error": f"The active media player does not support {action.replace('_', ' ')}."}
            if res.get("success"):
                time.sleep(0.1)
                return {"ok": True, "action": action, "result": get_now_playing(force=True)}
    except Exception:
        pass

    # Fallback to standard Windows multimedia key
    if action in ["play_pause", "next", "previous"]:
        key_res = send_media_key(action)
        time.sleep(0.1)
        return {"ok": key_res.get("ok", False), "action": action, "fallback": True, "result": get_now_playing(force=True)}
    
    if action in ["fast_forward", "rewind", "seek"]:
        return {"ok": False, "error": f"Seeking or {action.replace('_', ' ')} is not supported by the current media player."}
        
    return {"ok": False, "error": f"Could not execute media action '{action}'"}
