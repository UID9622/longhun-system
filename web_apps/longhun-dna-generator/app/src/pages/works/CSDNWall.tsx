// DNA: #龍芯⚡️丙午·甲申·丁未·亥时·䷎谦-DNA-COMPLETION-ebdaf3ec
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
import { useEffect, useRef } from 'react'
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'
import { ExternalLink } from 'lucide-react'
import SectionHeading from '@/components/SectionHeading'
import OutlineButton from '@/components/OutlineButton'
import { csdnSearchUrl } from '@/pages/works/worksData'

gsap.registerPlugin(ScrollTrigger)

/** CSDN 真实数据（2026-08-03 快照 · 真实可查禁止虚构） */
const STATS = [
  { value: 1512, label: '点赞' },
  { value: 844, label: '收藏' },
  { value: 12631, label: '博客总排名' },
]

const RANK = 12631
/** 对数刻度域：1 → 100K（log10 0..5） */
const pct = (v: number) => (Math.log10(v) / 5) * 100
const TICKS = [
  { v: 1, label: '1' },
  { v: 10, label: '10' },
  { v: 100, label: '100' },
  { v: 1000, label: '1K' },
  { v: 10000, label: '10K' },
]

const fmt = (n: number) => n.toLocaleString('en-US')

/**
 * S4 · CSDN 数据墙（works.md）
 * 三巨数递增计数 + 对数刻度尺 + 12,631 金色游标
 */
export default function CSDNWall() {
  const ref = useRef<HTMLElement>(null)
  const rulerRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return
    const ctx = gsap.context(() => {
      // 三巨数递增计数（1.6s，stagger 0.2s）
      gsap.utils.toArray<HTMLElement>('.wall-num').forEach((el, i) => {
        const target = Number(el.dataset.value || 0)
        const obj = { v: 0 }
        gsap.to(obj, {
          v: target,
          duration: 1.6,
          delay: i * 0.2,
          ease: 'power2.out',
          snap: { v: 1 },
          scrollTrigger: { trigger: el, start: 'top 70%' },
          onUpdate: () => {
            el.textContent = fmt(Math.round(obj.v))
          },
        })
      })
      // 刻度尺 scaleX 0→1（0.8s）
      gsap.fromTo(
        '.ruler-line',
        { scaleX: 0 },
        {
          scaleX: 1,
          duration: 0.8,
          ease: 'power3.out',
          scrollTrigger: { trigger: rulerRef.current, start: 'top 80%' },
        },
      )
      // 游标自左滑至 12,631 刻度（1s，ease-out）+ 金色脉冲一次
      ScrollTrigger.create({
        trigger: rulerRef.current,
        start: 'top 80%',
        onEnter: () => {
          const track = rulerRef.current
          if (!track) return
          const target = (track.clientWidth * pct(RANK)) / 100
          gsap.fromTo(
            '.ruler-cursor',
            { x: -target, opacity: 0 },
            { x: 0, opacity: 1, duration: 1, ease: 'power2.out', delay: 0.7 },
          )
          gsap.fromTo(
            '.rank-pulse',
            { scale: 1, opacity: 0.7 },
            { scale: 2.2, opacity: 0, duration: 1.2, ease: 'power2.out', delay: 1.7 },
          )
        },
      })
    }, ref)
    return () => ctx.revert()
  }, [])

  return (
    <section ref={ref} className="hairline-b bg-ink py-[120px] max-md:py-[72px]" aria-label="CSDN 数据墙">
      <div className="mx-auto w-full max-w-container px-6 md:px-12">
        <div className="flex flex-wrap items-end justify-between gap-8">
          <SectionHeading eyebrow="FIELD DATA" title="实战之证" />
          <div className="mb-2 flex flex-col items-start gap-3 md:items-end">
            <OutlineButton
              small
              variant="ghost"
              href={csdnSearchUrl('龍芯北辰_UID9622')}
              ariaLabel="前往 CSDN 主页：搜索 龍芯北辰_UID9622"
            >
              <ExternalLink size={14} aria-hidden="true" />
              CSDN 搜索：龍芯北辰_UID9622
            </OutlineButton>
            <span className="text-[13px] text-paper-faint">CSDN 真实数据 · 2026-08-03 快照</span>
          </div>
        </div>

        {/* 三巨数 */}
        <div className="mt-16 grid grid-cols-1 gap-12 md:grid-cols-3">
          {STATS.map((s) => (
            <div key={s.label} className="flex flex-col items-center gap-4">
              <span
                className="wall-num font-serif font-bold text-gold tabular-nums"
                style={{ fontSize: 'clamp(48px, 7vw, 88px)', lineHeight: 1.1 }}
                data-value={s.value}
              >
                {fmt(s.value)}
              </span>
              <span className="h-px w-10 bg-gold" aria-hidden="true" />
              <span className="inline-flex items-center rounded-full border border-dashed border-gold-dim px-[14px] py-1 text-[12px] tracking-[0.2em] text-paper-dim">
                {s.label}
              </span>
            </div>
          ))}
        </div>

        {/* 对数刻度尺：博客总排名量级 */}
        <div className="mt-20">
          <p className="mb-6 text-center font-mono text-[12px] tracking-[0.2em] text-paper-faint">
            博客总排名 · 对数刻度
          </p>
          <div ref={rulerRef} className="relative mx-auto h-16 max-w-[880px]">
            {/* 1px 发线 */}
            <span
              className="ruler-line absolute left-0 top-1/2 h-px w-full origin-left bg-gold-dim"
              aria-hidden="true"
            />
            {/* 刻度 */}
            {TICKS.map((t) => (
              <div
                key={t.v}
                className="absolute top-1/2 -translate-x-1/2"
                style={{ left: `${pct(t.v)}%` }}
                aria-hidden="true"
              >
                <span className="block h-3 w-px bg-gold-dim" />
                <span className="mt-2 block -translate-x-1/2 text-center font-mono text-[11px] text-paper-faint">
                  {t.label}
                </span>
              </div>
            ))}
            {/* 12,631 金色游标 */}
            <div
              className="absolute top-1/2 -translate-x-1/2"
              style={{ left: `${pct(RANK)}%` }}
            >
              <span className="ruler-cursor relative block">
                <span className="block h-5 w-[3px] -translate-y-[2px] bg-gold" aria-hidden="true" />
                <span
                  className="rank-pulse absolute left-1/2 top-[8px] h-5 w-5 -translate-x-1/2 -translate-y-1/2 rounded-full border border-gold opacity-0"
                  aria-hidden="true"
                />
                <span className="absolute left-1/2 top-6 -translate-x-1/2 whitespace-nowrap font-mono text-[12px] font-semibold text-gold">
                  12,631
                </span>
              </span>
            </div>
          </div>
        </div>

        <p className="mt-14 text-center text-[13px] text-paper-faint">
          数据真实可查 · 禁止虚构 · 转载须保留 DNA 追溯码
        </p>
      </div>
    </section>
  )
}
