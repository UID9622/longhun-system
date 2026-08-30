// DNA: #龍芯⚡️丙午·甲申·丁未·亥时·䷎谦-DNA-COMPLETION-88ebccf2
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
/**
 * 啟動AI · 作战指挥台控制台（原创黑金军规风，非任何既有聊天产品样式）
 * 桌面：右侧 420px 全高抽屉 · 移动端：全屏 sheet
 * 墨黑 ink-2 底 · 顶部 1px 金发丝线 · 零圆角
 * 思考中 = 旋转卦符（☰☱☲☳ 逐帧 200ms），打字机由 LaunchAIProvider 驱动（18ms/字）
 * 对话不落盘 · 刷新即焚 · Esc 关闭 · 焦点陷阱
 */
import { useCallback, useEffect, useRef, useState, memo } from 'react'
import { Link } from 'react-router'
import { AnimatePresence, motion } from 'framer-motion'
import { X, ArrowUpRight, CornerDownLeft } from 'lucide-react'
import { useLaunchAI, type ChatMessage } from '@/ai/useLaunchAI'
import type { Answer } from '@/ai/engine'
import type { QuickLink } from '@/ai/quicklinks'
import Markdown from '@/components/launchai/Markdown'
import SuggestionChips, { INITIAL_SUGGESTIONS } from '@/components/launchai/SuggestionChips'

/* ---------- 思考中：旋转卦符（逐帧切换，非普通 spinner） ---------- */
const TRIGRAMS = ['☰', '☱', '☲', '☳']

const ThinkingTrigram = memo(function ThinkingTrigram() {
  const [frame, setFrame] = useState(0)
  useEffect(() => {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return
    const t = window.setInterval(() => setFrame((f) => (f + 1) % TRIGRAMS.length), 200)
    return () => window.clearInterval(t)
  }, [])
  return (
    <span className="inline-flex items-center gap-3" role="status" aria-label="思考中">
      <span className="font-serif text-[18px] text-gold">{TRIGRAMS[frame]}</span>
      <span className="text-[12px] tracking-[0.3em] text-paper-faint">推演中</span>
    </span>
  )
})

/* ---------- 人格印章徽标 ---------- */
function PersonaSeal({ answer }: { answer: Answer }) {
  const { persona } = answer
  const color =
    persona.sealColor === 'vermilion'
      ? 'border-vermilion text-vermilion'
      : persona.sealColor === 'paper'
        ? 'border-paper-dim text-paper'
        : 'border-gold-dim text-gold'
  return (
    <span className="mb-2 inline-flex items-center gap-2.5">
      <span
        className={`flex h-7 w-7 items-center justify-center border font-serif text-[13px] font-bold leading-none ${color}`}
        aria-hidden="true"
      >
        {persona.sealChar}
      </span>
      <span className="flex items-baseline gap-2">
        <span className="font-serif text-[13px] font-bold tracking-[0.08em] text-paper">{persona.name}</span>
        <span className="font-cinzel text-[9px] font-semibold uppercase tracking-[0.3em] text-gold-dim">
          {persona.latin}
        </span>
      </span>
    </span>
  )
}

/* ---------- 外部快速链接 chip（文案即提示，不裸 URL） ---------- */
function QuickLinkChip({ ql, onInternalNav }: { ql: QuickLink; onInternalNav: () => void }) {
  const cls =
    'inline-flex items-center gap-2 rounded-full border border-dashed border-gold-dim px-[14px] py-1 text-[11px] tracking-[0.08em] text-paper-dim transition-colors duration-300 hover:border-gold hover:text-paper'
  const inner = (
    <>
      <ArrowUpRight size={11} className="shrink-0 text-gold-dim" aria-hidden="true" />
      {ql.label}
    </>
  )
  if (ql.url?.startsWith('/')) {
    return (
      <Link to={ql.url} onClick={onInternalNav} className={cls} title={ql.hint} aria-label={ql.hint}>
        {inner}
      </Link>
    )
  }
  if (ql.url) {
    return (
      <a href={ql.url} target="_blank" rel="noreferrer" className={cls} title={ql.hint} aria-label={ql.hint}>
        {inner}
      </a>
    )
  }
  return (
    <span className={cls} title={ql.hint}>
      {inner}
    </span>
  )
}

/* ---------- 单条 AI 回答 ---------- */
function AiMessage({ msg, onClose, onFollowup }: { msg: ChatMessage; onClose: () => void; onFollowup: (q: string) => void }) {
  if (msg.status === 'thinking' || !msg.answer) {
    return (
      <div className="border border-line bg-ink-3 px-4 py-4">
        <ThinkingTrigram />
      </div>
    )
  }
  const a = msg.answer
  const shown = a.markdown.slice(0, msg.revealed)
  return (
    <article className="border border-line bg-ink-3 px-4 py-4" aria-label={`${a.persona.name}的回答`}>
      <PersonaSeal answer={a} />
      <Markdown markdown={shown} />
      {msg.status === 'streaming' ? (
        <span className="mt-1 inline-block h-3.5 w-2 animate-pulse bg-gold" aria-hidden="true" />
      ) : null}

      {msg.status === 'done' ? (
        <div className="mt-4 space-y-3">
          {/* 尾部实时 DNA */}
          <p className="break-all border border-line border-l-[3px] border-l-gold bg-ink px-3 py-2 font-mono text-[11px] leading-relaxed text-paper-faint">
            {a.dna}
          </p>
          {/* 诚实标注 */}
          <p className="text-[11px] tracking-[0.1em] text-paper-faint">
            {a.engine === 'local' ? '本地引擎 · 离线可用 · 云端增强待配置' : '云端增强 · 已接入部署引擎'}
          </p>
          {/* 站内来源 */}
          {a.sources.length > 0 ? (
            <div>
              <p className="mb-1.5 font-cinzel text-[9px] font-semibold uppercase tracking-[0.38em] text-gold-dim">
                SOURCES · 站内出处
              </p>
              <div className="flex flex-wrap gap-2">
                {a.sources.map((s) => (
                  <Link
                    key={s.route + s.label}
                    to={s.route}
                    onClick={onClose}
                    className="border border-line px-3 py-1 text-[11px] tracking-[0.08em] text-paper-dim transition-colors duration-300 hover:border-gold hover:text-gold-bright"
                  >
                    {s.label} →
                  </Link>
                ))}
              </div>
            </div>
          ) : null}
          {/* 外部快速链接 */}
          {a.quicklinks.length > 0 ? (
            <div>
              <p className="mb-1.5 font-cinzel text-[9px] font-semibold uppercase tracking-[0.38em] text-gold-dim">
                INDEX · 外部索引
              </p>
              <div className="flex flex-wrap gap-2">
                {a.quicklinks.map((ql) => (
                  <QuickLinkChip key={ql.id} ql={ql} onInternalNav={onClose} />
                ))}
              </div>
            </div>
          ) : null}
          {/* 追问 */}
          <SuggestionChips items={a.followups} onPick={onFollowup} label="FOLLOW · 追问" />
        </div>
      ) : null}
    </article>
  )
}

/* ---------- 控制台主体 ---------- */
export default function LaunchAIConsole() {
  const { open, setOpen, messages, send, engineMode } = useLaunchAI()
  const [draft, setDraft] = useState('')
  const panelRef = useRef<HTMLDivElement>(null)
  const scrollRef = useRef<HTMLDivElement>(null)
  const inputRef = useRef<HTMLInputElement>(null)

  const close = useCallback(() => setOpen(false), [setOpen])

  // Esc 关闭 + 焦点陷阱 + 打开时聚焦输入框
  useEffect(() => {
    if (!open) return
    const panel = panelRef.current
    inputRef.current?.focus()
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        close()
        return
      }
      if (e.key === 'Tab' && panel) {
        const focusables = panel.querySelectorAll<HTMLElement>(
          'button, a[href], input, [tabindex]:not([tabindex="-1"])',
        )
        if (focusables.length === 0) return
        const first = focusables[0]
        const last = focusables[focusables.length - 1]
        const active = document.activeElement as HTMLElement | null
        if (e.shiftKey && (active === first || !panel.contains(active))) {
          e.preventDefault()
          last.focus()
        } else if (!e.shiftKey && (active === last || !panel.contains(active))) {
          e.preventDefault()
          first.focus()
        }
      }
    }
    document.addEventListener('keydown', onKey)
    return () => document.removeEventListener('keydown', onKey)
  }, [open, close])

  // 打开时锁定背景滚动
  useEffect(() => {
    if (!open) return
    document.body.style.overflow = 'hidden'
    return () => {
      document.body.style.overflow = ''
    }
  }, [open])

  // 新消息 / 打字机推进 → 滚动到底
  useEffect(() => {
    const el = scrollRef.current
    if (el) el.scrollTop = el.scrollHeight
  }, [messages])

  const submit = useCallback(() => {
    const q = draft.trim()
    if (!q) return
    setDraft('')
    send(q)
  }, [draft, send])

  return (
    <AnimatePresence>
      {open ? (
        <>
          {/* 遮罩（移动端正压全屏；桌面弱化） */}
          <motion.div
            className="fixed inset-0 z-[68] bg-[rgba(8,7,6,0.72)] sm:bg-[rgba(8,7,6,0.45)]"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.25 }}
            onClick={close}
            aria-hidden="true"
          />
          <motion.div
            ref={panelRef}
            role="dialog"
            aria-modal="true"
            aria-label="龍魂·啟動AI 作战指挥台"
            className="fixed inset-y-0 right-0 z-[70] flex h-[100dvh] w-full flex-col border-l border-line bg-ink-2 sm:w-[420px]"
            initial={{ x: '100%' }}
            animate={{ x: 0 }}
            exit={{ x: '100%' }}
            transition={{ duration: 0.45, ease: [0.22, 1, 0.36, 1] }}
          >
            {/* 顶部 1px 金发丝线 */}
            <div className="h-px w-full bg-gold" aria-hidden="true" />

            {/* 标题栏 */}
            <header className="flex items-center justify-between gap-3 border-b border-line px-5 py-4">
              <div className="min-w-0">
                <p className="font-serif text-[17px] font-bold tracking-[0.1em] text-paper">龍魂·啟動AI</p>
                <p className="mt-0.5 font-cinzel text-[9px] font-semibold uppercase tracking-[0.38em] text-gold-dim">
                  LAUNCH AI · UID9622
                </p>
              </div>
              <div className="flex shrink-0 items-center gap-3">
                <span
                  className={`inline-flex items-center gap-1.5 border px-2.5 py-1 text-[10px] tracking-[0.14em] ${
                    engineMode === 'cloud' ? 'border-gold text-gold-bright' : 'border-gold-dim text-paper-dim'
                  }`}
                  aria-label={engineMode === 'cloud' ? '云端增强引擎已接入' : '本地引擎，离线可用'}
                >
                  <span className={`h-1.5 w-1.5 ${engineMode === 'cloud' ? 'bg-gold-bright' : 'bg-gold-dim'}`} aria-hidden="true" />
                  {engineMode === 'cloud' ? '云端增强' : '本地引擎 · 离线可用'}
                </span>
                <button
                  type="button"
                  onClick={close}
                  aria-label="关闭啟動AI 控制台（Esc）"
                  className="border border-line p-1.5 text-paper-dim transition-colors duration-300 hover:border-gold hover:text-paper"
                >
                  <X size={16} />
                </button>
              </div>
            </header>

            {/* 消息区 */}
            <div ref={scrollRef} className="flex-1 overflow-y-auto px-5 py-5" aria-live="polite">
              {messages.length === 0 ? (
                <div className="flex h-full flex-col justify-center">
                  <div className="border border-line-strong bg-ink px-5 py-6">
                    <p className="font-serif text-[20px] font-bold leading-relaxed tracking-[0.06em] text-paper">
                      作战指挥台已上线。
                    </p>
                    <p className="mt-3 text-[13px] leading-[1.9] text-paper-dim">
                      问站内一切：协议、DNA、人格矩阵、作品、远征、创始人。
                      四人格轮值——审计师、架构师、哲人、助手，按问句自动路由。
                    </p>
                    <p className="mt-3 text-[11px] tracking-[0.1em] text-paper-faint">
                      对话不落盘 · 刷新即焚
                    </p>
                  </div>
                  <SuggestionChips items={[...INITIAL_SUGGESTIONS]} onPick={send} label="BRIEFING · 首轮推荐" />
                </div>
              ) : (
                <div className="space-y-4">
                  {messages.map((m) =>
                    m.role === 'user' ? (
                      <div key={m.id} className="flex justify-end">
                        <div className="max-w-[85%] border border-line-strong bg-transparent px-4 py-3">
                          <p className="text-[14px] leading-[1.8] text-paper">{m.text}</p>
                        </div>
                      </div>
                    ) : (
                      <div key={m.id} className="flex justify-start">
                        <div className="max-w-full flex-1">
                          <AiMessage msg={m} onClose={close} onFollowup={send} />
                        </div>
                      </div>
                    ),
                  )}
                </div>
              )}
            </div>

            {/* 输入区 · 终端风 */}
            <div className="border-t border-line bg-ink px-5 py-4">
              <p className="mb-2 text-[10px] tracking-[0.2em] text-paper-faint">对话不落盘 · 刷新即焚</p>
              <div className="flex items-stretch gap-3">
                <label className="flex flex-1 items-center gap-2 border border-line bg-ink-3 px-3 transition-colors duration-300 focus-within:border-gold">
                  <span className="shrink-0 font-mono text-[12px] text-gold" aria-hidden="true">
                    龍魂@uid9622:~$
                  </span>
                  <span className="sr-only">输入你的问题</span>
                  <input
                    ref={inputRef}
                    type="text"
                    value={draft}
                    onChange={(e) => setDraft(e.target.value)}
                    onKeyDown={(e) => {
                      if (e.key === 'Enter' && !e.nativeEvent.isComposing) submit()
                    }}
                    placeholder="输入指令，回车发送"
                    aria-label="输入你的问题，回车发送"
                    className="w-full bg-transparent py-3 font-mono text-[13px] text-paper placeholder:text-paper-faint focus:outline-none"
                  />
                </label>
                <button
                  type="button"
                  onClick={submit}
                  aria-label="发送"
                  className="group/send relative inline-flex shrink-0 items-center gap-2 overflow-hidden border border-line-strong px-4 font-serif text-[13px] font-bold tracking-[0.2em] text-gold transition-colors duration-300 hover:bg-[rgba(201,162,39,0.06)] hover:text-gold-bright"
                >
                  <CornerDownLeft size={14} aria-hidden="true" />
                  发送
                  <span className="pointer-events-none absolute left-0 top-0 h-px w-full origin-left scale-x-0 bg-gold-bright transition-transform duration-100 ease-linear group-hover/send:scale-x-100" />
                  <span className="pointer-events-none absolute right-0 top-0 h-full w-px origin-top scale-y-0 bg-gold-bright transition-transform delay-100 duration-100 ease-linear group-hover/send:scale-y-100" />
                  <span className="pointer-events-none absolute bottom-0 right-0 h-px w-full origin-right scale-x-0 bg-gold-bright transition-transform delay-200 duration-100 ease-linear group-hover/send:scale-x-100" />
                  <span className="pointer-events-none absolute bottom-0 left-0 h-full w-px origin-bottom scale-y-0 bg-gold-bright transition-transform delay-300 duration-100 ease-linear group-hover/send:scale-y-100" />
                </button>
              </div>
            </div>
          </motion.div>
        </>
      ) : null}
    </AnimatePresence>
  )
}
