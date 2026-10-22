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
| 4. Modelamiento de procesos | BPMN de 5 procesos con subprocesos (P1–P5; incluye Usuarios y Ticketera) | `03_bpmn...` |
| 5. Diseño UML | Casos de uso y componentes | `04_uml...` |
| 6. Modelo de datos | ER + diccionario de datos; 10 tablas, incluidas `tickets`, `ticket_adjuntos`, `notificaciones` y `auditoria_usuarios` | `05_modelo_datos...` |
| 7. Red e infraestructura | Topología, infraestructura y arquitectura | `06_…`, `07_…`, `08_…` |
| 8. Indicadores y servicios | KPI SMART y SLA | `09_kpi...`, `10_sla...` |
| 9. Calidad y pruebas | Plan de pruebas | `11_plan_de_pruebas...` |
| 10. Normas y estándares | Justificación de normas incorporadas | `12_normas...` |
| 11. Servicios TI y continuidad | Implementación, disponibilidad, continuidad y mantención | `13_…`, `14_…`, `15_…` |
| 12. Planificación | Carta Gantt / detalle de fases | `16_carta_gantt...` |
| 13. Justificación del cronograma | Adecuación del cronograma a la solución | §17.3 de este informe |
| 14. Conclusiones y trabajos futuros | Cierre del informe | §17.4 |

## 17.2 Resumen ejecutivo

El Hospital Félix Bulnes Cerda, en su calidad de Operador de Importancia Vital (Ley N.º 21.663), requiere demostrar la madurez de sus controles ISO/IEC 27001 y gestionar los incidentes de ciberseguridad dentro de plazos legales. El SGSI desarrollado como solución GRC se compone de una SPA React y una API REST FastAPI; integra controles, evidencias, madurez, incidentes, terceros, personas, reportería, administración de usuarios y una ticketera de denuncias/reportes con formulario público.

El cambio de alcance acordado con el Product Owner el 21-10-2026 incorpora el módulo Usuarios (administrado solo por `admin_sistema`) y la Ticketera, cuyo contenido queda restringido al equipo de ciberseguridad (`encargado`) y cuyo formulario público no requiere autenticación ni registra identidad del emisor. El sistema considera cinco roles y separación de funciones; la solución centraliza trazabilidad, controles y visualización de madurez, y habilita un canal interno para recibir y evaluar reportes de ciberseguridad.

## 17.3 Justificación de la adecuación del cronograma

### 17.3.1 Coherencia entre cronograma y solución

| Fase (Entregable 16) | Cómo habilita la funcionalidad de la solución |
|---|---|
| F1 Formulación y requisitos | Define el alcance original y registra el cambio Mayor aprobado el 21-10-2026 para incorporar Usuarios y Ticketera |
| F2 Diseño | Actualiza BPMN, UML, datos, arquitectura, privacidad y operación del canal público antes de construir |
| F3 Sprint Usuarios | Entrega CRUD, RBAC para `admin_sistema`, baja lógica y auditoría; es prerrequisito de la Ticketera |
| F4 Sprint Ticketera | Entrega formulario público, bandeja confidencial, adjuntos, notificaciones SMTP/internas y conversión a incidente |
| F5 Pruebas | Valida módulos y controles de seguridad, incluidos CP-20 a CP-38, anonimato, rate limiting y adjuntos |
| F6 Documentación | Aporta los planes (KPI, SLA, continuidad, mantención) que hacen operativa la solución |
| F7 Cierre | Consolida el informe y la demo para la defensa |

### 17.3.2 Justificación de la duración y holgura

- **Duración total: 11 semanas**, alineada con los hitos EF2 y ES2 del 11-12-2026; la ampliación de alcance fue formalizada el 21-10-2026 y aprobada por el Product Owner como cambio Mayor.
- Se agregan dos sprints completos, en orden: Usuarios (26-10 al 06-11) y Ticketera (09-11 al 20-11). Este orden habilita la asignación de roles antes de construir la bandeja y conserva separación entre `admin_sistema` y `encargado`.
- Las pruebas CP-20 a CP-38 y UAT se extienden hasta el 04-12; la actualización documental y el informe ABPro se solapan con la validación final. El solapamiento y la holgura protegen la fecha ES2 sin omitir anonimato, confidencialidad, SMTP ni validación de adjuntos.

### 17.3.3 Adecuación al problema

El cronograma conserva la prioridad del núcleo GRC (controles, madurez e incidentes) y agrega, en respuesta al cambio aprobado, Usuarios antes de Ticketera. La Ticketera incorpora el formulario público y la bandeja de ciberseguridad, sin asociar identidad del emisor, y permite derivar reportes a incidentes formales con plazos legales. Los hitos de prueba verifican además que el canal público esté disponible y protegido frente al abuso.

## 17.4 Conclusiones y trabajos futuros

**Conclusiones:**
- La solución cumple el objetivo general: registrar, medir y visualizar la madurez del SGSI y
  gestionar incidentes conforme a la Ley 21.663.
- El stack seleccionado (FastAPI + React + PostgreSQL) resultó técnicamente, económicamente e
  implementativamente viable (Entregable 1).

**Trabajos futuros (fuera del alcance actual):**
- Integración con SSO/LDAP para aprovisionamiento y ciclo de vida de usuarios, manteniendo RBAC y auditoría.
- Integración de tickets con la mesa de ayuda institucional, con clasificación y derivación controladas.
- Cifrado de adjuntos en reposo y gestión de llaves; análisis antivirus automatizado antes de su consulta.
- Integración automatizada con la plataforma de la ANCI cuando exista API oficial habilitada.
- Alta disponibilidad multi-sitio y fortalecimiento del monitoreo, rate limiting y protección anti-spam del formulario público.
- Extensión de auditoría de cambios con firma electrónica, sujeto a evaluación institucional.

## 17.5 Anexos

Los diagramas editables se encuentran en las carpetas `03_bpmn/`, `04_uml/`, `05_modelo_datos/`,
`06_topologia/`, `07_infraestructura/` y `08_arquitectura/` (formato `.drawio`).
