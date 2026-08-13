import { useEffect, useRef, useState } from 'react'
import { Link } from 'react-router'
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'
import { motion } from 'framer-motion'
import { MoveHorizontal } from 'lucide-react'
import SectionHeading from '@/components/SectionHeading'
import { hexagramSymbol } from '@/lib/ganzhi'

gsap.registerPlugin(ScrollTrigger)

const WORKS = [
  { slug: 'cnsh', name: 'CNSH 中文原生脚本', caption: '中文即代码' },
  { slug: 'sancai', name: '三才算法', caption: '天地人三才归一' },
  { slug: 'audit', name: '开放审计引擎', caption: '零黑箱的机器证明' },
  { slug: 'csdn-sync', name: 'CSDN 同步引擎', caption: '内容主权直通车' },
  { slug: 'gentleman', name: '君子协议（中英双语）', caption: '一诺既出，天下共鉴' },
  { slug: 'whitepaper', name: '20 人格治理白皮书 v1.4', caption: '十六人格，四维预备' },
  { slug: 'sovereign', name: '无后台主权协议 v3.0', caption: '无后台，方有主权' },
]

/**
 * S6 · 作品带（横向卡片轨）
 * 拖拽仅作用于卡轨（Framer Motion 隔离组件），入场由 GSAP ScrollTrigger 驱动
 */
export default function WorksRail() {
  const ref = useRef<HTMLElement>(null)
  const railWrapRef = useRef<HTMLDivElement>(null)
  const [dragLimit, setDragLimit] = useState(0)

  useEffect(() => {
    const measure = () => {
      const wrap = railWrapRef.current
      if (!wrap) return
      const track = wrap.querySelector<HTMLElement>('.works-track')
      if (!track) return
      setDragLimit(Math.max(0, track.scrollWidth - wrap.clientWidth))
    }
    measure()
    window.addEventListener('resize', measure)
    return () => window.removeEventListener('resize', measure)
  }, [])

  useEffect(() => {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return
    const ctx = gsap.context(() => {
      gsap.fromTo(
        '.works-rail',
        { x: 120, opacity: 0 },
        {
          x: 0,
          opacity: 1,
          duration: 0.8,
          ease: 'power3.out',
          clearProps: 'transform,opacity',
          scrollTrigger: { trigger: ref.current, start: 'top 80%' },
        },
      )
      gsap.fromTo(
        '.work-card-inner',
        { y: 20, opacity: 0 },
        {
          y: 0,
          opacity: 1,
          duration: 0.5,
          stagger: 0.05,
          ease: 'power3.out',
          clearProps: 'transform,opacity',
          scrollTrigger: { trigger: ref.current, start: 'top 80%' },
        },
      )
    }, ref)
    return () => ctx.revert()
  }, [])

  return (
    <section ref={ref} className="hairline-b overflow-hidden bg-ink py-[120px] max-md:py-[72px]" aria-label="作品开源">
      <div className="mx-auto w-full max-w-container px-6 md:px-12">
        <div className="flex items-end justify-between gap-8">
          <SectionHeading eyebrow="OPEN WORKS" title="作品开源 · 七器" />
          <p className="mb-2 hidden items-center gap-2 text-[13px] text-paper-dim md:flex">
            <MoveHorizontal size={16} className="text-gold" />
            拖拽探索
          </p>
        </div>
      </div>

      {/* 卡轨：桌面可拖拽，移动端原生横滚；左右缘渐变遮罩 */}
      <div ref={railWrapRef} className="works-rail relative mt-14">
        <div className="pointer-events-none absolute inset-y-0 left-0 z-10 w-16 bg-gradient-to-r from-ink to-transparent" aria-hidden="true" />
        <div className="pointer-events-none absolute inset-y-0 right-0 z-10 w-16 bg-gradient-to-l from-ink to-transparent" aria-hidden="true" />
        <div className="overflow-x-auto md:overflow-visible">
          <motion.div
            className="works-track flex w-max cursor-grab gap-6 px-6 active:cursor-grabbing md:px-12"
            drag="x"
            dragConstraints={{ left: -dragLimit, right: 0 }}
            dragElastic={0.06}
          >
            {WORKS.map((w, i) => (
              <div
                key={w.slug}
                className="work-card group relative h-[420px] w-[320px] shrink-0 select-none border border-line bg-ink-3 transition-all duration-300 hover:-translate-y-1.5 hover:border-gold"
              >
                {/* 顶部 2px 金条 */}
                <span
                  className="absolute left-0 top-0 h-[2px] w-full origin-left scale-x-0 bg-gold transition-transform duration-300 group-hover:scale-x-100"
                  aria-hidden="true"
                />
                {/* 卦符水印 */}
                <span
                  className="pointer-events-none absolute bottom-4 right-4 select-none font-serif text-[96px] leading-none text-gold opacity-0 transition-opacity duration-500 group-hover:opacity-[0.08]"
                  aria-hidden="true"
                >
                  {hexagramSymbol(i * 9 + 3)}
                </span>
                <div className="work-card-inner flex h-full flex-col p-7">
                  <span className="font-mono text-[12px] tracking-[0.2em] text-gold-dim">
                    WORK {String(i + 1).padStart(2, '0')}
                  </span>
                  <h3 className="mt-6 font-serif text-[22px] font-bold leading-[1.5] tracking-[0.04em] text-paper">
                    {w.name}
                  </h3>
                  <p className="mt-3 text-[13px] leading-[1.9] text-paper-dim">{w.caption}</p>
                  <div className="mt-auto">
                    <Link
                      to={`/works#${w.slug}`}
                      className="inline-flex items-center gap-2 border border-line-strong px-5 py-2 font-serif text-[13px] font-bold tracking-[0.3em] text-gold transition-colors duration-300 hover:border-gold hover:text-gold-bright"
                      onClick={(e) => e.stopPropagation()}
                    >
                      阅
                    </Link>
                  </div>
                </div>
              </div>
            ))}
          </motion.div>
        </div>
      </div>
    </section>
  )
}
