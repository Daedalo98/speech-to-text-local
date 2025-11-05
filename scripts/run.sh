#!/usr/bin/env bash
set -euo pipefail

# Setup (venv + deps + modello)
./scripts/setup.sh

# Attiva venv e avvia app
# shellcheck disable=SC1091
source .venv/bin/activate

# Permetti override dispositivo o directory modello via env
exec python src/app.py "$@"
