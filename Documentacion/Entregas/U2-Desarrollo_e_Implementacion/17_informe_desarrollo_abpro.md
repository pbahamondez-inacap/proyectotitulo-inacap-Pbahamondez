# 17. Informe de Desarrollo del Proyecto (Plantilla ABPro)

> **Entregable 17 — Evaluación Sumativa 2 (ES2), Unidad 2 (Desarrollo e Implementación)**
> **Proyecto:** SGSI — Sistema de Gestión de Seguridad de la Información
> **Mandante:** Hospital Félix Bulnes Cerda (Miguel Godoy, Encargado de Ciberseguridad)
> **Criterio evaluado:** `2.1.6.17` — Revisión y justificación de la adecuación del cronograma, en
> términos de funcionalidad y capacidad de resolver el problema abordado.

Este documento es el **informe de desarrollo consolidado** que integra los entregables 1–16 en la
estructura de la plantilla **ABPro**. Sirve de guía para armar el documento Word final.

---

## 17.1 Estructura del informe (mapeo a entregables)

| Sección ABPro | Contenido | Entregable fuente |
|---|---|---|
| Portada y datos del proyecto | Título, equipo, académico guía, mandante | Formulación U1 |
| Resumen ejecutivo | Problema, solución y resultados | Este informe (§17.2) |
| 1. Formulación y alcance | Problema, objetivos, alcance y restricciones | `borrador_informe_formulacion.md` |
| 2. Análisis comparativo | Selección de tecnologías y metodología (factibilidad) | `01_análisis...` |
| 3. Requerimientos de recursos | Herramientas, lenguajes, hardware y servicios TI | `02_herramientas...` |
| 4. Modelamiento de procesos | BPMN de 3 procesos con subprocesos | `03_bpmn...` |
| 5. Diseño UML | Casos de uso y componentes | `04_uml...` |
| 6. Modelo de datos | ER + diccionario de datos | `05_modelo_datos...` |
| 7. Red e infraestructura | Topología, infraestructura y arquitectura | `06_…`, `07_…`, `08_…` |
| 8. Indicadores y servicios | KPI SMART y SLA | `09_kpi...`, `10_sla...` |
| 9. Calidad y pruebas | Plan de pruebas | `11_plan_de_pruebas...` |
| 10. Normas y estándares | Justificación de normas incorporadas | `12_normas...` |
| 11. Servicios TI y continuidad | Implementación, disponibilidad, continuidad y mantención | `13_…`, `14_…`, `15_…` |
| 12. Planificación | Carta Gantt / detalle de fases | `16_carta_gantt...` |
| 13. Justificación del cronograma | Adecuación del cronograma a la solución | §17.3 de este informe |
| 14. Conclusiones y trabajos futuros | Cierre del informe | §17.4 |

## 17.2 Resumen ejecutivo

El Hospital Félix Bulnes Cerda, en su calidad de Operador de Importancia Vital (Ley N.º 21.663),
requiere demostrar la madurez de sus controles ISO/IEC 27001 y gestionar los incidentes de
ciberseguridad dentro de plazos legales. El proyecto desarrolló un **Sistema de Gestión de Seguridad
de la Información (SGSI)** de tipo GRC, compuesto por una **SPA en React** y una **API REST en
FastAPI**, que centraliza controles, evidencias, madurez, incidentes, terceros y personas, con
reportería exportable. La solución reemplaza el trabajo manual disperso por un sistema único,
auditable y con visualización gráfica del avance.

## 17.3 Justificación de la adecuación del cronograma

### 17.3.1 Coherencia entre cronograma y solución

| Fase (Entregable 16) | Cómo habilita la funcionalidad de la solución |
|---|---|
| F1 Formulación y requisitos | Asegura que los módulos construidos responden a las necesidades del mandante (controles, incidentes, terceros, personas) |
| F2 Diseño | Produce los modelos (BPMN, UML, datos, arquitectura) que guían el desarrollo y evitan retrabajo |
| F3–F4 Desarrollo | Entrega el backend (API + reglas) y el frontend (dashboard), que son el núcleo funcional |
| F5 Pruebas | Valida que la solución resuelve el problema (CP-01 a CP-16) |
| F6 Documentación | Aporta los planes (KPI, SLA, continuidad, mantención) que hacen operativa la solución |
| F7 Cierre | Consolida el informe y la demo para la defensa |

### 17.3.2 Justificación de la duración y holgura

- **Duración total: 11 semanas**, acorde al plazo de la Unidad 2 y a los hitos EF2 → ES2.
- **1 semana de holgura** en las fases de desarrollo permite absorber ajustes del mandante
  (refinamiento del catálogo de controles y de la taxonomía ANCI) sin comprometer la entrega.
- El **orden de fases** es secuencial donde existe dependencia (diseño antes de desarrollo, pruebas
  después de desarrollo) y **solapado** donde es posible (backend y frontend en paralelo), lo que
  optimiza el uso del equipo de 3 integrantes.

### 17.3.3 Adecuación al problema

El cronograma prioriza los módulos que **resuelven directamente el problema** identificado: primero el
registro de controles y el cálculo de madurez (indicador "15.4"), luego la gestión de incidentes con
plazos legales, y finalmente terceros/personas y reportería. Esta secuencia garantiza que, incluso
ante un recorte de plazo, el entregable mínimo viable cubra el cumplimiento normativo central.

## 17.4 Conclusiones y trabajos futuros

**Conclusiones:**
- La solución cumple el objetivo general: registrar, medir y visualizar la madurez del SGSI y
  gestionar incidentes conforme a la Ley 21.663.
- El stack seleccionado (FastAPI + React + PostgreSQL) resultó técnicamente, económicamente e
  implementativamente viable (Entregable 1).

**Trabajos futuros (fuera del alcance actual):**
- Integración automatizada con la plataforma de la ANCI (API oficial).
- Módulo de auditoría de cambios con firma electrónica.
- Integración con el directorio institucional (SSO/LDAP).
- Migración a nube y alta disponibilidad multi-sitio.

## 17.5 Anexos

Los diagramas editables se encuentran en las carpetas `03_bpmn/`, `04_uml/`, `05_modelo_datos/`,
`06_topologia/`, `07_infraestructura/` y `08_arquitectura/` (formato `.drawio`).
