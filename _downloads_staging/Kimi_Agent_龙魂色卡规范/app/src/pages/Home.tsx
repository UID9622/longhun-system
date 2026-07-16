import { useEffect, useState, useRef } from 'react';
import { Link } from 'react-router';
import { motion } from 'framer-motion';
import { Check, ChevronRight, Activity } from 'lucide-react';
import GlassPanel from '@/components/GlassPanel';
import ColorSwatch from '@/components/ColorSwatch';
import WeightDisplay from '@/components/WeightDisplay';
import AuthorityReveal from '@/components/AuthorityReveal';

/* ─── Animation helpers ─── */
const snapEase = [0.16, 1, 0.3, 1] as [number, number, number, number];

/* ─── Data ─── */
const fiveColors = [
  { color: '#00C853', name: '龙魂绿', hex: '#00C853', tag: '通过/正常', tagColor: '#00C853', tagTextColor: '#0A0A0F' },
  { color: '#FF3D00', name: '龙魂红', hex: '#FF3D00', tag: '熔断/阻断', tagColor: '#FF3D00', tagTextColor: '#FFFFFF' },
  { color: '#FFD600', name: '龙魂黄', hex: '#FFD600', tag: '警示/审查', tagColor: '#FFD600', tagTextColor: '#0A0A0F' },
  { color: '#1A1A2E', name: '龙魂黑', hex: '#1A1A2E', tag: '影子/静默', tagColor: 'transparent', tagTextColor: 'var(--dragon-gold)' },
  { color: '#FFD700', name: '龙魂金', hex: '#FFD700', tag: '主控/主权', tagColor: '#FFD700', tagTextColor: '#0A0A0F' },
];

const marqueeColors = [
  { color: '#00C853', label: '通过' },
  { color: '#FF3D00', label: '熔断' },
  { color: '#FFD600', label: '警示' },
  { color: '#1A1A2E', label: '影子' },
  { color: '#FFD700', label: '主控' },
  { color: '#2962FF', label: '外联' },
  { color: '#AA00FF', label: '进化' },
];

const countries = [
  {
    name: '中国',
    flag: '🇨🇳',
    extensions: ['#DE2910', '#F8B500'],
    extNames: ['中国红', '琉璃黄'],
  },
  {
    name: '日本',
    flag: '🇯🇵',
    extensions: ['#FFB7C5', '#4B0082'],
    extNames: ['樱花粉', '靛蓝'],
  },
  {
    name: '欧盟',
    flag: '🇪🇺',
    extensions: ['#003399', '#FFCC00'],
    extNames: ['欧盟蓝', '星金黄'],
  },
  {
    name: '美国',
    flag: '🇺🇸',
    extensions: ['#3C3B6E', '#B22234'],
    extNames: ['自由蓝', '勇气红'],
  },
];

/* ─── Weight Cascade number ─── */
function useWeightCascade(target: number, delay: number, triggered: boolean) {
  const [value, setValue] = useState(0);

  useEffect(() => {
    if (!triggered) return;
    const startTime = Date.now() + delay;
    const duration = 1200;

    const animate = () => {
      const elapsed = Date.now() - startTime;
      if (elapsed < 0) {
        requestAnimationFrame(animate);
        return;
      }
      const progress = Math.min(elapsed / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      setValue(eased * target);
      if (progress < 1) requestAnimationFrame(animate);
    };
    requestAnimationFrame(animate);
  }, [target, delay, triggered]);

  return value;
}

/* ═══════════════════════════════════════════
   Section 1: Hero
   ═══════════════════════════════════════════ */
function HeroSection() {
  const [formulaVisible, setFormulaVisible] = useState(false);
  const balanceScore = useWeightCascade(0.973, 2000, formulaVisible);

  useEffect(() => {
    const t = setTimeout(() => setFormulaVisible(true), 1600);
    return () => clearTimeout(t);
  }, []);

  return (
    <section
      className="relative min-h-[100dvh] flex items-center overflow-hidden"
      style={{
        backgroundColor: 'var(--spectrum-void)',
        paddingTop: 120,
      }}
    >
      {/* Background layers */}
      <div
        className="absolute inset-0 z-0"
        style={{
          backgroundImage: 'url(/grid-bg.png)',
          backgroundRepeat: 'repeat',
          opacity: 0.4,
        }}
      />
      <img
        src="/hero-glow.jpg"
        alt=""
        className="absolute bottom-0 right-0 w-[80%] h-auto z-0 pointer-events-none"
        style={{ opacity: 0.6 }}
      />

      {/* Content */}
      <div className="relative z-10 max-w-[800px] px-6 md:px-12">
        {/* Eyebrow */}
        <motion.div
          initial={{ opacity: 0, x: -40 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.6, delay: 0.2, ease: snapEase }}
          className="flex items-center gap-3 mb-6"
        >
          <span
            className="inline-block w-0.5 h-5"
            style={{ backgroundColor: 'var(--dragon-gold)' }}
          />
          <span
            className="text-label font-noto-sans"
            style={{ color: 'var(--dragon-gold)' }}
          >
            龙魂生态 · 权重视觉系统
          </span>
        </motion.div>

        {/* Headline Line 1 */}
        <motion.h1
          initial={{ opacity: 0, y: 80 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.4, ease: snapEase }}
          className="text-hero font-noto-serif leading-tight mb-2"
          style={{ color: 'var(--spectrum-peak)' }}
        >
          不动点五主色
        </motion.h1>

        {/* Headline Line 2 */}
        <motion.h1
          initial={{ opacity: 0, y: 80 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.8, ease: snapEase }}
          className="text-hero font-noto-serif leading-tight mb-6"
        >
          <span style={{ color: 'var(--spectrum-peak)' }}>机器识差</span>
          <span style={{ color: 'var(--spectrum-peak)' }}> · </span>
          <span
            style={{
              background: 'linear-gradient(135deg, #FFD700, #FFD600, #FF3D00)',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
              backgroundClip: 'text',
            }}
          >
            人眼不变
          </span>
        </motion.h1>

        {/* Subtitle */}
        <motion.p
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 1.2, ease: snapEase }}
          className="text-body-lg font-noto-sans mb-10 max-w-[560px]"
          style={{ color: 'var(--spectrum-medium)', lineHeight: 1.8 }}
        >
          五行定基，三才赋权，七彩通律。权重可算，颜色不可移。这叫做规矩。
        </motion.p>

        {/* Formula card */}
        <motion.div
          initial={{ opacity: 0, y: 60 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 1.6, ease: snapEase }}
        >
          <GlassPanel className="max-w-[480px] p-6">
            {/* Top row */}
            <div className="flex items-center justify-between pb-4" style={{ borderBottom: '1px solid var(--glass-border)' }}>
              <span className="text-label font-noto-sans" style={{ color: 'var(--spectrum-dim)' }}>
                三才平衡系数
              </span>
              <span className="text-code font-jetbrain" style={{ color: 'var(--dragon-gold)' }}>
                Heaven×0.35 + Earth×0.20 + Human×0.45
              </span>
            </div>

            {/* Middle row */}
            <div className="py-6 text-center">
              <span
                className="font-jetbrain tabular-nums"
                style={{
                  fontSize: 'clamp(28px, 3.5vw, 48px)',
                  fontWeight: 700,
                  color: 'var(--dragon-green)',
                }}
              >
                {balanceScore.toFixed(3)}
              </span>
            </div>

            {/* Bottom row */}
            <div className="flex items-center gap-3 pt-4" style={{ borderTop: '1px solid var(--glass-border)' }}>
              <span
                className="inline-flex items-center gap-1 text-label px-3 py-1.5 rounded-full"
                style={{
                  border: '1px solid var(--dragon-yellow)',
                  color: 'var(--dragon-yellow)',
                }}
              >
                铁律: Human≥0.34
              </span>
              <span
                className="inline-flex items-center gap-1 text-label px-3 py-1.5 rounded-full"
                style={{
                  backgroundColor: 'var(--dragon-green)',
                  color: 'var(--spectrum-void)',
                }}
              >
                <Check size={12} strokeWidth={3} /> 通过
              </span>
            </div>
          </GlassPanel>
        </motion.div>

        {/* CTA row */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 2.2, ease: snapEase }}
          className="flex items-center gap-4 mt-8"
        >
          <Link
            to="/weights"
            className="inline-flex items-center gap-2 px-8 py-3.5 rounded-lg font-noto-sans font-semibold transition-all duration-300 hover:scale-[1.03]"
            style={{
              backgroundColor: 'var(--dragon-gold)',
              color: 'var(--spectrum-void)',
            }}
          >
            进入权重面板
            <ChevronRight size={16} />
          </Link>
          <Link
            to="/colors"
            className="inline-flex items-center gap-2 px-8 py-3.5 rounded-lg font-noto-sans font-semibold transition-all duration-300"
            style={{
              backgroundColor: 'transparent',
              border: '1px solid var(--spectrum-border)',
              color: 'var(--spectrum-bright)',
            }}
            onMouseEnter={(e) => {
              (e.target as HTMLElement).style.borderColor = 'var(--dragon-gold)';
            }}
            onMouseLeave={(e) => {
              (e.target as HTMLElement).style.borderColor = 'var(--spectrum-border)';
            }}
          >
            查看不动点色卡
          </Link>
        </motion.div>
      </div>

      {/* Scroll indicator */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.5, delay: 3.0 }}
        className="absolute bottom-8 left-1/2 -translate-x-1/2 flex flex-col items-center gap-2"
      >
        <div className="relative w-px h-10 overflow-hidden" style={{ backgroundColor: 'var(--spectrum-dim)' }}>
          <div
            className="absolute top-0 left-0 w-full h-3 rounded-full"
            style={{
              backgroundColor: 'var(--spectrum-dim)',
              animation: 'scroll-dot 2s ease-in-out infinite',
            }}
          />
        </div>
        <span className="text-caption" style={{ color: 'var(--spectrum-dim)' }}>
          下 scroll
        </span>
      </motion.div>
    </section>
  );
}

/* ═══════════════════════════════════════════
   Section 2: Five Immutable Colors
   ═══════════════════════════════════════════ */
function FiveColorsSection() {
  const [sectionVisible, setSectionVisible] = useState(false);
  const sectionRef = useRef<HTMLElement>(null);

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) setSectionVisible(true);
      },
      { threshold: 0.2 }
    );
    if (sectionRef.current) observer.observe(sectionRef.current);
    return () => observer.disconnect();
  }, []);

  return (
    <section
      ref={sectionRef}
      className="relative py-24 md:py-32 px-6 md:px-12"
      style={{ backgroundColor: 'var(--spectrum-shadow)' }}
    >
      <div className="max-w-[1200px] mx-auto">
        {/* Section header */}
        <AuthorityReveal className="text-center mb-16">
          <span className="text-label font-noto-sans block mb-4" style={{ color: 'var(--dragon-gold)' }}>
            不动点协议
          </span>
          <h2 className="text-h1 font-noto-serif mb-4" style={{ color: 'var(--spectrum-peak)' }}>
            五主色 · 永不改变
          </h2>
          <p
            className="text-body-lg font-noto-sans max-w-[640px] mx-auto"
            style={{ color: 'var(--spectrum-medium)' }}
          >
            绿通过，红熔断，黄警示，黑影子，金主控。这五个颜色，从龙魂生态第一天到最后一天，位置不变，色值不变，含义不变。
          </p>
        </AuthorityReveal>

        {/* Color showcase row */}
        <div className="flex flex-wrap justify-center gap-8 md:gap-12 mb-16">
          {fiveColors.map((c, i) => (
            <motion.div
              key={c.hex}
              initial={{ opacity: 0, y: 60 }}
              animate={sectionVisible ? { opacity: 1, y: 0 } : {}}
              transition={{ duration: 0.5, delay: 0.3 + i * 0.15, ease: snapEase }}
            >
              <ColorSwatch
                color={c.color}
                name={c.name}
                hex={c.hex}
                tag={c.tag}
                tagColor={c.tagColor}
                tagTextColor={c.tagTextColor}
                size={120}
                showLock
                animatePulse
              />
            </motion.div>
          ))}
        </div>

        {/* Immutable rule strip */}
        <motion.div
          initial={{ opacity: 0, y: 40 }}
          animate={sectionVisible ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.6, delay: 1.2, ease: snapEase }}
          className="rounded-lg px-6 py-4 text-center overflow-hidden"
          style={{ backgroundColor: 'var(--spectrum-raise)' }}
        >
          <code
            className="text-code font-jetbrain block"
            style={{ color: 'var(--spectrum-bright)', fontSize: 'clamp(10px, 1.2vw, 14px)' }}
          >
            IMMUTABILITY_CLAUSE: color.hex ∈ {'{'} #00C853, #FF3D00, #FFD600, #1A1A2E, #FFD700 {'}'} ⇒ color.position = FIXED ∧ color.meaning = ETERNAL
          </code>
        </motion.div>
      </div>
    </section>
  );
}

/* ═══════════════════════════════════════════
   Section 3: Weight at a Glance
   ═══════════════════════════════════════════ */
function WeightSection() {
  return (
    <section
      className="py-24 md:py-32 px-6 md:px-12"
      style={{ backgroundColor: 'var(--spectrum-void)' }}
    >
      <div className="max-w-[1200px] mx-auto">
        {/* Section header */}
        <AuthorityReveal className="mb-16">
          <span className="text-label font-noto-sans block mb-4" style={{ color: 'var(--dragon-gold)' }}>
            权重面板 · 概览
          </span>
          <h2 className="text-h1 font-noto-serif" style={{ color: 'var(--spectrum-peak)' }}>
            三才赋权 · 五行定基
          </h2>
        </AuthorityReveal>

        {/* Three weight cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
          {/* 天 */}
          <AuthorityReveal delay={0}>
            <GlassPanel className="p-8 h-full relative">
              <span
                className="inline-block text-label px-3 py-1 rounded-full mb-6"
                style={{
                  border: '1px solid var(--dragon-gold)',
                  color: 'var(--dragon-gold)',
                }}
              >
                战略层
              </span>
              <WeightDisplay
                value={0.35}
                label="天 · Heaven"
                sublabel="天"
                color="var(--dragon-gold)"
                delay={0}
              />
              <p
                className="text-body font-noto-sans mt-4 text-center"
                style={{ color: 'var(--spectrum-medium)' }}
              >
                战略权重，高瞻远瞩。天定方向，占35%。
              </p>
            </GlassPanel>
          </AuthorityReveal>

          {/* 人 */}
          <AuthorityReveal delay={150}>
            <GlassPanel className="p-8 h-full relative" style={{ borderColor: 'var(--dragon-gold)', borderWidth: 2 }}>
              <span
                className="inline-block text-label px-3 py-1 rounded-full mb-6"
                style={{
                  border: '1px solid var(--dragon-green)',
                  color: 'var(--dragon-green)',
                }}
              >
                决策层
              </span>
              <WeightDisplay
                value={0.45}
                label="人 · Human"
                sublabel="人"
                color="var(--dragon-green)"
                delay={150}
                showBadge
                badgeText="✓ 铁律满足"
              />
              <p
                className="text-body font-noto-sans mt-4 text-center"
                style={{ color: 'var(--spectrum-medium)' }}
              >
                决策权重，核心枢纽。人永远不低于34%，这是铁律。
              </p>
            </GlassPanel>
          </AuthorityReveal>

          {/* 地 */}
          <AuthorityReveal delay={300}>
            <GlassPanel className="p-8 h-full relative">
              <span
                className="inline-block text-label px-3 py-1 rounded-full mb-6"
                style={{
                  border: '1px solid var(--dragon-yellow)',
                  color: 'var(--dragon-yellow)',
                }}
              >
                基础层
              </span>
              <WeightDisplay
                value={0.20}
                label="地 · Earth"
                sublabel="地"
                color="var(--dragon-yellow)"
                delay={300}
              />
              <p
                className="text-body font-noto-sans mt-4 text-center"
                style={{ color: 'var(--spectrum-medium)' }}
              >
                基础权重，承载万物。地基稳固，占20%。
              </p>
            </GlassPanel>
          </AuthorityReveal>
        </div>

        {/* Balance formula strip */}
        <AuthorityReveal delay={400}>
          <GlassPanel className="px-6 md:px-12 py-6 flex flex-col md:flex-row items-center justify-between gap-4">
            <span className="text-code font-jetbrain" style={{ color: 'var(--spectrum-bright)' }}>
              三才平衡系数 =
            </span>
            <span className="text-code font-jetbrain" style={{ color: 'var(--dragon-gold)' }}>
              0.35 × 0.35 + 0.20 × 0.20 + 0.45 × 0.45 = 0.365
            </span>
            <span
              className="inline-flex items-center gap-2 text-label px-4 py-2 rounded-full"
              style={{
                backgroundColor: 'var(--dragon-green)',
                color: 'var(--spectrum-void)',
              }}
            >
              平衡指数: 97.3%
            </span>
          </GlassPanel>
        </AuthorityReveal>

        {/* CTA */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5, delay: 0.3, ease: snapEase }}
          className="text-center mt-8"
        >
          <Link
            to="/weights"
            className="inline-flex items-center gap-2 px-8 py-3.5 rounded-lg font-noto-sans font-semibold transition-all duration-300 hover:scale-[1.03]"
            style={{
              backgroundColor: 'var(--dragon-gold)',
              color: 'var(--spectrum-void)',
            }}
          >
            进入完整权重面板
            <ChevronRight size={16} />
          </Link>
        </motion.div>
      </div>
    </section>
  );
}

/* ═══════════════════════════════════════════
   Section 4: Marquee Teaser
   ═══════════════════════════════════════════ */
function MarqueeSection() {
  const duplicated = [...marqueeColors, ...marqueeColors];

  return (
    <section
      className="relative py-16 md:py-24 px-6 md:px-12 overflow-hidden"
      style={{ backgroundColor: 'var(--spectrum-shadow)' }}
    >
      <div className="max-w-[1200px] mx-auto">
        <AuthorityReveal>
          {/* Speed indicator */}
          <div
            className="absolute top-4 right-8 md:right-12 flex items-center gap-1 text-caption"
            style={{ color: 'var(--spectrum-dim)' }}
          >
            <Activity size={12} />
            <span>速度: 1.0x</span>
          </div>

          {/* Marquee strip */}
          <div
            className="relative w-full h-20 rounded-xl overflow-hidden mb-8"
            style={{ backgroundColor: 'var(--spectrum-raise)' }}
          >
            <div className="flex animate-marquee-flow h-full" style={{ width: 'max-content' }}>
              {duplicated.map((item, i) => (
                <div
                  key={i}
                  className="flex-shrink-0 h-full flex items-center justify-center"
                  style={{
                    width: 200,
                    backgroundColor: item.color,
                  }}
                >
                  <span
                    className="text-label font-noto-sans font-semibold"
                    style={{
                      color:
                        item.color === '#1A1A2E'
                          ? 'var(--spectrum-dim)'
                          : item.color === '#FFD600' || item.color === '#FFD700'
                          ? '#0A0A0F'
                          : '#FFFFFF',
                    }}
                  >
                    {item.label}
                  </span>
                </div>
              ))}
            </div>
          </div>

          {/* Label below */}
          <div className="text-center mb-6">
            <h3 className="text-h3 font-noto-serif mb-2" style={{ color: 'var(--spectrum-peak)' }}>
              七彩跑马灯 · 七态通律
            </h3>
            <p className="text-body font-noto-sans" style={{ color: 'var(--spectrum-medium)' }}>
              绿红黄黑金蓝紫——七种状态，七种命令，机器一读便知。
            </p>
          </div>

          {/* CTA */}
          <div className="text-center">
            <Link
              to="/marquee"
              className="inline-flex items-center gap-2 px-6 py-3 rounded-lg font-noto-sans font-medium transition-all duration-300"
              style={{
                backgroundColor: 'transparent',
                border: '1px solid var(--spectrum-border)',
                color: 'var(--spectrum-bright)',
              }}
              onMouseEnter={(e) => {
                (e.target as HTMLElement).style.borderColor = 'var(--dragon-gold)';
              }}
              onMouseLeave={(e) => {
                (e.target as HTMLElement).style.borderColor = 'var(--spectrum-border)';
              }}
            >
              查看完整跑马灯系统
              <ChevronRight size={16} />
            </Link>
          </div>
        </AuthorityReveal>
      </div>
    </section>
  );
}

/* ═══════════════════════════════════════════
   Section 5: Country Palette Preview
   ═══════════════════════════════════════════ */
function CountrySection() {
  return (
    <section
      className="py-24 md:py-32 px-6 md:px-12"
      style={{ backgroundColor: 'var(--spectrum-void)' }}
    >
      <div className="max-w-[1200px] mx-auto">
        {/* Section header */}
        <AuthorityReveal className="text-center mb-16">
          <span className="text-label font-noto-sans block mb-4" style={{ color: 'var(--dragon-gold)' }}>
            各国色卡
          </span>
          <h2 className="text-h1 font-noto-serif mb-4" style={{ color: 'var(--spectrum-peak)' }}>
            一个基础 · 万国同源
          </h2>
          <p
            className="text-body-lg font-noto-sans max-w-[640px] mx-auto"
            style={{ color: 'var(--spectrum-medium)' }}
          >
            机器识别出色卡差异，但人眼永远习惯这五种颜色。中国加红加黄，日本加粉加靛——五主色不动，其余可移。
          </p>
        </AuthorityReveal>

        {/* Country cards */}
        <div className="flex flex-wrap justify-center gap-5 mb-12">
          {countries.map((country, i) => (
            <motion.div
              key={country.name}
              initial={{ opacity: 0, y: 60, rotate: 5 }}
              whileInView={{ opacity: 1, y: 0, rotate: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: i * 0.12, ease: snapEase }}
            >
              <Link to="/comparison" className="block">
                <GlassPanel className="p-6 w-[260px] h-[320px] flex flex-col items-center transition-transform duration-300 hover:scale-[1.03]">
                  {/* Flag + name */}
                  <div className="flex items-center gap-2 mb-4">
                    <span className="text-2xl">{country.flag}</span>
                    <span className="text-h3 font-noto-serif" style={{ color: 'var(--spectrum-peak)' }}>
                      {country.name}
                    </span>
                  </div>

                  {/* Five immutable dots */}
                  <div className="flex items-center gap-2 mb-3">
                    {fiveColors.map((c) => (
                      <span
                        key={c.hex}
                        className="inline-block rounded-full"
                        style={{
                          width: 12,
                          height: 12,
                          backgroundColor: c.color,
                          border: c.hex === '#1A1A2E' ? '1px solid var(--spectrum-border)' : 'none',
                        }}
                      />
                    ))}
                  </div>

                  {/* Divider */}
                  <div className="w-full h-px mb-3" style={{ backgroundColor: 'var(--spectrum-border)' }} />

                  {/* Extension label */}
                  <span className="text-label mb-2" style={{ color: 'var(--spectrum-dim)' }}>
                    + 扩展
                  </span>

                  {/* Extension dots */}
                  <div className="flex items-center gap-3 mb-4">
                    {country.extensions.map((ext, j) => (
                      <div key={ext} className="flex flex-col items-center gap-1">
                        <span
                          className="inline-block rounded-full"
                          style={{ width: 16, height: 16, backgroundColor: ext }}
                        />
                        <span className="text-caption" style={{ color: 'var(--spectrum-dim)' }}>
                          {country.extNames[j]}
                        </span>
                      </div>
                    ))}
                  </div>

                  {/* Footer */}
                  <span className="text-caption mt-auto" style={{ color: 'var(--spectrum-dim)' }}>
                    不动点 + 2
                  </span>
                </GlassPanel>
              </Link>
            </motion.div>
          ))}
        </div>

        {/* Immutable message */}
        <motion.div
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8, delay: 0.6, ease: snapEase }}
          className="text-center"
        >
          <span
            className="text-h3 font-noto-serif"
            style={{ color: 'var(--dragon-gold)' }}
          >
            五主色不动，这叫做规矩。
          </span>
        </motion.div>
      </div>
    </section>
  );
}

/* ═══════════════════════════════════════════
   Section 6: Home Footer Spectrum Strip
   ═══════════════════════════════════════════ */
function SpectrumStrip() {
  return (
    <div
      className="w-full h-1 animate-shimmer"
      style={{
        background: 'linear-gradient(90deg, #00C853, #FFD600, #FF3D00, #AA00FF, #2962FF, #FFD700, #1A1A2E, #00C853)',
        backgroundSize: '200% 100%',
      }}
    />
  );
}

/* ═══════════════════════════════════════════
   Home Page Assembly
   ═══════════════════════════════════════════ */
export default function Home() {
  return (
    <div>
      <HeroSection />
      <FiveColorsSection />
      <WeightSection />
      <MarqueeSection />
      <CountrySection />
      <SpectrumStrip />
    </div>
  );
}
