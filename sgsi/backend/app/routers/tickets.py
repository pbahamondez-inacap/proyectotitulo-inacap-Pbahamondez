"""Bandeja interna de tickets (denuncias y reportes): solo el encargado de ciberseguridad."""
from fastapi import APIRouter, Body, Depends, HTTPException, Query
from fastapi.responses import FileResponse
from sqlalchemy import or_
from sqlalchemy.orm import Session, selectinload

from ..database import get_db
from ..deps import require_roles
from ..models import EstadoTicket, Role, Severidad, Ticket, TicketAdjunto, TipoTicket
from ..schemas import (
    IncidenteOut,
    TicketConvertir,
    TicketDetalle,
    TicketEstadoUpdate,
    TicketOut,
    TicketResumen,
)
from ..services import incidente_to_dict
from ..tickets_service import (
    ESTADOS_PENDIENTES,
    TRANSICIONES,
    convertir_a_incidente,
    ruta_adjunto,
)

router = APIRouter(
    prefix="/tickets",
    tags=["tickets"],
    dependencies=[Depends(require_roles(Role.encargado))],
)


def _get_ticket(ticket_id: int, db: Session) -> Ticket:
    ticket = (
        db.query(Ticket)
        .options(selectinload(Ticket.adjuntos))
        .filter(Ticket.id == ticket_id)
        .first()
    )
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")
    return ticket


@router.get("", response_model=list[TicketOut])
def list_tickets(
    estado: EstadoTicket | None = Query(default=None),
    tipo: TipoTicket | None = Query(default=None),
    severidad: Severidad | None = Query(default=None),
    q: str | None = Query(default=None),
    db: Session = Depends(get_db),
):
    query = db.query(Ticket)
    if estado:
        query = query.filter(Ticket.estado == estado)
    if tipo:
        query = query.filter(Ticket.tipo == tipo)
    if severidad:
        query = query.filter(Ticket.severidad_percibida == severidad)
    if q:
        like = f"%{q}%"
        query = query.filter(
            or_(
                Ticket.codigo.ilike(like),
                Ticket.descripcion.ilike(like),
                Ticket.sistema_area.ilike(like),
                Ticket.categoria_otro.ilike(like),
            )
        )
    return query.order_by(Ticket.creado_en.desc(), Ticket.id.desc()).all()


# Declarada antes de /{ticket_id}
@router.get("/resumen", response_model=TicketResumen)
def resumen(db: Session = Depends(get_db)):
    conteo = {e: 0 for e in EstadoTicket}
    for ticket_estado, in db.query(Ticket.estado).all():
        conteo[ticket_estado] += 1
    return TicketResumen(
        registrado=conteo[EstadoTicket.registrado],
        en_analisis=conteo[EstadoTicket.en_analisis],
        derivado_a_incidente=conteo[EstadoTicket.derivado_a_incidente],
        cerrado=conteo[EstadoTicket.cerrado],
        pendientes=sum(conteo[e] for e in ESTADOS_PENDIENTES),
    )


@router.get("/{ticket_id}", response_model=TicketDetalle)
def get_ticket(ticket_id: int, db: Session = Depends(get_db)):
    return _get_ticket(ticket_id, db)


@router.patch("/{ticket_id}/estado", response_model=TicketDetalle)
def cambiar_estado(ticket_id: int, data: TicketEstadoUpdate, db: Session = Depends(get_db)):
    ticket = _get_ticket(ticket_id, db)
    if data.estado == EstadoTicket.derivado_a_incidente:
        raise HTTPException(
            status_code=400, detail="Para derivar a incidente use la conversión a incidente"
        )
    if data.estado not in TRANSICIONES[ticket.estado]:
        raise HTTPException(
            status_code=400,
            detail=f"Transición inválida: {ticket.estado.value} -> {data.estado.value}",
        )
    ticket.estado = data.estado
    if data.notas_internas is not None:
        ticket.notas_internas = data.notas_internas
    db.commit()
    db.refresh(ticket)
    return ticket


@router.post("/{ticket_id}/convertir-incidente", response_model=IncidenteOut, status_code=201)
def convertir_incidente(
    ticket_id: int,
    data: TicketConvertir | None = Body(default=None),
    db: Session = Depends(get_db),
):
    ticket = _get_ticket(ticket_id, db)
    incidente = convertir_a_incidente(db, ticket, data or TicketConvertir())
    db.commit()
    db.refresh(incidente)
    return IncidenteOut(**incidente_to_dict(incidente))


@router.get("/{ticket_id}/adjuntos/{adjunto_id}")
def descargar_adjunto(ticket_id: int, adjunto_id: int, db: Session = Depends(get_db)):
    adjunto = (
        db.query(TicketAdjunto)
        .filter(TicketAdjunto.id == adjunto_id, TicketAdjunto.ticket_id == ticket_id)
        .first()
    )
    ruta = ruta_adjunto(adjunto) if adjunto else None
    if ruta is None:
        raise HTTPException(status_code=404, detail="Adjunto no encontrado")
    return FileResponse(
        ruta,
        filename=adjunto.nombre_archivo,
        media_type=adjunto.mime,
        headers={"X-Content-Type-Options": "nosniff"},
    )
