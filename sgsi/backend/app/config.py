"""Configuración central de la aplicación SGSI."""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent  # carpeta backend/
DATA_DIR = Path(os.getenv("SGSI_DATA_DIR", BASE_DIR / "data"))
EVIDENCE_DIR = DATA_DIR / "evidencias"

SECRET_KEY = os.getenv("SGSI_SECRET_KEY", "clave-de-desarrollo-cambiar-en-produccion")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("SGSI_TOKEN_EXPIRE", "480"))

# PostgreSQL-compatible: SGSI_DATABASE_URL=postgresql+psycopg://user:pass@host/db
DATABASE_URL = os.getenv("SGSI_DATABASE_URL", f"sqlite:///{DATA_DIR / 'sgsi.db'}")

# Adjuntos de tickets: <SGSI_UPLOAD_DIR>/tickets/<codigo>/ (por defecto, bajo la carpeta de evidencias)
UPLOAD_DIR = Path(os.getenv("SGSI_UPLOAD_DIR", EVIDENCE_DIR))
TICKET_UPLOAD_DIR = UPLOAD_DIR / "tickets"
TICKET_MAX_FILES = 5
TICKET_MAX_FILE_BYTES = 10 * 1024 * 1024  # 10 MB por archivo
TICKET_ALLOWED_EXTENSIONS = {
    ".pdf", ".png", ".jpg", ".jpeg", ".txt", ".eml", ".msg", ".docx", ".xlsx", ".csv",
}


def _parse_rate_limit(value: str, default: tuple[int, int]) -> tuple[int, int]:
    """Interpreta 'N/segundos' (p. ej. '5/600' = 5 solicitudes cada 10 minutos)."""
    try:
        limit, window = value.split("/", 1)
        limit, window = int(limit), int(window)
        if limit > 0 and window > 0:
            return limit, window
    except ValueError:
        pass
    return default


# Rate limiting del formulario público (en memoria, por cliente; la IP nunca se persiste)
PUBLIC_RATE_LIMIT = _parse_rate_limit(os.getenv("SGSI_PUBLIC_RATE_LIMIT", "5/600"), (5, 600))
PUBLIC_LOOKUP_RATE_LIMIT = _parse_rate_limit(
    os.getenv("SGSI_PUBLIC_LOOKUP_RATE_LIMIT", "30/600"), (30, 600)
)
# Solo detrás de un reverse proxy de confianza: usa X-Forwarded-For para identificar al cliente
TRUST_PROXY = os.getenv("SGSI_TRUST_PROXY", "0").lower() in ("1", "true", "yes")

# Notificaciones por correo (SMTP institucional). Sin SGSI_SMTP_HOST el envío se simula.
SMTP_HOST = os.getenv("SGSI_SMTP_HOST", "")
SMTP_PORT = int(os.getenv("SGSI_SMTP_PORT", "587"))
SMTP_USER = os.getenv("SGSI_SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SGSI_SMTP_PASSWORD", "")
SMTP_FROM = os.getenv("SGSI_SMTP_FROM", "sgsi@hospital.local")
SMTP_TO = [t.strip() for t in os.getenv("SGSI_SMTP_TO", "").split(",") if t.strip()]
SMTP_STARTTLS = os.getenv("SGSI_SMTP_STARTTLS", "1").lower() in ("1", "true", "yes")
# Enlace a la bandeja de tickets que se incluye en el correo
APP_URL = os.getenv("SGSI_APP_URL", "http://localhost:5173").rstrip("/")

# Pesos de madurez por estado de control (para calcular el % de avance del SGSI)
MATURITY_WEIGHTS = {
    "no_iniciado": 0.0,
    "iniciado": 0.33,
    "implementado": 0.67,
    "gestionado": 1.0,
}
