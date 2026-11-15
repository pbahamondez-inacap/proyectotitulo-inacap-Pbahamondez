# -*- coding: utf-8 -*-
"""Genera el guion de la presentación SGSI_ES2_Rubrica_Presentacion.pptx (25 láminas)."""
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

OUT = "/Users/nahum.sanchez/Documents/Esposa/Proyecto-Titulo/Repositorios/proyectotitulo-inacap-Pbahamondez/Documentacion/Entregas/Defensa/Guion_ES2_Rubrica_SGSI.docx"

NAVY = RGBColor(0x15, 0x24, 0x3B)
CRIMSON = RGBColor(0xA6, 0x19, 0x2E)
BLUE = RGBColor(0x1B, 0x6C, 0xA8)
GRAY = RGBColor(0x5B, 0x6B, 0x7B)

doc = Document()

# estilos base
normal = doc.styles["Normal"]
normal.font.name = "Calibri"
normal.font.size = Pt(11)
normal.font.color.rgb = RGBColor(0x21, 0x2B, 0x38)

for sname, sz, col in [("Heading 1", 15, NAVY), ("Heading 2", 12.5, CRIMSON)]:
    st = doc.styles[sname]
    st.font.name = "Calibri"
    st.font.size = Pt(sz)
    st.font.color.rgb = col
    st.font.bold = True

for section in doc.sections:
    section.top_margin = Inches(0.8)
    section.bottom_margin = Inches(0.8)
    section.left_margin = Inches(0.9)
    section.right_margin = Inches(0.9)


def title_block():
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r = p.add_run("Guion de presentación")
    r.font.size = Pt(26)
    r.font.bold = True
    r.font.color.rgb = NAVY
    p2 = doc.add_paragraph()
    r2 = p2.add_run("Defensa del Proyecto de Título · SGSI — Sistema de Gestión de Seguridad de la Información")
    r2.font.size = Pt(14)
    r2.font.bold = True
    r2.font.color.rgb = CRIMSON
    p3 = doc.add_paragraph()
    r3 = p3.add_run("Hospital Félix Bulnes Cerda · Priscila Bahamóndez · Evaluación Sumativa 2 (ES2) · Noviembre 2026")
    r3.font.size = Pt(11)
    r3.font.color.rgb = GRAY
    doc.add_paragraph()


def say(label, text, color=BLUE):
    p = doc.add_paragraph()
    r = p.add_run(label + "  ")
    r.font.bold = True
    r.font.color.rgb = color
    r.font.size = Pt(11)
    r2 = p.add_run(text)
    r2.font.size = Pt(11)


def bullets(items):
    for it in items:
        p = doc.add_paragraph(style="List Bullet")
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(it)
        r.font.size = Pt(11)


def slide(num, title, criterio, decir, estudiar):
    doc.add_heading(f"Diapositiva {num} — {title}", level=2)
    if criterio:
        pc = doc.add_paragraph()
        rc = pc.add_run(criterio)
        rc.font.size = Pt(9.5)
        rc.font.bold = True
        rc.font.color.rgb = GRAY
    say("Qué decir", decir)
    p = doc.add_paragraph()
    r = p.add_run("Para estudiar")
    r.font.bold = True
    r.font.color.rgb = CRIMSON
    r.font.size = Pt(11)
    bullets(estudiar)
    doc.add_paragraph()


# ---------------------------------------------------------------- portada / uso
title_block()

doc.add_heading("Cómo usar este guion", level=1)
doc.add_paragraph(
    "Cada bloque corresponde a una diapositiva de la presentación «SGSI_ES2_Rubrica_Presentacion.pptx» "
    "(25 láminas, alineada a la rúbrica ES2 de 17 criterios). «Qué decir» es el texto para ensayar en voz alta; "
    "«Para estudiar» resume lo que no puedes olvidar de cada criterio."
)
doc.add_paragraph(
    "Tiempo objetivo: 20–25 minutos en total (45–60 segundos por diapositiva). Si dispones de menos tiempo, "
    "condensa las diapositivas 6 a 22 (los criterios 2.1.x) y conserva la portada, la agenda, el producto, "
    "la vista del sistema, los resultados y el cierre. Habla con calma y usa la lámina como apoyo, no como guion."
)
doc.add_paragraph()

# ---------------------------------------------------------------- diapositivas
slide(1, "Portada", "Portada · SGSI",
      "Buenos días. Soy Priscila Bahamóndez y presento el proyecto de título «SGSI: de planillas dispersas a "
      "gobierno auditable», un Sistema de Gestión de Seguridad de la Información para el Hospital Félix Bulnes "
      "Cerda. Esta presentación está estructurada según la rúbrica de la Evaluación Sumativa 2: voy a recorrer "
      "los 17 criterios de desarrollo e implementación y a mostrar el producto construido.",
      ["Posición inicial: vender la idea en una frase — «de planillas dispersas a gobierno auditable».",
       "Mencionar los tres anclajes: ISO/IEC 27001, Ley 21.663 y GRC.",
       "Aclarar que la presentación sigue la rúbrica ES2 (17 criterios)."])

slide(2, "Agenda — mapeo a la rúbrica", "Agenda",
      "La presentación se organiza en seis bloques que agrupan los diecisiete criterios de la rúbrica: análisis "
      "y recursos, modelamiento y diseño, indicadores y servicios, calidad y estándares, servicios TI y "
      "continuidad, y planificación. Al final mostraré el estado actual del producto y las conclusiones.",
      ["Dominar los seis bloques y su orden.",
       "Cada criterio se demuestra con el contenido del entregable correspondiente.",
       "Adelantar que se incluyen imágenes del sistema."])

slide(3, "El problema y la solución", "Contexto",
      "Parto por el porqué. El hospital es Operador de Importancia Vital según la Ley 21.663: debe demostrar la "
      "madurez de sus controles ISO 27001 y reportar incidentes a la ANCI en plazos estrictos — tres horas la "
      "alerta temprana, setenta y dos horas para severidad alta o crítica y quince días para media o baja. Hoy "
      "eso se lleva a mano, en planillas y correos. La solución es un sistema GRC único que centraliza controles, "
      "evidencias, madurez, incidentes, terceros, personas y reportes, y agrega usuarios con roles y una ticketera anónima.",
      ["Memorizar los tres plazos: 3 h · 72 h · 15 días.",
       "Recordar el alcance: 9 módulos · 5 roles · 5 procesos · 10 tablas · 11 KPI · 38 casos.",
       "Cerrar con la consecuencia que prepara la solución."])

slide(4, "El producto: nueve módulos", "El producto",
      "El producto se organiza en nueve módulos que comparten una sola fuente de verdad: controles ISO 27001 con "
      "su evidencia, madurez por dominio, incidentes con taxonomía ANCI, terceros, personas, reportería, usuarios "
      "y — el diferenciador — una ticketera de denuncias y reportes anónimos.",
      ["Saber enumerar los nueve módulos sin leer la lámina.",
       "Destacar la ticketera como el diferenciador del alcance final.",
       "Mencionar el dashboard de madurez como prueba visual."])

slide(5, "Vista del sistema (capturas)", "Vista del sistema",
      "Aquí se ve la aplicación funcionando: la reportería con su resumen ejecutivo y exportación CSV, el "
      "formulario público de tickets que no pide iniciar sesión, y la bandeja confidencial que solo ve el "
      "encargado de ciberseguridad.",
      ["Identificar las tres capturas: reportería, formulario anónimo y bandeja.",
       "Si hay demo en vivo, ofrecer mostrarla al final.",
       "Transmitir que el sistema está construido, no es solo un diseño."])

slide(6, "Análisis comparativo (2.1.1.1)", "Criterio 2.1.1.1 · Entregable 1",
      "Cada tecnología se eligió con criterio, no por moda. Hicimos una matriz ponderada de uno a cinco sobre "
      "siete criterios — madurez, curva de aprendizaje, seguridad, costo, desempeño, integración y soporte — y la "
      "validamos con factibilidad técnica, económica e implementativa. FastAPI obtuvo 4,30; React 4,55; "
      "PostgreSQL 4,85 y Scrum 4,70. Costo de licencias: cero, por usar software libre.",
      ["Memorizar los puntajes: 4,30 · 4,55 · 4,85 · 4,70.",
       "Las tres factibilidades resultaron viables.",
       "Cerrar con el argumento económico: $0 en licencias."])

slide(7, "Herramientas, lenguajes, hardware y servicios TI (2.1.1.2)", "Criterio 2.1.1.2 · Entregable 2",
      "Detallamos lenguajes, stack, hardware y servicios TI. Python y TypeScript; FastAPI con SQLAlchemy, PyJWT "
      "y PBKDF2 en el backend; React con Vite y Recharts en el frontend. El hardware de producción es una propuesta "
      "referencial — servidor de aplicaciones, de base de datos y NAS — y el servicio TI clave es el relay SMTP "
      "institucional para las notificaciones.",
      ["Stack en una frase: React + FastAPI + PostgreSQL.",
       "Recordar 9 módulos y 5 roles; CRUD Usuarios solo admin_sistema, tickets solo encargado.",
       "El SMTP institucional es un servicio requerido, no opcional."])

slide(8, "BPMN de procesos (2.1.2.3)", "Criterio 2.1.2.3 · Entregable 3",
      "Modelamos cinco procesos con notación BPMN 2.0, cada uno con sus subprocesos: controles ISO 27001, "
      "incidentes, terceros, usuarios y tickets. Por ejemplo, el proceso de tickets va desde el formulario público, "
      "la anonimización y la notificación, hasta derivar a incidente formal o cerrar.",
      ["Nombrar los cinco procesos P1–P5.",
       "Cada proceso tiene subprocesos y actores (pools/carriles).",
       "P2 incorpora el origen desde un ticket derivado."])

slide(9, "UML: casos de uso y componentes (2.1.2.4)", "Criterio 2.1.2.4 · Entregable 4",
      "El UML documenta quince casos de uso con su descripción y el diagrama de componentes. Hay cinco roles "
      "autenticados más un actor anónimo para el formulario público. Los componentes muestran la SPA React, la API "
      "FastAPI con sus routers — incluidos usuarios, tickets y tickets públicos — y la capa de datos.",
      ["Recordar 15 casos de uso (UC-01 a UC-15).",
       "Separación: admin_sistema gestiona usuarios; encargado gestiona tickets.",
       "Arquitectura monolítica modular en 3 capas."])

slide(10, "Modelo de datos y diccionario (2.1.2.5)", "Criterio 2.1.2.5 · Entregable 5",
      "El modelo tiene diez tablas con su diccionario de datos. Lo importante es una decisión de diseño: la tabla "
      "de tickets no tiene relación con usuarios. No guardamos nombre, correo, IP ni token del denunciante — "
      "anonimato por diseño.",
      ["Recordar las 10 tablas.",
       "tickets NO tiene FK a usuarios.",
       "Diccionario con tipos, claves, índices y enums."])

slide(11, "Topología de comunicación (2.1.2.6)", "Criterio 2.1.2.6 · Entregable 6",
      "La topología separa tres zonas con doble firewall: usuarios en la LAN, servidores en la DMZ y datos "
      "aislados. Solo se permite HTTPS hacia la aplicación, el puerto de base de datos hacia PostgreSQL y salida "
      "SMTP al relay institucional. Está aislado de Trakcare y sin conexión en línea con la ANCI.",
      ["Recordar las 3 zonas + firewall doble.",
       "Aislamiento de la red clínica (Trakcare).",
       "El reporte a ANCI es manual, sin API en línea."])

slide(12, "Diseño de infraestructura (2.1.2.7)", "Criterio 2.1.2.7 · Entregable 7",
      "Detallamos cada componente: servidor de aplicaciones con Nginx y Uvicorn, servidor de base de datos "
      "PostgreSQL con RAID, NAS para evidencias y adjuntos, respaldo y el relay SMTP existente. Las capacidades son "
      "una propuesta referencial a validar con el hospital.",
      ["Nombrar APP-01, DB-01, NAS-01, BK-01 y SMTP-01.",
       "Capacidades referenciales, a validar.",
       "Crecimiento estimado ~24 GB/año (100 tickets/mes, 2 adjuntos ≤ 10 MB)."])

slide(13, "Arquitectura de la solución (2.1.2.8)", "Criterio 2.1.2.8 · Entregable 8",
      "La arquitectura es de tres capas — presentación, aplicación y datos — con servicios transversales. Es un "
      "monolito modular, deliberadamente: menor complejidad de despliegue. Registramos decisiones de arquitectura "
      "como el anonimato sin clave foránea a usuarios, el endpoint público acotado con límite de solicitudes y la "
      "notificación tolerante a fallos.",
      ["Explicar las 3 capas y el aislamiento de Trakcare.",
       "Recordar los ADR clave (anonimato, endpoint público, notificación).",
       "Base intercambiable SQLite/PostgreSQL vía SQLAlchemy."])

slide(14, "KPI con detalle SMART (2.1.3.9)", "Criterio 2.1.3.9 · Entregable 9",
      "Definimos once KPI con detalle SMART. Los del núcleo GRC: madurez global de al menos sesenta por ciento e "
      "incidentes reportados en plazo al cien por ciento. Los de la ticketera: primera respuesta en menos de "
      "veinticuatro horas y noventa por ciento gestionados dentro del SLA. Son metas referenciales a validar.",
      ["Distinguir metas GRC (madurez, evidencia) de ticketera (24 h, SLA).",
       "Recordar 11 KPI SMART, cada uno ligado a su módulo.",
       "Aclarar que son referenciales y se baselinizan en UAT."])

slide(15, "SLA: disponibilidad y tiempos (2.1.3.10)", "Criterio 2.1.3.10 · Entregable 10",
      "Los SLA fijan disponibilidad de noventa y nueve por ciento en horario administrativo, tiempos de respuesta "
      "y resolución por severidad — treinta minutos para crítica — y recuperación con RPO de veinticuatro horas y "
      "RTO de ocho. También definimos el acuse de tickets y la baja de usuarios desvinculados.",
      ["Recordar 99 % de disponibilidad.",
       "Severidades: crítica 30 min/4 h · alta 1 h/8 h · media 4 h/24 h · baja 8 h/5 días.",
       "RPO ≤ 24 h · RTO ≤ 8 h · respaldo diario."])

slide(16, "Plan de pruebas CP-01 a CP-38 (2.1.4.11)", "Criterio 2.1.4.11 · Entregable 11",
      "El plan cubre pruebas unitarias, de integración, de sistema, de aceptación, de seguridad y de rendimiento, "
      "con treinta y ocho casos de prueba, de CP-01 a CP-38, incluyendo anonimato, control de acceso, límite de "
      "solicitudes y adjuntos. En el código hay treinta y nueve pruebas automatizadas.",
      ["Recordar 38 casos + 39 pruebas automatizadas.",
       "Niveles: unitarias, integración, sistema, UAT, seguridad, rendimiento.",
       "Herramientas: Pytest, Vitest, Swagger UI."])

slide(17, "Normas y estándares N1–N15 (2.1.4.12)", "Criterio 2.1.4.12 · Entregable 12",
      "Incorporamos quince normas y estándares con justificación: ISO 27001 y 27002 para el SGSI, la Ley 21.663 "
      "para los plazos, la Ley 19.628 y 21.719 para datos personales, OWASP para la seguridad de la aplicación, e "
      "ISO 20000 e ITIL para la operación.",
      ["Agrupar las 15 normas en SGSI, legal, calidad y servicios.",
       "Cada norma tiene justificación de incorporación.",
       "El canal de denuncias requiere validación jurídica."])

slide(18, "Implementación y disponibilidad (2.1.5.13)", "Criterio 2.1.5.13 · Entregable 13",
      "El plan de implementación avanza por fases — desarrollo, integración, producción y operación — y la gestión "
      "de disponibilidad asegura un noventa y nueve por ciento con monitoreo del endpoint de salud, respaldo diario "
      "y cambios controlados.",
      ["Recordar las 4 fases de despliegue.",
       "Disponibilidad ≥ 99 % en horario administrativo.",
       "Monitoreo de /api/health."])

slide(19, "Plan de continuidad (2.1.5.14)", "Criterio 2.1.5.14 · Entregable 14",
      "El plan de continuidad combina medidas proactivas — respaldo diario y offline, RAID, segmentación y "
      "monitoreo — con medidas reactivas: RPO de veinticuatro horas, RTO de ocho y un procedimiento de recuperación "
      "en ocho pasos, probado con simulacros trimestrales y semestrales.",
      ["Distinguir proactivo (prevenir) de reactivo (recuperar).",
       "RPO ≤ 24 h · RTO ≤ 8 h.",
       "Pruebas trimestrales de restauración y simulacros semestrales."])

slide(20, "Plan de mantención (2.1.5.15)", "Criterio 2.1.5.15 · Entregable 15",
      "La mantención cubre tres prácticas: gestión de configuración con línea base versionada, gestión de cambios "
      "— estándar, normal, mayor y de emergencia — y gestión de incidentes del propio sistema. El cambio de alcance "
      "de Usuarios y Ticketera se gestionó como cambio mayor aprobado por el Product Owner.",
      ["Recordar las 3 prácticas: configuración, cambios, incidentes.",
       "El cambio Mayor del 21-10-2026 (Usuarios + Ticketera).",
       "Distinguir ticketera de negocio de incidentes operativos del SGSI."])

slide(21, "Planificación: fases y carta Gantt (2.1.6.16)", "Criterio 2.1.6.16 · Entregable 16",
      "La planificación usa Scrum con detalle de fases y una carta Gantt de referencia: once semanas con hitos "
      "verificables — avance en octubre, cambio aprobado, Usuarios y Ticketera en noviembre, UAT y entrega ES2 el "
      "once de diciembre.",
      ["Dominar los hitos: 09-10 · 21-10 · 06-11 · 20-11 · 04-12 · 11-12.",
       "Metodología ágil: detalle de fases/sprints + Gantt de referencia.",
       "Transmitir holgura y control del cronograma."])

slide(22, "Justificación del cronograma (2.1.6.17)", "Criterio 2.1.6.17 · Entregable 17",
      "Justifico el cronograma en tres ejes: cada fase habilita la funcionalidad de la solución, la duración y la "
      "holgura protegen la fecha, y el orden Usuarios antes que Ticketera permite asignar roles antes de construir "
      "la bandeja. Así, el cambio de alcance no movió el hito ES2.",
      ["Tres ejes: coherencia, duración/holgura, adecuación al problema.",
       "ES2 se mantiene el 11-12-2026.",
       "Sin omitir anonimato, confidencialidad, SMTP ni validación de adjuntos."])

slide(23, "Estado actual: producto construido", "Resultados",
      "Y lo más importante: no es una idea en papel. El producto está construido — doce grupos de endpoints, "
      "treinta y nueve pruebas automatizadas y los nueve módulos funcionando, con controles precargados, cinco "
      "roles activos y el formulario público anónimo operativo.",
      ["Cifras concretas: 12 grupos de endpoints · 39 pruebas · 9 módulos.",
       "Ofrecer la demo en vivo si es posible.",
       "Mencionar la importación masiva de incidentes por CSV."])

slide(24, "Conclusiones y trabajos futuros", "Conclusiones",
      "Para cerrar: la solución cumple el objetivo de registrar, medir y visualizar la madurez y gestionar "
      "incidentes conforme a la Ley 21.663, con un stack viable en las tres factibilidades. Quedan trabajos futuros "
      "como SSO, cifrado de adjuntos o integración con la ANCI.",
      ["Objetivo general cumplido.",
       "Stack viable técnica, económica e implementativamente.",
       "Nombrar 2–3 trabajos futuros clave."])

slide(25, "Cierre", "Cierre",
      "Pasamos de planillas dispersas a un gobierno auditable. El SGSI permite medir, reaccionar y demostrar "
      "cumplimiento. Muchas gracias; quedo disponible para sus preguntas.",
      ["Terminar con los tres verbos: medir, reaccionar, demostrar.",
       "Invitación clara a preguntas."])

# ---------------------------------------------------------------- preguntas
doc.add_heading("Preguntas probables del tribunal y cómo responder", level=1)


def qa(q, a):
    doc.add_heading(q, level=2)
    doc.add_paragraph(a)


qa("¿Por qué no se integran con Trakcare o los sistemas clínicos?",
   "El SGSI es una herramienta de gobierno y cumplimiento, no asistencial. Integrarlo en línea con el sistema "
   "clínico crítico añadiría riesgo técnico y regulatorio sin aportar valor. La interacción es asíncrona: "
   "referencia descriptiva, carga manual de evidencia y exportación de reportes. Está fuera del alcance declarado.")

qa("¿Cómo se protege el anonimato de las denuncias?",
   "El ticket no guarda nombre, correo, IP, user-agent, token ni vínculo al usuario que reporta. La tabla tickets "
   "no tiene clave foránea a usuarios. El código de seguimiento permite consultar solo el estado, y el contenido "
   "queda reservado al encargado; admin_sistema no lo lee.")

qa("¿Qué pasa si falla el correo SMTP?",
   "La creación del ticket no se bloquea: la notificación queda en la bandeja interna para reintento. Además, el "
   "correo solo incluye código, tipo, severidad y enlace, nunca contenido sensible.")

qa("¿Por qué Scrum y no Cascada?",
   "El alcance se refina con el mandante — catálogo de controles y taxonomía ANCI — y hubo un cambio Mayor a mitad "
   "del semestre. Scrum permite validación incremental y absorbió ese cambio sin mover la fecha ES2; Cascada habría "
   "sido rígida frente a él.")

qa("¿Por qué FastAPI, React y PostgreSQL?",
   "Por una matriz ponderada de 1 a 5 con criterios de seguridad, curva de aprendizaje, costo e integración. "
   "Obtuvieron los mayores puntajes (4,30 / 4,55 / 4,85) y son software libre: costo de licencias cero.")

qa("¿Cómo se separa la administración técnica de la gestión de negocio?",
   "Con RBAC de cinco roles. admin_sistema solo administra usuarios — alta, edición, rol, restablecer clave y baja "
   "lógica — y no accede a controles, incidentes ni al contenido de tickets. El encargado gestiona la bandeja y el "
   "ciclo de vida de los tickets.")

qa("¿Qué es la «baja lógica»?",
   "Deshabilitar la cuenta sin borrar registros, para conservar trazabilidad y auditoría. Un usuario deshabilitado "
   "no puede iniciar sesión ni acceder, aunque conserve un token previo. No se puede deshabilitar a uno mismo ni al "
   "último admin_sistema activo.")

qa("¿Cómo se evita el abuso del formulario público?",
   "Con límite de solicitudes (rate limiting), validación y sanitización estricta, lista blanca de tipos de archivo, "
   "tamaño máximo cercano a 10 MB, honeypot o captcha simple y errores genéricos sin detalles internos. Los logs de "
   "esa ruta no guardan IP o la anonimizan.")

qa("¿Qué es la madurez del SGSI y cómo se calcula?",
   "Es el porcentaje de avance ponderado de los controles ISO 27001 según su estado: no iniciado 0, iniciado 0,33, "
   "implementado 0,67 y gestionado 1,0. Se ve por dominio y consolidado, con meta de al menos 60 % al cierre y "
   "100 % a mediano plazo.")

qa("¿Los plazos legales son automáticos?",
   "Sí. El sistema computa los plazos según severidad y taxonomía ANCI (3 h / 72 h / 15 días) y alerta los "
   "vencimientos. El reporte a la ANCI se mantiene por canal institucional; la integración directa por API está "
   "fuera de alcance.")

qa("¿Por qué monolito modular y no microservicios?",
   "Por el alcance: una sola institución, volumen transaccional bajo, equipo de tres estudiantes y plazo de un "
   "semestre. El monolito modular reduce la complejidad de despliegue sin renunciar a la separación por módulo, que "
   "queda encapsulado y reemplazable a futuro.")

qa("¿Por qué SQLite en desarrollo y PostgreSQL en producción?",
   "SQLAlchemy permite cambiar de motor por variable de entorno (SGSI_DATABASE_URL) sin modificar código. SQLite "
   "elimina administración en desarrollo y pruebas; PostgreSQL aporta auditoría, concurrencia multiusuario y "
   "respaldo en producción.")

qa("¿Cómo se justifica el RPO de 24 horas y el RTO de 8 horas?",
   "Son propuestas referenciales coherentes con un sistema de apoyo/gobernanza que opera en horario administrativo: "
   "respaldo diario con pérdida máxima de 24 horas y restablecimiento dentro de una jornada hábil. Los valores se "
   "confirman con el mandante según su política de TI.")

qa("¿Qué norma sustenta la ticketera anónima?",
   "ISO/IEC 27001:2022 Anexo A 6.8 y 5.24–5.28 para la notificación y respuesta a eventos; Anexo A 5.15–5.18 y 8.2 "
   "para el control de acceso; y las leyes 19.628 y 21.719 por el principio de minimización de datos, junto con "
   "OWASP ASVS/API Security para la seguridad del endpoint público.")

qa("¿Qué queda fuera del alcance?",
   "La integración en tiempo real con Trakcare, el reporte automatizado directo a la ANCI y la certificación formal "
   "ISO 27001 del hospital. El sistema apoya la gestión, pero no reemplaza la auditoría de certificación.")

qa("¿Cómo se probó el sistema?",
   "Con 39 pruebas automatizadas (funcionales y de seguridad) y los casos CP-01 a CP-38 más la UAT con el mandante, "
   "usando datos ficticios o anonimizados, sin acceder a información clínica real.")

# ---------------------------------------------------------------- consejos
doc.add_heading("Consejos finales para la presentación", level=1)
bullets([
    "Ensayá en voz alta dos o tres veces y cronometrate: apuntá a 20–25 minutos.",
    "Dominá la lámina de módulos y la matriz de decisión; son las más preguntadas.",
    "Tené lista la demo del producto por si te piden verlo en vivo.",
    "Respondé con la estructura «conclusión → fundamento → ejemplo», sin divagar.",
    "Hablá con frases cortas y pausas; dejá que la lámina refuerce, no que explique por ti.",
    "Si no sabés una respuesta, reconocelo y conectá con el alcance o con un trabajo futuro.",
])

p = doc.add_paragraph()
r = p.add_run("Mensaje para recordar: ")
r.font.bold = True
r.font.color.rgb = CRIMSON
r2 = p.add_run("de planillas dispersas a gobierno auditable — medir, reaccionar y demostrar.")
r2.font.bold = True
r2.font.color.rgb = NAVY

doc.core_properties.title = "Guion de presentación — SGSI · Evaluación Sumativa 2 (ES2)"
doc.core_properties.author = "Priscila Bahamóndez"

doc.save(OUT)
print("Guardado:", OUT)
