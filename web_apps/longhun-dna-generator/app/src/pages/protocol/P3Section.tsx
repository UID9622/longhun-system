// DNA: #龍芯⚡️丙午·甲申·丁未·亥时·䷎谦-DNA-COMPLETION-fb4b722d
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
import { useEffect, useRef } from 'react'
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'
import { Globe } from 'lucide-react'
import SealTag from '@/components/SealTag'
import { P3_ITEMS } from '@/pages/protocol/data'
import LayerHeader from '@/pages/protocol/LayerHeader'

gsap.registerPlugin(ScrollTrigger)

/**
 * S6 · P3 区域适配（10 项 · 一国一策）
 * 编辑风列表：卡间发线、无包壳 · hover 左金条 scaleY 0→1 + 整行右移 6px
 */
export default function P3Section() {
  const rootRef = useRef<HTMLElement>(null)

  useEffect(() => {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return
    const ctx = gsap.context(() => {
      gsap.fromTo(
        '.p3-row',
        { y: 30, opacity: 0 },
        {
          y: 0,
          opacity: 1,
          duration: 0.55,
          ease: 'cubic-bezier(0.22,1,0.36,1)',
          stagger: 0.08,
          scrollTrigger: { trigger: '.p3-list', start: 'top 75%' },
        },
      )
    }, rootRef)
    return () => ctx.revert()
  }, [])

  return (
    <section
      ref={rootRef}
      id="p3"
      className="hairline-t scroll-mt-[120px] bg-ink-2 py-[72px] md:py-[120px]"
      aria-label="P3 区域适配"
    >
      <div className="mx-auto w-full max-w-container px-6 md:px-12">
        <LayerHeader
          layer="P3"
          title="区域适配 · 一国一策"
          caption="十项适配准则，尊重每一片土地的法律、语言与礼俗。"
        />

        <div className="p3-list mt-12 flex flex-col border-t border-line">
          {P3_ITEMS.map((item) => (
            <div
              key={item.id}
              className="p3-row group relative flex items-center gap-6 border-b border-line px-2 py-6 transition-transform duration-300 hover:translate-x-[6px] md:px-4"
            >
              <span
                aria-hidden="true"
                className="absolute bottom-0 left-0 h-full w-[3px] origin-bottom scale-y-0 bg-gold transition-transform duration-300 group-hover:scale-y-100"
              />
              <SealTag className="shrink-0">{item.id}</SealTag>
              <div className="flex-1">
                <h3 className="font-serif text-[20px] font-bold tracking-[0.04em] text-paper">
                  {item.title}
                </h3>
                <p className="mt-1.5 text-[14px] leading-[1.85] text-paper-dim">{item.gloss}</p>
              </div>
              <Globe size={20} className="shrink-0 text-gold" aria-hidden="true" />
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
