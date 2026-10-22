import { useState, type FormEvent } from 'react'
import { Link, useSearchParams } from 'react-router-dom'
import PublicLayout from '../components/PublicLayout'
import Badge from '../components/Badge'
import { publicTicketsApi } from '../api'
import { ESTADO_TICKET_COLORS, ESTADO_TICKET_LABELS, TIPO_TICKET_LABELS } from '../constants'
import { fmtDate } from '../helpers'
import type { TicketSeguimiento } from '../types'

export default function SeguimientoTicket() {
  const [params] = useSearchParams()
  const [code, setCode] = useState(params.get('codigo') || '')
  const [ticket, setTicket] = useState<TicketSeguimiento | null>(null)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  async function lookup(event: FormEvent) {
    event.preventDefault()
    setTicket(null)
    setError('')
    if (!code.trim()) {
      setError('Ingresa el código privado de seguimiento.')
      return
    }
    setLoading(true)
    try {
      setTicket(await publicTicketsApi.track(code.trim()))
    } catch (err) {
      setError(err instanceof Error ? err.message : 'No se encontró un ticket con ese código.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <PublicLayout>
      <section className="public-form-card tracking-card">
        <span className="eyebrow">CONSULTA PRIVADA</span>
        <h2>Seguimiento de reporte</h2>
        <p>Ingresa el código de seguimiento que recibiste al enviar tu reporte. Por privacidad, no se muestra el contenido ni los adjuntos.</p>
        <form className="tracking-form" onSubmit={lookup}>
          <label className="field-label" htmlFor="tracking-code">Código de seguimiento</label>
          <div className="tracking-input-row"><input id="tracking-code" className="input mono" value={code} onChange={(event) => setCode(event.target.value)} autoComplete="off" required placeholder="Pega aquí tu código privado" /><button className="btn btn-primary" disabled={loading}>{loading ? 'Consultando…' : 'Consultar'}</button></div>
        </form>
        {error && <div className="alert alert-error" role="alert">{error}</div>}
        {ticket && <article className="tracking-result" aria-live="polite"><div className="card-head"><div><span className="detail-label">Código de ticket</span><strong className="mono tracking-ticket-code">{ticket.codigo}</strong></div><Badge color={ESTADO_TICKET_COLORS[ticket.estado]}>{ESTADO_TICKET_LABELS[ticket.estado]}</Badge></div><div className="tracking-meta"><div><span>Tipo</span><strong>{TIPO_TICKET_LABELS[ticket.tipo]}</strong></div><div><span>Recibido</span><strong>{fmtDate(ticket.creado_en)}</strong></div><div><span>Última actualización</span><strong>{fmtDate(ticket.actualizado_en)}</strong></div></div><p>El estado del reporte se actualiza a medida que el equipo de ciberseguridad lo revisa.</p></article>}
        <Link className="back-link" to="/reportar">← Volver al formulario de reporte</Link>
      </section>
    </PublicLayout>
  )
}
