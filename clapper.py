#!/usr/bin/env python3
"""
clapper — Double clap to launch & tile your apps.
Works on macOS and Windows.
"""

import json
import math
import os
import platform
import subprocess
import sys
import threading
import time

import numpy as np
import sounddevice as sd

IS_MAC = platform.system() == "Darwin"
IS_WIN = platform.system() == "Windows"

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

# ─── TTS ─────────────────────────────────────────────────────────────────────

_tts_engine = None

def _get_tts_engine():
    global _tts_engine
    if _tts_engine is None and IS_WIN:
        import pyttsx3
        _tts_engine = pyttsx3.init()
        # Prova a impostare una voce italiana
        for voice in _tts_engine.getProperty("voices"):
            if "italian" in voice.name.lower() or "it" in voice.id.lower():
                _tts_engine.setProperty("voice", voice.id)
                break
    return _tts_engine

def say(text, wait=False):
    if IS_MAC:
        p = subprocess.Popen(["say", "-v", "Luca", text])
        if wait:
            p.wait()
    elif IS_WIN:
        engine = _get_tts_engine()
        if wait:
            engine.say(text)
            engine.runAndWait()
        else:
            threading.Thread(target=lambda: (engine.say(text), engine.runAndWait())).start()

def typewrite(text, delay=0.03):
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write("\n")
    sys.stdout.flush()

def speak_and_show(text, voice_text=None, delay=0.03):
    if IS_MAC:
        p = subprocess.Popen(["say", "-v", "Luca", voice_text or text])
        typewrite(f"  {text}", delay)
        p.wait()
    elif IS_WIN:
        engine = _get_tts_engine()
        t = threading.Thread(target=lambda: (engine.say(voice_text or text), engine.runAndWait()))
        t.start()
        typewrite(f"  {text}", delay)
        t.join()
    else:
        typewrite(f"  {text}", delay)

# ─── SETUP WIZARD ────────────────────────────────────────────────────────────

def clean_app_name(raw):
    """Estrae il nome app da qualsiasi input: path, .app, .exe, drag & drop."""
    raw = raw.strip().rstrip("/")
    raw = raw.replace("\\", "/").strip("'\"")
    if "/" in raw:
        raw = raw.split("/")[-1]
    if raw.endswith(".app"):
        raw = raw[:-4]
    if raw.endswith(".exe"):
        raw = raw[:-4]
    # Su Windows, rimuovi .lnk (shortcut)
    if raw.endswith(".lnk"):
        raw = raw[:-4]
    return raw

def parse_spotify_link(raw):
    raw = raw.strip()
    if not raw:
        return None
    if "open.spotify.com" in raw:
        parts = raw.split("open.spotify.com/")[1].split("?")[0]
        return "spotify:" + parts.replace("/", ":")
    if raw.startswith("spotify:"):
        return raw
    return None

def setup():
    print()
    cfg = {"apps": [], "spotify_uri": ""}

    speak_and_show(
        "Ciao! Benvenuto nella configurazione di Clapper.",
        "Ciao! Benvenuto nella configurazione di Clapper."
    )
    time.sleep(0.5)
    speak_and_show(
        "Sarò il tuo assistente. Configuriamo tutto insieme.",
        "Sarò il tuo assistente. Configuriamo tutto insieme."
    )
    time.sleep(1)

    print()
    speak_and_show(
        "Per prima cosa, dimmi quali app vuoi far partire.",
        "Per prima cosa, dimmi quali app vuoi far partire."
    )
    time.sleep(0.3)
    speak_and_show(
        "Trascina le app qui dentro, oppure scrivi il nome, e premi invio.",
        "Trascina le app qui dentro, oppure scrivi il nome, e premi invio."
    )
    speak_and_show(
        "Quando hai finito, premi invio a vuoto e andiamo avanti.",
        "Quando hai finito, premi invio a vuoto e andiamo avanti."
    )
    print()

    apps = []
    while True:
        raw = input(f"    App #{len(apps)+1}: ").strip()
        if not raw:
            if len(apps) < 2:
                say("Dai, servono almeno due app.", wait=True)
                print("    Serve almeno 2 app. Riprova.")
                continue
            break
        name = clean_app_name(raw)
        if name:
            apps.append(name)
            say(f"{name}, perfetto.", wait=True)
            typewrite(f"             → {name}")
    cfg["apps"] = apps

    n = len(apps)
    speak_and_show(
        f"Ottimo, {n} app registrate. Bella scelta.",
        f"Ottimo, {n} app registrate. Bella scelta."
    )
    time.sleep(0.5)

    print()
    speak_and_show(
        "Ora la parte divertente: la musica.",
        "Ora la parte divertente. La musica."
    )
    time.sleep(0.3)
    speak_and_show(
        "Se vuoi, incolla qui il link di una canzone da Spotify.",
        "Se vuoi, incolla qui il link di una canzone da Spotify."
    )
    speak_and_show(
        "Lo trovi con tasto destro sulla canzone, Condividi, Copia link.",
        "Lo trovi con tasto destro sulla canzone, poi condividi, e copia link."
    )
    print()
    link = input("    Link Spotify (o invio per saltare): ").strip()
    uri = parse_spotify_link(link)
    if uri:
        cfg["spotify_uri"] = uri
        say("Canzone registrata. Ottima scelta musicale.", wait=True)
        typewrite(f"             → {uri}")
    else:
        say("Nessun problema, si va anche senza musica.", wait=True)
        typewrite("             → nessuna canzone")

    save_config(cfg)

    print()
    time.sleep(0.5)
    cols, rows = grid_shape(n)
    speak_and_show(
        f"Tutto pronto. Le tue {n} app saranno disposte in una griglia {cols} per {rows}.",
        f"Tutto pronto. Le tue {n} app saranno disposte in una griglia {cols} per {rows}."
    )
    time.sleep(0.3)
    print(f"    App: {', '.join(apps)}")
    if uri:
        print(f"    Musica: attiva")

    print()
    speak_and_show(
        "Ora parto in automatico. Batti le mani due volte e ci penso io!",
        "Ora parto in automatico. Batti le mani due volte, e ci penso io!"
    )
    print()

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
    if IS_MAC:
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
    elif IS_WIN:
        import ctypes
        user32 = ctypes.windll.user32
        return user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

def open_app(name):
    if IS_MAC:
        return subprocess.run(["open", "-a", name], capture_output=True, text=True)
    elif IS_WIN:
        return subprocess.run(["start", "", name], shell=True, capture_output=True, text=True)

def arrange_windows(apps):
    n = len(apps)
    if n == 0:
        return

    sw, sh = get_screen_size()

    if IS_MAC:
        menu = 37
        dock = 72
        avail_h = sh - menu - dock
        top_offset = menu
    elif IS_WIN:
        taskbar = 48
        avail_h = sh - taskbar
        top_offset = 0

    cols, rows = grid_shape(n)
    col_w = sw // cols
    row_h = avail_h // rows

    if IS_MAC:
        lines = []
        for i, app in enumerate(apps):
            r = i // cols
            c = i % cols

            apps_in_row = min(cols, n - r * cols)
            if apps_in_row < cols:
                w = sw // apps_in_row
                x = (i - r * cols) * w
            else:
                w = col_w
                x = c * col_w
            y = top_offset + r * row_h
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

    elif IS_WIN:
        import ctypes
        user32 = ctypes.windll.user32

        # Trova le finestre per nome app
        import ctypes.wintypes
        EnumWindows = user32.EnumWindows
        WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.wintypes.HWND, ctypes.wintypes.LPARAM)
        GetWindowText = user32.GetWindowTextW
        GetWindowTextLength = user32.GetWindowTextLengthW
        IsWindowVisible = user32.IsWindowVisible
        MoveWindow = user32.MoveWindow

        def find_window(app_name):
            """Trova la prima finestra visibile il cui titolo contiene app_name."""
            result = []
            def callback(hwnd, _):
                if IsWindowVisible(hwnd):
                    length = GetWindowTextLength(hwnd)
                    if length > 0:
                        buf = ctypes.create_unicode_buffer(length + 1)
                        GetWindowText(hwnd, buf, length + 1)
                        if app_name.lower() in buf.value.lower():
                            result.append(hwnd)
                            return False
                return True
            EnumWindows(WNDENUMPROC(callback), 0)
            return result[0] if result else None

        for i, app in enumerate(apps):
            r = i // cols
            c = i % cols

            apps_in_row = min(cols, n - r * cols)
            if apps_in_row < cols:
                w = sw // apps_in_row
                x = (i - r * cols) * w
            else:
                w = col_w
                x = c * col_w
            y = top_offset + r * row_h
            h = row_h

            hwnd = find_window(app)
            if hwnd:
                MoveWindow(hwnd, x, y, w, h, True)

# ─── TRIGGER ─────────────────────────────────────────────────────────────────

def trigger(cfg):
    apps = cfg["apps"]
    print(f"\n\U0001f44f  Doppio clap! Avvio {len(apps)} app...\n")

    say("Inizializzazione sistemi in corso")

    # Spotify
    if cfg.get("spotify_uri"):
        print("\U0001f3b8  Spotify...")
        if IS_MAC:
            subprocess.run(["open", "-a", "Spotify"])
            time.sleep(2)
            subprocess.run(["osascript", "-e",
                f'tell application "Spotify" to play track "{cfg["spotify_uri"]}"'])
        elif IS_WIN:
            subprocess.run(["start", "", "spotify"], shell=True)
            time.sleep(3)
            subprocess.run(["start", "", cfg["spotify_uri"]], shell=True)
        time.sleep(0.5)

    # Apri le app
    for app in apps:
        print(f"    Apro {app}...")
        result = open_app(app)
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
        setup()
        cfg = load_config()
        if cfg is None or not cfg.get("apps"):
            return

    listen(cfg)

if __name__ == "__main__":
    main()
