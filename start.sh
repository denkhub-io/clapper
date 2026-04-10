#!/bin/bash
# Avvia clapper — se manca il venv, lancia l'installer automaticamente
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

if [ ! -d "$SCRIPT_DIR/.venv" ]; then
    bash "$SCRIPT_DIR/install.sh"
fi

"$SCRIPT_DIR/.venv/bin/python" "$SCRIPT_DIR/clapper.py" "$@"
