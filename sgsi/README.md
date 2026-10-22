# SGSI — Sistema de Gestión de Seguridad de la Información

Aplicación web de tipo **GRC (Governance, Risk & Compliance)** para el **Hospital Félix Bulnes
Cerda**, construida a partir del informe de formulación del proyecto de título
(`Documentacion/Entregas/U1-Formulacion-Proyecto/borrador_informe_formulacion.md`).

Centraliza la gestión del SGSI en un único sistema auditable, con visualización del nivel de
madurez de los controles ISO/IEC 27001 y la gestión de incidentes de ciberseguridad conforme a la
Ley N.º 21.663 (taxonomía ANCI y plazos legales de reporte).

## Módulos

| Módulo | Descripción |
|---|---|
| **Controles ISO/IEC 27001** | Catálogo de controles del Anexo A por dominio (organizacional, personas, físico, tecnológico), estado (no iniciado / iniciado / implementado / gestionado) y evidencias adjuntas. |
| **Madurez del SGSI** | Cálculo automático del % de madurez por dominio y global, con gráficos (barras y torta). |
| **Incidentes** | Registro y clasificación según taxonomía ANCI, cómputo automático de plazos legales (alerta temprana 3 h; reporte 72 h para severidad alta/crítica, 15 días para media/baja) y alerta de vencimiento. |
| **Terceros / Proveedores** | Registro de contratos con checklist de cláusulas de seguridad y estado de cumplimiento. |
| **Controles de Personas** | Ciclo de vida del personal: capacitación, antecedentes, condiciones de empleo, disciplinario, término de contrato y confidencialidad. |
| **Reportería** | Resumen ejecutivo y exportación a CSV (compatible con Excel) para sustentar el indicador de gestión y auditorías. |
| **Usuarios** | CRUD de usuarios, asignación de roles, restablecimiento de contraseña, baja lógica de personal desvinculado y auditoría de cambios. Solo `admin_sistema`. |
| **Ticketera** | Denuncias y reportes de incidentes de ciberseguridad enviados por funcionarios mediante un **formulario público, sin autenticación y anónimo** (`/reportar`). Categorías predefinidas + "Otros" (texto libre), adjuntos, código de seguimiento privado, notificación al equipo por correo y/o bandeja interna (a elección del emisor) y conversión del ticket en incidente formal. Gestión por el `encargado`. |

## Stack tecnológico

- **Backend:** Python 3.14 + FastAPI + SQLAlchemy + SQLite (compatible con PostgreSQL vía variable de entorno).
- **Autenticación:** JWT con control de acceso basado en roles (RBAC, 5 roles) y hash de contraseñas PBKDF2.
- **Frontend:** React 18 + TypeScript + Vite + Recharts (gráficos). Identidad visual del Hospital Clínico Félix Bulnes (paleta carmesí/azul institucional, Roboto / Open Sans / Playfair Display) con modo oscuro persistente.
- **Correo:** SMTP opcional para notificar tickets (si no se configura, el envío se simula).

## Estructura del proyecto

```
sgsi/
├── backend/
│   ├── app/
│   │   ├── main.py          # Aplicación FastAPI y rutas raíz
│   │   ├── config.py        # Configuración (BD, JWT, pesos de madurez)
│   │   ├── database.py      # Conexión a BD
│   │   ├── models.py        # Modelos ORM
│   │   ├── schemas.py       # Esquemas Pydantic
│   │   ├── security.py      # Hash de contraseñas y JWT
│   │   ├── deps.py          # Dependencias de auth/roles
│   │   ├── services.py      # Plazos legales y reglas de madurez
│   │   ├── seed.py          # Datos de demostración
│   │   ├── tickets_service.py / notificaciones.py / ratelimit.py  # Ticketera, correo/bandeja, límite de tasa
│   │   └── routers/         # Endpoints por módulo (incl. usuarios, tickets, public_tickets, notificaciones)
│   ├── tests/               # Pruebas (pytest)
│   ├── requirements.txt
│   └── requirements-dev.txt
└── frontend/
    └── src/
        ├── pages/           # Login, Dashboard, Controles, Incidentes, Terceros, Personas, Reportes, Usuarios, Tickets, Reportar (público), SeguimientoTicket (público)
        ├── components/      # Layout, Modal, Badge
        ├── api.ts           # Cliente HTTP con token
        └── constants.ts     # Etiquetas y catálogos
```

## Puesta en marcha

### 1. Backend (puerto 8000)

```bash
cd sgsi/backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m app.seed          # crea la BD y los datos de demostración
uvicorn app.main:app --reload --port 8000
```

### 2. Frontend (puerto 5173)

```bash
cd sgsi/frontend
npm install
npm run dev
```

Abre http://localhost:5173 (el servidor de desarrollo redirige `/api` al backend en el puerto 8000).

### Usuarios de demostración (contraseña: `demo123`)

| Usuario | Rol | Permisos |
|---|---|---|
| `miguel.godoy` | Encargado de Ciberseguridad | Acceso total a módulos de negocio; gestiona la Ticketera y recibe notificaciones |
| `maria.perez` | Administrador de Contratos | Escritura en Terceros; lectura en el resto |
| `juan.rojas` | Referente Técnico | Solo lectura |
| `patricia.silva` | Director/a | Solo lectura |
| `admin.sistema` | Administrador de Sistema | Solo módulo Usuarios (sin acceso a módulos de negocio ni tickets) |

El **formulario público** de reporte está disponible sin iniciar sesión en http://localhost:5173/reportar
(seguimiento por código en `/reportar/seguimiento`).

### Pruebas del backend

```bash
cd sgsi/backend
pip install -r requirements-dev.txt
python -m pytest
```

## Endpoints principales

```
POST   /api/auth/login
GET    /api/auth/me
GET    /api/controles            (filtros: ?dominio=&estado=&search=)
POST   /api/controles
PUT    /api/controles/{id}
DELETE /api/controles/{id}
POST   /api/controles/{id}/evidencias   (multipart)
GET    /api/evidencias/{id}/download
GET    /api/madurez
GET    /api/incidentes           (filtros: ?severidad=&estado=&search=)
POST   /api/incidentes
PUT    /api/incidentes/{id}
GET    /api/terceros             (filtros: ?estado=&search=)
GET    /api/personas             (filtros: ?tipo=&estado=)
GET    /api/reportes/resumen
GET    /api/reportes/{controles,incidentes,terceros,personas}.csv

# Usuarios (solo admin_sistema)
GET/POST          /api/usuarios
PUT               /api/usuarios/{id}
POST              /api/usuarios/{id}/reset-password
POST              /api/usuarios/{id}/deshabilitar | /habilitar
GET               /api/usuarios/auditoria

# Ticketera (solo encargado)
GET               /api/tickets, /api/tickets/resumen
GET/PUT           /api/tickets/{id}
POST              /api/tickets/{id}/convertir-incidente
GET               /api/notificaciones

# Públicos (sin autenticación)
GET    /api/public/tickets/categorias
POST   /api/public/tickets                       (multipart, con límite de tasa)
GET    /api/public/tickets/{codigo_seguimiento}
```

La documentación interactiva (Swagger) está disponible en http://localhost:8000/docs.

## Configuración

Variables de entorno opcionales:

| Variable | Por defecto | Descripción |
|---|---|---|
| `SGSI_DATABASE_URL` | `sqlite:///data/sgsi.db` | Cadena de conexión (ej. `postgresql+psycopg://...`) |
| `SGSI_SECRET_KEY` | clave de desarrollo | Clave para firmar los tokens JWT |
| `SGSI_TOKEN_EXPIRE` | `480` | Validez del token en minutos |
| `SGSI_DATA_DIR` | `backend/data` | Carpeta de datos y evidencias |
| `SGSI_UPLOAD_DIR` | `backend/data/evidencias` | Carpeta base de adjuntos de tickets (`tickets/<código>/`) |
| `SGSI_SMTP_HOST`, `SGSI_SMTP_PORT` (587), `SGSI_SMTP_USER`, `SGSI_SMTP_PASSWORD`, `SGSI_SMTP_FROM`, `SGSI_SMTP_TO`, `SGSI_SMTP_STARTTLS` (1) | sin configurar (envío simulado) | Notificación por correo de tickets (`SGSI_SMTP_TO` admite lista separada por comas; el correo solo incluye código, tipo y severidad) |
| `SGSI_PUBLIC_RATE_LIMIT` | `5/600` | Envíos públicos permitidos por cliente (cantidad/segundos) |
| `SGSI_PUBLIC_LOOKUP_RATE_LIMIT` | `30/600` | Consultas públicas de seguimiento por cliente |
| `SGSI_TRUST_PROXY` | `0` | Usar `X-Forwarded-For` para el límite de tasa tras un proxy (la IP nunca se almacena) |
| `SGSI_APP_URL` | `http://localhost:5173` | URL base usada en los enlaces de las notificaciones |

> Los archivos de evidencia se guardan en `backend/data/evidencias/`.
> **Anonimato:** los tickets públicos no almacenan IP, user-agent ni identidad del emisor; el límite de
> tasa usa un hash con sal aleatoria en memoria. Se recomienda complementar con `limit_req` de Nginx y
> restringir el formulario a la red interna del hospital.
> **PostgreSQL existente:** si el rol es un enum nativo, ejecutar `ALTER TYPE ... ADD VALUE 'admin_sistema'`.

## Notas

- La **madurez** se calcula ponderando cada estado: no iniciado = 0, iniciado = 0.33,
  implementado = 0.67, gestionado = 1.0.
- Los **plazos legales** de incidentes se calculan desde la fecha de detección según la
  Ley 21.663: alerta temprana a las 3 horas; reporte a las 72 horas (severidad alta/crítica) o a
  los 15 días (media/baja).
- La base de datos y los datos de demostración se crean automáticamente al ejecutar `app.seed`.
  Para reiniciar los datos, borra `backend/data/sgsi.db` y vuelve a ejecutar el seed.
