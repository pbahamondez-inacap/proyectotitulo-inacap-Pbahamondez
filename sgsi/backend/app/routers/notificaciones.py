"""Bandeja interna de notificaciones de tickets (solo encargado)."""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload

from ..database import get_db
from ..deps import require_roles
from ..models import MedioNotificacion, Notificacion, Role
from ..schemas import NotificacionOut

router = APIRouter(prefix="/notificaciones", tags=["notificaciones"])

_encargado = require_roles(Role.encargado)


def _to_out(n: Notificacion) -> NotificacionOut:
    return NotificacionOut(
        id=n.id,
        ticket_id=n.ticket_id,
        ticket_codigo=n.ticket.codigo,
        tipo_ticket=n.ticket.tipo,
        severidad=n.ticket.severidad_percibida,
        medio=n.medio,
        leida=bool(n.leida),
        creado_en=n.creado_en,
    )


def _bandeja(db: Session, user):
    return db.query(Notificacion).filter(
        Notificacion.destinatario_id == user.id,
        Notificacion.medio == MedioNotificacion.bandeja,
    )


@router.get("", response_model=list[NotificacionOut])
def list_notificaciones(
    solo_no_leidas: bool = Query(default=False),
    db: Session = Depends(get_db),
    user=Depends(_encargado),
):
    q = _bandeja(db, user).options(joinedload(Notificacion.ticket))
    if solo_no_leidas:
        q = q.filter(Notificacion.leida.is_(False))
    return [_to_out(n) for n in q.order_by(Notificacion.creado_en.desc(), Notificacion.id.desc()).all()]


@router.get("/pendientes/count")
def count_pendientes(db: Session = Depends(get_db), user=Depends(_encargado)):
    return {"count": _bandeja(db, user).filter(Notificacion.leida.is_(False)).count()}


@router.post("/{notificacion_id}/leer", response_model=NotificacionOut)
def marcar_leida(notificacion_id: int, db: Session = Depends(get_db), user=Depends(_encargado)):
    notificacion = _bandeja(db, user).filter(Notificacion.id == notificacion_id).first()
    if not notificacion:
        raise HTTPException(status_code=404, detail="Notificación no encontrada")
    notificacion.leida = True
    db.commit()
    db.refresh(notificacion)
    return _to_out(notificacion)
