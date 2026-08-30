// DNA: #龍芯⚡️丙午·甲申·丁未·亥时·䷎谦-DNA-COMPLETION-4821cbeb
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
import { useEffect, useRef, useState } from 'react'
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'
import SealTag from '@/components/SealTag'
import OutlineButton from '@/components/OutlineButton'

gsap.registerPlugin(ScrollTrigger)

/**
 * S6 · 唯一性数学（收尾，约 50vh）
 * 居中排版孤岛：公式 60日柱 × 12时辰 × 64卦 = 46,080 组合/天（数字 1.2s 递增计数定格），
 * 孤岛四边绘制（0.6s，30% 视口触发），SealTag ×3 + ghost 按钮 → /works。
 */
export default function UniquenessMath() {
  const rootRef = useRef<HTMLElement>(null)
  const [count, setCount] = useState(0)

  useEffect(() => {
    const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches
    const counter = { v: 0 }
    const ctx = gsap.context(() => {
      ScrollTrigger.create({
        trigger: rootRef.current,
        start: 'top 30%',
        once: true,
        onEnter: () => {
          // 孤岛四边绘制（0.6s）
          gsap.fromTo('.math-edge-t', { scaleX: 0 }, { scaleX: 1, duration: reduced ? 0.001 : 0.15, ease: 'linear' })
          gsap.fromTo('.math-edge-r', { scaleY: 0 }, { scaleY: 1, duration: reduced ? 0.001 : 0.15, ease: 'linear', delay: reduced ? 0 : 0.15 })
          gsap.fromTo('.math-edge-b', { scaleX: 0 }, { scaleX: 1, duration: reduced ? 0.001 : 0.15, ease: 'linear', delay: reduced ? 0 : 0.3 })
          gsap.fromTo('.math-edge-l', { scaleY: 0 }, { scaleY: 1, duration: reduced ? 0.001 : 0.15, ease: 'linear', delay: reduced ? 0 : 0.45 })
          // 乘法式逐段淡入
          gsap.fromTo(
            '.math-part',
            { opacity: 0, y: 12 },
            { opacity: 1, y: 0, duration: reduced ? 0.001 : 0.4, stagger: 0.12, ease: 'power3.out', delay: reduced ? 0 : 0.4 },
          )
          // 46,080 递增计数（1.2s）后定格
          if (reduced) {
            setCount(46080)
          } else {
            gsap.to(counter, {
              v: 46080,
              duration: 1.2,
              delay: 0.6,
              ease: 'power2.out',
              onUpdate: () => setCount(Math.round(counter.v)),
            })
          }
          gsap.fromTo(
            '.math-rest',
            { opacity: 0, y: 16 },
            { opacity: 1, y: 0, duration: reduced ? 0.001 : 0.5, stagger: 0.12, ease: 'power3.out', delay: reduced ? 0 : 1.0 },
          )
        },
      })
    }, rootRef)
    return () => ctx.revert()
  }, [])

  return (
    <section
      ref={rootRef}
      className="hairline-t flex min-h-[50vh] items-center"
      aria-label="唯一性数学"
    >
      <div className="mx-auto w-full max-w-container px-6 py-[72px] md:px-12 md:py-[120px]">
        <div className="relative mx-auto max-w-[880px] bg-ink px-6 py-14 text-center md:px-16 md:py-20">
          {/* 孤岛四边金线 */}
          <span aria-hidden="true" className="math-edge-t absolute left-0 top-0 h-px w-full origin-left bg-line-strong" />
          <span aria-hidden="true" className="math-edge-r absolute right-0 top-0 h-full w-px origin-top bg-line-strong" />
          <span aria-hidden="true" className="math-edge-b absolute bottom-0 right-0 h-px w-full origin-right bg-line-strong" />
          <span aria-hidden="true" className="math-edge-l absolute bottom-0 left-0 h-full w-px origin-bottom bg-line-strong" />

          <h2 className="font-serif text-[clamp(30px,4vw,52px)] font-bold leading-[1.15] tracking-[0.05em] text-paper">
            为什么它永不重复
          </h2>

          {/* 公式 */}
          <p className="mt-10 font-mono text-[clamp(15px,2.4vw,20px)] tracking-[0.04em] text-gold">
            <span className="math-part opacity-0">60日柱</span>
            <span className="math-part opacity-0"> × </span>
            <span className="math-part opacity-0">12时辰</span>
            <span className="math-part opacity-0"> × </span>
            <span className="math-part opacity-0">64卦</span>
            <span className="math-part opacity-0"> = </span>
            <span className="math-part tabular-nums text-gold-bright opacity-0">
              {count.toLocaleString('en-US')}
            </span>
            <span className="math-part opacity-0"> 组合/天</span>
          </p>

          <p className="math-rest mx-auto mt-8 max-w-[560px] text-[18px] leading-[1.9] tracking-[0.02em] text-paper-dim opacity-0">
            再叠加两道唯一锚——当日单调递增序号与内容哈希 8 位。同一天内序号唯一，DNA
            即全局唯一；跨天日柱不同，天然不同。
          </p>

          <div className="math-rest mt-8 flex flex-wrap items-center justify-center gap-3 opacity-0">
            <SealTag>日序号锚</SealTag>
            <SealTag>SM3/SHA-256 哈希锚</SealTag>
            <SealTag>注册表持久化</SealTag>
          </div>

          <div className="math-rest mt-10 opacity-0">
            <OutlineButton variant="ghost" to="/works" ariaLabel="前往作品库看实战">
              前往作品库看实战
            </OutlineButton>
          </div>
        </div>
      </div>
    </section>
  )
}
