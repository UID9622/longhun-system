import type { ReactNode } from 'react'

interface Props {
  eyebrow: string
  title: ReactNode
  subtitle?: ReactNode
  align?: 'left' | 'center'
  className?: string
}

/**
 * SectionHeading 章节头（design.md 5.5）
 * Eyebrow（Cinzel + 左右 40px 发丝线）→ H2 宋体 → 可选 Body-L 副题
 */
export default function SectionHeading({
  eyebrow,
  title,
  subtitle,
  align = 'left',
  className = '',
}: Props) {
  const centered = align === 'center'
  return (
    <div className={`${centered ? 'text-center' : 'text-left'} ${className}`}>
      <div className={`flex items-center gap-6 ${centered ? 'justify-center' : ''}`}>
        <span className="h-px w-10 bg-line" aria-hidden="true" />
        <span className="eyebrow">{eyebrow}</span>
        <span className="h-px w-10 bg-line" aria-hidden="true" />
      </div>
      <h2 className="mt-6 font-serif font-bold text-[clamp(30px,4vw,52px)] leading-[1.15] tracking-[0.05em] text-paper">
        {title}
      </h2>
      {subtitle ? (
        <p
          className={`mt-6 max-w-[560px] text-[18px] leading-[1.9] tracking-[0.02em] text-paper-dim ${
            centered ? 'mx-auto' : ''
          }`}
        >
          {subtitle}
        </p>
      ) : null}
    </div>
  )
}
