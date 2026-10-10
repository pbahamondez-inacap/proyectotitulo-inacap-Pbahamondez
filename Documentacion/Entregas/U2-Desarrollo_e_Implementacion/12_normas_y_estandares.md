# 12. Normas y estándares a incorporar

> **Entregable 12 — Evaluación Sumativa 2 (ES2), Unidad 2 (Desarrollo e Implementación)**
> **Proyecto:** SGSI — Sistema de Gestión de Seguridad de la Información
> **Mandante:** Hospital Félix Bulnes Cerda (Miguel Godoy, Encargado de Ciberseguridad)
> **Criterio evaluado:** `2.1.4.12` — Normas y estándares incorporados en el desarrollo, con
> justificación detallada de su incorporación.

---

## 12.1 Resumen de normas y estándares

| # | Norma/Estándar | Ámbito | Uso en el proyecto |
|---|---|---|---|
| N1 | ISO/IEC 27001:2022 | SGSI (requisitos) | Base del catálogo de controles y del cálculo de madurez |
| N2 | ISO/IEC 27002:2022 | Guía de controles | Detalle de implementación de los controles del Anexo A |
| N3 | Ley N.º 21.663 | Ciberseguridad (Chile) | Taxonomía ANCI y plazos legales de reporte (OIV) |
| N4 | Ley N.º 19.628 / 21.719 | Protección de datos personales | Manejo de datos personales y de salud |
| N5 | ISO/IEC 25010 | Calidad de software | Criterios de calidad (seguridad, usabilidad, mantenibilidad) |
| N6 | IEEE 830 | Especificación de requisitos | Documentación de requerimientos funcionales/no funcionales |
| N7 | OWASP Top 10 / ASVS | Seguridad de aplicaciones web | Controles de autenticación, sesión y acceso |
| N8 | ISO/IEC 20000 / ITIL | Gestión de servicios TI | Planes de disponibilidad, continuidad y mantención (E.13–15) |
| N9 | PMBOK (PMI) | Gestión de proyectos | Cronograma, interesados y gestión del alcance |
| N10 | OpenAPI / Swagger | Especificación de API | Documentación de la API REST (`/docs`) |

## 12.2 Justificación detallada

### N1 — ISO/IEC 27001:2022
**Motivo:** el hospital es Operador de Importancia Vital (OIV) y debe demostrar madurez en sus
controles de seguridad. El sistema implementa el **Anexo A** (dominios organizacional, personas,
físico y tecnológico) y calcula el % de madurez según el estado de cada control.

### N2 — ISO/IEC 27002:2022
**Motivo:** proporciona la guía práctica para implementar cada control; se usa como referencia de
descripción y evidencia esperada por control.

### N3 — Ley N.º 21.663
**Motivo:** define las obligaciones del hospital como OIV: clasificación de incidentes según la
**taxonomía ANCI** y plazos de reporte (alerta temprana 3 h; 72 h severidad alta/crítica; 15 días
media/baja). Estas reglas están implementadas en `services.py`.

### N4 — Ley N.º 19.628 / 21.719
**Motivo:** el sistema maneja datos personales (usuarios, responsables, contactos); se garantiza
acceso mínimo por rol y se evita el uso de datos clínicos reales en pruebas.

### N5 — ISO/IEC 25010
**Motivo:** orienta la calidad de la solución: seguridad (confidencialidad/integridad), usabilidad
(dashboard), mantenibilidad (código modular) y rendimiento (SLA del Entregable 10).

### N6 — IEEE 830
**Motivo:** los requerimientos funcionales/no funcionales se documentan como historias de usuario con
atributos (prioridad, criterio de aceptación), compatibles con la especificación de requisitos.

### N7 — OWASP Top 10 / ASVS
**Motivo:** el SGSI es una aplicación web con autenticación; se aplican controles contra inyección,
gestión de sesión JWT, control de acceso (RBAC) y hash de contraseñas (PBKDF2).

### N8 — ISO/IEC 20000 / ITIL
**Motivo:** sustenta la operación del servicio: gestión de disponibilidad (Entregable 13),
continuidad (Entregable 14) y gestión de configuración/cambios/incidentes (Entregable 15).

### N9 — PMBOK
**Motivo:** marco de gestión del proyecto: identificación de interesados, cronograma (Entregable 16)
y justificación del alcance.

### N10 — OpenAPI / Swagger
**Motivo:** la API se documenta automáticamente en `/docs`, facilitando pruebas, integración y
auditoría del SGSI.

## 12.3 Aplicación por componente

| Componente | Normas aplicadas |
|---|---|
| Catálogo de controles y madurez | N1, N2 |
| Módulo de incidentes | N3 |
| Autenticación y RBAC | N4, N7, N10 |
| Diseño y calidad del software | N5, N6 |
| Operación del servicio | N8 |
| Gestión del proyecto | N9 |
