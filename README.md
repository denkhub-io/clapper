# Clapper

Batti le mani due volte. Il computer fa il resto.

**Doppio clap** &rarr; Spotify parte con la tua canzone, le app AI si aprono e si dispongono automaticamente sullo schermo in 4 quadranti.

## Come funziona

1. Il microfono rileva due battiti di mani ravvicinati (analisi RMS)
2. Spotify si apre e parte la canzone configurata
3. Le app AI (Claude, ChatGPT, Codex, Antigravity) si aprono e si posizionano in griglia 2x2

## Requisiti

- Python 3.10+
- macOS (per AppleScript window management) o Windows
- Spotify installato
- Microfono funzionante

## Installazione

```bash
# Clona il repo
git clone https://github.com/denkhub-io/clapper.git
cd clapper

# Installa le dipendenze
pip install sounddevice numpy

# Avvia
python3 clapper.py
```

## Personalizzazione

Apri `clapper.py` e modifica:

```python
SPOTIFY_TRACK_URI = "spotify:track:..."  # la tua canzone
APPS_TOP = ["Claude", "ChatGPT"]         # app riga superiore
APPS_BOT = ["Codex", "Antigravity"]      # app riga inferiore
CLAP_THRESHOLD  = 0.10                   # sensibilità microfono
```

## Tutorial interattivo

Incluso un tutorial vocale che spiega passo-passo come ricreare il programma:

```bash
python3 tutorial.py
# oppure doppio-click su avvia_tutorial.command
```

## Licenza

MIT

---

Un progetto [DenkHub](https://denkhub.io) Playground.
