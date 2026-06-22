# agents.md — Punto de entrada del proyecto

> **Reglas:**
> - Este archivo es el eslabón más importante. Leerlo siempre antes de cualquier tarea.
> - Cada cambio significativo debe reflejarse en este archivo y en los demás archivos del índice.
> - Debe ser técnico, claro y detailed para que cualquier humano, agente o IA lo entienda sin explicaciones previas.
> - **Cuando se diga "actualizar proyecto":** hacer commit de los cambios pendientes, actualizar `agents.md` y `.agente/proyecto_estructura.md` con el árbol de archivos actual.

---

## Antecedentes

FaceFusion es el módulo de **visión facial** del ecosistema Telcotronics. Se despliega como servicio en el servidor `APPS-SERVICE-IA` (`192.168.10.154`), el servidor dedicado a servicios de IA del ecosistema.

En desarrollo local corre como app Gradio en `http://127.0.0.1:7860`. En producción se integra al servidor IA del ecosistema bajo sesión tmux `ia-services`.

---

## Objetivo general

Proveer capacidades de manipulación y análisis facial como servicio de IA dentro del ecosistema Telcotronics.

1. Intercambio de rostros en imágenes y videos (face swap)
2. Mejora, edición y análisis facial (enhancer, editor, debugger, detector)
3. Procesamiento adicional: lip sync, coloreado, modificación de edad, restauración de expresión, eliminación de fondo

---

## Stack técnico

| Componente | Tecnología |
|---|---|
| Lenguaje | Python 3 |
| UI / local | Gradio 5.44.1 |
| Inferencia | ONNX Runtime 1.24.4 |
| Video | OpenCV 4.13 + FFmpeg |
| Servidor producción | `APPS-SERVICE-IA` — `192.168.10.154` |
| Sesión producción | tmux `ia-services` |

---

## Módulos del sistema

### 1. Procesadores (`facefusion/processors/modules/`)
**Estado: ✅ Activo**

| Procesador | Función |
|---|---|
| `face_swapper` | Intercambio de rostros |
| `face_enhancer` | Mejora de calidad facial |
| `face_editor` | Edición de expresiones y geometría facial |
| `face_debugger` | Visualización de detección facial |
| `age_modifier` | Modificación de edad aparente |
| `expression_restorer` | Restauración de expresión natural |
| `background_remover` | Eliminación de fondo |
| `deep_swapper` | Swap profundo |
| `frame_colorizer` | Coloreado de fotogramas |
| `frame_enhancer` | Mejora de fotogramas |
| `lip_syncer` | Sincronización de labios |

### 2. UI Gradio (`facefusion/uis/`)
**Estado: ✅ Activo**

Interfaz web local en español (translator.py modificado). Layouts: `default`, `benchmark`, `jobs`, `webcam`.

### 3. Workflows (`facefusion/workflows/`)
**Estado: ✅ Activo**

`image_to_image`, `image_to_video`

---

## Infraestructura (referencia rápida)

> ⚠️ La infraestructura es compartida por todo el ecosistema Telcotronics
> (sigma-robot, sigma-web, sigma-c, sigmac_app, CRM, ERP y otros).
> La fuente de verdad es **`mcp.telcotronics.net`** — actualmente 🔧 **en mantenimiento**.
> Mientras esté en mantenimiento, la fuente alternativa es `/home/pablinux/Projects/infraestructura.md`.
> No editar `.agente/infraestructura.md` directamente — ver protocolo de sincronización.

| Parámetro | Valor |
|---|---|
| Repo GitHub | `https://github.com/Pablinux/app_facefusion` (público) |
| Carpeta en servidor | `/home/pablinux/apps/app_facefusion` |
| Servidor producción | `APPS-SERVICE-IA` — `192.168.10.154` |
| Puerto local (dev) | 7860 (Gradio) |
| Puerto producción | [COMPLETAR] |
| Sesión tmux | `ia-services` |
| Dominio público | [COMPLETAR] |
| BD principal | [COMPLETAR] |
| MCP ecosistema | `mcp.telcotronics.net` 🔧 en mantenimiento |

> **Correo del ecosistema:** usar `no-reply@sigmac.app` con contraseña `Sigma.2030@`
> vía `smtp.sigmac.app:587` (STARTTLS). Desde LAN interna usar `192.168.10.111:587`.
> Credenciales disponibles en `.agente/infraestructura.md` — sección servidor-email.

> Para el detalle completo y datos del ecosistema ver `.agente/infraestructura.md`.

## Documentos del ecosistema (referencia)

> Estos documentos viven en `/home/pablinux/Projects/` y son la fuente de verdad del ecosistema.
> **No duplicar su contenido aquí** — referenciarlos.

| Documento | Descripción |
|---|---|
| `~/Projects/design-system.md` | Sistema de diseño unificado — colores, tipografía, componentes para Flutter / Vue / Java / PHP |
| `~/Projects/roadmap.md` | Hoja de ruta estratégica — decisiones técnicas tomadas y pendientes de ejecutar |
| `~/Projects/infraestructura.md` | Arquitectura completa de servidores, red, CTs y servicios del ecosistema |
| `~/Projects/prompt_actualizacion.md` | Protocolo de actualización — registrar objetivos, documentar sesiones, sincronizar |

---

## Variables de entorno (`.env`)

| Variable | Descripción |
|---|---|
| [COMPLETAR] | [COMPLETAR] |

---

## Migraciones

Runner: `[COMPLETAR — ej: node server/db/migrate.js]`

| Archivo | Tabla principal | Estado |
|---|---|---|
| — | — | — |

---

## Para arrancar en local

```bash
python facefusion.py run
# Gradio disponible en http://127.0.0.1:7860
```

## Para arrancar en producción

```bash
# En APPS-SERVICE-IA (192.168.10.154), sesión tmux ia-services:
python facefusion.py run
```

---

## Índice de archivos del proyecto

```
proyecto/
├── README.md
├── agents.md                            # ← LEER PRIMERO
└── .agente/
    ├── infraestructura.md               # Ecosistema — espejo del global
    ├── proyecto_estructura.md           # Árbol de archivos y rutas
    ├── proyecto_memoria.md              # Decisiones técnicas e historial
    ├── proyecto_errores.md              # Registro de errores
    ├── objetivos.md                     # Qué debe cumplirse (sin fecha)
    └── ideas.md                         # Posibilidades sin compromiso
```

---

## Estado global del proyecto

| Módulo | Estado |
|---|---|
| [COMPLETAR] | ⏳ Pendiente |
