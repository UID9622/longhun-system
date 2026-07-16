import { useEffect, useState, memo } from 'react';
import { Lock } from 'lucide-react';

interface ColorSwatchProps {
  color: string;
  name: string;
  hex: string;
  tag: string;
  tagColor?: string;
  tagTextColor?: string;
  size?: number;
  showLock?: boolean;
  animatePulse?: boolean;
}

function getPulseAnimation(hex: string): string {
  switch (hex.toUpperCase()) {
    case '#00C853':
      return 'animate-color-pulse-green';
    case '#FF3D00':
      return 'animate-color-pulse-red';
    case '#FFD600':
      return 'animate-color-pulse-yellow';
    case '#FFD700':
      return 'animate-color-pulse-gold';
    default:
      return '';
  }
}

const ColorSwatch = memo(function ColorSwatch({
  color,
  name,
  hex,
  tag,
  tagColor,
  tagTextColor,
  size = 120,
  showLock = false,
  animatePulse = false,
}: ColorSwatchProps) {
  const [locked, setLocked] = useState(false);

  useEffect(() => {
    if (showLock) {
      const timer = setTimeout(() => setLocked(true), 300);
      return () => clearTimeout(timer);
    }
  }, [showLock]);

  const pulseClass = animatePulse ? getPulseAnimation(hex) : '';

  return (
    <div className="flex flex-col items-center gap-3 select-none">
      {/* Color square */}
      <div
        className={`relative rounded-2xl transition-transform duration-300 hover:scale-108 ${pulseClass}`}
        style={{
          width: size,
          height: size,
          backgroundColor: color,
          border:
            hex.toUpperCase() === '#1A1A2E'
              ? '2px solid var(--spectrum-border)'
              : 'none',
        }}
      >
        {showLock && (
          <div
            className="absolute top-2 right-2 flex items-center justify-center rounded-full"
            style={{
              width: 24,
              height: 24,
              backgroundColor: 'rgba(255, 215, 0, 0.2)',
              transform: locked ? 'scale(1)' : 'scale(0)',
              transition: 'transform 0.4s cubic-bezier(0.16, 1, 0.3, 1)',
            }}
          >
            <Lock size={12} color="var(--dragon-gold)" strokeWidth={2} />
          </div>
        )}
      </div>

      {/* Color name */}
      <span
        className="text-h3 font-noto-serif"
        style={{ color: 'var(--spectrum-peak)' }}
      >
        {name}
      </span>

      {/* Hex code */}
      <span
        className="text-code"
        style={{ color: 'var(--spectrum-dim)' }}
      >
        {hex}
      </span>

      {/* Meaning tag */}
      <span
        className="text-label px-3 py-1 rounded-full"
        style={{
          backgroundColor: tagColor || color,
          color: tagTextColor || '#FFFFFF',
        }}
      >
        {tag}
      </span>
    </div>
  );
});

export default ColorSwatch;
