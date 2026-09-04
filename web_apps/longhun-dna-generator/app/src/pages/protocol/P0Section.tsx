// DNA: #龍芯⚡️丙午·甲申·丁未·亥时·䷎谦-DNA-COMPLETION-7fb59fce
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
import { useEffect, useRef, useState } from 'react'
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'
import { AnimatePresence, motion } from 'framer-motion'
import { Lock, Snowflake } from 'lucide-react'
import { P0_CLAUSES } from '@/pages/protocol/data'
import LayerHeader from '@/pages/protocol/LayerHeader'
import VermilionSeal from '@/pages/protocol/VermilionSeal'

gsap.registerPlugin(ScrollTrigger)

/**
 * S3 · P0 焊死底座（本页华章，全文陈列）
 * 十二则法典卡 · 朱砂 hover（焊死语义）· 点击展开冻结记录 · 「P0」巨字视差
 */
export default function P0Section() {
  const rootRef = useRef<HTMLElement>(null)
  const bigRef = useRef<HTMLSpanElement | null>(null)
  const [open, setOpen] = useState<Set<number>>(new Set())

  useEffect(() => {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return
    const ctx = gsap.context(() => {
      // 十二卡 2 列波次入场 stagger 0.07s，触发 20% 视口
      gsap.fromTo(
        '.p0-card',
        { y: 40, opacity: 0 },
        {
          y: 0,
          opacity: 1,
          duration: 0.6,
          ease: 'cubic-bezier(0.22,1,0.36,1)',
          stagger: 0.07,
          scrollTrigger: { trigger: '.p0-grid', start: 'top 80%' },
        },
      )
      // 「P0」巨字视差 y 40→-40
      if (bigRef.current) {
        gsap.fromTo(
          bigRef.current,
          { y: 40 },
          {
            y: -40,
            ease: 'none',
            scrollTrigger: { trigger: rootRef.current, start: 'top bottom', end: 'bottom top', scrub: true },
          },
        )
      }
    }, rootRef)
    return () => ctx.revert()
  }, [])

  const toggle = (i: number) => {
    setOpen((prev) => {
      const next = new Set(prev)
      if (next.has(i)) next.delete(i)
      else next.add(i)
      return next
    })
  }

  return (
    <section ref={rootRef} id="p0" className="scroll-mt-[120px] py-[72px] md:py-[120px]" aria-label="P0 焊死底座">
      <div className="mx-auto w-full max-w-container px-6 md:px-12">
        <LayerHeader
          layer="P0"
          title="焊死底座 · 十二则"
          bigRef={(el) => {
            bigRef.current = el
          }}
          right={<VermilionSeal chars={['不', '可', '更', '改']} size={72} rotate={-4} />}
        />

        {/* 警示条 */}
        <div className="mt-10 flex items-start gap-4 border border-dashed border-vermilion px-6 py-4">
          <Lock size={16} className="mt-0.5 shrink-0 text-vermilion" aria-hidden="true" />
          <p className="text-[13px] leading-[1.9] text-paper-dim">
            此层一经写入，任何人——包括创建者——不可删除、不可修改、不可凌驾。P0 原则：不删除，只冻结。
          </p>
        </div>

        {/* 十二条法典卡 */}
        <div className="p0-grid mt-12 grid grid-cols-1 gap-6 md:grid-cols-2">
          {P0_CLAUSES.map((c, i) => {
            const isOpen = open.has(i)
            return (
              <motion.article
                key={c.numeral}
                layout="position"
                className={`p0-card group relative cursor-pointer border bg-ink-3 px-7 py-6 transition-[border-color,transform] duration-300 hover:-translate-y-[3px] ${
                  isOpen ? 'border-vermilion' : 'border-line hover:border-vermilion'
                }`}
                onClick={() => toggle(i)}
                aria-expanded={isOpen}
              >
                <div className="flex items-start justify-between gap-4">
                  <span className="font-mono text-[12px] tracking-[0.2em] text-vermilion">
                    {c.numeral}
                  </span>
                  <span
                    className="font-mono text-[10px] tracking-[0.18em] text-paper-faint transition-colors duration-300 group-hover:text-vermilion"
                    aria-hidden="true"
                  >
                    WELDED
                  </span>
                </div>
                <h3 className="mt-3 font-serif text-[20px] font-bold tracking-[0.04em] text-paper">
                  {c.title}
                </h3>
                <p className="mt-2 text-[15px] leading-[1.85] text-paper-dim">{c.gloss}</p>

                <AnimatePresence initial={false}>
                  {isOpen ? (
                    <motion.div
                      key="freeze"
                      initial={{ height: 0, opacity: 0 }}
                      animate={{ height: 'auto', opacity: 1 }}
                      exit={{ height: 0, opacity: 0 }}
                      transition={{ duration: 0.45, ease: [0.22, 1, 0.36, 1] }}
                      className="overflow-hidden"
                    >
                      <div className="mt-5 flex items-center gap-3 border-t border-line pt-4">
                        <Snowflake size={13} className="shrink-0 text-gold" aria-hidden="true" />
                        <p className="font-mono text-[12px] tracking-[0.1em] text-paper-dim">
                          STATUS: WELDED · SINCE 2025
                        </p>
                      </div>
                      <p className="mt-2 font-mono text-[11px] leading-[1.8] tracking-[0.06em] text-paper-faint">
                        FREEZE-LOG: 冻结记录以注册表为准 · 此则永不可改写
                      </p>
                    </motion.div>
                  ) : null}
                </AnimatePresence>
              </motion.article>
            )
          })}
        </div>
      </div>
    </section>
  )
}
