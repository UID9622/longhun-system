import type { ReactNode } from 'react'
import SealTag from '@/components/SealTag'

interface Props {
  eyebrow: string
  title: ReactNode
  subtitle?: ReactNode
  seal: string // 页码标记，如 「卷一 / PROTOCOL」
  backgroundImage?: string // 该页专属生成式纹样（弱化版）
  children?: ReactNode
}

/**
 * PageHero 内页页头（design.md 5.7）
 * 高 52vh · 底部对齐 H1 + 副题 · 顶部留白避让 Navbar · 底部发丝线 + SealTag 页码
 */
export default function PageHero({ eyebrow, title, subtitle, seal, backgroundImage, children }: Props) {
  return (
    <header className="relative flex min-h-[52vh] flex-col overflow-hidden">
      {backgroundImage ? (
        <div
          className="pointer-events-none absolute inset-0 opacity-30"
          style={{
            backgroundImage: `url(${backgroundImage})`,
            backgroundSize: 'cover',
            backgroundPosition: 'center',
          }}
          aria-hidden="true"
        />
      ) : null}
      <div
        className="pointer-events-none absolute inset-0"
        style={{
          background:
            'radial-gradient(ellipse at 50% 80%, transparent 20%, rgba(8,7,6,0.92) 100%)',
        }}
        aria-hidden="true"
      />
      {/* 顶部留白避让 Navbar（Layout 已垫 72px，合计 160px） */}
      <div className="h-[88px] shrink-0" aria-hidden="true" />
      <div className="relative z-10 mx-auto flex w-full max-w-container flex-1 flex-col justify-end px-6 pb-14 md:px-12">
        <span className="eyebrow">{eyebrow}</span>
        <h1 className="mt-6 font-serif font-black text-[clamp(40px,6vw,80px)] leading-[1.1] tracking-[0.05em] text-paper">
          {title}
        </h1>
        {subtitle ? (
          <p className="mt-6 max-w-[560px] text-[18px] leading-[1.9] text-paper-dim">{subtitle}</p>
        ) : null}
        {children}
      </div>
      <div className="relative z-10 hairline-b">
        <div className="mx-auto flex w-full max-w-container justify-end px-6 pb-4 md:px-12">
          <SealTag>{seal}</SealTag>
        </div>
      </div>
    </header>
  )
}
