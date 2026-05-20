#!/usr/bin/env python3
import sys, os, time
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from tkinter import Frame, Label, Entry, StringVar, Canvas, Scrollbar, X, Y, BOTH, LEFT, RIGHT, TOP, BOTTOM, NSEW, NW, SUNKEN, FLAT, SOLID, RIDGE, GROOVE, NORMAL, DISABLED, END
from tkinter import Tk
from tkinter import font as tkfont
from PIL import ImageGrab
import webbrowser
import subprocess

# Inline the TOOLS and CATEGORIES to avoid import issues
TOOLS = [
    {"n": "QMK Firmware", "c": "Firmware", "d": "The standard open-source keyboard firmware. Supports 1000+ keyboards, layers, RGB, encoders, OLEDs.", "u": "https://github.com/qmk/qmk_firmware", "w": "", "l": "GPL-2", "s": "20.4k", "p": "Cross", "i": "qmk setup"},
    {"n": "Kanata", "c": "Remappers", "d": "Cross-platform key remapper with QMK-like layers, tap-hold, macros, mouse emulation.", "u": "https://github.com/jtroo/kanata", "w": "", "l": "LGPL-3", "s": "7.4k", "p": "Cross", "i": "cargo install kanata"},
    {"n": "Ergogen", "c": "Layout", "d": "Parametric keyboard generator. YAML config -> KiCad PCB, plates, 3D cases.", "u": "https://github.com/ergogen/ergogen", "w": "https://ergogen.xyz", "l": "MIT", "s": "1.5k", "p": "Cross", "i": "npm i -g ergogen"},
    {"n": "MonkeyType", "c": "Utilities", "d": "The most customizable typing test website. Multiple modes, progress tracking.", "u": "https://github.com/monkeytypegame/monkeytype", "w": "https://monkeytype.com", "l": "GPL-3", "s": "20.5k", "p": "Web", "i": "Visit monkeytype.com"},
    {"n": "OpenRGB", "c": "Utilities", "d": "Universal open-source RGB lighting control. Keyboards, mice, motherboards, RAM.", "u": "https://gitlab.com/CalcProgrammer1/OpenRGB", "w": "https://openrgb.org", "l": "GPL-2", "s": "4.1k", "p": "Cross", "i": "Download from openrgb.org"},
    {"n": "Keyboard Layout Editor", "c": "Layout", "d": "The standard web tool for designing keyboard layouts.", "u": "https://github.com/ijprest/keyboard-layout-editor", "w": "http://www.keyboard-layout-editor.com", "l": "MIT", "s": "3.0k", "p": "Web", "i": "Visit keyboard-layout-editor.com"},
    {"n": "AutoHotkey", "c": "Remappers", "d": "The dominant Windows scripting/automation utility.", "u": "https://github.com/AutoHotkey/AutoHotkey", "w": "https://www.autohotkey.com", "l": "GPL-2", "s": "12.4k", "p": "Windows", "i": "winget install AutoHotkey.AutoHotkey"},
    {"n": "KeyV2", "c": "Keycaps", "d": "Parametric mechanical keycap library for OpenSCAD.", "u": "https://github.com/rsheldiii/KeyV2", "w": "", "l": "GPL-3", "s": "1.7k", "p": "Cross", "i": "OpenSCAD: open customizer.scad"},
    {"n": "KiCad EDA", "c": "CAD/PCB", "d": "Industry-standard open-source PCB design suite.", "u": "https://gitlab.com/kicad/code/kicad", "w": "https://www.kicad.org", "l": "GPL-3", "s": "N/A", "p": "Cross", "i": "Download from kicad.org/download"},
    {"n": "Karabiner-Elements", "c": "Remappers", "d": "The most powerful macOS keyboard customization tool.", "u": "https://github.com/pqrs-org/Karabiner-Elements", "w": "https://karabiner-elements.pqrs.org", "l": "BSD-3", "s": "18.5k", "p": "macOS", "i": "brew install --cask karabiner-elements"},
    {"n": "VIAL", "c": "Firmware", "d": "Real-time keyboard configurator. Open-source alternative to VIA.", "u": "https://github.com/vial-kb/vial-gui", "w": "https://get.vial.today", "l": "GPL-2", "s": "1.3k", "p": "Cross", "i": "Download from get.vial.today"},
    {"n": "Keyboard Simulator", "c": "Utilities", "d": "3D keyboard simulator for visualizing layouts and colorways.", "u": "https://github.com/crsnbrt/keysim", "w": "https://keyboardsimulator.xyz", "l": "MIT", "s": "1.0k", "p": "Web", "i": "Visit keyboardsimulator.xyz"},
]
CATEGORIES = [
    ("Firmware", "Keyboard firmware, bootloaders, configurators", "#e94560"),
    ("Layout", "Layout editors and keymap generators", "#0ea5e9"),
    ("CAD/PCB", "PCB design, plate/case generators", "#10b981"),
    ("Remappers", "OS-level key remapping tools", "#f59e0b"),
    ("Utilities", "Typing testers, RGB, diagnostics", "#8b5cf6"),
    ("Keycaps", "Keycap design and visualization", "#ec4899"),
]

root = Tk()
root.title("Keyboard Toolkit")
root.geometry("1100x720")
root.configure(bg="#1a1a2e")

f_title = tkfont.Font(family="Helvetica", size=16, weight="bold")
f_sub = tkfont.Font(family="Helvetica", size=10)
f_card = tkfont.Font(family="Helvetica", size=11, weight="bold")
f_desc = tkfont.Font(family="Helvetica", size=9)
f_small = tkfont.Font(family="Helvetica", size=8)
f_btn = tkfont.Font(family="Helvetica", size=9, weight="bold")

current_cat = StringVar(value="All")
search_var = StringVar()
cards = []

def build_cards(parent, tools_to_show):
    for c in cards:
        c.destroy()
    cards.clear()
    cols = 3
    for i, t in enumerate(tools_to_show):
        card = Frame(parent, bg="#16213e", highlightbackground="#2a2a4e", highlightthickness=1)
        card.grid(row=i//cols, column=i%cols, padx=8, pady=8, sticky="nsew")
        cards.append(card)
        h = Frame(card, bg="#16213e")
        h.pack(fill=X, padx=10, pady=(10,0))
        Label(h, text=t["n"], font=f_card, bg="#16213e", fg="#eaeaea", anchor="w").pack(side=LEFT)
        if t["s"] != "N/A":
            Label(h, text=f" {t['s']}", font=f_small, bg="#16213e", fg="#fbbf24").pack(side=RIGHT)
        b = Frame(card, bg="#16213e")
        b.pack(fill=X, padx=10, pady=(2,0))
        cat_color = next((col for c,_,col in CATEGORIES if c == t["c"]), "#666")
        Label(b, text=f" {t['c']} ", font=f_small, bg=cat_color, fg="white").pack(side=LEFT)
        Label(b, text=f" {t['l']} ", font=f_small, bg="#1a1a3e", fg="#a0a0b0").pack(side=LEFT, padx=(4,0))
        Label(b, text=f" {t['p']} ", font=f_small, bg="#0f3460", fg="#90cdf4").pack(side=RIGHT)
        Label(card, text=t["d"], font=f_desc, bg="#16213e", fg="#a0a0b0",
              wraplength=300, justify=LEFT, anchor="nw").pack(fill=X, padx=10, pady=(6,4))
        btns = Frame(card, bg="#16213e")
        btns.pack(fill=X, padx=10, pady=(0,10))
        url = t["w"] or t["u"]
        if t["w"]:
            Label(btns, text=" Open Web App ", font=f_btn, bg="#0f3460", fg="#90cdf4",
                  cursor="hand2", relief="solid", bd=1).pack(side=LEFT, padx=(0,4))
            Label(btns, text=" GitHub ", font=f_btn, bg="#1a1a3e", fg="#a0a0b0",
                  cursor="hand2", relief="solid", bd=1).pack(side=LEFT, padx=(0,4))
        else:
            Label(btns, text=" Open ", font=f_btn, bg="#0f3460", fg="#90cdf4",
                  cursor="hand2", relief="solid", bd=1).pack(side=LEFT, padx=(0,4))
        Label(btns, text=" Copy Install ", font=f_btn, bg="#1a1a3e", fg="#a0a0b0",
              cursor="hand2", relief="solid", bd=1).pack(side=RIGHT)
    for c in range(cols):
        parent.columnconfigure(c, weight=1)

def refresh():
    cat = current_cat.get()
    q = search_var.get().lower()
    filtered = TOOLS
    if cat != "All":
        filtered = [t for t in filtered if t["c"] == cat]
    if q:
        filtered = [t for t in filtered if q in t["n"].lower() or q in t["d"].lower() or q in t["c"].lower()]
    count_label.config(text=f"Showing {len(filtered)} of {len(TOOLS)} tools")
    canvas.yview_moveto(0)
    build_cards(grid_frame, filtered)

# Top bar
top = Frame(root, bg="#0d1b2a", height=60)
top.pack(fill=X)
top.pack_propagate(False)
Label(top, text="Open Source Keyboard Toolkit", font=f_title, bg="#0d1b2a", fg="#eaeaea").pack(side=LEFT, padx=20)
search_frame = Frame(top, bg="#0d1b2a")
search_frame.pack(side=RIGHT, padx=20)
Label(search_frame, text="Search:", font=f_sub, bg="#0d1b2a", fg="#a0a0b0").pack(side=LEFT)
Entry(search_frame, textvariable=search_var, font=f_sub, bg="#0f3460", fg="#eaeaea",
      insertbackground="#eaeaea", width=30, relief="flat").pack(side=LEFT, padx=(5,0))

# Main
main = Frame(root, bg="#1a1a2e")
main.pack(fill=BOTH, expand=True)

sidebar = Frame(main, bg="#0d1b2a", width=180)
sidebar.pack(side=LEFT, fill=Y)
sidebar.pack_propagate(False)
Label(sidebar, text="Categories", font=f_sub, bg="#0d1b2a", fg="#a0a0b0").pack(pady=(15,5))

Label(sidebar, text=f"All ({len(TOOLS)})", font=f_btn, bg="#0f3460", fg="white",
      anchor="w", padx=15).pack(fill=X, pady=2)
for cat_name, cat_desc, cat_color in CATEGORIES:
    n = len([t for t in TOOLS if t["c"] == cat_name])
    Label(sidebar, text=f"{cat_name} ({n})", font=f_sub, bg="#0d1b2a", fg="#a0a0b0",
          anchor="w", padx=15).pack(fill=X, pady=2)

count_label = Label(sidebar, text=f"{len(TOOLS)} tools", font=f_small, bg="#0d1b2a", fg="#a0a0b0")
count_label.pack(side=BOTTOM, pady=10)

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

status = Frame(root, bg="#0d1b2a", height=25)
status.pack(fill=X, side=BOTTOM)
status.pack_propagate(False)
Label(status, text=f"{len(TOOLS)} tools loaded | Select a category or search",
      font=f_small, bg="#0d1b2a", fg="#a0a0b0").pack(side=LEFT, padx=10)

refresh()

# Screenshot
root.update()
time.sleep(0.5)
root.update()
x, y, w, h = root.winfo_rootx(), root.winfo_rooty(), root.winfo_width(), root.winfo_height()
img = ImageGrab.grab(bbox=(x, y, x+w, y+h))
img.save('/mnt/agents/output/keyboard-toolkit-simple/gui_screenshot.png')
print(f"Screenshot saved: {w}x{h}")
root.destroy()
