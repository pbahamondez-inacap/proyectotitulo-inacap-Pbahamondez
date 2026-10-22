import type {
  AuditoriaOut,
  CategoriaOption,
  EstadoTicket,
  Notificacion,
  PublicTicketResponse,
  Role,
  Severidad,
  TicketCatalogo,
  TicketDetalle,
  TicketOut,
  TicketResumen,
  TicketSeguimiento,
  Usuario,
  UsuarioCreate,
  UsuarioUpdate,
} from './types'

const TOKEN_KEY = 'sgsi_token'
const PUBLIC_CATEGORIAS: CategoriaOption[] = [
  { value: 'phishing', label: 'Phishing / correo sospechoso' },
  { value: 'malware_ransomware', label: 'Malware / Ransomware' },
  { value: 'acceso_no_autorizado', label: 'Acceso no autorizado' },
  { value: 'fuga_de_informacion', label: 'Fuga de información' },
  { value: 'uso_indebido_de_datos', label: 'Uso indebido de datos' },
  { value: 'falla_o_caida_de_servicio', label: 'Falla o caída de servicio' },
  { value: 'perdida_robo_de_equipo', label: 'Pérdida o robo de equipo' },
  { value: 'incumplimiento_de_politicas', label: 'Incumplimiento de políticas' },
  { value: 'otros', label: 'Otros (especificar)' },
]

export function getToken(): string | null {
  return localStorage.getItem(TOKEN_KEY)
}

export function setToken(token: string | null): void {
  if (token) localStorage.setItem(TOKEN_KEY, token)
  else localStorage.removeItem(TOKEN_KEY)
}

function getErrorMessage(json: unknown, statusText: string): string {
  if (json && typeof json === 'object' && 'detail' in json) {
    const detail = (json as { detail?: unknown }).detail
    return typeof detail === 'string' ? detail : JSON.stringify(detail)
  }
  return statusText || 'Error de comunicación con el servidor'
}

async function parseResponse<T>(res: Response): Promise<T> {
  if (res.status === 204) return null as T
  return (await res.json()) as T
}

async function request<T = unknown>(path: string, options: RequestInit = {}): Promise<T> {
  const headers: Record<string, string> = { ...(options.headers as Record<string, string> | undefined) }
  const token = getToken()
  if (token) headers.Authorization = `Bearer ${token}`

  const res = await fetch(`/api${path}`, { ...options, headers })
  if (res.status === 401 && path !== '/auth/login') {
    setToken(null)
    if (!window.location.pathname.startsWith('/login')) window.location.href = '/login'
    throw new Error('Sesión expirada')
  }
  if (!res.ok) {
    let message = res.statusText
    try {
      message = getErrorMessage(await res.json(), res.statusText)
    } catch {
      // El servidor puede responder sin cuerpo JSON.
    }
    throw new Error(message)
  }
  return parseResponse<T>(res)
}

async function publicRequest<T = unknown>(path: string, options: RequestInit = {}): Promise<T> {
  const headers: Record<string, string> = { ...(options.headers as Record<string, string> | undefined) }
  for (const key of Object.keys(headers)) {
    if (key.toLowerCase() === 'authorization') delete headers[key]
  }
  const res = await fetch(`/api${path}`, { ...options, headers, credentials: 'omit' })
  if (!res.ok) {
    let message = res.statusText
    try {
      message = getErrorMessage(await res.json(), res.statusText)
    } catch {
      // El servidor puede responder sin cuerpo JSON.
    }
    throw new Error(message)
  }
  return parseResponse<T>(res)
}

async function downloadFile(path: string, filename: string): Promise<void> {
  const headers: Record<string, string> = {}
  const token = getToken()
  if (token) headers.Authorization = `Bearer ${token}`
  const res = await fetch(`/api${path}`, { headers })
  if (!res.ok) throw new Error('Error al descargar el archivo')
  const blob = await res.blob()
  const url = URL.createObjectURL(blob)
  const anchor = document.createElement('a')
  anchor.href = url
  anchor.download = filename
  document.body.appendChild(anchor)
  anchor.click()
  anchor.remove()
  URL.revokeObjectURL(url)
}

export const api = {
  get: <T = unknown>(path: string) => request<T>(path),
  post: <T = unknown>(path: string, body?: unknown) =>
    request<T>(path, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: body === undefined ? undefined : JSON.stringify(body),
    }),
  put: <T = unknown>(path: string, body?: unknown) =>
    request<T>(path, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: body === undefined ? undefined : JSON.stringify(body),
    }),
  patch: <T = unknown>(path: string, body?: unknown) =>
    request<T>(path, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: body === undefined ? undefined : JSON.stringify(body),
    }),
  del: <T = unknown>(path: string) => request<T>(path, { method: 'DELETE' }),
  upload: <T = unknown>(path: string, form: FormData) => request<T>(path, { method: 'POST', body: form }),
  publicGet: <T = unknown>(path: string) => publicRequest<T>(path),
  publicUpload: <T = unknown>(path: string, form: FormData) =>
    publicRequest<T>(path, { method: 'POST', body: form }),
  download: downloadFile,
}

export const usuariosApi = {
  list: () => api.get<Usuario[]>('/usuarios'),
  create: (payload: UsuarioCreate) => api.post<Usuario>('/usuarios', payload),
  get: (id: number) => api.get<Usuario>(`/usuarios/${id}`),
  update: (id: number, payload: UsuarioUpdate) => api.put<Usuario>(`/usuarios/${id}`, payload),
  setActive: (id: number, activo: boolean) => api.patch<Usuario>(`/usuarios/${id}/estado`, { activo }),
  resetPassword: (id: number, password: string) => api.post<Usuario>(`/usuarios/${id}/reset-password`, { password }),
  audit: () => api.get<AuditoriaOut[]>('/usuarios/auditoria'),
}

export const ticketsApi = {
  list: (query = '') => api.get<TicketOut[]>(`/tickets${query ? `?${query}` : ''}`),
  get: (id: number) => api.get<TicketDetalle>(`/tickets/${id}`),
  summary: () => api.get<TicketResumen>('/tickets/resumen'),
  changeState: (id: number, estado: EstadoTicket, notas_internas?: string) =>
    api.patch<TicketDetalle>(`/tickets/${id}/estado`, { estado, notas_internas }),
  convertToIncident: (id: number, payload: { categoria_anci?: string; severidad?: Severidad; alcance?: string }) =>
    api.post(`/tickets/${id}/convertir-incidente`, payload),
  downloadAttachment: (id: number, adjuntoId: number, filename: string) =>
    api.download(`/tickets/${id}/adjuntos/${adjuntoId}`, filename),
}

export const notificacionesApi = {
  list: (soloNoLeidas = true) => api.get<Notificacion[]>(`/notificaciones?solo_no_leidas=${soloNoLeidas}`),
  pendingCount: () => api.get<{ count: number }>('/notificaciones/pendientes/count'),
  markRead: (id: number) => api.post<Notificacion>(`/notificaciones/${id}/leer`),
}

export const publicTicketsApi = {
  categories: async (): Promise<TicketCatalogo> => {
    try {
      return await api.publicGet<TicketCatalogo>('/public/tickets/categorias')
    } catch {
      return {
        tipos: [
          { value: 'denuncia', label: 'Denuncia' },
          { value: 'reporte_incidente', label: 'Reporte de incidente' },
        ],
        categorias: PUBLIC_CATEGORIAS,
        severidades: [
          { value: 'baja', label: 'Baja' },
          { value: 'media', label: 'Media' },
          { value: 'alta', label: 'Alta' },
          { value: 'critica', label: 'Crítica' },
        ],
        medios: [
          { value: 'correo', label: 'Correo electrónico' },
          { value: 'bandeja', label: 'Bandeja interna' },
        ],
      }
    }
  },
  create: (form: FormData) => api.publicUpload<PublicTicketResponse>('/public/tickets', form),
  track: (codigoSeguimiento: string) =>
    api.publicGet<TicketSeguimiento>(`/public/tickets/${encodeURIComponent(codigoSeguimiento)}`),
}

export type { Role }
