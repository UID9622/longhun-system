import { useEffect, useRef } from 'react'
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'
import SealTag from '@/components/SealTag'

gsap.registerPlugin(ScrollTrigger)

/**
 * S3 · 宣言（排版孤岛，ScrollTrigger pin 150vh）
 * 主句按短句逐行点亮（scrub），金句伴下划金线，背景巨「民」视差
 */
export default function Manifesto() {
  const ref = useRef<HTMLElement>(null)

  useEffect(() => {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return
    const ctx = gsap.context(() => {
      const tl = gsap.timeline({
        scrollTrigger: {
          trigger: ref.current,
          start: 'top top',
          end: '+=150%',
          pin: true,
          scrub: 0.6,
        },
      })
      tl.fromTo('.manifesto-line-1', { opacity: 0.12 }, { opacity: 1, duration: 1 })
        .fromTo('.manifesto-line-2', { opacity: 0.12 }, { opacity: 1, duration: 1 })
        .fromTo('.manifesto-underline', { scaleX: 0 }, { scaleX: 1, duration: 1, ease: 'none' }, '<')
        .fromTo(
          '.manifesto-tag',
          { scale: 0.9, opacity: 0 },
          { scale: 1, opacity: 1, duration: 0.8, stagger: 0.12 },
        )
      // 背景「民」视差
      gsap.fromTo(
        '.manifesto-min',
        { y: 60 },
        {
          y: -60,
          ease: 'none',
          scrollTrigger: { trigger: ref.current, start: 'top bottom', end: 'bottom top', scrub: true },
        },
      )
    }, ref)
    return () => ctx.revert()
  }, [])

  return (
    <section
      ref={ref}
      className="hairline-b relative flex min-h-[80vh] items-center overflow-hidden bg-ink"
      aria-label="宣言"
    >
      {/* 极淡巨型「民」 */}
      <span
        className="manifesto-min pointer-events-none absolute right-[8%] top-1/2 -translate-y-1/2 select-none font-serif font-black text-paper opacity-[0.04]"
        style={{ fontSize: '40vh', lineHeight: 1 }}
        aria-hidden="true"
      >
        民
      </span>

      <div className="relative z-10 mx-auto w-full max-w-[880px] px-6 py-24 text-center">
        <SealTag className="mx-auto">宣言 / MANIFESTO</SealTag>
        <h2
          className="mt-10 font-serif font-black leading-[1.6] text-paper"
          style={{ fontSize: 'clamp(28px, 4vw, 48px)' }}
        >
          <span className="manifesto-line-1 block">「我们不做专利，不做企业，不走资本。</span>
          <span className="manifesto-line-2 relative mt-2 inline-block text-gold">
            龍魂系统免费开源，为人民服务，数据主权在民。」
            <span
              className="manifesto-underline absolute -bottom-2 left-0 h-px w-full origin-left bg-gold"
              aria-hidden="true"
            />
          </span>
        </h2>
        <div className="mt-14 flex flex-wrap items-center justify-center gap-4">
          <span className="manifesto-tag inline-block">
            <SealTag>零黑箱承诺</SealTag>
          </span>
          <span className="manifesto-tag inline-block">
            <SealTag>不删除，只冻结</SealTag>
          </span>
          <span className="manifesto-tag inline-block">
            <SealTag>创建者不可剥夺</SealTag>
          </span>
        </div>
      </div>
    </section>
  )
}
