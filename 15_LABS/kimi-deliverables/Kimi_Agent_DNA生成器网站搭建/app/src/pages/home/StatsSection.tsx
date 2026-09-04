import { useEffect, useRef } from 'react'
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'
import { ExternalLink } from 'lucide-react'

gsap.registerPlugin(ScrollTrigger)

const STATS = [
  { value: 1512, label: '点赞' },
  { value: 844, label: '收藏' },
  { value: 12631, label: '博客总排名' },
]

const fmt = (n: number) => n.toLocaleString('en-US')

/** S8 · CSDN 实战数据（三巨数） */
export default function StatsSection() {
  const ref = useRef<HTMLElement>(null)

  useEffect(() => {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return
    const ctx = gsap.context(() => {
      gsap.utils.toArray<HTMLElement>('.stat-num').forEach((el) => {
        const target = Number(el.dataset.value || 0)
        const obj = { v: 0 }
        gsap.to(obj, {
          v: target,
          duration: 1.6,
          ease: 'power2.out',
          snap: { v: 1 },
          scrollTrigger: { trigger: el, start: 'top 70%' },
          onUpdate: () => {
            el.textContent = fmt(Math.round(obj.v))
          },
        })
      })
      gsap.fromTo(
        '.stat-underline',
        { scaleX: 0 },
        {
          scaleX: 1,
          duration: 1.2,
          ease: 'power3.out',
          stagger: 0.15,
          scrollTrigger: { trigger: ref.current, start: 'top 70%' },
        },
      )
      gsap.fromTo(
        '.stat-tag',
        { opacity: 0, y: 12 },
        {
          opacity: 1,
          y: 0,
          duration: 0.5,
          stagger: 0.15,
          ease: 'power3.out',
          scrollTrigger: { trigger: ref.current, start: 'top 70%' },
        },
      )
    }, ref)
    return () => ctx.revert()
  }, [])

  return (
    <section ref={ref} className="hairline-t hairline-b bg-ink-2 py-20" aria-label="CSDN 实战数据">
      <div className="mx-auto w-full max-w-container px-6 md:px-12">
        <div className="flex justify-end">
          <a
            href="https://blog.csdn.net/"
            target="_blank"
            rel="noreferrer"
            className="inline-flex items-center gap-2 text-[13px] text-paper-dim transition-colors duration-200 hover:text-gold"
          >
            <ExternalLink size={14} />
            前往 CSDN 主页
          </a>
        </div>
        <div className="mt-10 grid grid-cols-1 gap-12 md:grid-cols-3">
          {STATS.map((s) => (
            <div key={s.label} className="flex flex-col items-center gap-4">
              <span
                className="stat-num font-serif font-bold text-gold tabular-nums"
                style={{ fontSize: 'clamp(40px, 6vw, 72px)', lineHeight: 1.1 }}
                data-value={s.value}
              >
                {fmt(s.value)}
              </span>
              <span className="stat-underline h-px w-10 origin-center bg-gold" aria-hidden="true" />
              <span className="stat-tag inline-flex items-center rounded-full border border-dashed border-gold-dim px-[14px] py-1 text-[12px] tracking-[0.2em] text-paper-dim">
                {s.label}
              </span>
            </div>
          ))}
        </div>
        <p className="mt-12 text-center text-[13px] text-paper-faint">
          CSDN 实战数据 · 真实可查 · 禁止虚构
        </p>
      </div>
    </section>
  )
}
