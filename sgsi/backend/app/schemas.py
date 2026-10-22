"""Esquemas Pydantic de entrada/salida de la API."""
from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

from .models import (
    CategoriaTicket,
    Dominio,
    EstadoControl,
    EstadoCumplimiento,
    EstadoIncidente,
    EstadoTicket,
    MedioNotificacion,
    Role,
    Severidad,
    TipoPersonaControl,
    TipoTicket,
)


# ---------- Autenticación ----------
class UsuarioOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    nombre_completo: str
    rol: Role
    activo: bool = True

    @field_validator("activo", mode="before")
    @classmethod
    def _activo_none_es_inactivo(cls, v):
        return bool(v)


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenOut(BaseModel):
    token: str
    user: UsuarioOut


# ---------- Usuarios (administración) ----------
USERNAME_PATTERN = r"^[A-Za-z0-9._@-]+$"


class UsuarioCreate(BaseModel):
    username: str = Field(min_length=3, max_length=64, pattern=USERNAME_PATTERN)
    nombre_completo: str = Field(min_length=1, max_length=150)
    password: str = Field(min_length=8, max_length=128)
    rol: Role

    @field_validator("username", "nombre_completo", mode="before")
    @classmethod
    def _strip(cls, v):
        return v.strip() if isinstance(v, str) else v


class UsuarioUpdate(BaseModel):
    username: Optional[str] = Field(default=None, min_length=3, max_length=64, pattern=USERNAME_PATTERN)
    nombre_completo: Optional[str] = Field(default=None, min_length=1, max_length=150)
    rol: Optional[Role] = None

    @field_validator("username", "nombre_completo", mode="before")
    @classmethod
    def _strip(cls, v):
        return v.strip() if isinstance(v, str) else v


class UsuarioEstado(BaseModel):
    activo: bool


class UsuarioResetPassword(BaseModel):
    password: str = Field(min_length=8, max_length=128)


class AuditoriaOut(BaseModel):
    id: int
    actor_id: int
    actor_username: Optional[str] = None
    usuario_objetivo_id: int
    usuario_objetivo_username: Optional[str] = None
    accion: str
    detalle: str = ""
    creado_en: datetime


# ---------- Controles / Evidencias ----------
class EvidenciaOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    control_id: int
    tipo: str
    nombre: str
    descripcion: str
    archivo_path: Optional[str] = None
    fecha_subida: datetime


class ControlBase(BaseModel):
    codigo: str = ""
    titulo: str
    descripcion: str = ""
    dominio: Dominio
    grupo: str = ""
    estado: EstadoControl = EstadoControl.no_iniciado
    responsable: str = ""
    notas: str = ""


class ControlCreate(ControlBase):
    pass


class ControlUpdate(BaseModel):
    codigo: Optional[str] = None
    titulo: Optional[str] = None
    descripcion: Optional[str] = None
    dominio: Optional[Dominio] = None
    grupo: Optional[str] = None
    estado: Optional[EstadoControl] = None
    responsable: Optional[str] = None
    notas: Optional[str] = None


class ControlOut(ControlBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    fecha_actualizacion: Optional[datetime] = None
    evidencias: List[EvidenciaOut] = []


# ---------- Incidentes ----------
class IncidenteBase(BaseModel):
    titulo: str
    descripcion: str = ""
    categoria: str = ""
    severidad: Severidad
    alcance: str = "interno"
    sistema_afectado: str = ""
    fecha_deteccion: datetime
    estado: EstadoIncidente = EstadoIncidente.registrado
    reportado_anci: bool = False
    notas: str = ""


class IncidenteCreate(IncidenteBase):
    pass


class IncidenteUpdate(BaseModel):
    titulo: Optional[str] = None
    descripcion: Optional[str] = None
    categoria: Optional[str] = None
    severidad: Optional[Severidad] = None
    alcance: Optional[str] = None
    sistema_afectado: Optional[str] = None
    fecha_deteccion: Optional[datetime] = None
    fecha_reporte: Optional[datetime] = None
    estado: Optional[EstadoIncidente] = None
    reportado_anci: Optional[bool] = None
    notas: Optional[str] = None


class IncidenteOut(IncidenteBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    fecha_reporte: Optional[datetime] = None
    alerta_temprana: Optional[datetime] = None
    plazo_reporte: Optional[datetime] = None
    vencido: bool = False


# ---------- Terceros / Proveedores ----------
class ClausulaItem(BaseModel):
    nombre: str
    cumplida: bool = False


class TerceroBase(BaseModel):
    nombre: str
    rut: str = ""
    tipo: str = "proveedor_sistema"
    contrato_ref: str = ""
    fecha_inicio: Optional[datetime] = None
    fecha_termino: Optional[datetime] = None
    contacto: str = ""
    estado_cumplimiento: EstadoCumplimiento = EstadoCumplimiento.pendiente
    clausulas: List[ClausulaItem] = []
    notas: str = ""


class TerceroCreate(TerceroBase):
    pass


class TerceroUpdate(BaseModel):
    nombre: Optional[str] = None
    rut: Optional[str] = None
    tipo: Optional[str] = None
    contrato_ref: Optional[str] = None
    fecha_inicio: Optional[datetime] = None
    fecha_termino: Optional[datetime] = None
    contacto: Optional[str] = None
    estado_cumplimiento: Optional[EstadoCumplimiento] = None
    clausulas: Optional[List[ClausulaItem]] = None
    notas: Optional[str] = None


class TerceroOut(TerceroBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


# ---------- Personas ----------
class PersonaControlBase(BaseModel):
    tipo: TipoPersonaControl
    titulo: str
    descripcion: str = ""
    estado: EstadoControl = EstadoControl.no_iniciado
    fecha: Optional[datetime] = None
    responsable: str = ""
    notas: str = ""


class PersonaControlCreate(PersonaControlBase):
    pass


class PersonaControlUpdate(BaseModel):
    tipo: Optional[TipoPersonaControl] = None
    titulo: Optional[str] = None
    descripcion: Optional[str] = None
    estado: Optional[EstadoControl] = None
    fecha: Optional[datetime] = None
    responsable: Optional[str] = None
    notas: Optional[str] = None


class PersonaControlOut(PersonaControlBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


# ---------- Madurez ----------
class MadurezDominio(BaseModel):
    dominio: Dominio
    total: int
    estados: Dict[str, int]
    pct: float
    gestionados: int
    implementados: int


class MadurezOut(BaseModel):
    global_pct: float
    total_controles: int
    dominios: List[MadurezDominio]


# ---------- Tickets (denuncias / reportes) ----------
class TicketPublicCreated(BaseModel):
    codigo: str
    codigo_seguimiento: str
    estado: EstadoTicket
    mensaje: str


class TicketPublicEstado(BaseModel):
    codigo: str
    tipo: TipoTicket
    estado: EstadoTicket
    creado_en: datetime
    actualizado_en: Optional[datetime] = None


class TicketAdjuntoOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre_archivo: str
    mime: str
    tamano_bytes: int


class TicketOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    codigo: str
    tipo: TipoTicket
    categoria: CategoriaTicket
    categoria_otro: Optional[str] = None
    severidad_percibida: Severidad
    estado: EstadoTicket
    sistema_area: str = ""
    fecha_hecho_aprox: Optional[datetime] = None
    notificar_correo: bool = False
    notificar_bandeja: bool = True
    canal_origen: str = "publico"
    incidente_id: Optional[int] = None
    creado_en: datetime
    actualizado_en: Optional[datetime] = None


class TicketDetalle(TicketOut):
    descripcion: str
    notas_internas: str = ""
    adjuntos: List[TicketAdjuntoOut] = []


class TicketEstadoUpdate(BaseModel):
    estado: EstadoTicket
    notas_internas: Optional[str] = Field(default=None, max_length=5000)


class TicketConvertir(BaseModel):
    categoria_anci: Optional[str] = Field(default=None, max_length=200)
    severidad: Optional[Severidad] = None
    alcance: Optional[str] = Field(default=None, max_length=100)


class TicketResumen(BaseModel):
    registrado: int
    en_analisis: int
    derivado_a_incidente: int
    cerrado: int
    pendientes: int


class NotificacionOut(BaseModel):
    id: int
    ticket_id: int
    ticket_codigo: str
    tipo_ticket: TipoTicket
    severidad: Severidad
    medio: MedioNotificacion
    leida: bool
    creado_en: datetime
