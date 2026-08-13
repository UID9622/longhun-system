import { useEffect, useRef, useState } from 'react'
import { Link } from 'react-router'
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'
import { ArrowUpRight, Github } from 'lucide-react'
import SectionHeading from '@/components/SectionHeading'
import SealTag from '@/components/SealTag'
import DNACode from '@/components/DNACode'
import OutlineButton from '@/components/OutlineButton'
import { WORKS, HASH_PLACEHOLDER_NOTE, csdnSearchUrl } from '@/pages/works/worksData'
import type { WorkEntry } from '@/pages/works/worksData'

gsap.registerPlugin(ScrollTrigger)

/**
 * S2 · 七器长卷（works.md）
 * 法典/目录式全宽横栏 · clip-path 逐条揭开 · 手风琴详情（同屏仅一条展开）
 */
export default function SevenScrolls() {
  const ref = useRef<HTMLElement>(null)
  const [openId, setOpenId] = useState<string | null>(null)

  useEffect(() => {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return
    const ctx = gsap.context(() => {
      gsap.fromTo(
        '.scroll-entry',
        { clipPath: 'inset(0 100% 0 0)' },
        {
          clipPath: 'inset(0 0% 0 0)',
          duration: 0.5,
          stagger: 0.12,
          ease: 'power3.out',
          clearProps: 'clipPath',
          scrollTrigger: { trigger: '.scroll-list', start: 'top 78%' },
        },
      )
      gsap.fromTo(
        '.scroll-num',
        { opacity: 0 },
        {
          opacity: 1,
          duration: 0.5,
          stagger: 0.12,
          delay: 0.3,
          ease: 'power2.out',
          scrollTrigger: { trigger: '.scroll-list', start: 'top 78%' },
        },
      )
    }, ref)
    return () => ctx.revert()
  }, [])

  return (
    <section ref={ref} className="hairline-b bg-ink py-[120px] max-md:py-[72px]" aria-label="七器长卷">
      <div className="mx-auto w-full max-w-container px-6 md:px-12">
        <SectionHeading
          eyebrow="THE SEVEN"
          title="七器"
          subtitle="七项作品，法典式索引。点击条目展开详情——每一器皆铸有 DNA 追溯码。"
        />

        <div className="scroll-list mt-16 hairline-t">
          {WORKS.map((w) => (
            <ScrollEntry
              key={w.id}
              work={w}
              open={openId === w.id}
              onToggle={() => setOpenId(openId === w.id ? null : w.id)}
            />
          ))}
        </div>
      </div>
    </section>
  )
}

function ScrollEntry({
  work,
  open,
  onToggle,
}: {
  work: WorkEntry
  open: boolean
  onToggle: () => void
}) {
  const panelId = `work-panel-${work.id}`
  return (
    <article id={work.id} className="scroll-entry group relative scroll-mt-28 hairline-b">
      {/* 首页 WorksRail 兼容锚点（/works#csdn-sync） */}
      {work.id === 'csdn' ? (
        <span id="csdn-sync" className="absolute -top-28" aria-hidden="true" />
      ) : null}
      {/* 左侧 3px 金条（hover scaleY 0→1） */}
      <span
        className="pointer-events-none absolute left-0 top-0 z-10 h-full w-[3px] origin-top scale-y-0 bg-gold transition-transform duration-300 group-hover:scale-y-100"
        aria-hidden="true"
      />
      <button
        type="button"
        onClick={onToggle}
        aria-expanded={open}
        aria-controls={panelId}
        className="grid w-full grid-cols-[auto_1fr_auto] items-center gap-x-6 gap-y-3 bg-ink-3 px-5 py-8 text-left transition-colors duration-300 hover:bg-ink-4 md:grid-cols-[72px_minmax(0,5fr)_minmax(0,4fr)_minmax(0,3fr)] md:px-8 md:py-0 md:min-h-[140px]"
      >
        <span className="scroll-num font-mono text-[32px] leading-none text-gold-dim tabular-nums">
          {work.index}
        </span>
        <span className="flex min-w-0 flex-col gap-3">
          <span className="font-serif text-[22px] font-bold tracking-[0.04em] text-paper md:text-[26px]">
            {work.name}
          </span>
          <span>
            <SealTag>{work.category}</SealTag>
          </span>
        </span>
        <span className="col-span-2 flex min-w-0 flex-col gap-2 md:col-span-1">
          <span className="text-[15px] leading-[1.85] text-paper-dim">{work.caption}</span>
          <span className="font-mono text-[13px] tracking-[0.04em] text-gold-dim">
            {work.version}
          </span>
        </span>
        <span className="col-span-3 flex items-center justify-end gap-4 md:col-span-1">
          <span className="hidden max-w-[220px] truncate font-mono text-[11px] tracking-[0.04em] text-paper-faint lg:inline">
            {work.dna}
          </span>
          <ArrowUpRight
            size={18}
            className="shrink-0 text-gold-dim transition-all duration-300 group-hover:translate-x-1.5 group-hover:text-gold"
            aria-hidden="true"
          />
        </span>
      </button>

      {/* 手风琴详情：grid-rows 0fr→1fr 实现高度 auto 过渡 0.45s */}
      <div
        id={panelId}
        className={`grid transition-[grid-template-rows] duration-[450ms] ease-out ${
          open ? 'grid-rows-[1fr]' : 'grid-rows-[0fr]'
        }`}
      >
        <div className="overflow-hidden">
          <div
            className={`border-t border-line bg-ink-2 px-5 py-10 transition-all duration-[350ms] md:px-8 ${
              open ? 'translate-y-0 opacity-100' : 'translate-y-4 opacity-0'
            }`}
          >
            <div className="grid gap-10 md:grid-cols-2">
              <div className="flex flex-col gap-4">
                {work.detail.map((line, i) => (
                  <p key={i} className="text-[15px] leading-[1.95] text-paper-dim">
                    {line}
                  </p>
                ))}
                <p className="mt-2 font-mono text-[11px] leading-[1.8] text-paper-faint">
                  {HASH_PLACEHOLDER_NOTE}
                </p>
              </div>
              <div className="flex flex-col gap-6">
                <DNACode code={work.dna} fontSize={13} />
                <div className="flex flex-wrap items-center gap-4">
                  <OutlineButton
                    small
                    variant="ghost"
                    href={csdnSearchUrl(work.searchQuery)}
                    ariaLabel={`获取源码：CSDN 搜索 ${work.searchQuery}`}
                  >
                    <Github size={14} aria-hidden="true" />
                    获取源码
                  </OutlineButton>
                  <Link
                    to="/dna#verify"
                    className="inline-flex items-center gap-2 text-[13px] tracking-[0.1em] text-gold underline decoration-gold-dim underline-offset-8 transition-colors duration-200 hover:text-gold-bright hover:decoration-gold"
                  >
                    验证 DNA
                    <ArrowUpRight size={14} aria-hidden="true" />
                  </Link>
                </div>
                <p className="font-mono text-[11px] text-paper-faint">
                  快速链接 · CSDN 搜索：{work.searchQuery}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </article>
  )
}
