import { Navigate, Outlet, Route, Routes } from 'react-router-dom'
import { useAuth } from './auth'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import Controles from './pages/Controles'
import Incidentes from './pages/Incidentes'
import Login from './pages/Login'
import Personas from './pages/Personas'
import Reportes from './pages/Reportes'
import Reportar from './pages/Reportar'
import SeguimientoTicket from './pages/SeguimientoTicket'
import Tickets from './pages/Tickets'
import Usuarios from './pages/Usuarios'
import Terceros from './pages/Terceros'
import type { Role } from './types'

function HomeRedirect() {
  const { user } = useAuth()
  if (user?.rol === 'admin_sistema') return <Navigate to="/usuarios" replace />
  return <Navigate to="/dashboard" replace />
}

function RoleRoute({ roles, children }: { roles: Role[]; children: React.ReactNode }) {
  const { user } = useAuth()
  if (!user || !roles.includes(user.rol)) return <HomeRedirect />
  return children
}

function ProtectedRoute() {
  const { user } = useAuth()
  if (!user) return <Navigate to="/login" replace />
  return <Outlet />
}

export default function App() {
  const { user, loading } = useAuth()

  if (loading) return <div className="loading-screen"><span className="loader" />Cargando plataforma…</div>

  return (
    <Routes>
      <Route path="/reportar" element={<Reportar />} />
      <Route path="/reportar/seguimiento" element={<SeguimientoTicket />} />
      <Route
        path="/login"
        element={user ? <HomeRedirect /> : <Login />}
      />
      <Route element={<ProtectedRoute />}>
        <Route element={<Layout />}>
        <Route path="/" element={<HomeRedirect />} />
        <Route path="/dashboard" element={<RoleRoute roles={['encargado', 'admin_contratos', 'referente_tecnico', 'director']}><Dashboard /></RoleRoute>} />
        <Route path="/controles" element={<RoleRoute roles={['encargado', 'admin_contratos', 'referente_tecnico', 'director']}><Controles /></RoleRoute>} />
        <Route path="/incidentes" element={<RoleRoute roles={['encargado', 'admin_contratos', 'referente_tecnico', 'director']}><Incidentes /></RoleRoute>} />
        <Route path="/terceros" element={<RoleRoute roles={['encargado', 'admin_contratos', 'referente_tecnico', 'director']}><Terceros /></RoleRoute>} />
        <Route path="/personas" element={<RoleRoute roles={['encargado', 'admin_contratos', 'referente_tecnico', 'director']}><Personas /></RoleRoute>} />
        <Route path="/reportes" element={<RoleRoute roles={['encargado', 'admin_contratos', 'referente_tecnico', 'director']}><Reportes /></RoleRoute>} />
        <Route path="/tickets" element={<RoleRoute roles={['encargado']}><Tickets /></RoleRoute>} />
        <Route path="/usuarios" element={<RoleRoute roles={['admin_sistema']}><Usuarios /></RoleRoute>} />
        </Route>
      </Route>
      <Route path="*" element={user ? <HomeRedirect /> : <Navigate to="/login" replace />} />
    </Routes>
  )
}
