import { useState, useEffect, useRef, useCallback, memo } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import {
  Lock,
  Eye,
  ChevronDown,
  ChevronUp,
  Sparkles,
  CheckCircle2,
  Bot,
} from 'lucide-react';
import GlassPanel from '@/components/GlassPanel';
import AuthorityReveal from '@/components/AuthorityReveal';
import {
  IMMUTABLE_COLORS,
  COUNTRIES,
  FULL_PALETTES,
  TABLE_ROWS,
  DOCTRINE_CHARS,
  DOCTRINE_ORBS,
} from './comparison/data';
import type { CountryData } from './comparison/data';

gsap.registerPlugin(ScrollTrigger);

/* ─────────────────────── Animation Easing ─────────────────────── */
const EASE = [0.16, 1, 0.3, 1] as [number, number, number, number];

/* ─────────────────────── Color Pulse Class Helper ─────────────────────── */
function getPulseAnimation(hex: string): string {
  switch (hex.toUpperCase()) {
    case '#00C853': return 'animate-color-pulse-green';
    case '#FF3D00': return 'animate-color-pulse-red';
    case '#FFD600': return 'animate-color-pulse-yellow';
    case '#FFD700': return 'animate-color-pulse-gold';
    default: return '';
  }
}

/* ═══════════════════════════════════════════════════════════════
   Section 1 — Hero: 万国同源 · 五色不变
   ═══════════════════════════════════════════════════════════════ */
function HeroSection() {
  const sectionRef = useRef<HTMLDivElement>(null);
  const titleRef = useRef<HTMLHeadingElement>(null);

  useEffect(() => {

    if (!titleRef.current) return;
    const chars = titleRef.current.querySelectorAll('.hero-char');
    gsap.from(chars, {
      y: 60,
      opacity: 0,
      duration: 0.5,
      stagger: 0.08,
      ease: 'power3.out',
      scrollTrigger: {
        trigger: sectionRef.current,
        start: 'top 80%',
        once: true,
      },
    });
  
    return () => { ScrollTrigger.getAll().forEach(t => t.kill()); };
  }, []);

  const titleText = '万国同源 · 五色不变';
  const titleChars = titleText.split('');

  return (
    <section
      ref={sectionRef}
      className="relative flex flex-col items-center justify-center px-6 md:px-12 text-center"
      style={{
        minHeight: '55vh',
        backgroundColor: 'var(--spectrum-void)',
      }}
    >
      {/* Breadcrumb */}
      <AuthorityReveal delay={0}>
        <div
          className="text-label mb-6"
          style={{ color: 'var(--spectrum-dim)', fontFamily: 'JetBrains Mono, monospace' }}
        >
          龙魂生态 / 各国色卡
        </div>
      </AuthorityReveal>

      {/* Title with per-character animation */}
      <h1
        ref={titleRef}
        className="text-hero font-noto-serif mb-8"
        style={{ color: 'var(--spectrum-peak)', lineHeight: 1.2 }}
      >
        {titleChars.map((char, i) => (
          <span key={i} className="hero-char inline-block">
            {char === ' ' ? '\u00A0' : char}
          </span>
        ))}
      </h1>

      {/* Doctrine statement */}
      <AuthorityReveal delay={600} className="max-w-[720px]">
        <p
          className="text-body-lg font-noto-sans mb-2"
          style={{
            color: 'var(--spectrum-medium)',
            lineHeight: 2.0,
            textAlign: 'center',
          }}
        >
          一个基础，万国同源。五主色不动，各国可增。机器识别出色卡差异，但人眼永远习惯这五种颜色。
        </p>
        <p
          className="text-h3 font-noto-serif mt-4"
          style={{ color: 'var(--dragon-gold)', textAlign: 'center' }}
        >
          什么叫做权威？这叫做规矩，这叫做不动点。
        </p>
      </AuthorityReveal>

      {/* Base + Extension visual diagram */}
      <AuthorityReveal delay={900} className="mt-10">
        <div className="flex flex-col items-center gap-4">
          <div className="flex items-center gap-6 flex-wrap justify-center">
            {/* Immutable colors */}
            <div className="flex flex-col items-center gap-2">
              <span
                className="text-label"
                style={{ color: 'var(--dragon-gold)' }}
              >
                不动点五主色
              </span>
              <div className="flex items-center gap-2">
                {IMMUTABLE_COLORS.map((c) => (
                  <div key={c.hex} className="relative">
                    <div
                      className={`rounded-full ${getPulseAnimation(c.hex)}`}
                      style={{
                        width: 20,
                        height: 20,
                        backgroundColor: c.hex,
                        border: c.hex === '#1A1A2E' ? '1px solid var(--spectrum-border)' : 'none',
                      }}
                    />
                    <Lock
                      size={8}
                      className="absolute -top-1 -right-1"
                      style={{ color: 'var(--dragon-gold)' }}
                    />
                  </div>
                ))}
              </div>
            </div>

            {/* Plus symbol */}
            <span className="text-h2 font-noto-serif" style={{ color: 'var(--dragon-gold)' }}>
              +
            </span>

            {/* Extension colors */}
            <div className="flex flex-col items-center gap-2">
              <span
                className="text-label"
                style={{ color: 'var(--spectrum-dim)' }}
              >
                各国扩展色
              </span>
              <div className="flex items-center gap-2">
                {COUNTRIES.map((country) => (
                  <div
                    key={country.id}
                    className="rounded-full"
                    style={{
                      width: 20,
                      height: 20,
                      backgroundColor: country.extensions[0].hex,
                      border: '1px solid var(--spectrum-border)',
                    }}
                  />
                ))}
              </div>
            </div>
          </div>

          {/* Equals */}
          <span className="text-label mt-2" style={{ color: 'var(--spectrum-dim)' }}>
            = 完整色卡
          </span>
        </div>
      </AuthorityReveal>
    </section>
  );
}

/* ═══════════════════════════════════════════════════════════════
   Section 2 — Country Palette Comparison Grid
   ═══════════════════════════════════════════════════════════════ */

const tabColors: Record<string, string> = {
  china: '#DE2910',
  japan: '#FFB7C5',
  eu: '#003399',
  us: '#3C3B6E',
};

const CountryFlag = memo(function CountryFlag({ country }: { country: CountryData }) {
  return (
    <div
      className="w-12 h-12 rounded-lg bg-cover bg-no-repeat flex-shrink-0"
      style={{
        backgroundImage: 'url(/country-flags-sprite.png)',
        backgroundPosition: country.flagBgPos,
        backgroundSize: '400% 100%',
        border: '1px solid var(--spectrum-border)',
      }}
    />
  );
});

const PaletteStrip = memo(function PaletteStrip({
  colors,
  isExpanded = false,
}: {
  colors: string[];
  isExpanded?: boolean;
}) {
  return (
    <div
      className="w-full flex overflow-hidden"
      style={{
        height: isExpanded ? 40 : 32,
        borderRadius: 8,
        border: '1px solid var(--spectrum-border)',
      }}
    >
      {colors.map((hex, i) => {
        const isImmutable = i < 5;
        return (
          <div
            key={`${hex}-${i}`}
            className="flex-1 flex items-center justify-center transition-all duration-300"
            style={{
              backgroundColor: hex,
              boxShadow: isImmutable ? 'inset 0 0 0 1px rgba(255,215,0,0.3)' : 'none',
            }}
          >
            {isExpanded && (
              <span
                className="text-[9px] font-jetbrain hidden md:block"
                style={{
                  color: hex === '#1A1A2E' || hex === '#3C3B6E' || hex === '#4B0082' || hex === '#003399'
                    ? 'rgba(255,255,255,0.5)'
                    : 'rgba(0,0,0,0.4)',
                  fontFamily: 'JetBrains Mono, monospace',
                }}
              >
                {hex}
              </span>
            )}
          </div>
        );
      })}
    </div>
  );
});

function CountryCard({
  country,
  isFocused,
  isDimmed,
  onClick,
}: {
  country: CountryData;
  isFocused: boolean;
  isDimmed: boolean;
  onClick: () => void;
}) {
  const [expanded, setExpanded] = useState(false);
  const fullPalette = FULL_PALETTES[country.id];

  return (
    <motion.div
      layout
      onClick={() => {
        setExpanded(!expanded);
        onClick();
      }}
      whileHover={{ scale: 1.02, rotateX: 1, rotateY: 1 }}
      transition={{ duration: 0.3, ease: EASE }}
      className="cursor-pointer"
      style={{
        opacity: isDimmed ? 0.6 : 1,
        boxShadow: isFocused
          ? `0 0 30px ${country.primaryColor}33, 0 8px 32px rgba(0,0,0,0.4)`
          : '0 8px 32px rgba(0,0,0,0.4)',
        transformStyle: 'preserve-3d',
        perspective: 1000,
      }}
    >
      <GlassPanel
        className="relative overflow-hidden"
        style={{
          minHeight: 520,
          borderTop: `4px solid ${country.primaryColor}`,
          borderRadius: 16,
        }}
      >
        <div className="p-6 flex flex-col h-full">
          {/* Header */}
          <div className="flex items-center gap-4 mb-6">
            <CountryFlag country={country} />
            <div>
              <h3
                className="text-h2 font-noto-serif"
                style={{ color: 'var(--spectrum-peak)' }}
              >
                {country.nameCn}
              </h3>
              <span
                className="text-label"
                style={{ color: 'var(--spectrum-dim)' }}
              >
                {country.nameEn}
              </span>
            </div>
          </div>

          {/* Label */}
          <div
            className="text-label mb-4 px-3 py-1.5 rounded-full self-start"
            style={{
              backgroundColor: `${country.primaryColor}22`,
              color: country.primaryColor,
            }}
          >
            {country.label}
          </div>

          {/* Immutable Colors Section */}
          <div className="mb-2">
            <div className="flex items-center gap-2 mb-3">
              <Lock size={12} style={{ color: 'var(--dragon-gold)' }} />
              <span
                className="text-label"
                style={{ color: 'var(--dragon-gold)' }}
              >
                不动点五主色
              </span>
            </div>
            <div className="flex gap-2 flex-wrap">
              {IMMUTABLE_COLORS.map((c) => (
                <div key={c.hex} className="flex flex-col items-center gap-1">
                  <div
                    className={`rounded-lg ${getPulseAnimation(c.hex)}`}
                    style={{
                      width: 56,
                      height: 56,
                      backgroundColor: c.hex,
                      border: c.hex === '#1A1A2E' ? '1px solid var(--spectrum-border)' : 'none',
                      boxShadow: `inset 0 0 0 1px var(--dragon-gold)`,
                    }}
                  />
                  <span
                    className="text-[10px] font-jetbrain"
                    style={{ color: 'var(--spectrum-dim)', fontFamily: 'JetBrains Mono, monospace' }}
                  >
                    {c.hex}
                  </span>
                </div>
              ))}
            </div>
            <p
              className="text-caption mt-2 flex items-center gap-1"
              style={{ color: 'var(--dragon-green)', fontFamily: 'JetBrains Mono, monospace' }}
            >
              <CheckCircle2 size={11} /> 五主色与全球版本完全一致
            </p>
          </div>

          {/* Divider */}
          <div
            className="w-full my-4"
            style={{ height: 1, backgroundColor: 'var(--glass-border)' }}
          />

          {/* Extension Colors Section */}
          <div className="mb-4">
            <div className="flex items-center gap-2 mb-3">
              <Sparkles size={12} style={{ color: country.primaryColor }} />
              <span
                className="text-label"
                style={{ color: country.primaryColor }}
              >
                {country.nameCn}扩展色
              </span>
            </div>
            <div className="flex gap-4 flex-wrap">
              {country.extensions.map((ext) => (
                <div key={ext.hex} className="flex flex-col gap-1 flex-1 min-w-[120px]">
                  <div
                    className="rounded-lg"
                    style={{
                      width: 80,
                      height: 80,
                      backgroundColor: ext.hex,
                      border: '1px solid var(--spectrum-border)',
                    }}
                  />
                  <span
                    className="text-label mt-1"
                    style={{ color: 'var(--spectrum-peak)' }}
                  >
                    {ext.name}
                  </span>
                  <span
                    className="text-caption"
                    style={{
                      color: 'var(--spectrum-dim)',
                      fontFamily: 'JetBrains Mono, monospace',
                    }}
                  >
                    {ext.hex}
                  </span>
                  <span
                    className="text-caption"
                    style={{ color: 'var(--spectrum-medium)' }}
                  >
                    {ext.tag}
                  </span>
                  <p
                    className="text-[10px] leading-relaxed mt-1"
                    style={{ color: 'var(--spectrum-dim)' }}
                  >
                    {ext.description}
                  </p>
                </div>
              ))}
            </div>
          </div>

          {/* Complete Palette Strip */}
          <div className="mt-auto">
            <PaletteStrip colors={fullPalette} isExpanded={expanded} />
          </div>

          {/* Expand hint */}
          <div className="flex items-center justify-center gap-1 mt-3">
            {expanded ? (
              <ChevronUp size={14} style={{ color: 'var(--spectrum-dim)' }} />
            ) : (
              <ChevronDown size={14} style={{ color: 'var(--spectrum-dim)' }} />
            )}
            <span
              className="text-caption"
              style={{ color: 'var(--spectrum-dim)', fontFamily: 'JetBrains Mono, monospace' }}
            >
              {expanded ? '收起' : '展开完整色卡'}
            </span>
          </div>
        </div>
      </GlassPanel>
    </motion.div>
  );
}

function CountryGridSection() {
  const [activeTab, setActiveTab] = useState<string | null>(null);
  const sectionRef = useRef<HTMLDivElement>(null);
  const cardsRef = useRef<HTMLDivElement>(null);

  const handleTabClick = useCallback((id: string) => {
    setActiveTab((prev) => (prev === id ? null : id));
  }, []);

  useEffect(() => {

    if (!cardsRef.current) return;
    const cards = cardsRef.current.querySelectorAll('.country-card-wrapper');
    gsap.from(cards, {
      y: 80,
      opacity: 0,
      rotateX: 10,
      duration: 0.6,
      stagger: 0.15,
      ease: 'power3.out',
      scrollTrigger: {
        trigger: cardsRef.current,
        start: 'top 85%',
        once: true,
      },
    });
  
    return () => { ScrollTrigger.getAll().forEach(t => t.kill()); };
  }, []);

  return (
    <section
      ref={sectionRef}
      className="w-full px-6 md:px-12"
      style={{
        backgroundColor: 'var(--spectrum-shadow)',
        paddingTop: 128,
        paddingBottom: 128,
      }}
    >
      <div className="max-w-[1440px] mx-auto">
        {/* Country Selector Tabs */}
        <AuthorityReveal>
          <div
            className="flex justify-center mb-12"
            style={{ borderBottom: '1px solid var(--spectrum-border)' }}
          >
            <div className="flex">
              {COUNTRIES.map((country) => {
                const isActive = activeTab === country.id;
                return (
                  <motion.button
                    key={country.id}
                    onClick={() => handleTabClick(country.id)}
                    whileHover={{ y: -2 }}
                    transition={{ duration: 0.2 }}
                    className="px-6 md:px-8 py-4 text-label font-noto-sans relative cursor-pointer"
                    style={{
                      color: isActive ? 'var(--spectrum-peak)' : 'var(--spectrum-dim)',
                      borderBottom: isActive
                        ? `3px solid ${tabColors[country.id]}`
                        : '3px solid transparent',
                      transition: 'all 0.3s ease',
                    }}
                  >
                    {country.flagEmoji} {country.nameCn} {country.nameEn}
                  </motion.button>
                );
              })}
            </div>
          </div>
        </AuthorityReveal>

        {/* Country Cards Grid */}
        <div
          ref={cardsRef}
          className="grid grid-cols-1 md:grid-cols-2 gap-6"
        >
          {COUNTRIES.map((country) => (
            <div key={country.id} className="country-card-wrapper">
              <CountryCard
                country={country}
                isFocused={activeTab === country.id}
                isDimmed={activeTab !== null && activeTab !== country.id}
                onClick={() => handleTabClick(country.id)}
              />
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

/* ═══════════════════════════════════════════════════════════════
   Section 3 — Machine vs Human Recognition
   ═══════════════════════════════════════════════════════════════ */

const MachineStrip = memo(function MachineStrip({
  countryId,
  countryName,
}: {
  countryId: string;
  countryName: string;
}) {
  const palette = FULL_PALETTES[countryId];
  const [typed, setTyped] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => setTyped(true), 800);
    return () => clearTimeout(timer);
  }, []);

  return (
    <div className="mb-4">
      <div className="flex items-center gap-2 mb-2">
        <span
          className="text-label"
          style={{ color: 'var(--spectrum-medium)' }}
        >
          {countryName}
        </span>
      </div>
      <div
        className="w-full flex overflow-hidden mb-2"
        style={{ height: 24, borderRadius: 4, border: '1px solid var(--spectrum-border)' }}
      >
        {palette.map((hex, i) => (
          <motion.div
            key={i}
            className="flex-1"
            initial={{ scaleX: 0 }}
            animate={{ scaleX: 1 }}
            transition={{ delay: i * 0.03, duration: 0.3, ease: EASE }}
            style={{
              backgroundColor: hex,
              transformOrigin: 'left',
            }}
          />
        ))}
      </div>
      <AnimatePresence>
        {typed && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            transition={{ duration: 0.4 }}
            className="text-caption flex flex-col gap-0.5 pl-1"
            style={{ color: 'var(--spectrum-dim)', fontFamily: 'JetBrains Mono, monospace' }}
          >
            <span>识别到 7 个色块</span>
            <span style={{ color: 'var(--dragon-green)' }}>不动点匹配: 5/5 ✓</span>
            <span>扩展色: 2 (新)</span>
            <span>ΔE max: &lt; 0.5</span>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
});

const HumanStrip = memo(function HumanStrip({
  countryId,
  countryName,
}: {
  countryId: string;
  countryName: string;
}) {
  const palette = FULL_PALETTES[countryId];
  const [showBlur, setShowBlur] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => setShowBlur(true), 1200);
    return () => clearTimeout(timer);
  }, []);

  return (
    <div className="mb-4">
      <div className="flex items-center gap-2 mb-2">
        <span
          className="text-label"
          style={{ color: 'var(--spectrum-medium)' }}
        >
          {countryName}
        </span>
      </div>
      <div
        className="w-full flex overflow-hidden mb-2 relative"
        style={{ height: 24, borderRadius: 4, border: '1px solid var(--spectrum-border)' }}
      >
        {palette.map((hex, i) => {
          const isImmutable = i < 5;
          return (
            <motion.div
              key={i}
              className="flex-1 relative"
              initial={{ scaleX: 0 }}
              animate={{ scaleX: 1 }}
              transition={{ delay: i * 0.03, duration: 0.3, ease: EASE }}
              style={{
                backgroundColor: hex,
                transformOrigin: 'left',
              }}
            >
              {/* Blur overlay on extension colors */}
              {!isImmutable && (
                <motion.div
                  className="absolute inset-0"
                  initial={{ backdropFilter: 'blur(0px)' }}
                  animate={{
                    backdropFilter: showBlur ? 'blur(2px)' : 'blur(0px)',
                  }}
                  transition={{ duration: 0.5 }}
                  style={{
                    backgroundColor: showBlur ? 'rgba(10,10,15,0.3)' : 'transparent',
                  }}
                />
              )}
            </motion.div>
          );
        })}
      </div>
      <AnimatePresence>
        {showBlur && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.4 }}
            className="text-body flex flex-col gap-0.5 pl-1"
            style={{ color: 'var(--spectrum-medium)' }}
          >
            <span>首先看到: 绿红黄黑金（五主色）</span>
            <span>其次注意到: 2个新增颜色</span>
            <span>核心印象: 这和龙魂基础色卡一致</span>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
});

function MachineVsHumanSection() {
  const sectionRef = useRef<HTMLDivElement>(null);

  return (
    <section
      ref={sectionRef}
      className="w-full px-6 md:px-12"
      style={{
        backgroundColor: 'var(--spectrum-void)',
        paddingTop: 128,
        paddingBottom: 128,
      }}
    >
      <div className="max-w-[1200px] mx-auto">
        {/* Section title */}
        <AuthorityReveal className="text-center mb-16">
          <h2
            className="text-h2 font-noto-serif"
            style={{ color: 'var(--spectrum-peak)' }}
          >
            机器 vs 人眼
          </h2>
          <p
            className="text-body mt-4"
            style={{ color: 'var(--spectrum-medium)' }}
          >
            同一组色卡，不同视角
          </p>
        </AuthorityReveal>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 relative">
          {/* VS divider */}
          <div
            className="hidden lg:flex absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 items-center justify-center z-10"
          >
            <span
              className="text-hero font-noto-serif"
              style={{ color: 'var(--spectrum-dim)', opacity: 0.3 }}
            >
              VS
            </span>
          </div>

          {/* Left — Machine Recognition */}
          <AuthorityReveal delay={0}>
            <GlassPanel className="p-6 md:p-8 h-full">
              {/* Header */}
              <div className="flex items-center gap-3 mb-6">
                <Bot size={20} style={{ color: 'var(--dragon-green)' }} />
                <h3
                  className="text-h2 font-jetbrain"
                  style={{ color: 'var(--spectrum-peak)' }}
                >
                  机器识别
                </h3>
              </div>

              <p
                className="text-body mb-6"
                style={{ color: 'var(--spectrum-medium)' }}
              >
                机器精确识别色卡差异，检测到每个国家的扩展色，生成ΔE报告
              </p>

              {/* Machine image decoration */}
              <div
                className="w-full h-32 rounded-lg bg-cover bg-center mb-6 opacity-60"
                style={{
                  backgroundImage: 'url(/machine-vision.jpg)',
                  border: '1px solid var(--spectrum-border)',
                }}
              />

              {/* Machine strips */}
              {COUNTRIES.map((c) => (
                <MachineStrip key={c.id} countryId={c.id} countryName={c.nameCn} />
              ))}

              {/* Machine conclusion */}
              <div
                className="mt-4 p-4 rounded-xl"
                style={{
                  border: '1px solid var(--dragon-green)',
                  backgroundColor: 'rgba(0, 200, 83, 0.05)',
                }}
              >
                <p
                  className="text-body font-jetbrain"
                  style={{ color: 'var(--dragon-green)', fontFamily: 'JetBrains Mono, monospace' }}
                >
                  机器结论: 四份色卡均包含完整的五主色不动点，扩展色识别正常，无异常偏移。
                </p>
              </div>
            </GlassPanel>
          </AuthorityReveal>

          {/* Right — Human Perception */}
          <AuthorityReveal delay={300}>
            <GlassPanel className="p-6 md:p-8 h-full">
              {/* Header */}
              <div className="flex items-center gap-3 mb-6">
                <Eye size={20} style={{ color: 'var(--dragon-gold)' }} />
                <h3
                  className="text-h2 font-noto-serif"
                  style={{ color: 'var(--spectrum-peak)' }}
                >
                  人眼习惯
                </h3>
              </div>

              <p
                className="text-body mb-6"
                style={{ color: 'var(--spectrum-medium)' }}
              >
                人先看到五主色，扩展色只是习惯。不动点才是规矩。
              </p>

              {/* Human perception visual */}
              <div
                className="w-full h-32 rounded-lg mb-6 flex items-center justify-center relative overflow-hidden"
                style={{
                  background: 'linear-gradient(90deg, #00C853, #FF3D00, #FFD600, #1A1A2E, #FFD700)',
                  border: '1px solid var(--spectrum-border)',
                }}
              >
                <span
                  className="text-h3 font-noto-serif relative z-10"
                  style={{
                    color: 'var(--spectrum-peak)',
                    textShadow: '0 2px 8px rgba(0,0,0,0.8)',
                  }}
                >
                  五色为先
                </span>
              </div>

              {/* Human strips */}
              {COUNTRIES.map((c) => (
                <HumanStrip key={c.id} countryId={c.id} countryName={c.nameCn} />
              ))}

              {/* Human conclusion */}
              <div
                className="mt-4 p-4 rounded-xl"
                style={{
                  border: '1px solid var(--dragon-gold)',
                  backgroundColor: 'rgba(255, 215, 0, 0.05)',
                }}
              >
                <p
                  className="text-body font-noto-serif"
                  style={{ color: 'var(--dragon-gold)' }}
                >
                  人眼结论: 无论哪国色卡，最先识别的永远是五主色。扩展色是锦上添花，不动点才是规矩。
                </p>
              </div>
            </GlassPanel>
          </AuthorityReveal>
        </div>

        {/* Fixed Point divider */}
        <AuthorityReveal delay={600} className="mt-16 text-center">
          <div
            className="inline-flex items-center gap-3 px-6 py-3 rounded-full"
            style={{
              border: '1px solid var(--dragon-gold)',
              backgroundColor: 'rgba(255, 215, 0, 0.05)',
            }}
          >
            <Lock size={16} style={{ color: 'var(--dragon-gold)' }} />
            <span
              className="text-label font-noto-serif"
              style={{ color: 'var(--dragon-gold)' }}
            >
              不动点 = 永不变更的五主色
            </span>
            <Lock size={16} style={{ color: 'var(--dragon-gold)' }} />
          </div>
        </AuthorityReveal>
      </div>
    </section>
  );
}

/* ═══════════════════════════════════════════════════════════════
   Section 4 — The Fixed Point Doctrine (不动点教义)
   ═══════════════════════════════════════════════════════════════ */

function DoctrineSection() {
  const sectionRef = useRef<HTMLDivElement>(null);
  const charsRef = useRef<HTMLDivElement>(null);
  const orbsRef = useRef<HTMLDivElement>(null);

  useEffect(() => {

    if (!charsRef.current) return;
    const chars = charsRef.current.querySelectorAll('.doctrine-char');
    gsap.from(chars, {
      y: 60,
      opacity: 0,
      duration: 0.5,
      stagger: 0.08,
      ease: 'power3.out',
      scrollTrigger: {
        trigger: charsRef.current,
        start: 'top 80%',
        once: true,
      },
    });
  
    return () => { ScrollTrigger.getAll().forEach(t => t.kill()); };
  }, []);

  useEffect(() => {

    if (!orbsRef.current) return;
    const orbs = orbsRef.current.querySelectorAll('.doctrine-orb');
    gsap.from(orbs, {
      scale: 0,
      opacity: 0,
      duration: 0.6,
      stagger: 0.1,
      ease: 'back.out(1.7)',
      scrollTrigger: {
        trigger: orbsRef.current,
        start: 'top 80%',
        once: true,
      },
    });
  
    return () => { ScrollTrigger.getAll().forEach(t => t.kill()); };
  }, []);

  return (
    <section
      ref={sectionRef}
      className="w-full px-6 md:px-12"
      style={{
        backgroundColor: 'var(--spectrum-shadow)',
        paddingTop: 128,
        paddingBottom: 128,
      }}
    >
      <div className="max-w-[800px] mx-auto flex flex-col items-center">
        {/* Immutable statement with colored characters */}
        <div ref={charsRef} className="flex flex-wrap justify-center gap-2 md:gap-4 mb-12">
          {DOCTRINE_CHARS.map((item, i) => (
            <span
              key={i}
              className="doctrine-char inline-block text-hero font-noto-serif"
              style={{
                color: item.color,
                textShadow: `0 0 40px ${item.color}4D`,
                lineHeight: 1.2,
              }}
            >
              {item.char}
            </span>
          ))}
        </div>

        {/* Doctrine paragraphs */}
        <AuthorityReveal delay={200} className="w-full">
          <p
            className="text-body-lg font-noto-sans mb-8"
            style={{ color: 'var(--spectrum-medium)', lineHeight: 2.0 }}
          >
            每一个国家的色卡都是独一无二的。中国有中国红和琉璃黄，日本有樱花粉和靛蓝，欧盟有欧盟蓝和星金黄，美国有自由蓝和勇气红。机器读取这些色卡时，能精确识别出每一组扩展色的差异。
          </p>
        </AuthorityReveal>

        <AuthorityReveal delay={400} className="w-full">
          <p
            className="text-body-lg font-noto-sans mb-8"
            style={{ color: 'var(--spectrum-medium)', lineHeight: 2.0 }}
          >
            但是，无论哪一国的色卡，前五个颜色永远是
            <span style={{ color: '#00C853' }}>绿</span>、
            <span style={{ color: '#FF3D00' }}>红</span>、
            <span style={{ color: '#FFD600' }}>黄</span>、
            <span style={{ color: '#555580' }}>黑</span>、
            <span style={{ color: '#FFD700' }}>金</span>
            。这是规矩。这五个颜色是龙魂生态的不动点，是万国同源的根基。
          </p>
        </AuthorityReveal>

        <AuthorityReveal delay={600} className="w-full">
          <p
            className="text-h3 font-noto-serif mt-8 mb-16"
            style={{
              color: 'var(--dragon-gold)',
              lineHeight: 2.0,
              textAlign: 'center',
            }}
          >
            什么叫做权威？这叫做规矩，这叫做不动点。机器可以算出色卡之间的汉明距离，但人眼永远先看到那五个颜色。权重可算，颜色不可移。这是龙魂。
          </p>
        </AuthorityReveal>

        {/* Five Immutable Color Orbs */}
        <div ref={orbsRef} className="flex flex-wrap justify-center gap-4 md:gap-6">
          {DOCTRINE_ORBS.map((orb, i) => (
            <div key={i} className="doctrine-orb flex flex-col items-center gap-3">
              <div
                className={`rounded-full flex items-center justify-center ${getPulseAnimation(orb.color)}`}
                style={{
                  width: 100,
                  height: 100,
                  backgroundColor: orb.color,
                  boxShadow: `0 0 40px ${orb.color}4D`,
                  border: orb.color === '#1A1A2E' ? '2px solid var(--spectrum-border)' : 'none',
                }}
              >
                <span
                  className="font-noto-serif text-[36px] font-bold"
                  style={{
                    color: orb.color === '#1A1A2E' ? 'var(--spectrum-dim)' : '#FFFFFF',
                    textShadow: orb.color === '#FFD600' ? '0 1px 4px rgba(0,0,0,0.5)' : 'none',
                  }}
                >
                  {orb.char}
                </span>
              </div>
              <span
                className="text-label"
                style={{ color: 'var(--spectrum-medium)' }}
              >
                {orb.label}
              </span>
            </div>
          ))}
        </div>

        {/* Subtitle */}
        <AuthorityReveal delay={800} className="mt-12">
          <p
            className="text-h3 font-noto-serif text-center"
            style={{ color: 'var(--dragon-gold)' }}
          >
            五色五规，是为权威
          </p>
        </AuthorityReveal>
      </div>
    </section>
  );
}

/* ═══════════════════════════════════════════════════════════════
   Section 5 — Color Data Table (全球色卡数据总表)
   ═══════════════════════════════════════════════════════════════ */

function DataTableSection() {
  const sectionRef = useRef<HTMLDivElement>(null);
  const tableRef = useRef<HTMLTableElement>(null);
  const [sortKey, setSortKey] = useState<string | null>(null);
  const [sortAsc, setSortAsc] = useState(true);

  const handleSort = useCallback((key: string) => {
    setSortKey((prev) => {
      if (prev === key) {
        setSortAsc((a) => !a);
        return prev;
      }
      setSortAsc(true);
      return key;
    });
  }, []);

  const sortedRows = (() => {
    if (!sortKey) return TABLE_ROWS;
    const rows = [...TABLE_ROWS];
    rows.sort((a, b) => {
      let av: string, bv: string;
      switch (sortKey) {
        case 'color': av = a.colorName; bv = b.colorName; break;
        case 'china': av = a.china; bv = b.china; break;
        case 'japan': av = a.japan; bv = b.japan; break;
        case 'eu': av = a.eu; bv = b.eu; break;
        case 'us': av = a.us; bv = b.us; break;
        case 'type': av = a.type; bv = b.type; break;
        case 'status': av = a.status; bv = b.status; break;
        default: return 0;
      }
      return sortAsc ? av.localeCompare(bv) : bv.localeCompare(av);
    });
    return rows;
  })();

  useEffect(() => {

    if (!tableRef.current) return;
    const rows = tableRef.current.querySelectorAll('.table-row');
    gsap.from(rows, {
      x: -15,
      opacity: 0,
      duration: 0.4,
      stagger: 0.05,
      ease: 'power3.out',
      scrollTrigger: {
        trigger: tableRef.current,
        start: 'top 85%',
        once: true,
      },
    });
  
    return () => { ScrollTrigger.getAll().forEach(t => t.kill()); };
  }, []);

  return (
    <section
      ref={sectionRef}
      className="w-full px-6 md:px-12"
      style={{
        backgroundColor: 'var(--spectrum-void)',
        paddingTop: 96,
        paddingBottom: 96,
      }}
    >
      <div className="max-w-[1440px] mx-auto">
        <AuthorityReveal className="mb-10">
          <h2
            className="text-h2 font-noto-serif"
            style={{ color: 'var(--spectrum-peak)' }}
          >
            全球色卡数据总表
          </h2>
        </AuthorityReveal>

        <GlassPanel className="overflow-x-auto" style={{ borderRadius: 16 }}>
          <table
            ref={tableRef}
            className="w-full min-w-[800px]"
            style={{ borderCollapse: 'collapse' }}
          >
            <thead>
              <tr
                className="text-label sticky top-0 z-10"
                style={{
                  backgroundColor: 'var(--spectrum-raise)',
                  color: 'var(--spectrum-dim)',
                }}
              >
                {[
                  { key: 'color', label: '颜色' },
                  { key: 'china', label: '中国' },
                  { key: 'japan', label: '日本' },
                  { key: 'eu', label: '欧盟' },
                  { key: 'us', label: '美国' },
                  { key: 'type', label: '类型' },
                  { key: 'status', label: '状态' },
                ].map((col) => (
                  <th
                    key={col.key}
                    onClick={() => handleSort(col.key)}
                    className="px-4 py-3 text-left cursor-pointer select-none transition-colors duration-200 hover:text-[var(--spectrum-bright)]"
                  >
                    <span className="flex items-center gap-1">
                      {col.label}
                      {sortKey === col.key && (
                        <span style={{ color: 'var(--dragon-gold)' }}>
                          {sortAsc ? '↑' : '↓'}
                        </span>
                      )}
                    </span>
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {sortedRows.map((row, idx) => (
                <tr
                  key={`${row.colorName}-${idx}`}
                  className="table-row transition-colors duration-200"
                  style={{
                    borderLeft: row.type === 'immutable'
                      ? `3px solid ${row.leftBorderColor}`
                      : '3px solid transparent',
                    borderBottom: '1px solid var(--spectrum-border)',
                  }}
                  onMouseEnter={(e) => {
                    (e.currentTarget as HTMLElement).style.backgroundColor = 'rgba(255,215,0,0.04)';
                  }}
                  onMouseLeave={(e) => {
                    (e.currentTarget as HTMLElement).style.backgroundColor = 'transparent';
                  }}
                >
                  {/* Color Name */}
                  <td className="px-4 py-3">
                    <div className="flex items-center gap-2">
                      {row.type === 'immutable' && row.hex && (
                        <div
                          className="rounded flex-shrink-0"
                          style={{
                            width: 16,
                            height: 16,
                            backgroundColor: row.hex,
                            border: row.hex === '#1A1A2E' ? '1px solid var(--spectrum-border)' : 'none',
                          }}
                        />
                      )}
                      <div className="flex flex-col">
                        <span
                          className="text-body font-noto-sans"
                          style={{ color: 'var(--spectrum-peak)' }}
                        >
                          {row.colorName}
                        </span>
                        {row.hex && (
                          <span
                            className="text-caption"
                            style={{
                              color: 'var(--spectrum-dim)',
                              fontFamily: 'JetBrains Mono, monospace',
                            }}
                          >
                            {row.hex}
                          </span>
                        )}
                      </div>
                    </div>
                  </td>

                  {/* Country columns */}
                  {(['china', 'japan', 'eu', 'us'] as const).map((col) => {
                    const val = row[col];
                    const isCheck = val === '✓';
                    return (
                      <td key={col} className="px-4 py-3">
                        {isCheck ? (
                          <span style={{ color: 'var(--dragon-green)' }}>✓</span>
                        ) : (
                          <span
                            className="text-caption"
                            style={{
                              color: 'var(--spectrum-medium)',
                              fontFamily: 'JetBrains Mono, monospace',
                            }}
                          >
                            {val}
                          </span>
                        )}
                      </td>
                    );
                  })}

                  {/* Type */}
                  <td className="px-4 py-3">
                    <span
                      className="text-label px-2 py-0.5 rounded-full"
                      style={{
                        color: row.type === 'immutable' ? 'var(--dragon-gold)' : 'var(--spectrum-dim)',
                        backgroundColor: row.type === 'immutable'
                          ? 'rgba(255, 215, 0, 0.1)'
                          : 'rgba(85, 85, 128, 0.1)',
                      }}
                    >
                      {row.type === 'immutable' ? '不动点' : '扩展'}
                    </span>
                  </td>

                  {/* Status */}
                  <td className="px-4 py-3">
                    <div className="flex items-center gap-1">
                      {row.type === 'immutable' && (
                        <Lock size={11} style={{ color: row.statusColor }} />
                      )}
                      <span
                        className="text-label"
                        style={{ color: row.statusColor }}
                      >
                        {row.status}
                      </span>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </GlassPanel>
      </div>
    </section>
  );
}

/* ═══════════════════════════════════════════════════════════════
   Main Comparison Page
   ═══════════════════════════════════════════════════════════════ */

export default function Comparison() {
  useEffect(() => {
    window.scrollTo(0, 0);
  }, []);

  return (
    <div>
      <HeroSection />
      <CountryGridSection />
      <MachineVsHumanSection />
      <DoctrineSection />
      <DataTableSection />
    </div>
  );
}
