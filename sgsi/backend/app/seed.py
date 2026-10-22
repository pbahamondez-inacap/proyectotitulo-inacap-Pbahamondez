"""Población inicial de datos de demostración (no usar en producción)."""
from datetime import timedelta

from .database import Base, SessionLocal, engine
from .models import (
    CategoriaTicket,
    Control,
    Dominio,
    EstadoControl,
    EstadoCumplimiento,
    EstadoIncidente,
    Incidente,
    PersonaControl,
    Role,
    Severidad,
    Tercero,
    Ticket,
    TipoPersonaControl,
    TipoTicket,
    Usuario,
)
from .notificaciones import crear_notificaciones
from .security import hash_password
from .tickets_service import crear_ticket
from .utils import now_naive

DEMO_PASSWORD = "demo123"


def _asegurar_modulos_usuarios_y_tickets(db) -> None:
    """Idempotente: agrega admin.sistema y tickets demo aunque la base ya tenga datos previos."""
    if not db.query(Usuario).filter(Usuario.username == "admin.sistema").first():
        db.add(Usuario(username="admin.sistema", password_hash=hash_password(DEMO_PASSWORD),
                       nombre_completo="Administrador de Sistema", rol=Role.admin_sistema))
        db.commit()
        print("Usuario demo creado: admin.sistema (admin_sistema)")

    if db.query(Ticket).count() > 0:
        return
    demos = [
        dict(tipo=TipoTicket.reporte_incidente, categoria=CategoriaTicket.phishing,
             descripcion="Recibí un correo que simula ser de Mesa de Ayuda solicitando mi clave "
                         "de acceso al sistema de fichas clínicas.",
             sistema_area="Correo institucional", severidad_percibida=Severidad.alta),
        dict(tipo=TipoTicket.denuncia, categoria=CategoriaTicket.uso_indebido_de_datos,
             descripcion="Se observó que se comparten datos de pacientes por mensajería "
                         "personal fuera de los canales autorizados.",
             sistema_area="Unidad de Urgencia", severidad_percibida=Severidad.media),
        dict(tipo=TipoTicket.reporte_incidente, categoria=CategoriaTicket.otros,
             categoria_otro="Equipo de red sin etiquetar",
             descripcion="Se encontró un equipo de red desconocido conectado en la sala de "
                         "servidores del segundo piso.",
             sistema_area="Sala de servidores", severidad_percibida=Severidad.baja),
    ]
    for demo in demos:
        ticket = crear_ticket(db, canal_origen="publico", notificar_bandeja=True,
                              notificar_correo=False, **demo)
        crear_notificaciones(db, ticket)
        db.commit()
    print("Tickets demo creados: 3")


def run_seed() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if db.query(Usuario).count() > 0:
            print("La base ya contiene datos; se omite el seed de datos base.")
            _asegurar_modulos_usuarios_y_tickets(db)
            return

        # ---- Usuarios (RBAC) ----
        usuarios = [
            Usuario(username="miguel.godoy", password_hash=hash_password(DEMO_PASSWORD),
                    nombre_completo="Miguel Godoy", rol=Role.encargado),
            Usuario(username="maria.perez", password_hash=hash_password(DEMO_PASSWORD),
                    nombre_completo="María Pérez", rol=Role.admin_contratos),
            Usuario(username="juan.rojas", password_hash=hash_password(DEMO_PASSWORD),
                    nombre_completo="Juan Rojas", rol=Role.referente_tecnico),
            Usuario(username="patricia.silva", password_hash=hash_password(DEMO_PASSWORD),
                    nombre_completo="Patricia Silva", rol=Role.director),
        ]
        db.add_all(usuarios)

        # ---- Controles ISO/IEC 27001:2022 (Anexo A) ----
        controles = [
            # Organizacional
            dict(codigo="A.5.1", titulo="Políticas de seguridad de la información",
                 dominio=Dominio.organizacional, grupo="5 Políticas de seguridad de la información",
                 estado=EstadoControl.gestionado, responsable="Encargado de Ciberseguridad"),
            dict(codigo="A.5.2", titulo="Roles y responsabilidades de seguridad",
                 dominio=Dominio.organizacional, grupo="5 Políticas de seguridad de la información",
                 estado=EstadoControl.implementado, responsable="Dirección"),
            dict(codigo="A.5.7", titulo="Inteligencia de amenazas",
                 dominio=Dominio.organizacional, grupo="5 Organización de la seguridad de la información",
                 estado=EstadoControl.iniciado, responsable="Referente técnico"),
            dict(codigo="A.5.24", titulo="Planificación y preparación de continuidad",
                 dominio=Dominio.organizacional, grupo="5 Organización de la seguridad de la información",
                 estado=EstadoControl.iniciado, responsable="Encargado de Ciberseguridad"),
            dict(codigo="A.5.19", titulo="Seguridad de la información en relaciones con proveedores",
                 dominio=Dominio.organizacional, grupo="5 Organización de la seguridad de la información",
                 estado=EstadoControl.iniciado, responsable="Administrador de Contratos"),
            # Personas
            dict(codigo="A.6.1", titulo="Verificación de antecedentes",
                 dominio=Dominio.personas, grupo="6 Controles de personas",
                 estado=EstadoControl.implementado, responsable="RRHH"),
            dict(codigo="A.6.3", titulo="Concientización, educación y formación",
                 dominio=Dominio.personas, grupo="6 Controles de personas",
                 estado=EstadoControl.implementado, responsable="Encargado de Ciberseguridad"),
            dict(codigo="A.6.4", titulo="Proceso disciplinario",
                 dominio=Dominio.personas, grupo="6 Controles de personas",
                 estado=EstadoControl.iniciado, responsable="RRHH"),
            dict(codigo="A.6.5", titulo="Responsabilidades después del término",
                 dominio=Dominio.personas, grupo="6 Controles de personas",
                 estado=EstadoControl.no_iniciado, responsable="RRHH"),
            dict(codigo="A.6.6", titulo="Acuerdos de confidencialidad",
                 dominio=Dominio.personas, grupo="6 Controles de personas",
                 estado=EstadoControl.implementado, responsable="RRHH"),
            # Físico
            dict(codigo="A.7.1", titulo="Perímetro de seguridad física",
                 dominio=Dominio.fisico, grupo="7 Controles físicos",
                 estado=EstadoControl.gestionado, responsable="Operaciones"),
            dict(codigo="A.7.2", titulo="Control de acceso físico",
                 dominio=Dominio.fisico, grupo="7 Controles físicos",
                 estado=EstadoControl.implementado, responsable="Operaciones"),
            dict(codigo="A.7.7", titulo="Escritorio limpio y pantalla limpia",
                 dominio=Dominio.fisico, grupo="7 Controles físicos",
                 estado=EstadoControl.iniciado, responsable="Encargado de Ciberseguridad"),
            dict(codigo="A.7.8", titulo="Ubicación y protección de equipos",
                 dominio=Dominio.fisico, grupo="7 Controles físicos",
                 estado=EstadoControl.implementado, responsable="Informática"),
            # Tecnológico
            dict(codigo="A.8.1", titulo="Puntos de acceso de usuario (identidades)",
                 dominio=Dominio.tecnologico, grupo="8 Controles tecnológicos",
                 estado=EstadoControl.implementado, responsable="Informática"),
            dict(codigo="A.8.3", titulo="Control de acceso a la información",
                 dominio=Dominio.tecnologico, grupo="8 Controles tecnológicos",
                 estado=EstadoControl.implementado, responsable="Informática"),
            dict(codigo="A.8.7", titulo="Protección contra malware",
                 dominio=Dominio.tecnologico, grupo="8 Controles tecnológicos",
                 estado=EstadoControl.gestionado, responsable="Informática"),
            dict(codigo="A.8.8", titulo="Gestión de vulnerabilidades técnicas",
                 dominio=Dominio.tecnologico, grupo="8 Controles tecnológicos",
                 estado=EstadoControl.iniciado, responsable="Referente técnico"),
            dict(codigo="A.8.12", titulo="Prevención de fuga de datos",
                 dominio=Dominio.tecnologico, grupo="8 Controles tecnológicos",
                 estado=EstadoControl.no_iniciado, responsable="Referente técnico"),
            dict(codigo="A.8.24", titulo="Uso de criptografía",
                 dominio=Dominio.tecnologico, grupo="8 Controles tecnológicos",
                 estado=EstadoControl.iniciado, responsable="Informática"),
        ]
        db.add_all([Control(**c) for c in controles])

        # ---- Incidentes ----
        ahora = now_naive()
        incidentes = [
            Incidente(
                titulo="Ransomware con exfiltración de historial clínico",
                descripcion="Cifrado de estaciones de urgencia y exfiltración parcial de fichas clínicas.",
                categoria="ransomware", severidad=Severidad.critica, alcance="interno",
                sistema_afectado="Trakcare - módulo urgencias",
                fecha_deteccion=ahora - timedelta(days=4),
                estado=EstadoIncidente.contenido, reportado_anci=True,
                fecha_reporte=ahora - timedelta(days=4, hours=-2)),
            Incidente(
                titulo="Campaña de phishing dirigida a correos institucionales",
                descripcion="Correos simulando el SSMOCC solicitando credenciales.",
                categoria="phishing", severidad=Severidad.alta, alcance="interno",
                sistema_afectado="Correo institucional",
                fecha_deteccion=ahora - timedelta(days=1),
                estado=EstadoIncidente.en_analisis),
            Incidente(
                titulo="Acceso no autorizado a cuenta de proveedor externo",
                descripcion="Uso de credenciales del proveedor de mantenimiento fuera de horario.",
                categoria="acceso_no_autorizado", severidad=Severidad.media, alcance="proveedor",
                sistema_afectado="Plataforma de mantenimiento",
                fecha_deteccion=ahora - timedelta(days=20),
                estado=EstadoIncidente.resuelto, reportado_anci=True,
                fecha_reporte=ahora - timedelta(days=19)),
            Incidente(
                titulo="Intento de denegación de servicio contra portal web",
                descripcion="Tráfico anómalo hacia el portal institucional detectado por el firewall.",
                categoria="denegacion_servicio", severidad=Severidad.baja, alcance="externo",
                sistema_afectado="Portal web institucional",
                fecha_deteccion=ahora - timedelta(days=2),
                estado=EstadoIncidente.registrado),
        ]
        db.add_all(incidentes)

        # ---- Terceros ----
        clausulas_base = [
            {"nombre": "Acuerdo de confidencialidad (NDA)", "cumplida": True},
            {"nombre": "Tratamiento de datos personales", "cumplida": True},
            {"nombre": "Reporte de incidentes de seguridad", "cumplida": True},
            {"nombre": "Continuidad y niveles de servicio (SLA)", "cumplida": True},
            {"nombre": "Subcontratación autorizada", "cumplida": False},
            {"nombre": "Derecho de auditoría", "cumplida": False},
            {"nombre": "Devolución/eliminación de datos al término", "cumplida": False},
        ]
        terceros = [
            Tercero(nombre="InterSystems Chile SpA", rut="76.000.000-0", tipo="proveedor_sistema",
                    contrato_ref="LIC-2024-018", contacto="soporte.cl@intersystems.com",
                    estado_cumplimiento=EstadoCumplimiento.parcial, clausulas=clausulas_base),
            Tercero(nombre="Seguritec Ltda.", rut="77.500.000-1", tipo="proveedor_servicio",
                    contrato_ref="LIC-2025-003", contacto="contacto@seguritec.cl",
                    estado_cumplimiento=EstadoCumplimiento.cumple,
                    clausulas=[{**c, "cumplida": True} for c in clausulas_base]),
        ]
        db.add_all(terceros)

        # ---- Controles de personas ----
        personas = [
            PersonaControl(tipo=TipoPersonaControl.antecedentes,
                           titulo="Verificación de antecedentes del personal nuevo",
                           estado=EstadoControl.implementado, responsable="RRHH",
                           fecha=ahora - timedelta(days=30)),
            PersonaControl(tipo=TipoPersonaControl.capacitacion,
                           titulo="Capacitación anual de concientización en ciberseguridad",
                           estado=EstadoControl.implementado, responsable="Encargado de Ciberseguridad",
                           fecha=ahora - timedelta(days=10)),
            PersonaControl(tipo=TipoPersonaControl.confidencialidad,
                           titulo="Firma de acuerdos de confidencialidad",
                           estado=EstadoControl.implementado, responsable="RRHH",
                           fecha=ahora - timedelta(days=15)),
            PersonaControl(tipo=TipoPersonaControl.condiciones_empleo,
                           titulo="Cláusulas de seguridad en condiciones de empleo",
                           estado=EstadoControl.iniciado, responsable="RRHH"),
            PersonaControl(tipo=TipoPersonaControl.disciplinario,
                           titulo="Proceso disciplinario por incumplimiento de seguridad",
                           estado=EstadoControl.no_iniciado, responsable="RRHH"),
            PersonaControl(tipo=TipoPersonaControl.termino_contrato,
                           titulo="Retiro de accesos y devolución de activos al término",
                           estado=EstadoControl.iniciado, responsable="Informática"),
        ]
        db.add_all(personas)

        db.commit()
        _asegurar_modulos_usuarios_y_tickets(db)
        print(f"Seed completado. Usuarios (contraseña: {DEMO_PASSWORD}):")
        print("  miguel.godoy (encargado), maria.perez (admin_contratos), "
              "juan.rojas (referente_tecnico), patricia.silva (director), "
              "admin.sistema (admin_sistema)")
    finally:
        db.close()


if __name__ == "__main__":
    run_seed()
