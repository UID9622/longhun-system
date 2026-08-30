// DNA: #龍芯⚡️丙午·甲申·丁未·亥时·䷎谦-DNA-COMPLETION-79f74d6c
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
import { useEffect, useRef } from 'react'
import gsap from 'gsap'
import SealTag from '@/components/SealTag'

const TITLE = '作品開源'
const SEALS = ['免费', '开源', '可审计']

/**
 * S1 · PageHero（works.md）
 * protocol-banner.png 复用（10% 透明，水平镜像）· H1 逐字入场 · 三枚 SealTag 盖章式入场
 */
export default function WorksHero() {
  const ref = useRef<HTMLElement>(null)

  useEffect(() => {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return
    const ctx = gsap.context(() => {
      const tl = gsap.timeline({ defaults: { ease: 'power3.out' } })
      tl.fromTo(
        '.works-hero-bg',
        { opacity: 0 },
        { opacity: 0.1, duration: 1.2, ease: 'power2.out' },
      )
        .fromTo(
          '.works-hero-eyebrow',
          { opacity: 0, y: 16 },
          { opacity: 1, y: 0, duration: 0.5 },
          0.2,
        )
        .fromTo(
          '.works-hero-char',
          { opacity: 0, y: 40 },
          { opacity: 1, y: 0, duration: 0.6, stagger: 0.12 },
          0.35,
        )
        .fromTo(
          '.works-hero-sub',
          { opacity: 0, y: 20 },
          { opacity: 1, y: 0, duration: 0.6 },
          '-=0.2',
        )
        .fromTo(
          '.works-hero-seal',
          { opacity: 0, scale: 1.4 },
          { opacity: 1, scale: 1, duration: 0.4, stagger: 0.15, ease: 'power2.in' },
          '-=0.3',
        )
        .fromTo(
          '.works-hero-pageseal',
          { opacity: 0 },
          { opacity: 1, duration: 0.5 },
          '-=0.1',
        )
    }, ref)
    return () => ctx.revert()
  }, [])

  return (
    <header ref={ref} className="relative flex min-h-[52vh] flex-col overflow-hidden">
      {/* 卷轴纹：10% 透明 · 水平镜像 */}
      <div
        className="works-hero-bg pointer-events-none absolute inset-0 opacity-10"
        style={{
          backgroundImage: "url('/protocol-banner.png')",
          backgroundSize: 'cover',
          backgroundPosition: 'center',
          transform: 'scaleX(-1)',
        }}
        aria-hidden="true"
      />
      <div
        className="pointer-events-none absolute inset-0"
        style={{
          background:
            'radial-gradient(ellipse at 50% 80%, transparent 20%, rgba(8,7,6,0.92) 100%)',
        }}
        aria-hidden="true"
      />
      {/* 顶部留白避让 Navbar */}
      <div className="h-[88px] shrink-0" aria-hidden="true" />
      <div className="relative z-10 mx-auto flex w-full max-w-container flex-1 items-end justify-between gap-10 px-6 pb-14 md:px-12">
        <div className="flex flex-col justify-end">
          <span className="works-hero-eyebrow eyebrow">SCROLL IV · OPEN WORKS</span>
          <h1
            className="mt-6 font-serif font-black text-[clamp(40px,6vw,80px)] leading-[1.1] tracking-[0.05em] text-paper"
            aria-label={TITLE}
          >
            {Array.from(TITLE).map((ch, i) => (
              <span key={i} className="works-hero-char inline-block" aria-hidden="true">
                {ch}
              </span>
            ))}
          </h1>
          <p className="works-hero-sub mt-6 max-w-[560px] text-[18px] leading-[1.9] text-paper-dim">
            七器皆开源。不做专利，不走资本，每一行代码属于人民。
          </p>
        </div>
        {/* 右侧三枚 SealTag 纵排 */}
        <div className="hidden shrink-0 flex-col items-end gap-4 md:flex">
          {SEALS.map((s) => (
            <span key={s} className="works-hero-seal inline-block">
              <SealTag>{s}</SealTag>
            </span>
          ))}
        </div>
      </div>
      <div className="works-hero-pageseal relative z-10 hairline-b">
        <div className="mx-auto flex w-full max-w-container justify-end px-6 pb-4 md:px-12">
          <SealTag>卷四 / WORKS</SealTag>
        </div>
      </div>
    </header>
  )
}
