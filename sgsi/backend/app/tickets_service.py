"""Lógica de negocio de la ticketera: catálogos, códigos, adjuntos, transiciones y conversión a incidente."""
import mimetypes
import secrets
import shutil
import uuid
from pathlib import Path

from fastapi import HTTPException, UploadFile
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .config import (
    TICKET_ALLOWED_EXTENSIONS,
    TICKET_MAX_FILE_BYTES,
    TICKET_MAX_FILES,
    TICKET_UPLOAD_DIR,
)
from .models import (
    CategoriaTicket,
    EstadoIncidente,
    EstadoTicket,
    Incidente,
    MedioNotificacion,
    Severidad,
    Ticket,
    TicketAdjunto,
    TipoTicket,
)
from .schemas import TicketConvertir
from .utils import now_naive

TIPO_LABELS = {
    TipoTicket.denuncia: "Denuncia",
    TipoTicket.reporte_incidente: "Reporte de incidente de ciberseguridad",
}

CATEGORIA_LABELS = {
    CategoriaTicket.phishing: "Phishing / correo sospechoso",
    CategoriaTicket.malware_ransomware: "Malware / Ransomware",
    CategoriaTicket.acceso_no_autorizado: "Acceso no autorizado",
    CategoriaTicket.fuga_de_informacion: "Fuga de información",
    CategoriaTicket.uso_indebido_de_datos: "Uso indebido de datos",
    CategoriaTicket.falla_o_caida_de_servicio: "Falla o caída de servicio",
    CategoriaTicket.perdida_robo_de_equipo: "Pérdida o robo de equipo",
    CategoriaTicket.incumplimiento_de_politicas: "Incumplimiento de políticas",
    CategoriaTicket.otros: "Otros (especificar)",
}

SEVERIDAD_LABELS = {
    Severidad.baja: "Baja",
    Severidad.media: "Media",
    Severidad.alta: "Alta",
    Severidad.critica: "Crítica",
}

MEDIO_LABELS = {
    MedioNotificacion.bandeja: "Bandeja interna de tickets pendientes",
    MedioNotificacion.correo: "Correo electrónico",
}

# Transiciones manuales; derivado_a_incidente solo se alcanza al convertir el ticket.
TRANSICIONES = {
    EstadoTicket.registrado: {EstadoTicket.en_analisis},
    EstadoTicket.en_analisis: {EstadoTicket.cerrado},
    EstadoTicket.derivado_a_incidente: {EstadoTicket.cerrado},
    EstadoTicket.cerrado: set(),
}

ESTADOS_PENDIENTES = (EstadoTicket.registrado, EstadoTicket.en_analisis)


def catalogo_publico() -> dict:
    return {
        "tipos": [{"value": t.value, "label": TIPO_LABELS[t]} for t in TipoTicket],
        "categorias": [{"value": c.value, "label": CATEGORIA_LABELS[c]} for c in CategoriaTicket],
        "severidades": [{"value": s.value, "label": SEVERIDAD_LABELS[s]} for s in Severidad],
        "medios": [{"value": m.value, "label": MEDIO_LABELS[m]} for m in MedioNotificacion],
    }


def categoria_texto(ticket: Ticket) -> str:
    if ticket.categoria == CategoriaTicket.otros and ticket.categoria_otro:
        return ticket.categoria_otro
    return CATEGORIA_LABELS[ticket.categoria]


# ---------- Adjuntos ----------
class ArchivoValidado:
    def __init__(self, nombre: str, extension: str, contenido: bytes):
        self.nombre = nombre
        self.extension = extension
        self.contenido = contenido
        self.mime = mimetypes.guess_type(f"x{extension}")[0] or "application/octet-stream"


async def validar_archivos(archivos: list[UploadFile]) -> list[ArchivoValidado]:
    """Valida cantidad, extensión (lista blanca) y tamaño antes de guardar cualquier cosa."""
    archivos = [a for a in archivos if a is not None and a.filename]
    if len(archivos) > TICKET_MAX_FILES:
        raise HTTPException(status_code=413, detail=f"Máximo {TICKET_MAX_FILES} archivos por ticket")
    validados: list[ArchivoValidado] = []
    for archivo in archivos:
        nombre = Path(archivo.filename.replace("\\", "/")).name[:200]
        extension = Path(nombre).suffix.lower()
        if extension not in TICKET_ALLOWED_EXTENSIONS:
            raise HTTPException(status_code=415, detail="Tipo de archivo no permitido")
        contenido = await archivo.read(TICKET_MAX_FILE_BYTES + 1)
        if len(contenido) > TICKET_MAX_FILE_BYTES:
            raise HTTPException(status_code=413, detail="El archivo supera el tamaño máximo de 10 MB")
        validados.append(ArchivoValidado(nombre, extension, contenido))
    return validados


def guardar_adjuntos(db: Session, ticket: Ticket, archivos: list[ArchivoValidado]) -> None:
    """Guarda los archivos con nombre aleatorio en <upload>/tickets/<codigo>/ y registra sus metadatos."""
    if not archivos:
        return
    carpeta = TICKET_UPLOAD_DIR / ticket.codigo
    carpeta.mkdir(parents=True, exist_ok=True)
    for archivo in archivos:
        almacenado = f"{uuid.uuid4().hex}{archivo.extension}"
        (carpeta / almacenado).write_bytes(archivo.contenido)
        db.add(
            TicketAdjunto(
                ticket_id=ticket.id,
                nombre_archivo=archivo.nombre,
                ruta=f"{ticket.codigo}/{almacenado}",
                mime=archivo.mime,
                tamano_bytes=len(archivo.contenido),
            )
        )


def eliminar_carpeta_ticket(codigo: str) -> None:
    shutil.rmtree(TICKET_UPLOAD_DIR / codigo, ignore_errors=True)


def ruta_adjunto(adjunto: TicketAdjunto) -> Path | None:
    """Resuelve la ruta física del adjunto evitando salir de la carpeta de tickets."""
    base = TICKET_UPLOAD_DIR.resolve()
    ruta = (TICKET_UPLOAD_DIR / adjunto.ruta).resolve()
    if base not in ruta.parents or not ruta.is_file():
        return None
    return ruta


# ---------- Creación ----------
def crear_ticket(db: Session, canal_origen: str = "publico", **campos) -> Ticket:
    """Crea el ticket con código TCK-<año>-<00001> y token de seguimiento aleatorio (hace flush, no commit)."""
    anio = now_naive().year
    prefijo = f"TCK-{anio}-"
    for _ in range(5):
        ultimo = (
            db.query(Ticket.codigo)
            .filter(Ticket.codigo.like(f"{prefijo}%"))
            .order_by(Ticket.codigo.desc())
            .first()
        )
        siguiente = int(ultimo[0].rsplit("-", 1)[1]) + 1 if ultimo else 1
        ticket = Ticket(
            codigo=f"{prefijo}{siguiente:05d}",
            codigo_seguimiento=secrets.token_urlsafe(9),
            canal_origen=canal_origen,
            **campos,
        )
        db.add(ticket)
        try:
            db.flush()
            return ticket
        except IntegrityError:
            db.rollback()  # código ocupado por una solicitud concurrente: reintentar
    raise HTTPException(status_code=500, detail="No fue posible registrar el ticket")


# ---------- Conversión a incidente ----------
def convertir_a_incidente(db: Session, ticket: Ticket, data: TicketConvertir) -> Incidente:
    if ticket.incidente_id is not None:
        raise HTTPException(status_code=409, detail="El ticket ya fue convertido en incidente")
    if ticket.estado not in (EstadoTicket.registrado, EstadoTicket.en_analisis):
        raise HTTPException(status_code=400, detail="El ticket cerrado no puede convertirse en incidente")

    categoria = categoria_texto(ticket)
    incidente = Incidente(
        titulo=f"Ticket {ticket.codigo}: {categoria}"[:250],
        descripcion=ticket.descripcion,
        categoria=data.categoria_anci or categoria,
        severidad=data.severidad or ticket.severidad_percibida,
        alcance=data.alcance or "interno",
        sistema_afectado=ticket.sistema_area or "",
        fecha_deteccion=ticket.fecha_hecho_aprox or now_naive(),
        estado=EstadoIncidente.registrado,
        notas=f"Origen: ticket {ticket.codigo}",
    )
    db.add(incidente)
    db.flush()
    ticket.incidente_id = incidente.id
    ticket.estado = EstadoTicket.derivado_a_incidente
    return incidente
