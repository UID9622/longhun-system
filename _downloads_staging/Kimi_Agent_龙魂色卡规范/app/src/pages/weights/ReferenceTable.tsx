import { useRef } from 'react';
import gsap from 'gsap';
import GlassPanel from '@/components/GlassPanel';
import AuthorityReveal from '@/components/AuthorityReveal';
import { useGsapScroll } from './useGsapScroll';

/* ─────────── Table Data ─────────── */

interface TableRow {
  system: string;
  dimension: string;
  weight: number;
  level: string;
  color: string;
  colorHex: string;
  ironLaw: string;
}

const rows: TableRow[] = [
  { system: '三才', dimension: '天 Heaven', weight: 0.35, level: '战略层', color: '金', colorHex: '#FFD700', ironLaw: '—' },
  { system: '三才', dimension: '人 Human', weight: 0.45, level: '决策层', color: '绿', colorHex: '#00C853', ironLaw: 'Human ≥ 0.34' },
  { system: '三才', dimension: '地 Earth', weight: 0.20, level: '基础层', color: '黄', colorHex: '#FFD600', ironLaw: '—' },
  { system: '五行', dimension: '金 Metal', weight: 0.20, level: '—', color: '白', colorHex: '#FFFFFF', ironLaw: '—' },
  { system: '五行', dimension: '木 Wood', weight: 0.25, level: '—', color: '绿', colorHex: '#00C853', ironLaw: '—' },
  { system: '五行', dimension: '水 Water', weight: 0.15, level: '—', color: '黑', colorHex: '#1A1A2E', ironLaw: '—' },
  { system: '五行', dimension: '火 Fire', weight: 0.20, level: '—', color: '红', colorHex: '#FF3D00', ironLaw: '—' },
  { system: '五行', dimension: '土 Earth', weight: 0.20, level: '—', color: '黄', colorHex: '#FFD600', ironLaw: '—' },
];

/* ─────────── Formula reference ─────────── */

const formulas = [
  { symbol: 'A', desc: '五行平衡指数', formula: 'A = 100 - (σ/avg × 100)' },
  { symbol: 'B', desc: '生克关系系数', formula: 'B = G(A→B) - R(A⇒B)' },
  { symbol: 'C', desc: '三才平衡系数', formula: 'C = Heaven×0.35 + Earth×0.20 + Human×0.45' },
  { symbol: 'D', desc: '综合权重', formula: 'D = A×0.35 + B×0.30 + C×0.35' },
];

/* ═══════════════════ MAIN REFERENCE TABLE ═══════════════════ */

export default function ReferenceTable() {
  const sectionRef = useRef<HTMLDivElement>(null);
  const tableRef = useRef<HTMLTableElement>(null);

  const tableSectionRef = useGsapScroll(({ scope }) => {
    if (!scope) return;
    const tbl = scope.querySelector('table');
    if (tbl) {
      const trs = tbl.querySelectorAll('tbody tr');
      gsap.from(trs, {
        x: -20,
        opacity: 0,
        duration: 0.4,
        stagger: 0.05,
        ease: 'power2.out',
        scrollTrigger: {
          trigger: tbl,
          start: 'top 80%',
          toggleActions: 'play none none none',
        },
      });
    }
  });

  /* Merge refs */
  const mergedRef = (el: HTMLDivElement | null) => {
    sectionRef.current = el;
    (tableSectionRef as React.MutableRefObject<HTMLDivElement | null>).current = el;
  };

  return (
    <section
      ref={mergedRef}
      className="relative w-full"
      style={{ backgroundColor: 'var(--spectrum-void)', paddingTop: 96, paddingBottom: 96 }}
    >
      <div className="w-full max-w-[1440px] mx-auto px-6 md:px-12">
        {/* Section title */}
        <AuthorityReveal>
          <h2 className="text-h2 font-noto-serif mb-8 text-center" style={{ color: 'var(--spectrum-peak)' }}>
            权重参考表
          </h2>
        </AuthorityReveal>

        {/* Formulas reference */}
        <AuthorityReveal delay={100}>
          <GlassPanel className="p-6 mb-8 max-w-[800px] mx-auto">
            <h3 className="text-label font-noto-sans mb-4" style={{ color: 'var(--dragon-gold)' }}>
              公式参考
            </h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              {formulas.map((f) => (
                <div key={f.symbol} className="flex items-start gap-2">
                  <span
                    className="text-label font-jetbrain px-2 py-0.5 rounded"
                    style={{ backgroundColor: 'var(--spectrum-raise)', color: 'var(--dragon-gold)' }}
                  >
                    {f.symbol}
                  </span>
                  <div>
                    <span className="text-caption font-noto-sans block" style={{ color: 'var(--spectrum-dim)' }}>
                      {f.desc}
                    </span>
                    <span className="text-code font-jetbrain" style={{ color: 'var(--spectrum-bright)' }}>
                      {f.formula}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </GlassPanel>
        </AuthorityReveal>

        {/* Main table */}
        <GlassPanel className="overflow-hidden">
          <div className="overflow-x-auto">
            <table ref={tableRef} className="w-full text-left">
              <thead>
                <tr style={{ backgroundColor: 'var(--spectrum-raise)' }}>
                  {['系统', '维度', '权重', '层级', '颜色', '铁律'].map((h) => (
                    <th
                      key={h}
                      className="text-label font-noto-sans px-4 py-3"
                      style={{ color: 'var(--spectrum-dim)' }}
                    >
                      {h}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {rows.map((row, i) => (
                  <tr
                    key={`${row.system}-${row.dimension}`}
                    className="transition-colors duration-200 hover:bg-[rgba(255,215,0,0.05)]"
                    style={{
                      backgroundColor: i % 2 === 0 ? 'transparent' : 'rgba(26,26,46,0.3)',
                    }}
                  >
                    <td className="px-4 py-3 text-body font-noto-sans" style={{ color: 'var(--spectrum-bright)' }}>
                      {row.system}
                    </td>
                    <td className="px-4 py-3 text-body font-noto-sans" style={{ color: 'var(--spectrum-bright)' }}>
                      {row.dimension}
                    </td>
                    <td
                      className="px-4 py-3 font-jetbrain text-code font-bold tabular-nums"
                      style={{ color: row.colorHex }}
                    >
                      {row.weight.toFixed(2)}
                    </td>
                    <td className="px-4 py-3 text-body font-noto-sans" style={{ color: 'var(--spectrum-medium)' }}>
                      {row.level}
                    </td>
                    <td className="px-4 py-3">
                      <div className="flex items-center gap-2">
                        <div
                          className="w-4 h-4 rounded-full"
                          style={{
                            backgroundColor: row.colorHex,
                            border: row.colorHex === '#1A1A2E' ? '1px solid var(--spectrum-border)' : 'none',
                          }}
                        />
                        <span className="text-caption font-noto-sans" style={{ color: 'var(--spectrum-dim)' }}>
                          {row.color}
                        </span>
                        <span className="text-caption font-jetbrain" style={{ color: 'var(--spectrum-dim)' }}>
                          {row.colorHex}
                        </span>
                      </div>
                    </td>
                    <td className="px-4 py-3">
                      {row.ironLaw === '—' ? (
                        <span className="text-body font-noto-sans" style={{ color: 'var(--spectrum-dim)' }}>
                          —
                        </span>
                      ) : (
                        <span
                          className="text-body font-noto-sans inline-flex items-center gap-1 px-2 py-0.5 rounded-full"
                          style={{ backgroundColor: 'rgba(0,200,83,0.15)', color: 'var(--dragon-green)' }}
                        >
                          ✓ {row.ironLaw}
                        </span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </GlassPanel>

        {/* 熔断条件 checklist */}
        <div className="mt-8 max-w-[800px] mx-auto">
          <AuthorityReveal delay={200}>
            <GlassPanel className="p-6">
              <h3 className="text-label font-noto-sans mb-4" style={{ color: 'var(--dragon-red)' }}>
                熔断条件检查清单
              </h3>
              <div className="flex flex-col gap-2">
                {[
                  'Human 权重 < 0.34 — 铁律违反',
                  'dr ∈ {3, 9} — 熔断触发',
                  '五行平衡指数 < 50 — 系统失衡',
                  '三才平衡系数 < 0.20 — 严重失衡',
                ].map((item, i) => (
                  <div key={i} className="flex items-center gap-3">
                    <div
                      className="w-4 h-4 rounded-full border flex items-center justify-center"
                      style={{ borderColor: 'var(--dragon-red)' }}
                    >
                      <span style={{ color: 'var(--dragon-red)', fontSize: 10 }}>✗</span>
                    </div>
                    <span className="text-body font-noto-sans" style={{ color: 'var(--spectrum-bright)' }}>
                      {item}
                    </span>
                  </div>
                ))}
              </div>
            </GlassPanel>
          </AuthorityReveal>
        </div>
      </div>
    </section>
  );
}
