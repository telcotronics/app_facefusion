#!/bin/bash
SERVIDOR="pablinux@192.168.10.154"
RUTA_REMOTA="/home/pablinux/apps/app_facefusion"
RUTA_LOCAL=$(dirname "$(realpath "$0")")

echo "=== Desplegando FaceFusion en $SERVIDOR ==="

echo "[1/2] Sincronizando archivos..."
rsync -avz --progress \
  --exclude='.git/' \
  --exclude='__pycache__/' \
  --exclude='*.pyc' \
  --exclude='.agente/' \
  --exclude='facefusion/.assets/' \
  --exclude='venv/' \
  "$RUTA_LOCAL/" "$SERVIDOR:$RUTA_REMOTA/"

echo "[2/2] Reiniciando FaceFusion en tmux..."
ssh "$SERVIDOR" bash << 'EOF'
SESSION="ia-services"
PANE="$SESSION:0.3"

if tmux has-session -t "$SESSION" 2>/dev/null; then
    tmux send-keys -t "$PANE" C-c
    sleep 1
    tmux send-keys -t "$PANE" "cd /home/pablinux/apps/app_facefusion && bash init.sh" Enter
    sleep 2
    tmux send-keys -t "$PANE" "1" Enter
    echo "FaceFusion reiniciado en pane $PANE"
else
    echo "Sesion tmux '$SESSION' no activa — arranca con: bash /home/pablinux/init.sh"
fi
EOF

echo ""
echo "=== Deploy completado ==="
echo "FaceFusion: http://192.168.10.154:7860"
