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
| N11 | ISO/IEC 27001:2022 Anexo A 6.8 y 5.24–5.28 | Eventos e incidentes de seguridad | Recepción, evaluación, respuesta y aprendizaje de reportes; derivación de tickets a incidentes formales |
| N12 | ISO/IEC 27001:2022 Anexo A 5.15–5.18 y 8.2 | Acceso e identidades privilegiadas | RBAC, altas/bajas de usuarios y separación del rol `admin_sistema` |
| N13 | ISO/IEC 27001:2022 Anexo A 8.15 y 6.5 | Registro y responsabilidades al término/cambio | Auditoría de acciones y deshabilitación oportuna de usuarios desvinculados |
| N14 | OWASP ASVS / OWASP API Security | Seguridad de aplicaciones y API | Validación, control de acceso, carga de archivos, rate limiting y protección contra asignación masiva |
| N15 | Ley N.º 21.719 / Ley N.º 19.628 | Protección y minimización de datos personales | No recolectar ni asociar la identidad de quien reporta por el canal público |

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

### N11 — ISO/IEC 27001:2022 Anexo A 6.8 y 5.24–5.28
**Motivo:** el control 6.8 sustenta la notificación de eventos de seguridad; los controles 5.24–5.28
orientan la preparación, evaluación, respuesta y aprendizaje ante incidentes. Se aplican al formulario,
a la bandeja de tickets y a la conversión de un ticket en incidente, sin confundir el reporte ciudadano
con un incidente formal hasta que el equipo de ciberseguridad lo evalúe.

### N12 — ISO/IEC 27001:2022 Anexo A 5.15–5.18 y 8.2
**Motivo:** fundamentan el control de acceso, la gestión de identidades y derechos, y la protección de
accesos privilegiados. El acceso a `/api/usuarios` se limita a `admin_sistema`; la gestión de tickets
se limita a `encargado`, con separación de funciones y mínimo privilegio.

### N13 — ISO/IEC 27001:2022 Anexo A 8.15 y 6.5
**Motivo:** 8.15 respalda el registro y monitoreo de actividad, aplicado a la auditoría de altas, cambios
y bajas de usuarios; 6.5 orienta responsabilidades ante término o cambio de funciones, materializadas
en la deshabilitación lógica oportuna de cuentas sin borrar su historial. Los registros no deben
contener contraseñas ni datos identificadores del emisor del formulario público.

### N14 — OWASP ASVS / OWASP API Security
**Motivo:** ASVS orienta la verificación de autenticación, autorización y manejo de archivos; OWASP API
Security guía la validación de entradas, autorización a nivel de función/objeto, protección frente a
rate abuse y asignación masiva. Para el formulario público se aplican límites de solicitudes, validación
estricta, sanitización y controles de tipo/tamaño de adjuntos.

### N15 — Ley N.º 21.719 / Ley N.º 19.628
**Motivo:** el principio de minimización exige no solicitar ni registrar datos identificatorios de quien
utiliza el formulario público. La tabla `tickets` no mantiene FK a usuarios; tampoco se registran token,
IP ni user-agent del emisor. Los datos de contacto internos del SGSI se mantienen sujetos a acceso mínimo.

> **Validación jurídica:** el canal de ticketera es un canal de reporte de ciberseguridad y no sustituye
> los canales formales de denuncia laboral o funcionaria. El alcance y los textos informativos del
> formulario deben validarse con el área jurídica del hospital antes de producción. No se presume la
> incorporación de legislación específica sobre denuncias.

## 12.3 Aplicación por componente

| Componente | Normas aplicadas |
|---|---|
| Catálogo de controles y madurez | N1, N2 |
| Módulo de incidentes | N3, N11 |
| Ticketera y conversión a incidente | N3, N7, N11, N14, N15 |
| Formulario público y adjuntos | N4, N7, N14, N15 |
| Administración de usuarios y auditoría | N4, N12, N13, N15 |
| Autenticación y RBAC | N4, N7, N10, N12 |
| Diseño y calidad del software | N5, N6 |
| Operación del servicio | N8 |
| Gestión del proyecto | N9 |
