import { useEffect, useRef } from 'react'
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'
import DNACode from '@/components/DNACode'
import OutlineButton from '@/components/OutlineButton'

gsap.registerPlugin(ScrollTrigger)

const CHARTER_DNA = '#龍芯⚡️丙午·甲申·己卯·午时·䷀乾-CHARTER-v1.0-0001-████████'

/**
 * S8 · 签署区（pin 120vh）
 * 背景巨「信」· 滚动进度驱动 16 人格签章点阵自中心向外点亮 · 点满后 H2 金线 scaleX 0→1
 */
export default function SignSection() {
  const rootRef = useRef<HTMLElement>(null)

  useEffect(() => {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return
    const ctx = gsap.context(() => {
      const tl = gsap.timeline({
        scrollTrigger: {
          trigger: rootRef.current,
          start: 'top top',
          end: '+=120%',
          pin: true,
          scrub: 0.6,
        },
      })
      // 按钮 stagger 0.1s 标准入场
      tl.fromTo(
        '.sign-cta',
        { y: 24, opacity: 0 },
        { y: 0, opacity: 1, duration: 0.5, stagger: 0.1, ease: 'cubic-bezier(0.22,1,0.36,1)' },
      )
      // 16 签章点阵自中心向外点亮（4×4，80px 网格）
      tl.fromTo(
        '.sign-dot',
        { backgroundColor: 'rgba(201,162,39,0.14)', scale: 0.75 },
        {
          backgroundColor: '#E9CB6B',
          scale: 1,
          duration: 0.4,
          stagger: { grid: [4, 4], from: 'center', each: 0.12 },
        },
        0.3,
      )
      // 点满后 H2 金色下划线
      tl.fromTo(
        '.sign-underline',
        { scaleX: 0 },
        { scaleX: 1, duration: 0.9, ease: 'none' },
        '-=0.1',
      )
    }, rootRef)
    return () => ctx.revert()
  }, [])

  return (
    <section
      ref={rootRef}
      id="sign"
      className="hairline-t relative flex min-h-[80vh] scroll-mt-[120px] items-center overflow-hidden bg-ink-2"
      aria-label="签署区"
    >
      {/* 顶部巨型「信」字背景（30vh，4% 透明） */}
      <span
        className="pointer-events-none absolute left-1/2 top-8 -translate-x-1/2 select-none font-serif font-black leading-none text-paper opacity-[0.04]"
        style={{ fontSize: '30vh' }}
        aria-hidden="true"
      >
        信
      </span>

      <div className="relative z-10 mx-auto w-full max-w-[880px] px-6 py-24 text-center">
        {/* 16 人格签章点阵（居中大版） */}
        <div
          className="mx-auto grid w-fit grid-cols-4"
          role="img"
          aria-label="十六人格会签点阵，随滚动自中心向外点亮"
        >
          {Array.from({ length: 16 }, (_, i) => (
            <span key={i} className="flex h-14 w-14 items-center justify-center md:h-20 md:w-20">
              <span className="sign-dot h-2 w-2 rounded-full bg-gold-bright md:h-2.5 md:w-2.5" />
            </span>
          ))}
        </div>

        <h2 className="mt-10 inline-block font-serif text-[clamp(30px,4vw,52px)] font-bold leading-[1.15] tracking-[0.05em] text-paper">
          <span className="relative inline-block">
            以人格签章，以 DNA 为证。
            <span
              className="sign-underline absolute -bottom-3 left-0 h-[3px] w-full origin-left bg-gold"
              aria-hidden="true"
            />
          </span>
        </h2>
        <p className="mx-auto mt-8 max-w-[560px] text-[18px] leading-[1.9] text-paper-dim">
          君子协议中英双语全文，一诺既出，天下共鉴。
        </p>

        <div className="mt-10 flex flex-wrap items-center justify-center gap-5">
          <span className="sign-cta inline-block">
            <OutlineButton to="/works#gentleman" variant="solid">
              阅读君子协议
            </OutlineButton>
          </span>
          <span className="sign-cta inline-block">
            <OutlineButton to="/dna#verify" variant="ghost">
              验证一份 DNA
            </OutlineButton>
          </span>
        </div>

        <div className="mx-auto mt-14 max-w-[720px] text-left">
          <DNACode code={CHARTER_DNA} fontSize={13} />
          <p className="mt-3 text-center font-mono text-[11px] tracking-[0.08em] text-paper-faint">
            哈希位以 █ 示意 · 真实哈希以注册表为准
          </p>
        </div>
      </div>
    </section>
  )
}
