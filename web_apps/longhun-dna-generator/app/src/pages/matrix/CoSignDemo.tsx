// DNA: #龍芯⚡️丙午·甲申·丁未·亥时·䷎谦-DNA-COMPLETION-5ee4d299
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
import { useEffect, useRef } from 'react'
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'
import SealTag from '@/components/SealTag'
import { PERSONAS } from '@/pages/matrix/personas'
import PersonaSeal from '@/pages/matrix/PersonaSeal'

gsap.registerPlugin(ScrollTrigger)

/**
 * S4 · 会签演示（matrix.md S4）—— pin 200vh scrub
 * 16 枚签章随滚动依序盖入决议卡；全部签满 → 四边金线绘制 + 「生效」浮现金字
 * 纯 GSAP 域（不引入 Framer Motion）
 */
export default function CoSignDemo() {
  const ref = useRef<HTMLElement>(null)

  useEffect(() => {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return
    const ctx = gsap.context(() => {
      const tl = gsap.timeline({
        scrollTrigger: {
          trigger: ref.current,
          start: 'top top',
          end: '+=200%',
          pin: true,
          scrub: 0.6,
          anticipatePin: 1,
        },
      })

      // 16 枚印章依序盖入：scale 1.8→1, opacity 0→1, rotate -15°→-6°
      const stamps = Array.from(
        ref.current?.querySelectorAll<HTMLElement>('.cosign-stamp') ?? [],
      )
      stamps.forEach((stamp, i) => {
        const at = (i / 16) * 0.82
        tl.fromTo(
          stamp,
          { scale: 1.8, opacity: 0, rotate: -15 },
          { scale: 1, opacity: 1, rotate: -6, duration: 0.05, ease: 'power3.in' },
          at,
        )
        // 卡面轻微震动（y 2px 回弹）
        tl.fromTo(
          '.cosign-card',
          { y: 0 },
          { y: 2, duration: 0.012, ease: 'power2.in', yoyo: true, repeat: 1 },
          at + 0.05,
        )
      })

      // 最后 10%：四边金线绘制
      tl.fromTo('.cosign-edge-t', { scaleX: 0 }, { scaleX: 1, duration: 0.03, ease: 'none' }, 0.88)
      tl.fromTo('.cosign-edge-r', { scaleY: 0 }, { scaleY: 1, duration: 0.03, ease: 'none' }, 0.91)
      tl.fromTo('.cosign-edge-b', { scaleX: 0 }, { scaleX: 1, duration: 0.03, ease: 'none' }, 0.94)
      tl.fromTo('.cosign-edge-l', { scaleY: 0 }, { scaleY: 1, duration: 0.03, ease: 'none' }, 0.97)
      // 「生效」金字弹性浮现
      tl.fromTo(
        '.cosign-effective',
        { scale: 0.6, opacity: 0 },
        { scale: 1, opacity: 1, duration: 0.06, ease: 'back.out(2)' },
        0.94,
      )
    }, ref)
    return () => ctx.revert()
  }, [])

  return (
    <section
      ref={ref}
      className="hairline-b flex min-h-[100dvh] flex-col justify-center overflow-hidden bg-ink py-[120px] max-md:py-[72px]"
      aria-label="会签演示"
    >
      <div className="mx-auto flex w-full max-w-container flex-col items-center px-6 md:px-12">
        <p className="mb-12 text-center text-[13px] tracking-[0.12em] text-paper-dim">
          任何重大决议，须十六人格全体会签——缺一，不生效。
        </p>

        {/* 决议卡 */}
        <div className="cosign-card relative w-full max-w-[480px] border border-line bg-ink-3 p-8 md:p-10">
          {/* 四边金线（签满后绘制） */}
          <span className="cosign-edge-t pointer-events-none absolute left-0 top-0 h-px w-full origin-left scale-x-0 bg-gold-bright" aria-hidden="true" />
          <span className="cosign-edge-r pointer-events-none absolute right-0 top-0 h-full w-px origin-top scale-y-0 bg-gold-bright" aria-hidden="true" />
          <span className="cosign-edge-b pointer-events-none absolute bottom-0 right-0 h-px w-full origin-right scale-x-0 bg-gold-bright" aria-hidden="true" />
          <span className="cosign-edge-l pointer-events-none absolute bottom-0 left-0 h-full w-px origin-bottom scale-y-0 bg-gold-bright" aria-hidden="true" />

          {/* 「生效」金字 */}
          <div className="cosign-effective pointer-events-none absolute inset-x-0 -top-5 flex justify-center opacity-0" aria-hidden="true">
            <span className="border border-gold bg-ink px-6 py-1 font-serif text-[32px] font-black tracking-[0.3em] text-gold">
              生效
            </span>
          </div>

          <div className="flex justify-center">
            <SealTag>决议 · RESOLUTION</SealTag>
          </div>
          <h3 className="mt-6 text-center font-serif text-[24px] font-bold tracking-[0.06em] text-paper">
            开放审计引擎 v2 发布
          </h3>
          <div className="mt-6 space-y-3" aria-hidden="true">
            <div className="h-3 w-full bg-line" />
            <div className="h-3 w-4/5 bg-line" />
          </div>

          {/* 16 格签章位 */}
          <div className="mt-10 grid grid-cols-8 gap-2" role="presentation">
            {PERSONAS.map((p) => (
              <div
                key={p.no}
                className="cosign-stamp flex items-center justify-center opacity-0"
                title={`${p.full} 签章`}
              >
                <PersonaSeal char={p.code[0]} size={28} tone="vermilion" />
              </div>
            ))}
          </div>
          <p className="mt-6 text-center font-mono text-[11px] tracking-[0.2em] text-paper-faint">
            16 / 16 SEALS REQUIRED
          </p>
        </div>
      </div>
    </section>
  )
}
