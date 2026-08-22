import { Routes, Route } from 'react-router'
import Layout from '@/components/Layout'
import Home from '@/pages/Home'
import Protocol from '@/pages/Protocol'
import Dna from '@/pages/Dna'
import Matrix from '@/pages/Matrix'
import Works from '@/pages/Works'
import Timeline from '@/pages/Timeline'
import Founder from '@/pages/Founder'

export default function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route index element={<Home />} />
        <Route path="protocol" element={<Protocol />} />
        <Route path="dna" element={<Dna />} />
        <Route path="matrix" element={<Matrix />} />
        <Route path="works" element={<Works />} />
        <Route path="timeline" element={<Timeline />} />
        <Route path="founder" element={<Founder />} />
        <Route path="*" element={<Home />} />
      </Route>
    </Routes>
  )
}
