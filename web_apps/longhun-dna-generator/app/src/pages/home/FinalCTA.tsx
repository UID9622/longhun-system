// DNA: #龍芯⚡️丙午·甲申·丁未·亥时·䷎谦-DNA-COMPLETION-de280740
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
import { useEffect, useRef } from 'react'
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'
import OutlineButton from '@/components/OutlineButton'

gsap.registerPlugin(ScrollTrigger)

const CONFIRM_CODE = '#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z'

/** S10 · 终章 CTA（约 70vh，居中排版孤岛） */
export default function FinalCTA() {
  const ref = useRef<HTMLElement>(null)

  useEffect(() => {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return
    const ctx = gsap.context(() => {
      gsap.fromTo(
        '.cta-hex',
        { scale: 0.8, opacity: 0 },
        {
          scale: 1,
          opacity: 1,
          duration: 0.8,
          ease: 'power3.out',
          scrollTrigger: { trigger: ref.current, start: 'top 75%' },
        },
      )
      // 卦符随滚动缓慢旋转 15°
      gsap.fromTo(
        '.cta-hex-rot',
        { rotate: 0 },
        {
          rotate: 15,
          ease: 'none',
          scrollTrigger: { trigger: ref.current, start: 'top bottom', end: 'bottom top', scrub: true },
        },
      )
      // 标题词级 stagger
      gsap.fromTo(
        '.cta-word',
        { y: 30, opacity: 0 },
        {
          y: 0,
          opacity: 1,
          duration: 0.6,
          stagger: 0.08,
          ease: 'power3.out',
          scrollTrigger: { trigger: ref.current, start: 'top 70%' },
        },
      )
      gsap.fromTo(
        '.cta-body',
        { y: 20, opacity: 0 },
        {
          y: 0,
          opacity: 1,
          duration: 0.6,
          ease: 'power3.out',
          scrollTrigger: { trigger: ref.current, start: 'top 65%' },
        },
      )
    }, ref)
    return () => ctx.revert()
  }, [])

  const title = '每一个此刻，都有唯一的干支。'

  return (
    <section
      ref={ref}
      className="relative flex min-h-[70vh] items-center overflow-hidden bg-ink"
      aria-label="终章"
    >
      {/* 巨型卦符（gold-dim，随滚动旋转） */}
      <span className="cta-hex pointer-events-none absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2" aria-hidden="true">
        <span className="cta-hex-rot block select-none font-serif text-[160px] leading-none text-gold-dim opacity-40">
          ䷀
        </span>
      </span>

      <div className="relative z-10 mx-auto w-full max-w-[880px] px-6 py-24 text-center">
        <h2 className="font-serif font-black leading-[1.4] tracking-[0.05em] text-paper" style={{ fontSize: 'clamp(30px, 4vw, 52px)' }}>
          {Array.from(title).map((ch, i) => (
            <span key={i} className="cta-word inline-block">
              {ch}
            </span>
          ))}
        </h2>
        <div className="cta-body">
          <p className="mx-auto mt-8 max-w-[560px] text-[18px] leading-[1.9] text-paper-dim">
            生成属于你这一刻的龍魂 DNA——免费、开源、永远如此。
          </p>
          <div className="mt-12 flex justify-center">
            <OutlineButton to="/dna" variant="solid" className="animate-gold-breathe">
              生成此刻 DNA
            </OutlineButton>
          </div>
          <p className="mt-8 break-all font-mono text-[11px] tracking-[0.04em] text-vermilion">{CONFIRM_CODE}</p>
        </div>
      </div>
    </section>
  )
}
