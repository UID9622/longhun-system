// DNA: #龍芯⚡️丙午·甲申·丁未·亥时·䷎谦-DNA-COMPLETION-215548c2
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
import { useEffect, useRef } from 'react'
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'
import SectionHeading from '@/components/SectionHeading'

gsap.registerPlugin(ScrollTrigger)

const NOTS = [
  { no: 'NO.1', title: '不做专利', desc: '不筑墙、不设卡。思想与方法属于所有人，任何组织都可自由取用。' },
  { no: 'NO.2', title: '不做企业', desc: '不注册公司、不设层级。系统以协议自治，而非以科层治人。' },
  { no: 'NO.3', title: '不走资本', desc: '不融资、不估值、不上市。拒绝让人民的系统沦为资本的筹码。' },
]

const FORS = [
  { no: 'FOR.1', title: '为人民服务', desc: '免费、可用、可依赖。一切设计的终点，是普通人的生活是否因此好一点。' },
  { no: 'FOR.2', title: '为开源存续', desc: '免费开源，代码全量公开。让系统即使失去创始人，也能在人民手中延续。' },
  { no: 'FOR.3', title: '为数据主权', desc: '数据主权在民。你的数据归你支配，系统只有守卫之责，没有占有之权。' },
]

/** S4 · 原则柱：三不 · 三为（founder.md S4）—— 纯 GSAP 域 */
export default function Principles() {
  const ref = useRef<HTMLElement>(null)

  useEffect(() => {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return
    const ctx = gsap.context(() => {
      // 上排 x:-40→0 / 下排 x:40→0 对向入场
      gsap.fromTo(
        '.principle-not',
        { x: -40, opacity: 0 },
        {
          x: 0,
          opacity: 1,
          duration: 0.6,
          ease: 'power2.out',
          stagger: 0.08,
          scrollTrigger: { trigger: '.principle-grid', start: 'top 80%' },
        },
      )
      gsap.fromTo(
        '.principle-for',
        { x: 40, opacity: 0 },
        {
          x: 0,
          opacity: 1,
          duration: 0.6,
          ease: 'power2.out',
          stagger: 0.08,
          scrollTrigger: { trigger: '.principle-grid', start: 'top 80%' },
        },
      )
    }, ref)
    return () => ctx.revert()
  }, [])

  return (
    <section ref={ref} className="hairline-b bg-ink py-[120px] max-md:py-[72px]" aria-label="三不三为">
      <div className="mx-auto w-full max-w-container px-6 md:px-12">
        <SectionHeading
          eyebrow="PRINCIPLES"
          title="三不 · 三为"
          subtitle="三条「不做」焊死边界，三条「为了」锚定方向。此六条与全站 P0 底座同源，终身不更。"
        />

        <div className="principle-grid mt-16 flex flex-col gap-6">
          {/* 上排：三不（朱砂序号） */}
          <div className="grid grid-cols-1 gap-6 md:grid-cols-3">
            {NOTS.map((c) => (
              <div
                key={c.no}
                className="principle-not group border border-line bg-ink-3 px-8 py-8 transition-all duration-300 hover:-translate-y-[3px] hover:border-gold"
              >
                <span className="font-mono text-[13px] tracking-[0.24em] text-vermilion transition-[text-shadow] duration-300 group-hover:[text-shadow:0_0_12px_rgba(168,56,42,0.6)]">
                  {c.no}
                </span>
                <h3 className="mt-4 font-serif text-[22px] font-bold tracking-[0.06em] text-paper">{c.title}</h3>
                <p className="mt-4 text-[14px] leading-[1.9] text-paper-dim">{c.desc}</p>
              </div>
            ))}
          </div>
          {/* 下排：三为（金序号） */}
          <div className="grid grid-cols-1 gap-6 md:grid-cols-3">
            {FORS.map((c) => (
              <div
                key={c.no}
                className="principle-for group border border-line bg-ink-3 px-8 py-8 transition-all duration-300 hover:-translate-y-[3px] hover:border-gold"
              >
                <span className="font-mono text-[13px] tracking-[0.24em] text-gold transition-[text-shadow] duration-300 group-hover:[text-shadow:0_0_12px_rgba(201,162,39,0.6)]">
                  {c.no}
                </span>
                <h3 className="mt-4 font-serif text-[22px] font-bold tracking-[0.06em] text-paper">{c.title}</h3>
                <p className="mt-4 text-[14px] leading-[1.9] text-paper-dim">{c.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  )
}
