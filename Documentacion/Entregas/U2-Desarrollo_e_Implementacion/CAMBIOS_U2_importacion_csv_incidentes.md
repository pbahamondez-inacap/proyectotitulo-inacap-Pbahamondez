# Registro de cambios — Importación masiva de incidentes por CSV

> **Proyecto:** SGSI — Sistema de Gestión de Seguridad de la Información · Hospital Félix Bulnes Cerda
> **Entregable:** Unidad 2 — Desarrollo e Implementación (módulo Incidentes)
> **Tipo de cambio:** mejora funcional (no altera el alcance de módulos, roles ni tablas)
> **Fecha:** 28-10-2026

## 1. Resumen

Se agrega al módulo **Incidentes** la funcionalidad de **carga masiva de incidentes mediante archivo CSV**,
orientada a escenarios de contingencia o migración donde se requiere registrar muchos incidentes de una vez.

La solución se implementa íntegramente en el frontend y **respeta el contrato existente del backend**:
cada fila válida del CSV se envía con `POST /api/incidentes` usando el mismo esquema `IncidenteCreate` que
el formulario manual. No se agregaron endpoints ni tablas nuevas.

## 2. Solución implementada

| Archivo | Cambio |
|---|---|
| `sgsi/frontend/src/incidentesCsv.ts` | Nuevo: parser CSV, validación por fila, generación y descarga de la plantilla. |
| `sgsi/frontend/src/pages/Incidentes.tsx` | Botón **Importar CSV** (rol `encargado`) y ventana de importación con guía, plantilla, vista previa y resultado. |

Funcionalidades de la ventana de importación:

- **Guía de usuario integrada:** tabla con cada columna, si es obligatoria y los valores/formato aceptados.
- **Plantilla descargable:** `plantilla_incidentes.csv` (UTF-8 con BOM, encabezados y filas de ejemplo).
- **Vista previa** de filas válidas y listado de filas con error (número de fila y motivo).
- **Progreso y resultado:** contador de importación, totales de registros creados y fallos, y recarga de la tabla.

## 3. Contrato del backend respetado

La importación **no introduce un endpoint nuevo**. Por cada fila válida se realiza:

```
POST /api/incidentes
Content-Type: application/json
```

con el mismo cuerpo del formulario manual (`IncidenteCreate`):

| Campo | Origen en el CSV | Tipo / valores |
|---|---|---|
| `titulo` | `titulo` | string, obligatorio |
| `severidad` | `severidad` | `baja` · `media` · `alta` · `critica`, obligatorio |
| `fecha_deteccion` | `fecha_deteccion` | datetime, obligatorio (`AAAA-MM-DD` o `AAAA-MM-DD HH:MM`) |
| `descripcion` | `descripcion` | string |
| `categoria` | `categoria` | string (taxonomía ANCI) |
| `alcance` | `alcance` | `interno` (por defecto) · `externo` · `proveedor` |
| `sistema_afectado` | `sistema_afectado` | string |
| `estado` | `estado` | `registrado` (por defecto) · `en_analisis` · `contenido` · `resuelto` · `reportado` · `cerrado` |
| `reportado_anci` | `reportado_anci` | `SI`/`NO` · `true`/`false` · `1`/`0` (por defecto NO) |
| `notas` | `notas` | string |

## 4. Guía de uso para el usuario

1. En **Incidentes**, pulsar **Importar CSV** (visible solo para `encargado`).
2. Descargar la **plantilla CSV** desde el botón de la ventana.
3. Completar el archivo en UTF-8 respetando los encabezados (una fila por incidente).
4. Seleccionar el archivo: la ventana muestra la **vista previa** y las **filas con error**.
5. Pulsar **Importar**: las filas válidas se registran y se muestra el resultado final.

Validaciones aplicadas por fila (en el cliente, antes de enviar):

- Columnas obligatorias presentes: `titulo`, `severidad`, `fecha_deteccion`.
- Enumerados normalizados (tildes y mayúsculas aceptadas): severidad, alcance, estado.
- Fechas reales (`AAAA-MM-DD` o `AAAA-MM-DD HH:MM`); una fecha sin hora se interpreta a las 00:00.
- Booleano `reportado_anci` en los formatos aceptados.
- CSV tolerante a comillas, comas y saltos de línea dentro de un campo.

## 5. Verificación

- `npm run typecheck`: sin errores.
- `npm run build`: compilación de producción correcta.
- Pruebas del parser (Node): plantilla parseable, campos con comas/comillas, variantes de encabezado
  (p. ej. `Título`, `fecha_detección`), fechas, valores inválidos, columna faltante y archivo vacío.

## 6. Impacto en entregables U2

- **Entregable 11 (Plan de pruebas):** se sugiere agregar casos de prueba para la importación masiva
  (archivo válido, filas inválidas, plantilla descargable, permisos por rol).
- **Entregable 17 (Informe ABPro):** registrar la funcionalidad como mejora del módulo Incidentes.
- No cambian módulos, roles, tablas, BPMN ni UML: es una ampliación de la interfaz del módulo existente.
