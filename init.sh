#!/bin/bash
RUTA=$(dirname "$(realpath "$0")")
VENV="$RUTA/venv"

echo ""
echo "=== FaceFusion ==="
echo "  1) Correr la app"
echo "  2) Instalar"
echo ""
read -p "Opcion: " op

case "$op" in
    1)
        source "$VENV/bin/activate"
        python "$RUTA/facefusion.py" run
        ;;
    2)
        python3 -m venv "$VENV"
        source "$VENV/bin/activate"
        pip install --upgrade pip -q
        pip install -r "$RUTA/requirements.txt"
        pip install onnxruntime-gpu
        echo "Instalacion completada."
        ;;
    *)
        exit 0
        ;;
esac
