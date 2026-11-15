# -*- coding: utf-8 -*-
"""Genera el guion de estudio para la defensa del proyecto SGSI (.docx)."""
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

NAVY = RGBColor(0x20, 0x27, 0x2B)
TEAL = RGBColor(0x00, 0x8B, 0x8F)
BODY = RGBColor(0x3A, 0x44, 0x49)
MUTED = RGBColor(0x6B, 0x77, 0x7C)

doc = Document()

# ---- base styles -------------------------------------------------
normal = doc.styles["Normal"]
normal.font.name = "Calibri"
normal.font.size = Pt(11)
normal.font.color.rgb = BODY
normal.paragraph_format.space_after = Pt(6)
normal.paragraph_format.line_spacing = 1.15

title_st = doc.styles["Title"]
title_st.font.name = "Calibri"
title_st.font.color.rgb = TEAL
title_st.font.size = Pt(26)
title_st.font.bold = True

for hname in ("Heading 1", "Heading 2"):
    st = doc.styles[hname]
    st.font.name = "Calibri"
    st.font.bold = True
    st.font.color.rgb = TEAL if hname == "Heading 1" else NAVY


def bullet(text_runs):
    p = doc.add_paragraph(style="List Bullet")
    for t, bold in text_runs:
        r = p.add_run(t)
        r.bold = bold
    return p


def speech(text):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.25)
    r = p.add_run(text)
    r.italic = True
    r.font.color.rgb = BODY
    return p


# ---- header ------------------------------------------------------
doc.add_heading("Guion de presentación", level=0)
sub = doc.add_paragraph()
r = sub.add_run("Defensa del Proyecto de Título · SGSI — Sistema de Gestión de "
                "Seguridad de la Información")
r.font.size = Pt(13)
r.font.color.rgb = NAVY
r.bold = True
sub2 = doc.add_paragraph()
r = sub2.add_run("Hospital Félix Bulnes Cerda · Priscila Bahamóndez · Noviembre 2026")
r.font.size = Pt(10.5)
r.font.color.rgb = MUTED

intro = doc.add_paragraph()
intro.add_run("Cómo usar este guion: ").bold = True
intro.add_run("cada bloque corresponde a una diapositiva. «Qué decir» es el texto "
              "para ensayar en voz alta; «Para estudiar» resume lo que no puedes "
              "olvidar. Tiempo objetivo: 12 a 15 minutos en total (45–60 segundos "
              "por diapositiva). Habla con calma y usa la lámina como apoyo, no como guion.")

# ---- slides ------------------------------------------------------
slides = [
    ("Diapositiva 1 — Portada",
     "Buenos días. Mi nombre es Priscila Bahamóndez y presento el proyecto de título "
     "«SGSI: de planillas dispersas a gobierno auditable», un Sistema de Gestión de "
     "Seguridad de la Información para el Hospital Félix Bulnes Cerda. En los próximos "
     "minutos les mostraré el producto y, después, el proceso con el que lo construimos "
     "y justificamos.",
     ["Posición inicial: vender la idea en una frase — «de planillas dispersas a gobierno auditable».",
      "Mencionar con seguridad los tres anclajes: ISO/IEC 27001, Ley 21.663 y GRC."]),

    ("Diapositiva 2 — El problema",
     "Parto por el porqué. El hospital es Operador de Importancia Vital según la Ley 21.663: "
     "debe demostrar la madurez de sus controles ISO 27001 y reportar los incidentes a la ANCI "
     "dentro de plazos muy estrictos: tres horas para la alerta temprana, setenta y dos horas "
     "para severidad alta o crítica, y quince días para el cierre. Hoy todo eso se lleva a mano, "
     "en planillas, correos y actas. Sin un repositorio único no se puede medir, ni demostrar, "
     "ni reaccionar a tiempo.",
     ["Memorizar los tres plazos: 3 h · 72 h · 15 días.",
      "Cerrar con la frase de consecuencia, que prepara la solución."]),

    ("Diapositiva 3 — La idea",
     "Frente a ese problema, la idea es convertir la evidencia dispersa en decisiones "
     "verificables. Proponemos un sistema único de gobierno, riesgo y cumplimiento — GRC — que "
     "centraliza controles, evidencia, incidentes y reportes. En la práctica, el hospital pasa "
     "de preguntarse «¿cómo vamos?» a verlo en pantalla y actuar.",
     ["Dominar el ciclo de tres verbos: Conocer · Actuar · Demostrar.",
      "Definir GRC con palabras simples: gobernanza, riesgo y cumplimiento."]),

    ("Diapositiva 4 — El producto",
     "El producto se organiza en nueve módulos que comparten una sola fuente de verdad. Registra "
     "controles ISO 27001 con su evidencia, calcula la madurez por dominio, gestiona incidentes "
     "con taxonomía ANCI, cubre terceros y personas, genera reportes, administra usuarios y — clave — "
     "incluye una ticketera para denuncias y reportes anónimos.",
     ["Saber enumerar los nueve módulos sin leer la diapositiva.",
      "Destacar la ticketera como el diferenciador del alcance final."]),

    ("Diapositiva 5 — Por qué es distinto",
     "¿Qué lo hace distinto? Tres cosas que vienen de fábrica. Primero, el anonimato: el formulario "
     "público no guarda nombre, correo ni IP de quien reporta. Segundo, cinco roles con acceso "
     "mínimo. Y tercero, la separación de funciones: quien administra cuentas no puede leer el "
     "contenido de los tickets; solo el encargado gestiona la bandeja.",
     ["Enumerar los cinco roles: encargado, admin_contratos, referente_tecnico, director y admin_sistema.",
      "Enfatizar la frase «protección por diseño, no por buenas intenciones»."]),

    ("Diapositiva 6 — El proceso",
     "Ahora el proceso. Trabajamos con Scrum, metodología ágil: cada sprint entrega una pieza "
     "funcional que se revisa con el mandante. En el camino hubo un cambio de alcance: el 21 de "
     "octubre se incorporaron los módulos de Usuarios y Ticketera como cambio Mayor aprobado por "
     "el Product Owner, y aun así mantuvimos la fecha comprometida.",
     ["Presentar el cambio de alcance como evidencia de gestión, no como desvío.",
      "Retener las fechas: cambio 21-10-2026 y hito ES2 11-12-2026."]),

    ("Diapositiva 7 — Arquitectura",
     "La arquitectura es de tres capas y monolítica modular: presentación con React, una API REST "
     "con FastAPI y datos con PostgreSQL — SQLite en desarrollo. Es una herramienta de gobierno, "
     "por eso está deliberadamente aislada de Trakcare y se despliega en la red interna, sin tocar "
     "los sistemas asistenciales.",
     ["Explicar con calma el aislamiento de Trakcare: gobierno, no asistencial.",
      "Recordar el stack en una frase: React + FastAPI + PostgreSQL."]),

    ("Diapositiva 8 — Decisiones técnicas",
     "Y cada tecnología se eligió con criterio, no por moda. Hicimos una matriz ponderada de uno a "
     "cinco sobre criterios como seguridad, curva de aprendizaje y costo. FastAPI obtuvo 4,30; "
     "React 4,55; PostgreSQL 4,85; y Scrum 4,70. Las tres factibilidades — técnica, económica e "
     "implementativa — resultaron viables, con costo de licencias cero por usar software libre.",
     ["Memorizar los puntajes y por qué gana cada alternativa.",
      "Cerrar con el argumento económico: $0 en licencias."]),

    ("Diapositiva 9 — Seguridad",
     "La seguridad está en todas las capas: roles RBAC, cifrado en tránsito y en reposo, auditoría "
     "de quién hizo qué y cuándo, anonimato de los tickets, y protección contra abuso con límite de "
     "solicitudes y validación estricta. Es seguridad desde el diseño, no un parche al final.",
     ["Enumerar los seis controles sin titubear.",
      "Frases puente: «defensa en profundidad» y «desde el diseño»."]),

    ("Diapositiva 10 — Cómo se mide el éxito",
     "¿Cómo sabemos que funciona? Con resultados, no actividad. Definimos once KPI medibles: sesenta "
     "por ciento de madurez global al cierre, cien por ciento de incidentes reportados en plazo, y "
     "primera respuesta a tickets en menos de veinticuatro horas. Son metas referenciales que se "
     "ajustan en la validación con el mandante.",
     ["Distinguir las metas del núcleo GRC (madurez, evidencia) de las de la ticketera (24 h, SLA).",
      "Aclarar que son referenciales y se baselinizan en UAT."]),

    ("Diapositiva 11 — Cronograma",
     "El cronograma cubre once semanas con hitos verificables: el avance en octubre, el cambio de "
     "alcance aprobado, los módulos de Usuarios y Ticketera en noviembre, la validación UAT y la "
     "entrega final ES2 el 11 de diciembre. La planificación por sprints deja holgura para proteger "
     "esa fecha.",
     ["Dominar la línea de hitos: 09-10 · 21-10 · 06-11 · 20-11 · 04-12 · 11-12.",
      "Transmitir holgura y control del cronograma."]),

    ("Diapositiva 12 — Estado actual",
     "Y lo más importante: esto no es una idea en papel. El producto ya está construido y probado: "
     "doce grupos de endpoints en la API, treinta y nueve pruebas automatizadas y los nueve módulos "
     "funcionando en la aplicación, con controles ISO 27001 precargados, los cinco roles activos y "
     "el formulario público anónimo operativo.",
     ["Este es el golpe de confianza: cifras concretas (12 · 39 · 9).",
      "Si hay demo, ofrecer mostrarla al final."]),

    ("Diapositiva 13 — Cierre",
     "Para cerrar: pasamos de la dispersión a la trazabilidad. El SGSI permite medir la madurez, "
     "reaccionar ante incidentes y demostrar cumplimiento ante la Dirección y los reguladores. Es "
     "una solución que alinea problema, producto y proceso, y que ya está construida. Muchas "
     "gracias; quedo disponible para sus preguntas.",
     ["Terminar con los tres verbos y la frase de valor.",
      "Invitación clara a preguntas."]),
]

for title, sp, study in slides:
    doc.add_heading(title, level=1)
    doc.add_heading("Qué decir", level=2)
    speech(sp)
    doc.add_heading("Para estudiar", level=2)
    for s in study:
        bullet([(s, False)])

# ---- Q&A ---------------------------------------------------------
doc.add_page_break()
doc.add_heading("Preguntas probables del tribunal y cómo responder", level=1)

qa = [
    ("¿Por qué no se integran con Trakcare o los sistemas clínicos?",
     "El SGSI es una herramienta de gobierno y cumplimiento, no asistencial. Integrarlo en línea "
     "con el sistema clínico crítico añadiría riesgo técnico y regulatorio sin aportar valor. La "
     "interacción es asíncrona: referencia descriptiva, carga manual de evidencia y exportación de "
     "reportes. Está fuera del alcance declarado."),
    ("¿Cómo se protege el anonimato de las denuncias?",
     "El ticket no guarda nombre, correo, IP, user-agent, token ni vínculo al usuario que reporta. "
     "El código de seguimiento permite consultar solo el estado, y el contenido queda reservado al "
     "encargado; admin_sistema no lo lee."),
    ("¿Qué pasa si falla el correo SMTP?",
     "La creación del ticket no se bloquea: la notificación queda en la bandeja interna para "
     "reintento. Además, el correo solo incluye código, tipo, severidad y enlace, nunca contenido "
     "sensible."),
    ("¿Por qué Scrum y no Cascada?",
     "El alcance se refina con el mandante — catálogo de controles y taxonomía ANCI — y hubo un "
     "cambio Mayor a mitad del semestre. Scrum permite validación incremental y absorbió ese cambio "
     "sin mover la fecha ES2; Cascada habría sido rígida frente a él."),
    ("¿Por qué FastAPI, React y PostgreSQL?",
     "Por una matriz ponderada de 1 a 5 con criterios de seguridad, curva de aprendizaje, costo e "
     "integración. Obtuvieron los mayores puntajes (4,30 / 4,55 / 4,85) y son software libre: costo "
     "de licencias cero."),
    ("¿Cómo se separa la administración técnica de la gestión de negocio?",
     "Con RBAC de cinco roles. admin_sistema solo administra usuarios — alta, edición, rol, "
     "restablecer clave y baja lógica — y no accede a controles, incidentes ni al contenido de "
     "tickets. El encargado gestiona la bandeja y el ciclo de vida de los tickets."),
    ("¿Qué es la «baja lógica»?",
     "Deshabilitar la cuenta sin borrar registros, para conservar trazabilidad y auditoría. Un "
     "usuario deshabilitado no puede iniciar sesión ni acceder, aunque conserve un token previo. No "
     "se puede deshabilitar a uno mismo ni al último admin_sistema activo."),
    ("¿Cómo se evita el abuso del formulario público?",
     "Con límite de solicitudes (rate limiting), validación y sanitización estricta, lista blanca de "
     "tipos de archivo, tamaño máximo cercano a 10 MB, honeypot o captcha simple y errores genéricos "
     "sin detalles internos. Los logs de esa ruta no guardan IP o la anonimizan."),
    ("¿Qué es la madurez del SGSI y cómo se calcula?",
     "Es el porcentaje de avance ponderado de los controles ISO 27001 según su estado: no iniciado "
     "0, iniciado 0,33, implementado 0,67 y gestionado 1,0. Se ve por dominio y consolidado, con "
     "meta de al menos 60 % al cierre y 100 % a mediano plazo."),
    ("¿Los plazos legales son automáticos?",
     "Sí. El sistema computa los plazos según severidad y taxonomía ANCI (3 h / 72 h / 15 días) y "
     "alerta los vencimientos. El reporte a la ANCI se mantiene por canal institucional; la "
     "integración directa por API está fuera de alcance."),
    ("¿Qué queda fuera del alcance?",
     "La integración en tiempo real con Trakcare, el reporte automatizado directo a la ANCI y la "
     "certificación formal ISO 27001 del hospital. El sistema apoya la gestión, pero no reemplaza "
     "la auditoría de certificación."),
    ("¿Cómo se probó el sistema?",
     "Con 39 pruebas automatizadas (funcionales y de seguridad) y las pruebas de casos CP-01 a CP-38 "
     "más la UAT con el mandante, usando datos ficticios o anonimizados, sin acceder a información "
     "clínica real."),
]

for q, a in qa:
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(6)
    r = p.add_run(q)
    r.bold = True
    r.font.color.rgb = NAVY
    doc.add_paragraph(a)

# ---- final tips --------------------------------------------------
doc.add_page_break()
doc.add_heading("Consejos finales para la defensa", level=1)
tips = [
    "Ensaya en voz alta dos o tres veces y cronométrate: apunta a 12–15 minutos.",
    "Domina la diapositiva de módulos y la matriz de decisión; son las más preguntadas.",
    "Ten lista la demo del producto por si te piden verlo en vivo.",
    "Responde con la estructura «conclusión → fundamento → ejemplo», sin divagar.",
    "Habla con frases cortas y pausas; deja que la diapositiva refuerce, no que explique por ti.",
    "Si no sabes una respuesta, reconócelo y conecta con el alcance o con un trabajo futuro.",
]
for t in tips:
    bullet([(t, False)])

close = doc.add_paragraph()
close.paragraph_format.space_before = Pt(10)
r = close.add_run("Mensaje para recordar: ")
r.bold = True
r.font.color.rgb = TEAL
close.add_run("de planillas dispersas a gobierno auditable — medir, reaccionar y demostrar.")

out = "Documentacion/Entregas/Defensa/Guion_Defensa_SGSI.docx"
doc.save(out)
print("Guardado:", out)
