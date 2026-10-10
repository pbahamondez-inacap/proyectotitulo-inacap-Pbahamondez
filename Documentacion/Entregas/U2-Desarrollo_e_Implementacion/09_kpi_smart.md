# 9. Definición de KPI con detalle SMART

> **Entregable 9 — Evaluación Sumativa 2 (ES2), Unidad 2 (Desarrollo e Implementación)**
> **Proyecto:** SGSI — Sistema de Gestión de Seguridad de la Información
> **Mandante:** Hospital Félix Bulnes Cerda (Miguel Godoy, Encargado de Ciberseguridad)
> **Criterio evaluado:** `2.1.3.9` — Detalle SMART de los indicadores clave de desempeño (KPI) que
> permitan medir la eficiencia de la solución desarrollada.

Este entregable define **8 KPI** con detalle **SMART** (Específico, Medible, Alcanzable, Relevante y
Acotado en el tiempo), cada uno vinculado a un módulo concreto del SGSI y a su fuente de datos real.

---

## 9.1 Resumen de KPI

| Código | Indicador | Fuente (módulo) | Meta |
|---|---|---|---|
| KPI-01 | % de madurez global del SGSI | Madurez (`GET /api/madurez`) | ≥ 60 % al cierre; 100 % a mediano plazo |
| KPI-02 | % de controles con evidencia registrada | Controles / Evidencias | ≥ 80 % |
| KPI-03 | % de incidentes reportados dentro de plazo legal | Incidentes | 100 % |
| KPI-04 | % de terceros con cláusulas de seguridad cumplidas | Terceros | ≥ 90 % |
| KPI-05 | % de controles de personas en estado gestionado | Personas | ≥ 75 % |
| KPI-06 | Disponibilidad del sistema (uptime) | Infraestructura/monitoreo | ≥ 99 % horario administrativo |
| KPI-07 | Tiempo medio de registro de incidente desde la detección | Incidentes | ≤ 30 minutos |
| KPI-08 | Adopción de la herramienta (sesiones/semana) | Autenticación | ≥ 20 sesiones/semana |

---

## 9.2 Detalle SMART por KPI

### KPI-01 — % de madurez global del SGSI

| Criterio | Detalle |
|---|---|
| **S** — Específico | Porcentaje de avance ponderado de los controles ISO/IEC 27001 (Anexo A) según su estado. |
| **M** — Medible | Fórmula: `Σ(peso del estado de cada control) / total de controles × 100`, con pesos `no_iniciado=0`, `iniciado=0.33`, `implementado=0.67`, `gestionado=1.0`. Fuente: módulo Madurez. |
| **A** — Alcanzable | Meta ≥ 60 % al cierre del proyecto; se ajusta con la validación del mandante (meta institucional "15.4"). |
| **R** — Relevante | Es el indicador de gestión institucional que sustenta el cumplimiento de la Ley 21.663 como OIV. |
| **T** — Temporal | Medición mensual; meta anual alineada al ciclo PDCA del SGSI. |

### KPI-02 — % de controles con evidencia registrada

| Criterio | Detalle |
|---|---|
| **S** | Proporción de controles que cuentan con al menos una evidencia adjunta. |
| **M** | `(controles con ≥ 1 evidencia / total de controles) × 100`. Fuente: Controles + Evidencias. |
| **A** | Meta ≥ 80 %; parte del estado actual (varios controles en "iniciado" sin evidencia). |
| **R** | La evidencia es la base de la trazabilidad y la auditabilidad del SGSI. |
| **T** | Medición mensual y por dominio (organizacional, personas, físico, tecnológico). |

### KPI-03 — % de incidentes reportados dentro de plazo legal

| Criterio | Detalle |
|---|---|
| **S** | Proporción de incidentes reportables a la ANCI que se reportaron dentro del plazo legal. |
| **M** | `(incidentes reportados ≤ plazo / total de incidentes reportables) × 100`. Plazos: alerta temprana 3 h; reporte 72 h (alta/crítica) o 15 días (media/baja). Fuente: Incidentes (fechas calculadas automáticamente). |
| **A** | Meta 100 %; el sistema computa los plazos y alerta vencimientos para facilitarlo. |
| **R** | Cumplimiento directo del deber de reportar de la Ley N.º 21.663. |
| **T** | Medición mensual y por evento. |

### KPI-04 — % de terceros con cláusulas de seguridad cumplidas

| Criterio | Detalle |
|---|---|
| **S** | Proporción de proveedores/terceros cuyo checklist de cláusulas de seguridad está en estado "cumple". |
| **M** | `(terceros con estado_cumplimiento = "cumple" / total de terceros) × 100`. Fuente: Terceros. |
| **A** | Meta ≥ 90 % para proveedores críticos (ej. InterSystems). |
| **R** | Mitiga el riesgo de terceros exigido por ISO/IEC 27001 (dominio organizacional/tecnológico). |
| **T** | Medición trimestral, alineada a renovaciones de contrato/licitación. |

### KPI-05 — % de controles de personas en estado gestionado

| Criterio | Detalle |
|---|---|
| **S** | Proporción de controles del ciclo de vida del personal (capacitación, antecedentes, confidencialidad, etc.) en estado "gestionado". |
| **M** | `(persona_controles con estado = "gestionado" / total) × 100`. Fuente: Personas. |
| **A** | Meta ≥ 75 %; parte de controles hoy "iniciado" sin evidencia (ej. revisión de antecedentes). |
| **R** | Evidencia el dominio "Personas" del Anexo A de ISO/IEC 27001. |
| **T** | Medición mensual. |

### KPI-06 — Disponibilidad del sistema (uptime)

| Criterio | Detalle |
|---|---|
| **S** | Porcentaje de tiempo en que el SGSI está operativo y accesible. |
| **M** | `(horas disponibles / horas totales del período) × 100`. Fuente: monitoreo del endpoint `/api/health`. |
| **A** | Meta ≥ 99 % en horario administrativo (08:00–17:00). |
| **R** | Respalda el SLA de disponibilidad (Entregable 10) y la continuidad del servicio (Entregable 14). |
| **T** | Medición mensual. |

### KPI-07 — Tiempo medio de registro de incidente desde la detección

| Criterio | Detalle |
|---|---|
| **S** | Tiempo promedio entre la detección de un evento y su registro en el SGSI. |
| **M** | `Σ(fecha_registro − fecha_deteccion) / n incidentes`, en minutos. Fuente: Incidentes. |
| **A** | Meta ≤ 30 minutos, suficiente para no comprometer la alerta temprana de 3 h. |
| **R** | Reduce el riesgo de incumplimiento de plazos legales de reporte. |
| **T** | Medición por evento y consolidado mensual. |

### KPI-08 — Adopción de la herramienta (sesiones/semana)

| Criterio | Detalle |
|---|---|
| **S** | Número de sesiones iniciadas (logins) por semana en el SGSI. |
| **M** | Conteo de accesos vía autenticación JWT (`POST /api/auth/login`). Fuente: Autenticación/logs. |
| **A** | Meta ≥ 20 sesiones/semana (4 roles activos). |
| **R** | Mide que la herramienta reemplaza efectivamente las planillas manuales. |
| **T** | Medición semanal. |

---

## 9.3 Fuente de datos y módulo de origen

| KPI | Módulo del SGSI | Dato técnico de origen |
|---|---|---|
| KPI-01, KPI-02 | Controles / Evidencias / Madurez | `controles.estado`, `evidencias.control_id`, cálculo de `madurez.py` |
| KPI-03, KPI-07 | Incidentes | `incidentes.fecha_deteccion`, `fecha_reporte`, plazos de `services.py` |
| KPI-04 | Terceros | `terceros.estado_cumplimiento` |
| KPI-05 | Personas | `persona_controles.estado` |
| KPI-06 | Infraestructura | Endpoint `GET /api/health` + monitoreo |
| KPI-08 | Autenticación | `POST /api/auth/login` + logs |

---

## 9.4 Nota sobre la meta institucional

El KPI-01 se vincula al indicador de gestión institucional referido por el mandante como
"compromiso/meta 15.4" (nombre oficial pendiente de confirmación con el hospital). Los valores de
meta aquí propuestos son referenciales y deben validarse con el Encargado de Ciberseguridad antes de
la entrega final.
