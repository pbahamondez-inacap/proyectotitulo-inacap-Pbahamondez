# Registro de cambios — Unidad 1 (Formulación del Proyecto)

> **Proyecto:** SGSI — Sistema de Gestión de Seguridad de la Información · Hospital Félix Bulnes Cerda
> **Documento afectado:** [`borrador_informe_formulacion.md`](./borrador_informe_formulacion.md)
> **Origen del cambio:** reunión con el Product Owner (Miguel Godoy, CISO) del **21-10-2026, 17:00 hrs**
> (minuta: [`Documentacion/baseline/20261021_170000.txt`](../../baseline/20261021_170000.txt))
> **Tipo de cambio:** cambio de alcance **mayor** (incorpora dos módulos al producto).

---

## 1. Resumen del cambio de alcance

| # | Módulo incorporado | Descripción | Quién lo usa |
|---|---|---|---|
| 8 | **Usuarios** (CRUD) | Alta, edición, asignación de roles, restablecimiento de contraseña y **baja lógica** de usuarios desvinculados, con auditoría (quién/qué/cuándo). | Solo el nuevo rol `admin_sistema` |
| 9 | **Ticketera** (denuncias y reportes de incidentes) | Formulario para reportar denuncias o incidentes de ciberseguridad, **anónimo** y con **versión pública sin autenticación**; categoría desde catálogo + "Otros" (texto libre); notificación al equipo de ciberseguridad por correo y/o bandeja interna (seleccionable); conversión del ticket a incidente formal (taxonomía ANCI y plazos Ley 21.663). | Cualquier funcionario del hospital (emisor); `encargado` (gestión) |

Consecuencias de alcance: la solución pasa de **7 a 9 módulos**, de **4 a 5 roles** (nuevo `admin_sistema`),
de **6 a 10 tablas** y se agrega un servicio de correo (SMTP) y un endpoint público acotado a la red interna.

## 2. Cambios por sección del informe

| Sección | Cambio realizado |
|---|---|
| **I. Introducción** | Se menciona el canal de reporte interno anónimo y la administración de accesos como parte del alcance. |
| **II. Identificación del problema** (2.1, 2.2) | Se agregan dos brechas: (a) ausencia de un canal confidencial/anónimo para que funcionarios reporten incidentes o denuncias (el módulo de incidentes sólo lo alimenta el analista del CISO); (b) falta de una interfaz de administración de usuarios y de baja de personal desvinculado. |
| **III. Levantamiento de requerimientos** | Nuevas historias de usuario y requerimientos funcionales de Usuarios y Ticketera; nuevos **RNF**: anonimato, confidencialidad de denuncias, auditoría de administración de usuarios, disponibilidad y protección del canal público contra abuso. Se registra la reunión del 21-10-2026 como instrumento de levantamiento. |
| **V. 5.1 Solución tecnológica** | La lista de módulos pasa a 9 (se añaden Usuarios y Ticketera) y se actualiza el alcance. |
| **V. 5.2 Impacto** | Nuevos interesados: funcionarios/denunciantes y Administrador de Sistema; nuevos indicadores **KPI-09** (tiempo medio de primera respuesta a tickets), **KPI-10** (% de tickets gestionados dentro de SLA) y **KPI-11** (deshabilitación de desvinculados ≤ 1 día hábil). |
| **V. 5.3 Objetivos** | Objetivos específicos ampliados para el módulo de usuarios (RBAC con 5 roles) y para la ticketera anónima. |
| **VI. Metodología** | Se registra el cambio de alcance del 21-10-2026 gestionado como incremento del backlog Scrum (orden: 1° Usuarios, 2° Ticketera) y su efecto en el cronograma. |
| **VII. 7.2 Diseño de la solución** | Diagrama de arquitectura (mermaid) con routers `usuarios`, `tickets`, `public_tickets`, servicio de notificaciones y SMTP; modelo conceptual de datos ampliado (tickets, adjuntos, notificaciones, auditoría); RBAC de 5 roles. |
| **VII. 7.3 Seguridad** | Endpoint público: HTTPS, restricción a la LAN, *rate limiting*, validación de adjuntos, sin registro de IP del emisor; separación de funciones (`admin_sistema` no ve tickets). |
| **VIII. Arquitectura empresarial** | Tablas de capas actualizadas (aplicación, datos, tecnología: correo institucional/SMTP) y compatibilidad con la arquitectura existente. |
| **IX. Conclusiones** | Se actualiza el listado de módulos y el aporte del canal anónimo a la cultura de reporte (ISO/IEC 27001 A.6.8). |

> Los marcadores `[PENDIENTE]` del borrador **no se modificaron**.

## 3. Decisiones y supuestos a validar con el Product Owner

1. El equipo de ciberseguridad gestiona los tickets con el rol existente `encargado` (no se crea un rol de analista separado).
2. `admin_sistema` **no** accede al contenido de tickets ni a módulos de negocio (separación de funciones).
3. El formulario público queda **restringido a la red interna** del hospital (no expuesto a Internet) salvo decisión contraria.
4. El canal **no sustituye** canales formales de denuncia laboral/funcionaria: validar con el área jurídica del hospital.
5. El anonimato prima sobre cualquier dato identificatorio: sin FK a usuarios, sin IP/user-agent, aun si el emisor tiene sesión iniciada.
