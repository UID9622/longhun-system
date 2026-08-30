// DNA: #龍芯⚡️丙午·甲申·丁未·亥时·䷎谦-DNA-COMPLETION-5d4748ef
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
import type { ReactNode } from 'react'

interface Props {
  layer: string // P0…P4
  title: string
  caption?: string
  right?: ReactNode
  bigRef?: (el: HTMLSpanElement | null) => void
}

/** P0–P4 区头同构：巨型 mono 层号（120px, gold-dim）+ H2 + caption + 可选右侧印章 */
export default function LayerHeader({ layer, title, caption, right, bigRef }: Props) {
  return (
    <div className="flex items-end justify-between gap-8">
      <div>
        <span
          ref={bigRef}
          className="block font-mono text-[120px] font-semibold leading-[0.9] tracking-[-0.02em] text-gold-dim will-change-transform"
          aria-hidden="true"
        >
          {layer}
        </span>
        <h2 className="mt-4 font-serif text-[clamp(30px,4vw,52px)] font-bold leading-[1.15] tracking-[0.05em] text-paper">
          {title}
        </h2>
        {caption ? (
          <p className="mt-5 max-w-[560px] text-[13px] leading-[1.9] text-paper-dim">{caption}</p>
        ) : null}
      </div>
      {right ? <div className="hidden shrink-0 pb-2 md:block">{right}</div> : null}
    </div>
  )
}
