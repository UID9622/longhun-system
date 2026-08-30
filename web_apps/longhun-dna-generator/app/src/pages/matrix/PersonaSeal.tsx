// DNA: #龍芯⚡️丙午·甲申·丁未·亥时·䷎谦-DNA-COMPLETION-bb4a2dce
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
interface Props {
  /** 印面单字（人格代号首字） */
  char: string
  size?: number
  tone?: 'gold' | 'vermilion'
  className?: string
}

/**
 * 人格方印 —— 篆刻风双线方印，各刻人格代号首字（matrix.md 资产引用）
 * 金线单色；朱砂仅用于会签盖印
 */
export default function PersonaSeal({ char, size = 32, tone = 'gold', className = '' }: Props) {
  const color = tone === 'vermilion' ? 'var(--vermilion)' : 'var(--gold)'
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 32 32"
      className={className}
      aria-hidden="true"
      role="presentation"
    >
      <rect x="1.5" y="1.5" width="29" height="29" fill="none" stroke={color} strokeWidth="1.4" />
      <rect x="4.5" y="4.5" width="23" height="23" fill="none" stroke={color} strokeWidth="0.7" />
      <text
        x="16"
        y="16"
        textAnchor="middle"
        dominantBaseline="central"
        fill={color}
        style={{
          fontFamily: '"Noto Serif SC", serif',
          fontWeight: 900,
          fontSize: 17,
        }}
      >
        {char}
      </text>
    </svg>
  )
}
