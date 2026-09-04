// DNA: #龍芯⚡️丙午·甲申·丁未·亥时·䷎谦-DNA-COMPLETION-daf011fb
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
import { useEffect, useMemo, useRef, useState } from 'react'
import { motion, useInView } from 'framer-motion'
import SectionHeading from '@/components/SectionHeading'
import OutlineButton from '@/components/OutlineButton'
import { getGanzhi } from '@/lib/ganzhi'

/** H2 词级切分 */
const TITLE_WORDS = ['名可考，', '言可验，', '码可审。']

/** S6 · 回响 CTA（founder.md S6）—— 实时 DNA 彩蛋 · 纯 Framer Motion 域 */
export default function FounderCTA() {
  const ref = useRef<HTMLElement>(null)
  const inView = useInView(ref, { once: true, amount: 0.4 })

  // 实时四柱 + 当下卦（GanzhiClock 同源算法）
  const dnaLine = useMemo(() => {
    const g = getGanzhi()
    return `#龍芯⚡️${g.year}·${g.month}·${g.day}·${g.hour}·${g.hexagramSymbol}${g.hexagramFullName}-FOUNDER-PAGE-v1.0-████-████████`
  }, [])

  // 打字机 15ms/字（入场触发）；reduced-motion 直接呈现终态
  const reduced = useMemo(
    () => window.matchMedia('(prefers-reduced-motion: reduce)').matches,
    [],
  )
  const [typed, setTyped] = useState(() => (reduced ? dnaLine.length : 0))
  useEffect(() => {
    if (!inView || reduced) return
    const t = window.setInterval(() => {
      setTyped((n) => {
        if (n >= dnaLine.length) {
          window.clearInterval(t)
          return n
        }
        return n + 1
      })
    }, 15)
    return () => window.clearInterval(t)
  }, [inView, reduced, dnaLine])

  const done = typed >= dnaLine.length

  return (
    <section ref={ref} className="bg-ink py-[120px] max-md:py-[72px]" aria-label="回响">
      <div className="mx-auto w-full max-w-container px-6 md:px-12">
        <div className="relative mx-auto max-w-[880px] px-8 py-16 text-center md:px-16 md:py-20">
          {/* 孤岛四边绘制（0.6s） */}
          <motion.span
            className="absolute left-0 top-0 h-px w-full origin-left bg-line-strong"
            initial={{ scaleX: 0 }}
            animate={inView ? { scaleX: 1 } : { scaleX: 0 }}
            transition={{ duration: 0.6, ease: 'linear' }}
            aria-hidden="true"
          />
          <motion.span
            className="absolute right-0 top-0 h-full w-px origin-top bg-line-strong"
            initial={{ scaleY: 0 }}
            animate={inView ? { scaleY: 1 } : { scaleY: 0 }}
            transition={{ duration: 0.6, delay: 0.1, ease: 'linear' }}
            aria-hidden="true"
          />
          <motion.span
            className="absolute bottom-0 right-0 h-px w-full origin-right bg-line-strong"
            initial={{ scaleX: 0 }}
            animate={inView ? { scaleX: 1 } : { scaleX: 0 }}
            transition={{ duration: 0.6, delay: 0.2, ease: 'linear' }}
            aria-hidden="true"
          />
          <motion.span
            className="absolute bottom-0 left-0 h-full w-px origin-bottom bg-line-strong"
            initial={{ scaleY: 0 }}
            animate={inView ? { scaleY: 1 } : { scaleY: 0 }}
            transition={{ duration: 0.6, delay: 0.3, ease: 'linear' }}
            aria-hidden="true"
          />
          <div className="absolute inset-0 bg-ink" style={{ zIndex: -1 }} aria-hidden="true" />

          <SectionHeading
            align="center"
            eyebrow="THE ECHO"
            title={
              <span aria-label="名可考，言可验，码可审。">
                {TITLE_WORDS.map((w, i) => (
                  <motion.span
                    key={w}
                    className="inline-block"
                    aria-hidden="true"
                    initial={{ y: 24, opacity: 0 }}
                    animate={inView ? { y: 0, opacity: 1 } : { y: 24, opacity: 0 }}
                    transition={{ duration: 0.5, delay: 0.2 + i * 0.1, ease: [0.22, 1, 0.36, 1] }}
                  >
                    {w}
                  </motion.span>
                ))}
              </span>
            }
            subtitle="这是一个老兵交给开源世界的全部。"
          />

          <div className="mt-12 flex flex-col items-center justify-center gap-5 sm:flex-row">
            <OutlineButton variant="solid" to="/dna">
              铸造你的 DNA
            </OutlineButton>
            <OutlineButton variant="ghost" to="/timeline">
              重走远征路
            </OutlineButton>
          </div>

          {/* 实时 DNA 彩蛋行（打字机） */}
          <p
            className="mt-14 break-all font-mono text-[11px] leading-[1.9] tracking-[0.04em] text-paper-faint"
            aria-label={dnaLine}
          >
            <span aria-hidden="true">{dnaLine.slice(0, typed)}</span>
            {!done ? <span className="animate-caret-blink text-gold" aria-hidden="true">▌</span> : null}
          </p>
        </div>
      </div>
    </section>
  )
}
