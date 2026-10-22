"""Servicio de notificaciones al equipo de ciberseguridad (bandeja interna y correo SMTP).

El correo solo incluye código, tipo, severidad y enlace a la bandeja: nunca el contenido
del ticket. Un fallo de SMTP no afecta la creación del ticket.
"""
import logging
import smtplib
from email.message import EmailMessage

from sqlalchemy.orm import Session

from . import config
from .database import SessionLocal
from .models import MedioNotificacion, Notificacion, Role, Ticket, Usuario
from .utils import now_naive

logger = logging.getLogger("sgsi.notificaciones")

SMTP_ATTEMPTS = 2


def crear_notificaciones(db: Session, ticket: Ticket) -> Notificacion | None:
    """Crea (sin commit) las notificaciones de bandeja y el registro de correo del ticket.

    Devuelve el registro de correo (para enviarlo en segundo plano) o None.
    """
    if ticket.notificar_bandeja:
        encargados = (
            db.query(Usuario).filter(Usuario.rol == Role.encargado, Usuario.activo.is_(True)).all()
        )
        for encargado in encargados:
            db.add(
                Notificacion(
                    ticket_id=ticket.id,
                    destinatario_id=encargado.id,
                    medio=MedioNotificacion.bandeja,
                    estado_envio="enviado",
                    enviada_en=now_naive(),
                )
            )
    correo = None
    if ticket.notificar_correo:
        correo = Notificacion(
            ticket_id=ticket.id, medio=MedioNotificacion.correo, estado_envio="pendiente"
        )
        db.add(correo)
    return correo


def _build_message(ticket: Ticket, destinatarios: list[str]) -> EmailMessage:
    msg = EmailMessage()
    msg["Subject"] = f"[SGSI] Nuevo ticket {ticket.codigo}"
    msg["From"] = config.SMTP_FROM
    msg["To"] = ", ".join(destinatarios)
    msg.set_content(
        "Se registró un nuevo ticket en el SGSI.\n\n"
        f"Código: {ticket.codigo}\n"
        f"Tipo: {ticket.tipo.value}\n"
        f"Severidad percibida: {ticket.severidad_percibida.value}\n\n"
        f"Revise la bandeja de tickets: {config.APP_URL}/tickets\n"
    )
    return msg


def _send_smtp(msg: EmailMessage) -> None:
    if config.SMTP_PORT == 465:
        server = smtplib.SMTP_SSL(config.SMTP_HOST, config.SMTP_PORT, timeout=10)
    else:
        server = smtplib.SMTP(config.SMTP_HOST, config.SMTP_PORT, timeout=10)
    with server:
        if config.SMTP_PORT != 465 and config.SMTP_STARTTLS:
            server.starttls()
        if config.SMTP_USER:
            server.login(config.SMTP_USER, config.SMTP_PASSWORD)
        server.send_message(msg)


def enviar_correo_ticket(notificacion_id: int) -> None:
    """Tarea en segundo plano: envía (o simula) el correo y actualiza el estado de envío."""
    db = SessionLocal()
    try:
        notificacion = db.get(Notificacion, notificacion_id)
        if notificacion is None:
            return
        ticket = db.get(Ticket, notificacion.ticket_id)
        destinatarios = config.SMTP_TO
        if not config.SMTP_HOST or not destinatarios:
            logger.info("Correo simulado para el ticket %s (SMTP no configurado)", ticket.codigo)
            notificacion.estado_envio = "simulado"
        else:
            estado = "error"
            for intento in range(1, SMTP_ATTEMPTS + 1):
                try:
                    _send_smtp(_build_message(ticket, destinatarios))
                    estado = "enviado"
                    break
                except Exception as exc:  # el fallo SMTP nunca debe afectar al ticket
                    logger.warning(
                        "Fallo al enviar correo del ticket %s (intento %s): %s",
                        ticket.codigo, intento, type(exc).__name__,
                    )
            notificacion.estado_envio = estado
        notificacion.enviada_en = now_naive()
        db.commit()
    except Exception:
        logger.exception("Error inesperado al procesar el correo de notificación")
    finally:
        db.close()
