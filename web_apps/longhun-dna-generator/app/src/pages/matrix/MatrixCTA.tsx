// DNA: #龍芯⚡️丙午·甲申·丁未·亥时·䷎谦-DNA-COMPLETION-f7e5ca65
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
import { useEffect, useRef } from 'react'
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'
import SectionHeading from '@/components/SectionHeading'
import OutlineButton from '@/components/OutlineButton'
import DNACode from '@/components/DNACode'

gsap.registerPlugin(ScrollTrigger)

/** 背景四枚卦符视差（不同速度上浮） */
const BG_HEXES = [
  { char: '䷀', top: '12%', left: '6%', size: 120, speed: -60 },
  { char: '䷁', top: '58%', left: '14%', size: 90, speed: -110 },
  { char: '䷂', top: '20%', left: '84%', size: 110, speed: -80 },
  { char: '䷃', top: '62%', left: '78%', size: 140, speed: -40 },
]

/** S6 · 治理白皮书 CTA（matrix.md S6）—— 纯 GSAP 域 */
export default function MatrixCTA() {
  const ref = useRef<HTMLElement>(null)

  useEffect(() => {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return
    const ctx = gsap.context(() => {
      // 排版孤岛边框绘制 + 入场
      gsap.fromTo(
        '.matrix-cta-island',
        { clipPath: 'inset(0 100% 0 0)' },
        {
          clipPath: 'inset(0 0% 0 0)',
          duration: 0.9,
          ease: 'power2.out',
          scrollTrigger: { trigger: '.matrix-cta-island', start: 'top 80%' },
        },
      )
      gsap.fromTo(
        '.matrix-cta-content',
        { opacity: 0, y: 40 },
        {
          opacity: 1,
          y: 0,
          duration: 0.6,
          ease: 'power3.out',
          scrollTrigger: { trigger: '.matrix-cta-island', start: 'top 80%' },
          delay: 0.3,
        },
      )
      // 四枚卦符不同速度视差上浮
      const hexes = Array.from(
        ref.current?.querySelectorAll<HTMLElement>('.cta-bg-hex') ?? [],
      )
      hexes.forEach((el) => {
        const speed = Number(el.dataset.speed ?? -60)
        gsap.fromTo(
          el,
          { y: 0 },
          {
            y: speed,
            ease: 'none',
            scrollTrigger: { trigger: ref.current, start: 'top bottom', end: 'bottom top', scrub: 1 },
          },
        )
      })
    }, ref)
    return () => ctx.revert()
  }, [])

  return (
    <section
      ref={ref}
      className="relative overflow-hidden bg-ink py-[120px] max-md:py-[72px]"
      aria-label="治理白皮书"
    >
      {/* 背景卦符视差层 */}
      {BG_HEXES.map((h) => (
        <span
          key={h.char}
          className="cta-bg-hex pointer-events-none absolute select-none text-gold-dim opacity-[0.1]"
          style={{ top: h.top, left: h.left, fontSize: h.size, lineHeight: 1 }}
          data-speed={h.speed}
          aria-hidden="true"
        >
          {h.char}
        </span>
      ))}

      <div className="relative mx-auto w-full max-w-container px-6 md:px-12">
        <div className="matrix-cta-island type-island mx-auto max-w-[880px] px-8 py-16 text-center md:px-16 md:py-20">
          <div className="matrix-cta-content">
            <SectionHeading
              align="center"
              eyebrow="THE WHITEPAPER"
              title="十六之外，还有二十。"
              subtitle="《20 人格治理白皮书 v1.4》——矩阵的完整形态，开源可读。"
            />
            <div className="mt-12 flex flex-col items-center justify-center gap-5 sm:flex-row">
              <OutlineButton variant="solid" to="/works#whitepaper">
                阅读白皮书
              </OutlineButton>
              <OutlineButton
                variant="ghost"
                onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}
              >
                返回矩阵顶部
              </OutlineButton>
            </div>
            <DNACode
              className="mx-auto mt-14 max-w-[640px] text-left"
              fontSize={12}
              code="#龍魂⚡️丙午·甲申·己卯·午时-䷀乾为天-WHITEPAPER-v1.4-20P-GOVERNANCE-a3f9c1e7"
            />
            <p className="mt-4 font-mono text-[11px] tracking-[0.16em] text-paper-faint">
              白皮书 DNA 追溯码示例 · 实际以发布时实时干支为准
            </p>
          </div>
        </div>
      </div>
    </section>
  )
}
