# Clapper

Batti le mani due volte. Il computer fa il resto.

**Doppio clap** → le tue app si aprono e si dispongono automaticamente sullo schermo. Scegli tu quali e quante.

Pagina progetto: [denkhub.io/jarvis](https://denkhub.io/jarvis)

## Quickstart

### macOS

```bash
gh repo clone denkhub-io/clapper
cd clapper
bash start.sh
```

### Windows

```cmd
gh repo clone denkhub-io/clapper
cd clapper
start.bat
```

Al primo avvio parte un wizard vocale che ti guida nella configurazione: trascina le app nel terminale, incolla un link Spotify se vuoi, e sei pronto. Dopo il setup il programma parte in automatico.

## Uso

Dalla seconda volta in poi:

- **macOS**: `bash start.sh`
- **Windows**: `start.bat`

Per riconfigurare:

- **macOS**: `bash start.sh setup`
- **Windows**: `start.bat setup`

## Come funziona

1. Al primo avvio, un wizard parlante ti guida nella scelta delle app e della canzone
2. La configurazione viene salvata in `~/.clapper.json`
3. Il programma ascolta il microfono — doppio clap e le app si aprono in griglia automatica
4. Supporta da 2 a 6+ app, disposte dinamicamente sullo schermo

## Requisiti

- Python 3.10+
- Microfono funzionante
- macOS o Windows

## Licenza

MIT

---

Un progetto [DenkHub](https://denkhub.io) Playground.
