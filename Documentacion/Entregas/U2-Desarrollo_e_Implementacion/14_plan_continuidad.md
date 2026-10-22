# 14. Plan de continuidad del servicio

> **Entregable 14 — Evaluación Sumativa 2 (ES2), Unidad 2 (Desarrollo e Implementación)**
> **Proyecto:** SGSI — Sistema de Gestión de Seguridad de la Información
> **Mandante:** Hospital Félix Bulnes Cerda (Miguel Godoy, Encargado de Ciberseguridad)
> **Criterio evaluado:** `2.1.5.14` — Procedimientos para impedir/minimizar las consecuencias de una
> grave interrupción (proactivos) y para reanudar el servicio lo antes posible (reactivos).

---

## 14.1 Objetivo

Garantizar la continuidad del SGSI ante interrupciones, combinando **medidas proactivas** (prevenir o
minimizar) y **medidas reactivas** (recuperar el servicio tras un desastre).

## 14.2 Análisis de riesgos y amenazas

| Amenaza | Impacto | Probabilidad | Medida principal |
|---|---|---|---|
| Falla de servidor de aplicaciones | Alto | Media | Documentación de reinstalación + respaldo de configuración |
| Pérdida/corrupción de BD o de datos de tickets | Crítico | Baja | Respaldo diario + RPO ≤ 24 h; incluir tablas `tickets`, `notificaciones` y `auditoria_usuarios` |
| Pérdida de evidencias (NAS) | Alto | Baja | Respaldo del NAS + réplica |
| Ataque/ransomware | Crítico | Media | Segmentación, respaldos offline, antivirus |
| Corte de energía | Medio | Media | UPS y generador de la sala de servidores |
| Error humano (cambio mal aplicado) | Medio | Media | Gestión de cambios controlada (Entregable 15) |
| Abuso o spam del formulario público | Alto | Media | Rate limiting, honeypot/captcha simple, validación y sanitización; no registrar IP del emisor en logs de aplicación |
| Caída del relay SMTP institucional | Medio | Media | La creación del ticket no depende del correo: bandeja interna, estado de envío y reintento; monitoreo del relay |
| Pérdida de adjuntos de tickets | Alto | Baja | Carpeta separada en NAS-01, respaldo junto con evidencias y pruebas de restauración dentro del RPO/RTO |
| Fuga de contenido de denuncias | Crítico | Baja | Acceso exclusivo de `encargado`, almacenamiento restringido, mínimo privilegio y revisión de auditoría; `admin_sistema` no accede al contenido |

## 14.3 Medidas proactivas (prevención y minimización)

| Medida | Descripción |
|---|---|
| Respaldo diario | Copia incremental diaria + completa semanal de BD y evidencias (BK-01) |
| Respaldo offline | Copia semanal en medio extraíble/offsite (protege contra ransomware) |
| Redundancia de disco | RAID1 en DB-01 (datos críticos) |
| Segmentación y firewalls | Aísla la aplicación y reduce la superficie de ataque |
| Monitoreo y alertas | Detección temprana de caídas (`/api/health`) |
| Documentación actualizada | Manual de instalación/recuperación y línea base de configuración |
| Gestión de cambios | Evita interrupciones por cambios no controlados |

## 14.4 Medidas reactivas (recuperación del servicio)

### 14.4.1 Objetivos de recuperación (coherentes con el SLA)

| Objetivo | Valor |
|---|---|
| **RPO** (pérdida máxima de datos) | ≤ 24 h para BD, evidencias y adjuntos de tickets en NAS-01 |
| **RTO** (tiempo de restablecimiento) | ≤ 8 h hábiles, incluyendo restauración de adjuntos de tickets y validación del formulario público |

### 14.4.2 Roles y responsabilidades

| Rol | Responsabilidad |
|---|---|
| Encargado de Ciberseguridad | Autoriza la activación del plan y comunica a la Dirección |
| Equipo de informática | Ejecuta la recuperación técnica |
| Administrador de contratos | Informa a proveedores si aplica |
| Dirección | Recibe reporte de estado |
| `admin_sistema` | Apoya recuperación técnica de cuentas, configuración de aplicación y permisos de almacenamiento; no consulta ni gestiona contenido de tickets |
| Encargado / equipo de ciberseguridad | Mantiene la continuidad operativa de la bandeja, prioriza tickets y evalúa si corresponde convertirlos en incidentes |

### 14.4.3 Procedimiento de recuperación (pasos)

1. **Detección y notificación:** el monitoreo o un usuario detecta la falla y notifica al equipo de
   informática.
2. **Evaluación:** se clasifica la severidad y se decide si se activa el plan.
3. **Activación:** el Encargado de Ciberseguridad autoriza la recuperación.
4. **Diagnóstico:** se identifica el componente afectado (aplicación, BD, NAS, red).
5. **Recuperación:**
   - Aplicación: reinstalar/reiniciar APP-01 desde la línea base de configuración.
   - Base de datos: restaurar el último respaldo válido en DB-01.
   - Evidencias y adjuntos: restaurar desde las carpetas respaldadas de NAS-01, incluyendo la ruta separada `/evidencias/tickets/`; verificar permisos restringidos.
   - Notificaciones: ante caída de SMTP, mantener la recepción de tickets y la bandeja interna; restablecer relay y procesar reintentos pendientes sin incluir contenido sensible en correos.
6. **Verificación:** validar `GET /api/health`, login por rol, formulario `/reportar` desde la red autorizada, creación de ticket sin identidad, estado de la bandeja y descarga controlada de adjuntos. No habilitar el canal hasta comprobar confidencialidad y disponibilidad.
7. **Comunicación:** informar a usuarios la reanudación del servicio.
8. **Lección aprendida:** registrar causa raíz y ajustar el plan.

## 14.5 Pruebas del plan

| Prueba | Frecuencia | Alcance |
|---|---|---|
| Restauración de BD y adjuntos de tickets desde respaldo | Trimestral | Validar RPO/RTO y permisos de NAS-01 |
| Continuidad ante caída SMTP | Semestral | Comprobar creación de ticket en bandeja, estado de envío y reintento posterior |
| Recuperación del formulario público | Semestral | Verificar disponibilidad desde red interna, rate limiting y anonimato |
| Simulacro de caída de aplicación | Trimestral | Validar procedimiento completo |
| Revisión del plan | Semestral | Actualizar roles, contactos y procedimientos |

## 14.6 Relación con otros entregables

- Objetivos RPO/RTO alineados con el SLA (Entregable 10).
- Respaldo ejecutado por BK-01 según la infraestructura (Entregable 7) y topología (Entregable 6).
- Cambios que puedan afectar la continuidad se gestionan por el plan de mantención (Entregable 15).
