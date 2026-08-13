import { useEffect, useState } from 'react'
import { Link, NavLink, useLocation } from 'react-router'
import { AnimatePresence, motion } from 'framer-motion'
import { Menu, X } from 'lucide-react'
import GanzhiClock from '@/components/GanzhiClock'
import OutlineButton from '@/components/OutlineButton'
import { useLaunchAI } from '@/ai/useLaunchAI'

export const NAV_LINKS = [
  { to: '/protocol', label: '协议' },
  { to: '/matrix', label: '矩阵' },
  { to: '/dna', label: 'DNA' },
  { to: '/works', label: '作品' },
  { to: '/timeline', label: '远征' },
  { to: '/founder', label: '创始人' },
  { to: '/storage', label: '存储' },
  { to: '/health', label: '健康' },
  { to: '/api', label: 'API' },
] as const

export const DNA_ANCHOR = '#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL'

/**
 * Navbar（design.md 5.1）
 * fixed 叠于 hero 之上 · 滚动 >80px 转 ink 实底 + 底部发丝线 · 高度 72px→60px
 * Layout 为其内容槽垫 72px；全幅 hero 在页内负边距豁免
 */
export default function Navbar() {
  const [scrolled, setScrolled] = useState(false)
  const [open, setOpen] = useState(false)
  const location = useLocation()
  const { toggle: toggleLaunchAI } = useLaunchAI()

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 80)
    onScroll()
    window.addEventListener('scroll', onScroll, { passive: true })
    return () => window.removeEventListener('scroll', onScroll)
  }, [])

  useEffect(() => {
    setOpen(false)
  }, [location.pathname])

  useEffect(() => {
    document.body.style.overflow = open ? 'hidden' : ''
    return () => {
      document.body.style.overflow = ''
    }
  }, [open])

  return (
    <>
      <nav
        className={`fixed inset-x-0 top-0 z-50 transition-all duration-300 ${
          scrolled ? 'h-[60px] border-b border-line bg-ink' : 'h-[72px] border-b border-transparent bg-transparent'
        }`}
        aria-label="主导航"
      >
        <div className="mx-auto flex h-full w-full max-w-container items-center justify-between px-6 md:px-12">
          {/* 左：印 + 名 */}
          <Link to="/" className="flex items-center gap-3" aria-label="龍魂系统首页">
            <img src="/logo-seal.svg" alt="龍魂印章" width={32} height={32} className="h-8 w-8" />
            <span className="flex items-baseline gap-3">
              <span className="font-serif text-[18px] font-bold tracking-[0.08em] text-paper">
                龍魂系统
              </span>
              <span className="hidden font-cinzel text-[11px] font-semibold tracking-[0.3em] text-gold-dim sm:inline">
                UID9622
              </span>
            </span>
          </Link>

          {/* 中：六页链接（桌面） */}
          <div className="hidden items-center gap-8 lg:flex">
            {NAV_LINKS.map((l) => (
              <NavLink
                key={l.to}
                to={l.to}
                className={({ isActive }) =>
                  `group relative text-[14px] tracking-[0.1em] transition-colors duration-300 ${
                    isActive ? 'text-paper' : 'text-paper-dim hover:text-paper'
                  }`
                }
              >
                {({ isActive }) => (
                  <>
                    {l.label}
                    <span
                      className={`absolute -bottom-2 left-0 h-px w-full origin-left bg-gold transition-transform duration-300 ${
                        isActive ? 'scale-x-100' : 'scale-x-0 group-hover:scale-x-100'
                      }`}
                      aria-hidden="true"
                    />
                  </>
                )}
              </NavLink>
            ))}
          </div>

          {/* 右：干支小时钟 + CTA（桌面）/ 汉堡（移动） */}
          <div className="flex items-center gap-6">
            <div className="hidden xl:block">
              <GanzhiClock variant="compact" />
            </div>
            <div className="hidden lg:block">
              <OutlineButton small onClick={toggleLaunchAI} ariaLabel="打开龍魂·啟動AI 智能助手（快捷键 Ctrl+K）">
                啟動AI
              </OutlineButton>
            </div>
            <div className="hidden lg:block">
              <OutlineButton to="/dna" small>
                生成 DNA
              </OutlineButton>
            </div>
            <button
              type="button"
              className="text-paper lg:hidden"
              onClick={() => setOpen(true)}
              aria-label="打开菜单"
              aria-expanded={open}
            >
              <Menu size={24} />
            </button>
          </div>
        </div>
      </nav>

      {/* 移动端全屏墨黑抽屉 */}
      <AnimatePresence>
        {open ? (
          <motion.div
            className="fixed inset-0 z-[60] flex flex-col bg-ink lg:hidden"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.25 }}
            role="dialog"
            aria-modal="true"
            aria-label="站点菜单"
          >
            <div className="flex h-[72px] items-center justify-between px-6">
              <span className="font-serif text-[18px] font-bold text-paper">龍魂系统</span>
              <button type="button" onClick={() => setOpen(false)} aria-label="关闭菜单" className="text-paper">
                <X size={26} />
              </button>
            </div>
            <div className="flex flex-1 flex-col justify-center gap-7 px-10">
              {[{ to: '/', label: '卷首' }, ...NAV_LINKS].map((l, i) => (
                <motion.div
                  key={l.to}
                  initial={{ opacity: 0, y: 24 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.07 * i, duration: 0.4, ease: [0.22, 1, 0.36, 1] }}
                >
                  <Link
                    to={l.to}
                    className="font-serif text-[32px] font-bold tracking-[0.1em] text-paper transition-colors hover:text-gold"
                  >
                    {l.label}
                  </Link>
                </motion.div>
              ))}
            </div>
            <div className="hairline-t px-10 py-6">
              <p className="break-all font-mono text-[11px] leading-relaxed text-paper-faint">{DNA_ANCHOR}</p>
              <div className="mt-4">
                <GanzhiClock variant="compact" />
              </div>
            </div>
          </motion.div>
        ) : null}
      </AnimatePresence>
    </>
  )
}
