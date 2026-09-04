// DNA: #龍芯⚡️丙午·甲申·丁未·亥时·䷎谦-DNA-COMPLETION-68127038
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
/**
 * 啟動AI · 推荐问题 / 追问 chips
 * 首轮 6 个推荐问题；每轮回答后渲染 followups。
 * 样式：SealTag 虚线篆刻标签（design.md 5.3），零玻璃拟态。
 */
import { motion } from 'framer-motion'

export const INITIAL_SUGGESTIONS = [
  'P0 焊死十二条是什么',
  '帮我铸造一个 DNA',
  '君子协议讲了什么',
  '龍魂和别的 AI 公司有什么不同',
  '未济卦对 AI 治理的启示',
  'CSDN 上的真实数据',
] as const

interface Props {
  items: string[]
  onPick: (question: string) => void
  label?: string
}

export default function SuggestionChips({ items, onPick, label }: Props) {
  if (items.length === 0) return null
  return (
    <div className="mt-3">
      {label ? (
        <p className="mb-2 font-cinzel text-[10px] font-semibold uppercase tracking-[0.38em] text-gold-dim">
          {label}
        </p>
      ) : null}
      <div className="flex flex-wrap gap-2">
        {items.map((q, i) => (
          <motion.button
            key={q}
            type="button"
            onClick={() => onPick(q)}
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.05 * i, duration: 0.3, ease: [0.22, 1, 0.36, 1] }}
            className="group/chip inline-flex items-center gap-2 rounded-full border border-dashed border-gold-dim px-[14px] py-1.5 text-[12px] tracking-[0.06em] text-paper-dim transition-colors duration-300 hover:border-gold hover:text-paper"
          >
            <svg width="8" height="8" viewBox="0 0 8 8" className="shrink-0 text-gold-dim transition-colors duration-300 group-hover/chip:text-gold" aria-hidden="true">
              <rect x="1" y="1" width="6" height="6" fill="none" stroke="currentColor" strokeWidth="1" strokeDasharray="2 2" />
            </svg>
            {q}
          </motion.button>
        ))}
      </div>
    </div>
  )
}
