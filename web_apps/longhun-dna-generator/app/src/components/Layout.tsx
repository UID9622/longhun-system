import { useEffect } from 'react'
import { useLocation, useOutlet } from 'react-router'
import Lenis from 'lenis'
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'
import { AnimatePresence, motion } from 'framer-motion'
import Navbar from '@/components/Navbar'
import Footer from '@/components/Footer'
import { LaunchAIProvider } from '@/ai/useLaunchAI'
import LaunchAIButton from '@/components/launchai/LaunchAIButton'
import LaunchAIConsole from '@/components/launchai/LaunchAIConsole'

gsap.registerPlugin(ScrollTrigger)

/**
 * Layout —— Navbar 为 fixed overlay（design.md 5.1），
 * 内容槽统一垫 72px 顶距；全幅 hero 在页面内部以负边距豁免。
 * 全局 Lenis（lerp 0.09）+ ScrollTrigger 同步（design.md §4）。
 * 路由转场：旧页 opacity→0, y:-12（0.25s）；新页 y:16→0（0.45s）。
 */
export default function Layout() {
  const location = useLocation()
  const outlet = useOutlet()

  // Lenis 全站平滑滚动 + GSAP ScrollTrigger 同步
  useEffect(() => {
    const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches
    if (reduced) return
    const lenis = new Lenis({ lerp: 0.09 })
    lenis.on('scroll', ScrollTrigger.update)
    const tick = (time: number) => lenis.raf(time * 1000)
    gsap.ticker.add(tick)
    gsap.ticker.lagSmoothing(0)
    return () => {
      gsap.ticker.remove(tick)
      lenis.destroy()
    }
  }, [])

  // 路由切换：回顶 + 刷新 ScrollTrigger
  useEffect(() => {
    window.scrollTo(0, 0)
    const t = window.setTimeout(() => ScrollTrigger.refresh(), 80)
    return () => window.clearTimeout(t)
  }, [location.pathname])

  return (
    <LaunchAIProvider>
      <div className="flex min-h-[100dvh] flex-col bg-ink text-paper">
        <Navbar />
        {/* fixed nav 高度 72px → 内容槽顶距；全幅 hero 页内 -mt-[72px] 豁免 */}
        <main className="flex-1 pt-[72px]">
          <AnimatePresence mode="wait">
            <motion.div
              key={location.pathname}
              initial={{ opacity: 0, y: 16 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -12, transition: { duration: 0.25 } }}
              transition={{ duration: 0.45, ease: [0.22, 1, 0.36, 1] }}
            >
              {outlet}
            </motion.div>
          </AnimatePresence>
        </main>
        <Footer />
        {/* 啟動AI：全站可达的作战指挥台（Cmd/Ctrl+K 开合） */}
        <LaunchAIButton />
        <LaunchAIConsole />
      </div>
    </LaunchAIProvider>
  )
}
