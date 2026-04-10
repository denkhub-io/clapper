#!/usr/bin/env python3
"""
clapper — Double clap to launch & tile your apps.
Run `clapper setup` to configure, then `start.sh` to listen.
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

# ─── SPOTIFY SEARCH ──────────────────────────────────────────────────────────

def search_spotify_track(query):
    """Cerca una canzone su Spotify tramite AppleScript e restituisce l'URI."""
    script = f'''
    tell application "Spotify"
        search "{query}"
    end tell
    '''
    # Spotify AppleScript non supporta search, usiamo l'approccio diretto:
    # apriamo la ricerca via URL
    safe_query = query.replace(" ", "%20")
    uri = f"spotify:search:{safe_query}"
    return uri

# ─── SETUP WIZARD ────────────────────────────────────────────────────────────

def setup():
    print()
    print("  ┌─────────────────────────────────┐")
    print("  │   CLAPPER SETUP                  │")
    print("  └─────────────────────────────────┘")
    print()

    cfg = {
        "apps": [],
        "spotify_track": "",
    }

    # Apps
    print("  Quali app vuoi aprire con il doppio clap?")
    print("  Scrivi solo il nome (es. WhatsApp, Safari, Claude)")
    print("  Riga vuota per terminare.")
    print()
    apps = []
    while True:
        name = input(f"    App #{len(apps)+1}: ").strip()
        if not name:
            if len(apps) < 2:
                print("    Serve almeno 2 app. Riprova.")
                continue
            break
        # Pulisci: se l'utente mette il path, estrai solo il nome
        if "/" in name:
            name = name.split("/")[-1].replace(".app", "").replace("\\", "")
        if name.endswith(".app"):
            name = name[:-4]
        apps.append(name)
    cfg["apps"] = apps

    # Spotify
    print()
    song = input("  Canzone da mettere su Spotify (es. Back in Black) o invio per saltare: ").strip()
    if song:
        # Cerca su Spotify via URL scheme
        safe_song = song.replace(" ", "%20")
        cfg["spotify_search"] = song
        cfg["spotify_uri"] = f"spotify:search:{safe_song}"

    save_config(cfg)

    # Preview
    n = len(apps)
    cols, rows = grid_shape(n)
    print(f"\n  Layout: {n} app in griglia {cols}x{rows}")
    print(f"  App: {', '.join(apps)}")
    if song:
        print(f"  Musica: {song}")
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
    script = 'tell application "Finder" to get bounds of window of desktop'
    out = subprocess.run(["osascript", "-e", script],
                         capture_output=True, text=True).stdout.strip()
    parts = [int(x.strip()) for x in out.split(",")]
    return parts[2], parts[3]

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

    for i, app in enumerate(apps):
        r = i // cols
        c = i % cols
        x = c * col_w
        y = menu + r * row_h

        apps_in_row = min(cols, n - r * cols)
        if apps_in_row < cols:
            col_w_adj = sw // apps_in_row
            c_adj = i - r * cols
            x = c_adj * col_w_adj
            w = col_w_adj
        else:
            w = col_w
        h = row_h

        script = f'''
        tell application "{app}" to activate
        delay 0.3
        tell application "System Events"
            tell process "{app}"
                try
                    set position of window 1 to {{{x}, {y}}}
                    set size of window 1 to {{{w}, {h}}}
                end try
            end tell
        end tell
        '''
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
        print(f"\U0001f3b8  Spotify: {cfg.get('spotify_search', '')}...")
        subprocess.run(["open", "-a", "Spotify"])
        time.sleep(2)
        subprocess.run(["open", cfg["spotify_uri"]])
        time.sleep(1)

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
    if cfg.get("spotify_search"):
        print(f"    Musica: {cfg['spotify_search']}")
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
