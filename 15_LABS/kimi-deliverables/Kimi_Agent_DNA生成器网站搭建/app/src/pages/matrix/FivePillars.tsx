import { useEffect, useRef } from 'react'
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'
import SectionHeading from '@/components/SectionHeading'
import { DIMS } from '@/pages/matrix/personas'

gsap.registerPlugin(ScrollTrigger)

/** 柱高错落：军事最高 240px，依次 -20px */
const HEIGHTS = [240, 220, 200, 180, 160]

/** S2 · 五维思维总纲 —— 五柱星盘（matrix.md S2） */
export default function FivePillars() {
  const ref = useRef<HTMLElement>(null)

  useEffect(() => {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return
    const ctx = gsap.context(() => {
      gsap.fromTo(
        '.dim-pillar',
        { scaleY: 0 },
        {
          scaleY: 1,
          duration: 0.7,
          ease: 'power2.out',
          transformOrigin: 'bottom',
          stagger: 0.12,
          scrollTrigger: { trigger: '.pillars-base', start: 'top 80%' },
        },
      )
      gsap.fromTo(
        '.dim-pillar-text',
        { opacity: 0, y: 12 },
        {
          opacity: 1,
          y: 0,
          duration: 0.5,
          ease: 'power2.out',
          stagger: 0.12,
          delay: 0.35,
          scrollTrigger: { trigger: '.pillars-base', start: 'top 80%' },
        },
      )
    }, ref)
    return () => ctx.revert()
  }, [])

  return (
    <section ref={ref} className="hairline-b bg-ink py-[120px] max-md:py-[72px]" aria-label="五维思维总纲">
      <div className="mx-auto w-full max-w-container px-6 md:px-12">
        <SectionHeading
          eyebrow="FIVE DIMENSIONS"
          title="五维 · 思维之柱"
          subtitle="军事、历史、哲学、经济、政治——五根柱子撑起十六人格的内阁。柱之高低，喻其在决断中的权重。"
        />

        <div className="pillars-base mt-20 grid grid-cols-1 gap-8 md:grid-cols-5 md:gap-6">
          {DIMS.map((d, i) => (
            <div key={d.key} className="group flex flex-col items-center md:justify-end">
              {/* 柱体 */}
              <div
                className="dim-pillar relative flex w-full flex-col items-center justify-between border border-line bg-ink-3 px-4 py-6 transition-colors duration-400 group-hover:border-gold md:max-w-[180px]"
                style={{ height: HEIGHTS[i] }}
              >
                {/* hover 金色渐变提亮（自下而上） */}
                <span
                  className="pointer-events-none absolute inset-0 origin-bottom scale-y-0 transition-transform duration-500 ease-out group-hover:scale-y-100"
                  style={{
                    background:
                      'linear-gradient(0deg, rgba(201,162,39,0.18) 0%, rgba(201,162,39,0.02) 100%)',
                  }}
                  aria-hidden="true"
                />
                <span
                  className="dim-pillar-text select-none text-[30px] leading-none text-gold-dim transition-colors duration-400 group-hover:text-gold"
                  aria-hidden="true"
                >
                  {d.trigram}
                </span>
                <div className="dim-pillar-text flex flex-col items-center gap-3">
                  <h3 className="font-serif text-[28px] font-bold tracking-[0.04em] text-paper transition-[letter-spacing] duration-400 group-hover:tracking-[0.12em]">
                    {d.name}
                  </h3>
                  <p className="text-center text-[14px] leading-[1.8] text-paper-dim">{d.desc}</p>
                  <span className="font-mono text-[12px] tracking-[0.3em] text-gold-dim transition-colors duration-400 group-hover:text-gold">
                    {d.key}
                  </span>
                </div>
                {/* 顶部 2px 金条 */}
                <span
                  className="absolute left-0 top-0 h-[2px] w-full origin-left scale-x-0 bg-gold transition-transform duration-300 group-hover:scale-x-100"
                  aria-hidden="true"
                />
              </div>
            </div>
          ))}
        </div>
        {/* 1px 金线基座 */}
        <div className="mt-0 h-px w-full bg-gold-dim" aria-hidden="true" />
      </div>
    </section>
  )
}
