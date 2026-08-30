// DNA: #龍芯⚡️丙午·甲申·丁未·亥时·䷎谦-DNA-COMPLETION-8ac3f87f
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
import { useEffect, useRef } from 'react'
import { STEMS, BRANCHES } from '@/lib/ganzhi'

const CHARS = (STEMS + BRANCHES).split('')

interface Props {
  count?: number // 字符数（≤10）
  direction?: 'fall' | 'rise'
  className?: string
}

interface Particle {
  x: number // 0..1
  y: number // 0..1
  speed: number // px/s
  size: number
  alpha: number
  ch: string
}

/**
 * 稀疏干支字符飘落/上浮 canvas（timeline.md S1 / 章间过渡带）
 * Canvas 2D · 离屏暂停 · prefers-reduced-motion 静态呈现
 */
export default function GanzhiCharCanvas({ count = 6, direction = 'rise', className = '' }: Props) {
  const canvasRef = useRef<HTMLCanvasElement>(null)

  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return
    const ctx = canvas.getContext('2d')
    if (!ctx) return

    const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches
    let raf = 0
    let running = false
    let last = 0
    let w = 0
    let h = 0

    const particles: Particle[] = Array.from({ length: count }, () => ({
      x: Math.random(),
      y: Math.random(),
      speed: 8 + Math.random() * 14,
      size: 13 + Math.random() * 8,
      alpha: 0.08 + Math.random() * 0.12,
      ch: CHARS[Math.floor(Math.random() * CHARS.length)],
    }))

    const resize = () => {
      const rect = canvas.getBoundingClientRect()
      const dpr = Math.min(window.devicePixelRatio || 1, 2)
      w = rect.width
      h = rect.height
      canvas.width = Math.max(1, Math.floor(w * dpr))
      canvas.height = Math.max(1, Math.floor(h * dpr))
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0)
    }

    const draw = () => {
      ctx.clearRect(0, 0, w, h)
      for (const p of particles) {
        ctx.font = `${p.size}px "JetBrains Mono", monospace`
        ctx.fillStyle = `rgba(201, 162, 39, ${p.alpha})`
        ctx.fillText(p.ch, p.x * w, p.y * h)
      }
    }

    const tick = (t: number) => {
      if (!running) return
      const dt = last ? Math.min((t - last) / 1000, 0.1) : 0
      last = t
      const dir = direction === 'fall' ? 1 : -1
      for (const p of particles) {
        p.y += (dir * p.speed * dt) / Math.max(h, 1)
        if (p.y < -0.05) {
          p.y = 1.05
          p.x = Math.random()
          p.ch = CHARS[Math.floor(Math.random() * CHARS.length)]
        } else if (p.y > 1.05) {
          p.y = -0.05
          p.x = Math.random()
          p.ch = CHARS[Math.floor(Math.random() * CHARS.length)]
        }
      }
      draw()
      raf = requestAnimationFrame(tick)
    }

    resize()
    draw()
    if (reduced) return // 静态呈现终态

    const io = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting && !running) {
          running = true
          last = 0
          raf = requestAnimationFrame(tick)
        } else if (!entry.isIntersecting && running) {
          running = false
          cancelAnimationFrame(raf)
        }
      },
      { threshold: 0.05 },
    )
    io.observe(canvas)

    const onResize = () => {
      resize()
      draw()
    }
    window.addEventListener('resize', onResize)
    return () => {
      io.disconnect()
      window.removeEventListener('resize', onResize)
      cancelAnimationFrame(raf)
    }
  }, [count, direction])

  return (
    <canvas
      ref={canvasRef}
      className={className}
      style={{ position: 'absolute', inset: 0, width: '100%', height: '100%', pointerEvents: 'none' }}
      aria-hidden="true"
    />
  )
}
