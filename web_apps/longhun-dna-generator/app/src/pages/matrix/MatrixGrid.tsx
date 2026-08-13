import { useRef, useState } from 'react'
import { AnimatePresence, motion, useInView, useScroll, useTransform } from 'framer-motion'
import { X } from 'lucide-react'
import SealTag from '@/components/SealTag'
import { DIMS, PERSONAS, radialDelay } from '@/pages/matrix/personas'
import type { Persona } from '@/pages/matrix/personas'
import RadarChart from '@/pages/matrix/RadarChart'
import PersonaSeal from '@/pages/matrix/PersonaSeal'

const dimName = (key: string) => DIMS.find((d) => d.key === key)?.name ?? key

/** 详情内容（桌面 sticky 面板与移动底部抽屉共用） */
function DetailContent({ persona }: { persona: Persona }) {
  return (
    <div className="flex flex-col gap-5">
      <div className="flex items-start justify-between gap-4">
        <div>
          <p className="font-mono text-[12px] tracking-[0.3em] text-gold-dim">{persona.no}</p>
          <p className="mt-2 font-serif text-[64px] font-black leading-none tracking-[0.04em] text-gold">
            {persona.code}
          </p>
          <p className="mt-3 font-serif text-[16px] font-bold tracking-[0.12em] text-paper">
            {persona.full}
          </p>
        </div>
        {/* 该人格签章样式 */}
        <div className="flex flex-col items-center gap-2">
          <PersonaSeal char={persona.code[0]} size={44} />
          <span className="font-mono text-[10px] tracking-[0.2em] text-paper-faint">签章样式</span>
        </div>
      </div>
      <div>
        <SealTag>主维 · {dimName(persona.primary)}</SealTag>
      </div>
      <p className="text-[15px] leading-[1.9] text-paper-dim">{persona.bio}</p>
      <div className="hairline-t pt-5">
        <RadarChart values={persona.vector} resetKey={persona.no} />
        <p className="mt-3 text-center font-mono text-[11px] tracking-[0.08em] text-paper-faint">
          {DIMS.map((d, i) => `${d.key} ${persona.vector[i]}`).join(' · ')}
        </p>
      </div>
    </div>
  )
}

/**
 * S3 · 4×4 交互大矩阵（matrix.md S3）
 * 径向入场 · 点选点亮 · 桌面右侧 sticky 详情 / 移动底部抽屉
 * 纯 Framer Motion 域（不引入 GSAP）
 */
export default function MatrixGrid() {
  const ref = useRef<HTMLElement>(null)
  const gridRef = useRef<HTMLDivElement>(null)
  const gridInView = useInView(gridRef, { once: true, amount: 0.2 })
  const [selected, setSelected] = useState<number | null>(null)

  // 背景 matrix-grid-bg.png 极缓视差（y ±30px scrub）
  const { scrollYProgress } = useScroll({ target: ref, offset: ['start end', 'end start'] })
  const bgY = useTransform(scrollYProgress, [0, 1], [30, -30])

  const persona = selected !== null ? PERSONAS[selected] : null

  return (
    <section ref={ref} className="hairline-b relative overflow-hidden bg-ink-2 py-[120px] max-md:py-[72px]" aria-label="矩阵点将">
      {/* 视差背景 */}
      <motion.div
        className="pointer-events-none absolute inset-[-60px] opacity-[0.14]"
        style={{
          y: bgY,
          backgroundImage: "url('/matrix-grid-bg.png')",
          backgroundSize: 'min(90vw, 900px)',
          backgroundPosition: 'center',
          backgroundRepeat: 'repeat',
        }}
        aria-hidden="true"
      />

      <div className="relative mx-auto w-full max-w-container px-6 md:px-12">
        <div className="flex items-end justify-between gap-6">
          <div>
            <span className="eyebrow">THE GRID</span>
            <h2 className="mt-6 font-serif text-[clamp(30px,4vw,52px)] font-bold leading-[1.15] tracking-[0.05em] text-paper">
              矩阵 · 点将
            </h2>
          </div>
          <p className="hidden pb-2 text-[13px] text-paper-dim md:block">点任一格，识其人格。十六格皆活。</p>
        </div>

        <div className="mt-14 flex flex-col gap-10 lg:flex-row lg:items-start">
          {/* 4×4 矩阵（移动 2 列） */}
          <div ref={gridRef} className="grid flex-1 grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-4 lg:gap-4">
            {PERSONAS.map((p, i) => {
              const active = selected === i
              const dimmed = selected !== null && !active
              return (
                <motion.button
                  key={p.no}
                  type="button"
                  onClick={() => setSelected(active ? null : i)}
                  initial={{ scale: 0.5, opacity: 0, y: 0 }}
                  animate={
                    gridInView
                      ? { scale: 1, opacity: dimmed ? 0.35 : 1, y: active ? -6 : 0 }
                      : { scale: 0.5, opacity: 0, y: 0 }
                  }
                  transition={
                    gridInView && selected === null
                      ? { duration: 0.5, delay: radialDelay(i), ease: [0.22, 1, 0.36, 1] }
                      : { duration: 0.3, ease: [0.22, 1, 0.36, 1] }
                  }
                  whileHover={{ y: active ? -6 : -3 }}
                  className={`group relative aspect-square border bg-ink-3 transition-colors duration-300 ${
                    active ? 'border-gold' : 'border-line hover:border-line-strong'
                  }`}
                  aria-pressed={active}
                  aria-label={`人格 ${p.full}（${p.no}）`}
                >
                  {/* 选中四边金线绘制 */}
                  <span className={`pointer-events-none absolute left-0 top-0 h-px w-full origin-left bg-gold-bright transition-transform duration-150 ${active ? 'scale-x-100' : 'scale-x-0'}`} aria-hidden="true" />
                  <span className={`pointer-events-none absolute right-0 top-0 h-full w-px origin-top bg-gold-bright transition-transform delay-75 duration-150 ${active ? 'scale-y-100' : 'scale-y-0'}`} aria-hidden="true" />
                  <span className={`pointer-events-none absolute bottom-0 right-0 h-px w-full origin-right bg-gold-bright transition-transform delay-150 duration-150 ${active ? 'scale-x-100' : 'scale-x-0'}`} aria-hidden="true" />
                  <span className={`pointer-events-none absolute bottom-0 left-0 h-full w-px origin-bottom bg-gold-bright transition-transform delay-200 duration-150 ${active ? 'scale-y-100' : 'scale-y-0'}`} aria-hidden="true" />
                  {/* 格角折角金饰 */}
                  <span className="pointer-events-none absolute right-0 top-0 h-3 w-3 border-l border-b border-gold-dim transition-colors duration-300 group-hover:border-gold" aria-hidden="true" />

                  <span className="flex h-full flex-col items-center justify-center gap-2 px-2">
                    <span className={`font-serif font-black leading-none tracking-[0.06em] transition-colors duration-300 text-[clamp(28px,3.4vw,40px)] ${active ? 'text-gold-bright' : 'text-gold'}`}>
                      {p.code}
                    </span>
                    <span className="font-mono text-[10px] tracking-[0.24em] text-paper-faint">{p.no}</span>
                    {/* 微缩五维条 */}
                    <span className="flex h-[5px] w-[72%] items-end gap-[2px]" aria-hidden="true">
                      {p.vector.map((v, di) => (
                        <span
                          key={di}
                          className="h-full"
                          style={{
                            width: `${v}%`,
                            background: `rgba(201,162,39,${0.35 + 0.65 * (v / 100)})`,
                          }}
                        />
                      ))}
                    </span>
                  </span>
                </motion.button>
              )
            })}
          </div>

          {/* 桌面：右侧 sticky 详情面板 */}
          <aside className="hidden w-[360px] shrink-0 lg:block">
            <div className="sticky top-[100px] border border-line bg-ink-3 p-8">
              <AnimatePresence mode="wait">
                {persona ? (
                  <motion.div
                    key={persona.no}
                    initial={{ x: 20, opacity: 0 }}
                    animate={{ x: 0, opacity: 1 }}
                    exit={{ x: -20, opacity: 0, transition: { duration: 0.2 } }}
                    transition={{ duration: 0.35, ease: [0.22, 1, 0.36, 1] }}
                  >
                    <DetailContent persona={persona} />
                  </motion.div>
                ) : (
                  <motion.div
                    key="empty"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0, transition: { duration: 0.2 } }}
                    className="flex min-h-[420px] flex-col items-center justify-center gap-6"
                  >
                    <span className="select-none text-[72px] leading-none text-gold-dim opacity-40" aria-hidden="true">
                      ☰
                    </span>
                    <p className="text-[13px] tracking-[0.2em] text-paper-faint">点一格以观之</p>
                  </motion.div>
                )}
              </AnimatePresence>
            </div>
          </aside>
        </div>
      </div>

      {/* 移动：底部抽屉 sheet */}
      <AnimatePresence>
        {persona ? (
          <motion.div
            key="sheet"
            className="fixed inset-x-0 bottom-0 z-40 max-h-[72dvh] overflow-y-auto border-t border-gold bg-ink-2 px-6 pb-10 pt-4 lg:hidden"
            initial={{ y: '100%' }}
            animate={{ y: 0 }}
            exit={{ y: '100%' }}
            transition={{ duration: 0.35, ease: [0.22, 1, 0.36, 1] }}
            role="dialog"
            aria-label={`人格详情：${persona.full}`}
          >
            <div className="mb-4 flex items-center justify-between">
              <span className="mx-auto h-px w-16 bg-gold-dim" aria-hidden="true" />
              <button
                type="button"
                onClick={() => setSelected(null)}
                className="absolute right-4 top-3 border border-line p-1.5 text-paper-dim transition-colors hover:border-gold hover:text-gold"
                aria-label="关闭详情"
              >
                <X size={16} />
              </button>
            </div>
            <AnimatePresence mode="wait">
              <motion.div
                key={persona.no}
                initial={{ x: 20, opacity: 0 }}
                animate={{ x: 0, opacity: 1 }}
                exit={{ x: -20, opacity: 0, transition: { duration: 0.2 } }}
                transition={{ duration: 0.35, ease: [0.22, 1, 0.36, 1] }}
              >
                <DetailContent persona={persona} />
              </motion.div>
            </AnimatePresence>
          </motion.div>
        ) : null}
      </AnimatePresence>
    </section>
  )
}
