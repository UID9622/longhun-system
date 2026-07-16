import { memo } from 'react';
import { COLOR_SEGMENTS } from './types';
import type { MarqueeSettings } from './types';

interface MarqueeStripProps {
  settings: MarqueeSettings;
  height?: number;
  segmentMinWidth?: number;
  showDetails?: boolean;
}

/**
 * Reusable MarqueeStrip component.
 * Renders 3x duplicated segments for seamless CSS loop.
 * Pure CSS animation — no JS-driven animation.
 */
const MarqueeStrip = memo(function MarqueeStrip({
  settings,
  height = 120,
  segmentMinWidth = 280,
  showDetails = true,
}: MarqueeStripProps) {
  const { speed, direction, mode, isPlaying } = settings;

  // Build segments array: 3 copies of 7 = 21 segments for seamless loop
  const segments = Array.from({ length: 21 }, (_, i) => ({
    ...COLOR_SEGMENTS[i % 7],
    uniqueId: i,
  }));

  const animDirection = direction === 'left' ? 'marquee-flow-left' : 'marquee-flow-right';
  const animDuration = `${speed}s`;

  const getPulseAnimation = (idx: number) => {
    if (mode === 'pulse') {
      return `color-pulse-${idx % 7} 2s ease-in-out infinite`;
    }
    if (mode === 'segment') {
      return `segment-flash 1.5s ease-in-out infinite`;
    }
    return 'none';
  };

  const getPulseDelay = (idx: number) => {
    if (mode === 'pulse') {
      const delays = [0, 0.3, 0.6, 0.9, 1.2, 1.5, 1.8];
      return `${delays[idx % 7]}s`;
    }
    if (mode === 'segment') {
      return `${(idx % 7) * 0.2}s`;
    }
    return '0s';
  };

  return (
    <div
      className="relative w-full overflow-hidden"
      style={{ height }}
    >
      {/* Edge fade gradients */}
      <div
        className="absolute top-0 left-0 bottom-0 z-10 pointer-events-none"
        style={{
          width: 120,
          background: 'linear-gradient(to right, var(--spectrum-shadow), transparent)',
        }}
      />
      <div
        className="absolute top-0 right-0 bottom-0 z-10 pointer-events-none"
        style={{
          width: 120,
          background: 'linear-gradient(to left, var(--spectrum-shadow), transparent)',
        }}
      />

      {/* Scrolling track */}
      <div
        className={`marquee-track flex items-center h-full ${!isPlaying ? 'paused' : ''}`}
        style={{
          animationName: animDirection,
          animationDuration: animDuration,
          animationTimingFunction: 'linear',
          animationIterationCount: 'infinite',
          width: 'fit-content',
        }}
      >
        {segments.map((seg, idx) => (
          <div
            key={seg.uniqueId}
            className="flex-shrink-0 flex flex-col justify-center items-center relative"
            style={{
              minWidth: segmentMinWidth,
              height: height - 16,
              borderRadius: 12,
              margin: '0 8px',
              backgroundColor: seg.hex,
              animation: getPulseAnimation(idx),
              animationDelay: getPulseDelay(idx),
              boxShadow: mode === 'continuous'
                ? 'inset 0 0 40px rgba(255,255,255,0.1)'
                : undefined,
            }}
          >
            {showDetails && (
              <>
                {/* Status name */}
                <span
                  className="text-h2 font-noto-serif"
                  style={{
                    color: seg.textColor,
                    fontSize: height > 80 ? undefined : 'clamp(16px, 2vw, 24px)',
                    textShadow: seg.hex === '#1A1A2E' ? '0 0 8px rgba(138,138,181,0.5)' : 'none',
                  }}
                >
                  {seg.name}
                </span>

                {/* Label */}
                <span
                  className="text-label mt-1"
                  style={{
                    color: seg.textColor,
                    opacity: 0.8,
                    fontSize: 10,
                  }}
                >
                  {seg.label}
                </span>

                {/* Hex code */}
                <span
                  className="text-code absolute bottom-2 right-3"
                  style={{
                    color: seg.textColor,
                    opacity: 0.6,
                    fontSize: 11,
                  }}
                >
                  {seg.hex}
                </span>
              </>
            )}
          </div>
        ))}
      </div>
    </div>
  );
});

export default MarqueeStrip;
