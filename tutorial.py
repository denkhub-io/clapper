#!/usr/bin/env python3
"""
tutorial.py — Tutorial interattivo JARVIS per clapper.py
Spiega passo-passo come ricreare il programma sul tuo Mac.
Il codice mostrato e IDENTICO a clapper.py — copia-incollabile.
"""

import os
import sys
import time
import subprocess
import shutil
import threading as _thr

# ─── COLORI ANSI ──────────────────────────────────────────────────────────────
RESET   = "\033[0m"
BOLD    = "\033[1m"
GREEN   = "\033[38;5;46m"
CYAN    = "\033[38;5;51m"
YELLOW  = "\033[38;5;220m"
WHITE   = "\033[38;5;255m"
ORANGE  = "\033[38;5;208m"
# ──────────────────────────────────────────────────────────────────────────────

TTS_VOICE = "Alice"


def clear():
    os.system("clear")


def narrate(display_text, spoken_text=None):
    """Mostra testo a schermo MENTRE Alice parla."""
    if spoken_text is None:
        spoken_text = display_text

    # Spezza in frasi per evitare che say si blocchi
    sentences = []
    for s in spoken_text.replace(". ", ".|").replace(", ", ",|").split("|"):
        s = s.strip()
        if s:
            sentences.append(s)

    def _speak():
        for sentence in sentences:
            subprocess.run(["say", "-v", TTS_VOICE, sentence],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    tts_thread = _thr.Thread(target=_speak, daemon=True)
    tts_thread.start()

    CHAR_DELAY = 0.048   # ~21 caratteri/secondo
    LINE_PAUSE = 0.15

    lines = display_text.split("\n")
    for i, line in enumerate(lines):
        for ch in line:
            sys.stdout.write(f"{WHITE}{BOLD}{ch}{RESET}")
            sys.stdout.flush()
            time.sleep(CHAR_DELAY)
        if i < len(lines) - 1:
            time.sleep(LINE_PAUSE)
            print()

    print()
    tts_thread.join()


def say_only(text):
    """TTS bloccante senza testo a schermo."""
    sentences = []
    for s in text.replace(". ", ".|").replace(", ", ",|").split("|"):
        s = s.strip()
        if s:
            sentences.append(s)
    for sentence in sentences:
        subprocess.run(["say", "-v", TTS_VOICE, sentence],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def wait_enter():
    print()
    print(f"  {GREEN}{'─' * 50}{RESET}")
    input(f"  {WHITE}Premi {GREEN}{BOLD}INVIO{RESET}{WHITE} per continuare...{RESET}  ")


def print_header(title):
    cols = shutil.get_terminal_size().columns
    w = min(cols - 4, 70)
    print()
    print(f"  {GREEN}{BOLD}{'━' * w}{RESET}")
    print(f"  {GREEN}{BOLD}  {title}{RESET}")
    print(f"  {GREEN}{BOLD}{'━' * w}{RESET}")
    print()


def print_code(lines):
    """Mostra codice SENZA indentazione — parte da colonna 0, copiabile."""
    print()
    for line in lines:
        # Stampa da colonna 0, nessun prefisso
        for ch in line:
            sys.stdout.write(f"{CYAN}{ch}{RESET}")
            sys.stdout.flush()
            time.sleep(0.006)
        print()
    print()


def print_command(cmd):
    print(f"{YELLOW}{BOLD}$ {cmd}{RESET}")


# ─── BANNER ───────────────────────────────────────────────────────────────────

BANNER = f"""
{GREEN}{BOLD}
       ██╗ █████╗ ██████╗ ██╗   ██╗██╗███████╗
       ██║██╔══██╗██╔══██╗██║   ██║██║██╔════╝
       ██║███████║██████╔╝██║   ██║██║███████╗
  ██   ██║██╔══██║██╔══██╗╚██╗ ██╔╝██║╚════██║
  ╚█████╔╝██║  ██║██║  ██║ ╚████╔╝ ██║███████║
   ╚════╝ ╚═╝  ╚═╝╚═╝  ╚═╝  ╚═══╝  ╚═╝╚══════╝
{RESET}
{WHITE}{BOLD}       Tutorial Interattivo — Clapper System{RESET}
"""


# ═══════════════════════════════════════════════════════════════════════════════
#  STEPS
# ═══════════════════════════════════════════════════════════════════════════════

def step_intro():
    clear()
    print(BANNER)
    time.sleep(1)
    narrate(
        "  Ciao! Sono Jarvis.\n"
        "  Ti spiego come ricreare il programma Clapper\n"
        "  sul tuo Mac. Batti le mani due volte\n"
        "  e il Mac apre musica e app automaticamente.",

        "Ciao! Sono Jarvis. Ti spiego come ricreare il programma Clapper "
        "sul tuo Mac. Batti le mani due volte e il Mac apre musica e app "
        "automaticamente. Premi invio quando sei pronto."
    )
    wait_enter()


def step_prerequisiti():
    clear()
    print_header("STEP 1 — Prerequisiti")
    narrate(
        "  Verifica di avere Python 3.\n"
        "  Scrivi questo comando nel Terminale.",
        "Verifica di avere Python 3. Scrivi questo comando nel Terminale."
    )
    print()
    print_command("python3 --version")
    wait_enter()


def step_dipendenze():
    clear()
    print_header("STEP 2 — Installare le dipendenze")
    narrate(
        "  Installa sounddevice per il microfono\n"
        "  e numpy per i calcoli audio.",
        "Installa sounddevice per il microfono e nampai per i calcoli audio."
    )
    print()
    print_command("pip3 install sounddevice numpy")
    wait_enter()


def step_permessi():
    clear()
    print_header("STEP 3 — Permessi microfono")
    narrate(
        "  Quando il Mac chiede l'accesso al microfono,\n"
        "  clicca Consenti. Se non appare il popup, vai in\n"
        "  Impostazioni > Privacy > Microfono > Terminale.",
        "Quando il Mac chiede l'accesso al microfono, clicca Consenti. "
        "Se non appare il popup, vai in Impostazioni, Privacy, Microfono, "
        "e attiva il Terminale."
    )
    wait_enter()


def step_imports():
    clear()
    print_header("STEP 4 — Importazioni")
    narrate(
        "  Queste sono le librerie che il programma usa.",
        "Queste sono le librerie che il programma usa. "
        "Copia questo blocco all'inizio del file."
    )
    print_code([
        '#!/usr/bin/env python3',
        '"""',
        'clapper.py — Double clap → Back in Black + AI apps tiled',
        '"""',
        '',
        'import os',
        'import sounddevice as sd',
        'import numpy as np',
        'import subprocess',
        'import threading',
        'import time',
    ])
    wait_enter()


def step_config():
    clear()
    print_header("STEP 5 — Configurazione")
    narrate(
        "  Questi parametri controllano sensibilita,\n"
        "  tempi, la canzone e le app da aprire.\n"
        "  Personalizzali come vuoi.",
        "Questi parametri controllano la sensibilita, i tempi, "
        "la canzone e le app da aprire. Personalizzali come vuoi."
    )
    print_code([
        '# ─── CONFIG ────────────────────────────────────────────────────────────────────',
        'CLAP_THRESHOLD  = 0.10   # abbassa se non rileva, alza se troppi falsi positivi',
        'DOUBLE_CLAP_MAX = 1.2    # secondi max tra i due clap',
        'CLAP_DEBOUNCE   = 0.08   # secondi minimi tra un clap e l\'altro',
        'COOLDOWN        = 4.0    # pausa prima del prossimo trigger',
        '',
        'SPOTIFY_TRACK_URI = "spotify:track:08mG3Y1vljYA6bvDt4Wqkj"',
        '',
        '# Layout:  top 2  →  Claude | ChatGPT',
        '#          bot 2  →  Codex  | Antigravity',
        'APPS_TOP = ["Claude", "ChatGPT"]',
        'APPS_BOT = ["Codex", "Antigravity"]',
        '# ───────────────────────────────────────────────────────────────────────────────',
    ])
    wait_enter()


def step_screen_size():
    clear()
    print_header("STEP 6 — Funzione get_screen_size")
    narrate(
        "  Chiede al Finder le dimensioni dello schermo\n"
        "  usando AppleScript.",
        "Questa funzione chiede al Finder le dimensioni dello schermo "
        "usando AppleScript."
    )
    print_code([
        '',
        'def get_screen_size():',
        '    script = \'tell application "Finder" to get bounds of window of desktop\'',
        '    out = subprocess.run(["osascript", "-e", script],',
        '                         capture_output=True, text=True).stdout.strip()',
        '    # "0, 0, 1512, 982"',
        '    parts = [int(x.strip()) for x in out.split(",")]',
        '    return parts[2], parts[3]   # width, height',
    ])
    wait_enter()


def step_arrange():
    clear()
    print_header("STEP 7 — Funzione arrange_windows")
    narrate(
        "  Divide lo schermo in 4 quadranti\n"
        "  e posiziona ogni app con AppleScript.",
        "Divide lo schermo in quattro quadranti e posiziona "
        "ogni app con AppleScript."
    )
    print_code([
        '',
        'def arrange_windows():',
        '    sw, sh = get_screen_size()',
        '    menu    = 37',
        '    dock    = 72',
        '    avail_h = sh - menu - dock',
        '    row_h   = avail_h // 2',
        '    col2    = sw // 2',
        '',
        '    layout = [',
        '        (APPS_TOP[0], 0,    menu,          col2, row_h),',
        '        (APPS_TOP[1], col2, menu,          col2, row_h),',
        '        (APPS_BOT[0], 0,    menu + row_h,  col2, row_h),',
        '        (APPS_BOT[1], col2, menu + row_h,  col2, row_h),',
        '    ]',
        '',
        '    # Attiva tutte le app prima, poi posiziona ciascuna',
        '    for app, x, y, w, h in layout:',
        "        script = f'''",
        '        tell application "{app}" to activate',
        '        delay 0.5',
        '        tell application "System Events"',
        '            tell process "{app}"',
        '                try',
        '                    set position of window 1 to {{{x}, {y}}}',
        '                    set size of window 1 to {{{w}, {h}}}',
        '                end try',
        '            end tell',
        '        end tell',
        "        '''",
        '        subprocess.run(["osascript", "-e", script], capture_output=True)',
    ])
    wait_enter()


def step_say():
    clear()
    print_header("STEP 8 — Funzione say")
    narrate(
        "  Questa funzione usa il sintetizzatore vocale\n"
        "  del Mac per parlare.",
        "Questa piccola funzione usa il sintetizzatore vocale del Mac."
    )
    print_code([
        '',
        'def say(text):',
        '    subprocess.Popen(["say", "-v", "Luca", text])',
    ])
    wait_enter()


def step_trigger():
    clear()
    print_header("STEP 9 — Funzione trigger")
    narrate(
        "  Questa e la funzione principale.\n"
        "  Apre Spotify, le app AI e dispone le finestre.",
        "Questa e la funzione principale. Apre Spotify, "
        "le app di intelligenza artificiale, e dispone le finestre."
    )
    print_code([
        '',
        'def trigger():',
        '    print("\\n\\U0001f44f  Doppio clap! Avvio...\\n")',
        '',
        '    # TTS apertura',
        '    say("Inizializzazione sistemi in corso")',
        '',
        '    # 1. Spotify + Back in Black',
        '    print("\\U0001f3b8  Spotify...")',
        '    subprocess.run(["open", "-a", "Spotify"])',
        '    time.sleep(2)',
        '    subprocess.run(["osascript", "-e",',
        '        f\'tell application "Spotify" to play track "{SPOTIFY_TRACK_URI}"\'])',
        '    time.sleep(0.5)',
        '',
        '    # 2. App AI',
        '    for app in APPS_TOP + [a for a in APPS_BOT if a != "Spotify"]:',
        '        result = subprocess.run(["open", "-a", app],',
        '                                capture_output=True, text=True)',
        '        if result.returncode != 0:',
        "            print(f\"   \\u26a0\\ufe0f  '{app}' non trovata\")",
        '        time.sleep(0.3)',
        '',
        '    # 3. Aspetta che le finestre siano cariche poi tilea',
        '    print("\\U0001fa9f  Disposizione finestre...")',
        '    time.sleep(3)',
        '    arrange_windows()',
        '',
        '    # TTS chiusura',
        '    say("Operativo")',
        '    print("\\u2705  Let there be rock.\\n")',
    ])
    wait_enter()


def step_main():
    clear()
    print_header("STEP 10 — Funzione main")
    narrate(
        "  Il loop che ascolta il microfono\n"
        "  e rileva il doppio clap.",
        "Questo e il loop che ascolta il microfono e rileva il doppio clap."
    )
    print_code([
        '',
        'def main():',
        '    print("\\U0001f44f  In ascolto — doppio clap per triggerare")',
        '    print("    Ctrl+C per uscire\\n")',
        '',
        '    last_clap      = 0.0',
        '    clap_count     = 0',
        '    fired          = threading.Event()',
        '    trigger_thread = None',
        '',
        '    def callback(indata, frames, time_info, status):',
        '        nonlocal last_clap, clap_count, trigger_thread',
        '',
        '        if fired.is_set():',
        '            return',
        '',
        '        rms = float(np.sqrt(np.mean(indata ** 2)))',
        '        now = time.time()',
        '',
        '        if rms > CLAP_THRESHOLD:',
        '            if now - last_clap < CLAP_DEBOUNCE:',
        '                return',
        '',
        '            gap       = now - last_clap',
        '            last_clap = now',
        '',
        '            clap_count = (clap_count + 1) if gap <= DOUBLE_CLAP_MAX else 1',
        '            print(f"  clap #{clap_count}  (rms={rms:.3f})")',
        '',
        '            if clap_count >= 2:',
        '                fired.set()',
        '                trigger_thread = threading.Thread(target=trigger)',
        '                trigger_thread.start()',
        '',
        '    with sd.InputStream(callback=callback, channels=1,',
        '                        samplerate=44100, blocksize=512):',
        '        try:',
        '            fired.wait()',
        '        except KeyboardInterrupt:',
        '            print("\\n\\U0001f44b  Clapper fermato.")',
        '',
        '    # stream chiuso, aspetta che trigger finisca prima di uscire',
        '    if trigger_thread:',
        '        trigger_thread.join()',
        '',
        '',
        'if __name__ == "__main__":',
        '    main()',
    ])
    wait_enter()


def step_esecuzione():
    clear()
    print_header("STEP 11 — Esegui il programma")
    narrate(
        "  Salva il file ed eseguilo cosi.",
        "Salva il file e eseguilo con questo comando. "
        "Batti le mani due volte e guarda la magia!"
    )
    print()
    print_command("cd ~/Desktop/clapper")
    print_command("python3 clapper.py")
    wait_enter()


def step_outro():
    clear()
    cols = shutil.get_terminal_size().columns
    w = min(cols - 4, 70)
    print()
    print(f"  {GREEN}{BOLD}{'━' * w}{RESET}")
    print(f"  {GREEN}{BOLD}  ✓  Tutorial completato!{RESET}")
    print(f"  {GREEN}{BOLD}{'━' * w}{RESET}")
    print()

    say_only("Complimenti! Hai completato il tutorial. "
             "Ora hai tutto per far funzionare il Clapper sul tuo Mac. "
             "Buon divertimento!")

    print(f"  {WHITE}Premi INVIO per uscire.{RESET}")
    input()


# ═══════════════════════════════════════════════════════════════════════════════

def main():
    steps = [
        step_intro,
        step_prerequisiti,
        step_dipendenze,
        step_permessi,
        step_imports,
        step_config,
        step_screen_size,
        step_arrange,
        step_say,
        step_trigger,
        step_main,
        step_esecuzione,
        step_outro,
    ]

    try:
        for step_fn in steps:
            step_fn()
    except KeyboardInterrupt:
        print(f"\n\n  {WHITE}Tutorial interrotto. A presto!{RESET}\n")
        sys.exit(0)


if __name__ == "__main__":
    main()
