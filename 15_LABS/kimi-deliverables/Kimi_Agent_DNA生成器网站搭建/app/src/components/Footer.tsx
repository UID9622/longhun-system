import { useState } from 'react'
import { Link } from 'react-router'
import { ArrowUpRight, Copy, Check } from 'lucide-react'
import { DNA_ANCHOR } from '@/components/Navbar'

const CONFIRM_CODE = '#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z'

const SITE_LINKS = [
  { to: '/', label: '卷首 · 首页' },
  { to: '/protocol', label: '龍魂协议' },
  { to: '/dna', label: 'DNA 追溯码' },
  { to: '/matrix', label: '16 人格矩阵' },
  { to: '/works', label: '作品开源' },
  { to: '/timeline', label: '远征日志' },
  { to: '/founder', label: '创始人' },
]

const WORK_LINKS = [
  { href: 'https://uid9622.cn/', label: 'CNSH 中文原生脚本' },
  { href: 'https://uid9622.cn/', label: '三才算法' },
  { href: 'https://uid9622.cn/', label: '开放审计引擎' },
  { href: 'https://blog.csdn.net/', label: 'CSDN 同步引擎' },
]

const HEX_ROW = '䷀䷁䷂䷃䷄䷅䷆䷇'

/** Footer（design.md 5.2） */
export default function Footer() {
  const [copied, setCopied] = useState(false)
  const copyAnchor = async () => {
    try {
      await navigator.clipboard.writeText(DNA_ANCHOR)
    } catch {
      /* ignore */
    }
    setCopied(true)
    window.setTimeout(() => setCopied(false), 1500)
  }

  return (
    <footer className="hairline-t bg-ink-2">
      <div className="mx-auto grid w-full max-w-container grid-cols-1 gap-12 px-6 py-16 md:grid-cols-4 md:px-12">
        {/* 1 宣言 */}
        <div className="flex flex-col gap-5">
          <img src="/logo-seal.svg" alt="龍魂印章" width={40} height={40} className="h-10 w-10" />
          <p className="font-serif text-[15px] font-bold leading-[2] tracking-[0.06em] text-paper">
            免费开源 · 为人民服务 · 数据主权在民
          </p>
          <p className="text-[13px] leading-[2] text-paper-dim">不做专利 · 不做企业 · 不走资本</p>
        </div>

        {/* 2 站点 */}
        <nav aria-label="站点地图">
          <h3 className="eyebrow mb-6">SITE</h3>
          <ul className="flex flex-col gap-3">
            {SITE_LINKS.map((l) => (
              <li key={l.to}>
                <Link
                  to={l.to}
                  className="text-[14px] text-paper-dim transition-colors duration-200 hover:text-gold"
                >
                  {l.label}
                </Link>
              </li>
            ))}
          </ul>
        </nav>

        {/* 3 作品 */}
        <nav aria-label="作品链接">
          <h3 className="eyebrow mb-6">WORKS</h3>
          <ul className="flex flex-col gap-3">
            {WORK_LINKS.map((l) => (
              <li key={l.label}>
                <a
                  href={l.href}
                  target="_blank"
                  rel="noreferrer"
                  className="group inline-flex items-center gap-1.5 text-[14px] text-paper-dim transition-colors duration-200 hover:text-gold"
                >
                  {l.label}
                  <ArrowUpRight
                    size={13}
                    className="text-paper-faint transition-colors duration-200 group-hover:text-gold"
                  />
                </a>
              </li>
            ))}
          </ul>
        </nav>

        {/* 4 印记 */}
        <div>
          <h3 className="eyebrow mb-6">IMPRINT</h3>
          <button
            type="button"
            onClick={copyAnchor}
            className="group flex items-start gap-2 text-left"
            aria-label="复制 DNA 锚定串"
          >
            <span className="break-all font-mono text-[11px] leading-[1.8] text-paper-faint transition-colors duration-200 group-hover:text-paper-dim">
              {DNA_ANCHOR}
            </span>
            {copied ? (
              <Check size={13} className="mt-1 shrink-0 text-gold" />
            ) : (
              <Copy size={13} className="mt-1 shrink-0 text-paper-faint group-hover:text-gold" />
            )}
          </button>
          <p className="mt-4 break-all font-mono text-[11px] leading-[1.8] text-vermilion">{CONFIRM_CODE}</p>
          <div className="mt-4 border border-dashed border-gold-dim px-3 py-2">
            <p className="font-mono text-[11px] tracking-[0.1em] text-paper-faint">
              GPG: ____ ____ ____ ____
            </p>
            <p className="mt-1 text-[11px] text-paper-faint">以站长注册表为准</p>
          </div>
        </div>
      </div>

      {/* 底行：八卦符号串 + 版权 */}
      <div className="hairline-t">
        <div className="mx-auto flex w-full max-w-container flex-col items-start justify-between gap-4 px-6 py-6 md:flex-row md:items-center md:px-12">
          <p className="select-none text-[16px] tracking-[0.3em] text-gold-dim" aria-hidden="true">
            {Array.from(HEX_ROW).map((ch, i) => (
              <span key={i} className="transition-colors duration-200 hover:text-gold-bright">
                {ch}
              </span>
            ))}
          </p>
          <p className="font-mono text-[12px] text-paper-faint">
            © 2025–2026 龍魂系统 UID9622 · 以人民之名
          </p>
        </div>
      </div>
    </footer>
  )
}
