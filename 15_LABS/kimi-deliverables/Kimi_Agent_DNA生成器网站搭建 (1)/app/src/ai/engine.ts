/**
 * 啟動AI · 引擎（纯前端 TS，移植自龍魂人格矩阵运行时）
 * ①人格路由（触发词计分，平局/零分 → generalist）
 * ②知识检索（关键词 + 同义词计分，top3）
 * ③按人格模板组装结构化回答（markdown 子集）
 * ④附站内来源（route）与外部快速链接 chips
 * ⑤每个回答尾部生成实时 DNA（复用 ganzhi.ts + localStorage 当日序号）
 * ⑥云端预留：VITE_LAUNCH_AI_ENDPOINT 存在则先 POST /api/chat，失败回退本地
 */
import { getGanzhi, fnv1a, hexagramSymbol, HEXAGRAM_FULL_NAMES } from '@/lib/ganzhi'
import { nextDailySerial } from '@/pages/dna/forge'
import { routePersona, type Persona } from '@/ai/personas'
import { searchKnowledge, type KnowledgeEntry } from '@/ai/knowledge'
import { quicklinksFor, type QuickLink } from '@/ai/quicklinks'

export interface Source {
  label: string
  route: string
}

export interface Answer {
  persona: Persona
  markdown: string
  sources: Source[]
  quicklinks: QuickLink[]
  dna: string
  followups: string[]
  /** 本回答由云端还是本地引擎产出 */
  engine: 'local' | 'cloud'
}

export const CLOUD_ENDPOINT = (import.meta.env.VITE_LAUNCH_AI_ENDPOINT as string | undefined) ?? ''

export function isCloudEnabled(): boolean {
  return CLOUD_ENDPOINT.length > 0
}

/* ---------- ⑤ 实时 DNA（与铸造器同一干支算法、同一 localStorage 当日序号） ---------- */

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

export async function launchDna(question: string, date: Date = new Date()): Promise<string> {
  const p = getGanzhi(date)
  const serial = nextDailySerial(date)
  const payload = `LAUNCH-AI|${question}|${date.toISOString()}|${serial}`
  const hash =
    (await sha256Hex8(payload)) ?? fnv1a(payload).toString(16).padStart(8, '0').slice(0, 8)
  return `#龍芯⚡️${p.year}·${p.month}·${p.day}·${p.hour}·${p.hexagramSymbol}${p.hexagramName}-LAUNCH-AI-v1.0-${serial}-${hash}`
}

/* ---------- ③ 人格模板 ---------- */

function sourcesOf(entries: KnowledgeEntry[]): Source[] {
  return entries.map((e) => ({ label: e.title, route: e.route }))
}

function followupsOf(entries: KnowledgeEntry[], personaId: string): string[] {
  const out: string[] = []
  for (const e of entries) {
    for (const f of e.followups ?? []) {
      if (!out.includes(f)) out.push(f)
    }
  }
  const fallback: Record<string, string[]> = {
    auditor: ['P0 焊死十二条是什么', '君子协议讲了什么'],
    coder: ['帮我铸造一个 DNA', '干支是怎么算出来的？'],
    philosopher: ['未济卦对 AI 治理的启示', '龍魂和别的 AI 公司有什么不同'],
    generalist: ['P0 焊死十二条是什么', '帮我铸造一个 DNA', '龍魂和别的 AI 公司有什么不同'],
  }
  for (const f of fallback[personaId] ?? fallback.generalist) {
    if (!out.includes(f)) out.push(f)
  }
  return out.slice(0, 3)
}

function auditorMarkdown(question: string, entries: KnowledgeEntry[]): string {
  const basis = entries.length > 0 ? entries[0].content : ''
  return [
    `## 审计判定 · 三色对照`,
    `**受审事项**：${question}`,
    `**审计基准**：P0 焊死十二则（第贰则 · 中国法律准绳为最高准绳）`,
    '',
    '- 🟢 **可通行**：符合 P0 十二则与君子协议六节之行为——免费开源、数据主权在民、不作恶、全程 DNA 可追溯',
    '- 🟡 **须留意**：涉及站外平台之数据与承诺，本引擎仅能以站内宪法对照，法条细节须自行复核（见下方检索提示）',
    '- 🔴 **红线**：触碰 P0 任何一则即违规——删除历史、僭越数据主权、作恶、为资本代理，人民保留永续冻结权',
    '',
    basis,
    '',
    '**处置建议**：依 P2 审计规则，质询必应、哈希公开可验；重大事项可走开放审计引擎独立复核。',
  ].join('\n')
}

function coderMarkdown(question: string, entries: KnowledgeEntry[]): string {
  const dnaRelated = entries.some((e) =>
    ['dna-format', 'ganzhi-algo', 'dna-uniqueness', 'forge-guide', 'verify-guide'].includes(e.id),
  )
  const intro = entries.length > 0 ? entries[0].content : ''
  const snippet = dnaRelated
    ? [
        '```ts',
        '// 铸造一枚 DNA（与站内铸造器同一算法）',
        "import { getGanzhi, fnv1a, hexagramSymbol, HEXAGRAM_NAMES } from '@/lib/ganzhi'",
        '',
        'const p = getGanzhi(new Date())',
        "const payload = `${title}|${action}|${version}|${new Date().toISOString()}|${serial}`",
        'const hash8 = fnv1a(payload).toString(16).padStart(8, \'0\').slice(0, 8)',
        'const hexIdx = parseInt(hash8.slice(0, 2), 16) % 64',
        'const dna = `#龍芯⚡️${p.year}·${p.month}·${p.day}·${p.hour}·${hexagramSymbol(hexIdx)}${HEXAGRAM_NAMES[hexIdx]}-${action}-${version}-${serial}-${hash8}`',
        '```',
      ]
    : [
        '```ts',
        '// 任务骨架：先立 P0 校验，再写业务逻辑——零黑箱，每一步可审计',
        'export async function run(task: Task): Promise<Result> {',
        '  assertP0Integrity() // 启动先验 P0，校验不通过则拒绝运行',
        '  const plan = triuneDecide(task) // 三才算法：天时 · 地利 · 人和',
        '  const result = await execute(plan)',
        '  return freezeWithDna(result) // 产物即刻铭刻干支 DNA',
        '}',
        '```',
      ]
  return [
    '## 架构师应答 · 可运行者优先',
    `**需求**：${question}`,
    '',
    intro,
    '',
    ...snippet,
    '',
    '每一行遵循 P0 第陆则（零黑箱承诺）与第玖则（DNA 全程追溯）——代码即证据。',
  ].join('\n')
}

function philosopherMarkdown(question: string, entries: KnowledgeEntry[]): string {
  let hexIdx = fnv1a(question) % 64
  if (question.includes('未济')) hexIdx = 63
  else if (question.includes('既济')) hexIdx = 62
  const symbol = hexagramSymbol(hexIdx)
  const fullName = HEXAGRAM_FULL_NAMES[hexIdx]
  const mapping = entries.length > 0 ? entries[0].content : ''
  return [
    `## 易解 · ${fullName}`,
    '',
    `【卦象】${symbol} **${fullName}**——王弼序第 ${hexIdx + 1} 卦。问句起卦，以问为机。`,
    '',
    '【现代映射】',
    mapping || '龍魂之事：以宪法为体、以人格为用，卦有六爻而事有始终。',
    '',
    '【启示】',
    '- 一爻不可躐等：系统之治，先焊死底座（P0），再谈枝叶',
    '- 阴阳相推：数据主权在民与系统可用性互为消长，守其中者久',
    '- 未济为终而未尝终：治理是永续的当下，而非一次性的竣工',
  ].join('\n')
}

function generalistMarkdown(question: string, entries: KnowledgeEntry[]): string {
  if (entries.length === 0) {
    return [
      '## 龍魂助手 · 诚实应答',
      `关于「${question}」，本地知识库未检索到高置信条目——宁可沉默，不可妄言（P1 言论真实义务）。`,
      '',
      '可改问站内已有之卷：',
      '- 协议：P0 焊死十二条、五层条目数',
      '- DNA：格式 v2.0、干支算法、铸造与验证',
      '- 作品：七项开源、君子协议、CSDN 数据',
      '- 远征与创始人：五座里程碑、三不三为',
    ].join('\n')
  }
  const [first, ...rest] = entries
  const parts = [first.content]
  if (rest.length > 0) {
    parts.push('', '**延伸阅读**')
    for (const e of rest) parts.push(`- ${e.title}（见来源链接）`)
  }
  return parts.join('\n')
}

function assembleMarkdown(persona: Persona, question: string, entries: KnowledgeEntry[]): string {
  switch (persona.id) {
    case 'auditor':
      return auditorMarkdown(question, entries)
    case 'coder':
      return coderMarkdown(question, entries)
    case 'philosopher':
      return philosopherMarkdown(question, entries)
    default:
      return generalistMarkdown(question, entries)
  }
}

/* ---------- ⑥ 云端增强（预留） ---------- */

interface CloudPayload {
  markdown?: string
  persona?: string
}

async function askCloud(question: string): Promise<CloudPayload | null> {
  if (!isCloudEnabled()) return null
  try {
    const ctrl = new AbortController()
    const timer = window.setTimeout(() => ctrl.abort(), 8000)
    const res = await fetch(`${CLOUD_ENDPOINT.replace(/\/$/, '')}/api/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question }),
      signal: ctrl.signal,
    })
    window.clearTimeout(timer)
    if (!res.ok) return null
    const data = (await res.json()) as CloudPayload
    if (typeof data.markdown !== 'string' || data.markdown.length === 0) return null
    return data
  } catch {
    return null
  }
}

/* ---------- 主入口 ---------- */

export async function ask(question: string): Promise<Answer> {
  const persona = routePersona(question)
  const entries = searchKnowledge(question, 3)
  const sources = sourcesOf(entries)
  const quicklinks = quicklinksFor(persona.id, entries.map((e) => e.id))
  const followups = followupsOf(entries, persona.id).filter((f) => f !== question.trim())
  const dna = await launchDna(question)

  const cloud = await askCloud(question)
  if (cloud) {
    return {
      persona,
      markdown: cloud.markdown!,
      sources,
      quicklinks,
      dna,
      followups,
      engine: 'cloud',
    }
  }

  return {
    persona,
    markdown: assembleMarkdown(persona, question, entries),
    sources,
    quicklinks,
    dna,
    followups,
    engine: 'local',
  }
}
