"""Módulo Ticketera (CP-27..CP-38)."""
import logging

from app import config, notificaciones, ratelimit
from app.database import SessionLocal
from app.models import Notificacion, Ticket, TicketAdjunto

from .conftest import TICKET_FORM


def _crear(crear_ticket_publico, **kw):
    r = crear_ticket_publico(**kw)
    assert r.status_code == 201, r.text
    return r.json()


def _id_por_codigo(client, auth, codigo):
    lista = client.get("/api/tickets", headers=auth("encargado")).json()
    return next(t["id"] for t in lista if t["codigo"] == codigo)


# ---------- Formulario público ----------
def test_crear_ticket_publico_sin_token(client, crear_ticket_publico):
    r = crear_ticket_publico()
    assert r.status_code == 201
    d = r.json()
    assert d["codigo"].startswith("TCK-") and d["estado"] == "registrado"
    assert len(d["codigo_seguimiento"]) >= 12 and d["mensaje"]


def test_categorias_publicas(client):
    r = client.get("/api/public/tickets/categorias")
    assert r.status_code == 200
    assert "otros" in str(r.json())


def test_otros_exige_texto(crear_ticket_publico):
    assert crear_ticket_publico(categoria="otros").status_code == 422
    assert crear_ticket_publico(categoria="otros", categoria_otro="Algo distinto").status_code == 201


def test_validaciones_del_formulario(crear_ticket_publico):
    assert crear_ticket_publico(descripcion="corta").status_code == 422
    assert crear_ticket_publico(descripcion="x" * 5001).status_code == 422
    assert crear_ticket_publico(tipo="otro").status_code == 422
    assert crear_ticket_publico(severidad_percibida="enorme").status_code == 422
    assert crear_ticket_publico(notificar_bandeja="false", notificar_correo="false").status_code == 422
    assert crear_ticket_publico(fecha_hecho_aprox="ayer").status_code == 422
    assert crear_ticket_publico(fecha_hecho_aprox="2026-10-01T10:00:00").status_code == 201


def test_honeypot_no_guarda(client, auth, crear_ticket_publico):
    r = crear_ticket_publico(website="http://spam.example")
    assert r.status_code == 201
    assert client.get("/api/tickets", headers=auth("encargado")).json() == []


def test_anonimato_no_persiste_identidad(client, auth, crear_ticket_publico):
    h = auth("admin_sistema")  # token válido enviado al endpoint público
    r = client.post("/api/public/tickets", data=TICKET_FORM,
                    headers={**h, "User-Agent": "UA-secreto/1.0", "X-Forwarded-For": "203.0.113.9"})
    assert r.status_code == 201
    db = SessionLocal()
    try:
        columnas = {c.name for c in Ticket.__table__.columns}
        prohibidas = {"ip", "ip_origen", "user_agent", "usuario_id", "creado_por", "autor_id", "autor"}
        assert not (columnas & prohibidas)
        fks = [fk.target_fullname for c in Ticket.__table__.columns for fk in c.foreign_keys]
        assert all(not f.startswith("usuarios.") for f in fks)
        t = db.query(Ticket).one()
        valores = " ".join(str(getattr(t, c)) for c in columnas)
        assert "UA-secreto" not in valores and "203.0.113.9" not in valores and "127.0.0.1" not in valores
    finally:
        db.close()


def test_consulta_de_estado_solo_datos_minimos(client, auth, crear_ticket_publico):
    d = _crear(crear_ticket_publico)
    r = client.get(f"/api/public/tickets/{d['codigo_seguimiento']}")
    assert r.status_code == 200
    assert set(r.json()) == {"codigo", "tipo", "estado", "creado_en", "actualizado_en"}
    assert client.get("/api/public/tickets/no-existe-123").status_code == 404
    # el código interno no sirve como código de seguimiento
    assert client.get(f"/api/public/tickets/{d['codigo']}").status_code == 404


def test_estado_publico_refleja_cambios(client, auth, crear_ticket_publico):
    d = _crear(crear_ticket_publico)
    tid = _id_por_codigo(client, auth, d["codigo"])
    client.patch(f"/api/tickets/{tid}/estado", json={"estado": "en_analisis"}, headers=auth("encargado"))
    assert client.get(f"/api/public/tickets/{d['codigo_seguimiento']}").json()["estado"] == "en_analisis"


# ---------- Notificaciones ----------
def test_notificacion_bandeja(client, auth, crear_ticket_publico):
    d = _crear(crear_ticket_publico)
    h = auth("encargado")
    assert client.get("/api/notificaciones/pendientes/count", headers=h).json() == {"count": 1}
    lista = client.get("/api/notificaciones", headers=h).json()
    assert len(lista) == 1 and lista[0]["ticket_codigo"] == d["codigo"] and lista[0]["leida"] is False
    assert client.post(f"/api/notificaciones/{lista[0]['id']}/leer", headers=h).status_code == 200
    assert client.get("/api/notificaciones/pendientes/count", headers=h).json() == {"count": 0}
    assert client.get("/api/notificaciones?solo_no_leidas=true", headers=h).json() == []


def test_notificaciones_solo_encargado(client, auth):
    for rol in ("admin_sistema", "director", "admin_contratos", "referente_tecnico"):
        assert client.get("/api/notificaciones", headers=auth(rol)).status_code == 403
    assert client.get("/api/notificaciones").status_code == 401


def test_notificar_solo_correo_sin_smtp_se_simula(client, auth, crear_ticket_publico):
    _crear(crear_ticket_publico, notificar_bandeja="false", notificar_correo="true")
    assert client.get("/api/notificaciones/pendientes/count", headers=auth("encargado")).json() == {"count": 0}
    db = SessionLocal()
    try:
        n = db.query(Notificacion).one()
        assert n.medio.value == "correo" and n.estado_envio == "simulado"
    finally:
        db.close()


def test_notificar_ambos_medios(client, auth, crear_ticket_publico):
    _crear(crear_ticket_publico, notificar_bandeja="true", notificar_correo="true")
    assert client.get("/api/notificaciones/pendientes/count", headers=auth("encargado")).json() == {"count": 1}
    db = SessionLocal()
    try:
        assert db.query(Notificacion).count() == 2
    finally:
        db.close()


def test_smtp_configurado_envia(monkeypatch, crear_ticket_publico):
    enviados = []
    monkeypatch.setattr(config, "SMTP_HOST", "smtp.local")
    monkeypatch.setattr(config, "SMTP_TO", ["encargado@hospital.cl"])
    monkeypatch.setattr(notificaciones, "_send_smtp", lambda msg: enviados.append(msg))
    _crear(crear_ticket_publico, notificar_correo="true")
    assert len(enviados) == 1
    assert enviados[0]["To"] == "encargado@hospital.cl"
    assert "Recibí un correo" not in enviados[0].get_content()  # sin contenido sensible
    db = SessionLocal()
    try:
        assert db.query(Notificacion).filter_by(medio="correo").one().estado_envio == "enviado"
    finally:
        db.close()


def test_fallo_smtp_no_afecta_al_ticket(monkeypatch, crear_ticket_publico):
    def falla(msg):
        raise OSError("sin conexión")

    monkeypatch.setattr(config, "SMTP_HOST", "smtp.local")
    monkeypatch.setattr(config, "SMTP_TO", ["encargado@hospital.cl"])
    monkeypatch.setattr(notificaciones, "_send_smtp", falla)
    r = crear_ticket_publico(notificar_correo="true")
    assert r.status_code == 201
    db = SessionLocal()
    try:
        assert db.query(Ticket).count() == 1
        assert db.query(Notificacion).filter_by(medio="correo").one().estado_envio == "error"
    finally:
        db.close()


# ---------- Bandeja interna ----------
def test_bandeja_solo_encargado(client, auth, crear_ticket_publico):
    _crear(crear_ticket_publico)
    assert client.get("/api/tickets").status_code == 401
    for rol in ("admin_sistema", "director", "admin_contratos", "referente_tecnico"):
        h = auth(rol)
        assert client.get("/api/tickets", headers=h).status_code == 403
        assert client.get("/api/tickets/resumen", headers=h).status_code == 403
        assert client.get("/api/tickets/1", headers=h).status_code == 403
        assert client.patch("/api/tickets/1/estado", json={"estado": "cerrado"}, headers=h).status_code == 403
        assert client.post("/api/tickets/1/convertir-incidente", headers=h).status_code == 403
    assert client.get("/api/tickets", headers=auth("encargado")).status_code == 200


def test_listado_filtros_resumen_y_detalle(client, auth, crear_ticket_publico):
    h = auth("encargado")
    a = _crear(crear_ticket_publico)
    _crear(crear_ticket_publico, tipo="denuncia", severidad_percibida="baja", categoria="fuga_de_informacion")
    assert len(client.get("/api/tickets", headers=h).json()) == 2
    assert len(client.get("/api/tickets?tipo=denuncia", headers=h).json()) == 1
    assert len(client.get("/api/tickets?severidad=alta", headers=h).json()) == 1
    assert len(client.get("/api/tickets?estado=cerrado", headers=h).json()) == 0
    assert client.get("/api/tickets?estado=xx", headers=h).status_code == 422
    assert client.get("/api/tickets/resumen", headers=h).json() == {
        "registrado": 2, "en_analisis": 0, "derivado_a_incidente": 0, "cerrado": 0, "pendientes": 2}
    tid = _id_por_codigo(client, auth, a["codigo"])
    det = client.get(f"/api/tickets/{tid}", headers=h).json()
    assert det["descripcion"] and det["adjuntos"] == []
    assert "codigo_seguimiento" not in det
    assert client.get("/api/tickets/9999", headers=h).status_code == 404


def test_transiciones_de_estado(client, auth, crear_ticket_publico):
    h = auth("encargado")
    d = _crear(crear_ticket_publico)
    tid = _id_por_codigo(client, auth, d["codigo"])
    url = f"/api/tickets/{tid}/estado"
    assert client.patch(url, json={"estado": "derivado_a_incidente"}, headers=h).status_code == 400
    r = client.patch(url, json={"estado": "en_analisis", "notas_internas": "Revisando"}, headers=h)
    assert r.status_code == 200 and r.json()["estado"] == "en_analisis" and r.json()["notas_internas"] == "Revisando"
    assert client.patch(url, json={"estado": "registrado"}, headers=h).status_code == 400
    assert client.patch(url, json={"estado": "cerrado"}, headers=h).status_code == 200
    assert client.patch(url, json={"estado": "en_analisis"}, headers=h).status_code == 400
    assert client.get("/api/tickets/resumen", headers=h).json()["cerrado"] == 1


def test_convertir_a_incidente(client, auth, crear_ticket_publico):
    h = auth("encargado")
    d = _crear(crear_ticket_publico, fecha_hecho_aprox="2026-10-01T10:00:00")
    tid = _id_por_codigo(client, auth, d["codigo"])
    r = client.post(f"/api/tickets/{tid}/convertir-incidente", headers=h)
    assert r.status_code == 201, r.text
    inc = r.json()
    assert d["codigo"] in inc["titulo"] and inc["severidad"] == "alta"
    assert inc["plazo_reporte"] and inc["alerta_temprana"]
    assert client.get(f"/api/incidentes/{inc['id']}", headers=h).status_code == 200
    det = client.get(f"/api/tickets/{tid}", headers=h).json()
    assert det["estado"] == "derivado_a_incidente" and det["incidente_id"] == inc["id"]
    assert client.post(f"/api/tickets/{tid}/convertir-incidente", headers=h).status_code == 409
    assert client.patch(f"/api/tickets/{tid}/estado", json={"estado": "cerrado"}, headers=h).status_code == 200


def test_convertir_con_ajustes(client, auth, crear_ticket_publico):
    h = auth("encargado")
    d = _crear(crear_ticket_publico)
    tid = _id_por_codigo(client, auth, d["codigo"])
    r = client.post(f"/api/tickets/{tid}/convertir-incidente", headers=h,
                    json={"severidad": "critica", "categoria_anci": "Compromiso de credenciales", "alcance": "externo"})
    assert r.status_code == 201
    inc = r.json()
    assert inc["severidad"] == "critica" and inc["categoria"] == "Compromiso de credenciales"
    assert inc["alcance"] == "externo"


def test_convertir_ticket_cerrado_falla(client, auth, crear_ticket_publico):
    h = auth("encargado")
    d = _crear(crear_ticket_publico)
    tid = _id_por_codigo(client, auth, d["codigo"])
    client.patch(f"/api/tickets/{tid}/estado", json={"estado": "en_analisis"}, headers=h)
    client.patch(f"/api/tickets/{tid}/estado", json={"estado": "cerrado"}, headers=h)
    assert client.post(f"/api/tickets/{tid}/convertir-incidente", headers=h).status_code == 400


def test_eliminar_incidente_desvincula_ticket(client, auth, crear_ticket_publico):
    h = auth("encargado")
    d = _crear(crear_ticket_publico)
    tid = _id_por_codigo(client, auth, d["codigo"])
    inc = client.post(f"/api/tickets/{tid}/convertir-incidente", headers=h).json()
    r = client.delete(f"/api/incidentes/{inc['id']}", headers=h)
    assert r.status_code in (200, 204)
    assert client.get(f"/api/tickets/{tid}", headers=h).json()["incidente_id"] is None


# ---------- Adjuntos ----------
def test_adjunto_valido_y_descarga(client, auth, crear_ticket_publico):
    d = _crear(crear_ticket_publico, files=[("archivos", ("captura.png", b"\x89PNG-datos", "image/png"))])
    h = auth("encargado")
    tid = _id_por_codigo(client, auth, d["codigo"])
    det = client.get(f"/api/tickets/{tid}", headers=h).json()
    assert len(det["adjuntos"]) == 1 and det["adjuntos"][0]["nombre_archivo"] == "captura.png"
    r = client.get(f"/api/tickets/{tid}/adjuntos/{det['adjuntos'][0]['id']}", headers=h)
    assert r.status_code == 200 and r.content == b"\x89PNG-datos"
    assert r.headers.get("x-content-type-options") == "nosniff"
    assert client.get(f"/api/tickets/{tid}/adjuntos/{det['adjuntos'][0]['id']}").status_code == 401
    assert client.get(f"/api/tickets/{tid}/adjuntos/{det['adjuntos'][0]['id']}",
                      headers=auth("admin_sistema")).status_code == 403
    db = SessionLocal()
    try:
        ruta = db.query(TicketAdjunto).one().ruta
        assert "captura" not in ruta
    finally:
        db.close()


def test_adjunto_extension_no_permitida_415(client, auth, crear_ticket_publico):
    r = crear_ticket_publico(files=[("archivos", ("virus.exe", b"MZ", "application/octet-stream"))])
    assert r.status_code == 415
    assert client.get("/api/tickets", headers=auth("encargado")).json() == []


def test_adjunto_muy_grande_413(client, crear_ticket_publico):
    big = b"a" * (config.TICKET_MAX_FILE_BYTES + 1)
    assert crear_ticket_publico(files=[("archivos", ("grande.pdf", big, "application/pdf"))]).status_code == 413


def test_demasiados_adjuntos(crear_ticket_publico):
    files = [("archivos", (f"a{i}.txt", b"x", "text/plain")) for i in range(config.TICKET_MAX_FILES + 1)]
    assert crear_ticket_publico(files=files).status_code == 413


def test_nombre_malicioso_no_escapa_del_directorio(client, auth, crear_ticket_publico):
    r = crear_ticket_publico(files=[("archivos", ("../../evil.txt", b"x", "text/plain"))])
    assert r.status_code == 201
    base = config.TICKET_UPLOAD_DIR.resolve()
    archivos = [p for p in base.rglob("*") if p.is_file()]
    assert archivos and all(base in p.resolve().parents for p in archivos)


# ---------- Rate limit ----------
def test_rate_limit_creacion(crear_ticket_publico):
    ratelimit.create_limiter.limit = 3
    codigos = [crear_ticket_publico().status_code for _ in range(5)]
    assert codigos == [201, 201, 201, 429, 429]


def test_rate_limit_consulta(client):
    ratelimit.lookup_limiter.limit = 2
    codigos = [client.get("/api/public/tickets/abc").status_code for _ in range(4)]
    assert codigos == [404, 404, 429, 429]
    assert "retry-after" in client.get("/api/public/tickets/abc").headers


def test_no_se_registra_contenido_en_logs(client, caplog, crear_ticket_publico):
    caplog.set_level(logging.DEBUG)
    crear_ticket_publico(descripcion="Texto confidencial unico ZZZ-12345 de la denuncia")
    assert "ZZZ-12345" not in caplog.text
