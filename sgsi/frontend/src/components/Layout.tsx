import { useEffect, useState } from 'react'
import { Link, NavLink, Outlet, useNavigate } from 'react-router-dom'
import { useAuth } from '../auth'
import { notificacionesApi } from '../api'
import { ROL_LABELS } from '../constants'
import { ThemeToggle } from '../theme'

const BUSINESS_ITEMS = [
  { to: '/dashboard', label: 'Resumen', icon: '⌂', end: true },
  { to: '/controles', label: 'Controles ISO 27001', icon: '✓' },
  { to: '/incidentes', label: 'Incidentes', icon: '◇' },
  { to: '/terceros', label: 'Terceros y proveedores', icon: '◈' },
  { to: '/personas', label: 'Controles de personas', icon: '♙' },
  { to: '/reportes', label: 'Reportería', icon: '▤' },
]

export default function Layout() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()
  const [pending, setPending] = useState(0)
  const isAdmin = user?.rol === 'admin_sistema'
  const items = isAdmin
    ? [{ to: '/usuarios', label: 'Usuarios', icon: '♙', end: true }]
    : user?.rol === 'encargado'
      ? [...BUSINESS_ITEMS, { to: '/tickets', label: 'Ticketera', icon: '▣', end: true }]
      : BUSINESS_ITEMS

  useEffect(() => {
    if (user?.rol !== 'encargado') return
    let mounted = true
    const update = () => notificacionesApi.pendingCount().then((r) => mounted && setPending(r.count)).catch(() => undefined)
    update()
    window.addEventListener('sgsi:refresh-notification-count', update)
    const timer = window.setInterval(update, 60_000)
    return () => {
      mounted = false
      window.clearInterval(timer)
      window.removeEventListener('sgsi:refresh-notification-count', update)
    }
  }, [user?.rol])

  function handleLogout() {
    logout()
    navigate('/login')
  }

  return (
    <div className="app-shell">
      <aside className="sidebar" aria-label="Navegación principal">
        <Link className="brand" to="/" aria-label="SGSI Hospital Félix Bulnes">
          <img className="brand-logo" src="/logo-hfb.png" alt="Hospital Clínico Félix Bulnes" />
          <span className="brand-rule" aria-hidden="true"><i /><b /></span>
          <span className="brand-copy">
            <strong>SGSI</strong>
            <small>Seguridad de la información</small>
          </span>
        </Link>
        <div className="nav-section-label">PLATAFORMA</div>
        <nav className="nav">
          {items.map((item) => (
            <NavLink key={item.to} to={item.to} end={item.end} className={({ isActive }) => `nav-link${isActive ? ' active' : ''}`}>
              <span className="nav-icon" aria-hidden="true">{item.icon}</span>
              <span>{item.label}</span>
              {item.to === '/tickets' && pending > 0 && <span className="nav-count" aria-label={`${pending} pendientes`}>{pending > 99 ? '99+' : pending}</span>}
            </NavLink>
          ))}
        </nav>
        {!isAdmin && (
          <Link className="nav-link report-shortcut" to="/reportar">
            <span className="nav-icon" aria-hidden="true">＋</span>
            <span>Reportar anónimamente</span>
          </Link>
        )}
        <div className="sidebar-footer">
          <span>Hospital Clínico Félix Bulnes Cerda</span>
          <small>Sistema institucional SGSI</small>
        </div>
      </aside>
      <div className="main">
        <header className="topbar">
          <div className="topbar-brand">
            <span className="topbar-kicker">HOSPITAL CLÍNICO FÉLIX BULNES</span>
            <h1 className="page-title">Sistema de Gestión de Seguridad de la Información</h1>
          </div>
          <div className="user-menu">
            <ThemeToggle />
            <div className="user-avatar" aria-hidden="true">{user?.nombre_completo?.slice(0, 1).toUpperCase()}</div>
            <div className="user-info">
              <div className="user-name">{user?.nombre_completo}</div>
              <div className="user-role">{user ? ROL_LABELS[user.rol] : ''}</div>
            </div>
            <button className="btn btn-ghost btn-sm" onClick={handleLogout}>Salir</button>
          </div>
        </header>
        <main className="content"><Outlet /></main>
        <footer className="app-footer">Hospital Clínico Félix Bulnes Cerda <span aria-hidden="true">·</span> SGSI</footer>
      </div>
    </div>
  )
}
