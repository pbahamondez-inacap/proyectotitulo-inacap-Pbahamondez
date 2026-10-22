"""Fixtures de pruebas: BD SQLite aislada dentro de tests/.test_data (ignorada por git)."""
import os
import shutil
from pathlib import Path

_DATA = Path(__file__).parent / ".test_data"
shutil.rmtree(_DATA, ignore_errors=True)
_DATA.mkdir(parents=True, exist_ok=True)
os.environ["SGSI_DATA_DIR"] = str(_DATA)
os.environ["SGSI_DATABASE_URL"] = f"sqlite:///{_DATA / 'test.db'}"
os.environ["SGSI_UPLOAD_DIR"] = str(_DATA / "uploads")
os.environ.pop("SGSI_SMTP_HOST", None)
os.environ.pop("SGSI_SMTP_TO", None)

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

from app import ratelimit  # noqa: E402
from app.database import Base, SessionLocal, engine  # noqa: E402
from app.main import app  # noqa: E402
from app.models import Role, Usuario  # noqa: E402
from app.security import hash_password  # noqa: E402

PASSWORD = "demo12345"
USUARIOS = {
    "encargado": ("miguel.godoy", Role.encargado),
    "admin_contratos": ("maria.perez", Role.admin_contratos),
    "referente_tecnico": ("juan.rojas", Role.referente_tecnico),
    "director": ("patricia.silva", Role.director),
    "admin_sistema": ("admin.sistema", Role.admin_sistema),
}

TICKET_FORM = {
    "tipo": "reporte_incidente",
    "categoria": "phishing",
    "descripcion": "Recibí un correo sospechoso que pide mi contraseña institucional.",
    "severidad_percibida": "alta",
    "notificar_bandeja": "true",
    "notificar_correo": "false",
}


@pytest.fixture(autouse=True)
def _db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    for username, rol in USUARIOS.values():
        db.add(Usuario(username=username, password_hash=hash_password(PASSWORD),
                       nombre_completo=username.replace(".", " ").title(), rol=rol, activo=True))
    db.commit()
    db.close()
    shutil.rmtree(_DATA / "uploads", ignore_errors=True)
    ratelimit.create_limiter.reset()
    ratelimit.lookup_limiter.reset()
    old = (ratelimit.create_limiter.limit, ratelimit.lookup_limiter.limit)
    ratelimit.create_limiter.limit = 1000
    ratelimit.lookup_limiter.limit = 1000
    yield
    ratelimit.create_limiter.limit, ratelimit.lookup_limiter.limit = old


@pytest.fixture()
def client():
    with TestClient(app) as c:
        yield c


def login(client, username, password=PASSWORD):
    return client.post("/api/auth/login", json={"username": username, "password": password})


@pytest.fixture()
def auth(client):
    """auth('encargado') -> cabeceras Authorization."""
    def _auth(rol: str) -> dict:
        r = login(client, USUARIOS[rol][0])
        assert r.status_code == 200, r.text
        return {"Authorization": f"Bearer {r.json()['token']}"}
    return _auth


@pytest.fixture()
def crear_ticket_publico(client):
    def _crear(files=None, **overrides):
        data = {**TICKET_FORM, **overrides}
        data = {k: v for k, v in data.items() if v is not None}
        return client.post("/api/public/tickets", data=data, files=files)
    return _crear
