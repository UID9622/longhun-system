// DNA: #龍芯⚡️丙午·甲申·丁未·亥时·䷎谦-DNA-COMPLETION-c6ed20e5
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
/**
 * 啟動AI · 全局状态（React context，Layout 层挂载）
 * 对话仅存内存：不落盘、刷新即焚。
 * 打字机驱动：AI 回答 18ms/字推进 revealed；prefers-reduced-motion 直呈终态。
 * 快捷键：Cmd/Ctrl+K 开合控制台。
 */
import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useRef,
  useState,
  type ReactNode,
} from 'react'
import { ask, isCloudEnabled, type Answer } from '@/ai/engine'

export interface ChatMessage {
  id: string
  role: 'user' | 'ai'
  text: string // 用户原文
  answer?: Answer
  /** thinking=等待引擎；streaming=打字机中；done=终态 */
  status: 'thinking' | 'streaming' | 'done'
  revealed: number
}

interface LaunchAIContextValue {
  open: boolean
  setOpen: (v: boolean) => void
  toggle: () => void
  messages: ChatMessage[]
  send: (question: string) => void
  engineMode: 'local' | 'cloud'
}

const LaunchAIContext = createContext<LaunchAIContextValue | null>(null)

let seq = 0
const nextId = () => `m${++seq}-${Date.now()}`

const TYPE_MS = 18

export function LaunchAIProvider({ children }: { children: ReactNode }) {
  const [open, setOpen] = useState(false)
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const engineMode: 'local' | 'cloud' = isCloudEnabled() ? 'cloud' : 'local'
  const timerRef = useRef<number | null>(null)
  const reducedRef = useRef(
    typeof window !== 'undefined' &&
      window.matchMedia('(prefers-reduced-motion: reduce)').matches,
  )

  const toggle = useCallback(() => setOpen((v) => !v), [])

  // Cmd/Ctrl+K 开合
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault()
        toggle()
      }
    }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [toggle])

  // 打字机推进：找到正在 streaming 的消息，每 18ms +1 字
  useEffect(() => {
    const streaming = messages.find((m) => m.status === 'streaming')
    if (!streaming || !streaming.answer) return
    const full = streaming.answer.markdown.length
    if (reducedRef.current) {
      setMessages((prev) =>
        prev.map((m) => (m.id === streaming.id ? { ...m, revealed: full, status: 'done' } : m)),
      )
      return
    }
    timerRef.current = window.setInterval(() => {
      setMessages((prev) =>
        prev.map((m) => {
          if (m.id !== streaming.id || !m.answer) return m
          const next = Math.min(m.revealed + 1, m.answer.markdown.length)
          return { ...m, revealed: next, status: next >= m.answer.markdown.length ? 'done' : 'streaming' }
        }),
      )
    }, TYPE_MS)
    return () => {
      if (timerRef.current !== null) window.clearInterval(timerRef.current)
    }
  }, [messages])

  // 打开时若有 thinking 残留（极端时序），保底不卡死：交给 send 的 promise 处理即可

  const send = useCallback((question: string) => {
    const q = question.trim()
    if (!q) return
    const userMsg: ChatMessage = { id: nextId(), role: 'user', text: q, status: 'done', revealed: 0 }
    const aiId = nextId()
    const thinking: ChatMessage = { id: aiId, role: 'ai', text: '', status: 'thinking', revealed: 0 }
    setMessages((prev) => [...prev, userMsg, thinking])
    void ask(q).then((answer) => {
      setMessages((prev) =>
        prev.map((m) => (m.id === aiId ? { ...m, answer, status: 'streaming', revealed: 0 } : m)),
      )
    })
  }, [])

  const value = useMemo(
    () => ({ open, setOpen, toggle, messages, send, engineMode }),
    [open, toggle, messages, send, engineMode],
  )

  return <LaunchAIContext.Provider value={value}>{children}</LaunchAIContext.Provider>
}

export function useLaunchAI(): LaunchAIContextValue {
  const ctx = useContext(LaunchAIContext)
  if (!ctx) throw new Error('useLaunchAI must be used within LaunchAIProvider')
  return ctx
}
