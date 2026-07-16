import { useRef, useMemo, memo } from 'react';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { motion } from 'framer-motion';
import { useGsapScroll } from './useGsapScroll';
import GlassPanel from '@/components/GlassPanel';
import AuthorityReveal from '@/components/AuthorityReveal';

gsap.registerPlugin(ScrollTrigger);

interface WuxingWeights {
  metal: number;
  wood: number;
  water: number;
  fire: number;
  earth: number;
}

interface Props {
  weights: WuxingWeights;
  onWeightsChange: (w: WuxingWeights) => void;
}

/* ─────────── Wuxing element config ─────────── */

const ELEMENTS = [
  { key: 'metal' as const, label: '金', en: 'Metal', color: '#FFFFFF', angle: -90 },
  { key: 'water' as const, label: '水', en: 'Water', color: '#1A1A2E', angle: -18 },
  { key: 'wood' as const, label: '木', en: 'Wood', color: '#00C853', angle: 54 },
  { key: 'fire' as const, label: '火', en: 'Fire', color: '#FF3D00', angle: 126 },
  { key: 'earth' as const, label: '土', en: 'Earth', color: '#FFD600', angle: 198 },
];

/* ─────────── Pentagon vertex position ─────────── */
function getVertex(cx: number, cy: number, r: number, angleDeg: number) {
  const rad = (angleDeg * Math.PI) / 180;
  return { x: cx + r * Math.cos(rad), y: cy + r * Math.sin(rad) };
}

/* ═══════════════════ SVG WUXING PENTAGON ═══════════════════ */

const WuxingPentagon = memo(function WuxingPentagon({ weights, onToggle }: { weights: WuxingWeights; onToggle: (key: keyof WuxingWeights) => void }) {
  const cx = 300;
  const cy = 300;
  const r = 200;
  const circleR = 40;

  const vertices = useMemo(
    () => ELEMENTS.map((el) => ({ ...el, ...getVertex(cx, cy, r, el.angle) })),
    []
  );

  /* Creation cycle (outer pentagon): 金→水→木→火→土→金 */
  const creationOrder = [0, 1, 2, 3, 4, 0];
  const creationPath = creationOrder.map((i) => `${vertices[i].x},${vertices[i].y}`).join(' ');

  /* Destruction cycle (inner star) */
  const destructionOrder = [0, 2, 4, 1, 3, 0];
  const destructionPath = destructionOrder.map((i) => `${vertices[i].x},${vertices[i].y}`).join(' ');

  return (
    <svg
      viewBox="0 0 600 600"
      className="w-full max-w-[600px] h-auto"
      style={{ overflow: 'visible' }}
    >
      <defs>
        {vertices.map((v) => (
          <filter key={v.key} id={`glow-${v.key}`}>
            <feGaussianBlur stdDeviation="6" result="blur" />
            <feMerge>
              <feMergeNode in="blur" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>
        ))}
        {/* Arrow marker for creation cycle */}
        <marker id="arrow-creation" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto" markerUnits="strokeWidth">
          <path d="M0,0 L0,6 L9,3 z" fill="#FFD700" />
        </marker>
        <marker id="arrow-destruction" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto" markerUnits="strokeWidth">
          <path d="M0,0 L0,6 L9,3 z" fill="#FF3D00" />
        </marker>
      </defs>

      {/* Outer pentagon — creation cycle */}
      <polygon
        points={creationPath}
        fill="none"
        stroke="#FFD700"
        strokeWidth="2"
        opacity="0.4"
        markerEnd="url(#arrow-creation)"
        strokeDasharray="6 3"
      />

      {/* Inner star — destruction cycle */}
      <polygon
        points={destructionPath}
        fill="none"
        stroke="#FF3D00"
        strokeWidth="1.5"
        opacity="0.25"
        strokeDasharray="4 4"
      />

      {/* Arrows along creation cycle */}
      {creationOrder.slice(0, -1).map((fromIdx, i) => {
        const toIdx = creationOrder[i + 1];
        const from = vertices[fromIdx];
        const to = vertices[toIdx];
        return (
          <line
            key={`creation-${i}`}
            x1={from.x} y1={from.y}
            x2={to.x} y2={to.y}
            stroke="#FFD700"
            strokeWidth="2"
            opacity="0.5"
            markerEnd="url(#arrow-creation)"
          />
        );
      })}

      {/* Element circles */}
      {vertices.map((v) => (
        <g
          key={v.key}
          onClick={() => onToggle(v.key)}
          style={{ cursor: 'pointer' }}
          filter={`url(#glow-${v.key})`}
        >
          <circle
            cx={v.x}
            cy={v.y}
            r={circleR}
            fill={v.color}
            stroke={v.color === '#FFFFFF' ? '#FFD700' : v.color}
            strokeWidth="3"
            opacity={weights[v.key] > 0 ? 1 : 0.3}
            style={{ transition: 'opacity 0.3s' }}
          />
          {/* Chinese character */}
          <text
            x={v.x}
            y={v.y}
            textAnchor="middle"
            dominantBaseline="central"
            fontSize="28"
            fontWeight="700"
            fontFamily="Noto Serif SC, serif"
            fill={v.color === '#FFFFFF' || v.color === '#FFD600' ? '#1A1A2E' : '#FFFFFF'}
            style={{ pointerEvents: 'none' }}
          >
            {v.label}
          </text>
          {/* Weight label */}
          <text
            x={v.x}
            y={v.y + circleR + 18}
            textAnchor="middle"
            fontSize="13"
            fontFamily="JetBrains Mono, monospace"
            fill="var(--spectrum-bright)"
            fontWeight="600"
          >
            {v.label}: {weights[v.key].toFixed(2)}
          </text>
        </g>
      ))}
    </svg>
  );
});

/* ─────────── Element Detail Card ─────────── */

function ElementCard({
  element,
  weight,
  onToggle,
}: {
  element: typeof ELEMENTS[0];
  weight: number;
  onToggle: () => void;
}) {
  return (
    <motion.div
      whileHover={{ scale: 1.05, y: -4 }}
      whileTap={{ scale: 0.97 }}
      className="cursor-pointer"
      onClick={onToggle}
    >
      <GlassPanel
        className="p-4 flex flex-col items-center gap-2 min-w-[140px]"
        style={{
          borderColor: `${element.color}40`,
          opacity: weight > 0 ? 1 : 0.5,
          transition: 'opacity 0.3s',
        }}
      >
        <span
          className="font-noto-serif text-[28px] font-bold"
          style={{ color: element.color }}
        >
          {element.label}
        </span>
        <div
          className="w-6 h-6 rounded-full"
          style={{ backgroundColor: element.color, boxShadow: `0 0 10px ${element.color}60` }}
        />
        <span className="font-jetbrain text-[22px] font-bold tabular-nums" style={{ color: element.color }}>
          {weight.toFixed(2)}
        </span>
        <span className="text-label font-noto-sans" style={{ color: 'var(--spectrum-dim)' }}>
          {element.en}
        </span>
      </GlassPanel>
    </motion.div>
  );
}

/* ─────────── Sigma/Avg Bar Chart ─────────── */

function SigmaBarChart({ weights }: { weights: WuxingWeights }) {
  const values = [weights.metal, weights.wood, weights.water, weights.fire, weights.earth];
  const mean = values.reduce((a, b) => a + b, 0) / values.length;
  const stdDev = Math.sqrt(values.reduce((sq, n) => sq + Math.pow(n - mean, 2), 0) / values.length);

  return (
    <GlassPanel className="p-6 max-w-[400px] mx-auto w-full">
      <h4 className="text-label font-noto-sans mb-4 text-center" style={{ color: 'var(--spectrum-dim)' }}>
        σ/avg 分布图
      </h4>
      <div className="flex items-end gap-3 h-[120px] relative">
        {/* Mean line */}
        <div
          className="absolute left-0 right-0 border-t border-dashed z-10"
          style={{ borderColor: 'var(--spectrum-dim)', bottom: `${mean * 200}px` }}
        />
        {/* Sigma band */}
        <div
          className="absolute left-0 right-0 z-0 rounded"
          style={{
            bottom: `${Math.max(0, (mean - stdDev) * 200)}px`,
            height: `${stdDev * 400}px`,
            backgroundColor: 'rgba(255,215,0,0.08)',
          }}
        />
        {values.map((v, i) => {
          const aboveMean = v >= mean;
          const barHeight = Math.max(v * 200, 2);
          return (
            <div key={i} className="flex-1 flex flex-col items-center gap-1 relative z-10">
              <motion.div
                initial={{ height: 0 }}
                whileInView={{ height: barHeight }}
                viewport={{ once: true }}
                transition={{ duration: 0.8, delay: i * 0.06, ease: [0.16, 1, 0.3, 1] as [number, number, number, number] }}
                className="w-full rounded-t"
                style={{
                  backgroundColor: aboveMean ? 'var(--dragon-green)' : 'var(--dragon-yellow)',
                  opacity: 0.8,
                }}
              />
              <span className="text-label font-noto-sans" style={{ color: 'var(--spectrum-dim)' }}>
                {ELEMENTS[i].label}
              </span>
            </div>
          );
        })}
      </div>
      <div className="mt-3 text-caption font-jetbrain text-center" style={{ color: 'var(--spectrum-dim)' }}>
        均值 μ = {mean.toFixed(3)} | 标准差 σ = {stdDev.toFixed(3)}
      </div>
    </GlassPanel>
  );
}

/* ═══════════════════ MAIN WUXING SECTION ═══════════════════ */

export default function WuxingSection({ weights, onWeightsChange }: Props) {
  const sectionRef = useRef<HTMLDivElement>(null);

  /* Balance index: 100 - (σ/avg × 100) */
  const values = [weights.metal, weights.wood, weights.water, weights.fire, weights.earth];
  const mean = values.reduce((a, b) => a + b, 0) / values.length || 0.001;
  const stdDev = Math.sqrt(values.reduce((sq, n) => sq + Math.pow(n - mean, 2), 0) / values.length);
  const balanceIndex = Math.max(0, 100 - (stdDev / mean) * 100);

  const handleToggle = (key: keyof WuxingWeights) => {
    onWeightsChange({
      ...weights,
      [key]: weights[key] > 0 ? 0 : 0.20,
    });
  };

  const wuxingRef = useGsapScroll(({ scope }) => {
    if (!scope) return;
    gsap.from(scope.querySelectorAll('.wuxing-reveal'), {
      y: 60,
      opacity: 0,
      duration: 0.6,
      stagger: 0.08,
      ease: 'power3.out',
      scrollTrigger: {
        trigger: scope,
        start: 'top 80%',
        toggleActions: 'play none none none',
      },
    });
  });

  /* Merge refs */
  const mergedRef = (el: HTMLDivElement | null) => {
    sectionRef.current = el;
    (wuxingRef as React.MutableRefObject<HTMLDivElement | null>).current = el;
  };

  return (
    <section
      ref={mergedRef}
      className="relative w-full"
      style={{ backgroundColor: 'var(--spectrum-void)', paddingTop: 128, paddingBottom: 128 }}
    >
      {/* Background decoration */}
      <div className="absolute inset-0 flex items-center justify-center opacity-[0.05] pointer-events-none">
        <img src="/wuxing-diagram.png" alt="" className="max-w-[500px] w-full object-contain" />
      </div>

      <div className="w-full max-w-[1440px] mx-auto px-6 md:px-12 relative z-10">
        {/* Section header */}
        <div className="mb-12 text-center">
          <AuthorityReveal>
            <span className="text-label font-noto-sans block mb-2" style={{ color: 'var(--dragon-gold)' }}>
              五行定基 · Wuxing System
            </span>
          </AuthorityReveal>
          <AuthorityReveal delay={100}>
            <h2 className="text-h1 font-noto-serif mb-4" style={{ color: 'var(--spectrum-peak)' }}>
              金 · 木 · 水 · 火 · 土
            </h2>
          </AuthorityReveal>
          <AuthorityReveal delay={200}>
            <p className="text-body-lg font-noto-sans max-w-[700px] mx-auto" style={{ color: 'var(--spectrum-medium)' }}>
              五行平衡指数 = 100 - (σ/avg × 100)。五行相生相克，权重此消彼长，但总在规矩之内。
            </p>
          </AuthorityReveal>
        </div>

        {/* Pentagon diagram */}
        <div className="wuxing-reveal flex justify-center mb-12">
          <WuxingPentagon weights={weights} onToggle={handleToggle} />
        </div>

        {/* Balance score */}
        <div className="wuxing-reveal text-center mb-12">
          <motion.div
            initial={{ opacity: 0, scale: 0.8 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] as [number, number, number, number] }}
          >
            <span
              className="font-jetbrain tabular-nums"
              style={{
                fontSize: 'clamp(64px, 10vw, 120px)',
                fontWeight: 700,
                color: balanceIndex > 80 ? 'var(--dragon-green)' : balanceIndex > 50 ? 'var(--dragon-yellow)' : 'var(--dragon-red)',
                lineHeight: 1,
              }}
            >
              {balanceIndex.toFixed(1)}
            </span>
            <h3 className="text-h3 font-noto-serif mt-2" style={{ color: 'var(--spectrum-peak)' }}>
              五行平衡指数
            </h3>
            <p className="text-code font-jetbrain mt-1" style={{ color: 'var(--spectrum-dim)' }}>
              100 - (σ/avg × 100) = {balanceIndex.toFixed(1)}%
            </p>
            <div
              className="inline-flex items-center gap-2 mt-3 px-3 py-1 rounded-full text-label"
              style={{
                backgroundColor: balanceIndex > 80 ? 'rgba(0,200,83,0.15)' : 'rgba(255,61,0,0.15)',
                color: balanceIndex > 80 ? 'var(--dragon-green)' : 'var(--dragon-red)',
              }}
            >
              {balanceIndex > 80 ? '✓ 五行平衡' : '✗ 失衡警告'}
            </div>
          </motion.div>
        </div>

        {/* Element detail cards */}
        <div className="wuxing-reveal flex flex-wrap justify-center gap-4 mb-12">
          {ELEMENTS.map((el) => (
            <ElementCard
              key={el.key}
              element={el}
              weight={weights[el.key]}
              onToggle={() => handleToggle(el.key)}
            />
          ))}
        </div>

        {/* Sigma/avg chart */}
        <div className="wuxing-reveal">
          <SigmaBarChart weights={weights} />
        </div>
      </div>
    </section>
  );
}
