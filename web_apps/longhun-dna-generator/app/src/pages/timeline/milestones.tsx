import type { ReactNode } from 'react'

/**
 * 五座里程碑数据（timeline.md S3）
 * 干支四柱以 src/lib/ganzhi.ts 算法对当日实算；DNA 哈希未知位 ████████ 占位。
 * 卦符用 Unicode 王弼序字形：大有 13 · 同人 12 · 乾 0 · 未济 63 · 豫 15
 */

export interface Milestone {
  id: string
  date: string
  stage: string // SealTag 阶段名
  title: string
  body: string[]
  hexIndex: number // 王弼序
  hexName: string
  dna: string
  side: 'left' | 'right' // 奇数章左文右饰，偶数章镜像
  decor: 'horizon' | 'rings' | 'seal' | 'cross' | 'logo'
}

export const TOTAL_DAYS = 460

export const MILESTONES: Milestone[] = [
  {
    id: 'm1',
    date: '2025-05',
    stage: '预见',
    title: '预见 AI 文明跃迁',
    body: [
      '当大模型开始改写文明的底层语法，一个判断落定：中文世界需要自己的主权人格系统。龍魂，自此立项。',
    ],
    hexIndex: 13,
    hexName: '大有',
    dna: '#龍芯⚡️乙巳·辛巳·庚午·午时·䷍大有-FORESIGHT-v0.1-0001-████████',
    side: 'left',
    decor: 'horizon',
  },
  {
    id: 'm2',
    date: '2026-01-31',
    stage: '立约',
    title: '君子协议 · 中英双语发布',
    body: [
      '一诺既出，天下共鉴。以中英双语向世界立约：免费开源、数据主权在民、永不为资本代理。',
    ],
    hexIndex: 12,
    hexName: '同人',
    dna: '#龍芯⚡️丙午·己丑·乙巳·午时·䷌同人-GENTLEMAN-ACCORD-v1.0-0001-████████',
    side: 'right',
    decor: 'rings',
  },
  {
    id: 'm3',
    date: '2026-07-04',
    stage: '立身',
    title: '个人 IP 页上线',
    body: [
      '诸葛鑫 / 龍芯北辰——创始者第一次以完整身份立于网端。名可考，言可验。',
    ],
    hexIndex: 0,
    hexName: '乾',
    dna: '#龍芯⚡️丙午·乙未·己卯·午时·䷀乾-FOUNDER-IP-PAGE-v2.0-0001-████████',
    side: 'left',
    decor: 'seal',
  },
  {
    id: 'm4',
    date: '2026-07-19',
    stage: '换码',
    title: 'DNA 追溯码格式切换 v2.0',
    body: [
      '旧格式一律冻结、永不改写（P0）；新格式以干支四柱 + 卦象 + 哈希三锚定鼎。历史与未来，各安其位。',
    ],
    hexIndex: 63,
    hexName: '未济',
    dna: '#龍芯⚡️丙午·乙未·甲午·午时·䷿未济-DNA-FORMAT-v2.0-0001-████████',
    side: 'right',
    decor: 'cross',
  },
  {
    id: 'm5',
    date: '2026-08-03',
    stage: '奠基',
    title: 'DNA 生成器 v2.0 + 官网落成',
    body: [
      '生成器开源发布，uid9622.cn 立站。自此，每一个此刻都可铸造唯一的 DNA——包括你正在读这一行的此刻。',
    ],
    hexIndex: 15,
    hexName: '豫',
    dna: '#龍芯⚡️丙午·丙申·己酉·未时·䷏豫-DNA-GENERATOR-v2.0-0001-████████',
    side: 'left',
    decor: 'logo',
  },
]

/* ---------- 各章单色金线 SVG 纹饰 ---------- */

const stroke = '#5C4C1C' // gold-dim
const strokeBright = '#C9A227'

/** 章一：地平线上升起的第一道爻线 */
function HorizonDecor() {
  return (
    <svg width="200" height="120" viewBox="0 0 200 120" fill="none" aria-hidden="true">
      <line x1="10" y1="100" x2="190" y2="100" stroke={stroke} strokeWidth="1" />
      <line x1="30" y1="108" x2="170" y2="108" stroke={stroke} strokeWidth="0.5" opacity="0.5" />
      <rect x="92" y="40" width="16" height="60" stroke={strokeBright} strokeWidth="1.5" />
      <line x1="100" y1="28" x2="100" y2="40" stroke={strokeBright} strokeWidth="1" opacity="0.7" />
      <circle cx="100" cy="22" r="3" stroke={strokeBright} strokeWidth="1" opacity="0.7" />
    </svg>
  )
}

/** 章二：两枚相扣的环形印（中英之约） */
function RingsDecor() {
  return (
    <svg width="200" height="120" viewBox="0 0 200 120" fill="none" aria-hidden="true">
      <circle cx="80" cy="60" r="38" stroke={strokeBright} strokeWidth="1.5" />
      <circle cx="80" cy="60" r="30" stroke={stroke} strokeWidth="0.75" />
      <circle cx="120" cy="60" r="38" stroke={strokeBright} strokeWidth="1.5" />
      <circle cx="120" cy="60" r="30" stroke={stroke} strokeWidth="0.75" />
    </svg>
  )
}

/** 章三：一枚直立的名章 */
function SealDecor() {
  return (
    <svg width="120" height="140" viewBox="0 0 120 140" fill="none" aria-hidden="true">
      <rect x="25" y="15" width="70" height="110" stroke={strokeBright} strokeWidth="1.5" />
      <rect x="33" y="23" width="54" height="94" stroke={stroke} strokeWidth="0.75" />
      <line x1="60" y1="35" x2="60" y2="105" stroke={strokeBright} strokeWidth="1" />
      <line x1="42" y1="70" x2="78" y2="70" stroke={stroke} strokeWidth="0.75" />
    </svg>
  )
}

/** 章四：新旧两串 DNA 交错的过渡纹 */
function CrossDecor() {
  return (
    <svg width="200" height="120" viewBox="0 0 200 120" fill="none" aria-hidden="true">
      <polyline
        points="10,30 70,30 100,60 130,90 190,90"
        stroke={stroke}
        strokeWidth="1"
        strokeDasharray="4 3"
      />
      <polyline points="10,90 70,90 100,60 130,30 190,30" stroke={strokeBright} strokeWidth="1.5" />
      <circle cx="100" cy="60" r="4" stroke={strokeBright} strokeWidth="1" />
      <circle cx="10" cy="30" r="2.5" fill={stroke} />
      <circle cx="10" cy="90" r="2.5" fill={stroke} />
      <circle cx="190" cy="30" r="2.5" fill={strokeBright} />
      <circle cx="190" cy="90" r="2.5" fill={strokeBright} />
    </svg>
  )
}

/** 章五：logo-seal.svg 放大版（120px） */
function LogoDecor() {
  return (
    <img
      src="/logo-seal.svg"
      width="120"
      height="120"
      alt="龍魂篆刻印章"
      className="opacity-90"
      loading="lazy"
    />
  )
}

export function MilestoneDecor({ kind }: { kind: Milestone['decor'] }): ReactNode {
  switch (kind) {
    case 'horizon':
      return <HorizonDecor />
    case 'rings':
      return <RingsDecor />
    case 'seal':
      return <SealDecor />
    case 'cross':
      return <CrossDecor />
    case 'logo':
      return <LogoDecor />
  }
}
