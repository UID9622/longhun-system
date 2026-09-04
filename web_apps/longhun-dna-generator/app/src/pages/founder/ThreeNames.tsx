import { useRef } from 'react'
import { motion, useInView } from 'framer-motion'
import PersonaSeal from '@/pages/matrix/PersonaSeal'

const NAMES = [
  {
    seal: '鑫',
    name: '诸葛鑫',
    role: '本名 · 法律与责任之名',
    line: '签署协议、承担责任时，用此名。',
  },
  {
    seal: '辰',
    name: '龍芯北辰',
    role: '号 · 技术与远征之名',
    line: '写代码、铸 DNA 时，用此号。',
  },
  {
    seal: 'L',
    name: 'Lucky',
    role: '名 · 开源世界之名',
    line: '与全球开发者同行时，用此名。',
  },
]

/** S2 · 三个名字（founder.md S2）—— 纯 Framer Motion 域 */
export default function ThreeNames() {
  const ref = useRef<HTMLElement>(null)
  const inView = useInView(ref, { once: true, amount: 0.3 })

  return (
    <section ref={ref} className="hairline-b bg-ink py-[120px] max-md:py-[72px]" aria-label="三个名字">
      <div className="mx-auto w-full max-w-container px-6 md:px-12">
        <p className="text-center text-[13px] tracking-[0.2em] text-paper-dim">一人三名，各有其所。</p>

        <div className="mt-14 grid grid-cols-1 gap-6 md:grid-cols-3">
          {NAMES.map((n, i) => (
            <motion.div
              key={n.name}
              initial={{ y: 40, opacity: 0 }}
              animate={inView ? { y: 0, opacity: 1 } : { y: 40, opacity: 0 }}
              transition={{ duration: 0.6, delay: i * 0.12, ease: [0.22, 1, 0.36, 1] }}
              className="group relative border border-line bg-ink-3 px-8 py-10 transition-colors duration-300 hover:border-gold"
            >
              {/* 顶部 2px 金条（hover 顶入） */}
              <span
                className="absolute left-0 top-0 h-[2px] w-full origin-left scale-x-0 bg-gold transition-transform duration-300 group-hover:scale-x-100"
                aria-hidden="true"
              />
              {/* 名章：盖章式 scale 1.5→1 延迟入场；hover 回正 */}
              <motion.div
                initial={{ scale: 1.5, opacity: 0 }}
                animate={inView ? { scale: 1, opacity: 1 } : { scale: 1.5, opacity: 0 }}
                transition={{ duration: 0.4, delay: 0.3 + i * 0.12, ease: [0.22, 1, 0.36, 1] }}
              >
                <div className="-rotate-6 transition-transform duration-300 group-hover:rotate-0">
                  <PersonaSeal char={n.seal} size={40} tone="vermilion" />
                </div>
              </motion.div>
              <h3 className="mt-6 font-serif text-[28px] font-bold tracking-[0.08em] text-paper">
                {n.name}
              </h3>
              <p className="mt-3 font-mono text-[12px] tracking-[0.16em] text-gold-dim">{n.role}</p>
              <p className="mt-5 text-[15px] leading-[1.9] text-paper-dim">{n.line}</p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  )
}
