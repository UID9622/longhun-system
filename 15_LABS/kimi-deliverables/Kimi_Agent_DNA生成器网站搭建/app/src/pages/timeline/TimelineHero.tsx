import { useEffect, useRef } from 'react'
import gsap from 'gsap'
import SealTag from '@/components/SealTag'
import GanzhiCharCanvas from '@/pages/timeline/GanzhiCharCanvas'

const TITLE = '遠征日誌'
const DAY_TEXT = 'DAY 000 / 460'

/**
 * S1 · PageHero（timeline.md）
 * 纯 ink + 自顶部垂落的 1px 金线 + 稀疏干支字符缓落 canvas + 里程读数打字机
 */
export default function TimelineHero() {
  const ref = useRef<HTMLElement>(null)
  const dayRef = useRef<HTMLSpanElement>(null)

  useEffect(() => {
    const dayEl = dayRef.current
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      if (dayEl) dayEl.textContent = DAY_TEXT
      return
    }
    const ctx = gsap.context(() => {
      const tl = gsap.timeline({ defaults: { ease: 'power3.out' } })
      // 金线自顶部 scaleY 0→1（1s，origin top）
      tl.fromTo(
        '.tl-hero-line',
        { scaleY: 0 },
        { scaleY: 1, duration: 1, ease: 'power2.inOut' },
      )
        // H1 逐字 stagger 0.12s
        .fromTo(
          '.tl-hero-char',
          { opacity: 0, y: 40 },
          { opacity: 1, y: 0, duration: 0.6, stagger: 0.12 },
          0.5,
        )
        .fromTo(
          '.tl-hero-eyebrow',
          { opacity: 0, y: 16 },
          { opacity: 1, y: 0, duration: 0.5 },
          0.6,
        )
        .fromTo(
          '.tl-hero-sub',
          { opacity: 0, y: 20 },
          { opacity: 1, y: 0, duration: 0.6 },
          '-=0.3',
        )
      // 里程读数打字机显现
      const counter = { v: 0 }
      tl.to(
        counter,
        {
          v: DAY_TEXT.length,
          duration: 0.8,
          ease: 'none',
          onUpdate: () => {
            if (dayEl) dayEl.textContent = DAY_TEXT.slice(0, Math.round(counter.v))
          },
        },
        '-=0.2',
      )
        .fromTo('.tl-hero-pageseal', { opacity: 0 }, { opacity: 1, duration: 0.5 }, '-=0.2')
    }, ref)
    return () => ctx.revert()
  }, [])

  return (
    <header ref={ref} className="relative flex min-h-[52vh] flex-col overflow-hidden bg-ink">
      {/* 稀疏干支字符缓落 canvas（≤10 字符） */}
      <GanzhiCharCanvas count={8} direction="fall" />
      {/* 自顶部垂落的 1px 金线（与 S2 主轴同 x 位） */}
      <span
        className="tl-hero-line absolute inset-y-0 left-5 w-px origin-top bg-gold md:left-20"
        aria-hidden="true"
      />
      {/* 顶部留白避让 Navbar */}
      <div className="h-[88px] shrink-0" aria-hidden="true" />
      <div className="relative z-10 mx-auto flex w-full max-w-container flex-1 flex-col justify-end px-6 pb-14 md:px-12">
        <span className="tl-hero-eyebrow eyebrow">SCROLL V · THE EXPEDITION</span>
        <h1
          className="mt-6 font-serif font-black text-[clamp(40px,6vw,80px)] leading-[1.1] tracking-[0.05em] text-paper"
          aria-label={TITLE}
        >
          {Array.from(TITLE).map((ch, i) => (
            <span key={i} className="tl-hero-char inline-block" aria-hidden="true">
              {ch}
            </span>
          ))}
        </h1>
        <p className="tl-hero-sub mt-6 max-w-[560px] text-[18px] leading-[1.9] text-paper-dim">
          四百六十天。从一次预见，到一部宪法。
        </p>
        <p className="mt-8 font-mono text-[14px] tracking-[0.2em] text-gold">
          <span ref={dayRef} className="tabular-nums" aria-label="里程读数 DAY 000 / 460" />
          <span className="ml-1 inline-block h-[14px] w-[8px] translate-y-[2px] animate-caret-blink bg-gold" aria-hidden="true" />
        </p>
      </div>
      <div className="tl-hero-pageseal relative z-10 hairline-b">
        <div className="mx-auto flex w-full max-w-container justify-end px-6 pb-4 md:px-12">
          <SealTag>卷五 / LOG</SealTag>
        </div>
      </div>
    </header>
  )
}
