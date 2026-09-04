// DNA: #龍芯⚡️丙午·甲申·丁未·亥时·䷎谦-DNA-COMPLETION-f3ff5164
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
import { useEffect, useRef, useState } from 'react'
import gsap from 'gsap'
import { getGanzhi } from '@/lib/ganzhi'
import type { GanzhiPillars } from '@/lib/ganzhi'
import SealTag from '@/components/SealTag'

/**
 * S1 · PageHero + 活 DNA 仪表台（70vh）
 * 中央巨型 DNACode 实时展示「此刻若生成」的 DNA；四柱/时辰/卦每秒刷新，
 * 时辰切换瞬间整条 DNA 重排（字段 key 重挂 + dna-field-in）。
 * 载入：四边金线汇聚（0.5s）→ 打字机逐字（30ms/字，金色光标块）→ 标题入场。
 */
function liveDnaString(p: GanzhiPillars): string {
  return `#龍芯⚡️${p.year}·${p.month}·${p.day}·${p.hour}·${p.hexagramSymbol}${p.hexagramName}-NOW-LIVE-实时-████████`
}

export default function LiveDashboard() {
  const rootRef = useRef<HTMLElement>(null)
  const [pillars, setPillars] = useState<GanzhiPillars>(() => getGanzhi())
  const [typedCount, setTypedCount] = useState(0)
  const [typingDone, setTypingDone] = useState(false)
  // 打字机期间的样本串固定，避免秒针刷新打断
  const sampleRef = useRef<string>(liveDnaString(getGanzhi()))

  // 每秒刷新活干支
  useEffect(() => {
    const t = window.setInterval(() => setPillars(getGanzhi()), 1_000)
    return () => window.clearInterval(t)
  }, [])

  // 载入编排：金线汇聚 → 标题 → 打字机
  useEffect(() => {
    const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches
    const total = Array.from(sampleRef.current).length
    if (reduced) {
      setTypedCount(total)
      setTypingDone(true)
      return
    }
    const ctx = gsap.context(() => {
      const tl = gsap.timeline({ defaults: { ease: 'power3.out' } })
      tl.fromTo('.dash-line-h', { scaleX: 0 }, { scaleX: 1, duration: 0.5 }, 0)
        .fromTo('.dash-line-v', { scaleY: 0 }, { scaleY: 1, duration: 0.5 }, 0)
        .fromTo('.dash-eyebrow', { opacity: 0 }, { opacity: 1, duration: 0.4 }, 0.3)
        .fromTo('.dash-title', { y: 40, opacity: 0 }, { y: 0, opacity: 1, duration: 0.6 }, 0.4)
        .fromTo('.dash-sub', { y: 24, opacity: 0 }, { y: 0, opacity: 1, duration: 0.6 }, 0.55)
        .fromTo('.dash-board', { opacity: 0 }, { opacity: 1, duration: 0.4 }, 0.6)
    }, rootRef)

    // 打字机 30ms/字，0.8s 后开始
    let interval = 0
    const kick = window.setTimeout(() => {
      interval = window.setInterval(() => {
        setTypedCount((n) => {
          if (n + 1 >= total) {
            window.clearInterval(interval)
            setTypingDone(true)
            return total
          }
          return n + 1
        })
      }, 30)
    }, 800)

    return () => {
      ctx.revert()
      window.clearTimeout(kick)
      if (interval) window.clearInterval(interval)
    }
  }, [])

  const typedText = Array.from(sampleRef.current).slice(0, typedCount).join('')

  return (
    <section
      ref={rootRef}
      className="relative flex min-h-[70vh] flex-col overflow-hidden"
      aria-label="活 DNA 仪表台"
    >
      {/* 四根 1px 金线从四边向中心仪表台汇聚（静态装饰） */}
      <span
        aria-hidden="true"
        className="dash-line-v pointer-events-none absolute left-1/2 top-0 h-14 w-px origin-top bg-gold-dim"
      />
      <span
        aria-hidden="true"
        className="dash-line-v pointer-events-none absolute bottom-16 left-1/2 h-14 w-px origin-bottom bg-gold-dim"
      />
      <span
        aria-hidden="true"
        className="dash-line-h pointer-events-none absolute left-0 top-1/2 h-px w-16 origin-left bg-gold-dim md:w-32"
      />
      <span
        aria-hidden="true"
        className="dash-line-h pointer-events-none absolute right-0 top-1/2 h-px w-16 origin-right bg-gold-dim md:w-32"
      />

      <div className="mx-auto flex w-full max-w-container flex-1 flex-col items-center justify-center px-6 py-20 text-center md:px-12">
        <span className="dash-eyebrow eyebrow opacity-0">SCROLL II · THE DNA</span>
        <h1 className="dash-title mt-6 font-serif font-black text-[clamp(40px,6vw,80px)] leading-[1.1] tracking-[0.05em] text-paper opacity-0">
          DNA 追溯碼
        </h1>
        <p className="dash-sub mt-6 max-w-[560px] text-[18px] leading-[1.9] tracking-[0.02em] text-paper-dim opacity-0">
          每一个汉字、每一行代码、每一份协议——都有唯一的干支生辰。
        </p>

        {/* 仪表台：巨型 DNACode（mono 20–24px 可换行） */}
        <div className="dash-board relative mt-12 w-full max-w-[960px] border border-line border-l-[3px] border-l-gold bg-ink-3 px-6 py-8 opacity-0 md:px-10">
          <div className="mb-4 flex items-center justify-between">
            <span className="font-cinzel text-[11px] uppercase tracking-[0.38em] text-gold-dim">
              LIVE CONSOLE
            </span>
            <span className="font-mono text-[11px] tracking-[0.1em] text-paper-faint">
              每秒刷新 · 时辰切换即重排
            </span>
          </div>
          <code className="block break-all text-left font-mono text-[clamp(15px,2.2vw,22px)] leading-[2] tracking-[0.04em] text-paper">
            {!typingDone ? (
              <>
                <span className="text-gold-bright">{typedText}</span>
                <span className="dna-cursor" aria-hidden="true" />
              </>
            ) : (
              <>
                <span>#龍芯⚡️</span>
                <span key={pillars.year} className="dna-field-in text-gold-bright">
                  {pillars.year}
                </span>
                <span>·</span>
                <span key={pillars.month} className="dna-field-in text-gold-bright">
                  {pillars.month}
                </span>
                <span>·</span>
                <span key={pillars.day} className="dna-field-in text-gold-bright">
                  {pillars.day}
                </span>
                <span>·</span>
                <span key={pillars.hour} className="dna-field-in text-gold-bright">
                  {pillars.hour}
                </span>
                <span>·</span>
                <span className="group relative cursor-default">
                  <span
                    key={pillars.hexagramSymbol}
                    className="dna-field-in text-gold-bright"
                    aria-label={`${pillars.hexagramFullName}，王弼序第 ${pillars.hexagramIndex + 1} 卦`}
                  >
                    {pillars.hexagramSymbol}
                    {pillars.hexagramName}
                  </span>
                  <span className="pointer-events-none absolute -top-9 left-1/2 z-10 -translate-x-1/2 whitespace-nowrap border border-line bg-ink px-3 py-1 font-mono text-[11px] text-paper-dim opacity-0 transition-opacity duration-200 group-hover:opacity-100">
                    王弼序第 {pillars.hexagramIndex + 1} 卦 · {pillars.hexagramFullName}
                  </span>
                </span>
                <span>-</span>
                <span className="text-vermilion">NOW</span>
                <span>-</span>
                <span>LIVE</span>
                <span>-</span>
                <span>实时</span>
                <span>-</span>
                <span className="text-paper-dim">████████</span>
              </>
            )}
          </code>
        </div>
      </div>

      {/* 底部发丝线 + 页码 */}
      <div className="hairline-b relative">
        <div className="mx-auto flex w-full max-w-container justify-end px-6 pb-4 md:px-12">
          <SealTag>卷二 / DNA</SealTag>
        </div>
      </div>
    </section>
  )
}
