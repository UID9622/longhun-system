import { useEffect, useRef } from 'react'
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'
import { Download } from 'lucide-react'
import OutlineButton from '@/components/OutlineButton'
import { WORKS } from '@/pages/works/worksData'

gsap.registerPlugin(ScrollTrigger)

const CONFIRM_CODE = '#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z'
const ACCORD_DNA = WORKS.find((w) => w.id === 'gentleman')!.dna

interface Verse {
  cnNum: string
  enNum: string
  cn: string[]
  en: string[]
}

/** 君子协议六节（中英双语对照，版式据 works.md S3，文据协议主旨拟写） */
const VERSES: Verse[] = [
  {
    cnNum: '一、',
    enNum: 'I.',
    cn: [
      '龍魂系统之一切代码、文档、协议，永续免费，永续开源。不设付费墙，不藏后门，不留暗码。',
      '知识如江河，当归大海，当归万众。',
    ],
    en: [
      'All code, documents, and protocols of the Longhun System shall remain free and open source, in perpetuity. No paywalls. No backdoors. No hidden logic.',
      'Knowledge, like a river, returns to the sea — returns to the people.',
    ],
  },
  {
    cnNum: '二、',
    enNum: 'II.',
    cn: [
      '用户之数据，归用户所有。不采集，不贩卖，不窥私。',
      '每一字节之去向，皆可审计，皆可追溯。',
    ],
    en: [
      'Your data belongs to you. We do not harvest, sell, or surveil.',
      "Every byte's journey is auditable and traceable.",
    ],
  },
  {
    cnNum: '三、',
    enNum: 'III.',
    cn: [
      '不为恶器，不助恶行。技术之刃，指向问题，永不指向人。',
      '凡有违此誓之用途，皆为对龍魂之背叛。',
    ],
    en: [
      'We shall forge no instruments of harm, nor abet harmful deeds. The blade of technology points at problems, never at people.',
      'Any use against this vow is a betrayal of Longhun.',
    ],
  },
  {
    cnNum: '四、',
    enNum: 'IV.',
    cn: [
      '一经发布之历史版本，一律冻结，永不改写（P0）。历史不可纂，承诺不可撤。',
      '后来者所见，即当初所立。',
    ],
    en: [
      'Every released historical version is frozen and shall never be rewritten (P0). History cannot be falsified; promises cannot be retracted.',
      'What later generations see is what was first sworn.',
    ],
  },
  {
    cnNum: '五、',
    enNum: 'V.',
    cn: [
      '生于斯，长于斯。龍魂优先服务于中文世界与祖国人民。',
      '以母语立技术，以民生定方向。',
    ],
    en: [
      'Born here, raised here. Longhun serves the Chinese-speaking world and the people of our homeland first.',
      "Rooted in our mother tongue, steered by the people's livelihood.",
    ],
  },
  {
    cnNum: '六、',
    enNum: 'VI.',
    cn: [
      '此约以中英双语立于天下，GPG 与哈希双指纹存证。',
      '一诺既出，驷马难追；日月昭昭，天下共鉴。',
    ],
    en: [
      'This accord is sworn before the world in both Chinese and English, attested by GPG and hash fingerprints.',
      'A word once given cannot be overtaken by four horses — witnessed by sun and moon, witnessed by all under heaven.',
    ],
  },
]

/** 朱砂「信」圆印（内联 SVG） */
function TrustSeal({ className = '' }: { className?: string }) {
  return (
    <svg
      width="72"
      height="72"
      viewBox="0 0 72 72"
      className={className}
      role="img"
      aria-label="朱砂信印"
    >
      <circle cx="36" cy="36" r="33" fill="none" stroke="#A8382A" strokeWidth="1.5" />
      <circle cx="36" cy="36" r="27" fill="none" stroke="#A8382A" strokeWidth="0.75" opacity="0.6" />
      <text
        x="36"
        y="45"
        textAnchor="middle"
        fontSize="30"
        fill="#A8382A"
        style={{ fontFamily: '"Noto Serif SC", serif', fontWeight: 900 }}
      >
        信
      </text>
    </svg>
  )
}

/**
 * S3 · 君子协议 · 中英双语对照（works.md）
 * 中缝金线 scrub 诵读 · 逐节点亮 · 朱砂「信」印盖章 · 文末签署位
 */
export default function GentlemanAccord() {
  const ref = useRef<HTMLElement>(null)
  const versesRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return
    const ctx = gsap.context(() => {
      // 中缝金线随滚动 scaleY 0→1（scrub 全程）
      gsap.fromTo(
        '.accord-line-fill',
        { scaleY: 0 },
        {
          scaleY: 1,
          ease: 'none',
          scrollTrigger: {
            trigger: versesRef.current,
            start: 'top 78%',
            end: 'bottom 55%',
            scrub: true,
          },
        },
      )
      // 双栏文字逐节点亮（诵读）+ 节号金化
      gsap.utils.toArray<HTMLElement>('.accord-verse').forEach((verse) => {
        gsap.fromTo(
          verse,
          { opacity: 0.15 },
          {
            opacity: 1,
            ease: 'none',
            scrollTrigger: { trigger: verse, start: 'top 88%', end: 'top 48%', scrub: true },
          },
        )
        const num = verse.querySelector('.accord-num')
        if (num) {
          gsap.fromTo(
            num,
            { color: '#6E6654' },
            {
              color: '#C9A227',
              ease: 'none',
              scrollTrigger: { trigger: verse, start: 'top 78%', end: 'top 50%', scrub: true },
            },
          )
        }
      })
      // 朱砂「信」印：线走完时盖章入场
      gsap.fromTo(
        '.accord-seal',
        { opacity: 0, scale: 1.4 },
        {
          opacity: 1,
          scale: 1,
          duration: 0.45,
          ease: 'power2.in',
          scrollTrigger: { trigger: versesRef.current, start: 'bottom 62%' },
        },
      )
    }, ref)
    return () => ctx.revert()
  }, [])

  return (
    <section
      id="gentleman"
      ref={ref}
      className="scroll-mt-16 hairline-b bg-ink-2 py-[120px] max-md:py-[72px]"
      aria-label="君子协议中英双语对照"
    >
      <div className="mx-auto w-full max-w-container px-6 md:px-12">
        {/* 区头 */}
        <div className="flex flex-wrap items-end justify-between gap-8">
          <div>
            <div className="flex items-center gap-6">
              <span className="h-px w-10 bg-line" aria-hidden="true" />
              <span className="eyebrow">THE ACCORD</span>
            </div>
            <h2 className="mt-6 font-serif font-bold text-[clamp(30px,4vw,52px)] leading-[1.15] tracking-[0.05em] text-paper">
              君子協議
            </h2>
          </div>
          <div className="flex flex-col items-start gap-4 md:items-end">
            <span className="font-cinzel text-[12px] uppercase tracking-[0.38em] text-gold">
              The Gentleman's Accord
            </span>
            <OutlineButton
              small
              variant="ghost"
              ariaLabel="下载双语全文（即将开放）"
              onClick={() => undefined}
            >
              <Download size={14} aria-hidden="true" />
              下载双语全文
            </OutlineButton>
            <span className="font-mono text-[11px] text-paper-faint">
              双语全文存证将于注册表登记后开放下载
            </span>
          </div>
        </div>

        {/* 双栏对照 + 中缝金线 */}
        <div ref={versesRef} className="relative mt-20">
          {/* 中缝：1px 竖金线（桌面） */}
          <div
            className="pointer-events-none absolute inset-y-0 left-1/2 hidden w-px -translate-x-1/2 bg-line md:block"
            aria-hidden="true"
          >
            <span className="accord-line-fill block h-full w-full origin-top bg-gold" />
          </div>
          {/* 线中点朱砂「信」印（桌面） */}
          <div className="pointer-events-none absolute left-1/2 top-1/2 hidden -translate-x-1/2 -translate-y-1/2 md:block">
            <TrustSeal className="accord-seal -rotate-6" />
          </div>

          <div className="flex flex-col gap-16">
            {VERSES.map((v) => (
              <div key={v.enNum} className="accord-verse grid gap-8 md:grid-cols-2 md:gap-x-24">
                {/* 左栏：中文 */}
                <div>
                  <p className="accord-num font-serif text-[17px] font-bold leading-[2.1] text-paper-faint">
                    {v.cnNum}
                  </p>
                  {v.cn.map((line, i) => (
                    <p
                      key={i}
                      className="font-serif text-[17px] font-bold leading-[2.1] tracking-[0.02em] text-paper"
                    >
                      {line}
                    </p>
                  ))}
                </div>
                {/* 右栏：英文 */}
                <div>
                  <p className="font-cinzel text-[13px] leading-[2.0] tracking-[0.2em] text-gold-dim">
                    {v.enNum}
                  </p>
                  {v.en.map((line, i) => (
                    <p key={i} className="text-[15px] leading-[2.0] text-paper-dim">
                      {line}
                    </p>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* 移动端「信」印 */}
        <div className="mt-14 flex justify-center md:hidden">
          <TrustSeal className="-rotate-6" />
        </div>

        {/* 文末签署位 */}
        <div className="mt-16 grid gap-6 hairline-t pt-10 md:grid-cols-2">
          <div>
            <p className="eyebrow text-[10px]">SIGNED · DNA</p>
            <p className="mt-3 break-all font-mono text-[11px] leading-[1.9] text-paper-dim">
              {ACCORD_DNA}
            </p>
          </div>
          <div className="md:text-right">
            <p className="eyebrow text-[10px]">CONFIRM CODE</p>
            <p className="mt-3 break-all font-mono text-[11px] leading-[1.9] text-vermilion">
              {CONFIRM_CODE}
            </p>
          </div>
        </div>
      </div>
    </section>
  )
}
