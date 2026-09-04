import { useEffect, useRef, useState } from 'react'
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'
import SectionHeading from '@/components/SectionHeading'
import { HEXAGRAM_NAMES, hexagramSymbol } from '@/lib/ganzhi'

gsap.registerPlugin(ScrollTrigger)

/**
 * S5 · 干支算法白皮书 + 64 卦王弼序全表
 * 四张算法卡（左卡名 / 右代码块，行号 paper-faint；干支字符金、注释 paper-faint）。
 * 64 卦 8×8 网格：入场按王弼序波浪点亮（每格 0.015s），此后每 3s 随机一格呼吸。
 */

interface AlgoCard {
  name: string
  code: string[]
}

const CARDS: AlgoCard[] = [
  {
    name: '年柱',
    code: [
      '// 立春近似 = 公历年',
      'const stem   = (year - 4) % 10  // 甲乙丙丁戊己庚辛壬癸',
      'const branch = (year - 4) % 12  // 子丑寅卯辰巳午未申酉戌亥',
    ],
  },
  {
    name: '月柱 · 五虎遁',
    code: [
      '// 甲己之年丙作首，乙庚之岁戊为头',
      '// 丙辛必定寻庚起，丁壬壬位顺行流',
      '// 戊癸何方发，甲寅之上好追求 · 正月建寅',
      'const monthStem   = (yearStem * 2 + month) % 10',
      'const monthBranch = month % 12  // 2月→寅 … 12月→子',
    ],
  },
  {
    name: '日柱 · 儒略日',
    code: [
      '// 锚点校验：2000-01-01 = 戊午',
      'const jdn = julianDayNumber(y, m, d)',
      'const idx = (jdn + 49) % 60  // → 六十甲子序号',
    ],
  },
  {
    name: '时辰',
    code: [
      '// 23:00 起子时，两小时一时辰',
      'const shichen = ((hour + 1) >> 1) % 12',
    ],
  },
]

const GANZHI_CHARS = /[甲乙丙丁戊己庚辛壬癸子丑寅卯辰巳午未申酉戌亥]/u

/** 单行代码着色：注释 paper-faint；干支字符金；其余 paper */
function CodeLine({ line }: { line: string }) {
  const commentAt = line.indexOf('//')
  const codePart = commentAt >= 0 ? line.slice(0, commentAt) : line
  const commentPart = commentAt >= 0 ? line.slice(commentAt) : ''
  return (
    <>
      <span className="text-paper">
        {Array.from(codePart).map((ch, i) =>
          GANZHI_CHARS.test(ch) ? (
            <span key={i} className="text-gold-bright">
              {ch}
            </span>
          ) : (
            <span key={i}>{ch}</span>
          ),
        )}
      </span>
      {commentPart ? (
        <span className="text-paper-faint">
          {Array.from(commentPart).map((ch, i) =>
            GANZHI_CHARS.test(ch) ? (
              <span key={i} className="text-gold">
                {ch}
              </span>
            ) : (
              <span key={i}>{ch}</span>
            ),
          )}
        </span>
      ) : null}
    </>
  )
}

export default function AlgorithmSection() {
  const rootRef = useRef<HTMLElement>(null)
  const [breatheIdx, setBreatheIdx] = useState<number | null>(null)

  // 算法卡入场 + 64 卦波浪点亮
  useEffect(() => {
    const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches
    const ctx = gsap.context(() => {
      gsap.fromTo(
        '.algo-card',
        { y: 40, opacity: 0 },
        {
          y: 0,
          opacity: 1,
          duration: reduced ? 0.001 : 0.6,
          stagger: 0.1,
          ease: 'power3.out',
          scrollTrigger: { trigger: '.algo-list', start: 'top 80%', once: true },
        },
      )
      gsap.fromTo(
        '.hex-cell',
        { opacity: 0 },
        {
          opacity: 1,
          duration: reduced ? 0.001 : 0.3,
          stagger: 0.015,
          ease: 'none',
          scrollTrigger: { trigger: '.hex-grid', start: 'top 80%', once: true },
        },
      )
    }, rootRef)

    let breathe = 0
    if (!reduced) {
      breathe = window.setInterval(() => {
        setBreatheIdx(Math.floor(Math.random() * 64))
      }, 3_000)
    }
    return () => {
      ctx.revert()
      if (breathe) window.clearInterval(breathe)
    }
  }, [])

  return (
    <section ref={rootRef} className="hairline-t" aria-label="干支算法白皮书">
      <div className="mx-auto w-full max-w-container px-6 py-[72px] md:px-12 md:py-[120px]">
        <SectionHeading
          eyebrow="THE ALGORITHM"
          title="干支算法 · 可直译"
          subtitle="算法公开即审计。以下伪码与站内生成器逐行同构。"
        />

        {/* 四张算法卡 */}
        <div className="algo-list mt-16 flex flex-col gap-6">
          {CARDS.map((card) => (
            <div
              key={card.name}
              className="algo-card grid grid-cols-1 gap-6 border border-line bg-ink-3 p-6 opacity-0 md:grid-cols-[220px_1fr] md:p-8"
            >
              <h3 className="font-serif text-[24px] font-bold tracking-[0.04em] text-paper">
                {card.name}
              </h3>
              <div className="overflow-x-auto border border-line border-l-[3px] border-l-gold bg-ink px-5 py-4">
                <pre className="font-mono text-[13px] leading-[2] tracking-[0.02em]">
                  {card.code.map((line, i) => (
                    <div key={i} className="flex">
                      <span className="w-8 shrink-0 select-none text-right text-paper-faint">
                        {i + 1}
                      </span>
                      <span className="w-4 shrink-0" />
                      <code className="whitespace-pre">
                        <CodeLine line={line} />
                      </code>
                    </div>
                  ))}
                </pre>
              </div>
            </div>
          ))}
        </div>

        {/* 64 卦王弼序全表 */}
        <div className="mt-20">
          <div className="mb-6 flex flex-wrap items-baseline justify-between gap-3">
            <h3 className="font-serif text-[24px] font-bold tracking-[0.04em] text-paper">
              六十四卦 · 王弼序全表
            </h3>
            <span className="font-mono text-[11px] tracking-[0.1em] text-paper-faint">
              符号 U+4DC0–U+4DFF · 系统字形 · 无图片依赖
            </span>
          </div>
          <div className="overflow-x-auto">
            <div className="hex-grid grid min-w-[720px] grid-cols-8 border border-line">
              {HEXAGRAM_NAMES.map((name, i) => (
                <div
                  key={i}
                  title={`王弼序第 ${i + 1} 卦 · ${name}`}
                  className={`hex-cell group relative flex cursor-default flex-col items-center gap-1 border border-line px-2 py-3 opacity-0 transition-colors duration-200 hover:bg-ink-4 ${
                    breatheIdx === i ? 'dna-cell-breathe' : ''
                  }`}
                >
                  <span className="text-[22px] leading-none text-paper-dim transition-colors duration-200 group-hover:text-gold-bright">
                    {hexagramSymbol(i)}
                  </span>
                  <span className="text-[10px] leading-none text-paper-faint transition-colors duration-200 group-hover:text-paper">
                    {name}
                  </span>
                  <span className="absolute right-1 top-1 font-mono text-[9px] text-gold opacity-0 transition-opacity duration-200 group-hover:opacity-100">
                    {i + 1}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
