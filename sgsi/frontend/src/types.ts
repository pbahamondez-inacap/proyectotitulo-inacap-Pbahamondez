export type Role = 'encargado' | 'admin_contratos' | 'referente_tecnico' | 'director' | 'admin_sistema'
export type Dominio = 'organizacional' | 'personas' | 'fisico' | 'tecnologico'
export type EstadoControl = 'no_iniciado' | 'iniciado' | 'implementado' | 'gestionado'
export type Severidad = 'baja' | 'media' | 'alta' | 'critica'
export type EstadoIncidente =
  | 'registrado'
  | 'en_analisis'
  | 'contenido'
  | 'resuelto'
  | 'reportado'
  | 'cerrado'
export type EstadoCumplimiento = 'pendiente' | 'parcial' | 'cumple' | 'no_cumple'
export type TipoPersonaControl =
  | 'capacitacion'
  | 'antecedentes'
  | 'condiciones_empleo'
  | 'disciplinario'
  | 'termino_contrato'
  | 'confidencialidad'
export type TipoTicket = 'denuncia' | 'reporte_incidente'
export type EstadoTicket = 'registrado' | 'en_analisis' | 'derivado_a_incidente' | 'cerrado'
export type MedioNotificacion = 'correo' | 'bandeja'

export interface Usuario {
  id: number
  username: string
  nombre_completo: string
  rol: Role
  activo: boolean
}

export interface UsuarioCreate {
  username: string
  nombre_completo: string
  password: string
  rol: Role
}

export interface UsuarioUpdate {
  username?: string
  nombre_completo?: string
  rol?: Role
}

export interface AuditoriaOut {
  id: number
  actor_id: number
  actor_username: string
  usuario_objetivo_id: number
  usuario_objetivo_username: string
  accion: string
  detalle: string
  creado_en: string
}

export interface TicketAdjunto {
  id: number
  nombre_archivo: string
  mime: string
  tamano_bytes: number
}

export interface TicketOut {
  id: number
  codigo: string
  tipo: TipoTicket
  categoria: string
  categoria_otro: string | null
  severidad_percibida: Severidad
  estado: EstadoTicket
  sistema_area: string | null
  fecha_hecho_aprox: string | null
  notificar_correo: boolean
  notificar_bandeja: boolean
  canal_origen: string
  incidente_id: number | null
  creado_en: string
  actualizado_en: string
}

export interface TicketDetalle extends TicketOut {
  descripcion: string
  notas_internas: string | null
  adjuntos: TicketAdjunto[]
}

export interface TicketResumen {
  registrado: number
  en_analisis: number
  derivado_a_incidente: number
  cerrado: number
  pendientes: number
}

export interface CategoriaOption {
  value: string
  label: string
}

export interface TicketCatalogo {
  tipos: CategoriaOption[]
  categorias: CategoriaOption[]
  severidades: CategoriaOption[]
  medios: CategoriaOption[]
}

export interface PublicTicketResponse {
  codigo: string
  codigo_seguimiento: string
  estado: EstadoTicket
  mensaje: string
}

export interface TicketSeguimiento {
  codigo: string
  tipo: TipoTicket
  estado: EstadoTicket
  creado_en: string
  actualizado_en: string
}

export interface Notificacion {
  id: number
  ticket_id: number
  ticket_codigo: string
  tipo_ticket: TipoTicket
  severidad: Severidad
  medio: MedioNotificacion
  leida: boolean
  creado_en: string
}

export interface Incidente {
  id: number
  titulo: string
  descripcion: string
  categoria: string
  severidad: Severidad
  alcance: string
  sistema_afectado: string
  fecha_deteccion: string
  fecha_reporte: string | null
  estado: EstadoIncidente
  reportado_anci: boolean
  notas: string
  alerta_temprana: string
  plazo_reporte: string
  vencido: boolean
}

export interface Evidencia {
  id: number
  control_id: number
  tipo: string
  nombre: string
  descripcion: string
  archivo_path: string | null
  fecha_subida: string
}

export interface Control {
  id: number
  codigo: string
  titulo: string
  descripcion: string
  dominio: Dominio
  grupo: string
  estado: EstadoControl
  responsable: string
  notas: string
  fecha_actualizacion: string | null
  evidencias: Evidencia[]
}

export interface Clausula {
  nombre: string
  cumplida: boolean
}

export interface Tercero {
  id: number
  nombre: string
  rut: string
  tipo: string
  contrato_ref: string
  fecha_inicio: string | null
  fecha_termino: string | null
  contacto: string
  estado_cumplimiento: EstadoCumplimiento
  clausulas: Clausula[]
  notas: string
}

export interface PersonaControl {
  id: number
  tipo: TipoPersonaControl
  titulo: string
  descripcion: string
  estado: EstadoControl
  fecha: string | null
  responsable: string
  notas: string
}

export interface MadurezDominio {
  dominio: Dominio
  total: number
  estados: Record<string, number>
  pct: number
  gestionados: number
  implementados: number
}

export interface Madurez {
  global_pct: number
  total_controles: number
  dominios: MadurezDominio[]
}

export interface Resumen {
  total_controles: number
  por_estado: Record<string, number>
  madurez_global_pct: number
  total_incidentes: number
  incidentes_abiertos: number
  incidentes_vencidos: number
  total_terceros: number
  terceros_con_brechas: number
}
