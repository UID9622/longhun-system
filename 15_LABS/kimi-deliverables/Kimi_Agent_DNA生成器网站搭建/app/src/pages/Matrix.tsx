import { useEffect, useRef } from 'react'
import gsap from 'gsap'
import SealTag from '@/components/SealTag'
import FivePillars from '@/pages/matrix/FivePillars'
import MatrixGrid from '@/pages/matrix/MatrixGrid'
import CoSignDemo from '@/pages/matrix/CoSignDemo'
import DimensionMixer from '@/pages/matrix/DimensionMixer'
import MatrixCTA from '@/pages/matrix/MatrixCTA'

/**
 * /matrix · 16 人格矩阵（matrix.md）
 * S1 PageHero → S2 五维思维柱 → S3 4×4 交互矩阵 → S4 会签演示 → S5 五维调配 → S6 白皮书 CTA
 */
export default function Matrix() {
  const heroRef = useRef<HTMLElement>(null)

  useEffect(() => {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return
    const ctx = gsap.context(() => {
      // H1 逐字 y:70→0 stagger 0.12s
      gsap.fromTo(
        '.matrix-hero-char',
        { y: 70, opacity: 0 },
        { y: 0, opacity: 1, duration: 0.8, ease: 'power3.out', stagger: 0.12, delay: 0.15 },
      )
      gsap.fromTo(
        '.matrix-hero-sub',
        { y: 20, opacity: 0 },
        { y: 0, opacity: 1, duration: 0.6, ease: 'power2.out', delay: 0.7 },
      )
      // 八卦盘显影：opacity 0→6%, rotate -10°→0°（1.2s）
      gsap.fromTo(
        '.matrix-hero-bagua',
        { opacity: 0, rotate: -10 },
        { opacity: 0.06, rotate: 0, duration: 1.2, ease: 'power2.out' },
      )
    }, heroRef)
    return () => ctx.revert()
  }, [])

  const title = '十六人格'

  return (
    <>
      {/* S1 · PageHero（matrix.md S1） */}
      <header
        ref={heroRef}
        className="relative flex min-h-[52vh] flex-col overflow-hidden"
        aria-label="矩阵页头"
      >
        {/* matrix-grid-bg.png 12% */}
        <div
          className="pointer-events-none absolute inset-0 opacity-[0.12]"
          style={{
            backgroundImage: "url('/matrix-grid-bg.png')",
            backgroundSize: 'min(80vw, 720px)',
            backgroundPosition: 'center',
            backgroundRepeat: 'repeat',
          }}
          aria-hidden="true"
        />
        {/* bagua-ring.svg 80vh 居右，160s/圈极缓 */}
        <img
          src="/bagua-ring.svg"
          alt=""
          className="matrix-hero-bagua pointer-events-none absolute right-[-10%] top-1/2 aspect-square h-[80vh] -translate-y-1/2 animate-spin-slow opacity-0"
          style={{ animationDuration: '160s' }}
          aria-hidden="true"
        />
        <div
          className="pointer-events-none absolute inset-0"
          style={{
            background: 'radial-gradient(ellipse at 40% 80%, transparent 20%, rgba(8,7,6,0.92) 100%)',
          }}
          aria-hidden="true"
        />
        {/* 顶部留白避让 Navbar */}
        <div className="h-[88px] shrink-0" aria-hidden="true" />
        <div className="relative z-10 mx-auto flex w-full max-w-container flex-1 flex-col justify-end px-6 pb-14 md:px-12">
          <span className="eyebrow">SCROLL III · THE COUNCIL</span>
          <h1
            className="mt-6 font-serif text-[clamp(40px,6vw,80px)] font-black leading-[1.1] tracking-[0.05em] text-paper"
            aria-label={title}
          >
            {Array.from(title).map((ch, i) => (
              <span key={i} className="matrix-hero-char inline-block" aria-hidden="true">
                {ch}
              </span>
            ))}
          </h1>
          <p className="matrix-hero-sub mt-6 max-w-[560px] text-[18px] leading-[1.9] text-paper-dim">
            一个系统，十六重人格。军事、历史、哲学、经济、政治——五维思维，内阁共治。
          </p>
        </div>
        <div className="hairline-b relative z-10">
          <div className="mx-auto flex w-full max-w-container justify-end px-6 pb-4 md:px-12">
            <SealTag>卷三 / MATRIX</SealTag>
          </div>
        </div>
      </header>

      <FivePillars />
      <MatrixGrid />
      <CoSignDemo />
      <DimensionMixer />
      <MatrixCTA />
    </>
  )
}
