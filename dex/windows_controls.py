import os
import time
import uuid
import ctypes
import ctypes.wintypes
from pathlib import Path
from typing import Dict, Any, Optional
import comtypes
from PIL import Image
from config import SCREENSHOTS_DIR

# Keep registry of generated screenshot IDs to prevent arbitrary file access
_authorized_screenshots: Dict[str, Path] = {}

def _init_com():
    """Ensure COM is initialized on the current worker thread."""
    try:
        comtypes.CoInitialize()
    except Exception:
        pass

def get_volume_info() -> Dict[str, Any]:
    """Retrieve actual Windows master audio volume and mute state."""
    _init_com()
    try:
        from pycaw.pycaw import AudioUtilities
        device = AudioUtilities.GetSpeakers()
        if not device:
            return {"ok": False, "volume": 0, "is_muted": False, "error": "No audio endpoint found"}
        endpoint = device.EndpointVolume
        scalar = endpoint.GetMasterVolumeLevelScalar()
        muted = bool(endpoint.GetMute())
        return {
            "ok": True,
            "volume": int(round(scalar * 100)),
            "is_muted": muted
        }
    except Exception as e:
        return {"ok": False, "volume": 0, "is_muted": False, "error": str(e)}

def set_master_volume(level: int) -> Dict[str, Any]:
    """Set actual Windows master volume (0 - 100)."""
    _init_com()
    try:
        from pycaw.pycaw import AudioUtilities
        device = AudioUtilities.GetSpeakers()
        if not device:
            return {"ok": False, "error": "No audio endpoint found"}
        endpoint = device.EndpointVolume
        clamped = max(0, min(100, int(level)))
        endpoint.SetMasterVolumeLevelScalar(clamped / 100.0, None)
        return get_volume_info()
    except Exception as e:
        return {"ok": False, "error": str(e)}

def change_master_volume(delta: int) -> Dict[str, Any]:
    """Change actual Windows master volume by delta (+/- percent)."""
    current = get_volume_info()
    if not current.get("ok"):
        return current
    new_vol = max(0, min(100, current["volume"] + delta))
    return set_master_volume(new_vol)

def set_master_mute(mute: Optional[bool] = None) -> Dict[str, Any]:
    """Set or toggle actual Windows master mute state."""
    _init_com()
    try:
        from pycaw.pycaw import AudioUtilities
        device = AudioUtilities.GetSpeakers()
        if not device:
            return {"ok": False, "error": "No audio endpoint found"}
        endpoint = device.EndpointVolume
        if mute is None:
            new_mute = not bool(endpoint.GetMute())
        else:
            new_mute = bool(mute)
        endpoint.SetMute(int(new_mute), None)
        return get_volume_info()
    except Exception as e:
        return {"ok": False, "error": str(e)}

def capture_screen() -> Dict[str, Any]:
    """Capture Windows laptop screen using native GDI BitBlt and save to secure directory."""
    try:
        u32 = ctypes.windll.user32
        g32 = ctypes.windll.gdi32
        
        # Make process DPI aware for accurate screen bounds
        try:
            u32.SetProcessDPIAware()
        except Exception:
            pass

        w = u32.GetSystemMetrics(0)
        h = u32.GetSystemMetrics(1)
        if w <= 0 or h <= 0:
            w, h = 1920, 1080

        hdc_src = u32.GetDC(0)
        hdc_mem = g32.CreateCompatibleDC(hdc_src)
        hbmp = g32.CreateCompatibleBitmap(hdc_src, w, h)
        old_bmp = g32.SelectObject(hdc_mem, hbmp)
        
        SRCCOPY = 0x00CC0020
        g32.BitBlt(hdc_mem, 0, 0, w, h, hdc_src, 0, 0, SRCCOPY)
        
        class BITMAPINFOHEADER(ctypes.Structure):
            _fields_ = [
                ('biSize', ctypes.wintypes.DWORD),
                ('biWidth', ctypes.wintypes.LONG),
                ('biHeight', ctypes.wintypes.LONG),
                ('biPlanes', ctypes.wintypes.WORD),
                ('biBitCount', ctypes.wintypes.WORD),
                ('biCompression', ctypes.wintypes.DWORD),
                ('biSizeImage', ctypes.wintypes.DWORD),
                ('biXPelsPerMeter', ctypes.wintypes.LONG),
                ('biYPelsPerMeter', ctypes.wintypes.LONG),
                ('biClrUsed', ctypes.wintypes.DWORD),
                ('biClrImportant', ctypes.wintypes.DWORD)
            ]
            
        class BITMAPINFO(ctypes.Structure):
            _fields_ = [('bmiHeader', BITMAPINFOHEADER), ('bmiColors', ctypes.wintypes.DWORD * 3)]
            
        bmi = BITMAPINFO()
        bmi.bmiHeader.biSize = ctypes.sizeof(BITMAPINFOHEADER)
        bmi.bmiHeader.biWidth = w
        bmi.bmiHeader.biHeight = -h  # top-down DIB
        bmi.bmiHeader.biPlanes = 1
        bmi.bmiHeader.biBitCount = 32
        bmi.bmiHeader.biCompression = 0
        
        buf = ctypes.create_string_buffer(w * h * 4)
        g32.GetDIBits(hdc_mem, hbmp, 0, h, buf, ctypes.byref(bmi), 0)
        
        # Clean up GDI handles
        g32.SelectObject(hdc_mem, old_bmp)
        g32.DeleteObject(hbmp)
        g32.DeleteDC(hdc_mem)
        u32.ReleaseDC(0, hdc_src)
        
        img = Image.frombuffer('RGBA', (w, h), buf, 'raw', 'BGRA', 0, 1)
        # Convert to RGB JPEG for fast transmission to iPad
        rgb_img = img.convert('RGB')
        
        shot_id = f"shot_{int(time.time())}_{uuid.uuid4().hex[:8]}"
        filename = f"{shot_id}.jpg"
        filepath = SCREENSHOTS_DIR / filename
        rgb_img.save(filepath, "JPEG", quality=85)
        
        _authorized_screenshots[shot_id] = filepath
        
        # Keep only the last 20 screenshots
        if len(_authorized_screenshots) > 20:
            oldest_id = next(iter(_authorized_screenshots))
            old_path = _authorized_screenshots.pop(oldest_id)
            try:
                if old_path.exists():
                    old_path.unlink()
            except Exception:
                pass

        return {
            "ok": True,
            "id": shot_id,
            "filename": filename,
            "width": w,
            "height": h,
            "timestamp": time.time(),
            "url": f"/api/v1/screenshots/{shot_id}"
        }
    except Exception as e:
        return {"ok": False, "error": f"Failed to capture screen: {str(e)}"}

def get_screenshot_path(shot_id: str) -> Optional[Path]:
    """Retrieve validated file path for an authorized screenshot ID."""
    path = _authorized_screenshots.get(shot_id)
    if path and path.exists():
        return path
    # Check directory safely
    candidate = (SCREENSHOTS_DIR / f"{shot_id}.jpg").resolve()
    if candidate.is_relative_to(SCREENSHOTS_DIR) and candidate.exists():
        _authorized_screenshots[shot_id] = candidate
        return candidate
    return None

def toggle_desktop() -> Dict[str, Any]:
    """Show or hide Windows desktop via Shell COM."""
    _init_com()
    try:
        import comtypes.client
        shell = comtypes.client.CreateObject("Shell.Application")
        shell.ToggleDesktop()
        return {"ok": True, "message": "Toggled Windows desktop"}
    except Exception:
        # Fallback to Win + D
        return send_shortcut("Win+D")

def lock_workstation() -> Dict[str, Any]:
    """Lock the Windows laptop workstation."""
    try:
        res = ctypes.windll.user32.LockWorkStation()
        if res:
            return {"ok": True, "message": "Windows workstation locked successfully"}
        return {"ok": False, "error": "Failed to lock workstation"}
    except Exception as e:
        return {"ok": False, "error": str(e)}

# Key code constants
VK_CODES = {
    'BACK': 0x08, 'TAB': 0x09, 'RETURN': 0x0D, 'ENTER': 0x0D,
    'SHIFT': 0x10, 'CONTROL': 0x11, 'CTRL': 0x11, 'ALT': 0x12, 'MENU': 0x12,
    'PAUSE': 0x13, 'CAPITAL': 0x14, 'ESCAPE': 0x1B, 'ESC': 0x1B,
    'SPACE': 0x20, 'LEFT': 0x25, 'UP': 0x26, 'RIGHT': 0x27, 'DOWN': 0x28,
    'SNAPSHOT': 0x2C, 'INSERT': 0x2D, 'DELETE': 0x2E,
    'LWIN': 0x5B, 'WIN': 0x5B, 'RWIN': 0x5C,
    'MEDIA_NEXT_TRACK': 0xB0, 'MEDIA_PREV_TRACK': 0xB1,
    'MEDIA_STOP': 0xB2, 'MEDIA_PLAY_PAUSE': 0xB3,
    'VOLUME_MUTE': 0xAD, 'VOLUME_DOWN': 0xAE, 'VOLUME_UP': 0xAF,
}
# Add numbers 0-9 and letters A-Z
for i in range(10):
    VK_CODES[str(i)] = 0x30 + i
for c in range(ord('A'), ord('Z') + 1):
    VK_CODES[chr(c)] = c

APPROVED_SHORTCUTS = {
    "Win+E": [('WIN', True), ('E', True), ('E', False), ('WIN', False)],
    "Win+Shift+S": [('WIN', True), ('SHIFT', True), ('S', True), ('S', False), ('SHIFT', False), ('WIN', False)],
    "Ctrl+Shift+Esc": [('CTRL', True), ('SHIFT', True), ('ESC', True), ('ESC', False), ('SHIFT', False), ('CTRL', False)],
    "Alt+Tab": [('ALT', True), ('TAB', True), ('TAB', False), ('ALT', False)],
    "Win+D": [('WIN', True), ('D', True), ('D', False), ('WIN', False)],
    "Ctrl+C": [('CTRL', True), ('C', True), ('C', False), ('CTRL', False)],
    "Ctrl+V": [('CTRL', True), ('V', True), ('V', False), ('CTRL', False)],
    "Ctrl+Z": [('CTRL', True), ('Z', True), ('Z', False), ('CTRL', False)],
    "Ctrl+Shift+T": [('CTRL', True), ('SHIFT', True), ('T', True), ('T', False), ('SHIFT', False), ('CTRL', False)],
}

KEYEVENTF_KEYUP = 0x0002

def send_shortcut(shortcut_name: str) -> Dict[str, Any]:
    """Execute an approved keyboard shortcut on Windows laptop."""
    seq = APPROVED_SHORTCUTS.get(shortcut_name)
    if not seq:
        return {"ok": False, "error": f"Shortcut '{shortcut_name}' is not in the approved allowlist"}
    
    try:
        user32 = ctypes.windll.user32
        for key_name, is_down in seq:
            vk = VK_CODES.get(key_name)
            if vk is not None:
                flags = 0 if is_down else KEYEVENTF_KEYUP
                user32.keybd_event(vk, 0, flags, 0)
                time.sleep(0.02)
        return {"ok": True, "message": f"Executed shortcut {shortcut_name}"}
    except Exception as e:
        return {"ok": False, "error": str(e)}

def send_media_key(key_action: str) -> Dict[str, Any]:
    """Send Windows multimedia virtual key event."""
    action_map = {
        "play_pause": 0xB3,
        "next": 0xB0,
        "previous": 0xB1,
        "stop": 0xB2,
        "volume_up": 0xAF,
        "volume_down": 0xAE,
        "mute": 0xAD
    }
    vk = action_map.get(key_action)
    if not vk:
        return {"ok": False, "error": f"Unknown media key action '{key_action}'"}
    
    try:
        user32 = ctypes.windll.user32
        user32.keybd_event(vk, 0, 0, 0)
        time.sleep(0.03)
        user32.keybd_event(vk, 0, KEYEVENTF_KEYUP, 0)
        return {"ok": True, "message": f"Sent media key {key_action}"}
    except Exception as e:
        return {"ok": False, "error": str(e)}
