# FaceFusion v3.6.1

**Plataforma de manipulación facial por inteligencia artificial.**

FaceFusion es una herramienta de procesamiento de imágenes y videos que utiliza modelos de IA (ONNX) para aplicar transformaciones faciales avanzadas: intercambio de rostros, mejora de calidad, edición de expresiones, sincronización de labios, modificación de edad y mucho más.

Dentro del ecosistema Telcotronics opera como el módulo de **visión facial** del servidor de IA (`APPS-SERVICE-IA` — `192.168.10.154`).

---

## ¿Qué hace?

Recibe una imagen o video de entrada (**destino**) y opcionalmente una imagen de referencia (**origen**), aplica uno o varios procesadores de IA en cadena, y produce un archivo de salida transformado.

### Procesadores disponibles

| Procesador | Qué hace |
|---|---|
| **Face Swapper** | Intercambia el rostro de la imagen origen por el del destino. Soporta múltiples modelos: `inswapper`, `ghost`, `simswap`, `uniface`, `blendswap`, `hififace`, `hyperswap`. |
| **Face Enhancer** | Mejora la calidad y nitidez del rostro procesado. Modelos: `codeformer`, `gfpgan` (1.2–1.4), `gpen` (256–2048px), `restoreformer++`. |
| **Face Editor** | Edita geometría y expresión facial: dirección de cejas, mirada, apertura de ojos y labios, sonrisa, posición de boca, inclinación y rotación de cabeza (pitch, yaw, roll). |
| **Face Debugger** | Visualiza los puntos de referencia faciales detectados (útil para diagnóstico y ajuste de parámetros). |
| **Age Modifier** | Modifica la edad aparente del rostro (rejuvenecer o envejecer). |
| **Expression Restorer** | Restaura la expresión natural del rostro de origen sobre el resultado del swap. |
| **Background Remover** | Elimina o separa el fondo de la imagen. |
| **Deep Swapper** | Swap profundo de alta fidelidad. |
| **Frame Colorizer** | Colorea fotogramas en escala de grises usando IA. |
| **Frame Enhancer** | Mejora la calidad general del fotograma completo (no solo el rostro). |
| **Lip Syncer** | Sincroniza el movimiento de labios con una pista de audio (lip sync). |

Se pueden activar **varios procesadores en cadena** en un mismo procesamiento.

---

## ¿Para qué sirve?

- Producción de contenido audiovisual: intercambio de actores, anonimización de rostros, doblaje visual.
- Restauración de videos y fotos antiguas (mejora de calidad + coloreado).
- Sincronización de labios para doblaje automático.
- Prototipado de personajes virtuales.
- Análisis y diagnóstico facial (modo debugger).
- Como servicio de IA dentro del ecosistema Telcotronics para cualquier app que necesite procesamiento facial.

---

## Cómo funciona

```
[Imagen origen]  +  [Imagen/Video destino]
        ↓
  Detección facial (ONNX)
        ↓
  Selección de rostros (filtros: orden, género, edad, etnia, distancia)
        ↓
  Pipeline de procesadores (configurables)
  ┌─────────────┐   ┌──────────────┐   ┌─────────────────┐
  │ face_swapper│ → │face_enhancer │ → │ otros procesadores│
  └─────────────┘   └──────────────┘   └─────────────────┘
        ↓
  [Imagen/Video de salida]
```

1. **Detección:** localiza todos los rostros en el fotograma usando el modelo detector configurado (`retinaface`, `scrfd`, `yolo_face`, `yunet`).
2. **Puntos de referencia:** mapea 5 puntos clave del rostro (landmarker) para alinear con precisión.
3. **Selección:** filtra qué rostros procesar según orden espacial, género, edad, etnia o distancia a un rostro de referencia.
4. **Procesamiento:** cada procesador activo recibe el fotograma, aplica su modelo ONNX, y devuelve el fotograma transformado.
5. **Máscara facial:** permite aplicar máscaras de oclusión y segmentación por región (piel, cejas, ojos, nariz, boca, labios) para un resultado más natural.
6. **Ensamblado:** reensambla los fotogramas procesados y los une con el audio original usando FFmpeg.

---

## Estructura del proyecto

```
facefusion/
├── facefusion.py                  # Punto de entrada — arranca la app
├── facefusion.ini                 # Configuración por defecto
├── requirements.txt               # Dependencias Python
│
└── facefusion/                    # Módulo principal
    ├── core.py                    # Lógica central y comandos CLI
    ├── state_manager.py           # Estado global de la sesión
    ├── process_manager.py         # Control del proceso de ejecución
    │
    ├── face_detector.py           # Detección de rostros
    ├── face_landmarker.py         # Puntos de referencia faciales
    ├── face_recognizer.py         # Reconocimiento / embedding facial
    ├── face_analyser.py           # Análisis facial (edad, género, etnia)
    ├── face_masker.py             # Máscaras de oclusión y región
    ├── face_selector.py           # Selección y filtrado de rostros
    ├── face_store.py              # Almacenamiento de rostros en sesión
    │
    ├── inference_manager.py       # Gestión de modelos ONNX en memoria
    ├── vision.py                  # Operaciones de imagen/video (OpenCV)
    ├── ffmpeg.py                  # Extracción y ensamblado de video
    ├── audio.py                   # Manejo de pistas de audio
    ├── download.py                # Descarga automática de modelos
    ├── translator.py              # Internacionalización (español por defecto)
    │
    ├── processors/                # Procesadores de IA
    │   └── modules/
    │       ├── face_swapper/      # Intercambio de rostros
    │       ├── face_enhancer/     # Mejora facial
    │       ├── face_editor/       # Edición de expresión y geometría
    │       ├── face_debugger/     # Visualización de detección
    │       ├── age_modifier/      # Modificación de edad
    │       ├── expression_restorer/  # Restauración de expresión
    │       ├── background_remover/   # Eliminación de fondo
    │       ├── deep_swapper/      # Swap profundo
    │       ├── frame_colorizer/   # Coloreado de fotogramas
    │       ├── frame_enhancer/    # Mejora de fotograma completo
    │       └── lip_syncer/        # Sincronización de labios
    │
    ├── uis/                       # Interfaz de usuario (Gradio)
    │   ├── layouts/               # Vistas: default, benchmark, jobs, webcam
    │   └── components/            # Componentes por procesador y función
    │
    ├── workflows/                 # Flujos de procesamiento
    │   ├── image_to_image.py      # Imagen → Imagen
    │   └── image_to_video.py      # Imagen + Video → Video
    │
    └── jobs/                      # Sistema de colas de trabajo
        ├── job_manager.py
        └── job_runner.py
```

---

## Formatos soportados

| Tipo | Formatos |
|---|---|
| **Imágenes** | BMP, JPEG, PNG, TIFF, WebP |
| **Videos** | AVI, M4V, MKV, MP4, MPEG, MOV, MXF, WebM, WMV |
| **Audio** | FLAC, M4A, MP3, OGG, OPUS, WAV |

---

## Modos de ejecución

| Modo | Descripción |
|---|---|
| `run` | Lanza la interfaz web Gradio en `http://127.0.0.1:7860` |
| `headless-run` | Procesa sin interfaz gráfica (para scripts y automatización) |
| `batch-run` | Procesamiento de múltiples archivos en lote |
| `benchmark` | Mide el rendimiento de los modelos |
| `force-download` | Descarga todos los modelos sin procesar nada |
| `job-*` | Sistema de trabajos: crear, listar, ejecutar, reintentar colas de trabajo |

---

## Ejecución

### Local (desarrollo)

```bash
python facefusion.py run
# Interfaz disponible en http://127.0.0.1:7860
```

### Producción

Servidor: `APPS-SERVICE-IA` (`192.168.10.154`) — sesión tmux `ia-services`

```bash
python facefusion.py run
```

### Sin interfaz (headless)

```bash
python facefusion.py headless-run \
  -s origen.jpg \
  -t destino.mp4 \
  -o salida.mp4 \
  --processors face_swapper face_enhancer
```

---

## Configuración principal (`facefusion.ini`)

El archivo `facefusion.ini` permite preconfigurar todos los parámetros para no tener que pasarlos por línea de comandos cada vez: procesadores activos, modelos, calidad de salida, proveedores de ejecución (CPU / CUDA), hilos, límite de memoria, etc.

---

## Dependencias

```
gradio==5.44.1          # Interfaz web
numpy==2.2.1            # Álgebra lineal
onnx==1.21.0            # Definición de modelos
onnxruntime==1.24.0     # Ejecución de modelos ONNX
opencv-python==4.13     # Procesamiento de imagen/video
scipy==1.17.1           # Cálculos científicos
tqdm==4.67.3            # Barras de progreso
```

---

## Licencia

OpenRAIL-AS — uso responsable de IA. No permite uso para generar contenido que dañe, engañe o vulnere derechos de personas reales sin su consentimiento.
