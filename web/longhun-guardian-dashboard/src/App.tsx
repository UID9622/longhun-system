import { Routes, Route } from 'react-router'
import Home from './pages/Home'
import Login from "./pages/Login"
import Dashboard from "./pages/Dashboard"
import ContentMgmt from "./pages/ContentMgmt"
import PersonaConfig from "./pages/PersonaConfig"
import DeviceMgmt from "./pages/DeviceMgmt"
import SMKeys from "./pages/SMKeys"
import AuditLog from "./pages/AuditLog"
import Recharge from "./pages/Recharge"
import PaymentMgmt from "./pages/PaymentMgmt"
import IntakeDropZone from "./pages/IntakeDropZone"
import Guardian from "./pages/Guardian"
import NotFound from "./pages/NotFound"

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/login" element={<Login />} />
      <Route path="/dashboard" element={<Dashboard />} />
      <Route path="/dashboard/content" element={<ContentMgmt />} />
      <Route path="/dashboard/persona" element={<PersonaConfig />} />
      <Route path="/dashboard/devices" element={<DeviceMgmt />} />
      <Route path="/dashboard/smkeys" element={<SMKeys />} />
      <Route path="/dashboard/recharge" element={<Recharge />} />
      <Route path="/dashboard/payments" element={<PaymentMgmt />} />
      <Route path="/dashboard/intake" element={<IntakeDropZone />} />
      <Route path="/dashboard/guardian" element={<Guardian />} />
      <Route path="/dashboard/audit" element={<AuditLog />} />
      <Route path="*" element={<NotFound />} />
    </Routes>
  )
}
