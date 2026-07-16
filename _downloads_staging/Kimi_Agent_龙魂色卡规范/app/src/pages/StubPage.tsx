import { useLocation } from 'react-router';
import GlassPanel from '@/components/GlassPanel';

const pageNames: Record<string, string> = {
  colors: '不动点',
  weights: '权重面板',
  marquee: '七彩跑马灯',
  comparison: '各国色卡',
};

export default function StubPage() {
  const location = useLocation();
  const pageKey = location.pathname.replace(/^\//, '').split('/')[0];
  const name = pageNames[pageKey] || pageKey;

  return (
    <div
      className="min-h-[100dvh] flex items-center justify-center px-6"
      style={{ backgroundColor: 'var(--spectrum-void)' }}
    >
      <GlassPanel className="px-12 py-16 text-center max-w-md">
        <h1
          className="text-h1 font-noto-serif mb-4"
          style={{ color: 'var(--spectrum-peak)' }}
        >
          {name}
        </h1>
        <p
          className="text-body-lg font-noto-sans mb-6"
          style={{ color: 'var(--spectrum-medium)' }}
        >
          页面开发中...
        </p>
        <div
          className="inline-flex items-center gap-2 px-4 py-2 rounded-full text-label"
          style={{
            backgroundColor: 'rgba(255, 215, 0, 0.15)',
            color: 'var(--dragon-gold)',
          }}
        >
          即将推出
        </div>
      </GlassPanel>
    </div>
  );
}
