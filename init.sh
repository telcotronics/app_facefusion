#!/bin/bash
RUTA=$(dirname "$(realpath "$0")")
VENV="$RUTA/venv"

source "$VENV/bin/activate"
python "$RUTA/facefusion.py" run
