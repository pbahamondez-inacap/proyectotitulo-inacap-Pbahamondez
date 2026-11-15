# -*- coding: utf-8 -*-
"""
Construye la presentación "SGSI — Evaluación Sumativa 2 (ES2)" alineada a la rúbrica
(17 criterios 2.1.1.1 … 2.1.6.17) usando python-pptx.
"""
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from PIL import Image

REPO = "/Users/nahum.sanchez/Documents/Esposa/Proyecto-Titulo/Repositorios/proyectotitulo-inacap-Pbahamondez"
MOCK = os.path.join(REPO, "Documentacion", "Entregas", "Defensa", "mockup")
OUT = os.path.join(REPO, "Documentacion", "Entregas", "Defensa",
                   "SGSI_ES2_Rubrica_Presentacion.pptx")

# ---------------------------------------------------------------- colores / medidas
NAVY = RGBColor(0x15, 0x24, 0x3B)
NAVY2 = RGBColor(0x1E, 0x34, 0x55)
CRIMSON = RGBColor(0xA6, 0x19, 0x2E)
BLUE = RGBColor(0x1B, 0x6C, 0xA8)
SKY = RGBColor(0x9D, 0xB8, 0xD2)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
TEXT = RGBColor(0x21, 0x2B, 0x38)
MUTED = RGBColor(0x5B, 0x6B, 0x7B)
LIGHT = RGBColor(0xF1, 0xF5, 0xF9)
CARD = RGBColor(0xF8, 0xFA, 0xFC)
BORDER = RGBColor(0xD9, 0xE2, 0xEC)
GREEN = RGBColor(0x1E, 0x7B, 0x4F)
GOLD = RGBColor(0xB0, 0x78, 0x1F)

FONT = "Calibri"
SW = 13.333
SH = 7.5

prs = Presentation()
prs.slide_width = Inches(SW)
prs.slide_height = Inches(SH)
BLANK = prs.slide_layouts[6]


def S(size=12, bold=False, color=TEXT, italic=False, font=FONT):
    return {"size": size, "bold": bold, "color": color, "italic": italic, "font": font}


def add_text(slide, x, y, w, h, paras, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, space_after=3):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    for i, para in enumerate(paras):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.space_after = Pt(space_after)
        runs = para if isinstance(para, list) else [para]
        for (t, st) in runs:
            r = p.add_run()
            r.text = t
            f = r.font
            f.size = Pt(st.get("size", 12))
            f.bold = st.get("bold", False)
            f.italic = st.get("italic", False)
            f.name = st.get("font", FONT)
            if "color" in st:
                f.color.rgb = st["color"]
    return box


def rect(slide, x, y, w, h, fill, line=None, shape=MSO_SHAPE.RECTANGLE, radius=None):
    sh = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    if fill is None:
        sh.fill.background()
    else:
        sh.fill.solid()
        sh.fill.fore_color.rgb = fill
    if line is None:
        sh.line.fill.background()
    else:
        sh.line.color.rgb = line
        sh.line.width = Pt(0.75)
    if radius is not None:
        try:
            sh.adjustments[0] = radius
        except Exception:
            pass
    return sh


def header(slide, kicker, title, idx):
    rect(slide, 0, 0, SW, 1.06, NAVY)
    rect(slide, 0, 1.06, SW, 0.045, CRIMSON)
    rect(slide, 0.55, 0.20, 0.07, 0.62, CRIMSON)
    add_text(slide, 0.80, 0.12, 11.6, 0.30, [[(kicker, S(11, True, SKY))]])
    add_text(slide, 0.80, 0.40, 11.8, 0.62, [[(title, S(20, True, WHITE))]])
    footer(slide, idx)


def footer(slide, idx):
    rect(slide, 0, 7.16, SW, 0.34, NAVY)
    add_text(slide, 0.55, 7.20, 9.0, 0.26,
             [[("SGSI · Hospital Félix Bulnes Cerda · Evaluación Sumativa 2 (ES2) · Unidad 2",
                S(8.5, False, SKY))]])
    add_text(slide, 11.6, 7.20, 1.2, 0.26, [[(str(idx), S(9, True, WHITE))]], align=PP_ALIGN.RIGHT)


def card(slide, x, y, w, h, title, lines, title_color=BLUE, fill=CARD, size=10.5):
    rect(slide, x, y, w, h, fill, BORDER, MSO_SHAPE.ROUNDED_RECTANGLE, 0.05)
    paras = [[(title, S(12.5, True, title_color))]]
    for ln in lines:
        paras.append([("•  " + ln, S(size, False, TEXT))])
    add_text(slide, x + 0.14, y + 0.08, w - 0.28, h - 0.16, paras, space_after=3)


def table(slide, x, y, w, data, col_widths, font_size=10.5, row_h=0.34, header_fill=NAVY):
    rows = len(data)
    cols = len(data[0])
    total_h = row_h * rows
    gf = slide.shapes.add_table(rows, cols, Inches(x), Inches(y), Inches(w), Inches(total_h))
    tb = gf.table
    tb.first_row = False
    tb.horz_banding = False
    for ci, cw in enumerate(col_widths):
        tb.columns[ci].width = Inches(cw)
    for ri, row in enumerate(data):
        tb.rows[ri].height = Inches(row_h)
        for ci, val in enumerate(row):
            cell = tb.cell(ri, ci)
            cell.margin_left = Inches(0.06)
            cell.margin_right = Inches(0.06)
            cell.margin_top = Inches(0.02)
            cell.margin_bottom = Inches(0.02)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            tf = cell.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            r = p.add_run()
            r.text = str(val)
            f = r.font
            f.size = Pt(font_size)
            f.name = FONT
            if ri == 0:
                f.bold = True
                f.color.rgb = WHITE
                cell.fill.solid()
                cell.fill.fore_color.rgb = header_fill
            else:
                f.color.rgb = TEXT
                cell.fill.solid()
                cell.fill.fore_color.rgb = WHITE if ri % 2 == 0 else LIGHT
    return tb


def metric(slide, x, y, w, h, number, label, sub, accent=CRIMSON):
    rect(slide, x, y, w, h, CARD, BORDER, MSO_SHAPE.ROUNDED_RECTANGLE, 0.05)
    add_text(slide, x + 0.15, y + 0.12, w - 0.3, 0.75, [[(number, S(34, True, accent))]])
    add_text(slide, x + 0.15, y + 0.85, w - 0.3, 0.55, [[(label, S(13.5, True, NAVY))]])
    add_text(slide, x + 0.15, y + 1.30, w - 0.3, h - 1.4, [[(sub, S(10, False, MUTED))]])


def add_image(slide, path, x, y, w, caption, cap_color=MUTED):
    im = Image.open(path)
    h = w * (im.height / im.width)
    slide.shapes.add_picture(path, Inches(x), Inches(y), width=Inches(w))
    rect(slide, x - 0.03, y - 0.03, w + 0.06, h + 0.06, None, BORDER)
    add_text(slide, x, y + h + 0.05, w, 0.28, [[(caption, S(9, False, cap_color))]], align=PP_ALIGN.CENTER)
    return h


def note(slide, y, text, color=GREEN):
    rect(slide, 0.55, y, SW - 1.1, 0.44, LIGHT, None, MSO_SHAPE.ROUNDED_RECTANGLE, 0.5)
    add_text(slide, 0.75, y + 0.07, SW - 1.5, 0.32, [[(text, S(11, True, color))]])


def new_slide():
    return prs.slides.add_slide(BLANK)


# ---------------------------------------------------------------- imágenes (orden = hora)
imgs = sorted([f for f in os.listdir(MOCK) if f.lower().endswith(".png")])
img = {k: os.path.join(MOCK, imgs[i]) for k, i in
       zip(["login", "dashboard", "reporte", "tickets_anon", "ticketera"], range(5))}

# ================================================================ 1 · PORTADA
s = new_slide()
rect(s, 0, 0, SW, SH, NAVY)
rect(s, 0, 0, SW, 0.14, CRIMSON)
rect(s, 0, SH - 0.14, SW, 0.14, CRIMSON)
add_text(s, 0.9, 1.05, 11.5, 0.4,
         [[("EVALUACIÓN SUMATIVA 2 (ES2) · UNIDAD 2 · DESARROLLO E IMPLEMENTACIÓN",
            S(14, True, SKY))]])
add_text(s, 0.9, 1.5, 11.5, 1.5, [[("SGSI", S(66, True, WHITE))]])
add_text(s, 0.9, 2.95, 11.5, 0.5,
         [[("Sistema de Gestión de Seguridad de la Información", S(24, False, WHITE))]])
add_text(s, 0.9, 3.5, 11.5, 0.5,
         [[("De planillas dispersas a gobierno auditable", S(16, False, SKY))]])
rect(s, 0.93, 4.35, 4.2, 0.05, CRIMSON)
add_text(s, 0.9, 4.6, 11.5, 1.5, [
    [("Priscila Bahamóndez  ·  Proyecto de Título TIHI84  ·  INACAP", S(15, False, WHITE))],
    [("Mandante: Miguel Godoy (Encargado de Ciberseguridad) · Hospital Félix Bulnes Cerda",
      S(13, False, SKY))],
    [("Noviembre 2026", S(13, False, SKY))],
])
add_text(s, 0.9, 6.55, 11.5, 0.5,
         [[("Alineada a la rúbrica ES2 (17 criterios 2.1.1.1 → 2.1.6.17) y a los 17 entregables de la Unidad 2.",
            S(11.5, False, RGBColor(0x8A, 0xA3, 0xBE)))]])
s.notes_slide.notes_text_frame.text = (
    "Presentación del proyecto SGSI para el Hospital Félix Bulnes Cerda, estructurada según los 17 criterios "
    "de la rúbrica de la Evaluación Sumativa 2 (Unidad 2).")

# ================================================================ 2 · AGENDA
s = new_slide()
header(s, "AGENDA", "Estructura: mapeo a los 17 criterios de la rúbrica", 2)
grupos = [
    ("2.1.1", "Análisis y recursos", "Criterios 1–2 · Entregables 1–2", BLUE),
    ("2.1.2", "Modelamiento y diseño", "Criterios 3–8 · Entregables 3–8", BLUE),
    ("2.1.3", "Indicadores y servicios", "Criterios 9–10 · Entregables 9–10", BLUE),
    ("2.1.4", "Calidad y estándares", "Criterios 11–12 · Entregables 11–12", BLUE),
    ("2.1.5", "Servicios TI y continuidad", "Criterios 13–15 · Entregables 13–15", BLUE),
    ("2.1.6", "Planificación y justificación", "Criterios 16–17 · Entregables 16–17", BLUE),
]
gx, gy = 0.55, 1.45
gw, gh, gap = 3.98, 1.55, 0.22
for i, (code, tit, sub, _c) in enumerate(grupos):
    r, c = divmod(i, 3)
    x = gx + c * (gw + gap)
    y = gy + r * (gh + gap + 0.12)
    rect(s, x, y, gw, gh, CARD, BORDER, MSO_SHAPE.ROUNDED_RECTANGLE, 0.05)
    rect(s, x, y, 0.08, gh, CRIMSON)
    add_text(s, x + 0.22, y + 0.14, gw - 0.4, 0.4, [[(code, S(16, True, CRIMSON))]])
    add_text(s, x + 0.22, y + 0.55, gw - 0.4, 0.4, [[(tit, S(13.5, True, NAVY))]])
    add_text(s, x + 0.22, y + 0.98, gw - 0.4, 0.45, [[(sub, S(10.5, False, MUTED))]])
add_text(s, 0.55, 5.55, 12.2, 0.9, [
    [("Cada criterio de la rúbrica se demuestra con el contenido del entregable correspondiente, más imágenes representativas del sistema (capturas del mockup).", S(11.5, False, MUTED))],
    [("Además de los 17 criterios, se incluye contexto del proyecto, el producto, una vista demo y las conclusiones.", S(11.5, False, MUTED))],
])
s.notes_slide.notes_text_frame.text = "Agenda: 6 bloques que agrupan los 17 criterios de la rúbrica."

# ================================================================ 3 · CONTEXTO
s = new_slide()
header(s, "CONTEXTO", "El problema y la solución", 3)
add_text(s, 0.55, 1.30, 7.3, 0.4, [[("PROBLEMA", S(12, True, CRIMSON))]])
card(s, 0.55, 1.72, 7.3, 2.0, "Hospital Félix Bulnes Cerda (Operador de Importancia Vital)", [
    "Ley 21.663: demostrar madurez ISO/IEC 27001 y reportar incidentes a la ANCI en plazos legales.",
    "Plazos: alerta temprana 3 h · reporte 72 h (alta/crítica) · 15 días (media/baja).",
    "Hoy se gestiona a mano: planillas, correos y actas; sin repositorio único.",
], title_color=CRIMSON)
add_text(s, 0.55, 3.90, 7.3, 0.4, [[("SOLUCIÓN", S(12, True, BLUE))]])
card(s, 0.55, 4.32, 7.3, 2.35, "SGSI — sistema GRC único y auditable", [
    "Centraliza controles, evidencias, madurez, incidentes, terceros, personas y reportes.",
    "Agrega Usuarios (RBAC) y Ticketera anónima (formulario público /reportar).",
    "Alcance: 9 módulos · 5 roles RBAC · 5 procesos BPMN · 10 tablas · 11 KPI · 38 casos de prueba.",
    "Stack: React + FastAPI + PostgreSQL (SQLite en desarrollo) · metodología Scrum.",
], title_color=BLUE)
add_image(s, img["login"], 8.15, 1.60, 4.55, "Login del sistema (JWT + RBAC)")
s.notes_slide.notes_text_frame.text = "Contexto: obligación legal del hospital y la solución GRC construida."

# ================================================================ 4 · PRODUCTO (9 módulos)
s = new_slide()
header(s, "EL PRODUCTO", "Nueve módulos, una sola fuente de verdad", 4)
mods = [
    ("01", "Controles", "Catálogo ISO 27001 (Anexo A)."),
    ("02", "Evidencias", "Documentos y trazabilidad."),
    ("03", "Madurez", "% por dominio y global."),
    ("04", "Incidentes", "Taxonomía ANCI y plazos."),
    ("05", "Terceros", "Cláusulas de seguridad."),
    ("06", "Personas", "Ciclo de vida del personal."),
    ("07", "Reportería", "Resumen y exportación CSV."),
    ("08", "Usuarios", "Cuentas, roles, baja lógica."),
    ("09", "Ticketera", "Denuncias y reportes anónimos."),
]
gx, gy = 0.55, 1.42
cw, ch, gpx, gpy = 2.62, 1.05, 0.16, 0.16
for i, (num, tit, desc) in enumerate(mods):
    r, c = divmod(i, 3)
    x = gx + c * (cw + gpx)
    y = gy + r * (ch + gpy)
    rect(s, x, y, cw, ch, CARD, BORDER, MSO_SHAPE.ROUNDED_RECTANGLE, 0.08)
    add_text(s, x + 0.14, y + 0.10, cw - 0.28, 0.35,
             [[(num + "  ", S(11, True, CRIMSON)), (tit, S(12.5, True, NAVY))]])
    add_text(s, x + 0.14, y + 0.48, cw - 0.28, 0.5, [[(desc, S(9.5, False, MUTED))]])
add_text(s, 0.55, 5.35, 8.1, 0.8, [
    [("El producto reemplaza el trabajo manual disperso por un sistema auditable y visual.", S(11.5, True, NAVY))],
    [("La Ticketera es el diferenciador del alcance final: canal anónimo de denuncias/reportes.", S(11, False, MUTED))],
])
add_image(s, img["dashboard"], 8.62, 1.60, 4.15, "Dashboard de madurez (Recharts)")
s.notes_slide.notes_text_frame.text = "Producto: 9 módulos funcionales; destacar la Ticketera como diferenciador."

# ================================================================ 5 · VISTA DEMO (3 imágenes)
s = new_slide()
header(s, "VISTA DEL SISTEMA", "Capturas representativas de la aplicación", 5)
add_text(s, 0.55, 1.30, 12.2, 0.4,
         [[("Interfaz web SPA React con identidad del Hospital Clínico Félix Bulnes.", S(12, False, MUTED))]])
iw = 3.92
gapx = 0.27
x0 = (SW - (3 * iw + 2 * gapx)) / 2
caps = [
    ("Reportería — resumen ejecutivo y exportación CSV", img["reporte"]),
    ("Formulario público de tickets anónimos (/reportar)", img["tickets_anon"]),
    ("Ticketera — bandeja confidencial del encargado", img["ticketera"]),
]
for i, (cap, path) in enumerate(caps):
    x = x0 + i * (iw + gapx)
    add_image(s, path, x, 1.85, iw, cap)
add_text(s, 0.55, 4.95, 12.2, 1.4, [
    [("El sistema ya está construido y operativo: los módulos de negocio, la administración de usuarios y el canal público anónimo funcionan en la SPA.", S(12, True, NAVY))],
    [("Estas capturas corresponden al mockup del sistema presentado en la defensa del proyecto.", S(11, False, MUTED))],
])
s.notes_slide.notes_text_frame.text = "Demo: reportería, formulario público anónimo y bandeja de la ticketera."

# ================================================================ 6 · 2.1.1.1
s = new_slide()
header(s, "CRITERIO 2.1.1.1 · ENTREGABLE 1", "Análisis comparativo y selección de tecnologías y metodología", 6)
card(s, 0.55, 1.35, 7.0, 4.6, "Método y comparación", [
    "Matriz ponderada: escala 1–5 × peso sobre 7 criterios (madurez, curva de aprendizaje, seguridad, costo, desempeño, integración, soporte).",
    "Backend: FastAPI vs Django vs Flask vs Node/Express.",
    "Frontend: React+Vite vs Angular vs Vue 3.",
    "Base de datos: PostgreSQL vs MySQL vs SQLite.",
    "Metodología: Scrum vs Kanban vs Cascada.",
    "Validación con estudio de factibilidad técnica, económica e implementativa.",
])
table(s, 7.75, 1.35, 5.0, [
    ["Capa", "Selección", "Puntaje"],
    ["Backend", "FastAPI + SQLAlchemy", "4.30"],
    ["Frontend", "React 18 + TS + Vite", "4.55"],
    ["Base de datos", "PostgreSQL (SQLite dev)", "4.85"],
    ["Metodología", "Scrum (ágil)", "4.70"],
], [2.0, 2.2, 0.8], font_size=10, row_h=0.34)
add_text(s, 7.75, 3.55, 5.0, 2.4, [
    [("Factibilidad", S(12, True, BLUE))],
    [("Técnica ✓   Económica ✓   Implementativa ✓", S(11, False, GREEN))],
    [("$0 en licencias — 100 % software libre/open source.", S(11, False, TEXT))],
    [("Stack elegido por mayor puntaje y por ajuste al equipo y al plazo del semestre.", S(11, False, MUTED))],
])
note(s, 6.25, "Selección objetiva y replicable: la alternativa con mayor puntaje ponderado fue la elegida.")
s.notes_slide.notes_text_frame.text = "Criterio 2.1.1.1: matriz ponderada y factibilidad técnica, económica e implementativa."

# ================================================================ 7 · 2.1.1.2
s = new_slide()
header(s, "CRITERIO 2.1.1.2 · ENTREGABLE 2", "Herramientas, lenguajes, hardware y servicios TI", 7)
card(s, 0.55, 1.35, 2.95, 3.6, "Lenguajes", [
    "Python 3.14 (backend).",
    "TypeScript 5.7 (frontend).",
    "HTML5 + CSS3.",
    "SQL (PostgreSQL/SQLite).",
    "JSON (API y JWT).",
])
card(s, 3.62, 1.35, 3.4, 3.6, "Stack técnico", [
    "FastAPI + Uvicorn + SQLAlchemy + Pydantic.",
    "PyJWT + PBKDF2 (autenticación).",
    "React 18 + Vite + Recharts + React Router.",
    "smtplib / slowapi / psycopg.",
])
card(s, 7.14, 1.35, 3.0, 3.6, "Hardware (referencial)", [
    "Desarrollo: portátil 8 GB RAM / SSD.",
    "APP-01: 2 vCPU · 4 GB · 40 GB.",
    "DB-01: 2 vCPU · 4 GB · 100 GB RAID1.",
    "NAS-01: 100+ GB evidencias/adjuntos.",
])
card(s, 10.26, 1.35, 2.52, 3.6, "Servicios TI", [
    "Hosting, DNS, TLS.",
    "Respaldo y monitoreo.",
    "Mesa de ayuda.",
    "Relay SMTP institucional (requerido).",
], size=10)
note(s, 5.15, "9 módulos · 5 roles RBAC · CRUD Usuarios solo admin_sistema · tickets solo encargado.")
add_text(s, 0.55, 5.70, 12.2, 0.9, [
    [("Herramientas de desarrollo y modelado: VS Code · Git/GitHub · venv/pip · Node/npm · Swagger UI · DBeaver · Draw.io · Mermaid.", S(11, False, MUTED))],
])
s.notes_slide.notes_text_frame.text = "Criterio 2.1.1.2: lenguajes, stack, hardware y servicios TI requeridos."

# ================================================================ 8 · 2.1.2.3
s = new_slide()
header(s, "CRITERIO 2.1.2.3 · ENTREGABLE 3", "BPMN de los procesos de negocio (5 procesos con subprocesos)", 8)
table(s, 0.55, 1.35, 12.23, [
    ["Proceso", "Subprocesos principales"],
    ["P1 · Gestión de controles ISO/IEC 27001", "Registrar control · gestionar evidencia · actualizar estado · validar/aprobar · publicar madurez"],
    ["P2 · Gestión de incidentes", "Clasificar (taxonomía ANCI) · computar plazos (3 h/72 h/15 d) · alertar · reportar a ANCI · contener/cerrar"],
    ["P3 · Gestión de terceros/proveedores", "Registrar contrato · revisar checklist · verificar cumplimiento · corregir · publicar estado"],
    ["P4 · Gestión de usuarios", "Alta · edición · restablecer contraseña · habilitar/deshabilitar (baja lógica) · auditar"],
    ["P5 · Gestión de tickets (denuncias/reportes)", "Formulario público · anonimizar · notificar · analizar · derivar a incidente o cerrar"],
], [4.2, 8.03], font_size=10.5, row_h=0.62)
note(s, 5.55, "Notación BPMN 2.0 (pools, carriles, eventos, compuertas, flujos de mensaje) · archivos .drawio en 03_bpmn/.")
add_text(s, 0.55, 6.10, 12.2, 0.7, [
    [("Al menos tres procesos principales con subprocesos: se modelaron cinco (P1–P5), incorporando Usuarios y Ticketera tras el cambio de alcance del 21-10-2026.", S(11, False, MUTED))],
])
s.notes_slide.notes_text_frame.text = "Criterio 2.1.2.3: cinco procesos BPMN con sus subprocesos y actores."

# ================================================================ 9 · 2.1.2.4
s = new_slide()
header(s, "CRITERIO 2.1.2.4 · ENTREGABLE 4", "UML: casos de uso (UC-01 a UC-15) y diagrama de componentes", 9)
card(s, 0.55, 1.35, 3.6, 4.55, "Actores", [
    "encargado (negocio + tickets).",
    "admin_contratos (terceros).",
    "referente_tecnico (lectura).",
    "director (lectura).",
    "admin_sistema (solo usuarios).",
    "Funcionario/denunciante anónimo (sin autenticación).",
])
card(s, 4.27, 1.35, 4.35, 4.55, "Casos de uso destacados", [
    "UC-01 login · UC-02/03 controles y evidencias.",
    "UC-05 incidentes · UC-08 exportar reportes.",
    "UC-09/10 gestionar usuarios, roles y estado.",
    "UC-11 crear ticket público · UC-12 bandeja.",
    "UC-13 convertir ticket en incidente.",
    "UC-14 consultar estado por código · UC-15 notificar.",
])
card(s, 8.74, 1.35, 4.04, 4.55, "Componentes (3 capas)", [
    "SPA React (páginas, componentes, api.ts).",
    "API FastAPI: routers auth, negocio, usuarios, tickets, public_tickets.",
    "Seguridad JWT/PBKDF2 + RBAC (security.py, deps.py).",
    "Datos: PostgreSQL/SQLite + archivos de evidencias.",
    "Externo: relay SMTP institucional.",
])
note(s, 6.05, "Relaciones «include»/«extend» documentadas por caso de uso · .drawio en 04_uml/.")
s.notes_slide.notes_text_frame.text = "Criterio 2.1.2.4: 15 casos de uso con descripción y diagrama de componentes."

# ================================================================ 10 · 2.1.2.5
s = new_slide()
header(s, "CRITERIO 2.1.2.5 · ENTREGABLE 5", "Modelo de datos relacional y diccionario de datos", 10)
card(s, 0.55, 1.35, 5.9, 3.3, "10 tablas", [
    "usuarios · controles · evidencias · incidentes · terceros.",
    "persona_controles · tickets · ticket_adjuntos · notificaciones · auditoria_usuarios.",
    "Enums: Role, Dominio, EstadoControl, Severidad, EstadoIncidente, TipoTicket, CategoriaTicket, EstadoTicket, MedioNotificacion.",
])
card(s, 6.57, 1.35, 6.21, 3.3, "Relaciones y cardinalidades", [
    "controles 1—N evidencias · tickets 1—N adjuntos y notificaciones.",
    "tickets 0..1 incidente (relación 1:1 al convertir).",
    "usuarios actor/objetivo de auditoria_usuarios.",
    "Diccionario con tipos, PK/FK, índices, restricciones y catálogos de valores.",
])
rect(s, 0.55, 4.85, 12.23, 1.15, RGBColor(0xFB, 0xF1, 0xF2), None, MSO_SHAPE.ROUNDED_RECTANGLE, 0.05)
add_text(s, 0.75, 4.97, 11.9, 0.9, [
    [("Anonimato por diseño:  ", S(12, True, CRIMSON)),
     ("la tabla tickets NO tiene FK a usuarios ni guarda identidad, IP, user-agent o token del emisor.", S(12, False, TEXT))],
])
note(s, 6.15, "Modelo entidad-relación con diccionario de datos completo · .drawio en 05_modelo_datos/.")
s.notes_slide.notes_text_frame.text = "Criterio 2.1.2.5: 10 tablas, relaciones y anonimato por diseño."

# ================================================================ 11 · 2.1.2.6
s = new_slide()
header(s, "CRITERIO 2.1.2.6 · ENTREGABLE 6", "Topología de comunicación: 3 zonas y firewall doble", 11)
card(s, 0.55, 1.35, 3.95, 2.5, "Zona de usuarios (LAN)", [
    "Estaciones de trabajo de los 5 roles y funcionarios.",
    "Acceso a la SPA por HTTPS 443.",
    "Formulario /reportar anónimo, solo en la LAN.",
])
card(s, 4.62, 1.35, 3.95, 2.5, "Zona DMZ (servidores)", [
    "FW-01 perimetral (LAN 443; salida SMTP 587).",
    "APP-01: SPA + FastAPI/Uvicorn.",
    "FW-02 interno hacia la zona de datos.",
])
card(s, 8.69, 1.35, 4.09, 2.5, "Zona de datos (aislada)", [
    "PostgreSQL (TCP 5432).",
    "NAS evidencias/adjuntos (SMB3 445 / NFS 2049).",
    "Servidor de respaldo.",
])
table(s, 0.55, 4.05, 12.23, [
    ["Flujo", "Origen → destino", "Protocolo / puerto"],
    ["F1–F2", "Usuarios → FW-01 → APP-01", "HTTPS 443"],
    ["F3–F4", "APP-01 → FW-02 → PostgreSQL", "TCP 5432"],
    ["F5", "APP-01 → NAS", "SMB3 445 / NFS 2049"],
    ["F8", "APP-01 → relay SMTP institucional", "TCP 587 (STARTTLS)"],
    ["F7", "Encargado → portal ANCI", "Manual (sin API en línea)"],
], [1.2, 7.0, 4.03], font_size=10.5, row_h=0.40)
note(s, 6.55, "Aislado de Trakcare/red clínica · sin integración en línea con ANCI · firewalls segmentan cada zona.")
s.notes_slide.notes_text_frame.text = "Criterio 2.1.2.6: topología en 3 zonas con defensa en profundidad."

# ================================================================ 12 · 2.1.2.7
s = new_slide()
header(s, "CRITERIO 2.1.2.7 · ENTREGABLE 7", "Diseño de infraestructura (componentes y dimensionamiento)", 12)
table(s, 0.55, 1.35, 12.23, [
    ["Componente", "Especificación", "Software / función"],
    ["FW-01 / FW-02", "Firewall perimetral e interno", "HTTPS 443 LAN→APP · TCP 5432 APP→DB · SMB/NFS"],
    ["APP-01", "2 vCPU · 4 GB RAM · 40 GB SSD", "Nginx (SPA + rate limiting) + Uvicorn/FastAPI"],
    ["DB-01", "2 vCPU · 4 GB RAM · 100 GB SSD RAID1", "PostgreSQL 16"],
    ["NAS-01", "100+ GB", "evidencias/ y evidencias/tickets/ con permisos restringidos"],
    ["BK-01", "Según política de retención", "Respaldo BD + evidencias y adjuntos"],
    ["SMTP-01", "Servicio institucional existente", "Relay saliente TCP 587/STARTTLS"],
    ["SW-01 + 4 PC", "24 puertos Gigabit · 8 GB RAM/SSD", "Cliente ligero (navegador web)"],
], [1.9, 3.3, 7.03], font_size=10.5, row_h=0.52)
note(s, 5.55, "Capacidades referenciales a validar · crecimiento estimado ~24 GB/año (100 tickets/mes, 2 adjuntos ≤ 10 MB).")
add_text(s, 0.55, 6.10, 12.2, 0.7, [
    [("Patrón cliente-servidor en 3 capas: toda la lógica en APP-01 y los datos en DB-01/NAS-01.", S(11, False, MUTED))],
])
s.notes_slide.notes_text_frame.text = "Criterio 2.1.2.7: infraestructura y dimensionamiento por componente."

# ================================================================ 13 · 2.1.2.8
s = new_slide()
header(s, "CRITERIO 2.1.2.8 · ENTREGABLE 8", "Arquitectura de la solución: 3 capas + transversales", 13)
card(s, 0.55, 1.35, 3.95, 2.4, "Presentación", [
    "SPA React + TypeScript + Vite.",
    "Dashboard, formularios y ticketera.",
    "4 estaciones (navegador web).",
], title_color=CRIMSON)
card(s, 4.62, 1.35, 3.95, 2.4, "Aplicación", [
    "Nginx → FastAPI/Uvicorn (APP-01).",
    "9 módulos de negocio.",
    "JWT/PBKDF2 + RBAC · services.py.",
], title_color=CRIMSON)
card(s, 8.69, 1.35, 4.09, 2.4, "Datos + transversales", [
    "PostgreSQL (DB-01) + NAS evidencias.",
    "Seguridad, monitoreo, respaldo.",
    "Relay SMTP institucional.",
], title_color=CRIMSON)
rect(s, 0.55, 3.95, 12.23, 2.55, LIGHT, BORDER, MSO_SHAPE.ROUNDED_RECTANGLE, 0.04)
add_text(s, 0.75, 4.06, 11.9, 0.4, [[("Decisiones de arquitectura (ADR)", S(12.5, True, NAVY))]])
add_text(s, 0.75, 4.50, 11.9, 1.9, [
    [("•  ", S(10.5, True, BLUE)), ("Monolito modular (no microservicios): despliegue simple sin renunciar a la separación por módulo.", S(10.5, False, TEXT))],
    [("•  ", S(10.5, True, BLUE)), ("API REST documentada (OpenAPI/Swagger) y base de datos intercambiable vía SQLAlchemy (SGSI_DATABASE_URL).", S(10.5, False, TEXT))],
    [("•  ", S(10.5, True, BLUE)), ("Sin integración en línea con Trakcare ni ANCI.", S(10.5, False, TEXT))],
    [("•  ", S(10.5, True, BLUE)), ("Tickets anónimos sin FK a usuarios · endpoint público acotado + rate limiting · notificación tolerante a fallos.", S(10.5, False, TEXT))],
], space_after=4)
s.notes_slide.notes_text_frame.text = "Criterio 2.1.2.8: arquitectura de 3 capas con software y hardware por capa."

# ================================================================ 14 · 2.1.3.9
s = new_slide()
header(s, "CRITERIO 2.1.3.9 · ENTREGABLE 9", "11 KPI con detalle SMART", 14)
table(s, 0.55, 1.35, 12.23, [
    ["KPI", "Indicador", "Meta"],
    ["KPI-01", "% madurez global del SGSI", "≥ 60 % (100 % medio plazo)"],
    ["KPI-02", "% controles con evidencia", "≥ 80 %"],
    ["KPI-03", "% incidentes reportados en plazo legal", "100 %"],
    ["KPI-04", "% terceros con cláusulas cumplidas", "≥ 90 %"],
    ["KPI-05", "% controles de personas gestionados", "≥ 75 %"],
    ["KPI-06", "Disponibilidad del sistema (uptime)", "≥ 99 %"],
    ["KPI-07", "Tiempo medio de registro de incidente", "≤ 30 min"],
    ["KPI-08", "Adopción (sesiones/semana)", "≥ 20"],
    ["KPI-09", "Primera respuesta a tickets", "≤ 24 h hábiles"],
    ["KPI-10", "% tickets gestionados en SLA", "≥ 90 %"],
    ["KPI-11", "Baja de cuentas desvinculadas", "100 % en ≤ 1 día hábil"],
], [1.2, 7.3, 3.73], font_size=10.5, row_h=0.40)
note(s, 6.25, "Detalle SMART por KPI, con fuente de datos real en el SGSI · metas referenciales a validar con el mandante.")
s.notes_slide.notes_text_frame.text = "Criterio 2.1.3.9: 11 KPI SMART vinculados a cada módulo."

# ================================================================ 15 · 2.1.3.10
s = new_slide()
header(s, "CRITERIO 2.1.3.10 · ENTREGABLE 10", "SLA: disponibilidad, tiempos y recuperación", 15)
card(s, 0.55, 1.35, 3.95, 3.6, "Disponibilidad", [
    "Horario L–V 08:00–17:00.",
    "Uptime ≥ 99 % (SGSI y /reportar).",
    "Mantención programada: aviso ≥ 48 h, máx. 2 h.",
    "Monitoreo GET /api/health.",
])
table(s, 4.62, 1.35, 4.5, [
    ["Severidad", "Respuesta", "Resolución"],
    ["Crítica", "30 min", "4 h"],
    ["Alta", "1 h", "8 h"],
    ["Media", "4 h", "24 h"],
    ["Baja", "8 h", "5 días"],
], [1.6, 1.4, 1.5], font_size=10, row_h=0.34)
card(s, 9.24, 1.35, 3.54, 3.6, "Recuperación y tickets", [
    "RPO ≤ 24 h · RTO ≤ 8 h.",
    "Respaldo diario + semanal; retención 30 d.",
    "Ticket: acuse ≤ 24 h hábiles.",
    "Alta/crítica ≤ 4 h · ≥ 90 % en SLA.",
    "Baja de usuario ≤ 1 día hábil.",
], size=10)
note(s, 5.15, "Umbrales referenciales a confirmar con el mandante · SLA vinculados a KPI-06, KPI-09, KPI-10 y KPI-11.")
add_text(s, 0.55, 5.70, 12.2, 0.9, [
    [("Rendimiento: API p95 ≤ 500 ms · SPA ≤ 3 s · export CSV ≤ 10 s · ≥ 10 usuarios concurrentes.", S(11, False, MUTED))],
])
s.notes_slide.notes_text_frame.text = "Criterio 2.1.3.10: SLA de disponibilidad, tiempos por severidad y RPO/RTO."

# ================================================================ 16 · 2.1.4.11
s = new_slide()
header(s, "CRITERIO 2.1.4.11 · ENTREGABLE 11", "Plan de pruebas (CP-01 a CP-38)", 16)
card(s, 0.55, 1.35, 3.6, 4.35, "Niveles y herramientas", [
    "Unitarias, integración, sistema, UAT.",
    "Seguridad y rendimiento.",
    "Pytest · Vitest · Swagger UI.",
    "SQLite desechable · SMTP simulado.",
    "5 cuentas de prueba (datos ficticios).",
])
table(s, 4.27, 1.35, 8.51, [
    ["Módulo", "Casos de prueba"],
    ["Autenticación y roles", "CP-01 a CP-03, CP-07, CP-14"],
    ["Controles / Evidencias", "CP-04 a CP-06"],
    ["Madurez", "CP-08, CP-09"],
    ["Incidentes", "CP-10 a CP-12"],
    ["Terceros / Personas / Reportes", "CP-13 a CP-16"],
    ["No funcionales", "CP-17 a CP-19"],
    ["Usuarios", "CP-20 a CP-26"],
    ["Ticketera", "CP-27 a CP-38"],
], [3.1, 5.41], font_size=10.5, row_h=0.44)
note(s, 5.90, "Criterios de entrada/salida y matriz de trazabilidad requisito ↔ prueba · 39 pruebas automatizadas en el backend.")
s.notes_slide.notes_text_frame.text = "Criterio 2.1.4.11: plan de pruebas por niveles y 38 casos funcionales/de seguridad."

# ================================================================ 17 · 2.1.4.12
s = new_slide()
header(s, "CRITERIO 2.1.4.12 · ENTREGABLE 12", "Normas y estándares incorporados (N1–N15)", 17)
card(s, 0.55, 1.35, 6.0, 2.15, "SGSI y seguridad", [
    "ISO/IEC 27001:2022 (Anexo A) + ISO 27002:2022.",
    "OWASP Top 10 / ASVS / API Security.",
], title_color=CRIMSON)
card(s, 6.68, 1.35, 6.1, 2.15, "Marco legal", [
    "Ley 21.663: taxonomía ANCI y plazos de reporte.",
    "Ley 19.628 / 21.719: protección y minimización de datos.",
], title_color=CRIMSON)
card(s, 0.55, 3.62, 6.0, 2.15, "Calidad y requisitos", [
    "ISO/IEC 25010 (calidad de software).",
    "IEEE 830 (especificación de requisitos).",
], title_color=CRIMSON)
card(s, 6.68, 3.62, 6.1, 2.15, "Servicios y proyecto", [
    "ISO/IEC 20000 / ITIL · PMBOK.",
    "OpenAPI / Swagger (documentación de API).",
], title_color=CRIMSON)
note(s, 5.95, "Justificación detallada por norma · validación jurídica del canal de denuncias antes de producción.")
s.notes_slide.notes_text_frame.text = "Criterio 2.1.4.12: 15 normas/estándares con justificación de incorporación."

# ================================================================ 18 · 2.1.5.13
s = new_slide()
header(s, "CRITERIO 2.1.5.13 · ENTREGABLE 13", "Plan de implementación y gestión de disponibilidad", 18)
fases = [
    ("1 · Desarrollo", "SQLite local; módulos y unitarias.", "tsc --noEmit OK + unitarias verdes"),
    ("2 · Integración", "Staging PostgreSQL; UAT + SMTP simulado.", "CP-01–16 y CP-20–38 críticos"),
    ("3 · Producción", "APP/DB/NAS, /reportar, SMTP, admin_sistema.", "Aprobación del Encargado"),
    ("4 · Operación", "Monitoreo, respaldo y mantención.", "SLA cumplido"),
]
for i, (t, a, c) in enumerate(fases):
    x = 0.55 + i * 3.10
    rect(s, x, 1.35, 2.95, 2.6, CARD, BORDER, MSO_SHAPE.ROUNDED_RECTANGLE, 0.05)
    add_text(s, x + 0.14, 1.47, 2.66, 0.4, [[(t, S(12.5, True, CRIMSON))]])
    add_text(s, x + 0.14, 1.90, 2.66, 1.1, [[(a, S(10, False, TEXT))]])
    add_text(s, x + 0.14, 3.05, 2.66, 0.8, [[("Paso: ", S(9.5, True, BLUE)), (c, S(9.5, False, MUTED))]])
card(s, 0.55, 4.15, 12.23, 1.7, "Disponibilidad objetivo y elementos que la aseguran", [
    "Disponibilidad mensual ≥ 99 % en horario administrativo (SGSI y formulario público /reportar).",
    "Firewall doble y segmentación · respaldo diario (BK-01) · monitoreo /api/health · arquitectura 3 capas.",
    "Gestión de disponibilidad: monitoreo → medición → análisis → mejora → reporte mensual.",
])
note(s, 6.05, "10 actividades clave de puesta en producción · escalamiento vertical futuro según crecimiento.")
s.notes_slide.notes_text_frame.text = "Criterio 2.1.5.13: despliegue por fases y disponibilidad ≥ 99 %."

# ================================================================ 19 · 2.1.5.14
s = new_slide()
header(s, "CRITERIO 2.1.5.14 · ENTREGABLE 14", "Plan de continuidad del servicio (proactivo + reactivo)", 19)
card(s, 0.55, 1.35, 6.0, 3.5, "Medidas proactivas (prevención)", [
    "Respaldo diario + copia offline semanal.",
    "RAID1 en DB-01 · segmentación y firewalls.",
    "Monitoreo y alertas (/api/health).",
    "Documentación y línea base de configuración.",
    "Gestión de cambios controlada.",
], title_color=BLUE)
card(s, 6.68, 1.35, 6.1, 3.5, "Medidas reactivas (recuperación)", [
    "RPO ≤ 24 h · RTO ≤ 8 h hábiles.",
    "Procedimiento: detección → evaluación → activación → diagnóstico → recuperación → verificación → comunicación → lección.",
    "Pruebas trimestrales de restauración y simulacros semestrales.",
    "Recupera BD, evidencias, adjuntos y formulario público.",
], title_color=CRIMSON)
note(s, 5.05, "Amenazas cubiertas: falla de servidor, pérdida de BD/evidencias, ransomware, corte de energía, abuso del formulario, caída SMTP, fuga de denuncias.")
add_text(s, 0.55, 5.60, 12.2, 0.8, [
    [("Roles definidos (Encargado autoriza, informática ejecuta, admin_sistema apoya la recuperación técnica sin acceder a tickets).", S(11, False, MUTED))],
])
s.notes_slide.notes_text_frame.text = "Criterio 2.1.5.14: continuidad proactiva y reactiva con RPO/RTO."

# ================================================================ 20 · 2.1.5.15
s = new_slide()
header(s, "CRITERIO 2.1.5.15 · ENTREGABLE 15", "Plan de mantención: configuración, cambios e incidentes", 20)
card(s, 0.55, 1.35, 3.95, 3.9, "Gestión de configuración", [
    "Inventario de CI: código, BD, APP/DB/NAS, SMTP, /reportar, SGSI_*.",
    "Línea base versionada en Git.",
    "Auditoría contra la línea base.",
])
card(s, 4.62, 1.35, 4.15, 3.9, "Gestión de cambios", [
    "Tipos: estándar, normal, mayor, emergencia.",
    "Flujo: solicitud → evaluación → aprobación → implementación → prueba → cierre.",
    "Cambio Mayor 21-10-2026 (Usuarios + Ticketera).",
])
card(s, 8.89, 1.35, 3.89, 3.9, "Gestión de incidentes", [
    "Del propio SGSI (no la ticketera de negocio).",
    "Detección → clasificación → diagnóstico → resolución → verificación → cierre.",
    "Prioridades = SLA (30 min / 1 h / 4 h / 8 h).",
], size=10.5)
note(s, 5.45, "Los entregables (código, diagramas, documentación) se gestionan como cambios: cada modificación se registra y revisa en Git.")
add_text(s, 0.55, 6.00, 12.2, 0.7, [
    [("Distinción de alcance: la ticketera es un módulo de negocio; los incidentes operativos del SGSI se gestionan por el proceso de soporte.", S(11, False, MUTED))],
])
s.notes_slide.notes_text_frame.text = "Criterio 2.1.5.15: configuración, cambios e incidentes del servicio."

# ================================================================ 21 · 2.1.6.16
s = new_slide()
header(s, "CRITERIO 2.1.6.16 · ENTREGABLE 16", "Planificación: detalle de fases (Scrum) y carta Gantt", 21)
table(s, 0.55, 1.35, 7.0, [
    ["Fase", "Duración", "Hito / entregable"],
    ["F1 Formulación y requisitos", "2 sem", "Avance EF2 (09-10)"],
    ["F2 Diseño", "2 sem", "BPMN/UML/datos/arquitectura"],
    ["F3 Sprint Usuarios", "2 sem", "Módulo Usuarios (06-11)"],
    ["F4 Sprint Ticketera", "2 sem", "Módulo Ticketera (20-11)"],
    ["F5 Pruebas", "4 sem", "UAT (04-12)"],
    ["F6 Documentación ES2", "2 sem", "Entregables 9–15"],
    ["F7 Cierre y presentación", "1 sem", "ES2 (11-12)"],
], [2.9, 1.4, 2.7], font_size=10.5, row_h=0.42)
add_text(s, 7.85, 1.35, 4.9, 0.4, [[("Hitos de entrega", S(12.5, True, NAVY))]])
hitos = [
    ("09-10", "Avance formativo EF2"),
    ("21-10", "Cambio Mayor aprobado (Usuarios + Ticketera)"),
    ("06-11", "Módulo Usuarios integrado"),
    ("20-11", "Módulo Ticketera integrado"),
    ("04-12", "Validación UAT"),
    ("11-12", "Entrega sumativa ES2"),
]
for i, (f, h) in enumerate(hitos):
    y = 1.82 + i * 0.60
    rect(s, 7.85, y + 0.05, 0.62, 0.5, CRIMSON, None, MSO_SHAPE.ROUNDED_RECTANGLE, 0.12)
    add_text(s, 7.85, y + 0.10, 0.62, 0.4, [[(f, S(10.5, True, WHITE))]], align=PP_ALIGN.CENTER)
    add_text(s, 8.60, y + 0.02, 4.15, 0.6, [[(h, S(11, False, TEXT))]])
note(s, 5.75, "Metodología ágil: detalle de fases/sprints + carta Gantt de referencia · revisión y re-priorización por sprint.")
s.notes_slide.notes_text_frame.text = "Criterio 2.1.6.16: planificación por sprints con hitos verificables."

# ================================================================ 22 · 2.1.6.17
s = new_slide()
header(s, "CRITERIO 2.1.6.17 · ENTREGABLE 17", "Justificación de la adecuación del cronograma", 22)
card(s, 0.55, 1.35, 3.95, 3.9, "Coherencia con la solución", [
    "Cada fase habilita la funcionalidad.",
    "F1 alcance + cambio Mayor.",
    "F2 actualiza BPMN/UML/datos/arquitectura.",
    "F3 Usuarios (prerrequisito) → F4 Ticketera.",
    "F5 prueba CP-20 a CP-38, anonimato, adjuntos.",
], title_color=BLUE)
card(s, 4.62, 1.35, 3.95, 3.9, "Duración y holgura", [
    "11 semanas, alineadas a EF2/ES2 (11-12-2026).",
    "Dos sprints en orden: Usuarios → Ticketera.",
    "Solapamiento pruebas/documentación.",
    "Holgura protege la fecha ES2.",
], title_color=BLUE)
card(s, 8.69, 1.35, 4.09, 3.9, "Adecuación al problema", [
    "Núcleo GRC priorizado (controles, madurez, incidentes).",
    "Ticketera anónima + derivación a incidente legal.",
    "Canal público disponible y protegido.",
    "Sin omitir anonimato, SMTP ni validación.",
], title_color=BLUE)
note(s, 5.45, "El cronograma absorbió el cambio Mayor del 21-10-2026 sin mover el hito ES2 del 11-12-2026.")
add_text(s, 0.55, 6.00, 12.2, 0.8, [
    [("Trabajos futuros (fuera de alcance): SSO/LDAP, integración con mesa de ayuda, cifrado de adjuntos, integración ANCI por API, alta disponibilidad multi-sitio, firma electrónica.", S(11, False, MUTED))],
])
s.notes_slide.notes_text_frame.text = "Criterio 2.1.6.17: justificación de coherencia, duración y adecuación del cronograma."

# ================================================================ 23 · ESTADO ACTUAL
s = new_slide()
header(s, "RESULTADOS", "Estado actual: producto construido y probado", 23)
metric(s, 0.55, 1.45, 3.95, 2.6, "12", "grupos de endpoints", "API REST FastAPI con autenticación JWT y RBAC.", CRIMSON)
metric(s, 4.62, 1.45, 3.95, 2.6, "39", "pruebas automatizadas", "Casos funcionales y de seguridad con datos de prueba.", CRIMSON)
metric(s, 8.69, 1.45, 4.09, 2.6, "9", "módulos en la SPA", "Dashboard y flujos completos en React.", CRIMSON)
card(s, 0.55, 4.35, 12.23, 1.75, "Ya está operativo", [
    "Catálogo de controles ISO/IEC 27001 precargado · cinco roles activos · formulario público anónimo · bandeja confidencial.",
    "Notificaciones (correo/bandeja) y conversión de denuncia a incidente formal · importación masiva de incidentes por CSV.",
    "El prototipo funcional respalda la defensa: la solución está construida y probada.",
])
s.notes_slide.notes_text_frame.text = "Resultados: cifras concretas (12 grupos de endpoints, 39 pruebas, 9 módulos)."

# ================================================================ 24 · CONCLUSIONES
s = new_slide()
header(s, "CONCLUSIONES", "Síntesis y trabajos futuros", 24)
card(s, 0.55, 1.35, 6.0, 3.9, "Conclusiones", [
    "Cumple el objetivo: registrar, medir y visualizar la madurez del SGSI y gestionar incidentes conforme a la Ley 21.663.",
    "Stack (FastAPI + React + PostgreSQL) viable técnica, económica e implementativamente.",
    "De planillas dispersas a gobierno auditable: medir, reaccionar y demostrar.",
], title_color=GREEN)
card(s, 6.68, 1.35, 6.1, 3.9, "Trabajos futuros (fuera del alcance)", [
    "SSO/LDAP para ciclo de vida de usuarios.",
    "Integración de tickets con mesa de ayuda.",
    "Cifrado de adjuntos en reposo + antivirus.",
    "Integración ANCI por API (cuando exista).",
    "Alta disponibilidad multi-sitio y monitoreo.",
    "Firma electrónica en auditoría de cambios.",
], title_color=GOLD)
note(s, 5.45, "La solución alinea problema, producto y proceso, y ya está construida.")
s.notes_slide.notes_text_frame.text = "Conclusiones: objetivo cumplido, viabilidad del stack y próximos pasos."

# ================================================================ 25 · CIERRE
s = new_slide()
rect(s, 0, 0, SW, SH, NAVY)
rect(s, 0, 0, SW, 0.14, CRIMSON)
rect(s, 0, SH - 0.14, SW, 0.14, CRIMSON)
add_text(s, 1.2, 2.0, 11.0, 0.5, [[("GRACIAS", S(20, True, SKY))]])
add_text(s, 1.2, 2.7, 11.0, 1.6, [
    [("SGSI — De planillas dispersas a gobierno auditable", S(36, True, WHITE))],
])
add_text(s, 1.2, 4.35, 11.0, 1.4, [
    [("Medir  ·  Reaccionar  ·  Demostrar", S(20, False, SKY))],
])
add_text(s, 1.2, 5.75, 11.0, 1.0, [
    [("Priscila Bahamóndez  ·  Proyecto de Título TIHI84  ·  INACAP", S(14, False, WHITE))],
    [("Hospital Félix Bulnes Cerda  ·  Noviembre 2026", S(12, False, SKY))],
])
s.notes_slide.notes_text_frame.text = "Cierre: terminar con la frase de valor e invitar a preguntas."

# ---------------------------------------------------------------- guardar
prs.core_properties.title = "SGSI — Evaluación Sumativa 2 (ES2) · Unidad 2"
prs.core_properties.author = "Priscila Bahamóndez"
prs.core_properties.subject = "Presentación alineada a la rúbrica ES2 (17 criterios)"
prs.core_properties.comments = "Generada con python-pptx desde los entregables U2 y el mockup del sistema."

prs.save(OUT)
print("Guardado:", OUT)
print("Diapositivas:", len(prs.slides._sldIdLst))
