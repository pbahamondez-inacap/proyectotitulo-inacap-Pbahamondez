import { useCallback, useEffect, useMemo, useState, type FormEvent } from 'react'
import Badge from '../components/Badge'
import Modal from '../components/Modal'
import { notificacionesApi, ticketsApi } from '../api'
import { ALCANCE_OPCIONES, CATEGORIAS_INCIDENTE, CATEGORIA_TICKET_LABELS, ESTADO_TICKET_COLORS, ESTADO_TICKET_LABELS, SEVERIDAD_COLORS, SEVERIDAD_LABELS, TIPO_TICKET_LABELS } from '../constants'
import { fmtDate } from '../helpers'
import type { EstadoTicket, Notificacion, Severidad, TicketDetalle, TicketOut, TicketResumen } from '../types'

const FILTER_STATES: EstadoTicket[] = ['registrado', 'en_analisis', 'derivado_a_incidente', 'cerrado']

function readable(value: string | null | undefined) {
  return value ? value.replace(/_/g, ' ') : '—'
}
function prettySize(bytes: number) {
  return bytes < 1024 * 1024 ? `${Math.max(1, Math.round(bytes / 1024))} KB` : `${(bytes / (1024 * 1024)).toFixed(1)} MB`
}

export default function Tickets() {
  const [tickets, setTickets] = useState<TicketOut[]>([])
  const [summary, setSummary] = useState<TicketResumen | null>(null)
  const [notifications, setNotifications] = useState<Notificacion[]>([])
  const [statusFilter, setStatusFilter] = useState('')
  const [typeFilter, setTypeFilter] = useState('')
  const [severityFilter, setSeverityFilter] = useState('')
  const [search, setSearch] = useState('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [detail, setDetail] = useState<TicketDetalle | null>(null)
  const [detailLoading, setDetailLoading] = useState(false)
  const [notes, setNotes] = useState('')
  const [nextState, setNextState] = useState<EstadoTicket>('en_analisis')
  const [savingState, setSavingState] = useState(false)
  const [converting, setConverting] = useState(false)
  const [categoryAnci, setCategoryAnci] = useState(CATEGORIAS_INCIDENTE[0])
  const [severity, setSeverity] = useState<Severidad>('media')
  const [scope, setScope] = useState('interno')
  const [notificationLoading, setNotificationLoading] = useState(false)

  const query = useMemo(() => {
    const params = new URLSearchParams()
    if (statusFilter) params.set('estado', statusFilter)
    if (typeFilter) params.set('tipo', typeFilter)
    if (severityFilter) params.set('severidad', severityFilter)
    if (search.trim()) params.set('q', search.trim())
    return params.toString()
  }, [statusFilter, typeFilter, severityFilter, search])

  const loadTickets = useCallback(async () => {
    setLoading(true)
    setError('')
    try {
      const [items, totals] = await Promise.all([ticketsApi.list(query), ticketsApi.summary()])
      setTickets(items)
      setSummary(totals)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'No fue posible cargar la ticketera')
    } finally {
      setLoading(false)
    }
  }, [query])

  const loadNotifications = useCallback(async () => {
    setNotificationLoading(true)
    try {
      setNotifications(await notificacionesApi.list(true))
    } catch {
      setNotifications([])
    } finally {
      setNotificationLoading(false)
    }
  }, [])

  useEffect(() => { void loadTickets() }, [loadTickets])
  useEffect(() => {
    void loadNotifications()
    const timer = window.setInterval(() => void loadNotifications(), 60_000)
    return () => window.clearInterval(timer)
  }, [loadNotifications])

  async function openDetail(ticket: TicketOut | number) {
    setDetailLoading(true)
    setDetail(null)
    setError('')
    try {
      const result = await ticketsApi.get(typeof ticket === 'number' ? ticket : ticket.id)
      setDetail(result)
      setNotes(result.notas_internas || '')
      setNextState(result.estado === 'registrado' ? 'en_analisis' : 'cerrado')
    } catch (err) {
      setError(err instanceof Error ? err.message : 'No fue posible abrir el detalle del ticket')
    } finally {
      setDetailLoading(false)
    }
  }

  async function updateState(event: FormEvent) {
    event.preventDefault()
    if (!detail) return
    setSavingState(true)
    setError('')
    try {
      await ticketsApi.changeState(detail.id, nextState, notes)
      setDetail(await ticketsApi.get(detail.id))
      await loadTickets()
    } catch (err) {
      setError(err instanceof Error ? err.message : 'No fue posible cambiar el estado')
    } finally {
      setSavingState(false)
    }
  }

  async function convertToIncident() {
    if (!detail) return
    setConverting(true)
    setError('')
    try {
      await ticketsApi.convertToIncident(detail.id, { categoria_anci: categoryAnci, severidad: severity, alcance: scope })
      setDetail(null)
      await loadTickets()
    } catch (err) {
      setError(err instanceof Error ? err.message : 'No fue posible convertir el ticket en incidente')
    } finally {
      setConverting(false)
    }
  }

  async function markRead(notification: Notificacion) {
    try {
      await notificacionesApi.markRead(notification.id)
      setNotifications((current) => current.filter((item) => item.id !== notification.id))
      window.dispatchEvent(new Event('sgsi:refresh-notification-count'))
    } catch (err) {
      setError(err instanceof Error ? err.message : 'No fue posible marcar la notificación como leída')
    }
  }

  const allowedNextStates: EstadoTicket[] = detail?.estado === 'registrado' ? ['en_analisis'] : detail?.estado === 'en_analisis' ? ['cerrado'] : []
  const summaries = [
    { key: 'registrado', label: 'Registrados', value: summary?.registrado ?? 0, icon: '◷' },
    { key: 'en_analisis', label: 'En análisis', value: summary?.en_analisis ?? 0, icon: '⌕' },
    { key: 'derivado_a_incidente', label: 'Derivados', value: summary?.derivado_a_incidente ?? 0, icon: '↗' },
    { key: 'cerrado', label: 'Cerrados', value: summary?.cerrado ?? 0, icon: '✓' },
  ]

  return (
    <div className="page-stack">
      <div className="page-heading">
        <div><span className="eyebrow">GESTIÓN DE CIBERSEGURIDAD</span><h2>Ticketera</h2><p>Revisa denuncias y reportes recibidos de forma confidencial.</p></div>
        <button className="btn btn-ghost" onClick={() => { void loadTickets(); void loadNotifications() }}><span aria-hidden="true">↻</span> Actualizar</button>
      </div>
      <section className="ticket-kpis" aria-label="Resumen de tickets">
        {summaries.map((item) => <button key={item.key} className={`ticket-kpi${statusFilter === item.key ? ' selected' : ''}`} onClick={() => setStatusFilter(statusFilter === item.key ? '' : item.key)}>
          <span className="ticket-kpi-icon" aria-hidden="true">{item.icon}</span><span className="ticket-kpi-value">{item.value}</span><span className="ticket-kpi-label">{item.label}</span>
        </button>)}
        <div className="ticket-kpi ticket-kpi-pending"><span className="ticket-kpi-icon" aria-hidden="true">!</span><span className="ticket-kpi-value">{summary?.pendientes ?? 0}</span><span className="ticket-kpi-label">Pendientes de revisión</span></div>
      </section>
      {error && <div className="alert alert-error" role="alert">{error}</div>}
      <div className="tickets-layout">
        <section className="card table-card tickets-main">
          <div className="toolbar">
            <div><h3 className="card-title">Bandeja de tickets</h3><p className="text-muted">Contenido restringido al equipo de ciberseguridad.</p></div>
            <div className="filters">
              <label className="search-box"><span aria-hidden="true">⌕</span><input className="input" value={search} onChange={(event) => setSearch(event.target.value)} placeholder="Buscar código o área" aria-label="Buscar tickets" /></label>
              <select className="input" aria-label="Filtrar por estado" value={statusFilter} onChange={(event) => setStatusFilter(event.target.value)}><option value="">Todos los estados</option>{FILTER_STATES.map((state) => <option key={state} value={state}>{ESTADO_TICKET_LABELS[state]}</option>)}</select>
              <select className="input" aria-label="Filtrar por tipo" value={typeFilter} onChange={(event) => setTypeFilter(event.target.value)}><option value="">Todos los tipos</option><option value="denuncia">Denuncia</option><option value="reporte_incidente">Reporte de incidente</option></select>
              <select className="input" aria-label="Filtrar por severidad" value={severityFilter} onChange={(event) => setSeverityFilter(event.target.value)}><option value="">Todas las severidades</option>{Object.entries(SEVERIDAD_LABELS).map(([key, label]) => <option key={key} value={key}>{label}</option>)}</select>
            </div>
          </div>
          {loading ? <div className="loading-inline"><span className="loader" />Cargando tickets…</div> : <div className="table-wrap"><table className="table">
            <thead><tr><th>Código y categoría</th><th>Tipo</th><th>Severidad</th><th>Estado</th><th>Fecha</th><th /></tr></thead>
            <tbody>{tickets.map((ticket) => <tr key={ticket.id}>
              <td><strong className="mono">{ticket.codigo}</strong><small className="cell-sub">{ticket.categoria === 'otros' ? ticket.categoria_otro : CATEGORIA_TICKET_LABELS[ticket.categoria] || readable(ticket.categoria)}</small></td>
              <td>{TIPO_TICKET_LABELS[ticket.tipo]}</td>
              <td><Badge color={SEVERIDAD_COLORS[ticket.severidad_percibida]}>{SEVERIDAD_LABELS[ticket.severidad_percibida]}</Badge></td>
              <td><Badge color={ESTADO_TICKET_COLORS[ticket.estado]}>{ESTADO_TICKET_LABELS[ticket.estado]}</Badge></td>
              <td className="text-muted">{fmtDate(ticket.creado_en)}</td>
              <td><button className="btn btn-ghost btn-sm" onClick={() => void openDetail(ticket)}>Ver detalle <span aria-hidden="true">→</span></button></td>
            </tr>)}
              {tickets.length === 0 && <tr><td colSpan={6} className="empty-row"><span className="empty-icon">▣</span><strong>Sin tickets por mostrar</strong><small>Los reportes recibidos aparecerán en esta bandeja.</small></td></tr>}
            </tbody>
          </table></div>}
        </section>
        <aside className="card notification-panel">
          <div className="card-head"><div><h3 className="card-title">Notificaciones</h3><p className="text-muted">Pendientes de lectura</p></div><span className="notification-counter">{notifications.length}</span></div>
          {notificationLoading && notifications.length === 0 ? <div className="loading-inline"><span className="loader" /></div> : notifications.length > 0 ? <div className="notification-list">{notifications.map((notification) => <article className="notification-item" key={notification.id}>
            <span className="notification-dot" aria-hidden="true" /><div className="notification-copy"><strong>{notification.ticket_codigo}</strong><small>{TIPO_TICKET_LABELS[notification.tipo_ticket]} · {SEVERIDAD_LABELS[notification.severidad]}</small><small>{fmtDate(notification.creado_en)} · {notification.medio === 'correo' ? 'Correo' : 'Bandeja'}</small></div>
            <div className="notification-actions"><button className="icon-btn" aria-label={`Abrir ticket ${notification.ticket_codigo}`} onClick={() => { void openDetail(notification.ticket_id) }}>↗</button><button className="icon-btn" aria-label={`Marcar ${notification.ticket_codigo} como leído`} onClick={() => void markRead(notification)}>✓</button></div>
          </article>)}</div> : <div className="empty-state compact"><span className="empty-icon">✓</span><strong>Estás al día</strong><small>No hay notificaciones sin leer.</small></div>}
        </aside>
      </div>

      <Modal open={detailLoading || !!detail} onClose={() => setDetail(null)} title={detail ? `Ticket ${detail.codigo}` : 'Detalle del ticket'} wide>
        {detailLoading ? <div className="loading-inline"><span className="loader" />Cargando detalle…</div> : detail && <div className="ticket-detail">
          <div className="ticket-detail-summary"><Badge color={ESTADO_TICKET_COLORS[detail.estado]}>{ESTADO_TICKET_LABELS[detail.estado]}</Badge><Badge color={SEVERIDAD_COLORS[detail.severidad_percibida]}>{SEVERIDAD_LABELS[detail.severidad_percibida]}</Badge><span>{TIPO_TICKET_LABELS[detail.tipo]}</span><span className="text-muted">{fmtDate(detail.creado_en)}</span></div>
          <div className="ticket-detail-grid">
            <div><span className="detail-label">Categoría</span><strong>{detail.categoria === 'otros' ? detail.categoria_otro : CATEGORIA_TICKET_LABELS[detail.categoria] || readable(detail.categoria)}</strong></div>
            <div><span className="detail-label">Sistema o área</span><strong>{detail.sistema_area || 'No indicado'}</strong></div>
            <div><span className="detail-label">Fecha aproximada del hecho</span><strong>{fmtDate(detail.fecha_hecho_aprox)}</strong></div>
            <div><span className="detail-label">Canal</span><strong>{detail.canal_origen === 'publico' ? 'Formulario público' : readable(detail.canal_origen)}</strong></div>
          </div>
          <section className="detail-section"><h4>Descripción del reporte</h4><p className="ticket-description">{detail.descripcion}</p></section>
          <section className="detail-section"><h4>Archivos adjuntos <span className="detail-count">{detail.adjuntos.length}</span></h4>{detail.adjuntos.length ? <ul className="attachment-list">{detail.adjuntos.map((file) => <li key={file.id}><span className="attachment-icon" aria-hidden="true">▤</span><span><strong>{file.nombre_archivo}</strong><small>{file.mime} · {prettySize(file.tamano_bytes)}</small></span><button className="btn btn-ghost btn-sm" onClick={() => void ticketsApi.downloadAttachment(detail.id, file.id, file.nombre_archivo)}>Descargar</button></li>)}</ul> : <p className="text-muted">No se adjuntaron archivos.</p>}</section>
          {detail.incidente_id && <div className="alert alert-info">Este ticket ya fue convertido al incidente #{detail.incidente_id}.</div>}
          {allowedNextStates.length > 0 && <form className="detail-section state-form" onSubmit={updateState}><h4>Actualizar seguimiento</h4><div className="form-grid"><div><label className="field-label" htmlFor="next-state">Cambiar estado</label><select id="next-state" className="input" value={nextState} onChange={(event) => setNextState(event.target.value as EstadoTicket)}>{allowedNextStates.map((state) => <option key={state} value={state}>{ESTADO_TICKET_LABELS[state]}</option>)}</select></div><div className="field-full"><label className="field-label" htmlFor="internal-notes">Notas internas (solo equipo SGSI)</label><textarea id="internal-notes" className="input" rows={3} value={notes} onChange={(event) => setNotes(event.target.value)} placeholder="Registra acciones o contexto de seguimiento" /></div></div><button className="btn btn-primary" disabled={savingState}>{savingState ? 'Guardando…' : 'Guardar actualización'}</button></form>}
          {detail.estado !== 'cerrado' && detail.estado !== 'derivado_a_incidente' && !detail.incidente_id && <section className="detail-section convert-panel"><div><h4>Convertir en incidente formal</h4><p>Clasifica el caso según la taxonomía ANCI para iniciar el flujo de gestión legal.</p></div><div className="form-grid"><div><label className="field-label" htmlFor="anci-category">Categoría ANCI</label><select id="anci-category" className="input" value={categoryAnci} onChange={(event) => setCategoryAnci(event.target.value)}>{CATEGORIAS_INCIDENTE.map((category) => <option key={category} value={category}>{readable(category)}</option>)}</select></div><div><label className="field-label" htmlFor="incident-severity">Severidad</label><select id="incident-severity" className="input" value={severity} onChange={(event) => setSeverity(event.target.value as Severidad)}>{Object.entries(SEVERIDAD_LABELS).map(([key, label]) => <option key={key} value={key}>{label}</option>)}</select></div><div><label className="field-label" htmlFor="incident-scope">Alcance</label><select id="incident-scope" className="input" value={scope} onChange={(event) => setScope(event.target.value)}>{ALCANCE_OPCIONES.map((item) => <option key={item} value={item}>{readable(item)}</option>)}</select></div><div className="field-full"><button className="btn btn-primary" onClick={() => void convertToIncident()} disabled={converting}>{converting ? 'Convirtiendo…' : 'Convertir en incidente'}</button></div></div></section>}
          {error && <div className="alert alert-error" role="alert">{error}</div>}
        </div>}
      </Modal>
    </div>
  )
}
