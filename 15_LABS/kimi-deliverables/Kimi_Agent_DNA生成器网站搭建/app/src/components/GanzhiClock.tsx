import { useEffect, useState } from 'react'
import { getGanzhi, msToNextShichen, formatCountdown } from '@/lib/ganzhi'
import type { GanzhiPillars } from '@/lib/ganzhi'
import SealTag from '@/components/SealTag'

interface Props {
  variant?: 'compact' | 'full'
  className?: string
}

function useGanzhi(intervalMs: number) {
  const [pillars, setPillars] = useState<GanzhiPillars>(() => getGanzhi())
  useEffect(() => {
    const t = window.setInterval(() => setPillars(getGanzhi()), intervalMs)
    return () => window.clearInterval(t)
  }, [intervalMs])
  return pillars
}

/**
 * GanzhiClock 实时干支时钟（design.md 5.8）
 * compact：Navbar 用，mono 12px，每分钟刷新
 * full：首页时钟带用，五单元 + 卦符 + 倒计时，每秒刷新
 */
export default function GanzhiClock({ variant = 'compact', className = '' }: Props) {
  const pillars = useGanzhi(variant === 'compact' ? 60_000 : 1_000)
  const [countdown, setCountdown] = useState(() => formatCountdown(msToNextShichen()))

  useEffect(() => {
    if (variant !== 'full') return
    const t = window.setInterval(() => setCountdown(formatCountdown(msToNextShichen())), 1_000)
    return () => window.clearInterval(t)
  }, [variant])

  if (variant === 'compact') {
    return (
      <span
        className={`font-mono text-xs tracking-[0.04em] text-paper-dim select-none ${className}`}
        title={`当下卦 ${pillars.hexagramFullName} · 王弼序第 ${pillars.hexagramIndex + 1} 卦`}
      >
        {pillars.year}·{pillars.month}·{pillars.day}·{pillars.hour}
      </span>
    )
  }

  const cells = [
    { tag: 'YEAR PILLAR', label: '年柱', value: pillars.year },
    { tag: 'MONTH PILLAR', label: '月柱', value: pillars.month },
    { tag: 'DAY PILLAR', label: '日柱', value: pillars.day },
    { tag: 'HOUR', label: '时辰', value: pillars.hour },
  ]

  return (
    <div className={className}>
      <div className="grid grid-cols-2 md:grid-cols-5 gap-y-10 gap-x-6">
        {cells.map((c) => (
          <div key={c.tag} className="clock-cell flex flex-col items-center gap-3">
            <SealTag>{c.tag}</SealTag>
            <div className="flex items-baseline gap-2">
              <span className="font-serif font-bold text-[32px] text-gold tracking-[0.05em]">
                {c.value}
              </span>
            </div>
            <span className="text-[13px] text-paper-dim">此刻{c.label}</span>
          </div>
        ))}
        <div className="clock-cell col-span-2 md:col-span-1 flex flex-col items-center gap-3">
          <SealTag>HEXAGRAM</SealTag>
          <div className="group relative flex items-baseline gap-3">
            <span
              className="text-[44px] leading-none text-gold-bright transition-transform duration-300 group-hover:scale-[1.15] cursor-default select-none"
              aria-label={`${pillars.hexagramFullName}，王弼序第 ${pillars.hexagramIndex + 1} 卦`}
            >
              {pillars.hexagramSymbol}
            </span>
            <span className="font-serif font-bold text-[32px] text-gold tracking-[0.05em]">
              {pillars.hexagramFullName}
            </span>
            <span className="pointer-events-none absolute -top-8 left-1/2 -translate-x-1/2 whitespace-nowrap border border-line bg-ink-3 px-3 py-1 font-mono text-[11px] text-paper-dim opacity-0 transition-opacity duration-200 group-hover:opacity-100">
              {pillars.hexagramName} · 第{pillars.hexagramIndex + 1}卦
            </span>
          </div>
          <span className="font-mono text-[13px] text-paper-dim">
            距下一时辰 <span className="text-paper tabular-nums">{countdown}</span>
          </span>
        </div>
      </div>
      <p className="mt-10 text-center font-mono text-[12px] text-paper-faint tracking-[0.04em]">
        天干地支 · 五虎遁 · 儒略日锚定 2000-01-01 戊午
      </p>
    </div>
  )
}
