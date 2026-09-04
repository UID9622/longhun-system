import { useEffect, useMemo, useRef } from 'react'
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'
import { getGanzhi } from '@/lib/ganzhi'
import { MILESTONES, TOTAL_DAYS } from '@/pages/timeline/milestones'
import MilestoneChapter from '@/pages/timeline/MilestoneChapter'
import GanzhiCharCanvas from '@/pages/timeline/GanzhiCharCanvas'

gsap.registerPlugin(ScrollTrigger)

/**
 * S2 · 滚动时间线主轴（timeline.md）
 * 视口左缘 1px 竖金线随滚动前进（scrub）· DAY n / 460 常驻读数 · 章间干支过渡带
 */
export default function ExpeditionTrack() {
  const ref = useRef<HTMLDivElement>(null)
  const chipRef = useRef<HTMLDivElement>(null)
  const dayRef = useRef<HTMLSpanElement>(null)
  const now = useMemo(() => getGanzhi(), [])

  useEffect(() => {
    const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches
    const dayEl = dayRef.current
    const chipEl = chipRef.current
    const ctx = gsap.context(() => {
      if (reduced) {
        // 降级：金线全程点亮，读数定格终态
        if (dayEl) dayEl.textContent = `DAY ${TOTAL_DAYS} / ${TOTAL_DAYS}`
      } else {
        // 金线随滚动 scaleY 前进 + DAY 读数线性插值 0→460（snap 1）
        gsap.fromTo(
          '.rail-fill',
          { scaleY: 0 },
          {
            scaleY: 1,
            ease: 'none',
            scrollTrigger: {
              trigger: ref.current,
              start: 'top 55%',
              end: 'bottom 55%',
              scrub: true,
              onUpdate: (self) => {
                if (dayEl) {
                  dayEl.textContent = `DAY ${Math.round(self.progress * TOTAL_DAYS)} / ${TOTAL_DAYS}`
                }
              },
            },
          },
        )
      }
      // 常驻读数：进入主轴区间时显现
      ScrollTrigger.create({
        trigger: ref.current,
        start: 'top 70%',
        end: 'bottom 25%',
        onToggle: (self) => {
          if (chipEl) chipEl.style.opacity = self.isActive ? '1' : '0'
        },
      })
    }, ref)
    return () => ctx.revert()
  }, [])

  return (
    <section ref={ref} className="relative bg-ink" aria-label="远征时间线主轴">
      {/* 竖金线轨道：x=80px（桌面）/ 20px（移动） */}
      <span className="absolute inset-y-0 left-5 w-px bg-line md:left-20" aria-hidden="true">
        <span className="rail-fill block h-full w-full origin-top bg-gold" />
      </span>

      {/* 常驻 mono 进度读数 */}
      <div
        ref={chipRef}
        className="pointer-events-none fixed bottom-6 left-4 z-40 border border-line bg-ink/90 px-4 py-3 opacity-0 transition-opacity duration-300 md:left-8"
        aria-hidden="true"
      >
        <p className="font-mono text-[13px] font-semibold tracking-[0.12em] text-gold">
          <span ref={dayRef} className="tabular-nums">
            DAY 000 / {TOTAL_DAYS}
          </span>
        </p>
        <p className="mt-1 font-mono text-[11px] tracking-[0.08em] text-paper-faint">
          此刻 {now.year}年 · {now.month}月
        </p>
      </div>

      {/* 五座里程碑章 + 章间视差过渡带（40vh，干支字符稀疏上浮） */}
      {MILESTONES.map((m, i) => (
        <div key={m.id}>
          <MilestoneChapter m={m} />
          {i < MILESTONES.length - 1 ? (
            <div className="relative h-[40vh]" aria-hidden="true">
              <GanzhiCharCanvas count={6} direction="rise" />
            </div>
          ) : null}
        </div>
      ))}
    </section>
  )
}
