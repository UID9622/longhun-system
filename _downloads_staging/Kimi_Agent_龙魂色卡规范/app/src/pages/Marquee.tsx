import { useState, useEffect, useRef } from 'react';
import { motion } from 'framer-motion';
import {
  Play,
  Pause,
  RotateCcw,
  ArrowRight,
  ArrowLeft,
  Zap,
  Activity,
  Radio,
} from 'lucide-react';
import GlassPanel from '@/components/GlassPanel';
import AuthorityReveal from '@/components/AuthorityReveal';
import MarqueeStrip from './marquee/MarqueeStrip';
import MarqueeKeyframes from './marquee/MarqueeKeyframes';
import { COLOR_SEGMENTS, TITLE_CHARS } from './marquee/types';
import type { MarqueeSettings, ColorSegment } from './marquee/types';

/* ─── easing constants ─── */
const ease = [0.16, 1, 0.3, 1] as [number, number, number, number];

/* ─── Log entry generator ─── */
let frameCounter = 0;
function generateLogEntry(): {
  time: string;
  frame: number;
  color: ColorSegment;
  deltaE: string;
} {
  frameCounter += 1;
  const now = new Date();
  const time = `${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}:${String(now.getSeconds()).padStart(2, '0')}.${String(now.getMilliseconds()).padStart(3, '0')}`;
  const color = COLOR_SEGMENTS[frameCounter % 7];
  const deltaE = (Math.random() * 0.05).toFixed(2);
  return { time, frame: 1247 + frameCounter, color, deltaE };
}

/* ═══════════════════════════════════════════════════════════
   Section 1 — Signal Tower Hero
   ═══════════════════════════════════════════════════════════ */
function SignalTowerHero({ settings }: { settings: MarqueeSettings }) {
  const modeMap: Record<string, string> = {
    continuous: '自动循环',
    pulse: '脉冲波',
    segment: '段闪',
  };

  return (
    <section
      className="relative w-full flex flex-col items-center justify-center overflow-hidden"
      style={{
        minHeight: '50vh',
        backgroundColor: 'var(--spectrum-void)',
        paddingTop: 64 + 48,
        paddingBottom: 48,
      }}
    >
      {/* Machine scan overlay */}
      <div
        className="absolute inset-0 pointer-events-none z-0"
        style={{
          backgroundImage: 'url(/scan-line.png)',
          backgroundRepeat: 'no-repeat',
          backgroundSize: '100% 1px',
          animation: 'machine-scan 4s linear infinite',
          opacity: 0.4,
        }}
      />

      <div className="relative z-10 flex flex-col items-center text-center px-6 max-w-[900px]">
        {/* Breadcrumb */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.3, ease }}
          className="text-label text-code mb-6"
          style={{ color: 'var(--spectrum-dim)', textTransform: 'none' }}
        >
          龙魂生态 / 七彩跑马灯
        </motion.div>

        {/* Title with colored characters */}
        <div className="flex items-center justify-center flex-wrap gap-1 mb-4">
          {TITLE_CHARS.map((tc, i) => (
            <motion.span
              key={i}
              initial={{ opacity: 0, y: 40 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.4, delay: i * 0.06, ease }}
              className="text-hero font-noto-serif inline-block"
              style={{
                color: tc.color,
                WebkitTextStroke: tc.strokeColor ? `1.5px ${tc.strokeColor}` : 'none',
                textShadow: tc.strokeColor
                  ? '0 0 20px rgba(255,255,255,0.2)'
                  : `0 0 30px ${tc.color}66`,
                fontWeight: 900,
              }}
            >
              {tc.char}
            </motion.span>
          ))}
          {/* SYSTEM suffix */}
          <motion.span
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.4, delay: 0.5, ease }}
            className="text-code ml-3 self-end mb-3"
            style={{
              color: 'var(--spectrum-dim)',
              fontSize: 18,
              letterSpacing: '0.2em',
              fontFamily: "'JetBrains Mono', monospace",
              textTransform: 'uppercase',
            }}
          >
            SYSTEM
          </motion.span>
        </div>

        {/* Subtitle */}
        <motion.p
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.8, ease }}
          className="text-body-lg font-noto-sans mb-6"
          style={{
            color: 'var(--spectrum-medium)',
            maxWidth: 600,
            lineHeight: 1.7,
          }}
        >
          七种状态，七种命令。绿通过，红熔断，黄警示，黑影子，金主控，蓝外联，紫进化。机器一读，全部知晓。
        </motion.p>

        {/* Status readout */}
        <motion.div
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 1.0, ease }}
          className="flex items-center gap-6 flex-wrap justify-center"
        >
          {/* Mode badge */}
          <span
            className="text-label px-4 py-1.5 rounded-full"
            style={{
              backgroundColor: 'rgba(255, 215, 0, 0.15)',
              color: 'var(--dragon-gold)',
              textTransform: 'none',
            }}
          >
            当前模式: {modeMap[settings.mode]}
          </span>

          {/* Speed */}
          <span
            className="text-label"
            style={{ color: 'var(--spectrum-dim)', textTransform: 'none' }}
          >
            速度: {(20 / settings.speed).toFixed(1)}x
          </span>

          {/* Status with pulsing dot */}
          <div className="flex items-center gap-2">
            <span
              className="inline-block w-2 h-2 rounded-full animate-pulse"
              style={{ backgroundColor: 'var(--dragon-green)' }}
            />
            <span
              className="text-label"
              style={{ color: 'var(--dragon-green)', textTransform: 'none' }}
            >
              {settings.isPlaying ? '运行中' : '已暂停'}
            </span>
          </div>
        </motion.div>
      </div>
    </section>
  );
}

/* ═══════════════════════════════════════════════════════════
   Section 2 — Main Marquee Display
   ═══════════════════════════════════════════════════════════ */
function MainMarqueeDisplay({ settings }: { settings: MarqueeSettings }) {
  const speedFactor = (20 / settings.speed).toFixed(1);

  return (
    <section
      className="relative w-full"
      style={{
        height: 400,
        backgroundColor: 'var(--spectrum-shadow)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
      }}
    >
      {/* Speed gauge - top right */}
      <div
        className="absolute top-4 right-8 z-20 flex items-center gap-4"
      >
        {/* Direction indicator */}
        <div className="flex items-center gap-1.5">
          {settings.direction === 'right' ? (
            <ArrowRight size={16} style={{ color: 'var(--dragon-gold)' }} />
          ) : (
            <ArrowLeft size={16} style={{ color: 'var(--dragon-gold)' }} />
          )}
          <span
            className="text-caption"
            style={{ color: 'var(--dragon-gold)' }}
          >
            {settings.direction === 'right' ? '向右' : '向左'}
          </span>
        </div>

        {/* Speed gauge circle */}
        <div
          className="relative flex items-center justify-center"
          style={{ width: 60, height: 60 }}
        >
          {/* Background circle */}
          <svg width="60" height="60" viewBox="0 0 60 60" className="absolute">
            <circle
              cx="30"
              cy="30"
              r="26"
              fill="none"
              stroke="var(--spectrum-border)"
              strokeWidth="3"
            />
            <circle
              cx="30"
              cy="30"
              r="26"
              fill="none"
              stroke="var(--dragon-gold)"
              strokeWidth="3"
              strokeLinecap="round"
              strokeDasharray={`${(parseFloat(speedFactor) / 3) * 163.36} 163.36`}
              strokeDashoffset="-40.84"
              transform="rotate(-90 30 30)"
              style={{ transition: 'stroke-dasharray 0.3s ease' }}
            />
          </svg>
          <span
            className="text-code relative z-10"
            style={{ color: 'var(--spectrum-peak)', fontSize: 13, fontWeight: 600 }}
          >
            {speedFactor}x
          </span>
        </div>
      </div>

      {/* Main marquee strip */}
      <MarqueeStrip settings={settings} height={120} segmentMinWidth={280} showDetails />
    </section>
  );
}

/* ═══════════════════════════════════════════════════════════
   Section 3 — Control Panel
   ═══════════════════════════════════════════════════════════ */
function ControlPanel({
  settings,
  onSettingsChange,
}: {
  settings: MarqueeSettings;
  onSettingsChange: (s: MarqueeSettings) => void;
}) {
  const speedPercent = ((settings.speed - 5) / (60 - 5)) * 100;

  const handleSpeedChange = (val: number) => {
    onSettingsChange({ ...settings, speed: val });
  };

  const handleDirectionToggle = (dir: 'left' | 'right') => {
    onSettingsChange({ ...settings, direction: dir });
  };

  const handleModeChange = (mode: MarqueeSettings['mode']) => {
    onSettingsChange({ ...settings, mode });
  };

  const handleTogglePlay = () => {
    onSettingsChange({ ...settings, isPlaying: !settings.isPlaying });
  };

  const handleReset = () => {
    onSettingsChange({
      speed: 20,
      direction: 'left',
      mode: 'continuous',
      isPlaying: true,
    });
  };

  const modes: { key: MarqueeSettings['mode']; label: string; icon: React.ReactNode }[] = [
    { key: 'continuous', label: '连续流动', icon: <Activity size={14} /> },
    { key: 'pulse', label: '脉冲波', icon: <Zap size={14} /> },
    { key: 'segment', label: '段闪', icon: <Radio size={14} /> },
  ];

  return (
    <section
      className="w-full py-12 px-6"
      style={{ backgroundColor: 'var(--spectrum-void)' }}
    >
      <div className="max-w-[960px] mx-auto grid grid-cols-1 md:grid-cols-2 gap-8">
        {/* ── Left column: Speed & Direction ── */}
        <AuthorityReveal delay={0}>
          <div className="flex flex-col gap-6">
            {/* Speed control */}
            <div>
              <div className="flex items-center justify-between mb-3">
                <span
                  className="text-label"
                  style={{ color: 'var(--spectrum-bright)', textTransform: 'none' }}
                >
                  跑马灯速度
                </span>
                <span
                  className="text-code"
                  style={{ color: 'var(--dragon-gold)', fontWeight: 600 }}
                >
                  {(20 / settings.speed).toFixed(1)}x
                </span>
              </div>
              <input
                type="range"
                min={5}
                max={60}
                step={1}
                value={settings.speed}
                onChange={(e) => handleSpeedChange(Number(e.target.value))}
                className="marquee-slider w-full"
                style={{ '--slider-percent': `${speedPercent}%` } as React.CSSProperties}
              />
              <div className="flex items-center justify-between mt-2">
                <span className="text-caption" style={{ color: 'var(--spectrum-dim)' }}>快速 (5s)</span>
                <span className="text-caption" style={{ color: 'var(--spectrum-dim)' }}>慢速 (60s)</span>
              </div>
              {/* Preset buttons */}
              <div className="flex gap-2 mt-3">
                {[20, 40, 60].map((preset) => (
                  <motion.button
                    key={preset}
                    whileTap={{ scale: 0.95 }}
                    onClick={() => handleSpeedChange(preset)}
                    className="text-caption px-3 py-1.5 rounded-md transition-all duration-200"
                    style={{
                      backgroundColor: settings.speed === preset
                        ? 'rgba(255, 215, 0, 0.2)'
                        : 'var(--spectrum-raise)',
                      color: settings.speed === preset
                        ? 'var(--dragon-gold)'
                        : 'var(--spectrum-medium)',
                      border: `1px solid ${settings.speed === preset ? 'var(--dragon-gold)' : 'var(--spectrum-border)'}`,
                    }}
                  >
                    {preset === 20 ? '1.0x正常' : preset === 40 ? '0.5x慢速' : '0.3x极慢'}
                  </motion.button>
                ))}
              </div>
            </div>

            {/* Direction toggle */}
            <div>
              <span
                className="text-label block mb-3"
                style={{ color: 'var(--spectrum-bright)', textTransform: 'none' }}
              >
                方向
              </span>
              <div className="flex gap-2">
                {(['left', 'right'] as const).map((dir) => (
                  <motion.button
                    key={dir}
                    whileTap={{ scale: 0.95 }}
                    onClick={() => handleDirectionToggle(dir)}
                    className="flex items-center gap-1.5 px-4 py-2 rounded-lg text-body transition-all duration-200"
                    style={{
                      backgroundColor: settings.direction === dir
                        ? 'rgba(255, 215, 0, 0.2)'
                        : 'var(--spectrum-raise)',
                      color: settings.direction === dir
                        ? 'var(--dragon-gold)'
                        : 'var(--spectrum-medium)',
                      border: `1.5px solid ${settings.direction === dir ? 'var(--dragon-gold)' : 'var(--spectrum-border)'}`,
                    }}
                  >
                    {dir === 'left' ? <ArrowLeft size={16} /> : <ArrowRight size={16} />}
                    {dir === 'left' ? '向左' : '向右'}
                  </motion.button>
                ))}
              </div>
            </div>

            {/* Mode selector */}
            <div>
              <span
                className="text-label block mb-3"
                style={{ color: 'var(--spectrum-bright)', textTransform: 'none' }}
              >
                运行模式
              </span>
              <div className="flex flex-col gap-2">
                {modes.map((m) => (
                  <motion.button
                    key={m.key}
                    whileTap={{ scale: 0.98 }}
                    onClick={() => handleModeChange(m.key)}
                    className="flex items-center gap-2 px-4 py-3 rounded-lg text-body transition-all duration-200 text-left"
                    style={{
                      backgroundColor: settings.mode === m.key
                        ? 'rgba(255, 215, 0, 0.1)'
                        : 'var(--glass-panel)',
                      color: settings.mode === m.key
                        ? 'var(--dragon-gold)'
                        : 'var(--spectrum-medium)',
                      border: `2px solid ${settings.mode === m.key ? 'var(--dragon-gold)' : 'var(--glass-border)'}`,
                    }}
                  >
                    {m.icon}
                    {m.label}
                  </motion.button>
                ))}
              </div>
            </div>

            {/* Play/Pause + Reset */}
            <div className="flex gap-3 mt-2">
              <motion.button
                whileTap={{ scale: 0.95 }}
                onClick={handleTogglePlay}
                className="flex items-center gap-2 px-6 py-3 rounded-lg text-body font-medium transition-all duration-200"
                style={{
                  backgroundColor: settings.isPlaying
                    ? 'rgba(255, 61, 0, 0.2)'
                    : 'rgba(0, 200, 83, 0.2)',
                  color: settings.isPlaying ? 'var(--dragon-red)' : 'var(--dragon-green)',
                  border: `1.5px solid ${settings.isPlaying ? 'var(--dragon-red)' : 'var(--dragon-green)'}`,
                }}
              >
                {settings.isPlaying ? <Pause size={18} /> : <Play size={18} />}
                {settings.isPlaying ? '暂停' : '播放'}
              </motion.button>

              <motion.button
                whileTap={{ scale: 0.95 }}
                onClick={handleReset}
                className="flex items-center gap-2 px-6 py-3 rounded-lg text-body transition-all duration-200"
                style={{
                  backgroundColor: 'var(--spectrum-raise)',
                  color: 'var(--spectrum-medium)',
                  border: '1.5px solid var(--spectrum-border)',
                }}
              >
                <RotateCcw size={16} />
                重置
              </motion.button>
            </div>
          </div>
        </AuthorityReveal>

        {/* ── Right column: Color detail cards ── */}
        <AuthorityReveal delay={150}>
          <div className="flex flex-col gap-2 max-h-[500px] overflow-y-auto color-list-scroll pr-1">
            {COLOR_SEGMENTS.map((color, idx) => (
              <motion.div
                key={color.id}
                initial={{ opacity: 0, x: 30 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.4, delay: idx * 0.05, ease }}
                whileHover={{ x: 4, transition: { duration: 0.15 } }}
                className="flex items-center gap-3 h-12 px-4 rounded-lg cursor-default transition-colors duration-200"
                style={{
                  backgroundColor: 'var(--glass-panel)',
                  border: `1px solid var(--glass-border)`,
                }}
                onMouseEnter={(e) => {
                  (e.currentTarget as HTMLElement).style.backgroundColor = `${color.hex}14`;
                }}
                onMouseLeave={(e) => {
                  (e.currentTarget as HTMLElement).style.backgroundColor = 'var(--glass-panel)';
                }}
              >
                {/* Color dot */}
                <div
                  className="w-5 h-5 rounded-full flex-shrink-0"
                  style={{
                    backgroundColor: color.hex,
                    boxShadow: color.hex === '#1A1A2E'
                      ? '0 0 0 1px var(--spectrum-border)'
                      : `0 0 8px ${color.hex}66`,
                  }}
                />
                {/* Name */}
                <span
                  className="text-body flex-1"
                  style={{ color: 'var(--spectrum-bright)' }}
                >
                  {color.name} · {color.label.split(' · ')[0]}
                </span>
                {/* Hex */}
                <span
                  className="text-code"
                  style={{ color: 'var(--spectrum-dim)', fontSize: 12 }}
                >
                  {color.hex}
                </span>
              </motion.div>
            ))}
          </div>
        </AuthorityReveal>
      </div>
    </section>
  );
}

/* ═══════════════════════════════════════════════════════════
   Section 4 — Color Meaning Reference
   ═══════════════════════════════════════════════════════════ */
function ColorMeaningReference({ settings }: { settings: MarqueeSettings }) {
  return (
    <section
      className="w-full py-24 md:py-32 px-6"
      style={{ backgroundColor: 'var(--spectrum-shadow)' }}
    >
      {/* Section title */}
      <AuthorityReveal className="text-center mb-12">
        <h2
          className="text-h1 font-noto-serif"
          style={{ color: 'var(--spectrum-peak)' }}
        >
          七色状态详解
        </h2>
      </AuthorityReveal>

      {/* Seven cards grid */}
      <div className="max-w-[1440px] mx-auto grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-7 gap-4">
        {COLOR_SEGMENTS.map((color, idx) => (
          <AuthorityReveal key={color.id} delay={idx * 80}>
            <motion.div
              whileHover={{ scale: 1.02, transition: { duration: 0.25 } }}
              className="rounded-2xl overflow-hidden h-full"
              style={{
                background: 'var(--glass-panel)',
                border: '1px solid var(--glass-border)',
                backdropFilter: 'blur(20px)',
                WebkitBackdropFilter: 'blur(20px)',
                boxShadow: '0 8px 32px rgba(0, 0, 0, 0.4)',
              }}
            >
              {/* Color header strip */}
              <div
                className="w-full h-12"
                style={{
                  backgroundColor: color.hex,
                  animation: `color-pulse-${idx} 2s ease-in-out infinite`,
                  animationDelay: `${idx * 0.3}s`,
                }}
              />

              {/* Card content */}
              <div className="p-5 flex flex-col gap-3">
                {/* Status name */}
                <h3
                  className="text-h3 font-noto-serif"
                  style={{ color: color.hex }}
                >
                  {color.state}
                </h3>

                {/* English label */}
                <span
                  className="text-label"
                  style={{ color: 'var(--spectrum-dim)', fontSize: 10 }}
                >
                  {color.enLabel}
                </span>

                {/* Meaning */}
                <p
                  className="text-body"
                  style={{ color: 'var(--spectrum-medium)' }}
                >
                  {color.meaning}
                </p>

                {/* Hex */}
                <span
                  className="text-code"
                  style={{ color: color.hex, fontSize: 13, fontWeight: 500 }}
                >
                  {color.hex}
                </span>

                {/* Trigger conditions */}
                <div className="flex flex-col gap-1 mt-1">
                  <span
                    className="text-caption"
                    style={{ color: 'var(--spectrum-dim)', fontSize: 10 }}
                  >
                    触发条件:
                  </span>
                  {color.triggers.map((t, i) => (
                    <span
                      key={i}
                      className="text-caption"
                      style={{ color: 'var(--spectrum-dim)' }}
                    >
                      • {t}
                    </span>
                  ))}
                </div>

                {/* Action required */}
                <div
                  className="mt-auto pt-3"
                  style={{ borderTop: '1px solid var(--spectrum-border)' }}
                >
                  <span
                    className="text-caption"
                    style={{ color: color.hex }}
                  >
                    → {color.action}
                  </span>
                </div>
              </div>
            </motion.div>
          </AuthorityReveal>
        ))}
      </div>

      {/* Secondary marquee strip */}
      <div className="mt-12 max-w-[1440px] mx-auto">
        <MarqueeStrip
          settings={{ ...settings, speed: 10 }}
          height={60}
          segmentMinWidth={180}
          showDetails={false}
        />
      </div>
    </section>
  );
}

/* ═══════════════════════════════════════════════════════════
   Section 5 — Machine Detection Overlay
   ═══════════════════════════════════════════════════════════ */
function MachineDetectionOverlay() {
  const [logs, setLogs] = useState<ReturnType<typeof generateLogEntry>[]>([]);
  const logEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const interval = setInterval(() => {
      setLogs((prev) => {
        const next = [...prev, generateLogEntry()];
        if (next.length > 50) return next.slice(-50);
        return next;
      });
    }, 500);
    return () => clearInterval(interval);
  }, []);

  // Auto-scroll
  useEffect(() => {
    if (logEndRef.current) {
      logEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [logs]);

  return (
    <section
      className="w-full py-20 md:py-24 px-6"
      style={{ backgroundColor: 'var(--spectrum-void)' }}
    >
      <div className="max-w-[1440px] mx-auto grid grid-cols-1 lg:grid-cols-5 gap-10">
        {/* Left column: Title + Description + Log */}
        <div className="lg:col-span-3 flex flex-col gap-6">
          <AuthorityReveal delay={0}>
            <h2
              className="text-h2 font-noto-serif"
              style={{ color: 'var(--spectrum-peak)' }}
            >
              机器识别层
            </h2>
          </AuthorityReveal>

          <AuthorityReveal delay={100}>
            <p
              className="text-body font-noto-sans"
              style={{
                color: 'var(--spectrum-medium)',
                lineHeight: 1.8,
                maxWidth: 480,
              }}
            >
              跑马灯不只是给人看的。机器的识别层在每一帧扫描每一个色块，精确读取RGB值，与不动点数据库比对。ΔE = 0 是识别标准。任何偏差超过 ΔE &lt; 1 的色块将被标记为异常。
            </p>
          </AuthorityReveal>

          {/* Detection log panel */}
          <AuthorityReveal delay={200}>
            <GlassPanel className="p-5 min-h-[280px] flex flex-col">
              {/* Log header */}
              <div className="flex items-center gap-2 mb-4 pb-3" style={{ borderBottom: '1px solid var(--spectrum-border)' }}>
                <Radio size={14} style={{ color: 'var(--dragon-gold)' }} />
                <span
                  className="text-label"
                  style={{ color: 'var(--dragon-gold)', textTransform: 'none' }}
                >
                  实时检测日志
                </span>
                <span
                  className="text-code"
                  style={{
                    color: 'var(--dragon-gold)',
                    animation: 'blink-cursor 1s step-end infinite',
                  }}
                >
                  █
                </span>
              </div>

              {/* Log entries */}
              <div
                className="flex-1 overflow-y-auto font-mono text-left"
                style={{
                  maxHeight: 320,
                  fontFamily: "'JetBrains Mono', monospace",
                  fontSize: 11,
                  lineHeight: 2,
                }}
              >
                {logs.map((log, idx) => (
                  <motion.div
                    key={log.frame}
                    initial={{ opacity: 0, y: 8 }}
                    animate={{ opacity: idx < logs.length - 6 ? 0.4 : 1, y: 0 }}
                    transition={{ duration: 0.2 }}
                    className="whitespace-nowrap"
                  >
                    {/* Timestamp */}
                    <span style={{ color: 'var(--spectrum-dim)' }}>
                      {log.time}
                    </span>
                    {' '}
                    {/* Scan info */}
                    <span style={{ color: 'var(--spectrum-medium)' }}>
                      SCAN frame#{log.frame} → color[{log.color.id}] = {log.color.hex}
                    </span>
                    {' '}
                    {/* Match */}
                    <span style={{ color: log.color.hex }}>
                      → MATCH({log.color.enLabel.split(' / ')[0]}) → ΔE: {log.deltaE} ✓
                    </span>
                  </motion.div>
                ))}
                <div ref={logEndRef} />
              </div>
            </GlassPanel>
          </AuthorityReveal>
        </div>

        {/* Right column: Machine vision image */}
        <AuthorityReveal delay={300} className="lg:col-span-2 flex flex-col items-center justify-center">
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.5, delay: 0.3 }}
            className="w-full"
          >
            <img
              src="/machine-vision.jpg"
              alt="机器视觉识别示意"
              className="w-full rounded-2xl object-cover"
              style={{
                maxHeight: 400,
                boxShadow: '0 8px 32px rgba(0, 0, 0, 0.4)',
              }}
            />
            <p
              className="text-caption text-center mt-4"
              style={{ color: 'var(--spectrum-dim)' }}
            >
              机器视觉识别示意——每一帧精确到像素级
            </p>
          </motion.div>
        </AuthorityReveal>
      </div>
    </section>
  );
}

/* ═══════════════════════════════════════════════════════════
   Main Page — Marquee
   ═══════════════════════════════════════════════════════════ */
export default function Marquee() {
  const [settings, setSettings] = useState<MarqueeSettings>({
    speed: 20,
    direction: 'left',
    mode: 'continuous',
    isPlaying: true,
  });

  return (
    <div className="w-full" style={{ backgroundColor: 'var(--spectrum-void)' }}>
      {/* Inject CSS keyframes */}
      <MarqueeKeyframes />

      {/* Section 1: Signal Tower Hero */}
      <SignalTowerHero settings={settings} />

      {/* Section 2: Main Marquee Display */}
      <MainMarqueeDisplay settings={settings} />

      {/* Section 3: Control Panel */}
      <ControlPanel settings={settings} onSettingsChange={setSettings} />

      {/* Section 4: Color Meaning Reference */}
      <ColorMeaningReference settings={settings} />

      {/* Section 5: Machine Detection Overlay */}
      <MachineDetectionOverlay />
    </div>
  );
}
