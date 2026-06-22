#!/bin/bash
RUTA=$(dirname "$(realpath "$0")")
VENV="$RUTA/venv"

correr() {
    if [ ! -d "$VENV" ]; then
        echo "Entorno virtual no encontrado. Ejecuta: bash init.sh instalar"
        exit 1
    fi
    source "$VENV/bin/activate"
    python "$RUTA/facefusion.py" run
}

instalar() {
    echo "[1/3] Creando entorno virtual..."
    python3 -m venv "$VENV"
    source "$VENV/bin/activate"

    echo "[2/3] Instalando dependencias..."
    pip install --upgrade pip -q
    pip install -r "$RUTA/requirements.txt"

    echo "[3/3] Instalando ONNX Runtime GPU..."
    pip install onnxruntime-gpu

    echo ""
    echo "Instalacion completada."
    read -p "Correr la app ahora? (s/n): " respuesta
    [ "$respuesta" = "s" ] && correr
}

case "$1" in
    correr|1)    correr ;;
    instalar|2)  instalar ;;
    *)
        echo ""
        echo "=== FaceFusion ==="
        echo "  1) Correr la app"
        echo "  2) Instalar / reinstalar"
        echo ""
        read -p "Opcion: " op
        case "$op" in
            1) correr ;;
            2) instalar ;;
            *) exit 0 ;;
        esac
        ;;
esac
