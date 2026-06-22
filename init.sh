#!/bin/bash
RUTA=$(dirname "$(realpath "$0")")
VENV="$RUTA/venv"

echo ""
echo "=== FaceFusion ==="
echo "  1) Correr la app"
echo "  2) Instalar / reinstalar"
echo "  3) Salir"
echo ""
read -p "Opcion (1/2/3): " opcion

case "$opcion" in
    1)
        echo ""
        if [ ! -d "$VENV" ]; then
            echo "Error: entorno virtual no encontrado. Ejecuta la opcion 2 primero."
            exit 1
        fi
        echo "Activando entorno virtual..."
        source "$VENV/bin/activate"
        echo "Iniciando FaceFusion..."
        python facefusion.py run
        ;;
    2)
        echo ""
        echo "[1/3] Creando entorno virtual..."
        python3 -m venv "$VENV"
        source "$VENV/bin/activate"

        echo "[2/3] Instalando dependencias..."
        pip install --upgrade pip -q
        pip install -r "$RUTA/requirements.txt"

        echo "[3/3] Instalando ONNX Runtime GPU (CUDA)..."
        pip install onnxruntime-gpu

        echo ""
        echo "Instalacion completada. Ejecuta la opcion 1 para correr la app."
        ;;
    3|*)
        echo "Saliendo."
        exit 0
        ;;
esac
