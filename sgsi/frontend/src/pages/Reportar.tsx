import { useEffect, useState, type FormEvent } from 'react'
import PublicLayout from '../components/PublicLayout'
import { publicTicketsApi } from '../api'
import { fromLocalInput } from '../helpers'
import type { CategoriaOption, PublicTicketResponse, TicketCatalogo, TipoTicket } from '../types'

const ALLOWED_EXTENSIONS = ['.pdf', '.png', '.jpg', '.jpeg', '.txt', '.eml', '.msg', '.docx', '.xlsx', '.csv']
const FALLBACK_CATALOG: TicketCatalogo = {
  tipos: [{ value: 'denuncia', label: 'Denuncia' }, { value: 'reporte_incidente', label: 'Reporte de incidente' }],
  categorias: [
    { value: 'phishing', label: 'Phishing / correo sospechoso' },
    { value: 'malware_ransomware', label: 'Malware / Ransomware' },
    { value: 'acceso_no_autorizado', label: 'Acceso no autorizado' },
    { value: 'fuga_de_informacion', label: 'Fuga de información' },
    { value: 'uso_indebido_de_datos', label: 'Uso indebido de datos' },
    { value: 'falla_o_caida_de_servicio', label: 'Falla o caída de servicio' },
    { value: 'perdida_robo_de_equipo', label: 'Pérdida o robo de equipo' },
    { value: 'incumplimiento_de_politicas', label: 'Incumplimiento de políticas' },
    { value: 'otros', label: 'Otros (especificar)' },
  ],
  severidades: [{ value: 'baja', label: 'Baja' }, { value: 'media', label: 'Media' }, { value: 'alta', label: 'Alta' }, { value: 'critica', label: 'Crítica' }],
  medios: [{ value: 'correo', label: 'Correo electrónico' }, { value: 'bandeja', label: 'Bandeja interna' }],
}

function fileExtension(fileName: string) {
  return fileName.slice(fileName.lastIndexOf('.')).toLowerCase()
}

export default function Reportar() {
  const [catalog, setCatalog] = useState<TicketCatalogo>(FALLBACK_CATALOG)
  const [tipo, setTipo] = useState<TipoTicket>('denuncia')
  const [categoria, setCategoria] = useState('phishing')
  const [categoriaOtro, setCategoriaOtro] = useState('')
  const [descripcion, setDescripcion] = useState('')
  const [sistemaArea, setSistemaArea] = useState('')
  const [fechaAprox, setFechaAprox] = useState('')
  const [severidad, setSeveridad] = useState('media')
  const [notificarCorreo, setNotificarCorreo] = useState(false)
  const [notificarBandeja, setNotificarBandeja] = useState(true)
  const [files, setFiles] = useState<File[]>([])
  const [website, setWebsite] = useState('')
  const [response, setResponse] = useState<PublicTicketResponse | null>(null)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const [copied, setCopied] = useState(false)

  useEffect(() => { void publicTicketsApi.categories().then(setCatalog) }, [])

  function updateFiles(selected: FileList | null) {
    if (!selected) return
    const chosen = Array.from(selected)
    if (chosen.length > 5) {
      setError('Puedes adjuntar un máximo de 5 archivos.')
      return
    }
    const invalidType = chosen.find((file) => !ALLOWED_EXTENSIONS.includes(fileExtension(file.name)))
    if (invalidType) {
      setError(`El archivo ${invalidType.name} tiene una extensión no permitida. Tipos permitidos: ${ALLOWED_EXTENSIONS.join(', ')}.`)
      return
    }
    const oversized = chosen.find((file) => file.size > 10 * 1024 * 1024)
    if (oversized) {
      setError(`El archivo ${oversized.name} supera el límite de 10 MB.`)
      return
    }
    setFiles(chosen)
    setError('')
  }

  async function submitReport(event: FormEvent) {
    event.preventDefault()
    setError('')
    if (descripcion.trim().length < 20) {
      setError('Describe el hecho con al menos 20 caracteres.')
      return
    }
    if (categoria === 'otros' && !categoriaOtro.trim()) {
      setError('Indica una categoría para poder continuar.')
      return
    }
    if (!notificarCorreo && !notificarBandeja) {
      setError('Selecciona al menos un medio de notificación para el equipo de ciberseguridad.')
      return
    }
    setLoading(true)
    const form = new FormData()
    form.set('tipo', tipo)
    form.set('categoria', categoria)
    if (categoria === 'otros') form.set('categoria_otro', categoriaOtro.trim())
    form.set('descripcion', descripcion.trim())
    if (sistemaArea.trim()) form.set('sistema_area', sistemaArea.trim())
    const fechaHecho = fromLocalInput(fechaAprox)
    if (fechaHecho) form.set('fecha_hecho_aprox', fechaHecho)
    form.set('severidad_percibida', severidad)
    form.set('notificar_correo', String(notificarCorreo))
    form.set('notificar_bandeja', String(notificarBandeja))
    form.set('website', website)
    files.forEach((file) => form.append('archivos', file))
    try {
      setResponse(await publicTicketsApi.create(form))
    } catch (err) {
      setError(err instanceof Error ? err.message : 'No fue posible enviar el reporte. Intenta nuevamente.')
    } finally {
      setLoading(false)
    }
  }

  async function copyTrackingCode() {
    if (!response) return
    try {
      await navigator.clipboard.writeText(response.codigo_seguimiento)
      setCopied(true)
      window.setTimeout(() => setCopied(false), 2200)
    } catch {
      setCopied(false)
    }
  }

  function startNewReport() {
    setResponse(null)
    setTipo('denuncia')
    setCategoria('phishing')
    setCategoriaOtro('')
    setDescripcion('')
    setSistemaArea('')
    setFechaAprox('')
    setSeveridad('media')
    setNotificarCorreo(false)
    setNotificarBandeja(true)
    setFiles([])
  }

  if (response) return (
    <PublicLayout>
      <section className="public-form-card success-card">
        <span className="success-check" aria-hidden="true">✓</span>
        <span className="eyebrow">REPORTE RECIBIDO</span>
        <h2>Gracias por ayudar a protegernos.</h2>
        <p>{response.mensaje || 'Tu reporte fue recibido de forma confidencial por el equipo de ciberseguridad.'}</p>
        <div className="ticket-code-box"><span>Código de ticket</span><strong className="mono">{response.codigo}</strong></div>
        <div className="tracking-code-box"><div><span>Tu código privado de seguimiento</span><strong className="mono">{response.codigo_seguimiento}</strong></div><button className="btn btn-ghost" onClick={() => void copyTrackingCode()}>{copied ? 'Copiado ✓' : 'Copiar código'}</button></div>
        <div className="alert alert-info"><strong>Guarda este código.</strong> Es la única forma de consultar el estado de tu reporte; no podremos recuperarlo por identidad.</div>
        <div className="success-actions"><a className="btn btn-primary" href={`/reportar/seguimiento?codigo=${encodeURIComponent(response.codigo_seguimiento)}`}>Consultar seguimiento</a><button className="btn btn-ghost" onClick={startNewReport}>Enviar otro reporte</button></div>
      </section>
    </PublicLayout>
  )

  const categoryList: CategoriaOption[] = catalog.categorias.length ? catalog.categorias : FALLBACK_CATALOG.categorias
  return (
    <PublicLayout>
      <section className="public-form-card">
        <div className="public-form-heading"><span className="eyebrow">FORMULARIO CONFIDENCIAL</span><h2>Reportar un incidente o denuncia</h2><p>Completa los datos que conozcas. No necesitas identificarte.</p></div>
        <div className="anonymity-notice"><span className="anonymity-shield" aria-hidden="true">◉</span><div><strong>Tu identidad no será solicitada ni almacenada.</strong><p>Este canal no registra quién envía el reporte. El contenido será visible únicamente para el equipo de ciberseguridad.</p></div></div>
        <form className="public-form" onSubmit={submitReport}>
          <div className="form-grid">
            <div><label className="field-label" htmlFor="report-type">Tipo de reporte <span className="required-mark">*</span></label><select id="report-type" className="input" required value={tipo} onChange={(event) => setTipo(event.target.value as TipoTicket)}>{catalog.tipos.map((option) => <option value={option.value} key={option.value}>{option.label}</option>)}</select></div>
            <div><label className="field-label" htmlFor="report-category">Categoría <span className="required-mark">*</span></label><select id="report-category" className="input" required value={categoria} onChange={(event) => setCategoria(event.target.value)}>{categoryList.map((option) => <option value={option.value} key={option.value}>{option.label}</option>)}</select></div>
            {categoria === 'otros' && <div className="field-full"><label className="field-label" htmlFor="category-other">Especifica la categoría <span className="required-mark">*</span></label><input id="category-other" className="input" value={categoriaOtro} onChange={(event) => setCategoriaOtro(event.target.value)} required placeholder="Describe brevemente la categoría" /></div>}
            <div className="field-full"><label className="field-label" htmlFor="report-description">Descripción del hecho <span className="required-mark">*</span></label><textarea id="report-description" className="input report-description" minLength={20} maxLength={10000} required value={descripcion} onChange={(event) => setDescripcion(event.target.value)} placeholder="¿Qué ocurrió? Incluye detalles relevantes como mensajes, alertas o acciones observadas." /><span className="field-hint">Al menos 20 caracteres. No incluyas contraseñas ni datos personales innecesarios. ({descripcion.length}/10000)</span></div>
            <div><label className="field-label" htmlFor="system-area">Sistema o área afectada</label><input id="system-area" className="input" value={sistemaArea} onChange={(event) => setSistemaArea(event.target.value)} placeholder="Ej.: correo institucional, Urgencia" /></div>
            <div><label className="field-label" htmlFor="occurred-at">Fecha y hora aproximada</label><input id="occurred-at" className="input" type="datetime-local" value={fechaAprox} onChange={(event) => setFechaAprox(event.target.value)} /></div>
            <div><label className="field-label" htmlFor="severity">Severidad percibida <span className="required-mark">*</span></label><select id="severity" className="input" required value={severidad} onChange={(event) => setSeveridad(event.target.value)}>{catalog.severidades.map((option) => <option value={option.value} key={option.value}>{option.label}</option>)}</select></div>
            <div className="field-full"><span className="field-label">¿Cómo notificamos al equipo? <span className="required-mark">*</span></span><div className="notification-options">
              {catalog.medios.map((option) => <label className="checkbox" key={option.value}><input type="checkbox" checked={option.value === 'correo' ? notificarCorreo : notificarBandeja} onChange={(event) => option.value === 'correo' ? setNotificarCorreo(event.target.checked) : setNotificarBandeja(event.target.checked)} />{option.label}</label>)}
            </div><span className="field-hint">Selecciona al menos una opción. La notificación no incluirá la descripción ni adjuntos.</span></div>
            <div className="field-full"><label className="field-label" htmlFor="attachments">Archivos adjuntos <span className="optional-label">Opcional · máximo 5 archivos, 10 MB cada uno</span></label><input id="attachments" className="input file-input" type="file" multiple accept=".pdf,.png,.jpg,.jpeg,.txt,.eml,.msg,.docx,.xlsx,.csv" onChange={(event) => updateFiles(event.target.files)} /><span className="field-hint">Formatos permitidos: PDF, imágenes, texto, correo, Word, Excel y CSV.</span>{files.length > 0 && <ul className="selected-files">{files.map((file) => <li key={`${file.name}-${file.size}`}>{file.name}<span>{(file.size / (1024 * 1024)).toFixed(1)} MB</span></li>)}</ul>}</div>
          </div>
          <div className="honeypot" aria-hidden="true"><label htmlFor="website">Sitio web</label><input id="website" name="website" tabIndex={-1} autoComplete="off" value={website} onChange={(event) => setWebsite(event.target.value)} /></div>
          {error && <div className="alert alert-error" role="alert">{error}</div>}
          <div className="public-submit-row"><p><span aria-hidden="true">▣</span> Envío cifrado y confidencial</p><button className="btn btn-primary" disabled={loading}>{loading ? <><span className="loader loader-small" />Enviando…</> : <>Enviar reporte <span aria-hidden="true">→</span></>}</button></div>
        </form>
      </section>
      <div className="public-help"><span>¿Ya enviaste un reporte?</span><a href="/reportar/seguimiento">Consulta su estado con tu código de seguimiento →</a></div>
    </PublicLayout>
  )
}
