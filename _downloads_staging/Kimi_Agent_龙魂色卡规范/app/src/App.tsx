import { Routes, Route } from 'react-router'
import Layout from './components/Layout'
import Home from './pages/Home'
import Colors from './pages/Colors'
import Weights from './pages/Weights'
import Marquee from './pages/Marquee'
import Comparison from './pages/Comparison'

export default function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route index element={<Home />} />
        <Route path="colors" element={<Colors />} />
        <Route path="weights" element={<Weights />} />
        <Route path="marquee" element={<Marquee />} />
        <Route path="comparison" element={<Comparison />} />
      </Route>
    </Routes>
  )
}
