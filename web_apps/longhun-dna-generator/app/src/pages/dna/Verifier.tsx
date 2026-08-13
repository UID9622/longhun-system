import { useRef, useState } from 'react'
import { AlertTriangle, ShieldCheck } from 'lucide-react'
import OutlineButton from '@/components/OutlineButton'
import { verifyDna } from '@/pages/dna/verify'
import type { VerifyResult } from '@/pages/dna/verify'

/**
 * S4 · 验证器（#verify）
 * 单行输入 + ghost「验」；金色扫描线 0.8s 扫过后出三态结果：
 * ✅ 自洽解析表 / ⚠️ 朱砂警示 + 首个不合规字段 / 空态 64 卦水印「静候来码」。
 */

type VPhase = 'empty' | 'scanning' | 'done'

const FIELD_LABELS: Array<[keyof NonNullable<VerifyResult['fields']>, string]> = [
  ['year', '年柱'],
  ['month', '月柱'],
  ['day', '日柱'],
  ['hour', '时辰'],
  ['hexName', '卦象'],
  ['action', '动作'],
  ['version', '版本'],
  ['serial', '序号'],
  ['hash', '哈希'],
]

export default function Verifier() {
  const [value, setValue] = useState('')
  const [phase, setPhase] = useState<VPhase>('empty')
  const [result, setResult] = useState<VerifyResult | null>(null)
  const timerRef = useRef(0)

  const run = () => {
    if (phase === 'scanning') return
    window.clearTimeout(timerRef.current)
    const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches
    if (!value.trim()) {
      setResult(null)
      setPhase('empty')
      return
    }
    setPhase('scanning')
    timerRef.current = window.setTimeout(
      () => {
        setResult(verifyDna(value))
        setPhase('done')
      },
      reduced ? 0 : 850,
    )
  }

  const f = result?.fields ?? {}

  return (
    <section id="verify" className="hairline-t bg-ink-2 hairline-b" aria-label="验证器">
      <div className="mx-auto w-full max-w-[720px] px-6 py-[72px] md:py-[120px]">
        <h3 className="text-center font-serif text-[24px] font-bold tracking-[0.04em] text-paper">
          验 证
        </h3>
        <p className="mt-4 text-center text-[13px] leading-[1.9] text-paper-dim">
          粘贴任一龍魂 DNA，验其四柱、卦象与哈希是否自洽。
        </p>

        {/* 输入行 + 扫描线 */}
        <div className="relative mt-10">
          <div className="flex gap-3">
            <input
              type="text"
              value={value}
              onChange={(e) => setValue(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter') run()
              }}
              placeholder="#龍芯⚡️丙午·甲申·己卯·午时·䷀乾-CREATE-v1.0-0001-…"
              aria-label="待验证的 DNA 码"
              className="h-14 min-w-0 flex-1 border border-line bg-ink px-4 font-mono text-[15px] tracking-[0.02em] text-paper outline-none transition-colors duration-200 placeholder:text-paper-faint focus:border-gold"
            />
            <OutlineButton variant="ghost" onClick={run} small ariaLabel="验证">
              验
            </OutlineButton>
          </div>
          {phase === 'scanning' ? (
            <span
              aria-hidden="true"
              className="dna-scan pointer-events-none absolute top-0 h-full w-[2px] bg-gold-bright shadow-[0_0_12px_rgba(233,203,107,0.8)]"
            />
          ) : null}
        </div>

        {/* 结果面板 */}
        <div className="mt-8">
          {phase === 'empty' ? (
            <div className="relative flex min-h-[200px] items-center justify-center overflow-hidden border border-dashed border-line">
              <div
                aria-hidden="true"
                className="absolute inset-0 grid grid-cols-8 place-items-center text-[22px] text-gold opacity-[0.07] select-none"
              >
                {Array.from({ length: 64 }, (_, i) => (
                  <span key={i}>{String.fromCodePoint(0x4dc0 + i)}</span>
                ))}
              </div>
              <span className="relative font-mono text-[12px] tracking-[0.3em] text-paper-faint">
                静候来码
              </span>
            </div>
          ) : null}

          {phase === 'scanning' ? (
            <div className="border border-line bg-ink px-6 py-10 text-center font-mono text-[12px] tracking-[0.3em] text-gold-dim">
              逐段扫描中…
            </div>
          ) : null}

          {phase === 'done' && result ? (
            <div
              className="translate-y-0 border border-line bg-ink px-6 py-6 opacity-100 transition-all duration-400"
              style={{ animation: 'dna-field-in 0.4s cubic-bezier(0.22,1,0.36,1) both' }}
            >
              {result.status === 'ok' ? (
                <>
                  <div className="flex items-center gap-3">
                    <ShieldCheck size={20} className="text-gold" />
                    <span className="font-serif text-[18px] font-bold tracking-[0.06em] text-gold">
                      自洽 · 此码合法
                    </span>
                  </div>
                  <dl className="mt-6 grid grid-cols-1 gap-x-8 sm:grid-cols-2">
                    {FIELD_LABELS.map(([key, label]) => (
                      <div
                        key={key}
                        className="flex items-baseline justify-between border-b border-line py-2.5"
                      >
                        <dt className="text-[13px] text-paper-dim">{label}</dt>
                        <dd className="font-mono text-[13px] tracking-[0.04em] text-gold-bright">
                          {key === 'hexName'
                            ? `${f.hexSymbol ?? ''}${f.hexName ?? ''} · 第 ${(f.hexIndex ?? 0) + 1} 卦`
                            : String(f[key] ?? '—')}
                        </dd>
                      </div>
                    ))}
                  </dl>
                  <p className="mt-4 font-mono text-[11px] text-paper-faint">
                    注：哈希内容不可逆推，此处验其结构、甲子配对、五虎遁与卦序自洽。
                  </p>
                </>
              ) : (
                <>
                  <div className="flex items-center gap-3">
                    <AlertTriangle size={20} className="text-vermilion" />
                    <span className="font-serif text-[18px] font-bold tracking-[0.06em] text-vermilion">
                      格式存疑
                    </span>
                  </div>
                  <ul className="mt-6 flex flex-col gap-3">
                    {result.issues.map((iss, i) => (
                      <li key={i} className="border-l-2 border-vermilion pl-4">
                        <span className="text-[13px] text-paper">{iss.field}</span>
                        <span className="ml-3 text-[13px] text-paper-dim">{iss.message}</span>
                        {iss.segment ? (
                          <code className="mt-1 block break-all font-mono text-[13px] text-vermilion underline decoration-vermilion underline-offset-4">
                            {iss.segment}
                          </code>
                        ) : null}
                      </li>
                    ))}
                  </ul>
                </>
              )}
            </div>
          ) : null}
        </div>
      </div>
    </section>
  )
}
