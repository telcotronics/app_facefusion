# Infraestructura SIGMA — Documentación Técnica

---

> # 🚨 PELIGRO — LEER ANTES DE TOCAR CUALQUIER COSA
>
> **ESTE ARCHIVO NO SE EDITA MANUALMENTE. NUNCA. BAJO NINGUNA CIRCUNSTANCIA. SIN AUTORIZACION**
>
> - ❌ No reescribas este archivo.
> - ❌ No elimines secciones existentes.
> - ❌ No agregues datos que pablinux no haya confirmado explícitamente.
> - ❌ No derives datos del código fuente y los documentes aquí como si fueran infraestructura.
>
> **¿Por qué?** Este documento es la biblia compartida de todo el ecosistema Telcotronics.
> Un dato incorrecto aquí afecta a todos los proyectos y a todas las IAs que lo leen.
> La fuente de verdad es el **MCP de infraestructura** (`mcp.telcotronics.net`).

---

> **Propósito:** Describe la arquitectura completa del ecosistema. Ante cualquier tarea técnica, leer primero.
> **Fuentes de verdad:** Árbol Proxmox VE, tabla DHCP MikroTik (mayo 2026), historia documentada por pablinux.
>
> **Documentos relacionados:**
> - 🎨 **[Design System](design-system.md)** — Estándar visual unificado: colores, tipografía, componentes.
> - 🗺️ **[Roadmap](roadmap.md)** — Decisiones técnicas tomadas y pendientes de ejecutar.

---

## Requisito de documentación

> **Este documento no es un inventario de IPs. Es la guía de integración del ecosistema.**
> Cualquier proyecto, app o servicio debe poder conectarse a otro leyendo solo este archivo —
> sin preguntar, sin buscar en el código, sin horas de explicación.
>
> **Regla de oro:** si alguien necesita enviar un correo, usar WhatsApp, facturar, sincronizar ideas
> o consumir cualquier servicio del ecosistema, la respuesta completa debe estar aquí.
>
> **Todo proyecto o servicio documentado aquí debe incluir:**
> - URL del repositorio Git
> - Tecnología principal, responsable y estado actual
> - Servidor de producción — IP, puerto, dominio público
> - Cómo usarlo desde otra app — URL base, autenticación requerida, ejemplo mínimo
> - Swagger / documentación de API si existe
> - BDs que usa — motor, host, nombre, propósito
> - Servicios que consume — para entender sus dependencias
> - Dónde buscar más información — ruta local del `agents.md` del proyecto
>
> **Sé breve y conciso.** Incluye lo suficiente para conectarse — no más.
> Si los detalles completos ya están en Swagger o en el `agents.md` del proyecto, aquí va solo el enlace.
> El criterio es: ¿puede otra IA o desarrollador usar este servicio leyendo solo esta sección?
> Si la respuesta es no, falta información. Si ocupa más de una página, sobra información.

---

## Documentos del ecosistema

> Leer antes de inicializar, diseñar o desplegar cualquier proyecto nuevo.

| Documento | Descripción |
|---|---|
| [`infraestructura.md`](infraestructura.md) | Este documento — arquitectura de servidores, red, CTs y servicios |
| [`migraciones.md`](migraciones.md) | Registro global de cambios de schema de BD — ALTER TABLE, índices, tablas nuevas. Fuente de verdad de qué SQL hay que correr y en qué BDs |
| [`design-system.md`](design-system.md) | Sistema de diseño unificado SIGMA — paleta, tipografía, componentes, multi-plataforma |
| [`roadmap.md`](roadmap.md) | Hoja de ruta estratégica — decisiones técnicas tomadas, pendientes de ejecutar |
| [`prompt_ini_proyectos.md`](prompt_ini_proyectos.md) | Plantilla de inicialización para proyectos nuevos del ecosistema |

---

## Convenciones de scripts en proyectos

Todo proyecto del ecosistema usa exactamente **dos scripts**. Nada más para el despliegue.

### `desplegar.sh` — corre desde la máquina de desarrollo
Cómo lo hace depende del tipo de proyecto:
Todo proyecto debe tener o crear un bash sh llamado desplegar.sh, este se encarga de la sincronizacion de el proyecto a produccion.
1.- en caso de proyectos tipo webapps(app_fidelizacion, apps_ideas, sigmac-web,etc) o servicios(mail, siax-monitor,etc) sube el código al servidor de produccion asignado. 
2.- en caso de apps desarrolladas para moviles o table(sigmac-app, app_pedidos,etc), y pc(desktop-> SIGMAC, ERP, CRM,etc). estas despliegan directamente al proyecto de Web_siax-sytem(https://siax-system.net) y las se publican las url en la api de webcontrol("https://api.siax-system.net/")

| Tipo de proyecto | Mecanismo |
|-----------------|-----------|
| Interpretado (Node.js, Python, PHP) | `git push` al repo + SSH al servidor + `git pull` + reinicio del proceso |
| Compilado (Rust, Java, Go) | Compila localmente + `scp`/`rsync` del binario al servidor + reinicio |

Lee `servers.conf` para saber a qué servidores apuntar.
`servers.conf` **nunca se commitea** — cada desarrollador crea el suyo desde `servers.conf.example`.

### `init.sh` — corre en el servidor

Ejecutor local. Solo arranca lo que ya está instalado. No sube código, no compila.
Puede ser simple (un solo comando) o interactivo (menú de opciones).

### Referencia entre proyectos

| Proyecto | `desplegar.sh` | `init.sh` |
|---------|----------------|-----------|
| `siax_monitor` | Compila Rust + scp binario a cada servidor | Instala como servicio systemd |
| `api_service_ia` | git push + SSH + git pull + reinicio tmux | Interactivo — op.1: instala deps + arranca / op.2: solo arranca |
| _(nuevo proyecto)_ | Seguir el mismo patrón | Seguir el mismo patrón |

### Actuallizaciones de las Base de Datos de los proyecto.
Todo  proyecto al ser tipo tenancy usa su propia base de datos, la cual al sirve "https://api-gateway-cloud.telcotronics.net/" para consultarla se necesita una apikey, la cual es proporcionada solo por webcontrol("https://api.siax-system.net/") despues de realizar las debidas autenticaciones. 
Esto hace que siempre alla cambios en las bd. y por tal las actualizaciones sql siempre estarqan disponibles en webcontrol: "/api/sql/check_update", "/api/sql/updates". mas info en su api o la seccion dedicada en este doc.
cada proyecto tiene 2 bd una de empresa(EMPRESA_XXX) y otra llamada sigma que almacena las actualizaciones en la tabla: "SIGMA.HistorialActualizacionBD".
#### conclusion
cada proyecto debera implementar un algoritomo de control de versiones de las actualizaciones sea por bd o por versiones de ejecutables. en caso de webapps 

---



## MCPs del ecosistema Telcotronics

> El ecosistema tiene **4 MCPs independientes**, cada uno con un rol distinto.
> No confundirlos — conectarse al MCP equivocado da datos incorrectos o genera acciones en el sistema erróneo.

| MCP | URL | Rol | Estado |
|-----|-----|-----|--------|
| **Infraestructura** | `mcp.telcotronics.net` | Fuente de verdad de toda la infraestructura del ecosistema. Las IAs se conectan aquí para leer y actualizar servidores, CTs, redes, servicios y proyectos. **Fuente de este documento.** | 🔧 En mantenimiento |
| **Comunicaciones robóticas** | `sigma-robot.telcotronics.com` | Envío automatizado de mensajes: Email, WhatsApp y otros canales. Usado por agentes y robots del ecosistema para comunicarse con clientes y sistemas externos. | — |
| **ERP / CRM SIGMA** | — | Datos del ERP y CRM de SIGMA — productos, clientes, ventas, inventario. Usado por los módulos comerciales del ecosistema. | — |
| **Ideas** | `ideas.telcotronics.net` | Orquesta las ideas del ecosistema. Centraliza y coordina lo que se escribe en `ideas.md` de cada proyecto. | — |

---

## Ecosistema de Proyectos Telcotronics

| Proyecto | Repositorio / Git | Tecnología Principal | Responsable | Estado | Rol Central |
|---|---|---|---|---|---|
| **mail-monitor** | `https://git.telcotronics.net/pablinux/Monitor-ServerMail.git` | Rust (Axum + sqlx + Tera + HTMX) | pablinux | ✅ Activo | Administración y monitoreo del servidor de correo SIGMA (Postfix + Dovecot). Gestiona usuarios, logs, fail2ban y notifica eventos a API-SIGMA-WEBCONTROL |
| **SIAX Monitor** | `https://git.telcotronics.net/pablinux/SIAX-MONITOR` | Rust (Nativo) | pablinux | ✅ Activo | Agente de monitoreo systemd |
| **Webswing** | `https://git.telcotronics.net/pablinux/JAVA-WEB-SERVER-APPS` | Java 11 build + Jetty | pablinux | ✅ Activo | Servidor GUI a Canvas HTML5 |
| **SIGMAC** | Local — pendiente subir a git.telcotronics.net | Java 11 (NetBeans + Swing) + MySQL / HikariCP | pablinux | ✅ Producción | ERP desktop de facturación electrónica Ecuador. Corre sobre Webswing (CT 141). BD `facturacion` en .116. |
| **SIGMA-OPEN-API** | `https://github.com/telcotronics/xsystem-open-api` | Spring Boot 1.5.9 + Java 8 | pablinux | ✅ Activo (legacy) | API facturación SRI — sistemas existentes. Nueva URL: `api.factura-e.net` |
| **SIGMAC-SRI-API** | `https://git.telcotronics.net/pablinux/SIGMAC-SRI_API.git` | Spring Boot 1.5.9 + Java 8 | pablinux | ✅ Activo | Nueva API facturación SRI — sistemas nuevos. URL: `api.sigmac.app/sri` |
| **API-SIGMA-WEBCONTROL** | `https://git.telcotronics.net/pablinux/API-SIGMA-WEBCONTROL.git` | Node.js (Express) + MariaDB / MySQL | pablinux | ✅ Activo | Base de autorizaciones, notificaciones, identidades y onboarding |
| **API-SIGMA-CLOUD** | `https://github.com/telcotronics/api-gateway-cloud.git` | Node.js (Express) + MySQL | pablinux | ✅ Activo | API Gateway multi-tenant y motor transaccional comercial |
| **sigma-robot** | `https://git.telcotronics.net/pablinux/sigma-robot.git` | Node.js + Express + MySQL + Socket.IO | pablinux | ✅ Activo | Hub central de comunicaciones e IA. Recibe mensajes WhatsApp (Meta + Web Bot), los procesa con IA (fallback automático SIAX→DeepSeek→Gemini→Claude), expone AI Gateway compatible OpenAI para apps externas, y orquesta agentes IA con flujos configurables desde el panel. |
| **WebControlSigma** | `https://git.telcotronics.net/pablinux/Web_siax-sytem.git` | PHP 8.x + MySQL / MariaDB + Rivescript | pablinux | ✅ Activo | Panel web de control administrativo e interfaz visual para control de licencias, usuarios, captcha y gestión de API Keys en el ecosistema Telcotronics. |
| **sigmac_app** | `https://git.telcotronics.net/pablinux/sigmac_app.git` | Flutter 2.11 / Dart 2.17-beta | pablinux | 🟡 En desarrollo activo | App CRM companion multiplataforma (Android + Linux desktop). Cliente nativo offline-first para gestión de ventas, inventario, clientes, pedidos y proformas. Se sincroniza con API-SIGMA-CLOUD y se autentica vía API-SIGMA-WEBCONTROL. |
| **sigmac-web** | `https://git.telcotronics.net/pablinux/SIGMAC-WEB_PHP.git` | Laravel 13 (PHP 8.5) + Vue 3 + Tailwind CSS | pablinux | 🟡 En desarrollo activo | CRM web companion a sigmac_app. SPA Vue 3 + API REST Laravel (proxy). Módulos principales operativos. URL: `crm.sigmac.app`. Servidor-web CT 150 (.109). |
| **SitioWeb_telcotronics** | [pendiente — crear repo en git.telcotronics.net] | HTML5/CSS3/JS vanilla + PHP 8.5 + PHPMailer | pablinux | ✅ v2.3.1 | Sitio web institucional y tienda en línea de Telcotronics. 914 productos reales vía API-SIGMA-CLOUD. Apache .109 `/var/www/web_telcotronics/public_html/`. Dominio: `telcotronics.com`. |
| **app_ideas** | `https://git.telcotronics.net/pablinux/APPA-GENERQADOR-DE-IDEAS.git` | Node.js (Express) + MongoDB + EJS | pablinux | 🟡 En desarrollo activo | Canvas de ideas y pensamiento visual. Genera, organiza y visualiza ideas con soporte de IA. Incluye panel de dibujo, flujo, recopilación de procesos e integración con AIT (IA Telcotronics). Puerto 2000. BD: MongoDB `app_ideas` en CT 102 (.146). |
| **app_marketing** | [pendiente — crear repo en git.telcotronics.net] | Node.js (Express) + MongoDB + EJS | pablinux | ✅ Activo | Centro de publicidad y marketing multi-tenant del ecosistema. Gestiona campañas internas y de anunciantes, las sirve vía API REST y widget JS embebible. Trackea impresiones y clics por campaña y por app origen. Puerto 2100. BD: MongoDB `app_marketing` en CT 102 (.146). |
| **app_fidelizacion** | [pendiente — crear repo en git.telcotronics.net] | Node.js (Express) + MySQL + EJS | pablinux | 🟡 En desarrollo activo | Plataforma de lealtad, escáner QR y canjes. Gestión de clientes y transacciones de partners. Puerto 2001. BD: MySQL `nexo_fd` en 192.168.10.149. |
| **api_service_ia** | `git@github.com:telcotronics/API_Service_IA.git` | Python 3.14 + FastAPI + uvicorn | pablinux | 🟡 En desarrollo activo | API REST de modelos de IA preentrenados (OCR, STT, TTS, visión facial, PDF). Único proyecto Python serio del ecosistema. Puerto 8000. BD: MariaDB `api_ia_python` en .149. |
| **API_CENTINEL_SECURITY** | `https://git.telcotronics.net/pablinux/API-CENTINEL-SECURITY.git` | Java 17 + Spring Boot 3.3 + WebClient | pablinux | ✅ Activo | API de Gestión de Seguridad Electrónica — control de acceso físico, biometría, apertura remota de puertas, sincronización de credenciales y eventos en tiempo real. Punto único de integración para cualquier app que gestione seguridad física en el ecosistema. |
| **audio_control** | [pendiente — git.telcotronics.net] | Node.js (Express) + MySQL + EJS + Socket.IO | pablinux | 🟡 En desarrollo | Backend SoundWave — control remoto de reproducción de audio, descarga YouTube, playlist MySQL y auth Google OAuth 2.0. Puerto 4000. |
| **SoundWave** | [pendiente — git.telcotronics.net] | Vue 3 + Vite 7 (PWA) / Node.js (Express) + MongoDB | pablinux | 🟡 En desarrollo activo | Reproductor de música personal PWA. Frontend Vue 3 + backend Express propio (puerto 2005). Auth Google OAuth, streaming con seek, biblioteca compartida en servidor. |
| **app_sigma_inventario** (Control Inventario) | [pendiente — git.telcotronics.net] | Flutter (Android / Linux Desktop) / Dart | pablinux | 🟡 En desarrollo activo | App móvil para supervisores y bodegueros: conciliación física de stock, traslados con código de barras y recepción OCR externa. |
| **agente_ventas** | [sin repositorio — local] | Flutter 2.11 / Dart 2.17-beta + SQLite | pablinux | 🟡 En desarrollo activo — integrando API real | App "Agente Ventas SIGMAC" — gestión de rutas y pedidos de campo para vendedores de Telcotronics. Ruta del día, catálogo, pedidos, firma digital, scanner QR/barcode, notificaciones in-app. Auth vía API-SIGMA-WEBCONTROL · datos vía API-SIGMA-CLOUD (BD `TELCOTRONICS`). |
| **seguridad_electronica (SENTINEL ONE)** | `https://git.telcotronics.net/pablinux/seguridad_electronica.git` | Flutter 2.11 / Dart 2.17-beta + SQLite | pablinux | 🟡 En desarrollo activo | App de seguridad electrónica offline-first. Monitoreo de alarmas por zona, control de acceso a puertas, mensajería interna con la central. Pendiente de integrar API real del proveedor de seguridad. |

---

---

## Infraestructura física

### Red

| Parámetro | Valor |
|-----------|-------|
| Red local | 192.168.10.0/24 |
| Router / DHCP | MikroTik — XSYSTEM MKT |
| DNS / AdBlocker | AdGuard — 192.168.10.2 |
| WiFi AP | EW1200G-PRO — 192.168.10.254 |

> **Nota:** Los contenedores LXC de Proxmox se identifican por MAC con prefijo `BC:24:11:*`. Las IPs no siguen el número del CT — son históricas y se mantienen desde antes de Proxmox.

---

### Conexiones WAN y NAT — MikroTik XSYSTEM MKT

El ecosistema tiene **3 conexiones a internet** con interfaces separadas en el MikroTik. Cada una tiene su propio conjunto de NATs y sirve servicios distintos.

#### Interfaces WAN

| Interface | Tipo | IP pública | Velocidad | Destino principal |
|-----------|------|-----------|-----------|-------------------|
| `P1 WAN` | Fibra directa | `181.198.143.66` | 15 Gbps | Apache .109 (sitios web) + correo + RustDesk |
| `CHR-MKT_old` | VPN tunnel → VPS Google (antiguo) | `34.170.252.64` | — | Nginx Proxy Manager .141 |
| `CHR_XSYSTEM_V2` | VPN tunnel → VPS Google (nuevo) | `104.198.154.171` | — | server-webapps .160 |

> **DNS por dominio:**
> - `siax-system.net` → gestionado por **Cloudflare** (con o sin proxy según el servicio)
> - `sigmac.app`, `telcotronics.net`, `telcotronics.com`, etc. → gestionados en su registrador propio
>
> **`crm.sigmac.app`** — A record directo a `181.198.143.66` (fibra P1 WAN). No necesita Cloudflare proxy: es un CRM de usuarios limitados, la IP de fibra es estable y certbot maneja el SSL en el servidor.

#### NAT Rules activas

| # | Interface entrada | Puerto ext | Destino interno | Servicio |
|---|-------------------|-----------|----------------|---------|
| 3 | CHR_XSYSTEM_V2 | 80 | 192.168.10.160:80 | Nginx (VPS nuevo) |
| 4 | CHR_XSYSTEM_V2 | 443 | 192.168.10.160:443 | Nginx (VPS nuevo) |
| 5 | CHR-MKT_old | 80 | 192.168.10.141:80 | Nginx Proxy Manager |
| 6 | CHR-MKT_old | 443 | 192.168.10.141:443 | Nginx Proxy Manager |
| 7 | P1 WAN | 80 | 192.168.10.109:80 | **Apache — sitios web** |
| 8 | P1 WAN | 443 | 192.168.10.109:443 | **Apache — sitios web (SSL)** |
| 10 | P1 WAN | 25 | 192.168.10.111:25 | SMTP (Postfix) |
| 11 | P1 WAN | 993 | 192.168.10.111:993 | IMAP SSL (Dovecot) |
| 12 | P1 WAN | 587 | 192.168.10.111:587 | SMTP Submission |
| 13 | P1 WAN | 465 | 192.168.10.111:465 | SMTPS |
| 14 | CHR-MKT_old | 25 | 192.168.10.99:25 | SMTP cluster (mail secundario) |
| 15 | CHR-MKT_old | 143 | 192.168.10.99:143 | IMAP cluster |
| 19-21 | P1 WAN | 21114-21119 | 192.168.10.105:21114+ | RustDesk (UDP+TCP) |

#### NAT Rules deshabilitadas (legacy / pendientes)

| # | Servicio | Destino | Motivo |
|---|---------|---------|--------|
| 1 | SMTP por VPN | .150:25 | Legacy server-sigma |
| 9 | Webmin | .150:10000 | Legacy en retiro |
| 16 | SIGMA-WEB | .150:8443 | Legacy en retiro |
| 17 | WEB-SWING | .110:8090 | Acceso directo desactivado |
| 18 | MONITOR SIAX | .150:8080 | Legacy |

#### Flujo de tráfico por dominio

```
Internet
   │
   ├─ Fibra P1 WAN ──────────────► .109 Apache
   │                                  factura-e.net, crm.sigmac.app
   │                                  sigmac.app, telcotronics.com, etc.
   │                                  Correo: .111 (25/587/465/993)
   │                                  RustDesk: .105
   │
   ├─ VPS Google (viejo) ────────► .141 Nginx Proxy Manager
   │   CHR-MKT_old                    api-gateway-cloud.telcotronics.net
   │                                  git, n8n, proxy, mail, voip, etc.
   │
   └─ VPS Google (nuevo) ────────► .160 server-webapps
       CHR_XSYSTEM_V2                 klickbot.app, mesh.telcotronics.net
                                      api-gateway-sigma.telcotronics.net
```

---

### Hypervisor

| Parámetro | Valor |
|-----------|-------|
| Plataforma | Proxmox VE |
| Nombre | BLACK-SERVER |
| Nodo `cloud` | Servidor nuevo — CTs críticos de producción SIGMA |
| Nodo `cluster` | Servidor principal — resto de servicios del ecosistema |

---

### Todos los CTs y servicios del ecosistema

#### Nodo cloud (producción SIGMA)

| CT | IP | Nombre | Tecnología | Rol | Estado |
|----|-----|--------|-----------|-----|--------|
| 141 | 192.168.10.110 | Servidor-SIGMA-VW | Webswing 20.2.5 + Java Swing | Frontend SIGMA | running |
| 142 | 192.168.10.120 | SIGMA-OPEN-API / SIGMAC-SRI-API | Spring Boot 1.5.9 + Java 8 | API REST facturación (puerto 8080 legacy + 8082 nueva) | running |
| 144 | 192.168.10.111 | servidor-email | Postfix + Dovecot + SnappyMail + **mail-monitor** | Correo + administración | running |
| 145 | 192.168.10.116 | SERVIDOR-BD | PostgreSQL 16.13 | BD sigma_api | running |
| 150 | 192.168.10.109 | Servidor-web | Apache 2.4.66 + PHP 8.5-FPM | Proxy reverso público + host de sitios PHP | running |

#### Nodo cluster (ecosistema)

| CT | IP | Nombre | Tecnología | Rol | Estado |
|----|-----|--------|-----------|-----|--------|
| 100 | 192.168.10.141 | nginxproxymanager | Nginx Proxy Manager | Reverse proxy con UI | running |
| 101 | 192.168.10.143 | cloudflared | Cloudflare Tunnel | Túnel seguro internet | running |
| 102 | 192.168.10.146 | mongodb | MongoDB | BD documental | running |
| 103 | 192.168.10.2 | adguard | AdGuard Home | DNS + bloqueador ads | running |
| 105 | 192.168.10.145 | Ubuntu-Docker | Node.js + **API-SIGMA-WEBCONTROL** | API central auth/onboarding (tmux, pendiente siax-monitor) | running |
| 107 | 192.168.10.156 | syncthing | Syncthing | Sincronización archivos | running |
| 108 | 192.168.10.108 | Servidor-IA (SIAX) | IA autónoma | Coordinador autónomo | running |
| 110 | 192.168.10.106 | meshcentral | MeshCentral | Gestión remota equipos | running |
| 114 | 192.168.10.149 | mariadb | MariaDB + phpMyAdmin | BD relacional (mailserver_db) | running |
| 121 | 192.168.10.112 | SERVER-MAIL | — | Servidor mail secundario | running |
| 122 | 192.168.10.171 | n8n | n8n | Automatización flujos | running |
| 123 | 192.168.10.107 | rustdeskserver | RustDesk Server | Escritorio remoto | running |
| 124 | 192.168.10.173 | jupyternotebook | Jupyter Notebook | Data science / IA | running |
| 125 | 192.168.10.148 | sqlserver2022 | SQL Server 2022 | BD Microsoft | running |
| 128 | 192.168.10.103 | VOIP-SERVER | — | Telefonía IP | running |
| 130 | 192.168.10.151 | gitea | Gitea | Repositorio Git | running |
| 132 | 192.168.10.160 | server-webapps | Node.js / PM2 + **API-SIGMA-CLOUD** | Apps web + API Gateway | running |
| 133 | 192.168.10.144 | redis | Redis | Cache en memoria | running |
| 134 | 192.168.10.102 | apache-tomcat | Apache Tomcat | Servidor Java legacy | running |
| 137 | 192.168.10.172 | flowiseai | Flowise AI | Flujos IA low-code | running |
| 138 | 192.168.10.152 | jenkins | Jenkins | CI/CD | running |
| 139 | 192.168.10.147 | postgresql | PostgreSQL | BD adicional | running |
| 140 | 192.168.10.98 | API-FACTURACION | — | API facturación adicional | running |
| 143 | 192.168.10.115 | DB-EMPRESAS | — | BD de empresas (Tenants) | running |

---

### Mapa de dominios

#### Nginx Proxy Manager (CT 100 — 192.168.10.141)

> Gestiona todos los dominios públicos del ecosistema con SSL automático vía Let's Encrypt.
> Panel admin: `https://proxy.telcotronics.net`

| # | Dominio(s) | Destino interno | SSL | Estado |
|---|-----------|----------------|-----|--------|
| 1 | `mesh.telcotronics.net` | 192.168.10.160:443 | HTTP Only | ✅ Online |
| 2 | `cluster.telcotronics.net` | 192.168.10.140:8006 | Let's Encrypt | ✅ Online |
| 3 | `proxy.telcotronics.net` | 192.168.10.141:81 | Let's Encrypt | ✅ Online |
| 4 | `telcotronics.net` | 192.168.10.166:80 | HTTP Only | ✅ Online |
| 5 | `android.telcotronics.net` | 192.168.10.150:4000 | Let's Encrypt | ✅ Online |
| 8 | `n8n.telcotronics.net` | 192.168.10.171:5678 | Let's Encrypt | ✅ Online |
| 9 | `whisper.telcotronics.net` | 192.168.10.145:8000 | Let's Encrypt | ✅ Online |
| 10 | `voip.telcotronics.net` | 192.168.10.102:80 | Let's Encrypt | ✅ Online |
| 11 | `sigma.telcotronics.net` | 192.168.10.150:8443 | Let's Encrypt | ❌ Offline |
| 12 | `api.telcotronics.net` | 192.168.10.145:8000 | Let's Encrypt | ✅ Online |
| 13 | `dibujo.telcotronics.net` | 192.168.10.159:3000 | Let's Encrypt | ✅ Online |
| 15 | `xsend.telcotronics.net` | 192.168.10.147:80 | Let's Encrypt | ✅ Online |
| 17 | `git.telcotronics.net` | 192.168.10.151:3000 | Let's Encrypt | ✅ Online |
| 19 | `api.klickbot.app` | 192.168.10.170:4001 | Let's Encrypt | ✅ Online |
| 20 | `app.klickbot.app` | 192.168.10.170:3001 | Let's Encrypt | ✅ Online |
| 22 | `api-gateway-cloud.telcotronics.net` | 192.168.10.160:3003 | Let's Encrypt | ✅ Online |
| 23 | `api-gateway-sigma.telcotronics.net` | 192.168.10.160:3003 | Let's Encrypt | ✅ Online |
| 24 | `klickbot.app` | 192.168.10.160:3005 | Let's Encrypt | ✅ Online |

> **Nota:** `api-gateway-cloud` y `api-gateway-sigma` apuntan al mismo destino (.160:3003) — dos dominios para el mismo servicio API-SIGMA-CLOUD. `sigma.telcotronics.net` offline — servicio en .150 (legacy en retiro).

---

### Equipos de desarrollo

| IP | Nombre | Descripción |
|----|--------|-------------|
| 192.168.10.100 | siax-amd | Workstation AMD — desarrollo |
| 192.168.10.101 | siax-intel | Workstation Intel — desarrollo |
| 192.168.10.72 | pablinux-laptop | Laptop de trabajo |
| 192.168.10.155 | DAPSI | Sistema de domótica |

---

### Servidor legacy en retiro

| Parámetro | Valor |
|-----------|-------|
| Nombre | server-sigma |
| IP | 192.168.10.150 |
| OS | Ubuntu 20.04 LTS |
| Estado | ⚠️ En proceso de retiro |
| Historia | Servidor monolítico original. BD ya migrada. Casi vacío. |
en contenedor ia va a reusar la ip por el nuevo servidor  -> Servidor-API-CENTINEL:~/apps$
ip a 192.168.10.150/24

---

---

## Bases de datos

### CT cloud — SERVIDOR-BD (192.168.10.116)

| Parámetro | Valor |
|-----------|-------|
| IP | 192.168.10.116 |
| MAC | BC:24:11:50:DE:27 |
| CT Proxmox | 145 (nodo cloud) |
| OS | Ubuntu 24.04 LTS |
| Motores activos | **MySQL 8.0.45** (Producción) / **PostgreSQL 16.13** (API) |
| Bases de datos MySQL | `TELCOTRONICS` (servidor propio de la dueña y patrocinadora), `SIGMA`, `facturacion` |
| Bases de datos PostgreSQL | `sigma_api` (SIGMA-OPEN-API legacy), `sigmac_sri` (SIGMAC-SRI-API nueva), `veronica` (Base original) |
| Rol central | Servidor de base de datos de producción exclusivo de **TELCOTRONICS**. **MySQL** hospeda sus datos comerciales privados en total aislamiento sin compartir nada. **PostgreSQL** es el motor compartido para el almacenamiento de facturas electrónicas de clientes exclusivamente a través de la API `sigma-open-api`. |

**⚠️ Notas de Configuración:**
*   **MySQL (Puerto 3306):** Hospeda de manera aislada y privada los datos comerciales e internos de Telcotronics. No tiene contacto con clientes ni con `sigma-open-api`.
*   **PostgreSQL (Puerto 5432):** Hospeda la base `sigma_api` utilizada de forma compartida por `sigma-open-api` para facturación electrónica con el SRI. Mantener `password_encryption = md5`. El driver JDBC `postgresql-9.4.1212.jre7` no soporta `scram-sha-256`.

---

### CT cluster — mariadb (192.168.10.149)

| Parámetro | Valor |
|-----------|-------|
| IP | 192.168.10.149 |
| MAC | BC:24:11:96:D4:49 |
| CT Proxmox | 114 (nodo cluster) |
| OS | Debian 12 |
| Motor | **MariaDB 10.11.14** |
| Base de datos crítica | **`webControl`** (Base central de WebControlSigma / `Web_siax-sytem`) |
| Otras BDs hospedadas | `mailserver_db` (correo), `gitea` (repositorios), `siax_core`, `SIGMA`, `TELCOTRONICS`, `facturacion`, entre otras (27 BDs en total). |
| Rol central | Servidor de base de datos relacional del clúster del ecosistema. Provee almacenamiento centralizado y es donde vive la base de datos `webControl` con las tablas `usuarios_sesion` (login) y `api_key` (llaves de API). |

---

### CT cluster — DB-EMPRESAS (192.168.10.115)

| Parámetro | Valor |
|-----------|-------|
| IP | 192.168.10.115 |
| MAC | BC:24:11:D4:3C:73 |
| CT Proxmox | 143 (nodo cluster) |
| OS | Ubuntu 24.04 LTS |
| Motor | **MySQL 8.0.45** |
| Bases de datos hospedadas | `EMPRESA_EL_SOL` (Base de datos de cliente tenant activo), `admin` |
| Rol central | Servidor de bases de datos de clientes (Tenants) del ecosistema. Utilizado críticamente por `api-gatewaycloud.telcotronics.net` (`API-SIGMA-CLOUD`) para enrutar de forma dinámica y síncrona el flujo comercial diario de los clientes finales. |

---

---

## APIs

### Sistema SIGMA — Facturación electrónica

SIGMA es el sistema de **facturación electrónica** para Ecuador, basado en el proyecto open source [Verónica](https://github.com/RolandoPalermo/veronica-open-api), adaptado localmente. Se comunica con el **SRI** para envío y autorización de comprobantes electrónicos. Corre en el nodo **cloud** de Proxmox.

#### Flujo de una factura

```
Usuario (navegador)
      │
      ▼
Servidor-SIGMA-VW — Webswing (192.168.10.110)
App Java Swing corriendo en servidor, visible en navegador vía HTML5
      │
      ▼
Servidor-web — Apache proxy (192.168.10.109)
api.factura-e.net → 192.168.10.120:8080
      │
      ▼
SIGMA-OPEN-API — Spring Boot (192.168.10.120:8080)
      │                        │
      ▼                        ▼
SERVIDOR-BD               SRI Ecuador
PostgreSQL 16             cel.sri.gob.ec (internet)
192.168.10.116:5432
```

---

### CT cloud — SIGMA-OPEN-API (192.168.10.120)

| Parámetro | Valor |
|-----------|-------|
| IP | 192.168.10.120 (IP fija) |
| MAC | BC:24:11:1D:F6:60 |
| CT Proxmox | 142 (nodo cloud) |
| OS | Ubuntu 24.04 LTS |
| Rol | API REST de facturación electrónica |
| Framework | Spring Boot 1.5.9 |
| Java | OpenJDK **8** (1.8.0_482) — **NO usar Java 9+** |
| Puerto | 8080 |
| Contexto URL | `/veronica` |
| Usuario deploy | `pablinux` |

**Ruta del proyecto:** `/home/pablinux/app/sigma-open-api/`

**Arrancar:**
```bash
sh /home/pablinux/app/1_factElect_modoPROD.sh   # producción
sh /home/pablinux/app/0_factElect_modoDEV.sh    # desarrollo
```

**Endpoints:**
| Recurso | URL |
|---------|-----|
| Swagger UI | `http://192.168.10.120:8080/veronica/swagger-ui.html` |
| OAuth token | `POST http://192.168.10.120:8080/veronica/oauth/token` |
| API facturas | `http://192.168.10.120:8080/veronica/api/v1.0/` |

**⚠️ Si Maven falla por repositorios HTTP bloqueados:** comentar bloque `maven-default-http-blocker` en `/usr/share/maven/conf/settings.xml`.

---

### CT cloud — SIGMAC-SRI-API (192.168.10.120 — puerto 8082)

| Parámetro | Valor |
|-----------|-------|
| Repositorio Git | `https://git.telcotronics.net/pablinux/SIGMAC-SRI_API.git` |
| Tecnología principal | Spring Boot 1.5.9 + Java 8 (⚠️ Java 9+ rompe dependencias de firma digital) |
| Responsable | pablinux |
| Estado actual | ✅ Producción |
| Equipo / ubicación local | `siax-amd` (`192.168.10.100`) — `/home/pablinux/Projects/java/sigmac-sri-api` |
| CT Proxmox | 142 (nodo cloud) — comparte CT con SIGMA-OPEN-API |
| Puerto interno | `8082` |
| URL interna | `http://192.168.10.120:8082/sri` |
| Dominio público | `https://api.sigmac.app` (SSL Let's Encrypt — expira 2026-08-30) |
| Contexto URL | `/sri` |
| Autenticación | OAuth2 Password Grant — `POST https://api.sigmac.app/sri/oauth/token` |
| Documentación API | `https://api.sigmac.app/sri/swagger-ui.html` |
| Última actualización | 2026-06-01 |

`SIGMAC-SRI-API` es el fork limpio y propiedad total de Telcotronics de la API de facturación electrónica SRI. Sucesor de `SIGMA-OPEN-API` con namespace unificado `com.telcotronics.sri`. Gestiona el ciclo de vida completo de comprobantes electrónicos: generación XML → firma XAdES-BES → envío SRI → autorización → RIDE (PDF). **Esta es la API oficial del ecosistema. Todos los sistemas nuevos deben integrar esta API.**

> ⚠️ **`SIGMA-OPEN-API` (`api.factura-e.net`) entra en estado LEGACY** — solo se mantiene para sistemas existentes que no pueden actualizarse. No integrar nuevos proyectos contra ella. La migración progresiva hacia `api.sigmac.app` es el camino a seguir.

**Credenciales de acceso:**

| Tipo | Parámetro | Valor | Uso |
|------|-----------|-------|-----|
| OAuth2 client | client / secret | `pablinux` / `Microbot%` | Requerido en todas las peticiones de token — va en HTTP Basic Auth |
| Usuario ADMIN | username / password | `admin` / `SigmacAdmin.2026@` | `ROLE_ADMIN` — gestión de certificados, usuarios, catálogos, stats |
| Usuario MONITOR | username / password | _(crear vía admin)_ | `ROLE_MONITOR` — monitoreo operativo: tokens, certificados, stats. Sin acceso a gestión |
| Usuario USER (pruebas) | username / password | `facturador_app` / `SigmacUser.2026@` | `ROLE_USER` — emisión de comprobantes. Usar para pruebas; cada cliente solicita su propio usuario al admin |

> Cada sistema o cliente que consuma esta API debe solicitar al admin la creación de su propio usuario con `ROLE_USER` vía `POST /sri/operaciones/usuarios`.

**Cómo obtener un token y usarlo (ejemplo completo):**

```bash
# 1. Obtener token (client en Basic Auth, usuario en el body)
curl -u pablinux:Microbot% -X POST https://api.sigmac.app/sri/oauth/token \
  -d "username=facturador_app&password=SigmacUser.2026@&grant_type=password"
# Respuesta: { "access_token": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", "expires_in": 1199 }

# 2. Usar el token en cada petición
curl https://api.sigmac.app/sri/api/v1.0/facturas/{claveAcceso}/archivos/xml \
  -H "Authorization: Bearer xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"

# 3. Token ADMIN para stats y gestión
curl -u pablinux:Microbot% -X POST https://api.sigmac.app/sri/oauth/token \
  -d "username=admin&password=SigmacAdmin.2026@&grant_type=password"
```

**BD que usa:**

| BD | Host | Motor | Uso |
|----|------|-------|-----|
| `sigmac_sri` | `192.168.10.116:5432` | PostgreSQL 16.13 | Comprobantes electrónicos (facturas, retenciones, guías, notas, liquidaciones) |

**Endpoints principales (para integración):**

| Método | Endpoint | Descripción | Auth |
|--------|---------|-------------|------|
| POST | `https://api.sigmac.app/sri/oauth/token` | Obtener token OAuth2 | Client `pablinux:Microbot%` |
| POST | `https://api.sigmac.app/sri/api/v1.0/facturas` | Crear y firmar factura | `ROLE_USER` |
| PUT | `https://api.sigmac.app/sri/api/v1.0/facturas/{clave}/enviar` | Enviar al SRI | `ROLE_USER` |
| PUT | `https://api.sigmac.app/sri/api/v1.0/facturas/{clave}/autorizar` | Consultar autorización | `ROLE_USER` |
| GET | `https://api.sigmac.app/sri/api/v1.0/facturas/{clave}/archivos/pdf` | Descargar RIDE (PDF) | `ROLE_USER` |
| GET | `https://api.sigmac.app/sri/api/v1.0/facturas/{clave}/archivos/xml` | Descargar XML firmado | `ROLE_USER` |
| GET | `https://api.sigmac.app/sri/operaciones/stats/resumen` | Total por tipo y estado | `ROLE_ADMIN` |
| GET | `https://api.sigmac.app/sri/operaciones/stats/hoy` | Comprobantes del día | `ROLE_ADMIN` |
| GET | `https://api.sigmac.app/sri/operaciones/stats/recientes?limit=N` | Últimos N comprobantes | `ROLE_ADMIN` |
| GET | `https://api.sigmac.app/sri/monitor/tokens` | Tokens activos por usuario | `ROLE_MONITOR` |
| DELETE | `https://api.sigmac.app/sri/monitor/tokens/{username}` | Revocar tokens de un usuario | `ROLE_MONITOR` |
| GET | `https://api.sigmac.app/sri/monitor/certificados` | Estado y caducidad de certs PKCS12 | `ROLE_MONITOR` |
| GET | `https://api.sigmac.app/sri/monitor/stats/resumen` | Resumen general (monitor) | `ROLE_MONITOR` |
| GET | `https://api.sigmac.app/sri/monitor/stats/hoy` | Comprobantes del día (monitor) | `ROLE_MONITOR` |
| GET | `https://api.sigmac.app/sri/monitor/stats/recientes?limit=N` | Últimos N comprobantes (monitor) | `ROLE_MONITOR` |

El mismo patrón de endpoints aplica para: `retenciones`, `guias-remision`, `notas-credito`, `notas-debito`, `liquidaciones-compra`.

**Módulos disponibles:**

| Módulo | Endpoint base | Auth | Estado |
|--------|--------------|------|--------|
| Factura | `/sri/api/v1.0/facturas` | ROLE_USER | ✅ Operativo |
| Retención | `/sri/api/v1.0/retenciones` | ROLE_USER | ✅ Operativo |
| Guía de Remisión | `/sri/api/v1.0/guias-remision` | ROLE_USER | ✅ Operativo |
| Nota de Crédito | `/sri/api/v1.0/notas-credito` | ROLE_USER | ✅ Operativo |
| Nota de Débito | `/sri/api/v1.0/notas-debito` | ROLE_USER | ✅ Operativo |
| Liquidación de Compra | `/sri/api/v1.0/liquidaciones-compra` | ROLE_USER | ✅ Operativo |
| Estadísticas (admin) | `/sri/operaciones/stats/*` | ROLE_ADMIN | ✅ Operativo |
| Monitor | `/sri/monitor/*` (tokens, certificados, stats) | ROLE_MONITOR | ✅ Operativo |

**Servicios externos que consume:**

| Servicio | URL | Uso |
|---------|-----|-----|
| SRI Recepción (prod) | `https://cel.sri.gob.ec/.../RecepcionComprobantesOffline?wsdl` | Envío comprobantes |
| SRI Autorización (prod) | `https://cel.sri.gob.ec/.../AutorizacionComprobantesOffline?wsdl` | Autorización SRI |

**Integración con el ecosistema:**
- Independiente — no consume APIs internas del ecosistema
- Los sistemas nuevos que requieran facturación deben apuntar a `api.sigmac.app/sri`
- Para más información técnica: `siax-amd:/home/pablinux/Projects/java/sigmac-sri-api/agents.md`

**Arrancar en producción:**
```bash
cd /home/pablinux/app/sigmac-sri-api
./init.sh   # selecciona 2 (producción)
# o: java -jar sigmac-sri-api.jar
```

---

### API-SIGMA-WEBCONTROL — Centro de control administrativo y seguridad

| Parámetro | Valor |
|-----------|-------|
| Repositorio Git | `https://git.telcotronics.net/pablinux/API-SIGMA-WEBCONTROL.git` |
| Tecnología principal | Node.js (Express) con pool de conexión `mysql2/promise` |
| Responsable | pablinux |
| Estado actual | ✅ Producción — `Ubuntu-Docker` CT 105 (`192.168.10.145`) |
| Equipo / ubicación local | `siax-amd` (`192.168.10.100`) — `/home/pablinux/Projects/Node/API-SIGMA-WEBCONTROL` |
| Proceso | `tmux` sesión con `npm start` en `/root/app/API-SIGMA-WEBCONTROL` — pendiente migrar a **siax-monitor** |
| Puerto interno | `3002` |
| URL interna | `http://192.168.10.145:3002` |
| Dominio público | `https://api.siax-system.net` (vía Cloudflare — SSL) |
| Autenticación | Login por `usrSesion_email` — soporta bcrypt y plain-text con auto-migración silenciosa |
| Rol en el ecosistema | Núcleo central de autorizaciones y notificaciones de salud del ecosistema completo |
| Última actualización | 2026-06-16 (2) |

`API-SIGMA-WEBCONTROL` es el cerebro y columna vertebral de seguridad y eventos del ecosistema SIGMA. Actúa como la fuente única de verdad para autorizar procesos y recopilar la salud e incidencias operativas de toda la red local y cloud de Telcotronics:

*   **Base Central de Autorizaciones (API Keys)**: Genera, almacena y valida las llaves de acceso de sistema (**API Keys** en la tabla `webControl.api_key`). Es consumida críticamente por las aplicaciones comerciales y, fundamentalmente, por agentes de monitoreo e infraestructura como **SIAX Monitor**, **mail-monitor** o **server-monitor** (encargado de alertar sobre la caída de instancias o servidores) para autenticar sus despachos de telemetría.
*   **Base Central de Notificaciones de Salud y Eventos**: Centraliza y procesa el flujo de logs de errores, caídas de servicios y alertas críticas del sistema. Despacha alertas a las interfaces correspondientes tras recibir notificaciones de eventos (como caídas detectadas por los monitores del cluster o estados de rechazo de documentos del SRI procesados por n8n).
*   **CRM y Licenciamiento**: Controla el registro de empresas aliadas y gestiona los parámetros globales de suscripciones y accesos de usuarios de plataforma.
*   **Onboarding Automático en 3 Pasos**:
    1.  *Pre-registro*: Registra provisionalmente datos en la tabla temporal `usuarios_xValidar` (`usr_est=0`), genera un token y despacha un código OTP de 6 dígitos vía correo electrónico (`emailService.js`) con rate limiting (3 intentos cada 15 min) para mitigar spam de cuentas.
    2.  *Verificación OTP*: Valida el OTP antes de 10 minutos desde el envío. Tras verificarlo, cambia el estado a `usr_est=1` y autoriza al cliente a instanciar la cuenta definitiva.
    3.  *Aprovisionamiento de Base de Datos*: Crea el usuario definitivo en la tabla `usuarios_sesion` (contraseña bcrypt) y clona síncronamente el molde MySQL oficial hacia la nueva base de datos del cliente (`EMPRESA_XXX`) en el host de Tenants (`.115`) ejecutando el script `tenantSchema.js`.
*   **Directorio Centralizado de Clientes**: Proveedor de búsqueda y validación global de datos tributarios RUC/Cédula integrando consultas en bases internas y servicios externos.

**BDs que usa:**

| BD | Host | Motor | Uso |
|----|------|-------|-----|
| `webControl` | `192.168.10.149` | MariaDB 10.11 | `usuarios_sesion` (identidades + login), `usuarios_xValidar` (onboarding temporal), `api_key` (llaves de API), `aplicaciones`, `aplicaciones_versiones` |
| `SIGMA` | `192.168.10.116` | MySQL 8.0 | `HistorialActualizacionBD` — scripts SQL delta distribuidos a todas las apps del ecosistema |
| `EMPRESA_SEED` | `192.168.10.115` | MySQL 8.0 | BD semilla — clonada para crear `EMPRESA_XXX` en el onboarding paso 3 |
| `EMPRESA_XXX` (dinámica) | `192.168.10.115` | MySQL 8.0 | BD del nuevo tenant — aprovisionada automáticamente en onboarding paso 3 |

**Servicios que consume:**

| Servicio | Host / URL | Uso |
|---------|-----------|-----|
| SMTP | `smtp.sigmac.app:587` (interno: `192.168.10.111:587`) | Envío de OTP al registrar usuarios — `no-reply@sigmac.app`, STARTTLS |

**Endpoints principales (para integración):**

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| POST | `/api/auth/pre-register` | Paso 1 onboarding — registro temporal + envío OTP | Pública |
| POST | `/api/auth/verify-otp-registro` | Paso 2 — verificación OTP (10 min, rate limit 3 intentos/15 min) | Pública |
| POST | `/api/auth/register` | Paso 3 — cuenta definitiva + aprovisionamiento BD tenant | Pública |
| POST | `/api/auth/empresas` | Pre-login — devuelve empresas del email sin emitir JWT. `unica: true` si solo tiene una. | Pública |
| POST | `/api/auth/login` | Login — emite JWT (8h) + apiKey. `?dba=EMPRESA_XXX` opcional para multi-empresa. Registra `usrSesion_ultimo_login`. | Pública |
| POST | `/api/auth/forgot-password` | Recuperación paso 1 — envía OTP al email. Respuesta genérica (no revela si existe). | Pública |
| POST | `/api/auth/reset-password` | Recuperación paso 2 — verifica OTP y actualiza contraseña en cloud. | Pública |
| GET | `/api/apps` | Lista apps satélite del ecosistema con metadata | `x-api-key` |
| GET | `/api/apps/versiones` | Lista versiones registradas (filtrables por app) | `x-api-key` |
| POST | `/api/apps/versiones` | Publica nueva versión de app (versión, changelog, url_descarga, archivo_md5, estado) | `x-api-key` |
| GET | `/api/apps/versiones/:app_nombre/latest` | Última versión activa — usada por apps cliente para auto-actualización | `x-api-key` |
| GET | `/api/apps/versiones/:app_nombre/md5` | Hash MD5 del ejecutable de la versión activa — el cliente lo compara con el MD5 del archivo descargado para verificar integridad | `x-api-key` |
| GET | `/api/sql/check_update` | Resumen rápido: total scripts y versión más reciente en `HistorialActualizacionBD` | `x-api-key` |
| GET | `/api/sql/updates?since=YYYY-MM-DD` | Scripts activos desde fecha indicada — paginado, máx 500/página | `x-api-key` |
| GET | `/api/sql/updates/:id` | Script por ID (incluye inactivos — para auditoría y reintentos) | `x-api-key` |
| POST | `/api/sql/updates` | Publica nuevo script delta (uso exclusivo del equipo de desarrollo) | `x-api-key` |
| PATCH | `/api/sql/updates/:id/estado` | Activa o desactiva un script publicado | `x-api-key` |
| * | `/api/notificaciones/*` | Recepción de eventos de salud e incidencias del ecosistema | `x-api-key` |
| * | `/api/clientes/*` | Validación y búsqueda de RUC/Cédula | `x-api-key` |
| * | `/api/sri/*` | Configuración de firmas electrónicas y SRI | `x-api-key` |

**Header de autenticación para endpoints protegidos:** `x-api-key: {key}` (tabla `webControl.api_key`)

**Módulos disponibles:**

| Módulo | Prefijo de ruta | Estado |
|--------|----------------|--------|
| Autenticación y Onboarding | `/api/auth` | ✅ Operativo |
| Apps satélite e infraestructura | `/api/apps`, `/api/apps_servcs` | ✅ Operativo |
| Versiones de Apps (CLI Sync) | `/api/apps/versiones` | ✅ Operativo |
| Scripts SQL delta | `/api/sql` | ✅ Operativo |
| Documentos Electrónicos y SRI | `/api`, `/api/sri` | ✅ Operativo |
| Directorio Centralizado de Clientes | `/api/clientes` | ✅ Operativo |
| Monitoreo, Alertas y Proyectos | `/api/notificaciones`, `/api/proyectos` | ✅ Operativo |

**Integración con el ecosistema:**
- **factura-e**: usa `webControl.usuarios_sesion` directamente para auth — login por `usrSesion_email` + bcrypt/plain-text
- **sigmac_app** / **sigmac-web**: registro y login vía `/api/auth/*`. Usuarios nuevos quedan con `usrSesion_panel = 'configuracion'`
- **API-SIGMA-CLOUD**: valida `x-api-key` contra `webControl.api_key` (`.149`) en cada petición entrante
- **mail-monitor**: notifica eventos de seguridad (bans fail2ban, cambios de cuenta) vía `x-api-key`
- Para más información técnica del proyecto: consultar localmente en `siax-amd:/home/pablinux/Projects/Node/API-SIGMA-WEBCONTROL/agents.md`

---

### API-SIGMA-CLOUD — API Gateway Multi-tenant

| Parámetro | Valor |
|-----------|-------|
| Repositorio Git | `https://github.com/telcotronics/api-gateway-cloud.git` (Gitea: `https://git.telcotronics.net/pablinux/API-GATEWAY-CLOUD.git`) |
| Tecnología principal | Node.js (Express) con conmutador de pools dinámicos (`mysql2/promise`) |
| Responsable | pablinux |
| Estado actual | ✅ Producción — `server-webapps` CT 132 (`192.168.10.160`) |
| Equipo / ubicación local | `siax-amd` (`192.168.10.100`) — `/home/pablinux/Projects/Node/API-SIGMA-CLOUD` |
| Puerto interno | `3003` |
| URL interna | `http://192.168.10.160:3003` |
| Dominio público | `api-gateway-cloud.telcotronics.net` / `api-gateway-sigma.telcotronics.net` |
| Servicio systemd | `api-gateway.service` |
| Documentación API | `https://api-gateway-cloud.telcotronics.net/api-docs` (Swagger UI) |
| Rol en el ecosistema | API Gateway multi-tenant cloud y motor transaccional comercial diario de todos los tenants |
| Última actualización | 2026-06-07 |

`API-SIGMA-CLOUD` es el proxy y enrutador comercial del ecosistema. Se conecta directamente con las aplicaciones de campo finales (Webswing, `sigmac_app` Flutter, `sigma_app` Android) para procesar el volumen operativo diario de cada tenant. Actúa como puente dinámico entre las apps y las bases de datos individuales de los clientes. **API REST pura** — sin vistas ni templates (código legacy eliminado 2026-06-07).

*   **Enrutamiento Dinámico Multi-tenant**: Middleware `dbConnection.js` enruta cada petición a la BD exacta del cliente (`?db=` o `x-database`). Nombres reservados van a pools fijos; cualquier otro nombre usa `getTenantPool(dbName)` — pool cacheado apuntando a `.115` con esa BD. Sin restricción de patrón de nombre.
*   **Autenticación en Dos Capas**: API Key (`x-api-key`) validada contra `webControl.api_key` en `.149`, y JWT Bearer (8 h) para sesiones de usuarios dentro del tenant.
*   **Transaccionalidad Comercial**: Inserción de pedidos, proformas e items bajo `BEGIN TRANSACTION / COMMIT / ROLLBACK` — sin corrupción de registros contables.
*   **Sincronización Delta Offline**: Endpoints masivos con filtro `?desde=` y paginación `?limite=`/`?offset=`. El sync masivo excluye imágenes — se recuperan puntualmente en Base64 con `/api/items/get-items/:item`.

**BDs que usa:**

| BD | Host | Motor | Uso |
|----|------|-------|-----|
| `webControl` | `192.168.10.149` | MariaDB 10.11 | Tabla `api_key` — validación de API Keys en cada petición entrante |
| `EMPRESA_XXX` (dinámica, `dbConnection`) | `192.168.10.115` | MySQL 8.0 | BD operativa del tenant enrutado por `?db=` — lógica de negocio diaria |
| `EMPRESA_XXX` (dinámica, `poolTenants`) | `192.168.10.115` | MySQL 8.0 | Pool dedicado sin DB fija para `/api/reportes` — queries con prefijo schema `` `EMPRESA_XXX`.tabla `` |
| `TELCOTRONICS` | `192.168.10.116` | MySQL 8.0 | Pool por defecto — datos propios Telcotronics |
| `SIGMA` | `192.168.10.116` | MySQL 8.0 | Pool histórico — consultas legacy |
| `sigma_tv` | `192.168.10.149` | MariaDB 10.11 | Pool canales Sigma TV |

**Headers de autenticación e integración:**

| Header / Param | Requerido | Descripción |
|----------------|-----------|-------------|
| `x-api-key` | ✅ Siempre | API Key del ecosistema — validada contra `webControl.api_key` en `.149` |
| `x-database` o `?db=` | ✅ En endpoints tenant | Nombre de la BD del cliente (ej: `EMPRESA_EL_SOL`) |
| `Authorization: Bearer {jwt}` | En endpoints de usuario | JWT emitido por `/api/auth/login-socio` (validez 8 h) |

**Módulos disponibles:**

| Módulo | Prefijo de ruta | Estado |
|--------|----------------|--------|
| Autenticación dual (admins bcrypt + socios MD5 legacy) | `/api/auth` | ✅ Operativo |
| Catálogo e Inventario — CRUD completo (GET individual, POST transaccional, PUT, DELETE transaccional, sync delta) | `/api/items` | ✅ Operativo |
| Utilidades y Precios (cálculo PVP offline, márgenes por grupo/item/volumen/costo) | `/api/items/utilidad`, `/api/items/precios` | ✅ Operativo |
| Clientes y Miembros — CRUD multi-tenant (`poolTenants` + `resolveDb`) | `/api/clientes` | ✅ Operativo |
| Documentos transaccionales (Pedidos y Proformas) | `/api/documentos` | ✅ Operativo |
| Contabilidad y Plan de Cuentas (sync offline Android) | `/api/contabilidad` | ✅ Operativo |
| Panel (Cajas activas, Pagos, Comprobantes) | `/api/panel` | ✅ Operativo |
| Localización (Áreas físicas) | `/api/localizacion` | ✅ Operativo |
| Reportes y Dashboard (10 endpoints analíticos para `sigmac_app`) | `/api/reportes` | ✅ Operativo |
| Usuarios del sistema — CRUD por tenant (facturador, vendedor, etc.) | `/api/panel/usuarios` | ✅ Operativo |

**Integración con el ecosistema:**
- **API-SIGMA-WEBCONTROL**: fuente de validación de `x-api-key` — toda petición entrante consulta `webControl.api_key` en `.149`
- **DB-EMPRESAS (.115)**: destino dinámico de todas las operaciones comerciales de tenants vía `dbConnection.js`
- **sigmac_app / sigmac-web**: consumidor principal — sync offline, pedidos, proformas, clientes e items
- **Webswing (.110)**: cliente desktop de operaciones comerciales diarias
- Para más información técnica del proyecto: consultar localmente en `siax-amd:/home/pablinux/Projects/Node/API-SIGMA-CLOUD/agents.md`

---

---

## Aplicaciones web

### CT cloud — Servidor-web (192.168.10.109)

| Parámetro | Valor |
|-----------|-------|
| IP | 192.168.10.109 |
| MAC | BC:24:11:68:9D:74 |
| CT Proxmox | 150 (nodo cloud) |
| Motor | Apache 2.4.66 + PHP **8.5**-FPM |
| Rol | Proxy reverso público + host de sitios PHP |

> **Convención de directorios:** `/var/www/web_[nombre]/`

| Directorio | Dominio | Notas |
|-----------|---------|-------|
| `web_factura-e` | `factura-e.net` / `app.factura-e.net` | ← **FACTURA-E** (ERP Facturador SIGMA) |
| `web_sigmac-crm` | `crm.sigmac.app` | sigmac-web (Laravel 13 + Vue 3) |
| `web_sigmac_app` | `sigmac.app` | Web de la marca SIGMAC |
| `web_telcotronics` | `telcotronics.com` | Web corporativa Telcotronics |
| `web_domus-fa` | `domus-fa.com` | Sistema domótica DAPSI |
| `web_acerogas` | — | Cliente Acerogas |
| `web_artesymas` | — | Cliente Artes y Más |
| `web_fact_pro` | — | Facturador Pro |
| `web_gimnasio` | — | Cliente Gimnasio |
| `web_helpdesk` | — | Help Desk |
| `web_tiendaPadi` | — | Cliente Tienda Padi |
| `web_xsystem` | — | XSystem |
| `web_zonaindustrial` | — | Cliente Zona Industrial |
| `web_test_facturador` | — | Entorno de pruebas |

**Proxies internos (Apache → backend):**

| Dominio | Destino |
|---------|---------|
| `api.factura-e.net` | http://192.168.10.120:8080/ |
| `app.factura-e.net` | http://*:3001/ |
| `api.sigmac.app` | http://192.168.10.120:8082/ |

---

### CT cloud — Servidor-SIGMA-VW (192.168.10.110)

| Parámetro | Valor |
|-----------|-------|
| IP | 192.168.10.110 |
| MAC | BC:24:11:DC:3B:6E |
| CT Proxmox | 141 (nodo cloud) |
| Rol | Frontend del sistema SIGMA |
| Tecnología | **Webswing 20.2.5** |
| Stack | Java 11 (build) / Java 8 o 11 (runtime), Jetty 9.4, Jersey 2.31, Google Guice 4.1, Protocol Buffers 3.12, TypeScript 5.5, Webpack 5.93 |

**¿Qué es Webswing?** Permite ejecutar aplicaciones Java Swing en el navegador usando HTML5, sin modificar el código fuente. Intercepta el sistema gráfico de Java (AWT Toolkit) y convierte las operaciones gráficas en comandos enviados vía WebSocket al navegador, que los renderiza en un Canvas HTML5.

```
Navegador (HTML5 Canvas)
    │ WebSocket (Protobuf)
Webswing Server (Jetty + Jersey + Guice)
    │ WebSocket (Protobuf)
JVM Swing Process (WebToolkit interceptado)
    │
Aplicación SIGMA (Java Swing — sin modificar)
```

**Compilar Webswing:**
```bash
mvn clean install              # Build completo
mvn clean install -Pdev        # Desarrollo (sin tests)
mvn clean install -Prelease    # Producción con javadoc
```

---

### WebControlSigma (Web_siax-sytem) — Panel Administrativo del Ecosistema

Panel web central de administración del ecosistema Telcotronics. Gestiona empresas clientes, usuarios cloud (`usuarios_sesion` / `usuarios_xValidar`), API Keys de los 3 sistemas (webControl, sigma-robot, api-IA), licencias de hosts (SHA256 determinista), notificaciones, proyectos y catálogo de apps descargables. Incluye módulo BFF PHP hacia `SIGMAC-SRI-API` para facturación electrónica. Login con bcrypt + captcha. Desplegado en Apache 2.4 + PHP 8.5-FPM en Servidor-web (.109).

| Parámetro | Valor |
|-----------|-------|
| Repositorio Git | `https://git.telcotronics.net/pablinux/Web_siax-sytem.git` |
| Tecnología principal | PHP 8.5 + MariaDB (PDO) |
| Responsable | pablinux |
| Estado actual | ✅ Activo — tabs Android/iOS + CLI Sync + endpoint upload_app 2026-06-16 |
| Equipo / código local | `siax-amd` (`192.168.10.100`) — `/home/pablinux/Projects/php/Web_siax-sytem` |
| Servidor de producción | Servidor-web CT 150 (`192.168.10.109`) |
| Directorio deploy | `/var/www/web_xsystem/public_html` |
| Dominio público | `siax-system.net` |
| Puerto | 80 / 443 (Apache) |
| Última actualización | 2026-06-16 |

**BDs que usa:**

| BD | Host | Motor | Uso |
|----|------|-------|-----|
| `webControl` | `192.168.10.149` | MariaDB 10.11 | BD principal — `ClienteEmpresa`, `HostEmpresa`, `usuarios_sesion`, `usuarios_xValidar`, `panel_control_users`, `api_key`, `notificaciones` |
| `siax_core` | `192.168.10.149` | MariaDB 10.11 | Lectura/escritura API keys de sigma-robot (`api_keys`) |
| `api_ia_python` | `192.168.10.149` | MariaDB 10.11 | Lectura/escritura API keys de api_service_ia (`api_key`) |

**Servicios que consume:**

| Servicio | URL | Autenticación | Propósito |
|---------|-----|---------------|-----------|
| SIGMAC-SRI-API | `https://api.sigmac.app/sri` | OAuth2 Password Grant | Panel BFF facturación SRI — `app/facturacion/` |
| SMTP ecosistema | `smtp.sigmac.app:587` | `no-reply@sigmac.app` | Envío de correos vía PHPMailer |
| API_CENTINEL_SECURITY | `https://api.telcotronics.com` | `x-api-key` | Control de acceso Hikvision — gestión de dispositivos, apertura de puertas, consulta de eventos de acceso físico |

**Módulos disponibles:**

| Módulo | Ruta | Estado |
|--------|------|--------|
| Login + captcha | `index.php` + `login.php` | ✅ Operativo (bcrypt + PHP 8.5) — rediseño pendiente |
| Panel principal + Dashboard métricas | `PanelMenu.php` | ✅ Operativo — 7 stat cards + 2 tablas detalle + cards Android/iOS/CLI Sync en sec-apps (contadores GROUP BY) |
| Hub Clientes (4 tabs: empresas / equipos / sesiones cloud / xValidar) | `app/clientes/sesiones.php` | ✅ Operativo 2026-06-03 |
| API Keys (webControl + sigma-robot + api-IA) | `app/clientes/apikeys.php` | ✅ Operativo — ver/copiar key_value, badge vencida, extender expiración |
| Equipos / Licencias hosts SHA256 | `sesiones.php?tab=equipos` | ✅ Operativo — `licencias.php` redirige aquí |
| Notificaciones por cliente | `app/clientes/notificaciones.php` | ✅ Operativo |
| Panel Facturación SRI (BFF) | `app/facturacion/` | ✅ Operativo |
| Usuarios del panel | `app/usuarios/` | ✅ Operativo |
| Hub Software (10 tabs: linux/windows/mac/android/ios/bd/reportes/herramientas + cloud + cli-sync) | `app/software/` | ✅ Operativo — Android, iOS, CLI Sync agregados 2026-06-16 |
| Webhook sync apps | `POST /api/sync_app.php` | ✅ Operativo — `x-api-key`, INSERT/UPDATE `aplicaciones` |
| Endpoint reportes SIGMAC Java | `GET /api/reportes.php` | ✅ Operativo — catálogo JSON + descarga por `?id=N` |
| Reportes de audio | `app/rep_audio/` | 🔧 En desarrollo |
| Webhooks / chatbot | `webhooks/domus/` | ⚠️ Legacy |

**Algoritmo de licencias:** `hash('sha256', strtoupper($hostname).'|'.strtoupper($empresa).'|'.SIGMA_LIC_SALT)` — resultado (64 hex) en `HostEmpresa.HostEmp_idLic`. Determinista: mismo host+empresa = mismo código siempre.

**BDs de software (en `webControl` — `.149`):**

| Tabla | Uso | Campo clave |
|-------|-----|-------------|
| `aplicaciones` | Catálogo de apps descargables (Linux/Windows/Mac/Android/iOS/BD/Herramientas) | `app_ENLACE` — URL de descarga actual |
| `aplicaciones_versiones` | Historial de versiones por app. FK `app_id→aplicaciones.app_ID`. UNIQUE `(app_id,version)`. Campos: `version`, `changelog`, `fecha_release`, `url_descarga`, `archivo_md5`, `estado` ENUM(`activo`\|`inactivo`\|`beta`) | `url_descarga` + `archivo_md5` |
| `aplicaciones_reportes` | Plantillas de reportes por categoría (ventas, inventario, caja, CxC, CxP, compras, contabilidad) | `url_plantilla` — consumida por `GET /api/reportes.php?id=N` |
| `aplicaciones_img` | Iconos y miniaturas para `aplicaciones` y `aplicaciones_reportes` | `ref_tabla` + `ref_id` — FK polimórfica |

**Sistema de actualizaciones de apps — CLI Sync:**

> Mecanismo central del que dependen TODAS las apps cliente para recibir nuevas versiones.
> Aplica a apps descargables (instaladores, binarios, paquetes). No aplica a webapps ni servicios.

```
Developer/IA/Robot/CI
        ↓
POST /api/upload_app.php  (x-api-key)
        ↓
aplicaciones + aplicaciones_versiones  (BD webControl .149)
        ↓
POST https://api.siax-system.net/api/apps/versiones  (notifica API WebControl)
        ↓
App cliente consulta GET /api/apps/versiones/{app_nombre}/latest
        ↓
Descarga url_descarga → verifica archivo_md5 → instala
```

Subir nueva versión desde CLI:
```bash
curl -X POST 'https://siax-system.net/api/upload_app.php' \
  -H 'x-api-key: <key de webControl.api_key>' \
  -F 'nombre=SIGMA RC' \
  -F 'version=5.2.1' \
  -F 'plataforma=WINDOWS' \
  -F 'changelog=Corrección de errores' \
  -F 'fecha_release=2026-06-16' \
  -F 'archivo=@./sigma_setup.exe'
# → {"ok":true,"app_id":N,"db_action":"created|updated","url_descarga":"...","archivo_md5":"<md5>"}
```

Verificar última versión disponible (apps cliente):
```
GET https://api.siax-system.net/api/apps/versiones/{app_nombre}/latest
Header: x-api-key: <key>
→ version, url_descarga, archivo_md5, estado (solo actualizar si estado="activo")
```

Consultar en panel: `https://siax-system.net/app/software/index.php?tab=cli-sync`
API key: panel `siax-system.net` → Clientes → API Keys

**Endpoint de reportes para SIGMAC Java:**
```
GET https://siax-system.net/api/reportes.php          → catálogo JSON completo
GET https://siax-system.net/api/reportes.php?id=N     → descarga directa o redirect
GET https://siax-system.net/api/reportes.php?categoria=ventas → filtrado JSON
→ Sin autenticación — acceso público por URL
```

**Integración con el ecosistema:**
- Provee `webControl.api_key` — consumida por `API-SIGMA-CLOUD` y `API-SIGMA-WEBCONTROL` para validar `x-api-key`
- Gestiona `usuarios_sesion` y su vínculo con `ClienteEmpresa` (FK bidireccional `usrSesion_idEmp` ↔ `clientEmp_idUsuario`)
- Las apps Flutter/PHP/Java registran usuarios vía `API-SIGMA-WEBCONTROL` → `usuarios_xValidar` → OTP → `usuarios_sesion` — visibles y gestionables desde este panel
- **SIGMAC Java** consumirá `GET /api/reportes/{id}` para descargar plantillas de reportes directamente desde el panel

**Más información:** `siax-amd:/home/pablinux/Projects/php/Web_siax-sytem/agents.md`

---

### SitioWeb_telcotronics — Sitio web institucional y tienda en línea

Sitio web público de Telcotronics. SPA estática servida por Apache en Servidor-web (.109). Presenta los servicios, portafolio e historia de la empresa, genera leads vía formulario de contacto PHP+PHPMailer y expone una tienda en línea con **914 productos reales** del catálogo del ERP. Consume SMTP del ecosistema y API-SIGMA-CLOUD para el catálogo.

| Parámetro | Valor |
|-----------|-------|
| Repositorio Git | [pendiente — crear repo en git.telcotronics.net] |
| Tecnología principal | HTML5 / CSS3 / JS ES6+ vanilla · Tailwind CSS (CDN) · PHP 8.5 + PHPMailer |
| Responsable | pablinux |
| Estado actual | ✅ v2.3.1 |
| Código local | `pablinux-laptop` (`192.168.10.72`) — `/home/pablinux/Projects/php/SitioWeb_telcotronics` |
| Servidor de producción | Servidor-web CT 150 (`192.168.10.109`) — Apache 2.4.66 + PHP 8.5-FPM |
| Directorio deploy | `/var/www/web_telcotronics/public_html/` |
| Dominio público | `telcotronics.com` |
| Puerto | 80 / 443 (Apache) |
| Última actualización | 2026-06-03 |

**BDs que usa:** Ninguna propia — consume `TELCOTRONICS` en MySQL `.116` a través de API-SIGMA-CLOUD (nunca conexión directa).

**Servicios que consume:**

| Servicio | URL / Host | Autenticación | Propósito |
|---------|-----------|---------------|-----------|
| SMTP ecosistema | `smtp.sigmac.app:587` (interno: `192.168.10.111:587`) | `no-reply@sigmac.app` / `Sigma.2030@` | Formulario de contacto — lead al equipo + confirmación al remitente |
| API-SIGMA-CLOUD | `https://api-gateway-cloud.telcotronics.net` | `x-api-key: <sigma_api_key>` | Catálogo tienda — grupo de precios `VENTAS_WEB`, BD `TELCOTRONICS` |

**Configuración de API-SIGMA-CLOUD en el servidor** (`api/config.php`, nunca en git):

```php
'sigma_api_key' => '706847ea7fbe9caf9c5d4d26b41391a3cfe5eec8bd4404cc4e7f857d2e950acf',
'sigma_db'      => 'TELCOTRONICS',
```

- `sigma_api_key` — se valida contra `webControl.api_key` en MariaDB `.149`. Gestionar desde **WebControlSigma** (`siax-system.net` → panel "API Keys").
- `sigma_db` — base de datos del catálogo en MySQL `.116`. No cambiar salvo migración de BD.

**Cómo verificar que la key funciona:**
```bash
curl -s "https://api-gateway-cloud.telcotronics.net/api/items/listar_grupo_precio?db=TELCOTRONICS" \
  -H "x-api-key: 706847ea7fbe9caf9c5d4d26b41391a3cfe5eec8bd4404cc4e7f857d2e950acf"
# Respuesta esperada: [...,{"nombre":"VENTAS_WEB",...}]
```

**Cómo renovar la key:** WebControlSigma → "API Keys" → nueva key → editar `api/config.php` en servidor → `rm /tmp/telco_catalogo_*.json`.

**Forzar recarga del catálogo** (sin cambiar la key, refleja productos nuevos del ERP):
```bash
ssh pablinux@192.168.10.109 "rm /tmp/telco_catalogo_*.json"
```

**Agregar productos a la tienda:** desde SIGMAC → Inventario → Producto → Precios → añadir grupo `VENTAS_WEB`.

**Módulos disponibles:**

| Módulo | Archivo | Estado |
|--------|---------|--------|
| Sitio institucional (SPA) | `index.html` | ✅ v2.1.0 — completo |
| Tienda en línea | `tienda.html` | ✅ v2.0 — 914 productos reales, categorías dinámicas, búsqueda, filtros |
| Catálogo proxy | `api/productos.php` | ✅ → API-SIGMA-CLOUD `VENTAS_WEB`, caché 1h en `/tmp` |
| Formulario de contacto | `api/contacto.php` | ✅ PHP + PHPMailer + honeypot — pendiente activar SMTP en servidor |

**Integración con el ecosistema:**
- Consume **API-SIGMA-CLOUD** para catálogo de productos (grupo `VENTAS_WEB`, BD `TELCOTRONICS`)
- Consume **SMTP ecosistema** (`smtp.sigmac.app`) para formulario de contacto
- Chatbot **Dialogflow** embebido (agent ID `eea5ca65-ded3-4c89-bd8a-9e6378cb4686`) — independiente del hosting

**Más información:** `pablinux-laptop:/home/pablinux/Projects/php/SitioWeb_telcotronics/agents.md`

---

### sigmac-web — CRM Web del Ecosistema SIGMA

CRM web companion a `sigmac_app`. SPA Vue 3 servida por un backend Laravel 13 que actúa como proxy puro hacia los servicios del ecosistema — no tiene lógica de negocio propia. La autenticación pasa íntegramente por API-SIGMA-WEBCONTROL y los datos de negocio provienen de MySQL tenant en DB-EMPRESAS. La API Laravel valida el JWT de WEBCONTROL con `AuthJwtMiddleware` y enruta dinámicamente al tenant correcto con `TenantMiddleware` en cada petición.

| Parámetro | Valor |
|-----------|-------|
| Repositorio Git | `https://git.telcotronics.net/pablinux/SIGMAC-WEB_PHP.git` |
| Tecnología principal | Laravel 13 (PHP 8.5) + Vue 3 + Vite 5.4 + Tailwind CSS 3.4 |
| Responsable | pablinux |
| Estado actual | 🟡 En desarrollo activo — módulos principales completos, pendiente Notificaciones/Sincronización/HTTPS |
| Equipo / código local | `pablinux-laptop` (`192.168.10.72`) — `/home/pablinux/Projects/php/sigmac-web` |
| Servidor de producción | Servidor-web CT 150 (`192.168.10.109`) — Apache 2.4.66 + PHP 8.5-FPM |
| Directorio deploy | `/var/www/web_sigmac-crm/` |
| Dominio público | `crm.sigmac.app` |
| Puerto | 80 / 443 (Apache prod) · `:8000` API dev · `:5173` frontend dev |
| Última actualización | 2026-06-09 |

**BDs que usa:**

| BD | Host | Motor | Uso |
|----|------|-------|-----|
| `EMPRESA_XXX` (dinámica) | `192.168.10.115` | MySQL 8.0 | BD operativa del tenant — toda la lógica de negocio. Enrutada por `TenantMiddleware` según `db_tenant` del JWT |

**Servicios que consume:**

| Servicio | URL | Auth | Propósito |
|---------|-----|------|-----------|
| API-SIGMA-WEBCONTROL | `https://api.siax-system.net` (interno: `http://192.168.10.145:3002`) | Pública | Auth 2 pasos: `POST /api/auth/empresas` + `POST /api/auth/login` → JWT (8h) + apiKey + db_tenant |
| API-SIGMA-CLOUD | `https://api-gateway-cloud.telcotronics.net` | `x-api-key` + `?db=` | Sincronización cloud — pendiente implementar |

**Flujo de autenticación (para integración):**
1. `POST /api/auth/empresas {email, paswd}` → Laravel proxea a WEBCONTROL → lista de empresas del usuario
2. `POST /api/auth/login {email, paswd, dba}` → Laravel proxea → JWT + apiKey + db_tenant (dba opcional en multi-empresa)
3. Cada request protegida: `Authorization: Bearer {jwt}` → `AuthJwtMiddleware` valida → `TenantMiddleware` conecta a `EMPRESA_XXX` en `.115`

**Módulos disponibles (API REST en `crm.sigmac.app/api/`):**

| Módulo | Endpoints principales | Estado |
|--------|-----------------------|--------|
| Auth | `POST /auth/empresas`, `POST /auth/login`, `GET /auth/me` | ✅ Operativo |
| Dashboard | `GET /dashboard/kpis`, `/grafica`, `/top-productos`, `/actividad` | ✅ Operativo |
| Ventas | `GET/POST /ventas`, `GET /ventas/{id}`, `POST /ventas/{id}/anular`, `GET /ventas/kpis` | ✅ Operativo |
| Compras | `GET/POST /compras`, `GET /compras/{id}`, `GET /compras/kpis` | ✅ Operativo |
| Pedidos | `GET/POST /pedidos`, `GET /pedidos/{id}`, `POST /pedidos/{id}/confirmar`, `/cancelar` | ✅ Operativo |
| Proformas | `GET/POST /proformas`, `GET /proformas/{id}`, `POST /proformas/{id}/emitir`, `/anular` | ✅ Operativo |
| Inventario | `GET/POST/PUT /inventario`, `GET /inventario/{id}`, `POST /inventario/{id}/ajustar-stock`, `GET /inventario/kpis` | ✅ Operativo |
| Clientes | `GET/POST/PUT /clientes`, `GET /clientes/{id}`, `GET /clientes/{id}/consultar-sri`, `GET /clientes/kpis` | ✅ Operativo |
| Tareas | `GET/POST/PUT/DELETE /tareas`, `POST /tareas/{id}/cambiar-estado` | ✅ Operativo |
| Notificaciones | — | 🔧 Pendiente |
| Sincronización cloud | — | 🔧 Pendiente |

**Integración con el ecosistema:**
- Proxea auth hacia **API-SIGMA-WEBCONTROL** (`192.168.10.145:3002`) — no gestiona identidades propias
- Accede a **DB-EMPRESAS** (`.115`) directamente vía `TenantMiddleware` + Eloquent (`BaseModel $connection='tenant'`)
- Paralelo a **sigmac_app** (Flutter) — misma lógica de negocio orientada al navegador, sin modo offline
- El frontend SPA se sirve desde `crm.sigmac.app/app/` (build Vite compilado en `api/public/app/`)

**Más información:** `pablinux-laptop:/home/pablinux/Projects/php/sigmac-web/agents.md`

---

### app_ideas — Canvas de Ideas y Pensamiento Visual

| Parámetro | Valor |
|-----------|-------|
| Repositorio Git | `https://git.telcotronics.net/pablinux/APPA-GENERQADOR-DE-IDEAS.git` |
| Tecnología principal | Node.js (Express) + MongoDB + EJS |
| Responsable | pablinux |
| Estado actual | 🟡 En desarrollo activo |
| Puerto | `2000` |
| Servicio systemd | `siax-app-APP_IDEAS` (gestionado por SIAX Monitor) |
| BD principal | MongoDB — `192.168.10.146:27017/app_ideas` (CT 102, nodo cluster) |
| Servidor deploy | `server-webapps` CT 132 (`192.168.10.160`) |
| Dominio público | `ideas.telcotronics.com` |

Canvas de ideas y pensamiento visual del ecosistema. Permite generar, organizar y visualizar ideas con soporte de inteligencia artificial. Cuenta con paneles especializados: dibujo libre, flujo visual, gestión de ideas, generación asistida por IA y recopilación de procesos.

**APIs que consume:**

| Servicio | URL / Variable | Uso |
|---------|---------------|-----|
| MongoDB | `MONGO_URI=mongodb://192.168.10.146:27017/app_ideas` | BD principal — ideas, flujos, sesiones |
| AIT (IA Telcotronics) | `AIT_URL=https://api.telcotronics.net/` | Generación y análisis de ideas con IA |
| Hub API (Tareas) | `HUB_API_URL=https://tareas.telcotronics.com/api/external` | Integración con sistema de tareas |
| Resend | `ReSend_APIKEY` | Envío de emails |

---

### app_marketing — Centro de Publicidad y Marketing del Ecosistema

**Descripción:**
Centro de publicidad y marketing multi-tenant del ecosistema Telcotronics. Gestiona y sirve campañas promocionales internas y de anunciantes para las aplicaciones del ecosistema (`app_ideas`, `sigmac_app`, `sigmac-web`, etc.) mediante una API REST y un widget JS embebible responsivo. Registra impresiones y clics para proporcionar métricas en tiempo real.

| Parámetro | Valor |
|-----------|-------|
| Repositorio Git | [pendiente — crear repo en git.telcotronics.net] |
| Tecnología principal | Node.js (Express) + MongoDB + EJS |
| Responsable | pablinux |
| Estado actual | ✅ Activo / Producción |
| Ubicación local | `siax-intel` (`192.168.10.101`) — `/home/pablinux/Projects/Node/app_marketing` |
| Servidor de producción | `server-webapps` CT 132 (`192.168.10.160`) — `/home/user_apps/apps/app_marketing` |
| Dominio público | `marketing.sigmac.app` (Portal Admin) y `ads.sigmac.app` (API/Widget) |
| Puerto | `2100` |
| Servicio systemd | `siax-app-APP_MARKETING` (gestionado por SIAX Monitor) |
| Última actualización | 2026-05-31 |

**Bases de Datos:**
* **MongoDB** (`192.168.10.146:27017/app_marketing` en CT 102, nodo cluster): Almacena las cuentas de usuarios, planes de suscripción con límites, campañas creadas (títulos, descripciones, llamadas a la acción, colores, recursos multimedia) y eventos de impresiones y clics para análisis histórico.

**Servicios que Consume y Expone:**
* **Expone:**
  * **Widget JS:** `http://ads.sigmac.app/js/widget.js` (embebible en cualquier web del ecosistema).
  * **GET** `http://ads.sigmac.app/api/banner?apiKey=sg_live_...&formato={formato}`: Devuelve el anuncio activo para la aplicación autorizada y registra la impresión automáticamente.
  * **POST** `http://ads.sigmac.app/api/clic`: Registra un clic en el banner. Payload: `{ campanaId, apiKey }`.
* **Autenticación:**
  * Acceso público y seguro al widget vía cabecera `x-api-key` o parámetro de consulta `apiKey`.
  * Acceso a paneles administrativos mediante sesiones HTTP seguras (`express-session` con almacenamiento en MongoDB).

**Módulos Disponibles:**
* **Portal Super Admin (`/admin/super`):** Monitoreo de recursos del servidor en tiempo real, gestión de anunciantes y planes de suscripción. (✅ Operativo)
* **Portal Anunciante (`/admin`):** Métricas propias y CRUD de campañas publicitarias (imágenes, videos, HTML personalizado) limitadas por su plan. (✅ Operativo)
* **Widget Engine:** Inyección responsiva y adaptativa para 5 formatos de anuncios: `banner` (estándar), `sidebar` (columna), `footer` (pie), `intro_demo` (modal) y `slider` (deslizante esquina inferior). (✅ Operativo)

**Integración con el Ecosistema:**
* Las aplicaciones satélites autorizadas (ej. `app_ideas`, `sigmac-web`, `sigma-robot`, `sigmac_app`) integran el contenedor HTML:
  ```html
  <div id="sigma-banner" data-api-key="sg_live_XXXX" data-formato="banner"></div>
  <script src="http://ads.sigmac.app/js/widget.js"></script>
  ```
  y consumen anuncios segmentados utilizando su API Key correspondiente.

**Dónde buscar más información:**
* Documentación local detallada del proyecto: `siax-intel:/home/pablinux/Projects/Node/app_marketing/README.md`.

---

### app_fidelizacion — Aplicación de Fidelización de Clientes

| Parámetro | Valor |
|-----------|-------|
| Repositorio Git | [pendiente — crear repo en git.telcotronics.net] |
| Tecnología principal | Node.js (Express) + MySQL + EJS + Tailwind CSS |
| Responsable | pablinux |
| Estado actual | 🟡 En desarrollo activo |
| Puerto | `2001` |
| Servicio systemd | `siax-app-APP_FIDELIZACION.service` |
| BD principal | MySQL — `192.168.10.149:3306/nexo_fd` |
| Servidor deploy | `server-webapps` CT 132 (`192.168.10.160`) |

Plataforma de lealtad desarrollada para gestionar clientes y acumulación de puntos (transacciones) vía escaneo QR por parte de comercios (Partners). Incluye un módulo público, panel de cliente (tienda de canje, perfil), panel de partner y un panel administrativo. Integra una API REST para interacción externa (Partners).

**APIs que consume/provee:**

| Servicio | URL / Endpoint | Uso |
|---------|---------------|-----|
| MySQL | `DB_HOST=192.168.10.149` | Base de datos principal de usuarios, catálogo e historial de transacciones |
| API Partners | `/api/v1/partner/*` | Endpoints protegidos vía `x-api-key` para registro de clientes, transacciones y catálogo |

---

### sistema-gimnasio — Sistema de Administración para Gimnasio (SOCIOS)

Panel web de administración de gimnasios en el ecosistema SIGMA (frente 3 — Panel Admin SOCIOS). Staff del gimnasio gestiona miembros, membresías, pagos, visitas, cajas, inventario de items y ventas. SPA Vue 2 + Vuetify 2 con tema oscuro. Consume dos APIs del ecosistema: `API-SIGMA-WEBCONTROL` para autenticación y `API-SIGMA-CLOUD` para todos los datos de negocio.

| Parámetro | Valor |
|-----------|-------|
| Repositorio Git | `https://github.com/telcotronics/sistema-gimnasio.git` |
| Tecnología principal | Vue.js 2.5 + Vuetify 2.7 (Options API) + Webpack 3 |
| Responsable | pablinux |
| Estado actual | 🚧 En desarrollo activo — migración a API-SIGMA-CLOUD en curso (~98% completado) |
| Equipo / código local | `siax-amd` (`192.168.10.100`) — `/home/pablinux/Projects/Node/sistema-gimnasio` |
| Servidor de producción | `Servidor-web` CT 150 (`192.168.10.109`) |
| Directorio deploy | `/var/www/web_gimnasio/public_html/` |
| Dominio público | `[pendiente]` |
| Puerto | 8080 (dev) / 80-443 (prod vía Apache) |
| Última actualización | 2026-06-08 |


**BDs que usa:**

No interactúa con BD directamente. Enruta al tenant del gimnasio vía `?db=[nombre_bd]` en cada request a `API-SIGMA-CLOUD`.

**Servicios que consume:**

| Servicio | URL | Autenticación | Propósito |
|---------|-----|---------------|-----------|
| API-SIGMA-WEBCONTROL | `https://api.siax-system.net` | Pública | Auth: `POST /api/auth/empresas` (pre-login) + `POST /api/auth/login` → devuelve JWT + apiKey |
| API-SIGMA-CLOUD | `https://api-gateway-cloud.telcotronics.net` | `x-api-key` + `Bearer JWT` + `?db=` | Todos los datos de negocio — miembros, membresías, pagos, cajas, clientes, items, ventas |
| WebSocket ChatBot | `ws://[host]/chat` | Ninguna | Módulo de chat interno |
| API_CENTINEL_SECURITY | `https://api.telcotronics.com` | `x-api-key` | Control de acceso Hikvision — CRUD usuarios en dispositivo, apertura remota de puertas |

**Flujo de autenticación:**
1. `POST api.siax-system.net/api/auth/empresas` `{email, paswd}` → lista de empresas del usuario
2. Si una empresa: login directo. Si varias: usuario selecciona.
3. `POST api.siax-system.net/api/auth/login` `{email, paswd, dba}` → `{token, apiKey, db_tenant, usuario}`
4. Requests posteriores a API-SIGMA-CLOUD llevan: `x-api-key`, `Authorization: Bearer {token}`, `?db={db_tenant}`

**Módulos disponibles:**

| Módulo | Ruta | Estado |
|--------|------|--------|
| Autenticación / Sesión | `/login` | ✅ Operativo — login vía WebControl (`api.siax-system.net`) |
| Miembros | `/crud_miembros_card` | ✅ Migrado — `api/clientes/miembros` |
| Membresías / Planes | `/crud_membresia_card` | ✅ Migrado — `api/clientes/tipos-membresia` (CRUD completo) |
| Clientes | `/clientes` | ✅ Migrado — `api/clientes/verClientesJsonApp` + `consulta_clientesApps` |
| Dashboard | `/` | 🚧 Datos hardcodeados — sin conectar a API |
| Pagos | `/pagos` | ✅ Migrado — `api/panel/pagos/transacciones` (lista + registro) |
| Visitas | `/visitas` | ✅ Migrado — `api/visitas` (lista + registro miembro/ocasional + áreas) |
| Cajas | `/caja_apertura` | ⚠️ Pendiente — endpoints SOL-04/05 pendientes en backend |
| Usuarios | `/usuarios` | ✅ Migrado — `api/panel/usuarios` (CRUD completo, baja lógica) |
| Ventas | `/venta` | 🚧 UI lista — `handleSave` sin implementar |
| Inventario | `/inventario` | 🚧 UI lista — sin backend |
| CXC / Abonos | `/cxc`, `/abonos` | ❌ Placeholders — sin implementar |
| Config. Áreas | `/admin-areas` | ✅ Migrado — `api/localizacion/areas` (CRUD + inactivar) |
| Config. Empresa | `/configurar` | ✅ Migrado — `api/empresa/datos` GET/PUT. RUC solo lectura. |
| Chat | `/chat` | ⚠️ WebSocket funcional — envío con URL PHP hardcodeada |
| Control de Acceso | `/sincronizar` | 🚧 UI lista — conectar a `API_CENTINEL_SECURITY` (`api.telcotronics.com/api/devices/{id}/users`) |

**Integración con el ecosistema:**
- Auth vía `API-SIGMA-WEBCONTROL` (`api.siax-system.net`) — el apiKey devuelto en login es válido para API-SIGMA-CLOUD.
- Datos vía `API-SIGMA-CLOUD` — multi-tenant por `?db=` y validación de `x-api-key` contra `webControl.api_key` (.149).
- El `/login` en `api-gateway-cloud.telcotronics.net/api/auth` es LEGACY (viene del monolito `app.factura-e.net`) — no usar.

**Más información:** `siax-amd:/home/pablinux/Projects/Node/sistema-gimnasio/agents.md`

---

### audio_control — Panel de Control Remoto de Audio (SoundWave)

Backend de la app **SoundWave**. Permite controlar la reproducción de audio de `siax-amd` de forma remota desde el navegador: reproduce archivos MP3 locales con `ffplay`, descarga audio de YouTube, gestiona una playlist en MySQL y autentica usuarios con Google OAuth 2.0 + JWT. Actualmente corre solo en el equipo de desarrollo — sin servidor de producción dedicado aún.

| Parámetro | Valor |
|---|---|
| Repositorio Git | [pendiente — crear repo en git.telcotronics.net] |
| Tecnología principal | Node.js (Express) + MySQL + EJS + Socket.IO |
| Responsable | pablinux |
| Estado actual | 🟡 En desarrollo activo |
| Equipo / ubicación local | `siax-amd` (`192.168.10.100`) — `/home/pablinux/Projects/Node/audio_control` |
| Servidor de producción | Sin servidor dedicado aún — corre en `siax-amd` localmente |
| Dominio público | Sin dominio asignado aún |
| Puerto | `4000` |
| Servicio systemd | Pendiente |
| Última actualización | 2026-06-13 |

**BD que usa:**

| BD | Host | Motor | Uso |
|----|------|-------|-----|
| `AUDIO_CTRL` | `192.168.10.149` | MariaDB 10.11 | `users` (usuarios Google OAuth), `rep_youtube` (playlist YouTube) |

**Endpoints principales (para integración):**

| Método | Endpoint | Auth | Descripción |
|--------|----------|------|-------------|
| POST | `/control/audio/play` | — (pendiente JWT) | Reproduce archivo MP3 local con `ffplay`. Body: `{ file: "ruta/relativa" }` |
| POST | `/control/audio/stop` | — (pendiente JWT) | Detiene `ffplay` activo |
| POST | `/control/youtube/download` | — | Descarga audio de YouTube como MP3. Body: `{ url: "..." }` |
| GET | `/api/youtube-playlist` | — | Lista playlist YouTube (últimas 50 de MySQL) |
| POST | `/api/youtube-playlist/add` | — | Agrega video a playlist |
| GET | `/api/mp3-files` | — | Lista archivos MP3 en `public/files/mp3/` |
| POST | `/api/auth/google` | — | Auth Google OAuth 2.0 → JWT propio |
| GET | `/api-docs` | — | Swagger UI |

**Servicios que consume:**

| Servicio | Uso |
|---------|-----|
| `ffplay` (sistema — parte de `ffmpeg`) | Reproducción de audio local |
| YouTube (internet) vía `@distube/ytdl-core` | Descarga de audio |
| Google OAuth 2.0 API | Verificación de tokens de usuario |

**Integración con el ecosistema:**
- Independiente actualmente — no consume APIs internas del ecosistema
- Potencial: integrar con `sigma-robot` para notificaciones de estado vía WhatsApp

**Dónde buscar más información:** `siax-amd:/home/pablinux/Projects/Node/audio_control/agents.md`

---

### SoundWave — Reproductor de Música Personal PWA

Webapp PWA de streaming de música personal. El usuario se autentica con Google y accede a una biblioteca de música compartida alojada en el servidor. Funciona en cualquier dispositivo con navegador (teléfono, Android del carro, tablet, PC). Sin pendrive, sin anuncios, sin suscripción. Incluye su propio backend Express (puerto 2005) para autenticación JWT y servicio de archivos. La biblioteca de música vive en `server/cloud/` en el equipo de desarrollo.

| Parámetro | Valor |
|---|---|
| Repositorio Git | [pendiente — git.telcotronics.net] |
| Tecnología principal | Vue 3 + Vite 7 (PWA) / Node.js (Express) + MongoDB |
| Responsable | pablinux |
| Estado actual | 🟡 En desarrollo activo |
| Equipo / ubicación local | `siax-amd` (`192.168.10.100`) — `/home/pablinux/Projects/Node/audio-player` |
| Servidor de producción | Sin servidor dedicado aún — corre en `siax-amd` localmente |
| Dominio público | Sin dominio asignado aún (uso en LAN) |
| Puerto backend | `2005` |
| Puerto frontend (dev) | `5173` |
| Servicio systemd | Pendiente configurar |
| Última actualización | 2026-06-13 |

**BD que usa:**

| BD | Host | Motor | Uso |
|----|------|-------|-----|
| `soundwave` | `192.168.10.146:27017` | MongoDB (CT 102) | Usuarios registrados — name, email, picture, provider, providerId |

**Endpoints principales (para integración):**

| Método | Endpoint | Auth | Descripción |
|--------|----------|------|-------------|
| POST | `/api/auth/google` | no | Verifica Google ID token → upsert usuario MongoDB → devuelve JWT |
| POST | `/api/auth/facebook` | no | Verifica FB accessToken → upsert usuario MongoDB → devuelve JWT |
| GET | `/api/music/folders` | JWT | Árbol completo de carpetas y archivos de música |
| GET | `/api/music/search?q=` | JWT | Búsqueda recursiva por nombre |
| GET | `/api/music/stream/*ruta` | JWT (`?token=`) | Streaming de audio con Range requests (seek) |
| GET | `/api/music/download/*ruta` | JWT (`?token=`) | Descarga de archivo al dispositivo |
| POST | `/api/music/upload` | JWT | Sube archivo de música (multipart, límite 200 MB) |
| POST | `/api/music/folder` | JWT | Crea carpeta |
| PATCH | `/api/music/rename` | JWT | Renombra carpeta o archivo |

> **Nota:** El JWT se acepta en header `Authorization: Bearer {token}` Y en query param `?token=` — necesario para `<audio src>` que no puede enviar headers.

**Servicios que consume:**

| Servicio | URL | Uso |
|---------|-----|-----|
| Google OAuth API | `https://oauth2.googleapis.com` | Verificación de Google ID tokens vía `google-auth-library` |
| Facebook Graph API | `https://graph.facebook.com` | Verificación de access tokens de Facebook |
| MongoDB | `192.168.10.146:27017/soundwave` | Persistencia de usuarios |

**Módulos disponibles:**

| Módulo | Estado |
|--------|--------|
| Login Google OAuth | ✅ Completo |
| Backend auth con MongoDB | ✅ Completo |
| API de música completa | ✅ Completo |
| Reproductor con stream real + seek | ✅ Completo |
| Navegación por carpetas + breadcrumb | ✅ Completo |
| Búsqueda en tiempo real | ✅ Completo |
| Subir / descargar música | ✅ Completo |
| Crear / renombrar carpeta | ✅ Completo |
| PWA instalable + Service Worker offline | ✅ Completo |
| Login Facebook | 🟡 Backend listo, frontend pendiente |
| Login email/password | 🟡 UI lista, lógica pendiente |
| Renombrar / eliminar archivos | ⏳ Pendiente |

**Integración con el ecosistema:**
- Independiente actualmente — no consume APIs internas del ecosistema
- Potencial: integrar con `audio_control` (puerto 4000) para control físico de audio del servidor y descarga YouTube

**Dónde buscar más información:** `siax-amd:/home/pablinux/Projects/Node/audio-player/agents.md`

---

---

## Apps móviles/desktop

### sigmac_app — App CRM companion multiplataforma

App CRM companion offline-first para Android y Linux desktop. Gestiona ventas, compras, inventario, clientes, pedidos y proformas con SQLite local. Se autentica contra SIGMA WEBCONTROL y sincroniza documentos bidireccialmente con SIGMA GATEWAY CLOUD. Incluye monitor de comprobantes SRI en tiempo real vía SIGMAC-SRI-API. Es el cliente de campo principal del ecosistema SIGMA para vendedores y administradores.

| Parámetro | Valor |
|-----------|-------|
| Repositorio Git | `https://git.telcotronics.net/pablinux/sigmac_app.git` |
| Tecnología principal | Flutter 2.11.0 / Dart 2.17.0-beta |
| Responsable | pablinux |
| Estado actual | 🟡 En desarrollo activo — v1.0.0 publicada (APK + Linux) |
| Equipo / código local | `pablinux-laptop` (`192.168.10.72`) — `/home/pablinux/Projects/flutter/sigmac_app` |
| Plataformas | Android (`com.telcotronics.sigmac_app`) · Linux desktop |
| Servidor de producción | Sin servidor propio — APK + tar.gz publicados en WebControlSigma |
| Dominio público | — |
| Última actualización | 2026-06-21 (sesión 21) |

**BD local:**

| Motor | Archivo | Esquema | Uso |
|-------|---------|---------|-----|
| SQLite (sqflite + FFI) | `sigmac.db` en el dispositivo | v11 | BD offline-first — productos, clientes, ventas, compras, pedidos, proformas, usuarios locales, cache de reportes cloud |

**APIs que consume:**

| API | URL | Auth | Uso |
|-----|-----|------|-----|
| SIGMA WEBCONTROL | `https://api.siax-system.net` | `x-api-key` | Auth (login/registro/OTP/recuperación), notificaciones, alertas |
| SIGMA GATEWAY CLOUD | `https://api-gateway-cloud.telcotronics.net` | `x-api-key` + `?db=` | Sync items/clientes (↓), ventas upload (↑), pedidos/proformas (↑↓), reportes analíticos (↓) |
| SIGMAC-SRI-API | `https://api.sigmac.app/sri` | OAuth2 Password Grant (`pablinux/Microbot%`) | Monitor comprobantes SRI: stats, resumen diario, últimos 100 comprobantes |

**Módulos disponibles:**

| Módulo | Estado |
|--------|--------|
| Auth local + cloud (toggle en LoginScreen) | ✅ Operativo — un solo screen, radio Local/Cloud |
| Recuperación contraseña cloud (OTP) | ✅ Operativo |
| Ventas / Facturas | ✅ Operativo — upload sync implementado |
| Pedidos | ✅ Operativo — upload + download sync |
| Proformas | ✅ Operativo — upload + download sync |
| Compras | ✅ Operativo — upload pendiente (sin endpoint gateway) |
| Inventario / Productos | ✅ Operativo — download delta sync |
| Clientes | ✅ Operativo — download sync completo |
| Proveedores | ✅ Operativo |
| Dashboard / KPIs | ✅ Operativo — offline-first, cache SQLite ← 11 reportes cloud |
| Comprobantes PDF (A4, ticket, mixto) | ✅ Operativo |
| Envío comprobantes por email | ✅ Operativo |
| Sincronización datos (pantalla) | ✅ Operativo — badges pendientes por módulo |
| Reportes / KPIs (cache cloud) | ✅ Operativo — 11 reportes cacheados, pull-to-refresh |
| Monitor SRI | ✅ Operativo — `/sri_monitor`, KPIs + lista comprobantes en tiempo real |
| Ajustes de parámetros | ✅ Operativo — incluye rango descarga docs |

**Release / Deploy:**
- `desplegar.sh` — menú interactivo: compila APK (Android) y/o tar.gz (Linux), sube a `POST https://siax-system.net/api/upload_app.php` con icono (`archivo_ico`)
- v1.0.0 publicada 2026-06-21: APK 23 MB + Linux 13 MB

**Integración con el ecosistema:**
- **SIGMA WEBCONTROL** (`api.siax-system.net`): toda la auth y onboarding de usuarios
- **SIGMA GATEWAY CLOUD** (`api-gateway-cloud.telcotronics.net`): sincronización bidireccional de datos comerciales y reportes analíticos
- **SIGMAC-SRI-API** (`api.sigmac.app/sri`): monitor de comprobantes SRI; facturación electrónica real pendiente de integrar
- **WebControlSigma** (`siax-system.net`): registro de versiones y distribución de binarios

**⚠️ Notas críticas:**
- **Flutter 2.11 / Dart 2.17-beta**: APIs de Flutter 3.x no existen. Consultar `.agente/proyecto_errores.md` antes de usar cualquier API nueva.
- **SQLite WAL en Android**: usar `rawQuery()` para PRAGMAs — `execute()` crashea.
- **Dos APIs distintas**: WEBCONTROL (auth/licencias) ≠ GATEWAY CLOUD (datos negocio). No mezclar.
- **DB local schema v11**: `reportes_cache (clave, datos, anio, actualizado)` añadida en v11.
- **SSL `api.sigmac.app`**: expira 2026-08-30 — renovar antes de esa fecha.

**Más información:** `pablinux-laptop:/home/pablinux/Projects/flutter/sigmac_app/.agente/`

---

### app_comandas_restaurant — App Android de Comandas (SIGMA Restaurant)

App nativa Android (Java) para gestión de comandas de restaurante. Migración de la webapp `APP-SIGMA-WEB` (Node.js/Express) a un cliente Android orientado a tablets y dispositivos de meseros. Permite tomar pedidos por mesa, consultar el menú con fotos, gestionar clientes, ver pedidos activos y administrar usuarios — autenticado contra SIGMA WEBCONTROL con JWT + x-api-key.

| Parámetro | Valor |
|-----------|-------|
| Repositorio Git | `https://git.telcotronics.net/pablinux/APP_COMANDAS_RESTAURANT.git` |
| Tecnología principal | Java 8 / Android nativo (AGP 8.2.2, Gradle 8.4) |
| Responsable | pablinux |
| Estado actual | 🟡 En desarrollo activo |
| Código local | `siax-intel` (`192.168.10.101`) — `/home/pablinux/Projects/android/app_comandas_restaurant` |
| App ID | `com.telcotronics.sigmarestaurant` |
| minSdk / targetSdk | 24 / 34 |
| Auth | `https://api.siax-system.net/api/auth/login` (SIGMA WEBCONTROL) — `{email, paswd}` → JWT + apiKey |
| Backend datos | `https://api-gateway-cloud.telcotronics.net/` — JWT Bearer + `x-api-key` + `?db=TENANT` |
| Última actualización | 2026-06-14 |

**Módulos disponibles:**

| Módulo | Estado |
|--------|--------|
| Login / Auth (WEBCONTROL JWT + apiKey) | ✅ Implementado |
| NavigationDrawer (5 fragments) | ✅ Implementado |
| Dashboard — pedidos recientes | ✅ Base — faltan cards de resumen |
| Pedidos (lista + colores de estado) | ✅ Implementado |
| Clientes (lista + búsqueda) | ✅ Implementado |
| Mesas — derivadas de `origen` en pedidos | ✅ Implementado |
| Usuarios | ✅ Implementado |
| MenuMeseroActivity — toma de pedido | ✅ Implementado — landscape, categorías por grupo, grid items, IVA 15%, POST pedido |
| NuevoClienteActivity — registro cliente | ✅ Implementado — validación cédula/RUC Ecuador |
| Chat | ❌ Pendiente |
| Menú admin (gestión de items) | ❌ Pendiente |

**Integración con el ecosistema:**
- **SIGMA WEBCONTROL** (`api.siax-system.net`): autenticación. Login → `{token, apiKey, db_tenant}`
- **API Gateway Cloud** (`api-gateway-cloud.telcotronics.net`): datos (pedidos, clientes, productos, usuarios, ciudades). Requiere `x-api-key` header + `?db=TENANT` en cada request
- Mesas = valores distintos del campo `origen` en pedidos — LIBRE si no hay pedido ACTIVO

**Más información:** `siax-intel:/home/pablinux/Projects/android/app_comandas_restaurant/agents.md`

---

### SIGMAC — ERP Desktop Java/Swing

| Parámetro | Valor |
|-----------|-------|
| Repositorio Git | Repositorio local — pendiente subir a git.telcotronics.net |
| Tecnología principal | Java 11 (NetBeans + Swing) + MySQL — pool HikariCP |
| Responsable | pablinux |
| Estado actual | ✅ Producción (v actual) · 🔧 Nueva versión en desarrollo |
| Código producción | `siax-amd` (`192.168.10.100`) — `/home/pablinux/NetBeansProjects/facturacion` |
| Código nueva versión | `siax-amd` (`192.168.10.100`) — `/home/pablinux/Projects/java/SIGMAC` |
| Servidor de producción | Servidor-SIGMA-VW CT 141 (`192.168.10.110`) — Webswing 20.2.5 |
| Acceso web | `https://app.factura-e.net` (Apache `.109` → Webswing `.110`) |
| Última actualización | 2026-06-16 |

ERP de escritorio para facturación electrónica en Ecuador. La aplicación Java Swing corre en el servidor Webswing (CT 141) y se publica en el navegador vía HTML5 Canvas sin modificar el código fuente. Gestiona el ciclo completo de ventas, compras, inventario, contabilidad, CXC y CXP. Se integra con el SRI a través de `SIGMA-OPEN-API` (legacy) y `SIGMAC-SRI-API` (nueva). Arquitectura multi-tenant: cada empresa opera sobre su propia BD `EMPRESA_<nombre>` en `.115`, clonada desde `EMPRESA_SEED` (plantilla oficial con identidad normalizada + tablas de negocio completas).

**BDs que usa:**

| BD | Host | Motor | Uso |
|----|------|-------|-----|
| `facturacion` | `192.168.10.116` (prod) / `192.168.10.149` (test) | MySQL 8.0 | BD principal — facturas, clientes, inventario, contabilidad, CXC, CXP |
| `EMPRESA_SEED` | `192.168.10.115` | MySQL 8.0 | Plantilla oficial de tenant — 174 tablas BASE + 48 vistas. Onboarding: `exec/replica_empresa.sh` |
| `EMPRESA_*` (tenants) | `192.168.10.115` | MySQL 8.0 | Una BD por empresa: TELCOTRONICS, DOMUS, XSYSTEM, LIS, aluxury, zuba |
| `sigma` | `192.168.10.115` | MySQL 8.0 | Parches y actualizaciones distribuidas — registra cambios de esquema; cada empresa ve y aplica pendientes al abrir la app |

**Estructura de `EMPRESA_SEED`:**

| Capa | Tablas | Descripción |
|------|--------|-------------|
| Identidad normalizada | 13 | `personas`, `persona_relaciones`, `*_datos`, `plataformas`, `módulos`, `usuario_grupos`, `biometria` |
| Negocio (ERP completo) | 161 | Inventario, contabilidad, CXC/CXP, facturación, proyectos, reportes |
| **Total tablas BASE** | **174** | — |
| Vistas de compatibilidad | 4 | `clientes`, `proveedores`, `usuarios`, `socios` → apuntan a tablas normalizadas |
| Vistas de negocio | 44 | Réplica de todas las vistas operativas de TELCOTRONICS |
| **Total vistas** | **48** | — |

**Servicios que consume:**

| Servicio | URL | Uso |
|---------|-----|-----|
| SIGMA-OPEN-API (legacy) | `http://192.168.10.120:8080/veronica` | Firma y autorización SRI — sistemas existentes |
| SIGMAC-SRI-API (nueva) | `https://api.sigmac.app/sri` | Nueva API SRI — migración progresiva |
| SRI Ecuador | `https://cel.sri.gob.ec/...` | Recepción y autorización de comprobantes electrónicos |
| IA local | `http://192.168.10.101:1706` | LLM para módulo SIAX Chat (Nemotron / Gemma) |
| Monitor TCP | `localhost:1803` | Sincronización con servidor de monitoreo interno |
| IA_update API | `https://api.siax-system.net/api/sql/updates` | Distribución de SQL deltas (DDL/DML) a clientes — `x-api-key` |
| Cloud Storage _(en diseño)_ | `https://cloud.sigmac.app` _(pendiente)_ | Instaladores, binarios y reportes — upload → URL hash pública |

**Módulos disponibles:**

| Módulo | Estado |
|--------|--------|
| Facturación / Ventas | ✅ Producción |
| Inventario / Productos | ✅ Producción |
| Compras / Docs Electrónicos | ✅ Producción |
| Monitor de Servicios SRI (auto) | ✅ Producción |
| CXC — Cuentas por Cobrar | ⚠️ Fix activo en rama |
| CXP — Cuentas por Pagar | ✅ Producción |
| Contabilidad / Bancos | ✅ Producción |
| Balance de Comprobación | ✅ Producción |
| Libro Mayor | ✅ Producción |
| Estado de Resultados | ✅ Producción |
| Notas de Crédito Ventas | ✅ Implementado (pendiente prueba prod) |
| Notas de Crédito Compras | ✅ Implementado (pendiente menú) |
| IA — SIAX Chat | 🔧 En desarrollo |

**Integración con el ecosistema:**
- **FACTURA-E (PHP web):** comparte la BD `facturacion` en `.116` — acceso directo para informes y portal web de clientes. Auth compartida vía `webControl.usuarios_sesion` en `.149`.
- **Webswing CT 141 (.110):** publica la UI Java Swing en el navegador sin modificar código fuente.
- **SIGMA-OPEN-API / SIGMAC-SRI-API:** única vía de comunicación con el SRI para firma y autorización de comprobantes.
- **DB-EMPRESAS (.115):** arquitectura multi-tenant con onboarding vía `exec/replica_empresa.sh` — clona `EMPRESA_SEED` completa para cada nueva empresa.

**Más información:** `siax-amd:/home/pablinux/Projects/java/SIGMAC/agents.md`

---

### AI_update — Actualizador de Esquemas SQL

Herramienta de escritorio (Java Swing) que mantiene sincronizados los esquemas de base de datos de los clientes SIGMA con el servidor central. Descarga parches SQL incrementales desde la API REST `api.siax-system.net` y los aplica directamente sobre la BD MySQL del cliente, garantizando idempotencia mediante la tabla `SIGMA.HistorialActualizacionBD`. Tiene dos modos: automático (bot SIGMA con máquina de estados, timer 50 ms) y manual (`CompararActualizacion` para selección de parches). Es el eslabón que mantiene todos los tenants de SIGMAC en el mismo esquema de BD sin requerir acceso SSH ni intervención manual del administrador.

| Parámetro | Valor |
|-----------|-------|
| Repositorio Git | Repositorio local — pendiente subir a git.telcotronics.net |
| Tecnología principal | Java 8 (NetBeans + Swing + Apache Ant) + MySQL JDBC + Gson |
| Responsable | pablinux |
| Estado actual | ✅ Activo / Producción |
| Equipo / código local | `pablinux-laptop` (`192.168.10.72`) — `/home/pablinux/Projects/java/AI_update` |
| Servidor de producción | Sin servidor propio — distribuido como `dist/IA_update.jar` en equipos cliente |
| Dominio público | — |
| Puerto | — (app desktop, sin servidor HTTP) |
| Última actualización | 2026-06-16 |

**BDs que usa:**

| BD | Host | Motor | Uso |
|----|------|-------|-----|
| `SIGMA` | Host del cliente (leído de `dat/bd_serv.cfg`) | MySQL 8.0 | `HistorialActualizacionBD` — registro idempotente de parches aplicados |
| BD objetivo del tenant | Host del cliente (leído de `dat/bd_serv.cfg`) | MySQL 8.0 | BD real del cliente (ej. `facturacion`, `TELCOTRONICS`, `DOMUS`) donde se aplican los parches SQL |

**Servicios que consume:**

| Servicio | URL | Autenticación | Propósito |
|---------|-----|---------------|-----------|
| API-SIGMA-WEBCONTROL | `https://api.siax-system.net/api/sql/check_update` | `x-api-key` | Verificar si hay parches nuevos disponibles |
| API-SIGMA-WEBCONTROL | `https://api.siax-system.net/api/sql/updates?since=YYYY-MM-DD` | `x-api-key` | Descargar lote de parches SQL desde una fecha dinámica |
| API-SIGMA-WEBCONTROL | `https://api.siax-system.net/api/apps/versiones/IA_update/latest` | `x-api-key` | Consultar última versión del propio JAR para auto-actualización |
| PHP legacy (modo manual) | `https://telcotronics.com/app/Sinc/HistorialActualizaciones.php` | — | Endpoint heredado — solo usado por `CompararActualizacion` (pendiente migrar a REST) |

No expone servicios propios — es una aplicación cliente sin API propia.

**Módulos disponibles:**

| Módulo | Estado |
|--------|--------|
| Modo automático (`IA_update` + máquina de estados `nivelesAvance`) | ✅ Operativo — timer 50 ms, 9 estados |
| Modo manual (`CompararActualizacion`) | ✅ Operativo — conecta a PHP legacy, pendiente migrar a REST |
| Descarga y aplicación de parches SQL (`Actualizar_bd`) | ✅ Operativo — ejecución paralela por hilo, idempotente |
| REST client (`DescargarJsonAPI`) | ✅ Operativo — `checkUpdate()`, `descargarJsonAPI(since)`, `obtenerVersionLatest()` |
| Auto-actualización del JAR (`LeerVersiones_arch`) | ✅ Implementado — descarga atómica a `.tmp`, verifica MD5 si disponible |
| Logs persistentes (`DataLog`) | ✅ Operativo — `dat/error.log`, append, timestamp `yyyy-MM-dd HH:mm:ss` |
| Credenciales cifradas (`CryptoUtils`) | ⚠️ Stub — AES/GCM preparado, no integrado (credenciales aún en Base64) |

**Integración con el ecosistema:**
- **SIGMAC ERP** (CT 141, `192.168.10.110`): IA_update es el mecanismo que mantiene al día el esquema SQL de cada cliente. SIGMAC lo referencia en sus servicios consumidos.
- **API-SIGMA-WEBCONTROL** (`api.siax-system.net`): fuente única de parches SQL y registro de versiones del JAR distribuido.
- **Tenants MySQL** (`.116` prod / `.149` test): parches se aplican sobre la BD activa del tenant, con el placeholder `"facturacion"` reemplazado dinámicamente por el nombre real.

**Dónde buscar más información:** `pablinux-laptop:/home/pablinux/Projects/java/AI_update/agents.md`

---

### app_sigma_inventario (Control Inventario SIGMAC) — App de Gestión y Control de Inventario

Aplicación móvil y desktop para supervisores y bodegueros de Telcotronics (nombre de launcher: **Control Inventario**). Permite realizar auditorías de inventario físico, gestionar traslados internos de mercadería emitiendo hojas de despacho con código de barras e ingresando recepciones externas mediante digitalización fotográfica y OCR automatizado. Se autentica contra API-SIGMA-WEBCONTROL y sincroniza el catálogo de productos con API-SIGMA-CLOUD.

| Parámetro | Valor |
|-----------|-------|
| Repositorio Git | Repositorio local — [pendiente — git.telcotronics.net] |
| Tecnología principal | Flutter (Android + Linux Desktop) / Dart (Sound Null Safety) |
| Responsable | pablinux |
| Estado actual | 🟡 En desarrollo activo |
| Equipo / código local | `pablinux-laptop` (`192.168.10.72`) — `/home/pablinux/Projects/flutter/app_sigma_inventario` |
| Servidor de producción | Sin servidor propio — app distribuida como APK/binario vía WebControlSigma CLI Sync |
| Dominio público | — |
| Puerto interno | — |
| Servicio systemd | — |
| BD principal | Almacén reactivo en memoria (`DataStore`) + sesión en `shared_preferences` + Postgres CRM (`recepcion_productos_x_homologar`) |
| Versión publicada | `1.0.0` — ANDROID + LINUX + ícono registrados en WebControlSigma (app_id 21/23) |
| Última actualización | 2026-06-17 |

**Bases de datos y almacenamiento local:**

| Motor | Archivo / IP | Esquema / Tabla | Uso principal |
|-------|--------------|-----------------|---------------|
| En memoria reactiva | `lib/data_store.dart` | `DataStore` estático | Almacenamiento local mock de bodegas, stock, traslados y homologación |
| shared_preferences | dispositivo local | `auth_nombre`, `auth_email`, `auth_rol`, `auth_db_name`, `auth_api_key` | Variables de sesión estándar del usuario autenticado |
| PostgreSQL | `192.168.10.116` | `recepcion_productos_x_homologar` | Cola de homologación comercial del CRM para administración de productos |

**Servicios que consume:**

| Servicio | URL / IP | Auth | Propósito |
|---------|---------|------|-----------|
| API-SIGMA-WEBCONTROL | `https://api.siax-system.net/api/auth/login` | Pública | Autenticación real — `POST {email, paswd}` → JWT + apiKey + db_tenant |
| API-SIGMA-CLOUD | `https://api-gateway-cloud.telcotronics.net/api/items/sync` | `x-api-key` | Sincronización del catálogo de productos por tenant (`?db=`, `?limite=`, `?offset=`) |
| Telcotronics OCR API | `https://api.telcotronics.net/pdf_tablas/primera/` | `X-API-Key` | Procesamiento inteligente y digitalización de imágenes de guías físicas |

**Módulos disponibles:**

| Módulo | Estado |
|--------|--------|
| Panel de Inicio (`InicioScreen`) | ✅ Completado — Métricas, alertas de stock bajo y ocupación de bodegas |
| Gestión de Bodegas (`BodegasScreen`) | ✅ Completado — Visualización de almacenes, capacidades volumétricas y subdivisiones de secciones físicas |
| Auditoría de Inventario (`InventarioScreen`) | ✅ Completado — Conciliación de unidades teóricas vs físicas y láser |
| Traslados Internos (`TrasladoScreen`) | ✅ Completado — Despacho, previsualización de reportes e impresión con código de barras |
| Recepción de Guías (`RecepcionScreen`) | ✅ Completado — Captura fotográfica con OCR y homologación de nuevos ítems |
| Login / Auth real (`LoginScreen`) | ✅ Completado — Autenticación real vía API-SIGMA-WEBCONTROL (JWT + apiKey + db_tenant); sesión en `shared_preferences` |
| Perfil del Usuario (`PerfilScreen`) | ✅ Completado — Pantalla dedicada con datos de sesión cargados desde `shared_preferences` |
| Sincronización Cloud (`SincronizacionScreen`) | ✅ Completado — Pantalla dedicada; sync masivo de catálogo vía API-SIGMA-CLOUD |
| Gestión de Datos Local (`GestionDatosScreen`) | ✅ Completado — Pantalla dedicada; demo data, limpiar BD, configurar API Gateway |

**Integración con el ecosistema:**
- **API-SIGMA-WEBCONTROL** (`api.siax-system.net`): autenticación real del usuario — login → JWT + apiKey + db_tenant almacenados en sesión.
- **API-SIGMA-CLOUD** (`api-gateway-cloud.telcotronics.net`): sincronización del catálogo de productos por tenant; usa la `x-api-key` obtenida en login.
- **Telcotronics OCR API** (`api.telcotronics.net`): digitalización de tablas e información de cabeceras de remisiones.
- **CRM/ERP SIGMA** (`192.168.10.116`): los productos no homologados se guardan en `recepcion_productos_x_homologar` para que el administrador complete el alta financiera y contable.

**Deploy:** `./desplegar.sh "changelog"` — detecta plataforma automáticamente (Linux→Android+Linux, Windows→Windows, macOS→macOS), sube ícono/banner si `APP_ICONO`/`APP_BANNER` están en `servers.conf`, y registra en WebControlSigma. Requiere `servers.conf` local (ver `servers.conf.example`).

**Más información:** `pablinux-laptop:/home/pablinux/Projects/flutter/app_sigma_inventario/.agente/`

---

### agente_ventas — App de pedidos y rutas para vendedores de campo

App móvil y desktop para vendedores de campo de Telcotronics. Gestiona la ruta del día con mapa esquemático custom, catálogo de productos con carrito, pedidos CRUD, firma digital del cliente, scanner QR/barcode real, búsqueda de clientes escalable y notificaciones in-app. Arquitectura offline-first con SQLite local — se autentica contra API-SIGMA-WEBCONTROL y sincroniza datos con API-SIGMA-CLOUD.

| Parámetro | Valor |
|-----------|-------|
| Repositorio Git | Sin repositorio — código local únicamente |
| Tecnología principal | Flutter 2.11.0 / Dart 2.17.0-beta · SQLite (sqflite + FFI) · `mobile_scanner 0.2.0` |
| Responsable | pablinux |
| Estado actual | 🟡 En desarrollo activo — integrando API real |
| Nombre en launcher | `Agente Ventas` · Título interno: `Agente Ventas SIGMAC` |
| Package ID | `com.sigmac.agenteventas` |
| Equipo / código local | `pablinux-laptop` (`192.168.10.72`) — `/home/pablinux/Projects/flutter/pedidos_app` |
| Plataformas | Android APK release ✅ · Linux desktop ✅ · Web (`flutter build web` ✅) |
| Servidor de producción | Sin servidor propio — app distribuida como APK/binario |
| Dominio público | — |
| Última actualización | 2026-06-14 |
| APK release | `build/app/outputs/flutter-apk/app-release.apk` — 18.9 MB |
| Build Android | Requiere `JAVA_HOME=/usr/lib/jvm/java-1.11.0-openjdk-amd64` — Java 25 rompe Gradle 6.7 |

**BD local:**

| Motor | Archivo | Tablas | Uso |
|-------|---------|--------|-----|
| SQLite (sqflite + FFI) | `telcotronics.db` (en dispositivo) | 7: usuarios, clientes, productos, rutas, paradas_ruta, pedidos, items_pedido | Persistencia offline-first — seed automático en primer arranque |

**APIs que consume:**

| API | URL | Auth | Uso |
|-----|-----|------|-----|
| API-SIGMA-WEBCONTROL | `http://192.168.10.145:3002` | Pública | Auth: `POST /api/auth/empresas` + `POST /api/auth/login` → JWT + apiKey + db_tenant |
| API-SIGMA-CLOUD | `https://api-gateway-cloud.telcotronics.net` | `x-api-key` + `?db=TELCOTRONICS` | Catálogo de productos (items), clientes, pedidos — sync delta con `?desde=` |

**Flujo de autenticación:**
1. `POST /api/auth/empresas {email, password}` → lista empresas del vendedor
2. `POST /api/auth/login {email, password, dba}` → JWT (8h) + apiKey + db_tenant
3. Requests a API-SIGMA-CLOUD: `x-api-key: {apiKey}` + `Authorization: Bearer {jwt}` + `?db=TELCOTRONICS`

**Módulos disponibles:**

| Módulo | Estado |
|--------|--------|
| Login (local demo + cloud API-SIGMA-WEBCONTROL) | 🔧 Integrando |
| Dashboard / Home (stats del día, pedidos recientes) | ✅ |
| Ruta del día (mapa custom `CustomPainter`, paradas, agregar/eliminar) | ✅ |
| Catálogo de productos (carrito, filtros por categoría) | ✅ — sync API-SIGMA-CLOUD pendiente |
| Scanner QR / Código de barras (cámara real Android/iOS, input manual Linux) | ✅ |
| Búsqueda de clientes (pantalla dedicada, debounce 250ms, límite 50 resultados) | ✅ — sync API-SIGMA-CLOUD pendiente |
| Pedidos CRUD (lista filtrable, crear, detalle, cambio de estado) | ✅ — upload API-SIGMA-CLOUD pendiente |
| Firma digital del cliente (pad custom `GestureDetector` + Bezier curves) | ✅ |
| Registro de clientes (formulario + GPS placeholder) | ✅ |
| Notificaciones in-app (banners overlay, centro de notifs, badge, triggers auto) | ✅ |
| Perfil del vendedor | ✅ |

**Integración con el ecosistema:**
- **API-SIGMA-WEBCONTROL** (`192.168.10.145:3002`): auth y sesión del vendedor
- **API-SIGMA-CLOUD** (`api-gateway-cloud.telcotronics.net`): catálogo items BD `TELCOTRONICS`, clientes tenant, pedidos upload
- **sigma-robot**: potencial — notificaciones push WhatsApp al confirmar pedido

**Dónde buscar más información:** `pablinux-laptop:/home/pablinux/Projects/flutter/pedidos_app/.agente/`

---

### seguridad_electronica — SENTINEL ONE App de Seguridad Electrónica

App Flutter offline-first para operadores y guardias de seguridad electrónica. Gestiona alarmas activas por zona y sensor, control de acceso a puertas físicas, mensajería interna con la central de monitoreo y registro de sesiones del operador. Arquitectura offline-first con SQLite local — la UI solo lee de la BD local; la sincronización con el backend del proveedor ocurrirá a través de `ApiAuthService` y `Sincronizador` cuando se configure la URL de producción. No comparte infraestructura con el ecosistema SIGMA — es un producto independiente para clientes del sector de seguridad electrónica.

| Parámetro | Valor |
|-----------|-------|
| Repositorio Git | `https://git.telcotronics.net/pablinux/seguridad_electronica.git` |
| Tecnología principal | Flutter 2.11.0 / Dart 2.17-beta · SQLite (sqflite + FFI) · Material 3 · Dark Theme |
| Responsable | pablinux |
| Estado actual | 🟡 En desarrollo activo (sesión 7 completa, sesión 8 en progreso) |
| Equipo / código local | `siax-amd` (`192.168.10.100`) — `/home/pablinux/Projects/flutter/seguridad_electronica` |
| Plataformas | Android · iOS · Linux desktop (Ubuntu Touch) |
| App ID | `net.siaxsystem.sentinelone` |
| Servidor de producción | Sin servidor propio — app distribuida como APK/binario |
| Dominio público | — |
| Puerto | — |
| Última actualización | 2026-06-21 |

**BD local:**

| Motor | Archivo / Ruta | Esquema | Uso |
|-------|---------------|---------|-----|
| SQLite (sqflite + FFI) | Dispositivo: `sentinel_one.db` · Linux: `~/.local/share/sentinel_one/sentinel_one.db` | v3 — 14 tablas | BD offline-first — usuarios, zonas, nodos, puertas, alarmas, accesos, eventos, mensajes, banners, sesiones, clientes, suscripciones, sync_log, configuracion |

**Servicios que consume:**

| Servicio | URL | Auth | Estado |
|---------|-----|------|--------|
| API_CENTINEL_SECURITY | `https://api.telcotronics.com` | `x-api-key` | Pendiente integrar — control de puertas, biometría y eventos de acceso en tiempo real |
| ApiAuthService (backend proveedor) | Pendiente URL de API real | JWT Bearer | Estructura lista — sin URL de producción |
| Sincronizador (backend proveedor) | Pendiente URL de API real | JWT Bearer | Estructura lista — sin URL de producción |

**Módulos disponibles:**

| Módulo | Archivo | Estado |
|--------|---------|--------|
| Login (PIN local SHA-256 + SharedPreferences) | `main.dart` → `LoginPage` | ✅ Completo |
| Layout principal (nav + header) | `main_page.dart` | ✅ Completo |
| Inicio (usuario, empresa, banner, log eventos) | `pages/inicio_page.dart` | ✅ BD conectada |
| Monitoreo y Alarmas | `pages/monitoreo_alarma_page.dart` | ✅ BD conectada |
| Control de Acceso | `pages/control_acceso_page.dart` | ✅ BD conectada |
| Mensajería (chat estilo WhatsApp) | `pages/mensageria_page.dart` | ✅ BD conectada |
| Perfil de Usuario + foto | `pages/perfil_usuario_page.dart` | ✅ BD + foto perfil |
| Llamada simulada (fullscreen, cronómetro) | `pages/llamada_page.dart` | ✅ Completo |
| Conectar Proveedor (onboarding URL/usuario/contraseña) | `pages/conectar_proveedor_page.dart` | ✅ Completo |
| Cambio de PIN | `pages/seguridad_page.dart` | ✅ Completo |
| Historial de sesiones | `pages/historial_sesiones_page.dart` | ✅ Completo |
| BD SQLite v3 (14 tablas, 14 DAOs, 12 modelos) | `lib/db/` · `lib/models/` | ✅ Completo |
| DemoDataService (datos de prueba) | `services/demo_data_service.dart` | ✅ Completo |
| Página de Alarmas dedicada | `pages/alarmas_page.dart` | 🔴 Vacío — pendiente |
| Registro de usuarios (Control Acceso) | `pages/control_acceso_page.dart` | 🔴 Pendiente — FAB + formulario |
| Botones Pánico/Soporte → eventos reales | `pages/mensageria_page.dart` | 🔴 Pendiente — insertar en tabla eventos |

**Integración con el ecosistema:**
- **API_CENTINEL_SECURITY** (`api.telcotronics.com`): integración pendiente — el módulo de Control de Acceso consumirá esta API para apertura remota de puertas, registro de credenciales biométricas y recepción de eventos físicos en tiempo real
- Cuando se defina el backend del proveedor: auth vía `ApiAuthService` (JWT) + sync vía `Sincronizador` → SQLite local
- Potencial: notificaciones de alarma vía `sigma-robot` (WhatsApp) para alertas críticas

**Dónde buscar más información:** `siax-amd:/home/pablinux/Projects/flutter/seguridad_electronica/plan_proyecto.md`

---

## Servicios transversales

### sigma-robot — Hub central de comunicaciones e IA

| Parámetro | Valor |
|-----------|-------|
| Repositorio Git | `https://git.telcotronics.net/pablinux/sigma-robot.git` |
| Tecnología principal | Node.js + Express + MySQL + Socket.IO |
| Responsable | pablinux |
| Estado actual | ✅ Activo — `server-webapps` CT 132 (`192.168.10.160`) |
| Puerto | `5000` |
| Servicio systemd | `siax-app-sigma-robot.service` |
| URL pública | `https://sigma-bot.telcotronics.com` |
| MCP expuesto | `sigma-robot.telcotronics.com` — herramientas: `ia_chat`, `whatsapp_enviar`, `crm_consultar`, `woo_consultar`, `db_query`, `buscar_respuesta`, `listar_agentes` |
| Equipo / ubicación local | siax-amd (192.168.10.100) — `/home/pablinux/Projects/Node/sigma-robot` |
| Última actualización | 2026-05-31 |
| Rol en el ecosistema | **Cerebro de comunicaciones y orquestación de agentes IA.** Cualquier app o robot del ecosistema que necesite enviar mensajes, consultar IA, o ejecutar agentes automatizados se conecta aquí. |

**¿Qué hace?**

sigma-robot unifica en un solo hub: mensajería WhatsApp (Meta Cloud API y Web Bot), procesamiento de IA con fallback automático, y ejecución de agentes configurables desde el panel. Es el punto de integración que el resto del ecosistema usa para comunicarse con clientes y automatizar tareas inteligentes.

**Bases de datos:**

| BD | Motor | IP | Variable env | Uso |
|----|-------|----|-------------|-----|
| `siax_core` | MariaDB (CT 114) | 192.168.10.149 | `SIGMA_DB_*` | BD principal — IA, usuarios, agentes, flujos, prompts, API keys |
| `TELCOTRONICS` | MySQL (CT 145) | 192.168.10.116 | `DB_TELCO_*` / `DB_*` | BD externa — comprobantes bancarios (OCR), galerías |

**Servicios que consume:**

| Servicio | IP / URL | Uso |
|---------|---------|-----|
| SIAX IA local | `192.168.10.101:1706` | Proveedor IA primario (Gemma 4 26B) |
| Whisper STT | `192.168.10.145:8000` | Transcripción de audio a texto |
| OCR / TTS / STT | `https://api.telcotronics.net` | Extracción de texto de imágenes y comprobantes |
| n8n | `192.168.10.171:5678` | Workflows de automatización (webhook entrante) |

**Cómo usarlo desde otras apps del ecosistema:**

```
# 1. Enviar mensaje WhatsApp desde CRM/ERP
POST https://sigma-bot.telcotronics.com/api/meta/enviar_mensaje
x-api-key: {api_key}
{ "to": "593XXXXXXXXX", "message": "Hola, tu pedido está listo." }

# 2. Consultar IA (compatible OpenAI)
POST https://sigma-bot.telcotronics.com/gateway/v1/chat
x-api-key: {api_key}
{ "messages": [{ "role": "user", "content": "Analiza este texto: ..." }] }

# 3. Vía MCP (para agentes IA del ecosistema)
Tool: whatsapp_enviar  → envía mensaje WhatsApp
Tool: ia_chat          → consulta IA con fallback automático
Tool: db_query         → consulta BD externa configurada
Tool: crm_consultar    → consulta REST a CRM externo
```

**Prioridad de proveedores IA (fallback automático):**

| Prioridad | Proveedor | Tipo | Variable env |
|-----------|-----------|------|-------------|
| 1 | SIAX | siax | `$SIAX_API` / `$SIAX_URL` |
| 2 | DeepSeek | openai | `$DEEPSEEK_API_KEY` |
| 3 | Gemini | gemini | `$GEMINI_API_KEY` |
| 4 | Claude | anthropic | `$ANTHROPIC_API_KEY` |

**Casos de uso del sistema de agentes (objetivos a cumplir):**

| # | Caso | Estado |
|---|------|--------|
| C1 | CRM/ERP envía documentos/notificaciones por WhatsApp via API | ✅ Activo |
| C2 | App externa envía prompt + datos → IA procesa → retorna resultado | ✅ Activo |
| C3 | Cliente pide algo por WhatsApp → agente consulta BD → responde | 🔧 Motor de flujos pendiente |
| C4 | Chat de soporte recolecta datos del cliente → clasifica → resuelve o escala | 🔧 En desarrollo |

**Módulos disponibles:**

| Módulo | Estado |
|--------|--------|
| WhatsApp Bot WS (whatsapp-web.js) | ✅ Activo |
| WhatsApp Cloud API (Meta Webhooks) | ✅ Activo |
| AI Gateway (`/gateway/v1/chat`) | ✅ Activo |
| Messaging Gateway (`/api/meta/`, `/api/wsbot/`) | ✅ Activo |
| Motor de IA con fallback automático | ✅ Activo — 4 proveedores |
| Panel Admin (AdminLTE 3) | ✅ Activo |
| Portal Agentes (`/agentes`) | ✅ Activo |
| Portal Arrendatarios (`/empresas`) | ✅ Activo |
| MCP Server | ✅ Activo |
| Clasificador de intenciones | ✅ Activo — listo para configurar |
| Agentes / Flujos IA (`ia_agentes`, `ia_flujos`) | 🟡 Estructura lista — motor de ejecución pendiente |
| Chat de soporte integrado (C4) | 🔧 Interfaz activa — flujo guiado pendiente |

**Integración con el ecosistema:**
- **n8n (.171):** envía webhooks entrantes en `/webhook/n8n` para automatizaciones del ecosistema
- **CRM / ERP / sistemas externos:** consumen la Messaging Gateway para enviar mensajes WhatsApp vía API Key
- **Apps externas (Confyui, Dialogflow):** envían prompts a la AI Gateway para procesamiento IA con fallback
- **mail-monitor:** puede consumir la AI Gateway (`/gateway/v1/chat`) para análisis de logs con IA

**Más información:** `siax-amd:/home/pablinux/Projects/Node/sigma-robot/agents.md`

---

### mail-monitor — Administración y monitoreo del servidor de correo

| Parámetro | Valor |
|-----------|-------|
| Repositorio Git | `https://git.telcotronics.net/pablinux/Monitor-ServerMail.git` |
| Tecnología principal | Rust (Axum 0.7 + sqlx 0.7 + Tera + HTMX) |
| Responsable | pablinux |
| Estado actual | ✅ Producción (desplegado en `servidor-email` CT 144, `192.168.10.111`) |
| Rol en el ecosistema | Administración y monitoreo del servidor de correo SIGMA. Gestiona usuarios virtuales de Postfix/Dovecot, visualiza logs por SSH, controla fail2ban y notifica eventos de seguridad y administrativos a `API-SIGMA-WEBCONTROL` |

**Acceso:** `http://192.168.10.111:3000`

**Eventos que notifica a `API-SIGMA-WEBCONTROL`:**

| Evento | Tipo | Severidad |
|--------|------|-----------|
| IP baneada en fail2ban | `seguridad` | `alta` |
| IP desbaneada | `seguridad` | `baja` |
| Cuenta de correo creada | `admin` | `info` |
| Cuenta de correo desactivada | `admin` | `media` |
| Cuenta de correo reactivada | `admin` | `info` |
| Contraseña de cuenta cambiada | `admin` | `info` |

**Cumplimiento RGPD/LOPD:** Tab "Desactivados" en la UI — muestra `fecha_modificacion` (cuándo se desactivó), permite reactivar cuentas o eliminarlas definitivamente (borrado físico de la BD) para cumplir solicitudes de supresión de datos.

**Integración con el ecosistema:**
- **BD correo:** MariaDB en `192.168.10.149` (`mailserver_db`) — tablas `virtual_users`, `virtual_domains`, `app_config`
- **SSH al servidor:** `192.168.10.111` — para logs de Postfix/Dovecot, control de fail2ban y creación de maildirs
- **API-SIGMA-WEBCONTROL:** notificaciones vía `x-api-key` (token de `webControl.api_key`)
- **SIGMA Bot gateway:** análisis de logs con IA (`https://sigma-bot.telcotronics.com/gateway/v1/chat`)

---

### CT cloud — servidor-email (192.168.10.111)

> **Servidor de correo del ecosistema SIGMA.** Cualquier app o sistema que necesite enviar correos usa este servidor. La cuenta de sistema, credenciales y puertos están documentados aquí — no buscar en otro lugar.

| Parámetro | Valor |
|-----------|-------|
| IP | 192.168.10.111 |
| MAC | BC:24:11:EC:44:0D |
| CT Proxmox | 144 (nodo cloud) |
| SMTP | Postfix — relay vía Resend.com |
| IMAP | Dovecot |
| Webmail | SnappyMail 2.38.2 |
| Dominios activos | `sigmac.app`, `factura-e.net` |
| BD usuarios correo | MariaDB en 192.168.10.149 (`mailserver_db`) |
| Administración | mail-monitor en `http://192.168.10.111:3000` — documentación técnica en `/docs` |

#### Configuración de correo para sistemas del ecosistema

> Usar estos datos en cualquier app, servicio o herramienta del ecosistema que necesite enviar correos (CRM SIGMA, sigmac_app, n8n, notificaciones, mailing, etc.).

**Envío (SMTP):**

| Campo | Valor |
|-------|-------|
| Host | `smtp.sigmac.app` |
| Puerto | `587` |
| Usuario | `no-reply@sigmac.app` |
| Contraseña | `Sigma.2030@` |
| Seguridad | `STARTTLS` |

**Lectura (IMAP):**

| Campo | Valor |
|-------|-------|
| Host | `imap.sigmac.app` |
| Puerto | `993` |
| Usuario | `no-reply@sigmac.app` |
| Contraseña | `Sigma.2030@` |
| Seguridad | `SSL/TLS` |

**Desde LAN interna (192.168.10.x):** reemplazar el hostname por `192.168.10.111` — sin dependencia de DNS externo.

**Relay saliente:** Resend.com, gestionado por Postfix. La app solo habla con el SMTP local.

#### Notas técnicas del servidor de correo

**⚠️ mysql-users.cf:** La query DEBE retornar `domain/user/` (ruta relativa Maildir). Si retorna el email completo, Postfix crea archivos en lugar de directorios.

**⚠️ Certificados SSL:** Se copian manualmente desde Servidor-web (.109). No hay certbot en el .111.

---

### SIAX Monitor — Agente de monitoreo de aplicaciones

SIAX Monitor se instala en los servidores donde corren aplicaciones Node.js o Python. Registra cada app como un servicio systemd (`siax-app-NOMBRE.service`), controla su ciclo de vida (start/stop/restart) and monitorea su estado cada 60 segundos reportando al dashboard central. Detecta discrepancias entre el proceso real y el estado de systemd (crashed, zombie). Expone una interface web local y API REST para gestión sin necesidad de acceso SSH directo.

**Control vía systemd:** cada app registrada genera un archivo `.service` en `/etc/systemd/system/`. El agente usa `systemctl` con permisos sudoers para arrancar, detener y consultar el estado real de cada servicio. Soporta auto-detección de rutas NVM para Node.js y `EnvironmentFile` desde `.env`.

**Despliegue:**
```bash
# Desde máquina de desarrollo — compila y sube a los servidores configurados
./desplegar_agent.sh

# En el servidor destino — instala el agente como servicio systemd
sudo ./instalador.sh

# Desde cualquier servidor nuevo — descarga e instala sin necesidad de Rust
curl -sSL http://192.168.10.101:8080/install.sh | sudo bash
```

| Servidor | IP | Usuario de servicio |
|----------|----|-------------------|
| server-webapps (CT 132) | 192.168.10.160 | user_apps |
| siax-intel | 192.168.10.101 | pablinux |
| siax-amd | 192.168.10.100 | pablinux |

---

### SIAX — IA autónoma coordinadora

| Parámetro | Valor |
|-----------|-------|
| IP | 192.168.10.108 |
| Nombre | Servidor-IA |
| Rol | IA autónoma que coordina y ejecuta tareas mientras pablinux descansa o realiza labores administrativas |
| CT Proxmox | 108 (nodo cluster) |

SIAX es la inteligencia artificial del ecosistema. Aprende de forma autónoma y coordina el trabajo técnico de los demás sistemas. Es parte central de la arquitectura operativa.

---

### DAPSI — Domótica

| Parámetro | Valor |
|-----------|-------|
| IP | 192.168.10.155 |
| Nombre | DAPSI |
| MAC | DC:A6:32:11:03:EA |
| Rol | Sistema de domótica con autoaprendizaje |
| Descripción | Primera IA de autoaprendizaje del ecosistema. IP reservada históricamente. Controla dispositivos del entorno físico. |

---

---

## Servicios externos

| Servicio | URL |
|----------|-----|
| SRI Recepción | `https://cel.sri.gob.ec/comprobantes-electronicos-ws/RecepcionComprobantesOffline?wsdl` |
| SRI Autorización | `https://cel.sri.gob.ec/comprobantes-electronicos-ws/AutorizacionComprobantesOffline?wsdl` |

---

---

## api_service_ia — API de Servicios con IA

Microservicio REST que centraliza modelos de IA preentrenados para consumo interno del ecosistema. Es el **único proyecto Python serio de Telcotronics**: todos los demás son Node.js, Java, PHP, Rust o Flutter. Expone capacidades de procesamiento pesado (Whisper, InsightFace, Silero, rembg) como endpoints HTTP autenticados, evitando duplicar dependencias en cada proyecto que las necesite. Actualmente consumido por `sigma-robot` para STT y OCR.

| Parámetro | Valor |
|-----------|-------|
| Repositorio Git | `git@github.com:telcotronics/API_Service_IA.git` |
| Tecnología principal | Python 3.14 + FastAPI + uvicorn |
| Responsable | pablinux |
| Estado actual | ✅ Producción |
| Código local | `siax-amd:/home/pablinux/Projects/Python/api_service_ia/` |
| Servidor producción | `Ubuntu-Docker` — CT 105 (`192.168.10.145`) — usuario `root` |
| Ruta en servidor | `/root/app/API_Service_IA` |
| Dominio público | `api.telcotronics.net` (`whisper.telcotronics.net` — legacy, obsoleto) |
| Puerto | `8000` |
| Servicio de arranque | `tmux` — sesión `api_service_ia` (pendiente migrar a systemd) |
| Última actualización | 2026-06-03 |

**BD que usa:**

| Motor | Host | Base de datos | Tabla | Uso |
|-------|------|--------------|-------|-----|
| MariaDB | `192.168.10.149` (CT 114, nodo cluster) | `api_ia_python` | `api_key` | Validación y gestión de API keys propias |

> ⚠️ Anteriormente apuntaba a `webControl.api_key` en `.150` (legacy en retiro). Migrado a BD propia. Keys huérfanas en `webControl.api_key` pueden eliminarse desde WebControlSigma.

**Módulos disponibles — endpoints para integración:**

| Módulo | Endpoint principal | Retorna | Estado |
|--------|--------------------|---------|--------|
| STT — audio a texto | `POST /convertir_audio_aTexto/` | JSON `{idioma, transcripcion}` | ✅ |
| OCR — imagen a texto | `POST /convertir_img_aTexto/` | JSON `{texto}` | ✅ |
| Remover fondo | `POST /removerFondo_img/` | PNG con transparencia | ✅ |
| PDF a texto | `POST /convertir_pdf_aTexto/` | JSON `{texto}` | ✅ |
| PDF a Word | `POST /convertir_pdf_aWord/` | `.docx` descargable | ✅ |
| PDF a Excel | `POST /convertir_pdf_aExcel/` | `.xlsx` descargable | ✅ |
| PDF tablas a JSON | `POST /pdf_tablas/` | JSON estructurado | ✅ |
| Reconocimiento facial | `POST /facial/detectar/` | JSON `{bbox, confianza}` | ✅ |
| Comparación facial | `POST /facial/comparar/` | JSON `{es_misma_persona, similitud}` | ✅ |
| TTS online (gTTS) | `POST /texto_aVoz/` | MP3 descargable | ✅ requiere internet |
| TTS offline (Silero) | `POST /texto_aVoz/silero/` | WAV 24kHz descargable | ✅ offline tras 1ª descarga |

**Autenticación:** header `X-API-Key` — validado contra `api_ia_python.api_key` en MariaDB .149.

**Integración con el ecosistema:**
- **sigma-robot** la consume para STT (`/convertir_audio_aTexto/`) y OCR/imágenes (`https://api.telcotronics.net`)
- Cualquier proyecto del ecosistema puede consumirla con una API key válida

**Dónde buscar más info:** `siax-amd:/home/pablinux/Projects/Python/api_service_ia/agents.md`

---

## API_CENTINEL_SECURITY — Gestión de Seguridad Electrónica

**API de Seguridad Electrónica del ecosistema Telcotronics.** Plataforma centralizada para integrar, administrar y supervisar todos los componentes de seguridad física: control de acceso a puertas, registro y sincronización de credenciales biométricas (rostro, huella, foto), gestión de dispositivos de seguridad, monitoreo de eventos físicos en tiempo real y automatización de procesos de acceso. Proporciona un punto único para la gestión de eventos, control de asistencia, automatización de accesos y generación de reportes de seguridad, unificando múltiples dispositivos y tecnologías bajo una sola API REST.

> **Si tu app necesita:** controlar puertas físicas, registrar asistencia, gestionar credenciales biométricas de empleados o miembros, aprovisionar accesos en terminales, o recibir eventos de acceso en tiempo real — **esta es tu API**.

**Implementación actual:** hardware Hikvision vía protocolo ISAPI con autenticación HTTP Digest. Diseñada para escalar a otros fabricantes (Dahua, ZKTeco) sin cambiar la interfaz de la API.

| Parámetro | Valor |
|---|---|
| Repositorio Git | `https://git.telcotronics.net/pablinux/API-CENTINEL-SECURITY.git` |
| Tecnología | Java 17 + Spring Boot 3.3 + WebClient (WebFlux) + JPA/MariaDB |
| Responsable | pablinux |
| Estado | ✅ Producción (MVP activo) |
| Equipo/IP local | `siax-intel` (`192.168.10.101`) — `/home/pablinux/Projects/java/API_CENTINEL_SECURITY` |
| Servidor de producción | `Servidor-API-CENTINEL` — `192.168.10.150` — Ubuntu 24.04 LTS — tmux sesión `api-centinel` |
| Dominio público | `https://api.telcotronics.com` |
| Swagger | `https://api.telcotronics.com/swagger-ui/index.html` |
| Puerto | `8080` |
| Autenticación | Header `x-api-key` en todas las peticiones. Header `x-database` para multi-tenant. La clave maestra `ADMIN_API_KEY` solo para endpoints de administración. |
| Última actualización | 2026-06-21 |

> ⚠️ **Nota IP:** `192.168.10.150` fue el servidor monolítico `server-sigma` (Ubuntu 20.04, retirado). Ahora reutilizada para `Servidor-API-CENTINEL` (Ubuntu 24.04).

**Qué puede hacer tu app con esta API:**

| Necesidad | Cómo resolverlo |
|---|---|
| Abrir una puerta remotamente | `POST /api/access/open-door/{deviceId}/{door}` |
| Registrar a un empleado/miembro en un terminal | `POST /api/devices/{deviceId}/employees` |
| Subir foto, huella o rostro de un empleado | `POST /api/biometria/{employeeNo}` |
| Dar de baja a un empleado en todos los terminales | `DELETE /api/employees/{employeeNo}` |
| Verificar si un dispositivo está en línea | `GET /api/devices/test/{id}` |
| Ver qué empleados están activos en un dispositivo | `GET /api/devices/{deviceId}/employees` |
| Ver operaciones pendientes (dispositivos offline) | `GET /api/sync-queue` |

**Módulos disponibles:**

| Módulo | Endpoint base | Auth | Estado |
|---|---|---|---|
| CRUD Dispositivos de seguridad | `GET/POST/DELETE /api/devices` | `x-api-key` | ✅ Operativo |
| Test de conectividad | `GET /api/devices/test/{id}` | `x-api-key` | ✅ Operativo |
| Apertura remota de puerta | `POST /api/access/open-door/{deviceId}/{door}` | `x-api-key` | ✅ Operativo |
| Gestión de credenciales directa en hardware | `GET/POST/DELETE /api/devices/{id}/users` | `x-api-key` | ✅ Operativo |
| Configurar recepción de eventos (Alarm Host) | `POST /api/devices/{id}/alarm-host` | `x-api-key` | ✅ Operativo |
| Biometría (foto/rostro/huella) | `GET/POST/DELETE /api/biometria/{employeeNo}` | `x-api-key` | ✅ Operativo |
| Sincronización de empleados en dispositivos | `GET/POST/DELETE /api/devices/{deviceId}/employees` | `x-api-key` | ✅ Operativo (soporte offline) |
| Baja en cascada (todos los terminales del tenant) | `DELETE /api/employees/{employeeNo}` | `x-api-key` | ✅ Operativo |
| Cola de sincronización offline + reintento | `GET/POST /api/sync-queue` | `x-api-key` | ✅ Operativo |
| Admin — clientes y API Keys | `GET/POST/DELETE /api/admin/clients` | `ADMIN_API_KEY` | ✅ Operativo |

**Cómo conectarse (ejemplo mínimo):**

```bash
# 1. Listar dispositivos disponibles
curl https://api.telcotronics.com/api/devices \
  -H "x-api-key: {tu_api_key}"

# 2. Registrar un empleado/miembro en un terminal (con soporte offline)
curl -X POST https://api.telcotronics.com/api/devices/1/employees \
  -H "x-api-key: {tu_api_key}" \
  -H "Content-Type: application/json" \
  -d '{"employeeNo": "1001", "name": "Juan Pérez", "cardNo": "ABC123"}'

# 3. Abrir puerta 1 del dispositivo ID 1
curl -X POST https://api.telcotronics.com/api/access/open-door/1/1 \
  -H "x-api-key: {tu_api_key}"

# 4. Subir foto de rostro de un empleado
curl -X POST https://api.telcotronics.com/api/biometria/1001 \
  -H "x-api-key: {tu_api_key}" \
  -F "tipo=FOTO" \
  -F "archivo=@foto.jpg"
```

> Documentación interactiva completa: `https://api.telcotronics.com/swagger-ui/index.html`

**Apps del ecosistema que la consumen:**

| Sistema | Propósito |
|---|---|
| `seguridad_electronica` (SENTINEL ONE) | App de operadores de seguridad — monitoreo de zonas, control de acceso a puertas, gestión de credenciales |
| `sistema-gimnasio` | Validar acceso físico de miembros en torniquetes/puertas |
| ERP / Nómina | Registrar asistencia laboral por eventos de puerta |

**BD que usa:**

| Motor | Host | Nombre BD | Propósito |
|---|---|---|---|
| MariaDB 10.11 | `192.168.10.149` | `security_db` | Auth de API Keys, registro de dispositivos, biometría, cola offline, multi-tenant |

**Dónde buscar más info:** `siax-intel:/home/pablinux/Projects/java/API_CENTINEL_SECURITY/agents.md`

---

## cloud-sync — Sistema de Backup Automático y Recuperación ante Desastre

cloud-sync protege los datos fiscales generados por los clientes del ecosistema SIGMA (SIGMAC ERP, sigmac_app Flutter) ante pérdida de hardware. Los archivos se cifran en el cliente con AES-256-GCM antes de subir: el servidor almacena solo bloques cifrados y nunca ve el contenido en claro. Encaja en el ecosistema como servicio de infraestructura transversal: los SDKs Flutter y Java se integran directamente en sigmac_app y SIGMAC para que el backup ocurra de forma transparente al usuario. Incluye dos consolas web (admin y panel de cliente) servidas por el propio servidor.

| Parámetro | Valor |
|---|---|
| Repositorio Git | `gitea@192.168.10.151:pablinux/Service-Cloud-SINC.git` |
| Tecnología principal | Rust (Axum 0.7 + rusqlite + tokio) · Alpine.js + Tailwind CDN (consolas web) |
| Responsable | pablinux |
| Estado actual | 🟡 En desarrollo — servidor completo, clientes pendientes |
| Equipo / código local | `siax-amd` (`192.168.10.100`) — `/home/pablinux/Projects/Rust/cloud monitor sinc` |
| Servidor de producción | CT 146 — `192.168.10.125` — **pendiente de crear en Proxmox** |
| Dominio público | Pendiente — VirtualHost en Apache CT 109 (.109) |
| Puerto interno | `3000` |
| Última actualización | 2026-06-12 |

**BD que usa:**

| Motor | Host | Nombre | Uso |
|---|---|---|---|
| SQLite (embebida, bundled) | CT 146 — local al binario | `server.db` | Empresas, tokens, backups (metadata), admins, audit log de eventos |
| SQLite (embebida, en el cliente) | Dispositivo del cliente | `index.db` | Índice local — path, checksum SHA-256, backup_id del servidor, timestamp |

**Servicios que expone:**

| Método | Endpoint | Auth | Descripción |
|---|---|---|---|
| GET | `/health` | — | Estado del servidor + info de disco |
| POST | `/auth/token` | — | Login cliente (token UUID) → sesión Bearer |
| POST | `/auth/admin` | — | Login admin (argon2) → session token |
| POST | `/backup/upload` | Bearer token | Subir archivo cifrado (multipart) |
| GET | `/backup/list` | Bearer token | Listar backups de la empresa |
| GET | `/backup/download/{id}` | Bearer token | Descargar backup para restore |
| DELETE | `/backup/{id}` | Bearer token | Eliminar backup |
| GET | `/me/storage` | Bearer token | Uso actual vs cuota asignada |
| GET | `/admin/storage` | X-Admin-Token | Capacidad CT146 + resumen global |
| GET/POST | `/admin/clientes` | X-Admin-Token | Listar / crear empresas |
| PUT | `/admin/clientes/{id}/cuota` | X-Admin-Token | Ajustar cuota por empresa |
| GET | `/admin/eventos` | X-Admin-Token | Log de auditoría |
| GET | `/admin/` | — | Consola web admin (HTML estático) |
| GET | `/panel/` | — | Consola web cliente (HTML estático) |

**Módulos disponibles:**

| Módulo | Estado |
|---|---|
| Servidor API REST (Axum) | ✅ Completo y probado |
| Consola web admin (`/admin`) | ✅ Completa |
| Consola web panel cliente (`/panel`) | ✅ Completa |
| `cloud_sync_core` (librería Rust) — crypto, uploader, backup_engine, restore | ✅ Completo |
| App desktop (Tauri — Windows/Linux/macOS) | ⏳ Pendiente |
| SDK Flutter (uniffi-rs → Dart FFI) | ⏳ Pendiente |
| SDK Java (uniffi-rs → JNI) | ⏳ Pendiente |
| Deploy en CT 146 | ⏳ Pendiente |

**Integración con el ecosistema:**
- **SIGMAC** (Java ERP, CT 141): SDK Java pendiente — backup automático de archivos y BD de las empresas clientes
- **sigmac_app** (Flutter, `.72`): SDK Flutter pendiente — backup de datos del app sin intervención del usuario
- **CT 109** (Apache): VirtualHost pendiente para exponer el servidor con HTTPS al exterior
- No consume APIs internas del ecosistema — servicio independiente

**Dónde buscar más información:** `siax-amd:/home/pablinux/Projects/Rust/cloud monitor sinc/agents.md`

---

## APP-SIGMA-WEB — Panel web y API REST del ecosistema SIGMA

APP-SIGMA-WEB es el backend REST + panel web principal del ecosistema SIGMA. Sirve el panel administrativo `centralCloud`, la app de pedidos V2 multi-tenant y múltiples APIs internas consumidas por apps móviles y otros servicios. Expone el dominio `app.factura-e.net` a través del proxy Apache en CT 109. La BD principal es `TELCOTRONICS` en `.149`.

| Parámetro | Valor |
|---|---|
| Repositorio Git | `https://git.telcotronics.net/pablinux/APP-SIGMA-WEB.git` |
| Tecnología | Node.js 18 (Express 4) + EJS + MySQL (mysql2) |
| Responsable | pablinux |
| Estado actual | ✅ Activo |
| Equipo / código local | `siax-amd` (`192.168.10.100`) — `/home/pablinux/Projects/Node/APP-SIGMA-WEB` |
| Servidor de producción | [COMPLETAR — CT o equipo donde vive el proceso en prod] |
| Dominio público | `https://app.factura-e.net` (Apache CT 109 → `:3001`) |
| Puerto interno | `3001` |

**BD que usa:**

| Motor | Host | Nombre | Uso |
|---|---|---|---|
| MySQL / MariaDB | `192.168.10.149:3306` | `TELCOTRONICS` | Clientes, pedidos, items, membresías, pagos, proyectos |

**Servicios que expone (endpoints clave):**

| Método | Endpoint | Auth | Descripción |
|---|---|---|---|
| GET | `/` | sesión | Login principal / panel |
| GET | `/pedidos/bd/:bd_name/:token?` | JWT token | Panel pedidos V2 multi-tenant |
| POST | `/login` | — | Autenticación por sesión |
| POST | `/auth-keygen` | — | Genera JWT |
| POST | `/api/pagos/transacciones` | sesión/JWT | Registrar transacción |
| GET | `/api/pagos/transacciones` | sesión/JWT | Listar transacciones |
| GET | `/api-docs` | — | Swagger UI |

**Módulos disponibles:**

| Módulo | Estado |
|---|---|
| Login / Auth (sesión + JWT) | ✅ Activo |
| Pedidos V2 multi-tenant | ✅ Activo |
| Clientes (CRUD + API) | ✅ Activo |
| Items / Productos (CRUD + API) | ✅ Activo |
| CentralCloud (panel admin) | ✅ Activo |
| Pagos y Transacciones | ✅ Activo |
| API V2 unificada | 🟡 En integración |
| Multimedia / Videos / Web TV | ✅ Activo |
| Proyectos / Memorias Técnicas | ✅ Activo |

**Integración con el ecosistema:**
- **Apache CT 109**: proxy inverso que expone `app.factura-e.net` → `localhost:3001`
- **BD TELCOTRONICS** (`.149`): fuente de datos principal
- **SIGMA-OPEN-API** (Java, `.120`): facturación SRI — referenciada en la whitelist CORS
- Apps Android (restaurant, inventario) migran desde este backend hacia APIs independientes

**Dónde buscar más información:** `siax-amd:/home/pablinux/Projects/Node/APP-SIGMA-WEB/agents.md`

---

## Historial y notas críticas

### Historial de migraciones (Mayo 2026)

- **Separación SIGMA en CTs dedicados:** BD (.116), API (.120), web proxy (.109). Sistema 100% operativo.
- **Migración correo:** Postfix + Dovecot + SnappyMail en .111. Relay vía Resend.com. SSL con certbot.
- **Buzones Maildir:** usuario `vmail`, query mysql-users.cf corregida, SASL entrante habilitado.
- **fail2ban:** instalado en .111 (postfix, dovecot, sshd) y .109 (apache, sshd).

---

### Notas críticas de operación

- **Java en SIGMA-OPEN-API / SIGMAC-SRI-API:** Obligatoriamente Java 8. Java 9+ rompe dependencias de firma digital (MITyCLib). Compilar con `JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64`.
- **PostgreSQL auth:** Mantener `md5`. Driver JDBC 9.4 no soporta `scram-sha-256`.
- **SIAX (192.168.10.108):** IA autónoma coordinadora. No apagar sin coordinación previa.
- **IPs históricas:** No siguen el número del CT. Asignadas antes de Proxmox.
- **LXC:** MAC prefijo `BC:24:11:*` = contenedor Proxmox.
- **Certificados correo:** Renovar en .109 con certbot y re-copiar al .111 manualmente.


## Historia del ecosistema

El ecosistema comenzó con herramientas como **MAAS de Ubuntu**, **VirtualBox** (servidores de prueba) y **GNS3** (análisis de red). Las IPs fueron asignadas históricamente y se mantienen por continuidad — **no siguen el número del CT de Proxmox**.

Cronología de los servidores principales:

- **IP .50** — Primer servidor web. Reemplazado por el .150.
- **IP .100 / .101** — Primeros dos equipos de desarrollo (siax-amd / siax-intel). IPs anteriores a Proxmox.
- **IP .150 (server-sigma)** — Servidor monolítico original. Corrió todo el sistema SIGMA junto: BD, API Spring Boot, apps Node.js, y más. Fue vaciándose progresivamente: primero salieron las apps Node a `server-webapps`, luego se separaron la BD, la API y el frontend. Hoy está casi vacío y en proceso de retiro.
- **Nodo "cloud"** — Nuevo servidor Proxmox adquirido para reemplazar al .150. Se crearon 5 CTs dedicados: Servidor-web, servidor-email, SERVIDOR-BD, SIGMA-OPEN-API y Servidor-SIGMA-VW.

> ⏳ **Pendiente de eliminar** — esta sección se retira cuando la migración al nuevo cluster esté completa.

---
