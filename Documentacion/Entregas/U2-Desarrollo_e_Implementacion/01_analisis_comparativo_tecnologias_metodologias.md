# 1. Análisis comparativo de tecnologías y metodologías

> **Entregable 1 — Evaluación Sumativa 2 (ES2), Unidad 2 (Desarrollo e Implementación)**
> **Proyecto:** SGSI — Sistema de Gestión de Seguridad de la Información
> **Mandante:** Hospital Félix Bulnes Cerda (Miguel Godoy, Encargado de Ciberseguridad)
> **Asignatura:** Proyecto de Título TIHI84 · INACAP
> **Equipo:** Priscila Bahamóndez (Líder) + 2 integrantes

---

## 1.1 Objetivo del análisis

Seleccionar, mediante un análisis **cualitativo y cuantitativo**, las tecnologías (backend,
frontend, base de datos, infraestructura) y la **metodología de desarrollo** más adecuadas para
construir el SGSI del Hospital Félix Bulnes Cerda, considerando los **estudios de factibilidad
técnica, económica e implementativa** y las restricciones del proyecto (equipo de 3 estudiantes,
un semestre académico, infraestructura hospitalaria existente, nueve módulos funcionales y
obligaciones de la Ley N.º 21.663).

El alcance considera los siete módulos de negocio existentes y dos incorporaciones formalizadas por el Product Owner el 21-10-2026: **Módulo 8 — Usuarios** y **Módulo 9 — Ticketera**.

---

## 1.2 Metodología del análisis comparativo

Para que la comparación sea objetiva y replicable, se definió:

1. **Criterios de evaluación** ponderados según el impacto en el proyecto (Tabla 1).
2. **Escala cuantitativa** de 1 a 5 por criterio (1 = deficiente, 5 = excelente).
3. **Puntaje ponderado** = Σ (calificación × peso). La alternativa con mayor puntaje es la
   recomendada, y se valida con un **estudio de factibilidad** (técnica, económica, implementativa).

### Tabla 1 — Criterios y ponderación

| # | Criterio | Peso | Justificación |
|---|---|---|---|
| C1 | Madurez y estabilidad del ecosistema | 15 % | Reduce riesgo técnico en un sistema que debe ser auditable y mantenible. |
| C2 | Curva de aprendizaje / competencias del equipo | 20 % | Equipo de 3 estudiantes con plazo acotado de un semestre. |
| C3 | Seguridad (autenticación, control de acceso, protección de datos) | 20 % | El sistema gestiona información sensible de seguridad y debe cumplir la Ley 21.663. |
| C4 | Costo de licenciamiento y operación | 15 % | Presupuesto académico limitado; se prioriza software libre/open source. |
| C5 | Desempeño y escalabilidad | 10 % | Volumen transaccional bajo, pero debe soportar crecimiento institucional. |
| C6 | Integración e interoperabilidad | 10 % | Exportación de reportes, carga de evidencias, posible integración futura. |
| C7 | Soporte comunitario / documentación | 10 % | Disponibilidad de documentación y comunidad para resolver problemas. |
| | **Total** | **100 %** | |

---

## 1.3 Comparación de tecnologías de backend

El backend expone una **API REST** que concentra la lógica de negocio (controles ISO 27001,
cálculo de madurez, plazos legales de incidentes, terceros, personas, reportería, gestión de usuarios
y ticketera) y gestiona la autenticación JWT con control de acceso por **RBAC de cinco roles**.
El formulario público de tickets constituye una excepción deliberada a la autenticación y aplica
controles específicos de anonimato, validación y limitación de solicitudes.

### Tabla 2 — Comparación cualitativa de frameworks backend

| Criterio | FastAPI | Django | Flask | Node.js + Express |
|---|---|---|---|---|
| Lenguaje | Python 3 | Python 3 | Python 3 | JavaScript/TypeScript |
| Paradigma | Asíncrono (ASGI) | Síncrono (WSGI) | Síncrono (WSGI) | Asíncrono |
| Validación de datos | Pydantic (tipado) | Forms/Serializers | Manual | Manual/librerías |
| Documentación automática | Swagger/OpenAPI nativo | DRF-Spectacular | Swagger plugins | Swagger plugins |
| ORM | SQLAlchemy | Django ORM | SQLAlchemy | Prisma/Sequelize |
| Auth/JWT | Librerías (PyJWT) | DRF + JWT | Librerías | jsonwebtoken |
| Curva de aprendizaje | Media | Media-alta | Baja | Media |
| Comunidad/documentación | Alta | Muy alta | Alta | Muy alta |
| Desempeño | Alto (asíncrono) | Medio | Medio | Alto |
| Licencia | MIT (open source) | BSD | BSD | MIT |

### Tabla 3 — Matriz cuantitativa (escala 1–5 × peso)

| Criterio | Peso | FastAPI | Django | Flask | Node/Express |
|---|---|---|---|---|---|
| C1 Madurez | 15 % | 4 | 5 | 4 | 5 |
| C2 Curva aprendizaje | 20 % | 4 | 3 | 5 | 3 |
| C3 Seguridad | 20 % | 4 | 5 | 3 | 3 |
| C4 Costo | 15 % | 5 | 5 | 5 | 5 |
| C5 Desempeño | 10 % | 5 | 3 | 3 | 5 |
| C6 Integración | 10 % | 4 | 4 | 3 | 4 |
| C7 Soporte | 10 % | 4 | 5 | 4 | 5 |
| **Puntaje ponderado** | | **4.30** | **4.15** | **3.85** | **3.95** |

**Conclusión backend:** **FastAPI** obtiene el mayor puntaje. Su tipado con Pydantic garantiza la
integridad de los datos de entrada (crítico para un SGSI), genera documentación OpenAPI automática
(facilita pruebas y auditoría) y su modelo asíncrono es eficiente sin añadir la complejidad de
Django. Se descarta Django porque su curva de aprendizaje y acoplamiento a su propio ORM exceden lo
necesario para el alcance; Flask por requerir más ensamblaje manual de seguridad; Node/Express por
introducir un segundo lenguaje en el equipo, ya competente en Python.

---

## 1.4 Comparación de tecnologías de frontend

El frontend es una **SPA** con dashboard (gráficos de madurez), formularios de registro y gestión
por roles; incluye la administración de usuarios y el formulario público de tickets, accesible sin
autenticación.

### Tabla 4 — Comparación cualitativa de frameworks/librerías frontend

| Criterio | React + Vite | Angular | Vue 3 |
|---|---|---|---|
| Tipo | Librería UI | Framework completo | Framework progresivo |
| Lenguaje | TypeScript/JSX | TypeScript | TypeScript |
| Curva de aprendizaje | Media | Alta | Baja-media |
| Ecosistema de gráficos | Recharts (maduro) | ngx-charts | ECharts/Chart.js |
| Herramienta de build | Vite (rápido) | Angular CLI | Vite |
| Control de estado | Context/Redux | Servicios/RxJS | Pinia |
| Comunidad | Muy alta | Alta | Alta |
| Licencia | MIT | MIT | MIT |

### Tabla 5 — Matriz cuantitativa (escala 1–5 × peso)

| Criterio | Peso | React + Vite | Angular | Vue 3 |
|---|---|---|---|---|
| C1 Madurez | 15 % | 5 | 5 | 4 |
| C2 Curva aprendizaje | 20 % | 4 | 2 | 5 |
| C3 Seguridad | 20 % | 4 | 5 | 4 |
| C4 Costo | 15 % | 5 | 5 | 5 |
| C5 Desempeño | 10 % | 5 | 4 | 5 |
| C6 Integración | 10 % | 4 | 4 | 4 |
| C7 Soporte | 10 % | 5 | 5 | 4 |
| **Puntaje ponderado** | | **4.55** | **3.85** | **4.45** |

**Conclusión frontend:** **React 18 + TypeScript + Vite**. React lidera el ecosistema de
componentes y gráficos (Recharts), permite un desarrollo incremental acorde a Scrum y su curva de
aprendizaje es menor que la de Angular. Vue es una alternativa válida, pero React ofrece mayor
comunidad y compatibilidad con el perfil del equipo. Angular se descarta por su mayor rigidez y
tiempo de aprendizaje frente al plazo del semestre.

---

## 1.5 Comparación de bases de datos

El sistema persiste controles, evidencias, incidentes, contratos/terceros, controles de personas,
usuarios y tickets con sus adjuntos, notificaciones y auditoría; requiere **integridad referencial**,
**trazabilidad** y separación de los datos identificatorios del denunciante.

### Tabla 6 — Comparación cualitativa de motores de base de datos

| Criterio | PostgreSQL | MySQL/MariaDB | SQLite |
|---|---|---|---|
| Tipo | Relacional (SQL) | Relacional (SQL) | Relacional embebido |
| Integridad referencial | Completa | Completa | Completa |
| Transacciones/concurrencia | Alta | Alta | Media (bloqueo de escritura) |
| Administración | Requiere servidor | Requiere servidor | Sin servidor |
| Costo | Open source (PostgreSQL License) | Open source (GPL) | Dominio público |
| Despliegue | Servidor propio/nube | Servidor propio/nube | Archivo local |
| Uso recomendado | Producción / multiusuario | Producción | Desarrollo / bajo volumen |

### Tabla 7 — Matriz cuantitativa (escala 1–5 × peso)

| Criterio | Peso | PostgreSQL | MySQL | SQLite |
|---|---|---|---|---|
| C1 Madurez | 15 % | 5 | 5 | 5 |
| C2 Curva aprendizaje | 20 % | 4 | 4 | 5 |
| C3 Seguridad | 20 % | 5 | 4 | 3 |
| C4 Costo | 15 % | 5 | 5 | 5 |
| C5 Desempeño | 10 % | 5 | 4 | 2 |
| C6 Integración | 10 % | 5 | 4 | 3 |
| C7 Soporte | 10 % | 5 | 5 | 4 |
| **Puntaje ponderado** | | **4.85** | **4.35** | **3.85** |

**Conclusión base de datos:** **PostgreSQL** como motor de producción, con **SQLite** para
desarrollo y demostración. La solución se implementó sobre **SQLAlchemy**, que permite cambiar de
motor vía variable de entorno (`SGSI_DATABASE_URL`) **sin modificar código**, de modo que en
entornos reales se despliega PostgreSQL (auditoría, concurrencia multiusuario, respaldo) mientras
el desarrollo y las pruebas académicas usan SQLite (cero administración). Esta estrategia maximiza
la factibilidad implementativa sin sacrificar el camino a producción.

---

## 1.6 Comparación de metodologías de desarrollo

### Tabla 8 — Comparación cualitativa de metodologías

| Criterio | Scrum (ágil) | Kanban (ágil) | Cascada (predictiva) |
|---|---|---|---|
| Entrega de valor | Incremental (sprints) | Continua | Al final |
| Flexibilidad ante cambios | Alta | Alta | Baja |
| Interacción con el mandante | Frecuente (revisiones) | Continua | Puntual (hitos) |
| Documentación | Progresiva | Progresiva | Exhaustiva inicial |
| Gestión del alcance | Backlog priorizado | Flujo WIP | Alcance cerrado |
| Rol del equipo | Autoorganizado | Autoorganizado | Jerárquico |
| Adecuación a requisitos que cambian | Muy alta | Muy alta | Baja |

### Tabla 9 — Matriz cuantitativa (escala 1–5 × peso)

| Criterio | Peso | Scrum | Kanban | Cascada |
|---|---|---|---|---|
| C1 Madurez/formalidad | 15 % | 4 | 3 | 5 |
| C2 Adecuación al equipo | 20 % | 5 | 4 | 3 |
| C3 Retroalimentación del mandante | 20 % | 5 | 4 | 2 |
| C4 Gestión del alcance acotado | 15 % | 5 | 4 | 5 |
| C5 Control de tiempos (semestre) | 15 % | 5 | 3 | 4 |
| C6 Documentación académica exigida | 15 % | 4 | 3 | 5 |
| **Puntaje ponderado** | | **4.70** | **3.55** | **3.85** |

**Conclusión metodológica:** **Scrum (ágil)**. Los nueve módulos del SGSI (controles, evidencias,
madurez, incidentes, terceros, personas, reportería, usuarios y ticketera) se validan de forma
incremental con el mandante, cuya retroalimentación es clave para refinar el catálogo de controles y la taxonomía ANCI. El plazo
acotado del semestre se gestiona con sprints semanales e hitos de entrega (EF2 → ES2). Se descarta
Cascada porque el alcance se refina a medida que se revisan los controles reales del hospital; y
Kanban como marco único por su menor estructura de hitos formales, aunque sus tableros se usan como
herramienta de apoyo dentro del sprint.

---

## 1.7 Estudio de factibilidad

### 1.7.1 Factibilidad técnica

| Aspecto | Evaluación |
|---|---|
| Competencias del equipo | Python + TypeScript/React dentro de las competencias del equipo; documentación amplia. |
| Alcance y factibilidad funcional | Nueve módulos: los siete de negocio existentes más Usuarios (módulo 8) y Ticketera (módulo 9), incorporados al alcance formal. |
| Compatibilidad con infraestructura hospitalaria | Solución web desplegable en servidor propio o nube; no requiere integración en línea con Trakcare. El formulario público se sirve por HTTPS desde la red interna hospitalaria. |
| Seguridad requerida | RBAC de cinco roles: `encargado`, `admin_contratos`, `referente_tecnico`, `director` y `admin_sistema`. Este último solo administra usuarios; solo `encargado` gestiona tickets y procesos de negocio. |
| Seguridad del formulario público | Acceso anónimo sin JWT; no guardar identidad, IP, user-agent ni token del emisor. Aplicar HTTPS, validación estricta, lista blanca de adjuntos, límite aproximado de 10 MB, rate limiting (Nginx y/o middleware), honeypot/captcha simple y errores genéricos. |
| Notificaciones | Servicio de correo mediante relay SMTP institucional requerido para habilitar la notificación por email; el fallo de SMTP no bloquea el registro y se conserva la notificación en bandeja interna. |
| Rendimiento | Volumen transaccional bajo; FastAPI asíncrono y PostgreSQL/SQLite sobran para el alcance. |
| **Veredicto** | **Viable.** |

### 1.7.2 Factibilidad económica

| Aspecto | Evaluación |
|---|---|
| Licenciamiento | 100 % software libre/open source (MIT/BSD/PostgreSQL) → costo de licencias $0. |
| Infraestructura | Servidor reutilizable del hospital o nube de bajo costo; SQLite elimina costo en desarrollo. |
| Recursos humanos | Equipo académico (3 estudiantes) sin costo de contratación externa. |
| Mantenimiento | Comunidad activa y documentación gratuita; bajo costo de soporte futuro. |
| Notificaciones por correo | El uso del relay SMTP institucional existente evita licencias adicionales; requiere habilitación y configuración por TI. |
| **Veredicto** | **Viable — costo marginal cercano a $0.** |

### 1.7.3 Factibilidad implementativa

| Aspecto | Evaluación |
|---|---|
| Plazo (un semestre) | Sprints semanales con entregables priorizados; el stack elegido acelera el desarrollo. Se implementa primero Usuarios y luego Ticketera, según el acuerdo del 21-10-2026. |
| Disponibilidad de servicios | La operación de notificaciones por correo requiere que TI habilite una cuenta o relay SMTP institucional y los parámetros de conexión. |
| Gestión y separación de roles | Cinco roles RBAC; `admin_sistema` administra exclusivamente usuarios y no accede a datos de negocio ni a tickets. |
| Disponibilidad del mandante | Reuniones periódicas de revisión de sprint con el encargado de ciberseguridad. |
| Restricciones de datos | Uso de datos ficticios/anonimizados para pruebas (sin acceso a datos clínicos reales). |
| Riesgo de despliegue | Arquitectura monolítica modular de 3 capas: despliegue y mantenimiento simples. |
| **Veredicto** | **Viable.** |

---

## 1.8 Selección final justificada

| Capa | Tecnología seleccionada | Justificación resumida |
|---|---|---|
| Backend | **Python 3 + FastAPI + SQLAlchemy** | Tipado Pydantic, Swagger automático, asíncrono, seguridad estándar, curva de aprendizaje adecuada. |
| Autenticación | **JWT + RBAC de 5 roles** (PyJWT, PBKDF2) | `encargado`, `admin_contratos`, `referente_tecnico`, `director` y `admin_sistema`; permisos separados por función. |
| Alcance funcional | **9 módulos** (7 existentes + Usuarios y Ticketera) | Incluye administración de usuarios y formulario público anónimo de denuncias/reportes. |
| Notificaciones | **Servicio SMTP institucional** + bandeja interna | El correo notifica solo código, tipo, severidad y enlace; no incluye contenido sensible. |
| Base de datos | **PostgreSQL** (producción) / **SQLite** (desarrollo) | Integridad referencial y auditoría en producción; cero administración en desarrollo vía SQLAlchemy. |
| Frontend | **React 18 + TypeScript + Vite + Recharts** | Ecosistema maduro de gráficos para el dashboard de madurez; SPA rápida y mantenible. |
| Metodología | **Scrum (ágil)** | Validación incremental con el mandante y gestión del plazo del semestre. |
| Arquitectura | **Monolito modular en 3 capas** (presentación / API / datos) | Menor complejidad de despliegue sin renunciar a la separación por módulo de negocio. |

La combinación seleccionada es **técnicamente viable** (competencias del equipo y compatibilidad con
el entorno hospitalario), **económicamente viable** (software 100 % open source) e
**implementativamente viable** (plazo y despliegue acotados), garantizando la entrega de un sistema
auditable que apoya el cumplimiento de la Ley N.º 21.663 y de la norma ISO/IEC 27001:2022.

---

## 1.9 Referencias

- FastAPI. (s. f.). *FastAPI — Modern, fast (high-performance) web framework*. https://fastapi.tiangolo.com
- Django Software Foundation. (s. f.). *Django documentation*. https://docs.djangoproject.com
- React. (s. f.). *React — A JavaScript library for building user interfaces*. https://react.dev
- Vite. (s. f.). *Vite — Next generation frontend tooling*. https://vite.dev
- PostgreSQL Global Development Group. (s. f.). *PostgreSQL documentation*. https://www.postgresql.org/docs/
- SQLAlchemy. (s. f.). *The database toolkit for Python*. https://www.sqlalchemy.org
- Schwaber, K., & Sutherland, J. (2020). *The Scrum Guide*. https://scrumguides.org
- ISO/IEC. (2022). *ISO/IEC 27001:2022 — Information security, cybersecurity and privacy protection — Information security management systems — Requirements*.
- Biblioteca del Congreso Nacional de Chile. (2024). *Ley N.º 21.663 — Marco de Ciberseguridad e Infraestructura Crítica*. https://www.bcn.cl

> **Nota:** las referencias web son las fuentes oficiales de documentación de cada tecnología; el
> equipo debe completar las citas en formato APA 7.ª ed. con fecha de consulta al integrar este
> contenido en la plantilla ABPro del informe final.
