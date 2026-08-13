import { useRef, useState } from 'react'
import { motion, useInView } from 'framer-motion'
import { DIMS, DIM_COLORS } from '@/pages/matrix/personas'

const INITIAL: [number, number, number, number, number] = [42, 18, 15, 15, 10]

/**
 * 拖一根滑杆，其余按当前占比自动平衡，总和恒 100
 */
function rebalance(prev: number[], idx: number, next: number): number[] {
  const clamped = Math.max(0, Math.min(100, Math.round(next)))
  const othersSum = prev.reduce((s, v, i) => (i === idx ? s : s + v), 0)
  const remain = 100 - clamped
  const out = prev.map((v, i) => (i === idx ? clamped : v))
  if (othersSum === 0) {
    const share = Math.floor(remain / 4)
    for (let i = 0; i < out.length; i++) if (i !== idx) out[i] = share
    // 余数补给第一根其他杆
    const used = out.reduce((s, v) => s + v, 0)
    for (let i = 0; i < out.length && used < 100; i++) {
      if (i !== idx) {
        out[i] += 100 - used
        break
      }
    }
    return out
  }
  let distributed = 0
  const scaled = out.map((v, i) => {
    if (i === idx) return v
    const nv = Math.round((prev[i] / othersSum) * remain)
    distributed += nv
    return nv
  })
  // 四舍五入残差修正：补给当前最大的其他杆
  let diff = 100 - clamped - distributed
  const order = prev
    .map((v, i) => ({ v, i }))
    .filter((o) => o.i !== idx)
    .sort((a, b) => b.v - a.v)
  let k = 0
  while (diff !== 0 && order.length > 0) {
    const t = order[k % order.length].i
    if (scaled[t] + Math.sign(diff) >= 0) {
      scaled[t] += Math.sign(diff)
      diff -= Math.sign(diff)
    }
    k++
    if (k > 400) break
  }
  return scaled
}

/**
 * S5 · 五维调配演示（matrix.md S5）—— 交互滑杆
 * 总和恒 100 · 拖一根其余按比例平衡 · 实时堆叠条 + mono 读数
 * 纯 Framer Motion 域
 */
export default function DimensionMixer() {
  const ref = useRef<HTMLElement>(null)
  const inView = useInView(ref, { once: true, amount: 0.3 })
  const [values, setValues] = useState<number[]>(INITIAL)

  const onSlide = (idx: number, next: number) => {
    setValues((prev) => rebalance(prev, idx, next))
  }

  return (
    <section ref={ref} className="hairline-b bg-ink-2 py-[120px] max-md:py-[72px]" aria-label="五维调配演示">
      <div className="mx-auto grid w-full max-w-container grid-cols-1 items-center gap-16 px-6 md:px-12 lg:grid-cols-2">
        {/* 左文 */}
        <div>
          <span className="eyebrow">THE MIXER</span>
          <h2 className="mt-6 font-serif text-[clamp(30px,4vw,52px)] font-bold leading-[1.15] tracking-[0.05em] text-paper">
            五维如何调配
          </h2>
          <p className="mt-6 max-w-[560px] text-[18px] leading-[1.9] tracking-[0.02em] text-paper-dim">
            同一个人格，在不同议题下调用不同维度配比。拖动滑杆，看内阁席位的力量消长。
          </p>
          {/* 实时堆叠条形图 */}
          <div className="mt-12">
            <div className="flex h-[28px] w-full border border-line" role="img"
              aria-label={`五维占比：${DIMS.map((d, i) => `${d.name} ${values[i]}%`).join('，')}`}
            >
              {values.map((v, i) => (
                <motion.div
                  key={DIMS[i].key}
                  className="h-full"
                  animate={{ width: `${v}%` }}
                  transition={{ type: 'spring', stiffness: 260, damping: 28 }}
                  style={{ background: DIM_COLORS[i] }}
                />
              ))}
            </div>
            <p className="mt-4 font-mono text-[14px] tracking-[0.06em] text-gold-bright tabular-nums">
              {DIMS.map((d, i) => `${d.key} ${values[i]}`).join(' · ')}
            </p>
          </div>
        </div>

        {/* 右器：五根滑杆 */}
        <div className="flex flex-col gap-8">
          {DIMS.map((d, i) => (
            <motion.div
              key={d.key}
              initial={{ scaleX: 0, opacity: 0 }}
              animate={inView ? { scaleX: 1, opacity: 1 } : { scaleX: 0, opacity: 0 }}
              transition={{ duration: 0.6, delay: i * 0.08, ease: [0.22, 1, 0.36, 1] }}
              style={{ transformOrigin: 'left' }}
            >
              <div className="mb-3 flex items-baseline justify-between">
                <label htmlFor={`mixer-${d.key}`} className="font-serif text-[16px] font-bold tracking-[0.1em] text-paper">
                  {d.name}
                  <span className="ml-3 font-mono text-[11px] tracking-[0.24em] text-gold-dim">{d.key}</span>
                </label>
                <span className="font-mono text-[14px] text-gold tabular-nums">{values[i]}</span>
              </div>
              <input
                id={`mixer-${d.key}`}
                type="range"
                min={0}
                max={100}
                step={1}
                value={values[i]}
                onChange={(e) => onSlide(i, Number(e.target.value))}
                aria-label={`${d.name}维度占比`}
                className="h-[2px] w-full cursor-pointer appearance-none bg-line outline-none
                  [&::-webkit-slider-thumb]:h-4 [&::-webkit-slider-thumb]:w-4
                  [&::-webkit-slider-thumb]:appearance-none [&::-webkit-slider-thumb]:rounded-none
                  [&::-webkit-slider-thumb]:bg-gold [&::-webkit-slider-thumb]:border [&::-webkit-slider-thumb]:border-gold-bright
                  [&::-webkit-slider-thumb]:transition-colors [&::-webkit-slider-thumb]:duration-200
                  [&::-webkit-slider-thumb]:hover:bg-gold-bright
                  [&::-moz-range-thumb]:h-4 [&::-moz-range-thumb]:w-4 [&::-moz-range-thumb]:rounded-none
                  [&::-moz-range-thumb]:bg-gold [&::-moz-range-thumb]:border [&::-moz-range-thumb]:border-gold-bright
                  [&::-moz-range-track]:h-[2px] [&::-moz-range-track]:bg-line"
              />
            </motion.div>
          ))}
          <p className="text-[13px] leading-[1.9] text-paper-faint">
            总和恒为 100。任一维度增减，其余席位按现有权重自动让渡或递补——此谓「内阁制衡」。
          </p>
        </div>
      </div>
    </section>
  )
}
