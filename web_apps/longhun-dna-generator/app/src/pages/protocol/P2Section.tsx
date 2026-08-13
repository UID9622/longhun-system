import { useEffect, useMemo, useRef, useState } from 'react'
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'
import { AnimatePresence, motion } from 'framer-motion'
import { Search } from 'lucide-react'
import SealTag from '@/components/SealTag'
import { P2_RULES } from '@/pages/protocol/data'
import LayerHeader from '@/pages/protocol/LayerHeader'

gsap.registerPlugin(ScrollTrigger)

/**
 * S5 · P2 系统规则（41 条 · 索引矩阵）
 * 7 列编号瓦片 · 顶部检索实时过滤 · 点击瓦片详情面板滑出（移动：下方抽屉）
 */
export default function P2Section() {
  const rootRef = useRef<HTMLElement>(null)
  const [query, setQuery] = useState('')
  const [selectedId, setSelectedId] = useState(P2_RULES[0].id)

  useEffect(() => {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return
    const ctx = gsap.context(() => {
      // 瓦片自中心径向 stagger：每片 0.02s，总约 0.9s
      gsap.fromTo(
        '.p2-tile',
        { scale: 0.7, opacity: 0 },
        {
          scale: 1,
          opacity: 1,
          duration: 0.4,
          ease: 'power3.out',
          stagger: { each: 0.02, grid: [6, 7], from: 'center' },
          scrollTrigger: { trigger: '.p2-tiles', start: 'top 80%' },
        },
      )
    }, rootRef)
    return () => ctx.revert()
  }, [])

  const q = query.trim()
  const matched = useMemo(() => {
    if (!q) return new Set(P2_RULES.map((r) => r.id))
    return new Set(
      P2_RULES.filter(
        (r) => r.id.includes(q) || r.title.includes(q) || r.body.includes(q) || r.tag.includes(q),
      ).map((r) => r.id),
    )
  }, [q])

  const selected = P2_RULES.find((r) => r.id === selectedId) ?? P2_RULES[0]

  return (
    <section
      ref={rootRef}
      id="p2"
      className="hairline-t scroll-mt-[120px] py-[72px] md:py-[120px]"
      aria-label="P2 系统规则"
    >
      <div className="mx-auto w-full max-w-container px-6 md:px-12">
        <LayerHeader layer="P2" title="系统规则 · 四十一则" caption="运行之规，迭代之矩。" />

        {/* 检索框 */}
        <div className="mt-10 flex max-w-[420px] items-center gap-3 border border-line bg-ink-3 px-4 py-3 transition-colors duration-300 focus-within:border-gold">
          <Search size={15} className="shrink-0 text-paper-faint" aria-hidden="true" />
          <input
            type="search"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="检索规则…"
            aria-label="检索系统规则"
            className="w-full bg-transparent font-mono text-[13px] tracking-[0.06em] text-paper placeholder:text-paper-faint focus:outline-none"
          />
          {q ? (
            <span className="shrink-0 font-mono text-[11px] text-gold-dim">
              {matched.size}/41
            </span>
          ) : null}
        </div>

        <div className="mt-10 grid gap-10 lg:grid-cols-[1fr_360px]">
          {/* 索引矩阵：7 列（移动 2 列）56×56 瓦片 */}
          <div className="p2-tiles grid grid-cols-2 gap-3 sm:grid-cols-4 md:grid-cols-7">
            {P2_RULES.map((r) => {
              const isHit = matched.has(r.id)
              const isSel = selectedId === r.id
              return (
                <button
                  key={r.id}
                  type="button"
                  onClick={() => setSelectedId(r.id)}
                  aria-pressed={isSel}
                  aria-label={`${r.id} ${r.title}`}
                  style={{ transitionDuration: '250ms' }}
                  className={`p2-tile flex h-14 w-full items-center justify-center border font-mono text-[13px] tracking-[0.06em] transition-all md:w-14 ${
                    isSel
                      ? 'border-gold bg-ink-4 text-gold-bright'
                      : q && isHit
                        ? 'border-line-strong text-gold hover:border-gold'
                        : 'border-line text-paper-dim hover:border-gold hover:text-paper'
                  } ${isHit ? 'opacity-100 scale-100' : 'opacity-[0.15] scale-[0.92]'}`}
                >
                  {r.id}
                </button>
              )
            })}
          </div>

          {/* 详情面板（移动：下方抽屉） */}
          <div className="lg:sticky lg:top-[140px] lg:self-start">
            <AnimatePresence mode="wait">
              <motion.div
                key={selected.id}
                initial={{ x: 40, opacity: 0 }}
                animate={{ x: 0, opacity: 1 }}
                exit={{ x: 20, opacity: 0 }}
                transition={{ duration: 0.4, ease: [0.22, 1, 0.36, 1] }}
                className="border border-line border-l-[3px] border-l-gold bg-ink-3 px-7 py-6"
              >
                <div className="flex items-center justify-between gap-4">
                  <span className="font-mono text-[14px] tracking-[0.1em] text-gold">
                    {selected.id}
                  </span>
                  <SealTag>{selected.tag}</SealTag>
                </div>
                <h3 className="mt-4 font-serif text-[24px] font-bold tracking-[0.04em] text-paper">
                  {selected.title}
                </h3>
                <p className="mt-3 text-[16px] leading-[1.85] text-paper-dim">{selected.body}</p>
                <p className="mt-5 border-t border-line pt-4 font-mono text-[11px] tracking-[0.08em] text-paper-faint">
                  关联层 · P2 系统规则 · 全文以注册表冻结版为准
                </p>
              </motion.div>
            </AnimatePresence>
          </div>
        </div>
      </div>
    </section>
  )
}
