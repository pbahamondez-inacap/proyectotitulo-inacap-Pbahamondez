"""Formulario público de tickets (sin autenticación, anónimo por diseño).

Anonimato: estos endpoints no leen el token de autorización, no persisten ni registran la IP,
el user-agent ni las cabeceras del emisor, y no escriben el contenido del ticket en logs.
Los errores son genéricos.
"""
import secrets
from datetime import datetime
from typing import List, Optional

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    File,
    Form,
    HTTPException,
    UploadFile,
)
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import CategoriaTicket, EstadoTicket, Severidad, Ticket, TipoTicket
from ..notificaciones import crear_notificaciones, enviar_correo_ticket
from ..ratelimit import limit_ticket_creation, limit_ticket_lookup
from ..schemas import TicketPublicCreated, TicketPublicEstado
from ..tickets_service import (
    catalogo_publico,
    crear_ticket,
    eliminar_carpeta_ticket,
    guardar_adjuntos,
    validar_archivos,
)
from ..utils import now_naive, to_naive

router = APIRouter(prefix="/public/tickets", tags=["tickets-publicos"])

MENSAJE_OK = (
    "Su reporte fue registrado. Guarde el código de seguimiento para consultar su estado; "
    "no se almacena información que lo identifique."
)
DESCRIPCION_MIN = 20
DESCRIPCION_MAX = 5000


@router.get("/categorias")
def get_catalogo():
    return catalogo_publico()


@router.post(
    "",
    response_model=TicketPublicCreated,
    status_code=201,
    dependencies=[Depends(limit_ticket_creation)],
)
async def crear_ticket_publico(
    background_tasks: BackgroundTasks,
    tipo: TipoTicket = Form(...),
    categoria: CategoriaTicket = Form(...),
    descripcion: str = Form(...),
    severidad_percibida: Severidad = Form(...),
    categoria_otro: Optional[str] = Form(default=None),
    sistema_area: Optional[str] = Form(default=None),
    fecha_hecho_aprox: Optional[str] = Form(default=None),
    notificar_correo: bool = Form(default=False),
    notificar_bandeja: bool = Form(default=True),
    website: Optional[str] = Form(default=None),  # honeypot: los humanos no lo ven ni lo completan
    archivos: List[UploadFile] = File(default=[]),
    db: Session = Depends(get_db),
):
    if website:
        # Bot: respuesta simulada sin guardar nada
        return TicketPublicCreated(
            codigo=f"TCK-{now_naive().year}-{secrets.randbelow(99999) + 1:05d}",
            codigo_seguimiento=secrets.token_urlsafe(9),
            estado=EstadoTicket.registrado,
            mensaje=MENSAJE_OK,
        )

    descripcion = descripcion.strip()
    if len(descripcion) < DESCRIPCION_MIN or len(descripcion) > DESCRIPCION_MAX:
        raise HTTPException(
            status_code=422,
            detail=f"La descripción debe tener entre {DESCRIPCION_MIN} y {DESCRIPCION_MAX} caracteres",
        )
    categoria_otro = (categoria_otro or "").strip()
    if categoria == CategoriaTicket.otros:
        if not categoria_otro:
            raise HTTPException(status_code=422, detail="Debe especificar la categoría cuando elige 'Otros'")
    else:
        categoria_otro = ""
    if len(categoria_otro) > 200 or len((sistema_area or "").strip()) > 200:
        raise HTTPException(status_code=422, detail="Un campo de texto excede el largo permitido")
    if not (notificar_correo or notificar_bandeja):
        raise HTTPException(status_code=422, detail="Debe seleccionar al menos un medio de notificación")

    fecha = None
    if fecha_hecho_aprox and fecha_hecho_aprox.strip():
        try:
            fecha = to_naive(datetime.fromisoformat(fecha_hecho_aprox.strip()))
        except ValueError:
            raise HTTPException(status_code=422, detail="Fecha inválida (use formato ISO 8601)")

    validados = await validar_archivos(archivos)

    ticket = crear_ticket(
        db,
        canal_origen="publico",
        tipo=tipo,
        categoria=categoria,
        categoria_otro=categoria_otro or None,
        descripcion=descripcion,
        sistema_area=(sistema_area or "").strip(),
        fecha_hecho_aprox=fecha,
        severidad_percibida=severidad_percibida,
        notificar_correo=notificar_correo,
        notificar_bandeja=notificar_bandeja,
    )
    try:
        guardar_adjuntos(db, ticket, validados)
        correo = crear_notificaciones(db, ticket)
        db.commit()
    except Exception:
        db.rollback()
        eliminar_carpeta_ticket(ticket.codigo)
        raise HTTPException(status_code=500, detail="No fue posible registrar el reporte")
    db.refresh(ticket)

    if correo is not None:
        background_tasks.add_task(enviar_correo_ticket, correo.id)

    return TicketPublicCreated(
        codigo=ticket.codigo,
        codigo_seguimiento=ticket.codigo_seguimiento,
        estado=ticket.estado,
        mensaje=MENSAJE_OK,
    )


@router.get(
    "/{codigo_seguimiento}",
    response_model=TicketPublicEstado,
    dependencies=[Depends(limit_ticket_lookup)],
)
def consultar_estado(codigo_seguimiento: str, db: Session = Depends(get_db)):
    ticket = db.query(Ticket).filter(Ticket.codigo_seguimiento == codigo_seguimiento).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Código de seguimiento no encontrado")
    return ticket
