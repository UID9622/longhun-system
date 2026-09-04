// DNA: #龍芯⚡️丙午·甲申·丁未·亥时·䷎谦-DNA-COMPLETION-58c94e0d
import { useEffect, useRef } from 'react'
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'
import SealTag from '@/components/SealTag'

gsap.registerPlugin(ScrollTrigger)

const PARAGRAPHS = [
  '2008 年退伍——服役 2 年，退伍 18 年。队列、纪律、口令，成为此后一切系统设计的骨相。军营教给他的第一件事不是如何进攻，而是如何守住：守住队列的笔直，守住命令的准确，守住身后的人。',
  '从焊死的 P0 到发丝般的 1px 金边，军事的秩序感被翻译成了协议的秩序感。条令即代码，哨位即服务，口令即签名——每一层协议，都是一次操练。',
  '「退伍不褪色」——只是战场换成了数据主权的战场，守卫的对象换成了人民。枪已入库，但哨位仍在；这一回，他站在代码的哨位上。',
]

const TAGS = ['纪律', '焊死', '守卫']

/** 微型五角星 SVG（金） */
function GoldStar({ size = 22, className = '' }: { size?: number; className?: string }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" className={className} aria-hidden="true">
      <path
        d="M12 2 L14.6 8.6 L21.6 9.1 L16.3 13.7 L17.9 20.6 L12 16.9 L6.1 20.6 L7.7 13.7 L2.4 9.1 L9.4 8.6 Z"
        fill="none"
        stroke="var(--gold)"
        strokeWidth="1.2"
        strokeLinejoin="round"
      />
    </svg>
  )
}

/**
 * S3 · 老兵章（founder.md S3）—— pin 120vh 叙事段
 * 三段叙事随滚动逐段点亮 · 「兵」字背景视差 · 五角星弹入
 * 纯 GSAP 域
 */
export default function VeteranSection() {
  const ref = useRef<HTMLElement>(null)

  useEffect(() => {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return
    const ctx = gsap.context(() => {
      // pin 120vh：三段叙事逐段点亮（scrub）
      const tl = gsap.timeline({
        scrollTrigger: {
          trigger: ref.current,
          start: 'top top',
          end: '+=120%',
          pin: true,
          scrub: 0.6,
          anticipatePin: 1,
        },
      })
      const paras = Array.from(
        ref.current?.querySelectorAll<HTMLElement>('.veteran-para') ?? [],
      )
      paras.forEach((p, i) => {
        tl.fromTo(p, { opacity: 0.15 }, { opacity: 1, duration: 0.28, ease: 'none' }, i * 0.3)
      })
      // 「兵」字背景视差 y: 50→-50
      tl.fromTo('.veteran-bing', { y: 50 }, { y: -50, duration: 1, ease: 'none' }, 0)
      // 五角星 pin 起点弹入
      gsap.fromTo(
        '.veteran-star',
        { scale: 0, rotate: -72 },
        {
          scale: 1,
          rotate: 0,
          duration: 0.6,
          ease: 'back.out(2)',
          scrollTrigger: { trigger: ref.current, start: 'top 70%' },
        },
      )
    }, ref)
    return () => ctx.revert()
  }, [])

  return (
    <section
      ref={ref}
      className="hairline-b relative flex min-h-[100dvh] items-center overflow-hidden bg-ink-2 py-[120px] max-md:py-[72px]"
      aria-label="老兵章"
    >
      {/* 右缘 1px 竖金线 + 顶部五角星 */}
      <div className="pointer-events-none absolute bottom-[12%] right-6 top-[12%] w-px bg-line md:right-12" aria-hidden="true" />
      <div className="veteran-star absolute right-[15px] top-[10%] md:right-[41px]">
        <GoldStar />
      </div>

      <div className="mx-auto grid w-full max-w-container grid-cols-12 gap-8 px-6 md:px-12">
        {/* 左 5 列：竖排大字「兵」+ SERVED · 2008 */}
        <div className="relative col-span-12 flex items-center justify-center gap-6 lg:col-span-5">
          <span
            className="veteran-bing select-none font-serif font-black leading-none text-gold opacity-[0.05]"
            style={{ fontSize: '36vh' }}
            aria-hidden="true"
          >
            兵
          </span>
          <span className="writing-vertical select-none font-cinzel text-[13px] font-semibold tracking-[0.4em] text-gold-dim" aria-hidden="true">
            SERVED · 2YRS · 2008
          </span>
        </div>

        {/* 右 7 列：叙事 */}
        <div className="col-span-12 lg:col-span-7">
          <span className="eyebrow">THE VETERAN</span>
          <h2 className="mt-6 font-serif text-[clamp(30px,4vw,52px)] font-bold leading-[1.15] tracking-[0.05em] text-paper">
            从军营到代码
          </h2>
          <div className="mt-10 flex max-w-prose flex-col gap-8">
            {PARAGRAPHS.map((p, i) => (
              <p key={i} className="veteran-para text-[18px] leading-[2.0] tracking-[0.02em] text-paper-dim opacity-[0.15]">
                {p}
              </p>
            ))}
          </div>
          <div className="mt-12 flex flex-wrap gap-4">
            {TAGS.map((t) => (
              <SealTag key={t}>{t}</SealTag>
            ))}
          </div>
        </div>
      </div>
    </section>
  )
}
