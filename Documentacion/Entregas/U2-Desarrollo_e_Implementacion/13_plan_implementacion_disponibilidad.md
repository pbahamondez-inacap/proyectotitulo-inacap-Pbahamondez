# 13. Plan de implementación y gestión de disponibilidad

> **Entregable 13 — Evaluación Sumativa 2 (ES2), Unidad 2 (Desarrollo e Implementación)**
> **Proyecto:** SGSI — Sistema de Gestión de Seguridad de la Información
> **Mandante:** Hospital Félix Bulnes Cerda (Miguel Godoy, Encargado de Ciberseguridad)
> **Criterio evaluado:** `2.1.5.13` — Servicios TI asociados al desarrollo de la solución, asegurando
> que infraestructura, procesos, herramientas y funciones de TI sean adecuados para cumplir los
> objetivos de disponibilidad propuestos.

---

## 13.1 Objetivo

Definir el **plan de implementación** (puesta en producción) y la **gestión de disponibilidad** del
SGSI, garantizando que el servicio cumpla la disponibilidad objetivo (≥ 99 % en horario
administrativo, Entregable 10).

## 13.2 Estrategia de implementación

Se usa un despliegue por **fases con ambientes progresivos** (desarrollo → pruebas → producción),
minimizando el riesgo y validando cada etapa:

| Fase | Ambiente | Actividades | Criterio de paso |
|---|---|---|---|
| 1. Desarrollo | Local (SQLite) | Construcción de módulos y pruebas unitarias | `tsc --noEmit` OK + pruebas unitarias verdes |
| 2. Integración | Staging (PostgreSQL) | Migración de datos de prueba, pruebas de sistema y UAT | Casos CP-01 a CP-16 aprobados |
| 3. Puesta en producción | Producción | Instalación en APP-01/DB-01/NAS-01, migración, capacitación | Aprobación del Encargado de Ciberseguridad |
| 4. Operación | Producción | Monitoreo, respaldo y mantención continua | SLA cumplido |

### Actividades clave de implementación

1. Preparar el servidor de aplicaciones (Linux + Nginx + Python 3.14 + Uvicorn).
2. Instalar PostgreSQL y crear la base `sgsi` (variable `SGSI_DATABASE_URL`).
3. Compilar la SPA (`npm run build`) y publicarla en Nginx.
4. Configurar HTTPS/TLS y el proxy inverso hacia Uvicorn.
5. Configurar firewalls (HTTPS 443 y TCP 5432) según la topología (Entregable 6).
6. Cargar datos iniciales y crear usuarios con roles.
7. Capacitar a los 4 roles de usuario.
8. Activar monitoreo y respaldo.

## 13.3 Gestión de disponibilidad

### 13.3.1 Objetivo de disponibilidad

- Disponibilidad mensual ≥ 99 % en horario administrativo (08:00–17:00).
- Ventanas de mantenimiento planificadas fuera del horario, notificadas con ≥ 48 h.

### 13.3.2 Proceso de gestión de disponibilidad

| Actividad | Descripción | Frecuencia |
|---|---|---|
| Monitoreo | Verificación del endpoint `GET /api/health` y de los servicios (Nginx, Uvicorn, PostgreSQL) | Continua |
| Medición | Cálculo de uptime mensual y registro de indisponibilidades | Mensual |
| Análisis | Revisión de incidentes que afectaron disponibilidad y de su causa raíz | Mensual |
| Mejora | Acciones correctivas/preventivas (redundancia, ajuste de capacidad) | Continua |
| Reporte | Informe de disponibilidad al Encargado de Ciberseguridad | Mensual |

### 13.3.3 Elementos que aseguran la disponibilidad

| Elemento | Aporte a la disponibilidad |
|---|---|
| Firewall doble y segmentación | Aísla la aplicación de la red de usuarios y de la red clínica |
| Respaldo diario (BK-01) | Permite recuperar datos ante fallas |
| Monitoreo del endpoint de salud | Detección temprana de caídas |
| Arquitectura 3 capas | Facilita diagnóstico y mantenimiento sin afectar otras capas |
| Documentación y gestión de cambios | Reduce errores por cambios no controlados (Entregable 15) |

## 13.4 Capacidad y rendimiento

- Dimensionamiento inicial: APP-01 (2 vCPU/4 GB) y DB-01 (2 vCPU/4 GB), suficientes para ≤ 10
  usuarios concurrentes (Entregable 7).
- Escalamiento futuro: vertical (más CPU/RAM) o separación de servicios, según crecimiento.
