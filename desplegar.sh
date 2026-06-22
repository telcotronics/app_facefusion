#!/bin/bash
SERVIDOR="root@192.168.10.154"
RUTA_REMOTA="/root/apps/app_facefusion"
RUTA_LOCAL=$(dirname "$(realpath "$0")")

echo "=== Desplegando FaceFusion en $SERVIDOR ==="

echo "[1/3] Sincronizando archivos..."
rsync -avz --progress \
  --exclude='.git/' \
  --exclude='__pycache__/' \
  --exclude='*.pyc' \
  --exclude='.agente/' \
  --exclude='facefusion/.assets/' \
  "$RUTA_LOCAL/" "$SERVIDOR:$RUTA_REMOTA/"

echo "[2/3] Subiendo init.sh del servidor..."
scp "$RUTA_LOCAL/init.sh" "$SERVIDOR:/root/init.sh"

echo "[3/3] Reiniciando FaceFusion en tmux..."
ssh "$SERVIDOR" bash << 'EOF'
SESSION="ia-services"
PANE="$SESSION:0.3"

if tmux has-session -t "$SESSION" 2>/dev/null; then
    tmux send-keys -t "$PANE" C-c
    sleep 1
    tmux send-keys -t "$PANE" "cd /root/apps/app_facefusion && python facefusion.py run" Enter
    echo "FaceFusion reiniciado en pane $PANE"
else
    echo "Sesion tmux '$SESSION' no activa — arranca con: bash /root/init.sh"
fi
EOF

echo ""
echo "=== Deploy completado ==="
echo "FaceFusion: http://192.168.10.154:7860"
