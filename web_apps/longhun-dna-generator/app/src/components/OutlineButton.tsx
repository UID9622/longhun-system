// DNA: #龍芯⚡️丙午·甲申·丁未·亥时·䷎谦-DNA-COMPLETION-b7ad1089
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
import type { ReactNode } from 'react'
import { Link } from 'react-router'

interface Props {
  children: ReactNode
  variant?: 'solid' | 'ghost'
  to?: string
  href?: string
  onClick?: () => void
  className?: string
  small?: boolean
  ariaLabel?: string
}

/**
 * OutlineButton 军规描边按钮（design.md 5.4）
 * 零圆角 · 1px line-strong 描边 · Serif SC 700 · hover 四边金线依次绘制（每边 0.12s）
 */
export default function OutlineButton({
  children,
  variant = 'ghost',
  to,
  href,
  onClick,
  className = '',
  small = false,
  ariaLabel,
}: Props) {
  const base =
    'group/btn relative inline-flex items-center justify-center gap-3 overflow-hidden font-serif font-bold tracking-[0.3em] transition-colors duration-300 select-none'
  const sizing = small ? 'px-6 py-2.5 text-[13px]' : 'px-9 py-4 text-[15px]'
  const skin =
    variant === 'solid'
      ? 'bg-gold text-ink border border-gold hover:bg-gold-bright'
      : 'bg-transparent text-gold border border-line-strong hover:bg-[rgba(201,162,39,0.06)] hover:text-gold-bright'

  /* 四边金线（ghost 变体 hover 绘制；solid 变体用亮金 hover 底色即可） */
  const edges =
    variant === 'ghost' ? (
      <>
        <span className="pointer-events-none absolute left-0 top-0 h-px w-full origin-left scale-x-0 bg-gold-bright transition-transform duration-100 ease-linear group-hover/btn:scale-x-100" />
        <span className="pointer-events-none absolute right-0 top-0 h-full w-px origin-top scale-y-0 bg-gold-bright transition-transform delay-100 duration-100 ease-linear group-hover/btn:scale-y-100" />
        <span className="pointer-events-none absolute bottom-0 right-0 h-px w-full origin-right scale-x-0 bg-gold-bright transition-transform delay-200 duration-100 ease-linear group-hover/btn:scale-x-100" />
        <span className="pointer-events-none absolute bottom-0 left-0 h-full w-px origin-bottom scale-y-0 bg-gold-bright transition-transform delay-300 duration-100 ease-linear group-hover/btn:scale-y-100" />
      </>
    ) : null

  const cls = `${base} ${sizing} ${skin} ${className}`
  const inner = (
    <>
      {edges}
      <span className="relative z-10 inline-flex items-center gap-3">{children}</span>
    </>
  )

  if (to) {
    return (
      <Link to={to} className={cls} aria-label={ariaLabel}>
        {inner}
      </Link>
    )
  }
  if (href) {
    return (
      <a href={href} className={cls} target="_blank" rel="noreferrer" aria-label={ariaLabel}>
        {inner}
      </a>
    )
  }
  return (
    <button type="button" onClick={onClick} className={cls} aria-label={ariaLabel}>
      {inner}
    </button>
  )
}
