# 10. Definición de SLA (Acuerdos de Nivel de Servicio)

> **Entregable 10 — Evaluación Sumativa 2 (ES2), Unidad 2 (Desarrollo e Implementación)**
> **Proyecto:** SGSI — Sistema de Gestión de Seguridad de la Información
> **Mandante:** Hospital Félix Bulnes Cerda (Miguel Godoy, Encargado de Ciberseguridad)
> **Criterio evaluado:** `2.1.3.10` — Detalle de los niveles de servicio (SLA) considerando los
> resultados esperados por el cliente una vez implementada la solución.

Este entregable define los **acuerdos de nivel de servicio (SLA)** del SGSI: disponibilidad, tiempos
de respuesta y resolución según severidad, respaldo (RTO/RPO), rendimiento y proceso de escalamiento.
Los valores son una **propuesta referencial** a validar con el mandante.

---

## 10.1 Resumen del servicio

| Parámetro | Valor propuesto |
|---|---|
| Horario de servicio | Lunes a viernes, 08:00–17:00 (horario administrativo) |
| Disponibilidad | ≥ 99 % mensual en horario de servicio |
| Usuarios | 5 roles: `encargado`, `admin_contratos`, `referente_tecnico`, `director` y `admin_sistema` |
| Mesa de ayuda | Interna (08:00–17:00) + proveedor (17:00–06:59, alineado a la operación del hospital) |
| Cobertura | El SGSI es un sistema de **apoyo/gobernanza** (no crítico como Trakcare) |

---

## 10.2 Disponibilidad del servicio

| Métrica | Compromiso |
|---|---|
| Disponibilidad mensual del SGSI (horario de servicio) | ≥ 99 % |
| Disponibilidad mensual del formulario público de tickets (horario de servicio) | ≥ 99 %; accesible por HTTPS desde la red interna del hospital, sin autenticación solo en los endpoints auxiliares del formulario (categorías y envío) y la consulta pública de estado por código |
| Ventanas de mantenimiento | Programadas, notificadas con ≥ 48 h de anticipación, preferentemente fuera del horario de servicio |
| Tiempo máximo de indisponibilidad planificada | ≤ 2 h por ventana |
| Monitoreo | Verificación automática del endpoint `GET /api/health` |

---

## 10.3 Tiempos de respuesta y resolución por severidad

| Severidad | Definición (ejemplo) | Tiempo de respuesta | Tiempo de resolución |
|---|---|---|---|
| **Crítica** | Sistema inaccesible para todos los usuarios o pérdida de datos | 30 min | 4 h |
| **Alta** | Módulo clave no funciona (ej. incidentes o reporte) | 1 h | 8 h (mismo día) |
| **Media** | Función degradada sin detener la operación | 4 h | 24 h |
| **Baja** | Mejora o error cosmético | 8 h | 5 días hábiles |

---

### SLA específicos de ticketera y ciclo de vida de usuarios

| Servicio / evento | Compromiso | Responsable / condición |
|---|---|---|
| Acuse de recibo y primera revisión de un ticket | Pasar a `en_analisis` en ≤ 24 h hábiles desde el registro | Equipo de ciberseguridad (`encargado`); se registra el cambio de estado |
| Ticket de severidad percibida alta o crítica | Primera atención en ≤ 4 h hábiles | Prioridad en la bandeja; si se determina incidente reportable, aplican además los plazos legales del KPI-03 |
| Tickets gestionados dentro de SLA | ≥ 90 % | Medición mensual según KPI-10; no reemplaza obligaciones legales de reporte |
| Baja de usuario desvinculado | Deshabilitación lógica en ≤ 1 día hábil desde la solicitud | `admin_sistema`; no se elimina el usuario ni su auditoría |

La creación pública y la consulta de categorías no requieren autenticación ni deben registrar identidad del emisor. La gestión de la bandeja, el cambio de estado y la conversión a incidente requieren autenticación y rol `encargado`; `admin_sistema` no accede al contenido de tickets.

## 10.4 Respaldo, recuperación (RTO/RPO) y continuidad

| Métrica | Compromiso |
|---|---|
| **RPO** (pérdida máxima de datos tolerada) | ≤ 24 h para base de datos, evidencias y adjuntos de tickets (`ticket_adjuntos`) almacenados en NAS-01 |
| **RTO** (tiempo para restablecer el servicio) | ≤ 8 h hábiles, incluyendo restauración de base de datos, evidencias y adjuntos de tickets |
| Frecuencia de respaldo | Diaria (incremental) + semanal (completo) para BD y carpetas de evidencias y tickets |
| Retención de respaldos | 30 días (mínimo) |
| Prueba de restauración | Trimestral (simulacro de recuperación) |

> Los valores de RPO/RTO se alinean con el Plan de Continuidad del Servicio (Entregable 14).

---

## 10.5 Rendimiento

| Métrica | Compromiso |
|---|---|
| Tiempo de respuesta de la API (p95) | ≤ 500 ms para operaciones CRUD típicas |
| Carga de la SPA (dashboard) | ≤ 3 s en red interna |
| Exportación de reportes CSV | ≤ 10 s para volúmenes de catálogo (≤ 1.000 registros) |
| Usuarios concurrentes soportados | ≥ 10 simultáneos sin degradación |

---

## 10.6 Seguridad y confidencialidad

| Métrica | Compromiso |
|---|---|
| Autenticación | JWT obligatoria para toda operación, excepto `POST /api/public/tickets`, consulta de categorías y consulta de estado por código de seguimiento; esta excepción no habilita acceso anónimo a otros datos o módulos |
| Control de acceso | RBAC por rol (mínimo privilegio) |
| Cifrado en tránsito | HTTPS/TLS obligatorio |
| Integridad y trazabilidad | Registro de estado y evidencias auditable por control/incidente |
| Reporte de incidentes de seguridad del propio SGSI | Según proceso interno del hospital |

---

## 10.7 Proceso de escalamiento

1. **Nivel 1 — Mesa de ayuda interna:** recibe y registra el requerimiento (08:00–17:00).
2. **Nivel 2 — Equipo de informática:** resuelve fallas funcionales/técnicas del SGSI.
3. **Nivel 3 — Equipo de desarrollo / proveedor:** escalamiento para defectos de software o cambios
   (se rige por el plan de gestión de cambios, Entregable 15).
4. **Notificación al Encargado de Ciberseguridad:** obligatoria para severidad Crítica/Alta.

---

## 10.8 Medición y reporte

- Los SLA se miden mensualmente y se reportan en el **resumen ejecutivo** del módulo de Reportería.
- El cumplimiento de disponibilidad se vincula al **KPI-06** (uptime ≥ 99 %) del Entregable 9.
- Los tiempos de resolución se registran en la gestión de incidentes del propio SGSI (Entregable 15), distinta de los tickets de negocio de ciberseguridad.
- Los SLA de tickets y baja de usuarios se siguen con los KPI-09, KPI-10 y KPI-11 del Entregable 9.

---

## 10.9 Nota de validación

Los umbrales (disponibilidad, tiempos de respuesta/resolución, RPO/RTO y retención) deben
**confirmarse con el mandante** antes de la entrega final, dado que el hospital definirá los
parámetros definitivos según su política de TI y la criticidad asignada al SGSI.
