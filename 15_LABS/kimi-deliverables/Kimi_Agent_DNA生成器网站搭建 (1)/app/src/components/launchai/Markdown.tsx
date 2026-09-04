/**
 * 啟動AI · markdown 子集渲染器（标题 / 列表 / 代码块 / 段落 / **强调** / `行内码`）
 * 黑金排版：ink-3 代码块 + 左缘 3px 金条（DNACode 风格）
 */
import type { ReactNode } from 'react'

/** 行内：**强调** 与 `行内码` */
function renderInline(text: string, keyPrefix: string): ReactNode[] {
  const parts = text.split(/(\*\*[^*]+\*\*|`[^`]+`)/g)
  return parts.map((p, i) => {
    const key = `${keyPrefix}-${i}`
    if (p.startsWith('**') && p.endsWith('**')) {
      return (
        <strong key={key} className="font-medium text-gold-bright">
          {p.slice(2, -2)}
        </strong>
      )
    }
    if (p.startsWith('`') && p.endsWith('`')) {
      return (
        <code key={key} className="border border-line bg-ink px-1.5 py-0.5 font-mono text-[12px] text-gold-bright">
          {p.slice(1, -1)}
        </code>
      )
    }
    return <span key={key}>{p}</span>
  })
}

interface Props {
  markdown: string
}

export default function Markdown({ markdown }: Props) {
  const lines = markdown.split('\n')
  const blocks: ReactNode[] = []
  let i = 0
  let key = 0

  while (i < lines.length) {
    const line = lines[i]

    // 代码块
    if (line.startsWith('```')) {
      const buf: string[] = []
      i++
      while (i < lines.length && !lines[i].startsWith('```')) {
        buf.push(lines[i])
        i++
      }
      i++ // 跳过收尾 ```
      blocks.push(
        <pre
          key={key++}
          className="my-3 overflow-x-auto border border-line border-l-[3px] border-l-gold bg-ink px-4 py-3 font-mono text-[12px] leading-[1.8] text-paper-dim"
        >
          {buf.join('\n')}
        </pre>,
      )
      continue
    }

    // 标题
    if (line.startsWith('### ')) {
      blocks.push(
        <h4 key={key++} className="mt-4 font-serif text-[15px] font-bold tracking-[0.04em] text-paper">
          {renderInline(line.slice(4), `h4-${key}`)}
        </h4>,
      )
      i++
      continue
    }
    if (line.startsWith('## ')) {
      blocks.push(
        <h3
          key={key++}
          className="mb-3 border-l-[3px] border-gold pl-3 font-serif text-[17px] font-bold tracking-[0.04em] text-paper"
        >
          {renderInline(line.slice(3), `h3-${key}`)}
        </h3>,
      )
      i++
      continue
    }

    // 列表项
    if (line.startsWith('- ')) {
      const items: string[] = []
      while (i < lines.length && lines[i].startsWith('- ')) {
        items.push(lines[i].slice(2))
        i++
      }
      blocks.push(
        <ul key={key++} className="my-2 space-y-1.5">
          {items.map((it, j) => (
            <li key={j} className="flex gap-2.5 text-[14px] leading-[1.8] text-paper-dim">
              <span className="mt-[11px] h-1.5 w-1.5 shrink-0 bg-gold-dim" aria-hidden="true" />
              <span>{renderInline(it, `li-${key}-${j}`)}</span>
            </li>
          ))}
        </ul>,
      )
      continue
    }

    // 空行
    if (line.trim() === '') {
      i++
      continue
    }

    // 普通段落
    blocks.push(
      <p key={key++} className="my-2 text-[14px] leading-[1.85] text-paper-dim">
        {renderInline(line, `p-${key}`)}
      </p>,
    )
    i++
  }

  return <div className="launchai-md">{blocks}</div>
}
