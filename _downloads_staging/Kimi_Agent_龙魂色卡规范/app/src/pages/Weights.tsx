import { useEffect, useRef, useState, useCallback } from 'react';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { useGsapScroll } from './weights/useGsapScroll';
import GlassPanel from '@/components/GlassPanel';

gsap.registerPlugin(ScrollTrigger);
import AuthorityReveal from '@/components/AuthorityReveal';
import SancaiSection from './weights/SancaiSection';
import WuxingSection from './weights/WuxingSection';
import CalculatorSection from './weights/CalculatorSection';
import ReferenceTable from './weights/ReferenceTable';

/* ───────────────────── Live dashboard strip data ───────────────────── */

interface LivePanelData {
  label: string;
  value: string;
  color: string;
  showPulse?: boolean;
}

const livePanels: LivePanelData[] = [
  { label: '三才平衡', value: '0.973', color: '#00C853' },
  { label: '五行平衡指数', value: '97.3%', color: '#00C853' },
  { label: '铁律状态', value: '✓ Human≥0.34', color: '#00C853' },
  { label: '熔断监视', value: 'CLEAR', color: '#00C853', showPulse: true },
];

/* ───────────────────── Live Dashboard Panel ───────────────────── */

function LivePanel({ panel, index }: { panel: LivePanelData; index: number }) {
  return (
    <AuthorityReveal delay={800 + index * 100}>
      <GlassPanel
        className="px-6 py-4 min-w-[180px] flex flex-col items-center gap-1"
      >
        <span className="text-label font-noto-sans" style={{ color: 'var(--spectrum-dim)' }}>
          {panel.label}
        </span>
        <span
          className="font-jetbrain tabular-nums flex items-center gap-2"
          style={{ fontSize: 'clamp(20px, 2.5vw, 32px)', fontWeight: 700, color: panel.color }}
        >
          {panel.value}
          {panel.showPulse && (
            <span className="inline-block w-2 h-2 rounded-full animate-pulse" style={{ backgroundColor: panel.color }} />
          )}
        </span>
      </GlassPanel>
    </AuthorityReveal>
  );
}

/* ───────────────────── Status Bar ───────────────────── */

function StatusBar() {
  const [balanceScore, setBalanceScore] = useState(97.3);
  const [lastUpdate, setLastUpdate] = useState(new Date());
  const intervalRef = useRef<ReturnType<typeof setInterval> | undefined>(undefined);

  useEffect(() => {
    intervalRef.current = setInterval(() => {
      setBalanceScore((prev) => {
        const delta = (Math.random() - 0.5) * 0.4;
        const next = Math.max(95, Math.min(99.9, prev + delta));
        return Math.round(next * 10) / 10;
      });
      setLastUpdate(new Date());
    }, 2000);
    return () => clearInterval(intervalRef.current);
  }, []);

  return (
    <div className="w-full max-w-[1440px] mx-auto mb-8">
      <GlassPanel className="px-6 py-3 flex flex-wrap items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <span className="relative flex h-3 w-3">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-[var(--dragon-green)] opacity-75" />
            <span className="relative inline-flex rounded-full h-3 w-3 bg-[var(--dragon-green)]" />
          </span>
          <span className="text-label font-noto-sans" style={{ color: 'var(--dragon-gold)' }}>
            系统正常
          </span>
        </div>
        <div className="flex items-center gap-6">
          <span className="text-label font-noto-sans" style={{ color: 'var(--spectrum-dim)' }}>
            平衡系数:
          </span>
          <span className="font-jetbrain tabular-nums text-body" style={{ color: 'var(--dragon-green)', fontWeight: 700 }}>
            {balanceScore.toFixed(1)}%
          </span>
          <span className="text-caption font-jetbrain" style={{ color: 'var(--spectrum-dim)' }}>
            {lastUpdate.toLocaleTimeString('zh-CN')}
          </span>
        </div>
      </GlassPanel>
    </div>
  );
}

/* ═══════════════════════════ MAIN PAGE ═══════════════════════════ */

export default function Weights() {
  const containerRef = useRef<HTMLDivElement>(null);

  /* GSAP ScrollTrigger setup */
  const scrollContainerRef = useGsapScroll(({ scope }) => {
    if (!scope) return;

    const sections = scope.querySelectorAll('.gsap-section');
    sections.forEach((section) => {
      gsap.from(section.querySelectorAll('.gsap-reveal'), {
        y: 60,
        opacity: 0,
        duration: 0.6,
        stagger: 0.08,
        ease: 'power3.out',
        scrollTrigger: {
          trigger: section,
          start: 'top 80%',
          toggleActions: 'play none none none',
        },
      });
    });
  });

  /* Merge refs */
  const mergedRef = (el: HTMLDivElement | null) => {
    containerRef.current = el;
    (scrollContainerRef as React.MutableRefObject<HTMLDivElement | null>).current = el;
  };

  /* Sancai state for interactive pyramid */
  const [sancaiWeights, setSancaiWeights] = useState({ heaven: 0.35, human: 0.45, earth: 0.20 });
  const balanceCoeff = sancaiWeights.heaven * 0.35 + sancaiWeights.earth * 0.20 + sancaiWeights.human * 0.45;
  const balanceIndex = Math.min(100, (balanceCoeff / 0.365) * 97.3);

  /* Wuxing state */
  const [wuxingWeights, setWuxingWeights] = useState({
    metal: 0.20, wood: 0.25, water: 0.15, fire: 0.20, earth: 0.20,
  });

  const handleSancaiChange = useCallback((weights: { heaven: number; human: number; earth: number }) => {
    setSancaiWeights(weights);
  }, []);

  const handleWuxingChange = useCallback((weights: typeof wuxingWeights) => {
    setWuxingWeights(weights);
  }, []);

  return (
    <div ref={mergedRef}>
      {/* ─── Section 1: Page Header ─── */}
      <section
        className="relative min-h-[60vh] flex flex-col items-center justify-center px-6 md:px-12 pt-16"
        style={{ backgroundColor: 'var(--spectrum-void)' }}
      >
        <div className="w-full max-w-[1440px] mx-auto">
          {/* Breadcrumb */}
          <AuthorityReveal delay={0}>
            <div className="text-label font-jetbrain mb-4" style={{ color: 'var(--spectrum-dim)' }}>
              龙魂生态 / 权重面板
            </div>
          </AuthorityReveal>

          {/* Title */}
          <AuthorityReveal delay={100}>
            <h1
              className="text-hero font-noto-serif mb-2"
              style={{ color: 'var(--spectrum-peak)' }}
            >
              权重面板
            </h1>
          </AuthorityReveal>

          {/* Subtitle */}
          <AuthorityReveal delay={400}>
            <p className="text-h3 font-noto-serif mb-10" style={{ color: 'var(--dragon-gold)' }}>
              五行定基 · 三才赋权 · 一算便知
            </p>
          </AuthorityReveal>

          {/* Live dashboard strip */}
          <div className="flex flex-wrap gap-4 mb-8">
            {livePanels.map((panel, i) => (
              <LivePanel key={panel.label} panel={panel} index={i} />
            ))}
          </div>

          {/* Status bar */}
          <StatusBar />
        </div>
      </section>

      {/* ─── Section 2: 三才 Pyramid ─── */}
      <SancaiSection weights={sancaiWeights} balanceCoeff={balanceCoeff} balanceIndex={balanceIndex} />

      {/* ─── Section 3: 五行 Pentagon ─── */}
      <WuxingSection weights={wuxingWeights} onWeightsChange={handleWuxingChange} />

      {/* ─── Section 4: Interactive Calculator ─── */}
      <CalculatorSection weights={sancaiWeights} onWeightsChange={handleSancaiChange} balanceCoeff={balanceCoeff} balanceIndex={balanceIndex} />

      {/* ─── Section 5: Reference Table ─── */}
      <ReferenceTable />
    </div>
  );
}
