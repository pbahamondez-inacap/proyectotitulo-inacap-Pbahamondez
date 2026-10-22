import type { ReactNode } from 'react'
import { Link } from 'react-router-dom'
import { ThemeToggle } from '../theme'

export default function PublicLayout({ children }: { children: ReactNode }) {
  return (
    <div className="public-shell">
      <header className="public-header">
        <Link to="/reportar" className="public-brand" aria-label="Hospital Clínico Félix Bulnes, reportes">
          <img src="/logo-hfb.png" alt="Hospital Clínico Félix Bulnes" />
          <span className="brand-rule" aria-hidden="true"><i /><b /></span>
        </Link>
        <nav className="public-nav" aria-label="Navegación pública">
          <Link to="/reportar/seguimiento">Consultar seguimiento</Link>
          <ThemeToggle />
          <Link className="public-login-link" to="/login">Acceso personal</Link>
        </nav>
      </header>
      <div className="public-banner">
        <div className="public-banner-inner">
          <span className="eyebrow">CANAL CONFIDENCIAL</span>
          <h1>Tu reporte contribuye a protegernos.</h1>
          <p>Un espacio seguro para comunicar incidentes y situaciones que puedan afectar la seguridad de la información.</p>
        </div>
        <span className="public-banner-orbit" aria-hidden="true" />
      </div>
      <main className="public-content">{children}</main>
      <footer className="public-footer">Hospital Clínico Félix Bulnes Cerda <span aria-hidden="true">·</span> Sistema de Gestión de Seguridad de la Información</footer>
    </div>
  )
}
