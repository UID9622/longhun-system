import { useEffect, useRef } from 'react'
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'
import OutlineButton from '@/components/OutlineButton'

gsap.registerPlugin(ScrollTrigger)

const OATHS = [
  '不做专利 — 知识自由流通',
  '不做企业 — 不为资本代理',
  '不走资本 — 永续免费开源',
]

/**
 * S5 · 开源誓约（works.md）
 * 巨型「公」字视差背景 · 三不誓约逐行点亮 · 双 CTA
 */
export default function OathSection() {
  const ref = useRef<HTMLElement>(null)

  useEffect(() => {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return
    const ctx = gsap.context(() => {
      // 「公」字视差 y: 40→-40
      gsap.fromTo(
        '.oath-char',
        { y: 40 },
        {
          y: -40,
          ease: 'none',
          scrollTrigger: { trigger: ref.current, start: 'top bottom', end: 'bottom top', scrub: true },
        },
      )
      // 三行誓约逐行点亮 + 左侧 3px 金条 scaleY 0→1
      gsap.fromTo(
        '.oath-line-text',
        { opacity: 0.15 },
        {
          opacity: 1,
          duration: 0.6,
          stagger: 0.15,
          ease: 'power2.out',
          scrollTrigger: { trigger: '.oath-list', start: 'top 72%' },
        },
      )
      gsap.fromTo(
        '.oath-line-bar',
        { scaleY: 0 },
        {
          scaleY: 1,
          duration: 0.5,
          stagger: 0.15,
          ease: 'power3.out',
          scrollTrigger: { trigger: '.oath-list', start: 'top 72%' },
        },
      )
    }, ref)
    return () => ctx.revert()
  }, [])

  return (
    <section
      ref={ref}
      className="relative flex min-h-[60vh] items-center overflow-hidden bg-ink-2 py-[120px] max-md:py-[72px]"
      aria-label="开源誓约"
    >
      {/* 背景巨型「公」字（4% 透明，视差） */}
      <span
        className="oath-char pointer-events-none absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 select-none font-serif font-black text-gold opacity-[0.04]"
        style={{ fontSize: '32vh', lineHeight: 1 }}
        aria-hidden="true"
      >
        公
      </span>

      <div className="relative z-10 mx-auto flex w-full max-w-[720px] flex-col items-center px-6 text-center">
        <div className="flex items-center gap-6">
          <span className="h-px w-10 bg-line" aria-hidden="true" />
          <span className="eyebrow">THE OATH</span>
          <span className="h-px w-10 bg-line" aria-hidden="true" />
        </div>
        <h2 className="mt-8 font-serif font-bold text-[clamp(30px,4vw,52px)] leading-[1.15] tracking-[0.05em] text-paper">
          代码属于人民。
        </h2>

        <div className="oath-list mt-14 flex flex-col items-center gap-6">
          {OATHS.map((o) => (
            <div key={o} className="flex items-center gap-5">
              <span
                className="oath-line-bar block h-8 w-[3px] origin-top bg-gold"
                aria-hidden="true"
              />
              <p className="oath-line-text text-[18px] leading-[2.0] tracking-[0.06em] text-paper">
                {o}
              </p>
            </div>
          ))}
        </div>

        <div className="mt-16 flex flex-wrap items-center justify-center gap-5">
          <OutlineButton variant="solid" to="/dna#verify">
            验证这一切的 DNA
          </OutlineButton>
          <OutlineButton variant="ghost" to="/founder">
            认识缔造者
          </OutlineButton>
        </div>
      </div>
    </section>
  )
}
