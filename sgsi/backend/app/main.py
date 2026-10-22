"""Aplicación FastAPI del SGSI — Hospital Félix Bulnes Cerda."""
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models  # noqa: F401  (registra los modelos en Base.metadata)
from .database import Base, engine
from .routers import (
    auth,
    controles,
    evidencias,
    incidentes,
    madurez,
    notificaciones,
    personas,
    public_tickets,
    reportes,
    terceros,
    tickets,
    usuarios,
)


class _OmitirRutasPublicas(logging.Filter):
    """Anonimato: el log de acceso no registra (IP incluida) las solicitudes al formulario público."""

    def filter(self, record: logging.LogRecord) -> bool:
        args = record.args
        path = args[2] if isinstance(args, tuple) and len(args) >= 3 else ""
        return not str(path).startswith("/api/public/")


logging.getLogger("uvicorn.access").addFilter(_OmitirRutasPublicas())

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SGSI — Hospital Félix Bulnes Cerda",
    description="Sistema de Gestión de Seguridad de la Información (controles ISO/IEC 27001, madurez, incidentes ANCI, terceros, personas, usuarios y ticketera de denuncias/reportes).",
    version="1.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for router in (
    auth.router,
    controles.router,
    evidencias.router,
    incidentes.router,
    terceros.router,
    personas.router,
    madurez.router,
    reportes.router,
    usuarios.router,
    tickets.router,
    public_tickets.router,
    notificaciones.router,
):
    app.include_router(router, prefix="/api")


@app.get("/api/health")
def health():
    return {"status": "ok"}
