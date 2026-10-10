# 3. Diagramas BPMN de los procesos de negocio

> **Entregable 3 — Evaluación Sumativa 2 (ES2), Unidad 2 (Desarrollo e Implementación)**
> **Proyecto:** SGSI — Sistema de Gestión de Seguridad de la Información
> **Mandante:** Hospital Félix Bulnes Cerda (Miguel Godoy, Encargado de Ciberseguridad)
> **Criterio evaluado:** `2.1.2.3` — BPMN de al menos 3 procesos principales con sus subprocesos.

Este entregable modela **tres procesos principales** del negocio mediante notación BPMN 2.0, cada
uno con sus **subprocesos**, **actores (pools/carriles)**, **eventos**, **tareas**, **compuertas** y
**flujos de mensaje**. Cada proceso se entrega en dos formatos:

- **Mermaid** (incrustado aquí): se visualiza directamente en GitHub/VS Code.
- **`.drawio`**: archivo editable para abrir en draw.io (ver carpeta `03_bpmn/`).

---

## 3.1 Procesos seleccionados

| # | Proceso principal | Subprocesos | Archivo `.drawio` |
|---|---|---|---|
| P1 | Gestión de controles ISO/IEC 27001 | Registrar control, gestionar evidencia, actualizar estado, validar y aprobar, publicar madurez | `03a_proceso_controles_iso27001.drawio` |
| P2 | Gestión de incidentes de ciberseguridad | Clasificar (taxonomía ANCI), computar plazos, alertar, reportar, contener, cerrar | `03b_proceso_incidentes.drawio` |
| P3 | Gestión de terceros/proveedores (cláusulas de seguridad) | Registrar contrato, revisar checklist, verificar cumplimiento, corregir, publicar estado | `03c_proceso_terceros.drawio` |

**Notación utilizada:** piscinas (pools) para organizaciones externas, carriles (lanes) para roles
internos, círculo = evento, rectángulo = tarea, rectángulo con borde marcado = subproceso, rombo =
compuerta exclusiva (XOR), flecha punteada = flujo de mensaje, flecha continua = flujo de secuencia.

---

## 3.2 Proceso P1 — Gestión de controles ISO/IEC 27001

### Descripción

El Encargado de Ciberseguridad registra en el SGSI cada control del Anexo A de ISO/IEC 27001,
indicando su dominio (organizacional, personas, físico, tecnológico), descripción y estado inicial.
Si existe evidencia, se adjunta el documento de respaldo; luego se actualiza el estado (no iniciado /
iniciado / implementado / gestionado). El Referente Técnico o la Dirección validan la evidencia y,
si es aprobada, el control se marca como gestionado; en caso contrario vuelve a actualizarse. El
sistema recalcula el porcentaje de madurez y lo publica en el dashboard.

### Actores

| Actor | Tipo | Responsabilidad |
|---|---|---|
| Encargado de Ciberseguridad | Carril (interno) | Registrar controles, adjuntar evidencia, actualizar estado |
| Referente Técnico / Dirección | Carril (interno) | Validar cumplimiento y aprobar |
| Sistema SGSI | Carril (sistema) | Calcular madurez y publicar dashboard |

### Subprocesos

| Subproceso | Descripción |
|---|---|
| S1.1 Registrar control | Alta del control con dominio, descripción y estado inicial |
| S1.2 Gestionar evidencia | Adjuntar/retirar archivos de evidencia (acta, documento, certificado) |
| S1.3 Actualizar estado | Cambio de estado según nivel de avance (no iniciado → iniciado → implementado → gestionado) |
| S1.4 Validar y aprobar | Revisión de la evidencia y aprobación/rechazo del cumplimiento |
| S1.5 Publicar madurez | Recálculo del % de madurez por dominio/global y visualización en el dashboard |

### Diagrama (Mermaid)

```mermaid
flowchart TD
    subgraph A["Carril: Encargado de Ciberseguridad"]
        A1([Inicio]) --> A2[Identificar control del Anexo A a registrar]
        A2 --> A3[Registrar control: dominio, descripción, estado inicial]
        A3 --> G1{¿Existe evidencia?}
        G1 -- Sí --> A4[Adjuntar evidencia: acta / documento / certificado]
        G1 -- No --> A5
        A4 --> A5[Actualizar estado del control]
    end
    subgraph B["Carril: Referente Técnico / Dirección"]
        B1[(Subproceso: Validar cumplimiento y revisar evidencia)] --> G2{¿Control validado?}
        G2 -- Sí --> B2[Marcar control como gestionado]
    end
    subgraph C["Carril: Sistema SGSI"]
        C1[Calcular porcentaje de madurez y publicar en dashboard] --> C2([Fin: control visible])
    end
    A5 --> B1
    G2 -- No --> A5
    B2 --> C1
```

> **Archivo editable:** `03_bpmn/03a_proceso_controles_iso27001.drawio`

---

## 3.3 Proceso P2 — Gestión de incidentes de ciberseguridad

### Descripción

Un evento de seguridad detectado por TI (p. ej. falla en Trakcare, intento de ataque) se notifica al
Encargado de Ciberseguridad, quien lo clasifica según la **taxonomía ANCI** (tipo, alcance,
severidad). Si el evento no cumple los criterios para ser reportable, se registra como no reportable
y finaliza. Si corresponde reportar, el SGSI registra el incidente, **computa los plazos legales** de
la Ley 21.663 (alerta temprana 3 h; reporte 72 h para severidad alta/crítica o 15 días para
media/baja) y genera las alertas de vencimiento. El encargado **reporta al portal de la ANCI** y
realiza el seguimiento/contención hasta el cierre, dejando registro de la lección aprendida.

### Actores

| Actor | Tipo | Responsabilidad |
|---|---|---|
| TI / Informática (mesa de ayuda) | Carril (interno) | Detectar y notificar eventos |
| Encargado de Ciberseguridad | Carril (interno) | Clasificar, reportar, contener y cerrar |
| Sistema SGSI | Carril (sistema) | Computar plazos y alertar vencimientos |
| ANCI | Pool externo | Recepcionar el reporte oficial |

### Subprocesos

| Subproceso | Descripción |
|---|---|
| S2.1 Clasificar incidente | Aplicar taxonomía ANCI (tipo, alcance, severidad) |
| S2.2 Computar plazos legales | Calcular alerta temprana (3 h) y plazos de reporte (72 h / 15 días) |
| S2.3 Alertar vencimientos | Generar alertas de vencimiento de plazos |
| S2.4 Reportar a ANCI | Emitir el reporte oficial en el portal de la ANCI |
| S2.5 Contener y cerrar | Seguimiento/contención, cierre y lección aprendida |

### Diagrama (Mermaid)

```mermaid
flowchart TD
    subgraph TI["Carril: TI / Informática"]
        S2([Inicio]) --> T1[Detectar evento de seguridad]
        T1 --> T2[Notificar al Encargado de Ciberseguridad]
    end
    subgraph ENC["Carril: Encargado de Ciberseguridad"]
        T3[Clasificar según taxonomía ANCI] --> G1{¿Corresponde reportar a ANCI?}
        G1 -- No --> T4[Registrar como evento no reportable] --> E1([Fin])
        G1 -- Sí --> T5[Reportar a ANCI y realizar seguimiento / contención]
        T5 --> G2{¿Incidente resuelto?}
        G2 -- No --> T5
        G2 -- Sí --> T6[Cerrar incidente y registrar lección aprendida] --> E2([Fin])
    end
    subgraph SIS["Carril: Sistema SGSI"]
        T7[Registrar incidente y computar plazos 3h/72h/15d] --> T8[Generar alerta temprana y de vencimiento]
    end
    subgraph ANCI["Pool externo: ANCI"]
        T9[Recepcionar reporte del incidente]
    end
    T2 --> T3
    G1 -- Sí --> T7
    T8 --> T5
    T5 -. mensaje .-> T9
```

> **Archivo editable:** `03_bpmn/03b_proceso_incidentes.drawio`

---

## 3.4 Proceso P3 — Gestión de terceros/proveedores (cláusulas de seguridad)

### Descripción

El Administrador de Contratos recepciona un contrato o bases de licitación y registra al tercero. El
Encargado de Ciberseguridad revisa el **checklist de cláusulas de seguridad** exigidas al proveedor.
Si faltan cláusulas, se solicita el ajuste al proveedor, quien corrige y reenvía el contrato. Cuando
el checklist está completo, se verifica el cumplimiento con la documentación de respaldo; si no
cumple, se marca "no conforme" con plan de acción, y si cumple, se marca "conforme/habilitado" y se
publica el estado en el reporte de terceros.

### Actores

| Actor | Tipo | Responsabilidad |
|---|---|---|
| Administrador de Contratos | Carril (interno) | Recepcionar y registrar contratos/licitaciones |
| Encargado de Ciberseguridad | Carril (interno) | Revisar checklist, verificar cumplimiento y publicar estado |
| Proveedor / Tercero | Pool externo | Corregir/incorporar cláusulas de seguridad |

### Subprocesos

| Subproceso | Descripción |
|---|---|
| S3.1 Registrar contrato | Ingreso del tercero y del contrato/licitación |
| S3.2 Revisar checklist | Verificación de cláusulas de seguridad presentes en el contrato |
| S3.3 Verificar cumplimiento | Validación con documentación de respaldo |
| S3.4 Corregir contrato | Solicitud de ajuste al proveedor y recepción de correcciones |
| S3.5 Publicar estado | Actualizar estado (conforme / no conforme) y reporte de terceros |

### Diagrama (Mermaid)

```mermaid
flowchart TD
    subgraph ADM["Carril: Administrador de Contratos"]
        S3([Inicio]) --> A1[Recepcionar contrato / bases de licitación]
        A1 --> A2[Registrar tercero y contrato]
    end
    subgraph ENC["Carril: Encargado de Ciberseguridad"]
        B1[Revisar checklist de cláusulas de seguridad] --> G1{¿Cláusulas completas?}
        G1 -- Sí --> B2[Verificar cumplimiento con documentación]
        B2 --> G2{¿Cumple requisitos de seguridad?}
        G2 -- No --> B3[Marcar no conforme + plan de acción] --> E1([Fin])
        G2 -- Sí --> B4[Marcar conforme / habilitado]
        B4 --> B5[Actualizar estado y publicar en reporte de terceros] --> E2([Fin])
    end
    subgraph PROV["Pool externo: Proveedor / Tercero"]
        C1[Corregir / incorporar cláusulas de seguridad]
    end
    A2 --> B1
    G1 -. No solicitar ajuste .-> C1
    C1 -. reenvía contrato corregido .-> B1
```

> **Archivo editable:** `03_bpmn/03c_proceso_terceros.drawio`

---

## 3.5 Archivos `.drawio` generados

Los siguientes archivos se encuentran en la carpeta `03_bpmn/` y pueden abrirse directamente en
draw.io (escritorio o web) para su edición y exportación:

| Archivo | Proceso |
|---|---|
| `03_bpmn/03a_proceso_controles_iso27001.drawio` | P1 — Gestión de controles ISO/IEC 27001 |
| `03_bpmn/03b_proceso_incidentes.drawio` | P2 — Gestión de incidentes de ciberseguridad |
| `03_bpmn/03c_proceso_terceros.drawio` | P3 — Gestión de terceros/proveedores |

> **Nota:** los archivos `.drawio` usan la biblioteca de formas estándar (piscinas, carriles, tareas,
> eventos y compuertas) para una edición ágil. Si se requiere la notación BPMN 2.0 completa con
> íconos específicos, en draw.io se puede activar la biblioteca **"BPMN 2.0"** (`+ Más formas → BPMN`)
> y reemplazar cada forma por su equivalente BPMN manteniendo la estructura ya definida.
