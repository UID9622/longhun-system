import { useRef, useState, useEffect, memo, useCallback } from 'react';
import type { ReactNode } from 'react';
import { Link } from 'react-router';
import { motion, useMotionValue, useTransform } from 'framer-motion';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { Lock, BookOpen, Crown, Grid3X3 } from 'lucide-react';

import GlassPanel from '@/components/GlassPanel';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';

import {
  IMMUTABLE_COLORS,
  COLOR_SPACE_DATA,
  IMMUTABILITY_RULES,
} from './colors/data';
import type { ImmutableColor, ImmutabilityRule } from './colors/data';

/* ──────────────────────────────────────────────
   GSAP Plugin Registration
   ────────────────────────────────────────────── */
gsap.registerPlugin(ScrollTrigger);

/* ──────────────────────────────────────────────
   Easing Constants
   ────────────────────────────────────────────── */
const EASE_SNAP = 'cubic-bezier(0.16, 1, 0.3, 1)';

/* ──────────────────────────────────────────────
   Section 1: Hero — Color Constitution
   ────────────────────────────────────────────── */
function ColorHero() {
  const sectionRef = useRef<HTMLDivElement>(null);
  const titleRef = useRef<HTMLHeadingElement>(null);
  const statementRef = useRef<HTMLDivElement>(null);
  const metaRef = useRef<HTMLDivElement>(null);
  const swatchesRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const section = sectionRef.current;
    if (!section) return;

    const ctx = gsap.context(() => {
      // Breadcrumb fade in
      gsap.fromTo(
        '.hero-breadcrumb',
        { opacity: 0 },
        { opacity: 1, duration: 0.4, delay: 0.1, ease: 'power3.out' }
      );

      // Title word reveal
      if (titleRef.current) {
        const words = titleRef.current.querySelectorAll('.hero-word');
        gsap.fromTo(
          words,
          { y: 60, opacity: 0 },
          {
            y: 0,
            opacity: 1,
            duration: 0.5,
            stagger: 0.1,
            ease: 'power3.out',
            delay: 0.3,
          }
        );
      }

      // Statement reveal
      if (statementRef.current) {
        gsap.fromTo(
          statementRef.current,
          { y: 60, opacity: 0 },
          { y: 0, opacity: 1, duration: 0.5, ease: 'power3.out', delay: 0.9 }
        );
      }

      // Metadata stagger
      if (metaRef.current) {
        const items = metaRef.current.querySelectorAll('.meta-item');
        gsap.fromTo(
          items,
          { y: 30, opacity: 0 },
          {
            y: 0,
            opacity: 1,
            duration: 0.5,
            stagger: 0.08,
            ease: 'power3.out',
            delay: 1.3,
          }
        );
      }

      // Mini swatches lock animation
      if (swatchesRef.current) {
        const swatches = swatchesRef.current.querySelectorAll('.mini-swatch');
        gsap.fromTo(
          swatches,
          { scale: 0, opacity: 0 },
          {
            scale: 1,
            opacity: 1,
            duration: 0.4,
            stagger: 0.1,
            ease: 'back.out(1.7)',
            delay: 1.7,
          }
        );
      }
    }, section);

    return () => ctx.revert();
  }, []);

  const titleWords = ['不动点', '五主色'];

  return (
    <section
      ref={sectionRef}
      className="relative w-full flex items-center overflow-hidden"
      style={{
        minHeight: '70vh',
        backgroundColor: 'var(--spectrum-void)',
      }}
    >
      {/* Grid background */}
      <div
        className="absolute inset-0 opacity-30"
        style={{
          backgroundImage: 'url(/grid-bg.png)',
          backgroundRepeat: 'repeat',
          backgroundSize: '400px 400px',
        }}
      />

      <div className="relative z-10 max-w-[1440px] mx-auto w-full px-6 md:px-12 py-24">
        {/* Breadcrumb */}
        <div className="hero-breadcrumb mb-6" style={{ opacity: 0 }}>
          <span
            className="text-label font-jetbrain"
            style={{ color: 'var(--spectrum-dim)' }}
          >
            <Link
              to="/"
              className="hover:text-[var(--dragon-gold)] transition-colors"
            >
              龙魂生态
            </Link>
            {' / '}
            <span style={{ color: 'var(--spectrum-medium)' }}>
              不动点协议
            </span>
          </span>
        </div>

        {/* Page title */}
        <h1
          ref={titleRef}
          className="text-hero font-noto-serif mb-8"
          style={{ color: 'var(--spectrum-peak)' }}
        >
          {titleWords.map((word, i) => (
            <span
              key={i}
              className="hero-word inline-block mr-4 opacity-0"
            >
              {word === '不动点' ? (
                <span
                  style={{
                    borderBottom: '4px solid var(--dragon-gold)',
                    paddingBottom: '8px',
                  }}
                >
                  {word}
                </span>
              ) : (
                word
              )}
            </span>
          ))}
        </h1>

        {/* Protocol statement */}
        <div
          ref={statementRef}
          className="max-w-[680px] mb-8 opacity-0"
          style={{
            borderLeft: '3px solid var(--dragon-red)',
            paddingLeft: '20px',
          }}
        >
          <p
            className="text-body-lg font-noto-sans"
            style={{
              color: 'var(--spectrum-medium)',
              lineHeight: 1.9,
            }}
          >
            以下五种颜色为龙魂生态的不动点。其色值、含义、优先级、在光谱中的相对位置——自系统启动之日起，永恒不变。任何试图修改此页面的行为将被标记为红色熔断状态。
          </p>
        </div>

        {/* Protocol metadata row */}
        <div ref={metaRef} className="flex flex-wrap gap-8 mb-10">
          <span
            className="meta-item text-code font-jetbrain opacity-0"
            style={{ color: 'var(--spectrum-dim)' }}
          >
            协议版本: v2.4.0-FIXED
          </span>
          <span
            className="meta-item text-code font-jetbrain opacity-0"
            style={{ color: 'var(--spectrum-dim)' }}
          >
            最后审计: 2025-01-15
          </span>
          <span className="meta-item opacity-0 flex items-center gap-2">
            <span
              className="text-code font-jetbrain"
              style={{ color: 'var(--spectrum-dim)' }}
            >
              状态:
            </span>
            <span
              className="text-label px-3 py-1 rounded-full border"
              style={{
                borderColor: 'var(--dragon-green)',
                color: 'var(--dragon-green)',
              }}
            >
              {'\u2713'} 不可变
            </span>
          </span>
          <span
            className="meta-item text-code font-jetbrain opacity-0"
            style={{ color: 'var(--spectrum-dim)' }}
          >
            审计人: 龙魂治理层
          </span>
        </div>

        {/* Five mini swatches */}
        <div ref={swatchesRef} className="flex gap-4">
          {IMMUTABLE_COLORS.map((c) => (
            <div
              key={c.hex}
              className="mini-swatch relative rounded-full opacity-0"
              style={{
                width: 40,
                height: 40,
                backgroundColor: c.hex,
                border: '2px solid var(--spectrum-peak)',
              }}
            >
              <div
                className="absolute -bottom-1 -right-1 flex items-center justify-center rounded-full"
                style={{
                  width: 16,
                  height: 16,
                  backgroundColor: 'var(--dragon-gold)',
                }}
              >
                <Lock size={8} color="var(--spectrum-void)" strokeWidth={3} />
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

/* ──────────────────────────────────────────────
   TiltCard — Isolated Framer Motion component
   ────────────────────────────────────────────── */
interface TiltCardProps {
  children: ReactNode;
  className?: string;
}

const TiltCard = memo(function TiltCard({ children, className = '' }: TiltCardProps) {
  const x = useMotionValue(0);
  const y = useMotionValue(0);
  const rotateX = useTransform(y, [-150, 150], [2, -2]);
  const rotateY = useTransform(x, [-150, 150], [-2, 2]);

  const handleMouseMove = useCallback(
    (e: React.MouseEvent<HTMLDivElement>) => {
      const rect = e.currentTarget.getBoundingClientRect();
      const cx = rect.left + rect.width / 2;
      const cy = rect.top + rect.height / 2;
      x.set(e.clientX - cx);
      y.set(e.clientY - cy);
    },
    [x, y]
  );

  const handleMouseLeave = useCallback(() => {
    x.set(0);
    y.set(0);
  }, [x, y]);

  return (
    <motion.div
      className={className}
      style={{
        perspective: 1000,
        rotateX,
        rotateY,
        transformStyle: 'preserve-3d',
      }}
      onMouseMove={handleMouseMove}
      onMouseLeave={handleMouseLeave}
    >
      {children}
    </motion.div>
  );
});

/* ──────────────────────────────────────────────
   HexTyping — Character-by-character reveal
   ────────────────────────────────────────────── */
const HexTyping = memo(function HexTyping({
  hex,
  color,
  trigger,
}: {
  hex: string;
  color: string;
  trigger: boolean;
}) {
  const [displayed, setDisplayed] = useState('');

  useEffect(() => {
    if (!trigger) return;
    let i = 0;
    const interval = setInterval(() => {
      i++;
      setDisplayed(hex.slice(0, i));
      if (i >= hex.length) clearInterval(interval);
    }, 50);
    return () => clearInterval(interval);
  }, [trigger, hex]);

  return (
    <span className="font-jetbrain" style={{ color }}>
      {trigger ? displayed : ''}
      <span
        className="inline-block w-[2px] h-[1em] ml-0.5 align-middle"
        style={{
          backgroundColor: color,
          opacity: displayed.length < hex.length && trigger ? 1 : 0,
          animation: displayed.length < hex.length && trigger ? 'caret-blink 1s infinite' : 'none',
        }}
      />
    </span>
  );
});

/* ──────────────────────────────────────────────
   Section 2: Color Detail Card
   ────────────────────────────────────────────── */
function ColorDetailCard({
  color,
}: {
  color: ImmutableColor;
}) {
  const cardRef = useRef<HTMLDivElement>(null);
  const [hexTriggered, setHexTriggered] = useState(false);
  const [locked, setLocked] = useState(false);

  useEffect(() => {
    const card = cardRef.current;
    if (!card) return;

    const ctx = gsap.context(() => {
      gsap.fromTo(
        card,
        { y: 60, opacity: 0 },
        {
          y: 0,
          opacity: 1,
          duration: 0.5,
          ease: 'power3.out',
          scrollTrigger: {
            trigger: card,
            start: 'top 80%',
            once: true,
          },
          onComplete: () => {
            setHexTriggered(true);
            setTimeout(() => setLocked(true), 500);
          },
        }
      );
    }, card);

    return () => ctx.revert();
  }, []);

  const isDarkText = color.hex === '#1A1A2E';

  return (
    <div ref={cardRef} className="opacity-0">
      <TiltCard className="w-full">
        <GlassPanel className="p-8 md:p-10">
          <div className="flex flex-col lg:flex-row gap-10">
            {/* Left column (60%) */}
            <div className="lg:w-[60%] relative">
              {/* Watermark index */}
              <span
                className="absolute top-0 left-0 font-jetbrain pointer-events-none select-none hidden md:block"
                style={{
                  fontSize: '96px',
                  color: 'var(--spectrum-border)',
                  lineHeight: 1,
                  zIndex: 0,
                }}
              >
                {color.index}
              </span>

              <div className="relative z-10 pt-4">
                {/* Color name */}
                <h2
                  className="text-h1 font-noto-serif mb-2"
                  style={{ color: color.textColor }}
                >
                  {color.name}
                </h2>

                {/* English name */}
                <p
                  className="text-label font-jetbrain mb-6"
                  style={{ color: 'var(--spectrum-dim)' }}
                >
                  {color.englishName} — {color.englishSubtitle}
                </p>

                {/* Meaning block */}
                <p
                  className="text-h3 font-noto-serif mb-4"
                  style={{ color: color.textColor }}
                >
                  {color.meaning}
                </p>

                <p
                  className="text-body font-noto-sans mb-6 max-w-[480px]"
                  style={{
                    color: 'var(--spectrum-medium)',
                    lineHeight: 1.8,
                  }}
                >
                  {color.description}
                </p>

                {/* Usage bullets */}
                <ul className="space-y-2 mb-8">
                  {color.bullets.map((b) => (
                    <li key={b} className="flex items-start gap-3">
                      <span
                        className="w-2 h-2 rounded-full mt-1.5 flex-shrink-0"
                        style={{
                          backgroundColor:
                            color.hex === '#1A1A2E'
                              ? 'var(--spectrum-dim)'
                              : color.hex,
                        }}
                      />
                      <span
                        className="text-body font-noto-sans"
                        style={{ color: 'var(--spectrum-medium)' }}
                      >
                        {b}
                      </span>
                    </li>
                  ))}
                </ul>

                {/* Hex display */}
                <div>
                  <div
                    className="font-jetbrain mb-1"
                    style={{ fontSize: '48px', color: color.textColor }}
                  >
                    <HexTyping
                      hex={color.hex}
                      color={color.textColor}
                      trigger={hexTriggered}
                    />
                  </div>
                  <span
                    className="text-code font-jetbrain"
                    style={{ color: 'var(--spectrum-dim)' }}
                  >
                    {color.rgb}
                  </span>
                </div>
              </div>
            </div>

            {/* Right column (40%) */}
            <div className="lg:w-[40%] flex flex-col items-center lg:items-end">
              {/* Large color swatch */}
              <div className="relative mb-6">
                <div
                  className={`rounded-[20px] ${color.pulseClass || ''}`}
                  style={{
                    width: 280,
                    height: 280,
                    backgroundColor: color.hex,
                    border: isDarkText
                      ? '3px solid var(--spectrum-border)'
                      : `3px solid ${color.hex}80`,
                  }}
                />

                {/* Lock badge */}
                <div
                  className="absolute -bottom-3 -right-3 flex items-center gap-1.5 px-3 py-1.5 rounded-full"
                  style={{
                    backgroundColor: 'var(--dragon-gold)',
                    transform: locked ? 'scale(1)' : 'scale(0)',
                    transition:
                      'transform 0.3s cubic-bezier(0.16, 1, 0.3, 1)',
                  }}
                >
                  <Lock
                    size={12}
                    color="var(--spectrum-void)"
                    strokeWidth={2.5}
                  />
                  <span
                    className="text-label font-jetbrain"
                    style={{
                      color: 'var(--spectrum-void)',
                      fontSize: '10px',
                      fontWeight: 700,
                    }}
                  >
                    IMMUTABLE
                  </span>
                </div>
              </div>

              {/* Machine recognition panel */}
              <GlassPanel className="w-full max-w-[280px] p-4">
                <p
                  className="text-label font-noto-sans mb-3"
                  style={{ color: 'var(--spectrum-dim)' }}
                >
                  机器识别结果
                </p>
                <div className="space-y-1.5 font-jetbrain text-code">
                  <p style={{ color: 'var(--spectrum-medium)' }}>
                    HSL: {color.hsl}
                  </p>
                  <p style={{ color: 'var(--spectrum-medium)' }}>
                    LAB: {color.lab}
                  </p>
                  <p style={{ color: 'var(--dragon-green)' }}>
                    {'\u0394'}E to base: 0.00 (IDENTICAL)
                  </p>
                </div>
              </GlassPanel>
            </div>
          </div>
        </GlassPanel>
      </TiltCard>
    </div>
  );
}

function ColorCardsSection() {
  return (
    <section
      className="w-full py-24 md:py-32"
      style={{ backgroundColor: 'var(--spectrum-shadow)' }}
    >
      <div className="max-w-[1440px] mx-auto px-6 md:px-12 space-y-12">
        {IMMUTABLE_COLORS.map((color) => (
          <ColorDetailCard key={color.hex} color={color} />
        ))}
      </div>
    </section>
  );
}

/* ──────────────────────────────────────────────
   Section 3: Machine Recognition Proof
   ────────────────────────────────────────────── */
function MachineProofSection() {
  const sectionRef = useRef<HTMLDivElement>(null);
  const leftRef = useRef<HTMLDivElement>(null);
  const tableRef = useRef<HTMLDivElement>(null);
  const imgRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const section = sectionRef.current;
    if (!section) return;

    const ctx = gsap.context(() => {
      // Left column reveal
      if (leftRef.current) {
        const children = leftRef.current.querySelectorAll('.reveal-item');
        gsap.fromTo(
          children,
          { y: 40, opacity: 0 },
          {
            y: 0,
            opacity: 1,
            duration: 0.5,
            stagger: 0.1,
            ease: 'power3.out',
            scrollTrigger: {
              trigger: leftRef.current,
              start: 'top 80%',
              once: true,
            },
          }
        );
      }

      // Table rows stagger
      if (tableRef.current) {
        const rows = tableRef.current.querySelectorAll('.proof-row');
        gsap.fromTo(
          rows,
          { x: -20, opacity: 0 },
          {
            x: 0,
            opacity: 1,
            duration: 0.4,
            stagger: 0.06,
            ease: 'power3.out',
            scrollTrigger: {
              trigger: tableRef.current,
              start: 'top 85%',
              once: true,
            },
          }
        );
      }

      // Image reveal
      if (imgRef.current) {
        gsap.fromTo(
          imgRef.current,
          { scale: 0.95, opacity: 0 },
          {
            scale: 1,
            opacity: 1,
            duration: 0.6,
            ease: 'power3.out',
            scrollTrigger: {
              trigger: imgRef.current,
              start: 'top 80%',
              once: true,
            },
          }
        );
      }
    }, section);

    return () => ctx.revert();
  }, []);

  return (
    <section
      ref={sectionRef}
      className="w-full py-20 md:py-24"
      style={{ backgroundColor: 'var(--spectrum-void)' }}
    >
      <div className="max-w-[1440px] mx-auto px-6 md:px-12">
        <div className="flex flex-col lg:flex-row gap-12">
          {/* Left column (55%) */}
          <div ref={leftRef} className="lg:w-[55%]">
            <h2
              className="reveal-item text-h1 font-noto-serif mb-6 opacity-0"
              style={{ color: 'var(--spectrum-peak)' }}
            >
              机器识色 · 人眼不变
            </h2>

            <p
              className="reveal-item text-body-lg font-noto-sans mb-8 max-w-[520px] opacity-0"
              style={{
                color: 'var(--spectrum-medium)',
                lineHeight: 1.9,
              }}
            >
              机器读取的是色值——十六进制、RGB、HSL、LAB。每一种表示方法都精确指向同一个点。人眼看到的是习惯——绿是通行，红是危险，金是主权。机器能检测出色卡扩展中新增的每一个附加色，但它永远首先识别出这五个不动点。这叫做规矩。
            </p>

            {/* Proof data table */}
            <div ref={tableRef} className="reveal-item opacity-0">
              <GlassPanel className="p-6 overflow-x-auto">
                <Table>
                  <TableHeader>
                    <TableRow
                      style={{
                        borderColor: 'var(--spectrum-border)',
                      }}
                    >
                      <TableHead
                        className="text-code font-jetbrain"
                        style={{ color: 'var(--spectrum-dim)' }}
                      >
                        Color
                      </TableHead>
                      <TableHead
                        className="text-code font-jetbrain"
                        style={{ color: 'var(--spectrum-dim)' }}
                      >
                        Hex
                      </TableHead>
                      <TableHead
                        className="text-code font-jetbrain hidden md:table-cell"
                        style={{ color: 'var(--spectrum-dim)' }}
                      >
                        RGB
                      </TableHead>
                      <TableHead
                        className="text-code font-jetbrain hidden lg:table-cell"
                        style={{ color: 'var(--spectrum-dim)' }}
                      >
                        HSL
                      </TableHead>
                      <TableHead
                        className="text-code font-jetbrain hidden sm:table-cell"
                        style={{ color: 'var(--spectrum-dim)' }}
                      >
                        LAB
                      </TableHead>
                      <TableHead
                        className="text-code font-jetbrain"
                        style={{ color: 'var(--spectrum-dim)' }}
                      >
                        {'\u0394'}E
                      </TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {COLOR_SPACE_DATA.map((row) => (
                      <TableRow
                        key={row.hex}
                        className="proof-row"
                        style={{
                          borderColor: 'var(--spectrum-border)',
                        }}
                      >
                        <TableCell
                          className="text-code font-jetbrain font-medium"
                          style={{ color: row.textColor }}
                        >
                          {row.name}
                        </TableCell>
                        <TableCell
                          className="text-code font-jetbrain"
                          style={{ color: row.textColor }}
                        >
                          {row.hex}
                        </TableCell>
                        <TableCell
                          className="text-code font-jetbrain hidden md:table-cell"
                          style={{ color: 'var(--spectrum-dim)' }}
                        >
                          {row.rgb}
                        </TableCell>
                        <TableCell
                          className="text-code font-jetbrain hidden lg:table-cell"
                          style={{ color: 'var(--spectrum-dim)' }}
                        >
                          {row.hsl}
                        </TableCell>
                        <TableCell
                          className="text-code font-jetbrain hidden sm:table-cell"
                          style={{ color: 'var(--spectrum-dim)' }}
                        >
                          {row.lab}
                        </TableCell>
                        <TableCell
                          className="text-code font-jetbrain font-bold"
                          style={{ color: 'var(--dragon-green)' }}
                        >
                          {row.deltaE}
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </GlassPanel>
            </div>
          </div>

          {/* Right column (45%) */}
          <div ref={imgRef} className="lg:w-[45%] flex flex-col items-center opacity-0">
            <img
              src="/machine-vision.jpg"
              alt="机器视觉下的五主色识别"
              className="w-full rounded-2xl object-cover"
              style={{
                boxShadow: '0 0 40px rgba(255, 215, 0, 0.15)',
              }}
            />
            <p
              className="text-caption font-jetbrain text-center mt-4"
              style={{ color: 'var(--spectrum-dim)' }}
            >
              机器视觉下的五主色识别——每一种表示方式都指向同一个不动点
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}

/* ──────────────────────────────────────────────
   Rule Card — GSAP scroll reveal + Framer tilt
   ────────────────────────────────────────────── */
function RuleCardComponent({
  rule,
  cardIndex,
}: {
  rule: ImmutabilityRule;
  cardIndex: number;
}) {
  const cardRef = useRef<HTMLDivElement>(null);
  const [codeVisible, setCodeVisible] = useState(false);

  useEffect(() => {
    const card = cardRef.current;
    if (!card) return;

    const ctx = gsap.context(() => {
      const fromX = cardIndex % 2 === 0 ? -40 : 40;

      gsap.fromTo(
        card,
        { x: fromX, opacity: 0 },
        {
          x: 0,
          opacity: 1,
          duration: 0.5,
          ease: 'power3.out',
          scrollTrigger: {
            trigger: card,
            start: 'top 85%',
            once: true,
          },
          onComplete: () => {
            setTimeout(() => setCodeVisible(true), 300);
          },
        }
      );
    }, card);

    return () => ctx.revert();
  }, [cardIndex]);

  const iconMap = {
    lock: Lock,
    grid: Grid3X3,
    book: BookOpen,
    crown: Crown,
  };
  const IconComp = iconMap[rule.icon];

  return (
    <div ref={cardRef} className="opacity-0">
      <TiltCard className="h-full">
        <GlassPanel
          className="h-full p-6 md:p-8 flex flex-col"
          style={{
            border: '1px solid var(--glass-border)',
          }}
        >
          {/* Icon */}
          <div className="mb-4">
            <IconComp
              size={32}
              color="var(--dragon-gold)"
              strokeWidth={1.5}
            />
          </div>

          {/* Title */}
          <h3
            className="text-h2 font-noto-serif mb-3"
            style={{ color: 'var(--spectrum-peak)' }}
          >
            {rule.title}
          </h3>

          {/* Text */}
          <p
            className="text-body font-noto-sans mb-5 flex-1"
            style={{
              color: 'var(--spectrum-medium)',
              lineHeight: 1.8,
            }}
          >
            {rule.text}
          </p>

          {/* Code block */}
          <div
            className="rounded-md p-3 font-jetbrain text-code overflow-x-auto"
            style={{
              backgroundColor: `${rule.codeColor}14`,
              opacity: codeVisible ? 1 : 0,
              transform: codeVisible ? 'translateY(0)' : 'translateY(8px)',
              transition: `all 0.4s ${EASE_SNAP}`,
            }}
          >
            <span style={{ color: rule.codeColor }}>{rule.code}</span>
          </div>
        </GlassPanel>
      </TiltCard>
    </div>
  );
}

/* ──────────────────────────────────────────────
   Section 4: Immutability Rules
   ────────────────────────────────────────────── */
function ImmutabilityRulesSection() {
  const titleRef = useRef<HTMLHeadingElement>(null);

  useEffect(() => {
    const title = titleRef.current;
    if (!title) return;

    const ctx = gsap.context(() => {
      gsap.fromTo(
        title,
        { y: 40, opacity: 0 },
        {
          y: 0,
          opacity: 1,
          duration: 0.5,
          ease: 'power3.out',
          scrollTrigger: {
            trigger: title,
            start: 'top 85%',
            once: true,
          },
        }
      );
    }, title);

    return () => ctx.revert();
  }, []);

  return (
    <section
      className="w-full py-20 md:py-24"
      style={{ backgroundColor: 'var(--spectrum-shadow)' }}
    >
      <div className="max-w-[960px] mx-auto px-6 md:px-12">
        {/* Section title */}
        <h2
          ref={titleRef}
          className="text-h1 font-noto-serif text-center mb-12 opacity-0"
          style={{ color: 'var(--spectrum-peak)' }}
        >
          不动点铁律
        </h2>

        {/* Four rule cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {IMMUTABILITY_RULES.map((rule, i) => (
            <RuleCardComponent key={rule.title} rule={rule} cardIndex={i} />
          ))}
        </div>
      </div>
    </section>
  );
}

/* ──────────────────────────────────────────────
   Main Colors Page
   ────────────────────────────────────────────── */
export default function Colors() {
  return (
    <div className="w-full">
      <ColorHero />
      <ColorCardsSection />
      <MachineProofSection />
      <ImmutabilityRulesSection />
    </div>
  );
}
