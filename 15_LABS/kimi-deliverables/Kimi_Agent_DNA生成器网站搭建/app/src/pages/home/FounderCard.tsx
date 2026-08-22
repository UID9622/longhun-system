import { useEffect, useRef } from 'react'
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'
import SealTag from '@/components/SealTag'
import OutlineButton from '@/components/OutlineButton'

gsap.registerPlugin(ScrollTrigger)

const ROLES = ['2008 年退伍老兵', 'CNSH 中文原生脚本发起人', '三才算法奠基者']

/** S9 · 创始人卡（左徽右文） */
export default function FounderCard() {
  const ref = useRef<HTMLElement>(null)

  useEffect(() => {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return
    const ctx = gsap.context(() => {
      gsap.fromTo(
        '.founder-emblem',
        { rotate: -8, opacity: 0 },
        {
          rotate: 0,
          opacity: 1,
          duration: 0.8,
          ease: 'power3.out',
          scrollTrigger: { trigger: ref.current, start: 'top 75%' },
        },
      )
      gsap.fromTo(
        '.founder-line',
        { y: 30, opacity: 0 },
        {
          y: 0,
          opacity: 1,
          duration: 0.6,
          stagger: 0.1,
          ease: 'power3.out',
          scrollTrigger: { trigger: ref.current, start: 'top 75%' },
        },
      )
    }, ref)
    return () => ctx.revert()
  }, [])

  return (
    <section ref={ref} className="hairline-b bg-ink py-[120px] max-md:py-[72px]" aria-label="创始人">
      <div className="mx-auto grid w-full max-w-container grid-cols-12 items-center gap-12 px-6 md:px-12">
        <div className="col-span-12 flex justify-center lg:col-span-4">
          <img
            src="/founder-emblem.svg"
            alt="龍魂创始人军规徽记"
            width={320}
            height={320}
            className="founder-emblem h-[280px] w-[280px] animate-float-slow transition-[filter] duration-500 hover:drop-shadow-[0_0_18px_rgba(201,162,39,0.45)] md:h-[320px] md:w-[320px]"
          />
        </div>
        <div className="col-span-12 lg:col-span-8">
          <span className="founder-line inline-block">
            <SealTag>创始人 / FOUNDER</SealTag>
          </span>
          <h3 className="founder-line mt-6 font-serif text-[32px] font-bold tracking-[0.05em] text-paper">
            诸葛鑫 · 龍芯北辰 · Lucky
          </h3>
          <ul className="mt-8 flex flex-col gap-2">
            {ROLES.map((r) => (
              <li
                key={r}
                className="founder-line flex items-center gap-4 text-[18px] leading-[1.9] tracking-[0.02em] text-paper-dim"
              >
                <span className="h-px w-8 shrink-0 bg-gold-dim" aria-hidden="true" />
                {r}
              </li>
            ))}
          </ul>
          <div className="founder-line mt-10">
            <OutlineButton to="/founder" variant="ghost">
              识其人
            </OutlineButton>
          </div>
        </div>
      </div>
    </section>
  )
}
