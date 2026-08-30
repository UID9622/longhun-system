// DNA: #龍芯⚡️丙午·甲申·丁未·亥时·䷎谦-DNA-COMPLETION-812186b0
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
import { useEffect, useRef } from 'react'
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'
import SectionHeading from '@/components/SectionHeading'
import OutlineButton from '@/components/OutlineButton'

gsap.registerPlugin(ScrollTrigger)

const PERSONAS = [
  '將', '史', '哲', '衡', '政', '法', '工', '商',
  '農', '醫', '文', '武', '謀', '信', '禮', '數',
]

/** S5 · 16 人格矩阵预告（左文右阵） */
export default function MatrixPreview() {
  const ref = useRef<HTMLElement>(null)

  useEffect(() => {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return
    const ctx = gsap.context(() => {
      // 从中心向外的径向 stagger
      const grid = ref.current?.querySelector('.matrix-grid')
      if (!grid) return
      const cells = gsap.utils.toArray<HTMLElement>('.matrix-cell', grid)
      const rect = grid.getBoundingClientRect()
      const cx = rect.left + rect.width / 2
      const cy = rect.top + rect.height / 2
      const ordered = cells
        .map((el) => {
          const r = el.getBoundingClientRect()
          return { el, d: Math.hypot(r.left + r.width / 2 - cx, r.top + r.height / 2 - cy) }
        })
        .sort((a, b) => a.d - b.d)
        .map((w) => w.el)
      gsap.fromTo(
        ordered,
        { scale: 0.6, opacity: 0 },
        {
          scale: 1,
          opacity: 1,
          duration: 0.5,
          ease: 'power3.out',
          stagger: 0.06,
          clearProps: 'opacity,transform', // 交还 CSS hover 控制
          scrollTrigger: { trigger: grid, start: 'top 75%' },
        },
      )
    }, ref)
    return () => ctx.revert()
  }, [])

  return (
    <section
      ref={ref}
      className="hairline-b relative overflow-hidden bg-ink py-[120px] max-md:py-[72px]"
      aria-label="16 人格矩阵预告"
    >
      {/* matrix-grid-bg.png 8% 垫底 */}
      <div
        className="pointer-events-none absolute inset-0 opacity-[0.08]"
        style={{
          backgroundImage: 'url(/matrix-grid-bg.png)',
          backgroundSize: 'cover',
          backgroundPosition: 'center',
        }}
        aria-hidden="true"
      />
      <div className="relative z-10 mx-auto grid w-full max-w-container grid-cols-12 items-center gap-12 px-6 md:px-12">
        <div className="col-span-12 lg:col-span-5">
          <SectionHeading
            eyebrow="THE MATRIX"
            title="十六人格 · 五维思维"
            subtitle="军事、历史、哲学、经济、政治——五维思维在十六个人格间动态调配，每一个决定都经过一场内阁辩论。"
          />
          <div className="mt-10">
            <OutlineButton to="/matrix" variant="ghost">
              进入矩阵
            </OutlineButton>
          </div>
        </div>
        <div className="col-span-12 lg:col-span-7">
          {/* hover 单格：上浮 4px + 金字转亮 + 其余降至 40%（纯 CSS，避免与 GSAP 冲突） */}
          <div className="matrix-grid group/grid grid grid-cols-4 gap-3">
            {PERSONAS.map((p, i) => (
              <div
                key={p}
                className="matrix-cell group/cell flex aspect-square cursor-default flex-col items-center justify-center gap-2 border border-line bg-ink-3 transition-all duration-200 hover:-translate-y-1 hover:border-gold group-hover/grid:opacity-40 hover:!opacity-100"
              >
                <span className="font-serif text-[clamp(24px,3.2vw,44px)] font-bold text-gold transition-colors duration-300 group-hover/cell:text-gold-bright">
                  {p}
                </span>
                <span className="font-mono text-[10px] tracking-[0.1em] text-paper-faint">
                  M-{String(i + 1).padStart(2, '0')}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  )
}
