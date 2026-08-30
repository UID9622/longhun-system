// DNA: #龍芯⚡️丙午·甲申·丁未·亥时·䷎谦-DNA-COMPLETION-338fed72
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
import { useState } from 'react'
import { Copy, Check } from 'lucide-react'

interface Props {
  code: string
  className?: string
  fontSize?: number
  showCopy?: boolean
}

/**
 * DNACode 代码块（design.md 5.6）
 * ink-3 底 + 1px line + 左缘 3px 金条 · JetBrains Mono · 右上复制按钮（copy→check「已录入」1.5s）
 * 干支/卦符 → gold-bright；动作标签（CREATE/AUDIT 等）→ 朱砂；哈希 → paper-dim
 */
export default function DNACode({ code, className = '', fontSize = 14, showCopy = true }: Props) {
  const [copied, setCopied] = useState(false)

  const onCopy = async () => {
    try {
      await navigator.clipboard.writeText(code)
    } catch {
      /* 剪贴板不可用时静默 */
    }
    setCopied(true)
    window.setTimeout(() => setCopied(false), 1500)
  }

  // 轻量着色：干支字符与卦符 → 亮金；全大写动作段 → 朱砂；8 位 hex → paper-dim
  const GANZHI_RE = /[甲乙丙丁戊己庚辛壬癸子丑寅卯辰巳午未申酉戌亥]|[\u4DC0-\u4DFF]/u
  const ACTION_RE = /^[A-Z][A-Z-]{2,}$/
  const HASH_RE = /^[0-9a-f]{6,}$/i
  const segments = code.split(/([·\-\s])/).filter((s) => s.length > 0)

  return (
    <div
      className={`relative border border-line border-l-[3px] border-l-gold bg-ink-3 px-6 py-5 ${className}`}
    >
      {showCopy ? (
        <button
          type="button"
          onClick={onCopy}
          aria-label="复制 DNA 码"
          className="absolute right-3 top-3 inline-flex items-center gap-1.5 border border-line px-2 py-1 font-mono text-[11px] text-paper-dim transition-colors duration-200 hover:border-gold hover:text-gold"
        >
          {copied ? <Check size={12} className="text-gold" /> : <Copy size={12} />}
          {copied ? '已录入' : '复制'}
        </button>
      ) : null}
      <code
        className="block whitespace-pre-wrap break-all font-mono leading-[1.9] tracking-[0.04em] text-paper"
        style={{ fontSize }}
      >
        {segments.map((seg, i) => {
          if (/^[·\-\s]$/.test(seg)) return <span key={i}>{seg}</span>
          if (ACTION_RE.test(seg))
            return (
              <span key={i} className="text-vermilion">
                {seg}
              </span>
            )
          if (HASH_RE.test(seg))
            return (
              <span key={i} className="text-paper-dim">
                {seg}
              </span>
            )
          // 逐字符染干支/卦符
          return (
            <span key={i}>
              {Array.from(seg).map((ch, j) =>
                GANZHI_RE.test(ch) ? (
                  <span key={j} className="text-gold-bright">
                    {ch}
                  </span>
                ) : (
                  <span key={j}>{ch}</span>
                ),
              )}
            </span>
          )
        })}
      </code>
    </div>
  )
}
