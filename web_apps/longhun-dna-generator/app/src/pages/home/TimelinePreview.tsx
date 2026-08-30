// DNA: #龍芯⚡️丙午·甲申·丁未·亥时·䷎谦-DNA-COMPLETION-e4d78b87
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
import { useEffect, useRef } from 'react'
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'
import SectionHeading from '@/components/SectionHeading'
import OutlineButton from '@/components/OutlineButton'

gsap.registerPlugin(ScrollTrigger)

const NODES = [
  { date: '2025-05', title: '预见 · 立项', caption: '预见 AI 文明跃迁，龍魂立项', side: 'left' as const, latest: false },
  { date: '2026-01-31', title: '君子协议发布', caption: '一诺既出，天下共鉴（中英双语）', side: 'right' as const, latest: false },
  { date: '2026-08-03', title: 'DNA v2.0 · 官网落成', caption: 'DNA 生成器 v2.0 上线，官网竣工', side: 'left' as const, latest: true },
]

/** S7 · 远征时间线预告（纵向三节点 + CTA） */
export default function TimelinePreview() {
  const ref = useRef<HTMLElement>(null)

  useEffect(() => {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return
    const ctx = gsap.context(() => {
      // 竖线随滚动生长
      gsap.fromTo(
        '.tl-line',
        { scaleY: 0 },
        {
          scaleY: 1,
          ease: 'none',
          scrollTrigger: { trigger: '.tl-track', start: 'top 80%', end: 'bottom 60%', scrub: true },
        },
      )
      // 节点入场：左右交替
      gsap.utils.toArray<HTMLElement>('.tl-node').forEach((node) => {
        const fromX = node.dataset.side === 'left' ? -40 : 40
        gsap.fromTo(
          node,
          { x: fromX, opacity: 0 },
          {
            x: 0,
            opacity: 1,
            duration: 0.6,
            ease: 'power3.out',
            scrollTrigger: { trigger: node, start: 'top 70%' },
          },
        )
      })
    }, ref)
    return () => ctx.revert()
  }, [])

  return (
    <section ref={ref} className="hairline-b bg-ink py-[120px] max-md:py-[72px]" aria-label="远征时间线预告">
      <div className="mx-auto w-full max-w-container px-6 md:px-12">
        <SectionHeading eyebrow="THE EXPEDITION" title="远征 · 从预见到奠基" align="center" />

        <div className="tl-track relative mx-auto mt-20 max-w-[880px]">
          {/* 中央竖金线（移动端靠左） */}
          <span
            className="tl-line absolute left-[7px] top-0 h-full w-px origin-top bg-gold md:left-1/2"
            aria-hidden="true"
          />
          <div className="flex flex-col gap-16">
            {NODES.map((n) => (
              <div
                key={n.date}
                className={`relative grid items-center gap-6 pl-10 md:grid-cols-2 md:pl-0 ${
                  n.side === 'left' ? '' : ''
                }`}
              >
                {/* 节点金点 + 脉冲环 */}
                <span className="absolute left-0 top-2 md:left-1/2 md:-translate-x-1/2" aria-hidden="true">
                  <span className="block h-[15px] w-[15px] rounded-full border border-gold bg-ink" />
                  <span className="absolute inset-0 flex items-center justify-center">
                    <span className="block h-2 w-2 rounded-full bg-gold" />
                  </span>
                  <span
                    className={`absolute -inset-[5px] rounded-full border border-gold ${
                      n.latest ? 'animate-pulse-ring' : 'opacity-0'
                    }`}
                  />
                </span>
                <div
                  className={`tl-node ${
                    n.side === 'left'
                      ? 'md:col-start-1 md:pr-14 md:text-right'
                      : 'md:col-start-2 md:pl-14 md:text-left'
                  }`}
                  data-side={n.side}
                >
                  <p className="font-mono text-[15px] font-semibold tracking-[0.08em] text-gold">{n.date}</p>
                  <h3 className="mt-2 font-serif text-[22px] font-bold tracking-[0.05em] text-paper">{n.title}</h3>
                  <p className="mt-2 text-[13px] leading-[1.9] text-paper-dim">{n.caption}</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="mt-16 flex justify-center">
          <OutlineButton to="/timeline" variant="ghost">
            完整远征日志
          </OutlineButton>
        </div>
      </div>
    </section>
  )
}
