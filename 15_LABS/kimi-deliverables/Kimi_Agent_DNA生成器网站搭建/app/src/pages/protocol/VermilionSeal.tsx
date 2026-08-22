/**
 * 朱砂方印（内联 SVG，篆刻方印风格）
 * chars：2 字纵排 或 4 字 2×2；朱砂 #A8382A，透明底。
 */
interface Props {
  chars: string[]
  size?: number
  rotate?: number
  className?: string
}

export default function VermilionSeal({ chars, size = 40, rotate = 0, className = '' }: Props) {
  const four = chars.length >= 4
  const cells = four
    ? [
        { x: 30, y: 29 },
        { x: 50, y: 29 },
        { x: 30, y: 51 },
        { x: 50, y: 51 },
      ]
    : [
        { x: 40, y: 30 },
        { x: 40, y: 52 },
      ]
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 80 80"
      role="img"
      aria-label={`朱砂印：${chars.join('')}`}
      className={className}
      style={rotate ? { transform: `rotate(${rotate}deg)` } : undefined}
    >
      <rect x="6" y="6" width="68" height="68" fill="none" stroke="#A8382A" strokeWidth="3.2" />
      <rect x="12.5" y="12.5" width="55" height="55" fill="none" stroke="#A8382A" strokeWidth="1.2" opacity="0.8" />
      {chars.slice(0, 4).map((ch, i) => (
        <text
          key={i}
          x={cells[i].x}
          y={cells[i].y}
          textAnchor="middle"
          dominantBaseline="central"
          fill="#A8382A"
          fontSize={four ? 21 : 24}
          fontWeight={900}
          fontFamily='"Noto Serif SC", serif'
        >
          {ch}
        </text>
      ))}
    </svg>
  )
}
