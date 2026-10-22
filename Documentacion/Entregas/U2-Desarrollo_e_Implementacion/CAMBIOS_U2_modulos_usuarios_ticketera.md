# Registro de cambios — Unidad 2 (Desarrollo e Implementación)

> **Proyecto:** SGSI — Sistema de Gestión de Seguridad de la Información · Hospital Félix Bulnes Cerda
> **Alcance:** entregables 1–17 de la ES2 (carpeta [`U2-Desarrollo_e_Implementacion`](./README.md))
> **Origen del cambio:** reunión con el Product Owner (Miguel Godoy, CISO) del **21-10-2026, 17:00 hrs**
> (minuta: [`Documentacion/baseline/20261021_170000.txt`](../../baseline/20261021_170000.txt))
> **Tipo de cambio:** cambio de alcance **mayor** — módulos **Usuarios** (8) y **Ticketera** (9).

## 1. Resumen cuantitativo

| Elemento | Antes | Ahora |
|---|---|---|
| Módulos de negocio | 7 | **9** (+ Usuarios, + Ticketera) |
| Roles RBAC | 4 | **5** (+ `admin_sistema`) |
| Procesos BPMN | 3 | **5** (+ P4 Usuarios, + P5 Tickets) |
| Casos de uso | UC-01…UC-08 | UC-01…**UC-15** |
| Tablas de datos | 6 | **10** (+ `tickets`, `ticket_adjuntos`, `notificaciones`, `auditoria_usuarios`) |
| KPI | 8 | **11** (+ KPI-09, 10, 11) |
| Casos de prueba | CP-01…CP-19 | CP-01…**CP-38** |
| Servicios TI | — | + correo institucional / relay SMTP |

## 2. Cambios por entregable

| # | Entregable | Cambios |
|---|---|---|
| 01 | Análisis comparativo de tecnologías y metodologías | Alcance de 9 módulos; RBAC de 5 roles; factibilidad de correo SMTP; riesgos y seguridad del formulario público. |
| 02 | Herramientas, lenguajes, hardware y servicios TI | Librerías/servicios nuevos (SMTP, *rate limiting*, validación de adjuntos); correo institucional como servicio TI requerido; gestión de usuarios. |
| 03 | BPMN (procesos de negocio) | **P4 Gestión de usuarios** y **P5 Gestión de tickets** (formulario público, anonimización, notificación, análisis, derivación a incidente); P2 incorpora segundo origen (*ticket derivado*). Nuevos `03d_proceso_usuarios.drawio` y `03e_proceso_tickets.drawio`; actualizado `03b_proceso_incidentes.drawio`. |
| 04 | UML casos de uso y componentes | Nuevos actores `admin_sistema` y **Funcionario/denunciante anónimo** (sin autenticación); **UC-09…UC-15** (UC-09 gestionar usuarios, UC-10 gestionar roles y estado, UC-11 crear ticket público, UC-12 gestionar bandeja de tickets, UC-13 convertir ticket en incidente, UC-14 consultar estado por código, UC-15 notificar al equipo de ciberseguridad); componentes `usuarios`, `tickets`, `public_tickets`, `notificaciones` y SMTP. `.drawio` 04a y 04b actualizados. |
| 05 | Modelo de datos y diccionario | 4 tablas nuevas, enums (`Role`+`admin_sistema`, `TipoTicket`, `CategoriaTicket`, `EstadoTicket`, `MedioNotificacion`), relaciones y notas de privacidad/retención. Decisión de diseño: `tickets` **sin FK a usuarios** (anonimato). `.drawio` 05a actualizado. |
| 06 | Topología y comunicación | Flujo público HTTPS 443 sin autenticación desde la LAN; salida SMTP APP-01 → relay; nuevas reglas de firewall; zonas de usuarios (`admin_sistema`, funcionarios). `.drawio` 06a. |
| 07 | Infraestructura | Relay SMTP, *rate limiting* en Nginx, carpeta de adjuntos de tickets en NAS-01, respaldos de nuevas tablas/adjuntos. `.drawio` 07a. |
| 08 | Arquitectura de la solución | 9 módulos, interfaces nuevas (endpoint público, SMTP), decisiones arquitectónicas (anonimato sin FK, endpoint público con límite de tasa, notificación tolerante a fallos). `.drawio` 08a. |
| 09 | KPI SMART | **KPI-09** tiempo medio de primera respuesta a tickets (≤ 24 h hábiles), **KPI-10** % tickets gestionados en SLA (≥ 90 %), **KPI-11** baja de usuarios desvinculados (≤ 1 día hábil). |
| 10 | SLA | 5 roles; SLA de tickets (acuse ≤ 24 h hábiles; denuncias alta/crítica ≤ 4 h hábiles) y de baja de usuarios; disponibilidad del formulario público; excepción de acceso anónimo sólo al formulario público; adjuntos en RPO/RTO. |
| 11 | Plan de pruebas | **CP-20…CP-26** (Usuarios) y **CP-27…CP-38** (Ticketera: anonimato, "Otros", correo/bandeja, permisos, conversión a incidente, adjuntos, *rate limiting*, seguimiento); CP-19 precisado; usuario de prueba `admin.sistema`; matriz de trazabilidad. |
| 12 | Normas y estándares | ISO/IEC 27001 Anexo A 6.8, 5.15–5.18, 5.24–5.28, 8.2, 8.5, 8.15, 6.5; OWASP ASVS y API Security; Ley 21.719 (minimización); nota de validación jurídica. |
| 13 | Implementación y disponibilidad | Puesta en producción con SMTP, usuario `admin_sistema` inicial, capacitación a 5 roles y difusión del formulario público; disponibilidad del canal público. |
| 14 | Continuidad del servicio | Amenazas nuevas: abuso/spam del formulario, caída de SMTP, fuga/pérdida de adjuntos; medidas y rol `admin_sistema`. |
| 15 | Mantención | CI nuevos (relay SMTP, variables `SGSI_SMTP_*`, carpeta de tickets); cambio de alcance del 21-10-2026 gestionado como cambio **mayor**; diferencia entre ticketera de negocio e incidentes del propio SGSI. |
| 16 | Carta Gantt | Sprints de **Usuarios** y **Ticketera** (orden 1° Usuarios, 2° Ticketera) y registro del cambio de alcance; ES2 se mantiene el 11-12-2026. |
| 17 | Informe ABPro | Resumen ejecutivo, mapeo (5 procesos BPMN), justificación del cronograma y trabajos futuros (SSO/LDAP, integración con mesa de ayuda, cifrado de adjuntos). |
| — | `README.md` | Índice y nota de cambio de alcance con conteos actualizados. |

## 3. Diagramas

Los `.drawio` modificados/nuevos y sus exportaciones `.drawio.png` se regeneraron con la CLI de draw.io:
`03b`, `03d` (nuevo), `03e` (nuevo), `04a`, `04b`, `05a`, `06a`, `07a`, `08a`.
Los diagramas 04a y 05a tienen líneas que se cruzan: conviene ordenarlos manualmente en draw.io antes de la entrega final.

## 4. Implementación en código (posterior a esta documentación)

El diseño documentado se implementó en `sgsi/` (backend FastAPI y frontend React), junto con el rediseño visual
con la identidad del Hospital Clínico Félix Bulnes. Detalle técnico y cómo ejecutarlo: [`sgsi/README.md`](../../../sgsi/README.md).

## 5. Decisiones y supuestos a validar

1. Gestión de tickets con el rol `encargado` (sin rol de analista aparte).
2. `admin_sistema` no accede al contenido de tickets ni a módulos de negocio.
3. Formulario público restringido a la red interna del hospital.
4. Los umbrales de SLA/KPI nuevos son referenciales y deben validarse con el mandante.
5. El canal no sustituye canales formales de denuncia laboral: validar con el área jurídica.
