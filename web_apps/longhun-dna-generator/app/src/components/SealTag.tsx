import type { ReactNode } from 'react'

interface Props {
  children: ReactNode
  className?: string
}

/**
 * SealTag 虚线篆刻标签（design.md 5.3）
 * 1px dashed gold-dim · pill · Cinzel/Sans 12px · 字距 0.2em · hover 虚线转动
 */
export default function SealTag({ children, className = '' }: Props) {
  return (
    <span
      className={`group/seal inline-flex items-center gap-2 rounded-full border border-dashed border-gold-dim px-[14px] py-1 text-[12px] tracking-[0.2em] text-paper-dim transition-colors duration-300 hover:border-gold hover:text-paper ${className}`}
    >
      <svg
        width="8"
        height="8"
        viewBox="0 0 8 8"
        className="shrink-0 text-gold-dim transition-colors duration-300 group-hover/seal:text-gold"
        aria-hidden="true"
      >
        <rect
          x="1"
          y="1"
          width="6"
          height="6"
          fill="none"
          stroke="currentColor"
          strokeWidth="1"
          strokeDasharray="2 2"
          className="group-hover/seal:animate-dash-rotate"
        />
      </svg>
      {children}
    </span>
  )
}
