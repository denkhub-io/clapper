# Clapper

Batti le mani due volte. Il computer fa il resto.

**Doppio clap** → le tue app si aprono e si dispongono automaticamente sullo schermo. Scegli tu quali e quante.

## Quickstart

```bash
gh repo clone denkhub-io/clapper
cd clapper
bash start.sh
```

Al primo avvio parte un wizard vocale che ti guida nella configurazione: trascina le app nel terminale, incolla un link Spotify se vuoi, e sei pronto. Dopo il setup il programma parte in automatico.

## Uso

Dalla seconda volta in poi basta:

```bash
bash start.sh
```

Per riconfigurare le app:

```bash
bash start.sh setup
```

## Come funziona

1. Al primo avvio, un wizard parlante ti guida nella scelta delle app e della canzone
2. La configurazione viene salvata in `~/.clapper.json`
3. Il programma ascolta il microfono — doppio clap e le app si aprono in griglia automatica
4. Supporta da 2 a 6+ app, disposte dinamicamente sullo schermo

## Requisiti

- macOS
- Python 3.10+
- Microfono funzionante

## Licenza

MIT

---

Un progetto [DenkHub](https://denkhub.io) Playground.
