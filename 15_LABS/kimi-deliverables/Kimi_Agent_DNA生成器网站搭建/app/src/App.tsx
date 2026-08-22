import { lazy, Suspense } from 'react'
import { Routes, Route } from 'react-router'
import Layout from '@/components/Layout'
import ErrorBoundary from '@/components/ErrorBoundary'
import PageSkeleton from '@/components/PageSkeleton'

// 路由级代码分割（React.lazy）：首屏仅加载 Home，其余按需加载
const Home = lazy(() => import('@/pages/Home'))
const Protocol = lazy(() => import('@/pages/Protocol'))
const Dna = lazy(() => import('@/pages/Dna'))
const Matrix = lazy(() => import('@/pages/Matrix'))
const Works = lazy(() => import('@/pages/Works'))
const Timeline = lazy(() => import('@/pages/Timeline'))
const Founder = lazy(() => import('@/pages/Founder'))

/** 统一的页面包装器：ErrorBoundary + Suspense + 骨架屏 */
function PageWrap({ children }: { children: React.ReactNode }) {
  return (
    <ErrorBoundary>
      <Suspense fallback={<PageSkeleton />}>{children}</Suspense>
    </ErrorBoundary>
  )
}

export default function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route index element={<PageWrap><Home /></PageWrap>} />
        <Route path="protocol" element={<PageWrap><Protocol /></PageWrap>} />
        <Route path="dna" element={<PageWrap><Dna /></PageWrap>} />
        <Route path="matrix" element={<PageWrap><Matrix /></PageWrap>} />
        <Route path="works" element={<PageWrap><Works /></PageWrap>} />
        <Route path="timeline" element={<PageWrap><Timeline /></PageWrap>} />
        <Route path="founder" element={<PageWrap><Founder /></PageWrap>} />
        <Route path="*" element={<PageWrap><Home /></PageWrap>} />
      </Route>
    </Routes>
  )
}
