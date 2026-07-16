import { useState, useEffect, useRef, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import GlassPanel from '@/components/GlassPanel';
import AuthorityReveal from '@/components/AuthorityReveal';

interface SancaiWeights {
  heaven: number;
  human: number;
  earth: number;
}

interface Props {
  weights: SancaiWeights;
  onWeightsChange: (w: SancaiWeights) => void;
  balanceCoeff: number;
  balanceIndex: number;
}

/* ─────────── Custom Slider ─────────── */

interface SliderProps {
  label: string;
  sublabel: string;
  value: number;
  color: string;
  onChange: (v: number) => void;
}

function CustomSlider({ label, sublabel, value, color, onChange }: SliderProps) {
  const trackRef = useRef<HTMLDivElement>(null);
  const isDragging = useRef(false);

  const handleUpdate = useCallback(
    (clientX: number) => {
      if (!trackRef.current) return;
      const rect = trackRef.current.getBoundingClientRect();
      const pct = Math.max(0, Math.min(1, (clientX - rect.left) / rect.width));
      onChange(Math.round(pct * 100) / 100);
    },
    [onChange]
  );

  useEffect(() => {
    const handleMove = (e: MouseEvent) => {
      if (isDragging.current) handleUpdate(e.clientX);
    };
    const handleUp = () => {
      isDragging.current = false;
    };
    window.addEventListener('mousemove', handleMove);
    window.addEventListener('mouseup', handleUp);
    return () => {
      window.removeEventListener('mousemove', handleMove);
      window.removeEventListener('mouseup', handleUp);
    };
  }, [handleUpdate]);

  return (
    <div className="w-full">
      {/* Label row */}
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center gap-2">
          <span className="text-label font-noto-sans" style={{ color: 'var(--spectrum-bright)' }}>
            {label}
          </span>
          <span className="text-caption font-noto-sans" style={{ color: 'var(--spectrum-dim)' }}>
            {sublabel}
          </span>
        </div>
        <span className="font-jetbrain text-code tabular-nums font-bold" style={{ color }}>
          {value.toFixed(2)}
        </span>
      </div>

      {/* Slider track */}
      <div
        ref={trackRef}
        className="relative w-full h-2 rounded-full cursor-pointer"
        style={{ backgroundColor: 'var(--spectrum-border)' }}
        onMouseDown={(e) => {
          isDragging.current = true;
          handleUpdate(e.clientX);
        }}
      >
        {/* Fill */}
        <div
          className="absolute top-0 left-0 h-full rounded-full pointer-events-none"
          style={{
            width: `${value * 100}%`,
            backgroundColor: color,
            boxShadow: `0 0 8px ${color}60`,
            transition: isDragging.current ? 'none' : 'width 0.1s ease',
          }}
        />
        {/* Thumb */}
        <div
          className="absolute top-1/2 -translate-y-1/2 rounded-full cursor-grab active:cursor-grabbing"
          style={{
            left: `${value * 100}%`,
            width: 24,
            height: 24,
            marginLeft: -12,
            backgroundColor: color,
            boxShadow: `0 0 12px ${color}66`,
            transition: isDragging.current ? 'none' : 'left 0.1s ease',
          }}
        />
      </div>
    </div>
  );
}

/* ─────────── Circuit Breaker Check ─────────── */

function CircuitBreakerCheck({ dr }: { dr: number }) {
  const triggered = dr === 3 || dr === 9;

  return (
    <div className="mt-3">
      <div className="flex items-center gap-2">
        <span className="text-label font-noto-sans" style={{ color: 'var(--spectrum-dim)' }}>
          熔断条件:
        </span>
        <span className="text-code font-jetbrain" style={{ color: 'var(--spectrum-bright)' }}>
          dr ∈ {'{3, 9}'}
        </span>
        <span
          className="text-label px-2 py-0.5 rounded-full"
          style={{
            backgroundColor: triggered ? 'rgba(255,61,0,0.2)' : 'rgba(0,200,83,0.15)',
            color: triggered ? 'var(--dragon-red)' : 'var(--dragon-green)',
          }}
        >
          {triggered ? '触发' : '正常'}
        </span>
      </div>

      <AnimatePresence>
        {triggered && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.3 }}
            className="overflow-hidden"
          >
            <div
              className="mt-2 px-4 py-3 rounded-xl flex items-center gap-3"
              style={{
                backgroundColor: 'rgba(255,61,0,0.15)',
                border: '1px solid rgba(255,61,0,0.4)',
              }}
            >
              <span className="text-xl">🔴</span>
              <span className="text-body font-noto-sans" style={{ color: 'var(--dragon-red)' }}>
                熔断触发 — dr = {dr}，系统进入熔断审查状态
              </span>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

/* ═══════════════════ MAIN CALCULATOR SECTION ═══════════════════ */

export default function CalculatorSection({ weights, onWeightsChange, balanceCoeff, balanceIndex }: Props) {
  const [localWeights, setLocalWeights] = useState(weights);
  const [drValue] = useState(0); /* Simulated dr value; could be derived from actual logic */
  const resultRef = useRef<HTMLDivElement>(null);

  /* Sync with parent */
  useEffect(() => {
    setLocalWeights(weights);
  }, [weights]);

  const handleChange = (key: keyof SancaiWeights, value: number) => {
    const next = { ...localWeights, [key]: value };
    setLocalWeights(next);
    onWeightsChange(next);
  };

  const handleReset = () => {
    const defaults = { heaven: 0.35, human: 0.45, earth: 0.20 };
    setLocalWeights(defaults);
    onWeightsChange(defaults);
  };

  const ironLawSatisfied = localWeights.human >= 0.34;
  const coeffColor = balanceCoeff >= 0.34 ? 'var(--dragon-green)' : balanceCoeff >= 0.20 ? 'var(--dragon-yellow)' : 'var(--dragon-red)';

  return (
    <section
      className="relative w-full"
      style={{ backgroundColor: 'var(--spectrum-shadow)', paddingTop: 96, paddingBottom: 96 }}
    >
      <div className="w-full max-w-[1440px] mx-auto px-6 md:px-12">
        {/* Section header */}
        <div className="text-center mb-12">
          <AuthorityReveal>
            <h2 className="text-h1 font-noto-serif mb-4" style={{ color: 'var(--spectrum-peak)' }}>
              交互权重计算器
            </h2>
          </AuthorityReveal>
          <AuthorityReveal delay={100}>
            <p className="text-body-lg font-noto-sans max-w-[600px] mx-auto" style={{ color: 'var(--spectrum-medium)' }}>
              调整三才权重，实时查看平衡系数。铁律不可违反。
            </p>
          </AuthorityReveal>
        </div>

        {/* Sliders */}
        <div className="max-w-[720px] mx-auto flex flex-col gap-8 mb-12">
          <AuthorityReveal delay={150}>
            <CustomSlider
              label="天 · Heaven"
              sublabel="战略层"
              value={localWeights.heaven}
              color="#FFD700"
              onChange={(v) => handleChange('heaven', v)}
            />
          </AuthorityReveal>
          <AuthorityReveal delay={300}>
            <CustomSlider
              label="人 · Human"
              sublabel="决策层"
              value={localWeights.human}
              color="#00C853"
              onChange={(v) => handleChange('human', v)}
            />
          </AuthorityReveal>
          <AuthorityReveal delay={450}>
            <CustomSlider
              label="地 · Earth"
              sublabel="基础层"
              value={localWeights.earth}
              color="#FFD600"
              onChange={(v) => handleChange('earth', v)}
            />
          </AuthorityReveal>
        </div>

        {/* Results panel */}
        <AuthorityReveal delay={600}>
          <GlassPanel className="p-8 max-w-[720px] mx-auto">
            {/* Sancai Balance */}
            <div className="mb-6">
              <h4 className="text-h3 font-noto-serif mb-3" style={{ color: 'var(--spectrum-bright)' }}>
                三才平衡系数
              </h4>
              <p className="text-code font-jetbrain mb-4" style={{ color: 'var(--spectrum-dim)' }}>
                0.35 × {localWeights.heaven.toFixed(2)} + 0.20 × {localWeights.earth.toFixed(2)} + 0.45 × {localWeights.human.toFixed(2)} = {balanceCoeff.toFixed(3)}
              </p>

              <motion.div
                ref={resultRef}
                key={balanceCoeff.toFixed(3)}
                initial={{ scale: 1.05 }}
                animate={{ scale: 1 }}
                transition={{ duration: 0.2, ease: [0.16, 1, 0.3, 1] as [number, number, number, number] }}
                className="font-jetbrain tabular-nums text-center py-4 rounded-xl"
                style={{
                  fontSize: 'clamp(36px, 5vw, 72px)',
                  fontWeight: 700,
                  color: coeffColor,
                  backgroundColor: `${coeffColor}15`,
                  border: `1px solid ${coeffColor}30`,
                }}
              >
                {balanceCoeff.toFixed(3)}
              </motion.div>

              {/* Balance index */}
              <div className="flex items-center justify-center gap-4 mt-4">
                <div className="flex items-center gap-2">
                  <svg width="36" height="36" viewBox="0 0 36 36">
                    <circle cx="18" cy="18" r="15" fill="none" stroke="var(--spectrum-border)" strokeWidth="3" />
                    <circle
                      cx="18" cy="18" r="15" fill="none"
                      stroke={balanceIndex >= 90 ? 'var(--dragon-green)' : 'var(--dragon-yellow)'}
                      strokeWidth="3"
                      strokeDasharray={`${2 * Math.PI * 15}`}
                      strokeDashoffset={`${2 * Math.PI * 15 * (1 - Math.min(balanceIndex, 100) / 100 * 0.8)}`}
                      strokeLinecap="round"
                      transform="rotate(-90 18 18)"
                      style={{ transition: 'stroke-dashoffset 0.5s ease' }}
                    />
                  </svg>
                  <span
                    className="font-jetbrain text-h3 tabular-nums"
                    style={{ color: balanceIndex >= 90 ? 'var(--dragon-green)' : 'var(--dragon-yellow)' }}
                  >
                    {Math.min(100, balanceIndex).toFixed(1)}%
                  </span>
                </div>
              </div>
            </div>

            <div className="border-t pt-6" style={{ borderColor: 'var(--glass-border)' }}>
              {/* Iron Law Check */}
              <div className="flex items-center gap-3 mb-2">
                <span className="text-label font-noto-sans" style={{ color: 'var(--spectrum-dim)' }}>
                  铁律检查:
                </span>
                <span
                  className="text-body font-noto-sans inline-flex items-center gap-2 px-3 py-1 rounded-full"
                  style={{
                    backgroundColor: ironLawSatisfied ? 'rgba(0,200,83,0.15)' : 'rgba(255,61,0,0.15)',
                    color: ironLawSatisfied ? 'var(--dragon-green)' : 'var(--dragon-red)',
                  }}
                >
                  {ironLawSatisfied ? '✓' : '✗'} Human ≥ 0.34
                </span>
              </div>

              {/* Warning banner */}
              <AnimatePresence>
                {!ironLawSatisfied && (
                  <motion.div
                    initial={{ height: 0, opacity: 0 }}
                    animate={{ height: 'auto', opacity: 1 }}
                    exit={{ height: 0, opacity: 0 }}
                    transition={{ duration: 0.3 }}
                    className="overflow-hidden"
                  >
                    <div
                      className="mt-3 px-4 py-3 rounded-xl flex items-center gap-3"
                      style={{
                        backgroundColor: 'rgba(255,61,0,0.12)',
                        border: '1px solid rgba(255,61,0,0.35)',
                      }}
                    >
                      <span className="text-xl">⚠️</span>
                      <span className="text-body font-noto-sans" style={{ color: 'var(--dragon-red)' }}>
                        铁律违反：Human权重低于0.34，系统将进入熔断审查状态
                      </span>
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>

              {/* Circuit breaker */}
              <CircuitBreakerCheck dr={drValue} />
            </div>
          </GlassPanel>
        </AuthorityReveal>

        {/* Reset button */}
        <div className="text-center mt-6">
          <motion.button
            whileHover={{ scale: 1.03 }}
            whileTap={{ scale: 0.97 }}
            onClick={handleReset}
            className="px-6 py-3 rounded-xl text-label font-noto-sans transition-colors"
            style={{
              backgroundColor: 'var(--spectrum-raise)',
              color: 'var(--spectrum-bright)',
              border: '1px solid var(--spectrum-border)',
            }}
          >
            恢复默认值
          </motion.button>
        </div>
      </div>
    </section>
  );
}
