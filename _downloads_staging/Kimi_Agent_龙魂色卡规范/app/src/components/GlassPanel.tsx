import { forwardRef } from 'react';
import type { ReactNode, HTMLAttributes } from 'react';

interface GlassPanelProps extends HTMLAttributes<HTMLDivElement> {
  children: ReactNode;
  className?: string;
}

const GlassPanel = forwardRef<HTMLDivElement, GlassPanelProps>(
  ({ children, className = '', style, ...props }, ref) => {
    return (
      <div
        ref={ref}
        className={`rounded-2xl ${className}`}
        style={{
          background: 'var(--glass-panel)',
          border: '1px solid var(--glass-border)',
          backdropFilter: 'blur(20px)',
          WebkitBackdropFilter: 'blur(20px)',
          boxShadow: '0 8px 32px rgba(0, 0, 0, 0.4)',
          ...style,
        }}
        {...props}
      >
        {children}
      </div>
    );
  }
);

GlassPanel.displayName = 'GlassPanel';

export default GlassPanel;
