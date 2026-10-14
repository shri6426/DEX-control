import os
import shutil
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional, List
import psutil
import ctypes

def _focus_window_by_process_name(process_name: str) -> bool:
    """Attempt to bring an already running application window to the foreground."""
    try:
        user32 = ctypes.windll.user32
        
        # Enumerate top-level windows
        SW_RESTORE = 9
        matched_hwnd = None
        
        # We find PIDs for the process
        target_pids = set()
        for p in psutil.process_iter(['name', 'pid']):
            try:
                if p.info['name'] and p.info['name'].lower() == process_name.lower():
                    target_pids.add(p.info['pid'])
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
                
        if not target_pids:
            return False
            
        def enum_windows_cb(hwnd, lparam):
            nonlocal matched_hwnd
            if user32.IsWindowVisible(hwnd):
                pid = ctypes.wintypes.DWORD()
                user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
                if pid.value in target_pids:
                    # Ignore tool windows or invisible helper windows
                    length = user32.GetWindowTextLengthW(hwnd)
                    if length > 0:
                        matched_hwnd = hwnd
                        return False  # stop enumeration
            return True
            
        WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.wintypes.BOOL, ctypes.wintypes.HWND, ctypes.wintypes.LPARAM)
        cb = WNDENUMPROC(enum_windows_cb)
        user32.EnumWindows(cb, 0)
        
        if matched_hwnd:
            user32.ShowWindow(matched_hwnd, SW_RESTORE)
            user32.SetForegroundWindow(matched_hwnd)
            return True
    except Exception:
        pass
    return False

class AppRegistry:
    """Registry and launcher for approved Windows applications."""
    
    def __init__(self, custom_apps: Optional[Dict[str, Dict[str, Any]]] = None):
        self.custom_apps = custom_apps or {}
        
    def detect_antigravity(self, custom_path: Optional[str] = None) -> Optional[str]:
        if custom_path and Path(custom_path).is_file():
            return custom_path
        # Check running process
        for p in psutil.process_iter(['name', 'exe']):
            try:
                if p.info['name'] and 'antigravity' in p.info['name'].lower() and p.info['exe']:
                    return p.info['exe']
            except Exception:
                continue
        # Check standard user paths
        local_app_data = os.environ.get("LOCALAPPDATA", "")
        candidates = [
            Path(local_app_data) / "Programs" / "Antigravity IDE" / "Antigravity IDE.exe",
            Path(local_app_data) / "Programs" / "antigravity" / "antigravity.exe",
            Path(os.environ.get("PROGRAMFILES", "C:\\Program Files")) / "Antigravity IDE" / "Antigravity IDE.exe",
        ]
        for c in candidates:
            if c.is_file():
                return str(c)
        return shutil.which("antigravity") or shutil.which("Antigravity IDE")

    def detect_chrome(self, custom_path: Optional[str] = None) -> Optional[str]:
        if custom_path and Path(custom_path).is_file():
            return custom_path
        candidates = [
            Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
            Path(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"),
            Path(os.environ.get("LOCALAPPDATA", "")) / "Google" / "Chrome" / "Application" / "chrome.exe"
        ]
        for c in candidates:
            if c.is_file():
                return str(c)
        return shutil.which("chrome")

    def detect_windows_terminal(self, custom_path: Optional[str] = None) -> Optional[str]:
        if custom_path and Path(custom_path).is_file():
            return custom_path
        candidates = [
            Path(os.environ.get("LOCALAPPDATA", "")) / "Microsoft" / "WindowsApps" / "wt.exe",
            Path(r"C:\Program Files\WindowsApps\Microsoft.WindowsTerminal_*\wt.exe"),
        ]
        for c in candidates:
            if c.is_file():
                return str(c)
        return shutil.which("wt")

    def detect_powershell(self, custom_path: Optional[str] = None) -> Optional[str]:
        if custom_path and Path(custom_path).is_file():
            return custom_path
        candidates = [
            Path(r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"),
            Path(r"C:\Program Files\PowerShell\7\pwsh.exe"),
        ]
        for c in candidates:
            if c.is_file():
                return str(c)
        return shutil.which("powershell") or shutil.which("pwsh")

    def get_registered_apps(self, custom_configs: Optional[Dict[str, str]] = None) -> List[Dict[str, Any]]:
        """Return list of all available and detectable applications with status."""
        custom_configs = custom_configs or {}
        
        antigravity_path = self.detect_antigravity(custom_configs.get("antigravity"))
        chrome_path = self.detect_chrome(custom_configs.get("chrome"))
        wt_path = self.detect_windows_terminal(custom_configs.get("terminal"))
        ps_path = self.detect_powershell(custom_configs.get("powershell"))
        
        apps = [
            {
                "id": "antigravity",
                "name": "Antigravity IDE",
                "category": "development",
                "icon": "code",
                "path": antigravity_path,
                "installed": bool(antigravity_path),
                "is_running": self._is_process_running("Antigravity IDE.exe"),
                "description": "Primary coding environment and agent IDE"
            },
            {
                "id": "chrome",
                "name": "Google Chrome",
                "category": "browsers",
                "icon": "globe",
                "path": chrome_path,
                "installed": bool(chrome_path),
                "is_running": self._is_process_running("chrome.exe"),
                "description": "Web browser"
            },
            {
                "id": "terminal",
                "name": "Windows Terminal",
                "category": "utilities",
                "icon": "terminal",
                "path": wt_path,
                "installed": bool(wt_path),
                "is_running": self._is_process_running("WindowsTerminal.exe") or self._is_process_running("wt.exe"),
                "description": "Windows modern terminal console"
            },
            {
                "id": "powershell",
                "name": "PowerShell",
                "category": "utilities",
                "icon": "command-line",
                "path": ps_path,
                "installed": bool(ps_path),
                "is_running": self._is_process_running("powershell.exe") or self._is_process_running("pwsh.exe"),
                "description": "Windows PowerShell environment"
            },
            {
                "id": "whatsapp",
                "name": "WhatsApp Desktop",
                "category": "communication",
                "icon": "message-circle",
                "path": "whatsapp://",
                "installed": True,  # Desktop app or web fallback supported
                "is_running": self._is_process_running("WhatsApp.exe") or self._is_process_running("WhatsApp.Root.exe"),
                "description": "WhatsApp messaging client (with Web fallback)"
            },
            {
                "id": "explorer",
                "name": "File Explorer",
                "category": "system",
                "icon": "folder",
                "path": "explorer.exe",
                "installed": True,
                "is_running": True,
                "description": "Windows file management"
            },
            {
                "id": "taskmgr",
                "name": "Task Manager",
                "category": "system",
                "icon": "activity",
                "path": "taskmgr.exe",
                "installed": True,
                "is_running": self._is_process_running("Taskmgr.exe"),
                "description": "System resource and task manager"
            },
            {
                "id": "settings",
                "name": "Windows Settings",
                "category": "system",
                "icon": "settings",
                "path": "ms-settings:",
                "installed": True,
                "is_running": self._is_process_running("SystemSettings.exe"),
                "description": "Windows operating system settings"
            },
            {
                "id": "snipping",
                "name": "Snipping Tool",
                "category": "utilities",
                "icon": "crop",
                "path": "ms-screenclip:",
                "installed": True,
                "is_running": False,
                "description": "Windows screen clipping tool"
            }
        ]
        
        # Add custom apps configured by user
        for app_id, item in self.custom_apps.items():
            path_val = item.get("path", "")
            exists = Path(path_val).is_file() if path_val else False
            proc_name = Path(path_val).name if path_val else ""
            apps.append({
                "id": app_id,
                "name": item.get("name", app_id),
                "category": item.get("category", "games"),
                "icon": item.get("icon", "gamepad"),
                "path": path_val,
                "installed": exists,
                "is_running": self._is_process_running(proc_name) if proc_name else False,
                "description": item.get("description", "Custom user application"),
                "is_custom": True
            })
            
        return apps

    def _is_process_running(self, process_name: str) -> bool:
        if not process_name:
            return False
        for p in psutil.process_iter(['name']):
            try:
                if p.info['name'] and p.info['name'].lower() == process_name.lower():
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return False

    def launch_app(self, app_id: str, custom_configs: Optional[Dict[str, str]] = None, focus_if_running: bool = True) -> Dict[str, Any]:
        """Launch approved application safely on Windows laptop."""
        custom_configs = custom_configs or {}
        
        # Built-in handlers
        if app_id == "antigravity":
            path = self.detect_antigravity(custom_configs.get("antigravity"))
            if not path:
                return {"ok": False, "error": "Antigravity IDE executable not found. Please set its path in Settings."}
            if focus_if_running and _focus_window_by_process_name("Antigravity IDE.exe"):
                return {"ok": True, "message": "Focused existing Antigravity IDE window", "action": "focused"}
            subprocess.Popen([path], close_fds=True)
            return {"ok": True, "message": "Launched Antigravity IDE", "action": "launched"}
            
        elif app_id == "chrome":
            path = self.detect_chrome(custom_configs.get("chrome"))
            if not path:
                return {"ok": False, "error": "Google Chrome executable not found."}
            if focus_if_running and _focus_window_by_process_name("chrome.exe"):
                return {"ok": True, "message": "Focused existing Google Chrome window", "action": "focused"}
            subprocess.Popen([path], close_fds=True)
            return {"ok": True, "message": "Launched Google Chrome", "action": "launched"}
            
        elif app_id == "terminal":
            path = self.detect_windows_terminal(custom_configs.get("terminal"))
            if not path:
                return {"ok": False, "error": "Windows Terminal (wt.exe) not found on this system. You can launch PowerShell instead."}
            if focus_if_running and (_focus_window_by_process_name("WindowsTerminal.exe") or _focus_window_by_process_name("wt.exe")):
                return {"ok": True, "message": "Focused existing Windows Terminal", "action": "focused"}
            subprocess.Popen([path], close_fds=True)
            return {"ok": True, "message": "Launched Windows Terminal", "action": "launched"}
            
        elif app_id == "powershell":
            path = self.detect_powershell(custom_configs.get("powershell"))
            if not path:
                return {"ok": False, "error": "PowerShell executable not found."}
            subprocess.Popen([path], close_fds=True)
            return {"ok": True, "message": "Launched PowerShell", "action": "launched"}
            
        elif app_id == "whatsapp":
            # Attempt to launch desktop WhatsApp protocol
            try:
                os.startfile("whatsapp:")
                return {"ok": True, "message": "Launched WhatsApp Desktop", "action": "launched"}
            except Exception:
                # Offer or open WhatsApp Web
                chrome = self.detect_chrome(custom_configs.get("chrome"))
                if chrome:
                    subprocess.Popen([chrome, "https://web.whatsapp.com"], close_fds=True)
                    return {"ok": True, "message": "Opened WhatsApp Web in Chrome (Desktop app not registered)", "action": "web_fallback"}
                else:
                    os.startfile("https://web.whatsapp.com")
                    return {"ok": True, "message": "Opened WhatsApp Web in default browser", "action": "web_fallback"}
                    
        elif app_id == "explorer":
            os.startfile("explorer.exe")
            return {"ok": True, "message": "Opened File Explorer", "action": "launched"}
            
        elif app_id == "taskmgr":
            os.startfile("taskmgr.exe")
            return {"ok": True, "message": "Opened Task Manager", "action": "launched"}
            
        elif app_id == "settings":
            os.startfile("ms-settings:")
            return {"ok": True, "message": "Opened Windows Settings", "action": "launched"}
            
        elif app_id == "snipping":
            try:
                os.startfile("ms-screenclip:")
            except Exception:
                os.startfile("snippingtool.exe")
            return {"ok": True, "message": "Opened Snipping Tool", "action": "launched"}
            
        # Check custom applications
        elif app_id in self.custom_apps:
            item = self.custom_apps[app_id]
            target_path = item.get("path")
            if not target_path or not Path(target_path).is_file():
                return {"ok": False, "error": f"Configured path for '{item.get('name', app_id)}' does not exist."}
            
            proc_name = Path(target_path).name
            if focus_if_running and _focus_window_by_process_name(proc_name):
                return {"ok": True, "message": f"Focused existing window for {item.get('name')}", "action": "focused"}
                
            subprocess.Popen([target_path], close_fds=True)
            return {"ok": True, "message": f"Launched {item.get('name', app_id)}", "action": "launched"}

        return {"ok": False, "error": f"Application '{app_id}' is not in the registry."}
