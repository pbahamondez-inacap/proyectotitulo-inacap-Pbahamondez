# 15. Plan de mantención

> **Entregable 15 — Evaluación Sumativa 2 (ES2), Unidad 2 (Desarrollo e Implementación)**
> **Proyecto:** SGSI — Sistema de Gestión de Seguridad de la Información
> **Mandante:** Hospital Félix Bulnes Cerda (Miguel Godoy, Encargado de Ciberseguridad)
> **Criterio evaluado:** `2.1.5.15` — Procedimiento para control de cambios en configuración, cambios
> en entregables y gestión de incidentes.

Este plan cubre las tres prácticas de mantención del servicio: **gestión de configuración**,
**gestión de cambios** y **gestión de incidentes**.

---

## 15.1 Gestión de configuración

### Objetivo
Mantener el inventario y la línea base de los elementos de configuración (CI) del SGSI, para conocer
qué se ejecuta, dónde y en qué versión.

### Elementos de configuración (CI)

| CI | Descripción | Identificación |
|---|---|---|
| Código fuente (backend/frontend) | Repositorio Git | Tag/versión (ej. `v1.0.0`) |
| Base de datos | Esquema y datos | Versión de esquema (migraciones) |
| Servidor de aplicaciones | APP-01 (Nginx + Uvicorn) | Configuración versionada |
| Servidor de BD | DB-01 (PostgreSQL) | Configuración versionada |
| Almacenamiento | NAS-01 (evidencias y adjuntos de tickets) | Rutas separadas y permisos restringidos; `/evidencias/tickets/` |
| Relay SMTP | Correo institucional saliente | Host/puerto y estado del servicio, sin secretos en la línea base |
| Servicio de notificaciones | Correo SMTP y bandeja interna | Configuración `SGSI_SMTP_*`, estados de envío y reintentos |
| Formulario público | Ruta `/reportar`, endpoint público y reglas de Nginx | HTTPS, rate limiting y logs anonimizados/deshabilitados para IP del emisor |
| Ambiente de despliegue | Variables de entorno (`SGSI_*`, `SGSI_SMTP_*`) | Archivo/gestor de secretos protegido; valores sensibles excluidos de Git |

### Proceso

1. Registrar cada CI con su identificador y responsable.
2. Mantener la **línea base** (snapshot) de configuración en control de versiones.
3. Auditar periódicamente la configuración contra la línea base.
4. Actualizar la línea base solo mediante un **cambio aprobado** (sección 15.2).

## 15.2 Gestión de cambios

### Objetivo
Controlar cualquier modificación al software, configuración o entregables, minimizando el riesgo de
interrupción.

### Tipos de cambio

| Tipo | Ejemplo | Aprobación |
|---|---|---|
| Estándar | Actualización de contenido (controles, evidencias) | Operador autorizado |
| Normal | Cambio de código o configuración menor | Encargado de Ciberseguridad |
| Mayor | Cambio de alcance, funcionalidad o arquitectura con impacto transversal | Product Owner y Encargado de Ciberseguridad, según impacto |
| Emergencia | Corrección de incidente crítico que no admite espera | Encargado + informática, con revisión posterior |

### Proceso de control de cambios

1. **Solicitud:** se registra el cambio con justificación, impacto y plan de reversión.
2. **Evaluación:** se analiza el impacto (disponibilidad, seguridad, datos) y el riesgo.
3. **Aprobación:** el responsable autoriza según el tipo de cambio.
4. **Implementación:** se aplica el cambio en un ambiente controlado (o ventana de mantenimiento).
5. **Prueba:** se verifica que el cambio no rompe la funcionalidad (regresión).
6. **Cierre:** se actualiza la línea base de configuración y se documenta.

> Los entregables del proyecto (código, diagramas, documentación) también se gestionan como cambios:
> cada modificación se registra en Git con un identificador y se revisa antes de integrarse.

### Cambio de alcance del 21-10-2026

La incorporación del módulo de Usuarios y de la Ticketera, acordada con el Product Owner el
21-10-2026, se gestionó como **cambio Mayor**, con aprobación del Product Owner. Se revisaron su
impacto en alcance, roles, privacidad, pruebas, infraestructura y cronograma; este cambio queda
registrado en la línea base documental y en la carta Gantt (Entregable 16).

## 15.3 Gestión de incidentes

### Objetivo
Restablecer el servicio lo antes posible ante incidentes del propio SGSI, con trazabilidad completa.

**Distinción de alcance:** la ticketera es un módulo de negocio para recibir denuncias y reportes de
ciberseguridad del hospital; sus tickets son gestionados por `encargado` y, si corresponde, se derivan
a incidentes formales del negocio. Esta sección trata únicamente incidentes de operación del propio
SGSI (caídas, defectos, pérdida de datos o fallas de configuración), que se registran en el proceso de
soporte/gestión de incidentes del servicio. No son el mismo registro ni ciclo de vida, y `admin_sistema`
no obtiene por ello acceso al contenido de denuncias.

### Priorización

| Prioridad | Definición | Tiempo de respuesta | Resolución |
|---|---|---|---|
| Crítica | Sistema caído o pérdida de datos | 30 min | 4 h |
| Alta | Módulo clave no funciona | 1 h | 8 h |
| Media | Función degradada | 4 h | 24 h |
| Baja | Error cosmético | 8 h | 5 días hábiles |

### Proceso de gestión de incidentes

1. **Detección y registro:** por monitoreo (`/api/health`) o reporte a la mesa de ayuda; no utilizar la ticketera de negocio como canal de soporte de fallas del propio SGSI.
2. **Clasificación:** asignar prioridad y categoría.
3. **Diagnóstico:** identificar causa probable.
4. **Resolución y recuperación:** aplicar la solución (puede requerir un cambio, sección 15.2).
5. **Verificación:** confirmar que el servicio volvió a la normalidad.
6. **Cierre:** documentar causa raíz, solución y lección aprendida.

### Escalamiento

| Nivel | Responsable |
|---|---|
| N1 | Mesa de ayuda interna |
| N2 | Equipo de informática |
| N3 | Equipo de desarrollo/proveedor |
| Notificación | Encargado de Ciberseguridad (obligatoria en Crítica/Alta) |
