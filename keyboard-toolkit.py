#!/usr/bin/env python3
"""
Open Source Keyboard Toolkit - Simple Edition
==============================================
A single-file, zero-dependency launcher for open-source keyboard tools.

Usage:
  python keyboard-toolkit.py              Launch GUI (default)
  python keyboard-toolkit.py --gui        Force GUI mode
  python keyboard-toolkit.py list         List all tools
  python keyboard-toolkit.py list <cat>   List by category
  python keyboard-toolkit.py search <q>   Search tools
  python keyboard-toolkit.py launch <n>   Open tool in browser
  python keyboard-toolkit.py info <n>     Show tool details
"""

import argparse
import os
import subprocess
import sys
import webbrowser

try:
    from tkinter import *
    from tkinter import font as tkfont
except ImportError:
    TKINTER = False
else:
    TKINTER = True

# =============================================================================
# TOOL DATABASE - 50 essential open-source keyboard tools
# =============================================================================

TOOLS = [
    # ----- FIRMWARE -----
    {"n": "QMK Firmware",        "c": "Firmware",     "d": "The standard open-source keyboard firmware. Supports 1000+ keyboards, layers, RGB, encoders, OLEDs.",           "u": "https://github.com/qmk/qmk_firmware",           "w": "",                                 "l": "GPL-2",   "s": "20.4k", "p": "Cross",     "i": "qmk setup"},
    {"n": "ZMK Firmware",        "c": "Firmware",     "d": "Wireless-first keyboard firmware on Zephyr RTOS. BLE, split, power-efficient.",                           "u": "https://github.com/zmkfirmware/zmk",             "w": "https://zmk.dev",                "l": "MIT",     "s": "4.1k",  "p": "Cross",     "i": "pip install zmk"},
    {"n": "VIAL",                "c": "Firmware",     "d": "Real-time keyboard configurator. Open-source alternative to VIA. Edit keymaps without reflashing.",       "u": "https://github.com/vial-kb/vial-gui",           "w": "https://get.vial.today",         "l": "GPL-2",   "s": "1.3k",  "p": "Cross",     "i": "Download from get.vial.today"},
    {"n": "KMK Firmware",        "c": "Firmware",     "d": "CircuitPython keyboard firmware. Edit keymaps as Python files — no compilation needed.",                   "u": "https://github.com/KMKfw/kmk_firmware",         "w": "",                                 "l": "GPL-3",   "s": "1.7k",  "p": "CircuitPy", "i": "Copy CircuitPython + KMK files to MCU"},
    {"n": "RMK",                 "c": "Firmware",     "d": "Rust keyboard firmware with Vial support, BLE wireless, split. Config via keyboard.toml.",               "u": "https://github.com/HaoboGu/rmk",                  "w": "",                                 "l": "MIT",     "s": "1.6k",  "p": "Cross",     "i": "cargo install rmkit"},
    {"n": "QMK Toolbox",         "c": "Firmware",     "d": "All-in-one GUI for flashing QMK firmware. Bundles bootloaders, key tester, debug console.",             "u": "https://github.com/qmk/qmk_toolbox",              "w": "",                                 "l": "MIT",     "s": "3.0k",  "p": "Win/Mac",   "i": "Download from GitHub Releases"},
    {"n": "QMK Configurator",    "c": "Firmware",     "d": "Web GUI for creating QMK firmware keymaps without code. 1000+ keyboards supported.",                    "u": "https://github.com/qmk/qmk_configurator",         "w": "https://config.qmk.fm",          "l": "MIT",     "s": "833",   "p": "Web",       "i": "Visit config.qmk.fm"},
    {"n": "VIA",                 "c": "Firmware",     "d": "Web configurator for real-time keymap changes on QMK keyboards. 1400+ keyboards.",                      "u": "https://github.com/the-via/app",                  "w": "https://usevia.app",             "l": "GPL-2",   "s": "300",   "p": "Web",       "i": "Visit usevia.app"},
    {"n": "Keymap Drawer",       "c": "Firmware",     "d": "Visualize QMK/ZMK keymaps as SVG diagrams. Parses keymap files automatically.",                         "u": "https://github.com/caksoylar/keymap-drawer",      "w": "https://caksoylar.github.io/keymap-drawer", "l": "MIT", "s": "700", "p": "Cross", "i": "pipx install keymap-drawer"},
    {"n": "KMK (RP2040)",        "c": "Firmware",     "d": "PRK Firmware - keyboard firmware in Ruby for RP2040. Copy files like a USB drive.",                      "u": "https://github.com/picoruby/prk_firmware",         "w": "",                                 "l": "MIT",     "s": "200",   "p": "RP2040",    "i": "Copy UF2 + keymap.rb to RP2040"},
    {"n": "Keyberon",            "c": "Firmware",     "d": "Rust crate for building keyboard firmware. no_std, layers, tap-hold, chords.",                          "u": "https://github.com/TeXitoi/keyberon",             "w": "",                                 "l": "MIT",     "s": "400",   "p": "Rust",      "i": "cargo add keyberon"},

    # ----- LAYOUT -----
    {"n": "Keyboard Layout Editor","c": "Layout",    "d": "The standard web tool for designing keyboard layouts. Exports JSON used by all other tools.",             "u": "https://github.com/ijprest/keyboard-layout-editor","w": "http://www.keyboard-layout-editor.com","l": "MIT", "s": "3.0k", "p": "Web",    "i": "Visit keyboard-layout-editor.com"},
    {"n": "KLE-NG",              "c": "Layout",       "d": "Modern reimplementation of KLE with plate/PCB generation. Dark theme, better UX.",                       "u": "https://github.com/adamws/kle-ng",               "w": "https://editor.keyboard-tools.xyz","l": "MIT",     "s": "191",   "p": "Web",       "i": "Visit editor.keyboard-tools.xyz"},
    {"n": "Ergogen",             "c": "Layout",       "d": "Parametric keyboard generator. YAML config -> KiCad PCB, plates, 3D cases. The full pipeline.",         "u": "https://github.com/ergogen/ergogen",              "w": "https://ergogen.xyz",            "l": "MIT",     "s": "1.5k",  "p": "Cross",     "i": "npm i -g ergogen"},
    {"n": "KBFirmware",          "c": "Layout",       "d": "Web tool for generating QMK firmware from visual layouts. Good for beginners.",                        "u": "https://github.com/kbfirmware/kbfirmware",        "w": "https://kbfirmware.com",         "l": "GPL-2",   "s": "200",   "p": "Web",       "i": "Visit kbfirmware.com"},
    {"n": "KeyFab",              "c": "Layout",       "d": "Modern layout editor with cloud save, layout sharing, split keyboard presets.",                        "u": "https://github.com/jaroslaw-weber/keyfab",        "w": "https://jaroslaw-weber.github.io/keyfab", "l": "Open", "s": "200", "p": "Web", "i": "Visit keyfab website"},

    # ----- CAD / PCB -----
    {"n": "KiCad EDA",           "c": "CAD/PCB",      "d": "Industry-standard open-source PCB design suite. Full schematic-to-manufacturing workflow.",              "u": "https://gitlab.com/kicad/code/kicad",             "w": "https://www.kicad.org",          "l": "GPL-3",   "s": "N/A",   "p": "Cross",     "i": "Download from kicad.org/download"},
    {"n": "KiCad kbplacer",      "c": "CAD/PCB",      "d": "KiCad plugin for auto-placing switches/diodes and routing tracks from layout files.",                  "u": "https://github.com/adamws/kicad-kbplacer",       "w": "",                                 "l": "MIT",     "s": "514",   "p": "Cross",     "i": "Via KiCad Plugin Manager"},
    {"n": "marbastlib",          "c": "CAD/PCB",      "d": "The most comprehensive KiCad library for keyboards. MX/Choc footprints, USB-C, BLE modules.",          "u": "https://github.com/ebastler/marbastlib",          "w": "",                                 "l": "Open",    "s": "300",   "p": "KiCad",     "i": "Via KiCad Plugin Manager"},
    {"n": "ai03 Plate Generator","c": "CAD/PCB",      "d": "Advanced web plate generator with proper cutouts, stabilizer support, kerf compensation.",             "u": "https://github.com/ai03-2725",                    "w": "https://kbplate.ai03.com",       "l": "MIT",     "s": "N/A",   "p": "Web",       "i": "Visit kbplate.ai03.com"},
    {"n": "Hotswap PCB Gen",     "c": "CAD/PCB",      "d": "3D-printable hotswap PCBs for prototyping. Wire-press matrix, no PCB fabrication needed.",            "u": "https://github.com/50an6xy06r6n/hotswap_pcb_generator","w": "",                            "l": "MIT",     "s": "600",   "p": "Cross",     "i": "OpenSCAD + Node.js"},
    {"n": "Flatboard",           "c": "CAD/PCB",      "d": "Parametric keyboard case generator. TypeScript config -> STL files. No CAD knowledge needed.",          "u": "https://github.com/20lives/flatboard",            "w": "",                                 "l": "MIT",     "s": "50",    "p": "Cross",     "i": "git clone + bun install"},
    {"n": "Dactyl-ManuForm",     "c": "CAD/PCB",      "d": "Generate ergonomic split keyboard cases. Configurable rows, columns, curvature, thumb clusters.",       "u": "https://github.com/poppatchara/dactyl-keyboard-py3","w": "",                               "l": "AGPL-3",  "s": "600",   "p": "Cross",     "i": "Docker or Python + CadQuery"},
    {"n": "keyboard-tools.xyz",  "c": "CAD/PCB",      "d": "Web interface for generating KiCad PCB files from layout files. No-schematic workflow.",              "u": "https://github.com/adamws/keyboard-tools",       "w": "https://keyboard-tools.xyz",     "l": "MIT",     "s": "93",    "p": "Web",       "i": "Visit keyboard-tools.xyz"},
    {"n": "KLE PCB Generator",   "c": "CAD/PCB",      "d": "Generate complete KiCad projects from KLE JSON. Schematic + partially routed PCB.",                   "u": "https://github.com/jeroen94704/klepcbgen",        "w": "",                                 "l": "CC-NC",   "s": "450",   "p": "Cross",     "i": "pip install -r requirements.txt"},
    {"n": "Keyboard STL Gen",    "c": "CAD/PCB",      "d": "Generate 3D-printable STL cases from KLE layouts. Top/bottom/plate with auto-segmentation.",         "u": "https://github.com/jeffminton/keyboard_stl_generator","w": "",                             "l": "MIT",     "s": "60",    "p": "Cross",     "i": "pip install -r requirements.txt + OpenSCAD"},

    # ----- REMAPPERS -----
    {"n": "Kanata",              "c": "Remappers",    "d": "Cross-platform key remapper with QMK-like layers, tap-hold, macros, mouse emulation.",                 "u": "https://github.com/jtroo/kanata",                 "w": "",                                 "l": "LGPL-3",  "s": "7.4k",  "p": "Cross",     "i": "Download from GitHub Releases or cargo install kanata"},
    {"n": "Karabiner-Elements",  "c": "Remappers",    "d": "The most powerful macOS keyboard customization tool. Complex modifications, layers, key remapping.",   "u": "https://github.com/pqrs-org/Karabiner-Elements",  "w": "https://karabiner-elements.pqrs.org","l": "BSD-3", "s": "18.5k", "p": "macOS",    "i": "brew install --cask karabiner-elements"},
    {"n": "AutoHotkey",          "c": "Remappers",    "d": "The dominant Windows scripting/automation utility. Hotkeys, macros, key remapping.",                     "u": "https://github.com/AutoHotkey/AutoHotkey",        "w": "https://www.autohotkey.com",     "l": "GPL-2",   "s": "12.4k", "p": "Windows",   "i": "winget install AutoHotkey.AutoHotkey"},
    {"n": "keyd",                "c": "Remappers",    "d": "Linux system-wide key remapping daemon. Kernel-level, sub-1ms latency, layers, QMK-like config.",       "u": "https://github.com/rvaiya/keyd",                  "w": "",                                 "l": "MIT",     "s": "5.4k",  "p": "Linux",     "i": "make && sudo make install"},
    {"n": "Kmonad",              "c": "Remappers",    "d": "Advanced keyboard manager in Haskell. QMK-inspired layers, tap-hold, tap-dance.",                       "u": "https://github.com/kmonad/kmonad",               "w": "",                                 "l": "MIT",     "s": "3.4k",  "p": "Cross",     "i": "brew install kmonad (macOS) or stack install"},
    {"n": "GokuRakuJoudo",       "c": "Remappers",    "d": "Clojure DSL for generating Karabiner-Elements configs. Write concise configs, get verbose JSON.",       "u": "https://github.com/yqrashawn/GokuRakuJoudo",     "w": "",                                 "l": "GPL-3",   "s": "1.4k",  "p": "macOS",     "i": "brew install yqrashawn/goku/goku"},
    {"n": "xremap",              "c": "Remappers",    "d": "Fast key remapper for Linux X11/Wayland. App-specific remapping, Rust, evdev-based.",                   "u": "https://github.com/xremap/xremap",               "w": "",                                 "l": "MIT",     "s": "2.1k",  "p": "Linux",     "i": "Download from GitHub Releases"},
    {"n": "SharpKeys",           "c": "Remappers",    "d": "Simple Windows registry-based key remapping. No background software — changes stored in registry.",   "u": "https://github.com/randyrants/sharpkeys",        "w": "",                                 "l": "MIT",     "s": "5k",    "p": "Windows",   "i": "Download from GitHub Releases or Microsoft Store"},

    # ----- UTILITIES -----
    {"n": "MonkeyType",          "c": "Utilities",    "d": "The most customizable typing test website. Multiple modes, progress tracking, minimal design.",          "u": "https://github.com/monkeytypegame/monkeytype",   "w": "https://monkeytype.com",         "l": "GPL-3",   "s": "20.5k", "p": "Web",       "i": "Visit monkeytype.com"},
    {"n": "Keybr.com",           "c": "Utilities",    "d": "Intelligent touch typing tutor. Generates lessons matching your current typing abilities.",            "u": "https://github.com/aradzie/keybr.com",           "w": "https://www.keybr.com",          "l": "AGPL-3",  "s": "4.4k",  "p": "Web",       "i": "Visit keybr.com"},
    {"n": "OpenRGB",             "c": "Utilities",    "d": "Universal open-source RGB lighting control. Keyboards, mice, motherboards, RAM. Cross-platform.",      "u": "https://gitlab.com/CalcProgrammer1/OpenRGB",     "w": "https://openrgb.org",            "l": "GPL-2",   "s": "4.1k",  "p": "Cross",     "i": "Download from openrgb.org"},
    {"n": "Keyboard Simulator",  "c": "Utilities",    "d": "3D keyboard simulator for visualizing layouts and colorways. Real keypress testing. Three.js.",       "u": "https://github.com/crsnbrt/keysim",              "w": "https://keyboardsimulator.xyz",  "l": "MIT",     "s": "1.0k",  "p": "Web",       "i": "Visit keyboardsimulator.xyz"},
    {"n": "InputScope",          "c": "Utilities",    "d": "Mouse and keyboard input heatmap visualizer. Tray program, SQLite database, web UI.",                "u": "https://github.com/suurjaak/InputScope",         "w": "",                                 "l": "MIT",     "s": "500",   "p": "Win/Lin",   "i": "pip install inputscope"},
    {"n": "Keyboard Inspector",  "c": "Utilities",    "d": "Record and analyze keyboard/mouse input data. Fourier analysis for polling rate detection.",          "u": "https://github.com/mat1jaczyyy/Keyboard-Inspector","w": "",                               "l": "Open",    "s": "300",   "p": "Windows",   "i": "Download from GitHub Releases"},
    {"n": "OSLTT",               "c": "Utilities",    "d": "Open-source latency testing tool. End-to-end keyboard/mouse/display latency measurement.",          "u": "https://github.com/TechteamGB/OSLTTCrossPlatform","w": "",                                "l": "Open",    "s": "200",   "p": "Windows",   "i": "Download from GitHub Releases"},
    {"n": "keyboard-tester.com", "c": "Utilities",    "d": "Simple web-based keyboard key tester. Press keys to see if they register correctly.",                  "u": "https://github.com/nasirazizawan009/keyboardtester-click","w": "https://keyboard-tester.com", "l": "MIT", "s": "50", "p": "Web", "i": "Visit keyboard-tester.com"},

    # ----- KEYCAPS -----
    {"n": "KeyV2",               "c": "Keycaps",      "d": "Parametric mechanical keycap library for OpenSCAD. DSA/DCS/SA/Cherry profiles, custom legends.",       "u": "https://github.com/rsheldiii/KeyV2",             "w": "",                                 "l": "GPL-3",   "s": "1.7k",  "p": "Cross",     "i": "OpenSCAD: open customizer.scad"},
    {"n": "OpenCherry Font",     "c": "Keycaps",      "d": "Open-source keycap font inspired by Cherry legends. For creating authentic keycap designs.",           "u": "https://github.com/dakotafelder/opencherry",     "w": "",                                 "l": "OFL",     "s": "70",    "p": "Cross",     "i": "Download font files from GitHub"},
    {"n": "joric/keycaps",       "c": "Keycaps",      "d": "Keyboard layout editor and 3D keycap renderer. OpenSCAD + THREE.js.",                                  "u": "https://github.com/joric/keycaps",               "w": "http://joric.github.io/keycaps", "l": "Public",  "s": "120",   "p": "Web",       "i": "Visit joric.github.io/keycaps"},
]

CATEGORIES = [
    ("Firmware",    "Keyboard firmware, bootloaders, configurators", "#e94560"),
    ("Layout",      "Layout editors and keymap generators",          "#0ea5e9"),
    ("CAD/PCB",     "PCB design, plate/case generators",             "#10b981"),
    ("Remappers",   "OS-level key remapping tools",                  "#f59e0b"),
    ("Utilities",   "Typing testers, RGB, diagnostics",              "#8b5cf6"),
    ("Keycaps",     "Keycap design and visualization",               "#ec4899"),
]


# =============================================================================
# CLI
# =============================================================================

def _find(name):
    name = name.lower()
    for t in TOOLS:
        if t["n"].lower() == name:
            return t
    matches = [t for t in TOOLS if name in t["n"].lower()]
    return matches[0] if len(matches) == 1 else None

def cmd_list(cat=None):
    if cat:
        tools = [t for t in TOOLS if t["c"].lower() == cat.lower()]
        if not tools:
            print(f"Category '{cat}' not found. Available:")
            for c, d, _ in CATEGORIES:
                n = len([t for t in TOOLS if t["c"] == c])
                print(f"  {c} ({n})")
            return
    else:
        tools = TOOLS
    for t in tools:
        stars = f" ({t['s']} stars)" if t['s'] != "N/A" else ""
        print(f"\n  [{t['c']}] {t['n']}{stars}")
        print(f"    {t['d'][:90]}")
        print(f"    {t['u']}")

def cmd_search(query):
    q = query.lower()
    found = []
    for t in TOOLS:
        score = 0
        if q == t["n"].lower(): score += 100
        if q in t["n"].lower(): score += 50
        if q in t["d"].lower(): score += 20
        if q in t["c"].lower(): score += 10
        if q in " ".join(t.get("t",[])).lower(): score += 15
        if q in t.get("p","").lower(): score += 5
        if score > 0:
            found.append((score, t))
    found.sort(key=lambda x: -x[0])
    if not found:
        print(f"No tools found for '{query}'")
        return
    for _, t in found[:20]:
        stars = f" ({t['s']} stars)" if t['s'] != "N/A" else ""
        print(f"\n  {t['n']}{stars}  [{t['c']}]  {t['p']}")
        print(f"    {t['d'][:100]}")
        url = t['w'] or t['u']
        print(f"    {url}")

def cmd_info(name):
    t = _find(name)
    if not t:
        print(f"Tool '{name}' not found. Try: python keyboard-toolkit.py search {name}")
        return
    print(f"\n  {'='*50}")
    print(f"  {t['n']}")
    print(f"  {'='*50}")
    print(f"  {t['d']}")
    print(f"  Category: {t['c']}  |  Platform: {t['p']}  |  License: {t['l']}")
    print(f"  Stars: {t['s']}")
    print(f"  GitHub: {t['u']}")
    if t['w']: print(f"  Web App: {t['w']}")
    print(f"  Install: {t['i']}")
    print(f"  {'='*50}\n")

def cmd_launch(name):
    t = _find(name)
    if not t:
        print(f"Tool '{name}' not found.")
        return
    url = t['w'] or t['u']
    print(f"Opening {t['n']}: {url}")
    webbrowser.open(url)

def cmd_categories():
    for c, d, _ in CATEGORIES:
        n = len([t for t in TOOLS if t["c"] == c])
        print(f"  {c} ({n}): {d}")

def run_cli():
    ap = argparse.ArgumentParser(description="Open Source Keyboard Toolkit")
    ap.add_argument("command", nargs="?", choices=["list","search","info","launch","categories"], help="Command")
    ap.add_argument("arg", nargs="?", help="Category name, search query, or tool name")
    ap.add_argument("--gui", action="store_true", help="Launch GUI")
    args = ap.parse_args()

    if args.gui:
        run_gui()
        return
    if args.command == "list" or (args.command is None and args.arg and args.command is None):
        cmd_list(args.arg)
    elif args.command == "search":
        cmd_search(args.arg or "")
    elif args.command == "info":
        cmd_info(args.arg or "")
    elif args.command == "launch":
        cmd_launch(args.arg or "")
    elif args.command == "categories":
        cmd_categories()
    else:
        # No args given - try GUI, fallback to help
        run_gui()


# =============================================================================
# GUI
# =============================================================================

def run_gui():
    if not TKINTER:
        print("ERROR: tkinter not available. Use CLI commands instead.")
        print("  python keyboard-toolkit.py list")
        print("  python keyboard-toolkit.py search <query>")
        sys.exit(1)

    root = Tk()
    root.title("Keyboard Toolkit")
    root.geometry("1200x820")
    root.configure(bg="#1a1a2e")

    # Fonts
    f_title = tkfont.Font(family="Helvetica", size=20, weight="bold")
    f_sub = tkfont.Font(family="Helvetica", size=13)
    f_card = tkfont.Font(family="Helvetica", size=14, weight="bold")
    f_desc = tkfont.Font(family="Helvetica", size=12)
    f_small = tkfont.Font(family="Helvetica", size=11)
    f_btn = tkfont.Font(family="Helvetica", size=12, weight="bold")

    # State
    current_cat = StringVar(value="All")
    search_var = StringVar()
    cards = []

    def build_cards(parent, tools_to_show):
        # Clear existing
        for c in cards:
            c.destroy()
        cards.clear()

        cols = 3 if root.winfo_width() > 900 else 2
        for i, t in enumerate(tools_to_show):
            card = Frame(parent, bg="#16213e", highlightbackground="#4a4a7e", highlightthickness=1)
            card.grid(row=i//cols, column=i%cols, padx=8, pady=8, sticky="nsew")
            cards.append(card)

            # Header: name + stars
            h = Frame(card, bg="#16213e")
            h.pack(fill=X, padx=10, pady=(10,0))
            Label(h, text=t["n"], font=f_card, bg="#16213e", fg="#ffffff", anchor="w").pack(side=LEFT)
            if t["s"] != "N/A":
                Label(h, text=f" {t['s']}", font=f_small, bg="#16213e", fg="#fbbf24").pack(side=RIGHT)

            # Category + License badges
            b = Frame(card, bg="#16213e")
            b.pack(fill=X, padx=10, pady=(2,0))
            cat_color = next((col for c,_,col in CATEGORIES if c == t["c"]), "#666")
            Label(b, text=f" {t['c']} ", font=f_small, bg=cat_color, fg="white").pack(side=LEFT)
            Label(b, text=f" {t['l']} ", font=f_small, bg="#2a2a5e", fg="#d0d8f0").pack(side=LEFT, padx=(4,0))
            Label(b, text=f" {t['p']} ", font=f_small, bg="#0f3460", fg="#a8d4ff").pack(side=RIGHT)

            # Description
            Label(card, text=t["d"], font=f_desc, bg="#16213e", fg="#c8d0e8",
                  wraplength=340 if cols==3 else 260, justify=LEFT, anchor="nw").pack(
                fill=X, padx=10, pady=(6,4))

            # Buttons
            btns = Frame(card, bg="#16213e")
            btns.pack(fill=X, padx=10, pady=(0,10))
            url = t["w"] or t["u"]

            def make_open(u):
                return lambda _: webbrowser.open(u)

            if t["w"]:
                btn = Label(btns, text=" Open Web App ", font=f_btn, bg="#0f3460", fg="#90cdf4",
                           cursor="hand2", relief="solid", bd=1)
                btn.pack(side=LEFT, padx=(0,4))
                btn.bind("<Button-1>", make_open(t["w"]))
                gh_btn = Label(btns, text=" GitHub ", font=f_btn, bg="#1a1a3e", fg="#b8c4d8",
                              cursor="hand2", relief="solid", bd=1)
                gh_btn.pack(side=LEFT, padx=(0,4))
                gh_btn.bind("<Button-1>", make_open(t["u"]))
            else:
                btn = Label(btns, text=" Open ", font=f_btn, bg="#0f3460", fg="#90cdf4",
                           cursor="hand2", relief="solid", bd=1)
                btn.pack(side=LEFT, padx=(0,4))
                btn.bind("<Button-1>", make_open(url))

            copy_btn = Label(btns, text=" Copy Install ", font=f_btn, bg="#1a1a3e", fg="#b8c4d8",
                            cursor="hand2", relief="solid", bd=1)
            copy_btn.pack(side=RIGHT)
            def make_copy(inst):
                return lambda _: copy_to_clipboard(inst)
            copy_btn.bind("<Button-1>", make_copy(t["i"]))

        # Configure grid weights
        for c in range(cols):
            parent.columnconfigure(c, weight=1)
        for r in range((len(tools_to_show) + cols - 1) // cols):
            parent.rowconfigure(r, weight=1)

    def copy_to_clipboard(text):
        try:
            if sys.platform == "darwin":
                subprocess.run(["pbcopy"], input=text.encode(), check=True)
            elif sys.platform == "win32":
                subprocess.run(["powershell", "-command", f"Set-Clipboard -Value '{text}'"], check=True)
            else:
                subprocess.run(["xclip", "-selection", "clipboard"], input=text.encode(), check=True)
        except Exception:
            pass
        status.config(text=f"Copied: {text[:60]}")
        root.after(3000, lambda: status.config(text=f"{len(TOOLS)} tools loaded | Select a category or search"))

    def refresh():
        cat = current_cat.get()
        q = search_var.get().lower()
        filtered = TOOLS
        if cat != "All":
            filtered = [t for t in filtered if t["c"] == cat]
        if q:
            filtered = [t for t in filtered if q in t["n"].lower() or q in t["d"].lower()
                        or q in t["c"].lower() or q in t.get("p","").lower()]
        count_label.config(text=f"Showing {len(filtered)} of {len(TOOLS)} tools")
        # Rebuild canvas
        canvas.yview_moveto(0)
        build_cards(grid_frame, filtered)

    # ---- LAYOUT ----
    # Top bar
    top = Frame(root, bg="#0d1b2a", height=60)
    top.pack(fill=X)
    top.pack_propagate(False)
    Label(top, text="Open Source Keyboard Toolkit", font=f_title, bg="#0d1b2a", fg="#ffffff").pack(side=LEFT, padx=20)

    search_frame = Frame(top, bg="#0d1b2a")
    search_frame.pack(side=RIGHT, padx=20)
    Label(search_frame, text="Search:", font=f_sub, bg="#0d1b2a", fg="#b8c4d8").pack(side=LEFT)
    search_entry = Entry(search_frame, textvariable=search_var, font=f_sub, bg="#0f3460", fg="#eaeaea",
                        insertbackground="#eaeaea", width=30, relief="flat")
    search_entry.pack(side=LEFT, padx=(5,0))
    search_var.trace("w", lambda *args: refresh())

    # Main area: sidebar + content
    main = Frame(root, bg="#1a1a2e")
    main.pack(fill=BOTH, expand=True)

    # Sidebar
    sidebar = Frame(main, bg="#0d1b2a", width=180)
    sidebar.pack(side=LEFT, fill=Y)
    sidebar.pack_propagate(False)

    Label(sidebar, text="Categories", font=f_sub, bg="#0d1b2a", fg="#b8c4d8").pack(pady=(15,5))

    cat_buttons = []
    def make_cat_btn(cat_name, color):
        def on_click():
            current_cat.set(cat_name)
            for btn_data in cat_buttons:
                b, c = btn_data
                if c == cat_name:
                    b.config(bg=color, fg="white", font=f_btn)
                else:
                    b.config(bg="#0d1b2a", fg="#b8c4d8", font=f_sub)
            refresh()
        return on_click

    # All button
    btn_all = Label(sidebar, text=f"All ({len(TOOLS)})", font=f_btn, bg="#0f3460", fg="white",
                    cursor="hand2", anchor="w", padx=15)
    btn_all.pack(fill=X, pady=2)
    btn_all.bind("<Button-1>", lambda e: make_cat_btn("All", "#0f3460")())
    cat_buttons.append((btn_all, "All"))

    for cat_name, cat_desc, cat_color in CATEGORIES:
        n = len([t for t in TOOLS if t["c"] == cat_name])
        btn = Label(sidebar, text=f"{cat_name} ({n})", font=f_sub, bg="#0d1b2a", fg="#b8c4d8",
                   cursor="hand2", anchor="w", padx=15)
        btn.pack(fill=X, pady=2)
        btn.bind("<Button-1>", lambda e, c=cat_name, col=cat_color: make_cat_btn(c, col)())
        cat_buttons.append((btn, cat_name))

    # Count label
    count_label = Label(sidebar, text=f"{len(TOOLS)} tools", font=f_small, bg="#0d1b2a", fg="#b8c4d8")
    count_label.pack(side=BOTTOM, pady=10)

    # Scrollable content area
    content_frame = Frame(main, bg="#1a1a2e")
    content_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)

    canvas = Canvas(content_frame, bg="#1a1a2e", highlightthickness=0)
    scrollbar = Scrollbar(content_frame, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side=RIGHT, fill=Y)
    canvas.pack(side=LEFT, fill=BOTH, expand=True)

    grid_frame = Frame(canvas, bg="#1a1a2e")
    canvas_window = canvas.create_window((0, 0), window=grid_frame, anchor="nw")

    def on_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
        canvas.itemconfig(canvas_window, width=event.width)
    grid_frame.bind("<Configure>", on_configure)
    canvas.bind("<Configure>", lambda e: canvas.itemconfig(canvas_window, width=e.width))

    # Status bar
    status = Frame(root, bg="#0d1b2a", height=25)
    status.pack(fill=X, side=BOTTOM)
    status.pack_propagate(False)
    status_label = Label(status, text=f"{len(TOOLS)} tools loaded | Select a category or search",
                         font=f_small, bg="#0d1b2a", fg="#b8c4d8")
    status_label.pack(side=LEFT, padx=10)

    # Mouse wheel scrolling
    def on_scroll(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    canvas.bind_all("<MouseWheel>", on_scroll)

    # Initial build
    refresh()

    root.mainloop()


# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_cli()
    else:
        run_gui()
