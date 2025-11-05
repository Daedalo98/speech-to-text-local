#!/usr/bin/env bash
set -euo pipefail

PY="${PYTHON_BIN:-python3}"
VENV=".venv"

if [ ! -d "$VENV" ]; then
  echo "[setup] Creo virtualenv in $VENV"
  $PY -m venv "$VENV"
fi

# shellcheck disable=SC1091
source "$VENV/bin/activate"

echo "[setup] Aggiorno pip"
python -m pip install --upgrade pip

echo "[setup] Installo requirements"
pip install -r requirements.txt

echo "[setup] Scarico modello (se necessario)"
./scripts/download_model.sh

echo "[setup] Fatto."
