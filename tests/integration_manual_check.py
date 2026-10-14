import time
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dex.windows_controls import (
    get_volume_info, set_master_volume, change_master_volume, set_master_mute,
    capture_screen, toggle_desktop, send_shortcut
)
from dex.media_controls import get_now_playing, execute_transport_action
from dex.app_launcher import AppRegistry

print("=== DEX CONTROL LIVE INTEGRATION VERIFICATION ===")

# 1. Real Volume Check
v_orig = get_volume_info()
print(f"1. Original Windows Volume: {v_orig['volume']}%, Muted: {v_orig['is_muted']}")

# Step volume
change_master_volume(2)
v_after_step = get_volume_info()
print(f"   After +2% step: {v_after_step['volume']}%")

# Set volume explicitly
set_master_volume(35)
v_set = get_volume_info()
print(f"   After set to 35%: {v_set['volume']}%")

# Restore original volume
set_master_volume(v_orig['volume'])
print(f"   Restored to original: {get_volume_info()['volume']}%")

# 2. Media Metadata Check
now_playing = get_now_playing(force=True)
print(f"2. Media Live Metadata:")
print(f"   Has Session: {now_playing.get('has_session')}")
print(f"   Title: {now_playing.get('title')}")
print(f"   Artist: {now_playing.get('artist')}")
print(f"   Status: {now_playing.get('playback_status')}")

# 3. Screenshot Capture Check
shot_res = capture_screen()
print(f"3. Screenshot Capture:")
print(f"   Success: {shot_res.get('ok')}")
print(f"   Dimensions: {shot_res.get('width')}x{shot_res.get('height')}")
print(f"   File: {shot_res.get('filename')}")

# 4. App Registry Detection
reg = AppRegistry()
apps = reg.get_registered_apps()
print(f"4. Application Detection ({len(apps)} apps):")
for a in apps[:6]:
    print(f"   - {a['name']}: installed={a['installed']}, running={a['is_running']}, path={a['path']}")

# 5. Show Desktop Test
desk_res = toggle_desktop()
print(f"5. Toggle Desktop: {desk_res}")
time.sleep(0.5)
desk_res2 = toggle_desktop()
print(f"   Toggle Desktop Back: {desk_res2}")

print("=== ALL LIVE INTEGRATION CHECKS COMPLETED ===")
