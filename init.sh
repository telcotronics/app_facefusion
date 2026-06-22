#!/bin/bash
SESSION="ia-services"

if tmux has-session -t "$SESSION" 2>/dev/null; then
    echo "La sesion TMUX '$SESSION' ya existe."
    echo "  1) Destruir y recrear"
    echo "  2) Adjuntarse a la sesion existente"
    echo "  3) Salir"
    read -p "Opcion (1/2/3): " opcion

    case "$opcion" in
        1)
            echo "Destruyendo sesion existente..."
            tmux kill-session -t "$SESSION"
            ;;
        2)
            echo "Adjuntando..."
            tmux attach-session -t "$SESSION"
            exit 0
            ;;
        3|*)
            echo "Saliendo."
            exit 0
            ;;
    esac
fi

echo "Iniciando servicios de TMUX"
tmux new -d -s "$SESSION" -n main

echo "Iniciando servicios de ComfyUI"
tmux send -t "$SESSION:0.0" "bash /home/pablinux/apps/confyui/init.sh" Enter
tmux split -v -t "$SESSION:0.0"

echo "Iniciando servicios de API-SERVICE"
tmux send -t "$SESSION:0.1" "cd /home/pablinux/apps/API_Service_IA/" Enter
tmux send -t "$SESSION:0.1" "bash init.sh" Enter
sleep 5
tmux send-keys -t "$SESSION:0.1" "2" Enter
tmux split -h -t "$SESSION:0.1"

echo "Iniciando servicios de OLLAMA"
sleep 10
tmux send -t "$SESSION:0.2" "cd /home/pablinux/apps/vllm/" Enter
tmux send -t "$SESSION:0.2" "bash init.sh" Enter
tmux split -h -t "$SESSION:0.0"

echo "Iniciando servicios de FaceFusion"
tmux send -t "$SESSION:0.3" "cd /home/pablinux/apps/app_facefusion/" Enter
tmux send -t "$SESSION:0.3" "python facefusion.py run" Enter

tmux select-layout -t "$SESSION:0" tiled

echo ""
echo "=== Servicios IA activos ==="
echo "ComfyUI:    http://192.168.10.154:8188"
echo "API:        http://192.168.10.154:8000"
echo "vLLM:       http://192.168.10.154:8001"
echo "FaceFusion: http://192.168.10.154:7860"
echo ""
echo "Adjuntar:  tmux a -t $SESSION"
echo "Matar:     tmux kill-session -t $SESSION"
