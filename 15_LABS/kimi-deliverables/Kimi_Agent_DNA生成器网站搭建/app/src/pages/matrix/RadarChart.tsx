import { motion } from 'framer-motion'
import { DIMS } from '@/pages/matrix/personas'

interface Props {
  /** 五维值 0–100，顺序同 DIMS */
  values: readonly number[]
  /** 变更时重新弹性展开 */
  resetKey: string
  size?: number
}

/**
 * 五维雷达图（matrix.md S3）
 * SVG 五边形雷达 · 金色填充 25% 透明 · 顶点标维度代号
 * 自中心 scale 0→1 弹性展开（spring stiffness 180 damping 18）
 */
export default function RadarChart({ values, resetKey, size = 240 }: Props) {
  const cx = 120
  const cy = 124
  const R = 86

  const pointAt = (i: number, ratio: number): [number, number] => {
    const angle = (-90 + i * 72) * (Math.PI / 180)
    return [cx + Math.cos(angle) * R * ratio, cy + Math.sin(angle) * R * ratio]
  }

  const ringPoints = [0.25, 0.5, 0.75, 1].map((ratio) =>
    Array.from({ length: 5 }, (_, i) => pointAt(i, ratio).join(',')).join(' '),
  )

  const valuePoints = Array.from({ length: 5 }, (_, i) =>
    pointAt(i, Math.max(0.06, (values[i] ?? 0) / 100)).join(','),
  ).join(' ')

  return (
    <svg
      width="100%"
      viewBox="0 0 240 248"
      style={{ maxWidth: size }}
      role="img"
      aria-label={`五维雷达图：${DIMS.map((d, i) => `${d.key} ${values[i]}`).join('，')}`}
    >
      {/* 同心五边形网格 */}
      {ringPoints.map((pts, i) => (
        <polygon
          key={i}
          points={pts}
          fill="none"
          stroke="var(--line)"
          strokeWidth="1"
        />
      ))}
      {/* 轴线 */}
      {Array.from({ length: 5 }, (_, i) => {
        const [x, y] = pointAt(i, 1)
        return (
          <line key={i} x1={cx} y1={cy} x2={x} y2={y} stroke="var(--line)" strokeWidth="1" />
        )
      })}
      {/* 数值多边形（弹性展开） */}
      <motion.g
        key={resetKey}
        initial={{ scale: 0, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        transition={{ type: 'spring', stiffness: 180, damping: 18 }}
        style={{ transformOrigin: `${cx}px ${cy}px` }}
      >
        <polygon
          points={valuePoints}
          fill="rgba(201,162,39,0.25)"
          stroke="var(--gold)"
          strokeWidth="1.5"
          strokeLinejoin="round"
        />
        {Array.from({ length: 5 }, (_, i) => {
          const [x, y] = pointAt(i, Math.max(0.06, (values[i] ?? 0) / 100))
          return <circle key={i} cx={x} cy={y} r="2.4" fill="var(--gold-bright)" />
        })}
      </motion.g>
      {/* 顶点维度代号 */}
      {DIMS.map((d, i) => {
        const [x, y] = pointAt(i, 1.22)
        return (
          <text
            key={d.key}
            x={x}
            y={y}
            textAnchor="middle"
            dominantBaseline="central"
            fill="var(--paper-dim)"
            style={{ fontFamily: '"JetBrains Mono", monospace', fontSize: 10, letterSpacing: '0.1em' }}
          >
            {d.key}
          </text>
        )
      })}
    </svg>
  )
}
