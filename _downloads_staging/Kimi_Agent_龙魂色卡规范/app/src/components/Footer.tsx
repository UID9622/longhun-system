const footerColumns = [
  {
    title: '不动点协议',
    items: ['五主色定义', '不可变性条款', '机器识别标准', '版本历史'],
  },
  {
    title: '权重公式',
    items: ['三才平衡', '五行系统', '权重计算器', '铁律说明'],
  },
  {
    title: '五行系统',
    items: ['金木水火土', '生克关系', '配色规则', '应用场景'],
  },
  {
    title: '三才平衡',
    items: ['天地人', '权重分配', '平衡指数', '调参指南'],
  },
];

export default function Footer() {
  return (
    <footer
      className="w-full pt-16 pb-8 px-6 md:px-12"
      style={{
        backgroundColor: 'var(--spectrum-void)',
        borderTop: '1px solid var(--spectrum-border)',
      }}
    >
      {/* Row 1: Four columns */}
      <div className="max-w-[1440px] mx-auto grid grid-cols-2 md:grid-cols-4 gap-8 mb-12">
        {footerColumns.map((col) => (
          <div key={col.title}>
            <h4
              className="text-label font-noto-serif mb-4"
              style={{ color: 'var(--dragon-gold)' }}
            >
              {col.title}
            </h4>
            <ul className="space-y-2">
              {col.items.map((item) => (
                <li
                  key={item}
                  className="text-body font-noto-sans cursor-default transition-colors duration-200 hover:text-[var(--spectrum-bright)]"
                  style={{ color: 'var(--spectrum-dim)' }}
                >
                  {item}
                </li>
              ))}
            </ul>
          </div>
        ))}
      </div>

      {/* Row 2: Centered brand */}
      <div
        className="text-label font-noto-sans text-center mb-3"
        style={{ color: 'var(--spectrum-dim)' }}
      >
        龙魂生态 · 权重视觉系统
      </div>

      {/* Row 3: Version */}
      <div
        className="text-caption text-center mb-8"
        style={{ color: 'var(--spectrum-dim)' }}
      >
        v2.4.0 | Fixed Point Protocol
      </div>
    </footer>
  );
}
