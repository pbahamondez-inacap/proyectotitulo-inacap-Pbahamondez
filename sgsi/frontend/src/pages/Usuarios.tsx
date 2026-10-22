import { useCallback, useEffect, useMemo, useState, type FormEvent } from 'react'
import Badge from '../components/Badge'
import Modal from '../components/Modal'
import { usuariosApi } from '../api'
import { ROL_LABELS, ROLES } from '../constants'
import { fmtDate } from '../helpers'
import type { AuditoriaOut, Role, Usuario, UsuarioCreate } from '../types'

interface UsuarioForm {
  username: string
  nombre_completo: string
  password: string
  rol: Role
}
const emptyForm: UsuarioForm = { username: '', nombre_completo: '', password: '', rol: 'encargado' }

export default function Usuarios() {
  const [users, setUsers] = useState<Usuario[]>([])
  const [audit, setAudit] = useState<AuditoriaOut[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [query, setQuery] = useState('')
  const [roleFilter, setRoleFilter] = useState('')
  const [statusFilter, setStatusFilter] = useState('')
  const [tab, setTab] = useState<'users' | 'audit'>('users')
  const [modalOpen, setModalOpen] = useState(false)
  const [editing, setEditing] = useState<Usuario | null>(null)
  const [form, setForm] = useState<UsuarioForm>(emptyForm)
  const [saving, setSaving] = useState(false)
  const [resetTarget, setResetTarget] = useState<Usuario | null>(null)
  const [newPassword, setNewPassword] = useState('')

  const load = useCallback(async () => {
    setLoading(true)
    setError('')
    try {
      const [usersResponse, auditResponse] = await Promise.all([usuariosApi.list(), usuariosApi.audit()])
      setUsers(usersResponse)
      setAudit(auditResponse)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'No fue posible cargar usuarios')
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => { void load() }, [load])

  const filtered = useMemo(() => users.filter((user) => {
    const searchMatch = `${user.nombre_completo} ${user.username}`.toLowerCase().includes(query.toLowerCase())
    return searchMatch && (!roleFilter || user.rol === roleFilter) && (!statusFilter || String(user.activo) === statusFilter)
  }), [users, query, roleFilter, statusFilter])

  function openCreate() {
    setEditing(null)
    setForm(emptyForm)
    setError('')
    setModalOpen(true)
  }

  function openEdit(user: Usuario) {
    setEditing(user)
    setForm({ username: user.username, nombre_completo: user.nombre_completo, password: '', rol: user.rol })
    setError('')
    setModalOpen(true)
  }

  async function saveUser(event: FormEvent) {
    event.preventDefault()
    setSaving(true)
    setError('')
    try {
      if (editing) {
        await usuariosApi.update(editing.id, {
          username: form.username.trim(),
          nombre_completo: form.nombre_completo.trim(),
          rol: form.rol,
        })
      } else {
        const payload: UsuarioCreate = {
          username: form.username.trim(),
          nombre_completo: form.nombre_completo.trim(),
          password: form.password,
          rol: form.rol,
        }
        await usuariosApi.create(payload)
      }
      setModalOpen(false)
      await load()
    } catch (err) {
      setError(err instanceof Error ? err.message : 'No fue posible guardar el usuario')
    } finally {
      setSaving(false)
    }
  }

  async function toggleStatus(user: Usuario) {
    const action = user.activo ? 'deshabilitar' : 'habilitar'
    if (!window.confirm(`¿Confirmas ${action} al usuario ${user.nombre_completo}?`)) return
    setError('')
    try {
      await usuariosApi.setActive(user.id, !user.activo)
      await load()
    } catch (err) {
      setError(err instanceof Error ? err.message : `No fue posible ${action} el usuario`)
    }
  }

  async function resetPassword(event: FormEvent) {
    event.preventDefault()
    if (!resetTarget) return
    setSaving(true)
    setError('')
    try {
      await usuariosApi.resetPassword(resetTarget.id, newPassword)
      setResetTarget(null)
      setNewPassword('')
      await load()
    } catch (err) {
      setError(err instanceof Error ? err.message : 'No fue posible restablecer la contraseña')
    } finally {
      setSaving(false)
    }
  }

  return (
    <div className="page-stack">
      <div className="page-heading">
        <div><span className="eyebrow">ADMINISTRACIÓN DEL SISTEMA</span><h2>Gestión de usuarios</h2><p>Administra accesos, roles y trazabilidad de las cuentas del SGSI.</p></div>
        <button className="btn btn-primary" onClick={openCreate}><span aria-hidden="true">＋</span> Crear usuario</button>
      </div>
      <div className="module-tabs" role="tablist" aria-label="Panel de usuarios">
        <button type="button" role="tab" aria-selected={tab === 'users'} className={tab === 'users' ? 'selected' : ''} onClick={() => setTab('users')}>Usuarios <span className="tab-count">{users.length}</span></button>
        <button type="button" role="tab" aria-selected={tab === 'audit'} className={tab === 'audit' ? 'selected' : ''} onClick={() => setTab('audit')}>Auditoría</button>
      </div>
      {error && <div className="alert alert-error" role="alert">{error}</div>}
      {tab === 'users' ? (
        <section className="card table-card">
          <div className="toolbar">
            <div><h3 className="card-title">Cuentas registradas</h3><p className="text-muted">{filtered.length} de {users.length} usuarios</p></div>
            <div className="filters">
              <label className="search-box"><span aria-hidden="true">⌕</span><input className="input" aria-label="Buscar usuarios" placeholder="Buscar por nombre o usuario" value={query} onChange={(event) => setQuery(event.target.value)} /></label>
              <select className="input" aria-label="Filtrar por rol" value={roleFilter} onChange={(event) => setRoleFilter(event.target.value)}><option value="">Todos los roles</option>{ROLES.map((role) => <option key={role.value} value={role.value}>{role.label}</option>)}</select>
              <select className="input" aria-label="Filtrar por estado" value={statusFilter} onChange={(event) => setStatusFilter(event.target.value)}><option value="">Todos los estados</option><option value="true">Activo</option><option value="false">Inactivo</option></select>
            </div>
          </div>
          {loading ? <div className="loading-inline"><span className="loader" />Cargando usuarios…</div> : (
            <div className="table-wrap"><table className="table">
              <thead><tr><th>Usuario</th><th>Rol asignado</th><th>Estado</th><th className="actions-head">Acciones</th></tr></thead>
              <tbody>
                {filtered.map((user) => <tr key={user.id}>
                  <td><div className="user-cell"><span className="user-avatar user-avatar-small">{user.nombre_completo.slice(0, 1).toUpperCase()}</span><span><strong>{user.nombre_completo}</strong><small>@{user.username}</small></span></div></td>
                  <td><Badge color={user.rol === 'admin_sistema' ? 'purple' : user.rol === 'encargado' ? 'blue' : 'gray'}>{ROL_LABELS[user.rol]}</Badge></td>
                  <td><Badge color={user.activo ? 'green' : 'gray'}><span className="status-dot" />{user.activo ? 'Activo' : 'Inactivo'}</Badge></td>
                  <td><div className="row-actions"><button className="btn btn-ghost btn-sm" onClick={() => openEdit(user)} aria-label={`Editar ${user.username}`}>Editar</button><button className="btn btn-ghost btn-sm" onClick={() => { setResetTarget(user); setNewPassword('') }}>Restablecer clave</button><button className={`btn btn-sm ${user.activo ? 'btn-danger' : 'btn-success'}`} onClick={() => void toggleStatus(user)}>{user.activo ? 'Deshabilitar' : 'Habilitar'}</button></div></td>
                </tr>)}
                {filtered.length === 0 && <tr><td colSpan={4} className="empty-row"><span className="empty-icon">♙</span><strong>No hay usuarios que coincidan</strong><small>Ajusta los filtros o crea una cuenta nueva.</small></td></tr>}
              </tbody>
            </table></div>
          )}
        </section>
      ) : (
        <section className="card table-card">
          <div className="card-head"><div><h3 className="card-title">Registro de auditoría</h3><p className="text-muted">Historial de cambios y operaciones sobre cuentas.</p></div><button className="btn btn-ghost btn-sm" onClick={() => void load()}>Actualizar</button></div>
          {loading ? <div className="loading-inline"><span className="loader" />Cargando auditoría…</div> : <div className="table-wrap"><table className="table">
            <thead><tr><th>Quién</th><th>Acción</th><th>Usuario afectado</th><th>Detalle</th><th>Fecha y hora</th></tr></thead>
            <tbody>{audit.map((entry) => <tr key={entry.id}><td><strong>{entry.actor_username}</strong></td><td><Badge color={entry.accion === 'crear_usuario' ? 'green' : entry.accion.includes('deshabilitar') ? 'red' : 'blue'}>{entry.accion.replace(/_/g, ' ')}</Badge></td><td>{entry.usuario_objetivo_username}</td><td>{entry.detalle || '—'}</td><td className="text-muted">{fmtDate(entry.creado_en)}</td></tr>)}
              {audit.length === 0 && <tr><td colSpan={5} className="empty-row">Aún no hay eventos de auditoría.</td></tr>}</tbody>
          </table></div>}
        </section>
      )}

      <Modal open={modalOpen} onClose={() => setModalOpen(false)} title={editing ? 'Editar usuario' : 'Crear usuario'}>
        <form className="form-stack" onSubmit={saveUser}>
          <div className="form-grid">
            <div className="field-full"><label className="field-label" htmlFor="full-name">Nombre completo</label><input id="full-name" className="input" required value={form.nombre_completo} onChange={(event) => setForm({ ...form, nombre_completo: event.target.value })} /></div>
            <div className="field-full"><label className="field-label" htmlFor="username-new">Nombre de usuario</label><input id="username-new" className="input" required value={form.username} onChange={(event) => setForm({ ...form, username: event.target.value })} autoComplete="off" /></div>
            {!editing && <div className="field-full"><label className="field-label" htmlFor="password-new">Contraseña inicial</label><input id="password-new" className="input" type="password" required minLength={8} value={form.password} onChange={(event) => setForm({ ...form, password: event.target.value })} autoComplete="new-password" /><small className="field-hint">Mínimo 8 caracteres.</small></div>}
            <div className="field-full"><label className="field-label" htmlFor="user-role">Rol</label><select id="user-role" className="input" value={form.rol} onChange={(event) => setForm({ ...form, rol: event.target.value as Role })}>{ROLES.map((role) => <option value={role.value} key={role.value}>{role.label}</option>)}</select></div>
          </div>
          {error && <div className="alert alert-error" role="alert">{error}</div>}
          <div className="modal-actions"><button type="button" className="btn btn-ghost" onClick={() => setModalOpen(false)}>Cancelar</button><button className="btn btn-primary" disabled={saving}>{saving ? 'Guardando…' : editing ? 'Guardar cambios' : 'Crear usuario'}</button></div>
        </form>
      </Modal>
      <Modal open={!!resetTarget} onClose={() => setResetTarget(null)} title="Restablecer contraseña">
        <form className="form-stack" onSubmit={resetPassword}>
          <p>Define una nueva contraseña para <strong>{resetTarget?.nombre_completo}</strong>.</p>
          <label className="field-label" htmlFor="reset-password">Nueva contraseña</label>
          <input id="reset-password" className="input" type="password" minLength={8} required value={newPassword} onChange={(event) => setNewPassword(event.target.value)} autoComplete="new-password" />
          {error && <div className="alert alert-error" role="alert">{error}</div>}
          <div className="modal-actions"><button type="button" className="btn btn-ghost" onClick={() => setResetTarget(null)}>Cancelar</button><button className="btn btn-primary" disabled={saving}>{saving ? 'Actualizando…' : 'Restablecer contraseña'}</button></div>
        </form>
      </Modal>
    </div>
  )
}
