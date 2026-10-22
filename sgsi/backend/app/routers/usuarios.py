"""Administración de usuarios (solo admin_sistema) con bitácora de auditoría."""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func
from sqlalchemy.orm import Session, aliased

from ..database import get_db
from ..deps import require_roles
from ..models import AuditoriaUsuario, Role, Usuario
from ..schemas import (
    AuditoriaOut,
    UsuarioCreate,
    UsuarioEstado,
    UsuarioOut,
    UsuarioResetPassword,
    UsuarioUpdate,
)
from ..security import hash_password

router = APIRouter(prefix="/usuarios", tags=["usuarios"])

_admin = require_roles(Role.admin_sistema)


def _get_usuario(usuario_id: int, db: Session) -> Usuario:
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario


def _username_en_uso(db: Session, username: str, excluir_id: int | None = None) -> bool:
    q = db.query(Usuario.id).filter(func.lower(Usuario.username) == username.lower())
    if excluir_id is not None:
        q = q.filter(Usuario.id != excluir_id)
    return q.first() is not None


def _es_ultimo_admin_activo(db: Session, usuario: Usuario) -> bool:
    if usuario.rol != Role.admin_sistema or not usuario.activo:
        return False
    activos = (
        db.query(Usuario)
        .filter(Usuario.rol == Role.admin_sistema, Usuario.activo.is_(True))
        .count()
    )
    return activos <= 1


def _auditar(db: Session, actor: Usuario, objetivo: Usuario, accion: str, detalle: str = "") -> None:
    db.add(
        AuditoriaUsuario(
            actor_id=actor.id, usuario_objetivo_id=objetivo.id, accion=accion, detalle=detalle
        )
    )


@router.get("", response_model=list[UsuarioOut])
def list_usuarios(db: Session = Depends(get_db), user=Depends(_admin)):
    return db.query(Usuario).order_by(Usuario.id).all()


@router.post("", response_model=UsuarioOut, status_code=201)
def create_usuario(data: UsuarioCreate, db: Session = Depends(get_db), user=Depends(_admin)):
    if _username_en_uso(db, data.username):
        raise HTTPException(status_code=409, detail="El nombre de usuario ya existe")
    usuario = Usuario(
        username=data.username,
        nombre_completo=data.nombre_completo,
        password_hash=hash_password(data.password),
        rol=data.rol,
        activo=True,
    )
    db.add(usuario)
    db.flush()
    _auditar(db, user, usuario, "crear_usuario", f"username={usuario.username}; rol={usuario.rol.value}")
    db.commit()
    db.refresh(usuario)
    return usuario


# Declarada antes de /{usuario_id} para que "auditoria" no se interprete como id
@router.get("/auditoria", response_model=list[AuditoriaOut])
def list_auditoria(
    limit: int = Query(default=500, ge=1, le=2000),
    db: Session = Depends(get_db),
    user=Depends(_admin),
):
    actor = aliased(Usuario)
    objetivo = aliased(Usuario)
    filas = (
        db.query(AuditoriaUsuario, actor.username, objetivo.username)
        .outerjoin(actor, actor.id == AuditoriaUsuario.actor_id)
        .outerjoin(objetivo, objetivo.id == AuditoriaUsuario.usuario_objetivo_id)
        .order_by(AuditoriaUsuario.creado_en.desc(), AuditoriaUsuario.id.desc())
        .limit(limit)
        .all()
    )
    return [
        AuditoriaOut(
            id=a.id,
            actor_id=a.actor_id,
            actor_username=actor_username,
            usuario_objetivo_id=a.usuario_objetivo_id,
            usuario_objetivo_username=objetivo_username,
            accion=a.accion,
            detalle=a.detalle or "",
            creado_en=a.creado_en,
        )
        for a, actor_username, objetivo_username in filas
    ]


@router.get("/{usuario_id}", response_model=UsuarioOut)
def get_usuario(usuario_id: int, db: Session = Depends(get_db), user=Depends(_admin)):
    return _get_usuario(usuario_id, db)


@router.put("/{usuario_id}", response_model=UsuarioOut)
def update_usuario(
    usuario_id: int,
    data: UsuarioUpdate,
    db: Session = Depends(get_db),
    user=Depends(_admin),
):
    usuario = _get_usuario(usuario_id, db)
    cambios = data.model_dump(exclude_unset=True)
    detalle_datos: list[str] = []

    if cambios.get("username") is not None and cambios["username"] != usuario.username:
        if _username_en_uso(db, cambios["username"], excluir_id=usuario.id):
            raise HTTPException(status_code=409, detail="El nombre de usuario ya existe")
        detalle_datos.append(f"username: {usuario.username} -> {cambios['username']}")
        usuario.username = cambios["username"]

    if cambios.get("nombre_completo") is not None and cambios["nombre_completo"] != usuario.nombre_completo:
        detalle_datos.append(
            f"nombre_completo: {usuario.nombre_completo} -> {cambios['nombre_completo']}"
        )
        usuario.nombre_completo = cambios["nombre_completo"]

    nuevo_rol = cambios.get("rol")
    detalle_rol = None
    if nuevo_rol is not None and nuevo_rol != usuario.rol:
        if usuario.rol == Role.admin_sistema and _es_ultimo_admin_activo(db, usuario):
            raise HTTPException(
                status_code=400,
                detail="No se puede cambiar el rol del último administrador de sistema activo",
            )
        detalle_rol = f"rol: {usuario.rol.value} -> {nuevo_rol.value}"
        usuario.rol = nuevo_rol

    if detalle_datos:
        _auditar(db, user, usuario, "editar_usuario", "; ".join(detalle_datos))
    if detalle_rol:
        _auditar(db, user, usuario, "cambiar_rol", detalle_rol)
    db.commit()
    db.refresh(usuario)
    return usuario


@router.patch("/{usuario_id}/estado", response_model=UsuarioOut)
def set_estado(
    usuario_id: int,
    data: UsuarioEstado,
    db: Session = Depends(get_db),
    user=Depends(_admin),
):
    usuario = _get_usuario(usuario_id, db)
    if bool(usuario.activo) == data.activo:
        return usuario
    if not data.activo:
        if usuario.id == user.id:
            raise HTTPException(status_code=400, detail="No puede deshabilitar su propio usuario")
        if _es_ultimo_admin_activo(db, usuario):
            raise HTTPException(
                status_code=400,
                detail="No se puede deshabilitar al último administrador de sistema activo",
            )
    usuario.activo = data.activo
    _auditar(
        db, user, usuario, "habilitar_usuario" if data.activo else "deshabilitar_usuario",
        f"username={usuario.username}",
    )
    db.commit()
    db.refresh(usuario)
    return usuario


@router.post("/{usuario_id}/reset-password")
def reset_password(
    usuario_id: int,
    data: UsuarioResetPassword,
    db: Session = Depends(get_db),
    user=Depends(_admin),
):
    usuario = _get_usuario(usuario_id, db)
    usuario.password_hash = hash_password(data.password)
    _auditar(db, user, usuario, "reset_password", "Contraseña restablecida")
    db.commit()
    return {"ok": True}
