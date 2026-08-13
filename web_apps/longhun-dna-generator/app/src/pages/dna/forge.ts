/**
 * 在线铸造器核心逻辑（design/dna.md §S3）
 * 格式 v2.0：#龍芯⚡️{年}·{月}·{日}·{时辰}·{卦符卦名}-{动作}-{版本}-{日序号}-{哈希8}
 * 干支四柱来自 @/lib/ganzhi（与全站时钟同一算法）；哈希优先 Web Crypto SHA-256 前 8 位 hex，
 * 非安全上下文回退 FNV-1a（与 ganzhi.ts 同源）；日序号 localStorage 当日单调递增。
 */
import { getGanzhi, hexagramSymbol, HEXAGRAM_NAMES, fnv1a } from '@/lib/ganzhi'

export const ACTIONS = [
  'CREATE',
  'AUDIT-REPORT',
  'PROTOCOL',
  'SCRIPT',
  'DOC',
  'INTEL',
  'OTHER',
] as const

export interface DnaRecord {
  id: string
  code: string
  confirm: string
  title: string
  action: string
  version: string
  iso: string
  serial: string
  hash: string
  hexagramIndex: number
  createdAt: number
}

export interface ForgeResult extends DnaRecord {
  year: string
  month: string
  day: string
  hour: string
  hexSymbol: string
  hexName: string
}

const SEQ_PREFIX = 'uid9622:dna-seq:'
const HISTORY_KEY = 'uid9622:dna-history:v1'
const HISTORY_CAP = 20

function dayKey(d: Date): string {
  const m = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  return `${d.getFullYear()}-${m}-${day}`
}

/** 日序号：localStorage 当日计数器单调递增，0001 起 */
export function nextDailySerial(date: Date): string {
  const key = SEQ_PREFIX + dayKey(date)
  let n = 1
  try {
    n = (parseInt(window.localStorage.getItem(key) ?? '0', 10) || 0) + 1
    window.localStorage.setItem(key, String(n))
  } catch {
    /* 隐私模式下计数退回内存态，仍保证本次会话内递增 */
  }
  return String(Math.min(n, 9999)).padStart(4, '0')
}

async function sha256Hex8(input: string): Promise<string | null> {
  try {
    if (typeof crypto !== 'undefined' && crypto.subtle) {
      const buf = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(input))
      return Array.from(new Uint8Array(buf))
        .map((b) => b.toString(16).padStart(2, '0'))
        .join('')
        .slice(0, 8)
    }
  } catch {
    /* fall through */
  }
  return null
}

const CONFIRM_CHARS = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'
function randomConfirm8(): string {
  const buf = new Uint8Array(8)
  if (typeof crypto !== 'undefined' && crypto.getRandomValues) {
    crypto.getRandomValues(buf)
  } else {
    for (let i = 0; i < 8; i++) buf[i] = Math.floor(Math.random() * 256)
  }
  const s = Array.from(buf, (b) => CONFIRM_CHARS[b % CONFIRM_CHARS.length]).join('')
  return `${s.slice(0, 4)}-${s.slice(4)}`
}

/** 铸造一枚 DNA（纯前端，与 dna.md 铸造逻辑逐行同构） */
export async function forgeDna(
  title: string,
  action: string,
  version: string,
  date: Date,
): Promise<ForgeResult> {
  const p = getGanzhi(date)
  const serial = nextDailySerial(date)
  // 哈希：标题+动作+版本+ISO时间+序号
  const payload = `${title}|${action}|${version}|${date.toISOString()}|${serial}`
  const hash =
    (await sha256Hex8(payload)) ?? fnv1a(payload).toString(16).padStart(8, '0').slice(0, 8)
  // 卦：内容哈希首字节 % 64 → 王弼序
  const hexagramIndex = parseInt(hash.slice(0, 2), 16) % 64
  const hexSymbol = hexagramSymbol(hexagramIndex)
  const hexName = HEXAGRAM_NAMES[hexagramIndex]
  const code = `#龍芯⚡️${p.year}·${p.month}·${p.day}·${p.hour}·${hexSymbol}${hexName}-${action}-${version}-${serial}-${hash}`
  return {
    id: `${date.getTime()}-${serial}-${hash}`,
    code,
    confirm: `#CONFIRM🌌9622-ONLY-ONCE🧬${randomConfirm8()}`,
    title,
    action,
    version,
    iso: date.toISOString(),
    serial,
    hash,
    hexagramIndex,
    createdAt: Date.now(),
    year: p.year,
    month: p.month,
    day: p.day,
    hour: p.hour,
    hexSymbol,
    hexName,
  }
}

export function loadHistory(): DnaRecord[] {
  try {
    const raw = window.localStorage.getItem(HISTORY_KEY)
    if (!raw) return []
    const arr = JSON.parse(raw)
    return Array.isArray(arr) ? (arr as DnaRecord[]) : []
  } catch {
    return []
  }
}

function saveHistory(list: DnaRecord[]) {
  try {
    window.localStorage.setItem(HISTORY_KEY, JSON.stringify(list.slice(0, HISTORY_CAP)))
  } catch {
    /* ignore */
  }
}

export function pushHistory(rec: DnaRecord): DnaRecord[] {
  const next = [rec, ...loadHistory()].slice(0, HISTORY_CAP)
  saveHistory(next)
  return next
}

export function removeHistory(id: string): DnaRecord[] {
  const next = loadHistory().filter((r) => r.id !== id)
  saveHistory(next)
  return next
}

/** 下载存证卡：canvas 动态生成 1200×630 PNG（黑金卡面 + DNA + 二维码占位） */
export async function downloadCertificate(rec: DnaRecord): Promise<void> {
  try {
    await document.fonts?.ready
  } catch {
    /* fonts 不可用时用系统字形 */
  }
  const W = 1200
  const H = 630
  const canvas = document.createElement('canvas')
  canvas.width = W
  canvas.height = H
  const ctx = canvas.getContext('2d')
  if (!ctx) return

  // 墨底
  ctx.fillStyle = '#080706'
  ctx.fillRect(0, 0, W, H)
  // 1px 金线边框 + 内框
  ctx.strokeStyle = 'rgba(201,162,39,0.42)'
  ctx.lineWidth = 1
  ctx.strokeRect(24.5, 24.5, W - 49, H - 49)
  ctx.strokeStyle = 'rgba(201,162,39,0.16)'
  ctx.strokeRect(40.5, 40.5, W - 81, H - 81)
  // 左缘 3px 金条
  ctx.fillStyle = '#C9A227'
  ctx.fillRect(40, 40, 3, H - 80)

  // Eyebrow
  ctx.fillStyle = '#C9A227'
  ctx.font = '600 18px Cinzel, serif'
  ctx.textBaseline = 'alphabetic'
  const eyebrow = 'LONGHUN DNA CERTIFICATE · UID9622'
  ctx.save()
  // Cinzel 宽字距近似：手动加字距
  let ex = 88
  for (const ch of eyebrow) {
    ctx.fillText(ch, ex, 108)
    ex += ctx.measureText(ch).width + 7
  }
  ctx.restore()

  // 标题
  ctx.fillStyle = '#EFE7D3'
  ctx.font = '700 44px "Noto Serif SC", serif'
  ctx.fillText(rec.title.slice(0, 24) || '未命名之作', 88, 180)

  // DNA 码（mono，可换行两段）
  ctx.font = '400 24px "JetBrains Mono", monospace'
  ctx.fillStyle = '#E9CB6B'
  const code = rec.code
  const maxW = W - 88 - 240
  let line = ''
  let ly = 260
  for (const ch of Array.from(code)) {
    if (ctx.measureText(line + ch).width > maxW) {
      ctx.fillText(line, 88, ly)
      line = ch
      ly += 44
    } else {
      line += ch
    }
  }
  ctx.fillText(line, 88, ly)

  // 确认码（朱砂）
  ctx.font = '400 16px "JetBrains Mono", monospace'
  ctx.fillStyle = '#A8382A'
  ctx.fillText(rec.confirm, 88, ly + 76)

  // 铸造时间
  ctx.fillStyle = '#A49A80'
  ctx.font = '400 14px "JetBrains Mono", monospace'
  ctx.fillText(`CAST AT ${rec.iso} · SEQ ${rec.serial}`, 88, H - 84)
  ctx.fillText('uid9622.cn · 免费开源 · 数据主权在民', 88, H - 56)

  // 二维码占位（右下虚线方框）
  const qs = 132
  const qx = W - 88 - qs
  const qy = H - 96 - qs
  ctx.strokeStyle = 'rgba(201,162,39,0.6)'
  ctx.setLineDash([6, 5])
  ctx.strokeRect(qx, qy, qs, qs)
  ctx.setLineDash([])
  ctx.fillStyle = '#5C4C1C'
  ctx.font = '400 13px "JetBrains Mono", monospace'
  ctx.textAlign = 'center'
  ctx.fillText('QR SEAL', qx + qs / 2, qy + qs / 2 - 4)
  ctx.fillText('待刻', qx + qs / 2, qy + qs / 2 + 18)
  ctx.textAlign = 'left'

  const a = document.createElement('a')
  a.href = canvas.toDataURL('image/png')
  a.download = `dna-certificate-${rec.serial}-${rec.hash}.png`
  a.click()
}
