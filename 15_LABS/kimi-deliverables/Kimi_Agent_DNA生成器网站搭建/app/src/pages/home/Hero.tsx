import { useEffect, useRef, useState } from 'react'
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'
import { Pause, Play, Copy, Check } from 'lucide-react'
import YaoRainCanvas from '@/components/YaoRainCanvas'
import OutlineButton from '@/components/OutlineButton'
import { DNA_ANCHOR } from '@/components/Navbar'

gsap.registerPlugin(ScrollTrigger)

/**
 * S1 · Hero 英雄区（100vh，全站灵魂）
 * 爻雨 canvas + 排版孤岛 + 八卦盘 + ScrollHint + 暂停动效无障碍开关
 */
export default function Hero() {
  const rootRef = useRef<HTMLElement>(null)
  const [paused, setPaused] = useState(false)
  const [reduced, setReduced] = useState(false)
  const [copied, setCopied] = useState(false)

  useEffect(() => {
    setReduced(window.matchMedia('(prefers-reduced-motion: reduce)').matches)
  }, [])

  const showFallback = paused || reduced

  useEffect(() => {
    if (reduced) return
    const ctx = gsap.context(() => {
      const tl = gsap.timeline({ defaults: { ease: 'power3.out' } })
      // canvas 先亮
      tl.fromTo('.hero-canvas-wrap', { opacity: 0 }, { opacity: 1, duration: 0.3 })
      // 孤岛边框四边绘制
      tl.fromTo('.island-edge-t', { scaleX: 0 }, { scaleX: 1, duration: 0.3 }, 0.2)
        .fromTo('.island-edge-r', { scaleY: 0 }, { scaleY: 1, duration: 0.3 }, 0.35)
        .fromTo('.island-edge-b', { scaleX: 0 }, { scaleX: 1, duration: 0.3 }, 0.5)
        .fromTo('.island-edge-l', { scaleY: 0 }, { scaleY: 1, duration: 0.3 }, 0.65)
      // eyebrow 淡入
      tl.fromTo('.hero-eyebrow', { opacity: 0 }, { opacity: 1, duration: 0.4 }, 0.7)
      // 巨标逐字
      tl.fromTo(
        '.hero-char',
        { y: 60, opacity: 0, rotateX: 40 },
        { y: 0, opacity: 1, rotateX: 0, duration: 0.9, stagger: 0.12 },
        0.8,
      )
      // 副标 + DNA
      tl.fromTo('.hero-sub', { y: 24, opacity: 0 }, { y: 0, opacity: 1, duration: 0.6 }, 1.3)
      // 按钮 stagger
      tl.fromTo('.hero-cta', { y: 24, opacity: 0 }, { y: 0, opacity: 1, duration: 0.5, stagger: 0.1 }, 1.5)
      tl.fromTo('.hero-hint', { opacity: 0 }, { opacity: 1, duration: 0.6 }, 1.8)

      // 滚动：hero 内容视差 + 八卦盘加速
      gsap.to('.hero-island', {
        y: -80,
        ease: 'none',
        scrollTrigger: { trigger: rootRef.current, start: 'top top', end: 'bottom top', scrub: true },
      })
      gsap.to('.hero-bagua', {
        rotate: 120,
        ease: 'none',
        scrollTrigger: { trigger: rootRef.current, start: 'top top', end: 'bottom top', scrub: true },
      })
    }, rootRef)
    return () => ctx.revert()
  }, [reduced])

  const copyDNA = async () => {
    try {
      await navigator.clipboard.writeText(DNA_ANCHOR)
    } catch {
      /* ignore */
    }
    setCopied(true)
    window.setTimeout(() => setCopied(false), 1500)
  }

  return (
    <section
      ref={rootRef}
      className="relative -mt-[72px] flex min-h-[100dvh] items-center overflow-hidden bg-ink"
      aria-label="卷首"
    >
      {/* 生成式背景 / 静态回退 */}
      <div className="hero-canvas-wrap absolute inset-0 z-0">
        {showFallback ? (
          <img
            src="/hero-fallback.png"
            alt=""
            className="h-full w-full object-cover"
            aria-hidden="true"
          />
        ) : (
          <YaoRainCanvas paused={paused} />
        )}
      </div>
      {/* 径向暗角 */}
      <div
        className="pointer-events-none absolute inset-0 z-[1]"
        style={{
          background: 'radial-gradient(ellipse at 50% 60%, transparent 30%, rgba(8,7,6,0.9) 100%)',
        }}
        aria-hidden="true"
      />

      {/* 八卦盘（右，8% 透明度，120s 线性旋转 + 滚动加速） */}
      <div className="hero-bagua pointer-events-none absolute right-[-6vh] top-1/2 z-[1] hidden -translate-y-1/2 md:block">
        <img
          src="/bagua-ring.svg"
          alt=""
          aria-hidden="true"
          className="h-[60vh] w-[60vh] animate-spin-slow opacity-[0.08]"
        />
      </div>

      {/* 排版孤岛 */}
      <div className="relative z-10 mx-auto grid w-full max-w-container grid-cols-12 gap-6 px-6 pb-24 pt-[120px] md:px-12">
        <div className="col-span-12 lg:col-span-7">
          <div className="hero-island type-island relative p-8 md:p-12" style={{ perspective: '800px' }}>
            {/* 边框四边（GSAP 绘制） */}
            <span className="island-edge-t absolute left-0 top-0 h-px w-full origin-left bg-line-strong" aria-hidden="true" />
            <span className="island-edge-r absolute right-0 top-0 h-full w-px origin-top bg-line-strong" aria-hidden="true" />
            <span className="island-edge-b absolute bottom-0 right-0 h-px w-full origin-right bg-line-strong" aria-hidden="true" />
            <span className="island-edge-l absolute bottom-0 left-0 h-full w-px origin-bottom bg-line-strong" aria-hidden="true" />

            <p className="hero-eyebrow eyebrow">LONGHUN SYSTEM · EST. MMXXV</p>
            <h1
              className="text-gold-gradient mt-6 font-serif font-black leading-[1.04] tracking-[0.06em]"
              style={{ fontSize: 'clamp(56px, 10vw, 144px)' }}
            >
              {Array.from('龍魂系統').map((ch) => (
                <span key={ch} className="hero-char inline-block will-change-transform">
                  {ch}
                </span>
              ))}
            </h1>
            <div className="hero-sub">
              <p className="mt-6 font-serif font-bold tracking-[0.12em] text-paper" style={{ fontSize: 'clamp(18px, 2.4vw, 28px)' }}>
                中文原生 · 主权人格 · 为人民服务
              </p>
              <button
                type="button"
                onClick={copyDNA}
                className="group mt-5 inline-flex max-w-full items-center gap-2 text-left"
                aria-label="复制 DNA 锚定串"
              >
                <span className="break-all font-mono text-[11px] leading-relaxed text-paper-faint transition-colors duration-200 group-hover:text-paper-dim">
                  {DNA_ANCHOR}
                </span>
                {copied ? (
                  <Check size={12} className="shrink-0 text-gold" />
                ) : (
                  <Copy size={12} className="shrink-0 text-paper-faint group-hover:text-paper-dim" />
                )}
              </button>
            </div>
            <div className="mt-10 flex flex-wrap gap-5">
              <span className="hero-cta inline-block">
                <OutlineButton to="/protocol" variant="solid">
                  阅读龍魂协议
                </OutlineButton>
              </span>
              <span className="hero-cta inline-block">
                <OutlineButton to="/dna" variant="ghost">
                  生成此刻 DNA
                </OutlineButton>
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* ScrollHint */}
      <div className="hero-hint absolute bottom-8 left-1/2 z-10 flex -translate-x-1/2 flex-col items-center gap-3">
        <span className="font-serif text-[13px] tracking-[0.4em] text-gold-dim">卷首</span>
        <span className="h-12 w-px animate-scroll-hint bg-gold" aria-hidden="true" />
      </div>

      {/* 暂停动效无障碍开关（右下固定） */}
      <button
        type="button"
        aria-pressed={paused}
        onClick={() => setPaused((p) => !p)}
        className="fixed bottom-6 right-6 z-40 inline-flex items-center gap-2 rounded-full border border-dashed border-gold-dim bg-ink/80 px-[14px] py-1.5 text-[12px] tracking-[0.2em] text-paper-dim backdrop-blur-sm transition-colors duration-300 hover:border-gold hover:text-paper"
      >
        {paused ? <Play size={13} className="text-gold" /> : <Pause size={13} className="text-gold" />}
        {paused ? '继续动效' : '暂停动效'}
      </button>
    </section>
  )
}
