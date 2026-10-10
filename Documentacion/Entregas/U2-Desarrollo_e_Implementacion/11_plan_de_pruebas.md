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
| Seguridad | Validar autenticación, RBAC y confidencialidad | Equipo de desarrollo | Fase final |
| Rendimiento | Validar tiempos de respuesta y carga concurrente | Equipo de desarrollo | Fase final |

## 11.3 Ambiente de pruebas

| Elemento | Configuración |
|---|---|
| Backend | FastAPI + Uvicorn (puerto 8000), SQLite de prueba (BD desechable) |
| Frontend | Vite (puerto 5173) con proxy `/api` → 8000 |
| Datos | Datos de demostración generados por `python -m app.seed` |
| Usuarios de prueba | `miguel.godoy` (encargado), `maria.perez` (admin contratos), `juan.rojas` (referente), `patricia.silva` (director) — contraseña `demo123` |

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
| CP-19 | Seguridad | Sin acceso anónimo; RBAC aplicado; hash PBKDF2 en contraseñas |

## 11.5 Criterios de entrada y salida

- **Entrada:** código compilado (`tsc --noEmit` sin errores), BD de prueba cargada con `app.seed`.
- **Salida:** 100 % de casos funcionales críticos (CP-01 a CP-16) aprobados; defectos severos
  corregidos y re-ejecutados; aprobación UAT del Encargado de Ciberseguridad.

## 11.6 Matriz de trazabilidad (requisito ↔ prueba)

| Requisito (historia de usuario) | Casos de prueba |
|---|---|
| Autenticación y roles | CP-01, CP-02, CP-03, CP-07, CP-14 |
| Registrar controles y evidencias | CP-04, CP-05, CP-06 |
| Visualizar madurez | CP-08, CP-09 |
| Gestionar incidentes con plazos | CP-10, CP-11, CP-12 |
| Gestionar terceros y personas | CP-13, CP-14, CP-15 |
| Exportar reportes | CP-16 |
| Rendimiento y seguridad | CP-17, CP-18, CP-19 |

## 11.7 Herramientas de prueba

- **Swagger UI** (`/docs`) para pruebas manuales de la API.
- **Pytest** (pruebas unitarias/integración del backend).
- **Vitest / Testing Library** (pruebas de componentes frontend).
- Navegador para validación manual de la SPA.
