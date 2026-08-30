// DNA: #龍芯⚡️丙午·甲申·丁未·亥时·䷎谦-DNA-COMPLETION-684c63b0
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
import { useEffect, useRef, useState } from 'react'
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'
import { AnimatePresence, motion } from 'framer-motion'
import { ChevronDown } from 'lucide-react'
import DNACode from '@/components/DNACode'
import { P1_CLAUSES } from '@/pages/protocol/data'
import LayerHeader from '@/pages/protocol/LayerHeader'

gsap.registerPlugin(ScrollTrigger)

/** 16 人格会签点阵（4×4，金点 6px，展开时自左上至右下逐格点亮） */
function SignDots({ lit }: { lit: boolean }) {
  return (
    <motion.div
      className="grid shrink-0 grid-cols-4 gap-[5px]"
      initial={false}
      animate={lit ? 'lit' : 'dim'}
      variants={{ lit: { transition: { staggerChildren: 0.03 } }, dim: {} }}
      aria-label={lit ? '16 人格已全体会签' : '会签点阵'}
      role="img"
    >
      {Array.from({ length: 16 }, (_, i) => (
        <motion.span
          key={i}
          className="h-[6px] w-[6px] rounded-full"
          variants={{
            dim: { backgroundColor: 'rgba(201,162,39,0.16)', scale: 1 },
            lit: { backgroundColor: '#C9A227', scale: [1, 1.5, 1] },
          }}
          transition={{ duration: 0.3 }}
        />
      ))}
    </motion.div>
  )
}

/**
 * S4 · P1 核心宪法（17 条 · 签章陈列）
 * 奏折条纵向排列 · 手风琴互斥（默认 §01）· 展开显示全文 + DNA + 会签时间
 */
export default function P1Section() {
  const rootRef = useRef<HTMLElement>(null)
  const [openId, setOpenId] = useState<string>(P1_CLAUSES[0].id)

  useEffect(() => {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return
    const ctx = gsap.context(() => {
      gsap.fromTo(
        '.p1-bar',
        { x: -30, opacity: 0 },
        {
          x: 0,
          opacity: 1,
          duration: 0.5,
          ease: 'cubic-bezier(0.22,1,0.36,1)',
          stagger: 0.05,
          scrollTrigger: { trigger: '.p1-list', start: 'top 80%' },
        },
      )
    }, rootRef)
    return () => ctx.revert()
  }, [])

  return (
    <section
      ref={rootRef}
      id="p1"
      className="hairline-t scroll-mt-[120px] bg-ink-2 py-[72px] md:py-[120px]"
      aria-label="P1 核心宪法"
    >
      <div className="mx-auto w-full max-w-container px-6 md:px-12">
        <LayerHeader
          layer="P1"
          title="核心宪法 · 十七则"
          caption="16 人格签章 + DNA 验证，缺一不生效。"
        />

        <div className="p1-list mt-12 flex flex-col border-t border-line">
          {P1_CLAUSES.map((c) => {
            const isOpen = openId === c.id
            return (
              <div key={c.id} className="p1-bar border-b border-line">
                <button
                  type="button"
                  onClick={() => setOpenId(isOpen ? '' : c.id)}
                  aria-expanded={isOpen}
                  className={`flex w-full items-center gap-5 py-5 text-left transition-colors duration-300 ${
                    isOpen ? 'bg-ink-3 px-5 md:px-7' : 'px-2 hover:bg-ink-3 md:px-4'
                  }`}
                >
                  <span className="w-10 shrink-0 font-mono text-[14px] tracking-[0.08em] text-gold">
                    {c.id}
                  </span>
                  <span className="flex-1 font-serif text-[18px] font-bold tracking-[0.04em] text-paper">
                    {c.title}
                  </span>
                  <SignDots lit={isOpen} />
                  <ChevronDown
                    size={16}
                    aria-hidden="true"
                    className={`shrink-0 text-paper-dim transition-transform duration-300 ${
                      isOpen ? 'rotate-180 text-gold' : ''
                    }`}
                  />
                </button>

                <AnimatePresence initial={false}>
                  {isOpen ? (
                    <motion.div
                      key="body"
                      initial={{ height: 0, opacity: 0 }}
                      animate={{ height: 'auto', opacity: 1 }}
                      exit={{ height: 0, opacity: 0 }}
                      transition={{ duration: 0.45, ease: [0.22, 1, 0.36, 1] }}
                      className="overflow-hidden"
                    >
                      <div className="grid gap-8 bg-ink-3 px-5 pb-8 pt-2 md:grid-cols-[1fr_320px] md:px-7">
                        <div>
                          <p className="max-w-prose text-[18px] leading-[1.9] tracking-[0.02em] text-paper-dim">
                            {c.body}
                          </p>
                          <p className="mt-5 font-mono text-[12px] tracking-[0.08em] text-gold-dim">
                            {c.signedAt}
                          </p>
                        </div>
                        <DNACode code={c.dna} fontSize={12} />
                      </div>
                    </motion.div>
                  ) : null}
                </AnimatePresence>
              </div>
            )
          })}
        </div>
      </div>
    </section>
  )
}
