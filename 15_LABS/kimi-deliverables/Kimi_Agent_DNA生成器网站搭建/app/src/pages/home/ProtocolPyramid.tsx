import { useEffect, useRef } from 'react'
import type { CSSProperties } from 'react'
import { Link } from 'react-router'
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'
import { ArrowRight } from 'lucide-react'
import SectionHeading from '@/components/SectionHeading'
import OutlineButton from '@/components/OutlineButton'

gsap.registerPlugin(ScrollTrigger)

const LAYERS = [
  { id: 'p0', no: 'P0', name: '焊死底座', count: '12 条', quote: '为人民服务 / 中国法律准绳 / 人民数据主权…', width: '40%', tone: 1, welded: true },
  { id: 'p1', no: 'P1', name: '核心宪法', count: '17 条', quote: '16 人格签章 + DNA 验证', width: '55%', tone: 1, welded: false },
  { id: 'p2', no: 'P2', name: '系统规则', count: '41 条', quote: '治理引擎的运行律令', width: '70%', tone: 0.7, welded: false },
  { id: 'p3', no: 'P3', name: '区域适配', count: '10 项', quote: '一国一策', width: '85%', tone: 0.5, welded: false },
  { id: 'p4', no: 'P4', name: '用户自定义', count: '10 项', quote: '权力归于此刻的你', width: '100%', tone: 0.35, welded: false },
]

/** S4 · 协议五层总览（倒金字塔堆叠） */
export default function ProtocolPyramid() {
  const ref = useRef<HTMLElement>(null)

  useEffect(() => {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return
    const ctx = gsap.context(() => {
      gsap.fromTo(
        '.pyramid-layer',
        { clipPath: 'inset(0 100% 0 0)' },
        {
          clipPath: 'inset(0 0% 0 0)',
          duration: 0.5,
          ease: 'power2.out',
          stagger: 0.15,
          scrollTrigger: { trigger: '.pyramid-stack', start: 'top 80%' },
        },
      )
      // P0 朱砂盖章
      gsap.fromTo(
        '.p0-seal',
        { scale: 1.4, rotate: -12, opacity: 0 },
        {
          scale: 1,
          rotate: -6,
          opacity: 1,
          duration: 0.4,
          ease: 'power3.out',
          scrollTrigger: { trigger: '.pyramid-stack', start: 'top 80%' },
          delay: 0.4 + 0.15 * 1,
        },
      )
    }, ref)
    return () => ctx.revert()
  }, [])

  return (
    <section ref={ref} className="hairline-b bg-ink py-[120px] max-md:py-[72px]" aria-label="协议五层总览">
      <div className="mx-auto w-full max-w-container px-6 md:px-12">
        <SectionHeading
          eyebrow="THE CONSTITUTION"
          title="五层协议 · 焊死的底座"
          subtitle="从不可更改的 P0 到底层用户自定义的 P4，权力自上而下递减，自由自下而上递增。"
        />

        <div className="pyramid-stack mt-16 flex flex-col items-center gap-3">
          {LAYERS.map((l) => (
            <Link
              key={l.id}
              to={`/protocol#${l.id}`}
              className="pyramid-layer group relative flex w-full items-center gap-5 border border-line bg-ink-3 px-6 py-5 transition-all duration-300 hover:translate-x-2 hover:border-gold md:w-[var(--layer-w)]"
              style={{ '--layer-w': l.width } as CSSProperties}
            >
              {/* 左缘色条：P0 朱砂，其余金（递减） */}
              <span
                className="absolute bottom-0 left-0 top-0 w-[3px]"
                style={{
                  background: l.welded ? 'var(--vermilion)' : `rgba(201,162,39,${l.tone})`,
                }}
                aria-hidden="true"
              />
              {l.welded ? (
                <span
                  className="p0-seal absolute right-4 top-2 border border-vermilion px-2 py-0.5 font-serif text-[12px] font-bold tracking-[0.2em] text-vermilion"
                  style={{ rotate: '-6deg' }}
                >
                  焊死
                </span>
              ) : null}
              <span className="font-mono text-[24px] font-semibold text-gold">{l.no}</span>
              <span className="flex flex-1 flex-wrap items-baseline gap-x-4 gap-y-1">
                <span className="font-serif text-[18px] font-bold tracking-[0.06em] text-paper">
                  {l.name}
                </span>
                <span className="font-mono text-[13px] text-paper-dim">{l.count}</span>
              </span>
              <span className="hidden max-w-[300px] truncate text-[13px] text-paper-dim lg:inline">
                {l.quote}
              </span>
              <ArrowRight
                size={18}
                className="shrink-0 -translate-x-2 text-gold opacity-0 transition-all duration-300 group-hover:translate-x-0 group-hover:opacity-100"
              />
            </Link>
          ))}
        </div>

        <div className="mt-12 flex justify-end">
          <OutlineButton to="/protocol" variant="ghost">
            展开全部协议条文
          </OutlineButton>
        </div>
      </div>
    </section>
  )
}
