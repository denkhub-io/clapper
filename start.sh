#!/bin/bash
# Avvia clapper usando il python del venv
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
"$SCRIPT_DIR/.venv/bin/python" "$SCRIPT_DIR/clapper.py" "$@"
