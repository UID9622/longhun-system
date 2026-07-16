import { useRef, useState, useEffect } from 'react';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { motion } from 'framer-motion';
import GlassPanel from '@/components/GlassPanel';
import AuthorityReveal from '@/components/AuthorityReveal';
import { useGsapScroll } from './useGsapScroll';

interface SancaiWeights {
  heaven: number;
  human: number;
  earth: number;
}

interface Props {
  weights: SancaiWeights;
  balanceCoeff: number;
  balanceIndex: number;
}

/* ─────────── Animated number that counts up ─────────── */
function useCountUp(target: number, duration = 1200, decimals = 3) {
  const [value, setValue] = useState(0);
  useEffect(() => {
    const start = Date.now();
    let raf: number;
    const tick = () => {
      const p = Math.min((Date.now() - start) / duration, 1);
      const eased = 1 - Math.pow(1 - p, 3);
      setValue(eased * target);
      if (p < 1) raf = requestAnimationFrame(tick);
    };
    raf = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(raf);
  }, [target, duration]);
  return decimals === 0 ? Math.round(value) : value.toFixed(decimals);
}

/* ─────────── Pyramid level component ─────────── */
function PyramidLevel({
  label,
  sublabel,
  weight,
  color,
  width,
  isCenter,
  delay,
}: {
  label: string;
  sublabel: string;
  weight: number;
  color: string;
  width: number;
  isCenter?: boolean;
  delay: number;
}) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 40, scale: 0.9 }}
      whileInView={{ opacity: 1, y: 0, scale: 1 }}
      viewport={{ once: true }}
      transition={{ duration: 0.6, delay, ease: [0.16, 1, 0.3, 1] as [number, number, number, number] }}
      className="flex flex-col items-center gap-2"
    >
      <span className="text-label font-noto-sans" style={{ color: 'var(--spectrum-bright)' }}>
        {label}
      </span>
      <span className="text-caption font-noto-sans" style={{ color: 'var(--spectrum-dim)' }}>
        {sublabel}
      </span>

      <div
        className="relative flex flex-col items-center justify-center py-4"
        style={{
          width,
          borderRadius: isCenter ? '50%' : 8,
          border: `2px solid ${color}`,
          backgroundColor: `${color}15`,
          boxShadow: isCenter ? `0 0 30px ${color}40` : `0 0 15px ${color}20`,
        }}
      >
        {isCenter && (
          <div
            className="absolute -top-3 text-label px-2 py-0.5 rounded-full"
            style={{ backgroundColor: 'var(--dragon-green)', color: 'var(--spectrum-void)', fontSize: 10 }}
          >
            铁律 ✓
          </div>
        )}
        <span
          className="font-jetbrain tabular-nums"
          style={{ fontSize: isCenter ? 56 : 42, fontWeight: 700, color }}
        >
          {weight.toFixed(2)}
        </span>
        {/* Weight bar */}
        <div className="w-3/4 h-1.5 rounded-full overflow-hidden mt-2" style={{ backgroundColor: 'var(--spectrum-border)' }}>
          <div
            className="h-full rounded-full transition-all duration-700"
            style={{ width: `${weight * 100}%`, backgroundColor: color }}
          />
        </div>
      </div>
    </motion.div>
  );
}

/* ─────────── Calculation Panel ─────────── */
function CalculationPanel({ weights, balanceCoeff, balanceIndex }: Props) {
  const coeffStr = useCountUp(balanceCoeff, 800, 3);
  const indexStr = useCountUp(Math.min(100, balanceIndex), 800, 1);

  return (
    <GlassPanel className="p-6 w-full max-w-[320px]">
      <h3 className="text-h3 font-noto-serif mb-4" style={{ color: 'var(--spectrum-bright)' }}>
        实时计算
      </h3>
      <div className="flex flex-col gap-2 font-jetbrain text-code" style={{ color: 'var(--spectrum-dim)' }}>
        <div style={{ color: 'var(--dragon-gold)' }}>
          天 × 0.35 = {weights.heaven.toFixed(2)} × 1.0 = {(weights.heaven * 0.35).toFixed(3)}
        </div>
        <div style={{ color: 'var(--dragon-yellow)' }}>
          地 × 0.20 = {weights.earth.toFixed(2)} × 1.0 = {(weights.earth * 0.20).toFixed(3)}
        </div>
        <div style={{ color: 'var(--dragon-green)' }}>
          人 × 0.45 = {weights.human.toFixed(2)} × 1.0 = {(weights.human * 0.45).toFixed(3)}
        </div>
        <div className="border-t border-b py-2 my-1" style={{ borderColor: 'var(--glass-border)' }}>
          <div style={{ color: 'var(--spectrum-peak)' }}>
            Σ = {(weights.heaven * 0.35).toFixed(3)} + {(weights.earth * 0.20).toFixed(3)} + {(weights.human * 0.45).toFixed(3)}
          </div>
          <div style={{ color: 'var(--spectrum-peak)' }}>
            = {(weights.heaven * 0.35 + weights.earth * 0.20 + weights.human * 0.45).toFixed(3)}
          </div>
        </div>
        <div style={{ color: 'var(--spectrum-bright)' }}>
          平衡系数 = 0.35×{weights.heaven.toFixed(2)} + 0.20×{weights.earth.toFixed(2)} + 0.45×{weights.human.toFixed(2)}
        </div>
        <div style={{ color: 'var(--dragon-green)', fontSize: 'clamp(20px, 2.5vw, 32px)', fontWeight: 700 }}>
          = {coeffStr}
        </div>
      </div>

      {/* Progress ring */}
      <div className="mt-4 flex items-center gap-3">
        <svg width="48" height="48" viewBox="0 0 48 48">
          <circle cx="24" cy="24" r="20" fill="none" stroke="var(--spectrum-border)" strokeWidth="3" />
          <circle
            cx="24" cy="24" r="20" fill="none"
            stroke="var(--dragon-green)" strokeWidth="3"
            strokeDasharray={`${2 * Math.PI * 20}`}
            strokeDashoffset={`${2 * Math.PI * 20 * (1 - Math.min(balanceIndex, 100) / 100 * 0.8)}`}
            strokeLinecap="round"
            transform="rotate(-90 24 24)"
            style={{ transition: 'stroke-dashoffset 0.5s ease' }}
          />
        </svg>
        <div>
          <div className="text-label font-noto-sans" style={{ color: 'var(--spectrum-dim)' }}>
            平衡指数
          </div>
          <div className="font-jetbrain tabular-nums text-h3" style={{ color: 'var(--dragon-green)' }}>
            {indexStr}%
          </div>
        </div>
      </div>
    </GlassPanel>
  );
}

/* ─────────── Iron Law Badge ─────────── */
function IronLawBadge({ humanWeight }: { humanWeight: number }) {
  const satisfied = humanWeight >= 0.34;
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.8 }}
      whileInView={{ opacity: 1, scale: 1 }}
      viewport={{ once: true }}
      transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] as [number, number, number, number] }}
    >
      <GlassPanel
        className="p-6 text-center"
        style={{ border: '2px solid var(--dragon-gold)' }}
      >
        <h3 className="text-h2 font-noto-serif mb-2" style={{ color: 'var(--dragon-gold)' }}>
          铁律
        </h3>
        <p className="text-body font-noto-sans mb-2" style={{ color: 'var(--spectrum-bright)' }}>
          Human ≥ 0.34 — 人永远不低于34%
        </p>
        <div
          className="text-body font-noto-sans inline-flex items-center gap-2 px-3 py-1 rounded-full"
          style={{
            color: satisfied ? 'var(--dragon-green)' : 'var(--dragon-red)',
            backgroundColor: satisfied ? 'rgba(0,200,83,0.15)' : 'rgba(255,61,0,0.15)',
          }}
        >
          {satisfied ? '✓' : '✗'} 当前: Human = {humanWeight.toFixed(2)} {satisfied ? '满足' : '违反'}
        </div>
      </GlassPanel>
    </motion.div>
  );
}

/* ═══════════════════ MAIN SANCAI SECTION ═══════════════════ */

export default function SancaiSection({ weights, balanceCoeff, balanceIndex }: Props) {
  const sectionRef = useRef<HTMLDivElement>(null);
  const pyramidRef = useRef<HTMLDivElement>(null);

  /* Pin the section via a dedicated useEffect (not part of gsap context) */
  useEffect(() => {
    if (!sectionRef.current) return;
    const st = ScrollTrigger.create({
      trigger: sectionRef.current,
      start: 'top top',
      end: '+=200%',
      pin: true,
      scrub: 0.5,
    });
    return () => { st.kill(); };
  }, []);

  /* Stagger reveal via our local hook */
  const sancaiRef = useGsapScroll(({ scope }) => {
    if (!scope) return;
    const pyr = scope.querySelector('.pyramid-ref');
    if (pyr) {
      const levels = pyr.querySelectorAll('.pyramid-level');
      gsap.from(levels, {
        y: 60,
        opacity: 0,
        scale: 0.9,
        stagger: 0.15,
        duration: 0.6,
        ease: 'power3.out',
        scrollTrigger: {
          trigger: scope,
          start: 'top 60%',
          toggleActions: 'play none none none',
        },
      });
    }
  });

  /* Merge refs */
  const mergedRef = (el: HTMLDivElement | null) => {
    sectionRef.current = el;
    pyramidRef.current = el;
    (sancaiRef as React.MutableRefObject<HTMLDivElement | null>).current = el;
  };

  return (
    <section
      ref={mergedRef}
      className="relative w-full min-h-[100dvh] flex items-center pyramid-ref"
      style={{ backgroundColor: 'var(--spectrum-shadow)', paddingTop: 128, paddingBottom: 128 }}
    >
      {/* Background pyramid decoration */}
      <div
        className="absolute inset-0 flex items-center justify-center opacity-[0.07] pointer-events-none select-none"
      >
        <img
          src="/sancai-pyramid.png"
          alt=""
          className="max-w-[600px] w-full object-contain"
        />
      </div>

      <div className="w-full max-w-[1440px] mx-auto px-6 md:px-12 relative z-10">
        {/* Section header */}
        <div className="mb-12">
          <AuthorityReveal>
            <span className="text-label font-noto-sans block mb-2" style={{ color: 'var(--dragon-gold)' }}>
              三才赋权 · Sancai Weights
            </span>
          </AuthorityReveal>
          <AuthorityReveal delay={100}>
            <h2 className="text-h1 font-noto-serif mb-4" style={{ color: 'var(--spectrum-peak)' }}>
              天 · 地 · 人
            </h2>
          </AuthorityReveal>
          <AuthorityReveal delay={200}>
            <GlassPanel className="inline-block px-4 py-2">
              <span className="text-code font-jetbrain" style={{ color: 'var(--spectrum-dim)' }}>
                Heaven × 0.35 + Earth × 0.20 + Human × 0.45 = Balance Coefficient
              </span>
            </GlassPanel>
          </AuthorityReveal>
        </div>

        {/* Pyramid + Calculation */}
        <div className="flex flex-col lg:flex-row items-center justify-center gap-12 lg:gap-16">
          {/* Pyramid */}
          <div ref={pyramidRef} className="flex flex-col items-center gap-6">
            <div className="pyramid-level">
              <PyramidLevel
                label="天 · Heaven"
                sublabel="战略层"
                weight={weights.heaven}
                color="#FFD700"
                width={200}
                delay={0.15}
              />
            </div>
            <div className="pyramid-level">
              <PyramidLevel
                label="人 · Human · 决策层"
                sublabel="核心层"
                weight={weights.human}
                color="#00C853"
                width={260}
                isCenter
                delay={0.30}
              />
            </div>
            <div className="pyramid-level">
              <PyramidLevel
                label="地 · Earth · 基础层"
                sublabel="基础层"
                weight={weights.earth}
                color="#FFD600"
                width={360}
                delay={0.45}
              />
            </div>

            {/* Connecting energy particles (decorative) */}
            <div className="absolute inset-0 pointer-events-none overflow-hidden">
              {[...Array(6)].map((_, i) => (
                <motion.div
                  key={i}
                  className="absolute w-1 h-1 rounded-full"
                  style={{ backgroundColor: 'var(--dragon-gold)' }}
                  animate={{
                    y: [0, -200, 0],
                    x: [0, (i % 2 === 0 ? 30 : -30), 0],
                    opacity: [0, 1, 0],
                  }}
                  transition={{
                    duration: 3 + i * 0.5,
                    repeat: Infinity,
                    delay: i * 0.4,
                    ease: 'easeInOut',
                  }}
                  initial={{ left: `${30 + i * 8}%`, bottom: '20%' }}
                />
              ))}
            </div>
          </div>

          {/* Right side: Calculation + Iron Law */}
          <div className="flex flex-col gap-6">
            <CalculationPanel
              weights={weights}
              balanceCoeff={balanceCoeff}
              balanceIndex={balanceIndex}
            />
            <IronLawBadge humanWeight={weights.human} />
          </div>
        </div>
      </div>
    </section>
  );
}
