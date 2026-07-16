import { useEffect, useState, useRef, memo } from 'react';

interface WeightDisplayProps {
  value: number;
  label: string;
  sublabel: string;
  color: string;
  delay?: number;
  showBadge?: boolean;
  badgeText?: string;
}

const WeightDisplay = memo(function WeightDisplay({
  value,
  label,
  sublabel,
  color,
  delay = 0,
  showBadge = false,
  badgeText = '',
}: WeightDisplayProps) {
  const [displayValue, setDisplayValue] = useState(0);
  const [hasAnimated, setHasAnimated] = useState(false);
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        if (entries[0].isIntersecting && !hasAnimated) {
          setHasAnimated(true);
          const startTime = Date.now();
          const duration = 1200;
          const startDelay = delay;

          const animate = () => {
            const elapsed = Date.now() - startTime - startDelay;
            if (elapsed < 0) {
              requestAnimationFrame(animate);
              return;
            }
            const progress = Math.min(elapsed / duration, 1);
            // cubic-bezier(0.16, 1, 0.3, 1) approximation
            const eased = 1 - Math.pow(1 - progress, 3);
            setDisplayValue(eased * value);
            if (progress < 1) {
              requestAnimationFrame(animate);
            }
          };
          requestAnimationFrame(animate);
        }
      },
      { threshold: 0.3 }
    );

    if (ref.current) {
      observer.observe(ref.current);
    }

    return () => observer.disconnect();
  }, [value, delay, hasAnimated]);

  const formattedValue = displayValue.toFixed(2);

  return (
    <div ref={ref} className="flex flex-col items-center gap-4 relative">
      {/* Badge */}
      {showBadge && (
        <div
          className="absolute top-0 right-0 text-label px-2 py-1 rounded-full"
          style={{
            backgroundColor: 'var(--dragon-green)',
            color: 'var(--spectrum-void)',
          }}
        >
          {badgeText}
        </div>
      )}

      {/* Label */}
      <span
        className="text-label font-noto-sans"
        style={{ color: 'var(--spectrum-dim)' }}
      >
        {label}
      </span>

      {/* Number */}
      <span
        className="font-jetbrain tabular-nums"
        style={{
          fontSize: 'clamp(64px, 10vw, 120px)',
          fontWeight: 700,
          color,
          lineHeight: 1,
        }}
      >
        {formattedValue}
      </span>

      {/* Sublabel */}
      <span
        className="text-h3 font-noto-serif"
        style={{ color: 'var(--spectrum-peak)' }}
      >
        {sublabel}
      </span>

      {/* Progress bar */}
      <div
        className="w-full h-1.5 rounded-full overflow-hidden"
        style={{ backgroundColor: 'var(--spectrum-border)' }}
      >
        <div
          className="h-full rounded-full transition-all duration-1000"
          style={{
            width: `${displayValue * 100}%`,
            backgroundColor: color,
          }}
        />
      </div>
    </div>
  );
});

export default WeightDisplay;
