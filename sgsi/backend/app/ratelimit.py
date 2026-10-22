"""Rate limiting en memoria (ventana deslizante) para los endpoints públicos.

Anonimato: la clave del cliente es un hash con sal aleatoria por proceso; la IP no se
persiste ni se registra en logs y el estado desaparece al reiniciar la aplicación.
"""
import hashlib
import secrets
import threading
import time
from collections import deque

from fastapi import HTTPException, Request, status

from .config import PUBLIC_LOOKUP_RATE_LIMIT, PUBLIC_RATE_LIMIT, TRUST_PROXY

_SALT = secrets.token_bytes(16)
_MAX_KEYS = 10_000


def client_key(request: Request) -> str:
    host = request.client.host if request.client else "desconocido"
    if TRUST_PROXY:
        forwarded = request.headers.get("x-forwarded-for", "")
        if forwarded:
            host = forwarded.split(",")[0].strip() or host
    return hashlib.sha256(_SALT + host.encode()).hexdigest()


class SlidingWindowLimiter:
    def __init__(self, limit: int, window_seconds: int):
        self.limit = limit
        self.window = window_seconds
        self._hits: dict[str, deque] = {}
        self._lock = threading.Lock()

    def reset(self) -> None:
        with self._lock:
            self._hits.clear()

    def hit(self, key: str) -> float | None:
        """Registra una solicitud. Devuelve None si se permite o los segundos de espera si se excede."""
        now = time.monotonic()
        with self._lock:
            if len(self._hits) > _MAX_KEYS:
                self._purge(now)
            hits = self._hits.setdefault(key, deque())
            while hits and now - hits[0] >= self.window:
                hits.popleft()
            if len(hits) >= self.limit:
                return max(self.window - (now - hits[0]), 1.0)
            hits.append(now)
            return None

    def _purge(self, now: float) -> None:
        for key in [k for k, h in self._hits.items() if not h or now - h[-1] >= self.window]:
            del self._hits[key]


create_limiter = SlidingWindowLimiter(*PUBLIC_RATE_LIMIT)
lookup_limiter = SlidingWindowLimiter(*PUBLIC_LOOKUP_RATE_LIMIT)


def _enforce(limiter: SlidingWindowLimiter, request: Request) -> None:
    wait = limiter.hit(client_key(request))
    if wait is not None:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Demasiadas solicitudes. Intente nuevamente más tarde.",
            headers={"Retry-After": str(int(wait))},
        )


def limit_ticket_creation(request: Request) -> None:
    _enforce(create_limiter, request)


def limit_ticket_lookup(request: Request) -> None:
    _enforce(lookup_limiter, request)
