#!/usr/bin/env python3
"""
clapper — Double clap to launch & tile your apps.
"""

import json
import math
import os
import subprocess
import sys
import threading
import time

import numpy as np
import sounddevice as sd

CONFIG_PATH = os.path.expanduser("~/.clapper.json")

# ─── CONFIG ──────────────────────────────────────────────────────────────────

def load_config():
    if not os.path.exists(CONFIG_PATH):
        return None
    with open(CONFIG_PATH) as f:
        return json.load(f)

def save_config(cfg):
    with open(CONFIG_PATH, "w") as f:
        json.dump(cfg, f, indent=2)
    print(f"\n  Configurazione salvata in {CONFIG_PATH}")

# ─── SETUP WIZARD ────────────────────────────────────────────────────────────

def clean_app_name(raw):
    """Estrae il nome app da qualsiasi input: path, .app, drag & drop."""
    raw = raw.strip().rstrip("/")
    # Rimuovi escape e virgolette dal drag & drop
    raw = raw.replace("\\", "").strip("'\"")
    # Se è un path, prendi solo il nome
    if "/" in raw:
        raw = raw.split("/")[-1]
    # Rimuovi .app
    if raw.endswith(".app"):
        raw = raw[:-4]
    return raw

def parse_spotify_link(raw):
    """Converte un link Spotify in URI. Accetta link o URI."""
    raw = raw.strip()
    if not raw:
        return None
    # https://open.spotify.com/track/4OHVCeQYPncEwZOtNAJZZx?si=xxx
    if "open.spotify.com" in raw:
        # Estrai tipo e ID dal path
        parts = raw.split("open.spotify.com/")[1].split("?")[0]
        # parts = "track/4OHVCeQYPncEwZOtNAJZZx"
        return "spotify:" + parts.replace("/", ":")
    # Già un URI spotify:track:xxx
    if raw.startswith("spotify:"):
        return raw
    return None

def setup():
    print()
    print("  ┌─────────────────────────────────┐")
    print("  │   CLAPPER SETUP                  │")
    print("  └─────────────────────────────────┘")
    print()

    cfg = {"apps": [], "spotify_uri": ""}

    # Apps
    print("  Quali app vuoi aprire con il doppio clap?")
    print("  Trascina le app qui dentro, oppure scrivi il nome.")
    print("  Riga vuota per terminare.")
    print()
    apps = []
    while True:
        raw = input(f"    App #{len(apps)+1}: ").strip()
        if not raw:
            if len(apps) < 2:
                print("    Serve almeno 2 app. Riprova.")
                continue
            break
        name = clean_app_name(raw)
        if name:
            apps.append(name)
            print(f"             → {name}")
    cfg["apps"] = apps

    # Spotify
    print()
    print("  Canzone Spotify: apri Spotify, tasto destro sulla canzone")
    print("  → Condividi → Copia link, e incollalo qui.")
    link = input("  Link (o invio per saltare): ").strip()
    uri = parse_spotify_link(link)
    if uri:
        cfg["spotify_uri"] = uri
        print(f"             → {uri}")

    save_config(cfg)

    n = len(apps)
    cols, rows = grid_shape(n)
    print(f"\n  Layout: {n} app in griglia {cols}x{rows}")
    print(f"  App: {', '.join(apps)}")
    if uri:
        print(f"  Musica: attiva")
    print("\n  Esegui 'bash start.sh' per avviare.\n")

# ─── TILING ──────────────────────────────────────────────────────────────────

def grid_shape(n):
    if n <= 1:
        return 1, 1
    if n == 2:
        return 2, 1
    if n == 3:
        return 3, 1
    cols = math.ceil(math.sqrt(n))
    rows = math.ceil(n / cols)
    return cols, rows

def get_screen_size():
    script = '''
    tell application "Finder"
        set _b to bounds of window of desktop
        set _w to item 3 of _b
        set _h to item 4 of _b
        return ((_w as text) & "," & (_h as text))
    end tell
    '''
    out = subprocess.run(["osascript", "-e", script],
                         capture_output=True, text=True).stdout.strip()
    parts = out.split(",")
    return int(parts[0]), int(parts[1])

def arrange_windows(apps):
    n = len(apps)
    if n == 0:
        return

    sw, sh = get_screen_size()
    menu = 37
    dock = 72
    avail_h = sh - menu - dock

    cols, rows = grid_shape(n)
    col_w = sw // cols
    row_h = avail_h // rows

    # Costruisco un unico AppleScript per tutte le finestre (più veloce e affidabile)
    lines = []
    for i, app in enumerate(apps):
        r = i // cols
        c = i % cols

        # Ultima riga: allarga se ha meno app
        apps_in_row = min(cols, n - r * cols)
        if apps_in_row < cols:
            w = sw // apps_in_row
            x = (i - r * cols) * w
        else:
            w = col_w
            x = c * col_w
        y = menu + r * row_h
        h = row_h

        lines.append(f'''
        tell application "{app}" to activate
        delay 0.5
        try
            tell application "System Events" to tell (first process whose frontmost is true)
                set position of window 1 to {{{x}, {y}}}
                set size of window 1 to {{{w}, {h}}}
            end tell
        end try
        delay 0.2
        ''')

    script = "\n".join(lines)
    subprocess.run(["osascript", "-e", script], capture_output=True)

# ─── TRIGGER ─────────────────────────────────────────────────────────────────

def say(text):
    subprocess.Popen(["say", "-v", "Luca", text])

def trigger(cfg):
    apps = cfg["apps"]
    print(f"\n\U0001f44f  Doppio clap! Avvio {len(apps)} app...\n")

    say("Inizializzazione sistemi in corso")

    # Spotify
    if cfg.get("spotify_uri"):
        print("\U0001f3b8  Spotify...")
        subprocess.run(["open", "-a", "Spotify"])
        time.sleep(2)
        subprocess.run(["osascript", "-e",
            f'tell application "Spotify" to play track "{cfg["spotify_uri"]}"'])
        time.sleep(0.5)

    # Apri le app
    for app in apps:
        print(f"    Apro {app}...")
        result = subprocess.run(["open", "-a", app], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"    \u26a0\ufe0f  '{app}' non trovata")
        time.sleep(0.3)

    # Tiling
    print("\U0001fa9f  Disposizione finestre...")
    time.sleep(3)
    arrange_windows(apps)

    say("Operativo")
    print("\u2705  Pronto.\n")

# ─── LISTENER ────────────────────────────────────────────────────────────────

def listen(cfg):
    n = len(cfg["apps"])
    cols, rows = grid_shape(n)
    print(f"\U0001f44f  Clapper attivo — {n} app in griglia {cols}x{rows}")
    print(f"    App: {', '.join(cfg['apps'])}")
    if cfg.get("spotify_uri"):
        print(f"    Musica: attiva")
    print("    Doppio clap per triggerare, Ctrl+C per uscire\n")

    last_clap = 0.0
    clap_count = 0
    fired = threading.Event()
    trigger_thread = None

    def callback(indata, frames, time_info, status):
        nonlocal last_clap, clap_count, trigger_thread

        if fired.is_set():
            return

        rms = float(np.sqrt(np.mean(indata ** 2)))
        now = time.time()

        if rms > 0.10:
            if now - last_clap < 0.08:
                return

            gap = now - last_clap
            last_clap = now
            clap_count = (clap_count + 1) if gap <= 1.2 else 1
            print(f"  clap #{clap_count}  (rms={rms:.3f})")

            if clap_count >= 2:
                fired.set()
                trigger_thread = threading.Thread(target=trigger, args=(cfg,))
                trigger_thread.start()

    with sd.InputStream(callback=callback, channels=1,
                        samplerate=44100, blocksize=512):
        try:
            fired.wait()
        except KeyboardInterrupt:
            print("\n\U0001f44b  Clapper fermato.")

    if trigger_thread:
        trigger_thread.join()

# ─── MAIN ────────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "setup":
        setup()
        return

    cfg = load_config()
    if cfg is None or not cfg.get("apps"):
        print("  Nessuna configurazione trovata. Avvio setup...\n")
        setup()
        cfg = load_config()
        if cfg is None or not cfg.get("apps"):
            return

    listen(cfg)

if __name__ == "__main__":
    main()
