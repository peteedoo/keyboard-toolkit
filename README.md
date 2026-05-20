# Open Source Keyboard Toolkit - Simple Edition

A single-file, zero-dependency launcher for **50 essential open-source keyboard customization tools**.

## Quick Start

**Double-click to launch GUI:**
- **Windows**: Double-click `keyboard-toolkit.bat`
- **macOS**: Double-click `keyboard-toolkit.command`
- **Linux**: Double-click `keyboard-toolkit` or run `./keyboard-toolkit`

**Terminal commands:**
```bash
./keyboard-toolkit list                          # List all tools
./keyboard-toolkit list "Firmware"               # List by category
./keyboard-toolkit search "QMK"                  # Search tools
./keyboard-toolkit info "QMK Firmware"           # Detailed info
./keyboard-toolkit launch "QMK Firmware"         # Open in browser
./keyboard-toolkit categories                    # List categories
```

## What's Included (50 Tools)

| Category | Count | Key Tools |
|----------|-------|-----------|
| **Firmware** | 11 | QMK, ZMK, VIAL, KMK, RMK, QMK Toolbox, QMK Configurator, VIA, Keymap Drawer, Keyberon, PRK |
| **Layout** | 5 | Keyboard Layout Editor, KLE-NG, Ergogen, KBFirmware, KeyFab |
| **CAD/PCB** | 12 | KiCad, kbplacer, marbastlib, ai03 Plate Gen, Hotswap PCB Gen, Flatboard, Dactyl, keyboard-tools.xyz, KLE PCB Gen, Keyboard STL Gen |
| **Remappers** | 8 | Kanata, Karabiner-Elements, AutoHotkey, keyd, Kmonad, GokuRakuJoudo, xremap, SharpKeys |
| **Utilities** | 9 | MonkeyType, Keybr.com, OpenRGB, Keyboard Simulator, InputScope, Keyboard Inspector, OSLTT, keyboard-tester.com |
| **Keycaps** | 3 | KeyV2, OpenCherry Font, joric/keycaps |

## Requirements

- Python 3.8+ (with tkinter for GUI mode)
- Zero external dependencies

## Files

| File | Purpose |
|------|---------|
| `keyboard-toolkit.py` | Main application (single file, GUI + CLI) |
| `keyboard-toolkit.bat` | Windows launcher |
| `keyboard-toolkit.command` | macOS launcher |
| `keyboard-toolkit` | Linux launcher |

## License

MIT - All included tools are open source with their respective licenses.
