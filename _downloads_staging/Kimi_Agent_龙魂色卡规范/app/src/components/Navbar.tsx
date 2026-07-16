import { useEffect, useState } from 'react';
import { Link, useLocation } from 'react-router';

const navLinks = [
  { label: '不动点', path: '/colors' },
  { label: '权重面板', path: '/weights' },
  { label: '七彩跑马灯', path: '/marquee' },
  { label: '各国色卡', path: '/comparison' },
];

export default function Navbar() {
  const location = useLocation();
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    requestAnimationFrame(() => setMounted(true));
  }, []);

  return (
    <nav
      className="fixed top-0 left-0 right-0 z-50 h-16 flex items-center justify-between px-6 md:px-12"
      style={{
        background: 'var(--glass-panel)',
        backdropFilter: 'blur(16px)',
        WebkitBackdropFilter: 'blur(16px)',
        borderBottom: '1px solid var(--glass-border)',
        transform: mounted ? 'translateY(0)' : 'translateY(-64px)',
        transition: 'transform 0.5s cubic-bezier(0.16, 1, 0.3, 1)',
      }}
    >
      {/* Left: Brand mark */}
      <Link to="/" className="flex items-center gap-2 group">
        <img
          src="/dragon-mark.png"
          alt="龙"
          className="h-8 w-8 object-contain"
        />
        <span
          className="text-label font-noto-serif"
          style={{ color: 'var(--dragon-gold)' }}
        >
          龙魂生态
        </span>
        <span
          className="inline-block w-1 h-1 rounded-full animate-pulse"
          style={{ backgroundColor: 'var(--dragon-green)' }}
        />
      </Link>

      {/* Center: Nav links */}
      <div className="hidden md:flex items-center gap-8">
        {navLinks.map((link) => (
          <Link
            key={link.path}
            to={link.path}
            className="text-label font-noto-sans relative py-1 transition-colors duration-300 hover:text-[var(--dragon-gold)]"
            style={{
              color:
                location.pathname === link.path
                  ? 'var(--dragon-gold)'
                  : 'var(--spectrum-medium)',
            }}
          >
            {link.label}
            {location.pathname === link.path && (
              <span
                className="absolute bottom-0 left-0 right-0 h-0.5"
                style={{ backgroundColor: 'var(--dragon-gold)' }}
              />
            )}
          </Link>
        ))}
      </div>

      {/* Right: Authority score badge */}
      <div
        className="flex items-center gap-2 px-3 py-1.5 rounded-full text-label"
        style={{
          backgroundColor: 'rgba(0, 200, 83, 0.15)',
          color: 'var(--dragon-green)',
        }}
      >
        <span className="font-noto-sans">权威值: 97.3</span>
        <span className="inline-block w-1.5 h-1.5 rounded-full animate-pulse" style={{ backgroundColor: 'var(--dragon-green)' }} />
      </div>
    </nav>
  );
}
