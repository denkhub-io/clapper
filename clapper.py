#!/usr/bin/env python3
"""
clapper.py — Double clap → Back in Black + AI apps tiled
"""

import os
import sounddevice as sd
import numpy as np
import subprocess
import threading
import time

# ─── CONFIG ────────────────────────────────────────────────────────────────────
CLAP_THRESHOLD  = 0.10   # abbassa se non rileva, alza se troppi falsi positivi
DOUBLE_CLAP_MAX = 1.2    # secondi max tra i due clap
CLAP_DEBOUNCE   = 0.08   # secondi minimi tra un clap e l'altro
COOLDOWN        = 4.0    # pausa prima del prossimo trigger

SPOTIFY_TRACK_URI = "spotify:track:08mG3Y1vljYA6bvDt4Wqkj"

# Layout:  top 2  →  Claude | ChatGPT
#          bot 2  →  Codex  | Antigravity
APPS_TOP = ["Claude", "ChatGPT"]
APPS_BOT = ["Codex", "Antigravity"]
# ───────────────────────────────────────────────────────────────────────────────

def get_screen_size():
    script = 'tell application "Finder" to get bounds of window of desktop'
    out = subprocess.run(["osascript", "-e", script],
                         capture_output=True, text=True).stdout.strip()
    # "0, 0, 1512, 982"
    parts = [int(x.strip()) for x in out.split(",")]
    return parts[2], parts[3]   # width, height

def arrange_windows():
    sw, sh = get_screen_size()
    menu    = 37
    dock    = 72
    avail_h = sh - menu - dock
    row_h   = avail_h // 2
    col2    = sw // 2

    layout = [
        (APPS_TOP[0], 0,    menu,          col2, row_h),
        (APPS_TOP[1], col2, menu,          col2, row_h),
        (APPS_BOT[0], 0,    menu + row_h,  col2, row_h),
        (APPS_BOT[1], col2, menu + row_h,  col2, row_h),
    ]

    # Attiva tutte le app prima, poi posiziona ciascuna
    for app, x, y, w, h in layout:
        script = f'''
        tell application "{app}" to activate
        delay 0.5
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

def say(text):
    subprocess.Popen(["say", "-v", "Luca", text])

def trigger():
    print("\n\U0001f44f  Doppio clap! Avvio...\n")

    # TTS apertura
    say("Inizializzazione sistemi in corso")

    # 1. Spotify + Back in Black
    print("\U0001f3b8  Spotify...")
    subprocess.run(["open", "-a", "Spotify"])
    time.sleep(2)
    subprocess.run(["osascript", "-e",
        f'tell application "Spotify" to play track "{SPOTIFY_TRACK_URI}"'])
    time.sleep(0.5)

    # 2. App AI
    for app in APPS_TOP + [a for a in APPS_BOT if a != "Spotify"]:
        result = subprocess.run(["open", "-a", app],
                                capture_output=True, text=True)
        if result.returncode != 0:
            print(f"   \u26a0\ufe0f  '{app}' non trovata")
        time.sleep(0.3)

    # 3. Aspetta che le finestre siano cariche poi tilea
    print("\U0001fa9f  Disposizione finestre...")
    time.sleep(3)
    arrange_windows()

    # TTS chiusura
    say("Operativo")
    print("\u2705  Let there be rock.\n")

def main():
    print("\U0001f44f  In ascolto — doppio clap per triggerare")
    print("    Ctrl+C per uscire\n")

    last_clap      = 0.0
    clap_count     = 0
    fired          = threading.Event()
    trigger_thread = None

    def callback(indata, frames, time_info, status):
        nonlocal last_clap, clap_count, trigger_thread

        if fired.is_set():
            return

        rms = float(np.sqrt(np.mean(indata ** 2)))
        now = time.time()

        if rms > CLAP_THRESHOLD:
            if now - last_clap < CLAP_DEBOUNCE:
                return

            gap       = now - last_clap
            last_clap = now

            clap_count = (clap_count + 1) if gap <= DOUBLE_CLAP_MAX else 1
            print(f"  clap #{clap_count}  (rms={rms:.3f})")

            if clap_count >= 2:
                fired.set()
                trigger_thread = threading.Thread(target=trigger)
                trigger_thread.start()

    with sd.InputStream(callback=callback, channels=1,
                        samplerate=44100, blocksize=512):
        try:
            fired.wait()
        except KeyboardInterrupt:
            print("\n\U0001f44b  Clapper fermato.")

    # stream chiuso, aspetta che trigger finisca prima di uscire
    if trigger_thread:
        trigger_thread.join()


if __name__ == "__main__":
    main()