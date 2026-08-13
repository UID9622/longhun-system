import { useEffect, useRef, useState } from 'react'
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'
import SealTag from '@/components/SealTag'
import DNACode from '@/components/DNACode'
import { getGanzhi, hexagramSymbol } from '@/lib/ganzhi'
import { MilestoneDecor } from '@/pages/timeline/milestones'
import type { Milestone } from '@/pages/timeline/milestones'

gsap.registerPlugin(ScrollTrigger)

/** 章尾 DNACode 打字机（15ms/字，入视口触发） */
function DnaTypewriter({ code }: { code: string }) {
  const ref = useRef<HTMLDivElement>(null)
  const [n, setN] = useState(() =>
    typeof window !== 'undefined' &&
    window.matchMedia('(prefers-reduced-motion: reduce)').matches
      ? code.length
      : 0,
  )

  useEffect(() => {
    if (n >= code.length) return
    let timer = 0
    const st = ScrollTrigger.create({
      trigger: ref.current,
      start: 'top 82%',
      onEnter: () => {
        timer = window.setInterval(() => {
          setN((v) => {
            if (v >= code.length) {
              window.clearInterval(timer)
              return v
            }
            return v + 1
          })
        }, 15)
      },
      once: true,
    })
    return () => {
      st.kill()
      window.clearInterval(timer)
    }
  }, [code.length, n])

  return (
    <div ref={ref}>
      <DNACode code={code.slice(0, n)} fontSize={13} showCopy={n >= code.length} />
      {n < code.length ? <div className="h-5" aria-hidden="true" /> : null}
    </div>
  )
}

/** 章五实时彩蛋：「你读到此处时：{实时日柱}·{实时时辰}」 */
function LiveMoment() {
  const [now, setNow] = useState(() => getGanzhi())
  useEffect(() => {
    const t = window.setInterval(() => setNow(getGanzhi()), 60_000)
    return () => window.clearInterval(t)
  }, [])
  return (
    <p className="mt-6 font-mono text-[13px] tracking-[0.08em] text-gold">
      你读到此处时：<span className="text-gold-bright">{now.day}</span>·
      <span className="text-gold-bright">{now.hour}</span>
      <span className="ml-3 text-paper-faint">（实时干支）</span>
    </p>
  )
}

interface Props {
  m: Milestone
}

/**
 * S3 · 里程碑章（timeline.md）
 * 左右交替版式 · 轨道金点激活 · 日期/章题/章文入场 · 卦符缓转 · DNA 打字机
 */
export default function MilestoneChapter({ m }: Props) {
  const ref = useRef<HTMLElement>(null)
  const [lit, setLit] = useState(() =>
    typeof window !== 'undefined' &&
    window.matchMedia('(prefers-reduced-motion: reduce)').matches,
  )

  useEffect(() => {
    const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches
    const ctx = gsap.context(() => {
      // 轨道金点：到达激活 / 回退熄灭
      ScrollTrigger.create({
        trigger: ref.current,
        start: 'top 55%',
        onEnter: () => setLit(true),
        onLeaveBack: () => setLit(false),
      })
      if (reduced) return
      const fromX = m.side === 'left' ? -60 : 60
      gsap.fromTo(
        '.ms-date',
        { x: fromX, opacity: 0 },
        {
          x: 0,
          opacity: 1,
          duration: 0.7,
          ease: 'power3.out',
          scrollTrigger: { trigger: ref.current, start: 'top 68%' },
        },
      )
      gsap.fromTo(
        '.ms-title-word',
        { y: 24, opacity: 0 },
        {
          y: 0,
          opacity: 1,
          duration: 0.5,
          stagger: 0.08,
          ease: 'power3.out',
          scrollTrigger: { trigger: ref.current, start: 'top 66%' },
        },
      )
      gsap.fromTo(
        '.ms-body',
        { y: 30, opacity: 0 },
        {
          y: 0,
          opacity: 1,
          duration: 0.6,
          ease: 'power3.out',
          scrollTrigger: { trigger: ref.current, start: 'top 62%' },
        },
      )
      // 卦符章饰：rotate -20°→0, opacity 0→1（0.8s）
      gsap.fromTo(
        '.ms-decor',
        { rotate: -20, opacity: 0 },
        {
          rotate: 0,
          opacity: 1,
          duration: 0.8,
          ease: 'power3.out',
          scrollTrigger: { trigger: ref.current, start: 'top 62%' },
        },
      )
    }, ref)
    return () => ctx.revert()
  }, [m.side])

  const contentCol = (
    <div className="ms-content md:col-span-7">
      <div className="flex flex-wrap items-center gap-5">
        <p className="ms-date font-mono font-semibold tracking-[0.04em] text-gold tabular-nums"
          style={{ fontSize: 'clamp(36px, 5vw, 64px)', lineHeight: 1.1 }}
        >
          {m.date}
        </p>
        <SealTag>{m.stage}</SealTag>
      </div>
      <h3 className="mt-6 font-serif text-[32px] font-bold leading-[1.3] tracking-[0.04em] text-paper">
        {m.title.split(/\s+/).map((w, i) => (
          <span key={i} className="ms-title-word inline-block">
            {w}
            {i < m.title.split(/\s+/).length - 1 ? ' ' : ''}
          </span>
        ))}
      </h3>
      <div className="ms-body mt-6 max-w-[560px]">
        {m.body.map((line, i) => (
          <p key={i} className="text-[18px] leading-[1.9] tracking-[0.02em] text-paper-dim">
            {line}
          </p>
        ))}
      </div>
      <div className="ms-body mt-8">
        <DnaTypewriter code={m.dna} />
        {m.id === 'm5' ? <LiveMoment /> : null}
      </div>
    </div>
  )

  const decorCol = (
    <div className="ms-decor flex flex-col items-center gap-10 md:col-span-5" aria-hidden="true">
      {/* 专属卦符：64px gold-dim，常驻 60s/圈缓转 */}
      <span className="block">
        <span
          className="block animate-spin-slow text-[64px] leading-none text-gold-dim select-none"
          style={{ animationDuration: '60s' }}
          title={`${m.hexName}卦`}
        >
          {hexagramSymbol(m.hexIndex)}
        </span>
      </span>
      <span className="font-mono text-[12px] tracking-[0.3em] text-gold-dim">{m.hexName}</span>
      <MilestoneDecor kind={m.decor} />
    </div>
  )

  return (
    <article
      ref={ref}
      className="ms-chapter relative flex min-h-[80vh] items-center py-24"
      aria-label={`里程碑：${m.date} ${m.title}`}
    >
      {/* 轨道金点：10px · 未激活 40% 空圈 · 激活常亮 + 脉冲一次 */}
      <span
        className="absolute left-5 top-28 z-10 -translate-x-1/2 md:left-20"
        aria-hidden="true"
      >
        <span
          className={`block h-[10px] w-[10px] rounded-full border transition-all duration-500 ${
            lit ? 'border-gold bg-gold' : 'border-gold/40 bg-transparent'
          }`}
        />
        {lit ? (
          <span
            className="absolute -inset-[5px] rounded-full border border-gold"
            style={{ animation: 'pulse-ring 1.2s ease-out 1 forwards' }}
          />
        ) : null}
      </span>

      <div className="mx-auto grid w-full max-w-container items-center gap-14 px-6 pl-14 md:grid-cols-12 md:px-12 md:pl-32">
        {m.side === 'left' ? (
          <>
            {contentCol}
            {decorCol}
          </>
        ) : (
          <>
            {decorCol}
            {contentCol}
          </>
        )}
      </div>
    </article>
  )
}
