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

# Install dependencies
echo "  → Installo dipendenze..."
python3 -m pip install --quiet sounddevice numpy
echo "  ✓ Dipendenze installate"

# Permessi
chmod +x "$(dirname "$0")/clapper.py"

# Avvia setup
echo ""
python3 "$(dirname "$0")/clapper.py" setup
