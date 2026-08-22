import { useEffect, useRef, useState, useCallback } from 'react'
import { AnimatePresence, motion } from 'framer-motion'
import { Check, ChevronDown, Copy, Download, Trash2, Share2 } from 'lucide-react'
import SectionHeading from '@/components/SectionHeading'
import OutlineButton from '@/components/OutlineButton'
import { getGanzhi, hexagramSymbol, formatCountdown, msToNextShichen } from '@/lib/ganzhi'
import {
  ACTIONS,
  forgeDna,
  loadHistory,
  pushHistory,
  removeHistory,
  downloadCertificate,
} from '@/pages/dna/forge'
import type { DnaRecord, ForgeResult } from '@/pages/dna/forge'

/**
 * S3 · 在线生成器（核心交互）
 * 左 5 列表单面板 / 右 7 列输出区；铸造动效 1.8s：
 * 64 卦高速轮转渐慢 → 定格本卦弹性 → 四柱亮金 → 卦次之 → 动作朱砂盖入 →
 * 版本/序号淡入 → 哈希老虎机 0.4s → 整串金色脉冲。
 */

type Phase = 'idle' | 'spinning' | 'revealing' | 'done'

const HEX_CHARS = '0123456789abcdef'

/** 哈希老虎机：8 位逐位滚定（0.4s） */
function SlotHash({ hash }: { hash: string }) {
  const [chars, setChars] = useState<string[]>(() => hash.split(''))
  const [locked, setLocked] = useState(0)

  useEffect(() => {
    const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches
    if (reduced) {
      setLocked(8)
      return
    }
    setLocked(0)
    const started = Date.now()
    const t = window.setInterval(() => {
      const elapsed = Date.now() - started
      const nowLocked = Math.min(8, Math.floor(elapsed / 50))
      setLocked(nowLocked)
      setChars((prev) =>
        prev.map((_, i) =>
          i < nowLocked ? hash[i] : HEX_CHARS[Math.floor(Math.random() * 16)],
        ),
      )
      if (nowLocked >= 8) {
        window.clearInterval(t)
        setChars(hash.split(''))
      }
    }, 40)
    return () => window.clearInterval(t)
  }, [hash])

  return (
    <span className="text-paper-dim">
      {chars.map((c, i) => (
        <span key={i} className={i >= locked ? 'dna-hash-rolling' : undefined}>
          {c}
        </span>
      ))}
    </span>
  )
}

export default function Generator() {
  const [title, setTitle] = useState('')
  const [action, setAction] = useState<string>(ACTIONS[0])
  const [version, setVersion] = useState('v1.0')
  const [useCustom, setUseCustom] = useState(false)
  const [customDt, setCustomDt] = useState('')
  const [error, setError] = useState('')

  const [phase, setPhase] = useState<Phase>('idle')
  const [result, setResult] = useState<ForgeResult | null>(null)
  const [step, setStep] = useState(0)
  const [spinIdx, setSpinIdx] = useState(0)
  const [history, setHistory] = useState<DnaRecord[]>([])
  const [copied, setCopied] = useState(false)
  const [host, setHost] = useState('')
  const timersRef = useRef<number[]>([])

  // 实时干支时钟（每 10s 刷新）
  const [liveGanzhi, setLiveGanzhi] = useState(() => getGanzhi())
  const [nextShichen, setNextShichen] = useState('')

  useEffect(() => {
    const tick = () => {
      setLiveGanzhi(getGanzhi(new Date()))
      setNextShichen(formatCountdown(msToNextShichen(new Date())))
    }
    tick()
    const t = window.setInterval(tick, 10_000)
    return () => window.clearInterval(t)
  }, [])

  useEffect(() => {
    setHost(typeof window !== 'undefined' ? window.location.origin : '')
  }, [])

  useEffect(() => {
    setHistory(loadHistory())
    return () => {
      timersRef.current.forEach((t) => window.clearTimeout(t))
    }
  }, [])

  const later = (fn: () => void, ms: number) => {
    timersRef.current.push(window.setTimeout(fn, ms))
  }

  const cast = async () => {
    if (phase === 'spinning' || phase === 'revealing') return
    if (!title.trim()) {
      setError('标题必填——为你的作品命名。')
      return
    }
    setError('')
    const date = useCustom && customDt ? new Date(customDt) : new Date()
    if (Number.isNaN(date.getTime())) {
      setError('指定时刻无效。')
      return
    }
    const res = await forgeDna(title.trim(), action, version.trim() || 'v1.0', date)
    setResult(res)
    setStep(0)
    setPhase('spinning')

    const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches
    if (reduced) {
      setStep(6)
      setPhase('done')
      setHistory(pushHistory(res))
      return
    }

    // 64 卦符高速轮转（80ms/帧）渐慢，约 1s
    let delay = 80
    let elapsed = 0
    const spinTick = () => {
      setSpinIdx(Math.floor(Math.random() * 64))
      elapsed += delay
      delay = 80 + elapsed * 0.28 // 渐慢
      if (elapsed < 1000) {
        later(spinTick, delay)
      } else {
        setSpinIdx(res.hexagramIndex)
        // 逐段铸造显现
        setPhase('revealing')
        later(() => setStep(1), 60) // 四柱先亮
        later(() => setStep(2), 320) // 卦定格弹性
        later(() => setStep(3), 620) // 动作朱砂盖入
        later(() => setStep(4), 860) // 版本/序号淡入
        later(() => setStep(5), 1080) // 哈希老虎机
        later(() => {
          setStep(6) // 金色脉冲 + 落库
          setPhase('done')
          setHistory(pushHistory(res))
        }, 1560)
      }
    }
    spinTick()
  }

  const copyCode = async (code: string) => {
    try {
      await navigator.clipboard.writeText(code)
    } catch {
      /* ignore */
    }
    setCopied(true)
    window.setTimeout(() => setCopied(false), 1500)
  }

  const shareResult = useCallback(async () => {
    if (!result) return
    const link = `${host}/dna?code=${encodeURIComponent(result.code)}`
    try {
      await navigator.clipboard.writeText(link)
      setCopySuccess(true)
      window.setTimeout(() => setCopySuccess(false), 2000)
    } catch {
      // 兜底：打开分享面板
      if (navigator.share) {
        try {
          await navigator.share({ title: result.code, url: link })
        } catch {
          /* 用户取消 */
        }
      }
    }
  }, [result, host])

  const spinning = phase === 'spinning'
  const forging = spinning || phase === 'revealing'

  const inputCls =
    'h-12 w-full border border-line bg-ink px-4 text-[16px] text-paper outline-none transition-colors duration-200 placeholder:text-paper-faint focus:border-gold'

  return (
    <section className="hairline-t" aria-label="在线生成器">
      <div className="mx-auto w-full max-w-container px-6 py-[72px] md:px-12 md:py-[120px]">
        <SectionHeading
          eyebrow="THE GENERATOR"
          title="生成你的 DNA"
          subtitle="免费、开源、永不收费。生成即拥有。"
        />

        {/* 实时干支时钟 */}
        <div className="mt-8 flex items-center justify-center gap-3">
          <span className="font-mono text-[13px] text-paper-dim tracking-[0.06em]">
            此刻 ·
          </span>
          <span className="font-serif text-[16px] font-bold text-gold tracking-[0.06em]">
            {liveGanzhi.year}{liveGanzhi.month}{liveGanzhi.day}{liveGanzhi.hour}
          </span>
          <span className="inline-flex h-1.5 w-1.5 animate-pulse rounded-full bg-gold" aria-hidden="true" />
          {nextShichen ? (
            <span className="font-mono text-[11px] text-paper-faint">
              下一个时辰 {nextShichen}
            </span>
          ) : null}
        </div>

        <div className="mt-16 grid grid-cols-1 gap-8 lg:grid-cols-12">
          {/* 左 5 列：表单面板 */}
          <div className="border border-line bg-ink-3 p-6 md:p-8 lg:col-span-5">
            <label className="block">
              <span className="mb-2 block font-mono text-[12px] tracking-[0.2em] text-gold-dim">
                标题 TITLE *
              </span>
              <input
                type="text"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                placeholder="为你的作品命名…"
                className={inputCls}
                maxLength={60}
              />
            </label>

            <label className="mt-6 block">
              <span className="mb-2 block font-mono text-[12px] tracking-[0.2em] text-gold-dim">
                动作标签 ACTION
              </span>
              <span className="relative block">
                <select
                  value={action}
                  onChange={(e) => setAction(e.target.value)}
                  className={`${inputCls} appearance-none pr-10 font-mono text-[14px]`}
                >
                  {ACTIONS.map((a) => (
                    <option key={a} value={a} className="bg-ink">
                      {a}
                    </option>
                  ))}
                </select>
                <ChevronDown
                  size={16}
                  className="pointer-events-none absolute right-4 top-1/2 -translate-y-1/2 text-paper-dim"
                />
              </span>
            </label>

            <label className="mt-6 block">
              <span className="mb-2 block font-mono text-[12px] tracking-[0.2em] text-gold-dim">
                版本 VERSION
              </span>
              <input
                type="text"
                value={version}
                onChange={(e) => setVersion(e.target.value)}
                placeholder="v1.0"
                className={`${inputCls} font-mono text-[14px]`}
                maxLength={12}
              />
            </label>

            <div className="mt-6">
              <span className="mb-2 block font-mono text-[12px] tracking-[0.2em] text-gold-dim">
                日期时间 MOMENT
              </span>
              <label className="flex cursor-pointer items-center gap-3 text-[14px] text-paper-dim">
                <input
                  type="checkbox"
                  checked={useCustom}
                  onChange={(e) => setUseCustom(e.target.checked)}
                  className="h-4 w-4 accent-[#C9A227]"
                />
                指定时刻（默认 = 此刻实时）
              </label>
              {useCustom ? (
                <input
                  type="datetime-local"
                  value={customDt}
                  onChange={(e) => setCustomDt(e.target.value)}
                  className={`${inputCls} mt-3 font-mono text-[14px]`}
                  style={{ colorScheme: 'dark' }}
                />
              ) : null}
            </div>

            {error ? <p className="mt-4 text-[13px] text-vermilion">{error}</p> : null}

            <OutlineButton
              variant="solid"
              onClick={cast}
              className={`mt-8 w-full text-[18px] tracking-[0.4em] ${forging ? 'pointer-events-none opacity-60' : ''}`}
              ariaLabel="铸造 DNA"
            >
              {forging ? '铸造中' : '铸 造'}
            </OutlineButton>
            <p className="mt-4 text-center font-mono text-[11px] tracking-[0.1em] text-paper-faint">
              纯前端铸造 · 日序号本机持久化 · 哈希 SHA-256
            </p>
          </div>

          {/* 右 7 列：输出区 */}
          <div className="lg:col-span-7">
            {phase === 'idle' ? (
              <div className="relative flex min-h-[320px] flex-col items-center justify-center overflow-hidden border border-dashed border-gold-dim">
                <span
                  aria-hidden="true"
                  className="animate-spin-slow select-none text-[120px] leading-none text-gold-dim opacity-20"
                >
                  ䷀
                </span>
                <span className="mt-4 font-serif text-[14px] text-paper-dim">
                  {liveGanzhi.year}年{liveGanzhi.month}月{liveGanzhi.day}日{liveGanzhi.hour}
                </span>
                <span className="absolute bottom-6 font-mono text-[12px] tracking-[0.3em] text-paper-faint">
                  待铸造
                </span>
              </div>
            ) : null}

            {spinning ? (
              <div className="relative flex min-h-[320px] flex-col items-center justify-center border border-line bg-ink-3">
                <span className="dna-spin-jitter select-none text-[96px] leading-none text-gold">
                  {hexagramSymbol(spinIdx)}
                </span>
                <span className="mt-6 font-mono text-[12px] tracking-[0.3em] text-gold-dim">
                  铸造中 · 64 卦轮转
                </span>
              </div>
            ) : null}

            {result && (phase === 'revealing' || phase === 'done') ? (
              <div
                key={result.id}
                className={`relative border border-line border-l-[3px] border-l-gold bg-ink-3 px-6 py-6 md:px-8 ${
                  phase === 'done' ? 'dna-pulse-once' : ''
                }`}
              >
                <div className="absolute right-3 top-3 flex items-center gap-2">
                  <button
                    type="button"
                    onClick={shareResult}
                    aria-label="复制分享链接"
                    className="inline-flex items-center gap-1.5 border border-line px-2 py-1 font-mono text-[11px] text-paper-dim transition-colors duration-200 hover:border-gold hover:text-gold"
                  >
                    {copySuccess ? <Check size={12} className="text-gold" /> : <Share2 size={12} />}
                    {copySuccess ? '已复制链接' : '分享'}
                  </button>
                  <button
                    type="button"
                    onClick={() => copyCode(result.code)}
                    aria-label="复制 DNA 码"
                    className="inline-flex items-center gap-1.5 border border-line px-2 py-1 font-mono text-[11px] text-paper-dim transition-colors duration-200 hover:border-gold hover:text-gold"
                  >
                    {copied ? <Check size={12} className="text-gold" /> : <Copy size={12} />}
                    {copied ? '已录入' : '复制'}
                  </button>
                </div>
                <code className="block break-all font-mono text-[clamp(14px,1.9vw,20px)] leading-[2.1] tracking-[0.04em] text-paper">
                  <span>#龍芯⚡️</span>
                  {step >= 1 ? (
                    <>
                      <span className="dna-field-in text-gold-bright">{result.year}</span>
                      <span>·</span>
                      <span className="dna-field-in text-gold-bright">{result.month}</span>
                      <span>·</span>
                      <span className="dna-field-in text-gold-bright">{result.day}</span>
                      <span>·</span>
                      <span className="dna-field-in text-gold-bright">{result.hour}</span>
                      <span>·</span>
                    </>
                  ) : null}
                  {step >= 2 ? (
                    <span className="dna-hex-lock text-gold-bright">
                      {result.hexSymbol}
                      {result.hexName}
                    </span>
                  ) : null}
                  {step >= 3 ? (
                    <>
                      <span>-</span>
                      <span className="dna-stamp text-vermilion">{result.action}</span>
                    </>
                  ) : null}
                  {step >= 4 ? (
                    <>
                      <span>-</span>
                      <span className="dna-field-in">{result.version}</span>
                      <span>-</span>
                      <span className="dna-field-in">{result.serial}</span>
                    </>
                  ) : null}
                  {step >= 5 ? (
                    <>
                      <span>-</span>
                      <SlotHash hash={result.hash} />
                    </>
                  ) : null}
                </code>

                {phase === 'done' ? (
                  <div className="mt-5 border-t border-line pt-5">
                    <p className="font-mono text-[12px] tracking-[0.04em] text-vermilion">
                      {result.confirm}
                    </p>
                    <div className="mt-4 flex flex-wrap items-center gap-4">
                      <OutlineButton
                        variant="ghost"
                        small
                        onClick={() => void downloadCertificate(result)}
                        ariaLabel="下载存证卡"
                      >
                        <Download size={14} /> 下载存证卡
                      </OutlineButton>
                      <span className="font-mono text-[11px] text-paper-faint">
                        {result.iso} · 王弼序第 {result.hexagramIndex + 1} 卦
                      </span>
                    </div>
                  </div>
                ) : null}
              </div>
            ) : null}

            {/* 本机铸造记录 */}
            <div className="mt-8">
              <div className="mb-3 flex items-baseline justify-between">
                <h3 className="font-serif text-[18px] font-bold tracking-[0.04em] text-paper">
                  本机铸造记录
                </h3>
                <span className="font-mono text-[11px] text-paper-faint">
                  localStorage 持久化 · 最新在顶
                </span>
              </div>
              {history.length === 0 ? (
                <p className="border border-dashed border-line px-4 py-6 text-center font-mono text-[12px] text-paper-faint">
                  尚无铸造记录
                </p>
              ) : (
                <ul className="flex flex-col gap-2">
                  <AnimatePresence initial={false}>
                    {history.map((rec) => (
                      <motion.li
                        key={rec.id}
                        layout="position"
                        initial={{ y: -20, opacity: 0 }}
                        animate={{ y: 0, opacity: 1 }}
                        exit={{ opacity: 0 }}
                        transition={{ duration: 0.4, ease: [0.22, 1, 0.36, 1] }}
                        className="group flex items-center gap-3 border border-line bg-ink-3 px-4 py-3"
                      >
                        <code className="min-w-0 flex-1 truncate font-mono text-[12px] tracking-[0.02em] text-paper-dim">
                          {rec.code}
                        </code>
                        <button
                          type="button"
                          onClick={() => copyCode(rec.code)}
                          aria-label="复制此条 DNA"
                          className="shrink-0 text-paper-faint transition-colors hover:text-gold"
                        >
                          <Copy size={14} />
                        </button>
                        <button
                          type="button"
                          onClick={() => setHistory(removeHistory(rec.id))}
                          aria-label="删除此条记录"
                          className="shrink-0 text-paper-faint transition-colors hover:text-vermilion"
                        >
                          <Trash2 size={14} />
                        </button>
                      </motion.li>
                    ))}
                  </AnimatePresence>
                </ul>
              )}
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
