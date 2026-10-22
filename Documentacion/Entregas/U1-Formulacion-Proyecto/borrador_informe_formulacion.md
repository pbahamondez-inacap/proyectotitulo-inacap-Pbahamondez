# FORMULACIÓN DEL PROYECTO DE TÍTULO

> Borrador de contenido para copiar/adaptar en `TIHI84_U1_Plantilla_informe_Guía_ABPro.docx`.
> Los bloques marcados con **[PENDIENTE]** requieren datos institucionales oficiales (organigrama,
> misión/visión, presupuesto real, etc.) que el equipo debe validar directamente con el mandante
> (Hospital Félix Bulnes Cerda) antes de la entrega, ya que no fueron proporcionados en la entrevista
> base y no deben inventarse ni copiarse de fuentes externas sin verificar.
>
> **Actualizado para ES1:** la guía de Evaluación Sumativa 1 (`TIHI84_U1_ES1_GUÍA.txt`) agrega a la
> ponderación las Actividades 7 y 8 (arquitectura TI y arquitectura empresarial, secciones VII y VIII)
> y evalúa con escala Excelente/Bueno/Insatisfactorio en lugar del Sí/No de la EF1. Por eso ambas
> secciones se desarrollaron aquí con mayor profundidad (plan de diseño concreto), y se cuidó el uso
> de lenguaje formal/técnico y la coherencia problema→solución→conclusión (criterio 1.1.6).

**Asignatura:** Proyecto de Título – TIHI84
**Sección:** [PENDIENTE: completar]
**Académico guía:** Luis Bravo
**Referente / encargado de seguridad (mandante):** Miguel Godoy — Hospital Félix Bulnes Cerda
**Integrantes del equipo:** Priscila Bahamóndez (Líder) + 2 integrantes [PENDIENTE: completar]

**Nombre tentativo del proyecto:** Sistema de Gestión de Seguridad de la Información (SGSI) para el
seguimiento de madurez de controles ISO/IEC 27001 e incidentes de ciberseguridad — Hospital Félix
Bulnes Cerda.

---

## I. Introducción

El Hospital Félix Bulnes Cerda, establecimiento público de alta complejidad perteneciente a la Red
Asistencial del Servicio de Salud Metropolitano Occidente, ha sido declarado **Operador de
Importancia Vital (OIV)** en el marco de la Ley N.º 21.663 sobre Marco de Ciberseguridad e
Infraestructura Crítica. Esta condición obliga al establecimiento a mantener un nivel de madurez
verificable en la implementación de controles de seguridad de la información (ISO/IEC 27001) y a
reportar incidentes de ciberseguridad a la Agencia Nacional de Ciberseguridad (ANCI) dentro de plazos
legales estrictos.

Actualmente, el seguimiento del estado de los controles del Sistema de Gestión de Seguridad de la
Información (SGSI) se realiza de manera manual y dispersa (planillas, correos, actas), sin una
herramienta centralizada que permita visualizar el nivel de madurez alcanzado ni gestionar de forma
estructurada la evidencia de cumplimiento. Este informe formula un proyecto orientado a diseñar e
implementar una solución tecnológica de tipo GRC (Governance, Risk & Compliance) que permita al
encargado de ciberseguridad del hospital administrar usuarios, recibir denuncias y reportes de incidentes mediante una ticketera, además de
registrar controles, evidencias, incidentes y proveedores, visualizando de manera gráfica el avance del
SGSI institucional.

*(Se recomienda redactar la versión final de esta introducción al terminar el resto del informe,
resumiendo en una página los puntos II a VIII.)*

---

## II. Identificación del Problema

### 2.1 Actualización y justificación del problema

#### 2.1.1 Descripción de la organización

- **Tipo y rubro:** Institución pública de salud, establecimiento hospitalario de alta complejidad,
  dependiente del Servicio de Salud Metropolitano Occidente (SSMOCC), Ministerio de Salud de Chile.
- **Posicionamiento:** Hospital de referencia para la comuna de Cerro Navia y sectores aledaños de la
  Región Metropolitana, con atención de urgencia adulto, infantil y obstétrica, hospitalización y
  atención ambulatoria.
- **Estructura organizacional (organigrama):** **[PENDIENTE]** — incorporar organigrama oficial,
  ubicando la Unidad/Encargado de Ciberseguridad y su dependencia (habitualmente bajo Subdirección de
  Gestión de la Información o Dirección del establecimiento).
- **Misión y Visión:** **[PENDIENTE]** — citar textualmente desde fuente institucional oficial
  (PEI o sitio web del hospital), con referencia APA.
- **Cadena de valor / Cuadro de mando integral:** **[PENDIENTE]** — a completar por el equipo en base
  a procesos asistenciales (admisión, atención, egreso) y de apoyo (TI, ciberseguridad, abastecimiento).
- **Estándares adoptados y certificaciones:** ISO/IEC 27001:2022 (en proceso de implementación, no
  certificado aún), Ley N.º 21.663 (Marco de Ciberseguridad e Infraestructura Crítica), Ley N.º 19.628 /
  21.719 sobre Protección de Datos Personales, taxonomía de incidentes ANCI.
- **Arquitectura tecnológica y de aplicaciones:** Sistema clínico centralizado **Trakcare** (registro
  de admisión, ficha clínica electrónica, gestión de urgencias adulto/infantil), con soporte de mesa
  de ayuda interna (08:00–17:00, equipo de informática del hospital) y mesa de ayuda del proveedor
  InterSystems (17:00–06:59 del día siguiente).
- **Unidades de negocio/procesos afectados:** Urgencia, hospitalización, atención ambulatoria,
  informática, abastecimiento/licitaciones y la unidad de ciberseguridad institucional.

#### 2.1.2 Descripción del problema

El hospital cuenta con un catálogo de controles de seguridad (basado en las categorías organizacional,
de personas, física y tecnológica de ISO/IEC 27001 Anexo A) cuyo estado de avance —no iniciado,
iniciado, implementado, gestionado— y evidencia asociada se registran de forma manual y no
estandarizada. No existe un repositorio único que permita saber, para cada grupo de control, cuántos
controles existen, cuál es su estado y qué evidencia lo sustenta (p. ej. registros de capacitación,
actas de reunión firmadas, cláusulas contractuales, revisiones de antecedentes). Como consecuencia:

- No es posible calcular ni comunicar de manera visual el **nivel de madurez** (%) del SGSI por
  dominio ni de forma global, dificultando la rendición de cuentas ante la Dirección y ante organismos
  reguladores.
- La gestión de **incidentes de ciberseguridad** no está integrada a una clasificación formal según la
  taxonomía de la ANCI, lo que genera incertidumbre sobre si un evento debe reportarse y en qué plazo
  (3 horas para alerta temprana, 72 horas y 15 días según severidad, conforme a la Ley 21.663).
- El control de cláusulas de seguridad en **contratos, licitaciones y acuerdos de confidencialidad**
  con terceros/proveedores es incompleto y disperso, al igual que los controles del ciclo de vida del
  personal (verificación de antecedentes, condiciones de empleo, proceso disciplinario,
  responsabilidades post-término).
- El reporte de incidentes depende actualmente del analista del CISO y no existe un canal formal
  interno ni un formulario público que permita a funcionarios u otras personas del hospital presentar
  denuncias o reportes, incluso de forma anónima. Esto dificulta la detección temprana y puede inhibir
  la comunicación de hechos sensibles.
- La administración de cuentas se realiza mediante carga inicial o seed, sin una interfaz para crear,
  revisar, modificar, habilitar o deshabilitar usuarios y sus roles. La falta de baja lógica oportuna
  debilita el control de acceso y la trazabilidad cuando una persona deja el hospital.

### 2.2 Justificación del problema

#### 2.2.1 Relevancia del problema

El hospital tiene obligaciones legales directas (Ley 21.663 como OIV, Ley de Protección de Datos
Personales sobre fichas clínicas) cuyo cumplimiento se mide, entre otros, mediante un indicador de
gestión institucional asociado al avance de implementación del SGSI (referido en la entrevista con el
mandante como "compromiso/meta 15.4" — **[PENDIENTE: verificar nombre oficial exacto del indicador con
el mandante]**). El incumplimiento expone al hospital a sanciones normativas y, más relevante aún, a
riesgos sobre la continuidad de la atención de pacientes y la confidencialidad de su información
clínica (ejemplo real reportado: incidente de ransomware con exfiltración de historial clínico
completo, clasificado como severidad crítica).

#### 2.2.2 Complejidad del problema

La complejidad radica en la heterogeneidad de los controles a gestionar (organizacionales, de
personas, físicos y tecnológicos), la multiplicidad de tipos de evidencia (documentos, actas, registros
digitales), la necesidad de trazabilidad temporal (plazos legales de reporte de incidentes) y la
participación de actores con responsabilidades distintas (encargado de ciberseguridad, administrador
de contratos, referente técnico, admin_sistema, funcionarios denunciantes y proveedores externos como
InterSystems). Se requiere proteger la confidencialidad de las denuncias y separar la administración
técnica de usuarios de la gestión de los tickets. A esto se suma la ausencia actual de un sistema de
información dedicado, por lo que parte de la gestión depende de trabajo manual y memoria institucional.

---

## III. Levantamiento de Requerimientos

### Instrumentos utilizados

- **Entrevista semiestructurada** con el encargado de ciberseguridad del Hospital Félix Bulnes Cerda
  (Miguel Godoy), enfocada en el estado actual de gestión del SGSI, incidentes y controles de
  terceros/personas.
- **[PENDIENTE]** Complementar con observación directa de las planillas/repositorios actuales y,
  si es posible, una segunda entrevista o encuesta a otros stakeholders (informática, abastecimiento).

### Principales requerimientos identificados (resumen; ver detalle en Anexos)

**Requerimientos funcionales (historias de usuario):**

- Como encargado de ciberseguridad, quiero registrar cada control ISO 27001 con su dominio, estado y
  evidencia asociada, para tener trazabilidad del cumplimiento.
- Como encargado de ciberseguridad, quiero visualizar el nivel de madurez por dominio y global en
  gráficos (torta/barra), para comunicar el avance a la Dirección de forma comprensible.
- Como encargado de ciberseguridad, quiero registrar incidentes según la taxonomía ANCI y recibir
  alertas de vencimiento de los plazos de reporte (3 h / 72 h / 15 días), para cumplir la Ley 21.663.
- Como encargado de ciberseguridad, quiero registrar cláusulas de seguridad de proveedores y
  controles del ciclo de vida de las personas, para evidenciar su cumplimiento.
- Como Administrador de Sistema (admin_sistema), quiero listar, crear usuarios con nombre completo,
  username, contraseña inicial y rol, editar sus datos y rol, restablecer contraseñas y habilitar o
  deshabilitar cuentas, para administrar los accesos; cada operación debe quedar auditada y la baja
  será lógica. No podré deshabilitar mi propia cuenta ni deshabilitar o degradar al último admin_sistema
  activo.
- Como funcionario o denunciante del hospital, quiero crear desde el formulario público, sin iniciar
  sesión, un ticket de tipo denuncia o reporte_incidente, e indicar categoría de un catálogo (phishing,
  malware/ransomware, acceso no autorizado, fuga de información, uso indebido de datos, falla/caída de
  servicio, pérdida/robo de equipo, incumplimiento de políticas u Otros), descripción, sistema/área
  afectada, fecha y hora aproximada, severidad percibida (baja, media, alta o crítica) y adjuntos
  opcionales. Si selecciono Otros, informaré una categoría en texto libre. Puedo elegir notificación por
  correo, bandeja interna o ambos; la identidad no se vinculará al ticket aunque se indique como
  identificado.
- Como encargado de ciberseguridad, quiero revisar la bandeja confidencial, cambiar el estado del
  ticket y, cuando corresponda, convertirlo en incidente formal con taxonomía ANCI y plazos legales.
- Como denunciante anónimo, quiero consultar el estado de mi ticket con un código de seguimiento,
  sin acceder a datos sensibles ni tener que revelar mi identidad.

**Requerimientos no funcionales:**

- **Anonimato:** los tickets no almacenarán nombre, correo, IP, user-agent, token de sesión ni FK al
  usuario que reporta; la identidad tampoco será visible ni asociable cuando se indique voluntariamente.
- **Confidencialidad:** el contenido y los adjuntos de tickets solo serán accesibles al encargado de
  ciberseguridad; admin_sistema no tendrá acceso al contenido de la ticketera.
- **Control de acceso y auditoría:** RBAC para cinco roles; solo admin_sistema administra usuarios,
  con trazabilidad de quién, qué y cuándo para altas, cambios, restablecimientos y estados.
- **Disponibilidad y protección frente a abuso:** canal público disponible en la red interna por
  HTTPS, con limitación de solicitudes, validación estricta de datos y adjuntos, y manejo de errores
  sin detalles internos.
- Confidencialidad e integridad de la información del SGSI, cifrado en tránsito y protección de
  archivos en repositorios con permisos restringidos.
- Compatibilidad con la infraestructura tecnológica existente del hospital.

*(Se sugiere incluir en Anexos el listado completo de requerimientos documentado bajo IEEE 830 o
historias de usuario, según el método adoptado por el equipo.)*

---

## IV. Marco Teórico

Temas a desarrollar con revisión bibliográfica formal (APA 7ª ed.):

1. **Sistemas de Gestión de Seguridad de la Información (SGSI)** y la norma **ISO/IEC 27001:2022**
   (ciclo PDCA, Anexo A y sus 4 categorías de controles: organizacionales, de personas, físicos y
   tecnológicos) y **ISO/IEC 27002:2022** (guía de implementación de controles).
2. **Marco normativo chileno de ciberseguridad:** Ley N.º 21.663 (Marco de Ciberseguridad e
   Infraestructura Crítica), rol de la Agencia Nacional de Ciberseguridad (ANCI), concepto de
   "Operador de Importancia Vital" y taxonomía de incidentes.
3. **Protección de datos personales en salud:** Ley N.º 19.628 y su actualización por la Ley
   N.º 21.719, aplicada a fichas clínicas electrónicas.
4. **Modelos de madurez de seguridad de la información** (p. ej. CMMI aplicado a seguridad, modelos de
   madurez de controles ISO 27001) como sustento metodológico para calcular y visualizar el % de
   avance.
5. **Herramientas GRC (Governance, Risk and Compliance)** y buenas prácticas de dashboards de
   cumplimiento normativo en el sector salud.
6. **Metodologías de desarrollo de software** (predictiva vs. ágil) aplicables a un sistema de gestión
   documental/dashboard como el propuesto.

*(El equipo debe buscar, seleccionar y citar fuentes reales —libros, papers, normas oficiales— para
cada punto; este listado es solo la estructura temática a cubrir.)*

---

## V. Objetivos del Proyecto

### 5.1 Solución tecnológica

#### 5.1.1 Formulación de la Solución

Se propone diseñar e implementar un **Sistema de Gestión de Seguridad de la Información (SGSI)**,
materializado como una aplicación web de tipo GRC, que centralice:

1. **Gestión de controles ISO/IEC 27001** — catálogo por dominio, estado y evidencia de cumplimiento.
2. **Gestión de evidencias** — carga y trazabilidad documental asociada a controles y registros.
3. **Cálculo y visualización de madurez** — indicadores por dominio, grupo de control y consolidado.
4. **Gestión de incidentes** — clasificación ANCI, cómputo de plazos legales (3 h, 72 h, 15 días) y
   alertas de vencimiento.
5. **Gestión de terceros/proveedores** — verificación de cláusulas de seguridad en contratos y
   licitaciones.
6. **Gestión de controles de personas** — capacitaciones, antecedentes, condiciones de empleo,
   confidencialidad y término de contrato.
7. **Reportería para cumplimiento normativo** — informes exportables para gestión y auditorías.
8. **Gestión de usuarios** — altas, edición, asignación de roles, restablecimiento de contraseñas y
   habilitación/deshabilitación lógica con auditoría; acceso exclusivo de admin_sistema.
9. **Ticketera de denuncias y reportes** — formulario público sin autenticación, registro anónimo,
   notificaciones seleccionables por correo y/o bandeja interna, gestión confidencial por el encargado
   y conversión a incidente cuando corresponda.

La solución busca reemplazar el trabajo manual disperso (planillas, correos, actas) por un sistema
único, auditable y con visualización orientada a la toma de decisiones de la Dirección del hospital.

#### 5.1.2 Alcance y restricciones

**Dentro del alcance:**
- Los nueve módulos descritos en 5.1.1: controles, evidencias, madurez, incidentes, terceros,
  personas, reportería, usuarios y ticketera.
- Administración de usuarios solo por admin_sistema: alta, edición, rol, restablecimiento de
  contraseña y baja lógica, sin borrado físico, con prevención de deshabilitarse a sí mismo o al último
  administrador de sistema activo y con registro de auditoría. Un usuario deshabilitado no podrá iniciar
  sesión ni acceder al sistema, incluso si conserva un token previo.
- Formulario público /reportar sin autenticación, disponible en la red interna del hospital, y acceso
  desde el menú autenticado; creación de tickets anónimos, consulta de estado mediante código,
  adjuntos opcionales y selección de notificación por correo institucional y/o bandeja interna.
- Bandeja de tickets y gestión de su ciclo de vida exclusiva del encargado; conversión a incidente
  formal con taxonomía ANCI y plazos legales cuando corresponda.
- RBAC con cinco roles y separación entre administración técnica y gestión de contenidos de negocio.
- Medidas de seguridad para la ticketera: HTTPS, limitación de solicitudes, validación y restricción
  de adjuntos, almacenamiento separado y confidencial, y notificaciones sin incluir contenido sensible.

**Fuera del alcance (propuesto para otra instancia):**
- Integración automática/en tiempo real con Trakcare u otros sistemas clínicos.
- Reporte automatizado directo a la plataforma de la ANCI (integración API oficial).
- Certificación formal ISO 27001 del hospital (el sistema apoya la gestión, no reemplaza la auditoría
  de certificación).

**Restricciones:** tiempo del semestre académico, disponibilidad del mandante para validar
requerimientos, ausencia de acceso a datos reales de pacientes (se usarán datos ficticios/anonimizados
para pruebas).

### 5.2 Impacto de la solución

#### 5.2.1 Proceso de negocio afectado

Principalmente el proceso de **gestión de seguridad de la información y cumplimiento normativo**,
liderado por el encargado de ciberseguridad, con participación de funcionarios y denunciantes del
hospital mediante el canal de reportes, y del administrador de sistema para la gestión técnica de
cuentas. Interactúa con TI/informática (soporte técnico), abastecimiento (licitaciones/contratos) y
recursos humanos (controles de personas).

#### 5.2.2 Registro de Interesados

| Interesado | Rol | Interés/Impacto |
|---|---|---|
| Encargado de Ciberseguridad (Miguel Godoy) | Mandante / usuario principal | Gestionar incidentes, bandeja y tickets; supervisar el SGSI |
| Funcionarios y denunciantes del hospital | Usuarios internos o actores anónimos | Informar denuncias y reportes mediante el formulario público sin revelar identidad |
| Administrador de Sistema (admin_sistema) | Administrador técnico | Gestionar cuentas, roles y estados con trazabilidad; sin acceso al contenido de tickets |
| Dirección del Hospital | Patrocinador | Visibilidad de cumplimiento y riesgo |
| Equipo de Informática | Soporte técnico | Mantención de la plataforma, HTTPS, almacenamiento y correo |
| Administrador de Contratos | Usuario secundario | Registro de cláusulas de seguridad |
| Proveedor Trakcare (InterSystems) | Tercero | Referencia de soporte, no usuario directo |
| ANCI (Agencia Nacional de Ciberseguridad) | Ente regulador | Receptor final de reportes formales de incidentes |

*(Completar siguiendo formato PMBOK: poder/interés, estrategia de gestión, etc.)*

#### 5.2.3 Indicadores de gestión

- % de madurez global del SGSI (meta institucional vinculada al indicador de gestión "15.4" —
  **[PENDIENTE: confirmar nombre oficial]**).
- % de controles con evidencia registrada por dominio.
- N.º de incidentes reportados dentro de plazo legal vs. fuera de plazo.
- % de contratos/licitaciones con cláusulas de seguridad verificadas.
- **KPI-09 — Tiempo medio de primera respuesta a tickets:** tiempo desde registrado hasta en análisis,
  con meta de ≤ 24 horas hábiles.
- **KPI-10 — Gestión de tickets dentro de SLA:** porcentaje de tickets que avanzan desde registrado
  a otro estado dentro del SLA aplicable, con meta ≥ 90 %.
- **KPI-11 — Cobertura de deshabilitación de cuentas:** porcentaje de usuarios desvinculados
  deshabilitados dentro de 24 horas (o 1 día hábil) desde la solicitud, con meta ≥ 100 %.
- Los tickets convertidos en incidentes reportables mantienen los plazos legales medidos por KPI-03.

#### 5.2.4 Niveles de servicio

**[PENDIENTE]** — definir junto al mandante (ej. disponibilidad del sistema en horario administrativo,
tiempo de respuesta de soporte, tiempo máximo para registrar un incidente desde su detección).

### 5.3 Objetivos del proyecto

#### 5.3.1 Objetivo General

Desarrollar un Sistema de Gestión de Seguridad de la Información (SGSI) que permita al Hospital Félix
Bulnes Cerda registrar, medir y visualizar el nivel de madurez de sus controles ISO/IEC 27001, gestionar
incidentes de ciberseguridad conforme a la Ley 21.663, administrar usuarios con roles y auditoría, y
recibir denuncias y reportes anónimos mediante una ticketera confidencial, con el fin de fortalecer su
capacidad de cumplimiento normativo y toma de decisiones en seguridad de la información.

#### 5.3.2 Objetivos Específicos

1. Diseñar el modelo de datos del SGSI para sus diez tablas: Control, Evidencia, Incidente,
   Tercero, PersonaControl, Usuario, tickets, ticket_adjuntos, notificaciones y auditoria_usuarios,
   preservando el anonimato y la trazabilidad de la información.
2. Implementar los módulos de controles, evidencias, cálculo de madurez, incidentes, terceros,
   personas y reportería para apoyar el cumplimiento de ISO/IEC 27001 y la Ley 21.663.
3. Implementar la administración de usuarios con RBAC de cinco roles, acceso exclusivo de
   admin_sistema, baja lógica y auditoría de las operaciones sensibles.
4. Implementar la ticketera con formulario público anónimo, bandeja confidencial, notificaciones
   seleccionables por correo y/o bandeja, consulta segura de estado y conversión a incidente formal.
5. Definir controles de seguridad y disponibilidad para proteger el anonimato, la confidencialidad y
   la trazabilidad, y reducir el abuso del endpoint público.
6. Validar los módulos y sus permisos mediante pruebas funcionales con datos de prueba representativos
   y participación del encargado de ciberseguridad del hospital.

---

## VI. Metodología de Trabajo

### 6.1 Metodología de Desarrollo de la solución

Se propone una metodología **ágil (Scrum)**, dada la necesidad de validar de forma incremental los
nueve módulos (controles, evidencias, madurez, incidentes, terceros, personas, reportería, usuarios y
ticketera) directamente con el mandante, priorizando la retroalimentación y refinando los requerimientos
en el backlog a medida que se revisa la solución. **[PENDIENTE: justificar formalmente con marco teórico y
confirmar con el equipo si se adoptará metodología predictiva en su lugar.]**

### 6.2 Duración y cronograma

Duración total: 5 semanas (según guía EF1/ES1). **[PENDIENTE: detallar carta Gantt con hitos semanales:
S1 formulación y organización de equipo, S2 levantamiento de requerimientos y marco teórico, S3 entrega
EF1, S4 retroalimentación y ajustes, S5 entrega ES1.]**

**Registro de cambio de alcance (21-10-2026):** por acuerdo con el Product Owner se incorporan los
módulos Usuarios y Ticketera, junto con el rol admin_sistema y el formulario público anónimo. El cambio
se gestiona en el backlog y se prioriza en este orden: 1) Usuarios; 2) Ticketera (backend y frontend,
formulario público y notificaciones). La planificación debe absorber el trabajo mediante solapamiento y
holgura, manteniendo como hito ES2 el 11-12-2026.

### 6.3 Equipo de trabajo

**[PENDIENTE]** Matriz RACI por actividad (Responsable, Aprueba, Consultado, Informado) para cada
integrante del equipo (Priscila Bahamóndez + 2 integrantes por definir), rotando el rol de líder.

### 6.4 Plan de recursos

**[PENDIENTE]** Detallar recursos humanos (equipo de 3 estudiantes + académico guía + mandante),
tecnológicos (entorno de desarrollo, hosting de prueba) y de tiempo. Elaborar presupuesto estimado si
corresponde.

---

## VII. Definición de arquitectura TI

### 7.1 Necesidad de integración con sistemas existentes

El hospital opera **Trakcare** como sistema clínico crítico (ficha clínica electrónica, admisión,
urgencias). Se evaluó si el SGSI requiere integrarse en tiempo real con Trakcare y **se concluye que
no**: el SGSI es un sistema de apoyo/gobierno (gestión documental de cumplimiento), no un sistema
asistencial, por lo que integrarlo en línea con Trakcare añadiría riesgo técnico y regulatorio
innecesario a un sistema crítico, sin aportar valor al objetivo del proyecto. En cambio, sí existen
**puntos de integración asíncrona** necesarios:

- Referenciar, dentro de un registro de incidente del SGSI, el sistema/módulo afectado (p. ej.
  "Trakcare – módulo de admisión de urgencias") como dato descriptivo, sin conexión directa a la base
  clínica.
- Exportar reportes (PDF/Excel) del nivel de madurez e incidentes para sustentar el indicador de
  gestión institucional ante la Dirección y organismos reguladores.
- Permitir la carga manual de evidencia generada en otros sistemas (actas firmadas, correos,
  certificados de capacitación) como archivos adjuntos.

Esta decisión responde directamente al criterio de evaluación *"Define la arquitectura TI
verificando la necesidad de integración con otros sistemas"*.

### 7.2 Plan de diseño de la solución (arquitectura propuesta)

Se propone una **aplicación web en 3 capas** (presentación, lógica de negocio, datos), de tipo
cliente-servidor, organizada en los nueve módulos del punto 5.1.1, con un formulario público separado
lógicamente de las rutas autenticadas:

```mermaid
flowchart TB
    subgraph Presentacion["Capa de Presentación"]
        UI["SPA interna: dashboard y nueve módulos"]
        PUB["Formulario público /reportar (sin autenticación)"]
    end
    subgraph Aplicacion["Capa de Aplicación (API REST)"]
        AUTH["Autenticación y autorización RBAC"]
        RBAC["5 roles: encargado, admin_contratos, referente_tecnico, director, admin_sistema"]
        CTRL["Módulo Controles ISO 27001"]
        EVID["Módulo Evidencias"]
        MAD["Módulo Madurez"]
        INC["Módulo Incidentes (ANCI + plazos)"]
        TERC["Módulo Terceros / Proveedores"]
        PERS["Módulo Personas"]
        REP["Módulo Reportería / Exportación"]
        USR["Módulo Usuarios (solo admin_sistema)"]
        TICK["Módulo Ticketera / bandeja (solo encargado)"]
        PTICK["API pública: POST /api/public/tickets; GET /api/public/tickets/categorias y GET /api/public/tickets/{codigo_seguimiento}"]
        NOTIF["Servicio de notificaciones: correo y bandeja interna"]
    end
    subgraph Datos["Capa de Datos"]
        DB[("Base relacional: 10 tablas")]
        FILES[("Repositorio de evidencias")]
        ADJ[("NAS-01 /evidencias/tickets/, acceso restringido")]
        SMTP[("SMTP institucional / relay")]
    end

    UI --> AUTH
    AUTH --> RBAC
    UI --> CTRL
    UI --> EVID
    UI --> MAD
    UI --> INC
    UI --> TERC
    UI --> PERS
    UI --> REP
    UI --> USR
    UI --> TICK
    PUB --> PTICK
    CTRL --> DB
    EVID --> DB
    MAD --> DB
    INC --> DB
    TERC --> DB
    PERS --> DB
    REP --> DB
    USR --> DB
    TICK --> DB
    TICK --> INC
    TICK --> ADJ
    TICK --> NOTIF
    PTICK --> DB
    PTICK --> ADJ
    PTICK --> NOTIF
    NOTIF --> DB
    NOTIF --> SMTP
    CTRL --> FILES
    EVID --> FILES
    INC --> FILES
    TERC --> FILES
    PERS --> FILES
```

**Modelo de datos conceptual:** las seis tablas preexistentes (Control, Evidencia, Incidente,
Tercero/Proveedor, PersonaControl y Usuario) se amplían con cuatro nuevas, por un total de diez:
**tickets**, **ticket_adjuntos**, **notificaciones** y **auditoria_usuarios**. Usuario conserva el estado
activo y uno de los cinco roles. auditoria_usuarios registra actor, usuario objetivo, acción, detalle y
fecha. tickets almacena código y código de seguimiento, tipo (denuncia o reporte_incidente), categoría
del catálogo predefinido y categoria_otro para Otros, descripción, sistema/área, fecha-hora aproximada,
severidad percibida, estado (registrado, en_analisis, derivado_a_incidente o cerrado), origen, medios
de notificación seleccionados y referencia nullable a incidentes.id; no tiene FK a usuarios ni almacena
nombre, correo u otro identificador del emisor. ticket_adjuntos referencia al ticket; notificaciones
registra medio, destinatario del equipo de ciberseguridad, estado de envío y lectura.

**RBAC (5 roles):** encargado, admin_contratos, referente_tecnico, director y admin_sistema. Solo
admin_sistema administra usuarios y no ve el contenido de tickets; solo encargado gestiona la bandeja,
el ciclo de vida y la conversión de tickets. admin_sistema se limita a la administración técnica y su
propio perfil, sin acceso a controles ni incidentes de negocio. El actor no autenticado puede crear un
ticket o consultar únicamente su estado mediante el código de seguimiento.

**Justificación de la arquitectura elegida:** dado el alcance acotado (una sola institución, volumen
transaccional bajo, equipo de 3 estudiantes y plazo de un semestre), se prefiere una arquitectura
**monolítica modular en 3 capas** por sobre microservicios: reduce la complejidad de despliegue y
mantenimiento, sin renunciar a la separación de responsabilidades por módulo (cada dominio de negocio
queda encapsulado y es reemplazable a futuro). **[PENDIENTE]** Confirmar stack tecnológico específico
(ej. backend Node.js/Express o Python/Django, frontend React, base de datos PostgreSQL) y justificarlo
formalmente en el marco teórico (IV) según criterios de madurez, soporte y seguridad de cada
tecnología.

### 7.3 Seguridad de la arquitectura

Dado que el SGSI almacena información sensible sobre controles, brechas, incidentes y denuncias, se
requieren RBAC de cinco roles, autenticación en todas las rutas internas, cifrado TLS en tránsito,
cifrado en reposo para archivos, repositorios con permisos restringidos y auditoría de operaciones
sensibles, incluidos los cambios de estado de controles e incidentes, y las altas, cambios de rol,
restablecimientos y cambios de estado de usuarios. Solo admin_sistema podrá administrar usuarios; el
contenido y la gestión de tickets quedarán reservados al encargado de ciberseguridad, sin acceso para
admin_sistema ni los otros roles.

El endpoint público POST /api/public/tickets y la ruta /reportar serán excepciones explícitas a la
autenticación, accesibles por HTTPS desde la red interna del hospital; el firewall/WAF no los expondrá a
Internet salvo decisión del mandante. Para reducir abuso se aplicarán rate limiting, honeypot o captcha
simple, validación y sanitización de entradas, lista blanca de tipos de archivo y tamaño máximo cercano
a 10 MB, con análisis antivirus recomendado. Los errores no revelarán detalles internos. El ticket no
registrará identidad, token, IP ni user-agent; los logs de aplicación y reverse proxy para esta ruta no
guardarán la IP o deberán anonimizarla. El código de seguimiento permitirá consultar solo el estado,
sin datos sensibles. Los correos se limitarán a código, tipo, severidad y enlace a la bandeja; si SMTP
falla, la creación no se bloqueará y el ticket quedará en la bandeja interna para reintento.

### 7.4 Modelo de despliegue

Se recomienda un despliegue **on-premise o en nube privada dentro de la red corporativa del hospital**
(no SaaS público de terceros), consistente con la naturaleza sensible de la información gestionada y
con las restricciones de continuidad exigidas a un operador de importancia vital (Ley 21.663).

Con este plan de diseño, la arquitectura queda definida (7.1–7.2) y justificada (7.2–7.4) de forma
explícita, cubriendo los criterios *"define la arquitectura TI"* y *"justifica el uso de la arquitectura
TI seleccionada"*.

---

## VIII. Reconocimiento de arquitectura empresarial

### 8.1 Tipo de organización y estructura

El Hospital Félix Bulnes Cerda corresponde a una **organización pública de salud**, establecimiento de
alta complejidad dependiente del Servicio de Salud Metropolitano Occidente (SSMOCC) y, en última
instancia, del Ministerio de Salud de Chile. Su estructura es **jerárquico-funcional**, típica del
sector público de salud: Dirección del establecimiento, Subdirecciones (Médica, Administrativa, Gestión
del Cuidado, Recursos Humanos, entre otras) y unidades de apoyo transversal, entre ellas la unidad o el
encargado de Ciberseguridad, cuya función de cumplimiento normativo (Ley 21.663, protección de datos)
es transversal a toda la organización y reporta habitualmente a la Dirección o a la Subdirección de
Gestión de la Información. **[PENDIENTE: reemplazar por organigrama oficial una vez validado con el
mandante.]**

Para ordenar el análisis se utiliza una vista simplificada de arquitectura empresarial (inspirada en
TOGAF), en 4 capas:

| Capa | Elemento institucional | Elemento del proyecto |
|---|---|---|
| Negocio | Proceso de gestión de seguridad de la información y cumplimiento normativo (Ley 21.663, protección de datos) | Objetivo general y objetivos específicos del SGSI (punto 5.3) |
| Aplicación | Funciones del encargado de ciberseguridad, administrador de contratos, referente técnico y administrador técnico; funcionarios como denunciantes | Nueve módulos: Controles, Evidencias, Madurez, Incidentes, Terceros, Personas, Reportería, Usuarios y Ticketera. RBAC con cinco roles: encargado, admin_contratos, referente_tecnico, director y admin_sistema (punto 7.2) |
| Datos | Evidencia documental de cumplimiento, registros de usuarios y tickets anónimos | Diez tablas: Control, Evidencia, Incidente, Tercero, PersonaControl, Usuario, tickets, ticket_adjuntos, notificaciones y auditoria_usuarios; tickets no se vinculan a la identidad del emisor |
| Tecnología | Infraestructura de red corporativa del hospital y sistema Trakcare | Aplicación web en 3 capas; APP-01, DB-01, NAS-01 y BK-01; formulario HTTPS desde la LAN, almacenamiento restringido de adjuntos y servicio SMTP institucional/relay (SMTP-01, salida APP-01 por puerto 587 o 25) para notificaciones |

### 8.2 Compatibilidad de la solución con la arquitectura empresarial

La solución es compatible con la arquitectura empresarial existente porque:

- **No modifica procesos asistenciales** ni el sistema clínico Trakcare; opera exclusivamente sobre el
  proceso de apoyo/gobierno de gestión de seguridad de la información, ya existente en la organización.
- **Respeta la estructura de roles de negocio** del hospital (encargado de ciberseguridad,
  administrador de contratos, referente técnico y director) y añade admin_sistema como rol técnico,
  distinto del encargado y restringido a administración de usuarios. El RBAC considera cinco roles;
  el encargado gestiona tickets y admin_sistema no accede a su contenido.
- **Incorpora a los funcionarios y denunciantes** como actores del proceso de reporte, mediante un
  formulario público sin autenticación que minimiza datos personales y no asocia la identidad al ticket.
- **Mantiene la separación de funciones:** el administrador técnico gestiona cuentas; el equipo de
  ciberseguridad conserva en exclusiva la lectura y gestión del ciclo de vida de los tickets.
- **Puede adoptarse sin rediseñar la estructura organizacional actual**, ya que se integra como una
  herramienta de apoyo a una función de cumplimiento que el hospital ya ejerce, cubriendo así los
  criterios *"reconoce las características de la arquitectura empresarial"* y *"define la solución de
  manera compatible con la arquitectura empresarial"*.

**[PENDIENTE: complementar con organigrama oficial y detalle formal de las unidades involucradas una
vez validado con el mandante.]**

---

## IX. Conclusiones

El diagnóstico realizado (sección II) evidenció que el Hospital Félix Bulnes Cerda, en su condición de
Operador de Importancia Vital bajo la Ley N.º 21.663, necesita centralizar la gestión de controles
ISO/IEC 27001, evidencias e incidentes ANCI, y además carece de un canal formal interno o público para
reportar denuncias e incidentes y de herramientas para administrar las cuentas y roles de usuarios. El
cambio de alcance acordado con el Product Owner el 21-10-2026 incorpora los módulos Usuarios y
Ticketera para abordar estas brechas.

La solución propuesta (sección V) comprende nueve módulos: Controles, Evidencias, Madurez, Incidentes,
Terceros, Personas, Reportería, Usuarios y Ticketera. El módulo Usuarios reserva a admin_sistema la
administración técnica de cuentas, con baja lógica y auditoría; la Ticketera permite crear reportes por
formulario público anónimo, protege su confidencialidad y reserva su gestión al encargado de
ciberseguridad. La arquitectura de soporte (secciones VII y VIII) mantiene un registro trazable,
notificaciones por correo institucional y/o bandeja interna, y conversión de tickets a incidentes
formales, sin alterar los procesos asistenciales ni integrarse en tiempo real con Trakcare.

De este modo, el problema identificado, la solución y su arquitectura son coherentes: los nueve
módulos responden a necesidades de cumplimiento y seguridad, con cinco roles RBAC, anonimato,
confidencialidad y auditoría. El cambio se gestiona en el backlog, priorizando Usuarios y luego
Ticketera, y debe incorporarse a la planificación sin perder el hito ES2 del 11-12-2026.

**[PENDIENTE — a completar por el equipo]**: incorporar aquí las reflexiones y aprendizajes propios del
proceso de levantamiento y formulación (p. ej. dificultades para interpretar la normativa de
ciberseguridad, lecciones del trabajo en equipo), además de proponer líneas de profundización para
etapas futuras del Proyecto de Título, tales como: integración progresiva con Trakcare mediante
reportería automatizada, evaluación de una futura integración directa con la plataforma de la ANCI, y
extensión del modelo de madurez a otros dominios normativos (p. ej. continuidad operacional).

---

## X. Referencias bibliográficas

**[PENDIENTE]** — completar con normas APA 7ª edición. Fuentes mínimas sugeridas a citar formalmente:

- ISO/IEC 27001:2022 — Information security management systems — Requirements.
- ISO/IEC 27002:2022 — Information security controls.
- Chile. Ley N.º 21.663, Marco de Ciberseguridad e Infraestructura Crítica.
- Chile. Ley N.º 19.628 / Ley N.º 21.719, sobre Protección de Datos Personales.
- Documentación pública de la Agencia Nacional de Ciberseguridad (ANCI) sobre taxonomía de incidentes.

---

## XI. Anexos

- Anexo 1: Transcripción/minuta de la entrevista con el encargado de ciberseguridad (base de este
  informe).
- Anexo 2: Listado completo de requerimientos (IEEE 830 o historias de usuario).
- Anexo 3: **[PENDIENTE]** Organigrama institucional.
- Anexo 4: **[PENDIENTE]** Matriz RACI y carta Gantt.
- Anexo 5: Diagrama de arquitectura de la soluci\u00f3n (ver punto 7.2) en formato ampliado.
