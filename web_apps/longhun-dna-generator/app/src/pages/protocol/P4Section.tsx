import { useEffect, useRef } from 'react'
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'
import { PenLine, Plus } from 'lucide-react'
import { P4_ITEMS } from '@/pages/protocol/data'
import LayerHeader from '@/pages/protocol/LayerHeader'

gsap.registerPlugin(ScrollTrigger)

/**
 * S7 · P4 用户自定义（10 项 · 留白之层）
 * 虚线描边表达「可书写」· 空白卡虚线常驻流转，hover 转金色实线
 */
export default function P4Section() {
  const rootRef = useRef<HTMLElement>(null)

  useEffect(() => {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return
    const ctx = gsap.context(() => {
      gsap.fromTo(
        '.p4-card',
        { y: 30, opacity: 0 },
        {
          y: 0,
          opacity: 1,
          duration: 0.55,
          ease: 'cubic-bezier(0.22,1,0.36,1)',
          stagger: 0.06,
          scrollTrigger: { trigger: '.p4-grid', start: 'top 80%' },
        },
      )
    }, rootRef)
    return () => ctx.revert()
  }, [])

  return (
    <section
      ref={rootRef}
      id="p4"
      className="hairline-t scroll-mt-[120px] py-[72px] md:py-[120px]"
      aria-label="P4 用户自定义"
    >
      <style>{`
        @keyframes p4-dash-flow { to { stroke-dashoffset: -160; } }
        .p4-blank-dash { animation: p4-dash-flow 20s linear infinite; }
        @media (prefers-reduced-motion: reduce) { .p4-blank-dash { animation: none; } }
      `}</style>

      <div className="mx-auto w-full max-w-container px-6 md:px-12">
        <LayerHeader
          layer="P4"
          title="用户自定义 · 十项"
          caption="权力的尽头是自由。此层属于每一位使用者。"
        />

        <div className="p4-grid mt-12 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {P4_ITEMS.map((item) => (
            <article
              key={item.id}
              className="p4-card group relative border border-dashed border-line-strong bg-transparent px-7 py-6 transition-colors duration-300 hover:border-gold hover:bg-[rgba(201,162,39,0.04)]"
            >
              <span className="font-mono text-[12px] tracking-[0.2em] text-gold">{item.id}</span>
              <h3 className="mt-3 font-serif text-[18px] font-bold tracking-[0.04em] text-paper">
                {item.title}
              </h3>
              <p className="mt-2 text-[13px] leading-[1.85] text-paper-dim">{item.gloss}</p>
              <PenLine
                size={15}
                aria-hidden="true"
                className="absolute bottom-4 right-4 text-paper-dim transition-colors duration-300 group-hover:text-gold"
              />
            </article>
          ))}

          {/* 空白卡：+ 你的规则 */}
          <div className="p4-card group relative flex min-h-[168px] items-center justify-center px-7 py-6">
            {/* 常驻流转虚线框；hover 转金色实线 */}
            <svg
              style={{ transitionDuration: '400ms' }}
              className="pointer-events-none absolute inset-0 h-full w-full transition-opacity group-hover:opacity-0"
              aria-hidden="true"
            >
              <rect
                x="0.5"
                y="0.5"
                style={{ width: 'calc(100% - 1px)', height: 'calc(100% - 1px)' }}
                fill="none"
                stroke="var(--line-strong)"
                strokeWidth="1"
                strokeDasharray="8 6"
                className="p4-blank-dash"
              />
            </svg>
            <span
              aria-hidden="true"
              style={{ transitionDuration: '400ms' }}
              className="pointer-events-none absolute inset-0 border border-gold opacity-0 transition-opacity group-hover:opacity-100"
            />
            <span
              style={{ transitionDuration: '400ms' }}
              className="inline-flex items-center gap-3 font-serif text-[18px] font-bold tracking-[0.06em] text-paper-dim transition-colors group-hover:text-gold"
            >
              <Plus size={18} aria-hidden="true" />
              你的规则
            </span>
            {/* tooltip */}
            <span
              role="tooltip"
              className="pointer-events-none absolute -top-11 left-1/2 -translate-x-1/2 whitespace-nowrap border border-line bg-ink-3 px-4 py-2 font-mono text-[11px] tracking-[0.06em] text-paper-dim opacity-0 transition-opacity duration-300 group-hover:opacity-100"
            >
              P4 由你书写——本地生效，永不上传。
            </span>
          </div>
        </div>
      </div>
    </section>
  )
}
