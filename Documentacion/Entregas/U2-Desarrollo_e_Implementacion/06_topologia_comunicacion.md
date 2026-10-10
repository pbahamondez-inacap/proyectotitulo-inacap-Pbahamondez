# 6. Diagrama de topología de comunicación

> **Entregable 6 — Evaluación Sumativa 2 (ES2), Unidad 2 (Desarrollo e Implementación)**
> **Proyecto:** SGSI — Sistema de Gestión de Seguridad de la Información
> **Mandante:** Hospital Félix Bulnes Cerda (Miguel Godoy, Encargado de Ciberseguridad)
> **Criterio evaluado:** `2.1.2.6` — Diagrama de la topología de comunicación que da soporte a la solución.

Este entregable describe la **topología de red** que soporta el SGSI, organizada en zonas de
seguridad separadas por firewalls, con los protocolos y puertos de cada flujo de comunicación. La
topología sigue el principio de **defensa en profundidad** y **mínimo privilegio**: los usuarios
acceden solo a la aplicación, la aplicación accede solo a los datos, y la zona de datos queda
aislada de la red de usuarios.

---

## 6.1 Descripción general

La solución se despliega en **tres zonas de comunicación**:

| Zona | Contenido | Función |
|---|---|---|
| **Zona de usuarios (LAN hospitalaria)** | Estaciones de trabajo de los usuarios (Encargado de Ciberseguridad, Administrador de Contratos, Referente Técnico, Director/a) y switch de acceso. | Acceso a la aplicación vía navegador (HTTPS). |
| **Zona DMZ (servidores)** | Firewall perimetral, servidor web/aplicación (SPA + FastAPI/uvicorn) y firewall interno. | Publicar la aplicación y aplicar la lógica de negocio. |
| **Zona de datos (aislada)** | Servidor PostgreSQL, almacenamiento de evidencias (NAS) y servidor de respaldo. | Persistencia y respaldo; accesible solo desde la capa de aplicación. |

### 6.1.1 Decisiones clave

- **Aislamiento de la red clínica:** el SGSI **no se conecta** a Trakcare ni a la red asistencial;
  es un sistema de apoyo administrativo. Con esto se evita exponer el sistema clínico crítico.
- **Sin integración en línea con la ANCI:** el reporte de incidentes al portal ANCI lo realiza el
  Encargado de Ciberseguridad por el canal institucional (no existe conexión API del SGSI a la
  ANCI). En el diagrama se representa como flujo externo (línea punteada).
- **Firewall doble:** un firewall perimetral separa usuarios de la DMZ y un firewall interno separa
  la DMZ de la zona de datos.

---

## 6.2 Diagrama de topología (Mermaid)

```mermaid
flowchart LR
    subgraph LAN["Zona de usuarios (LAN hospitalaria)"]
        U1["Encargado de Ciberseguridad"]
        U2["Administrador de Contratos"]
        U3["Referente Técnico"]
        U4["Director/a"]
        SW["Switch de acceso"]
        U1 --- SW
        U2 --- SW
        U3 --- SW
        U4 --- SW
    end

    subgraph DMZ["Zona DMZ (servidores)"]
        FW1["Firewall perimetral"]
        WEB["Servidor web/aplicación<br>(Frontend SPA + FastAPI/uvicorn)"]
        FW2["Firewall interno (BD)"]
    end

    subgraph DATOS["Zona de datos (aislada)"]
        DB[("PostgreSQL")]
        NAS[("Almacenamiento de evidencias (NAS)")]
        BK["Servidor de respaldo"]
    end

    EXT["Internet / Portal ANCI<br>(flujo institucional)"]

    SW -->|"HTTPS 443"| FW1
    FW1 -->|"HTTPS 443"| WEB
    WEB -->|"TCP 5432"| FW2
    FW2 -->|"TCP 5432"| DB
    WEB -->|"SMB/NFS (archivos)"| NAS
    WEB -->|"backup programado"| BK
    U1 -.->|"reporte vía portal (manual)"| EXT
```

---

## 6.3 Componentes de comunicación

| Componente | Zona | Función | Protocolo / Puerto |
|---|---|---|---|
| Estaciones de trabajo (4) | Usuarios | Acceso a la SPA vía navegador | HTTPS 443 |
| Switch de acceso | Usuarios | Conectividad LAN de los usuarios | Ethernet |
| Firewall perimetral | DMZ | Filtra el tráfico de usuarios hacia la aplicación | HTTPS 443 (solo) |
| Servidor web/aplicación | DMZ | Sirve la SPA y ejecuta la API FastAPI/uvicorn | HTTPS 443 (entrada) |
| Firewall interno | DMZ/Datos | Restringe el acceso a la base de datos | TCP 5432 (solo desde la app) |
| Servidor PostgreSQL | Datos | Persistencia de la base de datos | TCP 5432 |
| Almacenamiento de evidencias (NAS) | Datos | Guarda los archivos de evidencia | SMB/NFS |
| Servidor de respaldo | Datos | Copias de seguridad de BD y evidencias | Backup (rsync/agente) |

---

## 6.4 Flujos de comunicación

| # | Origen | Destino | Protocolo/Puerto | Propósito |
|---|---|---|---|---|
| F1 | Estaciones de trabajo | Firewall perimetral | HTTPS 443 | Solicitudes de la SPA. |
| F2 | Firewall perimetral | Servidor web/aplicación | HTTPS 443 | Entrega de la aplicación. |
| F3 | Servidor web/aplicación | Firewall interno | TCP 5432 | Consultas a la base de datos. |
| F4 | Firewall interno | PostgreSQL | TCP 5432 | Acceso a datos (solo lectura/escritura de la app). |
| F5 | Servidor web/aplicación | NAS | SMB/NFS | Carga/descarga de evidencias. |
| F6 | Servidor web/aplicación | Servidor de respaldo | Backup | Copias periódicas. |
| F7 | Estación del Encargado | Portal ANCI (Internet) | HTTPS 443 | Reporte institucional de incidentes (manual, sin integración). |

---

## 6.5 Nota sobre aislamiento con la red clínica

El SGSI es un sistema de **apoyo/gobernanza**, no asistencial. Por ello se mantiene **físicamente y
lógicamente aislado** de la red clínica (Trakcare): no existen flujos de comunicación entre ambas
redes. Si en el futuro se requiriera consultar datos clínicos, se haría mediante exportación manual
y anonimizada, nunca con conexión directa.

---

## 6.6 Archivos `.drawio` generados

| Archivo | Diagrama |
|---|---|
| `06_topologia/06a_topologia_comunicacion.drawio` | Topología de comunicación (3 zonas + firewalls + flujos). |

> **Nota:** los dispositivos de red se representan con formas estándar (rectángulos, cilindros para
> BD/NAS). Para íconos específicos (firewall, switch, servidor), en draw.io usa la biblioteca
> **"Redes"** (`+ Más formas → Redes`).
