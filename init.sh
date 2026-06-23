#!/bin/bash
RUTA=$(dirname "$(realpath "$0")")
VENV="$RUTA/venv"

source "$VENV/bin/activate"
GRADIO_SERVER_NAME=0.0.0.0 python "$RUTA/facefusion.py" run
