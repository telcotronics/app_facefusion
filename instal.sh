#!/bin/bash
RUTA=$(dirname "$(realpath "$0")")
VENV="$RUTA/venv"

echo "=== Instalando FaceFusion ==="
python3 -m venv "$VENV"
source "$VENV/bin/activate"
pip install --upgrade pip -q
pip install -r "$RUTA/requirements.txt"
pip install onnxruntime-gpu
echo "Instalacion completada."
