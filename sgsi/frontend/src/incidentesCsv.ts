import type { EstadoIncidente, Severidad } from './types'

export interface IncidenteCsvFila {
  numero: number
  titulo: string
  descripcion: string
  categoria: string
  severidad: Severidad
  alcance: string
  sistema_afectado: string
  fecha_deteccion: string
  estado: EstadoIncidente
  reportado_anci: boolean
  notas: string
}

export interface IncidenteCsvError {
  numero: number
  mensaje: string
}

export interface IncidenteCsvParseResult {
  filas: IncidenteCsvFila[]
  errores: IncidenteCsvError[]
}

const COLUMNAS = [
  'titulo',
  'descripcion',
  'categoria',
  'severidad',
  'alcance',
  'sistema_afectado',
  'fecha_deteccion',
  'estado',
  'reportado_anci',
  'notas',
]

const COLUMNAS_OBLIGATORIAS = ['titulo', 'severidad', 'fecha_deteccion']

const SEVERIDADES_CSV: Severidad[] = ['baja', 'media', 'alta', 'critica']
const ALCANCES_CSV = ['interno', 'externo', 'proveedor']
const ESTADOS_CSV: EstadoIncidente[] = [
  'registrado',
  'en_analisis',
  'contenido',
  'resuelto',
  'reportado',
  'cerrado',
]

/** Normaliza un encabezado o valor enumerado: sin tildes, minúsculas y separadores a "_". */
function normalizar(valor: string): string {
  return valor
    .normalize('NFD')
    .replace(/\p{Diacritic}/gu, '')
    .toLowerCase()
    .trim()
    .replace(/[\s-]+/g, '_')
}

function esBisiesto(anio: number): boolean {
  return (anio % 4 === 0 && anio % 100 !== 0) || anio % 400 === 0
}

function fechaValida(anio: number, mes: number, dia: number, hora: number, min: number, seg: number): boolean {
  if (anio < 1900 || anio > 2100) return false
  if (mes < 1 || mes > 12) return false
  if (hora < 0 || hora > 23 || min < 0 || min > 59 || seg < 0 || seg > 59) return false
  const diasPorMes = [31, esBisiesto(anio) ? 29 : 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
  return dia >= 1 && dia <= diasPorMes[mes - 1]
}

function parseFecha(valor: string): string | null {
  const v = valor.trim()
  if (!v) return null
  const soloFecha = /^(\d{4})-(\d{2})-(\d{2})$/.exec(v)
  if (soloFecha) {
    const [, a, m, d] = soloFecha
    if (!fechaValida(Number(a), Number(m), Number(d), 0, 0, 0)) return null
    return `${a}-${m}-${d}T00:00:00`
  }
  const conHora = /^(\d{4})-(\d{2})-(\d{2})[ T](\d{2}):(\d{2})(?::(\d{2}))?$/.exec(v)
  if (conHora) {
    const [, a, m, d, h, min, s = '00'] = conHora
    if (!fechaValida(Number(a), Number(m), Number(d), Number(h), Number(min), Number(s))) return null
    return `${a}-${m}-${d}T${h}:${min}:${s}`
  }
  return null
}

function parseBooleano(valor: string): boolean | null {
  const v = normalizar(valor)
  if (!v) return false
  if (['si', 'yes', 'true', '1', 'verdadero'].includes(v)) return true
  if (['no', 'false', '0', 'falso'].includes(v)) return false
  return null
}

/** Parser CSV tolerante a comillas, comas y saltos de línea dentro de campos. */
function parseCsv(texto: string): string[][] {
  const filas: string[][] = []
  let fila: string[] = []
  let campo = ''
  let enComillas = false
  let i = texto.charCodeAt(0) === 0xfeff ? 1 : 0

  while (i < texto.length) {
    const ch = texto[i]
    if (enComillas) {
      if (ch === '"') {
        if (texto[i + 1] === '"') {
          campo += '"'
          i += 2
          continue
        }
        enComillas = false
        i += 1
        continue
      }
      campo += ch
      i += 1
      continue
    }
    if (ch === '"') {
      enComillas = true
      i += 1
      continue
    }
    if (ch === ',') {
      fila.push(campo)
      campo = ''
      i += 1
      continue
    }
    if (ch === '\r') {
      i += 1
      continue
    }
    if (ch === '\n') {
      fila.push(campo)
      filas.push(fila)
      fila = []
      campo = ''
      i += 1
      continue
    }
    campo += ch
    i += 1
  }
  if (campo !== '' || fila.length > 0) {
    fila.push(campo)
    filas.push(fila)
  }
  return filas
}

export function parseIncidentesCsv(texto: string): IncidenteCsvParseResult {
  const errores: IncidenteCsvError[] = []
  if (!texto.trim()) {
    return { filas: [], errores: [{ numero: 0, mensaje: 'El archivo está vacío.' }] }
  }

  const filas = parseCsv(texto).filter((f) => f.some((c) => c.trim() !== ''))
  if (filas.length === 0) {
    return { filas: [], errores: [{ numero: 0, mensaje: 'El archivo no contiene datos.' }] }
  }

  const columna: Record<string, number> = {}
  filas[0].forEach((h, idx) => {
    const nombre = normalizar(h)
    if (nombre && !(nombre in columna)) columna[nombre] = idx
  })

  for (const obligatoria of COLUMNAS_OBLIGATORIAS) {
    if (!(obligatoria in columna)) {
      errores.push({ numero: 0, mensaje: `Falta la columna obligatoria «${obligatoria}».` })
    }
  }
  if (errores.length > 0) return { filas: [], errores }

  const resultado: IncidenteCsvFila[] = []
  for (let i = 1; i < filas.length; i += 1) {
    const campos = filas[i]
    const numero = i + 1
    const get = (nombre: string): string => {
      const idx = columna[nombre]
      return idx !== undefined && idx < campos.length ? campos[idx].trim() : ''
    }
    const erroresFila: string[] = []

    const titulo = get('titulo')
    if (!titulo) erroresFila.push('El título es obligatorio.')

    const severidadRaw = get('severidad')
    let severidad: Severidad = 'media'
    if (!severidadRaw) {
      erroresFila.push('La severidad es obligatoria.')
    } else {
      const s = normalizar(severidadRaw)
      if (SEVERIDADES_CSV.includes(s as Severidad)) severidad = s as Severidad
      else erroresFila.push(`Severidad inválida «${severidadRaw}» (valores: ${SEVERIDADES_CSV.join(', ')}).`)
    }

    const alcanceRaw = get('alcance')
    let alcance = 'interno'
    if (alcanceRaw) {
      const a = normalizar(alcanceRaw)
      if (ALCANCES_CSV.includes(a)) alcance = a
      else erroresFila.push(`Alcance inválido «${alcanceRaw}» (valores: ${ALCANCES_CSV.join(', ')}).`)
    }

    const estadoRaw = get('estado')
    let estado: EstadoIncidente = 'registrado'
    if (estadoRaw) {
      const e = normalizar(estadoRaw)
      if (ESTADOS_CSV.includes(e as EstadoIncidente)) estado = e as EstadoIncidente
      else erroresFila.push(`Estado inválido «${estadoRaw}» (valores: ${ESTADOS_CSV.join(', ')}).`)
    }

    const fechaRaw = get('fecha_deteccion')
    let fechaDeteccion = ''
    if (!fechaRaw) {
      erroresFila.push('La fecha de detección es obligatoria.')
    } else {
      const f = parseFecha(fechaRaw)
      if (f) fechaDeteccion = f
      else erroresFila.push(`Fecha de detección inválida «${fechaRaw}» (use AAAA-MM-DD o AAAA-MM-DD HH:MM).`)
    }

    const reportadoRaw = get('reportado_anci')
    let reportadoAnci = false
    if (reportadoRaw) {
      const b = parseBooleano(reportadoRaw)
      if (b === null) erroresFila.push(`Valor inválido para reportado_anci «${reportadoRaw}» (use SI/NO, true/false o 1/0).`)
      else reportadoAnci = b
    }

    if (erroresFila.length > 0) {
      errores.push({ numero, mensaje: erroresFila.join(' ') })
    } else {
      resultado.push({
        numero,
        titulo,
        descripcion: get('descripcion'),
        categoria: get('categoria'),
        severidad,
        alcance,
        sistema_afectado: get('sistema_afectado'),
        fecha_deteccion: fechaDeteccion,
        estado,
        reportado_anci: reportadoAnci,
        notas: get('notas'),
      })
    }
  }

  return { filas: resultado, errores }
}

export function toIncidentePayload(fila: IncidenteCsvFila) {
  return {
    titulo: fila.titulo,
    descripcion: fila.descripcion,
    categoria: fila.categoria,
    severidad: fila.severidad,
    alcance: fila.alcance,
    sistema_afectado: fila.sistema_afectado,
    fecha_deteccion: fila.fecha_deteccion,
    estado: fila.estado,
    reportado_anci: fila.reportado_anci,
    notas: fila.notas,
  }
}

function csvEscape(valor: string): string {
  return /[",\r\n]/.test(valor) ? `"${valor.replace(/"/g, '""')}"` : valor
}

const PLANTILLA_FILAS: string[][] = [
  COLUMNAS,
  [
    'Campaña de phishing detectada en correo institucional',
    'Varios funcionarios reportaron correos con enlaces maliciosos y solicitud de credenciales.',
    'phishing',
    'alta',
    'interno',
    'Correo institucional',
    '2026-10-28 09:15',
    'registrado',
    'NO',
    'Ejemplo de plantilla',
  ],
  [
    'Acceso no autorizado a sistema de fichas clínicas',
    '',
    '',
    'critica',
    '',
    'Sistema de fichas clínicas',
    '2026-10-28',
    '',
    'NO',
    '',
  ],
]

export function plantillaIncidentesCsv(): string {
  return '\ufeff' + PLANTILLA_FILAS.map((f) => f.map(csvEscape).join(',')).join('\r\n')
}

export function descargarPlantillaIncidentes(): void {
  const blob = new Blob([plantillaIncidentesCsv()], { type: 'text/csv;charset=utf-8' })
  const url = URL.createObjectURL(blob)
  const anchor = document.createElement('a')
  anchor.href = url
  anchor.download = 'plantilla_incidentes.csv'
  document.body.appendChild(anchor)
  anchor.click()
  anchor.remove()
  URL.revokeObjectURL(url)
}
