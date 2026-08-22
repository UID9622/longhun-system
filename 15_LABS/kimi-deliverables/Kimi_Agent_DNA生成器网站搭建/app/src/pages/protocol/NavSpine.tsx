import { useEffect, useState } from 'react'
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'
import { LAYERS } from '@/pages/protocol/data'
import type { LayerId } from '@/pages/protocol/data'

gsap.registerPlugin(ScrollTrigger)

/**
 * S2 · 层级导航脊（sticky 锚点条）
 * sticky top 60px · ink 95% 底 · 当前阅读层 ScrollTrigger 高亮 · 点击平滑滚动（offset -120px）
 */
export default function NavSpine() {
  const [active, setActive] = useState<LayerId>('p0')

  useEffect(() => {
    const triggers = LAYERS.map(({ id }) =>
      ScrollTrigger.create({
        trigger: `#${id}`,
        start: 'top center',
        end: 'bottom center',
        onToggle: (self) => {
          if (self.isActive) setActive(id)
        },
      }),
    )
    return () => triggers.forEach((t) => t.kill())
  }, [])

  const jump = (id: LayerId) => {
    const el = document.getElementById(id)
    if (!el) return
    const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches
    el.scrollIntoView({ behavior: reduced ? 'auto' : 'smooth', block: 'start' })
  }

  return (
    <nav
      aria-label="协议层级导航"
      className="sticky top-[60px] z-40 h-12 border-b border-line bg-ink/95 backdrop-blur-sm"
    >
      <div className="mx-auto flex h-full w-full max-w-container items-center gap-1 overflow-x-auto px-6 md:justify-between md:gap-4 md:px-12">
        {LAYERS.map(({ id, layer, label }) => {
          const isActive = active === id
          return (
            <button
              key={id}
              type="button"
              onClick={() => jump(id)}
              aria-current={isActive ? 'true' : undefined}
              className="group relative flex h-full shrink-0 items-center gap-2 px-3 md:px-2"
            >
              <span className="font-mono text-[13px] tracking-[0.06em] text-gold">{layer}</span>
              <span
                className={`whitespace-nowrap text-[13px] transition-colors duration-300 ${
                  isActive ? 'text-paper' : 'text-paper-dim group-hover:text-paper'
                }`}
              >
                {label}
              </span>
              <span
                aria-hidden="true"
                className={`absolute bottom-0 left-1/2 h-[2px] w-full -translate-x-1/2 origin-center bg-gold transition-transform duration-300 ${
                  isActive ? 'scale-x-100' : 'scale-x-0'
                }`}
              />
            </button>
          )
        })}
      </div>
    </nav>
  )
}
