# 2. Herramientas, aplicaciones, lenguajes, hardware y servicios TI

> **Entregable 2 — Evaluación Sumativa 2 (ES2), Unidad 2 (Desarrollo e Implementación)**
> **Proyecto:** SGSI — Sistema de Gestión de Seguridad de la Información
> **Mandante:** Hospital Félix Bulnes Cerda (Miguel Godoy, Encargado de Ciberseguridad)
> **Criterio evaluado:** `2.1.1.2` — Descripción de herramientas, aplicaciones, lenguajes,
> componentes de hardware y servicios TI requeridos para el desarrollo del proyecto.

Este documento detalla los **lenguajes**, **herramientas de desarrollo y modelado**, **aplicaciones**
(módulos de la solución y aplicaciones externas), **componentes de hardware** y **servicios TI**
necesarios para construir y operar el SGSI, conforme a la selección tecnológica justificada en el
Entregable 1.

---

## 2.1 Lenguajes de programación

| Lenguaje | Uso | Justificación |
|---|---|---|
| **Python 3.14** | Backend (API REST, lógica de negocio) | Tipado y ecosistema para desarrollo web seguro; base de FastAPI y SQLAlchemy. |
| **TypeScript 5.7** | Frontend (tipado de la SPA) | Detección de errores en compilación, mantenibilidad y soporte nativo de React. |
| **HTML5 + CSS3** | Estructura y estilos de la interfaz | Base de toda interfaz web; estilos propios en `styles.css`. |
| **SQL** | Consultas y modelo de datos | Lenguaje estándar para PostgreSQL/SQLite vía SQLAlchemy ORM. |
| **JSON** | Intercambio de datos API | Formato de los endpoints REST y de los tokens JWT. |

---

## 2.2 Frameworks y bibliotecas (stack técnico)

### Backend

| Componente | Versión | Rol |
|---|---|---|
| **FastAPI** | actual | Framework web asíncrono; generación automática de OpenAPI/Swagger. |
| **Uvicorn** (standard) | actual | Servidor ASGI que ejecuta la aplicación FastAPI (puerto 8000). |
| **SQLAlchemy** | actual | ORM: mapeo de modelos a la base de datos (SQLite/PostgreSQL). |
| **Pydantic** | (incluido en FastAPI) | Validación de esquemas de entrada/salida (`schemas.py`). |
| **PyJWT** | actual | Emisión y verificación de tokens JWT (HS256). |
| **passlib/PBKDF2** | actual | Hash de contraseñas para autenticación segura. |
| **python-multipart** | actual | Carga de archivos (evidencias y adjuntos de tickets) vía `multipart/form-data`. |
| **Validación de adjuntos** (Pydantic + utilidades estándar) | según stack existente | Lista blanca de extensiones y tipos MIME, tamaño máximo aproximado de 10 MB, nombre seguro y rechazo de formatos no permitidos; escaneo antivirus recomendado. |
| **smtplib** (biblioteca estándar) / **aiosmtplib** (opcional) | estándar / opcional | Envío de avisos mediante el servicio de notificaciones con relay SMTP institucional; mantener credenciales en configuración protegida (`SGSI_SMTP_*`). |
| **slowapi** (opcional) | opcional | Rate limiting de endpoints públicos; Nginx `limit_req` es una alternativa de infraestructura. |
| **psycopg** | (al desplegar PostgreSQL) | Driver para conectar `postgresql+psycopg://` en producción. |

### Frontend

| Componente | Versión | Rol |
|---|---|---|
| **React** | 18.3 | Librería de interfaz de usuario (componentes y estado). |
| **react-dom** | 18.3 | Renderizado de React en el navegador. |
| **react-router-dom** | 6.30 | Enrutamiento de páginas (Login, Dashboard, Controles, Usuarios, Tickets y formulario público `/reportar`). |
| **Recharts** | 2.15 | Gráficos de barras y torta para el dashboard de madurez. |
| **Vite** | 6.2 | Herramienta de build y servidor de desarrollo (puerto 5173, proxy `/api` → 8000). |
| **@vitejs/plugin-react** | 4.3 | Soporte de JSX/TSX en Vite. |
| **TypeScript** | 5.7 | Compilador/verificador de tipos (`tsc --noEmit`). |

---

## 2.3 Herramientas de desarrollo

| Herramienta | Propósito | Alternativa libre |
|---|---|---|
| **VS Code** | Editor/IDE principal (backend + frontend) | — |
| **Git + GitHub** | Control de versiones y repositorio del proyecto | GitLab |
| **Python (venv)** | Entorno virtual para aislar dependencias del backend | uv / Poetry |
| **pip** | Gestor de paquetes de Python (`requirements.txt`) | uv |
| **Node.js + npm** | Ejecutar Vite y gestionar dependencias del frontend | pnpm |
| **Postman / Swagger UI** | Probar la API REST (`/docs` ya lo incluye FastAPI) | cURL, Insomnia |
| **DBeaver** | Explorar/administrar la base de datos (SQLite/PostgreSQL) | pgAdmin |
| **Docker** (opcional) | Contenerizar backend/frontend para despliegue reproducible | Podman |

---

## 2.4 Herramientas de modelado y documentación

| Herramienta | Uso en el proyecto |
|---|---|
| **Draw.io / diagrams.net** | Diagramas BPMN, UML (casos de uso, componentes), topología, infraestructura y arquitectura. |
| **PlantUML** (opcional) | Generar diagramas UML a partir de texto versionable. |
| **Mermaid** | Diagramas embebidos en la documentación Markdown. |
| **Microsoft Word / Markdown** | Informes y documentación (plantilla ABPro, checklist ES2). |
| **Microsoft Project / Planner** (o Excel) | Carta Gantt y seguimiento del cronograma. |

---

## 2.5 Aplicaciones

### 2.5.1 Aplicación a desarrollar (módulos del SGSI)

| Módulo | Funcionalidad |
|---|---|
| **Autenticación y roles (transversal)** | Login JWT y control RBAC de cinco roles: `encargado`, `admin_contratos`, `referente_tecnico`, `director` y `admin_sistema`. El último administra usuarios, pero no ve tickets ni datos de negocio; no se contabiliza como módulo de negocio. |
| **Controles ISO/IEC 27001 (módulo 1)** | Catálogo de controles del Anexo A por dominio y estado. |
| **Evidencias (módulo 2)** | Carga y gestión de respaldos asociados a controles, con acceso restringido por rol. |
| **Madurez del SGSI** | Cálculo y visualización del % de madurez por dominio y global (gráficos). |
| **Incidentes** | Registro y clasificación según taxonomía ANCI; cómputo de plazos legales (3 h / 72 h / 15 días). |
| **Terceros / Proveedores** | Contratos y checklist de cláusulas de seguridad con estado de cumplimiento. |
| **Controles de Personas** | Ciclo de vida del personal (capacitación, antecedentes, confidencialidad, término). |
| **Reportería** | Resumen ejecutivo y exportación a CSV (compatible con Excel). |
| **Usuarios (módulo 8)** | CRUD de cuentas, asignación de rol, restablecimiento de contraseña, habilitación/deshabilitación lógica y auditoría; exclusivo de `admin_sistema`. |
| **Ticketera (módulo 9)** | Formulario público `/reportar` sin autenticación, denuncias/reportes anónimos, adjuntos validados, bandeja confidencial para `encargado`, notificaciones y derivación a incidentes. |

**Conteo del alcance:** 9 módulos funcionales (controles, evidencias, madurez, incidentes, terceros, personas, reportería, usuarios y ticketera) y 5 roles RBAC. El formulario público no recoge ni registra identidad, IP, user-agent o token del emisor; queda accesible por HTTPS en la red interna del hospital y protegido contra abuso.

### 2.5.2 Aplicaciones de apoyo y externas

| Aplicación | Relación con la solución |
|---|---|
| **Swagger UI** (FastAPI `/docs`) | Documentación interactiva y pruebas de la API. |
| **Navegador web** (Chrome/Edge/Firefox) | Cliente de la SPA para usuarios finales. |
| **Trakcare** (InterSystems) | Sistema clínico externo; el SGSI **no se integra en línea**, solo lo referencia como dato descriptivo del sistema/módulo afectado en un incidente. |
| **Microsoft Excel / LibreOffice** | Consumo de los reportes CSV exportados por el SGSI. |
| **Mesa de ayuda interna + InterSystems** | Soporte operativo externo al que el SGSI se alinea en horarios (no es dependencia técnica directa). |

---

## 2.6 Componentes de hardware

> **Nota:** las capacidades de producción son una **propuesta referencial**; el hospital validará el
> dimensionamiento final según su política de infraestructura. El desarrollo puede realizarse
> íntegramente en los equipos portátiles del equipo.

### Entorno de desarrollo (por integrante)

| Componente | Especificación mínima |
|---|---|
| Equipo portátil/estación | CPU x86-64/ARM64, 4 núcleos |
| Memoria RAM | 8 GB |
| Almacenamiento | SSD 256 GB (código + evidencias de prueba) |
| Red | Conexión a Internet (descarga de dependencias y Git) |

### Entorno de producción (propuesta referencial)

| Componente | Especificación | Observación |
|---|---|---|
| Servidor de aplicaciones | 2 vCPU, 4 GB RAM, 40 GB SSD | Ejecuta FastAPI (uvicorn) + sirve la SPA compilada. |
| Servidor de base de datos | 2 vCPU, 4 GB RAM, 100 GB SSD (RAID) | PostgreSQL con respaldo; puede convivir con el de aplicaciones en fase piloto. |
| Almacenamiento de evidencias y adjuntos | 100+ GB | NAS/repositorio; evidencias y tickets en carpetas separadas (por ejemplo, `/evidencias/tickets/`) con permisos restringidos. |
| Red local / DMZ | Conmutador + firewall | Aislamiento de la zona del SGSI respecto de la red clínica. |
| Respaldo | Disco externo/NAS o almacenamiento en nube | Copias periódicas de BD y evidencias (plan de continuidad, Entregable 14). |

---

## 2.7 Servicios TI

| Servicio | Descripción |
|---|---|
| **Hosting / despliegue** | Servidor propio del hospital o nube (IaaS) para backend y frontend compilado. |
| **Dominio y DNS** | Nombre institucional del SGSI y resolución DNS interna/externa. |
| **Certificado TLS/HTTPS** | Cifrado en tránsito de credenciales y datos del SGSI. |
| **Respaldo (backup)** | Copias automáticas de base de datos y evidencias, con retención definida. |
| **Monitoreo** | Vigilancia de disponibilidad y errores del servicio (logs, health check `/api/health`). |
| **Gestión de usuarios y roles** | Gobierno de cuentas y asignación RBAC de 5 roles; el CRUD del SGSI corresponde exclusivamente a `admin_sistema`. |
| **Mesa de ayuda / soporte** | Soporte a usuarios del SGSI dentro del horario institucional. |
| **Correo institucional / relay SMTP** | Servicio **requerido** para habilitar avisos por correo al equipo de ciberseguridad; TI provee relay, cuenta y parámetros SMTP. El mensaje contiene solo código, tipo, severidad y enlace; ante una falla, el ticket se crea y queda en la bandeja interna. |
| **Protección del formulario público** | HTTPS en red hospitalaria, límites de solicitudes, validación de entradas y adjuntos y logs sin datos que identifiquen al emisor. |
| **Gestión de cambios y configuraciones** | Procedimientos de actualización controlada de la aplicación (Entregable 15). |

---

## 2.8 Resumen consolidado

| Categoría | Selección |
|---|---|
| Lenguajes | Python 3.14, TypeScript, HTML/CSS, SQL, JSON |
| Backend | FastAPI + Uvicorn + SQLAlchemy + Pydantic + PyJWT + PBKDF2 |
| Frontend | React 18 + TypeScript + Vite + Recharts + React Router |
| Base de datos | PostgreSQL (producción) / SQLite (desarrollo) vía SQLAlchemy |
| Herramientas | VS Code, Git/GitHub, venv/pip, Node/npm, Swagger UI, DBeaver, Draw.io, Mermaid |
| Hardware | Equipos de desarrollo (8 GB RAM/SSD) + servidores referenciales de producción |
| Servicios TI | Hosting, DNS, TLS, respaldo, monitoreo, mesa de ayuda, gestión de usuarios/cambios y relay SMTP institucional requerido para correo |
| Alcance funcional | 9 módulos y 5 roles RBAC; CRUD Usuarios exclusivo de `admin_sistema`, tickets visibles y gestionables solo por `encargado` |
| Librerías/controles nuevos | `smtplib` estándar o `aiosmtplib` opcional, `slowapi` opcional, validación de extensión/MIME/tamaño de adjuntos |
