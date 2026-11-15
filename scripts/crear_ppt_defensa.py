# -*- coding: utf-8 -*-
"""Genera la presentación de defensa del Proyecto de Título SGSI.

Estilo alineado a las entregas anteriores (Aptos Display / Aptos, paleta
teal + navy + magenta, 16:9). Lenguaje simple y formal para "vender" el
producto y "defender" el proceso.
"""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# ---------------------------------------------------------------- palette
NAVY      = RGBColor(0x20, 0x27, 0x2B)
TEAL      = RGBColor(0x00, 0x8B, 0x8F)
TEAL_LT   = RGBColor(0x7B, 0xC9, 0xC4)
TEAL_PALE = RGBColor(0xE7, 0xF4, 0xF4)
MAGENTA   = RGBColor(0xD8, 0x32, 0x63)
INK       = RGBColor(0x20, 0x27, 0x2B)
BODY      = RGBColor(0x5A, 0x66, 0x6D)
MUTED     = RGBColor(0x8F, 0xA0, 0xA2)
FAINT     = RGBColor(0xAE, 0xBB, 0xBC)
LIGHT     = RGBColor(0xDD, 0xE5, 0xE5)
PAPER     = RGBColor(0xF5, 0xF7, 0xF7)
WHITE     = RGBColor(0xFF, 0xFF, 0xFF)

DISPLAY = "Aptos Display"
SANS    = "Aptos"

SLIDE_W = 13.333
SLIDE_H = 7.5
MARGIN  = 0.62

prs = Presentation()
prs.slide_width  = Inches(SLIDE_W)
prs.slide_height = Inches(SLIDE_H)
BLANK = prs.slide_layouts[6]

# ---------------------------------------------------------------- helpers
def _set_run(r, text, size, color, bold, font, italic):
    r.text = text
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.italic = italic
    r.font.name = font
    r.font.color.rgb = color


def text(slide, x, y, w, h, paras, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP,
         space_after=0, line_spacing=None):
    """paras: list of paragraphs; each paragraph is a list of run dicts."""
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = 0
    tf.margin_right = 0
    tf.margin_top = 0
    tf.margin_bottom = 0
    for i, para in enumerate(paras):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        if space_after:
            p.space_after = Pt(space_after)
        if line_spacing:
            p.line_spacing = line_spacing
        for rd in para:
            r = p.add_run()
            _set_run(r, rd["t"], rd.get("size", 14), rd.get("color", BODY),
                     rd.get("bold", False), rd.get("font", SANS),
                     rd.get("italic", False))
    return tb


def line(slide, x, y, w, h, s, size, color, bold=False, font=SANS,
         align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP):
    return text(slide, x, y, w, h, [[{"t": s, "size": size, "color": color,
                                       "bold": bold, "font": font}]],
                align=align, anchor=anchor)


def rect(slide, x, y, w, h, fill=None, line_color=None, line_w=0.75,
         round_=False, radius=0.06):
    shp = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE if round_ else MSO_SHAPE.RECTANGLE,
        Inches(x), Inches(y), Inches(w), Inches(h))
    if round_:
        try:
            shp.adjustments[0] = radius
        except Exception:
            pass
    if fill is None:
        shp.fill.background()
    else:
        shp.fill.solid()
        shp.fill.fore_color.rgb = fill
    if line_color is None:
        shp.line.fill.background()
    else:
        shp.line.color.rgb = line_color
        shp.line.width = Pt(line_w)
    shp.shadow.inherit = False
    return shp


def kicker(slide, s):
    line(slide, MARGIN, 0.42, 10.0, 0.32, s, 13, TEAL, bold=True)


def title(slide, s, size=29, color=INK, w=12.1):
    text(slide, MARGIN, 0.72, w, 0.85,
         [[{"t": s, "size": size, "color": color, "bold": True, "font": DISPLAY}]])


def rule(slide):
    rect(slide, MARGIN, 1.52, 0.85, 0.045, fill=TEAL)


def source(slide, s):
    line(slide, MARGIN, 7.02, 12.1, 0.3, s, 9, MUTED)


def footer(slide, page):
    line(slide, SLIDE_W - 1.0, 7.02, 0.7, 0.3, f"{page:02d}", 11, FAINT,
         align=PP_ALIGN.RIGHT)


def card(slide, x, y, w, h, fill=PAPER, line_color=LIGHT, radius=0.055):
    return rect(slide, x, y, w, h, fill=fill, line_color=line_color,
                line_w=0.75, round_=True, radius=radius)


# ================================================================ 1 · PORTADA
s = prs.slides.add_slide(BLANK)
rect(s, 0, 0, SLIDE_W, SLIDE_H, fill=NAVY)
rect(s, 0, 0, 0.28, SLIDE_H, fill=TEAL)
rect(s, 0.28, 0, 0.06, SLIDE_H, fill=MAGENTA)

line(s, MARGIN, 0.7, 10.0, 0.35, "PROYECTO DE TÍTULO  ·  DEFENSA DEL PROYECTO",
     13, TEAL_LT, bold=True)
line(s, MARGIN, 1.35, 11.5, 1.6, "SGSI", 96, WHITE, bold=True, font=DISPLAY)
line(s, MARGIN, 2.95, 11.8, 0.8,
     "De planillas dispersas a gobierno auditable", 30, WHITE, bold=True,
     font=DISPLAY)
text(s, MARGIN, 3.85, 11.6, 1.2, [[
    {"t": "Sistema de Gestión de Seguridad de la Información para medir la "
          "madurez ISO/IEC 27001 y gestionar incidentes de ciberseguridad.",
     "size": 16, "color": LIGHT, "bold": False, "font": SANS}]])

# pills
pills = ["ISO/IEC 27001", "Ley 21.663", "GRC · Gobernanza, Riesgo y Cumplimiento"]
px = MARGIN
for ptext in pills:
    w = 0.34 + 0.115 * len(ptext)
    rect(s, px, 5.35, w, 0.5, fill=None, line_color=TEAL_LT, line_w=1.2,
         round_=True, radius=0.5)
    line(s, px, 5.42, w, 0.36, ptext, 12, TEAL_LT, bold=True,
         align=PP_ALIGN.CENTER)
    px += w + 0.25

text(s, MARGIN, 6.35, 12.0, 0.8, [
    [{"t": "Priscila Bahamóndez", "size": 14, "color": WHITE, "bold": True, "font": SANS},
     {"t": "   ·   Académico guía: Luis Bravo   ·   Mandante: Miguel Godoy", "size": 14, "color": FAINT, "font": SANS}],
    [{"t": "Hospital Félix Bulnes Cerda   ·   Noviembre 2026", "size": 13, "color": FAINT, "font": SANS}],
], space_after=6)

# ================================================================ 2 · PROBLEMA
s = prs.slides.add_slide(BLANK)
kicker(s, "01 · EL PROBLEMA")
title(s, "Una obligación legal que hoy se cumple a mano")
rule(s)

text(s, MARGIN, 1.95, 6.0, 4.4, [
    [{"t": "El Hospital Félix Bulnes Cerda es ", "size": 16, "color": BODY, "font": SANS},
     {"t": "Operador de Importancia Vital", "size": 16, "color": INK, "bold": True, "font": SANS},
     {"t": " (Ley 21.663): debe demostrar la madurez de sus controles ISO/IEC 27001 y reportar incidentes a la ANCI dentro de plazos estrictos.", "size": 16, "color": BODY, "font": SANS}],
    [{"t": "Hoy esa evidencia vive dispersa en ", "size": 16, "color": BODY, "font": SANS},
     {"t": "planillas, correos y actas", "size": 16, "color": INK, "bold": True, "font": SANS},
     {"t": ". El resultado: poca visibilidad del estado real, auditorías costosas y riesgo de vencer plazos.", "size": 16, "color": BODY, "font": SANS}],
], space_after=10, line_spacing=1.12)

# reloj legal
rx = 7.0
line(s, rx, 1.95, 5.6, 0.35, "RELOJ LEGAL DE INCIDENTES", 13, TEAL, bold=True)
clock = [
    ("3 h", "alerta temprana", MAGENTA),
    ("72 h", "reporte alta / crítica", TEAL),
    ("15 días", "reporte media / baja", INK),
]
cy = 2.45
for big, small, col in clock:
    rect(s, rx, cy, 5.6, 1.05, fill=PAPER, line_color=LIGHT, line_w=1.0,
         round_=True, radius=0.1)
    rect(s, rx, cy, 0.09, 1.05, fill=col)
    line(s, rx + 0.35, cy + 0.12, 2.0, 0.8, big, 30, col, bold=True,
         font=DISPLAY)
    line(s, rx + 0.35, cy + 0.68, 5.0, 0.35, small, 14, INK, bold=True)
    cy += 1.22

# consequence bar
rect(s, MARGIN, 6.0, 12.1, 0.72, fill=TEAL_PALE, line_color=None, round_=True, radius=0.14)
text(s, MARGIN + 0.3, 6.0, 11.6, 0.72, [[
    {"t": "Consecuencia:  ", "size": 14, "color": TEAL, "bold": True, "font": SANS},
    {"t": "sin un repositorio único no se puede medir, demostrar ni reaccionar a tiempo.",
     "size": 14, "color": INK, "font": SANS}]], anchor=MSO_ANCHOR.MIDDLE)

footer(s, 2)

# ================================================================ 3 · LA IDEA
s = prs.slides.add_slide(BLANK)
kicker(s, "02 · LA IDEA")
title(s, "Convertir evidencia dispersa en decisiones verificables")
rule(s)

text(s, MARGIN, 1.95, 12.0, 1.2, [[
    {"t": "Un sistema único de gobierno, riesgo y cumplimiento (GRC) que centraliza "
          "controles, evidencia, incidentes y reportes, para que el hospital conozca su "
          "estado real, actúe sobre las brechas y demuestre cumplimiento.", "size": 17,
     "color": BODY, "font": SANS}]], line_spacing=1.15)

cols = [
    ("CONOCER", "Controles ISO 27001 y evidencia en un solo lugar, con madurez por dominio visible en gráficos.", TEAL),
    ("ACTUAR", "Incidentes con taxonomía ANCI, plazos legales automáticos y bandeja confidencial de denuncias.", MAGENTA),
    ("DEMOSTRAR", "Reportes exportables y auditoría de cada cambio, listos para la Dirección y los reguladores.", INK),
]
cw = 3.92
gap = 0.17
for i, (k, d, col) in enumerate(cols):
    x = MARGIN + i * (cw + gap)
    y = 3.5
    card(s, x, y, cw, 2.6)
    rect(s, x, y, cw, 0.14, fill=col)
    line(s, x + 0.3, y + 0.42, cw - 0.6, 0.6, k, 24, col, bold=True, font=DISPLAY)
    text(s, x + 0.3, y + 1.05, cw - 0.6, 1.4,
         [[{"t": d, "size": 14.5, "color": BODY, "font": SANS}]], line_spacing=1.15)

source(s, "La propuesta cubre el ciclo completo del SGSI: registrar, medir, alertar y evidenciar.")
footer(s, 3)

# ================================================================ 4 · PRODUCTO
s = prs.slides.add_slide(BLANK)
kicker(s, "03 · EL PRODUCTO")
title(s, "Nueve módulos, una sola fuente de verdad")
rule(s)

mods = [
    ("Controles", "Catálogo ISO 27001 por dominio, estado y responsable."),
    ("Evidencias", "Documentos y trazabilidad del cumplimiento."),
    ("Madurez", "Avance por dominio y consolidado, en gráficos."),
    ("Incidentes", "Taxonomía ANCI y plazos legales automáticos."),
    ("Terceros", "Cláusulas de seguridad en contratos y licitaciones."),
    ("Personas", "Ciclo de vida y controles del personal."),
    ("Reportería", "Informes y exportación CSV para auditoría."),
    ("Usuarios", "Cuentas, roles y baja lógica auditada."),
    ("Ticketera", "Denuncias y reportes anónimos por formulario público."),
]
cw = 3.92
ch = 1.42
gapx = 0.17
gapy = 0.18
x0 = MARGIN
y0 = 1.9
for idx, (name, desc) in enumerate(mods):
    col = idx % 3
    row = idx // 3
    x = x0 + col * (cw + gapx)
    y = y0 + row * (ch + gapy)
    card(s, x, y, cw, ch)
    rect(s, x, y, 0.08, ch, fill=TEAL if (idx % 2 == 0) else MAGENTA)
    line(s, x + 0.32, y + 0.18, cw - 0.6, 0.4, f"0{idx+1}", 12, MUTED, bold=True)
    line(s, x + 0.32, y + 0.5, cw - 0.6, 0.4, name, 17, INK, bold=True, font=DISPLAY)
    text(s, x + 0.32, y + 0.88, cw - 0.6, 0.55,
         [[{"t": desc, "size": 12, "color": BODY, "font": SANS}]], line_spacing=1.05)

source(s, "El producto reemplaza el trabajo manual disperso por un sistema auditable y visual.")
footer(s, 4)

# ================================================================ 5 · DISTINTO
s = prs.slides.add_slide(BLANK)
kicker(s, "04 · POR QUÉ ES DISTINTO")
title(s, "El anonimato y la separación de funciones vienen de fábrica")
rule(s)

feats = [
    ("Ticketera anónima", "Formulario público sin iniciar sesión. El sistema no guarda nombre, correo ni IP del denunciante.", MAGENTA),
    ("Cinco roles RBAC", "encargado, admin_contratos, referente_tecnico, director y admin_sistema. Cada uno ve solo lo que necesita.", TEAL),
    ("Separación de funciones", "admin_sistema administra cuentas pero no lee el contenido de los tickets; solo el encargado gestiona la bandeja.", INK),
]
cw = 3.92
gap = 0.17
for i, (k, d, col) in enumerate(feats):
    x = MARGIN + i * (cw + gap)
    card(s, x, 1.95, cw, 3.5)
    rect(s, x, 1.95, cw, 0.14, fill=col)
    line(s, x + 0.3, 2.35, cw - 0.6, 0.9, k, 20, col, bold=True, font=DISPLAY)
    text(s, x + 0.3, 3.35, cw - 0.6, 1.9,
         [[{"t": d, "size": 14, "color": BODY, "font": SANS}]], line_spacing=1.18)

source(s, "La confidencialidad de las denuncias se protege por diseño, no por buenas intenciones.")
footer(s, 5)

# ================================================================ 6 · PROCESO
s = prs.slides.add_slide(BLANK)
kicker(s, "05 · EL PROCESO")
title(s, "Scrum: construir, validar y ajustar con el mandante")
rule(s)

text(s, MARGIN, 1.95, 5.7, 3.6, [
    [{"t": "Trabajamos con metodología ágil ", "size": 15.5, "color": BODY, "font": SANS},
     {"t": "Scrum", "size": 15.5, "color": INK, "bold": True, "font": SANS},
     {"t": ": cada sprint entrega una pieza funcional que se revisa con el encargado de ciberseguridad.", "size": 15.5, "color": BODY, "font": SANS}],
    [{"t": "Backlog priorizado por valor, revisiones frecuentes y trazabilidad de cada decisión para absorber cambios sin perder el hito.", "size": 14, "color": BODY, "font": SANS}],
], space_after=12, line_spacing=1.18)

phases = [
    ("F1", "Formulación", "Requisitos y marco normativo."),
    ("F2", "Diseño", "BPMN, UML, datos y arquitectura."),
    ("F3–F4", "Desarrollo", "Sprints Usuarios y Ticketera."),
    ("F5", "Pruebas", "CP-01 a CP-38 y UAT."),
    ("F6–F7", "Cierre", "Documentación, ABPro y defensa."),
]
px = 6.95
py = 1.95
ph = 0.7
for i, (tag, name, det) in enumerate(phases):
    card(s, px, py, 5.75, ph, fill=WHITE, line_color=LIGHT)
    rect(s, px, py, 1.0, ph, fill=TEAL if i % 2 == 0 else NAVY)
    line(s, px, py + 0.06, 1.0, ph - 0.12, tag, 13.5, WHITE, bold=True,
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    line(s, px + 1.2, py + 0.09, 4.4, 0.3, name, 13.5, INK, bold=True)
    line(s, px + 1.2, py + 0.38, 4.4, 0.26, det, 11, BODY)
    py += ph + 0.12

rect(s, MARGIN, 6.15, 12.1, 0.75, fill=NAVY, round_=True, radius=0.12)
text(s, MARGIN + 0.35, 6.15, 11.4, 0.75, [[
    {"t": "Cambio de alcance gestionado:  ", "size": 13.5, "color": TEAL_LT, "bold": True, "font": SANS},
    {"t": "el 21-10-2026 se incorporaron Usuarios y Ticketera como cambio Mayor aprobado por el Product Owner, sin mover el hito ES2 (11-12-2026).",
     "size": 13.5, "color": WHITE, "font": SANS}]], anchor=MSO_ANCHOR.MIDDLE)

source(s, "La agilidad permitió absorber el nuevo alcance manteniendo la fecha comprometida.")
footer(s, 6)

# ================================================================ 7 · ARQUITECTURA
s = prs.slides.add_slide(BLANK)
kicker(s, "06 · ARQUITECTURA")
title(s, "Tres capas, monolito modular y aislado de la red clínica")
rule(s)

layers = [
    ("PRESENTACIÓN", "SPA React + TypeScript", "Dashboard, formularios y ticketera para cada rol.", TEAL),
    ("APLICACIÓN", "API REST FastAPI", "RBAC y lógica de negocio de los nueve módulos.", MAGENTA),
    ("DATOS", "PostgreSQL · SQLite", "Base relacional de 10 tablas + repositorio de evidencias.", INK),
]
ly = 1.95
for i, (k, t, d, col) in enumerate(layers):
    card(s, MARGIN, ly, 7.4, 1.32, fill=WHITE, line_color=LIGHT)
    rect(s, MARGIN, ly, 0.09, 1.32, fill=col)
    line(s, MARGIN + 0.35, ly + 0.2, 1.9, 0.35, k, 14, col, bold=True)
    line(s, MARGIN + 0.35, ly + 0.55, 6.8, 0.35, t, 17, INK, bold=True, font=DISPLAY)
    line(s, MARGIN + 0.35, ly + 0.92, 6.8, 0.32, d, 12.5, BODY)
    ly += 1.55

# right panel
rx = 8.3
rect(s, rx, 1.95, 4.42, 4.4, fill=NAVY, round_=True, radius=0.07)
text(s, rx + 0.35, 2.3, 3.7, 3.9, [
    [{"t": "Decisiones clave", "size": 15, "color": TEAL_LT, "bold": True, "font": SANS}],
    [{"t": "Aislado de Trakcare", "size": 13.5, "color": WHITE, "bold": True, "font": SANS}],
    [{"t": "Herramienta de gobierno, no sistema asistencial: evita riesgo técnico y regulatorio.", "size": 12.5, "color": LIGHT, "font": SANS}],
    [{"t": "On-premise / nube privada", "size": 13.5, "color": WHITE, "bold": True, "font": SANS}],
    [{"t": "Consistente con la sensibilidad de un Operador de Importancia Vital.", "size": 12.5, "color": LIGHT, "font": SANS}],
    [{"t": "Monolito modular", "size": 13.5, "color": WHITE, "bold": True, "font": SANS}],
    [{"t": "Separación clara por módulo sin el costo operativo de microservicios.", "size": 12.5, "color": LIGHT, "font": SANS}],
], space_after=8, line_spacing=1.08)

source(s, "Arquitectura en 3 capas: presentación, lógica de negocio y datos.")
footer(s, 7)

# ================================================================ 8 · DECISIONES
s = prs.slides.add_slide(BLANK)
kicker(s, "07 · DECISIONES TÉCNICAS")
title(s, "Cada tecnología se eligió con criterio, no por moda")
rule(s)

rows = [
    ("Backend", "FastAPI + SQLAlchemy", "4.30", "Tipado, Swagger automático y rendimiento asíncrono."),
    ("Frontend", "React 18 + TypeScript + Vite", "4.55", "Ecosistema maduro de gráficos y desarrollo incremental."),
    ("Base de datos", "PostgreSQL (SQLite en desarrollo)", "4.85", "Integridad referencial y auditoría; cero costo."),
    ("Metodología", "Scrum (ágil)", "4.70", "Validación incremental con el mandante."),
]
ry = 1.95
rh = 0.92
for i, (k, t, sc, d) in enumerate(rows):
    card(s, MARGIN, ry, 7.75, rh, fill=WHITE, line_color=LIGHT)
    line(s, MARGIN + 0.3, ry + 0.16, 1.6, 0.3, k, 11, MUTED, bold=True)
    line(s, MARGIN + 0.3, ry + 0.42, 6.4, 0.35, t, 15, INK, bold=True)
    line(s, MARGIN + 0.3, ry + 0.68, 6.9, 0.25, d, 11, BODY)
    rect(s, 8.5, ry, 1.5, rh, fill=TEAL_PALE)
    line(s, 8.5, ry, 1.5, rh, sc, 20, TEAL, bold=True, font=DISPLAY,
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    ry += rh + 0.13

# factibilidad panel
rect(s, 10.25, 1.95, 2.47, 4.0, fill=NAVY, round_=True, radius=0.07)
text(s, 10.55, 2.3, 1.95, 3.4, [
    [{"t": "Factibilidad", "size": 15, "color": TEAL_LT, "bold": True, "font": SANS}],
    [{"t": "Técnica", "size": 13, "color": WHITE, "bold": True, "font": SANS},
     {"t": "   ✓", "size": 13, "color": TEAL_LT, "font": SANS}],
    [{"t": "Económica", "size": 13, "color": WHITE, "bold": True, "font": SANS},
     {"t": "   ✓", "size": 13, "color": TEAL_LT, "font": SANS}],
    [{"t": "Implementativa", "size": 12.5, "color": WHITE, "bold": True, "font": SANS},
     {"t": "  ✓", "size": 12.5, "color": TEAL_LT, "font": SANS}],
    [{"t": "$0 en licencias", "size": 12.5, "color": LIGHT, "font": SANS}],
    [{"t": "100 % software libre", "size": 12.5, "color": LIGHT, "font": SANS}],
], space_after=8, line_spacing=1.12)

source(s, "Matriz ponderada (escala 1–5): la alternativa con mayor puntaje fue la elegida.")
footer(s, 8)

# ================================================================ 9 · SEGURIDAD
s = prs.slides.add_slide(BLANK)
kicker(s, "08 · SEGURIDAD")
title(s, "Defensa en profundidad en cada capa")
rule(s)

segs = [
    ("RBAC", "Cinco roles con acceso mínimo por responsabilidad."),
    ("TLS", "Cifrado en tránsito en toda la aplicación."),
    ("Cifrado en reposo", "Evidencia y adjuntos con permisos restringidos."),
    ("Auditoría", "Registro de quién, qué y cuándo en operaciones sensibles."),
    ("Anonimato", "Tickets sin nombre, correo, IP ni vínculo al emisor."),
    ("Anti-abuso", "Rate limiting, validación estricta y adjuntos controlados."),
]
cw = 3.92
ch = 1.7
gapx = 0.17
gapy = 0.2
for i, (k, d) in enumerate(segs):
    col = i % 3
    row = i // 3
    x = MARGIN + col * (cw + gapx)
    y = 1.95 + row * (ch + gapy)
    card(s, x, y, cw, ch)
    line(s, x + 0.3, y + 0.28, cw - 0.6, 0.45, k, 18, TEAL if row == 0 else INK,
         bold=True, font=DISPLAY)
    text(s, x + 0.3, y + 0.82, cw - 0.6, 0.8,
         [[{"t": d, "size": 12.5, "color": BODY, "font": SANS}]], line_spacing=1.1)

source(s, "La seguridad se incorpora desde el diseño, no se agrega al final.")
footer(s, 9)

# ================================================================ 10 · KPI
s = prs.slides.add_slide(BLANK)
kicker(s, "09 · CÓMO SE MIDE EL ÉXITO")
title(s, "Resultados, no actividad")
rule(s)

kpis = [
    ("≥ 60 %", "madurez global al cierre", TEAL),
    ("≥ 80 %", "controles con evidencia", TEAL),
    ("100 %", "incidentes reportados en plazo", MAGENTA),
    ("≥ 90 %", "terceros con cláusulas cumplidas", TEAL),
    ("≤ 24 h", "primera respuesta a tickets", INK),
    ("≥ 90 %", "tickets gestionados en SLA", INK),
]
cw = 3.92
ch = 1.55
gapx = 0.17
gapy = 0.2
for i, (v, d, col) in enumerate(kpis):
    col_i = i % 3
    row = i // 3
    x = MARGIN + col_i * (cw + gapx)
    y = 1.95 + row * (ch + gapy)
    card(s, x, y, cw, ch)
    rect(s, x, y, cw, 0.12, fill=col)
    line(s, x + 0.3, y + 0.3, cw - 0.6, 0.7, v, 30, col, bold=True, font=DISPLAY)
    line(s, x + 0.3, y + 1.0, cw - 0.6, 0.4, d, 13.5, INK, bold=True)

rect(s, MARGIN, 5.6, 12.1, 0.9, fill=TEAL_PALE, round_=True, radius=0.12)
text(s, MARGIN + 0.3, 5.6, 11.5, 0.9, [[
    {"t": "Metas referenciales definidas en el informe.  ", "size": 13.5, "color": TEAL, "bold": True, "font": SANS},
    {"t": "Se baselinizan con datos reales durante la validación (UAT) y la operación.",
     "size": 13.5, "color": INK, "font": SANS}]], anchor=MSO_ANCHOR.MIDDLE)

source(s, "Once KPI SMART conectan cada módulo con una meta verificable.")
footer(s, 10)

# ================================================================ 11 · CRONOGRAMA
s = prs.slides.add_slide(BLANK)
kicker(s, "10 · CRONOGRAMA")
title(s, "Once semanas, hitos verificables")
rule(s)

# timeline bar
rect(s, MARGIN, 2.7, 12.1, 0.07, fill=LIGHT)
milestones = [
    ("09-10", "Avance EF2", 0.6, TEAL),
    ("21-10", "Cambio Mayor", 2.6, MAGENTA),
    ("06-11", "Usuarios", 4.8, TEAL),
    ("20-11", "Ticketera", 6.9, TEAL),
    ("04-12", "UAT", 9.0, MAGENTA),
    ("11-12", "ES2", 11.2, NAVY),
]
for date, name, x, col in milestones:
    rect(s, MARGIN + x, 2.58, 0.16, 0.32, fill=col, round_=True, radius=0.5)
    line(s, MARGIN + x - 0.9, 2.95, 2.0, 0.3, date, 13, INK, bold=True)
    line(s, MARGIN + x - 0.9, 3.2, 2.0, 0.3, name, 11.5, BODY)

# phases summary
ph = [
    ("Formulación y diseño", "Requisitos, BPMN, UML, datos y arquitectura."),
    ("Desarrollo", "Sprints Usuarios y Ticketera, con pruebas por sprint."),
    ("Validación", "Pruebas CP-01 a CP-38 y UAT con el mandante."),
    ("Cierre", "Informe ABPro, demo y defensa del proyecto."),
]
cw = (12.1 - 3 * 0.17) / 4
for i, (k, d) in enumerate(ph):
    x = MARGIN + i * (cw + 0.17)
    card(s, x, 3.75, cw, 2.1)
    rect(s, x, 3.75, cw, 0.12, fill=TEAL if i % 2 == 0 else NAVY)
    line(s, x + 0.22, 4.05, cw - 0.44, 0.6, k, 14, INK, bold=True, font=DISPLAY)
    text(s, x + 0.22, 4.7, cw - 0.44, 1.0,
         [[{"t": d, "size": 11.5, "color": BODY, "font": SANS}]], line_spacing=1.1)

source(s, "La planificación por sprints conserva holgura para proteger la fecha ES2.")
footer(s, 11)

# ================================================================ 12 · ESTADO
s = prs.slides.add_slide(BLANK)
kicker(s, "11 · ESTADO ACTUAL")
title(s, "No es una idea en papel: es un producto que ya funciona")
rule(s)

stats = [
    ("12", "grupos de endpoints", "API REST FastAPI con autenticación JWT y RBAC."),
    ("39", "pruebas automatizadas", "Casos funcionales y de seguridad con datos de prueba."),
    ("9", "módulos en la SPA", "Dashboard y flujos de trabajo completos en React."),
]
cw = 3.92
gap = 0.17
for i, (v, k, d) in enumerate(stats):
    x = MARGIN + i * (cw + gap)
    card(s, x, 1.95, cw, 2.5)
    line(s, x + 0.3, 2.15, cw - 0.6, 1.0, v, 56, TEAL if i != 1 else MAGENTA,
         bold=True, font=DISPLAY)
    line(s, x + 0.3, 3.15, cw - 0.6, 0.4, k, 15, INK, bold=True)
    text(s, x + 0.3, 3.6, cw - 0.6, 0.8,
         [[{"t": d, "size": 12, "color": BODY, "font": SANS}]], line_spacing=1.1)

rect(s, MARGIN, 4.85, 12.1, 1.55, fill=NAVY, round_=True, radius=0.07)
text(s, MARGIN + 0.4, 4.85, 11.3, 1.55, [
    [{"t": "Ya está operativo:  ", "size": 14.5, "color": TEAL_LT, "bold": True, "font": SANS},
     {"t": "catálogo de controles ISO 27001 precargado, cinco roles, formulario público anónimo, "
           "bandeja confidencial, notificaciones y conversión de denuncia a incidente formal.",
      "size": 14.5, "color": WHITE, "font": SANS}],
], anchor=MSO_ANCHOR.MIDDLE, line_spacing=1.15)

source(s, "El prototipo funcional respalda la defensa: la solución está construida y probada.")
footer(s, 12)

# ================================================================ 13 · CIERRE
s = prs.slides.add_slide(BLANK)
rect(s, 0, 0, SLIDE_W, SLIDE_H, fill=NAVY)
rect(s, 0, 0, 0.28, SLIDE_H, fill=TEAL)
rect(s, 0.28, 0, 0.06, SLIDE_H, fill=MAGENTA)

line(s, MARGIN, 0.8, 10.0, 0.35, "12 · CIERRE", 13, TEAL_LT, bold=True)
line(s, MARGIN, 1.5, 11.8, 1.0, "De dispersión a trazabilidad", 44, WHITE, bold=True,
     font=DISPLAY)
text(s, MARGIN, 2.65, 11.6, 0.9, [[
    {"t": "El SGSI alinea problema, solución y arquitectura en una sola plataforma "
          "para decidir con evidencia y responder dentro de plazo.", "size": 17,
     "color": LIGHT, "font": SANS}]], line_spacing=1.15)

verbs = [
    ("MEDIR", "Madurez por dominio y global.", TEAL_LT),
    ("REACCIONAR", "Incidentes y plazos legales.", TEAL_LT),
    ("DEMOSTRAR", "Evidencia auditable y reportes.", TEAL_LT),
]
cw = 3.92
gap = 0.17
for i, (k, d, col) in enumerate(verbs):
    x = MARGIN + i * (cw + gap)
    rect(s, x, 4.1, cw, 1.7, fill=None, line_color=TEAL_LT, line_w=1.2,
         round_=True, radius=0.09)
    line(s, x + 0.3, 4.4, cw - 0.6, 0.6, k, 24, col, bold=True, font=DISPLAY)
    line(s, x + 0.3, 5.05, cw - 0.6, 0.6, d, 13.5, LIGHT)

text(s, MARGIN, 6.35, 12.0, 0.8, [
    [{"t": "Priscila Bahamóndez", "size": 14, "color": WHITE, "bold": True, "font": SANS},
     {"t": "   ·   Proyecto de Título TIHI84   ·   Hospital Félix Bulnes Cerda", "size": 14, "color": FAINT, "font": SANS}],
    [{"t": "Gracias", "size": 14, "color": TEAL_LT, "bold": True, "font": SANS}],
], space_after=6)

# ---------------------------------------------------------------- save
prs.core_properties.title = "SGSI — Defensa de Proyecto de Título"
prs.core_properties.author = "Priscila Bahamóndez"
prs.core_properties.subject = "Sistema de Gestión de Seguridad de la Información"
prs.core_properties.language = "es-CL"

import os
os.makedirs("Documentacion/Entregas/Defensa", exist_ok=True)
OUT = "Documentacion/Entregas/Defensa/SGSI_Defensa_Proyecto.pptx"
prs.save(OUT)
print("Guardado:", OUT, "| slides:", len(prs.slides.__iter__.__self__._sldIdLst))
