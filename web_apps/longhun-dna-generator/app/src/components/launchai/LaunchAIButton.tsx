// DNA: #龍芯⚡️丙午·甲申·丁未·亥时·䷎谦-DNA-COMPLETION-0d21f32d
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
/**
 * 啟動AI · 全局浮动启动钮（design.md 5.3/5.4 技法）
 * 右下固定 · 方形篆刻印章：零圆角、双线金框、内刻「啟」
 * hover 四边金线依次绘制（复用 OutlineButton 四伪元素法）
 * 快捷键 Cmd/Ctrl+K 由 LaunchAIProvider 全局托管
 */
import { AnimatePresence, motion } from 'framer-motion'
import SealTag from '@/components/SealTag'
import { useLaunchAI } from '@/ai/useLaunchAI'

export default function LaunchAIButton() {
  const { open, toggle } = useLaunchAI()

  return (
    <AnimatePresence>
      {!open ? (
        <motion.div
          className="fixed bottom-6 right-6 z-[65] flex flex-col items-end gap-2"
          initial={{ opacity: 0, y: 24 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: 24 }}
          transition={{ duration: 0.35, ease: [0.22, 1, 0.36, 1] }}
        >
          <SealTag className="bg-ink">啟動 AI</SealTag>
          <button
            type="button"
            onClick={toggle}
            aria-label="打开龍魂·啟動AI 智能助手（快捷键 Ctrl+K）"
            className="group/launch relative flex h-14 w-14 items-center justify-center border border-line-strong bg-ink transition-colors duration-300 hover:bg-[rgba(201,162,39,0.06)]"
          >
            {/* 内圈第二道金线框（双线篆刻框） */}
            <span
              className="pointer-events-none absolute inset-[5px] border border-gold-dim transition-colors duration-300 group-hover/launch:border-gold"
              aria-hidden="true"
            />
            {/* 内刻「啟」 */}
            <span className="relative z-10 font-serif text-[22px] font-bold leading-none text-gold transition-colors duration-300 group-hover/launch:text-gold-bright">
              啟
            </span>
            {/* hover 四边金线依次绘制 */}
            <span className="pointer-events-none absolute left-0 top-0 h-px w-full origin-left scale-x-0 bg-gold-bright transition-transform duration-100 ease-linear group-hover/launch:scale-x-100" />
            <span className="pointer-events-none absolute right-0 top-0 h-full w-px origin-top scale-y-0 bg-gold-bright transition-transform delay-100 duration-100 ease-linear group-hover/launch:scale-y-100" />
            <span className="pointer-events-none absolute bottom-0 right-0 h-px w-full origin-right scale-x-0 bg-gold-bright transition-transform delay-200 duration-100 ease-linear group-hover/launch:scale-x-100" />
            <span className="pointer-events-none absolute bottom-0 left-0 h-full w-px origin-bottom scale-y-0 bg-gold-bright transition-transform delay-300 duration-100 ease-linear group-hover/launch:scale-y-100" />
          </button>
        </motion.div>
      ) : null}
    </AnimatePresence>
  )
}
