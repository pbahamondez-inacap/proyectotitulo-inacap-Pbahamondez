"""Modelos ORM del SGSI (SQLAlchemy)."""
import enum

from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    DateTime,
    Enum as SAEnum,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from .database import Base
from .utils import now_naive


class Role(str, enum.Enum):
    encargado = "encargado"
    admin_contratos = "admin_contratos"
    referente_tecnico = "referente_tecnico"
    director = "director"
    admin_sistema = "admin_sistema"


class Dominio(str, enum.Enum):
    organizacional = "organizacional"
    personas = "personas"
    fisico = "fisico"
    tecnologico = "tecnologico"


class EstadoControl(str, enum.Enum):
    no_iniciado = "no_iniciado"
    iniciado = "iniciado"
    implementado = "implementado"
    gestionado = "gestionado"


class Severidad(str, enum.Enum):
    baja = "baja"
    media = "media"
    alta = "alta"
    critica = "critica"


class EstadoIncidente(str, enum.Enum):
    registrado = "registrado"
    en_analisis = "en_analisis"
    contenido = "contenido"
    resuelto = "resuelto"
    reportado = "reportado"
    cerrado = "cerrado"


class EstadoCumplimiento(str, enum.Enum):
    pendiente = "pendiente"
    parcial = "parcial"
    cumple = "cumple"
    no_cumple = "no_cumple"


class TipoPersonaControl(str, enum.Enum):
    capacitacion = "capacitacion"
    antecedentes = "antecedentes"
    condiciones_empleo = "condiciones_empleo"
    disciplinario = "disciplinario"
    termino_contrato = "termino_contrato"
    confidencialidad = "confidencialidad"


class TipoTicket(str, enum.Enum):
    denuncia = "denuncia"
    reporte_incidente = "reporte_incidente"


class CategoriaTicket(str, enum.Enum):
    phishing = "phishing"
    malware_ransomware = "malware_ransomware"
    acceso_no_autorizado = "acceso_no_autorizado"
    fuga_de_informacion = "fuga_de_informacion"
    uso_indebido_de_datos = "uso_indebido_de_datos"
    falla_o_caida_de_servicio = "falla_o_caida_de_servicio"
    perdida_robo_de_equipo = "perdida_robo_de_equipo"
    incumplimiento_de_politicas = "incumplimiento_de_politicas"
    otros = "otros"


class EstadoTicket(str, enum.Enum):
    registrado = "registrado"
    en_analisis = "en_analisis"
    derivado_a_incidente = "derivado_a_incidente"
    cerrado = "cerrado"


class MedioNotificacion(str, enum.Enum):
    bandeja = "bandeja"
    correo = "correo"


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    nombre_completo = Column(String, nullable=False)
    rol = Column(SAEnum(Role), nullable=False)
    activo = Column(Boolean, default=True)


class Control(Base):
    __tablename__ = "controles"

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String, index=True)  # ej. "A.5.1"
    titulo = Column(String, nullable=False)
    descripcion = Column(Text, default="")
    dominio = Column(SAEnum(Dominio), nullable=False, index=True)
    grupo = Column(String, default="")  # ej. "5 Políticas de seguridad de la información"
    estado = Column(SAEnum(EstadoControl), default=EstadoControl.no_iniciado, index=True)
    responsable = Column(String, default="")
    notas = Column(Text, default="")
    fecha_actualizacion = Column(DateTime, default=now_naive, onupdate=now_naive)

    evidencias = relationship(
        "Evidencia", back_populates="control", cascade="all, delete-orphan"
    )


class Evidencia(Base):
    __tablename__ = "evidencias"

    id = Column(Integer, primary_key=True, index=True)
    control_id = Column(Integer, ForeignKey("controles.id"), nullable=False)
    tipo = Column(String, default="documento")
    nombre = Column(String, nullable=False)
    descripcion = Column(Text, default="")
    archivo_path = Column(String, nullable=True)
    fecha_subida = Column(DateTime, default=now_naive)

    control = relationship("Control", back_populates="evidencias")


class Incidente(Base):
    __tablename__ = "incidentes"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    descripcion = Column(Text, default="")
    categoria = Column(String, default="")  # taxonomía ANCI
    severidad = Column(SAEnum(Severidad), nullable=False, index=True)
    alcance = Column(String, default="interno")  # interno / externo / proveedor
    sistema_afectado = Column(String, default="")
    fecha_deteccion = Column(DateTime, default=now_naive)
    fecha_reporte = Column(DateTime, nullable=True)
    estado = Column(SAEnum(EstadoIncidente), default=EstadoIncidente.registrado, index=True)
    reportado_anci = Column(Boolean, default=False)
    notas = Column(Text, default="")


class Tercero(Base):
    __tablename__ = "terceros"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    rut = Column(String, default="")
    tipo = Column(String, default="proveedor_sistema")
    contrato_ref = Column(String, default="")
    fecha_inicio = Column(DateTime, nullable=True)
    fecha_termino = Column(DateTime, nullable=True)
    contacto = Column(String, default="")
    estado_cumplimiento = Column(
        SAEnum(EstadoCumplimiento), default=EstadoCumplimiento.pendiente
    )
    # Lista de cláusulas de seguridad: [{"nombre": str, "cumplida": bool}]
    clausulas = Column(JSON, default=list)
    notas = Column(Text, default="")


class PersonaControl(Base):
    __tablename__ = "persona_controles"

    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(SAEnum(TipoPersonaControl), nullable=False, index=True)
    titulo = Column(String, nullable=False)
    descripcion = Column(Text, default="")
    estado = Column(SAEnum(EstadoControl), default=EstadoControl.no_iniciado, index=True)
    fecha = Column(DateTime, nullable=True)
    responsable = Column(String, default="")
    notas = Column(Text, default="")


class AuditoriaUsuario(Base):
    """Bitácora de administración de usuarios (nunca contiene contraseñas)."""

    __tablename__ = "auditoria_usuarios"

    id = Column(Integer, primary_key=True, index=True)
    actor_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False, index=True)
    usuario_objetivo_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False, index=True)
    accion = Column(String, nullable=False, index=True)
    detalle = Column(Text, default="")
    creado_en = Column(DateTime, default=now_naive, index=True)

    actor = relationship("Usuario", foreign_keys=[actor_id])
    usuario_objetivo = relationship("Usuario", foreign_keys=[usuario_objetivo_id])


class Ticket(Base):
    """Denuncia o reporte de incidente. Anónimo por diseño: sin FK a usuarios ni datos del emisor."""

    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String, unique=True, index=True, nullable=False)  # TCK-2026-00001
    codigo_seguimiento = Column(String, unique=True, index=True, nullable=False)
    tipo = Column(SAEnum(TipoTicket), nullable=False, index=True)
    categoria = Column(SAEnum(CategoriaTicket), nullable=False)
    categoria_otro = Column(String, nullable=True)
    descripcion = Column(Text, nullable=False)
    sistema_area = Column(String, default="")
    fecha_hecho_aprox = Column(DateTime, nullable=True)
    severidad_percibida = Column(SAEnum(Severidad), nullable=False, index=True)
    estado = Column(SAEnum(EstadoTicket), default=EstadoTicket.registrado, index=True)
    notificar_correo = Column(Boolean, default=False)
    notificar_bandeja = Column(Boolean, default=True)
    canal_origen = Column(String, default="publico")  # publico / interno (sin identidad)
    incidente_id = Column(Integer, ForeignKey("incidentes.id"), nullable=True)
    creado_en = Column(DateTime, default=now_naive, index=True)
    actualizado_en = Column(DateTime, default=now_naive, onupdate=now_naive)
    notas_internas = Column(Text, default="")

    adjuntos = relationship(
        "TicketAdjunto", back_populates="ticket", cascade="all, delete-orphan"
    )


class TicketAdjunto(Base):
    __tablename__ = "ticket_adjuntos"

    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer, ForeignKey("tickets.id"), nullable=False, index=True)
    nombre_archivo = Column(String, nullable=False)
    ruta = Column(String, nullable=False)
    mime = Column(String, default="application/octet-stream")
    tamano_bytes = Column(Integer, default=0)
    creado_en = Column(DateTime, default=now_naive)

    ticket = relationship("Ticket", back_populates="adjuntos")


class Notificacion(Base):
    """Aviso al equipo de ciberseguridad: bandeja interna (por encargado) o correo (sin destinatario de usuario)."""

    __tablename__ = "notificaciones"

    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer, ForeignKey("tickets.id"), nullable=False, index=True)
    destinatario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True, index=True)
    medio = Column(SAEnum(MedioNotificacion), nullable=False)
    leida = Column(Boolean, default=False)
    creado_en = Column(DateTime, default=now_naive)
    enviada_en = Column(DateTime, nullable=True)
    estado_envio = Column(String, default="pendiente")  # pendiente / enviado / simulado / error

    ticket = relationship("Ticket")
