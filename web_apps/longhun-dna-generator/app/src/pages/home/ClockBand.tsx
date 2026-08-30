// DNA: #龍芯⚡️丙午·甲申·丁未·亥时·䷎谦-DNA-COMPLETION-0f3e227d
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
import { useEffect, useRef } from 'react'
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'
import GanzhiClock from '@/components/GanzhiClock'

gsap.registerPlugin(ScrollTrigger)

/** S2 · 实时干支时钟带（全宽横带） */
export default function ClockBand() {
  const ref = useRef<HTMLElement>(null)

  useEffect(() => {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return
    const ctx = gsap.context(() => {
      gsap.fromTo(
        '.clock-cell',
        { y: 30, opacity: 0 },
        {
          y: 0,
          opacity: 1,
          duration: 0.6,
          ease: 'power3.out',
          stagger: 0.1,
          scrollTrigger: { trigger: ref.current, start: 'top 75%' },
        },
      )
    }, ref)
    return () => ctx.revert()
  }, [])

  return (
    <section ref={ref} className="hairline-t hairline-b bg-ink-2 py-16" aria-label="实时干支时钟">
      <div className="mx-auto w-full max-w-container px-6 md:px-12">
        <GanzhiClock variant="full" />
      </div>
    </section>
  )
}
