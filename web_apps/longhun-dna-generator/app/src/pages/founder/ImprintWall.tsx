import { useRef, useState } from 'react'
import { motion, useInView } from 'framer-motion'
import { Copy, Check } from 'lucide-react'
import SealTag from '@/components/SealTag'

const DNA_ANCHOR = '#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL'
const CONFIRM_CODE = '#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z'

/** 单条凭证行：DNACode 风 + 左 SealTag 分类 + 右复制按钮 */
function CredentialRow({
  tag,
  code,
  highlight,
  index,
  inView,
}: {
  tag: string
  code: string
  highlight?: string
  index: number
  inView: boolean
}) {
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

  // 朱砂高亮指定片段（确认码 ONLY-ONCE 段）
  const renderCode = () => {
    if (!highlight || !code.includes(highlight)) return code
    const [before, after] = code.split(highlight)
    return (
      <>
        {before}
        <span className="text-vermilion">{highlight}</span>
        {after}
      </>
    )
  }

  return (
    <motion.div
      initial={{ y: 30, opacity: 0 }}
      animate={inView ? { y: 0, opacity: 1 } : { y: 30, opacity: 0 }}
      transition={{ duration: 0.6, delay: index * 0.12, ease: [0.22, 1, 0.36, 1] }}
      className="flex flex-col gap-3 sm:flex-row sm:items-center sm:gap-6"
    >
      <div className="shrink-0 sm:w-[120px]">
        <SealTag>{tag}</SealTag>
      </div>
      {/* 复制点击：整条金色脉冲 + 左缘金条闪 */}
      <motion.div
        animate={
          copied
            ? {
                boxShadow: [
                  '0 0 0 0 rgba(201,162,39,0)',
                  '0 0 24px 2px rgba(201,162,39,0.35)',
                  '0 0 0 0 rgba(201,162,39,0)',
                ],
              }
            : { boxShadow: '0 0 0 0 rgba(201,162,39,0)' }
        }
        transition={{ duration: 0.8 }}
        className="relative flex-1 border border-line bg-ink-3 px-6 py-5"
      >
        <motion.span
          className="absolute bottom-0 left-0 top-0 bg-gold"
          animate={{ width: copied ? [3, 6, 3] : 3 }}
          transition={{ duration: 0.8 }}
          aria-hidden="true"
        />
        <code className="block break-all pr-20 font-mono text-[13px] leading-[1.9] tracking-[0.04em] text-paper">
          {renderCode()}
        </code>
        <button
          type="button"
          onClick={onCopy}
          aria-label={`复制${tag}`}
          className="absolute right-3 top-3 inline-flex items-center gap-1.5 border border-line px-2 py-1 font-mono text-[11px] text-paper-dim transition-colors duration-200 hover:border-gold hover:text-gold"
        >
          {copied ? <Check size={12} className="text-gold" /> : <Copy size={12} />}
          {copied ? '已录入' : '复制'}
        </button>
      </motion.div>
    </motion.div>
  )
}

/** GPG 指纹虚线占位（不可复制 · 禁用态 · 虚线流转） */
function GpgPlaceholder({ index, inView }: { index: number; inView: boolean }) {
  return (
    <motion.div
      initial={{ y: 30, opacity: 0 }}
      animate={inView ? { y: 0, opacity: 1 } : { y: 30, opacity: 0 }}
      transition={{ duration: 0.6, delay: index * 0.12, ease: [0.22, 1, 0.36, 1] }}
      className="flex flex-col gap-3 sm:flex-row sm:items-center sm:gap-6"
      aria-disabled="true"
    >
      <div className="shrink-0 sm:w-[120px]">
        <SealTag>GPG 指纹</SealTag>
      </div>
      <div className="relative flex-1 cursor-not-allowed opacity-70">
        {/* 虚线流转边框 */}
        <svg className="pointer-events-none absolute inset-0 h-full w-full" aria-hidden="true">
          <rect
            x="0.5"
            y="0.5"
            width="calc(100% - 1px)"
            height="calc(100% - 1px)"
            fill="none"
            stroke="var(--gold-dim)"
            strokeWidth="1"
            strokeDasharray="6 4"
            className="animate-dash-rotate"
            style={{ width: 'calc(100% - 1px)', height: 'calc(100% - 1px)' }}
          />
        </svg>
        <div className="bg-ink-3 px-6 py-5">
          <code className="block font-mono text-[13px] leading-[1.9] tracking-[0.3em] text-paper-faint">
            ____ ____ ____ ____ ____
          </code>
          <p className="mt-2 text-[13px] text-paper-faint">真实指纹以站长注册表为准 · 暂缓公示</p>
        </div>
      </div>
    </motion.div>
  )
}

/** S5 · 印记墙（founder.md S5）—— 纯 Framer Motion 域 */
export default function ImprintWall() {
  const ref = useRef<HTMLElement>(null)
  const inView = useInView(ref, { once: true, amount: 0.3 })

  return (
    <section ref={ref} className="hairline-b bg-ink-2 py-[120px] max-md:py-[72px]" aria-label="印记墙">
      <div className="mx-auto w-full max-w-container px-6 md:px-12">
        <div>
          <span className="eyebrow">THE IMPRINTS</span>
          <h2 className="mt-6 font-serif text-[clamp(30px,4vw,52px)] font-bold leading-[1.15] tracking-[0.05em] text-paper">
            印记 · 可验之身
          </h2>
          <p className="mt-4 text-[13px] tracking-[0.12em] text-paper-dim">
            以下印记全部公开可查。伪造必究，验证免费。
          </p>
        </div>

        <div className="mt-14 flex flex-col gap-8">
          <CredentialRow tag="DNA 锚定" code={DNA_ANCHOR} index={0} inView={inView} />
          <CredentialRow tag="确认码" code={CONFIRM_CODE} highlight="ONLY-ONCE" index={1} inView={inView} />
          <GpgPlaceholder index={2} inView={inView} />
        </div>
      </div>
    </section>
  )
}
