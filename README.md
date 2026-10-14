# DEX Control 🎛️

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Platform Windows](https://img.shields.io/badge/platform-Windows%2010%20%2F%2011-0078D6.svg)](https://www.microsoft.com/windows)
[![License MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Interface Apple Touch](https://img.shields.io/badge/interface-iPad%20Safari%20PWA-orange.svg)]()

> **Turn your Apple iPad or tablet into a native-grade, responsive Windows Touch Control Deck.**  
> Control your Windows PC audio, media, apps, and macros wirelessly over your local Wi-Fi network with zero cloud dependencies and zero subscriptions.

---

## ✨ Features

- 🔊 **Real Windows Core Audio Master Volume:**
  - Real-time responsive volume slider with 50ms debouncing that adjusts your actual Windows endpoint audio in real-time.
  - Quick-snap preset buttons (`20%`, `50%`, `80%`, `100%`) and instant hardware mute toggle.
  - Automatically queries and syncs with Windows master volume state.

- 🎵 **Windows GSMTC Media Control Center:**
  - Direct integration with Windows Global System Media Transport Controls (GSMTC).
  - Displays live track title, artist, playback status, and source app (Spotify, Chrome, YouTube, VLC, etc.).
  - Hardware media transport buttons: Play/Pause, Next Track, Previous Track, Rewind, Fast Forward.

- 🚀 **Native App Launcher & Smart Focusing:**
  - Auto-detects installed software including Antigravity IDE, Google Chrome, Windows Terminal, PowerShell, WhatsApp Desktop, File Explorer, and System Settings.
  - If an app is already open, DEX Control brings its window to the foreground instead of spawning duplicate instances.
  - Register custom game and program `.exe` paths with server-side validation.

- ⚡ **Visual Multi-Step Macro Builder:**
  - Chain actions together (e.g. Set volume to 30% ➔ Delay 1s ➔ Launch IDE ➔ Focus Terminal).
  - Built-in concurrency guards prevent overlapping macro runs.
  - Pre-configured defaults for Dev Setup, Focus Mode, and Media.

- 📱 **Interactive Profile & Stream Deck Grid Editor:**
  - Multiple built-in profiles: General, Coding, Gaming, Media.
  - Visual grid customization: Add buttons, customize icons, assign actions or shortcuts, rearrange, resize (1x1 or 2x1 wide), and duplicate.
  - Light and Dark themes with persistent local storage.

- 🔒 **Security-First Architecture:**
  - 100% local hosting: No external telemetry, no internet required.
  - Master password hashed with `scrypt`.
  - Convenient 6-Digit Touch Pairing PIN for iPad touchscreens.
  - Per-request cryptographic CSRF token validation on all state-changing endpoints.
  - Inbound host header validation and IP rate limiting against brute-force attacks.
  - Allowlist-only action dispatch: strictly zero arbitrary shell command execution.

---

## 🚀 Quick Start

### Option 1: Automatic Launch (Recommended)

Simply double-click or run:
```cmd
run.bat
```
The launcher will automatically:
1. Verify Python 3.10+ is installed and in your `PATH`.
2. Create an isolated virtual environment (`.venv`) if one does not exist.
3. Install or update all required dependencies (`requirements.txt`).
4. Terminate any stale processes on port 5000 and start the DEX Control server.

### Option 2: Manual Setup

```powershell
# 1. Clone the repository
git clone https://github.com/your-username/dex-control.git
cd dex-control

# 2. Create and activate a virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start the server
python app.py
```

The terminal will display your local URL (`http://127.0.0.1:5000`) and private Wi-Fi network URL (`http://<your-pc-ip>:5000`).

---

## 📱 Setting Up on Apple iPad (Safari PWA)

To get the full standalone, borderless hardware deck experience:

1. **Connect to Same Network:** Ensure your iPad and Windows PC are connected to the same Wi-Fi router.
2. **Initial Setup on PC:**
   - Open `http://127.0.0.1:5000` in your PC browser.
   - Create your master password.
   - Open **Settings** on the deck and confirm **"Enable Private LAN Access"** is checked. Note the displayed LAN URL (e.g., `http://192.168.1.45:5000`).
3. **Open on iPad:**
   - Open Safari on your iPad and navigate to your PC's LAN URL (`http://<your-pc-ip>:5000`).
   - Log in using your master password or the 6-digit PIN shown in PC Settings.
4. **Install as Fullscreen Web App:**
   - In Safari, tap the **Share** button (box with an upward arrow).
   - Tap **"Add to Home Screen"**.
   - Tap **"Add"**.
   - Launch **DEX Control** directly from your iPad home screen to run in borderless standalone mode!

---

## 🛡️ Security Model

Because DEX Control interacts with your computer's operating system, security is enforced at every layer:

| Security Measure | Implementation |
|---|---|
| **Localhost Default** | Binds to `127.0.0.1` unless Private LAN Access is explicitly enabled in Settings |
| **Authentication** | Password protection using `scrypt` key derivation (`data/credentials.json` excluded from git) |
| **iPad PIN Pairing** | Ephemeral 6-digit PIN regenerated on demand so you don't need to type master passwords on touchscreens |
| **CSRF Defense** | Cryptographic session tokens and `X-CSRF-Token` headers required for all state mutations |
| **Strict Allowlist** | Actions, keyboard shortcuts, and commands use fixed allowlists; arbitrary shell commands are rejected |
| **Screenshot Safety** | Screen captures are stored in a dedicated protected folder and indexed with random UUID tokens |
| **Rate Limiting** | Exponential backoff and lockout protection against brute-force login attempts |

> [!TIP]
> **Windows Firewall Note:** If your iPad cannot connect, make sure your Windows Wi-Fi network profile is set to **Private**. To create a firewall rule restricted to your private home network:
> ```powershell
> New-NetFirewallRule -DisplayName "DEX Control (Private LAN)" -Direction Inbound -LocalPort 5000 -Protocol TCP -Action Allow -Profile Private
> ```

---

## 📁 Project Structure

```
dex-control/
├── app.py                      # Flask application and REST API endpoints
├── config.py                   # Environment, storage paths, and network IP detection
├── run.bat                     # Windows one-click start script
├── requirements.txt            # Python dependencies (pycaw, comtypes, pillow, psutil, waitress, flask)
├── LICENSE                     # MIT License
├── README.md                   # Project documentation
├── .gitignore                  # Git exclusions for credentials, secrets, and venv
├── dex/                        # Core backend Python package
│   ├── __init__.py             # Package definition
│   ├── actions.py              # Validated action dispatch and activity history
│   ├── app_launcher.py         # App discovery, registry, and window focusing
│   ├── auth.py                 # Scrypt encryption, PIN pairing, rate-limiting, and CSRF
│   ├── gsmtc_worker.ps1        # WinRT media session PowerShell worker
│   ├── macros.py               # Macro automation engine with safety validation
│   ├── media_controls.py       # GSMTC media metadata and transport controls
│   ├── profiles.py             # Profile presets and layout definitions
│   ├── settings.py             # Server settings, LAN configuration, and custom apps
│   └── windows_controls.py     # Real Core Audio, GDI screen capture, shortcuts
├── static/                     # Frontend static assets
│   ├── app.js                  # Touch deck client engine, real-time sync, volume debouncing
│   └── style.css               # Glassmorphic Apple-inspired design system
├── templates/                  # Frontend HTML templates
│   ├── index.html              # Main Stream Deck dashboard
│   ├── login.html              # Touch-friendly authentication and PIN entry
│   └── setup.html              # Initial setup and master password creation
└── tests/                      # Automated test suite
    ├── test_actions.py         # Action validation and shortcut allowlists
    ├── test_api.py             # REST API, CSRF, and volume endpoint tests
    ├── test_auth.py            # Password hashing, rate limiting, and session tests
    ├── test_concurrency.py     # Macro locking and concurrency handling
    ├── test_macros.py          # Macro safety limits and step validation
    ├── test_validation.py      # Executable path validation and profile integrity
    └── integration_manual_check.py # Real live Windows integration verification
```

---

## 🧪 Testing

Run the automated test suite with Python's built-in `unittest`:
```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -p "test_*.py"
```

To run the live hardware integration verification (tests volume stepping, media metadata, screenshot capture, and app detection):
```powershell
.\.venv\Scripts\python.exe tests\integration_manual_check.py
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. **Fork** the repository and create a feature branch (`git checkout -b feature/amazing-feature`).
2. Keep the architecture **dependency-light**: stick to pure native web tech (Vanilla JS & CSS) and standard Python libraries wherever possible.
3. Ensure all tests pass (`python -m unittest discover -s tests`).
4. Commit your changes (`git commit -m "Add amazing feature"`).
5. Push to your branch (`git push origin feature/amazing-feature`) and open a **Pull Request**.

---

## 📄 License

This project is open-source and distributed under the **[MIT License](LICENSE)**.
