#!/bin/bash
# Clapper — install & setup in un colpo solo

set -e

echo ""
echo "  ┌─────────────────────────────────┐"
echo "  │   CLAPPER INSTALLER             │"
echo "  └─────────────────────────────────┘"
echo ""

# Check Python 3
if ! command -v python3 &>/dev/null; then
    echo "  ✗ Python 3 non trovato. Installalo e riprova."
    exit 1
fi
echo "  ✓ Python 3 trovato"

# Crea virtual environment
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$SCRIPT_DIR/.venv"

if [ ! -d "$VENV_DIR" ]; then
    echo "  → Creo ambiente virtuale..."
    python3 -m venv "$VENV_DIR"
fi
echo "  ✓ Ambiente virtuale pronto"

# Install dependencies
echo "  → Installo dipendenze..."
"$VENV_DIR/bin/pip" install --quiet sounddevice numpy
echo "  ✓ Dipendenze installate"

# Permessi
chmod +x "$SCRIPT_DIR/clapper.py"

# Avvia setup
echo ""
"$VENV_DIR/bin/python" "$SCRIPT_DIR/clapper.py" setup
