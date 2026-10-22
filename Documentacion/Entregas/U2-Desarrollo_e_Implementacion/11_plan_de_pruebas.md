# 11. Plan de pruebas

> **Entregable 11 — Evaluación Sumativa 2 (ES2), Unidad 2 (Desarrollo e Implementación)**
> **Proyecto:** SGSI — Sistema de Gestión de Seguridad de la Información
> **Mandante:** Hospital Félix Bulnes Cerda (Miguel Godoy, Encargado de Ciberseguridad)
> **Criterio evaluado:** `2.1.4.11` — Plan de pruebas determinando y detallando las pruebas de
> software que se llevarán a cabo.

---

## 11.1 Estrategia y alcance

El plan cubre la validación funcional y no funcional del SGSI sobre **datos de prueba ficticios y
anonimizados** (sin acceso a datos clínicos reales), siguiendo un enfoque por niveles: pruebas
unitarias, de integración, de sistema, de aceptación (UAT) y no funcionales (seguridad y rendimiento).

## 11.2 Niveles de prueba

| Nivel | Objetivo | Responsable | Momento |
|---|---|---|---|
| Unitarias | Validar funciones aisladas (reglas de madurez y plazos legales) | Equipo de desarrollo | Durante el desarrollo |
| Integración | Validar la interacción API ↔ ORM ↔ BD y el flujo JWT/RBAC | Equipo de desarrollo | Al integrar módulos |
| Sistema | Validar flujos completos de cada módulo | Equipo de desarrollo | Antes de la entrega |
| Aceptación (UAT) | Validar con el mandante los flujos de negocio clave | Encargado de Ciberseguridad | Antes del cierre |
| Seguridad | Validar autenticación, RBAC, anonimato del canal público, rate limiting, manejo seguro de adjuntos y confidencialidad de denuncias | Equipo de desarrollo | Fase final |
| Rendimiento | Validar tiempos de respuesta y carga concurrente | Equipo de desarrollo | Fase final |

## 11.3 Ambiente de pruebas

| Elemento | Configuración |
|---|---|
| Backend | FastAPI + Uvicorn (puerto 8000), SQLite de prueba (BD desechable) |
| Frontend | Vite (puerto 5173) con proxy `/api` → 8000 |
| Datos | Datos de demostración generados por `python -m app.seed` |
| Correo | SMTP simulado (mock/relay de pruebas) para validar notificaciones sin enviar correo institucional real |
| Usuarios de prueba | `miguel.godoy` (`encargado`), `maria.perez` (`admin_contratos`), `juan.rojas` (`referente_tecnico`), `patricia.silva` (`director`) y `admin.sistema` (`admin_sistema`) — contraseña de demostración `demo123`; no reutilizar credenciales demo en producción |

## 11.4 Casos de prueba (principales)

### Módulo Autenticación

| ID | Caso | Pasos | Resultado esperado |
|---|---|---|---|
| CP-01 | Login exitoso | Ingresar `miguel.godoy` / `demo123` | Token JWT emitido; redirección al Dashboard |
| CP-02 | Login con credenciales inválidas | Ingresar clave incorrecta | Mensaje de error; sin token |
| CP-03 | Acceso sin token | Llamar `GET /api/controles` sin token | Error 401 |

### Módulo Controles / Evidencias

| ID | Caso | Pasos | Resultado esperado |
|---|---|---|---|
| CP-04 | Registrar control | `POST /api/controles` con dominio y título | Control creado con estado `no_iniciado` |
| CP-05 | Adjuntar evidencia | `POST /api/controles/{id}/evidencias` (multipart) | Evidencia asociada y descargable |
| CP-06 | Editar estado | `PUT /api/controles/{id}` con `gestionado` | Estado actualizado y fecha de actualización refrescada |
| CP-07 | Restricción por rol | `POST /api/controles` como `referente_tecnico` | Error 403 (sin permiso) |

### Módulo Madurez

| ID | Caso | Pasos | Resultado esperado |
|---|---|---|---|
| CP-08 | Cálculo de madurez | `GET /api/madurez` con controles en estados mixtos | % global = Σ pesos / total × 100, coherente con la regla |
| CP-09 | Dashboard | Abrir Dashboard | Gráficos de torta/barras por dominio renderizados |

### Módulo Incidentes

| ID | Caso | Pasos | Resultado esperado |
|---|---|---|---|
| CP-10 | Computar plazos | Registrar incidente severidad `critica` con fecha de detección | `alerta_temprana` = detección + 3 h; `plazo_reporte` = detección + 72 h |
| CP-11 | Plazo media/baja | Registrar incidente severidad `media` | `plazo_reporte` = detección + 15 días |
| CP-12 | Alerta de vencimiento | Simular incidente con plazo vencido | Campo `vencido` = true y alerta visible |

### Módulo Terceros / Personas / Reportes

| ID | Caso | Pasos | Resultado esperado |
|---|---|---|---|
| CP-13 | Registrar tercero con cláusulas | `POST /api/terceros` con cláusulas `[{nombre, cumplida}]` | Tercero creado; checklist persistido |
| CP-14 | Escritura por roles | `POST /api/terceros` como `admin_contratos` | Permitido; como `director` → 403 |
| CP-15 | Registrar control de personas | `POST /api/personas` con tipo `capacitacion` | Control creado con estado `no_iniciado` |
| CP-16 | Exportar CSV | `GET /api/reportes/controles.csv` | Archivo CSV descargable (compatible con Excel) |

### Pruebas no funcionales

| ID | Caso | Criterio de aceptación |
|---|---|---|
| CP-17 | Rendimiento API | p95 ≤ 500 ms en operaciones CRUD típicas |
| CP-18 | Carga concurrente | ≥ 10 usuarios simultáneos sin degradación |
| CP-19 | Seguridad general | El acceso anónimo se deniega para todos los recursos salvo el formulario público de tickets, sus categorías y la consulta de estado por código; RBAC aplicado; contraseñas con hash PBKDF2 |

### Módulo Usuarios

| ID | Caso | Pasos | Resultado esperado |
|---|---|---|---|
| CP-20 | Crear usuario | Autenticarse como `admin.sistema` y crear usuario con `username`, nombre completo, clave inicial y rol | Usuario creado con rol asignado; la acción queda auditada |
| CP-21 | Editar rol/datos | Como `admin.sistema`, cambiar nombre, `username` o rol de una cuenta existente | Datos actualizados y cambio registrado en `auditoria_usuarios` |
| CP-22 | Deshabilitar usuario | Deshabilitar una cuenta de prueba e intentar iniciar sesión y usar un token previo | Baja lógica; login y token de usuario inactivo rechazados |
| CP-23 | Impedir autodeshabilitación | Intentar deshabilitar la propia cuenta activa de `admin.sistema` | Operación rechazada; sesión y cuenta se mantienen activas |
| CP-24 | Proteger último `admin_sistema` | Intentar deshabilitar o degradar el último administrador de sistema activo | Operación rechazada; se mantiene al menos un `admin_sistema` activo |
| CP-25 | Restringir administración de usuarios | Llamar `/api/usuarios` con cada rol distinto de `admin_sistema` | Acceso denegado con HTTP 403 |
| CP-26 | Auditar cambios de usuarios | Crear, editar rol/datos, restablecer contraseña y habilitar/deshabilitar una cuenta | `auditoria_usuarios` registra actor, acción, fecha y detalle, sin guardar contraseñas en claro |

### Módulo Ticketera

| ID | Caso | Pasos | Resultado esperado |
|---|---|---|---|
| CP-27 | Crear ticket público sin token | Enviar formulario público sin JWT con datos válidos | HTTP 201; se asigna código y el ticket no queda asociado a un usuario |
| CP-28 | Validar categoría Otros | Enviar categoría `otros` primero sin y luego con texto libre | Sin `categoria_otro` se rechaza; con descripción se acepta |
| CP-29 | Verificar anonimato con sesión activa | Crear ticket mientras existe una sesión autenticada y revisar registro, adjuntos y logs de aplicación | No se guarda identidad, FK a usuario, token, IP ni user-agent del emisor; anonimato se conserva aun con sesión activa |
| CP-30 | Notificación por bandeja | Crear ticket con notificación interna seleccionada | Notificación pendiente visible para destinatarios `encargado` |
| CP-31 | Notificación por correo | Crear ticket con correo seleccionado usando SMTP simulado | Relay de prueba recibe correo con código, tipo, severidad y enlace; sin contenido sensible |
| CP-32 | Seleccionar ambos medios | Crear ticket con correo y bandeja seleccionados | Se generan ambas notificaciones; fallo SMTP no impide crear ni conservar el ticket en la bandeja |
| CP-33 | Confidencialidad de la bandeja | Consultar y gestionar tickets como `encargado`, otro rol y `admin_sistema` | Solo `encargado` accede al contenido; los demás reciben HTTP 403 |
| CP-34 | Cambiar estado | Como `encargado`, mover ticket por el ciclo registrado → en análisis → cerrado | Estado válido persistido con trazabilidad; otros roles no pueden modificarlo |
| CP-35 | Convertir ticket en incidente | Como `encargado`, derivar ticket a incidente y completar taxonomía ANCI | Incidente vinculado; ticket pasa a `derivado_a_incidente`; se calculan plazos legales de 3 h, 72 h o 15 días según corresponda |
| CP-36 | Validar adjuntos | Enviar archivos permitidos y luego un tipo no permitido o que exceda el límite configurado | Archivos válidos aceptados; tipo/tamaño inválido rechazado sin exponer ruta interna |
| CP-37 | Limitar abuso del formulario | Superar el umbral configurado de solicitudes públicas | Rate limiting bloquea o ralentiza solicitudes excedentes sin afectar tickets válidos |
| CP-38 | Consultar estado por código | Consultar con código de seguimiento válido e inválido | Se informa solo estado/código; nunca identidad, descripción ni datos sensibles del ticket |

## 11.5 Criterios de entrada y salida

- **Entrada:** compilación y validaciones estáticas sin errores; BD desechable cargada con datos ficticios; cinco cuentas de prueba disponibles, incluida `admin.sistema`; SMTP simulado operativo; almacenamiento de adjuntos aislado; límites de solicitudes del endpoint público configurados.
- **Salida:** CP-01 a CP-16 y CP-20 a CP-38 funcionales críticos aprobados; anonimato, controles de acceso, rate limiting y validación de adjuntos verificados; defectos severos corregidos y re-ejecutados; aprobación UAT del Encargado de Ciberseguridad. CP-17 a CP-19 se aprueban según sus criterios no funcionales.

## 11.6 Matriz de trazabilidad (requisito ↔ prueba)

| Requisito (historia de usuario) | Casos de prueba |
|---|---|
| Autenticación y roles | CP-01, CP-02, CP-03, CP-07, CP-14 |
| Registrar controles y evidencias | CP-04, CP-05, CP-06 |
| Visualizar madurez | CP-08, CP-09 |
| Gestionar incidentes con plazos | CP-10, CP-11, CP-12 |
| Gestionar terceros y personas | CP-13, CP-14, CP-15 |
| Exportar reportes | CP-16 |
| Gestionar usuarios, roles y auditoría | CP-20 a CP-26 |
| Crear, notificar y gestionar tickets de forma confidencial | CP-27 a CP-36 |
| Protección del canal público y consulta anónima | CP-29, CP-36 a CP-38 |
| Rendimiento y seguridad | CP-17, CP-18, CP-19, CP-25, CP-29, CP-33, CP-36, CP-37 |

## 11.7 Herramientas de prueba

- **Swagger UI** (`/docs`) para pruebas manuales de la API.
- **Pytest** (pruebas unitarias/integración del backend).
- **Vitest / Testing Library** (pruebas de componentes frontend).
- Navegador para validación manual de la SPA.
