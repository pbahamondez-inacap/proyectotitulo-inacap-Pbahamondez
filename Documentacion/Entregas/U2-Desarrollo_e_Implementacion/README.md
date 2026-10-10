# Entregables — Unidad 2 (Desarrollo e Implementación) · ES2

Repositorio de los 17 entregables del checklist de la **Evaluación Sumativa 2 (ES2)** del proyecto
**SGSI — Sistema de Gestión de Seguridad de la Información** para el Hospital Félix Bulnes Cerda.

> Proyecto de Título TIHI84 · INACAP · Mandante: Miguel Godoy (Encargado de Ciberseguridad).
> Stack implementado: FastAPI + SQLAlchemy (SQLite/PostgreSQL) + JWT/RBAC · React 18 + TS + Vite +
> Recharts · metodología Scrum.

---

## Índice de entregables

| # | Entregable | Archivo | Criterio rúbrica |
|---|---|---|---|
| 1 | Análisis comparativo de tecnologías y metodologías | `01_analisis_comparativo_tecnologias_metodologias.md` | 2.1.1.1 |
| 2 | Herramientas, aplicaciones, lenguajes, hardware y servicios TI | `02_herramientas_aplicaciones_lenguajes_hardware_servicios_ti.md` | 2.1.1.2 |
| 3 | Diagramas BPMN (3 procesos con subprocesos) | `03_bpmn_procesos_negocio.md` | 2.1.2.3 |
| 4 | Diagramas UML: casos de uso + componentes | `04_uml_casos_de_uso_y_componentes.md` | 2.1.2.4 |
| 5 | Modelo de datos + diccionario | `05_modelo_datos_diccionario.md` | 2.1.2.5 |
| 6 | Topología de comunicación | `06_topologia_comunicacion.md` | 2.1.2.6 |
| 7 | Infraestructura | `07_infraestructura.md` | 2.1.2.7 |
| 8 | Arquitectura de la solución | `08_arquitectura_solucion.md` | 2.1.2.8 |
| 9 | KPI con detalle SMART | `09_kpi_smart.md` | 2.1.3.9 |
| 10 | Definición de SLA | `10_sla.md` | 2.1.3.10 |
| 11 | Plan de pruebas | `11_plan_de_pruebas.md` | 2.1.4.11 |
| 12 | Normas y estándares | `12_normas_y_estandares.md` | 2.1.4.12 |
| 13 | Plan de implementación / disponibilidad | `13_plan_implementacion_disponibilidad.md` | 2.1.5.13 |
| 14 | Plan de continuidad del servicio | `14_plan_continuidad.md` | 2.1.5.14 |
| 15 | Plan de mantención | `15_plan_mantencion.md` | 2.1.5.15 |
| 16 | Carta Gantt / detalle de fases | `16_carta_gantt.md` | 2.1.6.16 |
| 17 | Informe de desarrollo (ABPro) | `17_informe_desarrollo_abpro.md` | 2.1.6.17 |

## Diagramas editables (`.drawio`)

Para abrir en **draw.io** (escritorio o web): `Archivo → Abrir` y seleccionar el archivo.

| Carpeta | Diagrama |
|---|---|
| `03_bpmn/` | `03a_proceso_controles_iso27001.drawio` · `03b_proceso_incidentes.drawio` · `03c_proceso_terceros.drawio` |
| `04_uml/` | `04a_uml_casos_de_uso.drawio` · `04b_uml_componentes.drawio` |
| `05_modelo_datos/` | `05a_modelo_datos.drawio` |
| `06_topologia/` | `06a_topologia_comunicacion.drawio` |
| `07_infraestructura/` | `07a_infraestructura.drawio` |
| `08_arquitectura/` | `08a_arquitectura_solucion.drawio` |

> En los `.drawio` se usan formas estándar para edición ágil. Para notación estricta (BPMN 2.0, UML,
> Entity Relation, Redes), activa la biblioteca correspondiente en draw.io con `+ Más formas`.

## Guía de uso

1. **Documentos Markdown:** los diagramas Mermaid se visualizan directamente en GitHub/VS Code.
2. **Validación de datos:** los valores referenciales (hardware, SLA, RPO/RTO, metas KPI) están
   marcados como propuesta y deben confirmarse con el mandante.
3. **Informe final:** el `17_informe_desarrollo_abpro.md` es el hilo conductor que integra los 16
   entregables previos en la estructura de la plantilla ABPro.

## Nota de coherencia entre diagramas

- **Entregable 4** → componentes de **software** (UML).
- **Entregables 6 y 7** → red e infraestructura **física**.
- **Entregable 8** → vista integrada **software + hardware** de la solución.
