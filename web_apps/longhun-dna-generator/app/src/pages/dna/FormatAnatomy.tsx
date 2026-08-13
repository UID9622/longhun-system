import { useEffect, useRef, useState } from 'react'
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'
import SectionHeading from '@/components/SectionHeading'

gsap.registerPlugin(ScrollTrigger)

/**
 * S2 · 格式解剖（v2.0 规范图解）
 * 放大的 DNA 标本 + 1px 金线引注线连接 4+3 两排注解卡；
 * hover 注解卡 → 对应 DNA 字段金底墨字反色 + 引注线转亮金。
 */

interface Segment {
  text: string
  sep: string // 前置分隔符
  name: string
  note: string
  color: string
}

const SEGMENTS: Segment[] = [
  { text: '#龍芯⚡️', sep: '', name: '#龍芯⚡️', note: '族徽前缀 · 龍魂血统标识', color: 'text-paper' },
  {
    text: '丙午·甲申·己卯·午时',
    sep: '',
    name: '丙午·甲申·己卯·午时',
    note: '干支四柱 · 年月日时（天干 10 × 地支 12 = 60 甲子）',
    color: 'text-gold-bright',
  },
  {
    text: '䷀乾',
    sep: '·',
    name: '䷀乾',
    note: '卦符卦名 · 王弼序 64 卦（U+4DC0+i）',
    color: 'text-gold-bright',
  },
  {
    text: 'AUDIT-REPORT',
    sep: '-',
    name: 'AUDIT-REPORT',
    note: '动作标签 · 朱砂色显示',
    color: 'text-vermilion',
  },
  { text: 'v1.0', sep: '-', name: 'v1.0', note: '版本号', color: 'text-paper' },
  {
    text: '0007',
    sep: '-',
    name: '0007',
    note: '日序号 · 当日单调递增，机器级不重复',
    color: 'text-paper',
  },
  {
    text: 'a3f9c21e',
    sep: '-',
    name: 'a3f9c21e',
    note: '内容哈希 8 位 · SM3/SHA256',
    color: 'text-paper-dim',
  },
]

const SPECIMEN = SEGMENTS.map((s) => s.sep + s.text).join('')

export default function FormatAnatomy() {
  const rootRef = useRef<HTMLElement>(null)
  const [hover, setHover] = useState<number | null>(null)
  const [typed, setTyped] = useState(0)
  const [typing, setTyping] = useState(false)
  const specimenDone = typed >= Array.from(SPECIMEN).length

  // 标本打字机 20ms/字（入视口触发）+ 引注线/注解卡入场
  useEffect(() => {
    const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches
    const total = Array.from(SPECIMEN).length
    if (reduced) {
      setTyped(total)
      return
    }
    let interval = 0
    const ctx = gsap.context(() => {
      ScrollTrigger.create({
        trigger: rootRef.current,
        start: 'top 70%',
        once: true,
        onEnter: () => {
          setTyping(true)
          interval = window.setInterval(() => {
            setTyped((n) => {
              if (n + 1 >= total) {
                window.clearInterval(interval)
                return total
              }
              return n + 1
            })
          }, 20)
          gsap.fromTo(
            '.anat-leader',
            { scaleY: 0 },
            { scaleY: 1, duration: 0.3, stagger: 0.08, ease: 'power2.out', delay: total * 0.02 + 0.1 },
          )
          gsap.fromTo(
            '.anat-card',
            { y: 20, opacity: 0 },
            {
              y: 0,
              opacity: 1,
              duration: 0.5,
              stagger: 0.08,
              ease: 'power3.out',
              delay: total * 0.02 + 0.2,
            },
          )
        },
      })
    }, rootRef)
    return () => {
      ctx.revert()
      if (interval) window.clearInterval(interval)
    }
  }, [])

  const typedText = Array.from(SPECIMEN).slice(0, typed).join('')

  const renderCard = (seg: Segment, i: number) => (
    <div key={i} className="flex flex-col items-center">
      {/* 引注线 */}
      <span
        aria-hidden="true"
        className={`anat-leader block h-10 w-px origin-top transition-colors duration-250 ${
          hover === i ? 'bg-gold-bright' : 'bg-line'
        }`}
      />
      <button
        type="button"
        onMouseEnter={() => setHover(i)}
        onMouseLeave={() => setHover(null)}
        onFocus={() => setHover(i)}
        onBlur={() => setHover(null)}
        className={`anat-card w-full cursor-default border bg-ink-3 px-4 py-4 text-left opacity-0 transition-colors duration-300 ${
          hover === i ? 'border-gold' : 'border-line'
        }`}
      >
        <span className="block break-all font-mono text-[13px] tracking-[0.04em] text-gold">
          {seg.name}
        </span>
        <span className="mt-2 block text-[13px] leading-[1.8] text-paper-dim">{seg.note}</span>
      </button>
    </div>
  )

  return (
    <section ref={rootRef} className="hairline-t relative" aria-label="格式解剖">
      <div className="mx-auto w-full max-w-container px-6 py-[72px] md:px-12 md:py-[120px]">
        <SectionHeading eyebrow="ANATOMY" title="格式 v2.0 · 解剖" />

        <div className="relative mt-16">
          {/* 右侧竖排 caption：分隔符之礼 */}
          <p className="writing-vertical absolute right-0 top-0 hidden select-none text-[13px] leading-[2.2] tracking-[0.2em] text-paper-faint lg:block">
            分隔符之礼：四柱与卦用「·」，其后诸段用「-」。旧格式一律冻结不改写（P0）。
          </p>

          {/* DNA 标本 */}
          <div className="mx-auto max-w-[860px] border border-line border-l-[3px] border-l-gold bg-ink-3 px-6 py-6 md:px-8">
            <code className="block break-all font-mono text-[15px] leading-[2] tracking-[0.04em] md:text-[18px]">
              {!specimenDone ? (
                <>
                  <span className="text-gold-bright">{typedText}</span>
                  {typing ? <span className="dna-cursor" aria-hidden="true" /> : null}
                </>
              ) : (
                SEGMENTS.map((seg, i) => (
                  <span key={i}>
                    <span className="text-paper-faint">{seg.sep}</span>
                    <span
                      className={`${seg.color} transition-colors duration-250 ${
                        hover === i ? 'bg-gold text-ink' : ''
                      }`}
                    >
                      {seg.text}
                    </span>
                  </span>
                ))
              )}
            </code>
          </div>

          {/* 注解卡 4+3 两排环绕 */}
          <div className="mx-auto mt-2 grid max-w-[1080px] grid-cols-1 gap-x-6 gap-y-2 sm:grid-cols-2 lg:grid-cols-4">
            {SEGMENTS.slice(0, 4).map((seg, i) => renderCard(seg, i))}
          </div>
          <div className="mx-auto mt-2 grid max-w-[820px] grid-cols-1 gap-x-6 gap-y-2 sm:grid-cols-2 lg:grid-cols-3">
            {SEGMENTS.slice(4).map((seg, i) => renderCard(seg, i + 4))}
          </div>

          {/* 移动端的分隔符之礼 */}
          <p className="mt-10 text-[13px] leading-[2] text-paper-faint lg:hidden">
            分隔符之礼：四柱与卦用「·」，其后诸段用「-」。旧格式一律冻结不改写（P0）。
          </p>
        </div>
      </div>
    </section>
  )
}
