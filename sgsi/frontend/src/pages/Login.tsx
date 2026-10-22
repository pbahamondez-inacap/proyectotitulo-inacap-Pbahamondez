import { useState, type FormEvent } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../auth'
import { ThemeToggle } from '../theme'

export default function Login() {
  const { login } = useAuth()
  const navigate = useNavigate()
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  async function handleSubmit(event: FormEvent) {
    event.preventDefault()
    setError('')
    setLoading(true)
    try {
      const user = await login(username.trim(), password)
      navigate(user.rol === 'admin_sistema' ? '/usuarios' : user.rol === 'encargado' ? '/tickets' : '/dashboard', { replace: true })
    } catch (err) {
      setError(err instanceof Error ? err.message : 'No fue posible iniciar sesión')
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="login-page">
      <div className="login-top-tools"><ThemeToggle /></div>
      <section className="login-layout">
        <div className="login-brand-panel">
          <div className="login-hospital-brand">
            <img src="/logo-hfb.png" alt="Hospital Clínico Félix Bulnes" />
            <span className="brand-rule" aria-hidden="true"><i /><b /></span>
          </div>
          <p className="eyebrow">HOSPITAL CLÍNICO FÉLIX BULNES CERDA</p>
          <h1>Seguridad que cuida<br /><em>lo que más importa.</em></h1>
          <p className="login-brand-description">Plataforma institucional para gestionar la seguridad de la información, proteger nuestros sistemas y fortalecer la confianza de nuestra comunidad.</p>
          <div className="login-brand-note"><span aria-hidden="true">✦</span> Compromiso con una atención segura y confiable</div>
          <div className="brand-orbit orbit-one" aria-hidden="true" />
          <div className="brand-orbit orbit-two" aria-hidden="true" />
        </div>
        <div className="login-form-panel">
          <div className="login-card">
            <div className="login-form-heading">
              <span className="login-mark" aria-hidden="true">SGSI</span>
              <p className="eyebrow">ACCESO SEGURO</p>
              <h2>Bienvenido/a</h2>
              <p>Ingresa con tus credenciales institucionales.</p>
            </div>
            <form onSubmit={handleSubmit}>
              <label className="field-label" htmlFor="username">Usuario</label>
              <input
                id="username"
                className="input"
                value={username}
                onChange={(event) => setUsername(event.target.value)}
                placeholder="Nombre de usuario"
                autoComplete="username"                required
              />
              <label className="field-label" htmlFor="password">Contraseña</label>
              <input
                id="password"
                className="input"
                type="password"
                value={password}
                onChange={(event) => setPassword(event.target.value)}
                placeholder="Ingresa tu contraseña"
                autoComplete="current-password"
                required
              />
              {error && <div className="alert alert-error" role="alert">{error}</div>}
              <button className="btn btn-primary btn-block login-submit" disabled={loading}>
                {loading ? <><span className="loader loader-small" />Ingresando…</> : <>Ingresar al sistema <span aria-hidden="true">→</span></>}
              </button>
            </form>
            <div className="login-divider"><span>o bien</span></div>
            <Link to="/reportar" className="anonymous-link"><span className="anonymous-icon" aria-hidden="true">◌</span><span><strong>Reportar un incidente o denuncia</strong><small>Canal público y anónimo</small></span><span className="anonymous-arrow" aria-hidden="true">↗</span></Link>
            <div className="login-security-note"><span aria-hidden="true">▣</span> Tu sesión está protegida mediante autenticación segura.</div>
          </div>
          <footer className="login-footer">© Hospital Clínico Félix Bulnes Cerda <span>·</span> Sistema de Gestión de Seguridad de la Información</footer>
        </div>
      </section>
    </main>
  )
}
