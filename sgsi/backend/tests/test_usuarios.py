"""Módulo Usuarios (CP-20..CP-26)."""
from .conftest import PASSWORD, USUARIOS, login


def _nuevo(client, h, **kw):
    body = {"username": "ana.torres", "nombre_completo": "Ana Torres",
            "password": "clave-segura-1", "rol": "director", **kw}
    return client.post("/api/usuarios", json=body, headers=h)


def test_solo_admin_sistema_accede(client, auth):
    for rol in ("encargado", "admin_contratos", "referente_tecnico", "director"):
        h = auth(rol)
        assert client.get("/api/usuarios", headers=h).status_code == 403
        assert client.get("/api/usuarios/auditoria", headers=h).status_code == 403
        assert _nuevo(client, h).status_code == 403
    assert client.get("/api/usuarios").status_code == 401


def test_crud_y_login_del_nuevo_usuario(client, auth):
    h = auth("admin_sistema")
    r = _nuevo(client, h)
    assert r.status_code == 201, r.text
    u = r.json()
    assert u["activo"] is True and u["rol"] == "director" and "password" not in u
    assert "password_hash" not in u
    assert login(client, "ana.torres", "clave-segura-1").status_code == 200

    r = client.put(f"/api/usuarios/{u['id']}", json={"nombre_completo": "Ana T.", "rol": "encargado"}, headers=h)
    assert r.status_code == 200 and r.json()["rol"] == "encargado"
    assert client.get(f"/api/usuarios/{u['id']}", headers=h).json()["nombre_completo"] == "Ana T."
    lista = client.get("/api/usuarios", headers=h).json()
    assert len(lista) == len(USUARIOS) + 1


def test_username_duplicado_409_y_password_corta_422(client, auth):
    h = auth("admin_sistema")
    assert _nuevo(client, h).status_code == 201
    assert _nuevo(client, h).status_code == 409
    assert _nuevo(client, h, username="ANA.TORRES").status_code == 409
    assert _nuevo(client, h, username="otra.persona", password="corta").status_code == 422


def test_deshabilitar_impide_login_y_token_existente(client, auth):
    h = auth("admin_sistema")
    uid = _nuevo(client, h).json()["id"]
    token = login(client, "ana.torres", "clave-segura-1").json()["token"]
    r = client.patch(f"/api/usuarios/{uid}/estado", json={"activo": False}, headers=h)
    assert r.status_code == 200 and r.json()["activo"] is False
    assert login(client, "ana.torres", "clave-segura-1").status_code == 401
    assert client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"}).status_code == 401
    client.patch(f"/api/usuarios/{uid}/estado", json={"activo": True}, headers=h)
    assert login(client, "ana.torres", "clave-segura-1").status_code == 200


def test_no_puede_deshabilitarse_a_si_mismo(client, auth):
    h = auth("admin_sistema")
    me = client.get("/api/auth/me", headers=h).json()
    r = client.patch(f"/api/usuarios/{me['id']}/estado", json={"activo": False}, headers=h)
    assert r.status_code == 400


def test_ultimo_admin_sistema_protegido(client, auth):
    h = auth("admin_sistema")
    uid = _nuevo(client, h, username="admin.dos", rol="admin_sistema").json()["id"]
    h2 = {"Authorization": f"Bearer {login(client, 'admin.dos', 'clave-segura-1').json()['token']}"}
    me = client.get("/api/auth/me", headers=h).json()
    # con dos admins se puede cambiar el rol de uno
    assert client.put(f"/api/usuarios/{me['id']}", json={"rol": "director"}, headers=h2).status_code == 200
    # el que queda es el último: no se puede deshabilitar ni degradar
    assert client.patch(f"/api/usuarios/{uid}/estado", json={"activo": False}, headers=h2).status_code == 400
    assert client.put(f"/api/usuarios/{uid}", json={"rol": "director"}, headers=h2).status_code == 400


def test_reset_password(client, auth):
    h = auth("admin_sistema")
    uid = _nuevo(client, h).json()["id"]
    r = client.post(f"/api/usuarios/{uid}/reset-password", json={"password": "nueva-clave-99"}, headers=h)
    assert r.status_code == 200
    assert login(client, "ana.torres", "clave-segura-1").status_code == 401
    assert login(client, "ana.torres", "nueva-clave-99").status_code == 200
    assert client.post(f"/api/usuarios/{uid}/reset-password", json={"password": "x"}, headers=h).status_code == 422


def test_auditoria_registra_acciones_sin_secretos(client, auth):
    h = auth("admin_sistema")
    uid = _nuevo(client, h).json()["id"]
    client.put(f"/api/usuarios/{uid}", json={"rol": "encargado"}, headers=h)
    client.post(f"/api/usuarios/{uid}/reset-password", json={"password": "nueva-clave-99"}, headers=h)
    client.patch(f"/api/usuarios/{uid}/estado", json={"activo": False}, headers=h)
    client.patch(f"/api/usuarios/{uid}/estado", json={"activo": True}, headers=h)
    r = client.get("/api/usuarios/auditoria", headers=h)
    assert r.status_code == 200
    acciones = {a["accion"] for a in r.json()}
    assert {"crear_usuario", "cambiar_rol", "reset_password",
            "deshabilitar_usuario", "habilitar_usuario"} <= acciones
    assert all(a["actor_username"] == "admin.sistema" for a in r.json())
    assert "nueva-clave-99" not in r.text and "clave-segura-1" not in r.text


def test_admin_sistema_no_accede_a_modulos_de_negocio(client, auth):
    h = auth("admin_sistema")
    for ruta in ("/api/controles", "/api/incidentes", "/api/terceros", "/api/personas",
                 "/api/madurez", "/api/reportes/resumen", "/api/reportes/controles.csv"):
        assert client.get(ruta, headers=h).status_code == 403, ruta


def test_roles_existentes_siguen_funcionando(client, auth):
    for rol in ("encargado", "admin_contratos", "referente_tecnico", "director"):
        h = auth(rol)
        assert client.get("/api/controles", headers=h).status_code == 200
        assert client.get("/api/incidentes", headers=h).status_code == 200
    assert PASSWORD
