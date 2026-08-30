// DNA: #龍芯⚡️丙午·甲申·丁未·亥时·䷎谦-DNA-COMPLETION-8a5a156e
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
import { memo, useEffect, useRef } from 'react'
import { JIAZI_60 } from '@/lib/ganzhi'

interface Props {
  paused: boolean
  className?: string
}

interface RainChar {
  x: number
  y: number
  speed: number
  size: number
  alpha: number
  ch: string
  drift: number
}

interface Particle {
  bx: number
  by: number
  x: number
  y: number
  dx: number
  dy: number
  r: number
  phase: number
}

interface HexStack {
  x: number
  halfW: number
  yaos: boolean[] // true=阳
  shown: number
  alpha: number
  phase: 'stacking' | 'hold' | 'fade'
  timer: number
  baseY: number
}

/**
 * 「爻雨」生成式背景（home.md S1）
 * ① 底部金色六爻卦线堆叠（每 4s 一卦，堆满 6 爻后淡出循环）
 * ② 60 干支字符金雨（8–20% 透明度，字符级视差）
 * ③ 40 稀疏金粒随鼠标轻微避让
 * rAF · DPR 感知 · 离屏/暂停即停帧
 */
function YaoRainCanvas({ paused, className = '' }: Props) {
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const pausedRef = useRef(paused)
  pausedRef.current = paused

  useEffect(() => {
    // canvas 必已挂载（ref 在 effect 前完成绑定），ctx 为 2D 标准上下文
    const canvas = canvasRef.current!
    const ctx = canvas.getContext('2d')!

    let W = 0
    let H = 0
    let raf = 0
    let running = true
    let visible = true
    const dpr = Math.min(window.devicePixelRatio || 1, 2)

    const mouse = { x: -9999, y: -9999 }

    // ---------- 对象池 ----------
    const chars: RainChar[] = []
    const particles: Particle[] = []
    const stacks: HexStack[] = []

    const rand = (a: number, b: number) => a + Math.random() * (b - a)

    function seedChars() {
      chars.length = 0
      for (let i = 0; i < 60; i++) {
        const size = rand(14, 34)
        chars.push({
          x: rand(0, W),
          y: rand(-H, H),
          speed: (size / 34) * rand(0.35, 0.8) + 0.15, // 视差：大近快、小远慢
          size,
          alpha: rand(0.08, 0.2),
          ch: JIAZI_60[Math.floor(rand(0, 60))][Math.random() < 0.5 ? 0 : 1],
          drift: rand(-0.08, 0.08),
        })
      }
    }

    function seedParticles() {
      particles.length = 0
      for (let i = 0; i < 40; i++) {
        const bx = rand(0, W)
        const by = rand(0, H)
        particles.push({
          bx,
          by,
          x: bx,
          y: by,
          dx: 0,
          dy: 0,
          r: rand(0.6, 1.8),
          phase: rand(0, Math.PI * 2),
        })
      }
    }

    function newStack(x: number, baseY: number): HexStack {
      return {
        x,
        halfW: rand(60, 130),
        yaos: Array.from({ length: 6 }, () => Math.random() < 0.55),
        shown: 0,
        alpha: 0,
        phase: 'stacking',
        timer: 0,
        baseY,
      }
    }

    function seedStacks() {
      stacks.length = 0
      const n = Math.max(4, Math.floor(W / 260))
      for (let i = 0; i < n; i++) {
        const st = newStack((W / n) * (i + 0.5) + rand(-30, 30), H - rand(40, 110))
        // 相位错开：有的已在 hold/fade
        st.shown = Math.floor(rand(0, 6))
        st.alpha = rand(0.3, 0.9)
        st.phase = Math.random() < 0.5 ? 'stacking' : 'hold'
        stacks.push(st)
      }
    }

    function resize() {
      const rect = canvas.getBoundingClientRect()
      W = rect.width
      H = rect.height
      canvas.width = Math.round(W * dpr)
      canvas.height = Math.round(H * dpr)
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0)
      seedChars()
      seedParticles()
      seedStacks()
    }

    // ---------- 帧 ----------
    const YAO_GAP = 24
    let last = performance.now()

    function frame(now: number) {
      raf = requestAnimationFrame(frame)
      const dt = Math.min(0.05, (now - last) / 1000)
      last = now
      if (!running || !visible || pausedRef.current) return

      ctx.clearRect(0, 0, W, H)

      // ① 爻线堆叠
      for (let i = 0; i < stacks.length; i++) {
        const st = stacks[i]
        st.timer += dt
        if (st.phase === 'stacking') {
          st.alpha = Math.min(0.9, st.alpha + dt * 1.2)
          if (st.timer >= 0.62) {
            st.timer = 0
            st.shown += 1
            if (st.shown >= 6) st.phase = 'hold'
          }
        } else if (st.phase === 'hold') {
          if (st.timer >= 1.6) {
            st.timer = 0
            st.phase = 'fade'
          }
        } else {
          st.alpha -= dt * 0.5
          if (st.alpha <= 0) {
            stacks[i] = newStack(st.x, H - rand(40, 110))
          }
        }
        ctx.strokeStyle = `rgba(201,162,39,${(st.alpha * 0.75).toFixed(3)})`
        ctx.lineWidth = 3
        ctx.lineCap = 'butt'
        const glowA = st.alpha * 0.25
        for (let j = 0; j < st.shown; j++) {
          const y = st.baseY - j * YAO_GAP
          const yang = st.yaos[j]
          ctx.shadowColor = `rgba(201,162,39,${glowA.toFixed(3)})`
          ctx.shadowBlur = 10
          ctx.beginPath()
          if (yang) {
            ctx.moveTo(st.x - st.halfW, y)
            ctx.lineTo(st.x + st.halfW, y)
          } else {
            const g = st.halfW * 0.24
            ctx.moveTo(st.x - st.halfW, y)
            ctx.lineTo(st.x - g, y)
            ctx.moveTo(st.x + g, y)
            ctx.lineTo(st.x + st.halfW, y)
          }
          ctx.stroke()
        }
        ctx.shadowBlur = 0
      }

      // ② 干支字符雨
      for (const c of chars) {
        c.y += c.speed * (dt * 60)
        c.x += c.drift
        if (c.y > H + 40) {
          c.y = rand(-120, -20)
          c.x = rand(0, W)
          c.ch = JIAZI_60[Math.floor(rand(0, 60))][Math.random() < 0.5 ? 0 : 1]
        }
        ctx.font = `${c.size}px "Noto Serif SC", serif`
        ctx.fillStyle = `rgba(201,162,39,${c.alpha.toFixed(3)})`
        ctx.fillText(c.ch, c.x, c.y)
      }

      // ③ 稀疏金粒（鼠标避让 + lerp 衰减）
      for (const p of particles) {
        const mdx = p.x - mouse.x
        const mdy = p.y - mouse.y
        const dist2 = mdx * mdx + mdy * mdy
        if (dist2 < 120 * 120 && dist2 > 0.01) {
          const dist = Math.sqrt(dist2)
          const f = ((120 - dist) / 120) * 1.6
          p.dx += (mdx / dist) * f
          p.dy += (mdy / dist) * f
        }
        p.dx *= 0.92
        p.dy *= 0.92
        p.phase += dt
        p.x = p.bx + Math.sin(p.phase * 0.7) * 6 + p.dx * 8
        p.y = p.by + Math.cos(p.phase * 0.5) * 6 + p.dy * 8
        ctx.beginPath()
        ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2)
        ctx.fillStyle = `rgba(233,203,107,${(0.28 + 0.2 * Math.sin(p.phase)).toFixed(3)})`
        ctx.fill()
      }
    }

    // ---------- 事件 ----------
    const onMove = (e: PointerEvent) => {
      const rect = canvas.getBoundingClientRect()
      mouse.x = e.clientX - rect.left
      mouse.y = e.clientY - rect.top
    }
    const onLeave = () => {
      mouse.x = -9999
      mouse.y = -9999
    }
    const io = new IntersectionObserver(([entry]) => {
      visible = entry.isIntersecting
    })
    io.observe(canvas)
    const onVis = () => {
      running = document.visibilityState === 'visible'
    }

    resize()
    window.addEventListener('resize', resize)
    canvas.addEventListener('pointermove', onMove)
    canvas.addEventListener('pointerleave', onLeave)
    document.addEventListener('visibilitychange', onVis)
    raf = requestAnimationFrame(frame)

    return () => {
      cancelAnimationFrame(raf)
      window.removeEventListener('resize', resize)
      canvas.removeEventListener('pointermove', onMove)
      canvas.removeEventListener('pointerleave', onLeave)
      document.removeEventListener('visibilitychange', onVis)
      io.disconnect()
    }
  }, [])

  return (
    <canvas
      ref={canvasRef}
      className={className}
      style={{
        position: 'absolute',
        inset: 0,
        width: '100%',
        height: '100%',
        zIndex: 0,
        cursor: 'crosshair',
      }}
      aria-hidden="true"
    />
  )
}

export default memo(YaoRainCanvas)
