import { useEffect, useRef, useState } from 'react'
import gsap from 'gsap'
import SealTag from '@/components/SealTag'
import VermilionSeal from '@/pages/protocol/VermilionSeal'

/** 极慢下落的隶书笔画粒子（≤10 粒，金色蚕头燕尾横画） */
function StrokeRain({ paused }: { paused: boolean }) {
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const pausedRef = useRef(paused)

  useEffect(() => {
    pausedRef.current = paused
  }, [paused])

  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return
    const ctx = canvas.getContext('2d')
    if (!ctx) return

    let raf = 0
    let visible = true
    const dpr = Math.min(window.devicePixelRatio || 1, 2)
    const particles = Array.from({ length: 9 }, () => ({
      x: Math.random(),
      y: Math.random(),
      len: 40 + Math.random() * 80,
      speed: 0.00022 + Math.random() * 0.00028,
      sway: 0.6 + Math.random() * 1.4,
      phase: Math.random() * Math.PI * 2,
      alpha: 0.12 + Math.random() * 0.22,
    }))

    const resize = () => {
      const { clientWidth, clientHeight } = canvas
      canvas.width = clientWidth * dpr
      canvas.height = clientHeight * dpr
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0)
    }
    resize()
    window.addEventListener('resize', resize)

    const io = new IntersectionObserver(([e]) => {
      visible = e.isIntersecting
    })
    io.observe(canvas)

    const drawStroke = (x: number, y: number, len: number, alpha: number) => {
      // 隶书横画：蚕头（左粗圆）→ 细腰 → 燕尾（右上挑）
      ctx.save()
      ctx.translate(x, y)
      ctx.strokeStyle = `rgba(201,162,39,${alpha})`
      ctx.lineCap = 'round'
      ctx.lineWidth = 2.6
      ctx.beginPath()
      ctx.moveTo(0, 0)
      ctx.bezierCurveTo(len * 0.3, 1.5, len * 0.7, -1.5, len, -3)
      ctx.stroke()
      // 蚕头
      ctx.fillStyle = `rgba(201,162,39,${alpha})`
      ctx.beginPath()
      ctx.arc(0, 0, 2.2, 0, Math.PI * 2)
      ctx.fill()
      // 燕尾
      ctx.beginPath()
      ctx.moveTo(len - 10, -2)
      ctx.lineTo(len, -4.5)
      ctx.lineTo(len - 4, 0.5)
      ctx.closePath()
      ctx.fill()
      ctx.restore()
    }

    let t = 0
    const loop = () => {
      raf = requestAnimationFrame(loop)
      if (!visible || pausedRef.current) return
      t += 1
      const w = canvas.clientWidth
      const h = canvas.clientHeight
      ctx.clearRect(0, 0, w, h)
      for (const p of particles) {
        p.y += p.speed
        if (p.y > 1.1) {
          p.y = -0.1
          p.x = Math.random()
        }
        const x = p.x * w + Math.sin(t / 90 + p.phase) * p.sway * 10
        drawStroke(x, p.y * h, p.len, p.alpha)
      }
    }
    loop()

    return () => {
      cancelAnimationFrame(raf)
      window.removeEventListener('resize', resize)
      io.disconnect()
    }
  }, [])

  return (
    <canvas
      ref={canvasRef}
      style={{ position: 'absolute', inset: 0, width: '100%', height: '100%', zIndex: 1 }}
      aria-hidden="true"
    />
  )
}

/**
 * S1 · PageHero（52vh）
 * protocol-banner.png 18% + ink 渐变罩 · 隶书笔画粒子 · 逐字 H1 · 朱砂「焊死」盖章入场
 */
export default function ProtocolHero() {
  const rootRef = useRef<HTMLElement>(null)
  const [reduced] = useState(() => window.matchMedia('(prefers-reduced-motion: reduce)').matches)

  useEffect(() => {
    if (reduced) return
    const ctx = gsap.context(() => {
      const tl = gsap.timeline({ defaults: { ease: 'power3.out' } })
      tl.fromTo('.ph-eyebrow', { opacity: 0 }, { opacity: 1, duration: 0.4 }, 0.1)
      // H1 四字逐字 y:80→0, rotateX 50°→0，stagger 0.14s
      tl.fromTo(
        '.ph-char',
        { y: 80, opacity: 0, rotateX: 50 },
        { y: 0, opacity: 1, rotateX: 0, duration: 0.9, stagger: 0.14 },
        0.25,
      )
      // 副题 y:24→0 延迟 0.5s
      tl.fromTo('.ph-sub', { y: 24, opacity: 0 }, { y: 0, opacity: 1, duration: 0.6 }, 0.5)
      // 朱砂印 0.9s 盖章入场 + 冲击环
      tl.fromTo(
        '.ph-seal',
        { scale: 1.6, opacity: 0 },
        { scale: 1, opacity: 1, duration: 0.28, ease: 'power4.in' },
        0.9,
      )
      tl.fromTo(
        '.ph-seal-ring',
        { scale: 0.6, opacity: 0.9 },
        { scale: 2.4, opacity: 0, duration: 0.4, ease: 'power2.out' },
        1.18,
      )
      tl.fromTo('.ph-seal-tag', { opacity: 0 }, { opacity: 1, duration: 0.5 }, 1.3)
    }, rootRef)
    return () => ctx.revert()
  }, [reduced])

  return (
    <header
      ref={rootRef}
      className="relative flex min-h-[52vh] flex-col overflow-hidden"
      aria-label="龍魂协议页头"
    >
      {/* 背景：protocol-banner.png 18% + ink 渐变罩 */}
      <div
        className="pointer-events-none absolute inset-0 opacity-[0.18]"
        style={{
          backgroundImage: 'url(/protocol-banner.png)',
          backgroundSize: 'cover',
          backgroundPosition: 'center',
        }}
        aria-hidden="true"
      />
      <div
        className="pointer-events-none absolute inset-0"
        style={{
          background:
            'radial-gradient(ellipse at 50% 80%, rgba(8,7,6,0.55) 0%, rgba(8,7,6,0.94) 100%)',
        }}
        aria-hidden="true"
      />
      {!reduced ? <StrokeRain paused={false} /> : null}

      {/* 顶部留白避让 Navbar（Layout 已垫 72px，合计 160px） */}
      <div className="h-[88px] shrink-0" aria-hidden="true" />

      <div className="relative z-10 mx-auto flex w-full max-w-container flex-1 flex-col justify-end px-6 pb-14 md:px-12">
        <span className="ph-eyebrow eyebrow">SCROLL I · THE CONSTITUTION</span>
        <div className="mt-6 flex items-end justify-between gap-8">
          <h1
            className="font-serif font-black text-[clamp(40px,6vw,80px)] leading-[1.1] tracking-[0.05em] text-gold"
            style={{ perspective: '800px' }}
          >
            {Array.from('龍魂協議').map((ch) => (
              <span key={ch} className="ph-char inline-block will-change-transform">
                {ch}
              </span>
            ))}
          </h1>
          {/* 朱砂方印「焊死」 rotate -6° */}
          <div className="relative mb-2 hidden shrink-0 sm:block">
            <span
              className="ph-seal-ring pointer-events-none absolute inset-0 border border-ink"
              aria-hidden="true"
            />
            <VermilionSeal chars={['焊', '死']} size={64} rotate={-6} className="ph-seal" />
          </div>
        </div>
        <p className="ph-sub mt-6 max-w-[560px] text-[18px] leading-[1.9] text-paper-dim">
          五层八十一则。最底层焊死，最上层自由。
        </p>
      </div>

      <div className="relative z-10 hairline-b">
        <div className="mx-auto flex w-full max-w-container justify-end px-6 pb-4 md:px-12">
          <span className="ph-seal-tag">
            <SealTag>卷一 / PROTOCOL</SealTag>
          </span>
        </div>
      </div>
    </header>
  )
}
