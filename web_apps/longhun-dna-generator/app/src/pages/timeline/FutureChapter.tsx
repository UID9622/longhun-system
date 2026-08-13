import { useEffect, useRef } from 'react'
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'
import OutlineButton from '@/components/OutlineButton'

gsap.registerPlugin(ScrollTrigger)

const H2_SEGMENTS = ['下一座里程碑，', '由你书写。']

/**
 * S4 · 未来空白章（timeline.md）
 * 金线中断为虚线向前延伸 · 日期占位闪烁光标 · 双 CTA 呼吸描边
 */
export default function FutureChapter() {
  const ref = useRef<HTMLElement>(null)

  useEffect(() => {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return
    const ctx = gsap.context(() => {
      gsap.fromTo(
        '.future-date',
        { opacity: 0, y: 16 },
        {
          opacity: 1,
          y: 0,
          duration: 0.6,
          ease: 'power3.out',
          scrollTrigger: { trigger: ref.current, start: 'top 62%' },
        },
      )
      // H2 词级 stagger 0.1s
      gsap.fromTo(
        '.future-word',
        { y: 30, opacity: 0 },
        {
          y: 0,
          opacity: 1,
          duration: 0.6,
          stagger: 0.1,
          ease: 'power3.out',
          scrollTrigger: { trigger: ref.current, start: 'top 58%' },
        },
      )
      gsap.fromTo(
        '.future-sub, .future-cta',
        { y: 24, opacity: 0 },
        {
          y: 0,
          opacity: 1,
          duration: 0.6,
          stagger: 0.12,
          ease: 'power3.out',
          scrollTrigger: { trigger: ref.current, start: 'top 52%' },
        },
      )
    }, ref)
    return () => ctx.revert()
  }, [])

  return (
    <section
      ref={ref}
      className="relative flex min-h-[70vh] items-center overflow-hidden hairline-t bg-ink-2"
      aria-label="未来空白章"
    >
      {/* 金线中断为虚线，向前延伸至视口外（stroke-dashoffset 15s 无限流转） */}
      <svg
        className="absolute left-5 top-0 h-[130%] w-px md:left-20"
        width="1"
        height="130%"
        preserveAspectRatio="none"
        aria-hidden="true"
      >
        <line
          x1="0.5"
          y1="0"
          x2="0.5"
          y2="100%"
          stroke="#C9A227"
          strokeWidth="1"
          strokeDasharray="6 6"
          className="animate-dash-rotate"
          style={{ animationDuration: '15s' }}
        />
      </svg>

      <div className="relative z-10 mx-auto flex w-full max-w-[720px] flex-col items-center px-6 py-[120px] text-center">
        {/* mono 日期占位 + 闪烁光标块 */}
        <p className="future-date font-mono text-[15px] tracking-[0.3em] text-paper-faint">
          20XX-XX-XX
          <span
            className="ml-2 inline-block h-[14px] w-[9px] translate-y-[2px] animate-caret-blink bg-paper-faint"
            aria-hidden="true"
          />
        </p>
        <h2 className="mt-8 font-serif font-black text-[clamp(30px,4.5vw,56px)] leading-[1.2] tracking-[0.05em] text-paper">
          {H2_SEGMENTS.map((seg, i) => (
            <span key={i} className="future-word inline-block">
              {seg}
            </span>
          ))}
        </h2>
        <p className="future-sub mt-8 max-w-[560px] text-[18px] leading-[1.9] tracking-[0.02em] text-paper-dim">
          开源在此。Fork 它，铸造它，把你的干支刻进来。
        </p>
        <div className="future-cta mt-14 flex flex-wrap items-center justify-center gap-5">
          <span className="inline-block animate-gold-breathe">
            <OutlineButton variant="solid" to="/dna">
              铸造我的 DNA
            </OutlineButton>
          </span>
          <OutlineButton variant="ghost" to="/protocol">
            阅读协议
          </OutlineButton>
        </div>
      </div>
    </section>
  )
}
