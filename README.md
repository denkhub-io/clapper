# Clapper

Batti le mani due volte. Il computer fa il resto.

**Doppio clap** → le tue app si aprono e si dispongono automaticamente sullo schermo. Scegli tu quali e quante.

## Quickstart

```bash
git clone https://github.com/denkhub-io/clapper.git
cd clapper
bash install.sh
```

Fatto. L'installer configura tutto e ti guida nella scelta delle app.

## Uso

```bash
# Avvia l'ascolto
bash start.sh

# Riconfigura le app
bash start.sh setup
```

## Come funziona

1. L'installer installa le dipendenze e avvia il setup
2. Scegli le app da aprire (2, 3, 4, 5, quante ne vuoi)
3. Opzionale: traccia Spotify, voce TTS, sensibilità microfono
4. Doppio clap → le app si aprono e si dispongono in griglia automatica

La configurazione viene salvata in `~/.clapper.json` — riesegui `setup` quando vuoi cambiarla.

## Requisiti

- Python 3.10+
- macOS (usa AppleScript per il window management)
- Microfono funzionante

## Licenza

MIT

---

Un progetto [DenkHub](https://denkhub.io) Playground.
